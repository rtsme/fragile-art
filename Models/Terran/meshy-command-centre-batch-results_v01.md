# Command Centre Meshy source-generation results v01

Status: **all source jobs completed; visual and geometry review pending**

This record covers the original `TER-GLZ-BND-M` pipeline trial plus the eleven-job Command Centre
batch. Every job used Meshy's latest multi-image-to-3D model with ordered front/back/left/right
inputs, 4K PBR textures, GLB output, and remeshing disabled. These are maximum-detail source meshes,
not approved or game-ready assets.

| Asset | Route | Meshy task ID | Credits | GLB size | Vertices | Triangles | Maps |
|---|:---:|---|---:|---:|---:|---:|---:|
| TER-GLZ-BND-M | R | `01a057df-974d-7056-8dc3-344fc9a16d6e` | 30 | 76.57 MB | 1,010,182 | 1,958,274 | 5 |
| TER-GLZ-BND-CNR | R | `01a0584e-054a-7602-af1f-17e95aaa9706` | 30 | 76.83 MB | 1,019,913 | 1,944,478 | 5 |
| TER-DOR-PRT-L | R | `01a0584e-058a-727a-8ede-e5515bcaf5f6` | 30 | 80.62 MB | 1,030,052 | 1,989,316 | 5 |
| TER-VNT-FAN-L | H | `01a05852-46ca-776c-b518-cff79e7e591a` | 30 | 78.20 MB | 1,035,642 | 1,971,964 | 5 |
| TER-PIP-ELB-M | R | `01a05852-8a85-72be-a83a-e1e6fc931ef8` | 30 | 73.57 MB | 917,126 | 1,768,638 | 5 |
| TER-PIP-TEE-M | R | `01a05856-a40b-728d-bbcd-8a1f014ff632` | 30 | 77.58 MB | 1,038,239 | 1,996,564 | 5 |
| TER-ACC-RMP-L | R | `01a05856-e622-7704-870b-af9a407d09bc` | 30 | 78.91 MB | 1,037,139 | 1,987,470 | 5 |
| TER-ACC-RAL-M | H | `01a0585a-8309-7509-89e1-9ab7151ea221` | 30 | 74.56 MB | 937,009 | 1,805,858 | 5 |
| TER-ACC-RAL-CNR | H | `01a0585a-deb2-75e9-9d65-6ff03bed0d5f` | 30 | 77.82 MB | 1,030,904 | 1,989,416 | 5 |
| TER-ANT-AER-S | H | `01a0585e-cd5d-75c9-90eb-5d62968c7f26` | 30 | 77.17 MB | 1,027,725 | 1,996,120 | 5 |
| TER-ANT-AER-M | H | `01a0585f-2af3-73d2-af44-15a2d4bddcf3` | 30 | 77.70 MB | 1,020,450 | 1,976,476 | 5 |
| BLD-CMD-001-base | base | `01a05863-1f09-7771-8d5a-625e229ded56` | 30 | 70.64 MB | 1,038,641 | 1,997,976 | 5 |

Totals: **12 jobs, 360 credits, 12 parseable GLBs, 60 texture maps, 920.1 MB of GLB source data**.
The eleven-job batch itself consumed 330 credits; the first row was the earlier 30-credit trial.

`R` marks components intended for reconstruction-led cleanup. `H` marks fragile components whose
generated result is an experiment and must not replace the hand-modelled route without visual
approval. All outputs still require silhouette review, exact metre scaling, origin/orientation
normalization, watertightness testing, retopology/decimation, UV/material cleanup, and receiver-fit
testing against `BLD-CMD-001`.
