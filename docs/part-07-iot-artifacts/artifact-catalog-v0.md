# Artifact Catalog v0

**Twin Earth NYC -- Part 7: IoT Artifacts**
**Version:** 0.1.0
**Status:** Draft
**Last Updated:** 2026-01-27

---

## 1. Artifact Doctrine

> **Artifact = discrete entity with state + sensors/actuators + interfaces + constraints.**

Every IoT artifact in Twin Earth NYC is a first-class simulation entity. Artifacts participate in the game world as physical objects with defined behavior, limited knowledge, and real failure modes. They are the sensory nervous system of the city and the mechanical hands through which systems act on the environment.

**Artifacts ARE:**

- Stateful objects with a finite, enumerable set of states and well-defined transitions.
- Sensor platforms that observe limited slices of the world within defined range, fidelity, and modality.
- Actuators that change the physical or informational state of the world subject to latency and failure.
- Event participants that emit and consume messages on the Event Bus (see `event-bus-spec-v0.md`).
- Constrained by uptime, power, bandwidth, weather, maintenance, and security posture.

**Artifacts are NOT:**

- **Omniscient.** A camera sees its FOV cone and nothing else. A door sensor knows open/closed, not who opened it.
- **Always connected.** Network partitions, power failures, and jamming are first-class conditions.
- **Always truthful.** Sensor confidence is probabilistic. Spoofing, tampering, and degradation produce false or misleading data.
- **Infinitely durable.** Artifacts degrade over time, fail under stress, and require maintenance to remain operational.
- **Intelligent.** Artifacts do not reason. They execute state machines. Intelligence emerges from the systems that consume their data.

---

## 2. V1 Artifact Classes

### 2.1 TRAFFIC LIGHT

| Property | Value |
|---|---|
| **Entity Prefix** | `ENT_TLIGHT_` |
| **Class ID** | `artifact.traffic_light` |

**States:**

| State | Description | LED Pattern |
|---|---|---|
| `red` | Stop signal active | Solid red |
| `yellow` | Caution/transition signal | Solid yellow |
| `green` | Go signal active | Solid green |
| `flashing` | Malfunction or special mode | Flashing red or yellow |
| `off` | No power / deactivated | Dark |

**State Transitions:**

```
green --(timer)--> yellow --(timer)--> red --(timer)--> green
any --(power_fail)--> off
any --(malfunction)--> flashing
off --(power_restore)--> flashing --(reset)--> red --(timer)--> green
flashing --(manual_reset)--> red
```

**Cycle Configuration:**

| Parameter | Default | Range | Notes |
|---|---|---|---|
| `cycle_duration` | 60s | 30s -- 120s | Total cycle length |
| `green_ratio` | 0.50 | 0.30 -- 0.65 | Fraction of cycle in green |
| `yellow_duration` | 4s | 3s -- 6s | Fixed yellow interval |
| `red_clearance` | 2s | 1s -- 4s | All-red overlap for safety |
| `phase_offset` | 0s | 0s -- 120s | Offset for green-wave coordination |

**Sensors:** None. Traffic lights are purely timer-driven in v1. Future versions may add inductive loop detectors or adaptive timing.

**Actuators:**

| Actuator | Action | Latency |
|---|---|---|
| Light state change | Switches active lamp | < 100ms |

**Interfaces:**

| Interface | Direction | Topic | Details |
|---|---|---|---|
| Signal change event | Emit | `traffic.signal.changed` | Emitted on every state transition |
| Visual query | Respond | N/A (line of sight) | NPCs and players observe signal state visually; no network query needed |

**Constraints:**

| Constraint | Value | Notes |
|---|---|---|
| Uptime | 99.5% | Hardwired power; very reliable |
| Latency | < 100ms | State change actuation |
| Power dependency | Grid power, no battery | Goes dark on power failure |
| Maintenance cycle | 2000 sim-hours | Degradation begins after cycle |

**Failure Modes:**

| Mode | Trigger | Behavior | Evidence |
|---|---|---|---|
| Stuck on one color | Malfunction (random/age) | Remains on last state indefinitely | Traffic congestion anomaly |
| Flashing mode | Malfunction or manual override | Flashes red or yellow | Visual observation |
| Dark (power failure) | Grid power loss | All lamps off | Visual observation, power system event |

---

### 2.2 CROSSWALK SIGNAL

| Property | Value |
|---|---|
| **Entity Prefix** | `ENT_XWALK_` |
| **Class ID** | `artifact.crosswalk_signal` |

**States:**

