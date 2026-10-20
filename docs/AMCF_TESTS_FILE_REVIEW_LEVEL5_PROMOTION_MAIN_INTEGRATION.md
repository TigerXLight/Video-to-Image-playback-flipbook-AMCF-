# AMCF Tests File Review: Level 5 Main Integration

## Scope

This review covers the evidence folder `Test AMCF_LEVEL5_PROMOTION_MAIN_INTEGRATION_RELEASE_REFRESH/20261009_225757` and its refreshed lightweight release candidate. It is a digital/semantic AMCF parity review. It does not claim physical hardware, physical Level 5, a manufactured player, real motors, real sensors, real cartridges, or physical optical validation.

## Evidence Inventory

The folder contains 94 files:

- 9 Python files: validation, acceptance, archive writer/reader, runtime, and refresh orchestration.
- 31 Markdown files: release notes, specifications, limitations, handoff, and status records.
- 33 JSON files and 9 CSV files: validation, vector, benchmark, manifest, and status data.
- 3 HTML files: static benchmark/viewer evidence.
- 2 command files: local execution wrappers.
- 7 ZIP files: generated archive/release fixtures.

The JSON, CSV, HTML, ZIP, and command outputs are evidence or local release artifacts. They are not copied into the public source tree as generated output.

## Accepted Status

The evidence records a Main-facing promotion of two bounded semantic/object proof vectors:

1. controlled canonical lost/recovered proof;
2. HOOT dataset-annotated lost/recovered proof.

The public representation is `src/amcf_semantic_level5_proof.py`, with tests, demo output, explicit scope, and `unsafe_acceptance_count: 0`. Earlier segmentation, tracking, deep-tool, mask, and automatic lost/recovered attempts remain recorded as progression evidence and are not silently promoted to accepted Level 5.

The Main-facing runtime is represented by `src/amcf_vnext.py`. A direct SHA-256 comparison found:

| File | Size | SHA-256 | Result |
| --- | ---: | --- | --- |
| `<workspace-root>/Main/amcf_vnext.py` | 23,523 bytes | `2786735B...C3B93` | reference |
| `src/amcf_vnext.py` | 23,523 bytes | `2786735B...C3B93` | byte-identical to Main |

The shortened hash display above is only for readable evidence; the comparison used the complete SHA-256 value. This confirms that the Main-facing Level 5 validation/status and archive-inspection surface was not lost when moved into the public package.

## Public Mapping

| Candidate evidence surface | Public mapping | Classification |
| --- | --- | --- |
| `RUNTIME/amcf_vnext.py` | `src/amcf_vnext.py` | superseded by the byte-identical Main/public runtime |
| `RUNTIME/amcf_runtime_v_next.py` | `src/amcf_vnext.py`, `src/amcf_archive_writer_reader.py`, and tested public runtime layers | consolidated newer equivalent |
| `ARCHIVE_WRITER_READER/amcf_archive_writer_v_next.py` | `src/amcf_archive_writer_reader.py` | consolidated newer equivalent |
| `ARCHIVE_WRITER_READER/amcf_archive_reader_v_next.py` | `src/amcf_archive_writer_reader.py` | consolidated newer equivalent |
| `VALIDATOR/amcf_validator_v_next.py` | `src/amcf_release_candidate_acceptance.py` plus archive fail-closed validation | public acceptance/validation equivalent with tests |
| `ACCEPTANCE/amcf_acceptance_harness.py` | `src/amcf_release_candidate_acceptance.py` and its demo/tests | public-safe acceptance layer; generated vectors excluded |
| candidate test vectors and release ZIPs | public archive writer/reader fixtures generated during tests | generated artifacts; do not commit |
| candidate viewer/benchmark HTML and JSON | public static component-event/deliverable viewers and reports | newer public inspection surfaces |

The public repository already contains tested layers for archive manifests, claim boundaries, sidecars, checksums, fail-closed validation, semantic proof scope, release acceptance, V2 metadata, diagnostic viewers, quality metrics, and deterministic deliverable packaging. Copying the candidate scripts under new names would duplicate older implementations and risk conflicting schemas.

## Main Integration Finding

The Level 5 promotion was integrated into local `Main` through `amcf_vnext.py`, its command wrapper, documentation, and provenance. The public `src/amcf_vnext.py` matches the current `Main/amcf_vnext.py` byte-for-byte. The public repository also contains later public-safe modules that are absent from the small local `Main` folder, including the digital video pipeline, component-event archive, diagnostics, archive writer/reader, semantic proof, release acceptance, V2, player-control, and physical-player layers.

This is therefore not evidence that every historical local output or private model/checkpoint is public. It is evidence that the accepted reusable Main-facing Level 5 control surface and the later public consolidation are represented.

## Claim Boundary

- semantic/object Level 5: accepted only for the two explicitly named proof vectors;
- physical hardware validation claimed: false;
- physical Level 5 claimed: false;
- manufactured player claimed: false;
- real motors, sensors, cartridges, scanners, printers, USB, or serial hardware: not claimed;
- `unsafe_acceptance_count`: 0;
- generated candidate output committed: no.

The candidate release notes contain mixed historical wording: one status file says the semantic branch is parked at Level 4.99, while the promotion notes accept the two bounded proof vectors. The public repo resolves this by keeping semantic/object proof scope explicit and keeping physical-player claim flags false.

## Remaining Parity Work

This folder does not identify a missing Level 5 runtime file that should be copied immediately. Remaining parity work is the broader newest-to-oldest review of later Test groups, especially accepted diagnostics/viewer behavior and any source-specific outputs not yet mapped into public modules. The next review must continue with actual source files, tests, and output manifests; it must not treat historical generated artifacts as source requirements.

