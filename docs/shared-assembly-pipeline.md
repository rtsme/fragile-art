# Shared-asset assembly pipeline

Status: **active trial**, beginning with `BLD-CMD-001` on 2026-08-31.

This pipeline separates a building's structural shell from the recurring detail that image-to-3D
generation cannot reproduce reliably. The approved concept remains the design target; it is not
the mesh-generation input.

## Folder contract

Every asset taken through this pipeline uses this layout:

```text
Concepts/<Faction>/<Category>/<Asset ID>/
  <Asset ID>_concept_vNN.png             final appearance target
  <Asset ID>_assembly-manifest_vNN.md    exact shared-asset bill of materials
  Base/
    <Asset ID>_base-concept_vNN.png      body-only generation source
    README.md                            asset-specific inclusion boundary

References/<Faction>/<Category>/<Asset ID>/Base/
  <Asset ID>_base_{front,back,left,right}_vNN.png

Models/<Faction>/<Category>/<Asset ID>/
  Base/                                  generated and cleaned structural shell
  <Asset ID>_*.assembly.json             editable Art Forge placement scene
  Assembly/                              editable assembled source and exports

Models/<Faction>/Shared/<Component ID>/  one reusable detail mesh per exact ID
```

The `References/.../Base/` and `Models/.../` folders are created when those stages begin. Empty
production folders are not committed in advance.

## Non-negotiable rules

1. **The root concept is final.** `<Asset ID>_concept_vNN.png` is the immutable final appearance
   target for that approved revision. It may show the fully dressed building, but it is never sent
   as geometry input. It may guide broad material zoning while the body-only source is created and,
   after geometry review, may be supplied to an optional texture-only refinement pass. Both uses are
   palette/material references only.
2. **Generate only the base.** The generator receives only images from `Base/` and
   `References/.../Base/`. The base contains the foundation, load-bearing walls, roofs, towers,
   large overhangs, deep structural setbacks and silhouette-defining structural masses. Those images
   retain approved broad material zones and macro wear; body-only does not mean untextured clay.
3. **Every detachable detail is separate.** Doors, glazing, vents, fans, tanks, pipes, antennas,
   dishes, lights, railings, stairs, ramps, equipment boxes, access panels and similar fittings
   are shared assets. They are not painted onto or modelled into the generated base.
4. **Receivers are allowed; detail is not.** The base may contain a closed, flat-bottomed recess,
   flush pad or simple S1-S4 socket where a shared mesh will attach. A receiver must have less
   geometric detail than the component it receives.
5. **The assembly manifest is a gate.** Every visible detachable item in the final concept must
   map to an exact shared component ID and a planned receiver. Family-only mappings such as
   `TER-VNT` are insufficient for production.
6. **A missing component is explicit.** If the final concept requires a detail with no matching
   shared ID, mark it `NEW SHARED ASSET REQUIRED`. Do not improvise it in the base. Either add the
   part to the shared library or revise the final concept to use an existing approved part.
7. **Assemble, then compare.** The assembled building is reviewed against the final concept.
   Approval depends on matching its silhouette, hierarchy and visible detail distribution, not
   on making the base image look finished.

## Structure-versus-detail test

A form stays in the base only when removing it would change the building's primary silhouette or
break the continuity of a load-bearing architectural mass. A form becomes a shared attachment
when it has its own functional identity, material break, replacement seam or plausible mounting
interface. Large buttresses merged continuously into a wall may remain structural; a bolt-on
brace fairing does not.

When uncertain, separate it. A slightly plain base is recoverable during assembly; baked-in noisy
detail defeats the purpose of the pipeline.

## Generation sequence

1. Lock the final concept revision.
2. Inventory every detachable visible detail and map it to exact shared IDs.
3. Resolve or record all shared-library gaps.
4. Produce the textured body-only concept and a socket schedule.
5. Produce one consistent textured four-view body-only reference set.
6. Generate and clean the base mesh.
7. Optionally refine or repair the approved base texture from the final concept; reject painted-on
   shared details and preserve geometry.
8. Generate or model each missing shared component in isolation, once.
9. Assemble shared meshes onto the base using the socket schedule.
10. Compare the dressed assembly with the locked final concept and sign off.

For the trial, Art Forge reads `art-forge-assembly-v1` JSON scenes. Each scene defines unique source
assets once, their target metre envelopes, and a list of reusable instances with position and
rotation. The viewer normalizes and instances them without changing the source GLBs. Saved preview
transforms become the starting receiver-coordinate schedule; they are not production approval by
themselves.

Texture the base and attachments independently according to
[`material-assembly-pipeline.md`](material-assembly-pipeline.md). Shared components keep their own
reusable UVs and materials; the base receives only large architectural material zones.
