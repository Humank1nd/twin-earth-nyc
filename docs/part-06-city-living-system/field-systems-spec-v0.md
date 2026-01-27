# Field Systems Spec v0 — Spatial Fields, Coupling Matrix, and Anti-O(N^2) Rules

> **Series:** Twin Earth NYC — Part 6: City-as-Living-System
> **Document:** `field-systems-spec-v0.md`
> **Status:** Draft v0
> **Last Updated:** 2026-01-27
> **Depends On:** `ontology-spec-v0.md` (entity hierarchy, field overview), Part 4 (geospatial grid alignment)

---

## 1. Governing Principle

> **"Fields are the city's nervous system. They carry information continuously through space so that entities never need to poll each other."**

Every continuous spatial quantity in Twin Earth NYC is modeled as a field: a regular grid of values overlaid on the simulation slice. Fields decouple entities from each other. Instead of NPC A asking NPC B "how loud are you?", NPC A reads the noise field at its own position. This architectural choice eliminates O(N^2) entity-entity queries and replaces them with O(1) field lookups per entity and O(cells) field updates per tick.

This document specifies each field in full: grid parameters, source and sink terms, inter-field coupling, entity coupling, boundary conditions, and debug visualization.

---

## 2. Common Field Infrastructure

All fields share the following infrastructure:

### 2.1 Grid Specification

| Parameter | Value |
|-----------|-------|
| Grid alignment | Axis-aligned with ENU coordinate system (see Part 4 geospatial contract) |
| Grid origin | Southwest corner of simulation slice bounding box |
| Cell indexing | (ix, iy) for 2D fields; (ix, iy, iz) for 3D fields; integer coordinates |
| Coordinate lookup | `cell = floor((world_pos - grid_origin) / cell_size)` |
| Out-of-bounds policy | Clamp to nearest boundary cell (no wrap-around) |
| Storage | Flat array, row-major order; double-buffered (read from front, write to back, swap on tick) |

### 2.2 Update Pipeline (Per Tick)

```
[1. Source Accumulation]   Entities write contributions to back buffer
[2. Diffusion / Decay]    Field-internal propagation (blur, decay, advection)
[3. Inter-Field Coupling]  Read other fields' front buffers; apply coupling rules to back buffer
[4. Boundary Enforcement]  Apply boundary conditions to back buffer edges
[5. Buffer Swap]           Back buffer becomes front buffer; old front buffer cleared for next tick
```

### 2.3 LOD Policy

Fields support level-of-detail based on camera distance:

| Distance from Camera | Resolution Multiplier | Update Rate Multiplier |
|---------------------|----------------------|----------------------|
| 0--50 m | 1x (full resolution) | 1x (full rate) |
| 50--150 m | 2x (half resolution) | 0.5x (half rate) |
| 150--300 m | 4x (quarter resolution) | 0.25x (quarter rate) |
| > 300 m | Frozen (last computed value) | 0x (no updates) |

---

## 3. Wind Field

### 3.1 Parameters

| Property | Value |
|----------|-------|
| Data type | `vec3` (3D direction + magnitude in m/s) |
| Grid resolution | 5 m horizontal, 5 m vertical |
| Grid dimensions (slice) | ~120 x 60 x 20 = 144,000 cells |
| Update frequency | 2 Hz |
| Memory footprint | 144,000 x 12 bytes = ~1.7 MB (double-buffered: 3.4 MB) |

### 3.2 Source Terms

| Source | Contribution Rule | Spatial Extent |
|--------|-------------------|----------------|
| **Weather system** | Base wind vector from City-level weather state; uniform across slice | Global (all cells) |
| **Building geometry** | Static deflection map precomputed from building meshes; applied as multiplicative modifier to base wind | Per-cell (baked at load time, recomputed only on geometry change) |
| **HVAC vents** | Point sources adding 2--5 m/s outward vector within 10 m radius | Radial falloff from vent position |
| **Subway grate updraft** | Vertical vector (0, +3 m/s, 0) applied at grate positions, radius 3 m | Radial falloff from grate center |
| **Anomaly vortex** | Circular wind pattern around anomaly center; magnitude proportional to anomaly intensity (0--15 m/s) | Radius = anomaly_radius x 2; falloff = 1/r |
| **Explosion shockwave** | Radial outward impulse, 30 m/s peak, decays over 0.5 s | Spherical, radius 50 m, 1/r^2 falloff |

