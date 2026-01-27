#!/usr/bin/env python3
"""JSON Schema validation tool.

Validates that every .schema.json file in schemas/ is:
1. Valid JSON
2. Valid JSON Schema (draft 2020-12)
3. Self-consistent (required fields exist in properties, enums non-empty, etc.)
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = ROOT / "schemas"

try:
    from jsonschema import Draft202012Validator, ValidationError
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False


def check_schema_file(path):
    """Returns (status, detail) where status is 'pass', 'warn', or 'fail'."""
    # 1. Valid JSON?
    try:
        with open(path, "r", encoding="utf-8") as f:
            schema = json.load(f)
    except json.JSONDecodeError as e:
        return "fail", f"Invalid JSON: {e}"

    # 2. Has required fields?
    issues = []
    if "type" not in schema and "$ref" not in schema:
        issues.append("Missing top-level 'type' or '$ref'")
    if "title" not in schema:
        issues.append("Missing 'title'")

    # 3. Validate against JSON Schema meta-schema (if library available)
    if HAS_JSONSCHEMA:
        try:
            Draft202012Validator.check_schema(schema)
        except Exception as e:
            return "fail", f"Invalid schema: {e}"

    # 4. Self-consistency checks
    props = schema.get("properties", {})
    required = schema.get("required", [])
    for r in required:
        if r not in props:
            issues.append(f"Required field '{r}' not in properties")

    # Check enum fields aren't empty
    def check_enums(obj, path=""):
        if isinstance(obj, dict):
            if "enum" in obj and len(obj["enum"]) == 0:
                issues.append(f"Empty enum at {path}")
            for k, v in obj.items():
                check_enums(v, f"{path}.{k}")
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                check_enums(item, f"{path}[{i}]")
    check_enums(schema)

    if issues:
        return "warn", "; ".join(issues)

    # Count fields for reporting
    n_props = len(props)
    n_required = len(required)
    n_defs = len(schema.get("$defs", {}))
    return "pass", f"{n_props} properties, {n_required} required, {n_defs} $defs"


def main():
    schema_files = sorted(SCHEMA_DIR.glob("*.schema.json"))
    if not schema_files:
        print("ERROR: No schema files found in schemas/", file=sys.stderr)
        sys.exit(1)

    print("=" * 68)
    print("  JSON SCHEMA VALIDATION REPORT")
    print("=" * 68)
    print()

    total = pass_count = warn_count = fail_count = 0
    for path in schema_files:
        status, detail = check_schema_file(path)
        total += 1
        if status == "pass":
            pass_count += 1
        elif status == "warn":
            warn_count += 1
        else:
            fail_count += 1

        mark = {"pass": "+", "warn": "~", "fail": "!"}[status]
        tag = status.upper()
        print(f"  [{mark}] {tag}  {path.name}")
        print(f"           {detail}")
        print()

    print("-" * 68)
    print(f"  TOTAL: {total}  |  PASS: {pass_count}  |  WARN: {warn_count}  |  FAIL: {fail_count}")
    overall = "PASS" if fail_count == 0 else "FAIL"
    print(f"  OVERALL: {overall}")
    if not HAS_JSONSCHEMA:
        print("  NOTE: jsonschema not installed; meta-schema validation skipped")
    print("-" * 68)

    sys.exit(0 if overall == "PASS" else 1)


if __name__ == "__main__":
    main()
