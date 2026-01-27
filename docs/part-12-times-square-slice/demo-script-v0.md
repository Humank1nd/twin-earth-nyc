# Demo Script + Regression Pack v0

**Document:** Twin Earth NYC — Part 12, File 6 of 6
**Status:** v0 Draft
**Scope:** Detailed demo script, regression capture pack, pass/fail criteria, anticipated issues

---

## 1. Overview

This document defines the complete, repeatable demo script for the Times Square slice -- "The 5-Minute Proof." It provides frame-level verification instructions, regression data capture specifications, pass/fail criteria, and a prioritized list of anticipated issues.

The demo script is both a **showcase** (proving the slice works) and a **test harness** (catching regressions). Every build must pass this script before promotion to QA.

---

## 2. Pre-Conditions

Before running the demo, the following state must be established. Any deviation from these pre-conditions invalidates the run.

### 2.1 World State

| Parameter | Required Value | Verification |
|-----------|---------------|-------------|
| **Time of day** | 2:00 PM (14:00 sim-time) | HUD clock display |
| **Weather** | Clear | Sky state check |
| **Heat (Physical)** | 0.0 | Heat debug overlay |
| **Heat (Social)** | 0.0 | Heat debug overlay |
| **Heat (Institutional)** | 0.0 | Heat debug overlay |
| **Heat (Ecological)** | 0.0 | Heat debug overlay |
| **Anomaly state** | Dormant (scheduled to trigger at T+1:00) | Anomaly system debug |
| **Portal state** | LATENT | Portal system debug |
| **Ledger** | Empty (no prior events) | Ledger query: count = 0 |
| **Player inventory** | Empty | Inventory screen |
| **Player health** | 100% | HUD |
| **Player position** | 46th St / Broadway, facing south | Coordinates check |

### 2.2 System State

| System | Required State | Verification |
|--------|---------------|-------------|
| **All 12 traffic signals** | Cycling normally | Signal debug overlay |
| **All 24 crosswalk signals** | Synced to traffic signals | Crosswalk debug overlay |
| **All 18 CCTV cameras** | Operational, normal scan rate (2Hz) | Camera status panel |
| **All 5 kiosks** | IDLE state | Kiosk status panel |
| **All 25 doors** | Per schedule (14:00 = business hours, most unlocked) | Door status panel |
| **NPC population** | Midday targets (1200 bg peds, 40 vehicles, 15 hero, 2 hero vehicles, 3 authority) | Population counter |
| **Billboards** | All displaying correct tier content | Visual inspection |
| **Performance** | Stable 60fps | FPS counter |
| **Event bus** | Operational, queue depth 0 | Bus monitor |
| **Random seed** | 42 (for reproducibility) | Seed display in debug |

### 2.3 Pre-Condition Validation Script

```
PRE-CONDITION VALIDATION (automated):

  function validate_preconditions():
    assert sim_time == "14:00:00", "Time must be 2:00 PM"
    assert weather.state == CLEAR, "Weather must be clear"
    assert heat.physical == 0.0, "Heat Physical must be 0"
    assert heat.social == 0.0, "Heat Social must be 0"
    assert heat.institutional == 0.0, "Heat Institutional must be 0"
    assert heat.ecological == 0.0, "Heat Ecological must be 0"
    assert anomaly_system.state == DORMANT, "Anomaly must be dormant"
    assert portal_system.state == LATENT, "Portal must be latent"
    assert ledger.count() == 0, "Ledger must be empty"
    assert player.inventory.count() == 0, "Inventory must be empty"
    assert player.health == 1.0, "Player must be at full health"
    assert distance(player.position, VEC3(-85, 0, 250)) < 5.0,
           "Player must be near 46th/Broadway"

    assert traffic_signals.all_operational(), "All signals must work"
    assert cctv_cameras.all_operational(), "All cameras must work"
    assert kiosks.all_idle(), "All kiosks must be idle"
    assert npc_population.background_peds >= 1100, "Peds near midday target"
    assert npc_population.hero_peds >= 10, "Hero NPCs present"
    assert npc_population.authority >= 2, "Authority units on patrol"
    assert fps.current >= 55, "FPS must be stable at start"
    assert event_bus.queue_depth == 0, "Event bus must be clear"
    assert random_seed == 42, "Seed must be 42"

    print("ALL PRE-CONDITIONS MET — READY FOR DEMO")
    return true
```

---

## 3. The 5-Minute Proof — Complete Script

### Beat 1: Establishing Walk (T+0:00 to T+0:30)

**Location:** 46th St / Broadway, facing south
**Player action:** Begin walking south on Broadway west sidewalk at normal pace

```
BEAT 1 — VERIFICATION CHECKLIST:

  GEOMETRY:
  [ ] Player stands on solid ground (no floating, no sinking)
  [ ] Sidewalk surface is continuous (no gaps, no z-fighting)
  [ ] Building facades render correctly on both sides
  [ ] Curb edge visible and correct height (~15cm)

  CROWD:
  [ ] Background NPCs visible, walking in both directions
  [ ] Crowd density appropriate for midday (~1.0 person/m² on sidewalk)
  [ ] No NPC clipping through each other or through geometry
  [ ] Multiple NPC presets visible: commuters (fast), tourists (slow, looking up)
  [ ] At least 2 different body types visible within 10m

  BILLBOARDS:
  [ ] Nearest billboard displays correct Near-tier content (video or 5fps)
  [ ] Mid-range billboards display correct Mid-tier content (5fps loop)
  [ ] Far billboards (south toward 42nd) display static emissive
  [ ] No tier pop-in visible during walk
  [ ] Billboard light spill subtle but present on nearby surfaces

  SHOW DIRECTOR:
  [ ] Near-band NPCs have full animation (walking, phone, looking around)
  [ ] Mid-band NPCs have simplified animation (walking only)
  [ ] Far-band NPCs appear as particle crowd (if any visible at 150m+)
  [ ] No visible LOD transition artifacts

  AUDIO:
  [ ] City ambient: traffic, crowd murmur, distant horns
  [ ] Billboard audio bleed from nearest sign
  [ ] Footstep audio on concrete (player and nearby NPCs)
  [ ] Audio correctly spatialized (sounds come from correct directions)

  PERFORMANCE:
  [ ] FPS >= 55 (no significant drops during establishing walk)
```

