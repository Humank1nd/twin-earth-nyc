# Residual + Correction Policy v0

**Document:** Part 04 — Earth Reality Layer
**Status:** v0 Draft
**Scope:** Tracked residuals, correction policy, validation harness
**Authority:** All corrections to the truth layer (geospatial, structural, semantic) must follow this policy. No ad-hoc fixes.

---

## 1. Residuals Tracked

Five residual categories are continuously monitored. Each has a warn threshold (triggers investigation) and a correct threshold (triggers mandatory correction).

### 1.1 Anchor Drift

| Property | Specification |
|---|---|
| **Definition** | Euclidean distance between an anchor's placed position in-engine and its reference WGS84 position (converted to ENU) |
| **Warn Threshold** | 0.5 m |
| **Correct Threshold** | 1.0 m |
| **Measurement Method** | Automated Anchor Checker (see Anchor Set document, Section 3). Positions compared in ENU coordinate space. |
| **Cadence** | Nightly CI build; on-demand after truth-layer edits |
| **Affected Systems** | Navigation mesh alignment, NPC pathfinding, crosswalk intelligence, camera FOV registration |

### 1.2 Skyline Silhouette Mismatch

| Property | Specification |
|---|---|
| **Definition** | Percentage of pixels differing between the engine's building silhouette render and a reference silhouette image, measured via Canny edge detection and Hausdorff distance |
| **Warn Threshold** | 5% pixel deviation |
| **Correct Threshold** | 10% pixel deviation |
| **Measurement Method** | Fixed virtual cameras at 4 cardinal positions (N, S, E, W) at 500 m distance, 200 m elevation, aimed at Times Square center. Render silhouette-only pass (buildings = white, sky = black). Compare against reference renders via edge map overlap. |
| **Cadence** | Weekly; after any building model update |
| **Affected Systems** | Visual fidelity, player orientation, landmark recognition, skyline-based navigation |

### 1.3 Road / Sidewalk Boundary Mismatch

| Property | Specification |
|---|---|
| **Definition** | Lateral distance between engine curb-line geometry and georeferenced curb-line data (NYC DOT planimetric dataset) |
| **Warn Threshold** | 0.3 m |
| **Correct Threshold** | 0.5 m |
| **Measurement Method** | Extract curb-line polylines from engine collision mesh (top-down orthographic projection). Overlay with reference polylines from NYC Open Data. Measure maximum perpendicular distance (Hausdorff) per block segment. |
| **Cadence** | After any road/sidewalk geometry edit; weekly sweep |
| **Affected Systems** | Pedestrian/vehicle zone separation, crosswalk intelligence, NPC curb-step behavior, ADA ramp placement |

### 1.4 Landmark Pose Mismatch

| Property | Specification |
|---|---|
| **Definition** | Angular rotation error (degrees) and scale error (percent) of major building models compared to photo reference |
| **Warn Threshold** | 2 degrees rotation OR 2% scale deviation |
| **Correct Threshold** | 5 degrees rotation OR 5% scale deviation |
| **Measurement Method** | For each landmark building: capture engine render from 3 standardized viewpoints. Extract corner features. Compute homography against reference photos. Decompose homography into rotation and scale components. |
| **Cadence** | After any building model replacement or transform edit; monthly full sweep |
| **Affected Systems** | Visual plausibility, shadow casting accuracy, billboard placement, anchor point registration |

### 1.5 Signal Placement Zone Drift

| Property | Specification |
|---|---|
| **Definition** | Distance between a traffic signal's engine position and its expected position zone (defined by intersection geometry and DOT placement standards) |
| **Warn Threshold** | 1.0 m |
| **Correct Threshold** | 2.0 m |
| **Measurement Method** | For each signal entity, compute distance to the nearest valid placement zone (intersection corner, +/- standard offset per DOT specs). Automated check reads signal entity positions and intersection anchor positions. |
| **Cadence** | After any intersection geometry or signal entity edit; weekly sweep |
| **Affected Systems** | Crosswalk intelligence (signal-crosswalk linkage), NPC crossing behavior, traffic simulation accuracy |

---

## 2. Residual Summary Table

| # | Residual | Warn | Correct | Cadence | Measurement |
|---|---|---|---|---|---|
| 1 | Anchor drift | 0.5 m | 1.0 m | Nightly | ENU distance comparison |
| 2 | Skyline silhouette | 5% px | 10% px | Weekly | Edge detection overlap |
| 3 | Road/sidewalk boundary | 0.3 m | 0.5 m | Weekly | Curb-line Hausdorff distance |
| 4 | Landmark pose | 2 deg / 2% | 5 deg / 5% | Monthly | Homography decomposition |
| 5 | Signal placement zone | 1.0 m | 2.0 m | Weekly | Zone distance check |

