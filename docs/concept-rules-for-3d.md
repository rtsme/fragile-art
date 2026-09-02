# Concept rules for 3D reconstruction

Rules for authoring concepts and orthographic references that survive image-to-3D generation.
These are **not** style rules — faction aesthetics live in the tracker's `Faction Styles` sheet.
These are constraints imposed by how the generator reconstructs shape, and they apply to every
faction equally.

Every rule below is derived from an observed failure on a real asset, not from general advice.

## Why these limits exist

The generator does not "understand" a machine. It infers a **volumetric field** from the images
and extracts a surface from it. Three consequences follow, and they explain almost every failure
we have seen:

1. **A surface needs volume on both sides to exist.** Thin shells and open frameworks have no
   interior for the field to fill, so they collapse into solid masses or noisy sheets.
2. **Detail below the field's resolution is averaged, not simplified.** Small features do not
   become simpler — they blur into their neighbours.
3. **Depth is inferred from shading.** Anything that reads as depth in the image becomes depth in
   the mesh, whether or not it is real geometry.

## A. Geometry

**A1 — No open frameworks.** Trusses, derricks, lattice towers, exposed scaffolding, A-frames.
*Observed:* BLD-MIN-001's drilling derrick — an open triangulated A-frame — came back as a
**solid fin**. Not a resolution problem; the reconstructor cannot represent see-through structure.
**Instead:** draw the same form as a solid tapered volume, or leave it out and kitbash it later.

**A2 — Minimum feature size ≈ 2% of the longest dimension.** Anything smaller blurs into whatever
it touches. On a 40 m building that is roughly 80 cm.
**Instead:** fewer, bigger, deeper features. One 40 cm panel break reads; five 5 cm scribes become
a smear.

**A3 — Thin shells need visible thickness.** Dishes, vanes, fins, blades, aerial reflectors.
*Observed:* the comms dish on BLD-CMD-001 reconstructs as messy, noisy geometry — it is a
doubly-curved sheet with a feed strut, which is the worst case for A1 and A2 together.
**Instead:** draw a dish as a **thick bowl** with an obvious rim and a chunky mount, or omit it.

**A4 — Flat planes with bold breaks beat dense greeble.** Large flat surfaces reconstruct cleanly
and read well at gameplay distance. Fine mechanical filigree does not survive.
**Instead:** big planes, deep chamfers, strong step changes between masses.

**A5 — No free-standing thin elements.** Wires, cables, chains, aerials, thin handrails, ladders.
**Instead:** railings become **solid low parapets**; conduits become raised ribs on a surface.

**Pipeline rule — no railings in Meshy reconstruction inputs.** Do not draw rail-form geometry in
single-image or multiview inputs, including low-detail monolithic buildings. Meshy may fuse occluded
rails into nearby machinery at maximum detail or collapse them into spikes during remesh. Omit them
entirely; use a broad solid parapet only when that parapet is part of the building's primary massing.

**A6 — Keep the silhouette closed.** Avoid negative space you can see through. Enclosed volumes
reconstruct reliably; gaps invite noise.

## B. Surface and material

**B1 — Glass is flat, opaque and single-valued.** No visible interiors, no screens, no figures,
no depth behind the pane, no reflections.
*Observed:* windows drawn with lit interior detail confuse the reconstructor — it reads the
interior as recessed geometry and produces lumps behind the glass.
**Instead:** one dark, flat value, at most a subtle vertical gradient. Interior life is an
**emissive material in-engine**, not concept geometry.

**B2 — No mirrors, chrome or high gloss.** Specular highlights are read as form, so a bright
reflection becomes a bump.
**Instead:** matte to satin. Metal reads as metal through value and edge wear, not shine.

**B3 — No transparency anywhere.** Same reason as B1, and it also corrupts background removal.

**B4 — Do not paint detail that mimics geometry.** Fake panel lines rendered as soft shadow are
sometimes reconstructed as real depth and sometimes ignored, inconsistently across views.
**Instead:** either make it real geometry with real thickness, or make it unambiguously flat
(a painted marking, a decal, a stencil).

## C. Presentation

**C1 — Flat neutral studio lighting.** No strong cast shadows, no dramatic rim light, no
ambient occlusion baked into the drawing. Ambiguous shadow becomes ambiguous shape.

