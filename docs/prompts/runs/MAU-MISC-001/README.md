# MAU-MISC-001 — Mauna missiles, satellites, environment and prop kits

17 assets: MIS-ORD-001–003, SAT-ORB-001–003, ENV-INF-001–002, PRP-IND-001–007 and PRP-CON-001–002.
`make_prompts.py` writes one prompt per asset plus `jobs.tsv`; `wait_and_run.sh` runs them with three
references each (an approved Mauna asset for materials, the emblem, and the Terran equivalent for
function only) and retries after a usage-limit stop.

Kits are the hard case for `concept-rules-for-3d.md`, so each prompt names its solid-form equivalent:
conveyors are closed boxes, pipes enclosed trunks, the crane kit is tower and boom housings with no
lattice or cables, and the scaffolding kit is stepped blocks and plate stacks.

## Run log

**2026-09-22 20:19, run 1 (2 parallel).** All 17 saved by 20:34, no limit stop.

Review: every asset holds the approved look, and the kits came back as solid closed volumes — the
rules held even for cranes and scaffolding. Four deviations:

| Asset | Deviation | Action |
|---|---|---|
| ENV-INF-001 | dark vignette background, plus red/white striping on some blocks | v02 re-roll |
| PRP-IND-006 | dark vignette background, labels hard to read | v02 re-roll |
| PRP-IND-004 | added a title and tagline in the sheet | recorded only |
| PRP-IND-007 | added a title line | recorded only |

The background matters because the pipeline's reference and background-removal steps expect a plain
flat light-grey field; a vignette would corrupt them. The added titles are cosmetic.

**2026-09-22 20:36, re-rolls.** ENV-INF-001 v02 saved and fixes both faults: one flat light-grey field
edge to edge, no hazard striping, legible labels, one emblem on the large plinth. PRP-IND-006 v02 hit
the usage limit (resets 2026-09-23 00:05) and is queued; its v01 stays usable for reference but should
not go to the reference stage while the background is a vignette.
