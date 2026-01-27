# Performance Budget Sheet

> **Twin Earth NYC -- Part 10: Build Pipeline**
> Document: `performance-budget-v0.md` | Version 0.1 | Status: Draft
> Last updated: 2026-01-27

---

## Purpose

Every asset, system, and effect in Twin Earth NYC must fit within a fixed performance envelope. This document defines triangle budgets, texture memory allocations, CPU time per subsystem, streaming constraints, scenario-specific targets, and emergency fallback measures. No asset may ship without verifying its contribution fits within these budgets.

**Rule:** If it does not fit in the budget, it does not ship. There are no exceptions -- only trade-offs.

---

## Target Platform

| Spec | Minimum | Recommended |
|------|---------|-------------|
| **GPU** | NVIDIA RTX 4070 / AMD RX 7800 XT | RTX 4080 / RX 7900 XT |
| **VRAM** | 12 GB | 16 GB |
| **CPU** | 8-core / 16-thread (Ryzen 7 7700X / i7-13700K) | 12-core / 24-thread |
| **RAM** | 16 GB DDR5 | 32 GB DDR5 |
| **Storage** | NVMe SSD (PCIe 3.0, 3 GB/s read) | NVMe SSD (PCIe 4.0, 5+ GB/s read) |
| **OS** | Windows 10 64-bit | Windows 11 64-bit |
| **API** | DirectX 12 / Vulkan 1.3 | DirectX 12 Ultimate |

### Frame Rate Targets

| Target | Value | Enforcement |
|--------|-------|-------------|
| **Primary target** | **60 fps** (16.6ms frame budget) | Design goal for baseline scenarios |
| **Acceptable floor** | **30 fps** (33.3ms frame budget) | Absolute minimum -- never below this |
| **VSync** | Adaptive | No fixed VSync -- adaptive sync preferred |

---

## Triangle Budgets

All values are per-frame maximums for the visible scene (after frustum culling, occlusion culling, and LOD selection).

### By Category and Distance Band

| Category | Near (0--30m) | Mid (30--150m) | Far (150m+) | Total |
|----------|---------------|----------------|-------------|-------|
| **Buildings** | 1,500,000 | 800,000 | 200,000 | **2,500,000** |
| **Street / Ground** | 300,000 | 150,000 | 50,000 | **500,000** |
| **Props** | 200,000 | 100,000 | 20,000 | **320,000** |
| **Vehicles** | 100,000 | 50,000 | 10,000 | **160,000** |
| **Characters** | 500,000 | 200,000 | 20,000 | **720,000** |
| **Billboards** | 50,000 | 30,000 | 10,000 | **90,000** |
| **VFX / Particles** | -- | -- | -- | **100,000** |
| **TOTAL** | **2,650,000** | **1,330,000** | **310,000** | **~4,390,000** |

### Per-Asset Triangle Limits

| Asset Type | L0 (Near) | L1 (Mid) | L2 (Far) | Notes |
|------------|-----------|----------|----------|-------|
| Hero building (T1) | 150,000 | 40,000 | 5,000 | One Times Square, Marriott, etc. |
| Support building (T2) | 50,000 | 15,000 | 2,000 | Mid-block buildings |
| Background building (T3) | 10,000 | 3,000 | 500 | Distant skyline fill |
| Hero prop (T1) | 5,000 | 1,500 | 200 | TKTS steps, kiosks |
| Standard prop (T2) | 1,500 | 500 | 50 | Bollards, trash cans |
| Background prop (T3) | 300 | 100 | -- (culled) | Distant street furniture |
| Vehicle (near) | 15,000 | 5,000 | 500 | Player-proximate vehicles |
| Vehicle (traffic) | 5,000 | 1,500 | 200 | Background traffic |
| NPC (hero) | 25,000 | 8,000 | 500 | Named / interactable NPCs |
| NPC (crowd) | 5,000 | 1,500 | 200 | Background pedestrians |
| NPC (impostor) | -- | -- | 2 (billboard) | Farthest crowd, camera-facing quads |

### LOD Transition Distances

