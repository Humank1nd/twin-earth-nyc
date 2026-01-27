# Scenario Evaluation Suite v0

**Document:** Twin Earth NYC — Part 5, Deliverable 3
**Status:** v0 Draft
**Last Updated:** 2026-01-27
**Depends On:** Part 2 (Simulation Systems), Part 3 (Show Director), Evolvable Parameter Registry v0, Constraint Test Suite v0

---

## 1. Purpose

The Scenario Evaluation Suite defines exactly five reproducible scenarios that test candidate configurations across a range of conditions. Each scenario has a fixed seed, fixed initial conditions, fixed duration, and a defined set of metrics. Together they cover: normal operations, adverse weather, high-action incidents, crowd stress, and anomaly system coupling.

No candidate may be scored on fewer than all five scenarios. The overall score is the **minimum** across scenarios, forcing robustness rather than specialization.

---

## 2. Scenario Registry

### 2.1 Master Scenario Table

| # | Scenario ID | Seed | Duration | Time of Day | Weather | Crowd Level | Key Stressor |
|---|-------------|------|----------|-------------|---------|-------------|--------------|
| 1 | BASELINE_MIDDAY | 42 | 10 min | 12:00 PM | Clear | Moderate (60%) | None — baseline conditions |
| 2 | RAINY_NIGHT | 137 | 10 min | 10:00 PM | Rain (heavy) | Reduced (35%) | Weather rendering + reduced visibility |
| 3 | POLICE_PURSUIT | 256 | 5 min | 3:30 PM | Clear | Moderate (55%) | Active chase + evidence generation |
| 4 | CROWD_SURGE | 512 | 5 min | 10:15 PM | Clear | Peak (95%) | Theater let-out + bottleneck stress |
| 5 | ANOMALY_PORTAL | 1024 | 10 min | 2:00 AM | Fog (light) | Low (20%) | Anomaly bleed + portal pocket + system coupling |

---

## 3. Scenario Specifications

### 3.1 Scenario 1: BASELINE_MIDDAY

**Purpose:** Establish performance and plausibility under normal midday conditions. This is the control scenario. Any candidate that fails here is fundamentally broken.

**Configuration:**

| Parameter | Value |
|-----------|-------|
| Seed | 42 |
| Duration | 600 seconds (10 minutes) |
| Start Time | 12:00:00 PM (solar noon) |
| Weather | Clear sky, no precipitation |
| Temperature | 72 F (22 C) |
| Wind | Light breeze, 5 mph NW |
| Crowd Density | Moderate — 60% of zone capacity |
| Traffic Density | Normal weekday midday |
| Active Incidents | None |
| Anomaly Activity | None |

**Initial Conditions:**
- All traffic signals begin at cycle start (green for east-west).
- Crowd distribution follows midday foot-traffic patterns: heavier on Broadway, lighter on side streets.
- All billboard video content active.
- CCTV systems operational at full coverage.
- Show Director in normal mode (no performance interventions active).

**Key Metrics:**
| Metric | Description | Target |
|--------|-------------|--------|
| `avg_fps` | Average frames per second over full run | > 45 |
| `min_fps_1pct` | 1st percentile FPS (worst 1% of frames) | > 30 |
| `max_fps_spike` | Longest single-frame time in ms | < 50 ms |
| `deadlock_count` | NPCs stuck in mutual blocking for > 3 sec | = 0 |
| `collision_errors` | NPCs or vehicles intersecting geometry | = 0 |
| `npc_path_failures` | Navigation requests that returned no path | < 5 |
| `teleport_incidents` | NPCs teleported to resolve stuck state | = 0 |
| `vram_usage_peak` | Peak VRAM consumption | < 5.0 GB |
| `ram_usage_peak` | Peak system RAM consumption | < 8.0 GB |
| `cpu_utilization_avg` | Average CPU utilization across all cores | < 80% |
| `ledger_events` | Total ledger events recorded | > 0 |
| `anchor_drift_max` | Maximum anchor position error at T=end | < 0.5 m |

