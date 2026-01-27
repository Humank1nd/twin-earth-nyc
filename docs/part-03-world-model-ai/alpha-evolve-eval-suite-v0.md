# AlphaEvolve Eval Suite v0 — Automated Evolution & Safety Rails

> **Series:** Twin Earth NYC — Part 3: World Model & AI
> **Document:** `alpha-evolve-eval-suite-v0.md`
> **Status:** Draft v0
> **Last Updated:** 2026-01-27
> **Depends On:** `proposal-spec-v0.md`, `scenario-library-v0.md`, `fuzz-harness-plan-v0.md`, `canonicalization-checklist.md`, Part 1 (Truth Anchors), Part 2 (Ledger & Evidence)

---

## 1. Overview

AlphaEvolve is the automated parameter optimization system for Twin Earth NYC. It uses evolutionary strategies to tune simulation parameters — improving crowd flow, reducing visual artifacts, optimizing performance, and balancing gameplay systems — while operating under strict safety constraints that prevent it from ever touching the truth layer.

**Core principle:** AlphaEvolve can tune the knobs. It cannot move the walls.

This document defines:
1. Which components AlphaEvolve may evolve (and which are locked).
2. Ten automated evaluation tests with quantitative targets.
3. Safety rails that prevent truth corruption.
4. Rollback policy for recovering from failed evolutions.

---

## 2. Evolvable vs. Locked Components

### 2.1 Evolvable Components

These are simulation parameters that AlphaEvolve may modify within defined bounds. They affect *how* the simulation behaves, not *what* the simulation is.

| # | Component | Parameter Group | Bounds | Default | Effect |
|---|-----------|----------------|--------|---------|--------|
| 1 | **LOD Thresholds** | `lod.transition_distances` | Near: 5-25m, Mid: 20-80m, Far: 50-200m | 15/50/150 | Controls when assets switch detail levels. Lower = higher quality but more expensive. Higher = better performance but visible transitions. |
| 2 | **Crowd Speed** | `crowd.agent_speed` | 0.8 - 2.0 m/s | 1.4 m/s | Walking speed of pedestrian NPCs. Affects flow rates, crossing times, and perceived realism. |
| 3 | **Crowd Spacing** | `crowd.min_spacing` | 0.3 - 1.5 m | 0.6 m | Minimum distance between NPCs. Lower = denser crowds, more collision checks. Higher = sparser, more performant. |
| 4 | **Crowd Lane Strength** | `crowd.lane_formation_weight` | 0.0 - 1.0 | 0.5 | How strongly NPCs form directional lanes on sidewalks. 0 = random, 1 = strict lanes. |
| 5 | **Traffic Light Timing** | `traffic.signal_timing` | Green: 15-60s, Yellow: 3-6s, All-red: 1-4s | 30/4/2 | Duration of traffic signal phases at each intersection. Affects throughput and congestion. |
| 6 | **Anomaly Propagation Rules** | `anomaly.propagation` | Speed: 0.1-5.0 m/s, Decay: 0.01-0.5/s, Max radius: 5-50m | 1.0/0.1/20 | How fast anomaly effects spread, how quickly they fade, and their maximum extent. |
| 7 | **Drift Correction Thresholds** | `drift.correction_threshold` | 0.01 - 1.0 m | 0.1 m | How much an entity can drift from its canonical position before correction snaps it back. Lower = stricter, more corrections. Higher = smoother but less accurate. |
| 8 | **Caching/Streaming Policies** | `streaming.cache_policy` | Preload radius: 50-300m, Unload hysteresis: 10-50m, Priority weights per tier | 150/30/[1.0,0.5,0.2] | How aggressively the streaming system preloads and caches assets. Affects memory usage and pop-in. |
| 9 | **Billboard Activation Distances** | `billboard.activation_distance` | Emissive on: 50-300m, Animation on: 20-150m, Full resolution: 10-80m | 200/100/40 | At what distance billboards switch from static to animated to full-resolution emissive content. Affects GPU load. |
| 10 | **Weather Effect Intensities** | `weather.effect_intensity` | Particle density: 0.1-1.0, Surface wetness: 0.0-1.0, Fog density: 0.0-0.5, Wind strength: 0.0-1.0 | 0.7/0.8/0.1/0.3 | Visual intensity of weather effects. Higher = more immersive but more expensive. |

#### Parameter Genome

