# TER-KIT-001 Command Centre gap modules — production specification v04

Status: **approved concept and complete four-view reference packages; meshes pending** on 2026-08-31.
Visual reference: `TER-KIT-001_command-centre-gap-modules_concept_v04.png`
Base library: `TER-KIT-001_production-spec_v02.md`
Priority extension: `TER-KIT-001_priority-modules_production-spec_v03.md`

This extension closes the eleven exact-component gaps found by the `BLD-CMD-001` split-pipeline
trial. It inherits the v02 construction grid, socket classes, scale tolerance and material
language. Dimensions are width × depth × height in metres.

`R` means the component may be reconstructed from isolated references. `H` means hand-model or
retopologize deliberately. Neither classification permits baking the component into a building's
base mesh.

## TER-GLZ — command-window additions

| Component ID | Description | Envelope | Mount face | Build | Notes |
|---|---|---:|---:|:---:|---|
| TER-GLZ-BND-M | medium framed window band | 4 × 0.5 × 1.5 | 4 × 1.5 | R | same section as TER-GLZ-BND-L; opaque pane |
| TER-GLZ-BND-CNR | 135-degree exterior band corner | 2 × 2 × 1.5 | two 2 × 1.5 faces | R | both legs share the BND-M/L frame section |

The corner module's 135-degree exterior angle matches the faceted Command Centre command block.
Do not mirror one pane through the corner; the structural corner post remains a solid shared frame.

## TER-DOR — entrance addition

| Component ID | Description | Envelope | Interface | Build | Notes |
|---|---|---:|---|:---:|---|
| TER-DOR-PRT-L | large fortified entrance portal | 6 × 2 × 5 | S4 wall/ground | R | surround only; TER-DOR-CGO-L remains a separate insert |

The portal is a closed projecting frame. Its clear internal opening is 4.75 × 4.25 m so the cargo
door can sit behind it without z-fighting. The portal and door must remain independently reusable.

## TER-VNT — fan addition

| Component ID | Description | Envelope | Mount face | Build | Notes |
|---|---|---:|---:|:---:|---|
| TER-VNT-FAN-L | large enclosed axial fan housing | 4 × 1.5 × 4 | 4 × 4 | H | five broad blades; deep housing; no thin grille |

Produce the housing and fan rotor as separate child meshes under one shared-asset root. The rotor
may remain static in the initial game asset but must have a centred pivot.

## TER-PIP — trunk-routing additions

| Component ID | Description | Envelope | Connection | Build | Notes |
|---|---|---:|---|:---:|---|
| TER-PIP-ELB-M | enclosed 90-degree trunk elbow | 2.5 × 2.5 × 1.5 | two S2 inline ends | R | square section matches TER-PIP-TRK-M |
| TER-PIP-TEE-M | enclosed three-way trunk junction | 3 × 2 × 1.5 | three S2 inline ends | R | branch centre snaps to 0.5 m grid |

All openings are capped in concept/reference renders. Production connection faces may be opened
only after reconstruction and must preserve the S2 footprint.

## TER-ACC — access additions

| Component ID | Description | Envelope | Interface | Build | Notes |
|---|---|---:|---|:---:|---|
| TER-ACC-RMP-L | long enclosed access ramp/landing | 4 × 8 × 2 | S4 door/ground | R | solid side cheeks; 1:8 nominal incline |
| TER-ACC-RAL-M | medium guardrail run | 4 × 0.3 × 1.2 | S1 at each end | H | thick posts and two robust rails |
| TER-ACC-RAL-CNR | 90-degree guardrail corner | 1 × 1 × 1.2 | two S1 endpoints | H | same post and rail section as RAL-M |

The rail assets are exceptions to the body-reconstruction thin-element rule because they are
modelled in isolation or by hand. Do not include them in any parent reference image used for mesh
generation.

## TER-ANT — aerial-tip additions

| Component ID | Description | Envelope | Socket | Build | Notes |
|---|---|---:|---|:---:|---|
| TER-ANT-AER-S | short aerial tip | 0.5 × 0.5 × 1.5 | S1 | H | minimum shaft diameter 0.25 m |
| TER-ANT-AER-M | medium aerial tip | 0.5 × 0.5 × 2.5 | S1 | H | minimum shaft diameter 0.3 m |

Both aerials use a chunky enclosed base and a single solid tapered shaft. No wires, loops or
crossbars. Their S1 bases fit the top sockets on TER-ANT-MST-S/M/L.

## Production order

1. Use the completed isolated references in `References/Terran/Shared/<Component ID>/`.
2. Generate the six `R` components and hand-model or deliberately retopologize the five `H`
   components.
3. Validate scale, origin, forward axis and socket footprint against this specification.
4. Apply the Terran shared-detail material set described in `docs/material-assembly-pipeline.md`.
5. Test all eleven on the `BLD-CMD-001` base before approving them for wider concept reuse.
