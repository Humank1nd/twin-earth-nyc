# Show Director + Billboard Tier Config v0

**Document:** Twin Earth NYC — Part 12, File 2 of 6
**Status:** v0 Draft
**Scope:** Distance bands, billboard tier configuration, seam locations, performance caps

---

## 1. Overview

The Show Director manages the visual fidelity of the Times Square slice by dynamically allocating rendering resources based on the player's position. Times Square is the most billboard-dense environment in the game, making it the stress test for the Show Director's LOD system, billboard management, and seam concealment.

This document configures the Show Director specifically for the Times Square slice. All values are tuned for this environment's unique density and visual requirements.

---

## 2. Distance Bands

The Show Director partitions the world into three concentric bands around the player camera. Each band has distinct budgets for geometry, materials, physics, and AI.

### 2.1 Band Definitions

| Band | Range (from camera) | Description |
|------|---------------------|-------------|
| **Near** | 0 - 30m | Full fidelity. Everything the player can closely inspect. |
| **Mid** | 30 - 150m | Reduced fidelity. Recognizable but not inspectable. |
| **Far** | 150m+ | Minimal fidelity. Silhouettes, atmosphere, distant glow. |

### 2.2 Budget Allocation Per Band

| Resource | Near (0-30m) | Mid (30-150m) | Far (150m+) |
|----------|-------------|---------------|-------------|
| **Triangle Budget** | 2.65M triangles | 1.33M triangles | 310K triangles |
| **Material Budget** | 512 unique materials | 256 materials (instanced) | 64 materials (atlas) |
| **Texture Resolution** | Full (up to 4K) | Half (up to 2K) | Quarter (up to 512) |
| **Active Physics** | Full PhysX at 60Hz | None (visual only) | None |
| **AI Budget — Hero NPCs** | Full behavior tree | Simplified decision tree | N/A (despawned or frozen) |
| **AI Budget — Background NPCs** | Heuristic navigation | Flow-follow only | None (particle crowds) |
| **Shadow Quality** | Full cascaded shadows | Simplified shadow maps | No individual shadows |
| **Reflection Quality** | SSR + planar probes | SSR only | None (baked) |

### 2.3 Band Transition Rules

```
TRANSITION RULES:
  Near -> Mid:
    - Trigger: object center crosses 30m from camera
    - Transition time: 0.5s fade (geometry swap masked by distance)
    - Material swap: immediate (pre-cached at 25m)
    - Physics: disable at 30m boundary (no fade)
    - AI: downgrade at 30m (hero NPCs keep decision tree, BG NPCs drop to flow)

  Mid -> Far:
    - Trigger: object center crosses 150m from camera
    - Transition time: 1.0s fade (distance makes swap invisible)
    - Material swap: atlas lookup (pre-cached at 140m)
    - AI: BG NPCs become particle representations
    - Hero NPCs: frozen at last known position (not visible at this range)

  Reverse transitions (Far->Mid, Mid->Near):
    - Pre-load at 10m inside boundary (load at 140m for Far->Mid, 25m for Mid->Near)
    - Geometry and material swap occurs at boundary crossing
    - Physics re-enabled at Near boundary with 2-frame settle
    - AI upgrades immediately on crossing
```

### 2.4 Times Square Special Considerations

Times Square's density means the Near band is unusually packed:

| Concern | Mitigation |
|---------|------------|
| Billboard density in Near band | Max 4 full-video simultaneously; others auto-demote to 5fps |
| NPC density in Near band at peak | Aggressive LOD on NPC meshes beyond 15m even within Near |
| Light source count (billboard spill) | Max 8 dynamic lights from billboards; others baked |
| Reflection complexity (wet streets) | SSR only; no real-time cubemaps in Times Square |

---

## 3. Billboard Tier Configuration

### 3.1 Hero Billboards

Eight hero billboards define the Times Square visual identity. Each has three content tiers that activate based on the player's distance.

| ID | Name | Size Class | Location | Facing |
|----|------|-----------|----------|--------|
| BB_H01 | One Times Square South | XL (15m x 20m) | 43rd/Broadway, south face | South + East |
| BB_H02 | One Times Square North | XL (15m x 20m) | 43rd/Broadway, north face | North + West |
| BB_H03 | Reuters (3 Times Square) | L (12m x 15m) | 43rd/7th Ave, NE corner | West + South |
| BB_H04 | ABC SuperSign (1515 Broadway) | L (12m x 18m) | 44th/Broadway, east face | East |
| BB_H05 | Marriott Marquis Marquee | L (10m x 12m) | 45th/Broadway, east face | East + South |
| BB_H06 | TKTS Screen | M (6m x 4m) | Father Duffy Square, steps | South |
| BB_H07 | 44th/Broadway Corner | M (8m x 6m) | 44th/Broadway, corner wrap | South + East |
| BB_H08 | 46th/7th Corner | M (8m x 6m) | 46th/7th Ave, corner wrap | West + South |