### 3.3 Sink / Decay Terms

| Mechanism | Rule |
|-----------|------|
| **Viscous damping** | Each cell decays toward base wind at rate `0.3 / s` (exponential decay) |
| **Building absorption** | Cells inside building volumes are zeroed each tick (no wind indoors in exterior sim) |

### 3.4 Entity Coupling

| Entity Type | Read / Write | Behavior |
|-------------|-------------|----------|
| Paper / cloth props | Read | Animate flutter direction and intensity from local wind vector |
| NPC hair / clothing | Read | Blend animation layers for wind response; hat-blow-off event if wind > 12 m/s |
| Rain particles | Read | Rain angle = wind vector projected onto horizontal plane; streak length proportional to wind speed |
| Sound propagation | Read | Downwind sound carries +3 dB; upwind sound carries -6 dB (simplified Doppler / propagation) |
| Drone entity | Read + Write | Drone reads wind for flight stability; drone rotor writes 5 m/s downwash in 3 m radius below |

### 3.5 Boundary Conditions

| Edge | Condition |
|------|-----------|
| Horizontal slice edges | Inflow: base wind vector applied at upwind edge. Outflow: free advection (values carried out of domain). |
| Vertical floor (street level) | No-slip: wind magnitude reduced to 0.1x within 1 m of ground (boundary layer approximation). |
| Vertical ceiling (top of grid) | Open: values extrapolated from interior (no reflection). |

### 3.6 Debug Visualization

- **Arrow field overlay:** 3D arrows at every other grid cell, color-coded by magnitude (blue = calm, yellow = moderate, red = gust).
- **Streamline mode:** Animated particle traces following wind vectors; 500 tracer particles.
- **Slice view:** Horizontal or vertical cross-section with heatmap of wind magnitude.

---

## 4. Noise Field

### 4.1 Parameters

| Property | Value |
|----------|-------|
| Data type | `float32` (scalar, dB-equivalent, range 0--120) |
| Grid resolution | 2 m horizontal (2D field; height ignored, ground-plane only) |
| Grid dimensions (slice) | ~300 x 150 = 45,000 cells |
| Update frequency | 5 Hz |
| Memory footprint | 45,000 x 4 bytes = ~180 KB (double-buffered: 360 KB) |

### 4.2 Source Terms

| Source | Contribution Rule | Spatial Extent |
|--------|-------------------|----------------|
| **Vehicle engine** | +65--80 dB at source position (varies by vehicle type: bus = 80, taxi = 70, bike = 45) | Point source, 1/r^2 falloff, max range 80 m |
| **Vehicle horn** | +95 dB impulse, 0.5 s duration | Point source, 1/r^2 falloff, max range 120 m |
| **Crowd chatter** | +55 dB per 10 persons/m^2 (read from crowd density field) | Per-cell contribution (density-driven) |
| **Construction** | +90 dB continuous while active | Point source at construction site, 1/r^2 falloff, max range 150 m |
| **Siren** | +105 dB, oscillating pattern | Point source on emergency vehicle, 1/r^2 falloff, max range 200 m |
| **Billboard speakers** | +70 dB while powered | Point source per billboard, directed cone (120-degree forward arc), max range 40 m |
| **Explosion / gunshot** | +130 dB impulse, 0.1 s duration | Point source, 1/r^2 falloff, max range 300 m |
| **Anomaly hum** | +40--80 dB continuous (proportional to anomaly intensity) | Radial from anomaly center, radius = anomaly_radius x 3 |
| **Wind contribution** | +wind_speed x 0.1 dB per cell (from wind field coupling) | Per-cell (read from wind field) |

### 4.3 Sink / Decay Terms