Each generation of AlphaEvolve produces a **genome** — a complete set of all evolvable parameters:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://twin-earth-nyc.dev/schemas/alpha-evolve/genome-v0.json",
  "title": "AlphaEvolveGenome",
  "type": "object",
  "required": ["genome_id", "generation", "parent_ids", "parameters", "created_at"],
  "properties": {
    "genome_id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique identifier for this genome."
    },
    "generation": {
      "type": "integer",
      "minimum": 0,
      "description": "Evolution generation number. 0 = initial hand-tuned values."
    },
    "parent_ids": {
      "type": "array",
      "items": { "type": "string", "format": "uuid" },
      "description": "Genome IDs of parent(s). Empty for generation 0."
    },
    "parameters": {
      "type": "object",
      "properties": {
        "lod": {
          "type": "object",
          "properties": {
            "near_distance": { "type": "number", "minimum": 5, "maximum": 25 },
            "mid_distance": { "type": "number", "minimum": 20, "maximum": 80 },
            "far_distance": { "type": "number", "minimum": 50, "maximum": 200 }
          }
        },
        "crowd": {
          "type": "object",
          "properties": {
            "agent_speed": { "type": "number", "minimum": 0.8, "maximum": 2.0 },
            "min_spacing": { "type": "number", "minimum": 0.3, "maximum": 1.5 },
            "lane_formation_weight": { "type": "number", "minimum": 0.0, "maximum": 1.0 }
          }
        },
        "traffic": {
          "type": "object",
          "properties": {
            "green_duration": { "type": "number", "minimum": 15, "maximum": 60 },
            "yellow_duration": { "type": "number", "minimum": 3, "maximum": 6 },
            "all_red_duration": { "type": "number", "minimum": 1, "maximum": 4 }
          }
        },
        "anomaly": {
          "type": "object",
          "properties": {
            "propagation_speed": { "type": "number", "minimum": 0.1, "maximum": 5.0 },
            "decay_rate": { "type": "number", "minimum": 0.01, "maximum": 0.5 },
            "max_radius": { "type": "number", "minimum": 5, "maximum": 50 }
          }
        },
        "drift": {
          "type": "object",
          "properties": {
            "correction_threshold": { "type": "number", "minimum": 0.01, "maximum": 1.0 }
          }
        },
        "streaming": {
          "type": "object",
          "properties": {
            "preload_radius": { "type": "number", "minimum": 50, "maximum": 300 },
            "unload_hysteresis": { "type": "number", "minimum": 10, "maximum": 50 },
            "tier_priority_weights": {
              "type": "array",
              "items": { "type": "number", "minimum": 0, "maximum": 1 },
              "minItems": 3,
              "maxItems": 3
            }
          }
        },
        "billboard": {
          "type": "object",
          "properties": {
            "emissive_on_distance": { "type": "number", "minimum": 50, "maximum": 300 },
            "animation_on_distance": { "type": "number", "minimum": 20, "maximum": 150 },
            "full_res_distance": { "type": "number", "minimum": 10, "maximum": 80 }
          }
        },
        "weather": {
          "type": "object",
          "properties": {
            "particle_density": { "type": "number", "minimum": 0.1, "maximum": 1.0 },
            "surface_wetness": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
            "fog_density": { "type": "number", "minimum": 0.0, "maximum": 0.5 },
            "wind_strength": { "type": "number", "minimum": 0.0, "maximum": 1.0 }
          }
        }
      }
    },
    "created_at": {
      "type": "string",
      "format": "date-time"
    },
    "fitness_scores": {
      "type": "object",
      "description": "Scores from evaluation tests. Populated after evaluation.",
      "additionalProperties": { "type": "number" }
    },
    "passed_hard_constraints": {
      "type": "boolean",
      "description": "Whether all hard constraints passed."
    },
    "status": {
      "type": "string",
      "enum": ["pending", "evaluating", "passed", "failed", "active", "archived"],
      "description": "Current lifecycle status of this genome."
    }
  }
}
```

### 2.2 Locked Components (Non-Evolvable)

These components are **permanently locked**. AlphaEvolve has no read-write access to them. Any attempt to modify these values is blocked at the API level and logged as a safety violation.

| # | Locked Component | Why It Is Locked | Enforcement |
|---|-----------------|------------------|-------------|
| 1 | **Scale Anchors** | Scale anchors define the real-world measurement references (door heights, human proportions, vehicle sizes). Moving them invalidates every scale check in the pipeline. | API rejects writes to `truth.scale_anchors`. Hash verified at boot. |
| 2 | **Georeferenced Coordinates** | Latitude, longitude, and altitude of every canonical entity are surveyed truth data. Changing them breaks the "Twin Earth" premise. | API rejects writes to `truth.coordinates`. Ledger entries are immutable. |
| 3 | **Collision Truth** | Collision meshes define walkable surfaces, barriers, and physics boundaries. They are hand-verified through the canonicalization checklist. | API rejects writes to `truth.collision`. Collision mesh hashes verified at load. |
| 4 | **Street Layout** | Road geometry, sidewalk boundaries, intersection shapes, and lane markings are georeferenced truth. | API rejects writes to `truth.streets`. Street mesh hash verified at boot. |
| 5 | **Entity Identity** | Every canonical entity has a permanent ledger ID. Identities cannot be created, merged, split, or destroyed by automated systems. | Ledger service rejects unauthorized identity operations. Audit log on all attempts. |
| 6 | **Ledger History** | The event ledger is append-only. Past entries cannot be modified, reordered, or deleted. | Ledger service enforces append-only with hash chain. Read-only access for AlphaEvolve. |

#### Enforcement Architecture

```
+------------------+        +------------------+        +------------------+
| AlphaEvolve      |------->| Parameter API    |------->| Evolvable Store  |
| (optimizer)      |        | (gatekeeper)     |        | (mutable params) |
+------------------+        +------------------+        +------------------+
                                    |
                                    | BLOCKED
                                    v
                            +------------------+
                            | Truth Store      |
                            | (immutable)      |
                            | - Anchors        |
                            | - Coordinates    |
                            | - Collision      |
                            | - Streets        |
                            | - Entity IDs     |
                            | - Ledger History |
                            +------------------+
