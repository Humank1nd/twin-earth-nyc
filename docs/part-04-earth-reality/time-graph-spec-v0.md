# Time Graph Spec v0

**Document:** Part 04 — Earth Reality Layer
**Status:** v0 Draft
**Scope:** Timeline stack, canonical time, schedules data, world state node schema, starter nodes, commit/merge/replay rules
**Authority:** All systems that read or modify world temporal state must conform to this specification.

---

## 1. Timeline Stack

The simulation models time as a layered stack of temporal contexts, from broadest (seasonal) to narrowest (moment-to-moment). Each layer modulates the layers below it.

```
┌─────────────────────────────────────────────┐
│  SEASONAL CYCLE (outermost envelope)        │
│  summer / fall / winter / spring            │
│  ┌─────────────────────────────────────────┐│
│  │  DAILY CYCLE (diurnal pattern)          ││
│  │  7 named phases per 24-hour period      ││
│  │  ┌─────────────────────────────────────┐││
│  │  │  PRESENT MOMENT (active sim state)  │││
│  │  │  default active — drives all queries│││
│  │  └─────────────────────────────────────┘││
│  └─────────────────────────────────────────┘│
└─────────────────────────────────────────────┘
```

### 1.1 Seasonal Cycle

| Season | Months | Weather Envelope | Lighting Profile | Crowd Modifier |
|---|---|---|---|---|
| **Summer** | Jun - Aug | High temp (25-35 C), afternoon thunderstorms possible, high humidity | Long golden hour, harsh midday shadows, sunset ~20:30 | +20% tourist density; outdoor performers active |
| **Fall** | Sep - Nov | Mild to cool (8-22 C), occasional rain, lower humidity | Warm tones, sunset ~18:00 by Nov, shorter shadows | Baseline density; theater season ramp-up |
| **Winter** | Dec - Feb | Cold (−5 to 5 C), snow possible, low humidity | Blue-shifted ambient, sunset ~16:45, long shadows | +30% holiday crowds (Dec); reduced Jan-Feb |
| **Spring** | Mar - May | Cool to warm (8-22 C), frequent rain, variable | Neutral tones, sunset ~19:30 by May | Gradual increase; spring break surges |

### 1.2 Daily Cycle

| Phase | Hours (Local) | Character | Crowd Density | Traffic Intensity | Lighting State |
|---|---|---|---|---|---|
| **Pre-Dawn** | 02:00 - 07:00 | Quiet, maintenance, delivery trucks | 0.05 - 0.10 | 0.10 (delivery vehicles only) | Artificial only; billboards at reduced brightness |
| **Morning Rush** | 07:00 - 09:00 | Commuter surge, coffee carts active | 0.40 - 0.60 | 0.80 (peak inbound) | Sunrise transition; mixed natural + artificial |
| **Midday** | 10:00 - 14:00 | Tourist peak, lunch crowds, street performers | 0.60 - 0.85 | 0.50 (moderate) | Full daylight; billboards at daytime brightness |
| **Afternoon** | 14:00 - 17:00 | Sustained tourist flow, school releases | 0.50 - 0.70 | 0.60 (building) | Afternoon light; golden hour approaches |
| **Evening Rush** | 17:00 - 19:00 | Commuter outflow + early theater arrivals | 0.70 - 0.90 | 0.85 (peak outbound) | Sunset transition; billboards ramp to full |
| **Theater** | 19:00 - 22:00 | Theater crowds, dining, nightlife onset | 0.65 - 0.80 | 0.45 (taxis dominant) | Full artificial; billboard peak brightness |
| **Late Night** | 22:00 - 02:00 | Theater releases, bar crowds, gradual thinning | 0.30 - 0.55 | 0.25 (taxis, rideshare) | Full artificial; some signs dim after midnight |

Density values are normalized 0.0 - 1.0, where 1.0 = maximum comfortable capacity for the zone (~8,000 pedestrians in the Times Square bowtie).

---

## 2. Canonical Time