| LOD Transition | Distance | Hysteresis |
|----------------|----------|------------|
| L0 --> L1 | 30m | +/- 3m |
| L1 --> L2 | 150m | +/- 10m |
| L2 --> Cull | 500m (buildings), 200m (props), 300m (vehicles) | +/- 20m |
| Impostor activation | 250m+ (characters only) | +/- 15m |

---

## Texture Memory (VRAM)

### Budget by Category

| Category | Budget | Notes |
|----------|--------|-------|
| **Building textures** (atlas + unique) | 1,500 MB | Shared atlas for T2/T3; unique maps for T1 hero buildings |
| **Street / ground textures** | 256 MB | Tiled materials with detail maps |
| **Prop textures** | 256 MB | Shared atlas for standard kit; unique for hero props |
| **Character textures** | 512 MB | Hero NPCs: individual maps; crowd: shared atlas |
| **Billboard video frames** (4 active) | 256 MB | 4 simultaneous video billboards at 1080p |
| **VFX textures** | 128 MB | Particle atlases, rain, fog volumes |
| **UI + HUD** | 64 MB | Menus, overlays, minimap |
| **Shadow maps** | 256 MB | Cascaded shadow maps (4 cascades) |
| **Render targets** (GBuffer, post-process) | 512 MB | At 2560x1440 target resolution |
| **TOTAL VRAM** | **~3,740 MB** | **Within 4 GB target leaving ~260 MB headroom** |

### Texture Resolution Limits

| Asset Type | Max Resolution | Format |
|------------|---------------|--------|
| Hero building facade (T1) | 4096 x 4096 | BC7 (albedo), BC5 (normal), BC4 (roughness) |
| Support building (T2) | 2048 x 2048 | BC7 / BC5 / BC4 |
| Background building (T3) | 1024 x 1024 | BC1 (albedo only) |
| Hero prop (T1) | 2048 x 2048 | BC7 / BC5 / BC4 |
| Standard prop (T2) | 1024 x 1024 | BC7 / BC5 |
| Character (hero) | 2048 x 2048 | BC7 / BC5 / BC4 |
| Character (crowd) | 512 x 512 (atlas tile) | BC7 |
| Billboard (video) | 1920 x 1080 per frame | BC1 (compressed video decode) |
| Ground / road | 2048 x 2048 (tiled) | BC7 / BC5 / BC4 |

---

## CPU Budgets

### Per-Frame Time Allocation (target: 16.6ms total for 60fps)

| System | Per-Frame Budget | Update Rate | Notes |
|--------|-----------------|-------------|-------|
| **Rendering** (main thread submission) | 4.0 ms | Every frame | Draw call submission, state changes |
| **Physics** (PhysX / custom) | 4.0 ms | Every frame | Hero zone full sim; background simplified rigid body |
| **NPC AI -- background** | 2.0 ms | Batched (staggered 5Hz) | Heuristic pathfinding, state machine updates |
| **NPC AI -- hero** | 3.0 ms | 10 Hz | RL inference for named NPCs; decision tree for interactables |
| **Traffic logic** | 1.0 ms | 2 Hz (interpolated) | Signal state, lane assignment, vehicle spawning |
| **Show Director** | 0.5 ms | Every frame | LOD decisions, swap scheduling, near-band management |
| **Event bus** | 0.5 ms | Every frame | Event processing, evidence generation, subscriber dispatch |
| **Ledger** | 0.2 ms | Event-driven | Commit operations, entity state persistence |
| **Audio** | 1.5 ms | Every frame | 3D positioned sources, priority sorting, occlusion |
| **Animation** | 2.0 ms | Every frame | Skeletal animation, blend trees, IK |
| **Streaming** | 0.5 ms | Async (spikes managed) | Asset load scheduling, priority queue management |
| **Game logic** (scripts, quests, triggers) | 1.0 ms | Every frame | Gameplay systems, mission state, UI updates |
| **TOTAL** | **~20.2 ms** | -- | **Exceeds single-thread budget; relies on multi-threading** |

### Threading Strategy

