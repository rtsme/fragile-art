# Fragile Art

Art production for the Fragile Frontiers remake: approved concepts, orthographic reconstruction
references, generated/cleaned meshes, modular materials and the tools that connect them.

**This repository is the art pipeline.** The game repository contains only the final runtime assets
it loads. Everything upstream—prompts, concepts, source references, Meshy tasks, source meshes and
assembly records—lives here.

## Start here

New contributor or starting a new race? Read
**[`docs/new-race-production-guide.md`](docs/new-race-production-guide.md)** first. It contains the
complete workstation setup, Meshy/local-backend configuration, naming contract, generation rules,
approval gates and end-to-end race workflow.

Quick workstation setup:

```powershell
git lfs install
git clone <fragile-art-repository-url>
cd fragile-art
python -m pip install -r requirements-tools.txt
python tools/art-forge/forge.py
```

On Windows you can instead double-click `tools/art-forge/Art Forge.bat`. Python 3.12+ is required.
Art Forge opens at `http://127.0.0.1:8770/`.

## Configure Meshy

Create a key in [Meshy API settings](https://www.meshy.ai/settings/api), then use one of these
methods.

Repository-local key file:

```powershell
Copy-Item tools/art-forge/meshy.key.example tools/art-forge/meshy.key
notepad tools/art-forge/meshy.key
```

Put the key only on the first line. `meshy.key` is gitignored.

Or set it for the current PowerShell session:

```powershell
$env:MESHY_API_KEY = "msy_your_key_here"
python tools/art-forge/forge.py
```

Never commit or paste a real key into a prompt/job record. Meshy submissions are paid; confirm the
inputs and output path before generating.

## Optional local generation

The viewer, repository browser, reference checks, assembly editor and Meshy backend do not require
Modly. Art Forge's current local adapter talks to Modly, but the model behind it is configurable.
Install Modly separately and point Art Forge at it:

```powershell
$env:MODLY_DIR = "D:\Tools\modly"
$env:MODLY_DATA = "D:\ArtCache\modly-data"
$env:MODLY_API_URL = "http://127.0.0.1:8765"
$env:MODLY_MODEL_ID = "hunyuan3d-mini/generate"
python tools/art-forge/forge.py
```

Art Forge expects `<MODLY_DIR>/tools/modly-cli/agent.py` and
`<MODLY_DIR>/api/.venv/Scripts/python.exe`. `MODLY_MODEL_ID` selects whichever compatible model the
local installation exposes; Hunyuan3D Mini is only the default. NVIDIA/CUDA workstations may support
different or larger models than AMD/ROCm machines, depending on VRAM, drivers and the local backend.
An external local tool may also generate a GLB for import even when Art Forge has no adapter for it.
Local output still passes the same geometry, scale and provenance gates. Full setup details are in the
[new-race guide](docs/new-race-production-guide.md#optional-local-generation-with-modly-or-another-local-model).

## Repository layout

```text
Concepts/<Race>/<Category>/<Asset ID>/       approved targets, Base/, assembly manifest
References/<Race>/<Category>/<Asset ID>/     four-view modelling/generation inputs
References/<Race>/Shared/<Component ID>/     isolated reusable-object inputs
Materials/<Race>/                            race material definitions and maps
Models/<Race>/<Category>/<Asset ID>/         generated/cleaned bases and assemblies
Models/<Race>/Shared/<Component ID>/         reusable detail meshes
docs/prompts/                                prompt and generation job records
tools/art-forge/                             local UI, viewer, Meshy/local clients
```

Images, meshes, texture maps and the production tracker use Git LFS. Raw generator outputs are
gitignored until reviewed and deliberately promoted.

## Production pipeline

```text
race direction
  → approved dressed concept
  → exact shared-asset audit
  → body-only base source
  → one consistent four-view reference set
  → base + isolated shared-object generation
  → concept-conditioned base retexture
  → modular assembly
  → cleanup, LOD/collision and game export
```

The approved dressed concept is the final visual target. It is never used to generate the base
geometry. The base is generated from body-only references; doors, windows, vents, tanks, pipes,
antennae, lights, railings, stairs and other detachable details are independent shared assets. The
final concept may be supplied later only as a texture/style reference for the completed base.

## Non-negotiable generation rules

These rules apply to every race. The full contract and examples are in the
[new-race production guide](docs/new-race-production-guide.md); reconstruction rationale is in
[`concept-rules-for-3d.md`](docs/concept-rules-for-3d.md).

1. Lock and version the final concept; never overwrite an approved revision.
2. Generate only body-only structural bases. Every detachable detail is a shared component.
3. Map every visible detail to an exact component ID and receiver before base generation. Missing
   parts are `NEW SHARED ASSET REQUIRED`, never improvised into the base.
4. Use solid enclosed volumes, closed silhouettes, broad planes and deep breaks. No open lattice,
   wires, transparent surfaces or geometry smaller than roughly 2% of the asset's longest dimension.
5. Glass is flat, opaque and dark; materials are matte/satin; concepts have neutral light, no cast
   shadow, reflection, environment or emissive glow.
6. Generate one orthographic turnaround sheet and crop it into identical front/back/left/right
   files. Do not generate four independent views.
7. Same canvas, scale and centre in every view: height variation across all views and width
   variation within opposing front/back or left/right pairs stay under 3%; centre drift stays under
   2%; 10% variation is a hard fail. Run `tools/check-views.py` before spending credits.
8. Meshy input order is **front, back, left, right**; front is always primary. Maximum four images.
9. One isolated shared object per 3D request. `R` parts may be reconstructed in isolation; `H` parts
   are manual/procedural. Neither is baked into a parent base.
10. Use 1 unit = 1 metre, the 0.5 m construction grid and standard S1-S4 receivers. Never rescale a
    component connection face independently.
11. Leave Meshy remesh off for maximum-detail sources. Retopology/decimation is a later reviewed
    operation; generated output is not automatically game-ready.
12. Retexture only after geometry approval. Preserve original UVs, request PBR/4K, and reject any
    painted-on fake doors, windows, pipes, antennae or other shared details.
13. Never apply one seamless material image across a unique baked UV atlas. The Command Centre
    trial proved that this produces uniform surface noise and destroys deliberate material zones.
14. Inspect front, rear, both sides and roof at every geometry, texture and assembly gate.
15. Assembly scenes instance exact shared meshes in metres; preview transforms are not approval.
16. Record prompts, task IDs, cost/settings and review outcomes. Never record secrets or temporary
    signed download URLs.
17. Promote/commit only reviewed artifacts. Every assembly dependency must be tracked or
    reproducible from committed references and a manifest.

## Common commands

Validate a four-view package:

```powershell
python tools/check-views.py <front.png> <back.png> <left.png> <right.png>
```

Generate a maximum-detail base or isolated shared object with Meshy:

```powershell
python tools/art-forge/run-meshy-cli.py `
  <front.png> <back.png> <left.png> <right.png> `
  --output <source.glb> --texture-resolution 4k
```

Retexture an approved base from its final concept without regenerating geometry:

```powershell
python tools/art-forge/run-meshy-retexture-cli.py `
  --input-task-id <completed-base-task-id> `
  --style-image <approved-concept.png> `
  --output <concept-textured-base.glb> `
  --texture-resolution 4k --ai-model latest
```

List procedural kit examples:

```powershell
python tools/kitgen.py --list
```

## Authoritative documents

- [Start a new race](docs/new-race-production-guide.md) — setup, entire workflow and approval gates.
- [Concept rules for 3D](docs/concept-rules-for-3d.md) — reconstruction constraints and failure cases.
- [Shared-asset assembly pipeline](docs/shared-assembly-pipeline.md) — base/detail folder contract.
- [Material and texturing pipeline](docs/material-assembly-pipeline.md) — modular materials and the
  approved concept-conditioned retexture route.
- [Art Forge](tools/art-forge/README.md) — viewer, assembly editor and generation commands.
- `docs/Fragile_Allegiance_Art_Asset_Production_Tracker.xlsx` — asset production status.

## Current reference implementation

`BLD-CMD-001` is the first complete pipeline trial. Its base was generated from body-only four-view
references, retextured from the approved concept without changing geometry, and combined with
separate shared meshes in an editable Art Forge assembly. Its placement and high-detail source
meshes still require production cleanup; use it as a workflow example, not as proof that every
runtime gate has passed.

Finished game-ready meshes are copied into
`FragileRemake/apps/godot/assets/structures/` and committed in the game repository. Upstream source
art remains here.

## Credits

`tools/art-forge/vendor/` bundles [three.js](https://threejs.org) r169 under the MIT licence for the
built-in offline mesh viewer.
