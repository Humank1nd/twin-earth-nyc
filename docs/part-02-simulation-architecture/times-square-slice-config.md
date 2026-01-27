# Twin Earth NYC -- Times Square Slice Configuration

**Document:** Part 2, Deliverable 4
**Status:** Draft v0.1
**Scope:** Spatial, LOD, Commit, and Performance Configuration for the Times Square Vertical Slice
**Last Updated:** 2026-01-27

---

## 1. Slice Bounds

The Times Square vertical slice encompasses the "bowtie" intersection zone where Broadway crosses Seventh Avenue diagonally, creating the iconic triangular pedestrian plazas.

### Geographic Extents

| Edge | Street | Latitude / Longitude | Notes |
|---|---|---|---|
| **South** | West 42nd Street (centerline) | 40.7557N | Southern boundary. Includes 42nd St crosswalks. |
| **North** | West 47th Street (centerline) | 40.7598N | Northern boundary. Includes 47th St crosswalks. |
| **East** | Seventh Avenue (east curb line) | 73.9849W | Eastern boundary. Includes full 7th Ave roadway within slice. |
| **West** | Broadway (west curb line) | 73.9870W | Western boundary. Includes full Broadway roadway within slice. |

### Derived Measurements

| Property | Value |
|---|---|
| North-south extent | ~460m (42nd to 47th, 5 short NYC blocks) |
| East-west extent (widest) | ~180m (at 42nd St where Broadway and 7th Ave diverge) |
| East-west extent (narrowest) | ~65m (at 45th St where Broadway and 7th Ave converge) |
| Total ground area | ~52,000 m2 (approximately 12.8 acres) |
| Playable surface area (walkable) | ~18,000 m2 (sidewalks, plazas, crosswalks, TKTS steps) |
| Road surface area | ~22,000 m2 |
| Building footprint area (within bounds) | ~12,000 m2 |

### Key Landmarks Within Bounds

| Landmark | Location | Slice Region Code | Role |
|---|---|---|---|
| One Times Square | South end of bowtie, Broadway at 42nd-43rd | `TSQ` | Iconic triangular building; ball-drop tower; primary orientation landmark |
| TKTS Red Steps / Father Duffy Square | Between 45th-47th, Broadway median | `DUF` | Elevated viewing platform; social gathering point; 24 red steps |
| Marriott Marquee | West 45th-46th, Broadway west side | `BWY` | Curved LED facade; major visual landmark |
| Times Square Tower (One Astor Plaza) | West 44th-45th, Broadway west side | `BWY` | Tall office tower; defines western canyon wall |
| U.S. Armed Forces Recruiting Station | Between 43rd-44th, Broadway median island | `TSQ` | Small glass structure in pedestrian island; scale reference |
| George M. Cohan Statue | Father Duffy Square, north island | `DUF` | Bronze statue; collision object; cultural reference point |
| Father Duffy Statue | Father Duffy Square, central | `DUF` | Bronze statue on granite base; orientation landmark |

### Slice Region Codes

The slice is subdivided into regions for entity ID assignment and spatial queries:

| Code | Name | Description |
|---|---|---|
| `TSQ` | Times Square Core | Bowtie intersection, One Times Square, south pedestrian plazas (42nd-44th) |
| `DUF` | Duffy Square | Father Duffy Square, TKTS steps, north pedestrian plazas (45th-47th) |
| `BWY` | Broadway Corridor | Broadway roadway and adjacent building frontages |
| `7AV` | Seventh Avenue Corridor | 7th Ave roadway and adjacent building frontages |
| `SDE` | Side Streets | Cross streets (43rd, 44th, 45th, 46th) within slice bounds |

---

## 2. Distance Bands

All distance measurements are from the active camera position. Band boundaries are soft -- entities within 5m of a boundary use the higher-fidelity band to prevent oscillation.

