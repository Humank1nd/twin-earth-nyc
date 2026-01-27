# AlphaEvolve Ops Playbook v0

**Document:** Twin Earth NYC — Part 5, Deliverable 5
**Status:** v0 Draft
**Last Updated:** 2026-01-27
**Depends On:** Evolvable Parameter Registry v0, Constraint Test Suite v0, Scenario Evaluation Suite v0, Scoring Function Spec v0

---

## 1. Purpose

This playbook defines the complete operational procedure for running AlphaEvolve: the evolutionary optimization loop that tunes Twin Earth NYC's runtime parameters. It covers the generation loop, mutation operators, selection rules, rollback procedures, human-in-the-loop checkpoints, and the promotion pipeline from sandbox to canonical configuration.

This is the operator's manual. Follow it exactly.

---

## 2. Generation Process

### 2.1 Population Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Population size | 10 candidates per generation | Small enough for fast iteration, large enough for diversity |
| Survivors per generation | 3 | Top 2 by score + 1 diversity pick |
| Children per generation | 7 | Fill remaining slots via mutation and crossover |
| Elitism count | 1 | Top performer survives unchanged |
| Max generations | 100 | Hard cap; manual extension requires operator approval |

### 2.2 Generation Loop

Each generation executes the following steps in strict order:

```
GENERATION LOOP (gen = 0, 1, 2, ... , max_gen):

    1. GENERATE candidates
       - If gen == 0: seed population from Bundle A, Bundle B, Bundle C,
         and 7 random perturbations of Bundle C
       - If gen > 0: apply selection, then mutation/crossover to produce
         10 new candidates

    2. VALIDATE candidates (pre-evaluation)
       - Bounds check against Evolvable Parameter Registry
       - Rate limit check (no param changed > 20% from parent)
       - Dependency constraint enforcement (clamp or discard)
       - Replace invalid candidates with fresh mutations from survivors

    3. EVALUATE candidates
       - Run Constraint Test Suite (10 tests, fail = discard)
       - For surviving candidates: run all 5 evaluation scenarios
       - Collect telemetry

    4. SCORE candidates
       - Compute performance, plausibility, consistency per scenario
       - Compute overall score = MIN across scenarios
       - Apply diversity bonus and staleness penalty

    5. SELECT survivors
       - Sort by final score descending
       - Keep top 2 (by score)
       - Keep 1 diversity pick (most different from top 2)
       - Discard remaining 7

    6. CHECK stopping conditions
       - If met: exit loop
       - If not: increment gen, go to step 1

    7. LOG generation results
       - Record all scores, constraint results, telemetry
       - Update dashboard
       - Archive best candidate config
```

### 2.3 Generation Zero (Initialization)

The first generation is special. It establishes the baseline.

| Slot | Source | Description |
|------|--------|-------------|
| Candidate 0 | Bundle A | Performance-first configuration |
| Candidate 1 | Bundle B | Plausibility-first configuration |
| Candidate 2 | Bundle C | Balanced configuration (default) |
| Candidate 3 | Bundle C + small jitter | Random +-5% perturbation of Bundle C |
| Candidate 4 | Bundle C + small jitter | Different random seed |
| Candidate 5 | Bundle C + small jitter | Different random seed |
| Candidate 6 | Bundle C + medium jitter | Random +-15% perturbation of Bundle C |
| Candidate 7 | Bundle C + medium jitter | Different random seed |
| Candidate 8 | Bundle A/C crossover | Uniform crossover between A and C |
| Candidate 9 | Bundle B/C crossover | Uniform crossover between B and C |

---

## 3. Mutation Operators

### 3.1 Mutation Types

| Operator | Magnitude | Probability | Description |
|----------|-----------|-------------|-------------|
| Small jitter | +/-5% per parameter | 80% | Fine-tuning near current values. Applied independently to each parameter. |
| Medium jitter | +/-15% per parameter | 15% | Moderate exploration. Still within the neighborhood of the parent. |
| Large exploration | +/-30% per parameter | 5% | Bold jumps to escape local optima. High risk, high reward. |

### 3.2 Mutation Procedure

