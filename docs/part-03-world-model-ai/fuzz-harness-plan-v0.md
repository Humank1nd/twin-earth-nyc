# Fuzz Harness Plan v0 — Break the Sim

> **Series:** Twin Earth NYC — Part 3: World Model & AI
> **Document:** `fuzz-harness-plan-v0.md`
> **Status:** Draft v0
> **Last Updated:** 2026-01-27
> **Depends On:** `proposal-spec-v0.md`, `scenario-library-v0.md`, Part 1 (Truth Anchors), Part 2 (Ledger & Evidence)

---

## 1. Purpose

This document defines the fuzz testing harness for Twin Earth NYC. The goal is to systematically discover simulation failures before players do. The harness defines 10 "break the sim" interactions, a bot driver specification for automated exploration, a taxonomy of expected failure types, and a triage template for cataloging discovered issues.

The philosophy is simple: **if a player can try it, we must test it first.**

---

## 2. Ten "Break the Sim" Interactions

Each interaction describes a player behavior designed to stress a specific system boundary. For each, we define the action, the expected safe behavior, the systems under test, and the failure modes we are guarding against.

---

### Interaction 01: Sprint Into Crowds

| Field | Detail |
|-------|--------|
| **Action** | Player character sprints at full speed directly into a dense NPC crowd on the sidewalk. |
| **Expected Safe Behavior** | Crowd parts ahead of the player using anticipatory avoidance. NPCs within collision range are nudged aside with stagger/stumble animations. Player speed is reduced by crowd friction. No NPC phases through the player or another NPC. No NPC is launched or teleported. NPCs resume normal flow within 5 seconds of player passing. |
| **Systems Under Test** | Crowd AI (avoidance), physics (character-character collision), animation (stumble/reaction), pathfinding (reroute after disruption) |
| **Failure Modes** | NPC phasing through player. NPCs launched by collision impulse. Crowd deadlock behind player. NPC T-pose on stumble animation failure. Player clipping through NPC volume. |
| **Pass Criteria** | Zero phasing events. Zero launches (velocity > 5 m/s on NPC). Crowd recovery < 5s. All NPCs remain on navmesh. |

---

### Interaction 02: Jump Barriers

| Field | Detail |
|-------|--------|
| **Action** | Player attempts to jump over police barriers, construction fences, traffic bollards, and subway railings at various points in the slice. |
| **Expected Safe Behavior** | Low barriers (< 0.8m): player performs vault/climb animation and crosses. Medium barriers (0.8-1.5m): player is blocked, performs a "can't climb" feedback animation. High barriers (> 1.5m): player is fully blocked, no animation attempt. In no case does the player clip through the barrier geometry. Collision response is immediate and visually clean. |
| **Systems Under Test** | Collision (barrier surfaces), animation (vault/blocked), player controller (traversal rules), navmesh (barrier boundaries) |
| **Failure Modes** | Player clipping through barrier. Player floating above barrier during vault. Barrier collision missing (fall-through). Player stuck on barrier geometry. Vault animation playing on non-vaultable barrier. |
| **Pass Criteria** | Zero clipping events. Correct animation selection for barrier height. Player never occupies interior of barrier volume. Recovery to ground within 0.5s of vault completion. |

---

### Interaction 03: Drive Onto Sidewalks

| Field | Detail |
|-------|--------|
| **Action** | Player drives a vehicle (car, taxi) directly onto the sidewalk at multiple locations — where bollards exist, where bollards are absent, and at crosswalk transition points. |
| **Expected Safe Behavior** | Where bollards/barriers exist: vehicle collides with bollard, takes damage, stops or deflects. Bollard may deform but holds. Where no barriers: vehicle mounts curb (bump physics), enters pedestrian zone, NPCs scatter. Wanted level increases immediately. Police response triggers within 15 seconds. Vehicle speed is reduced on sidewalk surface. No NPCs are passed through — they are either hit (ragdoll) or dodge. |
| **Systems Under Test** | Vehicle physics (curb mounting, bollard collision), NPC AI (scatter behavior), wanted system (crime detection), police AI (response), collision (vehicle-pedestrian, vehicle-bollard) |
| **Failure Modes** | Vehicle phasing through bollard. Vehicle falling through sidewalk geometry. NPCs not reacting to oncoming vehicle. Wanted level not triggering. Vehicle stuck on curb geometry. NPC ragdoll launching into orbit. |
| **Pass Criteria** | Bollard collision stops or deflects vehicle. Curb mount produces correct bump response. All NPCs within 10m react (flee or hit). Wanted level triggers within 2s of sidewalk entry. No fall-through. No NPC launches > 10m. |

---

