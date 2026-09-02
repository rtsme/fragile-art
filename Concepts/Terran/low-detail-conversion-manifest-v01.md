# Terran low-detail Meshy conversion — v01

Started 2026-09-02.

## Locked generation rules

- One coherent, watertight-looking asset per concept.
- Preserve the source silhouette and two or three large identity features only.
- Use broad planar masses, thick structural forms, shallow chamfers and minimal rounding.
- Use warm off-white armour, graphite structure, dark blue-black glazing or functional faces, and sparse flat amber accents.
- No railings, guardrails, cables, exposed pipes, antennas, dishes, rods, ladders, fans, fine vents, tiny panels, open frames, floating props or disconnected pieces.
- No geometry continues beneath a building foundation.
- Ships with configurable loadouts remain weapon-neutral, with no fixed guns or visible hardpoints.
- Concept images are generated first. Cardinal front/left/right/back reference sets follow only after concept approval.

## Generated and visually checked

### Ships

| Asset | Low-detail concept | Review |
|---|---|---|
| SHP-TER-001 — Scout | `Ships/SHP-TER-001/LowDetail/SHP-TER-001_low-detail_concept_v01.png` | Pass |
| SHP-TER-002 — Fighter | `Ships/SHP-TER-002/LowDetail/SHP-TER-002_low-detail_concept_v02-clean-airframe.png` | Approved; cardinal set complete |
| SHP-TER-003 — Corvette | `Ships/SHP-TER-003/LowDetail/SHP-TER-003_low-detail_concept_v01.png` | Pass |
| SHP-TER-004 — Frigate | `Ships/SHP-TER-004/LowDetail/SHP-TER-004_low-detail_concept_v01.png` | Pass |
| SHP-TER-005 — Transport | `Ships/SHP-TER-005/LowDetail/SHP-TER-005_low-detail_concept_v01.png` | Pass |
| SHP-TER-006 — Destroyer | `Ships/SHP-TER-006/LowDetail/SHP-TER-006_low-detail_concept_v01.png` | Pass |
| SHP-TER-007 — Cruiser | `Ships/SHP-TER-007/LowDetail/SHP-TER-007_low-detail_concept_v01.png` | Pass |
| SHP-TER-008 — Command Cruiser | `Ships/SHP-TER-008/LowDetail/SHP-TER-008_low-detail_concept_v01.png` | Pass |
| SHP-TER-009 — Colony Ship | `Ships/SHP-TER-009/LowDetail/SHP-TER-009_low-detail_concept_v01.png` | Review identity; possibly too generic beside Transport |
| SHP-TER-010 — Freighter | `Ships/SHP-TER-010/LowDetail/SHP-TER-010_low-detail_concept_v01.png` | Pass |
| SHP-TER-011 — Bomber | `Ships/SHP-TER-011/LowDetail/SHP-TER-011_low-detail_concept_v01.png` | Pass; weapon-neutral |
| SHP-TER-012 — Shuttle | `Ships/SHP-TER-012/LowDetail/SHP-TER-012_low-detail_concept_v01.png` | Pass |

### Buildings

| Asset group | Generated assets | Review |
|---|---|---|
| Command | BLD-CMD-001, BLD-CMD-002 | Pass |
| Habitation | BLD-HAB-001, BLD-HAB-002, BLD-HAB-003 | Pass |
| Life support | BLD-LIF-001 through BLD-LIF-005 | Pass |
| Mining | BLD-MIN-001 through BLD-MIN-004 | Pass |
| Storage | BLD-STO-001 through BLD-STO-003 | Pass |
| Power | BLD-PWR-001 through BLD-PWR-004 | Pass |

All new building files are stored as:

`Buildings/<asset-id>/LowDetail/<asset-id>_low-detail_concept_v01.png`

The previously approved Command Centre and Basic Mine retain their existing selected low-detail files.

### Props

| Asset | Low-detail concept | Review |
|---|---|---|
| PRP-IND-001 — Conveyor Module | `Props/PRP-IND-001/LowDetail/PRP-IND-001_low-detail_concept_v01.png` | Pass; single usable straight module rather than a kit sheet |

## Remaining concept groups

- BLD-PWR-005 and PRP-IND-003.
- Manufacturing and logistics buildings.
- Defence buildings.
- Sensor and technology buildings.
- Environment infrastructure.
- Missiles and satellites.
- Remaining industrial/construction props and the material library.

## Generation record

Mode: built-in ImageGen, style-transfer workflow.

Each call used the original asset concept as the identity reference and the approved low-detail Command Centre as the simplification/style reference. Per-asset prompt clauses retained only the dominant silhouette and functional masses while applying the locked exclusions above.
