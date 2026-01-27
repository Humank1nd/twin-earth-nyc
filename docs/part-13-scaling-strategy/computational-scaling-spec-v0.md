# Computational Scaling Spec v0

**Twin Earth NYC -- Part 13: Scaling Strategy and Risk Control**
**Document:** Anti-O(N^2) Strategies and Compute Budget Scaling
**Version:** 0.1.0
**Status:** Draft
**Last Updated:** 2026-01-27

---

## 1. Purpose

Twin Earth NYC must scale from 5 blocks to 500+ without frame rate, memory, or tick time growing faster than linearly with the number of active blocks. This document defines the locality rules, hierarchical aggregation strategies, event escalation policies, and budget formulas that prevent quadratic (or worse) cost growth. Every system architect must demonstrate that their system's cost function is at most O(N log N) in entity count before it ships.

**Rule:** Any system whose cost grows as O(N^2) or worse in entity count is a scaling time bomb. It must be redesigned before integration.

---

## 2. The Quadratic Threat

### 2.1 Where O(N^2) Hides

| System | Naive Implementation | Quadratic Source | Entity Count at Pain Threshold |
|--------|---------------------|------------------|-------------------------------|
| NPC-to-NPC awareness | Every NPC checks every other NPC for proximity | N*(N-1)/2 distance checks per tick | ~500 NPCs -> 124,750 checks/tick |
| Crowd collision avoidance | Every pedestrian resolves collisions against all others | Pairwise force computation | ~800 NPCs -> 319,200 pairs/tick |
| Event bus broadcast | Every event delivered to every subscriber | N_events * N_subscribers | ~200 events/s * 500 subscribers = 100K deliveries/s |
| Evidence correlation | Every new observation compared to all existing observations | N_new * N_existing | ~50 new/s * 10K existing = 500K comparisons/s |
| Line-of-sight checks | Every NPC raycasts against every other entity | N_npcs * N_entities | ~500 * 5000 = 2.5M raycasts/tick |
| Heat propagation | Every cell influences every other cell | N_cells^2 | ~1000 cells -> 1M interactions/tick |

### 2.2 The Budget Wall

At the Times Square slice (5 blocks), naive implementations are survivable. The pain threshold is predictable:

```
Entity growth with blocks:

  Entities(B) = E_base + E_per_block * B

  where:
    E_base      = 200    (global entities: skyline, weather, player)
    E_per_block = ~800   (NPCs: ~500, props: ~200, IoT: ~50, vehicles: ~50)

  5 blocks:   ~4,200 entities
  17 blocks:  ~13,800 entities
  41 blocks:  ~33,000 entities
  100 blocks: ~80,200 entities

Quadratic cost growth:
  5 blocks:   4,200^2  = ~17.6M operations
  17 blocks:  13,800^2 = ~190M operations     (10.8x growth for 3.3x entities)
  41 blocks:  33,000^2 = ~1.09B operations     (5.7x growth for 2.4x entities)
  100 blocks: 80,200^2 = ~6.43B operations     (5.9x growth for 2.4x entities)
```

At 100 blocks, a naive O(N^2) system consumes **365x** the CPU it used at 5 blocks. This is not "optimization needed" -- it is architectural failure.

---

## 3. Locality Rules

### 3.1 The Locality Principle

> No entity may interact with, query, or reason about any entity outside its **locality radius** unless the interaction is mediated by a hierarchical aggregation system.

| System | Locality Radius | Justification |
|--------|----------------|---------------|
| NPC vision | 50 m (recognition), 200 m (detection) | Sensor spec (Part 2) |
| NPC collision avoidance | 5 m | Physical interaction range |
| NPC social awareness | 30 m | Crowd behavior range |
| Physics simulation | 30 m (hero), 150 m (standard), 300 m (background) | Physics fidelity tiers (Part 2) |
| Event bus delivery | Per-topic locality (see Section 5) | Not all events are global |
| Heat propagation | 1 block (~200 m) | Heat is a local phenomenon; cross-block propagation uses aggregation |
| Show Director evaluation | Camera frustum + 35 m pre-stream | Only evaluate what might be visible soon |
| Evidence correlation | Same block + adjacent blocks | Observations from distant blocks are irrelevant to local events |

