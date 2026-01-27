# Invariant Preservation Spec v0

**Twin Earth NYC -- Part 13: Scaling Strategy and Risk Control**
**Document:** Invariant Preservation -- What Must Survive Growth
**Version:** 0.1.0
**Status:** Draft
**Last Updated:** 2026-01-27

---

## 1. Purpose

As Twin Earth NYC grows from five blocks to five hundred, certain properties of the world must never change. These are the **invariants** -- the spatial, visual, and systemic facts that anchor the player's sense of place and the simulation's internal consistency. This document defines the complete invariant taxonomy, specifies tolerance tables for each class, establishes verification methods, and mandates a regression testing protocol that scales with the world.

**Rule:** If growth breaks an invariant, growth stops until the invariant is restored. There are no exceptions.

---

## 2. Invariant Taxonomy

Every invariant belongs to one of five classes. Each class has distinct verification methods and failure severity.

| Class | Description | Example | Failure Severity |
|-------|-------------|---------|-----------------|
| **Landmark Silhouette** | The recognizable outline of an iconic structure as seen from street level | One Times Square's triangular wedge profile | P0 -- ship-blocking |
| **Scale Anchor** | A real-world object whose dimensions the human visual system uses unconsciously to judge distances and proportions | Door height (2.1 m), taxi length (4.8 m), human height (1.75 m) | P0 -- ship-blocking |
| **Skyline Profile** | The composite edge-line of the skyline as seen from defined vantage points within the playable zone | Empire State silhouette visible from 42nd/7th looking SSE | P1 -- milestone-blocking |
| **Street Topology** | The connectivity, width, angle, and lane structure of the street network | Broadway diagonal at ~29 degrees off grid; 7th Ave width ~23 m | P0 -- ship-blocking |
| **System Coupling** | Behavioral invariants that ensure simulation systems interact correctly as the world grows | Heat decay rates remain constant regardless of block count; event bus throughput scales linearly | P1 -- milestone-blocking |

---

## 3. Landmark Silhouette Invariants

### 3.1 Definition

A landmark silhouette invariant specifies that the 2D outline of a structure, as captured from a defined camera position, must match a reference photograph within tolerance. The silhouette is the boundary between the structure and the sky (or other background). Interior detail, texture, and material may change -- the outline must not.

### 3.2 Registered Landmarks

| ID | Landmark | Primary Vantage | Silhouette Features | Tolerance |
|----|----------|-----------------|---------------------|-----------|
| LS-01 | One Times Square | 43rd/Broadway looking S | Triangular wedge taper, billboard wrap zone, rooftop mast | 2 deg rotation, 3% scale, 5 px edge deviation at 1920x1080 |
| LS-02 | TKTS Red Steps | 44th/7th looking NW | Step cascade profile, canopy overhang, Duffy statue silhouette behind | 2 deg rotation, 3% scale, 5 px edge deviation |
| LS-03 | Marriott Marquis facade | 46th/Broadway looking S | Curved LED panel profile, entrance canopy | 3 deg rotation, 5% scale, 8 px edge deviation |
| LS-04 | Empire State Building | 42nd/7th looking SSE | Art Deco setbacks, antenna mast, overall proportion | 2 deg rotation, 5% scale, 10 px edge deviation (distant) |
| LS-05 | Chrysler Building | 42nd/Lexington sightline | Eagle ornaments (as notch pattern), spire taper | 3 deg rotation, 5% scale, 10 px edge deviation (distant) |
| LS-06 | One World Trade Center | West St sightline (from Ring 3+) | Tapered obelisk, antenna mast | 2 deg rotation, 5% scale, 10 px edge deviation |
| LS-07 | Bank of America Tower | 42nd looking E | Crystalline faceted crown | 3 deg rotation, 5% scale, 8 px edge deviation |

### 3.3 Verification Method

```
SILHOUETTE VERIFICATION PIPELINE:

  1. Capture:  Position camera at defined vantage point.
               Render frame with sky-only background (all non-target geometry
               replaced with solid blue).
               Output: binary mask (structure = white, sky = black).

  2. Compare:  Load reference mask (captured from surveyed photograph).
               Compute Hausdorff distance between edge contours.
               Compute rotation offset via principal axis alignment.
               Compute scale ratio via bounding box comparison.

  3. Evaluate: Pass if ALL of:
                 - Hausdorff distance < tolerance_px
                 - Rotation offset < tolerance_deg
                 - Scale ratio within 1.0 +/- tolerance_scale

  4. Report:   Generate overlay image (reference in red, capture in green).
               Log pass/fail, all measured values, delta from tolerance.
```

