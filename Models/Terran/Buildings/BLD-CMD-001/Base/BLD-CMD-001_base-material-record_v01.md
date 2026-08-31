# BLD-CMD-001 base material record v01

Status: **rejected experiment — do not use**

- Geometry source: `BLD-CMD-001_base_hq_v01.glb`
- Textured output: `BLD-CMD-001_base_textured_v01.glb`
- Material: `MAT-TER-001_ARMOUR`
- UV channel: existing `TEXCOORD_0`
- Embedded maps: base colour, metallic-roughness, normal, emission
- Geometry preserved: 1,038,641 vertices; 1,997,976 triangles

The material applicator changed only the GLB material/images. It did not alter geometry, normals,
UV coordinates, scale or transforms. The original Meshy source remains untouched.

Visual review on 2026-08-31 rejected this output. A seamless material tile was applied across the
base's unique baked UV atlas, producing uniform white surface noise and losing the concept's
off-white armour, graphite structure and deliberate panel hierarchy. The trial assembly was restored
to `BLD-CMD-001_base_hq_v01.glb`. Keep this file only as a record of the failed method; do not use it
in the assembly or game.
