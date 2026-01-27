# LOD + Motif Library v0

**Twin Earth NYC -- Part 9: Forced Perspective**
**Document:** Level-of-Detail and Motif Library Specification
**Version:** 0.1.0
**Status:** Draft
**Last Updated:** 2026-01-27

---

## 1. Purpose

This document defines the LOD tier specifications for every asset class in the Times Square slice, the motif family system used to efficiently populate mid-distance facades, and the transition rules that prevent visible pop-in. Together with the Show Director Spec, this document forms the complete rendering-quality contract: the Director decides *which* LOD tier an entity should use; this library defines *what* each tier contains.

---

## 2. Asset-Class LOD Tables

### 2.1 Buildings

Buildings are the most complex asset class. Each building has up to four LOD tiers, with dramatic reductions in geometry, texture, and interactivity at each step.

| LOD Tier | Label | Geometry | Textures | Animation | Interaction |
|----------|-------|----------|----------|-----------|-------------|
| **L0** | Near | Full unique mesh. All architectural detail modeled: window frames, cornices, fire escapes, awnings, door recesses. Target: 50K--200K tris per building. | 4K PBR texture set (albedo, normal, roughness, metallic, emissive) per unique facade. Unique detail textures for signage, damage, and story-relevant features. | Window parallax (interior cubemap with depth offset). Door open/close animation. Awning flutter. Emissive sign flicker. | Doors openable (if mission-relevant). Windows breakable (if designated). Surface material queries (footstep audio). Cover points active for AI. |
| **L1** | Mid | Simplified mesh at ~50% triangle count of L0. Window recesses flattened to normal-map only. Fire escapes merged into facade. Awnings baked into geometry. Target: 25K--100K tris. | 2K atlas texture. Motif-instanced materials (shared across family members). No unique detail textures; signage zones use family-generic placeholders. | Static window parallax (reduced depth, no animation). No door animation. No flutter effects. | No direct interaction. Visual presence only. Cover points still registered in truth layer (collision mesh unchanged). |
| **L2** | Far | Box proxy with silhouette cap mesh. Building reduced to extruded footprint + roofline profile. Target: 500--2K tris. | 512 x 512 combined emissive + albedo texture. Single-sided, no PBR (emissive for lit windows, flat albedo for daylight). | None. Fully static geometry. | None. Truth-layer collision still exists but render is minimal. |
| **L3** | Culled | No geometry rendered. | No textures loaded. | None. | None. Truth-layer collision persists for physics/AI but no visual. |

### 2.2 Billboards

Times Square billboards are a signature visual element and require their own LOD pipeline due to the cost of video decoding.

| LOD Tier | Label | Content | Resolution | Audio | Interaction |
|----------|-------|---------|------------|-------|-------------|
| **L0** | Near | Full video playback at native framerate (30 fps target). Content sourced from billboard content library (looping video files or procedural shaders). | Native resolution, up to 1920 x 1080 per surface. Rendered to texture each frame. | 3D-positioned audio spill. Volume attenuates with distance (max audible range: 40 m). Spatial blend: 100% 3D. | Hackable in missions (player can alter content via gameplay mechanic). Scannable for intel. |
| **L1** | Mid | Low-FPS animated loop. Pre-cached keyframes extracted from source video. 5 frames per second. | 512 x 512 render target. Bilinear filtered. | No audio output. | None. |
| **L2** | Far | Single static emissive texture. Representative frame chosen from source content. | 256 x 256 emissive texture. | None. | None. |
| **L3** | Culled | Not rendered. | None. | None. | None. |

### 2.3 Street Props

Includes: traffic lights, street lamps, bollards, fire hydrants, mailboxes, newspaper boxes, benches, trash cans, planters, sign poles, parking meters.

| LOD Tier | Label | Geometry | Shadow | Collision |
|----------|-------|----------|--------|-----------|
| **L0** | Near | Full unique mesh. All hardware detail modeled (bolts, labels, wear marks). Target: 500--5K tris per prop depending on size. | Full shadow map contribution. Correct self-shadowing. | Full collision mesh matching visual geometry. Physics-active (can be knocked over if designated). |
| **L1** | Mid | LOD1 simplified mesh at ~25% triangle count. Small details removed (bolts, labels). Target: 125--1.25K tris. | Simplified shadow (reduced mesh, shadow bias increased). | Simplified collision hull (convex approximation). Not physics-active. |
| **L2** | Far | Billboard sprite or removed entirely (based on prop importance). Camera-facing quad for large props (traffic lights, lamps). Small props (hydrants, meters) removed. | No shadow contribution. | No collision geometry rendered. Truth-layer collision still present if prop is an anchor. |
| **L3** | Culled | Not rendered. | None. | None. Truth-layer collision persists. |

