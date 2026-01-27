# IoT + Evidence + Ledger v0

**Document:** Twin Earth NYC — Part 12, File 4 of 6
**Status:** v0 Draft
**Scope:** IoT artifact inventory, event bus topics, ledger schema, commit rules, persistence, replay tests

---

## 1. Overview

The Times Square slice contains a dense network of IoT artifacts -- traffic signals, CCTV cameras, information kiosks, and access-controlled doors. These artifacts generate events on the event bus, which are processed into evidence records and committed to the persistent ledger. The ledger is the game's memory: it records what happened, when, where, and who was involved. It supports persistence across sessions, replay validation, and Heat channel integration.

This document specifies every IoT artifact in the slice, the events they generate, the ledger schema, commit rules, and persistence behavior.

---

## 2. IoT Artifact Inventory

### 2.1 Summary

| Category | Count | ID Range | Primary Function |
|----------|-------|----------|-----------------|
| Traffic Signals | 12 | SIG_TSQ_001 - SIG_TSQ_012 | Vehicle traffic control |
| Crosswalk Signals | 24 | XWK_TSQ_001 - XWK_TSQ_024 | Pedestrian crossing control |
| CCTV Cameras | 18 | CAM_TSQ_001 - CAM_TSQ_018 | Surveillance, motion detection, evidence |
| Information Kiosks | 5 | KSK_TSQ_001 - KSK_TSQ_005 | Public information, alerts |
| Doors (access-controlled) | 25 | DOOR_TSQ_001 - DOOR_TSQ_025 | Building access, state tracking |

**Total IoT artifacts in slice: 84**

### 2.2 Traffic Signals — Detailed

Each traffic signal controls one direction of vehicle traffic at an intersection. The slice contains intersections at 42nd, 43rd, 44th, 45th, 46th, and 47th Streets.

| Signal ID | Intersection | Controls | Cycle Time | Green Duration | Notes |
|-----------|-------------|----------|-----------|---------------|-------|
| SIG_TSQ_001 | 42nd / 7th Ave | 7th Ave southbound | 90s | 45s green | Major intersection |
| SIG_TSQ_002 | 42nd / 7th Ave | 42nd St westbound | 90s | 35s green | Cross traffic |
| SIG_TSQ_003 | 43rd / Broadway-7th | 7th Ave southbound | 90s | 40s green | Bowtie zone |
| SIG_TSQ_004 | 43rd / Broadway-7th | Broadway northbound | 90s | 35s green | Bowtie zone |
| SIG_TSQ_005 | 44th / Broadway-7th | 7th Ave southbound | 90s | 40s green | Portal zone adjacent |
| SIG_TSQ_006 | 44th / Broadway-7th | Broadway northbound | 90s | 35s green | Portal zone adjacent |
| SIG_TSQ_007 | 45th / Broadway-7th | 7th Ave southbound | 90s | 40s green | Near TKTS |
| SIG_TSQ_008 | 45th / Broadway-7th | Broadway northbound | 90s | 35s green | Near TKTS |
| SIG_TSQ_009 | 46th / 7th Ave | 7th Ave southbound | 90s | 45s green | Standard |
| SIG_TSQ_010 | 46th / Broadway | Broadway northbound | 90s | 40s green | Standard |
| SIG_TSQ_011 | 47th / 7th Ave | 7th Ave southbound | 90s | 45s green | Boundary intersection |
| SIG_TSQ_012 | 47th / Broadway | Broadway northbound | 90s | 40s green | Boundary intersection |

**Signal cycle structure:**
```
SIGNAL CYCLE (90 seconds total):

  Phase 1 — Main avenue green:
    0s:   Main avenue GREEN, cross street RED
    [green_duration]s: Main avenue YELLOW (3s)
    [green_duration + 3]s: ALL RED (2s clearance)

  Phase 2 — Cross street green:
    [green_duration + 5]s: Cross street GREEN, main avenue RED
    [90 - 5]s: Cross street YELLOW (3s)
    [90 - 2]s: ALL RED (2s clearance)

  Phase 3 — Cycle repeats

  Signal coordination:
    - Signals are offset to create a "green wave" down 7th Ave southbound
    - Offset between consecutive intersections: ~8s (tuned for 25 mph)
    - Broadway signals run independently (different flow pattern due to diagonal)
```

### 2.3 Crosswalk Signals — Detailed

Two crosswalk signals per intersection per crossing direction (one on each side of the street). Crosswalk signals are synced to their parent traffic signal.

