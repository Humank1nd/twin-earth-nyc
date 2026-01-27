# Portal Spec — Twin Earth NYC (Multiverse Interface Layer)

**Project:** Twin Earth NYC — Multiverse GTA-Scale Simulation
**Document:** Part 1 Deliverable — Portal System Specification
**Status:** Foundational / Locked
**Version:** 1.0

---

## Portal Definition

> A **portal** is a bounded spatial interface between two universe instances, governed by measurable physical properties (stability, bandwidth, anchor, signature, bleed). It exists as an entity in the Truth Engine, registered in the Trust Ledger, and observable through the city's sensor network.

A portal is not a loading screen. It is not a menu transition. It is not a cutscene trigger. It is a *physical object* in the simulation — a region of space where the physics rules of two universes overlap, creating a traversable boundary. It has a location, a size, a shape, a lifespan, and a set of measurable properties that determine what can pass through it, how long it remains open, and what side effects it produces in the surrounding environment.

Portals are the expansion architecture of the entire project. Every new universe, every new content pack, every new faction, and every new narrative thread enters the simulation through a portal. There are no other entry points. The main menu does not branch into separate game modes. The hub world does not have magic doors to themed zones. Everything connects through portals, and every portal obeys the same rules.

---

## Five Portal Properties

Every portal instance is defined by five measurable properties. These properties are continuous variables, not binary states — a portal can be partially stable, partially open, partially detectable. The interplay of these five values creates the tactical and strategic texture of portal gameplay.

### 1. Stability — `stability: float [0.0 - 1.0]`

**Definition:** The portal's structural integrity as a fraction of maximum coherence. At 1.0, the portal is perfectly stable and will remain open indefinitely (barring external disruption). At 0.0, the portal has collapsed and is no longer traversable.

**Behavior:**
- Stability decays over time at a rate determined by the portal's origin (natural anomalies decay fast, ritually opened portals decay slowly, device-stabilized portals decay at a moderate rate that can be counteracted with maintenance).
- `time_to_collapse` is derived from current stability and decay rate: the estimated seconds until stability reaches 0.0.
- External events can spike or drain stability: energy input increases it, physical disruption decreases it, entropy bleed from the destination universe applies constant downward pressure.
- At `stability < 0.3`, the portal enters a visually and audibly unstable state — flickering, crackling, spatial distortion around the edges. NPCs in sensor range will react with alarm.
- At `stability < 0.1`, traversal becomes dangerous: entities passing through may suffer translation errors (inventory corruption, status effects, positional displacement on the other side).

### 2. Bandwidth — `bandwidth: float [kg/s]`

**Definition:** The maximum mass throughput the portal can sustain per second, measured in kilograms per second. This is a hard cap — exceeding it causes immediate stability damage.

**Behavior:**
- A human body (approximately 70-80 kg) passing through a low-bandwidth portal (e.g., 20 kg/s) would require approximately 3.5-4 seconds of sustained transit, during which the entity is partially in both universes and vulnerable.
- A high-bandwidth portal (e.g., 500 kg/s) allows near-instantaneous human transit and can accommodate vehicles, large objects, or multiple simultaneous entities.
- Bandwidth is correlated with but not identical to portal size. A small portal can have high bandwidth (dense, efficient transfer) and a large portal can have low bandwidth (thin, fragile membrane).
- Attempting to push mass through faster than bandwidth allows causes `stability` drain proportional to the overage. Catastrophic overage (>200% bandwidth) triggers immediate collapse.

### 3. Anchor — `anchor: entity_id`

**Definition:** The entity (object, device, ritual circle, or anomaly source) that binds the portal to its physical location in the hub world. The anchor determines where the portal exists and how it can be moved or destroyed.

**Behavior:**
- If the anchor is a fixed structure (e.g., a building wall, a subway tunnel section), the portal is stationary and its position is determined by the anchor's geometry.
- If the anchor is a movable object (e.g., a device the player built, an artifact), the portal moves with the anchor — but movement causes stability drain proportional to velocity.
- If the anchor is destroyed, the portal immediately enters collapse sequence regardless of current stability.
- Anchors can be transferred between entities through specific gameplay actions (ritual rebinding, device recalibration), but transfer always costs stability.
- The anchor's `entity_id` is registered in the Trust Ledger at portal creation, establishing the causal chain: "this portal exists because this anchor exists at this location at this time."

