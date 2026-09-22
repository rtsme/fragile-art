# Mauna concept set and style direction — v01

Started 2026-09-14. Race: **Mauna** / folder `Mauna` / code **`MAU`**.
Status: **style direction approved by the owner 2026-09-14** (look, palette and silhouette sheet).
**The Mauna concept set is complete** as of 2026-09-22: 45 buildings, 7 ships, 3 missiles, 3 satellites, 2 environment kits and 9 prop kits (review sheets in `review-shots/`), awaiting owner verdict. Approved so far: the Exchange, the kit sheet, Scoutship v03a, Hauler and Fleet Battleship.

**Asset IDs are race-prefixed** (owner decision 2026-09-14): `MAU-<CATEGORY>-<ROLE>-NNN` for
buildings, props, environment, missiles and satellites (`MAU-BLD-CMD-001`), and `MAU-SHP-NNN`
for ships. Shared-component IDs already start with the race code (`MAU-CLP-…`).

Visual review sheet: `Concepts/Mauna/Direction/MAU-DIR-001_silhouette-sheet_v01.png`
(flat silhouette and palette blocking; **not** an image-generation or Meshy input).
Prompt record: `docs/prompts/MAU-DIR-001-style-direction-v01.md`.

## Why this direction

The Mauna are the one verified race from the original. Per the game spec they colonise, fight and
can be accused like any faction, **and** they run the black market that Federation law forbids
trading with (`FragileRemake/docs/spec/50-diplomacy-agents.md`). The owner chose a
**smuggler-salvage** look: a race whose hardware is visibly acquired, re-purposed and
hidden, not designed from a clean sheet. Every Mauna asset should look like it has more cargo
space than it admits to.

## Faction Styles row (paste into the tracker's `Faction Styles` sheet)

| Field | Mauna |
|---|---|
| Faction | Mauna |
| Style Sign-off Status | Approved |
| Style Sheet Link | `MAU-DIR-001_silhouette-sheet_v01.png` (silhouette intent) and `Buildings/MAU-BLD-CMD-001/MAU-BLD-CMD-001_concept_v01.png` (the approved Exchange, the style anchor) |
| Design Intent | Black-market traders whose technology is acquired, rebuilt and concealed; every machine hides cargo. |
| Shape Language | Rounded cargo-belly hulls (ovoids, capsules) welded to angular salvaged blocks; clamp-collar joints; unequal engine clusters; deliberate asymmetry with a visible counterweight. |
| Materials | Tarnished bronze alloy hull, verdigris-oxidised patch plates, salvaged off-white foreign plating, gunmetal frames and collars, opaque dark glazing. |
| Palette | Bronze and umber body; verdigris secondary; off-white salvage used only as whole welded sections; gunmetal joints; **one controlled accent, Mauna crimson, as flat trade-mark decals only**. |
| Construction Logic | Assembled from whole recovered sections joined by thick clamp collars and welded seams; cargo pods clamp on externally; smuggler compartments are large flush hatches. |
| Mechanical Language | Mismatched thick-walled engine bells of unequal size; enclosed cargo pods; concealed turret cupolas that sit flush when stowed; squat thick-bowl dishes. |
| Lighting / Emissives | In engine only: warm lantern housings at hatches and collars and dim teal cargo-bay light. Concepts show everything unlit. |
| Surface Detail | Few big stepped patch plates with real thickness; weld seams as raised ribs; crimson trade marks as flat stencils; wear heaviest at clamp collars and hatches. |
| Emblem | **Crescent-and-blade** (from the MAU-BLD-CMD-001 v01 concept; reference `Shared/MAU-EMB-001/MAU-emblem_ref_v01.png`). One emblem on every asset, as a flat stencil in crimson or off-white. Owner choice 2026-09-14. |
| Silhouette Rules | Readable from top view by *belly + offset block + unequal engines*; never bilaterally symmetric; one hidden-cargo feature per asset. |
| Prohibited Motifs | Rope, nets, cables, chains, dangling or strapped cargo, open scaffolds, see-through rust holes, tarps, thin aerials, Terran hazard stripes, clean luxury curves, all-over neon. |
| Scale Rules | 1 unit = 1 m; Terran gameplay footprints and S1–S4 receivers; doors 2.2–2.6 m; salvaged sections keep their original (Terran-scale) proportions. |
| Notes | Approved 2026-09-14; the approved Exchange concept is the style anchor. Salvage must be expressed by *mismatched solid masses*, never by broken/open/thin geometry — see "3D-safe salvage" below. |

