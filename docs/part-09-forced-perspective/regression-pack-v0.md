# Regression Pack v0

**Twin Earth NYC -- Part 9: Forced Perspective**
**Document:** Regression Test Pack, Camera Positions, Walk Test Route, and Truth Firewall
**Version:** 0.1.0
**Status:** Draft
**Last Updated:** 2026-01-27

---

## 1. Purpose

The forced perspective system is fragile by design -- it achieves visual fidelity through controlled deception. Any change to geometry, LOD thresholds, streaming logic, or asset data can break the illusion in ways that are difficult to detect through automated unit tests alone. This document defines a comprehensive regression testing framework: fixed camera positions for screenshot comparison, a standardized capture protocol, a checklist of regression checks, a walk test route, and the Truth Firewall that defines what the illusion layer is never permitted to alter.

---

## 2. Fixed Camera Positions (10)

These cameras define canonical viewpoints used for screenshot-based regression testing. Each camera has a fixed world-space position, rotation, and field of view. They are placed to cover every major sightline, LOD transition zone, seam location, and visual landmark in the Times Square slice.

| Camera ID | Position (Description) | World Coords (X, Y, Z) | Look Direction | FOV | Purpose |
|-----------|----------------------|------------------------|----------------|-----|---------|
| **CAM_REG_01** | 42nd St / Broadway, NW corner sidewalk | (0, 1.7, 0) | North (bearing 0 deg) up Broadway | 75 deg | Street-level perspective looking into the slice. Tests Broadway sightline, near-band billboards, One Times Square silhouette, street width proportions. |
| **CAM_REG_02** | TKTS Red Steps, top tier center | (85, 4.5, 120) | South (bearing 180 deg) | 90 deg | Elevated overview of the intersection. Tests crowd density, bowtie geometry, billboard ring, vehicle flow. **Also used for 30-second motion artifact video.** |
| **CAM_REG_03** | 44th St / 7th Ave, SE corner | (-40, 1.7, 200) | East (bearing 90 deg) toward bowtie | 75 deg | Cross-street perspective. Tests 7th Ave width, mid-distance facade motifs (Family A glass towers), side-street support zone transition. |
| **CAM_REG_04** | 45th St pedestrian zone, center | (30, 1.7, 280) | South (bearing 180 deg) | 75 deg | Density and signage check. Tests pedestrian zone props, background billboard density, crowd near/mid transition, signage readability. |
| **CAM_REG_05** | One Times Square, base (south side sidewalk) | (50, 1.7, 80) | Up (pitch 70 deg) | 90 deg | Extreme vertical perspective. Tests scale anchor accuracy (building height), billboard tier at close range (BB_H01 must be T0), vertical LOD transition. |
| **CAM_REG_06** | 46th St / Broadway, SW corner | (20, 1.7, 360) | South (bearing 180 deg) | 75 deg | Long sightline down Broadway. Tests full LOD gradient (near -> mid -> far visible in single frame), distant silhouette stability, haze/atmosphere. |
| **CAM_REG_07** | 42nd St subway entrance (S06) | (60, 0.5, 10) | West (bearing 270 deg) | 75 deg | Ground-level seam check. Tests subway entrance seam (S06), ground-plane collision alignment, near-band street detail, southern boundary seam (S03) visible in periphery. |
| **CAM_REG_08** | Center of bowtie intersection | (50, 1.7, 160) | 360 deg panoramic | 360 deg | Full-surround reference. Captured as equirectangular panorama. Tests all directions simultaneously. Verifies that no seam is visible from the center of the stage. **Also used for 30-second motion artifact video (rotating).** |
| **CAM_REG_09** | Marriott Marquee entrance (45th St) | (-10, 1.7, 280) | East-southeast (bearing 110 deg) across 45th | 75 deg | Mid-distance facade check. Tests Marriott sign (BB_H05) tier, Family B brick heritage motifs on 45th St buildings, seam S07 (Marquee lobby door) appearance. |
| **CAM_REG_10** | 47th St, north boundary center | (30, 1.7, 440) | South (bearing 180 deg) | 75 deg | Full slice overview from maximum distance. Tests far-band LOD for entire slice, seam S04 (north boundary) not visible behind camera, skyline silhouette stability. |

