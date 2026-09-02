# TER-KIT-001 mining modules — production specification v05

Status: **superseded for BLD-MIN-001 by production specification v06** after user review on
2026-08-31. The nine-object sheet remains the visual-generation record; its drill-bit tile is no
longer in Basic Mine production scope.

Visual reference: `TER-KIT-001_mining-modules_concept_v05.png`

This extension closes the shared-library gaps exposed by the Basic Mine. It defines only the
reusable mining parts needed to split `BLD-MIN-001` into a reconstructable structural base and
deliberately modelled machinery. It does not approve generated meshes or replace the broader
family-consolidation work recorded in `TER-KIT-001_component-usage-audit_v01.md`.

Dimensions are width × depth × height in metres. Connection faces use the project S1-S4 socket
contract. `R` means safe to reconstruct in isolation; `H` means manual/procedural production,
although an AI result may be retained as a non-production reference experiment.

## TER-MAN — mining gantry additions

| Exact component ID | Component | Envelope | Receiver | Route | Production note |
|---|---|---:|---|---|---|
| TER-MAN-GAN-L | large portal derrick frame | 10 × 6 × 18 | paired S4 foot pads | H | open bracing, ladders and platforms are hand-modelled; origin centred between feet |
| TER-MAN-HST-M | enclosed hoist head | 4 × 3 × 3 | S3 gantry head | R | closed casing; centred vertical drill-line socket |

## TER-DRL — mining drill modules

| Exact component ID | Component | Envelope | Receiver | Route | Production note |
|---|---|---:|---|---|---|
| TER-DRL-ROT-L | large rotary drill head | 4 × 4 × 5 | S4 axial | H | broad enclosed rotary body; no cable or hose geometry |
| TER-DRL-SFT-L | heavy drill shaft | 1.5 × 1.5 × 10 | S3 axial | H | straight segmented shaft; pivot/axis through centre |
| TER-DRL-BIT-L | large drill bit | 2.5 × 2.5 × 3 | S3 axial | H | thick replaceable cutter; no fragile teeth below the detail floor |

## TER-CNV — enclosed conveyor modules

| Exact component ID | Component | Envelope | Receiver | Route | Production note |
|---|---|---:|---|---|---|
| TER-CNV-ENC-L | large enclosed incline conveyor | 12 × 4 × 4 | S4 end faces | R | sealed transfer housing; no visible belt or ore |
| TER-CNV-JNC-M | enclosed transfer junction | 4 × 4 × 4 | S4 end faces | R | closed three-way processing junction; no open hopper |

## TER-FLU — industrial exhaust additions

| Exact component ID | Component | Envelope | Receiver | Route | Production note |
|---|---|---:|---|---|---|
| TER-FLU-CWL-M | medium capped roof cowl | 2 × 2 × 3 | S2 roof pad | R | broad weather cap; opaque and inactive |
| TER-FLU-STK-M | medium capped exhaust stack | 2 × 2 × 5 | S2 roof pad | R | thick enclosed stack; no smoke or glow |

## BLD-MIN-001 receiver contract

- The structural base owns the foundation slab, low processing-building shells, central drill deck
  and its closed S4 turntable receiver.
- `TER-MAN-GAN-L` uses two paired S4 pads straddling the central drill receiver. The gantry opening
  stays centred on the drill axis.
- `TER-MAN-HST-M`, `TER-DRL-ROT-L`, `TER-DRL-SFT-L` and `TER-DRL-BIT-L` share one vertical axis and
  are never fused into the AI-generated building base.
- `TER-CNV-ENC-L` connects the rear process block to the right processing bunker through two S4
  closed end pads. The body-only base contains neither the conveyor shell nor painted fake belts.
- `TER-FLU-*` modules attach to S2 roof pads and remain separate from antenna and engine families.
- Open rails, ladders and fine gantry braces remain route `H`; reconstruction references for the
  building show only their sockets.

## Approval boundary

The IDs and envelopes above are stable for the Basic Mine trial. Visual concept review, isolated
four-view references, receiver-fit tests and production meshes remain pending. A future consolidated
kit revision may add sizes, but it must not silently rename or repurpose these IDs.
