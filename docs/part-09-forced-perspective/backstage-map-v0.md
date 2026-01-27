# Backstage Map v0

**Twin Earth NYC -- Part 9: Forced Perspective**
**Document:** Backstage Map and Seam Policy
**Version:** 0.1.0
**Status:** Draft
**Last Updated:** 2026-01-27

---

## 1. Purpose

The Times Square slice is a bounded stage. Like a theater set, it has a **show side** (where the audience -- the player -- experiences the illusion) and a **backstage** (where the illusion ends and the machinery is hidden). This document classifies every zone in the slice, catalogs the seams where the illusion must be masked, and defines the policy for how each seam is disguised, streamed, and failure-protected.

---

## 2. Zone Classification

Every cubic meter of the Times Square slice falls into one of three zone types. Zone type determines default fidelity, accessibility, and streaming behavior.

| Zone Type | Description | Default Fidelity | Player Accessible | Streaming Behavior |
|-----------|-------------|-------------------|-------------------|--------------------|
| **Show Street** | Main pedestrian and vehicle corridors. Includes Broadway, 7th Avenue, the TKTS pedestrian island, the bowtie intersection, and all sidewalks between 42nd and 47th Streets. This is the primary performance space. | Full fidelity (near-band treatment always). All invariants enforced. Truth and illusion layers fully populated. | **Yes, always.** This is the player's primary navigable space. All collision, navigation, and interaction systems active. | Always loaded. Never streamed out. Resident in memory for the duration of the Times Square gameplay session. |
| **Support Zone** | Adjacent blocks and secondary streets visible from Show Street but not the primary stage. Includes: side streets (42nd--47th between 6th and 8th Aves), rear facades of buildings facing away from the bowtie, upper floors of buildings beyond the 5th story. | Mid-band default. Upgrades to near-band when the player approaches or has direct sightline within 30 m. | **Yes, but with reduced detail.** Player can walk down side streets. Collision and navigation active. Interaction limited (no mission content, fewer interactive props). | Loaded at session start in mid-fidelity. Upgrades streamed on demand when player approaches (2 s pre-stream window). |
| **Backstage** | Service alleys not visible from Show Street, subway tunnels (below grade), building interiors that are not mission spaces, rooftops not designated as accessible, and all geometry beyond the slice boundary. | Minimal. No visual content until the Director issues an inflation request. Truth-layer collision shells may exist (to block player from falling through the world) but render geometry is absent. | **No** (masked by diegetic barriers). Exception: backstage zones that become accessible during specific missions are inflated with content when the mission activates. | Not loaded by default. Inflated on demand when (a) the player approaches a backstage entrance that is becoming accessible, or (b) a mission script triggers backstage content. Inflation takes 1--3 s; the seam mask hides the loading. |

### 2.1 Zone Map -- Plan View (Schematic)

```
                    47th St (S04 - North Boundary)
    ================================================================
    |  BACKSTAGE  |     SUPPORT      |     SUPPORT     | BACKSTAGE |
    |  (west)     |   (side street)  |  (side street)  | (east)    |
    |             |                  |                  |           |
    |  S01 -------|--- 7th Ave ------|--- Broadway -----|---- S02   |
    |  (west      |                  |    SHOW          | (east     |
    |  boundary)  |  SHOW STREET     |    STREET        | boundary) |
    |             |  (7th Ave)       |  (Broadway)      |           |
    |             |                  |                  |           |
    |             |     BOWTIE       |                  |           |
    |             |   INTERSECTION   |                  |           |
    |             |   (SHOW STREET)  |                  |           |
    |             |                  |                  |           |
    |             |   TKTS ISLAND    |                  |           |
    |             |   (SHOW STREET)  |                  |           |
    |             |                  |                  |           |
    |  S01 -------|--- 7th Ave ------|--- Broadway -----|---- S02   |
    |  BACKSTAGE  |     SUPPORT      |     SUPPORT     | BACKSTAGE |
    ================================================================
                    42nd St (S03 - South Boundary)
```

---

## 3. Seam Locations

Ten seams define the boundaries and transition points of the Times Square slice. Each seam is classified by type and assigned a diegetic mask that justifies the boundary within the game world.

