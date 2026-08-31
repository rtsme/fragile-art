# TER-KIT-001 shared detail library — production specification v02

Status: **visual direction approved** on 2026-08-31.

Visual reference: `TER-KIT-001_shared-detail-library_concept_v02.png`

This document is authoritative for identifiers, dimensions, mounting footprints and build
classification. The concept sheet is authoritative for shape language, materials and colour.

## Common standard

- Units are metres. Dimensions are written **width × depth × height** and describe the maximum
  component envelope, not clearance.
- Primary construction grid: **0.5 m**. Structural footprints and attachment centres snap to it.
- Detail grid: **0.25 m**. It may be used for trim and recessed panels, but never to position a
  gameplay-relevant connection.
- Standard attachment classes:
  - **S1:** 0.5 × 0.5 m light-detail socket.
  - **S2:** 1 × 1 m equipment or conduit socket.
  - **S3:** 2 × 2 m structural or service socket.
  - **S4:** 4 × 4 m heavy docking socket.
- A ground-mounted part uses its listed width × depth as its placement footprint. A wall-mounted
  part lists its mounting face as width × height in the notes.
- **R** means the closed body is reconstruction-safe when it remains above the parent asset's 2%
  feature-size threshold. **H** means hand-model only. Components marked H may still appear in a
  parent concept as a closed placeholder or socket.
- All visible edges use broad chamfers. No production component may introduce open lattice, loose
  wires, thin rails, transparent surfaces, glow or geometry-sized greeble.

## Component catalogue

### TER-PAR — solid parapets

| Component ID | Description | Envelope | Socket | Build | Notes |
|---|---|---:|---|:---:|---|
| TER-PAR-STR-S | short straight parapet | 4 × 1 × 1.5 | S2 | R | end faces accept TER-PAR-END |
| TER-PAR-STR-M | medium straight parapet | 8 × 1 × 1.5 | S2 | R | two 4 m visual bays |
| TER-PAR-CNR | 90-degree corner | 2 × 2 × 1.5 | S2 | R | 1 m legs align to straight runs |
| TER-PAR-END | capped terminator | 1 × 1 × 1.5 | S2 | R | no exposed connection face |

### TER-TNK — tanks, vessels and hoppers

| Component ID | Description | Envelope | Footprint | Build | Notes |
|---|---|---:|---:|:---:|---|
| TER-TNK-V-S | small vertical vessel | 2 × 2 × 4 | 2 × 2 | R | top S1 service cap |
| TER-TNK-V-M | medium vertical vessel | 3 × 3 × 6 | 3 × 3 | R | side S2 service socket |
| TER-TNK-V-L | large vertical vessel | 4 × 4 × 8 | 4 × 4 | R | side S2 service socket |
| TER-TNK-H-S | small horizontal vessel | 4 × 2 × 2.5 | 4 × 2 | R | end S2 connection |
| TER-TNK-H-M | medium horizontal vessel | 6 × 3 × 3.5 | 6 × 3 | R | end S2 connection |
| TER-TNK-H-L | large horizontal vessel | 8 × 4 × 4.5 | 8 × 4 | R | end S3 connection |
| TER-TNK-HOP-M | medium enclosed hopper | 4 × 4 × 5 | 4 × 4 | R | bottom S2 outlet placeholder |

### TER-ANT — dishes, radar heads and mast bases

| Component ID | Description | Envelope | Footprint | Build | Notes |
|---|---|---:|---:|:---:|---|
| TER-ANT-DSH-S | small thick-bowl dish | 2.5 × 2.5 × 2.5 | 1.5 × 1.5 | H | bowl thickness at least 0.2 m |
| TER-ANT-DSH-M | medium thick-bowl dish | 4 × 4 × 4 | 2 × 2 | H | no thin feed struts |
| TER-ANT-DSH-L | large thick-bowl dish | 6 × 6 × 6 | 3 × 3 | H | no thin feed struts |
| TER-ANT-RDR-S | small block radar head | 1.5 × 1.5 × 1.5 | 1 × 1 | H | mounts to S2 pivot |
| TER-ANT-RDR-M | medium block radar head | 2.5 × 2.5 × 2.5 | 1.5 × 1.5 | H | mounts to S3 pivot |
| TER-ANT-MST-S | small tapered mast base | 1.5 × 1.5 × 2.5 | 1.5 × 1.5 | R | top S1 socket |
| TER-ANT-MST-M | medium tapered mast base | 2 × 2 × 4 | 2 × 2 | R | top S2 socket |
| TER-ANT-MST-L | large tapered mast base | 3 × 3 × 6 | 3 × 3 | R | top S2 socket |

### TER-VNT — vents, filters and heat exchangers

