# AMCF Tests Newest-To-Oldest Part 15: Test 02 and Legacy Test 01

This part covers the last two named folders in the descending `Tests` review. `Test 02` has eight dated runs; `Legacy Test 01` has one prototype folder. The transcript summary and the runs' own verdicts determine which behavior is useful and which older method must not be promoted as a final AMCF implementation. Reaching the oldest folder is not proof that every top-level folder, nested file, or generated output was reviewed; see `docs/AMCF_TESTS_FILE_LEVEL_COVERAGE_BASELINE.md`.

| Local folder | Source/result | `Main` and public mapping |
| --- | --- | --- |
| `Test 02/20261013_071127` | Latest four-frame rerun; 8 tracks, 9 component events, synchronized diagnostic viewer; final AMCF acceptance: FAIL. | `Main/amcf_test02.py` is byte-identical to public `src/amcf_local_main_test02.py`; public `src/amcf_test02_diagnostic_viewer.py` covers the reusable viewer contract. |
| `Test 02/20261013_061205` | Four-frame rerun with the same tracks, quality metrics, and viewer HTML as the latest rerun. | Same public code path; not an additional accepted implementation. |
| `Test 02/20261013_060131` | Same bounded four-frame evidence. | Same public code path. |
| `Test 02/20261013_055937` | Same bounded four-frame evidence. | Same public code path. |
| `Test 02/20261013_054829` | Same bounded four-frame evidence. | Same public code path. |
| `Test 02/20261013_023556` | Same bounded four-frame evidence. | Same public code path. |
| `Test 02/20261013_023117` | Earliest of the seven four-frame reruns; same bounded evidence. | Same public code path. |
| `Test 02/20261003_165701` | Original 288-frame native-resolution run; masks, contours, eight tracks, optical-flow diagnostics, 213 component patch events, self-contained archive and archive-only decoder. Final AMCF acceptance: FAIL. | `Main/amcf_test02.py` and `Main/test_archive_decode.py` are represented in public as `src/amcf_local_main_test02.py` and `src/amcf_local_main_archive_decode_check.py`. The diagnostic viewer was added in Part 1. |
| `Legacy Test 01/AMCF_Waterfall_Test_01` | 288-frame, 120-region WebP tile prototype with independent update events, archived AAC, archive-only decode, and intermediate frame-hash checks. Its own verdict is **working mechanism / failed quality-equivalent compression test**. | Not integrated into `Main` as selected code. Public component-event work is not a byte-identical copy of this older algorithm; do not restore its fixed tile scheduler as final AMCF behavior. |

## Concrete Checks

- The seven short Test 02 runs each contain four frames. Their track manifests, quality metrics, and viewer HTML match by SHA-256; their generated ZIPs and run metadata need not match byte-for-byte.
- The public archive-inspection helper accepted all eight local Test 02 archives.
- The public diagnostic-viewer loader read the full run and representative short runs. The full run reported 8 tracks, 2,304 contour track-frames, 213 component update events, parent/child taxonomy, motion metrics, and `unsafe_acceptance_count: 0`. The short runs reported 8 tracks, 32 contour track-frames, 9 events, and zero unsafe acceptance.
- The public archive-only decoder reconstructed the latest four-frame archive and the original 288-frame archive. In both cases, `decoded_state_hashes.txt` matched the local run exactly. The generated four-frame and 288-frame videos remained under ignored `output/`, not in Git.
- The original full Test 02 archive was 4,338,023 bytes against an 11,661,942-byte source, but reconstruction measured only 18.244 dB PSNR and 0.3946 sampled SSIM, while its AV1 control measured 40.817 dB and 0.9915. The later short reruns measured 35.815 dB and 0.9765 over only four frames; they do not reverse the full-run FAIL verdict.
- Legacy Test 01 measured 9,376 update events and an 8,206,510-byte archive at 960x480; its own report identifies a failed same-fidelity compression comparison and motion freezing. It is a historical stepping stone, not a selected implementation.

## Progression Decision

Legacy Test 01 established an archive/decode mechanism but failed quality-equivalent compression. Test 02 replaced the static tile idea with per-frame component masks, track IDs, optical-flow diagnostics, and a synchronized comparison viewer, yet also failed final fidelity acceptance. Later local experiments and accepted package work must govern public feature selection; an older run's working mechanism is not evidence that its rejected quality result was solved.

This part adds no runtime code. Public Test 02 behavior needed for this comparison is already represented, including its diagnostic contract. Full local-workspace parity remains open: the folder summaries do not dispose of every nested file. The next work should use the file-level inventory to close those gaps with evidence and tests, not restart either failed Test 01 or Test 02 strategy.

Generated output committed: no. Unsafe acceptance count in checked diagnostic reports: 0. Hardware validation claimed: false. Physical Level 5 claimed: false. Manufactured player claimed: false.
