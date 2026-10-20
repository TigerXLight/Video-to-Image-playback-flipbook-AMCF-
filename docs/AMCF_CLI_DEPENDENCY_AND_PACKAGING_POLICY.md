# AMCF CLI Dependency and Packaging Policy

## Purpose

This document records the installable package boundary for the maintained AMCF
workflow CLI. It makes the tested `src/amcf_cli.py` module available as the
`amcf` console command. The CLI is real and installable; an EXE, installer,
GUI, and hardware adapter remain separate boundaries.

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
- no real printer, reader, scanner, player, motor, sensor, cartridge, USB, or
  serial integration is included;
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

The EXE is a CLI wrapper; it does not claim a GUI, hardware access, physical
Level 5, or a manufactured player.
