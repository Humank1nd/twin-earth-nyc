# Asset Naming Conventions + Registry

> **Twin Earth NYC -- Part 10: Build Pipeline**
> Document: `naming-conventions-v0.md` | Version 0.1 | Status: Draft
> Last updated: 2026-01-27

---

## Purpose

Every asset in Twin Earth NYC follows a deterministic naming convention. Given an asset name, any team member can immediately determine its region, type, subtype, instance, LOD level, tier, and promotion status. This document defines the naming schema, all valid tokens, the asset registry format, and the promotion/versioning workflow.

**Rule:** If you cannot parse an asset's name into the schema below, it is incorrectly named and must be renamed before commit.

---

## Region Naming

Regions are the top-level geographic divisions of the game world.

| Code | Region | Status |
|------|--------|--------|
| `TSQ` | Times Square (42nd--47th, Broadway to 7th Ave) | Active -- primary build target |
| `MID` | Midtown (surrounding Times Square expansion) | Planned |
| `CHE` | Chelsea (south expansion) | Planned |
| `HEK` | Hell's Kitchen (west expansion) | Planned |
| `BRP` | Bryant Park (east expansion) | Planned |
| `GBL` | Global (shared assets not region-specific) | Active |

### Block Naming

Blocks are individual city blocks within a region, identified by a grid coordinate.

**Format:** `<region>_BLK_<row><col>`

- Row: uppercase letter (A = southernmost, B = next north, etc.)
- Column: digit (1 = westernmost, 2 = next east, etc.)

**Examples:**
| Name | Description |
|------|-------------|
| `TSQ_BLK_A1` | Times Square, Block A1 (southwest corner of region) |
| `TSQ_BLK_A2` | Times Square, Block A2 (next east) |
| `TSQ_BLK_B1` | Times Square, Block B1 (next north) |
| `TSQ_BLK_C3` | Times Square, Block C3 |

### Intersection Naming

Intersections are named by their cross-streets.

**Format:** `<region>_INT_<street1>_<street2>`

- Streets use abbreviated names: numbered streets as digits, named streets abbreviated.

**Examples:**
| Name | Description |
|------|-------------|
| `TSQ_INT_42_BWAY` | 42nd Street and Broadway |
| `TSQ_INT_42_7AV` | 42nd Street and 7th Avenue |
| `TSQ_INT_44_BWAY` | 44th Street and Broadway |
| `TSQ_INT_46_7AV` | 46th Street and 7th Avenue |

**Street abbreviations:**
| Abbreviation | Full Name |
|-------------|-----------|
| `BWAY` | Broadway |
| `7AV` | 7th Avenue |
| `6AV` | 6th Avenue |
| `8AV` | 8th Avenue |
| `42` -- `47` | 42nd -- 47th Street |

---

## Asset Naming Schema

### Full Format

```
<region>_<type>_<subtype>_<id>_<lod>
```

| Component | Format | Description | Required |
|-----------|--------|-------------|----------|
| `<region>` | 3 uppercase letters | Geographic region code (see Region Naming) | Yes |
| `<type>` | 2--4 uppercase letters | Asset type code (see Type Codes) | Yes |
| `<subtype>` | 2--10 uppercase letters | Specific subtype within the type (see Subtype Codes) | Yes |
| `<id>` | 3-digit number OR block ID | Unique instance identifier within type+subtype | Yes |
| `<lod>` | `L0`, `L1`, `L2`, `LIMP` | Level of detail (L0 = highest, LIMP = impostor) | Yes (for renderable assets) |

### Type Codes

| Code | Type | Description | Example Asset |
|------|------|-------------|---------------|
| `BLD` | Building | Complete building or building section | `TSQ_BLD_FACADE_001_L0` |
| `PRP` | Prop | Street furniture, small objects | `TSQ_PRP_BOLLARD_015_L1` |
| `VEH` | Vehicle | Cars, trucks, buses | `TSQ_VEH_TAXI_003_L0` |
| `CHR` | Character | NPCs, pedestrians | `TSQ_CHR_PEDNPC_042_L0` |
| `BB` | Billboard | LED screens, signage, marquees | `TSQ_BB_HERO_01_L0` |
| `COL` | Collision | Collision meshes (not rendered) | `TSQ_COL_SIDEWALK_A1_L0` |
| `NAV` | NavMesh | Navigation meshes and annotations | `TSQ_NAV_PED_A1` |
| `MAT` | Material | Material definitions | `TSQ_MAT_ASPHALT_WET_001` |
| `TEX` | Texture | Texture maps | `TSQ_TEX_BRICK_RED_001` |
| `VFX` | Visual Effect | Particle systems, post-process volumes | `TSQ_VFX_STEAM_VENT_003` |
| `AUD` | Audio | Sound effects, ambience | `TSQ_AUD_TRAFFIC_LOOP_001` |
| `LIT` | Lighting | Light entities, lightmaps | `TSQ_LIT_STREETLIGHT_A1_007` |
| `IOT` | IoT Artifact | Cameras, sensors, signal controllers | `TSQ_IOT_CAMERA_A1_003` |
| `SPL` | Splat | Gaussian splat captures | `TSQ_SPL_BLOCK_A1` |
| `DRV` | Derived Mesh | Meshes derived from scans/splats | `TSQ_DRV_STOOP_042_L0` |
| `SKL` | Skeleton | Geospatial skeleton data | `TSQ_SKL_TILE_A1` |
| `ANM` | Animation | Animation clips and blend trees | `GBL_ANM_WALK_CASUAL_001` |

