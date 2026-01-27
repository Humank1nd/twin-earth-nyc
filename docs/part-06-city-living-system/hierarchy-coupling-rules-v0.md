# Hierarchy and Coupling Rules v0 — Multi-Resolution Simulation, Aggregation, and Event Escalation

> **Series:** Twin Earth NYC — Part 6: City-as-Living-System
> **Document:** `hierarchy-coupling-rules-v0.md`
> **Status:** Draft v0
> **Last Updated:** 2026-01-27
> **Depends On:** `ontology-spec-v0.md` (entity hierarchy), `field-systems-spec-v0.md` (field update pipeline)

---

## 1. Governing Principle

> **"Information flows upward through aggregation. Policy flows downward through influence. Events escalate only when thresholds are crossed. No level reaches past its immediate neighbor."**

The Twin Earth NYC simulation is a strict five-level hierarchy: City, District, Block, Patch, Entity. Each level operates at its own temporal resolution, manages its own state, and communicates with adjacent levels through well-defined aggregation (upward) and influence (downward) channels. Skip-level communication is forbidden. This document defines the rules governing all inter-level data flow.

---

## 2. Multi-Resolution Hierarchy

| Level | Scope | Spatial Extent | Update Rate | State Examples | Responsible System |
|-------|-------|---------------|-------------|----------------|-------------------|
| **City** | Entire simulation | Full slice (~600 m x 300 m) | 0.01 Hz (every 100 s) | Global weather state (rain, wind, temperature, cloud cover), economy index (0.0--1.0), time-of-day (24h clock), global event flags (blackout, emergency, holiday) | Weather Engine, Economy Sim, Time Manager |
| **District** | ~10 contiguous blocks | ~250 m radius | 0.1 Hz (every 10 s) | Faction dominance scores (per faction, 0.0--1.0), aggregate Heat (4-channel average across blocks), crowd mood index (-1.0 hostile to +1.0 festive), ambient sound profile (base noise level + dominant sound type), district alert level (green / yellow / red) | District Manager |
| **Block** | 1 city block | ~80 m x 120 m | 1 Hz | Local pedestrian density (persons/block), traffic segment state (`flowing` / `congested` / `blocked` / `closed`), building occupancy states (per building: `open` / `closed` / `evacuated`), streetlight schedule state (`on` / `off` / `emergency`), incident count (rolling 300 s window) | Block Sim |
| **Patch** | Sub-block area | ~10 m x 10 m | 0.1--1 Hz | Wetness (0.0--1.0), grime accumulation (0.0--1.0), physical damage marks (type + severity list), anomaly residue stain (signature + intensity + decay timer), surface material ID | Patch System |
| **Entity** | Individual object | Bounding volume | 10--60 Hz | Position, velocity, orientation, health, behavior state, sensor readings, inventory contents, memory log entries, active interaction target | Entity System (ECS) |

---

## 3. Upward Aggregation Rules

Aggregation flows from fine-grained levels to coarse-grained levels. Each aggregation step reduces data volume and increases temporal smoothing. Aggregation is computed at the **receiver's** update rate (i.e., Block aggregates Patch data at 1 Hz, not at Patch's 0.1 Hz rate).

### 3.1 Entity to Patch

| Aggregated Quantity | Source | Aggregation Method | Notes |
|---------------------|--------|-------------------|-------|
| **Crowd density contribution** | NPC positions within Patch bounds | Count NPCs, divide by Patch area (100 m^2) | Feeds into crowd density field; recomputed every density field tick (5 Hz) |
| **Damage event marks** | Entity damage events (impact, explosion, bullet) | Record damage type + position + timestamp on Patch | Persistent until decay timer expires or cleanup event |
| **Noise contribution** | Entity noise emissions (vehicle engine, horn, speech) | Summed into noise field cells overlapping Patch | Handled by noise field system, not Patch system directly |
| **Anomaly interaction** | Entity-anomaly contact events | Record anomaly signature + intensity on Patch as residue stain | Residue decays over 600 s; affects field readings in Patch area |

### 3.2 Patch to Block