### 3.2 Spatial Indexing Requirement

Every system that performs entity queries must use a spatial index. The mandated index types:

| Query Pattern | Required Index | Lookup Cost | Update Cost |
|--------------|---------------|-------------|-------------|
| "All entities within R meters of point P" | Spatial hash grid (cell size = R) | O(1) average for fixed R | O(1) per entity move |
| "All entities in frustum F" | BVH (bounding volume hierarchy) | O(log N) | O(log N) per entity move |
| "K nearest entities to point P" | k-d tree or spatial hash | O(log N + K) | O(log N) per entity move |
| "All entities in block B" | Block-indexed array (direct lookup) | O(1) | O(1) on block transition |

### 3.3 Spatial Hash Grid Specification

The primary spatial index for NPC interactions is a uniform spatial hash grid:

```
SPATIAL HASH GRID:

  Cell size:    10 m x 10 m (horizontal)
  Grid extent:  Covers all loaded blocks + 50 m buffer
  Hash function: hash(x, z) = (floor(x/10) * PRIME_A) XOR (floor(z/10) * PRIME_B)
                 PRIME_A = 73856093, PRIME_B = 19349663
  Bucket:       Dynamic array (average 5-10 entities per cell in Times Square density)

  Lookup cost:  O(1) to find bucket + O(K) to iterate K entities in cell
  Worst case:   K = max_entities_per_cell (capped at 50; overflow logged as warning)
  Update cost:  O(1) per entity per frame (remove from old cell, insert into new cell)

  Memory per cell: ~80 bytes (array header + 10 entity pointers)
  Total memory (100 blocks, ~80K cells): ~6.4 MB
```

---

## 4. Hierarchical Aggregation

### 4.1 Three-Level Hierarchy

The world is organized into three spatial levels for aggregation:

```
Level 0: ENTITY    (individual NPC, prop, vehicle, sensor)
Level 1: BLOCK     (one city block, ~100m x 200m, ~800 entities)
Level 2: DISTRICT  (cluster of 4-9 blocks, ~400m x 600m, ~3000-7000 entities)
```

Systems that need cross-block information query the **block aggregate** (Level 1) instead of individual entities. Systems that need cross-district information query the **district aggregate** (Level 2).

### 4.2 Block Aggregates

Each block maintains a summary record updated once per second:

| Aggregate Field | Type | Description |
|----------------|------|-------------|
| `block_id` | string | Unique block identifier |
| `center` | vec3 | Block center position |
| `npc_count` | int | Total NPCs currently in block |
| `crowd_density` | float | NPCs per square meter (average) |
| `heat_levels[4]` | float[4] | Current Heat channel values (Physical, Social, Institutional, Ecological) |
| `alert_level` | int | Highest authority alert level in block |
| `active_anomalies` | int | Number of active anomalies |
| `traffic_congestion` | float | 0.0 (empty) to 1.0 (gridlock) |
| `ambient_noise_db` | float | Average ambient noise level |
| `event_rate` | float | Events per second (rolling 10 s window) |

**Cost:** 10 fields * ~8 bytes = ~80 bytes per block. Update: 1 Hz. Total for 100 blocks: 8 KB, negligible.

### 4.3 District Aggregates

Each district maintains a summary record updated every 5 seconds:

| Aggregate Field | Type | Description |
|----------------|------|-------------|
| `district_id` | string | Unique district identifier |
| `block_ids[]` | string[] | Constituent blocks |
| `total_npc_count` | int | Sum of block NPC counts |
| `mean_heat[4]` | float[4] | Average Heat across constituent blocks |
| `max_alert_level` | int | Highest alert level across blocks |
| `has_active_anomaly` | bool | Any block has an active anomaly |

