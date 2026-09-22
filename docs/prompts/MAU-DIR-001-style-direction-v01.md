# MAU-DIR-001 — Mauna style direction, concept prompts (v01; style approved 2026-09-14)

Backend: Codex CLI 0.153.0 `image_generation` (`codex exec`, one run per asset), 2026-09-14.
Exact prompts as run: `docs/prompts/runs/MAU-DIR-001/*.txt`. See "Generation record" at the end.
Style source: `Concepts/Mauna/mauna-concept-manifest-v01.md` (Faction Styles row, draft).
Blocking sheet: `Concepts/Mauna/Direction/MAU-DIR-001_silhouette-sheet_v01.png`. It shows
silhouette and palette intent only; **do not feed it to a generator**.

Run order: kit sheet → anchor hero → ships. Record every accepted output, revision and correction
pass in this file, following the TER-KIT-001 records.

---

## Shared scan-safety block (append verbatim to every prompt)

> Isolated elevated orthographic-style three-quarter view, complete asset centred on a plain flat
> light-grey background. No ground shadow, no environment, no text, no watermark, no people.
> **Build it to be scanned into 3D. These are hard constraints:** solid enclosed volumes and a
> closed silhouette; no open lattice, truss or scaffold; no wires, cables, ropes, nets, straps,
> chains or thin aerials; no holes or see-through damage; no feature smaller than about 2% of the
> asset's longest dimension; large planes with deep bold breaks, no fine greeble. Patch plates are
> real stepped plates with visible thickness. Windows are flat, opaque, near-black glass with no
> interior, screens or reflections. Matte to satin only; no chrome, gloss or transparency. Flat
> even studio lighting, no rim light, no baked ambient occlusion, **no glowing lights or emissive
> surfaces**. Crimson markings are flat painted stencils, not raised geometry.

## Shared Mauna style block (append verbatim to every prompt)

> Mauna smuggler-salvage faction. Hardware is acquired and rebuilt, not designed from scratch:
> rounded bronze cargo-belly hulls welded to whole angular salvaged sections of off-white foreign
> plating, joined by thick gunmetal clamp collars. Deliberately asymmetric, balanced by a visible
> counterweight mass. Large verdigris-oxidised stepped patch plates. Engines are two or three
> thick-walled bells of clearly unequal size. Cargo lives in enclosed capsule pods seated in solid
> clamp collars, and every asset has at least one large flush closed smuggler hatch. Palette:
> tarnished bronze and umber body, verdigris secondary, off-white only on whole salvaged sections,
> gunmetal joints, near-black glazing, and a single controlled accent of deep crimson as flat
> trade-mark stencils. Wear concentrates at collars and hatches. **Avoid** Terran hazard stripes,
> tarps, dangling cargo, clean luxury curves and all-over neon.

---

## 1. MAU-KIT-001 — shared detail library sheet

> A labelled component sheet of isolated Mauna shared parts in neat rows on a light-grey
> background, each part drawn separately at consistent scale with a small family code label:
> MAU-CLP thick clamp-collar rings and split clamps in three sizes; MAU-POD enclosed capsule cargo
> pods in small, medium and large; MAU-PAT stepped salvage patch plates; MAU-HAT large flush closed
> smuggler hatches and cargo shutters; MAU-ENG thick-walled engine bells in three unequal sizes;
> MAU-SLV two whole salvaged off-white angular blocks; MAU-GLZ opaque slit viewports; MAU-ANT one
> squat thick-bowl dish with a heavy rim on a block mount, plus a block sensor head; MAU-WPN a
> concealed cupola turret shown stowed and deployed with a thick barrel shroud; MAU-CWT a solid
> tapered counterweight tower; MAU-LGT an inactive lantern housing; MAU-DCK a pod-transfer cradle.
> *(+ style block + scan-safety block; labels are the only permitted text)*

## 2. MAU-BLD-CMD-001 — Exchange (Mauna Command Centre), hero concept

