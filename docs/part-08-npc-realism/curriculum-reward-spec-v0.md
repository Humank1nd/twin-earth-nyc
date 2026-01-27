# Curriculum + Reward Spec v0

**Document:** Part 8 — NPC Realism
**File:** `curriculum-reward-spec-v0.md`
**Status:** Draft v0
**Last Updated:** 2026-01-27
**Depends On:** NPC Taxonomy + Tier Plan v0, Sensor Interface Spec v0
**Feeds Into:** Runtime Validation Checklist, Policy Export Pipeline

---

## 1. Training Overview

Hero NPC policies are trained via reinforcement learning in a **four-stage curriculum** of increasing environmental complexity. Each stage introduces new observations and challenges, building on skills mastered in prior stages. Training uses PPO (Proximal Policy Optimization) with the reward function defined in Section 3.

### Training Infrastructure

| Parameter | Value |
|-----------|-------|
| Algorithm | PPO (clip ratio 0.2, GAE lambda 0.95) |
| Framework | PyTorch (training), ONNX (export) |
| Parallel environments | 256 (vectorized) |
| Steps per update | 2,048 per environment |
| Minibatch size | 4,096 |
| Learning rate | 3e-4 (linear decay to 1e-5) |
| Discount factor (gamma) | 0.99 |
| Episode max length | 600 steps (60 s at 10 Hz) |
| Policy architecture | MLP: 490 -> 256 -> 256 -> 128 -> 5 (action) |
| Value head | Shared trunk, separate 128 -> 1 output |

---

## 2. Four Training Stages

### Stage 1: Basic Locomotion (Empty Environment)

| Parameter | Specification |
|-----------|---------------|
| **Environment** | Flat plane, 100 m x 100 m, no obstacles |
| **Task** | Walk from spawn position to a single target waypoint |
| **Success criterion** | Reach within 1.0 m of target |
| **Graduation threshold** | > 95% success rate over 1,000 consecutive episodes |
| **Observations** | Depth probes only (16 floats) + self velocity (2 floats) + self heading (1 float) + goal vector (2 floats) |
| **Actions** | `velocity_x` (float, -1 to 1), `velocity_z` (float, -1 to 1), `heading_delta` (float, -0.2 to 0.2 rad) |
| **Reward components active** | Goal reached, smooth motion, deadlock penalty, freezing penalty |
| **Domain randomization** | Spawn position: random within arena. Goal position: random, > 20 m from spawn. |
| **Estimated training time** | ~2 hours (256 envs, commodity GPU) |

**Purpose:** Establish basic movement control -- forward locomotion, turning, velocity regulation, and goal-seeking.

---

### Stage 2: Obstacle Avoidance + Static Signals

| Parameter | Specification |
|-----------|---------------|
| **Environment** | Sidewalk corridor (200 m x 10 m) with static obstacles: bollards (0.3 m radius), benches (1.5 m x 0.5 m), planters (1.0 m x 1.0 m). One traffic signal at a crosswalk. |
| **Task** | Navigate to waypoint on the opposite side of the crosswalk, obey traffic signal (stop at red, proceed at green) |
| **Success criterion** | Reach within 1.0 m of target without collision AND obey all signals encountered |
| **Graduation threshold** | > 95% success rate AND > 99% signal compliance over 1,000 episodes |
| **Observations** | Depth probes + forward camera (64 x 64 encoded to 128-dim feature via frozen CNN) + traffic signal state + goal vector |
| **Actions** | Same as Stage 1 |
| **Reward components active** | All Stage 1 + signal compliance, signal violation, collision (static) |
| **Domain randomization** | Obstacle count: 5 -- 20 (uniform). Obstacle positions: random within corridor. Signal cycle: 15 -- 45 s red, 15 -- 30 s green (uniform). Spawn side: random. |
| **Estimated training time** | ~6 hours |

**Purpose:** Learn spatial reasoning around static obstacles and introduce rule-following behavior (traffic signal compliance).

---

### Stage 3: Moving Crowds + Dynamic Signals

| Parameter | Specification |
|-----------|---------------|
| **Environment** | Times Square block (200 m x 200 m) with 50 -- 200 background pedestrians following heuristic lane-follow behavior, active signal cycles at 4 intersections |
| **Task** | Navigate through crowd to waypoint, cross intersections legally |
| **Success criterion** | Reach target, < 2 pedestrian collisions, all signals obeyed |
| **Graduation threshold** | > 90% success rate with < 0.5 average collisions per episode over 1,000 episodes |
| **Observations** | Full sensor suite: occupancy grid (20 x 20), visible agents list (16 x 5), traffic signal, noise direction, stress indicators, self state |
| **Actions** | Same as Stage 1 + `look_delta` (float, -0.5 to 0.5 rad -- optional head turn independent of movement) |
| **Reward components active** | All Stage 2 + collision (pedestrian), witness behavior |
| **Domain randomization** | Crowd density: 0.5 -- 2.5 persons/m² (uniform). Signal timing: variable. Background NPC speed: 0.8 -- 1.5 m/s (normal distribution, mu=1.2, sigma=0.2). Weather: clear or rain (50/50). Time of day: 8 AM -- 10 PM (uniform). |
| **Estimated training time** | ~24 hours |

