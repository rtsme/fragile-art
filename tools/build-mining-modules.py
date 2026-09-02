"""Build the Basic Mine's three manual-route shared modules as textured GLBs.

The output is deliberately modular, dimensioned in metres, and uses embedded
Terran material textures so the models remain self-contained in Art Forge.
"""
from __future__ import annotations

import argparse
import base64
import io
import json
import math
import struct
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from PIL import Image


MATERIALS = (
    ("Terran_Graphite", (56, 61, 63), 0.72, 0.62),
    ("Terran_Armour", (205, 201, 188), 0.22, 0.68),
    ("Terran_Hazard", (202, 126, 14), 0.34, 0.58),
)


def texture_png(colour: tuple[int, int, int]) -> bytes:
    image = Image.new("RGB", (64, 64), colour)
    pixels = image.load()
    for y in range(64):
        for x in range(64):
            grain = ((x * 17 + y * 29 + x * y * 3) % 15) - 7
            wear = -18 if ((x * 13 + y * 7) % 97 == 0) else 0
            pixels[x, y] = tuple(max(0, min(255, c + grain + wear)) for c in colour)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG", optimize=True)
    return buffer.getvalue()


@dataclass
class Primitive:
    positions: list[tuple[float, float, float]] = field(default_factory=list)
    normals: list[tuple[float, float, float]] = field(default_factory=list)
    uvs: list[tuple[float, float]] = field(default_factory=list)
    indices: list[int] = field(default_factory=list)
    material: int = 0


class Builder:
    def __init__(self) -> None:
        self.primitives: list[Primitive] = []

    def add_box(
        self,
        center: tuple[float, float, float],
        size: tuple[float, float, float],
        material: int = 0,
        axes: np.ndarray | None = None,
    ) -> None:
        cx, cy, cz = center
        sx, sy, sz = (value / 2 for value in size)
        transform = np.eye(3) if axes is None else axes
        faces = (
            ((1, 0, 0), ((sx, -sy, -sz), (sx, sy, -sz), (sx, sy, sz), (sx, -sy, sz))),
            ((-1, 0, 0), ((-sx, -sy, sz), (-sx, sy, sz), (-sx, sy, -sz), (-sx, -sy, -sz))),
            ((0, 1, 0), ((-sx, sy, -sz), (-sx, sy, sz), (sx, sy, sz), (sx, sy, -sz))),
            ((0, -1, 0), ((-sx, -sy, sz), (-sx, -sy, -sz), (sx, -sy, -sz), (sx, -sy, sz))),
            ((0, 0, 1), ((-sx, -sy, sz), (sx, -sy, sz), (sx, sy, sz), (-sx, sy, sz))),
            ((0, 0, -1), ((sx, -sy, -sz), (-sx, -sy, -sz), (-sx, sy, -sz), (sx, sy, -sz))),
        )
        primitive = Primitive(material=material)
        for normal, corners in faces:
            start = len(primitive.positions)
            world_normal = transform @ np.asarray(normal, dtype=float)
            for corner, uv in zip(corners, ((0, 0), (1, 0), (1, 1), (0, 1))):
                world = transform @ np.asarray(corner, dtype=float) + np.asarray((cx, cy, cz))
                primitive.positions.append(tuple(float(v) for v in world))
                primitive.normals.append(tuple(float(v) for v in world_normal))
                primitive.uvs.append(uv)
            primitive.indices.extend((start, start + 1, start + 2, start, start + 2, start + 3))
        self.primitives.append(primitive)

    def add_bar(
        self,
        start: tuple[float, float, float],
        end: tuple[float, float, float],
        thickness: tuple[float, float],
        material: int = 0,
    ) -> None:
        p0 = np.asarray(start, dtype=float)
        p1 = np.asarray(end, dtype=float)
        direction = p1 - p0
        length = float(np.linalg.norm(direction))
        y_axis = direction / length
        helper = np.asarray((0.0, 0.0, 1.0)) if abs(y_axis[2]) < 0.9 else np.asarray((1.0, 0.0, 0.0))
        x_axis = np.cross(helper, y_axis)
        x_axis /= np.linalg.norm(x_axis)
        z_axis = np.cross(x_axis, y_axis)
        axes = np.column_stack((x_axis, y_axis, z_axis))
        self.add_box(tuple((p0 + p1) / 2), (thickness[0], length, thickness[1]), material, axes)

    def add_cylinder(
        self,
        center: tuple[float, float, float],
        radius: float,
        height: float,
        material: int = 0,
        segments: int = 16,
    ) -> None:
        cx, cy, cz = center
        primitive = Primitive(material=material)
        bottom, top = cy - height / 2, cy + height / 2
        for i in range(segments):
            angle0 = 2 * math.pi * i / segments
            angle1 = 2 * math.pi * (i + 1) / segments
            x0, z0 = math.cos(angle0), math.sin(angle0)
            x1, z1 = math.cos(angle1), math.sin(angle1)
            start = len(primitive.positions)
            primitive.positions.extend(((cx + radius*x0, bottom, cz + radius*z0),
                                        (cx + radius*x1, bottom, cz + radius*z1),
                                        (cx + radius*x1, top, cz + radius*z1),
                                        (cx + radius*x0, top, cz + radius*z0)))
            primitive.normals.extend(((x0, 0, z0), (x1, 0, z1), (x1, 0, z1), (x0, 0, z0)))
            primitive.uvs.extend(((i/segments, 0), ((i+1)/segments, 0), ((i+1)/segments, 1), (i/segments, 1)))
            primitive.indices.extend((start, start+1, start+2, start, start+2, start+3))
        for y, normal, reverse in ((top, (0, 1, 0), False), (bottom, (0, -1, 0), True)):
            center_index = len(primitive.positions)
            primitive.positions.append((cx, y, cz))
            primitive.normals.append(normal)
            primitive.uvs.append((0.5, 0.5))
            for i in range(segments):
                angle = 2 * math.pi * i / segments
                primitive.positions.append((cx + radius*math.cos(angle), y, cz + radius*math.sin(angle)))
                primitive.normals.append(normal)
                primitive.uvs.append((0.5 + 0.5*math.cos(angle), 0.5 + 0.5*math.sin(angle)))
            for i in range(segments):
                a = center_index + 1 + i
                b = center_index + 1 + ((i + 1) % segments)
                primitive.indices.extend((center_index, b, a) if reverse else (center_index, a, b))
        self.primitives.append(primitive)


