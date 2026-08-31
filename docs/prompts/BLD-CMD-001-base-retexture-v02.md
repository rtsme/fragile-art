# BLD-CMD-001 base retexture v02

Status: **complete and visually approved for the trial assembly**

## Inputs

- Geometry source: completed Meshy task `01a05863-1f09-7771-8d5a-625e229ded56`
- Local source record: `Models/Terran/Buildings/BLD-CMD-001/Base/BLD-CMD-001_base_hq_v01.glb`
- Style image: `Concepts/Terran/Buildings/BLD-CMD-001/BLD-CMD-001_concept_v01.png`
- Intended output: `Models/Terran/Buildings/BLD-CMD-001/Base/BLD-CMD-001_base_concept-textured_v02.glb`

## Texture direction read from the approved concept

- Warm, weathered off-white armour panels as the dominant material.
- Graphite structural bands, roof planes, recesses and base trim.
- Very dark blue-black glazing only where the base already has window-like recesses.
- Restrained amber/orange accent paint and emissive points.
- Industrial metal roughness, subtle edge wear and grime; no uniform plaster or concrete noise.

The final concept is a style/material reference, not a geometry instruction. Pipes, railings,
antennae, fans, lamps, doors and access modules remain shared assets. Reject the result if these are
painted onto unrelated shell surfaces or if material zones do not follow the base's existing forms.

## Meshy settings

- Route: Retexture (texture-only)
- Style mode: single image reference
- AI model: latest
- Preserve original UVs: yes
- PBR: yes
- Texture resolution: 4k
- Remove lighting from style image: yes
- Target format: GLB

## Result

- Retexture task: `01a058c6-e9b3-7063-ab33-36449c7bbc8d`
- Credits consumed: 10
- GLB size: 103,215,664 bytes
- Downloaded PBR maps: 4
- Geometry preserved: 1,038,641 vertices; 1,997,976 triangles

Art Forge review checked front, side and rear coverage. The result follows existing base forms with
off-white armour, graphite recesses and dark glazing. No obvious pipes, railings, antennae, fans or
dish were painted onto unrelated surfaces. This output is active in the v04 trial assembly.