| State | Description | Display |
|---|---|---|
| `walk` | Pedestrians may cross | White walk icon |
| `dont_walk` | Pedestrians must not cross | Solid orange hand |
| `countdown` | Transition warning with timer | Flashing orange hand + seconds |
| `off` | No power / deactivated | Dark |

**State Transitions:**

```
dont_walk --(parent_green + pedestrian_phase)--> walk
walk --(timer)--> countdown
countdown --(timer_zero)--> dont_walk
any --(power_fail)--> off
off --(power_restore)--> dont_walk
```

**Parent Linkage:** Every crosswalk signal has a `parent_signal_id` referencing its controlling traffic light. The crosswalk phase is derived from the parent signal cycle. When the parent enters a state that permits pedestrian crossing (typically the perpendicular green phase), the crosswalk transitions to `walk`.

**Sensors:**

| Sensor | Type | Range | Notes |
|---|---|---|---|
| Pedestrian presence detector | Passive IR / pressure pad | 3m radius | Detects waiting pedestrians to request walk phase |

**Actuators:**

| Actuator | Action | Latency |
|---|---|---|
| Display state change | Updates walk/don't walk display | < 100ms |
| Audible signal | Accessibility beep during walk phase | Immediate |

**Interfaces:**

| Interface | Direction | Topic | Details |
|---|---|---|---|
| State change event | Emit | `traffic.crosswalk.changed` | Emitted on every state transition |
| Visual query | Respond | N/A (line of sight) | NPCs observe visually |

**Constraints:**

| Constraint | Value | Notes |
|---|---|---|
| Uptime | 99.0% | Slightly lower than traffic lights due to additional sensors |
| Sync tolerance | < 500ms | Must stay in sync with parent signal |
| Power dependency | Grid power via parent signal | Shares power with traffic light |
| Sensor range | 3m | Pedestrian detection radius |

**Failure Modes:**

| Mode | Trigger | Behavior | Evidence |
|---|---|---|---|
| Out of sync | Communication fault with parent | Walk signal during wrong phase | Pedestrian-vehicle conflicts |
| Stuck | Actuator malfunction | Remains on last displayed state | Pedestrian confusion, reports |
| Dark | Power failure (parent) | Display off | Visual observation |
| Sensor dead | Sensor failure | Never requests walk phase | Pedestrians wait indefinitely |

---

### 2.3 CCTV CAMERA

| Property | Value |
|---|---|
| **Entity Prefix** | `ENT_CCTV_` |
| **Class ID** | `artifact.cctv_camera` |

**States:**

| State | Description | Recording |
|---|---|---|
| `active` | Operational, observing | Continuous |
| `recording` | Active with flagged event capture | Continuous + high-priority buffer |
| `offline` | Not operational | None |
| `tampered` | Physical interference detected | Last-known frame + tamper alert |

**State Transitions:**

```
active --(motion_threshold)--> recording
recording --(motion_clear + timeout)--> active
active --(power_fail | network_fail)--> offline
active --(physical_interference)--> tampered
tampered --(maintenance)--> active
offline --(restore)--> active
```

**Sensors:**

| Sensor | Type | Specification | Notes |
|---|---|---|---|
| RGB Camera | Visual | FOV 90 degrees, range 30m | Primary observation sensor |
| Motion detection | Computed from video | Sensitivity configurable | Triggers recording state |
| Night vision (IR) | Infrared | Same FOV, reduced quality | Auto-activates in low light; quality penalty applies |

**Actuators:**

| Actuator | Type | Notes |
|---|---|---|
| Pan/Tilt | Motorized mount | Optional; most Times Square cameras are fixed |

**Interfaces:**

| Interface | Direction | Topic | Details |
|---|---|---|---|
| Motion event | Emit | `security.camera.motion` | Continuous stream when motion detected |
| Observation event | Emit | `security.camera.observation` | Entity identification with confidence |
| Tamper alert | Emit | `security.camera.tampered` | Immediate alert on physical interference |
| Feed request | Respond | Command: `request_camera_feed` | Requires authority role + range; bandwidth limited |

**Constraints:**

| Constraint | Value | Notes |
|---|---|---|
| Uptime | 95.0% | Outdoor exposure increases failure rate |
| Detection latency | 500ms | Time from event to emitted observation |
| Bandwidth | 3 concurrent full-res feeds per node | Additional requests queued or degraded |
| Weather dependency | See confidence model | Rain, fog, snow degrade quality |
| Power dependency | Grid + 2h battery backup | Battery kicks in on grid failure |
| Storage retention | 1 sim-hour raw, 24 sim-hours summary | Key events retained permanently |