### 3.2 Content Tiers Per Billboard

| ID | Near Content (0-30m) | Mid Content (30-150m) | Far Content (150m+) |
|----|---------------------|----------------------|---------------------|
| BB_H01 | Full video, 30fps, 1920x1080 | 5fps loop, 960x540 | Static emissive, 256x256 |
| BB_H02 | Full video, 30fps, 1920x1080 | 5fps loop, 960x540 | Static emissive, 256x256 |
| BB_H03 | Full video, 30fps, 1920x1080 | 5fps loop, 960x540 | Static emissive, 256x256 |
| BB_H04 | Full video, 30fps, 1920x1080 | 5fps loop, 960x540 | Static emissive, 256x256 |
| BB_H05 | Full video, 30fps, 1920x1080 | 5fps loop, 960x540 | Static emissive, 256x256 |
| BB_H06 | Full video, 30fps, 1280x720 | 5fps loop, 640x360 | Static emissive, 128x128 |
| BB_H07 | 5fps loop, 960x540 (not always hero) | Static emissive, 256x256 | Off |
| BB_H08 | 5fps loop, 960x540 (not always hero) | Static emissive, 256x256 | Off |

**Note on BB_H07 and BB_H08:** These are conditional hero billboards. They display 5fps loops at Near range but do not play full video. They are promoted to hero status for specific narrative events (e.g., emergency broadcast during anomaly). At Mid and Far, they are static or off.

### 3.3 Light Spill Configuration

Each hero billboard emits colored light that illuminates nearby geometry, NPCs, and street surfaces. This is critical for the Times Square "glow canyon" effect, especially at night.

| ID | Light Spill Radius | Color Temperature | Intensity (Night) | Intensity (Day) | Flicker |
|----|-------------------|-------------------|-------------------|-----------------|---------|
| BB_H01 | 20m | Warm white (4000K) | 1.0 | 0.3 | Subtle (content-driven) |
| BB_H02 | 20m | Cool blue (7500K) | 1.0 | 0.3 | Subtle (content-driven) |
| BB_H03 | 15m | Neutral white (5500K) | 0.8 | 0.2 | Moderate (news ticker) |
| BB_H04 | 15m | Multicolor (animated) | 0.9 | 0.25 | Active (show promo) |
| BB_H05 | 15m | Gold (3000K) | 0.8 | 0.2 | Gentle pulse |
| BB_H06 | 10m | Neutral white (5500K) | 0.6 | 0.15 | Minimal |
| BB_H07 | 10m | Varies by content | 0.5 | 0.1 | Content-driven |
| BB_H08 | 10m | Varies by content | 0.5 | 0.1 | Content-driven |

**Light Spill Implementation:**
```
PSEUDOCODE — Billboard Light Spill Update (per frame):

for each hero_billboard in active_billboards:
    if player_distance(hero_billboard) > hero_billboard.spill_radius * 2:
        continue  // Too far, skip light update

    // Sample dominant color from billboard content
    dominant_color = sample_billboard_dominant_color(hero_billboard)

    // Modulate by time of day
    time_factor = lerp(hero_billboard.intensity_day,
                       hero_billboard.intensity_night,
                       night_factor())  // 0.0 = noon, 1.0 = midnight

    // Apply to point light
    hero_billboard.spill_light.color = dominant_color
    hero_billboard.spill_light.intensity = time_factor
    hero_billboard.spill_light.radius = hero_billboard.spill_radius

    // Flicker (optional, per billboard config)
    if hero_billboard.flicker != NONE:
        hero_billboard.spill_light.intensity *= flicker_value(
            hero_billboard.flicker_type, game_time)
```

### 3.4 Background Billboards

| ID Range | Count | Size Range | Location | Near Content | Mid Content | Far Content | Light Spill |
|----------|-------|-----------|----------|-------------|-------------|-------------|-------------|
| BB_B01 - BB_B10 | 10 | M (6-8m) | Building facades, various | Static emissive, 512x512 | Simplified emissive, 256x256 | Off | 5m each, white |
| BB_B11 - BB_B20 | 10 | S (2-4m) | Awnings, storefronts, poles | Static emissive, 256x256 | Off | Off | 3m each, warm |

**Total billboard count:** 8 hero + 20 background = 28 billboards in slice.

### 3.5 Billboard Content Pipeline

