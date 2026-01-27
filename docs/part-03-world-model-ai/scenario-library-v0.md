# Scenario Library v0 — Times Square Stress Scenarios

> **Series:** Twin Earth NYC — Part 3: World Model & AI
> **Document:** `scenario-library-v0.md`
> **Status:** Draft v0
> **Last Updated:** 2026-01-27
> **Depends On:** `proposal-spec-v0.md`, Part 1 (Truth Anchors), Part 2 (Ledger & Evidence)

---

## 1. Overview

This document defines 20 stress scenarios for Times Square simulation testing. Each scenario is designed to push specific subsystems to their limits and expose failure modes before they reach players.

Five scenarios are selected for the v1 milestone. All 20 are available for regression testing and future milestone planning.

A **scenario runner** interface spec is included at the end, defining how scenarios are loaded, executed, measured, and replayed.

---

## 2. Scenario Catalog — All 20 Scenarios

### Summary Table

| # | Scenario Name | Severity | Affected Systems | v1 Selected |
|---|--------------|----------|-----------------|-------------|
| 1 | Baseline Midday | 1 | All (nominal) | **YES** |
| 2 | Rainstorm | 3 | lighting, crowds, traffic, audio, devices | **YES** |
| 3 | Parade | 4 | traffic, crowds, cops, audio | |
| 4 | Blackout | 5 | lighting, traffic, crowds, audio, devices, cops | **YES** |
| 5 | Protest March | 4 | crowds, traffic, cops, audio | |
| 6 | Vehicle Accident | 3 | traffic, crowds, cops, audio | |
| 7 | Portal Panic | 5 | anomaly, crowds, cops, lighting, audio, devices | |
| 8 | Construction Closure | 2 | traffic, crowds | |
| 9 | Celebrity Sighting | 2 | crowds, traffic, cops | |
| 10 | Fire Alarm Evacuation | 4 | crowds, traffic, cops, audio | |
| 11 | Subway Disruption | 3 | crowds, traffic | |
| 12 | Police Chase | 4 | traffic, crowds, cops, audio | **YES** |
| 13 | Street Performer Crowd | 2 | crowds, traffic, audio | |
| 14 | New Year's Eve Density | 5 | crowds, traffic, cops, lighting, audio, devices | |
| 15 | Summer Heat Wave | 2 | crowds, lighting, audio | |
| 16 | Snowstorm | 4 | traffic, crowds, lighting, audio | |
| 17 | Gas Leak | 4 | crowds, traffic, cops, audio | |
| 18 | Drone Swarm Sighting | 3 | crowds, cops, audio, devices, anomaly | |
| 19 | Billboard Malfunction Cascade | 3 | lighting, devices, crowds, audio | |
| 20 | Tourist Bus Blockage | 2 | traffic, crowds | |
| 21 | Anomaly Shimmer at Intersection | 5 | anomaly, traffic, crowds, cops, lighting, audio, devices | **YES** |

> **Note:** Scenario 21 is the anomaly shimmer scenario. It was listed as item 20 in the design brief but added as #21 here because "tourist bus blockage" was also specified. Both are included.

---

### Scenario Details

---

#### Scenario 01: Baseline Midday
**v1 SELECTED**

| Field | Value |
|-------|-------|
| **Severity** | 1 (Nominal) |
| **Affected Systems** | All — at normal operating levels |
| **Description** | Standard midday conditions in Times Square. Moderate pedestrian density (60-70% of capacity), normal vehicle traffic flow, all billboards operational, clear weather, standard ambient audio. This is the control scenario against which all stress tests are compared. |
| **Setup Parameters** | Time: 12:30 PM. Weather: clear, 72F. Crowd density: 65%. Traffic: normal signal timing. All systems nominal. |
| **Success Criteria** | All 8 baseline metrics pass. This scenario defines the reference values. |
| **Key Measurements** | Establish baseline FPS, memory usage, crowd flow rates, traffic throughput. |
| **Duration** | 10 minutes sim-time |

---

#### Scenario 02: Rainstorm
**v1 SELECTED**

| Field | Value |
|-------|-------|
| **Severity** | 3 (Moderate) |
| **Affected Systems** | Lighting, crowds, traffic, audio, devices |
| **Description** | Heavy rainstorm hits Times Square. Wet surface reflections activate on all roads and sidewalks. Pedestrians seek shelter under awnings and building overhangs, causing localized crowd compression. Traffic slows 30%. Billboard reflections intensify. Umbrella props spawn on 60% of NPCs. Audio layer shifts to rain ambience with thunder stingers. Street-level visibility reduced. |
| **Setup Parameters** | Time: 2:00 PM. Weather: heavy rain, 58F, wind 15mph from NW. Crowd density: 50% (reduced from baseline, but compressed under cover). Traffic speed modifier: 0.7x. Surface wetness: 1.0. |
| **Stress Targets** | Reflection shader performance. Crowd pathfinding under shelter-seeking behavior. Wet surface material swaps on all ground planes. Particle system budget (rain + splashes). Audio occlusion changes under awnings. |
| **Failure Modes to Watch** | Crowd deadlocks at shelter points. Rain particles obscuring UI. Reflection rendering dropping FPS below floor. NPCs walking through each other at compressed shelter zones. Puddle reflections showing wrong billboard content. |
| **Duration** | 10 minutes sim-time (storm onset at T+60s, peak at T+180s, steady through end) |

---

#### Scenario 03: Parade

| Field | Value |
|-------|-------|
| **Severity** | 4 (High) |
| **Affected Systems** | Traffic, crowds, cops, audio |
| **Description** | A parade procession moves south on Broadway through Times Square. Broadway is fully closed to vehicle traffic from 47th to 42nd. Police barriers line the route. Spectator crowds build 8-deep at barriers. Cross-traffic on 44th, 45th, and 46th is rerouted. Parade floats, marching bands, and performers generate extreme audio levels and visual spectacle. |
| **Setup Parameters** | Time: 11:00 AM. Broadway: closed 47th-42nd. Parade entities: 12 float objects + 200 marcher NPCs. Spectator density: 95% at barriers, 40% elsewhere. Police barrier entities: 48 units. Cross-traffic: diverted to 8th/6th Ave. |
| **Stress Targets** | Massive NPC count (baseline + 200 marchers + compressed spectators). Traffic rerouting under full road closure. Audio mixing with marching band sources. Large-entity physics (parade floats). Barrier collision accuracy. |
| **Failure Modes to Watch** | Spectator NPCs phasing through barriers. Traffic pathfinding failure on reroute. Parade floats clipping buildings. Audio distortion from overlapping band sources. Crowd deadlock at cross-street chokepoints. |
| **Duration** | 15 minutes sim-time |