---

## 3. Correction Policy

### 3.1 Core Rule

> **"Truth layer gets corrected first; illusion layer re-renders after."**

All corrections operate on the truth layer: the scene graph transforms, collision meshes, anchor positions, and semantic labels. The illusion layer (rendered visuals, LOD meshes, lightmaps) is derived from the truth layer and re-generated automatically after any truth-layer correction. Never apply pixel-level or visual-only patches to compensate for truth-layer errors.

### 3.2 Correction Cadence

| Rule | Specification |
|---|---|
| **Maximum correction rate** | 1 truth-layer correction per sim-day per affected entity. This prevents visual jitter from rapid successive adjustments. |
| **Illusion layer update** | May update every frame. After a truth-layer correction, the illusion layer re-renders immediately but this is not counted as a "correction." |
| **Batch corrections** | If multiple residuals exceed thresholds simultaneously, corrections are batched into a single atomic commit applied at the next sim-day boundary. |
| **Emergency override** | If a residual exceeds 3x the correct threshold (e.g., anchor drift > 3.0 m), an immediate correction is applied regardless of cadence. Logged as `EMERGENCY_CORRECTION`. |

### 3.3 Correction Targets

All corrections are applied to **latent scene graph transforms**, not pixel-level adjustments:

| Correction Type | Target | Operation |
|---|---|---|
| Anchor drift | Entity transform (position vector) | Translate entity to corrected ENU position |
| Skyline silhouette | Building prim transforms (scale, rotation) | Adjust building scale/rotation to match reference silhouette |
| Road/sidewalk boundary | Collision mesh vertex positions | Shift curb-line vertices to match reference polylines |
| Landmark pose | Building prim transform (rotation, scale) | Apply corrective rotation and scale to building root prim |
| Signal placement | Signal entity transform (position) | Translate signal entity to valid placement zone |

### 3.4 Rollback Protocol

Every correction is logged in the correction ledger with full before/after state, enabling rollback if a correction introduces new problems.

**Ledger Entry Schema:**

```json
{
  "correction_id": "string — unique identifier",
  "timestamp": "ISO 8601 UTC",
  "residual_type": "anchor_drift | skyline | road_boundary | landmark_pose | signal_zone",
  "entity_id": "string — affected entity",
  "before_state": {
    "transform": { "position": [x, y, z], "rotation": [qx, qy, qz, qw], "scale": [sx, sy, sz] },
    "residual_value": "float — measured residual before correction"
  },
  "after_state": {
    "transform": { "position": [x, y, z], "rotation": [qx, qy, qz, qw], "scale": [sx, sy, sz] },
    "residual_value": "float — measured residual after correction"
  },
  "auto_revert_window": 100,
  "reverted": false,
  "revert_reason": "string | null"
}
```

**Auto-Revert Rules:**

| Condition | Action |
|---|---|
| Correction breaks gameplay (detected within **100 sim-ticks**) | Automatic revert to `before_state`. Flag entity for manual review. |
| "Breaks gameplay" definition | Any of: NPC pathfinding failure rate > 5%, physics collision anomaly count > 10, anchor checker reports new FAIL that did not exist before correction, player-facing visual glitch reported by QA bot |
| Manual revert | Operator can revert any correction via ledger UI within 7 real-time days. After 7 days, correction is considered permanent. |
| Revert cascade | If reverting correction A would invalidate correction B (applied after A to the same entity), both are reverted and flagged for manual review. |

---

## 4. Validation Harness — "Reference Verification Walk"

### 4.1 Route Definition

A fixed 12-point walking route through Times Square, designed to cover all major landmark zones and anchor clusters. Total distance: approximately 1.2 km.

