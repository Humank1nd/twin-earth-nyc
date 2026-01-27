# Constraint Test Suite v0

**Document:** Twin Earth NYC — Part 5, Deliverable 2
**Status:** v0 Draft
**Last Updated:** 2026-01-27
**Depends On:** Part 1 (World Bible), Part 2 (Simulation Systems), Part 4 (Evidence & Ledger), Evolvable Parameter Registry v0

---

## 1. Purpose

The Constraint Test Suite is the gatekeeper for AlphaEvolve. Every candidate configuration must pass **all** tests in this suite before it is eligible for scoring. A single failure means automatic discard. No exceptions. No overrides. No partial credit.

This suite verifies that a candidate configuration preserves the **canonical truths** of Twin Earth NYC:

- Geography does not move.
- Physics truth does not change.
- The ledger remains consistent and replayable.
- Navigation meshes remain intact.
- Entity identities are preserved.
- Evidence generation continues to function.

---

## 2. Test Registry

### 2.1 Master Test Table

| Test ID | Name | Description | Metric | Threshold | Action on Fail |
|---------|------|-------------|--------|-----------|----------------|
| CT-01 | ANCHOR_DRIFT | Measure maximum positional error of all anchor points against their canonical coordinates after a full scenario run. | `max_error_m` | < 1.0 m | **DISCARD** |
| CT-02 | COLLISION_WALK | Spawn an NPC at each of 10 predefined start points and navigate to 10 predefined end points. Count navigation snags (stuck > 2 sec, clipping through geometry, falling through world). | `snag_count` | = 0 | **DISCARD** |
| CT-03 | SEED_STABILITY | Run BASELINE_MIDDAY scenario with seed=42 twice using the candidate config. Compare ledger outputs byte-for-byte. | `ledger_diff_count` | = 0 | **DISCARD** |
| CT-04 | LEDGER_REPLAY | Run BASELINE_MIDDAY scenario, then replay the ledger. Compare simulation state at T=end between live run and replay. | `mismatch_count` | = 0 | **DISCARD** |
| CT-05 | SCALE_CHECK | Measure 5 scale anchor distances (see Section 3.1) and compare against canonical reference values. | `max_scale_error_pct` | < 2% | **DISCARD** |
| CT-06 | STREET_TOPOLOGY | Hash all crosswalk positions and curb vertex arrays. Compare hash against canonical reference. | `topology_diff` | = 0 | **DISCARD** |
| CT-07 | ENTITY_IDENTITY | After scenario run, enumerate all ledger-bound entities and verify each has a valid, unchanged entity ID mapping. | `orphan_count` | = 0 | **DISCARD** |
| CT-08 | EVIDENCE_FIDELITY | During POLICE_PURSUIT scenario, measure evidence event generation rate during the active pursuit phase. | `events_per_sec` | > 0.5 | **DISCARD** |
| CT-09 | NAV_INTEGRITY | Export navmesh walkable area polygons before and after candidate config application. Compare total walkable area. | `area_diff_pct` | < 0.1% | **DISCARD** |
| CT-10 | PHYSICS_TRUTH | Export all physics material properties (friction, restitution, density) and compare against canonical reference table. | `property_diff` | = 0 | **DISCARD** |

### 2.2 Pass/Fail Rule

```
RESULT = ALL(test.passed for test in [CT-01 .. CT-10])

if RESULT == TRUE:
    candidate proceeds to scoring
else:
    candidate is DISCARDED
    failure details are logged
    no scoring is performed
```

**There is no partial pass.** A candidate that passes 9 of 10 tests is treated identically to one that passes 0 of 10: it is discarded.

---

## 3. Test Specifications

### 3.1 CT-01: ANCHOR_DRIFT

**Purpose:** Verify that no canonical anchor point has moved beyond tolerance.

**Procedure:**
1. Load candidate configuration.
2. Run BASELINE_MIDDAY scenario (seed=42, 10 min).
3. At T=end, sample all registered anchor positions.
4. Compute Euclidean distance between each sampled position and its canonical reference.
5. Record `max_error_m` = max(all distances).

**Anchor Points Sampled:**
- Times Square center (Broadway & 7th Ave intersection)
- 42nd Street & 8th Ave corner
- 44th Street & Broadway corner
- Port Authority Bus Terminal entrance
- TKTS booth center point

**Threshold:** `max_error_m` < 1.0 m

**Failure Mode:** If any anchor has drifted > 1.0 m, the simulation world has been distorted. Discard immediately.

---

### 3.2 CT-02: COLLISION_WALK

**Purpose:** Verify that NPC navigation is unimpaired by the candidate configuration.