---

#### Scenario 04: Blackout
**v1 SELECTED**

| Field | Value |
|-------|-------|
| **Severity** | 5 (Critical) |
| **Affected Systems** | Lighting, traffic, crowds, audio, devices, cops |
| **Description** | Total power failure across Times Square. All billboards go dark simultaneously. Traffic signals fail, defaulting to flashing red (all-way stop). Street lights extinguish. Interior building lights cut out. Emergency generators activate on some buildings after 30-second delay (partial restoration). Crowd behavior shifts to confusion and phone-flashlight activation. Police redirect traffic manually. Vehicle headlights become primary illumination source. |
| **Setup Parameters** | Time: 9:30 PM (maximum visual impact). Power state: OFF at T+0. Emergency generators: 15% of buildings restore at T+30s. Billboard state: all dark. Traffic signals: flashing red. Crowd behavior: confusion mode (40%), phone-light mode (30%), shelter-seeking (20%), normal (10%). Police: traffic-directing behavior. |
| **Stress Targets** | Real-time lighting recalculation for entire scene. Dynamic light source management (hundreds of phone flashlights + vehicle headlights replacing static billboard illumination). NPC behavior tree mass-transition. Traffic system fallback to uncontrolled intersections. Audio shift to low-ambience emergency state. Shadow recalculation with removed emissive sources. |
| **Failure Modes to Watch** | Lighting system collapse (too many dynamic lights replacing baked billboard light). Complete darkness (no fallback illumination). Traffic AI failure at uncontrolled intersections causing gridlock. NPCs not reacting to darkness. Billboard textures showing through despite power-off state. Memory spike from lighting recalculation. |
| **Duration** | 10 minutes sim-time (blackout at T+0, partial restore at T+30s, full restore at T+480s) |

---

#### Scenario 05: Protest March

| Field | Value |
|-------|-------|
| **Severity** | 4 (High) |
| **Affected Systems** | Crowds, traffic, cops, audio |
| **Description** | An organized protest group of 500 NPCs marches east on 45th Street, turns south on 7th Avenue. Chanting audio, sign props, police escort. Counter-protesters gather at 44th and 7th. Traffic disrupted on affected streets. Police form cordon between groups. Bystander NPCs exhibit rubbernecking behavior, compressing sidewalk density. |
| **Setup Parameters** | Time: 3:00 PM. Marcher count: 500. Route: 45th St E to 7th Ave S. Counter-protest: 100 NPCs at 44th/7th. Police cordon: 30 officers. Crowd behavior: 60% curious, 25% avoiding, 15% joining. |
| **Stress Targets** | Large-group coordinated movement. NPC group coherence (marchers stay in formation). Police AI cordon behavior. Two opposed crowd groups with tension mechanics. Audio chanting synchronization. |
| **Failure Modes to Watch** | Marcher group losing coherence. Police cordon NPCs failing to form line. Counter-protest NPCs phasing through cordon. Traffic not yielding to march. Crowd compression causing physics explosions. |
| **Duration** | 12 minutes sim-time |

---

#### Scenario 06: Vehicle Accident

| Field | Value |
|-------|-------|
| **Severity** | 3 (Moderate) |
| **Affected Systems** | Traffic, crowds, cops, audio |
| **Description** | Two-vehicle collision at 7th Avenue and 45th Street. Vehicles stop in intersection, blocking two lanes. Debris props spawn. Crowd gathers to rubberneck. Emergency vehicles (police, ambulance) navigate through traffic to reach scene. Traffic reroutes around blocked intersection. NPCs near impact point exhibit flee/shock behavior. |
| **Setup Parameters** | Time: 4:30 PM (rush hour). Collision location: center of 7th/45th intersection. Blocked lanes: 2 of 4. Emergency response: T+90s (police), T+180s (ambulance). Debris radius: 8m. Crowd curiosity radius: 25m. |
| **Stress Targets** | Vehicle damage model and debris spawning. Emergency vehicle pathfinding through congested traffic. Crowd formation around incident. Traffic rerouting with partial intersection blockage. Audio impact sounds and siren propagation. |
| **Failure Modes to Watch** | Emergency vehicles unable to reach scene. Traffic deadlock from rerouting. Crowd NPCs walking through debris/vehicles. Rubbernecker crowd blocking emergency access. |
| **Duration** | 10 minutes sim-time |

---

#### Scenario 07: Portal Panic

| Field | Value |
|-------|-------|
| **Severity** | 5 (Critical) |
| **Affected Systems** | Anomaly, crowds, cops, lighting, audio, devices |
| **Description** | A major anomaly portal opens at the center of Duffy Square (TKTS steps area). Portal is 4m diameter, emits blue-white light, audible hum at 200m. Reality distortion effects within 15m radius — visual shimmer, floating debris, altered gravity on small objects. Mass crowd panic radiates outward. Police establish perimeter. Billboards near portal show interference patterns. Portal persists for 5 minutes, then collapses, leaving residual anomaly markers. |
| **Setup Parameters** | Time: 8:00 PM. Portal location: Duffy Square center. Portal radius: 2m. Effect radius: 15m. Panic radius: 50m. Police perimeter: 30m. Duration: 300s. Crowd density pre-event: 80%. |
| **Stress Targets** | VFX budget for portal + distortion + floating debris. Mass panic crowd AI (hundreds of NPCs fleeing simultaneously). Police perimeter formation under chaotic conditions. Billboard interference shader. Audio system with extreme point-source + ambient layers. Evidence generation rate during high-activity event. |
| **Failure Modes to Watch** | Crowd stampede causing physics explosions. Portal VFX tanking framerate. NPCs running through portal geometry. Police unable to form perimeter due to fleeing crowds. Evidence system overwhelmed. Memory spike from simultaneous VFX + crowd + audio. |
| **Duration** | 10 minutes sim-time |