| Thread | Systems | Target Time |
|--------|---------|-------------|
| **Main thread** | Rendering submission, Game logic, UI | < 12 ms |
| **Physics thread** | PhysX simulation | < 4 ms |
| **AI thread pool** (2--4 threads) | NPC AI (hero + background), Traffic | < 5 ms parallel |
| **Audio thread** | Audio mixing, 3D positioning | < 1.5 ms |
| **Streaming thread** | Async I/O, decompression | Non-blocking; < 500ms spike |
| **Worker pool** (4+ threads) | Animation, Event bus, Ledger, Show Director | < 4 ms parallel |

**Effective parallel budget:** ~12 ms main thread + subsystems on parallel threads = **fits within 16.6ms** for 60fps.

---

## Streaming Budgets

| Parameter | Value | Notes |
|-----------|-------|-------|
| **Cell size** | 1 city block (~100m x 200m) | Matches block intake unit |
| **Pre-load radius** | 2 cells ahead of player direction | Predictive based on velocity and heading |
| **Max concurrent loads** | 2 cells | Prevents I/O saturation |
| **Load time target** | < 500ms per cell | NVMe SSD assumed; decompression included |
| **Streaming spike ceiling** | < 6 GB total RAM during cell transitions | Includes old cell (not yet released) + current cell + new cell loading |
| **Asset pool size** | 8 GB resident (steady state) | Working set of loaded assets |
| **Unload latency** | < 2 frames after cell exits active set | Prevents memory accumulation during fast traversal |

### Streaming Priority Order

| Priority | Asset Type | Rationale |
|----------|-----------|-----------|
| 1 (highest) | Collision + NavMesh | Player must never fall through the world |
| 2 | Ground / road textures | Immediate visual impact underfoot |
| 3 | Building L2 (silhouettes) | Canyon shape must be visible immediately |
| 4 | Building L1 / L0 | Detail pops in second |
| 5 | Props + street furniture | Context fills in |
| 6 | Characters / NPCs | Crowd density fills in |
| 7 | Billboard content | Video frames can start black and fade in |
| 8 (lowest) | VFX, detail particles | Ambient effects last |

---

## Performance Scenarios

| Scenario | FPS Target | Key Pressure Points | Budget Notes |
|----------|-----------|---------------------|--------------|
| **Baseline midday** | 60 fps | Crowd density (800 NPCs visible) + billboard video playback | Standard budget; all systems at normal load |
| **Rainy night** | 55 fps | Screen-space reflections on wet surfaces + rain particle system + reduced LOD distances due to fog | Reduce SSR to half-res; cap rain particles at 50K; tighten LOD L0 to 25m |
| **Anomaly event** | 45 fps | VFX burst (anomaly visuals) + additional entity spawns + evidence generation I/O | Allow VFX to consume extra 2ms; defer non-critical evidence writes |
| **Peak crowd** (2000 NPCs visible) | 40 fps | Character rendering (skeleton + animation) + AI compute | Aggressively use impostors beyond 100m; batch AI updates at 2Hz for background |
| **Worst case** (rain + anomaly + peak crowd) | 30 fps **(minimum -- never below)** | Everything at maximum load simultaneously | Emergency measures activate automatically (see below) |

### Scenario Budget Adjustments

```
BASELINE (60fps target):
  GPU: 16.6ms  |  CPU: 16.6ms (parallel)
  ├── Triangles: 4.3M max
  ├── Draw calls: 2,500 max
  ├── Characters: 800 visible, 200 skeletal, 600 impostor
  └── Billboards: 4 video + 20 static

RAINY NIGHT (55fps target):
  GPU: 18.2ms  |  CPU: 16.6ms
  ├── Triangles: 3.8M max (tighter LOD)
  ├── Draw calls: 2,200 max
  ├── SSR: half-resolution
  ├── Rain particles: 50,000 max
  └── Wet material shader: enabled (adds ~1ms GPU)

ANOMALY EVENT (45fps target):
  GPU: 22.2ms  |  CPU: 18ms (AI thread relaxed)
  ├── Triangles: 4.5M max (VFX extra)
  ├── VFX budget: +100K triangles, +2ms GPU
  ├── Evidence writes: deferred batch (async)
  └── Crowd reduced by 15% (background despawn)

PEAK CROWD (40fps target):
  GPU: 25ms  |  CPU: 20ms
  ├── Characters: 2000 visible, 300 skeletal, 1700 impostor
  ├── AI: background NPCs at 2Hz, hero NPCs at 5Hz
  ├── Animation: LOD blending (far NPCs: root motion only)
  └── Props: reduce to L1 beyond 20m

WORST CASE (30fps target):
  GPU: 33.3ms  |  CPU: 25ms
  └── EMERGENCY MEASURES ACTIVE (see below)
```

