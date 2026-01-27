# Twin Earth NYC -- Test Plan v0

**Document:** Part 2, Deliverable 3
**Status:** Draft v0.1
**Scope:** 10 Player Torture Tests for the Times Square Vertical Slice
**Last Updated:** 2026-01-27

---

## Purpose

These tests simulate the most punishing behaviors a suspicious, thorough, or adversarial player might exhibit. Each test targets a specific architectural promise. If any test fails, the corresponding system contract is violated and a P0 bug is filed.

All tests are designed to be run manually by QA or automated in CI where noted. **Every test must pass before the vertical slice is considered shippable.**

---

## Test 1: Revisit Test (World Persistence)

**Contract Under Test:** Trust Ledger persistence, Truth Engine world state durability

**Setup:** Player is positioned in Times Square near a destructible prop (e.g., a newspaper box at 44th and Broadway).

**Procedure:**
1. Player damages the newspaper box (kick, throw object, or anomaly effect). Confirm damage is visible (dented mesh, scattered papers).
2. Player walks 200m north (out of near band) and waits 5 minutes sim-time.
3. Player returns to the exact location of the damaged newspaper box.

**Pass Criteria:**
- [ ] The newspaper box is still damaged (same mesh state, scattered papers present).
- [ ] The Trust Ledger contains a `DMG` event for the newspaper box entity with correct timestamp and position (+/- 0.5m).
- [ ] No visual pop or state reset occurs when the object re-enters the near band.
- [ ] If a CCTV camera had line-of-sight to the damage event, an `EVD` observation entry exists in the ledger.

**Failure Mode:** Object resets to undamaged state, ledger entry missing, or visual discontinuity on return. **Priority: P0.**

---

## Test 2: Chase Test (Pursuit Intelligence)

**Contract Under Test:** Sensor truth (no god-knowledge), NPC perception model, authority response system

**Setup:** Player commits a visible crime (e.g., forces a locked door) in view of an NPC police officer.

**Procedure:**
1. Player forces a door while an NPC officer is within 20m and has line-of-sight.
2. Officer initiates pursuit (verbal warning, then chase).
3. Player sprints around a corner, breaking line-of-sight.
4. Player enters a side alley (backstage corridor) and remains stationary for 60 seconds.

**Pass Criteria:**
- [ ] Officer pursues to last-known-position (the corner), not directly to player's hiding spot.
- [ ] Officer exhibits search behavior: checking the alley entrance, looking both directions, radioing for support.
- [ ] If no CCTV covers the alley, the officer does not enter the alley unless they witness the player entering it.
- [ ] If CCTV covers the alley, pursuit updates to alley location within 5 seconds of CCTV detection.
- [ ] The pursuit ledger entry records `last_known_position`, not `actual_position`.
- [ ] After 120 seconds without new observations, pursuit downgrades from ACTIVE to SEARCHING.

**Failure Mode:** Officer teleports to player, navigates directly to hidden player without sensor justification, or pursuit never ends despite total LOS break. **Priority: P0.**

---

## Test 3: Replay Test (Determinism)

**Contract Under Test:** Deterministic replay, ledger reproducibility, physics determinism

**Setup:** A scripted 60-second scenario: player walks a fixed path, interacts with two objects, and one NPC event triggers.

**Procedure:**
1. Record the scenario with seed `0xDEADBEEF` and capture the full input log.
2. Export the Trust Ledger at scenario end (Run A).
3. Reset all state. Replay the scenario from the same seed with the same input log.
4. Export the Trust Ledger at scenario end (Run B).
5. Diff the two ledger exports.

**Pass Criteria:**
- [ ] Ledger diff is **empty** -- identical event IDs, timestamps, positions, categories, and commit states.
- [ ] Physics object final positions match within +/- 0.001m.
- [ ] NPC decision outcomes are identical (same behavior tree paths taken).
- [ ] Signal phase states are identical at every sampled tick.

