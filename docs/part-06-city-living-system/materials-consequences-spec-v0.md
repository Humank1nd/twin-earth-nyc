# Materials and Consequences Spec v0 — The Periodic Table of NYC Surfaces

> **Series:** Twin Earth NYC — Part 6: City-as-Living-System
> **Document:** `materials-consequences-spec-v0.md`
> **Status:** Draft v0
> **Last Updated:** 2026-01-27
> **Depends On:** `ontology-spec-v0.md` (entity types, patch system), `field-systems-spec-v0.md` (wetness, noise, light fields)

---

## 1. Governing Principle

> **"Materials are not textures. They are rule modules. Every surface in the city defines how it responds to force, water, light, and sound -- and those responses cascade into evidence, perception, and consequence."**

Twin Earth NYC does not treat materials as cosmetic properties. A material ID on a surface determines friction, breakability, sound emission, visual rain response, AI perception rules, and evidence generation. When glass breaks, that is not just a visual effect -- it is a noise field spike, a witness generation event, an evidence packet, and a Heat bump. The material system is the bridge between physics and narrative consequence.

This document defines the material property table ("periodic table"), the consequence chain rules, and the coupling between materials, fields, and the evidence system.

---

## 2. Material Property Table

Every surface and prop in the simulation is assigned exactly one material ID from the table below. Material IDs are immutable for a given object (a glass window is always glass; it does not become "broken glass" material -- it becomes a glass object in `shattered` damage state).

### 2.1 Core Properties

| Material | ID | Friction (Dry) | Friction (Wet) | Restitution | Hardness | Breakable | Break Threshold (J) | Sound Class | Density (kg/m^3) |
|----------|----|----------------|----------------|-------------|----------|-----------|---------------------|-------------|-------------------|
| **Asphalt** | `MAT_ASPHALT` | 0.70 | 0.40 | 0.20 | High | No (surface damage only) | N/A | `road_surface` | 2300 |
| **Concrete** | `MAT_CONCRETE` | 0.80 | 0.50 | 0.15 | High | Crack on heavy impact | 5000 | `concrete_impact` | 2400 |
| **Steel** | `MAT_STEEL` | 0.40 | 0.25 | 0.50 | Very High | Dent on extreme force | 20000 | `metal_ring` | 7800 |
| **Glass** | `MAT_GLASS` | 0.30 | 0.20 | 0.70 | High (brittle) | Shatters on impact | 50 | `glass_shatter` | 2500 |
| **Painted Metal** | `MAT_PAINTED_METAL` | 0.50 | 0.30 | 0.40 | High | Dent + paint chip | 8000 | `painted_metal_thud` | 7500 |
| **Rubber** | `MAT_RUBBER` | 0.90 | 0.60 | 0.60 | Medium | Tears under extreme | 3000 | `rubber_squeak` | 1100 |
| **Fabric** | `MAT_FABRIC` | 0.60 | 0.30 | 0.10 | Low | Tears easily | 20 | `fabric_rustle` | 300 |
| **Plastic** | `MAT_PLASTIC` | 0.40 | 0.25 | 0.50 | Medium | Cracks | 500 | `plastic_crack` | 1200 |
| **Wood** | `MAT_WOOD` | 0.60 | 0.35 | 0.30 | Medium | Splinters | 2000 | `wood_impact` | 600 |
| **Brick** | `MAT_BRICK` | 0.75 | 0.45 | 0.20 | High | Chips | 4000 | `brick_impact` | 1900 |

### 2.2 Weather Visual Response

Each material responds visually to the wetness field. These responses are driven by shader parameters keyed to `wetness` value at the surface's Patch position.

