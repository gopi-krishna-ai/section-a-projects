"""
AI Learning Intelligence for Notes and PDF Analysis - document engine.

Turns an uploaded PDF or scanned/handwritten note into an interactive study
resource, covering the pipeline the abstract describes:

    PDF / image  ->  text extraction (PyMuPDF)  ->  OCR fallback (Tesseract)
                 ->  chunking + sentence embeddings (MiniLM)
                 ->  semantic search, extractive + abstractive summaries,
                     key concepts, question answering (DistilBERT-SQuAD),
                     flashcards, quizzes, topic organisation, study plan

Model notes
-----------
transformers 5.x removed the `question-answering` and `summarization` pipeline
tasks, so both are driven through their model classes directly
(`AutoModelForQuestionAnswering`, `AutoModelForSeq2SeqLM`) with the span /
generation logic implemented here. Models are loaded lazily and cached, so the
first call pays the load cost and later calls are fast.
"""

import math
import os
import re
import threading
from collections import Counter

import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

EMBED_MODEL = "all-MiniLM-L6-v2"
QA_MODEL = "distilbert-base-cased-distilled-squad"
SUMMARY_MODEL = "t5-small"

# Common Windows install location - pytesseract needs an explicit path when
# tesseract.exe is not on PATH (which is the default on this machine).
TESSERACT_PATHS = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
]

_models = {}
_lock = threading.Lock()

STOPWORDS = set("""
a an the and or but if while of at by for with about against between into through during before
after above below to from up down in out on off over under again further then once here there
when where why how all any both each few more most other some such no nor not only own same so
than too very s t can will just don should now is are was were be been being have has had having
do does did doing this that these those i you he she it we they them his her its our their as
also may might must shall would could one two three new used using use used based can't cannot
which what who whom whose whether because since however therefore thus hence although though
been being upon within without along across among around another many much several every either
neither various given often usually generally particularly especially example examples following
above below like unlike due including included include includes according respectively etc
""".split())


# ---------------------------------------------------------------------------
# lazy model loading
# ---------------------------------------------------------------------------
def _get(name, builder):
    if name in _models:
        return _models[name]
    with _lock:
        if name not in _models:
            _models[name] = builder()
    return _models[name]


def embedder():
    def build():
        from sentence_transformers import SentenceTransformer
        return SentenceTransformer(EMBED_MODEL)
    return _get("embed", build)


def qa_model():
    def build():
        import torch
        from transformers import AutoModelForQuestionAnswering, AutoTokenizer
        tok = AutoTokenizer.from_pretrained(QA_MODEL)
        mdl = AutoModelForQuestionAnswering.from_pretrained(QA_MODEL)
        mdl.eval()
        return {"tok": tok, "model": mdl, "torch": torch}
    return _get("qa", build)


def summary_model():
    def build():
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
        tok = AutoTokenizer.from_pretrained(SUMMARY_MODEL)
        mdl = AutoModelForSeq2SeqLM.from_pretrained(SUMMARY_MODEL)
        mdl.eval()
        return {"tok": tok, "model": mdl}
    return _get("sum", build)


# ---------------------------------------------------------------------------
# text extraction  (+ OCR)
# ---------------------------------------------------------------------------
def _configure_tesseract():
    import pytesseract
    import shutil
    if shutil.which("tesseract"):
        return pytesseract
    for p in TESSERACT_PATHS:
        if os.path.exists(p):
            pytesseract.pytesseract.tesseract_cmd = p
            return pytesseract
    return None


def ocr_available():
    try:
        return _configure_tesseract() is not None
    except Exception:
        return False


def extract_from_pdf(path, ocr_threshold=40):
    """Extract text page by page.

    A page with almost no embedded text is treated as scanned and rendered to
    an image for OCR, which is how handwritten/scanned notes are supported.
    """
    import fitz

    pages, ocr_pages = [], []
    doc = fitz.open(path)
    try:
        pyt = _configure_tesseract()
        for i, page in enumerate(doc):
            text = (page.get_text() or "").strip()
            if len(text) < ocr_threshold and pyt is not None:
                try:
                    from PIL import Image
                    pix = page.get_pixmap(dpi=200)
                    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
                    ocr_text = (pyt.image_to_string(img) or "").strip()
                    if len(ocr_text) > len(text):
                        text = ocr_text
                        ocr_pages.append(i + 1)
                except Exception:
                    pass                      # keep whatever embedded text existed
            pages.append({"page": i + 1, "text": text})
    finally:
        doc.close()

    return {"pages": pages, "ocr_pages": ocr_pages,
            "text": "\n\n".join(p["text"] for p in pages if p["text"])}