### 4. Signature — `signature: hash`

**Definition:** A unique identifier generated at portal creation that encodes the portal's origin universe, creation method, and physical characteristics. The signature is detectable by the city's sensor network and by specialized player equipment.

**Behavior:**
- Every portal emits its signature as a detectable field within a radius proportional to its stability and bandwidth. Higher-stability, higher-bandwidth portals are easier to detect at range.
- The signature is a composite hash incorporating: origin universe ID, creation timestamp, creation method (anomaly/ritual/device), anchor entity ID, and a randomized salt.
- Sensors (CCTV with anomaly-detection firmware, specialized player scanners, NPC perceptual models with multiverse awareness) can detect signatures and classify them by origin type.
- Signatures persist after portal collapse as part of the residue patch (see Closing a Portal below), allowing forensic analysis of closed portals.
- Two portals from the same origin universe will have related signatures (shared prefix), enabling pattern detection across multiple events.
- The signature is committed to the Trust Ledger at creation and referenced by every subsequent event involving the portal.

### 5. Entropy Bleed — `entropy_bleed: float [meters, radius]`

**Definition:** The radius around the portal within which the destination universe's physics rules begin to contaminate the hub world's physics rules. Measured in meters from the portal's center point.

**Behavior:**
- Within the bleed radius, physical constants may shift: gravity strength, friction coefficients, light spectrum, speed of sound, material properties. The magnitude of the shift increases closer to the portal.
- At the bleed radius boundary, effects are subtle and ambiguous — a player might notice that colors look slightly wrong or that a dropped object falls slightly too fast. At the portal surface, effects are dramatic and unmistakable.
- Entropy bleed is the primary environmental hazard of portals. It affects everything in the radius: NPCs, vehicles, objects, infrastructure. Prolonged exposure causes cumulative effects (structural fatigue in buildings, disorientation in NPCs, equipment malfunction).
- Bleed radius is proportional to `stability * bandwidth` — a stable, high-bandwidth portal has a large bleed zone. A dying, narrow portal has a tiny one.
- Bleed effects are the most visible and sensor-detectable aspect of portals. They are what draw attention, trigger anomaly alerts, and make portals impossible to operate covertly at high power.

---

## What Portals Do NOT Do

These constraints are as important as the properties. They define the boundaries of the portal system and prevent it from collapsing gameplay into trivial solutions.

| Constraint | Rationale |
|-----------|-----------|
| **No free teleportation anywhere.** | Portals connect to specific universes at specific locations. They are not a fast-travel network. The player cannot open a portal to "the other side of Manhattan." Portals go to *other universes*, not other places in this one. Intra-hub movement uses the city's real transportation systems. |
| **No unlimited mass transfer.** | Bandwidth caps ensure that portals are chokepoints, not highways. You cannot drive a fleet of trucks through a portal. You cannot evacuate a building through one. Every kilogram costs throughput and stability. Mass transfer is a resource to be managed, not assumed. |
| **No invisible or undetectable operation.** | Every portal emits a signature and produces entropy bleed. A portal can be *subtle* (low stability, low bandwidth, small bleed radius) but never *invisible*. The city's sensor network — and attentive NPCs — will eventually detect any active portal. Covert portal operations are about speed and misdirection, not true stealth. |
| **No permanent stability without maintenance.** | Every portal decays. Even the most powerful ritual or the most advanced device cannot create a portal that lasts forever without ongoing energy input, structural maintenance, or anchor reinforcement. Permanent portal infrastructure is an endgame achievement, not a starting condition, and even then it requires upkeep. |
| **No physics override in the hub.** | Entropy bleed can *contaminate* the hub's physics, but it cannot *replace* them. Within the hub world outside the bleed radius, physics truth is absolute. A portal cannot make the hub world's gravity reverse, stop time, or alter fundamental constants. The hub is the ground truth. Portals can stress it, blur it at the edges, but not break it. |

---

## Closing a Portal

Portal closure is not instantaneous. It is a three-phase process that produces observable, detectable, and persistent consequences.

### Phase 1: Unstable (stability dropping toward 0.0)

- Portal begins flickering visually and emitting audio distortion (crackling, harmonic oscillation).
- Entropy bleed radius contracts rapidly, pulling contaminated physics back toward the portal center. Objects and NPCs in the bleed zone experience a brief "snap-back" as normal physics reassert.
- Traversal is still possible but increasingly dangerous. Translation errors spike. Entities mid-transit may be displaced or partially corrupted.
- Duration: seconds to minutes depending on how the closure was initiated (forced collapse is fast, natural decay is slow).

