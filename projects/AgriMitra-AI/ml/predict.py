"""
prediction utilities

Loads the saved ML models once and exposes prediction functions.
Feature order is always taken from the saved bundle (the same order
used during training) to avoid training/prediction mismatches.
"""

import os
import threading

import joblib

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODELS_DIR = os.path.join(BASE_DIR, "models")

CROP_MODEL_PATH = os.path.join(MODELS_DIR, "crop_model.joblib")
FERTILIZER_MODEL_PATH = os.path.join(MODELS_DIR, "fertilizer_model.joblib")

_lock = threading.Lock()
_crop_bundle = None
_fert_bundle = None


class ModelLoadError(Exception):
    """Raised when a model file is missing or cannot be loaded."""


# Aliases so the same physical value can arrive under different spellings
# (e.g. dataset column "pH_Value" but form field "ph").
# Keys are stored in normalized form (lowercase, no spaces/underscores).
COLUMN_ALIASES = {
    "phvalue": ["ph"],
    "phosphorous": ["phosphorus"],
    "phosphorus": ["phosphorous"],
    "temperature": ["temparature"],
}


def _normalize(key):
    """Lowercases a key and removes spaces/underscores for matching."""
    return key.lower().replace("_", "").replace(" ", "")


def _resolve_input(inputs, column):
    """Finds the value for a dataset column in the input dict (any spelling)."""
    normalized_inputs = {_normalize(k): v for k, v in inputs.items()}
    normalized = _normalize(column)
    if normalized in normalized_inputs:
        return normalized_inputs[normalized]
    for alias in COLUMN_ALIASES.get(normalized, []):
        key = _normalize(alias)
        if key in normalized_inputs:
            return normalized_inputs[key]
    return None


def _load_crop_bundle():
    global _crop_bundle
    if _crop_bundle is None:
        with _lock:
            if _crop_bundle is None:
                if not os.path.exists(CROP_MODEL_PATH):
                    raise ModelLoadError(
                        f"Crop model not found at {CROP_MODEL_PATH}. "
                        "Run 'python ml/train_crop_model.py' first."
                    )
                _crop_bundle = joblib.load(CROP_MODEL_PATH)
    return _crop_bundle


def _load_fertilizer_bundle():
    global _fert_bundle
    if _fert_bundle is None:
        with _lock:
            if _fert_bundle is None:
                if not os.path.exists(FERTILIZER_MODEL_PATH):
                    raise ModelLoadError(
                        f"Fertilizer model not found at {FERTILIZER_MODEL_PATH}. "
                        "Run 'python ml/train_fertilizer_model.py' first."
                    )
                _fert_bundle = joblib.load(FERTILIZER_MODEL_PATH)
    return _fert_bundle


def predict_crop(inputs):
    """
    Predicts a crop from a dict of soil/environment values.

    Expected keys: nitrogen, phosphorus, potassium, temperature, humidity,
    ph, rainfall (or their exact dataset column names).
    """
    bundle = _load_crop_bundle()
    feature_columns = bundle["feature_columns"]
    model = bundle["model"]
    label_encoder = bundle["label_encoder"]

    row = []
    for column in feature_columns:
        value = _resolve_input(inputs, column)
        if value is None:
            raise ValueError(f"Missing input value for feature '{column}'")
        row.append(float(value))

    # Single sample as a DataFrame so feature names match training
    import numpy as np
    import pandas as pd

    sample = pd.DataFrame([row], columns=feature_columns)
    label_index = int(model.predict(sample)[0])
    crop_name = label_encoder.inverse_transform([label_index])[0]

    probabilities = model.predict_proba(sample)[0]
    confidence = float(max(probabilities))
    
    top3_indices = np.argsort(probabilities)[-3:][::-1]
    top3 = [
        {"name": label_encoder.inverse_transform([idx])[0], "prob": round(float(probabilities[idx] * 100), 1)}
        for idx in top3_indices
    ]

    return {
        "crop": crop_name,
        "confidence": round(confidence, 4),
        "top3": top3,
        "input_features": dict(zip(feature_columns, row)),
    }


def predict_fertilizer(inputs):
    """
    Predicts a fertilizer from a dict of inputs.

    Expected keys: temperature, humidity, moisture, soil_type, crop_type,
    nitrogen, potassium, phosphorous (or exact dataset column names).
    """
    bundle = _load_fertilizer_bundle()
    numeric_columns = bundle["numeric_columns"]
    categorical_columns = bundle["categorical_columns"]
    pipeline = bundle["pipeline"]
    label_encoder = bundle["label_encoder"]

    row = {}
    for column in numeric_columns:
        value = _resolve_input(inputs, column)
        if value is None:
            raise ValueError(f"Missing input value for feature '{column}'")
        row[column] = float(value)

    for column in categorical_columns:
        value = _resolve_input(inputs, column)
        if value is None:
            raise ValueError(f"Missing input value for feature '{column}'")
        row[column] = str(value).strip()

    import numpy as np
    import pandas as pd

    sample = pd.DataFrame([row], columns=numeric_columns + categorical_columns)
    label_index = int(pipeline.predict(sample)[0])
    fertilizer_name = label_encoder.inverse_transform([label_index])[0]

    probabilities = pipeline.predict_proba(sample)[0]
    confidence = float(max(probabilities))
    
    top3_indices = np.argsort(probabilities)[-3:][::-1]
    top3 = [
        {"name": label_encoder.inverse_transform([idx])[0], "prob": round(float(probabilities[idx] * 100), 1)}
        for idx in top3_indices
    ]

    return {
        "fertilizer": fertilizer_name,
        "confidence": round(confidence, 4),
        "top3": top3,
        "input_features": {k: v for k, v in row.items()},
    }


def crop_model_info():
    """Returns metadata about the loaded crop model (for the UI footer/displays)."""
    bundle = _load_crop_bundle()
    return {
        "classes": bundle["classes"],
        "accuracy": round(float(bundle["accuracy"]), 4),
        "trained_rows": bundle.get("trained_rows"),
    }


def fertilizer_model_info():
    bundle = _load_fertilizer_bundle()
    return {
        "classes": bundle["classes"],
        "accuracy": round(float(bundle["accuracy"]), 4),
        "trained_rows": bundle.get("trained_rows"),
    }


def fertilizer_categories():
    """Returns the trained categorical values (soil types, crop types)."""
    bundle = _load_fertilizer_bundle()
    onehot = bundle["pipeline"].named_steps["preprocessor"].named_transformers_["cat"]
    categories = onehot.categories_
    return {
        "soil_types": sorted(categories[0]),
        "crop_types": sorted(categories[1]),
    }
