# Evolvable Parameter Registry v0

**Document:** Twin Earth NYC — Part 5, Deliverable 1
**Status:** v0 Draft
**Last Updated:** 2026-01-27
**Depends On:** Part 1 (World Bible), Part 2 (Simulation Systems), Part 3 (Show Director), Part 4 (Evidence & Ledger)

---

## 1. Scope Statement

> **AlphaEvolve may optimize parameters and procedural rules; it may not invent canonical geography.**

AlphaEvolve operates exclusively within the gaps left open by the design. It tunes constants, adjusts policy thresholds, and selects between pre-approved module variants. It never creates new streets, moves anchor points, rewrites ledger history, or alters the canonical shape of the world. The world's truth is authored by humans; AlphaEvolve makes that truth run well.

---

## 2. Legal and Illegal Targets

### 2.1 Legal Gap Targets (15)

These parameters and rules are explicitly available for evolutionary optimization.

| # | Target | Category | Rationale |
|---|--------|----------|-----------|
| L-01 | LOD distance thresholds | Parameter | Balances visual fidelity against draw-call budget without changing geometry truth. |
| L-02 | Crowd preferred speed distributions | Parameter | Mean and variance of pedestrian walking speed; affects flow realism and deadlock rate. |
| L-03 | Crowd personal space radius | Parameter | Minimum comfortable distance between NPCs; trades density against plausibility. |
| L-04 | Crowd lane attraction strength | Parameter | How strongly pedestrians prefer implicit sidewalk lanes; affects flow patterns. |
| L-05 | Traffic signal cycle lengths | Parameter | Green/yellow/red durations per intersection; affects vehicle throughput and pedestrian wait. |
| L-06 | Vehicle spawn rate | Parameter | Vehicles entering the simulation per minute per entry point; affects traffic density. |
| L-07 | Vehicle braking aggressiveness | Parameter | Deceleration curve when approaching obstacles; affects realism and collision avoidance. |
| L-08 | Show Director LOD swap distances | Parameter | Distance at which the Show Director replaces full actors with simplified proxies. |
| L-09 | Proxy swap thresholds | Parameter | Performance headroom threshold that triggers proxy substitution. |
| L-10 | Billboard video activation radius | Parameter | Distance at which animated billboards begin playback; saves GPU bandwidth. |
| L-11 | Wetness drying rate | Parameter | Speed at which surfaces transition from wet to dry after rain stops. |
| L-12 | Traction curve under rain | Parameter | Friction multiplier as a function of wetness level; affects vehicle and NPC behavior. |
| L-13 | Glare/haze intensity scalars | Parameter | Post-process intensity of environmental glare and atmospheric haze. |
| L-14 | Anomaly bleed radius growth rate | Parameter | How quickly anomaly visual effects expand outward from the source point. |
| L-15 | Portal bandwidth cap curve | Parameter | Data-throughput ceiling governing portal transition fidelity as a function of player distance. |

### 2.2 Illegal Targets (15)

These elements are **permanently locked**. Any candidate that modifies them is automatically discarded.

| # | Target | Category | Rationale |
|---|--------|----------|-----------|
| X-01 | Moving streets | Geography | Street layout is canonical truth; moving them breaks spatial continuity and all dependent systems. |
| X-02 | Changing anchor coordinates | Geography | Anchors are the absolute reference frame for all positioning; altering them invalidates the world. |
| X-03 | Rewriting ledger history | Narrative | The ledger is an append-only record of truth; rewriting it destroys evidence integrity. |
| X-04 | Altering landmark silhouettes | Geography | Landmark shapes are identity-defining; changing them breaks recognition and narrative reference. |
| X-05 | Modifying collision truth meshes | Physics | Collision geometry defines walkable/drivable truth; changes break navigation and physics. |
| X-06 | Changing entity IDs | Identity | Entity IDs are the primary key linking simulation state to ledger records; changing them orphans evidence. |
| X-07 | Overriding physics material table | Physics | Material properties (friction, restitution) are authored truth; overriding them breaks consistency. |
| X-08 | Altering sensor truth parameters | Evidence | Sensor intrinsics (FOV, resolution, noise model) define evidence fidelity; altering them corrupts forensics. |
| X-09 | Changing crosswalk positions | Geography | Crosswalk locations are part of canonical street topology; moving them breaks pedestrian routing truth. |
| X-10 | Modifying curb geometry | Geography | Curb lines define the boundary between sidewalk and street; moving them alters the navigable world. |
| X-11 | Redefining scale anchors | Geography | Scale anchors ensure metric consistency; changing them warps perceived distances. |
| X-12 | Altering time schedule structure | Simulation | The master time schedule (day/night cycle, event timing) is authored narrative; evolution cannot reschedule it. |
| X-13 | Changing evidence schema | Evidence | The evidence data schema is the contract between simulation and investigation tools; changing it breaks replay. |
| X-14 | Modifying faction identity | Narrative | Faction names, allegiances, and identities are authored narrative; evolution cannot rewrite story. |
| X-15 | Bypassing translation gates | Architecture | Translation gates enforce system boundaries; bypassing them breaks modular isolation. |

