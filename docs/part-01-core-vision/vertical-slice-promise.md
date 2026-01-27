# Vertical Slice Promise — Twin Earth NYC (Times Square Proof of Concept)

**Project:** Twin Earth NYC — Multiverse GTA-Scale Simulation
**Document:** Part 1 Deliverable — Vertical Slice Promise
**Status:** Foundational / Locked
**Version:** 1.0

---

## The Promise

The Times Square vertical slice is the proof that this project works — technically and emotionally. Technically, it demonstrates that the full-stack architecture (Truth Engine, Illusion Engine, Trust Ledger, IoT artifact system, NPC sensor-based realism, Heat accumulation model, anomaly detection pipeline, and portal traversal framework) can run simultaneously in a single contiguous space without compromise: physics is honest, consequences are recorded, NPCs perceive through sensors and not omniscience, the city's surveillance apparatus watches and remembers, portals obey their own rules, and every system talks to every other system through the ledger. Emotionally, it proves something harder to quantify but immediately recognizable: this city *feels alive*. The crowds have rhythm. The traffic has frustration. The cops have jurisdiction. The cameras have blind spots. And when the sky cracks open and something impossible bleeds through from another universe, the city does not shrug — it reacts with the full weight of ten million people's institutional machinery, from the 911 dispatcher to the cable news helicopter, and the player stands at the center of that reaction knowing that what just happened is *permanent*, recorded, and will have consequences that ripple through every session that follows.

---

## Success Metric

> **"If we can run a 5-minute loop — walk through crowds, trigger an anomaly, watch authorities respond, enter a portal pocket, complete an objective, return to hub with persistent consequences — then we can scale to Manhattan and beyond."**

This is the atomic test. Five minutes. One player. One city block. One anomaly. One portal. One objective. One return. If the loop holds — if every system fires, every consequence lands, every NPC reacts through its sensor model, every state change hits the ledger, and the player *feels it* — then the architecture is proven. Everything after that is content, geography, and scale. The hard problem is the loop. The loop is what we are building first.

### The 5-Minute Loop, Step by Step

| Time | Action | Systems Engaged |
|------|--------|----------------|
| 0:00-0:30 | Player walks south through Father Duffy Square. Crowds part naturally. A taxi honks. A cop on the corner checks their phone. | Crowd flow, traffic, NPC sensors, ambient audio |
| 0:30-1:00 | Player passes a CCTV camera. A subtle UI indicator confirms they are in frame. A street vendor calls out. The TKTS line shuffles forward. | Surveillance system, NPC commerce AI, crowd queue behavior |
| 1:00-1:30 | Player reaches 44th Street. A sensor anomaly triggers — the player's phone (or wrist device) vibrates. Nearby, a 10m radius zone shows faint gravitational distortion: trash lifts slightly, a coffee cup slides across a ledge, a pigeon's flight path curves wrong. | Anomaly detection, physics truth (localized gravity modification), IoT device notification, environmental object interaction |
| 1:30-2:00 | NPCs within sensor range react. Nearby pedestrians stop, point, back away. A tourist films with their phone. A cop 50m away hears a radio dispatch and begins moving toward the anomaly. Two blocks out, another patrol car's dashboard camera catches the light distortion. | NPC sensor-based perception, crowd fear/curiosity response, police dispatch chain, CCTV anomaly detection, radio communication propagation |
| 2:00-2:30 | The anomaly intensifies. A portal aperture opens in an alley off 44th Street — a shimmering vertical tear, 2m tall, emitting a low hum and a faint otherworldly light. Entropy bleed radius: 5m. Within the bleed zone, colors shift slightly and the player feels lighter (gravity reduced 10%). | Portal instantiation, entropy bleed physics, audio design, visual effects, signature emission |
| 2:30-3:30 | Player enters the portal. Transition: a 1.5-second traversal through a translation membrane. On the other side: a single room — an alien space, architecturally impossible, lit by bioluminescent surfaces. A pedestal holds an artifact (a crystalline object pulsing with energy). The room has one hostile entity (guardian) and one environmental hazard (unstable floor section). Player defeats or evades the guardian, grabs the artifact. | Portal traversal, translation gate processing, pocket zone loading, destination physics profile, combat/stealth systems, inventory acquisition, environmental hazard |
| 3:30-4:00 | Portal stability drops to 0.2. Warning: instability spike. The room shakes. The player sprints for the portal. Translation gate processes the artifact (compatibility: 0.6 — moderate decay, detectable signature trace). Player exits into the alley. The portal enters collapse sequence behind them. | Stability decay, instability warning, time pressure, translation gate compatibility check, portal collapse Phase 1-2, evidence burst |
| 4:00-5:00 | Player emerges in the alley. The portal collapses with an energy burst detectable two blocks out. Residue patch remains. The artifact in the player's inventory is emitting a faint signature. Two cop cars are now at 44th Street, lights on. A news van is pulling up. Three civilian phones have uploaded footage. The player's Heat has increased by two levels. A faction (unnamed in the slice — represented by a figure watching from a rooftop) notes the event. The player walks away through the crowd, artifact hidden in a bag, cameras tracking, sirens behind them. The ledger records: anomaly event, portal open, portal traversal, artifact extraction, portal collapse, evidence burst, authority response, media response, Heat increase, faction observation. All persistent. All permanent. All queryable. | Post-portal consequence cascade, Heat system, evidence accumulation, authority response escalation, media system, faction awareness, surveillance tracking, ledger commit sequence, artifact signature detection, crowd/traffic disruption |

