# Scoring Function Spec v0

**Document:** Twin Earth NYC — Part 5, Deliverable 4
**Status:** v0 Draft
**Last Updated:** 2026-01-27
**Depends On:** Scenario Evaluation Suite v0, Constraint Test Suite v0, Evolvable Parameter Registry v0

---

## 1. Purpose

The Scoring Function converts raw scenario telemetry into a single scalar score for each candidate configuration. This score is the sole input to evolutionary selection. The function is designed to:

1. **Reward** performance, plausibility, and consistency simultaneously.
2. **Prevent overfitting** to any single scenario.
3. **Enforce hard constraints** that no amount of good scoring can override.
4. **Encourage diversity** in the candidate population.

---

## 2. Hard Constraints (Pre-Scoring Gates)

Before any scoring occurs, the following hard constraints must be satisfied. Failure on any gate means the candidate receives a score of **0.0** and is discarded.

| Gate | Condition | Source |
|------|-----------|--------|
| G-01 | All constraint tests pass (CT-01 through CT-10) | Constraint Test Suite v0 |
| G-02 | No scenario drops below 20 FPS at any point (`min_fps_absolute` >= 20) | Scenario telemetry |
| G-03 | No ledger corruption detected in any scenario | Ledger telemetry |
| G-04 | All parameter values within registry bounds | Evolvable Parameter Registry v0 |
| G-05 | Rate limit respected (no param changed > 20% from parent) | Constraint Test Suite v0, Section 4.1 |

```python
def hard_constraint_check(candidate, constraint_results, scenario_results):
    """
    Returns True only if ALL hard constraints are satisfied.
    Any failure -> score = 0.0, candidate discarded.
    """
    # G-01: All constraint tests pass
    if not constraint_results.all_pass:
        return False

    # G-02: No scenario drops below 20 FPS at any point
    for scenario in scenario_results:
        if scenario.min_fps_absolute < 20.0:
            return False

    # G-03: No ledger corruption
    for scenario in scenario_results:
        if scenario.ledger.corruption_detected:
            return False

    # G-04: All params in bounds
    if not bounds_check(candidate.config, registry):
        return False

    # G-05: Rate limit
    if not rate_limit_check(candidate.config, candidate.parent_config):
        return False

    return True
```

---

## 3. Metric Definitions

### 3.1 Performance Score (0.0 -- 1.0)

Measures how well the simulation runs from a technical standpoint: frame rate and memory.

```
performance_score =
    0.3 * clamp(avg_fps / 60.0, 0.0, 1.0)
  + 0.4 * clamp(min_fps_1pct / 30.0, 0.0, 1.0)
  + 0.3 * clamp(1.0 - (mem_spike_gb / 6.0), 0.0, 1.0)
```

| Component | Weight | Numerator | Denominator | Interpretation |
|-----------|--------|-----------|-------------|----------------|
| Average FPS | 0.3 | `avg_fps` | 60.0 | Score of 1.0 at 60 FPS or above |
| Minimum FPS (1st percentile) | 0.4 | `min_fps_1pct` | 30.0 | Score of 1.0 at 30 FPS or above. Heaviest weight because frame drops are the most noticeable. |
| Memory headroom | 0.3 | `1.0 - mem_spike / 6.0` | -- | Score of 1.0 when peak memory = 0 GB (unrealistic); score of 0.0 at 6 GB (hard cap). Linear interpolation. |

**Where:**
- `avg_fps` = average frames per second across the full scenario run.
- `min_fps_1pct` = 1st percentile FPS (the FPS exceeded 99% of the time).
- `mem_spike_gb` = max(vram_peak_gb, ram_peak_gb / 2) — a combined memory pressure metric. RAM is halved because VRAM is the tighter constraint.

**Example calculation:**
```
avg_fps = 52.0   -> component = 0.3 * min(52/60, 1.0) = 0.3 * 0.867 = 0.260
min_fps  = 28.0  -> component = 0.4 * min(28/30, 1.0) = 0.4 * 0.933 = 0.373
mem_spike = 4.2  -> component = 0.3 * max(1 - 4.2/6, 0) = 0.3 * 0.300 = 0.090

performance_score = 0.260 + 0.373 + 0.090 = 0.723
```

