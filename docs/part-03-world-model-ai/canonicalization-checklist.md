# Canonicalization Checklist — Generative Outputs to Real Assets

> **Series:** Twin Earth NYC — Part 3: World Model & AI
> **Document:** `canonicalization-checklist.md`
> **Status:** Draft v0
> **Last Updated:** 2026-01-27
> **Depends On:** `proposal-spec-v0.md`, Part 1 (Truth Anchors), Part 2 (Ledger & Evidence)

---

## 1. The No Contamination Rule

> **Generative outputs NEVER become truth assets without explicit verification and promotion.**

This is the foundational rule of the Twin Earth NYC asset pipeline. It exists because:

- **Generative models hallucinate.** A model that suggests a prop placement may put it inside a wall, at the wrong scale, or in a location that violates real-world truth.
- **Truth assets are permanent.** Once an asset is canonical, it affects collision, navigation, entity identity, and the persistent ledger. A bad asset corrupts gameplay.
- **Players depend on truth.** The game's core mechanic — detecting anomalies in a faithful replica of NYC — requires that the baseline world be trustworthy. If generative noise leaks into the truth layer, the entire premise breaks.

The No Contamination Rule means:

1. No generative output may be referenced by the truth layer, collision system, navmesh, ledger, or entity registry without passing the full canonicalization checklist.
2. No generative output may be cached in a location where it could be mistakenly loaded as a canonical asset.
3. All generative outputs must be stored in a separate directory tree (`/suggestive/`) from canonical assets (`/canonical/`).
4. Any process that reads from `/canonical/` must never fall through to `/suggestive/` as a fallback.

---

## 2. Two Asset Classes

Every asset in Twin Earth NYC belongs to exactly one of two classes. There is no middle ground.

### 2.1 Suggestive Assets

**Definition:** Outputs from the world model, generative tools, or exploration pipelines that have not been verified. They exist to inspire, preview, and prototype — never to ship.

| Property | Value |
|----------|-------|
| **Storage** | `/assets/suggestive/` directory tree |
| **File prefix** | `sug_` (e.g., `sug_hotdog_cart_7av_v3.fbx`) |
| **Metadata flag** | `"canonical": false` |
| **Used by** | Previs tools, mood boards, review sessions, sandbox simulations |
| **NOT used by** | Runtime game, collision system, navmesh, ledger, entity registry |
| **Lifetime** | Temporary. Pruned after 30 days if not promoted. |
| **Collision data** | None. Suggestive assets have no collision geometry. |
| **Entity ID** | None. Suggestive assets are not entities. They use `pending:` prefixed temporary IDs. |

**Types of Suggestive Assets:**

| Type | Description | Example |
|------|-------------|---------|
| **Previs Renders** | Camera angles, lighting setups, scene compositions rendered from the world model. | A rendered frame showing how a vendor cart cluster might look at sunset. |
| **Mood Boards** | Collections of reference images, color palettes, and atmosphere targets. | A board showing "rainy night Times Square" visual references. |
| **Staging References** | NPC positions, event blocking, crowd flow visualizations. | A top-down view showing proposed NPC placement for a parade scene. |
| **Layout Drafts** | Prop placements, furniture arrangements, signage positions. | A scene with 5 different food cart positions to choose from. |
| **Texture Explorations** | Material variations, surface treatments, signage content options. | 4 different billboard texture variants for a storefront. |

### 2.2 Canonical Assets

**Definition:** Verified, promoted assets that are part of the game's truth layer. They define what is real in Twin Earth NYC.

| Property | Value |
|----------|-------|
| **Storage** | `/assets/canonical/` directory tree |
| **File prefix** | `can_` (e.g., `can_tkts_steps_v2.fbx`) |
| **Metadata flag** | `"canonical": true, "promoted_from": "<suggestive_id or null>"` |
| **Used by** | Runtime game, collision system, navmesh, ledger, entity registry |
| **Lifetime** | Permanent until explicitly deprecated (with ledger entry). |
| **Collision data** | Required. Every canonical asset has verified collision geometry. |
| **Entity ID** | Required. Every canonical asset has a stable entity ID in the ledger. |

**Types of Canonical Assets:**

