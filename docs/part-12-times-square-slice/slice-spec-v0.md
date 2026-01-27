# Times Square Slice Spec v0

**Document:** Twin Earth NYC — Part 12, File 1 of 6
**Status:** v0 Draft
**Scope:** Slice polygon, invariants, "done" definition, success demo

---

## 1. Slice Overview

The Times Square slice is the first playable vertical slice of Twin Earth NYC. It captures the iconic "bowtie" intersection where Broadway crosses 7th Avenue diagonally, encompassing the most recognizable pedestrian space in Manhattan. This slice serves as the proof-of-concept for every major system: geometry, crowd simulation, IoT event bus, evidence ledger, Heat channels, anomaly spawning, portal pockets, and the Show Director.

**Purpose:** Prove that all engine systems work together in a single, dense, visually spectacular urban environment.

**Target:** A 5-minute continuous playthrough that exercises walk, drive, crowd, billboard, anomaly, portal, and evidence systems without interruption.

---

## 2. Slice Polygon

### 2.1 Boundary Definition

| Boundary | Reference | Alignment |
|----------|-----------|-----------|
| **South** | 42nd Street | Center line of roadway |
| **North** | 47th Street | Center line of roadway |
| **East** | 7th Avenue | East sidewalk edge (building frontage line) |
| **West** | Broadway | West sidewalk edge (building frontage line) |

### 2.2 Key Geometric Notes

- **The Bowtie:** Broadway runs diagonally (NW to SE) through the Manhattan grid, crossing 7th Avenue (which runs due north-south) at approximately 43rd-44th Street. This diagonal crossing creates the triangular pedestrian plazas that define Times Square.
- **Father Duffy Square:** The northern triangle of the bowtie, between 45th and 47th Streets, containing the TKTS Red Steps and the Father Duffy statue.
- **Times Square proper:** The southern triangle, between 42nd and 45th Streets, anchored by One Times Square.
- The slice polygon is **irregular** due to Broadway's diagonal. The east-west width varies from approximately 150m at the narrow ends to 250m where Broadway diverges furthest from 7th Avenue.

### 2.3 Dimensions

| Measurement | Value |
|-------------|-------|
| North-south extent | ~500m (42nd to 47th, 5 blocks) |
| East-west extent (narrowest) | ~150m (at 42nd and 47th) |
| East-west extent (widest) | ~250m (at bowtie center, ~44th) |
| Total area | ~0.08 km² (8 hectares) |
| Block count | 5 cross-streets, 2 avenues, 1 diagonal |

### 2.4 Slice Map

```
                            47th Street
            __________________|___________________
           |                  |                    |
           |   B              |        7th         |
           |   r              |        Avenue      |
           |   o         Father Duffy              |
           |   a           Square                  |
           |   d          ________                 |
           |   w         / TKTS   \                |
           |   a        / Red Steps\               |
           |   y       /____________\              |
           |          /              \             |
           |    46th St               46th St      |
           |        /                  \           |
           |       /                    \          |
           |    45th St               45th St      |
           |     /                      \          |
           |    /     B O W T I E        \         |
           |   / I N T E R S E C T I O N  \       |
           |  /          ZONE              \       |
           | /                              \      |
           |/    44th St ---- 44th St        \     |
           |\     [Portal Zone]              /     |
           | \                              /      |
           |  \   One Times Square         /       |
           |   \    (wedge bldg)          /        |
           |    \                        /         |
           |     \    43rd St           /          |
           |      \                    /           |
           |       \                  /            |
           |        \________________/             |
           |                  |                    |
           |__________________|____________________|
                            42nd Street

     WEST (Broadway)                    EAST (7th Ave)

     Legend:
       / \  = Broadway diagonal edges
       |    = 7th Avenue (north-south)
       ---  = Cross streets
       [Portal Zone] = First anomaly/portal location
```

### 2.5 Notable Structures Within Slice

| Structure | Location | Role in Slice |
|-----------|----------|---------------|
| One Times Square | 42nd/Broadway-7th wedge | Visual anchor, hero billboard host |
| TKTS Red Steps | Father Duffy Square | Crowd attractor, scale anchor |
| 3 Times Square (Reuters) | 43rd/7th NE corner | Hero billboard host |
| 1515 Broadway (ABC) | 44th/Broadway | Hero billboard host |
| Marriott Marquis | 45th/Broadway | Hero billboard, seam location |
| AMC Empire 25 | 42nd St | Seam location (vertical) |
| Father Duffy Statue | Duffy Square | Landmark anchor |
| 42nd St Subway Entrance | 42nd/7th | Zone transition seam |

