# Show Director Spec v0

**Twin Earth NYC -- Part 9: Forced Perspective**
**Document:** Show Director Specification
**Version:** 0.1.0
**Status:** Draft
**Last Updated:** 2026-01-27

---

## 1. Purpose

The Show Director is the runtime system responsible for maintaining the perceptual illusion of a fully realized Times Square while operating within strict performance budgets. It arbitrates between the **truth layer** (metric reality used by gameplay, physics, and AI) and the **illusion layer** (visual representation optimized for the current viewpoint). Every frame, the Show Director evaluates what the player can see, reach, and verify, then allocates rendering resources accordingly.

This document defines the doctrine governing that arbitration, the invariants that must never be violated, the allowed variances that grant creative and performance freedom, and the per-frame budget contracts the Director enforces.

---

## 2. Forced Perspective Doctrine

### 2.1 Truth Layer Rules -- "Truth Never Lies"

These three rules are **inviolable**. No optimization, artistic choice, or performance pressure may override them. They form the foundation of player trust.

| # | Rule | Rationale |
|---|------|-----------|
| **T1** | **Scale anchors remain metrically accurate at all distances.** Door height = 2.1 m. Standing human = 1.75 m. Yellow taxi = 4.8 m. These proportions hold regardless of LOD level, distance band, or proxy state. | Scale anchors are the subconscious reference points the human visual system uses to gauge depth and distance. If a door shrinks at range, the entire scene reads as miniature. |
| **T2** | **Collision and navigation surfaces match truth geometry.** What the player walks on, bumps into, and stands behind is defined by the truth-layer collision mesh. The visual mesh may simplify, but the walkable surface and physics boundaries never deviate from surveyed geometry. | Gameplay depends on spatial consistency. A player who ducks behind a wall for cover must be occluded by the same geometry the AI uses for line-of-sight checks. |
| **T3** | **Sensor occlusion is physically correct.** Line-of-sight, audio occlusion, and detection cones are computed against truth-layer collision geometry. A wall blocks vision even if the illusion layer has simplified that wall to a flat plane. You cannot see through a wall even if the wall's render mesh has been culled. | AI fairness and player trust require that hiding behind geometry actually hides you, regardless of how the renderer has optimized that geometry. |

### 2.2 Illusion Layer Rules -- "Illusion May Cheat"

These three rules define the **degrees of freedom** the illusion layer has to reduce rendering cost and increase visual richness without violating truth.

| # | Rule | Scope |
|---|------|-------|
| **I1** | **Render-only geometry may deviate from truth beyond verification range (>30 m).** Facades beyond 30 m may use simplified meshes, merged geometry, or proxy representations, provided their silhouette, color palette, and scale anchors are preserved. | Geometry simplification |
| **I2** | **Proxy skylines may replace real geometry when silhouette is preserved.** Entire building clusters beyond the mid-band may be replaced by billboard proxies, impostor meshes, or baked panoramic cards, as long as the skyline edge-profile matches the truth geometry within tolerance. | Large-scale substitution |
| **I3** | **Window interiors, micro-clutter, and distant signage text may be implied or procedurally varied.** Interior parallax effects behind windows do not need to represent real rooms. Street-level litter, puddle positions, and background shop names may be randomized or instanced without matching any ground truth. | Detail fabrication |

---

## 3. Invariants List -- Times Square Slice

These measurements define what **must** be metrically correct in every build. Each invariant has a type, tolerance, and automated or semi-automated verification method.

| # | Invariant | Type | Tolerance | Verification Method |
|---|-----------|------|-----------|---------------------|
| INV-01 | Street widths (Broadway, 7th Ave) | Geometry | +/- 0.5 m | Overhead orthographic measure against survey data |
| INV-02 | Door / window scale cues (height ratios) | Proportion | +/- 5% | Screenshot comparison with annotated reference |
| INV-03 | One Times Square silhouette | Silhouette | 2 deg rotation, 3% scale | Edge detection overlay vs. reference photograph |
| INV-04 | TKTS Red Steps position and scale | Geometry | +/- 0.25 m | Anchor coordinate check against survey |
| INV-05 | Marriott Marquee sign zone | Placement | +/- 1.0 m | Reference photo overlay alignment |
| INV-06 | Traffic signal positions | Placement | +/- 0.5 m | Anchor coordinate check against survey |
| INV-07 | Sidewalk-road boundary lines | Geometry | +/- 0.3 m | Collision mesh overlay vs. visual mesh |
| INV-08 | Broadway / 7th Ave intersection angles | Geometry | +/- 1 deg | Overhead orthographic comparison |
| INV-09 | Key sightline silhouettes (5 defined) | Visual | Qualitative pass | Human review panel (3 reviewers, majority vote) |
| INV-10 | Billboard placement zones | Placement | +/- 1.0 m | Reference photo overlay alignment |

**Sightline Definitions (INV-09):**

