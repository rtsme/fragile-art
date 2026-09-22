# MAU-BLD-001 — Mauna building concept batch (v01)

44 buildings (every Terran building except the Command Centre, whose Mauna equivalent is the approved
Exchange `MAU-BLD-CMD-001`). Backend: Codex CLI `image_generation`, one run per building.

- `make_prompts.py` writes one `<ASSET>_concept_v01.txt` per building plus `jobs.tsv`. Per-building Mauna
  subjects live in its `BUILDINGS` table.
- `run_batch.sh [jobs]` runs the batch and skips any building that already has a v01 PNG, so it is safe
  to re-run.
- Each run attaches three references: the approved Exchange (materials and rendering only), the
  crescent emblem crop, and the building's latest Terran concept (function and footprint only).

## Run log

**2026-09-14, run 1 (4 parallel).** 8 saved: CMD-002, HAB-001–003, LIF-001–004. The other 36 stopped on
`usage_limit_reached` (ChatGPT Plus Codex limit; resets 2026-09-15 03:49 local). No prompt faults.

Review of the 8 saved: Security Centre (CMD-002) is close to a clone of the Exchange, and Medical Centre
(LIF-001) and Environment Control (LIF-003) reuse its dome, pods, dish and tower. The cause was the
reference instruction "match … salvage shape language exactly" plus a style block that demanded a
counterweight and crimson band on every building. The prompt generator was fixed before the resume:
the Exchange is now a material, palette and rendering reference only, its composition is explicitly
excluded, and the emblem is limited to one small stencil. All 44 prompt files were regenerated;
the 8 saved images came from the earlier wording.

**Owner decision 2026-09-14: re-roll the three copies** as v02 (CMD-002, LIF-001, LIF-003). Each v02 prompt
adds an explicit "must NOT look like the Exchange" line naming its dominant form (the `REROLL` table in
`make_prompts.py`). The v01 images and v01 prompt files are kept as record. `jobs.tsv` now carries a
version column, and `run_batch.sh` checks for that version, so the re-rolls run with the resume after the
Codex limit resets.

**Runner fix before the resume.** A dry run with a stand-in `codex` showed all 44 jobs would re-run. Python
on Windows had written `jobs.tsv` with `\r\n`, so the version column read `v01\r` and the "already
exists" check never matched. `make_prompts.py` now writes `\n` and `run_batch.sh` strips any `\r`. The
repeated dry run skips the 5 kept buildings (HAB-001–003, LIF-002, LIF-004) and queues 39: 36 new and
3 v02 re-rolls.

**2026-09-14 23:27, run 2 (owner, 2 parallel).** 0 saved. It was started before the 03:49 reset, and every
job hit the same ChatGPT Plus Codex limit. The runner labelled these FAILED rather than LIMIT, because
Codex printed only the plain-English message and not `usage_limit_reached`. It also carried on through
all 39 jobs. `run_batch.sh` now matches both messages, prints the reset time, and stops the batch at the
first limit hit (exit 255 ends `xargs`).

**2026-09-22, run 3 (2 parallel).** 18 saved, including the three v02 re-rolls (CMD-002, LIF-001,
LIF-003), then the limit stopped the batch cleanly at LOG-002/003 (resets 13:58). 27 of 45 building
concepts now exist. Still to generate: LOG-002–004, DEF-001–008, SEN-001–002, TEC-001–005.

Review: all 18 hold the approved Mauna look and read as distinct buildings — the anti-clone prompt
change worked, and the three re-rolls no longer copy the Exchange (CMD-002 is a low flat-roofed
fortress, LIF-001 a mostly off-white capsule, LIF-003 has no dome). Minor notes for cleanup, not
regeneration: MIN-002's screw drills hang below the plinth line, and PWR-003 uses crimson arrow
marks rather than the emblem.

**2026-09-22 14:02, run 4 (watcher, 2 parallel).** The remaining 18 saved in one window: LOG-002–004,
DEF-001–008, SEN-001–002, TEC-001–005. **All 45 building concepts now exist.** `wait_and_run.sh` waited
out the 13:58 reset and exited at 14:21 once the count was complete.

Review: all 18 hold the approved look and read as their own buildings — cupola turrets on heavy
turntables, a closed-cell anti-missile pod, the split silo hatch with the emblem, the bunker's slit
ports, the thick-bowl sensor dish, the clamped gravity rings, the asteroid engine's huge thrust bell
and the teleport pad in its three pylons. Two deviations for cleanup, not regeneration: LOG-002 carries
red diagonal hazard stripes (a prohibited Terran motif) and LOG-003's repair bay is an open recess
(negative space, rule A6) — both were invited by their own prompt wording.
