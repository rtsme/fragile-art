"""Art Forge - browse art, inspect GLB/GLTF models and run 3D generation.

The viewer and Meshy backend are standalone. Modly is optional and is used only
as the current adapter for a configured local generation model.

Stdlib only - run with Python 3.12:  py -3.12 forge.py
"""
from __future__ import annotations

import base64
import json
import mimetypes
import os
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

# --------------------------------------------------------------------------- #
# Configuration - environment variables win, so this is portable off my machine
# --------------------------------------------------------------------------- #

HERE = Path(__file__).resolve().parent

# Modly is optional and deliberately has no developer-specific default. A fresh
# clone stays in viewer/Meshy-only mode until MODLY_DIR is configured.
MODLY_DIR = Path(os.environ.get("MODLY_DIR", HERE / "_modly-not-configured")).expanduser()
MODLY_DATA = Path(
    os.environ.get("MODLY_DATA", Path.home() / ".fragile-art" / "modly-data")
).expanduser()
MODLY_API = os.environ.get("MODLY_API_URL", "http://127.0.0.1:8765")

# The art repo root — Concepts/, References/ and Models/ sit directly under it.
ART_ROOT = Path(os.environ.get("ART_ROOT", HERE.parent.parent))
MODEL_ID = os.environ.get("MODLY_MODEL_ID", "hunyuan3d-mini/generate")

FORGE_PORT = int(os.environ.get("FORGE_PORT", "8770"))
APP_VERSION = "1.3.0"

CHECK_VIEWS = HERE.parent / "check-views.py"

CLI = MODLY_DIR / "tools" / "modly-cli" / "agent.py"
API_DIR = MODLY_DIR / "api"
API_PY = API_DIR / ".venv" / "Scripts" / "python.exe"

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
MESH_EXTS = {".glb", ".gltf"}
ASSEMBLY_SUFFIX = ".assembly.json"
VENDOR = HERE / "vendor"

# Meshy cloud backend. The key is read from the environment or a local file that
# is gitignored — it is never stored in the repo.
MESHY_BASE = os.environ.get("MESHY_API_URL", "https://api.meshy.ai/openapi/v1")
MESHY_KEY_FILE = HERE / "meshy.key"
MESHY_MAX_IMAGES = 4          # multi-image-to-3d accepts at most four
MESHY_POLL_SECONDS = 3.0

# Modly's backend takes a while to import torch on a cold start.
BACKEND_BOOT_TIMEOUT = 120


def python312() -> str:
    """The interpreter used to run Modly's CLI. The CLI is stdlib-only."""
    return sys.executable


def local_available() -> bool:
    """Whether the optional Modly-powered local generator is installed."""
    return CLI.is_file() and API_PY.is_file()


def helper_python() -> str:
    """Use Modly's environment when present, otherwise Art Forge's Python."""
    return str(API_PY if API_PY.is_file() else Path(sys.executable))


# --------------------------------------------------------------------------- #
# Job state - one generation at a time, guarded by a lock
# --------------------------------------------------------------------------- #


class Job:
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.reset()

    def reset(self) -> None:
        self.status = "idle"      # idle | running | done | error | cancelled
        self.progress = 0
        self.step = ""
        self.error: str | None = None
        self.result: dict | None = None
        self.run_id: str | None = None
        self.started_at: float | None = None
        self.finished_at: float | None = None
        self.image: str | None = None
        self.output: str | None = None
        self.log: list[str] = []
        self.proc: subprocess.Popen | None = None

    def snapshot(self) -> dict:
        with self.lock:
            elapsed = 0.0
            if self.started_at:
                end = self.finished_at or time.time()
                elapsed = round(end - self.started_at, 1)
            return {
                "status": self.status,
                "progress": self.progress,
                "step": self.step,
                "error": self.error,
                "result": self.result,
                "run_id": self.run_id,
                "elapsed": elapsed,
                "image": self.image,
                "output": self.output,
                "log": self.log[-40:],
            }

    def note(self, line: str) -> None:
        with self.lock:
            self.log.append(line)


JOB = Job()


# --------------------------------------------------------------------------- #
# Modly backend
# --------------------------------------------------------------------------- #


def backend_up(timeout: float = 2.0) -> bool:
    if not local_available():
        return False
    try:
        with urllib.request.urlopen(f"{MODLY_API}/health", timeout=timeout) as r:
            return r.status == 200
    except Exception:
        return False


def port_busy(port: int) -> bool:
    with socket.socket() as s:
        s.settimeout(0.4)
        return s.connect_ex(("127.0.0.1", port)) == 0


