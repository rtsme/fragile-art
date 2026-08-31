# BLD-CMD-001 — body-only pipeline trial prompt record v01

Date: 2026-08-31
Mode: built-in image generation, image-edit workflow
Final target input: `Concepts/Terran/Buildings/BLD-CMD-001/BLD-CMD-001_concept_v01.png`
Accepted output: `Concepts/Terran/Buildings/BLD-CMD-001/Base/BLD-CMD-001_base-concept_v01.png`

## First edit prompt

> Edit the supplied approved Terran Command Centre concept into a BODY-ONLY 3D mesh-generation
> source image. The supplied image is the immutable FINAL APPEARANCE TARGET. Preserve its camera,
> full building footprint, overall proportions, stepped fortress silhouette, dominant central
> command block, roof heights, primary wall planes, foundation slab, large structural frames,
> major chamfers, and large silhouette-defining buttresses. Do not redesign the building.
>
> Remove every reusable/detail attachment from the building body: dishes, antennas, radar heads,
> masts, aerials, windows, glazing modules, personnel doors, airlocks, cargo doors, hatches, tanks,
> vessels, exposed pipes, conduit, valves, couplers, vents, louvers, heat exchangers, roof fans,
> equipment boxes, access panels, lamps, warning beacons, stairs, ramps, railings, ladders, catwalk
> details, small platforms, surface greeble, decorative seams, bolts, decals, hazard striping and
> painted markings. Replace glazing and door modules with plain, closed, flat-bottomed receiving
> recesses; never show an interior.
>
> Where a removed component attaches, show only a simple low-detail mounting interface: a blank
> square or circular pad/recess on the 0.5 m construction grid. Use four standardized visual sizes
> only: S1 0.5 m, S2 1 m, S3 2 m, S4 4 m. Pads must be flush or shallow, broad, closed, and easy
> for image-to-3D reconstruction. Do not place component labels or text on the image.
>
> Keep only the main enclosed architectural shell: foundation, load-bearing walls, roofs, towers,
> large overhangs, deep structural setbacks, broad armour masses, and silhouette-defining
> buttresses. The result should look intentionally unfinished and ready for separate shared-kit
> parts to be attached later. Render as a single elevated three-quarter view matching the source
> composition, centred on a plain light-grey background. Uniform matte light neutral grey clay
> material, subtle value separation between major masses only. Flat neutral studio lighting, no
> cast ground shadow, no environment, no text, no people, no vehicles, no props, no emissive glow,
> no glass, no thin elements, no surface noise. Crisp hard-surface edges and broad chamfers.

## Cleanup edit prompt

> Refine the first body-only pass while preserving its camera, footprint, stepped fortress massing,
> roofs, walls, broad chamfers, foundation slab, structural frames and silhouette-defining
> buttresses. Completely remove the remaining front stair/ramp/landing, side access steps and
> decorative projecting portal frame. Close every dark/open doorway or hatch aperture and replace
> it with a shallow flat-bottomed rectangular receiver. Keep the broad command-window receivers,
> but leave them plain and solid with no glass, panes, mullions, glow or interior. Retain only the
> simple square/circular mounting pads. Remove any remaining detailed attachment or greeble.
> Uniform matte neutral-grey clay, flat studio light, plain background, no shadow, text or props.

## Review result

Accepted after the cleanup edit. The image retains the primary Command Centre massing while
showing only a closed structural shell, glazing/door recesses and simple mounting pads. All visible
detail is governed separately by `BLD-CMD-001_assembly-manifest_v01.md`.
