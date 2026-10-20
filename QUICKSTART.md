# Quickstart

## 1. Run AMCF v-next smoke/validator path

From the full workspace, use:

```cmd
Main\RUN_AMCF_VNEXT.cmd status
Main\RUN_AMCF_VNEXT.cmd validate-level5
Main\RUN_AMCF_VNEXT.cmd smoke --output "Tests\Main vnext smoke"
```

In this release package, `src/amcf_vnext.py` is included for review/demo context.

## 1A. Run the workflow CLI from source

From the repository root, before installing a package:

```text
python src/amcf_cli.py status
python src/amcf_cli.py --help
```

The repository also declares an installable console command in `pyproject.toml`:

```text
python -m pip install -e .
amcf status
```

The editable install command is a developer/package check, not a Windows EXE
build. FFmpeg/FFprobe remain external optional tools for MP4 input/export.

## 2. Run virtual hardware demo

```cmd
demo\RUN_VIRTUAL_HARDWARE_DEMO.cmd
```

This writes demo output under `output\`.

## 3. Open AMCF Player UI state viewer

Open:

```text
viewer\amcf_player_ui_state_viewer.html
```

## 4. No real hardware required

The hardware support is virtual/emulated now. No real sensors, scans, motors, cartridges, or physical prototype are required.

## 5. Optional future physical experiments

Physical experiments are future optional work. They must not be confused with this software/demo package.

## Source frames to AMCF digital smoke demo

Run:

```bat
cd AMCF_GITHUB_CLEAN_PACKAGE
demo\RUN_SOURCE_FRAMES_TO_AMCF_DIGITAL_DEMO.cmd
```

The demo generates deterministic sample source frames, writes `demo\output\source_to_amcf\sample_video_source.amcf.zip`, validates the archive, and writes `SOURCE_TO_AMCF_DEMO_RESULT.md`.

This is source-frame support, not a claim of arbitrary real-world video ingestion. No real hardware is required and no physical proof or hardware validation is claimed.

## AMCF digital to physical carrier package demo

Run:

```bat
cd AMCF_GITHUB_CLEAN_PACKAGE
demo\RUN_AMCF_TO_PHYSICAL_CARRIER_DEMO.cmd
```

The demo generates deterministic source frames, encodes them into `sample_video_source.amcf.zip`, then creates `demo\output\amcf_to_physical_carrier\physical_carrier_manifest.json` and indexed carrier section files under `carrier_sections\`.

This is software carrier preparation only. It does not perform real printing and does not claim physical proof or hardware validation.

## Virtual reader recovery/export demo

Run:

```bat
cd AMCF_GITHUB_CLEAN_PACKAGE
demo\RUN_VIRTUAL_READER_RECOVERY_EXPORT_DEMO.cmd
```

The demo creates source frames, an AMCF digital archive, an indexed carrier package, then uses the virtual carrier reader to recover AMCF state and export recovered PPM frame payloads.

No real scanner, real reader hardware, physical scanning, or MP4/video-container export is claimed.

## Mechanical / optical physical player simulator demo

Run:

```bat
cd AMCF_GITHUB_CLEAN_PACKAGE
demo\RUN_MECHANICAL_OPTICAL_PLAYER_SIMULATOR_DEMO.cmd
```

The demo creates source frames, an AMCF digital archive, an indexed carrier package, then simulates a future mechanical/optical player moving sections through a fixed view gate with illumination and alignment state.

This is software simulation only. It is not real physical playback, not a digital-screen physical-player claim, and not hardware validation.

## Concept assets and physical-player correction

`assets/concepts/` contains current and legacy AMCF concept references. Old diagrams may be superseded and are retained for context only.

The corrected mechanical/optical physical-player concept is the current physical-player reference. In this package, physical player means mechanical/optical playback through indexed media, a fixed view/playback gate, illumination, and an optical viewing path for direct human viewing.

The physical player is not a digital-screen player, not the software UI viewer, and not the reader/scanner path. Concept assets do not claim hardware validation, physical proof, final UI, manufacturing readiness, or a built prototype.
