# AMCF Tests File Review: Test 02, 20261013_071127

This is one bounded, file-level part of the newest-to-oldest local `Tests` review. Scope: all 49 files under `<workspace-root>/Tests/Test 02/20261013_071127` in the inspected filesystem snapshot, plus a complete path/hash comparison of the six older `20261013_*` short reruns (343 files total). The folders contain generated evidence, not their own source module. Their generating code is represented by local `Main/amcf_test02.py` and the exact public `src/amcf_local_main_test02.py`; the public diagnostic viewer generator is `src/amcf_test02_diagnostic_viewer.py`. Each run's own verdict is **FAIL for final AMCF acceptance**, so none should be promoted as a successful final codec.

## Checks Performed

- Enumerated and SHA-256-read every one of the 49 files. Parsed every JSON/CSV/text file; verified every JPEG/WebP with Pillow; checked ZIP integrity and every member. FFprobe read all four MP4 files and both M4A files. Visually inspected the tracking overlay, reconstructed still, and amplified difference still. This is not a frame-by-frame visual review of every video or still.
- Source MP4 exists outside this run and matches the report's SHA-256 `4c44c01e3a82d6246794676b81b31d25ee2e2150b9dd162ffb7ad9642adac81d`.
- The 12 ZIP members pass integrity checking. Eleven payload members are byte-identical to their `work/` counterparts; the archived manifest parses to the same object as `work/manifest.json`. `archive_audio.m4a` and `work/audio.m4a` match; the two track manifests match.
- The manifest has four source frames, eight tracks, and nine patch events. The track manifest has four frames and 32 track rows, matching the 32 CSV rows. Public archive-only decoding reproduced all four local `decoded_state_hashes.txt` values under ignored `output/amcf_test02_latest_full_file_review/`.
- FFprobe: conventional AV1 baseline 288 frames; AMCF reconstruction four encoded frames; both containers last about 12.1 seconds and include AAC. The two viewer comparison videos have 288 frames at 1920x480. The viewer's 288-frame media is not proof of 288 decoded AMCF states in this run.
- The reported four-frame AMCF score is 35.815 dB PSNR / 0.9765 SSIM at the stated analysis scale; the 288-frame conventional control is 40.817 dB / 0.9915. Different frame counts limit any direct general-performance conclusion.

`EVIDENCE` below means generated local output, not source to copy. `ARCHIVE_EXACT` means the file is represented byte-for-byte inside the local archive, not committed to GitHub. `PUBLIC_TESTED` means the relevant public behavior was exercised against this local archive or manifest. No generated media or private path is a port target.

## Every File