| Material | Visual Response to Rain (wetness 0.0 to 1.0) | Puddle Formation | Drying Behavior |
|----------|----------------------------------------------|------------------|-----------------|
| **Asphalt** | Darkens uniformly (albedo x (1.0 - 0.3 x wetness)); puddles form in low spots (mesh depressions) | Yes (depressions, cracks) | Slow (porous; shade factor applies) |
| **Concrete** | Darkens uniformly (albedo x (1.0 - 0.25 x wetness)); no streaking | Yes (flat surfaces pool) | Medium (semi-porous) |
| **Steel** | Water beads (discrete droplet particles on surface); high specular reflection (specular += wetness x 0.8) | No (water sheets off) | Fast (non-porous, wind-assisted) |
| **Glass** | Water streaks (animated downward streak texture overlay); view distortion (refraction offset += wetness x 0.02) | No (vertical surfaces drain) | Fast (smooth, gravity-assisted) |
| **Painted Metal** | Water beads (similar to steel but less uniform; paint imperfections trap droplets) | No | Fast |
| **Rubber** | No visual change (hydrophobic surface; water repelled) | No | Instant (water does not adhere) |
| **Fabric** | Darkens significantly (albedo x (1.0 - 0.5 x wetness)); drip particles spawn at edges when wetness > 0.7 | N/A (absorbs, does not pool) | Very slow (absorptive; retains moisture) |
| **Plastic** | Water beads (similar to steel); slight color shift | No | Fast |
| **Wood** | Darkens unevenly (grain-following darkening pattern); prolonged wetness (> 300 s at wetness > 0.5) triggers warp visual state | N/A (absorbs partially) | Slow (semi-porous; warp persists after drying) |
| **Brick** | Darkens unevenly (mortar joints darken faster than brick face); patchy wet pattern | Yes (mortar line channels) | Slow (very porous) |

### 2.3 Sound Properties

Each material defines how it participates in sound generation and propagation within the noise field.

| Material | Impact Sound (dB at 1 m) | Scrape Sound (dB at 1 m) | Sound Reflection Coefficient | Sound Absorption Coefficient | Footstep Sound Class |
|----------|-------------------------|-------------------------|-----------------------------|-----------------------------|---------------------|
| **Asphalt** | 55 | 40 | 0.3 | 0.7 | `footstep_road` |
| **Concrete** | 60 | 45 | 0.4 | 0.6 | `footstep_concrete` |
| **Steel** | 80 | 70 | 0.9 | 0.1 | `footstep_metal` |
| **Glass** | 90 (shatter) | 50 | 0.8 | 0.2 | N/A (not walkable) |
| **Painted Metal** | 70 | 55 | 0.8 | 0.2 | `footstep_metal_muffled` |
| **Rubber** | 30 | 25 | 0.1 | 0.9 | `footstep_rubber` |
| **Fabric** | 20 | 15 | 0.05 | 0.95 | N/A (not walkable in urban context) |
| **Plastic** | 50 | 40 | 0.3 | 0.7 | `footstep_plastic` |
| **Wood** | 55 | 45 | 0.4 | 0.6 | `footstep_wood` |
| **Brick** | 55 | 40 | 0.5 | 0.5 | `footstep_brick` |

### 2.4 AI Perception Properties

Materials affect how AI systems (NPC perception, CCTV analysis) interpret surfaces.

| Material | Visual Transparency | Occlusion Factor (AI line-of-sight) | Thermal Signature | Anomaly Residue Retention |
|----------|--------------------|------------------------------------|-------------------|--------------------------|
| **Asphalt** | Opaque | 1.0 (full occlusion) | Absorbs heat; warm in sun | High (porous; stain persists) |
| **Concrete** | Opaque | 1.0 | Moderate thermal mass | High (porous) |
| **Steel** | Opaque | 1.0 | Reflects ambient; cool in shade | Low (non-porous; residue washes off) |
| **Glass** | Transparent (0.9 transmittance when clean; 0.6 when wet/dirty) | 0.1 (minimal occlusion; AI can see through) | Transparent to thermal | Very low (smooth; residue slides off) |
| **Painted Metal** | Opaque | 1.0 | Similar to steel | Low |
| **Rubber** | Opaque | 1.0 | Insulating; thermal neutral | Medium |
| **Fabric** | Opaque (but thin; AI treats as partial cover at 0.7 occlusion) | 0.7 | Insulating | High (absorptive) |
| **Plastic** | Varies (clear plastic = 0.7 transmittance; opaque plastic = 0.0) | 0.3 (clear) / 1.0 (opaque) | Insulating | Medium |
| **Wood** | Opaque | 1.0 | Moderate; warm tone | High (porous; grain traps residue) |
| **Brick** | Opaque | 1.0 | High thermal mass; slow temperature change | Very high (extremely porous) |

---

## 3. Damage State System

Every breakable object has a damage state machine. Damage states are discrete, not continuous. Transitions are triggered by impact energy exceeding the material's break threshold.

### 3.1 Damage State Definitions

