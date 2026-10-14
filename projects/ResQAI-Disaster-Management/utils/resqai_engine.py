"""
ResQAI - disaster relief intelligence engine.

Wraps the trained classifier with the operational layer the abstract calls
for: real-time tweet classification, emergency prioritisation, incident
monitoring, live statistics, disaster-trend analysis and analytical reports.
"""

import math
import os
import re
import threading
from collections import Counter, deque
from datetime import datetime, timedelta

import joblib
import numpy as np
import pandas as pd

from utils.preprocessing import clean_text, preprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "model")
DATA_PATH = os.path.join(BASE_DIR, "data", "kaggle_reference", "train.csv")

# Incident feed is capped so a long-running dashboard cannot grow unbounded.
MAX_INCIDENTS = 500

_cache = {}
_lock = threading.Lock()

# ---------------------------------------------------------------------------
# Severity lexicon - drives emergency prioritisation.
# Terms are stemmed at match time so "fatalities"/"fatality" both hit "fatal".
# ---------------------------------------------------------------------------
SEVERITY_TERMS = {
    "critical": ["trap", "dead", "death", "fatal", "kill", "casualti", "bodi", "corps",
                  "collaps", "bury", "buri", "drown", "explos", "bomb", "massacr",
                  "rescu", "sos", "emerg", "urgent", "help", "stuck", "injur", "wound",
                  "bleed", "unconsci", "miss", "hijack", "terror", "attack", "jihad", "plane"],
    "high": ["evacu", "fire", "flood", "earthquak", "wildfir", "storm", "hurrican",
              "cyclon", "tornado", "landslid", "tsunami", "derail", "crash", "burn",
              "destroy", "damag", "wreck", "blaze", "siren", "alarm"],
    "medium": ["warn", "alert", "risk", "threat", "danger", "hazard", "evacuat",
                "shelter", "relief", "aid", "displac", "outag", "block"],
}
SEVERITY_WEIGHT = {"critical": 3.0, "high": 2.0, "medium": 1.0}

# Casualty phrasing like "3 dead" / "20 injured" is a strong urgency signal.
CASUALTY_RE = re.compile(r"\b(\d{1,6})\s*(?:people|persons|residents)?\s*"
                          r"(dead|died|killed|injured|missing|trapped|evacuated|feared)",
                          re.IGNORECASE)

DISASTER_CATEGORIES = {
    "Fire / Wildfire": ["fire", "wildfir", "blaze", "burn", "smoke", "arson", "flame"],
    "Flood / Storm": ["flood", "storm", "hurrican", "cyclon", "typhoon", "rain", "deluge",
                       "tsunami", "surg", "monsoon"],
    "Earthquake / Landslide": ["earthquak", "quak", "aftershock", "landslid", "mudslid",
                                "sinkhol", "tremor", "avalanch"],
    "Explosion / Structural": ["explos", "bomb", "blast", "collaps", "detonat", "rubbl",
                                "demolish"],
    "Transport Accident": ["crash", "derail", "collis", "accid", "wreck", "capsiz",
                            "airplan", "train"],
    "Severe Weather": ["tornado", "hail", "blizzard", "heatwav", "drought", "lightn",
                        "windstorm"],
}


