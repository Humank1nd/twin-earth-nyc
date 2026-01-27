# Heat + Anomaly + Portal Pocket v0

**Document:** Twin Earth NYC — Part 12, File 5 of 6
**Status:** v0 Draft
**Scope:** Heat implementation, first anomaly specification, first portal pocket specification

---

## 1. Overview

This document specifies the three interconnected supernatural systems as they manifest in the Times Square slice:

1. **Heat** -- the four-channel tension meter that tracks the world's reaction to player and anomaly activity
2. **Anomaly** -- the first reality distortion event, a gravity wobble with visual shimmer at 44th Street
3. **Portal Pocket** -- the first traversable portal leading to an otherworldly pocket dimension

These systems are tightly coupled: anomalies raise Heat, Heat affects world response, and portal activity generates evidence that further elevates Heat. The Times Square slice is the proving ground for this feedback loop.

---

## 2. Heat Implementation (Times Square)

### 2.1 Channel Definitions

Four independent Heat channels track different types of world tension. Each ranges from 0.0 (completely calm) to 1.0 (maximum crisis).

| Channel | Name | What It Measures | Primary Sources | Primary Responders |
|---------|------|-----------------|----------------|-------------------|
| **Physical** | Physical Disruption | Property damage, structural change, collisions | Explosions, forced doors, vehicle accidents, combat | Infrastructure repair, emergency services |
| **Social** | Social Awareness | Public attention, crowd anxiety, media interest | Witnesses, crowd reactions, anomaly visibility, NPC fights | Crowd behavior, media response, rumor spread |
| **Institutional** | Institutional Response | Government/authority awareness and action | Authority dispatch, CCTV alerts, door breaches, evidence | Police, emergency services, government agencies |
| **Ecological** | Ecological Stress | Reality integrity, interdimensional disturbance | Anomalies, portals, artifacts, reality bleed | Anomaly behavior, portal stability, containment |

### 2.2 Initial State

All four channels begin at 0.0 at the start of a clean session. On session load, channels are restored from save with decay applied for elapsed time.

```
INITIAL STATE:
  heat.physical     = 0.0
  heat.social       = 0.0
  heat.institutional = 0.0
  heat.ecological   = 0.0

ON SESSION LOAD:
  for each channel:
    channel.value = saved_value - (decay_rate * elapsed_sim_minutes)
    channel.value = max(0.0, channel.value)
```

### 2.3 Heat Sources (Times Square Slice)

Every action, event, and system interaction that affects Heat is enumerated below. Values are additive and applied immediately on event.

| Source Event | Physical | Social | Institutional | Ecological | Notes |
|-------------|---------|--------|---------------|------------|-------|
| **Vehicle accident** | +0.15 | +0.05 | +0.05 | 0.00 | Two vehicles collide, or vehicle hits object |
| **Door forced** | +0.02 | 0.00 | +0.05 | 0.00 | Player or NPC forces a locked door |
| **NPC fight** | +0.05 | +0.10 | +0.05 | 0.00 | Physical altercation between NPCs |
| **Anomaly shimmer** (appears) | 0.00 | +0.10 | +0.05 | +0.20 | First visual manifestation |
| **Anomaly growth** (per radius doubling) | 0.00 | +0.05 | +0.03 | +0.10 | Ongoing anomaly expansion |
| **Portal opens** | +0.10 | +0.20 | +0.10 | +0.30 | Portal transitions to STABLE state |
| **Portal operation** (player enters/exits) | +0.05 | +0.10 | +0.05 | +0.10 | Each traversal |
| **Artifact imported** (brought from pocket) | +0.02 | +0.05 | +0.02 | +0.15 | Cross-dimensional object enters Hub |
| **Explosion / major damage** | +0.25 | +0.15 | +0.10 | +0.05 | Large-scale physical destruction |
| **Camera jammed** | 0.00 | 0.00 | +0.05 | 0.00 | CCTV disabled by player/NPC |
| **Kiosk spoofed** | 0.00 | +0.05 | +0.03 | 0.00 | False information displayed |
| **Player detected by CCTV with artifact** | 0.00 | +0.02 | +0.03 | +0.05 | Signature picked up by camera |
| **Authority cordon placed** | -0.02 | +0.03 | 0.00 | 0.00 | Reduces Physical, increases Social (visible response) |
| **Authority arrest** | -0.05 | +0.05 | -0.05 | 0.00 | Resolution reduces Physical/Institutional, but Social notices |
| **Crowd evacuation order** | 0.00 | +0.10 | +0.05 | 0.00 | Panic increases Social |
| **Portal collapses** | -0.05 | +0.05 | 0.00 | -0.10 | Portal sealed reduces Physical/Ecological, Social notices |

