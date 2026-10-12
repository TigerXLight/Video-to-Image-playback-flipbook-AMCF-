# AMCF Digital AMCF Parity Audit

Run name: `AMCF_GITHUB_DIGITAL_AMCF_PARITY_AUDIT_V1`

Audit date: 2026-10-12

Branch: `main`

Starting HEAD: `20405ade156ef564f2181335f47ee53dceede569`

This is a discovery and parity-audit document for the public GitHub version of AMCF. It checks whether the current repo supports the same core user-facing AMCF workflow expected from the already-tested local work:

1. video/source frames to digital AMCF
2. digital AMCF to print process
3. digital AMCF to decoded frames/video

This audit does not implement new runtime behaviour, GUI, EXE packaging, hardware APIs, printer/scanner/camera/USB/serial support, or physical-player simulator changes.

## Summary

| Capability | Status | Current evidence |
| --- | --- | --- |
| MP4/source video to digital AMCF | MISSING | No public-repo source path accepts MP4 directly, extracts frames from video, invokes FFmpeg, preserves audio, or creates a component archive from a video container. |
| Source-frame folder to digital AMCF | IMPLEMENTED | `src/amcf_digital_encoder.py`, `src/amcf_digital_validator.py`, `demo/run_source_frames_to_amcf_digital_demo.py`, and `tests/test_source_frames_to_amcf_digital.py` create and validate a real `.amcf.zip` from deterministic PPM frames. |
| Digital AMCF to print process | PARTIAL | `src/amcf_physical_carrier.py` and `src/amcf_print_layout.py` provide no-hardware carrier/layout planning. No real printer, PDF, PNG, or production print pipeline is claimed. |
| Digital AMCF to decoded frames | PARTIAL | `src/amcf_virtual_carrier_reader.py` can recover PPM frames through the software carrier/virtual reader path. There is no single direct user command for `.amcf.zip` to decoded frames yet. |
| Digital AMCF to decoded MP4/video | MISSING | The public repo explicitly does not claim MP4/video-container export. |
| Audio preservation/handling | MISSING | The public digital AMCF smoke archive stores frame payloads only. Audio preservation is not implemented in the public repo. |
| Archive size ceiling <= source size | MISSING | The canonical concept requires size discipline, but current public encoder/tests do not enforce an archive-size ceiling against the source. |
| Manifest/update-event schedule | PARTIAL | The digital archive has `manifest.json`, `frame_entries`, frame count, dimensions, hashes, and fps. The shared package model has update events, but current `.amcf.zip` smoke archives do not yet carry a first-class update-event schedule. |
| Validation/report output | PARTIAL | Digital archive validation exists and demos emit JSON summaries. A full user-facing parity validation report for MP4, audio, size ceiling, update events, and decoded video does not yet exist. |

## Current Digital AMCF Runnable Surface

Current public-repo digital AMCF commands are developer demos rather than a unified user CLI:

| Command | Purpose | Output | Status |
| --- | --- | --- | --- |
| `python demo/run_source_frames_to_amcf_digital_demo.py` | Builds deterministic PPM sample frames, encodes them into digital AMCF, and validates the archive. | `demo/output/source_to_amcf/sample_video_source.amcf.zip` plus JSON summaries. | DEMO-ONLY, IMPLEMENTED core source-frame archive path |
| `python demo/run_amcf_to_physical_carrier_demo.py` | Converts a digital AMCF archive into a no-hardware physical carrier package. | `demo/output/amcf_to_physical_carrier/` | DEMO-ONLY, PARTIAL print-process path |
| `python demo/run_virtual_reader_recovery_export_demo.py` | Runs software carrier recovery and exports recovered PPM frames and a recovered AMCF state/archive. | `demo/output/virtual_reader_recovery/` | DEMO-ONLY, PARTIAL decoded-frame path |
| `python demo/run_amcf_shared_package_model_demo.py` | Demonstrates shared package, manifest, physical-section, and update-event model primitives. | `output/amcf_shared_package_model/` | FIXTURE-ONLY support layer |
| `python demo/run_amcf_cross_corridor_roundtrip_demo.py` | Runs a no-hardware software I/O roundtrip using fixtures and corridor models. | `output/amcf_cross_corridor_roundtrip/` | FIXTURE-ONLY cross-corridor prototype |

There is no current public-repo command equivalent to:

```text
amcf encode --input-video input.mp4 --output output/my_amcf
amcf decode --input output/my_amcf/archive.amcf.zip --output output/my_decoded_video
```

## MP4 to AMCF Status

Status: MISSING

The public GitHub repo does not currently support direct MP4/source-video ingestion into digital AMCF.

Findings:

- No public-repo encoder accepts an `input_video` or MP4 path.
- No public-repo code extracts frames from MP4.
- No public-repo code invokes FFmpeg for digital AMCF encoding.
- No public-repo code preserves, copies, or validates audio in the digital AMCF archive.
- The current encoder claim boundary explicitly keeps arbitrary real-video support unclaimed.
- README and workflow docs correctly describe real video input as future work.