---

## 3. Gap Categories

AlphaEvolve operates in exactly three categories of gaps. Each category has distinct rules and mutation semantics.

### 3.1 Parameter Gaps (Constants)

Scalar or vector values that control continuous behavior. These are the simplest to evolve: mutate the number, observe the result.

| Example Parameters | Typical Range | Mutation Semantics |
|--------------------|---------------|-------------------|
| Friction scalars | 0.1 -- 1.0 | Jitter by percentage |
| Crowd spacing (personal space radius) | 0.3 -- 2.0 m | Jitter by absolute value |
| Light intensity curves | 0.0 -- 5.0 | Jitter control points |
| Spawn rates (vehicles, NPCs) | 0.0 -- 60.0 /min | Jitter by percentage |
| LOD distance thresholds | 5.0 -- 500.0 m | Jitter by percentage |
| Drying rate | 0.001 -- 0.1 /sec | Jitter by percentage |

**Mutation rule:** A parameter gap may be jittered within its declared `[min, max]` bounds. Out-of-bounds mutations are clamped.

### 3.2 Policy Gaps (If/Then Rules)

Conditional rules that govern system behavior at decision points. Evolution adjusts the thresholds and actions within pre-approved rule templates.

| Example Policy | Template | Evolvable Parts |
|----------------|----------|-----------------|
| When to spawn proxies | `IF fps < T THEN swap_to_proxy(radius=R)` | T (fps threshold), R (proxy radius) |
| When to open police cordons | `IF heat > H AND duration > D THEN open_cordon(radius=R)` | H (heat threshold), D (duration), R (radius) |
| When to escalate Heat responses | `IF incidents > N within W seconds THEN escalate_heat(level=L)` | N (incident count), W (time window), L (target level) |
| When to activate billboard video | `IF player_distance < D THEN activate_video(quality=Q)` | D (distance), Q (quality tier) |
| When to reduce crowd density | `IF fps < T AND crowd_count > C THEN cull_distant(fraction=F)` | T, C, F |

**Mutation rule:** Only the numeric parameters within the template may be evolved. The logical structure of the rule is fixed.

### 3.3 Structural Gaps (Module Selection)

Choices between pre-approved alternative implementations. Evolution selects which module to use in which context.

| Example Decision | Options | Context Variable |
|------------------|---------|-----------------|
| LOD method per zone | `{discrete_lod, continuous_lod, impostor}` | Zone density classification |
| Crowd model in density band | `{agent_based, flow_field, hybrid}` | Pedestrian density (people/m^2) |
| Weather shader variant | `{full_volumetric, simplified_particles, screen_space_only}` | GPU headroom |
| Traffic AI model | `{lane_based, free_flow, scripted_path}` | Intersection complexity |
| Anomaly VFX pipeline | `{compute_shader, particle_system, post_process}` | Anomaly intensity level |

**Mutation rule:** Evolution may select any option from the declared set. It may not add new options.

---

## 4. Evolvable Parameter Table (Full Registry)

Every parameter available to AlphaEvolve is registered below. No parameter may be evolved unless it appears in this table.

### 4.1 Crowd System Parameters

| ID | Variable | Type | Min | Max | Default | Unit | Dependencies |
|----|----------|------|-----|-----|---------|------|-------------|
| C-01 | `crowd_speed_mean` | float | 0.8 | 2.0 | 1.3 | m/s | C-02 (variance must be < 0.5 * mean) |
| C-02 | `crowd_speed_variance` | float | 0.05 | 0.8 | 0.25 | m/s | C-01 (must be < 0.5 * C-01) |
| C-03 | `crowd_personal_space` | float | 0.3 | 2.0 | 0.8 | m | C-04 (lane width must be > 2 * personal_space) |
| C-04 | `crowd_lane_width` | float | 1.0 | 4.0 | 2.0 | m | C-03 (must be > 2 * C-03) |
| C-05 | `crowd_lane_attraction` | float | 0.0 | 1.0 | 0.6 | unitless | None |
| C-06 | `crowd_density_cap` | int | 20 | 200 | 80 | NPCs/zone | SD-01 (if cap > 120, proxy distance must decrease) |
| C-07 | `crowd_avoidance_lookahead` | float | 1.0 | 10.0 | 4.0 | m | None |
| C-08 | `crowd_group_cohesion` | float | 0.0 | 1.0 | 0.5 | unitless | None |

