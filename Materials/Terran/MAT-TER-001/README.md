# MAT-TER-001 — Terran architectural material library

Status: **v01 generated and active for base-model previews**

This library provides reusable, seamless 2048×2048 PBR materials for undecorated Terran building
shells. It deliberately contains no doors, windows, vents, panel seams, bolts, markings or other
shared-asset detail.

## Material sets

| Folder | Intended use | Metallic | Roughness |
|---|---|---:|---:|
| `armour/` | warm off-white ceramic-coated structural armour | 0.02 | 0.70 |
| `graphite/` | exposed dark structural steel | 0.78 | 0.56 |
| `concrete/` | foundations and heavy ground-contact masses | 0.00 | 0.88 |
| `amber/` | restrained faction/safety accents | 0.02 | 0.66 |

Each folder contains base colour, tangent-space normal, glTF metallic-roughness and black emission
maps plus `material.json`. Opposite texture edges are identical, so the maps tile without seams.

`Source/` retains the generated base-colour sources. Run
`tools/materials/build-terran-pbr.py` to rebuild the power-of-two PBR sets. Use
`tools/materials/apply-glb-material.py` to embed one set into a UV-mapped GLB without touching its
geometry.

The Command Centre source mesh currently exposes one material slot, so v01 applies armour across
the full shell. Graphite, concrete and amber zones require cleaned topology/material assignments;
they should not be faked as unique painted details in the base-colour map.
