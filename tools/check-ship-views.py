"""Validate top/bottom/left/rear orthographic spacecraft reference views.

Unlike upright buildings, spacecraft project each world dimension onto a
different image axis. This checker compares corresponding dimensions:

- length: top height, bottom height, left width
- width: top width, bottom width, rear width
- height: left height, rear height

Usage:
    python tools/check-ship-views.py TOP BOTTOM LEFT REAR
"""
from __future__ import annotations

import sys
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image


WARN_PCT = 3.0
FAIL_PCT = 10.0
BG_TOLERANCE = 40
ROLES = ("top", "bottom", "left", "rear")


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


def silhouette(path: Path) -> dict:
    with Image.open(path) as source:
        image = source.convert("RGB")
    pixels = np.asarray(image).astype(np.int16)
    background = pixels[2, 2]
    raw_mask = np.abs(pixels - background).sum(2) > BG_TOLERANCE
    mask = remove_border_components(raw_mask)
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        raise ValueError(f"{path.name}: no interior silhouette found")
    return {
        "name": path.name,
        "canvas": image.size,
        "width": int(xs.max() - xs.min() + 1),
        "height": int(ys.max() - ys.min() + 1),
        "cx": float((xs.min() + xs.max()) / 2 / image.width),
        "cy": float((ys.min() + ys.max()) / 2 / image.height),
    }


def spread(values: list[float]) -> float:
    low, high = min(values), max(values)
    return 0.0 if high == 0 else (high - low) / high * 100.0


def main() -> int:
    if len(sys.argv) != 5:
        print(__doc__)
        return 2
    views = {role: silhouette(Path(path)) for role, path in zip(ROLES, sys.argv[1:])}
    issues: list[tuple[str, str]] = []

    canvases = {view["canvas"] for view in views.values()}
    if len(canvases) > 1:
        issues.append(("FAIL", f"canvas sizes differ: {sorted(canvases)}"))

    dimensions = {
        "length": [views["top"]["height"], views["bottom"]["height"], views["left"]["width"]],
        "width": [views["top"]["width"], views["bottom"]["width"], views["rear"]["width"]],
        "height": [views["left"]["height"], views["rear"]["height"]],
    }
    for label, values in dimensions.items():
        delta = spread(values)
        if delta >= FAIL_PCT:
            issues.append(("FAIL", f"projected {label} varies by {delta:.1f}%: {values}"))
        elif delta >= WARN_PCT:
            issues.append(("WARN", f"projected {label} varies by {delta:.1f}%: {values}"))

    for axis in ("cx", "cy"):
        values = [view[axis] for view in views.values()]
        drift = (max(values) - min(values)) * 100
        if drift >= 4.0:
            issues.append(("FAIL", f"centring {axis} drifts {drift:.1f}% of canvas"))
        elif drift >= 2.0:
            issues.append(("WARN", f"centring {axis} drifts {drift:.1f}% of canvas"))

    for role in ROLES:
        view = views[role]
        print(
            f"{role:<7} {view['canvas'][0]}x{view['canvas'][1]}  "
            f"silhouette {view['width']:>4}x{view['height']:<4}  "
            f"centre ({view['cx']:.3f}, {view['cy']:.3f})"
        )
    print()
    if not issues:
        print("OK - ship views are mutually consistent.")
    else:
        for level, detail in issues:
            print(f"[{level}] {detail}")
    return 1 if any(level == "FAIL" for level, _ in issues) else 0


if __name__ == "__main__":
    raise SystemExit(main())
