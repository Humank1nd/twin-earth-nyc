# Coupling Rules Sheet v0

**Twin Earth NYC -- Part 7: IoT Artifacts**
**Version:** 0.1.0
**Status:** Draft
**Last Updated:** 2026-01-27

---

## 1. Overview

Artifacts do not operate in isolation. Their behavior is continuously modulated by the simulation's environmental fields -- crowd density, weather, lighting, noise, anomaly intensity, and Heat level. This document defines every coupling between simulation fields and artifact behavior, the authority dispatch loop that consumes artifact events, and the criminal exploitation mechanics that allow players and NPCs to subvert artifacts.

---

## 2. Artifact-Field Coupling Table

### 2.1 Crowd Density Couplings

| Field | Artifact | Coupling Effect | Formula / Rule |
|---|---|---|---|
| Crowd Density | CCTV Camera | Occlusion increases with crowd density, reducing observation confidence | `effective_confidence = base_confidence * (1 - 0.5 * density_normalized)` where `density_normalized` is [0.0, 1.0] for the camera's coverage zone |
| Crowd Density | Witness (NPC) | More potential witnesses available in dense crowds | `witness_count = floor(density * area * 0.1)` where `area` is the observation zone in square meters |
| Crowd Density | Information Kiosk | Physical access blocked at high density; crowd prevents approach | `if density_normalized > 0.8 then kiosk_accessible = false` |
| Crowd Density | Crosswalk Signal | Pedestrian sensor always triggered; walk phase requested continuously | `if density_normalized > 0.3 then pedestrian_present = true` (sensor always activated) |
| Crowd Density | Door/Lock | Increased door event rate as more people enter/exit buildings | `door_event_rate = base_rate * (1 + density_normalized * 0.5)` |

**Notes:** `density_normalized` is the crowd density in the artifact's immediate zone, normalized to [0.0, 1.0] where 0.0 = empty and 1.0 = maximum simulated density (shoulder-to-shoulder, approximately 4 persons per square meter). Typical Times Square afternoon density is 0.3-0.5. New Year's Eve approaches 0.9-1.0.

### 2.2 Weather Couplings

| Field | Artifact | Coupling Effect | Formula / Rule |
|---|---|---|---|
| Weather (rain) | CCTV Camera | Image degradation from water on lens and reduced visibility | `effective_confidence = base_confidence * 0.7` during rain |
| Weather (rain) | Information Kiosk | Pedestrians shelter indoors; reduced kiosk interaction | `usage_probability = base_usage * 0.5` during rain |
| Weather (rain) | Door/Lock | More people entering buildings for shelter | `door_event_rate = base_rate * 1.5` during rain |
| Weather (fog) | CCTV Camera | Severe visibility reduction | `effective_confidence = base_confidence * 0.5` during fog |
| Weather (snow) | CCTV Camera | Moderate lens occlusion and visibility reduction | `effective_confidence = base_confidence * 0.65` during snow |
| Weather (rain/snow) | Crosswalk Signal | Sensor reliability slightly degraded | `sensor_detection_probability = base * 0.9` during precipitation |
| Weather (rain/snow) | All outdoor artifacts | Increased failure rate | See `artifact-catalog-v0.md` Section 4.4 for multipliers |

### 2.3 Light Level Couplings

| Field | Artifact | Coupling Effect | Formula / Rule |
|---|---|---|---|
| Light Level | CCTV Camera | Observation quality depends on ambient light | `effective_confidence = base_confidence * (light_level / reference_light)` where `reference_light = 1.0` (full daylight). Times Square billboards provide a floor of ~0.4 even at night. |
| Light Level | Witness (NPC) | Perception quality degrades in low light | `witness_confidence = base_confidence * light_factor` where `light_factor`: daylight = 1.0, streetlit = 0.7, dark = 0.3, billboard_lit = 0.5 |
| Light Level | Information Kiosk | Screen readability improves in low light (backlit display) | No penalty; screen brightness auto-adjusts. `screen_visibility_range` increases from 5m to 8m at night. |

### 2.4 Noise Level Couplings

| Field | Artifact | Coupling Effect | Formula / Rule |
|---|---|---|---|
| Noise Level | Witness (NPC) | Communication difficulty reduces witness accuracy for verbal descriptions | `witness_accuracy = base_accuracy * (1 - noise_normalized * 0.3)` where `noise_normalized` is [0.0, 1.0] |
| Noise Level | Information Kiosk | Audio alerts less effective | `if noise_normalized > 0.7 then kiosk_audio_effective = false` (visual alerts still function) |
| Noise Level | Door/Lock | Forced entry sound masked by ambient noise | `force_detection_probability = base * (1 - noise_normalized * 0.5)` -- nearby witnesses less likely to hear |

### 2.5 Anomaly Couplings