**Procedure:**
1. Load candidate configuration.
2. For each of 10 predefined routes:
   a. Spawn NPC at start position.
   b. Issue navigation command to end position.
   c. Monitor for snag conditions:
      - NPC stationary for > 2 seconds while not at destination
      - NPC mesh intersects world collision geometry
      - NPC Y-position drops below street level (fall-through)
   d. Record any snag as `snag_count += 1`.
3. Total `snag_count` across all 10 routes.

**Predefined Routes:**
| Route | Start | End | Expected Path |
|-------|-------|-----|---------------|
| R-01 | 42nd & 7th Ave (NE corner) | 44th & Broadway (SW corner) | Sidewalk north, cross Broadway |
| R-02 | Port Authority entrance | Times Square center | Sidewalk east on 42nd |
| R-03 | 43rd & 8th Ave | 43rd & 7th Ave | Sidewalk east on 43rd |
| R-04 | TKTS booth | 42nd & 8th Ave (NW corner) | Sidewalk south, west on 42nd |
| R-05 | 45th & Broadway | 41st & 7th Ave | Sidewalk south through Times Square |
| R-06 | 42nd & Broadway (center) | 42nd & Broadway (center) via loop | Circular path through adjacent blocks |
| R-07 | 44th & 8th Ave | Times Square center | Diagonal via 43rd |
| R-08 | 41st & Broadway | 45th & 8th Ave | North on Broadway, west on 45th |
| R-09 | 43rd & 7th Ave | Port Authority entrance | West on 43rd, south to entrance |
| R-10 | Times Square center | 44th & 7th Ave | North on 7th Ave sidewalk |

**Threshold:** `snag_count` = 0

**Failure Mode:** Any navigation failure indicates the candidate has corrupted walkable space or collision geometry. Discard immediately.

---

### 3.3 CT-03: SEED_STABILITY

**Purpose:** Verify deterministic simulation. Same seed, same config, same result.

**Procedure:**
1. Load candidate configuration.
2. Run BASELINE_MIDDAY scenario (seed=42, 10 min). Record full ledger output as `ledger_A`.
3. Reset simulation completely.
4. Run identical scenario again. Record full ledger output as `ledger_B`.
5. Perform byte-level diff: `ledger_diff_count` = number of differing ledger entries.

**Threshold:** `ledger_diff_count` = 0

**Failure Mode:** Non-determinism breaks replay, evidence consistency, and comparative analysis. Discard immediately.

**Note:** Floating-point determinism is required. The simulation must use deterministic math modes (no async GPU readback for simulation logic, fixed-order entity updates).

---

### 3.4 CT-04: LEDGER_REPLAY

**Purpose:** Verify that the ledger can faithfully reconstruct simulation state.

**Procedure:**
1. Load candidate configuration.
2. Run BASELINE_MIDDAY scenario (seed=42, 10 min). Record ledger and final simulation state `S_live`.
3. Reset simulation.
4. Replay ledger from beginning to end.
5. Capture final simulation state `S_replay`.
6. Compare `S_live` vs `S_replay`: count mismatches in entity positions (> 0.01 m), entity states, and event timestamps (> 1 ms).

**Threshold:** `mismatch_count` = 0

**Failure Mode:** Replay divergence means the ledger is not a faithful record. Evidence becomes unreliable. Discard immediately.

---

### 3.5 CT-05: SCALE_CHECK

**Purpose:** Verify that metric scale has not been distorted.

**Procedure:**
1. Load candidate configuration.
2. Measure 5 reference distances between known anchor pairs:

| Pair | Point A | Point B | Canonical Distance |
|------|---------|---------|-------------------|
| S-01 | Times Square center | TKTS booth center | 87.3 m |
| S-02 | 42nd & 7th Ave | 42nd & 8th Ave | 274.5 m |
| S-03 | 43rd & Broadway | 44th & Broadway | 80.1 m |
| S-04 | Port Authority entrance | 42nd & 8th Ave | 52.8 m |
| S-05 | 41st & 7th Ave | 45th & 7th Ave | 321.7 m |

3. Compute percentage error for each: `error_pct = abs(measured - canonical) / canonical * 100`.
4. Record `max_scale_error_pct` = max(all error percentages).

**Threshold:** `max_scale_error_pct` < 2%

**Failure Mode:** Scale distortion breaks spatial reasoning, navigation timing, and visual plausibility. Discard immediately.

---

### 3.6 CT-06: STREET_TOPOLOGY

**Purpose:** Verify that street layout is unchanged.