---

### 3.2 Scenario 2: RAINY_NIGHT

**Purpose:** Stress weather rendering, streaming, and sensor systems under adverse conditions. Night + rain activates the most expensive shader paths and challenges CCTV confidence.

**Configuration:**

| Parameter | Value |
|-----------|-------|
| Seed | 137 |
| Duration | 600 seconds (10 minutes) |
| Start Time | 10:00:00 PM |
| Weather | Heavy rain, continuous, puddles forming |
| Temperature | 48 F (9 C) |
| Wind | Moderate, 15 mph E |
| Crowd Density | Reduced — 35% of zone capacity |
| Traffic Density | Light evening traffic |
| Active Incidents | None |
| Anomaly Activity | None |

**Initial Conditions:**
- Rain begins at T=0 at full intensity.
- Wetness = 0.0 at T=0, accumulates naturally via `puddle_formation_rate` (W-06).
- All street surfaces dry at start; progressively wet.
- Neon and billboard lighting fully active (night scene).
- CCTV systems operational but with degraded confidence due to rain and darkness.
- Vehicle headlights on.
- Reduced NPC spawn rate reflecting late-evening pedestrian patterns.

**Key Metrics:**
| Metric | Description | Target |
|--------|-------------|--------|
| `avg_fps` | Average FPS | > 40 |
| `min_fps_1pct` | 1st percentile FPS | > 25 |
| `streaming_stalls` | Texture/asset streaming stalls > 100 ms | < 3 |
| `cctv_confidence_avg` | Average CCTV detection confidence | > 0.3 |
| `cctv_confidence_min` | Minimum CCTV confidence during run | > 0.1 |
| `rain_render_cost` | GPU time spent on rain particles (ms/frame) | < 4.0 ms |
| `reflection_quality` | Wet surface reflection coherence score | > 0.7 |
| `traction_events` | Vehicle traction-loss events | tracked (no threshold) |
| `vram_usage_peak` | Peak VRAM | < 5.5 GB |
| `wetness_at_end` | Surface wetness level at T=end | 0.5 -- 1.0 (validates drying/accumulation) |
| `ledger_events` | Total ledger events | > 0 |
| `anchor_drift_max` | Max anchor error at T=end | < 0.5 m |

---

### 3.3 Scenario 3: POLICE_PURSUIT

**Purpose:** Stress the evidence generation pipeline, NPC reactive behavior, and Show Director under a high-action incident. The pursuit tests whether the candidate config supports investigation-critical systems.

**Configuration:**

| Parameter | Value |
|-----------|-------|
| Seed | 256 |
| Duration | 300 seconds (5 minutes) |
| Start Time | 3:30:00 PM |
| Weather | Clear sky |
| Temperature | 65 F (18 C) |
| Wind | Calm |
| Crowd Density | Moderate — 55% of zone capacity |
| Traffic Density | Moderate afternoon |
| Active Incidents | Police pursuit triggered at T=15 sec |
| Anomaly Activity | None |

**Initial Conditions:**
- Normal afternoon simulation for the first 15 seconds.
- At T=15s, a pursuit event triggers: suspect NPC begins fleeing south on Broadway from 44th Street.
- Two police NPCs initiate chase from 44th & 7th Ave.
- Pursuit route: south on Broadway, east on 42nd, resolves near 42nd & 7th Ave.
- Bystander NPCs react: avoidance behavior, line-of-sight observation.
- CCTV cameras along route begin priority recording.
- Evidence generation systems fully active.

**Pursuit Event Timeline:**
| Time | Event |
|------|-------|
| T=0s | Simulation begins, normal conditions |
| T=15s | Pursuit trigger: suspect flees south on Broadway |
| T=15-20s | Police NPCs begin pursuit, sirens activate |
| T=20-60s | Active chase through Broadway corridor |
| T=60-90s | Suspect turns east on 42nd Street |
| T=90-150s | Chase continues on 42nd toward 7th Ave |
| T=150-180s | Pursuit resolution (apprehension or escape, seed-determined) |
| T=180-300s | Post-incident: evidence collection, crowd normalization |

