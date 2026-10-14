"""
train_crop_model.py

Trains the CROP RECOMMENDATION model (Random Forest Classifier).

Dataset  : datasets/crop_recommendation.csv
Features : Nitrogen, Phosphorus, Potassium, Temperature, Humidity, pH_Value, Rainfall
Target   : Crop (22 crop classes)

Output   : models/crop_model.joblib  (contains the trained pipeline)
           models/crop_model_metrics.json  (measured accuracy / report)

Run:  python ml/train_crop_model.py
"""

import json
import os

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATASET_PATH = os.path.join(BASE_DIR, "datasets", "crop_recommendation.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODELS_DIR, "crop_model.joblib")
METRICS_PATH = os.path.join(MODELS_DIR, "crop_model_metrics.json")

# Feature order used for training AND prediction (must stay identical).
FEATURE_COLUMNS = [
    "Nitrogen",
    "Phosphorus",
    "Potassium",
    "Temperature",
    "Humidity",
    "pH_Value",
    "Rainfall",
]

RANDOM_STATE = 42


def load_and_validate_data():
    """Loads the dataset and validates its structure."""
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Dataset not found: {DATASET_PATH}")

    df = pd.read_csv(DATASET_PATH)

    missing = [c for c in FEATURE_COLUMNS + ["Crop"] if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in dataset: {missing}")

    print(f"Loaded {len(df)} rows, {len(df.columns)} columns")
    print(f"Missing values: {int(df[FEATURE_COLUMNS + ['Crop']].isnull().sum().sum())}")
    print(f"Duplicate rows: {int(df.duplicated().sum())}")
    print(f"Crop classes: {df['Crop'].nunique()}")

    return df


def main():
    os.makedirs(MODELS_DIR, exist_ok=True)

    df = load_and_validate_data()

    # Encode target labels (crop names -> integers)
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(df["Crop"])
    X = df[FEATURE_COLUMNS]

    # Train/test split (stratified keeps every crop represented in both sets)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

    # Random Forest Classifier
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    # Evaluation on the held-out test set
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    report = classification_report(
        y_test,
        y_pred,
        target_names=label_encoder.classes_,
        output_dict=True,
    )

    print(f"\nTest accuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)")
    print(f"Trained on {len(X_train)} rows, tested on {len(X_test)} rows")

    # Save model + label encoder together (joblib preserves feature order in the
    # fitted trees; the FEATURE_COLUMNS list is stored with the bundle as a guard)
    bundle = {
        "model": model,
        "label_encoder": label_encoder,
        "feature_columns": FEATURE_COLUMNS,
        "classes": label_encoder.classes_.tolist(),
        "accuracy": accuracy,
        "trained_rows": len(df),
    }
    joblib.dump(bundle, MODEL_PATH)

    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(
            {
                "accuracy": round(float(accuracy), 4),
                "classes": len(label_encoder.classes_),
                "trained_rows": len(df),
                "classification_report": report,
            },
            f,
            indent=2,
        )

    print(f"Model saved to: {MODEL_PATH}")
    print(f"Metrics saved to: {METRICS_PATH}")


if __name__ == "__main__":
    main()