### Phase 2: Collapsing (stability at 0.0, portal geometry contracting)

- The portal's spatial boundary shrinks from its edges toward its center. The visible aperture contracts like a closing iris.
- Anything partially inside the portal at this stage is severed at the boundary — objects are cut, energy fields are disrupted, entities are ejected violently to whichever side contains more of their mass.
- A burst of energy is released proportional to the portal's peak bandwidth and remaining entropy. This burst is detectable by sensors across a wide radius (hundreds of meters for a significant portal) and is the primary alert trigger for authorities and factions.
- Duration: 1-5 seconds. This phase is fast and violent.

### Phase 3: Sealed (portal closed, residue remains)

- The portal's spatial aperture is gone. No traversal is possible.
- A **residue patch** remains at the portal's former location. The patch is a zone of subtly altered physics — detectable by specialized sensors for hours or days depending on the portal's former strength. Residue patches appear visually as a faint shimmer or color aberration, audibly as a low hum or frequency shift.
- The residue patch is the primary forensic evidence of portal activity. Factions, authorities, and the player can analyze residue to determine the portal's origin universe, duration, throughput history, and closure cause.
- The seal event — including portal ID, closure timestamp, closure cause, residue location, and evidence burst characteristics — is committed to the Trust Ledger as an immutable record.

---

## Universe Pack Template

Every universe accessible through the portal system is defined by a standardized data structure called a **Universe Pack**. This is the modular content format that enables expansion without architectural changes.

```
Universe Pack Schema
{
  name:                    string       // Display name: "Earth-616", "Noir-Verse", "Symbiote Hive"
  universe_id:             uuid         // Unique identifier, referenced by all portal signatures
  physics_profile:         object       // Override table for physical constants
                                        //   gravity_multiplier: float
                                        //   friction_modifier: float
                                        //   light_spectrum_shift: vec3
                                        //   speed_of_sound_modifier: float
                                        //   material_property_overrides: map<material_id, properties>
  cognition_profile:       object       // NPC behavior modifications in this universe
                                        //   perception_model_overrides: object
                                        //   memory_model_overrides: object
                                        //   faction_behavior_overrides: object
                                        //   language_model: string
  law_profile:             object       // Governance and enforcement rules
                                        //   authority_factions: array<faction_id>
                                        //   crime_definitions: array<crime>
                                        //   enforcement_response_curves: object
                                        //   legal_status_of_player: enum
  aesthetic_profile:        object       // Visual and audio presentation
                                        //   color_grading_lut: asset_id
                                        //   ambient_audio_set: asset_id
                                        //   skybox_configuration: object
                                        //   particle_system_overrides: object
                                        //   architectural_style: string
  persistence_contract:    object       // How this universe handles state
                                        //   state_persistence: enum [full, session, none]
                                        //   ledger_integration: enum [full, partial, isolated]
                                        //   reset_conditions: array<condition>
  faction_set:             array        // Factions active in this universe
                                        //   [{ faction_id, role, disposition_to_player, power_level }]
  entry_conditions:        object       // Requirements to open a portal to this universe
                                        //   minimum_portal_stability: float
                                        //   required_items: array<item_id>
                                        //   required_knowledge: array<knowledge_id>
                                        //   required_faction_standing: map<faction_id, float>
  loot_table:              object       // Items, artifacts, and resources obtainable
                                        //   guaranteed_drops: array<item_id>
                                        //   probability_tables: array<{item_id, weight, conditions}>
                                        //   unique_artifacts: array<{item_id, acquisition_method}>
  translation_gate_overrides: object    // Special rules for items crossing into/out of this universe
                                        //   import_compatibility_modifiers: map<item_type, float>
                                        //   export_restrictions: array<item_id>
                                        //   special_translation_effects: array<effect>
}
```

---

## Zone Definitions

### Pocket Portal Zone

A **pocket portal zone** is a small, self-contained space accessed through a portal. It is not a full universe — it is a single room, corridor, arena, or environmental set piece floating in the destination universe's context.