---

### 3.2 Plausibility Score (0.0 -- 1.0)

Measures how believable and correct the simulation behaves. Covers crowd behavior, traffic flow, and evidence generation.

```
plausibility_score =
    0.3 * clamp(1.0 - deadlock_rate, 0.0, 1.0)
  + 0.2 * clamp(traffic_flow_score, 0.0, 1.0)
  + 0.2 * clamp(crowd_smoothness, 0.0, 1.0)
  + 0.3 * clamp(evidence_rate_score, 0.0, 1.0)
```

| Component | Weight | Computation | Interpretation |
|-----------|--------|-------------|----------------|
| Deadlock-free | 0.3 | `1.0 - (deadlock_count / max_tolerable_deadlocks)` | 1.0 = no deadlocks; 0.0 = max_tolerable_deadlocks or more |
| Traffic flow | 0.2 | See Section 3.2.1 | Smooth, realistic traffic movement |
| Crowd smoothness | 0.2 | See Section 3.2.2 | Natural-looking crowd flow |
| Evidence generation | 0.3 | See Section 3.2.3 | Adequate evidence for investigation |

#### 3.2.1 Traffic Flow Score

```python
def traffic_flow_score(scenario):
    """
    Measures traffic flow quality.
    1.0 = all vehicles move smoothly through intersections.
    0.0 = complete gridlock.
    """
    # Average vehicle speed as fraction of expected free-flow speed
    speed_ratio = clamp(avg_vehicle_speed / expected_free_flow_speed, 0.0, 1.0)

    # Fraction of intersections without gridlock
    clear_intersections = intersections_without_gridlock / total_intersections

    # Penalty for vehicle collision events
    collision_penalty = clamp(vehicle_collisions / 10.0, 0.0, 1.0)

    return 0.4 * speed_ratio + 0.4 * clear_intersections + 0.2 * (1.0 - collision_penalty)
```

#### 3.2.2 Crowd Smoothness Score

```python
def crowd_smoothness(scenario):
    """
    Measures crowd movement quality.
    1.0 = smooth, natural pedestrian flow.
    0.0 = constant collisions, jittering, unnatural movement.
    """
    # Average NPC velocity smoothness (low jitter = smooth)
    velocity_smoothness = clamp(1.0 - avg_velocity_jitter / max_jitter, 0.0, 1.0)

    # Fraction of NPCs that reached their destination without incident
    completion_ratio = npcs_completed / npcs_spawned

    # Penalty for teleport incidents (strong signal of broken navigation)
    teleport_penalty = clamp(teleport_incidents / 5.0, 0.0, 1.0)

    return 0.4 * velocity_smoothness + 0.4 * completion_ratio + 0.2 * (1.0 - teleport_penalty)
```

#### 3.2.3 Evidence Rate Score

```python
def evidence_rate_score(scenario):
    """
    Measures whether evidence generation keeps pace with events.
    1.0 = robust evidence flow.
    0.0 = no evidence being generated.
    """
    if scenario.has_active_incident:
        # During incidents, evidence rate must be high
        rate = scenario.evidence_events_per_sec_during_incident
        return clamp(rate / 2.0, 0.0, 1.0)  # 2.0 events/sec = perfect
    else:
        # During normal operations, baseline evidence is sufficient
        rate = scenario.evidence_events_per_sec
        return clamp(rate / 0.5, 0.0, 1.0)  # 0.5 events/sec = adequate
```

**Max tolerable deadlocks per scenario:**

| Scenario | `max_tolerable_deadlocks` |
|----------|--------------------------|
| BASELINE_MIDDAY | 3 |
| RAINY_NIGHT | 3 |
| POLICE_PURSUIT | 5 |
| CROWD_SURGE | 10 |
| ANOMALY_PORTAL | 5 |

