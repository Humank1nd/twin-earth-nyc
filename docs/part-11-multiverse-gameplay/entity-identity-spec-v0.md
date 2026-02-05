# Entity Identity Spec v0

> **Twin Earth NYC** -- Part 11: Multiverse Gameplay
> **Document:** Entity Identity Specification
> **Version:** 0.1.0
> **Status:** Draft
> **Last Updated:** 2026-01-27

---

## Overview

The Entity Identity System prevents multiverse imports from breaking Earth-1218 realism.
It defines immutable canonical identities, instance variants, and deterministic overlap rules
that drive portal gating, ledger logging, and Heat escalation.

Design goals:
- Maintain hub sacredness (Earth-1218 remains baseline reality).
- Allow modular universe packs without identity power creep.
- Provide deterministic, testable rules for variant collisions.

---

## Identity Objects

### Canonical Identity (Cross-Reality Essence)

Immutable essence shared across all variants.

Format:
```
CAN-[ARCHETYPE]-[HASH]
```

Fields:
- `canonical_id` (string): global, immutable ID.
- `archetype` (string): human-readable concept.
- `traits` (list): fixed traits shared across variants.
- `baseline` (object): optional fixed traits or constraints.

### Instance Identity (Variant-Specific)

Timeline-bound realization of a canonical identity.

Format:
```
INST-[CANONICAL_ID]-[TIMELINE_ID]-[DIVERGENCE_HASH]
```

Fields:
- `instance_id` (string): unique per variant.
- `canonical_id` (string): parent canonical.
- `timeline_id` (string): origin timeline.
- `traits` (list): active traits for this variant.
- `history` (list): key events for overlap scoring.
- `deltas` (object): divergences from baseline.

---

## Overlap Scoring (Collision Detection)

Overlap is computed deterministically for two variants:

```
overlap_score = (traits * 0.6) + (history * 0.3) + (proximity * 0.1)
```

Where:
- `traits`: shared traits normalized by max trait count.
- `history`: shared history events normalized by max history count.
- `proximity`: linear falloff to 0 at 1000m.

### Verdicts

| Score | Verdict | Action |
| --- | --- | --- |
| < 0.4 | PASS | Allow interaction |
| 0.4 - 0.7 | WARN | Quarantine or conditions |
| > 0.7 | BLOCK | Force fork, extract, or deny |

---

## Portal Decay

Cross-realm imports reduce overlap to simulate instability:

```
decayed_score = max(0, overlap_score - (0.2 * hops))
```

This prevents imported duplicates from dominating Earth-1218 and supports
safe anomaly tests in the Times Square slice.

---

## Integration Notes

- **Translation Gate:** low compatibility items still cross, but high identity overlap
  raises Heat and evidence risk.
- **Trust Ledger:** every fork, duplicate, or pruning action is logged as a ledger event.
- **Heat Channels:** overlap > 0.7 spikes Social and Institutional Heat; repeated WARN
  events slowly raise Ecological Heat due to reality stress.

---

## Per-Channel Heat Bounds (Upper Limits)

Upper bounds constrain heat escalation per channel to prevent hub creep while still
allowing visible anomalies. WARN ranges cap contained events; BLOCK thresholds allow
escalations when identity collisions are severe.

| Channel | WARN Range | BLOCK Threshold | Notes |
| --- | --- | --- | --- |
| Ecological | 0.05 - 0.10 | > 0.10 | Reality-warp risk (Wanda/Aether) |
| Institutional | 0.04 - 0.08 | > 0.08 | Authority disruption (TVA/Loki) |
| Social | 0.03 - 0.07 | > 0.07 | Witness confusion (Spider-Man) |
| Physical | 0.06 - 0.12 | > 0.12 | Matter conflict (Jotunheim cap) |

Note: Physical Heat remains near zero in current probes; ranges are defined for future
scenarios where matter conflicts are simulated.

---

## MCU Example: Spider-Man (Peter Parker)

