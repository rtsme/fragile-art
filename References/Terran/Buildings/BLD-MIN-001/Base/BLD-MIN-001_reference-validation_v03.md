# BLD-MIN-001 textured base reference validation — v03

Date: 2026-08-31
Source design: `../../../../../Concepts/Terran/Buildings/BLD-MIN-001/Base/BLD-MIN-001_base-concept_v02.png`
Status: **alignment gate passed; reference package approved for body-only 3D submission**

## Approved package

`BLD-MIN-001_base_reference-sheet_v12.png` is the active textured turnaround. Its divider-safe
production crops are:

- `BLD-MIN-001_base_front_v12.png`
- `BLD-MIN-001_base_back_v12.png`
- `BLD-MIN-001_base_left_v12.png`
- `BLD-MIN-001_base_right_v12.png`

| View | Canvas | Silhouette | Centre |
|---|---:|---:|---:|
| front | 624 × 624 | 530 × 184 | 0.501, 0.512 |
| back | 624 × 624 | 533 × 184 | 0.490, 0.512 |
| left | 624 × 624 | 392 × 185 | 0.496, 0.511 |
| right | 624 × 624 | 389 × 183 | 0.484, 0.510 |

The package has 1.1% all-view silhouette-height variation, 0.6% front/back width variation, 0.8%
left/right width variation, 1.7% horizontal-centre drift and 0.24% vertical-centre drift. These are
all within the preferred 3% scale and 2% centring tolerances. The validator reports no issues.

## Revision audit

| Revision | Height variation | Vertical-centre drift | Result |
|---|---:|---:|---|
| v08 | 4.4% | 7.6% | rejected; side views moved upward |
| v09 | 7.1% | 0.6% | rejected; side views over-enlarged |
| v10 | 6.5% | 1.4% | rejected; side views over-shrunk |
| v11 | 8.9% | 1.3% | rejected; size correction overshot |
| v12 | 1.1% | 0.24% | approved; deterministic uniform scale and translation only |

v12 uses the accepted v06 pixels. Front and back are unchanged. Left and right were uniformly
scaled and translated without repainting by `tools/align-reference-views.py`, then assembled into
the divider-preserving 2 × 2 sheet. This corrects camera scale and framing without introducing new
geometry or texture drift.
