"""
GuardPath - Training dataset generator.

Generates a simulated dataset (area_dataset.csv) representing the
environmental safety attributes of many locations. This is the data
the Random Forest model is trained on. No external API, GPS device,
or live data source is used - everything is generated locally so the
project can run completely offline, as described in the abstract.

Each safety class (Safe / Moderate / Unsafe) is sampled from its own
feature distribution (a common technique for simulated ML datasets),
which keeps the classes balanced and gives the model a realistic,
non-trivial - but learnable - pattern to pick up on.

Run:
    python generate_dataset.py
"""

import csv
import os
import random

random.seed(42)

OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "area_dataset.csv")
SAMPLES_PER_CLASS = 120
LABEL_NOISE_RATE = 0.04  # fraction of rows relabelled to an adjacent class to mimic real-world ambiguity

# mean, std-dev per feature, per class
CLASS_PROFILES = {
    "Safe": {
        "crime_rate": (2.0, 1.0),
        "road_condition": (8.0, 1.0),
        "lighting_condition": (8.0, 1.0),
        "traffic_level": (4.0, 1.5),
    },
    "Moderate": {
        "crime_rate": (5.0, 1.2),
        "road_condition": (5.5, 1.2),
        "lighting_condition": (5.5, 1.2),
        "traffic_level": (5.5, 1.5),
    },
    "Unsafe": {
        "crime_rate": (7.5, 1.2),
        "road_condition": (3.0, 1.2),
        "lighting_condition": (3.0, 1.2),
        "traffic_level": (6.0, 1.8),
    },
}

ADJACENT_LABEL = {"Safe": "Moderate", "Moderate": "Unsafe", "Unsafe": "Moderate"}


def clip(value, lo=0.0, hi=10.0):
    return max(lo, min(hi, value))


def generate_row(label):
    profile = CLASS_PROFILES[label]
    crime_rate = round(clip(random.gauss(*profile["crime_rate"])), 1)
    road_condition = round(clip(random.gauss(*profile["road_condition"])), 1)
    lighting_condition = round(clip(random.gauss(*profile["lighting_condition"])), 1)
    traffic_level = round(clip(random.gauss(*profile["traffic_level"])), 1)
    return crime_rate, road_condition, lighting_condition, traffic_level, label


def main():
    rows = []
    for label in CLASS_PROFILES:
        rows.extend(generate_row(label) for _ in range(SAMPLES_PER_CLASS))
    random.shuffle(rows)

    # Simulate real-world label noise/ambiguity near class boundaries
    flip_count = int(LABEL_NOISE_RATE * len(rows))
    flip_indices = random.sample(range(len(rows)), flip_count)
    for i in flip_indices:
        crime_rate, road_condition, lighting_condition, traffic_level, label = rows[i]
        rows[i] = (crime_rate, road_condition, lighting_condition, traffic_level, ADJACENT_LABEL[label])

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["crime_rate", "road_condition", "lighting_condition", "traffic_level", "safety_label"])
        writer.writerows(rows)

    print(f"Generated {len(rows)} rows -> {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