### Interaction 04: Lure Cops Into Anomaly Zone

| Field | Detail |
|-------|--------|
| **Action** | Player commits a crime near an active anomaly zone, then flees into the anomaly's effect radius. Pursuing police officers must decide how to handle the anomaly while maintaining pursuit. |
| **Expected Safe Behavior** | Police pursue player toward anomaly zone. Upon entering anomaly proximity (effect radius), officers exhibit hesitation behavior — slowed approach, radio callout, possible request for backup. If anomaly intensity is high, officers establish perimeter at safe distance rather than entering. If intensity is low, officers continue pursuit but with cautious behavior. In no case do officers ignore the anomaly entirely. In no case do officers become stuck or loop between pursue/avoid states. |
| **Systems Under Test** | Police AI (pursuit + anomaly awareness), behavior tree (priority conflict resolution), anomaly system (effect radius detection), pathfinding (route through/around anomaly) |
| **Failure Modes** | Officers ignoring anomaly entirely (immersion break). Officers stuck in decision loop (pursue/retreat oscillation). Officers pathing through anomaly center without reaction. Officers permanently abandoning pursuit due to anomaly (exploit). Police AI crash when encountering unprecedented pursuit + anomaly combination. |
| **Pass Criteria** | Officers acknowledge anomaly (behavior change visible). No decision loop oscillation (state changes < 3 per 5s). Officers either pursue cautiously or establish perimeter (valid outcome in both cases). Pursuit is not permanently broken by anomaly proximity. |

---

### Interaction 05: Force Portal at Intersection Peak

| Field | Detail |
|-------|--------|
| **Action** | Player triggers or forces an anomaly portal event at the busiest intersection during peak traffic flow (maximum vehicles + pedestrians in the intersection simultaneously). |
| **Expected Safe Behavior** | Portal spawns at intersection center. Vehicles in the intersection brake hard or swerve. Vehicles approaching yield or stop. Traffic signals go erratic within anomaly radius. Pedestrians in crosswalk flee. Evidence events burst at high rate. No vehicles phase through the portal. No pedestrians are deleted or teleported. Traffic eventually reroutes around the blocked intersection. System handles the simultaneous stress of portal VFX + traffic disruption + crowd panic + evidence generation without frame rate collapse. |
| **Systems Under Test** | Anomaly system (portal spawn), traffic AI (emergency response), crowd AI (panic), evidence system (burst generation), rendering (VFX + traffic + crowd simultaneously), physics (vehicle braking at speed) |
| **Failure Modes** | Vehicles driving through portal as if not present. Traffic deadlock (no rerouting). Evidence system overflow or dropped events. Frame rate collapse below minimum. Portal VFX occluding gameplay-critical information. Pedestrians walking into portal. Traffic signals stuck in erratic state after portal closes. |
| **Pass Criteria** | All vehicles within 20m react within 2s. Traffic reroutes within 60s. Evidence rate > 1/sec. FPS stays above scenario-adjusted floor. No entity passes through portal geometry. Traffic signals recover within 30s of portal close. |

---

### Interaction 06: Stack Objects on Crosswalk