### 4.2 Traffic System Parameters

| ID | Variable | Type | Min | Max | Default | Unit | Dependencies |
|----|----------|------|-----|-----|---------|------|-------------|
| T-01 | `traffic_signal_green` | float | 15.0 | 90.0 | 45.0 | sec | T-02 (green + yellow + red = cycle) |
| T-02 | `traffic_signal_yellow` | float | 3.0 | 8.0 | 5.0 | sec | T-01 |
| T-03 | `traffic_signal_red` | float | 15.0 | 90.0 | 45.0 | sec | T-01 |
| T-04 | `vehicle_spawn_rate` | float | 0.5 | 30.0 | 8.0 | veh/min/entry | T-05 (if spawn > 20, braking must be > 0.6) |
| T-05 | `vehicle_braking_aggression` | float | 0.1 | 1.0 | 0.5 | unitless | T-04, W-02 (increases with wetness) |
| T-06 | `vehicle_follow_distance` | float | 2.0 | 15.0 | 5.0 | m | T-05 (must be > 3.0 if braking < 0.4) |
| T-07 | `vehicle_lane_change_threshold` | float | 0.1 | 1.0 | 0.4 | unitless | None |

### 4.3 Show Director Parameters

| ID | Variable | Type | Min | Max | Default | Unit | Dependencies |
|----|----------|------|-----|-----|---------|------|-------------|
| SD-01 | `sd_proxy_swap_distance` | float | 10.0 | 200.0 | 60.0 | m | C-06 (if crowd cap > 120, must decrease to < 40) |
| SD-02 | `sd_lod_near` | float | 5.0 | 50.0 | 15.0 | m | SD-03 (must be < SD-03) |
| SD-03 | `sd_lod_mid` | float | 20.0 | 150.0 | 50.0 | m | SD-02, SD-04 (SD-02 < SD-03 < SD-04) |
| SD-04 | `sd_lod_far` | float | 50.0 | 500.0 | 150.0 | m | SD-03 (must be > SD-03) |
| SD-05 | `sd_performance_headroom_target` | float | 0.1 | 0.5 | 0.25 | fraction | None |
| SD-06 | `sd_proxy_swap_hysteresis` | float | 1.0 | 20.0 | 5.0 | m | SD-01 (must be < 0.3 * SD-01) |

### 4.4 Weather and Materials Parameters

| ID | Variable | Type | Min | Max | Default | Unit | Dependencies |
|----|----------|------|-----|-----|---------|------|-------------|
| W-01 | `wetness_drying_rate` | float | 0.001 | 0.1 | 0.02 | /sec | W-02 (traction must decrease while wetness > 0.3) |
| W-02 | `traction_wet_multiplier` | float | 0.3 | 0.9 | 0.6 | unitless | W-01, T-05 (vehicle braking must increase proportionally) |
| W-03 | `glare_intensity` | float | 0.0 | 3.0 | 1.0 | unitless | W-04 (if glare > 2.0, haze must be > 0.5) |
| W-04 | `haze_intensity` | float | 0.0 | 2.0 | 0.5 | unitless | W-03 |
| W-05 | `rain_particle_density` | float | 100.0 | 10000.0 | 3000.0 | particles/m^3 | W-02 (if density > 7000, traction must be < 0.5) |
| W-06 | `puddle_formation_rate` | float | 0.001 | 0.05 | 0.01 | /sec | W-01 (must be < drying_rate * 3) |

### 4.5 Anomaly System Parameters

| ID | Variable | Type | Min | Max | Default | Unit | Dependencies |
|----|----------|------|-----|-----|---------|------|-------------|
| A-01 | `anomaly_bleed_radius_growth` | float | 0.1 | 5.0 | 1.0 | m/sec | A-02 (portal bandwidth must scale with bleed radius) |
| A-02 | `portal_bandwidth_cap` | float | 10.0 | 1000.0 | 200.0 | MB/s | A-01 |
| A-03 | `anomaly_visual_intensity` | float | 0.1 | 2.0 | 0.8 | unitless | None |
| A-04 | `anomaly_evidence_gen_rate` | float | 0.1 | 5.0 | 1.0 | events/sec | A-01 (must increase when bleed radius > 3.0) |

