# Pursuit AI Spec v0 — Autonomous Search & Interception

> **Series:** Twin Earth NYC — Part 8: NPC Realism
> **Document:** `pursuit-spec-v0.md`
> **Status:** Draft v0
> **Depends On:** `navigation-service-v0.md`, `agent-profiles-v0.md` (cognition)

---

## 1. Overview

Pursuit AI governs how Authority and Hostile NPCs respond to perceived threats or anomalies. It bridges the gap between raw **Perception** (Phase 38) and **Navigation** (Part 4) by managing a high-level state machine focused on target acquisition and tracking.

## 2. Pursuit State Machine

Agents transition through the following states based on Line-of-Sight (LOS) and Witness Data.

| State | Condition | Effect |
|-------|-----------|--------|
| **PATROL** | No active target. | Move along predefined waypoints (Scale Anchors). |
| **PURSUE** | Target in LOS. | Navigate directly to target. Request Visual Scaling boost (Band 0). |
| **SEARCH** | Target lost, but LKP (Last Known Position) exists. | Navigate to LKP. Query **Witness Network** for updates. |
| **COOLDOWN** | Target lost > 60s. | Return to PATROL. Update Institutional Heat (Social trace). |

## 3. Witness Network (Search Heuristics)

When a target is lost, searching agents can "poll" nearby NPCs (The Local, The Tourist) for LKP updates.

- **Query Cost:** O(1) field lookup (reads the Witness field at current position).
- **Success Probability:** Based on Witness profile sensitivity and Anomaly level.
- **MCU Diegetic Tag:** **Heimdall Search** (Hyper-focused target tracking across the mesh).

## 4. Navigation Constraints

Pursuit logic utilizes the `NavigationService` to enforce `NAV_PATH_VALID` constraints.

- **Re-solving Rate:** Pursuit paths are re-solved every 2.0s to account for dynamic crowd shifts (Phase 37).
- **Interception Logic:** Predicts target's future position based on current velocity vector.

---
*End of Document*
