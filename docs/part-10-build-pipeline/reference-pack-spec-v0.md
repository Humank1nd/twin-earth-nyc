# Times Square Reference Pack + License Sheet

> **Twin Earth NYC -- Part 10: Build Pipeline**
> Document: `reference-pack-spec-v0.md` | Version 0.1 | Status: Draft
> Last updated: 2026-01-27

---

## Purpose

The Reference Pack is the curated visual library that every artist, modeler, and environment designer uses as ground truth for "how Times Square actually looks." This document specifies folder structure, curation targets, the 10 Hero Angles that must match real-world appearance, the reference sheet tracking format, and all scraping ethics and licensing rules.

**Principle:** Quality over quantity. 50 well-tagged, properly licensed images beat 5,000 unorganized screenshots.

---

## Folder Structure

```
reference-pack/
├── landmarks/                    # One Times Square, TKTS, Marriott Marquee, etc.
│   ├── one-times-square/
│   ├── tkts-red-steps/
│   ├── marriott-marquee/
│   ├── nasdaq-tower/
│   ├── palace-theatre/
│   └── other/
├── intersections/                # Key intersection views
│   ├── 42nd-broadway/
│   ├── 42nd-7th-ave/
│   ├── 44th-broadway/
│   ├── 46th-broadway/
│   └── bowtie-overhead/
├── billboards/                   # Billboard reference photos
│   ├── static-signage/
│   ├── led-screens/
│   ├── video-boards/
│   └── marquees/
├── street-furniture/             # Props, signals, bollards, etc.
│   ├── traffic-signals/
│   ├── streetlights/
│   ├── bollards/
│   ├── trash-cans/
│   ├── benches/
│   ├── phone-booths/
│   ├── subway-entrances/
│   ├── fire-hydrants/
│   └── newsboxes/
├── night-variants/               # Nighttime references
│   ├── golden-hour/
│   ├── blue-hour/
│   ├── full-dark/
│   └── late-night-low-crowd/
├── rain-variants/                # Wet condition references
│   ├── light-rain/
│   ├── heavy-rain/
│   ├── wet-pavement-reflections/
│   └── post-rain/
├── aerial/                       # Overhead/drone views
│   ├── low-angle-100ft/
│   ├── mid-angle-300ft/
│   └── high-angle-satellite/
├── materials/                    # Surface material close-ups
│   ├── asphalt/
│   ├── concrete-sidewalk/
│   ├── granite-curb/
│   ├── metal-grating/
│   ├── glass-facades/
│   └── brick/
├── licensed/                     # Cleared for direct use in game assets
├── reference-only/               # Inspiration/comparison only -- NOT for asset derivation
├── reference-sheet.csv           # Master reference tracking spreadsheet
└── README.md                     # Pack usage instructions and license summary
```

---

## Curation Target

| Metric | Target | Notes |
|--------|--------|-------|
| Total reference images | 50 -- 200 | Quality over quantity |
| Landmarks coverage | 100% of named landmarks | Minimum 3 angles per landmark |
| Hero Angles (see below) | 10 matched angles | Must be pixel-matchable to in-game camera |
| Night variants | 15 -- 30 | Coverage of all lighting conditions |
| Rain variants | 10 -- 20 | Wet pavement reflections are critical |
| Aerial views | 5 -- 10 | At least 1 ortho overhead |
| Street furniture types | All types represented | Minimum 2 examples per type |
| Material close-ups | 10 -- 20 | For PBR material authoring reference |

---

## Reference Sheet Format

The file `reference-sheet.csv` tracks every image/video in the pack. All fields are required.

### CSV Header

```csv
filename,source,license_status,license_detail,location_tag,heading_approx,time_of_day,weather,resolution,format,capture_date,notes
```