---

## Minimum Hub Systems

These are the systems required to make the Times Square hub feel alive and functional before any anomaly or portal content is triggered. Classified by priority tier.

### Must-Have (Required for Vertical Slice)

**Walkability**
The player can walk, jog, and sprint through the bowtie zone with physically accurate movement. Collision with all surfaces, objects, NPCs, and vehicles is resolved correctly. Sidewalks, crosswalks, plazas, curbs, steps, and street surfaces have distinct traversal properties (walking speed on stairs differs from flat ground; crossing against traffic is dangerous; crowd density affects movement speed). The player can: step off curbs, cross streets, navigate around obstacles, ascend the TKTS Red Steps, lean against walls, and duck into alleys. Movement is the foundation — if walking doesn't feel right, nothing else matters.

**Traffic Signals**
All traffic signals in the bowtie zone operate on realistic timing cycles. Pedestrian walk/don't-walk signals function. Vehicles stop on red, proceed on green, and turn on protected arrows. Signal timing affects pedestrian crossing windows, traffic density, and gridlock patterns. Emergency vehicles trigger signal preemption (all lights change to allow passage). Broken signals (a later game event) cause intersection chaos. Signals are observable, predictable, and exploitable — the player can learn the timing and use it.

**Crowd Flow**
Pedestrians populate the bowtie zone at density levels corresponding to time of day (sparse at 3 AM, packed at 6 PM on a Friday). Pedestrian movement follows plausible paths: commuters walk with purpose on predictable routes; tourists cluster, stop, and photograph; vendors remain stationary at their posts; homeless individuals occupy consistent spots. Crowd density affects the player's movement speed, visibility to cameras, ability to be followed, and noise level. Crowds react to events: an anomaly draws gawkers and repels the cautious; a police siren causes heads to turn; a sudden noise causes a ripple of flinching. Crowd members are individual NPCs with sensor models — they see, hear, and remember within their individual capabilities.

**CCTV and Evidence System**
A minimum of 15-20 operational CCTV cameras are placed at real-world positions within the bowtie zone (intersection cameras, building-mounted security cameras, ATM cameras). Each camera has a defined field of view, resolution, and recording status. The player can identify cameras visually and, with appropriate equipment, detect their coverage zones. Camera feeds are recorded to the Trust Ledger — any event occurring within a camera's field of view is evidenced. The evidence system also encompasses: civilian phone recordings (NPCs may film unusual events), police body cameras (officers on scene have active recording), and dashcams (patrol vehicles and taxis). The player's awareness of the evidence system is a core gameplay skill: knowing what is recorded, what is not, and how to operate in the gaps.

**Lighting and Time of Day**
The hub operates on a 24-hour cycle with accurate sunrise/sunset times, sun angle, and shadow casting for the Times Square latitude/longitude. Artificial lighting activates at dusk: streetlights, traffic signals, building interior lights, and — critically — the Times Square billboard and LED displays, which are the dominant light source at night. Time of day affects: NPC population density, traffic volume, store open/close status, police patrol patterns, ambient audio mix, and visual atmosphere. The lighting system is not just aesthetic — it affects gameplay through visibility, shadow cover, and the dramatic difference between daytime and nighttime operations.

