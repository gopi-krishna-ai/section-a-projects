"""
AI-Assisted Smart Study Planner - core engine.

Ties together the trained Random Forest priority model with a
Pomodoro-based weekly schedule generator, progress tracking, and
plain-language recommendations - mirroring the GuardPath project's
"predict -> score -> explain" pattern.
"""

import csv
import datetime
import os

import joblib
import pandas as pd

SESSION_MINUTES = 25
BREAK_MINUTES = 5
PLAN_DAYS = 7
LOW_WEEKLY_HOURS_THRESHOLD = 5
PRE_EXAM_WINDOW_DAYS = 5

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "study_priority_rf_model.pkl")
BENCHMARKS_PATH = os.path.join(BASE_DIR, "data", "kaggle_reference", "study_benchmarks.csv")

FEATURES = ["days_to_exam", "completion_pct", "difficulty", "weightage"]
LABEL_WEIGHT = {"Low": 0, "Medium": 50, "High": 100}

_model = None
_benchmarks = None


def _load_benchmarks():
    """Real averages from the Kaggle 'Students Performance in Exams' dataset
    (30,641 students), used to ground two recommendation rules in actual
    evidence instead of an invented formula. See README for the full
    citation. Returns {} if the benchmark file hasn't been generated yet
    (python data/process_kaggle_dataset.py) - recommendations degrade
    gracefully to the priority-only rules in that case."""
    global _benchmarks
    if _benchmarks is None:
        _benchmarks = {}
        if os.path.exists(BENCHMARKS_PATH):
            with open(BENCHMARKS_PATH, newline="") as f:
                for row in csv.DictReader(f):
                    _benchmarks.setdefault(row["category"], {})[row["subgroup"]] = {
                        "avg_score": float(row["avg_score"]),
                        "n": int(row["n"]),
                    }
    return _benchmarks


def _load_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError("Model file not found. Run 'python model/train_model.py' first.")
        _model = joblib.load(MODEL_PATH)
    return _model


def predict_priority(days_to_exam, completion_pct, difficulty, weightage):
    model = _load_model()
    X = pd.DataFrame(
        [[max(0, days_to_exam), completion_pct, difficulty, weightage]], columns=FEATURES
    )
    proba = model.predict_proba(X)[0]
    label = model.classes_[proba.argmax()]
    urgency = sum(p * LABEL_WEIGHT[cls] for p, cls in zip(proba, model.classes_))
    return label, round(urgency, 1)


def _subject_state(name, info, as_of_date):
    exam_date = datetime.date.fromisoformat(info["exam_date"])
    days_to_exam = (exam_date - as_of_date).days
    total = max(1, info["total_topics"])
    completed = min(info["completed_topics"], info["total_topics"])
    completion_pct = round(completed / total * 100, 1)
    label, urgency = predict_priority(days_to_exam, completion_pct, info["difficulty"], info["weightage"])
    return {
        "name": name,
        "exam_date": info["exam_date"],
        "days_to_exam": days_to_exam,
        "total_topics": info["total_topics"],
        "completed_topics": completed,
        "remaining_topics": max(0, info["total_topics"] - completed),
        "completion_pct": completion_pct,
        "difficulty": info["difficulty"],
        "weightage": info["weightage"],
        "priority": label,
        "urgency_score": urgency,
        "exam_passed": days_to_exam < 0,
        "syllabus_complete": completed >= info["total_topics"],
    }


def all_subject_states(store, as_of_date=None):
    as_of_date = as_of_date or datetime.date.today()
    return [_subject_state(name, info, as_of_date) for name, info in store["subjects"].items()]


def _largest_remainder_round(weights, total):
    """Round a list of fractional weights (summing to `total`) to integers
    that still sum to exactly `total`, using the largest-remainder method."""
    floors = [int(w) for w in weights]
    remainder_budget = total - sum(floors)
    remainders = sorted(range(len(weights)), key=lambda i: weights[i] - floors[i], reverse=True)
    for i in remainders[:remainder_budget]:
        floors[i] += 1
    return floors


