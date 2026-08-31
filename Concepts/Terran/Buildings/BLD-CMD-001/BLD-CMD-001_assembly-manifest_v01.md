# BLD-CMD-001 — Command Centre assembly manifest v01

Status: **pipeline trial / concept-pass quantities**
Final appearance target: `BLD-CMD-001_concept_v01.png`
Body-only source: `Base/BLD-CMD-001_base-concept_v01.png`

The final concept is authoritative for appearance. The body-only source is authoritative only for
what is allowed into AI mesh generation. Counts below cover the visible hero-concept design; rear
and hidden-face counts must be frozen when the consistent four-view base/assembly reference set is
made. No listed detail may be baked into the base to avoid that count pass.

## Approved shared-library assets

| Exact component ID | Trial qty | Receiver | Intended use |
|---|---:|---|---|
| TER-GLZ-BND-L | 6 | 6 × 1.5 m wall recess | long command-window runs |
| TER-GLZ-PNL-L | 4 | 4 × 2.5 m wall recess | end and lower-level glazing |
| TER-DOR-CGO-L | 1 | 4.5 × 4 m wall recess | main cargo/command entrance |
| TER-DOR-AIR-M | 3 | 2.5 × 3 m wall recess | secondary personnel airlocks |
| TER-DOR-HTC-S | 4 | 1.5 × 2.25 m wall recess | service hatches |
| TER-ANT-DSH-L | 1 | S3 roof mount | primary communications dish |
| TER-ROT-S3 | 1 | S3 roof pad | dish traverse |
| TER-ANT-MST-L | 1 | 3 × 3 m roof pad | primary mast base |
| TER-ANT-MST-M | 2 | S3 roof pad | secondary mast bases |
| TER-ANT-RDR-S | 2 | S2 pivot | block radar heads |
| TER-ANT-PVT-S | 2 | S2 roof pad | radar-head pivots |
| TER-TNK-V-M | 4 | 3 × 3 m ground/side pad | right-side service-vessel bank |
| TER-VNT-LVR-L | 2 | 4 × 4 m wall recess | major intake/exhaust faces |
| TER-VNT-LVR-M | 4 | 2.5 × 2.5 m wall recess | secondary ventilation |
| TER-VNT-HX-L | 2 | 4 × 4 m side pad | heat-exchanger housings |
| TER-PIP-TRK-L | 2 | S3 endpoints | long service trunks |
| TER-PIP-TRK-M | 4 | S2 endpoints | medium service trunks |
| TER-PIP-CPL-M | 6 | S2 inline | trunk couplers |
| TER-PIP-VLV-M | 2 | S2 inline | service isolation blocks |
| TER-PIP-RIB | 6 | S1 surface pads | short surface conduit runs |
| TER-ACC-STR-L | 1 | 3 × 6 m ground pad | main enclosed access stair |
| TER-ACC-STR-M | 2 | 2.5 × 4.5 m ground pad | secondary stairs |
| TER-ACC-STP | 4 | 1 × 1 m ground pad | service steps |
| TER-PNL-ACS-M | 8 | 1.5 × 1.5 m wall pad | access panels |
| TER-PNL-ACS-L | 4 | 2.5 × 2.5 m wall pad | large maintenance panels |
| TER-PNL-EQB-M | 6 | S2 wall/roof pad | equipment boxes |
| TER-PNL-SKT-S | 8 | S1 surface recess | visible light-detail sockets |
| TER-PNL-SKT-M | 8 | S2 surface recess | visible equipment sockets |
| TER-LGT-WRK-M | 12 | S1 | perimeter work lights |
| TER-LGT-BCN-S | 12 | S1 | roof and corner warning beacons |
| TER-PAR-STR-M | 6 | S2 deck edge | solid parapet runs visible in final |
| TER-PAR-CNR | 4 | S2 deck corner | solid parapet corners |
| TER-PAR-END | 4 | S2 deck edge | solid parapet terminations |
| TER-BRC-FAR-M | 4 | 2 × 3 m wall/ground pad | bolt-on brace fairings only |

Large silhouette-defining buttresses remain part of the base. `TER-BRC-FAR-M` is reserved for
smaller bolt-on braces and must not duplicate those structural masses.

## Shared-library gaps exposed by the final concept — now defined in v04

These parts were absent from TER-KIT-001 v02/v03. They are now defined by
`../../Shared/TER-KIT-001/TER-KIT-001_command-centre-gap-modules_production-spec_v04.md`; their
maximum-detail Meshy source meshes are now generated; production cleanup and approval are pending.

| Proposed component ID | Trial qty | Receiver | Requirement |
|---|---:|---|---|
| TER-GLZ-BND-M | 4 | 4 × 1.5 m wall recess | shorter window-band module |
| TER-GLZ-BND-CNR | 4 | paired band recess | framed angled command-window corner |
| TER-DOR-PRT-L | 1 | S4 wall/ground interface | heavy projecting entrance portal around TER-DOR-CGO-L |
| TER-VNT-FAN-L | 2 | S3 roof recess | enclosed axial roof-fan housing |
| TER-PIP-ELB-M | 8 | S2 inline | enclosed 90-degree trunk elbow |
| TER-PIP-TEE-M | 2 | S2 inline | enclosed three-way trunk junction |
| TER-ACC-RMP-L | 1 | S4 ground/door interface | main enclosed access ramp/landing |
| TER-ACC-RAL-M | 12 | S1 deck-edge sockets | reusable guardrail run matching final concept |
| TER-ACC-RAL-CNR | 8 | S1 deck-edge sockets | guardrail corner/return |
| TER-ANT-AER-S | 4 | S1 mast-top socket | short aerial tip |
| TER-ANT-AER-M | 2 | S1 mast-top socket | medium aerial tip |

Status for every row above: **DEFINED IN TER-KIT-001 v04 — FOUR-VIEW REFERENCES COMPLETE — MESHY
SOURCE GENERATED — REVIEW/CLEANUP PENDING**. The base must not absorb them during production
cleanup. The five `H`-route objects remain reconstruction experiments until visual approval.

## Initial receiver schedule

- Roof centre: one S3 traverse receiver for the primary dish.
- Upper command roof: one 3 × 3 m mast pad, two S3 secondary mast pads, two S2 radar-pivot pads,
  and six S1 aerial/light receivers.
- Command-block faces: continuous flat-bottomed glazing recesses divided only at shared-module
  boundaries.
- Main front face: one S4 portal/cargo-door receiver, with a separate ground pad for the ramp.
- Side and rear faces: three airlock recesses, four hatch recesses, ventilation recesses and S1/S2
  panel/light pads on the 0.5 m grid.
- Right service yard: four 3 × 3 m tank pads, two S3 trunk endpoints and S2 elbow/valve receivers.
- Accessible roof/deck edges: S1 guardrail sockets or S2 solid-parapet sockets according to the
  final concept; never a generated rail/parapet fused to the body.

Exact coordinates are deferred to the body-only orthographic pass. That pass must preserve these
receiver classes and may adjust counts only by updating this manifest first.