### Beat 2: Signal Crossing (T+0:30 to T+0:45)

**Location:** Approaching 45th St crosswalk
**Player action:** Arrive at crosswalk, wait for WALK signal, cross with NPCs

```
BEAT 2 — VERIFICATION CHECKLIST:

  SIGNAL:
  [ ] Traffic signal visible at 45th St intersection
  [ ] Crosswalk signal visible on far side (facing player)
  [ ] Signal state correct: if DON'T WALK, vehicles flowing on 45th
  [ ] Signal changes to WALK within one cycle (~90s max wait)
  [ ] Countdown timer visible during FLASHING_STOP phase

  NPC COMPLIANCE:
  [ ] NPCs queue at curb edge when DON'T WALK
  [ ] NPCs step into crosswalk on WALK signal
  [ ] >95% of NPCs wait for signal (may see 1-2 jaywalkers)
  [ ] NPCs walk across at appropriate speed (1.0-1.4 m/s)
  [ ] NPCs on far side also cross when signal permits

  VEHICLE COMPLIANCE:
  [ ] Vehicles stop at red signal (within 2m of stop line)
  [ ] Vehicles proceed on green within 1 second
  [ ] No vehicle enters crosswalk while pedestrians crossing
  [ ] Vehicle types visible: taxis, sedans, delivery trucks

  PLAYER MOVEMENT:
  [ ] Player steps down curb (step animation, physics correct)
  [ ] Player walks across crosswalk (painted lines visible on road)
  [ ] Player steps up curb on far side
  [ ] No collision snags on curb edges
  [ ] No floating above road surface
```

### Beat 3: TKTS Approach (T+0:45 to T+1:00)

**Location:** Approaching TKTS Red Steps in Father Duffy Square
**Player action:** Walk toward TKTS steps, observe tourist NPCs

```
BEAT 3 — VERIFICATION CHECKLIST:

  TKTS RED STEPS:
  [ ] Steps visible and correctly positioned (Invariant #4)
  [ ] Step count correct (27 steps)
  [ ] Step height and depth physically accurate
  [ ] Red color of steps is correct
  [ ] Player can walk up steps if desired (collision on each step)

  TOURIST NPCS:
  [ ] Tourist NPCs gathered on and around steps (ATT_01 attraction)
  [ ] Some tourists sitting on steps (seated animation)
  [ ] Some tourists taking photos (hold phone up, 3-5s pose)
  [ ] Tourist groups visible (2-4 NPCs walking together)
  [ ] No NPC clipping through steps or each other

  SCALE ANCHORS:
  [ ] Human proportions correct (NPC height ~1.7m average)
  [ ] Steps proportional to humans (each step ~18cm rise)
  [ ] Father Duffy statue visible (if in scope) at correct scale
  [ ] Billboard sizes appear correct from this distance

  BILLBOARD LIGHT:
  [ ] Billboard light spill visible on crowd faces (subtle at 2PM)
  [ ] Color temperature varies by billboard
  [ ] Light correctly blocked by geometry (no light through buildings)
```

### Beat 4: Anomaly Appears (T+1:00 to T+1:15)

**Location:** Player near Father Duffy Square, looking south toward 44th St
**Event:** Anomaly spawns at 44th St alley

```
BEAT 4 — VERIFICATION CHECKLIST:

  ANOMALY VISUAL:
  [ ] Shimmer appears at 44th St location (visible from ~80m away)
  [ ] Initial radius ~3m (visual distortion contained to small area)
  [ ] Light refraction effect: heat-haze-like distortion
  [ ] Faint luminous particles within anomaly zone
  [ ] No pop-in: shimmer fades in over 2-3 seconds

  ANOMALY AUDIO:
  [ ] Low-frequency hum begins (30-60 Hz, audible within 20m)
  [ ] Hum is spatialized (comes from 44th St direction)
  [ ] City ambient audio not interrupted (hum layers on top)

  EVENT BUS:
  [ ] anomaly.zone.spike event published (check event bus monitor)
  [ ] Event contains correct location, radius, type
  [ ] Event timestamp matches sim-time

  CCTV RESPONSE:
  [ ] CAM_TSQ_007 (44th/Broadway building) generates observation
  [ ] security.camera.observation event on bus
  [ ] Observation type: "anomalous_visual"
  [ ] Confidence score present (expected ~0.7)

  HEAT UPDATE:
  [ ] Physical: 0.0 (unchanged)
  [ ] Social: ~0.10 (witnesses noticing)
  [ ] Institutional: ~0.05 (system alert)
  [ ] Ecological: ~0.20 (reality distortion)
  [ ] heat.channel.changed events published for channels crossing 0.0

  EVIDENCE:
  [ ] evidence.recorded event published
  [ ] Ledger now contains at least 1 committed event (auto_anomaly rule)
```