**Note:** World coordinates are illustrative and will be finalized when the slice geometry is baselined. The relative positions and look directions are the binding specification.

---

## 3. Capture Protocol

### 3.1 Conditions Matrix

Each camera position is captured under three environmental conditions, producing a total of **30 baseline screenshots** (10 cameras x 3 conditions).

| Condition ID | Label | Time of Day | Weather | Special State |
|--------------|-------|-------------|---------|---------------|
| **COND_A** | Baseline Midday | 12:00 (sun at zenith) | Clear sky, no precipitation | Normal gameplay state, standard crowd density, all billboards nominal |
| **COND_B** | Rainy Night | 22:00 (full dark) | Heavy rain, wet surfaces, reflections active | Night billboard glow at full intensity, rain particle system active, reduced crowd density (rain modifier) |
| **COND_C** | Anomaly Event | 14:00 (overcast) | Anomaly atmospheric distortion (color shift, particle effects) | Portal active at S10, billboard content overridden with anomaly messages (BB_H02, BB_H04), heightened light spill (2.5x multiplier) |

### 3.2 Capture Specifications

| Parameter | Value |
|-----------|-------|
| **Resolution** | 1920 x 1080 (Full HD) |
| **Format** | PNG (lossless compression) |
| **Color Space** | sRGB, 8-bit per channel |
| **Anti-aliasing** | TAA enabled (standard game settings) |
| **Post-processing** | All enabled at default settings (bloom, DOF, color grading, AO) |
| **HUD** | Disabled (clean capture, no UI elements) |
| **Frame timing** | Capture after scene has been stable for 2 seconds (no in-progress LOD transitions) |

### 3.3 File Naming Convention

```
REG_{camera_id}_{condition}_{version}.png
```

**Examples:**
- `REG_CAM_REG_01_COND_A_v0.1.0.png`
- `REG_CAM_REG_08_COND_B_v0.1.0.png`
- `REG_CAM_REG_05_COND_C_v0.1.0.png`

### 3.4 Video Captures

In addition to the 30 screenshots, two video captures are required:

| Video ID | Camera | Duration | Content | Format |
|----------|--------|----------|---------|--------|
| **VID_REG_01** | CAM_REG_02 (TKTS top) | 30 seconds | Static camera, observing crowd flow, vehicle movement, billboard animation, LOD transitions in mid-band | 1080p, 30fps, H.264, CRF 18 |
| **VID_REG_02** | CAM_REG_08 (bowtie center) | 30 seconds | 360 deg slow rotation (12 deg/s = full rotation in 30 s), observing all directions for LOD pop-in, seam visibility, billboard tier changes | Equirectangular 4096x2048, 30fps, H.264, CRF 18 |

### 3.5 Capture Folder Structure

```
twin-earth-nyc/
  regression/
    screenshots/
      v0.1.0/
        REG_CAM_REG_01_COND_A_v0.1.0.png
        REG_CAM_REG_01_COND_B_v0.1.0.png
        REG_CAM_REG_01_COND_C_v0.1.0.png
        ... (30 files total)
    videos/
      v0.1.0/
        VID_REG_01_COND_A_v0.1.0.mp4
        VID_REG_02_COND_A_v0.1.0.mp4
    baselines/
      v0.1.0/
        (copy of screenshots used as comparison baseline)
    diffs/
      v0.1.0_vs_v0.2.0/
        (generated diff images from regression comparison)
```

---

## 4. Regression Checks

### 4.1 Automated and Semi-Automated Checks

Each regression check defines a method, pass criteria, and the cameras/conditions against which it is evaluated.