### Subtype Codes (by Type)

**Buildings (`BLD`):**
| Subtype | Description |
|---------|-------------|
| `FACADE` | Building facade (exterior wall) |
| `ROOF` | Rooftop geometry |
| `INTERIOR` | Interior space |
| `ENTRANCE` | Entrance/doorway |
| `CANOPY` | Awning or canopy |
| `FIRE_ESC` | Fire escape |

**Props (`PRP`):**
| Subtype | Description |
|---------|-------------|
| `BOLLARD` | Street bollard |
| `TRASHCAN` | Trash receptacle |
| `BENCH` | Street bench |
| `HYDRANT` | Fire hydrant |
| `NEWSBOX` | Newspaper box |
| `PHONE` | Phone booth |
| `MAILBOX` | USPS mailbox |
| `PLANTER` | Street planter |
| `SCAFFOLD` | Construction scaffolding |
| `BARRIER` | Temporary barrier |
| `CONE` | Traffic cone |
| `SIGN_POST` | Street sign post |
| `SIGNAL` | Traffic signal |
| `STREETLT` | Streetlight |

**Vehicles (`VEH`):**
| Subtype | Description |
|---------|-------------|
| `TAXI` | Yellow taxi cab |
| `SEDAN` | Standard sedan |
| `SUV` | Sport utility vehicle |
| `BUS` | City bus |
| `DELIVERY` | Delivery truck |
| `POLICE` | Police vehicle |
| `AMBULANCE` | Ambulance |
| `BIKE` | Bicycle |
| `MOTORCYCLE` | Motorcycle |

**Billboards (`BB`):**
| Subtype | Description |
|---------|-------------|
| `HERO` | Hero billboard (T1, full animation) |
| `SUPPORT` | Support billboard (T2, simple animation) |
| `STATIC` | Static signage (T3, no animation) |
| `MARQUEE` | Theater marquee |
| `TICKER` | News/stock ticker |

**Collision (`COL`):**
| Subtype | Description |
|---------|-------------|
| `ROAD` | Road surface collision |
| `SIDEWALK` | Sidewalk collision |
| `CURB` | Curb geometry |
| `STAIR` | Staircase collision |
| `BARRIER` | Impassable barrier |
| `MEDIAN` | Road median |
| `DRV` | Collision proxy for derived mesh |

**IoT Artifacts (`IOT`):**
| Subtype | Description |
|---------|-------------|
| `CAMERA` | Surveillance camera |
| `SENSOR` | Environmental sensor |
| `SIGNAL` | Traffic signal controller |
| `SPEAKER` | Public address speaker |
| `SCREEN` | Information display |

---

## Tier Tags

Tier indicates fidelity level and determines asset budgets, LOD behavior, and streaming priority.

| Tag | Name | Description | Triangle Budget | Texture Budget |
|-----|------|-------------|-----------------|----------------|
| `T1` | Hero | Highest fidelity, unique assets. Landmarks, key interaction points. | Full per-asset budget | Up to 4K textures |
| `T2` | Support | Mid-distance, instanced motifs. Repeated building sections, standard props. | 50% of hero budget | Up to 2K textures |
| `T3` | Background | Far-field, silhouette only. Distant buildings, skyline fill. | 10% of hero budget | Up to 1K textures |

Tier is encoded in the asset's metadata (not in the filename) but is tracked in the registry:

```json
{
  "asset_id": "TSQ_BLD_FACADE_001_L0",
  "tier": "T1",
  "triangle_count": 142000,
  "texture_resolution": "4096x4096"
}
```

---

## Version + Promotion Suffixes

### Staging vs Canonical

| Suffix | Meaning | Usage |
|--------|---------|-------|
| `_STAGE` | Staging asset | Asset is work-in-progress, not yet promoted to canonical. Lives in working branch only. May not be referenced by canonical assets. |
| `_CANON` | Canonical asset | Asset has passed the Promotion Checklist (see `asset-ladder-v0.md`) and is approved for use in builds. |

