# AMCF Tests File Review: Pre-GitHub Mechanical Optical Player

This is the file-level review for:

`<workspace-root>/Tests/Test AMCF_PRE_GITHUB_MECHANICAL_OPTICAL_PLAYER_SIMULATOR/20261010_230845`

This run added the first executable software simulator for the future
mechanical/optical player path over indexed carrier sections. It models the
software state and controls only. It does not claim real optical transport,
motors, sensors, cartridges, physical playback, or a manufactured player.

## Review Scope And Result

| Field | Result |
| --- | --- |
| Files discovered | 60 |
| Files accounted for below | 60 |
| Scanner verification failures | 0 |
| Refreshed ZIP | 48 members; CRC test passed |
| Simulator proof | Passed in the source run and current public tests |
| View-gate/timeline/controls | Passed in the source run |
| Current public simulator | Newer tested superset |
| Runtime port required from this folder | No; public demo exact, module/test extended safely |
| Generated output committed | No |

## Exact File Inventory

### Run audit and generated evidence: 10 files

```text
20261010_230845/00_INPUT_AUDIT/input_audit.json
20261010_230845/00_INPUT_AUDIT/INPUT_AUDIT.md
20261010_230845/08_REVALIDATION/revalidation_results.json
20261010_230845/08_REVALIDATION/REVALIDATION_RESULTS.md
20261010_230845/09_UPDATED_COVERAGE_MINI_AUDIT/updated_coverage_mini_audit.json
20261010_230845/09_UPDATED_COVERAGE_MINI_AUDIT/UPDATED_COVERAGE_MINI_AUDIT.md
20261010_230845/10_REFRESHED_CLEAN_ZIP/<clean-package-mechanical-optical-player-simulator>.zip
20261010_230845/11_NEXT_PART_PROMPT/NEXT_PART_PROMPT.md
20261010_230845/12_FINAL_STATUS/final_status.json
20261010_230845/12_FINAL_STATUS/FINAL_STATUS.md
```

All ten are `GENERATED_EVIDENCE_NOT_SOURCE`. They were read to confirm the
pre-run gaps, passing simulator/timeline/view-gate/control checks, explicit
software-only boundary, zero unsafe acceptance, and next confidence-audit
phase.

### Clean-package files: 48 files

The clean package was compared to the current public repository by SHA-256.

#### `PUBLIC_EXACT`: 37 files

```text
01_UPDATED_CLEAN_PACKAGE/<clean-package>/.gitignore
01_UPDATED_CLEAN_PACKAGE/<clean-package>/cmd/RUN_AMCF_VNEXT.cmd
01_UPDATED_CLEAN_PACKAGE/<clean-package>/demo/generate_sample_source_frames.py
01_UPDATED_CLEAN_PACKAGE/<clean-package>/demo/RUN_AMCF_TO_PHYSICAL_CARRIER_DEMO.cmd
01_UPDATED_CLEAN_PACKAGE/<clean-package>/demo/run_amcf_to_physical_carrier_demo.py
01_UPDATED_CLEAN_PACKAGE/<clean-package>/demo/RUN_MECHANICAL_OPTICAL_PLAYER_SIMULATOR_DEMO.cmd
01_UPDATED_CLEAN_PACKAGE/<clean-package>/demo/run_mechanical_optical_player_simulator_demo.py
01_UPDATED_CLEAN_PACKAGE/<clean-package>/demo/RUN_SOURCE_FRAMES_TO_AMCF_DIGITAL_DEMO.cmd
01_UPDATED_CLEAN_PACKAGE/<clean-package>/demo/run_source_frames_to_amcf_digital_demo.py
01_UPDATED_CLEAN_PACKAGE/<clean-package>/demo/RUN_VIRTUAL_HARDWARE_DEMO.cmd
01_UPDATED_CLEAN_PACKAGE/<clean-package>/demo/run_virtual_hardware_demo.py
01_UPDATED_CLEAN_PACKAGE/<clean-package>/demo/RUN_VIRTUAL_READER_RECOVERY_EXPORT_DEMO.cmd
01_UPDATED_CLEAN_PACKAGE/<clean-package>/demo/run_virtual_reader_recovery_export_demo.py
01_UPDATED_CLEAN_PACKAGE/<clean-package>/DEPENDENCIES_AND_PROVENANCE.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/docs/AMCF_PHYSICAL_CARRIER_OUTPUT_PACKAGE.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/docs/AMCF_PHYSICAL_MEDIUM_BOUNDARY.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/docs/AMCF_VIRTUAL_READER_RECOVERY_EXPORT.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/docs/OPTIONAL_DEEP_TOOL_ADAPTERS.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/docs/PHYSICAL_PLAYER_VISUAL_REFERENCE_NOTE.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/docs/PLAYER_UI_VIEWER_STUB.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/docs/SOFTWARE_FIRST_HARDWARE_SUPPORT.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/examples/sample_player_ui_state.json
01_UPDATED_CLEAN_PACKAGE/<clean-package>/examples/sample_virtual_cartridge.json
01_UPDATED_CLEAN_PACKAGE/<clean-package>/examples/source_frames/README.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/LICENSE_DECISION_REQUIRED.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/src/amcf_physical_carrier.py
01_UPDATED_CLEAN_PACKAGE/<clean-package>/src/amcf_virtual_carrier_reader.py
01_UPDATED_CLEAN_PACKAGE/<clean-package>/src/amcf_virtual_hardware.py
01_UPDATED_CLEAN_PACKAGE/<clean-package>/src/amcf_vnext.py
01_UPDATED_CLEAN_PACKAGE/<clean-package>/tests/RUN_RELEASE_TESTS.cmd
01_UPDATED_CLEAN_PACKAGE/<clean-package>/tests/test_amcf_to_physical_carrier.py
01_UPDATED_CLEAN_PACKAGE/<clean-package>/tests/test_source_frames_to_amcf_digital.py
01_UPDATED_CLEAN_PACKAGE/<clean-package>/tests/test_virtual_reader_recovery_export.py
01_UPDATED_CLEAN_PACKAGE/<clean-package>/viewer/amcf_player_ui_state_viewer.html
```