**C2 — No emissive glow in the concept.** Warm window glow and running lights fight the
generator's `remove_lighting` pass. Add them in the material pass.

**C3 — Plain neutral background, no ground shadow, no environment.**

**C4 — The four views must agree with each other.** This is the most-violated rule and the
easiest to miss, because each view looks fine on its own.

*Observed:* the original BLD-CMD-001 set was measured after the fact and failed badly — the back
view drew the building **14.5% smaller** than the front, the four images were not even the same
canvas size (two 1402×1122, two 1536×1024), and the subject centre drifted 3.3% across views.
The reconstructor has to reconcile views that disagree about how big the thing is, and where they
conflict it hedges — which is a strong candidate for the smeared, doubled detail we saw.

Concretely:

- **Identical canvas size** for all four images.
- **Silhouette height within 3% across all upright views.** Compare width within opposing pairs
  (front/back and left/right), not front against side; a rectangular asset's width and depth differ.
  Over 10% within one of those valid comparisons is a hard fail.
- **Subject centred identically** — centre drift under 2% of canvas.
- **Generate the four as one set**, not as four independent images, wherever the tool allows it.
  Independent generation is what produces the drift.

**Check it before spending credits:**

```bash
python tools/check-views.py References/Terran/Buildings/<ASSET-ID>/*.png
```

It prints each view's silhouette and flags the disagreements, exiting non-zero on a hard fail.
Art Forge runs the same check automatically and shows the result as soon as you select two or
more images.

**C5 — Front view is supplied first** — the generator treats image one as the primary view.

## D. Build these by hand instead

These are exactly the forms that break rules A1, A3 and A5, and they are all trivial to model
and cheap to reuse. Model each once, reuse across the faction:

- comms dishes and radar arrays
- antenna masts and aerials
- railings, ladders and catwalks
- exposed pipework and conduit runs
- derricks, cranes and gantries

Reuse is a bonus, not a consolation: a shared kit gives the faction a consistency that
per-asset generation cannot, and it keeps the parts that read at gameplay distance under
deliberate control.

## E. Split generation and assembly

The approved concept is the final dressed appearance target, not a geometry-reconstruction input.
Before mesh generation, create a body-only source in the asset's `Base/` folder. It keeps only the
main structural shell and replaces every detachable detail with a closed recess, flush pad or S1-S4
receiver. Generate the shell from body-only orthographic references; generate or model reusable
details separately and attach them afterwards.

"Body-only" describes the geometry split, not a clay render. Keep broad approved material zones,
race colour hierarchy and macro-scale wear in the body-only concept and every orthographic view.
Textures must describe existing surfaces only: do not paint fake doors, glazing, vents, pipes,
railings, antennae, panels, seams or recesses where no corresponding form or receiver exists.

After the base geometry passes review, the final concept may also be used in an optional
**texture-only** refinement pass as a palette/material-style reference. That pass must preserve
geometry and be rejected if it paints shared attachments onto unrelated shell surfaces. It refines
or repairs the texture already established by the references; it is not the first texture stage.

This rule applies even when a shared component is individually reconstruction-safe. The point is
to stop the parent generator from having to resolve many small adjacent details at building scale.
See [`shared-assembly-pipeline.md`](shared-assembly-pipeline.md) for the folder contract and gates.

## Prompt block

Append to the `Concept Prompt` and `Reference Prompt` columns in the tracker:

> Solid enclosed volumes only. No open lattice, truss or scaffold structures. No thin sheets,
> wires, cables or thin railings — railings are solid low parapets. Large flat panels with deep
> bold breaks rather than fine greeble; no feature smaller than roughly 2% of the building's
> width. Windows are flat opaque dark glass with no visible interior, no screens and no
> reflections. Matte to satin surfaces only, no chrome, gloss or transparency. Flat neutral
> studio lighting, no cast shadows, no glow or emissive lights. Plain neutral background.

For the orthographic set, add: **all four views on the same canvas size, at the same camera
distance, with the subject at the same scale and the same centre in every view; orthographic
projection; generated as a single consistent set rather than four independent images.**

## Changing these rules

If a rule turns out to be wrong, change it here and say which asset disproved it. Every rule
above names the asset that produced it, and should keep doing so.
