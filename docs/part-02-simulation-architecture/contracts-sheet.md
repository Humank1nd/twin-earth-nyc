# Twin Earth NYC -- Contracts Sheet

**Document:** Part 2, Deliverable 2
**Status:** Draft v0.1
**Scope:** System Invariants and Tolerances for the Times Square Vertical Slice
**Last Updated:** 2026-01-27

---

Every system in Twin Earth NYC operates under a contract. A contract is a promise that the system makes to every other system and to the player. Contract violations are categorized as **P0 (ship-blocking)**, **P1 (must-fix before milestone)**, or **P2 (fix before release)**. This sheet is the canonical reference for all contracts.

**Rule of Contracts:** If a system cannot meet its contract under current performance conditions, it must degrade gracefully within declared tolerances -- never silently break the contract.

---

## Geometry Contracts

| Invariant | Tolerance | Priority | Verification Method |
|---|---|---|---|
| Street layout matches NYC DOT survey data | +/- 0.5m horizontal | P0 | Overlay GIS data on navmesh; automated pixel comparison |
| Building footprints match cadastral data | +/- 1.0m per edge | P1 | Footprint polygon comparison vs. NYC PLUTO dataset |
| Landmark positions (One Times Square, TKTS steps, major intersections) | +/- 0.25m from surveyed coordinates | P0 | GPS-tagged reference points vs. world-space query |
| Curb heights | 15cm +/- 2cm | P1 | Collision ray test at 50 sampled curb points |
| Door heights | 2.1m +/- 5cm | P0 | Scale validation sweep: raycast at every door entity |
| Sidewalk width matches DOT records | +/- 0.3m | P1 | Navmesh width measurement at 20 sampled cross-sections |
| Crosswalk positions match signal positions | +/- 1.0m center alignment | P0 | Visual + navmesh audit per intersection |
| Navmesh covers all walkable surfaces with no gaps > 0.3m | Zero uncovered walkable areas | P0 | Flood-fill reachability test from 10 spawn points |

---

## Traffic Contracts

| Invariant | Tolerance | Priority | Verification Method |
|---|---|---|---|
| Signal cycle timing is deterministic given seed | Exact match (zero tolerance) | P0 | Replay test: two runs with same seed, diff signal logs |
| Signal phases follow NYC DOT standard sequences | Correct phase order; timing +/- 0.5s per phase | P1 | Phase sequence validator against DOT spec |
| Vehicle paths are reproducible from seed | Exact waypoint sequence (position +/- 0.1m from interpolation) | P0 | Replay diff: path log comparison |
| Intersection clearance guaranteed (no gridlock deadlocks) | Zero permanent deadlocks; temporary congestion allowed up to 120s | P0 | 1-hour stress test: inject max vehicle density, verify flow resumes |
| Vehicle speed limits respected in normal state | Posted limit +/- 5 mph (emergency vehicles exempt) | P1 | Speed sampling at 10 road segments over 10 min |
| Pedestrian signals match traffic signals | Zero conflicts (walk signal never active with conflicting green) | P0 | Exhaustive signal state matrix verification |
| Turn restrictions obeyed | Zero illegal turns in normal traffic | P1 | Path audit: log all turns, cross-reference legal turn table |

---

## Crowd Contracts

| Invariant | Tolerance | Priority | Verification Method |
|---|---|---|---|
| No NPC teleportation (position discontinuities > 1m/frame) | Zero occurrences | P0 | Frame-over-frame position delta check, flag > 1m |
| No NPC phasing through static geometry | Zero occurrences in near band; < 1/min in mid band | P0 (near), P1 (mid) | Continuous collision overlap test on NPC capsules |
| No NPC phasing through other NPCs | Zero full-body overlaps in near band | P0 | Capsule overlap audit in near band every frame |
| Density caps enforced per zone | Max 4 NPCs/m2 (extreme crowd), normal max 2 NPCs/m2 | P1 | Spatial density query per navmesh polygon |
| NPCs navigate around obstacles, not through them | Zero pathfinding-through-wall events | P0 | Navmesh + obstacle avoidance integration test |
| Crowd flow direction matches time-of-day patterns | Majority flow direction correct for commute hours | P2 | Statistical flow analysis at 4 measurement points |
| NPC pop-in distance | No visible NPC spawn within 30m of camera | P1 | Spawn event distance log; flag < 30m events |
| NPC despawn distance | No visible NPC despawn within 50m of camera (unless masked) | P1 | Despawn event distance + frustum check |

---

## Lighting Contracts

| Invariant | Tolerance | Priority | Verification Method |
|---|---|---|---|
| Sun position matches astronomical calculation for sim date/time/location | +/- 0.5 degrees azimuth and elevation | P0 | Compare engine sun vector vs. NOAA solar calculator at 24 sample times |
| Shadow direction consistent with sun position | Shadow angle matches sun azimuth +/- 2 degrees | P0 | Shadow ray comparison at 5 landmark locations |
| Billboard colors stable across LOD transitions | Delta E (CIE2000) < 3.0 between LOD levels | P1 | Automated screenshot comparison at LOD transition distances |
| Time-of-day lighting transitions smooth | No visible discontinuities; transition over >= 60s sim-time | P1 | Frame-capture during dawn/dusk transitions; histogram analysis |
| Night billboard illumination creates visible glow on nearby surfaces | Emissive bounce detectable on surfaces within 10m of billboard | P2 | Luminance sampling on surfaces adjacent to active billboards |
| Interior lights follow plausible on/off schedule | > 80% of windows lit at night, < 30% during day | P2 | Window emissive state survey at noon and midnight |
| No shadow acne or peter-panning on landmark surfaces | Zero visible artifacts on One Times Square, TKTS steps, Marriott facade | P0 | Visual inspection at 5 camera angles per landmark |

