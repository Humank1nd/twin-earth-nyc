# Splat Alignment + Residual Checklist

> **Twin Earth NYC -- Part 10: Build Pipeline**
> Document: `splat-alignment-checklist-v0.md` | Version 0.1 | Status: Draft
> Last updated: 2026-01-27

---

## Purpose

Gaussian splats and photogrammetry captures are never pixel-perfect to the geospatial skeleton. This checklist defines the mandatory alignment procedure, tolerance thresholds, recovery actions when alignment fails, residual computation methodology, and the quality tier system that determines how each aligned splat may be used in the final build.

**Core Principle:** The geospatial skeleton (Rung 1) is always truth. Splats conform to the skeleton -- never the reverse.

---

## Alignment Procedure

Execute every step in order. Do not skip steps. If a step fails, execute the recovery action before proceeding.

| Step | Action | Tolerance | Recovery if Fail |
|------|--------|-----------|------------------|
| **1** | **Import splat scene into engine.** Load the Gaussian splat (`.ply`, `.splat`, or engine-native format) or photogrammetry mesh into the scene. Verify the file loads without corruption: point/splat count matches export manifest, no NaN positions, no degenerate splats. | -- (binary pass/fail) | Re-export from source with correct format settings. Verify export tool version compatibility. If persistent, re-capture. |
| **2** | **Set splat origin to match geospatial skeleton (coarse alignment).** Translate the splat so that a clearly identifiable feature (building corner, intersection center, monument base) aligns with its corresponding position in the Rung 1 skeleton. This is a rough manual placement. | **< 5m** positional error at the alignment feature | Manual origin adjustment: pick 3 corresponding points and apply rigid transform. If > 20m off, verify the splat's source coordinate system (check CRS, UTM zone, local origin). |
| **3** | **ICP (Iterative Closest Point) refinement.** Run ICP registration between splat point cloud and skeleton geometry. Use at least 10,000 sample points. Max iterations: 100. Convergence threshold: 0.01m RMS delta between iterations. | **< 0.5m** RMS residual after convergence | Increase ICP iterations to 500. Add 5+ manual correspondence points as initial alignment hints. Reduce sample radius to focus on high-confidence geometry (ground plane, building edges). If still failing, the splat may have severe distortion -- flag for re-capture. |
| **4** | **Verify scale: measure 3 known objects.** Measure at least 3 real-world objects visible in the splat and compare against known dimensions. Mandatory measurement targets (use at least 3): | **< 3% error** on each measurement | Apply **uniform** scale correction. Compute the average scale factor across all measurements and apply as a single uniform scale. Non-uniform scale is prohibited (it breaks splat rendering). If error persists after uniform correction, the capture has non-uniform distortion -- flag for re-capture. |

**Scale measurement targets (choose 3+ from this list):**

| Object | Known Dimension | Measurement Axis |
|--------|----------------|------------------|
| Standard door | 2.1m height | Vertical |
| NYC yellow taxi | 4.9m length | Horizontal |
| Streetlight pole | 8.0m height | Vertical |
| Fire hydrant | 0.76m height | Vertical |
| Standard bollard | 0.91m height | Vertical |
| Crosswalk stripe width | 0.3m width | Horizontal |
| Curb height | 0.15m height | Vertical |
| Subway entrance railing | 1.07m height | Vertical |