def start_backend() -> tuple[bool, str]:
    """Boot Modly's FastAPI backend with the same env Electron would give it."""
    if not local_available():
        return False, (
            "Local generation is unavailable because Modly is not installed. "
            "The Art Forge viewer and Meshy generator do not require Modly."
        )
    if backend_up():
        return True, "already running"

    env = {
        **os.environ,
        "MODELS_DIR": str(MODLY_DATA / "models"),
        "WORKSPACE_DIR": str(MODLY_DATA / "workspace"),
        "EXTENSIONS_DIR": str(MODLY_DATA / "ext"),
        "PYTHONUNBUFFERED": "1",
    }
    log = MODLY_DATA / "backend.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    handle = open(log, "ab", buffering=0)
    subprocess.Popen(
        [str(API_PY), "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8765"],
        cwd=str(API_DIR),
        env=env,
        stdout=handle,
        stderr=subprocess.STDOUT,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )

    deadline = time.time() + BACKEND_BOOT_TIMEOUT
    while time.time() < deadline:
        if backend_up():
            return True, "started"
        time.sleep(1.0)
    return False, f"backend did not answer within {BACKEND_BOOT_TIMEOUT}s (see {log})"


def model_state() -> dict:
    try:
        with urllib.request.urlopen(f"{MODLY_API}/model/status", timeout=4) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception:
        return {}


# --------------------------------------------------------------------------- #
# Generation
# --------------------------------------------------------------------------- #


def run_generation(image: Path, output: Path, steps: int, octree: int, remesh: str, seed: int | None) -> None:
    params = {"num_inference_steps": steps, "octree_resolution": octree}
    if seed is not None:
        params["seed"] = seed

    cmd = [
        python312(), str(CLI), "generate",
        "--image", str(image),
        "--output", str(output),
        "--model", MODEL_ID,
        "--no-texture",
        "--remesh", remesh,
        "--format", "glb",
        "--timeout", "7200",
        "--poll", "1.5",
        "--progress",
        "--params-json", json.dumps(params),
    ]

    output.parent.mkdir(parents=True, exist_ok=True)
    JOB.note(f"$ {' '.join(cmd[2:])}")

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    with JOB.lock:
        JOB.proc = proc

    def pump_stderr() -> None:
        assert proc.stderr is not None
        for raw in proc.stderr:
            line = raw.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                JOB.note(line)
                continue
            with JOB.lock:
                if JOB.status != "running":
                    continue
                JOB.progress = int(msg.get("progress") or 0)
                JOB.step = msg.get("step") or JOB.step
                JOB.run_id = msg.get("run_id") or JOB.run_id

    pump = threading.Thread(target=pump_stderr, daemon=True)
    pump.start()

    stdout, _ = proc.communicate()
    pump.join(timeout=3)

    payload: dict | None = None
    if stdout:
        try:
            payload = json.loads(stdout)
        except json.JSONDecodeError:
            JOB.note(stdout.strip()[-800:])

    with JOB.lock:
        if JOB.status == "cancelled":
            return
        ok = proc.returncode == 0 and bool(payload and payload.get("ok"))
        if ok:
            JOB.status = "done"
            JOB.progress = 100
            JOB.step = "Done"
            JOB.result = payload
        else:
            JOB.status = "error"
            JOB.error = (payload or {}).get("message") or f"generation failed (exit {proc.returncode})"
        JOB.finished_at = time.time()

    if JOB.status == "done":
        stats = mesh_stats(output)
        if stats:
            with JOB.lock:
                JOB.result = {**(JOB.result or {}), "mesh": stats}


# --------------------------------------------------------------------------- #
# Meshy cloud backend
# --------------------------------------------------------------------------- #


def meshy_key() -> str | None:
    key = os.environ.get("MESHY_API_KEY", "").strip()
    if key:
        return key
    if MESHY_KEY_FILE.exists():
        key = MESHY_KEY_FILE.read_text(encoding="utf-8").strip()
        if key:
            return key
    return None


def _meshy_request(method: str, path: str, key: str, body: dict | None = None, timeout: int = 90) -> dict:
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(
        f"{MESHY_BASE}{path}",
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:400]
        raise RuntimeError(f"Meshy {exc.code}: {detail}") from exc