| Type | Description | Example |
|------|-------------|---------|
| **Collision Meshes** | Simplified geometry used for physics and navigation. | The walkable surface of the TKTS steps. |
| **Final Textures** | Approved, resolution-locked surface materials. | The actual billboard texture for a specific storefront. |
| **Stable Props** | Verified objects that exist in the persistent world. | A specific fire hydrant at 45th and 7th Avenue. |
| **Anchor-Verified Placements** | Props and structures whose positions have been checked against truth anchors. | A newsstand placed within 0.05m of its surveyed real-world position. |
| **Ledger-Bound Entities** | Objects with permanent identity in the game's state ledger. | A CCTV camera with entity ID, position, coverage cone, and operational state. |

---

## 3. Canonicalization Checklist — 9 Steps

A suggestive asset becomes canonical only by passing every step of this checklist. No step may be skipped. The checklist is executed by the asset pipeline with human oversight at the final step.

---

### Step 1: Georeferenced Placement Verified

**What:** Confirm that the asset's proposed position matches a real-world location within the tolerance defined by its anchor class.

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| Position vs. survey data | Compare proposed lat/lon/alt to GIS reference data or photogrammetry point cloud. | Within tolerance: Tier 1 = 0.05m, Tier 2 = 0.25m, Tier 3 = 1.0m. |
| Orientation vs. reference | Compare rotation to Street View or survey photography. | Within 5 degrees of reference for Tier 1, 15 degrees for Tier 2, 30 degrees for Tier 3. |
| Ground plane contact | Verify asset sits on the correct surface, not floating or sunk. | Bottom face within 0.02m of ground plane. |

**Output:** Placement verification report with measured offsets.

**Failure Action:** Return to world model with correction guidance. Do not proceed.

---

### Step 2: Scale Check vs. 3+ Anchors

**What:** Verify the asset's dimensions are correct by comparing against at least three independent scale reference anchors.

