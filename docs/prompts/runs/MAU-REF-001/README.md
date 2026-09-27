# MAU-REF-001 — Mauna orthographic reference sets (buildings)

Four-view reference sets for all 45 Mauna buildings, generated from the **approved low-detail**
concepts (not the dressed concepts) and validated with `tools/check-views.py`.

```text
References/Mauna/Buildings/<MAU-BLD-…>/LowDetail/
  <asset>_low-detail_reference-sheet_v01.png   generated 2x2 sheet
  <asset>_low-detail_reference-sheet_v02.png   only when the sheet came back an odd pixel size
  <asset>_low-detail_{front,back,left,right}_v03.png   mechanical crops, dividers excluded
  <asset>_low-detail_{front,back,left,right}_v04.png   normalised, and the set that passes the checker
  <asset>_low-detail_reference-sheet_v04.png   rebuilt sheet for review
```

**v04 is the deliverable.** Meshy input order stays front, back, left, right.

- `make_prompts.py` writes one sheet prompt per building.
- `process_sheet.py <asset>` crops, normalises and validates one asset; exits non-zero unless the
  checker reports the views mutually consistent.
- `wait_and_run.sh` drives the batch and retries through usage-limit stops.

## Three faults this stage exposed

1. **Divider pixels.** Cropping without `--center-gutter-px` leaves the sheet's divider lines inside
   the tiles. Everything downstream then measures 3px out, and `align-reference-views.py`
   mis-measured one view by a third before this was found.
2. **Uneven view scale.** The generator reliably draws the side views taller than front and back —
   14.9% on the anchor, 11.0% on the landing pad — which fails the checker outright.
   `normalize-reference-views.py` repairs it deterministically (uniform scale and translation, no
   repainting). **Normalise DOWN to the smallest view height**: scaling up pushes a wide subject into
   the tile edge, and both tools discard any silhouette touching the border, which silently wipes the
   view. That was the Landing Pad failure.
3. **Odd sheet dimensions.** Some sheets come back with an odd width or height (1374x1145), which the
   crop tool rejects. `process_sheet.py` trims one row/column first.

## Run log

**2026-09-27, run 1 (2 parallel, 10 attempts across usage-limit windows).** 39 of 44 validated on the
batch; the remaining five failed on faults 2 and 3 above and passed once the script was fixed. With
the anchor, **all 45 buildings now have a validated four-view set**.

Spot-checked visually (DEF-001, LOG-001, MIN-003, CMD-001): same object in every tile, asymmetry
flips correctly between front and back, true orthographic, matched scale and centring.

## Not done here

Ships. Spacecraft project each world dimension onto a different image axis, and the repo validates
them with `tools/check-ship-views.py` (top, bottom, left, rear) rather than `check-views.py`. The
Terran ship reference sets under `References/Terran/Ships/` should be read before generating the
Mauna ones.
