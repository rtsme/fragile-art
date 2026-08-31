# TER-GLZ-BND-M — Meshy generation job v01

Status: **Meshy source generated; visual/geometry review pending**

## Ordered inputs

1. `../../../../References/Terran/Shared/TER-GLZ-BND-M/TER-GLZ-BND-M_front_v01.png`
2. `../../../../References/Terran/Shared/TER-GLZ-BND-M/TER-GLZ-BND-M_back_v01.png`
3. `../../../../References/Terran/Shared/TER-GLZ-BND-M/TER-GLZ-BND-M_left_v01.png`
4. `../../../../References/Terran/Shared/TER-GLZ-BND-M/TER-GLZ-BND-M_right_v01.png`

## Meshy settings

- endpoint: multi-image-to-3D
- AI model: latest
- target format: GLB
- texture: enabled
- PBR: enabled
- texture resolution: 4K
- remesh: disabled for maximum source detail
- scale after cleanup: 4 × 0.5 × 1.5 m
- target output: `TER-GLZ-BND-M_hq_v01.glb`

Generated PBR maps are review/reference material. Final UVs and materials follow
`docs/material-assembly-pipeline.md` after cleanup.

## Completion record

- Meshy task ID: `01a057df-974d-7056-8dc3-344fc9a16d6e`
- credits consumed: 30
- output downloaded: `TER-GLZ-BND-M_hq_v01.glb` (76.6 MB)
- texture maps downloaded: 5 files in `TER-GLZ-BND-M_hq_v01_textures/` (51.6 MB total)
- GLB inspection: glTF 2.0; one mesh/primitive; 1,010,182 vertices; 1,958,274 triangles;
  one material; four embedded texture/image bindings

This is the maximum-detail source mesh. It is not approved or game-ready until visual inspection,
scale correction, retopology/decimation, UV/material cleanup and receiver-fit testing are complete.
