# AMCF Local Tests Progression Integration Ledger

Run context: `AMCF_LOCAL_TESTS_PROGRESSION_INTEGRATION_LEDGER_V1`

This ledger maps the local `Main` folder and the milestone-specific `Tests` folders into the public GitHub package. It exists because the local project did not progress in one linear source tree: many improvements were locked into isolated test folders, then some were integrated into `Main`, and later some were ported into the public repo as cleaner public modules.

This is not a byte-for-byte generated-output identity claim. It is a procedural fullness ledger for code, behavior, diagnostics, tests, and useful package surfaces while preserving the newer public software I/O and physical-player work.

Coverage correction: Parts 1-15 are selective folder-level reviews, not an exhaustive inspection of all nested files. The current file-level baseline is `docs/AMCF_TESTS_FILE_LEVEL_COVERAGE_BASELINE.md`; no folder or full-workspace parity claim is complete solely because its name appeared in this ledger.

The non-`Tests` workspace checkpoint is recorded in `docs/AMCF_NON_TESTS_WORKSPACE_PARITY_INVENTORY.md`. It maps the maintained local `Main` files, root physical/research runners, handoff/viewer bundles, diagnostics/assets/media, upstream references, virtual environments, and archives without treating generated or third-party material as missing application source.

## Claim Boundary

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- real printer integration claimed: false
- real scanner integration claimed: false
- real player hardware claimed: false
- unsafe_acceptance_count: 0
- full parity claimed by this ledger: false

## Current Reading

The most useful local evidence is split across:

- `Main`, which holds app-facing source/docs and selected integrated tools.
- `Tests/Test 02/20261013_071127`, which preserves the latest waterfall component archive, masks, contours, optical-flow diagnostics, viewer, and decoded reconstruction evidence.
- `Tests/Test 13I`, `13J/13K`, `13J2/13N`, and `13P`, which establish the accepted bounded native payload/archive and reader/compositor/playback-loop chain.
- `Tests/Test 14B`, `14C`, `14D`, and `14F`, which consolidate the V2 read-only archive reader, WebP decode adapter, playback-loop dry run, and integrated bounded prototype package.
- Pre-GitHub package runs for source-frame AMCF encoding, physical carrier planning, virtual reader recovery/export, and mechanical/optical simulation.

## Main Mapping

| Local file | Public file | Status |
| --- | --- | --- |
| `Main/amcf_test02.py` | `src/amcf_local_main_test02.py` | exact code |
| `Main/amcf_vnext.py` | `src/amcf_vnext.py` | exact code |
| `Main/test_archive_decode.py` | `src/amcf_local_main_archive_decode_check.py` | exact code |
| `Main/amcf_tracking_test03a.py` | `src/amcf_local_main_tracking_test03a.py` | public-safe adaptation / review |

The `amcf_tracking_test03a.py` difference is expected because the public file was adapted to discover a public-safe workspace root instead of depending on the original local path layout.

## V2 / 14F Package Mapping

The local `Test 14F_V2_INTEGRATED_BOUNDED_PROTOTYPE_PACKAGE` Python package is represented by public `src/amcf_v2/`.

- local Python files: 39
- public Python files: 39
- byte-identical Python files: 38
- one intentional public-safe difference: `decode/decode_pipeline.py`

The public difference hardens the Pillow import so the package fails gracefully when optional image support is unavailable. This is a public-safe dependency handling improvement, not a missing feature.

## Progression Group Status

