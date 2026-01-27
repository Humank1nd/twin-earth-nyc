# Evidence Schema v0

**Twin Earth NYC -- Part 7: IoT Artifacts**
**Version:** 0.1.0
**Status:** Draft
**Last Updated:** 2026-01-27

---

## 1. Observation Object

The Observation is the atomic unit of evidence in Twin Earth NYC. Every piece of information captured by a sensor, witnessed by an NPC, or photographed by a player is stored as an Observation object. Observations are immutable once committed -- they can be annotated, linked, and re-evaluated, but never modified or deleted.

### 1.1 Schema Definition

```json
{
  "observation_id": "OBS_<type>_<stablehash>",
  "observer_id": "ENT_CCTV_TSQ_a7f3",
  "observer_type": "cctv|witness|device_telemetry|player_capture",
  "target_id": "ENT_DOOR_TSQ_b2c4",
  "target_class": "person|vehicle|door|device|anomaly|unknown",
  "time": "2026-01-27T14:30:00Z",
  "location": { "x": 0.0, "y": 0.0, "z": 0.0 },
  "modality": "video|audio|telemetry|visual_witness|photo",
  "confidence": 0.75,
  "tamperability": 0.2,
  "raw_data_ref": "path/to/capture",
  "metadata": {
    "weather": "rain",
    "lighting": "night",
    "occlusion_level": 0.3,
    "distance_to_target": 12.5
  }
}
```

### 1.2 Field Reference

| Field | Type | Required | Description |
|---|---|---|---|
| `observation_id` | string | Yes | Globally unique ID. Format: `OBS_<modality>_<stablehash8>`. The stable hash is derived from observer + target + time to ensure deterministic deduplication. |
| `observer_id` | string | Yes | Entity ID of the observer (camera, NPC, player, device). |
| `observer_type` | enum | Yes | Category of observer: `cctv`, `witness`, `device_telemetry`, `player_capture`. |
| `target_id` | string | Yes | Entity ID of the observed subject. May be `unknown` if not identified. |
| `target_class` | enum | Yes | Classification of the target: `person`, `vehicle`, `door`, `device`, `anomaly`, `unknown`. |
| `time` | ISO 8601 | Yes | Sim-time when observation was recorded. |
| `location` | object | Yes | World-space coordinates `{ x, y, z }` where the observation was made (observer position). |
| `modality` | enum | Yes | Sensory channel: `video`, `audio`, `telemetry`, `visual_witness`, `photo`. |
| `confidence` | float | Yes | Overall reliability of the observation [0.0, 1.0]. See Section 2 for computation. |
| `tamperability` | float | Yes | How easily this observation could be forged or spoofed [0.0, 1.0]. See Section 3. |
| `raw_data_ref` | string | No | Reference path to the raw capture data (video clip, audio recording, screenshot). Null for witness observations. |
| `metadata` | object | Yes | Environmental context at time of observation. All fields optional but should be populated when available. |
| `metadata.weather` | enum | No | `clear`, `rain`, `heavy_rain`, `fog`, `snow`. |
| `metadata.lighting` | enum | No | `daylight`, `streetlit_night`, `dark`, `billboard_glare`. |
| `metadata.occlusion_level` | float | No | Fraction of target obscured [0.0, 1.0]. |
| `metadata.distance_to_target` | float | No | Distance in meters from observer to target. |

---

## 2. Confidence Model

### 2.1 Confidence Tiers

| Tier | Range | Meaning | Typical Sources |
|---|---|---|---|
| Very High | 0.90 -- 1.00 | Near-certain identification | Close-range CCTV (< 5m), player photograph, device telemetry with crypto signature |
| High | 0.70 -- 0.89 | Reliable but not perfect | Mid-range CCTV, multiple corroborating witnesses, badge reader log |
| Moderate | 0.40 -- 0.69 | Useful but uncertain | Far-range CCTV, single witness, degraded conditions |
| Low | 0.10 -- 0.39 | Suggestive only | Distant/occluded camera view, rumor from unreliable NPC, poor weather at night |
| Negligible | 0.00 -- 0.09 | Essentially noise | Heavily degraded sensor, known-spoofed source, contradicted by other evidence |