## 3D-safe salvage: reconciling the look with the concept rules

Scrappy salvage is the look most likely to break `docs/concept-rules-for-3d.md`. These
translations are part of the style, not exceptions to it:

| Salvage idea | Forbidden rendering | Mauna rendering |
|---|---|---|
| Patched hull | painted patch outlines, soft fake seams (B4) | stepped plates ≥ 2% of length, with real thickness, in a different material zone |
| Lashed-on cargo | straps, rope, nets (A5) | enclosed capsule pods seated in **solid clamp collars** (shared `MAU-CLP`) |
| Rust-through damage | holes, see-through gaps (A6, B3) | flat oxidised material zones; silhouette stays closed |
| Improvised aerials | wires, rods, lattice masts (A1, A5) | squat thick-bowl dish on a block mount; solid tapered counterweight towers |
| Stolen parts | tiny mixed greeble (A2) | **whole** foreign sections: one big off-white block welded on, not fragments |
| Hidden compartments | visible interiors, open bays (B1) | large flush hatches, drawn closed |
| Mismatched engines | thin exhaust fins | 2–3 thick-walled bells of clearly unequal size |

## Shared modular-detail library (proposed families)

Kit ID: `MAU-KIT-001`. Exact component IDs and envelopes are defined in its production spec once the
family sheet is approved; the codes below are families, not assembly-ready IDs.

| Code | Family | Route |
|---|---|---|
| MAU-CLP | clamp collars: thick rings and split clamps joining sections and pods, S2–S4 | R |
| MAU-POD | enclosed capsule cargo pods, S/M/L, with collar seats | R |
| MAU-PAT | stepped salvage patch plates, square/irregular, S2–S4 | R |
| MAU-HAT | flush smuggler hatches and cargo shutters, closed state | R |
| MAU-ENG | thick-walled engine bells and nacelle caps in unequal sizes | R |
| MAU-SLV | whole salvaged foreign blocks (off-white, Terran-proportioned) | R |
| MAU-GLZ | opaque slit viewports and dark glazing bands | R |
| MAU-ANT | squat thick-bowl dishes, block sensor heads, tapered solid masts | H for dishes, R for blocks |
| MAU-WPN | concealed cupola turrets with thick barrel shrouds, stowed and deployed | R |
| MAU-CWT | solid tapered counterweight towers and ballast blocks | R |
| MAU-LGT | lantern housings, shown inactive | R |
| MAU-DCK | docking clamps and pod-transfer cradles | R |

## Anchor and first batch

Mirroring the Terran P0 validation batch, anchor first and then the rest:

1. **MAU-BLD-CMD-001 — Exchange** (Mauna Command Centre): a grounded, inverted freighter hull on a
   stepped plinth, turned into a fortified market hall. One welded salvaged block, a clamped pod
   rack, a counterweight tower, a thick-bowl dish and one oversized flush smuggler hatch.
   *Anchor: run it through the full pipeline before anything else.*
