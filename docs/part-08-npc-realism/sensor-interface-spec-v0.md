# Sensor Interface Spec v0

**Document:** Part 8 — NPC Realism
**File:** `sensor-interface-spec-v0.md`
**Status:** Draft v0
**Last Updated:** 2026-01-27
**Depends On:** NPC Taxonomy + Tier Plan v0, Part 4 (Slice Architecture)
**Feeds Into:** Curriculum + Reward Spec, Runtime Validation Checklist, Authority Response Spec

---

## 1. Design Principle

> **"Unseen objects aren't known."**

Hero NPCs perceive the world exclusively through simulated sensors. No NPC has access to ground-truth game state. All behavior emerges from sensor observations filtered through noise, occlusion, and limited field of view. This constraint produces believable failures -- NPCs that miss events behind them, react late in fog, and lose track of targets around corners.

---

## 2. Hero Pedestrian Sensors

### 2.1 Forward RGB Camera

| Parameter | Value |
|-----------|-------|
| FOV | 120° horizontal, 80° vertical |
| Range | 50 m (detail degrades linearly beyond 25 m) |
| Resolution | 64 x 64 (training), 128 x 128 (inference, optional high-fidelity mode) |
| Update rate | 10 Hz |
| Noise model | Gaussian, sigma = 0.02 per channel (normalized pixel intensity) |
| Rain modifier | sigma += 0.01 (rain streaks simulated as structured noise) |
| Night modifier | sigma += 0.03 (reduced illumination simulated as increased read noise) |
| Fog modifier | range reduced to 20 m, sigma += 0.02 |
| Occlusion | Ray-traced from NPC eye point; objects block view realistically |
| Mounting | Head height (1.6 m default), follows head orientation with 200°/s slew limit |

### 2.2 Depth Probes (Proximity Sense)

| Parameter | Value |
|-----------|-------|
| Type | 16 radial raycasts from chest height (1.2 m) |
| Angular distribution | Uniform 360° (22.5° spacing) |
| Range | 5 m per ray |
| Update rate | 10 Hz |
| Noise | +/- 5 cm Gaussian per ray |
| Output | 16-element float vector (distance to nearest hit, or max range if no hit) |
| Purpose | Collision avoidance, obstacle detection, crowd proximity awareness |

### 2.3 Audio Proxy (v1 Simplified)

| Parameter | Value |
|-----------|-------|
| Type | Omnidirectional scalar |
| Output | `(loudness_dB: float, direction_bearing: float)` — loudness and bearing to loudest source |
| Range | 30 m (attenuated by inverse-square distance and obstacle occlusion) |
| Obstacle attenuation | -10 dB per solid wall, -3 dB per vehicle, -1 dB per pedestrian cluster |
| Update rate | 5 Hz |
| Noise | Bearing: +/- 15° Gaussian; Loudness: +/- 3 dB Gaussian |
| Purpose | Siren detection, anomaly hum awareness, crowd noise level sensing |

---

## 3. Perception Outputs (Policy Input Vector)

The sensor suite is processed into a structured observation that the RL policy receives each tick.

### 3.1 Occupancy Grid

| Parameter | Value |
|-----------|-------|
| Size | 20 x 20 cells |
| Cell resolution | 0.5 m x 0.5 m |
| Origin | Centered on NPC, aligned to NPC forward direction |
| Cell values | `0` = free, `1` = static obstacle, `2` = dynamic agent, `3` = vehicle, `4` = anomaly zone |
| Update source | Depth probes (near field) + forward camera (far field, forward arc only) |
| Unseen cells | Marked `-1` (unknown) — cells outside FOV or behind occluders |

### 3.2 Visible Agents List

| Field | Type | Description |
|-------|------|-------------|
| `relative_position` | `vec2` (x, z) | Position relative to NPC, in NPC-local coordinates |
| `velocity` | `vec2` (vx, vz) | Estimated velocity of detected agent |
| `class` | `enum` | `pedestrian`, `vehicle`, `cop`, `ems`, `vendor`, `unknown` |
| Max entries | 16 | Nearest 16 agents within FOV; overflow discarded by distance |

### 3.3 Traffic Light State

| Condition | Value |
|-----------|-------|
| Signal in FOV and not occluded | `red`, `green`, `yellow`, `walk`, `dont_walk` |
| Signal out of FOV | `unknown` |
| Signal occluded | `unknown` |
| Artifact query (future) | NPC can "look up" at signal — costs 0.5 s animation, then state becomes known |

### 3.4 Noise Direction

| Field | Type | Description |
|-------|------|-------------|
| `bearing` | `float` (radians) | Direction to loudest audio source, relative to NPC facing |
| `loudness` | `float` (0.0 -- 1.0) | Normalized loudness (0 = ambient, 1 = dangerous/painful) |

### 3.5 Stress Indicators