### Nice-to-Have (Enhanced Experience, Not Blocking)

**Sound Design**
Full spatial audio with distance attenuation, occlusion through buildings, reflection off hard surfaces, and Doppler shift on moving vehicles. The Times Square soundscape is layered: traffic baseline, crowd murmur, construction percussion, subway rumble, advertising audio bleed, emergency sirens, street performer music, vendor calls, and the distinct acoustic signature of the bowtie's canyon geometry. Sound affects NPC sensor models — a loud event masks quieter ones; operating during a construction noise window reduces audio detection range for all entities.

**Weather**
Dynamic weather system with rain, overcast, clear, wind, and temperature variation. Weather affects: surface reflections (rain creates puddles and wet-road reflections), NPC behavior (umbrellas, faster walking, shelter-seeking), visibility range (fog, rain reduce camera and NPC visual range), and ambient audio (rain adds a broadband noise layer that masks footsteps). Weather follows plausible multi-day patterns rather than random cycling.

### Later Phase (Not in Vertical Slice)

**Full Interiors**
Building interiors beyond the implied interior system (ambient audio, window lighting, parallax glimpses). Full interiors include: navigable floor plans, interior NPCs, commerce interactions, security systems, and interior-to-exterior sightlines. Full interiors are expansion content — each opened interior is a significant content investment and is prioritized based on narrative and gameplay need. The vertical slice may include 1-2 shallow interiors (a lobby, a shop) as stretch goals, but no full multi-floor interiors.

---

## First Anomaly

> **"A localized gravity wobble in a 10-meter radius near 44th Street — visible distortion, sensor spike, crowd reaction, authority dispatch."**

### Specification

- **Location:** Sidewalk on the east side of Broadway between 44th and 45th Streets, centered approximately 15 meters north of the 44th Street crosswalk.
- **Radius:** 10 meters from center point.
- **Effect:** Gravity within the radius is reduced by 15-25% (variable, pulsing). Objects not secured to surfaces drift upward slightly: litter, loose papers, a coffee cup on a ledge, a vendor's hat. Heavier objects (trash cans, newspaper boxes) shift and scrape. Pedestrians within the radius feel lighter and stumble; some are lifted slightly on their toes. The visual effect is subtle but unmistakable — a shimmer in the air, like heat haze but geometric, and the uncanny sight of objects defying gravity in the middle of Manhattan.
- **Audio:** A low-frequency hum at the center, rising in pitch toward the edges. A faint crackling, like static discharge. Objects scraping against surfaces as they shift.
- **Duration:** 45-90 seconds before the anomaly either dissipates (no portal) or intensifies into a portal opening (scripted path for the vertical slice).
- **Sensor detection:** IoT devices within 100 meters register a gravitational anomaly reading. CCTV cameras within line of sight capture the visual distortion. NPC phones within 30 meters may trigger automatic "unusual event" recording.
- **NPC reaction:** Pedestrians within the radius: immediate startled reaction, then either flee (70%) or freeze and stare (20%) or film with phone (10%). Pedestrians outside the radius but within visual range: stop and look, point, begin clustering at a safe distance. Police NPCs: if within 100 meters, dispatch receives anomaly alert and nearest officer moves to investigate. If no officer is nearby, dispatch assigns a patrol car (arrival in 2-4 minutes depending on traffic).
- **Player interaction:** The player can walk into the anomaly radius and experience the gravity reduction directly (movement changes — higher jumps, floatier steps, objects can be thrown farther). The player can use a scanner device to read the anomaly's signature, which provides information about the potential portal and its likely origin universe.

---

## First Portal Pocket

> **"A single-room off-world space accessible through an alley portal — extract one artifact, return with evidence spike + Heat bump + faction interest."**

### Specification

