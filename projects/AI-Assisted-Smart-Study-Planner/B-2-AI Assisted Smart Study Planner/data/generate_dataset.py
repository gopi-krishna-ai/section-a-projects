"""
AI-Assisted Smart Study Planner - Training dataset generator.

Generates a simulated dataset (priority_dataset.csv) used to train the
Random Forest model that predicts a subject's study PRIORITY
(High / Medium / Low) from four features:

  days_to_exam     - how many days remain until that subject's exam
  completion_pct   - % of the syllabus already completed
  difficulty       - subject difficulty, 1 (easy) - 5 (hard)
  weightage        - exam importance/credit weight, 1 (low) - 5 (high)

Each priority class is sampled from its own feature distribution
(same balanced-archetype technique used in the GuardPath project),
which keeps the classes balanced and avoids a trivial majority class.

Run:
    python generate_dataset.py
"""

import csv
import os
import random

random.seed(42)

OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "priority_dataset.csv")
SAMPLES_PER_CLASS = 140
LABEL_NOISE_RATE = 0.04

# mean, std-dev per feature, per class
CLASS_PROFILES = {
    "High": {
        "days_to_exam": (7, 4),
        "completion_pct": (30, 15),
        "difficulty": (4.0, 0.8),
        "weightage": (4.0, 0.8),
    },
    "Medium": {
        "days_to_exam": (20, 7),
        "completion_pct": (55, 15),
        "difficulty": (3.0, 0.9),
        "weightage": (3.0, 0.9),
    },
    "Low": {
        "days_to_exam": (45, 15),
        "completion_pct": (80, 12),
        "difficulty": (2.0, 0.8),
        "weightage": (2.0, 0.8),
    },
}

ADJACENT_LABEL = {"High": "Medium", "Medium": "Low", "Low": "Medium"}


def clip(value, lo, hi):
    return max(lo, min(hi, value))


def generate_row(label):
    p = CLASS_PROFILES[label]
    days_to_exam = round(clip(random.gauss(*p["days_to_exam"]), 0, 90))
    completion_pct = round(clip(random.gauss(*p["completion_pct"]), 0, 100))
    difficulty = round(clip(random.gauss(*p["difficulty"]), 1, 5))
    weightage = round(clip(random.gauss(*p["weightage"]), 1, 5))
    return days_to_exam, completion_pct, difficulty, weightage, label


def main():
    rows = []
    for label in CLASS_PROFILES:
        rows.extend(generate_row(label) for _ in range(SAMPLES_PER_CLASS))
    random.shuffle(rows)

    flip_count = int(LABEL_NOISE_RATE * len(rows))
    flip_indices = random.sample(range(len(rows)), flip_count)
    for i in flip_indices:
        days_to_exam, completion_pct, difficulty, weightage, label = rows[i]
        rows[i] = (days_to_exam, completion_pct, difficulty, weightage, ADJACENT_LABEL[label])

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["days_to_exam", "completion_pct", "difficulty", "weightage", "priority"])
        writer.writerows(rows)

    print(f"Generated {len(rows)} rows -> {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