### 2.4 Heat Decay Rates

Heat naturally decays over time when no new sources are adding to it. Each channel has its own decay rate, reflecting how quickly that type of tension resolves.

| Channel | Decay Rate | Interpretation |
|---------|-----------|---------------|
| **Physical** | -0.02 / minute | Damage gets cleaned up, infrastructure repaired |
| **Social** | -0.01 / minute | People forget slowly, move on |
| **Institutional** | -0.005 / minute | Bureaucracy responds slowly, investigations linger |
| **Ecological** | -0.003 / minute | Reality heals very slowly; interdimensional stress persists |

**Decay implementation:**
```
HEAT DECAY (runs every frame):

  delta_time = frame_time_in_minutes  // e.g., 1/60 for 60fps = 0.000278 min

  for each channel in [physical, social, institutional, ecological]:
    if channel.value > 0:
      channel.value -= channel.decay_rate * delta_time
      channel.value = max(0.0, channel.value)

    // Clamp to [0.0, 1.0]
    channel.value = clamp(channel.value, 0.0, 1.0)

  // Log threshold crossings
  for each channel:
    old_level = get_heat_level(channel.previous_value)
    new_level = get_heat_level(channel.value)
    if old_level != new_level:
      publish("heat.channel.changed", {
        channel: channel.name,
        old_level: old_level,
        new_level: new_level,
        value: channel.value
      })
```

### 2.5 Heat Response Levels

The world responds differently at each Heat level. Responses are driven by the **maximum** across all four channels (composite Heat level).

| Level | Range | Composite Name | Description |
|-------|-------|---------------|-------------|
| **Normal** | 0.0 - 0.2 | Calm | City operating normally |
| **Elevated** | 0.2 - 0.4 | Uneasy | Something is off; subtle changes |
| **High** | 0.4 - 0.7 | Tense | Active incident; significant response |
| **Critical** | 0.7 - 0.9 | Crisis | Major emergency; full mobilization |
| **Crisis** | 0.9 - 1.0 | Extreme | Catastrophic; system breakdown |

### 2.6 Response Behaviors by Level

#### Crowd Response

| Level | Behavior Changes |
|-------|-----------------|
| **Normal** | Normal pedestrian flow. All presets active. Tourists stop at attractions. |
| **Elevated** | Walk speed increases by 10%. Fewer tourists stop at attractions (-30% dwell time). Some NPCs glance over shoulders. |
| **High** | Tourist preset NPCs begin leaving slice (walk toward boundaries). Commuter speed +20%. Crowd avoids Heat epicenter (30m radius). Crossing compliance drops to 85%. |
| **Critical** | Mass movement away from epicenter. Running behavior activated for 30% of NPCs. Tourist and Shopper presets fully evacuate. Only Commuters and Workers remain. Crowd density drops to 40% of normal. |
| **Crisis** | Full evacuation behavior. All NPCs except Authority move toward slice boundaries. Panic animations active. Running at 2.0 m/s. Crowd density drops to 10% of normal. Stampede risk at choke points. |

#### Authority Response

| Level | Behavior Changes |
|-------|-----------------|
| **Normal** | Routine patrol. 2-3 units on standard routes. Response to minor incidents. |
| **Elevated** | Patrol routes tighten toward Heat epicenter. Extra patrol dispatched (1 unit from outside slice, arrives in 5 min). Investigation posture. Radio chatter audible. |
| **High** | Cordon established around incident (50m radius). Crowd management active (push civilians back). 2 additional units dispatched. Traffic signals overridden for emergency vehicle access. |
| **Critical** | Full response: all units converge. Road closures at slice boundaries. ESU (Emergency Services Unit) dispatched (arrives 3 min). Helicopter audio cue. Crowd evacuation orders issued. |
| **Crisis** | Military consideration flagged (narrative event). Full lockdown. All civilian NPCs forcefully evacuated. Barriers at all entry points. Authority NPCs in containment mode only. Player movement restricted but not blocked. |

#### IoT Device Response

| Level | Behavior Changes |
|-------|-----------------|
| **Normal** | All devices operating normally. Standard detection rates. |
| **Elevated** | CCTV scan rate increases (2Hz to 4Hz). Kiosks display "advisory" banners. Signal timing unaffected. |
| **High** | CCTV in alert mode (10Hz scan). 5% device failure rate per detection pass (system stress). Kiosks display emergency alerts. Signal timing may be overridden for emergency vehicles. |
| **Critical** | 15% device failure rate. Some cameras go dark (overloaded or damaged). Kiosks show evacuation routes. All signals forced to flashing red (traffic halt). |
| **Crisis** | 30% device failure rate. Widespread camera outages. Kiosks go dark or show static. Signal systems may fail entirely. IoT network degraded. |