Canonical:
```
{
  "canonical_id": "CAN-PETER-PARKER-acc5298d",
  "traits": ["Web-Slinging", "Spider-Sense", "Super Strength", "Inventor"]
}
```

Instances:
```
{
  "instance_id": "INST-CAN-PETER-PARKER-acc5298d-TL-616-97928732",
  "deltas": {"age": "teen", "mentor": "tony-stark"},
  "history": ["uncle-ben", "avengers", "no-way-home"]
}
{
  "instance_id": "INST-CAN-PETER-PARKER-acc5298d-TL-96283-93bb8ec7",
  "deltas": {"age": "adult", "organic_webs": true},
  "history": ["uncle-ben", "green-goblin", "no-way-home"]
}
```

Base overlap (no decay) is typically > 0.7 (BLOCK). After 2 portal hops,
score decays below 0.4 (PASS), enabling a safe Times Square anomaly test.

---

## MCU Example: Wanda Maximoff (Scarlet Witch)

Canonical:
```
{
  "canonical_id": "CAN-WANDA-MAXIMOFF-1f2g3h4i",
  "traits": ["Chaos Magic", "Telekinesis", "Mind Manipulation", "Reality Warping"]
}
```

Instances:
```
{
  "instance_id": "INST-CAN-WANDA-MAXIMOFF-1f2g3h4i-TL-616-5j6k7l8m",
  "deltas": {"power_amp": "Darkhold", "family_loss": true},
  "history": ["ultron", "vision", "westview", "darkhold"]
}
{
  "instance_id": "INST-CAN-WANDA-MAXIMOFF-1f2g3h4i-TL-838-9n0p1q2r",
  "deltas": {"power_amp": "Illuminati", "children_alive": true},
  "history": ["ultron", "vision", "westview", "illuminati"]
}
```

Example overlap (distance ~100m):
- traits overlap ~0.8, history overlap ~0.75, proximity ~0.9 -> raw score ~0.80 (BLOCK)
- after 2 portal hops: decayed ~0.40 (PASS)
- Heat emphasis: ecological channel spikes higher due to reality-warp risk

---

## MCU Example: Loki Laufeyson

Canonical:
```
{
  "canonical_id": "CAN-LOKI-LAUFYSON-4p5q6r7s",
  "traits": ["Illusion Mastery", "Shape-Shifting", "Deception", "Asgardian Physiology"]
}
```

Instances:
```
{
  "instance_id": "INST-CAN-LOKI-LAUFYSON-4p5q6r7s-TL-616-8t9u0v1w",
  "deltas": {"alliance": "thanos", "death_count": 1},
  "history": ["odin", "thor", "avengers", "ragnarok"]
}
{
  "instance_id": "INST-CAN-LOKI-LAUFYSON-4p5q6r7s-TL-sacred-2x3y4z5a",
  "deltas": {"tva_escape": true, "variant_status": "pruned"},
  "history": ["odin", "thor", "avengers", "tva"]
}
{
  "instance_id": "INST-CAN-LOKI-LAUFYSON-4p5q6r7s-TL-classic-6b7c8d9e",
  "deltas": {"isolation": true, "power_amp": "classic"},
  "history": ["odin", "thor", "ragnarok", "isolation"]
}
```

Pruning rule example:
- overlap > 0.9 triggers BLOCK (auto-prune / extraction; ledger event recorded)
- after 2 portal hops: decayed ~0.5 (WARN)
- Heat emphasis: institutional channel spikes due to authority pursuit

---

## Times Square Slice Test

Scenario: two Spider-Man variants emerge within 50m in Times Square.

Expected behavior:
- Overlap score > 0.7 triggers BLOCK.
- Translation Gate applies decay per hop on import.
- Trust Ledger records fork and pruning events.
- Social + Institutional Heat spikes immediately; Ecological Heat rises
  if repeated overlaps occur.

---

*End of document.*