| Group | Status | Public coverage | Next action |
| --- | --- | --- | --- |
| `local_main_core` | `IN_GITHUB_EXACT_OR_PUBLIC_SAFE_PORT` | `src/amcf_local_main_test02.py`, `src/amcf_vnext.py`, `src/amcf_local_main_archive_decode_check.py`, `src/amcf_local_main_tracking_test03a.py`, public docs | Keep exact/adapted mappings tested. |
| `test02_latest_diagnostic_archive` | `TARGETED_DIAGNOSTIC_VIEWER_PARITY_PORTED` | component-event archive, basic viewer, quality metrics, optical-flow tracking, local-main Test02 source, and `src/amcf_test02_diagnostic_viewer.py` | Continue newest-to-oldest review for other accepted diagnostics and reject older failed methods unless later runs reused them. |
| `pre_github_source_to_amcf` | `IN_GITHUB_EQUIVALENT_PORT` | digital encoder, validator, source-frame demo and tests | Keep source-frame archive path tested. |
| `pre_github_physical_carrier_reader` | `IN_GITHUB_EQUIVALENT_PORT` | physical carrier, virtual reader, demos and tests | Keep no-hardware carrier/reader path tested. |
| `level5_main_promotion` | `IN_GITHUB_EXACT_CODE` | `src/amcf_vnext.py` | Keep semantic/object Level 5 separate from physical hardware Level 5. |
| `native_payload_13i_13j_13j2_13p` | `LOCAL_ACCEPTED_EVIDENCE_COVERED_BY_PUBLIC_V2` | `src/amcf_v2/` plus V2 demo/tests/doc | Keep as accepted local evidence feeding the public V2 package; do not bulk-copy generated archives. |
| `v2_14b_14c_14d_14f_package` | `IN_GITHUB_EXACT_CODE_WITH_PUBLIC_SAFE_DIFF` | `src/amcf_v2/` plus V2 demo/tests/doc | Preserve the V2 package and document the one dependency-hardening diff. |
| `benchmark_consolidation_13m` | `EVIDENCE_ONLY_NOT_BULK_PORT_TARGET` | parity docs and ledgers | Extract decision evidence only; do not copy generated/imported benchmark evidence wholesale. |
| `canonical_physical_boundary` | `IN_GITHUB_DOCS_AND_PHYSICAL_BRANCH` | canonical docs and physical-player docs | Keep physical robustness work separate from digital AMCF parity closeout. |

## Immediate Gap

The first highest-priority fullness gap was diagnostic/viewer parity around the latest `Test 02` evidence. The state-to-event integration is now present in `Main`, and the maintained profile bundle now has runnable 03M, 08E, 10A/10B, 12D, and 12E audit paths. Remaining gaps are claim-specific rather than an absent renderer:

- masks
- contours
- optical-flow diagnostics
- source-specific track taxonomy
- contour-overlay viewer behavior
- `tracking_diagnostics` output conventions and confirmation of any particular semantic person track

Public GitHub already contained exact or equivalent core code for much of this. `AMCF_TEST02_DIAGNOSTIC_VIEWER_PARITY_PORT_V1` adds the reusable diagnostic viewer contract for track taxonomy, contours, update reasons, motion metric cards, same-clock comparison/difference hooks, and frame-data export. `AMCF_DIAGNOSTIC_PROFILE_BUNDLE_COMPLETION_V1` now adds the normalized state handoff used by Main's component-event encoder, with explicit status for 03M, 08E, 10A/10B, 12E, and HOOT rather than silently treating one profile as another.

The integrated state path is intentionally narrow and honest:

- Test 02 polygon contours drive masked component events.
- An exact residual event closes every changed pixel outside those masks.
- 03M camera-compensated zone motion is recorded as a diagnostic measurement, not as segmentation geometry.
- 08E heat/diff behavior is recorded with its Farneback/TURBO contract; a single-pair heat artifact is not presented as the full truth/decoded comparison.
- 10A/10B crop review and 12D/12E proxy taxonomy are runnable review diagnostics; proxy boxes are not masks.
- HOOT remains a bounded dataset-annotated semantic proof and is not embedded as a universal claim.

The full 288-frame Main integration produced a source-independent decoded archive with 2,583 events and zero unsafe acceptances. That generated archive is intentionally evidence under `Main/output/`, not a source/release artifact, and its 209.6 MB size is not a compactness result.

Recommended next phase:

`AMCF_TESTS_NEWEST_TO_OLDEST_DEEP_REVIEW_CONTINUE_V1`

## Newest-To-Oldest Part Log