**Procedure:**
1. Load candidate configuration.
2. Export all crosswalk position arrays and curb vertex arrays.
3. Compute SHA-256 hash of the exported data.
4. Compare against canonical hash stored in reference file.
5. `topology_diff` = 0 if hashes match, 1 if they differ.

**Canonical Hash Reference:**
```json
{
  "crosswalks_hash": "CANONICAL_REF_HASH_CROSSWALKS",
  "curbs_hash": "CANONICAL_REF_HASH_CURBS",
  "generated_at": "2026-01-27T00:00:00Z",
  "reference_version": "1.0.0"
}
```

**Threshold:** `topology_diff` = 0

**Failure Mode:** Street topology change means an illegal target was modified. Discard immediately.

---

### 3.7 CT-07: ENTITY_IDENTITY

**Purpose:** Verify that all ledger-bound entities retain their canonical IDs.

**Procedure:**
1. Load candidate configuration.
2. Run BASELINE_MIDDAY scenario (seed=42, 10 min).
3. At T=end, enumerate all entities that have ledger entries.
4. For each entity, verify:
   a. Entity ID exists in the canonical entity registry.
   b. Entity ID has not been reassigned to a different entity type.
   c. Entity ID maps to exactly one active entity.
5. `orphan_count` = number of ledger entries referencing a non-existent or mismatched entity ID.

**Threshold:** `orphan_count` = 0

**Failure Mode:** Orphaned entity IDs break evidence chains and investigation logic. Discard immediately.

---

### 3.8 CT-08: EVIDENCE_FIDELITY

**Purpose:** Verify that evidence generation systems function during active incidents.

**Procedure:**
1. Load candidate configuration.
2. Run POLICE_PURSUIT scenario (seed=256, 5 min).
3. Identify the active pursuit phase (from chase trigger to resolution).
4. Count all evidence events generated during the pursuit phase.
5. Compute `events_per_sec` = total_events / pursuit_duration_sec.

**Evidence Event Types Counted:**
- CCTV capture events
- Witness observation events
- Physical evidence deposit events
- Radio communication events
- Vehicle tracking events

**Threshold:** `events_per_sec` > 0.5

**Failure Mode:** If evidence generation drops below threshold, the candidate configuration is starving the investigation system. Players cannot investigate. Discard immediately.

---

### 3.9 CT-09: NAV_INTEGRITY

**Purpose:** Verify that the navigation mesh has not been altered.

**Procedure:**
1. Load canonical navmesh. Compute total walkable area `A_canonical` (sum of all polygon areas).
2. Load candidate configuration. Export navmesh. Compute total walkable area `A_candidate`.
3. Compute `area_diff_pct` = abs(A_candidate - A_canonical) / A_canonical * 100.

**Threshold:** `area_diff_pct` < 0.1%

**Note:** The 0.1% tolerance accounts for floating-point rounding in navmesh baking, not intentional changes. Any intentional change to walkable area would produce errors far exceeding this threshold.

**Failure Mode:** Navmesh changes break NPC pathing, accessibility, and collision expectations. Discard immediately.

---

### 3.10 CT-10: PHYSICS_TRUTH

**Purpose:** Verify that physics material properties are unchanged.

**Procedure:**
1. Load candidate configuration.
2. Export all physics material properties from the material table:
   - Static friction coefficient
   - Dynamic friction coefficient
   - Restitution (bounciness)
   - Density
   - Drag coefficients
3. Compare each value against the canonical reference table.
4. `property_diff` = count of values that differ from canonical (exact floating-point match required).

**Canonical Material Count:** All materials registered in the physics material table (expected: 30-50 materials).

**Threshold:** `property_diff` = 0

**Note:** AlphaEvolve may tune behavioral parameters that *use* physics materials (e.g., `traction_wet_multiplier` W-02) but may never alter the underlying material table itself. W-02 is a simulation-layer multiplier applied on top of the physics truth.

**Failure Mode:** Physics material changes break determinism and violate the illegal-targets contract. Discard immediately.

---

## 4. Allowed Parameter Bounds

All candidates must have parameter values within the bounds declared in the **Evolvable Parameter Registry v0** (Part 5, Deliverable 1). The constraint test suite verifier performs a bounds check before running any tests:

```python
def bounds_check(candidate_config, registry):
    """
    Pre-test validation: ensure all parameters are within declared bounds.
    Returns True if all parameters are in bounds, False otherwise.
    """
    for param_id, value in candidate_config.items():
        entry = registry.get(param_id)
        if entry is None:
            # Unknown parameter: candidate is modifying something not in the registry
            return False
        if value < entry.min or value > entry.max:
            return False
    return True
```

### 4.1 Rate Limit Rule

**No variable may change more than 20% per generation.**

