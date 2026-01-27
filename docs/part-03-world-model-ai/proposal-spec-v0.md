# Proposal Spec v0 — World Model Output Contract

> **Series:** Twin Earth NYC — Part 3: World Model & AI
> **Document:** `proposal-spec-v0.md`
> **Status:** Draft v0
> **Last Updated:** 2026-01-27
> **Depends On:** Part 1 (Truth Anchors), Part 2 (Ledger & Evidence)

---

## 1. Role of the World Model

### 1.1 Governing Principle

> **"The world model generates proposals. The Truth Engine validates reality."**

The world model is a creative, probabilistic system that explores the possibility space of Twin Earth NYC. It produces *suggestions* — never *facts*. Every output is a proposal that must survive validation against the canonical truth layer before it can affect the persistent game state.

This separation is absolute. The world model operates in a sandbox. The Truth Engine operates on the ledger. They communicate exclusively through the Proposal Protocol defined in this document.

### 1.2 Tasks the World Model MAY Perform

The world model is authorized to generate speculative, non-binding outputs in the following domains:

| # | Task | Description | Output Type |
|---|------|-------------|-------------|
| 1 | **Previs Scene Blocking** | Compose rough camera angles, character positions, and event staging for cutscenes or triggered moments. | Camera path + entity positions (draft) |
| 2 | **Layout Suggestions for Prop Placement** | Suggest where street furniture, vendor carts, trash cans, or seasonal decorations could plausibly appear. | Position + rotation + prop ID (suggestive) |
| 3 | **Traffic Flow Hypotheses** | Model alternative traffic patterns, signal timings, and congestion scenarios for intersection management. | Traffic graph + timing table (draft) |
| 4 | **Crowd Density Prototypes** | Generate crowd distribution maps, pedestrian flow corridors, and gathering-point predictions. | Density heatmap + flow vectors (draft) |
| 5 | **Weather Effect Previews** | Produce visual drafts of rain, fog, snow, heat haze, and their impact on surfaces, reflections, and visibility. | Shader parameter set + particle config (draft) |
| 6 | **Lighting Mood Exploration** | Explore time-of-day lighting, neon interactions, emergency lighting states, and anomaly glow palettes. | Light rig preset + color palette (suggestive) |
| 7 | **Signage Variant Generation** | Create alternative billboard content, storefront signs, and informational displays within brand/lore constraints. | Texture atlas + placement metadata (suggestive) |
| 8 | **NPC Behavior Drafts** | Sketch behavioral routines, reaction trees, and dialogue stubs for non-player characters. | Behavior tree fragment + dialogue lines (draft) |
| 9 | **Anomaly Visual Concepts** | Propose visual treatments for anomaly events — shimmer effects, portal aesthetics, reality-tear patterns. | VFX parameter set + reference images (suggestive) |
| 10 | **Sound Design Sketches** | Draft ambient soundscapes, event stingers, crowd murmur layers, and anomaly audio signatures. | Audio graph + sample references (draft) |

All outputs from the above tasks carry the classification **"suggestive"** and must not be treated as canonical until promoted through the canonicalization pipeline (see `canonicalization-checklist.md`).

### 1.3 Tasks the World Model May NOT Perform

The following operations are **strictly forbidden** for the world model. These belong exclusively to the Truth Engine, human reviewers, or the canonical asset pipeline.

| # | Forbidden Task | Reason | Owner |
|---|---------------|--------|-------|
| 1 | **Author Canonical Geometry** | Geometry that players collide with must be hand-verified or scan-derived. Generative meshes are not collision-safe by default. | Asset Pipeline |
| 2 | **Define Collision Surfaces** | Collision truth determines gameplay physics. A wrong surface breaks traversal, driving, and NPC pathfinding. | Truth Engine |
| 3 | **Write Persistent Ledger Entries Without Validation** | The ledger is append-only and immutable once committed. Unvalidated writes corrupt game history. | Ledger Service |
| 4 | **Set Anchor Coordinates** | Anchor positions are derived from surveyed real-world data. Moving them invalidates the entire truth layer. | Truth Engine |
| 5 | **Override Physics Constants** | Gravity, friction, and restitution values are calibrated to match real-world NYC behavior. | Physics System |
| 6 | **Establish Entity Identity** | Entity IDs are assigned by the ledger and are permanent. The world model cannot create, merge, or destroy identities. | Ledger Service |
| 7 | **Modify Street Layout** | Street geometry is georeferenced truth data. Changing it breaks navigation, traffic, and spatial anchoring. | Truth Engine |
| 8 | **Change Landmark Silhouettes** | Landmark outlines are locked to photogrammetry references. Altering them breaks visual recognition and scale anchoring. | Asset Pipeline |
| 9 | **Alter Scale Anchors** | Scale references (door heights, vehicle dimensions, human proportions) are truth constants used for validation. | Truth Engine |
| 10 | **Commit to Mission Outcomes** | Narrative outcomes are determined by player action plus validated game logic, never by generative prediction. | Game Logic Layer |