### 4.6 Billboard and Activation Parameters

| ID | Variable | Type | Min | Max | Default | Unit | Dependencies |
|----|----------|------|-----|-----|---------|------|-------------|
| B-01 | `billboard_activation_radius` | float | 10.0 | 200.0 | 80.0 | m | B-02 (if count_in_view > 5, resolution must scale down) |
| B-02 | `billboard_resolution_scale` | float | 0.25 | 1.0 | 0.75 | fraction | B-01 |

---

## 5. Candidate Bundles

Three pre-defined bundles establish the initial population spread. Each represents a different optimization philosophy.

### 5.1 Bundle A — Performance-First

Prioritizes frame rate and memory headroom. Sacrifices visual density and weather complexity.

| Parameter | Bundle A Value | vs Default |
|-----------|---------------|------------|
| `crowd_density_cap` (C-06) | 40 | -50% |
| `crowd_personal_space` (C-03) | 1.2 | +50% |
| `sd_proxy_swap_distance` (SD-01) | 30.0 | -50% |
| `sd_lod_near` (SD-02) | 10.0 | -33% |
| `sd_lod_mid` (SD-03) | 30.0 | -40% |
| `sd_lod_far` (SD-04) | 80.0 | -47% |
| `rain_particle_density` (W-05) | 1000.0 | -67% |
| `billboard_activation_radius` (B-01) | 40.0 | -50% |
| `billboard_resolution_scale` (B-02) | 0.5 | -33% |
| `anomaly_visual_intensity` (A-03) | 0.5 | -38% |
| `vehicle_spawn_rate` (T-04) | 4.0 | -50% |
| All others | Default | -- |

**Expected profile:** High FPS, low memory pressure, visually sparse, fast LOD transitions. Risk: scenes feel empty.

### 5.2 Bundle B — Plausibility-First

Prioritizes visual richness and behavioral realism. Accepts higher GPU load.

| Parameter | Bundle B Value | vs Default |
|-----------|---------------|------------|
| `crowd_density_cap` (C-06) | 150 | +88% |
| `crowd_personal_space` (C-03) | 0.5 | -38% |
| `sd_proxy_swap_distance` (SD-01) | 35.0 | -42% |
| `sd_lod_near` (SD-02) | 25.0 | +67% |
| `sd_lod_mid` (SD-03) | 80.0 | +60% |
| `sd_lod_far` (SD-04) | 250.0 | +67% |
| `rain_particle_density` (W-05) | 8000.0 | +167% |
| `billboard_activation_radius` (B-01) | 150.0 | +88% |
| `billboard_resolution_scale` (B-02) | 1.0 | +33% |
| `anomaly_visual_intensity` (A-03) | 1.5 | +88% |
| `vehicle_spawn_rate` (T-04) | 15.0 | +88% |
| All others | Default | -- |

**Expected profile:** Rich, dense, immersive scenes. Risk: FPS drops below threshold in stress scenarios. Note: SD-01 reduced to comply with dependency constraint (C-06 > 120 requires SD-01 < 40).

### 5.3 Bundle C — Balanced

Moderate settings intended as the evolutionary midpoint. Most parameters at or near default.

| Parameter | Bundle C Value | vs Default |
|-----------|---------------|------------|
| `crowd_density_cap` (C-06) | 100 | +25% |
| `crowd_personal_space` (C-03) | 0.7 | -13% |
| `sd_proxy_swap_distance` (SD-01) | 50.0 | -17% |
| `sd_lod_near` (SD-02) | 15.0 | 0% |
| `sd_lod_mid` (SD-03) | 50.0 | 0% |
| `sd_lod_far` (SD-04) | 150.0 | 0% |
| `rain_particle_density` (W-05) | 4000.0 | +33% |
| `billboard_activation_radius` (B-01) | 100.0 | +25% |
| `billboard_resolution_scale` (B-02) | 0.75 | 0% |
| `anomaly_visual_intensity` (A-03) | 1.0 | +25% |
| `vehicle_spawn_rate` (T-04) | 10.0 | +25% |
| All others | Default | -- |

**Expected profile:** Reasonable balance of performance and plausibility. Intended as the safe baseline for evolution.

---

## 6. Dependency Constraints

Every dependency listed here is enforced at candidate-generation time (pre-evaluation) and again at validation time (post-evaluation). Violation of any constraint marks the candidate for discard.

