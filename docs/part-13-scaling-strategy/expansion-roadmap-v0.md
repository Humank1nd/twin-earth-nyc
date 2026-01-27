# Expansion Roadmap v0

**Twin Earth NYC -- Part 13: Scaling Strategy and Risk Control**
**Document:** Block-by-Block Growth Plan and Subway Streaming Network
**Version:** 0.1.0
**Status:** Draft
**Last Updated:** 2026-01-27

---

## 1. Purpose

This document defines the expansion plan for Twin Earth NYC: the order in which city blocks are built and unlocked, the subway system's role as a backstage streaming network, how each new block inherits the Block Intake SOP from Part 10, the risk registry for scaling failures, and the milestone gates that must be passed before each expansion ring proceeds.

---

## 2. Expansion Philosophy

### 2.1 Core Principle

> **Grow outward from the portal.** Every new block must be justified by a gameplay or narrative reason -- not by map completionism. The world expands because the player's story demands more territory, not because the production schedule says "build 20 blocks this quarter."

### 2.2 Expansion Triggers

A new ring of blocks enters production only when one of these triggers fires:

| Trigger | Description | Example |
|---------|-------------|---------|
| **Narrative pull** | The story requires the player to travel to a location outside the current boundary | A mission requires visiting Bryant Park (3 blocks east of Ring 0) |
| **Portal geography** | A new portal type requires spatial conditions not available in existing blocks | A portal that forms only in a park (no parks in Ring 0) or on a waterfront |
| **System maturity** | A simulation system (e.g., subway, weather, district-scale events) needs more geography to function meaningfully | The subway system needs at least 3 connected stations to demonstrate network behavior |
| **Player exploration pressure** | Telemetry shows players consistently walking into seam barriers, indicating demand for more world | 40%+ of sessions include the player pressing against a Ring 0 boundary for > 30 seconds |

### 2.3 What Never Triggers Expansion

- Marketing requests for "bigger map" without gameplay justification
- Competitor feature parity ("Game X has 50 km^2, so we need 50 km^2")
- Art team availability ("We have spare artists, let's build more blocks")
- Technology demos ("We can render 200 blocks, so let's build 200 blocks")

---

## 3. District Unlock Order

### 3.1 Growth Map

```
EXPANSION RINGS -- PLAN VIEW (SCHEMATIC):

                        NORTH
                          |
    +---------+-----------+-----------+---------+
    |         |           |           |         |
    |  R3     |    R2     |    R2     |   R3    |
    |  Hell's |  W 50s    |  E 50s   |  Turtle |
    |  Kitchen|           |           |   Bay   |
    |         |           |           |         |
    +---------+-----------+-----------+---------+
    |         |           |           |         |
    |  R2     |    R1     |    R1     |   R2    |
    |  W 40s  |  NW adj   |  NE adj  |  E 40s  |
    |  8th Ave|  46-48th  |  46-48th |  6th Ave|
    +---------+-----------+-----------+---------+
    |         |     R0: TIMES SQUARE            |
    |  R1     |     42nd - 47th Street          |   R1
    |  W adj  |     Broadway - 7th Ave          |   E adj
    |  8th Ave|     THE BOWTIE                  |   6th Ave
    +---------+-----------+-----------+---------+
    |         |           |           |         |
    |  R2     |    R1     |    R1     |   R2    |
    |  W 30s  |  SW adj   |  SE adj  |  E 30s  |
    |  9th Ave|  40-42nd  |  40-42nd | 5th Ave |
    +---------+-----------+-----------+---------+
    |         |           |           |         |
    |  R3     |    R2     |    R2     |   R3    |
    |  Hudson |  Garment  | Bryant   | Murray  |
    |  Yards  |  District | Park     | Hill    |
    |         |           |           |         |
    +---------+-----------+-----------+---------+
                          |
                        SOUTH

    R0 = Ring 0 (Launch): 5 blocks
    R1 = Ring 1 (Q+1):   12 blocks
    R2 = Ring 2 (Q+2):   24 blocks
    R3 = Ring 3 (Q+3):   40 blocks
```

