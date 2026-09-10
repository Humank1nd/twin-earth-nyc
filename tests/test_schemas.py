"""Tests for JSON schema validity."""
import json


class TestSchemaFiles:
    EXPECTED_SCHEMAS = [
        "artifact.schema.json",
        "entity.schema.json",
        "event-bus-message.schema.json",
        "heat-state.schema.json",
        "ledger-event.schema.json",
        "npc.schema.json",
        "observation.schema.json",
        "operation.schema.json",
        "portal.schema.json",
        "portal-identity-pruned.schema.json",
        "alphaevolve-fitness-ledger.schema.json",
        "proposal.schema.json",
        "universe-profile.schema.json",
        "world-state-node.schema.json",
    ]

    def test_all_schemas_exist(self, schema_dir):
        existing = {f.name for f in schema_dir.glob("*.schema.json")}
        for expected in self.EXPECTED_SCHEMAS:
            assert expected in existing, f"Missing schema: {expected}"

    def test_no_extra_schemas(self, schema_dir):
        existing = {f.name for f in schema_dir.glob("*.schema.json")}
        expected = set(self.EXPECTED_SCHEMAS)
        extra = existing - expected
        assert not extra, f"Unexpected schemas: {extra}"

    def test_count(self, schema_dir):
        assert len(list(schema_dir.glob("*.schema.json"))) == 14


class TestSchemaValidity:
    def test_all_valid_json(self, schema_dir):
        for path in schema_dir.glob("*.schema.json"):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)  # raises on invalid JSON
            assert isinstance(data, dict), f"{path.name} root is not object"

    def test_all_have_title(self, schema_dir):
        for path in schema_dir.glob("*.schema.json"):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            assert "title" in data, f"{path.name} missing title"

    def test_all_have_type_or_ref(self, schema_dir):
        for path in schema_dir.glob("*.schema.json"):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            assert "type" in data or "$ref" in data, \
                f"{path.name} missing 'type' or '$ref'"

    def test_required_fields_exist_in_properties(self, schema_dir):
        for path in schema_dir.glob("*.schema.json"):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            props = set(data.get("properties", {}).keys())
            required = data.get("required", [])
            for r in required:
                assert r in props, \
                    f"{path.name}: required field '{r}' not in properties"

    def test_no_empty_enums(self, schema_dir):
        def find_empty_enums(obj, path_str=""):
            issues = []
            if isinstance(obj, dict):
                if "enum" in obj and len(obj["enum"]) == 0:
                    issues.append(path_str)
                for k, v in obj.items():
                    issues.extend(find_empty_enums(v, f"{path_str}.{k}"))
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    issues.extend(find_empty_enums(item, f"{path_str}[{i}]"))
            return issues

        for path in schema_dir.glob("*.schema.json"):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            empties = find_empty_enums(data)
            assert not empties, f"{path.name} has empty enums at: {empties}"


class TestEntitySchema:
    def test_entity_has_key_fields(self, schema_dir):
        with open(schema_dir / "entity.schema.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        required = data.get("required", [])
        assert "entity_id" in required
        assert "entity_type" in required
        assert "position" in required

    def test_entity_types_comprehensive(self, schema_dir):
        with open(schema_dir / "entity.schema.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        types = data["properties"]["entity_type"]["enum"]
        for expected in ["person", "vehicle", "door", "camera", "portal", "anomaly"]:
            assert expected in types, f"entity_type missing '{expected}'"


class TestPortalSchema:
    def test_portal_has_states(self, schema_dir):
        with open(schema_dir / "portal.schema.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        # Should have portal state somewhere in the schema
        schema_str = json.dumps(data)
        assert "stable" in schema_str.lower() or "state" in schema_str.lower(), \
            "Portal schema should reference states"
