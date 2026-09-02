"""Normalize all four orthographic crops to one silhouette height and centre.

The operation is deterministic and preserves each crop's pixels apart from uniform
scaling and translation. It also rebuilds a divider-preserving 2x2 reference sheet.
"""
from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter


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
    parser.add_argument("--target-height", type=int, required=True)
    parser.add_argument("--target-cx", type=float, default=0.5)
    parser.add_argument("--target-cy", type=float, default=0.5)
    parser.add_argument("--center-gutter-px", type=int, default=2)
    parser.add_argument("--translate-only", action="store_true")
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
    pixels = np.asarray(image.convert("RGB")).astype(np.int16)
    background = pixels[2, 2]
    mask = remove_border_components(np.abs(pixels - background).sum(2) > BG_TOLERANCE)
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        raise ValueError("no interior silhouette found")
    return (
        int(xs.max() - xs.min() + 1),
        int(ys.max() - ys.min() + 1),
        float((xs.min() + xs.max()) / 2),
        float((ys.min() + ys.max()) / 2),
    )


def foreground_mask(image: Image.Image) -> np.ndarray:
    pixels = np.asarray(image.convert("RGB")).astype(np.int16)
    background = pixels[2, 2]
    return remove_border_components(np.abs(pixels - background).sum(2) > BG_TOLERANCE)


def fitted_background(image: Image.Image, mask: np.ndarray) -> Image.Image:
    """Fit the smooth studio backdrop so translated assets do not leave seams."""
    pixels = np.asarray(image.convert("RGB"), dtype=np.float64)
    height, width, _ = pixels.shape
    yy, xx = np.mgrid[0:height, 0:width]
    x = xx / max(1, width - 1)
    y = yy / max(1, height - 1)
    basis = np.stack((np.ones_like(x), x, y, x * x, y * y, x * y), axis=-1)
    sample = (~mask) & ((xx % 8 == 0) & (yy % 8 == 0))
    design = basis[sample]
    fitted = np.empty_like(pixels)
    for channel in range(3):
        coefficients, *_ = np.linalg.lstsq(design, pixels[:, :, channel][sample], rcond=None)
        fitted[:, :, channel] = np.tensordot(basis, coefficients, axes=([2], [0]))
    return Image.fromarray(np.clip(fitted, 0, 255).astype(np.uint8), "RGB")


def normalize(
    source: Image.Image,
    target_height: int,
    target_cx: float,
    target_cy: float,
    translate_only: bool,
) -> Image.Image:
    source = source.convert("RGB")
    canvas_width, canvas_height = source.size
    _, source_height, source_cx, source_cy = silhouette(source)
    mask = foreground_mask(source)
    alpha = Image.fromarray((mask.astype(np.uint8) * 255), "L").filter(ImageFilter.MaxFilter(7))
    alpha = alpha.filter(ImageFilter.GaussianBlur(0.8))
    foreground = source.convert("RGBA")
    foreground.putalpha(alpha)
    background = fitted_background(source, mask).convert("RGBA")
    scale = 1.0 if translate_only else target_height / source_height
    desired_cx = target_cx * canvas_width
    desired_cy = target_cy * canvas_height
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
        transformed = foreground.transform(
            source.size,
            Image.Transform.AFFINE,
            inverse,
            resample=Image.Resampling.BICUBIC,
            fillcolor=(0, 0, 0, 0),
        )
        result = Image.alpha_composite(background, transformed).convert("RGB")
        _, measured_height, measured_cx, measured_cy = silhouette(result)
        if not translate_only:
            scale *= target_height / measured_height
        desired_cx += target_cx * canvas_width - measured_cx
        desired_cy += target_cy * canvas_height - measured_cy
    return result


def main() -> int:
    args = parse_args()
    if args.target_height <= 0 or args.center_gutter_px < 0:
        raise SystemExit("target height must be positive and gutter cannot be negative")
    if not 0 < args.target_cx < 1 or not 0 < args.target_cy < 1:
        raise SystemExit("target centre ratios must be between zero and one")

    paths = dict(zip(ROLES, (args.front, args.back, args.left, args.right)))
    images = {role: Image.open(path).convert("RGB") for role, path in paths.items()}
    try:
        sizes = {image.size for image in images.values()}
        if len(sizes) != 1:
            raise SystemExit(f"input crop sizes differ: {sorted(sizes)}")
        tile_width, tile_height = next(iter(sizes))
        corrected = {
            role: normalize(image, args.target_height, args.target_cx, args.target_cy, args.translate_only)
            for role, image in images.items()
        }
        args.output_dir.mkdir(parents=True, exist_ok=True)
        for role, image in corrected.items():
            output = args.output_dir / f"{args.stem}_{role}_{args.version}.png"
            if output.exists():
                raise SystemExit(f"refusing to overwrite {output}")
            image.save(output)
            width, height, cx, cy = silhouette(image)
            print(f"{output} silhouette={width}x{height} centre=({cx/tile_width:.4f},{cy/tile_height:.4f})")

        with Image.open(args.source_sheet) as source_sheet:
            sheet = source_sheet.convert("RGB").copy()
        half_width, half_height = sheet.width // 2, sheet.height // 2
        gutter = args.center_gutter_px
        expected_size = (half_width - gutter, half_height - gutter)
        if expected_size != (tile_width, tile_height):
            raise SystemExit(f"sheet/crop geometry mismatch: expected {expected_size}, got {(tile_width, tile_height)}")
        positions = {
            "front": (0, 0),
            "back": (half_width + gutter, 0),
            "left": (0, half_height + gutter),
            "right": (half_width + gutter, half_height + gutter),
        }
        for role, image in corrected.items():
            sheet.paste(image, positions[role])
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
