"""Normalize front/back/left/right spacecraft elevations to one world scale."""
from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path
from statistics import median

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


BG_TOLERANCE = 40
ROLES = ("front", "back", "left", "right")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_sheet", type=Path)
    parser.add_argument("front", type=Path)
    parser.add_argument("back", type=Path)
    parser.add_argument("left", type=Path)
    parser.add_argument("right", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--stem", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--target-cx", type=float, default=0.5)
    parser.add_argument("--target-cy", type=float, default=0.5)
    parser.add_argument("--center-gutter-px", type=int, default=5)
    return parser.parse_args()


def remove_border_components(mask: np.ndarray) -> np.ndarray:
    height, width = mask.shape
    border = np.zeros_like(mask, dtype=bool)
    pending: deque[tuple[int, int]] = deque()
    for x in range(width):
        if mask[0, x]:
            pending.append((0, x))
        if mask[height - 1, x]:
            pending.append((height - 1, x))
    for y in range(1, height - 1):
        if mask[y, 0]:
            pending.append((y, 0))
        if mask[y, width - 1]:
            pending.append((y, width - 1))
    while pending:
        y, x = pending.popleft()
        if border[y, x] or not mask[y, x]:
            continue
        border[y, x] = True
        if y:
            pending.append((y - 1, x))
        if y + 1 < height:
            pending.append((y + 1, x))
        if x:
            pending.append((y, x - 1))
        if x + 1 < width:
            pending.append((y, x + 1))
    return mask & ~border


def bounds(image: Image.Image) -> tuple[int, int, int, int]:
    pixels = np.asarray(image.convert("RGB")).astype(np.int16)
    background = pixels[2, 2]
    raw_mask = np.abs(pixels - background).sum(2) > BG_TOLERANCE
    mask = remove_border_components(raw_mask)
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        raise ValueError("no interior silhouette found")
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def normalize(
    source: Image.Image,
    target_width: int,
    target_height: int,
    target_cx: float,
    target_cy: float,
) -> Image.Image:
    source = source.convert("RGB")
    canvas_width, canvas_height = source.size
    x0, y0, x1, y1 = bounds(source)
    scale_x = target_width / (x1 - x0)
    scale_y = target_height / (y1 - y0)
    padding = 18
    crop_x0, crop_y0 = max(0, x0 - padding), max(0, y0 - padding)
    crop_x1, crop_y1 = min(canvas_width, x1 + padding), min(canvas_height, y1 + padding)
    crop = source.crop((crop_x0, crop_y0, crop_x1, crop_y1))
    resized = crop.resize(
        (max(1, round(crop.width * scale_x)), max(1, round(crop.height * scale_y))),
        Image.Resampling.LANCZOS,
    )
    result = Image.new("RGB", source.size, source.getpixel((2, 2)))
    subject_x0 = target_cx * canvas_width - target_width / 2
    subject_y0 = target_cy * canvas_height - target_height / 2
    paste_x = round(subject_x0 - (x0 - crop_x0) * scale_x)
    paste_y = round(subject_y0 - (y0 - crop_y0) * scale_y)
    feather = 7
    mask = Image.new("L", resized.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle(
        (feather, feather, resized.width - feather - 1, resized.height - feather - 1),
        fill=255,
    )
    mask = mask.filter(ImageFilter.GaussianBlur(3))
    result.paste(resized, (paste_x, paste_y), mask)
    return result


def main() -> int:
    args = parse_args()
    inputs = dict(zip(ROLES, (args.front, args.back, args.left, args.right)))
    images = {role: Image.open(path).convert("RGB") for role, path in inputs.items()}
    try:
        sizes = {image.size for image in images.values()}
        if len(sizes) != 1:
            raise SystemExit(f"input crop sizes differ: {sorted(sizes)}")
        measured = {role: bounds(image) for role, image in images.items()}
        widths = {role: box[2] - box[0] for role, box in measured.items()}
        heights = {role: box[3] - box[1] for role, box in measured.items()}
        hull_height = round(median(heights.values()))
        wingspan = round(median((widths["front"], widths["back"])))
        hull_length = round(median((widths["left"], widths["right"])))
        targets = {
            "front": (wingspan, hull_height),
            "back": (wingspan, hull_height),
            "left": (hull_length, hull_height),
            "right": (hull_length, hull_height),
        }
        corrected = {
            role: normalize(image, *targets[role], args.target_cx, args.target_cy)
            for role, image in images.items()
        }

        args.output_dir.mkdir(parents=True, exist_ok=True)
        for role, image in corrected.items():
            output = args.output_dir / f"{args.stem}_{role}_{args.version}.png"
            if output.exists():
                raise SystemExit(f"refusing to overwrite {output}")
            image.save(output)
            print(output)

        with Image.open(args.source_sheet) as source:
            background = source.convert("RGB").getpixel((2, 2))
        tile_width, tile_height = next(iter(sizes))
        gutter = args.center_gutter_px
        sheet = Image.new(
            "RGB",
            (tile_width * 2 + gutter * 2, tile_height * 2 + gutter * 2),
            background,
        )
        placements = {
            "front": (0, 0),
            "left": (tile_width + gutter * 2, 0),
            "right": (0, tile_height + gutter * 2),
            "back": (tile_width + gutter * 2, tile_height + gutter * 2),
        }
        for role, image in corrected.items():
            sheet.paste(image, placements[role])
        output = args.output_dir / f"{args.stem}_reference-sheet_{args.version}.png"
        if output.exists():
            raise SystemExit(f"refusing to overwrite {output}")
        sheet.save(output)
        print(output)
        print(f"world targets: length={hull_length}px wingspan={wingspan}px height={hull_height}px")
    finally:
        for image in images.values():
            image.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
