# Twin Earth NYC -- Architecture Specification v0

**Document:** Part 2, Deliverable 1
**Status:** Draft v0.1
**Scope:** Simulation Architecture for the Times Square Vertical Slice
**Last Updated:** 2026-01-27

---

## Table of Contents

1. [Truth Engine Boundaries](#1-truth-engine-boundaries)
2. [Illusion Engine Rules (Show Director v0)](#2-illusion-engine-rules-show-director-v0)
3. [Trust Ledger v0 Scope and Schema](#3-trust-ledger-v0-scope-and-schema)

---

## 1. Truth Engine Boundaries

The Truth Engine is the authoritative simulation layer. Every system that affects gameplay logic, NPC reasoning, evidence generation, or persistent world state must route through the Truth Engine. Visual presentation systems may approximate, but they must never contradict the Truth Engine's declared state.

### 1.1 Canonical Units and Coordinate Systems

| Property | Specification |
|---|---|
| **Linear Unit** | Meters (SI) |
| **Up Axis** | +Y |
| **Handedness** | Right-handed |
| **Angular Unit** | Radians (internal), Degrees (config/UI) |
| **Time Unit** | Seconds (double-precision) |
| **Mass Unit** | Kilograms |
| **Temperature Unit** | Kelvin (internal), Celsius (display) |

#### World Origin Policy

The simulation uses a **floating origin** system to maintain numerical precision across the playable area:

- **Logical Origin:** Times Square center, latitude 40.7580N, longitude 73.9855W, elevation 10.0m above WGS84 ellipsoid. This is the permanent reference for all geospatial mappings and ledger coordinates.
- **Camera-Relative Rebase:** The rendering origin rebases when the active camera moves more than **5,000 meters** from the current floating origin. All transform hierarchies shift in a single frame. Physics bodies are teleported atomically.
- **Precision Guarantee:** Within the 5km rebase radius, single-precision floats maintain sub-millimeter accuracy (worst case ~0.3mm error at 5km). All ledger coordinates are stored as double-precision offsets from the logical origin.
- **Rebase Event:** On rebase, the engine fires a `WORLD_ORIGIN_REBASE` event containing the old and new origin in ECEF doubles. All subsystems holding cached world-space positions must subscribe and update. Failure to handle rebase is a fatal contract violation.

#### Georeference Mapping Pipeline

The coordinate pipeline transforms data through three stages:

```
Cesium (WGS84 ECEF)  -->  Engine (ENU Local Meters)  -->  Omniverse (USD Stage)
      Source                   Runtime Truth                  Presentation
```

| Stage | System | Convention | Notes |
|---|---|---|---|
| **Source** | Cesium / OpenStreetMap / GIS imports | WGS84 ECEF (Earth-Centered, Earth-Fixed) | Double-precision geodetic coordinates |
| **Runtime** | Engine Truth Layer | ENU local meters (East-North-Up), origin at Times Square center (~40.758N, 73.9855W) | Right-handed, Y-up. East = +X, North = +Z, Up = +Y |
| **Presentation** | NVIDIA Omniverse / USD | USD stage meters, Z-up convention | Axis conversion applied at USD export: Engine Y-up to USD Z-up (swap Y/Z, negate new Y). All USD prims carry `metersPerUnit = 1.0` |

The ENU-to-ECEF back-transform is maintained for any system that needs to query real-world geospatial data at runtime (e.g., astronomical sun position, satellite imagery streaming).

### 1.2 Collision Truth Surfaces

The Times Square slice contains five categories of collision surface, each with distinct gameplay and navigation implications:

| Surface | Material | Geometry Representation | Nav Properties |
|---|---|---|---|
| **Sidewalks** | Concrete | Flat navmesh polygons | Walkable. Primary pedestrian surface. Slope tolerance per canonical spec. |
| **Curbs** | Concrete/granite | Step-up extrusions, 15cm height | Walkable step-up for pedestrians. Barrier for wheeled vehicles under clearance threshold. |
| **Steps / Stairs** | Concrete, metal (TKTS red steps) | Triangle mesh, 18cm risers, 28cm treads | Walkable. NPCs use stair locomotion blend. The TKTS red steps (Father Duffy Square) are a landmark collision surface with 24 risers. |
| **Barriers / Medians** | Steel bollards, concrete planters, jersey barriers | Simplified convex hulls | Impassable for pedestrians and vehicles. Destructible flag per-instance (most are indestructible in v1). |
| **Roads** | Asphalt | Heightfield (subtle crown camber) | Vehicle-only zones. Pedestrians may cross but receive jaywalking flag. NPCs avoid unless at crosswalk or in panic state. |

#### Collision Constants

| Constant | Value | Rationale |
|---|---|---|
| Maximum walkable slope | 35 degrees | ADA/IBC ramp maximum ~8.3% (4.8 degrees) for accessibility; 35 degrees is the gameplay upper bound for scramble-walk |
| Maximum step height | 25cm | Standard stair riser is 18cm; 25cm allows for curbs and irregular geometry |
| Standard curb step | 15cm | NYC DOT standard curb height: 15cm (6 inches) |
| Vehicle clearance height | 2.1m | Minimum underpass clearance for standard vehicles; anything below blocks vehicle pathing |
| Bollard spacing | 1.5m center-to-center | Allows pedestrian flow, blocks vehicles |
| Navmesh cell size | 0.15m | Sufficient to resolve curbs and steps |
| Navmesh cell height | 0.10m | Resolves step geometry at 18cm risers |

### 1.3 Physics Truth

**Authority:** NVIDIA Omniverse PhysX is the authoritative physics solver for v1. No secondary physics system may override or bypass PhysX results for gameplay-affecting interactions.

#### Physics Material Table

| Material | Static Friction | Dynamic Friction | Restitution | Density (kg/m3) | Damping | Notes |
|---|---|---|---|---|---|---|
| Asphalt | 0.70 | 0.65 | 0.20 | 2300 | 0.05 | Road surfaces |
| Concrete | 0.80 | 0.75 | 0.15 | 2400 | 0.03 | Sidewalks, curbs, building bases |
| Metal (bare) | 0.40 | 0.35 | 0.50 | 7800 | 0.01 | Structural steel, railings, grates |
| Glass | 0.30 | 0.25 | 0.70 | 2500 | 0.02 | Storefronts, windows (pre-shatter) |
| Painted Metal | 0.50 | 0.45 | 0.40 | 7800 | 0.02 | Vehicles, signage frames, traffic lights |
| Rubber | 0.90 | 0.85 | 0.60 | 1100 | 0.50 | Tires, floor mats, bumper guards |
| Wood | 0.60 | 0.55 | 0.30 | 600 | 0.10 | Vendor stalls, benches |
| Fabric/Awning | 0.50 | 0.45 | 0.10 | 200 | 0.40 | Canopies, banners |
| Water (puddle) | 0.20 | 0.15 | 0.05 | 1000 | 0.30 | Surface friction modifier overlay |

#### Physics Fidelity Tiers

| Tier | Zone | Update Rate | Collision | Constraints | Use Case |
|---|---|---|---|---|---|
| **Hero** | 0-30m from camera | 60 Hz (fixed step) | Full continuous collision detection (CCD) | All joints, breakable constraints, ragdoll | Player interactions, nearby NPCs, story-critical objects |
| **Standard** | 30-150m from camera | 30 Hz | Discrete collision | Simplified joints, no breakable constraints | Mid-range vehicles, falling debris, ambient physics |
| **Background** | 150m+ | 15 Hz | Broadphase only, swept AABB | No joints, kinematic-only | Distant traffic, swaying signs, flag cloth |
| **Dormant** | Off-screen or >300m | 0 Hz (frozen) | None | None | State preserved but not simulated; reactivates on proximity |

Tier transitions are smoothed over 3 frames to prevent visible pops. Objects under player observation (gaze ray intersection) are promoted one tier regardless of distance.

### 1.4 Sensor Truth

**Cardinal Rule:** *NPCs perceive only through their declared sensor loadout and their memory graph. No NPC may access ground-truth world state directly. Violation of this rule is a P0 bug.*

#### v1 Sensor Suite

| Sensor | FOV | Range | Update Rate | Noise Model | Latency | Notes |
|---|---|---|---|---|---|---|
| **RGB Camera** (eyes) | 90 degrees horizontal, 60 degrees vertical | 50m (recognition), 200m (detection) | 30 Hz | Gaussian per-channel, sigma = 0.02 | 30ms | Primary visual sense. Affected by lighting, occlusion, weather. Recognition range halved at night without street lighting. |
| **Depth Probes** (spatial awareness) | 60 degrees cone | 20m | 15 Hz | Uniform +/-5cm | 15ms | Proxy for proprioception + spatial reasoning. Allows NPCs to navigate without perfect geometry knowledge. |
| **Audio Proxy** | 360 degrees omnidirectional | 100m (loud), 15m (conversation), 5m (whisper) | 10 Hz | Distance-dependent attenuation + reflection estimation | 50ms | Deferred to v1.1. For v1, NPCs use a simplified alert radius system as placeholder. |

#### Sensor Degradation Conditions

| Condition | RGB Camera Effect | Depth Probe Effect | Audio Effect |
|---|---|---|---|
| Night (no street light) | Range halved, noise sigma x3 | No effect | No effect |
| Rain (heavy) | Range reduced 30%, noise sigma x2 | Range reduced 20% | Range reduced 40%, localization accuracy halved |
| Fog / steam | Range scales with visibility distance | Range reduced proportionally | No effect |
| Crowd density >2/m2 | Occlusion-based, recognition failures increase | Effective range capped at 3m | Conversation range reduced to 2m |
| Anomaly bleed zone | Noise sigma x5, color shift artifacts | Range fluctuates +/-50% | Phantom source probability 20% |

### 1.5 Timebase

#### Global Simulation Clock

The simulation runs on a **UTC-like global clock** starting at a configurable epoch (default: 2025-06-15T08:00:00Z, a summer morning). The clock is:

- **Monotonic:** It never runs backward during normal play.
- **Configurable time scale:** Adjustable from 1x (real-time) to 60x (one real second = one sim minute). Default gameplay scale is **1x** for exploration, **12x** for narrative time-skips.
- **Deterministic:** Given the same seed and input sequence, the clock produces identical state at every tick.

#### Subsystem Update Rates

| Subsystem | Target Rate | Timing Mode | Notes |
|---|---|---|---|
| **Physics (PhysX)** | 60 Hz | Fixed timestep (16.67ms) | Accumulator model; interpolated for rendering |
| **AI Decisions** | 10 Hz | Fixed timestep (100ms) | Behavior tree tick, sensor processing, memory writes |
| **Traffic Logic** | 2 Hz | Fixed timestep (500ms) | Signal phase changes, vehicle route decisions, intersection arbitration |
| **Weather System** | 0.1 Hz | Fixed timestep (10s) | Cloud evolution, precipitation intensity, wind vector changes |
| **Ledger Commits** | Event-driven | Asynchronous (ordered queue) | Commits fire on observation corroboration, authority action, or player explicit commit |
| **Rendering** | Variable (target 60 Hz) | Variable timestep | Decoupled from simulation; interpolates between physics states |
| **Audio Mix** | 60 Hz | Fixed timestep | Matches physics rate for spatial accuracy |
| **Animation** | 30 Hz (blend), 60 Hz (root motion) | Fixed timestep | Root motion feeds back into physics at 60 Hz |

#### Pause, Step, and Replay

| Feature | Mechanism | Constraints |
|---|---|---|
| **Pause** | All fixed-timestep subsystems freeze. Rendering continues (camera-only mode). UI remains interactive. | Pause does not affect the ledger clock; paused time is not recorded. |
| **Single Step** | Advances exactly one physics tick (16.67ms). All subsystems that would fire within that window execute once. | Available in debug/dev builds only. |
| **Deterministic Replay** | Full replay from `seed + ordered_event_log`. The event log captures all external inputs: player actions, random seed consumption points, network events (if any). | Replay divergence is a P0 bug. Replay validation runs nightly in CI. The event log format is a flat binary sequence: `[tick:u64][event_type:u16][payload:var]`. |
| **Time Scale Change** | Smooth ramp over 1 real second to avoid physics instability. During ramp, physics sub-steps are clamped to max 4 per frame. | Scale changes above 10x disable hero-tier physics (drops to standard tier for all objects). |

---

## 2. Illusion Engine Rules (Show Director v0)

The Illusion Engine (internally: **Show Director**) manages everything the player perceives. Its mandate: *make every frame feel like a real place without simulating a real place everywhere at once.* The Show Director may bend, simplify, and fake--but it must never contradict the Truth Engine's declared state within the player's observable context.

### 2.1 Attention Model

The player's **attention** is a composite score computed per-frame for every managed entity:

```
Attention(entity) = w_frustum * Frustum(entity)
                  + w_distance * (1 - Distance(entity) / max_distance)
                  + w_velocity * VelocityRelevance(player, entity)
                  + w_gaze * GazeProximity(entity)
```

| Component | Weight (default) | Computation |
|---|---|---|
| **Frustum** | 0.35 | 1.0 if inside camera frustum, 0.0 if outside. Padded by 10 degrees on each edge for pre-streaming. |
| **Distance** | 0.30 | Linear falloff from 1.0 at 0m to 0.0 at `max_distance` (300m). Clamped. |
| **Player Velocity** | 0.15 | Entities in the player's forward velocity cone (+/-30 degrees, scaled by speed) receive a boost. At sprint speed, forward entities get +0.15; stationary player = no boost. |
| **Gaze Proxy** | 0.20 | Raycast from screen center into world. Entities within 5 degrees of the gaze ray receive full weight. Falls off to 0.0 at 20 degrees. |

Entities below attention threshold 0.05 are candidates for dormancy. Entities above 0.80 are flagged for hero-tier treatment.

#### Distance Bands

| Band | Range | Fidelity | Asset Strategy | Physics | AI |
|---|---|---|---|---|---|
| **Near** | 0-30m | Full | Unique assets, full material complexity, subsurface scattering on skin, readable text on signs | Hero tier (60 Hz, CCD) | Full behavior tree, individual personality, reactive dialogue |
| **Mid** | 30-150m | Reduced | Instanced motif assets (e.g., "generic Broadway building" x4), simplified animation (half bone count), LOD1 meshes | Standard tier (30 Hz, discrete) | Simplified behavior (state machine), archetype personality, no dialogue |
| **Far** | 150m+ | Minimal | Silhouette meshes + emissive map response, billboard proxies for crowds, baked light response | Background tier (15 Hz) or dormant | No individual AI; flow-field driven or scripted loops |

### 2.2 Invariants (Things That Must Never Change)

The Show Director may improvise details, but the following **invariants** are sacred. Violating any invariant under any LOD, distance, or performance condition is a **ship-blocking bug**:

| Category | Invariant | Tolerance |
|---|---|---|
| **Scale Anchors** | Human NPC height: 1.75m (+/-0.15m for variation) | Must be visually correct relative to doors and vehicles at all distances |
| | Standard taxi length: 4.8m | +/-0.1m at near band; silhouette must read as "taxi" at far band |
| | Standard door height: 2.1m | +/-0.05m; must be walkable without ducking |
| | Traffic light height: 5.5m (signal center) | +/-0.2m |
| **Landmark Silhouettes** | One Times Square (triangular wedge, illuminated facade) | Recognizable from all angles within slice bounds |
| | Marriott Marquee (curved LED facade) | Curve profile must be correct; content may simplify |
| | TKTS Red Steps (Father Duffy Square) | Step count and red color must be correct; individual step detail may simplify |
| **Intersection Geometry** | The "bowtie" where Broadway crosses 7th Avenue | Lane geometry, crosswalk positions, and island shapes are locked to survey data |
| | Signal positions and count | Every real signal must have a corresponding sim signal |

#### Allowed Variance (Things the Show Director May Change)

- Micro-details: cracks in sidewalks, litter placement, puddle shapes, gum spots
- Clutter: newspaper boxes, trash bags, construction cones (non-landmark)
- Window interiors: may be parallax-mapped fakes, black voids, or simple rooms; need not match any real interior
- Far signage text: text on buildings beyond 100m may be lorem ipsum or simplified; brand names simplified to avoid licensing issues
- NPC clothing details: fabric weave, button count, accessory variation
- Vehicle color and plate: randomized per spawn; only class silhouette matters

### 2.3 Perceptual LOD Table

#### Buildings

| LOD Level | Distance Trigger | Geometry | Materials | Lighting | Animation |
|---|---|---|---|---|---|
| **LOD0** (Near) | 0-50m | Unique mesh, full detail, modeled window frames, AC units, fire escapes | Full PBR, 4K textures, parallax occlusion on windows | Per-pixel lighting, real-time shadows, screen-space reflections | Animated signage, blinking lights, steam vents |
| **LOD1** (Mid) | 50-150m | Motif-instanced mesh, simplified silhouette, merged small features | 2K textures, simplified PBR (no parallax) | Shadow maps at reduced resolution, baked ambient | Simplified signage animation (2fps texture flip), static vents |
| **LOD2** (Far) | 150m+ | Silhouette mesh + emissive billboard face | 1K emissive map + flat color | No real-time shadows, emissive-only response | Static emissive; brightness modulated by time-of-day |

#### Billboards and Signage

| LOD Level | Distance Trigger | Content | Update Rate | Power Draw Simulation |
|---|---|---|---|---|
| **LOD0** | 0-30m | Full video playback, readable text, accurate color | 30fps video texture | Emissive matches real LED panel output (~6000 nits) |
| **LOD1** | 30-100m | Low-resolution loop (4fps), text simplified to color blocks | 4fps texture flip | Emissive reduced 50% (perceptual match at distance) |
| **LOD2** | 100m+ | Static emissive rectangle, color-sampled from LOD0 dominant palette | Static | Emissive glow halo only |

#### Props (Street Furniture, Vehicles, Vendor Carts)

| LOD Level | Distance Trigger | Geometry | Physics | Interaction |
|---|---|---|---|---|
| **LOD0** | 0-30m | Unique mesh, full detail | Hero-tier, interactive | Fully interactive (open doors, push carts, read signs) |
| **LOD1** | 30-100m | Simplified mesh (50% polycount), merged small parts | Standard-tier, non-interactive | Visual only; no player interaction |
| **LOD2** | 100m+ | Billboard sprite or removed entirely | None | None |

#### Crowds (NPCs)

| LOD Level | Distance Trigger | Geometry | Animation | AI |
|---|---|---|---|---|
| **LOD0** | 0-20m | Unique skeletal mesh, full bone rig (65 bones), individual face blend shapes | Full animation set, procedural gaze, lip sync | Full behavior tree, individual memory, reactive |
| **LOD1** | 20-80m | Instanced archetype mesh (from pool of 24 archetypes), reduced rig (32 bones), no face detail | Reduced animation set (walk/idle/turn), no facial animation | State-machine AI, group behavior, no dialogue |
| **LOD2** | 80m+ | Animated billboard cards (8 variants per archetype), 2-frame walk cycle | Billboard rotation to face camera | Flow-field movement, no individual behavior |

### 2.4 Forced Perspective and Atmospheric Effects

#### Camera Presets

| Preset | Focal Length Equivalent | Use Case | Perceptual Effect |
|---|---|---|---|
| **Normal** (default) | 35mm | Standard exploration | Natural sense of space; buildings feel tall but not oppressive |
| **Mild Telephoto** | 50-70mm | Approaching landmarks, dramatic reveals, mission briefings | Compression makes buildings feel monumental, crowds feel denser |
| **Wide** | 24mm | Chase sequences, disorientation, anomaly encounters | Exaggerated perspective, stretched edges, chaos and speed |

The Show Director may subtly shift between presets during gameplay to amplify emotional beats. Transitions ramp over 2-4 seconds and never exceed 5mm/s focal length change to avoid player nausea.

#### Atmospheric Haze

```
haze_density(d, humidity, heat_island_factor) =
    base_haze * (1.0 + humidity * 0.8) * (1.0 + heat_island_factor * 0.3) * (1.0 - exp(-d * extinction_coeff))
```

| Parameter | Default Value | Range |
|---|---|---|
| `base_haze` | 0.003 | 0.0 - 0.02 (clear to heavy smog) |
| `humidity` | 0.5 | 0.0 - 1.0 |
| `heat_island_factor` | 0.4 | 0.0 - 1.0 (NYC urban heat island) |
| `extinction_coeff` | 0.008 per meter | 0.001 - 0.05 |

At night, haze scatters billboard light, creating the characteristic Times Square glow dome. The glow dome radius is approximately 500m and is rendered as a post-process volumetric effect.

#### Billboard Glow Scaling

Billboards in Times Square emit significant light. The Show Director scales emissive intensity non-linearly with distance to maintain the perceptual "wall of light" effect:

```
emissive_scale(d) = base_emissive * (1.0 + glow_boost * max(0, 1.0 - d / glow_range)^2)
```

| Parameter | Value |
|---|---|
| `base_emissive` | 1.0 (physically-based nit value) |
| `glow_boost` | 3.0 (perceptual compensation) |
| `glow_range` | 200m |

At distance 0m, emissive is 4x physical (the eye adapts; this compensates for HDR tone mapping compression). At 200m+, emissive returns to physical values but haze scattering takes over.

#### Skyline Silhouette Accuracy

The following structures must be silhouette-accurate when visible from within the Times Square slice. They are rendered as LOD2 silhouette meshes with emissive window patterns:

| Structure | Direction from TSQ Center | Distance | Visible Conditions |
|---|---|---|---|
| **One Times Square** | Within slice (south end of bowtie) | ~0m (inside slice) | Always (it is the defining landmark) |
| **Empire State Building** | South-southeast | ~1.2km | Clear weather, looking south down Broadway or 7th Ave |
| **Chrysler Building** | East-southeast | ~1.5km | Clear weather, looking east along 42nd St or visible in gaps |
| **Times Square Tower** (One Astor Plaza) | Within slice (west edge) | ~0m (inside slice) | Always |
| **1 Bryant Park** (Bank of America Tower) | East | ~0.4km | Clear weather, looking east on 42nd/43rd |

### 2.5 Backstage Corridors and Streaming Seams

#### Backstage Spaces

"Backstage" areas are spaces the player can see or enter but which are not part of the core Truth Engine simulation. They serve as:

- **Transition zones** between fully simulated regions
- **Mystery spaces** that hint at content beyond the current slice
- **Performance buffers** where the engine streams in/out content

| Backstage Type | Example | Treatment |
|---|---|---|
| **Service Alleys** | Side alleys off 43rd, 44th, 45th streets | Modeled to 20m depth with decreasing detail. Dead-end with diegetic blocker (dumpsters, locked gate). Ambient lighting only. |
| **Subway Entrances** | Times Square-42nd St station entrances (6 real entrances in slice) | Stairs descend 5m to a locked turnstile or "temporarily closed" sign. Sound design suggests trains below. v2 candidate for full subway level. |
| **Building Interiors** | Lobbies visible through glass storefronts | Parallax interior mapping for most. 2-3 hero interiors (e.g., a diner, a souvenir shop) modeled to 10m depth with simple NPC loops. |

#### Streaming Masks

When the engine needs to stream in or swap large chunks of content, it uses **diegetic masks** -- in-world elements that justify visual disruption:

| Mask Type | Visual | Blocks LOS? | Audio | Duration Budget |
|---|---|---|---|---|
| **Construction Wall** | Plywood + mesh barrier with posted permits | Full | Drill/hammer ambient | Persistent (can hold seam for entire session) |
| **Police Tape / Barriers** | NYPD tape + sawhorses | Partial (see over) | Radio chatter | 5-30 minutes sim time |
| **Portal Shimmer** | Heat-distortion + color shift (anomaly-themed) | Full (distortion) | Tonal hum | 10-60 seconds (mission transition) |
| **Dense Crowd** | 50+ NPCs in tight formation (protest, event, tourist group) | Partial | Crowd noise | 2-10 minutes sim time |
| **Billboard Glare** | Overexposed bloom from nearby LED panel | Partial (directional) | Electronic hum | Situational (angle-dependent) |

#### Seam Budget

The Times Square slice may contain a **maximum of 10 active streaming seams** at any time. Each seam must satisfy the following requirements:

1. **At least one diegetic mask** must be active at the seam location.
2. The mask must be **plausible for the current world state** (no construction wall appearing/disappearing while player watches).
3. Seams within the **near band (0-30m)** require **two independent masks** (e.g., construction wall + crowd).
4. Seam activation/deactivation must take at least **3 seconds** of masked time.
5. The player must never see raw LOD transitions, texture pop-in, or geometry snapping at a seam boundary.

---

## 3. Trust Ledger v0 Scope and Schema

The Trust Ledger is the game's persistent memory. It records what happened, what was observed, and what the world's authorities believe. It is the single source of truth for narrative consequences, NPC knowledge, and world persistence.

### 3.1 Design Philosophy

The ledger answers three questions:
1. **What actually happened?** (Ground truth events, recorded by the Truth Engine.)
2. **What was observed?** (Sensor events -- cameras, witnesses, devices -- with confidence and precision metadata.)
3. **What does the world believe?** (Fused observations, authority responses, and their consequences.)

The player does not interact with the ledger directly. The ledger manifests through world consequences: a broken door stays broken, a witnessed crime triggers pursuit, an anomaly leaves evidence.

### 3.2 Event Categories

| Category | Code | Description | Retention | Examples |
|---|---|---|---|---|
| **Damage** | `DMG` | Physical alteration to world state | Permanent | Door forced, window broken, vehicle dented, wall cracked |
| **Access** | `ACC` | Entry/exit through controlled points | Permanent | Door opened (key/force/hack), gate passed, turnstile jumped |
| **Evidence** | `EVD` | Information artifacts created by events | Permanent | CCTV footage, fingerprints, witness memory, device log |
| **Anomaly** | `ANM` | Reality-bending events from Twin Earth bleed | Permanent | Spatial distortion, object duplication, temporal echo, physics violation |
| **Pursuit** | `PRS` | Active tracking/chase of an entity | Summarized after 24h sim-time | Police chase initiated, search radius declared, APB issued |
| **Authority Response** | `ATH` | Official action by world authorities | Permanent | Arrest, lockdown, investigation opened, alert level change |

### 3.3 Commit Points

Events are buffered until a **commit point** is reached. Uncommitted events exist in a speculative state and may be rolled back (e.g., if an anomaly rewinds time).

| Commit Trigger | Condition | Latency |
|---|---|---|
| **Authority Action** | Any authority entity (police, security, building system) takes an action based on the event | Immediate on action |
| **Observation Corroboration** | Two or more independent observation sources agree on an event within tolerance | Immediate on second corroboration |
| **Player Explicit Commit** | Player performs a "save" action or triggers a narrative checkpoint | Immediate on input |
| **Time Decay** | Event has existed uncommitted for >5 minutes sim-time without contradiction | Auto-commit at 5-minute mark |
| **Session Boundary** | Player exits session | All pending events committed with `SESSION_BOUNDARY` flag |

### 3.4 Storage Architecture

| Property | v0 Specification |
|---|---|
| **Engine** | SQLite 3.x (single-file, embedded, zero-config) |
| **File Location** | `<save_root>/ledger/trust_ledger_v0.db` |
| **Max Size** | 500 MB soft cap, 1 GB hard cap. Summarization triggers at soft cap. |
| **Portability** | Single file, platform-independent. Can be copied between machines for debugging. |
| **Queryability** | Full SQL query support. Debug UI provides a "ledger inspector" panel with pre-built queries. |
| **Backup** | WAL mode (Write-Ahead Logging) for crash recovery. Auto-backup every 30 minutes real-time. |
| **Thread Safety** | Single-writer, multiple-reader. Write queue is serviced by a dedicated ledger thread. |

#### Retention Policies

| Event Type | Retention | Summarization |
|---|---|---|
| Damage events | Permanent | Never summarized; always queryable at full fidelity |
| Evidence events | Permanent | Never summarized |
| Authority responses | Permanent | Never summarized |
| Anomaly events | Permanent | Never summarized |
| Pursuit events | Permanent header, details summarized after 24h sim-time | After 24h: pursuit reduced to `{start, end, result, zones_covered}` |
| Micro-observations (NPC glances, ambient CCTV with no event) | Decay after 1h sim-time | Deleted entirely unless flagged by a subsequent query |

### 3.5 Entity ID System

All ledger-referenceable entities receive a stable identifier:

**Format:** `ENT_<type>_<region>_<stablehash>`

| Component | Description | Examples |
|---|---|---|
| `ENT_` | Fixed prefix, identifies a ledger entity | -- |
| `<type>` | Entity class (4 chars max, uppercase) | `DOOR`, `VCLE` (vehicle), `NPC`, `CCTV`, `SIGN`, `ANOM`, `PROP`, `PLAY` |
| `<region>` | Geographic region code (3 chars) | `TSQ` (Times Square), `BWY` (Broadway), `7AV` (7th Avenue), `DUF` (Duffy Square) |
| `<stablehash>` | 4-character hex hash, stable across sessions | `a7f3`, `00b1`, `fe22` |

**Examples:**
- `ENT_DOOR_TSQ_a7f3` -- A specific door in the Times Square zone
- `ENT_CCTV_BWY_00b1` -- A CCTV camera on Broadway
- `ENT_NPC_DUF_fe22` -- An NPC in Father Duffy Square
- `ENT_VCLE_7AV_c4d8` -- A vehicle on 7th Avenue
- `ENT_ANOM_TSQ_1a2b` -- An anomaly event in Times Square

**Stability Rules:**
- Landmark entities (buildings, fixed cameras, faction HQs) have **permanent** IDs across all sessions and saves.
- Device entities (traffic lights, CCTV, access panels) have **session-stable** IDs that persist within a save file.
- NPC entities are **session-stable** for named/story NPCs and **ephemeral** for ambient crowd members (recycled after leaving the far band).
- Player assets and placed items are **permanent** from creation.

### 3.6 Observation Types and Confidence

| Source Type | Code | Spatial Precision | Temporal Precision | Confidence | Tamperability | Notes |
|---|---|---|---|---|---|---|
| **CCTV Camera** | `OBS_CCTV` | High (+/-0.5m) | High (+/-1 frame) | Moderate (0.7 base) | Low (hardened systems) | Fixed viewpoint, limited FOV. Confidence drops in poor lighting or weather. Can be disabled by the player. |
| **Witness (NPC)** | `OBS_WITN` | Low (+/-5m) | Low (+/-30s) | Variable (0.3-0.8) | High (memory is fallible) | Confidence scales with NPC alertness, distance to event, and stress level. Witnesses can be intimidated, bribed, or confused. |
| **Device Telemetry** | `OBS_DTEL` | High (+/-0.1m) | High (+/-1ms) | High (0.9 base) | Low (encrypted logs) | Access control systems, alarm sensors, pressure plates. Binary events (triggered / not triggered). |
| **Player Capture** | `OBS_PLAY` | Variable (depends on tool) | High (+/-1 frame) | High (0.85 base) | Moderate (data can be lost) | Player's own recordings, photos, notes. Stored as ledger entries with optional media attachment reference. |

#### Conflict Resolution and Fusion

When multiple observations describe the same event, the ledger fuses them:

1. **Agreement:** If two or more observations with combined confidence >= 0.9 agree (within spatial/temporal tolerance), the event is promoted to **CONFIRMED** status and auto-committed.
2. **Contradiction:** If observations disagree, the ledger stores all versions with a `DISPUTED` flag. The event is not auto-committed. Resolution requires either additional evidence or authority adjudication.
3. **Fusion formula:** Combined confidence = 1 - product(1 - confidence_i) for i in agreeing observations. Example: two witnesses at 0.5 confidence each yield combined confidence = 1 - (0.5 * 0.5) = 0.75. Add a CCTV at 0.7: combined = 1 - (0.5 * 0.5 * 0.3) = 0.925 (CONFIRMED).
4. **Tampering:** If a player tampers with an observation source (e.g., destroys a CCTV, intimidates a witness), the observation's confidence is reduced to 0.0 but remains in the ledger with a `TAMPERED` flag. Authority systems may notice the tampering itself as a separate event.

### 3.7 Core Schema (SQLite DDL)

```sql
-- Trust Ledger v0 Core Schema

CREATE TABLE events (
    event_id        TEXT PRIMARY KEY,       -- UUID v4
    category        TEXT NOT NULL,          -- DMG, ACC, EVD, ANM, PRS, ATH
    timestamp_sim   REAL NOT NULL,          -- Sim-time seconds since epoch
    timestamp_wall  TEXT NOT NULL,          -- ISO 8601 wall-clock time
    entity_id       TEXT NOT NULL,          -- ENT_<type>_<region>_<hash>
    position_x      REAL NOT NULL,          -- ENU meters from origin
    position_y      REAL NOT NULL,
    position_z      REAL NOT NULL,
    description     TEXT NOT NULL,          -- Human-readable event description
    severity        INTEGER DEFAULT 1,      -- 1 (minor) to 5 (critical)
    committed       INTEGER DEFAULT 0,      -- 0 = speculative, 1 = committed
    commit_trigger  TEXT,                   -- AUTHORITY, CORROBORATION, PLAYER, DECAY, SESSION
    superseded_by   TEXT,                   -- event_id of superseding event, if any
    FOREIGN KEY (entity_id) REFERENCES entities(entity_id)
);

CREATE TABLE observations (
    obs_id          TEXT PRIMARY KEY,       -- UUID v4
    event_id        TEXT NOT NULL,          -- Links to events table
    source_type     TEXT NOT NULL,          -- OBS_CCTV, OBS_WITN, OBS_DTEL, OBS_PLAY
    source_entity   TEXT NOT NULL,          -- Entity ID of the observer
    timestamp_sim   REAL NOT NULL,
    precision_m     REAL NOT NULL,          -- Spatial precision in meters
    confidence      REAL NOT NULL,          -- 0.0 to 1.0
    tampered        INTEGER DEFAULT 0,     -- 0 = intact, 1 = tampered
    raw_data        BLOB,                  -- Optional: image hash, audio clip ref, etc.
    notes           TEXT,                   -- Optional: human-readable context
    FOREIGN KEY (event_id) REFERENCES events(event_id),
    FOREIGN KEY (source_entity) REFERENCES entities(entity_id)
);

CREATE TABLE entities (
    entity_id       TEXT PRIMARY KEY,       -- ENT_<type>_<region>_<hash>
    entity_type     TEXT NOT NULL,          -- DOOR, VCLE, NPC, CCTV, SIGN, ANOM, PROP, PLAY
    region          TEXT NOT NULL,          -- TSQ, BWY, 7AV, DUF
    display_name    TEXT,                   -- Human-readable name (nullable for generic entities)
    persistent      INTEGER DEFAULT 0,     -- 1 = survives session boundaries
    created_sim     REAL NOT NULL,          -- Sim-time of entity creation
    last_updated    REAL NOT NULL,          -- Sim-time of last state change
    state_json      TEXT NOT NULL           -- JSON blob of current entity state
);

CREATE TABLE authority_state (
    authority_id    TEXT PRIMARY KEY,       -- e.g., NYPD_PRECINCT_TSQ, BLDG_SEC_MARRIOTT
    alert_level     INTEGER DEFAULT 0,     -- 0 (calm) to 5 (lockdown)
    active_pursuits INTEGER DEFAULT 0,
    last_updated    REAL NOT NULL,
    state_json      TEXT NOT NULL           -- JSON blob of authority-specific state
);

CREATE TABLE fusion_log (
    fusion_id       TEXT PRIMARY KEY,       -- UUID v4
    event_id        TEXT NOT NULL,
    obs_ids         TEXT NOT NULL,          -- JSON array of observation IDs used in fusion
    combined_conf   REAL NOT NULL,          -- Fused confidence value
    status          TEXT NOT NULL,          -- CONFIRMED, DISPUTED, PENDING
    timestamp_sim   REAL NOT NULL,
    FOREIGN KEY (event_id) REFERENCES events(event_id)
);

-- Indexes for common queries
CREATE INDEX idx_events_entity ON events(entity_id);
CREATE INDEX idx_events_category ON events(category);
CREATE INDEX idx_events_time ON events(timestamp_sim);
CREATE INDEX idx_events_committed ON events(committed);
CREATE INDEX idx_obs_event ON observations(event_id);
CREATE INDEX idx_obs_source ON observations(source_entity);
CREATE INDEX idx_entities_type ON entities(entity_type);
CREATE INDEX idx_entities_region ON entities(region);
```

---

## Appendix A: Glossary

| Term | Definition |
|---|---|
| **Truth Engine** | The authoritative simulation layer that maintains world state, physics, and NPC cognition |
| **Illusion Engine / Show Director** | The presentation layer that manages LOD, streaming, atmosphere, and perceptual fidelity |
| **Trust Ledger** | The persistent event database that records observations, evidence, and consequences |
| **Hero Tier** | Highest fidelity physics/rendering tier, applied to entities near the player |
| **Diegetic Mask** | An in-world element used to conceal streaming boundaries or LOD transitions |
| **Floating Origin** | Technique where the world-space origin moves with the camera to maintain floating-point precision |
| **ENU** | East-North-Up local tangent plane coordinate system |
| **Commit Point** | The moment a speculative ledger event becomes permanent |
| **Observation Fusion** | Process of combining multiple observations to determine event confidence |

## Appendix B: Open Questions for v1

1. **Audio sensor model:** Deferred to v1.1. What fidelity does the audio proxy need to support NPC behaviors like "heard gunshot from the east"?
2. **Subway level:** Backstage stubs exist at 6 entrances. When do we commit to a full underground layer?
3. **Building interiors:** How many hero interiors does the slice need? Current plan is 2-3. Playtesting will determine.
4. **Anomaly physics:** How does the anomaly bleed zone interact with PhysX? Current plan: overlay force fields. May need custom solver.
5. **Multi-player considerations:** The ledger is single-writer. If co-op is added, we need a merge strategy for concurrent observations.

---

*End of Architecture Specification v0*
