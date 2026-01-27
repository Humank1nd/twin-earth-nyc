# Performance-as-Design Spec v0

**Twin Earth NYC -- Part 13: Scaling Strategy and Risk Control**
**Document:** Performance as Design Constraint -- Staged Fidelity and Show Street Economics
**Version:** 0.1.0
**Status:** Draft
**Last Updated:** 2026-01-27

---

## 1. Purpose

Performance in Twin Earth NYC is not an optimization pass that happens after features are built. Performance is a **design constraint** that shapes every feature from conception. This document defines the staged fidelity model, the economics of show-quality versus support-quality versus background-quality blocks, budget allocation across the world, and the profiling cadence that enforces these constraints throughout development.

**Rule:** If a feature cannot describe its performance cost before implementation begins, it is not ready for implementation.

---

## 2. Performance-First Design Doctrine

### 2.1 The Three Laws

| # | Law | Consequence |
|---|-----|-------------|
| 1 | **Every feature has a budget before it has a prototype.** | Feature proposals include a cost estimate (CPU ms, GPU ms, memory MB, event throughput). The estimate is reviewed by the Performance Lead before prototyping begins. |
| 2 | **No feature may borrow from another feature's budget.** | If the billboard system needs 3 ms GPU and the NPC system needs 5 ms CPU, one cannot "borrow" from the other's allocation. Budgets are per-system, enforced independently. |
| 3 | **When budget and design conflict, design adapts.** | The frame budget (16.6 ms at 60 fps) is not negotiable. If a design requires 20 ms, the design is simplified, staged, or deferred -- the budget is never raised. |

### 2.2 The Performance Review Gate

Every feature passes through a performance review before merging to main:

```
PERFORMANCE REVIEW GATE:

  1. PROPOSAL PHASE
     Feature owner submits:
       - CPU cost estimate (per-frame, per-event, per-entity)
       - GPU cost estimate (triangles, draw calls, shader complexity)
       - Memory estimate (resident, streaming, transient)
       - Scaling behavior (O(1), O(N), O(N log N), O(N^2)?)
     Performance Lead reviews and approves budget allocation.

  2. PROTOTYPE PHASE
     Feature implemented on branch.
     Profiled against budget:
       - Actual CPU <= estimated CPU * 1.2 (20% margin for measurement noise)
       - Actual GPU <= estimated GPU * 1.2
       - Actual memory <= estimated memory * 1.1
     If over budget: optimize or simplify before merge.

  3. INTEGRATION PHASE
     Feature merged to main.
     Full-scene profiling verifies:
       - Total frame time still within 16.6 ms (main thread)
       - No existing system's measured cost increased by > 5%
       - Emergency measures (Part 10) do not activate during baseline scenario

  4. SHIP PHASE
     Feature included in milestone build.
     Milestone performance report confirms:
       - All scenarios (baseline, rain, anomaly, peak crowd, worst case) meet targets
       - No regression from previous milestone
```

---

## 3. Staged Fidelity Model

### 3.1 The Three Fidelity Tiers

Every city block in Twin Earth NYC is classified into one of three fidelity tiers. The tier determines the asset quality, simulation depth, and compute allocation the block receives.

| Tier | Name | Quality Level | Use Case | Compute Cost |
|------|------|---------------|----------|-------------|
| **T1** | **Show Street** | Maximum fidelity. Unique hero assets, full physics, full AI, full sensor coverage, full IoT, full evidence generation. | Blocks the player is currently in or can reach within 10 seconds. The performance stage. | ~182 MB memory, full per-frame tick budget |
| **T2** | **Support Block** | Reduced fidelity. Instanced motif assets, simplified physics (standard tier), state-machine AI, reduced IoT (cameras only), limited evidence. | Blocks visible from show streets but not the player's current location. Structural backdrop. | ~85 MB memory, ~40% of per-frame tick budget |
| **T3** | **Background Block** | Minimal fidelity. Silhouette geometry, no physics, flow-field NPC movement, no IoT simulation, no evidence generation. | Blocks visible only as skyline or distant street depth. Pure visual fill. | ~20 MB memory, ~5% of per-frame tick budget |