---

#### Scenario 08: Construction Closure

| Field | Value |
|-------|-------|
| **Severity** | 2 (Low) |
| **Affected Systems** | Traffic, crowds |
| **Description** | Construction scaffolding closes the east sidewalk of Broadway between 45th and 46th. Pedestrian bridge installed. One vehicle lane closed with concrete barriers and orange cones. Construction noise audio. Worker NPCs present. Pedestrian flow forced through narrowed corridor. |
| **Setup Parameters** | Time: 10:00 AM. Closed: east sidewalk Broadway 45th-46th + 1 vehicle lane. Detour: pedestrian bridge. Worker NPCs: 8. Barrier entities: 24 cones + 6 concrete barriers. |
| **Stress Targets** | Pedestrian rerouting through narrow corridor. Traffic lane reduction without gridlock. Construction prop collision accuracy. NPC pathfinding around multi-level detour. |
| **Failure Modes to Watch** | Pedestrians walking through barriers. Traffic not respecting lane closure. NPC pathfinding failure on pedestrian bridge. Crowd compression at corridor entry/exit. |
| **Duration** | 8 minutes sim-time |

---

#### Scenario 09: Celebrity Sighting

| Field | Value |
|-------|-------|
| **Severity** | 2 (Low) |
| **Affected Systems** | Crowds, traffic, cops |
| **Description** | A celebrity NPC exits a vehicle at 44th and Broadway. Paparazzi NPCs (20) and fan crowd (100) rapidly converge. Bodyguard NPCs attempt to create path. Police assist with crowd control. Traffic briefly blocked by stopped vehicle and crowd spillover. Phone-camera props raised by crowd NPCs. |
| **Setup Parameters** | Time: 7:00 PM. Location: 44th/Broadway east side. Celebrity NPC: 1 + 4 bodyguards. Paparazzi: 20, converge within 15s. Fan crowd: builds to 100 over 60s. Vehicle: double-parked SUV. |
| **Stress Targets** | Rapid crowd convergence pathfinding. Bodyguard AI (maintain formation while moving through crowd). Phone-prop raise animation on many NPCs simultaneously. Traffic handling of double-parked vehicle. |
| **Failure Modes to Watch** | Celebrity NPC engulfed by crowd (bodyguard failure). Crowd NPCs phasing through bodyguards. Traffic not reacting to stopped vehicle. |
| **Duration** | 6 minutes sim-time |

---

#### Scenario 10: Fire Alarm Evacuation

| Field | Value |
|-------|-------|
| **Severity** | 4 (High) |
| **Affected Systems** | Crowds, traffic, cops, audio |
| **Description** | Fire alarm triggers in a major building on 7th Avenue (simulated Marriott Marquis). 800 NPCs evacuate simultaneously through multiple exits onto 7th Ave and 45th/46th Streets. Fire trucks navigate through Times Square. Evacuees mill on sidewalks, compressing pedestrian space. Police close nearest intersection. Alarm audio audible for 2 blocks. |
| **Setup Parameters** | Time: 2:00 PM. Evacuating building: west side 7th Ave, 45th-46th. Evacuee count: 800 (spawned from building exits over 120s). Fire trucks: 3 units arriving T+180s. Police: close 7th/45th intersection. Alarm audio radius: 150m. |
| **Stress Targets** | Mass NPC spawn and pathfinding from building interiors. Sidewalk capacity under evacuation load. Emergency vehicle navigation. Intersection closure traffic rerouting. Audio alarm propagation. NPC count spike (800 new entities). |
| **Failure Modes to Watch** | NPCs stacking at building exits. Sidewalk overflow causing NPCs in roadway. Fire trucks unable to reach building. Memory spike from 800 simultaneous NPC spawns. Pathfinding collapse under load. |
| **Duration** | 12 minutes sim-time |

---

#### Scenario 11: Subway Disruption

| Field | Value |
|-------|-------|
| **Severity** | 3 (Moderate) |
| **Affected Systems** | Crowds, traffic |
| **Description** | Times Square subway station (42nd St) is closed due to service disruption. Commuters who would normally enter/exit underground are redirected to surface level. Pedestrian density increases 40% across the slice. Bus stops see increased queuing. Taxi demand spikes. Crowd flow patterns shift as underground shortcuts are unavailable. |
| **Setup Parameters** | Time: 5:30 PM (evening rush). Subway exits: closed (barricaded). Surface crowd modifier: +40%. Bus stop queue multiplier: 2.5x. Taxi demand: 3x normal. |
| **Stress Targets** | Sustained elevated crowd density across entire slice. Bus stop queue management. Taxi spawning and pickup logistics. Pedestrian flow redistribution without underground routes. |
| **Failure Modes to Watch** | Crowd density exceeding capacity causing deadlocks. Bus stop queues blocking sidewalks. Too many taxi spawns causing traffic gridlock. Sustained high NPC count degrading performance. |
| **Duration** | 10 minutes sim-time |

---

#### Scenario 12: Police Chase
**v1 SELECTED**