| Damage State | Visual Effect | Functional Effect | Reversible | Patch Recording |
|--------------|--------------|-------------------|------------|-----------------|
| `pristine` | Default appearance | Full material properties apply | N/A (initial state) | None |
| `scratched` | Surface scratch marks (normal map overlay) | No functional change | Yes (city-services repair) | None (cosmetic only) |
| `cracked` | Visible crack lines (geometry displacement or decal) | Structural integrity -30%; increased break probability on next impact | Yes (city-services repair) | Damage mark recorded on Patch |
| `dented` | Deformation (vertex displacement on mesh) | Collision shape modified; may affect door/mechanism function | Yes (city-services repair, slow) | Damage mark recorded on Patch |
| `shattered` | Fragmented geometry (pre-fractured mesh swap); debris particles | Object non-functional; hole in surface (glass: see-through, door: passable); debris becomes physics props | No (replacement only) | Damage mark recorded on Patch; debris entities spawned |
| `destroyed` | Object removed from scene; scorch/debris mark on ground | Object no longer exists as entity; replaced by Patch damage mark | No (replacement only) | Heavy damage mark on Patch; ledger entry for destruction |

### 3.2 Damage State Transitions by Material

| Material | pristine -> scratched | scratched -> cracked | cracked -> shattered | shattered -> destroyed | Special Rules |
|----------|----------------------|---------------------|---------------------|----------------------|---------------|
| **Asphalt** | Impact > 100 J | Impact > 1000 J | Impact > 5000 J | N/A (surface only; potholes form at `cracked`) | Pothole: `cracked` state creates vehicle hazard |
| **Concrete** | Impact > 200 J | Impact > 2000 J | Impact > 5000 J | Impact > 10000 J | Rebar exposed at `shattered`; structural concern at `cracked` |
| **Steel** | Impact > 500 J | N/A (steel skips `cracked`) | N/A | Impact > 20000 J (extreme: vehicle collision at speed) | `dented` replaces `cracked`; dent at > 5000 J |
| **Glass** | Impact > 10 J | Impact > 30 J | Impact > 50 J | N/A (shattered is terminal for glass) | Single impact can skip states if energy >> threshold; thermal shock (fire near cold glass) shatters at 30 J |
| **Painted Metal** | Impact > 300 J (paint chip) | Impact > 3000 J | N/A | Impact > 8000 J | Paint chip reveals bare metal; corrosion visual over time if wet |
| **Rubber** | Impact > 500 J | Impact > 1500 J (tear initiation) | Impact > 3000 J (full tear) | N/A | Rubber deforms rather than cracks; `cracked` = tear in rubber |
| **Fabric** | Impact > 5 J (scuff) | Impact > 10 J (rip) | Impact > 20 J (torn) | N/A | Very low thresholds; wind > 15 m/s can cause tear on damaged fabric |
| **Plastic** | Impact > 50 J | Impact > 300 J | Impact > 500 J | Impact > 1000 J | UV degradation over time (cosmetic only, not simulated in v0) |
| **Wood** | Impact > 100 J (gouge) | Impact > 1000 J (split) | Impact > 2000 J (splinter) | Impact > 4000 J | Wet wood (`wetness > 0.5 for > 300 s`): all thresholds reduced by 30% |
| **Brick** | Impact > 200 J (chip) | Impact > 2000 J | Impact > 4000 J | Impact > 8000 J | Individual brick displacement at `cracked`; mortar failure at `shattered` |

---

## 4. Consequence Chain Rules

The material system does not exist in isolation. Every material interaction generates downstream consequences that ripple through fields, the evidence system, and NPC behavior. The following rules define these consequence chains.

### 4.1 Impact Consequence Chain

When an object impacts a surface, the following chain executes:

```
[Impact Event]
  |
  +--> [1. Energy Calculation]
  |        impact_energy = 0.5 x mass x velocity^2 (Joules)
  |
  +--> [2. Damage State Transition]
  |        if impact_energy > material.break_threshold:
  |            advance damage state
  |            generate visual effect (crack decal, shatter mesh, debris)
  |
  +--> [3. Sound Event]
  |        sound_dB = material.impact_sound + 10 x log10(impact_energy / reference_energy)
  |        write to noise field at impact position
  |        sound class = material.sound_class
  |
  +--> [4. Visual Mark on Patch]
  |        if damage state advanced:
  |            record damage mark on containing Patch
  |            mark type = material.damage_visual_type
  |            mark persists until cleanup or decay
  |
  +--> [5. Evidence Generation]
  |        if sound_dB > 70:
  |            generate evidence packet: { type: "impact_sound", position, timestamp, sound_dB, material }
  |            send to Event Bus
  |        if damage state = shattered or destroyed:
  |            generate evidence packet: { type: "property_damage", position, timestamp, object_id, material, damage_state }
  |            send to Event Bus
  |
  +--> [6. Witness Generation]
  |        witnesses = NPCs within radius = sound_dB / 2 (meters) AND line-of-sight not occluded
  |        each witness generates: evidence packet { type: "witness_observation", observer_id, event_ref, confidence }
  |        confidence modified by noise field (see field-systems-spec-v0.md Section 4.4)
  |
  +--> [7. Heat Bump]
  |        if damage state = shattered or destroyed:
  |            Physical Heat += 0.05
  |            Social Heat += 0.02 (if witnesses > 3)
  |            Institutional Heat += 0.01 (if CCTV captured event)
  |
  +--> [8. Ledger Commit]
           all evidence packets committed to immutable ledger
           (information conservation: see ontology-spec-v0.md Section 5.3)
```