- **Portal location:** An alley between two buildings on the west side of 44th Street, approximately 20 meters from the anomaly center. The portal manifests as a vertical tear in space, roughly 2 meters tall and 1 meter wide, shimmering with the destination universe's color palette.
- **Portal properties:** Stability 0.6 (decaying at 0.02/second — roughly 30 seconds of safe operation), bandwidth 100 kg/s (fast human transit), anchor bound to a cracked section of the alley wall, signature traceable to an unknown origin universe, entropy bleed radius 5 meters (within the alley, contained by the building walls — minimal street-level visibility).
- **Pocket zone interior:** A single room, approximately 15m x 10m x 8m. Architecture: non-Euclidean angles, surfaces that appear organic but are rigid (bioluminescent walls, a floor that pulses faintly underfoot, a ceiling that seems to breathe). Physics: gravity reduced 20%, slightly increased friction, ambient temperature cold. Audio: a distant, rhythmic thrumming; faint whispers at the edge of perception; echo behavior inconsistent with room geometry.
- **Objective:** A crystalline artifact sits on a raised pedestal at the room's far end. The artifact is the extraction target. It is approximately 2 kg, emits a visible energy pulse every 3 seconds, and has a compatibility score of 0.6 (will decay slowly in the hub, emits detectable signature, functions in an altered/reduced capacity).
- **Opposition:** A single guardian entity — humanoid, 2.5 meters tall, slow-moving but powerful, with limited sensory range (primarily motion-detection, narrow visual cone, no audio perception). It patrols a circuit around the pedestal. The player can engage it directly (difficult, resource-intensive) or evade it using the room's geometry and the guardian's sensor limitations (stealth approach — rewarded with lower Heat on return due to less evidence of violence).
- **Environmental hazard:** A section of the floor (approximately 4m x 3m) between the entrance and the pedestal is structurally unstable. Stepping on it causes cracks that spread over 2 seconds; full collapse after 4 seconds, dropping the player into a sub-level that requires climbing back up (time cost — critical when stability is decaying). The hazard is visually signaled (different surface texture, faint cracks) but not explicitly called out.
- **Exit:** The same portal used for entry. The player must physically return to the portal aperture and traverse back. If the portal collapses while the player is inside, an emergency ejection triggers: the player is expelled back to the hub at the portal's former location, suffering translation damage (temporary status effects — disorientation, inventory scramble, minor health loss) and generating a massive evidence burst.

### Return Consequences

- **Evidence spike:** The portal collapse (or controlled exit) generates an energy burst detectable within a 200-meter radius. All cameras, sensors, and NPC phones in range capture the event. The alley residue patch will be detectable for 24 in-game hours.
- **Heat bump:** The player's Heat level increases by 2 tiers (out of a 10-tier system). At this Heat level, police and surveillance systems are on moderate alert for anomalous activity. The player is not yet a suspect, but the city is looking for explanations.
- **Faction interest:** One faction (represented in the vertical slice by a single NPC observer — a figure on a rooftop or in a window, visible but not interactable) registers the event and begins tracking the player. This faction interest persists into future sessions and seeds the longer narrative.
- **Artifact in inventory:** The crystalline artifact is now a persistent object in the player's possession. It emits a signature trace detectable by sensors within 5 meters. It pulses visually every 3 seconds (concealable in a bag, but not suppressible). It has a function that will be revealed in later content. Its decay rate (compatibility 0.6) means it will degrade to non-functionality in approximately 72 in-game hours unless the player finds a stabilization method.

---

## Hub Loop Without Portals

> **"Explore, observe, interact with the city's systems — cross streets, evade cameras, force doors, gather evidence, build reputation — and feel the city push back."**

The hub world is not a portal waiting room. It is a complete gameplay experience. A player who never triggers an anomaly or enters a portal should still find dozens of hours of engaging, emergent gameplay in the Times Square bowtie. The hub loop is built on five interlocking activities:

1. **Explore** — Learn the geography, identify landmarks, discover alleys and corners and vantage points. Map the camera network. Time the traffic signals. Learn which buildings have accessible rooftops, which alleys connect, which doors are locked but forcible, which fences can be climbed. The city is a puzzle box, and knowledge of its layout is the first resource.

2. **Observe** — Watch NPCs. Learn their routines, their patrol patterns, their shift changes, their habits. Identify which cop always checks their phone at 2:15 PM (creating a 30-second window). Notice which vendor leaves their cart unattended during bathroom breaks. Track which cameras go offline during maintenance. Information is power, and the hub rewards patience and attention.

