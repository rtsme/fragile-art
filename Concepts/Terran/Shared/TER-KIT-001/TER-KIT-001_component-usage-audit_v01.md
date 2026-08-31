# TER-KIT-001 concept component-usage audit — v01

Audit date: 2026-08-31
Scope: all **75 current Terran concept sheets** selected by
`Concepts/Terran/terran-concept-manifest-v01.md`
Shared-library baseline: `TER-KIT-001_shared-detail-library_concept_v02.png` and
`TER-KIT-001_production-spec_v02.md`

## Result

The v02 library is a valid visual anchor, but it is **not a complete inventory of the reusable
assets depicted across the concept set**.

- The current library contains 12 families and 72 specified components.
- Five existing families need substantial expansion from already-approved specialist kit
  concepts: `TER-TNK`, `TER-ANT`, `TER-PIP`, `TER-MAN`, and the combined
  `TER-PAR`/`TER-ACC`/`TER-BRC` construction group.
- Sixteen additional reusable families occur in two or more concepts and should be added to the
  shared production library.
- Seven concepts were identified for a new concept pass because the missing component was their
  dominant readable feature.
- Known hand-model references and asset-specific hero structures should be retained; they do not
  justify changing otherwise valid body concepts.

The audit records visible functional forms, not every painted seam or armour plate. A family is
considered recurring when the same functional component appears in at least two current concepts,
even when image generation changed its exact proportions.

### Resolution update — priority pass complete

The first priority pass was completed on 2026-08-31:

- `TER-KIT-001_priority-modules_concept_v03.png` and its companion production specification now
  define `TER-GLZ`, `TER-SOL`, `TER-ROT`, `TER-WPN`, `TER-PWR`, `TER-LCH`, plus `TER-ANT` additions.
- BLD-LIF-005, BLD-PWR-001, BLD-PWR-002 and BLD-DEF-001 through BLD-DEF-004 were revised and the
  manifest now selects their v02 concepts.
- Ten newly proposed families remain for later consolidation: `TER-FND`, `TER-RMP`, `TER-FLU`,
  `TER-CNV`, `TER-BUL`, `TER-CRT`, `TER-ENG`, `TER-LDG`, `TER-ORD` and `TER-DRL`.
- The specialist expansions to `TER-PIP`, `TER-TNK`, `TER-MAN`, and the construction group remain
  outstanding. `TER-ANT` received only the priority panel/pivot additions in this pass.

## Current v02 family usage

These counts come from the manifest's per-asset mappings and were checked against the contact-sheet
review. The manifest remains the detailed source for the individual asset-to-family mapping.

| Existing family | Concepts mapped | Coverage verdict |
|---|---:|---|
| TER-PNL | 75 | keep; sufficient base range |
| TER-LGT | 75 | keep; sufficient base range |
| TER-ACC | 54 | expand with ramps and construction access modules |
| TER-PAR | 47 | expand with foundation-edge and construction barriers |
| TER-DOR | 29 | keep; add heavy hangar-door size during modelling |
| TER-TNK | 29 | materially under-specified; import specialist vessel variants |
| TER-DCK | 28 | keep; add landing-gear interfaces and heavy service sockets |
| TER-BRC | 27 | expand from the construction-kit concept |
| TER-VNT | 27 | keep; sufficient base range |
| TER-PIP | 20 | materially under-specified; import the full pipe topology set |
| TER-ANT | 15 | materially under-specified; import panel sensors and mast variants |
| TER-MAN | 14 | materially under-specified; import arm, gantry and end-effector variants |

The exact 72 current component IDs are listed in `TER-KIT-001_production-spec_v02.md`.

## Existing specialist concepts that already contain shared assets

These concepts should be treated as source catalogues, not as unrelated one-off props. Their useful
variants need exact IDs, dimensions and socket classes in a future consolidated production spec.