### 6.1 Dependency Rules (10)

| Rule | Condition | Required Response | Enforcement |
|------|-----------|-------------------|-------------|
| D-01 | `crowd_density_cap` (C-06) > 120 | `sd_proxy_swap_distance` (SD-01) must be < 40.0 m | Clamp SD-01 at generation; discard if violated at evaluation |
| D-02 | `wetness` > 0.3 (runtime) | `traction_wet_multiplier` (W-02) must be < 0.7 AND `vehicle_braking_aggression` (T-05) must be > 0.5 | Pre-condition check; discard candidate if static params violate under any wetness scenario |
| D-03 | Anomaly `heat_level` > medium (runtime) | `anomaly_evidence_gen_rate` (A-04) must be > 1.5 events/sec | Validate via scenario run; discard if evidence rate drops below threshold during Heat |
| D-04 | Count of active billboards in view > 5 | `billboard_resolution_scale` (B-02) must be < 0.6 | Validate via scenario instrumentation; warn if violated (soft constraint) |
| D-05 | `heat_level` > medium (runtime) | Crowd routing must enable avoidance zones (policy flag must be true) | Validate via scenario; discard if NPCs walk through active danger zones |
| D-06 | `crowd_speed_variance` (C-02) | Must be < 0.5 * `crowd_speed_mean` (C-01) | Clamp at generation time |
| D-07 | `crowd_lane_width` (C-04) | Must be > 2 * `crowd_personal_space` (C-03) | Clamp at generation time |
| D-08 | LOD ordering: SD-02 < SD-03 < SD-04 | `sd_lod_near` < `sd_lod_mid` < `sd_lod_far` | Sort and clamp at generation time |
| D-09 | `sd_proxy_swap_hysteresis` (SD-06) | Must be < 0.3 * `sd_proxy_swap_distance` (SD-01) | Clamp at generation time |
| D-10 | `rain_particle_density` (W-05) > 7000 | `traction_wet_multiplier` (W-02) must be < 0.5 | Clamp W-02 at generation time; discard if violated at evaluation |

### 6.2 Dependency Enforcement Order

1. **Generation time (pre-evaluation):** Apply clamping rules D-06, D-07, D-08, D-09 immediately after mutation.
2. **Conditional clamping:** Apply D-01, D-10 based on static parameter values.
3. **Static validation:** Verify D-02 bounds are satisfiable.
4. **Runtime validation (post-evaluation):** Check D-03, D-04, D-05 from scenario telemetry.
5. **Discard:** Any candidate failing any dependency at any stage is discarded.

---

## 7. Registry Versioning

This registry is versioned alongside the canonical config. Every generation references a specific registry version.

| Field | Value |
|-------|-------|
| Registry Version | `0.1.0` |
| Parameter Count | 27 |
| Dependency Count | 10 |
| Legal Targets | 15 |
| Illegal Targets | 15 |
| Gap Categories | 3 |
| Candidate Bundles | 3 |

**Change policy:** Adding a parameter requires a minor version bump. Removing a parameter or changing bounds requires a major version bump and full regression.

---

## Appendix A: Parameter ID Quick Reference

```
C-01  crowd_speed_mean              C-05  crowd_lane_attraction
C-02  crowd_speed_variance          C-06  crowd_density_cap
C-03  crowd_personal_space          C-07  crowd_avoidance_lookahead
C-04  crowd_lane_width              C-08  crowd_group_cohesion

T-01  traffic_signal_green          T-05  vehicle_braking_aggression
T-02  traffic_signal_yellow         T-06  vehicle_follow_distance
T-03  traffic_signal_red            T-07  vehicle_lane_change_threshold
T-04  vehicle_spawn_rate

SD-01 sd_proxy_swap_distance        SD-04 sd_lod_far
SD-02 sd_lod_near                   SD-05 sd_performance_headroom_target
SD-03 sd_lod_mid                    SD-06 sd_proxy_swap_hysteresis

W-01  wetness_drying_rate           W-04  haze_intensity
W-02  traction_wet_multiplier       W-05  rain_particle_density
W-03  glare_intensity               W-06  puddle_formation_rate

A-01  anomaly_bleed_radius_growth   A-03  anomaly_visual_intensity
A-02  portal_bandwidth_cap          A-04  anomaly_evidence_gen_rate

B-01  billboard_activation_radius   B-02  billboard_resolution_scale
```

---

*End of Evolvable Parameter Registry v0.*