Envelope: Terran BLD-CMD-001 footprint, **70 × 55 × 35 m**, so the gameplay footprint is shared.
At 70 m the 2% floor is **~1.4 m**.

> Mauna Exchange, 70 × 55 × 35 metres: the colony headquarters of a black-market trading race,
> built from a large freighter hull that has been grounded upside-down on a stepped gunmetal
> plinth and turned into a fortified market hall. The dominant mass is the smooth bronze dome of
> the inverted hull, with a wide crimson trade-mark band stencilled around it and one long opaque
> slit viewport near its crown. Welded to one side is a whole salvaged off-white angular block of
> foreign construction, joined to the dome by a thick gunmetal clamp collar. On the opposite side,
> a rack of three enclosed capsule cargo pods sits in solid clamp collars on the plinth. Behind
> the dome, one solid tapered counterweight tower with a block cap. On the shoulder, a squat
> thick-bowl dish on a chunky block mount. At the front, one oversized flush closed smuggler hatch
> set into the hull. Large stepped verdigris patch plates on the dome. Strong asymmetry and one
> dominant feature: the inverted hull.
> *(+ style block + scan-safety block)*

The later body-only base prompt (Stage C) removes the pods, collars, dish, hatch, lanterns and
tower cap as `MAU-*` shared parts, and keeps the dome, plinth, salvaged block and material zones.
Write it as `MAU-BLD-CMD-001-base-v01.md` only after the hero concept is approved.

## 3. MAU-SHP-001 — Scoutship

Envelope: Terran scout proportions measured from `scout.glb`, **length : width : height = 1 : 0.70 : 0.32**
(in game: Scoutship, 0.62 world units). The lopsided pod may widen it slightly, but keep the length dominant.

> Mauna scout ship: a small bronze teardrop hull, nose forward, pushed by one oversized
> thick-walled engine nacelle offset to port. The imbalance is countered by one enclosed off-white
> capsule pod clamped to the starboard flank in a thick gunmetal collar. A narrow opaque cockpit
> slit sits off-centre near the nose. One verdigris patch plate, one small crimson stencil and one
> flush closed hatch on the dorsal hull. Compact, fast-looking, clearly lopsided.
> *(+ style block + scan-safety block)*

## 4. MAU-SHP-003 — Hauler

Envelope: Terran transporter proportions measured from `transporter.glb`, **1 : 0.41 : 0.19**
(in game: Hauler, 0.82 world units). The Mauna belly is deliberately wider, so target about 1 : 0.55 : 0.25 and
check it against the Hauler slot before generating.

> Mauna hauler: an oversized bulbous bronze cargo belly, much wider than its tiny
> salvaged off-white cockpit block, which is welded on off-axis at the nose. Two thick gunmetal
> clamp collars wrap the belly. Three thick-walled engine bells of clearly unequal size are
> clustered at the stern. Large verdigris patch plates, a crimson stencil band beside the forward
> collar, and a very large flush closed smuggler hatch along the belly. It should read as
> "carrying more than it declares".
> *(+ style block + scan-safety block)*

## 5. MAU-SHP-007 — Fleet Battleship

Envelope: Terran battleship proportions measured from `battleship.glb`, **1 : 0.45 : 0.14**
(in game: Fleet Battleship, 1.30 world units, the largest hull). Long and low; the joining collar
and turret cupolas must not push the height much above 0.2.

> Mauna fleet battleship: a long, low capital hull visibly made of two different ships, with a rounded verdigris-plated
> forward section and an angular salvaged off-white aft section, joined at a massive gunmetal
> clamp collar. An enclosed bronze cargo pod runs along the spine. Two concealed cupola turrets
> with thick barrel shrouds sit asymmetrically, one on each section. Two thick-walled engine bells
> of unequal size are at the stern. A narrow opaque bridge slit and crimson chevron stencils are at
> the bow. Menacing but improvised.
> *(+ style block + scan-safety block)*

