# City Ontology Spec v0 — Entity Hierarchy, Types, Fields, and Conserved Flows

> **Series:** Twin Earth NYC — Part 6: City-as-Living-System
> **Document:** `ontology-spec-v0.md`
> **Status:** Draft v0
> **Last Updated:** 2026-01-27
> **Depends On:** Part 2 (Ledger & Evidence), Part 4 (Earth Reality Layer), Part 5 (Alpha-Evolve)

---

## 1. Governing Principle

> **"The city is not a backdrop. It is a hierarchy of living containers, each with state, each with agency, each coupled to its neighbors through fields and flows."**

Twin Earth NYC models New York City as a nested ontology of spatial containers and discrete entities, bound together by continuous fields and conserved flows. Every object in the simulation exists at a precise level in this hierarchy. Every field propagates through the hierarchy according to explicit coupling rules. Nothing is decoration; everything participates.

This document defines three things:

1. **The Entity Hierarchy** — the nesting structure from City down to Component.
2. **The Entity Type Table** — the classification of every discrete object.
3. **The Field Systems** — the continuous spatial quantities overlaid on the hierarchy.
4. **The Conserved Flows** — the quantities that must balance across the simulation boundary.

---

## 2. Entity Hierarchy

The hierarchy is strict: every runtime object exists at exactly one level, and every level is spatially contained within its parent. There is no cross-parenting. An entity belongs to one Patch, which belongs to one Block, which belongs to one District, which belongs to the City.

```
City (singleton)
 +-- District (neighborhood-scale, e.g., Times Square, Hell's Kitchen)
      +-- Block (city block, bounded by streets)
           +-- Patch (sub-block area, ~10 m x 10 m)
                +-- Entity (discrete object: NPC, vehicle, prop, artifact)
                     +-- Component (ECS property: position, health, inventory, sensor, memory)
```

### 2.1 Level Definitions

| Level | Spatial Scope | Typical Count (Times Square Slice) | State Responsibility |
|-------|--------------|-------------------------------------|----------------------|
| **City** | Entire simulation bounds | 1 | Global weather state, time-of-day, economy index, global event flags |
| **District** | ~10 contiguous blocks (~250 m radius) | 3--5 | Aggregate faction presence, district-level Heat channels, crowd mood index, ambient sound profile |
| **Block** | 1 city block (~80 m x 120 m) | 20--40 | Local pedestrian density, traffic segment state (flow / congested / blocked), building occupancy states, streetlight schedule |
| **Patch** | ~10 m x 10 m sub-block area | 800--1600 per block | Micro-surface state: wetness (0--1), grime accumulation (0--1), physical damage marks, anomaly residue stain (type + intensity) |
| **Entity** | Individual object (bounding volume) | 500--5000 active in slice | Position, velocity, behavior state, sensor readings, inventory, health, identity (ledger ID) |
| **Component** | Property of an entity (no spatial extent) | 5--20 per entity | Pure data: `Transform`, `Health`, `Inventory`, `SensorArray`, `MemoryLog`, `FactionAffinity`, `BehaviorTree` |

### 2.2 Containment Rules

1. **Spatial assignment is automatic.** An entity's containing Patch, Block, and District are computed from its world-space position. When an entity moves, it re-registers with the new container.
2. **Events propagate upward.** An event at the Entity level (e.g., glass break) is recorded on the Patch, aggregated at the Block, and escalated to the District only if thresholds are crossed. See `hierarchy-coupling-rules-v0.md` for escalation rules.
3. **Policy propagates downward.** A District-level faction order (e.g., "increase patrols") flows down to Blocks (patrol routes), then to Patches (surveillance coverage), and finally to Entities (authority NPC behavior parameters).
4. **No skip-level coupling.** A City-level state change (e.g., blackout) must cascade through District, then Block, then Patch, then Entity. Direct City-to-Entity coupling is forbidden to preserve hierarchical coherence and computational locality.

---

## 3. Entity Types

Every discrete simulation object is classified into exactly one of the following types. Type determines update priority, persistence model, default components, and interaction vocabulary.

