# Art Forge

Art Forge is a standalone local browser and 3D viewer for the Fragile Art repository. It can also
submit multi-view jobs to Meshy. **Modly is optional** and is the current adapter for invoking a
configured local generation model.

## Start

Install Python 3.12+ and, from the repository root, optionally install the authoring helpers:

```powershell
python -m pip install -r requirements-tools.txt
```

Double-click `Art Forge.bat`, or run `python tools/art-forge/forge.py`. The launcher accepts either
the `python` command or the Windows `py -3.12` launcher. The app opens at
`http://127.0.0.1:8770/`.

Without Modly installed:

- repository browsing works
- GLB/GLTF discovery and the 3D viewer work
- Meshy generation works when `MESHY_API_KEY` or the gitignored `meshy.key` is configured
- the Modly-backed Local generator is disabled and labelled unavailable

## Meshy key

Create a key in [Meshy API settings](https://www.meshy.ai/settings/api). Meshy displays the value
only once. Configure Art Forge with either a gitignored local file:

```powershell
Copy-Item tools/art-forge/meshy.key.example tools/art-forge/meshy.key
notepad tools/art-forge/meshy.key
```

or a session-only environment variable:

```powershell
$env:MESHY_API_KEY = "msy_your_key_here"
python tools/art-forge/forge.py
```

The key file contains only the key on one line. Never commit keys, prompt records containing keys,
or Meshy's temporary signed download URLs. Meshy submission is paid; selecting a generator does not
spend credits, but starting a generation/retexture job does.

To inspect the first shared object, open:

```text
Models/Terran/Shared/TER-GLZ-BND-M
```

Then click `TER-GLZ-BND-M_hq_v01.glb` in the **Meshes in this folder** section.

## Assembly preview

Art Forge discovers files ending in `.assembly.json` and lists them under **Assemblies in this
folder**. An assembly keeps the source GLBs separate, loads each unique source once, and reuses it
for every placed instance. Production-envelope sizes are applied in the viewer; the original GLBs
are never rescaled or merged on disk.

To open the Command Centre trial:

```text
Models/Terran/Buildings/BLD-CMD-001
```

Click **BLD-CMD-001 Command Centre — v04 trial assembly**. The first load reads twelve high-detail
source GLBs, so it can take a moment. The Parts panel provides:

- a selector for all 49 placed instances
- position and rotation editing in metres/degrees
- production-envelope size controls
- per-instance visibility
- **Save layout**, which writes the transforms back to the `.assembly.json` file

Double-click a visible part to select it directly. Wireframe, grid, spin and camera reset work for
both single meshes and assemblies.

## Concept-conditioned retexturing

`run-meshy-retexture-cli.py` sends an existing Meshy model through the texture-only API using one
approved concept image as its style reference. It preserves the original UV layout by default,
requests PBR maps and a GLB, and does not regenerate the geometry.

```powershell
python tools/art-forge/run-meshy-retexture-cli.py `
  --input-task-id <completed-image-to-3d-task-id> `
  --style-image Concepts/Terran/Buildings/BLD-CMD-001/BLD-CMD-001_concept_v01.png `
  --output Models/Terran/Buildings/BLD-CMD-001/Base/BLD-CMD-001_base_concept-textured_v02.glb
```

Keep shared decorations out of the base geometry. After each retexture, inspect the result for
painted-on details copied from the concept before activating it in an assembly.

## Optional Modly integration

Modly is a separate checkout/runtime. Install it according to that repository's instructions, then
connect it for the current PowerShell session:

```powershell
$env:MODLY_DIR = "D:\Tools\modly"
$env:MODLY_DATA = "D:\ArtCache\modly-data"
$env:MODLY_API_URL = "http://127.0.0.1:8765"
$env:MODLY_MODEL_ID = "hunyuan3d-mini/generate"
python tools/art-forge/forge.py
```

Art Forge enables Local only when `<MODLY_DIR>/tools/modly-cli/agent.py` and
`<MODLY_DIR>/api/.venv/Scripts/python.exe` both exist. It starts the API when needed and writes the
backend log to `<MODLY_DATA>/backend.log`. No Modly configuration is needed for viewing or Meshy.
`MODLY_MODEL_ID` is not restricted to Hunyuan3D Mini; it selects any compatible model exposed by
that Modly installation. Available models and feasible resolution depend on the contributor's GPU,
VRAM and backend. NVIDIA/CUDA machines may expose different or larger options than AMD/ROCm systems.

Art Forge currently requests geometry-only output from its local adapter. Contributors using a
different local application may export GLB/GLTF into `Models/` and inspect it in Art Forge without a
direct adapter. Record the generator, model/version, settings and hardware in the job record. Every
local output follows the same scale, geometry, receiver and approval gates and is not automatically
production-ready.

For the complete contributor and new-race workflow, read
[`docs/new-race-production-guide.md`](../../docs/new-race-production-guide.md).
