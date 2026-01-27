# Translation Gate Rules v0

> **Twin Earth NYC** -- Part 11: Multiverse Gameplay
> **Document:** Translation Gate Rules
> **Version:** 0.1.0
> **Status:** Draft
> **Last Updated:** 2026-01-27

---

## Table of Contents

1. [Overview](#overview)
2. [What Can Cross](#what-can-cross)
3. [Compatibility Score](#compatibility-score)
4. [Consequences of Low Compatibility](#consequences-of-low-compatibility)
5. [Import Examples](#import-examples)
6. [Soft Limits](#soft-limits)
7. [Hard Limits](#hard-limits)
8. [Integration Notes](#integration-notes)

---

## Overview

The **Translation Gate** is the rule system governing what can and cannot pass through a portal between universes. It is not a physical object -- it is a set of physics constraints enforced by the portal itself and by the destination universe's reality.

Every item, entity, and piece of information that crosses a portal is evaluated by the Translation Gate. The gate assigns a **compatibility score** (0.0 -- 1.0) that determines how well the item functions in the destination universe and how much evidence its presence generates.

### Design Intent

The Translation Gate serves three game design purposes:

1. **Balance control** -- prevents the player from importing all-powerful artifacts and trivializing EARTH-1218 gameplay. Exotic items degrade, malfunction, and draw attention.
2. **Evidence generation** -- every import is a ticking clock. Incompatible items generate Heat over time, forcing the player to manage their exotic inventory actively.
3. **Strategic decisions** -- the player must weigh the utility of an imported item against its decay rate, evidence footprint, and maintenance cost. Not everything worth taking is worth keeping.

---

## What Can Cross

All items, entities, and information are classified into one of seven categories. Each category has a default crossing status, decay behavior, detection signature, and representative examples.

### Crossing Rules by Category

| Category | Status | Decay Rule | Detection Signature | Examples |
|---|---|---|---|---|
| **Mundane Objects** | Allowed | None -- fully stable in any universe | Low (trace signature at translation, fades within minutes) | Clothing, hand tools, food, water, paper, basic furniture, raw natural materials |
| **Advanced Technology** | Restricted | Functionality degrades; half-life of 24h in foreign universe. At each half-life, device effectiveness drops by 50%. | Medium (detectable by IoT sensors within 30m, unusual EM emissions) | Weapons (ranged), computers, vehicles, communication devices, medical tech, powered armor |
| **Exotic Materials** | Restricted | Physical instability -- vibration, spontaneous heat generation, phase shifts (flicker between solid/translucent). Half-life varies by material (6-48h). | High (detectable by IoT sensors within 100m, visible anomalous behavior to naked eye) | Vibranium, Uru metal, alien biological samples, enchanted items, portal residue crystals |
| **Energy Constructs** | Forbidden (hard cap) | Instant dissipation outside native universe. No exceptions. Energy constructs cannot exist in a universe with different energy conservation rules. | Maximum (massive energy signature at point of dissipation, detectable city-wide) | Magic spells (active), force fields, energy weapons (beam/projection type), psychic constructs, hard-light holograms |
| **Living Beings** | Allowed | Physiological stress: nausea, disorientation, sensory distortion. 30-second adjustment period upon arrival. No permanent damage to baseline organisms. | Medium (biological signature detectable by medical/bio sensors within 10m, fades after adjustment period) | NPCs (human and non-human), player character, animals, insects, microorganisms |
| **Information** | Allowed | None -- memories, knowledge, and recorded data persist perfectly across universes. | No signature (information has no physical presence to detect) | Memories, spoken knowledge, photographs, video recordings, written documents, digital data files |
| **Large Masses** | Hard capped | N/A -- cannot transit | N/A -- transit rejected | Any single object or combined load exceeding 500kg per portal traversal event |

### Category Boundary Cases

| Edge Case | Ruling | Rationale |
|---|---|---|
| Powered-down technology (no active electronics) | Treated as **Mundane Object** if no exotic components | A dead phone is just plastic and glass |
| Kinetic weapons (swords, bows, bullets) | Treated as **Mundane Object** (no power source) | Exception: if made from exotic materials, classified as **Exotic Materials** |
| Living beings carrying exotic items | Being: **Allowed**; items evaluated separately per category | Each item in inventory is individually assessed |
| Photographs of exotic events | **Information** (allowed, no decay) | The image is data, not matter |
| Biological samples (dead tissue) | **Exotic Materials** if from alien biology; **Mundane** if from Earth-equivalent | Non-native biology triggers exotic classification |
| AI / digital consciousness | **Information** (allowed) if purely data; **Energy Construct** (forbidden) if requiring active energy substrate | Software survives; energy-dependent hardware does not |
| Portal residue (collected from sealed portals) | **Exotic Materials** | Portal residue is dimensionally charged matter |

---

## Compatibility Score

Every item that crosses a portal receives a **compatibility score** ranging from 0.0 (completely incompatible) to 1.0 (fully compatible). This score determines the item's behavior in the destination universe.

### Score Formula

```
compatibility = base_compatibility x physics_match x material_match x energy_match
```

**Factor definitions:**

| Factor | Range | Calculation | Examples |
|---|---|---|---|
| `base_compatibility` | 0.0 -- 1.0 | Determined by item category (see table below) | Mundane: 1.0, Advanced Tech: 0.8, Exotic: 0.5, Energy: 0.0 |
| `physics_match` | 0.5 -- 1.0 | How similar the source and destination universe physics are. Calculated from gravity differential, energy conservation mode match, and special physics rule overlap. | 1218 to 616: 0.85, 1218 to alien: 0.6 |
| `material_match` | 0.5 -- 1.0 | Whether the item's constituent materials exist in the destination universe and behave the same way. | Steel in 1218: 1.0, Vibranium in 1218: 0.6, Alien bio-metal in 1218: 0.5 |
| `energy_match` | 0.0 -- 1.0 | Whether the item's energy source/mechanism is compatible with destination physics. 0.0 for pure energy constructs in strict-conservation universes. | Battery-powered in 1218: 0.9, Magic-powered in 1218: 0.3, Energy construct in 1218: 0.0 |

### Base Compatibility by Category

| Category | Base Compatibility | Notes |
|---|---|---|
| Mundane Objects | 1.0 | Always fully compatible at base level |
| Advanced Technology | 0.8 | Reduced by energy source incompatibility |
| Exotic Materials | 0.5 | Inherently unstable outside native universe |
| Energy Constructs | 0.0 | Hard-capped at zero (instant dissipation) |
| Living Beings | 0.9 | Minor physiological adjustment needed |
| Information | 1.0 | Perfect compatibility (no physical component) |

### Compatibility Score Ranges

| Score Range | Classification | Summary |
|---|---|---|
| **1.0** | Fully Compatible | Item functions identically to native equivalent. No decay, no evidence, no maintenance. Mundane objects in similar universes. |
| **0.7 -- 0.99** | Minor Issues | Item functions well but with small imperfections. Slight performance degradation, minor visual glitches (subtle glow, occasional flicker). Evidence generation is trace-level. |
| **0.3 -- 0.69** | Significant Issues | Item functions partially but with major imperfections. Periodic malfunction, visible instability (vibration, heat, phase shifting). Generates detectable evidence continuously. Requires maintenance. |
| **0.0 -- 0.29** | Critical Incompatibility | Item barely functions or fails entirely. Rapid degradation, dangerous side effects (radiation, reality distortion, spontaneous energy release). Generates obvious evidence. Containment recommended or required. |

---

## Consequences of Low Compatibility

The compatibility score directly determines four gameplay consequences: item performance, visual/audio effects, evidence generation, and Heat impact.

### Consequence Table

| Compatibility | Item Effect | Visual/Audio | Evidence Generated | Heat Impact |
|---|---|---|---|---|
| **0.7 -- 0.99** | Minor visual glitch on item model (subtle shimmer); slight performance loss (e.g., weapon damage -5%, device speed -10%) | Faint glow visible only in dark conditions; barely audible hum at <1m distance | Trace signature: detectable only by specialized sensors at close range (<5m) | +0.01 per hour to Ecological Heat (negligible) |
| **0.3 -- 0.69** | Visible instability (item vibrates, flickers, runs hot); periodic malfunction (random failure 10% per use); signature spikes during use | Visible glow/distortion noticeable in normal lighting; audible hum/crackle within 10m; periodic energy flashes | Detectable by standard IoT sensors within 30m; CCTV can capture anomalous visual; NPCs may notice and comment | +0.05 per hour to Ecological Heat; +0.02 per use to Institutional Heat (sensor logs) |
| **0.0 -- 0.29** | Rapid degradation (effectiveness drops 25% per hour); dangerous side effects (heat burns at touch, gravity distortion within 2m, reality flicker within 5m); containment device required for safe storage | Obvious glow/distortion visible to anyone within 20m; loud crackling/humming; environmental effects (lights flicker, electronics glitch nearby) | Obvious to any witness within visual range; all sensor types trigger; automatic evidence logging across all channels | +0.2 immediately to Ecological Heat on import; +0.1 per hour ongoing; +0.05 per hour to Physical Heat (environmental damage) |

### Degradation Timeline

For items in the 0.3 -- 0.69 range, degradation follows a predictable curve:

```
Effectiveness over time (compatibility 0.5 example):

100% |****
 90% |    ***
 80% |       ***
 70% |          **
 60% |            **
 50% |              **        <- half-life point (24h)
 40% |                **
 30% |                  ***
 20% |                     ***
 10% |                        ****
  0% |________________________________
     0h   6h  12h  18h  24h  30h  36h  42h  48h

     Half-life = 24h (standard for Advanced Technology)
     At half-life, item is at 50% original effectiveness
     At 2x half-life (48h), item is at 25% effectiveness
     Items below 10% effectiveness are classified "inert" (useless)
```

---

## Import Examples

Ten representative imports demonstrating the Translation Gate system in action. All examples assume destination universe is EARTH-1218 (hub, strict energy conservation, standard physics).

### Import Examples Table

| # | Item | Origin Universe | Compatibility in 1218 | Degradation Behavior | Evidence Profile |
|---|---|---|---|---|---|
| **1** | **Vibranium Shard** (raw, fist-sized) | Earth-616 | **0.4** | Vibrates at audible frequency; emits heat (warm to touch, hot after 6h); becomes physically unstable after 6h (micro-fractures); usable for crafting/stabilization within first 6h window | High EM signature detectable by sensors within 80m; faint visible glow (CCTV-detectable at night); heat signature on thermal cameras |
| **2** | **Stark-tech Gauntlet** (repulsor-class) | Earth-199999 | **0.6** | Power cells drain at 3x normal rate (operational for ~8h instead of 24h); targeting system drifts (+15% accuracy penalty, worsening over time); repulsor output at 70% and declining | Medium tech signature (unusual EM emissions within 30m); power drain detectable by electrical sensors; occasional visible energy flicker when fired |
| **3** | **Sling Ring** (mystic focus) | Earth-616 (Strange's Sanctum) | **0.3** | Only functions within 10m of active portal residue (useless elsewhere in 1218); each use drains the user (10% HP fatigue); portal created is micro-scale (person-sized, 30s duration, unstable) | High mystical signature when activated (detectable by Strange's network immediately); visible portal effects (witnesses); residue generation at use site |
| **4** | **Alien Plant Sample** (bio-specimen) | Unknown pocket | **0.5** | Wilts in Earth atmosphere over 12h; emits foreign spores during decay (bio-hazard, containment required); useful for analysis/crafting within 12h window if contained | Bio-hazard signature (detectable by environmental sensors); witness reports if spores are visible; CCTV-detectable containment failure |
| **5** | **Wakandan Kimoyo Beads** (comm/med device) | Earth-616 | **0.7** | Communication functions work reliably; holographic display flickers (30% display accuracy loss); medical scanning functions degrade over 48h; vibranium-laced shell is stable | Low-medium tech signature (unusual wireless frequencies within 15m); hologram flicker visible to nearby observers; mostly concealable with care |
| **6** | **Cosmic Cube Fragment** (reality-warping) | Earth-616 | **0.1** | Extremely unstable -- reality distortion within 5m radius (gravity fluctuations, visual tears, temperature spikes); effectiveness unpredictable (may grant enormous power briefly or backfire catastrophically); degrades to inert within 2h | Maximum signature across all sensor types; detectable city-wide when active; immediate Heat crisis across all four channels; witnesses experience disorientation and trauma |
| **7** | **Foreign Currency / Data Chips** (monetary) | Various | **0.9** | Works fine as physical objects; minor encoding differences in digital data (recoverable with standard decryption); currency has no value in 1218 economy (collector's item only) | Negligible signature; forensic analysis could identify foreign manufacture but requires deliberate investigation; no passive detection |
| **8** | **Symbiote Sample** (alien organism, contained) | Earth-616 | **0.2** | Aggressively unstable -- containment critical; sample attempts to bond with nearby organic matter; outside containment, full symbiote emergence within minutes; inside containment, slow degradation over 6h | Bio + anomaly signature (dual-channel detection); containment device itself generates medium tech signature; breach event generates maximum biological and ecological evidence |
| **9** | **Off-world Kinetic Weapon** (rifle-class) | Pocket universe | **0.8** | Weapon frame and mechanism function normally (kinetic, no exotic energy); ammunition is incompatible (different caliber, different propellant chemistry); usable as melee weapon or with improvised ammunition at reduced effectiveness | Low-medium signature (unusual material composition detectable at close range); functionally a strange-looking gun -- not immediately suspicious to casual observers |
| **10** | **Portal Stabilizer Device** (tech artifact) | Earth-838 | **0.6** | Functions effectively within 20m of active portal or fresh residue; degrades rapidly when moved away from portal energy (effectiveness halves per 50m distance); excellent for field stabilization work but cannot be used as a general-purpose device | Medium tech signature concentrated near portal sites; generates localized EM field detectable by sensors within 40m; effectiveness variation is itself a detectable pattern |

### Import Decision Framework

When deciding whether to import an item, the player should evaluate:

```
IMPORT DECISION MATRIX:

Is the item worth importing?
  |
  +-- Compatibility > 0.7?
  |     YES: Low risk. Import freely. Minimal maintenance.
  |     NO:  Continue evaluation.
  |
  +-- Compatibility 0.3-0.69?
  |     Is the utility worth the Heat cost?
  |       YES: Import with containment plan. Budget maintenance time.
  |       NO:  Leave it. Use the intel (Information) instead.
  |
  +-- Compatibility < 0.3?
        Is this a critical mission item?
          YES: Import with extreme caution. Have containment ready.
               Plan to use immediately and dispose/seal.
          NO:  Do not import. Risk far exceeds utility.
```

---

## Soft Limits

Soft limits are constraints that the player can work around with effort, resources, and risk. They make exotic imports costly and temporary, not impossible.

### Soft Limit 1: Decay

**Rule:** All exotic imports have a half-life. Item effectiveness halves over each half-life period.

| Category | Standard Half-Life | Modifiers |
|---|---|---|
| Advanced Technology | 24h sim-time | Extended to 36h if maintained with portal residue |
| Exotic Materials | 6 -- 48h sim-time (varies by material) | Extended by 50% if stored in containment device |
| Living Beings | N/A (adjustment period only, no decay) | Stress increases if being is from very different universe |

**Workarounds:**
- **Portal residue recharging:** Exposing decaying items to active portal residue resets their decay clock by 50%. Costs residue (finite resource) and generates Ecological Heat (+0.02 per recharge).
- **Containment storage:** Specialized containers slow decay by 50% (half-life is doubled). Containers are craftable but require exotic components.
- **Artifact synergy:** Some artifacts decay slower when stored together (specific combinations, discoverable through experimentation).

### Soft Limit 2: Traceability

**Rule:** All imports leave signature traces detectable by the IoT sensor network in EARTH-1218.

| Compatibility Range | Detection Range | Detection Method | Fade Time |
|---|---|---|---|
| 0.7 -- 0.99 | 5m (close range only) | Specialized sensors only | Signature fades in 1h after item removal |
| 0.3 -- 0.69 | 30m (standard sensor range) | IoT network, CCTV (if visual effects), NPC observation | Signature fades in 6h after item removal |
| 0.0 -- 0.29 | 100m+ (wide area) | All sensor types, naked eye, automatic alerts | Signature fades in 24h after item removal or containment |

**Workarounds:**
- **Shielded containers:** Block 80% of signature emission. Reduces detection range by 80%. Craftable, requires rare components.
- **Movement:** Keep moving. Stationary exotic items build up detectable signature fields. Moving items disperse the trail.
- **Timing:** Operate during high-noise periods (Times Square peak hours, special events) when sensor noise floors are elevated.

### Soft Limit 3: Maintenance Cost

**Rule:** Keeping exotic items functional requires active maintenance -- either portal residue exposure or periodic recharging via proximity to active portals.

| Maintenance Method | Cost | Frequency | Effectiveness |
|---|---|---|---|
| Portal residue application | 1 unit residue per maintenance cycle | Every 12h sim-time | Resets decay clock by 50% |
| Active portal proximity | None (passive) | Continuous while within 20m of STABLE portal | Pauses decay entirely while in range |
| Containment device storage | Power cell (consumed over 48h) | Continuous | Slows decay by 50% |

**Economic impact:** Maintenance creates ongoing resource pressure. The player must balance:
- Residue supply (limited, collected from sealed portals)
- Portal availability (maintaining an open portal for proximity charging has its own Heat costs)
- Power cells (consumed by containment devices, needed for other tech)

---

## Hard Limits

Hard limits are absolute constraints that cannot be worked around. They are physics-level restrictions enforced by the portal and the destination universe.

### Hard Limit 1: Mass Cap

**Rule:** No single portal traversal event can transport more than **500kg** of total mass.

| Specification | Value |
|---|---|
| Maximum mass per traversal | 500 kg |
| Enforcement mechanism | Portal bandwidth property (portal physically cannot transmit more) |
| Failure mode | Excess mass is rejected -- bounced back with force, causing portal stability loss (-0.05) |
| Workaround | None. Multiple traversals can move more total mass, but each is limited to 500kg. Each traversal consumes portal stability and generates evidence. |
| Design rationale | Prevents importing vehicles, large structures, or military hardware in a single trip. Forces the player to prioritize what they bring through. |

**Mass budget examples:**

| Payload | Approximate Mass | Remaining Budget |
|---|---|---|
| Player (with gear) | 100 kg | 400 kg |
| Player + companion NPC | 200 kg | 300 kg |
| Player + heavy equipment loadout | 150 kg | 350 kg |
| Player + small vehicle (motorcycle, disassembled) | 350 kg | 150 kg |
| Player + large artifact (statue, machinery) | 300-500 kg | 0-200 kg |

### Hard Limit 2: Energy Cap

**Rule:** No active energy construct survives translation between universes. Energy constructs dissipate **instantly** upon crossing the Translation Gate.

| Specification | Value |
|---|---|
| Affected items | Magic spells (active castings), force fields, energy weapons (beam/projection type), psychic constructs, hard-light holograms, any manifestation that is pure energy |
| Enforcement mechanism | Destination universe physics instantly decohere foreign energy patterns |
| Failure mode | Instant dissipation with massive energy release at the portal exit point |
| Energy release | Equivalent to the construct's stored energy, released as heat + light + kinetic force. Physical Heat spike proportional to construct power. |
| Workaround | None. This is absolute. A magic shield cast in Universe-616 ceases to exist the instant it crosses into 1218. The caster can re-cast using local energy (if their method works in 1218 -- see Sling Ring example). |
| Design rationale | Prevents energy-based superpowers from being imported wholesale. The player cannot bring a force field from a magic universe and use it as permanent protection in 1218. This maintains 1218's grounded, realistic tone. |

**What counts as an "energy construct":**

| Energy Construct (Forbidden) | NOT Energy Construct (Allowed) |
|---|---|
| Active magic spell (fireball, shield, telekinesis) | Magic-infused physical object (enchanted sword -- Exotic Material) |
| Force field (any type) | Powered armor (technology -- the armor is physical, the power source degrades) |
| Energy beam weapon (repulsor beam, magic bolt) | Kinetic weapon (gun, bow -- projectile is physical) |
| Psychic manifestation (telekinetic construct) | Psychic ability (the mind itself crosses -- the ability may not function in 1218) |
| Hard-light hologram | Recorded hologram data (Information -- the data crosses, the projection must be re-created) |

---

## Integration Notes

### System Dependencies

| System | Integration Point | Data Flow |
|---|---|---|
| **Portal State Machine** | Gate checks portal state before allowing transit | Gate reads: bandwidth, stability, state. Rejects transit if state != STABLE or stability < 0.3 |
| **Universe Profile** | Compatibility formula uses physics/material/energy profiles | Gate reads: source and destination universe profiles to calculate `physics_match`, `material_match`, `energy_match` |
| **Heat System** | Imported items generate ongoing Heat based on compatibility | Gate writes: Heat impacts per imported item (see Consequences table) |
| **Evidence Economy** | Imported items generate evidence entries | Gate writes: evidence class entries (physical, digital, witness) per import event and ongoing |
| **Inventory System** | Items gain compatibility metadata on import | Gate writes: `compatibility_score`, `decay_clock`, `maintenance_schedule` to item entity |
| **Faction AI** | Factions detect and respond to imported items | Gate fires: `translation.item_imported` event consumed by faction response system |

### Event Bus Integration

Translation events fire the following event:

```json
{
  "event_type": "translation.item_imported",
  "item_id": "unique_item_entity_id",
  "item_category": "exotic_material",
  "item_name": "Vibranium Shard",
  "source_universe": "EARTH-616",
  "destination_universe": "EARTH-1218",
  "compatibility_score": 0.4,
  "portal_id": "portal_entity_id",
  "portal_signature": "64char_hex_hash",
  "decay_half_life_hours": 12,
  "detection_range_meters": 80,
  "heat_impact_immediate": {
    "physical": 0.0,
    "social": 0.0,
    "institutional": 0.02,
    "ecological": 0.05
  },
  "heat_impact_per_hour": {
    "ecological": 0.05
  },
  "timestamp": "sim_time_iso8601"
}
```

### Cross-Reference Documents

| Document | Relationship |
|---|---|
| `universe-profile-template-v0.md` | Source and destination profiles provide compatibility formula inputs |
| `portal-state-machine-v0.md` | Gate checks portal state/bandwidth before transit; excess mass degrades stability |
| `operations-library-v0.md` | Operations specify expected imports and their compatibility ratings |
| `heat-evidence-economy-spec-v0.md` | Import evidence feeds into Heat channels and evidence economy |
| `faction-response-table-v0.md` | Faction responses to detected imports (NYPD investigation, Criminal interest, etc.) |

---

*End of Translation Gate Rules v0*