#### Portal/Anomaly Response

| Level | Behavior Changes |
|-------|-----------------|
| **Normal** | Anomalies and portals behave per their own specs. No Heat influence. |
| **Elevated** | Minor instability: active portals flicker occasionally (visual only). Anomaly growth rate unchanged. |
| **High** | Decay rate multiplied by 1.5x (portals close faster). Anomaly growth rate reduced by 20%. Reality is "fighting back." |
| **Critical** | Decay rate multiplied by 3x. Portal bandwidth reduced by 50%. Anomaly bleed radius multiplied by 2x (wider area of distortion, but anomaly is weaker). |
| **Crisis** | Spontaneous micro-portals may appear (visual-only, 2m radius, last 10-30s). These are narrative flavor: they show reality fracturing but cannot be entered. Existing portals become extremely unstable (stability loss rate 3x). |

### 2.7 Heat Visualization

```
HEAT DISPLAY (player HUD):

  Optional display (toggle with key):
    - 4 vertical bars, one per channel, color-coded:
        Physical:      Red
        Social:        Yellow
        Institutional: Blue
        Ecological:    Green/Purple

    - Bar height = channel value (0.0 to 1.0)
    - Background color changes at thresholds:
        Normal:   dark gray
        Elevated: amber tint
        High:     orange tint
        Critical: red tint
        Crisis:   pulsing red

  World visualization (always-on, subtle):
    - Sky color shifts toward overcast/dark as composite Heat rises
    - Ambient audio tension layer fades in (strings, low drone)
    - Billboard content may show "breaking news" overlays at High+
    - Police siren frequency increases with Heat level
```

### 2.8 Heat Calculation Example: The Demo Run

Tracking Heat through the 5-minute proof scenario:

```
T+0:00  All channels: 0.0
        Level: Normal

T+1:00  Anomaly shimmer appears
        Physical: 0.0, Social: 0.10, Institutional: 0.05, Ecological: 0.20
        Level: Elevated (Ecological > 0.2)

T+1:30  Anomaly growing, crowd reacting
        Social: 0.10 + 0.05 (growth) = 0.15
        Institutional: 0.05 + 0.03 (growth) = 0.08
        Ecological: 0.20 + 0.10 (growth) = 0.30
        Decay applied (~0.5 min): Physical 0.0, Social ~0.145,
        Institutional ~0.078, Ecological ~0.299
        Level: Elevated (Ecological > 0.2)

T+2:15  Portal opens
        Physical: 0.0 + 0.10 = 0.10
        Social: 0.145 + 0.20 - decay(0.75min*0.01) = 0.338
        Institutional: 0.078 + 0.10 - decay(0.75min*0.005) = 0.174
        Ecological: 0.299 + 0.30 - decay(0.75min*0.003) = 0.597
        Level: High (Ecological > 0.4)

T+2:30  Player enters portal
        Physical: 0.10 + 0.05 = 0.15
        Social: 0.338 + 0.10 - decay = ~0.435
        Institutional: 0.174 + 0.05 - decay = ~0.222
        Ecological: 0.597 + 0.10 - decay = ~0.695
        Level: High (Ecological approaching Critical)

T+3:45  Player exits with artifact, portal collapses
        Physical: 0.15 + 0.05(exfil) - 0.05(collapse) - decay = ~0.12
        Social: 0.435 + 0.10(exfil) + 0.05(collapse) + 0.05(artifact)
                - decay(~1.25min*0.01) = ~0.62
        Institutional: 0.222 + 0.05(exfil) + 0.02(artifact)
                       - decay(~1.25min*0.005) = ~0.286
        Ecological: 0.695 + 0.10(exfil) - 0.10(collapse) + 0.15(artifact)
                    - decay(~1.25min*0.003) = ~0.841
        Level: Critical (Ecological > 0.7)

T+5:00  Aftermath, decay only (~1.25 min of pure decay)
        Physical: 0.12 - (1.25*0.02) = ~0.095
        Social: 0.62 - (1.25*0.01) = ~0.608
        Institutional: 0.286 - (1.25*0.005) = ~0.280
        Ecological: 0.841 - (1.25*0.003) = ~0.837
        Level: Critical (Ecological still > 0.7)

  NOTE: During Critical, authority is in full response mode.
  Portal decay was 3x due to Critical-level Ecological Heat.
  Crowd is evacuating. This is the state the demo ends in.
```