| Field | Detail |
|-------|--------|
| **Action** | Player picks up or pushes moveable objects (trash cans, vendor cart props, barrier segments) and stacks them in the center of a crosswalk, creating an impassable obstacle for pedestrians. |
| **Expected Safe Behavior** | NPCs approaching the blocked crosswalk detect the obstacle and reroute — either to an adjacent crosswalk, around the obstacle if space permits, or wait and then reroute. No NPC walks through the stacked objects. No NPC becomes permanently stuck. If the blockage persists for > 60s, NPCs should use alternative paths exclusively. No crowd deadlock forms at the blocked crosswalk. Police may eventually investigate the obstruction. |
| **Systems Under Test** | NPC pathfinding (dynamic obstacle avoidance), navmesh (runtime update for placed objects), physics (object stacking stability), crowd flow (rerouting), object interaction (pickup/push) |
| **Failure Modes** | NPCs walking through stacked objects. NPCs deadlocking at the blocked crosswalk (can't find alternative). Stacked objects physics-exploding. Navmesh not updating for placed objects. Permanent crowd disruption after obstacle removed. NPC count building up endlessly at blockage. |
| **Pass Criteria** | Zero NPC-through-object phasing. Deadlock rate < 0.1% at blockage. NPCs find alternative within 10s. Object stack remains physically stable for 60s. Navmesh reflects obstruction within 2s of placement. Normal flow resumes within 10s of obstacle removal. |

---

### Interaction 07: Spam Door Interactions

| Field | Detail |
|-------|--------|
| **Action** | Player rapidly and repeatedly triggers door interaction prompts — open/close on shop doors, building entrances, vehicle doors — at maximum input rate (button mashing). |
| **Expected Safe Behavior** | Door interaction has a cooldown (minimum 0.5s between state changes). Rapid inputs beyond cooldown are queued (max queue depth: 1) or discarded. Door animation plays fully before state changes again. No door state corruption (door simultaneously open and closed). No interaction prompt permanently disappearing. No NPC trapped by rapidly toggling door. Sound effects respect cooldown (no audio stacking). |
| **Systems Under Test** | Interaction system (input handling, cooldown), animation (door open/close completion), state machine (door states), audio (cooldown on interaction sounds), NPC AI (reaction to door state changes) |
| **Failure Modes** | Door state corruption (visual open, collision closed, or vice versa). Interaction prompt disappearing permanently. Audio stacking (20 door sounds overlapping). NPC walking into closing door and getting stuck. Animation blending error from rapid state changes. Memory leak from queued interactions. |
| **Pass Criteria** | Door state always consistent (visual = collision = logical). Cooldown enforced (< 2 state changes per second). No audio overlap beyond 2 concurrent door sounds. No NPC entrapment. Interaction prompt always returns after cooldown. Zero state corruption over 100 rapid inputs. |

---

### Interaction 08: Block CCTV With Objects

| Field | Detail |
|-------|--------|
| **Action** | Player places objects (held props, parked vehicles, stacked items) directly in front of CCTV cameras positioned at intersections and on buildings, attempting to blind the surveillance system. |
| **Expected Safe Behavior** | CCTV system detects reduced coverage and logs it as an event. Coverage map updates to reflect blind spots. If coverage drops below threshold, system flags the area as "under-monitored." Evidence collection in the blocked area is reduced but not eliminated (other cameras, NPC witnesses still contribute). The game does not crash or produce errors from a CCTV ray hitting an unexpected obstacle. Blocking is a valid gameplay tactic with consequences (reduced surveillance), not an exploit that breaks systems. |
| **Systems Under Test** | CCTV system (occlusion detection), evidence system (coverage calculation), rendering (camera frustum vs. obstacle), gameplay (surveillance as mechanic) |
| **Failure Modes** | CCTV system crash when ray hits player-placed object. Coverage map not updating (blind spot not registered). Evidence system continuing to generate from blocked camera (false evidence). Game treating all CCTV as blocked when one is (cascading failure). Performance hit from CCTV rays hitting complex player-placed geometry. |
| **Pass Criteria** | Coverage map reflects actual occlusion within 1s. No system crash from any obstruction configuration. Evidence from blocked camera drops to zero. Unblocked cameras continue functioning normally. Performance impact < 1ms per blocked camera. |

---

### Interaction 09: Trigger Multiple Anomalies Simultaneously

| Field | Detail |
|-------|--------|
| **Action** | Player finds ways to trigger or be present during 3+ simultaneous anomaly events across the playable slice. This tests the anomaly system's ability to handle concurrent supernatural events. |
| **Expected Safe Behavior** | The anomaly system has a Heat mechanic that tracks total anomaly intensity. When Heat exceeds threshold, the system prioritizes — oldest anomalies stabilize or close, newest anomaly takes priority for VFX budget. Police and NPC responses are distributed across anomalies by proximity, not duplicated. Evidence system handles multi-source events without duplication or loss. VFX budget is shared (reduced per-anomaly effects when multiple are active). Frame rate remains above floor through budgeted VFX allocation. |
| **Systems Under Test** | Anomaly system (concurrent management, Heat mechanic), VFX (budget allocation), evidence system (multi-source), NPC AI (multi-threat response), performance (concurrent VFX + AI load) |
| **Failure Modes** | VFX budget exceeded causing frame collapse. Evidence events duplicated across anomalies. NPCs oscillating between anomaly responses. Heat system not triggering (unlimited anomalies). All anomalies rendering at full quality simultaneously. Police AI failing to distribute across threats. Memory spike from concurrent anomaly assets. |
| **Pass Criteria** | Heat system activates at threshold (max 3 concurrent full-intensity anomalies). VFX budget stays within allocation. Evidence events are correctly attributed (no duplication). NPCs respond to nearest anomaly. FPS stays above adjusted floor. Memory stays below ceiling. |

---

### Interaction 10: Rapid Zone Transitions

| Field | Detail |
|-------|--------|
| **Action** | Player moves rapidly back and forth across streaming zone boundaries — sprinting, driving, or using any fast-movement mechanic to repeatedly cross the line where one zone loads and another unloads. |
| **Expected Safe Behavior** | Streaming system handles rapid transitions gracefully. Zones load and unload based on player position with hysteresis (load distance > unload distance) to prevent thrashing. No visible pop-in of geometry, textures, or entities during normal-speed transitions. During rapid back-and-forth, system may briefly show lower LOD but never missing geometry. No T-pose NPCs from interrupted loading. No texture streaming failures (black/pink textures). Memory stays within ceiling despite rapid load/unload cycles. |
| **Systems Under Test** | Streaming (zone load/unload), LOD (transition smoothness), memory management (allocation/deallocation cycling), NPC system (spawn/despawn at boundaries), texture streaming (priority management) |
| **Failure Modes** | Visible pop-in of buildings or props. T-pose NPCs at zone boundary. Missing textures (pink/black surfaces). Memory leak from load/unload cycling. LOD stutter (rapidly switching between detail levels). Zone not loading in time (player in empty space). NPC duplication at boundary (spawned in both zones). |
| **Pass Criteria** | Zero missing geometry during normal-speed crossing. Zero T-pose occurrences. Zero pink/black textures. Memory delta < 100MB after 20 rapid crossings (no leak). LOD transitions smooth (no single-frame jumps). Hysteresis prevents zone thrashing (load/unload cycle < 1 per 2 seconds). |

---

## 3. Bot Driver Specification

### 3.1 Overview

The Bot Driver is an automated player agent that explores the simulation slice, performing a configurable mix of normal gameplay, boundary testing, and adversarial actions. Its purpose is to run continuously during testing, generating fuzz events and recording everything for later triage.

### 3.2 Behavior Distribution

| Behavior Class | Weight | Description |
|---------------|--------|-------------|
| **Normal** | 70% | Walk sidewalks, obey signals, enter shops, ride in vehicles, observe scenery. Mimics a typical player exploring Times Square. |
| **Boundary Testing** | 20% | Walk near edges of geometry, attempt to climb barriers, push against collision surfaces, stand on unusual surfaces, test interaction prompts at limits. |
| **Adversarial** | 10% | Sprint into crowds, drive on sidewalks, stack objects, spam interactions, trigger anomalies in high-traffic areas, block CCTV, rapid zone transitions. Directly executes the 10 break-the-sim interactions. |

### 3.3 Configuration

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://twin-earth-nyc.dev/schemas/bot-driver/v0.json",
  "title": "BotDriverConfig",
  "type": "object",
  "required": ["seed", "behavior_weights", "bounds", "duration_minutes"],
  "properties": {
    "seed": {
      "type": "integer",
      "description": "Deterministic random seed for reproducible runs."
    },
    "behavior_weights": {
      "type": "object",
      "properties": {
        "normal": {
          "type": "number",
          "minimum": 0,
          "maximum": 1,
          "default": 0.7
        },
        "boundary_testing": {
          "type": "number",
          "minimum": 0,
          "maximum": 1,
          "default": 0.2
        },
        "adversarial": {
          "type": "number",
          "minimum": 0,
          "maximum": 1,
          "default": 0.1
        }
      },
      "description": "Weights must sum to 1.0."
    },
    "bounds": {
      "type": "object",
      "properties": {
        "min_lat": { "type": "number" },
        "max_lat": { "type": "number" },
        "min_lon": { "type": "number" },
        "max_lon": { "type": "number" }
      },
      "description": "Geographic bounds of the playable slice. Bot stays within these."
    },
    "duration_minutes": {
      "type": "number",
      "minimum": 1,
      "maximum": 1440,
      "description": "How long the bot runs (sim-time minutes)."
    },
    "action_interval_seconds": {
      "type": "number",
      "minimum": 0.5,
      "maximum": 30,
      "default": 2.0,
      "description": "Average time between bot decisions."
    },
    "screenshot_interval_seconds": {
      "type": "number",
      "minimum": 1,
      "maximum": 60,
      "default": 10,
      "description": "Interval between automatic screenshots."
    },
    "event_log_path": {
      "type": "string",
      "description": "Path to write the event log."
    },
    "screenshot_path": {
      "type": "string",
      "description": "Directory for screenshot captures."
    },
    "adversarial_focus": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": [
          "sprint_crowd",
          "jump_barriers",
          "drive_sidewalk",
          "lure_cops_anomaly",
          "force_portal",
          "stack_crosswalk",
          "spam_doors",
          "block_cctv",
          "multi_anomaly",
          "rapid_zone_transition"
        ]
      },
      "description": "Which adversarial interactions to focus on. Empty = all."
    },
    "max_vehicle_time_seconds": {
      "type": "number",
      "default": 120,
      "description": "Maximum time bot spends in a vehicle before exiting."
    },
    "interaction_cooldown_seconds": {
      "type": "number",
      "default": 5,
      "description": "Minimum time between interaction attempts."
    }
  }
}
```

### 3.4 Bot Decision Loop

```
Every action_interval_seconds:
  1. Roll behavior class from weighted distribution
  2. Based on class, select action:

     NORMAL:
       - Choose from: walk_to_waypoint, wait_at_signal, enter_shop,
         hail_taxi, observe_billboard, sit_on_steps, use_phone,
         follow_crowd_flow, cross_at_crosswalk, ride_subway_entrance
       - Execute action with normal timing and animations

     BOUNDARY TESTING:
       - Choose from: walk_along_building_edge, attempt_climb_surface,
         push_against_wall, stand_on_planter, walk_on_road_edge,
         test_interaction_range, approach_barrier, walk_into_dead_end,
         stand_on_vehicle_roof, walk_under_scaffolding
       - Execute action and log any collision anomalies

     ADVERSARIAL:
       - Choose from adversarial_focus list (or all 10 interactions)
       - Execute the full interaction sequence
       - Log all events with elevated priority

  3. Record:
       - Bot position, rotation, velocity
       - Action taken and parameters
       - Any system events triggered (collision, AI reaction, etc.)
       - Screenshot if at interval
       - Any error/warning from game systems
