# TER-KIT-001 priority modules — production specification v03

Status: **approved for concept reuse** on 2026-08-31.
Visual reference: `TER-KIT-001_priority-modules_concept_v03.png`
Base library: `TER-KIT-001_production-spec_v02.md`

This extension defines the seven families needed to resolve the first concept-consistency gate.
It inherits the v02 units, 0.5 m construction grid, S1-S4 sockets, materials and reconstruction
rules. Dimensions are width × depth × height in metres.

## TER-GLZ — opaque glazing modules

| Component ID | Description | Envelope | Mount face | Build | Notes |
|---|---|---:|---:|:---:|---|
| TER-GLZ-PNL-S | small opaque pane | 1 × 0.25 × 1 | 1 × 1 | R | one near-black value |
| TER-GLZ-PNL-M | medium opaque pane | 2 × 0.25 × 1.5 | 2 × 1.5 | R | one near-black value |
| TER-GLZ-PNL-L | large opaque pane | 4 × 0.3 × 2.5 | 4 × 2.5 | R | one near-black value |
| TER-GLZ-BND-L | framed window-band module | 6 × 0.5 × 1.5 | 6 × 1.5 | R | thick structural frame |
| TER-GLZ-ROF-M | medium greenhouse roof bay | 4 × 0.5 × 3 | 4 × 3 | R | opaque; no visible interior |
| TER-GLZ-ROF-L | large greenhouse roof bay | 6 × 0.5 × 4 | 6 × 4 | R | opaque; no visible interior |

## TER-SOL — solar panel modules

| Component ID | Description | Envelope | Socket | Build | Notes |
|---|---|---:|---|:---:|---|
| TER-SOL-TIL-S | framed solar tile | 2 × 0.25 × 2 | S2 | H | rigid inactive cell surface |
| TER-SOL-PNL-M | medium framed panel | 4 × 0.35 × 4 | S3 | H | repeatable cell matrix |
| TER-SOL-PNL-L | large framed panel | 8 × 0.5 × 4 | S4 | H | used by BLD-PWR-001 |
| TER-SOL-WNG-L | long radial panel wing | 10 × 0.5 × 4 | S4 | H | repeated six times on BLD-PWR-002 |
| TER-SOL-HNG-M | medium folded hinge/root | 2 × 2 × 2.5 | S3 | H | closed folded silhouette |
| TER-SOL-HNG-L | large folded hinge/root | 3 × 3 × 3.5 | S4 | H | closed folded silhouette |

The cell matrix is a material subdivision inside the fixed frame. It may vary with panel length;
the frame, root and socket—not the painted cell count—define interchangeability.

## TER-ROT — rotational interfaces

| Component ID | Description | Envelope | Interface | Build | Notes |
|---|---|---:|---|:---:|---|
| TER-ROT-S2 | small enclosed bearing | 2 × 2 × 1 | S2 | R | closed top during reconstruction |
| TER-ROT-S3 | medium enclosed traverse | 3 × 3 × 1.5 | S3 | R | accepts medium modules |
| TER-ROT-S4 | heavy enclosed turntable | 4.5 × 4.5 × 2 | S4 | R | accepts solar, weapon or launcher roots |

## TER-WPN — gun modules

| Component ID | Description | Envelope | Interface | Build | Notes |
|---|---|---:|---|:---:|---|
| TER-WPN-RCV-S | small enclosed receiver | 2 × 3 × 2 | S2 | H | closed rectangular body |
| TER-WPN-RCV-M | medium enclosed receiver | 3 × 5 × 3 | S3 | H | BLD-DEF-001 and BLD-DEF-003 |
| TER-WPN-RCV-L | large enclosed receiver | 4 × 7 × 4 | S4 | H | BLD-DEF-002 |
| TER-WPN-BRL-S | short thick barrel/shroud | 1 × 2 × 1 | S2 | H | no unsupported thin bore |
| TER-WPN-BRL-M | medium thick barrel/shroud | 1.5 × 4 × 1.5 | S3 | H | rectangular outer shroud |
| TER-WPN-BRL-L | large thick barrel/shroud | 2 × 5 × 2 | S4 | H | rectangular outer shroud |
| TER-WPN-MZL-PLS | wide plasma muzzle module | 3 × 2 × 3 | S4 | H | flat opaque dark muzzle; no glow |