| XWK ID Range | Intersection | Crossing | Synced To | Walk Duration |
|-------------|-------------|---------|-----------|---------------|
| XWK_TSQ_001-002 | 42nd / 7th Ave | Across 7th Ave | SIG_TSQ_002 phase | 25s |
| XWK_TSQ_003-004 | 42nd / 7th Ave | Across 42nd St | SIG_TSQ_001 phase | 20s |
| XWK_TSQ_005-006 | 43rd / bowtie | Across 7th Ave | SIG_TSQ_003 phase | 22s |
| XWK_TSQ_007-008 | 43rd / bowtie | Across Broadway | SIG_TSQ_004 phase | 22s |
| XWK_TSQ_009-010 | 44th / bowtie | Across 7th Ave | SIG_TSQ_005 phase | 22s |
| XWK_TSQ_011-012 | 44th / bowtie | Across Broadway | SIG_TSQ_006 phase | 22s |
| XWK_TSQ_013-014 | 45th / bowtie | Across 7th Ave | SIG_TSQ_007 phase | 22s |
| XWK_TSQ_015-016 | 45th / bowtie | Across Broadway | SIG_TSQ_008 phase | 22s |
| XWK_TSQ_017-018 | 46th / 7th Ave | Across 7th Ave | SIG_TSQ_009 phase | 25s |
| XWK_TSQ_019-020 | 46th / Broadway | Across Broadway | SIG_TSQ_010 phase | 22s |
| XWK_TSQ_021-022 | 47th / 7th Ave | Across 7th Ave | SIG_TSQ_011 phase | 25s |
| XWK_TSQ_023-024 | 47th / Broadway | Across Broadway | SIG_TSQ_012 phase | 22s |

**Crosswalk signal states:**
```
CROSSWALK STATES:

  WALK:          Solid white walk symbol. Pedestrians may enter crosswalk.
  FLASHING_STOP: Flashing orange hand. Do not start crossing.
                 Countdown timer displayed (seconds remaining).
  DONT_WALK:     Solid orange hand. Do not cross.

  Timing:
    WALK:          first 60% of walk_duration
    FLASHING_STOP: last 40% of walk_duration (with countdown)
    DONT_WALK:     remainder of cycle
```

### 2.4 CCTV Cameras — Detailed

| Camera ID | Location | Mounting | FOV | Pan Range | Coverage Area |
|-----------|----------|---------|-----|-----------|--------------|
| CAM_TSQ_001 | 42nd / 7th Ave, NW pole | Pole, 5m height | 90 deg | Fixed | 42nd/7th intersection |
| CAM_TSQ_002 | 42nd / Broadway, NE pole | Pole, 5m height | 90 deg | Fixed | 42nd/Broadway intersection |
| CAM_TSQ_003 | 42nd / mid-block, south face | Building, 8m height | 60 deg | +/-30 deg pan | 42nd St roadway |
| CAM_TSQ_004 | 43rd / 7th Ave, pole | Pole, 5m height | 90 deg | Fixed | 43rd/7th intersection |
| CAM_TSQ_005 | 43rd / Broadway, building | Building, 10m height | 75 deg | +/-45 deg pan | 43rd/Broadway + One TS base |
| CAM_TSQ_006 | 44th / 7th Ave, pole | Pole, 5m height | 90 deg | Fixed | 44th/7th intersection |
| CAM_TSQ_007 | 44th / Broadway, building | Building, 8m height | 90 deg | +/-30 deg pan | **44th alley / portal zone** |
| CAM_TSQ_008 | 44th / mid-block, pole | Pole, 6m height | 120 deg | Fixed (wide angle) | 44th St between avenues |
| CAM_TSQ_009 | 45th / 7th Ave, pole | Pole, 5m height | 90 deg | Fixed | 45th/7th intersection |
| CAM_TSQ_010 | 45th / Broadway, building | Building, 10m height | 75 deg | +/-45 deg pan | TKTS area from south |
| CAM_TSQ_011 | Father Duffy Square, pole | Pole, 6m height | 120 deg | +/-60 deg pan | TKTS Red Steps + statue |
| CAM_TSQ_012 | 46th / 7th Ave, pole | Pole, 5m height | 90 deg | Fixed | 46th/7th intersection |
| CAM_TSQ_013 | 46th / Broadway, pole | Pole, 5m height | 90 deg | Fixed | 46th/Broadway intersection |
| CAM_TSQ_014 | 47th / 7th Ave, pole | Pole, 5m height | 90 deg | Fixed | 47th/7th intersection |
| CAM_TSQ_015 | 47th / Broadway, pole | Pole, 5m height | 90 deg | Fixed | 47th/Broadway intersection |
| CAM_TSQ_016 | One Times Square, south face | Building, 15m height | 60 deg | Fixed | South approach from 42nd |
| CAM_TSQ_017 | Marriott Marquis entrance | Building, 4m height | 90 deg | Fixed | Hotel entrance + 45th sidewalk |
| CAM_TSQ_018 | 44th service entrance | Building, 3m height | 60 deg | Fixed | Service door (DOOR_TSQ_005 area) |

