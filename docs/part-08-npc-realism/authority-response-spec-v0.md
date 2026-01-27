# Authority Response Spec v0

**Document:** Part 8 — NPC Realism
**File:** `authority-response-spec-v0.md`
**Status:** Draft v0
**Last Updated:** 2026-01-27
**Depends On:** NPC Taxonomy + Tier Plan v0, Sensor Interface Spec v0, Part 7 (Event Bus + Heat System + Evidence Ledger)
**Feeds Into:** Runtime Validation Checklist, Part 7 Dispatch Integration, Mission Design

---

## 1. Authority Agent Types (v1)

| Role | Tier | Count (Times Square) | Primary Behavior | Trigger Condition | Equipment |
|------|------|----------------------|------------------|-------------------|-----------|
| Patrol cop | Hero | 2 -- 5 | Walk beat route, respond to alerts, initiate pursuit | Evidence threshold, Heat threshold, direct sighting of crime | Radio (dispatch link), vehicle (optional, parked at precinct) |
| Crowd control cop | Background | 0 -- 5 (event-driven) | Place cordons, direct pedestrian flow via megaphone, maintain perimeter | High crowd density + significant event (anomaly, explosion, large protest) | Barriers (deployable), megaphone (audio source for NPC redirection) |
| Detective / analyst | Hero (future) | 0 -- 1 (v2 feature) | Review accumulated evidence, detect patterns, issue warrants | Accumulated evidence confidence exceeds investigation threshold | Terminal access (queries evidence ledger directly) |

### Patrol Cop Behavior Model

Patrol cops are **hero-tier NPCs** with the full sensor suite (forward camera, depth probes, audio proxy) plus an additional **radio channel** that receives dispatch messages. Their behavior combines:

1. **Beat patrol** -- a learned heuristic loop through assigned waypoints (2 -- 4 waypoints per beat, 5 -- 10 minute cycle).
2. **Alert response** -- interrupts beat when dispatch message or direct sensor stimulus triggers response.
3. **Pursuit policy** -- a separately trained RL policy activated when a suspect is identified (see Section 3).

### Crowd Control Behavior Model

Crowd control cops are **background-tier NPCs** with scripted behavior:

1. Receive cordon placement order via event bus.
2. Navigate to assigned barrier position (A* pathfinding on navmesh).
3. Deploy barrier (2 s animation).
4. Enter stationary state, periodically emit megaphone audio cue (redirects nearby background NPCs).
5. Remove barrier when stand-down order received.

---

## 2. Response Triggers

The authority dispatch system evaluates incoming events from the Part 7 event bus and determines the appropriate response level.

### Trigger Matrix

| # | Trigger Type | Threshold | Response Level | Dispatch Action |
|---|-------------|-----------|----------------|-----------------|
| 1 | Direct sighting of crime | Immediate (cop sensor detects criminal act) | **Priority 1** -- Immediate | Nearest patrol unit pursues; backup dispatched if available |
| 2 | CCTV evidence, confidence > 0.7 | Single event | **Priority 1** -- Immediate | Dispatch nearest unit to camera location with target description |
| 3 | CCTV evidence, confidence 0.4 -- 0.7 | 3+ events within 5 min window | **Priority 2** -- Investigation | Dispatch unit for area sweep; no specific target, patrol mode with heightened awareness |
| 4 | Heat (physical) > 0.5 | Sustained for 2 min | **Priority 3** -- Presence increase | Increase patrol density in affected grid cells (spawn additional patrol cop if below max) |
| 5 | Heat (institutional) > 0.7 | Sustained for 5 min | **Priority 3** -- Containment | Activate cordons + road closures around high-Heat zone |
| 6 | Anomaly detected | Any anomaly event | **Priority 0** -- Critical | Highest priority dispatch; all available units redirect. Containment protocol initiated (cordons at 50 m radius). |

### Priority Resolution

When multiple triggers are active simultaneously, the dispatch system processes them in priority order (0 = highest). Rules:

- A unit already engaged in a Priority 1 pursuit will **not** be reassigned to Priority 2 or 3 tasks.
- A unit engaged in Priority 2 or 3 tasks **will** be reassigned to Priority 0 (anomaly) or Priority 1 (active crime) if it is the nearest available.
- Maximum simultaneous pursuits: 2 (to prevent all patrol cops from chasing the same target).
- If all units are engaged and a new Priority 1 trigger arrives, the trigger is queued with a 30 s timeout. If no unit becomes available, the event is logged as "unresponded" in the evidence ledger.

---

## 3. Pursuit Mechanics (Perception-Based)

Pursuit is entirely **perception-driven** -- cops do not have access to ground-truth player position. They must see, hear, or receive dispatched information to track a suspect.

### 3.1 Pursuit State Machine

```
                            +-----------+
                            |   PATROL  |
                            +-----+-----+
                                  |
                    [trigger: sighting OR dispatch]
                                  |
                                  v
                          +-------+-------+
                          | ACTIVE PURSUIT|
                          +-------+-------+
                                  |
                  +---------------+---------------+
                  |                               |
       [target caught]                   [LOS break > 10s]
                  |                               |
                  v                               v
          +-------+-------+              +-------+-------+
          |    ARRESTED   |              |  SEARCH MODE  |
          +---------------+              +-------+-------+
                                                 |
                                 +---------------+---------------+
                                 |                               |
                      [reacquire target]               [timeout 60s]
                                 |                               |
                                 v                               v
                         +-------+-------+              +--------+--------+
                         | ACTIVE PURSUIT|              | RETURN TO PATROL|
                         +---------------+              +-----------------+
```

### 3.2 Pursuit Phase Details

#### Initiation

| Condition | Detail |
|-----------|--------|
| Direct sighting | Cop's forward camera detects suspect within FOV (120 degrees) and range (50 m). Identification requires suspect to match a known description (clothing, build) with confidence > 0.6 OR cop witnesses criminal act directly. |
| Dispatch | Cop receives `authority.dispatch.unit` event with target description and last known location. Cop navigates to location and begins visual search. |
| Confidence decay | If cop sees suspect but confidence < 0.6, cop enters "watch" state (follows at distance, does not initiate pursuit). |

#### Active Pursuit

| Parameter | Value |
|-----------|-------|
| Cop run speed | 1.2x NPC base speed (catchable in straight line; player advantage in agility/turns) |
| Tracking method | Line-of-sight following. Cop's forward camera must maintain target in FOV. |
| Pathfinding | Real-time navmesh pathfinding toward last observed target position. Cop obeys traffic signals only if no active pursuit (ignores signals during pursuit). |
| Communication | Cop emits `authority.pursuit.update` event every 5 s with `{ unit_id, target_last_position, target_heading, confidence }`. Other cops receive this via radio channel. |
| Stamina | No stamina limit in v1 (pursuit can continue indefinitely while LOS maintained). |

#### Line-of-Sight Break

| Parameter | Value |
|-----------|-------|
| LOS break timer | Starts when target leaves cop's FOV or is fully occluded |
| Timer duration | 10 seconds |
| Camera assist | During LOS break, if any CCTV camera in the network detects the target, the LOS break timer resets and cop is redirected to camera's observed position |
| If timer expires | Cop transitions to Search Mode |

#### Search Mode

| Parameter | Value |
|-----------|-------|
| Duration | 60 seconds maximum |
| Behavior | Cop navigates to target's last known position. Then executes a search pattern: checks nearby alleys, subway entrances, and building doorways within 50 m radius. |
| CCTV query | Every 10 s, cop queries CCTV network for target sighting. If target spotted, cop redirected and transitions back to Active Pursuit. |
| Likely escape routes | Cop prioritizes checking: (1) nearest subway entrance, (2) nearest alley, (3) direction of last known heading. |
| End condition | Target reacquired (back to Active Pursuit) OR 60 s elapsed (return to Patrol). |

#### Pursuit Resolution