### 2.4 Crowds (NPCs)

| LOD Tier | Label | Representation | Animation | AI Behavior |
|----------|-------|----------------|-----------|-------------|
| **L0** | Near | Unique skeletal mesh. Full character model with individual clothing, accessories, skin tone variation. Hero NPCs: facial blend shapes, eye tracking, lip sync. Background NPCs: body animation only. Target: 5K--15K tris per character. | Full animation blend tree. Walk, idle, talk, phone-check, sit, look-around, react. Hero NPCs: facial animation, gesture system. Blend space driven by AI state. | **Hero NPCs:** Full sensor model (vision cone, hearing radius), behavior tree with state machine, dialogue capability, quest interaction. **Background NPCs:** Heuristic flow-follow with obstacle avoidance, context-appropriate idle selection, proximity reaction (step aside for player). |
| **L1** | Mid | Instanced archetypes. 20 visual variants (combinations of body type, clothing color, accessory). Shared skeletal rig. Target: 2K--4K tris per instance. | Walk cycle only. Single animation clip per archetype, playback rate varied +/- 10% to reduce lockstep appearance. No blend tree. | Simple flow-follow along predefined paths. No obstacle avoidance beyond path adherence. No player interaction. Despawn/respawn at zone boundaries. |
| **L2** | Far | Animated sprite cards. Camera-facing quads with pre-rendered walk cycle sprite sheets (8 frames, 4 directions). 2--4 visual variants. | Sprite sheet playback (sway and shuffle). Frame rate: 8 fps. | None. Particle-system-like behavior: spawn at emitter, flow along vector field, despawn at sink. No individual agency. |
| **L3** | Culled | Not rendered. | None. | None. |

### 2.5 Vehicles

| LOD Tier | Label | Geometry | Animation | Physics |
|----------|-------|----------|-----------|---------|
| **L0** | Near | Full unique mesh. Interior visible through windows. Wheel rotation, steering animation. Target: 15K--30K tris. | Wheel spin, suspension bob, turn signal blink, brake light response. | Full rigid-body physics. Collision with player and other vehicles. |
| **L1** | Mid | Simplified mesh (~40% tris). Interior removed (tinted windows). Target: 6K--12K tris. | Wheel spin only. No suspension. Brake lights binary (on/off). | On-rails movement along traffic spline. No physics collision with player (ghost through if somehow reached). |
| **L2** | Far | Low-poly proxy. No interior, merged wheels. Target: 500--1K tris. | None. Slides along spline without wheel animation. | None. Visual only. |
| **L3** | Culled | Not rendered. | None. | None. |

---

## 3. Motif Families -- Mid-Distance Facade System

### 3.1 Concept

At mid-distance (30--150 m), individual building facades are too far to read unique architectural details but close enough that their overall character matters. The **Motif Family** system groups buildings with similar architectural language into families that share modular facade components. This dramatically reduces unique texture memory and draw calls while preserving the visual variety of the streetscape.

Each family defines:
- A set of **floor modules** (horizontal slices of facade that can be stacked)
- A set of **edge modules** (corner and roofline treatments)
- A **color/material palette** (shared PBR parameters with per-building tint variation)
- **Tiling rules** (how modules combine to produce a plausible facade)

### 3.2 Family Definitions

#### Family A: "Glass Tower"

| Property | Value |
|----------|-------|
| **Member Buildings** | 4 buildings along 7th Avenue (north side, 43rd--46th St) |
| **Architectural Character** | Modern glass curtain wall. Blue-green tinted reflective panels. Regular grid of floor-to-ceiling windows. Minimal ornamentation. Steel mullion grid visible. |
| **Floor Modules** | 3 variants: (A1) standard office floor, (A2) mechanical floor (narrower windows, vents), (A3) lobby/retail floor (taller windows, canopy) |
| **Edge Modules** | 2 variants: (AE1) flat parapet with HVAC screen, (AE2) chamfered corner with accent lighting |
| **Tiling Rule** | Stack: A3 (ground) + A1 x N + A2 (every 8th floor) + A1 x M + AE1 or AE2 (top). N and M vary per building to match floor count. |
| **Color Palette** | Base: `#2A4858` (blue-green). Per-building tint: hue shift +/- 10 deg, brightness +/- 15%. Mullion: `#808080` metallic. |