### 2.1 Time Representation

| Property | Specification |
|---|---|
| **Internal Clock** | UTC timestamp, int64 milliseconds since Unix epoch |
| **Local Offset** | EST (UTC-5) or EDT (UTC-4), applied for display and schedule lookups |
| **"Now"** | Simulation clock value; defaults to 1:1 with wall-clock real time |
| **Time Scale** | Adjustable: 1x (real time) through 60x (1 real second = 1 sim minute) |
| **Pause** | Sim clock can be paused; all temporal queries return the frozen timestamp |
| **Time Step** | Physics at fixed 60 Hz (16.67 ms sim-time per tick at 1x). At higher scales, physics sub-steps maintain stability. |

### 2.2 Time Query API

```
fn sim_now() -> Timestamp           // Current sim UTC millis
fn sim_local_now() -> LocalTime     // Current sim time in EST/EDT
fn sim_phase() -> DailyPhase        // Current named phase (e.g., "evening_rush")
fn sim_season() -> Season           // Current season enum
fn sim_scale() -> f64               // Current time multiplier
fn set_sim_scale(scale: f64)        // Set time multiplier [1.0 .. 60.0]
fn set_sim_time(ts: Timestamp)      // Jump to specific time (triggers re-evaluation of all schedules)
```

---

## 3. Schedules Data for Times Square

### 3.1 Pedestrian Flow

| Window | Day Type | Density Multiplier | Distribution Model |
|---|---|---|---|
| 11:00 - 14:00 | Weekday | 0.70 | Uniform with Gaussian peaks at 12:00 and 13:00 |
| 11:00 - 14:00 | Weekend | 0.85 | Uniform with broader plateau |
| 17:00 - 20:00 | Weekday | 0.80 | Sharp rise at 17:00, plateau, theater arrival spike at 19:00 |
| 17:00 - 20:00 | Fri/Sat | 0.95 | Peak of the week; sustained high density |
| 22:00 - 23:00 | Any | 0.55 | Theater release pulse (see 3.4) |

### 3.2 Traffic Intensity

| Window | Day Type | Intensity | Dominant Vehicle Types |
|---|---|---|---|
| 07:00 - 09:00 | Weekday | 0.80 | Private cars, buses, commercial delivery |
| 07:00 - 09:00 | Weekend | 0.30 | Taxis, rideshare |
| 16:00 - 19:00 | Weekday | 0.85 | Private cars outbound, buses, taxis |
| 16:00 - 19:00 | Weekend | 0.50 | Taxis, rideshare, tour buses |
| 22:00 - 02:00 | Fri/Sat | 0.35 | Taxis, rideshare (surge pricing active) |

### 3.3 Police / Authority Presence

| Window | Day Type | Presence Level | Notes |
|---|---|---|---|
| 06:00 - 18:00 | Any | Moderate (2-4 officers visible) | Fixed posts at TKTS, 42nd/7th, 42nd/Broadway |
| 18:00 - 02:00 | Weekday | Elevated (4-6 officers) | Evening patrol routes activated |
| 18:00 - 02:00 | Fri/Sat | High (6-10 officers + mobile unit) | Supplemental crowd management |
| 02:00 - 06:00 | Any | Low (1-2 officers, mobile patrol) | Vehicle patrol primarily |

### 3.4 Theater Release Schedule

Broadway theaters in the Times Square zone release audiences in a staggered pattern:

| Release Window | Theaters Active | Approximate Audience |
|---|---|---|
| 22:10 - 22:20 | Lyceum, Booth, Schoenfeld | ~2,500 |
| 22:20 - 22:30 | Marquis, Palace, Minskoff | ~4,800 |
| 22:30 - 22:45 | Gershwin, Majestic, Lunt-Fontanne | ~5,200 |

Total pulse: ~12,500 pedestrians entering the Times Square zone within a 35-minute window. This creates a detectable density wave moving outward from theater doors toward subway entrances and taxi queues.

### 3.5 Deterministic vs. Stochastic Events

