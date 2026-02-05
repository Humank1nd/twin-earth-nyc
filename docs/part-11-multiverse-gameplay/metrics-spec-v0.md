# Metrics Spec v0

> **Twin Earth NYC** — Part 11: Multiverse Gameplay  
> **Document:** Metrics Specification  
> **Version:** 0.1.0  
> **Status:** Draft  
> **Last Updated:** 2026-01-29

---

## Overview

AlphaEvolve adapters pull runtime metrics for optimization and diagnostics. Metrics
follow a strict source hierarchy to preserve hub sacredness and maintain deterministic
fallbacks during development.

---

## Adapter Source Hierarchy

1. **HTTP** — `AXE_METRICS_URL` (default: `/world/life/metrics`)
2. **MCP** — Unreal MCP client `get_simulation_metrics`
3. **Mock** — local heuristics when real data is unavailable

Set `AXE_SIM_METRICS_MODE=mock` to force mock behavior in dev tests.

---

## Metrics Exposed

- **deadlock_rate** — derived from `idle_agents / agent_count` if not provided.
- **fps / avg_fps** — read from metrics payload if present; fallback heuristic otherwise.
- **source metadata** — `http | mcp | mock` recorded alongside values.

---

## Diagnostics Endpoints

**/health/metrics** (DEBUG‑only) returns:
```json
{
  "deadlock_rate": 0.05,
  "source_deadlocks": "http",
  "fps": 62.5,
  "source_fps": "mcp",
  "timestamp": "2026-01-28T00:00:00Z"
}
```

**/health/detailed** includes a `probes.metrics` snapshot when DEBUG.

**/health/test-multi-adapter** (DEBUG‑only) runs weighted adapter probes and can
append a fitness ledger entry when `emit_ledger=true`.

It returns:
- `weighted_fitness` — weighted average of adapter fitness values.
- `fitness_components` — per-adapter fitness values keyed by adapter name.
- `raw_metrics` — per-adapter metrics payloads (includes source metadata).
- `verdict` — PASS/WARN/BLOCK based on weighted fitness bounds.
- `weights` and `adapters` — the applied weight list and adapter order.

Bounds:
- `WARN` if `weighted_fitness` > 1.0 (over‑amplified)
- `BLOCK` if `weighted_fitness` < 0.5 (under‑performing)

---

## Handshake Flow

The Yggdrasil Bridge WebSocket transport expects a HELLO/READY handshake before
SUBSCRIBE_EVENTS or other commands are sent.

Example subscribe payload (after READY):
```json
{
  "msg_type": "SUBSCRIBE_EVENTS",
  "payload": {"branch_id": "sacred", "from_event_idx": 0},
  "msg_id": "uuid-5678",
  "timestamp": 1700000001.0,
  "role": "OBSERVER",
  "protocol_version": "0.1.0"
}
```

---

## Mixed Test Endpoint

**/health/test-mixed** (DEBUG‑only) returns compounded Heat/prune for multi‑entity
transits.

It returns:
- `mixed_emitted` — true if a mixed-transit prune event was emitted.
- `compounded_heat` — total Heat impact summed across all entities and channels.
- `schema_valid` — true if all emitted messages pass schema validation.

Diegetic Idea: **Convergence** as a multi‑realm vulnerability allowing cross-realm alignment stress.

---

## CI Coverage

Health endpoint tests include the multi-adapter probe and adapter source hierarchy.
These run in `schema-validation.yml` to guard regressions in weighted metrics and
ledger emissions.

Doc date checks run in CI with a check-only pass (no auto-rewrite) to enforce
manual timestamp updates for Part 11 indexes.

Failures include a summary of stale entries with current vs computed dates for
quick remediation.

---

## CLI Example

```bash
python scripts/alphaevolve_cli_wrapper.py \
  --multi-adapter "twin_earth.sim_adapters.omniverse_metrics:omniverse_crowd_deadlocks,twin_earth.sim_adapters.fps_stability:fps_stability" \
  --weights "0.7,0.3" \
  --emit-ledger
```

---

## Diegetic Note

Metrics act as “Heimdall telemetry”: a limited, redacted signal that preserves hub
reality while enabling controlled optimization in pocket packs.

---

## Evolvable Parameters (MCU Enhanced)

Parameters available for AlphaEvolve optimization, tagged with MCU analogies for diegetic context.

| Parameter | ID | Description | MCU Analogy | Bounds |
|---|---|---|---|---|
| **slew_rate_max_delta_down** | `P-01` | Rate at which a value can decay | **Odinforce cooldown** (Power recharge rate) | 0.1 - 0.9 |
| **max_governed_cost** | `P-02` | Computational cost cap | **Reality Stone limit** (Maximum distortion allowed) | 100 - 1000 ops |
| **convergence_threshold** | `P-03` | Error margin for stability | **Convergence alignment** (Planetary alignment precision) | 0.01 - 0.1 |
| **traffic_signal_green** | `T-01` | Duration of green light | **Bifrost open duration** | 15.0 - 90.0s |

---

## Evolvable Self-Improvement (Meta-Metrics)

Metrics used by AlphaEvolve to monitor and refine its own optimization performance.

| Metric | ID | Description | MCU Diegetic Tag |
|---|---|---|---|
| **mutation_rate** | `META-01` | Probability of random jitter | **Odinforce Recharge** (Kernel cooldown) |
| **selection_bias** | `META-02` | Score vs Diversity weighting | **Heimdall Choice** (Priority routing) |

---

*End of document.*