| # | Check | Method | Pass Criteria | Cameras | Conditions |
|---|-------|--------|---------------|---------|------------|
| **RC-01** | Silhouette stability | Edge detection (Canny filter) on current screenshot vs. baseline. Compare edge maps using structural similarity index (SSIM). | SSIM > 0.97 (< 3% pixel deviation in edge map) | All 10 | All 3 |
| **RC-02** | Scale anchor accuracy | Automated measurement of known objects in screenshot using reference markers. Measure pixel height of doors (2.1 m truth), standing NPCs (1.75 m truth), and taxis (4.8 m truth) visible in frame. | All measured objects within +/- 5% of expected pixel size (derived from camera FOV and distance) | CAM_REG_01, 03, 04, 05 | COND_A |
| **RC-03** | Billboard tier correctness | For each billboard visible in frame, verify its tier matches the tiering rules (distance-based). Inspector overlay shows billboard ID, current tier, and expected tier. | All billboards match expected tier. Zero mismatches. | CAM_REG_01, 02, 05, 06, 10 | All 3 |
| **RC-04** | LOD transition smoothness | Review VID_REG_01 and VID_REG_02 for pop-in artifacts. Frame-by-frame analysis flags any single-frame geometry appearance/disappearance (instant swap without cross-fade). | No instant LOD transitions detected. All transitions use cross-fade or disguise rules from LOD Motif Library. | VID_REG_01, VID_REG_02 | COND_A |
| **RC-05** | Crowd density plausibility | Count pedestrian NPCs visible in near zone (0--30 m from camera). Compare to target density from crowd system specification. | Count within +/- 20% of target density for the given condition (COND_B has reduced density due to rain). | CAM_REG_02, 04 | All 3 |
| **RC-06** | Seam invisibility | Inspect all 10 seam locations in screenshots and video. Check for visible boundaries, missing mask geometry, z-fighting, or void exposure. | No visible seam artifacts at any location. All masks present and rendering correctly. | CAM_REG_01 (S03), 03 (S01), 06 (S04), 07 (S06, S03), 09 (S07), 10 (S04) | All 3 |
| **RC-07** | Lighting consistency | Extract shadow direction from 3+ shadow-casting objects across multiple cameras. Compare shadow angle to expected sun position for the condition's time of day. | Shadow direction consistent across all cameras within +/- 2 deg. No contradictory shadow directions. | CAM_REG_01, 03, 04, 06 | COND_A, COND_C |
| **RC-08** | Collision parity | Automated walk test: AI-controlled character walks the regression route (Section 5). Record character height (Y position) relative to visual ground plane at 100 sample points. | Character Y position within +/- 0.05 m of visual ground at all sample points. No floating (character above ground) or sinking (character below ground). | Walk test route (not camera-specific) | COND_A |

### 4.2 Pass/Fail Summary Table (Template)

| Check | Build Version | Result | Notes |
|-------|--------------|--------|-------|
| RC-01: Silhouette stability | v_._._  | PASS / FAIL | |
| RC-02: Scale anchor accuracy | v_._._  | PASS / FAIL | |
| RC-03: Billboard tier correctness | v_._._  | PASS / FAIL | |
| RC-04: LOD transition smoothness | v_._._  | PASS / FAIL | |
| RC-05: Crowd density plausibility | v_._._  | PASS / FAIL | |
| RC-06: Seam invisibility | v_._._  | PASS / FAIL | |
| RC-07: Lighting consistency | v_._._  | PASS / FAIL | |
| RC-08: Collision parity | v_._._  | PASS / FAIL | |
| **Overall** | v_._._  | **PASS / FAIL** | All checks must pass for overall PASS |

---

## 5. Walk Test Route

### 5.1 Route Description

The walk test is a standardized traversal of the entire Show Street zone, designed to exercise every major sightline, LOD transition, seam proximity, and crowd interaction in the slice.

**Total distance:** approximately 800 m
**Expected duration:** approximately 10 minutes at walk speed (1.4 m/s)

### 5.2 Waypoints

