# Universe Profile Template v0

> **Twin Earth NYC** -- Part 11: Multiverse Gameplay
> **Document:** Universe Profile Template
> **Version:** 0.1.0
> **Status:** Draft
> **Last Updated:** 2026-01-27

---

## Table of Contents

1. [Overview](#overview)
2. [Universe Profile Schema](#universe-profile-schema)
3. [Schema Field Reference](#schema-field-reference)
4. [EARTH-1218 Profile (Hub / Baseline)](#earth-1218-profile-hub--baseline)
5. [Toy Portal Pocket Profile (Test Pocket)](#toy-portal-pocket-profile-test-pocket)
6. [Usage Guidelines](#usage-guidelines)
7. [Integration Notes](#integration-notes)

---

## Overview

Every universe the player can visit, traverse, or interact with through portals is described by a **Universe Profile**. This document defines the canonical schema for those profiles, provides field-by-field reference documentation, and supplies two completed profiles:

- **EARTH-1218** -- the hub universe where Times Square gameplay takes place. This is the baseline against which all other universes are measured.
- **Toy Portal Pocket** -- a minimal test pocket used during development and early-game tutorial sequences to validate portal mechanics without introducing full multiverse complexity.

All universe profiles are consumed by the following downstream systems:

| Consumer System | Fields Used |
|---|---|
| Physics Engine | Physics Profile (gravity, speed of light, material overrides, energy rules) |
| NPC AI Director | Cognition Profile (awareness, memory, communication, stress) |
| Authority / Heat System | Law Profile (structure, enforcement, portal legality, player standing) |
| Rendering Pipeline | Aesthetic Profile (visual style, palette, architecture, lighting, audio) |
| Persistence Layer | Persistence Contract (damage, evidence, NPC memory, environment, loot) |
| Translation Gate | Physics Profile + Persistence Contract (compatibility scoring) |
| Portal State Machine | Physics Profile + Persistence Contract (stability modifiers) |

---

## Universe Profile Schema

The following is the canonical fill-in template. All fields are required unless marked `(optional)`.

```yaml
# ═══════════════════════════════════════════════════════════════
# UNIVERSE PROFILE
# ═══════════════════════════════════════════════════════════════

universe_profile:
  name: "[Human-readable name]"
  universe_id: "[e.g., EARTH-1218, EARTH-616, EARTH-838, POCKET-001]"
  classification: "[Hub / Pocket / Full]"
  #   Hub    = persistent home universe, full simulation
  #   Pocket = limited-scope fragment, may reset, reduced simulation
  #   Full   = complete alternate universe, persistent, full simulation
  description: "[1-2 sentence summary of this universe's identity]"
  version: "[schema version, e.g., 0.1.0]"
  author: "[designer name or team]"
  created: "[ISO date]"
  last_modified: "[ISO date]"

  # ═══ PHYSICS PROFILE ═══
  physics:
    gravity:
      value: "[float, m/s^2]"
      type: "[standard / modified / variable]"
      notes: "[any special behavior, e.g., 'variable near portals']"
    speed_of_light:
      value: "[standard (299792458 m/s) / modified]"
      type: "[standard / modified]"
      notes: "[if modified, describe impact on gameplay]"
    material_properties_override:
      enabled: "[true / false]"
      overrides: "[list of material:modification pairs, or 'none']"
      # Example: "steel:brittle, glass:elastic, water:viscous_x2"
    energy_conservation:
      mode: "[strict / relaxed / suspended]"
      notes: "[describe deviations, e.g., 'magic ignores thermodynamics']"
    special_physics_rules:
      - "[rule_1: description]"
      - "[rule_2: description]"
      # Examples: "magic_as_physics: spells obey force equations"
      #           "tech_enhanced: electronics operate at 2x efficiency"

  # ═══ COGNITION PROFILE ═══
  cognition:
    npc_awareness_level:
      value: "[baseline_human / enhanced / telepathic / limited]"
      detection_radius: "[meters, or 'standard']"
      notes: "[special awareness behaviors]"
    memory_model:
      type: "[standard_decay / perfect / fractured]"
      decay_rate: "[e.g., 'realistic -- forgets minor details after hours']"
      notes: "[special memory behaviors]"
    communication:
      primary: "[verbal / telepathic / tech_mediated]"
      secondary: "[optional secondary channel]"
      language: "[English / translated / alien / contextual]"
    stress_response:
      model: "[realistic / heightened / suppressed]"
      panic_threshold: "[0.0-1.0, lower = more easily panicked]"
      notes: "[special stress behaviors]"

  # ═══ LAW PROFILE ═══
  law:
    authority_structure: "[democratic / authoritarian / anarchic / feudal / corporate]"
    enforcement_level: "[heavy / moderate / light / none]"
    enforcement_entities: "[list of entities, e.g., 'NYPD, federal agencies']"
    legal_status_of_portals: "[unknown / classified / public / weaponized]"
    player_legal_standing: "[citizen / alien / fugitive / asset / unknown]"
    special_laws:
      - "[any universe-specific legal considerations]"

  # ═══ AESTHETIC PROFILE ═══
  aesthetic:
    visual_style: "[photorealistic / stylized / noir / neon / organic]"
    color_palette:
      primary: "[e.g., 'earth tones', 'vibrant primaries']"
      accent: "[e.g., 'neon blue highlights']"
      mood: "[warm / cool / neutral / shifted]"
    architecture:
      base: "[NYC-derivative / alien / art-deco / brutalist / organic]"
      modifications: "[describe deviations from base]"
    lighting_model:
      type: "[natural / artificial_dominant / bioluminescent / otherworldly]"
      time_of_day: "[dynamic / fixed / N/A]"
      special: "[any unique lighting behaviors]"
    audio_signature:
      ambient: "[urban / silence / industrial / alien_soundscape]"
      music_style: "[describe musical tone]"
      special_sounds: "[any universe-specific audio cues]"

  # ═══ PERSISTENCE CONTRACT ═══
  persistence:
    damage_persistence:
      mode: "[full / partial / none]"
      decay_rate: "[if partial, e.g., '50% per 24h sim-time']"
      notes: "[special damage persistence rules]"
    evidence_generation:
      mode: "[standard / enhanced / disabled]"
      types: "[physical / digital / witness -- which are active]"
      notes: "[special evidence rules]"
    npc_memory_of_player:
      mode: "[persistent / session_only / none]"
      scope: "[individual / faction / universal]"
      notes: "[how NPCs remember the player]"
    environmental_changes:
      mode: "[permanent / temporary / procedural_reset]"
      revert_timer: "[if temporary, time to revert]"
      notes: "[what changes and what doesn't]"
    loot_artifact_export:
      mode: "[allowed / restricted / forbidden]"
      translation_gate: "[yes / no -- requires compatibility check]"
      restrictions: "[any specific restrictions on export]"
```

---

## Schema Field Reference

### Classification Types

| Classification | Description | Simulation Scope | Persistence | Typical Use |
|---|---|---|---|---|
| **Hub** | The player's home universe. Full simulation, always loaded. | Full city simulation, all systems active | Complete persistence across sessions | EARTH-1218 only |
| **Pocket** | A fragment of a universe. Limited scope, may reset. | Reduced scope (single area, limited NPCs) | Varies (none to partial) | Operations, tutorials, test environments |
| **Full** | A complete alternate universe. Full simulation when loaded. | Full simulation when active | Full persistence | Major story universes (future content) |

### Physics Field Details

| Field | Valid Range | Gameplay Impact |
|---|---|---|
| `gravity.value` | 0.0 -- 20.0 m/s^2 | Movement speed, jump height, fall damage, projectile arcs |
| `speed_of_light` | standard / 0.5x -- 2.0x | Visual effects only (no relativistic gameplay) |
| `material_properties_override` | Per-material modifiers | Item durability, structural integrity, crafting recipes |
| `energy_conservation` | strict / relaxed / suspended | Determines if exotic energy sources work, magic viability |
| `special_physics_rules` | Freeform list | Universe-specific mechanics (magic, tech boost, etc.) |

### Cognition Field Details

| Field | Valid Range | Gameplay Impact |
|---|---|---|
| `npc_awareness_level` | baseline / enhanced / telepathic / limited | Stealth difficulty, detection ranges, social deception |
| `memory_model` | standard / perfect / fractured | NPC recall of player actions, reputation persistence |
| `communication` | verbal / telepathic / tech_mediated | Dialogue options, eavesdropping mechanics, language barriers |
| `stress_response` | realistic / heightened / suppressed | Crowd behavior, panic propagation, witness reliability |

### Persistence Contract Details

| Field | Impact on Translation Gate | Impact on Heat System |
|---|---|---|
| `damage_persistence` | Exported damage evidence carries over | Persistent damage feeds Physical Heat channel |
| `evidence_generation` | Evidence types determine detection signature | Active evidence types feed Institutional Heat |
| `npc_memory_of_player` | Cross-universe reputation possible if persistent | Witness Heat depends on memory mode |
| `environmental_changes` | Determines if extraction sites remain viable | Environmental changes feed Ecological Heat |
| `loot_artifact_export` | Core gate for Translation Gate system | Exported items generate ongoing Heat via signatures |

---

## EARTH-1218 Profile (Hub / Baseline)

This is the canonical hub universe. All other universes are measured against this profile for Translation Gate compatibility scoring.

```yaml
# ═══════════════════════════════════════════════════════════════
# EARTH-1218 — HUB UNIVERSE (BASELINE)
# ═══════════════════════════════════════════════════════════════

universe_profile:
  name: "Earth Prime — New York City"
  universe_id: "EARTH-1218"
  classification: "Hub"
  description: >
    The real-world baseline. Standard physics, democratic governance,
    photorealistic rendering. This is present-day NYC as experienced by
    the player — Times Square, Midtown Manhattan, and surrounding blocks.
    Marvel events are fiction here. Portals are anomalies, not features.
  version: "0.1.0"
  author: "Twin Earth NYC Design Team"
  created: "2026-01-27"
  last_modified: "2026-01-27"

  # ═══ PHYSICS PROFILE ═══
  physics:
    gravity:
      value: 9.81
      type: "standard"
      notes: "No modifications. Baseline Earth gravity throughout."
    speed_of_light:
      value: "standard (299792458 m/s)"
      type: "standard"
      notes: "No modifications. Standard electromagnetic propagation."
    material_properties_override:
      enabled: false
      overrides: "none"
    energy_conservation:
      mode: "strict"
      notes: >
        All energy interactions obey conservation laws. No free energy.
        Exotic items imported from other universes experience energy
        drain and degradation precisely because 1218 enforces strict
        conservation. Portal energy is the sole exception — treated as
        an external input, not a violation.
    special_physics_rules:
      - "portal_anomaly: Portals introduce localized physics distortions
         within entropy_bleed radius. Inside bleed zone, gravity may
         fluctuate +/- 5%, EM readings spike, temperature shifts occur.
         These are symptoms, not controllable mechanics."
      - "reality_inertia: EARTH-1218 actively resists foreign physics.
         Exotic items and energy constructs decay because this universe's
         physics 'pushes back' against incompatible rules. This is the
         foundation of the Translation Gate decay mechanic."

  # ═══ COGNITION PROFILE ═══
  cognition:
    npc_awareness_level:
      value: "baseline_human"
      detection_radius: "standard (visual: 50m clear LOS, audio: 20m)"
      notes: >
        NPCs have realistic human perception. They can be fooled by
        disguises, distracted by noise, and miss things outside their
        attention focus. No supernatural awareness. Peripheral vision
        is modeled — NPCs detect movement at edges before detail.
    memory_model:
      type: "standard_decay"
      decay_rate: >
        Minor details: forgotten after 2-4 hours sim-time.
        Significant events: remembered for 24-72 hours sim-time.
        Traumatic events: permanent memory (witness reports persist).
        Faces: recognized for 48 hours after single encounter,
        permanently after 3+ encounters.
      notes: >
        NPC memory feeds the Evidence Economy. Witness memories generate
        social Heat. Memory decay provides natural Heat cooldown — if
        enough time passes without reinforcing events, witnesses forget
        and social Heat decays.
    communication:
      primary: "verbal"
      secondary: "phone/text (tech-mediated for off-screen NPCs)"
      language: "English (with contextual multilingual NYC flavor)"
    stress_response:
      model: "realistic"
      panic_threshold: 0.5
      notes: >
        Standard human stress responses. Crowds exhibit emergent panic
        behavior — stampede risk at high density + high stress. Individual
        NPCs have varied thresholds (tourists panic easier than locals).
        First responders have suppressed panic (threshold 0.8).
        Panic propagation: stressed NPCs stress nearby NPCs at -0.1
        radius per second.

  # ═══ LAW PROFILE ═══
  law:
    authority_structure: "democratic"
    enforcement_level: "moderate"
    enforcement_entities:
      - "NYPD (primary — patrol, investigation, SWAT)"
      - "FDNY (fire/hazmat response to anomaly events)"
      - "Federal agencies (triggered at Institutional Heat > 0.6)"
      - "Private security (Times Square specific, lower authority)"
    legal_status_of_portals: "unknown"
    player_legal_standing: "citizen"
    special_laws:
      - "Portal activity has no legal framework — authorities treat
         anomalies as hazmat/structural events initially. At higher
         Institutional Heat and Belief, specialized legal responses
         emerge (executive orders, emergency powers)."
      - "Player starts as ordinary citizen. Legal standing can shift
         to 'person of interest' (Institutional Heat > 0.4),
         'suspect' (> 0.6), or 'asset' (if cooperating with authority
         faction at high trust)."
      - "Destruction of property, assault, and other standard crimes
         are prosecutable. Portal-related charges do not exist at
         game start but may be created dynamically if Belief rises
         high enough and Institutional Heat triggers legislative
         response."

  # ═══ AESTHETIC PROFILE ═══
  aesthetic:
    visual_style: "photorealistic"
    color_palette:
      primary: "earth tones — concrete gray, asphalt black, brick red,
                glass blue-green, steel silver"
      accent: "neon signage (Times Square), yellow taxi, traffic light
               spectrum, LED billboard colors"
      mood: "neutral-warm (daytime), cool-blue (nighttime), warm-orange
             (golden hour), harsh-white (artificial night lighting)"
    architecture:
      base: "NYC-derivative"
      modifications: >
        Faithful recreation of Times Square and surrounding Midtown
        blocks. Recognizable landmarks with fictional business names.
        Architecture spans NYC's range: art-deco (older buildings),
        glass-and-steel (modern towers), mixed commercial (ground level).
        Portal anomaly zones may exhibit subtle architectural distortion
        (within entropy_bleed radius) — slight warping, color shifting,
        geometry that doesn't quite resolve.
    lighting_model:
      type: "natural + artificial_dominant (Times Square)"
      time_of_day: "dynamic (full day-night cycle, ~1h real = 24h sim)"
      special: >
        Times Square lighting is a character in itself. Billboards
        provide constant artificial light. Portal anomalies introduce
        light distortions — flickering, color temperature shifts, shadow
        anomalies. The IoT sensor network occasionally causes visible
        data-overlay effects (AR-style) when player uses detection
        equipment.
    audio_signature:
      ambient: "urban"
      music_style: >
        Diegetic urban soundscape: traffic, crowd chatter, distant
        sirens, subway rumble, street performers. Non-diegetic score
        is minimal and tension-driven — low synth drones during anomaly
        events, percussive hits during action, quiet piano for
        character moments.
      special_sounds:
        - "portal_hum: Low-frequency resonance near active portals,
           increases with stability. Detectable before visual signs."
        - "reality_crackle: Static-electric sound during translation
           gate traversal and near high entropy_bleed zones."
        - "heat_pulse: Subliminal bass throb that intensifies as
           combined Heat rises. Player learns to 'feel' Heat level."

  # ═══ PERSISTENCE CONTRACT ═══
  persistence:
    damage_persistence:
      mode: "full"
      decay_rate: "N/A (full persistence)"
      notes: >
        All damage to the environment persists until repaired. Broken
        windows, cracked pavement, scorch marks from portal energy —
        all remain visible and detectable. Repair occurs through NPC
        city maintenance (slow, days of sim-time) or player-initiated
        cleanup actions. Persistent damage feeds Physical Heat channel
        and generates physical evidence class entries.
    evidence_generation:
      mode: "standard"
      types: "physical, digital, witness — all three active"
      notes: >
        Physical: debris, scorch marks, residue patches, structural
        damage. Persists until cleaned.
        Digital: CCTV footage (auto-captured within camera FOV), IoT
        sensor logs (anomaly readings), device data (phone recordings
        by NPC bystanders). Persists in institutional memory.
        Witness: NPC testimony, subject to memory decay model. Most
        volatile evidence class but hardest to suppress.
    npc_memory_of_player:
      mode: "persistent"
      scope: "individual (recognized by NPCs who have met player) +
              faction (faction reputation persists globally)"
      notes: >
        Individual NPCs remember the player based on encounter count
        and significance. Faction reputation is shared — all faction
        members know the player's standing. Cross-session persistence
        is full. NPCs may reference past events in dialogue.
    environmental_changes:
      mode: "permanent"
      revert_timer: "N/A (permanent until repaired/restored)"
      notes: >
        Environmental changes from portal activity, combat, and player
        actions are permanent. The city evolves based on cumulative
        player impact. Road closures, construction barriers, increased
        security presence — all persist and accumulate. This creates
        a living record of the player's actions visible in the world.
    loot_artifact_export:
      mode: "allowed"
      translation_gate: true
      restrictions: >
        Items imported into EARTH-1218 are subject to Translation Gate
        compatibility scoring. All imports must pass through an active
        portal. Mass cap: 500kg per traversal. Energy constructs
        cannot survive translation. Exotic items decay according to
        their compatibility score. All imports generate detection
        signatures proportional to their incompatibility.
```

### EARTH-1218 Quick Reference Card

| Category | Value | Notes |
|---|---|---|
| **Universe ID** | EARTH-1218 | Hub / Baseline |
| **Classification** | Hub | Always loaded, full simulation |
| **Gravity** | 9.81 m/s^2 (standard) | Baseline |
| **Speed of Light** | Standard | Baseline |
| **Material Overrides** | None | Baseline |
| **Energy Conservation** | Strict | Exotic items decay here |
| **NPC Awareness** | Baseline Human | Visual 50m, Audio 20m |
| **Memory Model** | Standard Decay | Minor: 2-4h, Significant: 24-72h, Traumatic: permanent |
| **Communication** | Verbal + Phone | English primary |
| **Stress Response** | Realistic | Panic threshold 0.5, propagation modeled |
| **Authority** | Democratic | NYPD primary, federal at high Heat |
| **Enforcement** | Moderate | Escalates with Institutional Heat |
| **Portal Legal Status** | Unknown | No legal framework at game start |
| **Player Standing** | Citizen | Can shift based on Heat/cooperation |
| **Visual Style** | Photorealistic | Faithful NYC recreation |
| **Color Palette** | Earth Tones + Neon Accents | Times Square signature lighting |
| **Architecture** | NYC-Derivative | Art-deco to modern glass-steel |
| **Lighting** | Natural + Artificial | Dynamic day-night, billboard-lit |
| **Audio** | Urban Ambient | Diegetic soundscape, minimal score |
| **Damage Persistence** | Full | Persists until repaired |
| **Evidence Generation** | Standard (all types) | Physical, digital, witness |
| **NPC Memory** | Persistent | Individual + faction scope |
| **Environment Changes** | Permanent | City evolves with player actions |
| **Loot Export** | Allowed (Translation Gate) | 500kg cap, compatibility scoring |

---

## Toy Portal Pocket Profile (Test Pocket)

This is a minimal-complexity pocket universe designed for two purposes:

1. **Development testing** -- validate portal mechanics (opening, traversal, stabilization, collapse) without engaging the full complexity of alternate universe simulation.
2. **Early-game tutorial** -- introduce the player to portal traversal in a low-stakes environment before real operations begin.

The pocket represents a small, self-contained space with reduced physics, simple NPC behavior, no law enforcement, and zero persistence (resets on exit). It is stylized as a noir-influenced fragment -- a darkened alleyway that loops back on itself, populated by a handful of enhanced-awareness NPCs who serve as tutorial guides.

```yaml
# ═══════════════════════════════════════════════════════════════
# TOY PORTAL POCKET — TEST / TUTORIAL POCKET UNIVERSE
# ═══════════════════════════════════════════════════════════════

universe_profile:
  name: "Toy Portal Pocket — The Loop Alley"
  universe_id: "POCKET-TEST-001"
  classification: "Pocket"
  description: >
    A minimal test pocket for validating portal mechanics and
    introducing players to multiverse traversal. A noir-styled
    looping alleyway with reduced gravity, enhanced NPCs, no law,
    and no persistence. Exists only while the portal connecting
    to it remains open. Resets completely on exit.
  version: "0.1.0"
  author: "Twin Earth NYC Design Team"
  created: "2026-01-27"
  last_modified: "2026-01-27"

  # ═══ PHYSICS PROFILE ═══
  physics:
    gravity:
      value: 7.85
      type: "modified"
      notes: >
        0.8x Earth standard (7.85 m/s^2). Player immediately feels
        the difference — slightly floaty jumps, slower falls, objects
        feel lighter. This is the first signal that 'you are not in
        Kansas anymore.' Designed to be noticeable but not disorienting.
        Teaches players to expect physics differences across universes.
    speed_of_light:
      value: "standard"
      type: "standard"
      notes: "No modification. Visual rendering is standard."
    material_properties_override:
      enabled: true
      overrides:
        - "glass: unbreakable (tutorial environment, prevent sequence breaks)"
        - "metal: resonant (produces audible hum near portal energy,
           audio tutorial cue)"
    energy_conservation:
      mode: "relaxed"
      notes: >
        Energy conservation is relaxed to allow tutorial devices to
        function without resource management. Stabilization devices
        recharge freely. This removes resource pressure so the player
        can focus on learning portal mechanics.
    special_physics_rules:
      - "looping_geometry: The alley loops — walking to the end returns
         you to the beginning. This is a spatial anomaly specific to
         this pocket. Teaches players that pocket geometry is unreliable."
      - "echo_physics: Sounds echo with slight delay and pitch shift,
         creating an uncanny audio environment. Reinforces the 'wrong
         universe' feeling."
      - "portal_magnetism: Objects near the portal entry point drift
         slowly toward it. Visual and physics cue that the portal is
         the way out."

  # ═══ COGNITION PROFILE ═══
  cognition:
    npc_awareness_level:
      value: "enhanced"
      detection_radius: "extended (visual: 100m, audio: 50m — pocket is small)"
      notes: >
        NPCs in the test pocket have enhanced awareness. They detect
        the player immediately upon entry and approach to deliver
        tutorial dialogue. This ensures the player cannot miss tutorial
        content. Enhanced awareness also demonstrates that NPC cognition
        varies across universes — a lesson for future operations.
    memory_model:
      type: "fractured"
      decay_rate: "instant — NPCs reset to default state each visit"
      notes: >
        NPCs have fractured memory. They do not remember previous
        visits. Each entry is treated as the first encounter. This
        is narratively framed as a property of the pocket — 'this
        place doesn't hold onto things.' Mechanically, it allows
        repeatable tutorial runs without continuity issues.
    communication:
      primary: "verbal"
      secondary: "none"
      language: >
        English, but with slight distortion (reverb, occasional word
        substitution). NPCs speak clearly enough for tutorial purposes
        but with an uncanny quality that signals 'different universe.'
    stress_response:
      model: "suppressed"
      panic_threshold: 1.0
      notes: >
        NPCs do not panic. They are tutorial constructs. No matter
        what the player does, NPCs remain calm and helpful. This
        prevents tutorial disruption and teaches the player that
        NPC behavior varies across universes.

  # ═══ LAW PROFILE ═══
  law:
    authority_structure: "anarchic"
    enforcement_level: "none"
    enforcement_entities: "none"
    legal_status_of_portals: "unknown"
    player_legal_standing: "unknown"
    special_laws:
      - "No laws, no enforcement, no consequences. The pocket exists
         outside any governance structure. This allows the player to
         experiment freely with portal mechanics — stabilize, destabilize,
         overload — without Heat or legal consequences."
      - "Tutorial NPCs may comment on player actions ('That was reckless'
         or 'Good technique') but these are instructional, not punitive."

  # ═══ AESTHETIC PROFILE ═══
  aesthetic:
    visual_style: "noir"
    color_palette:
      primary: "desaturated — black, dark gray, charcoal, deep shadow"
      accent: "single accent color: amber/gold (portal energy, NPC eyes,
               interactive highlights)"
      mood: "cool-dark, high contrast, deep shadows, amber warmth at
             points of interest"
    architecture:
      base: "NYC-derivative (distorted)"
      modifications: >
        The pocket resembles a NYC alleyway but wrong. Proportions are
        slightly off — walls too tall, ground too narrow, fire escapes
        at impossible angles. Signage is present but text is scrambled
        or in unknown characters. Dumpsters, pipes, and urban detritus
        are present but subtly wrong (too smooth, wrong materials,
        slightly oversized). The overall effect is 'familiar but alien.'
    lighting_model:
      type: "artificial_dominant"
      time_of_day: "fixed (perpetual night)"
      special: >
        No natural light source. Illumination comes from a sourceless
        ambient glow (dim), the portal itself (amber), and scattered
        neon elements (dim amber). Heavy use of volumetric fog.
        Shadows are deep and well-defined. The visual language is
        classic noir — high contrast, dramatic shadows, isolated
        pools of light. Portal energy casts moving amber light on
        nearby surfaces.
    audio_signature:
      ambient: "near-silence with distant, unidentifiable reverb"
      music_style: >
        Sparse, ambient noir score. Solo saxophone or muted trumpet,
        heavily reverbed. Plays only during key tutorial moments.
        Otherwise, near-silence with subtle environmental drones.
      special_sounds:
        - "loop_transition: A soft chime when the player reaches the
           loop boundary and resets to the alley entrance."
        - "npc_approach: Footsteps with slightly wrong timing (too slow
           for the stride length), enhancing uncanny feeling."
        - "portal_call: The connecting portal emits a periodic low
           tone, guiding the player back to the exit."

  # ═══ PERSISTENCE CONTRACT ═══
  persistence:
    damage_persistence:
      mode: "none"
      decay_rate: "instant reset on exit"
      notes: >
        No damage persists. The pocket resets to its default state
        every time the player exits and re-enters. This allows
        repeatable experimentation. Smash a window (they're unbreakable
        anyway), kick a dumpster, overload the portal — everything
        resets. Narratively: 'the pocket doesn't remember.'
    evidence_generation:
      mode: "disabled"
      types: "none active"
      notes: >
        No evidence is generated within the pocket. No CCTV, no
        sensors, no witnesses (tutorial NPCs don't count as witnesses).
        Actions in the pocket have zero Heat impact on EARTH-1218.
        This is the safe space for learning.
    npc_memory_of_player:
      mode: "none"
      scope: "N/A"
      notes: >
        NPCs do not remember the player between visits. Each entry
        triggers fresh tutorial dialogue. No reputation, no relationship
        building, no consequences.
    environmental_changes:
      mode: "procedural_reset"
      revert_timer: "instant (on player exit)"
      notes: >
        All environmental changes revert the moment the player exits
        the pocket. The pocket state is a pure function of its template —
        no accumulated history. If the player re-enters, everything is
        exactly as it was on first entry.
    loot_artifact_export:
      mode: "forbidden"
      translation_gate: false
      restrictions: >
        Nothing can be exported from the test pocket. Items picked up
        inside the pocket disappear from inventory on exit. This
        prevents tutorial rewards from affecting the real game economy
        and reinforces the pocket's disposable nature. The player
        receives a tutorial-completion reward in EARTH-1218 instead
        (granted by Strange's contact upon return).
```

### Toy Portal Pocket Quick Reference Card

| Category | Value | Notes |
|---|---|---|
| **Universe ID** | POCKET-TEST-001 | Test / Tutorial pocket |
| **Classification** | Pocket | Resets on exit |
| **Gravity** | 7.85 m/s^2 (0.8g) | Noticeably lighter |
| **Speed of Light** | Standard | No modification |
| **Material Overrides** | Glass: unbreakable, Metal: resonant | Tutorial safety + audio cue |
| **Energy Conservation** | Relaxed | Free device recharging |
| **NPC Awareness** | Enhanced | 100m visual, 50m audio |
| **Memory Model** | Fractured (instant reset) | No memory between visits |
| **Communication** | Verbal (distorted) | English with reverb |
| **Stress Response** | Suppressed | NPCs never panic |
| **Authority** | Anarchic | No governance |
| **Enforcement** | None | Zero consequences |
| **Portal Legal Status** | Unknown | N/A |
| **Player Standing** | Unknown | N/A |
| **Visual Style** | Noir | High contrast, deep shadows |
| **Color Palette** | Desaturated + Amber accent | Black/gray with gold highlights |
| **Architecture** | NYC-Derivative (distorted) | Familiar but wrong |
| **Lighting** | Artificial (perpetual night) | Volumetric fog, amber portal light |
| **Audio** | Near-silence + noir score | Sparse, reverbed, uncanny |
| **Damage Persistence** | None (resets on exit) | Full experimentation freedom |
| **Evidence Generation** | Disabled | Zero Heat impact |
| **NPC Memory** | None | Fresh tutorial each visit |
| **Environment Changes** | Procedural reset (instant) | Clean slate every entry |
| **Loot Export** | Forbidden | Nothing leaves the pocket |

---

## Usage Guidelines

### Creating a New Universe Profile

1. **Copy the schema template** from Section 2 above.
2. **Fill in all required fields.** Every field has a type and valid range described in Section 3.
3. **Define the profile relative to EARTH-1218.** Use phrases like "0.8x standard gravity" or "enhanced compared to baseline" to make differences explicit.
4. **Test with the Translation Gate.** Run a compatibility check against EARTH-1218 for at least 5 representative items to validate physics and material override settings.
5. **Register the profile** in the Universe Registry (maintained separately) with its `universe_id`.

### Profile Versioning

- Profiles use semantic versioning: `major.minor.patch`.
- **Patch** (0.1.1): Typo fixes, notes updates, no mechanical changes.
- **Minor** (0.2.0): Value adjustments, new special rules, balance changes.
- **Major** (1.0.0): Structural changes to the profile, new required fields, breaking changes to consumers.

### Classification Upgrade Path

Pockets can be upgraded to Full universes in later content packs:

```
POCKET (v0: limited scope, may reset)
   ↓ [content expansion]
FULL (v1: complete simulation, persistent)
```

This requires filling in all fields that were simplified in the pocket version and implementing full persistence.

---

## Integration Notes

### Downstream System Contracts

| System | Required Fields | Update Frequency |
|---|---|---|
| Physics Engine | `physics.*` | On universe load |
| NPC AI Director | `cognition.*` | On universe load + per-NPC spawn |
| Authority / Heat System | `law.*`, `persistence.evidence_generation` | On universe load + per-event |
| Rendering Pipeline | `aesthetic.*` | On universe load |
| Persistence Layer | `persistence.*` | On universe load + per-save |
| Translation Gate | `physics.*`, `persistence.loot_artifact_export` | Per-item translation check |
| Portal State Machine | `physics.special_physics_rules`, `persistence.*` | Per-portal-state-change |

### Cross-Reference Documents

| Document | Relationship |
|---|---|
| `portal-state-machine-v0.md` | Portal behavior is modified by universe physics profile |
| `translation-gate-rules-v0.md` | Compatibility scoring uses physics + material profiles of source and destination |
| `operations-library-v0.md` | Each operation references a target universe profile |
| `heat-evidence-economy-spec-v0.md` | Evidence generation mode from persistence contract feeds Heat system |
| `faction-response-table-v0.md` | Faction behavior is scoped to EARTH-1218 law profile |

---

*End of Universe Profile Template v0*
