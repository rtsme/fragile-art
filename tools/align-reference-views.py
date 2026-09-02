"""Deterministically align orthographic crops without repainting their contents.

Front and back are copied unchanged. Left and right are uniformly scaled and
translated so their measured silhouette height and centre match explicit targets.
The corrected crops are also assembled into a divider-preserving 2x2 sheet.

Usage:
    python tools/align-reference-views.py SOURCE_SHEET.png FRONT.png BACK.png LEFT.png RIGHT.png \
        --output-dir DIR --stem ASSET_base --version v12 --target-height 184
"""
from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path

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
    parser.add_argument("--target-height", type=int, default=184)
    parser.add_argument("--target-cy", type=float, default=0.510)
    parser.add_argument("--target-cx", type=float, default=0.500)
    parser.add_argument("--left-cx", type=float, default=0.495)
    parser.add_argument("--right-cx", type=float, default=0.485)
    parser.add_argument(
        "--align-all",
        action="store_true",
        help="uniformly scale and centre every view using a feathered crop",
    )
    parser.add_argument("--center-gutter-px", type=int, default=3)
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


def silhouette(image: Image.Image) -> tuple[int, int, float, float]:
    rgb = image.convert("RGB")
    pixels = np.asarray(rgb).astype(np.int16)
    background = pixels[2, 2]
    raw_mask = np.abs(pixels - background).sum(2) > BG_TOLERANCE
    mask = remove_border_components(raw_mask)
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        raise ValueError("no interior silhouette found")
    width = int(xs.max() - xs.min() + 1)
    height = int(ys.max() - ys.min() + 1)
    cx = float((xs.min() + xs.max()) / 2)
    cy = float((ys.min() + ys.max()) / 2)
    return width, height, cx, cy