This prevents catastrophic jumps that could pass constraint tests in isolation but produce emergent failures in combination.

```python
def rate_limit_check(candidate_config, parent_config):
    """
    Verify no parameter changed by more than 20% from parent.
    """
    for param_id, new_value in candidate_config.items():
        old_value = parent_config[param_id]
        if old_value == 0:
            max_delta = 0.2 * registry[param_id].max
        else:
            max_delta = 0.2 * abs(old_value)
        if abs(new_value - old_value) > max_delta:
            return False
    return True
```

**Rationale:** A 20% per-generation limit means it takes at least 5 generations to double any parameter. This gives the constraint suite and scoring function time to catch emerging problems before they compound.

---

## 5. Rollback Policy

### 5.1 Automatic Rollback Triggers

- Any generation in which **all** candidates are discarded triggers automatic rollback.
- Any generation in which the best surviving candidate scores lower than the previous generation's worst surviving candidate triggers automatic rollback.

### 5.2 Rollback Procedure

1. **Revert** the active configuration to the last passing generation's canonical config.
2. **Verify** the restored config by running the full constraint suite (CT-01 through CT-10).
3. **Log** the rollback event:

```json
{
  "event": "ROLLBACK",
  "timestamp": "2026-01-27T15:45:00Z",
  "from_generation": 23,
  "to_generation": 22,
  "reason": "All candidates in gen23 failed CT-03 (SEED_STABILITY)",
  "verification_result": "ALL_PASS",
  "operator_notified": true
}
```

4. **Resume** evolution from the restored generation, with a fresh population seeded from the restored config.

### 5.3 Archive Policy

- **Archive depth:** Last 5 passing canonical configs are retained.
- **Tagging format:** Each archived config is tagged with:

```json
{
  "generation": 22,
  "timestamp": "2026-01-27T14:30:00Z",
  "overall_score": 0.83,
  "config_hash": "b4e2a1f9c83d...",
  "constraint_results": "ALL_PASS",
  "registry_version": "0.1.0"
}
```

- **Retention:** Archived configs are immutable once written. They may be read for rollback or analysis but never modified.
- **Storage location:** `configs/archive/gen{N}_canonical.json`

### 5.4 Emergency Stop

If three consecutive rollbacks occur, the evolutionary loop halts automatically and notifies the operator. Manual investigation is required before resuming.

```
IF consecutive_rollbacks >= 3:
    HALT evolution
    NOTIFY operator with full diagnostic report
    REQUIRE manual approval to resume
```

---

## 6. Test Execution Order

Tests are executed in a fixed order designed to fail fast on the cheapest checks:

1. **Bounds check** (no simulation required)
2. **Rate limit check** (no simulation required)
3. **CT-10: PHYSICS_TRUTH** (data comparison only)
4. **CT-06: STREET_TOPOLOGY** (hash comparison only)
5. **CT-09: NAV_INTEGRITY** (navmesh area comparison)
6. **CT-05: SCALE_CHECK** (distance measurement)
7. **CT-01: ANCHOR_DRIFT** (requires short sim run)
8. **CT-07: ENTITY_IDENTITY** (requires sim run)
9. **CT-02: COLLISION_WALK** (requires 10 path tests)
10. **CT-03: SEED_STABILITY** (requires 2 full sim runs)
11. **CT-04: LEDGER_REPLAY** (requires sim + replay)
12. **CT-08: EVIDENCE_FIDELITY** (requires specific scenario)

**Early termination:** If any test fails, all subsequent tests are skipped and the candidate is immediately discarded. This minimizes wasted compute.

---

## 7. Test Result Schema

Every test execution produces a structured result record:

```json
{
  "suite_version": "0.1.0",
  "candidate_id": "gen47_candidate_03",
  "generation": 47,
  "timestamp": "2026-01-27T14:32:15Z",
  "registry_version": "0.1.0",
  "bounds_check": "PASS",
  "rate_limit_check": "PASS",
  "tests": [
    {
      "test_id": "CT-01",
      "name": "ANCHOR_DRIFT",
      "metric": "max_error_m",
      "value": 0.003,
      "threshold": 1.0,
      "operator": "<",
      "result": "PASS",
      "duration_sec": 12.4
    },
    {
      "test_id": "CT-02",
      "name": "COLLISION_WALK",
      "metric": "snag_count",
      "value": 0,
      "threshold": 0,
      "operator": "=",
      "result": "PASS",
      "duration_sec": 45.2
    }
  ],
  "overall_result": "PASS",
  "total_duration_sec": 312.7,
  "early_termination": false,
  "terminated_at": null
}
```

---

*End of Constraint Test Suite v0.*
