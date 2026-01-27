# Event Bus Specification v0

**Twin Earth NYC -- Part 7: IoT Artifacts**
**Version:** 0.1.0
**Status:** Draft
**Last Updated:** 2026-01-27

---

## 1. Overview

The Event Bus is the central nervous system connecting all IoT artifacts, game systems, and AI agents in Twin Earth NYC. Every artifact state change, sensor observation, and command flows through the bus as a structured message. The bus is asynchronous, topic-based, and designed for lossy operation -- messages may be delayed or dropped under high Heat or network stress, and consumers must tolerate this.

---

## 2. Topic Structure

All topics follow the three-level naming convention:

```
domain.type.action
```

| Segment | Purpose | Examples |
|---|---|---|
| `domain` | Top-level system category | `traffic`, `security`, `access` |
| `type` | Entity class or subsystem | `signal`, `camera`, `door`, `zone` |
| `action` | What happened or what is requested | `changed`, `motion`, `state_changed`, `spike` |

---

## 3. Domains

| Domain | Scope | Artifact Classes | Description |
|---|---|---|---|
| `traffic` | Signals, crosswalks, vehicle flow | Traffic Light, Crosswalk Signal | Road and pedestrian traffic control events |
| `access` | Doors, locks, credentials | Door/Lock | Physical access control and authentication events |
| `security` | Cameras, alarms, patrols | CCTV Camera | Surveillance, motion detection, and security alerts |
| `public_info` | Kiosks, alerts, broadcasts | Information Kiosk | Public-facing information and emergency alerts |
| `anomaly` | Zone spikes, portal activity, reality distortion | Anomaly System (engine) | Supernatural and reality-distortion events |
| `evidence` | Observations recorded, evidence committed | Evidence System (engine) | Chain-of-custody events for the investigation system |

---

## 4. Event Types (v1 Complete List)

### 4.1 Traffic Events

**`traffic.signal.changed`**

| Field | Type | Description |
|---|---|---|
| `signal_id` | string | Unique traffic light entity ID (e.g., `ENT_TLIGHT_TSQ_01`) |
| `old_state` | enum | Previous state: `red`, `yellow`, `green`, `flashing`, `off` |
| `new_state` | enum | New state: `red`, `yellow`, `green`, `flashing`, `off` |
| `intersection_id` | string | Intersection group ID |
| `timestamp` | ISO 8601 | Sim-time of state change |

- **Source:** Traffic Light
- **Rate:** ~1/min per signal (each phase transition)
- **Priority:** Low

```json
{
  "topic": "traffic.signal.changed",
  "payload": {
    "signal_id": "ENT_TLIGHT_TSQ_01",
    "old_state": "green",
    "new_state": "yellow",
    "intersection_id": "INT_42_BROADWAY",
    "timestamp": "2026-01-27T14:30:00Z"
  }
}
```

---

**`traffic.crosswalk.changed`**

| Field | Type | Description |
|---|---|---|
| `crosswalk_id` | string | Unique crosswalk entity ID |
| `old_state` | enum | Previous state: `walk`, `dont_walk`, `countdown`, `off` |
| `new_state` | enum | New state |
| `parent_signal_id` | string | Controlling traffic light entity ID |
| `timestamp` | ISO 8601 | Sim-time of state change |

- **Source:** Crosswalk Signal
- **Rate:** ~1/min per crosswalk
- **Priority:** Low

```json
{
  "topic": "traffic.crosswalk.changed",
  "payload": {
    "crosswalk_id": "ENT_XWALK_TSQ_03",
    "old_state": "walk",
    "new_state": "countdown",
    "parent_signal_id": "ENT_TLIGHT_TSQ_01",
    "timestamp": "2026-01-27T14:30:15Z"
  }
}
```

---

### 4.2 Security Events

**`security.camera.motion`**

| Field | Type | Description |
|---|---|---|
| `camera_id` | string | Unique CCTV entity ID |
| `zone` | string | Coverage zone identifier |
| `motion_level` | float | Normalized motion intensity [0.0, 1.0] |
| `timestamp` | ISO 8601 | Sim-time of detection |

- **Source:** CCTV Camera
- **Rate:** Continuous stream while motion detected (throttled to 1/s max)
- **Priority:** Low (unless motion_level > 0.7, then Medium)