---

## 3. Invariants

Ten geometric, visual, and physics invariants that must hold true for the slice to be considered accurate. These are measured during every regression pass.

| # | Invariant | Type | Tolerance | Verification Method | Reference Source |
|---|-----------|------|-----------|--------------------|--------------------|
| 1 | **Broadway alignment angle** — Broadway's diagonal must match real-world bearing through the slice | Geometry | +/-1 degree from surveyed angle (~29 deg off grid) | Overhead orthographic capture compared to satellite imagery | NYC GIS, Google Earth Pro |
| 2 | **7th Avenue width** — Curb-to-curb plus sidewalks must match surveyed dimensions | Geometry | +/-0.5m from ~23m total (curb-to-curb ~15m) | Cross-section measurement at 3 points (43rd, 44th, 45th) | NYC DOT street survey |
| 3 | **42nd-47th block spacing** — Cumulative distance from 42nd center line to 47th center line | Geometry | +/-1.0m cumulative over 5 blocks (~400m total) | Distance check along 7th Ave centerline | NYC GIS block dimensions |
| 4 | **TKTS Red Steps position and dimensions** — Steps must be correctly placed within Father Duffy Square with accurate footprint and height | Geometry | +/-0.25m position, +/-0.1m height | Anchor check against surveyed coordinates; step count verification (27 steps) | TKTS architectural drawings, photogrammetry |
| 5 | **One Times Square silhouette** — Building outline as seen from 43rd/Broadway must match reference photography | Visual | 2 degree rotation tolerance, 3% scale tolerance | Edge detection comparison against reference photo set (4 angles) | Reference photography library |
| 6 | **Bowtie intersection angles** — The angles formed where Broadway crosses 7th Ave at the bowtie | Geometry | +/-1 degree per angle | Overhead orthographic capture, angle measurement | NYC GIS, surveyed intersections |
| 7 | **Sidewalk widths (Broadway and 7th Ave)** — Measured at building frontage to curb edge | Geometry | +/-0.3m | Cross-section measurement at 6 points (3 per avenue) | NYC DOT pedestrian survey |
| 8 | **Curb heights** — Standard NYC curb height throughout slice | Physics | +/-2cm from 15cm standard | Step measurement tool; physics collision test (drop object on curb) | NYC DOT standard spec |
| 9 | **Crosswalk placement** — Painted crosswalk positions at all intersections relative to intersection corners | Geometry | +/-0.5m | Anchor check against surveyed crosswalk positions | NYC DOT intersection plans |
| 10 | **Marriott Marquis sign zone** — The marquee sign area on the Marriott facade must be correctly positioned for billboard content | Placement | +/-1.0m position | Reference overlay comparison against street-level photography | Photogrammetry, Google Street View |

### Invariant Verification Schedule

- **Every build:** Invariants 1, 3, 6 (structural geometry — automated overhead capture)
- **Every art pass:** Invariants 4, 5, 7, 9, 10 (placement and visual — semi-automated with manual review)
- **Every physics update:** Invariant 8 (curb physics — automated drop test)
- **Every street update:** Invariant 2 (avenue width — automated cross-section)

### Invariant Failure Protocol

1. Any invariant failure blocks the build from promotion to QA.
2. Failure is logged with measured value, expected value, delta, and screenshot/capture.
3. Owner is auto-assigned based on invariant type (Geometry -> Level Design, Visual -> Art, Physics -> Engineering).
4. Fix must be verified by re-running the specific invariant check before re-promotion.

---

## 4. "Done" Definition

The Times Square slice is **done** when all five of the following criteria are met simultaneously in a single build:

### 4.1 WALK

> A player can walk the full slice -- 42nd to 47th on both Broadway and 7th Ave sidewalks -- without collision snags, floating, or falling through geometry.