```

The Parameter API maintains a whitelist of writable keys. Any key not on the whitelist is rejected with error code `SAFETY_VIOLATION_LOCKED_COMPONENT`. All rejected attempts are logged with the requesting genome ID, timestamp, and attempted key.

---

## 3. Ten Automated Evaluation Tests

Each test runs against a genome configuration using the scenario runner (see `scenario-library-v0.md`). Tests produce a pass/fail result plus a continuous fitness score (0.0 - 1.0) for optimization.

---

### Test 01: Reduce Crowd Deadlocks

| Field | Value |
|-------|-------|
| **Target** | < 0.1% of NPCs deadlocked at any sample point |
| **Hard Constraint** | Rate must be below 0.1%. Failure = genome rejected. |
| **Fitness Function** | `fitness = 1.0 - (deadlock_rate * 1000)` (clamped 0-1). Lower deadlocks = higher fitness. |
| **Scenario** | Baseline Midday + Rainstorm (shelter-seeking creates chokepoints) |
| **Parameters Tested** | `crowd.min_spacing`, `crowd.lane_formation_weight`, `crowd.agent_speed` |
| **Measurement** | Sample every 5 seconds. Count NPCs with zero movement for > 10s who have active navigation goals. Divide by total NPCs. |
| **Example** | 4200 NPCs total, 3 deadlocked = 0.071% = PASS (fitness: 0.929) |

---

### Test 02: Reduce Visual Pop-In

| Field | Value |
|-------|-------|
| **Target** | 0 obvious pop-in events per standardized walk route |
| **Hard Constraint** | 0 "obvious" pops (defined as: LOD jump visible to a frame-diff algorithm with threshold > 0.15 SSIM delta in a 200x200 pixel region). |
| **Fitness Function** | `fitness = 1.0 - (pop_count / 10.0)` (clamped 0-1). 0 pops = perfect. 10+ pops = zero fitness. |
| **Scenario** | Baseline Midday, automated camera following the standardized walk route (TKTS to 47th via 7th Ave, return via Broadway). |
| **Parameters Tested** | `lod.transition_distances`, `streaming.preload_radius`, `streaming.unload_hysteresis`, `streaming.tier_priority_weights` |
| **Measurement** | Frame-by-frame SSIM comparison. Flag frames where any 200x200 region changes by > 0.15 SSIM in a single frame, not caused by camera movement or entity animation. |
| **Example** | Walk route completed, 0 flagged frames = PASS (fitness: 1.0) |

---

### Test 03: Increase NPC Path Success Rate

| Field | Value |
|-------|-------|
| **Target** | > 99% of NPC navigation attempts succeed |
| **Hard Constraint** | Rate must exceed 99%. Below 99% = genome rejected. |
| **Fitness Function** | `fitness = (success_rate - 0.99) * 100` (clamped 0-1). 99% = 0.0, 100% = 1.0. |
| **Scenario** | Baseline Midday + Construction Closure (forces rerouting) |
| **Parameters Tested** | `crowd.min_spacing`, `crowd.lane_formation_weight`, `drift.correction_threshold` |
| **Measurement** | Track every NPC navigation request. Count successes (NPC reaches destination or valid intermediate waypoint within timeout). Count failures (NPC gives up, times out, or gets stuck). |
| **Example** | 12,000 navigation attempts, 11,976 succeed = 99.8% = PASS (fitness: 0.80) |

---

### Test 04: Preserve Landmark Invariants

| Field | Value |
|-------|-------|
| **Target** | 0 landmark invariant violations |
| **Hard Constraint** | Any violation = genome immediately rejected. Zero tolerance. |
| **Fitness Function** | Binary. 0 violations = 1.0. Any violation = 0.0. |
| **Scenario** | All v1 scenarios (invariants must hold under all conditions) |
| **Parameters Tested** | All evolvable parameters (ensuring none of them indirectly cause invariant violations) |
| **Measurement** | For each landmark (TKTS steps, One Times Square, key intersections): verify position within Tier 1 tolerance (0.05m), verify silhouette matches reference (SSIM > 0.95), verify scale against 3 anchors. |

**Landmark Invariants Checked:**

| Invariant | Check | Tolerance |
|-----------|-------|-----------|
| TKTS steps position | Centroid position vs. canonical | < 0.05m |
| TKTS steps silhouette | SSIM vs. reference from 4 angles | > 0.95 |
| One Times Square position | Base centroid vs. canonical | < 0.05m |
| One Times Square silhouette | SSIM vs. reference from 2 angles | > 0.95 |
| Intersection 7th/45th geometry | Road surface hash | Exact match |
| Intersection 7th/44th geometry | Road surface hash | Exact match |
| Intersection Broadway/45th geometry | Road surface hash | Exact match |
| Street widths | Lane width measurement at 10 points | < 0.1m deviation |
| Sidewalk widths | Width measurement at 10 points | < 0.15m deviation |
| Scale anchor consistency | Door/human/vehicle scale check | < 2% deviation |

---

### Test 05: Maximize FPS Under Stress

| Field | Value |
|-------|-------|
| **Target** | > 30 FPS floor (0% of frames below 30) |
| **Hard Constraint** | No frame may render below 30 FPS during any v1 scenario at severity-adjusted threshold. |
| **Fitness Function** | `fitness = min(1.0, (avg_fps - 30) / 30)` (clamped 0-1). 30fps average = 0.0, 60fps average = 1.0. |
| **Scenario** | All v1 scenarios, with Blackout (#04) as the primary stress target. |
| **Parameters Tested** | `lod.transition_distances`, `billboard.activation_distance`, `weather.particle_density`, `streaming.cache_policy`, `crowd.min_spacing` (affects NPC count) |
| **Measurement** | Per-frame timing across entire scenario run. Report min, mean, p5, p50, p95. Count frames below 30. |
| **Example** | Blackout scenario: mean 38fps, min 31fps, p5 33fps, 0 frames below 30 = PASS (fitness: 0.267) |

---

### Test 06: Minimize Memory Spikes

| Field | Value |
|-------|-------|
| **Target** | < 6 GB peak memory usage |
| **Hard Constraint** | Peak memory must not exceed 6144 MB. Exceeding = genome rejected. |
| **Fitness Function** | `fitness = 1.0 - (peak_memory_mb / 6144)` (clamped 0-1). 0 MB = 1.0 (impossible), 6144 MB = 0.0. Practically, 3-4 GB = good fitness. |
| **Scenario** | All v1 scenarios, with New Year's Eve Density (#14, if available) or Blackout (#04) as primary stress. |
| **Parameters Tested** | `streaming.preload_radius`, `streaming.unload_hysteresis`, `streaming.tier_priority_weights`, `lod.transition_distances`, `billboard.activation_distance` |
| **Measurement** | Sample memory usage every 1 second. Report peak, mean, p95. Identify spike events (> 500 MB increase in < 5 seconds). |
| **Example** | Blackout scenario: peak 5200 MB, mean 4100 MB, p95 4800 MB, 0 spikes > 500 MB = PASS (fitness: 0.154) |

---

### Test 07: Reduce Collision Errors

| Field | Value |
|-------|-------|
| **Target** | < 0.01% collision error rate |
| **Hard Constraint** | Rate must be below 0.01%. Above = genome rejected. |
| **Fitness Function** | `fitness = 1.0 - (error_rate * 10000)` (clamped 0-1). 0% = 1.0, 0.01% = 0.0. |
| **Scenario** | Police Chase (#12) + Fuzz bot session (adversarial interactions stress collision) |
| **Parameters Tested** | `drift.correction_threshold`, `crowd.min_spacing` (affects collision frequency), `crowd.agent_speed` (affects collision velocity) |
| **Measurement** | Count all collision events. Flag errors: penetrations (entity inside another entity's collision volume), fall-throughs (entity below ground plane), incorrect responses (entity bouncing when it should stop, or vice versa). |
| **Example** | 250,000 collision events, 18 errors = 0.0072% = PASS (fitness: 0.28) |

---

### Test 08: Maintain Evidence Generation Rate

| Field | Value |
|-------|-------|
| **Target** | > 1 evidence event per second during active incidents |
| **Hard Constraint** | During any incident window, average evidence rate must exceed 1.0/sec. Below = genome rejected. |
| **Fitness Function** | `fitness = min(1.0, (evidence_rate - 1.0) / 4.0)` (clamped 0-1). 1/sec = 0.0, 5/sec = 1.0. Higher rate = more gameplay data = better. |
| **Scenario** | Anomaly Shimmer (#21) + Police Chase (#12) |
| **Parameters Tested** | `anomaly.propagation_speed`, `anomaly.decay_rate`, `anomaly.max_radius` (affect how much evidence is generated), `crowd.agent_speed` (affects NPC witness rate) |
| **Measurement** | During incident windows (anomaly active, chase in progress), count evidence events: CCTV captures, NPC witness reports, physical trace deposits, player observations. Divide by incident duration in seconds. |
| **Example** | Anomaly shimmer: 180s incident, 420 evidence events = 2.33/sec = PASS (fitness: 0.333) |

---

### Test 09: Preserve Replay Consistency

| Field | Value |
|-------|-------|
| **Target** | Ledger diff = 0 between original run and replay |
| **Hard Constraint** | Any ledger diff = genome rejected. |
| **Fitness Function** | Binary. 0 diffs = 1.0. Any diff = 0.0. |
| **Scenario** | Baseline Midday + Anomaly Shimmer (replayed from seed) |
| **Parameters Tested** | All evolvable parameters (any parameter change that causes nondeterministic ledger behavior is rejected) |
| **Measurement** | Run scenario with genome parameters and seed. Record ledger state. Replay with identical seed and parameters. Diff ledger states. Any entry that differs in content, order, or count is a diff. |

**What constitutes a ledger diff:**

| Diff Type | Description | Severity |
|-----------|-------------|----------|
| **Entry mismatch** | Same event recorded with different data. | Critical — genome rejected. |
| **Order mismatch** | Same events but in different order. | Critical — genome rejected. |
| **Count mismatch** | Different number of events. | Critical — genome rejected. |
| **Timing mismatch** | Same events at different sim-times (> 0.1s delta). | Warning — acceptable if content matches. |

---

### Test 10: Minimize Anchor Drift

| Field | Value |
|-------|-------|
| **Target** | < 0.25m drift for all landmarks |
| **Hard Constraint** | No landmark anchor may drift more than 0.25m from canonical position. Exceeding = genome rejected. |
| **Fitness Function** | `fitness = 1.0 - (max_drift_m / 0.25)` (clamped 0-1). 0m = perfect, 0.25m = zero fitness. |
| **Scenario** | All v1 scenarios (drift can accumulate under stress). Measured at scenario end. |
| **Parameters Tested** | `drift.correction_threshold` (directly controls correction), all other parameters (indirectly — crowd pressure, traffic forces, and anomaly effects can push entities) |
| **Measurement** | At scenario end, measure the distance between each landmark anchor's current position and its canonical position. Report per-anchor drift and maximum drift. |

**Anchor Drift Budget by Tier:**

| Tier | Max Drift | Correction Behavior |
|------|-----------|-------------------|
| Tier 1 (Hero) | 0.05m | Immediate correction. Entity snaps back within 1 frame if displaced. |
| Tier 2 (Mid) | 0.25m | Gradual correction. Entity slides back over 2 seconds. |
| Tier 3 (Skyline) | 1.0m | Periodic correction. Checked every 30 seconds. |

---

### Test Summary Table

| # | Test | Target | Hard? | Primary Parameters | Primary Scenario |
|---|------|--------|-------|--------------------|-----------------|
| 1 | Crowd Deadlocks | < 0.1% | Yes | crowd.* | Baseline + Rainstorm |
| 2 | Visual Pop-In | 0 obvious | Yes | lod.*, streaming.* | Baseline (walk route) |
| 3 | NPC Path Success | > 99% | Yes | crowd.*, drift.* | Baseline + Construction |
| 4 | Landmark Invariants | 0 violations | Yes | All (indirect) | All v1 |
| 5 | FPS Floor | > 30fps | Yes | lod.*, billboard.*, weather.*, streaming.* | Blackout |
| 6 | Memory Ceiling | < 6GB | Yes | streaming.*, lod.*, billboard.* | Blackout |
| 7 | Collision Errors | < 0.01% | Yes | drift.*, crowd.* | Police Chase + Fuzz |
| 8 | Evidence Rate | > 1/sec | Yes | anomaly.*, crowd.* | Anomaly Shimmer |
| 9 | Replay Consistency | diff = 0 | Yes | All | Baseline + Anomaly |
| 10 | Anchor Drift | < 0.25m | Yes | drift.*, all indirect | All v1 |

> **Note:** All 10 tests are hard constraints. A genome must pass every test to be considered viable. This is intentionally strict — we prefer conservative, safe configurations over aggressive optimizations that pass 9 of 10 tests.

---

## 4. Evolution Process

### 4.1 Generation Lifecycle

```
Generation N:
  1. GENERATE: Create K candidate genomes by mutating/crossing from generation N-1.
     - Mutation: Randomly perturb 1-3 parameters within bounds.
     - Crossover: Combine parameters from 2 parent genomes.
     - Elitism: Top 2 genomes from N-1 pass through unchanged.
     - Population size K = 20 per generation.

  2. EVALUATE: Run all 10 tests against each candidate genome.
     - Each genome runs all 5 v1 scenarios.
     - Each scenario produces scores for the relevant tests.
     - Total evaluation time per genome: ~50 minutes sim-time.
     - Parallelizable across 8 sandbox instances = ~2.5 hours per generation wall-clock.

  3. FILTER: Reject any genome that fails any hard constraint.
     - Failed genomes are archived with failure reason.
     - If all genomes fail, revert to last passing generation and reduce mutation rate.

  4. RANK: Score surviving genomes by composite fitness.
     - Composite fitness = weighted average of all 10 test fitness scores.
     - Weights: equal (0.1 each) in v0. Tunable in future versions.

  5. SELECT: Top 5 genomes become parents for generation N+1.
     - Top 1 genome is promoted to "active" status (used in live game).
     - Top 2 genomes pass through as elites to generation N+1.
     - Remaining 3 are used as crossover parents.

  6. ARCHIVE: Store all genomes, scores, and logs for generation N.
     - Last 5 passing generations are retained for rollback.
     - Older passing generations are compressed and archived.
     - Failed generations are retained for 30 days then pruned.