---

## 3. First Anomaly Specification

### 3.1 Anomaly Profile

| Property | Value |
|----------|-------|
| **Anomaly ID** | ANOMALY_TSQ_001 |
| **Type** | Gravity wobble + visual distortion (light refraction shimmer) |
| **Location** | 44th Street between Broadway and 7th Ave, near alley entrance |
| **World coordinates** | (-25, 0, 45) — approximately 25m west of 7th Ave, 45m north of bowtie center |
| **Trigger** | Scripted at T+1:00 in demo (can also be event-triggered) |
| **Initial radius** | 3.0 meters |
| **Maximum radius** | 10.0 meters |
| **Growth duration** | 5 minutes to near-maximum |

### 3.2 Growth Curve

The anomaly grows following an exponential approach curve:

```
GROWTH EQUATION:

  r(t) = 3 + 7 * (1 - e^(-t/180))

  Where:
    r(t) = radius in meters at time t
    t    = time in seconds since anomaly appearance
    3    = initial radius (meters)
    7    = additional growth (meters)
    180  = time constant (seconds, ~3 minutes to reach ~63%)

  Key points:
    t = 0s:    r = 3.0m  (initial)
    t = 60s:   r = 5.2m  (1 minute)
    t = 120s:  r = 6.6m  (2 minutes)
    t = 180s:  r = 7.4m  (3 minutes — 63% of growth)
    t = 300s:  r = 9.2m  (5 minutes — near maximum)
    t = 480s:  r = 9.9m  (8 minutes — effectively at maximum)

  Visual representation:
    Radius
    10m |                                          ___________
        |                                    _____/
     8m |                              _____/
        |                         ____/
     6m |                    ____/
        |               ____/
     4m |          ____/
        |    _____/
     3m |___/
        |___|____|____|____|____|____|____|____|____|
        0   60   120  180  240  300  360  420  480  seconds
```

### 3.3 Anomaly Effects

#### Visual Effects

| Effect | Range | Description |
|--------|-------|-------------|
| **Shimmer** | 0 to radius | Light refraction distortion, like heat haze. Intensity strongest at center, fades at edge. |
| **Color shift** | 0 to radius * 0.5 | Slight desaturation within inner half of anomaly zone |
| **Edge distortion** | radius * 0.8 to radius | Visible boundary where distortion begins. Faint luminous edge. |
| **Particle effects** | 0 to radius | Small floating particles of light, drifting slowly (dust-like) |
| **Ground marking** | 0 to radius * 0.3 | Faint geometric pattern on ground (alien geometry, glowing lines) |

#### Audio Effects

| Effect | Range | Description |
|--------|-------|-------------|
| **Low-frequency hum** | 0 to 20m | Deep bass hum (30-60 Hz), volume increases closer to center |
| **Spatial distortion** | 0 to radius | Ambient city sounds become muffled and slightly pitch-shifted within zone |
| **Harmonic whisper** | 0 to 5m | At very close range, faint harmonic tones (otherworldly) |

#### Physics Effects

| Effect | Range | Description |
|--------|-------|-------------|
| **Gravity reduction** | 0 to radius | Gravity = 0.8g within anomaly zone. Objects feel lighter. Jump height increased by 25%. |
| **Positional jitter** | 0 to radius * 0.5 | Entities inside experience random positional offset: 0.05m per second, applied as micro-teleport. Visible as slight shaking. |
| **Object drift** | 0 to radius * 0.3 | Loose objects (trash, paper, small props) slowly drift upward or sideways |

### 3.4 Detection and Evidence

| Detector | Range | What It Detects | Event Generated |
|----------|-------|----------------|-----------------|
| **CCTV cameras** | Camera FOV intersects anomaly zone | Visual distortion causes edge detection failures, motion artifacts, false positives | `security.camera.observation` (type: anomalous_visual) |
| **CCTV cameras** | Camera FOV includes anomaly boundary | Luminous edge visible as unexplained light source | `security.camera.observation` (type: unexplained_light) |
| **Hero NPC witnesses** | Within 15m and line-of-sight | Visual shimmer observed, unusual feeling reported | `npc.hero.observation` (type: anomaly_witness) |
| **Background NPC reaction** | Within 15m | Rubbernecking (15-20m ring), avoidance (within 10m) | No direct event; behavioral change drives Social Heat |
| **Player** | Within 20m (visual), within radius (physics) | Full sensory experience: visual, audio, physics | Player-driven evidence recording |
| **IoT sensors (kiosks)** | Within 10m | EM interference detected | `iot.device.failure` (type: em_interference) |