| Field | Value |
|-------|-------|
| **Severity** | 4 (High) |
| **Affected Systems** | Traffic, crowds, cops, audio |
| **Description** | A suspect vehicle flees south on 7th Avenue pursued by 3 police vehicles. Sirens at maximum. The chase enters Times Square from the north, weaves through traffic, and the suspect vehicle crashes at 43rd Street. Police on foot pursue the fleeing suspect into the pedestrian areas around TKTS steps. Crowd NPCs react with flee and rubberneck behaviors. Traffic yields (or fails to yield) to chase vehicles. |
| **Setup Parameters** | Time: 10:00 PM. Chase entry: 7th Ave at 47th, southbound. Suspect vehicle: sedan, speed 60mph in 25mph zone. Police vehicles: 3, pursuit formation. Crash location: 7th/43rd. Foot chase: 43rd to Duffy Square. Siren audio radius: 300m. Crowd reaction radius: 40m from vehicle path. |
| **Stress Targets** | High-speed vehicle AI in dense urban environment. Traffic AI yielding/dodge behavior. Police pursuit formation and coordination. Transition from vehicle chase to foot chase. Crowd panic along chase path. Crash physics and debris. Siren audio Doppler and occlusion. Evidence generation during high-speed event. |
| **Failure Modes to Watch** | Chase vehicles clipping through traffic. Traffic AI not reacting to sirens. Crash physics launching vehicles unrealistically. Foot chase NPC clipping through crowd. Crowd not fleeing from speeding vehicles. Siren audio cutting out during rapid movement. |
| **Duration** | 8 minutes sim-time (chase enters at T+30s, crash at T+90s, foot chase T+100s-T+240s, aftermath through end) |

---

#### Scenario 13: Street Performer Crowd

| Field | Value |
|-------|-------|
| **Severity** | 2 (Low) |
| **Affected Systems** | Crowds, traffic, audio |
| **Description** | Three street performers set up at different locations: a breakdancer at 45th/Broadway, a guitarist at TKTS steps, and a living statue on the 7th Ave sidewalk. Each attracts a semi-circular crowd of 30-50 spectators. Pedestrian flow must route around these gatherings. Performance audio competes with ambient sound. Tips animation triggers periodically. |
| **Setup Parameters** | Time: 4:00 PM. Performer locations: 3 positions. Crowd per performer: 30-50 NPCs in semicircle. Pedestrian detour: around each gathering. Audio sources: 3 performance + ambient. |
| **Stress Targets** | Semi-circular crowd formation and maintenance. Pedestrian rerouting around multiple obstacles. Multi-source audio mixing. NPC attention behavior (watching, tipping, leaving). |
| **Failure Modes to Watch** | Crowd circles collapsing or drifting. Pedestrians walking through performer crowds. Audio sources drowning each other out. Crowd NPCs blocking entire sidewalk width. |
| **Duration** | 8 minutes sim-time |

---

#### Scenario 14: New Year's Eve Density

| Field | Value |
|-------|-------|
| **Severity** | 5 (Critical) |
| **Affected Systems** | Crowds, traffic, cops, lighting, audio, devices |
| **Description** | Times Square at peak New Year's Eve density. Crowd fills every available pedestrian surface to maximum capacity. Police barriers create holding pens. No vehicle traffic — all streets closed. Every billboard at maximum brightness. Confetti burst at midnight. Audio at maximum — crowd roar, music stages, countdown. This is the absolute maximum load scenario. |
| **Setup Parameters** | Time: 11:55 PM, Dec 31. Crowd density: 100% capacity. Vehicle traffic: 0 (all streets closed). Police barriers: full grid. Billboard brightness: maximum. Stage audio: 4 locations. Confetti: midnight burst (particle system stress test). |
| **Stress Targets** | Absolute maximum NPC count. Maximum lighting load (all billboards at full + stage lights). Particle system maximum (confetti). Audio maximum (crowd + music + countdown). Zero vehicle traffic (unusual state). Barrier collision with maximum crowd pressure. |
| **Failure Modes to Watch** | NPC count exceeding system capacity. Frame rate collapse under maximum load. Confetti particles causing memory spike. Crowd crush physics at barriers. Audio distortion from all sources at maximum. Streaming system failure under maximum asset load. |
| **Duration** | 10 minutes sim-time (countdown at T+300s) |

---

#### Scenario 15: Summer Heat Wave

| Field | Value |
|-------|-------|
| **Severity** | 2 (Low) |
| **Affected Systems** | Crowds, lighting, audio |
| **Description** | Extreme heat (105F) affects NPC behavior and visual atmosphere. Heat haze distortion over asphalt. Reduced pedestrian density as NPCs seek shade and air-conditioned interiors. Open fire hydrant on side street with children playing. Ice cream vendor queues lengthened. Harsh midday shadows. Steam rising from subway grates intensified. |
| **Setup Parameters** | Time: 1:00 PM. Temperature: 105F. Crowd density: 45% (reduced). Heat haze: enabled on roads. Shade-seeking: 60% of NPCs. Fire hydrant: open at 46th side street. Steam intensity: 2x baseline. |
| **Stress Targets** | Heat haze shader performance over large road surfaces. NPC shade-seeking pathfinding (many NPCs converging on limited shade). Water particle effects (hydrant). Steam particle effects (grates). |
| **Failure Modes to Watch** | Heat haze causing visual artifacts or performance drop. All NPCs converging on same shade spots. Fire hydrant water particles tanking performance. |
| **Duration** | 8 minutes sim-time |

---

#### Scenario 16: Snowstorm

| Field | Value |
|-------|-------|
| **Severity** | 4 (High) |
| **Affected Systems** | Traffic, crowds, lighting, audio |
| **Description** | Heavy snowfall blankets Times Square. Snow accumulation on horizontal surfaces (car roofs, awnings, steps, barriers). Reduced visibility to 50m. Traffic slowed to 40% of normal speed. Pedestrians walk carefully (reduced speed, slip animations). Snowplow vehicles operate on main roads. Billboard light scatters through falling snow. Road surface changes to packed snow (friction reduction). |
| **Setup Parameters** | Time: 6:00 PM. Snowfall rate: heavy (particle density high). Accumulation: enabled on all horizontal surfaces. Visibility: 50m. Traffic speed: 0.4x. Pedestrian speed: 0.6x. Snowplows: 2 vehicles on 7th Ave. Surface friction: 0.4x. |
| **Stress Targets** | Snow particle system at high density. Accumulation system (dynamic texture/mesh modification on all surfaces). Reduced-friction vehicle physics. Snowplow vehicle AI (clearing lanes). Visibility fog system combined with snow particles. Light scattering through snow volume. |
| **Failure Modes to Watch** | Snow particles tanking framerate. Accumulation system causing texture popping. Vehicles sliding uncontrollably on low-friction surfaces. Snowplow AI failing to navigate. Snow appearing inside buildings/tunnels. |
| **Duration** | 10 minutes sim-time |