### 2.2 Confidence Modifiers

Confidence is computed from a base value and modified by environmental factors. Modifiers are additive and the result is clamped to [0.0, 1.0].

**Weather Modifiers:**

| Condition | Modifier | Notes |
|---|---|---|
| Clear | +0.00 | Baseline conditions |
| Rain | -0.15 | Lens water, reduced visibility |
| Fog | -0.25 | Severe visibility reduction |
| Snow | -0.10 | Moderate visibility reduction |

**Lighting Modifiers:**

| Condition | Modifier | Notes |
|---|---|---|
| Daylight | +0.00 | Baseline conditions |
| Streetlit night | -0.10 | Adequate but reduced illumination |
| Dark | -0.30 | Minimal illumination, IR cameras partially compensate |
| Billboard glare | -0.05 | Localized overexposure artifacts |

**Occlusion Modifiers:**

| Condition | Modifier | Notes |
|---|---|---|
| None (0.0) | +0.00 | Target fully visible |
| Partial (0.1-0.5) | -0.20 | Target partially blocked by crowd, object, or structure |
| Heavy (0.5-1.0) | -0.40 | Target mostly or fully obscured |

**Distance Modifiers:**

| Range | Modifier | Notes |
|---|---|---|
| < 5m | +0.10 | Close range, high detail |
| 5 -- 15m | +0.00 | Nominal range |
| 15 -- 25m | -0.10 | Reduced detail |
| 25 -- 30m | -0.20 | Edge of effective range |

**Device Health Modifiers:**

| Status | Modifier | Notes |
|---|---|---|
| Good | +0.00 | Nominal operation |
| Degraded | -0.15 | Sensor wear, partial malfunction |
| Failing | -0.30 | Imminent failure, unreliable output |

**Computation Example:**

A CCTV camera with base confidence 0.80, during rain, at streetlit night, with partial occlusion, at 18m distance, in good health:

```
confidence = 0.80 + (-0.15) + (-0.10) + (-0.20) + (-0.10) + (0.00)
           = 0.80 - 0.55
           = 0.25
```

Result: **Low** tier -- suggestive only. This matches intuition: a rainy night with partial occlusion at moderate distance produces unreliable footage.

---

## 3. Tamperability Model

### 3.1 Tamperability Tiers

| Tier | Range | Examples |
|---|---|---|
| Hard to forge | 0.00 -- 0.20 | CCTV with chain-of-custody and crypto-signed frames, device telemetry with tamper-evident logging, biometric access logs |
| Moderate | 0.20 -- 0.50 | Standard CCTV (can be spoofed with effort and tech skill), player-taken photographs, badge reader logs (badge can be cloned) |
| Easy to spoof | 0.50 -- 0.80 | NPC witness reports (can be coerced or confused), kiosk alerts (can be falsely triggered), unsigned telemetry |
| Unreliable | 0.80 -- 1.00 | Rumors, hearsay, anonymous tips, data from compromised devices, observations during high anomaly activity |

### 3.2 Tamperability by Observer Type

| Observer Type | Base Tamperability | Notes |
|---|---|---|
| `cctv` | 0.15 | Low if chain-of-custody intact; rises to 0.40 if device was recently in `tampered` state |
| `device_telemetry` | 0.10 | Crypto-signed; very difficult to forge without system compromise |
| `player_capture` | 0.30 | Player photos are moderately trustworthy but lack automated chain-of-custody |
| `witness` | 0.60 | NPC witnesses are fallible, can be confused, coerced, or lying |

---

## 4. Evidence Fusion

### 4.1 Fusion Rule

Multiple independent, low-confidence observations of the same event can be combined to produce a higher-confidence composite observation.

**Two observations:**

```
combined_confidence = 1 - (1 - c1) * (1 - c2)
```

**Three or more observations (iterative):**

```
combined_confidence = 1 - product(1 - ci) for all i
```

**Example:** Three independent witnesses each report the same event with confidence 0.30:

```
combined = 1 - (1 - 0.30)^3
         = 1 - (0.70)^3
         = 1 - 0.343
         = 0.657
```

Three Low-tier observations fuse into a single Moderate-tier observation.

### 4.2 Fusion Conditions

Fusion applies only when all conditions are met:

| Condition | Requirement | Rationale |
|---|---|---|
| Independence | Different observer IDs | Same camera twice is not independent |
| Temporal proximity | Observations within 60 sim-seconds of each other | Ensures they refer to the same event |
| Spatial proximity | Observers within 50m of each other | Ensures they could plausibly observe the same event |
| Target agreement | Same `target_id` or compatible `target_class` | Cannot fuse observations of different targets |

### 4.3 Fusion Limitations

- Fused confidence is capped at 0.95. No amount of weak evidence produces certainty.
- If any contributing observation has tamperability > 0.7, it is excluded from fusion.
- Fused observations create a new Observation object with `observer_type: "fused"` and references to source observations.

---

## 5. CCTV Behavior (v1)

### 5.1 Detection Capabilities

| Capability | Confidence Basis | Notes |
|---|---|---|
| Motion detection | Always active | Binary: motion present or absent. No classification. |
| Proximity detection | Always active | Entities within FOV cone are detected. |
| Identity class | At computed confidence | Classifies as `person`, `vehicle`, `unknown`. Does not identify individuals by name without additional system support. |
| Suspicious actions | At reduced confidence (x0.7) | Detects: loitering (> 5 min stationary), running, forced entry, fighting. Classification is probabilistic. |

### 5.2 Data Retention

| Phase | Duration | Content | Storage Cost |
|---|---|---|---|
| Raw video | 1 sim-hour | Full-resolution feed | High |
| Summary | 24 sim-hours | Key frames, motion events, observation logs | Medium |
| Key events | Permanent | Forced entry, anomaly, flagged observations | Low |

After the raw retention window closes, only the summary and flagged key events remain. Investigations that need raw footage must access it within the 1-hour window or it is lost.

### 5.3 Privacy Model

In v1, there is no ethical occlusion. NPCs have no privacy expectation in public space within the game simulation. All public-area CCTV operates without restriction. Interior cameras (lobby, hallway) follow the same rules. Private interiors (hotel rooms, offices) do not have CCTV coverage.

---

## 6. Example Evidence Records

### 6.1 Door Forced Open

```json
{
  "observation_id": "OBS_telemetry_d4e5f6a1",
  "observer_id": "ENT_DOOR_TSQ_AMC_02",
  "observer_type": "device_telemetry",
  "target_id": "ENT_DOOR_TSQ_AMC_02",
  "target_class": "door",
  "time": "2026-01-27T02:14:33Z",
  "location": { "x": 245.3, "y": 0.0, "z": 102.7 },
  "modality": "telemetry",
  "confidence": 0.95,
  "tamperability": 0.10,
  "raw_data_ref": "telemetry/door/ENT_DOOR_TSQ_AMC_02/20260127_021433.log",
  "metadata": {
    "weather": "clear",
    "lighting": "streetlit_night",
    "occlusion_level": 0.0,
    "distance_to_target": 0.0
  }
}
```

**Context:** The AMC Empire 25 side exit was forced open at 2:14 AM. The door's own contact sensor and lock mechanism telemetry recorded the forced state transition with very high confidence. Device telemetry has low tamperability because it is crypto-signed and locally logged.

---

### 6.2 Vehicle Crash

```json
{
  "observation_id": "OBS_video_b7c8d9e2",
  "observer_id": "ENT_CCTV_TSQ_07",
  "observer_type": "cctv",
  "target_id": "ENT_VEH_unknown_01",
  "target_class": "vehicle",
  "time": "2026-01-27T11:42:17Z",
  "location": { "x": 220.8, "y": 5.5, "z": 130.4 },
  "modality": "video",
  "confidence": 0.82,
  "tamperability": 0.15,
  "raw_data_ref": "video/cctv/ENT_CCTV_TSQ_07/20260127_114217_clip.mp4",
  "metadata": {
    "weather": "clear",
    "lighting": "daylight",
    "occlusion_level": 0.1,
    "distance_to_target": 8.3
  }
}
```