**Examples:**
```
TSQ_DRV_STOOP_042_L0_STAGE    -- Work in progress, not yet reviewed
TSQ_DRV_STOOP_042_L0_CANON    -- Promoted, approved, canonical
```

### Version Numbers

**Format:** `_v<NNN>` (3-digit zero-padded)

Versions increment when a canonical asset is revised. The previous version is archived, not deleted.

**Examples:**
```
TSQ_BLD_FACADE_001_L0_CANON_v001   -- First canonical version
TSQ_BLD_FACADE_001_L0_CANON_v002   -- Revised version (v001 archived)
TSQ_BLD_FACADE_001_L0_CANON_v003   -- Third revision
```

### Full Name Example (Maximum Specificity)

```
TSQ_BLD_FACADE_001_L0_CANON_v002
│    │    │       │   │   │      │
│    │    │       │   │   │      └── Version 2
│    │    │       │   │   └── Canonical (promoted)
│    │    │       │   └── LOD 0 (near/highest detail)
│    │    │       └── Instance 001
│    │    └── Subtype: Facade
│    └── Type: Building
└── Region: Times Square
```

---

## Asset Registry

### Registry File: `registry/asset-registry.csv`

Every committed asset must have a row in the registry. The registry is the single source of truth for what exists in the project.

**CSV Format:**

```csv
asset_id,display_name,type,subtype,region,block,tier,lod,status,rung,version,triangle_count,texture_res,author,created_date,last_modified,notes
```

**Field Definitions:**

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `asset_id` | string | Full asset name (without version suffix) | `TSQ_BLD_FACADE_001_L0` |
| `display_name` | string | Human-readable name | `One Times Square - North Facade` |
| `type` | enum | Type code | `BLD` |
| `subtype` | string | Subtype code | `FACADE` |
| `region` | enum | Region code | `TSQ` |
| `block` | string | Block ID (if block-specific) | `A1` |
| `tier` | enum | `T1`, `T2`, `T3` | `T1` |
| `lod` | enum | `L0`, `L1`, `L2`, `LIMP` | `L0` |
| `status` | enum | `STAGE`, `CANON`, `DEPRECATED`, `ARCHIVED` | `CANON` |
| `rung` | int | Asset Ladder rung (1--5) | `4` |
| `version` | int | Current version number | `2` |
| `triangle_count` | int | Triangle count for this LOD | `142000` |
| `texture_res` | string | Max texture resolution | `4096x4096` |
| `author` | string | Creator | `j.martinez` |
| `created_date` | date | First commit date | `2026-02-10` |
| `last_modified` | date | Last modification date | `2026-03-01` |
| `notes` | string | Freeform | `Hero building - primary facade` |

**Example Rows:**

```csv
TSQ_BLD_FACADE_001_L0,One Times Square North Facade,BLD,FACADE,TSQ,A1,T1,L0,CANON,4,2,142000,4096x4096,j.martinez,2026-02-10,2026-03-01,Hero building primary facade
TSQ_PRP_BOLLARD_015_L1,Standard NYC Bollard,PRP,BOLLARD,TSQ,A1,T2,L1,CANON,5,1,480,1024x1024,s.chen,2026-02-14,2026-02-14,Standard kit piece
TSQ_COL_SIDEWALK_A1_L0,Block A1 Sidewalk Collision,COL,SIDEWALK,TSQ,A1,,L0,CANON,2,3,1200,,k.okafor,2026-02-08,2026-02-20,Updated curb heights in v3
TSQ_BB_HERO_01_L0,Primary One TS Billboard,BB,HERO,TSQ,A1,T1,L0,CANON,5,1,800,1920x1080,a.wright,2026-02-18,2026-02-18,Video billboard - 4 content slots
TSQ_NAV_PED_A1,Block A1 Pedestrian NavMesh,NAV,PED,TSQ,A1,,,CANON,2,4,,,k.okafor,2026-02-08,2026-02-22,Crosswalk zones updated in v4
```

---

## Promotion Log

### Promotion Log File: `registry/promotions.csv`

Every promotion event (STAGE to CANON, or rung change) is recorded.

**CSV Format:**

```csv
date,asset_id,asset_name,from_status,to_status,from_rung,to_rung,version,reviewer,checklist_steps,notes
```

**Example Rows:**

```csv
2026-02-15,TSQ_DRV_STOOP_042_L0,42nd St Stoop,STAGE,CANON,3,4,1,j.martinez,1;2;3;4;5;6;8;9;10,Retopo from splat capture batch 07
2026-02-20,TSQ_COL_SIDEWALK_A1_L0,Block A1 Sidewalk,CANON,CANON,2,2,3,k.okafor,1;2;3;5;6;9;10,Curb height correction - re-promoted same rung
2026-03-01,TSQ_BLD_FACADE_001_L0,One TS North Facade,CANON,CANON,4,4,2,j.martinez,1;2;4;5;8;10,LOD chain revised for performance
```

