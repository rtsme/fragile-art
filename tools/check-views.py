"""
Check that a set of orthographic reference views agree with each other.

Independently generated views often disagree about the subject's size and position.
The reconstructor has to reconcile them, and where they disagree it hedges — which
shows up as smeared or doubled detail in the mesh. This catches that before you spend
credits on it.

Usage:
    python check-views.py <image> [<image> ...]      # human-readable report
    python check-views.py --json <image> ...         # machine-readable, for Art Forge

Exit code is 1 if any check fails, so it can gate a script.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image

# Silhouette dimensions may differ by this much before we complain. 3% is comfortably
# inside "the same drawing at the same scale"; the BLD-CMD-001 set that motivated this
# check was out by 14.5%.
WARN_PCT = 3.0
FAIL_PCT = 10.0

BG_TOLERANCE = 40          # per-pixel colour distance that counts as "not background"


def silhouette(path: Path) -> dict | None:
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(np.int16)
    bg = a[2, 2]                                  # a flat corner is the background
    mask = np.abs(a - bg).sum(2) > BG_TOLERANCE
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    return {
        "name": path.name,
        "canvas": list(im.size),
        "width": int(xs.max() - xs.min() + 1),
        "height": int(ys.max() - ys.min() + 1),
        "cx": round(float((xs.min() + xs.max()) / 2 / im.width), 4),
        "cy": round(float((ys.min() + ys.max()) / 2 / im.height), 4),
    }


def spread(values: list[float]) -> float:
    """Percentage spread across a set of measurements."""
    lo, hi = min(values), max(values)
    return 0.0 if hi == 0 else (hi - lo) / hi * 100.0


def view_role(name: str) -> str | None:
    """Read front/back/left/right from a conventional reference filename."""
    match = re.search(r"(?:^|_)(front|back|left|right)(?:_|\.)", name.lower())
    return match.group(1) if match else None


def check(paths: list[Path]) -> dict:
    views = [v for v in (silhouette(p) for p in paths) if v]
    issues: list[dict] = []

    if len(views) < 2:
        return {"ok": True, "views": views, "issues": []}

    def add(level, rule, detail):
        issues.append({"level": level, "rule": rule, "detail": detail})

    # 1. Canvas size — differing aspect ratios mean differing implied cameras.
    canvases = {tuple(v["canvas"]) for v in views}
    if len(canvases) > 1:
        add("fail", "canvas size",
            "views use different canvas sizes: "
            + ", ".join(f"{w}x{h}" for w, h in sorted(canvases)))

    # 2. Subject scale — height should agree across every upright view. Width is
    # compared only between opposing elevations: a rectangular object's front
    # width and side depth are physically different and must not be compared.
    hs = spread([v["height"] for v in views])
    scale_checks = [("height (all views)", hs)]
    roles = {view_role(v["name"]): v for v in views}
    for label, pair in (("width (front/back)", ("front", "back")),
                        ("width (left/right)", ("left", "right"))):
        pair_views = [roles.get(role) for role in pair]
        if all(pair_views):
            scale_checks.append((label, spread([v["width"] for v in pair_views])))
    if len(scale_checks) == 1 and len(views) <= 2:
        scale_checks.append(("width", spread([v["width"] for v in views])))

    for label, pct in scale_checks:
        if pct >= FAIL_PCT:
            add("fail", f"subject {label}",
                f"silhouette {label} varies by {pct:.1f}% "
                f"(should be under {WARN_PCT:.0f}%)")
        elif pct >= WARN_PCT:
            add("warn", f"subject {label}",
                f"silhouette {label} varies by {pct:.1f}%")

    # 3. Centring — a drifting subject shifts the implied camera between views.
    for axis in ("cx", "cy"):
        vals = [v[axis] for v in views]
        drift = (max(vals) - min(vals)) * 100
        if drift >= 4.0:
            add("fail", f"centring {axis}",
                f"subject centre drifts {drift:.1f}% of canvas across views")
        elif drift >= 2.0:
            add("warn", f"centring {axis}",
                f"subject centre drifts {drift:.1f}% of canvas across views")

    return {"ok": not any(i["level"] == "fail" for i in issues),
            "views": views, "issues": issues}


def main() -> int:
    args = sys.argv[1:]
    as_json = "--json" in args
    paths = [Path(a) for a in args if a != "--json"]
    if not paths:
        print(__doc__)
        return 2

    result = check(paths)

    if as_json:
        print(json.dumps(result))
        return 0 if result["ok"] else 1

    for v in result["views"]:
        print(f"{v['name'][:44]:44} canvas {v['canvas'][0]}x{v['canvas'][1]:<5} "
              f"silhouette {v['width']:>5} x {v['height']:<5} "
              f"centre ({v['cx']:.3f}, {v['cy']:.3f})")
    print()
    if not result["issues"]:
        print("OK - views are mutually consistent.")
    for i in result["issues"]:
        print(f"[{i['level'].upper():4}] {i['rule']:16} {i['detail']}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