| Waypoint | Location | Action | What to Observe |
|----------|----------|--------|-----------------|
| **WP-01** | CAM_REG_01 position (42nd / Broadway NW) | Start. Face north. Begin walking. | Southern boundary seam S03 should be visible as construction barriers behind the player. |
| **WP-02** | One Times Square base (south side) | Pause 3 s. Look up at BB_H01. | Billboard should be T0 (full video). Scale anchor check: building reads as correct height. |
| **WP-03** | TKTS Red Steps base | Walk up steps to top. Pause 3 s at top. | Steps geometry matches collision (no floating). Crowd visible in all distance bands from elevated position. |
| **WP-04** | Bowtie intersection center | Walk to center of intersection. Pause 2 s. Look 360 deg. | All billboards visible. No seams visible from center. LOD ring visible (near detail fading to mid). |
| **WP-05** | 44th St / Broadway | Turn west on 44th St. Walk toward 7th Ave. | Side street transition from Show Street to Support Zone. Detail should reduce subtly. Seam S05 (alley) visible on left -- masked by dumpsters/gate. |
| **WP-06** | 44th St / 7th Ave intersection | Arrive at 7th Ave. Turn north. | Western boundary seam S01 visible across 7th Ave -- masked by scaffolding. Support Zone facades on 7th Ave should be mid-band, upgrading to near as approached. |
| **WP-07** | 45th St / 7th Ave | Continue north. Pass Marriott Marquee. | BB_H05 (Marquee sign) should be T0 at this range. Seam S07 (lobby doors) visible -- glass reflection mask in place. |
| **WP-08** | 46th St / 7th Ave | Continue north. Approach BB_H08. | BB_H08 should transition from T1 to T0 as player approaches (within 30 m). Cross-fade should be smooth. |
| **WP-09** | 46th St, turn east toward Broadway | Turn east on 46th. Walk toward Broadway. | Observe LOD gradient: near detail around player, mid-distance motifs (Family C commercial signage) on Broadway facades ahead. |
| **WP-10** | 46th St / Broadway | Arrive at Broadway. Turn south. | Long sightline down Broadway. Far-band buildings at south end of slice. Silhouette stability check. |
| **WP-11** | Walk south on Broadway to 44th St | Walk south along Broadway east sidewalk. | Observe billboard transitions as distance changes. Background billboards (BB_B01--B05) on west side should cycle through tiers. No pop-in within 20 m. |
| **WP-12** | 44th St / Broadway, Portal alley (S10) | Approach portal zone near alley. | Anomaly distortion visible at S10 (if anomaly condition active). Seam S08 (service entrance) visible across the alley -- steel door mask in place. |
| **WP-13** | Continue south on Broadway to 42nd St | Walk south to starting position. | Approach southern boundary. Seam S03 barriers should resolve at full detail. Subway entrance S06 visible -- stairs and darkness. |
| **WP-14** | Return to WP-01 | End at starting position. | Full loop complete. |

### 5.3 Walk Test Acceptance Criteria

| Criterion | Requirement |
|-----------|-------------|
| **NPC Pop-in** | No NPC (L0 or L1) appears or disappears within 20 m of the player without a disguise (cross-fade, crowd screen, or motion occlusion). |
| **Collision** | No collision snags (player stuck on invisible geometry). No falling through ground. No floating above ground (> 0.05 m gap). |
| **Visual Quality** | No obvious rendering artifacts: z-fighting, texture stretching, missing geometry, black faces, flickering. |
| **Seam Integrity** | All 10 seams encountered or visible during the walk are properly masked. No void, no invisible walls without visual justification. |
| **Performance** | Frame rate remains above 30 FPS throughout the walk. No frame time spikes > 50 ms. |
| **Billboard Behavior** | Billboard tier transitions match distance rules. No billboard stuck in wrong tier. |

---

## 6. Truth Firewall

### 6.1 Definition

The Truth Firewall is a strict boundary between the truth layer and the illusion layer. It defines five categories of data that the illusion layer is **absolutely prohibited from altering**. Violations of the Truth Firewall are treated as critical bugs -- equivalent to a security vulnerability in a network system.