| Source concept | Reusable assets depicted | Required integration |
|---|---|---|
| ENV-INF-001 | square, rectangular and octagonal foundation pads; deck tiles; pad edges; access tiles; equipment sockets | create `TER-FND`; route its ramps to `TER-RMP` |
| ENV-INF-002 | straight, curved, sloped, T and cross road sections; roadside service blocks | create `TER-FND` road subset |
| PRP-IND-001 | straight, inclined and curved conveyors; X/T/Y junctions; transfer sections | create `TER-CNV` |
| PRP-IND-002 | sealed ore containers, open bulk bins and hopper containers | create `TER-BUL` and share sealed forms with `TER-CRT` |
| PRP-IND-003 | power nodes, junctions, trunks, couplers and damaged-state node | create `TER-PWR`; use `TER-PIP` for passive trunks |
| PRP-IND-004 | straight pipes, elbows, tees, crosses, valves, reducers, caps, trunks, saddles and supports | expand `TER-PIP` |
| PRP-IND-005 | vertical, horizontal, domed, legged, hopper and rectangular vessels | expand `TER-TNK` |
| PRP-CON-001 | overhead crane beams, gantries, articulated arms, hinge segments, hooks, grippers and tool heads | expand `TER-MAN` |
| PRP-CON-002 | foundation slabs, construction shells, barriers, ramps, braces and equipment boxes | expand `TER-FND`, `TER-RMP`, `TER-PAR`, `TER-ACC` and `TER-BRC` |
| PRP-IND-006 | sealed crates, long cases, pallets, bundled loads, drums and fluid containers | create `TER-CRT` |
| PRP-IND-007 | dishes, flat sensor panels, masts, radar heads, sensor boxes and equipment bases | expand `TER-ANT` |
| MAT-TER-001 | armour colours, hazard panels, inset panels, solar-cell finish and bumper/trim treatments | retain as the surface-material authority; no geometry family |

## Recurring assets missing from the shared library

Every row below has multiple visual occurrences. “Add” means extend the production library first;
it does not automatically require repainting every concept.

