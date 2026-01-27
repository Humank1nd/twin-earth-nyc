# Vision Spec — Twin Earth NYC (Earth-1218 Hub)

**Project:** Twin Earth NYC — Multiverse GTA-Scale Simulation
**Document:** Part 1 Deliverable — Core Vision Specification
**Status:** Foundational / Locked
**Version:** 1.0

---

## Mantra

> **"Earth-1218 NYC is the grounded, persistent, audited reality bank — where Marvel is fiction, physics is law, and every consequence has a receipt."**

Everything in this project flows from that sentence. The hub world is not a theme park. It is a simulation of a real place governed by real rules, and the entire multiverse expansion model depends on players *trusting* that this ground truth is solid. If the foundation lies, nothing built on top of it matters.

---

## Three Non-Negotiables

These are the pillars that cannot be compromised, deferred, or approximated. If a feature, system, or content decision violates any of these three, it is rejected at the design level regardless of schedule or budget pressure.

### 1. Scale Truth (Real-World Metric Accuracy)

Every spatial measurement in the hub world corresponds to a verifiable real-world metric. Building heights, street widths, crosswalk lengths, sidewalk depths, lane counts, sign placements, and structural proportions are sourced from survey data, public GIS records, and photogrammetry. A player standing at 42nd and Broadway and looking south should see a skyline whose silhouette, proportional spacing, and depth layering match a photograph taken from the same position. Scale truth is not about polygon count — it is about the *feeling* that distances, heights, and spatial relationships are honest. When a player says "that building looks right," it is because it *is* right, within a tolerance of less than one meter at street level within the playable zone.

### 2. Consequence Persistence (Ledger Commits Are Irreversible)

Every meaningful state change in the simulation is written to the Trust Ledger as an immutable commit. Broken glass stays broken. Displaced objects remain displaced. Evidence collected by cameras, microphones, and NPC witnesses is stored and queryable. Heat accumulated by the player does not decay on reload — it decays on the simulation's own clock, governed by in-world systems (media cycle, police staffing, public attention span). There is no "undo." The player's relationship with the city is cumulative. The ledger is the city's memory, and the city does not forget unless there is a diegetic reason (evidence destroyed, witnesses silenced, records corrupted). Saves and loads interact with the ledger through a snapshot-and-replay model — loading a save replays the ledger up to the snapshot point, but the ledger itself is append-only. The emotional design goal: the player should feel *weight* behind every action because the city is always keeping score.

### 3. Sensor Realism (NPCs Perceive Only Through Sensors + Memory)

No NPC in the simulation has access to ground truth. Every NPC — pedestrian, police officer, vendor, security guard, cab driver — perceives the world exclusively through a defined sensor model: a vision cone with range, angle, and occlusion; an audio detection radius with falloff and masking; and a memory buffer with capacity, decay rate, and reliability score. An NPC who did not see or hear an event does not know about it unless another NPC or system (radio dispatch, news broadcast, surveillance feed) communicates that information through an in-world channel. This is the foundation of stealth, deception, reputation, and emergent narrative. If the player breaks a window and no sensor detects it, the simulation does not react — but the *ledger still records it*, because the ledger is not a sensor. The ledger is truth. Sensors are perception. The gap between truth and perception is where gameplay lives.

---

## Three Allowed Cheats

These are the sanctioned shortcuts — places where the simulation is permitted to simplify, approximate, or fake without violating the player's trust. Each cheat has a boundary condition: the point at which the simplification would become noticeable and must be upgraded.

### 1. Perceptual LOD (Distant Detail Can Simplify)

Objects, NPCs, and environmental detail beyond the player's immediate verification range (roughly 80-120 meters depending on context and line of sight) may use simplified geometry, reduced animation fidelity, and proxy textures. The boundary condition: if a player uses a scoped or zoomed view (binoculars, camera zoom, drone feed) to examine a distant object, the system must be capable of streaming in higher-detail assets within a perceivable but acceptable latency window (target: under 2 seconds). LOD transitions must never produce visible pop-in within the primary attention zone (roughly 40 meters). The emotional contract: "Everything close to you is real. Everything far away looks real. If you go check, it becomes real."

### 2. Proxy Skyline (Silhouette-Accurate but Simplified Beyond Verification Range)

The New York City skyline visible from the playable zone is rendered as a silhouette-accurate panoramic shell. Building outlines, relative heights, and iconic shapes (Empire State, Chrysler, One World Trade, Hudson Yards) are correct to within visual tolerance from any street-level vantage point within the hub. However, the actual geometry behind these silhouettes is not fully modeled — they are projection surfaces with baked lighting, parallax-corrected cubemaps, and time-of-day color grading. The boundary condition: if gameplay ever requires the player to physically travel to one of these skyline buildings, that building must be promoted from proxy to real geometry before the player arrives. The proxy skyline is a *promise* of a larger world, not a wall.

### 3. Implied Interiors (Most Doors Don't Open but Feel Alive)