**Specific requirements:**
- Continuous walk on Broadway west sidewalk from 42nd to 47th: no collider gaps, no invisible walls, no z-fighting
- Continuous walk on 7th Ave east sidewalk from 42nd to 47th: same criteria
- Cross at every crosswalk (42nd through 47th): player correctly steps up/down curbs, crosswalk signals function
- Walk up and down TKTS Red Steps: collision on every step, no clipping through risers
- Walk through Father Duffy Square: navigable around statue, benches, planters
- Walk along 44th St between Broadway and 7th Ave: full connectivity
- No location where player capsule gets stuck on geometry seams
- No location where player floats above ground plane by more than 2cm
- No location where player falls through ground

### 4.2 DRIVE

> A vehicle can complete a traffic loop through the slice following signals without clipping, wrong-way, or gridlock.

**Specific requirements:**
- Vehicle enters from 47th St southbound on 7th Ave, follows signal at each intersection, exits at 42nd St: complete loop without stopping except at red signals
- Vehicle enters from 42nd St northbound on Broadway (where applicable), navigates to exit: correct lane following through bowtie
- No vehicle clips through curbs, bollards, or other vehicles
- No vehicle enters wrong-way on one-way streets
- Signal compliance: vehicles stop at red within 2m of stop line, proceed within 1s of green
- No gridlock condition: all vehicles in slice clear within 3 signal cycles under normal load
- Turning vehicles at intersections follow correct turning radii (no cutting corners through sidewalks)

### 4.3 CROWD

> 500+ background pedestrians and 10 hero NPCs navigate the slice with less than 0.1% deadlock rate and realistic signal compliance (>95%).

**Specific requirements:**
- Minimum 500 background NPCs active simultaneously during midday period
- Minimum 10 hero NPCs active with full behavior trees
- Deadlock rate: fewer than 1 deadlock per 1,000 NPC-minutes (0.1%)
- Deadlock definition: 3+ NPCs with velocity < 0.05 m/s for > 10 seconds
- Signal compliance: >95% of NPCs wait for walk signal before crossing
- No NPC walks through solid geometry (buildings, vehicles, bollards)
- No NPC hovers above or sinks below ground plane
- Crowd density visually plausible: no obvious clumping artifacts, no empty voids in high-traffic areas
- NPCs react to anomaly events (approach/avoid based on type)
- Hero NPCs maintain distinct behaviors (not just following flow)

### 4.4 BILLBOARDS

> 8 hero billboards display correct tier content at correct distances, light spill active at night, performance within budget.

**Specific requirements:**
- All 8 hero billboards (BB_H01 through BB_H08) display content
- Near tier (0-30m): full video at 30fps for top-tier billboards
- Mid tier (30-150m): 5fps loop or static based on billboard class
- Far tier (150m+): static emissive or off based on billboard class
- Tier transitions are smooth (no pop or flash)
- Light spill: each hero billboard casts colored light on nearby geometry and NPCs at night
- Light spill radius and color match spec (see Show Director Config)
- Total billboard GPU time < 2ms
- No more than 4 full-video billboards active simultaneously
- Background billboards (BB_B01-20) display static content, contribute to ambiance
- Emergency mode: if FPS drops below 35, all billboards demote to static within 1 frame

### 4.5 LOGGING

> Every IoT artifact generates events, evidence accumulates in the ledger, Heat responds to incidents, and a replay test produces consistent results.

**Specific requirements:**
- All 12 traffic signals cycle and emit `traffic.signal.changed` events
- All 24 crosswalk signals sync and emit `traffic.crosswalk.changed` events
- All 18 CCTV cameras generate `security.camera.motion` events on detection
- All 5 kiosks respond to `public_info.kiosk.alert` events
- All 25 doors track state and emit `access.door.state_changed` events
- Evidence records are created for every significant observation
- Ledger commits occur at all specified commit points (authority action, evidence corroboration, damage state change, anomaly state change, timer)
- Heat channels respond correctly to events (values rise and decay per spec)
- Replay test: running the demo script with seed=42 twice produces ledger outputs that match within stochastic tolerance (defined as: same event count +/-2%, same event types, same ordering of committed events)

---

## 5. Success Demo: "The 5-Minute Proof"

### 5.1 Concept

A single continuous 5-minute gameplay sequence that proves every major system is working. No cuts, no teleports, no debug commands. One take. If it plays clean, the slice is done.

### 5.2 Sequence Overview