### 6.2 Protected Categories

| # | Protected Element | Description | Why It Cannot Be Altered |
|---|-------------------|-------------|--------------------------|
| **TF-01** | **Collision Meshes** | The navmesh (used for AI and player pathfinding) and physics collision hulls (used for rigid-body simulation and raycasts). These define the physical shape of the world. | Gameplay fairness depends on physical consistency. If the illusion layer could reshape collision, cover would be unreliable, pathfinding would diverge from visible geometry, and physics puzzles would become unsolvable. The navmesh and collision hulls are authored from truth-layer survey data and are immutable at runtime. |
| **TF-02** | **Anchor Coordinates** | The world-space position of all registered anchors: scale anchors (doors, humans, taxis), placement anchors (traffic lights, TKTS steps, Marriott sign), and sightline anchors (camera positions). | Anchors are the fixed reference points that the entire forced perspective system calibrates against. Moving an anchor would cascade errors through LOD selection, invariant checks, and regression tests. Anchor positions are set during slice authoring and locked. |
| **TF-03** | **Ledger-Committed States** | All persistent game state stored in the ledger system: quest progress, inventory, world-state flags, NPC relationship values, and player statistics. | Persistence integrity is fundamental to gameplay trust. The illusion layer renders visual representations of state but cannot modify the state itself. A quest flagged as complete in the ledger remains complete regardless of what the illusion layer shows. |
| **TF-04** | **Entity Identity** | The unique identifier (entity ID) of every managed entity in the world. The illusion layer can change an entity's visual appearance (LOD swap, motif instance, proxy replacement) but cannot change its identity. Entity ID = truth-layer assignment. | AI systems, quest scripts, and the event ledger reference entities by ID. If the illusion layer could reassign IDs (e.g., swapping one NPC's identity to another during a proxy swap), it would break quest targeting, dialogue trees, and AI memory. |
| **TF-05** | **Sensor Occlusion** | What blocks line-of-sight, hearing, and detection between entities is determined exclusively by truth-layer collision geometry. The illusion layer's render meshes (which may be simplified, proxied, or absent) have no effect on sensor calculations. | AI fairness and stealth gameplay require that occlusion is consistent with truth. A wall that is visually simplified (or even culled from rendering) still blocks AI vision. Conversely, a decorative illusion-layer element (a holographic sign, a volumetric fog effect) does not block sensors unless it has a truth-layer collision hull. |

### 6.3 Enforcement Mechanism

The Truth Firewall is enforced at three levels:

**Level 1 -- API Boundary:**
The illusion layer accesses truth-layer data through a read-only API. There are no write methods exposed. The illusion layer can query collision geometry, anchor positions, ledger states, entity IDs, and sensor results, but cannot modify them.

```
// Illusion Layer API (read-only)
interface TruthLayerQuery {
    getCollisionMesh(entityId): CollisionHull    // read-only
    getAnchorPosition(anchorId): Vector3          // read-only
    getLedgerState(key): StateValue               // read-only
    getEntityId(entity): EntityId                 // read-only
    querySensorOcclusion(from, to): OcclusionResult  // read-only
}

// NO write methods. No setCollisionMesh(). No setAnchorPosition().
// Compile-time enforcement: illusion layer module cannot import truth-layer write APIs.
```

**Level 2 -- Runtime Assertions:**
Every frame, a subset of truth-layer values are checksummed and compared against the previous frame's checksum. If any protected value has changed and the change did not originate from an authorized truth-layer system (physics engine, quest script, game logic), an assertion fires.

```python
def truth_firewall_check():
    for anchor in all_anchors:
        assert anchor.position == anchor.baseline_position, \
            f"FIREWALL VIOLATION: Anchor {anchor.id} moved from {anchor.baseline_position} to {anchor.position}"

    for entity in managed_entities:
        assert entity.id == entity.truth_id, \
            f"FIREWALL VIOLATION: Entity identity changed from {entity.truth_id} to {entity.id}"

    collision_checksum = compute_checksum(all_collision_meshes)
    assert collision_checksum == last_frame_collision_checksum, \
        "FIREWALL VIOLATION: Collision mesh modified outside truth layer"
```

