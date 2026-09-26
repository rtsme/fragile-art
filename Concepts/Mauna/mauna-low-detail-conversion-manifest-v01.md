# Mauna low-detail Meshy conversion — v01

Generated 2026-09-26, mirroring `Concepts/Terran/low-detail-conversion-manifest-v01.md`.
Scope: **52 assets** — all 45 buildings and all 7 ships. Each low-detail concept was generated from
that asset's own approved Mauna concept, which stays the dressed appearance target.

Prompts and run record: `docs/prompts/runs/MAU-LOD-001/`.
Contact sheets: `review-shots/MAU-LOD_buildings-sheet.png`, `review-shots/MAU-LOD_ships-sheet.png`.

## Locked generation rules

- One coherent, watertight-looking asset per concept; nothing floats or is disconnected.
- Preserve the source silhouette and only two or three named identity features.
- Broad planar masses, thick structural forms, shallow chamfers, minimal rounding.
- Mauna palette as flat zones: tarnished bronze and umber armour, gunmetal structure and plinths, one
  off-white salvaged section, flat near-black glazing, sparse flat crimson accents. **Not** the Terran
  off-white-and-amber scheme.
- No railings, cables, exposed pipes, antennae, rods, ladders, fans, fine vents, tiny panels, small
  patch plates, rivets, open frames or loose props.
- A dish survives only where it is an identity feature, and then only as a thick faceted solid bowl.
- No geometry continues beneath a building foundation.
- Ships stay weapon-neutral: no fixed guns, no visible hardpoints.
- One or two large flat stencils at most; the crescent emblem is the only mark.
- Concepts first; cardinal front/left/right/back reference sets follow only after approval.

## File locations

```text
Buildings/<MAU-BLD-…>/LowDetail/<MAU-BLD-…>_low-detail_concept_v01.png
Ships/<MAU-SHP-…>/LowDetail/<MAU-SHP-…>_low-detail_concept_v01.png
```

## Generated and visually checked

**All 52 pass the locked rules**: solid single masses, closed silhouettes, flat grey field, no thin
parts, no glow, palette consistent across the faction and distinct from the Terran set.

### Buildings (45)

| Group | Assets | Review |
|---|---|---|
| Command | MAU-BLD-CMD-001, 002 | Pass; the Exchange keeps its inverted-hull dome and pod rack |
| Habitation | MAU-BLD-HAB-001–003 | Pass |
| Life support | MAU-BLD-LIF-001–005 | Pass |
| Mining | MAU-BLD-MIN-001–004 | Pass |
| Storage | MAU-BLD-STO-001–003 | Pass |
| Power | MAU-BLD-PWR-001, 003–005 | Pass |
| Power (panels) | MAU-BLD-PWR-002 | **Thin-element risk**: radiating wings read as flat blades; v02 queued with thick slab wings |
| Manufacturing | MAU-BLD-MFG-001–004 | Pass |
| Logistics | MAU-BLD-LOG-001–004 | Pass |
| Defence | MAU-BLD-DEF-001–008 | Pass; barrel shrouds are thick blocks, launcher cells closed |
| Sensors | MAU-BLD-SEN-001 | Watch: dish bowl is close to the thickness floor, acceptable as drawn |
| Sensors | MAU-BLD-SEN-002 | **Thin-element risk**: tower dish reads as a thin sheet; v02 queued with a thick faceted bowl |
| Advanced tech | MAU-BLD-TEC-001–005 | Pass |

### Ships (7)

| Asset | Hull | Review |
|---|---|---|
| MAU-SHP-001 | Scoutship | Pass; engine mass integral to the hull |
| MAU-SHP-002 | Assault Fighter | Pass; wide wedge, engines in the trailing edge |
| MAU-SHP-003 | Hauler | Pass; belly and two clamp bands survive simplification |
| MAU-SHP-004 | Combat Eagle | Pass; salvaged nose block and sponsons kept, weapon-neutral |
| MAU-SHP-005 | Terminator | Pass; spinal shroud reads as a solid ridge |
| MAU-SHP-006 | Command Cruiser | Pass; stacked superstructure kept, thin bow turret correctly dropped |
| MAU-SHP-007 | Fleet Battleship | Pass; two-section hull and collar still legible |

## Known thin-element watch list

Solar and sensor assets are the only Mauna forms whose identity feature is inherently thin. The rule
is: panels are rigid thick slabs with visible edge depth, dishes are thick faceted bowls with heavy
rims. `MAU-BLD-PWR-001` and `MAU-BLD-SEN-001` sit within tolerance as drawn; `MAU-BLD-PWR-002` and
`MAU-BLD-SEN-002` do not and have v02 re-rolls.

## Next stage

Cardinal four-view reference sets are generated from an **approved** low-detail concept, not from the
dressed concept. The anchor `MAU-BLD-CMD-001` goes first, then the P0 assets
(MAU-BLD-MIN-001, MAU-BLD-MIN-003, MAU-BLD-PWR-004, MAU-BLD-MFG-002, MAU-BLD-LOG-001,
MAU-BLD-DEF-002, MAU-SHP-001, MAU-SHP-003, MAU-SHP-007).