def silhouette_bounds(image: Image.Image) -> tuple[int, int, int, int]:
    rgb = image.convert("RGB")
    pixels = np.asarray(rgb).astype(np.int16)
    background = pixels[2, 2]
    raw_mask = np.abs(pixels - background).sum(2) > BG_TOLERANCE
    mask = remove_border_components(raw_mask)
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        raise ValueError("no interior silhouette found")
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def align_cropped(
    source: Image.Image,
    target_height: int,
    target_cx_ratio: float,
    target_cy_ratio: float,
) -> Image.Image:
    """Normalize framing while preserving the generated subject pixels.

    Cropping avoids affine-transforming a studio gradient across the full canvas,
    which can make the background look like part of the silhouette. A feathered
    margin hides the crop boundary without touching the subject.
    """
    source = source.convert("RGB")
    canvas_width, canvas_height = source.size
    x0, y0, x1, y1 = silhouette_bounds(source)
    subject_height = y1 - y0
    scale = target_height / subject_height
    padding = 20
    crop_x0 = max(0, x0 - padding)
    crop_y0 = max(0, y0 - padding)
    crop_x1 = min(canvas_width, x1 + padding)
    crop_y1 = min(canvas_height, y1 + padding)
    crop = source.crop((crop_x0, crop_y0, crop_x1, crop_y1))
    resized = crop.resize(
        (max(1, round(crop.width * scale)), max(1, round(crop.height * scale))),
        Image.Resampling.LANCZOS,
    )

    background = source.getpixel((2, 2))
    result = Image.new("RGB", source.size, background)
    desired_subject_x0 = target_cx_ratio * canvas_width - (x1 - x0) * scale / 2
    desired_subject_y0 = target_cy_ratio * canvas_height - target_height / 2
    paste_x = round(desired_subject_x0 - (x0 - crop_x0) * scale)
    paste_y = round(desired_subject_y0 - (y0 - crop_y0) * scale)

    feather = max(2, round(8 * scale))
    mask = Image.new("L", resized.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle(
        (feather, feather, resized.width - feather - 1, resized.height - feather - 1),
        fill=255,
    )
    mask = mask.filter(ImageFilter.GaussianBlur(max(1, feather / 2)))
    result.paste(resized, (paste_x, paste_y), mask)
    return result


def align(
    source: Image.Image,
    target_height: int,
    target_cx_ratio: float,
    target_cy_ratio: float,
) -> Image.Image:
    source = source.convert("RGB")
    canvas_width, canvas_height = source.size
    _, source_height, source_cx, source_cy = silhouette(source)
    scale = target_height / source_height
    desired_cx = target_cx_ratio * canvas_width
    desired_cy = target_cy_ratio * canvas_height
    result = source

    for _ in range(4):
        inverse = (
            1.0 / scale,
            0.0,
            source_cx - desired_cx / scale,
            0.0,
            1.0 / scale,
            source_cy - desired_cy / scale,
        )
        result = source.transform(
            source.size,
            Image.Transform.AFFINE,
            inverse,
            resample=Image.Resampling.BICUBIC,
            fillcolor=source.getpixel((2, 2)),
        )
        _, measured_height, measured_cx, measured_cy = silhouette(result)
        if measured_height:
            scale *= target_height / measured_height
        desired_cx += target_cx_ratio * canvas_width - measured_cx
        desired_cy += target_cy_ratio * canvas_height - measured_cy

    return result


def main() -> int:
    args = parse_args()
    if (
        not 0 < args.target_cy < 1
        or not 0 < args.target_cx < 1
        or not 0 < args.left_cx < 1
        or not 0 < args.right_cx < 1
    ):
        raise SystemExit("target centre ratios must be between 0 and 1")
    if args.target_height <= 0 or args.center_gutter_px < 0:
        raise SystemExit("target height must be positive and gutter cannot be negative")

    inputs = dict(zip(ROLES, (args.front, args.back, args.left, args.right)))
    images = {role: Image.open(path).convert("RGB") for role, path in inputs.items()}
    try:
        sizes = {image.size for image in images.values()}
        if len(sizes) != 1:
            raise SystemExit(f"input crop sizes differ: {sorted(sizes)}")
        tile_width, tile_height = next(iter(sizes))
        if args.align_all:
            corrected = {
                role: align_cropped(image, args.target_height, args.target_cx, args.target_cy)
                for role, image in images.items()
            }
        else:
            corrected = {
                "front": images["front"].copy(),
                "back": images["back"].copy(),
                "left": align(images["left"], args.target_height, args.left_cx, args.target_cy),
                "right": align(images["right"], args.target_height, args.right_cx, args.target_cy),
            }

        args.output_dir.mkdir(parents=True, exist_ok=True)
        outputs = {}
        for role, image in corrected.items():
            output = args.output_dir / f"{args.stem}_{role}_{args.version}.png"
            if output.exists():
                raise SystemExit(f"refusing to overwrite {output}")
            image.save(output)
            outputs[role] = output
            width, height, cx, cy = silhouette(image)
            print(f"{output} silhouette={width}x{height} centre=({cx / tile_width:.4f},{cy / tile_height:.4f})")

        with Image.open(args.source_sheet) as sheet_source:
            sheet = sheet_source.convert("RGB").copy()
        half_width, half_height = sheet.width // 2, sheet.height // 2
        gutter = args.center_gutter_px
        expected_size = (half_width - gutter, half_height - gutter)
        if expected_size != (tile_width, tile_height):
            raise SystemExit(
                f"sheet/crop geometry mismatch: sheet expects {expected_size}, crops are {(tile_width, tile_height)}"
            )
        sheet.paste(corrected["front"], (0, 0))
        sheet.paste(corrected["back"], (half_width + gutter, 0))
        sheet.paste(corrected["left"], (0, half_height + gutter))
        sheet.paste(corrected["right"], (half_width + gutter, half_height + gutter))
        sheet_output = args.output_dir / f"{args.stem}_reference-sheet_{args.version}.png"
        if sheet_output.exists():
            raise SystemExit(f"refusing to overwrite {sheet_output}")
        sheet.save(sheet_output)
        print(sheet_output)
    finally:
        for image in images.values():
            image.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