| Field | Artifact | Coupling Effect | Formula / Rule |
|---|---|---|---|
| Anomaly Intensity | CCTV Camera | Signal interference degrades video feed; false positives increase | `effective_confidence = base_confidence * (1 - anomaly_intensity * 0.5)` AND `false_positive_rate = base_fpr * (1 + anomaly_intensity)` |
| Anomaly Intensity | All Devices | Latency spike from electromagnetic/reality distortion | `effective_latency = base_latency * (1 + anomaly_intensity * 2)` |
| Anomaly Intensity | Information Kiosk | Spontaneous alert display triggered by nearby anomaly | `if anomaly_intensity > 0.5 AND distance_to_anomaly < anomaly_radius then trigger kiosk.alert` with `alert_type = "anomaly_warning"` |
| Anomaly Intensity | Door/Lock | Electronic locks may malfunction | `if anomaly_intensity > 0.7 AND distance_to_anomaly < anomaly_radius then lock_malfunction_probability = anomaly_intensity * 0.3` |
| Anomaly Intensity | Traffic Light | Timing disruption | `if anomaly_intensity > 0.8 AND distance_to_anomaly < anomaly_radius then signal_desync_probability = anomaly_intensity * 0.2` |
| Anomaly Intensity | CCTV Camera | Anomaly itself may be visually detectable | Anomalies with `intensity > 0.3` produce detectable visual artifacts (shimmer, distortion) within camera FOV |

### 2.6 Heat Level Couplings

| Field | Artifact | Coupling Effect | Formula / Rule |
|---|---|---|---|
| Heat Level | All Devices | Increased failure rate across the board | `effective_failure_rate = base_failure_rate * (1 + Heat_level)` |
| Heat Level | CCTV Camera | Increased institutional scrutiny; cameras process more aggressively | `observation_rate = base_rate * (1 + institutional_Heat * 0.5)` -- more frequent identity checks, lower threshold for "suspicious" classification |
| Heat Level | All Networked Devices | Increased packet loss on wireless links | See `event-bus-spec-v0.md` Section 6: `effective_loss = base_loss + (max_loss - base_loss) * Heat_level` |
| Heat Level | Door/Lock | Security tightening; auto-lock timers shortened | `auto_lock_timer = base_timer * (1 - Heat_level * 0.5)` -- at max Heat, doors lock 50% faster |
| Heat Level | Information Kiosk | More frequent authority-pushed alerts | Authority dispatch pushes alerts to kiosks more aggressively at higher Heat |

---

## 3. Coupling Interaction Examples

### 3.1 Rainy Night at High Heat

Scenario: Rain, streetlit night, Heat at 0.7, crowd density 0.2 (light foot traffic due to rain).

**CCTV Camera (ENT_CCTV_TSQ_04) observing TKTS steps:**

```
base_confidence = 0.80
rain_factor:     * 0.70  = 0.56
light_factor:    * (0.4 / 1.0) = 0.224   (billboard ambient light floor)
crowd_occlusion: * (1 - 0.5 * 0.2) = 0.90 * 0.224 = 0.202
anomaly:         * 1.0 (no anomaly) = 0.202
```

Effective confidence: **0.20** (Low tier). The camera can detect motion and general shapes but cannot reliably identify individuals.

**Heat effects on this camera:**
- Failure rate: base * (1 + 0.7) = base * 1.7
- Observation rate: base * (1 + 0.7 * 0.5) = base * 1.35 (more aggressive scanning)
- Packet loss: 5% + (20% - 5%) * 0.7 = 15.5%

### 3.2 Anomaly Spike During Crowded Afternoon

Scenario: Clear day, crowd density 0.6 (typical afternoon), anomaly intensity 0.6, Heat 0.3.

**CCTV Camera observing anomaly zone:**

```
base_confidence = 0.80
weather:         * 1.0 = 0.80
light:           * 1.0 = 0.80
crowd_occlusion: * (1 - 0.5 * 0.6) = 0.70 * 0.80 = 0.56
anomaly:         * (1 - 0.6 * 0.5) = 0.70 * 0.56 = 0.392
```

Effective confidence: **0.39** (Low tier). False positive rate doubled.

**Kiosk (ENT_KIOSK_TSQ_03) in plaza:**
- Anomaly > 0.5 and within radius: triggers `public_info.kiosk.alert` with `anomaly_warning`
- Crowd density 0.6 < 0.8: kiosk still accessible
- Latency: 200ms * (1 + 0.6 * 2) = 440ms

**Doors near anomaly:**
- Lock malfunction probability: 0.6 * 0.3 = 0.18 (18% chance per check)
- If malfunction: random state change (locked <-> unlocked)

---

## 4. Authority Dispatch Loop

When artifacts generate evidence or alerts, the Authority system classifies them by severity and dispatches appropriate responses. This creates a feedback loop: more evidence generates higher Heat, which increases surveillance intensity, which generates more evidence.

