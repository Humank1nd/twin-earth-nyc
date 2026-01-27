# Reality Heat + Evidence Economy Spec v0

> **Twin Earth NYC** -- Part 11: Multiverse Gameplay
> **Document:** Reality Heat + Evidence Economy Specification
> **Version:** 0.1.0
> **Status:** Draft
> **Last Updated:** 2026-01-27

---

## Table of Contents

1. [Overview](#overview)
2. [Heat Channels](#heat-channels)
3. [Cross-Channel Coupling](#cross-channel-coupling)
4. [Heat Thresholds for Times Square](#heat-thresholds-for-times-square)
5. [Heat Event Chain Example](#heat-event-chain-example)
6. [Heat Coupling to Portals](#heat-coupling-to-portals)
7. [Evidence Economy](#evidence-economy)
8. [Belief Meter](#belief-meter)
9. [Rumor System](#rumor-system)
10. [Misinformation Actions](#misinformation-actions)
11. [Integration Notes](#integration-notes)

---

## Overview

**Reality Heat** is the core consequence system of Twin Earth NYC. It measures the degree to which multiverse activity has disrupted normal life in Times Square and surrounding neighborhoods. Heat is not a single number -- it is a four-channel system, each tracking a different dimension of disruption.

**Evidence** is the currency that feeds Heat. Every action the player takes (or fails to prevent) generates evidence across three classes. Evidence accumulates in a persistent ledger and drives Heat increases, faction responses, and the Belief Meter.

### Design Intent

Heat is the "bill" for multiverse gameplay. Every portal opened, every artifact imported, every anomaly left unsealed generates Heat. The player must constantly balance the utility of multiverse actions against their Heat cost. High Heat is not a game-over condition -- it is a world-state change that makes everything harder, more expensive, and more dangerous.

The system rewards careful, clean operations (low Heat generation) and punishes reckless play (high Heat spirals). However, some Heat is unavoidable -- the player is doing extraordinary things in a realistic city. The strategic question is always: "How much Heat can I afford for this action?"

---

## Heat Channels

Heat is tracked across four independent channels. Each channel has its own sources, sinks, decay rate, and threshold effects. Channels interact through cross-channel coupling rules (see Section 3).

### Channel Definitions

| Channel | What It Measures | Sources (Raises Heat) | Sinks (Lowers Heat) | Natural Decay Rate |
|---|---|---|---|---|
| **Physical** | Tangible damage to the environment -- structural, vehicular, bodily | Explosions, vehicle crashes, structural damage, portal energy bursts, combat collateral, falling debris | Time (natural decay), player cleanup actions, city repair crews (NPC), insurance/construction resolution | -0.02 per minute |
| **Social** | Public awareness and emotional response to anomalous events | Witness reports, crowd panic, media coverage, visible anomalies, social media posts, public confrontations | Time (natural decay), authority reassurance (NYPD "everything is fine" messaging), player-initiated coverup actions (misdirection, memory suppression) | -0.01 per minute |
| **Institutional** | Government/authority awareness and systemic response capability | Evidence accumulation in official records, authority encounters with anomalies, surveillance data triggers, repeat offenses at known locations, formal reports filed | Time (very slow natural decay), player cooperation with authorities (sharing intel, assisting investigations), legal resolution of incidents | -0.005 per minute |
| **Ecological** | Reality-level health of the local dimension -- how much the fabric of 1218 has been stressed | Anomaly residue accumulation, portal entropy_bleed persistence, reality distortion events, exotic material contamination, failed containment | Time (very slow natural decay), successful containment actions, Strange's intervention (reality repair rituals), portal residue cleanup | -0.003 per minute |

### Decay Rate Comparison

```
Decay speed (fastest to slowest):

Physical:      -0.02/min  ████████████████████  (50 min from 1.0 to 0.0)
Social:        -0.01/min  ██████████            (100 min from 1.0 to 0.0)
Institutional: -0.005/min █████                 (200 min from 1.0 to 0.0)
Ecological:    -0.003/min ███                   (~333 min from 1.0 to 0.0)

Physical damage fades fastest (city repairs itself).
Social panic fades moderately (people forget, move on).
Institutional memory is long (records persist, investigations continue).
Ecological damage is nearly permanent (reality heals very slowly).
```

### Channel Detail: Physical

Physical Heat measures the tangible, observable damage to the urban environment. This is the most immediate and visible form of Heat but also the fastest to decay.

| Threshold | Value Range | World State | NPC Behavior | Player Impact |
|---|---|---|---|---|
| **Low** | 0.0 -- 0.3 | Cosmetic damage: cracked pavement, broken windows, scorch marks. Normal city wear-and-tear plus anomaly residue. | NPCs step around damage, comment casually ("construction, huh?"). City maintenance crews schedule repairs (days). | Minimal. Damage is inconspicuous. |
| **Medium** | 0.3 -- 0.6 | Structural concerns: visibly damaged buildings, road surface warping, utility disruptions (flickering lights, water main stress). | NPCs avoid damaged areas. Concerned comments. Some businesses close temporarily. Construction barriers appear. | Road closures alter patrol routes and pedestrian flow. Some areas become difficult to access without climbing/alternate paths. |
| **High** | 0.6 -- 0.8 | Area evacuation: significant structural damage, unstable buildings cordoned off, emergency services active. Visible emergency response (fire trucks, ambulances, hazmat). | NPCs evacuate the area. Emergency workers take over. Crowds form at perimeter. Media arrives. | Player access restricted. Emergency response NPCs may question the player. Movement through affected area requires stealth or credentials. |
| **Crisis** | 0.8 -- 1.0 | Military consideration: catastrophic damage, buildings at risk of collapse, infrastructure failure. Federal emergency management assessment. National Guard staging possible. | Civilians fully evacuated. Only emergency/military personnel present. Media helicopters overhead. | Area is a restricted zone. Player must infiltrate or use credentials to access. Any action in the area generates maximum evidence. |

### Channel Detail: Social

Social Heat measures public awareness, emotional state, and collective behavior in response to anomalous events.

| Threshold | Value Range | World State | NPC Behavior | Player Impact |
|---|---|---|---|---|
| **Low** | 0.0 -- 0.3 | Rumors: vague talk of "weird stuff," unreliable social media posts, conspiracy forum activity. Mainstream unaware. | NPCs go about normal life. Occasional overheard conversation about "strange lights." Tourist behavior unchanged. | Player can operate with minimal social cover. Most actions pass unnoticed. |
| **Medium** | 0.3 -- 0.6 | Social media buzz: trending local hashtags, increased foot traffic from curious onlookers, local news coverage. "Something is happening in Times Square" is a known topic. | NPCs actively look for anomalies. Phones out more often. Crowd density increases near known anomaly sites (rubbernecking). Some NPCs approach the player to ask questions. | Increased witness density makes stealth harder. Social media documentation means any visible action has a higher chance of going viral. Player must be more careful about anomaly exposure. |
| **High** | 0.6 -- 0.8 | Protests/panic: organized citizen responses (protests demanding answers, or panic-driven avoidance). Mainstream media coverage. Political statements. | NPCs are polarized: some avoid Times Square entirely (fear), others flock to it (curiosity, protest). Crowd behavior is volatile -- panic propagation is faster, mobs form more easily. | Player faces unpredictable crowd behavior. Social cover is nearly impossible -- every bystander is a potential witness/recorder. Faction interactions become more charged. |
| **Crisis** | 0.8 -- 1.0 | Mass evacuation / mass gathering: depending on belief meter, either mass panic evacuation or mass gathering (people who believe demanding answers). National news coverage. Government spokespeople address the situation. | Extreme NPC behavior: evacuation stampedes, protest blockades, or eerie emptiness (everyone left). Remaining NPCs are highly alert and emotional. | Player is in a transformed social landscape. Normal social interactions are impossible. Every action is observed and reacted to. Faction allegiances become critical for navigation. |

### Channel Detail: Institutional

Institutional Heat measures the awareness and response capability of governmental and law enforcement systems. This is the slowest-decaying and most consequential channel for long-term gameplay.

| Threshold | Value Range | World State | Authority Behavior | Player Impact |
|---|---|---|---|---|
| **Low** | 0.0 -- 0.2 | Routine: standard NYPD patrols, standard surveillance, no special attention to anomaly zones. Reports filed but low-priority. | Beat cops on standard routes. 911 dispatch treats anomaly reports as "disturbance" calls. No specialized units. | Player operates freely. Police encounters are routine and easily managed. |
| **Medium** | 0.2 -- 0.4 | Dedicated investigation: detectives assigned to anomaly case file. Surveillance cameras re-tasked to cover known anomaly hotspots. Intelligence analysts review sensor data. | Increased patrol density near anomaly sites. Plainclothes detectives observing. Forensic teams may visit residue patches. Player may be questioned if present at multiple anomaly sites. | Player encounters investigators. Repeat visits to anomaly sites risk identification. CCTV coverage of player's operating areas increases. |
| **High** | 0.4 -- 0.7 | Task force: multi-agency task force formed. Federal involvement (FBI anomalous events liaison). Access restrictions at key locations. Surveillance network expanded. | Specialized response teams (not SWAT -- more like hazmat/intel hybrid). Undercover agents in Times Square. Sensor network actively hunting for anomaly signatures. Warrants issued for "persons of interest." | Player faces active investigation. If identified, warrants and pursuit. Access to anomaly sites requires planning to avoid detection. Faction contacts may be surveilled. Player's safe houses at risk. |
| **Crisis** | 0.7 -- 1.0 | State-level response: Governor's emergency declaration. National Security Council briefing. Military assets on standby. All anomaly evidence classified. Civilian access to Times Square severely restricted. | Full government response. Military checkpoints. Electronic surveillance blanket. Any anomalous energy signature triggers immediate armed response. Player is a high-priority target if identified. | Player is operating in a hostile institutional environment. Every action risks confrontation with armed, organized, resourced opponents. Faction alliances become essential for survival. Going underground may be necessary. |

### Channel Detail: Ecological

Ecological Heat measures the health of local reality -- how much the dimensional fabric of EARTH-1218 has been stressed by portal activity, anomaly residue, and exotic material contamination.

| Threshold | Value Range | World State | Environmental Effects | Player Impact |
|---|---|---|---|---|
| **Low** | 0.0 -- 0.1 | Minor glitches: imperceptible to the untrained eye. Scanner shows trace anomaly readings. Baseline reality is intact. | Occasional sensor blip. Pigeons slightly disoriented near residue patches. Electronics experience rare single-frame glitches. | Player's scanner detects faint background readings. No gameplay impact. |
| **Medium** | 0.1 -- 0.3 | Persistent anomaly patches: visible to attentive observers. Multiple residue locations. Background anomaly reading elevated across the neighborhood. | Persistent shimmer at residue sites. Electronics malfunction more frequently (phones restart, screens flicker). Animals avoid anomaly zones (pigeons, rats, dogs). Temperature microfluctuations near residue. | Anomaly sites are detectable without a scanner (visual cues). NPC behavior near residue changes (avoidance). Evidence generation is passively elevated. |
| **High** | 0.3 -- 0.5 | Reality instability: spontaneous micro-anomalies. Areas where physics behave slightly wrong (objects falling at wrong speed, shadows pointing wrong direction). Persistent distortion zones. | Spontaneous micro-portals (visual only -- not traversable, but alarming). Gravity fluctuations within 5m of major residue patches. Electronics fail reliably in anomaly zones. Structural stress from reality distortion. | Micro-anomalies generate Social and Physical Heat on their own (feedback loop). Player must manage Ecological Heat to prevent cascading effects. Portal stability in the area is reduced. |
| **Crisis** | 0.5 -- 1.0 | Reality fracture risk: the dimensional fabric is severely compromised. Spontaneous portal formation possible. Environmental conditions become hazardous. Strange considers drastic intervention. | Spontaneous traversable micro-portals (brief, dangerous, unpredictable destinations). Persistent gravity anomalies. Structural collapse from sustained reality distortion. Exotic contamination spreads. Area may become uninhabitable. | This is an emergency state. Portal operations become extremely unpredictable. Strange's faction shifts to crisis mode. The player must prioritize Ecological containment or face cascading system failure. End-game territory. |

---

## Cross-Channel Coupling

Heat channels are not independent -- high Heat in one channel can push other channels upward. This creates feedback loops and cascade risks.

### Coupling Rules

| Condition | Target Effect | Rationale |
|---|---|---|
| **Physical > 0.5** | Social +0.1 (one-time bump when threshold crossed) | Visible damage causes witnesses to panic and talk |
| **Social > 0.6** | Institutional +0.15 (one-time bump when threshold crossed) | Public outcry forces authorities to respond |
| **Institutional > 0.7** | Physical +0.05 (one-time bump when threshold crossed) | Heavy authority response (vehicles, equipment, forced entries) causes collateral damage |
| **Ecological > 0.5** | Social +0.2 (one-time bump when threshold crossed) | Visible reality anomalies cause widespread panic |
| **Ecological > 0.8** | Physical +0.1 (one-time bump when threshold crossed) | Reality distortion causes actual structural damage |
| **Any channel > 0.9** | All channels +0.05 (one-time bump when threshold crossed) | Cascade effect -- crisis in any domain destabilizes everything |

### Coupling Diagram

```
    PHYSICAL ---------> SOCIAL
    (> 0.5)    +0.1    (> 0.6)
       ^                  |
       |                  | +0.15
  +0.05|                  v
       |             INSTITUTIONAL
  ECOLOGICAL  +0.2       (> 0.7)
    (> 0.5) -------> SOCIAL
    (> 0.8) -------> PHYSICAL
               +0.1

  ANY > 0.9 ------> ALL CHANNELS +0.05 (cascade)
```

### Coupling Execution Rules

1. **One-time trigger:** Each coupling rule fires only once per threshold crossing. If Physical exceeds 0.5, Social gets +0.1 once. If Physical drops below 0.5 and rises above it again, the coupling fires again.
2. **Evaluation order:** Couplings are evaluated in the order listed above. A coupling that raises a channel may immediately trigger another coupling in the same evaluation pass.
3. **Cascade cap:** The cascade rule (any > 0.9 raises all by +0.05) can only fire once per evaluation pass to prevent infinite loops.
4. **Player notification:** When a coupling fires, the player receives a HUD notification: "Cascade: [source channel] is driving [target channel] up." This teaches the player about system interactions.

---

## Heat Thresholds for Times Square

The combined Heat state of all four channels determines the overall world state of Times Square. The following table defines composite threshold levels.

### Composite Threshold Table

| Level | Physical | Social | Institutional | Ecological | World State Description |
|---|---|---|---|---|---|
| **Normal** | 0.0 -- 0.2 | 0.0 -- 0.2 | 0.0 -- 0.2 | 0.0 -- 0.1 | Business as usual. Times Square operates normally. Tourists, commuters, performers, vendors -- all at standard density and behavior. Anomalies are invisible to the public. Player operates with maximum freedom. |
| **Elevated** | 0.2 -- 0.4 | 0.2 -- 0.4 | 0.2 -- 0.4 | 0.1 -- 0.3 | Increased patrols, minor news coverage. Something is "off" but life continues. Subtle changes: more police presence, a few news vans, social media chatter, occasional strange looks from locals. Player must be more careful. |
| **High** | 0.4 -- 0.7 | 0.4 -- 0.7 | 0.4 -- 0.6 | 0.3 -- 0.5 | Road closures, investigation active, crowd changes. Times Square is visibly different. Barriers, cordons, reduced foot traffic in some areas, increased in others (rubberneckers). Media presence. Detective activity. Player's operating environment is constrained. |
| **Critical** | 0.7 -- 0.9 | 0.7 -- 0.9 | 0.6 -- 0.8 | 0.5 -- 0.7 | Area lockdown, heavy response, media frenzy. Times Square is in crisis mode. Access restricted, heavy police/military presence, 24-hour news coverage, political statements. Civilian behavior is extreme (evacuation or protest). Player must navigate a hostile environment. |
| **Crisis** | 0.9+ | 0.9+ | 0.8+ | 0.7+ | Full lockdown, military consideration, reality fracture risk. Times Square is unrecognizable. Empty streets or barricaded zones. Federal/military control. Spontaneous anomaly events. The game world has fundamentally changed. Recovery requires sustained player effort and faction cooperation. |

### Threshold Triggers (specific world events)

| Composite Level | Triggered Events |
|---|---|
| **Normal to Elevated** | NYPD dispatch increases patrol frequency by 25%. Local news runs "unusual activity" segment. Social media algorithms promote Times Square content. |
| **Elevated to High** | NYPD forms dedicated investigation unit. Road closures on 1-2 blocks. News vans establish semi-permanent positions. City Council emergency session mentioned in news. |
| **High to Critical** | Multi-agency task force activated. Federal liaison arrives. Times Square perimeter established (checkpoints). Mayor's office issues statement. National news coverage begins. |
| **Critical to Crisis** | Governor's emergency declaration. National Guard deployed to perimeter. All civilian access suspended. President briefed (off-screen). Strange's faction enters crisis protocol. All portals in the area become highly unstable. |

---

## Heat Event Chain Example

A step-by-step walkthrough of how a single anomaly event cascades through all four Heat channels.

### Scenario: Uncontained Anomaly at 44th Street

Starting conditions: all Heat channels at 0.0 (fresh game state).

| Step | Event | Physical | Social | Institutional | Ecological | Notes |
|---|---|---|---|---|---|---|
| **1** | Anomaly shimmer appears at 44th St (natural, uncontrolled) | 0.0 | 0.0 | 0.0 | **+0.2 = 0.2** | Ecological Heat is the first responder. Anomaly energy stresses local reality. |
| **2** | CCTV detects distortion. Sensor log event: `security.camera.observation` | 0.0 | 0.0 | **+0.05 = 0.05** | 0.2 | Digital evidence class entry created. Institutional system now has a data point. |
| **3** | Nearby pedestrians notice shimmer. Crowd begins to form (rubbernecking). | 0.0 | **+0.1 = 0.1** | 0.05 | 0.2 | Witness evidence class entries begin. Social media risk increases with crowd size. |
| **4** | NYPD dispatch sends patrol unit to investigate "visual disturbance" report. | 0.0 | 0.1 | **+0.05 = 0.1** | 0.2 | Authority presence. Officers observe and report. Institutional memory strengthened. |
| **5** | Player enters anomaly zone. Interaction causes energy burst (attempting to contain). | **+0.1 = 0.1** | 0.1 | 0.1 | **+0.1 = 0.3** | Physical energy release. Ecological stress from player's containment energy. |
| **6** | Crowd reacts to energy burst. Running, shouting, noise spike. | 0.1 | **+0.15 = 0.25** | 0.1 | 0.3 | Crowd panic propagation. Multiple witness reports. Social media recording likely. |
| **7** | NYPD officers on scene establish cordon. Call for backup. | 0.1 | 0.25 | **+0.1 = 0.2** | 0.3 | Institutional response escalates. More officers, more reports, more data. |
| **8** | Anomaly intensifies into portal opening. Energy flash. | **+0.15 = 0.25** | **+0.2 = 0.45** | 0.2 | **+0.2 = 0.5** | Major event. Physical energy, crowd panic, ecological stress all spike. |
| | **TOTALS after chain:** | **0.25** | **0.45** | **0.20** | **0.50** | |

### Post-Chain Analysis

```
Channel Status After Event Chain:
  Physical:      0.25  [LOW]       ████████░░░░░░░░░░░░
  Social:        0.45  [MEDIUM]    █████████████░░░░░░░
  Institutional: 0.20  [ELEVATED]  ██████░░░░░░░░░░░░░░
  Ecological:    0.50  [HIGH]      ██████████████░░░░░░

Composite Level: HIGH (Social and Ecological are the drivers)

Coupling Check:
  - Ecological > 0.5 → Social +0.2 → Social becomes 0.65 [HIGH]
  - Social > 0.6 → Institutional +0.15 → Institutional becomes 0.35 [ELEVATED]
  - No other couplings triggered.

FINAL Heat State (post-coupling):
  Physical:      0.25  [LOW]
  Social:        0.65  [HIGH]
  Institutional: 0.35  [ELEVATED]
  Ecological:    0.50  [HIGH]

World State: HIGH — road closures, investigation active, crowd changes.
```

### Recovery Timeline (no further events)

```
Time to decay back to Normal (all channels < 0.2):

Physical (0.25):      ~2.5 min   (0.25 / 0.02 per min)
Social (0.65):        ~45 min    (0.45 / 0.01 per min, from 0.65 to 0.2)
Institutional (0.35): ~30 min    (0.15 / 0.005 per min, from 0.35 to 0.2)
Ecological (0.50):    ~100 min   (0.40 / 0.003 per min, from 0.50 to 0.1)

Ecological is the bottleneck. Even if the player does nothing else,
it takes nearly 2 hours of sim-time for the neighborhood to fully recover.
Active containment (Strange intervention, cleanup) can accelerate this.
```

---

## Heat Coupling to Portals

Heat levels directly affect portal behavior. This creates a feedback loop: portals generate Heat, and Heat destabilizes portals.

### Portal Modifiers by Heat Level

| Condition | Portal Effect | Mechanism |
|---|---|---|
| **Any Heat channel > 0.5** | Portal stability decay rate x1.5 | Environmental stress makes dimensional boundaries less stable. A portal that normally decays at -0.01/min now decays at -0.015/min. |
| **Ecological Heat > 0.7** | Entropy_bleed radius x2.0 | Compromised reality offers less resistance to bleed. A portal with 10m bleed now affects 20m. All effects within the bleed zone are doubled. |
| **Institutional Heat > 0.6** | Authority faction deploys containment teams near known portal zones | NYPD/federal teams establish perimeter around portal hotspots. Player must bypass or engage authority to access portals. |
| **Physical Heat > 0.8** | Spontaneous micro-portals may spawn | Reality is so stressed that small, uncontrolled portals open without any ritual or device. These generate Ecological Heat (feedback loop), are not traversable, and may produce dangerous bleed effects. Spawn rate: 1 per 10 minutes while Physical > 0.8. |

### Feedback Loop Diagram

```
Portal Activity
      |
      v
Heat Generation (all channels)
      |
      v
Heat Rises Above Thresholds
      |
      +---> Stability decay x1.5 (any > 0.5)
      |         |
      |         v
      |     Portals become harder to maintain
      |     (more stabilization resources needed)
      |
      +---> Bleed radius x2.0 (eco > 0.7)
      |         |
      |         v
      |     Larger bleed = more evidence = more Heat
      |
      +---> Authority containment teams (inst > 0.6)
      |         |
      |         v
      |     Portal access becomes harder
      |     (must evade authority to use portals)
      |
      +---> Spontaneous micro-portals (phys > 0.8)
              |
              v
          More Ecological Heat → more instability
          (RUNAWAY LOOP if not contained)
```

---

## Evidence Economy

Evidence is the raw material that feeds the Heat system. Every player action, NPC observation, and environmental effect generates evidence entries in a persistent ledger.

### Evidence Classes

| Class | Source | Persistence | Detection Method | Heat Channel Fed |
|---|---|---|---|---|
| **Physical** | Debris, damage marks, scorch marks, residue patches, structural deformation, exotic material traces, containment device remnants | Persists until cleaned or repaired. Residue patches: 12-24h. Structural damage: permanent until repaired. | Visual inspection, forensic analysis, residue scanners. Physical evidence is tangible -- it exists in the world as objects/textures. | Physical (primary), Institutional (secondary -- if collected by authorities) |
| **Digital** | CCTV footage, IoT sensor logs, device data (phone recordings by NPCs), seismic sensor data, EM anomaly logs, satellite imagery (at crisis level) | Persistent in institutional databases. CCTV: retained for 30 days. Sensor logs: indefinite. NPC phone recordings: until device wiped or battery dies. | Institutional analysis (automated sensor alerts, manual footage review). Digital evidence is data -- it exists in databases and devices. | Institutional (primary), Social (secondary -- if footage goes public/viral) |
| **Witness** | NPC testimony (verbal reports to authorities or other NPCs), NPC memories (may surface later), crowd behavior records (aggregate data from crowd density sensors), social media posts by NPC witnesses | Subject to NPC memory decay model. Minor events: 2-4h. Significant: 24-72h. Traumatic: permanent. Social media posts: indefinite (but can be buried by algorithms). | Interviews (authority NPCs actively interview witnesses near anomaly sites), social media monitoring, community forum scanning. | Social (primary), Institutional (secondary -- if formal statements taken) |

### Evidence Lifecycle

```
Event Occurs
    |
    v
Evidence Generated (class determined by event type)
    |
    +---> Physical Evidence
    |         |
    |         v
    |     Exists in world as object/texture
    |     Player can: clean, destroy, conceal
    |     Authority can: collect, analyze, catalog
    |     Decays: slowly (residue 12-24h) or never (structural)
    |
    +---> Digital Evidence
    |         |
    |         v
    |     Exists in databases/devices
    |     Player can: hack/delete CCTV footage, jam sensors,
    |                 suppress NPC phone recordings (EMP)
    |     Authority can: review, correlate, share across agencies
    |     Decays: never (institutional databases persist)
    |
    +---> Witness Evidence
              |
              v
          Exists in NPC memory
          Player can: intimidate (suppress testimony),
                      bribe (redirect testimony),
                      befriend (gain favorable account)
          Authority can: interview, take statements
          Decays: per NPC memory model (hours to permanent)
```

### Evidence Suppression Methods

| Method | Target | Effectiveness | Cost | Risk |
|---|---|---|---|---|
| **Cleanup** (physical) | Residue patches, debris, scorch marks | 80% reduction in physical evidence signature | Time (5-15 min per site), cleaning supplies | Low (if done before authority arrives). High if done after (tampering with evidence, Institutional Heat +0.1) |
| **CCTV hack** (digital) | Security camera footage | 100% deletion of specific footage segments | CCTV access credentials (obtained from faction or hacking), proximity to CCTV control node | Medium. If hack is detected, Institutional Heat +0.1, player flagged in security system. |
| **Sensor jam** (digital) | IoT sensor network in a radius | Suppresses all sensor data for 5-minute window within 50m radius | Jammer device (craftable, consumes power cell) | Medium. Sensor gap itself is logged (absence of data is evidence). Authority may investigate the gap. |
| **Witness management** (witness) | Individual NPC testimony | Varies: intimidation (70% suppression, high risk), bribe (60% suppression, medium risk), befriend (50% suppression, low risk) | Intimidation: threat of force. Bribe: currency. Befriend: time + social skill. | Intimidation: if NPC reports, Social Heat +0.1, Institutional Heat +0.1. Bribe: if NPC is an informant, trap. Befriend: time-consuming, may not work. |
| **Misinformation** (social/digital) | Public narrative, belief meter | Redirects attention, dilutes signal with noise | Hack skill + proximity to kiosk/social media node | Medium-High. If detected, Institutional Heat +0.1, trust damage with authority faction. |

---

## Belief Meter

The Belief Meter tracks how much a neighborhood's population accepts that "Marvel-stuff is real" -- that portals, anomalies, and multiverse events are genuine phenomena, not fiction, hallucinations, or hoaxes.

### Belief Meter Specification

| Parameter | Value |
|---|---|
| **Scale** | 0.0 (complete denial) to 1.0 (full acceptance) |
| **Scope** | Per neighborhood (Times Square has its own meter; adjacent neighborhoods track independently but are influenced) |
| **Starting Value** | 0.05 (almost total denial -- Marvel is fiction, anomalies are "gas leaks" or "performance art") |
| **Update Frequency** | Per evidence event + per rumor cycle (hourly check) |

### Belief Influences

| Influence | Direction | Magnitude | Mechanism |
|---|---|---|---|
| Evidence accumulation | + (increases belief) | +0.01 per physical evidence entry visible to public; +0.02 per viral social media post; +0.05 per mainstream news segment | More evidence = harder to deny |
| Authority messaging | + or - (depends on message) | Authority "everything is normal" messaging: -0.02 per broadcast. Authority "we are investigating anomalies": +0.03 per statement. | Authority credibility shapes public interpretation |
| Misinformation campaigns | + or - (player/faction controlled) | +/- 0.03 per successful misinformation action | Player can push belief up or down for strategic purposes |
| Time without events | - (decreases belief) | -0.005 per day of sim-time without any evidence event | People forget and rationalize |
| Traumatic events | + (sharp increase) | +0.1 per mass-witness anomaly event (portal opening in public, reality distortion affecting crowd) | Traumatic events are hard to deny or forget |

### Belief Effects on Gameplay

| Belief Range | Citizen Behavior | Police Posture | Crime Opportunities | Anomaly Panic Threshold |
|---|---|---|---|---|
| **0.0 -- 0.1** (Denial) | NPCs dismiss anomalies ("must be a movie shoot," "gas leak"). Witnesses are unreliable (low social evidence quality). Public is complacent. | Standard policing. Anomaly reports treated as noise. Officers skeptical. | Minimal portal-related crime (criminals don't believe either). Standard black market. | Very low -- any anomaly causes maximum surprise/panic (no mental preparation). |
| **0.1 -- 0.3** (Skeptical) | NPCs are curious but doubtful. "Did you see that weird thing on Twitter?" Social media engagement increasing. Some people actively seeking anomaly sightings. | Police beginning to take reports seriously. "Anomalous events" category created in dispatch. Some officers briefed. | Early portal-related black market. Criminals see opportunity. Fake "portal artifacts" appear (scam economy). | Low -- anomalies still cause significant panic, but some NPCs react with curiosity instead of fear. |
| **0.3 -- 0.5** (Uncertain) | NPCs divided. Some believe, some deny. Community meetings. Arguments in public. Some people prepare (emergency kits, "anomaly tourism"). | Police have dedicated anomaly resources. Specialized training for patrol officers. Institutional memory building rapidly. | Established portal-black market. Real exotic goods trading. Criminal factions actively pursuing portal access. | Medium -- mixed responses. Believers react with purpose (approach or flee). Deniers still panic. |
| **0.5 -- 0.7** (Accepting) | Majority accepts anomalies as real. Social adaptation begins. New businesses (anomaly tours, "portal insurance"). Cultural shift. | Police have full anomaly division. Federal coordination standard. Surveillance network optimized for portal detection. | Mature portal economy. Exotic goods have market prices. Criminal factions are multiverse-savvy. | Medium-High -- calmer initial response (people expect anomalies) but faster organized response (less shock delay). |
| **0.7 -- 1.0** (Integrated) | Anomalies are part of daily life. Public discourse is about policy, not belief. "How do we regulate portals?" not "Are portals real?" | Police are portal-trained. Federal portal authority established. Legal framework emerging. | Fully integrated underground economy. Portal smuggling is organized crime. State actors involved. | High -- minimal panic (normalized) but maximum institutional response speed (prepared systems). |

---

## Rumor System

Rumors are lightweight social evidence entries that spread through the NPC population and influence the Belief Meter. They are less formal than evidence entries but more pervasive.

### Rumor Types

| # | Rumor Type | Trigger | Spread Rate | Lifespan | Belief Impact | Heat Impact |
|---|---|---|---|---|---|---|
| **1** | "Strange lights near 44th" | Any anomaly event (shimmer, energy flash) near 44th St. Low evidence threshold. | Slow (word of mouth, 10 NPCs/hour) | 24h sim-time (fades without reinforcement) | +0.005 per spread cycle | Social: +0.01 per cycle (negligible individually) |
| **2** | "Someone broke into [building] using weird tech" | Player uses exotic technology in view of witnesses, especially during B&E operations. Medium evidence threshold. | Moderate (word of mouth + social media, 30 NPCs/hour) | 48h sim-time | +0.01 per spread cycle | Social: +0.02, Institutional: +0.01 per cycle |
| **3** | "Military vehicles spotted near Times Square" | Institutional Heat > 0.5 (authority response becomes visible). High institutional signal. | Fast (social media + news, 100 NPCs/hour) | 72h sim-time (self-reinforcing if military presence continues) | +0.02 per spread cycle | Social: +0.03, Institutional: +0.01 per cycle |
| **4** | "Video of portal on social media" | NPC captures video evidence of portal formation or traversal. Requires portal event + NPC with phone in recording range. | Very fast (viral social media, 500+ NPCs/hour) | Indefinite (digital persistence, cannot be fully suppressed) | +0.1 per viral event (one-time Belief spike) | Social: +0.1 immediately, Institutional: +0.05 immediately |
| **5** | "Government coverup -- something big happened" | Authority faction performs suppression action (confiscate evidence, issue gag order, force takedown of social media content). Meta-rumor: spawns FROM authority actions, not anomaly events. | Moderate-Fast (conspiracy networks, social media, 50 NPCs/hour) | 96h sim-time (conspiracy theories are persistent) | +0.03 per spread cycle (coverup accusations INCREASE belief) | Social: +0.02, Institutional: -0.01 (authority loses some credibility) |

### Rumor Lifecycle

```
Triggering Event
    |
    v
Rumor Spawns (type determined by event)
    |
    v
Spread Phase (rate depends on type)
    |
    +---> Each spread cycle: Belief +X, Heat +Y
    |
    +---> Reinforcement: if new evidence matches rumor,
    |     spread rate doubles and lifespan resets.
    |
    +---> Contradiction: if authority issues denial AND
    |     no new supporting evidence, spread rate halves.
    |
    v
Decay Phase (lifespan expires without reinforcement)
    |
    v
Rumor Fades (removed from active rumor pool)
```

### Rumor Interaction Rules

1. **Stacking:** Multiple rumors of the same type do not stack. If a second "strange lights" rumor spawns while the first is active, the first is refreshed (lifespan reset, spread rate maintained at the higher value).
2. **Escalation:** If 3+ different rumor types are active simultaneously, a meta-rumor spawns: "Something big is happening in Times Square." This meta-rumor has fast spread, long lifespan, and high Belief impact (+0.05 per cycle).
3. **Suppression:** Player or faction can attempt to suppress a rumor through misinformation or authority messaging. Suppression reduces spread rate by 50% but does not eliminate the rumor. Aggressive suppression (confiscation, gag orders) triggers Rumor Type 5 (coverup).

---

## Misinformation Actions

The player (and certain factions) can actively manipulate information flow to manage Heat and Belief.

### Kiosk Spoofing

**Mechanism:** Public information kiosks throughout Times Square (touchscreens, digital displays, wayfinding stations) can be hacked to display custom messages. The event bus address is `public_info.kiosk.alert`.

| Parameter | Specification |
|---|---|
| **Cost** | Hack skill check (moderate difficulty) + physical proximity (within 3m of kiosk) + 30-second interaction |
| **Effect** | Kiosk displays player-authored alert for 10 minutes (or until manually reset by city maintenance). Alert is seen by all NPCs who interact with the kiosk during that window. |
| **Belief Impact** | Customizable: player chooses the message direction. "Anomaly is real" messaging: Belief +0.03 in neighborhood. "Anomaly is a hoax/marketing stunt" messaging: Belief -0.03. |
| **Social Heat Impact** | +0.02 (any kiosk alert draws attention, regardless of content) |
| **Risk** | If hack is detected (30% base chance, reduced by hack skill): Institutional Heat +0.1, kiosk is flagged for security review (future hack attempts at that kiosk are harder), player may be identified on CCTV near the kiosk. |

### Social Media Manipulation

**Mechanism:** Player can use hacked accounts or bot networks (obtained from Criminal faction at cost) to amplify or suppress social media narratives.

| Parameter | Specification |
|---|---|
| **Cost** | Bot network access (purchased from Criminal faction, 1 use per purchase) + target narrative identified |
| **Effect** | Amplify: selected rumor spread rate x3 for 12h. Suppress: selected rumor spread rate x0.3 for 12h. |
| **Belief Impact** | Amplify: rumor's Belief impact x2 during amplification period. Suppress: rumor's Belief impact x0.5 during suppression period. |
| **Risk** | Platform detection: 20% chance social media platform flags bot activity, reducing effectiveness to zero and generating Institutional Heat +0.05 (platform reports to authorities). Criminal faction may leverage the favor (future request). |

### Authority Coordination

**Mechanism:** If the player has sufficient NYPD/authority faction reputation, they can request official messaging actions.

| Parameter | Specification |
|---|---|
| **Cost** | Authority faction reputation > 0.3. Request costs reputation (-0.05 per request, authority doesn't like being used). One request per 24h sim-time. |
| **Effect** | Authority issues official statement to media. Content options: "No cause for concern" (Belief -0.05, Social Heat -0.1), "Investigation underway" (Belief +0.03, Institutional Heat +0.05 but Social Heat -0.05), "Public advisory: avoid area" (Belief +0.05, Social Heat +0.1, Physical access restrictions in area). |
| **Risk** | Overuse erodes authority credibility. After 3 "no cause for concern" statements, public skepticism increases (Belief decay from authority messaging halves). If authority messaging contradicts visible evidence, Rumor Type 5 spawns. |

---

## Integration Notes

### System Dependencies

| System | Reads From Heat/Evidence | Writes To Heat/Evidence |
|---|---|---|
| **Portal State Machine** | Heat thresholds modify stability decay and bleed radius | Portal state transitions generate evidence and Heat events |
| **Translation Gate** | N/A | Imported items generate ongoing evidence and Heat |
| **Operations Library** | Current Heat levels drive dynamic twists | Operation aftermath defines Heat impact |
| **Faction System** | Heat levels determine faction response posture | Faction actions may raise or lower Heat |
| **NPC AI Director** | Heat channels modify NPC behavior (awareness, stress, patrol routes) | NPC actions generate evidence (witness reports, authority reports) |
| **Universe Profile** | N/A (Heat is EARTH-1218 specific) | N/A |
| **Belief Meter** | Evidence accumulation drives Belief | Belief level modifies NPC panic thresholds and faction postures |

### Event Bus Integration

Heat changes fire the following event:

```json
{
  "event_type": "heat.channel_update",
  "channel": "physical",
  "previous_value": 0.15,
  "new_value": 0.25,
  "delta": 0.10,
  "source": "portal.energy_burst",
  "source_location": {"x": 234.5, "y": 0.0, "z": -112.3},
  "threshold_crossed": null,
  "coupling_triggered": false,
  "timestamp": "sim_time_iso8601"
}
```

Evidence entries fire:

```json
{
  "event_type": "evidence.entry_created",
  "evidence_id": "unique_evidence_id",
  "evidence_class": "digital",
  "evidence_subtype": "cctv_footage",
  "location": {"x": 234.5, "y": 0.0, "z": -112.3},
  "source_event": "portal.state_change",
  "severity": "medium",
  "heat_impact": {
    "institutional": 0.05,
    "social": 0.02
  },
  "persistence": "30_days",
  "suppressible": true,
  "suppression_method": "cctv_hack",
  "timestamp": "sim_time_iso8601"
}
```

Belief Meter changes fire:

```json
{
  "event_type": "belief.meter_update",
  "neighborhood": "times_square",
  "previous_value": 0.05,
  "new_value": 0.08,
  "delta": 0.03,
  "source": "rumor.spread_cycle",
  "rumor_type": "strange_lights",
  "timestamp": "sim_time_iso8601"
}
```

### Cross-Reference Documents

| Document | Relationship |
|---|---|
| `universe-profile-template-v0.md` | EARTH-1218 persistence contract defines evidence generation modes |
| `portal-state-machine-v0.md` | Portal events are the primary Heat source; Heat modifies portal behavior |
| `translation-gate-rules-v0.md` | Imported items generate ongoing Heat and evidence |
| `operations-library-v0.md` | Operations define Heat impact in their aftermath sections |
| `faction-response-table-v0.md` | Heat thresholds drive faction response postures |

---

*End of Reality Heat + Evidence Economy Spec v0*
