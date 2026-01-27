# Operations Library v0

> **Twin Earth NYC** -- Part 11: Multiverse Gameplay
> **Document:** Operations Library (5 Operations)
> **Version:** 0.1.0
> **Status:** Draft
> **Last Updated:** 2026-01-27

---

## Table of Contents

1. [Overview](#overview)
2. [Operation Template](#operation-template)
3. [Operation 1: The Snatch (Extract)](#operation-1-the-snatch)
4. [Operation 2: Containment Protocol (Contain)](#operation-2-containment-protocol)
5. [Operation 3: Dark Mirror (Infiltrate)](#operation-3-dark-mirror)
6. [Operation 4: Supply Line (Sabotage)](#operation-4-supply-line)
7. [Operation 5: The Witness (Recon)](#operation-5-the-witness)
8. [Operations Summary Matrix](#operations-summary-matrix)
9. [Integration Notes](#integration-notes)

---

## Overview

An **operation** is a structured multiverse gameplay session. Operations are the primary way the player engages with portals, alternate universes, and the faction ecosystem. Each operation follows a five-phase structure: Prep, Insertion, Objective, Complication, and Exfil -- bookended by an Aftermath phase that resolves consequences in the EARTH-1218 hub.

### Operation Types

| Type | Description | Portal Traversal | Typical Difficulty | Hub Impact |
|---|---|---|---|---|
| **Extract** | Retrieve an item or entity from another universe and bring it to 1218 | Required (outbound + return) | 2-4 stars | High (imported item generates evidence) |
| **Contain** | Seal an anomaly or portal to prevent escalation | Optional (may be hub-only) | 1-3 stars | Positive (reduces Heat) |
| **Infiltrate** | Enter another universe to gather intelligence without being detected | Required (outbound + return) | 3-5 stars | Medium (intel gained, minimal physical evidence) |
| **Sabotage** | Destroy or disable a target in another universe | Required (outbound + return) | 3-5 stars | High (evidence from destruction) |
| **Escort** | Guide an NPC or valuable entity through a portal | Required (outbound + return) | 2-4 stars | Variable (depends on escort target) |
| **Recon** | Observe and document portal activity or anomalies | Optional (may include brief pocket entry) | 1-3 stars | Low-Medium (evidence gathered, not generated) |

### Difficulty Scale

| Stars | Description | Prep Required | Complication Severity | Exfil Pressure |
|---|---|---|---|---|
| 1 star | Tutorial / routine | Minimal (basic gear) | Low (manageable) | Low (generous time) |
| 2 stars | Standard | Moderate (specific gear + basic intel) | Medium (requires adaptation) | Medium (time pressure) |
| 3 stars | Challenging | Significant (specialized gear + intel + ally support) | High (multiple complications) | High (tight countdown) |
| 4 stars | Demanding | Extensive (multi-mission prep chain + faction support) | Severe (cascading failures) | Critical (emergency extraction) |
| 5 stars | Extreme | Maximum (full faction mobilization + rare resources) | Catastrophic (survival-level) | Desperate (may not extract cleanly) |

---

## Operation Template

The canonical structure for defining operations. All five operations in this library follow this template.

```
================================================================
OPERATION: [Name]
================================================================
Type:       [Extract / Contain / Infiltrate / Sabotage / Escort / Recon]
Universe:   [Target universe ID and description]
Difficulty: [1-5 stars]
Unlock:     [Prerequisites to access this operation]

────────────────────────────────────────
PHASE 1: PREP (NYC / EARTH-1218)
────────────────────────────────────────
Intel Required:     [What the player needs to know before starting]
Gear Required:      [Equipment checklist]
Allies Required:    [Faction support needed]
Portal Requirements:[Stability, bandwidth, anchor specifications]
Prep Time:          [Estimated real-world time for preparation]

────────────────────────────────────────
PHASE 2: INSERTION
────────────────────────────────────────
Entry Method:       [Portal type, location, timing]
Transition Effects: [What the player experiences during crossing]
Landing Zone:       [Where the player arrives in the target universe]

────────────────────────────────────────
PHASE 3: OBJECTIVE
────────────────────────────────────────
Primary:            [Main goal -- required for mission success]
Secondary:          [Bonus objective -- optional, grants extra reward]
Failure Condition:  [What causes mission failure]

────────────────────────────────────────
PHASE 4: COMPLICATION
────────────────────────────────────────
Scripted Twist:     [Pre-authored narrative complication]
Dynamic Twist:      [Heat/stability-driven complication, varies per run]

────────────────────────────────────────
PHASE 5: EXFIL
────────────────────────────────────────
Exit Conditions:    [What must be true to leave]
Time Pressure:      [Portal stability countdown or other timer]
Extraction Cost:    [What it costs to leave -- resources, stability, etc.]

────────────────────────────────────────
AFTERMATH (NYC / EARTH-1218)
────────────────────────────────────────
Evidence Generated: [What appears in the evidence ledger]
Heat Impact:        [Changes to Heat channels]
Faction Response:   [Who notices, who cares, relationship changes]
Persistent Changes: [What is different in Times Square after]
Rewards:            [What the player gains]
```

---

## Operation 1: The Snatch

```
================================================================
OPERATION: THE SNATCH
================================================================
Type:       Extract
Universe:   Earth-616 Pocket (Abandoned Sanctum Wing)
Difficulty: ★★☆☆☆ (2 stars)
Unlock:     Complete tutorial (Operation 2: Containment Protocol)
            + Strange faction reputation > 0.2
            + Tech Rig crafted
```

### Phase 1: Prep (NYC / EARTH-1218)

| Requirement | Details |
|---|---|
| **Intel Required** | Strange's contact briefs the player on a destabilizing pocket universe fragment -- a wing of a Sanctum Sanctorum from Earth-616 that is bleeding into 1218 near 44th Street. Inside: a mystical artifact (the "Vaulted Eye," a scrying focus) that is accelerating pocket decay. Removing it will stabilize the pocket remnant. Intel is delivered via dead-drop at a pre-arranged coffee shop. |
| **Gear Required** | Tech Rig (for portal stabilization), Containment Pouch (for artifact transport -- reduces evidence signature by 60%), Scanner (for artifact location within pocket), Basic urban clothing (no conspicuous gear for the 44th St approach) |
| **Allies Required** | Strange's faction provides: pocket location coordinates, artifact signature data, and a one-time stabilization boost (+0.2 stability on portal entry). No in-field ally -- player operates solo. |
| **Portal Requirements** | Stability > 0.5 (achievable with Tech Rig +0.3 + Strange boost +0.2), Bandwidth > 10 kg/s (standard -- player + artifact < 110 kg), Anchor required (player sets Tech Rig as anchor at 44th St alley) |
| **Prep Time** | ~15 minutes (gear check, travel to 44th St, alley reconnaissance, Tech Rig setup) |

### Phase 2: Insertion

| Element | Details |
|---|---|
| **Entry Method** | Player-opened portal via Tech Rig at 44th Street alley (between buildings, partial concealment from main street). Time: recommended after 11 PM sim-time (reduced foot traffic, lower Social Heat risk). Portal class: Standard (10 kg/s bandwidth). |
| **Transition Effects** | 30-second formation period. Visual: alley wall shimmers, then tears open to reveal a darkened stone corridor. Audio: grinding stone sound, then silence. Player experiences mild nausea and 3-second disorientation on crossing (standard living being adjustment). Colors shift -- 1218's urban palette gives way to the pocket's muted stone and amber mystical light. |
| **Landing Zone** | Interior of an abandoned Sanctum wing. Stone corridors, dust, broken display cases. Ambient mystical light (amber glow from wall sconces that still function). Gravity is standard (pocket mirrors 616 physics closely). Air is stale but breathable. No immediate hostiles. |

### Phase 3: Objective

| Element | Details |
|---|---|
| **Primary Objective** | Locate and extract the Vaulted Eye artifact. The artifact is in a sealed display room at the end of the corridor network (3 rooms deep). Scanner guides the player to the artifact's signature. The display case is locked (lockpick check, moderate difficulty) or breakable (generates noise, alerts guardian -- see Complication). The artifact must be placed in the Containment Pouch immediately on extraction. |
| **Secondary Objective** | Photograph 3 intact mystical texts visible in the corridor (Information class -- no decay, no evidence, valuable intel for Strange's faction, reputation +0.1). |
| **Failure Condition** | Player is killed by guardian entity OR portal collapses before player exits OR artifact is destroyed during extraction (drops below 10% integrity from mishandling). |

### Phase 4: Complication

| Element | Details |
|---|---|
| **Scripted Twist** | Upon extracting the Vaulted Eye from its case, a guardian entity awakens -- a mystical construct bound to protect the artifact. The guardian is a humanoid figure made of animated stone debris (moderate combat threat, vulnerable to kinetic attacks, resistant to tech). Simultaneously, removing the artifact accelerates the pocket's collapse -- structural cracking begins, dust falls, rooms begin to shift. The player now has a 3-minute countdown before pocket integrity fails (portal forced to COLLAPSING). |
| **Dynamic Twist** | If the player's Ecological Heat in 1218 is > 0.3 at mission start, the pocket is already more unstable: countdown is reduced to 2 minutes. If Institutional Heat > 0.4, an NYPD patrol passes the 44th St alley during the operation -- the player must deal with the portal being partially visible from the street (Social Heat +0.1 risk on exit). |

### Phase 5: Exfil

| Element | Details |
|---|---|
| **Exit Conditions** | Player must return to the portal entry point (3 rooms back from artifact location) while the portal is still in STABLE or UNSTABLE state (traversable). Guardian does not follow through the portal (bound to pocket). |
| **Time Pressure** | 3-minute countdown from artifact extraction to pocket collapse. Portal stability decays at -0.1/min during countdown (accelerated by pocket instability). If stability reaches < 0.1, portal enters COLLAPSING -- player is trapped (mission failure, respawn in 1218 with injuries and no artifact). |
| **Extraction Cost** | Stability -0.2 on exit (portal stress from pocket collapse shockwave). If player exits in the last 30 seconds, additional -0.1 stability (cutting it close). Portal enters UNSTABLE or COLLAPSING immediately after player exits (cannot be reused). |

### Aftermath (NYC / EARTH-1218)

| Element | Details |
|---|---|
| **Evidence Generated** | Physical: scorch marks on alley wall at portal site, faint residue patch. Digital: CCTV camera on 44th St captured brief energy flash during portal opening and closing (footage available to institutional faction). Witness: if any NPCs were in the alley (low probability at recommended time), they report "strange lights." |
| **Heat Impact** | Physical: +0.05 (minor alley damage from portal energy). Social: +0.05 (if late-night witnesses present, +0.1 if NYPD dynamic twist triggers). Institutional: +0.05 (CCTV footage logged in sensor network). Ecological: +0.1 (portal residue + artifact presence in 1218). **Net Heat: +0.15 to +0.35 depending on execution quality.** |
| **Faction Response** | Strange's Network: notices immediately (they commissioned the operation). If secondary objective completed, reputation +0.1 additional. They request the artifact for analysis (player can comply for reputation or keep it for personal use). NYPD: if dynamic twist triggered, increased patrol of 44th St for 48h sim-time. Criminal Syndicate: if they learn of the artifact (through informants, 30% chance), they approach the player to buy it (high price, reputation opportunity). |
| **Persistent Changes** | 44th St alley: residue patch visible for 24h (faint shimmer on wall), scorch marks persist until city maintenance. Player inventory: Vaulted Eye artifact (compatibility 0.4, decaying, containment required). Pocket universe: sealed and inaccessible (one-time operation). |
| **Rewards** | Vaulted Eye artifact (mystical scrying focus -- allows player to detect anomalies at 2x range while held, decays with 12h half-life, maintainable with portal residue). Strange faction reputation +0.15 (or +0.25 with secondary objective). Operation completion XP. Unlocks Operation 3: Dark Mirror. |

---

## Operation 2: Containment Protocol

```
================================================================
OPERATION: CONTAINMENT PROTOCOL
================================================================
Type:       Contain
Universe:   Earth-1218 (Hub) — Anomaly containment, no portal traversal
Difficulty: ★☆☆☆☆ (1 star — Tutorial)
Unlock:     Automatic — first operation in the game
            (triggered by Strange's contact approaching player)
```

### Phase 1: Prep (NYC / EARTH-1218)

| Requirement | Details |
|---|---|
| **Intel Required** | Strange's contact (a woman named Maya, operates a small bookshop on 43rd) intercepts the player and explains: an anomaly is forming at 44th Street. It hasn't become a full portal yet, but it's emitting detectable energy. If left unchecked, it will reach FORMING state within 20 minutes. Maya provides a containment device (prototype) and basic instructions. This is the player's introduction to the multiverse. |
| **Gear Required** | Containment Device (provided by Maya -- single-use, seals anomalies below FORMING state). Scanner (provided by Maya -- detects anomaly location and intensity). Both items are tutorial gear -- no crafting or purchase required. |
| **Allies Required** | Maya provides remote guidance via earpiece (tutorial voice). No combat ally needed (this operation has no hostile NPCs). |
| **Portal Requirements** | N/A -- this is a containment operation. The goal is to PREVENT a portal from forming. No traversal occurs. |
| **Prep Time** | ~5 minutes (dialogue with Maya, receive gear, walk to 44th St). |

### Phase 2: Insertion

| Element | Details |
|---|---|
| **Entry Method** | No portal traversal. Player walks from Maya's bookshop (43rd St) to the anomaly site (44th St, near the pedestrian plaza). The approach teaches the player to navigate the Times Square environment and use the scanner. |
| **Transition Effects** | N/A (hub operation). As the player approaches the anomaly site, the scanner begins pulsing. Environmental cues appear: slight visual shimmer in the air, pigeons avoiding the area, a hot-dog vendor commenting that his cart's electronics are glitching. |
| **Landing Zone** | The anomaly is located at a specific point on 44th Street -- a section of sidewalk near a building facade. It manifests as a faint visual distortion (like heat haze) approximately 2m in diameter, hovering 1m off the ground. Scanner confirms: anomaly_intensity 0.5 and rising. |

### Phase 3: Objective

| Element | Details |
|---|---|
| **Primary Objective** | Seal the anomaly before it reaches FORMING state (anomaly_intensity > 0.7). The player must: (1) approach within 3m of the anomaly, (2) activate the scanner to lock onto the anomaly's signature, (3) deploy the containment device (5-second channeling, interruptible). On success, the anomaly dissipates -- energy is absorbed by the containment device, which becomes spent. |
| **Secondary Objective** | Complete the seal without any NPC witnessing the containment device activation. This requires timing (wait for pedestrian gap) or positioning (use the player's body to block line-of-sight). Success: Social Heat +0.0 instead of +0.02. Maya commends the player's discretion. |
| **Failure Condition** | Anomaly reaches intensity 0.7 before containment (enters FORMING state -- tutorial pivots to observation, Strange intervenes remotely to seal it, player learns from failure). Containment device is interrupted 3 times (device overloads, tutorial pivots similarly). Note: failure is non-punitive in this tutorial -- the player learns regardless. |

### Phase 4: Complication

| Element | Details |
|---|---|
| **Scripted Twist** | Midway through the approach (anomaly at intensity 0.6), a crowd begins to form. A street performer nearby has drawn a cluster of tourists, and some of them notice the visual distortion. Phones come out. A few people approach for a closer look. The crowd density around the anomaly increases from sparse to moderate. The player must now navigate the crowd to reach the anomaly and deploy the device without causing a scene. If the player pushes through aggressively, Social Heat +0.05. If the player waits for a gap, anomaly intensity rises (time pressure). If a tourist photographs the anomaly, Social Heat +0.08 (social media post). |
| **Dynamic Twist** | If the player has been exploring Times Square for more than 30 minutes before this operation triggers (variable start time), an NYPD patrol is already in the area on routine assignment. The patrol notices the crowd gathering and moves to investigate. The player now has competing objectives: seal the anomaly AND avoid the officers seeing the containment device. If the officers reach the anomaly first, they cordon the area (Institutional Heat +0.05) and the player must talk their way past or find a different approach angle. Maya provides guidance: "Stay calm. They don't know what they're looking at." |

### Phase 5: Exfil

| Element | Details |
|---|---|
| **Exit Conditions** | N/A (hub operation). After sealing the anomaly, the player walks away. Maya contacts them via earpiece to debrief. If NYPD is present, the player should leave casually to avoid attention. |
| **Time Pressure** | Anomaly intensity rises at +0.01/second. From the player receiving the mission (intensity 0.5), they have approximately 20 seconds of real gameplay time before intensity 0.7 (FORMING threshold). This is generous for tutorial purposes but creates perceived urgency. |
| **Extraction Cost** | Containment Device is spent (single-use). Maya will provide replacement devices in the future (or the player can craft them after unlocking Tech Rig in Act 1). |

### Aftermath (NYC / EARTH-1218)

| Element | Details |
|---|---|
| **Evidence Generated** | Physical: small residue patch on the sidewalk where the anomaly was (faint discoloration, fades in 12h). Digital: if CCTV captured the anomaly shimmer (likely), sensor log entry created. If tourists photographed, social media posts exist (digital evidence class). Witness: crowd members may mention "weird shimmer" to friends -- low-grade witness evidence, decays in 24h. |
| **Heat Impact** | Physical: +0.0 (no physical damage from containment). Social: +0.02 base (crowd noticed something) or +0.0 if secondary objective achieved. Institutional: +0.02 (sensor log entry). Ecological: -0.05 (anomaly sealed, reducing ambient ecological stress). **Net Heat: -0.01 to +0.04 (net positive -- containment reduces Heat).** |
| **Faction Response** | Strange's Network: Maya is pleased. Player is formally inducted as an ally (faction reputation +0.15, unlocking future mission access). Maya explains the broader situation: portals are appearing, Strange is stretched thin, the player's help is needed. NYPD: if they were present, they file a "minor disturbance" report (routine, low priority). Citizens' Watch: a local notices the residue patch and posts about it on a community forum (low-grade belief meter nudge, +0.01). |
| **Persistent Changes** | 44th St sidewalk: faint residue mark (12h duration). Player: now allied with Strange's network. Tutorial complete -- all subsequent operations are available based on reputation and prerequisites. Player receives: earpiece (permanent communication with Maya), Scanner (permanent, upgradeable), Containment Device blueprint (can craft more). |
| **Rewards** | Strange faction reputation +0.15. Scanner (permanent equipment). Earpiece (permanent communication link). Containment Device blueprint. Tutorial completion (unlocks Operation 1: The Snatch and Operation 5: The Witness). Gameplay systems tutorial: player has learned anomaly detection, crowd navigation, evidence management, and basic containment. |

---

## Operation 3: Dark Mirror

```
================================================================
OPERATION: DARK MIRROR
================================================================
Type:       Infiltrate
Universe:   Earth-838 Pocket (Alternate Times Square Fragment)
Difficulty: ★★★☆☆ (3 stars)
Unlock:     Complete Operation 1: The Snatch
            + Strange faction reputation > 0.4
            + Obtain 838 credentials (side quest)
```

### Phase 1: Prep (NYC / EARTH-1218)

| Requirement | Details |
|---|---|
| **Intel Required** | Strange's network has detected an impending large-scale incursion -- something much bigger than the pocket anomalies seen so far. The source appears to be Earth-838, an alternate universe with a more technologically advanced and authoritarian version of NYC. A pocket fragment of 838's Times Square has stabilized near the 1218 portal zone. Strange needs intelligence: what is 838 preparing, and how soon? The player must infiltrate the pocket, access a data terminal, and extract incursion timeline data. |
| **Gear Required** | 838-compatible disguise (alternate-universe clothing with correct insignia -- obtained via side quest from Strange's contact who has cross-universe experience), Forged 838 ID badge (crafted using intel from Strange's network -- passes casual inspection, fails deep scan), Data extraction device (USB-equivalent, modified for 838 tech interface), Scanner (upgraded -- can detect 838 authority sensor sweeps), Tech Rig (for portal stabilization) |
| **Allies Required** | Strange performs portal stabilization ritual (+0.5 stability -- this is a Strange Ritual use, one of the limited 1-2 per act). Maya provides real-time guidance via earpiece (limited -- signal degrades across universes, intermittent contact). |
| **Portal Requirements** | Stability > 0.7 (Strange's ritual + Tech Rig achieves ~0.8), Bandwidth > 10 kg/s (standard -- player only, light gear), Anchor set by Strange (mystical mark, 24h duration -- covers the operation timeline) |
| **Prep Time** | ~25 minutes (disguise fitting, gear check, briefing from Strange, portal opening at designated location -- 45th St rooftop with line-of-sight concealment). |

### Phase 2: Insertion

| Element | Details |
|---|---|
| **Entry Method** | Strange-opened portal on a 45th Street rooftop (concealed from street level). Time: 2 AM sim-time (minimal 1218 foot traffic, 838 pocket operates on different time -- player arrives at 838's equivalent of mid-afternoon, shift change at the data center). Portal class: Standard, stabilized by Strange. |
| **Transition Effects** | Crossing is smoother than The Snatch (Strange's stabilization is superior). Visual: 1218 rooftop dissolves into a shimmering blue-white field, then resolves into 838's Times Square. Immediate sensory contrast: 838 is colder (blue-shifted lighting), cleaner (no litter, pristine surfaces), and quieter (orderly foot traffic, no honking). The player feels a 3-second disorientation plus a new sensation: being watched. 838 has pervasive surveillance -- the air itself feels monitored. |
| **Landing Zone** | An alley between two buildings in 838's Times Square fragment. The buildings are recognizable but wrong -- sleeker architecture, holographic signage in English (different fonts, corporate branding instead of entertainment), uniformed pedestrians visible on the main street. The data center is 2 blocks away (in 838 terms -- the pocket is limited, so "2 blocks" is the full extent of the traversable area). |

### Phase 3: Objective

| Element | Details |
|---|---|
| **Primary Objective** | Infiltrate the 838 data center (a building that in 1218 is a hotel, but in 838 is a surveillance/coordination facility). Access a data terminal on the 3rd floor. Extract incursion timeline data using the data extraction device (45-second download, player must remain at terminal). Return to the portal with the data. |
| **Secondary Objective** | Identify the 838 authority commander overseeing incursion preparations. This requires accessing a secure office on the 4th floor (additional infiltration risk, locked door, guard patrol). Success provides Strange with a named target for future diplomatic or defensive action (faction quest advancement, reputation +0.15). |
| **Failure Condition** | Player is captured by 838 authority (pursuit ends in capture -- player is detained and must be extracted by Strange's emergency protocol, losing all gathered data and generating maximum evidence in both universes). OR portal collapses before player returns (stranded in 838 -- Strange performs emergency extraction within 10 minutes, but the delay generates significant Heat). |

### Phase 4: Complication

| Element | Details |
|---|---|
| **Scripted Twist** | During the data download (45-second timer), 838 authority detects the player's foreign dimensional signature. The player's biology carries a trace of 1218 reality -- 838's advanced sensors pick this up. An alert is triggered: "Dimensional anomaly detected, Sector 7, Floor 3." The player has approximately 90 seconds before a response team reaches the terminal room. The download is at 60% when the alert sounds. The player must decide: (A) wait for full download (risky -- response team may arrive), (B) abort with partial data (60% -- enough for basic intel but not full timeline), or (C) attempt to spoof the sensor (Scanner can emit a counter-signal, 50% success rate -- if it works, buys 60 more seconds; if it fails, response is immediate). |
| **Dynamic Twist** | If the player's combined Heat in 1218 is > 0.5 at mission start, the 838 pocket is aware of increased dimensional activity from 1218. 838 authority is on heightened alert: patrol frequency is doubled, sensor sweep interval is halved. The player encounters checkpoints that don't exist at lower Heat levels. If Ecological Heat > 0.3, the portal's entropy_bleed is detectable from within 838 -- authority can triangulate the player's exit point. |

### Phase 5: Exfil

| Element | Details |
|---|---|
| **Exit Conditions** | Player must return to the portal entry point (alley, 2 blocks from data center) while the portal is STABLE. If 838 authority is in pursuit, the player must break line-of-sight before entering the alley (838 pursuit AI is aggressive but respects LOS breaks in the pocket's limited geometry). |
| **Time Pressure** | Portal stability decays at standard rate (-0.01/min). With Strange's stabilization, the portal starts at ~0.8 and will remain STABLE for approximately 40 minutes. The operation should take 15-25 minutes. If the scripted twist causes delays, stability may drop to marginal (0.5-0.6) by exfil time. If the dynamic twist is active and entropy_bleed is detected, 838 authority may attempt to interfere with the portal anchor (stability -0.1 if they reach it). |
| **Extraction Cost** | Stability -0.1 on exit (standard crossing stress). If pursued, additional -0.1 (hostile energy near portal). Portal is sealed cleanly by Strange after player exits (controlled seal -- minimal evidence). Strange's mystical anchor fades after seal. |

### Aftermath (NYC / EARTH-1218)

| Element | Details |
|---|---|
| **Evidence Generated** | Physical: minimal (rooftop portal site, faint residue, no street-level visibility). Digital: sensor logs from portal opening (rooftop, less CCTV coverage than street level). Witness: none (2 AM, rooftop, no bystanders). 838-side: significant (838 authority now has dimensional anomaly records, player's biological signature on file). |
| **Heat Impact** | Physical: +0.02 (rooftop residue only). Social: +0.0 (no witnesses). Institutional: +0.1 (838 is now aware of 1218 portal activity -- this is cross-universe institutional awareness that will factor into future 838 encounters). Ecological: +0.05 (portal residue on rooftop). **Net Heat: +0.17 (clean operation, institutional cost is the main expense).** |
| **Faction Response** | Strange's Network: primary beneficiary. Incursion timeline data is critical -- Strange can now prepare defenses. Reputation +0.2 (+0.35 if secondary objective completed). Strange begins planning countermeasures (unlocks Act 2 story content). NYPD: unaware (no street-level evidence). Criminal Syndicate: unaware unless they have rooftop informants (10% chance -- if so, they learn about 838 and begin probing for opportunities). Media: no coverage (nothing visible occurred). Citizens' Watch: if rooftop residue is discovered (unlikely but possible), a forum post appears speculating about "roof anomalies." |
| **Persistent Changes** | 45th St rooftop: residue patch (24h duration, low visibility). Player inventory: 838 incursion data (Information class -- no decay, no evidence, permanent intel asset). 838 pocket: sealed but 838 authority retains records -- future 838 encounters will reference this incursion (838 NPCs may recognize the player's signature). Story progression: Act 2 content unlocked (incursion preparation arc). |
| **Rewards** | Incursion timeline data (story progression). Strange faction reputation +0.2 (or +0.35). 838 authority intel (if secondary completed -- named commander, faction data). Operation completion XP. Unlocks Operation 4: Supply Line (after 2 additional side missions). |

---

## Operation 4: Supply Line

```
================================================================
OPERATION: SUPPLY LINE
================================================================
Type:       Sabotage
Universe:   Unknown Pocket (Criminal Faction Staging Area)
Difficulty: ★★★★☆ (4 stars)
Unlock:     Complete Operation 3: Dark Mirror
            + Complete 3 side missions (intel gathering chain)
            + Strange faction reputation > 0.5
            + Criminal faction reputation < 0.3 (hostile or neutral)
            + Demolition Gear crafted or acquired
```

### Phase 1: Prep (NYC / EARTH-1218)

| Requirement | Details |
|---|---|
| **Intel Required** | Through a chain of 3 prior intel-gathering side missions, the player has pieced together the Criminal Syndicate's multiverse operation: they are running a supply line through an unknown pocket universe, using it as a staging area to import exotic materials (weapons, artifacts, rare compounds) into 1218 for black market sale. The pocket is a warehouse-like space with a permanent portal stabilizer -- destroying this stabilizer will cut the supply line. Intel includes: pocket entry coordinates (obtained from an intercepted smuggler), stabilizer location within the pocket (center of warehouse floor), guard rotation (4 hostile NPCs, armed, rotating in pairs on 5-minute cycles), and booby trap warnings (trip wires, proximity sensors). |
| **Gear Required** | Tech Rig (portal opening), Demolition Charges (2 required -- craftable from components or purchased from a neutral arms dealer at high cost), EMP Grenade (1, for disabling proximity sensors), Scanner (upgraded, for trap detection), Combat gear (weapon of choice -- hostile NPCs are armed and will fight), Containment Pouch (optional, for looting exotic materials during sabotage) |
| **Allies Required** | Strange's faction provides: pocket coordinates and stabilization support (Strange Ritual +0.5 -- this is the second of the act's limited ritual uses). One combat ally available: either (A) Maya (stealth-focused, provides distraction and hacking support) or (B) a Strange's Network operative named Kai (combat-focused, provides direct fire support). Player chooses one. |
| **Portal Requirements** | Stability > 0.7 (Strange Ritual + Tech Rig achieves ~0.8), Bandwidth > 15 kg/s (player + ally + demolition gear = ~200kg, within standard bandwidth but needs headroom for combat movement), Anchor: Tech Rig anchor at entry point (44th St underground service tunnel -- concealed location) |
| **Prep Time** | ~30 minutes (gear assembly, ally briefing, travel to underground service tunnel, Tech Rig setup, Strange's ritual -- Strange performs remotely via Maya's relay). |

### Phase 2: Insertion

| Element | Details |
|---|---|
| **Entry Method** | Player-opened portal (Tech Rig + Strange boost) in an underground service tunnel beneath 44th Street. The tunnel location provides concealment and structural isolation (reduces Physical Heat from portal energy). Time: 3 AM sim-time. Portal class: Standard, upgraded with ally's assistance to 15 kg/s bandwidth. |
| **Transition Effects** | Crossing is rough -- the criminal pocket is dimensionally unstable (poorly maintained by the Syndicate's crude stabilization). Visual: 1218 tunnel dissolves into static-filled darkness, then resolves into a grimy industrial space. Audio: loud industrial hum, distant machinery, dripping water. The player feels strong disorientation (5-second adjustment -- longer than normal due to pocket instability). Gravity is 1.05x Earth standard (slightly heavier -- noticeable but not debilitating). Air is warm and metallic-smelling. |
| **Landing Zone** | A corner of the warehouse, behind stacked crates. The warehouse is large (approximately 50m x 30m), poorly lit (industrial overhead lights, many broken), and filled with crates, pallets of exotic materials, and smuggling equipment. The portal stabilizer is visible at the center: a crude device made from stolen tech components, bolted to the floor and humming with energy. Two guards are visible on patrol (far side of warehouse). Two more are in a break room (audible through a door). The player and ally have approximately 2 minutes before the patrol cycle brings guards near the entry point. |

### Phase 3: Objective

| Element | Details |
|---|---|
| **Primary Objective** | Plant 2 demolition charges on the portal stabilizer device (one on the power coupling, one on the control unit). Each charge requires 15 seconds to place (player must remain stationary and undetected/uncombated during placement). Once both charges are set, the player arms them (10-second countdown) and must reach a safe distance (20m) before detonation. Detonation destroys the stabilizer, which triggers a cascade failure in the pocket's integrity. |
| **Secondary Objective** | Loot the Syndicate's exotic material stockpile before destroying the stabilizer. The crates near the entry point contain 3 items of value: a Vibranium alloy ingot (compatibility 0.45), a tech weapon prototype (compatibility 0.65), and encrypted Syndicate communications data (Information class, no decay). Looting each crate takes 10 seconds. All 3 items fit within the mass budget. Risk: looting takes time, increasing detection probability. |
| **Failure Condition** | Player is killed in combat. OR both demolition charges are destroyed before placement (guards can shoot placed-but-unarmed charges, destroying them). OR portal collapses before player exits (pocket instability accelerates after detonation -- see Complication). |

### Phase 4: Complication

| Element | Details |
|---|---|
| **Scripted Twist** | The Syndicate has booby-trapped the stabilizer. When the first demolition charge is placed, a proximity sensor triggers an alarm (the EMP grenade can disable this sensor IF used before placement -- player choice). If the alarm triggers: all 4 guards are alerted immediately, break room guards emerge armed and hostile, and the warehouse's emergency lighting activates (eliminates stealth advantage). Additionally, the stabilizer emits a defensive energy pulse when tampered with -- player takes 15% HP damage on first charge placement. The ally provides cover fire (if Kai) or creates a distraction to draw 2 guards away (if Maya). After detonation, the pocket begins collapsing immediately -- the usual 3-minute countdown accelerates to 90 seconds because the pocket's only stabilizer was destroyed. Structural collapse begins: ceiling panels fall (dodge-able), floor cracks, crates topple. |
| **Dynamic Twist** | If Physical Heat in 1218 > 0.4, the underground tunnel portal is less stable (Heat coupling effect). Portal stability starts at 0.7 instead of 0.8, reducing the margin for error. If Criminal faction reputation is exactly 0.0 (neutral, not hostile), one guard recognizes the player and offers a deal: "Walk away, we'll give you a cut." This creates a moral choice branch (accept: abort mission, gain Criminal faction reputation +0.3 and ongoing income; refuse: proceed with sabotage, Criminal faction becomes fully hostile). If Ecological Heat > 0.4, the pocket is already partially destabilizing -- countdown after detonation is 60 seconds instead of 90. |

### Phase 5: Exfil

| Element | Details |
|---|---|
| **Exit Conditions** | Player (and ally) must return to the entry portal before pocket collapse. The portal is on the opposite side of the warehouse from the stabilizer -- approximately 40m run through a collapsing environment. Obstacles: falling debris (dodge), cracking floor (path-finding), panicked guards (combat or avoidance). If guards are neutralized before detonation, the path is clear. If guards survive, they are also fleeing toward the portal (they know it's the only exit) -- potential combat during retreat. |
| **Time Pressure** | 90-second countdown (or 60 if dynamic twist active). The portal itself is decaying: stability -0.15/min during pocket collapse (accelerated). If stability reaches 0.1 before the player exits, portal enters COLLAPSING and the player must make a critical decision: (A) attempt emergency traverse through a COLLAPSING portal (50% HP damage, 20% chance of random destination) or (B) search for the secondary portal (see below). |
| **Emergency Secondary Exit** | During the collapse, a secondary portal briefly manifests near the warehouse's loading dock (the pocket's instability tears open a seam). This is not pre-planned -- the player discovers it during the mission. The secondary portal leads to a random location in 1218 (within 500m of Times Square). It is UNSTABLE (traversal damage 20% HP) and exists for only 30 seconds. If the player uses it, they exit the pocket but arrive at an unexpected location with no prepared anchor or concealment. Evidence generation is high (uncontrolled portal exit in a random location). |

### Aftermath (NYC / EARTH-1218)

| Element | Details |
|---|---|
| **Evidence Generated** | Physical: underground tunnel portal site (scorch marks, structural stress, residue patch). If secondary exit used: additional uncontrolled evidence at random surface location (major residue patch, structural damage, witness probability high). Digital: sensor network detects both portal events. Seismic sensors may detect underground energy burst. Witness: minimal at primary site (underground). High at secondary site (if used). Smuggled goods (if looted): ongoing exotic material signatures. |
| **Heat Impact** | Physical: +0.1 (underground explosion energy transmitted through structure, minor surface vibration). Social: +0.05 (if any surface effects noticed) or +0.15 (if secondary exit used in public). Institutional: +0.1 (seismic sensors, energy detection, pattern recognition -- multiple portal events in short timeframe). Ecological: +0.15 (portal residue underground + pocket collapse energy bleedthrough). **Net Heat: +0.3 to +0.55 (this is a loud operation).** |
| **Faction Response** | Strange's Network: approves the sabotage (pocket threat eliminated). Reputation +0.1. Concerned about Heat levels -- may advise laying low. Criminal Syndicate: fully hostile (if not already). Supply line is disrupted: exotic goods prices increase 50% on black market for 72h sim-time, Syndicate activity in Times Square decreases for 48h, then slowly rebuilds using alternative routes. Syndicate puts a bounty on the player (assassination attempts, frequency based on Criminal faction hostility level). NYPD: seismic/energy data triggers investigation. "Underground disturbance" report filed. If secondary exit used, active investigation at that location (Institutional Heat +0.1 additional). Media: if secondary exit was public, news coverage of "underground explosion" or "sinkhole." Citizens' Watch: forum activity spikes about underground activity. |
| **Persistent Changes** | Underground tunnel: damaged, partially collapsed (inaccessible for future portal use without repair -- 48h and resources). Criminal supply line: disrupted for 72h sim-time (prices up, availability down, Syndicate reorganizing). Player inventory: looted goods (if secondary objective completed) -- Vibranium ingot, tech weapon, encrypted data. Each generates ongoing Heat. Story: Syndicate becomes a persistent antagonist. Ally (Maya or Kai) comments on the experience, relationship deepened. |
| **Rewards** | Criminal supply disruption (strategic advantage, temporary pricing shift). Looted exotic materials (if secondary completed): Vibranium ingot (crafting), tech weapon (combat), encrypted data (intel for future missions). Strange faction reputation +0.1. Operation completion XP (major). Unlocks late-game operations (Act 3 content). |

---

## Operation 5: The Witness

```
================================================================
OPERATION: THE WITNESS
================================================================
Type:       Recon
Universe:   Earth-1218 (Hub) + Brief pocket observation
Difficulty: ★★☆☆☆ (2 stars)
Unlock:     Complete Operation 2: Containment Protocol
            + Authority (NYPD) faction reputation > 0.1
            + Obtain CCTV access credentials (side quest)
```

### Phase 1: Prep (NYC / EARTH-1218)

| Requirement | Details |
|---|---|
| **Intel Required** | The NYPD's newly formed "Anomalous Events" liaison (Detective Reyes, a pragmatic cop who doesn't fully believe in portals but respects the evidence) has approached the player through Maya's network. Reyes needs documentation: his superiors want hard evidence of anomalous activity before authorizing resources. The player is tasked with observing and recording a known anomaly hotspot (42nd St / 7th Ave intersection) during a predicted activity window. Strange's network has predicted a minor anomaly event (not a full portal -- a "shimmer" that will manifest for approximately 10 minutes). |
| **Gear Required** | Surveillance camera (provided by Reyes -- records video admissible as evidence), Scanner (player's own -- records anomaly data), CCTV access credentials (obtained via side quest -- allows player to access 2 NYPD-affiliated cameras in the area for multi-angle coverage), Inconspicuous clothing (player must blend in as pedestrian). |
| **Allies Required** | Detective Reyes: on standby for debrief (not in field). Maya: provides earpiece guidance. No combat ally needed. |
| **Portal Requirements** | N/A for primary objective. If the player follows the subject through a portal (branching path -- see Complication), standard portal requirements apply (Tech Rig, stability > 0.5). |
| **Prep Time** | ~10 minutes (meet Reyes's dead-drop for camera, check CCTV access, travel to observation point, position for coverage). |

### Phase 2: Insertion

| Element | Details |
|---|---|
| **Entry Method** | No portal traversal (primary path). Player positions at the observation point -- a coffee shop with window view of the intersection, or a street-side bench with clear sightlines. The player has 3 camera positions to choose from (each covers different angles -- optimal coverage requires placing 2 CCTV feeds + handheld camera). |
| **Transition Effects** | N/A (hub observation). Environmental setup: the intersection is busy (mid-afternoon, moderate foot traffic). The predicted anomaly window is 15 minutes away. Player uses this time to set up cameras and scanner. |
| **Landing Zone** | 42nd St / 7th Ave intersection. Standard Times Square environment. The anomaly hotspot is a specific section of sidewalk near a subway entrance. Scanner shows low-level anomaly readings (intensity 0.3, slowly rising). |

### Phase 3: Objective

| Element | Details |
|---|---|
| **Primary Objective** | Record clear evidence of the anomaly event: (1) Handheld camera footage of the visual shimmer (minimum 30 seconds continuous recording during peak manifestation), (2) Scanner data log of anomaly intensity readings (automatic if scanner is active), (3) At least one CCTV angle capturing the event (from accessed cameras). All three evidence types required for full mission success. Partial evidence (2 of 3) is accepted at reduced reward. |
| **Secondary Objective** | Identify and photograph any NPCs who interact with the anomaly deliberately (i.e., someone who approaches it purposefully rather than stumbling near it by accident). This indicates other parties are aware of and monitoring anomaly sites. Success: provides Reyes with a "person of interest" lead (Institutional faction quest advancement). |
| **Failure Condition** | Player fails to capture any evidence (all cameras malfunction or are blocked). OR player is identified as a surveillance operative by the subject (if secondary objective leads to a confrontation -- see Complication). OR player causes a public disturbance that overshadows the anomaly event (Social Heat spike that triggers crowd response, ruining the controlled observation). |

### Phase 4: Complication

| Element | Details |
|---|---|
| **Scripted Twist** | During the anomaly event (shimmer reaches peak intensity 0.6 -- not a full portal, but visible to attentive observers), a figure appears. A person -- dressed in nondescript clothing, moving with purpose -- approaches the shimmer. They pull out a device (similar to the player's scanner but different design) and take readings. This is a member of the Criminal Syndicate's intel network, scouting anomaly sites for potential portal locations. The subject notices the player's scanner (brief mutual recognition -- both are "in the know"). The subject breaks eye contact and moves away quickly, heading toward a nearby alley. The anomaly begins to fade (natural decay). The player faces a critical decision: **(A) Stay and complete the recording** (maintain primary objective, lose the subject), **(B) Follow the subject** (abandon handheld camera position but CCTV continues recording -- partial primary evidence, gain pursuit intel), or **(C) Follow the subject through the portal** (if the subject opens a portal in the alley -- branches into a brief pocket observation, high risk, high reward). |
| **Dynamic Twist** | If Social Heat > 0.3, the area is more crowded than expected (elevated public interest in the area). The player's observation is hampered: more pedestrians block camera angles, increasing the difficulty of clean footage. If Institutional Heat > 0.3, Detective Reyes sends a text: "My captain is asking questions about our arrangement. Be discreet." -- this adds pressure to avoid any visible scanner use that might be reported. If the player has Criminal faction reputation > 0.0 (any positive relationship), the Syndicate scout may recognize the player and react differently: approaching to offer information (trade) rather than fleeing. |

### Phase 5: Exfil

| Element | Details |
|---|---|
| **Exit Conditions** | Path A (stay): observation complete, player collects camera data, walks to debrief with Reyes. Clean exit. Path B (follow): player follows subject through streets, gathering additional intel. Subject eventually loses the player or is cornered (player's choice to confront or observe). Player then debriefs Reyes. Path C (portal follow): player follows subject into a brief pocket (30-second observation window, pocket is tiny -- single room). Player observes what the subject is doing (relaying intel to Criminal faction contacts). Player must exit before pocket destabilizes (60-second window). Returns to 1218, debriefs Reyes. |
| **Time Pressure** | Path A: no time pressure (anomaly fades naturally, player collects at leisure). Path B: subject moves quickly -- player has 2 minutes to maintain pursuit before subject reaches a vehicle and escapes. Path C: 60-second pocket stability window. If player doesn't exit in time, pocket seals with player inside (Strange's emergency extraction, 5-minute delay, minor injury). |
| **Extraction Cost** | Path A: free (no portal involvement). Path B: free (foot pursuit in hub). Path C: Tech Rig stability cost (if player opens portal to follow) or subject's portal (unstable, traversal damage 10% HP). If emergency extraction needed (Path C timeout), Strange's resources are taxed (Strange faction reputation -0.05). |

### Aftermath (NYC / EARTH-1218)

| Element | Details |
|---|---|
| **Evidence Generated** | Primary evidence delivered to Reyes: video footage, scanner data, CCTV records. This evidence enters the institutional record (by design -- this is a sanctioned operation). Path B additional: subject description and movement pattern data. Path C additional: pocket observation data (exotic material detected, criminal activity documented). All evidence is intentionally generated for Reyes -- this is a "generate evidence on purpose" operation, rare in the game. |
| **Heat Impact** | Institutional: +0.05 (evidence delivered to NYPD -- this is the point, but it increases institutional awareness permanently). Social: +0.02 (any anomaly event in public generates minor social ripple). Ecological: +0.03 (anomaly event itself, not player-caused). Physical: +0.0 (no physical impact). Path C additional: Ecological +0.05 (portal traversal), Institutional +0.03 (more data in the system). **Net Heat: +0.1 (Path A) to +0.18 (Path C).** |
| **Faction Response** | Authority (NYPD): Reyes is satisfied. Evidence is compelling. His captain authorizes a small "anomalous events" budget. NYPD faction reputation +0.15. Reyes becomes a regular contact (unlocks NYPD-related side quests and intel sharing). Strange's Network: Maya is cautious -- giving evidence to NYPD is a double-edged sword. Institutional awareness helps and hurts. Strange faction reputation +0.0 (neutral -- they expected this). If Path C taken, Strange is mildly concerned about reckless portal use (reputation -0.05 but impressed by initiative, net neutral). Criminal Syndicate: if subject was identified, Syndicate knows someone is watching their scouts. Increased counter-surveillance in the area. If Path C was taken and player was observed inside the pocket, Syndicate is hostile (+0.1 hostility, potential retaliation). Media: if Path A footage leaks (10% chance -- Reyes's department has leaks), local news runs a "mysterious shimmer" segment. Belief meter +0.05 in the Times Square neighborhood. Citizens' Watch: if media coverage occurs, community forum activity increases. Local residents start paying more attention to anomaly sites. |
| **Persistent Changes** | NYPD: "Anomalous Events" liaison now has resources. Increased institutional sensor monitoring in the 42nd St area (+10% detection coverage). Player: established as an NYPD asset (player legal standing potentially shifts toward "asset" at higher reputation). Belief meter: +0.05 to +0.1 depending on evidence dissemination. Criminal Syndicate: if subject identified, scout pattern changes (new locations, increased counter-intel). |
| **Rewards** | NYPD faction reputation +0.15. Detective Reyes as ongoing contact (NYPD intel access, legal cover for certain activities, equipment loans). Evidence documentation XP. Path B bonus: Criminal Syndicate scout identification (intel asset for future operations). Path C bonus: pocket observation data (Strange's network values this -- reputation +0.1 if shared). Belief meter shift (gameplay consequence -- see Heat/Evidence Economy spec). Unlocks NYPD-faction side quest chain. |

---

## Operations Summary Matrix

| Operation | Type | Universe | Difficulty | Portal Traversal | Key Reward | Net Heat (est.) | Unlocked By |
|---|---|---|---|---|---|---|---|
| **Containment Protocol** | Contain | 1218 (hub) | 1 star | No | Tutorial completion, Strange alliance, Scanner | -0.01 to +0.04 | Game start |
| **The Snatch** | Extract | 616 Pocket | 2 stars | Yes (outbound + return) | Vaulted Eye artifact, Strange rep | +0.15 to +0.35 | Tutorial complete |
| **The Witness** | Recon | 1218 + pocket (optional) | 2 stars | Optional (Path C) | NYPD alliance, Reyes contact, Belief shift | +0.10 to +0.18 | Tutorial complete |
| **Dark Mirror** | Infiltrate | 838 Pocket | 3 stars | Yes (outbound + return) | Incursion intel, Act 2 unlock | +0.17 | The Snatch complete |
| **Supply Line** | Sabotage | Unknown Pocket | 4 stars | Yes (outbound + return) | Supply disruption, exotic loot, Act 3 unlock | +0.30 to +0.55 | Dark Mirror + 3 side missions |

### Recommended Play Order

```
1. Containment Protocol (tutorial, mandatory)
       |
       +---> 2. The Snatch (first portal traversal)
       |         |
       |         +---> 4. Dark Mirror (first infiltration, unlocks Act 2)
       |                    |
       |                    +---> [3 side missions: intel gathering chain]
       |                              |
       |                              +---> 5. Supply Line (climax of Act 1 operations)
       |
       +---> 3. The Witness (NYPD alliance, runs parallel to portal operations)
```

---

## Integration Notes

### System Dependencies

| System | How Operations Use It | How Operations Feed It |
|---|---|---|
| **Portal State Machine** | Operations define portal requirements (stability, bandwidth, anchor) and track portal state during mission | Operations generate portal events (open, traverse, collapse, seal) |
| **Translation Gate** | Operations involving extraction check item compatibility on import | Extracted items enter the Translation Gate economy (decay, evidence, maintenance) |
| **Heat System** | Operations check current Heat levels (dynamic twists) and generate Heat impacts | Operation aftermath feeds all four Heat channels |
| **Evidence Economy** | Operations generate evidence entries (physical, digital, witness) | Evidence from operations accumulates in the ledger, affects belief meter |
| **Faction System** | Operations require faction reputation thresholds and provide faction support | Operations change faction reputations and trigger faction responses |
| **Universe Profiles** | Operations reference target universe profiles for physics, cognition, and aesthetic | Operations may reveal new universe profile data (intel gathering) |

### Cross-Reference Documents

| Document | Relationship |
|---|---|
| `universe-profile-template-v0.md` | Each operation's target universe has a profile that determines physics, NPC behavior, and aesthetics |
| `portal-state-machine-v0.md` | Portal requirements and state transitions during operations are governed by this spec |
| `translation-gate-rules-v0.md` | Extracted items are evaluated by the Translation Gate on import |
| `heat-evidence-economy-spec-v0.md` | Operation aftermath feeds Heat channels and evidence ledger |
| `faction-response-table-v0.md` | Faction responses to operations are detailed in this table |

---

*End of Operations Library v0*