**CCTV behavior:**
```
CCTV DETECTION MODEL:

  Each camera runs a detection pass at its configured rate:
    - Normal: 2Hz (every 0.5s)
    - Elevated Heat: 4Hz (every 0.25s)
    - Alert mode: 10Hz (every 0.1s)

  Detection types:
    MOTION:
      - Trigger: any entity moving within FOV at > 0.5 m/s
      - Event: security.camera.motion
      - Confidence: 0.8 (normal), reduced by: distance (-0.1 per 10m),
        occlusion (-0.3 per obstacle), anomaly zone (-0.3 if inside)

    OBSERVATION:
      - Trigger: significant event detected (anomaly, forced door, fight,
        known entity, artifact signature)
      - Event: security.camera.observation
      - Contains: entity IDs, event classification, confidence score,
        timestamp, camera position
      - This is the primary evidence-generation event

    ARTIFACT_DETECTION:
      - Trigger: artifact with active signature within 5m of camera
      - Event: security.camera.observation (subtype: artifact_signature)
      - Confidence: 0.6 (signatures are subtle)
      - Range: 5m maximum detection distance for artifacts

  Camera failure:
    - At Heat Critical (0.7-0.9): 5% chance per detection pass of camera
      returning no result (simulating system stress)
    - At Heat Crisis (0.9+): 15% failure rate
    - Anomaly zone: cameras within anomaly radius have -30% confidence
      on all detections (EM interference)
    - Camera jammed: player or NPC action can disable camera for 60s
      (generates security.camera.observation with type "tampered")
```

### 2.5 Information Kiosks — Detailed

| Kiosk ID | Location | Type | Normal Content | Alert Content |
|----------|----------|------|---------------|---------------|
| KSK_TSQ_001 | TKTS area, south end | Freestanding touchscreen | Show listings, maps, ads | Emergency alerts, evacuation routes |
| KSK_TSQ_002 | 42nd / Broadway, NE corner | Freestanding touchscreen | Subway maps, directions | Emergency alerts |
| KSK_TSQ_003 | 44th / 7th Ave, east side | Freestanding touchscreen | Local info, ads, weather | Emergency alerts, anomaly warning |
| KSK_TSQ_004 | 45th pedestrian zone | Freestanding touchscreen | Show listings, restaurant guide | Emergency alerts |
| KSK_TSQ_005 | 46th / Broadway, west side | Freestanding touchscreen | Maps, directory, ads | Emergency alerts |

**Kiosk behavior:**
```
KIOSK STATE MACHINE:

  IDLE:
    - Displays rotating content (ads, maps, info)
    - Generates no events
    - Player interaction: view content (not gameplay-critical)

  ALERT:
    - Triggered by: public_info.kiosk.alert event on bus
    - Displays alert content (emergency message, evacuation route)
    - Generates: public_info.kiosk.display_changed event
    - NPC reaction: nearby NPCs may stop and read alert (tourist preset)

  SPOOFED:
    - Triggered by: player or NPC hack action
    - Displays false information
    - Generates: security.camera.observation from any camera with FOV on kiosk
    - Heat impact: Social +0.05, Institutional +0.03
    - Duration: 120s before auto-reset (or manual reset by authority)
    - Evidence: spoofing event logged in ledger

  ERROR:
    - Triggered by: Heat Crisis (0.9+) or physical damage
    - Displays error screen / static
    - Generates: iot.device.failure event
    - Requires: manual reset (authority action) or time-based auto-recovery (300s)
```

### 2.6 Doors — Detailed

25 access-controlled doors along Broadway and 7th Avenue building frontages. Doors track their state and generate events on state change.

| Door ID Range | Location | Count | Default State | Lock Type |
|--------------|----------|-------|--------------|-----------|
| DOOR_TSQ_001 - DOOR_TSQ_005 | 42nd-43rd block, Broadway side | 5 | Locked (after hours) / Unlocked (business hours) | Electronic keycard |
| DOOR_TSQ_006 - DOOR_TSQ_010 | 43rd-44th block, Broadway side | 5 | Locked (after hours) / Unlocked (business hours) | Electronic keycard |
| DOOR_TSQ_011 - DOOR_TSQ_015 | 44th-45th block, mixed | 5 | Mixed (see notes) | Electronic + deadbolt |
| DOOR_TSQ_016 - DOOR_TSQ_020 | 45th-46th block, 7th Ave side | 5 | Locked (after hours) / Unlocked (business hours) | Electronic keycard |
| DOOR_TSQ_021 - DOOR_TSQ_025 | 46th-47th block, mixed | 5 | Mixed | Electronic + physical |

**Key doors for gameplay:**

| Door ID | Specific Location | Significance |
|---------|------------------|-------------|
| DOOR_TSQ_005 | 43rd St alley (seam S05 area) | Service entrance, backstage seam |
| DOOR_TSQ_008 | 44th / Broadway building | Near portal zone, evidence location |
| DOOR_TSQ_011 | 44th St service entrance (seam S08) | Backstage access, player may attempt entry |
| DOOR_TSQ_016 | Marriott Marquis side entrance | Near seam S07 |
| DOOR_TSQ_022 | 46th / 7th Ave, secure door | Authority access point |

