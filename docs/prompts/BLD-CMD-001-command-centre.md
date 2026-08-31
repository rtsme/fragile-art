# BLD-CMD-001 — Command Centre, regeneration prompts (v02)

Rewrite of the v01 prompts to satisfy [`../concept-rules-for-3d.md`](../concept-rules-for-3d.md).
v01 produced a good drawing but a poor reconstruction: a noisy comms dish, lumps behind the
window glass, blurred greeble, and four orthographic views that disagreed with each other by
up to 14.5%.

**Asset spec** (from the tracker): 70 × 55 × 35 m, primary colony headquarters and landmark,
Terran industrial hard-surface. **Scale rule: 1 unit = 1 metre.**
At 70 m, rule A2's 2% floor means **no feature smaller than ~1.4 m**. Doors at 2.2–2.6 m clear
it; human-scale railings at ~1.1 m do not, which is why they become solid parapets.

---

## 1. Hero concept

> Elevated three-quarter industrial building concept, centred on a plain flat light-grey
> background. No ground shadow, no environment, no text, no props.
>
> **Subject.** Terran Command Centre, 70 × 55 × 35 metres — a fortified industrial headquarters
> for an asteroid mining colony, combining command operations, communications and visible colony
> authority. It is the settlement's landmark and must read as such from a distance.
>
> **Form.** Chunky rectangular and hexagonal masses in a stepped, fortress-like massing with a
> dominant central command block. Reinforced frames, controlled asymmetry, one dominant
> functional feature. Bolted frames, replaceable armour panels, external service routes and
> modular upgrade sockets. Visible pipes, tanks, vents and radiators, all as **solid raised
> volumes** built into the mass.
>
> **Materials.** Painted steel and exposed steel, ceramic armour, industrial plastic. Dark
> neutral metals with warm off-white panels and amber hazard accents. Matte to satin throughout.
> Functional seams, fasteners, and wear at contact points.
>
> **Build it to be scanned into 3D — these are hard constraints, not style notes:**
>
> - **Solid enclosed volumes only.** No open lattice, truss, scaffold or A-frame structures.
>   Anything that would be an open framework is drawn as a solid tapered mass instead.
> - **No thin elements.** No wires, cables, aerials, ladders or thin handrails. Railings are
>   **solid low parapets**. Conduits are raised ribs on a surface, not free-standing pipes.
> - **The antenna cluster is chunky.** Masts are thick tapered towers, not rods. Any dish is a
>   **thick solid bowl** with a heavy rim on a blocky mount — never a thin curved sheet.
> - **Windows are flat, opaque, dark glass.** A single dark value. **No visible interior, no
>   consoles, no screens, no figures, no reflections, no depth behind the pane.**
> - **Large flat panels with deep bold breaks.** No fine greeble, no dense mechanical filigree,
>   no decorative noise. **No feature smaller than about 1.4 metres.**
> - **Matte only.** No chrome, no gloss, no specular highlights, no transparency anywhere.
> - **Flat even studio lighting.** No cast shadows, no dramatic rim light, no ambient occlusion
>   drama. **No glowing windows, no emissive lights, no light spill** — lighting is added later
>   in-engine.

Read [`../concept-rules-for-3d.md`](../concept-rules-for-3d.md) for why each of these exists;
every one is traceable to an observed failure.

---

## 2. Orthographic references

**Generate one sheet, then crop it. Do not generate four separate images.**

This is the important change. v01's prompt asked for a 3×2 sheet, but the six delivered files
came out at two different canvas sizes (1402×1122 and 1536×1024) with silhouettes varying by
14.5% — so they were regenerated independently somewhere in the process. Cropping from a single
sheet makes consistency structural instead of something you have to police.

> Technical orthographic reference sheet for the approved Terran Command Centre. **Four true
> orthographic elevations in one image, arranged in a 2×2 grid: FRONT, BACK, LEFT, RIGHT.**
>
> **Every view at identical scale, identical camera distance and identical centring within its
> tile.** True orthographic projection — no perspective, no vanishing points, no foreshortening.
> Flat neutral studio lighting, identical across all four tiles. Plain neutral background, no
> ground shadow, no environment, no labels, no dimension lines.
>
> Preserve the approved design exactly — same proportions, same modules, same asymmetry, same
> tanks, glazing, antenna cluster and roof systems in every view. This is a measurement drawing
> of one object, **not a redesign**; the four views must describe the same building.
>
> Windows flat opaque dark, matte surfaces only, no glow, no reflections, no visible interiors.

**Then:**

1. Crop the four tiles to **identical pixel dimensions**.
2. Save as `BLD-CMD-001_{front,back,left,right}_v02.png`.
3. **Verify before generating a mesh:**

```bash
python tools/check-views.py References/Terran/Buildings/BLD-CMD-001/*_v02.png
```

It must report `OK - views are mutually consistent.` Art Forge runs the same check and will
warn in the UI as soon as you select the images.

Top and bottom are optional now (four-view package) — produce them only if the roof or underside
carries gameplay-readable detail.

---

## 3. Generating the mesh

Art Forge → Meshy backend → select the four views, **front first** → **Mesh: Max quality —
no remesh** → 4K + PBR. Roughly 10 minutes and 30 credits.

Do not use the remesh options for the source asset — Meshy's own guidance is that no-remesh
gives the highest-quality geometry, and remeshing at 15k was what melted the v01 result.
Decimate afterwards as a deliberate step you can inspect.

---

## 4. What to expect to still fail

Model these by hand and kitbash them in — they break the rules by their nature, and a shared kit
gives faction consistency that per-asset generation cannot:

- the comms dish and any radar array
- antenna masts, if they need to be genuinely slender
- railings, ladders and catwalks
- exposed pipework runs and gantries