---

#### Scenario 17: Gas Leak

| Field | Value |
|-------|-------|
| **Severity** | 4 (High) |
| **Affected Systems** | Crowds, traffic, cops, audio |
| **Description** | Con Edison reports a gas leak at 46th and Broadway. Police establish 2-block evacuation perimeter. All pedestrians within perimeter ordered to evacuate. Traffic rerouted around perimeter. Fire department and Con Edison trucks arrive. NPCs outside perimeter exhibit curiosity behavior. Gas hiss audio near source. No visible gas, but manhole steam used as visual indicator. |
| **Setup Parameters** | Time: 11:00 AM. Leak location: 46th/Broadway NE corner. Evacuation radius: 2 blocks. Police perimeter: 44th-48th, Broadway-8th Ave. Evacuee count: ~400 NPCs. Emergency vehicles: 5 (fire + utility). |
| **Stress Targets** | Large-area evacuation coordination. Multi-block traffic rerouting. Police perimeter over large area. NPC compliance with evacuation order (some resist, most comply). Emergency vehicle staging. |
| **Failure Modes to Watch** | NPCs ignoring evacuation perimeter. Traffic entering closed zone. Emergency vehicles blocking each other. Evacuation pathfinding failure (too many NPCs, too few exits). |
| **Duration** | 12 minutes sim-time |

---

#### Scenario 18: Drone Swarm Sighting

| Field | Value |
|-------|-------|
| **Severity** | 3 (Moderate) |
| **Affected Systems** | Crowds, cops, audio, devices, anomaly |
| **Description** | A swarm of 50 small drones appears above Times Square at 200ft altitude. NPCs look up, point, photograph. Some NPCs panic (anomaly fear). Police respond, attempting to identify operator. Drone lights create patterns visible against night sky. Billboards' CCTV systems track the swarm. Some drones descend to 50ft, increasing crowd reaction intensity. Ambiguous whether anomaly-related or mundane. |
| **Setup Parameters** | Time: 9:00 PM. Drone count: 50, altitude 200ft initial, 50ft descent for 10 units. Crowd reaction: 40% curious (phone-up), 30% nervous, 20% indifferent, 10% panic. Police response: T+60s. CCTV tracking: enabled. |
| **Stress Targets** | 50 flying entities with light sources above dense crowd. NPC look-up behavior and phone-camera animations at scale. CCTV tracking system processing multiple airborne targets. Anomaly ambiguity system (is it anomaly or not?). Light patterns from drone swarm on ground surfaces. |
| **Failure Modes to Watch** | Drones clipping through buildings. NPC look-up direction incorrect (not tracking swarm). Too many drone lights causing lighting system overload. CCTV system failing to track airborne objects. |
| **Duration** | 8 minutes sim-time |

---

#### Scenario 19: Billboard Malfunction Cascade

| Field | Value |
|-------|-------|
| **Severity** | 3 (Moderate) |
| **Affected Systems** | Lighting, devices, crowds, audio |
| **Description** | A software glitch causes Times Square billboards to malfunction in sequence. Starting from the north end, billboards begin displaying static, color bars, or extreme brightness flashes. The cascade moves south over 60 seconds. Each malfunction changes the local lighting dramatically. NPCs react to sudden brightness changes. Electrical buzzing audio from malfunctioning boards. Some boards go completely dark. The cascade reverses and boards restore in sequence. |
| **Setup Parameters** | Time: 8:30 PM. Cascade start: north end (47th). Cascade speed: 1 billboard per 3 seconds, moving south. Malfunction types: static (40%), color bars (30%), flash (20%), dark (10%). Electrical audio: per-billboard source. NPC reaction radius: 15m per billboard. |
| **Stress Targets** | Rapid sequential lighting changes across entire scene. Billboard emissive material swaps at runtime. Dynamic light recalculation as each billboard changes state. Electrical audio sources multiplying. NPC reaction chains (serial reactions as cascade moves). |
| **Failure Modes to Watch** | Lighting system unable to keep up with rapid changes. Billboard texture swaps causing frame hitches. Flash effects causing photosensitivity concerns (brightness must be capped). Memory leak from rapid material swaps. Audio source count exceeding budget. |
| **Duration** | 6 minutes sim-time (cascade forward: 60s, hold: 60s, cascade reverse: 60s, aftermath: 180s) |

---

#### Scenario 20: Tourist Bus Blockage

| Field | Value |
|-------|-------|
| **Severity** | 2 (Low) |
| **Affected Systems** | Traffic, crowds |
| **Description** | A double-decker tourist bus stalls at 7th Avenue and 44th Street, blocking the right two lanes. Passengers (40 NPCs) disembark and mill on the sidewalk. Tow truck dispatched. Traffic backs up on 7th Ave for 4 blocks. Pedestrians rubberneck. Bus driver NPC attempts restart periodically. A second tourist bus behind cannot pass, creating a larger blockage. |
| **Setup Parameters** | Time: 3:00 PM. Stall location: 7th/44th, right lanes. Passengers: 40 NPCs disembarking over 60s. Tow truck: arrives T+300s. Traffic backup: extends to 48th St. Second bus: stuck at T+30s. |
| **Stress Targets** | Large vehicle collision/blockage in narrow space. Traffic backup propagation over multiple blocks. NPC disembarkation from vehicle. Tow truck navigation through gridlocked traffic. Multi-vehicle blockage resolution. |
| **Failure Modes to Watch** | Traffic backup not propagating realistically. NPCs disembarking into traffic. Tow truck unable to reach stalled bus. Second bus clipping through first. |
| **Duration** | 10 minutes sim-time |

---

#### Scenario 21: Anomaly Shimmer at Intersection
**v1 SELECTED**