| Aggregated Quantity | Source | Aggregation Method | Notes |
|---------------------|--------|-------------------|-------|
| **Average wetness** | Wetness field values in all Patches of Block | Arithmetic mean of Patch wetness values | Used for Block-level weather response decisions |
| **Damage count** | Damage marks across all Patches | Count of active (non-expired) damage marks | If damage count > 10, triggers Block-level "area damaged" flag |
| **Anomaly coverage** | Anomaly residue stains across Patches | Fraction of Patches with residue intensity > 0.1 | If coverage > 0.3, escalates to District as "anomaly contamination" event |
| **Surface condition index** | Weighted average of grime, wetness, damage | `condition = 0.4 x avg_grime + 0.3 x avg_wetness + 0.3 x (damage_count / max_damage)` | Feeds into city-services dispatch priority |

### 3.3 Block to District

| Aggregated Quantity | Source | Aggregation Method | Notes |
|---------------------|--------|-------------------|-------|
| **Aggregate crowd count** | Pedestrian density per Block | Sum of (density x block_area) across all Blocks in District | Used for District-level crowd management decisions |
| **Incident rate** | Incident count per Block (rolling 300 s window) | Sum across all Blocks; normalized per hour | If rate > 5 incidents/hour, District alert level escalates |
| **Heat channels** | Per-Block Heat (4-channel) | Weighted average across Blocks (weight = Block population) | District-level Heat drives faction strategic decisions |
| **Traffic state summary** | Per-Block traffic segment state | Count of `congested` + `blocked` segments / total segments | If > 0.5 congested, District triggers traffic rerouting event |
| **Power status** | Per-Block power state | Count of powered vs. unpowered blocks | If > 0.3 unpowered, District triggers emergency power protocol |

### 3.4 District to City

| Aggregated Quantity | Source | Aggregation Method | Notes |
|---------------------|--------|-------------------|-------|
| **Overall population** | Aggregate crowd count per District | Sum across all Districts | Feeds into economy index (more people = more economic activity) |
| **Total Heat** | Per-District Heat (4-channel) | Max across Districts (not average — city responds to hottest spot) | Drives City-level event triggers (e.g., citywide alert if any District Physical Heat > 0.9) |
| **Economy indicators** | District commerce activity, vendor sales, transit throughput | Weighted sum normalized to 0.0--1.0 index | Feeds back as City-level economy state |
| **Anomaly status** | District-level anomaly contamination reports | Boolean: any District reporting active anomaly? + total anomaly intensity | Drives City-level anomaly response protocol (portal defense, reality anchoring) |

---

## 4. Downward Influence Rules

Influence flows from coarse-grained levels to fine-grained levels. Influence sets parameters, targets, and policies that constrain lower-level behavior. Influence is applied at the **sender's** update rate.

### 4.1 City to District

| Influence | Source State | Effect on District | Application Rule |
|-----------|-------------|-------------------|-----------------|
| **Weather** | City weather state (rain, wind, temperature, cloud cover) | All Districts receive identical weather; affects field source terms (rain -> wetness, wind -> wind field) | Applied uniformly every City tick (100 s); Districts do not modify weather |
| **Time-of-day** | City 24h clock | Districts adjust: streetlight schedules, vendor open/close, NPC routine phases, ambient sound profiles | Applied every City tick; Districts translate time into local schedule events |
| **Economy index** | City economy state (0.0--1.0) | Districts adjust: vendor prices, NPC spending behavior, pedestrian density targets (higher economy = more foot traffic) | Applied every City tick; linear scaling of District targets |
| **Global event flags** | City-level events (blackout, holiday, emergency) | Districts enter corresponding mode: blackout → power cascade, holiday → crowd boost + vendor activity, emergency → authority surge | Applied immediately on flag change (event-driven, not tick-driven) |

### 4.2 District to Block

| Influence | Source State | Effect on Block | Application Rule |
|-----------|-------------|----------------|-----------------|
| **Faction policy** | Faction dominance scores | Dominant faction sets Block-level rules: patrol routes (authority), vendor placement (commercial), protest zones (activist), surveillance density (institutional) | Recomputed every District tick (10 s); Blocks receive updated parameter sets |
| **District Heat** | Aggregate Heat channels | Blocks adjust: NPC spawn rate modifiers (high Physical Heat → fewer spawns; high Social Heat → more spawns near source), authority dispatch priority (high Institutional Heat → more patrols) | Applied every District tick; Block reads Heat and modifies its spawn/patrol parameters |
| **Alert level** | District alert level (green / yellow / red) | Blocks respond: green → normal operations; yellow → increased authority presence, reduced vendor activity; red → evacuation protocol, locked buildings, maximum authority | Applied on alert level change (event-driven) |
| **Traffic rerouting** | District traffic state summary | Blocks with `congested` segments receive rerouting directives: redirect vehicles to alternate segments, adjust signal timing | Applied every District tick when congestion > 0.3 |

