"""Crop one 2x2 orthographic reference sheet into front/back/left/right files.

The repository pipeline always lays views out in this order:
top-left front, top-right back, bottom-left left, bottom-right right.
Cropping is mechanical; this tool does not resize or repaint any tile.

Usage:
    python tools/crop-reference-sheet.py SHEET.png --output-dir DIR --stem ASSET_base --version v01
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sheet", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--stem", required=True, help="Filename stem before _front/_back/etc.")
    parser.add_argument("--version", default="v01")
    parser.add_argument(
        "--roles",
        nargs=4,
        default=("front", "back", "left", "right"),
        metavar=("TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT"),
        help="view names in sheet order; defaults to front back left right",
    )
    parser.add_argument(
        "--center-gutter-px",
        type=int,
        default=0,
        help="Pixels to exclude on each side of generated centre divider lines.",
    )
    parser.add_argument(
        "--vertical-divider",
        nargs=2,
        type=int,
        metavar=("LEFT_END", "RIGHT_START"),
        help="explicit vertical divider bounds for an irregular generated sheet",
    )
    parser.add_argument(
        "--horizontal-divider",
        nargs=2,
        type=int,
        metavar=("TOP_END", "BOTTOM_START"),
        help="explicit horizontal divider bounds for an irregular generated sheet",
    )
    parser.add_argument(
        "--pad-square",
        action="store_true",
        help="centre each crop on a square canvas without resizing it",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    with Image.open(args.sheet) as image:
        width, height = image.size
        if width % 2 or height % 2:
            raise SystemExit(f"sheet dimensions must be even, got {width}x{height}")
        if args.center_gutter_px < 0:
            raise SystemExit("--center-gutter-px cannot be negative")
        if len(set(args.roles)) != 4 or any(not role.replace("-", "").isalnum() for role in args.roles):
            raise SystemExit("--roles must contain four unique filename-safe names")

        args.output_dir.mkdir(parents=True, exist_ok=True)
        if bool(args.vertical_divider) != bool(args.horizontal_divider):
            raise SystemExit("explicit divider bounds must be supplied for both axes")
        if args.vertical_divider:
            left_end, right_start = args.vertical_divider
            top_end, bottom_start = args.horizontal_divider
            if not (0 < left_end <= right_start < width and 0 < top_end <= bottom_start < height):
                raise SystemExit("explicit divider bounds are outside the sheet")
        else:
            half_width, half_height = width // 2, height // 2
            gutter = args.center_gutter_px
            left_end, right_start = half_width - gutter, half_width + gutter
            top_end, bottom_start = half_height - gutter, half_height + gutter
        boxes = (
            (0, 0, left_end, top_end),
            (right_start, 0, width, top_end),
            (0, bottom_start, left_end, height),
            (right_start, bottom_start, width, height),
        )
        pixel_boxes = dict(zip(args.roles, boxes))
        square_size = max(max(box[2] - box[0], box[3] - box[1]) for box in boxes)
        for view, box in pixel_boxes.items():
            output = args.output_dir / f"{args.stem}_{view}_{args.version}.png"
            if output.exists():
                raise SystemExit(f"refusing to overwrite {output}")
            crop = image.crop(box)
            if args.pad_square:
                canvas = Image.new("RGB", (square_size, square_size), crop.getpixel((2, 2)))
                canvas.paste(crop, ((square_size - crop.width) // 2, (square_size - crop.height) // 2))
                crop = canvas
            crop.save(output)
            print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
