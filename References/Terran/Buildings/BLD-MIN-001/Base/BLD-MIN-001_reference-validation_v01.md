# BLD-MIN-001 base reference validation — v01

Date: 2026-08-31
Source design: `../../../../../Concepts/Terran/Buildings/BLD-MIN-001/Base/BLD-MIN-001_base-concept_v01.png`
Status: **reference gate not passed; Meshy submission blocked**

## Best candidate

`BLD-MIN-001_base_reference-sheet_v04.png` is the most coherent generated turnaround. Its four
divider-safe mechanical crops are:

- `BLD-MIN-001_base_front_v04.png`
- `BLD-MIN-001_base_back_v04.png`
- `BLD-MIN-001_base_left_v04.png`
- `BLD-MIN-001_base_right_v04.png`

Validation output:

| View | Canvas | Silhouette | Centre |
|---|---:|---:|---:|
| front | 624 × 624 | 524 × 181 | 0.501, 0.511 |
| back | 624 × 624 | 526 × 181 | 0.493, 0.511 |
| left | 624 × 624 | 360 × 170 | 0.506, 0.475 |
| right | 624 × 624 | 362 × 170 | 0.488, 0.475 |

Opposing-pair widths are consistent. The package reports 6.1% silhouette-height variation and 3.6%
vertical-centre drift, both above the preferred 3%/2% tolerances but below hard-failure thresholds.
Visual review confirms that the side elevations remain slightly too short and high in their tiles.

## Rejected revisions

- v01: 30.6% height variation.
- v02: 14.3% height variation after border-artifact filtering.
- v03: 5.1% vertical-centre drift after excluding the generated centre divider.
- v05: 10.0% height variation and 5.6% vertical-centre drift.

Rejected revisions are retained only as pipeline-test evidence. Do not submit any revision in this
folder to a paid generator until a replacement reaches the production tolerance or an explicit
exception is recorded.

## Validator finding

The initial v02 run appeared to pass because bright quadrant dividers were interpreted as a
full-canvas silhouette. `tools/check-views.py` now removes border-connected artifacts before
measuring, preventing that false positive. `tools/crop-reference-sheet.py` also supports
`--center-gutter-px` for a purely mechanical divider-safe crop.