### 4.4 Aggregation Use Cases

| Query | Naive Cost | Aggregated Cost | Speedup at 100 Blocks |
|-------|-----------|----------------|----------------------|
| "What is the crowd density 3 blocks north?" | Iterate all NPCs in target block: O(800) | Read block aggregate: O(1) | 800x |
| "Which district has the highest Heat?" | Iterate all entities in all blocks: O(80K) | Iterate district aggregates: O(12) | 6,667x |
| "Should authority dispatch to this block?" | Compute Heat from all evidence in all blocks: O(N_evidence) | Read block aggregate heat_levels: O(1) | ~10,000x |
| "How congested is the route from A to B?" | Pathfind through entity-level traffic: O(N_vehicles) | Read block aggregates along route: O(route_blocks) | ~500x |

---

## 5. Event Escalation Policy

### 5.1 Event Locality Tiers

Not all events need to reach all subscribers. The event bus partitions events into locality tiers:

| Tier | Scope | Delivery | Examples |
|------|-------|----------|---------|
| **Tier 0: Entity-local** | Same entity only | Direct callback, zero bus overhead | Animation state change, internal timer expiry |
| **Tier 1: Cell-local** | Same spatial hash cell (10 m radius) | Delivered to subscribers in same cell | NPC footstep, door open/close, small prop interaction |
| **Tier 2: Block-local** | Same city block | Delivered to subscribers in same block | Traffic signal change, CCTV observation, minor crime |
| **Tier 3: District-wide** | Same district (4-9 blocks) | Delivered to subscribers in district | Authority dispatch, siren activation, anomaly detection |
| **Tier 4: Global** | All loaded blocks | Broadcast to all subscribers | Portal formation, major Heat spike, weather change, player death |

### 5.2 Escalation Rules

Events start at their natural tier and **escalate** upward only when conditions are met:

```
EVENT ESCALATION:

  Initial tier = event.default_tier (defined per event type)

  IF event.severity >= 3 AND event.tier < DISTRICT:
    Escalate to DISTRICT

  IF event.severity >= 4 AND event.tier < GLOBAL:
    Escalate to GLOBAL

  IF event.heat_delta > 0.1 AND event.tier < BLOCK:
    Escalate to BLOCK

  IF event.triggers_authority AND event.tier < DISTRICT:
    Escalate to DISTRICT

  Events NEVER escalate past GLOBAL.
  Escalation is logged for debugging.
```

### 5.3 Delivery Cost Model

```
Delivery cost per event:

  Tier 0: ~0 (inline callback)
  Tier 1: ~10 subscriber checks (entities in cell)
  Tier 2: ~50-100 subscriber checks (entities in block)
  Tier 3: ~200-500 subscriber checks (entities in district)
  Tier 4: ~ALL subscribers (capped at 2000 per frame; excess queued)

Event bus budget: 0.5 ms per frame (see Part 10, performance-budget-v0)
At 60 fps: ~30 ms/s available for event delivery
Sustainable rate: ~2000 Tier 2 events/s, or ~200 Tier 3 events/s, or ~50 Tier 4 events/s
```

---

## 6. LOD as Compute Saving

### 6.1 LOD Reduces More Than Triangles

LOD tiers (from Show Director, Part 9) do not just reduce visual complexity -- they reduce **computational** complexity across every system:

| System | Near (L0) | Mid (L1) | Far (L2) | Culled |
|--------|-----------|----------|----------|--------|
| **Physics** | 60 Hz, full CCD | 30 Hz, discrete | 15 Hz, broadphase only | 0 Hz |
| **AI decisions** | 10 Hz, full behavior tree | 5 Hz, state machine | 0 Hz, flow-field | 0 Hz |
| **Animation** | Full skeleton (65 bones), blend tree | Reduced skeleton (32 bones), walk/idle | Billboard rotation | None |
| **Sensor processing** | Full sensor suite, per-frame | Reduced sensors, 5 Hz | No sensors | No sensors |
| **Event subscription** | All tiers (0-4) | Tiers 2-4 only | Tier 4 only | None |
| **Collision response** | Full response, callbacks | Simplified, no callbacks | None | None |