### Field Definitions

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `filename` | string | File name including extension | `HA01_broadway_north_42nd.jpg` |
| `source` | string | Where the image was obtained | `team_capture`, `unsplash`, `shutterstock`, `google_sv` |
| `license_status` | enum | `licensed`, `cc_by`, `cc0`, `public_domain`, `reference_only`, `pending` | `cc_by` |
| `license_detail` | string | License specifics, attribution requirements | `CC BY 4.0 - John Doe` |
| `location_tag` | string | Subfolder + landmark or intersection ID | `landmarks/one-times-square` |
| `heading_approx` | string | Compass heading camera faces | `North`, `SSW`, `Down` |
| `time_of_day` | enum | `dawn`, `morning`, `midday`, `afternoon`, `golden_hour`, `blue_hour`, `night`, `late_night` | `night` |
| `weather` | enum | `clear`, `overcast`, `light_rain`, `heavy_rain`, `wet_post_rain`, `snow`, `fog` | `clear` |
| `resolution` | string | Image dimensions | `4032x3024` |
| `format` | string | File format | `jpg`, `png`, `mp4`, `exr` |
| `capture_date` | date | When image was taken (if known) | `2025-11-15` |
| `notes` | string | Freeform notes | `Good billboard glow reference; slight lens flare on left` |

### Example Rows

```csv
HA01_broadway_north_42nd.jpg,team_capture,licensed,Full rights - team photo,intersections/42nd-broadway,North,midday,clear,4032x3024,jpg,2025-11-15,Hero Angle 01 - primary match target
HA08_night_billboard_glow.jpg,unsplash,cc0,CC0 Public Domain,night-variants/full-dark,North,night,clear,6000x4000,jpg,2025-09-20,Hero Angle 08 - billboard glow reference
ref_tkts_steps_rain.jpg,shutterstock,licensed,Shutterstock Standard License #SS-12345678,rain-variants/wet-pavement-reflections,Southeast,blue_hour,light_rain,5472x3648,jpg,2025-10-03,Excellent wet step reflections
gsv_42nd_7th_ave.jpg,google_sv,reference_only,Google Street View - not licensed for derivation,intersections/42nd-7th-ave,North,midday,clear,1920x1080,jpg,2025-08-01,Reference only - position/proportion check
```

---

## 10 Hero Angles

These 10 angles are the **canonical visual targets** for the Times Square build. Each must have at least one real-world reference photograph, and the in-game camera must be able to reproduce a near-identical composition. Art review compares Hero Angle screenshots against references at every milestone.

| Angle ID | Description | Location | Direction | Priority | Match Criteria |
|----------|-------------|----------|-----------|----------|----------------|
| **HA01** | Broadway looking north from 42nd | 42nd St / Broadway NW corner | North | **Critical** | Building silhouettes, billboard layout, street width |
| **HA02** | TKTS Red Steps from street level | Father Duffy Square, south edge | Southeast | **Critical** | Step geometry, surrounding buildings, statue position |
| **HA03** | One Times Square full height | Broadway median at 43rd | South-Southwest | **Critical** | Full building visible, billboard tiers, base proportions |
| **HA04** | 7th Ave looking north from 42nd | 42nd St / 7th Ave NW corner | North | **Critical** | Avenue width, building canyon, signal positions |
| **HA05** | Bowtie intersection overhead | Center of Broadway/7th Ave intersection | Down (overhead) | **High** | Road geometry, crosswalk pattern, median shape |
| **HA06** | Marriott Marquee entrance | 45th St near Broadway | West | **High** | Entrance canopy, LED signage, sidewalk width |
| **HA07** | Broadway canyon from 46th | 46th St / Broadway intersection | South | **High** | Canyon depth perspective, billboard density, traffic flow |
| **HA08** | Night billboard glow | TKTS steps, facing north | North | **High** | Light spill on pavement, color temperature, glow falloff |
| **HA09** | 42nd St corridor | 42nd St between Broadway and 7th Ave | East | **Medium** | Corridor proportions, pedestrian density context, storefront rhythm |
| **HA10** | Duffy Square statue | Father Duffy Square, near statue | Northwest | **Medium** | Statue detail, plinth, surrounding landscape elements |

### Hero Angle Matching Process