```
CONTENT SOURCES:
  - Hero XL/L billboards: Pre-rendered video loops (30s each), baked from
    fictional ad content (Twin Earth branding, in-universe corporations)
  - Hero M billboards: Pre-rendered 5fps loops or static images
  - Background M/S billboards: Static textures from asset library
  - Emergency override: all hero billboards can display emergency content
    (news alert, evacuation notice) triggered by narrative events

CONTENT LOADING:
  - Near tier videos: streamed from disk, 2-frame decode buffer
  - Mid tier loops: pre-loaded in memory (small file size at 5fps)
  - Far tier statics: loaded with scene, always resident
  - Pre-warm: when player approaches billboard (distance < spill_radius * 3),
    begin loading Near tier content into decode buffer
```

---

## 4. Seam Locations and Masks

The slice has hard boundaries where the game world ends. Seams must be visually concealed so the player never sees a raw edge, void, or LOD cliff. Ten seam locations are defined.

### 4.1 Seam Inventory

| Seam ID | Location | Type | Description |
|---------|----------|------|-------------|
| S01 | West of 7th Avenue (east edge of slice) | World edge | Eastern boundary where buildings and sidewalk end |
| S02 | East of Broadway (west edge of slice) | World edge | Western boundary where buildings and sidewalk end |
| S03 | South of 42nd Street | World edge | Southern boundary, road and sidewalk terminate |
| S04 | North of 47th Street | World edge | Northern boundary, road and sidewalk terminate |
| S05 | 43rd Street alley (between buildings) | Backstage | Narrow alley leading to unmodeled interior block |
| S06 | 42nd Street subway entrance | Zone transition | Stairs descending to underground (future zone) |
| S07 | Marriott Marquis lobby entrance | Interior transition | Glass doors to unmodeled hotel interior |
| S08 | 44th Street service entrance | Backstage | Service door on building side |
| S09 | AMC Empire 25 upper levels | Vertical seam | Elevator shaft to unmodeled upper floors |
| S10 | 44th Street portal zone | Portal transition | Special seam that becomes portal entrance during anomaly |

### 4.2 Mask Configuration

Each seam has a primary mask (visually interesting, diegetic) and a fallback mask (simpler, guaranteed to block sightlines).

| Seam ID | Primary Mask | Mask Assets | Fallback Mask | Fallback Assets |
|---------|-------------|-------------|---------------|-----------------|
| S01 | Construction scaffolding | Scaffold mesh + tarp + safety netting + caution signs | Jersey barriers | Barrier mesh (instanced x12) |
| S02 | Delivery trucks + scaffolding | Box truck (static) + scaffold section + loading zone signs | Police barriers | Metal barrier mesh (instanced x8) |
| S03 | Road work + barriers | Orange barrels + plates + "ROAD WORK AHEAD" sign + cone line | Cone line | Traffic cone mesh (instanced x20) |
| S04 | Construction crane | Crane base mesh + fencing + "HARD HAT AREA" signage | Chain-link fencing | Fence panels (instanced x6) |
| S05 | Dumpsters + metal gate | 2x dumpster mesh + rolling gate (closed) + trash bags | "No Access" door | Steel door mesh + padlock |
| S06 | Subway stairs into darkness | Stair geometry descending + darkness fog + subway signage | Turnstile barrier | Turnstile mesh + "CLOSED" sign |
| S07 | Glass doors + reflection | Glass door mesh + interior reflection cubemap + doorman NPC | "Closed" sign | Sign mesh + opaque door |
| S08 | Steel door (locked) | Steel door mesh + card reader + "STAFF ONLY" sign | Padlock | Same door + padlock overlay |
| S09 | Elevator (non-functional) | Elevator doors (closed) + floor indicator (stuck) + "OUT OF ORDER" sign | "Out of Order" sign | Sign on wall |
| S10 | Anomaly distortion VFX | Shimmer shader + particle effects + faint glow | Construction barrier | Orange barrier + cone |

### 4.3 Seam Behavior Rules

