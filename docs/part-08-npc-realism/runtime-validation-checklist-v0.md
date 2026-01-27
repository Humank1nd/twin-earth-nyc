# Runtime Validation Checklist v0

**Document:** Part 8 — NPC Realism
**File:** `runtime-validation-checklist-v0.md`
**Status:** Draft v0
**Last Updated:** 2026-01-27
**Depends On:** NPC Taxonomy + Tier Plan v0, Sensor Interface Spec v0, Curriculum + Reward Spec v0
**Feeds Into:** QA Pipeline, CI/CD Build Gates

---

## 1. Stability Tests

These tests must pass before any build is shipped. Tests marked "Every build" are CI gate requirements. Tests marked "Weekly" run in extended nightly/weekly regression suites.

| # | Test Name | Procedure | Pass Criteria | Frequency |
|---|-----------|-----------|---------------|-----------|
| 1 | **50-rep walk test** | Single hero NPC navigates to 50 random targets in the Times Square slice (full environment, midday density). Each target is > 50 m from the previous. | 0 falls, 0 stuck (velocity > 0.05 m/s within 15 s of any stop), < 2 total pedestrian collisions across all 50 routes | Every build |
| 2 | **Crowd density stress** | Incrementally spawn background NPCs: 500, then 1,000, then 2,000. Hold each tier for 60 s. Measure frame rate and NPC behavior coherence throughout. | No deadlocks at any tier. FPS > 30 at all tiers on target hardware. No NPC teleportation or visual popping. | Weekly |
| 3 | **Hero stability under density** | Spawn 10 hero NPCs simultaneously in peak crowd conditions (2.5 persons/m²). Each hero NPC assigned a unique waypoint > 100 m from spawn. Run for 5 minutes. | All 10 hero NPCs complete their routes. Collision rate < 5% (collisions / total steps). No hero NPC stuck for > 15 s. | Every build |
| 4 | **Signal compliance audit** | Run 100 intersection crossing events (hero NPCs approaching signalized crosswalks). Mix of green, red, and transition states. Record each crossing decision. | > 95% legal crossings (NPC waits at red, proceeds at green). 0 crossings initiated during red with oncoming traffic. | Every build |
| 5 | **10-minute continuous sim** | Full Times Square slice, all systems active (hero NPCs, background NPCs, vehicles, signals, Heat system, event bus). Run uninterrupted for 10 minutes of game time. | No NPC teleportation events. No stuck agents (velocity < 0.05 m/s for > 30 s without valid reason). No memory leaks (NPC memory allocation delta < 1 MB over 10 min). No crashes or exceptions. | Every build |
| 6 | **Hero NPC inference latency** | Profile ONNX inference time for 20 hero NPCs over 1,000 frames. | Mean inference time < 2 ms per NPC per tick. P99 inference time < 5 ms per NPC. Total hero NPC budget < 40 ms per frame. | Every build |
| 7 | **Background NPC throughput** | Profile heuristic update time for 1,500 background NPCs over 1,000 frames. | Mean update time < 0.1 ms per NPC per tick. Total background NPC budget < 150 ms per frame (amortized via round-robin). | Every build |

---

## 2. Deadlock Detection

### Definition

A **deadlock** occurs when 3 or more NPCs are mutually blocked (each waiting for another to move) for more than 10 seconds. This manifests as a cluster of stationary NPCs in a navigable area where no external constraint (signal, cordon, crowd crush) explains the stoppage.

### Automated Detection System

| Parameter | Value |
|-----------|-------|
| Monitoring scope | All NPCs (hero and background) |
| Detection method | Spatial clustering of low-velocity NPCs |
| Velocity threshold | < 0.05 m/s |
| Cluster radius | 3.0 m |
| Minimum cluster size | 3 NPCs |
| Time threshold | 10 seconds sustained |
| Sampling rate | 1 Hz (checked every second) |

### Detection Logic (Pseudocode)

```
every 1 second:
    slow_npcs = [npc for npc in all_npcs if npc.velocity < 0.05 m/s
                 AND npc.not_at_signal AND npc.not_in_cordon]
    clusters = spatial_cluster(slow_npcs, radius=3.0m)
    for cluster in clusters:
        if cluster.size >= 3 AND cluster.duration >= 10s:
            log_deadlock_event(cluster)
            apply_resolution(cluster)
```

### Resolution Protocol

| NPC Tier | Resolution Action |
|----------|-------------------|
| Background NPC | Force-reroute the slowest agent in the cluster to a random nearby walkable position (teleport if necessary, but log the teleport). |
| Hero NPC | **Do not force-reroute.** Flag for investigation. Log full sensor state and observation history for the 10 s leading up to deadlock. |
| Mixed cluster | Resolve background NPCs first. If hero NPC is still blocked after background resolution, give hero NPC a 5 s grace period, then flag. |

### Target Metric

- **< 0.1% deadlock rate** per 10-minute simulation (fewer than 1 deadlock event per 10-minute run on average).
- Tracked as a regression metric in CI dashboard.

---

## 3. Replay Consistency

### Deterministic Replay Test

| Step | Procedure |
|------|-----------|
| 1 | Configure scenario: Times Square slice, midday density, seed = 42. |
| 2 | Run simulation for 300 s (5 minutes). Capture NPC positions at T = 0, 60, 120, 180, 240, 300 s. |
| 3 | Reset all systems. Run identical scenario with same seed. Capture positions at same timestamps. |
| 4 | Compare position snapshots between Run A and Run B. |

### Pass Criteria

