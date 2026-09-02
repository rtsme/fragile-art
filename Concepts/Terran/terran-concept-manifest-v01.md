# Terran concept set and shared-component manifest — v01

Generated 2026-08-31 from the live production tracker and `docs/concept-rules-for-3d.md`.
Scope: **75 Terran tracker assets**. The approved Command Centre v01 and current Basic Mine v03 are retained; 73 missing concepts were generated with the built-in image-generation workflow. Four first passes were corrected as v02 after visual QA.

## Shared modular-detail library

Visual anchor: `Concepts/Terran/Shared/TER-KIT-001/TER-KIT-001_shared-detail-library_concept_v02.png`

Priority-module extension: `Concepts/Terran/Shared/TER-KIT-001/TER-KIT-001_priority-modules_concept_v03.png`

Production specification: `Concepts/Terran/Shared/TER-KIT-001/TER-KIT-001_production-spec_v02.md`

Priority-module specification: `Concepts/Terran/Shared/TER-KIT-001/TER-KIT-001_priority-modules_production-spec_v03.md`

Command Centre gap-module extension: `Concepts/Terran/Shared/TER-KIT-001/TER-KIT-001_command-centre-gap-modules_concept_v04.png`

Command Centre gap-module specification: `Concepts/Terran/Shared/TER-KIT-001/TER-KIT-001_command-centre-gap-modules_production-spec_v04.md`

Concept usage audit: `Concepts/Terran/Shared/TER-KIT-001/TER-KIT-001_component-usage-audit_v01.md`

Split-generation rule: `docs/shared-assembly-pipeline.md`

The original unlabelled v01 sheet is retained as an approved visual-direction record. The v02
sheet organizes the same language into twelve labelled families; the companion specification is
authoritative for component IDs, dimensions, snap footprints and reconstruction classification.

| Code | Family |
|---|---|
| TER-PAR | solid low parapets, corners and end caps |
| TER-TNK | vertical/horizontal tanks, vessels and hopper bodies in S/M/L sizes |
| TER-ANT | thick-bowl dishes, blocky radar heads and tapered mast bases |
| TER-VNT | deep vents, louvers, filter blocks and heat exchangers |
| TER-ACC | chunky stairs, recessed access ribs and service-step modules |
| TER-PIP | enclosed pipe trunks, raised conduit ribs, valves and couplers |
| TER-DOR | hatches, airlocks, cargo doors and docking collars |
| TER-PNL | access panels, equipment boxes and standardized sockets |
| TER-LGT | inset work-light housings and warning beacons, shown inactive in concepts |
| TER-BRC | solid buttresses and enclosed brace fairings |
| TER-DCK | docking clamps, landing/service sockets and refuelling couplers |
| TER-MAN | crane/manipulator roots, hinge blocks and folded-state mounts |
| TER-GLZ | opaque glazing panels, window bands and greenhouse roof bays |
| TER-SOL | rigid solar panels, panel wings and folded hinge/root blocks |
| TER-ROT | enclosed bearing rings, traverses and heavy turntables |
| TER-WPN | enclosed gun receivers, thick barrel shrouds and muzzle modules |
| TER-PWR | power nodes, capacitor banks and induction housings |
| TER-LCH | closed missile-cell pods, tube adapters and magazines |

Dishes, genuine masts, railings, ladders, exposed pipework, cranes, gantries, scaffolding and other thin/open parts are **hand-modelled shared-kit components**. The generated body concepts use closed placeholders or sockets for them.

## Per-asset mapping