| Field | Value |
|-------|-------|
| **Severity** | 5 (Critical) |
| **Affected Systems** | Anomaly, traffic, crowds, cops, lighting, audio, devices |
| **Description** | A reality anomaly manifests as a visible shimmer/distortion at the center of the 7th Avenue and 45th Street intersection. The shimmer is 3m wide and appears to bend light, like heat haze but with chromatic aberration and occasional sparks. Vehicles driving through it experience momentary visual glitch effects. NPCs near it feel uneasy and give it wide berth. Police are called, establish a loose perimeter. Traffic signals at the intersection begin behaving erratically. Nearby billboards show fleeting interference patterns. The anomaly fluctuates in intensity over time — sometimes nearly invisible, sometimes dramatically bright. Evidence collection is critical during high-intensity phases. |
| **Setup Parameters** | Time: 7:30 PM. Anomaly location: center of 7th/45th intersection. Shimmer radius: 1.5m (visual effect extends to 5m). Intensity cycle: sinusoidal, period 120s, range 0.2-1.0. Traffic signal disruption: within 20m radius. NPC avoidance radius: 8m (grows with intensity). Police response: T+120s. Billboard interference: within 30m. Evidence burst rate: proportional to intensity. |
| **Stress Targets** | Anomaly VFX shader at varying intensities. Traffic AI handling erratic signals. NPC avoidance pathfinding around dynamic obstacle. Vehicle pass-through glitch effects. Billboard interference shader on multiple screens. Evidence system generating at high rate during intensity peaks. Police AI responding to unprecedented situation. Dynamic lighting from anomaly affecting scene illumination. Audio anomaly hum with intensity-linked parameters. |
| **Failure Modes to Watch** | Anomaly VFX causing frame drops at high intensity. Traffic AI deadlocking at erratic signals. NPCs walking through anomaly during low-intensity phases. Evidence system overwhelmed during peaks. Police AI unable to form perimeter around moving/fluctuating obstacle. Billboard interference causing texture corruption. Anomaly light bleeding through buildings. Audio hum not scaling with intensity. |
| **Duration** | 10 minutes sim-time (anomaly appears at T+0, fluctuates continuously, does not resolve — scenario ends with anomaly still active) |

---

## 3. v1 Selected Scenarios — Summary

The following five scenarios are selected for the v1 milestone. They provide coverage across severity levels, system combinations, and gameplay-critical paths.