**Level 3 -- Build-Time Invariant Check:**
Before every build is promoted to a testable state, the following automated checks run:

1. Run all 10 invariant constraint tests from the Show Director Spec (INV-01 through INV-10).
2. Execute the full walk test route (Section 5) with automated acceptance criteria evaluation.
3. Capture all 30 regression screenshots and compare against baseline.
4. Run Truth Firewall assertion suite for 60 seconds of simulated gameplay.
5. **Any single failure flags the build for mandatory human review.** The build cannot be promoted without resolution.

### 6.4 Violation Severity

| Violation Type | Severity | Response |
|----------------|----------|----------|
| Collision mesh altered by illusion layer | **Critical** | Build rejected. Immediate investigation. |
| Anchor coordinate drift | **Critical** | Build rejected. Anchor re-survey required. |
| Ledger state corruption | **Critical** | Build rejected. Data integrity audit. |
| Entity ID reassignment | **High** | Build flagged. Must be resolved before next milestone. |
| Sensor occlusion inconsistency | **High** | Build flagged. AI team review required. |
| Invariant test failure (INV-01 through INV-10) | **Medium** | Build flagged. May ship to internal test with known issue documented. |
| Regression screenshot deviation (RC-01 through RC-08) | **Medium** | Build flagged. Human review determines if deviation is acceptable (intentional art change) or regression. |

---

## 7. Pre-Build Checklist

The following checklist is executed before every build promotion. All items must pass for the build to advance.

- [ ] **INV-01:** Street widths within +/- 0.5 m (automated overhead measure)
- [ ] **INV-02:** Door/window scale cues within +/- 5% (screenshot comparison)
- [ ] **INV-03:** One Times Square silhouette within 2 deg / 3% (edge detection)
- [ ] **INV-04:** TKTS Red Steps position within +/- 0.25 m (anchor check)
- [ ] **INV-05:** Marriott Marquee sign zone within +/- 1.0 m (overlay)
- [ ] **INV-06:** Traffic signal positions within +/- 0.5 m (anchor check)
- [ ] **INV-07:** Sidewalk-road boundaries within +/- 0.3 m (collision overlay)
- [ ] **INV-08:** Broadway/7th intersection angles within +/- 1 deg (overhead compare)
- [ ] **INV-09:** Key sightlines qualitative pass (human review, 3 reviewers)
- [ ] **INV-10:** Billboard placement zones within +/- 1.0 m (overlay)
- [ ] **RC-01:** Silhouette stability SSIM > 0.97
- [ ] **RC-02:** Scale anchor accuracy within +/- 5%
- [ ] **RC-03:** Billboard tier correctness: zero mismatches
- [ ] **RC-04:** LOD transition smoothness: no instant swaps detected
- [ ] **RC-05:** Crowd density within +/- 20% of target
- [ ] **RC-06:** Seam invisibility: all 10 seams masked
- [ ] **RC-07:** Lighting consistency: shadows within +/- 2 deg
- [ ] **RC-08:** Collision parity: character within +/- 0.05 m of ground
- [ ] **Walk Test:** Full route completed, all acceptance criteria met
- [ ] **Truth Firewall:** 60 s assertion suite passed, zero violations
- [ ] **Performance:** Frame rate above 30 FPS throughout walk test, no spikes > 50 ms

**Build disposition:**
- All checks PASS: Build promoted to internal test.
- Any MEDIUM failure: Build promoted with known issue documented. Must resolve before milestone.
- Any HIGH or CRITICAL failure: **Build rejected.** Fix required before re-submission.

---

## 8. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1.0 | 2026-01-27 | Design Team | Initial draft -- camera positions, capture protocol, regression checks, walk test, truth firewall, pre-build checklist |

---

*End of Regression Pack v0*