### 6.2 Compute Cost Per Entity by LOD

| LOD | CPU Cost Per Entity Per Frame | Memory Per Entity |
|-----|------------------------------|-------------------|
| L0 (Near) | ~0.15 ms | ~12 KB (full state, sensor buffers, memory graph) |
| L1 (Mid) | ~0.03 ms | ~4 KB (reduced state, no sensor buffers) |
| L2 (Far) | ~0.005 ms | ~0.5 KB (position, velocity, archetype ID) |
| Culled | ~0 ms | ~0.1 KB (existence record only) |

### 6.3 Entity Budget Formulas

Given the per-frame CPU budgets from Part 10:

```
NPC budget:
  Background NPC budget: 2.0 ms/frame
  Hero NPC budget:       3.0 ms/frame
  Total NPC budget:      5.0 ms/frame

Maximum entity counts by LOD distribution:

  Scenario A (5 blocks, Times Square only):
    L0: 50 NPCs * 0.15 ms  = 7.5 ms  -- OVER BUDGET
    Need: cap L0 at 33 NPCs (33 * 0.15 = 4.95 ms)
    L1: 200 NPCs * 0.03 ms = 6.0 ms  -- separate thread pool
    L2: 500 NPCs * 0.005 ms = 2.5 ms -- batched on worker
    Total visible: ~733 NPCs

  Scenario B (17 blocks, Ring 0+1):
    Active blocks (loaded, simulated): ~5-7 (near player)
    Dormant blocks: ~10-12 (state preserved, no tick)
    L0: 33 NPCs * 0.15 ms  = 4.95 ms  (same cap)
    L1: 300 NPCs * 0.03 ms = 9.0 ms   (2 AI threads)
    L2: 800 NPCs * 0.005 ms = 4.0 ms  (worker pool)
    Total visible: ~1133 NPCs

  Scenario C (100 blocks, full Midtown):
    Active blocks: ~5-9 (near player)
    Dormant blocks: ~91-95 (zero cost)
    L0: 33 NPCs * 0.15 ms  = 4.95 ms  (same cap -- locality!)
    L1: 500 NPCs * 0.03 ms = 15.0 ms  (4 AI threads)
    L2: 2000 NPCs * 0.005 ms = 10.0 ms (worker pool)
    Total visible: ~2533 NPCs

Key insight: L0 count is CONSTANT regardless of world size.
L1 and L2 grow linearly but run on parallel threads.
```

---

## 7. Memory Budget Scaling

### 7.1 Per-Block Memory Budget

| Category | Per Block | Notes |
|----------|-----------|-------|
| Collision meshes | 8 MB | Simplified geometry; shared materials |
| NavMesh | 4 MB | Recast/Detour format |
| Visual geometry (L0) | 60 MB | Hero buildings, unique props |
| Visual geometry (L1) | 15 MB | Instanced motifs, simplified |
| Visual geometry (L2) | 3 MB | Silhouettes, impostors |
| Textures (streamed) | 80 MB | BC7/BC5 compressed; shared atlases |
| NPC state (800 entities) | 6 MB | Full state for L0/L1; minimal for L2 |
| IoT artifact state | 1 MB | 50 artifacts per block |
| Audio samples | 5 MB | Per-block ambient; shared kit |
| **Total per block (loaded)** | **~182 MB** | |
| **Total per block (dormant)** | **~2 MB** | Entity existence records + block aggregate only |

### 7.2 Memory Scaling Table

