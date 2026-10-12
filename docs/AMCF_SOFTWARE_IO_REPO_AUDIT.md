# AMCF Software I/O Repo Audit

## Run Metadata

- Run name: `AMCF_SOFTWARE_IO_REPO_AUDIT_V1`
- Branch: `dev/amcf-software-io-control`
- Base commit: `6a0997036b5c3998efed038bbfa75ca0349b63a0`
- Dossier path used: `docs/AMCF_SOFTWARE_DEVELOPMENT_AND_IO_CONTROL_DOSSIER_COLLECTION.md`
- Audit type: repo discovery and corridor classification only
- Later implementation phase performed: no
- Hardware validation claimed: false
- Physical Level 5 claimed: false
- Manufactured player claimed: false

## High-Level Findings

The repository already contains a software-first AMCF surface with digital encoding/validation, physical carrier package preparation, virtual reader recovery/export, Physical I/O architecture models, mechanical/optical player simulation, physical-player state-machine/fail-closed/reverse-seek/mechanism-profile layers, public reports, public docs, release/package review scripts, and a GitHub Pages site.

The current repo has meaningful coverage for all three software I/O corridors, but most corridor-specific work is still represented as software simulation, documentation, demos, and report-generation layers. This audit does not implement the next shared package/manifest/update-event model phase.

Local `origin/main` inspection was read-only. The audit branch and local `origin/main` do not currently appear as a simple "origin/main contains this head" relationship in the local refs; no merge, rebase, or base change was performed.

## Corridor Classification Table

| Category | Representative existing files |
| --- | --- |
| Shared AMCF core | `src/amcf_digital_encoder.py`, `src/amcf_digital_validator.py`, `src/amcf_physical_io.py`, `src/amcf_physical_carrier.py`, `src/amcf_vnext.py` |
| PC -> Printer | `src/amcf_physical_carrier.py`, `demo/run_amcf_to_physical_carrier_demo.py`, `docs/AMCF_PHYSICAL_CARRIER_OUTPUT_PACKAGE.md`, `docs/AMCF_PHYSICAL_IO_ARCHITECTURE.md` |
| PC <-> Reader | `src/amcf_virtual_carrier_reader.py`, `demo/run_virtual_reader_recovery_export_demo.py`, `docs/AMCF_VIRTUAL_READER_RECOVERY_EXPORT.md`, `tests/test_virtual_reader_recovery_export.py` |
| Player <-> PC | `src/amcf_virtual_hardware.py`, `src/amcf_physical_player_state_machine.py`, `src/amcf_mechanical_optical_player.py`, `examples/sample_player_ui_state.json` |
| Existing physical-player simulator/control | `src/amcf_physical_player_state_machine.py`, `src/amcf_physical_player_mechanism_profiles.py`, `src/amcf_physical_player_integrated_demo_reports.py`, physical-player demo/test files |
| Reports/logs/audits | `demo/run_physical_player_release_review.py`, `demo/run_public_release_package_refresh.py`, `demo/run_public_github_pages_final_review.py`, `demo/run_public_release_closeout_handoff.py`, `demo/run_public_release_tag_prep.py` |
| Tests/fixtures | `tests/`, `examples/`, sample JSON fixtures, demo-generated output conventions |
| Docs/site/release tooling | `README.md`, `CLAIM_BOUNDARIES.md`, `docs/`, `site/`, release/package/tag-prep docs |
| Generated output / ignored artifacts | `output/`, `demo/output/`, `__pycache__/`, `*.pyc`, `.gitignore` policy |
| Unclear / duplicate / possible schema conflict | physical manifest, physical carrier, virtual hardware, mechanical player, and state-machine reports define related package/manifest/report/section concepts that need review before later shared-model work |

## Shared-Core Findings

Existing shared-core concepts are spread across digital encoder/validator, physical carrier, Physical I/O architecture, virtual hardware, and player simulator files. The repo already uses JSON dictionaries, dataclasses, manifest-like structures, claim-boundary fields, hash/checksum checks, validation reports, and generated Markdown summaries. Later shared-model work should adapt these structures rather than introducing duplicate package, manifest, report, or section concepts.

## PC -> Printer Findings

The repo has software carrier output support and docs for future printer/physical-output preparation. It does not contain real printer driver integration, PDF generation, or hardware print validation. Existing support is centered on indexed physical carrier sections, lanes, registration, colour registry, metadata, and hash/checksum data.

## PC <-> Reader Findings

The repo has virtual reader/recovery/export support. It reads generated carrier sections and validates lanes and hashes without requiring scanner hardware. No real scanner API, camera capture, or image-processing dependency is introduced by this audit.

## Player <-> PC Findings

The repo has virtual hardware and physical-player software/control simulation surfaces. These cover player-facing state, capability/mechanism profiles, fail-closed logic, reverse/seek limits, diagnostics, and report generation. There is no USB, HID, serial, firmware, or real player communication module in this phase.

## Existing Physical-Player Simulator / Control Findings

The existing physical-player sequence is substantial: state machine, fail-closed safety, reverse/seek, mechanism profiles, integrated simulator demo, release review, package refresh, final Pages review, closeout handoff, and tag prep are present. These remain unchanged by this audit.

## Reports / Logs / Audits Findings

Reports consistently use deterministic JSON and Markdown outputs under `output/`. Public review scripts include `final_passed`, `unsafe_acceptance_count`, generated-output checks, local-path checks, unsafe hardware claim scans, and false hardware-claim flags. The new audit follows that pattern.

## Tests / Fixtures Findings

The repo uses `unittest` and standard-library demos. Existing tests cover source-frame encoding, carrier package generation, virtual reader recovery, Physical I/O, mechanical/optical player simulation, physical-player state machine, fail-closed safety, reverse/seek, mechanism profiles, public docs, release/package checks, closeout, tag prep, and release packaging. `.gitignore` ignores `Tests/`, so new test files may require exact-path force-add when first committed.

## Docs / Site / Release Findings

The README, docs, site, claim boundaries, release review, package refresh, closeout handoff, and tag-prep materials are present. The public docs maintain the software/control boundary and no-hardware-validation wording.

## Generated Output And Ignored-Artifact Findings

Generated audit output is written under `output/amcf_software_io_repo_audit/`. Existing policy excludes `output/`, `demo/output/`, `__pycache__/`, and `*.pyc`. Generated output should remain uncommitted.

## Unclear / Duplicate / Possible Schema Findings

Before later model work, human review should compare overlapping concepts in:

- `src/amcf_physical_io.py`
- `src/amcf_physical_carrier.py`
- `src/amcf_virtual_hardware.py`
- `src/amcf_mechanical_optical_player.py`
- `src/amcf_physical_player_state_machine.py`
- `src/amcf_physical_player_state_machine_reports.py`
- `src/amcf_physical_player_integrated_demo_reports.py`

These files may define related manifest, section, package, report, claim-boundary, or validation concepts. Later phases should adapt and consolidate rather than duplicate.

## Recommended Next Phase

Recommended next phase: shared AMCF package / manifest / update-event / physical-section model foundation, after human review of the overlap candidates identified by this audit.

## Explicit Phase Boundary

No later implementation phase was performed. This audit did not create package-model, manifest-model, printer, reader, player-runtime, GUI, scanner, image-processing, PDF, barcode, USB, serial, or hardware modules.