### 4.2 Wet Surface Consequence Chain

When the wetness field value at a surface exceeds thresholds, the following consequences activate:

```
[Wetness > 0.0]
  |
  +--> [1. Traction Reduction]
  |        surface_traction = material.friction_dry x (1.0 - (material.friction_dry - material.friction_wet) x wetness)
  |        (linearly interpolates between dry and wet friction)
  |
  +--> [2. Vehicle Braking Distance]
  |        braking_distance = base_distance x (1.0 + 1.5 x wetness)
  |        (wet roads = 2.5x braking distance at full saturation)
  |
  +--> [3. NPC Slip Chance]
  |        if material.friction_wet < 0.3 AND wetness > 0.5:
  |            slip_probability = 0.02 per step (per NPC movement tick)
  |            slip event --> stumble animation, possible fall, possible minor injury
  |            fall on hard surface (hardness = High+): Health -= 5
  |
  +--> [4. Visual Response]
  |        apply material-specific wet shader (see Section 2.2)
  |        if wetness > 0.8 AND surface is flat (asphalt, concrete):
  |            enable puddle rendering at this cell
  |            puddle reflection captures light field at this position
  |
  +--> [5. CCTV Confidence]
           CCTV cameras viewing wet surfaces:
               image_confidence -= wetness x 0.15
               rain streaks on lens: additional -0.10 if rain active
               puddle reflections may create false positives (reflection of person != person)
```

### 4.3 Glass Break Consequence Chain

Glass breakage is the highest-consequence single-material event due to its sound signature, evidence generation, and Heat impact. It is detailed separately because of its narrative importance.

```
[Glass Break Event]
  |
  +--> [1. Sound Spike]
  |        noise_field write: +90 dB at break position
  |        sound class: glass_shatter (distinctive; high witness recognition)
  |        audible range: ~80 m (before attenuation to ambient)
  |
  +--> [2. Visual Effect]
  |        shatter mesh swap (pre-fractured geometry)
  |        debris particles: 20-50 glass shards, physics-simulated for 2 s then converted to decals
  |        debris shards inherit velocity of impacting object + radial scatter
  |
  +--> [3. Structural Consequence]
  |        window/door: now passable (hole in surface)
  |        AI occlusion: glass was 0.1 occlusion; shattered glass frame = 0.0 occlusion (fully open)
  |        wind field: new opening allows wind through-flow (interior wind if building has openings on both sides)
  |        noise field: new opening allows sound through-flow (interior sounds leak out)
  |
  +--> [4. Evidence Cascade]
  |        evidence packets generated:
  |            { type: "glass_shatter_sound", position, timestamp, dB: 90 }
  |            { type: "property_damage", object_id, material: glass, damage_state: shattered }
  |            per witness: { type: "witness_observation", ... }
  |            per CCTV with coverage: { type: "cctv_capture", frame_ref, confidence }
  |
  +--> [5. Heat Bump]
  |        Physical Heat += 0.05
  |        Social Heat += 0.05 (glass break is alarming; draws attention)
  |        Institutional Heat += 0.03 (property damage triggers authority interest)
  |
  +--> [6. NPC Behavioral Response]
           NPCs within 20 m: startle reaction (flinch animation, head turn toward source)
           NPCs within 50 m: awareness state = alert; look toward sound origin
           Authority NPCs: dispatch event if not already en route
           Pedestrians near glass: routing avoidance of debris zone (2 m radius for 60 s)
```

---

## 5. Material-Field Interaction Summary

This matrix summarizes how each material modifies field values and entity behavior when interacting with the field systems.