**Context:** A vehicle collision was captured by a CCTV camera mounted at the corner of 44th Street and Broadway. Clear daylight, minimal occlusion (slight crowd at edge of frame), and moderate distance yield a High-tier confidence of 0.82. The vehicle itself could not be positively identified (no plate reader in v1), so target_id is provisional.

---

### 6.3 NPC Fight

```json
{
  "observation_id": "OBS_visual_witness_f3a4b5c6",
  "observer_id": "ENT_NPC_vendor_12",
  "observer_type": "witness",
  "target_id": "ENT_NPC_a3b7",
  "target_class": "person",
  "time": "2026-01-27T19:55:08Z",
  "location": { "x": 232.1, "y": 0.0, "z": 119.8 },
  "modality": "visual_witness",
  "confidence": 0.52,
  "tamperability": 0.60,
  "raw_data_ref": null,
  "metadata": {
    "weather": "rain",
    "lighting": "streetlit_night",
    "occlusion_level": 0.35,
    "distance_to_target": 6.0
  }
}
```

**Context:** A street vendor NPC near the TKTS steps witnessed a fight between two NPCs at 7:55 PM during rain. The witness was 6 meters away but the crowd partially occluded the view and rain further degraded observation quality. As a witness report, tamperability is high -- the vendor could be confused about identities or details. Confidence lands at Moderate tier (0.52), enough to be useful but not definitive.

---

### 6.4 Anomaly Detection

```json
{
  "observation_id": "OBS_telemetry_e1d2c3b4",
  "observer_id": "ENT_CCTV_TSQ_04",
  "observer_type": "cctv",
  "target_id": "ANOMALY_ZONE_TKTS_01",
  "target_class": "anomaly",
  "time": "2026-01-27T23:18:44Z",
  "location": { "x": 228.5, "y": 5.5, "z": 116.0 },
  "modality": "video",
  "confidence": 0.41,
  "tamperability": 0.15,
  "raw_data_ref": "video/cctv/ENT_CCTV_TSQ_04/20260127_231844_anomaly.mp4",
  "metadata": {
    "weather": "clear",
    "lighting": "dark",
    "occlusion_level": 0.0,
    "distance_to_target": 14.0
  }
}
```

**Context:** A CCTV camera near the TKTS steps detected anomalous visual artifacts at 11:18 PM -- shimmering distortion, light bending, and brief spatial discontinuities consistent with portal activity. Despite clear weather and no occlusion, the dark lighting and moderate distance reduce confidence. Additionally, anomalies are inherently difficult to classify with standard visual systems, further reducing the confidence to Moderate tier. The camera's tamper-evident recording remains trustworthy.

---

### 6.5 Player Photographing Evidence

```json
{
  "observation_id": "OBS_photo_a5b6c7d8",
  "observer_id": "ENT_PLAYER_01",
  "observer_type": "player_capture",
  "target_id": "ENT_NPC_suspect_09",
  "target_class": "person",
  "time": "2026-01-27T15:03:22Z",
  "location": { "x": 237.9, "y": 0.0, "z": 121.5 },
  "modality": "photo",
  "confidence": 0.88,
  "tamperability": 0.30,
  "raw_data_ref": "player/captures/ENT_PLAYER_01/20260127_150322_photo.png",
  "metadata": {
    "weather": "clear",
    "lighting": "daylight",
    "occlusion_level": 0.05,
    "distance_to_target": 3.2
  }
}
```

**Context:** The player used their in-game camera to photograph a suspect NPC at close range (3.2m) during clear daylight near the pedestrian plaza on 45th Street. Excellent conditions yield High-tier confidence (0.88). The slight occlusion is from a passing pedestrian at the edge of frame. Tamperability is moderate -- player photos lack the crypto chain-of-custody of CCTV but are generally considered reliable evidence in the investigation system.

---

*End of Evidence Schema v0*
