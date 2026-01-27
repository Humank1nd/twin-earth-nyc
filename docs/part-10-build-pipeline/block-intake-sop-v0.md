# Block Intake SOP -- "Times Square Block Build"

> **Twin Earth NYC -- Part 10: Build Pipeline**
> Document: `block-intake-sop-v0.md` | Version 0.1 | Status: Draft
> Last updated: 2026-01-27

---

## Purpose

This Standard Operating Procedure defines the step-by-step process for building a single city block in Twin Earth NYC, from raw geospatial import through final integration testing. Every block follows this exact pipeline. No step may be skipped. Each phase has explicit inputs, outputs, tools, and QA checks.

**Scope:** One city block (~100m x 200m), covering all five Asset Ladder rungs from skeleton through detail.

---

## Pipeline Overview

```
Phase 1          Phase 2              Phase 3           Phase 4          Phase 5
SKELETON    -->  COLLISION + NAV  --> VISUAL CAPTURE --> DETAIL PASS  --> INTEGRATION + TEST
(Rung 1)         (Rung 2)            (Rung 3)          (Rung 4 & 5)     (All Rungs)
                                                                          |
                                                                          v
                                                                    BLOCK COMPLETE
```

**Parallelization:** Phases 1--5 are sequential per block, but multiple blocks can be in different phases simultaneously. Phase 3 (visual capture) can begin as soon as Phase 1 (skeleton) is complete, running in parallel with Phase 2 (collision), provided Phase 3 outputs are not used for collision until Phase 2 is finalized.

---

## Phase 1: Skeleton Import

**Goal:** Establish the geospatial ground truth for this block.
**Rung:** 1 (Geospatial Skeleton)
**Prerequisites:** Cesium Ion tileset access, anchor set for the region, block bounds definition from the master layout.

| Step | Action | Tool | Output | QA Check |
|------|--------|------|--------|----------|
| **1.1** | Import Cesium tile region for block. Load the 3D Tiles covering the block extents plus a 20m buffer on each side. | Cesium for Unreal / Unity plugin | Raw tile geometry in engine scene | Visual inspection: tiles loaded, no gaps, no obvious corruption |
| **1.2** | Verify scale using 3 anchors. Measure at least 3 known real-world objects within the block (e.g., door height = 2.1m, taxi length = 4.9m, streetlight height = 8.0m). | In-engine ruler tool | Scale verification report (`scale_report_<block>.csv`) | All measurements within **+/- 0.5m** of real-world values |
| **1.3** | Verify north alignment. Overlay a compass rose and verify building edges align with known orientations from survey data. | Compass overlay tool | Alignment report (`alignment_report_<block>.csv`) | North alignment within **+/- 1 degree** |
| **1.4** | Verify elevation sanity. Take cross-section slices at street level and verify no surfaces are floating above or sunk below ground plane. | Cross-section visualization tool | Elevation profile (`elevation_profile_<block>.png`) | No floating surfaces; no underground geometry that should be above grade |
| **1.5** | Define block bounds polygon. Create a closed polygon that defines the exact boundary of this block, snapped to street centerlines and building edges. | Editor polygon tool | Block bounds asset (`TSQ_BLK_<id>_bounds.geojson`) | Polygon matches street layout; no overlap with adjacent block definitions |

### Phase 1 Exit Criteria

- [ ] All 5 steps completed and QA checks passed
- [ ] Scale report filed in `qa/skeleton/`
- [ ] Alignment report filed in `qa/skeleton/`
- [ ] Block bounds asset committed to `geo/bounds/`
- [ ] Skeleton import reviewed by Geo Team lead

---

## Phase 2: Collision + Navigation

**Goal:** Create the physics and navigation ground truth for walkable/drivable surfaces.
**Rung:** 2 (Blockout Truth)
**Prerequisites:** Phase 1 complete and signed off.