**Confidence Model:**

The effective confidence of any CCTV observation is computed as:

```
effective_confidence = base_confidence
                     * rain_factor
                     * night_factor
                     * occlusion_factor
                     * distance_factor
```

| Factor | Value / Formula | Notes |
|---|---|---|
| `base_confidence` | 0.80 | Baseline for clear day, unobstructed, mid-range |
| `rain_factor` | 0.70 during rain, 1.0 otherwise | Lens water + reduced visibility |
| `night_factor` | 0.60 without IR, 0.85 with IR, 1.0 daytime | IR helps but does not fully compensate |
| `occlusion_factor` | 0.30 -- 1.0 | 1.0 = no occlusion, 0.3 = heavy crowd/object blocking |
| `distance_factor` | Linear decay: 1.0 at 0m to 0.3 at max range (30m) | `1.0 - (0.7 * distance / max_range)` |

**Example:** Rainy night, target at 20m, partial occlusion (0.6):

```
0.80 * 0.70 * 0.60 * 0.60 * (1.0 - 0.7 * 20/30)
= 0.80 * 0.70 * 0.60 * 0.60 * 0.533
= 0.107
```

This yields a **Low** confidence observation -- suggestive only.

**Failure Modes:**

| Mode | Trigger | Behavior | Evidence |
|---|---|---|---|
| Offline | Power/network failure | No output | Absence of heartbeat events |
| Fog/rain degradation | Weather condition | Reduced confidence (-30%) | Metadata flags weather condition |
| Blinded by glare | Direct light source in FOV | Whiteout in affected region | Partial frame loss |
| Jammed | Electronic countermeasure | Static or frozen frame | Tamper detection may trigger |
| Tampered | Physical interference | Tamper alert emitted | `security.camera.tampered` event |

---

### 2.4 INFORMATION KIOSK

| Property | Value |
|---|---|
| **Entity Prefix** | `ENT_KIOSK_` |
| **Class ID** | `artifact.info_kiosk` |

**States:**

| State | Description | Display |
|---|---|---|
| `active` | Operational, showing default content | Local info, maps, ads |
| `alert_mode` | Displaying emergency/anomaly alert | Alert message, colored border |
| `screensaver` | No recent interaction | Rotating ads / ambient display |
| `offline` | Not operational | Screen dark or frozen |

**State Transitions:**

```
screensaver --(proximity_detected)--> active
active --(idle_timeout: 30s)--> screensaver
active --(anomaly.zone.spike received | authority command)--> alert_mode
alert_mode --(alert_cleared)--> active
any --(power_fail)--> offline
offline --(power_restore)--> screensaver
```

**Sensors:**

| Sensor | Type | Range | Notes |
|---|---|---|---|
| Proximity detector | Passive IR | 2m radius | Wakes from screensaver |
| Touch input | Capacitive screen | Contact | User interaction for queries |

**Actuators:**

| Actuator | Type | Notes |
|---|---|---|
| Display screen | LCD | Outdoor-rated, high brightness |
| Speaker | Low-volume | Accessibility audio, alert chimes |

**Interfaces:**

| Interface | Direction | Topic | Details |
|---|---|---|---|
| Alert broadcast | Emit | `public_info.kiosk.alert` | When kiosk enters alert mode |
| Anomaly subscription | Receive | `anomaly.zone.spike` | Auto-triggers alert mode if intensity > 0.5 within range |
| Local info query | Respond | Direct interaction | Players/NPCs can query for area info, maps, transit |
| Display command | Receive | Command: `request_kiosk_display` | Authority/admin role required |

**Constraints:**

| Constraint | Value | Notes |
|---|---|---|
| Uptime | 90.0% | Outdoor exposure, touch screen wear |
| Power dependency | Grid power, no battery | Immediate offline on power failure |
| Screen visible range | 5m | Readable distance in daylight |
| Interaction range | 2m | Must be close to use touch screen |
| Audio range | 3m | Low-volume speaker |

**Failure Modes:**

| Mode | Trigger | Behavior | Evidence |
|---|---|---|---|
| Frozen display | Software hang | Last frame stuck on screen | Unresponsive to touch |
| False alert | Spoofed anomaly event or bug | Displays incorrect alert | Alert without corresponding anomaly data |
| Offline | Power failure | Screen dark | Visual observation |
| Touch failure | Screen damage / weather | Display works, no input accepted | Proximity wakes display but touch unresponsive |

---

