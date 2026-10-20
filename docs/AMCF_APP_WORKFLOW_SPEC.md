# AMCF App Workflow Specification

## 1. Purpose

`AMCF_APP_WORKFLOW_SPEC_V1` defines the first user-facing AMCF workflow. The
repo now has an installable `amcf` console CLI for this workflow, while GUI,
installer, and hardware adapters remain separate boundaries. A reproducible
Windows EXE build specification is present, but an EXE is only claimed after
the PyInstaller build and smoke check pass.

The app should first be understood as an AMCF conversion workbench:

```text
video / source frames
-> digital AMCF
-> print process
-> decoded video / decoded frames
```

This specification turns the current developer demos and no-hardware prototypes into a clear app/CLI plan. The initial CLI baseline wraps the clean public software paths; GUI and EXE work remain later packaging phases.

## 2. Intended User

The first intended user is a technically curious creator, researcher, or maintainer who wants to:

- convert visual source material into a digital AMCF package
- inspect and validate the AMCF package
- prepare a printable AMCF process plan
- decode or recover AMCF output back to frames
- understand what is proven in software and what remains future hardware work

The first app is usable from a command line; a GUI or Windows executable is a
packaging layer around that command-line contract.

## 3. Core User-Facing Workflow

The first user-facing workflow has three primary actions:

1. Encode source video or source frames into digital AMCF.
2. Prepare the digital AMCF package for the print process.
3. Decode digital AMCF back into decoded frames, with optional video-container export left for later.

The workflow should expose AMCF as a conversion pipeline, not only as a physical-player simulator.

## 4. Workflow A: Video / Source Frames To Digital AMCF

### Near-Term Input

- source frame folder
- deterministic sample source frames
- source-frame manifest

### Current Optional Input

- real video file such as `video.mp4`

Real video ingestion now has a public FFmpeg-backed adapter path in `src/amcf_video_pipeline.py` and `demo/run_amcf_video_pipeline_demo.py`. It remains optional because it requires FFmpeg/FFprobe on the host. The standard-library source-frame smoke path remains available without FFmpeg.

### Output

- digital AMCF archive, such as `sample_video_source.amcf.zip`
- `manifest.json` inside the archive
- frame payloads
- validation report
- human-readable summary

### Current Repo Support

Implemented developer support exists in:

- `src/amcf_digital_encoder.py`
- `src/amcf_digital_validator.py`
- `src/amcf_video_pipeline.py`
- `demo/run_source_frames_to_amcf_digital_demo.py`
- `demo/run_amcf_video_pipeline_demo.py`
- `tests/test_source_frames_to_amcf_digital.py`
- `tests/test_amcf_video_pipeline.py`

The current source-frame path can encode generated/source-frame PPM payloads into an AMCF digital archive and validate frame hashes, payload presence, manifest fields, and claim-boundary flags. The FFmpeg-backed video path extracts frames from MP4-style video input, carries copied audio into the archive when present, and validates the resulting archive.

### Missing Pieces

- GUI-level video file selection
- user-selected frame extraction
- user-facing progress output
- stable app command
- package config
- video dependency policy
- friendly error text for non-developers

## 5. Workflow B: Digital AMCF To Print Process

### Input

- digital AMCF package

### Output

- print layout manifest
- physical carrier/package plan
- indexed section files or section records
- lane geometry
- timing/index lane plan
- registration lane plan
- colour/reference lane plan
- hash/checksum lane plan
- print-preflight report

### Current Repo Support

Two related no-hardware paths exist:

- `src/amcf_physical_carrier.py` creates a software physical-carrier package from a digital AMCF archive.
- `src/amcf_print_layout.py` creates an abstract print-layout manifest from committed software I/O fixtures.

Supporting demos and tests include:

- `demo/run_amcf_to_physical_carrier_demo.py`
- `demo/run_amcf_pc_to_printer_layout_demo.py`
- `tests/test_amcf_to_physical_carrier.py`
- `tests/test_amcf_pc_to_printer_layout.py`

### Missing Pieces

- one user-facing print-plan command that accepts a real AMCF package path
- unified print-process output folder
- SVG, PNG, or PDF rendering
- reprint pack generation
- print preview
- printer margin calibration beyond abstract margin checks
- real printer driver integration
- OS print APIs

### Boundary

The print process is software planning only. It does not perform real printing, printer calibration, printer-driver integration, or hardware validation.

