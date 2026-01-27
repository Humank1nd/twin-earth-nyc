# NPC Tier Config v0

**Document:** Twin Earth NYC — Part 12, File 3 of 6
**Status:** v0 Draft
**Scope:** Population targets, spawn points, attraction points, behavior presets, deadlock metrics

---

## 1. Overview

The Times Square slice is the most pedestrian-dense environment in Twin Earth NYC. Real-world Times Square sees approximately 330,000 pedestrians daily, with peak densities exceeding 2 people per square meter on sidewalks. The NPC system must simulate this density convincingly while maintaining performance targets and supporting gameplay interactions (anomaly reactions, authority behavior, evidence generation).

This document defines:
- How many NPCs exist at each time of day
- Where they spawn and despawn
- What attracts them within the slice
- How they behave by type
- How deadlocks are detected and resolved

---

## 2. Population Targets

### 2.1 Time-of-Day Population Schedule

All counts represent the **steady-state target** for NPCs simultaneously active within the slice boundaries.

| Time Period | Hours | Background Peds | Background Vehicles | Hero Peds | Hero Vehicles | Authority Units | Total Entities |
|-------------|-------|----------------|--------------------:|----------:|--------------:|----------------:|---------------:|
| **Pre-dawn** | 02:00-07:00 | 100 | 10 | 5 | 1 | 2 patrol | 118 |
| **Morning rush** | 07:00-09:00 | 800 | 60 | 10 | 2 | 2 patrol | 874 |
| **Midday** | 10:00-14:00 | 1,200 | 40 | 15 | 2 | 3 patrol | 1,260 |
| **Afternoon** | 14:00-17:00 | 1,000 | 50 | 12 | 2 | 2 patrol | 1,066 |
| **Evening rush** | 17:00-19:00 | 1,500 | 70 | 15 | 3 | 3 patrol | 1,591 |
| **Theater** | 19:00-22:00 | 1,200 | 30 | 15 | 2 | 4 patrol | 1,251 |
| **Late night** | 22:00-02:00 | 400 | 20 | 8 | 1 | 3 patrol | 432 |

### 2.2 Transition Ramps

Population changes between periods are not instant. The system ramps linearly over 30 minutes at each transition boundary.

```
POPULATION RAMP:

  current_population(category) = lerp(
      previous_period.target(category),
      current_period.target(category),
      clamp01((current_time - period_start) / 30_minutes)
  )

  Example: Morning rush (07:00) to Midday (10:00)
    - At 09:30: still at morning rush targets (800 bg peds)
    - At 09:45: ramping (800 -> 1200, at 50% = 1000 bg peds)
    - At 10:00: at midday targets (1200 bg peds)
    - Ramp window: 09:30 to 10:00 (30 min before period start)

  EXCEPTION: Pre-dawn -> Morning rush ramp starts at 06:30
             (people start arriving before "rush hour")
```

### 2.3 NPC Categories Defined