### 4.3 Block to Patch

| Influence | Source State | Effect on Patch | Application Rule |
|-----------|-------------|-----------------|-----------------|
| **Construction status** | Block construction events (active / inactive) | Affected Patches marked as `impassable`: NPCs and vehicles route around; fields (noise, light) modified in affected area | Applied on construction event start/end |
| **Lighting schedule** | Block streetlight state (on / off / emergency) | Patches under streetlights have light field contribution toggled; emergency mode = flashing | Applied every Block tick (1 Hz) or on schedule change |
| **Building state** | Building occupancy state (open / closed / evacuated) | Patches adjacent to building entrances: `open` → NPC spawn point active; `closed` → NPC spawn point inactive; `evacuated` → NPC flee target | Applied on building state change |
| **Cleanup dispatch** | Block surface condition index exceeds threshold | Target Patches scheduled for cleanup: grime reduced, damage marks cleared over 60 s | Applied when condition index > 0.7; cleanup NPC dispatched |

### 4.4 Patch to Entity

| Influence | Source State | Effect on Entity | Application Rule |
|-----------|-------------|-----------------|-----------------|
| **Wetness** | Patch wetness value | Entity traction modifier; vehicle braking distance; NPC slip probability; visual wetness on entity feet/tires | Entity reads Patch wetness every movement tick |
| **Damage marks** | Patch damage list | NPC routing avoidance (NPCs prefer undamaged Patches); visual context for NPC reactions (glance at damage) | Entity reads Patch damage state on routing decision tick |
| **Anomaly residue** | Patch anomaly stain | Entity anomaly exposure accumulation; visual distortion effects; behavior tree modifier (caution / fascination / fear depending on NPC type) | Entity reads Patch anomaly state every behavior tick |
| **Surface material** | Patch material ID | Entity footstep sound selection; vehicle tire sound selection; fall damage modifier | Entity reads Patch material on movement tick |
| **Grime level** | Patch grime value (0.0--1.0) | Visual dirtying of entity lower body over time; NPC mood modifier (high grime → slight mood decrease) | Entity reads Patch grime on visual update tick |

---

## 5. Event Escalation Rules

Events originate at the Entity or Patch level and propagate upward through the hierarchy. Escalation is threshold-gated: an event only moves to the next level if the receiving level's threshold is exceeded. This prevents trivial events from consuming higher-level processing budgets.

### 5.1 Escalation Levels

```
Level 0 (Entity)
    |
    | automatic (all entity events recorded on containing Patch)
    v
Level 1 (Patch)
    |
    | threshold gate: Patch damage count > 3 OR anomaly intensity > 0.2
    v
Level 2 (Block)
    |
    | threshold gate: Block incident count > 5 (in 300 s) OR traffic state = blocked OR Heat channel > 0.3
    v
Level 3 (District)
    |
    | threshold gate: District Heat channel > 0.5 OR alert level = red OR anomaly contamination > 0.3
    v
Level 4 (City)
    |
    | (City always processes escalated District events)
    v
[Global Response]
```

### 5.2 Level 0: Entity Events (Handled Locally)

These events are processed entirely within the Entity System and recorded on the containing Patch. They do not escalate unless they contribute to a Patch-level threshold.

| Event | Trigger | Local Handling | Patch Recording |
|-------|---------|---------------|-----------------|
| NPC collision | Two NPCs occupy same cell | Physics impulse + stumble animation; no damage | None (too frequent to record) |
| Door forced open | Player or NPC forces locked door | Door state → `forced_open`; sound event; evidence generated | Damage mark at door position |
| Item dropped | Entity drops inventory item | Item entity spawned at position; enters entity pool | None |
| NPC verbal exchange | Two NPCs within communication range | Dialogue system trigger; memory log updated | None |
| Minor vehicle scrape | Vehicle contacts prop or vehicle at < 5 m/s | Damage state update on both objects; sound event | Damage mark at contact position |

