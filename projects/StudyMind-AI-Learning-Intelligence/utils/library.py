"""
AI Learning Intelligence - document library.

Holds every uploaded document's extracted text, chunks and embeddings, and
provides semantic search and question answering BOTH within a single document
and ACROSS the whole library - the cross-document understanding the abstract
lists as the main gap in existing systems.

Embeddings live in memory; the text and derived study material are persisted
to a JSON file so the library survives a restart.
"""

import json
import os
import tempfile
import threading

import numpy as np

from utils import document_engine as de

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORE_PATH = os.path.join(BASE_DIR, "data", "library.json")

_lock = threading.RLock()
_embeddings = {}          # doc_id -> np.ndarray  (in memory only)


# ---------------------------------------------------------------------------
# persistence
# ---------------------------------------------------------------------------
def _read():
    if not os.path.exists(STORE_PATH):
        return {"documents": []}
    try:
        with open(STORE_PATH, encoding="utf-8") as f:
            data = json.load(f)
        data.setdefault("documents", [])
        return data
    except (json.JSONDecodeError, OSError):
        return {"documents": []}


def _write(data):
    os.makedirs(os.path.dirname(STORE_PATH), exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(STORE_PATH), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=1)
        os.replace(tmp, STORE_PATH)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def _ensure_embeddings(doc):
    """Rebuild a document's embedding matrix if it is not in memory (e.g. after
    a restart, since embeddings are not persisted)."""
    did = doc["id"]
    if did in _embeddings:
        return _embeddings[did]
    texts = [c["text"] for c in doc["chunks"]]
    if not texts:
        _embeddings[did] = np.zeros((0, 384), dtype=np.float32)
        return _embeddings[did]
    vecs = de.embedder().encode(texts, normalize_embeddings=True, show_progress_bar=False)
    _embeddings[did] = np.asarray(vecs, dtype=np.float32)
    return _embeddings[did]


# ---------------------------------------------------------------------------
# ingestion
# ---------------------------------------------------------------------------
def add_document(path, original_name):
    extracted = de.extract(path)
    text = extracted.get("text", "")
    if len(text.strip()) < 40:
        return {"error": "No readable text found. If this is a scanned document, "
                          "ensure Tesseract OCR is installed."}

    chunks = de.chunk_pages(extracted["pages"])
    if not chunks:
        return {"error": "Document produced no usable text chunks."}

    concepts = de.key_concepts(text)
    language = de.detect_language(text)

    vecs = de.embedder().encode([c["text"] for c in chunks],
                                normalize_embeddings=True, show_progress_bar=False)
    vecs = np.asarray(vecs, dtype=np.float32)

    topics = de.organise_topics(chunks, vecs, concepts)

    doc = {
        "id": f"doc_{abs(hash((original_name, len(text)))) % (10 ** 10)}",
        "name": original_name,
        "pages": len(extracted["pages"]),
        "ocr_pages": extracted.get("ocr_pages", []),
        "characters": len(text),
        "words": len(text.split()),
        "language": language,
        "text": text,
        "chunks": chunks,
        "concepts": concepts,
        "topics": topics,
        "exam_topics": de.exam_topics(concepts, topics),
        "study_plan": de.study_plan(concepts, topics),
    }

    with _lock:
        data = _read()
        data["documents"] = [d for d in data["documents"] if d["name"] != original_name]
        data["documents"].append(doc)
        _write(data)
    _embeddings[doc["id"]] = vecs
    return doc


def list_documents():
    data = _read()
    return [{"id": d["id"], "name": d["name"], "pages": d["pages"], "words": d["words"],
             "language": d["language"], "ocr_pages": d.get("ocr_pages", []),
             "topic_count": len(d.get("topics", []))}
            for d in data["documents"]]


def get_document(doc_id):
    for d in _read()["documents"]:
        if d["id"] == doc_id:
            return d
    return None