---

### 3.3 Consistency Score (0.0 -- 1.0)

Measures determinism, ledger integrity, and spatial stability.

```
consistency_score =
    0.3 * clamp(1.0 - anchor_drift_norm, 0.0, 1.0)
  + 0.4 * clamp(replay_match_score, 0.0, 1.0)
  + 0.3 * clamp(ledger_continuity, 0.0, 1.0)
```

| Component | Weight | Computation | Interpretation |
|-----------|--------|-------------|----------------|
| Anchor stability | 0.3 | `1.0 - (max_drift_m / 1.0)` | 1.0 = zero drift; 0.0 = drift at discard threshold |
| Replay match | 0.4 | See Section 3.3.1 | Deterministic replay fidelity |
| Ledger continuity | 0.3 | See Section 3.3.2 | Unbroken ledger commit chain |

#### 3.3.1 Replay Match Score

```python
def replay_match_score(scenario):
    """
    Measures replay fidelity.
    1.0 = perfect replay match.
    0.0 = complete replay divergence.
    """
    if scenario.replay_check == "PASS":
        return 1.0
    elif scenario.replay_check == "PARTIAL":
        # Partial match: some entities diverged
        return clamp(1.0 - (divergent_entities / total_entities), 0.0, 1.0)
    else:
        return 0.0
```

#### 3.3.2 Ledger Continuity

```python
def ledger_continuity(scenario):
    """
    Measures whether the ledger maintained an unbroken commit chain.
    1.0 = all commits sequential, no gaps, no corruption.
    0.0 = ledger is broken.
    """
    if scenario.ledger.corruption_detected:
        return 0.0  # Hard constraint should have caught this

    gap_count = scenario.ledger.commit_gaps
    expected_commits = scenario.duration_sec / scenario.commit_interval

    return clamp(1.0 - (gap_count / expected_commits), 0.0, 1.0)
```

---

## 4. Aggregation

### 4.1 Per-Scenario Composite

```
scenario_score = 0.4 * performance_score + 0.3 * plausibility_score + 0.3 * consistency_score
```

This weighting reflects the priority order: the game must run well (performance), look right (plausibility), and be trustworthy (consistency).

### 4.2 Overall Score

```
overall_score = MIN(scenario_scores[BASELINE_MIDDAY],
                    scenario_scores[RAINY_NIGHT],
                    scenario_scores[POLICE_PURSUIT],
                    scenario_scores[CROWD_SURGE],
                    scenario_scores[ANOMALY_PORTAL])
```

**Rationale:** The minimum function forces the optimizer to be robust across all conditions. A candidate that scores 0.95 on four scenarios but 0.40 on one scenario gets an overall score of 0.40. This prevents specialization at the expense of general quality.

### 4.3 Full Scoring Pipeline

```python
def score_candidate(candidate, constraint_results, scenario_results):
    """
    Full scoring pipeline for one candidate.
    Returns overall_score in [0.0, 1.0] or 0.0 if hard constraints fail.
    """
    # Step 1: Hard constraint gate
    if not hard_constraint_check(candidate, constraint_results, scenario_results):
        return 0.0

    # Step 2: Score each scenario
    scenario_scores = {}
    for scenario in scenario_results:
        perf = performance_score(scenario)
        plaus = plausibility_score(scenario)
        consist = consistency_score(scenario)
        composite = 0.4 * perf + 0.3 * plaus + 0.3 * consist
        scenario_scores[scenario.id] = {
            "performance": perf,
            "plausibility": plaus,
            "consistency": consist,
            "composite": composite
        }

    # Step 3: Overall = minimum across scenarios
    overall = min(s["composite"] for s in scenario_scores.values())

    # Step 4: Diversity bonus (see Section 5)
    diversity = diversity_bonus(candidate)
    overall = min(overall + diversity, 1.0)  # Cap at 1.0

    return overall, scenario_scores
```

---

## 5. Anti-Overfitting Measures

### 5.1 Minimum-Across-Scenarios

