"""Embed a Fragile Art PBR material set into a GLB without changing its geometry or UVs."""
from __future__ import annotations

import argparse
import json
import struct
from pathlib import Path


JSON_CHUNK = 0x4E4F534A
BIN_CHUNK = 0x004E4942


def pad(data: bytes, byte: bytes) -> bytes:
    return data + byte * ((-len(data)) % 4)


def read_glb(path: Path) -> tuple[dict, bytes]:
    data = path.read_bytes()
    magic, version, total = struct.unpack_from("<4sII", data, 0)
    if magic != b"glTF" or version != 2 or total != len(data):
        raise ValueError(f"{path} is not a valid glTF 2.0 GLB")
    document = None
    binary = b""
    offset = 12
    while offset < len(data):
        length, kind = struct.unpack_from("<II", data, offset)
        payload = data[offset + 8:offset + 8 + length]
        if kind == JSON_CHUNK:
            document = json.loads(payload.decode("utf-8").rstrip(" \t\r\n\0"))
        elif kind == BIN_CHUNK:
            binary = payload
        offset += 8 + length
    if document is None:
        raise ValueError("GLB has no JSON chunk")
    return document, binary


def apply(input_path: Path, output_path: Path, material_dir: Path) -> None:
    document, binary = read_glb(input_path)
    metadata = json.loads((material_dir / "material.json").read_text(encoding="utf-8"))
    image_specs = [
        (metadata["base_color"], "base colour"),
        (metadata["metallic_roughness"], "metallic roughness"),
        (metadata["normal"], "normal"),
        (metadata["emission"], "emission"),
    ]
    buffer_views = document.setdefault("bufferViews", [])
    images = []
    combined = bytearray(binary)
    while len(combined) % 4:
        combined.append(0)
    for filename, label in image_specs:
        payload = (material_dir / filename).read_bytes()
        offset = len(combined)
        combined.extend(payload)
        while len(combined) % 4:
            combined.append(0)
        view_index = len(buffer_views)
        buffer_views.append({"buffer": 0, "byteOffset": offset, "byteLength": len(payload)})
        images.append({"name": f"{metadata['name']} {label}", "bufferView": view_index,
                       "mimeType": "image/png"})

    document["images"] = images
    document["samplers"] = [{"magFilter": 9729, "minFilter": 9987,
                             "wrapS": 10497, "wrapT": 10497}]
    document["textures"] = [{"sampler": 0, "source": index} for index in range(4)]
    document["materials"] = [{
        "name": metadata["name"],
        "pbrMetallicRoughness": {
            "baseColorFactor": [1, 1, 1, 1],
            "baseColorTexture": {"index": 0, "texCoord": 0},
            "metallicFactor": 1.0,
            "roughnessFactor": 1.0,
            "metallicRoughnessTexture": {"index": 1, "texCoord": 0},
        },
        "normalTexture": {"index": 2, "texCoord": 0, "scale": 0.45},
        "emissiveFactor": [0, 0, 0],
        "emissiveTexture": {"index": 3, "texCoord": 0},
        "alphaMode": "OPAQUE",
        "doubleSided": True,
        "extras": {"pipeline": "MAT-TER-001", "source": input_path.name},
    }]
    for mesh in document.get("meshes", []):
        for primitive in mesh.get("primitives", []):
            primitive["material"] = 0
    document.setdefault("buffers", [{"byteLength": 0}])[0]["byteLength"] = len(combined)
    document.setdefault("asset", {})["generator"] = "Fragile Art MAT-TER-001 material applicator"

    json_bytes = pad(json.dumps(document, separators=(",", ":")).encode("utf-8"), b" ")
    bin_bytes = pad(bytes(combined), b"\0")
    total = 12 + 8 + len(json_bytes) + 8 + len(bin_bytes)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as stream:
        stream.write(struct.pack("<4sII", b"glTF", 2, total))
        stream.write(struct.pack("<II", len(json_bytes), JSON_CHUNK))
        stream.write(json_bytes)
        stream.write(struct.pack("<II", len(bin_bytes), BIN_CHUNK))
        stream.write(bin_bytes)
    print(f"wrote {output_path} ({output_path.stat().st_size / 1048576:.1f} MB)")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("material_dir", type=Path)
    args = parser.parse_args()
    apply(args.input.resolve(), args.output.resolve(), args.material_dir.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
