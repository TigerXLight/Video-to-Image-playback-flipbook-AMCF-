# AMCF Tests File Review: Pre-GitHub Video To Digital AMCF Smoke

This is the file-level review for:

`<workspace-root>/Tests/Test AMCF_PRE_GITHUB_VIDEO_TO_AMCF_DIGITAL_SMOKE_DEMO/20261010_200512`

The run created the first clean-package source-frame-to-digital-AMCF path. It
was deliberately a generated-frame smoke proof, not arbitrary MP4 ingestion.
The current public repository has since evolved beyond this package: the public
encoder and validator contain later audio/source-video metadata extensions,
and the public repository now has a separately tested FFmpeg video pipeline.

## Review Scope And Result

| Field | Result |
| --- | --- |
| Files discovered | 45 |
| Files accounted for below | 45 |
| Scanner verification failures | 0 |
| Refreshed ZIP | 33 members; CRC test passed |
| Source-frame-to-AMCF proof | Passed in the source run and current public tests |
| Arbitrary MP4 input in this source run | Not implemented/claimed |
| Current public MP4 adapter | Present in later public code and tests |
| Runtime port required from this folder | No; already ported and subsequently extended |
| Generated output committed | No |

## Exact File Inventory

### Run audit and generated evidence: 10 files

These files are run-local records or a generated package archive. They are
accounted for but are not public runtime source:

```text
20261010_200512/00_INPUT_AUDIT/input_audit.json
20261010_200512/00_INPUT_AUDIT/INPUT_AUDIT.md
20261010_200512/09_REVALIDATION/revalidation_results.json
20261010_200512/09_REVALIDATION/REVALIDATION_RESULTS.md
20261010_200512/10_UPDATED_COVERAGE_MINI_AUDIT/updated_coverage_mini_audit.json
20261010_200512/10_UPDATED_COVERAGE_MINI_AUDIT/UPDATED_COVERAGE_MINI_AUDIT.md
20261010_200512/11_REFRESHED_CLEAN_ZIP/<clean-package-source-to-amcf-demo>.zip
20261010_200512/12_NEXT_PART_PROMPT/NEXT_PART_PROMPT.md
20261010_200512/13_FINAL_STATUS/final_status.json
20261010_200512/13_FINAL_STATUS/FINAL_STATUS.md
```

Disposition for all ten: `GENERATED_EVIDENCE_NOT_SOURCE`. Their contents were
read sufficiently to establish the run's scope, validation, claim boundaries,
next phase, and explicit status that arbitrary real video was not claimed. The
ZIP was independently opened and passed CRC validation with 33 members.

### Clean-package files: 33 files

The nested package is the actual implementation-bearing part of this run.
Each path was compared by SHA-256 with the current public repository.

#### `PUBLIC_EXACT` in the current public repository

```text
01_UPDATED_CLEAN_PACKAGE/<clean-package>/.gitignore
01_UPDATED_CLEAN_PACKAGE/<clean-package>/cmd/RUN_AMCF_VNEXT.cmd
01_UPDATED_CLEAN_PACKAGE/<clean-package>/demo/generate_sample_source_frames.py
01_UPDATED_CLEAN_PACKAGE/<clean-package>/demo/RUN_SOURCE_FRAMES_TO_AMCF_DIGITAL_DEMO.cmd
01_UPDATED_CLEAN_PACKAGE/<clean-package>/demo/run_source_frames_to_amcf_digital_demo.py
01_UPDATED_CLEAN_PACKAGE/<clean-package>/demo/RUN_VIRTUAL_HARDWARE_DEMO.cmd
01_UPDATED_CLEAN_PACKAGE/<clean-package>/demo/run_virtual_hardware_demo.py
01_UPDATED_CLEAN_PACKAGE/<clean-package>/DEPENDENCIES_AND_PROVENANCE.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/docs/AMCF_PHYSICAL_MEDIUM_BOUNDARY.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/docs/OPTIONAL_DEEP_TOOL_ADAPTERS.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/docs/PHYSICAL_PLAYER_VISUAL_REFERENCE_NOTE.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/docs/PLAYER_UI_VIEWER_STUB.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/docs/SOFTWARE_FIRST_HARDWARE_SUPPORT.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/examples/sample_player_ui_state.json
01_UPDATED_CLEAN_PACKAGE/<clean-package>/examples/sample_virtual_cartridge.json
01_UPDATED_CLEAN_PACKAGE/<clean-package>/examples/source_frames/README.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/LICENSE_DECISION_REQUIRED.md
01_UPDATED_CLEAN_PACKAGE/<clean-package>/src/amcf_virtual_hardware.py
01_UPDATED_CLEAN_PACKAGE/<clean-package>/src/amcf_vnext.py
01_UPDATED_CLEAN_PACKAGE/<clean-package>/tests/RUN_RELEASE_TESTS.cmd
01_UPDATED_CLEAN_PACKAGE/<clean-package>/tests/test_source_frames_to_amcf_digital.py
01_UPDATED_CLEAN_PACKAGE/<clean-package>/viewer/amcf_player_ui_state_viewer.html
```