| Band | Range | Hysteresis | Primary Use |
|---|---|---|---|
| **Near** | 0 - 30m | Downgrades at 33m, upgrades at 30m | Full fidelity simulation, unique assets, interactive |
| **Mid** | 30 - 150m | Downgrades at 155m, upgrades at 150m | Reduced fidelity, instanced motifs, simplified AI |
| **Far** | 150m+ | Upgrades at 150m | Silhouettes, billboards, flow-field crowds |

### Band Population Budgets

| Band | Max Buildings | Max Props | Max NPCs | Max Vehicles | Max Active VFX |
|---|---|---|---|---|---|
| **Near** | 12 unique | 200 unique | 150 (full skeletal) | 30 (full physics) | 50 emitters |
| **Mid** | 30 instanced | 100 LOD1 | 500 (instanced archetypes) | 60 (simplified) | 20 emitters |
| **Far** | Unlimited silhouettes | 0 (removed) | 1,350 (billboard cards) | 50 (kinematic sprites) | 5 emitters |
| **TOTAL** | -- | 300 | **2,000** | 140 | 75 |

---

## 3. LOD Thresholds Per Asset Class

### Buildings

| Transition | Distance | Geometry Change | Material Change | Streaming Cost |
|---|---|---|---|---|
| LOD0 to LOD1 | **50m** | Unique mesh to motif-instanced; small features merged (AC units, fire escapes consolidated into normal map) | 4K to 2K textures; parallax occlusion removed | ~15 MB freed per building |
| LOD1 to LOD2 | **150m** | Motif mesh to silhouette shell + emissive face | 2K to 1K emissive map; PBR replaced with flat unlit | ~8 MB freed per building |
| LOD2 to Dormant | **500m** (or off-screen) | Removed from render; collision retained as AABB | No textures resident | ~3 MB freed per building |

### Props (Street Furniture, Vehicles, Vendor Carts)

| Transition | Distance | Geometry Change | Physics Change | Streaming Cost |
|---|---|---|---|---|
| LOD0 to LOD1 | **30m** | Unique mesh to simplified mesh (50% polycount); small parts merged | Hero to Standard tier (60Hz to 30Hz); no CCD | ~2 MB freed per prop |
| LOD1 to LOD2 | **100m** | Simplified mesh to billboard sprite or removal | No physics | ~1 MB freed per prop |
| LOD2 to Dormant | **200m** (or off-screen) | Removed entirely | No physics; state preserved in ledger | ~0.5 MB freed per prop |

### Crowds (NPCs)

| Transition | Distance | Geometry Change | Animation Change | AI Change |
|---|---|---|---|---|
| LOD0 to LOD1 | **20m** | Unique skeletal (65 bones) to instanced archetype (32 bones); no face blendshapes | Full animation set to reduced set (walk/idle/turn); no facial; 30Hz update | Full behavior tree to state machine; no dialogue |
| LOD1 to LOD2 | **80m** | Instanced mesh to animated billboard card (8 variants) | 2-frame walk cycle; camera-facing rotation | No individual AI; flow-field driven |
| LOD2 to Dormant | **200m** (or off-screen for >10s) | Removed from render | None | Despawned; slot returned to pool |

### Billboards and Signage

| Transition | Distance | Content Change | Performance Impact |
|---|---|---|---|
| LOD0 to LOD1 | **30m** | Full 30fps video to 4fps low-res loop | ~50 MB VRAM saved per billboard |
| LOD1 to LOD2 | **100m** | 4fps loop to static emissive rectangle (dominant color sampled from LOD0) | ~10 MB VRAM saved per billboard |
| LOD2 to Dormant | **300m** | Emissive contribution baked into skybox glow; entity removed | ~2 MB VRAM saved per billboard |

---

## 4. Commit-Point Rules

The Trust Ledger commits events based on the following rules, specific to the Times Square slice context:

### Auto-Commit Triggers