| Step | Action | Tool | Output | QA Check |
|------|--------|------|--------|----------|
| **2.1** | Generate road collision (simplified). Create a clean, flat collision mesh for all road surfaces within the block. Lanes should be distinguishable for traffic logic. | Collision authoring tool (ProBuilder / custom) | Road collision mesh (`TSQ_COL_ROAD_<id>_L0`) | Surface is flat within lane; correct number of lanes; lane widths match survey |
| **2.2** | Generate sidewalk collision. Create collision meshes for all sidewalks. Include correct widths (standard NYC sidewalk: 3.0--4.6m) and surface height above road (~15cm). | Collision authoring tool | Sidewalk collision mesh (`TSQ_COL_SIDEWALK_<id>_L0`) | Correct widths verified against reference; surface height consistent |
| **2.3** | Generate curb geometry. Create curb collision strips at the road/sidewalk boundary. Standard NYC curb height: 15cm (6 inches). | Manual authoring / auto-detect from elevation data | Curb collision mesh (`TSQ_COL_CURB_<id>_L0`) | 15cm step-up verified at 5+ sample points; continuous along block edge |
| **2.4** | Generate stairs (if present). For any staircases within the block (subway entrances, building stoops, TKTS steps), create collision with correct riser heights (NYC code: 17.8cm / 7in max). | Manual authoring | Stair collision mesh (`TSQ_COL_STAIR_<id>_L0`) | Correct riser height; correct run depth; no gaps between treads |
| **2.5** | Generate barriers and medians. Create impassable collision for medians, Jersey barriers, permanent bollards, and other obstacles. | Manual/auto authoring | Barrier collision mesh (`TSQ_COL_BARRIER_<id>_L0`) | Impassable verified: test agent cannot pass through at any point |
| **2.6** | Bake pedestrian navmesh. Generate navigation mesh from the collision surfaces created in 2.1--2.5. Pedestrian agent radius: 0.3m, height: 1.8m, max step: 0.2m, max slope: 45 degrees. | NavMesh bake tool (Recast/Detour or engine-native) | NavMesh asset (`TSQ_NAV_PED_<id>`) | **Walk test: 5 predefined paths** across the block complete without stuck agents |
| **2.7** | Add crosswalk zones. Annotate the navmesh with crosswalk regions. Mark each crosswalk with signal-aware edge metadata (which traffic signal controls this crossing). | Manual annotation tool | NavMesh annotations (`TSQ_NAV_XWALK_<id>`) | Each crosswalk linked to correct signal; agents wait at red, cross at green |
| **2.8** | Add no-go zones. Block areas that are physically accessible but narratively off-limits: backstage areas, construction zones, locked parks. | Manual annotation tool | NavMesh blocked regions (`TSQ_NAV_NOGO_<id>`) | Blocked zones confirmed impassable; NPC and player cannot enter |

### Phase 2 Exit Criteria

- [ ] All 8 steps completed and QA checks passed
- [ ] Walk test report filed in `qa/collision/` (5 paths, 0 failures)
- [ ] All collision meshes committed to `collision/` branch
- [ ] NavMesh committed to `collision/navmeshes/`
- [ ] Collision reviewed by Collision Team lead

---

## Phase 3: Visual Capture

**Goal:** Align high-fidelity visual data and extract hero meshes where interaction requires real geometry.
**Rung:** 3 (Photogrammetry / Gaussian Splats) and 4 (Derived Mesh)
**Prerequisites:** Phase 1 complete. Phase 2 may run in parallel but must be complete before Phase 3 outputs are used for collision.

| Step | Action | Tool | Output | QA Check |
|------|--------|------|--------|----------|
| **3.1** | Import and align splats/photogrammetry. Load the Gaussian splat or photogrammetry capture for this block. Align to geospatial skeleton using the Splat Alignment Checklist (see `splat-alignment-checklist-v0.md`). | Splat import tool + ICP alignment | Aligned splat scene (`TSQ_SPLAT_<id>`) | Residual error at all anchor points **< 0.5m** (see alignment checklist) |
| **3.2** | Validate scale vs anchors. Measure the same 3+ objects used in Phase 1 within the splat. Compare splat measurements to skeleton measurements. | In-engine measurement | Scale comparison report | Scale discrepancy **< 3%** at all measurement points |
| **3.3** | Create splat visibility mask. Define where the splat is high-quality (render it) vs noisy/incomplete (mask it out and fall back to procedural). | Editor masking tool | Splat visibility mask (`TSQ_SPLAT_MASK_<id>`) | Clean boundaries; no visible seams where splat meets procedural |
| **3.4** | Extract hero meshes (if needed). For surfaces requiring player interaction (stoops, kiosks, benches), retopologize clean meshes from the splat reference. | Retopology tool (ZBrush/Blender/custom) | Clean hero meshes (`TSQ_DRV_<name>_<id>_L0`) | No navigation snags on walk test; mesh matches reference within tolerance |
| **3.5** | Generate collision proxies for derived meshes. For each hero mesh extracted in 3.4, create a simplified collision proxy. | Collision proxy generation | Collision proxies (`TSQ_COL_DRV_<name>_<id>`) | Walk test + drive test pass; no fall-throughs, no snags |