3. **Interact** — Engage with city systems. Cross streets strategically (jaywalking triggers potential detection; using crosswalks is slow but safe). Enter shops and make purchases (building commerce relationships). Talk to NPCs (gathering information, building reputation, creating witnesses). Use phones and devices (scanning, recording, communicating). Force doors (creating noise, triggering alarms, committing ledger events). Every interaction has a footprint.

4. **Build** — Accumulate resources, knowledge, and relationships. Craft devices from purchased or scavenged components. Upgrade sensor equipment. Establish safe houses (rented rooms with reduced surveillance). Build faction standing through favors, information trades, and mission completion. Develop the player character's capability and infrastructure.

5. **Manage** — Handle Heat, evidence, and consequences. When Heat is high, lay low — change routes, avoid cameras, stay indoors. When evidence accumulates against the player, take countermeasures — find and destroy recordings, discredit witnesses, create alibis. When faction relationships shift, adapt — a faction betrayed becomes an enemy; a faction served becomes an ally. The city's memory is the player's ongoing management challenge.

---

## Portal Operation Loop

The full portal operation is a seven-phase loop that begins and ends in the hub. Each phase engages different systems and requires different skills.

### Phase 1: Preparation (Hub)

Gather gear, intel, and resources in NYC. Purchase or craft equipment suited to the target universe's known conditions. Consult faction contacts for intelligence on the destination. Identify and prepare a portal site — scout the location, verify camera coverage, plan approach and exit routes. Optionally: pre-position a stabilization device or arrange faction support. Preparation time varies from minutes (emergency response to an active anomaly) to hours (planned infiltration of a known universe).

### Phase 2: Insertion (Portal)

Enter through the stabilized portal. The translation gate processes the player and all carried equipment — compatibility scores are applied, signature traces are imprinted, bandwidth is consumed. The transition is physically felt: a 1-2 second traversal through a disorienting membrane where both universes overlap. On the other side, the destination universe's physics assert themselves. Equipment that was reliable in the hub may behave differently. The player's senses adjust to new light, sound, gravity, and atmosphere.

### Phase 3: Objective (Destination)

Execute the mission verb — extract, contain, or infiltrate. Navigate the destination environment, which has its own rules, hazards, inhabitants, and sensor systems. Engage or evade opposition. Locate and secure the target (object, data, entity, or breach point). Every action in the destination is governed by that universe's physics profile and cognition profile. The player's hub-world skills and equipment may be advantaged, disadvantaged, or irrelevant depending on translation compatibility.

### Phase 4: Complication (Destination)

Something goes wrong. This is not optional — every portal operation includes at least one complication. Common complications: stability spike (sudden decay acceleration — timer shortens), unexpected opposition (reinforcements, alarm triggers, environmental shift), equipment failure (low-compatibility gear degrades mid-mission), secondary objective discovery (something unexpected and valuable that tempts the player to stay longer), or portal anchor disruption (the hub-side anchor is threatened by authorities or factions, and the player receives a warning that their exit may close).

### Phase 5: Exfiltration (Portal)

Return to the portal before collapse. This phase is always time-pressured — the complication has shortened the window, and the player must make tactical decisions: abandon secondary objectives to ensure extraction, or risk staying longer for greater reward. The portal's instability is visible and audible — the player can gauge remaining time by observing the portal's condition. Traversal back through the translation gate processes any acquired items (compatibility scores applied, bandwidth consumed). If the player is carrying mass that exceeds remaining bandwidth, they must shed items or accept stability damage.

### Phase 6: Aftermath (Hub — Immediate)

The player exits into the hub. The portal collapses behind them (or is deliberately sealed). The evidence burst radiates outward. Sensors detect. NPCs react. Authorities mobilize. The player must immediately manage their situation: conceal evidence, evade surveillance, blend into crowds, reach a safe house. The immediate aftermath is a stealth/evasion challenge in a city that is actively searching for the source of the disturbance.

### Phase 7: Consequences (Hub — Persistent)