2. MAU-SHP-001 Scoutship, MAU-SHP-003 Hauler, MAU-SHP-007 Fleet Battleship: the P0 ships
   (the Terran P0 Scout / Transport / Destroyer, mapped onto the game's hulls).
3. MAU-BLD-MIN-001 Basic Mine, MAU-BLD-MIN-003 Deep Bore Mine, MAU-BLD-PWR-004 Power Plant,
   MAU-BLD-MFG-002 Shipyard, MAU-BLD-LOG-001 Landing Pad, MAU-BLD-DEF-002 Plasma Turret.

## Full asset list (mirrors the Terran set; status `not started` unless stated)

Buildings, props, environment, missiles and satellites keep the Terran functional roles, because the
game's structure list is shared across factions. Only the anchor has a Mauna working title.

| Asset | Name | Status |
|---|---|---|
| MAU-BLD-CMD-001 | Exchange (Command Centre) | concept v01 approved |
| MAU-BLD-CMD-002 | Security Centre | concept v02 generated (re-roll), awaiting verdict |
| MAU-BLD-HAB-001 / 002 / 003 | Residential Block / Living Quarters / Pleasure Dome | concept v01 generated, awaiting verdict |
| MAU-BLD-LIF-001–005 | Medical Centre / Air Processor / Environment Control / Hydration / Hydroponics | all generated, awaiting verdict (001, 003 are v02 re-rolls) |
| MAU-BLD-MIN-001–004 | Basic / Advanced / Deep Bore Mine / Seismic Penetrator | concept v01 generated, awaiting verdict |
| MAU-BLD-STO-001–003 | Ore Storage / Protected Storage Tower / Ore Teleporter | concept v01 generated, awaiting verdict |
| MAU-BLD-PWR-001–005 | Solar Panel / Solar Matrix / Power Store / Power Plant / High-Energy Generator | concept v01 generated, awaiting verdict |
| MAU-BLD-MFG-001–004 | Weapons Factory / Shipyard / Space Dock / Construction Yard | concept v01 generated, awaiting verdict |
| MAU-BLD-LOG-001–004 | Landing Pad / Refuelling Depot / Repair Facility / Cargo Depot | all generated; LOG-002 v02 (stripes removed) and LOG-003 v02 (bay closed) supersede their v01 |
| MAU-BLD-DEF-001–008 | Basic / Plasma / Photon Turret, Anti-Missile Pod, Screen Gen., Missile / Satellite Silo, Bunker | concept v01 generated, awaiting verdict |
| MAU-BLD-SEN-001–002 | Sensor Array / Long Range Transmitter | concept v01 generated, awaiting verdict |
| MAU-BLD-TEC-001–005 | Gravity Nullifier / Asteroid Engine / Shield Gen. / Droid Hub / Teleportation | concept v01 generated, awaiting verdict |
| MAU-SHP-001 | Scoutship | concept v03a approved (v01, v02 rejected; v03b not used) |
| MAU-SHP-002 | Assault Fighter | concept v01 generated, awaiting verdict |
| MAU-SHP-003 | Hauler | concept v01 approved |
| MAU-SHP-004 | Combat Eagle | concept v01 generated, awaiting verdict |
| MAU-SHP-005 | Terminator | concept v01 generated, awaiting verdict |
| MAU-SHP-006 | Command Cruiser | concept v01 generated, awaiting verdict |
| MAU-SHP-007 | Fleet Battleship | concept v01 approved |
| MAU-MIS-ORD-001–003, MAU-SAT-ORB-001–003 | missiles and satellites | all generated, awaiting verdict |
| MAU-ENV-INF-001–002, MAU-PRP-IND-001–007, MAU-PRP-CON-001–002 | environment and prop kits | all generated, awaiting verdict; ENV-INF-001 and PRP-IND-006 fixed at v02 (flat grey field) |

## Ship scale, measured from the generated models (2026-09-14)

Ship size comes from the generated Terran models, not the tracker (owner decision). Meshy output
is normalised to **1.0 on the longest axis**, so the GLBs give *proportions* only. Absolute
in-game size is the per-hull normalisation in `FragileRemake/apps/godot/assets/ships/CREDITS.md`,
in **world units, not metres**.

| Generated model (`Downloaded files/usable/ships/`) | Length : width : height | Game hull | In-game size |
|---|---|---|---|
| `scout.glb` | 1 : 0.70 : 0.32 | Scoutship (`gen_scoutship.glb`) | 0.62 wu |
| `assault fighter.glb` | 1 : 0.80 : 0.26 | Assault Fighter (`gen_assault_fighter.glb`) | 0.66 wu |
| `transporter.glb` | 1 : 0.41 : 0.19 | Hauler (`gen_hauler.glb`, presumed source) | 0.82 wu |
| `battleship.glb` | 1 : 0.45 : 0.14 | Fleet Battleship (`gen_fleet_battleship.glb`) | 1.30 wu |
| `Meshy_AI_Ironwing_Freighter_*.glb` | 1 : 0.94 : 0.25 | not in game | — |

Combat Eagle (0.90), Terminator (1.00) and Command Cruiser (1.10) still use kit models and have no
generated proportions to measure.

## Ship list follows the game's hulls

Owner decision 2026-09-14: the Mauna ship list is the game's **seven hulls**, numbered in the order
of the game's hull table, not the art tracker's twelve Terran ship names. Scoutship, Hauler and
Fleet Battleship prompts use the measured proportions above. Combat Eagle, Terminator and Command
Cruiser have no generated Terran model yet, so their proportions get measured once one exists, or
the owner sets them before those prompts run.