| Waypoint | Location | Anchor References | Key Checks |
|---|---|---|---|
| WP-01 | 42nd St & Broadway — NW corner | ANC-001, ANC-019 | Intersection geometry, signal placement |
| WP-02 | 42nd St & 7th Ave — SE corner | ANC-004, ANC-003 | Subway entrance alignment, curb geometry |
| WP-03 | One Times Square — base NE | ANC-012 | Building base alignment, billboard registration |
| WP-04 | 43rd St pedestrian area | (interpolated) | Road/sidewalk boundary continuity |
| WP-05 | 44th St & Broadway — curb cut | ANC-015 | ADA ramp geometry, crosswalk alignment |
| WP-06 | TKTS Red Steps — bottom | ANC-010 | Step geometry, elevation accuracy |
| WP-07 | TKTS Red Steps — top | ANC-009 | Skyline view south, silhouette check |
| WP-08 | Father Duffy statue | ANC-017 | Monument placement, Duffy Square geometry |
| WP-09 | 45th St & Broadway | ANC-005 | Pedestrian plaza boundary, Marriott Marquis entrance alignment |
| WP-10 | 45th St & 7th Ave | ANC-007, ANC-016 | Intersection geometry, curb cut, signal placement |
| WP-11 | 46th St & Broadway | ANC-021 | Plaza bollard alignment, signal placement |
| WP-12 | 47th St & 7th Ave | ANC-008 | Northern boundary, Duffy Square completion, NYPD substation position |

### 4.2 Capture Protocol

At each waypoint, capture a standardized screenshot set:

| Capture | Camera Direction | FOV | Resolution | Purpose |
|---|---|---|---|---|
| `{WP}_forward.png` | Direction of travel (south to north along route) | 60 deg | 1920x1080 | Primary scene composition check |
| `{WP}_left.png` | 90 deg left of travel direction | 60 deg | 1920x1080 | Lateral building/street alignment |
| `{WP}_right.png` | 90 deg right of travel direction | 60 deg | 1920x1080 | Lateral building/street alignment |
| `{WP}_up.png` | Straight up (zenith) | 90 deg | 1920x1080 | Skyline silhouette, building height check |

Total captures per walk: **48 screenshots** (12 waypoints x 4 directions).

### 4.3 Execution Triggers

| Trigger | Requirement |
|---|---|
| After any truth-layer correction | Mandatory full walk |
| Nightly CI build | Automated walk (headless renderer) |
| Before any release milestone | Manual walk by QA with visual sign-off |
| After major asset import (new building, new block) | Mandatory full walk |

### 4.4 Pass Criteria

The Reference Verification Walk passes if ALL of the following are met:

| Criterion | Measurement | Threshold |
|---|---|---|
| No anchor exceeds tolerance | Anchor Checker results for all 25 anchors | All PASS (zero FAIL) |
| No silhouette regression | Skyline comparison at WP-07 (elevated vantage) and 4 cardinal cameras | No increase in pixel deviation vs. previous passing baseline |
| All nav tests pass | Automated NPC dispatched along walk route; must complete without pathfinding failure | 100% waypoint arrival, 0 stuck events |
| No new collision anomalies | Physics anomaly counter during walk | Zero new anomalies (existing known issues excluded) |
| Screenshot diff within budget | Perceptual hash (pHash) comparison of each capture against baseline set | Hamming distance < 12 bits per capture (allows lighting variation, rejects structural changes) |

### 4.5 Baseline Management

| Rule | Specification |
|---|---|
| **Baseline creation** | New baseline captured after a full walk passes all criteria AND is manually approved by lead artist + tech lead |
| **Baseline versioning** | Baselines stored as `baseline_v{N}_{date}/` with full screenshot set + Anchor Checker JSON + nav test log |
| **Baseline promotion** | Only the latest approved baseline is used for comparison. Previous baselines retained for historical audit. |
| **Baseline invalidation** | A baseline is invalidated if the anchor set document is revised (new anchors added, coordinates changed). New baseline required. |

---

## 5. Correction Flow Summary

```
Residual Detected (automated monitor)
    │
    ├── Below warn threshold → No action. Log metric.
    │
    ├── Between warn and correct threshold → Log WARNING.
    │   Add to weekly review queue. No automated correction.
    │
    ├── Above correct threshold → Schedule correction for next sim-day boundary.
    │   │
    │   ├── Apply truth-layer correction (scene graph transform).
    │   ├── Log correction in ledger (before/after state).
    │   ├── Illusion layer re-renders automatically.
    │   ├── Run Reference Verification Walk.
    │   │   │
    │   │   ├── Walk PASSES → Correction accepted. Monitor continues.
    │   │   │
    │   │   └── Walk FAILS → Check if failure is within 100 sim-ticks.
    │   │       │
    │   │       ├── Yes → Auto-revert correction. Flag for manual review.
    │   │       │
    │   │       └── No → Flag for manual review. Correction remains pending.
    │   │
    │   └── (end)
    │
    └── Above 3x correct threshold → EMERGENCY. Immediate correction.
        Apply same flow but skip sim-day boundary wait.
```

---

*End of Residual + Correction Policy v0.*