| Type | Examples | Scale | Update Rate | Persistence Model | Default Components |
|------|----------|-------|-------------|-------------------|--------------------|
| **Agent** | Pedestrian NPC, vehicle-driving NPC, authority NPC (police, DoT), hero NPC (faction leaders) | Individual | 10--60 Hz (LOD-dependent) | Session (spawned/despawned at slice boundaries; behavior state saved on exit) | `Transform`, `Locomotion`, `BehaviorTree`, `SensorArray`, `MemoryLog`, `Health`, `Inventory`, `FactionAffinity`, `AppearanceState` |
| **Artifact** | CCTV camera, Wi-Fi signal emitter, info kiosk, door (interactive), public phone, parking meter | Individual | Event-driven (updates on interaction, power change, or scheduled tick) | Permanent (survives sessions; state stored in ledger) | `Transform`, `DeviceState`, `PowerDraw`, `SensorArray`, `NetworkLink`, `InteractionPrompt` |
| **Prop** | Bollard, bench, trash can, fire hydrant, traffic cone, newspaper box, mailbox | Individual | Rarely (updates only on damage, weather response, or physics impulse) | Permanent (position + damage state persists across sessions; replaceable via city-services event) | `Transform`, `MaterialID`, `DamageState`, `PhysicsBody` (static or kinematic) |
| **Vehicle** | Taxi, city bus, police cruiser, delivery truck, ambulance, bicycle, motorcycle | Individual | 30 Hz (physics-driven) | Session (active vehicles despawn at boundaries; parked vehicles persist as props until claimed) | `Transform`, `VehiclePhysics`, `Locomotion`, `OccupantSlots`, `LightState`, `SirenState`, `DamageState`, `LicensePlate` |
| **Field** | Wind, noise, light, wetness, crowd density, Heat (4-channel) | Spatial grid overlay | 1--10 Hz (per field; see Section 4) | Derived (no direct persistence; recomputed each frame from source state; snapshot on session save for fast reload) | N/A (fields are not entities; they are grid systems read by entities) |
| **Patch** | Puddle, grime layer, scorch mark, bullet impact, anomaly residue stain | Sub-block area (~10 m^2) | 0.1 Hz (slow decay tick) | Persistent (state decays over real time; permanent marks possible for narrative anchors) | `PatchTransform`, `SurfaceState`, `DecayTimer`, `VisualOverlay`, `AnomalySignature` |

### 3.1 Agent Sub-Types

Agents are the most complex entity type. They are further sub-classified for behavior and priority purposes:

| Sub-Type | Behavior Model | LOD Tiers | Authority Level | Spawning Rule |
|----------|---------------|-----------|-----------------|---------------|
| **Pedestrian** | Routine-driven (commute, shop, loiter, react) | Full (near camera) / Simplified (mid) / Aggregate (far) | None | Density targets per block; spawned at subway exits, building doors, slice boundaries |
| **Authority** | Patrol + dispatch + escalation protocol | Full always (never simplified) | Institutional Heat writer | Dispatched by District Manager on incident escalation; baseline patrols from schedule |
| **Vehicle NPC** | Traffic-flow AI; lane-following + signal-obeying + obstacle avoidance | Full (on-screen) / Rail (off-screen, simplified path) | None (emergency vehicles = Authority sub-type) | Traffic flow targets per road segment; spawned at slice boundaries |
| **Hero** | Scripted + reactive hybrid; narrative-linked behavior tree | Full always; cinematic camera priority | Faction-dependent | Pre-placed or event-triggered; never randomly spawned |
| **Vendor** | Stationary + interaction-radius behavior; serves customers | Full (near) / Idle animation (far) | Social Heat writer (micro) | Placed by District schedule; some persistent, some session-only |

### 3.2 Entity Lifecycle

```
[Spawn Request]
    |
    v
[Entity Pool] --allocate--> [Init Components] --register--> [Patch / Block / District]
    |                                                              |
    v                                                              v
[Active Tick Loop]  <---field-reads/writes--->  [Field Systems]
    |
    | (on exit condition: boundary cross, despawn event, destruction)
    v
[Deregister from Hierarchy] --> [Serialize if persistent] --> [Return to Pool]
```

**Pool sizes (Times Square Slice budget):**

| Pool | Max Active | Reserve | Notes |
|------|-----------|---------|-------|
| Pedestrian Agents | 2000 | 500 | Density-driven spawn/despawn |
| Authority Agents | 50 | 20 | Dispatch-driven |
| Vehicles | 200 | 50 | Traffic-flow-driven |
| Props | 3000 | 0 | All pre-placed; no runtime spawning (damage only) |
| Artifacts | 500 | 0 | All pre-placed; no runtime spawning |
| Hero Agents | 10 | 5 | Event-driven |

---

## 4. Field Systems Overview

Fields are continuous spatial quantities overlaid on the simulation grid. They are not entities; they do not have identities, inventories, or behavior trees. They are data layers that entities read and write.

Each field is defined by its grid resolution, update frequency, source terms, and coupling rules. Full specifications are in `field-systems-spec-v0.md`. The summary below establishes the ontological role of each field.

