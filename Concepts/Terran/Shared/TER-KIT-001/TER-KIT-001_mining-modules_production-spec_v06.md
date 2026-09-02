# TER-KIT-001 mining modules — production specification v06

Status: **user-reviewed production scope generated for the BLD-MIN-001 assembly trial**. Eight new
module types remain in scope: five maximum-detail Meshy sources and three textured local
manual-route preview meshes now exist; visual, cleanup and receiver-fit approval remains pending.

Visual reference: `TER-KIT-001_mining-modules_concept_v05.png`. Use only the eight designs named in
this specification. The `TER-DRL-BIT-L` tile is historical and explicitly out of scope for the Basic
Mine.

This extension closes the shared-library gaps exposed by the Basic Mine. It defines only the
reusable mining parts required to combine the textured structural base with visible above-deck
machinery. No component extends below the building foundation.

Dimensions are width × depth × height in metres. Connection faces use the project S1-S4 socket
contract. `R` means safe to reconstruct in isolation; `H` means manual/procedural production,
although an AI result may be retained as a non-production reference experiment.

## TER-MAN — mining gantry additions

| Exact component ID | Component | Envelope | Receiver | Route | Production note |
|---|---|---:|---|---|---|
| TER-MAN-GAN-L | large portal derrick frame | 10 × 6 × 18 | paired S4 foot pads | H | open bracing, ladders and platforms are hand-modelled; origin centred between feet |
| TER-MAN-HST-M | enclosed hoist head | 4 × 3 × 3 | S3 gantry head | R | closed casing; centred vertical drill-line socket |

## TER-DRL — visible drill-support modules

| Exact component ID | Component | Envelope | Receiver | Route | Production note |
|---|---|---:|---|---|---|
| TER-DRL-ROT-L | large rotary drill head | 4 × 4 × 5 | S4 axial | H | broad enclosed rotary body; no cable or hose geometry |
| TER-DRL-SFT-L | visible drill stem | fit to gantry-to-deck gap; 1.5 × 1.5 section | S3 axial | H | model only the visible span from rotary head into the upper deck collar; terminate inside the receiver and create no below-deck geometry |

`TER-DRL-BIT-L` is removed from the Basic Mine production scope. If a future building exposes a
cutter, reactivate or redefine that asset under a later reviewed kit revision rather than producing
it for `BLD-MIN-001`.

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
- `TER-MAN-HST-M`, `TER-DRL-ROT-L` and `TER-DRL-SFT-L` share one vertical axis and are never fused
  into the generated building base.
- `TER-DRL-SFT-L` terminates inside the upper deck receiver. The building has no drill bit, cutter,
  shaft extension or other geometry below the deck/foundation plane.
- `TER-CNV-ENC-L` connects the rear process block to the right processing bunker through two S4
  closed end pads. The body-only base contains neither the conveyor shell nor painted fake belts.
- `TER-FLU-*` modules attach to S2 roof pads and remain separate from antenna and engine families.
- Open rails, ladders and fine gantry braces remain route `H`; reconstruction references for the
  building show only their sockets.

## Approval boundary

The eight IDs and envelopes above are the reviewed scope for the Basic Mine trial. Their source
meshes now load together in `Models/Terran/Buildings/BLD-MIN-001/BLD-MIN-001_trial.assembly.json`.
Visual review, cleanup and final receiver-fit approval remain pending. A future consolidated kit
revision may add sizes, but it must not silently restore the omitted cutter to `BLD-MIN-001`.