```
SEAM BEHAVIOR:

World Edge Seams (S01-S04):
  - Always active (masks never removed)
  - Player collision: invisible wall at mask location
  - NPC behavior: NPCs approaching seam despawn 3m before mask
    (walk behind truck, turn corner, enter scaffold gap)
  - Vehicle behavior: vehicles approaching seam despawn at mask
    (turn off-screen or stop at barrier)
  - Audio: construction ambience from S01, S02, S04; traffic from S03

Backstage Seams (S05, S08):
  - Always active
  - Player interaction: examine door/gate -> "Locked" / "No access"
  - NPC behavior: worker NPCs may patrol near these (vendor/worker preset)
  - No despawn near these (they are dead-ends)

Zone Transition Seams (S06, S07):
  - Active until zone is built
  - S06 (subway): future zone transition point. Currently stairs descend
    into darkness with a turnstile barrier and "STATION CLOSED" sign
  - S07 (Marriott): future interior zone. Currently glass doors show
    reflection. Doorman NPC says "Sorry, private event tonight."
  - These seams will be upgraded to functional transitions in future slices

Vertical Seam (S09):
  - Elevator doors always closed
  - Player interaction: press button -> nothing happens, "Out of Order" sign
  - Future: elevator becomes functional for vertical slice expansion

Portal Seam (S10):
  - Default state: construction barrier (normal appearance)
  - Pre-anomaly: barrier present, area looks like normal alley
  - During anomaly: barrier dissolves into anomaly VFX (shimmer replaces
    physical mask)
  - Portal active: seam becomes portal entrance (fully traversable)
  - Post-portal: residue shimmer + police tape replaces original barrier
  - Reset: after 48h sim-time, barrier returns (city "repaired" it)
```

### 4.4 Seam Map

```
                47th Street
    =====[S04: Crane + Fencing]=====
   |                                |
  [S02]                          [S01]
  Trucks                        Scaffold
   |                                |
   |    46th St                     |
   |    BB_H08                      |
   |                                |
   |    45th St                     |
   |    BB_H05 (Marriott)          |
   |          [S07: Glass Doors]    |
   |                                |
   |    Father Duffy / TKTS         |
   |    BB_H06                      |
   |                                |
   |    44th St                     |
   |    BB_H04, BB_H07              |
   |    [S08: Steel Door]           |
   |    [S10: Portal Zone]          |
   |                                |
   |    [S05: Dumpsters]            |
   |    43rd St                     |
   |    BB_H01, BB_H02, BB_H03     |
   |                                |
   |    One Times Square            |
   |    [S09: Elevator]             |
   |                                |
   |    [S06: Subway Entrance]      |
   |                                |
    =====[S03: Road Work]==========
                42nd Street

  WEST (Broadway)          EAST (7th Ave)
```

---

## 5. Performance Caps

### 5.1 Billboard Performance Budget

| Metric | Budget | Measurement |
|--------|--------|-------------|
| Max concurrent full-video billboards | 4 (of 8 hero) | Count of billboards in Near tier playing 30fps video |
| Max concurrent low-FPS billboards | 8 (all hero at 5fps) | Count of billboards playing any animated content |
| Total billboard GPU time | < 2.0ms per frame | GPU profiler, billboard render pass |
| Billboard video memory | < 256 MB total | Sum of all decoded billboard textures in flight |
| Billboard CPU decode time | < 0.5ms per frame | CPU profiler, video decode thread |

### 5.2 Billboard Priority System

When the player is positioned such that more than 4 hero billboards are within Near range (0-30m), the Show Director must prioritize:

```
PRIORITY ALGORITHM:

billboard_priority(bb) =
    base_priority(bb.size_class)     // XL=100, L=75, M=50
    + facing_bonus(bb, camera)        // +20 if facing camera, 0 if perpendicular
    + screen_area(bb, camera)         // 0-30 based on projected screen area
    + narrative_bonus(bb)             // +50 if currently narrative-relevant

Sort all Near-range hero billboards by priority descending.
Top 4 get full video (30fps).
Remaining Near-range hero billboards get 5fps loop.
All Mid-range get 5fps loop.
All Far-range get static.

EXCEPTION: During narrative events (emergency broadcast, anomaly alert),
one billboard can be force-promoted to full video regardless of position.
```

### 5.3 Emergency Performance Mode

```
EMERGENCY MODE:

Trigger: instantaneous FPS < 35 for 3 consecutive frames
         OR average FPS < 40 over 1 second

Actions (applied in order, each frame re-evaluates):
  Level 1 (FPS < 40 avg):
    - All hero billboards demote to 5fps loop (no full video)
    - Background billboards switch to simplified emissive
    - Billboard light spill reduced to 2 lights (nearest only)

  Level 2 (FPS < 35 for 3 frames):
    - All billboards demote to static emissive
    - All billboard light spill disabled
    - NPC LOD distance reduced by 30% (more aggressive culling)

  Level 3 (FPS < 30 for 5 frames):
    - Background NPC count reduced by 50% (despawn furthest first)
    - Shadow quality reduced one tier globally
    - Reflection probes disabled
    - Billboard render pass skipped entirely (static fallback baked into
      building textures)

Recovery:
  - FPS > 45 for 60 consecutive frames: step up one level
  - Hysteresis: 5-second cooldown between level changes to prevent thrashing
```