| Component ID | Description | Envelope | Mount face | Build | Notes |
|---|---|---:|---:|:---:|---|
| TER-VNT-LVR-S | small deep louver | 1.5 × 0.75 × 1.5 | 1.5 × 1.5 | R | minimum louver depth 0.2 m |
| TER-VNT-LVR-M | medium deep louver | 2.5 × 1 × 2.5 | 2.5 × 2.5 | R | five or fewer broad blades |
| TER-VNT-LVR-L | large deep louver | 4 × 1.5 × 4 | 4 × 4 | R | six or fewer broad blades |
| TER-VNT-FLT-M | enclosed filter block | 2 × 1 × 2 | 2 × 2 | R | no porous surface detail |
| TER-VNT-HX-L | enclosed heat exchanger | 4 × 2 × 4 | 4 × 4 | R | S2 sockets on both sides |

### TER-ACC — stairs, access ribs and service steps

| Component ID | Description | Envelope | Footprint | Build | Notes |
|---|---|---:|---:|:---:|---|
| TER-ACC-STR-S | short enclosed stair | 2 × 3 × 1.5 | 2 × 3 | R | solid cheeks; no railing |
| TER-ACC-STR-M | medium enclosed stair | 2.5 × 4.5 × 2.5 | 2.5 × 4.5 | R | solid cheeks; no railing |
| TER-ACC-STR-L | long enclosed stair | 3 × 6 × 4 | 3 × 6 | R | solid cheeks; no railing |
| TER-ACC-RIB-S | short recessed access rib | 1 × 0.5 × 2 | 1 × 2 wall | R | not climbable |
| TER-ACC-RIB-L | tall recessed access rib | 1.5 × 0.75 × 4 | 1.5 × 4 wall | R | not a ladder |
| TER-ACC-STP | solid service step | 1 × 1 × 0.5 | 1 × 1 | R | single closed block |

### TER-PIP — enclosed service trunks and couplers

| Component ID | Description | Envelope | Connection | Build | Notes |
|---|---|---:|---|:---:|---|
| TER-PIP-TRK-S | short enclosed pipe trunk | 2 × 1 × 1 | S2 inline | H | removable shared-kit run |
| TER-PIP-TRK-M | medium enclosed pipe trunk | 4 × 1.5 × 1.5 | S2 inline | H | removable shared-kit run |
| TER-PIP-TRK-L | long enclosed pipe trunk | 8 × 2 × 2 | S3 inline | H | removable shared-kit run |
| TER-PIP-CPL-S | small inline coupler | 1 × 1 × 1 | S2 inline | H | closed collar |
| TER-PIP-CPL-M | medium inline coupler | 1.5 × 1.5 × 1.5 | S2 inline | H | closed collar |
| TER-PIP-VLV-M | enclosed valve block | 2 × 1.5 × 2 | S2 inline | H | no thin handwheel |
| TER-PIP-RIB | surface conduit rib | 4 × 0.5 × 0.5 | S1 surface | H | follows parent surface |

### TER-DOR — hatches, airlocks, doors and collars

| Component ID | Description | Envelope | Opening | Build | Notes |
|---|---|---:|---:|:---:|---|
| TER-DOR-HTC-S | personnel hatch | 1.5 × 0.5 × 2.25 | 1 × 2 | R | opaque closed panel |
| TER-DOR-AIR-M | medium airlock | 2.5 × 1 × 3 | 1.5 × 2.25 | R | no visible interior |
| TER-DOR-CGO-L | large cargo door | 4.5 × 1.25 × 4 | 3.5 × 3 | R | opaque closed panel |
| TER-DOR-COL-S | small docking collar | 2 × 1 × 2 | 1.25 diameter | R | S2 rear socket |
| TER-DOR-COL-M | medium docking collar | 3 × 1.5 × 3 | 2 diameter | R | S3 rear socket |
| TER-DOR-COL-L | large docking collar | 4.5 × 2 × 4.5 | 3 diameter | R | S4 rear socket |

### TER-PNL — panels, boxes and sockets

| Component ID | Description | Envelope | Mount face | Build | Notes |
|---|---|---:|---:|:---:|---|
| TER-PNL-ACS-S | small access panel | 0.75 × 0.25 × 0.75 | 0.75 × 0.75 | R | flat marking only below 0.1 m |
| TER-PNL-ACS-M | medium access panel | 1.5 × 0.25 × 1.5 | 1.5 × 1.5 | R | broad recessed centre |
| TER-PNL-ACS-L | large access panel | 2.5 × 0.3 × 2.5 | 2.5 × 2.5 | R | broad recessed centre |
| TER-PNL-EQB-S | small equipment box | 1 × 0.5 × 1 | 1 × 1 | R | S1 underside socket |
| TER-PNL-EQB-M | medium equipment box | 2 × 0.75 × 2 | 2 × 2 | R | S2 underside socket |
| TER-PNL-SKT-S | small standard socket | 0.5 × 0.25 × 0.5 | 0.5 × 0.5 | R | accepts S1 |
| TER-PNL-SKT-M | medium standard socket | 1 × 0.35 × 1 | 1 × 1 | R | accepts S2 |