**Key Metrics:**
| Metric | Description | Target |
|--------|-------------|--------|
| `avg_fps` | Average FPS | > 40 |
| `min_fps_1pct` | 1st percentile FPS during pursuit | > 25 |
| `pursuit_duration` | Total pursuit time (trigger to resolution) | 60 -- 180 sec |
| `los_breaks` | Line-of-sight breaks between police and suspect | < 10 |
| `evidence_events_total` | Total evidence events during pursuit phase | > 50 |
| `evidence_events_per_sec` | Evidence generation rate during pursuit | > 0.5 |
| `cctv_captures` | CCTV frames capturing suspect | > 20 |
| `witness_observations` | Bystander witness events generated | > 10 |
| `crowd_avoidance_score` | Fraction of bystanders that successfully avoided pursuit path | > 0.8 |
| `npc_path_failures` | Navigation failures during pursuit chaos | < 10 |
| `ledger_commit_count` | Ledger commits during scenario | > 30 |
| `anchor_drift_max` | Max anchor error at T=end | < 0.5 m |

---

### 3.4 Scenario 4: CROWD_SURGE

**Purpose:** Stress crowd simulation at peak density. Theater let-out produces a sudden influx of pedestrians into an already-busy area, testing deadlock prevention, flow management, and the Show Director's density response.

**Configuration:**

| Parameter | Value |
|-----------|-------|
| Seed | 512 |
| Duration | 300 seconds (5 minutes) |
| Start Time | 10:15:00 PM |
| Weather | Clear sky |
| Temperature | 58 F (14 C) |
| Wind | Calm |
| Crowd Density | Peak — 95% of zone capacity after surge |
| Traffic Density | Moderate evening |
| Active Incidents | Theater let-out at T=0 |
| Anomaly Activity | None |

**Initial Conditions:**
- At T=0, 500 theater-goer NPCs begin exiting from three theater entrances on 44th and 45th Streets.
- Exit rate: approximately 100 NPCs per minute per exit for the first 2 minutes, then tapering.
- Existing sidewalk crowd at moderate evening density.
- Combined density reaches zone capacity within 90 seconds.
- Traffic signals operating normally; pedestrian crosswalk demand spikes.

**Surge Event Timeline:**
| Time | Event |
|------|-------|
| T=0s | Theater doors open, NPCs begin exiting |
| T=0-30s | Initial wave of ~150 NPCs joins sidewalk |
| T=30-90s | Peak exit rate, sidewalk density at maximum |
| T=90-120s | Exit rate begins tapering |
| T=120-180s | Crowd dispersal phase, density slowly decreasing |
| T=180-300s | Return toward normal density |

**Key Metrics:**
| Metric | Description | Target |
|--------|-------------|--------|
| `avg_fps` | Average FPS | > 35 |
| `min_fps_1pct` | 1st percentile FPS during peak density | > 20 |
| `deadlock_count` | Mutual-blocking deadlocks lasting > 3 sec | < 3 |
| `deadlock_duration_max` | Longest single deadlock in seconds | < 8 sec |
| `crowd_flow_rate` | Pedestrians passing a measurement line per minute | > 40/min |
| `bottleneck_clearance` | Time from peak density to 70% density | < 180 sec |
| `teleport_incidents` | NPCs teleported to resolve stuck states | < 5 |
| `npc_path_failures` | Navigation failures | < 20 |
| `sd_interventions` | Show Director proxy swaps or culling actions | tracked |
| `vram_usage_peak` | Peak VRAM during crowd peak | < 5.5 GB |
| `ram_usage_peak` | Peak system RAM during crowd peak | < 10.0 GB |
| `ledger_events` | Total ledger events | > 0 |
| `anchor_drift_max` | Max anchor error at T=end | < 0.5 m |