| Part | Folder range | Result | Public action |
| --- | --- | --- | --- |
| Part 1 | `Tests/Test 02/20261013_071127` | Source report, archive manifest, tracks manifest, and viewer code inspected. Missing diagnostic viewer contract found. | Ported `src/amcf_test02_diagnostic_viewer.py`, demo, tests, and `docs/AMCF_TEST02_DIAGNOSTIC_VIEWER_PARITY.md`. |
| Part 2 | Public prep, public assets, pre-public parity/license map, upload handoff, and final-confidence audit folders below Test 02 | Reports/status files/coverage matrices inspected. These folders are package/readiness evidence already represented by current public repo files. | Added `docs/AMCF_TESTS_NEWEST_TO_OLDEST_PART2_PUBLIC_PREP_REVIEW.md`; no runtime code port needed. |
| Part 3 | Pre-GitHub source-frame to AMCF, physical carrier, virtual reader recovery/export, and mechanical/optical simulator folders | Source/demo/test files compared against the latest combined pre-GitHub clean package. Public physical-carrier and virtual-reader files are byte-identical; public encoder/validator and mechanical player are newer supersets. Matching public demos passed. | Added `docs/AMCF_TESTS_NEWEST_TO_OLDEST_PART3_PRE_GITHUB_FUNCTIONAL_PATHS_REVIEW.md`; no runtime code port needed. |
| Part 4 | Pre-GitHub full functional coverage audit, physical analog/player concept correction docs, clean package prep, and release readiness audit | Historical audits/status files and clean-package source compared. The older Path A missing finding was resolved by later Part 3 source-frame AMCF work. `amcf_virtual_hardware.py`, `amcf_vnext.py`, and the virtual-hardware demo are byte-identical; current public docs are newer supersets. | Added `docs/AMCF_TESTS_NEWEST_TO_OLDEST_PART4_PRE_GITHUB_AUDIT_AND_CONCEPT_REVIEW.md`; no runtime code port needed. |
| Part 5 | Virtual hardware release refresh, player UI state viewer stub, virtual reader main integration, software virtual reader emulator, visual-stage closeout, and player UI concept folders | Virtual hardware code was already consolidated in public. The player UI static viewer existed, but the accepted JSON normalizer and Markdown report diagnostic helper were missing as reusable public source. | Ported `src/amcf_player_ui_state.py`, demo, tests, and `docs/AMCF_PLAYER_UI_STATE_DIAGNOSTIC_PARITY.md`; added `docs/AMCF_TESTS_NEWEST_TO_OLDEST_PART5_VIRTUAL_HARDWARE_PLAYER_UI_REVIEW.md`. |
| Part 6 | Dummy carrier transport, motor/encoder transport, bench sensor, CIS/scan-gate, physical device layout, and material-coupon scan planning folders | Most folders are future physical planning evidence with no hardware proof. The material-coupon run contained a reusable software-only analyzer for synthetic/scanned coupon images. | Ported `src/amcf_material_coupon_analysis.py`, demo, tests, and `docs/AMCF_MATERIAL_COUPON_ANALYSIS_PARITY.md`; added `docs/AMCF_TESTS_NEWEST_TO_OLDEST_PART6_PHYSICAL_TRANSPORT_SENSOR_REVIEW.md`. |
| Part 7 | Physical pre-prototype, integrated transport/scan-gate, detailed scan-gate, indexed feed, transport actuation, non-ideal physical carrier, canonical concept, vertical-stack, physical-medium, and single-app layout folders | Most folders are generated planning/simulation evidence, not maintained source. The accepted reusable behavior is the no-hardware physical-medium simulation summary for vertical-stack equivalence, ideal sequential carrier equivalence, non-ideal recovery, control-event diagnostics, and claim-boundary safety. | Ported `src/amcf_physical_medium_simulation.py`, demo, tests, and `docs/AMCF_PHYSICAL_MEDIUM_SIMULATION_PARITY.md`; added `docs/AMCF_TESTS_NEWEST_TO_OLDEST_PART7_PHYSICAL_MEDIUM_SIMULATION_REVIEW.md`. |
| Part 8 | Level 5 promotion, HOOT real-world lost/recovered proof, controlled lost/recovered proof, deep semantic bridge/mask/track runs, tool survey, and Tower Bridge proxy runs | The accepted timeline is controlled canonical semantic/object Level 5 plus HOOT dataset-annotated semantic/object Level 5. Earlier deep-tool and mask/track runs remain important progress but not accepted Level 5. This is digital/semantic proof only, not physical hardware proof. | Ported `src/amcf_semantic_level5_proof.py`, demo, tests, and `docs/AMCF_SEMANTIC_LEVEL5_PROOF_PARITY.md`; added `docs/AMCF_TESTS_NEWEST_TO_OLDEST_PART8_SEMANTIC_LEVEL5_REVIEW.md`. |
| Part 9 | Release candidate signoff, lightweight release package, autonomous roadmap executor, archive writer/reader integration, viewer/runtime polish, acceptance harness, canonical vector/validator, runtime-validator spec, post-Level-5 roadmap, and Level 5 gap-closure folders | Existing public modules already cover archive writer/reader and vnext surfaces. The missing reusable piece was the release-candidate acceptance timeline: 9 valid vectors passed, 9 invalid vectors rejected, 6 tiny archive fixtures, claim-boundary tests passed, and generated ZIPs not ported. | Ported `src/amcf_release_candidate_acceptance.py`, demo, tests, and `docs/AMCF_RELEASE_CANDIDATE_ACCEPTANCE_PARITY.md`; added `docs/AMCF_TESTS_NEWEST_TO_OLDEST_PART9_RELEASE_CANDIDATE_ACCEPTANCE_REVIEW.md`. |
| Part 10 | Older semantic continuity, source-anchored solver, machine-reviewed/machine-validated semantic object advancement, semantic micro-test, mask review, native playback, and roadmap closeout folders | These folders show progression toward semantic/object proof but mostly keep solved flags false and are superseded by later accepted proof vectors. The useful reusable behavior is semantic sidecar overlay and validation diagnostics from the micro-test path. | Ported `src/amcf_semantic_sidecar_overlay.py`, demo, tests, and `docs/AMCF_SEMANTIC_SIDECAR_OVERLAY_PARITY.md`; added `docs/AMCF_TESTS_NEWEST_TO_OLDEST_PART10_SEMANTIC_PROGRESSION_REVIEW.md`. |
| Part 11 | V2/native archive chain from 14J back through 13F: WebP demo codec sidecar, external review package, larger bounded V2 generalisation, component-delta investigations, V2 package, playback dry run, WebP decode adapter, read-only archive reader, native codec/player architecture, 13M closeout, native payload feasibility, and native reader/compositor progression | Public `src/amcf_v2/` already represents the 14F V2 package surface. The missing reusable piece was the 14J metadata sidecar reader contract that keeps WebP as bounded demo payload while carrying component/proxy-region metadata and safe claim flags. | Ported `src/amcf_v2_sidecar_metadata.py`, demo, tests, and `docs/AMCF_V2_SIDECAR_METADATA_PARITY.md`; added `docs/AMCF_TESTS_NEWEST_TO_OLDEST_PART11_V2_NATIVE_ARCHIVE_REVIEW.md`. |
| Part 12 | Runtime/archive optimisation and manual semantic-review band from 13C3 through 08B/08C/08D | 13C2/13E contained a reusable external decode/seek index and indexed playback reader planning contract. The 12* manual review/mask folders are important progression evidence but explicitly kept semantic-object solved false and human review required. | Ported `src/amcf_playback_index_planner.py`, demo, tests, and `docs/AMCF_PLAYBACK_INDEX_PLANNER_PARITY.md`; added `docs/AMCF_TESTS_NEWEST_TO_OLDEST_PART12_RUNTIME_OPTIMISATION_REVIEW.md`. |
| Part 13 | Residual compression, decoded-MP4, v0 archive, visual fidelity and component gates from 07I through 03U | 07E proved residual-stream reduction against a full-rate component estimate; 07I retained human review. Older 05C fallback and 03X partial results are progression evidence. Main did not integrate the 07E runner, while public v0 tooling covers the archive toolchain. | Ported `src/amcf_residual_visual_acceptance.py`, demo, tests, and `docs/AMCF_RESIDUAL_VISUAL_ACCEPTANCE_PARITY.md`; added `docs/AMCF_TESTS_NEWEST_TO_OLDEST_PART13_RESIDUAL_VISUAL_REVIEW.md`. Full 07E codec parity remains unproven. |
| Part 14 | Every top-level folder from `Test 03T` through `Test 03A` (20 folders); next: `Test 02`, then `Legacy Test 01` | 03A/03B failed tracking, 03C-03G passed bounded diagnostics, 03M produced the camera-compensated zone-motion diagnostic, and 03T remained partial at 100% measured current-frame support. Later 03V/03Y visual selections supersede flawed earlier candidates. Only 03A's bounded tracker was represented in `Main`. | Ported `src/amcf_motion_truth_diagnostics.py`, demo, tests, and `docs/AMCF_MOTION_TRUTH_DIAGNOSTICS_PARITY.md`; added the 20-folder `docs/AMCF_TESTS_NEWEST_TO_OLDEST_PART14_03A_TO_03T_REVIEW.md`. Full per-script and media parity remains open. |
| Part 15 | All eight dated `Test 02` runs and `Legacy Test 01/AMCF_Waterfall_Test_01`; oldest named folders in descending order | Public Test 02 code matches `Main`, all eight local archives pass public inspection, and public archive-only decoding reproduces local state hashes for both the latest four-frame and original 288-frame runs. Test 02 still fails final fidelity acceptance; the earlier fixed-tile Legacy Test 01 also failed its quality-equivalent compression goal. | Added `docs/AMCF_TESTS_NEWEST_TO_OLDEST_PART15_TEST02_LEGACY_REVIEW.md`; all 618 Test 02 files and all 10 Legacy Test 01 files now have documented file-level accounting. No runtime port. |
| Part 16 | `Test 05B` through `Test 05C6_06F` (5,178 files) | Component extraction/compositor, fallback decoders, parallax/tracking, accepted 05C4 full-rate visual control, rejected adaptive reductions, and 05C6 freeze were inspected from source runners and reports. | Added `docs/AMCF_TESTS_FILE_REVIEW_05B_TO_06F_EARLY_V0_PROGRESSION.md`; public v0/v2/archive/visual/diagnostic layers cover reusable contracts, while historical waterfall runners and generated media remain local evidence. |
| Part 17 | `Test 03U` through `Test 04F_05A` (1,106 files) | 03U numerical support pass was overturned by 03V visual review; 03W safe swaps, 03X fidelity checks, 03Y watchable/parallax baseline, 03Z consolidation, and 04A-04F/05A archive/viewer/toolchain hardening were inspected. | Added `docs/AMCF_TESTS_FILE_REVIEW_03U_TO_04F_05A_V0_CONSOLIDATION.md`; public v0 toolchain and visual/report contracts cover reusable behavior without copying source-specific media or rejected candidates. |
| Part 18 | `Test 03T` through `Test 03A` exact inventory (1,162 files) | Every nested file was enumerated by type; all 22 Python source files were identified and symbol-inspected. The band covers failed deep tracking, bounded diagnostics, motion/zone analysis, map preparation, and visual/support experiments with selective later promotion. | Added `docs/AMCF_TESTS_FILE_REVIEW_03A_TO_03T_EXACT_INVENTORY.md`; public motion diagnostics and claim-safe metrics are represented, while source-specific maps, media, and failed/rejected runners remain local evidence. |
| Part 20 | 52 top-level `Tests` folders that were only covered indirectly by range or semantic-group wording | Each exact folder name was reconciled to its source/status evidence and public disposition. The set divides into consolidated public behavior, historical/rejected semantic work, planning/provenance, and generated evidence. | Added `docs/AMCF_TESTS_TOP_LEVEL_FOLDER_RECONCILIATION.md`; no runtime code port in this bookkeeping pass. |
| Part 19 | `Test 13M_FINAL_BENCHMARK_VALIDATION_SPEC`, `Test 13M_FIX_13Q_13R_12K_GATE_CLOSEOUT`, and `Test AMCF_SOFTWARE_VIRTUAL_PHYSICAL_READER_EMULATOR` | 13M acceptance records were inspected as bounded research-prototype/spec evidence with explicit unresolved production/full-native flags. The 36-file software virtual-reader emulator was compared by source concepts and is consolidated in the richer public virtual-hardware/virtual-carrier modules. | Added `docs/AMCF_TESTS_FILE_REVIEW_TEST13M_AND_SOFTWARE_READER_EMULATOR.md`; no runtime code port needed. |
| Part 21 | `Test 03M`, `Test 08E`, `Test 10A_10B`, and reviewed `Test 12E` diagnostic contracts | The accepted 03M camera-compensated zone map, 08E `Stay Here for 13 Seconds` heat behavior, and later 12E conservative/narrow proxy review were rerun from their real inputs. The reference repositories supplied OpenCV/tracking primitives but not these AMCF-specific contracts. | Ported `src/amcf_diagnostic_profiles.py`, `demo/run_amcf_diagnostic_profiles.py`, focused tests, and the unified Main seven-zone/full-video diagnostic path. Generated evidence remains outside source/release files; semantic object solving remains unclaimed. |
| Part 22 | Diagnostic state bridge and 15-Oct Main acceptance follow-up | Normalized Test 02 track/mask/contour state now crosses into Main's component-event encoder. The archive retains all logical frame progression through contour-backed events plus exact residual closure, while the 03M/08E/10A-10B/12E/HOOT contracts remain explicitly classified. | Added `src/amcf_diagnostic_state.py`, integrated `amcf_component_event_archive.py` and the unified acceptance runner, focused tests, and this state/claim-boundary record. Full exact frame closure passes; compact size remains a separate research track. |
| Part 23 | 20-Oct diagnostic family completion and proxy-direction audit | The complete 03M motion-truth family, 08E heat/diff, 10A/10B crop review, 12D calibrated proxy, and 12E reviewed proxy all rendered successfully through Main. Temporal proxy boxes are implemented, but the reviewed evidence has zero leftward person tracks; the confirmed person/object positive moves slightly right. | Added the full 03M family renderer and coverage audit output under `Main/output/amcf_diagnostic_coverage_audit_20261020_full/`; added explicit right-to-left claim boundary. No generated media is a release source artifact. |

## What Not To Copy

- generated videos, generated archives, raw frame dumps, caches, or local output folders
- local absolute paths
- third-party reference repositories without separate license/provenance decisions
- physical robustness experiments as a substitute for digital AMCF parity closeout