| Mechanism | Rule |
|-----------|------|
| **Distance attenuation** | Applied during source accumulation: contribution = source_dB - 20 x log10(distance / 1m) |
| **Temporal decay** | Each cell decays toward ambient baseline (45 dB for Times Square) at rate 10 dB/s |
| **Building occlusion** | Cells behind buildings (relative to source) receive -20 dB penalty; precomputed occlusion map per source |
| **Material absorption** | Fabric and vegetation cells absorb -3 dB; concrete reflects (no absorption); metal reflects +1 dB |

### 4.4 Entity Coupling

| Entity Type | Read / Write | Behavior |
|-------------|-------------|----------|
| NPC (all types) | Read | Communication range = max(2 m, 20 m - (local_noise - 50) x 0.3 m/dB); if noise > 85 dB, stress += 0.01/s |
| NPC witness | Read | Witness accuracy = base_accuracy x clamp(1.0 - (noise - 60) / 40, 0.3, 1.0) |
| CCTV (audio channel) | Read | Audio evidence quality = clamp(1.0 - (noise - 70) / 30, 0.0, 1.0) |
| Player | Read | Audio mix: ambient noise volume scales with field value at player position |
| Vehicle NPC | Write | Engine noise written at vehicle position each tick |
| Crowd (aggregate) | Write | Density-to-noise contribution computed per cell from crowd density field |

### 4.5 Boundary Conditions

| Edge | Condition |
|------|-----------|
| All horizontal edges | Open: noise propagates out of domain freely. Incoming noise from off-slice sources modeled as fixed ambient (45 dB). |

### 4.6 Debug Visualization

- **Heatmap overlay:** Ground-plane color gradient from green (< 50 dB) to yellow (50--80 dB) to red (> 80 dB).
- **Source highlight:** Ring indicators around active noise sources, radius = audible range.
- **NPC communication circles:** Drawn around selected NPC showing effective communication range.

---

## 5. Light Field

### 5.1 Parameters

| Property | Value |
|----------|-------|
| Data type | `vec4` (RGB color + intensity, each `float16`) |
| Grid resolution | 1 m (near camera, < 50 m), 5 m (far, > 50 m) |
| Grid dimensions (slice) | Near: ~100 x 100 = 10,000 cells; Far: ~120 x 60 = 7,200 cells; Total: ~17,200 cells |
| Height layers | 3 layers (ground, eye-level at 1.7 m, sign-level at 5 m) |
| Effective cells | 17,200 x 3 = 51,600 |
| Update frequency | 10 Hz (near), 2 Hz (far) |
| Memory footprint | 51,600 x 8 bytes = ~413 KB (double-buffered: 826 KB) |

### 5.2 Source Terms

| Source | Contribution Rule | Spatial Extent |
|--------|-------------------|----------------|
| **Sun / sky** | Global directional light; intensity and color from City-level time-of-day + weather (overcast = 0.3x intensity, clear = 1.0x) | All cells; shadow map applied from building geometry |
| **Billboard** | RGB color from billboard content texture sampled at center; intensity = 2000 lux per billboard (powered) or 0 (unpowered) | Directed hemisphere forward from billboard face; 1/r^2 falloff; max range 60 m |
| **Streetlight** | Warm white (3200K mapped to RGB), 500 lux | Downward cone from light position; 1/r^2 falloff; max range 15 m |
| **Vehicle headlight** | White (5500K), 1000 lux per pair | Directed cone (30-degree half-angle), forward from vehicle; max range 40 m |
| **Emergency flasher** | Red/blue alternating at 2 Hz, 800 lux | Omnidirectional from vehicle roof; max range 30 m |
| **Anomaly glow** | Purple-cyan gradient (anomaly signature color), 0--3000 lux proportional to intensity | Radial from anomaly center; radius = anomaly_radius; 1/r falloff |
| **Fire / explosion** | Orange (2000K), 5000 lux peak, decays with event | Radial; max range 50 m |
| **Phone / device screen** | Dim white, 5 lux | Point source at NPC hand position; range 1 m |

### 5.3 Sink / Decay Terms

| Mechanism | Rule |
|-----------|------|
| **Distance attenuation** | 1/r^2 from each source; computed during source accumulation |
| **Shadow occlusion** | Static shadow volumes from buildings; dynamic shadows from large vehicles (bus, truck) computed at 2 Hz |
| **Temporal smoothing** | Light values blend toward new target at rate 5.0/s (prevents popping on sudden source changes) |