def build_gantry() -> Builder:
    b = Builder()
    for x in (-4.0, 4.0):
        for z in (-2.0, 2.0):
            b.add_box((x, 0.45, z), (2.0, 0.9, 1.6), 0)
            b.add_bar((x, 0.9, z), (x * 0.72, 16.2, z * 0.78), (0.72, 0.72), 0)
            b.add_bar((x, 3.2, z), (x * 0.84, 7.4, -z * 0.78), (0.38, 0.34), 1)
            b.add_bar((x * 0.84, 7.4, z * 0.78), (x * 0.76, 11.5, -z * 0.78), (0.38, 0.34), 0)
            b.add_bar((x * 0.76, 11.5, z * 0.78), (x * 0.72, 15.7, -z * 0.78), (0.38, 0.34), 1)
    for z in (-1.55, 1.55):
        b.add_bar((-3.0, 16.2, z), (3.0, 16.2, z), (0.8, 0.72), 0)
        b.add_bar((-3.0, 17.25, z), (3.0, 17.25, z), (0.9, 0.76), 1)
    b.add_box((0, 17.25, 0), (7.0, 1.4, 3.8), 0)
    b.add_box((0, 17.42, 0), (5.5, 0.65, 4.05), 1)
    for x in (-2.55, 2.55):
        b.add_box((x, 17.5, 0), (0.32, 0.72, 4.15), 2)
    return b


def build_rotary() -> Builder:
    b = Builder()
    layers = ((0.45, 1.65, 0.9, 0), (1.15, 1.95, 0.55, 1), (1.85, 1.75, 0.85, 0),
              (2.65, 1.9, 0.75, 1), (3.45, 1.55, 0.85, 0), (4.25, 1.25, 0.65, 2), (4.7, 0.9, 0.3, 0))
    for y, radius, height, material in layers:
        b.add_cylinder((0, y, 0), radius, height, material, 20)
    for angle in range(0, 360, 45):
        radians = math.radians(angle)
        b.add_box((1.72*math.cos(radians), 2.6, 1.72*math.sin(radians)), (0.32, 1.65, 0.32), 2)
    return b