| Outcome | Condition | Effect |
|---------|-----------|--------|
| **Target caught** | Cop within 2 m of target for 3 continuous seconds | Arrest sequence triggered. Target immobilized. Evidence event `authority.arrest` logged. |
| **Search timeout** | 60 s in Search Mode without reacquisition | Cop returns to beat patrol. Incident logged as `authority.pursuit.lost`. Target description retained in cop's long-term memory for future recognition. |
| **Target leaves slice** | Target crosses slice boundary during pursuit | Pursuit ends. `authority.pursuit.lost_boundary` event emitted. Adjacent slice's dispatch system receives alert with target description. |

### 3.3 Heat Generation During Pursuit

| Heat Channel | Rate | Duration |
|--------------|------|----------|
| Physical Heat | +0.1 / second | Active pursuit and search mode |
| Social Heat | +0.05 / second | Active pursuit only (visible to public) |
| Institutional Heat | +0.02 / second | From arrest event onward (paperwork, records) |

---

## 4. Dispatch Integration (Part 7 Event Bus)

Authority dispatch integrates with the Part 7 event bus as both a consumer and producer of events.

### 4.1 Events Consumed by Dispatch

| Event Topic | Payload | Dispatch Action |
|-------------|---------|-----------------|
| `evidence.cctv.detection` | `{ camera_id, target_description, confidence, position, timestamp }` | Evaluate against trigger matrix (Section 2). If threshold met, create dispatch order. |
| `heat.threshold.physical` | `{ grid_cell, heat_value, duration }` | If heat > 0.5 sustained 2 min, increase patrol density in area. |
| `heat.threshold.institutional` | `{ grid_cell, heat_value, duration }` | If heat > 0.7 sustained 5 min, activate cordon protocol. |
| `anomaly.detected` | `{ position, radius, type }` | Priority 0 dispatch. All available units redirect. Cordon at 50 m. |
| `authority.pursuit.update` | `{ unit_id, target_last_position, target_heading, confidence }` | Relay to other units. Update dispatch board. |

### 4.2 Events Produced by Dispatch

| Event Topic | Payload | When Emitted |
|-------------|---------|--------------|
| `authority.dispatch.unit` | `{ unit_id, target_location, priority, evidence_refs[], target_description }` | When dispatch assigns a unit to respond |
| `authority.unit.arrived` | `{ unit_id, location, timestamp }` | When dispatched unit reaches target location |
| `authority.incident.resolved` | `{ incident_id, resolution_type, unit_id, evidence_refs[], timestamp }` | When incident is closed (arrest, all-clear, stand-down) |
| `authority.incident.escalated` | `{ incident_id, escalation_reason, additional_units_requested, timestamp }` | When responding unit determines situation exceeds current response level |
| `authority.pursuit.initiated` | `{ unit_id, target_description, position, timestamp }` | When cop begins active pursuit |
| `authority.pursuit.lost` | `{ unit_id, target_last_position, search_duration, timestamp }` | When pursuit ends without arrest |
| `authority.arrest` | `{ unit_id, target_id, position, evidence_refs[], timestamp }` | When suspect is caught |
| `authority.cordon.placed` | `{ cordon_id, barrier_positions[], radius, reason, timestamp }` | When cordon barriers are deployed |
| `authority.cordon.removed` | `{ cordon_id, timestamp }` | When cordon is dismantled |

### 4.3 Dispatch Sequence Diagram

```
Evidence Event                    Dispatch System                   Patrol Cop
     |                                  |                               |
     |-- evidence.cctv.detection ------>|                               |
     |                                  |-- evaluate trigger matrix     |
     |                                  |-- select nearest unit         |
     |                                  |                               |
     |                                  |-- authority.dispatch.unit --->|
     |                                  |                               |-- navigate to location
     |                                  |                               |-- arrive
     |                                  |<-- authority.unit.arrived ----|
     |                                  |                               |-- assess situation
     |                                  |                               |
     |                            [if suspect found]                    |
     |                                  |                               |-- begin pursuit
     |                                  |<-- authority.pursuit.init ----|
     |                                  |                               |
     |                            [if suspect caught]                   |
     |                                  |<-- authority.arrest ----------|
     |                                  |-- authority.incident.resolved |
     |                                  |                               |-- return to patrol
```

