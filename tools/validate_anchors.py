#!/usr/bin/env python3
"""Anchor validation tool.

Loads data/anchors.json, checks every anchor against bounding box,
tolerance constraints, type coverage, and inter-anchor distances.
Outputs a structured report to stdout and optionally to a JSON file.
"""

import json
import math
import os
import sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
ANCHOR_FILE = ROOT / "data" / "anchors.json"

# Expected bounding box (from anchor-set doc)
BBOX = {
    "lat_min": 40.7555,
    "lat_max": 40.7600,
    "lon_min": -73.9880,
    "lon_max": -73.9840,
    "elev_min": 9.0,
    "elev_max": 115.0,
}

REQUIRED_TYPES = {
    "intersection",
    "structure",
    "building-base",
    "curb-cut",
    "monument",
    "signal",
    "subway-entrance",
    "building-entrance",
}

MIN_ANCHOR_COUNT = 15  # doc requires 15-30


def haversine_m(lat1, lon1, lat2, lon2):
    """Great-circle distance in meters between two WGS84 points."""
    R = 6_371_000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def load_anchors():
    with open(ANCHOR_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def validate(data):
    results = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "anchor_file": str(ANCHOR_FILE),
        "checks": [],
        "summary": {"total": 0, "pass": 0, "warn": 0, "fail": 0},
    }
    anchors = data["anchors"]
    scale_anchors = data.get("scale_anchors", [])

    def add(name, status, detail=""):
        results["checks"].append({"check": name, "status": status, "detail": detail})
        results["summary"][status] += 1
        results["summary"]["total"] += 1

    # --- Count check ---
    n = len(anchors)
    if n >= MIN_ANCHOR_COUNT:
        add("anchor_count", "pass", f"{n} anchors (>= {MIN_ANCHOR_COUNT})")
    else:
        add("anchor_count", "fail", f"{n} anchors (< {MIN_ANCHOR_COUNT})")

    # --- Bounding box check ---
    bbox_violations = []
    for a in anchors:
        issues = []
        if not (BBOX["lat_min"] <= a["lat"] <= BBOX["lat_max"]):
            issues.append(f'lat {a["lat"]} outside [{BBOX["lat_min"]}, {BBOX["lat_max"]}]')
        if not (BBOX["lon_min"] <= a["lon"] <= BBOX["lon_max"]):
            issues.append(f'lon {a["lon"]} outside [{BBOX["lon_min"]}, {BBOX["lon_max"]}]')
        if not (BBOX["elev_min"] <= a["elev"] <= BBOX["elev_max"]):
            issues.append(f'elev {a["elev"]} outside [{BBOX["elev_min"]}, {BBOX["elev_max"]}]')
        if issues:
            bbox_violations.append(f'{a["id"]}: {"; ".join(issues)}')

    if not bbox_violations:
        add("bounding_box", "pass", f"All {n} anchors within bounding box")
    else:
        add("bounding_box", "fail", f"{len(bbox_violations)} violations: {bbox_violations}")

    # --- Unique IDs ---
    ids = [a["id"] for a in anchors]
    dupes = [x for x in ids if ids.count(x) > 1]
    if not dupes:
        add("unique_ids", "pass", f"{n} unique IDs")
    else:
        add("unique_ids", "fail", f"Duplicate IDs: {set(dupes)}")

    # --- Type coverage ---
    found_types = {a["type"] for a in anchors}
    missing = REQUIRED_TYPES - found_types
    if not missing:
        add("type_coverage", "pass", f"All {len(REQUIRED_TYPES)} required types present")
    else:
        add("type_coverage", "fail", f"Missing types: {missing}")

    # --- Tolerance range check ---
    tol_issues = []
    for a in anchors:
        t = a["tolerance_m"]
        if t <= 0:
            tol_issues.append(f'{a["id"]}: tolerance {t} <= 0')
        elif t > 5.0:
            tol_issues.append(f'{a["id"]}: tolerance {t} > 5.0m (suspiciously large)')
    if not tol_issues:
        add("tolerance_range", "pass", "All tolerances in (0, 5.0]")
    else:
        add("tolerance_range", "warn", "; ".join(tol_issues))

    # --- Minimum inter-anchor distance (3D: horizontal + vertical) ---
    min_dist = float("inf")
    min_pair = ("", "")
    for i in range(n):
        for j in range(i + 1, n):
            horiz = haversine_m(anchors[i]["lat"], anchors[i]["lon"], anchors[j]["lat"], anchors[j]["lon"])
            vert = abs(anchors[i]["elev"] - anchors[j]["elev"])
            d3d = math.sqrt(horiz ** 2 + vert ** 2)
            if d3d < min_dist:
                min_dist = d3d
                min_pair = (anchors[i]["id"], anchors[j]["id"])
    if min_dist > 1.0:
        add("min_spacing", "pass", f"Min 3D distance {min_dist:.1f}m between {min_pair[0]} and {min_pair[1]}")
    elif min_dist > 0.5:
        add("min_spacing", "warn", f"Very close anchors: {min_dist:.1f}m (3D) between {min_pair[0]} and {min_pair[1]}")
    else:
        add("min_spacing", "fail", f"Overlapping anchors (3D): {min_dist:.1f}m between {min_pair[0]} and {min_pair[1]}")

    # --- Bounding box dimensions ---
    lats = [a["lat"] for a in anchors]
    lons = [a["lon"] for a in anchors]
    elevs = [a["elev"] for a in anchors]
    ns_span = haversine_m(min(lats), min(lons), max(lats), min(lons))
    ew_span = haversine_m(min(lats), min(lons), min(lats), max(lons))
    add("bbox_dimensions", "pass",
        f"N-S: {ns_span:.0f}m, E-W: {ew_span:.0f}m, Elev: {min(elevs):.1f}-{max(elevs):.1f}m")

    # --- Scale anchors ---
    if scale_anchors:
        sa_issues = []
        for sa in scale_anchors:
            if sa["value_m"] <= 0:
                sa_issues.append(f'{sa["id"]}: value {sa["value_m"]} <= 0')
            if sa["tolerance_m"] <= 0:
                sa_issues.append(f'{sa["id"]}: tolerance {sa["tolerance_m"]} <= 0')
            if sa["tolerance_m"] >= sa["value_m"]:
                sa_issues.append(f'{sa["id"]}: tolerance >= value')
        if not sa_issues:
            add("scale_anchors", "pass", f"{len(scale_anchors)} scale anchors valid")
        else:
            add("scale_anchors", "fail", "; ".join(sa_issues))
    else:
        add("scale_anchors", "warn", "No scale anchors defined")

    # --- Type distribution ---
    from collections import Counter
    type_counts = Counter(a["type"] for a in anchors)
    add("type_distribution", "pass",
        ", ".join(f"{t}: {c}" for t, c in sorted(type_counts.items())))

    return results