```

### 4.2 Evolution Configuration

```json
{
  "population_size": 20,
  "elite_count": 2,
  "parent_count": 5,
  "mutation_rate": 0.15,
  "mutation_magnitude": 0.1,
  "crossover_rate": 0.3,
  "max_generations": 100,
  "convergence_threshold": 0.001,
  "convergence_window": 10,
  "evaluation_scenarios": [
    "scenario:baseline-midday",
    "scenario:rainstorm",
    "scenario:police-chase",
    "scenario:anomaly-shimmer",
    "scenario:blackout"
  ],
  "fitness_weights": {
    "crowd_deadlocks": 0.10,
    "visual_pop_in": 0.10,
    "npc_path_success": 0.10,
    "landmark_invariants": 0.10,
    "fps_floor": 0.10,
    "memory_ceiling": 0.10,
    "collision_errors": 0.10,
    "evidence_rate": 0.10,
    "replay_consistency": 0.10,
    "anchor_drift": 0.10
  },
  "sandbox_instances": 8,
  "max_evaluation_time_minutes": 60,
  "archive_passing_generations": 5,
  "archive_failed_retention_days": 30
}
```

### 4.3 Mutation Rules

Mutations are bounded to prevent dramatic parameter swings:

| Parameter | Max Mutation Per Generation | Step Resolution |
|-----------|---------------------------|-----------------|
| LOD distances | +/- 10m | 1m |
| Crowd speed | +/- 0.1 m/s | 0.05 m/s |
| Crowd spacing | +/- 0.1m | 0.05m |
| Lane strength | +/- 0.1 | 0.05 |
| Traffic timing | +/- 5s (green), +/- 1s (yellow/red) | 1s |
| Anomaly propagation speed | +/- 0.5 m/s | 0.1 m/s |
| Anomaly decay rate | +/- 0.05/s | 0.01/s |
| Anomaly max radius | +/- 5m | 1m |
| Drift correction | +/- 0.1m | 0.01m |
| Streaming preload | +/- 25m | 5m |
| Streaming hysteresis | +/- 5m | 1m |
| Billboard distances | +/- 20m | 5m |
| Weather particle density | +/- 0.1 | 0.05 |
| Weather surface wetness | +/- 0.1 | 0.05 |
| Weather fog density | +/- 0.05 | 0.01 |
| Weather wind strength | +/- 0.1 | 0.05 |

---

## 5. Safety Rails

### 5.1 Safety Rail Definitions

| # | Safety Rail | Description | Enforcement | Violation Response |
|---|------------|-------------|-------------|-------------------|
| 1 | **Cannot Move Anchors** | No scale anchor, georeference anchor, or landmark anchor may be modified. | API whitelist excludes all `truth.*` keys. | Genome rejected. Violation logged. Alert to safety team. |
| 2 | **Cannot Change Street Layout** | Road geometry, sidewalk boundaries, intersection shapes, lane markings are immutable. | Hash verification of street meshes before and after evaluation. | Genome rejected. Evaluation environment investigated. |
| 3 | **Cannot Reduce Evidence Fidelity Below Threshold** | Evidence generation rate during incidents must stay above 1.0 events/sec. Parameters that would reduce this are rejected. | Test 08 (Evidence Rate) is a hard constraint. | Genome rejected. Parameters that caused reduction are flagged. |
| 4 | **Cannot Modify Committed Ledger Entries** | The ledger is append-only. No past entry may be changed, reordered, or deleted. | Ledger service enforces immutability. AlphaEvolve has read-only ledger access. | If violation detected, entire evolution run is halted. Ledger integrity audit triggered. |
| 5 | **Cannot Exceed Parameter Bounds** | Every evolvable parameter has a hard minimum and maximum. Mutations that exceed bounds are clamped. | Parameter API validates bounds on write. | Value clamped to nearest bound. Warning logged. |
| 6 | **Cannot Run Without Rollback Target** | No new genome can be promoted to active without at least one valid rollback target in the archive. | Promotion blocked if rollback archive is empty. | Promotion deferred until a rollback target exists. |
| 7 | **Cannot Evolve During Live Events** | If a live gameplay event (e.g., anomaly, chase) is in progress, evolution is paused. | Event system signals evolution pause. | Evolution queue holds. Resumes when event concludes. |
| 8 | **Cannot Bypass Human Review for Truth Changes** | If any evaluation detects an unexpected truth-layer change, the genome is quarantined. | Post-evaluation truth hash comparison. | Genome quarantined. Human review required. Evolution paused. |

### 5.2 Safety Violation Logging

Every safety violation is recorded:

```json
{
  "violation_id": "SAF-000001",
  "timestamp": "2026-01-27T14:30:00Z",
  "genome_id": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
  "generation": 15,
  "rail_violated": "cannot_move_anchors",
  "detail": "Genome attempted to write to truth.scale_anchors.door_height. Value rejected by Parameter API.",
  "attempted_key": "truth.scale_anchors.door_height",
  "attempted_value": 2.15,
  "action_taken": "genome_rejected",
  "alert_sent_to": ["safety-team@twin-earth.dev"],
  "investigation_required": true
}
```

### 5.3 Kill Switch

If 3+ safety violations occur within a single generation, or if any violation involves a ledger integrity failure, the entire AlphaEvolve system is halted automatically. Restart requires:

1. Human investigation of all violations.
2. Root cause analysis documented.
3. Fix deployed and verified.
4. Safety team sign-off to restart.

---

## 6. Rollback Policy

### 6.1 Rollback Triggers

| Trigger | Automatic? | Description |
|---------|-----------|-------------|
| **Hard constraint failure on active genome** | Yes | If the currently active genome fails any hard constraint during live monitoring, immediate rollback. |
| **Performance degradation detected** | Yes | If live FPS drops below 25 for > 30 seconds (below the severity-adjusted floor), immediate rollback. |
| **Player-reported regression** | No | If QA or players report a regression traced to a parameter change, manual rollback initiated. |
| **Safety violation** | Yes | Any safety rail violation triggers rollback of the current genome and halt of evolution. |
| **Scheduled regression test failure** | Yes | Nightly regression tests run all 10 eval tests against the active genome. Failure = rollback at next maintenance window. |

### 6.2 Rollback Process

```
1. IDENTIFY: Determine which genome is active and which is the rollback target.
   - Rollback target = most recent genome in archive with status "passed".
   - If no passed genome exists, use generation 0 (hand-tuned defaults).