| Asset | Concept file | Proposed shared components | Pipeline note |
|---|---|---|---|
| ENV-INF-001 — Construction Pad Kit | `Concepts/Terran/Environment/ENV-INF-001/ENV-INF-001_concept_v01.png` | TER-PNL, TER-LGT, TER-PIP, TER-MAN, TER-ACC, TER-PAR | use TER-PIP; no generated loose runs |
| ENV-INF-002 — Road and Pipe Network | `Concepts/Terran/Environment/ENV-INF-002/ENV-INF-002_concept_v01.png` | TER-PNL, TER-LGT, TER-PIP, TER-ACC, TER-PAR | use TER-PIP; no generated loose runs |
| BLD-CMD-001 — Command Centre | `Concepts/Terran/Buildings/BLD-CMD-001/BLD-CMD-001_concept_v01.png` | TER-GLZ, TER-DOR, TER-ANT, TER-ROT, TER-TNK, TER-VNT, TER-PIP, TER-ACC, TER-PNL, TER-LGT, TER-PAR, TER-BRC | split-pipeline trial: generate `Base/BLD-CMD-001_base-concept_v01.png` only; assemble per `BLD-CMD-001_assembly-manifest_v01.md`; 11 former gaps defined in TER-KIT-001 v04, production meshes pending |
| BLD-HAB-001 — Residential Block | `Concepts/Terran/Buildings/BLD-HAB-001/BLD-HAB-001_concept_v01.png` | TER-PNL, TER-LGT, TER-VNT, TER-DOR, TER-ACC, TER-PAR | body concept is scan-safe; add shared fittings during cleanup |
| BLD-HAB-002 — Living Quarters | `Concepts/Terran/Buildings/BLD-HAB-002/BLD-HAB-002_concept_v01.png` | TER-PNL, TER-LGT, TER-VNT, TER-PIP, TER-DOR, TER-ACC, TER-PAR | body concept is scan-safe; add shared fittings during cleanup |
| BLD-LIF-001 — Medical Centre | `Concepts/Terran/Buildings/BLD-LIF-001/BLD-LIF-001_concept_v01.png` | TER-PNL, TER-LGT, TER-TNK, TER-VNT, TER-DOR, TER-ACC, TER-PAR | body concept is scan-safe; add shared fittings during cleanup |
| BLD-HAB-003 — Pleasure Dome | `Concepts/Terran/Buildings/BLD-HAB-003/BLD-HAB-003_concept_v01.png` | TER-PNL, TER-LGT, TER-ACC, TER-PAR | body concept is scan-safe; add shared fittings during cleanup |
| BLD-CMD-002 — Security Centre | `Concepts/Terran/Buildings/BLD-CMD-002/BLD-CMD-002_concept_v01.png` | TER-PNL, TER-LGT, TER-DOR, TER-BRC, TER-ACC, TER-PAR | attach TER-ANT after body reconstruction; hand-model thin/deployable surfaces from thick concept massing |
| BLD-LIF-002 — Air Processor | `Concepts/Terran/Buildings/BLD-LIF-002/BLD-LIF-002_concept_v01.png` | TER-PNL, TER-LGT, TER-TNK, TER-VNT, TER-PIP, TER-ACC, TER-PAR | body concept is scan-safe; add shared fittings during cleanup |
| BLD-LIF-003 — Environment Control | `Concepts/Terran/Buildings/BLD-LIF-003/BLD-LIF-003_concept_v01.png` | TER-PNL, TER-LGT, TER-VNT, TER-ACC, TER-PAR | body concept is scan-safe; add shared fittings during cleanup |
| BLD-LIF-004 — Hydration Plant | `Concepts/Terran/Buildings/BLD-LIF-004/BLD-LIF-004_concept_v01.png` | TER-PNL, TER-LGT, TER-TNK, TER-VNT, TER-PIP, TER-ACC, TER-PAR | use TER-PIP; no generated loose runs |
| BLD-LIF-005 — Hydroponics Plant | `Concepts/Terran/Buildings/BLD-LIF-005/BLD-LIF-005_concept_v02.png` | TER-PNL, TER-LGT, TER-TNK, TER-VNT, TER-PIP, TER-DOR, TER-ACC, TER-PAR, TER-GLZ | standardized opaque TER-GLZ greenhouse bays selected in v02 |
| BLD-MIN-001 — Basic Mine | `Concepts/Terran/Buildings/BLD-MIN-001/BLD-MIN-001_concept_v03.png` | TER-PNL, TER-LGT, TER-TNK, TER-DOR, TER-VNT, TER-PIP, TER-ACC, TER-MAN, TER-DRL, TER-CNV, TER-FLU | body/detail split recorded in `BLD-MIN-001_assembly-manifest_v01.md`; reviewed mining scope defined in TER-KIT-001 v06 with the drill bit and all below-foundation geometry removed; textured body source v02 complete; textured orthographic v12 passes the reference gate; maximum-detail textured Meshy base v01 generated and structurally validated, with visual/geometry review pending |
| BLD-MIN-002 — Advanced Mine | `Concepts/Terran/Buildings/BLD-MIN-002/BLD-MIN-002_concept_v01.png` | TER-PNL, TER-LGT, TER-TNK, TER-ACC, TER-PAR | body concept is scan-safe; add shared fittings during cleanup |
| BLD-MIN-003 — Deep Bore Mine | `Concepts/Terran/Buildings/BLD-MIN-003/BLD-MIN-003_concept_v01.png` | TER-PNL, TER-LGT, TER-TNK, TER-MAN, TER-ACC, TER-PAR | hand-model TER-MAN/open-framework parts |
| BLD-MIN-004 — Seismic Penetrator | `Concepts/Terran/Buildings/BLD-MIN-004/BLD-MIN-004_concept_v01.png` | TER-PNL, TER-LGT, TER-BRC, TER-ACC, TER-PAR | body concept is scan-safe; add shared fittings during cleanup |
| BLD-STO-001 — Ore Storage | `Concepts/Terran/Buildings/BLD-STO-001/BLD-STO-001_concept_v01.png` | TER-PNL, TER-LGT, TER-TNK, TER-DOR, TER-MAN, TER-BRC, TER-ACC, TER-PAR | use TER-PAR/TER-ACC after reconstruction |
| BLD-STO-002 — Protected Storage Tower | `Concepts/Terran/Buildings/BLD-STO-002/BLD-STO-002_concept_v01.png` | TER-PNL, TER-LGT, TER-TNK, TER-DOR, TER-BRC, TER-ACC, TER-PAR | body concept is scan-safe; add shared fittings during cleanup |
| BLD-STO-003 — Ore Teleporter | `Concepts/Terran/Buildings/BLD-STO-003/BLD-STO-003_concept_v02.png` | TER-PNL, TER-LGT, TER-TNK, TER-VNT, TER-PIP, TER-ACC, TER-PAR | body concept is scan-safe; add shared fittings during cleanup |
| PRP-IND-001 — Conveyor Module Kit | `Concepts/Terran/Props/PRP-IND-001/PRP-IND-001_concept_v01.png` | TER-PNL, TER-LGT, TER-TNK, TER-BRC | body concept is scan-safe; add shared fittings during cleanup |
| PRP-IND-002 — Ore Container Kit | `Concepts/Terran/Props/PRP-IND-002/PRP-IND-002_concept_v01.png` | TER-PNL, TER-LGT, TER-TNK, TER-DOR, TER-DCK | body concept is scan-safe; add shared fittings during cleanup |
| BLD-PWR-001 — Solar Panel | `Concepts/Terran/Buildings/BLD-PWR-001/BLD-PWR-001_concept_v02.png` | TER-PNL, TER-LGT, TER-TNK, TER-PIP, TER-ACC, TER-PAR, TER-SOL, TER-ROT | standardized TER-SOL panel bank and TER-ROT-S4 traverse selected in v02; hand-model panel assembly |
| BLD-PWR-002 — Solar Matrix | `Concepts/Terran/Buildings/BLD-PWR-002/BLD-PWR-002_concept_v02.png` | TER-PNL, TER-LGT, TER-VNT, TER-PIP, TER-ACC, TER-PAR, TER-SOL, TER-ROT | six repeated TER-SOL-WNG-L modules and TER-ROT-S4 selected in v02; hand-model panel assembly |
| BLD-PWR-003 — Power Store | `Concepts/Terran/Buildings/BLD-PWR-003/BLD-PWR-003_concept_v01.png` | TER-PNL, TER-LGT, TER-TNK, TER-VNT, TER-PIP, TER-ACC, TER-PAR | body concept is scan-safe; add shared fittings during cleanup |
| BLD-PWR-004 — Power Plant | `Concepts/Terran/Buildings/BLD-PWR-004/BLD-PWR-004_concept_v01.png` | TER-PNL, TER-LGT, TER-TNK, TER-VNT, TER-PIP, TER-ACC, TER-PAR | body concept is scan-safe; add shared fittings during cleanup |
| BLD-PWR-005 — High-Energy Generator | `Concepts/Terran/Buildings/BLD-PWR-005/BLD-PWR-005_concept_v01.png` | TER-PNL, TER-LGT, TER-TNK, TER-PIP, TER-ACC, TER-PAR | body concept is scan-safe; add shared fittings during cleanup |
| PRP-IND-003 — Power Node Kit | `Concepts/Terran/Props/PRP-IND-003/PRP-IND-003_concept_v01.png` | TER-PNL, TER-LGT, TER-PIP | use TER-PIP; no generated loose runs |
| BLD-MFG-001 — Weapons Factory | `Concepts/Terran/Buildings/BLD-MFG-001/BLD-MFG-001_concept_v01.png` | TER-PNL, TER-LGT, TER-TNK, TER-DOR, TER-MAN, TER-BRC, TER-ACC, TER-PAR | hand-model TER-MAN/open-framework parts |
| BLD-MFG-002 — Shipyard | `Concepts/Terran/Buildings/BLD-MFG-002/BLD-MFG-002_concept_v01.png` | TER-PNL, TER-LGT, TER-DOR, TER-DCK, TER-MAN, TER-ACC, TER-PAR | use TER-PAR/TER-ACC after reconstruction |
| BLD-MFG-003 — Space Dock | `Concepts/Terran/Buildings/BLD-MFG-003/BLD-MFG-003_concept_v02.png` | TER-PNL, TER-LGT, TER-DCK, TER-MAN, TER-ACC, TER-PAR | hand-model TER-MAN/open-framework parts |
| BLD-LOG-001 — Landing Pad | `Concepts/Terran/Buildings/BLD-LOG-001/BLD-LOG-001_concept_v01.png` | TER-PNL, TER-LGT, TER-TNK, TER-DOR, TER-DCK, TER-ACC, TER-PAR | body concept is scan-safe; add shared fittings during cleanup |
| BLD-LOG-002 — Refuelling Depot | `Concepts/Terran/Buildings/BLD-LOG-002/BLD-LOG-002_concept_v02.png` | TER-PNL, TER-LGT, TER-TNK, TER-PIP, TER-DCK, TER-ACC, TER-PAR | use TER-PIP; no generated loose runs; hand-model thin/deployable surfaces from thick concept massing |
| BLD-LOG-003 — Repair Facility | `Concepts/Terran/Buildings/BLD-LOG-003/BLD-LOG-003_concept_v01.png` | TER-PNL, TER-LGT, TER-TNK, TER-VNT, TER-DOR, TER-DCK, TER-MAN, TER-ACC, TER-PAR | hand-model TER-MAN/open-framework parts |
| BLD-LOG-004 — Cargo Depot | `Concepts/Terran/Buildings/BLD-LOG-004/BLD-LOG-004_concept_v01.png` | TER-PNL, TER-LGT, TER-TNK, TER-DOR, TER-DCK, TER-ACC, TER-PAR | body concept is scan-safe; add shared fittings during cleanup |
| BLD-MFG-004 — Construction Yard | `Concepts/Terran/Buildings/BLD-MFG-004/BLD-MFG-004_concept_v01.png` | TER-PNL, TER-LGT, TER-TNK, TER-DOR, TER-MAN, TER-BRC, TER-ACC, TER-PAR | hand-model TER-MAN/open-framework parts |
| BLD-DEF-001 — Basic Turret | `Concepts/Terran/Buildings/BLD-DEF-001/BLD-DEF-001_concept_v02.png` | TER-PNL, TER-LGT, TER-PIP, TER-DCK, TER-BRC, TER-ACC, TER-PAR, TER-WPN, TER-ROT | standardized medium TER-WPN gun and TER-ROT-S3 selected in v02; hand-model weapon assembly |
| BLD-DEF-002 — Plasma Turret | `Concepts/Terran/Buildings/BLD-DEF-002/BLD-DEF-002_concept_v02.png` | TER-PNL, TER-LGT, TER-VNT, TER-PIP, TER-DCK, TER-BRC, TER-ACC, TER-PAR, TER-WPN, TER-PWR, TER-ROT | standardized large TER-WPN plasma emitter, TER-PWR banks and TER-ROT-S4 selected in v02 |
| BLD-DEF-003 — Photon Turret | `Concepts/Terran/Buildings/BLD-DEF-003/BLD-DEF-003_concept_v02.png` | TER-PNL, TER-LGT, TER-ANT, TER-VNT, TER-PIP, TER-DCK, TER-BRC, TER-ACC, TER-PAR, TER-WPN, TER-ROT | paired medium TER-WPN guns, block radar and TER-ROT-S4 selected in v02 |
| BLD-DEF-004 — Anti-Missile Pod | `Concepts/Terran/Buildings/BLD-DEF-004/BLD-DEF-004_concept_v02.png` | TER-PNL, TER-LGT, TER-ANT, TER-DOR, TER-DCK, TER-ACC, TER-PAR, TER-LCH, TER-ROT | standardized 4x4 TER-LCH pod, TER-ANT sensors and TER-ROT-S4 selected in v02 |
| BLD-DEF-005 — Screen Generator | `Concepts/Terran/Buildings/BLD-DEF-005/BLD-DEF-005_concept_v01.png` | TER-PNL, TER-LGT, TER-ACC, TER-PAR | body concept is scan-safe; add shared fittings during cleanup |
| BLD-DEF-006 — Missile Silo | `Concepts/Terran/Buildings/BLD-DEF-006/BLD-DEF-006_concept_v01.png` | TER-PNL, TER-LGT, TER-DOR, TER-DCK, TER-BRC, TER-ACC, TER-PAR | body concept is scan-safe; add shared fittings during cleanup |
| BLD-DEF-007 — Satellite Silo | `Concepts/Terran/Buildings/BLD-DEF-007/BLD-DEF-007_concept_v01.png` | TER-PNL, TER-LGT, TER-ANT, TER-DOR, TER-DCK, TER-MAN, TER-BRC, TER-ACC, TER-PAR | attach TER-ANT after body reconstruction; hand-model TER-MAN/open-framework parts |
| BLD-DEF-008 — Defensive Bunker | `Concepts/Terran/Buildings/BLD-DEF-008/BLD-DEF-008_concept_v01.png` | TER-PNL, TER-LGT, TER-DOR, TER-BRC, TER-ACC, TER-PAR | body concept is scan-safe; add shared fittings during cleanup |
| BLD-SEN-001 — Sensor Array | `Concepts/Terran/Buildings/BLD-SEN-001/BLD-SEN-001_concept_v01.png` | TER-PNL, TER-LGT, TER-ANT, TER-DCK, TER-ACC, TER-PAR | attach TER-ANT after body reconstruction |
| BLD-SEN-002 — Long Range Transmitter | `Concepts/Terran/Buildings/BLD-SEN-002/BLD-SEN-002_concept_v01.png` | TER-PNL, TER-LGT, TER-ANT, TER-BRC, TER-ACC, TER-PAR | attach TER-ANT after body reconstruction |
| BLD-TEC-001 — Gravity Nullifier | `Concepts/Terran/Buildings/BLD-TEC-001/BLD-TEC-001_concept_v02.png` | TER-PNL, TER-LGT, TER-ACC, TER-PAR | body concept is scan-safe; add shared fittings during cleanup |
| BLD-TEC-002 — Asteroid Engine | `Concepts/Terran/Buildings/BLD-TEC-002/BLD-TEC-002_concept_v01.png` | TER-PNL, TER-LGT, TER-TNK, TER-VNT, TER-ACC, TER-PAR | body concept is scan-safe; add shared fittings during cleanup |
| BLD-TEC-003 — Shield Generator | `Concepts/Terran/Buildings/BLD-TEC-003/BLD-TEC-003_concept_v01.png` | TER-PNL, TER-LGT, TER-TNK, TER-ACC, TER-PAR | body concept is scan-safe; add shared fittings during cleanup |
| BLD-TEC-004 — Construction Droid Hub | `Concepts/Terran/Buildings/BLD-TEC-004/BLD-TEC-004_concept_v01.png` | TER-PNL, TER-LGT, TER-DOR, TER-MAN, TER-ACC, TER-PAR | attach TER-ANT after body reconstruction |
| BLD-TEC-005 — Teleportation Equipment | `Concepts/Terran/Buildings/BLD-TEC-005/BLD-TEC-005_concept_v01.png` | TER-PNL, TER-LGT, TER-BRC, TER-ACC, TER-PAR | body concept is scan-safe; add shared fittings during cleanup |
| SHP-TER-001 — Scout | `Concepts/Terran/Ships/SHP-TER-001/SHP-TER-001_concept_v01.png` | TER-PNL, TER-LGT, TER-ANT, TER-VNT | attach TER-ANT after body reconstruction |
| SHP-TER-002 — Fighter | `Concepts/Terran/Ships/SHP-TER-002/SHP-TER-002_concept_v01.png` | TER-PNL, TER-LGT, TER-VNT | body concept is scan-safe; add shared fittings during cleanup |
| SHP-TER-003 — Corvette | `Concepts/Terran/Ships/SHP-TER-003/SHP-TER-003_concept_v01.png` | TER-PNL, TER-LGT, TER-VNT, TER-DCK, TER-BRC | body concept is scan-safe; add shared fittings during cleanup |
| SHP-TER-004 — Frigate | `Concepts/Terran/Ships/SHP-TER-004/SHP-TER-004_concept_v01.png` | TER-PNL, TER-LGT, TER-ANT, TER-VNT, TER-DCK, TER-BRC | attach TER-ANT after body reconstruction |
| SHP-TER-005 — Transport | `Concepts/Terran/Ships/SHP-TER-005/SHP-TER-005_concept_v01.png` | TER-PNL, TER-LGT, TER-VNT, TER-DOR, TER-DCK | body concept is scan-safe; add shared fittings during cleanup |
| SHP-TER-006 — Destroyer | `Concepts/Terran/Ships/SHP-TER-006/SHP-TER-006_concept_v01.png` | TER-PNL, TER-LGT, TER-VNT, TER-PIP, TER-DCK, TER-BRC | body concept is scan-safe; add shared fittings during cleanup |
| SHP-TER-007 — Cruiser | `Concepts/Terran/Ships/SHP-TER-007/SHP-TER-007_concept_v01.png` | TER-PNL, TER-LGT, TER-DOR, TER-DCK, TER-BRC | body concept is scan-safe; add shared fittings during cleanup |
| SHP-TER-008 — Command Cruiser | `Concepts/Terran/Ships/SHP-TER-008/SHP-TER-008_concept_v01.png` | TER-PNL, TER-LGT, TER-TNK, TER-ANT, TER-DOR, TER-DCK, TER-BRC | attach TER-ANT after body reconstruction |
| SHP-TER-009 — Colony Ship | `Concepts/Terran/Ships/SHP-TER-009/SHP-TER-009_concept_v01.png` | TER-PNL, TER-LGT, TER-TNK, TER-DOR, TER-DCK, TER-MAN | body concept is scan-safe; add shared fittings during cleanup |
| SHP-TER-010 — Freighter | `Concepts/Terran/Ships/SHP-TER-010/SHP-TER-010_concept_v01.png` | TER-PNL, TER-LGT, TER-TNK, TER-DOR, TER-DCK | body concept is scan-safe; add shared fittings during cleanup |
| SHP-TER-011 — Bomber | `Concepts/Terran/Ships/SHP-TER-011/SHP-TER-011_concept_v01.png` | TER-PNL, TER-LGT, TER-ANT, TER-VNT, TER-DOR, TER-BRC | attach TER-ANT after body reconstruction |
| SHP-TER-012 — Shuttle | `Concepts/Terran/Ships/SHP-TER-012/SHP-TER-012_concept_v01.png` | TER-PNL, TER-LGT, TER-VNT, TER-DOR, TER-DCK, TER-MAN, TER-ACC | body concept is scan-safe; add shared fittings during cleanup |
| MIS-ORD-001 — Standard Missile | `Concepts/Terran/Missiles/MIS-ORD-001/MIS-ORD-001_concept_v01.png` | TER-PNL, TER-LGT, TER-VNT, TER-DOR, TER-DCK, TER-BRC | hand-model thin/deployable surfaces from thick concept massing |
| MIS-ORD-002 — Plasma Missile | `Concepts/Terran/Missiles/MIS-ORD-002/MIS-ORD-002_concept_v01.png` | TER-PNL, TER-LGT, TER-TNK | hand-model thin/deployable surfaces from thick concept massing |
| MIS-ORD-003 — Interceptor Missile | `Concepts/Terran/Missiles/MIS-ORD-003/MIS-ORD-003_concept_v01.png` | TER-PNL, TER-LGT, TER-ANT, TER-VNT, TER-DCK | attach TER-ANT after body reconstruction; hand-model thin/deployable surfaces from thick concept massing |
| SAT-ORB-001 — Recon Satellite | `Concepts/Terran/Satellites/SAT-ORB-001/SAT-ORB-001_concept_v01.png` | TER-PNL, TER-LGT, TER-ANT, TER-VNT, TER-DCK, TER-ACC | attach TER-ANT after body reconstruction; hand-model thin/deployable surfaces from thick concept massing |
| SAT-ORB-002 — Defence Satellite | `Concepts/Terran/Satellites/SAT-ORB-002/SAT-ORB-002_concept_v01.png` | TER-PNL, TER-LGT, TER-ANT, TER-VNT, TER-PIP, TER-BRC, TER-ACC | attach TER-ANT after body reconstruction; hand-model thin/deployable surfaces from thick concept massing |
| SAT-ORB-003 — Communications Satellite | `Concepts/Terran/Satellites/SAT-ORB-003/SAT-ORB-003_concept_v01.png` | TER-PNL, TER-LGT, TER-ANT, TER-ACC | attach TER-ANT after body reconstruction; hand-model thin/deployable surfaces from thick concept massing |
| PRP-IND-004 — Industrial Pipe Kit | `Concepts/Terran/Props/PRP-IND-004/PRP-IND-004_concept_v01.png` | TER-PNL, TER-LGT, TER-PIP | use TER-PIP; no generated loose runs |
| PRP-IND-005 — Tank and Vessel Kit | `Concepts/Terran/Props/PRP-IND-005/PRP-IND-005_concept_v01.png` | TER-PNL, TER-LGT, TER-TNK, TER-ACC | use TER-PAR/TER-ACC after reconstruction |
| PRP-CON-001 — Crane and Manipulator Kit | `Concepts/Terran/Props/PRP-CON-001/PRP-CON-001_concept_v01.png` | TER-PNL, TER-LGT, TER-DCK, TER-MAN, TER-ACC | hand-model TER-MAN/open-framework parts; use TER-PAR/TER-ACC after reconstruction |
| PRP-CON-002 — Construction and Scaffolding Kit | `Concepts/Terran/Props/PRP-CON-002/PRP-CON-002_concept_v01.png` | TER-PNL, TER-LGT, TER-MAN, TER-BRC, TER-ACC | hand-model TER-MAN/open-framework parts |
| PRP-IND-006 — Cargo Crate Kit | `Concepts/Terran/Props/PRP-IND-006/PRP-IND-006_concept_v01.png` | TER-PNL, TER-LGT, TER-DOR, TER-DCK | body concept is scan-safe; add shared fittings during cleanup |
| PRP-IND-007 — Antenna and Sensor Kit | `Concepts/Terran/Props/PRP-IND-007/PRP-IND-007_concept_v01.png` | TER-PNL, TER-LGT, TER-ANT | attach TER-ANT after body reconstruction |
| MAT-TER-001 — Terran Industrial Material Library | `Concepts/Terran/Materials/MAT-TER-001/MAT-TER-001_concept_v01.png` | TER-PNL, TER-LGT, TER-BRC | hand-model thin/deployable surfaces from thick concept massing |

