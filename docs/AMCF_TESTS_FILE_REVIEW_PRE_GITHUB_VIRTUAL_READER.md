# AMCF Tests File Review: Pre-GitHub Virtual Reader Recovery

This is the file-level review for:

`<workspace-root>/Tests/Test AMCF_PRE_GITHUB_VIRTUAL_READER_RECOVERY_EXPORT_DEMO/20261010_222827`

This run added the no-hardware virtual reader path: software-generated carrier
sections are read, validated, recovered into AMCF state, and exported as PPM
frame payloads. It does not read a real scanner/camera or claim physical
scanback.

## Review Scope And Result

| Field | Result |
| --- | --- |
| Files discovered | 55 |
| Files accounted for below | 55 |
| Scanner verification failures | 0 |
| Refreshed ZIP | 43 members; CRC test passed |
| Virtual recovery proof | Passed in the source run and current public tests |
| Recovered frame export | 8 frames in the source run |
| Real scanner/reader | Not implemented or claimed |
| Runtime port required from this folder | No; reader module/demo/test are exact in public |
| Generated output committed | No |

## Exact File Inventory

### Run audit and generated evidence: 10 files

```text
20261010_222827/00_INPUT_AUDIT/input_audit.json
20261010_222827/00_INPUT_AUDIT/INPUT_AUDIT.md
20261010_222827/08_REVALIDATION/revalidation_results.json
20261010_222827/08_REVALIDATION/REVALIDATION_RESULTS.md
20261010_222827/09_UPDATED_COVERAGE_MINI_AUDIT/updated_coverage_mini_audit.json
20261010_222827/09_UPDATED_COVERAGE_MINI_AUDIT/UPDATED_COVERAGE_MINI_AUDIT.md
20261010_222827/10_REFRESHED_CLEAN_ZIP/<clean-package-virtual-reader-recovery-export>.zip
20261010_222827/11_NEXT_PART_PROMPT/NEXT_PART_PROMPT.md
20261010_222827/12_FINAL_STATUS/final_status.json
20261010_222827/12_FINAL_STATUS/FINAL_STATUS.md
```

All ten are `GENERATED_EVIDENCE_NOT_SOURCE`. They were read to confirm the
pre-run gaps, passing recovery/export validation, eight recovered frames,
zero unsafe acceptance, explicit no-real-scanner boundary, and next phase.

### Clean-package files: 43 files

The clean package was compared to the current public repository by SHA-256.

#### `PUBLIC_EXACT`: 32 files

```text
01_UPDATED_CLEAN_PACKAGE/<clean-package>/.gitignore
01_UPDATED_CLEAN_PACKAGE/<clean-package>/cmd/RUN_AMCF_VNEXT.cmd
01_UPDATED_CLEAN_PACKAGE/<clean-package>/demo/generate_sample_source_frames.py
01_UPDATED_CLEAN_PACKAGE/<clean-package>/demo/RUN_AMCF_TO_PHYSICAL_CARRIER_DEMO.cmd
01_UPDATED_CLEAN_PACKAGE/<clean-package>/demo/run_amcf_to_physical_carrier_demo.py
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

The exact matches include the carrier reader, recovery/export demo and test,
all earlier no-hardware paths, and the virtual-reader boundary documentation.

#### `PUBLIC_EQUIVALENT_TESTED`: 11 files

```text
01_UPDATED_CLEAN_PACKAGE/<clean-package>/CLAIM_BOUNDARIES.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/docs/AMCF_CANONICAL_CONCEPT.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/docs/AMCF_HARDWARE_SOFTWARE_PATHS.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/docs/AMCF_PHYSICAL_PLAYER_CONCEPT.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/docs/AMCF_SOFTWARE_AND_PHYSICAL_SUPPORT_BOUNDARY.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/QUICKSTART.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/README.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/RELEASE_MANIFEST.json
01_UPDATED_CLEAN_PACKAGE/<clean-package>/src/amcf_digital_encoder.py
01_UPDATED_CLEAN_PACKAGE/<clean-package>/src/amcf_digital_validator.py
01_UPDATED_CLEAN_PACKAGE/<clean-package>/tests/test_release_package.py
```

These files differ because the current public repo has later documentation,
audio/video-pipeline, package, and release-review extensions. They must not be
replaced by the older copies.

### Run-local orchestration: 2 files

```text
20261010_222827/RUN_AMCF_PRE_GITHUB_VIRTUAL_READER_RECOVERY_EXPORT_DEMO.cmd
20261010_222827/run_amcf_pre_github_virtual_reader_recovery_export_demo.py
```

Both are `LOCAL_MACHINE_SPECIFIC_DO_NOT_COPY`. They embed run/package paths,
copy trees, generate recovery artifacts, refresh a ZIP, and record local
status. The reusable reader logic was already ported as the exact public
`amcf_virtual_carrier_reader.py` module, demo, and test.

## Behavior Findings

The source run closed these no-hardware behaviors:

- read software-generated physical carrier sections;
- validate section metadata and payload hashes;
- reject missing/tampered sections;
- recover AMCF digital state;
- export recovered PPM frames/payloads;
- preserve `unsafe_acceptance_count: 0`.

Its own final status explicitly did not claim real scanner hardware, physical
scanning, MP4 export, arbitrary real video input, physical proof, hardware
validation, manufacturing readiness, or a built prototype.

Current public parity for this folder is:

| Behavior | Status | Evidence |
| --- | --- | --- |
| Carrier section -> recovered AMCF state | `PUBLIC_EXACT` | `src/amcf_virtual_carrier_reader.py` and test |
| Recovered frame/payload export | `PUBLIC_EXACT` | Public recovery/export demo and test |
| Missing/tampered section rejection | `PUBLIC_EXACT` | Reader validation test |
| Real scanner/camera input | `DO_NOT_PORT` from this folder | Explicitly outside the run |
| Physical scanback | `PORT_LATER` | Requires a separate physical/no-hardware fixture decision |
| MP4/video-container export from this run | `DO_NOT_PORT` as a claim | The source run explicitly did not claim it; later public video pipeline is separate |

This folder is closed as `PUBLIC_EXACT_FOR_IMPLEMENTED_SCOPE`.

## Progression Finding

This phase completes the software-only print-process readback boundary needed
for later cross-corridor tests. It does not convert simulated recovery into
evidence of a real scanner or physical player. The public exact reader path
must remain alongside the newer digital video pipeline and physical-player
simulator rather than being replaced by hardware code.

## Claim Boundary

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- real printer integration claimed: false
- real scanner/reader integration claimed: false
- real player hardware claimed: false
- `unsafe_acceptance_count`: 0 in the source run and current tested public path
- generated output committed: no

## Next Review Step

Continue with the pre-GitHub mechanical/optical player simulator folder, then
continue through the larger accepted/rejected digital and diagnostic groups.
Do not add real scanner or player APIs while closing this historical evidence
batch.