### 2.5 DOOR / LOCK

| Property | Value |
|---|---|
| **Entity Prefix** | `ENT_DOOR_` |
| **Class ID** | `artifact.door_lock` |

**States:**

| State | Description | Physical |
|---|---|---|
| `locked` | Secured, credential required to open | Door closed, bolt engaged |
| `unlocked` | Open-able without credential | Door closed, bolt retracted |
| `open` | Door physically open | Door ajar or fully open |
| `forced` | Lock bypassed by force | Door open, lock mechanism damaged |
| `broken` | Mechanism non-functional | Stuck in last position |

**State Transitions:**

```
locked --(valid_credential)--> unlocked
locked --(force_applied > threshold)--> forced
unlocked --(door_opened)--> open
open --(door_closed)--> unlocked
unlocked --(auto_lock_timer | manual_lock)--> locked
forced --(maintenance)--> locked
any --(mechanism_failure)--> broken
broken --(maintenance)--> locked
```

**Sensors:**

| Sensor | Type | Range | Notes |
|---|---|---|---|
| Contact sensor | Magnetic reed switch | Contact (door frame) | Detects open/closed state |
| Credential reader | Varies by type | Contact to 0.5m | Reads access credentials |

**Actuators:**

| Actuator | Type | Notes |
|---|---|---|
| Electronic lock mechanism | Motorized bolt / solenoid | Engages/disengages lock |

**Interfaces:**

| Interface | Direction | Topic | Details |
|---|---|---|---|
| State change event | Emit | `access.door.state_changed` | Emitted on every transition; includes actor and method |
| Forced entry alert | Emit | `access.door.forced` | Immediate alert on forced state |
| Failed auth event | Emit | `access.door.failed_auth` | Logged on invalid credential attempt |
| Unlock command | Receive | Command: `request_door_unlock` | Requires valid credential |

**Credential Types:**

| Type | Auth Method | Speed | Spoofability | Notes |
|---|---|---|---|---|
| Key | Physical key insertion | 2s | Low (requires physical copy) | Most common for older buildings |
| Badge | RFID proximity | 0.5s | Medium (cloneable with effort) | Standard commercial access |
| Code | Keypad entry | 3-5s | Medium (observable, brute-forceable) | Numeric PIN, lockout after 3 failures |
| Biometric | Fingerprint / facial scan | 2s | Low (difficult to spoof) | High-security locations only |
| Role-based | System role verification | 0.5s | Low (requires system compromise) | Authority/admin override |

**Constraints:**

| Constraint | Value | Notes |
|---|---|---|
| Uptime | 98.0% | Indoor location improves reliability |
| Actuation latency | < 200ms | Time from valid credential to bolt retraction |
| Battery backup | 4 hours | Maintains lock state during power failure |
| Auto-lock timer | 30s default | Door re-locks if not manually held open |
| Force threshold | Varies by door class | Residential < Commercial < Security |

**Failure Modes:**