---

## 4. Scale Anchor Invariants

### 4.1 Definition

A scale anchor is a common real-world object whose dimensions are deeply embedded in human spatial perception. If a door is 3 meters tall, the entire street reads as miniature. If a taxi is 3 meters long, buildings look like dollhouses. Scale anchors must be metrically accurate at all LOD levels, in all distance bands, and in all blocks -- including new blocks added during expansion.

### 4.2 Scale Anchor Registry

| ID | Anchor | Canonical Dimension | Tolerance | LOD Rule |
|----|--------|-------------------|-----------|----------|
| SA-01 | Standard door (residential/commercial) | Height: 2.1 m, Width: 0.9 m | +/- 0.05 m | All LODs must preserve height ratio. L2 may merge door into wall texture but must retain correct proportional rectangle. |
| SA-02 | Standing adult human (NPC) | Height: 1.75 m (+/- 0.15 m for variation) | Height range: 1.60 -- 1.90 m | Impostor billboards at L2 must match standing height within 5%. |
| SA-03 | Yellow taxi (sedan) | Length: 4.8 m, Height: 1.5 m | +/- 0.1 m | L2 may simplify to box silhouette but length and height preserved. |
| SA-04 | Traffic signal head | Mounting height: 5.5 m (center of signal) | +/- 0.2 m | L2 may reduce to point light at correct height. |
| SA-05 | Standard fire hydrant | Height: 0.76 m | +/- 0.05 m | Culled beyond 100 m; when visible, height is exact. |
| SA-06 | NYC curb | Step height: 0.15 m (6 in) | +/- 0.02 m | Physics collision must enforce this at all distances; visual may simplify. |
| SA-07 | Crosswalk stripe | Width: 0.30 m, spacing: 0.30 m | +/- 0.05 m | L2 may merge into solid white band; L0/L1 must show individual stripes. |
| SA-08 | Standard streetlight pole | Height: 8.0 m (to luminaire) | +/- 0.3 m | L2 may simplify to vertical line with light point. |
| SA-09 | MTA subway entrance canopy | Height: 2.4 m (clearance), Width: 3.0 m | +/- 0.2 m | Must be recognizable as subway entrance at all LODs where visible. |
| SA-10 | US mailbox (blue USPS) | Height: 1.1 m | +/- 0.05 m | Culled beyond 80 m. |

### 4.3 Scale Anchor Verification

| Test | Method | Frequency | Automation |
|------|--------|-----------|------------|
| **Dimension spot-check** | In-engine ruler tool measures 5 random instances of each anchor type per block | Every block completion (Phase 5) | Semi-automated: tool positions ruler, human reads value |
| **Ratio cross-check** | Screenshot at eye height; measure door-to-human, taxi-to-door, signal-to-human pixel ratios; compare to reference | Every build | Automated: pixel-ratio script |
| **LOD consistency** | Force each anchor to L0, L1, L2 in sequence; measure bounding box at each level | Every asset update | Automated: LOD test harness |
| **New block inheritance** | When a new block enters Phase 4, all placed anchors are measured against the registry | Every block intake | Automated: CI gate |

---

## 5. Skyline Profile Invariants

### 5.1 Definition

The skyline profile is the composite silhouette of all buildings visible from a defined vantage point, projected against the sky. Unlike individual landmark silhouettes, the skyline profile captures the **relationships between buildings** -- relative heights, spacing, layering depth.

### 5.2 Registered Skyline Profiles

| ID | Vantage Point | Direction | Key Features | Tolerance |
|----|--------------|-----------|--------------|-----------|
| SP-01 | TKTS Red Steps top | South toward 42nd | One Times Square tower, billboard canyon walls, street depth | 8 px edge deviation at 1920x1080; building order must match |
| SP-02 | 42nd / Broadway NW corner | North up Broadway | Converging facades, TKTS steps visible, Marriott curve | 8 px edge deviation; depth layering order must match |
| SP-03 | Center of bowtie | 360-degree panoramic | Surround skyline, billboard ring, street canyon from inside | 10 px edge deviation per 90-degree quadrant |
| SP-04 | 47th / 7th Ave | South down 7th Ave | Full slice depth, Times Square glow (at night) | 10 px edge deviation; glow dome visible at night |
| SP-05 | 34th / 5th Ave (Ring 3+) | North toward Midtown | Empire State foreground, Times Square towers mid-ground | 15 px edge deviation (distant view, coarser tolerance) |