### TER-LGT — work lights and warning beacons

| Component ID | Description | Envelope | Socket | Build | Notes |
|---|---|---:|---|:---:|---|
| TER-LGT-WRK-S | inset work light | 0.75 × 0.25 × 0.5 | S1 | H | inactive lens in concepts |
| TER-LGT-WRK-M | wide inset work light | 1.25 × 0.25 × 0.75 | S1 | H | inactive lens in concepts |
| TER-LGT-BCN-S | small warning beacon | 0.5 × 0.5 × 1 | S1 | H | opaque amber housing |
| TER-LGT-BCN-M | medium warning beacon | 0.75 × 0.75 × 1.5 | S1 | H | opaque amber housing |
| TER-LGT-BCN-L | large warning beacon | 1 × 1 × 2 | S2 | H | opaque amber housing |

### TER-BRC — buttresses and brace fairings

| Component ID | Description | Envelope | Footprint | Build | Notes |
|---|---|---:|---:|:---:|---|
| TER-BRC-BUT-S | small solid buttress | 1 × 2 × 2 | 1 × 2 | R | closed triangular wedge |
| TER-BRC-BUT-M | medium solid buttress | 1.5 × 3 × 3 | 1.5 × 3 | R | closed triangular wedge |
| TER-BRC-BUT-L | large solid buttress | 2 × 4 × 4 | 2 × 4 | R | closed triangular wedge |
| TER-BRC-FAR-M | medium brace fairing | 2 × 3 × 3 | 2 × 3 | R | enclosed structural cover |

### TER-DCK — docking and service interfaces

| Component ID | Description | Envelope | Interface | Build | Notes |
|---|---|---:|---|:---:|---|
| TER-DCK-CLP-S | small docking clamp | 1.5 × 1.5 × 1.5 | S2 | H | shown folded in concepts |
| TER-DCK-CLP-M | medium docking clamp | 2.5 × 2.5 × 2.5 | S3 | H | shown folded in concepts |
| TER-DCK-SKT-S | small landing socket | 2 × 1 × 2 | S2 | H | closed receiving ring |
| TER-DCK-SKT-M | medium landing socket | 3 × 1.5 × 3 | S3 | H | closed receiving ring |
| TER-DCK-SKT-L | heavy landing socket | 4.5 × 2 × 4.5 | S4 | H | closed receiving ring |
| TER-DCK-RFL-M | refuelling coupler | 2 × 2 × 2 | S2 | H | capped when inactive |

### TER-MAN — manipulator roots and folded mounts

| Component ID | Description | Envelope | Footprint | Build | Notes |
|---|---|---:|---:|:---:|---|
| TER-MAN-ROT-S | small rotary root | 1.5 × 1.5 × 1.5 | 1.5 × 1.5 | H | S2 pivot socket |
| TER-MAN-ROT-M | medium rotary root | 2.5 × 2.5 × 2.5 | 2.5 × 2.5 | H | S3 pivot socket |
| TER-MAN-HNG-S | small hinge block | 1 × 1 × 1 | 1 × 1 | H | pivot axis centred on grid |
| TER-MAN-HNG-M | medium hinge block | 2 × 2 × 2 | 2 × 2 | H | pivot axis centred on grid |
| TER-MAN-FLD-S | small folded manipulator mount | 1.5 × 2 × 3 | 1.5 × 2 | H | closed stowed silhouette |
| TER-MAN-FLD-M | medium folded manipulator mount | 2 × 3 × 4.5 | 2 × 3 | H | closed stowed silhouette |
| TER-MAN-FLD-L | large folded manipulator mount | 3 × 4 × 6 | 3 × 4 | H | closed stowed silhouette |

## Usage rules

1. Parent concepts reference the family code (`TER-TNK`); production models reference the exact
   component ID (`TER-TNK-H-M`).
2. Scale a component only within ±10%. Choose another size outside that range so mounting and
   chamfer language remain consistent.
3. **All shared components are separate attachments in the split-generation pipeline.** `R` means
   a component may be reconstructed in isolation; it does not permit that component to be baked
   into a parent building's generated body. `H` components are modelled by hand. Both attach after
   body reconstruction using the specified socket class.
4. Doors, collars, service trunks and docking parts must align to the 0.5 m grid. Never resize
   their connection face independently of the rest of the component.
5. Lights remain inactive and glass remains opaque in concepts. Emission belongs to the engine
   material pass.
6. The line-art silhouettes on the v02 visual sheet clarify mounting orientation only. They are
   not dimensioned orthographic references.