| Timestamp | Action | Systems Exercised |
|-----------|--------|-------------------|
| 0:00-0:45 | Walk south on Broadway, observe crowds | Walk, Crowd, Billboards, Show Director |
| 0:45-1:15 | Cross at 45th, approach TKTS steps | Walk, Signals, Crosswalk, NPC compliance |
| 1:15-1:45 | Observe anomaly shimmer at 44th | Anomaly system, CCTV events, Heat |
| 1:45-2:15 | Crowd reacts, authority dispatched | Crowd AI, Heat response, IoT events |
| 2:15-2:45 | Police arrive, portal forms | Authority behavior, Portal state machine |
| 2:45-3:15 | Enter portal pocket | Portal transition, pocket physics, aesthetic |
| 3:15-3:45 | Grab artifact, pocket destabilizes | Artifact system, stability timer, VFX |
| 3:45-4:00 | Exfil through portal | Portal exit, transition back to hub |
| 4:00-4:30 | Aftermath: evidence, heat, crowd response | Ledger, Heat persistence, crowd displacement |
| 4:30-5:00 | Return to scene, verify persistence | Persistence, residue, police tape, CCTV logs |

### 5.3 Detailed Beat Script

```
BEAT 1 — ESTABLISHING (T+0:00 to T+0:45)
  Location: 46th St / Broadway, facing south
  Player action: Walk south on Broadway sidewalk at normal pace

  Observe:
    - Crowd density matches midday spec (~1000 background NPCs visible)
    - Billboard tiers correct: near billboards playing video, mid billboards
      showing low-fps loops, far billboards static
    - No geometry pop-in within 30m
    - Ambient audio: city traffic, crowd murmur, billboard audio bleed
    - Lighting: afternoon sun angle, billboard glow visible even in daylight

  Systems proven: Walk, Show Director (LOD bands), Billboard tiers, Crowd density

BEAT 2 — CROSSING (T+0:45 to T+1:15)
  Location: 45th St crosswalk
  Player action: Wait for walk signal, cross 45th with NPC crowd

  Observe:
    - Crosswalk signal changes from DON'T WALK to WALK
    - NPCs queue at curb, step off together on WALK signal
    - Traffic stops at red, no vehicle incursion into crosswalk
    - Player steps up/down curbs cleanly (15cm, no floating)
    - After crossing, approach TKTS Red Steps area
    - Tourist NPCs gathered on and around steps, some taking photos
    - Scale check: steps, humans, signs all proportionally correct
    - Billboard light spill visible on crowd faces (subtle in daylight)

  Systems proven: Signal sync, NPC compliance, Vehicle compliance,
                   Curb physics, Attraction points, Scale anchors

BEAT 3 — ANOMALY APPEARS (T+1:15 to T+1:45)
  Location: Player near Father Duffy Square, looking south toward 44th
  Event: Anomaly triggers at 44th St between Broadway and 7th Ave

  Observe:
    - Visual shimmer appears: light refraction distortion, ~3m radius initial
    - Audio: low-frequency hum begins (audible within 20m)
    - Event bus fires: anomaly.zone.spike
    - Nearest CCTV (CAM_TSQ_007) generates security.camera.observation
      with "anomalous visual distortion" classification
    - Heat channels begin rising:
        Physical: 0.0 -> 0.0 (no physical damage yet)
        Social: 0.0 -> +0.10 (people noticing)
        Institutional: 0.0 -> +0.05 (system alert)
        Ecological: 0.0 -> +0.20 (reality distortion)

  Systems proven: Anomaly spawn, CCTV detection, Event bus, Heat channels

BEAT 4 — CROWD REACTION (T+1:45 to T+2:15)
  Location: Between Father Duffy Square and 44th St

  Observe:
    - Rubbernecking ring forms: curious NPCs slow and face anomaly (15-20m)
    - Avoidance zone: NPCs within 10m begin rerouting away
    - Some tourists move TOWARD anomaly (curiosity behavior)
    - Commuters reroute without stopping (commuter preset)
    - Authority dispatch triggered: authority.dispatch.unit event fires
    - Patrol officer begins routing from current position to 44th St
    - Social Heat continuing to rise
    - Anomaly radius growing: r(t) = 3 + 7*(1 - e^(-t/180)) meters

  Systems proven: NPC reaction behaviors, Crowd flow dynamics,
                   Authority dispatch, Heat accumulation

BEAT 5 — AUTHORITY ARRIVAL + PORTAL (T+2:15 to T+2:45)
  Location: Player approaches 44th St

  Observe:
    - Patrol officer arrives at scene, begins assessment behavior
    - Officer attempts to establish perimeter (cordon behavior triggered at
      High Heat)
    - Crowd management: officer gestures NPCs to move back
    - Anomaly reaches radius ~8m: PORTAL FORMS
    - Portal state: LATENT -> FORMING -> STABLE (with player proximity trigger)
    - Energy flash VFX at portal formation
    - Massive evidence burst: 5+ observations generated
        - CCTV saw portal open (CAM_TSQ_007, CAM_TSQ_008)
        - Witness observations from hero NPCs in range
        - Anomaly sensor spike logged
    - Heat spike: Physical +0.10, Social +0.20, Institutional +0.10,
      Ecological +0.30
    - Player can see portal entrance: shimmering vertical distortion in alley

  Systems proven: Authority AI, Portal state machine, Evidence generation,
                   Heat spike handling

BEAT 6 — PORTAL ENTRY (T+2:45 to T+3:00)
  Location: 44th St alley, portal entrance
  Player action: Step into portal

  Observe:
    - Smooth transition: Times Square geometry fades, pocket geometry loads
    - Physics shift: gravity changes to 0.8g (player feels lighter, jump higher)
    - Aesthetic shift: color palette desaturates to noir tones
    - Audio transition: Hub city sounds fade out over 1s, replaced by
      otherworldly ambient (low drone, distant metallic echoes)
    - Pocket geometry: 10m x 10m x 5m concrete corridor with alien
      geometric details (impossible angles, faint luminescent lines)
    - No NPCs in pocket (empty, isolated)
    - Portal exit visible behind player (the way back)

  Systems proven: Portal transition, Physics modification, Aesthetic layers,
                   Audio crossfade, Pocket geometry loading

BEAT 7 — OBJECTIVE + COMPLICATION (T+3:00 to T+3:30)
  Location: Inside pocket
  Player action: Walk to artifact, grab it

  Observe:
    - Artifact visible on pedestal at far end of corridor: small metallic
      object, glowing, rotating slowly
    - Grab artifact: artifact enters inventory
    - Inventory shows: artifact (2kg, compatibility 0.4 in universe 1218)
    - T+60s after entry: stability begins dropping (-0.1 per 30s)
    - Visual cracks appear in pocket geometry
    - Floor begins to crumble at edges
    - Walls distort (geometry warping VFX)
    - Audio urgency: cracks, groaning, frequency rising
    - At stability < 0.1: full collapse warning
        - Floor crumbling accelerates
        - Walls closing in
        - Player has 30s to reach exit

  Systems proven: Artifact pickup, Inventory system, Stability timer,
                   Pocket destabilization VFX, Urgency escalation

BEAT 8 — EXFIL (T+3:30 to T+3:45)
  Location: Pocket, moving toward exit
  Player action: Run to portal exit, step through

  Observe:
    - Portal exit still visible (glowing frame)
    - Player steps through: smooth transition back to Times Square
    - Physics return to 1.0g
    - Color palette restores to full saturation
    - Hub sounds return: sirens, crowd noise, traffic
    - Portal collapses behind player: STABLE -> COLLAPSING -> SEALED
    - Visual: portal implodes with energy discharge VFX
    - Stability forced to 0.0

  Systems proven: Portal exfil, Physics restoration, Portal collapse,
                   State machine completion

BEAT 9 — AFTERMATH (T+3:45 to T+4:30)
  Location: 44th St, Times Square
  Player action: Observe aftermath, then walk north into crowd

  Observe:
    - Artifact in inventory: glowing, emitting low-level signature
    - CCTV within 5m can detect artifact signature
    - Portal residue patch visible at former portal location: shimmer,
      slight gravity distortion, decays over 24h sim-time
    - Evidence burst logged in ledger: all observations committed
    - Police moving toward portal location (additional units dispatched)
    - Crowd displaced: running NPCs near 44th, normal flow further away
    - Heat levels check:
        Physical: ~0.12 (elevated)
        Social: ~0.30 (high)
        Institutional: ~0.15 (elevated)
        Ecological: ~0.50 (high)
    - Player walks north into crowd, blending in
    - Police not immediately pursuing (player not yet identified as
      connected to portal event)
    - Artifact signature slowly fading

  Systems proven: Artifact persistence, Evidence commit, Residue system,
                   Heat persistence, Crowd displacement, Authority escalation

BEAT 10 — PERSISTENCE CHECK (T+4:30 to T+5:00)
  Location: Return to 44th St
  Player action: Walk back to portal location

  Observe:
    - Police tape around portal residue zone
    - Residue shimmer still visible (only 2 minutes have passed)
    - CCTV events still logging (continuous monitoring of area)
    - Heat still elevated (slow decay in progress):
        Physical: ~0.10 (decaying at -0.02/min)
        Social: ~0.28 (decaying at -0.01/min)
        Institutional: ~0.14 (decaying at -0.005/min)
        Ecological: ~0.49 (decaying at -0.003/min)
    - Ledger query confirms: all events present, committed, consistent
    - FINAL FRAME: player stands at 44th, looking at the residue of what
      just happened, police activity around, crowds resuming normal flow
      further out, billboards blazing overhead, city continuing

  Systems proven: Persistence, Decay rates, Ledger integrity, World continuity

SCORE: PASS if all observe/verify steps confirmed across all 10 beats.
```