As described in Section 4.2, the overall score is the minimum scenario score. This is the primary anti-overfitting mechanism. A candidate cannot compensate for weakness in one scenario by excelling in another.

### 5.2 Holdout Scenario

The **RANDOM_STRESS** scenario (seed=9999) is never used during evolutionary scoring. It is run only during promotion review.

| Property | Value |
|----------|-------|
| Scenario ID | RANDOM_STRESS |
| Seed | 9999 |
| Duration | 600 seconds (10 minutes) |
| Weather | Random: cycles through clear, rain, fog at random intervals |
| Crowd | Random surges at unpredictable times |
| Incidents | Random: pursuits, anomalies, or none, injected at random times |
| Traffic | Variable density |

**Holdout pass threshold:** The candidate's holdout score must be within 15% of its training score (overall score from the 5 evaluation scenarios). If the holdout score drops by more than 15%, the candidate is suspected of overfitting and is rejected from promotion.

```python
def holdout_check(training_score, holdout_score):
    """
    Returns True if candidate is not overfitting.
    """
    if holdout_score < training_score * 0.85:
        return False  # Overfitting detected
    return True
```

### 5.3 Parameter Diversity Bonus

To prevent the population from converging on a single configuration too quickly, a diversity bonus is applied.

```python
def diversity_bonus(candidate, top_3_candidates):
    """
    Awards +0.05 if the candidate differs from ALL top-3 candidates
    by more than 10% on at least one parameter axis.
    """
    for top_candidate in top_3_candidates:
        is_different = False
        for param_id in candidate.config:
            old_val = top_candidate.config[param_id]
            new_val = candidate.config[param_id]
            if old_val == 0:
                continue
            if abs(new_val - old_val) / abs(old_val) > 0.10:
                is_different = True
                break
        if not is_different:
            return 0.0  # Too similar to at least one top candidate

    return 0.05  # Different from all top-3
```

**Rationale:** The diversity bonus is small (0.05) relative to typical score ranges (0.60-0.95), so it never overrides genuine quality differences. But it is enough to keep exploratory candidates alive in the population when the top performers are clustered.

### 5.4 Staleness Penalty

If a candidate's parameter values are identical to its grandparent (two generations back), it receives a staleness penalty of -0.02. This discourages the evolution from oscillating between two configurations.

```python
def staleness_penalty(candidate, grandparent):
    """
    Returns -0.02 if candidate is identical to grandparent.
    """
    if candidate.config == grandparent.config:
        return -0.02
    return 0.0
```

---

## 6. Score Reporting

### 6.1 Per-Candidate Score Record

```json
{
  "candidate_id": "gen47_candidate_03",
  "generation": 47,
  "timestamp": "2026-01-27T14:45:00Z",
  "config_hash": "a7f3c2e9...",
  "hard_constraints": "PASS",
  "scenario_scores": {
    "BASELINE_MIDDAY": {
      "performance": 0.87,
      "plausibility": 0.91,
      "consistency": 0.95,
      "composite": 0.906
    },
    "RAINY_NIGHT": {
      "performance": 0.78,
      "plausibility": 0.85,
      "consistency": 0.93,
      "composite": 0.846
    },
    "POLICE_PURSUIT": {
      "performance": 0.82,
      "plausibility": 0.88,
      "consistency": 0.94,
      "composite": 0.874
    },
    "CROWD_SURGE": {
      "performance": 0.71,
      "plausibility": 0.79,
      "consistency": 0.92,
      "composite": 0.797
    },
    "ANOMALY_PORTAL": {
      "performance": 0.76,
      "plausibility": 0.83,
      "consistency": 0.91,
      "composite": 0.827
    }
  },
  "overall_score": 0.797,
  "bottleneck_scenario": "CROWD_SURGE",
  "diversity_bonus": 0.05,
  "staleness_penalty": 0.0,
  "final_score": 0.847
}
```

### 6.2 Generation Summary Record

