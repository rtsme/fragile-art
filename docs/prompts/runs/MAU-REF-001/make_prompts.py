"""Write orthographic reference-sheet prompts for the approved Mauna low-detail buildings.

One 2x2 sheet per building (front, back, left, right), generated from that building's approved
low-detail concept. The anchor MAU-BLD-CMD-001 is already done and is skipped unless --all is given.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
MAUNA = ROOT / "Concepts/Mauna"
ANCHOR = "MAU-BLD-CMD-001"

BODY = """One image divided into a clean 2x2 grid of four orthographic views of the SAME building — the low-detail Mauna {name} from reference 1. Tile order, reading left to right, top row then bottom row: FRONT, BACK, LEFT, RIGHT.

These are hard requirements:
- True orthographic projection in every tile. No perspective, no foreshortening, no three-quarter angle, no tilt. Each view is a straight-on elevation at eye level with the building's centre.
- CRITICAL: the building's silhouette height must be IDENTICAL in all four tiles. Draw the base on the same horizontal line and the highest point at the same height in every tile. The side views are not nearer the camera and are not drawn larger. Width matches between FRONT and BACK, and between LEFT and RIGHT.
- The building sits at the exact centre of its tile in all four tiles, with the same margin all round, and no part touches or is cropped by a tile edge.
- Every tile shows the same object and the same asymmetry: a feature on one flank appears on the opposite side in BACK, and in profile in the side views. Nothing is added, removed, moved or re-invented between tiles.
- Keep the exact low-detail geometry, flat material zones, colour placement and wear from reference 1. Do not switch to clay, grey or untextured, and do not paint on detail that is not modelled.
- Plain flat light-grey background, the same tone in every tile. Flat even lighting, no ground shadow, no rim light, no ambient occlusion, no glow, no reflections.
- No text, no labels, no view names, no arrows, no dimensions, no watermark.

The subject stays exactly the approved low-detail asset in reference 1: tarnished bronze and umber armour, gunmetal structure and plinth, one off-white salvaged section where it has one, flat near-black glazing, sparse flat crimson accents and the crescent emblem. Matte to satin only."""


def main() -> None:
    include_anchor = "--all" in sys.argv
    jobs = []
    for d in sorted((MAUNA / "Buildings").iterdir()):
        mau = d.name
        if mau == ANCHOR and not include_anchor:
            continue
        low = sorted((d / "LowDetail").glob(f"{mau}_low-detail_concept_v*.png"))
        if not low:
            print(f"skip {mau}: no low-detail concept")
            continue
        src = low[-1]  # latest version, so v02 fixes win
        name = mau.replace("MAU-BLD-", "")
        target = ROOT / f"References/Mauna/Buildings/{mau}/LowDetail/{mau}_low-detail_reference-sheet_v01.png"
        text = (
            "Use your image generation tool to create exactly ONE image: a single 2x2 orthographic "
            "reference sheet. One reference image is attached:\n"
            f"1. {src.name}: the approved low-detail Mauna asset. This exact object, unchanged, is the "
            "subject of all four views.\n"
            "Do not edit any repository file. When the image exists, copy the generated PNG to this exact "
            "path (create folders as needed), then reply with only the saved path:\n"
            f"{target}\n\nPROMPT:\n{BODY.format(name=name)}\n"
        )
        p = OUT / f"{mau}_low-detail-sheet_v01.txt"
        p.write_text(text, encoding="utf-8", newline="\n")
        jobs.append(f"{mau}\t{p.name}\t{src.relative_to(ROOT).as_posix()}")
    (OUT / "jobs.tsv").write_text("\n".join(jobs) + "\n", encoding="utf-8", newline="\n")
    print(f"{len(jobs)} reference-sheet prompts written")


if __name__ == "__main__":
    main()
