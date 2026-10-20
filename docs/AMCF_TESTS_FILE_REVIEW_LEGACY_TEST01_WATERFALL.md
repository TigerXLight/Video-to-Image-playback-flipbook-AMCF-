# AMCF Tests File Review: Legacy Test 01 Waterfall

This is the file-level review for:

`<workspace-root>/Tests/Legacy Test 01/AMCF_Waterfall_Test_01`

The folder contains an older fixed-tile AMCF prototype and its generated
evidence. It is not the final public AMCF implementation. The review keeps its
mechanism and failure evidence traceable without promoting its rejected
quality/compression result.

## Review Scope

| Field | Result |
| --- | --- |
| Folder files discovered | 10 |
| Files accounted for below | 10 |
| Scanner verification failures | 0 |
| Archive integrity | `waterfall.amcf` is ZIP-compatible; CRC test passed |
| Public runtime port | No |
| Final quality acceptance | Failed by the source folder's own report |
| Generated output committed | No |

The standard-library evidence scanner wrote a temporary report under
`output/amcf_legacy_test01_evidence/`; that generated directory is ignored and
was removed after review. The scanner deliberately does not decide semantic
parity, so the dispositions below are based on the source, report, README, and
archive-member inspection.

## File Dispositions

| Local file | Role and evidence | Disposition | Public parity decision |
| --- | --- | --- | --- |
| `amcf_prototype.py` | 320-line Python 3.11 prototype. Uses FFmpeg/ffprobe, NumPy, Pillow, optional OpenCV preview, and scikit-image metrics. It creates a base WebP, fixed rectangular tile updates in `events.bin`, copied audio, and a decode path with intermediate RGB state hashes. | `HISTORICAL_FAILED` | Do not port this implementation. Its fixed 64x64-style rectangular scheduler is the method the README says tracks texture/luminance/noise rather than meaningful independent movement. |
| `README_TEST_01.md` | Human-readable run record. Explicitly says `WORKING MECHANISM / FAILED QUALITY-EQUIVALENT COMPRESSION TEST`, reduced analysis resolution, and no accepted native-4K result. | `HISTORICAL_FAILED` | Retain as provenance evidence only. Its restrictions agree with the public claim boundary. |
| `full_12sec_960p/test_report.json` | Parsed report for 288 frames at 960x480: 9,376 patch events, 8,206,510-byte archive, 26.751 dB mean PSNR, 0.7125 sampled SSIM, and intermediate hash verification. | `HISTORICAL_FAILED` | The size ceiling passed only at reduced resolution; the quality comparison did not. No public acceptance claim should be based on this report. |
| `full_12sec_960p/av1_reference_report.json` | Parsed same-resolution conventional AV1 comparison: 33.771 dB / 0.9334 SSIM at CRF45 and 31.533 dB / 0.8836 SSIM at CRF55, both much smaller than the prototype archive. | `GENERATED_EVIDENCE_NOT_SOURCE` | Benchmark evidence only; not a runtime input or package asset. |
| `full_12sec_960p/waterfall.amcf` | Valid ZIP-compatible custom `AMCF-PATCH-PROTOTYPE-0.1` archive with `manifest.json`, `base.webp`, `events.bin`, and `audio.mka`. Manifest records 288 frames, 120 tiles, 9,376 patch events, copied AAC, and frame hashes. | `GENERATED_EVIDENCE_NOT_SOURCE` | Do not copy or make it the public archive format. Public archive work uses newer tested schemas and fail-closed readers. The archive's historical decode success does not reverse its failed quality verdict. |
| `full_12sec_960p/frame_activity.csv` | 288-row per-frame update/MAE/PSNR diagnostic table. | `GENERATED_EVIDENCE_NOT_SOURCE` | Useful historical evidence of the update behavior; no public runtime dependency. |
| `full_12sec_960p/region_activity_map.png` | Verified 960x512 PNG showing the 120-region update-count map. | `GENERATED_EVIDENCE_NOT_SOURCE` | Diagnostic artifact only; no source logic to port. |
| `full_12sec_960p/baseline_960_av1_crf45.mkv` | 793,911-byte conventional AV1 reference media. | `GENERATED_EVIDENCE_NOT_SOURCE` | Benchmark artifact; not a public AMCF implementation asset. |
| `full_12sec_960p/reconstructed_full.mkv` | 6,731,358-byte H.264 playback copy reconstructed from the prototype archive and muxed with copied AAC. | `GENERATED_EVIDENCE_NOT_SOURCE` | Playback evidence only. It includes additional H.264 delivery loss and is not a replacement for the later accepted reconstruction/runtime paths. |
| `full_12sec_960p/digital_flipbook_comparison.mp4` | 4-panel diagnostic video showing source, reconstructed output, updated regions, and amplified difference for the first two seconds. | `GENERATED_EVIDENCE_NOT_SOURCE` | Viewer evidence only; not a user-facing app asset or final quality proof. |

## Archive Inspection

The archive passed `zipfile.testzip()` and contained exactly these four
members:

```text
manifest.json
base.webp
events.bin
audio.mka
```

The manifest identifies an `AMCF-PATCH-PROTOTYPE-0.1` format with a fixed
rectangular 120-tile layout, lossy WebP quality 70, threshold 12.0, and
timestamped tile events. The encoder's own decode path verified 288
intermediate RGB state hashes. This establishes that the prototype was
internally decodable; it does not establish equal-resolution or
quality-equivalent compression.

## Comparison With Main And Public

No file in local `Main` uses the `AMCF-PATCH-PROTOTYPE-0.1` format or the
`waterfall.amcf` member contract. The current public repository likewise has
no exact copy of `amcf_prototype.py`, and that is intentional.

The public repository already contains later, tested component-event and
archive paths with changed-region records, optional lossless WebP or PPM
payloads, adaptive scheduling, size-ceiling reporting, fail-closed validation,
quality metrics, and static viewer reporting. Those paths are not byte-identical
to this legacy prototype; they supersede its fixed-tile method for public
development. The source-specific Test 02 diagnostic path is also represented
separately and retains its own failed final-fidelity verdict.

Therefore this folder requires no runtime port. Porting it would reintroduce a
method that the historical run explicitly rejected as a final compression
solution.

## Progression Finding

This folder is a historical stepping stone before the later Test 02 and
accepted public archive/runtime work. It demonstrates that the project had an
independently timed region-event container, copied audio, archive-only decode,
and deterministic intermediate-state verification before the newer component,
diagnostic, and public-package layers. It does not supersede those later
layers, and it does not prove that the whole local workspace has reached public
parity.

Hardware validation claimed: false. Physical Level 5 claimed: false.
Manufactured player claimed: false. Real motors, sensors, cartridges, printer,
reader, scanner, USB, or physical prototype validation are not claimed.

## Next Review Step

Continue the file-level newest-to-oldest review with the remaining top-level
`Tests` folders and their nested files. This review closes only the 10 files in
this Legacy Test 01 folder; it does not close the broader `Tests` inventory or
prove 100% local-workspace parity.
