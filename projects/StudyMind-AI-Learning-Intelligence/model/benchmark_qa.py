"""
AI Learning Intelligence - QA accuracy benchmark.

Measures the question-answering component against the REAL SQuAD v1.1 dev set
using the official Exact Match and token-level F1 metrics, so the project can
report a measured accuracy rather than asserting one.

Two settings are evaluated:

  reading      - the gold paragraph is given as context. Measures the QA model
                 alone.
  retrieval    - the question is asked against the whole document collection
                 and the system must FIND the right passage first. This is the
                 setting the app actually runs in, so it is the honest number
                 to quote for the product.

Run:
    python model/benchmark_qa.py [--n 300]
"""

import argparse
import json
import os
import re
import string
import sys
import time
from collections import Counter

import joblib
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
from utils import document_engine as de  # noqa: E402

DEV_PATH = os.path.join(BASE_DIR, "data", "kaggle_reference", "dev-v1.1.json")
OUT_PATH = os.path.join(BASE_DIR, "model", "qa_benchmark.pkl")


# ---- official SQuAD metric implementation -------------------------------
def normalise(s):
    s = s.lower()
    s = "".join(ch for ch in s if ch not in set(string.punctuation))
    s = re.sub(r"\b(a|an|the)\b", " ", s)
    return " ".join(s.split())


def exact_match(pred, golds):
    return float(any(normalise(pred) == normalise(g) for g in golds))


def f1(pred, golds):
    best = 0.0
    p_tokens = normalise(pred).split()
    for g in golds:
        g_tokens = normalise(g).split()
        common = Counter(p_tokens) & Counter(g_tokens)
        same = sum(common.values())
        if same == 0:
            continue
        precision = same / len(p_tokens)
        recall = same / len(g_tokens)
        best = max(best, 2 * precision * recall / (precision + recall))
    return best


def load_examples(limit):
    data = json.load(open(DEV_PATH, encoding="utf-8"))
    rows = []
    for article in data["data"]:
        for para in article["paragraphs"]:
            for qa in para["qas"]:
                rows.append({
                    "question": qa["question"],
                    "golds": [a["text"] for a in qa["answers"]],
                    "context": para["context"],
                    "title": article["title"],
                })
    rng = np.random.default_rng(42)
    idx = rng.permutation(len(rows))[:limit]
    return [rows[i] for i in idx]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=300)
    args = ap.parse_args()

    examples = load_examples(args.n)
    print(f"Evaluating {len(examples)} real SQuAD v1.1 dev questions\n")

    # ---------------- setting 1: reading comprehension ----------------
    em_scores, f1_scores = [], []
    start = time.time()
    for i, ex in enumerate(examples, 1):
        try:
            res = de.answer_from_context(ex["question"], ex["context"])
            pred = res["answer"]
        except Exception:
            pred = ""
        em_scores.append(exact_match(pred, ex["golds"]))
        f1_scores.append(f1(pred, ex["golds"]))
        if i % 50 == 0:
            print(f"  reading  {i}/{len(examples)}  "
                  f"EM={np.mean(em_scores):.3f} F1={np.mean(f1_scores):.3f}  "
                  f"({time.time() - start:.0f}s)")

    reading = {"exact_match": round(float(np.mean(em_scores)), 4),
               "f1": round(float(np.mean(f1_scores)), 4),
               "n": len(examples)}

    # ---------------- setting 2: retrieval + QA ----------------
    # Each unique paragraph becomes a "document"; the system must retrieve the
    # right one by embedding similarity before answering.
    unique_ctx = list({ex["context"] for ex in examples})
    print(f"\nBuilding a {len(unique_ctx)}-passage corpus for retrieval evaluation...")
    ctx_vecs = np.asarray(de.embedder().encode(unique_ctx, normalize_embeddings=True,
                                                show_progress_bar=False), dtype=np.float32)

    em_r, f1_r, retrieved_ok = [], [], []
    start = time.time()
    for i, ex in enumerate(examples, 1):
        qv = np.asarray(de.embedder().encode([ex["question"]], normalize_embeddings=True,
                                              show_progress_bar=False), dtype=np.float32)[0]
        sims = ctx_vecs @ qv
        top = int(np.argmax(sims))
        retrieved_ok.append(float(unique_ctx[top] == ex["context"]))
        try:
            res = de.answer_from_context(ex["question"], unique_ctx[top])
            pred = res["answer"]
        except Exception:
            pred = ""
        em_r.append(exact_match(pred, ex["golds"]))
        f1_r.append(f1(pred, ex["golds"]))
        if i % 50 == 0:
            print(f"  retrieval {i}/{len(examples)}  "
                  f"EM={np.mean(em_r):.3f} F1={np.mean(f1_r):.3f} "
                  f"retrieval@1={np.mean(retrieved_ok):.3f}  ({time.time() - start:.0f}s)")

    retrieval = {"exact_match": round(float(np.mean(em_r)), 4),
                 "f1": round(float(np.mean(f1_r)), 4),
                 "retrieval_accuracy": round(float(np.mean(retrieved_ok)), 4),
                 "n": len(examples), "corpus_passages": len(unique_ctx)}

    result = {
        "dataset": "SQuAD v1.1 dev (Stanford Question Answering Dataset)",
        "qa_model": de.QA_MODEL,
        "embedding_model": de.EMBED_MODEL,
        "reading": reading,
        "retrieval": retrieval,
    }

    print("\n" + "=" * 60)
    print(f"READING (gold passage given)   EM {reading['exact_match']:.1%}  F1 {reading['f1']:.1%}")
    print(f"RETRIEVAL (must find passage)  EM {retrieval['exact_match']:.1%}  "
          f"F1 {retrieval['f1']:.1%}  retrieval@1 {retrieval['retrieval_accuracy']:.1%}")
    print("=" * 60)

    joblib.dump(result, OUT_PATH)
    print(f"\nSaved -> {OUT_PATH}")


if __name__ == "__main__":
    main()