| Trigger | Condition | Latency | Example |
|---|---|---|---|
| **Authority Action** | Any NYPD officer, security guard, or building system takes an enforcement action (arrest, lockdown, alarm activation, radio dispatch) | Immediate (same frame as action) | Officer radios dispatch about observed crime -- all related pending events commit |
| **Evidence Corroboration** | Two or more independent observation sources record the same event within spatial tolerance (+/- 5m) and temporal tolerance (+/- 30s) | Immediate on second source | CCTV captures door-force + NPC witness sees door-force = auto-commit both observations + the DMG event |
| **Anomaly Manifestation** | Any anomaly event reaches visible intensity (VFX active, physics distortion measurable) | Immediate on manifestation threshold | Reality bleed activates -- all anomaly-zone events commit |
| **Time Decay** | Uncommitted event has existed for 5 minutes sim-time without contradiction | At 5-minute mark | Player breaks a window, no one sees it, but after 5 sim-minutes the damage commits permanently |

### Player-Initiated Commits

| Trigger | Condition | Latency | Example |
|---|---|---|---|
| **Explicit Save** | Player opens menu and selects save (or autosave fires at checkpoint) | Immediate on confirm | All pending events commit with `PLAYER_SAVE` trigger tag |
| **Journal Entry** | Player records an observation in their in-game journal | Immediate | Player photographs evidence -- the observation event and all linked events commit |
| **Mission Checkpoint** | Player reaches a narrative checkpoint (mission start, objective complete, mission end) | Immediate | Starting a portal mission commits all hub events to prevent loss |

### Commit Conflict Rules

| Scenario | Resolution |
|---|---|
| Two events contradict (e.g., "door is locked" and "door is open") | Most recent event wins; older event marked `superseded_by` with newer event ID |
| Observation contradicts committed event | Observation stored with `DISPUTED` flag; does not override committed event unless authority re-adjudicates |
| Anomaly rollback affects committed events | Committed events gain `ANOMALY_REVERTED` tag but remain in ledger for narrative continuity; world state reverts |
| Session boundary with uncommitted events | All pending events commit with `SESSION_BOUNDARY` trigger; no data loss on exit |

---

## 5. Performance Targets

### Frame Rate

| Metric | Target | Minimum | Measurement |
|---|---|---|---|
| Average FPS | **60 fps** | **30 fps** | Rolling 10-second average |
| 99th percentile frame time | 22ms (45 fps) | 33ms (30 fps) | Per-frame measurement over 60s windows |
| Maximum single frame time | 33ms | 66ms (hard stutter limit) | Any single frame |
| Frame time during streaming | 22ms average | 33ms average | During LOD/asset streaming events |

### Memory Budgets

| Resource | Budget | Hard Cap | Notes |
|---|---|---|---|
| **VRAM (GPU)** | **4.0 GB** | 5.0 GB | Includes all textures, meshes, render targets, VFX buffers |
| **NPC RAM** | **2.0 GB** | 2.5 GB | Behavior trees, memory graphs, sensor buffers, animation state for all 2,000 NPCs |
| **Trust Ledger (disk)** | **500 MB** | 1.0 GB | SQLite database file. Summarization triggers at 500 MB soft cap. |
| **Streaming Pool** | 1.0 GB | 1.5 GB | Asset streaming ring buffer for LOD transitions |
| **Physics (PhysX)** | 512 MB | 768 MB | Collision meshes, broadphase structures, solver state |
| **Audio** | 256 MB | 384 MB | Loaded banks, streaming buffers, DSP state |
| **Total System RAM** | **8.0 GB** (game process) | 10.0 GB | Exclusive of OS and driver overhead |

### VRAM Breakdown (4.0 GB Budget)