### 5.3 Skyline Regression Protocol

When a new block is added, its geometry may alter skyline profiles visible from existing vantage points. The regression protocol:

```
FOR each registered skyline profile (SP-01 through SP-xx):
  1. Capture current profile from vantage point (pre-expansion).
  2. Add new block geometry.
  3. Capture updated profile from same vantage point (post-expansion).
  4. Compute edge deviation between pre and post profiles.
  5. IF deviation > tolerance for ANY profile:
       BLOCK the expansion.
       Root cause: did the new block occlude a landmark? Did it introduce
       a silhouette-breaking structure? Did LOD changes alter a distant
       building's outline?
       FIX before re-testing.
  6. IF all profiles pass:
       Update reference captures to include new block.
       New block's own vantage points (if any) are added to the registry.
```

---

## 6. Street Topology Invariants

### 6.1 Definition

Street topology invariants ensure that the navigable street network preserves real-world geometry: street widths, intersection angles, block lengths, lane counts, and one-way directions. These are sourced from NYC DOT survey data and GIS records.

### 6.2 Topology Constraints

| ID | Constraint | Specification | Tolerance | Source |
|----|-----------|---------------|-----------|--------|
| ST-01 | Broadway diagonal bearing | ~29 degrees off Manhattan grid (NW-SE) | +/- 1 degree | NYC GIS survey |
| ST-02 | 7th Avenue width (curb-to-curb + sidewalks) | ~23 m total (~15 m roadway, ~4 m each sidewalk) | +/- 0.5 m | NYC DOT street survey |
| ST-03 | Cross-street block spacing (42nd to 47th) | ~80 m per block (~400 m cumulative) | +/- 1.0 m cumulative | NYC GIS block dims |
| ST-04 | Avenue block spacing (6th to 8th Ave) | ~275 m per avenue block | +/- 2.0 m | NYC GIS block dims |
| ST-05 | One-way directions | Broadway: southbound below 59th. 7th Ave: southbound. Cross streets: alternating (even=eastbound, odd=westbound) | Exact | NYC DOT traffic rules |
| ST-06 | Lane count (7th Ave) | 4 traffic lanes + 1 parking lane each side (variable) | Exact count | NYC DOT |
| ST-07 | Crosswalk placement | All crosswalks within 0.5 m of surveyed position | +/- 0.5 m | NYC DOT intersection plans |
| ST-08 | Bowtie intersection angles | Acute angles where Broadway crosses 7th Ave | +/- 1 degree per angle | NYC GIS |
| ST-09 | Pedestrian island dimensions | Father Duffy Square, Times Square plaza | +/- 0.5 m on major dimensions | NYC DCP survey |
| ST-10 | Subway entrance positions | All MTA entrances within block footprint | +/- 1.0 m | MTA station plans |

### 6.3 Topology Verification

Topology is verified by an automated test that loads the NavMesh and collision geometry, extracts the street graph (nodes at intersections, edges along streets), and compares against a reference graph derived from NYC GIS data.

| Metric | Method | Pass Criteria |
|--------|--------|---------------|
| Node position accuracy | Compare intersection center coordinates to GIS reference | All nodes within tolerance per ST-01 through ST-10 |
| Edge bearing | Measure bearing of each street edge; compare to survey | All bearings within +/- 1 degree |
| Edge length | Measure length of each block edge; compare to survey | All lengths within +/- 1.0 m |
| Connectivity | Verify that the graph has the correct number of edges per node | Exact match with reference graph |
| One-way compliance | Verify traffic direction flags on each edge | Exact match with ST-05 |

---

## 7. System Coupling Invariants

### 7.1 Definition

System coupling invariants ensure that adding blocks does not change the behavior of simulation systems in existing blocks. These are behavioral, not geometric.

### 7.2 Coupling Constraints

