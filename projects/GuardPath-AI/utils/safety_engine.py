"""
GuardPath - Safety scoring engine.

Ties together the predefined road network, the predefined area
dataset and the trained Random Forest model to:
  1. find candidate routes between a source and a destination,
  2. predict the safety level of every area along each route,
  3. compute an overall safety score per route,
  4. classify each route as Safe / Moderate / Unsafe,
  5. explain the recommendation in plain language.
"""

import os

import joblib
import pandas as pd

from utils.city_graph import ROAD_NETWORK, find_routes

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AREAS_PATH = os.path.join(BASE_DIR, "data", "city_areas.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model", "guardpath_rf_model.pkl")

FEATURES = ["crime_rate", "road_condition", "lighting_condition", "traffic_level"]
LABEL_WEIGHT = {"Unsafe": 0, "Moderate": 50, "Safe": 100}

MODE_SPEED_KMPH = {
    "walking": 5,
    "bicycle": 15,
    "public_transport": 25,
    "car": 35,
}

MODE_ADJUSTMENT = {
    "walking": -8,
    "bicycle": -4,
    "public_transport": 0,
    "car": 5,
}

_model = None
_areas_df = None


def _load():
    global _model, _areas_df
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                "Model file not found. Run 'python model/train_model.py' first."
            )
        _model = joblib.load(MODEL_PATH)
    if _areas_df is None:
        _areas_df = pd.read_csv(AREAS_PATH, index_col="area_name")
    return _model, _areas_df


def get_area_list():
    _, areas_df = _load()
    return sorted(areas_df.index.tolist())


def get_area_coords():
    """Returns {area_name: [lat, lon]} for the offline schematic map view."""
    _, areas_df = _load()
    return {name: [row["lat"], row["lon"]] for name, row in areas_df.iterrows()}


def get_area_details():
    """Returns {area_name: {...}} with coordinates and raw attributes, for
    map tooltips. Real per-ward alert counts (from the Kaggle CAS dataset
    this data was derived from) are merged in separately by app.py."""
    _, areas_df = _load()
    details = {}
    for name, row in areas_df.iterrows():
        details[name] = {
            "lat": row["lat"],
            "lon": row["lon"],
            "crime_rate": row["crime_rate"],
            "road_condition": row["road_condition"],
            "lighting_condition": row["lighting_condition"],
            "traffic_level": row["traffic_level"],
        }
    return details


def _effective_features(area_name, travel_time):
    _, areas_df = _load()
    row = areas_df.loc[area_name]
    crime_rate = row["crime_rate"]
    road_condition = row["road_condition"]
    lighting_condition = row["lighting_condition"]
    traffic_level = row["traffic_level"]

    if travel_time == "night":
        crime_rate = min(10.0, crime_rate + 1.5)
        lighting_condition = max(0.0, lighting_condition - 2.0)

    return {
        "crime_rate": crime_rate,
        "road_condition": road_condition,
        "lighting_condition": lighting_condition,
        "traffic_level": traffic_level,
    }


def predict_area_safety(area_name, travel_time):
    """Runs the trained Random Forest model on one area's (time-of-day
    adjusted) features and returns its predicted label, a 0-100 safety
    index derived from the class probabilities, and the raw features
    used for the prediction."""
    model, _ = _load()
    features = _effective_features(area_name, travel_time)

    X = pd.DataFrame([features], columns=FEATURES)
    proba = model.predict_proba(X)[0]
    label = model.classes_[proba.argmax()]

    index = sum(p * LABEL_WEIGHT[cls] for p, cls in zip(proba, model.classes_))

    return {"area": area_name, "label": label, "index": round(index, 1), "features": features}


def _classify(score):
    if score >= 70:
        return "Safe"
    if score >= 40:
        return "Moderate"
    return "Unsafe"


def _segment_weights(path, distance):
    """Weight each area by the length of its adjacent road segment(s) so
    longer stretches near an area count more toward the route score."""
    weights = []
    for i, area in enumerate(path):
        edges = []
        if i > 0:
            edges.append(ROAD_NETWORK[path[i - 1]][area])
        if i < len(path) - 1:
            edges.append(ROAD_NETWORK[area][path[i + 1]])
        weights.append(sum(edges) / len(edges) if edges else 1.0)
    total = sum(weights) or 1.0
    return [w / total for w in weights]


