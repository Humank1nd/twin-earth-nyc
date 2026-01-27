# Scaling Doctrine v0

**Twin Earth NYC -- Part 13: Scaling Strategy and Risk Control**
**Document:** Scaling Doctrine -- Minimum Viable Manhattan
**Version:** 0.1.0
**Status:** Draft
**Last Updated:** 2026-01-27

---

## 1. Purpose

This document establishes the scaling philosophy for Twin Earth NYC: how the world grows from a five-block vertical slice to a full Manhattan simulation without ever breaking what already works. Every expansion decision flows from a single principle: **build the smallest Manhattan that can hold a portal, then grow by addition -- never by rewrite.**

---

## 2. The Portal Threshold Principle

### 2.1 Definition

> **"The smallest world that can hold a portal"** is the minimum contiguous geometry, simulation depth, and system coverage required for a player to experience the full anomaly-to-portal-to-exfil gameplay loop with every system operational.

This is not an abstract concept. It is a measurable engineering target:

| Requirement | Minimum | Why |
|-------------|---------|-----|
| Contiguous walkable area | 5 city blocks (~0.08 km2) | Player must be able to approach, observe, and flee an anomaly with room for NPC crowd reaction, authority response, and evidence accumulation |
| Street topology | At least 1 avenue + 1 diagonal + 3 cross-streets | Portal gameplay requires sightlines, escape routes, and crowd flow patterns that only emerge from a real intersection network |
| Landmark anchors | >= 3 recognizable structures | Player orientation requires triangulation; fewer than 3 landmarks and "where am I?" becomes unanswerable |
| NPC population | >= 500 background + 10 hero | Crowd reaction to anomaly requires visible density; hero NPCs provide narrative anchoring |
| IoT sensor coverage | >= 12 traffic signals, >= 18 CCTV, >= 25 doors | Evidence generation requires overlapping sensor fields; fewer than this and the ledger feels empty |
| Heat system headroom | 4 channels, full decay model | Portal events must generate, propagate, and decay Heat across all channels to prove persistence |
| Skyline silhouette | >= 5 recognizable buildings at distance | "This is New York" feeling requires iconic outlines visible from street level |

The Times Square bowtie (42nd to 47th, Broadway to 7th Avenue) meets every threshold. It is the portal-minimum world.

### 2.2 Why Not Smaller?

A single block cannot hold a portal because:

- No sightline depth for anomaly discovery (player would see the shimmer immediately -- no search, no tension)
- No room for crowd displacement (500 NPCs in one block is a mosh pit, not a city)
- No authority routing distance (police arrive instantly -- no escalation curve)
- No escape topology (one block has at most 4 exits -- trivially blockable)

A two-block corridor would technically fit the anomaly loop but fails the orientation test: without a diagonal or intersection, the player cannot distinguish "north" from "south" by landmarks alone.

### 2.3 Why Not Larger?

Starting larger than the bowtie violates the doctrine's second principle: **every block must be fully operational before the next block begins.** A 20-block initial scope means 20 blocks of partial functionality, 20 sets of incomplete seams, and 20 opportunities for systemic coupling bugs that only manifest at scale. The bowtie is the proof. Everything after it is expansion.

---

## 3. Growth-by-Addition, Never Growth-by-Rewrite

### 3.1 The Doctrine

Every expansion of Twin Earth NYC must satisfy the **Addition Test**:

> Can this new block/system/feature be added to the existing world without modifying any file, schema, or runtime behavior of the blocks and systems that are already shipping?

If the answer is no, the expansion is rejected until it can be reformulated as an addition.

### 3.2 What Addition Means in Practice

| Operation | Addition (Allowed) | Rewrite (Forbidden) |
|-----------|-------------------|---------------------|
| Add a new city block | New assets, new collision, new navmesh, new IoT artifacts -- all in new files. Existing blocks unchanged. | Modifying existing block geometry to "make room" for the new block. Changing global coordinate systems. |
| Extend the subway | New subway segment loaded behind a seam. New navmesh region stitched at boundary. | Restructuring the entire streaming architecture to accommodate underground layers. |
| Add a new NPC archetype | New behavior tree, new mesh, new sensor loadout -- registered in the archetype registry. | Modifying the base NPC class to add fields that all existing NPCs must now carry. |
| Increase crowd capacity | Tune the LOD impostor threshold; add more impostor variants to the pool. | Rewriting the crowd simulation algorithm. Changing the NPC tick rate contract. |
| Add a new Heat channel | Register new channel in Heat system; existing channels unmodified. | Changing the decay formula that existing channels use. |