1. **Capture**: Obtain real-world photograph from the specified location and direction.
2. **Camera Setup**: In-engine, place camera at equivalent geospatial coordinates with matched focal length.
3. **Overlay**: Generate a 50% opacity overlay of reference on in-engine capture.
4. **Score**: Rate alignment on a 1--5 scale for silhouette match, proportion accuracy, and detail fidelity.
5. **Iterate**: Adjust environment until all Critical angles score 4+ and all High angles score 3+.

---

## Scraping Ethics + Legality

### Core Policy

> **Only use sources with explicit reuse license (CC, public domain, licensed stock) OR use as reference-only (not directly incorporated into game assets).** When in doubt, classify as `reference_only`.

### Source-by-Source Rules

| Source | License Status | Usage Permission | Folder |
|--------|---------------|------------------|--------|
| **Team photography** | Full rights | Direct use in assets, textures, references | `licensed/` |
| **Licensed stock** (Shutterstock, Getty, Adobe Stock) | Per-license terms | Direct use per license agreement | `licensed/` |
| **CC0 / Public Domain** | Unrestricted | Direct use, no attribution required | `licensed/` |
| **CC BY / CC BY-SA** | Attribution required | Direct use with proper attribution in credits | `licensed/` |
| **CC NC** (non-commercial) | Non-commercial only | Reference only unless project qualifies | `reference-only/` |
| **Google Street View** | Not licensed for derivation | Reference only -- position, proportion, layout checking | `reference-only/` |
| **Google Earth / Maps** | Not licensed for derivation | Reference only -- aerial composition checking | `reference-only/` |
| **Cesium Ion tilesets** | Per-tileset license | Check license per tileset; typically licensed for visualization, not redistribution of raw tiles | Verify per tileset |
| **Social media** (Instagram, Flickr, X) | Varies per post | Do NOT use unless explicit CC license on the specific post | `reference-only/` unless CC verified |
| **News media** (AP, Reuters, NYT) | Copyrighted | Reference only -- never derive assets from news photos | `reference-only/` |
| **AI-generated images** | No real-world accuracy guarantee | Never use as reference for real-world matching; may use for mood/concept only | `suggestive/` (not in reference pack) |

### Mandatory Documentation

Every image entering the reference pack **must** have:

1. A row in `reference-sheet.csv` with all fields populated.
2. License status clearly set to one of: `licensed`, `cc_by`, `cc0`, `public_domain`, `reference_only`, `pending`.
3. If `pending`, the image must be resolved to a final status within 14 days or removed from the pack.
4. If `licensed`, the license agreement or purchase receipt must be stored in `licensed/receipts/`.

### Prohibited Actions

- **No scraping** of images from websites without explicit permission or compatible license.
- **No use of Google Street View imagery** as texture source, training data, or direct asset input.
- **No removal of watermarks** from stock photos.
- **No use of copyrighted billboard content** -- all in-game billboards use fictional or licensed designs.
- **No photographing private interiors** without property owner consent.

### Attribution File

All CC-licensed images requiring attribution are listed in:

```
reference-pack/ATTRIBUTIONS.md
```

Format:
```markdown
## Image Attributions

- `HA02_tkts_steps.jpg` -- Photo by Jane Smith, CC BY 4.0
  Source: https://example.com/photo/12345
- `ref_7th_ave_night.jpg` -- Photo by Alex Rivera, CC BY-SA 4.0
  Source: https://flickr.com/photos/arivera/98765
```

This file is also used to generate in-game credits for shipped builds.

---

## Reference Pack Maintenance

| Task | Frequency | Responsible |
|------|-----------|-------------|
| Audit `reference-sheet.csv` for missing fields | Monthly | Art lead |
| Resolve all `pending` license statuses | Within 14 days of entry | Production |
| Verify `licensed/` vs `reference-only/` folder correctness | Monthly | Legal / Production |
| Capture new team photography (seasonal updates) | Quarterly | Art team |
| Update Hero Angle match scores | Per milestone | Art lead + QA |
| Archive outdated references (replaced by better captures) | As needed | Art team |

---

*End of document. For questions about licensing or reference pack contributions, contact the Art Lead or Production.*