### Phase 3 Exit Criteria

- [ ] All 5 steps completed and QA checks passed
- [ ] Splat alignment report filed in `qa/capture/` (residual < 0.5m)
- [ ] Splat and mask committed to `capture/` branch
- [ ] Any derived meshes have passed the Promotion Checklist (see `asset-ladder-v0.md`)
- [ ] Visual capture reviewed by Art Lead

---

## Phase 4: Detail Pass

**Goal:** Dress the block with props, signage, billboards, semantic labels, and IoT artifacts.
**Rung:** 4 (Derived Mesh -- for promoted interactive props) and 5 (Procedural + Authored Detail)
**Prerequisites:** Phase 2 (collision) complete. Phase 3 (visual capture) complete or near-complete.

| Step | Action | Tool | Output | QA Check |
|------|--------|------|--------|----------|
| **4.1** | Place street furniture (from kit). Using the standardized street furniture kit, place bollards, trash cans, benches, fire hydrants, phone booths, newsboxes, and subway entrances. All props snap to Rung 2 collision surfaces. | Prop placement tool (rules-based) | Prop instances (`TSQ_PRP_<type>_<id>`) | Props sit on collision surface (no floating); no prop blocks nav paths without intent |
| **4.2** | Place billboards. Assign billboard entities to building facades per the billboard layout plan. Set tier (T1 hero, T2 support, T3 background), configure light spill radius and intensity. | Billboard placement tool | Billboard entities (`TSQ_BB_<tier>_<id>`) | Tier correctly assigned; light spill renders correctly at night; no z-fighting |
| **4.3** | Apply semantic labels. Tag every placeable entity and surface with its taxonomy class (building, vehicle, prop, surface) and affordances (walkable, climbable, interactable, destructible, evidence-bearing). | Semantic labeling tool | Tagged prims / metadata | All required classes labeled; spot-check 10 random entities for correctness |
| **4.4** | Place IoT artifacts. Position cameras, sensors, signal controllers, and other smart-city artifacts. Assign unique IDs and hook into the event system. | IoT placement tool | IoT artifact entities (`TSQ_IOT_<type>_<id>`) | Each artifact has unique ID; event hook fires on test trigger; coverage matches plan |
| **4.5** | Generate LOD chain. For every asset placed in this block, ensure L0 (near), L1 (mid), L2 (far) representations exist. Verify LOD transition distances. | LOD generation tool (Simplygon / nanite / custom) | L0/L1/L2 per asset | LOD transitions verified: no visible popping at target distances; triangle count within budget |

### Phase 4 Exit Criteria

- [ ] All 5 steps completed and QA checks passed
- [ ] All props, billboards, IoT artifacts committed to `detail/` branch
- [ ] Semantic labels verified on spot-check
- [ ] LOD chain generated and transition-tested
- [ ] Detail pass reviewed by Design Lead

---

## Phase 5: Integration + Test

**Goal:** Validate the complete block as a unified, playable environment meeting all quality and performance targets.
**Rung:** All (integrated)
**Prerequisites:** Phases 1--4 complete.