**Failure Mode:** Any ledger diff entry, physics position divergence beyond tolerance, or NPC behavioral divergence. **Priority: P0.**

**Automation:** This test runs nightly in CI with 5 distinct scenarios and 3 seeds each (15 total replay comparisons).

---

## Test 4: Scale Test (Proportional Correctness)

**Contract Under Test:** Geometry contracts, canonical unit system, invariant scale anchors

**Setup:** Player is positioned at the TKTS red steps in Father Duffy Square, surrounded by reference objects.

**Procedure:**
1. Player stands next to a standard door. Measure door height relative to player avatar.
2. Player stands next to a parked taxi. Measure taxi length relative to player height.
3. Player stands next to an NPC. Compare heights.
4. Player climbs the TKTS red steps. Count visible risers and estimate riser height.
5. Player approaches a traffic light pole. Estimate signal center height.

**Pass Criteria:**
- [ ] Player avatar height reads 1.75m (+/- 0.05m) via debug ruler.
- [ ] Door height reads 2.1m (+/- 0.05m). Player walks through without ducking animation.
- [ ] Taxi length reads 4.8m (+/- 0.1m). Player height is approximately 36% of taxi length (visually plausible).
- [ ] NPC heights range from 1.55m to 1.95m with median near 1.75m (sample 20 NPCs).
- [ ] TKTS steps have correct riser height (18cm +/- 1cm) and feel correct during traversal (no float, no sink).
- [ ] Traffic light signal center is at 5.5m (+/- 0.2m).

**Failure Mode:** Any measurement outside tolerance, or any visual impression of "wrong scale" (miniature/giant effect). **Priority: P0.**

---

## Test 5: Crowd Squeeze (Collision Integrity)

**Contract Under Test:** NPC-NPC and NPC-geometry collision, density caps, no phasing

**Setup:** Player navigates into the densest pedestrian area (7th Avenue sidewalk at 45th Street, lunch hour preset: 2.0 NPCs/m2).

**Procedure:**
1. Player walks directly into the crowd at normal speed.
2. Player attempts to sprint through the crowd.
3. Player stops in the middle of the crowd and observes NPC behavior for 30 seconds.
4. Player attempts to push against a wall of NPCs at a crosswalk waiting for a signal.

**Pass Criteria:**
- [ ] Player movement is slowed proportionally to crowd density (sprint speed reduced to walk speed in dense crowd).
- [ ] No NPC passes through the player's collision capsule.
- [ ] No NPC passes through another NPC's collision capsule (in near band; mid band allows minor overlap < 10cm).
- [ ] No NPC passes through static geometry (walls, bollards, planters).
- [ ] NPCs exhibit believable push-back: shuffle, adjust path, express annoyance (animation/audio cue).
- [ ] Density cap is respected: no zone exceeds 4.0 NPCs/m2 at any point.
- [ ] Player can always extricate themselves (no permanent crowd trapping).

**Failure Mode:** NPC phasing through player, other NPCs, or geometry. Player permanently stuck. Density cap exceeded. **Priority: P0.**

---

## Test 6: Signal Obey (Traffic Compliance)

**Contract Under Test:** Traffic logic determinism, NPC rule compliance, signal-pedestrian coordination

**Setup:** Player observes a signalized intersection (Broadway and 44th Street) for 3 full signal cycles.

**Procedure:**
1. Count the number of NPC pedestrians who wait at the red hand signal.
2. Count the number of NPC pedestrians who cross during the walk signal.
3. Count any jaywalkers (crossing against signal without justification).
4. Observe vehicle behavior at red/green transitions.
5. Note any NPC-vehicle conflicts.

**Pass Criteria:**
- [ ] >= 95% of NPC pedestrians obey the walk/don't-walk signal (wait at red, cross at white).
- [ ] The <= 5% who jaywalk do so with plausible behavior (check for traffic, cross quickly, show urgency animation).
- [ ] Zero NPC-vehicle collisions during normal signal operation.
- [ ] Vehicles stop within 2m of the stop line on red.
- [ ] Vehicles clear the intersection within 3 seconds of their signal turning red (no lingering in intersection).
- [ ] Signal phases are consistent across all 3 observed cycles (same durations, same sequence).

