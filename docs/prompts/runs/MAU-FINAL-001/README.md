# MAU-FINAL-001 — remaining Mauna ships and two building fixes

Six jobs: the four ships with no concept yet (MAU-SHP-002 Assault Fighter, 004 Combat Eagle,
005 Terminator, 006 Command Cruiser) and v02 fixes for the two buildings that broke the style
or the 3D rules.

- `jobs.tsv`: id, prompt file, target image, reference-1 image. Reference 2 is always the emblem.
  Ships reference the approved Fleet Battleship for materials only; the fixes reference their own v01.
- `run_batch`-equivalent logic lives in `wait_and_run.sh`, which waits out a usage-limit reset and
  retries until every target exists. Targets that already exist are skipped.

**Ship proportions.** MAU-SHP-002 uses the measured Terran assault-fighter proportions
(1 : 0.80 : 0.26). MAU-SHP-004, 005 and 006 have **no generated Terran model to measure**, so their
proportions are set by role (raider, gunship, flagship) against the in-game hull sizes 0.90, 1.00 and
1.10 world units. Replace them with measured values if a Terran model for those hulls ever exists.

**The two fixes.** LOG-002 v02 removes the red diagonal hazard stripes (a prohibited Terran motif that
the v01 prompt did not explicitly forbid). LOG-003 v02 closes the open repair bay with a flush
segmented hangar door, so the silhouette is closed (concept rule A6). Both keep everything else.

## Run log

**2026-09-22 15:0x, run 1 (2 parallel).** MAU-SHP-002 and MAU-SHP-004 saved; the other four hit the
Codex usage limit (resets 19:02). Both saved ships hold the approved look, keep engines built into the
hull rather than on pylons, and carry the crescent emblem. `wait_and_run.sh` is waiting out the reset.

**2026-09-22 19:05, run 2 (watcher, 2 parallel).** All four remaining jobs saved by 19:09:
MAU-SHP-005, MAU-SHP-006, LOG-002 v02 and LOG-003 v02. **The Mauna set is now complete: 45 buildings
and 7 ships.**

Review: both fixes worked — LOG-002 v02 has no hazard striping (plain worn plating, one small emblem)
and LOG-003 v02 closes the repair bay with a flush segmented door, so the silhouette is solid. The
Terminator reads as a heavy armoured hull, though its spinal weapon is subtler than the prompt asked
for. One note for cleanup: the Command Cruiser carries a thin twin-barrel turret at the bow, which is
the kind of thin element rule A5 warns about; everything else on both ships is solid.