**Purpose:** Master social navigation -- weaving through crowds, predicting pedestrian motion, maintaining personal space, and navigating dynamic intersections.

---

### Stage 4: Mixed Traffic + Stress Events

| Parameter | Specification |
|-----------|---------------|
| **Environment** | Full Times Square slice with vehicles (background drivers on scripted paths), crowds (50 -- 500 background NPCs), active signals at all intersections, random stress events |
| **Task** | Navigate to waypoint while adapting to dynamic conditions including emergency vehicles, anomaly shimmers, and crowd surges |
| **Success criterion** | Reach target, < 1 collision, appropriate stress response in all encountered events |
| **Graduation threshold** | > 85% success rate with appropriate stress responses in > 90% of events over 2,000 episodes |
| **Observations** | Full sensor suite + audio proxy (bearing + loudness) |
| **Actions** | Same as Stage 3 |
| **Reward components active** | All components (full reward function) |
| **Domain randomization** | Full randomization suite (see Section 4) |
| **Estimated training time** | ~72 hours |

**Stress events injected during Stage 4:**

| Event | Trigger Probability (per episode) | Expected NPC Response |
|-------|-----------------------------------|----------------------|
| Siren approach | 10% | Yield path, orient toward siren source |
| Anomaly shimmer | 5% | Divert route away from anomaly zone, increase walking speed |
| Crowd surge | 5% | Slow down, join flow direction or seek edge of crowd |
| Gunshot / explosion | 2% | Panic flee (run away from audio source at max speed) |
| Authority cordon placement | 3% | Reroute around cordoned area |

**Purpose:** Produce a robust, naturalistic policy that handles the full complexity of the Twin Earth Times Square environment including rare but critical stress events.

---

## 3. Reward Function

### Component Table

| # | Component | Weight | Formula | Active From |
|---|-----------|--------|---------|-------------|
| 1 | Goal reached | +10.0 | Binary: `1` if NPC within 1.0 m of target at episode end, else `0` | Stage 1 |
| 2 | Signal compliance | +2.0 | Per legal crossing: NPC enters crosswalk during green/walk phase | Stage 2 |
| 3 | Signal violation | -5.0 | Per illegal crossing: NPC enters crosswalk during red/don't-walk phase | Stage 2 |
| 4 | Collision (pedestrian) | -3.0 | Per collision event (NPC capsule overlaps pedestrian capsule for > 0.2 s) | Stage 3 |
| 5 | Collision (vehicle) | -10.0 | Per collision with any vehicle collider (severe consequence) | Stage 4 |
| 6 | Collision (static) | -1.0 | Per collision with static obstacle (bollard, bench, wall) | Stage 2 |
| 7 | Smooth motion | +0.5 / step | Awarded when jerk magnitude < 2.0 m/s^3: `0.5 * (1 - jerk / 2.0)` clamped to [0, 0.5] | Stage 1 |
| 8 | Deadlock penalty | -1.0 / sec | Applied when `velocity < 0.1 m/s` for > 5 s without a valid reason (signal wait does not count) | Stage 1 |
| 9 | Freezing penalty | -2.0 / sec | Applied when completely stationary (`velocity < 0.01 m/s`) for > 10 s without valid reason | Stage 1 |
| 10 | Anomaly avoidance | +3.0 | Awarded when NPC diverts route to maintain > 5 m distance from anomaly boundary | Stage 4 |
| 11 | Witness behavior | +5.0 | Awarded when NPC stops, orients toward major event, and generates a witness observation record | Stage 3 |

### Reward Shaping Notes

- **Goal distance shaping:** An additional dense reward of `+0.1 * delta_distance_to_goal` is applied per step (positive when getting closer, negative when moving away). This is annealed to zero by Stage 4 to avoid reward hacking.
- **Collision grace period:** After a collision event, a 1.0 s grace period prevents duplicate penalties for the same contact.
- **Valid stop reasons:** Signal wait (red light within 5 m), crowd density > 3.0 persons/m² (physical inability to move), cordon within 3 m. These suppress deadlock and freezing penalties.
- **Witness bonus conditions:** Only awarded for events classified as "major" (anomaly, explosion, pursuit, vehicle accident). NPC must be stationary for > 2 s and facing the event (within 30 degrees of bearing to event).

### Reward Normalization

| Parameter | Value |
|-----------|-------|
| Return normalization | Running mean and variance of episodic returns |
| Reward clipping | Per-step reward clipped to [-15.0, +15.0] |
| Advantage normalization | Per-minibatch, zero mean, unit variance |

