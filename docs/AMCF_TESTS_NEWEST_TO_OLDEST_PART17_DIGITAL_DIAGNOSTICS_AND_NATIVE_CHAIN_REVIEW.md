# AMCF Tests Newest-to-Oldest Part 17: Digital Diagnostics and Native Chain Review

Run context: `AMCF_FULL_LOCAL_WORKSPACE_PARITY_GROUP_LEDGER_V1`

This review covers the next evidence slice after the bounded V2/native closeout review:

- `Tests/Test 02/20261013_071127`
- `Tests/Test 13F_NATIVE_READER_COMPOSITOR_SKELETON`
- `Tests/Test 13G_NATIVE_COMPOSITOR_FRAME_RECONSTRUCTION`
- `Tests/Test 13H_NATIVE_RESIDUAL_COMPONENT_DECODER_INVESTIGATION`
- `Tests/Test 13I_REAL_NATIVE_PAYLOAD_ARCHIVE`
- `Tests/Test 13J_13K_NATIVE_READER_COMPOSITOR_INTEGRATION`
- `Tests/Test 13J2_13N_LONGER_NATIVE_ARCHIVE_SAMPLE`
- `Tests/Test 13D_13L_RESIDUAL_KEYFRAME_SCHEDULING_OPTIMISATION`
- `Tests/Test 13D2_13O_SPARSE_RESIDUAL_PAYLOAD_OPTIMISATION`
- `Tests/Test 13P_NATIVE_PAYLOAD_CODEC_FEASIBILITY`
- `Tests/Test 13M_FINAL_BENCHMARK_VALIDATION_SPEC`
- `Tests/Test 13M_FIX_13Q_13R_12K_GATE_CLOSEOUT`

The review uses source files and closeout reports as evidence. Generated archives, videos, image sheets, private media, and run folders are not copied into the public repository.

## Part 17 Result

**Status: REVIEWED. No missing accepted digital runtime behavior was found in this slice.**

The public repository already contains tested public-safe representations of the accepted bounded behavior:

| Local behavior | Public representation | Status |
| --- | --- | --- |
| Test 02 track taxonomy, contours, parent/child labels, update reasons, motion metrics | `src/amcf_test02_diagnostic_viewer.py`, its demo, and `tests/test_amcf_test02_diagnostic_viewer.py` | PORTED / TESTED |
| Native archive reader and manifest/index loading | `src/amcf_v2/container/` and `src/amcf_v2/decode/` | PORTED / TESTED |
| Native payload decode and frame reconstruction | `src/amcf_v2/codecs/`, `src/amcf_v2/decode/`, and public V2 tests | PORTED / TESTED for bounded fixtures |
| Reader -> decoder -> compositor -> playback loop | `src/amcf_v2/compositor/` and `src/amcf_v2/playback/` | PORTED / TESTED for bounded fixtures |
| Bounded 48-frame native sample | `src/amcf_v2_14h_archive.py` and its demo/test | PORTED / TESTED |
| WebP-lossless payload feasibility | `src/amcf_v2/codecs/webp_lossless.py` and V2 codec registry | PORTED / TESTED where Pillow is available; graceful fallback remains explicit |
| Sparse residual and keyframe experiments | V2 bounded codec/decode contracts and archive tests | ACCEPTED BOUNDED CONTRACT REPRESENTED; historical benchmark scripts not copied |
| 13M/13M-fix closeout status and limitations | public V2/archive/review docs | DOCUMENTED; generated closeout packages excluded |

## Test 02 Diagnostic Findings

The latest Test 02 evidence is useful diagnostics, but its own report is not final AMCF acceptance. The local evidence includes:

- persistent per-frame masks and contours;
- track IDs and parent/child taxonomy;
- component update reasons;
- optical-flow motion metrics;
- same-clock comparison and difference-video hooks;
- frame-data export and a static viewer.

The public diagnostic module preserves those reusable contracts using a small synthetic manifest in tests. The public demo passed with:

- `final_passed: true`;
- parent/child taxonomy present;
- motion metrics present;
- contour frames present;
- `unsafe_acceptance_count: 0`;
- hardware, physical Level 5, manufactured-player, and final-UI claims false.

This does not claim that the generated Test 02 waterfall media or its failed final-fidelity verdict has been promoted as an accepted AMCF codec.

## Native Chain Findings

The local 13M records distinguish bounded prototype readiness from production/full-video claims. The public mapping preserves that distinction:

- 13I real native payload archive: represented for bounded samples;
- 13J/13K reader, decoder, compositor, playback loop: represented for bounded samples;
- 13J2/13N longer 48-frame sample: represented and tested;
- 13D/13L and 13D2/13O residual/keyframe experiments: represented as bounded codec/decode contracts, not as a claim that general compression is solved;
- 13P WebP-lossless feasibility: represented as an optional codec path with explicit dependency handling;
- 13M and 13M-fix: closeout status and limitations are preserved.

The local closeout still marks these as not solved in the stricter production sense:

- full-video native AMCF archive;
- final production playback engine;
- general native payload compression;
- stage-4 temporal scheduling;
- semantic/object AMCF completion.

Those are not missing accepted bounded playback features. They are explicit future or non-claimed boundaries and must not be silently upgraded by copying historical experiment folders.

## Duplication and Port Decision

No duplicate native player package is added in Part 17. The public `src/amcf_v2/` package already provides the coherent bounded archive/decode/compositor/playback surface. The many local `imported_*`, `native_archives`, regression-runner, and generated-output copies are historical evidence or fixtures, not additional public runtime modules.

No new external dependency is added. Pillow/OpenCV/NumPy/FFmpeg remain optional or environment-detected in the existing public layers; no hardware or GUI path is introduced.

## Validation

Focused validation completed:

```text
python -m unittest tests.test_amcf_test02_diagnostic_viewer
Ran 4 tests ... OK

python demo/run_amcf_test02_diagnostic_viewer_demo.py
final_passed: true
unsafe_acceptance_count: 0
```

The full public suite remains green at `500` tests from the preceding parity checkpoint. Generated output remains under `output/` and is not committed.

## Claim Boundary

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- real motors/sensors/cartridges validated: false
- real printer/scanner/player integration claimed: false
- generated output committed: false
- unsafe acceptance count: `0` in the reviewed public diagnostic path

## Next Slice

Continue the newest-to-oldest review with the remaining older AMCF-owned groups, beginning with the 12B–12J semantic/diagnostic progression and then the older 05–11 archive/compositor progression where the current public V0/V2 surfaces need explicit file-level disposition. Do not copy rejected semantic experiments or generated evidence unless a later accepted public behavior requires a narrow, tested adapter.