| Step | Action | Tolerance | Recovery if Fail |
|------|--------|-----------|------------------|
| **5** | **Verify orientation: north arrow + building edges.** Overlay a compass rose on the splat. Verify that building edges known to run north-south or east-west are correctly oriented. Cross-reference with geospatial skeleton building outlines. | **< 2 degrees** rotation error | Apply rotation correction around the vertical axis. Compute the average angular error across 3+ building edges and apply a single yaw correction. If > 10 degrees, the splat origin orientation was wrong -- return to Step 2. |
| **6** | **Verify elevation: ground plane at known anchors.** At 5+ anchor points where the ground plane is visible in both the splat and the skeleton, measure the vertical offset between the splat ground and skeleton ground. | **< 0.3m** vertical error at each anchor | Apply Z-axis offset correction. If error varies significantly across anchors (> 0.5m range), the splat has vertical warping -- consider splitting into sub-regions and aligning each independently, or flag for re-capture. |
| **7** | **Compare splat silhouette vs reference photo.** Load a Hero Angle reference photograph. Position the engine camera to match. Overlay the splat render at 50% opacity over the reference photo. Assess building silhouettes, street proportions, and landmark placement. | **Qualitative** -- building outlines and major features should align | Flag specific areas of mismatch for manual review. If the entire silhouette is off, return to Step 3 (ICP may have converged to a local minimum). Try ICP with different initial alignment. |
| **8** | **Mark splat boundary (where it's reliable vs noisy).** Walk through the splat and identify regions of good quality (dense, clean, accurate) versus noisy/incomplete regions (sparse, floating artifacts, temporal ghosting from moving objects). Paint a quality mask. | -- (no numeric tolerance; qualitative assessment) | For noisy regions: mask them out so they do not render. These areas will be filled by procedural geometry (Rung 5). Document the noisy regions and their likely cause (occlusion, moving objects, lighting change during capture). |
| **9** | **Create splat visibility mask (compositing).** Define the final compositing mask: where the splat is rendered vs where procedural geometry takes over. The mask should feather at boundaries to avoid hard seams. Splat wins in areas where it is Tier A or B quality; procedural wins elsewhere. | -- (visual quality check: no hard seams at mask boundaries) | Adjust mask feathering width (typical: 2--5m feather). If seams remain visible, add a blending volume that cross-fades over a larger region. In extreme cases, extend the procedural geometry to fully cover the seam zone. |
| **10** | **Final residual report.** Compute the residual error at every anchor point within the splat coverage area. Generate a residual report and heatmap. Determine the overall quality tier. | **< 1.0m** at all anchor points | If any anchor exceeds 1.0m: repeat alignment from Step 3 with that anchor as a manual correspondence constraint. If still exceeding after 2 attempts, the splat has irrecoverable distortion at that location -- mask the region and fall back to procedural, or flag for re-capture. |

---

## Residual Computation

### Method

For each anchor point within the splat coverage area:

1. Identify the anchor's **truth position** from the Rung 1 geospatial skeleton (x, y, z in world coordinates).
2. Find the **corresponding position** in the aligned splat (nearest identifiable feature to the anchor).
3. Compute the positional error:

```
error_x = splat_x - truth_x
error_y = splat_y - truth_y
error_z = splat_z - truth_z
total_error = sqrt(error_x^2 + error_y^2 + error_z^2)
```

4. Record the result in the residual table.

### Residual Table Format

```csv
anchor_id,truth_x,truth_y,truth_z,splat_x,splat_y,splat_z,error_x,error_y,error_z,total_error,quality_tier
ANC_TSQ_001,583960.12,4507523.45,12.30,583960.25,4507523.60,12.22,0.13,0.15,-0.08,0.21,A
ANC_TSQ_002,583975.88,4507510.20,12.28,583976.10,4507510.55,12.40,0.22,0.35,0.12,0.43,B
ANC_TSQ_003,583990.44,4507498.77,12.35,583991.20,4507499.60,12.10,0.76,0.83,-0.25,1.16,D
```

### Residual Heatmap

Generate a top-down 2D heatmap overlaid on the block bounds:

- **Green (Tier A):** < 0.25m total error
- **Yellow (Tier B):** 0.25 -- 0.5m total error
- **Orange (Tier C):** 0.5 -- 1.0m total error
- **Red (Tier D):** > 1.0m total error

The heatmap is saved as `qa/capture/<block>_residual_heatmap.png` and attached to the block's QA record.

### Summary Statistics

The residual report must include:

| Metric | Value |
|--------|-------|
| Number of anchor points | (count) |
| Mean total error | (meters) |
| Median total error | (meters) |
| Max total error | (meters) |
| Std deviation | (meters) |
| % anchors in Tier A | (percentage) |
| % anchors in Tier B | (percentage) |
| % anchors in Tier C | (percentage) |
| % anchors in Tier D | (percentage) |
| Overall quality tier | (A / B / C / D -- determined by worst-anchor rule below) |

---

## Quality Tiers

| Tier | Max Residual (any anchor) | Mean Residual | Usage Authorization |
|------|---------------------------|---------------|---------------------|
| **A (Excellent)** | < 0.25m | < 0.15m | Hero zone, near-field rendering. Splat may be used as primary visual at close range. Derived meshes may be extracted for interaction surfaces. |
| **B (Good)** | 0.25 -- 0.5m | 0.15 -- 0.30m | Mid-distance, support zone. Splat renders at medium distances. Derived meshes require additional manual refinement before promotion. |
| **C (Acceptable)** | 0.5 -- 1.0m | 0.30 -- 0.60m | Far-field and background only. Splat renders only beyond 50m. No derived meshes may be extracted -- visual reference only. |
| **D (Poor)** | > 1.0m | > 0.60m | **Reject.** Splat is masked out entirely or used as loose visual reference in the `reference-only/` folder. Cannot render in-game at any distance. Flag for re-capture if the region is needed. |

### Tier Assignment Rule

The overall splat quality tier is determined by the **worst anchor**:

- If **any** anchor is Tier D, the entire splat is classified as Tier D for that region.
- Exception: If only 1 anchor out of 10+ is Tier D and all others are Tier B or better, the Tier D region may be locally masked and the remainder classified at its natural tier. This exception requires Art Lead sign-off.

---

## Checklist Summary Card

Print this card and keep it at the alignment workstation:

```
SPLAT ALIGNMENT CHECKLIST -- Quick Reference
=============================================
[ ] 1. Import splat -- no corruption
[ ] 2. Coarse align to skeleton -- < 5m
[ ] 3. ICP refinement -- < 0.5m RMS
[ ] 4. Scale check (3 objects) -- < 3% error
[ ] 5. Orientation check -- < 2 degrees
[ ] 6. Elevation check (5 anchors) -- < 0.3m
[ ] 7. Silhouette compare vs photo -- qualitative match
[ ] 8. Mark reliable vs noisy boundary
[ ] 9. Create visibility/compositing mask
[ ] 10. Final residual report -- < 1.0m all anchors

Tier: [ A ] [ B ] [ C ] [ D ]
Signed: ________________  Date: ________________
```

---

## Output Files

| Output | Path | Format |
|--------|------|--------|
| Aligned splat scene | `capture/splats/TSQ_SPLAT_<block>.splat` | Engine-native or `.ply` |
| Visibility mask | `capture/splats/TSQ_SPLAT_MASK_<block>.png` | Grayscale PNG (white = render, black = mask) |
| Residual table | `qa/capture/<block>_residuals.csv` | CSV (see format above) |
| Residual heatmap | `qa/capture/<block>_residual_heatmap.png` | PNG with overlay |
| Residual summary | `qa/capture/<block>_residual_summary.json` | JSON with summary statistics |
| Alignment log | `qa/capture/<block>_alignment_log.md` | Markdown with step-by-step notes |

---

*End of document. For questions about splat alignment procedures, contact the Art Lead or Geo Team lead.*