---

## 4. Domain Randomization

All randomization parameters are sampled independently at episode start unless noted otherwise.

| Parameter | Range | Distribution | Notes |
|-----------|-------|-------------|-------|
| Weather: wetness | 0.0 -- 1.0 | Uniform | Affects traction (friction *= 1 - 0.3 * wetness) and sensor noise |
| Lighting: time of day | 06:00 -- 02:00 | Uniform over 20-hour window | Affects camera noise model and NPC visibility |
| Crowd density | 0.1 -- 3.0 persons/m² | Uniform | Controls background NPC spawn rate |
| Ambient noise level | 40 -- 80 dB | Uniform | Affects audio proxy signal-to-noise ratio |
| Spawn position | Random within walkable area | Uniform over walkable navmesh | Must be on sidewalk or pedestrian zone |
| Goal position | Random within walkable area, > 50 m from spawn | Uniform over walkable navmesh | Must be reachable via legal paths |
| Parked vehicle occluders | 0 -- 5 | Uniform integer | Placed at random legal parking positions |
| Crowd clusters | 0 -- 3 | Uniform integer | Stationary groups of 5 -- 15 NPCs at random locations |
| Siren event | 10% per episode | Bernoulli | If triggered, siren approaches from random direction at T = uniform(10 s, 50 s) |
| Anomaly shimmer event | 5% per episode | Bernoulli | If triggered, anomaly appears at random walkable position at T = uniform(15 s, 45 s) |
| Crowd surge event | 5% per episode | Bernoulli | If triggered, surge direction and magnitude randomized at T = uniform(20 s, 50 s) |
| NPC walking speed | 0.8 -- 1.5 m/s | Normal (mu=1.2, sigma=0.2) | Per background NPC, sampled at spawn |
| Signal cycle length | 30 -- 90 s (full cycle) | Uniform | Red/green split: uniform between 40/60 and 60/40 |

---

## 5. Policy Export

### Export Specification

| Parameter | Value |
|-----------|-------|
| Format | ONNX (opset 17) |
| Input tensor | `observation: float32[1, 490]` (flattened observation vector) |
| Output tensor | `action: float32[1, 5]` — `[velocity_x, velocity_z, heading_delta, look_delta, stop_probability]` |
| `stop_probability` | If > 0.5, NPC enters voluntary stop (witness behavior, signal wait, etc.) |
| Runtime | ONNX Runtime 1.16+ (DirectML backend on Windows, CUDA on Linux) |
| Quantization | FP16 inference supported (< 3% performance degradation validated) |
| Model size | ~2 MB (FP32), ~1 MB (FP16) |

### Validation Protocol

| Step | Procedure | Pass Criterion |
|------|-----------|----------------|
| 1 | Export trained PyTorch model to ONNX | No export warnings, output shape matches spec |
| 2 | Run ONNX model through `onnx.checker.check_model()` | Model is valid |
| 3 | Deploy in game runtime with identical sensor interface | Observation vector shape and semantics match training |
| 4 | Run 100 episodes in game runtime | Success rate within +/- 5% of training performance |
| 5 | Run 100 episodes with FP16 quantized model | Success rate within +/- 3% of FP32 model |
| 6 | Profile inference latency | < 2 ms per NPC per tick on target hardware |
| 7 | Run 10-minute continuous sim with 20 hero NPCs | Total inference time < 40 ms per frame; no memory leaks |

### Versioning

- Policy models are versioned as `hero_ped_policy_v{MAJOR}.{MINOR}.onnx`
- Major version increments when observation vector shape changes
- Minor version increments for retraining with same interface
- Game runtime checks policy version against expected interface version at load time; mismatch = fatal error with descriptive message

---

## 6. Curriculum Progression Summary

```
Stage 1                Stage 2                  Stage 3                    Stage 4
Basic Locomotion  -->  Obstacles + Signals -->  Crowds + Dynamic Sigs -->  Full Environment
                                                                           + Stress Events

Observations:          Observations:            Observations:              Observations:
  Depth probes           + Forward camera         + Occupancy grid           + Audio proxy
  Self state             + Signal state           + Visible agents           + Stress indicators
  Goal vector                                     + Crowd density

Graduation:            Graduation:              Graduation:                Graduation:
  95% goal success       95% success              90% success                85% success
                         99% signal compliance    < 0.5 avg collisions       90% stress response
```

---

## Open Questions

1. Should Stage 4 be split into 4a (vehicles only) and 4b (vehicles + stress events) for more stable training?
2. What is the appropriate curriculum for hero vehicle driver NPCs? A parallel four-stage curriculum is assumed but not yet specified.
3. Should cop pursuit behavior be trained in a separate adversarial curriculum (cop vs. fleeing NPC)?
4. Is the 490-element observation vector too large for efficient training, or should we add a learned encoder pre-stage?

---

*End of document.*