### 4.1 Severity Classification

| Severity | Criteria | Examples |
|---|---|---|
| **Low** | Routine event, no immediate concern | Single camera motion event, door opened with valid credential, kiosk interaction |
| **Medium** | Notable event requiring attention | Repeated failed door access attempts, sustained high motion in unexpected area, single witness report of suspicious behavior |
| **High** | Significant incident requiring multi-unit response | Forced door entry, camera tampered, multiple corroborating reports of violence or anomaly, kiosk alert triggered |
| **Critical** | Major incident requiring full response | Anomaly spike > 0.8, multiple forced entries simultaneously, confirmed violent crime, reality distortion event |

### 4.2 Dispatch Rules

| Severity | Response | Latency | Escalation |
|---|---|---|---|
| **Low** | Log only; no active dispatch | N/A | Auto-escalates to Medium if 3+ Low events from same zone within 10 sim-minutes |
| **Medium** | Nearest patrol unit notified via radio | 30s -- 120s notification | Escalates to High if responding unit confirms incident |
| **High** | 2+ units dispatched; perimeter consideration for affected block | 60s -- 180s first arrival | Escalates to Critical if situation expands or anomaly detected |
| **Critical** | Full response: 4+ units, cordons established, possible road closures; Traffic signals may be overridden to facilitate emergency access | 120s -- 300s full deployment | Heat level increased by 0.2; sustained critical events lock Heat at maximum |

### 4.3 Dispatch Flow

```
[Artifact Event / Evidence]
        |
        v
[Severity Classifier] -- examines: event type, confidence, source reliability,
        |                  zone current Heat, recent event history
        v
[Severity: Low / Medium / High / Critical]
        |
        +-- Low ------> [Log to dispatch database] --> [Monitor for escalation]
        |
        +-- Medium ----> [Notify nearest patrol unit]
        |                     |
        |                     v
        |                [Unit acknowledges? Y/N]
        |                     |
        |                     +-- N (timeout 60s) --> Escalate to High
        |                     +-- Y --> [Unit responds, reports back]
        |
        +-- High ------> [Dispatch 2+ units]
        |                     |
        |                     v
        |                [Establish perimeter?]
        |                     |
        |                     +-- if anomaly detected --> Escalate to Critical
        |                     +-- if contained --> [De-escalate after resolution]
        |
        +-- Critical ---> [Full response activation]
                               |
                               v
                          [Road closures, cordons, signal override]
                               |
                               v
                          [Heat += 0.2, sustained events lock Heat at max]
```

### 4.4 Heat Feedback

The dispatch loop feeds back into the Heat system:

| Event | Heat Effect |
|---|---|
| Medium dispatch | Heat += 0.02 |
| High dispatch | Heat += 0.05 |
| Critical dispatch | Heat += 0.20 |
| Successful resolution | Heat -= 0.03 (slow decay) |
| False alarm confirmed | Heat -= 0.01 |
| Sustained critical (> 10 min) | Heat locked at current level (no decay) |

---

## 5. Criminal Exploitation

Players and criminal NPCs can interact with artifacts in adversarial ways. Every exploitation action has a cost (skill, tools, time), a risk (evidence generated, Heat impact), and consequences.

### 5.1 Exploitation Actions

| Action | Skill / Tool Required | Time Required | Risk Level | Evidence Generated |
|---|---|---|---|---|
| **Jam camera** | Tech skill (level 2+) + electronic jammer device | 5 seconds (must remain within 10m of target) | High -- increases zone Heat, detectable RF signature | `security.camera.tampered` event emitted; RF signature detectable by sweep within 30m; jammer device is physical evidence if found |
| **Blind camera** | Physical access + spray paint / tape / laser pointer | 3 seconds (must reach camera mount) | Medium -- physically visible, tamper event emitted | `security.camera.tampered` event; physical evidence (paint residue, tape); nearby witnesses may observe |
| **Spoof door access** | Cloned credential + proximity OR tech skill (level 3+) + bypass tool | 15-60 seconds depending on lock class | Medium-High -- failed attempts are logged, success leaves auth trail | `access.door.state_changed` event with cloned credential ID; `access.door.failed_auth` events on failed attempts; credential clone is traceable |
| **Force door** | Strength check (high) OR breaching tool | 10-30 seconds depending on door class | Very High -- loud, damages door, triggers forced state | `access.door.state_changed` with `new_state: "forced"` and `method: "force"`; noise audible within 20m; physical damage visible |
| **Trigger false kiosk alert** | Tech skill (level 2+) + proximity (within 2m) | 30 seconds | Low-Medium -- distracts authorities temporarily; suspicious if pattern detected | `public_info.kiosk.alert` event emitted with spoofed content; if 2+ false alerts from same zone within 30 min, pattern detection flags them as `suspicious` |
| **Intercept camera feed** | Tech skill (level 4+) + network access + specialized software | 120 seconds setup, then continuous | Medium -- no tamper alert, but network anomaly detectable on audit | No immediate event; network audit (if triggered) reveals unauthorized feed access; intercepted data can be used for planning |
| **Loop camera feed** | Tech skill (level 4+) + network access + pre-recorded footage | 60 seconds setup | High -- creates temporal inconsistency detectable by review | `security.camera.observation` events continue but with looped content; temporal analysis (matching timestamps to other cameras) can detect the loop |