```

### 3.5 Recording Format

The bot produces two output streams:

#### Event Log (JSON Lines)

One JSON object per line, one line per event.

```jsonl
{"t":0.000,"type":"bot_start","seed":12345,"config":"default_fuzz_v0"}
{"t":2.100,"type":"action","class":"normal","action":"walk_to_waypoint","target":[40.7580,-73.9855],"result":"started"}
{"t":4.300,"type":"position","pos":[40.7579,-73.9854,0.12],"rot":172.5,"vel":1.4}
{"t":10.000,"type":"screenshot","path":"screenshots/bot-001/frame-0010.png"}
{"t":12.500,"type":"action","class":"boundary","action":"push_against_wall","target":"wall:bldg-7av-45","result":"blocked_normal"}
{"t":15.800,"type":"action","class":"adversarial","action":"sprint_crowd","target":"crowd_cluster:7av-45-sw","result":"crowd_parted"}
{"t":15.850,"type":"system_event","source":"crowd_ai","event":"avoidance_triggered","entities":["npc:042","npc:043","npc:044"]}
{"t":16.200,"type":"metric","fps":42.1,"memory_mb":4120,"npc_count":312}
{"t":20.000,"type":"screenshot","path":"screenshots/bot-001/frame-0020.png"}
```

#### Screenshots

Captured at `screenshot_interval_seconds` intervals. Named sequentially with sim-time in filename.

```
screenshots/
  bot-001/
    frame-0010.png    (t=10s)
    frame-0020.png    (t=20s)
    frame-0030.png    (t=30s)
    ...
