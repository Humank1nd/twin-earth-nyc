"""Tests for cross-reference integrity and project structure."""
import re
from pathlib import Path


class TestPartCompleteness:
    EXPECTED_PARTS = 13

    def test_all_parts_exist(self, docs_dir):
        for i in range(1, self.EXPECTED_PARTS + 1):
            matches = list(docs_dir.glob(f"part-{i:02d}-*"))
            assert matches, f"Part {i} directory missing"

    def test_all_parts_have_files(self, docs_dir):
        for i in range(1, self.EXPECTED_PARTS + 1):
            matches = list(docs_dir.glob(f"part-{i:02d}-*"))
            if matches:
                files = list(matches[0].glob("*.md"))
                assert len(files) >= 3, \
                    f"Part {i} has only {len(files)} files (need >= 3)"

    def test_minimum_deliverable_counts(self, docs_dir):
        """Each part should have at least the number of deliverables the spec requires."""
        min_counts = {
            1: 3, 2: 4, 3: 5, 4: 5, 5: 5, 6: 4, 7: 5,
            8: 5, 9: 5, 10: 5, 11: 6, 12: 6, 13: 5,
        }
        for part, min_c in min_counts.items():
            matches = list(docs_dir.glob(f"part-{part:02d}-*"))
            assert matches, f"Part {part} missing"
            files = list(matches[0].glob("*.md"))
            assert len(files) >= min_c, \
                f"Part {part}: {len(files)} files < required {min_c}"


class TestAnchorReferences:
    def test_anchor_ids_in_docs_resolve(self, anchor_data, docs_dir):
        """Every ANC-### ref in docs should exist in anchors.json."""
        defined = {a["id"] for a in anchor_data["anchors"]}
        all_refs = set()
        for md in docs_dir.rglob("*.md"):
            text = md.read_text(encoding="utf-8", errors="replace")
            all_refs.update(re.findall(r"ANC-\d{3}", text))
        missing = all_refs - defined
        assert not missing, f"Docs reference undefined anchors: {missing}"


class TestDocQuality:
    def test_no_empty_docs(self, docs_dir):
        for md in docs_dir.rglob("*.md"):
            size = md.stat().st_size
            assert size > 100, f"{md.name} is only {size} bytes (likely empty)"

    def test_minimum_line_counts(self, docs_dir):
        for md in docs_dir.rglob("*.md"):
            with open(md, "r", encoding="utf-8", errors="replace") as f:
                lines = sum(1 for _ in f)
            assert lines >= 50, f"{md.name} has only {lines} lines (need >= 50)"

    def test_all_have_headers(self, docs_dir):
        for md in docs_dir.rglob("*.md"):
            text = md.read_text(encoding="utf-8", errors="replace")
            assert text.strip().startswith("#"), \
                f"{md.name} doesn't start with a markdown header"


class TestDataFiles:
    def test_anchors_json_exists(self, root):
        assert (root / "data" / "anchors.json").exists()

    def test_requirements_txt_exists(self, root):
        assert (root / "requirements.txt").exists()
