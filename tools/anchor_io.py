#!/usr/bin/env python3
"""Canonical anchor file I/O.

All tools that read or write data/anchors.json must use these functions
to ensure stable formatting and minimal diffs.

Format rules:
- indent=2, sorted keys
- floats: lat/lon to 7 decimal places, elev to 1, tolerance to 2
- anchors and scale_anchors arrays: one object per element, sorted by id
- no trailing whitespace, single trailing newline
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ANCHOR_FILE = ROOT / "data" / "anchors.json"


def load():
    """Load anchors.json and return parsed dict."""
    with open(ANCHOR_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save(data):
    """Write anchors.json in canonical format (stable diffs)."""
    # Normalize float precision before serializing
    for a in data.get("anchors", []):
        a["lat"] = round(a["lat"], 7)
        a["lon"] = round(a["lon"], 7)
        a["elev"] = round(a["elev"], 1)
        a["tolerance_m"] = round(a["tolerance_m"], 2)
    for s in data.get("scale_anchors", []):
        s["value_m"] = round(s["value_m"], 2)
        s["tolerance_m"] = round(s["tolerance_m"], 2)

    # Sort arrays by id for stable ordering
    data["anchors"] = sorted(data["anchors"], key=lambda x: x["id"])
    data["scale_anchors"] = sorted(data.get("scale_anchors", []), key=lambda x: x["id"])

    raw = json.dumps(data, indent=2, sort_keys=False, ensure_ascii=False)

    # Normalize trailing whitespace and ensure single trailing newline
    lines = [line.rstrip() for line in raw.splitlines()]
    output = "\n".join(lines) + "\n"

    with open(ANCHOR_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write(output)


def modify_anchor(anchor_id, **updates):
    """Load, update one anchor by id, save. Returns the modified anchor."""
    data = load()
    target = None
    for a in data["anchors"]:
        if a["id"] == anchor_id:
            target = a
            break
    if target is None:
        raise KeyError(f"Anchor {anchor_id} not found")
    for k, v in updates.items():
        if k not in target:
            raise KeyError(f"Unknown field '{k}' on anchor {anchor_id}")
        target[k] = v
    save(data)
    return target
