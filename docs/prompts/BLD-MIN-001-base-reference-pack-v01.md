# BLD-MIN-001 base orthographic reference package v01 — generation record

Date: 2026-08-31
Mode: built-in image generation with one body-only design reference
Input: `Concepts/Terran/Buildings/BLD-MIN-001/Base/BLD-MIN-001_base-concept_v01.png`
Initial output sheet: `References/Terran/Buildings/BLD-MIN-001/Base/BLD-MIN-001_base_reference-sheet_v01.png`
Best candidate: `References/Terran/Buildings/BLD-MIN-001/Base/BLD-MIN-001_base_reference-sheet_v04.png`
Status: **superseded clay-reference trial; replaced by textured reference record v02**

## Prompt

> Use case: stylized-concept. Asset type: orthographic 3D reconstruction reference sheet. Use the
> supplied image only as the exact design and massing reference. Create one square 2 × 2 sheet of
> the identical body-only Terran Basic Mine structural base in this exact order: top-left FRONT,
> top-right BACK, bottom-left LEFT, bottom-right RIGHT. True orthographic elevation in every tile;
> no perspective or foreshortening. Preserve the same 45 × 32 m footprint, low processing-building
> shells, broad foundation/deck, central raised octagonal drill deck, large chamfers, deep setbacks,
> structural buttresses and every closed mounting pad/recess. The object must have identical geometry,
> scale, vertical placement, camera distance and centre in all four tiles. Uniform matte light-neutral
> clay material on one neutral light-grey background with flat diffuse lighting and no ground shadow.
> Base shell only: no derrick, gantry, hoist, drill, conveyor, tanks, pipes, valves, vents, fans,
> flues, doors, hatches, railings, ladders, lights, panels, equipment boxes, decals, markings, wear,
> greeble, text, labels, borders, environment or loose objects. Do not redesign between views.

Crop the four tiles without creative repainting and submit them to later reconstruction in the
order front, back, left, right. `tools/check-views.py` must pass before any paid 3D job.

## Iteration results

| Revision | Result | Review |
|---|---|---|
| v01 | hard fail: 30.6% silhouette-height variation | side views were flattened and stretched |
| v02 | hard fail after validator correction: 14.3% height variation | divider lines originally caused a false pass |
| v03 | hard fail: 5.1% vertical-centre drift after divider-safe crop | height was close but side views sat too high |
| v04 | warning: 6.1% height variation and 3.6% vertical-centre drift | best candidate; visually coherent but outside preferred 3% gate |
| v05 | hard fail: 10.0% height variation and 5.6% vertical-centre drift | targeted correction overextended side elevations |

The built-in image-generation workflow produced all five clay revisions. v04 is retained only as
alignment/failure history. The production workflow continues with textured base concept v02 and
the textured reference record `BLD-MIN-001-base-reference-pack-v02.md`.
