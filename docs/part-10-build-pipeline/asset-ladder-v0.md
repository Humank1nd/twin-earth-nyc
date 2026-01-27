# NYC Asset Ladder + No-Contamination Rules

> **Twin Earth NYC -- Part 10: Build Pipeline**
> Document: `asset-ladder-v0.md` | Version 0.1 | Status: Draft
> Last updated: 2026-01-27

---

## Purpose

Every piece of geometry in Twin Earth NYC exists on exactly **one rung** of the Asset Ladder at any given time. The ladder enforces a strict hierarchy of truth: higher-authority rungs are never overwritten by lower-authority data. This document defines the five rungs, the rules that prevent cross-contamination between them, and the promotion checklist required to move an asset upward.

---

## The 5-Rung Asset Ladder

| Rung | Name | Purpose | Authority Level | Editable By |
|------|------|---------|-----------------|-------------|
| **1** | **Geospatial Skeleton** | Cesium tiles / authoritative geometry -- "Where things are" (position, scale, orientation) | **TRUTH** (highest) | Geo team only |
| **2** | **Blockout Truth** | Clean collision + nav surfaces -- "What you can walk/drive on" (physics interaction) | **TRUTH** | Collision team only |
| **3** | **Photogrammetry / Gaussian Splats** | Visual capture layer -- "How it looks at high fidelity" (appearance reference) | **REFERENCE** (not truth) | Art team |
| **4** | **Derived Mesh** | Selective mesh from scans/splats -- "Where real geometry is needed for interaction" (touchable surfaces) | **TRUTH** (promoted) | Art team + collision review |
| **5** | **Procedural + Authored Detail** | Props, signage, interiors, set dressing -- "Story-ready detail and performance control" (the show layer) | **ILLUSION** | Art team + design team |

### Rung Definitions

**Rung 1 -- Geospatial Skeleton.**
The immovable bedrock. Cesium 3D Tiles, surveyed GIS data, and anchor points define where every object in the world exists in real-world coordinates. No other rung may modify position, scale, or orientation established here. All downstream data aligns to this skeleton.

**Rung 2 -- Blockout Truth.**
The physics ground truth. Simplified collision meshes for roads, sidewalks, curbs, stairs, and barriers. These surfaces are what characters walk on, what vehicles drive on, and what raycasts hit. Blockout truth is authored against the geospatial skeleton and is the sole authority for "can I stand here?"

**Rung 3 -- Photogrammetry / Gaussian Splats.**
The visual reference layer. Captured data (photogrammetry point clouds, Gaussian splats, NeRF renders) provides high-fidelity appearance information. This layer is **reference only** -- it informs art decisions but never directly becomes collision, navigation, or physics geometry.

**Rung 4 -- Derived Mesh.**
Selective extraction. When an interactive surface requires real geometry (a stoop the player climbs, a phone booth they open), artists retopologize or model from the Rung 3 reference, then submit for collision review. Once promoted, derived meshes carry TRUTH authority for their specific interaction surfaces.

**Rung 5 -- Procedural + Authored Detail.**
The show layer. Street furniture, signage, billboard content, interior set dressing, and procedurally generated props. This layer creates the illusion of a living city but never overrides the physics truth established by Rungs 2 and 4. Props snap to collision surfaces; collision surfaces never warp to accommodate props.

---

## No-Contamination Rules

These five rules are **absolute** -- no exception workflow exists. Violations trigger an automatic build gate failure.

| Rule # | Rule | Rationale |
|--------|------|-----------|
| **1** | **Splats NEVER become collision directly.** Splat geometry is visual reference only. No splat vertex, face, or point may be promoted to a collision mesh without going through the Derived Mesh (Rung 4) pipeline. | Splat geometry is noisy, inconsistent in scale, and not watertight. Direct use causes physics glitches, navigation failures, and unpredictable player interactions. |
| **2** | **Derived mesh requires explicit promotion checklist.** Every asset promoted from Rung 3 reference to Rung 4 truth must pass all applicable checklist steps (see below): scale check, collision proxy, anchor verification. | Prevents "it looks right so ship it" shortcuts that create invisible collision bugs discovered only in playtesting. |
| **3** | **Procedural detail cannot override blockout truth.** Props snap to collision surfaces, not the other way around. If a prop placement conflicts with Rung 2 geometry, the prop moves or is removed -- the collision surface is never adjusted to accommodate the prop. | Ensures that navigation and physics remain stable regardless of art iteration. Show layer changes must never break the walkable world. |
| **4** | **Generative outputs remain in `suggestive/` folder until canonicalized.** Any asset produced by AI/ML generation (texture synthesis, procedural modeling, layout optimization) is quarantined in a `suggestive/` directory. It enters the canonical asset tree only after passing the full promotion checklist and human sign-off. | Generative outputs are non-deterministic. Quarantine ensures every canonical asset has been verified against the truth hierarchy before it can affect gameplay. |
| **5** | **Each rung has its own version control branch -- no cross-contamination of source files.** Rung 1 lives in `geo/`, Rung 2 in `collision/`, Rung 3 in `capture/`, Rung 4 in `derived/`, Rung 5 in `detail/`. No single commit may modify files across multiple rung directories. | Prevents a texture artist accidentally checking in a collision change, or a geo update silently altering art assets. Cross-rung changes require separate commits with separate reviews. |

