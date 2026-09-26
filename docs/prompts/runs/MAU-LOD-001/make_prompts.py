"""Generate Mauna low-detail (Meshy-conversion) concept prompts from the approved concepts.

One prompt per asset: 45 buildings + 7 ships. Each references that asset's own approved concept and
asks for a simplified, watertight, generation-safe version of the same silhouette — the Mauna
equivalent of Concepts/Terran/low-detail-conversion-manifest-v01.md.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
MAUNA = ROOT / "Concepts/Mauna"

# Two or three identity features to keep per asset, keyed by asset id.
IDENTITY = {
    "BLD-CMD-001": "the inverted freighter-hull dome on its stepped plinth, the welded off-white salvaged block, and the clamped pod rack",
    "BLD-CMD-002": "the long low flat-roofed armoured block and the off-white gatehouse block",
    "BLD-HAB-001": "the two staggered tiers of capsule dwellings and the long linking corridor block",
    "BLD-HAB-002": "the single grounded cargo hull and its clamped off-white end module",
    "BLD-HAB-003": "the wide low dome, its clamp band and the off-white entry block",
    "BLD-LIF-001": "the long off-white salvaged hull section lying horizontally and the medical roundel",
    "BLD-LIF-002": "the three upturned intake stacks on the long pressure-vessel body",
    "BLD-LIF-003": "the horizontal control capsule and the tall stacked heat-exchanger slabs",
    "BLD-LIF-004": "the cluster of four unequal capsule tanks and the central pump-house block",
    "BLD-LIF-005": "the long split hull with its rows of dark glazing bays and the tank spine",
    "BLD-MIN-001": "the tapered drill housing driven into the rock and the enclosed conveyor to the bunker",
    "BLD-MIN-002": "the two unequal drill housings and the enclosed conveyor to the processing capsule",
    "BLD-MIN-003": "the massive tiered vertical bore drum and its wide stepped foundation",
    "BLD-MIN-004": "the closed ram housing with its two shock cylinders and the off-white control block",
    "BLD-STO-001": "the three unequal capsule silos on a shared sloped hopper base",
    "BLD-STO-002": "the tall tapered vault tower banded by clamp collars",
    "BLD-STO-003": "the upright transfer ring with its flat dark disc and the two tapered pylons",
    "BLD-PWR-001": "the two tilted rigid panel slabs on a turntable block",
    "BLD-PWR-002": "the central hub and the radiating unequal panel wings",
    "BLD-PWR-003": "the row of capsule cells in clamp collars on a stepped plinth",
    "BLD-PWR-004": "the half-sunk reactor sphere, its clamp bands and the off-white turbine hall",
    "BLD-PWR-005": "the contained sphere held by three heavy clamp arms",
    "BLD-MFG-001": "the long factory hall with its huge flush loading hatches and the roof gantry housing",
    "BLD-MFG-002": "the grounded hangar with its segmented doors and the sloped launch ramp",
    "BLD-MFG-003": "the two enormous parallel hull spines forming a U-shaped cradle with corner towers",
    "BLD-MFG-004": "the tapered crane tower with folded boom housing and the solid material stacks",
    "BLD-LOG-001": "the broad octagonal pad with its raised lip, deck emblem and corner blast blocks",
    "BLD-LOG-002": "the three unequal capsule fuel tanks and the pump house with its folded boom",
    "BLD-LOG-003": "the bronze hull arch closed by its flush segmented door and the off-white office block",
    "BLD-LOG-004": "the low warehouse hall with its row of flush loading hatches and stacked pods",
    "BLD-DEF-001": "the bronze cupola on its turntable with one thick barrel shroud",
    "BLD-DEF-002": "the large cupola, short wide emitter shroud and the two capacitor capsules",
    "BLD-DEF-003": "the taller cupola with two unequal emitter shrouds and the block sensor head",
    "BLD-DEF-004": "the closed multi-cell launcher box on its gimbal and the small radar block",
    "BLD-DEF-005": "the central projector column capped by a flat dark disc inside its stacked rings",
    "BLD-DEF-006": "the low silo with its massive round split hatch and the blast trench",
    "BLD-DEF-007": "the squat launch drum with its segmented dome roof and the guidance mast block",
    "BLD-DEF-008": "the very low sloped bunker with its firing-port slits",
    "BLD-SEN-001": "the tapered mast block carrying one thick-bowl dish and the off-white cabin",
    "BLD-SEN-002": "the tall tapered banded tower with its dish near the top",
    "BLD-TEC-001": "the three thick concentric rings clamped around a solid dark sphere",
    "BLD-TEC-002": "the enormous thrust bell sunk into its stepped anchor foundation",
    "BLD-TEC-003": "the generator drum with its four field-coil rings and the capacitor bank",
    "BLD-TEC-004": "the low hub with its row of flush droid-bay hatches and the control mast block",
    "BLD-TEC-005": "the raised transfer pad with its flat dark disc and three tapered pylons",
    "SHP-001": "the bronze teardrop hull swelling into an offset stern engine and the clamped starboard pod",
    "SHP-002": "the wide flat wedge hull with engines in the trailing edge and the clamped port pod",
    "SHP-003": "the oversized cargo belly, its two clamp collars and the small off-white cockpit block",
    "SHP-004": "the off-white salvaged nose block and the two downswept sponsons",
    "SHP-005": "the heavy slab hull with its spinal weapon shroud and off-centre bridge block",
    "SHP-006": "the broad hull with its stacked off-white superstructure and the clamped flank pods",
    "SHP-007": "the two joined hull sections at their massive clamp collar and the spinal cargo pod",
}

RULES = (
    "LOW-DETAIL CONVERSION RULES — these override any detail in the reference:\n"
    "- One coherent, watertight, single-piece asset. Nothing floats, nothing is disconnected, and no "
    "geometry continues beneath the foundation.\n"
    "- Preserve the source silhouette and only the identity features named above. Delete everything else.\n"
    "- Broad planar masses, thick structural forms, shallow chamfers, minimal rounding. Far simpler than "
    "the reference: roughly a tenth of its detail.\n"
    "- Remove all railings, cables, ropes, exposed pipes, antennae, rods, ladders, fans, fine vents, tiny "
    "panels, small patch plates, rivets, open frames and loose props.\n"
    "- A dish is kept only when it is named as an identity feature, and then only as a thick faceted solid "
    "bowl on a chunky block.\n"
    "- Keep one or two large flat stencils at most; no small markings.\n"
    "- Materials as flat zones, not textures: tarnished bronze and umber armour, gunmetal structure and "
    "plinths, one off-white salvaged section, flat near-black glazing, sparse flat crimson accents. Keep "
    "the Mauna palette; do not use Terran off-white-and-amber.\n"
    "- Glass is flat, opaque and dark, with no interior.\n"
    "- Matte to satin only; no chrome, gloss, transparency or glow."
)

PRESENT = (
    "Isolated elevated three-quarter view, complete asset centred on a plain flat light-grey background, "
    "edge to edge. No ground shadow, no environment, no text, no labels, no watermark, no people. Flat even "
    "studio lighting, no rim light, no baked ambient occlusion, no emissive surfaces."
)


def main() -> None:
    jobs = []
    for asset, identity in IDENTITY.items():
        if asset.startswith("SHP-"):
            mau, folder = f"MAU-SHP-{asset[4:]}", "Ships"
        else:
            mau, folder = f"MAU-{asset}", "Buildings"
        src = sorted((MAUNA / folder / mau).glob(f"{mau}_concept_v*.png"))[-1]
        out = f"{folder}/{mau}/LowDetail/{mau}_low-detail_concept_v01.png"
        text = (
            "Use your image generation tool to create exactly ONE image. One reference image is attached:\n"
            f"1. {src.name}: the approved Mauna concept for this asset. Keep its silhouette, proportions and "
            "palette; simplify everything else.\n"
            "Do not edit any repository file. When the image exists, copy the generated PNG to this exact "
            "path (create folders as needed), then reply with only the saved path:\n"
            f"{MAUNA / out}\n\nPROMPT:\n"
            f"A low-detail, generation-ready version of the Mauna asset in reference 1, for conversion to a "
            f"game mesh. Keep only: {identity}.\n\n{RULES}\n\n{PRESENT}\n"
        )
        p = OUT / f"{mau}_low-detail_v01.txt"
        p.write_text(text, encoding="utf-8", newline="\n")
        jobs.append(f"{mau}\t{p.name}\t{out}\t{src.relative_to(MAUNA).as_posix()}")
    (OUT / "jobs.tsv").write_text("\n".join(jobs) + "\n", encoding="utf-8", newline="\n")
    print(f"{len(jobs)} low-detail prompts written")


if __name__ == "__main__":
    main()
