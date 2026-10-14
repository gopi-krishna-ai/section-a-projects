"""
train_fertilizer_model.py

Trains the FERTILIZER RECOMMENDATION model (Random Forest Classifier).

Dataset  : datasets/fertilizer_prediction.csv
Features : Temperature, Humidity, Moisture, Soil Type (cat), Crop Type (cat),
           Nitrogen, Potassium, Phosphorous
Target   : Fertilizer Name (7 classes: Urea, DAP, 28-28, 14-35-14, 20-20, 17-17-17, 10-26-26)

Output   : models/fertilizer_model.joblib (pipeline + encoders)
           models/fertilizer_model_metrics.json

Run:  python ml/train_fertilizer_model.py
"""

import json
import os

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATASET_PATH = os.path.join(BASE_DIR, "datasets", "fertilizer_prediction.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODELS_DIR, "fertilizer_model.joblib")
METRICS_PATH = os.path.join(MODELS_DIR, "fertilizer_model_metrics.json")

# Canonical feature names. The raw CSV uses 'Temparature' (typo) and
# 'Humidity ' (trailing space), so columns are normalised before use.
NUMERIC_COLUMNS = ["Temperature", "Humidity", "Moisture", "Nitrogen", "Potassium", "Phosphorous"]
CATEGORICAL_COLUMNS = ["Soil Type", "Crop Type"]
FEATURE_COLUMNS = NUMERIC_COLUMNS + CATEGORICAL_COLUMNS

RANDOM_STATE = 42


def load_and_validate_data():
    """Loads the dataset, normalises column names and validates structure."""
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Dataset not found: {DATASET_PATH}")

    df = pd.read_csv(DATASET_PATH)

    # Normalise column names: strip whitespace, fix the known 'Temparature' typo
    df.columns = [c.strip() for c in df.columns]
    rename = {"Temparature": "Temperature"}
    df = df.rename(columns=rename)

    missing = [c for c in FEATURE_COLUMNS + ["Fertilizer Name"] if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in dataset: {missing}")

    # Standardise categorical text (strip + title case)
    for c in CATEGORICAL_COLUMNS + ["Fertilizer Name"]:
        df[c] = df[c].astype(str).str.strip()

    print(f"Loaded {len(df)} rows")
    print(f"Missing values: {int(df[FEATURE_COLUMNS + ['Fertilizer Name']].isnull().sum().sum())}")
    print(f"Duplicate rows: {int(df.duplicated().sum())}")
    print(f"Soil types: {sorted(df['Soil Type'].unique())}")
    print(f"Crop types: {sorted(df['Crop Type'].unique())}")
    print(f"Fertilizer classes: {sorted(df['Fertilizer Name'].unique())}")

    return df


def main():
    os.makedirs(MODELS_DIR, exist_ok=True)

    df = load_and_validate_data()

    # Target encoding
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(df["Fertilizer Name"])
    X = df[FEATURE_COLUMNS]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

    # One-hot encode the two categorical features; keep numerics as-is
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", "passthrough", NUMERIC_COLUMNS),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_COLUMNS),
        ]
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", RandomForestClassifier(
                n_estimators=100, random_state=RANDOM_STATE, n_jobs=-1
            )),
        ]
    )

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    report = classification_report(
        y_test,
        y_pred,
        target_names=label_encoder.classes_,
        output_dict=True,
    )

    print(f"\nTest accuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)")
    print(f"Trained on {len(X_train)} rows, tested on {len(X_test)} rows")
    print("NOTE: dataset has only 99 rows; accuracy is measured on the held-out test set.")

    bundle = {
        "pipeline": pipeline,
        "label_encoder": label_encoder,
        "feature_columns": FEATURE_COLUMNS,
        "numeric_columns": NUMERIC_COLUMNS,
        "categorical_columns": CATEGORICAL_COLUMNS,
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
