# Fragile Art

Art production for the [Fragile Frontiers](../FragileRemake) remake — concepts, modelling
references, generated meshes, and the tooling that turns one into the other.

**This repo is the pipeline. The game repo holds only what the game loads at runtime.**
Finished, game-ready meshes are copied into `FragileRemake/apps/godot/assets/structures/`
and committed there; everything upstream of that lives here. The split exists because art
binaries are large and churn constantly, and baking them into the game repo's history is
irreversible.

## Structure

- `Concepts/<Faction>/<Category>/<Asset ID>/` — initial 2D concepts and approved design anchors.
- `References/<Faction>/<Category>/<Asset ID>/` — modelling references. Every approved package
  requires **four** standalone files: front, back, left and right. The 3D generator accepts at
  most four reference images and treats the first as the primary view, so front is always
  supplied first. Top and bottom are optional — produce them only when the roof or underside
  carries gameplay-readable detail. A combined tile sheet may be retained as an optional companion.
- `Models/<Faction>/<Category>/<Asset ID>/` — generated meshes and cleaned source files.
- `docs/` — the production tracker (`Fragile_Allegiance_Art_Asset_Production_Tracker.xlsx`),
  the single source of truth for asset status from style gate to final sign-off, and
  [`concept-rules-for-3d.md`](docs/concept-rules-for-3d.md) — **read this before drawing a
  concept.** Constraints the generator imposes on what can be reconstructed: solid enclosed
  volumes, flat opaque glass, no open lattice or thin elements. Every rule names the asset whose
  failure produced it.
- `tools/art-forge/` — Art Forge, the local UI that drives generation.
- `tools/check-views.py` — verifies a set of orthographic references agree with each other
  before you spend credits on them. Art Forge runs it automatically; run it by hand with
  `python tools/check-views.py References/Terran/Buildings/<ASSET-ID>/*.png`.

Use versioned filenames and retain superseded concepts when they document a reviewed design change.

## Large files

Images, meshes and the tracker go through **Git LFS** (see `.gitattributes`). Clone with LFS
installed or the binaries arrive as pointer files:

```bash
git lfs install
git clone <url>
```

Raw generator output (`*_ai_raw_*`, `*_ai_hi*_*`) is **gitignored** — it regenerates in seconds
and would otherwise churn on every parameter change. Commit approved meshes only.

## Generating a mesh

Run `tools/art-forge/Art Forge.bat`, point it at a reference folder, pick the images, forge.
Two backends:

| | Local (Hunyuan3D 2 mini) | Meshy (cloud) |
|---|---|---|
| cost | free | ~30 credits (~$0.60) per textured mesh |
| input | 1 image | up to 4 (first = front) |
| output | ~1–2 M faces, no UVs, no textures | ~40 k faces, quad, UVs, PBR maps |
| use for | fast massing and proportion reference | production assets |

The local backend runs on the AMD GPU through ROCm and is useful for quick iteration, but its
output is a sculpt — it cannot produce crisp mechanical edges, and open lattice structures
(derricks, gantries) come back as solid slabs. Meshy handles both.

Set `MESHY_API_KEY` or put the key in `tools/art-forge/meshy.key` (gitignored).

## Credits

`tools/art-forge/vendor/` bundles [three.js](https://threejs.org) r169 (MIT) for the built-in
mesh viewer, so the tool works offline.
