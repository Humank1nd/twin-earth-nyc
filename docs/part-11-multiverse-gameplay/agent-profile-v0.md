# Agent Profile v0 ? Persona Anchors for Universe Packs

> **Series:** Twin Earth NYC ? Part 11: Multiverse Gameplay
> **Document:** `agent-profile-v0.md`
> **Status:** Draft v0
> **Last Updated:** 2026-01-29
> **Depends On:** `../part-06-city-living-system/agent-hierarchy-v0.md`, `../part-08-npc-realism/agent-codex-v0.md`, `translation-gate-rules-v0.md`, `universe-profile-template-v0.md`

---

## 1. Governing Principle

> **"Persona anchors are cognition profiles, not power grants. They shape how agents think, not what they are allowed to do."**

Persona anchors map the six totems into reusable cognition profiles for universe packs. They are optional overlays that must never bypass hub constraints, stanza rules, or translation gates.

---

## 2. Persona Anchors (Cognition Profiles)

| Persona | Primary Function | Default Constraints |
|---------|-------------------|---------------------|
| Questioner | Inquiry, verification, causal analysis | Must validate inputs before action (Doorway stanza) |
| Planner | Routing, sequencing, dependency control | Time-boxed decisions (Measure stanza) |
| Maker | Construction, implementation, repair | Reversible changes, idempotent ops (Forge stanza) |
| Keeper | Resource stewardship, timing, budgets | Min-privilege access, release fast (Gift stanza) |
| Speaker | Communication, formatting, delivery | Minimal output, sanitize content (Voice stanza) |
| Rememberer | Oversight, ethics, reflection | Ownership on decisions (Watch stanza) |

**Note:** Persona anchors constrain behavior. Tool ownership and permissions remain governed by the core hierarchy and shared auth contracts.

---

## 3. Universe Pack Mapping

Persona anchors can be attached to a universe pack to bias cognition without changing constraints.

Example mapping:

| Pack Type | Primary Persona | Secondary Personas |
|-----------|------------------|-------------------|
| High-myth hub (Earth-1218) | Rememberer | Questioner, Keeper |
| Heroic realm | Maker | Planner, Speaker |
| Investigation realm | Questioner | Planner, Rememberer |
| Survival realm | Keeper | Questioner, Maker |

---

## 4. Translation Gate Compatibility

All persona overlays must pass translation gates. No persona may:

- bypass stanza rules
- elevate recursion tiers
- alter Trust Ledger write thresholds
- override shared auth/RBAC checks

If a pack proposes a persona overlay that conflicts with translation rules, the overlay is rejected or reduced to a non-authoritative label.

---

## 5. Times Square Slice Guidance

For the Times Square slice:

- Use **Questioner + Keeper** as default overlays for NPCs.
- Cap recursion depth to hub policy (no higher than 4 tiers).
- Use persona anchors only for bounded rationality, not for capability escalation.

---

## 6. Integration Checklist

1. Bind persona anchors to agent profiles using `universe-profile-template-v0.md`.
2. Validate overlays against `translation-gate-rules-v0.md`.
3. Enforce stanza rules and auth constraints at runtime.
4. Log persona assignments for auditability.

---

## 7. Cross-References

- `../part-06-city-living-system/agent-hierarchy-v0.md`
- `../part-08-npc-realism/agent-codex-v0.md`
- `translation-gate-rules-v0.md`
- `universe-profile-template-v0.md`

---

## 8. Related Docs

- [Agent Hierarchy v0](../part-06-city-living-system/agent-hierarchy-v0.md) ? 108-role structure with recursion tiers.
- [Agent Codex v0](../part-08-npc-realism/agent-codex-v0.md) ? Stanza framework for NPC decision constraints.

_Diegetic note: Treat the cross-links as Yggdrasil branches for safe realms navigation._

---

## 9. Open Questions

- Should persona anchors be declared at pack level only, or can districts override within a pack?
- Do we need a default persona fallback for packs with no declared overlays?