### 5.4 Entity Coupling

| Entity Type | Read / Write | Behavior |
|-------------|-------------|----------|
| CCTV camera | Read | Image quality = base_quality x clamp(light_intensity / 200 lux, 0.1, 1.0); below 50 lux: IR mode (reduced color info) |
| NPC perception | Read | NPC visibility range = base_range x clamp(light_intensity / 100 lux, 0.2, 1.5); dark = shorter range |
| NPC mood | Read | Prolonged darkness (< 30 lux for > 60 s) increases anxiety by 0.005/s |
| Forced perspective renderer | Read | Light field feeds into final compositing to ensure rendered geometry matches environmental lighting |
| Billboard entity | Write | Powered billboard writes light contribution at its position |
| Streetlight entity | Write | Powered streetlight writes light contribution |
| Vehicle entity | Write | Headlights and flashers write contributions while active |

### 5.5 Boundary Conditions

| Edge | Condition |
|------|-----------|
| Horizontal edges | Ambient sky light at boundary cells; no off-slice artificial light sources modeled |
| Vertical floor | Ground receives full illumination computation; no sub-surface light |
| Vertical ceiling | Open sky; sun/sky contribution applied directly |

### 5.6 Debug Visualization

- **Luminance heatmap:** Ground-plane overlay, black (0 lux) to white (> 2000 lux), logarithmic scale.
- **Color overlay:** RGB tint on ground showing dominant light color at each cell.
- **Shadow view:** Binary black/white showing shadowed vs. illuminated cells.
- **CCTV quality map:** Overlay showing effective CCTV image quality per cell (red = poor, green = good).

---

## 6. Wetness Field

### 6.1 Parameters

| Property | Value |
|----------|-------|
| Data type | `float32` (scalar, 0.0 = bone dry, 1.0 = saturated) |
| Grid resolution | 1 m (2D ground-plane only) |
| Grid dimensions (slice) | ~600 x 300 = 180,000 cells |
| Update frequency | 1 Hz |
| Memory footprint | 180,000 x 4 bytes = ~720 KB (double-buffered: 1.44 MB) |

### 6.2 Source Terms

| Source | Contribution Rule | Spatial Extent |
|--------|-------------------|----------------|
| **Rain** | `wetness += rain_rate x dt x (1.0 - shade_factor)`; rain_rate from City weather (0.0--1.0); shade_factor from building overhang map (precomputed) | All exposed cells |
| **Fire hydrant burst** | `wetness = 1.0` at hydrant position, spreading radially at 0.5 m/s up to 10 m radius | Radial from hydrant; duration = event length |
| **Sprinkler / cleaning** | `wetness += 0.3` in affected area | Rectangular zone defined by sprinkler coverage |

### 6.3 Sink / Decay Terms

| Mechanism | Rule |
|-----------|------|
| **Evaporation** | `wetness -= evap_rate x dt`; evap_rate = 0.01/s (overcast) to 0.05/s (sunny, warm) from weather state |
| **Drainage** | Cells tagged as drain (storm drains, gutter lines) have 3x evaporation rate |
| **Shade persistence** | Shaded cells (shade_factor > 0.7) have 0.5x evaporation rate (wetness lingers in shade) |
| **Wind drying** | `wetness -= wind_speed x 0.002 / s` (from wind field coupling); strong wind accelerates drying |

### 6.4 Entity Coupling

| Entity Type | Read / Write | Behavior |
|-------------|-------------|----------|
| Vehicle physics | Read | Braking distance = base_distance x (1.0 + 1.5 x wetness); tire traction = base_traction x (1.0 - 0.4 x wetness) |
| NPC locomotion | Read | Slip probability = wetness x 0.02 per step on smooth surfaces (metal, glass); NPC routing preference avoids cells with wetness > 0.6 |
| CCTV confidence | Read | Image confidence -= wetness x 0.15 (rain streaks on lens approximation) |
| Reflection renderer | Read | Reflection intensity = wetness x base_reflectivity (per material); puddle rendering threshold at wetness > 0.8 |
| Material visual | Read | All materials darken proportionally to wetness (see `materials-consequences-spec-v0.md`) |
| Hydrant entity | Write | Burst hydrant writes `wetness = 1.0` at its position |