**Failure Mode:** Compliance below 95%, NPC-vehicle collision, signal phase inconsistency, vehicles running red lights. **Priority: P0 (compliance, collisions), P1 (phase timing).**

---

## Test 7: Camera Audit (Evidence Generation)

**Contract Under Test:** CCTV observation pipeline, evidence ledger commits, detection latency

**Setup:** Player identifies a door covered by a CCTV camera (use debug overlay to confirm CCTV FOV cone).

**Procedure:**
1. Player forces the door while within CCTV field of view and range.
2. Immediately open the Trust Ledger debug inspector.
3. Query for evidence events linked to the forced door entity.

**Pass Criteria:**
- [ ] An `EVD` observation of type `OBS_CCTV` exists in the ledger.
- [ ] The observation's `source_entity` matches the CCTV entity ID.
- [ ] The observation's `timestamp_sim` is within **2.0 seconds** of the door-force action.
- [ ] The observation's `confidence` is >= 0.7 (well-lit, unobstructed CCTV).
- [ ] The linked `DMG` event for the door is present and correctly categorized.
- [ ] If the player disables the CCTV before forcing the door, no `OBS_CCTV` observation is generated (negative test).

**Failure Mode:** No evidence generated, evidence delayed beyond 2s, evidence generated from disabled camera, wrong confidence value. **Priority: P0.**

---

## Test 8: Anomaly Boundary (Effect Containment)

**Contract Under Test:** Anomaly bleed radius, effect containment, boundary sharpness

**Setup:** Trigger a test anomaly at a known location with a declared bleed radius of 15m.

**Procedure:**
1. Place test probe entities at the following distances from anomaly center: 5m, 10m, 14m, 15m (boundary), 15.5m (buffer), 16m (outside).
2. Activate the anomaly.
3. Record which probes are affected by anomaly effects (physics distortion, visual artifacts, sensor interference).
4. Walk a full circle at the 15m boundary and observe the edge condition.

**Pass Criteria:**
- [ ] Probes at 5m, 10m, 14m: fully affected by anomaly effects.
- [ ] Probe at 15m (boundary): affected (boundary is inclusive).
- [ ] Probe at 15.5m (buffer zone): may show attenuated effects but no gameplay-altering distortion.
- [ ] Probe at 16m: zero anomaly effects.
- [ ] The boundary is visually indicated (shimmer, color shift, particle curtain) so the player can perceive the edge.
- [ ] Walking around the boundary shows consistent radius (no bulges, no flat spots, smooth circle).
- [ ] The Trust Ledger contains `ANM` events for all affected probes and zero `ANM` events for the 16m probe.

**Failure Mode:** Effects detected beyond declared radius + 0.5m buffer, no effects within declared radius, inconsistent boundary shape. **Priority: P0.**

---

## Test 9: Portal Return (Cross-Context Persistence)

**Contract Under Test:** Trust Ledger persistence across portal/mission transitions, world state continuity

**Setup:** Player is near an active anomaly portal that leads to a Twin Earth mission instance.

**Procedure:**
1. Before entering the portal: damage a nearby object (e.g., break a storefront window). Note the ledger state.
2. Enter the portal. Complete or abandon the mission (minimum 5 minutes in mission space).
3. Return through the portal to the Times Square hub.
4. Check the storefront window.
5. Check the Trust Ledger for pre-portal events.

**Pass Criteria:**
- [ ] The storefront window is still broken upon return (same damage mesh, same debris).
- [ ] Pre-portal Trust Ledger events are intact and unchanged.
- [ ] NPC witnesses who observed the window break before portal entry still have that memory (query their memory graph).
- [ ] If authority was alerted before portal entry, the response has progressed appropriately during elapsed sim-time (e.g., police arrived, investigation started).
- [ ] Mission-space events are logged in the ledger with a `MISSION_CONTEXT` tag and do not overwrite hub events.
- [ ] No duplicate entity IDs between hub and mission spaces.