| Mode | Trigger | Behavior | Evidence |
|---|---|---|---|
| Jammed (won't open) | Mechanical fault | Valid credential accepted but bolt stuck | `access.door.state_changed` with error flag |
| Jammed (won't close) | Mechanical fault | Door remains unlocked/open | Prolonged open state event |
| Broken (stuck open) | Force or severe malfunction | Door cannot be secured | Continuous open state, security alert |
| Credential reader malfunction | Sensor failure | All credential attempts fail | Repeated `access.door.failed_auth` events |
| Battery depleted | Extended power outage > 4h | Fails to default state (locked or unlocked per config) | Power system event |

---

## 3. Universal Constraint Fields

Every artifact instance carries the following constraint fields, which govern its runtime behavior and interact with the simulation's environmental systems.

| Field | Description | Range | Default | Update Frequency |
|---|---|---|---|---|
| `uptime` | Probability of being operational at any given tick | 0.85 -- 0.995 | Per-class defined | Checked each sim-minute |
| `latency` | Response time for state changes and event emission | 50ms -- 2000ms | Per-class defined | Dynamic (Heat-affected) |
| `bandwidth` | Data throughput limit for networked operations | Per-class defined | Per-class defined | Dynamic (load-affected) |
| `range` | Effective sensor or actuator distance | 2m -- 50m | Per-class defined | Static (unless degraded) |
| `power` | Dependency on grid power | Boolean + battery backup duration | Per-class defined | Checked on grid events |
| `maintenance_status` | Current condition of the artifact | `good` / `degraded` / `failed` | `good` | Updated on inspection or failure |
| `security_posture` | Resistance to tampering and spoofing | `low` / `medium` / `high` | Per-class defined | Static (unless upgraded) |

**Maintenance Status Effects:**

| Status | Effect |
|---|---|
| `good` | All parameters at nominal values |
| `degraded` | Latency x1.5, confidence x0.85, failure rate x2.0 |
| `failed` | Artifact non-functional, emits no events, requires repair |

**Security Posture by Class:**

| Class | Default Posture | Tamper Detection | Notes |
|---|---|---|---|
| Traffic Light | Low | None | Hardwired, rarely targeted |
| Crosswalk Signal | Low | None | Linked to traffic light |
| CCTV Camera | Medium | Vibration + video loss | Alerts on physical interference |
| Information Kiosk | Low | Software watchdog | Reboots on hang detection |
| Door/Lock | Medium-High | Contact sensor + failed auth logging | Higher for security doors |

---

## 4. Failure Triggers

Artifacts do not fail only when the narrative demands it. Failures emerge from simulation conditions through the following trigger categories.

### 4.1 Random Failure (Poisson Process)

Each artifact class has a base failure rate modeled as a Poisson process.

| Class | Mean Time Between Failures (MTBF) | Lambda (per sim-hour) |
|---|---|---|
| Traffic Light | 2000 sim-hours | 0.0005 |
| Crosswalk Signal | 1500 sim-hours | 0.00067 |
| CCTV Camera | 500 sim-hours | 0.002 |
| Information Kiosk | 300 sim-hours | 0.0033 |
| Door/Lock | 1000 sim-hours | 0.001 |

**Roll:** Each sim-hour, for each artifact: `if random() < lambda then trigger_failure()`.

### 4.2 Heat-Driven Failure

As the Heat level (institutional pressure / narrative tension) rises, infrastructure comes under greater stress.

```
effective_failure_rate = base_failure_rate * (1 + Heat_level)
```

Where `Heat_level` is normalized to [0.0, 1.0]. At maximum Heat, failure rates double.

### 4.3 Sabotage (Player/NPC Action)

Deliberate interference by actors in the simulation. Sabotage always leaves evidence:

| Sabotage Type | Required Skill/Tool | Time Required | Evidence Left |
|---|---|---|---|
| Camera jam | Tech skill + jammer device | 5s | RF signature, tamper event |
| Camera blind | Physical (spray paint, tape) | 3s | Tamper event, physical evidence |
| Door force | Strength check or tool | 10-30s | Forced state, noise, physical damage |
| Door hack | Tech skill + bypass tool | 15-60s | Failed auth log anomaly |
| Kiosk hack | Tech skill + access | 30s | Software anomaly log |
| Signal override | Authority credential (stolen/forged) | 10s | Auth log with credential trace |

### 4.4 Weather-Driven Failure

Outdoor artifacts experience increased failure rates during adverse weather.

| Weather | Failure Rate Multiplier | Affected Classes |
|---|---|---|
| Clear | x1.0 | -- |
| Rain | x1.3 | CCTV, Kiosk, Crosswalk Signal |
| Heavy Rain | x1.8 | CCTV, Kiosk, Crosswalk Signal, Traffic Light |
| Snow | x1.5 | CCTV, Kiosk, Crosswalk Signal |
| Fog | x1.1 | CCTV (quality only, not mechanical) |

### 4.5 Age / Wear Degradation

Long-running artifacts accumulate wear. After exceeding their maintenance cycle threshold, they transition from `good` to `degraded` status, doubling their effective failure rate.

```
if sim_hours_since_maintenance > maintenance_cycle_threshold:
    maintenance_status = "degraded"
    effective_failure_rate *= 2.0
```

Maintenance actions (by city workers or player-triggered repair) reset the counter and restore `good` status.

---

## 5. Artifact Lifecycle

```
[Spawn] --> [good] --> (operate normally)
                |
                +--(wear/age)--> [degraded] --> (operate with penalties)
                |                    |
                |                    +--(failure trigger)--> [failed] --> (no output)
                |                                               |
                +--(failure trigger)--> [failed]                |
                                           |                    |
                                           +----(maintenance)---+--> [good]
```

**Spawn:** Artifacts are instantiated at simulation start from the placement map (see `times-square-placement-map-v0.md`). Each artifact receives a unique entity ID, initial state, and constraint values.

**Despawn:** Artifacts are not despawned in v1. Destroyed artifacts remain in `failed` state until repaired. Future versions may support permanent destruction for narrative events.

---

*End of Artifact Catalog v0*