These are exact code, test, wrapper, example, or public-boundary files from
the clean package. They are already retained in the public tree and require no
copy from this generated run.

#### `PUBLIC_EQUIVALENT_TESTED` in the current public repository

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

These paths differ from the old clean package but have public replacements or
supersets. The encoder now handles optional audio payload metadata and source
video metadata; the validator checks audio payload hashes and byte counts.
The current public tests additionally cover the later MP4/FFmpeg video
pipeline, decoded-video export, and public workflow CLI boundary. The older
package's files must not overwrite those extensions.

### Run-local orchestration: 2 files

```text
20261010_200512/RUN_AMCF_PRE_GITHUB_VIDEO_TO_AMCF_DIGITAL_SMOKE_DEMO.cmd
20261010_200512/run_amcf_pre_github_video_to_amcf_digital_smoke_demo.py
```

Disposition for both: `LOCAL_MACHINE_SPECIFIC_DO_NOT_COPY`. The runner embeds
workspace-relative package paths, copies a clean package, writes generated
source files into the run, refreshes a ZIP, and records run-local status. Its
useful implementation outputs were already ported into the clean package;
copying the orchestrator would reintroduce local-path and generated-run
coupling.

## Source And Behavior Findings

The source run's input audit explicitly recorded that there was no encoder,
validator, or runnable source-to-AMCF command before the run. The run added:

- deterministic PPM source-frame generation;
- `amcf-digital-smoke-v1` archive writing;
- frame manifest and SHA-256 payload validation;
- archive validation and release-package tests;
- explicit false claim flags and `unsafe_acceptance_count: 0`.

The source run's own final status said:

- generated source frames -> AMCF digital: `FUNCTIONAL_AND_TESTED`;
- arbitrary real video -> AMCF digital: missing/not claimed at that time;
- next gaps: physical carrier, virtual reader export, and player simulation;
- no hardware, final UI, manufacturing, or physical prototype claim.

Current public parity for this folder is therefore:

| Behavior | Status | Evidence |
| --- | --- | --- |
| Deterministic source frames -> digital AMCF | `PUBLIC_EQUIVALENT_TESTED` | Exact generator/demo/test plus current public encoder/validator tests |
| Manifest and frame payload hashes | `PUBLIC_EQUIVALENT_TESTED` | Current public archive validation tests |
| Optional audio payload validation | `PUBLIC_EQUIVALENT_TESTED` | Later public encoder/validator extension |
| MP4/video -> AMCF | `PUBLIC_IMPLEMENTED` in later public work | `src/amcf_video_pipeline.py`, `tests/test_amcf_video_pipeline.py`, and `demo/run_amcf_video_pipeline_demo.py`; FFmpeg/ffprobe are required and tests skip clearly when unavailable |
| Digital AMCF -> decoded frames | `PUBLIC_IMPLEMENTED` | Current public digital/component archive readers and tests |
| Digital AMCF -> decoded video | `PUBLIC_IMPLEMENTED` when FFmpeg is available | Current public video-pipeline and decoder paths; no hardware claim |
| Real printer/scanner/player integration | `DO_NOT_PORT` from this folder | This run expressly had no hardware integration |

This folder is closed as `COVERED_BY_PUBLIC_SOURCE_WITH_NEWER_EXTENSIONS`.
It is not evidence that every other local `Tests` folder is complete or that
the whole workspace has exact parity.

## Why No Runtime Port Is Needed

The public source-frame path and its test were exact matches to this package.
The only meaningful source differences are later public extensions, not lost
behavior. The run-local orchestration and generated media are not reusable
application source. Replacing the current public files with the older copies
would remove audio metadata validation and the later video pipeline.

No files from this folder were copied in this part.

## Claim Boundary

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- real printer integration claimed: false
- real scanner integration claimed: false
- real player hardware claimed: false
- `unsafe_acceptance_count`: 0 in the source run and current tested public paths
- generated output committed: no

## Next Review Step

Continue the file-level newest-to-oldest pass with the next pre-GitHub
functional folder, then the broader accepted/rejected digital, diagnostic, and
physical groups. Do not begin CLI/EXE packaging work until the remaining local
`Tests` evidence has a disposition and the digital parity ledger is closed.