def extract_from_image(path):
    pyt = _configure_tesseract()
    if pyt is None:
        return {"pages": [], "ocr_pages": [], "text": "",
                "error": "Tesseract OCR is not installed."}
    from PIL import Image
    text = (pyt.image_to_string(Image.open(path)) or "").strip()
    return {"pages": [{"page": 1, "text": text}], "ocr_pages": [1], "text": text}


def extract_from_text_file(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        text = f.read()
    return {"pages": [{"page": 1, "text": text}], "ocr_pages": [], "text": text}


def extract(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return extract_from_pdf(path)
    if ext in (".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"):
        return extract_from_image(path)
    return extract_from_text_file(path)


# ---------------------------------------------------------------------------
# language detection (multilingual support)
# ---------------------------------------------------------------------------
LANGUAGE_NAMES = {
    "en": "English", "hi": "Hindi", "kn": "Kannada", "ta": "Tamil", "te": "Telugu",
    "ml": "Malayalam", "mr": "Marathi", "bn": "Bengali", "gu": "Gujarati", "pa": "Punjabi",
    "ur": "Urdu", "fr": "French", "de": "German", "es": "Spanish", "pt": "Portuguese",
    "it": "Italian", "nl": "Dutch", "ru": "Russian", "ar": "Arabic", "zh-cn": "Chinese",
    "ja": "Japanese", "ko": "Korean",
}


def detect_language(text):
    sample = (text or "")[:3000].strip()
    if len(sample) < 20:
        return {"code": "unknown", "name": "Unknown"}
    try:
        from langdetect import DetectorFactory, detect
        DetectorFactory.seed = 0
        code = detect(sample)
        return {"code": code, "name": LANGUAGE_NAMES.get(code, code.upper())}
    except Exception:
        return {"code": "unknown", "name": "Unknown"}


# ---------------------------------------------------------------------------
# chunking + sentence splitting
# ---------------------------------------------------------------------------
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\u0900-\u0DFF])")


def split_sentences(text, min_len=25):
    raw = SENT_SPLIT.split(re.sub(r"\s+", " ", text or ""))
    return [s.strip() for s in raw if len(s.strip()) >= min_len]


def chunk_pages(pages, target_chars=900, overlap=150):
    """Split into overlapping chunks, keeping the page number for citation."""
    chunks = []
    for p in pages:
        text = re.sub(r"\s+", " ", p["text"] or "").strip()
        if not text:
            continue
        start = 0
        while start < len(text):
            end = min(len(text), start + target_chars)
            if end < len(text):                     # avoid cutting mid-word
                space = text.rfind(" ", start + int(target_chars * 0.6), end)
                if space > start:
                    end = space
            body = text[start:end].strip()
            if len(body) > 60:
                chunks.append({"page": p["page"], "text": body})
            if end >= len(text):
                break
            start = max(end - overlap, start + 1)
    return chunks