---

## Emergency Performance Measures

When frame rate drops below **35 fps** for more than **10 consecutive frames**, the following measures activate automatically in order. Each measure is released (reversed) when frame rate recovers above **45 fps** for 30 consecutive frames.

| Priority | Measure | Expected FPS Recovery | Side Effect |
|----------|---------|----------------------|-------------|
| **1** | **Demote all billboards to static emissive.** Stop video playback; replace with last-captured still frame as emissive texture. | +3--5 fps | Billboards freeze momentarily; acceptable for short durations |
| **2** | **Reduce crowd density by 30%.** Despawn the farthest 30% of background NPCs. Maintain hero NPCs and all NPCs within 30m. | +5--8 fps | Streets appear less crowded; re-spawn on recovery |
| **3** | **Reduce Show Director near-band to 20m** (from default 30m). Fewer entities receive full-detail treatment. | +2--3 fps | Detail pops in closer; subtle quality reduction |
| **4** | **Disable non-critical VFX.** Turn off rain splash particles, cloth simulation, trash blowing, steam vents. Keep critical VFX (anomaly indicators, player feedback). | +3--5 fps | Atmosphere reduced; critical gameplay VFX preserved |
| **5** | **Reduce shadow resolution by 50%.** Halve shadow map resolution across all cascades. | +2--4 fps | Softer, lower-quality shadows; acceptable at distance |
| **6** | **Reduce render resolution to 75%.** Apply dynamic resolution scaling to render at 75% of native, then upscale (FSR / DLSS). | +5--8 fps | Softer image; temporal upscaling mitigates most artifacts |
| **7** | **Disable screen-space reflections entirely.** Fall back to cubemap reflections only. | +2--3 fps | Wet surfaces lose accurate reflections; cubemaps provide approximation |

### Emergency Activation Log

Every emergency activation is logged:

```json
{
  "timestamp": "2026-03-15T22:15:03.412Z",
  "trigger": "fps_below_35_for_10_frames",
  "measures_activated": [1, 2],
  "fps_at_trigger": 32,
  "fps_after_activation": 44,
  "recovery_timestamp": "2026-03-15T22:15:18.001Z",
  "total_emergency_duration_ms": 14589
}
```

---

## Performance Testing Requirements

Every block and every build must pass these performance gates:

| Test | Condition | Pass Criteria | Frequency |
|------|-----------|---------------|-----------|
| **Baseline walk-through** | Walk through block at normal speed, midday, normal crowd | Average 60fps, no frame below 45fps | Every block completion |
| **Stress: peak crowd** | 2000 NPCs in block | Average 40fps, no frame below 30fps | Every block completion |
| **Stress: rain + night** | Night lighting + rain enabled | Average 55fps, no frame below 35fps | Every block completion |
| **Stress: worst case** | Rain + night + anomaly + 2000 NPCs | Average 30fps, no frame below 25fps for > 1 second | Weekly build validation |
| **Memory stability** | 30-minute session, all scenarios | No memory leak > 50MB over session; peak RAM < 14GB | Weekly build validation |
| **Streaming stress** | Sprint across 4 blocks at max speed | No visible pop-in for collision; texture pop-in < 500ms | Every block completion |

---

## Budget Enforcement

- **Pre-commit hook:** Triangle count and texture size are checked on every asset commit. Assets exceeding per-asset limits are rejected.
- **Nightly build:** Full-scene profiling runs automatically. Results posted to build dashboard.
- **Milestone gate:** Performance report is a mandatory sign-off item. No milestone ships without all scenarios meeting targets.
- **Budget trade requests:** If a team needs more budget in one category, they must identify an equal reduction in another category and submit a budget trade request to the Performance Lead for approval.

---

*End of document. For questions about performance budgets or optimization strategies, contact the Performance Lead or Tech Art.*