### 3.5 System Coupling

```
ANOMALY SYSTEM COUPLING:

  anomaly.zone.spike →
    ├── CCTV: CAM_TSQ_007 detects (confidence -30% inside zone)
    │   └── security.camera.observation → evidence.recorded
    │       └── ledger.write()
    ├── Heat: Social +0.10, Institutional +0.05, Ecological +0.20
    │   └── heat.channel.changed (if threshold crossed)
    │       └── Authority response upgrade
    │       └── Crowd behavior change
    ├── Crowd:
    │   ├── Rubbernecking ring (15-20m): Tourist + some Commuter slow/stop
    │   ├── Avoidance zone (0-10m): all presets divert
    │   └── Social Heat from visible crowd disruption
    ├── Authority:
    │   ├── At radius > 5m: dispatch triggered (authority.dispatch.unit)
    │   ├── Patrol reroutes toward anomaly
    │   └── At High Heat: cordon behavior
    └── Portal system:
        └── At radius ≥ 8m: portal formation possible (see Section 4)

  anomaly.zone.update (periodic, every 30s during active anomaly) →
    ├── Heat: Ecological += growth-based increment
    ├── CCTV: continuous observation generation
    └── NPC: behavior updates based on growing radius
```

### 3.6 Anomaly Lifecycle

| Phase | Condition | Duration | Description |
|-------|-----------|----------|-------------|
| **Dormant** | Before trigger | Indefinite | No anomaly present. Location is normal alley. |
| **Spawning** | Trigger event fires | 5 seconds | Brief energy flash, then shimmer appears at 3m radius |
| **Growing** | r(t) < 8m | ~2 minutes | Anomaly expanding per growth curve. Effects intensifying. |
| **Mature** | r(t) >= 8m | Until contained or timeout | Full effects active. Portal formation possible. |
| **Contained** | Authority containment action OR Heat-driven suppression | 3 minutes | Anomaly shrinks at -1m/30s. Effects weakening. |
| **Natural decay** | No containment, timeout (10-15 min) | 3-5 minutes | Anomaly slowly fades. Radius shrinks. |
| **Residue** | After anomaly fully decays | 24h sim-time | Faint shimmer, ground marking, detectable by sensitive instruments. No physics effects. |
| **Clear** | Residue fully decayed | Permanent | Location returns to normal. Ledger records persist. |

### 3.7 Anomaly Containment

If authority or player takes containment action (cordon + specific authority behavior at anomaly edge), the anomaly enters Contained phase:

```
CONTAINMENT:

  Trigger: Authority unit within 10m of anomaly center for >60s
           AND authority Heat response level >= Active (Heat 0.4+)
           AND cordon placed

  Effect:
    - Growth stops immediately
    - Decay begins: radius shrinks at -1m per 30 seconds
    - Anomaly fully decays in ~3 minutes from containment start
    - Residue remains after full decay
    - If portal already formed: portal stability not affected
      (containment addresses the anomaly, not the portal)
```

---

## 4. First Portal Pocket Specification

### 4.1 Portal Formation

| Property | Value |
|----------|-------|
| **Portal ID** | PORTAL_TSQ_001 |
| **Formation trigger** | Anomaly radius >= 8m AND (player within 5m of anomaly center OR 3 minutes at mature phase) |
| **Location** | 44th St alley entrance (seam S10 location) |
| **World coordinates** | (-28, 0, 43) — within the anomaly zone |

### 4.2 Portal State Machine