```python
def mutate(parent_config, registry, rng):
    """
    Produce a child config by mutating the parent.
    Each parameter is independently mutated.
    """
    child = {}

    for param_id, value in parent_config.items():
        entry = registry[param_id]

        # Select mutation magnitude
        roll = rng.random()
        if roll < 0.80:
            magnitude = 0.05  # Small jitter
        elif roll < 0.95:
            magnitude = 0.15  # Medium jitter
        else:
            magnitude = 0.30  # Large exploration

        # Apply mutation
        delta = value * magnitude * rng.uniform(-1.0, 1.0)
        new_value = value + delta

        # Clamp to registry bounds
        new_value = max(entry.min, min(entry.max, new_value))

        # Enforce rate limit (max 20% change from parent)
        max_delta = 0.20 * abs(value) if value != 0 else 0.20 * entry.max
        if abs(new_value - value) > max_delta:
            new_value = value + max_delta * (1.0 if new_value > value else -1.0)

        child[param_id] = new_value

    # Enforce dependency constraints (clamp)
    child = enforce_dependencies(child, registry)

    return child
```

### 3.3 Crossover Operator

```python
def crossover(parent_a, parent_b, rng):
    """
    Uniform crossover: each parameter has 50% chance
    of coming from either parent.
    """
    child = {}

    for param_id in parent_a:
        if rng.random() < 0.5:
            child[param_id] = parent_a[param_id]
        else:
            child[param_id] = parent_b[param_id]

    # Enforce dependency constraints (clamp)
    child = enforce_dependencies(child, registry)

    return child
```

### 3.4 Child Production (per generation)

From the 3 survivors, the 7 children are produced as follows:

| Child Slot | Method | Parents |
|------------|--------|---------|
| Child 0 | Elitism (copy) | Top performer (unchanged) |
| Child 1 | Mutation | Top performer |
| Child 2 | Mutation | Top performer |
| Child 3 | Mutation | Second performer |
| Child 4 | Mutation | Second performer |
| Child 5 | Crossover + Mutation | Top performer x Second performer |
| Child 6 | Crossover + Mutation | Top performer x Diversity pick |

Note: Child 0 is the elite copy. It is always included and never mutated. This ensures the best-known configuration always survives.

---

## 4. Selection

### 4.1 Selection Procedure

```python
def select_survivors(candidates, scored_results):
    """
    Select 3 survivors from the scored population.
    """
    # Sort by final score descending
    ranked = sorted(scored_results, key=lambda x: x.final_score, reverse=True)

    # Top 2 by score
    top_2 = ranked[:2]

    # Diversity pick: from remaining candidates, find the one
    # most different from top 2
    remaining = ranked[2:]
    diversity_pick = max(remaining, key=lambda c: min_distance(c, top_2))

    return top_2 + [diversity_pick]
```

### 4.2 Distance Metric for Diversity

```python
def min_distance(candidate, reference_set):
    """
    Compute the minimum normalized L2 distance between
    the candidate and any member of the reference set.
    """
    distances = []
    for ref in reference_set:
        dist = 0.0
        count = 0
        for param_id in candidate.config:
            c_val = candidate.config[param_id]
            r_val = ref.config[param_id]
            range_val = registry[param_id].max - registry[param_id].min
            if range_val > 0:
                dist += ((c_val - r_val) / range_val) ** 2
                count += 1
        if count > 0:
            dist = (dist / count) ** 0.5  # Normalized RMS distance
        distances.append(dist)
    return min(distances)
```

The diversity pick is the candidate that is maximally different from the nearest top-2 candidate. This prevents the population from collapsing to a single point in parameter space.

---

## 5. Stopping Conditions

The evolution loop halts when any of the following conditions is met:

| Condition | Threshold | Action |
|-----------|-----------|--------|
| Consistent constraint passes | All candidates pass constraints for 5 consecutive generations | Log "stable" status; continue unless another condition triggers |
| Score plateau | Best score improvement < 1% for 10 consecutive generations | HALT. Log plateau. Operator review required. |
| Manual stop | Operator issues stop command | HALT immediately. Archive current state. |
| Hard generation cap | Generation count reaches 100 | HALT. Log cap reached. Operator review required. |
| Emergency stop | 3 consecutive rollbacks | HALT. Full diagnostic required. See Section 8.4. |