| Field | Type | Description |
|-------|------|-------------|
| `crowd_density` | `float` (persons/m²) | Local density at NPC position (2 m radius sample) |
| `heat_level` | `float` (0.0 -- 1.0) | Current Heat value at NPC position (from Part 7 Heat grid) |
| `anomaly_proximity` | `float` (meters) | Distance to nearest anomaly boundary; `inf` if none within 100 m |
| `anomaly_bearing` | `float` (radians) | Direction to nearest anomaly, relative to NPC facing; `NaN` if none |

### 3.6 Full Observation Vector Summary

```
observation = {
    occupancy_grid:    float[20][20]     # 400 values
    visible_agents:    float[16][5]      # 80 values (x, z, vx, vz, class_id)
    traffic_signal:    int[1]            # 1 value (encoded state)
    noise_direction:   float[2]          # 2 values (bearing, loudness)
    stress_indicators: float[4]          # 4 values (density, heat, anomaly_dist, anomaly_bearing)
    self_velocity:     float[2]          # 2 values (vx, vz in local frame)
    self_heading:      float[1]          # 1 value (heading in world frame)
}
# Total: 490 floats
```

---

## 4. Inference Gaps and Memory

### Short-Term Memory (Working Memory)

| Parameter | Value |
|-----------|-------|
| Duration | 30 seconds from last observation |
| Content | Last known position and velocity of tracked agents that leave FOV |
| Decay | After 30 s without re-observation, tracked agent entry is deleted |
| Capacity | 8 tracked agents maximum |

### Long-Term Memory (Habit Memory)

| Parameter | Value |
|-----------|-------|
| Duration | Cross-session (persisted to save file) |
| Content | Location-class associations (e.g., "cop usually near 44th & Broadway") |
| Format | Sparse spatial hash: `(grid_cell) → [(class, frequency, last_seen_session)]` |
| Decay | Entries decay by 10% per session if not reinforced |
| Capacity | 256 entries maximum per hero NPC |

---

## 5. Hero Vehicle Sensors

Applicable to hero driver NPCs (Category 5 in taxonomy).

| Sensor | FOV | Range | Update Rate | Notes |
|--------|-----|-------|-------------|-------|
| Forward camera | 90° H, 60° V | 100 m | 10 Hz | Mounted at windshield height |
| Rear camera | 60° H, 40° V | 30 m | 10 Hz | Rearview mirror proxy |
| Proximity probes | 8 radial raycasts | 3 m | 10 Hz | Bumper-height, parking/lane-change assist |
| Speed / heading | N/A (internal) | N/A | Always known | From vehicle physics state |

Vehicle observation vector follows the same structure as pedestrian but with adjusted grid resolution (1.0 m cells, 30 x 30 grid) and added `self_speed: float[1]`.

---

## 6. Sensor Verification Tests

These tests validate that the sensor interface behaves correctly and that policies degrade gracefully under sensor limitations.

| # | Test Name | Procedure | Expected Outcome |
|---|-----------|-----------|------------------|
| 1 | **Occlusion correctness** | Place a city bus (occluder) between hero NPC and a target event (e.g., anomaly shimmer). Measure NPC reaction. | NPC does **not** react to the hidden event. Reaction begins only when occluder moves or NPC gains line of sight. |
| 2 | **Noise stability** | Inject maximum sensor noise (rain + night: sigma = 0.06) and run 50 navigation episodes. | Policy remains stable: no jitter (heading variance < 15°/s), no freezing (velocity > 0.1 m/s when moving), success rate degrades < 15% vs. clean conditions. |
| 3 | **Low-light degradation** | Remove all light sources except distant ambient. Run 20 crossing events. | NPC reaction time increases by 30--80% compared to daylight. NPC shows hesitation behavior (slower approach to intersections). No crashes or policy failures. |
| 4 | **FOV boundary** | Place event at 125° from NPC forward vector (just outside 120° FOV). | NPC does not react. Rotate NPC 10° toward event — NPC now detects and reacts. |
| 5 | **Memory timeout** | Agent A enters hero NPC FOV, then exits. Wait 25 s — query NPC for Agent A position. Wait 35 s — query again. | At 25 s: NPC reports estimated position (from working memory). At 35 s: NPC reports "unknown" (memory expired). |
| 6 | **Audio bearing accuracy** | Play siren at known bearing. Measure NPC head-turn response bearing. | NPC turns toward siren within +/- 20° of true bearing in > 80% of trials. |

---

## Open Questions

1. Should hero NPCs share perception data (e.g., cop radios position of suspect to other cops)? If so, what is the communication bandwidth and delay model?
2. Is 64 x 64 camera resolution sufficient for signal detection at 40 m, or should we use a foveated rendering approach?
3. Should audio proxy be upgraded to a multi-source model in v2 (top-3 loudest sources with bearings)?

---

*End of document.*
