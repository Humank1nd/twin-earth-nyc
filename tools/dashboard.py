#!/usr/bin/env python3
"""Project status dashboard.

Prints a terminal-based overview of the Twin Earth NYC project state:
- Part completion (file counts, line counts)
- Schema status
- Anchor summary
- Validation gate status
"""

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / "docs"
SCHEMA_DIR = ROOT / "schemas"
ANCHOR_FILE = ROOT / "data" / "anchors.json"

PART_NAMES = {
    1: "Core Vision",
    2: "Simulation Architecture",
    3: "World Model AI",
    4: "Earth Reality",
    5: "AlphaEvolve",
    6: "City-as-Living-System",
    7: "IoT Artifacts",
    8: "NPC Realism",
    9: "Forced Perspective",
    10: "Build Pipeline",
    11: "Multiverse Gameplay",
    12: "Times Square Slice",
    13: "Scaling Strategy",
}


def count_lines(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return sum(1 for _ in f)
    except Exception:
        return 0


def get_git_info():
    try:
        sha = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=str(ROOT), stderr=subprocess.DEVNULL
        ).decode().strip()
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=str(ROOT), stderr=subprocess.DEVNULL
        ).decode().strip()
        return sha, branch
    except Exception:
        return "no-repo", "n/a"


def main():
    sha, branch = get_git_info()

    # Header
    print()
    print("+" + "=" * 66 + "+")
    print("|" + " TWIN EARTH NYC — PROJECT DASHBOARD ".center(66) + "|")
    print("+" + "=" * 66 + "+")
    print(f"|  Branch: {branch:<20s}  Commit: {sha:<25s}  |")
    print("+" + "-" * 66 + "+")
    print()

    # Parts table
    print("  PART DELIVERABLES")
    print("  " + "-" * 62)
    print(f"  {'#':<4} {'Name':<26} {'Files':>5} {'Lines':>7} {'Status':>8}")
    print("  " + "-" * 62)

    total_files = 0
    total_lines = 0
    all_pass = True

    for i in range(1, 14):
        pattern = f"part-{i:02d}-*"
        matches = list(DOCS_DIR.glob(pattern))
        if matches:
            d = matches[0]
            files = list(d.glob("*.md"))
            n_files = len(files)
            n_lines = sum(count_lines(f) for f in files)
            status = "OK" if n_files > 0 else "EMPTY"
        else:
            n_files = 0
            n_lines = 0
            status = "MISSING"
            all_pass = False

        total_files += n_files
        total_lines += n_lines
        name = PART_NAMES.get(i, "Unknown")
        print(f"  {i:<4} {name:<26} {n_files:>5} {n_lines:>7} {status:>8}")

    print("  " + "-" * 62)
    print(f"  {'':4} {'TOTAL':<26} {total_files:>5} {total_lines:>7}")
    print()

    # Schemas
    schema_files = sorted(SCHEMA_DIR.glob("*.schema.json"))
    schema_valid = 0
    schema_invalid = 0
    for sf in schema_files:
        try:
            with open(sf, "r", encoding="utf-8") as f:
                json.load(f)
            schema_valid += 1
        except Exception:
            schema_invalid += 1

    print("  SCHEMAS")
    print("  " + "-" * 62)
    print(f"  Total: {len(schema_files)}  |  Valid JSON: {schema_valid}  |  Invalid: {schema_invalid}")
    schema_lines = sum(count_lines(f) for f in schema_files)
    print(f"  Total lines: {schema_lines}")
    print()

    # Anchors
    if ANCHOR_FILE.exists():
        with open(ANCHOR_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        anchors = data["anchors"]
        scales = data.get("scale_anchors", [])
        lats = [a["lat"] for a in anchors]
        lons = [a["lon"] for a in anchors]
        tols = [a["tolerance_m"] for a in anchors]

        print("  ANCHOR REGISTRY")
        print("  " + "-" * 62)
        print(f"  geo_anchors_count:   {len(anchors)}")
        print(f"  scale_anchors_count: {len(scales)}")
        print(f"  total_anchors_count: {len(anchors) + len(scales)}")
        print(f"  Lat range:   {min(lats):.4f} — {max(lats):.4f}")
        print(f"  Lon range:   {min(lons):.4f} — {max(lons):.4f}")
        print(f"  Tolerance:   {min(tols):.2f}m — {max(tols):.2f}m")
        from collections import Counter
        tc = Counter(a["type"] for a in anchors)
        print(f"  Types:       {dict(tc)}")
    else:
        print("  ANCHOR REGISTRY: NOT FOUND")
        all_pass = False
    print()

    # Validation gates
    print("  VALIDATION GATES")
    print("  " + "-" * 62)
    gates = [
        ("anchors.json exists", ANCHOR_FILE.exists()),
        ("schemas/ has 12 files", len(schema_files) == 12),
        ("All schemas valid JSON", schema_invalid == 0),
        ("All 13 parts have docs", all_pass),
        ("data/anchors.json loadable", ANCHOR_FILE.exists()),
    ]
    for name, ok in gates:
        mark = "+" if ok else "!"
        status = "PASS" if ok else "FAIL"
        print(f"  [{mark}] {status}  {name}")

    gate_pass = all(ok for _, ok in gates)
    print()
    print("  " + "-" * 62)
    overall = "READY" if gate_pass else "NOT READY"
    print(f"  BUNDLE STATUS: {overall}")
    print("+" + "=" * 66 + "+")
    print()

    # Grand total
    grand_lines = total_lines + schema_lines
    grand_files = total_files + len(schema_files) + (1 if ANCHOR_FILE.exists() else 0)
    print(f"  Grand total: {grand_files} files, {grand_lines} lines")
    print()

    sys.exit(0 if gate_pass else 1)


if __name__ == "__main__":
    main()