| Relative file | Disposition | Evidence / public comparison |
| --- | --- | --- |
| `archive_audio.m4a` | EVIDENCE | AAC; exact duplicate of `work/audio.m4a` and archive member. |
| `archive_manifest_resolved.json` | EVIDENCE | Parsed; core manifest fields equal the archived manifest, plus resolved archive metadata. |
| `ARTIFACT_SHA256SUMS.txt` | EVIDENCE | Five present artifact hashes checked; a sixth listed deliverable ZIP is absent from this folder. |
| `baseline_conventional_av1_crf32.mp4` | EVIDENCE | SHA-256 matches checksum list; 288 AV1 frames and AAC, conventional control. |
| `baseline_quality/quality_metrics.json` | EVIDENCE | Parsed 288-frame conventional quality result. |
| `baseline_quality/visual_comparisons/diff_x5_frame_001.jpg` | EVIDENCE | JPEG verified, 960x480; conventional-control difference still. |
| `baseline_quality/visual_comparisons/diff_x5_frame_048.jpg` | EVIDENCE | JPEG verified, 960x480; conventional-control difference still. |
| `baseline_quality/visual_comparisons/diff_x5_frame_144.jpg` | EVIDENCE | JPEG verified, 960x480; conventional-control difference still. |
| `baseline_quality/visual_comparisons/diff_x5_frame_216.jpg` | EVIDENCE | JPEG verified, 960x480; conventional-control difference still. |
| `baseline_quality/visual_comparisons/diff_x5_frame_288.jpg` | EVIDENCE | JPEG verified, 960x480; conventional-control difference still. |
| `baseline_quality/visual_comparisons/recon_frame_001.jpg` | EVIDENCE | JPEG verified, 960x480; conventional-control reconstruction still. |
| `baseline_quality/visual_comparisons/recon_frame_048.jpg` | EVIDENCE | JPEG verified, 960x480; conventional-control reconstruction still. |
| `baseline_quality/visual_comparisons/recon_frame_144.jpg` | EVIDENCE | JPEG verified, 960x480; conventional-control reconstruction still. |
| `baseline_quality/visual_comparisons/recon_frame_216.jpg` | EVIDENCE | JPEG verified, 960x480; conventional-control reconstruction still. |
| `baseline_quality/visual_comparisons/recon_frame_288.jpg` | EVIDENCE | JPEG verified, 960x480; conventional-control reconstruction still. |
| `baseline_quality/visual_comparisons/source_frame_001.jpg` | EVIDENCE | JPEG verified, 960x480; source reference still. |
| `baseline_quality/visual_comparisons/source_frame_048.jpg` | EVIDENCE | JPEG verified, 960x480; source reference still. |
| `baseline_quality/visual_comparisons/source_frame_144.jpg` | EVIDENCE | JPEG verified, 960x480; source reference still. |
| `baseline_quality/visual_comparisons/source_frame_216.jpg` | EVIDENCE | JPEG verified, 960x480; source reference still. |
| `baseline_quality/visual_comparisons/source_frame_288.jpg` | EVIDENCE | JPEG verified, 960x480; source reference still. |
| `decoded_state_hashes.txt` | PUBLIC_TESTED | Four recorded RGB-state hashes exactly reproduced by public archive-only decoder. |
| `quality_metrics.json` | EVIDENCE | Parsed; four-frame AMCF quality result, not the 288-frame control. |
| `reconstructed_from_amcf.mp4` | EVIDENCE | SHA-256 matches checksum list; four H.264 frames plus AAC over about 12.1 seconds. |
| `source_ffprobe.json` | EVIDENCE | Parsed source probe; 288 AV1 frames and AAC. |
| `TEST02_REPORT.md` | EVIDENCE | Read; explicitly marks final AMCF acceptance FAIL. |
| `track_metrics.csv` | EVIDENCE | Parsed 32 rows for four frames and eight tracks. |
| `tracking_diagnostics/source_tracking_frame_001.jpg` | EVIDENCE | JPEG verified and visually inspected; shows contours and labeled tracks. |
| `tracks_manifest.json` | PUBLIC_TESTED | Four frames, 32 track rows; diagnostic viewer contract read by public module. |
| `viewer/comparison_difference.mp4` | EVIDENCE | SHA-256 matches checksum list; 288 H.264 comparison frames, no audio stream. |
| `viewer/comparison_sync.mp4` | EVIDENCE | SHA-256 matches checksum list; 288 H.264 comparison frames, no audio stream. |
| `viewer/index.html` | PUBLIC_TESTED | Generated viewer; reusable controls represented by public diagnostic viewer generator, not Pages `site/index.html`. |
| `viewer/tracks_manifest.json` | EVIDENCE | Byte-identical duplicate of top-level `tracks_manifest.json`. |
| `visual_comparisons/diff_x5_frame_001.jpg` | EVIDENCE | JPEG verified and visually inspected; amplified four-frame AMCF difference still. |
| `visual_comparisons/recon_frame_001.jpg` | EVIDENCE | JPEG verified, 960x480; encoded reconstruction still. |
| `visual_comparisons/reconstructed_frame_001.jpg` | EVIDENCE | JPEG verified and visually inspected; archive-only reconstructed state still. |
| `visual_comparisons/source_frame_001.jpg` | EVIDENCE | JPEG verified, 960x480; same hash as baseline source frame 001. |
| `waterfall_test02.amcf.zip` | PUBLIC_TESTED | ZIP integrity passed, 12 members; public decode reproduced four state hashes. |
| `work/audio.m4a` | ARCHIVE_EXACT | AAC; exact archive member and top-level audio duplicate. |
| `work/base.webp` | ARCHIVE_EXACT | WebP verified at 3840x1920; exact archive member. |
| `work/events/0000_BRANCH_LEAF_GROUP_LEFT.webp` | ARCHIVE_EXACT | WebP verified; exact archive member. |
| `work/events/0000_BRANCH_LEAF_GROUP_RIGHT.webp` | ARCHIVE_EXACT | WebP verified; exact archive member. |
| `work/events/0000_FOREGROUND_TREE_LEFT.webp` | ARCHIVE_EXACT | WebP verified; exact archive member. |
| `work/events/0000_FOREGROUND_TREE_RIGHT.webp` | ARCHIVE_EXACT | WebP verified; exact archive member. |
| `work/events/0000_MIDGROUND_TREE.webp` | ARCHIVE_EXACT | WebP verified; exact archive member. |
| `work/events/0000_MIST_SPRAY.webp` | ARCHIVE_EXACT | WebP verified; exact archive member. |
| `work/events/0000_WATER_IMPACT_FOAM.webp` | ARCHIVE_EXACT | WebP verified; exact archive member. |
| `work/events/0000_WATERFALL_COLUMN.webp` | ARCHIVE_EXACT | WebP verified; exact archive member. |
| `work/events/0003_WATER_IMPACT_FOAM.webp` | ARCHIVE_EXACT | WebP verified; exact archive member. |
| `work/manifest.json` | ARCHIVE_EXACT | Parsed; same object as archived `manifest.json`. |

