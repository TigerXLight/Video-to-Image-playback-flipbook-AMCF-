# AMCF Tests Newest-To-Oldest Part 14: 03T Through 03A

This part covers every next top-level folder in descending name order, from `Test 03T` immediately below Part 13's `Test 03U` through `Test 03A`. The next folders are `Test 02` and `Legacy Test 01`; neither is silently skipped. Every folder's Python source inventory and available verdict/report was checked. Source logic was read closely for the selected 03M motion diagnostic and 03S map correction. A complete line-by-line comparison of every experimental script remains open.

The transcript summary confirms the progression: 03A/03B tracking failures led to 03C crash diagnosis, plain-SAM2 03D-03G diagnostics, preview and motion truth work in 03H-03O, then visual/support experiments in 03P-03T. Later 03U had stronger support accounting but visible tree/trunk artifacts; 03V selected 03P as the watchable baseline, and 03Y later selected mild sharpness recovery. These later decisions govern which older results are treated as accepted behavior.

| Folder | Local source and result | `Main` / public reading |
| --- | --- | --- |
| `Test 03T` | `run_autonomous_closeout_loop_03t.py`; PARTIAL after six iterations; nominal support 40%, measured current-frame support 100%. | Not integrated into `Main`; do not promote this support claim. |
| `Test 03S` | `create_ai_assisted_corrected_map_03s.py`; PASS for corrected-map creation; transient people and waterfall split; manual review required. | Not integrated into `Main`; source-specific map is evidence, not general ground truth. |
| `Test 03R` | `create_manual_map_smooth_retest_03r.py`; PASS for 288-frame retest; selected `manual_map_hybrid_support_40`; human review still required. | Not integrated into `Main`; 03T exposed its support-accounting limitation. |
| `Test 03Q` | `create_reduced_fullframe_amcf_ladder_03q.py`; setup PARTIAL, then local run selected 75% support because 50% failed its threshold. | Not integrated into `Main`; later 03V judged visual quality before support reduction. |
| `Test 03P` | `create_smooth_amcf_candidate_03p.py`; setup PARTIAL, local 288-frame run completed with a seed map; later 03V selected its visual baseline. | Not integrated into `Main` as this runner; accepted as a later visual reference, not final map truth. |
| `Test 03O` | `create_manual_roi_editor_03o.py`; editor setup and image-path repair PASS. | Not integrated into `Main`; corrected-map review remained a user task. |
| `Test 03N` | `create_corrected_motion_component_map_03n.py`; setup PASS, local 288-frame map run later completed. | Not integrated into `Main`; advanced the 03M motion taxonomy. |
| `Test 03M` | `create_motion_truth_audit_03m.py`; camera compensation, residual masks, zone metrics, overlay, and component coverage; local 288-frame run completed. | Not integrated into `Main`. Reusable motion-zone logic is ported in this part. |
| `Test 03L` | `create_single_review_amcf_layer_preview_03l.py`; setup PASS and later local review outputs. | Not integrated into `Main`; missing local motion prompted 03M. |
| `Test 03K` | `create_camera_registered_hold_preview_03k.py`; setup PASS; affine/tree registration preview. | Not integrated into `Main`; parallax and deformation remained limitations. |
| `Test 03J` | `create_physical_speed_smoothness_preview_03j.py`; setup PASS; cadence and held-component preview. | Not integrated into `Main`; no final reconstruction claim. |
| `Test 03I` | `create_watchable_amcf_preview_03i.py`; setup PASS; component-layer preview with source-frame support. | Not integrated into `Main`; source-background support limits reconstruction claims. |
| `Test 03H` | `create_amcf_review_playback_03h.py`; setup PASS; held contours and review cadence. | Not integrated into `Main`; held masks were labelled as held, not current tracking. |
| `Test 03G` | `run_plain_sam2_fluid_solid_split_03g.py`; bounded fluid/solid diagnostic PASS, broad foam background still unresolved. | Not integrated into `Main`; later component work superseded its raw masks. |
| `Test 03F` | `run_plain_sam2_hybrid_resolution_03f.py`; diagnostic PASS; box baseline remained safest, hybrid and higher resolution did not improve it. | Not integrated into `Main`; no final AMCF acceptance. |
| `Test 03E` | `run_plain_sam2_prompt_study_03e.py`; diagnostic PASS; box prompt selected over point/mask alternatives. | Not integrated into `Main`; bounded 24-frame study. |
| `Test 03D` | `run_plain_sam2_multitarget_03d.py`; plain-SAM2 multi-object diagnostic PASS at 48 frames. | Not integrated into `Main`; no archive/reconstruction acceptance. |
| `Test 03C` | SAMURAI crash diagnosis and microproof scripts; diagnostic PASS, not final 03B acceptance. | Not integrated into `Main`; plain-SAM2 route informed 03D. |
| `Test 03B` | `run_samurai_03b.py`; FAIL due multi-object crash and CPU feasibility. | Not integrated into `Main`; do not restore it as the selected backend. |
| `Test 03A` | Three dated attempts: dependency/tracking FAIL, then OpenCV diagnostic tracking that still failed object-bound contour fidelity. | `Main/amcf_tracking_test03a.py` retained the bounded diagnostic; public `src/amcf_local_main_tracking_test03a.py` is a public-safe adaptation. It is not an accepted tracking solution. |

## What Part 14 Added

- `src/amcf_motion_truth_diagnostics.py`: reusable 03M camera-compensated motion-zone and overlay behavior.
- `demo/run_amcf_motion_truth_diagnostics_demo.py`: deterministic synthetic-frame report and overlay.
- `tests/test_amcf_motion_truth_diagnostics.py`: positive and negative behavior checks.
- `docs/AMCF_MOTION_TRUTH_DIAGNOSTICS_PARITY.md`: scope and claim boundary.

The public repo's newer software I/O, component-event, V2, and physical-player layers remain present. This part does not establish complete parity for the full 03A-03T runners or media outputs. It preserves the later visual decisions that rejected earlier attractive but flawed methods.

Generated output committed: no. Unsafe acceptance count: 0. Hardware validation claimed: false. Physical Level 5 claimed: false. Manufactured player claimed: false.