This is the largest parity gap for the user-facing workflow.

## Source Frames to AMCF Status

Status: IMPLEMENTED

The public repo does support deterministic source-frame-folder style input through the current smoke encoder.

Relevant files:

- `src/amcf_digital_encoder.py`
- `src/amcf_digital_validator.py`
- `demo/run_source_frames_to_amcf_digital_demo.py`
- `tests/test_source_frames_to_amcf_digital.py`

Current behaviour:

- Reads a JSON source-frame manifest.
- Reads PPM frame payloads.
- Writes a real `.amcf.zip`.
- Stores `manifest.json` and `frames/frame_###.ppm`.
- Records hashes, dimensions, fps, payload sizes, frame count, and claim-boundary flags.
- Validates archive structure and frame hashes.
- Keeps `unsafe_acceptance_count` at `0`.

Limitations:

- Input is source frames, not MP4.
- Input is PPM-oriented and deterministic for tests/demos.
- There is no stable user CLI yet.
- The archive format is a smoke digital AMCF package, not the full component-update/archive parity format from the older local work.

## AMCF to Print Process Status

Status: PARTIAL

The repo has no-hardware print-process planning and carrier layout prototypes.

Relevant files:

- `src/amcf_physical_carrier.py`
- `src/amcf_print_layout.py`
- `demo/run_amcf_to_physical_carrier_demo.py`
- `demo/run_amcf_pc_to_printer_layout_demo.py`
- `tests/test_amcf_to_physical_carrier.py`
- `tests/test_amcf_pc_to_printer_layout.py`

Implemented:

- Digital AMCF to software carrier package.
- Section files with registration, timing/index, colour registry, payload, and hash/checksum lanes.
- Abstract lane geometry and print-layout manifest support.
- No-hardware validation.

Missing or future:

- Real printer integration.
- Production PDF/PNG/SVG export.
- Print-driver support.
- Printer margin calibration.
- Reprint pack generation from real scan failures.
- Printed-output validation.

## AMCF to Decoded Frames Status

Status: PARTIAL

The repo can recover PPM frames through the virtual carrier-reader path.

Relevant files:

- `src/amcf_virtual_carrier_reader.py`
- `demo/run_virtual_reader_recovery_export_demo.py`
- `tests/test_virtual_reader_recovery_export.py`

Implemented:

- Reads a software carrier package.
- Validates section order, required lanes, and payload hashes.
- Recovers PPM frame payloads from the source AMCF archive.
- Writes recovered frames.
- Can write a recovered `.amcf.zip`.
- Keeps `unsafe_acceptance_count` at `0`.

Limitations:

- This is a carrier/reader recovery demo, not a direct user-facing `amcf decode` command.
- It exports decoded frames, not a decoded video container.
- It does not use real scanner or camera input.

## AMCF to Decoded Video Status

Status: MISSING

The public repo does not currently export decoded MP4 or another video container from digital AMCF.

The virtual reader recovery claim boundary explicitly keeps MP4/video-container export unclaimed.

## Audio Handling Status

Status: MISSING

The public digital AMCF smoke archive does not preserve audio. Audio is discussed in canonical goals and physical-player sync testing, but the public digital encoder does not include audio payloads or audio extraction.

## Archive Size Ceiling Status

Status: MISSING

The canonical concept says AMCF should respect a source-size ceiling or explicitly fail that condition. The current public digital encoder and tests do not compare output archive size to source size.

This should be treated as a parity gap before declaring the public repo equivalent to the already-tested local implementation.

## Manifest and Update-Event Status

Status: PARTIAL

Current public digital archive:

- includes `manifest.json`
- includes schema `amcf-digital-smoke-v1`
- includes frame entries
- includes width, height, fps, frame count, hash algorithm, payload paths, payload bytes, and payload hashes

Current shared software I/O model:

- includes package manifest primitives
- includes physical sections
- includes update-event objects
- includes validation and report support

Gap:

- the current `.amcf.zip` smoke archive does not yet integrate the shared update-event schedule as the archive’s first-class playback schedule.

## Validation and Report Status

Status: PARTIAL

Implemented:

- archive validation dicts
- demo JSON summaries
- hash mismatch and missing payload tests
- claim-boundary flags
- `unsafe_acceptance_count == 0`

Missing:

- user-facing parity report for MP4 input
- audio parity validation
- archive-size ceiling validation
- decoded-video validation
- direct CLI validation report for the whole user workflow

## Local Working Implementation Comparison

Status: UNKNOWN for direct portability, useful for parity comparison

A separate local `Main` tree was found outside the public GitHub package. For public-doc safety, this audit refers to it as `<workspace-root>/Main`.

Relevant local files found:

- `<workspace-root>/Main/amcf_test02.py`
- `<workspace-root>/Main/test_archive_decode.py`
- `<workspace-root>/Main/amcf_vnext.py`
- `<workspace-root>/Main/requirements.txt`
- `<workspace-root>/Main/RUN_AMCF_VNEXT.cmd`

Observed local capabilities:

- MP4 source discovery and frame decoding through OpenCV-style video capture.
- Audio extraction/copy using an FFmpeg command.
- Component/update event archive generation.
- `.amcf.zip` archive writing.
- Archive decode/reconstruction path.
- Reconstructed MP4/video output using FFmpeg-style piping.
- Tests or helper checks for archive structure.

Why it was not ported in this audit:

- It depends on non-standard-library packages and external media tooling.
- It references local evidence folders and local media conventions.
- It contains broader research/proof-scope logic that is not the same as the public repo’s current no-dependency path.
- This task is an audit, not an implementation or dependency-import task.

Potential comparison files for a later porting phase:

- local component archive writer/decoder logic in `amcf_test02.py`
- local archive structure checker in `test_archive_decode.py`
- public frame encoder in `src/amcf_digital_encoder.py`
- public validator in `src/amcf_digital_validator.py`
- public workflow spec in `docs/AMCF_APP_WORKFLOW_SPEC.md`

## Comparison With Required User Workflow

Required user workflow:

1. video to digital AMCF
2. digital AMCF to print process
3. digital AMCF to decoded video

Current public repo status:

1. video to digital AMCF: MISSING for MP4/video; IMPLEMENTED only for source-frame fixtures.
2. digital AMCF to print process: PARTIAL no-hardware layout/carrier planning.
3. digital AMCF to decoded video: MISSING for video container; PARTIAL for recovered PPM frames through the virtual reader path.

Therefore the GitHub version is not yet at user-facing parity with the expected local/core AMCF workflow.

## Parity Gaps

1. MP4/source-video input is missing.
2. Audio extraction/preservation is missing.
3. Decoded MP4/video-container export is missing.
4. Archive size ceiling is missing.
5. Digital AMCF update-event schedule is not yet integrated into the `.amcf.zip` smoke archive.
6. The current digital AMCF archive is frame-payload based, not full component-update archive parity.
7. No stable CLI wraps encode, print-plan, and decode workflows.
8. No user guide covers a real end-to-end AMCF run.
9. No packaging/EXE validation should proceed until the workflow and CLI are stable.

## Recommended Next Phase

Recommended next phase: `AMCF_MP4_TO_DIGITAL_AMCF_PARITY_PLAN_V1`

Purpose:

- Define the public-repo parity target for MP4/source-video to digital AMCF.
- Compare the local `Main` implementation against the public repo safely.
- Decide the dependency policy for FFmpeg, OpenCV/Pillow, or a standard-library-only frame-folder bridge.
- Define archive structure requirements for frames, component updates, audio, manifest/update events, validation reports, and size ceiling.
- Decide whether the first public implementation should be:
  - source-frame CLI only,
  - MP4 via external FFmpeg adapter,
  - or a two-step import where users extract frames first.

The general CLI baseline should wait until this parity decision is made. A source-frame-only CLI could be built now, but it would not satisfy the stated normal-user workflow.

## CLI and EXE Readiness

CLI ready now: no

Reason:

- There is no MP4 input path.
- There is no decoded-video output path.
- There is no audio path.
- There is no source-size ceiling check.
- The user workflow contract is not yet stable enough for a single app entrypoint.

EXE ready now: no

Reason:

- The repo has no stable CLI entrypoint for the core user workflow.
- The repo has no packaging configuration for a user-facing executable.
- The repo has no MP4 dependency policy.
- The repo has no end-user workflow guide for real video input/output.

## Validation Run

Commands run with the bundled Python runtime:

```text
python -m unittest discover -s tests
python demo/run_source_frames_to_amcf_digital_demo.py
python demo/run_amcf_to_physical_carrier_demo.py
python demo/run_virtual_reader_recovery_export_demo.py
python demo/run_amcf_shared_package_model_demo.py
python demo/run_amcf_cross_corridor_roundtrip_demo.py
```

Results:

- unittest discover: PASS, 371 tests
- source frames to digital AMCF demo: PASS
- AMCF to physical carrier demo: PASS
- virtual reader recovery export demo: PASS
- shared package model demo: PASS
- cross-corridor roundtrip demo: PASS
- generated output committed: no
- `unsafe_acceptance_count`: 0

## Claim-Boundary Status

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- real printer integration claimed: false
- real scanner integration claimed: false
- real player hardware claimed: false
- real MP4 parity claimed: false
- decoded MP4/video export claimed: false
- generated output committed: false

This audit does not claim that the public repo proves real video parity yet. It confirms the public repo has a tested source-frame digital AMCF path and identifies the remaining parity gaps before a user-facing CLI or EXE should be built.