| Proposed family | Reusable assets | Visual occurrence evidence | Count | Resolution |
|---|---|---|---:|---|
| TER-FND | foundation slabs, pad tiles, deck edges, road straights/curves/junctions | ENV-INF-001, ENV-INF-002, BLD-MIN-001, BLD-STO-003, BLD-LOG-001, BLD-LOG-002, BLD-MFG-004, BLD-TEC-005, PRP-CON-002 | 9 | add from the existing environment and construction-kit concepts |
| TER-RMP | personnel ramps, cargo ramps, service aprons and ramp end caps | ENV-INF-001, BLD-CMD-001, BLD-HAB-002, BLD-LIF-001, BLD-HAB-003, BLD-CMD-002, BLD-LIF-003, BLD-LIF-004, BLD-LIF-005, BLD-MIN-002, BLD-STO-002, BLD-STO-003, BLD-PWR-001, BLD-PWR-003, BLD-PWR-005, BLD-MFG-001, BLD-LOG-001, BLD-LOG-004, BLD-MFG-004, BLD-DEF-001, BLD-DEF-003, BLD-DEF-005, BLD-DEF-006, BLD-SEN-001, BLD-SEN-002, BLD-TEC-001, BLD-TEC-003, BLD-TEC-004, BLD-TEC-005, PRP-CON-002 | 30 | add; replace generated ramp variants during model cleanup |
| TER-GLZ | flat opaque window bands, framed viewports, cockpit panes and greenhouse roof panels | BLD-CMD-001, BLD-HAB-001, BLD-HAB-002, BLD-LIF-001, BLD-HAB-003, BLD-LIF-003, BLD-LIF-005, BLD-MIN-002, BLD-STO-002, BLD-MFG-002, BLD-LOG-003, SHP-TER-001, SHP-TER-002, SHP-TER-003, SHP-TER-004, SHP-TER-005, SHP-TER-007, SHP-TER-008, SHP-TER-009, SHP-TER-010, SHP-TER-011, SHP-TER-012 | 22 | add; all glazing is one opaque dark value in reconstruction sources |
| TER-FLU | exhaust stacks, capped flues, roof cowls and industrial chimneys | BLD-CMD-001, BLD-HAB-001, BLD-LIF-002, BLD-LIF-003, BLD-MIN-001, BLD-PWR-003, BLD-MFG-002 | 7 | add; keep separate from antenna masts and engine nozzles |
| TER-SOL | framed solar panels, deployable panel wings, hinges and panel roots | BLD-CMD-002, BLD-PWR-001, BLD-PWR-002, SAT-ORB-002, SAT-ORB-003 | 5 | add; dominant-panel concepts require a consistency pass |
| TER-CNV | conveyors, enclosed transfer belts, inclines, junctions and chutes | BLD-MIN-001, BLD-MIN-002, BLD-STO-001, BLD-MFG-001, BLD-MFG-004, PRP-IND-001 | 6 | add from PRP-IND-001; hand-model moving/open belt detail |
| TER-BUL | open bulk bins, ore hoppers, discharge chutes and sealed ore containers | BLD-MIN-002, BLD-STO-001, BLD-STO-002, BLD-MFG-004, PRP-IND-002 | 5 | add from PRP-IND-002; reuse `TER-TNK` only for fully enclosed vessels |
| TER-CRT | cargo crates, equipment cases, pallet loads, drums and modular freight pods | BLD-LOG-004, BLD-MFG-004, SHP-TER-005, SHP-TER-009, SHP-TER-010, PRP-IND-006 | 6 | add from PRP-IND-006; ship pods receive `TER-DCK` sockets |
| TER-PWR | power nodes, capacitor banks, induction coils, bus blocks and energy-cell housings | BLD-PWR-003, BLD-PWR-004, BLD-PWR-005, PRP-IND-003, BLD-DEF-005, BLD-TEC-001, BLD-TEC-003, MIS-ORD-002 | 8 | add; use closed inactive housings in reconstruction concepts |
| TER-WPN | gun receivers, barrels, muzzle shrouds and compact weapon turrets | BLD-DEF-001, BLD-DEF-002, BLD-DEF-003, SHP-TER-002, SHP-TER-003, SHP-TER-004, SHP-TER-006, SHP-TER-007, SHP-TER-008, SAT-ORB-001, SAT-ORB-002 | 11 | add as a hand-model family; revise defence concepts where it is the hero silhouette |
| TER-LCH | missile-cell faces, launch tubes, pod housings, magazines and silo adapters | BLD-DEF-004, BLD-DEF-006, BLD-DEF-007, SHP-TER-006, SHP-TER-007, SHP-TER-011, SAT-ORB-002 | 7 | add as a hand-model family; keep doors and caps closed in reconstruction sources |
| TER-ROT | bearing rings, traverses, turntables, iris rings and heavy circular hatches | BLD-PWR-001, BLD-PWR-002, BLD-DEF-001, BLD-DEF-002, BLD-DEF-003, BLD-DEF-004, BLD-DEF-006, BLD-SEN-001, BLD-TEC-001, BLD-TEC-005, SAT-ORB-002 | 11 | add; standardize S2/S3/S4 rotational interfaces |
| TER-ENG | ship engine pods, main nozzles, manoeuvring thrusters and missile motor bells | BLD-TEC-002, SHP-TER-001, SHP-TER-002, SHP-TER-003, SHP-TER-004, SHP-TER-005, SHP-TER-006, SHP-TER-007, SHP-TER-008, SHP-TER-009, SHP-TER-010, SHP-TER-011, SHP-TER-012, MIS-ORD-001, MIS-ORD-002, MIS-ORD-003, SAT-ORB-001, SAT-ORB-002, SAT-ORB-003 | 19 | add as a hand-model family; body concepts retain only closed engine sockets |
| TER-LDG | landing feet, skids, telescoping gear roots and ground-contact pads | SHP-TER-005, SHP-TER-009, SHP-TER-012 | 3 | add as a hand-model family using `TER-DCK` sockets |
| TER-ORD | missile nose modules, guidance sections, control fins and motor adapters | MIS-ORD-001, MIS-ORD-002, MIS-ORD-003, BLD-DEF-004, BLD-DEF-006 | 5 | add as an ordnance kit; fins remain hand-model only |
| TER-DRL | drill heads, augers, bore shafts, rotary roots and penetrator tips | BLD-MIN-001, BLD-MIN-002, BLD-MIN-003, BLD-MIN-004, PRP-CON-001 | 5 | add as a hand-model mining kit; preserve class-specific sizes |

## Existing families that need more components

