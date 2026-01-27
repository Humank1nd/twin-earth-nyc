"""Known-bad fixtures: prove tests catch real failures.

Each test constructs an intentionally invalid anchor dataset and verifies
the validation tooling rejects it with a clear error message.
"""

import copy
import json
import math
import pytest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def good_data():
    """Load the real, valid anchors.json as a starting point."""
    with open(ROOT / "data" / "anchors.json", "r", encoding="utf-8") as f:
        return json.load(f)


# ── Helpers to run the validator on mutated data ─────────────

def run_anchor_validation(data):
    """Import and run validate() on arbitrary data, return results dict."""
    import sys
    sys.path.insert(0, str(ROOT / "tools"))
    from validate_anchors import validate
    return validate(data)


def assert_has_failure(results, check_name, substring=""):
    """Assert that a specific check failed and the detail contains substring."""
    for c in results["checks"]:
        if c["check"] == check_name and c["status"] == "fail":
            if substring:
                assert substring in str(c["detail"]), \
                    f"Check '{check_name}' failed but detail missing '{substring}': {c['detail']}"
            return
    failed_checks = [(c["check"], c["status"]) for c in results["checks"]]
    pytest.fail(f"Expected check '{check_name}' to FAIL. Got: {failed_checks}")


# ── Known-bad: Duplicate ID ─────────────────────────────────

class TestKnownBadDuplicateID:
    def test_duplicate_id_detected(self, good_data):
        """Two anchors with the same ID must cause a unique_ids failure."""
        bad = copy.deepcopy(good_data)
        bad["anchors"][1]["id"] = bad["anchors"][0]["id"]  # duplicate ANC-001
        results = run_anchor_validation(bad)
        assert_has_failure(results, "unique_ids", "ANC-001")

    def test_error_message_names_the_duplicate(self, good_data):
        """The error message should identify which ID is duplicated."""
        bad = copy.deepcopy(good_data)
        bad["anchors"][5]["id"] = "ANC-003"  # force dupe
        results = run_anchor_validation(bad)
        assert_has_failure(results, "unique_ids", "ANC-003")


# ── Known-bad: Anchor outside bounding box ──────────────────

class TestKnownBadOutOfBounds:
    def test_lat_too_high(self, good_data):
        """Latitude above the bounding box must fail."""
        bad = copy.deepcopy(good_data)
        bad["anchors"][0]["lat"] = 40.80  # way north of Times Square
        results = run_anchor_validation(bad)
        assert_has_failure(results, "bounding_box", "ANC-001")

    def test_lon_out_of_range(self, good_data):
        """Longitude outside the bounding box must fail."""
        bad = copy.deepcopy(good_data)
        bad["anchors"][2]["lon"] = -74.05  # way west
        results = run_anchor_validation(bad)
        assert_has_failure(results, "bounding_box", "ANC-003")

    def test_elev_out_of_range(self, good_data):
        """Elevation below minimum must fail."""
        bad = copy.deepcopy(good_data)
        bad["anchors"][3]["elev"] = -5.0  # below sea level
        results = run_anchor_validation(bad)
        assert_has_failure(results, "bounding_box", "ANC-004")


# ── Known-bad: Tolerance out of range ───────────────────────

class TestKnownBadTolerance:
    def test_zero_tolerance(self, good_data):
        """Tolerance of exactly 0 must be flagged."""
        bad = copy.deepcopy(good_data)
        bad["anchors"][0]["tolerance_m"] = 0
        results = run_anchor_validation(bad)
        assert_has_failure(results, "tolerance_range", "ANC-001")

    def test_negative_tolerance(self, good_data):
        """Negative tolerance must be flagged."""
        bad = copy.deepcopy(good_data)
        bad["anchors"][0]["tolerance_m"] = -0.5
        results = run_anchor_validation(bad)
        assert_has_failure(results, "tolerance_range", "ANC-001")


# ── Known-bad: Missing required type ────────────────────────