def build_shaft() -> Builder:
    b = Builder()
    b.add_cylinder((0, 4.0, 0), 0.48, 8.0, 1, 16)
    for y in (0.35, 1.4, 2.45, 3.5, 4.55, 5.6, 6.65, 7.65):
        b.add_cylinder((0, y, 0), 0.72 if y in (0.35, 7.65) else 0.61, 0.28, 0, 16)
    for y in (1.9, 4.0, 6.1):
        b.add_cylinder((0, y, 0), 0.64, 0.16, 2, 16)
    return b


def pack_glb(builder: Builder, name: str, output: Path) -> None:
    binary = bytearray()
    buffer_views: list[dict] = []
    accessors: list[dict] = []

    def append_blob(data: bytes, target: int | None = None) -> int:
        while len(binary) % 4:
            binary.append(0)
        offset = len(binary)
        binary.extend(data)
        view = {"buffer": 0, "byteOffset": offset, "byteLength": len(data)}
        if target is not None:
            view["target"] = target
        buffer_views.append(view)
        return len(buffer_views) - 1

    def accessor(array: np.ndarray, component_type: int, kind: str, target: int, include_bounds: bool = False) -> int:
        view = append_blob(array.tobytes(), target)
        entry = {"bufferView": view, "componentType": component_type, "count": len(array), "type": kind}
        if include_bounds:
            entry["min"] = array.min(axis=0).astype(float).tolist()
            entry["max"] = array.max(axis=0).astype(float).tolist()
        accessors.append(entry)
        return len(accessors) - 1

    primitives = []
    for primitive in builder.primitives:
        positions = np.asarray(primitive.positions, dtype="<f4")
        normals = np.asarray(primitive.normals, dtype="<f4")
        uvs = np.asarray(primitive.uvs, dtype="<f4")
        indices = np.asarray(primitive.indices, dtype="<u4")
        primitives.append({
            "attributes": {
                "POSITION": accessor(positions, 5126, "VEC3", 34962, True),
                "NORMAL": accessor(normals, 5126, "VEC3", 34962),
                "TEXCOORD_0": accessor(uvs, 5126, "VEC2", 34962),
            },
            "indices": accessor(indices, 5125, "SCALAR", 34963),
            "material": primitive.material,
            "mode": 4,
        })

    images = []
    textures = []
    materials = []
    for index, (material_name, colour, metallic, roughness) in enumerate(MATERIALS):
        image_view = append_blob(texture_png(colour))
        images.append({"name": f"{material_name}_Texture", "mimeType": "image/png", "bufferView": image_view})
        textures.append({"source": index, "sampler": 0})
        materials.append({
            "name": material_name,
            "pbrMetallicRoughness": {
                "baseColorTexture": {"index": index},
                "metallicFactor": metallic,
                "roughnessFactor": roughness,
            },
        })

    document = {
        "asset": {"version": "2.0", "generator": "Fragile Art procedural mining-module builder"},
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "nodes": [{"name": name, "mesh": 0}],
        "meshes": [{"name": name, "primitives": primitives}],
        "materials": materials,
        "samplers": [{"magFilter": 9729, "minFilter": 9987, "wrapS": 10497, "wrapT": 10497}],
        "textures": textures,
        "images": images,
        "accessors": accessors,
        "bufferViews": buffer_views,
        "buffers": [{"byteLength": len(binary)}],
    }
    json_bytes = json.dumps(document, separators=(",", ":")).encode("utf-8")
    json_bytes += b" " * ((4 - len(json_bytes) % 4) % 4)
    binary += b"\x00" * ((4 - len(binary) % 4) % 4)
    total = 12 + 8 + len(json_bytes) + 8 + len(binary)
    glb = bytearray(struct.pack("<4sII", b"glTF", 2, total))
    glb.extend(struct.pack("<II", len(json_bytes), 0x4E4F534A))
    glb.extend(json_bytes)
    glb.extend(struct.pack("<II", len(binary), 0x004E4942))
    glb.extend(binary)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(glb)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=Path("Models/Terran/Shared"))
    args = parser.parse_args()
    assets = {
        "TER-MAN-GAN-L": build_gantry(),
        "TER-DRL-ROT-L": build_rotary(),
        "TER-DRL-SFT-L": build_shaft(),
    }
    for asset_id, builder in assets.items():
        output = args.output_root / asset_id / f"{asset_id}_procedural_v01.glb"
        pack_glb(builder, asset_id, output)
        print(f"{output} ({output.stat().st_size:,} bytes; {len(builder.primitives)} primitives)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
