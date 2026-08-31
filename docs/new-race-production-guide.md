# Starting a new race

This is the contributor-facing production contract for adding a race/faction to Fragile Art. Read
it before generating concepts or spending Meshy credits. The Terran Command Centre
(`BLD-CMD-001`) is the reference implementation.

The central rule is simple: **the approved concept is the final dressed target; generation builds
the structural base and reusable details separately.**

## 1. Workstation setup

### Required

- Windows 10/11 for the supplied Art Forge launcher. Art Forge itself also runs anywhere Python
  and a browser are available.
- Git and [Git LFS](https://git-lfs.com/).
- 64-bit Python 3.12 or newer.
- A modern browser with WebGL 2 support.
- Disk space for LFS assets and high-detail source meshes. A single 4K Meshy source can exceed
  100 MB once its PBR maps are included.

Clone with LFS enabled:

```powershell
git lfs install
git clone <fragile-art-repository-url>
cd fragile-art
python -m pip install -r requirements-tools.txt
```

`requirements-tools.txt` installs Pillow and NumPy for reference validation/image preparation and
Trimesh for procedural kit utilities. Art Forge's browser, viewer and Meshy client use the Python
standard library and can still start if those optional packages are not installed.

Start Art Forge by double-clicking `tools/art-forge/Art Forge.bat`, or run:

```powershell
python tools/art-forge/forge.py
```

It opens `http://127.0.0.1:8770/`. Set `FORGE_PORT` before launch if that port is occupied. Set
`ART_ROOT` only when the tool lives outside this repository.

### Meshy cloud setup (Easiest but optional, costs money though so try local first)

Meshy is the production source-generation and retexturing backend. It is paid and every submit
uses the Meshy account associated with the key.

1. Create a Meshy account and API key in [Meshy API settings](https://www.meshy.ai/settings/api).
   Meshy only displays a new key once, so store it securely.
2. Choose one configuration method:

   Repository-local key file (easiest on a dedicated art workstation):

   ```powershell
   Copy-Item tools/art-forge/meshy.key.example tools/art-forge/meshy.key
   notepad tools/art-forge/meshy.key
   ```

   Replace the example with the key only, on one line. `meshy.key` is gitignored.

   Session-only PowerShell environment variable (preferred on shared machines):

   ```powershell
   $env:MESHY_API_KEY = "msy_your_key_here"
   python tools/art-forge/forge.py
   ```

3. Confirm Art Forge shows `Meshy key found` in its header.

Never place a real key in a prompt record, manifest, script, screenshot, commit or issue. Revoke a
key in Meshy immediately if it is exposed. Meshy's authentication and key-handling guidance is at
[docs.meshy.ai/en/api/authentication](https://docs.meshy.ai/en/api/authentication).

### Optional local generation with Modly or another local model (Freeeee)

Art Forge does **not** require Modly. Without it, repository browsing, reference checks, GLB/GLTF
viewing, assembly editing and Meshy all work normally. Local generation is useful for massing tests
and may become a production source when a model and workstation can meet the same approval gates.

Modly is a separate checkout and runtime. Install and initialize it using that repository's own
setup instructions. Art Forge expects this layout:

```text
<MODLY_DIR>/
  tools/modly-cli/agent.py
  api/.venv/Scripts/python.exe

<MODLY_DATA>/
  models/
  workspace/
  ext/
```

Connect an existing installation for the current PowerShell session:

```powershell
$env:MODLY_DIR = "D:\Tools\modly"
$env:MODLY_DATA = "D:\ArtCache\modly-data"
$env:MODLY_API_URL = "http://127.0.0.1:8765"
$env:MODLY_MODEL_ID = "hunyuan3d-mini/generate"
python tools/art-forge/forge.py
```

Art Forge enables `Local` only when both `tools/modly-cli/agent.py` and
`api/.venv/Scripts/python.exe` exist. It starts Modly's API when needed and writes its backend log to
`<MODLY_DATA>/backend.log`.

`MODLY_MODEL_ID` selects the compatible model exposed by that installation; the shown Hunyuan3D
Mini ID is a default, not a pipeline requirement. Hardware capabilities vary substantially:

- NVIDIA/CUDA workstations may expose different or larger reconstruction models and texture
  pipelines, subject to VRAM and driver requirements;
- AMD/ROCm systems may use a different supported set;
- CPU/Apple/other backends may be usable when their local tool can export a reviewable GLB/GLTF.

Art Forge's current Modly adapter intentionally requests geometry-only output. A model run through
another local application can still enter the repository by exporting GLB/GLTF into the appropriate
`Models/` folder and opening it in Art Forge. Record the generator, exact model/version, settings,
hardware/backend and output provenance in the job record. No local output is approved merely because
it ran on-device; it must pass the same geometry, scale, receiver, texture and runtime gates.

## 2. Define the race before defining assets

Choose and record:

- display name, folder name and unique three-letter uppercase race code, for example `Terran` / `TER`;
- shape language and primary silhouettes;
- material palette and controlled accent colours;
- construction grid, scale assumptions and wear language;
- initial category list and one anchor/hero building;
- shared-component families needed across multiple concepts.

Create folders only when the corresponding production stage starts; do not commit empty trees.

```text
Concepts/<Race>/
  <race>-concept-manifest-v01.md
  Buildings/<Asset ID>/
  Shared/<RACE>-KIT-001/

References/<Race>/
  Buildings/<Asset ID>/Base/
  Shared/<Component ID>/

Materials/<Race>/
  MAT-<RACE>-001/

Models/<Race>/
  Buildings/<Asset ID>/Base/
  Shared/<Component ID>/
```

Use the race manifest to list every concept, current approved revision, dimensions, status and
known shared-asset dependencies. Do not encode mutable status only in filenames.

## 3. Naming and versioning

- Asset IDs are uppercase and stable: `<CATEGORY>-<ROLE>-NNN`, for example `BLD-CMD-001`.
- Shared IDs start with the race code and identify an exact interchangeable object, for example
  `<RACE>-VNT-FAN-L`. A family code such as `<RACE>-VNT` is not an assembly-ready ID.
- Standard sizes use `S`, `M`, `L` only when the production specification defines their envelopes.
- Image and document revisions use `_vNN`, starting at `_v01`.
- Never overwrite an approved revision. Add a new version and update the manifest.
- Use metres everywhere. Dimensions are written **width × depth × height**.
- Origins for reusable components are centred on the mounting footprint and lie on the mounting
  plane. Forward orientation must match the front reference.
- The primary construction grid is 0.5 m; detail may use 0.25 m. Gameplay-relevant connections
  remain on the construction grid.

Standard socket envelopes:

| Socket | Envelope | Intended use |
|---|---:|---|
| S1 | 0.5 × 0.5 m | light/detail |
| S2 | 1 × 1 m | equipment/conduit |
| S3 | 2 × 2 m | structural/service |
| S4 | 4 × 4 m | heavy/docking |

## 4. Produce the race anchor asset

Start with one building that expresses the race clearly. Complete the full pipeline before scaling
out; it will expose missing component families and material rules cheaply.

### Stage A — approved final concept

Create:

```text
Concepts/<Race>/Buildings/<Asset ID>/<Asset ID>_concept_v01.png
docs/prompts/<Asset ID>-concept-v01.md
```

The concept is the immutable target for that approved revision. It may show the dressed building
and every reusable detail. It is authoritative for silhouette, hierarchy, palette and detail
distribution. It is **not** a geometry-generation input.

Concept-generation rules:

1. Use solid, enclosed, watertight-looking masses and a closed silhouette.
2. No open lattice, scaffolds, trusses, wires, chains or free-standing thin elements.
3. No feature smaller than roughly 2% of the asset's longest dimension.
4. Prefer broad planes, deep steps and bold chamfers over dense greeble.
5. Thin shells such as dishes require an obvious thick rim and chunky mount, or become shared
   hand-modelled parts.
6. Glass is flat, opaque and near-black. No visible interiors, reflections or transparency.
7. Surfaces are matte to satin. No chrome, mirrors or high-gloss highlights.
8. Painted markings must read as flat decals, not shaded fake geometry.
9. Use neutral, even studio lighting; no cast ground shadow, rim lighting or baked ambient occlusion.
10. No emissive glow, environment, people, vehicles, text or props unless they are the subject.

The rationale and observed failure cases are in
[`concept-rules-for-3d.md`](concept-rules-for-3d.md).

### Stage B — shared-asset audit and assembly manifest

Before removing anything from the concept, inventory every visible detachable detail:

```text
Concepts/<Race>/Buildings/<Asset ID>/<Asset ID>_assembly-manifest_v01.md
```

For every door, window, vent, fan, tank, pipe, antenna, dish, light, railing, stair, ramp, equipment
box, panel and replaceable fitting, record:

- exact shared-component ID;
- quantity, including rear/hidden faces once references exist;
- physical envelope and S1-S4 receiver;
- build route: `R` (safe to reconstruct in isolation) or `H` (manual/procedural modelling);
- placement intent and orientation;
- whether it already exists or is `NEW SHARED ASSET REQUIRED`.

Do not absorb a missing component into the base. Add it to the race kit or revise the concept to use
an approved existing part. A component may be scaled only within ±10%; choose or define another size
outside that range.

### Stage C — body-only source

Create:

```text
Concepts/<Race>/Buildings/<Asset ID>/Base/<Asset ID>_base-concept_v01.png
Concepts/<Race>/Buildings/<Asset ID>/Base/README.md
```

Keep foundations, load-bearing walls, roof masses, towers, large overhangs, deep structural
setbacks and silhouette-defining buttresses. Remove every detachable detail and replace attachment
locations with a closed recess, flush pad or simple S1-S4 receiver. The base should look deliberately
plain and unfinished.

Structure-versus-detail test: if removing a form breaks the primary silhouette or continuity of a
load-bearing mass, it stays in the base. If it has its own function, replacement seam, material break
or mounting interface, it is separate. When uncertain, separate it.

### Stage D — orthographic reference package

Generate **one** 2×2 sheet showing the identical object from front, back, left and right, then crop
the tiles. Do not generate four independent images.

```text
References/<Race>/Buildings/<Asset ID>/Base/
  <Asset ID>_base_reference-sheet_v01.png
  <Asset ID>_base_front_v01.png
  <Asset ID>_base_back_v01.png
  <Asset ID>_base_left_v01.png
  <Asset ID>_base_right_v01.png
```

Reference-generation rules:

1. True orthographic projection; no perspective or foreshortening.
2. Identical canvas dimensions, camera distance, lighting, scale and centre.
3. Silhouette-height variation across all upright views stays under 3%. Width variation is checked
   within opposing pairs—front/back and left/right—not front against side. A 10% difference within
   one of those valid comparisons is a hard failure.
4. Subject-centre drift under 2% of the canvas.
5. Every view describes exactly the same geometry and asymmetry.
6. Neutral background and flat lighting, with no ground shadow.
7. Crop from a single generated sheet, with no creative repainting per view.
8. Save and submit in this exact order: **front, back, left, right**. Front is primary.
9. Top/bottom are optional authoring references only; Meshy's multi-image job accepts at most four
   inputs in this pipeline.

Validate before spending credits:

```powershell
python tools/check-views.py `
  References/<Race>/Buildings/<Asset ID>/Base/<Asset ID>_base_front_v01.png `
  References/<Race>/Buildings/<Asset ID>/Base/<Asset ID>_base_back_v01.png `
  References/<Race>/Buildings/<Asset ID>/Base/<Asset ID>_base_left_v01.png `
  References/<Race>/Buildings/<Asset ID>/Base/<Asset ID>_base_right_v01.png
```

Warnings require visual review. A failing check blocks generation.

### Stage E — shared component packages

Each missing reusable component gets its own concept/specification and isolated four-view package:

```text
Concepts/<Race>/Shared/<RACE>-KIT-001/
References/<Race>/Shared/<Component ID>/
Models/<Race>/Shared/<Component ID>/
```

Shared-generation rules:

1. One object per request; never generate a sheet of unrelated objects as one 3D job.
2. Use the same front/back/left/right consistency rules as a base.
3. `R` parts must be closed, chunky and above the 2% detail floor when isolated.
4. `H` parts are manual/procedural even if an AI output is retained as a reference experiment.
5. Connection faces, sockets and envelopes are never rescaled independently.
6. Test each cleaned component on a real receiver before library approval.
7. Reuse the exact approved mesh and textures across buildings; do not mint asset-local duplicates.

Thin repetitive forms such as railings, ladders, catwalks and pipe runs are good procedural/manual
candidates. `tools/kitgen.py` demonstrates the convention; run `python tools/kitgen.py --list`.

### Stage F — generate the structural base

Use Art Forge or the CLI. CLI example:

```powershell
python tools/art-forge/run-meshy-cli.py `
  References/<Race>/Buildings/<Asset ID>/Base/<Asset ID>_base_front_v01.png `
  References/<Race>/Buildings/<Asset ID>/Base/<Asset ID>_base_back_v01.png `
  References/<Race>/Buildings/<Asset ID>/Base/<Asset ID>_base_left_v01.png `
  References/<Race>/Buildings/<Asset ID>/Base/<Asset ID>_base_right_v01.png `
  --output Models/<Race>/Buildings/<Asset ID>/Base/<Asset ID>_base_hq_v01.glb `
  --texture-resolution 4k
```

Mesh-generation rules:

1. Re-run the reference check immediately before submission.
2. Confirm the output path, estimated cost and front-first order before submitting.
3. Generate the body-only base, never the dressed final concept.
4. Use Meshy's latest model, PBR and 4K for a maximum-detail source.
5. Leave remesh **off** for the source; remeshing/decimation is a later inspected step.
6. Never assume AI scale. Set and verify 1 unit = 1 metre during cleanup.
7. Inspect every side for doubled forms, melted edges, accidental openings, non-manifold geometry
   and receiver damage.
8. Generated meshes are source assets, not automatically game-ready. Retopology/decimation, LODs,
   collision, pivots/origins, scale, material cleanup and engine validation remain required.

Raw `*_hq_*`, `*_ai_*` and `*_experiment_*` outputs are gitignored. After approval, promote the
mesh to a clearly versioned non-temporary filename or force-add the reviewed source deliberately.
Never force-add an unreviewed generation merely to make an assembly portable.

### Stage G — texture the base from the approved concept

The proven trial route is Meshy's texture-only retexture pass. It uses the approved final concept as
a **style/material reference**, while preserving the already generated geometry and original UVs.
This is the only permitted use of the dressed concept in the generation pipeline.

```powershell
python tools/art-forge/run-meshy-retexture-cli.py `
  --input-task-id <completed-base-task-id> `
  --style-image Concepts/<Race>/Buildings/<Asset ID>/<Asset ID>_concept_v01.png `
  --output Models/<Race>/Buildings/<Asset ID>/Base/<Asset ID>_base_concept-textured_v02.glb `
  --texture-resolution 4k `
  --ai-model latest
```

Texture-generation rules:

1. Retexture only after geometry review; do not hide geometry faults with colour.
2. Preserve original UVs for a Meshy-generated source unless a deliberate new unwrap exists.
3. Request PBR, 4K and lighting removal.
4. Treat the concept as palette/material language, not permission to invent geometry.
5. Reject painted-on fake doors, glazing, vents, pipes, railings, antennae or panels where the base
   has no corresponding form/receiver.
6. Inspect front, back, both sides and roofs; one attractive hero angle is not approval.
7. Geometry statistics and transforms must remain unchanged across a texture-only pass.
8. Keep base and shared-component materials independent. Shared components own reusable UVs and
   textures.
9. Do not apply a seamless material image directly across a unique baked UV atlas. The rejected
   `BLD-CMD-001_base_textured_v01.glb` experiment produced uniform noisy plaster and lost deliberate
   material zones.
10. Engine glow, glass response and decals are controlled downstream, not baked as concept lighting.

See [`material-assembly-pipeline.md`](material-assembly-pipeline.md) for the modular material
contract.

### Stage H — assemble and compare

Create an Art Forge scene beside the building models:

```text
Models/<Race>/Buildings/<Asset ID>/<Asset ID>_assembly_v01.assembly.json
```

Assembly rules:

1. Use `art-forge-assembly-v1` and metres.
2. Declare each unique source asset once and reuse it through instances.
3. Record the intended production envelope for every source.
4. Place components on manifest receivers; do not eyeball against unrelated surface detail.
5. Do not merge or destructively rescale source GLBs in the preview.
6. Saved Art Forge transforms are a receiver-coordinate starting point, not production approval.
7. Every visible detachable item in the final concept must resolve to an exact component instance or
   an explicitly accepted omission.
8. Compare silhouette, hierarchy, material balance and detail distribution against the locked final
   concept from multiple views.
9. Verify every referenced GLB exists and is tracked/promoted before another contributor relies on
   the assembly.

### Stage I — game-ready cleanup and delivery

Before copying an asset to the game repository:

- establish verified metre scale, origin and forward direction;
- retopologize/decimate with an inspected triangle budget;
- create LODs and collision;
- remove hidden/duplicate/non-manifold geometry;
- preserve modular components and stable material names;
- verify UV0/PBR maps and any lightmap UV channel;
- add engine-only glass, emission, decals and controlled effects;
- test the assembled hierarchy in the engine at gameplay camera distance;
- record approval and source task IDs in a model-side job record;
- copy only the runtime artifact to `FragileRemake/apps/godot/assets/structures/`.

## 5. Approval gates

Every generative action also receives a Markdown prompt/job record. Record its input files, exact
prompt or style reference, model/settings, output path, task ID, credits where known, and the review
result. Prompts must state that references describe one fixed object, forbid redesign between views,
and repeat the relevant negative geometry/lighting constraints. Never rely on chat history as the
only production record.

| Gate | Required evidence |
|---|---|
| Race direction | race manifest, palette/material definition, anchor asset selected |
| Final concept | approved version locked; prompt record retained |
| Split plan | exact assembly manifest; every missing detail explicit |
| References | single-set four views; `check-views.py` passes; front-first order |
| Base source | geometry inspected from every side; scale/receivers recorded |
| Shared asset | envelope, origin, socket, direction and receiver-fit verified |
| Texture | PBR maps present; geometry unchanged; no painted fake detail |
| Assembly | exact component IDs; tracked dependencies; multi-view concept comparison |
| Runtime | cleanup, LOD, collision, materials and in-engine review complete |

Nothing advances because a generation completed successfully. Each stage advances because its
review gate passed.

## 6. Commit and repository rules

- Git LFS owns images, meshes, texture maps and the production tracker.
- Never commit `meshy.key`, credentials, signed download URLs or account data.
- Retain prompts, task IDs, settings, costs and review outcomes in Markdown job records.
- Commit approved concepts/references; retain superseded approved revisions that explain a design
  change.
- Raw/rejected generation remains ignored or explicitly marked `rejected — do not use`.
- An assembly may reference only an artifact another contributor can obtain from the repository or
  regenerate from a committed manifest and recorded task settings.
- Do not edit unrelated race assets while onboarding a new race.

When evidence changes a production rule, update the authoritative rule document and name the asset
or failed/successful trial that justified the change. Keep the old job record so the reason is
reviewable; do not silently rewrite rules around an unexplained result.

## 7. Reference implementation

Follow this trail to see one complete trial:

- final target: `Concepts/Terran/Buildings/BLD-CMD-001/BLD-CMD-001_concept_v01.png`
- split manifest: `Concepts/Terran/Buildings/BLD-CMD-001/BLD-CMD-001_assembly-manifest_v01.md`
- body-only source: `Concepts/Terran/Buildings/BLD-CMD-001/Base/`
- base references: `References/Terran/Buildings/BLD-CMD-001/Base/`
- shared packages: `References/Terran/Shared/`
- models/assembly: `Models/Terran/Buildings/BLD-CMD-001/`
- successful retexture record: `Models/Terran/Buildings/BLD-CMD-001/Base/BLD-CMD-001_base-retexture-job_v02.md`

The Command Centre proves the workflow, not every final production decision. Its v04 assembly
placement is still a trial and its generated source geometry still requires game-mesh cleanup.
