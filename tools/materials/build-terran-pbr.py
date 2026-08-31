"""Build seamless, power-of-two Terran PBR material sets from approved colour sources."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Materials" / "Terran" / "MAT-TER-001" / "Source"
OUTPUT = ROOT / "Materials" / "Terran" / "MAT-TER-001"
SIZE = 2048

MATERIALS = {
    "armour": {"roughness": 0.70, "metallic": 0.02, "normal_strength": 2.0},
    "graphite": {"roughness": 0.56, "metallic": 0.78, "normal_strength": 1.6},
    "concrete": {"roughness": 0.88, "metallic": 0.0, "normal_strength": 2.5},
    "amber": {"roughness": 0.66, "metallic": 0.02, "normal_strength": 1.8},
}


def seamless(source: Image.Image) -> Image.Image:
    """Mirror a source into a periodic 2x2 field; opposite edges then match exactly."""
    source = source.convert("RGB")
    w, h = source.size
    tiled = Image.new("RGB", (w * 2, h * 2))
    tiled.paste(source, (0, 0))
    tiled.paste(ImageOps.mirror(source), (w, 0))
    tiled.paste(ImageOps.flip(source), (0, h))
    tiled.paste(ImageOps.flip(ImageOps.mirror(source)), (w, h))
    return tiled.resize((SIZE, SIZE), Image.Resampling.LANCZOS)


def normal_from_colour(colour: Image.Image, strength: float) -> Image.Image:
    grey = np.asarray(colour.convert("L"), dtype=np.float32) / 255.0
    low = np.asarray(colour.convert("L").filter(ImageFilter.GaussianBlur(10)), dtype=np.float32) / 255.0
    height = grey - low
    dx = (np.roll(height, -1, axis=1) - np.roll(height, 1, axis=1)) * strength
    dy = (np.roll(height, -1, axis=0) - np.roll(height, 1, axis=0)) * strength
    normal = np.dstack((-dx, dy, np.ones_like(height)))
    normal /= np.maximum(np.linalg.norm(normal, axis=2, keepdims=True), 1e-6)
    return Image.fromarray(np.uint8(np.clip(normal * 0.5 + 0.5, 0, 1) * 255), "RGB")


def metallic_roughness(colour: Image.Image, roughness: float, metallic: float) -> Image.Image:
    grey = np.asarray(colour.convert("L"), dtype=np.float32) / 255.0
    low = np.asarray(colour.convert("L").filter(ImageFilter.GaussianBlur(18)), dtype=np.float32) / 255.0
    variation = np.clip((grey - low) * 0.45, -0.08, 0.08)
    r = np.full_like(grey, 255.0)
    g = np.clip((roughness + variation) * 255.0, 0, 255)
    b = np.full_like(grey, metallic * 255.0)
    return Image.fromarray(np.uint8(np.dstack((r, g, b))), "RGB")


def main() -> int:
    for name, settings in MATERIALS.items():
        source = SOURCE / f"MAT-TER-001_{name}_base-color-source_v01.png"
        if not source.is_file():
            raise FileNotFoundError(source)
        folder = OUTPUT / name
        folder.mkdir(parents=True, exist_ok=True)
        colour = seamless(Image.open(source))
        base = folder / f"MAT-TER-001_{name}_base_color_v01.png"
        normal = folder / f"MAT-TER-001_{name}_normal_v01.png"
        mr = folder / f"MAT-TER-001_{name}_metallic_roughness_v01.png"
        emission = folder / f"MAT-TER-001_{name}_emission_v01.png"
        colour.save(base, optimize=True)
        normal_from_colour(colour, settings["normal_strength"]).save(normal, optimize=True)
        metallic_roughness(colour, settings["roughness"], settings["metallic"]).save(mr, optimize=True)
        Image.new("RGB", (4, 4), (0, 0, 0)).save(emission, optimize=True)
        metadata = {
            "schema": "fragile-art-pbr-v1",
            "name": f"MAT-TER-001_{name.upper()}",
            "tile_size": SIZE,
            "source": str(source.relative_to(ROOT)).replace("\\", "/"),
            "base_color": base.name,
            "normal": normal.name,
            "metallic_roughness": mr.name,
            "emission": emission.name,
            "roughness": settings["roughness"],
            "metallic": settings["metallic"],
        }
        (folder / "material.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
        print(f"built {name}: {folder.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