### 5.2 Exploitation Risk Matrix

| Action | Immediate Detection Probability | Post-Hoc Detection Probability | Heat Impact (if detected) | Heat Impact (if undetected) |
|---|---|---|---|---|
| Jam camera | 0.60 (RF sweep, tamper event) | 0.90 (gap in footage reviewed) | +0.10 | +0.02 (missing footage noted) |
| Blind camera | 0.70 (tamper event, witness) | 0.95 (physical evidence) | +0.08 | +0.02 |
| Spoof door access | 0.20 (only on failure) | 0.50 (credential audit) | +0.05 | 0.00 |
| Force door | 0.85 (noise, tamper event) | 0.99 (physical damage) | +0.15 | +0.05 |
| False kiosk alert | 0.10 (first occurrence) | 0.40 (pattern detection) | +0.03 | 0.00 |
| Intercept feed | 0.05 (no immediate alert) | 0.30 (network audit) | +0.08 | 0.00 |
| Loop feed | 0.15 (temporal analysis) | 0.60 (cross-camera review) | +0.12 | +0.03 |

### 5.3 Counter-Exploitation (Authority Tools)

Authorities have access to the following countermeasures when exploitation is detected:

| Countermeasure | Trigger | Effect | Cost |
|---|---|---|---|
| RF sweep | Camera tamper event in zone | Detects active jammers within 30m; locates jammer with 5m precision | Requires patrol unit with sweep equipment; 60s scan time |
| Credential audit | 3+ failed auth attempts on same door | Flags credential as compromised; revokes cloned badge IDs | Automatic; 5 min processing delay |
| Camera cross-reference | Single camera tampered or looped | Nearby cameras check for corroborating footage | Automatic; requires adjacent camera coverage |
| Network audit | Triggered by anomalous traffic patterns | Detects unauthorized feed access, injection attacks | Manual dispatch of tech unit; 300s audit time |
| Physical patrol increase | High-severity dispatch | Additional units sweep zone, increasing chance of catching exploiter | Heat-driven; 2+ units added to zone for 30 sim-minutes |

---

## 6. Coupling Summary Matrix

A condensed reference of all field-to-artifact couplings for implementation.

| Field \ Artifact | Traffic Light | Crosswalk Signal | CCTV Camera | Info Kiosk | Door/Lock | Witness (NPC) |
|---|---|---|---|---|---|---|
| **Crowd Density** | -- | Sensor always active > 0.3 | Confidence * (1 - 0.5d) | Blocked if d > 0.8 | Event rate * (1 + 0.5d) | Count = floor(d * A * 0.1) |
| **Rain** | Failure x1.3 | Sensor x0.9 | Confidence x0.7 | Usage x0.5 | Event rate x1.5 | -- |
| **Fog** | -- | -- | Confidence x0.5 | -- | -- | Confidence x0.4 |
| **Snow** | Failure x1.5 | Sensor x0.9 | Confidence x0.65 | -- | -- | -- |
| **Light Level** | -- | -- | Confidence * (L/Lref) | Visibility improves | -- | Confidence * L_factor |
| **Noise Level** | -- | -- | -- | Audio disabled > 0.7 | Force detection reduced | Accuracy * (1 - 0.3n) |
| **Anomaly** | Desync if I > 0.8 | -- | Confidence * (1 - 0.5I), FPR * (1+I) | Alert if I > 0.5 | Malfunction if I > 0.7 | Panic behavior > 0.6 |
| **Heat** | -- | -- | Obs rate * (1 + 0.5H) | More authority alerts | Auto-lock faster | More willing to report |
| **Heat (all)** | Failure * (1+H) | Failure * (1+H) | Failure * (1+H) | Failure * (1+H) | Failure * (1+H) | -- |
| **Anomaly (all)** | Latency * (1+2I) | Latency * (1+2I) | Latency * (1+2I) | Latency * (1+2I) | Latency * (1+2I) | -- |

**Legend:** `d` = density_normalized, `L` = light_level, `Lref` = reference_light, `n` = noise_normalized, `I` = anomaly_intensity, `H` = Heat_level, `A` = area in m^2.

---

*End of Coupling Rules Sheet v0*