**Failure Mode:** Pre-portal state reset, ledger data loss, authority response frozen during mission, entity ID collision. **Priority: P0.**

---

## Test 10: Performance Stress (Worst-Case Scenario)

**Contract Under Test:** Performance targets under maximum load, graceful degradation

**Setup:** Configure worst-case conditions simultaneously:
- Time: 11:30 PM (night, maximum billboard illumination)
- Weather: heavy rain (particle systems, wet material shaders, reflection updates)
- Crowd: 2,000 active NPCs in the slice (New Year's Eve density preset)
- Anomaly: one active anomaly with 20m bleed radius (VFX, physics distortion, sensor interference)
- Player position: center of the bowtie intersection (maximum visibility in all directions)

**Procedure:**
1. Spawn all conditions simultaneously.
2. Stand still for 60 seconds; record FPS, VRAM usage, RAM usage, CPU utilization.
3. Sprint north for 100m, triggering maximum streaming; record performance.
4. Turn 360 degrees slowly, forcing all direction-dependent LOD and streaming to cycle.
5. Interact with an object in the anomaly zone while all conditions are active.

**Pass Criteria:**
- [ ] **Average FPS >= 30** across the entire 3-minute test (hard minimum from contracts).
- [ ] **No single frame exceeds 66ms** (15 FPS floor -- no hard stutter).
- [ ] **VRAM usage <= 4.0 GB** (per slice config budget).
- [ ] **NPC RAM usage <= 2.0 GB** (per slice config budget).
- [ ] **Ledger file size <= 500 MB** (soft cap; test runs for limited time so should be well under).
- [ ] No visible LOD pop-in during the 360-degree turn (all seams masked).
- [ ] No NPC teleportation or phasing under stress.
- [ ] Physics interactions remain responsive (object responds to player within 2 frames).
- [ ] Rain particles do not visibly clip through building geometry.
- [ ] Anomaly VFX remain visible and correctly bounded during stress.

**Failure Mode:** FPS below 30 average, any frame above 66ms, memory budget exceeded, visible artifacts under stress. **Priority: P0 (FPS, memory), P1 (visual artifacts).**

**Automation:** This test runs weekly in CI on target hardware spec. Results are logged to a performance dashboard with historical trend tracking.

---

## Test Execution Summary

| # | Test Name | Primary Contract | Automated | Frequency |
|---|---|---|---|---|
| 1 | Revisit Test | World Persistence | Semi (scripted scenario, manual visual check) | Per milestone |
| 2 | Chase Test | Sensor Truth / No God-Knowledge | Manual (complex behavioral validation) | Per milestone |
| 3 | Replay Test | Determinism | **Fully automated** | Nightly CI |
| 4 | Scale Test | Geometry / Scale Anchors | Semi (automated measurement, manual visual) | Per milestone |
| 5 | Crowd Squeeze | Collision Integrity | Semi (automated overlap detection, manual feel) | Per milestone |
| 6 | Signal Obey | Traffic Logic | **Fully automated** (statistical counting) | Nightly CI |
| 7 | Camera Audit | Evidence Pipeline | **Fully automated** (scripted action + ledger query) | Nightly CI |
| 8 | Anomaly Boundary | Effect Containment | **Fully automated** (probe placement + effect query) | Nightly CI |
| 9 | Portal Return | Cross-Context Persistence | Semi (scripted scenario, manual state check) | Per milestone |
| 10 | Performance Stress | Performance Targets | **Fully automated** (metric capture + threshold check) | Weekly CI |

**Total: 5 fully automated, 4 semi-automated, 1 manual. Goal for v1: 8 fully automated.**

---

*End of Test Plan v0*
