"""
ResQAI - model training and comparison.

Trains and compares the four classifiers named in the project abstract
(Logistic Regression, Support Vector Machine, Naive Bayes, Random Forest)
on the real Kaggle Disaster Tweets dataset, using TF-IDF features built
from the abstract's preprocessing chain.

The best model by F1 is saved for the dashboard to use.

Run:
    python model/train_models.py
"""

import os
import sys

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, classification_report, confusion_matrix,
                              f1_score, precision_score, recall_score, roc_auc_score)
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
from utils.preprocessing import build_corpus  # noqa: E402

DATA_PATH = os.path.join(BASE_DIR, "data", "kaggle_reference", "train.csv")
MODEL_DIR = os.path.join(BASE_DIR, "model")

RANDOM_STATE = 42


def build_candidates():
    return {
        "Logistic Regression": LogisticRegression(C=2.0, max_iter=1000,
                                                   random_state=RANDOM_STATE),
        "Support Vector Machine": LinearSVC(C=0.5, random_state=RANDOM_STATE),
        "Naive Bayes": MultinomialNB(alpha=0.5),
        "Random Forest": RandomForestClassifier(n_estimators=300, max_depth=None,
                                                 min_samples_leaf=2, n_jobs=-1,
                                                 random_state=RANDOM_STATE),
    }


def main():
    df = pd.read_csv(DATA_PATH)
    print(f"Loaded {len(df):,} real tweets "
          f"({int((df.target == 1).sum()):,} disaster, {int((df.target == 0).sum()):,} not)")

    print("Preprocessing (clean -> tokenize -> stop-words -> stemming)...")
    corpus = build_corpus(df)
    y = df["target"].values

    X_train_txt, X_test_txt, y_train, y_test = train_test_split(
        corpus, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

    vectorizer = TfidfVectorizer(max_features=30000, ngram_range=(1, 2), min_df=1,
                                  sublinear_tf=True)
    X_train = vectorizer.fit_transform(X_train_txt)
    X_test = vectorizer.transform(X_test_txt)
    print(f"TF-IDF matrix: {X_train.shape[0]:,} x {X_train.shape[1]:,} features\n")

    results = {}
    print(f"{'Model':<24}{'Accuracy':>10}{'Precision':>11}{'Recall':>9}{'F1':>8}{'CV-F1':>8}")
    print("-" * 70)

    for name, model in build_candidates().items():
        model.fit(X_train, y_train)
        pred = model.predict(X_test)

        acc = accuracy_score(y_test, pred)
        prec = precision_score(y_test, pred)
        rec = recall_score(y_test, pred)
        f1 = f1_score(y_test, pred)
        cv = cross_val_score(model, X_train, y_train, cv=5, scoring="f1", n_jobs=-1).mean()

        results[name] = {
            "model": model, "accuracy": round(acc, 4), "precision": round(prec, 4),
            "recall": round(rec, 4), "f1": round(f1, 4), "cv_f1": round(cv, 4),
            "confusion": confusion_matrix(y_test, pred).tolist(),
        }
        print(f"{name:<24}{acc:>10.4f}{prec:>11.4f}{rec:>9.4f}{f1:>8.4f}{cv:>8.4f}")

    best_name = max(results, key=lambda k: results[k]["f1"])
    best = results[best_name]
    print(f"\nBest model: {best_name} (F1 = {best['f1']:.4f})\n")
    print(classification_report(y_test, best["model"].predict(X_test),
                                 target_names=["Not Disaster", "Disaster"]))

    # LinearSVC has no predict_proba; the dashboard needs a confidence score, so
    # record how to derive one (decision_function -> sigmoid) per model type.
    best_model = best["model"]
    supports_proba = hasattr(best_model, "predict_proba")

    joblib.dump(best_model, os.path.join(MODEL_DIR, "resqai_classifier.pkl"))
    joblib.dump(vectorizer, os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl"))
    joblib.dump({
        "best_model": best_name,
        "supports_proba": supports_proba,
        "n_train": int(len(y_train)),
        "n_test": int(len(y_test)),
        "n_features": int(X_train.shape[1]),
        "dataset": "Kaggle - Natural Language Processing with Disaster Tweets",
        "scores": {k: {m: v[m] for m in ("accuracy", "precision", "recall", "f1", "cv_f1", "confusion")}
                    for k, v in results.items()},
    }, os.path.join(MODEL_DIR, "model_metrics.pkl"))

    print(f"Saved best model + vectorizer + metrics -> {MODEL_DIR}")


if __name__ == "__main__":
    main()