| World Size | Loaded Blocks | Dormant Blocks | Active Memory | Dormant Memory | Total |
|-----------|---------------|----------------|---------------|----------------|-------|
| 5 blocks (Ring 0) | 5 | 0 | 910 MB | 0 | **910 MB** |
| 17 blocks (Ring 0+1) | 7 | 10 | 1,274 MB | 20 MB | **1,294 MB** |
| 41 blocks (Ring 0-2) | 9 | 32 | 1,638 MB | 64 MB | **1,702 MB** |
| 100 blocks (Midtown) | 9 | 91 | 1,638 MB | 182 MB | **1,820 MB** |
| 500 blocks (Manhattan) | 9 | 491 | 1,638 MB | 982 MB | **2,620 MB** |

**Key insight:** Active memory is bounded by the number of simultaneously loaded blocks (max ~9), which is constant regardless of total world size. Dormant memory grows linearly but is small (~2 MB/block).

### 7.3 Memory Budget Ceiling

| Resource | Budget | Headroom |
|----------|--------|----------|
| Total RAM | 16 GB (minimum spec) | |
| OS + drivers | 2 GB | |
| Engine overhead | 2 GB | |
| Render targets + GPU readback | 1.5 GB | |
| Available for game data | **10.5 GB** | |
| Active blocks (9 max) | 1,638 MB | |
| Dormant blocks (at 500) | 982 MB | |
| Ledger database | 500 MB (soft cap) | |
| Audio engine | 256 MB | |
| UI + HUD | 64 MB | |
| Streaming buffers (double-buffer) | 364 MB | |
| **Total game data** | **~3,804 MB** | **~6,696 MB headroom** |

---

## 8. Tick Budget Scaling

### 8.1 Per-Frame Tick Budget by System

All times assume 60 fps target (16.6 ms frame budget) with multi-threading:

| System | 5 Blocks | 17 Blocks | 100 Blocks | Scaling Law | Thread |
|--------|----------|-----------|------------|-------------|--------|
| Rendering submission | 4.0 ms | 4.0 ms | 4.0 ms | O(1) -- frustum-culled | Main |
| Physics (active entities) | 4.0 ms | 4.0 ms | 4.0 ms | O(1) -- locality-bounded | Physics |
| NPC AI (L0, hero) | 3.0 ms | 3.0 ms | 3.0 ms | O(1) -- capped at 33 L0 NPCs | AI pool |
| NPC AI (L1, background) | 2.0 ms | 3.0 ms | 5.0 ms | O(B_active) -- linear in loaded blocks | AI pool |
| Traffic logic | 1.0 ms | 1.2 ms | 1.5 ms | O(B_active) -- 2 Hz amortized | AI pool |
| Show Director | 0.5 ms | 0.6 ms | 0.8 ms | O(log N) -- spatial index | Worker |
| Event bus | 0.5 ms | 0.6 ms | 0.8 ms | O(E) -- linear in events/frame, locality-bounded | Worker |
| Ledger commits | 0.2 ms | 0.2 ms | 0.2 ms | O(1) -- async queue | Ledger |
| Audio | 1.5 ms | 1.5 ms | 1.5 ms | O(1) -- priority-sorted, capped sources | Audio |
| Animation | 2.0 ms | 2.5 ms | 3.0 ms | O(B_active) -- skeleton count grows with loaded blocks | Worker |
| Streaming | 0.5 ms | 0.5 ms | 0.5 ms | O(1) -- async I/O | Streaming |
| Block aggregation | 0.0 ms | 0.1 ms | 0.2 ms | O(B_total) -- 1 Hz, amortized | Worker |
| **Main thread total** | **~4.5 ms** | **~4.5 ms** | **~4.5 ms** | **O(1)** | |
| **Parallel total** | **~15.2 ms** | **~17.2 ms** | **~20.5 ms** | **~O(B_active)** | |

### 8.2 Thread Utilization at Scale