## Generation prompt set

Every new asset used its own built-in image-generation call. The per-asset tracker fields (ID, name, category, variants, scale, purpose, description, visual language and key features) were inserted into this common production prompt:

> Create one production hero concept (or one organized family sheet for modular kits) that preserves the asset's dominant functional feature and reads clearly from an RTS top/isometric camera. Match the approved Terran anchor: chunky rectangular and hexagonal reinforced masses, controlled asymmetry, dark neutral metals, warm off-white armour and restrained amber hazard accents. Intentionally reuse the mapped TER-* component families with common mounting flanges, chamfers and snap dimensions. Present the isolated complete asset in an elevated orthographic-style three-quarter view on a plain neutral light-grey background. Use closed coherent silhouettes, solid enclosed volumes, obvious thickness, large flat panels, deep chamfers and bold mass breaks. No open lattice/truss/scaffold, thin sheets, wires, cables, rods, thin railings, unsupported parts, transparent/interior-rich glass, chrome, glow, cast shadows or fine greeble. Railings become solid parapets; conduits become raised ribs; dishes become thick bowls. Reserve delicate rails, ladders, cranes, gantries, antennae and exposed pipework for later shared-kit hand modelling.

Targeted v02 corrections: Space Dock — closed segmented aperture and crane sockets; Refuelling Depot — enclosed rigid service trunk and folded manipulator; Ore Teleporter — capped solid transfer drum; Gravity Nullifier — enclosed containment drum with no open ring.

## Verification

- 74 staged PNGs verified readable (73 per-asset outputs plus the shared-detail sheet).
- No exact duplicate image files found.
- Category contact sheets were reviewed for silhouette/function/style drift.
- Four scan-unsafe first passes were regenerated and the v02 files selected above.
- Orthographic references were not generated in this pass; the tracker pipeline requires concept sign-off before four-view production.

## Existing-model review

The existing BLD-CMD-001 Meshy v01 GLB is a single-mesh, single-material asset with 34,588 vertices and 39,575 triangles. Its reference package fails the current consistency checker because canvases differ and silhouette size varies by roughly 14%. The rulebook records noisy dish reconstruction, glazing lumps and blurred greeble; these failures drove the closed-volume, opaque-glass and hand-modelled-detail rules used here.
