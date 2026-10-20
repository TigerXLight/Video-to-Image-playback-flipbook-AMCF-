# AMCF Tests File Review: Test 02, 20261003_165701

This is the next bounded part of the newest-to-oldest `Tests` file review. The inspected run has **275 files**. Its own `TEST02_REPORT.md` marks final AMCF acceptance **FAIL**; this review preserves the useful archive, tracking, and diagnostic mechanisms without presenting the rejected reconstruction quality as a final result.

Run `python demo/run_amcf_tests_folder_evidence.py "<workspace-root>/Tests/Test 02/20261003_165701" --output output/amcf_test02_288_file_review/evidence` after replacing `<workspace-root>` with the actual local path. The generated `file_evidence.jsonl` records the relative path, SHA-256, byte count, and format check for **each of the 275 files**. It stays under ignored `output/`. Its `semantic_disposition` deliberately remains `OPEN`; the decisions below require the separate run verdict, `Main` comparison, and public decode checks. The scanner does not prove parity on its own.

## Full File Accounting

| File set | Count | Check and disposition |
| --- | ---: | --- |
| `work/base.webp` and `work/events/*.webp` | 214 | Every image opened and verified; all are byte-identical to their respective members in the local AMCF archive. Generated payload evidence, not source to copy. |
| `baseline_quality/visual_comparisons/*.jpg` | 15 | Every image verified at 960x480: five source, five conventional-control reconstructions, five amplified differences. Generated comparison evidence. |
| `visual_comparisons/*.jpg` | 20 | Every image verified at 960x480: five source, five encoded reconstructions, five archive-state reconstructions, five amplified differences. The five source stills are exact duplicates of baseline source stills. Generated evidence. |
| `tracking_diagnostics/*.jpg` | 5 | Every image verified at 960x480; sampled frame 288 visually shows the labeled contour overlay. Generated diagnostic evidence. |
| Other individual files below | 21 | Parsed or byte-read as specified below. |
| **Total** | **275** | All relative paths appear individually in ignored `file_evidence.jsonl`; no read/format failures. |

The image verification checks file integrity/format, not visual correctness of every image. The report and representative source/reconstruction/overlay stills were inspected; this is not a frame-by-frame visual audit of all four videos.

| Relative file | Disposition and check |
| --- | --- |
| `archive_audio.m4a` | Generated AAC payload; FFprobe read it and it matches `work/audio.m4a`. |
| `archive_manifest_resolved.json` | Parsed; core fields match archived manifest, with resolved archive metadata. |
| `ARTIFACT_SHA256SUMS.txt` | Read; five present artifact hashes match. The listed deliverable ZIP is absent. |
| `baseline_conventional_av1_crf32.mp4` | Generated conventional control; SHA-256 matches list; FFprobe reports 288 AV1 frames and AAC. |
| `baseline_quality/quality_metrics.json` | Parsed; conventional 288-frame result: 40.817 dB PSNR, 0.9915 SSIM at the recorded scale. |
| `decoded_state_hashes.txt` | Read; all 288 RGB-state hashes were reproduced by public archive-only decoding. |
| `PROJECT_HIERARCHY_TEST02.txt` | Read; local hierarchy/provenance evidence with machine-local paths, not source to copy into public docs. |
| `quality_metrics.json` | Parsed; AMCF 288-frame result: 18.244 dB PSNR, 0.3946 SSIM at the recorded scale. |
| `reconstructed_from_amcf.mp4` | Generated decode video; SHA-256 matches list; FFprobe reports 288 H.264 frames and AAC. |
| `source_ffprobe.json` | Parsed; source has 288 AV1 frames and AAC. |
| `TEST02_REPORT.md` | Read; explicit final-acceptance FAIL verdict, eight named tracks and 213 component events. |
| `track_metrics.csv` | Parsed 2,304 track-frame rows. |
| `tracks_manifest.json` | Parsed 288 frames, eight tracks per frame; public diagnostic viewer accepted it with zero unsafe acceptance. |
| `viewer/comparison_difference.mp4` | Generated same-clock difference view; SHA-256 matches list; FFprobe reports 288 H.264 frames. |
| `viewer/comparison_sync.mp4` | Generated synchronized source/reconstruction view; SHA-256 matches list; FFprobe reports 288 H.264 frames. |
| `viewer/index.html` | Generated diagnostic viewer. Its reusable controls are represented by public `src/amcf_test02_diagnostic_viewer.py`, not by public Pages `site/index.html`. |
| `viewer/START_VIEWER.cmd` | Local launcher hardcodes a private Python installation path; do not copy. |
| `viewer/tracks_manifest.json` | Parsed; byte-identical duplicate of top-level `tracks_manifest.json`. |
| `waterfall_test02.amcf.zip` | ZIP CRC verified: 216 members. Its 215 payload members exactly match `work/`; the archived manifest parses equal to `work/manifest.json`. Public archive-only decode reproduced 288 state hashes. |
| `work/audio.m4a` | Generated AAC payload, exact archive member. |
| `work/manifest.json` | Parsed; 288 source frames, eight tracks, 213 events; same object as archived manifest. |

## Main and Public Comparison

- Local `Main/amcf_test02.py` is byte-identical to public `src/amcf_local_main_test02.py`. Local `Main/test_archive_decode.py` is byte-identical to public `src/amcf_local_main_archive_decode_check.py`. This run folder itself has no `.py` source file to port.
- Public archive-only decoding of this local ZIP reconstructed 288 states under ignored `output/amcf_test02_288_file_review/`. Every state SHA-256 matched `decoded_state_hashes.txt`. The public diagnostic viewer generator accepted the actual 288-frame track manifest, reported eight tracks and `unsafe_acceptance_count: 0`.
- The source MP4 exists outside the run and matches the report's SHA-256 `4c44c01e3a82d6246794676b81b31d25ee2e2150b9dd162ffb7ad9642adac81d`. The archived payload is below that source's byte size, but its severe reconstruction-quality deficit remains the controlling verdict. The late reconstructed still visibly contains block/region artifacts against the source still.
- The run's `decoded_frames/` directory is empty. The checksum list names an absent `AMCF_Test02_Deliverables_20261003_170352.zip`; this is missing local deliverable evidence, not evidence of missing accepted GitHub source code.

## Decision

All 275 files in this run have a file-level hash/format record and a group or individual evidence disposition above. No new `Main` or public source port is justified from this failed-fidelity Test 02 output. This is a complete **file accounting for this run**, not full visual, performance, or project-workspace parity. Continue with the next older folder in the ordered `Tests` review, then inspect other workspace roots before any final `Main`/GitHub completeness claim.

Generated output committed: no. Hardware validation, physical Level 5, and manufactured player claimed: false.