| Category | Model | Seed Behavior |
|---|---|---|
| **Deterministic** | Signal timing cycles (fixed phase durations per DOT data), scheduled theater releases, sunrise/sunset times, seasonal transitions | No seed required; computed from sim clock |
| **Stochastic — Pedestrian arrivals** | Poisson process with time-varying rate parameter lambda(t) derived from schedule tables | Seeded PRNG; seed stored in world state node for replay |
| **Stochastic — Vehicle arrivals** | Poisson process per lane, rate from traffic intensity schedule | Seeded PRNG; independent seed per lane |
| **Stochastic — Weather variation** | Markov chain within seasonal band (e.g., winter: P(snow given cloudy) = 0.15) | Seeded PRNG; seed stored in world state node |
| **Stochastic — Individual NPC behavior** | Behavioral tree with weighted random branch selection | Per-NPC seed derived from entity ID + world seed |

---

## 4. World State Node Schema

Each node in the time graph represents a distinct world state over a time span. Nodes form a directed acyclic graph (DAG) with branching for anomaly events.

```json
{
  "node_id": "string — unique identifier (e.g., 'TSQ_BASELINE_DAY_001')",
  "time_span": {
    "start": "ISO 8601 UTC timestamp",
    "end": "ISO 8601 UTC timestamp"
  },
  "scope": "district | block | zone",
  "parent_nodes": ["node_id", "..."],
  "reason": "natural | seasonal | episodic | anomaly | branch",
  "delta_from_parent": {
    "wetness": "float 0.0-1.0 — surface wetness coefficient",
    "lighting_profile": "string — reference to lighting preset ID",
    "crowd_density_mult": "float — multiplier applied to base schedule density",
    "device_log_entries": ["array of device event log references"],
    "damage_states": {
      "entity_id": "damage_level enum: none | cosmetic | structural | destroyed"
    }
  },
  "stochastic_seeds": {
    "pedestrian": "u64",
    "vehicle": "u64",
    "weather": "u64",
    "npc_behavior": "u64"
  },
  "committed": "boolean — true if node is finalized and immutable",
  "replayable": "boolean — true if node can be re-entered from snapshot"
}
```

### 4.1 Field Definitions

| Field | Description |
|---|---|
| `node_id` | Globally unique string. Format: `{ZONE}_{DESCRIPTOR}_{SEQUENCE}` |
| `time_span` | The simulation time range this node covers. Nodes cannot overlap in time for the same scope. |
| `scope` | Spatial extent: `district` (all of Times Square), `block` (one city block), `zone` (sub-block area like a crosswalk cluster) |
| `parent_nodes` | Ordered list of predecessor nodes. Natural evolution has one parent. Branches have one parent. Merges have two+ parents. |
| `reason` | Why this node was created: `natural` (time passage), `seasonal` (season change), `episodic` (scheduled event like theater release), `anomaly` (game anomaly event), `branch` (player-triggered divergence) |
| `delta_from_parent` | Only changed fields are specified. Unspecified fields inherit from parent. |
| `stochastic_seeds` | Seeds for all random processes, enabling deterministic replay. |
| `committed` | Once true, the node and its delta are immutable. Active nodes have `committed: false`. |
| `replayable` | Whether the game can re-enter this node state. Requires a snapshot. |

---

## 5. Starter Nodes

### 5.1 TSQ_BASELINE_DAY

**Purpose:** Default starting world state. Clear midday conditions, moderate activity, all systems nominal.

```json
{
  "node_id": "TSQ_BASELINE_DAY_001",
  "time_span": {
    "start": "2025-06-15T12:00:00Z",
    "end": "2025-06-15T14:00:00Z"
  },
  "scope": "district",
  "parent_nodes": [],
  "reason": "natural",
  "delta_from_parent": {
    "wetness": 0.0,
    "lighting_profile": "summer_midday_clear",
    "crowd_density_mult": 0.6,
    "device_log_entries": [],
    "damage_states": {}
  },
  "stochastic_seeds": {
    "pedestrian": 1000001,
    "vehicle": 2000001,
    "weather": 3000001,
    "npc_behavior": 4000001
  },
  "committed": true,
  "replayable": true
}
```