**Door state machine:**
```
DOOR STATES:

  LOCKED:     Closed and locked. Cannot be opened without key/card/force.
  UNLOCKED:   Closed but unlocked. Can be opened by any entity.
  OPEN:       Open. Entities can pass through. Auto-closes after 5s.
  FORCED:     Forced open (lock broken). Permanent until repaired.
              Generates: access.door.state_changed (type: "forced")
              Heat impact: Physical +0.02, Institutional +0.05
              CCTV evidence generated if camera has FOV on door.

  State transitions:
    LOCKED -> UNLOCKED: keycard/schedule/authority action
    LOCKED -> FORCED: player force action (tool required)
    UNLOCKED -> OPEN: entity approaches and activates
    OPEN -> UNLOCKED: auto-close timer (5s)
    OPEN -> LOCKED: manual lock by authority
    FORCED -> LOCKED: repair event (authority or maintenance NPC)

  Schedule:
    Business hours (08:00 - 20:00): customer-facing doors UNLOCKED
    After hours (20:00 - 08:00): all doors LOCKED
    Service doors: always LOCKED (keycard access only)
    Exception: during Crisis Heat, all doors may be forced open for evacuation
```

---

## 3. Event Bus — Active Topics

All topics from the Part 7 Event Bus specification are active in the Times Square slice. Below is the complete list with Times Square-specific details.

### 3.1 Topic Inventory

| Topic | Source | Rate (normal) | Rate (peak) | Payload Size | Priority |
|-------|--------|--------------|-------------|-------------|----------|
| `traffic.signal.changed` | 12 traffic signals | ~8/min (each cycles every 90s) | Same (deterministic) | 128 bytes | Normal |
| `traffic.crosswalk.changed` | 24 crosswalk signals | ~16/min | Same | 96 bytes | Normal |
| `security.camera.motion` | 18 cameras | ~36/min (2Hz normal, most detect) | ~180/min (10Hz alert) | 256 bytes | Low |
| `security.camera.observation` | 18 cameras (event-driven) | ~2/min (normal) | ~30/min (during incident) | 512 bytes | High |
| `access.door.state_changed` | 25 doors | ~5/min (business hours) | ~15/min (evacuation) | 128 bytes | Normal |
| `public_info.kiosk.alert` | System / narrative | 0 (normal) | ~5/min (emergency) | 256 bytes | High |
| `public_info.kiosk.display_changed` | 5 kiosks | ~1/min (rotation) | ~5/min (alert mode) | 128 bytes | Low |
| `anomaly.zone.spike` | Anomaly system | 0 (normal) | 10/min (active anomaly) | 512 bytes | Critical |
| `anomaly.zone.update` | Anomaly system | 0 (normal) | 2/min (active anomaly) | 256 bytes | High |
| `evidence.recorded` | Evidence processor | ~2/min (normal) | ~20/min (incident) | 1024 bytes | High |
| `evidence.committed` | Ledger | ~1/min (normal) | ~10/min (incident) | 256 bytes | Normal |
| `heat.channel.changed` | Heat system | ~4/min (4 channels) | ~20/min (active incident) | 64 bytes | Normal |
| `authority.dispatch.unit` | Authority system | 0 (normal) | ~5/min (crisis) | 256 bytes | Critical |
| `authority.action.taken` | Authority NPCs | ~1/min (patrol) | ~10/min (active response) | 512 bytes | High |
| `npc.hero.observation` | Hero NPCs | ~5/min (routine) | ~20/min (incident) | 512 bytes | Normal |
| `portal.state.changed` | Portal system | 0 (normal) | ~5/event (state transitions) | 512 bytes | Critical |
| `iot.device.failure` | Any IoT device | 0 (normal) | ~5/min (crisis) | 128 bytes | High |

### 3.2 Event Bus Throughput Budget

| Metric | Budget | Notes |
|--------|--------|-------|
| Max events per second | 200 | All topics combined |
| Max event payload per second | 50 KB | Sum of all event payloads |
| Event processing latency | < 5ms (p99) | From publish to all subscribers notified |
| Event queue depth | 500 events max | Events beyond this are dropped with warning |
| CPU budget | 0.5ms per frame | Event bus processing |

### 3.3 Event Bus Topology

```
EVENT BUS ARCHITECTURE (Times Square slice):

  Publishers:                     Event Bus                    Subscribers:
  ___________                    ___________                   ___________
 |  Traffic  |                  |           |                 |  Evidence |
 |  Signals  |---publish-----→ |           |---subscribe---→ | Processor |
 |  (12+24)  |                  |           |                 |___________|
 |___________|                  |           |                  ___________
  ___________                   |  Central  |                 |  Heat     |
 |   CCTV    |---publish-----→ |  Message  |---subscribe---→ | System    |
 |  Cameras  |                  |  Queue    |                 |___________|
 |   (18)    |                  |           |                  ___________
 |___________|                  |           |                 |  NPC AI   |
  ___________                   |  Topics:  |---subscribe---→ | (react to |
 |  Doors    |---publish-----→ |  17 active|                 |  events)  |
 |   (25)    |                  |           |                 |___________|
 |___________|                  |           |                  ___________
  ___________                   |           |                 |  Ledger   |
 |  Kiosks   |---publish-----→ |           |---subscribe---→ | Writer    |
 |   (5)     |                  |           |                 |___________|
 |___________|                  |           |                  ___________
  ___________                   |           |                 |  Show     |
 |  Anomaly  |---publish-----→ |           |---subscribe---→ | Director  |
 |  System   |                  |           |                 |___________|
 |___________|                  |           |                  ___________
  ___________                   |           |                 |  Audio    |
 |  Portal   |---publish-----→ |           |---subscribe---→ | System    |
 |  System   |                  |           |                 |___________|
 |___________|                  |___________|
  ___________
 | Authority |---publish+subscribe (bidirectional)
 |  System   |
 |___________|
  ___________
 |  Hero NPC |---publish+subscribe (bidirectional)
 |  System   |
 |___________|
```