### 5.3 Level 1: Patch Events (Propagate to Block)

These events represent significant local state changes that the Block needs to incorporate into its aggregate tracking.

| Event | Trigger | Patch Handling | Block Escalation Condition |
|-------|---------|---------------|--------------------------|
| Damage threshold exceeded | Patch damage count > 3 | Mark Patch as `heavily_damaged`; visual overlay intensifies | Always escalates: Block increments incident count |
| Anomaly detected | Anomaly residue intensity > 0.2 on Patch | Begin anomaly residue tracking; apply field perturbations | Always escalates: Block flags `anomaly_present` |
| Surface hazard | Wetness > 0.9 AND material friction < 0.3 | Mark as slip hazard; NPC routing avoidance | Escalates if > 5 adjacent Patches are hazardous |
| Fire ignition | Fire event on Patch | Begin fire spread simulation; light + Heat source | Always escalates: Block increments incident count and flags `fire_active` |

### 5.4 Level 2: Block Events (Propagate to District)

These events represent block-scale disruptions that require District-level coordination.

| Event | Trigger | Block Handling | District Escalation Condition |
|-------|---------|---------------|-------------------------------|
| Incident count threshold | > 5 incidents in rolling 300 s window | Block enters `elevated_alert` state; authority NPC patrol frequency doubles | Always escalates: District receives incident summary |
| Traffic gridlock | Traffic segment state = `blocked` for > 60 s | Block reroutes vehicles to adjacent segments; sound event (honking) | Escalates if > 2 segments blocked simultaneously |
| Authority dispatch request | Heat channel > 0.3 for any channel | Block requests authority NPC from District pool | Always escalates: District dispatch queue receives request |
| Building evacuation | Fire or structural damage in building | Block sets building state to `evacuated`; NPC flee behavior from building doors | Always escalates: District enters `yellow` alert if not already |
| Power failure | Block loses grid power | Blackout cascade within Block (see ontology-spec-v0.md Section 5.2) | Always escalates: District tracks powered block count |

### 5.5 Level 3: District Events (Propagate to City)

These events represent district-scale crises requiring global response.

| Event | Trigger | District Handling | City Escalation Condition |
|-------|---------|------------------|--------------------------|
| Heat threshold crossed | Any Heat channel > 0.5 (district aggregate) | District enters `yellow` alert; increases authority budget; notifies factions | Escalates if any channel > 0.8 (potential citywide crisis) |
| Faction response triggered | Faction dominance score shift > 0.2 in single tick | District recalculates faction policy; may trigger faction confrontation event | Escalates if confrontation involves > 2 factions |
| Mass casualty event | Physical Heat > 0.7 AND crowd count in affected blocks > 200 | District enters `red` alert; all blocks in district enter evacuation mode | Always escalates: City activates emergency protocol |
| Anomaly contamination | > 30% of blocks report anomaly presence | District flags `anomaly_crisis`; ecological Heat spike; portal defense protocol | Always escalates: City activates reality anchoring protocol |
| District-wide power failure | > 50% of blocks unpowered | District activates emergency power priorities; requests City-level generator dispatch | Always escalates: City evaluates grid-wide power state |

### 5.6 Level 4: City Events (Global Cascade Downward)

City-level events cascade downward to all Districts, then through the full hierarchy. These are rare, high-impact events.

| Event | Trigger | Cascade Path | Effect at Each Level |
|-------|---------|-------------|---------------------|
| **Blackout** | Grid supply drops to 0 (narrative event or cascading failure) | City → all Districts → all Blocks → all Patches (via light/power fields) → all Entities (device power state) | District: `red` alert. Block: blackout cascade sequence. Patch: light field drops. Entity: all powered devices off; NPC anxiety spikes. |
| **Weather change** | Weather Engine updates (scheduled or narrative-triggered) | City → all Districts (uniform) → all Blocks (field recalc) → all Patches (wetness/shade recalc) → Entities (clothing/behavior change) | District: ambient sound profile update. Block: lighting schedule adjustment. Patch: wetness source term change. Entity: umbrella/coat behavior; routing preference change. |
| **Citywide emergency** | Any District escalates Physical Heat > 0.9 | City → all Districts (`red` alert override) → all Blocks (evacuation protocol) → all Patches (emergency lighting) → Entities (flee behavior) | Full evacuation cascade; all non-authority NPCs route to nearest exit; vehicles yield to emergency vehicles. |
| **Economy shock** | Narrative event (market crash, holiday spending surge) | City → all Districts (economy modifier) → Blocks (vendor/traffic adjustment) → Entities (spending behavior, density targets) | Gradual cascade over 300 s; economy index shifts by up to 0.3; vendor prices adjust; crowd density targets adjust. |
| **Anomaly storm** | Multiple Districts report anomaly contamination simultaneously | City → all Districts (reality anchoring protocol) → all Blocks (anomaly defense posture) → Patches (field perturbation spike) → Entities (anomaly exposure acceleration) | All fields experience perturbation; portal stability drops globally; faction coordination events triggered. |

