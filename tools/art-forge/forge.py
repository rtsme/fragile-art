"""
Art Forge - a small local UI for turning 2D concept art into 3D meshes.

Point it at a folder of reference images, pick one, press Forge. It drives the
Modly backend (FastAPI on 127.0.0.1:8765) through Modly's own CLI, so the
generation path is exactly the one Modly uses itself.

Stdlib only - run with Python 3.12:  py -3.12 forge.py
"""
from __future__ import annotations

import json
import mimetypes
import os
import shutil
import socket
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

MODLY_DIR = Path(os.environ.get("MODLY_DIR", r"C:\Users\major\Documents\Projects\modly"))
MODLY_DATA = Path(os.environ.get("MODLY_DATA", r"C:\Users\major\modly-data"))
MODLY_API = os.environ.get("MODLY_API_URL", "http://127.0.0.1:8765")

# The art repo root — Concepts/, References/ and Models/ sit directly under it.
ART_ROOT = Path(os.environ.get("ART_ROOT", HERE.parent.parent))
MODEL_ID = os.environ.get("MODLY_MODEL_ID", "hunyuan3d-mini/generate")

FORGE_PORT = int(os.environ.get("FORGE_PORT", "8770"))

CHECK_VIEWS = HERE.parent / "check-views.py"

CLI = MODLY_DIR / "tools" / "modly-cli" / "agent.py"
API_DIR = MODLY_DIR / "api"
API_PY = API_DIR / ".venv" / "Scripts" / "python.exe"

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
MESH_EXTS = {".glb", ".gltf"}
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
    if backend_up():
        return True, "already running"
    if not API_PY.exists():
        return False, f"Modly api venv missing: {API_PY}"

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
    if not API_PY.exists():
        return path
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
            [str(API_PY), "-c", snippet, str(path), str(dst), str(max_px)],
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
    a generation is paid for. Needs Pillow, so it runs in Modly's api venv.
    """
    if not API_PY.exists() or not CHECK_VIEWS.exists() or len(images) < 2:
        return {"ok": True, "issues": []}
    try:
        r = subprocess.run(
            [str(API_PY), str(CHECK_VIEWS), "--json", *[str(p) for p in images]],
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
    """Face/vertex counts, read with Modly's api venv (it already has trimesh)."""
    if not API_PY.exists() or not path.exists():
        return None
    snippet = (
        "import json,sys,trimesh;"
        "s=trimesh.load(sys.argv[1]);"
        "m=s.to_mesh() if hasattr(s,'to_mesh') else s;"
        "print(json.dumps({'vertices':len(m.vertices),'faces':len(m.faces),"
        "'watertight':bool(m.is_watertight)}))"
    )
    try:
        out = subprocess.run(
            [str(API_PY), "-c", snippet, str(path)],
            capture_output=True, text=True, timeout=180,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        data = json.loads(out.stdout.strip())
        data["size_mb"] = round(path.stat().st_size / (1024 * 1024), 2)
        return data
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

    subdirs, images, meshes = [], [], []
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

    parent = str(folder.parent) if folder.parent != folder else None
    return {"ok": True, "path": str(folder), "parent": parent,
            "subdirs": subdirs, "images": images, "meshes": meshes}


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
            up = backend_up()
            self.send_json({
                "backend": up,
                "model": model_state() if up else {},
                "art_root": str(ART_ROOT),
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
    if not CLI.exists():
        print(f"[forge] Modly CLI not found at {CLI}")
        print("[forge] Set MODLY_DIR to your modly checkout.")
        return 1

    if port_busy(FORGE_PORT):
        url = f"http://127.0.0.1:{FORGE_PORT}/"
        print(f"[forge] Already running at {url}")
        webbrowser.open(url)
        return 0

    server = ThreadingHTTPServer(("127.0.0.1", FORGE_PORT), Handler)
    url = f"http://127.0.0.1:{FORGE_PORT}/"
    print("  Art Forge")
    print("  =========")
    print(f"  UI        : {url}")
    print(f"  Art root  : {ART_ROOT}")
    print(f"  Modly API : {MODLY_API}")
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