- **Size:** 1-5 rooms, roughly 50-500 square meters of traversable space.
- **Persistence:** Session-level by default (resets when portal closes), upgradeable to full persistence with stabilization investment.
- **Physics:** Governed by the destination universe's physics profile, but constrained to a small volume. Entropy bleed into the hub is minimal due to low bandwidth.
- **Purpose:** Tutorial spaces, quick extraction missions, loot caches, narrative encounters, boss arenas. The pocket portal zone is the "dungeon room" equivalent — a contained challenge with a clear entrance and exit.
- **Limit:** A pocket portal zone does not contain portals to other universes. It is a leaf node, not a hub.

### Full Universe Zone

A **full universe zone** is a large, persistent, explorable environment representing a substantial region of an alternate universe. It is the expansion-scale content unit.

- **Size:** Block-scale to district-scale (comparable to the hub's geography), potentially larger.
- **Persistence:** Full persistence by default. State changes in a full universe zone are ledgered and persist across sessions.
- **Physics:** Fully governed by the destination universe's physics profile. Entropy bleed into the hub is significant and must be managed.
- **Purpose:** Major story arcs, faction territory, endgame content, multiplayer zones. Full universe zones are the "expansion packs" — large new areas with their own ecosystems, factions, economies, and narratives.
- **Connectivity:** A full universe zone may contain portals to other universes (including back to the hub), creating a network topology. However, the hub remains the central node — all paths eventually lead back to Times Square.

### The Expansion Rule

> **"Expansions plug in through portals, not new main menus."**

There is no "DLC" in the traditional sense. There are no new campaigns accessed from a menu. Every piece of new content enters the simulation through the portal system. A new universe is discovered through anomaly detection, ritual research, or device construction. A new faction arrives through a portal breach. A new story begins with a signature detection. The player's experience of expansion content is diegetic — it happens inside the simulation, through the simulation's own systems, and is subject to the simulation's rules. This ensures that every expansion strengthens the core loop rather than fragmenting it.

---

## Portal Discovery Methods

There are three ways a portal comes into existence within the simulation. Each method has distinct gameplay implications, resource requirements, and risk profiles.

### 1. Anomaly Chain Detection

**Description:** The city's sensor network (or the player's personal sensors) detects a signature anomaly — an unexplained reading that doesn't match any known physics pattern. The player investigates, following a chain of increasingly strong readings to a location where reality is thin. The portal manifests naturally at that point, either spontaneously or triggered by the player's presence.

**Gameplay characteristics:**
- **Discovery feels emergent** — the player stumbles into something the city wasn't prepared for.
- **Low resource cost** — no special items or knowledge required, just sensor access and investigative skill.
- **Low initial stability** — anomaly-spawned portals are fragile and decay quickly. The player must act fast or invest in stabilization.
- **Unpredictable destination** — the player may not know what's on the other side until they look through.
- **High detection risk** — the anomaly chain is detectable by any entity with sensors, meaning authorities and factions may also be converging on the location.

### 2. Ritual Activation (Strange-Type)

**Description:** Through acquired knowledge (grimoires, faction intel, research data), the player performs a deliberate ritual to open a portal to a specific universe. This requires preparation, specific materials, and a suitable location.

**Gameplay characteristics:**
- **Discovery is intentional** — the player chooses the destination and plans the operation.
- **High resource cost** — rare materials, specific knowledge, time investment, and a secure location.
- **High initial stability** — ritually opened portals are the most stable and long-lasting.
- **Known destination** — the player knows (or can predict) what's on the other side.
- **Moderate detection risk** — the ritual itself is quiet, but the portal's activation produces a signature burst detectable by nearby sensors.

### 3. Tech Rig Construction (Player-Built)

**Description:** The player builds a technological device — a portal generator, stabilizer, or resonance amplifier — using components, blueprints, and engineering knowledge acquired through gameplay. The device, once powered and activated, forces open a portal.

**Gameplay characteristics:**
- **Discovery is engineered** — the player constructs a solution from parts and knowledge.
- **Variable resource cost** — depends on the device's sophistication. Basic rigs are cheap but produce weak portals. Advanced rigs are expensive but produce strong, controllable portals.
- **Moderate initial stability** — device-opened portals are more stable than anomalies but less stable than rituals. Stability can be actively maintained by feeding power to the device.
- **Configurable destination** — with sufficient blueprints and calibration data, the player can target specific universes.
- **Variable detection risk** — the device's power draw and electromagnetic signature are detectable. More powerful devices are harder to hide.

---

## Portal Stabilization Methods