```
PORTAL STATES:

  LATENT:
    - No portal visible
    - Anomaly may or may not be active
    - Transition to FORMING: anomaly radius >= 8m AND trigger condition met

  FORMING:
    - Duration: 15 seconds
    - Visual: swirling energy vortex coalescing at alley entrance
    - Audio: rising harmonic tone, spatial audio pulling toward portal
    - Physics: local gravity further reduced to 0.6g within 3m
    - NPC reaction: all NPCs within 30m react (freeze, then flee at 2m/s)
    - Evidence burst: 3+ observations generated
    - Heat: Physical +0.10, Social +0.20, Institutional +0.10, Ecological +0.30
    - Transition to STABLE: formation complete (15s elapsed)
    - Transition to COLLAPSING: extreme Heat causes abort (Crisis + all channels > 0.8)

  STABLE:
    - Portal is traversable
    - Visual: vertical distortion field (~2m wide x 3m tall), shimmering edges,
      glimpse of pocket space visible through portal
    - Audio: steady harmonic drone, wind-like suction sound
    - Stability: 0.4 initial (unstable baseline)
    - Bandwidth: 50 kg/s (player can enter at walking speed)
    - Bleed radius: 5m (anomaly effects extend from portal even if anomaly contained)
    - Signature: unique ID, detectable by CCTV within 10m
    - Duration: stable as long as stability > 0.0
    - Stability drain: -0.01/30s passive (very slow natural decay)
    - Player can enter by walking into portal surface
    - Transition to COLLAPSING: stability <= 0.0 OR player exits after entry

  COLLAPSING:
    - Duration: 10 seconds
    - Visual: portal implodes, energy discharge, sparks and debris
    - Audio: deep THOOM sound, reality snap, glass-breaking overtone
    - Physics: brief gravity spike (1.5g for 2s within 5m)
    - Evidence: portal.state.changed event (COLLAPSING)
    - NPC reaction: startle, duck, then resume fleeing
    - Stability forced to 0.0
    - Transition to SEALED: collapse complete

  SEALED:
    - Portal no longer traversable
    - Visual: residue shimmer at former portal location (same as anomaly residue)
    - Residue decays over 24h sim-time
    - Location marked in ledger
    - Police tape placed by authority (if authority present)
    - Transition to LATENT: residue fully decayed AND new anomaly trigger conditions met

STATE DIAGRAM:

  LATENT ──(anomaly r >= 8m + trigger)──→ FORMING
    ↑                                         │
    │                                    (15s elapsed)
    │                                         │
    │                                         ↓
    │                                      STABLE
    │                                    /         \
    │                          (stability=0)    (player exits)
    │                                  │              │
    │                                  ↓              ↓
    │                              COLLAPSING ←───────┘
    │                                    │
    │                              (10s elapsed)
    │                                    │
    │                                    ↓
    └─────────(24h decay)──────────── SEALED
```

### 4.3 Portal Properties

| Property | Value | Notes |
|----------|-------|-------|
| **Initial stability** | 0.4 | Unstable; sufficient for single traversal |
| **Passive drain** | -0.01 per 30s | Slow natural decay while open |
| **Bandwidth** | 50 kg/s | Player (~80kg) passes through in ~1.6s |
| **Signature** | Unique hash | Detected by CCTV within 10m, by ecological sensors |
| **Bleed radius** | 5m | Anomaly-like effects around portal, even if anomaly itself is contained |
| **Visual size** | 2m wide x 3m tall | Fits human-sized entities |
| **Traversal cost** | Stability -0.05 per traversal | Each entry/exit reduces stability |

### 4.4 Pocket Dimension Specification

The portal leads to a self-contained pocket dimension. This is the first pocket the player encounters.

#### Pocket Geometry

| Property | Value |
|----------|-------|
| **Pocket ID** | POCKET_TSQ_001 |
| **Dimensions** | 10m x 10m x 5m (length x width x height) |
| **Layout** | Single rectangular corridor |
| **Style** | Noir-lit concrete corridor with alien geometric details |
| **Lighting** | High contrast: pools of warm light alternating with deep shadow. Light sources are geometric shapes embedded in walls. |
| **Materials** | Concrete (dark gray, slightly wet-looking), metal (brushed steel accents), alien geometry (luminescent white lines forming impossible angles on walls and floor) |
| **Atmosphere** | Slight fog/haze at floor level. Particles of light floating slowly. |

#### Pocket Layout

```
POCKET LAYOUT (top-down):

  ENTRANCE                                          PEDESTAL
  (portal)                                          (artifact)
    ║                                                  ◆
    ║     ┌─────────────────────────────────────────┐
    ║     │                                         │
    ╠═════╡  Corridor (10m long, 5m wide)           │
    ║     │                                         │
    ║     │  ▓▓▓           ▓▓▓           ▓▓▓       │
    ║     │  (shadow)      (shadow)      (shadow)   │
    ║     │                                         │
    ╠═════╡  Light pools alternate with shadows      │
    ║     │                                         │
    ║     │  ░░░           ░░░           ░░░       │
    ║     │  (light)       (light)       (light)    │
    ║     │                                         │
    ║     └─────────────────────────────────────────┘
    ║
  ENTRANCE
  (portal)

  Legend:
    ║ ═ Portal entrance (2m wide)
    ◆   = Artifact on pedestal
    ▓▓▓ = Deep shadow zones
    ░░░ = Light pool zones
```

#### Pocket Physics

