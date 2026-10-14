"""
AI-Assisted Smart Study Planner - Model training script.

Trains a Random Forest classifier that predicts a subject's study
priority (High / Medium / Low) from days-to-exam, syllabus completion
percentage, difficulty, and exam weightage.

Run:
    python train_model.py
"""

import os

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "priority_dataset.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model", "study_priority_rf_model.pkl")

FEATURES = ["days_to_exam", "completion_pct", "difficulty", "weightage"]
TARGET = "priority"


def main():
    df = pd.read_csv(DATA_PATH)

    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(n_estimators=200, max_depth=8, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"Test accuracy: {accuracy:.2%}")
    print(classification_report(y_test, y_pred))

    print("Feature importances:")
    for feature, importance in zip(FEATURES, model.feature_importances_):
        print(f"  {feature}: {importance:.3f}")

    joblib.dump(model, MODEL_PATH)
    print(f"Model saved -> {MODEL_PATH}")


if __name__ == "__main__":
    main()