---

### 3.5 Scenario 5: ANOMALY_PORTAL

**Purpose:** Stress the anomaly system, portal transitions, and system coupling under supernatural conditions. This scenario activates the most exotic simulation paths and tests whether the candidate config handles cross-system interactions gracefully.

**Configuration:**

| Parameter | Value |
|-----------|-------|
| Seed | 1024 |
| Duration | 600 seconds (10 minutes) |
| Start Time | 2:00:00 AM |
| Weather | Light fog |
| Temperature | 42 F (6 C) |
| Wind | Still |
| Crowd Density | Low — 20% of zone capacity |
| Traffic Density | Minimal (late night) |
| Active Incidents | Anomaly manifestation at T=30s |
| Anomaly Activity | Full anomaly + portal sequence |

**Initial Conditions:**
- Late-night Times Square. Sparse pedestrian traffic. Occasional taxi.
- Light fog reduces visibility to ~200 m.
- At T=30s, an anomaly manifests at the intersection of 44th St and Broadway.
- Anomaly bleed radius grows according to `anomaly_bleed_radius_growth` (A-01).
- At T=120s, a portal pocket opens, creating a transition zone.
- Portal pocket mission runs from T=120s to T=480s.
- At T=480s, portal closes, anomaly recedes.
- T=480-600s: normalization phase.

**Anomaly Event Timeline:**
| Time | Event |
|------|-------|
| T=0s | Simulation begins, quiet late-night scene |
| T=30s | Anomaly manifests at 44th & Broadway |
| T=30-120s | Bleed radius expands, visual effects intensify |
| T=60s | Heat begins rising; nearby NPCs react |
| T=120s | Portal pocket opens |
| T=120-240s | Portal stabilization phase, peak bandwidth usage |
| T=240-480s | Active portal pocket mission |
| T=480s | Portal closes, anomaly begins receding |
| T=480-540s | Bleed radius shrinks, Heat dissipates |
| T=540-600s | Return to normal, post-anomaly cleanup |

**Key Metrics:**
| Metric | Description | Target |
|--------|-------------|--------|
| `avg_fps` | Average FPS | > 35 |
| `min_fps_1pct` | 1st percentile FPS during portal phase | > 20 |
| `heat_peak` | Maximum Heat level reached | tracked |
| `heat_escalation_time` | Time from anomaly start to peak Heat | tracked |
| `heat_cooldown_time` | Time from portal close to Heat = 0 | tracked |
| `anomaly_evidence_rate` | Evidence events/sec during anomaly phase | > 1.0 |
| `portal_bandwidth_peak` | Peak portal data throughput | < portal_bandwidth_cap (A-02) |
| `bleed_radius_max` | Maximum bleed radius reached | tracked |
| `system_coupling_errors` | Cross-system desync or error events | = 0 |
| `npc_reaction_score` | Fraction of nearby NPCs that reacted appropriately to anomaly | > 0.7 |
| `vram_usage_peak` | Peak VRAM during portal phase | < 5.5 GB |
| `anomaly_vfx_cost` | GPU time for anomaly VFX (ms/frame) | < 6.0 ms |
| `ledger_events` | Total ledger events | > 50 |
| `ledger_commit_count` | Ledger commits during anomaly | > 40 |
| `anchor_drift_max` | Max anchor error at T=end | < 0.5 m |

---

## 4. Instrumentation Specification

Every scenario run captures the following instrumentation data. This data feeds into the Scoring Function (Part 5, Deliverable 4) and is archived for regression analysis.

### 4.1 Performance Telemetry

Captured every frame, aggregated at 1-second intervals.