| Seam ID | Location | Type | Mask Method | Mask Description |
|---------|----------|------|-------------|------------------|
| **S01** | West side of 7th Ave (slice western boundary) | Edge of world | Construction scaffolding + barriers | Full-height scaffolding wraps the western building faces. Orange construction barriers and "Sidewalk Closed" signs block pedestrian access. Scaffolding netting obscures the void beyond. |
| **S02** | East side of Broadway (slice eastern boundary) | Edge of world | Parked delivery trucks + scaffolding | A line of double-parked delivery trucks blocks the street. Scaffolding on adjacent buildings extends the visual barrier upward. "No Pedestrian Access" signs reinforce. |
| **S03** | South of 42nd St (slice southern boundary) | Edge of world | Road work barriers + police tape | Full road closure with concrete Jersey barriers, orange drums, and yellow police tape. A "Water Main Repair" sign provides narrative justification. Utility work vehicles parked across the street. |
| **S04** | North of 47th St (slice northern boundary) | Edge of world | Construction crane + chain-link fencing | A tower crane base occupies the intersection. Chain-link fencing with privacy mesh extends across the full street width. "Hard Hat Area -- Authorized Personnel Only" signage. |
| **S05** | Alley behind 43rd St (between Broadway and 7th) | Backstage corridor | Dumpsters + locked gate | A row of commercial dumpsters partially blocks the alley entrance. A padlocked steel gate with "Private Property" signage blocks further access. Alley is dimly lit, uninviting. |
| **S06** | 42nd St subway entrance | Transition to underground | Stairs descend into darkness / load zone | Physical stairs lead down from street level. After the first landing, lighting dims sharply. A load-zone trigger halfway down the stairs initiates streaming of the subway level (if implemented) or presents a locked turnstile with "Service Suspended" signage (v0 fallback). |
| **S07** | Marriott Marquee lobby | Interior transition | Revolving door + glass reflection mask | Revolving glass doors reflect the exterior scene (environment cubemap capture). Through the glass, a low-fidelity lobby hint is visible (flat image). Entry is blocked by a "Private Event" sign in v0. In future versions, the interior inflates when the player pushes through the door. |
| **S08** | Service entrance on 44th St | Backstage access | Steel door + "Staff Only" signage | A heavy steel door with no exterior handle. "Staff Only -- Alarm Will Sound" decal. The door has no interaction prompt in normal gameplay. Mission scripts can unlock it, triggering backstage inflation behind the door. |
| **S09** | AMC Empire upper levels | Vertical transition | Elevator doors (non-functional in v0) | Elevator doors on the ground floor are visible but display an "Out of Order" sign. The call button produces no response. In future versions, the elevator is a vertical load-zone transition to upper-floor content. |
| **S10** | Portal spawn zone (44th St near alley) | Portal shimmer | Anomaly distortion effect | A shimmer/distortion post-processing effect marks the portal location. The visual distortion naturally obscures any loading artifacts behind it. The anomaly effect is diegetic -- it is a recognized in-world phenomenon in Twin Earth's fiction. |

---

## 4. Seam Policy

### 4.1 Mandatory Requirements

Every seam in the slice must satisfy all of the following requirements:

1. **Diegetic Mask (Required):** At least one in-world object, effect, or environmental feature must justify the boundary. The player should never encounter an unexplained invisible wall or void. The mask must be visually plausible from any angle the player can reach.

2. **Failure Behavior (Required):** If the primary mask fails (e.g., mask geometry fails to load, player clips through barrier), a fallback "area under construction" barrier must appear. This is a hard-coded emergency asset that is always resident in memory -- a simple orange-and-white striped barrier with a generic "Area Closed" sign. **There must never be an invisible wall without visual justification.**

3. **Streaming Pre-load (Required):** The cell or content behind a seam must begin loading when the player enters the **verification zone** -- defined as the area within 5 seconds of travel time from the seam boundary. At walk speed (1.4 m/s), this is approximately 7 m. At sprint speed (7 m/s), this is 35 m. The streaming system uses the larger of these two values (35 m) as the pre-load trigger distance to ensure content is ready even if the player sprints.

4. **Bidirectional Consistency:** Seams must work in both directions. If the player approaches from the backstage side (e.g., after a mission teleport), the Show Street side must be loaded before the seam is traversable.

### 4.2 Seam Interaction Matrix

| Seam Type | Player Can See Through? | Player Can Pass Through? | Content Behind Loads When? |
|-----------|------------------------|--------------------------|---------------------------|
| Edge of world (S01--S04) | No (opaque barriers) | No (collision blocks) | N/A (void beyond -- nothing to load) |
| Backstage corridor (S05, S08) | Partially (dim view through gaps) | No by default; yes during missions | On mission activation or when player is within 35 m and mission is active |
| Underground transition (S06) | Partially (stairs visible) | No in v0; yes when subway implemented | When player steps onto stairs (immediate trigger) |
| Interior transition (S07, S09) | Partially (glass reflection, lobby hint) | No in v0; yes in future versions | When player interacts with door (future) |
| Portal zone (S10) | No (distortion effect obscures) | Yes (portal is traversable when active) | When portal activation event fires (pre-streams during anomaly buildup) |

### 4.3 Emergency Seam Protocol

If the streaming system cannot load content behind a seam within the allotted time (player reaches seam before content is ready):

1. **Phase 1 (Stall):** Slow the player's movement speed by 30% when within 3 m of an unready seam (subtle, feels like difficult terrain).
2. **Phase 2 (Block):** If content is still not ready when the player reaches the seam, the diegetic mask blocks progress (door stays locked, barrier stays solid).
3. **Phase 3 (Fallback):** If the mask itself has failed, deploy the emergency "Area Closed" barrier.
4. **Logging:** All seam failures are logged with timestamp, player position, seam ID, and load state for debugging.

---

## 5. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1.0 | 2026-01-27 | Design Team | Initial draft -- zone classification, 10 seam definitions, seam policy |

---

*End of Backstage Map v0*
