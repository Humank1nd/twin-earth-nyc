# Faction Response Spec v0 — Dynamic Orchestration

> **Series:** Twin Earth NYC — Part 44: Faction Response
> **Document:** `faction-spec-v0.md`
> **Status:** Draft v0
> **Depends On:** `evidence-spec-v0.md` (belief/Heat inputs), `traffic-spec-v0.md` (interventions)

---

## 1. Overview

The Faction Response system governs how institutional and social actors (NYPD, SHIELD, Sanctum Guardians) respond to multiversal anomalies. It transform Heat channels and belief levels into world-state transitions and specific interventions.

## 2. Response Levels (The State Machine)

Factions transition through the following levels based on composite Heat ($H$) and Belief ($B$). 

| Level | Condition | Effect | MCU Diegetic Tag |
|-------|-----------|--------|------------------|
| **ROUTINE** | $H < 0.2$ | Standard patrol, no special alert. | **Standard Protocol** (Normalcy) |
| **ELEVATED** | $H \ge 0.2$ or $B \ge 0.3$ | Increased surveillance, plainclothes officers. | **SHIELD Level 1** (Observation) |
| **HIGH** | $H \ge 0.4$ or $B \ge 0.5$ | Road closures, specialized task force (Phase 41). | **SHIELD Level 3** (Intervention) |
| **CRISIS** | $H \ge 0.7$ or $B \ge 0.8$ | Full lockdown, National Guard, reality exfil blocks. | **SHIELD Level 7** (Martial Law) |

## 3. Reputation Standing

Player reputation with a faction determines the "friendly" vs "hostile" nature of the response.

- **Asset:** Reputation $> 0.5$. Faction shares intel, reduces Heat impact of player actions.
- **Neutral:** $-0.5 \le \text{Reputation} \le 0.5$. Standard protocol applies.
- **Target:** Reputation $< -0.5$. Faction actively pursues player, increases Institutional Heat.

## 4. Intervention Logic

When a level shift occurs, the **Response Manager** (Part 11.6) triggers one-time events.
- **Lockdown Trigger:** Transition to **CRISIS** forces all portals to **QUARANTINED** state (Phase 39).
- **MCU Diegetic Tag:** **Avengers Initiative** (Escalation to hero-level response).

---
*End of Document*