| Field | Data Type | Grid Resolution | Update Frequency | Primary Drivers | Primary Consumers |
|-------|-----------|----------------|-------------------|------------------|-------------------|
| **Wind** | 3D vector (m/s) | 5 m | 2 Hz | Building geometry, weather state, HVAC vents, subway grates | Paper/cloth props, NPC hair/clothing animation, rain angle, sound propagation direction |
| **Noise** | Scalar (dB equivalent, 0--120) | 2 m | 5 Hz | Traffic, crowd chatter, construction, events (explosions, sirens), music | NPC communication range, witness accuracy, stress levels, CCTV audio channel quality |
| **Light** | RGB + intensity (4-channel) | 1 m (near camera) / 5 m (far) | 10 Hz (near) / 2 Hz (far) | Sun position, billboards, streetlights, vehicle headlights, anomaly glow, emergency flashers | CCTV image quality, NPC visibility detection, mood system, forced-perspective rendering, shadow casting |
| **Wetness** | Scalar (0.0--1.0) | 1 m | 1 Hz | Rain rate, drainage topology, shade factor, sprinkler events | Surface traction, reflection intensity, CCTV confidence penalty, NPC routing preference (avoid puddles), material darkening |
| **Crowd Density** | Scalar (persons / m^2) | 2 m | 5 Hz | NPC positions (aggregated via spatial hash) | Movement speed cap, CCTV occlusion factor, witness count estimation, noise field contribution, pickpocket opportunity |
| **Heat** | 4-channel vector (physical, social, institutional, ecological) | Per-block (80 m) | 0.1 Hz | Events (crime, anomaly, protest, accident, construction) | Authority dispatch urgency, crowd behavior modifiers, portal stability, faction strategic decisions, media coverage probability |

### 4.1 Field-Entity Interaction Model

Entities interact with fields through two operations:

- **Read:** Entity samples field value at its current position. Cost: O(1) grid lookup. Example: NPC reads noise field to determine if it can hear a conversation.
- **Write (contribute):** Entity adds to field source term at its position. Cost: O(1) grid write, propagated on next field tick. Example: Vehicle engine adds to noise field; NPC body adds to crowd density field.

Fields never interact with entities directly. An entity's systems (behavior, physics, animation) read field values and make decisions. This preserves the O(cells) update cost and prevents O(N^2) entity-entity coupling through fields.

---

## 5. Conserved Flows

Three quantities are tracked as conserved flows across the simulation boundary. Conservation does not mean these quantities are physically simulated with differential equations; it means the simulation enforces balance constraints to prevent drift, leaks, and implausible accumulation.

### 5.1 Matter (Entity Mass Balance)

| Flow | Inflow Sources | Outflow Sinks | Conservation Rule |
|------|---------------|---------------|-------------------|
| **Vehicles** | Spawn at road entry points (slice boundary intersections) | Despawn at road exit points | Net vehicle count bounded to traffic-flow target +/- 10%; inflow rate = outflow rate averaged over 30 s window |
| **Pedestrian NPCs** | Spawn at subway exits, building doors, slice boundary sidewalks | Despawn at same locations (reversed) | Total pedestrian count per block bounded by density target; spawn rate adjusts dynamically to maintain target |
| **Props** | Placed by city-services event (e.g., new traffic cone) or player action | Destroyed by damage event or city-services cleanup | Total prop count bounded by block budget; destroyed props leave Patch damage marks |
| **Artifacts** | Installed by narrative event or pre-placed | Removed by narrative event only (never random) | Artifact count is fixed per session unless narrative modifies it; all changes ledger-logged |

**Boundary protocol:** The slice has defined entry/exit portals (road endpoints, subway tunnels, building interiors). Each portal has a target flow rate calibrated to real-world pedestrian and traffic data. Spawn/despawn managers at each portal enforce flow balance. If a portal is blocked (e.g., traffic jam), backpressure reduces inflow at adjacent portals to prevent entity count overflow.

### 5.2 Energy (Power Grid)

The simulation models a simplified power grid for the Times Square slice. This is not a full electrical simulation; it is a resource-budget system that enables blackout events and cascading device failures.

| Component | Power Role | Nominal Draw | Failure Behavior |
|-----------|-----------|-------------|------------------|
| **Billboard** | Consumer | 50 kW per billboard (scaled for visual prominence) | Screen off; light field drops; noise field drops (no speaker); anomaly concealment possible |
| **Streetlight** | Consumer | 0.5 kW per light | Dark patch; CCTV quality drops; NPC anxiety increases |
| **CCTV Camera** | Consumer | 0.1 kW per camera | Camera offline; evidence gap; institutional Heat blind spot |
| **Signal Kiosk** | Consumer | 1 kW per kiosk | No Wi-Fi; NPC phone behavior changes; information flow interrupted |
| **Traffic Signal** | Consumer | 0.3 kW per intersection | Intersection goes to flashing-red protocol; traffic AI switches to yield mode |
| **Grid Feed** | Supplier | Total slice budget: 5 MW | Blackout event: all consumers lose power simultaneously; field cascade triggers |