The vast majority of buildings in the playable zone have sealed doors. However, sealed does not mean dead. Every sealed building emits ambient audio (HVAC hum, muffled conversation, music bleed, elevator mechanics), casts interior lighting through windows that shifts with time of day, and has window surfaces that show plausible interior silhouettes (furniture shapes, occasionally moving human shadows). Some sealed doors have interactable surfaces — the player can knock (producing NPC audio response), peer through glass (seeing a shallow parallax interior), or attempt forced entry (which is logged by the ledger and may trigger an alarm sensor). The boundary condition: any building that becomes narratively important must be promoted to a full interior. The implied interior system is a *queue* of potential real spaces, not a permanent fake. The emotional contract: "Every building has something behind the door. You just can't get to most of them yet."

---

## What Counts as Real

The simulation defines "real" through a three-part test. An event, object, or state is considered real if and only if it satisfies all three criteria:

| Test | Definition | Example |
|------|-----------|---------|
| **Physics Truth** | The event obeys the hub's physics rules (gravity, collision, material properties, energy conservation). | A thrown bottle follows a ballistic arc, shatters on impact with correct fragment spread, and produces audio at appropriate volume. |
| **Ledger Commitment** | The event's state change is written to the Trust Ledger as an immutable record with timestamp, location, involved entities, and causal chain. | The bottle's impact point, shatter pattern, fragment positions, and audio event are all recorded. |
| **Evidence Trail** | The event is, in principle, discoverable after the fact through the city's sensor network or physical residue. | A nearby camera captured the throw. Glass fragments remain on the ground. An NPC witness stored the audio event in memory. A cleaning crew will eventually be dispatched. |

If something passes the physics test but is not ledgered, it is a rendering artifact (visual only, no consequence). If something is ledgered but has no evidence trail, it is an abstract record (data only, no gameplay surface). If something has an evidence trail but violates physics, it is a bug. All three must align for the simulation to call it real.

---

## Canon Constraints

### The Marvel Rule

> **"Marvel is fiction in Earth-1218 until proven otherwise."**

In the hub world, Marvel Comics, Marvel movies, and Marvel merchandise exist as *entertainment products*. A newsstand sells comic books. A movie theater marquee advertises a Marvel film. A kid on the subway wears a Spider-Man t-shirt. But there is no Spider-Man swinging between buildings. There is no Avengers Tower on the skyline. There is no SHIELD helicarrier in the sky. The Marvel universe is cultural context, not physical reality — *until a portal opens and something from another universe enters the hub*. At that point, the event is treated as an anomaly: unprecedented, terrifying, and subject to the city's full response apparatus (police, media, military, public panic, government investigation). The tonal north star: imagine if a real alien appeared in real Times Square tomorrow. That is the reaction we are simulating.

### Ten Everyday NYC Systems That Must Feel Real

These ten systems form the baseline "alive city" layer. Each must be functional, observable, and reactive in the vertical slice. They are listed in priority order:

| # | System | What "Feels Real" Means |
|---|--------|------------------------|
| 1 | **Traffic** | Vehicles obey signals, respond to pedestrians, honk in gridlock, double-park, yield to emergency vehicles. Cab behavior is distinct from private vehicles. Delivery trucks block lanes on schedule. |
| 2 | **Cops** | NYPD patrol units follow beats, respond to dispatch calls, escalate based on threat level, write tickets, direct traffic at broken signals, and cluster at shift-change near precincts. Off-duty behavior differs from on-duty. |
| 3 | **Crowds** | Pedestrian density varies by time of day, day of week, weather, and local events. Tourists cluster at landmarks and move slowly. Commuters move fast and avoid eye contact. Crowd flow follows real sidewalk bottlenecks. |
| 4 | **Weather** | Rain, overcast, clear, humidity, wind direction and speed. Weather affects NPC behavior (umbrellas, pace changes, shelter-seeking), surface reflections, ambient audio, and visibility range. Forecast data drives a plausible multi-day cycle. |
| 5 | **Ads** | Digital billboards cycle content on schedule. Static billboards age and peel. Ad content reflects in-world brands, events, and cultural moments. The density, brightness, and visual noise of Times Square advertising is a landmark experience in itself. |
| 6 | **Noise** | Ambient soundscape is spatially accurate: traffic roar on avenues, relative quiet on side streets, subway rumble through grates, construction percussion, vendor calls, distant sirens, helicopter overflights. Audio occlusion through buildings is physically modeled. |
| 7 | **Construction** | Active construction sites with scaffolding, barriers, equipment, and workers on schedule. Construction changes traffic patterns, creates noise zones, and occasionally closes sidewalks. Sites persist and (very slowly) progress. |
| 8 | **Commerce** | Shops open and close on schedule. Vendors set up and break down. Customers enter and exit with purchased items. Cash registers ring. Delivery cycles are visible (morning restocking, evening trash). Economic activity has a rhythm. |
| 9 | **Transit** | Subway entrances emit audio and foot traffic. Buses follow routes on schedule (approximately — delays are realistic). Taxis respond to hails with contextual availability. Rideshare vehicles pull over unpredictably. Bike couriers weave through traffic. |
| 10 | **Surveillance** | Visible CCTV cameras on buildings, traffic cameras at intersections, police body cameras, dashcams, and civilian phones. The player can identify cameras, understand their coverage cones, and plan movement accordingly. Surveillance is a *gameplay system*, not a backdrop. |