def generate_week_schedule(store, start_date=None, days=PLAN_DAYS):
    start_date = start_date or datetime.date.today()
    daily_hours = store["settings"].get("daily_hours", 4)
    sessions_per_day = max(1, int(daily_hours * 60 // (SESSION_MINUTES + BREAK_MINUTES)))
    session_actions = store.get("session_actions", {})

    week = []
    for offset in range(days):
        date = start_date + datetime.timedelta(days=offset)
        states = [s for s in all_subject_states(store, date) if not s["exam_passed"] and not s["syllabus_complete"]]
        states.sort(key=lambda s: s["urgency_score"], reverse=True)

        day_entry = {"date": date.isoformat(), "weekday": date.strftime("%A"), "sessions": []}

        if states:
            weights = [s["urgency_score"] + 1 for s in states]
            total_weight = sum(weights)
            proportional = [w / total_weight * sessions_per_day for w in weights]
            counts = _largest_remainder_round(proportional, sessions_per_day)

            session_number = 1
            for state, count in zip(states, counts):
                action_key = f"{date.isoformat()}|{state['name']}"
                acted_count = int(session_actions.get(action_key, 0))
                remaining_count = max(0, count - acted_count)

                # Get topics list if available
                t_names = store["subjects"][state["name"]].get("topic_names", [])

                for slot_index in range(remaining_count):
                    topic_idx = acted_count + slot_index
                    topic_label = f"Topic {topic_idx + 1}"
                    if t_names:
                        if topic_idx < len(t_names):
                            topic_label = t_names[topic_idx]
                        else:
                            topic_label = "Revision / Practice"

                    day_entry["sessions"].append(
                        {
                            "session_id": f"{date.isoformat()}|{state['name']}|{topic_idx + 1}",
                            "session_number": session_number,
                            "subject": state["name"],
                            "topic": topic_label,
                            "priority": state["priority"],
                            "duration_minutes": SESSION_MINUTES,
                            "break_minutes": BREAK_MINUTES,
                        }
                    )
                    session_number += 1

        week.append(day_entry)

    return week


def _record_session_action(store, subject_name, session_date, action):
    if subject_name not in store["subjects"]:
        raise KeyError(subject_name)

    key = f"{session_date}|{subject_name}"
    store.setdefault("session_actions", {})
    store["session_actions"][key] = int(store["session_actions"].get(key, 0)) + 1

    if action == "done":
        info = store["subjects"][subject_name]
        info["completed_topics"] = min(info["total_topics"], info["completed_topics"] + 1)
    elif action == "missed":
        store.setdefault("missed_log", [])
        store["missed_log"].append({"date": session_date, "subject": subject_name})
        store["missed_log"] = store["missed_log"][-50:]


def mark_session_complete(store, subject_name, session_date=None):
    session_date = session_date or datetime.date.today().isoformat()
    _record_session_action(store, subject_name, session_date, "done")
    return store


def mark_session_missed(store, subject_name, session_date=None):
    session_date = session_date or datetime.date.today().isoformat()
    _record_session_action(store, subject_name, session_date, "missed")
    return store


def weekly_hours_by_subject(schedule):
    hours = {}
    for day in schedule:
        for session in day["sessions"]:
            hours[session["subject"]] = hours.get(session["subject"], 0) + SESSION_MINUTES / 60
    return {name: round(h, 1) for name, h in hours.items()}


def generate_recommendations(store, schedule=None):
    states = all_subject_states(store)
    schedule = schedule if schedule is not None else generate_week_schedule(store)
    weekly_hours = weekly_hours_by_subject(schedule)
    benchmarks = _load_benchmarks()

    recent_missed = {
        entry["subject"]
        for entry in store["missed_log"]
        if (datetime.date.today() - datetime.date.fromisoformat(entry["date"])).days <= 2
    }

    recs = []
    for s in states:
        if s["exam_passed"]:
            recs.append({"severity": 3, "text": f"{s['name']}: exam date has passed — update or remove this subject."})
            continue
        if s["syllabus_complete"]:
            recs.append({"severity": 0, "text": f"{s['name']}: syllabus complete — switch to revision or drop it from the active plan."})
            continue

        if s["priority"] == "High" and s["completion_pct"] < 50:
            recs.append({
                "severity": 2,
                "text": f"{s['name']}: only {s['completion_pct']}% done with {s['days_to_exam']} day(s) left — this needs priority attention.",
            })
        elif s["priority"] == "High":
            recs.append({"severity": 1, "text": f"{s['name']}: exam is close — keep up the current pace."})

        if s["name"] in recent_missed:
            recs.append({
                "severity": 2,
                "text": f"{s['name']}: a recent session was missed and progress hasn't moved — it stays high priority.",
            })

        # Evidence-based rule 1: weekly hours vs a real study-hours/score benchmark.
        hrs = weekly_hours.get(s["name"], 0)
        study_bm = benchmarks.get("WklyStudyHours")
        if study_bm and s["priority"] in ("High", "Medium") and hrs < LOW_WEEKLY_HOURS_THRESHOLD:
            low = study_bm.get("< 5")
            high = study_bm.get("> 10")
            if low and high:
                recs.append({
                    "severity": 2 if s["priority"] == "High" else 1,
                    "text": (
                        f"{s['name']}: only {hrs} hr(s)/week allocated. In a real dataset of "
                        f"{low['n'] + high['n']:,} students, those studying under 5 hrs/week averaged "
                        f"{low['avg_score']} vs {high['avg_score']} for 10+ hrs/week — consider raising your "
                        f"daily study time or this subject's share of it."
                    ),
                })

        # Evidence-based rule 2: pre-exam revision nudge from the real test-prep benchmark.
        prep_bm = benchmarks.get("TestPrep")
        if prep_bm and 0 <= s["days_to_exam"] <= PRE_EXAM_WINDOW_DAYS:
            none_bm = prep_bm.get("none")
            done_bm = prep_bm.get("completed")
            if none_bm and done_bm:
                recs.append({
                    "severity": 2,
                    "text": (
                        f"{s['name']}: exam in {s['days_to_exam']} day(s) — schedule a focused revision/mock-test "
                        f"session. Real data ({none_bm['n'] + done_bm['n']:,} students) shows those who completed "
                        f"test-prep averaged {done_bm['avg_score']} vs {none_bm['avg_score']} for those who didn't."
                    ),
                })

    recs.sort(key=lambda r: r["severity"], reverse=True)
    return [r["text"] for r in recs[:8]] or ["Add a subject to get your first AI-generated recommendations."]


def compute_analytics(store):
    states = all_subject_states(store)
    total_missed_this_week = sum(
        1
        for entry in store["missed_log"]
        if (datetime.date.today() - datetime.date.fromisoformat(entry["date"])).days <= 7
    )
    return {
        "subjects": [
            {
                "name": s["name"],
                "completion_pct": s["completion_pct"],
                "priority": s["priority"],
                "urgency_score": s["urgency_score"],
                "days_to_exam": s["days_to_exam"],
            }
            for s in states
        ],
        "missed_sessions_this_week": total_missed_this_week,
    }


def get_full_view(store):
    schedule = generate_week_schedule(store)
    return {
        "subjects": all_subject_states(store),
        "schedule": schedule,
        "recommendations": generate_recommendations(store, schedule=schedule),
        "analytics": compute_analytics(store),
        "settings": store["settings"],
    }