def _prepare_image(path: Path, max_px: int = 2048) -> Path:
    """
    Flatten to a high-quality JPEG before upload, downscaling only if very large.

    Four full-size PNGs base64 to ~10 MB, which is slow to upload and was present
    on a request that timed out. 2048px at q92 lands around 2-3 MB for four images
    while keeping the panel-line detail the generator actually reconstructs from —
    1024px was over-aggressive and cost real fidelity. Falls back to the original
    if Pillow isn't reachable.
    """
    out_dir = Path(tempfile.gettempdir()) / "art-forge-upload"
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / (path.stem + ".jpg")
    snippet = (
        "import sys\n"
        "from PIL import Image\n"
        "src, dst, mx = sys.argv[1], sys.argv[2], int(sys.argv[3])\n"
        "im = Image.open(src)\n"
        "if im.mode in ('RGBA', 'LA', 'P'):\n"
        "    im = im.convert('RGBA')\n"
        "    bg = Image.new('RGB', im.size, (255, 255, 255))\n"
        "    bg.paste(im, mask=im.split()[-1])\n"
        "    im = bg\n"
        "else:\n"
        "    im = im.convert('RGB')\n"
        "im.thumbnail((mx, mx), Image.LANCZOS)\n"
        "im.save(dst, 'JPEG', quality=92, optimize=True)\n"
    )
    try:
        r = subprocess.run(
            [helper_python(), "-c", snippet, str(path), str(dst), str(max_px)],
            capture_output=True, text=True, timeout=120,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        if r.returncode == 0 and dst.is_file() and dst.stat().st_size > 0:
            return dst
        JOB.note(f"resize failed for {path.name}, sending original: {r.stderr.strip()[:160]}")
    except Exception as exc:
        JOB.note(f"resize error for {path.name}, sending original: {exc}")
    return path


def _data_uri(path: Path) -> str:
    import base64
    mime = "image/jpeg" if path.suffix.lower() in (".jpg", ".jpeg") else "image/png"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def _download(url: str, dest: Path) -> int:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=300) as resp, open(dest, "wb") as fh:
        shutil.copyfileobj(resp, fh, length=1 << 20)
    return dest.stat().st_size


def run_meshy(images: list[Path], output: Path, opts: dict) -> None:
    """Multi-image -> textured, retopologised mesh via Meshy's cloud API."""
    key = meshy_key()
    if not key:
        raise RuntimeError(
            "No Meshy API key. Set MESHY_API_KEY, or put the key in "
            f"{MESHY_KEY_FILE}"
        )

    picked = images[:MESHY_MAX_IMAGES]
    with JOB.lock:
        JOB.step = "Preparing images…"
    JOB.note(f"Meshy: uploading {len(picked)} image(s); first is the front view")

    uris, total = [], 0
    for i, p in enumerate(picked):
        small = _prepare_image(p)
        uri = _data_uri(small)
        total += len(uri)
        uris.append(uri)
        JOB.note(f"  {'front' if i == 0 else f'view {i+1}'}: {p.name} "
                 f"({small.stat().st_size/1024:.0f} KB)")
    JOB.note(f"payload: {total/1048576:.1f} MB base64")

    body = {
        "image_urls":        uris,
        "should_texture":    bool(opts.get("texture", True)),
        "enable_pbr":        bool(opts.get("pbr", True)),
        "texture_resolution": opts.get("texture_resolution", "2k"),
        "target_formats":    ["glb"],
        "ai_model":          opts.get("ai_model", "latest"),
    }

    # Meshy's own guidance: "For the highest-quality model, we recommend setting
    # should_remesh to false." Remeshing retopologises and decimates the result,
    # which costs exactly the crisp mechanical detail these buildings are made of.
    # Only send topology/polycount when the caller actually asked to remesh.
    if opts.get("remesh"):
        body["should_remesh"] = True
        body["topology"] = opts.get("topology", "quad")
        body["target_polycount"] = int(opts.get("polycount", 30000))
    else:
        body["should_remesh"] = False
    if opts.get("texture_prompt"):
        body["texture_prompt"] = str(opts["texture_prompt"])[:600]

    with JOB.lock:
        JOB.step = "Submitting to Meshy…"
    created = _meshy_request("POST", "/multi-image-to-3d", key, body)
    task_id = created.get("result")
    if not task_id:
        raise RuntimeError(f"Meshy did not return a task id: {created}")

    with JOB.lock:
        JOB.run_id = task_id
    JOB.note(f"Meshy task {task_id}")

    status = {}
    while True:
        with JOB.lock:
            if JOB.status == "cancelled":
                return
        time.sleep(MESHY_POLL_SECONDS)
        status = _meshy_request("GET", f"/multi-image-to-3d/{task_id}", key)
        state = status.get("status")
        with JOB.lock:
            # leave the last 10% for downloading
            JOB.progress = min(int(status.get("progress") or 0), 99)
            JOB.step = {"PENDING": "Queued at Meshy…",
                        "IN_PROGRESS": "Generating…"}.get(state, state or "…")
        if state in ("SUCCEEDED", "FAILED", "CANCELED"):
            break

    if status.get("status") != "SUCCEEDED":
        raise RuntimeError(f"Meshy task {status.get('status')}: "
                           f"{(status.get('task_error') or {}).get('message', 'no detail')}")

    glb = (status.get("model_urls") or {}).get("glb")
    if not glb:
        raise RuntimeError("Meshy returned no glb url")

    with JOB.lock:
        JOB.step = "Downloading mesh…"
    size = _download(glb, output)
    JOB.note(f"mesh: {output.name} ({size/1048576:.1f} MB)")

    # PBR maps land beside the mesh so Blender/Godot can find them.
    maps = 0
    tex_dir = output.with_name(output.stem + "_textures")
    for i, tex in enumerate(status.get("texture_urls") or []):
        for kind, url in (tex or {}).items():
            if not url:
                continue
            suffix = f"_{i}" if i else ""
            try:
                _download(url, tex_dir / f"{output.stem}{suffix}_{kind}.png")
                maps += 1
            except Exception as exc:            # a missing map must not fail the job
                JOB.note(f"texture {kind} failed: {exc}")
    if maps:
        JOB.note(f"textures: {maps} map(s) -> {tex_dir.name}/")

    with JOB.lock:
        JOB.result = {
            "ok": True,
            "backend": "meshy",
            "task_id": task_id,
            "consumed_credits": status.get("consumed_credits"),
            "texture_maps": maps,
        }