| Material | Wind Response | Noise Modification | Light Modification | Wetness Interaction | Heat Contribution |
|----------|-------------|-------------------|-------------------|--------------------|--------------------|
| **Asphalt** | Deflects wind upward at surface; no flutter | Moderate absorption (0.7) | Low reflectance; darkens when wet | Absorbs; puddles in depressions; slow dry | Impact damage contributes Physical Heat |
| **Concrete** | Similar to asphalt | Moderate absorption (0.6) | Low reflectance; uniform darkening | Absorbs; pools on flat surfaces | Structural crack triggers Physical Heat |
| **Steel** | Deflects wind; may vibrate (hum) in strong wind > 10 m/s | High reflection (0.9); causes echo patterns | High specular reflection; glint in sun | Beads and sheets off; fast dry | Dent triggers mild Physical Heat |
| **Glass** | No wind interaction (rigid, thin) | High reflection (0.8); sound passes through when broken | High transmittance (0.9); distorts view when wet | Streaks; fast drain on vertical surfaces | Shatter = significant multi-channel Heat |
| **Painted Metal** | Similar to steel; paint does not flutter | High reflection (0.8) | Moderate reflectance; color-dependent | Beads; paint chip exposes bare metal to wetness-corrosion | Dent + paint chip = mild Social Heat (vandalism read) |
| **Rubber** | No significant interaction | Very high absorption (0.9); dampens sound | Low reflectance; matte | Hydrophobic; instant repel | Tear = minimal Heat |
| **Fabric** | Flutters in wind > 3 m/s; billows > 8 m/s; tears > 15 m/s if damaged | Very high absorption (0.95); sound deadening | Low reflectance; absorbs light | Absorbs; darkens; drips at edges; retains moisture | Tear = minimal Heat |
| **Plastic** | Light plastic items may blow away in wind > 12 m/s | Moderate absorption (0.7) | Variable (clear = transmissive; opaque = matte) | Beads; fast dry | Crack = minimal Heat |
| **Wood** | No flutter (rigid); may creak in strong wind | Moderate absorption (0.6); warm resonance | Moderate reflectance; grain pattern | Absorbs; darkens unevenly; warps over time | Splinter = mild Physical Heat |
| **Brick** | No wind interaction (massive) | Moderate absorption/reflection (0.5/0.5) | Low reflectance; patchy wet darkening | Highly absorbent; slow dry; mortar channels | Chip = minimal; structural failure = high Physical Heat |

---

## 6. Implementation Notes

### 6.1 Material Assignment Pipeline

1. Every mesh in the asset pipeline is tagged with a `material_id` from the table in Section 2.1.
2. Material IDs are stored as an integer component on the entity (`MaterialID` component in ECS).
3. Patches inherit the dominant surface material from the ground mesh at their center position.
4. Multi-material objects (e.g., a painted metal door with a glass window) use the material of the **sub-mesh** at the contact point for consequence calculations. The object's primary material ID is the dominant surface area material.

### 6.2 Consequence Chain Execution

All consequence chains execute synchronously within the physics tick that generated the triggering event. The chain must complete before the next entity tick begins. This ensures:

- Sound events are written to the noise field in the same tick as the impact.
- Evidence packets are queued in the same tick (committed asynchronously by the ledger).
- Heat bumps are applied in the same tick (processed at the next Heat field update).

### 6.3 Performance Considerations

- Damage state transitions are rare events (seconds to minutes apart, not per-frame). The cost of consequence chain execution is negligible.
- Material property lookups are table lookups by integer ID: O(1), no branching.
- Sound contribution from material impacts is aggregated into the noise field (same O(cells) pipeline as all other noise sources).
- Visual effects (wet shaders, damage decals) are GPU-driven; material parameters are uploaded as per-instance data in the instancing buffer.

### 6.4 Extension Path

The material table is designed to be extended. Future versions may add:

- **Ice** (`MAT_ICE`): extreme low friction when wet; forms from prolonged sub-zero wetness.
- **Vegetation** (`MAT_VEGETATION`): high absorption for noise and light; grows over time on neglected surfaces.
- **Water** (`MAT_WATER`): for puddle/fountain surfaces; full fluid sim integration.
- **Neon Tube** (`MAT_NEON`): glass variant with internal light source; break = light source loss + gas release visual.
- **Anomaly-Touched** (`MAT_ANOMALY`): any material post-anomaly exposure; altered friction, sound, and visual properties.

Each new material must define all columns in the property table (Section 2.1), all weather visual responses (Section 2.2), all sound properties (Section 2.3), and all AI perception properties (Section 2.4) before integration.

---

*End of document. For the entity hierarchy that materials attach to, see `ontology-spec-v0.md`. For field systems that materials interact with, see `field-systems-spec-v0.md`. For the hierarchy and escalation rules that consequence chains feed into, see `hierarchy-coupling-rules-v0.md`.*