---

## 4. Ledger Schema

### 4.1 Event Record Schema (v0)

Every significant event is recorded as a ledger entry. The schema supports all event categories and is designed for queryability and replay.

```json
{
  "event_id": "EVT_<category>_<timestamp_hash>",
  "category": "damage | access | evidence | anomaly | authority_response | heat_change",
  "subcategory": "<specific_type>",
  "timestamp": "ISO-8601 with milliseconds",
  "sim_time": 0.0,
  "location": {
    "x": 0.0,
    "y": 0.0,
    "z": 0.0,
    "zone": "TSQ_001",
    "landmark_ref": "nearest_landmark_id"
  },
  "entities_involved": [
    {
      "entity_id": "string",
      "entity_type": "player | hero_npc | bg_npc | vehicle | device | anomaly | portal",
      "role": "actor | target | witness | sensor"
    }
  ],
  "observations": [
    {
      "observation_id": "OBS_<source>_<timestamp_hash>",
      "source_type": "cctv | witness | sensor | player",
      "source_id": "CAM_TSQ_007",
      "confidence": 0.85,
      "description": "Human-readable observation"
    }
  ],
  "description": "Human-readable event summary",
  "heat_impact": {
    "physical": 0.0,
    "social": 0.0,
    "institutional": 0.0,
    "ecological": 0.0
  },
  "committed": true,
  "commit_reason": "auto_authority | auto_corroborated | auto_damage | auto_anomaly | player_save | timer_batch",
  "reversible": false,
  "tags": ["anomaly", "portal", "evidence", "authority"],
  "linked_events": ["EVT_xxx_yyy"],
  "data": {}
}
```

### 4.2 Event Categories

| Category | Subcategories | Description | Typical Sources |
|----------|--------------|-------------|----------------|
| **damage** | object_broken, vehicle_collision, explosion, structural | Physical damage to world objects | Physics system, NPC actions, player actions |
| **access** | door_opened, door_forced, door_locked, area_entered, area_exited | Access control events | Door sensors, area triggers |
| **evidence** | visual_observation, audio_observation, sensor_reading, artifact_detected | Evidence gathered by cameras, witnesses, or sensors | CCTV, hero NPCs, kiosks |
| **anomaly** | zone_spike, zone_growth, zone_stable, zone_decay, portal_formed, portal_collapsed | Anomaly and portal state changes | Anomaly system, portal system |
| **authority_response** | unit_dispatched, cordon_placed, arrest_attempted, area_cleared, road_closed | Authority actions taken | Authority NPC system |
| **heat_change** | channel_threshold_crossed, spike, decay_milestone | Significant Heat level changes | Heat system |

### 4.3 Example Ledger Entries

**Example 1: Anomaly appears**
```json
{
  "event_id": "EVT_anomaly_1706385600_a7f3",
  "category": "anomaly",
  "subcategory": "zone_spike",
  "timestamp": "2024-01-28T14:01:00.000Z",
  "sim_time": 60.0,
  "location": {
    "x": -25.0, "y": 0.0, "z": 45.0,
    "zone": "TSQ_001",
    "landmark_ref": "44th_broadway_alley"
  },
  "entities_involved": [
    {"entity_id": "ANOMALY_001", "entity_type": "anomaly", "role": "actor"}
  ],
  "observations": [
    {
      "observation_id": "OBS_CAM_TSQ_007_1706385600_b2e1",
      "source_type": "cctv",
      "source_id": "CAM_TSQ_007",
      "confidence": 0.7,
      "description": "Anomalous visual distortion detected at 44th St alley. Edge detection failure, motion artifacts."
    },
    {
      "observation_id": "OBS_HERO_03_1706385600_c4d2",
      "source_type": "witness",
      "source_id": "HERO_03",
      "confidence": 0.9,
      "description": "Marcus 'Lens' Cole observed shimmering distortion from TKTS steps. Began recording."
    }
  ],
  "description": "Anomaly zone spike at 44th St. Radius 3m initial. Visual shimmer and low-frequency hum detected.",
  "heat_impact": {
    "physical": 0.0,
    "social": 0.10,
    "institutional": 0.05,
    "ecological": 0.20
  },
  "committed": true,
  "commit_reason": "auto_anomaly",
  "reversible": false,
  "tags": ["anomaly", "first_contact"],
  "linked_events": [],
  "data": {
    "anomaly_id": "ANOMALY_001",
    "initial_radius": 3.0,
    "growth_model": "exponential_decay",
    "signature_type": "gravity_wobble_visual_distortion"
  }
}
```

