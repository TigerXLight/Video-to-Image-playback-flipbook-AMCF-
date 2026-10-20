# AMCF Test 02 Diagnostic Viewer Parity

Run context: `AMCF_TEST02_DIAGNOSTIC_VIEWER_PARITY_PORT_V1`

This document records the first newest-to-oldest local `Tests` folder parity repair after the progression ledger. It focuses on `Tests/Test 02/20261013_071127`, which is the newest local evidence folder and contains the diagnostic surface around object-bound masks, contours, track IDs, parent/child labels, optical-flow metrics, update reasons, same-clock comparison playback, and viewer overlays.

## Boundary

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- real printer integration claimed: false
- real scanner integration claimed: false
- real player hardware claimed: false
- unsafe_acceptance_count: 0

## Source Reading

`Tests/Test 02/20261013_071127/TEST02_REPORT.md` says Test 02 is a fail for final AMCF acceptance, but it demonstrates useful local functionality:

- persistent per-frame object-bound masks
- contours in `tracks_manifest.json`
- track IDs and object-relative labels
- parent/child taxonomy for the waterfall and spray/tree/branch groups
- optical-flow motion metrics
- component update reasons
- self-contained component archive/decode evidence
- a synchronized viewer with contour overlays and a difference toggle

This means Test 02 must not be treated as the final accepted AMCF pipeline, but its diagnostic behavior must not be lost from the public repo.

## Public Gap Found

Before this parity repair, the public repo already had component-event archive, decode, quality, optical-flow, and a basic static component viewer. The basic viewer did not preserve the Test 02 diagnostic viewer contract:

- frame-indexed contour overlays
- focus filtering by track ID
- parent/child track taxonomy summary
- motion metric cards
- update reason display
- same-clock comparison/difference video hooks
- frame-data export

The public optical-flow report also used a generic `global_changed_region` track. That is useful for fixture tests, but it is not the same as the source-specific Test 02 waterfall taxonomy.

## Added Public Surface

The public repo now includes:

- `src/amcf_test02_diagnostic_viewer.py`
- `demo/run_amcf_test02_diagnostic_viewer_demo.py`
- `tests/test_amcf_test02_diagnostic_viewer.py`

The new module does not copy local generated media or raw output. It preserves the reusable diagnostic contract:

- load and validate a Test 02 style track manifest
- summarize track taxonomy and update counts
- preserve parent/child relationships
- preserve contour and motion metric expectations
- build a static same-clock diagnostic viewer scaffold
- keep claim-boundary flags false

## What Is Still Not Claimed

This repair does not make Test 02 the final AMCF acceptance proof. The local report itself says Test 02 failed final AMCF acceptance because native-resolution reconstruction fidelity was not good enough compared with conventional AV1.

This repair also does not claim byte-for-byte generated media parity, real hardware validation, final UI readiness, or physical Level 5 completion.

## Next Procedural Step

Continue the newest-to-oldest pass using real source reading and validation. The next folders to inspect should come from the latest `Tests` ordering and the transcript summary, while avoiding rejected historical methods unless a later accepted run reused their code or logic.