| Metric | Sample Rate | Aggregation | Storage |
|--------|-------------|-------------|---------|
| Frame time (ms) | Per frame | Min, Max, Avg, P1, P5, P50, P95, P99 per second | Full time series |
| FPS (derived) | Per frame | Avg, 1% low, 0.1% low | Full time series |
| VRAM usage (MB) | Per second | Current, Peak | Full time series |
| RAM usage (MB) | Per second | Current, Peak | Full time series |
| CPU utilization (%) | Per second | Per core, Total | Full time series |
| GPU utilization (%) | Per second | Current | Full time series |
| Draw calls | Per frame | Count | Sampled at 1Hz |
| Triangle count | Per frame | Count | Sampled at 1Hz |

### 4.2 Simulation Telemetry

Captured at event boundaries and sampled at 1-second intervals.

| Metric | Sample Rate | Description |
|--------|-------------|-------------|
| Deadlock count | On event | NPCs mutually blocked > 3 sec |
| Collision errors | On event | NPC/vehicle geometry intersection |
| NPC path failures | On event | Navigation request returned no valid path |
| Teleport incidents | On event | NPC teleported to resolve stuck state |
| Active NPC count | 1 Hz | Total NPCs being simulated |
| Active vehicle count | 1 Hz | Total vehicles being simulated |
| Proxy NPC count | 1 Hz | NPCs currently in proxy representation |
| Show Director actions | On event | Type and timestamp of each SD intervention |

### 4.3 Ledger Telemetry

Captured at commit boundaries.

| Metric | Sample Rate | Description |
|--------|-------------|-------------|
| Events logged (total) | Running count | Cumulative ledger events |
| Commit count | Running count | Number of ledger commits |
| Replay consistency check | At T=end | Quick replay verification (subset) |
| Evidence events by type | Running count | CCTV, witness, physical, radio, tracking |

### 4.4 Anchor Telemetry

Captured at scenario end and at midpoint.

| Metric | Sample Rate | Description |
|--------|-------------|-------------|
| Anchor position samples | T=mid, T=end | All registered anchor positions |
| Max drift | T=end | Maximum Euclidean distance from canonical |
| Mean drift | T=end | Average drift across all anchors |

### 4.5 Capture Requirements

Each scenario run produces the following visual captures for human review.

| Capture Type | Timing | Specification |
|--------------|--------|---------------|
| Video clip (30 sec) | T=0 to T=30 | 1080p, 30fps, from primary camera |
| Video clip (30 sec) | T=midpoint-15 to T=midpoint+15 | 1080p, 30fps, from primary camera |
| Video clip (30 sec) | T=end-30 to T=end | 1080p, 30fps, from primary camera |
| Screenshot | T=60 | Camera Point 1: Times Square overview (aerial) |
| Screenshot | T=60 | Camera Point 2: Broadway street level (north-facing) |
| Screenshot | T=60 | Camera Point 3: 42nd Street corridor (east-facing) |
| Screenshot | T=60 | Camera Point 4: 44th & Broadway intersection (ground level) |
| Screenshot | T=60 | Camera Point 5: CCTV camera #7 view (fixed surveillance angle) |

**Camera Points** are fixed world-space positions and orientations. They do not change between candidates or generations, ensuring visual comparisons are meaningful.

---

## 5. Scoring Integration

### 5.1 Per-Scenario Scoring

Each scenario produces a composite score using the weights defined in the **Scoring Function Spec v0** (Part 5, Deliverable 4):

```
scenario_score = 0.4 * performance_score + 0.3 * plausibility_score + 0.3 * consistency_score
```

### 5.2 Overall Scoring

```
overall_score = MIN(scenario_1_score, scenario_2_score, scenario_3_score, scenario_4_score, scenario_5_score)
```

The minimum-across-scenarios rule prevents a candidate from scoring well by excelling in easy scenarios while failing in hard ones. Every scenario matters equally as a potential bottleneck.

### 5.3 Holdout Scenario

In addition to the five evaluation scenarios, a sixth **holdout scenario** exists for validation only. It is never used during evolutionary scoring.