**Example 2: Door forced**
```json
{
  "event_id": "EVT_access_1706385900_d5e3",
  "category": "access",
  "subcategory": "door_forced",
  "timestamp": "2024-01-28T14:05:00.000Z",
  "sim_time": 300.0,
  "location": {
    "x": -30.0, "y": 0.0, "z": 30.0,
    "zone": "TSQ_001",
    "landmark_ref": "44th_service_entrance"
  },
  "entities_involved": [
    {"entity_id": "PLAYER_001", "entity_type": "player", "role": "actor"},
    {"entity_id": "DOOR_TSQ_011", "entity_type": "device", "role": "target"}
  ],
  "observations": [
    {
      "observation_id": "OBS_CAM_TSQ_018_1706385900_e6f4",
      "source_type": "cctv",
      "source_id": "CAM_TSQ_018",
      "confidence": 0.85,
      "description": "Individual forced service entrance door at 44th St. Lock mechanism compromised."
    }
  ],
  "description": "Service door DOOR_TSQ_011 forced open by player. Lock broken, door now in FORCED state.",
  "heat_impact": {
    "physical": 0.02,
    "social": 0.0,
    "institutional": 0.05,
    "ecological": 0.0
  },
  "committed": true,
  "commit_reason": "auto_damage",
  "reversible": false,
  "tags": ["access", "forced_entry", "evidence"],
  "linked_events": [],
  "data": {
    "door_id": "DOOR_TSQ_011",
    "previous_state": "LOCKED",
    "new_state": "FORCED",
    "method": "physical_force",
    "tool_used": "crowbar"
  }
}
```

---

## 5. Commit Points

### 5.1 Commit Rules

Events accumulate in a staging buffer before being committed to the persistent ledger. Committed events are permanent and cannot be retroactively altered (though they can be superseded by later events).

| Commit Type | Trigger | Latency | Description |
|-------------|---------|---------|-------------|
| **Auto-commit: Authority** | `authority.action.taken` event | Immediate | Any authority action (cordon, dispatch, arrest) commits all related pending events |
| **Auto-commit: Corroborated** | Evidence with 2+ independent observations | Immediate | When an event has observations from 2+ different sources, it auto-commits |
| **Auto-commit: Damage** | `access.door.state_changed` (forced), explosion, structural damage | Immediate | Physical state changes that cannot be undone |
| **Auto-commit: Anomaly** | `anomaly.zone.spike`, `portal.state.changed` | Immediate | Anomaly and portal state transitions |
| **Player-commit** | Player explicit save action | On action | Player chooses to save progress; all pending events committed |
| **Timer-commit** | Every 5 minutes sim-time | Batch | Uncommitted micro-events are reviewed: significant events committed, trivial events decayed |

### 5.2 Commit Process

```
COMMIT PROCESS:

  staging_buffer: list of uncommitted events (ordered by timestamp)

  on_event_received(event):
    event.committed = false
    staging_buffer.append(event)
    check_auto_commit_rules(event)

  check_auto_commit_rules(event):
    // Rule 1: Authority action commits related events
    if event.category == "authority_response":
      commit_related(event, staging_buffer)

    // Rule 2: Corroboration check
    if event.category == "evidence":
      for other in staging_buffer:
        if events_corroborate(event, other):
          commit(event)
          commit(other)

    // Rule 3: Damage auto-commit
    if event.category == "damage" or event.subcategory == "door_forced":
      commit(event)

    // Rule 4: Anomaly auto-commit
    if event.category == "anomaly":
      commit(event)

  events_corroborate(a, b):
    // Two events corroborate if they describe the same incident
    // from independent sources within 60s and 50m of each other
    return (
      abs(a.sim_time - b.sim_time) < 60 and
      distance(a.location, b.location) < 50 and
      a.observations[0].source_id != b.observations[0].source_id and
      a.category == b.category
    )

  commit(event):
    event.committed = true
    event.commit_reason = <determined by rule>
    ledger.write(event)
    publish("evidence.committed", event.event_id)

  timer_batch_commit():  // every 5 min sim-time
    for event in staging_buffer:
      if not event.committed:
        if event.heat_impact.total() > 0.01:
          commit(event)  // significant enough to persist
          event.commit_reason = "timer_batch"
        else:
          decay(event)   // trivial, remove from staging

  commit_related(trigger_event, buffer):
    // Find all events related to the trigger (same location cluster,
    // same entities, within time window)
    for event in buffer:
      if not event.committed:
        if (distance(event.location, trigger_event.location) < 100 and
            abs(event.sim_time - trigger_event.sim_time) < 300):
          commit(event)
          event.commit_reason = "auto_authority"
```

---

## 6. Persistence Rules

### 6.1 Persistence by Category

