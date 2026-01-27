# Portal State Machine + Properties Spec v0

> **Twin Earth NYC** -- Part 11: Multiverse Gameplay
> **Document:** Portal State Machine + Properties Specification
> **Version:** 0.1.0
> **Status:** Draft
> **Last Updated:** 2026-01-27

---

## Table of Contents

1. [Overview](#overview)
2. [Portal Properties](#portal-properties)
3. [Portal State Machine](#portal-state-machine)
4. [State Machine Diagram](#state-machine-diagram)
5. [State Transition Reference](#state-transition-reference)
6. [Stabilization Methods](#stabilization-methods)
7. [Disruption Methods](#disruption-methods)
8. [Integration Notes](#integration-notes)

---

## Overview

A **portal** is a traversable connection between two universes. Portals are the core mechanic of multiverse gameplay -- they are how the player accesses alternate universes, conducts operations, imports exotic materials, and generates the anomalies that drive the Heat and Evidence economies.

Portals are **not free highways**. They are volatile, resource-intensive, and dangerous. Every portal has measurable properties that decay over time, a finite state machine governing its lifecycle, and consequences for the surrounding environment. The player must actively manage portals -- stabilizing them for operations, sealing them to reduce Heat, and sometimes deliberately destabilizing them as a tactical weapon.

This document defines:

- **Portal Properties** -- the five numeric/data properties that describe a portal's current state.
- **Portal State Machine** -- the six states a portal can occupy and the transitions between them.
- **Stabilization Methods** -- how the player (and factions) can increase portal stability.
- **Disruption Methods** -- how portals can be destabilized or destroyed.

### Design Intent

Portals should feel like **controlled explosions** -- powerful, useful, but inherently unstable. The player is always balancing the utility of an open portal (access, loot, operations) against the cost (Heat, evidence, ecological damage, resource expenditure). There is no "free" portal. Every opening has a price.

---

## Portal Properties

Every portal entity in the simulation carries the following five properties. These properties are updated each simulation tick and are readable by the player through detection equipment and by NPCs through faction-specific sensors.

### Properties Table

| Property | Type | Range | Default (Latent) | Decay Rule | Player Influence | System Coupling |
|---|---|---|---|---|---|---|
| **stability** | `float` | 0.0 -- 1.0 | 0.0 | -0.01/min natural decay; -0.05/min if bandwidth exceeded | Stabilize (ritual/device): +0.3; Overload: -0.2 | Triggers state transitions at thresholds |
| **bandwidth** | `float` | 0 -- 100 kg/s | 10 kg/s | Fixed per portal class (does not decay) | Upgrade via device: x1.5 (cannot exceed hard cap of 100 kg/s) | Translation Gate mass flow limit |
| **anchor** | `entity_id` | any valid entity / null | null | Breaks (sets to null) if anchor entity is destroyed | Player can set anchor (device required, 30s setup) | Required for STABLE state |
| **signature** | `hash` | unique 64-char hex | Auto-generated on FORMING | Permanent (never changes, never decays) | Cannot be altered, only detected (detection device required) | Used for tracking, faction intel, evidence |
| **entropy_bleed** | `float` | 0 -- 50m radius | 0m | Grows +0.5m/min while portal is open; shrinks -0.1m/min after sealed | Containment action reduces active radius by 50% | Feeds Ecological Heat, affects local physics |

### Property Details

#### stability (float, 0.0 -- 1.0)

The primary health metric of a portal. Determines whether the portal can sustain traversal and how dangerous it is to use.

| Stability Range | Meaning | Traversal Safety | Visual Indicator |
|---|---|---|---|
| 0.0 -- 0.1 | Critical / Collapsing | Lethal (instant kill on traversal attempt) | Violent flickering, energy arcs, debris pulled in |
| 0.1 -- 0.3 | Unstable | Dangerous (50% chance of 30-70% HP damage) | Rapid distortion, intermittent visibility, sparks |
| 0.3 -- 0.5 | Marginal | Risky (20% chance of 10-30% HP damage) | Visible wobble, occasional flicker, audible stress |
| 0.5 -- 0.7 | Operational | Safe (no traversal damage) | Steady glow, clear view of destination, stable hum |
| 0.7 -- 1.0 | Optimal | Safe + bonus (faster traversal, reduced adjustment time) | Clean edges, bright and steady, harmonic tone |

**Decay mechanics:**
- Natural decay: -0.01 per minute (a stable portal at 0.7 lasts ~70 minutes before reaching zero without intervention).
- Bandwidth penalty: -0.05 per minute if current throughput exceeds bandwidth rating.
- Heat penalty: if any Heat channel > 0.8 in the portal's vicinity, decay rate doubles (-0.02/min natural).
- Stabilization actions counteract decay (see Stabilization Methods).

#### bandwidth (float, 0 -- 100 kg/s)

The maximum mass flow rate through the portal. Determines how quickly and how much material can be moved.

| Portal Class | Default Bandwidth | Upgrade Cap | Typical Use |
|---|---|---|---|
| Micro (spontaneous anomaly) | 5 kg/s | 7.5 kg/s | Single person, light gear |
| Standard (ritual/tech-opened) | 10 kg/s | 15 kg/s | Person + equipment, small artifacts |
| Heavy (faction infrastructure) | 30 kg/s | 45 kg/s | Multiple people, heavy equipment, vehicles (disassembled) |
| Mega (story event only) | 100 kg/s | 100 kg/s (hard cap) | Large-scale transit, plot-driven |

**Hard cap:** No portal can exceed 100 kg/s regardless of upgrades. This is a universe-physics constraint, not a technology limit.

**Exceeding bandwidth:** If the player attempts to push more mass through than the bandwidth allows:
1. Excess mass is rejected (bounced back with force).
2. Stability drops by -0.05 per failed attempt.
3. Portal enters stressed state (visual/audio warning).
4. If bandwidth is exceeded continuously for >30 seconds, portal transitions to UNSTABLE.

#### anchor (entity_id, nullable)

The physical or mystical anchor point that holds the portal in place. Without an anchor, a portal cannot reach STABLE state -- it will remain FORMING until it times out and collapses.

**Anchor types:**
| Anchor Type | Set Method | Durability | Notes |
|---|---|---|---|
| Physical device | Player places tech rig, 30s setup | Can be damaged/destroyed by combat or sabotage | Most common player-controlled anchor |
| Mystical mark | Strange's ritual, instant | Fades over 24h sim-time unless renewed | Limited availability, requires Strange faction |
| Natural convergence | Pre-placed (story/world event) | Permanent (cannot be destroyed, only sealed) | Rare, tied to specific locations |

**Anchor destruction:** If the anchor entity is destroyed (combat, sabotage, decay), the anchor property sets to null. If the portal is in STABLE state, it immediately transitions to UNSTABLE. If it was the only anchor, the portal will eventually collapse.

#### signature (hash, unique)

A permanent, unique identifier for each portal. Generated when the portal enters FORMING state. The signature never changes and never decays -- even after the portal is SEALED, the signature remains traceable in residue patches for 24 hours of sim-time.

**Gameplay function:**
- **Detection:** Player can detect portal signatures with scanning equipment. This reveals portal location, state, and properties.
- **Tracking:** Factions use signatures to catalog portal activity. Repeated openings at the same location generate a pattern that factions notice.
- **Evidence:** Signatures are logged in the Evidence Economy. Each unique signature is a data point that feeds Institutional Heat.
- **Forensics:** After a portal is sealed, the residue patch retains the signature. Authority faction can analyze residue to link events.

#### entropy_bleed (float, 0 -- 50m radius)

The radius of reality distortion around an active portal. Within the entropy_bleed zone, physics become unreliable, anomalies manifest, and the environment degrades.

| Bleed Radius | Effects Within Zone | Evidence Generated | Ecological Heat Impact |
|---|---|---|---|
| 0 -- 5m | Subtle visual shimmer, EM readings spike | Low (sensors only) | +0.01/min |
| 5 -- 15m | Gravity fluctuations (+/- 10%), temperature shifts, light bending | Medium (visible to attentive NPCs) | +0.03/min |
| 15 -- 30m | Structural stress (cracks, vibration), electronics malfunction, wildlife panic | High (obvious to anyone in zone) | +0.05/min |
| 30 -- 50m | Micro-portal sparks, reality tears (visual only), severe structural damage | Critical (impossible to miss) | +0.10/min |

**Growth rule:** +0.5m per minute while the portal is in FORMING, STABLE, or UNSTABLE states.
**Shrink rule:** -0.1m per minute after the portal enters SEALED state.
**Containment:** A player containment action (device or ritual) reduces the active bleed radius by 50% immediately. This does not stop growth, only cuts the current radius.

---

## Portal State Machine

### States

A portal exists in exactly one of six states at any given time. States are mutually exclusive and collectively exhaustive -- every portal is always in one state.

| State | Description | Traversable | Duration | Player Actions Available |
|---|---|---|---|---|
| **LATENT** | A potential portal site. No visible manifestation. Detectable only by specialized equipment as an anomaly reading. | No | Indefinite | Detect (scan), Monitor, Pre-position anchor |
| **FORMING** | A portal is materializing. Visible distortion, energy readings spiking, signature generated. Not yet traversable. | No | 30 -- 120 seconds (natural), or until stabilized/failed | Stabilize (to reach STABLE), Abandon (let it fail), Set anchor |
| **STABLE** | A fully operational portal. Clear view of destination, safe traversal, bandwidth active. | Yes (safe) | Until stability decays below threshold or deliberately sealed | Traverse, Transport items, Upgrade bandwidth, Seal (controlled) |
| **UNSTABLE** | A portal under stress. Visual distortion, traversal risky, bleed spikes. | Yes (risky) | Until re-stabilized or collapsed | Re-stabilize, Emergency traverse (risky), Trigger collapse |
| **COLLAPSING** | A portal in terminal failure. Violent energy release, untraverable, danger zone. | No (lethal) | 10 -- 30 seconds | Evacuate zone, Emergency containment (reduce blast) |
| **SEALED** | A closed portal. Residue patch remains, signature traceable, no traversal possible. | No | Residue persists 24h sim-time, then entity removed | Analyze residue, Clean residue (reduce evidence), Re-open (extremely difficult) |

### State Transition Table

| From State | To State | Trigger Condition | Duration | Effects |
|---|---|---|---|---|
| LATENT | FORMING | `anomaly_intensity > 0.7` OR `ritual_activation` OR `tech_rig_powered` | 30 -- 120s formation period | Signature generated and becomes detectable; entropy_bleed starts at 1m; energy readings spike; nearby IoT sensors trigger `anomaly.detected` event |
| FORMING | STABLE | `stability > 0.6` AND `anchor_set == true` | Instant transition | Portal becomes traversable; bandwidth activates at class default; entropy_bleed stabilizes at current radius; visual clears to show destination; audio shifts to stable hum |
| FORMING | COLLAPSING | `stability < 0.2` during FORMING OR timeout (5 min without reaching STABLE) | 10 -- 30s collapse | Energy burst (Physical Heat +0.1 in 20m radius); evidence spike (all three classes); entropy_bleed spikes to current + 10m then begins decay |
| STABLE | UNSTABLE | `stability < 0.4` OR bandwidth exceeded for >30s OR anchor damaged (not destroyed) OR any Heat channel > 0.8 in vicinity | Instant transition | Visual distortion begins; random entropy_bleed spikes (+1-5m bursts); traversal becomes risky (damage chance per crossing); audio shifts to stressed whine; NPC alert radius doubles |
| UNSTABLE | STABLE | `stability > 0.6` restored (via stabilization action) AND anchor intact | Instant transition | Returns to normal STABLE operation; bleed spikes stop; traversal safe again; audio normalizes |
| UNSTABLE | COLLAPSING | `stability < 0.1` OR anchor destroyed OR player triggers deliberate collapse | 10 -- 30s collapse | Massive energy burst (Physical Heat +0.2 in 30m radius); evidence spike (maximum); entropy_bleed spikes to current + 20m; structural damage in blast radius; NPC panic in 50m radius |
| COLLAPSING | SEALED | Automatic after collapse duration expires | Instant transition | Portal entity removed from active simulation; residue patch spawned at location; signature traceable for 24h sim-time; entropy_bleed begins decay (-0.1m/min from peak); Ecological Heat persists |
| STABLE | SEALED | Player or faction performs controlled seal (containment action) | 5 -- 15s shutdown sequence | Clean shutdown; minimal energy release (Physical Heat +0.02); small residue patch; signature traceable for 24h; entropy_bleed begins decay immediately; authority faction notes clean seal (reputation positive) |

---

## State Machine Diagram

### ASCII State Diagram

```
                        anomaly_intensity > 0.7
                        OR ritual_activation
                        OR tech_rig_powered
                              |
                              v
    +--------+          +---------+
    | LATENT | -------> | FORMING |
    +--------+          +---------+
                         /       \
                        /         \
           stability>0.6      stability<0.2
           AND anchor_set      OR timeout(5min)
                      /             \
                     v               v
               +--------+      +------------+
          +--> | STABLE | ---> | COLLAPSING |
          |    +--------+      +------------+
          |     |      |              |
          |     |      |   controlled |  automatic
 stability|     |      |     seal     |  after duration
    >0.6  |     |      |        |     |
          |     v      |        v     v
        +----------+   |    +--------+
        | UNSTABLE |   +--> | SEALED |
        +----------+   |    +--------+
              |         |
              |         |
     stability<0.1      |
     OR anchor_destroyed|
     OR player_trigger  |
              |         |
              v         |
        +------------+  |
        | COLLAPSING |--+
        +------------+
```

### Detailed Flow Diagram

```
                    +=============+
                    ||  LATENT   ||
                    || (dormant) ||
                    +=============+
                          |
          ~~~~~~~~~~~~~~~~|~~~~~~~~~~~~~~~~
          : anomaly > 0.7 | ritual | tech :
          ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                          |
                          v
                    +=============+
                    ||  FORMING  ||  duration: 30-120s
                    || (visible) ||  bleed starts: 1m
                    +=============+  signature: generated
                       /      \
                      /        \
      +==============+    timeout OR    +==============+
      || stability   |    stability     || COLLAPSING  ||
      || > 0.6 AND   |    < 0.2        || (failure)   ||
      || anchor set  |                  +==============+
      +==============+                        |
             |                                |
             v                                v
      +=============+                  +=============+
      ||  STABLE   || <--- restab --- ||  SEALED    ||
      || (active)  ||    ility>0.6    || (residue)  ||
      +=============+                  +=============+
        |    |    |                          ^
        |    |    +--- controlled seal ------+
        |    |                               |
        |    v                               |
        |  +=============+                   |
        |  || UNSTABLE  || --- collapse -----+
        |  || (stressed)||     (via COLLAPSING)
        |  +=============+
        |        ^
        +--------+
       heat>0.8 OR
       bandwidth exceeded OR
       anchor damaged OR
       stability < 0.4

    Legend:
    +====+ = State (double border = primary states)
    ----> = Transition
    ~~~~~ = Trigger condition
```

---

## State Transition Reference

### LATENT to FORMING

**Trigger conditions (any one):**
1. `anomaly_intensity > 0.7` -- natural anomaly buildup exceeds threshold. This happens at pre-determined locations (anomaly hotspots) or dynamically based on Ecological Heat.
2. `ritual_activation` -- a character (player via Strange's faction, or NPC) performs a portal-opening ritual. Requires mystical knowledge and components.
3. `tech_rig_powered` -- player activates a portal tech rig at a valid anomaly site. Requires crafted device + power source.

**Formation duration:** 30 -- 120 seconds, determined by:
- Anomaly intensity (higher = faster formation)
- Method (ritual: 30-60s, tech rig: 60-90s, natural anomaly: 60-120s)
- Universe compatibility (similar universes form faster)

**Immediate effects on formation start:**
- Portal signature is generated (unique hash, permanent).
- Entropy_bleed initializes at 1m radius and begins growing (+0.5m/min).
- IoT sensor network detects energy spike: `anomaly.energy.spike` event fires.
- Nearby NPCs within 20m may notice visual distortion (Social Heat +0.05).
- CCTV cameras within LOS begin recording anomaly (Digital evidence generated).

### FORMING to STABLE

**Requirements (all must be met):**
1. `stability > 0.6` -- achieved through stabilization actions during FORMING.
2. `anchor_set == true` -- player or NPC has placed an anchor entity.

**Effects on stabilization:**
- Portal becomes traversable. Player can see the destination universe through the portal surface.
- Bandwidth activates at the portal's class default (see bandwidth property table).
- Entropy_bleed stabilizes (stops growing, holds at current radius).
- Audio shifts from formation crackle to stable harmonic hum.
- Visual clarifies from distorted shimmer to clear window/doorway.

### FORMING to COLLAPSING (Formation Failure)

**Trigger conditions (any one):**
1. `stability < 0.2` -- stability dropped too low during formation (interference, no stabilization effort).
2. Timeout: 5 minutes elapsed since FORMING began without reaching STABLE requirements.

**Effects:**
- Energy burst: Physical Heat +0.1 in 20m radius. NPCs in range take minor damage (5-15% HP).
- Evidence spike: all three evidence classes (physical scarring, CCTV flash, witness reports).
- Entropy_bleed spikes to current_radius + 10m, then begins standard decay.
- Portal does not become traversable -- proceeds directly to COLLAPSING, then SEALED.

### STABLE to UNSTABLE

**Trigger conditions (any one):**
1. `stability < 0.4` -- natural decay or external interference brought stability below safe threshold.
2. Bandwidth exceeded for >30 continuous seconds.
3. Anchor damaged (but not destroyed) -- taking combat damage, environmental stress.
4. Any Heat channel > 0.8 in the portal's vicinity (within entropy_bleed radius).

**Effects:**
- Visual: portal surface distorts, ripples, occasionally flickers to show "wrong" destinations.
- Entropy_bleed: random spikes (+1-5m bursts every 10-30 seconds, unpredictable).
- Traversal risk: each crossing has a damage chance (see stability table in Properties section).
- Audio: stable hum shifts to stressed whine with intermittent crackle.
- NPC alert radius doubles -- NPCs further away notice the anomaly.

### UNSTABLE to STABLE (Re-stabilization)

**Requirements:**
1. `stability > 0.6` -- achieved through stabilization actions.
2. Anchor must still be intact (even if damaged, as long as entity exists).

**Effects:**
- All UNSTABLE effects cease. Portal returns to normal STABLE operation.
- Entropy_bleed spikes stop (radius holds at current level, resumes normal growth).
- Traversal is safe again.
- Note: re-stabilization does not repair anchor damage. A damaged anchor remains vulnerable.

### UNSTABLE to COLLAPSING

**Trigger conditions (any one):**
1. `stability < 0.1` -- portal is beyond recovery.
2. Anchor destroyed -- the physical/mystical anchor entity is eliminated.
3. Player triggers deliberate collapse (tactical choice -- button press with confirmation).

**Effects:**
- Massive energy burst: Physical Heat +0.2 in 30m radius. NPCs in range take significant damage (20-40% HP). Structural damage to environment.
- Evidence spike: maximum generation across all three classes.
- Entropy_bleed spikes to current_radius + 20m.
- NPC panic propagation in 50m radius (Social Heat +0.2).
- Any entities in transit during collapse take 50-80% HP damage and are ejected to the origin side.

### COLLAPSING to SEALED

**Trigger:** Automatic after collapse duration (10-30 seconds) expires. No player action required or possible.

**Effects:**
- Portal entity removed from active simulation.
- Residue patch spawned at portal location:
  - Contains portal signature (traceable for 24h sim-time).
  - Visual: scorched/distorted ground texture, faint shimmer.
  - Detectable by all sensor types (physical, digital, NPC witness memory).
- Entropy_bleed begins decay from peak (-0.1m/min).
- Ecological Heat remains elevated until bleed fully decays.

### STABLE to SEALED (Controlled Seal)

**Trigger:** Player or faction NPC performs a controlled seal action. Requires:
- Player must be within 5m of portal.
- Sealing device or ritual knowledge.
- 5-15 second channeling time (interruptible by combat).

**Effects:**
- Clean shutdown: minimal energy release (Physical Heat +0.02, barely noticeable).
- Small residue patch (less evidence than collapse -- signature traceable for 12h instead of 24h).
- Entropy_bleed begins immediate decay from current radius (-0.1m/min).
- Authority faction recognizes clean seals positively (reputation +0.05 if they observe it).
- Strange's faction prefers clean seals (reputation +0.1).

---

## Stabilization Methods

The player has three primary methods to increase portal stability. Each has different costs, availability, and tactical implications.

### Stabilization Methods Table

| Method | Stability Gain | Cost | Availability | Cooldown | Setup Time | Risk |
|---|---|---|---|---|---|---|
| **Strange Ritual** | +0.5 | Narrative cost (requires Strange's time, faction favor) | Limited: 1-2 per act, requires Strange faction standing > 0.3 | 24h sim-time between uses | 10s (ritual animation) | None (guaranteed success) |
| **Tech Rig** | +0.3 | Components (3x circuit board, 1x power cell, 1x antenna) + 5 min setup time + continuous power draw | Player-craftable after Act 1 tutorial, components purchasable or lootable | 1h sim-time between uses (rig cooldown) | 5 min (assembly + calibration) | 10% chance of minor overload (-0.05 stability, repairable) |
| **Artifact Anchor** | +0.1 to +0.4 (varies by artifact quality) | Consumes the artifact permanently | Loot-dependent: artifacts found during operations or purchased on black market | None (limited by artifact supply) | Instant (artifact is consumed on use) | Unpredictable: stability gain varies. Low-quality artifacts may only give +0.1. Exotic artifacts risk compatibility backlash (+0.4 stability but Ecological Heat +0.05) |

### Method Details

#### Strange Ritual

The most reliable stabilization method but the most constrained by narrative availability. Doctor Strange (or his designated agent) performs a mystical stabilization ritual that cleanly boosts portal stability.

**Requirements:**
- Strange faction reputation > 0.3 (trusted ally status).
- Strange or his agent must be present (or reachable by Sling Ring communication).
- Narrative availability: Strange has competing priorities. The player can request stabilization 1-2 times per story act, but additional requests require quid pro quo (side missions for Strange).

**Tactical notes:**
- Best used for critical operations where failure is not acceptable.
- Can stabilize a portal from FORMING to STABLE in one action (+0.5 brings most portals above 0.6).
- Leaves no physical evidence (mystical stabilization is undetectable by tech sensors).
- Ecological impact is neutral (mystical stabilization does not increase entropy_bleed).

#### Tech Rig

The workhorse stabilization method. Player-crafted, reusable (with cooldown), and reliable. The tech rig is a portable device that emits a stabilizing energy field tuned to the portal's signature.

**Requirements:**
- Crafting recipe unlocked after Act 1 tutorial.
- Components: 3x circuit board (common loot/purchase), 1x power cell (uncommon), 1x antenna (common).
- 5-minute setup time (player must remain within 5m of portal during calibration).
- Continuous power draw while active (power cell depletes over 2h sim-time).

**Tactical notes:**
- Primary method for routine operations.
- Can be pre-positioned at known anomaly sites before portal formation.
- Bandwidth upgrade module (separate craft) can be attached: x1.5 bandwidth boost.
- 10% overload risk on each use -- mitigated by higher crafting skill (future system).
- Generates medium tech signature (detectable by institutional sensors within 50m).

#### Artifact Anchor

A consumable stabilization method. Exotic artifacts from other universes carry inherent dimensional energy that can be channeled into portal stabilization. The artifact is consumed in the process.

**Requirements:**
- A compatible artifact in player inventory (compatibility > 0.3 with portal's target universe).
- Artifact must have sufficient energy charge (freshly imported artifacts have more).

**Tactical notes:**
- Quality varies: common artifacts give +0.1, rare give +0.2-0.3, exotic give +0.3-0.4.
- Instant use -- no setup time. Valuable for emergency stabilization mid-operation.
- Consumed permanently. There is no way to recover a used artifact.
- Exotic artifacts may cause compatibility backlash: +0.4 stability but Ecological Heat +0.05 due to energy release.
- Black market price for stabilization-grade artifacts: high (Criminal faction markup).

---

## Disruption Methods

Portals can be deliberately destabilized by the player, by hostile NPCs, or by faction agents. Disruption is a tactical tool -- sometimes you need to collapse an enemy's portal.

### Disruption Methods Table

| Method | Stability Loss | Evidence Generated | Risk to User | Cooldown | Requirements |
|---|---|---|---|---|---|
| **Sabotage (damage anchor)** | -0.3 | High (physical evidence: damage marks, tool traces, structural damage) | Structural damage in immediate area, Physical Heat +0.1 spike | None (limited by access to anchor) | Physical access to anchor entity, sabotage tools (crowbar, explosives, EMP device) |
| **Overload (exceed bandwidth)** | -0.2 per attempt | Medium (energy signature spike, detectable by sensors within 100m) | Blowback damage to user: 15-25% HP per attempt, pushed back 5m | 30s between attempts (recovery time) | Mass to push through (at least 50kg over bandwidth limit), physical proximity to portal |
| **Counter-ritual** | -0.4 | Low (subtle mystical residue, undetectable by tech sensors) | May backfire: 20% chance of -0.2 stability to ALL portals in 500m radius (including friendly) | 12h sim-time | Rare mystical knowledge (Strange faction rep > 0.5 OR stolen grimoire from black market), ritual components (candles, sigils, 2-minute channeling time) |

### Method Details

#### Sabotage (Damage Anchor)

The brute-force approach. Physically damage or destroy the anchor entity to destabilize the portal.

**Execution:**
1. Gain physical access to the portal's anchor (may require infiltration).
2. Apply destructive force: melee attack, explosives, EMP (for tech anchors).
3. Stability drops -0.3 on successful anchor damage, -0.5+ if anchor is destroyed outright.

**Evidence profile:**
- Physical evidence: damage marks, tool traces, explosive residue, structural damage.
- Digital evidence: CCTV footage of sabotage (if cameras present), sensor logs showing sudden stability drop.
- Witness evidence: NPCs may observe sabotage (depending on stealth).
- Total evidence generation: HIGH. Sabotage is loud, messy, and leaves traces.

**Risks:**
- Structural damage to surrounding environment (Physical Heat +0.1).
- If anchor is destroyed, portal enters COLLAPSING immediately (energy burst, blast radius).
- Player may be caught in blast radius if too close during collapse.
- Criminal faction may have booby-trapped their anchors (counter-sabotage explosives).

#### Overload (Exceed Bandwidth)

Force too much mass through the portal simultaneously, stressing it beyond its operating parameters.

**Execution:**
1. Position sufficient mass near the portal (at least 50kg over the bandwidth limit).
2. Push the excess mass through in a single burst.
3. Portal stability drops -0.2 per overload attempt.

**Evidence profile:**
- Energy signature spike (medium) -- detectable by sensors within 100m.
- Physical evidence: scattered objects that were rejected by the portal (bounced back).
- Low witness evidence (the overload itself is brief and confusing to observers).

**Risks:**
- Blowback damage: 15-25% HP to the user per attempt. The portal rejects excess mass violently.
- User is pushed back 5m from the portal surface.
- 30-second recovery time between attempts (player is stunned/staggered).
- If stability drops below 0.1 from overload, immediate COLLAPSING transition (be far away).

#### Counter-ritual

The surgical approach. A mystical counter-ritual that unravels the dimensional energy holding the portal together.

**Execution:**
1. Acquire counter-ritual knowledge (Strange faction at high trust, OR stolen grimoire from black market).
2. Gather components: 3x mystic candles, 1x sigil chalk, clear space within 10m of portal.
3. Channel for 2 minutes (interruptible by combat or portal state change).
4. On completion: stability drops -0.4.

**Evidence profile:**
- Mystical residue: undetectable by tech sensors. Only Strange's faction (or equivalent mystical actors) can identify a counter-ritual was performed.
- No physical evidence. No digital evidence. Minimal witness evidence (ritual looks like "someone meditating near the portal").
- Total evidence generation: LOW. The cleanest disruption method.

**Risks:**
- 20% backfire chance: if the ritual fails, ALL portals within 500m radius lose -0.2 stability. This includes the player's own portals. Catastrophic if multiple portals are active nearby.
- Requires rare knowledge: Strange faction won't teach counter-rituals casually (reputation > 0.5 required). Black market grimoires are expensive and may be incomplete (increasing backfire chance to 35%).
- 2-minute channeling time leaves the player vulnerable to interruption.

---

## Integration Notes

### System Dependencies

| System | Reads From Portal | Writes To Portal | Notes |
|---|---|---|---|
| **Heat System** | entropy_bleed, state transitions | Modifies decay rate via Heat thresholds | Heat > 0.8 doubles stability decay |
| **Evidence Economy** | signature, state transitions, entropy_bleed | N/A (one-way: portal generates evidence) | Every state transition generates evidence events |
| **Translation Gate** | bandwidth, stability, state | N/A (gate checks portal before allowing transit) | Gate refuses transit if stability < 0.3 or state != STABLE |
| **Faction AI** | signature (tracking), state (response triggers) | Factions may attempt stabilize/disrupt | NYPD responds to FORMING+, Strange monitors all states |
| **NPC Perception** | entropy_bleed radius, visual/audio effects | N/A | NPCs within bleed radius are affected by cognition modifiers |
| **Universe Profile** | physics profile modifies decay rates, bleed effects | N/A | Foreign universe physics may accelerate or slow portal decay |

### Event Bus Integration

Portal state transitions fire the following events on the global event bus:

```json
{
  "event_type": "portal.state_change",
  "portal_id": "unique_portal_entity_id",
  "signature": "64char_hex_hash",
  "previous_state": "FORMING",
  "new_state": "STABLE",
  "stability": 0.65,
  "bandwidth": 10.0,
  "entropy_bleed": 8.5,
  "anchor_id": "anchor_entity_id",
  "location": {"x": 234.5, "y": 0.0, "z": -112.3},
  "universe_id": "EARTH-1218",
  "target_universe_id": "EARTH-616",
  "timestamp": "sim_time_iso8601",
  "heat_impact": {
    "physical": 0.0,
    "social": 0.05,
    "institutional": 0.02,
    "ecological": 0.03
  },
  "evidence_generated": ["digital_sensor_log", "witness_visual"]
}
```

### Cross-Reference Documents

| Document | Relationship |
|---|---|
| `universe-profile-template-v0.md` | Universe physics profile modifies portal decay rates and bleed effects |
| `translation-gate-rules-v0.md` | Translation gate checks portal state and bandwidth before allowing item transit |
| `operations-library-v0.md` | Operations define portal requirements (stability, bandwidth, anchor) per mission |
| `heat-evidence-economy-spec-v0.md` | Portal events feed Heat channels and generate evidence entries |
| `faction-response-table-v0.md` | Faction responses are triggered by portal state transitions |

---

*End of Portal State Machine + Properties Spec v0*