### 5.4 Failure Conditions

Any single failure in the 5-Minute Proof means the slice is **not done**:

- Player gets stuck on geometry at any point
- Player floats or falls through ground
- NPC deadlock visible during sequence
- Signal does not change (stuck red or green)
- Vehicle clips through geometry
- Billboard fails to display or pops between tiers visibly
- Anomaly does not trigger on schedule
- CCTV does not detect anomaly
- Heat does not rise after portal event
- Portal transition is not smooth (hitch, black screen, crash)
- Pocket physics incorrect (gravity not 0.8g)
- Artifact does not enter inventory
- Pocket does not destabilize on timer
- Exfil transition fails
- Evidence not committed to ledger
- Residue not visible on return
- Police tape not placed
- FPS drops below 30 at any point during sequence

---

## 6. Coordinate System and Reference Points

### 6.1 World Origin

The slice uses a local coordinate system with origin at the center of the bowtie intersection (approximately 43rd St where Broadway median meets 7th Ave center).

| Axis | Direction | Reference |
|------|-----------|-----------|
| +X | East | Toward 7th Ave east sidewalk |
| -X | West | Toward Broadway west sidewalk |
| +Y | Up | Vertical |
| -Y | Down | Below street level |
| +Z | North | Toward 47th St |
| -Z | South | Toward 42nd St |