## 6. Workflow C: Digital AMCF To Decoded Video / Decoded Frames

### Input

- digital AMCF package
- later, optionally a software carrier package for recovery workflows

### Output

- decoded frames first
- decoded/recovered AMCF state manifest
- validation report
- optional video-container export later

### Current Repo Support

The current repo can recover frame payloads through the virtual carrier path:

- `src/amcf_virtual_carrier_reader.py`
- `demo/run_virtual_reader_recovery_export_demo.py`
- `tests/test_virtual_reader_recovery_export.py`

The current path exports recovered PPM frames and a recovered AMCF state manifest. It also validates missing sections, hash mismatch, missing lanes, duplicate/out-of-order section indices, and claim-boundary flags.

### Missing Pieces

- direct decode command from digital AMCF archive to frame folder
- optional MP4/video-container export
- media-player preview
- user-selected output format
- friendly decode diagnostics
- app-level success/failure wording

### Boundary

Decoded frame export may exist before MP4/video export. The current repo does not claim final media-player app behavior or video-container export.

## 7. Current Repo Support Summary

| Workflow | Current support | Current status |
| --- | --- | --- |
| source frames -> digital AMCF | `amcf_digital_encoder`, `amcf_digital_validator`, source-frame demo/tests | developer demo works |
| video file -> digital AMCF | FFmpeg-backed adapter and demo | optional dependency path |
| digital AMCF -> carrier/print process | physical-carrier generator and abstract print-layout prototype | no-hardware prototype |
| digital AMCF -> decoded frames | virtual carrier recovery exports PPM frames | no-hardware recovery demo |
| digital AMCF -> MP4/video | FFmpeg-backed archive decode/export path | optional dependency path |
| unified user CLI | `src/amcf_cli.py`, `demo/run_amcf_cli_workflow_demo.py`, `tests/test_amcf_cli.py` | initial baseline |
| GUI / EXE | not implemented | later |

## 8. Missing Pieces By Workflow

### Encode

- packaged dependency policy for FFmpeg/FFprobe
- stable CLI input contract
- output folder naming rules
- package metadata for an installable command

### Print Process

- digital-AMCF-package input for the abstract print-layout path
- render/preflight outputs suitable for a person to inspect
- PDF/SVG/PNG decisions
- real printer integration remains future

### Decode

- direct AMCF archive to decoded-frames command
- packaged MP4/video export policy
- output format settings

### Whole App

- one entrypoint
- command help
- user guide
- packaging metadata
- packaging validation plan
- installer/EXE plan after CLI stabilizes

## 9. Current And Proposed CLI Commands

Current public CLI module:

```text
python src/amcf_cli.py status
python src/amcf_cli.py encode --input-frames-manifest path/to/source_frames_manifest.json --output output/my_amcf
python src/amcf_cli.py encode --input-video path/to/video.mp4 --output output/my_amcf
python src/amcf_cli.py component-archive --input-frames-manifest path/to/source_frames_manifest.json --output output/my_component_archive
python src/amcf_cli.py decode --input output/my_amcf/package.amcf.zip --output output/my_decoded_frames
python src/amcf_cli.py print-plan --input output/my_amcf/package.amcf.zip --output output/my_print_plan
```

Near-term source-frame command:

```text
amcf encode --input-frames path/to/frames --output output/my_amcf
```

Future video input command:

```text
amcf encode --input-video path/to/video.mp4 --output output/my_amcf
```

Print-process planning command:

```text
amcf print-plan --input output/my_amcf/sample_video_source.amcf.zip --output output/my_print_plan
```

Decode command:

```text
amcf decode --input output/my_amcf/sample_video_source.amcf.zip --output output/my_decoded_frames
```

Potential later grouped workflow:

```text
amcf workflow full --input-video path/to/video.mp4 --output output/my_run --steps encode,print-plan,decode
```

The initial implementation now exposes `encode`, `component-archive`, `decode`, and `print-plan` subcommands before grouped workflows.

## 10. Proposed Output Folder Structure

For a full run:

```text
output/my_run/
  encode/
    source_manifest.json
    package.amcf.zip
    validation_report.json
    ENCODE_SUMMARY.md
  print_plan/
    physical_carrier_manifest.json
    carrier_sections/
    print_layout_manifest.json
    print_preflight_report.json
    PRINT_PLAN_SUMMARY.md
  decode/
    decoded_frames/
    recovered_amcf_manifest.json
    decode_validation_report.json
    DECODE_SUMMARY.md
  AMCF_WORKFLOW_SUMMARY.md
```