## Six Older Short Reruns

The same 49-row table applies, path for path, to `20261013_061205`, `20261013_060131`, `20261013_055937`, `20261013_054829`, `20261013_023556`, and `20261013_023117`. Every file in every run was SHA-256-read. Forty-four of the 49 relative files are byte-identical across all seven runs, including the images, audio, videos, track metrics, track manifests, viewer, and working WebP payloads. The five varying relative files were reviewed separately:

| Varying file | Across-run result |
| --- | --- |
| `work/manifest.json` | Parsed in all seven; only `created_utc` differs. |
| `archive_manifest_resolved.json` | Parsed in all seven; only `created_utc`, archive path, and archive SHA-256 differ. |
| `waterfall_test02.amcf.zip` | All seven have 12 intact members; only archived `manifest.json` differs. Public archive-only decoding matched each run's four recorded state hashes. |
| `ARTIFACT_SHA256SUMS.txt` | Five present artifacts match their listed hashes in each run; each list also names an absent run-specific deliverable ZIP. |
| `TEST02_REPORT.md` | Read in all seven; only the generated timestamp line differs. All retain the final-acceptance FAIL verdict. |

The common 44-file hash result is a comparison of every relative path, not merely matching file counts or names. The published `Test 02` decoder and viewer checks were exercised on the latest run; identical manifests and media plus all-seven archive decoding support the same bounded disposition for the six older short reruns. This does not establish final codec quality or output/performance parity with later accepted work.

## Absent or Incomplete Local Evidence

- `decoded_frames/` is empty in the short runs. The four state hashes were rechecked by decoding each archive, but there are no saved decoded frame files in those run folders to compare.
- The reports name diagnostic overlays for frames 048, 144, 216, and 288, but only `tracking_diagnostics/source_tracking_frame_001.jpg` is present in each short run. Those other overlays cannot be inspected from these folders.
- Each `ARTIFACT_SHA256SUMS.txt` lists a run-specific deliverable ZIP absent from its run folder. This is missing local deliverable evidence, not evidence that GitHub omitted accepted source code.

## Decision and Next Part

No new source is required from these 343 short-run files. The code that generated them already maps to `Main` and public; the public archive decoder and diagnostic viewer behavior were exercised. These seven folders are **file-dispositioned**, not accepted final AMCF runs and not visual/performance identity proof. Continue with the older 288-frame `Test 02/20261003_165701` folder, then other open `Tests` folders and eventually the rest of the workspace. Preserve later accepted work over this failed fidelity experiment.

Generated output committed: no. Unsafe acceptance count in the public diagnostic report: 0. Hardware validation, physical Level 5, and manufactured player claimed: false.