**Conservation rule:** Total consumption must not exceed supply. If supply drops (blackout event, partial outage), consumers are shed in priority order: billboards first, then kiosks, then streetlights, then traffic signals, then CCTV (last to lose power, first to restore). This priority order is tunable per district.

**Blackout cascade sequence:**

```
[Grid Feed drops to 0]
  --> [All billboard light sources OFF]     (Light field: intensity drops 60% in Times Square)
  --> [All kiosks OFF]                       (Information flow: severed)
  --> [Streetlights OFF after 3s UPS]        (Light field: drops to moonlight + vehicle headlights only)
  --> [Traffic signals OFF after 5s UPS]     (Traffic AI: yield mode; congestion spike)
  --> [CCTV OFF after 10s UPS]               (Surveillance: blind; institutional Heat = 0 contribution)
  --> [Emergency generators kick in at 30s]  (Partial restore: CCTV + traffic signals only)
```

### 5.3 Information (Evidence Flow)

Information is the most strictly conserved quantity. Once created, evidence cannot be destroyed -- only classified, suppressed, or contested.

| Flow Stage | Source | Sink | Conservation Rule |
|------------|--------|------|-------------------|
| **Generation** | Sensor event (CCTV frame, NPC witness observation, artifact log) | Event Bus | Every sensor reading generates exactly one evidence packet; no silent drops |
| **Transport** | Event Bus | Ledger Ingest Queue | Evidence packets are queued with guaranteed delivery; network partition = queue grows, never drops |
| **Commitment** | Ledger Ingest Queue | Immutable Ledger | Once committed, entry is permanent; no delete, no overwrite; only append of classification/contestation records |
| **Classification** | Ledger Entry | Faction Intelligence Layer | Factions may classify evidence (restrict access) but cannot erase it; classification is itself a ledger entry |
| **Suppression** | Faction Action | Public Evidence View | Suppression hides evidence from public queries but does not remove it from the ledger; suppression events are logged |

**Conservation invariant:** `count(evidence_generated) == count(evidence_committed)` over any sufficiently long window. Short-term: queue depth may grow during network partition. Long-term: all evidence reaches the ledger.

**Violation detection:** If `evidence_committed < evidence_generated - queue_depth`, a conservation violation has occurred. The system triggers a diagnostic alert and halts evidence-dependent faction decisions until the discrepancy is resolved.

---

## 6. Cross-Cutting Ontological Rules

### 6.1 Identity

Every entity that can participate in a ledger event must have a globally unique, immutable **Entity ID** assigned by the Ledger Service at spawn time. Entity IDs are never reused. Destroyed entities retain their ID in the ledger; the ID is marked as `retired`.

### 6.2 Determinism

Given identical initial state and identical input sequences, the simulation must produce identical entity states and field values at every tick. This requires:

- Fixed-point or deterministic floating-point arithmetic for field updates.
- Deterministic iteration order over entity containers (sorted by Entity ID, not memory address).
- Seeded RNG per entity, advanced only by entity-local events.

### 6.3 Serializability

The complete simulation state at any tick must be serializable to a snapshot file. The snapshot contains:

- City-level global state (weather, time, economy).
- Per-district aggregate state.
- Per-block state.
- Per-patch state (wetness, grime, damage, anomaly residue).
- Per-entity component data (only persistent entities; session entities are re-derived from flow targets on reload).
- Field snapshots (for fast reload; fields are technically derivable but expensive to recompute).

### 6.4 Budget Ceilings

| Resource | Hard Ceiling | Rationale |
|----------|-------------|-----------|
| Total active entities | 8,000 | GPU instancing budget + ECS tick budget at 60 Hz |
| Total field cells (all fields combined) | 2,000,000 | Memory budget: ~64 MB at 32 bytes/cell average |
| Total patches (active slice) | 50,000 | Persistent storage budget + decay-tick budget |
| Ledger entries per minute | 10,000 | Database write throughput + replication lag |
| Event bus messages per second | 50,000 | Network throughput + deserialization budget |

---

*End of document. For field-level detail, see `field-systems-spec-v0.md`. For hierarchy coupling rules, see `hierarchy-coupling-rules-v0.md`. For material properties and consequence chains, see `materials-consequences-spec-v0.md`.*