### Beat 5: Crowd Reaction (T+1:15 to T+1:45)

**Location:** Between Father Duffy Square and 44th St
**Event:** Crowd reacts to anomaly; authority dispatch triggered

```
BEAT 5 — VERIFICATION CHECKLIST:

  CROWD BEHAVIOR:
  [ ] Rubbernecking ring visible: NPCs at 15-20m from anomaly slow down
  [ ] Rubberneckers face anomaly (heads turned toward 44th St)
  [ ] Some tourists move TOWARD anomaly (curiosity behavior)
  [ ] NPCs within 10m of anomaly begin diverting around it
  [ ] Commuter NPCs continue walking but faster (Elevated response)
  [ ] No NPC walks directly into anomaly zone (avoidance active)
  [ ] Crowd flow disrupted but not deadlocked

  AUTHORITY DISPATCH:
  [ ] authority.dispatch.unit event published
  [ ] Nearest patrol officer (AUTH_01 or AUTH_02) changes route
  [ ] Officer begins moving toward 44th St at increased speed
  [ ] Officer radio chatter audio cue (faint, spatialized)

  HEAT PROGRESSION:
  [ ] Social Heat rising (crowd reaction amplifying)
  [ ] Institutional Heat rising (dispatch triggered)
  [ ] Ecological Heat rising (anomaly growing)
  [ ] Composite Heat level: Elevated (highest channel > 0.2)

  ANOMALY GROWTH:
  [ ] Radius now ~5m (per growth curve at ~75s)
  [ ] Shimmer intensity increased
  [ ] More particles visible
  [ ] Ground marking beginning to appear (faint)
```

### Beat 6: Authority Arrival + Portal Formation (T+1:45 to T+2:45)

**Location:** Player walks toward 44th St
**Events:** Police arrive, anomaly matures, portal forms

```
BEAT 6 — VERIFICATION CHECKLIST (T+1:45 to T+2:15):

  PLAYER APPROACH:
  [ ] Visual distortion increases as player gets closer to anomaly
  [ ] Camera slight tilt/wobble when entering anomaly influence (20m)
  [ ] Gravity wobble detectable (jump is slightly higher within zone)
  [ ] CCTV confidence dropping in anomaly zone (debug overlay)

  POLICE ARRIVAL (T+2:00):
  [ ] Patrol officer arrives at 44th St area
  [ ] Officer assessment behavior: cautious approach, radio usage
  [ ] Cordon preparation: officer begins directing NPCs away
  [ ] Additional dispatch event if Heat > 0.4 (Active response)
  [ ] Officer does not enter anomaly zone (stays at 10m+ distance)

BEAT 6 CONTINUED — VERIFICATION CHECKLIST (T+2:15 to T+2:45):

  PORTAL FORMATION (T+2:15):
  [ ] Anomaly radius has reached ~8m (formation threshold)
  [ ] Portal state transitions: LATENT → FORMING
  [ ] Swirling energy vortex VFX at alley entrance
  [ ] Rising harmonic audio tone
  [ ] Local gravity drop to 0.6g within 3m of portal forming point
  [ ] NPCs within 30m freeze momentarily, then flee at 2.0 m/s
  [ ] Energy flash VFX at formation completion (T+2:30, after 15s forming)
  [ ] Portal state: FORMING → STABLE

  EVIDENCE BURST:
  [ ] 5+ observations generated in rapid succession
  [ ] CAM_TSQ_007: portal energy detected
  [ ] CAM_TSQ_008: corroborating observation from mid-block camera
  [ ] Hero NPC observations (if HERO_02 or HERO_03 in range)
  [ ] All evidence auto-committed (corroboration rule: 2+ sources)

  HEAT SPIKE:
  [ ] Physical: ~0.10 (portal energy)
  [ ] Social: ~0.30+ (massive public event)
  [ ] Institutional: ~0.15+ (system alerts cascading)
  [ ] Ecological: ~0.50+ (reality breach)
  [ ] Composite Heat: High (>0.4)
  [ ] Authority response escalates to Active (cordon behavior)

  PORTAL APPEARANCE:
  [ ] Vertical distortion field visible (~2m x 3m)
  [ ] Shimmering edges with energy particles
  [ ] Glimpse of pocket space visible through portal (noir corridor)
  [ ] Steady harmonic drone audio
  [ ] Wind-like suction sound near portal
```

### Beat 7: Portal Entry (T+2:45 to T+3:00)

**Location:** 44th St alley, portal entrance
**Player action:** Walk into portal

```
BEAT 7 — VERIFICATION CHECKLIST:

  TRANSITION:
  [ ] Player walks into portal surface (collision triggers transition)
  [ ] Smooth transition: no black frame, no hitch, no pop
  [ ] Times Square geometry fades out (1s transition)
  [ ] Pocket geometry fades in simultaneously
  [ ] Transition VFX: energy wash, light streak, brief disorientation

  PHYSICS CHANGE:
  [ ] Gravity shifts to 0.8g (testable: jump is noticeably higher)
  [ ] Player movement feels slightly floaty
  [ ] No physics glitch (no ejection, no floor clip)

  AESTHETIC SHIFT:
  [ ] Color palette: desaturated, cool blue-gray tones
  [ ] High contrast: deep shadows and bright geometric light pools
  [ ] Film grain subtle overlay
  [ ] Vignette at screen edges
  [ ] Noir aesthetic achieved

  AUDIO TRANSITION:
  [ ] Hub city sounds fade out over 1 second
  [ ] Pocket ambience fades in: low drone, metallic echoes
  [ ] Reverb increases (enclosed space)
  [ ] Player footsteps echo on concrete (different surface)

  POCKET GEOMETRY:
  [ ] Corridor visible: 10m x 10m x 5m concrete space
  [ ] Alien geometric details on walls: luminescent white lines
  [ ] Floor-level fog/haze present
  [ ] Floating light particles
  [ ] Pedestal visible at far end with artifact
  [ ] Portal exit visible behind player (glowing frame)

  ISOLATION:
  [ ] No NPCs in pocket (empty, silent except ambience)
  [ ] No city sounds bleeding through
  [ ] Player is alone
```