---

## 5. Cordon Behavior

### 5.1 Cordon Activation

| Parameter | Value |
|-----------|-------|
| Trigger | Heat (institutional) > 0.7 **OR** anomaly with radius > 5 m |
| Placement logic | Barriers at nearest intersection crossings surrounding the incident zone. Minimum 4 barriers forming a perimeter. |
| Placement radius | Incident radius + 20 m buffer (minimum 30 m from incident center) |
| Deployment time | 2 s per barrier (crowd control cop navigates to position + deploy animation) |
| Maximum barriers | 12 per cordon (hardware budget for barrier physics objects) |

### 5.2 Cordon Effects

| Affected Entity | Behavior |
|-----------------|----------|
| Background pedestrians | Reroute around cordon. Pathfinding cost for cordoned cells set to infinity. NPCs approaching cordon slow, turn, and follow barrier line to nearest open route. |
| Hero pedestrians | Evaluate cordon. 95% comply (reroute). 5% attempt to observe from cordon edge (stop within 3 m, look toward incident). None breach in v1. |
| Background vehicles | Reroute via traffic system. Road segments within cordon marked as closed. |
| Hero vehicles | Reroute. If player vehicle, cordon acts as impassable barrier (vehicle collision with barrier triggers instant Heat spike). |
| Player (on foot) | Cordon is physically passable but triggers authority response: cop within LOS issues verbal warning, then pursuit if player crosses. |

### 5.3 Cordon Lifecycle

| Phase | Condition | Action |
|-------|-----------|--------|
| **Activation** | Trigger condition met | Dispatch emits `authority.cordon.placed`. Crowd control cops navigate to positions. |
| **Active** | Maintained while trigger condition persists | Barriers block navigation. Megaphone audio every 30 s. Cordon logged in evidence ledger. |
| **Wind-down** | Heat drops below 0.3 **OR** anomaly sealed **OR** manual stand-down | Crowd control cops begin barrier removal (2 s per barrier). |
| **Removal** | All barriers removed | Dispatch emits `authority.cordon.removed`. Navigation costs restored. Crowd control cops despawn or return to staging area. |

### 5.4 Evidence Logging

All cordon events are logged in the Part 7 evidence ledger:

| Ledger Entry | Fields |
|--------------|--------|
| Cordon placement | `{ cordon_id, position, radius, trigger_reason, timestamp, barrier_count }` |
| Cordon breach attempt | `{ cordon_id, agent_id, position, timestamp, response_action }` |
| Cordon removal | `{ cordon_id, duration, timestamp }` |

---

## 6. Authority Awareness Model

Patrol cops maintain an internal **awareness state** that modulates their perception sensitivity and response speed.

| Awareness Level | Trigger | Effect on Perception | Response Speed |
|-----------------|---------|---------------------|----------------|
| **Relaxed** (default) | No active alerts, Heat < 0.2 | Standard sensor parameters | Normal reaction time (1.0 s) |
| **Alert** | Heat 0.2 -- 0.5 in area, recent dispatch in neighborhood | Camera effective FOV +10 degrees (more head scanning), detection confidence threshold lowered to 0.5 | Faster reaction (0.6 s) |
| **High alert** | Active pursuit in area, Heat > 0.5, anomaly within 200 m | Camera update rate increased to 15 Hz, depth probe range +1 m, audio sensitivity +5 dB | Rapid reaction (0.3 s) |

Awareness level transitions are logged as internal state changes and affect the cop's animation state (walking pace, head movement frequency, hand position relative to equipment).

---

## Open Questions

1. Should player disguise/appearance changes affect cop identification confidence? If so, what is the recognition decay model?
2. Should cops be able to request CCTV footage review (time-shifted evidence), or only live feeds?
3. How does inter-slice pursuit handoff work when target crosses slice boundary during active pursuit?
4. Should the detective/analyst role (v2) be able to issue APBs that modify all patrol cops' target recognition lists?

---

*End of document.*