| Category | Allocation | Notes |
|---|---|---|
| Building textures (all LODs) | 1,200 MB | ~12 near buildings at 4K, 30 mid at 2K, far at 1K |
| Billboard video textures | 600 MB | ~15 active video billboards, LOD0 at full res |
| NPC textures + meshes | 500 MB | 150 near (unique), 500 mid (instanced), 1,350 far (cards) |
| Vehicle textures + meshes | 200 MB | 30 near, 60 mid, 50 far |
| Props + street furniture | 200 MB | 200 near, 100 mid |
| Render targets (G-buffer, shadows, reflections) | 500 MB | 1080p base; 4K shadow atlas; SSR buffer |
| VFX (rain, steam, anomaly, particles) | 300 MB | Particle buffers, noise textures, volumetric fog |
| Skybox + atmosphere | 100 MB | HDR cubemap + atmospheric LUT |
| Reserve / headroom | 400 MB | For spikes during streaming transitions |

### NPC Memory Breakdown (2.0 GB Budget)

| Category | Per NPC (Near) | Per NPC (Mid) | Per NPC (Far) | Total at Max Pop |
|---|---|---|---|---|
| Behavior tree state | 8 KB | 2 KB | 0 KB | 2.2 MB |
| Memory graph (observations) | 32 KB | 4 KB | 0 KB | 6.8 MB |
| Sensor buffers | 16 KB | 0 KB | 0 KB | 2.4 MB |
| Animation state | 4 KB | 2 KB | 0.1 KB | 1.9 MB |
| Navigation state | 2 KB | 1 KB | 0.5 KB | 1.4 MB |
| Skeletal mesh instance data | 64 KB | 8 KB | 0.5 KB | 14.3 MB |
| **Per-NPC total** | **126 KB** | **17 KB** | **1.1 KB** | -- |
| **Band total** | 150 x 126 KB = **18.5 MB** | 500 x 17 KB = **8.3 MB** | 1,350 x 1.1 KB = **1.4 MB** | **28.2 MB** |

Remaining NPC budget (~1.97 GB) is allocated to shared resources: archetype mesh pools (800 MB), animation libraries (600 MB), shared navigation mesh (200 MB), AI blackboard and group coordination (200 MB), and reserve headroom (170 MB).

### Streaming Budgets

| Metric | Budget | Notes |
|---|---|---|
| Max concurrent asset loads | 8 | Prevents I/O saturation |
| Asset load timeout | 500ms | Asset must be render-ready within 500ms of request or fallback LOD holds |
| LOD transition time | 3 frames (50ms at 60fps) | Cross-fade between LOD levels |
| Maximum active seams | 10 | Per Show Director seam budget (see Architecture Spec) |
| Seam activation time | >= 3 seconds masked | Diegetic mask must be in place for at least 3s before/after seam content swap |

### Performance Degradation Protocol

When performance drops below targets, the engine sheds load in this priority order (lowest-value first):

| Priority | System | Degradation Action | FPS Recovery Estimate |
|---|---|---|---|
| 1 (shed first) | Far-band VFX | Disable far-band particle emitters | +2-3 fps |
| 2 | Rain particles | Reduce rain particle count by 50% | +3-5 fps |
| 3 | Mid-band NPC animation | Drop mid-band NPCs to 15Hz animation update | +2-4 fps |
| 4 | Shadow resolution | Halve shadow map resolution | +3-5 fps |
| 5 | Screen-space reflections | Disable SSR, fall back to cubemap reflections | +2-4 fps |
| 6 | Mid-band physics | Drop mid-band physics to 15Hz | +2-3 fps |
| 7 | Far-band NPCs | Reduce far-band NPC count by 50% (despawn farthest) | +3-5 fps |
| 8 | Billboard video | Drop all billboards to LOD1 (4fps) regardless of distance | +5-8 fps |
| 9 (shed last) | Near-band fidelity | Reduce near-band to LOD1 thresholds (last resort) | +5-10 fps |

**Never degraded:** Trust Ledger commit rate, physics collision correctness in near band, NPC sensor truth model, anomaly boundary accuracy. These are contractual obligations that hold regardless of performance state.

---

*End of Times Square Slice Configuration*