### Beat 8: Artifact + Complication (T+3:00 to T+3:30)

**Location:** Inside pocket
**Player action:** Walk to artifact, grab it, deal with destabilization

```
BEAT 8 — VERIFICATION CHECKLIST:

  ARTIFACT:
  [ ] Artifact visible on pedestal: metallic polyhedron, glowing, rotating
  [ ] Glow intensifies as player approaches
  [ ] Hum audible near artifact
  [ ] Interaction prompt appears at 2m distance: "Take artifact"
  [ ] On pickup: flash of light, artifact enters inventory
  [ ] Inventory UI shows: "The Shard" — 2kg, compatibility 0.4

  DESTABILIZATION (begins on pickup):
  [ ] Visual cracks appear in walls within 30 seconds
  [ ] Floor edges begin crumbling (debris falls into void below)
  [ ] Walls show fractures that widen over time
  [ ] Fog increases
  [ ] Audio: cracking, groaning, rising urgency tone
  [ ] Camera shake increases subtly

  URGENCY CUES:
  [ ] Audio alarm begins at stability < 0.3
  [ ] Visual overlay (subtle red tinge) at stability < 0.2
  [ ] "GET OUT" style urgency at stability < 0.1
  [ ] Portal exit frame pulsing brighter (drawing player toward exit)

  PLAYER ACTION:
  [ ] Player can run toward exit (2.5-3.0 m/s run speed)
  [ ] No obstacles blocking path back to portal
  [ ] Corridor remains navigable despite visual destruction
  [ ] Reach portal entrance in ~3-4 seconds at run speed
```

### Beat 9: Exfiltration (T+3:30 to T+3:45)

**Location:** Pocket, moving to portal exit
**Player action:** Run to portal, step through back to Times Square

```
BEAT 9 — VERIFICATION CHECKLIST:

  EXIT TRANSITION:
  [ ] Player contacts portal exit surface
  [ ] Smooth transition back to Times Square (no hitch, no black frame)
  [ ] Pocket geometry fades out
  [ ] Hub geometry fades in
  [ ] Transition VFX mirrors entry (energy wash, light streak)

  PHYSICS RESTORATION:
  [ ] Gravity returns to 1.0g (immediate, no transition period)
  [ ] Player movement feels normal again
  [ ] No physics artifact from transition (no ejection, no fall)

  AESTHETIC RESTORATION:
  [ ] Full color saturation restored
  [ ] Normal contrast
  [ ] Film grain and vignette removed
  [ ] Times Square visual fidelity restored

  AUDIO RESTORATION:
  [ ] Hub sounds return: sirens (responding to incident), crowd noise, traffic
  [ ] Pocket ambience fades out over 1 second
  [ ] Siren audio prominent (authority response active)

  PORTAL COLLAPSE:
  [ ] Portal begins collapsing behind player (STABLE → COLLAPSING)
  [ ] Implosion VFX: energy pulled inward, sparks, debris
  [ ] Deep THOOM sound effect
  [ ] Gravity spike: brief 1.5g within 5m (player feels pulled back slightly)
  [ ] Collapse completes in 10 seconds → SEALED state
  [ ] Residue shimmer at former portal location
```

### Beat 10: Aftermath + Persistence (T+3:45 to T+5:00)

**Location:** 44th St, then walking away and returning
**Player action:** Observe aftermath, blend into crowd, return to verify persistence

