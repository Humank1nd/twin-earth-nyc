# Semantic Taxonomy v0

**Document:** Part 04 — Earth Reality Layer
**Status:** v0 Draft
**Scope:** Surface and object class definitions, affordance mappings, material assignments, labeling pipeline
**Authority:** All scene objects in Twin Earth NYC must be assigned exactly one primary semantic class from this taxonomy.

---

## 1. Surface / Object Classes

### 1.1 Affordance Key

| Code | Affordance | Description |
|---|---|---|
| **W** | Walk | NPCs and players can traverse on foot |
| **D** | Drive | Vehicles can traverse |
| **C** | Climb | Can be climbed over or ascended |
| **B** | Block | Obstructs movement (collision barrier) |
| **I** | Interact | Player/NPC can trigger an interaction (open, press, use) |
| **O** | Observe | Provides observational data (cameras, sensors, line-of-sight vantage) |
| **L** | Emit Light | Emits light affecting scene illumination and visibility |
| **E** | Log Events | Generates entries in the event ledger when state changes |

### 1.2 Class Registry

| # | Class | Affordances | Material | Physics Friction (static / dynamic) | NPC Training Relevance |
|---|---|---|---|---|---|
| 1 | **road** | W, D | asphalt | 0.85 / 0.68 | Vehicle pathfinding surface; lane boundaries define legal travel corridors |
| 2 | **crosswalk** | W, D | painted-asphalt | 0.80 / 0.65 | Critical pedestrian-vehicle negotiation zone; NPC crossing decision trigger |
| 3 | **sidewalk** | W | concrete | 0.90 / 0.72 | Primary NPC pedestrian navigation surface; crowd-flow simulation domain |
| 4 | **curb** | W, C, B | granite-curb | 0.92 / 0.74 | Road/sidewalk boundary; NPCs must step up/down; vehicles blocked |
| 5 | **steps / stairs** | W, C | stone-steps | 0.88 / 0.70 | Elevation change navigation; speed reduction zone for NPCs; TKTS steps gathering area |
| 6 | **railing** | B | steel-painted | 0.40 / 0.30 | Movement barrier; grab point for climb affordance; defines stair edges |
| 7 | **glass (window)** | B, O | glass-tempered | 0.18 / 0.12 | Transparent blocker; line-of-sight pass-through for observation; reflection source |
| 8 | **billboard** | O, L | LED-panel | 0.30 / 0.20 | Major light emitter; NPC gaze attractor; visual landmark for navigation |
| 9 | **kiosk** | I, B | steel-composite | 0.50 / 0.40 | Interactive information/ticket point; NPCs queue here; partial movement blocker |
| 10 | **door** | I, W, E | glass-aluminum | 0.45 / 0.35 | Enterable threshold; state change (open/closed) logged; NPC destination node |
| 11 | **camera (CCTV)** | O, E | plastic-housing | 0.50 / 0.40 | Surveillance field-of-view cone; event log source; detection confidence affected by weather |
| 12 | **traffic signal** | O, L, E | aluminum-visor | 0.45 / 0.35 | State machine (red/yellow/green/walk/don't-walk); NPC crossing decision input; event log per cycle |
| 13 | **streetlight** | L | steel-pole | 0.55 / 0.42 | Night illumination source; cone of light defines visibility zones; affects CCTV confidence |
| 14 | **bollard** | B | steel-concrete | 0.70 / 0.55 | Vehicle barrier; pedestrian pass-through; defines plaza boundary edges |
| 15 | **hydrant** | B, I, E | cast-iron | 0.75 / 0.60 | Obstruction; interactive (emergency use); state change logged; no-park zone marker |
| 16 | **trash can** | B, I | steel-mesh | 0.55 / 0.42 | Minor obstruction; interactive (dispose item); NPC avoidance object on sidewalk |
| 17 | **bench** | W, I, B | wood-steel | 0.65 / 0.50 | Seatable surface; NPC rest behavior trigger; partial blocker at leg height |
| 18 | **planter** | B | concrete-soil | 0.80 / 0.65 | Movement barrier; plaza boundary marker; NPC path deflection object |
| 19 | **taxi** | D, I, E | steel-body | 0.72 / 0.58 | Driveable vehicle; hailable interaction; logs pickup/dropoff events; NPC transport mode |
| 20 | **bus** | D, I, E | steel-body | 0.72 / 0.58 | Driveable vehicle; boardable at stops; logs route/stop events; NPC mass-transit option |
| 21 | **construction barrier** | B, L | plastic-reflective | 0.45 / 0.35 | Hard movement blocker; reflective strips emit under headlights; reroutes NPC paths |
| 22 | **subway grate** | W, O | steel-grate | 0.50 / 0.38 | Walkable with audio/visual cues (steam, noise); observation point for below-grade activity |
| 23 | **manhole cover** | W, D | cast-iron | 0.65 / 0.52 | Flush walkable/driveable surface; potential interactive (maintenance access); infrastructure marker |
| 24 | **newsstand** | I, B | steel-glass | 0.55 / 0.42 | Interactive commerce point; partial blocker; NPC purchase behavior; sidewalk landmark |
| 25 | **phone booth / charging station** | I, L, E | steel-glass-LED | 0.50 / 0.40 | Interactive (charge device, browse info); emits light; logs usage events; LinkNYC kiosk model |

---

## 2. Labeling Pipeline

### 2.1 Storage Architecture

Semantic labels are stored in two synchronized representations:

| Store | Format | Access Pattern |
|---|---|---|
| **USD Prim Tags** (Omniverse) | Custom `semantic:class` attribute on each USD prim, plus `semantic:affordances` as a token array | DCC tools, offline rendering, training data export |
| **ECS Components** (Engine) | `SemanticClass` component with `class_id: u16`, `affordance_flags: u32` bitmask | Runtime queries, NPC AI, physics dispatch |

**Sync Protocol:** On scene import from USD to engine, a `SemanticImporter` system reads prim tags and creates corresponding ECS components. On export, the reverse. Hash of semantic state is compared; mismatches block the export pipeline and raise an error.

### 2.2 Affordance Bitmask Layout

```
Bit 0: Walk      (0x01)
Bit 1: Drive     (0x02)
Bit 2: Climb     (0x04)
Bit 3: Block     (0x08)
Bit 4: Interact  (0x10)
Bit 5: Observe   (0x20)
Bit 6: Emit Light(0x40)
Bit 7: Log Events(0x80)
Bits 8-31: Reserved for future affordances
```

Example: `traffic signal` = Observe | Emit Light | Log Events = `0x20 | 0x40 | 0x80` = `0xE0`.

### 2.3 Semantics Pass Checklist (One Block)

When semantically labeling a new city block, apply labels in this order to ensure dependencies are met (e.g., crosswalks reference curbs, signals reference crosswalks):

| Step | Action | Depends On | Verification |
|---|---|---|---|
| 1 | Label all **crosswalk** boundaries | -- | Crosswalk polygons align with painted markings in reference |
| 2 | Label all **traffic signals** and link to crosswalks | Step 1 | Each crosswalk has at least one controlling signal |
| 3 | Label **sidewalks** and **curbs** | -- | Sidewalk polygons fill space between building faces and curb lines |
| 4 | Label **steps / stairs** and **railings** | Step 3 | Steps connect sidewalk elevations; railings bound step edges |
| 5 | Label **doors** and building thresholds | Step 3 | Doors sit on sidewalk-adjacent faces; marked as interactive |
| 6 | Label **cameras (CCTV)** and assign FOV cones | Steps 1-5 | Camera cones cover intended surveillance zones |
| 7 | Label **kiosks**, **newsstands**, **phone booths** | Step 3 | Placed on sidewalk surfaces; marked as blockers + interactive |
| 8 | Label all **props** (hydrants, bollards, benches, planters, trash cans) | Step 3 | Props placed on correct surface; blocker volumes correct |
| 9 | Label **vehicle zones** (road surfaces, taxi/bus entities) | Step 1 | Vehicle zones bounded by curbs; no overlap with sidewalk |
| 10 | **Validation pass** | Steps 1-9 | Run automated checker: all prims have semantic tag, no orphan geometry |

### 2.4 Minimum Semantic Set for "Crosswalk Intelligence"

The crosswalk intelligence subsystem (NPC pedestrian crossing AI) requires the following minimum labeled elements to function:

| Required Element | Semantic Class | Data Required |
|---|---|---|
| Crosswalk boundaries | `crosswalk` | Polygon outline (4+ vertices), walk direction vector |
| Signal state source | `traffic signal` | Linked signal entity ID, current state (walk/don't-walk/countdown), cycle timing |
| Curb locations | `curb` | Line segments defining road-sidewalk boundary at crosswalk endpoints |
| Vehicle zone boundaries | `road` | Polygon defining active vehicle travel lanes adjacent to crosswalk |
| Pedestrian wait zones | `sidewalk` | Polygon regions at each crosswalk end where NPCs queue before crossing |

**Crosswalk Intelligence Contract:** If any of the five elements above is missing or unlabeled for a given crosswalk, the NPC crossing system must fall back to a conservative "wait indefinitely" behavior and log a warning: `SEMANTIC_INCOMPLETE: crosswalk {id} missing {element}`.

---

## 3. Taxonomy Versioning

| Field | Value |
|---|---|
| Version | v0 (initial draft) |
| Total classes | 25 |
| Next review | After first block is fully labeled and crosswalk intelligence tested |
| Extension policy | New classes added via PR with affordance justification and at least one NPC training use case |
| Deprecation policy | Classes deprecated only after zero references remain in scene graph; 2-sprint warning period |

---

*End of Semantic Taxonomy v0.*
