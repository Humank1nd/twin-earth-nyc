# Traffic AI & Signal Control Spec v0 — Dynamic Infrastructure

> **Series:** Twin Earth NYC — Part 42: Traffic AI
> **Document:** `traffic-spec-v0.md`
> **Status:** Draft v0
> **Depends On:** `field-systems-spec-v0.md` (conserved flows), `pursuit-spec-v0.md` (NPC response)

---

## 1. Overview

Traffic AI governs the autonomous flow of vehicles and signal synchronization across the Midtown Corridor. It treats vehicle volume as a conserved matter field (Part 6.3) and utilizes **Gridlock Resolve** algorithms to ensure simulation stability during high-activity events (e.g., anomalies or pursuits).

## 2. Signal State Machine

Intersections utilize a synchronized state machine to manage throughput.

| State | Condition | Effect |
|-------|-----------|--------|
| **GREEN** | Cycle $T < 60s$ and $G < 0.5$ | Flow enabled in primary direction. |
| **RED** | Cycle $T \ge 60s$ or $G \ge 0.5$ | Flow stopped. Gridlock ($G$) threshold triggered. |
| **RESOLVING** | $G \ge 0.8$ | Emergency reroute active. Neighbors notified via Yggdrasil Bridge. |

- **Gridlock ($G$):** Scalar metric $[0, 1]$ representing occupancy vs. capacity.
- **MCU Diegetic Tag:** **Bifrost Congestion** (Heimdall rerouting traffic across the realms network).

## 3. Gridlock Resolve (Self-Healing)

When an intersection enters the **RESOLVING** state, the following rules apply:
1.  **Slew Rate Adjustment:** Flow capacity is artificially boosted ($+30\%$) to clear the bottleneck.
2.  **Reroute Command:** Agents in the "Active Corridor" (Phase 40) receive a semantic reroute event.
3.  **Stability Delta:** The transition must maintain a local field change $< 0.08$ to prevent visual popping.

## 4. Pursuit Integration

Pursuing agents (Phase 41) gain priority access to signal "Truth Layers."
- **Override Privilege:** Pursue state NPCs can force a GREEN state if within 20m of an intersection.
- **Avoidance:** Search state NPCs automatically reroute if $G > 0.5$ at their LKP.

## 5. IoT Sensor Integration

Signal controllers utilize real-time data from IoT artifacts (Part 7) to optimize throughput.

| Artifact | Data Input | Effect | MCU Diegetic Tag |
|----------|------------|--------|------------------|
| **CCTV Camera** | Traffic density ($D$) | Cycle reduction: $T_{new} = T_{base} \times (1 - D \times 0.5)$ | **Heimdall Sight** (Real-time flow monitoring) |
| **Proximity Sensor** | Emergency vehicle presence | Force GREEN state (override) | **Bifrost Clearance** (Priority routing) |

---
*End of Document*