### 5.4 Overall Frame Budget (Times Square Slice)

| System | Budget (ms) | Notes |
|--------|-------------|-------|
| Geometry rendering | 8.0ms | Buildings, streets, props |
| Billboard rendering | 2.0ms | All billboard content + light spill |
| NPC rendering | 3.0ms | All NPCs (hero + background) |
| NPC AI/pathing | 2.0ms | Behavior trees + navigation |
| Physics | 1.5ms | PhysX for Near band |
| VFX (particles, anomaly) | 1.5ms | Anomaly shimmer, portal, weather |
| IoT/Event bus | 0.5ms | Event processing, ledger writes |
| Audio | 1.0ms | Spatial audio, mixing |
| Post-processing | 2.0ms | Bloom, color grading, TAA |
| UI/HUD | 0.5ms | Inventory, Heat display |
| System overhead | 1.5ms | Engine, scene management, Show Director |
| **Total** | **24.0ms** | **Target: 60fps (16.67ms ideal, 24ms = 42fps minimum)** |
| **Headroom** | **9.33ms** | **Available for spikes, debug, future features** |

**Note:** The 24ms total leaves headroom for worst-case scenarios. Steady-state target is 16.67ms (60fps). The system must never exceed 33.33ms (30fps).

---

## 6. Show Director State Machine

### 6.1 Director Modes

The Show Director operates in one of four modes depending on game state:

| Mode | Trigger | Billboard Behavior | NPC Behavior | Performance Target |
|------|---------|-------------------|--------------|-------------------|
| **Normal** | Default state | Standard tier system | Standard population | 60fps |
| **Event** | Anomaly active or Heat > 0.4 | One billboard may show alert | NPCs react to event | 60fps (relaxed to 45fps) |
| **Portal** | Portal open | Nearest billboard flickers/distorts | NPCs displaced | 45fps (VFX budget increased) |
| **Emergency** | FPS < 35 | All demoted (see 5.3) | Reduced count | 30fps minimum |

### 6.2 Mode Transitions

```
STATE MACHINE:

  Normal --(anomaly.zone.spike OR heat > 0.4)--> Event
  Normal --(FPS < 35 for 3 frames)--> Emergency

  Event --(portal.state == STABLE)--> Portal
  Event --(heat < 0.2 AND no anomaly)--> Normal
  Event --(FPS < 35 for 3 frames)--> Emergency

  Portal --(portal.state == SEALED)--> Event  // aftermath
  Portal --(FPS < 35 for 3 frames)--> Emergency

  Emergency --(FPS > 45 for 60 frames)--> [previous mode]

Note: Emergency mode remembers the previous mode and returns to it
when performance recovers. The director does not skip modes on recovery.
```

---

## 7. Configuration File Format

All Show Director values are data-driven. The configuration for the Times Square slice is stored as structured data that can be hot-reloaded during development.

```json
{
  "slice_id": "TSQ_001",
  "slice_name": "Times Square",
  "version": "0.1.0",

  "distance_bands": {
    "near": {
      "range_min": 0,
      "range_max": 30,
      "triangle_budget": 2650000,
      "material_budget": 512,
      "physics_enabled": true,
      "physics_rate_hz": 60,
      "ai_hero": "full_behavior_tree",
      "ai_background": "heuristic_navigation"
    },
    "mid": {
      "range_min": 30,
      "range_max": 150,
      "triangle_budget": 1330000,
      "material_budget": 256,
      "physics_enabled": false,
      "ai_hero": "simplified_decision_tree",
      "ai_background": "flow_follow"
    },
    "far": {
      "range_min": 150,
      "range_max": 99999,
      "triangle_budget": 310000,
      "material_budget": 64,
      "physics_enabled": false,
      "ai_hero": "none",
      "ai_background": "particle_crowd"
    }
  },

  "billboard_performance": {
    "max_concurrent_full_video": 4,
    "max_concurrent_low_fps": 8,
    "gpu_time_budget_ms": 2.0,
    "video_memory_budget_mb": 256,
    "cpu_decode_budget_ms": 0.5
  },

  "emergency_thresholds": {
    "level_1_fps": 40,
    "level_1_window_seconds": 1.0,
    "level_2_fps": 35,
    "level_2_consecutive_frames": 3,
    "level_3_fps": 30,
    "level_3_consecutive_frames": 5,
    "recovery_fps": 45,
    "recovery_frames": 60,
    "hysteresis_seconds": 5.0
  }
}
```

---

*End of document. Next: NPC Tier Config v0.*
