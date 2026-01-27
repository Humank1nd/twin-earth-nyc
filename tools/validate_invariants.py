#!/usr/bin/env python3
"""Cross-reference invariant validator.

Checks that:
1. Every anchor referenced in invariant specs exists in anchors.json
2. Every schema referenced by docs has a corresponding .schema.json
3. Part deliverables exist on disk
4. Scale anchors have consistent tolerances
5. No orphaned schemas (every schema is referenced somewhere)
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ANCHOR_FILE = ROOT / "data" / "anchors.json"
SCHEMA_DIR = ROOT / "schemas"
DOCS_DIR = ROOT / "docs"


def load_anchors():
    with open(ANCHOR_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def find_anchor_refs_in_docs():
    """Find all ANC-### references across markdown docs."""
    refs = set()
    for md in DOCS_DIR.rglob("*.md"):
        text = md.read_text(encoding="utf-8", errors="replace")
        refs.update(re.findall(r"ANC-\d{3}", text))
    return refs


def find_schema_refs_in_docs():
    """Find all .schema.json references across markdown docs."""
    refs = set()
    for md in DOCS_DIR.rglob("*.md"):
        text = md.read_text(encoding="utf-8", errors="replace")
        refs.update(re.findall(r"[\w-]+\.schema\.json", text))
    return refs


def check_part_dirs():
    """Check all 13 part directories exist and have at least 1 file."""
    issues = []
    for i in range(1, 14):
        pattern = f"part-{i:02d}-*"
        matches = list(DOCS_DIR.glob(pattern))
        if not matches:
            issues.append(f"Part {i}: directory not found")
            continue
        d = matches[0]
        files = list(d.glob("*.md"))
        if not files:
            issues.append(f"Part {i}: no .md files in {d.name}")
    return issues


def main():
    print("=" * 68)
    print("  INVARIANT CROSS-REFERENCE REPORT")
    print("=" * 68)
    print()

    total = pass_count = warn_count = fail_count = 0

    def add(name, status, detail=""):
        nonlocal total, pass_count, warn_count, fail_count
        total += 1
        if status == "pass":
            pass_count += 1
        elif status == "warn":
            warn_count += 1
        else:
            fail_count += 1
        mark = {"pass": "+", "warn": "~", "fail": "!"}[status]
        print(f"  [{mark}] {status.upper()}  {name}")
        if detail:
            for line in detail.split("\n"):
                print(f"           {line}")
        print()

    # 1. Anchor reference integrity
    data = load_anchors()
    defined_ids = {a["id"] for a in data["anchors"]}
    doc_refs = find_anchor_refs_in_docs()
    missing_anchors = doc_refs - defined_ids
    unreferenced = defined_ids - doc_refs
    if not missing_anchors:
        add("anchor_ref_integrity", "pass",
            f"{len(doc_refs)} refs in docs, all resolve to anchors.json")
    else:
        add("anchor_ref_integrity", "fail",
            f"Docs reference {missing_anchors} but they're not in anchors.json")
    if unreferenced:
        add("anchor_coverage", "warn",
            f"{len(unreferenced)} anchors not referenced in any doc: {unreferenced}")
    else:
        add("anchor_coverage", "pass", "All anchors referenced in docs")

    # 2. Schema file existence
    schema_files = {f.name for f in SCHEMA_DIR.glob("*.schema.json")}
    doc_schema_refs = find_schema_refs_in_docs()
    missing_schemas = doc_schema_refs - schema_files
    orphaned = schema_files - doc_schema_refs
    if not missing_schemas:
        add("schema_ref_integrity", "pass",
            f"All {len(doc_schema_refs)} schema refs in docs have files")
    else:
        add("schema_ref_integrity", "fail",
            f"Missing schema files: {missing_schemas}")
    if orphaned:
        add("schema_coverage", "warn",
            f"{len(orphaned)} schema files not referenced in docs: {orphaned}")
    else:
        add("schema_coverage", "pass", "All schemas referenced in docs")

    # 3. Part directory completeness
    part_issues = check_part_dirs()
    if not part_issues:
        add("part_completeness", "pass", "All 13 parts have directories with .md files")
    else:
        add("part_completeness", "fail", "\n".join(part_issues))

    # 4. Scale anchor tolerance consistency
    scale_anchors = data.get("scale_anchors", [])
    tol_ratio_issues = []
    for sa in scale_anchors:
        ratio = sa["tolerance_m"] / sa["value_m"]
        if ratio > 0.10:
            tol_ratio_issues.append(
                f'{sa["id"]} ({sa["name"]}): tolerance/value = {ratio:.1%}')
    if not tol_ratio_issues:
        add("scale_tolerance_ratio", "pass",
            f"All {len(scale_anchors)} scale anchors have tolerance < 10% of value")
    else:
        add("scale_tolerance_ratio", "warn", "\n".join(tol_ratio_issues))

    # 5. Deliverable count per part
    for i in range(1, 14):
        pattern = f"part-{i:02d}-*"
        matches = list(DOCS_DIR.glob(pattern))
        if matches:
            files = list(matches[0].glob("*.md"))
            add(f"part_{i:02d}_files", "pass", f"{len(files)} deliverables")

    print("-" * 68)
    print(f"  TOTAL: {total}  |  PASS: {pass_count}  |  WARN: {warn_count}  |  FAIL: {fail_count}")
    overall = "PASS" if fail_count == 0 else "FAIL"
    print(f"  OVERALL: {overall}")
    print("-" * 68)

    sys.exit(0 if overall == "PASS" else 1)


if __name__ == "__main__":
    main()