def _build_reasons(area_predictions, travel_time, travel_mode):
    reasons = []
    n = len(area_predictions)

    avg_crime = sum(p["features"]["crime_rate"] for p in area_predictions) / n
    avg_road = sum(p["features"]["road_condition"] for p in area_predictions) / n
    avg_light = sum(p["features"]["lighting_condition"] for p in area_predictions) / n
    avg_traffic = sum(p["features"]["traffic_level"] for p in area_predictions) / n

    if avg_crime <= 3.5:
        reasons.append("Low crime rate reported across this route")
    elif avg_crime >= 6.0:
        reasons.append("Higher crime rate reported in parts of this route")

    if avg_light >= 7.0:
        reasons.append("Well-lit streets throughout the route")
    elif avg_light < 4.0:
        msg = "Poor street lighting in some areas"
        if travel_time == "night":
            msg += " (increased risk at night)"
        reasons.append(msg)

    if avg_road >= 7.0:
        reasons.append("Good road conditions along the way")
    elif avg_road < 4.0:
        reasons.append("Poor road conditions in some segments")

    if avg_traffic >= 7.0:
        reasons.append("Heavy traffic congestion expected")
    elif avg_traffic <= 3.0:
        reasons.append("Low traffic, smoother and calmer travel")

    if travel_mode in ("walking", "bicycle") and avg_crime >= 5.5:
        reasons.append("Increased exposure risk for pedestrians/cyclists in less safe zones")

    unsafe_areas = [p["area"] for p in area_predictions if p["label"] == "Unsafe"]
    if unsafe_areas:
        reasons.append(f"Passes through higher-risk area(s): {', '.join(unsafe_areas)}")

    return reasons[:5] if reasons else ["No significant safety concerns detected"]


def score_route(path, distance, travel_time, travel_mode):
    area_predictions = [predict_area_safety(area, travel_time) for area in path]
    weights = _segment_weights(path, distance)

    base_score = sum(p["index"] * w for p, w in zip(area_predictions, weights))

    # Explicit traffic penalty makes the route planner safety-aware even when
    # two routes receive similar Random Forest scores. Traffic is still the
    # project's area-level proxy, not live traffic.
    avg_traffic = sum(p["features"]["traffic_level"] for p in area_predictions) / len(area_predictions)
    traffic_penalty = max(0.0, avg_traffic - 3.0) * 1.8
    adjusted_score = base_score + MODE_ADJUSTMENT.get(travel_mode, 0) - traffic_penalty
    adjusted_score = max(0.0, min(100.0, adjusted_score))

    return {
        "path": path,
        "distance_km": round(distance, 1),
        "traffic_level": round(avg_traffic, 1),
        "traffic_label": "Heavy" if avg_traffic >= 7 else ("Moderate" if avg_traffic >= 4 else "Low"),
        "traffic_penalty": round(traffic_penalty, 1),
        "eta_minutes": round((distance / max(MODE_SPEED_KMPH.get(travel_mode, 5), 1)) * 60 * (1 + 0.45 * avg_traffic / 10), 1),
        "safety_score": round(adjusted_score, 1),
        "status": _classify(adjusted_score),
        "reasons": _build_reasons(area_predictions, travel_time, travel_mode),
        "area_breakdown": [
            {"area": p["area"], "label": p["label"], "index": p["index"]} for p in area_predictions
        ],
    }


def recommend_route(source, destination, travel_time, travel_mode):
    _load()

    if source == destination:
        return {"error": "Source and destination cannot be the same."}

    candidate_paths = find_routes(source, destination)
    if not candidate_paths:
        return {"error": f"No predefined route found between '{source}' and '{destination}'."}

    routes = [score_route(path, distance, travel_time, travel_mode) for path, distance in candidate_paths]
    for route in routes:
        mins = route["eta_minutes"]
        route["eta_text"] = f"{int(mins)} min" if mins < 60 else f"{int(mins // 60)}h {int(mins % 60)}m"
    routes.sort(key=lambda r: r["safety_score"], reverse=True)

    for i, route in enumerate(routes):
        route["route_id"] = i + 1
        route["recommended"] = i == 0

    return {"source": source, "destination": destination, "travel_time": travel_time,
            "travel_mode": travel_mode, "routes": routes}