**Conditions:** Dry surfaces. Sun at ~75 degree elevation (near summer solstice midday). Billboard brightness at daytime level. All traffic signals cycling normally. CCTV confidence at maximum. Crowd density at 0.6 (comfortable midday tourist flow). No police incidents active. No anomalies.

### 5.2 TSQ_RAINY_NIGHT

**Purpose:** Adverse conditions variant. Tests wet rendering, reduced visibility, lower crowd counts, degraded sensor performance.

```json
{
  "node_id": "TSQ_RAINY_NIGHT_001",
  "time_span": {
    "start": "2025-10-22T22:00:00Z",
    "end": "2025-10-23T00:00:00Z"
  },
  "scope": "district",
  "parent_nodes": ["TSQ_BASELINE_DAY_001"],
  "reason": "natural",
  "delta_from_parent": {
    "wetness": 0.85,
    "lighting_profile": "fall_night_rain",
    "crowd_density_mult": 0.3,
    "device_log_entries": [
      "CCTV_CONFIDENCE_DEGRADED: all units, factor 0.6",
      "WEATHER_ALERT: moderate rain, wind 15 km/h NW"
    ],
    "damage_states": {}
  },
  "stochastic_seeds": {
    "pedestrian": 1000002,
    "vehicle": 2000002,
    "weather": 3000002,
    "npc_behavior": 4000002
  },
  "committed": true,
  "replayable": true
}
```

**Conditions:** Wet surfaces (0.85 wetness). Fall nighttime, 10 PM local. Rain active with puddling on roads and sidewalks. Billboard reflections on wet pavement. Streetlights create glare halos. CCTV confidence reduced to 60% baseline. Crowd density at 0.3 (post-theater stragglers, reduced tourists). Taxi availability reduced. Umbrellas visible on NPCs. No anomalies.

### 5.3 TSQ_ANOMALY_EVENT

**Purpose:** Active anomaly scenario. Tests anomaly detection systems, crowd displacement AI, authority dispatch, Heat escalation.

```json
{
  "node_id": "TSQ_ANOMALY_EVENT_001",
  "time_span": {
    "start": "2025-06-15T14:30:00Z",
    "end": "2025-06-15T15:30:00Z"
  },
  "scope": "district",
  "parent_nodes": ["TSQ_BASELINE_DAY_001"],
  "reason": "anomaly",
  "delta_from_parent": {
    "wetness": 0.0,
    "lighting_profile": "summer_midday_clear_ALERT",
    "crowd_density_mult": 0.45,
    "device_log_entries": [
      "ANOMALY_DETECTED: zone 44th_broadway, type UNCLASSIFIED, heat_level 7.2",
      "CROWD_DISPLACEMENT: 44th block evacuating south toward 42nd",
      "AUTHORITY_DISPATCH: 3 units en route, ETA 4 min",
      "CCTV_ALERT: cameras 44-B1, 44-B2, 44-B3 tracking anomaly source",
      "TRAFFIC_REROUTE: 44th St closed Broadway to 7th Ave"
    ],
    "damage_states": {
      "bollard_44th_001": "cosmetic",
      "newsstand_44th_002": "structural"
    }
  },
  "stochastic_seeds": {
    "pedestrian": 1000003,
    "vehicle": 2000003,
    "weather": 3000003,
    "npc_behavior": 4000003
  },
  "committed": false,
  "replayable": true
}
```

**Conditions:** Anomaly active near 44th and Broadway. Heat level elevated to 7.2 (above the alert threshold of 5.0). Crowd displacing away from anomaly source, density reduced from 0.6 to 0.45 in broader zone but locally near-zero at 44th block. Authority dispatch active with 3 units. CCTV cameras locked on anomaly zone. 44th Street traffic rerouted. Minor damage to street furniture near anomaly epicenter. Lighting profile shifted to alert variant (emergency vehicle light contribution). Node is not yet committed (anomaly still evolving). Replayable from snapshot taken at node creation.

