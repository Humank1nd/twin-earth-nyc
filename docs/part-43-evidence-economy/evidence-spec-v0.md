# Evidence Economy Spec v0 — Informational Feedback Loops

> **Series:** Twin Earth NYC — Part 43: Evidence Economy
> **Document:** `evidence-spec-v0.md`
> **Status:** Draft v0
> **Depends On:** `field-systems-spec-v0.md` (informational flows), `heat-evidence-economy-spec-v0.md`

---

## 1. Overview

The Evidence Economy governs how multiversal anomalies manifest as "truth" in Earth-1218. It transform raw sensor data into public belief and institutional Heat, creating a feedback loop that drives faction responses.

## 2. Generation (The Nervous System)

IoT artifacts (Part 7.1) act as the primary sensors for evidence generation.

| Artifact | Data Input | Evidence Class | MCU Diegetic Tag |
|----------|------------|----------------|------------------|
| **CCTV Camera** | Visual Feed | Digital/Institutional | **Heimdall Scan** (Official telemetry) |
| **Information Kiosk** | System Logs | Digital/Social | **Daily Bugle Wire** (Public data) |
| **NPC Witness** | Direct Sighting | Witness/Rumor | **Loki Deception** (Narrative vector) |

## 3. Belief Mechanics (Bounded Rationality)

Belief ($B$) propagates through the NPC population via sequential gossip (Section 8.5).

### 3.1 Propagation Equation
$$
B_{t+1} = B_t \times (1 - \text{misinfo\_factor}) + \text{source\_input}
$$

- **Confidence Threshold:** If $B > 0.5$, the NPC transitions from "Complacent Local" to "Witness," enabling higher-tier reporting behaviors.

## 4. Heat Coupling (Institutional/Social Spikes)

Evidence accumulation drives spikes in the 4-channel Heat field (Section 11.4).

- **Institutional Heat:** Triggered by high-confidence CCTV evidence.

- **Social Heat:** Triggered by high-density rumor fields ($B > 0.7$).



## 5. Faction Integration



The Evidence Economy feeds Institutional Heat into the Faction Response state machine (Phase 44).



| Threshold | Faction Level | Dynamic Action | MCU Diegetic Tag |

|-----------|---------------|----------------|------------------|

| $H_i \ge 0.4$ | **HIGH** | Task force deployment, road closures | **SHIELD Level 3** (Intervention active) |

| $B \ge 0.8$ | **CRITICAL** | Media lockdown, evacuation advisory | **TVA Paradox Hunter** (Timeline pruning) |



---

*End of Document*
