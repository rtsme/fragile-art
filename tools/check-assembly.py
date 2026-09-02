#!/usr/bin/env python3
"""Validate an Art Forge assembly's sources, envelopes and receiver schedule."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def rotate_xyz(point: tuple[float, float, float], degrees: list[float]) -> tuple[float, float, float]:
    """Apply the same intrinsic XYZ Euler order used by Three.js."""
    x, y, z = point
    rx, ry, rz = (math.radians(float(value)) for value in degrees)
    cx, sx, cy, sy, cz, sz = math.cos(rx), math.sin(rx), math.cos(ry), math.sin(ry), math.cos(rz), math.sin(rz)
    return (
        cy * cz * x - cy * sz * y + sy * z,
        (cx * sz + sx * sy * cz) * x + (cx * cz - sx * sy * sz) * y - sx * cy * z,
        (sx * sz - cx * sy * cz) * x + (sx * cz + cx * sy * sz) * y + cx * cy * z,
    )


def bounds(size: list[float], position: list[float], rotation: list[float]) -> tuple[list[float], list[float]]:
    sx, sy, sz = (float(value) for value in size)
    corners = []
    for x in (-sx / 2, sx / 2):
        for y in (0.0, sy):
            for z in (-sz / 2, sz / 2):
                rotated = rotate_xyz((x, y, z), rotation)
                corners.append([rotated[i] + float(position[i]) for i in range(3)])
    return ([min(point[i] for point in corners) for i in range(3)],
            [max(point[i] for point in corners) for i in range(3)])


def angular_delta(a: float, b: float) -> float:
    return abs((float(a) - float(b) + 180.0) % 360.0 - 180.0)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("assembly", type=Path)
    parser.add_argument("--envelope", nargs=3, type=float, metavar=("X", "Y", "Z"))
    args = parser.parse_args()
    assembly_path = args.assembly.resolve()
    document = json.loads(assembly_path.read_text(encoding="utf-8"))
    repo = Path(__file__).resolve().parent.parent
    issues: list[str] = []

    assets = document.get("assets") or {}
    instances = document.get("instances") or []
    receivers = document.get("receivers") or []
    if document.get("schema") != "art-forge-assembly-v1":
        issues.append("unsupported schema")
    for asset_id, asset in assets.items():
        source = Path(asset.get("path") or "")
        if not source.is_absolute():
            source = repo / source
        if not source.is_file():
            issues.append(f"missing source for {asset_id}: {source}")

    receiver_ids = [receiver.get("id") for receiver in receivers]
    duplicates = sorted({receiver_id for receiver_id in receiver_ids if receiver_ids.count(receiver_id) > 1})
    if duplicates:
        issues.append(f"duplicate receiver ids: {', '.join(duplicates)}")
    receiver_by_id = {receiver.get("id"): receiver for receiver in receivers}

    envelope = args.envelope
    checked_bounds = []
    checked_supports = []
    for instance in instances:
        asset = assets.get(instance.get("asset"))
        if not asset:
            issues.append(f"{instance.get('id', '?')} references an unknown asset")
            continue
        size = instance.get("size") or asset.get("size")
        position = instance.get("position", [0, 0, 0])
        rotation = instance.get("rotation", [0, 0, 0])
        if not isinstance(size, list) or len(size) != 3:
            issues.append(f"{instance.get('id', '?')} has no three-axis size")
            continue
        minimum, maximum = bounds(size, position, rotation)
        checked_bounds.append({"id": instance.get("id"), "min": minimum, "max": maximum})
        if envelope and instance.get("asset") != "base":
            ex, ey, ez = envelope
            if minimum[0] < -ex / 2 or maximum[0] > ex / 2 or minimum[2] < -ez / 2 or maximum[2] > ez / 2:
                issues.append(f"{instance.get('id')} exceeds the {ex:g} x {ez:g} footprint")
            if minimum[1] < 0 or maximum[1] > ey:
                issues.append(f"{instance.get('id')} exceeds the 0..{ey:g} m height envelope")
        if instance.get("asset") != "base":
            receiver = receiver_by_id.get(f"{instance.get('id')}-receiver")
            if not receiver:
                issues.append(f"{instance.get('id')} has no named receiver")
            elif receiver.get("position") != position or receiver.get("rotation") != rotation:
                issues.append(f"{instance.get('id')} does not match its recorded receiver transform")

        support = instance.get("support")
        if support:
            instance_id = instance.get("id", "?")
            mode = support.get("mode")
            tolerance = float(support.get("tolerance", 0.02))
            if mode == "surface":
                point = support.get("point")
                if not isinstance(point, list) or len(point) != 3:
                    issues.append(f"{instance_id} has an invalid surface support point")
                elif abs(float(rotation[0])) > tolerance or abs(float(rotation[2])) > tolerance:
                    issues.append(f"{instance_id} uses surface support with a pitched transform")
                elif any(abs(float(position[i]) - float(point[i])) > tolerance for i in range(3)):
                    issues.append(f"{instance_id} is not seated on its recorded base-mesh surface")
                else:
                    checked_supports.append({"id": instance_id, "mode": mode, "point": point})
            elif mode == "bridge":
                start, end = support.get("start"), support.get("end")
                if not all(isinstance(point, list) and len(point) == 3 for point in (start, end)):
                    issues.append(f"{instance_id} has invalid bridge endpoints")
                else:
                    vector = [float(end[i]) - float(start[i]) for i in range(3)]
                    length = math.sqrt(sum(value * value for value in vector))
                    expected_position = [
                        (float(start[0]) + float(end[0])) / 2,
                        (float(start[1]) + float(end[1])) / 2,
                        (float(start[2]) + float(end[2])) / 2,
                    ]
                    expected_yaw = math.degrees(math.atan2(-vector[2], vector[0]))
                    expected_pitch = math.degrees(math.asin(vector[1] / length))
                    expected_position[1] -= float(size[1]) / 2 * math.cos(math.radians(expected_pitch))
                    checks = [
                        abs(float(position[i]) - expected_position[i]) <= tolerance for i in range(3)
                    ] + [
                        angular_delta(rotation[1], expected_yaw) <= tolerance,
                        angular_delta(rotation[2], expected_pitch) <= tolerance,
                        abs(float(size[0]) - length) <= tolerance,
                    ]
                    if not all(checks):
                        issues.append(f"{instance_id} does not fit its recorded bridge endpoints")
                    else:
                        checked_supports.append({"id": instance_id, "mode": mode, "start": start, "end": end})
            elif mode == "withheld":
                if instance.get("visible") is not False:
                    issues.append(f"{instance_id} is incomplete but still visible")
                else:
                    checked_supports.append({"id": instance_id, "mode": mode})
            else:
                issues.append(f"{instance_id} has unsupported attachment mode {mode!r}")

    result = {
        "ok": not issues,
        "schema": document.get("schema"),
        "assets": len(assets),
        "instances": len(instances),
        "receivers": len(receivers),
        "supports": len(checked_supports),
        "issues": issues,
        "bounds": checked_bounds,
    }
    print(json.dumps(result, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