---

## 6. Commit Rules

### 6.1 Commit Triggers

A new world state node is created and the current node is committed when any of the following occurs:

| Trigger | Condition | New Node Reason |
|---|---|---|
| **Heat threshold crossing** | Heat level crosses a defined threshold (0 -> 3: monitoring, 3 -> 5: alert, 5 -> 8: critical, 8 -> 10: extreme) | `anomaly` |
| **Anomaly state change** | Anomaly appears, escalates, de-escalates, or resolves | `anomaly` or `natural` (if resolving) |
| **Player major event** | Player triggers a significant world-altering action (defined by game design as "branch-worthy") | `branch` |
| **Scheduled transition** | Daily phase change, seasonal change, or scheduled episodic event (theater release) | `natural`, `seasonal`, or `episodic` |
| **Elapsed time cap** | No other trigger for 2 sim-hours | `natural` (ensures periodic snapshots) |

### 6.2 Merge Rules

| Scenario | Merge Allowed | Policy |
|---|---|---|
| Natural evolution nodes | Yes | Sequential parent chain; linear history |
| Seasonal transitions | Yes | Old season node committed, new season node created with single parent |
| Episodic events (theater release) | Yes | Event node committed after pulse dissipates; returns to natural evolution |
| **Anomaly branches** | **No** | Anomaly nodes create a permanent divergence. The world state cannot "un-see" an anomaly. Once an anomaly branch exists, the timeline proceeds from the anomaly-affected state. |
| Player branches | No (by default) | Player-triggered divergences are permanent unless explicitly "corrected" by in-game narrative mechanisms. |

**Rationale for no-merge on anomalies:** The design philosophy of Twin Earth NYC treats anomaly events as irreversible disruptions to the simulation's reality. The world remembers. This creates narrative weight and consequences.

### 6.3 Replay Rules

| Node Type | Replayable | Snapshot Requirements |
|---|---|---|
| Baseline / Natural | Yes, fully | Seed values sufficient for full reconstruction from time_span.start |
| Seasonal | Yes, fully | Season enum + seeds sufficient |
| Episodic | Yes, fully | Schedule data + seeds sufficient |
| Anomaly | Yes, from snapshot | Full ECS state snapshot required at node creation time; seeds alone are insufficient because anomaly behavior may involve non-deterministic player input |
| Player Branch | Conditional | Replayable only if player inputs are recorded in the event log. If input recording was disabled, node is not replayable. |

**Snapshot Storage:** Anomaly node snapshots are stored as compressed ECS state dumps (all entity positions, components, and state machines). Estimated size: ~50 MB per snapshot for the Times Square district scope. Maximum retained snapshots: 100 (ring buffer, oldest evicted unless pinned).

---

## 7. Time Graph Visualization

For debugging and design tools, the time graph is rendered as a DAG:

```
TSQ_BASELINE_DAY_001  ─────────────────────────────┬──── TSQ_EVENING_RUSH_001 ─── ...
     (12:00-14:00)                                  │         (natural)
                                                    │
                                                    └──── TSQ_ANOMALY_EVENT_001 ─── TSQ_ANOMALY_RESOLVE_001
                                                              (anomaly)                 (anomaly)
                                                              [DIVERGENT BRANCH — NO MERGE BACK]

TSQ_RAINY_NIGHT_001  ─── TSQ_LATE_NIGHT_001 ─── ...
     (22:00-00:00)          (natural)
```

**Tool Requirements:** The time graph inspector must display:
- Node chain with parent relationships
- Color coding by reason (green = natural, blue = seasonal, yellow = episodic, red = anomaly, purple = branch)
- Click-to-inspect showing full node JSON
- "Jump to node" button that sets sim_time to node's time_span.start and loads snapshot if available

---

*End of Time Graph Spec v0.*