### Branch Structure

```
main/
├── geo/                  # Rung 1 -- Geospatial Skeleton
│   ├── cesium-tiles/
│   ├── anchor-sets/
│   └── origin-definitions/
├── collision/            # Rung 2 -- Blockout Truth
│   ├── road-meshes/
│   ├── sidewalk-meshes/
│   ├── barrier-meshes/
│   └── navmeshes/
├── capture/              # Rung 3 -- Photogrammetry / Splats
│   ├── splats/
│   ├── photogrammetry/
│   └── reference-renders/
├── derived/              # Rung 4 -- Derived Mesh
│   ├── hero-meshes/
│   ├── collision-proxies/
│   └── promotion-logs/
├── detail/               # Rung 5 -- Procedural + Authored Detail
│   ├── props/
│   ├── billboards/
│   ├── signage/
│   └── interiors/
└── suggestive/           # Quarantine for generative outputs
    ├── ai-textures/
    ├── ai-layouts/
    └── ai-models/
```

---

## Promotion Checklist

Every asset moving **up** the ladder (or being promoted to TRUTH authority) must pass the applicable steps below. Steps marked as "Required For" a given rung are mandatory gates -- the asset cannot be promoted without sign-off.

| Step | Description | Required For | Sign-off By | Gate Type |
|------|-------------|--------------|-------------|-----------|
| **1. Georeferenced placement** | Position verified against the geospatial anchor set. Asset origin must match Rung 1 coordinates within tolerance. | Rung 2+ | Geo team | Hard gate |
| **2. Scale verification** | Physical dimensions measured against 3 or more scale anchors (known real-world objects: doors at 2.1m, taxis at 1.5m tall, streetlights at 8m). | Rung 2+ | QA | Hard gate |
| **3. Collision proxy generated** | A simplified collision mesh has been created, tested for watertightness, and verified to match the visual silhouette within 0.1m. | Rung 2, 4 | Collision team | Hard gate |
| **4. LOD chain generated** | Near (L0), mid (L1), and far (L2) representations created. LOD transitions verified at target distances with no visible popping. | Rung 3+ | Art team | Hard gate |
| **5. Semantic labels applied** | Taxonomy classification (building, prop, vehicle, etc.) and affordance tags (walkable, climbable, destructible, etc.) applied. | Rung 2+ | Design team | Hard gate |
| **6. Physics material assigned** | Material type from the physics material table (concrete, asphalt, glass, metal, etc.) applied. Friction and restitution values verified. | Rung 2, 4 | Physics team | Hard gate |
| **7. Ledger identity assigned** | Stable entity ID assigned for any object that must persist across sessions or participate in the evidence/event system. | Rung 4, 5 (if persistent) | Systems team | Soft gate (only if persistent) |
| **8. Visual regression captured** | Baseline screenshots captured from 3 or more standardized camera positions. Screenshots stored in regression archive with timestamp and asset version. | Rung 3+ | QA | Hard gate |
| **9. Walk/drive test passed** | Automated test: NPC walks 5 paths across/around the asset; vehicle drives 1 loop. Zero snags, zero fall-throughs, zero wrong-way traversals. | Rung 2, 4 | QA | Hard gate |
| **10. Human sign-off** | Final review by discipline lead. Reviewer confirms all applicable gates passed and asset is fit for canonical inclusion. | All promotions | Discipline Lead | Hard gate |

### Promotion Record Format

Every successful promotion is logged in `derived/promotion-logs/promotions.csv`:

```csv
date,asset_id,asset_name,from_rung,to_rung,reviewer,checklist_steps_passed,notes
2026-02-15,TSQ_DRV_STOOP_042,42nd St Stoop,3,4,j.martinez,1;2;3;4;5;6;8;9;10,Retopo from splat capture batch 07
```

---

## Quick-Reference Decision Tree

```
Is the data telling you WHERE something is?
  → Rung 1 (Geo Skeleton) -- only geo team touches it.

Is the data telling you WHAT YOU CAN WALK/DRIVE ON?
  → Rung 2 (Blockout Truth) -- only collision team touches it.

Is the data telling you HOW IT LOOKS?
  → Rung 3 (Capture) -- reference only, never collision.

Does the data need to be TOUCHED or INTERACTED WITH?
  → Rung 4 (Derived Mesh) -- must pass promotion checklist.

Is the data SET DRESSING or STORY CONTENT?
  → Rung 5 (Detail) -- snaps to truth, never overrides it.

Was the data GENERATED by AI/ML?
  → suggestive/ folder -- quarantine until canonicalized.
```

---

*End of document. For questions about rung assignment or promotion, contact the Build Pipeline lead.*