### 3.2 District Definitions

| District | Ring | Blocks | Distinctive Features | Gameplay Value |
|----------|------|--------|---------------------|----------------|
| **Times Square Bowtie** | 0 | 5 | Bowtie intersection, billboard canyon, TKTS steps, One Times Square | Portal ground zero. All systems proven here. |
| **Theater District North** | 1 | 3 | Broadway theaters (Minskoff, Gershwin), restaurant row | Crowd dynamics: theater crowds at showtime. NPC behavior diversity. |
| **Theater District South** | 1 | 3 | 42nd St corridor, Port Authority approach, New Amsterdam Theater | Transit hub pressure. Authority concentration. |
| **6th Avenue Corridor** | 1 | 3 | Radio City area approach, office towers, pedestrian density shift | Different crowd archetype (commuters, not tourists). |
| **8th Avenue Corridor** | 1 | 3 | Port Authority bus terminal approach, lower density, service blocks | Support infrastructure. Backstage of Times Square. |
| **Rockefeller Center** | 2 | 4 | 30 Rock, ice rink/plaza, Channel Gardens, Atlas statue | Landmark-dense. Second portal-capable zone. |
| **Bryant Park** | 2 | 4 | Park geometry, lawn, carousel, NY Public Library | First green space. Fundamentally different ground truth (grass, trees, paths vs. asphalt). |
| **Garment District** | 2 | 4 | Wholesale storefronts, rack pushers, loading docks | Industrial NPC archetypes. Commercial rhythm. |
| **Columbus Circle / Central Park South** | 2 | 4 | Circle geometry, park edge, Time Warner Center | Roundabout traffic. Park boundary as natural edge-of-world. |
| **Hell's Kitchen** | 3 | 6 | Residential density shift, restaurant row continuation, lower building heights | Scale change: Midtown canyon to low-rise neighborhood. |
| **Hudson Yards** | 3 | 6 | The Vessel, High Line terminus, mega-development glass towers | Modern architecture contrast. Elevated walkway (High Line). |
| **Murray Hill / Grand Central** | 3 | 6 | Grand Central Terminal, Met Life building, Park Avenue | Transit cathedral. Interior landmark (Grand Central main hall). |
| **Penn Station / MSG** | 3 | 6 | Madison Square Garden, Penn Station, subterranean complexity | Major transit node. Underground expansion required. |

### 3.3 Priority Rationale

Ring 1 expands along the four cardinal directions from the bowtie because:

1. **North and South** extend the primary avenues (Broadway, 7th Ave), allowing longer sightlines and more natural NPC flow
2. **East and West** connect the bowtie to the next major avenues (6th and 8th), creating the first cross-avenue navigation options
3. All Ring 1 blocks share the street grid geometry of Ring 0, minimizing novel engineering challenges

Ring 2 introduces the first **non-standard geometries**: a park (Bryant Park), a circular intersection (Columbus Circle), and a denser commercial zone (Garment District). These test the pipeline's ability to handle terrain and topology that differs from the Manhattan grid.