```

Screenshots include an overlay with: sim-time, bot position, current action, FPS, NPC count, memory usage.

---

## 4. Failure Taxonomy

All discovered failures are classified into five categories. Each category has specific subtypes with defined severity ranges.

### 4.1 Physics Faults

Failures in the physical simulation layer.

| Subtype | Code | Description | Default Severity | Example |
|---------|------|-------------|-----------------|---------|
| **Fall-Through** | PHY-001 | Entity passes through a surface that should be solid. | Critical | Player falls through sidewalk into void. |
| **Jitter** | PHY-002 | Entity vibrates rapidly in place due to competing collision responses. | Major | NPC vibrating between two collision surfaces. |
| **Penetration** | PHY-003 | Entity partially overlaps solid geometry without full fall-through. | Major | Player's arm clipping through wall. Vehicle bumper inside bollard. |
| **Launch** | PHY-004 | Entity is propelled at unrealistic velocity by physics solver. | Critical | NPC launched 50m into air by collision impulse. Vehicle catapulted by curb geometry. |
| **Stuck** | PHY-005 | Entity trapped in geometry with no valid movement direction. | Major | Player wedged between two objects, unable to move. |
| **Float** | PHY-006 | Entity hovering above a surface it should rest on. | Minor | Trash can floating 0.3m above sidewalk after being pushed. |
| **Settle Failure** | PHY-007 | Physics object never reaches rest state, continuously sliding or rocking. | Minor | Placed object slowly sliding downhill on flat surface. |

### 4.2 AI Faults

Failures in NPC behavior, pathfinding, and decision-making systems.

| Subtype | Code | Description | Default Severity | Example |
|---------|------|-------------|-----------------|---------|
| **Deadlock** | AI-001 | Two or more NPCs permanently blocking each other with no resolution. | Critical | Two NPCs face-to-face on narrow sidewalk, neither yields. |
| **Teleport** | AI-002 | NPC discontinuously jumps from one position to another. | Major | NPC snaps 5m to a navmesh point after being pushed off-mesh. |
| **Infinite Loop** | AI-003 | NPC repeats the same behavior pattern indefinitely. | Major | NPC walks to corner, turns around, walks back, repeat forever. |
| **Goal Thrashing** | AI-004 | NPC rapidly alternates between conflicting goals. | Major | Police officer alternating between "pursue suspect" and "avoid anomaly" every frame. |
| **Unresponsive** | AI-005 | NPC fails to react to a stimulus it should notice. | Major | Pedestrian NPC ignores car driving onto sidewalk directly at them. |
| **Wrong Reaction** | AI-006 | NPC reacts to a stimulus with incorrect behavior. | Minor | NPC applauds during a fire evacuation. |
| **Path Failure** | AI-007 | NPC cannot find a path to its destination and gives up or freezes. | Major | NPC targeting a shop entrance but can't reach it due to crowd. |
| **Group Coherence Failure** | AI-008 | NPCs that should move as a group scatter or lose formation. | Minor | Protest marchers splitting into random directions. |

### 4.3 Streaming Faults

Failures in level streaming, asset loading, and LOD management.

| Subtype | Code | Description | Default Severity | Example |
|---------|------|-------------|-----------------|---------|
| **Pop-In** | STR-001 | Asset appears suddenly within visible range rather than fading in. | Major | Building appears 20m in front of player while walking. |
| **Missing Texture** | STR-002 | Surface displays default/error texture (pink, black, checkerboard). | Major | Building facade shows pink checkerboard for 3 seconds during approach. |
| **LOD Stutter** | STR-003 | Visible frame hitch when LOD transition occurs. | Minor | Frame freeze for 100ms when building switches from mid to near LOD. |
| **T-Pose** | STR-004 | NPC displays in default T-pose instead of proper animation. | Major | NPC standing in T-pose at zone boundary for 2 seconds after load. |
| **Zone Gap** | STR-005 | Visible gap or seam between streaming zones. | Critical | Sky visible through gap between two building zones. |
| **Load Failure** | STR-006 | Zone fails to load entirely, leaving void or placeholder. | Critical | Player enters area with no loaded geometry. |
| **Unload Premature** | STR-007 | Zone unloads while still visible or occupied. | Critical | Building disappears while player is looking at it. |
| **Duplicate Spawn** | STR-008 | Entity spawned multiple times at zone boundary. | Minor | Two copies of same NPC at zone edge. |

### 4.4 Ledger Faults

Failures in the persistent game state, event recording, and evidence system.

| Subtype | Code | Description | Default Severity | Example |
|---------|------|-------------|-----------------|---------|
| **History Reset** | LDG-001 | Ledger entries disappear or revert to earlier state. | Critical | Evidence collected 5 minutes ago no longer appears in player inventory. |
| **Event Duplication** | LDG-002 | Same event recorded multiple times in the ledger. | Major | Anomaly event logged 3 times with identical timestamps. |
| **Orphaned Reference** | LDG-003 | Ledger entry references an entity that no longer exists. | Major | Evidence entry points to NPC ID that was despawned without cleanup. |
| **Write Failure** | LDG-004 | Ledger fails to record an event that should be persisted. | Critical | Player witnesses anomaly event but no evidence is generated. |
| **Sequence Error** | LDG-005 | Ledger entries appear out of chronological order. | Major | Event at T+60 recorded before event at T+30. |
| **Integrity Violation** | LDG-006 | Ledger hash chain is broken, indicating tampering or corruption. | Critical | Integrity check fails on ledger block. |
| **Attribution Error** | LDG-007 | Evidence attributed to wrong source or wrong location. | Major | Evidence from 7th Ave camera attributed to Broadway camera. |

### 4.5 Visual Faults

Failures in rendering, materials, lighting, and visual presentation.

| Subtype | Code | Description | Default Severity | Example |
|---------|------|-------------|-----------------|---------|
| **Scale Drift** | VIS-001 | Object renders at incorrect scale relative to environment. | Major | Fire hydrant appears 2x normal size after LOD transition. |
| **Z-Fighting** | VIS-002 | Two surfaces at same depth flicker between each other. | Minor | Sidewalk and manhole cover z-fighting at oblique angle. |
| **Billboard Artifact** | VIS-003 | Billboard/imposter sprite shows incorrect orientation or content. | Minor | Tree billboard facing wrong direction as player circles it. |
| **Shadow Error** | VIS-004 | Shadow does not match object geometry or light position. | Minor | Shadow of traffic light detached from pole by 1m. |
| **Reflection Error** | VIS-005 | Reflection shows incorrect or stale content. | Minor | Wet sidewalk reflects billboard that is behind the viewer. |
| **Material Seam** | VIS-006 | Visible seam where two materials or textures meet. | Minor | Line visible where two sidewalk textures tile. |
| **Flicker** | VIS-007 | Object or surface flickers between visible and invisible. | Major | Neon sign flickering in non-animated way (rendering error). |
| **Overdraw Blowout** | VIS-008 | Transparent/particle effects stack causing visual whiteout. | Major | Rain + anomaly shimmer + billboard glow combining to white screen. |

---

## 5. Triage Template

Every discovered issue is filed using the following template. This ensures consistent reporting and enables automated sorting, deduplication, and prioritization.

### 5.1 Triage Report Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://twin-earth-nyc.dev/schemas/triage-report/v0.json",
  "title": "TriageReport",
  "type": "object",
  "required": [
    "id",
    "repro_steps",
    "location",
    "sim_time",
    "expected_behavior",
    "actual_behavior",
    "category",
    "severity",
    "screenshot_path"
  ],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^FUZZ-\\d{6}$",
      "description": "Unique issue identifier. Format: FUZZ-NNNNNN."
    },
    "repro_steps": {
      "type": "array",
      "items": { "type": "string" },
      "minItems": 1,
      "description": "Ordered list of steps to reproduce the issue."
    },
    "location": {
      "type": "object",
      "required": ["lat", "lon", "zone"],
      "properties": {
        "lat": { "type": "number" },
        "lon": { "type": "number" },
        "alt": { "type": "number" },
        "zone": { "type": "string" },
        "nearest_landmark": { "type": "string" }
      },
      "description": "Where in the sim the issue occurred."
    },
    "sim_time": {
      "type": "number",
      "description": "Simulation time (seconds from session start) when the issue occurred."
    },
    "expected_behavior": {
      "type": "string",
      "description": "What should have happened according to design."
    },
    "actual_behavior": {
      "type": "string",
      "description": "What actually happened."
    },
    "category": {
      "type": "string",
      "enum": ["physics", "ai", "streaming", "ledger", "visual"],
      "description": "Primary failure category."
    },
    "subtype": {
      "type": "string",
      "description": "Specific fault subtype code (e.g., PHY-001, AI-003)."
    },
    "severity": {
      "type": "string",
      "enum": ["critical", "major", "minor", "cosmetic"],
      "description": "Issue severity level."
    },
    "screenshot_path": {
      "type": "string",
      "description": "Path to screenshot capturing the issue."
    },
    "video_clip_path": {
      "type": "string",
      "description": "Path to video clip if captured."
    },
    "event_log_excerpt": {
      "type": "string",
      "description": "Relevant excerpt from the bot event log."
    },
    "bot_session_id": {
      "type": "string",
      "description": "Which bot session discovered this issue."
    },
    "seed": {
      "type": "integer",
      "description": "Random seed for reproduction."
    },
    "frequency": {
      "type": "string",
      "enum": ["always", "often", "sometimes", "rare", "once"],
      "description": "How often this issue reproduces."
    },
    "related_issues": {
      "type": "array",
      "items": { "type": "string" },
      "description": "IDs of related or duplicate issues."
    },
    "discovered_at": {
      "type": "string",
      "format": "date-time",
      "description": "When the issue was discovered (wall-clock)."
    },
    "status": {
      "type": "string",
      "enum": ["new", "confirmed", "investigating", "fixed", "wont_fix", "duplicate"],
      "default": "new"
    },
    "assigned_to": {
      "type": "string",
      "description": "Engineer assigned to investigate."
    },
    "notes": {
      "type": "string",
      "description": "Additional context or observations."
    }
  }
}
```