### 3.3 The Seam Contract

When a new block connects to an existing block, the connection point is a **seam**. Seams obey strict contracts (see Part 9, Backstage Map):

```
SEAM CONTRACT:
  1. Collision mesh gap at boundary: < 1 cm
  2. NavMesh stitch: bidirectional, 0 stuck agents on 3 test paths
  3. Visual continuity: no visible pop at player height
  4. LOD consistency: transition distances within 5 m of neighbor
  5. Lighting gradient: smooth across boundary (no hard cut)
  6. Event bus: artifacts on both sides of seam publish to same topics
  7. Streaming: new block loads without affecting old block's frame time
```

If a seam cannot meet these seven criteria, the new block is not ready for integration.

### 3.4 The Rollback Guarantee

Every block expansion ships with a **rollback manifest** -- a list of every file added, every registry entry created, and every seam connection established. If the new block causes regression in any existing block's integration tests, the rollback manifest allows complete removal within one build cycle. The world returns to its previous state with zero data loss.

---

## 4. Growth Geometry

### 4.1 Concentric Ring Model

Expansion radiates outward from the Times Square bowtie in concentric rings. Each ring adds one layer of blocks around the existing world.

```
RING 0 (Launch):  Times Square bowtie
                  42nd-47th, Broadway-7th Ave
                  ~5 blocks, ~0.08 km2

RING 1 (Q+1):    Adjacent blocks on all 4 sides
                  41st-48th, 6th Ave to 8th Ave
                  ~12 new blocks, ~0.24 km2 cumulative

RING 2 (Q+2):    Second-layer expansion
                  39th-50th, 5th Ave to 9th Ave
                  ~24 new blocks, ~0.60 km2 cumulative

RING 3 (Q+3):    Theater District + Bryant Park + Port Authority
                  34th-53rd, 5th Ave to 10th Ave
                  ~40 new blocks, ~1.2 km2 cumulative

RING 4+ (Q+4+):  Midtown complete + expansion corridors
                  Subway connections to other neighborhoods
                  ~100+ blocks, ~3.0+ km2 cumulative
```

### 4.2 Ring Readiness Criteria

A ring is ready for production when:

| Criterion | Gate |
|-----------|------|
| All blocks in previous ring pass Phase 5 integration (Part 10 SOP) | Hard gate |
| Seam tests between previous ring and new ring pass at all boundary points | Hard gate |
| Performance budget holds with previous ring fully loaded + new ring streaming | Hard gate |
| Skyline silhouette regression passes with new ring geometry added | Hard gate |
| At least one portal gameplay loop tested in the new ring | Soft gate (may be deferred to mid-ring) |

---

## 5. Anti-Rewrite Safeguards

### 5.1 Schema Stability Rules

| System | Stability Rule |
|--------|---------------|
| Trust Ledger schema | Append-only columns. New fields added with DEFAULT values. Existing columns never renamed or retyped. |
| Entity ID format | `ENT_<type>_<region>_<hash>` is permanent. New regions get new codes; existing codes never change. |
| Event bus topics | New topics may be added. Existing topic names and payload schemas are frozen after first subscriber ships. |
| Performance budget | Per-block budgets are independent. Adding blocks does not reduce the budget of existing blocks. Global budget grows linearly with loaded block count. |
| Coordinate system | ENU origin at Times Square center is permanent. Floating-origin rebase threshold (5 km) accommodates full-Manhattan expansion without change. |
| Asset Ladder rungs | The 5-rung hierarchy is fixed. New asset types slot into existing rungs; no new rungs may be added without a major version bump. |

### 5.2 Interface Freezing Schedule

| Interface | Freeze Point | After Freeze |
|-----------|-------------|--------------|
| Block Intake SOP (Part 10) | Ring 0 ship | New blocks follow the same 5-phase pipeline. Pipeline steps may be refined but not restructured. |
| Show Director distance bands | Ring 0 ship | Near/Mid/Far thresholds are fixed. Per-entity overrides are allowed; global band definitions are not. |
| NPC sensor contract | Ring 0 ship | Sensor types, FOV ranges, and noise models are frozen. New sensors may be added; existing sensors may not change behavior. |
| Heat channel decay formulas | Ring 0 ship | Decay constants may be tuned via AlphaEvolve (Part 5). Formula structure is frozen. |
| Seam contract (7 criteria) | Ring 0 ship | Criteria may be tightened (stricter tolerance) but never loosened. |

---