| Property | Value | Comparison to Hub |
|----------|-------|------------------|
| **Gravity** | 0.8g (7.85 m/s^2) | Hub is 1.0g (9.81 m/s^2). Player feels lighter. |
| **Jump height** | ~1.5m (vs ~1.0m in Hub) | 50% increase due to reduced gravity |
| **Fall speed** | 80% of Hub | Slower descent |
| **Air resistance** | None | Objects drift slightly after throwing |
| **Sound propagation** | Slower, more reverb | Audio feels "underwater" slightly |

#### Pocket Aesthetics

| Aspect | Hub (Times Square) | Pocket |
|--------|-------------------|--------|
| **Color palette** | Full saturation, warm tones | Desaturated, cool blue-gray with warm accent lights |
| **Contrast** | Normal | High contrast (deep shadows, bright highlights) |
| **Post-processing** | Standard | Film grain (subtle), vignette, chromatic aberration at edges |
| **Animation style** | Realistic | Slightly slowed (0.9x speed), dreamlike quality |
| **Sound design** | Urban cacophony | Sparse, echoing, metallic. Low drone. Occasional distant metallic echoes. |

#### Pocket NPCs

None. The pocket is empty of all NPCs. This is the first pocket; isolation is intentional. The player is alone with the artifact.

### 4.5 Artifact Specification

| Property | Value |
|----------|-------|
| **Artifact ID** | ART_TSQ_001 |
| **Name** | "The Shard" (working name) |
| **Physical description** | Small metallic object, approximately 8cm x 5cm x 3cm. Irregular polyhedron shape. Surface shifts between brushed steel and mirror-like reflection. |
| **Mass** | 2.0 kg (surprisingly heavy for size) |
| **Compatibility** | 0.4 in Universe 1218 (Hub universe) — moderately incompatible |
| **Location in pocket** | On pedestal at far end of corridor |
| **Pickup interaction** | Walk to pedestal, prompt appears ("Take artifact"), confirm to pick up |

#### Artifact Behavior (In Pocket)

- Visible from entrance: faint glow, slowly rotating on pedestal
- As player approaches: glow intensifies, hum audible
- On pickup: flash of light, artifact enters inventory, destabilization begins

#### Artifact Behavior (In Hub / Times Square)

| Property | Value |
|----------|-------|
| **Visual** | Glowing in inventory; faint glow visible through player's clothing/bag (subtle) |
| **Signature** | Emits low-level interdimensional signature detectable by CCTV within 5m |
| **Heat impact** | Physical +0.02, Social +0.05, Institutional +0.02, Ecological +0.15 on import |
| **Ongoing signature** | Ecological +0.01/minute while carried (constant low-level reality stress) |
| **Decay** | Signature fades over 2 hours sim-time (artifact acclimates to Hub universe) |
| **Detection** | CCTV cameras generate `security.camera.observation` (type: artifact_signature) if artifact is within 5m of camera |

### 4.6 Pocket Destabilization Sequence

Once the artifact is picked up, the pocket begins to collapse. This is the "get out" moment.

```
DESTABILIZATION TIMELINE:

  T+0s:   Artifact picked up.
           Stability starts at portal.stability (whatever it is when player entered).
           Stability drain increases to -0.1 per 30s (10x faster than passive).

  T+30s:  Visual cracks appear in walls (hairline fractures, glowing).
           Audio: cracking sounds, groaning.
           Fog increases.

  T+60s:  Floor begins crumbling at edges (debris falls into void).
           Walls show large fractures (geometry deforming).
           Stability has dropped by ~0.2.
           Audio: alarm-like harmonic, increasing urgency.

  T+90s:  If player still inside: ceiling pieces begin falling (damaging).
           Floor is half-collapsed (navigable path narrowing).
           Stability very low.
           Audio: chaos, collapsing.

  AT STABILITY < 0.1:
           URGENT WARNING: red overlay, pulsing, "GET OUT" spatial audio.
           Player has 30 seconds before pocket fully collapses.
           If player does not exit in 30 seconds: force-teleport to portal
           entrance with damage penalty.

  AT STABILITY = 0.0 (pocket collapsed, player still inside):
           Force-teleport player to Hub (portal location).
           Player takes significant damage (50% health).
           Disorientation effect (blur, tinnitus audio) for 10 seconds.
           Artifact still in inventory.
           Portal auto-seals.

TYPICAL SCENARIO (player grabs artifact and runs):
  - Artifact pickup: T+0
  - Start running toward exit: T+5s
  - Reach portal entrance (10m at run speed ~3m/s): T+8s
  - Exit portal: T+10s
  - Total time in collapsing pocket: ~10 seconds
  - Stability lost: ~0.03 (well within margin)
  - Player experiences: initial cracks forming, urgency cue, but exits safely
```