### 5.2 Example Triage Report

```json
{
  "id": "FUZZ-000042",
  "repro_steps": [
    "Start at 7th Avenue and 45th Street, west sidewalk.",
    "Wait for crowd density to reach ~70% (approx 30 seconds after scenario start).",
    "Sprint directly east into the densest cluster of pedestrian NPCs.",
    "Maintain sprint for 3 seconds through the crowd.",
    "Observe NPC at position approximately 3m into the crowd."
  ],
  "location": {
    "lat": 40.75801,
    "lon": -73.98542,
    "alt": 0.15,
    "zone": "zone:ts-core-01",
    "nearest_landmark": "TKTS Steps"
  },
  "sim_time": 34.5,
  "expected_behavior": "All NPCs in the sprint path should perform avoidance (sidestep or stumble) animations and be nudged aside by collision. No NPC should phase through the player character.",
  "actual_behavior": "NPC entity npc:ped-0187 was pushed by player collision but responded with a velocity spike of 12.4 m/s, launching the NPC approximately 8m into the air before landing on the road surface. The NPC then resumed walking normally from the landing position.",
  "category": "physics",
  "subtype": "PHY-004",
  "severity": "critical",
  "screenshot_path": "screenshots/bot-001/fuzz-000042-launch.png",
  "video_clip_path": "captures/bot-001/fuzz-000042-clip.mp4",
  "event_log_excerpt": "{\"t\":34.5,\"type\":\"system_event\",\"source\":\"physics\",\"event\":\"velocity_spike\",\"entity\":\"npc:ped-0187\",\"velocity\":12.4,\"direction\":[0.2,0.95,0.1]}",
  "bot_session_id": "bot-session-20260127-001",
  "seed": 12345,
  "frequency": "sometimes",
  "related_issues": [],
  "discovered_at": "2026-01-27T15:42:00Z",
  "status": "new",
  "assigned_to": "",
  "notes": "Appears to happen when player sprint collision hits NPC at exact frame of NPC direction change. Likely a collision impulse calculation error when NPC velocity and player velocity are near-perpendicular."
}
```