#### Family B: "Brick Heritage"

| Property | Value |
|----------|-------|
| **Member Buildings** | 3 buildings along 45th--46th St (mid-block, between Broadway and 7th Ave) |
| **Architectural Character** | Pre-war red brick. Fire escape zigzags on facade. Irregular window rhythm (some bricked-in). Ornamental cornices. Water towers visible on roof. |
| **Floor Modules** | 4 variants: (B1) standard residential floor with paired windows, (B2) floor with fire escape landing, (B3) floor with bricked-in window (variation), (B4) commercial ground floor with storefront |
| **Edge Modules** | (BE1) ornamental cornice with dentil molding, (BE2) plain parapet. **Cap module:** water tower silhouette. |
| **Tiling Rule** | Stack: B4 (ground) + [B1, B2] alternating x N + B3 (random insertion, 1 per facade) + BE1 or BE2 (top) + water tower cap (50% chance). |
| **Color Palette** | Base: `#8B4513` (red-brown brick). Per-building tint: saturation +/- 20%, brightness +/- 10%. Fire escape: `#1A1A1A` (dark iron). |

#### Family C: "Commercial Signage"

| Property | Value |
|----------|-------|
| **Member Buildings** | 5 buildings along Broadway (both sides, 42nd--46th St) |
| **Architectural Character** | Mixed materials. Large billboard/sign zones dominating upper facades. Active retail ground floor with awnings. Highly varied -- unified by the dominance of signage over architecture. |
| **Floor Modules** | 2 base modules: (C1) retail ground floor with awning and window display, (C2) generic upper floor (often obscured by signage). **Sign panel:** (CS) large rectangular zone for billboard/signage overlay (occupies 2--4 floor heights). |
| **Edge Modules** | (CE1) flat top with rooftop signage frame. |
| **Tiling Rule** | Stack: C1 (ground) + C2 x 1--2 + CS (sign panel, spans multiple floors) + C2 x M + CE1 (top). Sign panel content is a separate billboard asset overlaid on the module. |
| **Color Palette** | Base: `#696969` (neutral gray -- most of facade is covered by signage). Awning colors: randomized per building from palette of 6 options. Sign panel: emissive overlay, not part of base material. |

### 3.3 Module Atlas Layout

All motif family modules share a single 4096 x 4096 texture atlas organized as follows:

```
+---------------------------+
|  Family A   |  Family B   |  (upper half: 2048 x 4096)
|  12 modules |  10 modules |
|             |             |
+-------------+-------------+
|  Family C   |  Reserved   |  (lower half: 2048 x 4096)
|  8 modules  |  (future)   |
|             |             |
+---------------------------+
```

Each module occupies a 512 x 512 or 512 x 1024 region depending on aspect ratio. The atlas supports albedo, normal, and emissive channels packed into a single RGBA + secondary normal texture.

---

## 4. Pop-In Disguise Rules

LOD transitions are one of the most immersion-breaking artifacts in open-world games. The following five rules define how the Show Director and rendering pipeline must handle transitions to minimize perceptible pop-in.

### Rule 1: Cross-Fade

**All LOD transitions use a 0.5-second alpha blend.** During the blend, both the outgoing and incoming LOD meshes are rendered simultaneously with complementary alpha values. This is the baseline disguise and applies to every transition.

```
t = transition_progress  // 0.0 to 1.0 over 0.5 seconds
outgoing.alpha = 1.0 - t
incoming.alpha = t
```

- **Exception:** Culled-to-any transitions do not cross-fade (entity appears from nothing). Instead, these use Rule 2 or Rule 4.
- **Cost:** Doubles triangle count for the affected entity during the 0.5 s window. Budgeted as part of the Show Director's swap-per-frame cap.

### Rule 2: Haze Masking

**Atmospheric haze density increases locally during LOD swaps for objects beyond 80 m.** A localized fog volume is placed around the swapping entity, intensified over 0.3 s, held for 0.2 s during the swap, then faded over 0.3 s.

