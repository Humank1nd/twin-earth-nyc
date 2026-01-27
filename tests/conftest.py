import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

@pytest.fixture
def root():
    return ROOT

@pytest.fixture
def anchor_data():
    with open(ROOT / "data" / "anchors.json", "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture
def schema_dir():
    return ROOT / "schemas"

@pytest.fixture
def docs_dir():
    return ROOT / "docs"