### 5.3 Severity Definitions

| Severity | Definition | Response SLA | Examples |
|----------|-----------|-------------|---------|
| **Critical** | Simulation integrity is compromised. Game state may be corrupted. Player may be stuck or experience crash-level disruption. | Fix before next milestone. Block release. | Fall-through, NPC launch, ledger corruption, zone load failure, history reset. |
| **Major** | Gameplay experience is significantly degraded. Immersion broken. Systems not functioning as designed. | Fix before release. May defer within milestone. | Pop-in, T-pose, NPC deadlock, missing textures, path failure, event duplication, penetration. |
| **Minor** | Noticeable but not disruptive. Does not affect gameplay outcomes. | Fix if time permits. May ship with known minor issues. | Z-fighting, shadow offset, material seam, LOD stutter, billboard orientation, slight scale drift. |
| **Cosmetic** | Only visible under specific conditions or close inspection. No gameplay impact. | Backlog. Fix in polish pass. | Subtle reflection error, minor texture tiling, animation blend imperfection. |

---

## 6. Fuzz Harness Execution Schedule

### 6.1 Continuous Integration

| Run Type | Frequency | Bot Duration | Focus | Output |
|----------|-----------|-------------|-------|--------|
| **Nightly Smoke** | Every night | 30 min sim-time | 100% normal behavior | Baseline regression. Catch new breaks. |
| **Daily Fuzz** | Every day | 4 hours sim-time | 70/20/10 default mix | Full coverage. Primary bug discovery. |
| **Weekly Adversarial** | Every Saturday | 8 hours sim-time | 30/30/40 (adversarial heavy) | Deep boundary testing. Edge case discovery. |
| **Pre-Milestone Soak** | Before each milestone | 24 hours sim-time | 70/20/10 default mix | Stability verification. No new criticals. |

