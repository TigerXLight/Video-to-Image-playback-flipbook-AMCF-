# AMCF Tests Newest-To-Oldest Part 13 Residual Visual Review

Part 13 surveyed the next 24 local `Tests` folders, from `Test 07I` down through `Test 03U`. It read the 07E runner's residual codec and gate, the 07I metrics and decision, the 03Y selection, folder-level verdicts, and each folder's Python inventory. The `Main` source inventory has no 07E residual runner or 07I acceptance module. Public `src/amcf_v0/` covers archive tooling, while `src/amcf_quality_metrics.py` covers frame metrics; neither provided the 07E gate and accounting contract. A full code comparison for every script in this band remains open.

| Folder band | Progression and status | Integration reading |
| --- | --- | --- |
| `07I` | `ACCEPT_07G_WITH_HUMAN_REVIEW`; 07A remains visual reference, compression proof retained | Gate/accounting behavior ported; human review remains required. |
| `07E_07F_07G_07H_08A` | `PASS_RESIDUAL_COMPRESSION_SAFE`; 12 residual strategies attempted; selected long-keyframe tile residual; second-clip generalisation not run | Visual threshold and residual-stream accounting ported; media codec/archive not claimed equivalent. |
| `07B_07C_07D`, `07A` | Full-rate truth freeze and original-truth visual baseline passed | Earlier control/reference for 07E and 07I, not a replacement codec. |
| `05C6_06F` through `05B` | Decoded-MP4, fallback/reference, artifact, jitter, and compositor experiments; 05C6 selected the 05C4 control | Progressive research evidence. Later full-rate and residual trials changed the selected path; older fallback acceptance is not promoted as final parity. |
| `04F_05A` through `04A`, `03Z` | v0 archive builder/loader/roundtrip/viewer consolidation | Public v0 toolchain already covers the reusable archive inspection and build surface. |
| `03Y` | `PASS` with mild sharpness recovery, parallax and waterfall checks; suspected texture artifact and human review remain | Artifact-warning gate retained; no claim of automated perceptual judgment. |
| `03X`, `03W`, `03V`, `03U` | Temporal fidelity audit partial; component swap and visual-artifact gates; registered-background active-components candidate strong pass | Shows why later work used zone/temporal diagnostics. Earlier partial work stays evidence, not a selected public default. |

The source runner for 07E uses NumPy frame arrays, OpenCV, and FFmpeg; its output contains local media and large generated archives. This part adds `src/amcf_residual_visual_acceptance.py`, a small demo, tests, and a focused parity document. It does not prove full code or output parity for the 07E codec or the whole local workspace.

Next: continue to the next older folder band, checking selected outcomes against later accepted runs before porting code. Generated output committed: no. Unsafe acceptance count: 0. Hardware validation claimed: false. Physical Level 5 claimed: false. Manufactured player claimed: false.