2. SWAP: Replace active genome with rollback target.
   - Atomic swap via Parameter API.
   - All runtime systems pick up new parameters within 1 frame.
   - No restart required.

3. VERIFY: Run a quick verification suite (abbreviated eval: tests 4, 5, 6, 10 only).
   - If verification passes, rollback is complete.
   - If verification fails, rollback to next-oldest archive entry. Repeat.

4. LOG: Record rollback event.
   - Previous active genome marked as "rolled_back" with reason.
   - Rollback target marked as "active".
   - Alert sent to evolution team.

5. INVESTIGATE: Determine why the rolled-back genome failed.
   - Was it a legitimate regression? Tighten that test.
   - Was it an environmental issue? (e.g., different hardware, network state)
   - Was it a safety violation? Engage safety rail investigation.
```

### 6.3 Archive Retention

| Archive Tier | Count | Description |
|-------------|-------|-------------|
| **Hot Archive** | Last 5 passing genomes | Instantly available for rollback. Stored in-memory and on fast storage. |
| **Warm Archive** | Last 20 passing genomes | Available within 30 seconds. Stored on local disk. |
| **Cold Archive** | All passing genomes ever | Available within 5 minutes. Stored in cloud archive. |
| **Failed Archive** | Last 30 days of failed genomes | For investigation and debugging. Pruned after 30 days. |

### 6.4 Rollback Verification Matrix

After a rollback, the following checks are performed:

| Check | Method | Pass Criteria | Timeout |
|-------|--------|---------------|---------|
| Parameter consistency | Verify all runtime systems reflect rollback genome parameters. | All systems report matching values. | 5 seconds |
| Landmark integrity | Quick anchor drift check on Tier 1 landmarks. | < 0.05m drift. | 10 seconds |
| FPS baseline | Run 60-second Baseline Midday mini-scenario. | > 30 FPS floor. | 90 seconds |
| Memory check | Sample memory during mini-scenario. | < 6 GB peak. | 90 seconds |
| Collision spot-check | Run 10 walk-test paths through key areas. | 0 errors. | 30 seconds |

Total rollback verification time: < 3 minutes.

---

## 7. Reporting & Dashboards

### 7.1 Per-Generation Report

After each generation completes evaluation, a report is generated:

```json
{
  "generation": 15,
  "timestamp": "2026-01-27T16:00:00Z",
  "population_size": 20,
  "passed_count": 12,
  "failed_count": 8,
  "best_genome": {
    "genome_id": "...",
    "composite_fitness": 0.742,
    "test_scores": {
      "crowd_deadlocks": 0.95,
      "visual_pop_in": 1.0,
      "npc_path_success": 0.80,
      "landmark_invariants": 1.0,
      "fps_floor": 0.35,
      "memory_ceiling": 0.22,
      "collision_errors": 0.45,
      "evidence_rate": 0.40,
      "replay_consistency": 1.0,
      "anchor_drift": 0.85
    },
    "promoted_to_active": true
  },
  "worst_passing_genome": {
    "genome_id": "...",
    "composite_fitness": 0.521
  },
  "failure_reasons": {
    "fps_floor": 3,
    "memory_ceiling": 2,
    "collision_errors": 2,
    "landmark_invariants": 1
  },
  "improvement_vs_previous": {
    "composite_fitness_delta": 0.018,
    "improved_tests": ["crowd_deadlocks", "npc_path_success"],
    "regressed_tests": [],
    "unchanged_tests": ["landmark_invariants", "replay_consistency"]
  },
  "safety_violations": 0,
  "wall_clock_duration_hours": 2.3
}
```

### 7.2 Convergence Tracking

AlphaEvolve monitors whether the population is converging (fitness improvements shrinking):

```
Convergence detected when:
  - Best composite fitness improvement < 0.001 for 10 consecutive generations.

