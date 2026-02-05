# Visual Scaling Spec v0 — Attention Budgeting & Perceptual LOD

> **Series:** Twin Earth NYC — Part 9: Forced Perspective
> **Document:** `visual-scaling-spec-v0.md`
> **Status:** Draft v0
> **Depends On:** `portal-spec-v0.md` (anomaly inputs), `simulation-architecture-v0.md`

---

## 1. Overview

Visual Scaling ensures that the Twin Earth simulation remains performant as it scales from a single block to the full Midtown Corridor. It operationalizes **Attention Budgeting**: a system that dynamically allocates rendering and simulation resources based on the player's perceptual focus.

## 2. Attention Budgeting Rules

The **Show Director** (Part 9.2) manages a global attention budget ($A = 1.0$).

| Zone | Attention Weight ($W$) | Description |
|------|------------------------|-------------|
| **Hero Zone** | $W \ge 0.8$ | 0-50m from camera. Full physics, 60fps logic, 4K textures. |
| **Active Corridor** | $0.4 \le W < 0.8$ | 50-200m. Simplified physics, 15fps logic, 1K textures. |
| **Background City** | $0.1 \le W < 0.4$ | >200m. No physics, static proxies, billboard crowds. |
| **Culled** | $W < 0.1$ | Outside FOV or occluded. Logic-only (no visual). |

## 3. LOD Bands (Semantic Reduction)

LOD transitions are determined by the **Reality Stone** logic (diegetic expansion idea).

### 3.1 Band Transitions
- **Band 0 (Truth):** Entity is exactly as defined in the Truth Engine.
- **Band 1 (Proxy):** Entity is replaced by a low-cost visual proxy (Scale Anchor).
- **Band 2 (Impression):** Entity is absorbed into a field gradient (e.g., individual NPCs become a "Crowd Density" field).

## 4. Stability Constraints

AlphaEvolve optimizes the `attention_decay` parameter to ensure smooth transitions between bands.

- **Flicker Delta:** Resource re-allocation must not cause visual popping $> 0.05$ change in triangle count per frame.
- **Budget Threshold:** If total triangle count exceeds 5M, the Show Director must force semantic reduction in the Background City.

## 5. Dynamic LOD (Pursuit Integration)

The Show Director can escalate LOD detail for entities identified as narrative-critical by the Pursuit AI (Part 8).

| Escalation Type | Condition | Visual Impact | MCU Diegetic Tag |
|-----------------|-----------|---------------|------------------|
| **Pursuit Boost** | Entity is actively pursued/engaged | +50% triangle budget, 60fps animation | **Heimdall Search** (Hyper-focus on target) |
| **Anomaly Surge** | Entity is within 10m of open portal | Dynamic light spill, shadow focus | **Reality Warp** (Local truth distortion) |

---
*End of Document*