### 3.2 Fidelity Tier Transition Rules

```
TIER TRANSITION RULES:

  T3 -> T2:
    Trigger: Player moves within 3 blocks of T3 block (or block enters camera frustum
             at < 300 m)
    Transition time: 2-5 seconds (streamed, masked by diegetic elements)
    Direction: Promotion

  T2 -> T1:
    Trigger: Player moves within 1 block of T2 block (or player is heading toward
             block at current velocity, ETA < 10 seconds)
    Transition time: 1-3 seconds (pre-streamed during T3->T2 if possible)
    Direction: Promotion

  T1 -> T2:
    Trigger: Player moves more than 2 blocks away from T1 block AND block exits
             camera frustum for > 5 seconds
    Transition time: Instant (no visual artifact -- block is offscreen)
    Direction: Demotion

  T2 -> T3:
    Trigger: Block is more than 4 blocks from player AND not in camera frustum
    Transition time: Instant
    Direction: Demotion

  Maximum simultaneous T1 blocks: 3 (center block + 2 adjacent)
  Maximum simultaneous T2 blocks: 8
  Maximum simultaneous T3 blocks: unlimited (memory-bounded)
```

### 3.3 Tier Content Breakdown

| Content Layer | T1 (Show Street) | T2 (Support) | T3 (Background) |
|--------------|-------------------|--------------|-----------------|
| **Building geometry** | Unique hero meshes (L0), 4K textures, parallax windows, modeled AC units, fire escapes | Instanced motif meshes (L1), 2K textures, flat windows | Silhouette meshes (L2), 1K emissive maps |
| **Street surface** | Full detail: lane markings, manhole covers, gum spots, puddle system | Lane markings, simplified surface | Flat color plane |
| **Props** | Full kit: bollards, hydrants, trash cans, newspaper boxes, vendor carts, all interactive | Reduced kit: major props only (hydrants, major bollards), non-interactive | None (or merged into building base) |
| **NPCs** | Hero NPCs (full AI, 65-bone rig, dialogue) + background crowd (500+) | Background crowd only (200, state-machine AI, 32-bone rig) | Flow-field crowd (50, billboard impostors) |
| **Vehicles** | Full traffic simulation, unique vehicle meshes, functional signals | Simplified traffic (scripted loops), instanced vehicles | Distant traffic sprites or none |
| **IoT artifacts** | Full coverage: CCTV, signals, access panels, kiosks | CCTV only (reduced update rate) | None |
| **Billboard/signage** | Full video playback (L0), accurate content | Static images (L1) | Emissive color blocks (L2) |
| **Physics** | Hero tier (60 Hz, CCD) | Standard tier (30 Hz, discrete) | None |
| **Audio** | Full 3D positioned sources, unique ambient | Reduced sources, shared ambient | Distant attenuation only |
| **Evidence generation** | Full ledger participation | Reduced (CCTV observations only) | None |

---

## 4. Show Street Economics

### 4.1 Cost Per Block by Tier

| Cost Category | T1 (Show Street) | T2 (Support) | T3 (Background) | Ratio T1:T2:T3 |
|--------------|-------------------|--------------|-----------------|----------------|
| **Asset creation (person-days)** | 8.5 | 3.5 | 0.5 | 17 : 7 : 1 |
| **Disk storage (MB)** | 450 | 120 | 15 | 30 : 8 : 1 |
| **Runtime memory (MB)** | 182 | 85 | 20 | 9 : 4 : 1 |
| **CPU per frame (ms)** | 5.0 | 2.0 | 0.25 | 20 : 8 : 1 |
| **GPU per frame (ms)** | 4.0 | 1.5 | 0.3 | 13 : 5 : 1 |
| **Triangle budget (in-view)** | 800K | 300K | 50K | 16 : 6 : 1 |
| **NPC capacity** | 500+ | 200 | 50 | 10 : 4 : 1 |
| **IoT artifacts** | 50 | 10 | 0 | -- |