| ID | Invariant | Specification | Verification |
|----|-----------|---------------|-------------|
| SC-01 | Heat decay rate is block-independent | Adding block N+1 does not change the decay rate of Heat in blocks 1..N | Run Heat decay test in Ring 0 blocks before and after Ring 1 integration; compare decay curves (must be identical within 0.01) |
| SC-02 | Event bus throughput scales linearly | Adding K blocks increases peak event rate by at most K * per_block_event_rate | Measure event bus throughput with N blocks, then N+1 blocks; verify delta <= per_block_event_rate (+/- 10%) |
| SC-03 | Ledger query time is sub-linear in event count | Query "all events in block X in last 5 minutes" completes in < 10 ms regardless of total ledger size | Benchmark query with 1K, 10K, 100K, 1M total events; verify all < 10 ms |
| SC-04 | NPC tick budget is per-block | Each block's NPC population consumes its own tick budget (2 ms background, 3 ms hero); adding blocks does not reduce budget for existing blocks | Profile NPC tick time per block before and after expansion; verify no block exceeds its budget |
| SC-05 | Show Director overhead is O(log N) in managed entities | Director tick time grows logarithmically with total entity count due to spatial indexing | Profile Director tick with 1K, 5K, 20K, 50K entities; verify sub-linear growth |
| SC-06 | Streaming throughput remains constant per cell transition | Loading one block takes < 500 ms regardless of how many blocks are already loaded | Measure cell load time with 5, 17, 41, 80 blocks loaded; verify all < 500 ms |
| SC-07 | Physics solver time is bounded by active-entity count, not total-entity count | Dormant entities (> 300 m from camera) contribute zero physics cost | Profile physics tick with 50K total entities, 2K active; verify cost matches 2K-entity baseline |

---

## 8. Tolerance Summary Table

| Invariant Class | Typical Tolerance | Measurement Unit | Verification Frequency |
|----------------|-------------------|------------------|----------------------|
| Landmark Silhouette | 2-3 deg rotation, 3-5% scale, 5-10 px edge | Degrees, %, pixels (at 1920x1080) | Every build |
| Scale Anchor | +/- 0.02 m to +/- 0.3 m (varies by anchor) | Meters | Every block completion |
| Skyline Profile | 8-15 px edge deviation | Pixels (at 1920x1080) | Every ring integration |
| Street Topology | +/- 0.5 m to +/- 2.0 m (varies by feature) | Meters, degrees | Every block completion |
| System Coupling | Varies by system (see SC-01 through SC-07) | ms, events/s, ratios | Every ring integration |

---

## 9. Regression Test Suite

### 9.1 Test Categories

| Category | Tests | Runtime | Trigger |
|----------|-------|---------|---------|
| **Silhouette regression** | 1 test per registered landmark x 1+ vantage points | ~30 s total (automated capture + comparison) | Every build |
| **Scale anchor spot-check** | 5 instances x 10 anchor types x loaded block count | ~2 min per block (semi-automated) | Every block Phase 5 |
| **Skyline profile regression** | 1 test per registered profile | ~20 s total (automated) | Every build that adds geometry |
| **Topology graph comparison** | 1 full-graph comparison | ~10 s (automated) | Every build |
| **System coupling benchmarks** | 7 benchmarks (SC-01 through SC-07) | ~5 min total (automated) | Every ring integration |

### 9.2 Failure Escalation

| Severity | Response | Timeline |
|----------|----------|----------|
| P0 (ship-blocking) | Build promotion halted. Fix assigned to owner within 4 hours. Verified fix required before next build. | Same day |
| P1 (milestone-blocking) | Logged with full diagnostic. Fix required before milestone gate. Does not block daily builds. | Within sprint |
| P2 (tracked) | Logged. Scheduled for next polish pass. Does not block anything. | Within ring |

---

## 10. Invariant Inheritance Protocol

When a new block enters the build pipeline (Part 10, Block Intake SOP), it inherits all applicable invariants automatically:

```
NEW BLOCK INVARIANT INHERITANCE:

  Phase 1 (Skeleton):
    - Inherit all Street Topology invariants for streets within block bounds
    - Inherit all Scale Anchor tolerances for the 10 registered anchors

  Phase 3 (Visual Capture):
    - Check: does this block contain a registered landmark?
      YES -> Landmark Silhouette invariant applies from this point forward
      NO  -> No landmark invariants (but skyline profiles may still be affected)

  Phase 4 (Detail Pass):
    - All placed scale anchors measured against registry
    - All IoT artifacts registered with correct entity IDs

  Phase 5 (Integration):
    - Full skyline profile regression (does this block change any profile?)
    - System coupling benchmarks re-run with new block loaded
    - Topology graph updated and re-verified
```

---

## 11. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1.0 | 2026-01-27 | Design Team | Initial draft -- taxonomy, tolerance tables, verification methods, regression suite |

---

*End of Invariant Preservation Spec v0*