| Category | Persistence | Decay Rule | Storage Format | Cross-Session |
|----------|-------------|-----------|---------------|---------------|
| **Damage** (broken objects) | Permanent until repaired | No decay | Full record with before/after state | Yes |
| **Door lock states** | Permanent until maintenance | Reset on maintenance event (authority repairs) | Current state + change history | Yes |
| **Evidence records** | Permanent (committed) | Raw observation data summarized after 1h sim-time; summary + key frames retained | Summary + key observation snapshots | Yes |
| **Heat levels** | Continuous | Channel-specific decay rates (see Heat doc) | Sampled every 30s, stored as time series | Session only (resets on new session with residual) |
| **Anomaly residue** | Persistent | Fades over 24h sim-time following decay curve | Radius + intensity curve over time | Yes |
| **NPC hero memory** | Cross-session | Habit strengthening: repeated observations reinforce; emotional weight decays per sim-time | Per-NPC memory store (100 entries max) | Yes |
| **Player inventory** | Permanent | No decay (artifacts may have their own stability) | Item list with properties | Yes |
| **Authority state** | Session + carryover | Patrol routes reset; alert level carries over with decay | Current disposition + recent action log | Partial |

### 6.2 Evidence Summarization

After 1 hour of sim-time, raw evidence records are summarized to save storage:

```
EVIDENCE SUMMARIZATION:

  Trigger: event.sim_time_since_commit > 3600 (1 hour)

  Process:
    1. Group related observations by location cluster and time window
    2. Select key frame: the observation with highest confidence
    3. Generate summary text from observation descriptions
    4. Store: summary + key frame + metadata
    5. Discard: raw motion detection data, low-confidence observations,
       redundant corroborating details
    6. Retain: all committed events (just compress observation details)

  Example:
    Before summarization (3 records):
      - CAM_TSQ_007: "Motion detected at 44th alley, confidence 0.4"
      - CAM_TSQ_007: "Anomalous visual distortion, confidence 0.7"
      - CAM_TSQ_008: "Corroborating distortion from 44th mid-block, confidence 0.6"

    After summarization (1 summary):
      - "Anomalous visual distortion confirmed at 44th St alley by 2 cameras.
         Peak confidence 0.7. Duration: 45 seconds before portal formation."
      - Key frame: CAM_TSQ_007 observation at confidence 0.7
```

### 6.3 Session Boundaries

```
SESSION SAVE/LOAD:

  On session save:
    1. Commit all staging buffer events (force timer_batch_commit)
    2. Serialize ledger to disk (JSON or binary format)
    3. Save current Heat levels (all 4 channels)
    4. Save all door states
    5. Save anomaly residue positions and intensities
    6. Save hero NPC memory stores
    7. Save player inventory
    8. Save authority disposition

  On session load:
    1. Load ledger from disk
    2. Restore door states
    3. Restore anomaly residue (advance decay by real-time elapsed)
    4. Restore hero NPC memories
    5. Restore player inventory
    6. Heat: load saved levels, apply decay for elapsed sim-time
       (capped at 24h decay maximum)
    7. Authority: reset patrol routes, apply saved alert level with decay
    8. Traffic signals: reset to cycle start (no persistence needed)
    9. CCTV: reset to normal operation
    10. Kiosks: reset to IDLE state
```

---

## 7. Replay Tests

Three replay tests verify ledger integrity, determinism, and rollback capability.

### 7.1 Test 1: Revisit Test

**Purpose:** Verify that world state changes persist when the player leaves and returns.

```
REVISIT TEST PROTOCOL:

  Setup:
    - Clean ledger, all doors locked, no anomaly
    - Player starts at 42nd St

  Steps:
    1. Player walks to DOOR_TSQ_005 (43rd alley service door)
    2. Player forces door (DOOR_TSQ_005 -> FORCED state)
    3. Verify: access.door.state_changed event generated
    4. Verify: CAM_TSQ_018 generates security.camera.observation
    5. Verify: ledger contains committed event for door force
    6. Player walks to 47th St (leaves area)
    7. Wait 60 seconds sim-time
    8. Player walks back to DOOR_TSQ_005

  Expected results:
    - Door state = FORCED (not reset)
    - CCTV evidence exists in ledger (observation committed)
    - Heat: Physical +0.02, Institutional +0.05 (decayed slightly over 60s)
    - No orphaned events in staging buffer

  PASS criteria:
    - All expected results confirmed
    - Door state query returns FORCED
    - Ledger query for DOOR_TSQ_005 returns force event
    - Evidence observation from CAM_TSQ_018 is committed and queryable
```

### 7.2 Test 2: Replay Determinism Test

**Purpose:** Verify that running the same scenario with the same seed produces consistent ledger output.

