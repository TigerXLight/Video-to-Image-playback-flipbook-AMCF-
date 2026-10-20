# AMCF CLI Dependency and Packaging Policy

## Purpose

This document records the installable package boundary for the maintained AMCF
workflow CLI. It makes the tested `src/amcf_cli.py` module available as the
`amcf` console command. The CLI, Windows EXE, workflow GUI, and per-user
installer are built together; physical hardware remains an explicit separate
validation boundary.

## Package Boundary

The repository now has a standard `pyproject.toml` using setuptools metadata:

```text
amcf = amcf_cli:main
```

The package includes the maintained top-level modules under `src/`, including
the component-event, temporal-codec, size-ceiling, diagnostic-profile, and
diagnostic-state modules, plus the `amcf_v0` and `amcf_v2` Python packages. The base package declares no Python
runtime dependencies so the source-frame, archive, report, and no-hardware
workflow paths remain inspectable with the standard library where their own
fallback rules permit it.

The package does not silently install FFmpeg. MP4 input and MP4 export require
the external `ffmpeg` and `ffprobe` executables and fail clearly when those
tools are unavailable. This is an explicit runtime-tool policy, not a hardware
integration claim.

## Optional Research Dependencies

The `research` extra names the scientific/image packages already represented
by the repository dependency manifest:

- NumPy
- Pillow
- OpenCV
- scikit-image
- SciPy
- imageio
- networkx
- tifffile
- lazy-loader

These packages are optional for the base CLI contract. Modules that use them
must retain graceful missing-dependency behavior and must not imply that a
research adapter is required for core archive validation or physical hardware.

## Intended Verification

The package metadata is validated by `tests/test_amcf_cli_packaging.py`, which
checks the project name, console-script target, source module coverage, and
absence of private workspace paths. On 2026-10-20 a wheel was built and
installed into a clean temporary virtual environment; both `amcf status` and
`amcf --help` returned successfully. The validation wheel was generated under
the ignored `output/amcf_package_validation_20261020/` directory.

For a repeatable package check, from the repository root:

```text
python -m pip wheel . --no-deps --no-build-isolation --wheel-dir output/package-check
python -m pip install --no-deps output/package-check/amcf_public_workflow-*.whl
amcf status
amcf --help
```

The wheel check is a package check, not an EXE build. MP4 workflows still need
the external FFmpeg tools described above, and diagnostic rendering uses the
optional research dependencies.

## Output and Claims

- workflow outputs remain under the caller-selected `output/` directory;
- generated archives, videos, reports, and editable-install metadata are not
  committed as release source;
- no physically validated printer, reader, scanner, player, motor, sensor,
  cartridge, USB, or serial integration is claimed; optional provider hooks
  are present and fail closed when a device or dependency is unavailable;
- hardware validation claimed: `false`;
- physical Level 5 claimed: `false`;
- manufactured player claimed: `false`;
- `unsafe_acceptance_count` remains `0` in the tested CLI paths.

## EXE Boundary

`packaging/amcf_cli.spec` and `packaging/build_amcf_cli_exe.ps1` define the
Windows console-EXE path. PyInstaller 6.22.3 built the current binary on
2026-10-20, and the binary passed both `status` and `--help` smoke tests:

```text
output/amcf_cli_exe_20261020/amcf.exe
```

The EXE is a CLI wrapper. The release bundle also contains the onedir GUI,
`RUN_AMCF_GUI.cmd`, `INSTALL_AMCF.cmd`, `install_amcf.ps1`, and their matching
uninstaller. The installer is per-user and does not require administrator
rights. None of these artifacts claims physical accuracy, physical Level 5,
or a manufactured player.

## Current Windows Bundle Verification

`packaging/build_amcf_release_bundle.ps1` builds:

- `amcf.exe`;
- `amcf_gui/amcf_gui.exe`;
- optional-device requirements;
- portable launch/install/uninstall scripts;
- the deterministic software-I/O fixture set.

The bundle was rebuilt and its CLI/device-system path was exercised on
2026-10-21. The installer was also tested into and removed from a temporary
directory with shortcuts disabled. Interactive GUI launch and real device
providers still require a Windows desktop/device environment and are not
silently treated as hardware validation.