| Scenario ID | Seed | Duration | Description |
|-------------|------|----------|-------------|
| RANDOM_STRESS | 9999 | 10 min | Random combination of weather, incidents, crowd surges, and anomaly events injected at unpredictable intervals |

The holdout scenario is run only during promotion (candidate moving from sandbox to canonical config). It detects overfitting: a candidate that scores well on the five training scenarios but poorly on the holdout is rejected.

---

## 6. Scenario Run Output Schema

Each completed scenario run produces a structured output:

```json
{
  "scenario_id": "BASELINE_MIDDAY",
  "seed": 42,
  "duration_sec": 600,
  "candidate_id": "gen47_candidate_03",
  "generation": 47,
  "timestamp_start": "2026-01-27T14:32:15Z",
  "timestamp_end": "2026-01-27T14:42:15Z",
  "config_hash": "a7f3c2e9...",
  "performance": {
    "avg_fps": 52.3,
    "min_fps_1pct": 34.7,
    "max_frame_time_ms": 38.2,
    "vram_peak_mb": 4200,
    "ram_peak_mb": 6800,
    "cpu_utilization_avg_pct": 67.2,
    "gpu_utilization_avg_pct": 82.1
  },
  "simulation": {
    "deadlock_count": 0,
    "collision_errors": 0,
    "npc_path_failures": 2,
    "teleport_incidents": 0,
    "active_npc_avg": 312,
    "active_vehicle_avg": 45,
    "proxy_npc_avg": 180,
    "sd_interventions": 12
  },
  "ledger": {
    "events_logged": 1847,
    "commit_count": 92,
    "replay_check": "PASS"
  },
  "anchors": {
    "max_drift_m": 0.003,
    "mean_drift_m": 0.001
  },
  "captures": {
    "video_t0": "captures/gen47_c03_baseline_t0.mp4",
    "video_tmid": "captures/gen47_c03_baseline_tmid.mp4",
    "video_tend": "captures/gen47_c03_baseline_tend.mp4",
    "screenshots": [
      "captures/gen47_c03_baseline_cam1.png",
      "captures/gen47_c03_baseline_cam2.png",
      "captures/gen47_c03_baseline_cam3.png",
      "captures/gen47_c03_baseline_cam4.png",
      "captures/gen47_c03_baseline_cam5.png"
    ]
  },
  "scores": {
    "performance_score": 0.87,
    "plausibility_score": 0.91,
    "consistency_score": 0.95,
    "scenario_composite": 0.906
  }
}
```

---

## 7. Scenario Execution Requirements

### 7.1 Isolation

Each scenario runs in a fresh simulation instance. No state carries over between scenarios. The simulation is fully reset between runs.

### 7.2 Determinism

Given the same seed and the same candidate config, a scenario must produce identical results. This is verified by CT-03 (SEED_STABILITY) in the constraint suite.

### 7.3 Timeout

Each scenario has a wall-clock timeout of **3x its simulation duration**. If the scenario does not complete within the timeout, it is marked as failed with `avg_fps` = 0 and all other metrics at worst-case values.

| Scenario | Sim Duration | Wall-Clock Timeout |
|----------|-------------|-------------------|
| BASELINE_MIDDAY | 10 min | 30 min |
| RAINY_NIGHT | 10 min | 30 min |
| POLICE_PURSUIT | 5 min | 15 min |
| CROWD_SURGE | 5 min | 15 min |
| ANOMALY_PORTAL | 10 min | 30 min |

### 7.4 Resource Limits

All scenario runs execute within the following resource envelope:

| Resource | Limit |
|----------|-------|
| VRAM | 6 GB (hard cap; exceeding triggers OOM failure) |
| System RAM | 12 GB (hard cap) |
| CPU Cores | 8 (matches target platform) |
| GPU | Single GPU (target spec) |
| Disk I/O | No throttling; SSD assumed |

---

*End of Scenario Evaluation Suite v0.*