On convergence:
  1. Log convergence event with generation number and final fitness.
  2. Archive the converged genome as a "stable baseline."
  3. Option A: Stop evolution. Notify team that current parameters are optimal.
  4. Option B: Increase mutation rate by 2x for 5 generations to explore beyond local optimum.
  5. Option C: Introduce new evaluation scenarios to change the fitness landscape.

Default: Option A (stop and notify). Human decides whether to continue.
```

### 7.3 Fitness History Visualization

The dashboard tracks per-test fitness across generations:

```
Generation:  0    5    10   15   20   25   30
             |    |    |    |    |    |    |
Deadlocks:   0.60 0.75 0.85 0.92 0.95 0.95 0.95  (converged)
Pop-In:      0.40 0.70 0.90 1.00 1.00 1.00 1.00  (converged)
NPC Paths:   0.50 0.60 0.70 0.78 0.80 0.82 0.83  (slow improvement)
Landmarks:   1.00 1.00 1.00 1.00 1.00 1.00 1.00  (always pass)
FPS:         0.10 0.15 0.20 0.28 0.33 0.35 0.35  (converged, low)
Memory:      0.05 0.10 0.15 0.18 0.20 0.22 0.22  (converged, low)
Collisions:  0.20 0.30 0.35 0.40 0.45 0.45 0.45  (converged)
Evidence:    0.30 0.32 0.33 0.35 0.38 0.40 0.40  (slow improvement)
Replay:      1.00 1.00 1.00 1.00 1.00 1.00 1.00  (always pass)
Anchor:      0.70 0.80 0.84 0.85 0.86 0.86 0.86  (converged)

