# AMCF Tests File Review: Pre-GitHub Printable Physical Carrier

This is the file-level review for:

`<workspace-root>/Tests/Test AMCF_PRE_GITHUB_AMCF_TO_PRINTABLE_PHYSICAL_CARRIER_GENERATOR/20261010_211716`

This run added the no-hardware digital-AMCF to indexed physical-carrier output
package. It is the second pre-GitHub functional step after source frames to
digital AMCF. It creates software manifests, section files, and lane metadata;
it does not drive a printer or validate a physical carrier.

## Review Scope And Result

| Field | Result |
| --- | --- |
| Files discovered | 50 |
| Files accounted for below | 50 |
| Scanner verification failures | 0 |
| Refreshed ZIP | 38 members; CRC test passed |
| Digital AMCF to carrier-plan proof | Passed in the source run and current public tests |
| Real printing | Not implemented or claimed |
| Runtime port required from this folder | No; carrier module/demo/test are exact in public |
| Generated output committed | No |

## Exact File Inventory

### Run audit and generated evidence: 10 files

```text
20261010_211716/00_INPUT_AUDIT/input_audit.json
20261010_211716/00_INPUT_AUDIT/INPUT_AUDIT.md
20261010_211716/08_REVALIDATION/revalidation_results.json
20261010_211716/08_REVALIDATION/REVALIDATION_RESULTS.md
20261010_211716/09_UPDATED_COVERAGE_MINI_AUDIT/updated_coverage_mini_audit.json
20261010_211716/09_UPDATED_COVERAGE_MINI_AUDIT/UPDATED_COVERAGE_MINI_AUDIT.md
20261010_211716/10_REFRESHED_CLEAN_ZIP/<clean-package-physical-carrier-generator>.zip
20261010_211716/11_NEXT_PART_PROMPT/NEXT_PART_PROMPT.md
20261010_211716/12_FINAL_STATUS/final_status.json
20261010_211716/12_FINAL_STATUS/FINAL_STATUS.md
```

All ten are `GENERATED_EVIDENCE_NOT_SOURCE`. Their contents were read to
confirm the input gap, passing revalidation, eight generated carrier sections,
zero unsafe acceptance, remaining gaps, claim boundaries, and next phase. The
refreshed archive passed CRC validation and is not a public source asset.

### Clean-package files: 38 files

The clean package was compared to the current public repository by SHA-256.

#### `PUBLIC_EXACT`: 27 files

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
01_UPDATED_CLEAN_PACKAGE/<clean-package>/DEPENDENCIES_AND_PROVENANCE.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/docs/AMCF_PHYSICAL_CARRIER_OUTPUT_PACKAGE.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/docs/AMCF_PHYSICAL_MEDIUM_BOUNDARY.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/docs/OPTIONAL_DEEP_TOOL_ADAPTERS.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/docs/PHYSICAL_PLAYER_VISUAL_REFERENCE_NOTE.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/docs/PLAYER_UI_VIEWER_STUB.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/docs/SOFTWARE_FIRST_HARDWARE_SUPPORT.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/examples/sample_player_ui_state.json
01_UPDATED_CLEAN_PACKAGE/<clean-package>/examples/sample_virtual_cartridge.json
01_UPDATED_CLEAN_PACKAGE/<clean-package>/examples/source_frames/README.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/LICENSE_DECISION_REQUIRED.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/src/amcf_physical_carrier.py
01_UPDATED_CLEAN_PACKAGE/<clean-package>/src/amcf_virtual_hardware.py
01_UPDATED_CLEAN_PACKAGE/<clean-package>/src/amcf_vnext.py
01_UPDATED_CLEAN_PACKAGE/<clean-package>/tests/RUN_RELEASE_TESTS.cmd
01_UPDATED_CLEAN_PACKAGE/<clean-package>/tests/test_amcf_to_physical_carrier.py
01_UPDATED_CLEAN_PACKAGE/<clean-package>/tests/test_source_frames_to_amcf_digital.py
01_UPDATED_CLEAN_PACKAGE/<clean-package>/viewer/amcf_player_ui_state_viewer.html
```

The exact matches include the physical-carrier writer, demo, tests, public
wrappers, virtual hardware surface, examples, and boundary documentation.

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

These files differ because the public repo has later documentation, package,
audio, and video-pipeline extensions. None should be replaced with the older
copies. In particular, the exact carrier module remains intact while the
shared digital encoder/validator have been safely extended.

### Run-local orchestration: 2 files

```text
20261010_211716/RUN_AMCF_PRE_GITHUB_AMCF_TO_PRINTABLE_PHYSICAL_CARRIER_GENERATOR.cmd
20261010_211716/run_amcf_pre_github_amcf_to_printable_physical_carrier_generator.py
```

Both are `LOCAL_MACHINE_SPECIFIC_DO_NOT_COPY`. The runner embeds source-package
paths, copies package trees, writes generated carrier artifacts, refreshes a
run-local ZIP, and records local status. Its useful implementation was already
copied into the clean package as the exact `amcf_physical_carrier.py` module,
demo, and tests; the orchestration wrapper must not be copied into the public
runtime.

## Behavior Findings

The source run's audit recorded the pre-run gaps as:

- no physical carrier/page/section generator;
- no timing/index/registration/colour/hash/metadata lane generator.

The run then produced and validated a software carrier package with eight
sections and lane metadata. The source final status explicitly kept these
boundaries:

- actual physical printing: not claimed;
- arbitrary real video input: not claimed;
- physical proof, hardware validation, manufacturing readiness, and built
  prototype: not claimed.

Current public parity for this folder is:

| Behavior | Status | Evidence |
| --- | --- | --- |
| Digital AMCF archive -> physical carrier manifest | `PUBLIC_EXACT` | `src/amcf_physical_carrier.py` and its test |
| Indexed section files | `PUBLIC_EXACT` | Carrier demo/test |
| Timing/index/registration/colour/hash/metadata lane plan | `PUBLIC_EXACT` | Carrier module and docs |
| Carrier preflight/validation | `PUBLIC_EXACT` | Carrier tests and public demo |
| Real printer output | `DO_NOT_PORT` | Explicitly outside this run |
| Physical scan/readback | `PORT_LATER` | Later virtual-reader/no-hardware fixture phase |

This folder is closed as `PUBLIC_EXACT_FOR_IMPLEMENTED_SCOPE`.

## Progression Finding

This phase fills the software print-process boundary needed by the app workflow
without introducing a printer dependency. It is retained in the current public
repo and must remain compatible with the later virtual-reader, software I/O,
and physical-player layers. The generated sections and ZIP are evidence, not
source files to commit.

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

Continue the file-level pass with the next pre-GitHub virtual-reader recovery
folder. Do not add real scanner support or change the carrier module while
reviewing this historical run.
