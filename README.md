# Twin Earth NYC: Real-Time Planetary Digital Twin & Geodetic Simulation Engine

**Unreal Engine 5 • Cesium 3D Tiles • WGS84 Georeferencing • Sub-Meter Spatial Anchors**

[![Validation Suite](https://img.shields.io/badge/Geodetic%20Validation-10%2F10%20PASS-brightgreen.svg)]()
[![Coordinate Reference](https://img.shields.io/badge/Datum-WGS84%20(EPSG%3A4326)-blue.svg)]()
[![Vertical Datum](https://img.shields.io/badge/Elevation-EGM96%20Geoid-orange.svg)]()
[![License](https://img.shields.io/badge/License-MIT-purple.svg)]()

---

## 🏛️ Executive Summary

Traditional AAA game open-world and virtual production pipelines require **3–5 years, 80+ environment artists, and tens of millions of dollars** to manually model, texture, and optimize a 1:1 city slice like Manhattan.

**Twin Earth NYC** introduces a streaming, sub-centimeter photorealistic geospatial digital twin pipeline in **Unreal Engine 5** via **Cesium for Unreal** and **Google Photorealistic 3D Tiles**. Instead of hand-building greybox cities, development teams stream 1:1 planetary meshes on Day 1, bound to a mathematically rigorous geodetic datum and verified by automated spatial invariant tests.

```
TRADITIONAL AAA PIPELINE (36–48 Months)
[Concept] ──> [Greybox] ──> [Manual DCC Modeling] ──> [Manual LODs] ──> [Optimization Hell] ──> [Ship]
Cost: $30M–$60M+ | 100+ Artists | High Burn Rate

STREAMING DIGITAL TWIN PIPELINE (12–18 Months)
[WGS84 1:1 Base Mesh Online (Day 1)] ──> [Hero Props & Interiors] ──> [Nanite/Lumen Pass] ──> [Ship]
Cost: 70% Asset Budget Reduction | Focus on Dynamic Gameplay & Art Direction
```

---

## 📐 Spatial Anchoring & Geodetic Architecture

To eliminate visual jitter, floating meshes, and misaligned physics colliders across massive open worlds, Twin Earth implements a dual geodetic-to-engine coordinate transformation system:

- **Horizontal Reference:** WGS84 ellipsoidal coordinates (EPSG:4326, Latitude/Longitude).
- **Vertical Reference:** EGM96 geoidal elevation (Meters Above Sea Level).
- **Origin Anchor:** Times Square Center (`lat: 40.7580`, `lon: -73.9855`, `elev: 10.0m`).
- **Tolerance Budgets:** Sub-meter tolerances categorized by structural permanence:
  - Intersections & Curb-Cuts: $\le 0.5\text{ m}$
  - Structural Facades & Subways: $\le 0.3\text{ m}$
  - Apex & Monuments: $\le 0.2\text{ m}$

```
                  WGS84 Geodetic Survey Ground Truth
                                  │
                                  ▼
               [data/anchors.json Canonical Registry]
                                  │
         ┌────────────────────────┴────────────────────────┐
         ▼                                                 ▼
[Automated Invariant Checks]                    [UE5 Engine Substrate]
• Bounding box enclosure                        • Double-precision Large World Coordinates
• Spatial density & 3D separation               • Cesium for Unreal georeferenced origin
• Regression against baseline tolerances        • Chaos Physics / Nanite collision binding
```

---

## 🚀 Quickstart & Anchor Invariant Verification

Verify the entire geodetic anchor suite with a single command:

```bash
# Clone the repository
git clone https://github.com/Humank1nd/twin-earth-nyc.git
cd twin-earth-nyc

# Execute the automated geodetic validator
python3 tools/validate_anchors.py
```

### Validation Report Output
```text
====================================================================
  ANCHOR VALIDATION REPORT
  Source: data/anchors.json
====================================================================
  [+] PASS  geo_anchor_count    (25 geo anchors >= 15 threshold)
  [+] PASS  scale_anchor_count  (10 scale anchors, 35 total)
  [+] PASS  bounding_box        (All anchors enclosed in Times Square bounds)
  [+] PASS  unique_ids          (25 unique canonical IDs)
  [+] PASS  type_coverage       (8/8 required spatial landmark types present)
  [+] PASS  tolerance_range     (All tolerances within (0, 5.0m])
  [+] PASS  min_spacing         (Min 3D distance 8.4m between ANC-019 and ANC-025)
  [+] PASS  bbox_dimensions     (N-S: 411m, E-W: 270m, Elev: 10.0-111.0m)
--------------------------------------------------------------------
  TOTAL: 10  |  PASS: 10  |  WARN: 0  |  FAIL: 0
  OVERALL: PASS
--------------------------------------------------------------------
```

---

## 🛠️ Tooling & Workflows

| Tool | Purpose |
| :--- | :--- |
| [`tools/validate_anchors.py`](tools/validate_anchors.py) | Mathematical validation of anchor coordinates, tolerances, and distribution. |
| [`tools/validate_invariants.py`](tools/validate_invariants.py) | Enforces geodetic invariants and flags regressions before scene compilation. |
| [`tools/anchor_io.py`](tools/anchor_io.py) | Canonical JSON I/O interface preventing formatting drift across branches. |
| [`tools/demo.sh`](tools/demo.sh) | End-to-end simulation workflow showing branch modification, tolerance alerts, and promotion. |

---

## 📚 Architectural Specifications

Deep-dive engineering specs located in [`docs/`](docs/):
- **Simulation Architecture:** [`docs/part-02-simulation-architecture`](docs/part-02-simulation-architecture)
- **World Model AI & Traffic:** [`docs/part-03-world-model-ai`](docs/part-03-world-model-ai), [`docs/part-42-traffic-ai`](docs/part-42-traffic-ai)
- **NPC Realism & Living City:** [`docs/part-06-city-living-system`](docs/part-06-city-living-system), [`docs/part-08-npc-realism`](docs/part-08-npc-realism)
- **Times Square Vertical Slice:** [`docs/part-12-times-square-slice`](docs/part-12-times-square-slice)

---

## 📄 License & Attribution

Architected and developed by **Andrew Carling** ([@Humank1nd](https://github.com/Humank1nd)).  
Released under the MIT License.