| Sightline ID | From | Toward | Key Features in Profile |
|--------------|------|--------|------------------------|
| SL-01 | 42nd / Broadway NW corner | North up Broadway | One Times Square tower, TKTS steps, converging facades |
| SL-02 | TKTS Red Steps top | South toward 42nd | Street canyon, billboard wall, taxi flow |
| SL-03 | 44th / 7th Ave | East toward bowtie | Cross-street compression, building stagger |
| SL-04 | 46th / Broadway | South down Broadway | Full slice depth, LOD gradient visible |
| SL-05 | Center of bowtie | 360 deg panoramic | Surround skyline, billboard ring |

---

## 4. Allowed Variance List

The following elements are explicitly permitted to vary between builds, LOD states, or frames without triggering a regression failure.

| Variance | Condition | Notes |
|----------|-----------|-------|
| Far facade window detail | Distance > 50 m | May use repeating texture tiles instead of unique windows |
| Window interior hints | Any distance | Parallax shader with generic interior cubemap; not real rooms |
| Micro-clutter placement | Any distance | Trash, leaves, puddle positions are non-deterministic |
| Distant crowd individuality | Distance > 30 m | Instanced archetypes (20 variants) replace unique meshes |
| Background shop signage text | Distance > 30 m | Procedurally varied; not required to match real-world signage |
| Far building material detail | Distance > 80 m | Simplified PBR (merged roughness/metallic, reduced texture res) |
| Ambient prop variety | Distance > 30 m | Bench style, trash can model, newspaper box variant may repeat |

---

## 5. Attention Inputs (v0)

The Show Director consumes five input signals each frame to determine where the player's attention is focused and what level of detail is required in each region.

### 5.1 Input Definitions

| Input | Source | Description | Update Rate |
|-------|--------|-------------|-------------|
| **Camera Frustum** (primary) | Render camera | Standard view-frustum pyramid. Everything inside is potentially visible and must be budgeted. | Every frame |
| **Distance Bands** | Player position | Three concentric zones around the player: Near (0--30 m), Mid (30--150 m), Far (150 m+). | Every frame |
| **Player Velocity** | Character controller | Current movement speed in m/s. High velocity compresses the mid-band threshold because the player has less time to scrutinize detail. Mid-band outer edge = `150 - (velocity * 8)` meters (clamped to [80, 150]). | Every frame |
| **Gaze Proxy** | Screen-center raycast | A ray from screen center into the scene. The first hit point receives a +20% detail budget bonus (effectively extends near-band treatment to a cone around the gaze target). Cone half-angle: 5 deg. | Every frame |
| **Verification Zones** | Navigation query | Any area the player can physically reach within 5 seconds (based on current velocity or default walk speed of 1.4 m/s). These zones receive near-band treatment even if they are currently in the mid-band by distance alone. This prevents the player from sprinting into under-detailed areas. | Every 0.25 s (amortized) |

### 5.2 Velocity-Adjusted Mid-Band

```
adjusted_mid_max = clamp(150.0 - (player_speed * 8.0), 80.0, 150.0)
```

At walking speed (1.4 m/s), mid-band extends to ~139 m. At sprint speed (7 m/s), mid-band compresses to ~94 m. This ensures that fast-moving players see higher fidelity in their direction of travel.

---

## 6. Director Outputs

Each frame, the Show Director produces the following output commands that downstream systems consume.

| Output | Target System | Effect |
|--------|---------------|--------|
| **LOD Tier Selection** | Per managed asset | Sets which LOD mesh, material set, and animation tier is active for the entity |
| **Proxy Swap Requests** | Per building / building cluster | Commands the streaming system to swap between unique geometry and instanced proxy (or vice versa) |
| **Inflation Requests** | Per occluded region / backstage zone | Triggers detail spawning inside hidden areas that the player is approaching |
| **Lens / Atmosphere Params** | Global post-processing | Adjusts atmospheric haze density, bloom intensity, and depth-of-field based on time-of-day, weather, and current LOD distribution |
| **Crowd Density Budget** | Per zone (near / mid / far) | Allocates the frame's NPC count budget across zones, ensuring near zones have enough unique individuals |

---

## 7. Director Tick Pseudocode

