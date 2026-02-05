# Agent Codex v0 ? Stanza Governance for NPC Bounded Rationality

> **Series:** Twin Earth NYC ? Part 8: NPC Realism
> **Document:** `agent-codex-v0.md`
> **Status:** Draft v0
> **Last Updated:** 2026-01-29
> **Depends On:** `authority-response-spec-v0.md` (escalation paths), `runtime-validation-checklist-v0.md` (runtime gates), `../part-06-city-living-system/agent-hierarchy-v0.md` (roles + recursion)

---

## 1. Governing Principle

> **"NPCs are bounded thinkers. They act with constraints, not omniscience. Their competence is a budget, not a promise."**

This codex applies the six Havamal stanzas to NPC decision-making. Each stanza is a behavioral constraint and a runtime checklist. The goal is believable agency under limits, not perfect optimization.

---

## 2. Bounded Rationality Envelope

Every NPC decision is constrained by explicit budgets:

| Budget | Default | Purpose |
|--------|---------|---------|
| Time | 50-200 ms | Prevents analysis paralysis |
| Context | 1-3 local facts | Limits scope to local reality |
| Memory | 0-3 short-term items | Avoids perfect recall |
| Escalation | 1 hop | Keeps authority local |

Budgets are tuned per NPC tier (see `npc-taxonomy-tier-plan-v0.md`).

---

## 3. Stanza Constraints (Decision Checklist)

Each stanza is a rule set applied to NPC decisions. If a rule cannot be satisfied, the NPC must degrade gracefully or escalate.

| Stanza | NPC Behavior Constraint | Failure Action |
|--------|--------------------------|----------------|
| Doorway (WHY) | Observe first, validate inputs, threat model | Escalate if context unverifiable |
| Gift (HOW) | Minimum privilege, release resources fast | Degrade if resources denied |
| Forge (WHAT) | Reversible changes, idempotent actions | Roll back or no-op |
| Measure (WHEN) | Time-box decisions | Escalate after budget exceeded |
| Voice (WHERE) | Minimal output, sanitize, context-aware | Redact and retry |
| Watch (WHO) | Ownership on every decision | Log "no action" with reason |

---

## 4. Persona Anchors

NPCs align to a persona anchor that shapes tone and priorities:

| Persona | Anchor Phrase | Example NPC Behavior |
|---------|---------------|----------------------|
| Questioner | Ask, then verify | Checks a signal before reacting |
| Planner | Measure twice | Chooses a safer path over fastest |
| Maker | Build to last | Prefers stable actions over flashy |
| Keeper | Guard borrowed resources | Avoids wasteful actions |
| Speaker | Words cannot return | Keeps output short and safe |
| Rememberer | Learn from the fallen | Avoids repeating known failures |

Persona anchors must not override stanza constraints.

---

## 5. NPC Memory and the Crystallization Gate

NPC memory writes are gated to preserve realism and prevent drift:

1. Confidence >= 0.7 and at least one contradicting hypothesis tested.
2. Human approval required unless confidence > 0.95.
3. Memory writes are append-only; use deprecation instead of deletion.

If the gate fails, the NPC must discard or keep only transient memory.

---

## 6. Strain Metrics and Heat Alignment

Strain metrics provide NPC-level signals that roll up into Heat channels.

| Wound | Signal | NPC Symptom |
|-------|--------|-------------|
| Eye | `wisdom_strain` | Overthinking, no action |
| Side | `fate_strain` | Over-planning, under-acting |
| Hand | `chaos_strain` | Thrashing behavior |
| Foot | `tide_strain` | Late or stalled responses |
| Throat | `place_strain` | Wrong audience/context |
| Heart | `watch_strain` | Decision fatigue |
| 7-9 | `system_strain` | Resource pressure |

**Ragnarok protocol:** Any wound > 0.8 triggers graceful degradation (drop to safe defaults, halt risky actions).

---

## 7. Runtime Validation Hooks

NPC decision loops must emit structured logs for validation:

```json
{
  "event": "npc_decision",
  "stanza": "Doorway",
  "budgets": {"time_ms": 120, "context": 2, "memory": 1},
  "verdict": "action",
  "strain": {"wisdom": 0.2, "chaos": 0.1}
}
```

These logs feed into the Part 8 runtime validation checklist.

---

## 8. Times Square Slice Guidance

For the Times Square slice:

- **Constrain memory writes:** favor transient memory only.
- **Low-latency decisions:** keep time budget < 100 ms for crowd behaviors.
- **No escalation past block:** avoid skip-level authority hops.

---

## 9. Optional Diegetic Expansion Tags (Non-Blocking)

Universe packs may add mythic labels for narrative flavor, but they cannot override stanza rules or budgets. Any thematic tags must be applied after translation gates to protect Earth-1218 hub constraints.

---

## 10. Implementation Checklist

1. Bind stanza checklists into NPC decision loops.
2. Enforce bounded rationality budgets by tier.
3. Gate memory writes through crystallization.
4. Emit strain metrics into Heat channels.
5. Validate logs with runtime checklist tooling.

---

## 11. Open Questions

- What is the default time budget per NPC tier in the Times Square slice?
- Which Heat channels should receive strain metrics first (physical, social, anomaly, or economic)?

