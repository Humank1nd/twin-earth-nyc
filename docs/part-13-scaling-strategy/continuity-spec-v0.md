# Cross-Slice Continuity Spec v0 — Scaling Strategy

> **Series:** Twin Earth NYC — Part 13: Scaling Strategy
> **Document:** `continuity-spec-v0.md`
> **Status:** Draft v0
> **Depends On:** `harlem-spec-v0.md`, `assembly-spec-v0.md`

---

## 1. Overview

As the simulation scales to Ring 2 (Harlem/UWS), the Manhattan Core is divided into geospatial slices. Phase 48 ensures that entities transiting between slices maintain state persistence without drift or "teleportation" artifacts.

## 2. Continuity Protocol

| Feature | Requirement | MCU Diegetic Tag |
|---------|-------------|------------------|
| **State Hand-off** | Snapshot of entity (pos, vel, memory) at slice boundary | **Bifrost Hand-off** (Slice transition) |
| **Boundary Buffer** | 10m overlap zone where both slices track entity | **Mirror Dimension Buffer** (Overlap tracking) |
| **Lineage Persistence** | Entity ID and parent take lineage must remain invariant | **Yggdrasil Root** (Authoritative lineage) |

## 3. Invariants

1. **INV-C4801:** Velocity vector continuity across slice boundaries (delta < 0.05).
2. **INV-C4802:** Memory-Tier (Working/Habit) must persist across transitions.
3. **INV-C4803:** Anomaly Attention Weight must not reset at boundary.

## 4. MCU Diegetic Expansion Idea

**Yggdrasil Root:** The cross-slice continuity layer acts as the root system of Yggdrasil, ensuring that even as the "branches" (slices/realms) multiply, the core identity of the simulation remains unified and grounded in NYC Truth.

---
*End of Document*

## 5. Worked Example (Slice Handoff)

Slice 7 (Midtown) hands a hot pursuit to Slice 8 (Harlem) at the 110th St
boundary: anomaly weights carry over intact, Yggdrasil root confirms both
slices share INV-C4803 state, and the handoff completes without resetting
attention. A cold handoff (weights dropped) would read as a continuity
break in audit — same rule as Quilt Tower's cross-slice canon checks.

## 6. Audit Checklist

- [ ] Anomaly weights preserved across every boundary crossed.
- [ ] INV-C4803 holds: no resets at slice edges.
- [ ] Yggdrasil root acknowledges both slices before handoff closes.

Continuity is the absence of surprises across boundaries. When in doubt,
carry state forward and log the carry.
