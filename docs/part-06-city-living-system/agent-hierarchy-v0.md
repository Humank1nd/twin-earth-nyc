# Agent Hierarchy v0 ? 108-Role Council, Stanza Governance, and Recursion Guards

> **Series:** Twin Earth NYC ? Part 6: City-as-Living-System
> **Document:** `agent-hierarchy-v0.md`
> **Status:** Draft v0
> **Last Updated:** 2026-01-29
> **Depends On:** `hierarchy-coupling-rules-v0.md` (multi-resolution flow), `field-systems-spec-v0.md` (field update pipeline)

---

## 1. Governing Principle

> **"Emergence comes from constraints, not scripts. Roles are fixed, behavior is bounded, and recursion is capped by the hub."**

The agent system uses a fixed 6 x 18 hierarchy (108 total roles) to ensure consistency across scales while allowing emergent behavior. Each totem governs a question (WHY/HOW/WHAT/WHEN/WHERE/WHO), with stanza rules that constrain decision-making. Recursion is permitted for simulation fidelity but must remain within the hub's allowed depth to prevent bleed across universe packs.

---

## 2. Totem Structure (6 x 18)

Each totem answers a core question and owns 18 roles organized as: 1 Chief, 2 Directors, 3 Leads, 5 Managers, 7 Specialists.

| Totem | Question | Function | Persona Anchor |
|------|----------|----------|----------------|
| Purple Elephant | WHO | Empathy, oversight, reflection | Rememberer |
| Red Owl | WHY | Research, inquiry, knowledge | Questioner |
| Orange Orangutan | HOW | Logistics, routing, planning | Planner |
| Yellow Honeybee | WHAT | Creativity, development, build | Maker |
| Green Tortoise | WHEN | Budgeting, resources, timing | Keeper |
| Blue Dolphin | WHERE | Communication, delivery, audience | Speaker |

**Role invariant:** The 108 roles are stable identifiers. Behavior changes by stanza rules and context, not by renaming roles.

---

## 3. Stanza Governance (WHY/HOW/WHAT/WHEN/WHERE/WHO)

Each totem uses a stanza checklist to constrain behavior. Stanzas replace vague "agent archetypes" with enforceable rules that align with bounded rationality.

| Stanza | Totem | Behavior Constraint | Failure Action |
|--------|-------|---------------------|----------------|
| Doorway (WHY) | Red Owl | Recon first, validate inputs, threat model | Escalate if inputs unverifiable |
| Gift (HOW) | Orange Orangutan | Minimum privilege, release resources fast | Degrade gracefully if resources denied |
| Forge (WHAT) | Yellow Honeybee | Reversible changes, idempotent ops, audit trail | Rollback on failed verification |
| Measure (WHEN) | Green Tortoise | Time-box decisions, avoid over-optimization | Escalate after N iterations |
| Voice (WHERE) | Blue Dolphin | Minimal output, sanitize, context-aware | Redact and retry if leak risk |
| Watch (WHO) | Purple Elephant | Ownership on every decision, no silent deferrals | Log "no action" with justification |

**Note:** Stanza rules are universal across packs. Universe packs may add flavor, but not weaken constraints.

---

## 4. Recursion Tiers and Hub Guardrails

Recursion enables multi-resolution reasoning, but must remain bounded by hub rules in Earth-1218.

| Tier | Scale | Example Use | Guardrail |
|------|-------|-------------|----------|
| Macro | City | City-level event synthesis | No direct writes to Entity memory |
| Meso | District/Block | Local policy and routing | No cross-district overrides |
| Micro | Patch | Field adjustments, local sensing | TTL-limited state only |
| Nano | Entity | Individual NPC behavior | No permanent memory writes without gate |

**Hub Sacred constraint:** Recursion depth is capped by pack policy. Earth-1218 defaults to 4 tiers unless explicitly approved.

---

## 5. Crystallization Gate (Persistence Filter)

Permanent understandings ("city memory") must pass a crystallization gate:

1. Confidence >= 0.7 and at least one contradicting hypothesis tested.
2. Human approval required unless confidence > 0.95.
3. Writes are append-only; deletions are disallowed (use deprecation).

This gate aligns with Trust Ledger persistence: knowledge is earned, not assumed.

---

## 6. Strain Metrics (Nine Wounds)

Strain metrics track systemic stress and map to emergency protocols.

| Wound | Phase | Signal | Example Symptom |
|------|-------|--------|----------------|
| Eye | Doorway | `wisdom_strain` | Too much research, no action |
| Side | Gift | `fate_strain` | Over-planning, under-executing |
| Hand | Forge | `chaos_strain` | Excess experimentation |
| Foot | Measure | `tide_strain` | Missed deadlines |
| Throat | Voice | `place_strain` | Wrong audience / context |
| Heart | Watch | `watch_strain` | Decision fatigue |
| 7-9 | Reserved | `system_strain` | Infra capacity pressure |

**Ragnarok protocol:** Any wound > 0.8 triggers graceful degradation. (Packs may theme this as a diegetic reset, but the action is a controlled rollback.)

---

## 7. Tool Ownership (Delegation Map)

Tools are owned by specific roles for accountability.

| Role | Tool |
|------|------|
| Orange: LLM Router | `route-66` |
| Orange: Provider Balancer | `route-66 pumps` |
| Orange: Fallback Handler | `route-66 transmission` |
| Red: Knowledge Architect | `world` |
| Red: Data Miner | `Vitalsource2pdf` |
| Yellow: Code Generator | `Jokebook` (creative), dev tools |
| Blue: Voice of the Council | `Caesar Core` |
| Purple: Emotional Resonance Analyst | `DeepLove` |
| Green: Token Counter | `ops-telemetry-monitor` |

---

## 8. Security Constraints (Shared Auth Modules)

Agent tooling and permission checks must align with shared security modules to keep hub policy consistent across products.

- **Auth modules:** `auth-core`, `auth-rbac`, `auth-apikeys`, `auth-contracts`
- **Contracts:** Schemas live under `auth-contracts/v1` and are versioned; schema changes require a new version.
- **Rules:** No app-specific logic inside shared modules; storage adapters are injectable; contracts are the single source of truth.

**Implication for agents:** Tool ownership and escalation decisions must flow through RBAC evaluation and contract schemas, not ad-hoc checks.

---

## 9. Times Square Slice: Minimal Viable Use

For the Times Square slice, the hierarchy is used as a controlled stress-test:

- **NPC bounded rationality:** Persona anchors apply without expanding recursion depth.
- **IoT integration:** Stanza rules gate sensor input and output.
- **No hub bleed:** Pack-specific flavor is allowed only after translation gates.

---

## 10. Optional Diegetic Expansion Tags (Non-Blocking)

Universe packs may add mythic labels for narrative flavor, but these are optional and non-authoritative. They must never override stanza or guardrail rules.

Examples:
- Totems as "admin clusters" for superuser ethics.
- Ragnarok protocol themed as a mythic reset.

---

## 11. Implementation Checklist

1. Bind stanza rules into prompt templates and agent runtime checks.
2. Enforce recursion tier caps in Earth-1218 configs.
3. Implement crystallization gate for all permanent writes.
4. Emit strain metrics into Heat channels for monitoring.
5. Add role-to-tool ownership mapping in telemetry.
6. Route tool access through shared auth modules and contract schemas.

---

## 12. Open Questions

- Should strain metrics map 1:1 to Heat channels, or remain a parallel diagnostic?
- What is the exact recursion cap for the Times Square slice (2, 3, or 4 tiers)?