Once a portal exists, its stability decays. Three methods can counteract this decay and extend the portal's operational lifetime.

### 1. Strange Ritual Stabilization

- **Stability output:** Highest (stability restored to 0.9-1.0 and decay rate reduced to near zero for the ritual's duration).
- **Availability:** Limited. Requires rare knowledge, rare materials, and faction standing with mystical factions. Not available in early game.
- **Maintenance model:** Periodic re-casting required. Each re-cast requires fresh materials. The ritual location must remain undisturbed.
- **Trade-off:** Maximum stability, but the player is dependent on scarce resources and faction relationships to maintain it.

### 2. Device Rig Stabilization

- **Stability output:** Moderate (stability maintained at 0.5-0.7 with active power supply).
- **Availability:** Player-craftable once blueprints and components are acquired. Available in mid-game.
- **Maintenance model:** Continuous power draw. The device requires fuel, batteries, or a tapped power source. Power interruption causes immediate stability drop.
- **Trade-off:** Reliable and self-sufficient, but requires ongoing resource expenditure and the device itself is a physical object that can be discovered, damaged, or stolen.

### 3. Artifact Anchor Stabilization

- **Stability output:** Variable (depends on the artifact's properties — some artifacts provide 0.3 stability, others provide 0.95).
- **Availability:** Loot-dependent. Artifacts are obtained from other universes, faction rewards, or anomaly events. Availability is unpredictable.
- **Maintenance model:** Passive — the artifact radiates stability as long as it's positioned at the anchor point. No ongoing input required. However, removing the artifact instantly removes the stabilization.
- **Trade-off:** Potentially the most efficient method (no ongoing costs), but the player must find and secure the right artifact, and keeping it at the portal site means not using it elsewhere.

---

## Portal Mission Verbs

Every portal-based mission is built around one of three core verbs. These verbs define the objective structure, the success/failure conditions, and the primary tension of the operation.

### 1. Extract

**Definition:** Retrieve a target (object, person, data, sample) from the destination universe and bring it back to the hub through the portal.

**Core tension:** The target is on the other side. The portal is decaying. The player must locate the target, secure it, and return before collapse — while managing bandwidth limits, translation compatibility, and whatever opposition the destination universe presents.

**Success:** Target arrives in the hub. Translation gate processes it. Ledger records the import. Player possesses the extracted item/entity.

**Failure modes:** Portal collapses before return (player stranded or ejected without target). Target exceeds bandwidth (cannot transit). Target has zero translation compatibility (destroyed in transit). Opposition prevents acquisition.

### 2. Contain

**Definition:** Seal a breach, prevent bleed, or neutralize a threat that is leaking from a destination universe into the hub through an active or unstable portal.

**Core tension:** Something is coming through, and the hub's systems are reacting. The player must reach the portal, assess the threat, and either stabilize and seal the portal or enter the destination universe to neutralize the source. Meanwhile, entropy bleed is affecting the surrounding neighborhood, sensors are spiking, authorities are responding, and public panic is building.

**Success:** Portal sealed (stability reduced to 0.0 in a controlled manner). Bleed effects neutralized. Threat contained. Residue patch left for forensic follow-up. Ledger records containment.

**Failure modes:** Bleed expands beyond containable radius (triggers city-wide alert). Entity fully transits into hub (creates persistent threat in the hub world). Uncontrolled collapse (evidence burst attracts maximum authority response). Player overwhelmed by destination-side opposition.

### 3. Infiltrate

**Definition:** Enter the destination universe covertly to gather intelligence, sabotage a target, or establish a foothold without being detected by the destination's inhabitants.

**Core tension:** The player is operating behind enemy lines with limited resources, no backup, and a decaying exit. The destination universe has its own sensor systems, its own factions, and its own rules. The player must accomplish the objective and exfiltrate cleanly — or face the consequences of discovery in an alien environment with no hub-world support.

**Success:** Objective completed (intel gathered, target sabotaged, foothold established). Player returns to hub without triggering destination-side alarm. Evidence of intrusion is minimal. Ledger records the operation.

**Failure modes:** Detection by destination factions (triggers pursuit, possible follow-through into hub). Portal collapses during operation (player stranded). Objective failure (target not found, sabotage incomplete). Cover blown on return (evidence of intrusion detected by hub-side sensors, creating Heat and faction suspicion).

---

## Translation Gate Rules

The **translation gate** is the boundary layer within a portal that governs how matter, energy, and information transform as they cross between universes. Every entity and object that passes through a portal is processed by the translation gate. Five rules govern this process.

### Rule 1: Compatibility Score

Every item imported through a portal has a **compatibility score** ranging from 0.0 to 1.0, representing how well the item's physical properties, material composition, and functional principles map to the destination universe's physics profile.

- **1.0:** Perfect compatibility. The item functions identically on both sides. (Example: a simple iron knife imported from a universe with identical metallurgy.)
- **0.5-0.9:** Partial compatibility. The item functions but with degraded performance, altered properties, or cosmetic changes. (Example: an energy weapon from a high-tech universe operates in the hub but at reduced power, with overheating issues, and emitting an unusual sound.)
- **0.1-0.4:** Low compatibility. The item is unstable, toxic, or hazardous in the destination universe. It may decay, emit harmful radiation, corrode surrounding materials, or behave unpredictably. (Example: organic matter from a universe with different biochemistry begins decomposing rapidly in the hub, releasing toxic compounds.)
- **0.0:** Zero compatibility. The item cannot exist in the destination universe. It is destroyed during translation — converted to inert residue and an energy burst. The ledger records the destruction.

### Rule 2: Decay, Toxicity, and Instability

Items with low compatibility (below 0.5) suffer ongoing negative effects in the destination universe. These effects are not instantaneous — they accumulate over time, creating a logistics and risk-management challenge.

- **Decay:** The item loses structural integrity over time. A weapon's blade dulls. An electronic device glitches. A container corrodes. Decay rate is inversely proportional to compatibility.
- **Toxicity:** The item emits substances or energies harmful to the local environment. Biological contamination, radiation, chemical off-gassing, or psychic interference. Toxicity severity is inversely proportional to compatibility.
- **Instability:** The item's behavior becomes unpredictable. A device may activate randomly. A material may phase-shift. An artifact may emit uncontrolled energy pulses. Instability frequency is inversely proportional to compatibility.

### Rule 3: Signature Traces

All imported items retain detectable traces of their origin universe's signature. These traces are permanent and cannot be removed or suppressed. They are detectable by the hub's sensor network, by specialized player equipment, and by NPCs with multiverse awareness.

- The trace intensity is proportional to the item's mass and inversely proportional to its compatibility score. A large, low-compatibility item screams its alien origin. A small, high-compatibility item whispers.
- Signature traces are the primary mechanism by which authorities, factions, and other players detect multiverse activity. Carrying imported items increases the player's detectability profile.
- The Trust Ledger records every import event, including the item's origin signature, translation timestamp, compatibility score, and the player responsible.

### Rule 4: Mass/Energy Throughput Cap

The portal's bandwidth property imposes a hard cap on the rate at which mass and energy can pass through the translation gate. This cap applies equally to all entities — the player, NPCs, objects, projectiles, radiation, and sound.

- The bandwidth cap is per-second, not per-transit. A player carrying 30 kg of equipment through a 50 kg/s portal transits in approximately 2 seconds (player mass + equipment mass / bandwidth).
- Energy throughput is converted to mass-equivalent using the portal's translation coefficient (which varies by universe pair). A high-energy beam passing through a portal may be attenuated to the point of uselessness if the bandwidth is low.
- Attempting to exceed the bandwidth cap triggers stability damage. The translation gate does not queue excess throughput — it rejects it, violently.

### Rule 5: No Bypass of Hub Physics Truth

No item, entity, ability, or effect imported through a portal can override the hub world's fundamental physics rules. This is the master rule — the one that protects the simulation's ground truth.

- An item that grants flight in its origin universe does not grant flight in the hub if the hub's physics do not permit human flight. The item may still function (emitting energy, glowing, producing thrust) but the *effect* is constrained by hub physics.
- An entity with supernatural abilities in its origin universe is subject to the hub's physics upon arrival. If the hub's physics do not support telepathy, the entity cannot use telepathy in the hub — though they may retain the *knowledge* they gained through telepathy elsewhere.
- This rule has one exception: within the entropy bleed radius of an active portal, the destination universe's physics partially apply. The closer to the portal, the more the origin rules bleed through. This is the only place in the hub where imported abilities and items can function at full power — and it is also the most dangerous and detectable zone in the simulation.

---

*End of Portal Spec — Part 1 Deliverable*