Composite:   0.49 0.57 0.63 0.68 0.70 0.71 0.71  (near convergence)
```

---

## 8. Integration with Other Systems

### 8.1 Scenario Runner Integration

AlphaEvolve uses the scenario runner (defined in `scenario-library-v0.md`) to evaluate genomes. The integration is:

1. AlphaEvolve creates a genome configuration.
2. AlphaEvolve calls `ScenarioRunner.loadBaseline()` to get the canonical world state.
3. AlphaEvolve applies the genome parameters to the world state.
4. AlphaEvolve calls `ScenarioRunner.run()` for each v1 scenario.
5. AlphaEvolve extracts metrics from `ExecutionResult.metrics_summary`.
6. AlphaEvolve scores the genome against the 10 evaluation tests.

### 8.2 Fuzz Harness Integration

The fuzz harness (defined in `fuzz-harness-plan-v0.md`) runs alongside AlphaEvolve evaluation:

- During each genome evaluation, a fuzz bot runs for 10 minutes in the background.
- Any critical or major fuzz findings during evaluation cause the genome to be flagged for review.
- Fuzz findings are correlated with genome parameters to identify which parameter ranges trigger failures.

### 8.3 Proposal System Integration

AlphaEvolve and the proposal system (defined in `proposal-spec-v0.md`) are complementary but separate:

- **Proposals** change *what* exists in the world (add a vendor cart, modify a lighting preset).
- **AlphaEvolve** changes *how* the simulation behaves (crowd speed, LOD distances, traffic timing).
- A proposal may be re-evaluated after AlphaEvolve changes parameters (e.g., a vendor cart placement that was valid at crowd speed 1.4 m/s might cause deadlocks at 1.8 m/s).
- AlphaEvolve does not generate proposals. It only modifies parameters within its authorized bounds.

### 8.4 Canonicalization Integration

AlphaEvolve operates entirely in the **evolvable parameter space** and never interacts with the canonicalization pipeline (defined in `canonicalization-checklist.md`). This separation is enforced by:

- AlphaEvolve has no write access to `/assets/canonical/` or `/assets/suggestive/`.
- AlphaEvolve has no write access to the entity ledger.
- AlphaEvolve cannot create, modify, or delete assets of any kind.
- AlphaEvolve can only read canonical assets (for evaluation) and write to the parameter store.

---

*End of document. End of Part 3 deliverables.*