```json
{
  "topic": "security.camera.motion",
  "payload": {
    "camera_id": "ENT_CCTV_TSQ_04",
    "zone": "ZONE_TKTS_STEPS",
    "motion_level": 0.45,
    "timestamp": "2026-01-27T14:30:22Z"
  }
}
```

---

**`security.camera.observation`**

| Field | Type | Description |
|---|---|---|
| `camera_id` | string | Unique CCTV entity ID |
| `target_id` | string | Observed entity ID (or `unknown`) |
| `target_class` | enum | `person`, `vehicle`, `door`, `device`, `anomaly`, `unknown` |
| `confidence` | float | Observation confidence [0.0, 1.0] |
| `position` | object | `{ x, y, z }` estimated world position |
| `timestamp` | ISO 8601 | Sim-time of observation |

- **Source:** CCTV Camera
- **Rate:** Event-driven (on entity detection or re-identification)
- **Priority:** Medium

```json
{
  "topic": "security.camera.observation",
  "payload": {
    "camera_id": "ENT_CCTV_TSQ_04",
    "target_id": "ENT_NPC_a3b7",
    "target_class": "person",
    "confidence": 0.72,
    "position": { "x": 234.5, "y": 0.0, "z": 118.2 },
    "timestamp": "2026-01-27T14:30:23Z"
  }
}
```

---

### 4.3 Access Events

**`access.door.state_changed`**

| Field | Type | Description |
|---|---|---|
| `door_id` | string | Unique door entity ID |
| `old_state` | enum | Previous state: `locked`, `unlocked`, `open`, `forced`, `broken` |
| `new_state` | enum | New state |
| `actor_id` | string | Entity ID of the actor who caused the change (or `system`) |
| `method` | enum | `key`, `badge`, `code`, `biometric`, `role`, `force`, `auto`, `system` |
| `timestamp` | ISO 8601 | Sim-time of state change |

- **Source:** Door/Lock
- **Rate:** Event-driven
- **Priority:** Medium (High if `new_state` is `forced`)

```json
{
  "topic": "access.door.state_changed",
  "payload": {
    "door_id": "ENT_DOOR_TSQ_MARRIOTT_01",
    "old_state": "locked",
    "new_state": "unlocked",
    "actor_id": "ENT_NPC_c4d8",
    "method": "badge",
    "timestamp": "2026-01-27T14:31:00Z"
  }
}
```

---

### 4.4 Public Information Events

**`public_info.kiosk.alert`**

| Field | Type | Description |
|---|---|---|
| `kiosk_id` | string | Unique kiosk entity ID |
| `alert_type` | enum | `anomaly_warning`, `emergency`, `amber_alert`, `weather`, `transit`, `custom` |
| `message` | string | Human-readable alert text |
| `severity` | enum | `info`, `warning`, `critical` |
| `timestamp` | ISO 8601 | Sim-time of alert |

- **Source:** Information Kiosk
- **Rate:** Event-driven
- **Priority:** Medium (High if severity is `critical`)

```json
{
  "topic": "public_info.kiosk.alert",
  "payload": {
    "kiosk_id": "ENT_KIOSK_TSQ_02",
    "alert_type": "anomaly_warning",
    "message": "Unusual atmospheric activity reported near TKTS steps. Please remain calm.",
    "severity": "warning",
    "timestamp": "2026-01-27T14:31:30Z"
  }
}
```

---

### 4.5 Anomaly Events

**`anomaly.zone.spike`**

| Field | Type | Description |
|---|---|---|
| `zone_id` | string | Affected zone identifier |
| `anomaly_type` | enum | `portal_activity`, `reality_distortion`, `temporal_echo`, `energy_surge` |
| `intensity` | float | Normalized intensity [0.0, 1.0] |
| `radius` | float | Affected radius in meters |
| `position` | object | `{ x, y, z }` epicenter world position |
| `timestamp` | ISO 8601 | Sim-time of detection |

- **Source:** Anomaly System (engine-level)
- **Rate:** Event-driven (spikes are infrequent but high-impact)
- **Priority:** High

```json
{
  "topic": "anomaly.zone.spike",
  "payload": {
    "zone_id": "ZONE_TKTS_STEPS",
    "anomaly_type": "portal_activity",
    "intensity": 0.73,
    "radius": 15.0,
    "position": { "x": 230.0, "y": 0.0, "z": 115.0 },
    "timestamp": "2026-01-27T14:32:00Z"
  }
}
```

