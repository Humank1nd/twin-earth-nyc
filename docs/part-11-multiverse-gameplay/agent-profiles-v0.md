# Agent Profiles Spec v0 — Cognitive Archetypes & Memory Models

> **Series:** Twin Earth NYC — Part 11: Multiverse Gameplay
> **Document:** `agent-profiles-v0.md`
> **Status:** Draft v0
> **Depends On:** `field-systems-spec-v0.md` (inputs), `npc-cognition-v0.md` (Phase 38 core)

---

## 1. Overview

Agent Profiles define the "lens" through which NPCs perceive and process the Living Systems fields. Instead of a generic AI, each NPC is assigned a profile that determines their:
1.  **Sensor Filter:** What they see/hear (e.g., ignoring anomalies vs. hyper-focus).
2.  **Memory Model:** How they retain information (short-term vs. long-term).
3.  **Decision Weighting:** How they prioritize inputs (Fear vs. Curiosity).

## 2. Standard Profiles (Earth-1218)

| Profile | Description | Sensor Bias | Memory Rule | MCU Diegetic Tag |
|---------|-------------|-------------|-------------|------------------|
| **The Local** | Times Square native, jaded. | Ignores low-level Noise/Social Heat. | High habit retention, low anomaly retention. | **Happy Hogan** (Seen it all, business as usual) |
| **The Tourist** | Overwhelmed, reactive. | High sensitivity to Visual/Noise fields. | Fragmented memory, high emotional imprint. | **Ant-Man (Lang)** (Awed by scale, reactive) |
| **The Authority** | Police/Security, objective. | Tuned to Physical/Institutional Heat. | Structured logging, verified facts only. | **SHIELD Agent** (Protocol-driven observation) |
| **The Witness** | Conspiracy theorist, seeking. | Hyper-sensitive to Anomaly fields. | High retention of "weird" events, confirmation bias. | **J. Jonah Jameson** (Seeking the narrative) |

## 3. Memory Architecture

Agents utilize a two-tier memory system:

### 3.1 Working Memory (Short-Term)
- **Capacity:** 5-9 "slots" (Miller's Law).
- **Decay:** Rapid exponential decay (slew_rate ~ 0.5/s).
- **Input:** Raw field data (e.g., "Loud noise at [10, 20]").

### 3.2 Habit Memory (Long-Term)
- **Capacity:** 100+ slots (compressed).
- **Reinforcement:** Repeated Working Memory entries transfer here.
- **Function:** Defines "Normalcy" bias. (e.g., "Times Square is always loud" -> Noise doesn't trigger stress).

## 4. AlphaEvolve Parameters

| Parameter | ID | Range | Description |
|-----------|----|-------|-------------|
| **memory_capacity_slots** | `M-01` | 3 - 15 | Number of concurrent items in Working Memory |
| **memory_decay_rate** | `M-02` | 0.1 - 2.0 | Speed at which un-reinforced memories fade |
| **anomaly_attention_weight** | `M-03` | 0.0 - 1.0 | Likelihood to prioritize Anomaly field data |

## 5. Worked Example (Memory Pressure)

An agent holds 15 slots (M-01 max) with decay 2.0 and anomaly weight 1.0
during a Convergence event: un-reinforced memories fade within the hour
while anomaly field data crowds out routine observations. The profile
recommends dropping decay to 0.5 post-event so baseline memory rebuilds
before the next slice.

---
*End of Document*
