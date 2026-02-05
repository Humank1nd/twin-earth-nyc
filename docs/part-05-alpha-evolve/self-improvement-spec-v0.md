# Self-Improvement Spec v0 — AlphaEvolve Meta-Optimization

> **Series:** Twin Earth NYC — Part 5: AlphaEvolve
> **Document:** `self-improvement-spec-v0.md`
> **Status:** Draft v0
> **Depends On:** `alpha-evolve-spec-v0.md`, `metrics-spec-v0.md`

---

## 1. Overview

Self-improvement in the Twin Earth Simulation is an emergent process where AlphaEvolve (Part 5) iteratively refines its own optimization mechanics. It treats hyperparameters—such as mutation rates and selection weights—as evolvable parameters, ensuring the "Flywheel" (Section 5.5) becomes increasingly efficient at gap-filling without authored bias.

## 2. Meta-Optimization Loop

The system executes a higher-order loop to tune the optimizer itself.

| Hyperparameter | Range | Function | MCU Diegetic Tag |
|----------------|-------|----------|------------------|
| **Mutation Rate** | 0.1 - 0.5 | Probability of random jitter in candidates. | **Odinforce Recharge** (Kernel cooldown) |
| **Selection Weight** | 0.5 - 0.9 | Bias toward high-score vs. high-diversity. | **Heimdall Choice** (Priority routing) |
| **Generational Gap** | 1 - 5 | Number of steps between meta-evaluations. | **Convergence Sync** (Alignment frequency) |

## 3. Feedback Mechanics

The meta-loop monitors **Optimization Stability** ($\Delta_{opt}$):
- **Criterion:** The change in average population score over 3 generations.
- **Rule:** If $\Delta_{opt} < 0.05$ (stagnation), increase Mutation Rate by 0.1.
- **Rule:** If $\Delta_{opt} > 0.20$ (chaos), decrease Mutation Rate by 0.05.

## 4. Stability Constraints

To prevent recursive runaway, meta-optimizations are decayed by **Translation Gates** (Phase 39) before being committed to the Hub's Truth Layer.

- **Impact Cap:** Meta-tuning cannot alter base physical constants (SI Units).
- **Diegetic Tag:** **Bifrost Bandwidth Cap** (Limits the energy available for self-modification).

## 5. IoT-Limited Meta-Optimization

Hyperparameters are subjected to sensor-limited noise from IoT artifacts (Part 7) to prevent meta-drift.

| Component | Rule | Effect | MCU Diegetic Tag |
|-----------|------|--------|------------------|
| **Meta-Sensor** | $M_{obs} = \max(0.1, M_{base} \times (1 - \text{noise}))$ | Random noise $[0, 0.2]$ | **Heimdall Sight** (Sensor-limited monitoring) |
| **Meta-Audit** | IDS Check | Reduction on tamper detection | **Heimdall IDS** (Evidence integrity) |

---
*End of Document*