---

### 4.6 Evidence Events

**`evidence.recorded`**

| Field | Type | Description |
|---|---|---|
| `evidence_id` | string | Unique evidence record ID |
| `observer_id` | string | Entity ID of the recording device or witness |
| `target_id` | string | Entity ID of the observed subject |
| `modality` | enum | `video`, `audio`, `telemetry`, `visual_witness`, `photo` |
| `confidence` | float | Observation confidence [0.0, 1.0] |
| `timestamp` | ISO 8601 | Sim-time of recording |

- **Source:** Evidence System (engine-level, triggered by artifact observations)
- **Rate:** Event-driven
- **Priority:** Medium

```json
{
  "topic": "evidence.recorded",
  "payload": {
    "evidence_id": "OBS_video_a7f3c2e1",
    "observer_id": "ENT_CCTV_TSQ_04",
    "target_id": "ENT_NPC_a3b7",
    "modality": "video",
    "confidence": 0.72,
    "timestamp": "2026-01-27T14:30:23Z"
  }
}
```

---

## 5. Command Types (v1)

Commands are request-response messages sent to artifacts. Unlike events (fire-and-forget), commands expect acknowledgment and may fail.

| Command | Required Auth | Target | Latency | Failure Modes |
|---|---|---|---|---|
| `query_crosswalk_state` | None (visual) | Crosswalk Signal | 0ms (direct observation) | Occlusion (can't see signal) |
| `query_door_lock_state` | Proximity (within 1m) | Door/Lock | 100ms | Device offline |
| `request_door_unlock` | Credential (key/badge/code/biometric) | Door/Lock | 200ms | Invalid credential, jammed, offline |
| `request_kiosk_display` | Role (authority/admin) | Information Kiosk | 500ms | Offline, queue full |
| `request_camera_feed` | Role (authority) + range (within node) | CCTV Camera | 1000ms | Offline, bandwidth exceeded, jammed |

**Command Envelope:**

```json
{
  "command": "request_door_unlock",
  "target_id": "ENT_DOOR_TSQ_MARRIOTT_01",
  "requester_id": "ENT_PLAYER_01",
  "auth": {
    "type": "badge",
    "credential_ref": "CRED_BADGE_0042"
  },
  "timestamp": "2026-01-27T14:31:00Z"
}
```

**Command Response:**

```json
{
  "command": "request_door_unlock",
  "target_id": "ENT_DOOR_TSQ_MARRIOTT_01",
  "status": "success",
  "new_state": "unlocked",
  "latency_ms": 187,
  "timestamp": "2026-01-27T14:31:00Z"
}
```

---

## 6. Latency and Range Defaults

| Artifact Class | Default Latency | Effective Range | Packet Loss (Normal) | Packet Loss (High Heat) |
|---|---|---|---|---|
| Traffic Signal | 50ms | Visual (line of sight) | 0% (hardwired) | 0% (hardwired) |
| CCTV Camera | 500ms | 30m (view cone) | 5% | 20% |
| Information Kiosk | 200ms | 5m (proximity) | 2% | 10% |
| Door/Lock | 150ms | Contact (1m) | 1% | 5% |

**Latency under Heat:**

```
effective_latency = base_latency * (1 + Heat_level * 2)
```

At maximum Heat (1.0), latency triples. At Heat 0.5, latency doubles.

**Packet Loss under Heat:**

```
effective_loss = base_loss + (max_loss - base_loss) * Heat_level
```

Lost events are silently dropped. Consumers must handle gaps. Critical events (forced entry, anomaly spikes) are sent with retry (3 attempts, exponential backoff).

---

## 7. Bus Guarantees

| Property | Guarantee | Notes |
|---|---|---|
| Ordering | Per-topic, per-source | Events from the same artifact on the same topic arrive in order |
| Delivery | At-most-once (default), at-least-once (critical events) | Critical = priority High or above |
| Latency | Best-effort, subject to Heat and load | See Section 6 |
| Retention | Events buffered for 60 sim-seconds | Late subscribers can catch up within window |
| Schema | All events validated against schema on emit | Malformed events rejected with error log |

---

*End of Event Bus Specification v0*