### 5.1 Plateau Detection

```python
def check_plateau(generation_history, window=10, threshold=0.01):
    """
    Returns True if evolution has plateaued.
    """
    if len(generation_history) < window:
        return False

    recent = generation_history[-window:]
    best_scores = [gen.best_score for gen in recent]
    improvement = max(best_scores) - min(best_scores)

    return improvement < threshold
```

---

## 6. Human-in-the-Loop

### 6.1 Manual Veto Triggers

A human operator may veto any candidate at any time. Specific triggers that should prompt manual review:

| Trigger | Description | Severity |
|---------|-------------|----------|
| Visual artifacts | Reviewer observes visual glitches, pop-in, or unnatural behavior in captured video/screenshots | HIGH — veto candidate |
| Narrative break | NPC behavior contradicts established narrative rules (e.g., police ignoring crime, crowds walking through anomaly) | HIGH — veto candidate |
| Systemic exploit | A parameter combination creates an exploitable game state (e.g., infinite evidence from trivial action) | CRITICAL — veto + investigate |
| Performance regression on holdout | Holdout score drops > 15% from training score | MEDIUM — block promotion |
| Population collapse | All surviving candidates have < 5% normalized distance from each other | MEDIUM — inject diversity manually |

### 6.2 Approval-to-Promote Rule

No candidate may be promoted from sandbox to canonical config without satisfying ALL of the following:

1. **All constraint tests pass** (CT-01 through CT-10).
2. **All 5 evaluation scenarios scored** with overall score > 0.60.
3. **Holdout scenario passed** (RANDOM_STRESS score within 15% of training score).
4. **Human visual review completed** — operator has reviewed all captured videos and screenshots and signed off.
5. **No active veto** — no team member has flagged the candidate.

```
PROMOTION_ELIGIBLE =
    constraint_tests == ALL_PASS
    AND overall_score > 0.60
    AND holdout_check == PASS
    AND human_review == APPROVED
    AND active_vetoes == 0
```

### 6.3 Review Cadence

| Frequency | Review Type | Reviewer |
|-----------|-------------|----------|
| Every generation | Automated constraint + score check | System (automatic) |
| Every 5 generations | Dashboard review (scores, trends, diversity) | Operator |
| Every 10 generations | Visual review of best candidate captures | Operator + Design lead |
| On promotion | Full review (all criteria in 6.2) | Operator + Design lead + QA |
| On rollback | Post-mortem analysis | Operator + Engineering lead |

---

## 7. Commit Pipeline

### 7.1 Pipeline Stages

```
CANDIDATE CONFIG
      |
      v
[Stage 1: CONSTRAINT GATE]
  - Run full Constraint Test Suite (CT-01 through CT-10)
  - FAIL -> DISCARD, no further processing
  - PASS -> proceed
      |
      v
[Stage 2: SCENARIO EVALUATION]
  - Run all 5 evaluation scenarios
  - Score using Scoring Function
  - Record all telemetry and captures
      |
      v
[Stage 3: SELECTION]
  - Apply selection rules
  - Identify promotion candidates (best of generation)
      |
      v
[Stage 4: STAGING]
  - Promoted candidate moves to staging environment
  - Run full regression suite:
    * All 5 evaluation scenarios (re-run in staging)
    * Holdout scenario (RANDOM_STRESS)
    * Full constraint suite (re-run)
  - FAIL -> reject from promotion, remain in sandbox
  - PASS -> proceed
      |
      v
[Stage 5: HUMAN REVIEW]
  - Operator reviews dashboard, scores, captures
  - Design lead reviews visual quality
  - QA reviews for exploits or narrative breaks
  - ALL approve -> proceed
  - ANY reject -> candidate returns to sandbox
      |
      v
[Stage 6: CANONICAL COMMIT]
  - Commit configuration with version tag
  - Update ledger with config version reference
  - Archive previous canonical config
  - Log commit audit record
      |
      v
[Stage 7: VERIFICATION]
  - Run constraint suite against newly committed canonical config
  - Verify ledger references are correct
  - Confirm rollback path is valid
  - PASS -> evolution may continue from new baseline
  - FAIL -> immediate rollback (should never happen)
```

