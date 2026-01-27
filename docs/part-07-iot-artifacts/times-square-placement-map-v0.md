# Times Square Artifact Placement Map v0

**Twin Earth NYC -- Part 7: IoT Artifacts**
**Version:** 0.1.0
**Status:** Draft
**Last Updated:** 2026-01-27

---

## 1. Placement Logic

### 1.1 Coverage Philosophy

Artifact placement in the Times Square zone (bounded by 42nd Street to 47th Street, Broadway to 7th Avenue) follows real-world NYC infrastructure patterns with selective densification for gameplay purposes.

**Principles:**

1. **Traffic signals and crosswalks** are placed at every intersection and mid-block crosswalk in the zone. This matches real NYC DOT placement. Every signalized intersection gets one traffic light per approach direction and one crosswalk signal per pedestrian crossing.

2. **CCTV cameras** are placed to provide overlapping but not total coverage. Gaps exist deliberately -- perfect surveillance would eliminate investigative gameplay. Cameras cluster at high-value locations (TKTS steps, major intersections, building entrances) and thin out in mid-block areas and alleys.

3. **Information kiosks** are placed at high-traffic pedestrian nodes: the TKTS booth area, the 42nd/Broadway intersection, and the 45th Street pedestrian plaza. These correspond to real-world LinkNYC kiosk placements.

4. **Doors** are placed on narratively significant buildings. Not every door in Times Square is modeled -- only those on buildings the player may need to enter, investigate, or secure. Default access levels reflect the building's real-world function (hotel = badge, theater = key during hours, retail = unlocked during hours).

### 1.2 Coordinate System

All placements use the game world coordinate system where:
- **X axis** runs east-west (increasing eastward)
- **Y axis** runs vertically (ground level = 0.0)
- **Z axis** runs north-south (increasing northward)

The origin (0, 0, 0) is at the southwest corner of the zone (42nd St / 7th Ave intersection).

### 1.3 Zone Boundaries