| Family | Missing components visible in concepts | Source to use |
|---|---|---|
| TER-PIP | 90-degree elbows in S/M/L, tees, crosses, reducers, U-bends, caps, pipe saddles, floor supports and larger valve blocks | PRP-IND-004 |
| TER-TNK | legged vertical tanks, domed vessels, box reservoirs, small paired cylinders, enclosed hoppers and additional horizontal sizes | PRP-IND-005 and PRP-IND-002 |
| TER-ANT | flat sensor panels, angled panel mounts, additional radar heads, mast caps, sensor boxes and low-profile antenna bases | PRP-IND-007 |
| TER-MAN | straight overhead rails, portal gantries, boom segments, telescoping arms, hooks, grippers, drills and folded-arm assemblies | PRP-CON-001 |
| TER-PAR / TER-ACC / TER-BRC | construction barriers, floor-edge pieces, solid service ramps, ramp end caps, low access blocks and additional enclosed brace shapes | PRP-CON-002 and ENV-INF-001 |
| TER-DCK | landing-gear sockets, ship cargo-pod latches, heavy refuelling faces and larger dock collars | SHP-TER-005, SHP-TER-009, SHP-TER-012 and BLD-LOG-002 |

## Concept revision decisions

### Revise after the relevant family is approved

These concepts use a missing shared component as a dominant gameplay-readable silhouette. A new
concept version is cheaper and safer than asking modelling to reconcile incompatible hero forms.

| Concept | Reason | Required family first |
|---|---|---|
| BLD-LIF-005 — Hydroponics Plant | greenhouse roof reads as translucent/interior-rich glazing, conflicting with the opaque-glass rule | TER-GLZ |
| BLD-PWR-001 — Solar Panel | the panel, hinge and traverse are the entire asset identity | TER-SOL, TER-ROT |
| BLD-PWR-002 — Solar Matrix | panel wings and pivots dominate the silhouette | TER-SOL, TER-ROT |
| BLD-DEF-001 — Basic Turret | receiver, barrel and traverse are the hero form | TER-WPN, TER-ROT |
| BLD-DEF-002 — Plasma Turret | receiver, muzzle and traverse are the hero form | TER-WPN, TER-ROT, TER-PWR |
| BLD-DEF-003 — Photon Turret | twin receivers, muzzles and traverse are the hero form | TER-WPN, TER-ROT |
| BLD-DEF-004 — Anti-Missile Pod | launch-cell face and sensor mount are the hero form | TER-LCH, TER-ROT, TER-ANT |

SAT-ORB-002 and SAT-ORB-003 should not be remade immediately. Their solar panels are detachable
hand-model parts, so the approved bodies can use closed panel-root sockets and receive TER-SOL
components after reconstruction.

### Retain as hand-model or split-reference concepts

| Concept group | Reason to retain |
|---|---|
| BLD-CMD-001 | approved faction anchor; dishes, rails, lights and exposed pipework are explicitly hand-model parts |
| BLD-MIN-001 | open derrick documents the intended machine, but is excluded from body reconstruction and built with TER-DRL/TER-MAN parts |
| PRP-CON-001 and PRP-CON-002 | these are catalogues for deliberate hand modelling, not single generated bodies |
| MIS-ORD-001 through MIS-ORD-003 | bodies remain useful; fins, seekers and motors are replaced with TER-ORD/TER-ENG parts |
| SAT-ORB-001 through SAT-ORB-003 | bodies remain useful; dishes, panels, guns and thrusters are attached shared components |
| SHP-TER-001 through SHP-TER-012 | hull silhouettes remain class-specific; engines, guns, landing gear and cargo sockets are modular attachments |

## One-off geometry that should remain asset-specific

The following forms do not recur enough, or carry too much identity, to become shared components:

- BLD-HAB-003 pleasure-dome shell and crown.
- BLD-STO-003 teleporter drum and upper transfer deck.
- BLD-PWR-005 central high-energy containment assembly.
- BLD-MFG-003 closed segmented space-dock aperture.
- BLD-TEC-002 asteroid rock shroud and main embedded engine body.
- BLD-TEC-004 construction-droid garage body and the droids themselves.
- BLD-TEC-005 teleportation arch pylons.
- Ship hull armour masses, bridges and class-specific wing/body silhouettes.

## Production gate

Before a concept advances to orthographic references:

1. Map every visible reusable part to either an exact current component ID, an approved new-family
   placeholder, or an explicit asset-specific body feature.
2. Do not mint an asset-local variant when an approved shared component performs the same function.
3. If a missing family appears in a second concept, stop and add it to this audit and to the shared
   production specification before generating more references.
4. If the missing family controls the concept's dominant silhouette, revise the concept after the
   family is approved. Otherwise retain the body and replace the part during model cleanup.
5. Hand-model families attach through S1-S4 sockets; their thin or open geometry is never included
   in image-to-3D body reconstruction.
