# AMCF Tests File Review: Physical Medium And Single-App Main Entry Point

This record covers:

- `Test AMCF_PHYSICAL_MEDIUM_FLIPBOOK_SIMULATION/20261009_232154`
- `Test AMCF_SINGLE_APP_MAIN_ENTRYPOINT_CONFIG_GITHUB_LAYOUT/20261009_231538`

## Complete File Disposition

| Folder | Files | Disposition |
| --- | ---: | --- |
| Ideal physical-medium simulation | 1,170 | generated simulation evidence; source behavior reviewed |
| Single-app/Main entrypoint configuration | 26 | configuration and validation evidence; reusable entrypoint compared |
| **Total** | **1,196** | every file assigned |

The physical-medium folder is dominated by 288 proxy page images, recovered
frames, metrics, manifests, and reports. The single-app folder is composed of
configuration, toolchain status, Level 5 validation/smoke records, GitHub
layout manifests, and legacy-routing evidence.

## Ideal Physical-Medium Result

The source run passed an ideal digital physical-medium simulation:

- 288 AMCF proxy frames;
- 288 page images;
- 288 recovered frames;
- AMCF-versus-physical mean MAE `0.0`;
- AMCF-versus-physical mean PSNR `99.0`.

Its own boundary says this is a lossless digital simulation under ideal
registration. It does not prove paper, printer, camera, noise tolerance, real
scanning, or a physical device. The later vertical-stack and non-ideal
simulation folders supersede its left-to-right/flipbook shorthand as the better
physical design direction.

## Single-App/Main Result

The single-app run recorded:

- `Main/amcf_vnext.py` as the primary Main-facing entrypoint;
- config resolution and optional SAM2/CoTracker path handling;
- Level 5 validation and Main smoke pass for controlled semantic proof vectors;
- GitHub layout and legacy routing readiness;
- Python compilation pass.

The `Level 5 claimed: True` value in this local run is explicitly limited to
controlled canonical and HOOT dataset-annotated semantic proof vectors. It is
not a physical Level 5 or hardware claim. The public repository correctly
keeps physical/hardware claim flags false.

## Main And Public Code Comparison

The actual reusable Main entrypoint files were compared:

| File | Main/public result |
| --- | --- |
| `Main/amcf_vnext.py` / `src/amcf_vnext.py` | byte-identical; 23,523 bytes each |
| `Main/amcf_virtual_hardware.py` / `src/amcf_virtual_hardware.py` | byte-identical; 27,752 bytes each |

The public repository also contains later `src/amcf_cli.py` and workflow/demo
layers that are not present in the local Main snapshot. Those are newer public
additions, not losses from Main. The public CLI must still be validated against
the accepted local digital behavior before any final app/EXE claim.

## Progression Finding

The ideal physical-medium result was evidence for the future carrier branch.
The single-app run integrated the Main-facing v-next validation/status path.
The current public package preserves the exact Main v-next and virtual-hardware
modules, then adds newer public software I/O, diagnostics, archive, physical
simulation, and release layers. The local Main folder is therefore not the
complete source of every newer public module, and the public package is not
identical to the whole local workspace.

## Status

`MAIN_ENTRYPOINT_EXACT_FOR_TWO_CORE_MODULES; PHYSICAL_SIMULATION_EVIDENCE_ONLY`.

All 1,196 files are accounted for. No generated page/frame media is source
code. Continue with the Level 5 promotion and digital roadmap groups, where
the accepted component archive, diagnostics, decoded playback, optimization,
and Main integration must be mapped carefully.

Claim boundary: physical hardware validation false; physical Level 5 false;
manufactured player false; semantic proof-vector claims remain distinct from
physical proof; generated output committed no.