### 4.2 The 3:8:N Rule

At any moment, the player experiences at most **3 show-quality blocks** surrounded by **8 support blocks** and an **unlimited number of background blocks**. This is the economic foundation of the entire rendering strategy:

```
BUDGET ALLOCATION (per frame, at 60 fps):

  GPU budget: 16.6 ms
    T1 blocks (3):  3 * 4.0 ms = 12.0 ms  (72% of GPU budget)
    T2 blocks (8):  8 * 1.5 ms = 12.0 ms  -- OVER BUDGET if sequential

    Resolution: T2 blocks share LOD pressure.
    Show Director demotes farthest T2 to T3 as needed.
    Effective T2 GPU: 8 * 0.5 ms (average, after demotion) = 4.0 ms
    T3 blocks:        ~0.6 ms total

    Total GPU: 12.0 + 4.0 + 0.6 = 16.6 ms  (budget met)

  CPU budget: 16.6 ms (main thread), parallel threads available
    T1 blocks (3):  3 * 1.5 ms (main thread share) = 4.5 ms
    T2 blocks (8):  8 * 0.3 ms = 2.4 ms
    T3 blocks:      ~0.1 ms total
    Overhead:       ~2.0 ms (game logic, UI, streaming management)

    Total main thread: 4.5 + 2.4 + 0.1 + 2.0 = 9.0 ms  (within budget)
    Parallel work: AI, physics, animation on dedicated threads (see Part 10)

  Memory budget:
    T1 blocks (3):  3 * 182 MB = 546 MB
    T2 blocks (8):  8 * 85 MB  = 680 MB
    T3 blocks (20): 20 * 20 MB = 400 MB
    Fixed overhead:              820 MB

    Total: 2,446 MB  (within 10.5 GB available)
```

### 4.3 Break-Even Analysis

How many show-quality blocks can the world sustain before hitting budget limits?

| Constraint | Limit | Show Blocks at Limit |
|-----------|-------|---------------------|
| GPU frame time (16.6 ms) | 4.0 ms per T1 block | 4 blocks (with zero T2/T3) |
| CPU main thread (16.6 ms) | 1.5 ms per T1 block (main thread share) | 9 blocks (with zero overhead -- unrealistic) |
| Memory (10.5 GB available) | 182 MB per T1 block | 57 blocks (with zero overhead -- unrealistic) |
| NPC tick budget (5 ms) | ~1.7 ms per T1 block (NPC AI) | 3 blocks (hard limit on L0 NPC count) |
| **Practical limit** | All constraints simultaneously | **3 T1 blocks** (with 8 T2 + N T3) |

---

## 5. Budget Allocation Models

### 5.1 Ring Budget Allocation

As the world grows ring by ring, the budget allocation shifts:

| Ring | Total Blocks | T1 (Active) | T2 (Loaded) | T3 (Loaded) | Dormant | Active Memory |
|------|-------------|-------------|-------------|-------------|---------|---------------|
| 0 | 5 | 3 | 2 | 0 | 0 | 716 MB |
| 0+1 | 17 | 3 | 6 | 4 | 4 | 1,136 MB |
| 0-2 | 41 | 3 | 8 | 12 | 18 | 1,546 MB |
| 0-3 | 81 | 3 | 8 | 20 | 50 | 1,946 MB |
| Full Midtown | 200 | 3 | 8 | 25 | 164 | 2,174 MB |

**Observation:** Active memory grows slowly because the number of T1 and T2 blocks is bounded. Growth in total world size primarily adds dormant blocks at ~2 MB each.

### 5.2 Scenario-Specific Budget Adjustments