| NPC Type | Position Delta Tolerance | Notes |
|----------|--------------------------|-------|
| Deterministic NPCs (scripted drivers, stationary vendors) | < 0.01 m at all timestamps | Must be bit-exact given same seed |
| Stochastic NPCs (background pedestrians with seeded random) | < 1.0 m at all timestamps | Tolerance accounts for floating-point accumulation; seeded RNG must produce identical sequence |
| Hero NPCs (RL policy) | < 0.1 m at all timestamps | ONNX inference must be deterministic given identical inputs; tolerance accounts for FP32 precision |

### Failure Investigation

If replay consistency fails:

1. Identify the first frame where divergence exceeds tolerance.
2. Log full observation vectors for divergent NPC at that frame in both runs.
3. Compare observation vectors -- any difference indicates a sensor or environment non-determinism bug.
4. If observations are identical but actions differ, investigate ONNX runtime determinism settings.

---

## 4. Stress Event Response Tests

These tests validate that hero NPCs respond appropriately to dynamic stress events. Each test is run 20 times with randomized NPC starting positions.

| # | Event | Setup | Expected Hero NPC Response | Pass Criteria |
|---|-------|-------|---------------------------|---------------|
| 1 | **Siren approach** | Emergency vehicle approaches from random direction at 60 km/h with active siren. Hero NPC is on sidewalk within 30 m of vehicle path. | NPC yields path (moves away from road edge), orients head toward siren source. | > 80% of trials show yield behavior (lateral displacement > 0.5 m from road) AND head orientation within 30 degrees of siren bearing. |
| 2 | **Anomaly shimmer** | Anomaly zone (5 m radius) appears 15 m ahead of hero NPC on their current route. | NPC diverts route to maintain > 5 m distance from anomaly boundary. Walking speed increases by > 20%. | > 70% of trials show successful avoidance (minimum distance to anomaly > 5 m) AND speed increase. |
| 3 | **Crowd surge** | 50 background NPCs suddenly accelerate in a uniform direction (simulating crowd surge). Hero NPC is within the surge zone. | NPC slows down, either joins flow direction or navigates to crowd edge. No collisions during adaptation. | > 85% of trials show zero collisions during surge. NPC does not move against surge direction (heading within 90 degrees of flow). |
| 4 | **Gunshot / explosion** | Loud impulse audio event (95 dB) at random position within 20 m of hero NPC. | Panic response: NPC runs away from audio source at > 80% of max speed for at least 5 s. | > 90% of trials show flee behavior (movement bearing > 90 degrees from source, velocity > 80% max). |
| 5 | **Authority cordon** | Barriers placed at nearest intersection crossings, blocking hero NPC's current route. | NPC detects cordon (via depth probes / camera), stops, then reroutes around cordoned area. | > 95% of trials show successful reroute. 0% of trials show NPC walking through barriers. |

---

## 5. Memory Persistence Tests

These tests validate the hero NPC long-term memory system across sessions and within sessions.

### 5.1 Route Preference Formation

| Step | Procedure |
|------|-----------|
| 1 | Assign hero NPC a recurring origin-destination pair (e.g., subway entrance to office building). |
| 2 | Run 10 consecutive trips. Record route taken each trip. |
| 3 | Analyze route consistency from trip 3 onward. |

**Pass criteria:** NPC uses the same route (within 5 m corridor) on 3 or more consecutive trips after initial exploration. Route preference is recorded in long-term memory.

### 5.2 Avoidance Zone Formation

| Step | Procedure |
|------|-----------|
| 1 | Hero NPC experiences a negative event (collision, anomaly exposure, pursuit) at a specific location. |
| 2 | Run 5 subsequent trips that would naturally route through that location. |
| 3 | Measure whether NPC diverts around the negative-event location. |

**Pass criteria:** NPC avoids the negative-event location (maintains > 10 m distance) on at least 3 of 5 subsequent trips. Avoidance zone entry is present in long-term memory with correct location and negative valence.

### 5.3 Habit Decay

| Step | Procedure |
|------|-----------|
| 1 | Establish avoidance zone per Test 5.2. |
| 2 | Run 10 additional trips where no negative event occurs at the avoided location. |
| 3 | Measure whether avoidance behavior fades. |

**Pass criteria:** By trip 8 -- 10 (after 10 non-reinforced trips), NPC resumes routing through the previously avoided location in at least 2 of the final 3 trips. Long-term memory entry for that location has decayed below avoidance threshold.

### 5.4 Cross-Session Persistence

| Step | Procedure |
|------|-----------|
| 1 | Establish route preference and avoidance zone in Session A. |
| 2 | Save and quit. Reload as Session B. |
| 3 | Assign same origin-destination pair. Observe route choice. |

**Pass criteria:** NPC retains route preference and avoidance zone from Session A. Behavior in Session B first trip matches Session A established behavior.

---

## 6. Validation Dashboard Metrics

The following metrics are tracked continuously and displayed on the CI validation dashboard.

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Walk test success rate | 100% | < 98% |
| Signal compliance rate | > 95% | < 93% |
| Collision rate (hero NPCs) | < 5% | > 7% |
| Deadlock rate (per 10 min) | < 0.1% | > 0.2% |
| FPS at peak density (2,000 NPCs) | > 30 | < 28 |
| Hero inference latency (P99) | < 5 ms | > 8 ms |
| Replay consistency (deterministic) | < 0.01 m | > 0.05 m |
| Stress response appropriateness | > 80% | < 70% |
| Memory persistence (cross-session) | 100% | < 100% |

---

## Open Questions

1. Should deadlock detection be extended to vehicle NPCs (gridlock detection)?
2. What is the acceptable teleport rate for background NPC deadlock resolution -- should it be visible to the player or hidden behind occluders?
3. Should stress response tests include compound events (e.g., anomaly + siren simultaneously)?

---

*End of document.*