# ---------------------------------------------------------------------------
# key concepts
# ---------------------------------------------------------------------------
def key_concepts(text, top_n=15):
    """Score candidate terms by TF, boosted for multi-word phrases and for
    capitalised (likely technical/proper) terms."""
    words = re.findall(r"[A-Za-z][A-Za-z\-']+", text or "")
    lower = [w.lower() for w in words]

    unigrams = Counter(w for w in lower if w not in STOPWORDS and len(w) > 3)
    bigrams = Counter()
    for i in range(len(lower) - 1):
        a, b = lower[i], lower[i + 1]
        if a not in STOPWORDS and b not in STOPWORDS and len(a) > 2 and len(b) > 2:
            bigrams[f"{a} {b}"] += 1

    capitalised = Counter(w.lower() for w in words if w[0].isupper() and w.lower() not in STOPWORDS)

    scores = {}
    for term, count in unigrams.items():
        if count < 2:
            continue
        scores[term] = count * (1.6 if capitalised.get(term, 0) >= max(1, count // 2) else 1.0)
    for term, count in bigrams.items():
        if count >= 2:
            scores[term] = count * 2.2                # phrases are more informative

    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)

    # Drop a unigram if it is already covered by a higher-ranked phrase.
    chosen, seen_words = [], set()
    for term, score in ranked:
        parts = set(term.split())
        if " " not in term and parts & seen_words:
            continue
        chosen.append({"term": term, "score": round(float(score), 1),
                        "occurrences": int(unigrams.get(term) or bigrams.get(term) or 0)})
        seen_words |= parts
        if len(chosen) >= top_n:
            break
    return chosen


# ---------------------------------------------------------------------------
# summarisation
# ---------------------------------------------------------------------------
def extractive_summary(text, max_sentences=6):
    """Embedding-based TextRank.

    Sentences are ranked by centrality in a cosine-similarity graph (a
    TextRank-style approach, but scored with MiniLM sentence embeddings rather
    than word overlap). Selected sentences are returned in original order.
    """
    sentences = split_sentences(text)
    if not sentences:
        return []
    if len(sentences) <= max_sentences:
        return sentences

    sentences = sentences[:250]                   # cap cost on very long documents
    emb = embedder().encode(sentences, normalize_embeddings=True, show_progress_bar=False)
    sim = np.asarray(emb) @ np.asarray(emb).T
    np.fill_diagonal(sim, 0.0)

    # Power iteration over the row-normalised similarity matrix.
    row_sums = sim.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1.0
    transition = sim / row_sums
    scores = np.ones(len(sentences)) / len(sentences)
    for _ in range(30):
        scores = 0.15 / len(sentences) + 0.85 * (transition.T @ scores)

    top_idx = sorted(np.argsort(scores)[-max_sentences:])
    return [sentences[i] for i in top_idx]


def abstractive_summary(text, max_length=110, min_length=30):
    """Generate a new summary with T5 (rather than selecting existing lines)."""
    m = summary_model()
    body = re.sub(r"\s+", " ", text or "").strip()
    if len(body) < 200:
        return None
    ids = m["tok"]("summarize: " + body, return_tensors="pt",
                    truncation=True, max_length=512)
    out = m["model"].generate(**ids, max_length=max_length, min_length=min_length,
                               num_beams=4, length_penalty=2.0, no_repeat_ngram_size=3)
    return m["tok"].decode(out[0], skip_special_tokens=True).strip()


def simplify(text, max_length=90):
    """'Explain this in simpler language' - a shorter, plainer restatement."""
    m = summary_model()
    body = re.sub(r"\s+", " ", text or "").strip()
    if len(body) < 80:
        return body
    ids = m["tok"]("summarize: " + body, return_tensors="pt", truncation=True, max_length=512)
    out = m["model"].generate(**ids, max_length=max_length, min_length=20,
                               num_beams=4, length_penalty=1.0, no_repeat_ngram_size=3)
    return m["tok"].decode(out[0], skip_special_tokens=True).strip()


# ---------------------------------------------------------------------------
# question answering
# ---------------------------------------------------------------------------
def answer_from_context(question, context, max_len=384, stride=128):
    """Extractive QA over one context, sliding a window over long passages."""
    m = qa_model()
    torch = m["torch"]
    tok, model = m["tok"], m["model"]

    enc = tok(question, context, return_tensors="pt", truncation="only_second",
              max_length=max_len, stride=stride, return_overflowing_tokens=True,
              padding="max_length")
    n_windows = enc["input_ids"].shape[0]

    best = {"score": -1e9, "answer": "", "start": 0, "end": 0}
    for w in range(n_windows):
        inputs = {"input_ids": enc["input_ids"][w].unsqueeze(0),
                  "attention_mask": enc["attention_mask"][w].unsqueeze(0)}
        with torch.no_grad():
            out = model(**inputs)
        start_logits = out.start_logits[0]
        end_logits = out.end_logits[0]

        seq_ids = enc.sequence_ids(w)
        # Only allow spans inside the context segment (sequence id 1).
        mask = torch.tensor([1 if s == 1 else 0 for s in seq_ids], dtype=torch.bool)
        start_logits = start_logits.masked_fill(~mask, -1e9)
        end_logits = end_logits.masked_fill(~mask, -1e9)

        # Softmax over the window gives a real span probability. Using the raw
        # logit sum instead saturates a sigmoid to 1.0 for almost every answer,
        # which would show "100% confidence" even when the span is wrong.
        start_probs = torch.softmax(start_logits, dim=-1)
        end_probs = torch.softmax(end_logits, dim=-1)

        top_starts = torch.topk(start_logits, k=min(20, start_logits.shape[0])).indices
        top_ends = torch.topk(end_logits, k=min(20, end_logits.shape[0])).indices
        for s in top_starts:
            for e in top_ends:
                if e < s or (e - s) > 60:
                    continue
                score = float(start_logits[s] + end_logits[e])
                if score > best["score"]:
                    span = tok.decode(enc["input_ids"][w][s:e + 1], skip_special_tokens=True)
                    if span.strip():
                        best = {"score": score, "answer": span.strip(),
                                "start": int(s), "end": int(e),
                                "probability": float(start_probs[s] * end_probs[e])}

    best["confidence"] = round(best.get("probability", 0.0), 3)
    return best


# ---------------------------------------------------------------------------
# flashcards + quizzes
# ---------------------------------------------------------------------------
def _definition_sentences(sentences, term):
    pat = re.compile(r"\b" + re.escape(term) + r"\b", re.IGNORECASE)
    return [s for s in sentences if pat.search(s)]


def build_flashcards(text, concepts, limit=10):
    """Term -> definition cards, sourced from the sentence that best explains
    each key concept (shortened with the summariser when long)."""
    sentences = split_sentences(text)
    cards = []
    for c in concepts:
        matches = _definition_sentences(sentences, c["term"])
        if not matches:
            continue
        # prefer an explicit definitional sentence
        definitional = [s for s in matches
                        if re.search(r"\b(is|are|means|refers to|defined as|consists of)\b", s, re.I)]
        best = (definitional or matches)[0]
        answer = best if len(best) <= 240 else simplify(best)
        cards.append({"front": c["term"].title(), "back": answer.strip(),
                       "occurrences": c["occurrences"]})
        if len(cards) >= limit:
            break
    return cards


def build_quiz(text, concepts, chunks, limit=6):
    """Generate MCQs.

    The stem is a real sentence from the document with the key term blanked
    out; the correct answer is that term and the distractors are other key
    terms from the same document, so every option is plausible in context.
    """
    import random
    rng = random.Random(42)

    sentences = split_sentences(text)
    pool = [c["term"] for c in concepts]
    questions = []

    for c in concepts:
        if len(questions) >= limit:
            break
        matches = _definition_sentences(sentences, c["term"])
        if not matches:
            continue

        # Prefer definitional sentences ("X is ...", "X refers to ...")
        # over arbitrary mentions, and skip very short fragments.
        definitional = [s for s in matches
                        if re.search(r"\b(is|are|means|refers to|defined as|consists of|involves|describes)\b", s, re.I)
                        and len(s) >= 50]
        candidates = definitional or [s for s in matches if len(s) >= 50]
        if not candidates:
            continue

        # Pick a medium-length sentence (not too short, not too long)
        candidates.sort(key=len)
        sentence = candidates[min(len(candidates) // 2, len(candidates) - 1)]
        if len(sentence) > 260:
            sentence = candidates[0]
        if len(sentence) > 260 or len(sentence) < 40:
            continue

        blanked = re.sub(r"\b" + re.escape(c["term"]) + r"\b", "________", sentence, count=1,
                          flags=re.IGNORECASE)

        # Skip if blank wasn't actually inserted (term not found as whole word)
        if "________" not in blanked:
            continue

        distractors = [t for t in pool if t != c["term"] and t not in c["term"] and c["term"] not in t]
        if len(distractors) < 3:
            continue
        options = rng.sample(distractors, 3) + [c["term"]]
        rng.shuffle(options)
        questions.append({
            "question": f"Fill in the blank: {blanked}",
            "options": [o.title() for o in options],
            "answer": c["term"].title(),
            "explanation": f"The correct answer is {c['term'].title()}. As stated in the document: \"{sentence.strip()}\"",
        })
    return questions


# ---------------------------------------------------------------------------
# topic organisation + study plan
# ---------------------------------------------------------------------------
def organise_topics(chunks, embeddings, concepts, n_topics=5):
    """Group chunks into topics with KMeans over their embeddings, labelling
    each cluster with the key concepts most frequent inside it."""
    if len(chunks) < 3:
        return [{"topic": "Full document", "label": "Full document",
                 "chunk_count": len(chunks), "pages": sorted({c["page"] for c in chunks})}]

    from sklearn.cluster import KMeans
    k = max(2, min(n_topics, len(chunks) // 2))
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(embeddings)

    terms = [c["term"] for c in concepts]
    topics = []
    for cid in range(k):
        idx = [i for i, l in enumerate(labels) if l == cid]
        if not idx:
            continue
        body = " ".join(chunks[i]["text"] for i in idx).lower()
        hits = sorted(((t, body.count(t)) for t in terms), key=lambda kv: kv[1], reverse=True)
        label = ", ".join(t.title() for t, n in hits[:3] if n > 0) or f"Section {cid + 1}"
        topics.append({
            "topic": f"Topic {cid + 1}",
            "label": label,
            "chunk_count": len(idx),
            "pages": sorted({chunks[i]["page"] for i in idx}),
            "preview": chunks[idx[0]]["text"][:180],
        })
    topics.sort(key=lambda t: t["chunk_count"], reverse=True)
    return topics


def exam_topics(concepts, topics, limit=6):
    """Likely exam focus: concepts that recur most and span several topics."""
    ranked = []
    for c in concepts[:limit * 2]:
        spread = sum(1 for t in topics if c["term"] in (t.get("label", "").lower()))
        ranked.append({"term": c["term"].title(), "occurrences": c["occurrences"],
                        "importance": round(c["score"] + spread * 5, 1)})
    ranked.sort(key=lambda r: r["importance"], reverse=True)
    return ranked[:limit]


def study_plan(concepts, topics, n_days=5):
    """Split topics across study days, heaviest first."""
    if not topics:
        return []
    plan = []
    days = min(n_days, len(topics))
    for d in range(days):
        assigned = topics[d::days]
        plan.append({
            "day": d + 1,
            "focus": [t["label"] for t in assigned],
            "pages": sorted({p for t in assigned for p in t["pages"]}),
            "chunks": sum(t["chunk_count"] for t in assigned),
        })
    return plan