```
BEAT 10a — IMMEDIATE AFTERMATH (T+3:45 to T+4:00):

  INVENTORY:
  [ ] Artifact "The Shard" in inventory
  [ ] Artifact glowing (visual indicator in inventory UI)
  [ ] Artifact emitting signature (debug overlay shows 5m detection radius)

  PORTAL STATE:
  [ ] Portal sealed (SEALED state)
  [ ] Residue shimmer visible at 44th St alley
  [ ] No portal entrance available (cannot re-enter)

  EVIDENCE:
  [ ] evidence.recorded events published for portal exit, collapse
  [ ] Ledger contains full chain: anomaly → portal → traversal → collapse
  [ ] All events committed (auto-commit rules satisfied)

  WORLD REACTION:
  [ ] Police moving toward portal location (if not already there)
  [ ] Additional police units arriving (Critical Heat response)
  [ ] Crowd displaced: running NPCs near 44th St
  [ ] Normal crowd flow further from scene (46th+)
  [ ] Sirens audible (multiple police vehicles)

BEAT 10b — BLEND IN (T+4:00 to T+4:30):

  PLAYER ACTION: Walk north away from scene into crowd

  [ ] Player can walk freely (not detained, not blocked)
  [ ] CCTV cameras near 44th detecting artifact signature (within 5m range)
  [ ] As player moves away from 44th cameras: detection stops
  [ ] Police not immediately pursuing player (not yet identified)
  [ ] Crowd behavior normalizing away from incident zone
  [ ] Tourist NPCs still evacuating (Elevated+ Heat area)
  [ ] Commuter NPCs resuming fast walk

  HEAT CHECK (at T+4:15):
  [ ] Physical: ~0.10 (decaying)
  [ ] Social: ~0.55+ (slowly decaying, was very high)
  [ ] Institutional: ~0.25+ (slowly decaying)
  [ ] Ecological: ~0.80+ (very slowly decaying)
  [ ] Composite level: Critical (Ecological > 0.7)

BEAT 10c — RETURN TO SCENE (T+4:30 to T+5:00):

  PLAYER ACTION: Walk back to 44th St portal location

  [ ] Police tape visible around residue zone (yellow/orange tape barriers)
  [ ] Residue shimmer still present (only ~1 min since seal)
  [ ] At least 1 authority unit standing near tape
  [ ] CCTV events still being logged (cameras on high alert, 10Hz)
  [ ] Crowd avoiding taped area (10m clearance)
  [ ] Billboard content: possibly showing "breaking news" if Marriott sign
      programmed for narrative events

  LEDGER FINAL CHECK:
  [ ] Query ledger: all events from this run present
  [ ] All events committed (no orphaned staging buffer entries)
  [ ] Event chain: anomaly.spike → camera.observation → authority.dispatch →
      portal.formed → portal.entered → portal.exited → portal.collapsed
  [ ] Heat records: sampled values present for all 4 channels
  [ ] Total event count: approximately 20-40 events (varies by NPC observations)

  FINAL STATE VERIFICATION:
  [ ] Heat levels: elevated but decaying (all channels > 0.0)
  [ ] Artifact: in inventory, signature fading slowly
  [ ] Portal: SEALED, residue active
  [ ] Authority: in Active/Critical response mode
  [ ] Crowd: displaced near 44th, normal elsewhere
  [ ] Billboards: all displaying (may be in emergency mode if FPS dropped)
  [ ] Performance: FPS > 30 at all times (ideally > 45)

  DEMO COMPLETE at T+5:00
```

---

## 4. Regression Capture Pack

After each demo run, the following data is captured for regression comparison between builds.

### 4.1 Regression Captures

| # | Capture | Format | Storage | Comparison Method |
|---|---------|--------|---------|------------------|
| 1 | **10 regression camera screenshots** | PNG, 1920x1080 | `/regression/screenshots/build_<N>/` | Pixel-diff with tolerance (SSIM > 0.95) |
| 2 | **Ledger export** | JSON | `/regression/ledger/build_<N>/ledger.json` | Event count, category distribution, ordering |
| 3 | **Heat state snapshot** | JSON | `/regression/heat/build_<N>/heat.json` | Channel values within +/- 0.05 |
| 4 | **Performance capture** | CSV (per-frame FPS, GPU ms, CPU ms, memory) | `/regression/perf/build_<N>/perf.csv` | FPS never < 30; avg > 45; memory < 4GB |
| 5 | **NPC state snapshot** | JSON | `/regression/npc/build_<N>/npc_state.json` | Hero NPC positions within 5m of expected |
| 6 | **Artifact inventory state** | JSON | `/regression/inventory/build_<N>/inventory.json` | Artifact present with correct properties |

### 4.2 Regression Camera Positions

10 fixed camera positions capture the visual state of the slice at specific moments.

| Camera # | Position | Facing | Timestamp | Purpose |
|----------|----------|--------|-----------|---------|
| RC_01 | 46th/Broadway, eye level | South | T+0:15 | Establishing: crowd, billboards, street |
| RC_02 | 45th crosswalk, eye level | East (across 7th Ave) | T+0:40 | Signal crossing: NPCs at crosswalk |
| RC_03 | TKTS steps, elevated (top of steps) | South | T+0:50 | Tourist gathering, Father Duffy Square |
| RC_04 | 44th/Broadway, eye level | East (toward anomaly) | T+1:10 | Anomaly first visible |
| RC_05 | 44th mid-block, eye level | South (anomaly zone) | T+1:30 | Crowd reaction to anomaly |
| RC_06 | 44th alley entrance, eye level | Into alley (portal) | T+2:20 | Portal forming |
| RC_07 | Inside pocket, eye level | Forward (toward artifact) | T+3:00 | Pocket environment |
| RC_08 | Inside pocket, eye level | Back (toward exit) | T+3:15 | Pocket destabilizing |
| RC_09 | 44th/Broadway, eye level | South (aftermath) | T+3:50 | Portal residue, police response |
| RC_10 | 44th alley, eye level | Into alley | T+4:45 | Police tape, residue, persistence |

### 4.3 Regression Screenshot Comparison

```
SCREENSHOT COMPARISON ALGORITHM:

  for each camera position (RC_01 through RC_10):
    current = load_screenshot(current_build, camera_id)
    baseline = load_screenshot(baseline_build, camera_id)

    // Structural Similarity Index
    ssim = compute_ssim(current, baseline)

    if ssim >= 0.95:
      result = PASS
    elif ssim >= 0.90:
      result = WARNING (flag for manual review)
    else:
      result = FAIL (visual regression detected)

    // Additional checks
    check_no_solid_color_frames(current)  // detect black/white/pink error frames
    check_no_missing_geometry(current, baseline)  // detect large missing regions
    check_billboard_content(current, camera_id)  // verify billboard regions not blank

  SPECIAL CASES:
    RC_04, RC_05: anomaly VFX may vary slightly per run.
      Tolerance increased to SSIM >= 0.88 for these frames.
    RC_07, RC_08: pocket environment is deterministic.
      Standard tolerance applies.
```

