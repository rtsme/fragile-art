# TER-KIT-001 Command Centre shared-object generation manifest v01

Status: **Meshy trial complete; reference validation exceptions documented; review/cleanup pending**
Approved concept sheet: `../../../Concepts/Terran/Shared/TER-KIT-001/TER-KIT-001_command-centre-gap-modules_concept_v04.png`
Production specification: `../../../Concepts/Terran/Shared/TER-KIT-001/TER-KIT-001_command-centre-gap-modules_production-spec_v04.md`

Each package contains one retained 2×2 source sheet and four standalone generator/modelling inputs.
Use files in this order: **front, back, left, right**.

Post-trial consistency results are recorded in `../TER-KIT-001_reference-validation_v01.md`.
Seven packages fail the current height/centring gate and must be regenerated before further paid
generation or production approval. Their existing GLBs are retained as trial outputs, not as proof
that the reference packages passed.

| Component ID | Envelope (m) | Build route | Reference folder | Production note |
|---|---:|:---:|---|---|
| TER-GLZ-BND-M | 4 × 0.5 × 1.5 | R | `TER-GLZ-BND-M/` | generate closed frame/pane; assign glass material later |
| TER-GLZ-BND-CNR | 2 × 2 × 1.5 | R | `TER-GLZ-BND-CNR/` | generate 135-degree corner; verify angle during cleanup |
| TER-DOR-PRT-L | 6 × 2 × 5 | R | `TER-DOR-PRT-L/` | generate portal only; cargo door remains separate |
| TER-VNT-FAN-L | 4 × 1.5 × 4 | H | `TER-VNT-FAN-L/` | model housing and centred rotor as separate child meshes |
| TER-PIP-ELB-M | 2.5 × 2.5 × 1.5 | R | `TER-PIP-ELB-M/` | generate capped; open S2 ends during cleanup if required |
| TER-PIP-TEE-M | 3 × 2 × 1.5 | R | `TER-PIP-TEE-M/` | generate capped; preserve exactly three S2 branches |
| TER-ACC-RMP-L | 4 × 8 × 2 | R | `TER-ACC-RMP-L/` | generate closed wedge; set exact 1:8 slope in cleanup |
| TER-ACC-RAL-M | 4 × 0.3 × 1.2 | H | `TER-ACC-RAL-M/` | hand-model exactly three posts and two rails |
| TER-ACC-RAL-CNR | 1 × 1 × 1.2 | H | `TER-ACC-RAL-CNR/` | hand-model 90-degree return with three posts |
| TER-ANT-AER-S | 0.5 × 0.5 × 1.5 | H | `TER-ANT-AER-S/` | hand-model minimum 0.25 m shaft diameter |
| TER-ANT-AER-M | 0.5 × 0.5 × 2.5 | H | `TER-ANT-AER-M/` | hand-model minimum 0.3 m shaft diameter |

`R` components may enter image-to-3D generation as isolated objects. `H` components use the same
four-view packages for controlled manual modelling or heavy retopology. Do not submit all eleven as
one combined generation request and do not merge any component into the Command Centre base.

All eleven components now have independent Meshy source GLBs. See
`../../../Models/Terran/meshy-command-centre-batch-results_v01.md` for task IDs, costs, geometry
statistics, and review status. `H` outputs remain experiments and are not automatically approved.

## Acceptance gates for each shared object

1. Envelope dimensions match the v04 specification at 1 unit = 1 metre.
2. Origin is centred on the mounting footprint and lies on the mounting plane.
3. Forward direction and socket face match the front reference.
4. Every S1-S4 interface is on the 0.5 m grid and is not rescaled independently.
5. Geometry is watertight where the specification says closed.
6. Generated colour/lighting is removed; production materials use the Terran modular material
   pipeline.
7. The cleaned component is tested on the `BLD-CMD-001` receiver before library approval.