#### `PUBLIC_EQUIVALENT_TESTED`: 11 files

```text
01_UPDATED_CLEAN_PACKAGE/<clean-package>/CLAIM_BOUNDARIES.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/docs/AMCF_CANONICAL_CONCEPT.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/docs/AMCF_HARDWARE_SOFTWARE_PATHS.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/docs/AMCF_MECHANICAL_OPTICAL_PLAYER_SIMULATOR.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/docs/AMCF_PHYSICAL_PLAYER_CONCEPT.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/docs/AMCF_SOFTWARE_AND_PHYSICAL_SUPPORT_BOUNDARY.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/QUICKSTART.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/README.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/RELEASE_MANIFEST.json
01_UPDATED_CLEAN_PACKAGE/<clean-package>/src/amcf_digital_encoder.py
01_UPDATED_CLEAN_PACKAGE/<clean-package>/src/amcf_digital_validator.py
01_UPDATED_CLEAN_PACKAGE/<clean-package>/src/amcf_mechanical_optical_player.py
01_UPDATED_CLEAN_PACKAGE/<clean-package>/tests/test_mechanical_optical_player_simulator.py
01_UPDATED_CLEAN_PACKAGE/<clean-package>/tests/test_release_package.py
```

The public simulator module and test differ because the current public branch
adds later physical-player controls: dynamic update scheduling, folded A/B
staging, hidden staging gates, transition blanking, prefetch timing, bounded
reverse/seek handling, and stricter fail-closed checks. The public demo remains
exact to the pre-GitHub run. The older copies must not replace those tested
supersets.

### Run-local orchestration: 2 files

```text
20261010_230845/RUN_AMCF_PRE_GITHUB_MECHANICAL_OPTICAL_PLAYER_SIMULATOR.cmd
20261010_230845/run_amcf_pre_github_mechanical_optical_player_simulator.py
```

Both are `LOCAL_MACHINE_SPECIFIC_DO_NOT_COPY`. They embed package/run paths,
copy trees, produce generated reports, refresh a ZIP, and record local status.
The reusable simulator surface was already ported into the public package and
then extended in the physical-player sequence.

## Behavior Findings

The source run closed these software-only behaviors:

- indexed carrier section loading;
- mechanical/optical presentation timeline;
- view-gate state modeling;
- play/pause/step/reverse/seek controls over simulated sections;
- explicit separation from digital-screen playback wording;
- claim-safe validation with `unsafe_acceptance_count: 0`.

The source final status explicitly did not claim real physical playback,
hardware, manufacturing, physical proof, MP4 export, or arbitrary real video
support.

Current public parity for this folder is:

| Behavior | Status | Evidence |
| --- | --- | --- |
| Basic mechanical/optical simulator demo | `PUBLIC_EXACT` | Public demo and wrapper |
| Player state/timeline model | `PUBLIC_EQUIVALENT_TESTED` | Current physical-player modules/tests |
| View-gate and transition behavior | `PUBLIC_EQUIVALENT_TESTED` | Current state-machine and simulator tests |
| A/B staging, prefetch, blanking, bounded reverse/seek | `PUBLIC_EQUIVALENT_TESTED` | Later public physical-player tests |
| Real motors/sensors/cartridges/optics | `DO_NOT_PORT` | Explicitly outside the run |
| Manufactured player or physical Level 5 | `DO_NOT_PORT` | Not claimed |

This folder is closed as `PUBLIC_EQUIVALENT_TESTED_WITH_NEWER_SUPERSET`.

## Progression Finding

This is the bridge from the virtual reader path to the public physical-player
software/control branch. The older pre-GitHub simulator was not lost; its demo
and core scope remain present, while later public work adds the more rigorous
state machine and fail-closed controls. That later code is the correct public
implementation and must not be flattened back to the first prototype.

## Claim Boundary

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- real motors validated: false
- real sensors validated: false
- real cartridges validated: false
- real optical playback validated: false
- `unsafe_acceptance_count`: 0 in the source run and current tested public path
- generated output committed: no

## Next Review Step

Continue with the pre-GitHub final functional confidence audit folder, then
review the broader accepted and rejected digital/diagnostic groups. Do not
replace the current physical-player supersets with the older package copy.
