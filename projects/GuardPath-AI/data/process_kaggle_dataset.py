"""
GuardPath - Real-data processing script.

Turns the raw Kaggle "Bangalore CAS Alerts" dataset (real GPS-tagged
collision-avoidance-system alerts from vehicles driving through
Bangalore) into GuardPath's area dataset (data/city_areas.csv) and
road network (utils/city_graph.py), instead of hand-invented numbers.

Source dataset: bangalore-cas-alerts.csv
  columns used: deviceCode_location_latitude, deviceCode_location_longitude,
  deviceCode_location_wardName, deviceCode_pyld_alarmType,
  deviceCode_time_recordedTime_$date

Alarm types in the raw data and what they mean:
  FCW       Forward Collision Warning        - sudden hard-braking / crash risk
  UFCW      Urban Forward Collision Warning   - same, at urban/low speed
  PCW       Pedestrian Collision Warning      - a pedestrian was in the vehicle's path
  HMW       Headway Monitoring Warning        - following too close (congestion/tailgating)
  LDWL/LDWR Lane Departure Warning (L/R)       - vehicle drifted out of its lane
  Overspeed Speed limit exceeded

HOW EACH GUARDPATH FEATURE IS DERIVED (real, not invented):
  traffic_level        <- HMW rate + UFCW rate   (congestion / dense-traffic interactions)
  road_condition       <- inverse of (LDW rate + FCW rate)  (lane-departure + hard-braking
                           events are treated as a proxy for hazardous/poor road segments)
  crime_rate            <- PCW rate (pedestrian-collision-warning rate). NOTE: this is a
                           pedestrian-hazard-exposure proxy from real sensor alerts, not
                           police-recorded crime statistics - there is no public locality-level
                           crime dataset for Bangalore, so this is the closest real substitute.
  lighting_condition    <- inverse of the share of a ward's alerts that occur at night
                           (20:00-05:59). This is an ESTIMATE, not a direct light-sensor
                           reading - no lighting data exists in the source dataset.

All four are min-max scaled to 0-10 across the included wards.

Run:
    python process_kaggle_dataset.py
"""

import csv
import math
import os
from collections import defaultdict
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_PATH = os.path.join(BASE_DIR, "data", "kaggle_reference", "bangalore_cas", "bangalore-cas-alerts.csv")
AREAS_OUT = os.path.join(BASE_DIR, "data", "city_areas.csv")
GRAPH_OUT = os.path.join(BASE_DIR, "utils", "city_graph.py")
STATS_OUT = os.path.join(BASE_DIR, "data", "kaggle_reference", "ward_derivation_stats.csv")

MIN_ALERTS = 200          # ignore wards with too little data to be meaningful
NIGHT_HOURS = set([20, 21, 22, 23, 0, 1, 2, 3, 4, 5]
                   )
K_NEAREST = 3              # road-network connections per ward
EXCLUDE_WARDS = {"other", "Other", ""}