### 6.5 Boundary Conditions

| Edge | Condition |
|------|-----------|
| All horizontal edges | Fixed at `wetness = rain_active ? rain_rate x 0.5 : 0.0` (boundary cells match ambient rain state) |
| Drain cells | Internal boundary: accelerated sink (see above) |

### 6.6 Debug Visualization

- **Wetness heatmap:** Blue gradient on ground plane (white = dry, deep blue = saturated).
- **Drainage overlay:** Yellow markers on drain cells.
- **Shade map:** Gray overlay showing shade_factor per cell.
- **Puddle threshold:** Cells with wetness > 0.8 outlined in cyan (indicates puddle rendering active).

---

## 7. Crowd Density Field

### 7.1 Parameters

| Property | Value |
|----------|-------|
| Data type | `float32` (scalar, persons / m^2, range 0.0--6.0) |
| Grid resolution | 2 m (2D ground-plane only) |
| Grid dimensions (slice) | ~300 x 150 = 45,000 cells |
| Update frequency | 5 Hz |
| Memory footprint | 45,000 x 4 bytes = ~180 KB (double-buffered: 360 KB) |

### 7.2 Source Terms

| Source | Contribution Rule | Spatial Extent |
|--------|-------------------|----------------|
| **NPC presence** | Each NPC adds 1.0 to the cell containing its position; aggregated via spatial hash | Point contribution at NPC cell |
| **Normalization** | Cell value = NPC count in cell / cell_area (4 m^2) | Per-cell |

This field is purely derived from NPC positions. There are no independent source terms. The field is recomputed from scratch every tick (no history dependence).

### 7.3 Sink / Decay Terms

| Mechanism | Rule |
|-----------|------|
| **Spatial smoothing** | 3x3 Gaussian blur applied after raw accumulation to prevent single-cell spikes; sigma = 1 cell |
| **No temporal decay** | Field is recomputed each tick; previous values discarded |

### 7.4 Entity Coupling

| Entity Type | Read / Write | Behavior |
|-------------|-------------|----------|
| NPC movement | Read | Movement speed multiplier = clamp(1.0 - (density - 1.0) x 0.25, 0.2, 1.0); density > 4.0 = crush risk, NPC attempts to flee |
| CCTV occlusion | Read | Person-identification probability = clamp(1.0 - density x 0.15, 0.1, 1.0); dense crowd = hard to identify individuals |
| Witness count | Read | Expected witnesses to event at cell = density x cell_area x awareness_probability (0.3 for loud event, 0.05 for quiet event) |
| Noise field coupling | Write (indirect) | Density value at each cell contributes to noise field: `noise += density x 15 dB` (crowd chatter) |
| Pickpocket AI | Read | Opportunity score = density x (1.0 - authority_visibility); requires density > 2.0 to attempt |
| Vehicle NPC | Read | Vehicles avoid cells with density > 1.0 on road surface (jaywalking crowd blocks traffic) |

### 7.5 Boundary Conditions

| Edge | Condition |
|------|-----------|
| All horizontal edges | Boundary cells use NPC count at boundary portals; effectively zero in non-portal boundary cells |

### 7.6 Debug Visualization

- **Density heatmap:** Ground-plane overlay, green (< 1.0) to yellow (1.0--3.0) to red (> 3.0) to magenta (> 5.0, crush danger).
- **Flow arrows:** Average NPC velocity vector per cell, drawn as arrows (shows crowd flow direction).
- **Bottleneck highlight:** Cells with density > 3.0 and flow speed < 0.5 m/s highlighted as orange (congestion point).

---

## 8. Heat Field (4-Channel)

### 8.1 Parameters

| Property | Value |
|----------|-------|
| Data type | `vec4` (4 floats: physical, social, institutional, ecological; each 0.0--1.0) |
| Grid resolution | Per-block (~80 m; aligned to block boundaries) |
| Grid dimensions (slice) | ~40 blocks = 40 cells |
| Update frequency | 0.1 Hz (every 10 seconds) |
| Memory footprint | 40 x 16 bytes = 640 bytes (negligible) |