```
REPLAY TEST PROTOCOL:

  Setup:
    - Seed: 42 (fixed random seed for all systems)
    - Clean ledger
    - Time: 2:00 PM
    - All systems at default state

  Steps:
    Run A:
      1. Start scenario: "anomaly at 44th" (scripted event sequence)
      2. Let simulation run for 5 minutes sim-time (no player input)
      3. Export ledger as JSON (ledger_run_A.json)
      4. Export Heat state (heat_run_A.json)
      5. Export NPC positions (npc_run_A.json)

    Run B:
      1. Reset all state to clean
      2. Set seed to 42
      3. Start same scenario
      4. Let simulation run for 5 minutes (no player input)
      5. Export ledger as JSON (ledger_run_B.json)
      6. Export Heat state (heat_run_B.json)
      7. Export NPC positions (npc_run_B.json)

  Comparison:
    - Event count: Run A event count == Run B event count (+/- 2%)
    - Event types: same set of event categories in both runs
    - Event ordering: committed events appear in same order
    - Heat levels: all channels within +/- 0.01 of each other
    - NPC positions: hero NPCs within 2m of same position at T+300s
    - Ledger structure: same committed/uncommitted ratio

  Stochastic tolerance:
    - Background NPC spawning has random jitter: +/- 2% event count acceptable
    - Camera detection has confidence variance: observation text may differ slightly
    - Heat values may differ by accumulated floating-point error: +/- 0.01

  PASS criteria:
    - All comparison metrics within tolerance
    - No missing event categories between runs
    - Committed event ordering identical
```

### 7.3 Test 3: Rollback Test

**Purpose:** Verify that a ledger snapshot can be restored cleanly with no orphaned references.

```
ROLLBACK TEST PROTOCOL:

  Setup:
    - Clean state, standard scenario

  Steps:
    1. Run simulation for 2 minutes sim-time
    2. Create snapshot:
       - Ledger state (all events, staging buffer)
       - Door states (all 25 doors)
       - Heat levels (all 4 channels)
       - Anomaly state (if any)
       - NPC memory states (all hero NPCs)
       - Save as snapshot_T120.dat
    3. Run simulation for 5 more minutes (total 7 min)
       - During this time: anomaly triggers, portal opens, evidence accumulates
    4. Verify: ledger has significantly more events than at T+120
    5. Execute rollback to snapshot_T120.dat
    6. Verify clean state restoration

  Verification after rollback:
    - Ledger event count matches snapshot (events from T+120 to T+420 removed)
    - No events reference entities that no longer exist
    - No orphaned observation references in committed events
    - Door states match snapshot values
    - Heat levels match snapshot values
    - Anomaly state matches snapshot (should be inactive at T+120)
    - Hero NPC memories match snapshot
    - Staging buffer restored (uncommitted events from snapshot preserved)
    - No null references in any data structure

  Integrity checks:
    for event in ledger.all_events():
      for entity in event.entities_involved:
        assert entity_exists(entity.entity_id), "Orphaned entity reference"
      for obs in event.observations:
        assert observation_source_exists(obs.source_id), "Orphaned observation source"
      for linked in event.linked_events:
        assert ledger.event_exists(linked), "Orphaned event link"

  PASS criteria:
    - All integrity checks pass (zero orphaned references)
    - State matches snapshot exactly
    - Simulation can continue from restored state without errors
    - Running for 60s after rollback produces no exceptions or data corruption
```

---

## 8. Ledger Query Interface

The ledger supports queries for gameplay systems (Heat calculation, evidence display, faction knowledge) and for debugging/QA.

### 8.1 Query API

```
LEDGER QUERY API:

  // Get all events in time range
  ledger.query(
    time_start: ISO-8601,
    time_end: ISO-8601,
    category: optional string,
    zone: optional string
  ) -> list[LedgerEvent]

  // Get events involving an entity
  ledger.query_by_entity(
    entity_id: string,
    role: optional string  // "actor", "target", "witness", "sensor"
  ) -> list[LedgerEvent]

  // Get events near a location
  ledger.query_by_location(
    x: float, y: float, z: float,
    radius: float,
    time_start: optional ISO-8601,
    time_end: optional ISO-8601
  ) -> list[LedgerEvent]

  // Get current state of a device
  ledger.device_state(
    device_id: string
  ) -> DeviceState

  // Get heat impact summary for a time range
  ledger.heat_summary(
    time_start: ISO-8601,
    time_end: ISO-8601,
    zone: optional string
  ) -> HeatImpactSummary

  // Get evidence chain for an incident
  ledger.evidence_chain(
    seed_event_id: string,
    depth: int = 3  // how many linked-event hops to follow
  ) -> list[LedgerEvent]

  // Export full ledger (for regression/replay)
  ledger.export(format: "json" | "binary") -> bytes
```

### 8.2 Query Performance Targets

| Query Type | Target Latency | Max Results | Notes |
|------------|---------------|-------------|-------|
| Time range (1 min) | < 1ms | 1000 | Indexed by timestamp |
| Entity query | < 2ms | 500 | Indexed by entity_id |
| Location query (50m radius) | < 5ms | 200 | Spatial index |
| Device state | < 0.5ms | 1 | Direct lookup |
| Heat summary | < 2ms | N/A | Aggregation query |
| Evidence chain (depth 3) | < 10ms | 100 | Graph traversal |
| Full export | < 100ms | All | Serialization |

---

*End of document. Next: Heat + Anomaly + Portal Pocket v0.*
