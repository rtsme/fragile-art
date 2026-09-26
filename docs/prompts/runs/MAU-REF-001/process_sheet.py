"""Crop, normalise and validate one generated 2x2 reference sheet.

Usage: python docs/prompts/runs/MAU-REF-001/process_sheet.py MAU-BLD-XXX-000

Steps, all deterministic:
  1. crop the sheet into four tiles, excluding the generator's divider pixels
  2. measure the FRONT tile's silhouette height — the truthful straight-on elevation
  3. normalise all four tiles to that height and a common centre
  4. run tools/check-views.py and report OK / WARN / FAIL

Exit code 0 means the set passed the checker and is ready for the Meshy stage.
"""
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[4]
BG_TOLERANCE = 40


def silhouette_height(path: Path) -> int:
    px = np.asarray(Image.open(path).convert("RGB")).astype(np.int16)
    bg = px[2, 2]
    mask = np.abs(px - bg).sum(2) > BG_TOLERANCE
    # drop anything touching the border so a divider line cannot be measured as subject
    h, w = mask.shape
    from collections import deque

    seen = np.zeros_like(mask)
    q = deque([(y, x) for x in range(w) for y in (0, h - 1) if mask[y, x]])
    q += deque([(y, x) for y in range(h) for x in (0, w - 1) if mask[y, x]])
    while q:
        y, x = q.popleft()
        if seen[y, x] or not mask[y, x]:
            continue
        seen[y, x] = True
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w:
                q.append((ny, nx))
    ys, _ = np.nonzero(mask & ~seen)
    if not len(ys):
        raise SystemExit(f"no silhouette found in {path}")
    return int(ys.max() - ys.min() + 1)


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)


def main() -> None:
    asset = sys.argv[1]
    d = ROOT / f"References/Mauna/Buildings/{asset}/LowDetail"
    stem = f"{asset}_low-detail"
    sheet = d / f"{stem}_reference-sheet_v01.png"
    if not sheet.exists():
        raise SystemExit(f"{asset}: no generated sheet")

    run(["python", "tools/crop-reference-sheet.py", str(sheet), "--output-dir", str(d),
         "--stem", stem, "--version", "v03", "--center-gutter-px", "3"])
    target = silhouette_height(d / f"{stem}_front_v03.png")

    run(["python", "tools/normalize-reference-views.py", str(sheet),
         *[str(d / f"{stem}_{v}_v03.png") for v in ("front", "back", "left", "right")],
         "--output-dir", str(d), "--stem", stem, "--version", "v04",
         "--target-height", str(target), "--center-gutter-px", "3"])

    check = run(["python", "tools/check-views.py",
                 *[str(d / f"{stem}_{v}_v04.png") for v in ("front", "back", "left", "right")]])
    out = check.stdout.strip().splitlines()
    verdict = [line for line in out if line.startswith(("OK", "[WARN]", "[FAIL]"))] or ["no verdict"]
    status = "PASS" if any(line.startswith("OK") for line in verdict) else "FAIL"
    print(f"{asset}: {status} (target height {target}) :: " + " | ".join(verdict))
    sys.exit(0 if status == "PASS" else 1)


if __name__ == "__main__":
    main()