| Step | Action | Tool | Output | QA Check |
|------|--------|------|--------|----------|
| **5.1** | Run walk test (5 paths). Automated: spawn NPC at 5 predefined start points, walk to 5 predefined destinations. Verify no stuck agents, no fall-throughs, no invisible walls. | Automated test harness | Walk test report (`qa/integration/<block>_walk.json`) | **0 snags, 0 falls** across all 5 paths |
| **5.2** | Run drive test (1 loop). Automated: spawn vehicle, drive a loop around the block perimeter. Verify no collision clipping, no wrong-way traversal, correct lane behavior. | Automated test harness | Drive test report (`qa/integration/<block>_drive.json`) | **0 clips, 0 wrong-way** events |
| **5.3** | Run crowd test (500 NPCs). Spawn 500 pedestrian NPCs distributed across the block. Let simulation run for 60 seconds of game time. Measure deadlocks. | Automated test harness | Crowd test report (`qa/integration/<block>_crowd.json`) | **< 0.1% deadlocks** (fewer than 1 in 500 stuck for > 5 seconds) |
| **5.4** | Capture regression screenshots. Position the camera rig at 10 standardized positions (including any Hero Angles within this block). Capture screenshots. Save as baseline. | Automated camera rig | 10 screenshots (`qa/regression/<block>_ss_01.png` ... `_10.png`) | Baseline saved and committed to regression archive |
| **5.5** | Run performance profile. Profile the block in isolation: measure frame time, triangle count, draw calls, VRAM usage, CPU time per system. Compare against budget. | Engine profiler (RenderDoc / Unreal Insights / custom) | Performance report (`qa/performance/<block>_perf.json`) | All metrics **within budget** per `performance-budget-v0.md` |
| **5.6** | Run constraint test suite. Execute all automated constraint checks: no-contamination rules, naming convention compliance, semantic label coverage, ledger ID uniqueness. | Automated constraint validator | Constraint report (`qa/constraints/<block>_constraints.json`) | **All constraints pass** |
| **5.7** | Human sign-off. Block lead and QA lead jointly review all test reports, walk the block in-engine, and stamp approval. | Human review | Approval stamp in `qa/signoff/<block>_signoff.md` | **Block marked COMPLETE** |

### Phase 5 Exit Criteria

- [ ] All 7 steps completed
- [ ] All test reports filed in `qa/integration/`
- [ ] Performance within budget
- [ ] All constraints passing
- [ ] Human sign-off document committed
- [ ] Block status updated to `COMPLETE` in master tracker

---

## Effort Estimation

| Phase | Typical Duration | Team | Parallelizable? |
|-------|-----------------|------|-----------------|
| **Phase 1: Skeleton** | 0.5 day | Geo team (1 person) | Yes -- across blocks |
| **Phase 2: Collision + Nav** | 1--2 days | Collision team (1--2 people) | Yes -- across blocks |
| **Phase 3: Visual Capture** | 1--2 days | Art team (1--2 people) | Yes -- across blocks; parallel with Phase 2 |
| **Phase 4: Detail** | 2--3 days | Art + Design team (2--3 people) | Yes -- across blocks |
| **Phase 5: Integration + Test** | 1 day | QA + leads (2--3 people) | Partially -- tests automated, sign-off serial |
| **Total per block** | **5--8.5 days** | **3--5 people** | — |

### Block Dependencies

```
Block A1 ─── Phase 1 ──> Phase 2 ──> Phase 4 ──> Phase 5
                 │                        ^
                 └───── Phase 3 ──────────┘

Block A2 ─── Phase 1 ──> Phase 2 ──> Phase 4 ──> Phase 5
                 │                        ^
                 └───── Phase 3 ──────────┘

(Blocks run independently; adjacent blocks reconcile boundaries in Phase 5)
```

---

## Boundary Reconciliation (Adjacent Blocks)

When two adjacent blocks are both in Phase 5 or later, a boundary reconciliation step is required:

| Check | Description | Tolerance |
|-------|-------------|-----------|
| Collision seam | No gap or overlap at block boundary in collision meshes | < 1cm gap, 0cm overlap |
| NavMesh stitch | Pedestrian can walk across block boundary without pause | 0 stuck agents on 3 cross-boundary paths |
| Visual seam | No visible popping or misalignment at block boundary | Qualitative: no seam visible from player height |
| LOD consistency | Adjacent blocks use same LOD distances at boundary | LOD transition within 5m of each other |
| Lighting continuity | No abrupt lighting changes at block boundary | Smooth gradient across boundary |

---

## Failure Recovery

| Failure Type | Recovery Action | Escalation |
|--------------|----------------|------------|
| Scale verification fails (Phase 1) | Re-import tiles; verify Cesium settings; check CRS | Geo Team lead |
| Walk test fails (Phase 2) | Identify snag location; fix collision; re-bake navmesh; re-test | Collision Team lead |
| Splat alignment residual too high (Phase 3) | Re-run ICP with more correspondences; try manual alignment; flag for re-capture if uncorrectable | Art Lead + Geo Team |
| Performance over budget (Phase 5) | Apply LOD aggressiveness; reduce prop density; simplify collision; re-profile | Tech Art + Performance lead |
| Constraint violation (Phase 5) | Fix specific violation; re-run validator; document exception if intentional | Build Pipeline lead |

---

*End of document. For questions about the Block Intake SOP, contact the Build Pipeline lead.*