| Category | Description | AI Level | LOD Tiers | Persistence |
|----------|-------------|----------|-----------|-------------|
| **Background Pedestrian** | Anonymous city-goers filling sidewalks | Heuristic (Near) / Flow (Mid) / Particle (Far) | 3 mesh tiers + particle | None (despawn on exit) |
| **Background Vehicle** | Taxis, cars, buses, trucks following traffic | Waypoint + signal compliance | 2 mesh tiers | None (despawn on exit) |
| **Hero Pedestrian** | Named NPCs with schedules, memory, faction ties | Full behavior tree (Near) / Simplified (Mid) | 2 mesh tiers (high detail) | Cross-session memory |
| **Hero Vehicle** | Specific vehicles (police cruiser, Strange's car, etc.) | Full behavior + dispatch | 1 mesh tier (always high) | Session-persistent |
| **Authority Unit** | NYPD patrol (foot/vehicle), security, emergency | Full behavior tree + dispatch | 1 mesh tier (always high) | Session-persistent |

---

## 3. Spawn Points

### 3.1 Pedestrian Spawn Points

NPCs are spawned at slice boundaries and key interior points. They walk through the slice and despawn at the opposite boundary or at attraction points that serve as "exits" (subway, buildings).

| Spawn ID | Type | Location | Primary Direction | Peak Rate | Minimum Rate |
|----------|------|----------|-------------------|-----------|-------------|
| SP_PED_N01 | Pedestrian | 47th St, Broadway sidewalk (west) | Southbound | 25/min | 3/min |
| SP_PED_N02 | Pedestrian | 47th St, 7th Ave sidewalk (east) | Southbound | 25/min | 3/min |
| SP_PED_S01 | Pedestrian | 42nd St, Broadway sidewalk (west) | Northbound | 30/min | 4/min |
| SP_PED_S02 | Pedestrian | 42nd St, 7th Ave sidewalk (east) | Northbound | 30/min | 4/min |
| SP_PED_E01 | Pedestrian | 7th Ave, cross-street sidewalks (east edge) | Westbound | 15/min | 2/min |
| SP_PED_E02 | Pedestrian | 7th Ave, mid-block (east edge) | Westbound | 15/min | 2/min |
| SP_PED_W01 | Pedestrian | Broadway, cross-street sidewalks (west edge) | Eastbound | 15/min | 2/min |
| SP_PED_W02 | Pedestrian | Broadway, mid-block (west edge) | Eastbound | 15/min | 2/min |
| SP_PED_SUB | Pedestrian | 42nd St subway exits (3 stairways) | Various | 40/min (burst capable) | 5/min |

**Subway burst behavior:**
```
SUBWAY SPAWN BURSTS:

  The 42nd St subway spawn point simulates train arrivals.
  Every 5-8 minutes (randomized), a burst of 30-50 pedestrians
  emerges over 60 seconds.

  burst_schedule:
    interval: uniform_random(300s, 480s)
    burst_size: uniform_random(30, 50)
    burst_duration: 60s
    spawn_rate_during_burst: burst_size / burst_duration

  Theater time special:
    At 19:00 and 19:30, double-size bursts (60-80 people)
    simulating theater-goers arriving.
```

### 3.2 Vehicle Spawn Points

| Spawn ID | Type | Location | Direction | Lanes | Peak Rate | Minimum Rate |
|----------|------|----------|-----------|-------|-----------|-------------|
| SP_VEH_N01 | Vehicle | 47th St, 7th Ave lanes | Southbound (7th Ave is one-way south) | 3 | 10/min | 2/min |
| SP_VEH_S01 | Vehicle | 42nd St, Broadway lanes | Northbound (Broadway is one-way north in this section) | 2 | 8/min | 1/min |
| SP_VEH_S02 | Vehicle | 42nd St, cross-street | Westbound | 1 | 5/min | 1/min |
| SP_VEH_N02 | Vehicle | 47th St, cross-street | Eastbound | 1 | 2/min | 0/min |

**Vehicle type distribution:**
| Vehicle Type | Percentage | Notes |
|-------------|-----------|-------|
| Yellow taxi | 40% | Iconic NYC, may stop for passengers |
| Sedan/SUV | 25% | Generic civilian vehicles |
| Rideshare (black car) | 15% | Uber/Lyft-style vehicles |
| Bus (MTA) | 5% | Large, slow, fixed route |
| Delivery truck | 10% | Box trucks, delivery vans |
| Police/Emergency | 5% | Authority vehicles, see Authority section |

### 3.3 Despawn Rules

```
DESPAWN RULES:

  Background Pedestrians:
    - Despawn when crossing a slice boundary going outward (3m past seam mask)
    - Despawn when entering a "sink" building door (walk through door, fade)
    - Despawn if stuck (velocity < 0.01 m/s for > 30s) — log and remove
    - Despawn if fallen below world plane (error recovery)
    - Never despawn while in player's Near band (visible pop)
    - Instead: walk behind occlusion (vehicle, column, crowd) then despawn

  Background Vehicles:
    - Despawn when crossing slice boundary
    - Despawn if gridlocked for > 3 signal cycles (error recovery)
    - Turn off at cross-streets to exit slice

  Hero NPCs:
    - NEVER despawn due to population management
    - May exit slice via boundary (tracked, will return on schedule)
    - If stuck: force-teleport to nearest valid navmesh point, log error

  Authority Units:
    - Persistent within session
    - May be dispatched out of slice (replaced by new unit if below minimum)
```

---

## 4. Attraction Points

Attraction points are locations within the slice that draw pedestrians, creating natural crowd clustering. Each point has a strength (how strongly it pulls), a type (what NPCs do there), and a schedule (when it is active).

### 4.1 Attraction Point Inventory

| Attraction ID | Location | Strength | Type | Schedule | Capacity |
|---------------|----------|----------|------|----------|----------|
| ATT_01 | TKTS Red Steps | **High** | Tourist gathering | All day, peak 11:00-14:00 | 80 NPCs |
| ATT_02 | One Times Square base | **Medium** | Photo spot | All day | 30 NPCs |
| ATT_03 | 42nd/Broadway corner (SE) | **High** | Crossing convergence | Continuous | 50 NPCs (transient) |
| ATT_04 | 45th/Broadway corner | **Medium** | Crossing convergence | Continuous | 40 NPCs (transient) |
| ATT_05 | Kiosk — TKTS area | **Low** | Brief interaction | 08:00-22:00 | 5 NPCs |
| ATT_06 | Kiosk — 42nd/Broadway | **Low** | Brief interaction | 08:00-22:00 | 5 NPCs |
| ATT_07 | Kiosk — 44th/7th Ave | **Low** | Brief interaction | 08:00-22:00 | 5 NPCs |
| ATT_08 | Kiosk — 45th pedestrian zone | **Low** | Brief interaction | 08:00-22:00 | 5 NPCs |
| ATT_09 | Street performer spot — 44th plaza | **Medium** | Entertainment cluster | 12:00-22:00 | 25 NPCs |
| ATT_10 | Street performer spot — 46th/Broadway | **Medium** | Entertainment cluster | 12:00-22:00 | 25 NPCs |
| ATT_11 | Kiosk — 46th/Broadway | **Low** | Brief interaction | 08:00-22:00 | 5 NPCs |
| ATT_12 | Father Duffy Statue | **Low** | Photo spot | All day | 10 NPCs |

### 4.2 Attraction Behavior

```
ATTRACTION PULL MODEL:

  For each background NPC on spawn or at decision point:

    1. Determine NPC preset (commuter, tourist, shopper, etc.)
    2. Based on preset, calculate attraction sensitivity:
        - Commuter: 0.1 (rarely attracted, mostly direct path)
        - Tourist: 0.8 (strongly attracted)
        - Shopper: 0.3 (attracted to kiosks and stores)
        - Performer audience: 0.9 (seeks performer spots)
        - Vendor/worker: 0.0 (not attracted, has fixed location)

    3. For each active attraction point within 100m:
        pull = attraction.strength * npc.sensitivity
               * schedule_factor(attraction, current_time)
               * (1.0 - (current_occupancy / capacity))  // crowding reduces pull
               / distance_squared(npc, attraction)

    4. If max(pull) > threshold (0.01):
        NPC routes toward attraction, spends time_at_attraction, then resumes

  time_at_attraction by type:
    - Tourist gathering: 60-300s (1-5 minutes, taking photos, sitting on steps)
    - Photo spot: 15-60s (take photo, move on)
    - Crossing convergence: 0s (just passing through, attraction is about flow)
    - Brief interaction: 10-30s (buy something, look at kiosk)
    - Entertainment cluster: 30-180s (watch performer)
```

### 4.3 Attraction Point Map

```
                      47th Street
     _____________________|_____________________
    |                     |                      |
    |                     |                      |
    |   ATT_10            |                      |
    |   (performer)       |                      |
    |            46th St  |                      |
    |   ATT_11            |                      |
    |   (kiosk)           |                      |
    |                     |                      |
    |            45th St  |                      |
    |   ATT_04            |                      |
    |   (crossing)        |                      |
    |                     |                      |
    |        ATT_01 (TKTS Red Steps)             |
    |        ATT_12 (Father Duffy Statue)        |
    |        ATT_05 (kiosk)                      |
    |        ATT_08 (kiosk)                      |
    |                     |                      |
    |            44th St  |   ATT_07             |
    |   ATT_09            |   (kiosk)            |
    |   (performer)       |                      |
    |                     |                      |
    |            43rd St  |                      |
    |                     |                      |
    |        ATT_02 (One Times Square base)      |
    |                     |                      |
    |            42nd St  |                      |
    |   ATT_03  ATT_06    |                      |
    |   (cross) (kiosk)   |                      |
    |_____________________|______________________|

    WEST (Broadway)              EAST (7th Ave)
```

---

## 5. Behavior Presets

### 5.1 Background NPC Presets

| Preset | % of Background | Walk Speed | Pattern | Attraction Sensitivity | Visual Markers | Special Behavior |
|--------|----------------|-----------|---------|----------------------|----------------|-----------------|
| **Commuter** | 40% | 1.4 m/s | Direct A-to-B, minimal stops | 0.1 | Business attire, carrying briefcase/bag, looking forward | Ignores most stimuli; uses phone while walking; jaywalks if gap available |
| **Tourist** | 30% | 0.8 m/s | Wandering, frequent stops at attractions | 0.8 | Casual clothes, camera/phone out, looking up at billboards | Takes photos (stops, holds phone up 3-5s); travels in groups of 2-4; reads maps/phones |
| **Shopper** | 15% | 1.0 m/s | Enters/exits door zones on buildings | 0.3 | Carrying shopping bags (visual only) | Pauses at store windows (5-10s); enters/exits shop doors periodically |
| **Performer Audience** | 10% | 0.2 m/s (standing) | Clusters around performer spots | 0.9 | Standing, facing performer, occasionally clapping | Claps at intervals; drops "tip" (animation); leaves after 30-180s |
| **Vendor/Worker** | 5% | 0.6 m/s | Stationary or short patrol | 0.0 | Uniform or apron; positioned near shops/carts | Stays within 10m of assigned location; may interact with shoppers |

### 5.2 Preset Distribution by Time Period

| Time Period | Commuter | Tourist | Shopper | Performer Audience | Vendor/Worker |
|-------------|---------|---------|---------|-------------------|---------------|
| Pre-dawn | 20% | 5% | 0% | 0% | 75% (cleanup crews) |
| Morning rush | 70% | 10% | 5% | 0% | 15% |
| Midday | 25% | 45% | 15% | 10% | 5% |
| Afternoon | 30% | 35% | 20% | 10% | 5% |
| Evening rush | 60% | 15% | 10% | 10% | 5% |
| Theater | 20% | 40% | 10% | 20% | 10% |
| Late night | 30% | 30% | 5% | 20% | 15% (bar/restaurant) |

### 5.3 Background NPC Navigation

```
NAVIGATION RULES:

  Sidewalk preference:
    - NPCs walk on sidewalks, not in streets
    - Jaywalking: only "Commuter" preset, only when no vehicles within 30m
      and no signal within 20m. Probability: 5% per crossing opportunity.

  Signal compliance:
    - Target: >95% of NPCs wait for WALK signal
    - Implementation: NPCs check signal state when approaching crosswalk.
      If DON'T WALK: 95% wait, 5% jaywalk (reduced to 2% if vehicle visible)
    - Waiting behavior: NPCs queue at curb edge, face crossing direction,
      some check phones, some look at billboards

  Collision avoidance:
    - RVO (Reciprocal Velocity Obstacles) for Near-band NPCs
    - Flow-field following for Mid-band NPCs
    - No collision for Far-band (particle representation)
    - Personal space: 0.5m radius (NPCs try to maintain this gap)
    - Failure mode: if gap impossible (dense crowd), NPCs slow to crowd speed

  Curb behavior:
    - NPCs step up/down at curbs (15cm step animation)
    - No jumping off curbs (adults)
    - Step up: slight pause, step animation
    - Step down: continuous motion, step-down animation
```

### 5.4 Hero NPC Specifications

Hero NPCs are named characters with full behavior trees, cross-session memory, and faction associations. They are placed in the slice for the demo scenario.

| Hero ID | Name | Faction | Location (default) | Schedule | Role in Demo |
|---------|------|---------|-------------------|----------|-------------|
| HERO_01 | Detective Ray Vasquez | Authority (NYPD) | Patrol route: 42nd-45th | Morning-Evening shift | First responder to anomaly |
| HERO_02 | Dr. Mei Lin | Strange's Network | Near 44th St | Appears 1:00 PM, stays until anomaly | Observes anomaly, provides exposition |
| HERO_03 | "Lens" (Marcus Cole) | Strange's Network | TKTS steps area | Afternoon, filming | Captures evidence on personal camera |
| HERO_04 | Officer Tanya Brooks | Authority (NYPD) | 45th/7th patrol | Afternoon shift | Secondary responder |
| HERO_05 | Jimmy "Two-Phones" | Criminal Network | 43rd/Broadway | Sporadic appearances | Notices portal, reports to faction |
| HERO_06 | Sarah Chen | Civilian (journalist) | Roaming slice | Midday-evening | Investigates aftermath |
| HERO_07 | "Big Mike" (Michael Torres) | Vendor (neutral) | Hot dog cart, 45th/Broadway | 10:00-22:00 | Witness, provides street-level intel |
| HERO_08 | Anya Petrov | Strange's Network | Variable (arrives during anomaly) | Event-triggered | Portal specialist, arrives to assess |
| HERO_09 | Sgt. Bill Hammond | Authority (NYPD) | 42nd precinct | On-call | Dispatched during High Heat |
| HERO_10 | "Ghost" (unknown real name) | Unknown faction | Shadows, 44th alley area | Night only (normally); appears during anomaly | Mysterious observer, possible rival |

### 5.5 Hero NPC Behavior Trees (Summary)

```
HERO NPC BEHAVIOR TREE STRUCTURE:

  ROOT
  ├── SELECTOR: Priority-based
  │   ├── [1] Emergency Response (if heat > 0.7 or direct threat)
  │   │   └── Authority: cordon + dispatch
  │   │   └── Civilian: flee or hide
  │   │   └── Network: observe + report
  │   │
  │   ├── [2] Event Response (if anomaly active or heat > 0.2)
  │   │   └── Authority: investigate, approach cautiously
  │   │   └── Network: observe from distance, take readings
  │   │   └── Criminal: assess opportunity, report to faction
  │   │   └── Civilian: rubberneck or avoid based on personality
  │   │
  │   ├── [3] Scheduled Activity (if within schedule window)
  │   │   └── Execute schedule waypoint sequence
  │   │   └── Interact with environment (vendor: serve, detective: patrol)
  │   │
  │   └── [4] Idle / Default
  │       └── Wander within territory
  │       └── React to ambient stimuli
  │       └── Check phone, talk to passersby, etc.
  │
  └── PARALLEL: Always running
      ├── Memory recording (observe events, store in per-NPC memory)
      ├── Relationship tracking (player proximity, interaction history)
      └── Faction communication (report significant observations)

HERO NPC MEMORY MODEL:
  - Each hero NPC has a memory store (array of observation records)
  - Observations: timestamp, location, entities seen, event type, emotional weight
  - Memory capacity: 100 most recent observations (oldest pruned)
  - Cross-session: memory persists between play sessions
  - Decay: emotional weight decays over sim-time
    (dramatic events stay vivid longer)
  - Habits: repeated observations strengthen behavioral patterns
    (e.g., if hero sees anomalies frequently, they become less fearful,
     more investigative)
```

---

## 6. Authority NPC Detailed Specification

### 6.1 Patrol Routes

| Unit ID | Type | Default Route | Speed | Equipment |
|---------|------|--------------|-------|-----------|
| AUTH_01 | Foot patrol | 42nd -> 44th -> 42nd (Broadway side) | 1.0 m/s | Radio, flashlight, sidearm |
| AUTH_02 | Foot patrol | 45th -> 47th -> 45th (7th Ave side) | 1.0 m/s | Radio, flashlight, sidearm |
| AUTH_03 | Vehicle patrol | Loop: 47th south on 7th, east on 42nd, exit | 8 m/s (20mph) | Cruiser, radio, lights |
| AUTH_04 | Foot patrol (theater detail) | TKTS area + 44th-46th | 0.8 m/s | Radio, flashlight |

### 6.2 Authority Response Escalation

```
AUTHORITY RESPONSE LEVELS:

  ROUTINE (Heat 0.0 - 0.2):
    - Normal patrol routes
    - Respond to minor incidents (lost tourist, minor argument)
    - Response time: 2-5 minutes (walk to location)

  ALERT (Heat 0.2 - 0.4):
    - Patrol routes tighten (closer to anomaly area)
    - Investigation posture: approach cautiously, radio for info
    - Additional unit requested from outside slice (arrives in 5 min)
    - Response time: 1-3 minutes

  ACTIVE (Heat 0.4 - 0.7):
    - Cordon established around incident
    - Crowd management: push civilians back
    - 2 additional units dispatched
    - Radio chatter increases (audible to player)
    - Response time: 30s-1 minute

  CRITICAL (Heat 0.7 - 0.9):
    - Full response: all available units converge
    - Road closures at slice boundaries
    - Crowd evacuation orders
    - Helicopter consideration (audio only, not rendered)
    - ESU (Emergency Service Unit) dispatched (arrives in 3 min)
    - Response time: immediate (all units redirect)

  CRISIS (Heat 0.9+):
    - Military consideration flagged (narrative event)
    - Full lockdown of slice
    - All civilian NPCs in evacuation mode
    - All authority units in containment mode
    - Player freedom severely restricted (but not prevented)
```

---

## 7. Deadlock Detection and Resolution

### 7.1 Definition

A **deadlock** occurs when a cluster of 3 or more NPCs all have velocity below 0.05 m/s for more than 10 consecutive seconds, AND at least one NPC in the cluster has a destination it has not reached.

### 7.2 Detection System

```
DEADLOCK DETECTION:

  Running continuously at 1Hz (once per second):

  1. Identify all NPCs with velocity < 0.05 m/s
  2. Cluster these NPCs spatially (within 2m of each other)
  3. For each cluster of size >= 3:
     a. Check if cluster has existed for > 10 seconds
     b. Check if any NPC in cluster has an active navigation goal
     c. If both conditions met: DEADLOCK DETECTED

  Data structure:
    deadlock_candidates = {}  // NPC_ID -> stuck_time_seconds

    each second:
      for npc in all_active_npcs:
        if npc.velocity < 0.05:
          deadlock_candidates[npc.id] += 1
        else:
          remove deadlock_candidates[npc.id]

      clusters = spatial_cluster(
        [npc for npc in deadlock_candidates if deadlock_candidates[npc] > 10],
        radius=2.0
      )

      for cluster in clusters:
        if len(cluster) >= 3 and any(npc.has_nav_goal for npc in cluster):
          trigger_deadlock_resolution(cluster)
          log_deadlock(cluster)
```

### 7.3 Resolution Protocol

```
DEADLOCK RESOLUTION:

  For background NPCs:
    1. Identify the slowest NPC in the cluster (lowest velocity)
    2. Force-reroute: assign a new random destination 20m away from cluster
    3. Temporarily increase this NPC's collision avoidance radius to 0.1m
       (allow it to push through)
    4. After 5 seconds, restore normal collision avoidance
    5. If deadlock persists after 5s: despawn the slowest NPC behind
       nearest occlusion, spawn replacement at nearest spawn point

  For hero NPCs:
    1. Do NOT force-reroute or despawn
    2. Log the deadlock for design review
    3. Apply gentle nudge force (0.5 m/s) in the direction of their goal
    4. If hero NPC is stuck for > 30s: teleport to nearest valid navmesh
       point in the direction of their goal (only if no player line-of-sight)
    5. Generate incident report for QA

  For vehicles:
    1. If vehicle stuck at intersection for > 2 signal cycles: force advance
       through intersection (ignore current signal)
    2. If vehicle stuck mid-block: despawn behind nearest large occlusion
    3. Log for traffic system tuning
```

### 7.4 Deadlock Metrics and Targets

| Metric | Target | Measurement Window | Action if Exceeded |
|--------|--------|-------------------|-------------------|
| Deadlock rate (background) | < 0.1% per 10 min | Rolling 10-minute window | Tune navmesh + attraction capacity |
| Deadlock rate (hero) | 0% | Per session | Must fix before ship |
| Deadlock rate (vehicle) | < 0.05% per 10 min | Rolling 10-minute window | Tune signal timing + lanes |
| Resolution success rate | > 99% | Per deadlock event | Improve resolution algorithm |
| Mean time to resolution | < 5 seconds | Per deadlock event | Improve detection speed |

### 7.5 Known Deadlock Risk Zones

| Zone | Location | Risk | Cause | Mitigation |
|------|----------|------|-------|------------|
| DZ_01 | TKTS steps base | **High** | Tourist attraction + crossing flow converge | Separate attraction area from crosswalk flow; directional flow on steps |
| DZ_02 | Bowtie intersection | **High** | Broadway diagonal creates awkward pedestrian crossing angles | Wide crosswalks, clear signal phasing, flow lanes painted on ground |
| DZ_03 | 42nd/Broadway corner | **Medium** | High crossing volume + subway burst | Staggered signal timing; subway spawn with directional bias |
| DZ_04 | 44th portal zone during anomaly | **Medium** | Rubbernecking NPCs + avoidance NPCs conflict | Rubberneck ring enforced at 15m minimum; avoidance NPCs rerouted to side streets |
| DZ_05 | Street performer spots | **Low** | Audience cluster + foot traffic | Performer spots placed 5m from sidewalk edge; audience faces away from flow |

---

## 8. NPC Visual Configuration

### 8.1 Mesh LOD Tiers

| Category | Near (0-30m) | Mid (30-150m) | Far (150m+) |
|----------|-------------|---------------|-------------|
| Hero NPC | 8,000 triangles, unique textures | 3,000 triangles, shared atlas | N/A (hero stays near or despawns) |
| Background NPC | 3,000 triangles, shared textures (32 variants) | 800 triangles, 8 body variants | Particle billboard (2 triangles) |
| Authority NPC | 8,000 triangles, unique uniform | 3,000 triangles, uniform atlas | 800 triangles (visible at distance due to uniform) |
| Vehicle (any) | 5,000 triangles, unique per type | 1,500 triangles, type atlas | 200 triangles (box + wheels) |

### 8.2 Background NPC Variety

To avoid the "clone army" effect, background NPCs are assembled from modular parts:

| Component | Variants | Notes |
|-----------|---------|-------|
| Body type | 8 | Male/female x 4 body shapes |
| Skin tone | 6 | Diverse range |
| Hair | 12 | Various styles and colors |
| Top (clothing) | 20 | Seasonal variants (summer/winter sets) |
| Bottom (clothing) | 15 | Pants, skirts, shorts |
| Footwear | 8 | Sneakers, dress shoes, boots, sandals |
| Accessories | 10 | Bags, hats, scarves, headphones, cameras |

**Total unique combinations:** 8 x 6 x 12 x 20 x 15 x 8 x 10 = 13,824,000 theoretical combinations. In practice, the system generates 200 unique presets at scene load and instances from that pool.

---

## 9. Performance Notes

### 9.1 NPC CPU Budget

| System | Budget | Notes |
|--------|--------|-------|
| Hero NPC AI (full tree) | 0.1ms per hero | 15 heroes = 1.5ms max |
| Background NPC navigation (Near) | 0.005ms per NPC | ~200 near NPCs = 1.0ms |
| Background NPC flow-follow (Mid) | 0.001ms per NPC | ~500 mid NPCs = 0.5ms |
| Background NPC particle (Far) | 0.0001ms per NPC | ~500 far NPCs = 0.05ms |
| Deadlock detection | 0.1ms flat | Runs at 1Hz |
| Spawn/despawn management | 0.2ms flat | Runs at 2Hz |
| **Total NPC AI budget** | **3.35ms max** | **Target: < 2.0ms steady state** |

### 9.2 NPC Rendering Budget

| System | Budget | Notes |
|--------|--------|-------|
| Hero NPC meshes | 120K triangles | 15 x 8,000 |
| Near background NPC meshes | 600K triangles | 200 x 3,000 |
| Mid background NPC meshes | 400K triangles | 500 x 800 |
| Far background NPC particles | 1K triangles | 500 x 2 |
| Vehicles (all tiers) | 300K triangles | Mixed |
| **Total NPC render budget** | **~1.42M triangles** | **Fits within Near+Mid geometry budgets** |

---

*End of document. Next: IoT + Evidence + Ledger v0.*
