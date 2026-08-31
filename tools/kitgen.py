"""
Procedural kit part generator.

Railings, ladders, catwalks and pipe runs are exactly the shapes image-to-3D cannot
produce — thin, open, repetitive — and exactly the shapes that are trivial to author
parametrically. This emits them directly as clean low-poly .glb, with no generation
cost, no reconstruction noise, and identical geometry every time.

Conventions, taken from FragileFrontiers.GodotShell.StructureModels:

  * **Wide-first.** Parts are authored running along +X. The assembly table has no
    rotation — only offsets — so a part that must run along Z is a separate part.
  * **Origin at the middle of the plan, at the base.** A part sits on the ground
    rather than floating at the middle of its own box.
  * **Units are kit units, nominally 1.0 = 1 metre.** Absolute scale does not matter
    to the engine (StructureModel.Fit normalises the whole assembly to the footprint),
    but parts must be consistent *with each other*.
  * **Flat-shaded, low-poly, box-built.** Matches the existing silhouette language.

Usage:
    python kitgen.py <out_dir> [part ...]      # default: every part
    python kitgen.py --list
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import trimesh

# Shared proportions, so every part in the kit agrees with every other.
POST = 0.06          # square section of a railing post
RAIL = 0.05          # square section of a horizontal rail
RAIL_H = 0.55        # handrail height - human-scale, deliberately below the 1.4 m
BAY = 0.50           # spacing between posts


def box(sx: float, sy: float, sz: float, at=(0.0, 0.0, 0.0)) -> trimesh.Trimesh:
    m = trimesh.creation.box(extents=(sx, sy, sz))
    m.apply_translation(at)
    return m


def combine(parts: list[trimesh.Trimesh], name: str) -> trimesh.Trimesh:
    m = trimesh.util.concatenate(parts)
    m.merge_vertices()
    # Sit the part on y=0 and centre its plan, per the origin convention.
    lo, hi = m.bounds
    m.apply_translation([-(lo[0] + hi[0]) / 2, -lo[1], -(lo[2] + hi[2]) / 2])
    m.metadata["name"] = name
    return m


# --------------------------------------------------------------------------- #
# Parts
# --------------------------------------------------------------------------- #


def rail_straight(bays: int = 4) -> trimesh.Trimesh:
    """A straight handrail run along +X: posts on a regular bay, two rails."""
    length = bays * BAY
    parts = []
    for i in range(bays + 1):
        x = -length / 2 + i * BAY
        parts.append(box(POST, RAIL_H, POST, (x, RAIL_H / 2, 0)))
    for h in (RAIL_H - RAIL / 2, RAIL_H * 0.55):
        parts.append(box(length + POST, RAIL, RAIL, (0, h, 0)))
    return combine(parts, "rail_straight")


def rail_corner() -> trimesh.Trimesh:
    """An L corner: one bay along +X meeting one bay along +Z, sharing the post."""
    parts = []
    for at in ((0, RAIL_H / 2, 0), (BAY, RAIL_H / 2, 0), (0, RAIL_H / 2, BAY)):
        parts.append(box(POST, RAIL_H, POST, at))
    for h in (RAIL_H - RAIL / 2, RAIL_H * 0.55):
        parts.append(box(BAY + POST, RAIL, RAIL, (BAY / 2, h, 0)))
        parts.append(box(RAIL, RAIL, BAY + POST, (0, h, BAY / 2)))
    return combine(parts, "rail_corner")


def parapet_straight(bays: int = 4) -> trimesh.Trimesh:
    """
    A solid low wall - the rules-compliant stand-in for a railing when the form has
    to survive image-to-3D rather than come from this kit.
    """
    length = bays * BAY
    return combine([
        box(length, RAIL_H * 0.8, 0.12, (0, RAIL_H * 0.4, 0)),
        box(length, 0.07, 0.18, (0, RAIL_H * 0.8, 0)),      # capping rail
    ], "parapet_straight")


def ladder(rungs: int = 6) -> trimesh.Trimesh:
    """A vertical ladder in the XY plane, rails along +Y, rungs along +X."""
    width, spacing = 0.34, 0.26
    height = rungs * spacing
    parts = [
        box(0.05, height, 0.05, (-width / 2, height / 2, 0)),
        box(0.05, height, 0.05, (width / 2, height / 2, 0)),
    ]
    for i in range(rungs):
        parts.append(box(width, 0.04, 0.04, (0, spacing * (i + 0.5), 0)))
    return combine(parts, "ladder")


def pipe_run(segments: int = 3) -> trimesh.Trimesh:
    """A straight pipe along +X on low saddles, with flanges at each joint."""
    seg, r = 0.9, 0.11
    length = segments * seg
    parts = [box(length, r * 2, r * 2, (0, r + 0.12, 0))]
    for i in range(segments + 1):
        x = -length / 2 + i * seg
        parts.append(box(0.06, r * 2.5, r * 2.5, (x, r + 0.12, 0)))       # flange
        if i < segments:
            parts.append(box(0.12, 0.12, 0.16, (x + seg / 2, 0.06, 0)))   # saddle
    return combine(parts, "pipe_run")


def catwalk(bays: int = 4) -> trimesh.Trimesh:
    """A walkway deck along +X with a railing on both sides."""
    length, width = bays * BAY, 0.7
    parts = [box(length, 0.06, width, (0, 0.03, 0))]
    for z in (-width / 2 + POST, width / 2 - POST):
        for i in range(bays + 1):
            x = -length / 2 + i * BAY
            parts.append(box(POST, RAIL_H, POST, (x, 0.06 + RAIL_H / 2, z)))
        for h in (RAIL_H - RAIL / 2, RAIL_H * 0.55):
            parts.append(box(length + POST, RAIL, RAIL, (0, 0.06 + h, z)))
    return combine(parts, "catwalk")


PARTS = {
    "KIT-RAIL-001_rail_straight": rail_straight,
    "KIT-RAIL-002_rail_corner": rail_corner,
    "KIT-RAIL-003_parapet_straight": parapet_straight,
    "KIT-ACC-001_ladder": ladder,
    "KIT-PIPE-001_pipe_run": pipe_run,
    "KIT-WALK-001_catwalk": catwalk,
}


def main() -> int:
    args = sys.argv[1:]
    if "--list" in args or not args:
        print("parts:")
        for k in PARTS:
            print("  ", k)
        return 0 if "--list" in args else 2

    out = Path(args[0])
    wanted = args[1:] or list(PARTS)
    out.mkdir(parents=True, exist_ok=True)

    for key in wanted:
        if key not in PARTS:
            print(f"unknown part: {key}")
            return 1
        mesh = PARTS[key]()
        dst = out / f"{key}.glb"
        mesh.export(dst)
        sx, sy, sz = mesh.extents
        print(f"{key:34} {len(mesh.faces):>5} tris  "
              f"size {sx:.3f} x {sy:.3f} x {sz:.3f}  "
              f"{dst.stat().st_size / 1024:.1f} KB")
        print(f"{'':34} Part(\"{key.split('_', 1)[1]}\", "
              f"{sx:.3f}, {sy:.3f}, {sz:.3f}),")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