---

## 2. Proposal Format — Standard Output Package

Every world model output is wrapped in a **Proposal** object. This is the sole interface between the world model and the rest of the system. No output may bypass this format.

### 2.1 Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `proposal_id` | `string` (UUID v4) | Yes | Unique identifier for this proposal. |
| `timestamp` | `string` (ISO 8601) | Yes | When the proposal was generated. |
| `model_version` | `string` (semver) | Yes | Version of the world model that produced this proposal. |
| `intent` | `string` | Yes | Plain-language description of what the proposal is trying to achieve. Must be human-readable and specific enough to evaluate. |
| `domain` | `string` (enum) | Yes | Which system domain this proposal targets. One of: `scene_blocking`, `prop_placement`, `traffic_flow`, `crowd_density`, `weather_effects`, `lighting_mood`, `signage_variant`, `npc_behavior`, `anomaly_visual`, `sound_design`. |
| `constraints_used` | `string[]` | Yes | List of truth constraints the model consulted when generating this proposal. References constraint IDs from the truth layer. |
| `assets_affected` | `string[]` (entity IDs) | Yes | List of entity IDs that would be modified, created (pending), or removed if this proposal is accepted. Empty array if no existing entities are affected. |
| `confidence` | `number` (0.0–1.0) | Yes | Model's self-assessed confidence that this proposal is plausible, constraint-compliant, and useful. Values below 0.5 are flagged for human review regardless of other metrics. |
| `rollback_path` | `string` | Yes | Description of how to undo this proposal's effects if it is accepted and later found to be problematic. Must reference specific state snapshots or inverse operations. |
| `audit_note` | `string` | Yes | Explanation of *why* this proposal is plausible. Must reference real-world knowledge, constraint data, or prior accepted proposals that support this output. |
| `payload` | `object` | Yes | Domain-specific data. Schema varies by domain (see Section 2.3). |
| `sandbox_id` | `string` | No | If this proposal was generated within a specific sandbox session, its ID. |
| `parent_proposal_id` | `string` | No | If this proposal refines or replaces a previous one, the parent's ID. |
| `tags` | `string[]` | No | Free-form tags for filtering and search. |
| `ttl_seconds` | `integer` | No | Time-to-live. Proposal expires and cannot be accepted after this duration. Default: 3600 (1 hour). |

