# Portal & Translation Gate Spec v0 — Multiversal Boundaries

> **Series:** Twin Earth NYC — Part 11: Multiverse Gameplay
> **Document:** `portal-spec-v0.md`
> **Status:** Draft v0
> **Depends On:** `universe-agent-profiles-v0.md` (cognition scaling), `simulation-architecture-v0.md`

---

## 1. Overview

Portals are the primary interfaces between the Earth-1218 Hub and external Universe Packs. They are modeled as stateful system boundaries that enforce **Translation Gates**: a set of decay rules that prevent "Impossible Realities" from destabilizing the Hub's physical baseline.

## 2. Portal State Machine

Portals transition through the following states based on Energy ($E$) and Strain ($S$) metrics.

| State | Condition | Effect |
|-------|-----------|--------|
| **CLOSED** | $E < 0.3$ | No traversal. Background anomaly hum only. |
| **OPENING** | $E \ge 0.3$ | Visual shimmer. 30s warmup period. |
| **OPEN** | $E \ge 0.5$ and $S < 0.8$ | Bidirectional traversal enabled. Translation Gates active. |
| **CLOSING** | $S \ge 0.8$ or manual trigger | Visual collapse. 10s exit window. Lethal if inside. |
| **QUARANTINED** | Reality Breach detected | Hard-sealed by System. Requires Admin cleanup. |

## 3. Translation Gates (The Decay Rule)

To maintain the "Marvel as fiction" baseline in Earth-1218, all imported artifacts and energy signatures undergo exponential decay when passing through a gate.

### 3.1 Decay Formula
$$Power_{Hub} = Power_{Origin} \times 0.7^{hops}$$

- **Hops:** Number of dimensional boundaries crossed (e.g., 616 -> Pocket -> 1218 = 2 hops).
- **MCU Diegetic Tag:** **Bifrost Bandwidth Cap** (The bridge cannot carry infinite energy; only a fraction reaches Midgard).

## 4. Stability Constraints

AlphaEvolve optimizes the `threshold` parameter to ensure portal activity does not trigger a global `HARD_FAIL`.

- **Stability Delta:** Change in local field values must remain $< 0.08$ per tick.
- **Strain Threshold:** If local Institutional Heat exceeds 0.7, the portal enters **CLOSING** state automatically.

---
*End of Document*