- **Parameters:** Haze color matches current atmosphere. Opacity: 40% at peak. Radius: entity bounding sphere x 1.5.
- **Applicability:** Far-band transitions only. Not used in near or mid bands (too obvious at close range).

### Rule 3: Glare Masking

**Billboard bloom/glare can mask nearby facade transitions.** When a billboard in the near band is producing significant bloom (brightness > 0.8 in emissive channel), adjacent building LOD transitions within a 15 m radius can be timed to coincide with bloom peaks.

- **Implementation:** The Show Director tracks billboard brightness per frame. When a swap is queued for a building near a bright billboard, the swap is delayed up to 0.5 s to align with the next bloom peak.
- **Applicability:** Times Square specific -- most useful along Broadway billboard row.

### Rule 4: Motion Occlusion (Saccade Suppression)

**LOD swaps are preferentially timed to occur when the player is in motion.** During translational or rotational movement (velocity > 0.5 m/s or angular velocity > 15 deg/s), the human visual system suppresses peripheral detail processing. The Director exploits this by queuing non-urgent swaps and executing them during motion frames.

- **Queue depth:** Up to 8 deferred swaps.
- **Timeout:** If a swap has been deferred for > 2.0 s, execute it regardless of motion state (prevents stale LODs).
- **Priority:** Swaps in the player's direct forward cone (30 deg half-angle) are never deferred -- they execute immediately with cross-fade.

### Rule 5: Crowd Screen

**Dense crowd geometry between the player and a swapping entity hides the transition.** If the Show Director detects that the line of sight to a swapping entity passes through a region with crowd density > 4 NPCs per 10 m^2, the swap is considered naturally occluded and can be executed without cross-fade (instant swap behind the crowd).

- **Detection:** Ray from player eye to entity center, count intersected NPC bounding boxes.
- **Threshold:** 3 or more NPC bounds intersected = occluded.

---

## 5. LOD Identity Contract

> **"Macro identity (silhouette, color palette, signage zone, floor count) persists across all LOD levels. Micro detail (individual windows, brick patterns, door handles) may vary."**

This contract means:

| Property | L0 | L1 | L2 | Required to Match? |
|----------|----|----|----|--------------------|
| Building silhouette (outline) | Exact | Exact | Simplified but recognizable | **Yes** -- within 3% scale, 2 deg rotation |
| Floor count | Exact | Exact | Approximate (floor lines may merge) | **Yes** -- must read as same height |
| Dominant color | Exact | Family-tinted (within palette) | Flat average | **Yes** -- hue within 15 deg |
| Signage zones (billboard areas) | Exact placement | Correct zone, simplified content | Emissive rectangle in correct position | **Yes** -- placement within 1 m |
| Window pattern | Unique per building | Family-instanced pattern | Not visible | **No** -- allowed to vary |
| Door hardware | Unique modeled | Texture-only | Not visible | **No** -- allowed to vary |
| Brick/material micro-detail | Full PBR | Atlas sample | Not visible | **No** -- allowed to vary |
| Interior visibility | Parallax cubemap | Static parallax | None | **No** -- allowed to vary |

---

## 6. LOD Transition Distance Matrix

Summary of the distance thresholds at which each asset class transitions between LOD tiers.

| Asset Class | L0 -> L1 | L1 -> L2 | L2 -> Culled | Hysteresis |
|-------------|----------|----------|--------------|------------|
| Buildings | 30 m | 150 m | 400 m (or out of frustum) | +/- 5 m |
| Billboards | 30 m | 80 m | 200 m (or out of frustum) | +/- 3 m |
| Street Props | 20 m | 60 m | 120 m (or out of frustum) | +/- 3 m |
| Crowds | 30 m | 80 m | 200 m (or out of frustum) | +/- 5 m |
| Vehicles | 30 m | 100 m | 250 m (or out of frustum) | +/- 5 m |

**Hysteresis** prevents oscillation at boundaries: an entity that transitioned from L0 to L1 at 30 m will not transition back to L0 until the player is within 25 m (30 m - 5 m hysteresis band).

---

## 7. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1.0 | 2026-01-27 | Design Team | Initial draft -- all asset-class LOD tables, motif families, pop-in rules, identity contract |

---

*End of LOD + Motif Library v0*
