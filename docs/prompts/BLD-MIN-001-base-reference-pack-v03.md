# BLD-MIN-001 textured base orthographic reference package v03 — correction record

Date: 2026-08-31
Mode: built-in image editing followed by deterministic non-repainting alignment
Starting package: `References/Terran/Buildings/BLD-MIN-001/Base/BLD-MIN-001_base_reference-sheet_v06.png`
Approved output: `References/Terran/Buildings/BLD-MIN-001/Base/BLD-MIN-001_base_reference-sheet_v12.png`
Status: **approved for body-only 3D submission**

## Built-in image-edit prompt set

All four attempts used the `precise-object-edit` mode, treated the current sheet as the edit target,
locked the top front/back views, preserved the 2 × 2 order, orthographic cameras, dividers, neutral
background, graphite/off-white/amber material zoning and surface wear, and prohibited redesign,
repainting, perspective, shadows, text, new objects and below-foundation geometry.

| Revision | Requested correction | Result |
|---|---|---|
| v08 | enlarge side views about 5.75% and move them down about 21 px; target common 184 px height and centre | model moved sides upward; rejected |
| v09 | from v08, move sides down about 47 px and enlarge about 4.5%; target 183 px and centre 0.512 | centring passed but size overshot; rejected |
| v10 | from v09, shrink sides about 7% around their unchanged centres; target 184 px | size over-corrected to 173 px; rejected |
| v11 | from v10, enlarge sides about 3.5% around unchanged centres; target 183–184 px | size over-corrected to 202 px; rejected |

## Final deterministic alignment

The accepted v06 front/back crops were copied unchanged. The accepted v06 left/right crops were
uniformly scaled to a 184 px target silhouette height and translated to target centres near 0.51;
no pixels were generated or repainted during this step. The exact command was:

```text
python -B tools/align-reference-views.py <v06 sheet> <v06 front> <v06 back> <v06 left> <v06 right> --output-dir <Base> --stem BLD-MIN-001_base --version v12 --target-height 184 --target-cy 0.510 --left-cx 0.495 --right-cx 0.485 --center-gutter-px 3
```

The resulting v12 package passes all preferred alignment checks with no validator issues. Full
measurements are recorded in `BLD-MIN-001_reference-validation_v03.md`.
