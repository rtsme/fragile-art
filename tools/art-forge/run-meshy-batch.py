"""Run a manifest of independent Meshy multi-image jobs with bounded concurrency."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


def run_one(root: Path, job: dict, settings: dict) -> dict:
    input_dir = root / job["input_dir"]
    prefix = job.get("input_prefix", job["id"])
    images = [input_dir / f'{prefix}_{view}_v01.png' for view in ("front", "back", "left", "right")]
    output = root / job["output"]
    cli = Path(__file__).with_name("run-meshy-cli.py")
    cmd = [sys.executable, str(cli), *map(str, images), "--output", str(output),
           "--texture-resolution", settings.get("texture_resolution", "4k"),
           "--texture-prompt", job.get("texture_prompt", "")]
    if settings.get("remesh"):
        cmd += ["--remesh", "--topology", settings.get("topology", "quad"),
                "--polycount", str(settings.get("polycount", 30000))]
    print(f"[{job['id']}] starting", flush=True)
    proc = subprocess.run(cmd, cwd=root, text=True, capture_output=True, env=os.environ.copy())
    if proc.stdout:
        for line in proc.stdout.splitlines():
            print(f"[{job['id']}] {line}", flush=True)
    if proc.stderr:
        for line in proc.stderr.splitlines():
            print(f"[{job['id']}] STDERR {line}", flush=True)
    return {"id": job["id"], "kind": job.get("kind"), "output": job["output"],
            "returncode": proc.returncode, "ok": proc.returncode == 0}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    settings = manifest.get("settings", {})
    jobs = manifest.get("jobs", [])
    results = []
    with ThreadPoolExecutor(max_workers=int(settings.get("max_concurrency", 2))) as pool:
        futures = [pool.submit(run_one, root, job, settings) for job in jobs]
        for future in as_completed(futures):
            results.append(future.result())
    results.sort(key=lambda item: item["id"])
    print(json.dumps({"ok": all(item["ok"] for item in results), "results": results}, indent=2), flush=True)
    return 0 if all(item["ok"] for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
