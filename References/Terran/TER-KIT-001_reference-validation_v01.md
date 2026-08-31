# TER-KIT-001 reference validation v01

Date: 2026-08-31
Checker: `python tools/check-views.py --json <front> <back> <left> <right>`

This records the consistency gate after correcting the checker to compare width only within valid
opposing pairs (front/back and left/right). Height and centring are still compared across all views.

These packages were already used for the completed Meshy trial before the gate was enforced. They
are retained to reproduce those source tasks and evaluate their outputs, but a failed package is not
an approved template for new generation. Regenerate a failed package before spending further credits
or promoting its source geometry beyond the recorded trial.

| Package | Result | Findings |
|---|---|---|
| BLD-CMD-001 Base | fail | height and vertical centring disagree |
| TER-ACC-RAL-CNR | fail | vertical centring disagrees |
| TER-ACC-RAL-M | fail | height and vertical centring disagree |
| TER-ACC-RMP-L | pass | no checker issue |
| TER-ANT-AER-M | pass | no checker issue |
| TER-ANT-AER-S | pass | no checker issue |
| TER-DOR-PRT-L | fail | height and vertical centring disagree; horizontal centring warning |
| TER-GLZ-BND-CNR | fail | height and vertical centring disagree |
| TER-GLZ-BND-M | fail | height and vertical centring disagree |
| TER-PIP-ELB-M | pass with warning | minor vertical centring warning |
| TER-PIP-TEE-M | fail | height and vertical centring disagree |
| TER-VNT-FAN-L | pass | no checker issue |

Summary: **5 pass/pass-with-warning; 7 fail**. The trial GLBs remain available for inspection and
assembly work, but the failures must not be described as gate-approved reference packages.