### 4.7 Aftermath Specification

After the player exits the portal with the artifact, the following world state changes occur:

```
AFTERMATH EVENTS (in order):

  1. Portal collapses (STABLE → COLLAPSING → SEALED over 10s)
     - Energy discharge VFX
     - Gravity spike (1.5g, 2s, 5m radius)
     - Audio: reality snap

  2. Evidence burst (5+ observations generated):
     - CAM_TSQ_007: portal open/close observed
     - CAM_TSQ_008: portal energy discharge detected
     - HERO_03 (Lens): filmed entire sequence (if present)
     - HERO_02 (Dr. Lin): recorded observations (if present)
     - Multiple background NPC witness observations

  3. Heat impact:
     - Portal operation (exfil): Physical +0.05, Social +0.10,
       Institutional +0.05, Ecological +0.10
     - Artifact import: Physical +0.02, Social +0.05,
       Institutional +0.02, Ecological +0.15
     - Portal collapse: Physical -0.05, Social +0.05,
       Institutional 0.00, Ecological -0.10

  4. Residue:
     - Anomaly residue patch at portal location
     - Visible shimmer (reduced intensity)
     - Ground marking persists
     - Radius: 3m
     - Decay: over 24h sim-time (linear fade)
     - Detectable by CCTV and sensitive NPCs

  5. Artifact in player inventory:
     - Glowing, emitting signature
     - CCTV detection within 5m
     - Ongoing Ecological Heat +0.01/min
     - Signature decays over 2h sim-time

  6. Faction responses (deferred, within 2h sim-time):
     - Strange's network contacts player (Dr. Lin or via dead drop)
     - NYPD increases patrol near 44th St (Institutional Heat effect)
     - Criminal faction (Jimmy Two-Phones) becomes aware of portal activity
     - Ghost (HERO_10) begins surveillance of player

  7. World state:
     - Police tape around residue zone (if authority reached area)
     - Crowd displaced, slowly returning to normal
     - Billboard content may show "breaking news" (if High Heat at time)
     - CCTV in area on high alert (10Hz scan rate persists until
       Institutional Heat drops below 0.2)
```

---

## 5. Integration Testing

### 5.1 Heat Integration Test

```
TEST: Heat feedback loop operates correctly

  Setup: Clean state, all Heat 0.0

  Steps:
    1. Trigger anomaly
    2. Verify Heat rises on Social, Institutional, Ecological
    3. Verify crowd behavior changes (Elevated level)
    4. Verify authority dispatched (Elevated level)
    5. Trigger portal
    6. Verify Heat spikes to High level
    7. Verify authority cordon behavior
    8. Verify crowd evacuation begins
    9. Player exits portal with artifact
    10. Verify Heat at Critical on Ecological channel
    11. Verify Critical-level responses active

  Pass: All Heat values within +/- 0.05 of calculated values.
  Pass: All response behaviors triggered at correct thresholds.
```

### 5.2 Anomaly-Portal Coupling Test

```
TEST: Anomaly growth correctly triggers portal formation

  Setup: Clean state, anomaly scripted

  Steps:
    1. Anomaly spawns at 3m radius
    2. Monitor growth: verify r(t) follows curve +/- 0.5m
    3. At radius 7.5m: verify portal still LATENT
    4. At radius 8.0m: verify portal transition to FORMING begins
       (if player within 5m)
    5. After 15s FORMING: verify portal at STABLE
    6. Enter portal, grab artifact
    7. Verify destabilization sequence matches timeline
    8. Exit portal
    9. Verify portal collapse and seal
    10. Verify residue at correct location

  Pass: All state transitions in correct order and within tolerance.
```

### 5.3 Evidence Chain Test

```
TEST: Complete evidence chain from anomaly to ledger

  Setup: Clean ledger, clean state

  Steps:
    1. Trigger anomaly
    2. Verify: anomaly.zone.spike event on bus
    3. Verify: CAM_TSQ_007 generates observation → evidence.recorded
    4. Verify: ledger entry committed (auto_anomaly rule)
    5. Wait for crowd reaction → verify: Social Heat rise → heat.channel.changed
    6. Wait for authority dispatch → verify: authority.dispatch.unit event
    7. Verify: authority action commits related evidence
    8. Open portal → verify: portal.state.changed event
    9. Verify: 5+ observations in ledger from portal formation
    10. Exit with artifact → verify: artifact import evidence committed

  Pass: Every expected event exists in ledger, all committed,
        no orphaned references, evidence chain query returns
        connected graph of events.
```

---

*End of document. Next: Demo Script + Regression Pack v0.*