### 6.2 Key Anchor Points

| Anchor | Local Coordinates (approx) | Real-World Reference |
|--------|---------------------------|---------------------|
| Bowtie center | (0, 0, 0) | Broadway/7th intersection center |
| TKTS Red Steps base | (-15, 0, +120) | Father Duffy Square |
| One Times Square apex | (-5, 0, -60) | 42nd/Broadway wedge |
| 42nd St center line | (0, 0, -200) | Southern boundary |
| 47th St center line | (0, 0, +300) | Northern boundary |
| 7th Ave east edge | (+75, 0, 0) | Eastern boundary |
| Broadway west edge | (-100, 0, 0) | Western boundary |

---

## 7. Dependencies

This slice spec depends on and references the following prior documents:

| Document | Part | Relevance |
|----------|------|-----------|
| Manhattan Grid Spec | Part 2 | Street dimensions, block spacing, curb standards |
| Show Director Architecture | Part 5 | LOD bands, distance calculations, performance budgets |
| Event Bus Spec | Part 7 | IoT topics, event schema, bus throughput |
| Heat System Design | Part 8 | Channel definitions, decay rates, response behaviors |
| Anomaly + Portal Design | Part 10 | Anomaly growth curves, portal state machine, pocket specs |
| Evidence + Ledger Design | Part 11 | Ledger schema, commit rules, persistence |
| Regression Pack Spec | Part 9 | Camera positions, comparison methodology |

---

## 8. Open Questions

| # | Question | Owner | Status |
|---|----------|-------|--------|
| 1 | Exact Broadway bearing through slice — need survey data to confirm 29-degree assumption | Level Design | Open |
| 2 | TKTS Red Steps — are all 27 steps individually modeled or can we merge groups? | Art | Open |
| 3 | Subway entrance at 42nd — is this a zone transition or a hard seam? | Design | Open |
| 4 | One Times Square interior — any interior needed or is it facade-only? | Design | Open |
| 5 | Father Duffy statue — hero asset or generic placeholder? | Art | Open |

---

*End of document. Next: Show Director + Billboard Tier Config v0.*
