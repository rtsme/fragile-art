# BLD-MIN-001 base-building source

`BLD-MIN-001_base-concept_v02.png` is the active textured body-only generation source for the Basic
Mine pipeline trial. It is derived from, but does not replace, `../BLD-MIN-001_concept_v03.png`.
The clay `BLD-MIN-001_base-concept_v01.png` is retained as superseded failure history: it established
the geometry split but incorrectly removed the base materials.

## Keep in the base

- integrated foundation/deck and broad perimeter edge masses
- low processing, utility and control-building shells
- central raised octagonal drill deck and closed S4 axial receiver
- broad structural steps, deep setbacks, large chamfers and continuous buttresses
- simple S1-S4 pads and closed recesses for every detachable component

## Keep out of the base

- portal derrick, gantry bracing, hoist, rotary head and visible drill stem
- enclosed conveyor and its transfer junction
- tanks, pipes, valves, vents, fans, flues and extraction fittings
- doors, hatches, railings, ladders, lights, beacons, panels and equipment boxes
- building-specific decals, glow and surface greeble

## Keep in the texture source

- broad warm off-white armour zones on structural shells
- matte graphite foundation, frame and receiver zones
- restrained flat amber hazard bands on existing deck edges and receiver surrounds
- macro-scale chipped paint, dust and mining grime that follows existing surfaces
- no painted detail that implies geometry not present in the base

Generate orthographic references from the textured body-only v02 image, not from the fully dressed
v03 concept or the clay v01 massing study. Exact attachments are controlled by
`../BLD-MIN-001_assembly-manifest_v01.md`.

The reviewed assembly has no drill-bit/cutter asset and no geometry beneath the foundation. The
visible drill stem ends inside the upper deck receiver.

The approved textured turnaround is reference-sheet v12. Its four crops pass the preferred scale
and centring tolerances with no validator issues. See
`../../../../../References/Terran/Buildings/BLD-MIN-001/Base/BLD-MIN-001_reference-validation_v03.md`.

The resulting maximum-detail textured Meshy source is
`../../../../../Models/Terran/Buildings/BLD-MIN-001/Base/BLD-MIN-001_base_hq_v01.glb`.
Task `01a059f4-8b63-7428-8c59-900835e146cd` completed for 30 credits with five downloaded PBR
maps. File integrity passes; visual geometry and texture review remains pending.