def _load():
    if _cache:
        return _cache
    with _lock:
        if _cache:
            return _cache
        built = {}
        clf_path = os.path.join(MODEL_DIR, "resqai_classifier.pkl")
        if not os.path.exists(clf_path):
            raise FileNotFoundError("Model not trained. Run: python model/train_models.py")
        built["clf"] = joblib.load(clf_path)
        built["vec"] = joblib.load(os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl"))
        built["metrics"] = joblib.load(os.path.join(MODEL_DIR, "model_metrics.pkl"))
        built["incidents"] = deque(maxlen=MAX_INCIDENTS)
        _cache.update(built)
    return _cache


def model_metrics():
    return _load()["metrics"]


# ---------------------------------------------------------------------------
# classification
# ---------------------------------------------------------------------------
def _confidence(clf, X):
    """Probability of the disaster class. LinearSVC exposes no predict_proba,
    so its signed distance from the hyperplane is squashed with a logistic
    function to give a comparable 0-1 confidence."""
    if hasattr(clf, "predict_proba"):
        return float(clf.predict_proba(X)[0][1])
    margin = float(clf.decision_function(X)[0])
    if margin > 100:
        return 1.0
    if margin < -100:
        return 0.0
    return 1.0 / (1.0 + math.exp(-margin))


def severity_of(stemmed, raw_text):
    """Weighted severity from the lexicon plus any casualty counts."""
    tokens = set(stemmed.split())
    hits = {}
    score = 0.0
    for level, terms in SEVERITY_TERMS.items():
        matched = [t for t in terms if any(tok.startswith(t) for tok in tokens)]
        if matched:
            hits[level] = matched
            score += SEVERITY_WEIGHT[level] * len(matched)

    casualties = 0
    for count, _kind in CASUALTY_RE.findall(raw_text or ""):
        try:
            casualties = max(casualties, int(count))
        except ValueError:
            pass
    if casualties:
        # log-scaled so 500 casualties does not dwarf every other signal
        score += 2.0 * math.log10(casualties + 1)

    return score, hits, casualties


def categorise(stemmed):
    tokens = set(stemmed.split())
    for name, terms in DISASTER_CATEGORIES.items():
        if any(any(tok.startswith(t) for tok in tokens) for t in terms):
            return name
    return "Other / Unclassified"


def priority_of(confidence, severity_score):
    """0-100 priority: model confidence that it is a real disaster, scaled up by
    how severe the language is. Confidence dominates (a false positive should
    not be top of the queue no matter how dramatic its wording)."""
    sev_norm = min(1.0, severity_score / 8.0)
    score = 100.0 * (0.65 * confidence + 0.35 * confidence * sev_norm)
    return round(min(100.0, score), 1)


def priority_band(score):
    if score >= 60:
        return "CRITICAL"
    if score >= 40:
        return "HIGH"
    if score >= 22:
        return "MEDIUM"
    return "LOW"


def classify_tweet(text, location=None, keyword=None, record=True):
    d = _load()
    raw = str(text or "").strip()
    if not raw:
        return {"error": "Empty tweet text."}

    combined = raw + (" " + keyword.replace("%20", " ") if keyword else "")
    stemmed = preprocess(combined)
    if not stemmed:
        stemmed = clean_text(combined)

    X = d["vec"].transform([stemmed])
    is_disaster = bool(d["clf"].predict(X)[0] == 1)
    confidence = _confidence(d["clf"], X)

    # Model Explainability
    explanation = []
    if hasattr(d["clf"], "coef_"):
        coefs = d["clf"].coef_[0]
        feature_names = d["vec"].get_feature_names_out()
        for idx in X[0].nonzero()[1]:
            weight = float(coefs[idx])
            explanation.append({
                "word": feature_names[idx], 
                "weight": round(weight, 3),
                "contribution": "Positive (Disaster)" if weight > 0 else "Negative (Not Disaster)"
            })
        explanation.sort(key=lambda x: abs(x["weight"]), reverse=True)

    sev_score, sev_hits, casualties = severity_of(stemmed, raw)

    # Blend with pre-trained Semantic Similarity Model
    try:
        from utils.pretrained_boost import get_pretrained_confidence
        pt_conf = get_pretrained_confidence(raw)
        if pt_conf is not None:
            # If the pre-trained model is highly confident it's a disaster (>0.7), override or boost
            if pt_conf > 0.75:
                is_disaster = True
                confidence = max(confidence, pt_conf)
                sev_score += (pt_conf - 0.5) * 5.0 # Boost severity score significantly
            elif is_disaster:
                # Average them if SVM thought it was a disaster but pretrained is unsure
                confidence = (confidence + pt_conf) / 2.0
    except Exception:
        pass

    category = categorise(stemmed) if is_disaster else None
    
    # If category is "Other", try to assign a better one for high priority
    if category == "Other / Unclassified" and is_disaster:
        if "terror" in raw.lower() or "attack" in raw.lower() or "hijack" in raw.lower():
            category = "Terrorism / Attack"
            
    priority = priority_of(confidence, sev_score) if is_disaster else round(confidence * 20, 1)

    # Reaction Logic
    reaction = "Standard review."
    if is_disaster:
        if priority >= 60:
            reaction = "URGENT ESCALATION: Dispatch immediate emergency services."
        elif priority >= 40:
            reaction = "HIGH PRIORITY: Verify with local authorities before committing resources."
        else:
            reaction = "SUPPORT: Monitor situation and prepare for potential escalation."
    else:
        reaction = "ENGAGEMENT: No immediate emergency action required. Routine monitoring."

    result = {
        "text": raw,
        "location": location or None,
        "keyword": keyword or None,
        "is_disaster": is_disaster,
        "label": "Disaster" if is_disaster else "Not Disaster",
        "confidence": round(confidence * 100, 1),
        "category": category,
        "severity_score": round(sev_score, 2),
        "severity_terms": sev_hits,
        "casualties_mentioned": casualties or None,
        "priority": priority,
        "priority_band": priority_band(priority) if is_disaster else "LOW",
        "model_explanation": explanation[:8], # Top 8 most influential words
        "reaction": reaction,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }

    if record and is_disaster:
        d["incidents"].append(result)
    return result


def classify_batch(items):
    return [classify_tweet(i.get("text", ""), i.get("location"), i.get("keyword"))
            for i in items]


# ---------------------------------------------------------------------------
# incident feed / prioritisation
# ---------------------------------------------------------------------------
def incident_feed(limit=50, band=None, category=None):
    d = _load()
    rows = list(d["incidents"])
    if band:
        rows = [r for r in rows if r["priority_band"] == band]
    if category:
        rows = [r for r in rows if r["category"] == category]
    rows.sort(key=lambda r: r["priority"], reverse=True)
    return rows[:limit]


def record_incident(result):
    """Record one operational incident while avoiding duplicate reports."""
    d = _load()
    incident_id = result.get("incident_id") or result.get("id")
    if incident_id:
        for existing in d["incidents"]:
            if existing.get("incident_id") == incident_id:
                return False
    else:
        signature = (result.get("text", "").strip().lower(), result.get("location"))
        for existing in d["incidents"]:
            if (existing.get("text", "").strip().lower(), existing.get("location")) == signature:
                return False
    d["incidents"].append(result)
    return True


def clear_incidents():
    _load()["incidents"].clear()


def statistics():
    d = _load()
    rows = list(d["incidents"])
    bands = Counter(r["priority_band"] for r in rows)
    cats = Counter(r["category"] for r in rows if r["category"])
    total_casualties = sum(r["casualties_mentioned"] or 0 for r in rows)
    return {
        "total_incidents": len(rows),
        "critical": bands.get("CRITICAL", 0),
        "high": bands.get("HIGH", 0),
        "medium": bands.get("MEDIUM", 0),
        "low": bands.get("LOW", 0),
        "categories": dict(cats.most_common()),
        "avg_priority": round(float(np.mean([r["priority"] for r in rows])), 1) if rows else 0.0,
        "avg_confidence": round(float(np.mean([r["confidence"] for r in rows])), 1) if rows else 0.0,
        "total_casualties_mentioned": total_casualties,
        "top_locations": dict(Counter(r["location"] for r in rows if r["location"]).most_common(8)),
    }


# ---------------------------------------------------------------------------
# trends + analytical reports
# ---------------------------------------------------------------------------
def trends():
    """Disaster trends over the live incident feed: category mix, priority
    distribution, and volume over the last 30 minutes."""
    d = _load()
    rows = list(d["incidents"])
    if not rows:
        return {"categories": [], "bands": [], "timeline": [], "keywords": []}

    cats = Counter(r["category"] for r in rows if r["category"])
    bands = Counter(r["priority_band"] for r in rows)

    now = datetime.now()
    buckets = Counter()
    for r in rows:
        ts = datetime.fromisoformat(r["timestamp"])
        minutes_ago = int((now - ts).total_seconds() // 60)
        if minutes_ago <= 30:
            buckets[minutes_ago] += 1
    timeline = [{"minutes_ago": m, "count": buckets.get(m, 0)} for m in range(30, -1, -1)]

    words = Counter()
    for r in rows:
        for level_terms in r["severity_terms"].values():
            words.update(level_terms)

    return {
        "categories": [{"name": k, "count": v} for k, v in cats.most_common()],
        "bands": [{"name": b, "count": bands.get(b, 0)}
                   for b in ("CRITICAL", "HIGH", "MEDIUM", "LOW")],
        "timeline": timeline,
        "keywords": [{"term": k, "count": v} for k, v in words.most_common(12)],
    }


def analytical_report():
    """Text summary for decision support (abstract: 'disaster summaries',
    'analytical reports to support decision-making')."""
    stats = statistics()
    tr = trends()
    lines = []

    if stats["total_incidents"] == 0:
        return {"generated_at": datetime.now().isoformat(timespec="seconds"),
                "summary": ["No disaster incidents in the current monitoring window."]}

    lines.append(f"{stats['total_incidents']} disaster incident(s) detected in the current "
                 f"monitoring window, with an average model confidence of "
                 f"{stats['avg_confidence']}%.")

    if stats["critical"]:
        lines.append(f"{stats['critical']} incident(s) are CRITICAL priority and require "
                     f"immediate rescue dispatch.")
    if stats["high"]:
        lines.append(f"{stats['high']} incident(s) are HIGH priority and should be queued "
                     f"after critical cases.")

    if tr["categories"]:
        top = tr["categories"][0]
        lines.append(f"The dominant incident type is '{top['name']}' "
                     f"({top['count']} of {stats['total_incidents']} reports).")

    if stats["total_casualties_mentioned"]:
        lines.append(f"Reports collectively mention approximately "
                     f"{stats['total_casualties_mentioned']} affected people - "
                     f"verify against official channels before resource allocation.")

    if stats["top_locations"]:
        loc = list(stats["top_locations"].items())[0]
        lines.append(f"Most frequently reported location: {loc[0]} ({loc[1]} report(s)).")

    lines.append("Recommended action: dispatch to CRITICAL incidents first, then confirm "
                 "HIGH priority reports with ground teams before committing resources.")

    return {"generated_at": datetime.now().isoformat(timespec="seconds"), "summary": lines}


# ---------------------------------------------------------------------------
# demo stream - replays real held-out tweets from the Kaggle dataset
# ---------------------------------------------------------------------------
def sample_real_tweets(n=25, seed=None):
    """Draw real tweets from the Kaggle dataset to simulate an incoming feed.
    These are genuine tweets, not invented text - the ground-truth label is
    returned alongside so the dashboard can be checked against it."""
    df = pd.read_csv(DATA_PATH)
    sample = df.sample(n=min(n, len(df)), random_state=seed)
    return [{"text": r["text"],
             "keyword": None if pd.isna(r["keyword"]) else str(r["keyword"]),
             "location": None if pd.isna(r["location"]) else str(r["location"]),
             "actual_label": int(r["target"])}
            for _, r in sample.iterrows()]