### 4.4 Ledger Regression Comparison

```
LEDGER COMPARISON:

  current_ledger = load_ledger(current_build)
  baseline_ledger = load_ledger(baseline_build)

  // Event count comparison
  count_diff = abs(current_ledger.count - baseline_ledger.count)
  assert count_diff <= baseline_ledger.count * 0.05,
         "Event count differs by more than 5%"

  // Category distribution
  for category in ALL_CATEGORIES:
    current_count = current_ledger.count_by_category(category)
    baseline_count = baseline_ledger.count_by_category(category)
    assert abs(current_count - baseline_count) <= max(2, baseline_count * 0.10),
           f"Category {category} count differs significantly"

  // Critical event presence
  REQUIRED_EVENTS = [
    ("anomaly", "zone_spike"),
    ("anomaly", "portal_formed"),
    ("anomaly", "portal_collapsed"),
    ("evidence", "visual_observation"),   // at least 5
    ("authority_response", "unit_dispatched"),
    ("heat_change", "channel_threshold_crossed"),  // at least 4
  ]

  for (category, subcategory) in REQUIRED_EVENTS:
    assert current_ledger.has_event(category, subcategory),
           f"Missing required event: {category}/{subcategory}"

  // Ordering
  committed_events_current = current_ledger.committed_events_ordered()
  committed_events_baseline = baseline_ledger.committed_events_ordered()
  assert events_same_order(committed_events_current, committed_events_baseline),
         "Committed event ordering has changed"
```

---

## 5. Pass/Fail Criteria

### 5.1 Hard Pass/Fail (any failure blocks build)

| Criteria | Pass Condition | Fail Condition | Measurement |
|----------|---------------|---------------|-------------|
| **FPS** | Never below 30 FPS during entire 5-minute demo | Any single frame below 30 FPS | Performance capture CSV |
| **Crowd deadlocks** | Zero deadlocks during demo | Any deadlock detected (3+ NPCs stuck > 10s) | Deadlock monitor log |
| **Evidence generation** | All expected events logged in ledger | Any required event missing (see list below) | Ledger query |
| **Heat response** | All Heat thresholds trigger correct behaviors | Any threshold crossed without corresponding behavior change | Heat debug log + visual verification |
| **Portal state machine** | All transitions in correct order (LATENT -> FORMING -> STABLE -> COLLAPSING -> SEALED) | Any skipped state, wrong order, or stuck state | Portal state log |
| **Persistence** | Ledger consistent on return to 44th St; door states persist; residue visible | Any state reset, missing event, or invisible residue | Manual verification + ledger query |
| **Visual** | No pop-in, no floating, no scale errors, no z-fighting visible | Any visible rendering artifact during demo | Screenshots + manual observation |
| **Audio** | Ambient + event audio plays correctly, transitions smooth | Missing audio, misplaced spatialization, or audio glitch | Manual audio review |

### 5.2 Required Events (Evidence Generation Check)

The following events MUST appear in the ledger after a complete demo run:

| # | Event Category | Subcategory | Minimum Count | Source |
|---|---------------|-------------|--------------|--------|
| 1 | anomaly | zone_spike | 1 | Anomaly system |
| 2 | evidence | visual_observation (anomaly) | 2 | CCTV cameras |
| 3 | authority_response | unit_dispatched | 1 | Authority system |
| 4 | heat_change | channel_threshold_crossed | 4 | Heat system (one per channel minimum) |
| 5 | anomaly | portal_formed | 1 | Portal system |
| 6 | evidence | visual_observation (portal) | 3 | CCTV + witnesses |
| 7 | anomaly | portal_collapsed | 1 | Portal system |
| 8 | evidence | artifact_detected | 1 | CCTV or sensor |

### 5.3 Soft Criteria (warning, does not block build)

| Criteria | Target | Warning Threshold | Notes |
|----------|--------|-------------------|-------|
| Average FPS | > 50 | < 45 | Performance degradation trend |
| NPC count accuracy | Within 10% of target | Within 20% of target | Spawn system tuning |
| Heat value accuracy | Within 0.05 of calculated | Within 0.10 of calculated | Floating point or timing drift |
| Screenshot SSIM | > 0.95 baseline match | > 0.90 baseline match | Visual drift detection |
| Event bus queue depth | Max < 50 | Max < 200 | Throughput concern |
| Memory usage | < 3 GB | < 4 GB | Memory pressure trend |

---

## 6. Top 10 Anticipated Issues

Prioritized list of issues most likely to arise during Times Square slice development and testing. Each includes the anticipated cause, detection method, and proposed mitigation.

### Issue 1: Crowd Bottleneck at TKTS Steps During Anomaly

**Priority:** HIGH
**Description:** When the anomaly triggers at 44th St, tourists at the TKTS steps (ATT_01) and fleeing NPCs from the anomaly zone may converge at the same choke point (Father Duffy Square narrows between steps and 7th Ave). This could cause a mass deadlock.

**Detection:** Deadlock monitor triggers; visual observation of NPC pile-up.

**Mitigation:**
- Attraction point ATT_01 reduces strength to 0 when Heat > 0.2 (tourists stop gathering)
- Evacuation routes for TKTS area direct NPCs east toward 7th Ave, not south through the bottleneck
- Emergency despawn: if deadlock cluster > 10 NPCs, force-despawn 50% behind nearest occlusion
- Physical separation: benches and planters channel flow