Ring 3 introduces **scale transitions** (midtown canyon to low-rise Hell's Kitchen), **elevated geometry** (High Line), and **major interior landmarks** (Grand Central). These are the hardest scaling challenges.

---

## 4. Per-Block SOP Inheritance

Every new block, regardless of ring, follows the Block Intake SOP defined in Part 10 (block-intake-sop-v0.md). The SOP is inherited, not copied -- meaning updates to the SOP apply to all future blocks automatically.

### 4.1 SOP Inheritance Chain

```
Part 10: Block Intake SOP v0
  |
  +-- Phase 1: Skeleton Import
  |     Inherited by: ALL new blocks
  |     Ring-specific additions:
  |       Ring 2+: Park blocks add terrain heightfield import step
  |       Ring 3+: Interior landmarks add floor-plan import step
  |
  +-- Phase 2: Collision + Navigation
  |     Inherited by: ALL new blocks
  |     Ring-specific additions:
  |       Ring 2+: Park blocks add off-grid path navmesh
  |       Ring 2+: Circle intersections add radial navmesh zones
  |       Ring 3+: Elevated walkways add multi-level navmesh stitch
  |
  +-- Phase 3: Visual Capture
  |     Inherited by: ALL new blocks
  |     No ring-specific additions (pipeline is universal)
  |
  +-- Phase 4: Detail Pass
  |     Inherited by: ALL new blocks
  |     Ring-specific additions:
  |       Ring 1+: Semantic labels include new taxonomy entries if needed
  |       Ring 2+: Park blocks add vegetation placement pass
  |       Ring 3+: Interior landmarks add interior detail pass
  |
  +-- Phase 5: Integration + Test
        Inherited by: ALL new blocks
        Ring-specific additions:
          Ring 1+: Boundary reconciliation with all adjacent completed blocks
          Ring 2+: Skyline profile regression (new geometry may alter profiles)
          Ring 3+: System coupling benchmarks (SC-01 through SC-07)
```

### 4.2 New Block Checklist (Addendum to SOP)

Before a new block enters Phase 1, the following pre-conditions must be met:

| # | Pre-condition | Verified By |
|---|--------------|-------------|
| 1 | All adjacent blocks in previous ring have passed Phase 5 | Build Pipeline Lead |
| 2 | Block bounds polygon defined and checked for overlap with all existing blocks | Geo Team |
| 3 | Block assigned to a fidelity tier (T1, T2, or T3) | Design Lead |
| 4 | Streaming seam masks identified for all boundary edges | Show Director Team |
| 5 | Performance budget allocated (must fit within ring budget from performance-design-spec) | Performance Lead |
| 6 | Rollback manifest template created (empty; populated during build) | Build Pipeline Lead |

---

## 5. Subway as Backstage Streaming Network

### 5.1 Concept

The NYC subway system serves two functions in Twin Earth NYC:

1. **Diegetic fast-travel:** The player enters a subway station, boards a train, and exits at another station. This is a gameplay feature.
2. **Backstage streaming corridor:** The underground transit between stations is a loading zone. While the player is "on the train," the engine streams out the departure neighborhood and streams in the destination neighborhood.

The subway is not a fully simulated underground world. It is a **streaming tunnel disguised as a train ride.**

### 5.2 Subway Architecture

```
SUBWAY CROSS-SECTION (SCHEMATIC):

  SURFACE (Show Street)
  ========================== ground level ==========================
        |                                                    |
        |   STATION A                           STATION B    |
        |   (entrance)                          (entrance)   |
        |       |                                   |        |
  ------+-------+-----------------------------------+--------+------
        |  mezzanine (ticket, turnstile)    mezzanine        |
  ------+-------+-----------------------------------+--------+------
        |       |                                   |        |
        | platform                              platform     |
        |    +========= TUNNEL ==================+           |
        |    |  (streaming corridor: low-detail   |          |
        |    |   tube geometry, no simulation,    |          |
        |    |   loading happens here)            |          |
        |    +====================================+          |
        |                                                    |
  ======== bedrock (no geometry below) ==========================
```

### 5.3 Station Types

| Type | Geometry | Simulation | Player Experience | Streaming Role |
|------|----------|-----------|-------------------|---------------|
| **Active Station** | Full platform, mezzanine, turnstiles, exits | NPCs wait on platform, trains arrive on schedule, PA announcements | Complete subway station experience | Entry/exit point for streaming corridor |
| **Express Station** | Simplified platform, no mezzanine detail | No NPC simulation, pre-rendered crowd on platform | Player sees platform through train window but cannot exit | Pass-through loading zone |
| **Stub Station** | Stairs descend to locked turnstile | No underground simulation | "Service Suspended" signage (Part 9, S06) | Future expansion point |

### 5.4 Streaming During Transit

```
SUBWAY STREAMING SEQUENCE:

  T+0s:    Player enters Station A. Surface blocks around A remain loaded.
  T+5s:    Player passes through turnstile, descends to platform.
           Engine begins pre-loading Station B surface blocks (T2 fidelity).
  T+15s:   Train arrives. Player boards.
           Tunnel geometry loads (minimal: cylinder + track + lighting).
  T+20s:   Train departs. Doors close.
           Station A surface blocks begin unloading (farthest first).
  T+25s:   Train enters tunnel. Player sees tunnel walls, dim lighting.
           Station A fully unloaded. Station B blocks loading at T1 fidelity.
  T+45s:   Train passes Express Station (if any). Player sees platform briefly.
           Station B T1 blocks ~50% loaded.
  T+60s:   Train arrives at Station B. Doors open.
           Station B fully loaded. Player exits to surface.
  T+65s:   Player emerges at Station B. Full T1 experience.

  TOTAL TRANSIT TIME: ~60-90 seconds (adjustable per line)
  LOADING WINDOW:     ~40-60 seconds of masked streaming time
  MINIMUM TRANSIT:    45 seconds (hard floor -- engine needs this much time)
```

### 5.5 Subway Lines (Planned)

| Line | Stations in Scope (Ring 0-3) | Purpose |
|------|------------------------------|---------|
| **1/2/3** (7th Ave line) | Times Sq-42nd, 50th St, Penn Station-34th | Primary north-south travel |
| **N/Q/R/W** (Broadway line) | Times Sq-42nd, 49th St, 34th-Herald Sq | Broadway corridor |
| **7** (Flushing line) | Times Sq-42nd, Hudson Yards-34th | East-west crosstown + Hudson Yards |
| **B/D/F/M** (6th Ave line) | 42nd-Bryant Park, 47-50th-Rockefeller | 6th Avenue corridor |
| **S** (42nd St shuttle) | Times Sq-42nd, Grand Central-42nd | East-west express (2 stops) |

### 5.6 Subway Implementation Phases

| Phase | Ring | Scope | Stations |
|-------|------|-------|----------|
| **Sub-0** | 0 | Stub stations only. Stairs to locked turnstile. No underground. | Times Sq-42nd (all entrances) |
| **Sub-1** | 1 | One active line (1/2/3). Times Sq station fully modeled. 50th St as express station. | Times Sq (active), 50th St (express) |
| **Sub-2** | 2 | Two active lines. Transfer between 1/2/3 and N/Q/R/W at Times Sq. Bryant Park station. | +49th St (active), +Bryant Park (active) |
| **Sub-3** | 3 | Four lines. Grand Central, Penn Station, Hudson Yards all active. | +Grand Central, +Penn Station, +Hudson Yards, +Rockefeller |

---

## 6. Risk Registry

### 6.1 Scaling Risks

| ID | Risk | Likelihood | Impact | Mitigation | Contingency |
|----|------|-----------|--------|------------|-------------|
| SR-01 | **Seam accumulation:** Each ring adds more boundary seams, increasing the chance of seam failures and visual artifacts | High | Medium | Seam budget (max 10 active per Part 9). Automated seam testing in CI. | Emergency "Area Closed" barriers (always resident in memory). |
| SR-02 | **Memory fragmentation:** Frequent block load/unload cycles cause memory fragmentation, leading to allocation failures | Medium | High | Pre-allocated block memory pools. Defragmentation pass during subway transit. | Reduce loaded block count. Force GC during diegetic masks. |
| SR-03 | **NPC population explosion:** More blocks means more NPCs, exceeding AI tick budget | High | High | Strict per-block NPC caps. LOD-based compute savings. L0 NPC count capped at 33 globally. | Emergency crowd density reduction (Part 10, measure 2). |
| SR-04 | **Event bus congestion:** More IoT artifacts means higher event throughput, exceeding 0.5 ms bus budget | Medium | Medium | Event locality tiers (Tier 0-4). Most events stay cell-local or block-local. | Event throttling: drop lowest-severity events first. |
| SR-05 | **Ledger growth:** More blocks and more play time means ledger database grows past 1 GB hard cap | Medium | Medium | Retention policies (Part 2). Micro-observations decay after 1 hr sim-time. Pursuit details summarized after 24 hr. | Ledger compaction pass. Archive oldest events to cold storage file. |
| SR-06 | **Skyline regression:** New block geometry alters landmark silhouettes or skyline profiles visible from existing vantage points | Medium | High | Automated skyline regression (Invariant Preservation Spec, Section 5.3). Every build that adds geometry runs profile comparison. | Block the expansion until silhouette is corrected. |
| SR-07 | **Streaming stall:** Player sprints across block boundaries faster than the streaming system can load content | Low | High | 35 m pre-load trigger. Diegetic stall measures (slow player near unready seam). | Emergency "Area Closed" barrier + movement speed reduction. |
| SR-08 | **Cross-block coupling:** Systems develop hidden dependencies between blocks (e.g., NPC in block A queries entity in block B directly) | Medium | High | Coupling audit (nightly CI). Allowed coupling matrix enforced. | Refactor to use block aggregates instead of direct queries. |
| SR-09 | **Subway loading time exceeds transit time:** Destination blocks fail to load before train arrives at station | Low | High | 45-second minimum transit time (hard floor). Pre-load begins when player enters station, not when train departs. | Extend train transit time dynamically ("signal delay"). |
| SR-10 | **Ring dependency deadlock:** Ring N cannot be completed because it depends on a feature planned for Ring N+1 | Low | Medium | Expansion triggers are gameplay-driven, not feature-driven. Each ring is self-contained. | Defer the dependent feature; deliver ring without it. |

### 6.2 Risk Severity Matrix

```
              IMPACT
              Low    Medium    High
LIKELIHOOD
  High        --     SR-01    SR-03
  Medium      --     SR-04    SR-02, SR-06, SR-08
              --     SR-05    --
  Low         --     SR-10    SR-07, SR-09
```

### 6.3 Risk Review Cadence

| Cadence | Action |
|---------|--------|
| Weekly | Performance Lead reviews SR-01 through SR-04 (high-frequency risks) |
| Per ring integration | Full risk registry review. All risks re-evaluated. New risks added if identified. |
| Per milestone | Risk report included in milestone sign-off documentation |

---

## 7. Milestone Gates

### 7.1 Gate Definitions

Each expansion ring must pass through four gates before the next ring enters production.

| Gate | Name | Criteria | Approver |
|------|------|----------|----------|
| **G1** | **SOP Compliance** | All blocks in the ring have passed Phase 5 of the Block Intake SOP. Zero open Phase 5 failures. | Build Pipeline Lead |
| **G2** | **Invariant Regression** | All invariants (landmark silhouette, scale anchor, skyline profile, street topology, system coupling) pass regression. Zero P0 or P1 failures. | QA Lead |
| **G3** | **Performance Gate** | All scenarios (baseline, rain, anomaly, peak crowd, worst case) meet frame rate targets with the full ring loaded. No emergency measures activate during baseline or rain scenarios. | Performance Lead |
| **G4** | **Gameplay Validation** | At least one complete portal gameplay loop (anomaly -> portal -> exfil -> aftermath) has been tested in the new ring with full system integration. Evidence appears in ledger. Heat channels respond correctly. | Design Lead |

### 7.2 Gate Sequence

```
RING EXPANSION GATE SEQUENCE:

  Previous ring: all gates passed
       |
       v
  [New ring enters production]
       |
       +-- Blocks built in parallel (Phase 1-4)
       |
       +-- Blocks integrated sequentially (Phase 5, boundary reconciliation)
       |
       v
  G1: SOP COMPLIANCE
       |  Pass -> continue
       |  Fail -> fix failing blocks, re-test
       v
  G2: INVARIANT REGRESSION
       |  Pass -> continue
       |  Fail -> identify invariant violation, fix, re-capture baselines
       v
  G3: PERFORMANCE GATE
       |  Pass -> continue
       |  Fail -> optimize, adjust tier assignments, re-profile
       v
  G4: GAMEPLAY VALIDATION
       |  Pass -> RING APPROVED. Next ring may enter production.
       |  Fail -> identify gameplay issue, fix, re-test
       v
  [Ring ships in next milestone build]
```

### 7.3 Gate Timing Targets

| Ring | Blocks | Target Duration (Production Start to G4 Pass) | Team Size |
|------|--------|-----------------------------------------------|-----------|
| Ring 0 | 5 | 8-10 weeks | 5-8 people |
| Ring 1 | 12 | 6-8 weeks | 6-10 people |
| Ring 2 | 24 | 8-12 weeks | 8-12 people |
| Ring 3 | 40 | 12-16 weeks | 10-15 people |

---

## 8. Long-Term Expansion Corridors

### 8.1 Beyond Ring 3

After Ring 3 (full Midtown), expansion follows **corridors** rather than concentric rings. Corridors are linear extensions along major transit lines:

| Corridor | Direction | Anchor | Terminus | Length | Unique Challenges |
|----------|-----------|--------|----------|--------|-------------------|
| **Broadway South** | Downtown | Herald Square | Union Square / Financial District | ~5 km | Longest sightline in Manhattan. Broadway diagonal continues. |
| **Park Avenue** | Uptown | Grand Central | Upper East Side / Museum Mile | ~3 km | Tunnel under Park Ave viaduct. Scale shift to residential. |
| **West Side** | South | Hudson Yards | Chelsea / Meatpacking / West Village | ~2 km | High Line elevated walkway. Gallery district. |
| **Central Park Edge** | North | Columbus Circle | Upper West Side | ~2 km | Park as natural boundary. Transition from urban canyon to park edge. |

### 8.2 Corridor Unlock Criteria

A corridor enters production only when:

1. The anchor district (origin end) has passed G4
2. A narrative or gameplay justification exists for the corridor destination
3. The subway line serving the corridor has at least one active station at the anchor end
4. Performance budget confirms the corridor can be supported at T2/T3 fidelity without affecting Midtown T1 performance

---

## 9. Expansion Checklist Summary

For quick reference, the complete checklist for adding a single new block:

```
PRE-PRODUCTION:
  [ ] Adjacent blocks in previous ring passed Phase 5
  [ ] Block bounds polygon defined, no overlap
  [ ] Fidelity tier assigned (T1/T2/T3)
  [ ] Streaming seam masks identified
  [ ] Performance budget allocated
  [ ] Rollback manifest template created

PRODUCTION (Part 10 SOP):
  [ ] Phase 1: Skeleton import + scale verification
  [ ] Phase 2: Collision + NavMesh + crosswalks
  [ ] Phase 3: Visual capture + splat alignment
  [ ] Phase 4: Detail pass + IoT + semantic labels + LOD chain
  [ ] Phase 5: Walk test + drive test + crowd test + regression screenshots
              + performance profile + constraint suite + human sign-off

INTEGRATION:
  [ ] Boundary reconciliation with all adjacent completed blocks
  [ ] Skyline profile regression (if block adds visible geometry)
  [ ] Scale anchor spot-check (10 anchor types)
  [ ] Event bus connectivity verified (IoT artifacts publish correctly)
  [ ] Rollback manifest populated and tested

RING GATE (when all blocks in ring complete):
  [ ] G1: SOP compliance
  [ ] G2: Invariant regression
  [ ] G3: Performance gate
  [ ] G4: Gameplay validation (portal loop in new ring)
```

---

## 10. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1.0 | 2026-01-27 | Design Team | Initial draft -- district unlock order, subway streaming, SOP inheritance, risk registry, milestone gates |

---

*End of Expansion Roadmap v0*