### 7.2 Version Tagging

Canonical configs are tagged with the following format:

```
config-v{MAJOR}.{MINOR}.{GEN}
```

| Component | Meaning |
|-----------|---------|
| MAJOR | Increments when registry changes (new params, changed bounds) |
| MINOR | Increments when scoring function weights change |
| GEN | Generation number of the promoted candidate |

Example: `config-v0.0.47` means registry v0, scoring v0, generation 47.

### 7.3 Ledger Integration

When a canonical config is committed, the ledger records the config version so that replays remain interpretable:

```json
{
  "ledger_event": "CONFIG_COMMIT",
  "timestamp": "2026-01-27T14:30:00Z",
  "config_version": "config-v0.0.47",
  "config_hash": "a7f3c2e9d1b4...",
  "effective_from": "2026-01-27T14:30:00Z",
  "previous_version": "config-v0.0.35",
  "previous_hash": "b4e2a1f9c83d..."
}
```

Any replay that spans a config change boundary must use the config version that was active at the time of the original recording.

---

## 8. Commit Audit Record

Every promotion to canonical config produces an immutable audit record.

### 8.1 Audit Record Schema

```json
{
  "audit_version": "1.0.0",
  "gen": 47,
  "candidate_id": "gen47_candidate_03",
  "timestamp": "2026-01-27T14:30:00Z",
  "config_version": "config-v0.0.47",
  "config_hash": "a7f3c2e9d1b4f8e7c3a9b2d5e1f4a8c6",
  "parent_config_hash": "b4e2a1f9c83d7a6b4e2f1c9d8a3b5e7f",
  "registry_version": "0.1.0",
  "diffs": {
    "crowd_speed_mean": {
      "param_id": "C-01",
      "old": 1.30,
      "new": 1.25,
      "change_pct": -3.85
    },
    "crowd_personal_space": {
      "param_id": "C-03",
      "old": 0.80,
      "new": 0.75,
      "change_pct": -6.25
    },
    "sd_proxy_swap_distance": {
      "param_id": "SD-01",
      "old": 60.0,
      "new": 55.0,
      "change_pct": -8.33
    },
    "vehicle_braking_aggression": {
      "param_id": "T-05",
      "old": 0.50,
      "new": 0.55,
      "change_pct": 10.00
    },
    "billboard_activation_radius": {
      "param_id": "B-01",
      "old": 80.0,
      "new": 72.0,
      "change_pct": -10.00
    }
  },
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
  "final_score": 0.847,
  "constraint_results": {
    "overall": "ALL_PASS",
    "tests": {
      "CT-01": "PASS",
      "CT-02": "PASS",
      "CT-03": "PASS",
      "CT-04": "PASS",
      "CT-05": "PASS",
      "CT-06": "PASS",
      "CT-07": "PASS",
      "CT-08": "PASS",
      "CT-09": "PASS",
      "CT-10": "PASS"
    }
  },
  "holdout_score": 0.79,
  "holdout_check": "PASS",
  "reviewer": "human",
  "reviewer_name": "J. Operator",
  "review_timestamp": "2026-01-27T14:25:00Z",
  "rationale": "Reduced crowd speed improves flow at bottlenecks without hurting plausibility. Tighter proxy swap distance recovers GPU headroom lost to increased crowd density. Billboard radius reduction frees streaming bandwidth.",
  "vetoes": [],
  "previous_canonical": {
    "config_version": "config-v0.0.35",
    "config_hash": "b4e2a1f9c83d7a6b4e2f1c9d8a3b5e7f",
    "overall_score": 0.812
  }
}
```

### 8.2 Audit Storage

- Audit records are stored as individual JSON files: `audit/gen{N}_commit.json`
- Audit records are append-only. They are never modified after creation.
- A master index file `audit/index.json` lists all committed generations in chronological order.

---

## 9. Rollback Procedure

### 9.1 When to Rollback

| Trigger | Source | Severity |
|---------|--------|----------|
| All candidates in a generation fail constraints | Automatic | Standard — system handles |
| Best candidate scores worse than previous generation's worst | Automatic | Standard — system handles |
| Human veto of current canonical config | Manual | High — operator initiated |
| Post-deployment regression discovered | Manual | Critical — immediate action |