def delete_document(doc_id):
    with _lock:
        data = _read()
        before = len(data["documents"])
        data["documents"] = [d for d in data["documents"] if d["id"] != doc_id]
        _write(data)
    _embeddings.pop(doc_id, None)
    return len(data["documents"]) < before


# ---------------------------------------------------------------------------
# semantic search
# ---------------------------------------------------------------------------
def semantic_search(query, doc_id=None, top_k=6):
    """Rank chunks by embedding cosine similarity.

    This is genuine semantic matching, not keyword matching: a query can score
    highly against a passage that shares no literal words with it.
    """
    docs = _read()["documents"]
    if doc_id:
        docs = [d for d in docs if d["id"] == doc_id]
    if not docs:
        return []

    qv = np.asarray(de.embedder().encode([query], normalize_embeddings=True,
                                          show_progress_bar=False), dtype=np.float32)[0]

    hits = []
    for doc in docs:
        vecs = _ensure_embeddings(doc)
        if vecs.shape[0] == 0:
            continue
        sims = vecs @ qv
        for i in np.argsort(sims)[-top_k:][::-1]:
            hits.append({
                "doc_id": doc["id"], "doc_name": doc["name"],
                "page": doc["chunks"][i]["page"],
                "text": doc["chunks"][i]["text"],
                "score": round(float(sims[i]), 4),
            })
    hits.sort(key=lambda h: h["score"], reverse=True)
    return hits[:top_k]


# ---------------------------------------------------------------------------
# question answering (single doc or across the library)
# ---------------------------------------------------------------------------
def ask(question, doc_id=None, n_context=5):
    """Use semantic retrieval + extractive QA for grounded document answers.

    This remains the document-only path. The Flask API also exposes /api/ask-ai,
    which uses the same retrieval results as context for an optional local LLM.
    """
    passages = semantic_search(question, doc_id=doc_id, top_k=n_context)
    if not passages:
        return {"error": "No documents available. Upload a PDF or note first."}

    best, best_passage = None, None
    for p in passages:
        try:
            res = de.answer_from_context(question, p["text"])
        except Exception:
            continue
        if res["answer"] and (best is None or res["score"] > best["score"]):
            best, best_passage = res, p

    if not best or not best["answer"]:
        return {"answer": None, "message": "No confident extractive answer found. Try Ask AI for an open-ended answer.",
                "sources": passages}

    return {
        "answer": best["answer"],
        "confidence": best["confidence"],
        "source": {"doc_name": best_passage["doc_name"], "page": best_passage["page"],
                    "doc_id": best_passage["doc_id"]},
        "context": best_passage["text"],
        "sources": passages,
    }


# ---------------------------------------------------------------------------
# study material
# ---------------------------------------------------------------------------
def study_pack(doc_id):
    doc = get_document(doc_id)
    if not doc:
        return {"error": "Document not found."}

    extractive = de.extractive_summary(doc["text"])
    try:
        abstractive = de.abstractive_summary(" ".join(extractive) or doc["text"][:3000])
    except Exception:
        abstractive = None

    return {
        "doc_id": doc["id"],
        "name": doc["name"],
        "language": doc["language"],
        "summary_extractive": extractive,
        "summary_abstractive": abstractive,
        "concepts": doc["concepts"],
        "topics": doc["topics"],
        "exam_topics": doc["exam_topics"],
        "study_plan": doc["study_plan"],
        "flashcards": de.build_flashcards(doc["text"], doc["concepts"]),
        "quiz": de.build_quiz(doc["text"], doc["concepts"], doc["chunks"]),
    }


def explain_concept(doc_id, term):
    """Explain a term in simpler language, grounded in the document."""
    doc = get_document(doc_id)
    if not doc:
        return {"error": "Document not found."}
    hits = semantic_search(term, doc_id=doc_id, top_k=2)
    if not hits:
        return {"error": "Nothing found for that term."}
    context = " ".join(h["text"] for h in hits)
    try:
        simple = de.simplify(context)
    except Exception:
        simple = context[:300]
    return {"term": term, "explanation": simple,
            "source_page": hits[0]["page"], "context": hits[0]["text"]}