## 6. Growth Cost Model

### 6.1 Per-Block Cost Estimates

| Cost Category | Ring 0 Block | Ring 1 Block | Ring 2+ Block | Notes |
|---------------|-------------|-------------|---------------|-------|
| Skeleton import (Phase 1) | 0.5 days | 0.5 days | 0.5 days | Cesium pipeline is amortized |
| Collision + Nav (Phase 2) | 2 days | 1.5 days | 1 day | Tooling improves; standard grid blocks are faster |
| Visual capture (Phase 3) | 2 days | 1.5 days | 1 day | Capture rig workflow matures |
| Detail pass (Phase 4) | 3 days | 2 days | 1.5 days | Kit library grows; less bespoke work per block |
| Integration + Test (Phase 5) | 1 day | 1 day | 1 day | Automated test suite coverage increases |
| **Total per block** | **8.5 days** | **6.5 days** | **5 days** | Amortization assumes stable SOP |

### 6.2 Cost Scaling Law

```
Total effort for N blocks (approximate):

  E(N) = E_ring0 + sum_{i=1}^{N-5} C_block(ring(i))

  where:
    E_ring0       = ~42.5 person-days (5 blocks x 8.5 days)
    C_block(r)    = 8.5 * (0.85 ^ min(r, 3)) person-days
                    (15% efficiency gain per ring, capped at Ring 3)

  Examples:
    17 blocks (Ring 0+1):  ~42.5 + 12 * 6.5 = ~120.5 person-days
    41 blocks (Ring 0-2):  ~120.5 + 24 * 5.0 = ~240.5 person-days
```

### 6.3 What Growth Does NOT Cost

Because the doctrine prohibits rewrite, the following costs are **zero** during expansion:

- Refactoring existing block geometry
- Migrating ledger data to new schemas
- Rewriting event bus topic structures
- Re-tuning Heat channels for existing blocks
- Rebuilding the Show Director's core loop

If any of these costs appear in an expansion estimate, the expansion plan violates the doctrine and must be reformulated.

---

## 7. Decision Framework

When evaluating any scaling proposal, apply these questions in order:

```
SCALING DECISION TREE:

  1. Does this proposal modify any shipped block?
     YES -> REJECT. Reformulate as addition.
     NO  -> Continue.

  2. Does this proposal modify any frozen interface?
     YES -> REJECT. Design an adapter or extension instead.
     NO  -> Continue.

  3. Does this proposal increase coupling between blocks?
     YES -> REJECT. Blocks must remain independently testable.
     NO  -> Continue.

  4. Does this proposal fit within the per-block performance budget?
     YES -> Continue.
     NO  -> Can it be made to fit via LOD/streaming adjustments?
            YES -> Continue with budget trade documentation.
            NO  -> REJECT. Block is too expensive.

  5. Does a rollback manifest exist?
     YES -> APPROVE for integration testing.
     NO  -> Create rollback manifest first.
```

---

## 8. Scaling Anti-Patterns

| Anti-Pattern | Description | Why It Fails | Correct Approach |
|-------------|-------------|--------------|------------------|
| **Big Bang Expansion** | "Let's build 50 blocks at once and integrate them all in one milestone" | Coupling bugs multiply combinatorially. Integration testing becomes intractable. | One ring at a time. Each ring fully integrated before the next begins. |
| **Retroactive Polish** | "We'll go back and redo Ring 0 blocks once we've learned from Ring 2" | Violates no-rewrite doctrine. Creates regression risk in the most-tested, most-trusted part of the world. | Polish fixes are patches, not rewrites. They follow the same addition rules. |
| **Global Tuning** | "Let's change the crowd density formula to work better across 40 blocks" | Changes behavior of all existing blocks simultaneously. Regression surface is the entire world. | Per-block density overrides. Global formula is frozen; local parameters are tunable. |
| **Shared Mutable State** | "All blocks read from a single global NPC pool" | Adding blocks increases contention on the pool. Performance degrades non-linearly. | Per-block NPC pools with a lightweight cross-block migration protocol. |
| **Premature Subway** | "Build the full subway network before the surface is done" | Underground is a second world with its own LOD, streaming, and crowd problems. Building both simultaneously doubles scope. | Surface first. Subway stubs at seams (Part 9, S06). Full subway is a Ring 3+ expansion. |

---

## 9. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1.0 | 2026-01-27 | Design Team | Initial draft -- portal threshold, growth-by-addition doctrine, ring model, cost estimates |

---

*End of Scaling Doctrine v0*