---

## 6. Cross-Level Timing and Synchronization

### 6.1 Tick Rate Hierarchy

```
Entity tick:    |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| (60 Hz)
Block tick:     |                                                            | (1 Hz)
Patch tick:     |         |         |         |         |         |          | (0.1-1 Hz)
District tick:  |                                                            | (0.1 Hz, every 10 s)
City tick:      |                                                                          | (0.01 Hz, every 100 s)
```

### 6.2 Synchronization Rules

1. **Upward aggregation** is computed at the receiver's tick rate. Block aggregates Patch data at 1 Hz. District aggregates Block data at 0.1 Hz. City aggregates District data at 0.01 Hz.
2. **Downward influence** is applied at the sender's tick rate. City influence reaches Districts every 100 s. District influence reaches Blocks every 10 s. Block influence reaches Patches every 1 s.
3. **Event escalation** is asynchronous. Events escalate immediately when thresholds are crossed, regardless of tick rates. Escalation bypasses the normal tick schedule using the event bus.
4. **No retroactive correction.** If a lower level changes state between higher-level ticks, the higher level sees the change at its next tick. There is no back-propagation of missed state.
5. **Deterministic ordering.** Within a tick at any level, processing order is fixed: aggregation first, then influence application, then local state update, then escalation check.

### 6.3 Latency Budget

| Path | Maximum Latency | Rationale |
|------|----------------|-----------|
| Entity event → Patch recording | 1 entity tick (16--100 ms) | Entity events are recorded on the same tick they occur |
| Patch escalation → Block processing | 1 block tick (1 s) | Block processes Patch escalations at next block tick |
| Block escalation → District processing | 1 district tick (10 s) | District processes Block escalations at next district tick |
| District escalation → City processing | 1 city tick (100 s) for normal; **immediate** for crisis (Physical Heat > 0.9) | Crisis events bypass City tick schedule |
| City cascade → Entity effect | 1 district tick + 1 block tick + 1 patch tick + 1 entity tick = ~11.1 s | Full downward cascade latency; acceptable for global events (weather, economy) |
| Emergency cascade (skip-tick) | ~2 s (event-bus driven, bypasses tick schedule) | Used only for Level 4 crisis events |

---

## 7. Invariants and Validation

The following invariants must hold at all times. Violation of any invariant triggers a diagnostic alert.

| # | Invariant | Validation Method | Frequency |
|---|-----------|------------------|-----------|
| 1 | Every Entity belongs to exactly one Patch, Block, and District | Spatial containment check on entity position | Every entity tick |
| 2 | Aggregate crowd count at District = sum of Block crowd counts | Recompute and compare at District tick | Every District tick |
| 3 | Heat channels are in range [0.0, 1.0] | Clamp check after every Heat update | Every Heat tick (0.1 Hz) |
| 4 | Event escalation never skips a level | Escalation path logging; audit trail check | Every escalation event |
| 5 | Downward influence never skips a level | Influence application logging | Every influence application |
| 6 | Total entity count does not exceed 8,000 | Entity pool size check | Every entity spawn |
| 7 | No circular escalation (event does not escalate up then cascade down to re-trigger itself) | Escalation source tagging; events carry origin level, cannot re-escalate past origin | Every escalation event |

---

*End of document. For entity definitions, see `ontology-spec-v0.md`. For field update rules, see `field-systems-spec-v0.md`. For material-level consequence rules, see `materials-consequences-spec-v0.md`.*