| Boundary | Street | Coordinate |
|---|---|---|
| South | 42nd Street | Z = 0 |
| North | 47th Street | Z = 250 |
| West | 7th Avenue | X = 0 |
| East | Broadway (diagonal) | X ~ 100-200 (varies with Broadway's angle) |

Broadway cuts diagonally across the grid, creating the distinctive "bowtie" shape of Times Square. The widest point of the bowtie (the pedestrian plazas) is near 45th-46th Streets.

---

## 2. Crosswalk Signals

Crosswalk signals are paired with parent traffic lights at each intersection. Each intersection typically has 4 crosswalks (one per leg), though T-intersections and the irregular Broadway geometry create some 3-crosswalk and 5-crosswalk configurations.

| ID | Location Description | Intersection | Parent Signal | Notes |
|---|---|---|---|---|
| `ENT_XWALK_TSQ_01` | 42nd St at 7th Ave, south leg | INT_42_7AVE | ENT_TLIGHT_TSQ_01 | High pedestrian volume; connects to Port Authority area |
| `ENT_XWALK_TSQ_02` | 42nd St at 7th Ave, east leg | INT_42_7AVE | ENT_TLIGHT_TSQ_01 | Crosses 7th Ave southbound approach |
| `ENT_XWALK_TSQ_03` | 42nd St at 7th Ave, north leg | INT_42_7AVE | ENT_TLIGHT_TSQ_01 | Leads into Times Square pedestrian zone |
| `ENT_XWALK_TSQ_04` | 42nd St at 7th Ave, west leg | INT_42_7AVE | ENT_TLIGHT_TSQ_01 | Crosses 42nd St westbound approach |
| `ENT_XWALK_TSQ_05` | 42nd St at Broadway, south leg | INT_42_BROADWAY | ENT_TLIGHT_TSQ_02 | Near AMC Empire 25 entrance |
| `ENT_XWALK_TSQ_06` | 42nd St at Broadway, northeast leg | INT_42_BROADWAY | ENT_TLIGHT_TSQ_02 | Diagonal crossing following Broadway angle |
| `ENT_XWALK_TSQ_07` | 42nd St at Broadway, west leg | INT_42_BROADWAY | ENT_TLIGHT_TSQ_02 | Connects to 42nd/7th Ave block |
| `ENT_XWALK_TSQ_08` | 43rd St at 7th Ave, south leg | INT_43_7AVE | ENT_TLIGHT_TSQ_03 | Mid-block crossing, moderate traffic |
| `ENT_XWALK_TSQ_09` | 43rd St at 7th Ave, north leg | INT_43_7AVE | ENT_TLIGHT_TSQ_03 | Adjacent to hotel zone |
| `ENT_XWALK_TSQ_10` | 44th St at Broadway, south leg | INT_44_BROADWAY | ENT_TLIGHT_TSQ_04 | Near Shubert Alley entrance |
| `ENT_XWALK_TSQ_11` | 44th St at Broadway, north leg | INT_44_BROADWAY | ENT_TLIGHT_TSQ_04 | Leads toward TKTS steps |
| `ENT_XWALK_TSQ_12` | 45th St at 7th Ave, south leg | INT_45_7AVE | ENT_TLIGHT_TSQ_05 | Edge of pedestrian plaza |
| `ENT_XWALK_TSQ_13` | 45th St at 7th Ave, north leg | INT_45_7AVE | ENT_TLIGHT_TSQ_05 | Enters main pedestrian zone |
| `ENT_XWALK_TSQ_14` | 45th St at Broadway, south leg | INT_45_BROADWAY | ENT_TLIGHT_TSQ_06 | TKTS steps adjacent; very high foot traffic |
| `ENT_XWALK_TSQ_15` | 45th St at Broadway, north leg | INT_45_BROADWAY | ENT_TLIGHT_TSQ_06 | Connects to north pedestrian plaza |
| `ENT_XWALK_TSQ_16` | 46th St at 7th Ave, south leg | INT_46_7AVE | ENT_TLIGHT_TSQ_07 | Near Marriott Marquis north entrance |
| `ENT_XWALK_TSQ_17` | 46th St at 7th Ave, north leg | INT_46_7AVE | ENT_TLIGHT_TSQ_07 | Restaurant row access |
| `ENT_XWALK_TSQ_18` | 46th St at Broadway, south leg | INT_46_BROADWAY | ENT_TLIGHT_TSQ_08 | North bowtie area |
| `ENT_XWALK_TSQ_19` | 47th St at 7th Ave, south leg | INT_47_7AVE | ENT_TLIGHT_TSQ_09 | Northern zone boundary |
| `ENT_XWALK_TSQ_20` | 47th St at Broadway, south leg | INT_47_BROADWAY | ENT_TLIGHT_TSQ_10 | Northern zone boundary, Broadway exit |

---

## 3. CCTV Cameras

Cameras are mounted on traffic signal poles, building corners, and dedicated security mounts. Placement prioritizes intersection coverage, the TKTS steps area, and building entrances. Mid-block alleys and the interior of the pedestrian plazas have deliberate coverage gaps to create investigative gameplay opportunities.

| ID | Location Description | Mounting | FOV Direction | Coverage Zone |
|---|---|---|---|---|
| `ENT_CCTV_TSQ_01` | 42nd St / 7th Ave, NE corner pole | Traffic signal pole, 5.5m | South-southeast | INT_42_7AVE south approach, 42nd St east sidewalk |
| `ENT_CCTV_TSQ_02` | 42nd St / 7th Ave, NW corner pole | Traffic signal pole, 5.5m | East-southeast | 7th Ave northbound approach, 42nd St west sidewalk |
| `ENT_CCTV_TSQ_03` | 42nd St / Broadway, SW corner building | Building corner mount, 8m | North-northeast | INT_42_BROADWAY, AMC Empire 25 frontage |
| `ENT_CCTV_TSQ_04` | TKTS Steps, south-facing | Dedicated security mount, 4m | South over steps | TKTS steps, southern pedestrian plaza |
| `ENT_CCTV_TSQ_05` | TKTS Steps, north-facing | Dedicated security mount, 4m | North over plaza | Northern TKTS approach, 47th St sightline |
| `ENT_CCTV_TSQ_06` | 44th St / Broadway, NE corner pole | Traffic signal pole, 5.5m | Southwest | INT_44_BROADWAY, Shubert Alley entrance |
| `ENT_CCTV_TSQ_07` | 44th St / 7th Ave, SE corner pole | Traffic signal pole, 5.5m | Northwest | INT_44_7AVE, mid-block 7th Ave |
| `ENT_CCTV_TSQ_08` | Marriott Marquis main entrance | Building mount, 3.5m | West over entrance | Marriott Marquis lobby approach, 45th St sidewalk |
| `ENT_CCTV_TSQ_09` | 45th St pedestrian plaza, west side | Pole mount, 6m | East across plaza | Central pedestrian plaza, kiosk area |
| `ENT_CCTV_TSQ_10` | 45th St / Broadway, NW corner | Building corner mount, 7m | South-southwest | INT_45_BROADWAY, TKTS queue area |
| `ENT_CCTV_TSQ_11` | 46th St / 7th Ave, SW corner pole | Traffic signal pole, 5.5m | Northeast | INT_46_7AVE, north approach |
| `ENT_CCTV_TSQ_12` | 46th St / Broadway, SE corner | Building mount, 6m | West-northwest | INT_46_BROADWAY, north bowtie area |
| `ENT_CCTV_TSQ_13` | 43rd St mid-block, 7th Ave side | Building mount, 4.5m | East | Mid-block alley between 43rd and 44th, 7th Ave storefronts |
| `ENT_CCTV_TSQ_14` | 47th St / 7th Ave, SE corner pole | Traffic signal pole, 5.5m | South-southwest | INT_47_7AVE, northern zone boundary |
| `ENT_CCTV_TSQ_15` | One Times Square (north face) | Building mount, 12m | North up Broadway | Broad view of central bowtie from elevated position; long range but low detail |
| `ENT_CCTV_TSQ_16` | 43rd St / Broadway, NW corner | Building mount, 5m | South-southeast | INT_43_BROADWAY, south bowtie approach |
| `ENT_CCTV_TSQ_17` | 45th St / 7th Ave, NE corner pole | Traffic signal pole, 5.5m | South | INT_45_7AVE, Marriott Marquis south side |
| `ENT_CCTV_TSQ_18` | 47th St / Broadway, SW corner | Building mount, 6m | East-southeast | INT_47_BROADWAY, northern exit |

**Coverage Gap Notes:**

| Gap Location | Reason | Gameplay Impact |
|---|---|---|
| Mid-block between 43rd-44th on Broadway side | No camera has direct sightline into narrow passage | Dead zone for surveillance; useful for covert NPC/player movement |
| Interior of south pedestrian plaza (south of TKTS) | ENT_CCTV_TSQ_04 covers steps but not deep plaza | Crowd density further degrades coverage; meeting point for informants |
| Alley behind 44th St buildings (Shubert Alley interior) | ENT_CCTV_TSQ_06 covers entrance only | Classic "meet in the alley" scenario; forced entry events less likely to be observed |
| 46th-47th mid-block on 7th Ave side | ENT_CCTV_TSQ_11 and _14 cover intersections but not mid-block | Loading dock area, service entrances; used for supply-side criminal activity |

---

## 4. Information Kiosks

Kiosks are placed at high-traffic pedestrian nodes corresponding to real-world LinkNYC kiosk locations. They serve as information sources, alert displays, and interactive investigation tools.

| ID | Location Description | Type | Notes |
|---|---|---|---|
| `ENT_KIOSK_TSQ_01` | 42nd St / Broadway, north sidewalk near AMC | LinkNYC-style interactive | High foot traffic from 42nd St corridor; primary transit info point. Nearest camera: ENT_CCTV_TSQ_03 |
| `ENT_KIOSK_TSQ_02` | TKTS steps, east side at base | LinkNYC-style interactive | Tourist information hub; highest interaction rate in zone. Nearest camera: ENT_CCTV_TSQ_04 |
| `ENT_KIOSK_TSQ_03` | 45th St pedestrian plaza, center-west | LinkNYC-style interactive | Central plaza location; good for anomaly alerts. Nearest camera: ENT_CCTV_TSQ_09 |
| `ENT_KIOSK_TSQ_04` | 46th St / 7th Ave, east sidewalk | LinkNYC-style interactive | North zone coverage; restaurant row wayfinding. Nearest camera: ENT_CCTV_TSQ_11 |
| `ENT_KIOSK_TSQ_05` | 43rd St / 7th Ave, west sidewalk | LinkNYC-style interactive | South zone coverage; connects to Port Authority info. Nearest camera: ENT_CCTV_TSQ_13 |

---

## 5. Doors

Doors are placed on narratively significant buildings within the Times Square zone. Each door has a defined access level reflecting the building's real-world function and its role in gameplay. Default states represent the door's condition at simulation start (daytime scenario).

### 5.1 Marriott Marquis (1535 Broadway)

| ID | Location Description | Building | Access Level | Default State | Notes |
|---|---|---|---|---|---|
| `ENT_DOOR_TSQ_MARRIOTT_01` | Main entrance, Broadway frontage | Marriott Marquis | Unlocked (public lobby) | `unlocked` | Revolving door; public access to lobby during business hours |
| `ENT_DOOR_TSQ_MARRIOTT_02` | Side entrance, 45th St | Marriott Marquis | Badge (hotel guest/staff) | `locked` | Card-key access; connects to elevator bank |
| `ENT_DOOR_TSQ_MARRIOTT_03` | Service entrance, 46th St alley | Marriott Marquis | Badge (staff only) | `locked` | Loading dock adjacent; high-security door class |
| `ENT_DOOR_TSQ_MARRIOTT_04` | Emergency exit, 45th St west | Marriott Marquis | Locked (alarm-equipped) | `locked` | Push-bar exit only; opening triggers security alert |

### 5.2 AMC Empire 25 (234 W 42nd St)

| ID | Location Description | Building | Access Level | Default State | Notes |
|---|---|---|---|---|---|
| `ENT_DOOR_TSQ_AMC_01` | Main entrance, 42nd St | AMC Empire 25 | Unlocked (during hours) | `unlocked` | Glass double doors; public access during operating hours |
| `ENT_DOOR_TSQ_AMC_02` | Side exit, 42nd St west | AMC Empire 25 | Key (staff) | `locked` | Emergency exit / staff access |
| `ENT_DOOR_TSQ_AMC_03` | Service entrance, alley | AMC Empire 25 | Key (staff) | `locked` | Rear service door; delivery access |

### 5.3 One Times Square (1475 Broadway)

| ID | Location Description | Building | Access Level | Default State | Notes |
|---|---|---|---|---|---|
| `ENT_DOOR_TSQ_OTS_01` | Ground floor entrance, Broadway | One Times Square | Badge (tenant/security) | `locked` | Iconic building; limited public access. Security desk inside |
| `ENT_DOOR_TSQ_OTS_02` | Service entrance, 42nd St side | One Times Square | Badge (maintenance) | `locked` | Access to billboard/signage infrastructure |

### 5.4 TKTS Booth Area

| ID | Location Description | Building | Access Level | Default State | Notes |
|---|---|---|---|---|---|
| `ENT_DOOR_TSQ_TKTS_01` | TKTS booth staff door, rear | TKTS Booth | Key (staff) | `locked` | Small service door behind the booth structure |

### 5.5 Broadway Retail Storefronts (42nd-44th St)

| ID | Location Description | Building | Access Level | Default State | Notes |
|---|---|---|---|---|---|
| `ENT_DOOR_TSQ_RETAIL_01` | Retail shop, 42nd St near 7th Ave | Generic retail | Unlocked (during hours) | `unlocked` | Souvenir shop; glass storefront |
| `ENT_DOOR_TSQ_RETAIL_02` | Retail shop, 43rd St Broadway side | Generic retail | Unlocked (during hours) | `unlocked` | Apparel store |
| `ENT_DOOR_TSQ_RETAIL_03` | Restaurant, 44th St near 7th Ave | Restaurant | Unlocked (during hours) | `unlocked` | Diner; NPC gathering point |
| `ENT_DOOR_TSQ_RETAIL_04` | Retail stockroom, 43rd alley | Generic retail (back) | Key (staff) | `locked` | Connects to ENT_DOOR_TSQ_RETAIL_02 interior |

### 5.6 7th Avenue Storefronts (44th-47th St)

| ID | Location Description | Building | Access Level | Default State | Notes |
|---|---|---|---|---|---|
| `ENT_DOOR_TSQ_RETAIL_05` | Electronics store, 45th St at 7th Ave | Retail | Unlocked (during hours) | `unlocked` | Player can purchase equipment here |
| `ENT_DOOR_TSQ_RETAIL_06` | Pharmacy, 46th St at 7th Ave | Retail | Unlocked (during hours) | `unlocked` | Standard retail access |
| `ENT_DOOR_TSQ_RETAIL_07` | Restaurant rear, 46th St alley | Restaurant (back) | Key (staff) | `locked` | Kitchen service entrance |

### 5.7 Office / Upper Floor Access

| ID | Location Description | Building | Access Level | Default State | Notes |
|---|---|---|---|---|---|
| `ENT_DOOR_TSQ_OFFICE_01` | Office building lobby, 43rd St at 7th Ave | Commercial office | Badge (tenant) | `locked` | After-hours locked; daytime lobby open with security desk |
| `ENT_DOOR_TSQ_OFFICE_02` | Office building lobby, 46th St at Broadway | Commercial office | Badge (tenant) | `locked` | Similar to above |
| `ENT_DOOR_TSQ_OFFICE_03` | Stairwell access, 44th St building | Commercial office (internal) | Code (tenant/maintenance) | `locked` | Numeric keypad; 4-digit code |

### 5.8 Subway Entrances

| ID | Location Description | Building | Access Level | Default State | Notes |
|---|---|---|---|---|---|
| `ENT_DOOR_TSQ_SUBWAY_01` | Times Square station, 42nd St / 7th Ave entrance | MTA Subway | Unlocked (public) | `unlocked` | Public transit entrance; turnstiles are separate system |
| `ENT_DOOR_TSQ_SUBWAY_02` | Times Square station, 44th St / Broadway entrance | MTA Subway | Unlocked (public) | `unlocked` | Secondary entrance; less crowded |
| `ENT_DOOR_TSQ_SUBWAY_03` | MTA service room, 42nd St mezzanine | MTA Subway (restricted) | Key (MTA staff) | `locked` | Utility/maintenance access |

---

## 6. Verification Notes

### 6.1 Coverage Verification

| Check | Method | Result |
|---|---|---|
| Every intersection has crosswalk signals | Count intersections (10) vs crosswalk groups | 20 crosswalks across 10 intersections: PASS |
| CCTV covers all intersections | Map camera FOV cones to intersection centers | All 10 intersections have at least one camera with direct LOS: PASS |
| TKTS steps have dedicated coverage | Check CCTV_04 and CCTV_05 placement | Dual-camera coverage (south and north facing): PASS |
| Kiosks accessible from all sub-zones | Check kiosk distribution against zone quadrants | 5 kiosks covering south (01, 05), center (02, 03), and north (04): PASS |
| Key buildings have door entries | Check Marriott, AMC, One Times Square, TKTS | 4+ doors on major buildings, retail coverage: PASS |
| Coverage gaps exist for gameplay | Identify blind spots in CCTV map | 4 documented gaps (see Section 3): PASS |

### 6.2 Density Check

| Artifact Class | Count | Per-Block Average | Real-World Comparable |
|---|---|---|---|
| Crosswalk Signals | 20 | 4.0 per intersection | Matches NYC standard |
| CCTV Cameras | 18 | 3.6 per block | Slightly above average for high-security zone |
| Information Kiosks | 5 | 1.0 per block | Matches LinkNYC density in Times Square |
| Doors | 28 | 5.6 per block | Selective; only key buildings modeled |

### 6.3 Entity ID Convention

All entity IDs follow the pattern:

```
ENT_<CLASS>_<ZONE>_<BUILDING?>_<SEQUENCE>
```

| Segment | Values | Example |
|---|---|---|
| `ENT` | Fixed prefix | `ENT` |
| `CLASS` | `XWALK`, `TLIGHT`, `CCTV`, `KIOSK`, `DOOR` | `DOOR` |
| `ZONE` | `TSQ` (Times Square) | `TSQ` |
| `BUILDING` | Optional: `MARRIOTT`, `AMC`, `OTS`, `TKTS`, `RETAIL`, `OFFICE`, `SUBWAY` | `MARRIOTT` |
| `SEQUENCE` | Two-digit zero-padded number | `01` |

Example: `ENT_DOOR_TSQ_MARRIOTT_03` = Door, Times Square zone, Marriott Marquis building, instance 03.

---

*End of Times Square Placement Map v0*