---

## Review gate before running

- [x] Owner approves the Faction Styles row and the silhouette sheet (approved 2026-09-14).
- [x] Asset IDs are race-prefixed (`MAU-BLD-…`, `MAU-SHP-…`; owner decision 2026-09-14).
- [x] Ship list follows the game's seven hulls (owner decision 2026-09-14).
- [x] Scoutship, Hauler and Fleet Battleship envelopes measured from the generated models (sections 3–5).

## Generation record — v01 (2026-09-14, awaiting owner verdict)

One run each, all first pass, no correction passes yet. Review against `docs/concept-rules-for-3d.md`:

| Output | On-look | 3D-rule issues / deviations for a v02 correction pass |
|---|---|---|
| `MAU-KIT-001_shared-detail-library_concept_v01.png` | yes; all 12 families, labels correct | invented crimson "M" logo on most parts; rivets below 2% (A2); dish is a thin shell (A3, already an H part) |
| `MAU-BLD-CMD-001_concept_v01.png` | yes; closest to the silhouette sheet | invented off-white emblem inside the crimson band (differs from the kit "M") |
| `MAU-SHP-001_concept_v01.png` | yes | deep open engine bell (A6 negative space); small rivets on the patch (A2) |
| `MAU-SHP-003_concept_v01.png` | yes | tiny text-like stencil near the band (C: no text); patches read thin rather than stepped (B4) |
| `MAU-SHP-007_concept_v01.png` | yes | thin twin gun barrels (A5); crimson chevrons repeated aft (prompt: bow only) |

### Owner verdict (2026-09-14)

- **Approved as v01:** MAU-BLD-CMD-001, MAU-KIT-001, MAU-SHP-003, MAU-SHP-007. The 3D-rule notes above
  are carried into cleanup/base generation, not a regeneration.
- **Rejected:** MAU-SHP-001 v01. The engine faces sideways, which makes no sense for thrust.
  v02 is a reference-conditioned edit: `runs/MAU-DIR-001/MAU-SHP-001_concept_v02.txt`, attached to
  v01 and the emblem crop. It points the engine straight aft, closes the bell with an exhaust plate,
  swaps the stencil for the emblem and removes the rivets.
  **Result:** `MAU-SHP-001_concept_v02.png` (Codex, one run). The engine axis now runs along the hull,
  pointing aft, with its end closed by an exhaust plate; the crescent emblem is on the dorsal hull and
  the rivets are gone.
  **Owner verdict on v02: rejected.** The engine still reads as a barrel stuck on the ship's behind.
- **MAU-SHP-001 v03: two alternatives, run in parallel.** Neither is conditioned on v01/v02, which
  kept steering the generator back to a separate cylinder. Both use the approved Hauler as the style
  reference, plus the emblem crop.
  - `v03a`: one continuous hull that swells into an offset engine housing built into the stern.
  - `v03b`: a bronze nose welded to a salvaged off-white engine block with two unequal recessed nozzles.
  Prompts: `runs/MAU-DIR-001/MAU-SHP-001_concept_v03a.txt` and `…_v03b.txt`.
  **Results:** both generated. v03a is a continuous bronze hull that swells into a stern engine
  housing, with the off-white pod snug to starboard and the crimson emblem on the back. v03b is a bronze
  nose clamped to a faceted off-white engine block with two unequal flush nozzles and the emblem on the
  block. Neither has a separate barrel. Comparison: `Concepts/Mauna/review-shots/MAU-SHP-001_v03-options.png`.
  **Owner pick (2026-09-14): v03a approved** (engine built into the hull). v03b is kept as a
  record and is not used.
- **Faction emblem:** the **Exchange crescent-and-blade** is the single Mauna emblem. Reference crop:
  `Concepts/Mauna/Shared/MAU-EMB-001/MAU-emblem_ref_v01.png`. The kit sheet's crimson "M" is not the
  emblem; it becomes the crescent when the kit parts are textured.