| Scenario | T1 Budget Adjustment | T2 Budget Adjustment | T3 Budget Adjustment |
|----------|---------------------|---------------------|---------------------|
| Baseline midday | Standard | Standard | Standard |
| Rainy night | GPU +1 ms (SSR, wet materials); reduce T2 to 6 max | Reduce to L1 at 20 m instead of 30 m | No change |
| Anomaly event | GPU +2 ms (VFX); CPU +1 ms (evidence); reduce T1 to 2 | Reduce NPC count by 15% | Reduce to silhouette-only |
| Peak crowd (2000 visible) | GPU +3 ms (characters); L0 NPC cap raised to 50 | Background AI to 2 Hz | Billboard impostors only |
| Worst case | All adjustments combined; emergency measures active | Maximum demotion to T3 | Culled beyond 200 m |

---

## 6. Asset Tier Economics

### 6.1 Production Cost Comparison

| Work Item | T1 (per instance) | T2 (per instance) | T3 (per instance) |
|-----------|-------------------|-------------------|-------------------|
| Building model (exterior) | 3-5 days (unique, hero quality) | 0.5 days (motif instance, minor customization) | 0.1 days (silhouette extrusion from GIS footprint) |
| Texture set | 2 days (4K unique PBR) | 0.5 days (2K atlas tile selection) | 0.1 days (1K emissive bake) |
| Collision mesh | 1 day (detailed walkable surfaces) | 0.5 days (simplified box collision) | 0 (no collision) |
| Props placement | 1 day (full kit, hand-placed, interactive) | 0.3 days (major props, rule-based placement) | 0 (no props) |
| IoT setup | 0.5 days (full artifact suite, event wiring) | 0.2 days (CCTV only) | 0 (no IoT) |
| QA + integration | 1 day (full Phase 5 test suite) | 0.5 days (reduced test suite) | 0.1 days (visual check only) |
| **Total per block** | **8.5 days** | **2.5 days** | **0.3 days** |

### 6.2 World Build Cost Projection

| World Size | T1 Blocks | T2 Blocks | T3 Blocks | Total Person-Days |
|-----------|-----------|-----------|-----------|-------------------|
| Ring 0 (5 blocks) | 5 | 0 | 0 | 42.5 |
| Ring 0+1 (17 blocks) | 5 | 8 | 4 | 42.5 + 20.0 + 1.2 = **63.7** |
| Ring 0-2 (41 blocks) | 5 | 16 | 20 | 42.5 + 40.0 + 6.0 = **88.5** |
| Ring 0-3 (81 blocks) | 8 | 24 | 49 | 68.0 + 60.0 + 14.7 = **142.7** |
| Full Midtown (200 blocks) | 15 | 50 | 135 | 127.5 + 125.0 + 40.5 = **293.0** |

**Key insight:** T3 blocks are nearly free in production cost. The economic strategy is: build a small number of hero-quality show streets (T1), a moderate ring of support blocks (T2), and fill the rest of the map with T3 background at minimal cost.

---

## 7. Profiling Cadence

### 7.1 Profiling Schedule

| Cadence | What | Who | Tool | Output |
|---------|------|-----|------|--------|
| **Every commit** | Per-asset triangle count, texture size | Automated pre-commit hook | Custom validator | Pass/fail in CI |
| **Every build (nightly)** | Full-scene profiling: frame time, draw calls, memory, CPU per system | Automated build pipeline | RenderDoc, Unreal Insights, custom telemetry | Performance dashboard update |
| **Every block completion** | Block-isolated profiling: 6 performance tests from Part 10 | QA team | Engine profiler | Block performance report |
| **Weekly** | Stress scenario profiling: worst-case, peak crowd, rain+night+anomaly | Performance Lead | Full profiling suite | Weekly performance digest |
| **Every ring integration** | System coupling benchmarks (SC-01 through SC-07 from Invariant Preservation Spec) | Performance Lead + Engineering | Custom benchmark harness | Scaling report |
| **Every milestone** | Full performance report across all scenarios; comparison to previous milestone | Performance Lead | All tools | Milestone performance sign-off |

