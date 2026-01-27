"""Tests for anchor data integrity."""
import math


def haversine_m(lat1, lon1, lat2, lon2):
    R = 6_371_000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


class TestAnchorCount:
    def test_minimum_anchor_count(self, anchor_data):
        assert len(anchor_data["anchors"]) >= 15, "Need at least 15 anchors per spec"

    def test_maximum_anchor_count(self, anchor_data):
        assert len(anchor_data["anchors"]) <= 30, "Spec says 15-30 anchors"

    def test_scale_anchor_count(self, anchor_data):
        assert len(anchor_data.get("scale_anchors", [])) == 10


class TestAnchorIDs:
    def test_unique_ids(self, anchor_data):
        ids = [a["id"] for a in anchor_data["anchors"]]
        assert len(ids) == len(set(ids)), f"Duplicate IDs found"

    def test_id_format(self, anchor_data):
        for a in anchor_data["anchors"]:
            assert a["id"].startswith("ANC-"), f'{a["id"]} bad format'
            num = a["id"].split("-")[1]
            assert num.isdigit() and len(num) == 3, f'{a["id"]} bad number'

    def test_sequential_ids(self, anchor_data):
        nums = sorted(int(a["id"].split("-")[1]) for a in anchor_data["anchors"])
        assert nums == list(range(1, len(nums) + 1)), "IDs not sequential"


class TestBoundingBox:
    BBOX = {"lat_min": 40.755, "lat_max": 40.760,
            "lon_min": -73.988, "lon_max": -73.984,
            "elev_min": 9.0, "elev_max": 115.0}

    def test_all_within_bbox(self, anchor_data):
        for a in anchor_data["anchors"]:
            assert self.BBOX["lat_min"] <= a["lat"] <= self.BBOX["lat_max"], \
                f'{a["id"]} lat {a["lat"]} out of bounds'
            assert self.BBOX["lon_min"] <= a["lon"] <= self.BBOX["lon_max"], \
                f'{a["id"]} lon {a["lon"]} out of bounds'
            assert self.BBOX["elev_min"] <= a["elev"] <= self.BBOX["elev_max"], \
                f'{a["id"]} elev {a["elev"]} out of bounds'

    def test_ns_span_reasonable(self, anchor_data):
        lats = [a["lat"] for a in anchor_data["anchors"]]
        span = haversine_m(min(lats), -73.985, max(lats), -73.985)
        assert 300 < span < 600, f"N-S span {span:.0f}m outside 300-600m range"

    def test_ew_span_reasonable(self, anchor_data):
        lons = [a["lon"] for a in anchor_data["anchors"]]
        span = haversine_m(40.758, min(lons), 40.758, max(lons))
        assert 200 < span < 400, f"E-W span {span:.0f}m outside 200-400m range"


class TestTolerances:
    def test_positive(self, anchor_data):
        for a in anchor_data["anchors"]:
            assert a["tolerance_m"] > 0, f'{a["id"]} tolerance <= 0'

    def test_tightest(self, anchor_data):
        tols = [a["tolerance_m"] for a in anchor_data["anchors"]]
        assert min(tols) == 0.3, "Tightest tolerance should be 0.3m per spec"

    def test_loosest(self, anchor_data):
        tols = [a["tolerance_m"] for a in anchor_data["anchors"]]
        assert max(tols) == 2.0, "Loosest tolerance should be 2.0m per spec"

    def test_structure_tight(self, anchor_data):
        """TKTS steps and curb cuts should have 0.3m tolerance."""
        for a in anchor_data["anchors"]:
            if a["type"] in ("structure", "curb-cut", "monument"):
                assert a["tolerance_m"] <= 0.3, \
                    f'{a["id"]} type={a["type"]} tolerance {a["tolerance_m"]} > 0.3'


class TestTypeCoverage:
    REQUIRED = {"intersection", "structure", "building-base", "curb-cut",
                "monument", "signal", "subway-entrance", "building-entrance"}

    def test_all_types_present(self, anchor_data):
        found = {a["type"] for a in anchor_data["anchors"]}
        missing = self.REQUIRED - found
        assert not missing, f"Missing anchor types: {missing}"

    def test_intersection_count(self, anchor_data):
        n = sum(1 for a in anchor_data["anchors"] if a["type"] == "intersection")
        assert n >= 6, f"Only {n} intersection anchors; need >= 6"


class TestScaleAnchors:
    def test_all_positive_values(self, anchor_data):
        for sa in anchor_data["scale_anchors"]:
            assert sa["value_m"] > 0, f'{sa["id"]} value <= 0'

    def test_tolerance_less_than_value(self, anchor_data):
        for sa in anchor_data["scale_anchors"]:
            assert sa["tolerance_m"] < sa["value_m"], \
                f'{sa["id"]} tolerance >= value'

    def test_door_height(self, anchor_data):
        door = next(s for s in anchor_data["scale_anchors"] if "door" in s["name"].lower())
        assert door["value_m"] == 2.1

    def test_taxi_length(self, anchor_data):
        taxi = next(s for s in anchor_data["scale_anchors"] if "taxi" in s["name"].lower())
        assert taxi["value_m"] == 4.8

    def test_human_height(self, anchor_data):
        human = next(s for s in anchor_data["scale_anchors"] if "human" in s["name"].lower())
        assert 1.5 <= human["value_m"] <= 2.0


class TestMinimumSpacing:
    def test_no_overlapping_anchors(self, anchor_data):
        anchors = anchor_data["anchors"]
        for i in range(len(anchors)):
            for j in range(i + 1, len(anchors)):
                d = haversine_m(
                    anchors[i]["lat"], anchors[i]["lon"],
                    anchors[j]["lat"], anchors[j]["lon"])
                assert d > 0.5, \
                    f'{anchors[i]["id"]} and {anchors[j]["id"]} only {d:.1f}m apart'
