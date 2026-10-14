"""
AI-Assisted Smart Study Planner - real-data benchmark processing.

Source: Kaggle "Students Performance in Exams (Extended)" dataset -
30,641 real student records with weekly study hours, test-prep-course
completion, sport practice frequency, and Math/Reading/Writing scores.

This dataset has no "days to exam" or "syllabus completion" concept,
so it CANNOT be used to retrain the priority classifier (see
data/generate_dataset.py for that - it stays a documented synthetic
dataset). What it DOES give us is real evidence for two of the app's
recommendation rules: how weekly study hours and test-prep completion
actually relate to exam scores. This script computes those real
averages and saves them as an auditable CSV that utils/planner_engine.py
reads at runtime.

Run:
    python process_kaggle_dataset.py
"""

import csv
import os
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_PATH = os.path.join(BASE_DIR, "data", "kaggle_reference", "Expanded_data_with_more_features.csv")
OUT_PATH = os.path.join(BASE_DIR, "data", "kaggle_reference", "study_benchmarks.csv")


def main():
    by_hours = defaultdict(list)
    by_prep = defaultdict(list)
    by_sport = defaultdict(list)

    with open(RAW_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                avg = (float(row["MathScore"]) + float(row["ReadingScore"]) + float(row["WritingScore"])) / 3
            except ValueError:
                continue

            wh = row["WklyStudyHours"].strip()
            if wh:
                by_hours[wh].append(avg)
            tp = row["TestPrep"].strip()
            if tp:
                by_prep[tp].append(avg)
            ps = row["PracticeSport"].strip()
            if ps:
                by_sport[ps].append(avg)

    rows = []
    for category, groups in [
        ("WklyStudyHours", by_hours),
        ("TestPrep", by_prep),
        ("PracticeSport", by_sport),
    ]:
        for subgroup, values in groups.items():
            rows.append((category, subgroup, round(sum(values) / len(values), 2), len(values)))

    with open(OUT_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["category", "subgroup", "avg_score", "n"])
        writer.writerows(rows)

    print(f"Wrote {len(rows)} real benchmark rows -> {OUT_PATH}")
    for r in rows:
        print(" ", r)


if __name__ == "__main__":
    main()