### 9.2 Rollback Steps

```
ROLLBACK PROCEDURE:

1. IDENTIFY target
   - Default: previous canonical config (generation N-1)
   - If N-1 is also compromised: search archive for last known good (up to 10 back)

2. LOAD target config
   - Read from archive: configs/archive/gen{TARGET}_canonical.json
   - Verify file integrity via hash check

3. VERIFY target config
   - Run full Constraint Test Suite (CT-01 through CT-10)
   - If ANY test fails: target is corrupted, try next archive entry
   - If ALL pass: proceed

4. ACTIVATE target config
   - Update active config pointer to target
   - Record effective timestamp

5. LOG rollback event
   - Write rollback record (see Section 9.3)
   - Update ledger with config change

6. NOTIFY
   - Alert operator via configured notification channel
   - Include: reason, from-generation, to-generation, verification result

7. RESUME evolution
   - Reset population: seed from restored config
   - Resume generation loop from restored generation + 1
```

### 9.3 Rollback Event Record

```json
{
  "event": "ROLLBACK",
  "timestamp": "2026-01-27T15:45:00Z",
  "from_generation": 48,
  "from_config_version": "config-v0.0.48",
  "from_config_hash": "c5d3e2f1a4b8...",
  "to_generation": 47,
  "to_config_version": "config-v0.0.47",
  "to_config_hash": "a7f3c2e9d1b4...",
  "reason": "Human veto: visual artifacts observed in RAINY_NIGHT captures — rain particles clipping through awnings at reduced activation radius",
  "trigger": "manual",
  "verification_result": "ALL_PASS",
  "verification_timestamp": "2026-01-27T15:43:00Z",
  "operator": "J. Operator",
  "population_reset": true,
  "notes": "Gen48 candidate reduced billboard_activation_radius too aggressively. Constraint suite does not cover particle rendering quality — consider adding CT-11."
}
```

### 9.4 Archive Policy

| Policy | Value |
|--------|-------|
| Archive depth | Last 10 passing canonical configs |
| Storage location | `configs/archive/gen{N}_canonical.json` |
| Immutability | Archived configs are never modified |
| Pruning | When archive exceeds 10 entries, oldest is removed (unless it is the gen0 baseline, which is always retained) |
| Metadata | Each archive entry includes generation number, timestamp, score, config hash, and registry version |

Archive entry format:

```json
{
  "generation": 47,
  "config_version": "config-v0.0.47",
  "timestamp": "2026-01-27T14:30:00Z",
  "overall_score": 0.847,
  "config_hash": "a7f3c2e9d1b4f8e7c3a9b2d5e1f4a8c6",
  "config": {
    "C-01": 1.25,
    "C-02": 0.22,
    "C-03": 0.75,
    "C-04": 2.0,
    "C-05": 0.6,
    "C-06": 100,
    "C-07": 4.0,
    "C-08": 0.5,
    "T-01": 45.0,
    "T-02": 5.0,
    "T-03": 45.0,
    "T-04": 10.0,
    "T-05": 0.55,
    "T-06": 5.0,
    "T-07": 0.4,
    "SD-01": 55.0,
    "SD-02": 15.0,
    "SD-03": 50.0,
    "SD-04": 150.0,
    "SD-05": 0.25,
    "SD-06": 5.0,
    "W-01": 0.02,
    "W-02": 0.6,
    "W-03": 1.0,
    "W-04": 0.5,
    "W-05": 4000.0,
    "W-06": 0.01,
    "A-01": 1.0,
    "A-02": 200.0,
    "A-03": 1.0,
    "A-04": 1.0,
    "B-01": 72.0,
    "B-02": 0.75
  },
  "constraint_results": "ALL_PASS",
  "registry_version": "0.1.0"
}
```

---

## 10. Operational Checklist

### 10.1 Pre-Run Checklist

Before starting an evolution run, verify:

- [ ] Evolvable Parameter Registry is at expected version
- [ ] Constraint Test Suite is deployed and all tests executable
- [ ] All 5 evaluation scenarios are configured with correct seeds
- [ ] Holdout scenario (RANDOM_STRESS) is configured
- [ ] Scoring function weights are set and documented
- [ ] Capture system is operational (video + screenshot)
- [ ] Archive directory is writable and has sufficient disk space
- [ ] Notification system is configured and tested
- [ ] Baseline config (Bundle C) is committed as gen0
- [ ] Dashboard is accessible and displaying correctly
- [ ] Operator schedule is confirmed for review cadence

### 10.2 Per-Generation Checklist (Automated)

Each generation automatically verifies:

- [ ] Population size = 10
- [ ] All candidates pass bounds check
- [ ] All candidates pass rate limit check
- [ ] Dependency constraints enforced
- [ ] Constraint suite executed for each candidate
- [ ] All 5 scenarios executed for surviving candidates
- [ ] Scores computed and recorded
- [ ] Selection applied
- [ ] Generation results logged
- [ ] Dashboard updated
- [ ] Best candidate config archived

### 10.3 Post-Run Checklist

After evolution halts (any stopping condition):

- [ ] Record final generation number and reason for halt
- [ ] Review best candidate across all generations
- [ ] Run holdout scenario on best candidate
- [ ] Complete human visual review
- [ ] If promoting: execute full commit pipeline (Section 7)
- [ ] If not promoting: document reason and archive results
- [ ] Update registry if parameter bounds need adjustment
- [ ] Conduct retrospective: what worked, what needs changing

---

## 11. Failure Recovery

### 11.1 Infrastructure Failures

| Failure | Detection | Recovery |
|---------|-----------|----------|
| Simulation crash mid-scenario | Process exit code != 0 | Mark candidate as failed (score = 0.0). Continue with next candidate. |
| Disk full during capture | Write error | Pause evolution. Alert operator. Clear space. Resume. |
| GPU driver crash | System event log | Restart evaluation node. Re-run affected candidates. |
| Network failure (if distributed) | Heartbeat timeout | Reassign work to another node. Re-run affected candidates. |
| Corrupt archive file | Hash mismatch on read | Use next-oldest archive. Alert operator. |

### 11.2 Logical Failures

| Failure | Detection | Recovery |
|---------|-----------|----------|
| All 10 candidates fail constraints | Zero survivors | Automatic rollback to previous generation. Seed fresh population. |
| Score regression (best < previous worst) | Score comparison | Automatic rollback. Log anomaly. |
| Population collapse (all candidates similar) | Diversity index < 0.05 | Inject 3 random candidates (large exploration) into next generation. |
| Holdout score drops > 15% | Holdout check | Block promotion. Flag overfitting. Operator review. |
| Scoring function produces NaN or negative | Value check | Discard candidate. Log error. Investigate metric source. |

### 11.3 Emergency Stop Protocol

If three consecutive rollbacks occur:

1. **HALT** the evolution loop immediately.
2. **FREEZE** the current state: archive all candidate configs, scores, and telemetry.
3. **NOTIFY** the operator, engineering lead, and design lead.
4. **DIAGNOSE**: Review the last 5 generations for patterns:
   - Are constraint tests overly sensitive?
   - Is a dependency constraint creating an impossible region?
   - Has the registry become inconsistent?
   - Is the scoring function rewarding pathological behavior?
5. **RESOLVE**: Fix the identified issue (may require registry update, constraint adjustment, or scoring reweight).
6. **RESUME**: Only after manual approval from operator + engineering lead.

---

## 12. Glossary

| Term | Definition |
|------|------------|
| Candidate | A specific set of parameter values being evaluated |
| Generation | One iteration of the evolutionary loop (10 candidates evaluated) |
| Canonical config | The currently active, approved configuration |
| Sandbox | The evaluation environment where candidates are tested before promotion |
| Staging | The pre-production environment for final validation before commit |
| Promotion | Moving a candidate from sandbox to canonical config |
| Rollback | Reverting to a previous canonical config |
| Holdout scenario | A scenario never used in training, only for validation |
| Diversity pick | A candidate selected for being different from the top performers |
| Elite | The top-performing candidate that survives unchanged to the next generation |
| Bounds check | Verification that all parameters are within declared min/max |
| Rate limit | Maximum 20% change per parameter per generation |

---

*End of AlphaEvolve Ops Playbook v0.*