### 8.2 Channel Definitions

| Channel | Index | Meaning | Typical Sources | Threshold Effects |
|---------|-------|---------|-----------------|-------------------|
| **Physical** | 0 | Danger to life/property: fire, collapse, explosion, traffic accident | Damage events, fire events, structural events | > 0.3: emergency response dispatched. > 0.7: evacuation behavior triggered. |
| **Social** | 1 | Public attention / unrest: protests, street performances, fights, anomaly rubbernecking | Crowd gathering events, altercation events, anomaly visibility | > 0.3: media coverage probability rises. > 0.7: faction leaders take notice. |
| **Institutional** | 2 | Authority pressure / surveillance intensity: police presence, CCTV coverage, regulatory action | Authority NPC patrol reports, CCTV evidence committed, citations issued | > 0.3: increased patrol frequency. > 0.7: lockdown protocol possibility. |
| **Ecological** | 3 | Environmental disruption: pollution, noise damage, infrastructure stress, anomaly contamination | Pollution events, sustained noise > 90 dB, infrastructure damage, anomaly residue | > 0.3: city-services dispatch. > 0.7: area closure for remediation. |

### 8.3 Source Terms

| Source Event | Channel(s) Affected | Contribution | Duration |
|-------------|---------------------|-------------|----------|
| Vehicle accident | Physical +0.15, Social +0.10, Institutional +0.05 | Instant bump, then decay | Decays over 300 s |
| Gunshot / explosion | Physical +0.30, Social +0.20, Institutional +0.20 | Instant bump | Decays over 600 s |
| Anomaly manifestation | All channels: +0.10 to +0.40 depending on intensity | Sustained while anomaly active | Residual Heat for 600 s after anomaly closes |
| Protest / large gathering | Social +0.25, Institutional +0.10 | Sustained while gathering persists | Decays over 300 s after dispersal |
| CCTV evidence committed | Institutional +0.02 per entry | Incremental | Decays at standard rate |
| Authority NPC patrol pass | Institutional +0.01 per pass | Incremental | Decays at standard rate |
| Fire | Physical +0.40, Social +0.15, Ecological +0.20 | Sustained while burning | Residual for 900 s |
| Power outage (block) | Physical +0.10, Social +0.15, Institutional -0.10 (blind spot) | Sustained while dark | Resolves when power restored |

### 8.4 Sink / Decay Terms

| Mechanism | Rule |
|-----------|------|
| **Natural decay** | Each channel decays at rate 0.001/s (exponential) toward 0.0 |
| **Authority suppression** | Institutional channel presence reduces Social channel at rate -0.0005/s per authority NPC in block (policing calms social Heat) |
| **Remediation event** | City-services cleanup event reduces Ecological channel by 0.2 (instant) |
| **Resolution event** | Narrative resolution (e.g., fire extinguished, suspect apprehended) reduces associated channels by 0.3 (instant) |

### 8.5 Entity Coupling

| Entity Type | Read / Write | Behavior |
|-------------|-------------|----------|
| Authority NPC | Read + Write | Reads Heat to determine urgency of dispatch and patrol routes; writes Institutional Heat via presence and reports |
| Faction AI | Read | Faction strategic decisions key off Heat thresholds (see channel threshold table above) |
| Pedestrian NPC | Read | Physical Heat > 0.5: avoidance routing (walk around block). Social Heat > 0.5: rubbernecking behavior (some NPCs move toward, some away) |
| Portal system | Read | Anomaly portal stability inversely proportional to local Heat magnitude (high Heat destabilizes portals) |
| Crowd density | Indirect | Physical Heat > 0.7 causes density decrease (avoidance); Social Heat > 0.5 causes density increase near source (rubbernecking) |
| Media NPC | Read | Social Heat > 0.3 triggers media NPC spawn/dispatch to block |

### 8.6 Boundary Conditions

| Edge | Condition |
|------|-----------|
| Adjacent districts | Heat diffuses across district boundaries at 0.1x rate (neighboring blocks in different districts receive 10% of Heat change) |
| Slice boundary | Heat at boundary blocks fixed at 0.0 (off-slice world assumed calm) |