Generated output should remain under `output/` and should not be committed.

## 11. Success Criteria

A future CLI workflow succeeds only if:

- all required input files exist
- the source package validates
- hashes/checksums match
- print-plan output is internally consistent
- decoded frames or recovered frames validate
- `unsafe_acceptance_count` remains `0`
- claim-boundary flags remain false
- output files are written under the requested output folder
- the user receives a clear summary

## 12. Failure States

The app should fail clearly for:

- missing source input
- unsupported video input when FFmpeg/FFprobe is unavailable or the input cannot be decoded
- malformed source-frame manifest
- missing frame payload
- hash mismatch
- invalid AMCF archive
- missing AMCF manifest
- unsupported package schema
- invalid or missing carrier lane
- duplicate or out-of-order section
- print-plan validation failure
- decode/recovery validation failure
- output folder write failure

Failure messages should explain what failed, what file was affected, and whether retry, rescan, reprint, or user correction is appropriate.

## 13. User-Facing Wording

Use plain action labels:

- Encode AMCF
- Prepare Print Plan
- Decode AMCF
- Validate Package
- Open Output Folder

Recommended user-facing summary wording:

```text
AMCF workflow complete.
Digital AMCF package created.
Print-plan files created.
Decoded frames created.
unsafe_acceptance_count: 0
Hardware validation claimed: false
```

If a feature is not implemented, say:

```text
This build supports source-frame input. Direct video-file input is planned but not enabled yet.
```

Do not present developer-only demos as final app features.

## 14. Claim Boundaries

Required claim values:

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- real printer integration claimed: false
- real scanner integration claimed: false
- real player hardware claimed: false
- real video ingestion support: optional FFmpeg-backed path, not GUI/EXE-ready
- MP4/video-container export support: optional FFmpeg-backed path, not GUI/EXE-ready
- `unsafe_acceptance_count` must remain `0`

The workflow may claim:

- software AMCF archive generation from source frames
- digital AMCF validation
- software print-process planning
- software carrier/package planning
- virtual reader/recovery over software carrier sections
- decoded/recovered frame export

## 15. What Is Intentionally Not Included Yet

- GUI
- Windows EXE
- installer
- real printer driver integration
- real scanner/camera input
- USB/serial/HID player communication
- firmware protocol
- motor/sensor control
- real hardware validation
- physical Level 5 completion
- manufactured-player claim
- real video-file ingestion dependency
- MP4/video-container export dependency
- PDF/SVG/PNG rendering dependency

## 16. Why CLI Should Come Before GUI / EXE

The CLI should come first because it forces stable decisions about:

- command names
- user inputs
- output folders
- validation reports
- error messages
- claim-boundary wording
- generated-output policy

A GUI or EXE built before those contracts would mostly wrap developer demos and would risk hiding unsupported features behind a polished surface. A CLI baseline gives the future GUI and EXE a tested command layer to call.

## 17. Recommended Next Implementation Phase

Completed baseline phase:

```text
AMCF_CLI_ENTRYPOINT_BASELINE_V1
```

That phase created a standard-library CLI entrypoint for the core app commands:

```text
amcf encode
amcf component-archive
amcf print-plan
amcf decode
```

Completed follow-up phase:

```text
AMCF_LOCAL_MAIN_DELIVERABLE_VIEWER_PARITY_V1
```

That phase aligned the safe local `Main` deliverable polish: track-taxonomy metadata, comparison frames, optional FFmpeg comparison video, static viewer files, quality report, and deterministic zip packaging without private paths or generated media.

Recommended next implementation phase:

```text
AMCF_LOCAL_MAIN_DEPENDENCY_AND_PACKAGING_POLICY_V1
```

That phase is now represented by `pyproject.toml`,
`docs/AMCF_CLI_DEPENDENCY_AND_PACKAGING_POLICY.md`, and
`tests/test_amcf_cli_packaging.py`. It defines the `amcf` console entry point,
keeps the base package dependency-free, declares optional research packages,
and documents external FFmpeg/FFprobe requirements. A clean isolated install
check remains before any EXE work.

## Readiness Summary

- EXE ready now: no
- GUI ready now: no
- first CLI baseline implemented: yes
- CLI package metadata declared: yes
- recommended next phase: isolated package build/install validation
- generated output committed: no
- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false