---

## Sound Contracts

| Invariant | Tolerance | Priority | Verification Method |
|---|---|---|---|
| Sound source spatial position matches visual source | +/- 15 degrees angular error at player position | P1 | Emit test tone from 10 placed sources; measure perceived vs. actual angle |
| No phantom sound sources (audio without visual cause) | Zero occurrences in near band | P0 | Audio event log cross-referenced with visual entity presence |
| Sound attenuation follows inverse-square law (modified for urban canyon) | +/- 3 dB from expected level at measured distance | P2 | dB measurement at 5m, 20m, 50m from reference source |
| Ambient bed matches time of day and weather | Correct ambient preset selected for each condition combo | P1 | State machine audit: verify correct bank for each (time, weather) pair |
| Doppler effect on moving vehicles | Perceptible pitch shift on vehicles passing > 10 m/s | P2 | Audio capture during vehicle pass-by; frequency analysis |
| Sound occlusion by buildings | Reduction of >= 10 dB when solid building is between source and listener | P2 | Occlusion test at 5 building corners with reference source |

---

## Device Contracts

| Invariant | Tolerance | Priority | Verification Method |
|---|---|---|---|
| All device state changes logged to Trust Ledger | Zero missed state transitions | P0 | Device event counter vs. ledger event count per session |
| Device entity IDs stable within save file | Zero ID collisions or mutations across save/load | P0 | Save, load, enumerate entities, compare ID sets |
| Event causality preserved (cause timestamp < effect timestamp) | Zero violations (strict temporal ordering) | P0 | Ledger query: find any effect event with timestamp <= cause event |
| CCTV detection latency | Event logged within 2.0s of observable action in FOV | P0 | Staged action in CCTV view; measure ledger entry timestamp delta |
| Access control response latency | Door/gate state change within 0.5s of valid input | P1 | Automated input-to-state-change timing test |
| Device power state respects grid | Powered devices go dark during blackout within 1s; battery backup devices persist | P1 | Trigger power outage event; audit device emissive states at 1s mark |
| Alarm propagation follows declared chain | Alarm reaches all linked devices in declared order within 5s total | P1 | Trigger alarm at source; verify cascade order and timing |

---

## Anomaly Contracts

| Invariant | Tolerance | Priority | Verification Method |
|---|---|---|---|
| Anomaly effects confined to declared bleed radius | Zero gameplay effects beyond declared boundary + 0.5m buffer | P0 | Place test entities at boundary, boundary+0.5m, boundary+1m; verify effect/no-effect |
| Bleed radius matches declared value | Measured radius within +/- 0.5m of declared radius | P0 | Raycast from anomaly center; find effect falloff distance |
| Every anomaly observation generates at least one evidence event | Zero unrecorded anomaly observations within sensor range | P0 | Trigger anomaly in sensor range of CCTV + NPC; count evidence events |
| Anomaly visual effects respect LOD (no invisible anomalies in near band) | LOD0 anomaly VFX always active within 30m | P0 | Distance sweep: verify VFX presence at 5m intervals from 0-50m |
| Anomaly aftermath persists after anomaly ends | Altered world state remains until repaired or overwritten | P0 | Trigger anomaly, wait for end, verify state delta persists for 1h sim-time |
| Anomaly sensor interference matches spec | Sensor noise within declared degradation parameters inside bleed zone | P1 | Sample sensor output inside and outside bleed zone; compare noise profiles |

---

## Determinism Contracts

| System | Determinism Class | Seed-Dependent | Tolerance | Priority |
|---|---|---|---|---|
| **Trust Ledger** (event content and order) | **Deterministic** | Yes (events are input-sequence-dependent) | Exact match across replays | P0 |
| **Mission Logic** (branching, state transitions) | **Deterministic** | Yes | Exact match across replays | P0 |
| **Collision resolution** (physics contacts, overlap results) | **Deterministic** | Yes (PhysX deterministic mode) | Position +/- 0.001m after 60s of simulation | P0 |
| **Traffic signal timing** | **Deterministic** | Yes | Exact phase match | P0 |
| **Vehicle pathing** (waypoint sequence) | **Deterministic** | Yes | Exact waypoint sequence | P0 |
| **NPC decision-tree outcomes** | **Deterministic** | Yes | Same decision at same tick given same inputs | P0 |
| Crowd micro-motions (idle sway, head turns) | **Stochastic (seeded)** | Yes | Statistically similar; not frame-exact | P2 |
| Ambient prop placement (litter, puddles) | **Stochastic (seeded)** | Yes | Same distribution; not identical placement | P2 |
| Distant signage content | **Stochastic (seeded)** | Yes | Any valid content from pool | -- |
| Particle effects (rain, steam, sparks) | **Stochastic (seeded)** | Yes | Visual similarity only; no gameplay impact | -- |
| Cloud patterns | **Stochastic (seeded)** | Yes | Same weather state; cloud shape varies | -- |

**Determinism Verification Rule:** The nightly CI pipeline runs a 5-minute replay comparison test. Two instances execute the same seed + input log. The ledger diff must be empty. The physics state diff must be within tolerance. Any divergence is an automatic P0 bug filed against the owning subsystem.

---

*End of Contracts Sheet*
