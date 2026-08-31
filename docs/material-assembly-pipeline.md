# Modular material and texturing pipeline

Status: **active trial; concept-conditioned Meshy retexture approved for the BLD-CMD-001 base**.

The generated base shell and shared detail meshes are textured independently. They meet only at
assembly time. This is the material equivalent of the split geometry pipeline: large building
surfaces stay efficient, and a door or vent looks identical everywhere it is reused.

## What happens to generated textures

Meshy PBR output may be retained as the standalone textured base when it passes geometry and
texture review. That makes the undecorated building useful in-engine before shared attachments are
placed. It is still a source asset: generated lighting, implausible painted detail and noisy
microdetail must be rejected or removed during cleanup, and engine-specific glass/emission remain
downstream concerns.

For the accepted route, submit the already approved base to Meshy's texture-only retexture pass,
preserve its original UVs, request PBR/4K and use the locked final concept only as a material/style
reference. The concept is not a geometry instruction. Review every face for invented or painted-on
attachments before approval.

## Base-building materials

The base shell receives only large architectural material zones:

- painted structural steel
- exposed dark steel and frame metal
- warm off-white ceramic/armour panels
- concrete or foundation material where required
- broad dirt, wear and colour-variation masks

There are two valid downstream routes after source generation:

1. **Concept-conditioned unique PBR:** retain the reviewed Meshy retexture as a usable standalone
   base and prototype/game candidate. It must follow existing forms and contain no painted fake
   shared details.
2. **Authored modular material pass:** after cleanup creates intentional material zones and a
   suitable unwrap, use shared tileables, a race trim sheet and broad masks. Material slots or
   vertex colours select armour, frame, foundation and wear zones.

A small unique mask may control large-scale weathering or faction colour placement. Reserve a
non-overlapping lightmap UV channel if the engine lighting workflow requires one.

Do not apply a seamless tile image directly to an AI model's existing unique baked UV atlas. UV
islands will sample unrelated pieces of the tile and destroy material hierarchy. A tile/trim route
requires a deliberate unwrap and explicit material-zone assignment. Do not unwrap a 70 m building
into one giant unique authored colour texture; tiling/trims provide production surface resolution
and unique masks provide variation.

## Shared-component materials

Every reusable component owns its UVs and references a small shared Terran material set. Component
instances reuse the same mesh and textures across all buildings.

- frames and housings use the Terran painted-metal/armour materials
- pipe and mechanical inserts use the dark exposed-metal material
- `TER-GLZ` uses one opaque near-black glazing material; reflections and tint are engine settings
- `TER-LGT` uses an inactive housing material plus a separate optional emissive material
- hazard accents use a shared amber material or decal, not unique baked colour per building

Normal, ambient-occlusion, roughness and metallic information is baked per shared component when
needed. Contact shadow between a component and its parent is not baked into the base, because the
same base receiver may accept a different component later.

## Assembly and export

1. Clean and UV the base shell.
2. Assign base tileables, trims and broad masks.
3. Clean, UV and texture each shared component once.
4. Instance components onto the base sockets without joining their authoring meshes.
5. Add building-specific decals, numbers, hazard markings and controlled wear after assembly.
6. Add glass reflections and light emission in-engine.
7. Export the assembled hierarchy to glTF/GLB while preserving shared material names.

The authoring source remains modular even if an optimization pass later combines meshes or packs
textures for runtime. Any atlas is a generated delivery artifact, not the master texture source.

## Command Centre trial

For `BLD-CMD-001`, the base should read as a clean but deliberately plain fortress shell before
attachments. Its unique visual richness comes from the shared glazing, entrance, antenna, vent,
pipe, access, light and panel meshes listed in its assembly manifest. This gives us one place to
correct a material or asset and lets every future Terran building inherit the fix.

`BLD-CMD-001_base_textured_v01.glb` is a rejected experiment. Applying one seamless armour tile to
the existing unique UV atlas produced uniform white/noisy plaster and erased the intended armour,
graphite and glazing hierarchy. It remains only as a failure record and must not be used.

`BLD-CMD-001_base_concept-textured_v02.glb` is the active trial base. Meshy retextured the approved
geometry from the locked final concept while preserving the original UVs and geometry. Art Forge
review passed its front, side and rear coverage with no obvious shared decorations painted onto
unrelated shell surfaces. The task and settings are recorded in
`Models/Terran/Buildings/BLD-CMD-001/Base/BLD-CMD-001_base-retexture-job_v02.md`.