### 7.2 Profiling Targets by Development Phase

| Phase | Focus | Key Metrics | Acceptable Overhead |
|-------|-------|-------------|-------------------|
| **Pre-production** | Validate architecture can meet targets with placeholder content | Main thread < 8 ms, parallel < 12 ms, memory < 1 GB | 50% margin (targets at 50% of budget) |
| **Production (Ring 0)** | Validate slice meets targets with real content | All scenario targets from Part 10 performance-budget-v0 | 20% margin |
| **Production (Ring 1+)** | Validate scaling behavior as world grows | Scaling law compliance (O(1) main thread, O(B_active) parallel) | 10% margin |
| **Polish** | Hit exact frame rate targets under all conditions | 60 fps baseline, 30 fps worst case, zero frames below 25 fps | 0% margin (ship quality) |

### 7.3 Performance Regression Detection

```
REGRESSION DETECTION PROTOCOL:

  Nightly build captures:
    - Frame time (average, P95, P99, max) for 5-minute baseline walkthrough
    - Memory high-water mark
    - CPU time per system (average)
    - GPU time per pass (average)

  Regression is detected when:
    - Average frame time increases by > 0.5 ms vs previous build
    - P99 frame time increases by > 2.0 ms vs previous build
    - Memory high-water increases by > 50 MB vs previous build
    - Any system's CPU time increases by > 20% vs previous build

  On regression detection:
    1. Build is flagged in dashboard (yellow warning)
    2. Automated bisect identifies the commit that introduced the regression
    3. Commit author is notified with profiling diff
    4. If regression exceeds 2x threshold (1.0 ms avg, 4.0 ms P99, 100 MB memory),
       build is promoted to RED and merge-to-main is blocked for that branch
```

---

## 8. Emergency Performance Measures at Scale

The emergency measures defined in Part 10 (performance-budget-v0.md, Section: Emergency Performance Measures) remain in effect. At scale, additional measures apply:

| Priority | Measure | Trigger | Recovery |
|----------|---------|---------|----------|
| 8 | **Demote outermost T2 blocks to T3** | FPS < 35 for 10 frames AND measures 1-7 already active | FPS > 45 for 30 frames |
| 9 | **Reduce loaded block count from 9 to 7** | FPS < 30 for 10 frames AND measure 8 active | FPS > 45 for 60 frames |
| 10 | **Reduce T1 block count from 3 to 1** | FPS < 25 for 5 frames (critical) | FPS > 40 for 60 frames |

These measures are destructive to the player experience and should never activate in a shipping build under normal conditions. If they activate during QA testing, the scenario that triggered them becomes a P0 performance bug.

---

## 9. Performance Budget Trade Protocol

When a team needs more budget in one category, they must follow this protocol:

```
BUDGET TRADE REQUEST:

  1. Requestor identifies:
     - System needing additional budget
     - Amount needed (CPU ms, GPU ms, or memory MB)
     - Justification (what feature or quality improvement requires it)

  2. Requestor identifies:
     - System offering to give up equivalent budget
     - How the reduction will be achieved (LOD change, feature cut, algorithm improvement)
     - Verification method (how to confirm the budget was actually freed)

  3. Performance Lead reviews:
     - Is the trade zero-sum? (budget gained = budget freed)
     - Is the verification method sound?
     - Does the trade affect any invariant?

  4. If approved:
     - Both changes implemented in the same milestone
     - Both changes profiled together
     - Trade documented in the performance budget sheet

  5. If not zero-sum:
     - Request rejected
     - Requestor must find additional savings or simplify the feature
```

---

## 10. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1.0 | 2026-01-27 | Design Team | Initial draft -- staged fidelity, show street economics, budget allocation, profiling cadence |

---

*End of Performance-as-Design Spec v0*