```
THREAD UTILIZATION (100 blocks, worst case):

  Main thread:     [Render 4.0ms][Game 0.5ms]              = 4.5ms  (27% utilized)
  Physics thread:  [PhysX  4.0ms]                          = 4.0ms  (24% utilized)
  AI thread 1:     [Hero AI 3.0ms]                         = 3.0ms  (18% utilized)
  AI thread 2:     [Background AI 2.5ms][Traffic 0.8ms]    = 3.3ms  (20% utilized)
  AI thread 3:     [Background AI 2.5ms]                   = 2.5ms  (15% utilized)
  Audio thread:    [Audio mix 1.5ms]                       = 1.5ms  (9% utilized)
  Worker 1:        [Animation 3.0ms]                       = 3.0ms  (18% utilized)
  Worker 2:        [Show Dir 0.8ms][Events 0.8ms][Agg 0.2] = 1.8ms  (11% utilized)
  Streaming:       [Async I/O, non-blocking]               = N/A

  Critical path: Main thread at 4.5ms -> fits in 16.6ms budget.
  All parallel work completes within 4.5ms window.
```

---

## 9. System Coupling Limits

### 9.1 Maximum Allowed Coupling

| System A | System B | Allowed Coupling | Forbidden Coupling |
|----------|----------|-----------------|-------------------|
| NPC AI | Physics | NPC reads own collision results | NPC queries physics state of distant NPCs |
| NPC AI | Event bus | NPC subscribes to cell-local + block-local events | NPC subscribes to global events (except Tier 4) |
| Show Director | All systems | Director reads entity positions, sets LOD tier | Director modifies entity behavior or state |
| Heat system | NPC AI | NPC reads block-aggregate Heat | NPC reads Heat of individual distant entities |
| Ledger | Event bus | Ledger subscribes to committed events | Ledger blocks event bus processing while writing |
| Streaming | All systems | Streaming loads/unloads block data | Streaming modifies active block state during load |
| Traffic | NPC AI | Traffic signals read by NPC via event bus | Traffic system directly modifies NPC paths |

### 9.2 Coupling Violation Detection

A nightly CI job runs a **coupling audit** that:

1. Instruments all cross-system function calls
2. Records caller system, callee system, and data accessed
3. Compares against the allowed coupling matrix (Section 9.1)
4. Flags any call that accesses data outside the allowed coupling

Violations are logged as P1 bugs and must be resolved before milestone.

---

## 10. Scaling Formulas Reference

```
ENTITY COUNT:
  E(B) = 200 + 800 * B
  where B = total blocks

ACTIVE ENTITY COUNT:
  E_active(B_loaded) = 200 + 800 * B_loaded
  where B_loaded = min(B, 9)  (at most 9 blocks loaded)

MEMORY (MB):
  M(B) = 182 * min(B, 9) + 2 * max(B - 9, 0) + 820
  where 820 = fixed overhead (engine, OS, render targets, UI, audio, ledger)

TICK TIME (ms, main thread):
  T_main(B) = 4.5  (constant -- frustum-bounded)

TICK TIME (ms, parallel worst-case):
  T_parallel(B_loaded) = 12.0 + 1.0 * B_loaded
  (scales with loaded blocks but runs on parallel threads)

EVENT BUS THROUGHPUT (events/s):
  R_events(B_loaded) = 50 * B_loaded  (Tier 2 events)
  Budget ceiling: 2000 Tier 2 events/s

LEDGER QUERY TIME (ms):
  T_query = O(log(N_events))  (B-tree indexed)
  At 1M events: ~3 ms
  At 10M events: ~5 ms

STREAMING LOAD TIME (ms per block):
  T_load = 500 ms  (constant -- NVMe I/O bounded, not world-size bounded)
```

---

## 11. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1.0 | 2026-01-27 | Design Team | Initial draft -- locality rules, aggregation hierarchy, event escalation, budget formulas |

---

*End of Computational Scaling Spec v0*