def print_report(results):
    s = results["summary"]
    print("=" * 68)
    print("  ANCHOR VALIDATION REPORT")
    print(f"  {results['timestamp']}")
    print(f"  Source: {results['anchor_file']}")
    print("=" * 68)
    print()
    for c in results["checks"]:
        icon = {"pass": "PASS", "warn": "WARN", "fail": "FAIL"}[c["status"]]
        mark = {"pass": "+", "warn": "~", "fail": "!"}[c["status"]]
        print(f"  [{mark}] {icon}  {c['check']}")
        if c["detail"]:
            for line in str(c["detail"]).split("; "):
                print(f"           {line}")
        print()
    print("-" * 68)
    print(f"  TOTAL: {s['total']}  |  PASS: {s['pass']}  |  WARN: {s['warn']}  |  FAIL: {s['fail']}")
    overall = "PASS" if s["fail"] == 0 else "FAIL"
    print(f"  OVERALL: {overall}")
    print("-" * 68)
    return overall


def main():
    if not ANCHOR_FILE.exists():
        print(f"ERROR: {ANCHOR_FILE} not found", file=sys.stderr)
        sys.exit(1)

    data = load_anchors()
    results = validate(data)
    overall = print_report(results)

    # Write JSON report
    report_path = ROOT / "data" / "anchor-report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n  JSON report: {report_path}")

    sys.exit(0 if overall == "PASS" else 1)


if __name__ == "__main__":
    main()