### 6.2 Pass Criteria by Run Type

| Run Type | Max Critical Issues | Max Major Issues | Max Regressions |
|----------|-------------------|-----------------|-----------------|
| Nightly Smoke | 0 new | 0 new | 0 (any regression = alert) |
| Daily Fuzz | 0 new critical blocks release | Report all | Track trend |
| Weekly Adversarial | Report all, triage Monday | Report all | Compare to prior week |
| Pre-Milestone Soak | 0 (zero tolerance) | < 5 unresolved | 0 regressions from prior soak |

---

## 7. Replay System

Every bot session is fully replayable. The replay system uses the event log and seed to reproduce the exact sequence of bot actions and verify that the same issues occur (or have been fixed).

### 7.1 Replay Requirements

- Given the same `seed` and `config`, the bot must make identical decisions.
- Given the same world state snapshot and event log, the simulation must produce the same physics/AI outcomes within tolerance (floating-point determinism is not required; behavioral determinism is).
- Replay can be run at 1x, 2x, 4x, or 10x speed.
- Replay can jump to any sim-time within the session.
- Issues discovered during replay can be filed using the same triage template, referencing the original session ID.

### 7.2 Replay Command Interface

```
fuzz-replay --session <session_id>          # Replay full session at 1x
fuzz-replay --session <session_id> --speed 4 # Replay at 4x speed
fuzz-replay --session <session_id> --seek 34.5 # Jump to sim-time 34.5s
fuzz-replay --session <session_id> --issue FUZZ-000042 # Jump to issue time
fuzz-replay --session <session_id> --verify  # Re-run and compare to original
```

---

*End of document. Next: `canonicalization-checklist.md`*
