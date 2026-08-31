"""Run Art Forge's Meshy backend without opening the UI.

The first image is always the front view. Authentication is read by forge.py from
MESHY_API_KEY or the gitignored tools/art-forge/meshy.key file.
"""

from __future__ import annotations

import argparse
import json
import threading
import time
from pathlib import Path

import forge


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("images", nargs="+", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--texture-resolution", default="4k", choices=("1k", "2k", "4k"))
    parser.add_argument("--remesh", action="store_true")
    parser.add_argument("--topology", default="quad")
    parser.add_argument("--polycount", type=int, default=30000)
    parser.add_argument("--texture-prompt", default="")
    args = parser.parse_args()

    missing = [str(path) for path in args.images if not path.is_file()]
    if missing:
        parser.error("missing input images: " + ", ".join(missing))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    forge.JOB.reset()
    forge.JOB.status = "running"
    forge.JOB.started_at = time.time()
    forge.JOB.output = str(args.output)

    original_note = forge.JOB.note

    def note(line: str) -> None:
        print(line, flush=True)
        original_note(line)

    forge.JOB.note = note
    stopped = threading.Event()

    def monitor() -> None:
        while not stopped.wait(15):
            snapshot = forge.JOB.snapshot()
            print(
                f"progress={snapshot['progress']}% step={snapshot['step']} "
                f"elapsed={snapshot['elapsed']}s",
                flush=True,
            )

    thread = threading.Thread(target=monitor, daemon=True)
    thread.start()
    try:
        forge.run_meshy(
            args.images,
            args.output,
            {
                "texture": True,
                "pbr": True,
                "texture_resolution": args.texture_resolution,
                "remesh": args.remesh,
                "topology": args.topology,
                "polycount": args.polycount,
                "texture_prompt": args.texture_prompt,
            },
        )
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), flush=True)
        return 1
    finally:
        stopped.set()

    print(json.dumps(forge.JOB.result or {"ok": True}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
