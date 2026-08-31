# Terran shared-component generation references

Each exact component ID has its own folder containing five files:

```text
<Component ID>_reference-sheet_vNN.png
<Component ID>_front_vNN.png
<Component ID>_back_vNN.png
<Component ID>_left_vNN.png
<Component ID>_right_vNN.png
```

The reference sheet is the generation record. The four standalone views are the inputs supplied to
Art Forge or used as modelling references, always in front, back, left, right order. Dimensions,
socket class and build classification remain authoritative in the relevant TER-KIT production
specification.

The current Command Centre trial packages include known scale/centring exceptions created before
the consistency gate was enforced. Read `../TER-KIT-001_reference-validation_v01.md` before reusing
or regenerating them.

The component is generated or modelled at the specification's real dimensions and with its origin
centred on the mounting footprint at ground/mounting-plane level. Reference backgrounds, shadows
and concept textures are not geometry.