The long-term results resolve over the following in-game hours and days. Heat level adjusts based on evidence accumulation. Faction relationships update based on mission outcome (Did the player serve a faction's interests? Oppose them? Reveal information they wanted hidden?). The extracted artifact or completed objective has ongoing effects — it may attract attention, enable new capabilities, or trigger follow-up events. Media coverage of the anomaly event shapes public awareness. The player's reputation evolves. The ledger records everything, and the city's institutional memory incorporates the new data. The next portal operation will begin in a city that has been changed by this one.

---

## Five Persistence Requirements

These five requirements define the minimum persistence standard. If any of these fail, the vertical slice has not achieved its architectural proof.

### 1. Physical Damage Persists

Broken objects stay broken. A shattered window does not repair itself. A dented car remains dented. A cracked sidewalk retains its crack. Displaced objects (knocked-over trash cans, scattered papers, moved furniture) remain in their new positions. Damage is not cosmetic — it is a physical state change committed to the Trust Ledger with timestamp, location, cause, and causal entity. A player who breaks a window and returns 48 in-game hours later will find that window still broken (or repaired by an in-world maintenance system, which itself is a ledgered event — a work order dispatched, a repair crew arrived, materials consumed, window replaced). The city does not quietly reset. It either stays damaged or is visibly repaired by a system that itself has a paper trail.

### 2. Evidence Accumulates in the Ledger

Every event detected by any sensor — camera, microphone, NPC witness, IoT device, player scanner — generates an evidence record in the Trust Ledger. Evidence records are append-only: they cannot be deleted, only supplemented with later records (contradicting evidence, witness recantation, footage analysis). The evidence record includes: event type, timestamp, location, involved entities, sensor source, confidence score (eyewitness < camera footage < direct sensor reading), and cross-references to related records. Over time, the ledger accumulates a comprehensive history of every significant event in the hub. This history is queryable by game systems (police investigation AI, faction intelligence, media reporting) and, with appropriate tools, by the player. The ledger is the city's memory, and it grows with every session.

### 3. Heat Level Carries Across Sessions

The player's Heat level is a persistent integer that survives save/load, session boundaries, and game exits. Heat is modified by events (criminal activity increases Heat, laying low decreases it, evidence accumulation increases it, counter-evidence decreases it) and decays on the simulation's own clock (not the player's real-time clock — Heat decays during simulated time, whether the player is present or not). When the player loads a save, the simulation fast-forwards Heat decay to the current simulation time. Heat level affects: police alertness toward the player, surveillance system sensitivity, faction willingness to interact, NPC ambient awareness (at high Heat, civilians may recognize the player from news coverage), and available missions (some missions require low Heat; others require high Heat as proof of capability).

### 4. Reputation with Factions Persists

The player's standing with each faction is a persistent floating-point value that evolves based on actions, mission outcomes, and narrative choices. Faction standing affects: mission availability, NPC dialogue, resource access, safe house availability, and the faction's active posture toward the player (allied, neutral, hostile). Faction standing changes are committed to the Trust Ledger with causal attribution — the player (and the game systems) can trace exactly why a faction's attitude changed. Faction standing does not reset. A betrayed faction remains hostile until the player invests in reparation — and even then, the trust may never fully recover. Factions remember, and their memory is backed by the same ledger that remembers everything else.

### 5. Device Logs Are Queryable After the Fact

Every IoT device, sensor, camera, and player-owned electronic device in the simulation maintains a log of its recorded events. These logs are persistent and queryable. A player who planted a scanner near a portal site three sessions ago can return and download the scanner's log, retrieving every sensor event it recorded during the intervening time. A CCTV camera's footage is stored and accessible (with appropriate hacking tools or legal authority) for a configurable retention period (default: 72 in-game hours). Police radio dispatch logs, traffic camera archives, cellphone tower records — all are data stores that accumulate over time and are, in principle, accessible. The simulation does not have a "fog of war" that erases history — it has an "archive of everything" that rewards the player for knowing how to query it.

---

## Closing Statement

The vertical slice is not a demo. It is not a proof of concept for investors. It is the project's first *real moment* — the first time the architecture runs end to end, the first time the city breathes, the first time a portal opens, the first time the ledger records something that matters. If the 5-minute loop works, the next five years of development have a foundation. If it doesn't, we will know exactly why, because the ledger will have recorded every failure with the same fidelity it records every success.

Build the loop. Trust the ledger. Let the city remember.

---

*End of Vertical Slice Promise — Part 1 Deliverable*