def load_raw():
    rows_by_ward = defaultdict(list)
    with open(RAW_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ward = row["deviceCode_location_wardName"].strip()
            if ward in EXCLUDE_WARDS:
                continue
            rows_by_ward[ward].append(row)
    return rows_by_ward


def parse_hour(iso_str):
    try:
        return datetime.strptime(iso_str, "%Y-%m-%dT%H:%M:%S.%fZ").hour
    except ValueError:
        return None


def aggregate(rows_by_ward):
    stats = {}
    for ward, rows in rows_by_ward.items():
        n = len(rows)
        if n < MIN_ALERTS:
            continue

        alarm_count = defaultdict(int)
        night_count = 0
        lat_sum = lon_sum = 0.0
        speed_sum = 0.0
        speed_n = 0

        for row in rows:
            alarm_count[row["deviceCode_pyld_alarmType"]] += 1
            lat_sum += float(row["deviceCode_location_latitude"])
            lon_sum += float(row["deviceCode_location_longitude"])
            hour = parse_hour(row["deviceCode_time_recordedTime_$date"])
            if hour is not None and hour in NIGHT_HOURS:
                night_count += 1
            try:
                speed_sum += float(row["deviceCode_pyld_speed"])
                speed_n += 1
            except (ValueError, KeyError):
                pass

        ldw = alarm_count.get("LDWL", 0) + alarm_count.get("LDWR", 0)
        stats[ward] = {
            "alert_count": n,
            "lat": round(lat_sum / n, 5),
            "lon": round(lon_sum / n, 5),
            "avg_speed": round(speed_sum / speed_n, 1) if speed_n else 0.0,
            "pcw_rate": alarm_count.get("PCW", 0) / n,
            "hmw_rate": alarm_count.get("HMW", 0) / n,
            "ufcw_rate": alarm_count.get("UFCW", 0) / n,
            "fcw_rate": alarm_count.get("FCW", 0) / n,
            "ldw_rate": ldw / n,
            "overspeed_rate": alarm_count.get("Overspeed", 0) / n,
            "night_ratio": night_count / n,
        }
    return stats


def minmax_scale(values):
    lo, hi = min(values), max(values)
    span = (hi - lo) or 1.0
    return [round(max(0.0, min(10.0, (v - lo) / span * 10)), 1) for v in values]


def build_features(stats):
    wards = list(stats.keys())

    traffic_raw = [stats[w]["hmw_rate"] + stats[w]["ufcw_rate"] for w in wards]
    hazard_raw = [stats[w]["ldw_rate"] + stats[w]["fcw_rate"] * 0.5 for w in wards]
    pcw_raw = [stats[w]["pcw_rate"] for w in wards]
    night_raw = [stats[w]["night_ratio"] for w in wards]

    traffic_scaled = minmax_scale(traffic_raw)
    hazard_scaled = minmax_scale(hazard_raw)          # higher = worse road condition
    crime_scaled = minmax_scale(pcw_raw)               # higher = worse (more pedestrian risk)
    night_scaled = minmax_scale(night_raw)             # higher = more night-skewed activity

    features = {}
    for i, ward in enumerate(wards):
        features[ward] = {
            "crime_rate": crime_scaled[i],
            "road_condition": round(10 - hazard_scaled[i], 1),
            "lighting_condition": round(10 - night_scaled[i], 1),
            "traffic_level": traffic_scaled[i],
            "lat": stats[ward]["lat"],
            "lon": stats[ward]["lon"],
        }
    return features


def haversine_km(a, b):
    lat1, lon1 = a
    lat2, lon2 = b
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    x = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.asin(math.sqrt(x))


def build_network(features):
    names = list(features.keys())
    coords = {n: (features[n]["lat"], features[n]["lon"]) for n in names}

    dist = {}
    for a in names:
        for b in names:
            if a != b:
                dist[(a, b)] = haversine_km(coords[a], coords[b])

    network = defaultdict(dict)
    for a in names:
        nearest = sorted((b for b in names if b != a), key=lambda b: dist[(a, b)])[:K_NEAREST]
        for b in nearest:
            d = round(dist[(a, b)], 1)
            network[a][b] = d
            network[b][a] = d

    # ensure the graph is fully connected: bridge any isolated components
    def component_of(start, adj):
        seen = {start}
        stack = [start]
        while stack:
            cur = stack.pop()
            for nxt in adj[cur]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        return seen

    while True:
        main_component = component_of(names[0], network)
        if len(main_component) == len(names):
            break
        outside = [n for n in names if n not in main_component]
        best_pair, best_dist = None, float("inf")
        for a in main_component:
            for b in outside:
                if dist[(a, b)] < best_dist:
                    best_dist, best_pair = dist[(a, b)], (a, b)
        a, b = best_pair
        network[a][b] = round(best_dist, 1)
        network[b][a] = round(best_dist, 1)

    return dict(network)


def write_city_areas(features):
    with open(AREAS_OUT, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["area_name", "crime_rate", "road_condition", "lighting_condition", "traffic_level", "lat", "lon"])
        for name in sorted(features):
            f_ = features[name]
            writer.writerow([name, f_["crime_rate"], f_["road_condition"], f_["lighting_condition"], f_["traffic_level"], f_["lat"], f_["lon"]])
    print(f"Wrote {len(features)} real wards -> {AREAS_OUT}")


def write_stats(stats, features):
    with open(STATS_OUT, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "area_name", "alert_count", "avg_speed_kmph", "pcw_rate", "hmw_rate", "ufcw_rate",
            "fcw_rate", "ldw_rate", "overspeed_rate", "night_ratio",
            "derived_crime_rate", "derived_road_condition", "derived_lighting_condition", "derived_traffic_level",
        ])
        for name in sorted(stats):
            s, f_ = stats[name], features[name]
            writer.writerow([
                name, s["alert_count"], s["avg_speed"], round(s["pcw_rate"], 4), round(s["hmw_rate"], 4),
                round(s["ufcw_rate"], 4), round(s["fcw_rate"], 4), round(s["ldw_rate"], 4),
                round(s["overspeed_rate"], 4), round(s["night_ratio"], 4),
                f_["crime_rate"], f_["road_condition"], f_["lighting_condition"], f_["traffic_level"],
            ])
    print(f"Wrote derivation audit trail -> {STATS_OUT}")