### 2.2 Full JSON Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://twin-earth-nyc.dev/schemas/proposal/v0.json",
  "title": "WorldModelProposal",
  "description": "Standard output package for all world model proposals in Twin Earth NYC.",
  "type": "object",
  "required": [
    "proposal_id",
    "timestamp",
    "model_version",
    "intent",
    "domain",
    "constraints_used",
    "assets_affected",
    "confidence",
    "rollback_path",
    "audit_note",
    "payload"
  ],
  "properties": {
    "proposal_id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique identifier for this proposal (UUID v4)."
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp of proposal generation."
    },
    "model_version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$",
      "description": "Semantic version of the world model that generated this proposal."
    },
    "intent": {
      "type": "string",
      "minLength": 10,
      "maxLength": 500,
      "description": "Human-readable description of what the proposal aims to achieve."
    },
    "domain": {
      "type": "string",
      "enum": [
        "scene_blocking",
        "prop_placement",
        "traffic_flow",
        "crowd_density",
        "weather_effects",
        "lighting_mood",
        "signage_variant",
        "npc_behavior",
        "anomaly_visual",
        "sound_design"
      ],
      "description": "System domain this proposal targets."
    },
    "constraints_used": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 1
      },
      "minItems": 1,
      "description": "Truth constraint IDs consulted during generation."
    },
    "assets_affected": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Entity IDs that would be modified if accepted. Empty array if no existing entities change."
    },
    "confidence": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0,
      "description": "Self-assessed plausibility confidence. Below 0.5 triggers mandatory human review."
    },
    "rollback_path": {
      "type": "string",
      "minLength": 5,
      "description": "How to undo this proposal if accepted and later reverted."
    },
    "audit_note": {
      "type": "string",
      "minLength": 10,
      "description": "Justification for why this proposal is plausible."
    },
    "payload": {
      "type": "object",
      "description": "Domain-specific proposal data. Schema varies by domain.",
      "properties": {
        "transforms": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "entity_id": { "type": "string" },
              "position": {
                "type": "object",
                "properties": {
                  "x": { "type": "number" },
                  "y": { "type": "number" },
                  "z": { "type": "number" }
                },
                "required": ["x", "y", "z"]
              },
              "rotation": {
                "type": "object",
                "properties": {
                  "yaw": { "type": "number" },
                  "pitch": { "type": "number" },
                  "roll": { "type": "number" }
                }
              },
              "scale": {
                "type": "object",
                "properties": {
                  "x": { "type": "number" },
                  "y": { "type": "number" },
                  "z": { "type": "number" }
                }
              }
            }
          },
          "description": "Transform changes for affected entities."
        },
        "parameters": {
          "type": "object",
          "additionalProperties": true,
          "description": "Domain-specific parameter overrides."
        },
        "references": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "uri"
          },
          "description": "URIs to supporting assets (textures, audio, previs renders)."
        },
        "metadata": {
          "type": "object",
          "additionalProperties": true,
          "description": "Additional context for reviewers."
        }
      }
    },
    "sandbox_id": {
      "type": "string",
      "description": "Sandbox session that produced this proposal, if applicable."
    },
    "parent_proposal_id": {
      "type": "string",
      "format": "uuid",
      "description": "ID of the proposal this one refines or replaces."
    },
    "tags": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Free-form tags for filtering."
    },
    "ttl_seconds": {
      "type": "integer",
      "minimum": 60,
      "maximum": 86400,
      "default": 3600,
      "description": "Time-to-live in seconds. Proposal expires after this duration."
    }
  },
  "additionalProperties": false
}
```

### 2.3 Example Proposal

```json
{
  "proposal_id": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
  "timestamp": "2026-01-27T14:30:00Z",
  "model_version": "0.3.1",
  "intent": "Place a hot dog vendor cart on the west sidewalk of 7th Avenue between 45th and 46th Streets, positioned near the existing newsstand to create a realistic vendor cluster.",
  "domain": "prop_placement",
  "constraints_used": [
    "constraint:sidewalk-clearance-min-1.5m",
    "constraint:vendor-spacing-min-3m",
    "constraint:fire-hydrant-clearance-5m",
    "constraint:pedestrian-flow-corridor-preserved"
  ],
  "assets_affected": [
    "entity:newsstand-7av-45st",
    "entity:sidewalk-segment-7av-45-46-west"
  ],
  "confidence": 0.82,
  "rollback_path": "Remove entity at proposed position. No existing entities are modified, only a new placement is suggested. Rollback = delete the placed prop and restore sidewalk walkability graph to snapshot snap:7av-45-46-20260127.",
  "audit_note": "Hot dog vendors are commonly observed at this location in real-world Times Square. The proposed position maintains 4.2m clearance from the nearest fire hydrant (exceeds 5ft NYC code minimum) and preserves a 2.1m pedestrian corridor (exceeds 1.5m minimum). The vendor cluster pattern matches observed real-world groupings of food vendors near high-traffic newsstand locations.",
  "payload": {
    "transforms": [
      {
        "entity_id": "pending:hotdog-cart-7av-45st-001",
        "position": { "x": -73.98542, "y": 40.75801, "z": 0.15 },
        "rotation": { "yaw": 172.5, "pitch": 0, "roll": 0 },
        "scale": { "x": 1.0, "y": 1.0, "z": 1.0 }
      }
    ],
    "parameters": {
      "prop_template": "vendor_cart_hotdog_v2",
      "npc_operator": true,
      "operating_hours": { "start": "10:00", "end": "22:00" },
      "smoke_vfx": true
    },
    "references": [
      "asset://props/vendor_carts/hotdog_v2/preview.png",
      "asset://reference_photos/7av_45st_vendors_2025.jpg"
    ],
    "metadata": {
      "real_world_reference": "Google Street View capture, July 2025",
      "pedestrian_flow_impact": "negligible — diverts <3% of sidewalk traffic"
    }
  },
  "sandbox_id": "sandbox:prop-exploration-session-042",
  "parent_proposal_id": null,
  "tags": ["props", "vendors", "7th-avenue", "street-life"],
  "ttl_seconds": 7200
}
```

---

## 3. Interactive Loop — Propose, Validate, Commit

### 3.1 The Five-Step Loop

Every world model output follows a strict five-step lifecycle. No step may be skipped.

```
  +----------+     +-----------+     +---------+     +--------+     +--------+
  | PROPOSE  | --> | SIMULATE  | --> | MEASURE | --> | DECIDE | --> | COMMIT |
  |          |     | (sandbox) |     | (metrics)|    |(accept/|     |(promote|
  | World    |     | Run in    |     | Compare  |    | reject)|     | to     |
  | Model    |     | isolated  |     | against  |    | Check  |     |canonical|
  | generates|     | env       |     | criteria |    |thresholds    | if     |
  | proposal |     |           |     |          |    |        |     |accepted|
  +----------+     +-----------+     +---------+     +--------+     +--------+
       |                                                  |              |
       |                                                  |  REJECTED    |
       +<-------------------------------------------------+              |
                    (feedback returned to model)                         |
                                                                         v
                                                                   [CANONICAL
                                                                    STATE]
```

#### Step 1: PROPOSE

The world model generates a `WorldModelProposal` object (Section 2). The proposal is assigned a unique ID and placed in the **proposal queue**. At this stage, the proposal has zero authority — it is purely speculative.

**Triggers:**
- Scheduled exploration (e.g., "explore prop placements for block 45-46")
- Reactive generation (e.g., "rainstorm scenario activated, generate crowd shelter behavior")
- Human request (e.g., designer asks "show me vendor cart options for 7th Ave")

**Output:** A valid `WorldModelProposal` JSON object.

#### Step 2: SIMULATE

The proposal is loaded into an **isolated sandbox environment**. The sandbox is a fork of the current canonical state with the proposal's changes applied.

**Sandbox Rules:**
- Sandbox has read access to canonical state, write access only to its own fork.
- Sandbox cannot affect the live game or any other sandbox.
- Sandbox lifetime is bounded by the proposal's `ttl_seconds`.
- Multiple proposals may be simulated in parallel in separate sandboxes.

**Actions:**
- Apply the proposal's transforms and parameters to the sandbox world.
- Run physics simulation for a configurable duration (default: 60 seconds sim-time).
- Execute NPC AI, traffic, crowd, and environmental systems.
- Record all events, collisions, pathfinding results, and visual output.

**Output:** Sandbox session log + captured metrics + optional video frames.

#### Step 3: MEASURE

The sandbox results are evaluated against the **acceptance metrics** (Section 3.2). Each metric produces a score. Some metrics are hard constraints (pass/fail); others are soft metrics (scored 0.0–1.0).

**Measurement Process:**
1. Extract metric values from sandbox session log.
2. Compare each hard constraint against its pass/fail threshold.
3. Score each soft metric on the 0.0–1.0 plausibility scale.
4. Compute composite plausibility score (weighted average of soft metrics).
5. Generate a **Measurement Report** (see Section 3.3).

**Output:** `MeasurementReport` JSON object.

#### Step 4: DECIDE (Accept / Reject)

The measurement report is evaluated against the acceptance criteria. The decision is binary: **ACCEPT** or **REJECT**.

**Acceptance Criteria — All Must Pass:**

| Criterion | Type | Threshold | Description |
|-----------|------|-----------|-------------|
| Hard constraint compliance | Pass/Fail | All pass | Every hard constraint must be satisfied. A single failure = rejection. |
| Composite plausibility score | Soft | >= 0.7 | Weighted average of all soft plausibility metrics. |
| Anchor drift | Hard | <= tolerance per anchor class | No truth anchor may drift beyond its defined tolerance (see Part 1). |
| Collision truth violations | Hard | 0 | No new collision geometry errors introduced. |
| Entity identity integrity | Hard | Pass | No entity IDs created, destroyed, or merged outside ledger protocol. |
| Ledger consistency | Hard | Pass | No orphaned references, no history corruption. |

**Decision Authority:**

| Proposal Target Layer | Auto-Commit Allowed? | Human Approval Required? |
|----------------------|---------------------|-------------------------|
| Illusion layer — sandbox zones (visual-only, non-persistent) | Yes, if all criteria pass | No |
| Illusion layer — persistent visuals (textures, lighting presets) | Yes, with elevated threshold (>= 0.85) | Recommended |
| Truth layer — any change (collision, anchors, ledger, layout) | No — never auto-commit | **Always required** |
| Mixed — proposal affects both layers | No | **Always required** |

**On Rejection:**
- The proposal is returned to the world model with the measurement report attached.
- The world model may revise and re-submit (incrementing a `revision` counter) up to a configurable retry limit (default: 3).
- After max retries, the proposal is archived with status `rejected_final` and flagged for human review if confidence was > 0.6.

#### Step 5: COMMIT

Accepted proposals are promoted to canonical state.

**Commit Process:**
1. Acquire write lock on affected entities/regions.
2. Apply proposal transforms and parameters to canonical state.
3. Write ledger entry documenting the change (source: proposal ID, approver: system or human ID).
4. Release write lock.
5. Broadcast state update to all connected clients and subsystems.
6. Archive the proposal with status `committed` and link to the ledger entry.

**Commit Atomicity:** All changes in a proposal are applied as a single transaction. If any part fails, the entire commit is rolled back.

**Post-Commit Monitoring:**
- For 300 seconds after commit, the affected region is in **observation mode**.
- If any hard constraint violation is detected during observation, an automatic rollback is triggered using the proposal's `rollback_path`.
- Observation results are logged and fed back to the world model for learning.

### 3.2 Acceptance Criteria — Detailed Definitions

#### Hard Constraints (Binary Pass/Fail)

| ID | Constraint | Validation Method |
|----|-----------|-------------------|
| HC-01 | **Anchor integrity** — No truth anchor moves beyond tolerance. | Compare anchor positions before/after simulation. Tolerance: Tier 1 = 0.05m, Tier 2 = 0.25m, Tier 3 = 1.0m. |
| HC-02 | **Collision truth** — No new walk-through or drive-through errors. | Run automated walk/drive test paths through affected area. Zero penetrations allowed. |
| HC-03 | **Entity identity** — No unauthorized entity creation/destruction. | Diff entity registry before/after. Only `pending:` prefixed entities from the proposal are allowed as new. |
| HC-04 | **Ledger consistency** — No orphaned refs, no history gaps. | Run ledger integrity check. All references must resolve. Append-only property maintained. |
| HC-05 | **Scale fidelity** — Proposed objects match real-world scale. | Check against 3+ scale anchors (door height: 2.1m, avg human: 1.75m, sedan length: 4.5m). Tolerance: +/- 5%. |
| HC-06 | **Street layout preservation** — No road/sidewalk geometry changes. | Hash comparison of street mesh before/after. Must be identical. |

#### Soft Metrics (Scored 0.0–1.0)

| ID | Metric | Weight | Scoring Method |
|----|--------|--------|---------------|
| SM-01 | **Visual plausibility** | 0.20 | Automated perceptual comparison against reference photos. SSIM-based. |
| SM-02 | **Pedestrian flow quality** | 0.15 | Deadlock rate, average travel time, path completion rate. |
| SM-03 | **Traffic flow quality** | 0.15 | Gridlock rate, signal compliance, average speed. |
| SM-04 | **Spatial coherence** | 0.15 | Objects don't float, overlap, or intersect illogically. Physics settle test. |
| SM-05 | **Behavioral plausibility** | 0.10 | NPC reactions are contextually appropriate. Behavior tree coverage score. |
| SM-06 | **Performance impact** | 0.10 | FPS delta from baseline. Score decreases linearly below 30fps floor. |
| SM-07 | **Narrative coherence** | 0.10 | Proposed changes are consistent with active mission state and world lore. |
| SM-08 | **Aesthetic quality** | 0.05 | Composition balance, color harmony, visual clutter index. |

**Composite Score Calculation:**

```
composite = sum(metric_score[i] * weight[i]) for i in SM-01..SM-08
```

Pass threshold: `composite >= 0.7`

### 3.3 Measurement Report Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://twin-earth-nyc.dev/schemas/measurement-report/v0.json",
  "title": "MeasurementReport",
  "type": "object",
  "required": [
    "report_id",
    "proposal_id",
    "timestamp",
    "hard_constraints",
    "soft_metrics",
    "composite_score",
    "decision",
    "sandbox_session_id"
  ],
  "properties": {
    "report_id": { "type": "string", "format": "uuid" },
    "proposal_id": { "type": "string", "format": "uuid" },
    "timestamp": { "type": "string", "format": "date-time" },
    "hard_constraints": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "name", "passed", "detail"],
        "properties": {
          "id": { "type": "string" },
          "name": { "type": "string" },
          "passed": { "type": "boolean" },
          "detail": { "type": "string" }
        }
      }
    },
    "soft_metrics": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "name", "score", "weight"],
        "properties": {
          "id": { "type": "string" },
          "name": { "type": "string" },
          "score": { "type": "number", "minimum": 0, "maximum": 1 },
          "weight": { "type": "number", "minimum": 0, "maximum": 1 },
          "detail": { "type": "string" }
        }
      }
    },
    "composite_score": { "type": "number", "minimum": 0, "maximum": 1 },
    "decision": { "type": "string", "enum": ["accepted", "rejected"] },
    "rejection_reasons": {
      "type": "array",
      "items": { "type": "string" }
    },
    "sandbox_session_id": { "type": "string" },
    "simulation_duration_seconds": { "type": "number" },
    "performance_summary": {
      "type": "object",
      "properties": {
        "avg_fps": { "type": "number" },
        "min_fps": { "type": "number" },
        "peak_memory_mb": { "type": "number" }
      }
    }
  }
}
```

---

## 4. Lifecycle State Machine

A proposal moves through the following states:

```
  [created] --> [queued] --> [simulating] --> [measured] --> [accepted] --> [committing] --> [committed]
                                                |                                            |
                                                v                                            v
                                           [rejected] --> [revised] --> [queued]         [observing]
                                                |                                            |
                                                v                                            v
                                         [rejected_final]                              [rolled_back]
                                                                                    (if post-commit
                                                                                     violation found)
```

| State | Description | Allowed Transitions |
|-------|-------------|-------------------|
| `created` | Proposal object instantiated. | `queued` |
| `queued` | Waiting for sandbox allocation. | `simulating`, `expired` |
| `simulating` | Running in sandbox environment. | `measured`, `simulation_failed` |
| `measured` | Metrics computed, awaiting decision. | `accepted`, `rejected` |
| `accepted` | Passed all criteria. Awaiting commit authority. | `committing` |
| `rejected` | Failed criteria. May be revised. | `revised`, `rejected_final` |
| `revised` | Model has submitted a new version. | `queued` |
| `rejected_final` | Max retries exceeded. Archived. | Terminal. |
| `committing` | Write transaction in progress. | `committed`, `commit_failed` |
| `committed` | Successfully promoted to canonical state. | `observing` |
| `observing` | Post-commit monitoring period (300s). | `stable`, `rolled_back` |
| `stable` | Observation passed. Proposal is finalized. | Terminal. |
| `rolled_back` | Post-commit violation detected. Changes reverted. | Terminal. |
| `expired` | TTL exceeded before simulation started. | Terminal. |
| `simulation_failed` | Sandbox crashed or timed out. | `queued` (retry), `rejected_final` |
| `commit_failed` | Write transaction failed. | `committing` (retry), `rejected_final` |

---

## 5. Audit Trail & Traceability

Every proposal carries a full audit trail:

1. **Generation context** — What triggered the proposal, which model version, what constraints were loaded.
2. **Simulation record** — Full sandbox session log, metrics, captured frames.
3. **Decision record** — Measurement report, decision authority (human or auto), timestamp.
4. **Commit record** — Ledger entry ID, affected entity IDs, state snapshot before/after.
5. **Observation record** — Post-commit monitoring results, any rollback events.

All records are immutable and stored alongside the ledger. Any canonical asset can be traced back to the proposal that introduced it, the simulation that validated it, and the human or automated authority that approved it.

---

## Appendix A: Proposal Queue Configuration Defaults

```json
{
  "max_concurrent_sandboxes": 8,
  "default_simulation_duration_seconds": 60,
  "max_simulation_duration_seconds": 300,
  "default_ttl_seconds": 3600,
  "max_retries_per_proposal": 3,
  "auto_commit_plausibility_threshold": 0.70,
  "elevated_auto_commit_threshold": 0.85,
  "post_commit_observation_seconds": 300,
  "low_confidence_review_threshold": 0.50,
  "proposal_archive_retention_days": 90
}
```

---

*End of document. Next: `scenario-library-v0.md`*