---

## Naming Validation Rules

Automated validation runs on every commit. The following rules are enforced:

| Rule | Check | Error Level |
|------|-------|-------------|
| **Region code valid** | `<region>` matches known region codes | Error (blocks commit) |
| **Type code valid** | `<type>` matches known type codes | Error |
| **Subtype valid for type** | `<subtype>` is in the valid subtype list for the given type | Error |
| **ID format correct** | 3-digit zero-padded number OR valid block ID | Error |
| **LOD suffix present** (for renderable assets) | `L0`, `L1`, `L2`, or `LIMP` | Error |
| **LOD suffix absent** (for non-renderable assets: NAV, COL) | No LOD suffix on collision/nav assets (they have single representations) | Warning |
| **No spaces or special characters** | Only uppercase letters, digits, and underscores | Error |
| **Registry entry exists** | Asset has a corresponding row in `asset-registry.csv` | Error |
| **No duplicate IDs** | No two assets share the same full `asset_id` | Error |
| **Version monotonically increasing** | New version number > previous version number for same asset | Error |
| **STAGE assets not referenced by CANON** | No canonical asset may depend on a staging asset | Error |

### Validation Script

```bash
# Run naming validation on all assets in a directory
python tools/validate_naming.py --directory assets/ --registry registry/asset-registry.csv

# Run on a single file
python tools/validate_naming.py --file assets/TSQ_BLD_FACADE_001_L0.uasset

# Run as pre-commit hook (configured in .pre-commit-config.yaml)
# Automatically validates all staged files
```

**Expected output (clean):**
```
Validating 347 assets...
  Region codes: 347/347 valid
  Type codes: 347/347 valid
  Subtype codes: 347/347 valid
  ID format: 347/347 valid
  LOD suffix: 312/312 renderable assets valid
  Registry entries: 347/347 found
  Duplicate check: 0 duplicates
  Reference integrity: 0 STAGE->CANON violations
RESULT: ALL PASSED
```

**Expected output (failure):**
```
Validating 348 assets...
  ERROR: TSQ_BLD_facade_001_L0 -- subtype must be uppercase (found 'facade')
  ERROR: TSQ_PRP_BOLLARD_15_L1 -- ID must be 3-digit zero-padded (found '15', expected '015')
  ERROR: TSQ_XYZ_THING_001_L0 -- unknown type code 'XYZ'
  WARNING: TSQ_COL_ROAD_A1_L0 -- collision asset has LOD suffix (not required)
RESULT: 3 ERRORS, 1 WARNING -- COMMIT BLOCKED
```

---

## Quick Reference Card

```
NAMING CONVENTION QUICK REFERENCE
==================================

Format:  <REGION>_<TYPE>_<SUBTYPE>_<ID>_<LOD>
Example: TSQ_BLD_FACADE_001_L0

REGIONS: TSQ MID CHE HEK BRP GBL
BLOCKS:  TSQ_BLK_A1  TSQ_BLK_B2  (row=letter, col=digit)
INTERS:  TSQ_INT_42_BWAY  TSQ_INT_44_7AV

TYPES:   BLD PRP VEH CHR BB COL NAV MAT TEX VFX AUD LIT IOT SPL DRV SKL ANM
LODs:    L0 (near)  L1 (mid)  L2 (far)  LIMP (impostor)
TIERS:   T1 (hero)  T2 (support)  T3 (background)
STATUS:  _STAGE (wip)  _CANON (approved)
VERSION: _v001  _v002  _v003 ...

COMMIT RULES:
 - Name must parse into schema
 - Registry entry required
 - No STAGE assets in CANON references
 - Pre-commit hook validates automatically
```

---

## File Extension Conventions

| Asset Type | Primary Extension | Notes |
|------------|-------------------|-------|
| Static mesh | `.uasset` (Unreal) / `.fbx` (interchange) | FBX for interchange; engine-native for commits |
| Texture | `.uasset` / `.png` (source) | Source PNGs in `source/`; compressed in engine |
| Material | `.uasset` / `.mat` | Engine-native material definition |
| Splat | `.ply` / `.splat` | Platform-specific splat format |
| NavMesh | `.navmesh` / engine-native | Baked navigation data |
| Collision | `.uasset` / engine-native | Simplified collision mesh |
| Audio | `.wav` (source) / `.ogg` (runtime) | Lossless source; compressed runtime |
| Animation | `.uasset` / `.fbx` (source) | FBX for interchange |
| Config/data | `.json` / `.csv` | Human-readable data files |

---

*End of document. For questions about naming conventions or registry management, contact the Build Pipeline lead.*
