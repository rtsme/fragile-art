# BLD-MIN-001 — Basic Mine assembly manifest v01

Status: **base and eight mining modules generated; coordinate-led fit rejected; contact-surface correction pending render**
Final appearance target: `BLD-MIN-001_concept_v03.png`
Body-only source: `Base/BLD-MIN-001_base-concept_v02.png`
Approved reference package: `../../../References/Terran/Buildings/BLD-MIN-001/Base/BLD-MIN-001_base_reference-sheet_v12.png`
Production envelope: **45 × 32 × 26 m**

The final concept is authoritative for the dressed appearance. The body-only source is authoritative
only for the geometry allowed into image-to-3D base generation. Counts describe the visible v03
concept; rear-face quantities remain provisional until the consistent four-view package is reviewed.

## Structural forms retained in the base

- integrated 45 × 32 m foundation/deck slab and broad edge masses
- low left utility shell, front control/service shells and right processing-bunker shell
- central raised octagonal drill deck with one closed S4 axial receiver
- broad structural steps, deep setbacks, bold chamfers and silhouette-defining wall buttresses
- paired S4 gantry foot pads, two S4 conveyor end pads, S2/S3 service pads and closed recesses

## Existing shared-library assets

| Exact component ID | Trial qty | Receiver | Intended use |
|---|---:|---|---|
| TER-ROT-S4 | 1 | central S4 axial recess | enclosed drill turntable/rotary interface |
| TER-TNK-V-M | 3 | 3 × 3 m ground pads | rear-right process vessel bank |
| TER-VNT-FAN-L | 2 | S3 roof recesses | large enclosed roof extraction fans |
| TER-VNT-LVR-M | 4 | 2.5 × 2.5 m wall recesses | bunker and utility-shell ventilation |
| TER-PIP-TRK-L | 2 | S3 endpoints | long process-service trunks |
| TER-PIP-TRK-M | 4 | S2 endpoints | short process-service trunks |
| TER-PIP-ELB-M | 8 | S2 inline | enclosed trunk turns |
| TER-PIP-TEE-M | 2 | S2 inline | enclosed service junctions |
| TER-PIP-CPL-M | 6 | S2 inline | visible trunk couplers |
| TER-PIP-VLV-M | 2 | S2 inline | service isolation blocks |
| TER-DOR-AIR-M | 2 | wall recess | front personnel airlocks |
| TER-DOR-HTC-S | 2 | wall recess | service hatches |
| TER-ACC-STP | 4 | 1 × 1 m ground pads | service steps |
| TER-ACC-RAL-M | 14 | S1 deck-edge sockets | straight safety-rail runs |
| TER-ACC-RAL-CNR | 10 | S1 deck-edge sockets | safety-rail corners/returns |
| TER-PNL-ACS-M | 8 | 1.5 × 1.5 m wall pads | maintenance panels |
| TER-PNL-EQB-M | 5 | S2 wall/roof pads | equipment boxes |
| TER-PNL-SKT-S | 12 | S1 surface recesses | light/detail receivers |
| TER-PNL-SKT-M | 8 | S2 surface recesses | equipment/service receivers |
| TER-LGT-WRK-M | 10 | S1 | inset work lights |
| TER-LGT-BCN-S | 8 | S1 | perimeter and machinery warning beacons |

## Mining-kit extension assets

Defined by `../../Shared/TER-KIT-001/TER-KIT-001_mining-modules_production-spec_v06.md`.

| Exact component ID | Trial qty | Receiver | Intended use |
|---|---:|---|---|
| TER-MAN-GAN-L | 1 | paired S4 deck pads | open portal derrick frame |
| TER-MAN-HST-M | 1 | S3 gantry-head socket | enclosed hoist head |
| TER-DRL-ROT-L | 1 | S4 axial | suspended rotary drill head |
| TER-DRL-SFT-L | 1 | S3 axial | visible drill stem from rotary head into the upper deck receiver |
| TER-CNV-ENC-L | 1 | two S4 end faces | sealed inclined conveyor housing |
| TER-CNV-JNC-M | 1 | S4 end faces | closed transfer junction at process bunker |
| TER-FLU-CWL-M | 1 | S2 roof pad | low capped dust-extraction cowl |
| TER-FLU-STK-M | 1 | S2 roof pad | rear process exhaust stack |

## Explicit base exclusions

- the complete derrick, crosshead, hoist, rotary head and visible drill stem; no cutter or
  subsurface drill geometry exists in the reviewed assembly scope
- the enclosed conveyor and transfer junction
- tanks, pipes, valves, vents, fans, flues and dust-extraction fittings
- doors, hatches, railings, ladders, lights, beacons, panels and equipment boxes
- building-specific decals and labels, emissive effects, painted fake geometry and fine greeble

No omitted item may be painted onto the generated base. The base receives only closed pads or
recesses on the 0.5 m construction grid.

## Review notes

- The v03 concept deliberately retains an open derrick as a hand-model reference. It is not a valid
  body-reconstruction form and must disappear from the base concept.
- The enclosed conveyor remains a separate reusable module because it recurs across mining,
  storage and manufacturing assets.
- Quantities are frozen for the visible concept pass. Update this manifest before changing counts
  after rear/side reference review.
- User review removes the separate drill-bit/cutter asset and all subsurface drill geometry from this
  building. Keep only the above-deck support assembly and the visible start of the drill stem, which
  terminates inside the upper deck receiver. Nothing is modelled beneath the building foundation.
- The textured v12 four-view package passes the production alignment gate with 183–185 px silhouette
  heights, 0.24% vertical-centre drift and no validator issues. It is approved as the input package
  for body-only 3D generation.
- Meshy task `01a059f4-8b63-7428-8c59-900835e146cd` generated the maximum-detail textured source
  `../../../../Models/Terran/Buildings/BLD-MIN-001/Base/BLD-MIN-001_base_hq_v01.glb` for 30 credits.
  The GLB and five PBR maps pass structural validation; visual silhouette, material and receiver-fit
  review remains pending.
- Five reconstruction-safe mining modules were generated as separate 4K-PBR Meshy sources for 150
  credits; the gantry, rotary head and visible stem were built as textured local procedural GLBs.
  All eight load with the base in `../../../../Models/Terran/Buildings/BLD-MIN-001/BLD-MIN-001_trial.assembly.json`.
  The trial currently uses 23 instances from 14 source GLBs; sixteen smaller general shared types
  remain pending and the first-pass receiver coordinates require visual approval.
- Receiver-fit scene `../../../../Models/Terran/Buildings/BLD-MIN-001/BLD-MIN-001_receiver-fit_v02.assembly.json`
  records 22 named receivers without replacing the v01 trial. Its coordinate-led rendered pass was
  rejected because shared assets remained visibly unsupported. The current saved correction uses
  measured base-mesh contact heights, pitches the conveyor between process roofs and withholds four
  incomplete standalone pipe fittings from preview. Structural, source-file and production-envelope
  checks pass. The existing `../../../../Models/Terran/Buildings/BLD-MIN-001/BLD-MIN-001_receiver-fit_v02_review/`
  images document the rejected pass; a replacement rendered review set is still required.