| Priority | Scenario | Severity | Rationale |
|----------|---------|----------|-----------|
| 1 | **Baseline Midday** (#01) | 1 | Establishes reference metrics. Every other scenario is compared against this. Must pass before any stress test is meaningful. |
| 2 | **Rainstorm** (#02) | 3 | Tests weather system, surface material changes, crowd behavior adaptation, and particle system budget. Moderate severity, high visual impact. Most common environmental stress. |
| 3 | **Police Chase** (#12) | 4 | Tests high-speed vehicle AI, traffic yielding, crowd panic, vehicle-to-foot transition, and evidence generation during fast-moving events. Core gameplay loop. |
| 4 | **Anomaly Shimmer at Intersection** (#21) | 5 | Tests the game's unique anomaly system, which is the core differentiator. Exercises nearly every subsystem simultaneously. Must work for the game's premise to function. |
| 5 | **Blackout** (#04) | 5 | Tests lighting system resilience, NPC behavior mass-transition, traffic fallback modes, and the visual identity of Times Square under extreme conditions. Maximum system stress without anomaly overlay. |

### v1 Scenario Execution Order

1. **Baseline Midday** — Establish reference metrics. All 8 baseline metrics must pass.
2. **Rainstorm** — First environmental stress test. Compare metrics against baseline.
3. **Police Chase** — First gameplay stress test. Focus on vehicle AI and crowd reaction.
4. **Anomaly Shimmer** — Core game mechanic test. Focus on VFX, evidence, and AI response.
5. **Blackout** — Maximum stress test. Focus on lighting system resilience and NPC behavior.

Each scenario must pass all 8 acceptance metrics (Section 5) before the next is attempted.

---

## 4. Scenario Runner Interface Spec

### 4.1 Overview

The **Scenario Runner** is the system responsible for loading, executing, measuring, and recording scenario test runs. It operates as a deterministic simulation harness that can replay scenarios identically given the same seed.

### 4.2 Interface Definition

```typescript
interface ScenarioRunner {
  /**
   * Load a baseline world state snapshot to serve as the
   * starting point for the scenario.
   */
  loadBaseline(snapshotId: string): Promise<WorldState>;

  /**
   * Apply scenario-specific parameters on top of the baseline.
   * Returns the modified world state ready for execution.
   */
  applyScenarioParams(
    worldState: WorldState,
    scenario: ScenarioDefinition
  ): Promise<WorldState>;

  /**
   * Execute the scenario for the specified duration.
   * Captures metrics, events, and video at configured intervals.
   *
   * @param worldState - The prepared world state
   * @param durationMinutes - Sim-time duration to run
   * @param config - Execution configuration (seed, capture intervals, etc.)
   * @returns Execution result with all captured data
   */
  run(
    worldState: WorldState,
    durationMinutes: number,
    config: RunConfig
  ): Promise<ExecutionResult>;

  /**
   * Export all captured data from a completed run.
   */
  exportResults(executionId: string): Promise<ScenarioOutput>;

  /**
   * Replay a previous run using its recorded seed and event log.
   */
  replay(executionId: string): Promise<ExecutionResult>;
}

interface ScenarioDefinition {
  id: string;                          // Unique scenario identifier
  name: string;                        // Human-readable name
  description: string;                 // Full description
  severity: 1 | 2 | 3 | 4 | 5;       // Stress severity
  affected_systems: SystemTag[];       // Which systems are stressed
  setup_parameters: Record<string, any>; // Scenario-specific overrides
  duration_minutes: number;            // Default sim-time duration
  timed_events: TimedEvent[];          // Events triggered at specific sim-times
  success_criteria: Criterion[];       // Scenario-specific pass/fail criteria
}

type SystemTag =
  | "traffic"
  | "crowds"
  | "lighting"
  | "audio"
  | "devices"
  | "cops"
  | "anomaly";

interface TimedEvent {
  sim_time_seconds: number;  // When to trigger (seconds into scenario)
  event_type: string;        // Event identifier
  parameters: Record<string, any>; // Event-specific data
}

interface RunConfig {
  seed: number;                        // Deterministic random seed
  capture_video: boolean;              // Enable video capture
  video_checkpoint_interval_seconds: number; // Video capture interval (default: 30)
  metrics_sample_interval_seconds: number;   // Metrics sampling rate (default: 1)
  screenshot_interval_seconds: number;       // Screenshot capture rate (default: 10)
  max_memory_mb: number;               // Memory ceiling for abort (default: 6144)
  target_fps: number;                  // Target frame rate (default: 30)
}

interface ExecutionResult {
  execution_id: string;                // Unique run identifier
  scenario_id: string;                 // Which scenario was run
  seed: number;                        // Random seed used
  start_time: string;                  // ISO 8601 wall-clock start
  end_time: string;                    // ISO 8601 wall-clock end
  sim_duration_seconds: number;        // Sim-time elapsed
  status: "completed" | "aborted" | "crashed"; // Run outcome
  abort_reason?: string;               // If aborted, why
  metrics_summary: MetricsSummary;     // Aggregated metrics
  event_log_path: string;              // Path to full event log
  video_captures: VideoCaptureRef[];   // Paths to video segments
  screenshots: ScreenshotRef[];        // Paths to screenshots
}
```

### 4.3 Execution Pipeline

```
1. LOAD BASELINE SNAPSHOT
   |
   +-- Deserialize world state from canonical snapshot
   +-- Verify snapshot integrity (hash check)
   +-- Initialize all subsystems to snapshot state
   |
2. APPLY SCENARIO PARAMETERS
   |
   +-- Override weather, time, crowd density, traffic state
   +-- Spawn scenario-specific entities (emergency vehicles, barriers, etc.)
   +-- Configure timed event triggers
   +-- Set random seed for deterministic execution
   |
3. RUN FOR N MINUTES SIM-TIME
   |
   +-- Advance simulation frame-by-frame
   +-- At each frame:
   |     +-- Tick physics, AI, traffic, crowd, weather, anomaly systems
   |     +-- Check timed event triggers
   |     +-- Sample metrics (at configured interval)
   |     +-- Capture screenshot (at configured interval)
   |     +-- Capture video segment (at checkpoint interval)
   |     +-- Log events to event log
   |     +-- Check abort conditions (memory ceiling, crash detection)
   |
4. EXPORT METRICS + REPLAY DATA
   |
   +-- Aggregate sampled metrics into summary
   +-- Write event log to disk
   +-- Finalize video captures
   +-- Generate metrics summary JSON
   +-- Package all outputs into ScenarioOutput
```

### 4.4 Required Outputs

Every scenario run produces the following artifacts:

#### 4.4.1 Event Log

A chronological record of every significant event during the run.

```json
{
  "execution_id": "run-20260127-baseline-001",
  "events": [
    {
      "sim_time": 0.000,
      "event_type": "scenario_start",
      "data": { "scenario": "baseline_midday", "seed": 42 }
    },
    {
      "sim_time": 12.450,
      "event_type": "npc_spawn",
      "data": { "entity_id": "npc:ped-0042", "location": [40.758, -73.985, 0.0] }
    },
    {
      "sim_time": 45.120,
      "event_type": "traffic_signal_change",
      "data": { "intersection": "7av-45st", "state": "green_ns" }
    }
  ]
}
```

Event types include: `scenario_start`, `scenario_end`, `npc_spawn`, `npc_despawn`, `npc_behavior_change`, `vehicle_spawn`, `vehicle_despawn`, `traffic_signal_change`, `collision_event`, `anomaly_state_change`, `evidence_generated`, `crowd_density_threshold`, `performance_warning`, `system_error`, `timed_event_triggered`, `police_response`, `emergency_vehicle_dispatch`.

#### 4.4.2 Video Captures (30-Second Checkpoints)

At every 30-second interval of sim-time, a 30-second video segment is captured from the primary evaluation camera (overhead view of the full scenario area).

```json
{
  "checkpoint_index": 0,
  "sim_time_start": 0.0,
  "sim_time_end": 30.0,
  "file_path": "captures/run-001/video/checkpoint-000.mp4",
  "resolution": "1920x1080",
  "fps": 30,
  "camera": "eval_overhead"
}
```

Additional cameras may be configured per-scenario (e.g., chase-cam for police chase, ground-level for crowd scenarios).

#### 4.4.3 Metrics Summary JSON

Aggregated metrics for the entire run, sampled at the configured interval.

```json
{
  "execution_id": "run-20260127-baseline-001",
  "scenario_id": "baseline_midday",
  "duration_seconds": 600,
  "metrics": {
    "fps": {
      "mean": 45.2,
      "min": 32.1,
      "max": 60.0,
      "p5": 33.8,
      "p50": 45.0,
      "p95": 58.2,
      "below_30_count": 0,
      "below_30_percentage": 0.0
    },
    "crowd_deadlock_rate": {
      "total_npcs": 4200,
      "deadlocked_npcs": 2,
      "rate": 0.00048
    },
    "traffic_gridlock_rate": {
      "total_intersections": 12,
      "gridlocked_intersections": 0,
      "rate": 0.0
    },
    "collision_error_rate": {
      "total_collision_checks": 182400,
      "errors": 3,
      "rate": 0.000016
    },
    "npc_incident_rate": {
      "total_npcs": 4200,
      "incidents": 5,
      "rate": 0.0012,
      "incident_types": {
        "stuck": 2,
        "path_failure": 1,
        "behavior_error": 2
      }
    },
    "anomaly_containment_success_rate": {
      "anomaly_events": 0,
      "contained": 0,
      "rate": null
    },
    "evidence_generation_rate": {
      "total_evidence_events": 0,
      "rate_per_second": 0.0,
      "note": "No incidents in baseline scenario"
    },
    "memory_peak_mb": {
      "peak": 4280,
      "mean": 3920,
      "spikes_above_6gb": 0
    }
  },
  "pass_fail": {
    "fps_stability": "PASS",
    "crowd_deadlock": "PASS",
    "traffic_gridlock": "PASS",
    "collision_errors": "PASS",
    "npc_incidents": "PASS",
    "anomaly_containment": "N/A",
    "evidence_generation": "N/A",
    "memory_ceiling": "PASS"
  },
  "overall": "PASS"
}
```

---

## 5. Acceptance Metrics — 8 Baselines

These eight metrics are evaluated for every scenario run. A scenario passes only if all applicable metrics meet their thresholds.

| # | Metric | Threshold | Measurement | Failure Consequence |
|---|--------|-----------|-------------|-------------------|
| 1 | **FPS Stability** | >30 FPS floor (0% of frames below 30) | Sample every frame. Count frames below 30. Report min, mean, p5. | Scenario fails. Performance optimization required. |
| 2 | **Crowd Deadlock Rate** | <0.1% of NPCs deadlocked at any sample | Sample every 5s. Count NPCs with zero movement for >10s who have active goals. | Scenario fails. Crowd pathfinding review required. |
| 3 | **Traffic Gridlock Rate** | <5% of intersections gridlocked | Sample every 10s. An intersection is gridlocked if no vehicle passes through in 60s despite queue. | Scenario fails. Traffic AI review required. |
| 4 | **Collision Error Rate** | <0.01% of collision checks produce errors | Count penetrations, fall-throughs, and incorrect collision responses. | Scenario fails. Physics/collision review required. |
| 5 | **NPC Incident Rate** | <1% of NPCs experience behavioral incidents | Count stuck NPCs, path failures, behavior tree errors, T-poses. | Warning below 0.5%, fail above 1%. |
| 6 | **Anomaly Containment Success Rate** | >95% of anomaly events properly contained by game systems | Count anomaly events where police respond, perimeter forms, evidence generated. | Scenario fails if anomaly scenario and rate <95%. N/A for non-anomaly scenarios. |
| 7 | **Evidence Generation Rate** | >1 evidence event/sec during active incidents | During incident windows, count evidence events per second. | Scenario fails if gameplay-critical evidence is missed. N/A for baseline. |
| 8 | **Memory/Streaming Spike Ceiling** | <6 GB peak memory usage | Sample memory every 1s. Report peak, mean, and count of samples above 6GB. | Scenario fails. Streaming/LOD optimization required. |

### Metric Weighting by Scenario Severity

| Severity | FPS Weight | Crowd Weight | Traffic Weight | Collision Weight | NPC Weight | Anomaly Weight | Evidence Weight | Memory Weight |
|----------|-----------|-------------|---------------|-----------------|-----------|---------------|----------------|-------------- |
| 1 (Nominal) | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | N/A | N/A | 1.0 |
| 2 (Low) | 1.0 | 1.0 | 1.0 | 1.0 | 0.8 | N/A | 0.8 | 1.0 |
| 3 (Moderate) | 0.9 | 0.9 | 0.9 | 1.0 | 0.7 | 1.0 | 1.0 | 0.9 |
| 4 (High) | 0.8 | 0.8 | 0.8 | 1.0 | 0.6 | 1.0 | 1.0 | 0.8 |
| 5 (Critical) | 0.7 | 0.7 | 0.7 | 1.0 | 0.5 | 1.0 | 1.0 | 0.7 |

> **Note:** At higher severity, soft metrics (FPS, crowd, traffic) are relaxed slightly — the system is expected to degrade gracefully. Hard metrics (collision, anomaly, evidence) never relax. Memory ceiling is slightly relaxed at severity 4-5 to account for peak load.

> **Interpreting weights:** A weight of 0.7 means the threshold is relaxed by 30%. For example, FPS floor at severity 5 becomes `30 * 0.7 = 21 FPS`. This is the absolute minimum acceptable — below this, the scenario still fails even at critical severity.

---

## 6. Scenario Definition Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://twin-earth-nyc.dev/schemas/scenario/v0.json",
  "title": "ScenarioDefinition",
  "type": "object",
  "required": ["id", "name", "severity", "affected_systems", "setup_parameters", "duration_minutes"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^scenario:[a-z0-9-]+$"
    },
    "name": {
      "type": "string"
    },
    "description": {
      "type": "string"
    },
    "severity": {
      "type": "integer",
      "minimum": 1,
      "maximum": 5
    },
    "affected_systems": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["traffic", "crowds", "lighting", "audio", "devices", "cops", "anomaly"]
      },
      "minItems": 1
    },
    "setup_parameters": {
      "type": "object",
      "properties": {
        "time_of_day": { "type": "string", "pattern": "^\\d{2}:\\d{2}$" },
        "weather": { "type": "string" },
        "temperature_f": { "type": "number" },
        "crowd_density_modifier": { "type": "number", "minimum": 0, "maximum": 2 },
        "traffic_speed_modifier": { "type": "number", "minimum": 0, "maximum": 2 },
        "road_closures": { "type": "array", "items": { "type": "string" } },
        "special_entities": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "template": { "type": "string" },
              "count": { "type": "integer" },
              "location": { "type": "string" },
              "spawn_time": { "type": "number" }
            }
          }
        }
      },
      "additionalProperties": true
    },
    "duration_minutes": {
      "type": "number",
      "minimum": 1,
      "maximum": 60
    },
    "timed_events": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["sim_time_seconds", "event_type"],
        "properties": {
          "sim_time_seconds": { "type": "number", "minimum": 0 },
          "event_type": { "type": "string" },
          "parameters": { "type": "object", "additionalProperties": true }
        }
      }
    },
    "success_criteria": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["metric", "threshold"],
        "properties": {
          "metric": { "type": "string" },
          "threshold": { "type": "number" },
          "comparison": { "type": "string", "enum": ["gt", "gte", "lt", "lte", "eq"] }
        }
      }
    },
    "v1_selected": {
      "type": "boolean",
      "default": false
    },
    "tags": {
      "type": "array",
      "items": { "type": "string" }
    }
  }
}
```

---

*End of document. Next: `fuzz-harness-plan-v0.md`*