### 8.7 Debug Visualization

- **4-channel bar chart:** Per-block overlay showing four vertical bars (red = physical, yellow = social, blue = institutional, green = ecological).
- **Threshold highlight:** Blocks exceeding any channel threshold (0.3, 0.7) outlined with corresponding color + pulsing intensity.
- **Heat history sparkline:** Per-block time-series graph of all four channels over the last 600 s (10 minutes).

---

## 9. Field Coupling Matrix

Fields do not exist in isolation. Changes in one field cause changes in others. All inter-field couplings are enumerated below. Coupling is computed per-cell during step 3 of the update pipeline (see Section 2.2).

| # | Source Field | Affected Field | Coupling Rule | Update Phase |
|---|-------------|----------------|---------------|-------------|
| 1 | **Rain (weather state)** | **Wetness** | `wetness += rain_rate x dt x (1.0 - shade_factor)` | Wetness source accumulation |
| 2 | **Wetness** | **Traction (entity property)** | `traction = base_traction x (1.0 - 0.4 x wetness)` | Entity reads wetness on movement tick |
| 3 | **Wind** | **Noise** | `noise += wind_speed x 0.1` per cell | Noise inter-field coupling step |
| 4 | **Wind** | **Wetness** | `wetness -= wind_speed x 0.002 x dt` (drying acceleration) | Wetness sink step |
| 5 | **Crowd Density** | **Noise** | `noise += density x 15` (dB equivalent, crowd chatter) | Noise inter-field coupling step |
| 6 | **Light** | **CCTV Quality (entity property)** | `quality = base_quality x clamp(light_intensity / reference_light, 0.1, 1.0)` | CCTV entity reads light on evidence tick |
| 7 | **Wetness** | **CCTV Confidence (entity property)** | `confidence -= wetness x 0.15` (rain-on-lens penalty) | CCTV entity reads wetness on evidence tick |
| 8 | **Wetness** | **Light (reflection)** | Wet cells increase specular reflection component by `wetness x 0.5` in light field | Light inter-field coupling step |
| 9 | **Heat (physical)** | **Crowd Density (behavioral)** | Physical Heat > 0.7 at block: density target for that block reduced by 50% (avoidance) | Density target adjustment at block-level tick (0.1 Hz) |
| 10 | **Heat (social)** | **Crowd Density (behavioral)** | Social Heat > 0.5 at block: density target increased by 30% at source cell (rubbernecking) | Density target adjustment at block-level tick |
| 11 | **Noise** | **Heat (ecological)** | Sustained noise > 90 dB for > 60 s: Ecological Heat += 0.01 per 10 s | Heat source accumulation |
| 12 | **Light (anomaly)** | **Heat (social)** | Visible anomaly glow (light.anomaly_component > 500 lux): Social Heat += 0.05 per 10 s | Heat source accumulation |
| 13 | **Anomaly event** | **Wind** | Anomaly zone generates vortex: circular wind pattern, magnitude = anomaly_intensity x 15 m/s | Wind source accumulation |
| 14 | **Anomaly event** | **Light** | Anomaly zone generates purple-cyan glow: intensity = anomaly_intensity x 3000 lux | Light source accumulation |
| 15 | **Anomaly event** | **Noise** | Anomaly zone generates low-frequency hum: +40 to +80 dB proportional to intensity | Noise source accumulation |
| 16 | **Anomaly event** | **Wetness** | Anomaly zone accelerates drying: `wetness -= anomaly_intensity x 0.1 x dt` (reality distortion dessicates) | Wetness sink step |
| 17 | **Anomaly event** | **Crowd Density** | Small anomaly (intensity < 0.3): rubbernecking, density increases. Large anomaly (> 0.5): displacement, density decreases (fleeing). | Behavioral (NPC decision) |

### 9.1 Coupling Execution Order

To prevent circular dependency artifacts, fields update in a fixed order each tick:

```
1. Wind         (reads: weather state, building map, anomaly state)
2. Wetness      (reads: weather state, wind field, anomaly state)
3. Light        (reads: time-of-day, entity lights, wetness field, anomaly state)
4. Noise        (reads: entity sources, wind field, crowd density field, anomaly state)
5. Crowd Density (reads: NPC positions — no field dependencies)
6. Heat         (reads: event log, noise field, light field — slowest update rate)
```