### Player Fantasy

> **"Street-level agency in a city that remembers."**

The player is not a superhero. The player is not a soldier. The player is a person with skills, tools, knowledge, and growing connections operating at street level in a city that is vastly larger, more complex, and more powerful than they are. The fantasy is not domination — it is *navigation*. The player reads the city, finds the gaps, exploits the seams, builds leverage, and accumulates influence. The city pushes back with indifference, bureaucracy, law enforcement, and social pressure. The player's victories are earned through understanding, not firepower. And every victory and every mistake is recorded, permanently, in a city that never stops watching.

---

## Scope Guardrails

### Minimum Playable Geography: The Times Square Bowtie

The vertical slice geography is the Times Square "bowtie" — the intersection zone where Broadway crosses 7th Avenue diagonally, creating the distinctive triangular plazas.

**Boundaries:**
- **North:** 47th Street (hard boundary with proxy skyline beyond)
- **South:** 42nd Street (hard boundary with proxy 42nd Street corridor beyond)
- **West:** 7th Avenue west sidewalk (hard boundary with proxy midblock beyond)
- **East:** Broadway east sidewalk (hard boundary with proxy midblock beyond)

This zone is approximately 5 blocks long and 1-2 blocks wide, encompassing roughly 0.15 square kilometers of playable, fully realized urban space. Within this zone, every surface, object, sign, signal, and NPC is operating at full simulation fidelity.

### Five Landmark Invariants

These five spatial facts are immutable. They are the geodetic anchors of the hub world. If any of these are wrong, the entire sense of place collapses. They are verified against survey data and photogrammetry and locked before any other content is placed.

| # | Invariant | Specification |
|---|-----------|--------------|
| 1 | **One Times Square Height and Silhouette** | The triangular wedge building at the south end of the bowtie. Height: 110.6 meters (363 feet) to roof. The iconic silhouette — narrow wedge tapering to a point — must be accurate from all street-level views within the playable zone. The LED billboard facades wrap the building and are a primary visual landmark. |
| 2 | **TKTS Red Steps Position and Scale** | The TKTS booth and red glass staircase structure sits in the northern triangle of the bowtie (Father Duffy Square). The steps rise approximately 4.9 meters (16 feet) above plaza level, span approximately 27 meters wide, and face south toward One Times Square. They serve as a natural elevated vantage point and crowd gathering area. Their exact position relative to the George M. Cohan statue and the Duffy statue must be correct. |
| 3 | **Broadway / 7th Avenue Intersection Geometry** | The diagonal crossing of Broadway and 7th Avenue creates the bowtie's distinctive geometry. The acute angle of intersection (~10-12 degrees from parallel), the resulting triangular pedestrian plazas, and the complex traffic signal patterns at 42nd, 43rd, 44th, 45th, 46th, and 47th Streets must be geometrically accurate. This is the most complex intersection geometry in the playable zone and defines the entire navigational feel. |
| 4 | **Marriott Marquis Signage Zone** | The New York Marriott Marquis at 1535 Broadway (between 45th and 46th Streets) occupies a massive footprint on the east side of Broadway. Its facade features one of the largest digital signage installations in Times Square. The signage zone — its height, width, curvature, and position relative to the street — is a dominant visual element when looking north on Broadway. The hotel's entrance canopy and the pedestrian experience at its base must be spatially accurate. |
| 5 | **42nd Street Corridor Width** | The 42nd Street corridor at its intersection with the bowtie is the southern gateway to Times Square. The street width (curb to curb approximately 18.3 meters / 60 feet), sidewalk widths (variable, 3-6 meters), and the canyon-like proportion created by the buildings on either side must be accurate. This corridor is the primary east-west movement axis and the transition zone between Times Square and the rest of Midtown. |

### Hub Return-to-Home Feeling

> **"After the multiverse's chaos, Times Square is the place where the rules work, the cameras watch, and the damage stays."**

This is the emotional design target for the hub-return experience. When a player exits a portal and re-enters the hub, they should feel three things simultaneously:

1. **Relief** — Physics works normally again. Gravity pulls down. Walls are solid. Time flows forward. The rules are predictable and trustworthy.
2. **Exposure** — The city's surveillance and social systems are immediately active. Cameras are watching. NPCs are reacting. Heat is accumulating. The player is no longer in a pocket dimension where the rules are negotiable — they are in a panopticon that records everything.
3. **Weight** — Whatever happened in the portal pocket — damage dealt, objects taken, energy expended — has persistent consequences in the hub. The artifact in the player's inventory is generating a sensor signature. The evidence of portal transit is logged. The factions aware of multiverse activity are updating their models. Nothing was free.

The hub is not a safe zone. It is a *real* zone. That is why the player keeps coming back to it, and that is why it matters.

---

*End of Vision Spec — Part 1 Deliverable*
