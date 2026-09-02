# BLD-MIN-001 textured base orthographic reference package v02 — generation record

Date: 2026-08-31
Mode: built-in image edit of the best clay-aligned sheet
Geometry/layout target: `References/Terran/Buildings/BLD-MIN-001/Base/BLD-MIN-001_base_reference-sheet_v04.png`
Material source: `Concepts/Terran/Buildings/BLD-MIN-001/Base/BLD-MIN-001_base-concept_v02.png`
Material library: `Concepts/Terran/Materials/MAT-TER-001/MAT-TER-001_concept_v01.png`
Best output: `References/Terran/Buildings/BLD-MIN-001/Base/BLD-MIN-001_base_reference-sheet_v06.png`
Status: **superseded by the passing v12 package recorded in reference-pack v03**

## Prompt

> Use case: precise-object-edit. Asset type: textured orthographic 3D reconstruction reference
> sheet v06. Image 1 is the four-view edit target; preserve its silhouettes, geometry, view order,
> camera scale, positions, dividers and canvas. Image 2 is the authoritative textured body-only
> material-zoning reference; Image 3 is the Terran palette reference. Change only the four objects'
> surface materials. Apply consistent matte graphite foundation/frame/receiver zones, warm off-white
> worn armour on broad building walls and roofs, restrained amber hazard bands on existing edges and
> receiver surrounds, and subtle broad chipped paint, mining dust and grime. Keep texture scale,
> placement and wear consistent between opposing views. Do not alter geometry or paint fake doors,
> windows, hatches, vents, fans, pipes, tanks, conveyors, drills, railings, lights, panels, bolts,
> seams or recesses. No glow, reflections, cast shadow, text, labels, environment or watermark.

## Results

| Revision | Result | Review |
|---|---|---|
| v06 | warning: 5.4% height variation and 3.4% vertical-centre drift | best textured candidate; material pass accepted, alignment still outside preferred gate |
| v07 | warning: 8.0% height variation and 2.2% vertical-centre drift | targeted centering correction regressed height consistency; rejected |

The four v06 tiles were cropped mechanically with `--center-gutter-px 3`. v06 remains below the
10% hard-failure threshold but is not approved for paid generation because it exceeds the preferred
3% height and 2% centre tolerances.