### Issue 2: CCTV Event Overload During Portal Energy Burst

**Priority:** HIGH
**Description:** When the portal forms, all 18 cameras may detect the energy burst simultaneously, generating 18+ `security.camera.observation` events within 1 second. Combined with NPC observation events and Heat updates, the event bus may hit its 200/s limit.

**Detection:** Event bus queue depth monitor exceeds 200; events dropped.

**Mitigation:**
- Camera observation cooldown: each camera can generate at most 2 observations per second
- Burst batching: during portal formation, observations are batched into 5-event bursts with 200ms spacing
- Priority filtering: Critical events (portal state) always processed; Low priority (motion) dropped during burst
- Evidence processor: aggregate similar observations from multiple cameras into single evidence record

### Issue 3: Billboard Performance Spike During Night + Anomaly VFX

**Priority:** HIGH
**Description:** If the demo is run at night (not default, but possible in testing), all hero billboards are at maximum brightness, portal VFX is active, anomaly shimmer is active, and particle effects are at maximum. Combined GPU load may exceed billboard 2ms budget.

**Detection:** GPU profiler shows billboard render pass > 2ms; FPS drops.

**Mitigation:**
- Show Director Event mode reduces max concurrent full-video to 2 (from 4) when anomaly active
- Anomaly VFX and billboard rendering share particle system budget; anomaly takes priority
- Emergency mode triggers at FPS < 35, demoting all billboards to static
- Night-specific: far billboard spill lights limited to 4 (nearest)

### Issue 4: NPC Pathing Through Anomaly Zone

**Priority:** MEDIUM
**Description:** Background NPCs following pre-calculated paths may attempt to walk through the anomaly zone, ignoring the avoidance behavior. This could happen if the path was calculated before the anomaly appeared.

**Detection:** NPCs walking through visual distortion; no avoidance observed.

**Mitigation:**
- Anomaly zone dynamically modifies navmesh: mark anomaly area as high-cost (cost multiplier 100x)
- Path invalidation: when anomaly spawns, all active paths within 30m are recalculated
- Fallback: NPCs inside anomaly zone when it spawns get force-rerouted immediately
- Exception: Hero NPCs may intentionally enter zone (investigation behavior)

### Issue 5: Portal VFX Performance Cost at Peak Crowd

**Priority:** MEDIUM
**Description:** Portal formation involves particle effects, energy vortex shader, and light emissions. At peak crowd times (1500 NPCs), the combined rendering cost of portal VFX + crowd may spike above budget.

**Detection:** FPS drops to < 35 during portal formation; GPU profiler shows VFX + NPC rendering exceeding budget.

**Mitigation:**
- Portal formation triggers Show Director Event mode: NPC LOD distances reduced by 20%
- Background NPCs beyond 30m switch to particle representation during portal formation
- Portal VFX has three quality tiers: High (normal), Medium (fewer particles, simpler shader), Low (minimal particles, no volumetric)
- Auto-select VFX tier based on current FPS headroom

### Issue 6: Ledger Write Speed During Evidence Burst

**Priority:** MEDIUM
**Description:** The portal formation evidence burst (5+ observations) plus Heat updates plus authority dispatch events may require 10-20 ledger writes within 2-3 seconds. If ledger writes are synchronous, this could cause frame hitches.

**Detection:** Frame time spikes during evidence burst; ledger write times > 1ms per write.

**Mitigation:**
- Ledger writes are asynchronous: events queued for write on background thread
- Batch write: evidence burst events are batched into single disk write operation
- Write-ahead buffer: 100 events buffered in memory before forced disk flush
- Emergency: if write queue exceeds 50 events, defer non-critical writes (motion events)

### Issue 7: Hero NPC Decision Quality Near Anomaly

**Priority:** MEDIUM
**Description:** Hero NPCs encountering the anomaly are facing a novel stimulus their behavior trees may not handle gracefully. Dr. Lin should observe scientifically, Lens should film, Detective Vasquez should investigate cautiously. If behavior trees are incomplete, heroes may default to generic "idle" behavior, breaking immersion.

**Detection:** Hero NPCs standing idle during anomaly; behavior tree debug shows fallback to default branch.

**Mitigation:**
- Pre-author anomaly-specific behavior branches for each hero NPC in slice
- "Anomaly encounter" behavior set: approach cautiously (authority), observe and record (network), flee then report (civilian), assess opportunity (criminal)
- Fallback behavior: if no anomaly-specific branch, default to "curious civilian" (approach to 15m, observe, then leave)
- QA protocol: manually verify each hero NPC's response during anomaly sequence

### Issue 8: Audio Overlap at Anomaly + Crowd + Sirens + Portal

**Priority:** MEDIUM
**Description:** During the portal formation sequence, multiple audio layers overlap: anomaly hum, crowd panic sounds, police sirens, portal harmonic drone, wind suction, and formation energy burst. Without careful mixing, the audio becomes an unintelligible wall of noise.

**Detection:** Audio review; player cannot distinguish key sounds; audio clipping detected.

**Mitigation:**
- Priority-based audio ducking: portal sounds duck crowd sounds by -6dB, sirens duck by -3dB
- Anomaly hum frequency specifically avoids siren frequency range (no masking)
- Max simultaneous crowd audio sources: 8 (excess NPCs use visual-only panic, no audio)
- Portal formation: brief audio "silence dip" (250ms) before THOOM impact for dramatic effect
- Master limiter on audio bus to prevent clipping