class TestKnownBadMissingType:
    def test_no_intersection_type(self, good_data):
        """Removing all 'intersection' anchors must fail type_coverage."""
        bad = copy.deepcopy(good_data)
        bad["anchors"] = [a for a in bad["anchors"] if a["type"] != "intersection"]
        results = run_anchor_validation(bad)
        assert_has_failure(results, "type_coverage", "intersection")

    def test_no_subway_entrance(self, good_data):
        """Removing all 'subway-entrance' anchors must fail type_coverage."""
        bad = copy.deepcopy(good_data)
        bad["anchors"] = [a for a in bad["anchors"] if a["type"] != "subway-entrance"]
        results = run_anchor_validation(bad)
        assert_has_failure(results, "type_coverage", "subway-entrance")


# ── Known-bad: Too few anchors ──────────────────────────────

class TestKnownBadInsufficientCount:
    def test_too_few_anchors(self, good_data):
        """Fewer than 15 geo anchors must fail."""
        bad = copy.deepcopy(good_data)
        bad["anchors"] = bad["anchors"][:5]
        results = run_anchor_validation(bad)
        assert_has_failure(results, "geo_anchor_count", "5")


# ── Known-bad: Scale anchor issues ──────────────────────────

class TestKnownBadScaleAnchors:
    def test_scale_tolerance_exceeds_value(self, good_data):
        """Scale anchor where tolerance >= value must fail."""
        bad = copy.deepcopy(good_data)
        bad["scale_anchors"][0]["tolerance_m"] = 999.0
        results = run_anchor_validation(bad)
        assert_has_failure(results, "scale_anchors", bad["scale_anchors"][0]["id"])

    def test_scale_value_zero(self, good_data):
        """Scale anchor with value=0 must fail."""
        bad = copy.deepcopy(good_data)
        bad["scale_anchors"][0]["value_m"] = 0
        results = run_anchor_validation(bad)
        assert_has_failure(results, "scale_anchors", bad["scale_anchors"][0]["id"])


# ── Known-bad: Formatting churn ─────────────────────────────

class TestFormattingStability:
    def test_save_roundtrip_no_diff(self, good_data, tmp_path):
        """Loading and re-saving anchors.json must produce identical bytes."""
        import sys
        sys.path.insert(0, str(ROOT / "tools"))
        from anchor_io import load, save, ANCHOR_FILE

        original = ANCHOR_FILE.read_text(encoding="utf-8")
        data = load()
        save(data)
        after = ANCHOR_FILE.read_text(encoding="utf-8")

        # Restore original regardless of test outcome
        ANCHOR_FILE.write_text(original, encoding="utf-8")

        assert original == after, \
            "anchor_io.save() produced a different file on round-trip (formatting churn!)"

    def test_single_edit_minimal_diff(self, good_data, tmp_path):
        """Modifying one anchor field should change exactly one line."""
        import sys
        sys.path.insert(0, str(ROOT / "tools"))
        from anchor_io import load, save, ANCHOR_FILE

        original_lines = ANCHOR_FILE.read_text(encoding="utf-8").splitlines()

        data = load()
        # Change ANC-005 lat by a tiny amount
        for a in data["anchors"]:
            if a["id"] == "ANC-005":
                a["lat"] = 40.7583001
                break
        save(data)
        modified_lines = ANCHOR_FILE.read_text(encoding="utf-8").splitlines()

        # Restore original
        ANCHOR_FILE.write_text("\n".join(original_lines) + "\n", encoding="utf-8")

        # Count differing lines
        diff_count = sum(1 for a, b in zip(original_lines, modified_lines) if a != b)
        # Also check for length change (added/removed lines)
        length_diff = abs(len(original_lines) - len(modified_lines))

        assert length_diff == 0, \
            f"Line count changed by {length_diff} (expected 0)"
        assert diff_count == 1, \
            f"Expected exactly 1 line to differ, got {diff_count}"