def check_views(images: list[Path]) -> dict:
    """
    Do these reference views agree with each other?

    Independently generated views often disagree on the subject's size, and the
    reconstructor smears detail where they conflict. Surfaced in the UI before
    a generation is paid for. Uses Art Forge's Python when Modly is absent.
    """
    if not CHECK_VIEWS.exists() or len(images) < 2:
        return {"ok": True, "issues": []}
    try:
        r = subprocess.run(
            [helper_python(), str(CHECK_VIEWS), "--json", *[str(p) for p in images]],
            capture_output=True, text=True, timeout=120,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        return json.loads(r.stdout.strip() or '{"ok": true, "issues": []}')
    except Exception as exc:
        return {"ok": True, "issues": [], "error": str(exc)}


def run_meshy_job(images: list[Path], output: Path, opts: dict) -> None:
    """Wraps run_meshy so the job state ends up in the same shape as the local path."""
    try:
        run_meshy(images, output, opts)
    except Exception as exc:
        with JOB.lock:
            if JOB.status != "cancelled":
                JOB.status = "error"
                JOB.error = str(exc)
                JOB.finished_at = time.time()
        return

    with JOB.lock:
        if JOB.status == "cancelled":
            return
        JOB.status = "done"
        JOB.progress = 100
        JOB.step = "Done"
        JOB.finished_at = time.time()

    stats = mesh_stats(output)
    if stats:
        with JOB.lock:
            JOB.result = {**(JOB.result or {}), "mesh": stats}


def mesh_stats(path: Path) -> dict | None:
    """Read basic GLB/GLTF statistics without Modly or third-party packages."""
    if not path.exists():
        return None
    try:
        if path.suffix.lower() == ".gltf":
            document = json.loads(path.read_text(encoding="utf-8"))
        else:
            with path.open("rb") as fh:
                magic, version, _ = struct.unpack("<4sII", fh.read(12))
                if magic != b"glTF" or version != 2:
                    return None
                document = None
                while header := fh.read(8):
                    length, kind = struct.unpack("<II", header)
                    payload = fh.read(length)
                    if kind == 0x4E4F534A:  # JSON
                        document = json.loads(payload.decode("utf-8").rstrip("\x00 \t\r\n"))
                        break
                if document is None:
                    return None

        accessors = document.get("accessors") or []
        primitives = [
            primitive
            for mesh in (document.get("meshes") or [])
            for primitive in (mesh.get("primitives") or [])
        ]
        vertices = 0
        faces = 0
        for primitive in primitives:
            position = (primitive.get("attributes") or {}).get("POSITION")
            if position is None or position >= len(accessors):
                continue
            vertex_count = int(accessors[position].get("count") or 0)
            vertices += vertex_count
            index = primitive.get("indices")
            element_count = (
                int(accessors[index].get("count") or 0)
                if index is not None and index < len(accessors)
                else vertex_count
            )
            mode = int(primitive.get("mode", 4))
            if mode == 4:       # TRIANGLES
                faces += element_count // 3
            elif mode in (5, 6):  # TRIANGLE_STRIP / TRIANGLE_FAN
                faces += max(0, element_count - 2)

        return {
            "vertices": vertices,
            "faces": faces,
            "watertight": None,
            "meshes": len(document.get("meshes") or []),
            "primitives": len(primitives),
            "size_mb": round(path.stat().st_size / (1024 * 1024), 2),
        }
    except Exception:
        return None


def cancel_job() -> None:
    with JOB.lock:
        run_id, proc = JOB.run_id, JOB.proc
        if JOB.status != "running":
            return
        JOB.status = "cancelled"
        JOB.step = "Cancelled"
        JOB.finished_at = time.time()
    if run_id:
        try:
            subprocess.run(
                [python312(), str(CLI), "workflow-run", "cancel", run_id],
                capture_output=True, timeout=30,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
        except Exception:
            pass
    if proc and proc.poll() is None:
        try:
            proc.terminate()
        except Exception:
            pass


# --------------------------------------------------------------------------- #
# Folder browsing
# --------------------------------------------------------------------------- #


def count_images(folder: Path) -> int:
    try:
        return sum(1 for p in folder.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTS)
    except OSError:
        return 0


def scan(folder: Path) -> dict:
    if not folder.exists() or not folder.is_dir():
        return {"ok": False, "error": f"Not a folder: {folder}"}

    subdirs, images, meshes, assemblies = [], [], [], []
    try:
        entries = sorted(folder.iterdir(), key=lambda p: p.name.lower())
    except OSError as exc:
        return {"ok": False, "error": str(exc)}

    for p in entries:
        if p.is_dir():
            if not p.name.startswith("."):
                subdirs.append({"name": p.name, "path": str(p), "images": count_images(p)})
        elif p.suffix.lower() in IMAGE_EXTS:
            images.append({"name": p.name, "path": str(p), "size": p.stat().st_size})
        elif p.suffix.lower() in MESH_EXTS:
            meshes.append({"name": p.name, "path": str(p), "size": p.stat().st_size})
        elif p.name.lower().endswith(ASSEMBLY_SUFFIX):
            summary = {"name": p.name, "path": str(p), "size": p.stat().st_size,
                       "title": p.name.removesuffix(ASSEMBLY_SUFFIX), "instances": None}
            try:
                document = json.loads(p.read_text(encoding="utf-8"))
                summary["title"] = document.get("name") or summary["title"]
                summary["instances"] = len(document.get("instances") or [])
            except Exception:
                pass
            assemblies.append(summary)

    parent = str(folder.parent) if folder.parent != folder else None
    return {"ok": True, "path": str(folder), "parent": parent,
            "subdirs": subdirs, "images": images, "meshes": meshes,
            "assemblies": assemblies}


def _inside_art_root(path: Path) -> Path:
    resolved = path.resolve()
    resolved.relative_to(ART_ROOT.resolve())
    return resolved


def assembly_document(path: Path) -> dict:
    """Load and validate an Art Forge assembly, adding resolved model paths for the UI."""
    path = _inside_art_root(path)
    if not path.is_file() or not path.name.lower().endswith(ASSEMBLY_SUFFIX):
        raise ValueError("Not an Art Forge .assembly.json file")
    document = json.loads(path.read_text(encoding="utf-8"))
    if document.get("schema") != "art-forge-assembly-v1":
        raise ValueError("Unsupported assembly schema")
    assets = document.get("assets")
    instances = document.get("instances")
    if not isinstance(assets, dict) or not isinstance(instances, list):
        raise ValueError("Assembly needs assets and instances")
    if len(instances) > 500:
        raise ValueError("Assembly exceeds the 500-instance preview limit")

    missing = []
    for asset_id, asset in assets.items():
        if not isinstance(asset, dict) or not asset.get("path"):
            raise ValueError(f"Asset {asset_id!r} has no path")
        source = Path(asset["path"])
        if not source.is_absolute():
            source = ART_ROOT / source
        try:
            source = _inside_art_root(source)
        except ValueError as exc:
            raise ValueError(f"Asset {asset_id!r} points outside the art repository") from exc
        if source.suffix.lower() not in MESH_EXTS:
            raise ValueError(f"Asset {asset_id!r} is not a GLB/GLTF model")
        asset["_resolved_path"] = str(source)
        if not source.is_file():
            missing.append(asset_id)

    for instance in instances:
        if not isinstance(instance, dict) or instance.get("asset") not in assets:
            raise ValueError("Every instance must reference a defined asset")
        for field in ("position", "rotation"):
            value = instance.get(field, [0, 0, 0])
            if not isinstance(value, list) or len(value) != 3:
                raise ValueError(f"Instance {instance.get('id', '?')} has an invalid {field}")
    return {"document": document, "missing_assets": missing}


def save_assembly(path: Path, document: dict) -> None:
    """Persist editable transforms while keeping server-only resolved paths out of the file."""
    path = _inside_art_root(path)
    if not path.name.lower().endswith(ASSEMBLY_SUFFIX):
        raise ValueError("Assembly filename must end with .assembly.json")
    clean = json.loads(json.dumps(document))
    for asset in (clean.get("assets") or {}).values():
        if isinstance(asset, dict):
            asset.pop("_resolved_path", None)
    if clean.get("schema") != "art-forge-assembly-v1":
        raise ValueError("Unsupported assembly schema")
    if not isinstance(clean.get("assets"), dict) or not isinstance(clean.get("instances"), list):
        raise ValueError("Assembly needs assets and instances")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(clean, indent=2) + "\n", encoding="utf-8")


def save_assembly_review_capture(path: Path, view: str, data_url: str,
                                 selected_instance: str | None = None) -> dict:
    """Save one deterministic viewer capture beside its assembly scene."""
    path = _inside_art_root(path)
    if not path.is_file() or not path.name.lower().endswith(ASSEMBLY_SUFFIX):
        raise ValueError("Not an Art Forge .assembly.json file")
    safe_view = "".join(c for c in (view or "view").lower() if c.isalnum() or c in "-_")
    if not safe_view:
        raise ValueError("Capture view needs a name")
    prefix = "data:image/png;base64,"
    if not isinstance(data_url, str) or not data_url.startswith(prefix):
        raise ValueError("Capture must be a PNG data URL")
    encoded = data_url[len(prefix):]
    if len(encoded) > 28_000_000:
        raise ValueError("Capture exceeds the 20 MB limit")
    try:
        png = base64.b64decode(encoded, validate=True)
    except Exception as exc:
        raise ValueError("Capture contains invalid base64") from exc
    if not png.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("Capture is not a valid PNG")

    scene_name = path.name[:-len(ASSEMBLY_SUFFIX)]
    review_dir = path.with_name(f"{scene_name}_review")
    review_dir.mkdir(parents=True, exist_ok=True)
    capture_path = review_dir / f"{safe_view}.png"
    capture_path.write_bytes(png)

    manifest_path = review_dir / "review-manifest.json"
    manifest = {}
    if manifest_path.is_file():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception:
            manifest = {}
    captures = manifest.setdefault("captures", {})
    captures[safe_view] = {
        "file": capture_path.name,
        "selected_instance": selected_instance,
        "updated": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }
    manifest["schema"] = "art-forge-assembly-review-v1"
    manifest["assembly"] = path.name
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return {"path": str(capture_path), "relative_path": str(capture_path.relative_to(ART_ROOT))}


def gallery(root: Path, limit: int = 400) -> dict:
    """
    Every asset under a subtree, with its images — the review pass over a whole
    concept sweep, instead of opening 49 folders one at a time.

    An "asset" is any directory that directly contains images; its name is the
    asset ID under the Concepts/References naming convention.
    """
    if not root.exists() or not root.is_dir():
        return {"ok": False, "error": f"Not a folder: {root}"}

    assets, total = [], 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
        imgs = sorted(f for f in filenames if Path(f).suffix.lower() in IMAGE_EXTS)
        if not imgs:
            continue
        here = Path(dirpath)
        assets.append({
            "asset": here.name,
            "path": str(here),
            "group": str(here.parent.relative_to(root)) if here != root else "",
            "images": [{"name": n, "path": str(here / n)} for n in imgs],
        })
        total += len(imgs)
        if total >= limit:
            break

    return {"ok": True, "root": str(root), "assets": assets,
            "count": total, "truncated": total >= limit}


def pick_folder(start: str) -> str | None:
    """Native folder dialog, run out-of-process so tkinter never fights our server."""
    code = (
        "import tkinter as tk, sys\n"
        "from tkinter import filedialog\n"
        "r = tk.Tk(); r.withdraw(); r.attributes('-topmost', True)\n"
        "p = filedialog.askdirectory(title='Choose a reference folder', initialdir=sys.argv[1])\n"
        "print(p or '')\n"
    )
    try:
        out = subprocess.run(
            [python312(), "-c", code, start],
            capture_output=True, text=True, timeout=300,
        )
        picked = out.stdout.strip()
        return picked or None
    except Exception:
        return None


def reveal(path: Path) -> None:
    try:
        if path.is_dir():
            subprocess.Popen(["explorer", str(path)])
        else:
            subprocess.Popen(["explorer", "/select,", str(path)])
    except Exception:
        pass


# --------------------------------------------------------------------------- #
# HTTP layer
# --------------------------------------------------------------------------- #


class Handler(BaseHTTPRequestHandler):
    server_version = "ArtForge/1.0"

    def log_message(self, fmt: str, *args) -> None:  # keep the console clean
        pass

    # -- helpers ----------------------------------------------------------- #

    def send_json(self, obj: dict, code: int = 200) -> None:
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def read_json(self) -> dict:
        length = int(self.headers.get("Content-Length") or 0)
        if not length:
            return {}
        try:
            return json.loads(self.rfile.read(length).decode("utf-8"))
        except json.JSONDecodeError:
            return {}

    # -- routes ------------------------------------------------------------ #

    def do_GET(self) -> None:
        url = urlparse(self.path)
        q = parse_qs(url.query)
        route = url.path

        if route in ("/", "/index.html"):
            page = HERE / "index.html"
            body = page.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if route == "/api/state":
            available = local_available()
            up = backend_up() if available else False
            self.send_json({
                "backend": up,
                "local_available": available,
                "model": model_state() if up else {},
                "art_root": str(ART_ROOT),
                "app_version": APP_VERSION,
                "model_id": MODEL_ID,
                "meshy_key": bool(meshy_key()),
                "meshy_max_images": MESHY_MAX_IMAGES,
                "job": JOB.snapshot(),
            })
            return

        if route == "/api/scan":
            target = q.get("path", [str(ART_ROOT)])[0]
            self.send_json(scan(Path(target)))
            return

        if route == "/api/gallery":
            target = q.get("path", [str(ART_ROOT / "Concepts")])[0]
            self.send_json(gallery(Path(target)))
            return

        if route == "/api/assembly":
            target = q.get("path", [""])[0]
            try:
                loaded = assembly_document(Path(target))
                self.send_json({"ok": True, "path": str(Path(target).resolve()), **loaded})
            except Exception as exc:
                self.send_json({"ok": False, "error": str(exc)}, 400)
            return

        if route == "/api/thumb":
            target = Path(q.get("path", [""])[0])
            if not target.is_file() or target.suffix.lower() not in IMAGE_EXTS:
                self.send_json({"ok": False}, 404)
                return
            ctype = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
            data = target.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "max-age=300")
            self.end_headers()
            self.wfile.write(data)
            return

        if route == "/api/mesh":
            target = Path(q.get("path", [""])[0])
            if not target.is_file() or target.suffix.lower() not in MESH_EXTS:
                self.send_json({"ok": False, "error": "not a mesh"}, 404)
                return
            self.send_file(target, "model/gltf-binary")
            return

        if route.startswith("/vendor/"):
            rel = route[len("/vendor/"):]
            target = (VENDOR / rel).resolve()
            try:
                target.relative_to(VENDOR.resolve())      # no traversal outside vendor/
            except ValueError:
                self.send_json({"ok": False}, 403)
                return
            if not target.is_file():
                self.send_json({"ok": False, "error": f"missing {rel}"}, 404)
                return
            self.send_file(target, "text/javascript")
            return

        if route == "/api/progress":
            self.send_json(JOB.snapshot())
            return

        self.send_json({"ok": False, "error": "not found"}, 404)

    def send_file(self, path: Path, ctype: str) -> None:
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "max-age=300")
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self) -> None:
        route = urlparse(self.path).path
        body = self.read_json()

        if route == "/api/backend/start":
            ok, msg = start_backend()
            self.send_json({"ok": ok, "message": msg})
            return

        if route == "/api/browse":
            picked = pick_folder(body.get("start") or str(ART_ROOT))
            self.send_json({"ok": bool(picked), "path": picked})
            return

        if route == "/api/reveal":
            reveal(Path(body.get("path") or str(ART_ROOT)))
            self.send_json({"ok": True})
            return

        if route == "/api/cancel":
            cancel_job()
            self.send_json({"ok": True})
            return

        if route == "/api/check-views":
            images = [Path(p) for p in (body.get("images") or []) if Path(p).is_file()]
            self.send_json(check_views(images))
            return

        if route == "/api/assembly/save":
            try:
                save_assembly(Path(body.get("path") or ""), body.get("document") or {})
                self.send_json({"ok": True})
            except Exception as exc:
                self.send_json({"ok": False, "error": str(exc)}, 400)
            return

        if route == "/api/assembly/review-capture":
            try:
                result = save_assembly_review_capture(
                    Path(body.get("path") or ""),
                    str(body.get("view") or ""),
                    str(body.get("data_url") or ""),
                    body.get("selected_instance"),
                )
                self.send_json({"ok": True, **result})
            except Exception as exc:
                self.send_json({"ok": False, "error": str(exc)}, 400)
            return

        if route == "/api/generate":
            with JOB.lock:
                if JOB.status == "running":
                    self.send_json({"ok": False, "error": "A generation is already running."}, 409)
                    return

            backend = body.get("backend") or "local"

            raw = body.get("images") or ([body["image"]] if body.get("image") else [])
            images = [Path(p) for p in raw]
            missing = [str(p) for p in images if not p.is_file()]
            if not images or missing:
                self.send_json({"ok": False,
                                "error": f"Image not found: {missing or '(none selected)'}"}, 400)
                return
            image = images[0]

            out_dir = Path(body.get("out_dir") or image.parent)
            name = (body.get("name") or image.stem).strip() or image.stem
            if not name.lower().endswith(".glb"):
                name += ".glb"
            output = out_dir / name

            if backend == "meshy":
                if not meshy_key():
                    self.send_json({"ok": False, "error":
                                    "No Meshy API key. Set MESHY_API_KEY or create "
                                    f"{MESHY_KEY_FILE.name} next to forge.py."}, 400)
                    return
                opts = {
                    "texture":            bool(body.get("texture", True)),
                    "pbr":                bool(body.get("pbr", True)),
                    "texture_resolution": body.get("texture_resolution") or "2k",
                    "remesh":             bool(body.get("remesh", False)),
                    "topology":           body.get("topology") or "quad",
                    "polycount":          int(body.get("polycount") or 30000),
                    "texture_prompt":     body.get("texture_prompt") or "",
                }
                target = run_meshy_job
                args = (images, output, opts)
            else:
                if not local_available():
                    self.send_json({"ok": False, "error":
                                    "Local generation requires Modly, which is not installed. "
                                    "Choose Meshy instead; browsing and the 3D viewer remain available."},
                                   400)
                    return
                steps = int(body.get("steps") or 30)
                octree = int(body.get("octree") or 380)
                remesh = body.get("remesh") or "none"
                seed_raw = body.get("seed")
                seed = int(seed_raw) if str(seed_raw).strip() not in ("", "None", "null") else None

                if not backend_up():
                    ok, msg = start_backend()
                    if not ok:
                        self.send_json({"ok": False, "error": msg}, 503)
                        return
                target = run_generation
                args = (image, output, steps, octree, remesh, seed)

            JOB.reset()
            with JOB.lock:
                JOB.status = "running"
                JOB.step = "Starting..."
                JOB.started_at = time.time()
                JOB.image = str(image)
                JOB.output = str(output)

            threading.Thread(target=target, args=args, daemon=True).start()
            self.send_json({"ok": True, "output": str(output), "backend": backend})
            return

        self.send_json({"ok": False, "error": "not found"}, 404)


def main() -> int:
    if port_busy(FORGE_PORT):
        url = f"http://127.0.0.1:{FORGE_PORT}/"
        print(f"[forge] Already running at {url}")
        if not os.environ.get("FORGE_NO_BROWSER"):
            webbrowser.open(url)
        return 0

    server = ThreadingHTTPServer(("127.0.0.1", FORGE_PORT), Handler)
    url = f"http://127.0.0.1:{FORGE_PORT}/"
    print("  Art Forge")
    print("  =========")
    print(f"  UI        : {url}")
    print(f"  Art root  : {ART_ROOT}")
    if local_available():
        print(f"  Local gen : available via {MODLY_API}")
    else:
        print("  Local gen : unavailable (Modly not installed; viewer and Meshy still work)")
    print("\n  Close this window to stop the tool.\n")
    if not os.environ.get("FORGE_NO_BROWSER"):
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[forge] stopped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
