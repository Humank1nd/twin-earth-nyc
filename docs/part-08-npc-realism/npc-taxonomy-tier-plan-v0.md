# NPC Taxonomy + Tier Plan v0

**Document:** Part 8 — NPC Realism
**File:** `npc-taxonomy-tier-plan-v0.md`
**Status:** Draft v0
**Last Updated:** 2026-01-27
**Depends On:** Part 4 (Slice Architecture), Part 7 (Event Bus + Heat System)
**Feeds Into:** Sensor Interface Spec, Curriculum + Reward Spec, Runtime Validation Checklist

---

## 1. NPC Categories (v1)

All counts are reference values for the **Times Square slice** at **midday peak density**. Other slices scale proportionally based on real-world pedestrian-flow data.

| # | Category | Tier | Count (Times Square) | Behavior Model | Persistence |
|---|----------|------|----------------------|----------------|-------------|
| 1 | Pedestrian (commuter) | Background | 500 -- 1,500 | Heuristic (lane-follow + avoidance) | Session only |
| 2 | Pedestrian (tourist) | Background | 200 -- 500 | Heuristic (stop-and-look + photo patterns) | Session only |
| 3 | Pedestrian (hero) | Hero | 5 -- 20 | Learned policy (sensor-limited RL) | Cross-session (memory persists) |
| 4 | Driver (vehicle) | Background | 50 -- 100 | Scripted path + traffic rules | Session only |
| 5 | Driver (hero) | Hero | 1 -- 5 | Learned policy (vehicle control RL) | Cross-session |
| 6 | Cop (patrol) | Hero | 2 -- 5 | Heuristic + learned pursuit | Cross-session (patrol memory) |
| 7 | Cop (crowd control) | Background | 0 -- 5 (event-driven) | Scripted cordon behavior | Event duration only |
| 8 | Security Guard | Background | 3 -- 8 | Heuristic (stationary + alert response) | Session only |
| 9 | Vendor | Background | 5 -- 15 | Scripted (stationary + interaction) | Session only |
| 10 | EMS | Background | 0 -- 2 (event-driven) | Scripted response routing | Event duration only |

---

## 2. Tier Definitions

### Background NPC

| Property | Value |
|----------|-------|
| Behavior | Heuristic or scripted -- no learning, no policy inference |
| Memory | None -- no persistent memory across or within sessions |
| Simulation cost | ~0.1 ms / tick (budget: 150 ms total for all background NPCs at peak) |
| Rendering | Visually instanced at distance (LOD Level 2+ beyond 30 m) |
| Sensor simulation | None -- behavior is reactive to immediate surroundings only |
| Physics | Simplified capsule collider, no ragdoll |
| Interaction | Limited -- can respond to player proximity cues but cannot initiate complex sequences |

### Hero NPC

| Property | Value |
|----------|-------|
| Behavior | Learned RL policy evaluated at runtime via ONNX inference |
| Memory | Working memory (30 s short-term) + long-term habit memory (cross-session) |
| Simulation cost | ~2 ms / tick (budget: 40 ms total for up to 20 hero NPCs) |
| Rendering | Unique appearance, full LOD chain, facial animation rig |
| Sensor simulation | Full sensor suite (forward camera, depth probes, audio proxy) |
| Physics | Full capsule + ragdoll on incapacitation, vehicle collision response |
| Interaction | Can initiate and sustain complex interactions, generate witness events, pursue/flee |

---

## 3. Policy Assignment Rule

> **"Hero learning only where consequences matter."**

Hero NPCs are placed exclusively where their autonomous decisions **affect gameplay systems**:

- **Pursuit** -- patrol cops that must perceive, decide, and chase.
- **Evidence generation** -- hero pedestrians who witness events and file observations into the evidence ledger (Part 7).
- **Anomaly response** -- hero NPCs near anomaly zones whose behavior visibly changes, providing the player environmental cues.
- **Mission interaction** -- any NPC the player may need to follow, distract, or observe across sessions.

All other population roles are filled by background NPCs to preserve compute budget.

---

## 4. Spawn / Despawn Rules

### Background NPCs

| Rule | Detail |
|------|--------|
| Spawn locations | Slice boundaries (sidewalk entry points), subway entrances, building doors |
| Despawn trigger | Distance > 200 m from player **OR** NPC reaches a slice boundary exit point |
| Spawn rate | Follows time-of-day schedule (see density targets below) |
| Pool recycling | Despawned NPCs return to an object pool; visual appearance is re-randomized before next spawn |
| Anti-pop-in | NPCs spawn behind occluders or at the edge of the camera frustum when possible |

### Hero NPCs

| Rule | Detail |
|------|--------|
| Spawn trigger | Session start -- placed at designated anchor locations (beat origins for cops, key intersections for hero pedestrians) |
| Despawn trigger | Session end **OR** distance-based tier downgrade (see below) |
| Tier downgrade | If hero NPC moves > 300 m from player AND no active gameplay link (pursuit, mission), demote to background-tier simulation. Re-promote on approach. |
| Memory on downgrade | Working memory frozen at downgrade; long-term memory retained. On re-promotion, working memory resumes from frozen state if < 5 min elapsed, otherwise cleared. |

### Density Targets

| Condition | Sidewalk Density (persons/m²) | Reference Location |
|-----------|-------------------------------|-------------------|
| Peak midday (12:00 -- 14:00) | 2.5 | TKTS booth / Duffy Square |
| Afternoon (14:00 -- 18:00) | 1.8 | Broadway & 45th |
| Evening (18:00 -- 22:00) | 1.5 | Theater district |
| Late night (22:00 -- 02:00) | 0.8 | General sidewalks |
| Off-peak night (02:00 -- 06:00) | 0.3 | General sidewalks |
| Morning ramp (06:00 -- 09:00) | 1.0 | Commuter corridors |
| Morning peak (09:00 -- 12:00) | 2.0 | Commuter corridors |

Density values are enforced by the spawn controller, which adjusts spawn rate and despawn distance dynamically to hit the target within +/- 10%.

---

## 5. Budget Summary

| Resource | Budget | Notes |
|----------|--------|-------|
| Background NPC tick (all) | 150 ms / frame | ~1,500 NPCs x 0.1 ms at peak |
| Hero NPC tick (all) | 40 ms / frame | ~20 hero NPCs x 2 ms at peak |
| Total NPC simulation | 190 ms / frame | Must fit within 33 ms game-tick via async spread across frames |
| NPC memory (hero, per NPC) | 64 KB working + 256 KB long-term | Serialized to save file on session end |
| NPC memory (background) | 0 | Stateless |

> **Note:** The 190 ms total is amortized across multiple game frames using a round-robin update scheduler. Not all NPCs update every frame -- background NPCs update at 5 Hz, hero NPCs at 10 Hz.

---

## Open Questions

1. Should hero pedestrian count scale with player notoriety (higher Heat = more alert hero NPCs spawned)?
2. What is the maximum hero NPC count before inference latency exceeds budget on target hardware?
3. Should vendor NPCs be promotable to hero tier for mission-specific interactions?

---

*End of document.*