### Issue 9: Seam Visibility at S10 During Portal Sequence

**Priority:** LOW-MEDIUM
**Description:** Seam S10 (44th St portal zone) transitions from construction barrier to portal entrance. During the transition, the barrier dissolves and portal VFX replaces it. If timing is off, the player may see the seam's raw edge (void behind the barrier) before VFX covers it.

**Detection:** Visible void/skybox behind dissolving barrier; edge of world visible.

**Mitigation:**
- Barrier dissolve does not begin until portal VFX covers the seam area (VFX renders first, barrier fades second)
- Safety geometry: a black plane sits behind the barrier, visible only during transition, preventing void sightline
- Portal VFX radius (3m) exceeds seam width (2m): VFX always fully covers the seam edge
- If VFX fails to load: barrier remains (portal cannot form, fallback to "anomaly failed to stabilize" narrative)

### Issue 10: Artifact Signature Detection Range Calibration

**Priority:** LOW
**Description:** The artifact emits a signature detectable by CCTV within 5m. If this range is too large, the player is constantly detected and cannot move freely after exiting the portal. If too small, the mechanic is irrelevant. Calibration is needed.

**Detection:** Player feedback during testing; detection event frequency analysis.

**Mitigation:**
- Default range: 5m (as specified)
- Tunable parameter: `artifact_detection_radius` exposed in config file
- CCTV detection of artifact has 0.6 confidence (not guaranteed on every scan)
- Signature fades over 2 hours sim-time: range shrinks linearly (5m -> 0m)
- Player can actively suppress signature by staying in crowds (crowd EM noise provides cover, detection confidence -0.2)
- QA test: count detections during 5-minute walk through slice post-portal. Target: 2-5 detections (not 0, not 20+)

---

## 7. Issue Resolution Workflow

```
ISSUE RESOLUTION PROCESS:

  1. Issue detected during demo run
  2. Issue logged with:
     - Build number
     - Timestamp in demo
     - Description
     - Screenshot/video if visual
     - Performance data if FPS-related
     - Severity: BLOCKER / HIGH / MEDIUM / LOW
  3. Issue triaged by lead:
     - BLOCKER: fix before next demo attempt
     - HIGH: fix within 2 days
     - MEDIUM: fix within sprint
     - LOW: backlog
  4. Fix implemented
  5. Fix verified by re-running demo script
  6. Regression pack compared to previous passing build
  7. Issue closed when demo passes clean
```

---

## 8. Demo Run Log Template

Each demo run is documented using this log:

```
DEMO RUN LOG
=============
Build:          [build number]
Date:           [date]
Runner:         [name]
Seed:           42
Pre-conditions: [PASS / FAIL — if FAIL, list failures and abort]

Beat 1 (T+0:00): [PASS / FAIL] Notes: ___
Beat 2 (T+0:30): [PASS / FAIL] Notes: ___
Beat 3 (T+0:45): [PASS / FAIL] Notes: ___
Beat 4 (T+1:00): [PASS / FAIL] Notes: ___
Beat 5 (T+1:15): [PASS / FAIL] Notes: ___
Beat 6 (T+1:45): [PASS / FAIL] Notes: ___
Beat 7 (T+2:45): [PASS / FAIL] Notes: ___
Beat 8 (T+3:00): [PASS / FAIL] Notes: ___
Beat 9 (T+3:30): [PASS / FAIL] Notes: ___
Beat 10 (T+3:45): [PASS / FAIL] Notes: ___

Overall: [PASS / FAIL]
FPS min: ___  FPS avg: ___  FPS max: ___
Memory peak: ___ MB
Deadlocks: ___
Events logged: ___
Issues found: [list with severity]

Regression captures saved to: [path]
Compared to baseline build: [build number]
Regression result: [PASS / WARNING / FAIL]
```

---

## 9. Appendix: Quick Reference Card

For use during live demo runs. Print this page.

```
╔══════════════════════════════════════════════════════════════╗
║              THE 5-MINUTE PROOF — QUICK REFERENCE           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  START: 46th/Broadway, face south, 2:00 PM, all Heat = 0   ║
║                                                              ║
║  0:00  Walk south on Broadway                                ║
║  0:30  Cross at 45th (wait for signal)                      ║
║  0:45  Approach TKTS steps                                   ║
║  1:00  ANOMALY TRIGGERS — look toward 44th St               ║
║  1:15  Observe crowd reaction                                ║
║  1:30  Authority dispatched                                  ║
║  1:45  Walk toward anomaly at 44th                          ║
║  2:00  Police arrive                                         ║
║  2:15  PORTAL FORMS                                          ║
║  2:30  Enter portal                                          ║
║  2:45  Inside pocket — walk to artifact                     ║
║  3:00  Grab artifact — DESTABILIZATION BEGINS               ║
║  3:15  Run to exit                                           ║
║  3:30  EXIT PORTAL — back in Times Square                   ║
║  3:45  Observe aftermath                                     ║
║  4:00  Walk north, blend into crowd                         ║
║  4:30  Return to 44th — verify persistence                  ║
║  5:00  END — check ledger, heat, inventory                  ║
║                                                              ║
║  PASS = all verify steps green + FPS >= 30 + 0 deadlocks   ║
╚══════════════════════════════════════════════════════════════╝
```

---

*End of document. This concludes the Part 12 deliverables for the Times Square slice.*