```python
# Show Director -- Main Tick (executes every frame)

NEAR_THRESHOLD   = 30.0    # meters
WALK_SPEED       = 1.4     # meters/second (fallback if player is stationary)
REACHABLE_WINDOW = 5.0     # seconds
GAZE_CONE_ANGLE  = 5.0     # degrees half-angle

TRIANGLE_BUDGET  = 5_000_000
VIDEO_BUDGET     = 4        # max concurrent full-video billboard surfaces
MATERIAL_BUDGET  = 512      # max unique textures in view

def director_tick():
    # --- Gather Inputs ---
    frustum      = get_camera_frustum()
    player_pos   = get_player_position()
    player_vel   = get_player_velocity()
    player_speed = length(player_vel)
    gaze_target  = raycast(screen_center)

    # Velocity-adjusted mid-band
    mid_threshold = clamp(150.0 - (player_speed * 8.0), 80.0, 150.0)

    # --- Per-Entity Evaluation ---
    for entity in managed_entities:
        dist          = distance(player_pos, entity.position)
        in_frustum    = frustum.contains(entity.bounds)
        travel_speed  = max(player_speed, WALK_SPEED)
        reachable_soon = (dist / travel_speed) < REACHABLE_WINDOW
        at_gaze       = angle_to(gaze_target, entity.position) < GAZE_CONE_ANGLE

        # Determine LOD tier
        if dist < NEAR_THRESHOLD or reachable_soon:
            entity.set_lod(NEAR)
        elif dist < mid_threshold:
            if at_gaze:
                entity.set_lod(NEAR)   # gaze bonus: promote to near
            else:
                entity.set_lod(MID)
        else:
            entity.set_lod(FAR)

        # Frustum culling (but not if reachable soon -- pre-stream)
        if not in_frustum and not reachable_soon:
            entity.set_lod(CULLED)

    # --- Budget Enforcement ---
    budget_check()

def budget_check():
    # Triangle budget
    if total_triangles_in_view() > TRIANGLE_BUDGET:
        demote_farthest_mid_to_far()
        # Repeat until under budget or no more mid-tier entities
        if total_triangles_in_view() > TRIANGLE_BUDGET:
            demote_farthest_near_to_mid()

    # Video surface budget
    if count_active_video_surfaces() > VIDEO_BUDGET:
        pause_farthest_video()

    # Material budget
    if count_unique_materials_in_view() > MATERIAL_BUDGET:
        merge_farthest_to_atlas()

    # Emergency framerate protection
    if current_fps() < 35:
        demote_all_billboards_to_static()
        reduce_crowd_density(factor=0.5)
```

---

## 8. Distance Bands -- Times Square Configuration

| Band | Range | Visual Guarantees | Interaction | Budget Fraction |
|------|-------|-------------------|-------------|-----------------|
| **Near** | 0 -- 30 m | Unique assets at full resolution. Full skeletal animation with blend trees. All interactive elements active. Physics-active props. Full PBR materials (4K). Real-time video on billboards. | Doors openable, props pickable, NPCs conversable, billboards hackable | 60% of triangle budget |
| **Mid** | 30 -- 150 m | Instanced motif families. Simplified animation (walk cycles, idle loops). No physics simulation (visual only). 2K atlas textures. Low-FPS billboard loops. | No direct interaction. Visual presence only. | 30% of triangle budget |
| **Far** | 150 m+ | Silhouette proxies and billboard impostors. Light-response only (emissive glow, ambient color). No animation. Static emissive billboard textures. | None. Pure backdrop. | 10% of triangle budget |

---

## 9. Per-Frame Budgets

Hard budget caps that the Show Director enforces every frame. If any budget is exceeded, the Director demotes entities starting from the farthest, lowest-priority targets.

| Resource | Budget | Near Allocation | Mid Allocation | Far Allocation |
|----------|--------|-----------------|----------------|----------------|
| **Triangle count (in view)** | 5,000,000 | 3,000,000 | 1,500,000 | 500,000 |
| **Proxy swaps per frame** | 4 | -- | -- | -- |
| **Inflations per frame** | 2 | -- | -- | -- |
| **Unique textures in view** | 512 | ~300 | ~150 | ~62 |
| **Full-video billboard surfaces** | 4 (hard cap) | 4 max | 0 | 0 |
| **Low-FPS billboard loops** | 8 | -- | 8 max | 0 |
| **Unique skeletal animations** | 70 total | 50 | 20 | 0 |

### 9.1 Budget Violation Cascade

When a budget is exceeded, the Director applies corrections in this priority order:

1. **Demote farthest mid-tier entities to far.** Cheapest visual impact.
2. **Pause lowest-priority video surfaces.** Fall back to static emissive.
3. **Merge farthest unique materials into atlas.** Reduces draw calls.
4. **Reduce crowd density in mid/far zones.** Despawn farthest instanced NPCs.
5. **Emergency mode (FPS < 35):** All billboards to static, crowd density halved, disable parallax shaders.

### 9.2 Recovery Behavior

When budget headroom returns (e.g., player turns away from dense area), the Director **does not** instantly restore all detail. Restoration follows these rules:

- Promote at most **2 entities per frame** from far to mid.
- Promote at most **1 entity per frame** from mid to near.
- Video surfaces resume only after 0.5 s of sustained budget headroom.
- Crowd density recovers at 10% per second until target is reached.

This prevents oscillation and visible "breathing" of detail levels.

---

## 10. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1.0 | 2026-01-27 | Design Team | Initial draft -- doctrine, invariants, budgets, pseudocode |

---

*End of Show Director Spec v0*