def write_city_graph(network):
    lines = [
        '"""',
        "GuardPath - Predefined road network.",
        "",
        "AUTO-GENERATED by data/process_kaggle_dataset.py - do not hand-edit.",
        "",
        "Nodes are real Bangalore wards taken from the Kaggle 'Bangalore CAS Alerts'",
        "dataset (real GPS coordinates, averaged per ward). Edges connect each ward",
        "to its 3 nearest neighbours by straight-line (haversine) distance, since the",
        "source dataset has no actual road-segment data. Distances are straight-line",
        "km, not real driving distance - a simplification, documented in README.md.",
        '"""',
        "",
        "ROAD_NETWORK = {",
    ]
    for area in sorted(network):
        neighbors = ", ".join(f'"{n}": {d}' for n, d in sorted(network[area].items()))
        lines.append(f'    "{area}": {{{neighbors}}},')
    lines.append("}")
    lines.append("")
    lines.append("")
    lines.append("def area_list():")
    lines.append("    return sorted(ROAD_NETWORK.keys())")
    lines.append("")
    lines.append("")
    lines.append("def all_edges():")
    lines.append('    """Every road segment once (undirected), for drawing the base map."""')
    lines.append("    seen = set()")
    lines.append("    edges = []")
    lines.append("    for area, neighbors in ROAD_NETWORK.items():")
    lines.append("        for neighbor, distance in neighbors.items():")
    lines.append("            key = tuple(sorted((area, neighbor)))")
    lines.append("            if key not in seen:")
    lines.append("                seen.add(key)")
    lines.append('                edges.append({"from": key[0], "to": key[1], "distance_km": distance})')
    lines.append("    return edges")
    lines.append("")
    lines.append("")
    lines.append("def find_routes(source, destination, max_routes=3, max_hops=6):")
    lines.append('    """Depth-first search that enumerates simple (loop-free) paths between')
    lines.append("    source and destination, keeping the shortest `max_routes` by distance.")
    lines.append("    This models 'the application identifies all predefined routes")
    lines.append("    connecting the selected locations' from the abstract.")
    lines.append('    """')
    lines.append("    if source not in ROAD_NETWORK or destination not in ROAD_NETWORK:")
    lines.append("        return []")
    lines.append("    if source == destination:")
    lines.append("        return []")
    lines.append("")
    lines.append("    found = []")
    lines.append("")
    lines.append("    def dfs(current, path, distance, visited):")
    lines.append("        if len(path) - 1 > max_hops:")
    lines.append("            return")
    lines.append("        if current == destination:")
    lines.append("            found.append((list(path), distance))")
    lines.append("            return")
    lines.append("        for neighbor, dist in ROAD_NETWORK[current].items():")
    lines.append("            if neighbor not in visited:")
    lines.append("                visited.add(neighbor)")
    lines.append("                path.append(neighbor)")
    lines.append("                dfs(neighbor, path, distance + dist, visited)")
    lines.append("                path.pop()")
    lines.append("                visited.discard(neighbor)")
    lines.append("")
    lines.append('    dfs(source, [source], 0.0, {source})')
    lines.append("    found.sort(key=lambda item: item[1])")
    lines.append("    return found[:max_routes]")
    lines.append("")

    with open(GRAPH_OUT, "w") as f:
        f.write("\n".join(lines))
    print(f"Wrote road network ({len(network)} wards) -> {GRAPH_OUT}")


def main():
    rows_by_ward = load_raw()
    stats = aggregate(rows_by_ward)
    print(f"{len(stats)} wards have >= {MIN_ALERTS} alerts and will be used")

    features = build_features(stats)
    network = build_network(features)

    write_city_areas(features)
    write_stats(stats, features)
    write_city_graph(network)


if __name__ == "__main__":
    main()