| Reference Anchor | Expected Value | Tolerance |
|-----------------|---------------|-----------|
| **Standard door height** | 2.1m (6'10") | +/- 5% (2.00m - 2.21m) |
| **Average human height** | 1.75m (5'9") | +/- 5% (1.66m - 1.84m) |
| **Standard sedan length** | 4.5m (14'9") | +/- 8% (4.14m - 4.86m) |
| **Fire hydrant height** | 0.76m (2'6") | +/- 5% (0.72m - 0.80m) |
| **Street lane width** | 3.0m (10') | +/- 5% (2.85m - 3.15m) |
| **Sidewalk width (typical)** | 3.7m (12') | +/- 10% (3.33m - 4.07m) |
| **Traffic light height** | 5.5m (18') | +/- 5% (5.23m - 5.78m) |
| **Bus stop shelter height** | 2.4m (8') | +/- 5% (2.28m - 2.52m) |

**Process:**
1. Place the asset in a test scene alongside at least 3 reference anchors.
2. Measure the asset's bounding box dimensions.
3. Compare proportions against each anchor.
4. All 3 comparisons must pass within tolerance.

**Output:** Scale comparison screenshot + measurement table.

**Failure Action:** Flag asset as incorrectly scaled. Return to source (generative or manual) for correction. Common fix: uniform scale adjustment.

---

### Step 3: Collision Proxy Generated and Tested

**What:** Generate a simplified collision mesh for the asset and verify it works correctly for both pedestrian and vehicle interactions.

| Test | Method | Pass Criteria |
|------|--------|---------------|
| **Walk test** | Automated NPC walks past, around, and into the asset from 8 cardinal directions. | NPC is blocked on all solid faces. NPC can walk past without getting stuck. No phasing. |
| **Drive test** | Automated vehicle drives past and into the asset from 4 approach angles. | Vehicle is blocked by solid faces. Vehicle does not phase through. Vehicle does not launch. |
| **Stand test** | NPC stands on all horizontal surfaces that should be walkable. | NPC stands without falling through. NPC does not slide off surfaces with < 30 degree slope. |
| **Gap test** | Check for gaps between collision proxy and visual mesh. | No gap > 0.1m between visual surface and collision surface. |
| **Convexity test** | Verify collision mesh has no degenerate faces or inverted normals. | Mesh validation passes. All normals face outward. |

**Output:** Collision test report with pass/fail per test. Screenshots of any failures.

**Failure Action:** Regenerate collision proxy with stricter parameters. If auto-generation fails, hand-model the collision mesh. Do not proceed without clean collision.

---

### Step 4: LOD Chain Generated

**What:** Create multiple levels-of-detail for the asset so it renders efficiently at all distances.

| LOD Level | Distance Range | Target Triangle Budget | Required Features |
|-----------|---------------|----------------------|-------------------|
| **LOD 0 (Near)** | 0 - 15m | Full detail (source mesh) | All geometry, full materials, all decals |
| **LOD 1 (Mid)** | 15 - 50m | 50% of LOD 0 | Simplified geometry, combined materials, major decals only |
| **LOD 2 (Far)** | 50 - 150m | 15% of LOD 0 | Block geometry, atlas texture, no decals |
| **LOD 3 (Distant)** | 150m+ | Billboard or impostor | Flat card or low-poly shell, baked texture from multiple angles |

**Verification:**
- Transition between each LOD level at the defined distances while walking toward and away from the asset.
- No visible pop or hitch at transition points.
- Silhouette of each LOD matches within tolerance (Tier 1: 95% match, Tier 2: 85%, Tier 3: 70%).
- LOD 0 triangle count is within budget for asset tier.

**Output:** LOD chain preview (side-by-side comparison at each level). Transition smoothness score.

**Failure Action:** Adjust LOD generation parameters or hand-edit problematic levels. Re-test transitions.

---

### Step 5: Ledger Identity Assigned

**What:** Register the asset as a persistent entity in the game ledger, assigning it a stable identity that will exist for the lifetime of the game.

| Assignment | Detail |
|-----------|--------|
| **Entity ID** | Permanent, globally unique. Format: `entity:<type>-<location>-<seq>` (e.g., `entity:hydrant-7av-45st-001`). |
| **Entity Type** | Classification from the entity taxonomy (e.g., `street_furniture.hydrant`). |
| **Creation Record** | Ledger entry documenting: when created, by whom (human + tool), source data (scan, manual, promoted from suggestive). |
| **Canonical Position** | Georeferenced position locked in ledger. Can only be changed by explicit ledger amendment (requires human approval). |
| **State Schema** | Definition of what mutable state this entity tracks (e.g., for a traffic light: `{current_phase, time_in_phase, operational}`). |
| **Ownership** | Which system "owns" this entity (e.g., traffic system owns traffic lights, building system owns facades). |

**Process:**
1. Generate entity ID from naming convention.
2. Verify ID does not already exist in ledger (no duplicates).
3. Create initial ledger entry with all required fields.
4. Verify entry is retrievable and consistent.

**Output:** Ledger entry confirmation with entity ID.

**Failure Action:** If ID collision, increment sequence number. If ledger write fails, investigate and retry. Do not proceed without confirmed ledger identity.

---

### Step 6: Material Properties Assigned

**What:** Assign physical material properties to all surfaces of the asset, enabling correct physics, audio, and gameplay interactions.

| Property | Description | Example Values |
|----------|-------------|----------------|
| **Surface type** | Physics material classification. | `concrete`, `metal`, `glass`, `wood`, `fabric`, `plastic`, `water` |
| **Friction coefficient** | Static and dynamic friction for character/vehicle movement. | Concrete: 0.7/0.5. Metal: 0.4/0.3. Wet concrete: 0.4/0.25. |
| **Restitution** | Bounciness for collisions. | Concrete: 0.1. Metal: 0.3. Rubber: 0.8. |
| **Footstep sound** | Audio event triggered when character walks on this surface. | `footstep_concrete`, `footstep_metal_grate`, `footstep_wet` |
| **Impact sound** | Audio event triggered when objects hit this surface. | `impact_metal_hollow`, `impact_glass_shatter`, `impact_concrete_thud` |
| **Destructibility** | Whether this surface can be damaged and how. | `indestructible`, `dent`, `shatter`, `scratch` |
| **Weather interaction** | How weather affects this surface visually. | `wet_reflective`, `snow_accumulates`, `ice_forms`, `none` |

**Process:**
1. For each surface of the asset, look up the material in the physics material table.
2. If material exists in table, assign automatically.
3. If material is new, define properties and add to table (requires human approval).
4. Verify by dropping a test object on each surface and checking sound + physics response.

**Output:** Material assignment table for the asset.

**Failure Action:** If material not in table, flag for human material definition. Do not proceed with undefined materials (gameplay will have wrong sounds and physics).

---

### Step 7: Semantic Labels Applied

**What:** Tag the asset with classification labels from the game's taxonomy, enabling gameplay systems to understand what the asset *is* and what players can *do* with it.

| Label Type | Description | Examples |
|-----------|-------------|---------|
| **Taxonomy Class** | Hierarchical classification. | `street_furniture.hydrant`, `vehicle.taxi.sedan`, `building.facade.storefront` |
| **Affordances** | What interactions the asset supports. | `climbable`, `destructible`, `interactable`, `cover_point`, `sit_target`, `hide_behind` |
| **Navigation Role** | How the asset affects NPC/player movement. | `obstacle`, `pathway`, `barrier`, `ramp`, `stairs`, `door` |
| **Evidence Role** | Whether the asset participates in the evidence system. | `cctv_camera`, `reflective_surface`, `witness_npc`, `evidence_container`, `none` |
| **Anomaly Affinity** | How the asset interacts with anomaly effects. | `anomaly_reactive` (flickers, distorts), `anomaly_immune` (unaffected), `anomaly_source` (generates anomaly) |
| **Occlusion Class** | How the asset occludes other objects for culling/streaming. | `large_occluder`, `small_occluder`, `transparent`, `non_occluding` |

**Process:**
1. Assign taxonomy class from the standard hierarchy.
2. Review asset geometry and design intent to determine affordances.
3. Tag navigation role based on collision proxy shape and placement.
4. Assign evidence role if applicable.
5. Set anomaly affinity based on material and location.
6. Classify occlusion behavior based on size and opacity.

**Output:** Semantic label set for the asset (stored in asset metadata).

**Failure Action:** If taxonomy class does not exist for this asset type, propose new class (requires taxonomy committee approval). Do not ship unlabeled assets.

---

### Step 8: Visual Regression Captured

**What:** Capture baseline screenshots of the asset in its canonical placement from standardized camera angles. These screenshots serve as the reference for future regression testing.

| Capture | Description | Camera Setup |
|---------|-------------|-------------|
| **Front** | Primary face of the asset as seen from the street/sidewalk. | Eye-level, 5m distance, centered on asset. |
| **Side Left** | Left profile. | Eye-level, 5m distance, 90 degrees left of front. |
| **Side Right** | Right profile. | Eye-level, 5m distance, 90 degrees right of front. |
| **Top-Down** | Overhead view showing footprint and placement context. | Directly above, altitude = 2x asset height. |
| **Context Wide** | Asset in its environment with surrounding buildings and props. | Eye-level, 20m distance, showing street context. |
| **Night** | Asset under nighttime lighting conditions. | Same as Front, but at 10:00 PM lighting. |
| **Wet** | Asset with wet weather surface treatment. | Same as Front, but with rain surface enabled. |

**Process:**
1. Place standardized camera rig at asset location.
2. Capture all 7 angles at runtime resolution.
3. Store as `regression/<entity_id>/baseline/` with ISO 8601 datestamp.
4. Record rendering settings (quality preset, LOD forced to 0, lighting state).

**Output:** 7 baseline screenshots per asset, stored with metadata.

**Failure Action:** If screenshots reveal visual issues (z-fighting, texture errors, scale problems), return to the relevant earlier step. Do not proceed with visually broken assets.

---

### Step 9: Sign-Off by Human Reviewer

**What:** A human reviewer examines the asset and all previous checklist outputs, then formally approves or rejects the asset for canonicalization.

| Review Item | Reviewer Checks |
|-------------|----------------|
| **Placement** | Does the asset look right in its location? Does it match reference photography? |
| **Scale** | Does the asset feel correct in scale relative to the player and surroundings? |
| **Collision** | Walk test and drive test results reviewed. Any edge cases? |
| **LODs** | Transition is smooth. No obvious quality gaps. |
| **Identity** | Ledger entry is correct. Entity ID follows convention. |
| **Materials** | Footstep sounds are correct. Physics responses feel right. |
| **Labels** | Taxonomy is accurate. Affordances match design intent. |
| **Visuals** | Baseline screenshots look correct. No artifacts. |
| **Context** | Asset fits the overall visual quality bar of the scene. Not out of place. |

**Approval Process:**
1. Reviewer opens the asset review package (generated from steps 1-8).
2. Reviewer inspects each checklist item.
3. Reviewer loads the asset in the game editor and performs a manual visual inspection.
4. Reviewer either:
   - **Approves:** Stamps the asset with approval date, reviewer ID, and any notes. Asset is moved from `/suggestive/` to `/canonical/` (or flagged as canonical if already in pipeline).
   - **Rejects with feedback:** Provides specific notes on what must change. Asset returns to the appropriate checklist step.
   - **Rejects permanently:** Asset is archived with reason. Entity ID is not reused.

**Output:** Approval stamp in asset metadata:

```json
{
  "canonical": true,
  "approved_by": "reviewer:jsmith",
  "approved_at": "2026-01-27T16:00:00Z",
  "checklist_version": "v0",
  "notes": "Approved. Minor note: consider adjusting awning drape in future polish pass.",
  "source": "promoted_from:sug_hotdog_cart_7av_v3",
  "checklist_results": {
    "step_1_placement": "pass",
    "step_2_scale": "pass",
    "step_3_collision": "pass",
    "step_4_lod": "pass",
    "step_5_identity": "pass",
    "step_6_materials": "pass",
    "step_7_labels": "pass",
    "step_8_regression": "pass",
    "step_9_signoff": "approved"
  }
}
```

**Failure Action:** Rejection returns to the flagged step. The cycle repeats until approval or permanent rejection.

---

## 4. Canonicalization Flow Diagram

```
  SUGGESTIVE ASSET                                                    CANONICAL ASSET
  (/suggestive/)                                                      (/canonical/)
       |                                                                    ^
       v                                                                    |
  [1. Georeference]                                                         |
       |                                                                    |
       v                                                                    |
  [2. Scale Check]                                                          |
       |                                                                    |
       v                                                                    |
  [3. Collision Proxy]                                                      |
       |                                                                    |
       v                                                                    |
  [4. LOD Chain]                                                            |
       |                                                                    |
       v                                                                    |
  [5. Ledger Identity]                                                      |
       |                                                                    |
       v                                                                    |
  [6. Material Props]                                                       |
       |                                                                    |
       v                                                                    |
  [7. Semantic Labels]                                                      |
       |                                                                    |
       v                                                                    |
  [8. Visual Regression]                                                    |
       |                                                                    |
       v                                                                    |
  [9. Human Sign-Off] ---APPROVED---> Promote to /canonical/ + Ledger entry-+
       |
       |---REJECTED---> Return to flagged step (loop)
       |
       |---REJECTED PERMANENTLY---> Archive with reason
```

Any step failure returns the asset to the world model or manual pipeline with specific feedback. The flow is strictly sequential — no step may be parallelized or skipped, because each step depends on the outputs of the previous one.

---

## 5. Asset Tier System for Times Square

Not all assets in the Times Square slice receive the same level of attention. The tier system defines build quality targets based on an asset's importance, visibility, and gameplay role.

### 5.1 Tier Definitions

---

#### Tier 1: Hero Assets

**Description:** The most important, most visible, most interacted-with assets in the slice. These define the visual identity of Twin Earth NYC's Times Square. Players will scrutinize them closely, photograph them, and use them as navigation landmarks.

| Property | Value |
|----------|-------|
| **Build Method** | Photogrammetry scan or Gaussian splat capture, followed by manual cleanup, retopology, and PBR material authoring. |
| **Triangle Budget** | 50,000 - 500,000 per asset (LOD 0) |
| **Texture Resolution** | 4K per material (8K for hero surfaces like TKTS signage) |
| **Collision Quality** | Hand-modeled collision proxy. Every step, rail, and surface is walkable/climbable as designed. |
| **LOD Levels** | 4 (LOD 0/1/2/3 with smooth transitions) |
| **Georeference Tolerance** | 0.05m (5cm) |
| **Scale Tolerance** | +/- 2% |
| **Canonicalization** | Full 9-step checklist, senior reviewer sign-off |
| **Update Frequency** | Rarely. Changes require design lead approval. |

**Examples:**

| Asset | Description | Why Hero |
|-------|-------------|----------|
| **TKTS Steps** | The iconic red steps in Duffy Square. | Central landmark. Player gathers evidence here. NPC gathering point. Most photographed structure. |
| **One Times Square** | The building at the south end where the ball drops. | Iconic silhouette. Defines the south boundary of the visual identity. |
| **Key Storefronts (5-8)** | Recognizable brand facades (TGI Friday's, M&M World, etc.). | Player uses these for navigation and reality-verification. Must match real world closely. |
| **Major Intersections (3)** | 7th/45th, 7th/44th, Broadway/45th. | Gameplay happens here. Traffic, anomalies, chases. Must be geometrically perfect. |
| **Police Station / Key Interior** | If present, the player's home base. | Repeated interaction. Must feel real and detailed. |

---

#### Tier 2: Mid-Distance Assets

**Description:** Assets that are clearly visible and contribute to the scene's believability but are not the primary focus of player attention. Players will see them at 10-50m and occasionally approach for closer inspection.

| Property | Value |
|----------|-------|
| **Build Method** | Procedural generation from reference photos, with texture transfer from scan data. Manual touch-up on visible faces only. |
| **Triangle Budget** | 5,000 - 50,000 per asset (LOD 0) |
| **Texture Resolution** | 2K per material |
| **Collision Quality** | Auto-generated collision proxy with manual correction for walkable surfaces. |
| **LOD Levels** | 3 (LOD 0/1/2 — LOD 3 merged into city-block LOD) |
| **Georeference Tolerance** | 0.25m (25cm) |
| **Scale Tolerance** | +/- 5% |
| **Canonicalization** | Full 9-step checklist, standard reviewer sign-off |
| **Update Frequency** | Occasional. Changes require pipeline lead approval. |

**Examples:**

| Asset | Description | Why Mid |
|-------|-------------|---------|
| **Secondary Facades** | Building fronts on the cross-streets (44th, 45th, 46th). | Visible but not hero. Players walk past, not toward. |
| **Side-Street Frontage** | Shops and restaurants on 44th-46th between Broadway and 8th Ave. | Background context. Some are explorable, but not primary destinations. |
| **Standard Street Furniture** | Generic trash cans, benches, newspaper boxes. | Common props. Players notice if wrong but don't inspect closely. |
| **Standard Vehicles** | Parked cars, buses, typical taxis in traffic. | Must look real at passing distance. Not individually scrutinized. |
| **Secondary Billboards** | Smaller signs, awning text, window displays. | Contribute to visual density. Legible at 10-20m. |

---

#### Tier 3: Skyline Assets

**Description:** Distant buildings and background elements that define the horizon and silhouette of the city. Players see them constantly but never approach them. Their shape matters more than their detail.

| Property | Value |
|----------|-------|
| **Build Method** | Generative patching from aerial/satellite imagery, with silhouette locked to photogrammetry reference. Detail is painted, not modeled. |
| **Triangle Budget** | 500 - 5,000 per asset (LOD 0, which is already simplified) |
| **Texture Resolution** | 1K per material (often atlas-packed with neighbors) |
| **Collision Quality** | None. Skyline assets are visual only — no collision, no navigation. |
| **LOD Levels** | 2 (LOD 0 = block model, LOD 1 = billboard/impostor) |
| **Georeference Tolerance** | 1.0m (1 meter) |
| **Scale Tolerance** | +/- 10% (but silhouette must match reference) |
| **Canonicalization** | Steps 1, 2, 4, 7, 8, 9 only (no collision, no ledger, no materials) |
| **Update Frequency** | Rare. Silhouette changes require art lead approval. |

**Examples:**

| Asset | Description | Why Skyline |
|-------|-------------|------------|
| **Distant Buildings** | Office towers, hotels, and residential buildings beyond the playable slice. | Visible from Times Square but unreachable. Define the Manhattan skyline. |
| **Background Silhouettes** | Building outlines against the sky at 500m+. | Shape recognition only. No detail needed. |
| **Distant Landmarks** | Empire State Building, Chrysler Building (visible from some angles). | Must be recognizable by silhouette. Detail irrelevant at distance. |
| **Sky Elements** | Cloud layers, aircraft, distant cranes. | Atmosphere and life. Lowest priority. |

### 5.2 Tier Decision Matrix

When an asset's tier is ambiguous, use this decision matrix:

```
Is the asset within 15m of a primary gameplay location?
  YES --> Is the asset interactable or a navigation landmark?
    YES --> TIER 1 (Hero)
    NO  --> TIER 2 (Mid)
  NO  --> Is the asset within the playable slice?
    YES --> Is it on a primary street (Broadway, 7th Ave)?
      YES --> TIER 2 (Mid)
      NO  --> Is it visible from a primary street?
        YES --> TIER 2 (Mid) or TIER 3 (Skyline) based on distance
        NO  --> TIER 3 (Skyline)
    NO  --> TIER 3 (Skyline)
```

### 5.3 Tier Budget Summary

| Tier | Asset Count (est.) | Total Triangle Budget | Total Texture Memory | Build Time Per Asset |
|------|-------------------|----------------------|---------------------|---------------------|
| Tier 1 (Hero) | 15 - 25 | 2M - 8M triangles | 2 - 4 GB | 2 - 5 days |
| Tier 2 (Mid) | 100 - 200 | 2M - 6M triangles | 1 - 3 GB | 0.5 - 2 days |
| Tier 3 (Skyline) | 50 - 100 | 100K - 500K triangles | 200 - 500 MB | 0.5 - 1 day |
| **Total** | **165 - 325** | **4M - 14.5M triangles** | **3.2 - 7.5 GB** | |

---

## 6. Promotion Audit Trail

Every canonicalized asset carries a permanent record of its journey from suggestive to canonical. This audit trail is stored in the ledger and cannot be modified after creation.

```json
{
  "entity_id": "entity:hydrant-7av-45st-001",
  "promotion_record": {
    "suggestive_source": "sug_hydrant_7av_45st_v2.fbx",
    "suggestive_created": "2026-01-15T10:00:00Z",
    "suggestive_source_type": "world_model_proposal",
    "proposal_id": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
    "checklist_started": "2026-01-20T09:00:00Z",
    "checklist_completed": "2026-01-27T15:30:00Z",
    "step_results": {
      "1_georeference": { "pass": true, "offset_m": 0.03, "date": "2026-01-20T09:15:00Z" },
      "2_scale": { "pass": true, "max_deviation_pct": 1.8, "anchors_used": 3, "date": "2026-01-20T10:00:00Z" },
      "3_collision": { "pass": true, "walk_test": "pass", "drive_test": "pass", "date": "2026-01-21T11:00:00Z" },
      "4_lod": { "pass": true, "levels": 4, "transition_score": 0.96, "date": "2026-01-22T14:00:00Z" },
      "5_identity": { "pass": true, "entity_id": "entity:hydrant-7av-45st-001", "date": "2026-01-23T09:00:00Z" },
      "6_materials": { "pass": true, "surface_type": "metal", "friction": 0.4, "date": "2026-01-24T10:00:00Z" },
      "7_labels": { "pass": true, "taxonomy": "street_furniture.hydrant", "affordances": ["cover_point"], "date": "2026-01-25T11:00:00Z" },
      "8_regression": { "pass": true, "screenshots": 7, "date": "2026-01-26T15:00:00Z" },
      "9_signoff": { "pass": true, "reviewer": "reviewer:jsmith", "date": "2026-01-27T15:30:00Z" }
    },
    "canonical_path": "canonical/street_furniture/hydrant-7av-45st-001/",
    "tier": 2
  }
}
```

---

## 7. Contamination Detection

To enforce the No Contamination Rule, the following automated checks run continuously:

| Check | Frequency | Method | Action on Failure |
|-------|-----------|--------|------------------|
| **Path scan** | Every build | Verify no `/suggestive/` asset is referenced by any runtime system. | Build fails. Alert asset pipeline lead. |
| **Metadata scan** | Every build | Verify all loaded assets have `"canonical": true` in metadata. | Build fails. Identify offending asset. |
| **Collision audit** | Nightly | Verify all collision meshes trace back to a canonicalized asset. | Report orphaned collision. Quarantine. |
| **Ledger reference audit** | Nightly | Verify all entity IDs in ledger resolve to existing canonical assets. | Report orphaned references. Flag for cleanup. |
| **File prefix check** | Every commit | Verify files in `/canonical/` have `can_` prefix, files in `/suggestive/` have `sug_` prefix. | Commit rejected. Developer notified. |
| **Cross-reference check** | Weekly | Verify no canonical asset's dependencies point to suggestive assets. | Report dependency violation. Flag for remediation. |

---

*End of document. Next: `alpha-evolve-eval-suite-v0.md`*