Fields at step N read the **front buffer** (just-swapped) of fields updated at steps 1 through N-1, and the **previous tick's front buffer** of fields updated at steps N+1 onward. This one-tick lag is imperceptible at runtime update rates.

---

## 10. Anti-O(N^2) Design Rules

These rules are non-negotiable architectural constraints. Any system that violates them must be refactored before merging.

### 10.1 Rule 1: Fields Update on Fixed Grids, Not Per-Entity Pairs

**Forbidden:**
```
for each entity_a:
    for each entity_b:
        compute_influence(entity_a, entity_b)   // O(N^2)
```

**Required:**
```
for each entity:
    write_to_field(entity.position, entity.contribution)   // O(N) write
for each cell:
    propagate(cell)   // O(cells) propagation
for each entity:
    read_from_field(entity.position)   // O(N) read
```

Total cost: O(N) + O(cells) + O(N) = O(N + cells). Since cells is fixed, this is O(N) in entity count.

### 10.2 Rule 2: Entity-Field Interaction is O(1) per Entity

An entity reads the field value at its grid cell. This is a single array index lookup. No iteration over other entities, no raycasts, no spatial queries.

**Exception:** If an entity needs values from a neighborhood (e.g., gradient for wind direction), it reads a fixed-size stencil (3x3 or 5x5 cells). This is still O(1) per entity (constant stencil size).

### 10.3 Rule 3: Field-Field Coupling is O(cells) per Tick

Inter-field coupling (Section 9) is computed per-cell, not per-entity. The coupling formula reads one field's cell value and writes to another field's cell value. Total cost: O(cells) per coupling per tick. With 6 fields and ~17 coupling rules, this is 17 x O(cells) = O(cells), which is bounded by the fixed grid size.

### 10.4 Rule 4: Event Escalation is Hierarchical, Not Broadcast

When an event occurs at Entity level, it is **not** broadcast to all entities. Instead:

1. Event is recorded on the containing Patch.
2. Patch aggregates events and checks Block-level threshold.
3. If threshold exceeded, event escalates to Block.
4. Block aggregates and checks District-level threshold.
5. If threshold exceeded, event escalates to District.

At each level, only the containing spatial unit processes the event. No global iteration. Cost: O(hierarchy_depth) = O(5) = O(1).

### 10.5 Rule 5: Locality — No Global Coupling Except Weather

No field effect propagates instantaneously across the entire slice. All field propagation is local (cell-to-neighbor diffusion) with finite propagation speed. The only exception is **weather state**, which is a City-level global and affects all cells uniformly.

**Consequence:** A noise event in Times Square does not instantly affect cells in Hell's Kitchen. It propagates through the noise field at the speed of sound (approximated as 1 cell per tick at 5 Hz update rate = ~10 m/s propagation in the field, slower than real sound but acceptable for gameplay).

### 10.6 Performance Budget Summary

| Operation | Cost per Tick | Frequency | Total Cost per Second |
|-----------|--------------|-----------|----------------------|
| Entity → field write | O(N) where N = active entities (~5000) | Per field update (1--10 Hz) | ~25,000 writes/s |
| Field propagation | O(cells) per field (~45,000--180,000) | Per field update (1--10 Hz) | ~500,000 cell updates/s |
| Field → entity read | O(N) per field (~5000) | Per entity tick (10--60 Hz) | ~150,000 reads/s |
| Inter-field coupling | O(cells) per coupling rule (~17 rules) | Per affected field update | ~300,000 cell updates/s |
| Event escalation | O(1) per event | Per event (~100 events/s) | ~500 operations/s |

**Total field system budget:** ~1M cell operations/s + ~175K entity operations/s. This fits within a single CPU core at modern clock speeds, leaving the GPU entirely free for rendering.

---

*End of document. For entity hierarchy definitions, see `ontology-spec-v0.md`. For escalation and hierarchy coupling rules, see `hierarchy-coupling-rules-v0.md`. For material-level field responses, see `materials-consequences-spec-v0.md`.*