## TER-PWR — power equipment modules

| Component ID | Description | Envelope | Socket | Build | Notes |
|---|---|---:|---|:---:|---|
| TER-PWR-NOD-S | compact power node | 2 × 2 × 2 | S2 | R | inactive housing |
| TER-PWR-NOD-M | medium power node | 3 × 3 × 3 | S3 | R | inactive housing |
| TER-PWR-CAP-M | medium capacitor bank | 2 × 1.5 × 3 | S2 | H | enclosed broad loops or ribs |
| TER-PWR-CAP-L | large capacitor bank | 3 × 2 × 4 | S3 | H | enclosed broad loops or ribs |
| TER-PWR-IND-L | enclosed induction housing | 4 × 3 × 4 | S4 | H | no exposed fine coil or glow |

## TER-LCH — launcher modules

| Component ID | Description | Envelope | Interface | Build | Notes |
|---|---|---:|---|:---:|---|
| TER-LCH-POD-2 | 2 × 2 closed-cell pod | 3 × 2 × 3 | S3 | H | four identical capped cells |
| TER-LCH-POD-3 | 3 × 3 closed-cell pod | 4 × 2.5 × 4 | S4 | H | nine identical capped cells |
| TER-LCH-POD-4 | 4 × 4 closed-cell pod | 5 × 3 × 5 | S4 | H | sixteen identical capped cells |
| TER-LCH-TUB-S | small capped tube adapter | 1 × 1.5 × 1 | S2 | H | cap closed by default |
| TER-LCH-TUB-M | medium capped tube adapter | 1.5 × 2 × 1.5 | S3 | H | cap closed by default |
| TER-LCH-MAG-L | large enclosed magazine | 4 × 3 × 4 | S4 | H | no visible ammunition |

## TER-ANT — v03 additions

These extend the v02 `TER-ANT` catalogue without replacing its dishes, radar heads or mast bases.

| Component ID | Description | Envelope | Socket | Build | Notes |
|---|---|---:|---|:---:|---|
| TER-ANT-PNL-S | small flat sensor panel | 1.5 × 0.5 × 1.5 | S2 | H | thick rigid slab |
| TER-ANT-PNL-M | medium flat sensor panel | 2.5 × 0.75 × 2.5 | S3 | H | thick rigid slab |
| TER-ANT-PNL-L | large flat sensor panel | 4 × 1 × 4 | S4 | H | thick rigid slab |
| TER-ANT-RDR-L | large block radar head | 3.5 × 3 × 3 | S4 | H | closed dark sensor face |
| TER-ANT-PVT-S | small enclosed sensor pivot | 1.5 × 1.5 × 1.5 | S2 | H | no exposed axle |
| TER-ANT-PVT-M | medium enclosed sensor pivot | 2.5 × 2.5 × 2 | S3 | H | no exposed axle |

## Approved concept mappings

| Concept | Shared modules introduced by this pass |
|---|---|
| BLD-LIF-005 v02 | TER-GLZ-ROF-M/L, TER-GLZ-PNL-M/L |
| BLD-PWR-001 v02 | TER-SOL-PNL-L, TER-SOL-HNG-L, TER-ROT-S4 |
| BLD-PWR-002 v02 | TER-SOL-WNG-L, TER-SOL-HNG-M, TER-ROT-S4 |
| BLD-DEF-001 v02 | TER-WPN-RCV-M, TER-WPN-BRL-M, TER-ROT-S3 |
| BLD-DEF-002 v02 | TER-WPN-RCV-L, TER-WPN-MZL-PLS, TER-PWR-CAP-L, TER-ROT-S4 |
| BLD-DEF-003 v02 | two TER-WPN-RCV-M/BRL-M sets, TER-ROT-S4, TER-ANT-RDR-S |
| BLD-DEF-004 v02 | TER-LCH-POD-4, TER-ROT-S4, TER-ANT-RDR-S, TER-ANT-DSH-S |