```json
{
  "generation": 47,
  "timestamp": "2026-01-27T14:50:00Z",
  "candidates_evaluated": 10,
  "candidates_discarded": 3,
  "candidates_scored": 7,
  "best_score": 0.847,
  "best_candidate": "gen47_candidate_03",
  "worst_score": 0.612,
  "mean_score": 0.734,
  "score_std_dev": 0.078,
  "improvement_over_previous": 0.012,
  "constraint_failures": {
    "CT-03": 2,
    "CT-08": 1
  },
  "promoted": false,
  "notes": "Crowd surge remains bottleneck. Candidate 03 improved traffic flow."
}
```

---

## 7. Baseline Dashboard

The baseline dashboard tracks evolution progress across generations.

### 7.1 Dashboard Table

| Gen# | Overall Score | Perf | Plaus | Consist | Constraints | Bottleneck | Notes |
|------|---------------|------|-------|---------|-------------|------------|-------|
| gen0 | (baseline) | TBD | TBD | TBD | PASS | TBD | Initial hand-tuned parameters (Bundle C) |
| gen1 | -- | -- | -- | -- | -- | -- | First evolved generation |
| gen2 | -- | -- | -- | -- | -- | -- | |
| ... | | | | | | | |
| genN | -- | -- | -- | -- | -- | -- | Latest generation |

### 7.2 Dashboard Metrics (Live)

| Metric | Value | Trend |
|--------|-------|-------|
| Current Generation | 0 | -- |
| Best Overall Score | TBD | -- |
| Best Candidate | -- | -- |
| Consecutive Improvements | 0 | -- |
| Consecutive Plateaus | 0 | -- |
| Consecutive Rollbacks | 0 | -- |
| Population Diversity Index | TBD | -- |
| Constraint Pass Rate | TBD | -- |
| Holdout Score (last check) | TBD | -- |

### 7.3 Visualization Targets

The following charts should be generated and updated each generation:

1. **Score over generations:** Line plot of best, mean, and worst scores per generation.
2. **Component breakdown:** Stacked area chart of performance, plausibility, consistency contributions.
3. **Scenario heatmap:** 5-column heatmap (one per scenario) showing composite score per generation.
4. **Parameter drift:** Line plots of each parameter value in the best candidate over generations.
5. **Constraint failures:** Bar chart of constraint test failure counts per generation.
6. **Diversity index:** Line plot of population diversity over generations.

---

## 8. Tuning Notes

### 8.1 Weight Sensitivity

The scoring weights (0.4/0.3/0.3 for perf/plaus/consist) are initial values. They may be adjusted between evolution runs but must remain fixed within a single evolution run. Any weight change resets the generation counter and invalidates previous scores.

### 8.2 Threshold Sensitivity

The following thresholds are particularly sensitive and should be reviewed if scoring produces unexpected results:

| Threshold | Current Value | Sensitivity |
|-----------|---------------|-------------|
| FPS target for perf score of 1.0 | 60 FPS | High — lowering this is equivalent to lowering the performance bar |
| Min FPS for perf score of 1.0 | 30 FPS | High — this is the "acceptable" minimum |
| Memory cap | 6 GB | Medium — hardware-dependent |
| Evidence rate target | 2.0 events/sec | Medium — affects investigation pacing |
| Holdout tolerance | 15% | High — tighter = more candidates rejected, looser = more overfitting |
| Diversity bonus | +0.05 | Low — small enough to not dominate, large enough to matter |

### 8.3 Score Range Expectations

Based on the metric definitions, expected score ranges are:

| Condition | Expected Overall Score |
|-----------|----------------------|
| Excellent candidate (all scenarios strong) | 0.85 -- 0.95 |
| Good candidate (minor weaknesses) | 0.70 -- 0.85 |
| Acceptable candidate (one weak scenario) | 0.55 -- 0.70 |
| Poor candidate (multiple weak scenarios) | 0.30 -- 0.55 |
| Failing candidate (hard constraint failure) | 0.0 |

---

*End of Scoring Function Spec v0.*
