# AMCF App Readiness and Gap Audit

## Run Metadata

- Run name: `AMCF_APP_READINESS_AND_GAP_AUDIT_V1`
- Audit type: app/readiness planning only
- Branch: `main`
- HEAD: `4bd3a6619e252ca7f61fe0fca58b5f263372cafe`
- Audit time: 2026-10-12 18:35:58 +01:00
- Runtime behaviour changed: no
- GUI implemented: no
- executable built: no
- dependencies added: no
- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false

## Evidence Read

The audit used the current public docs and implementation records, including:

- `docs/AMCF_SOFTWARE_DEVELOPMENT_AND_IO_CONTROL_DOSSIER_COLLECTION.md`
- `docs/AMCF_SOFTWARE_IO_IMPLEMENTATION_PROGRESS.md`
- `docs/AMCF_SOFTWARE_IO_DOCS_MAP.md`
- `docs/AMCF_SOFTWARE_IO_PUBLIC_SUMMARY.md`
- `docs/AMCF_PHYSICAL_PLAYER_DESIGN_AND_STRUCTURE_DOSSIER_COLLECTION.md`
- `docs/AMCF_PHYSICAL_PLAYER_IMPLEMENTATION_PROGRESS.md`
- `docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md`
- `README.md`
- corridor source, demos, docs, and tests for printer, reader, player, and roundtrip prototypes

## Current Runnable Commands

The current repo exposes developer/demo commands rather than one stable user-facing app entrypoint.

| Command | Purpose | Input required | Output generated | Demo-only | End-user suitable | Fixture required | Writes under `output/` | Safe to package now |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `python -m unittest discover -s tests` | Full regression suite | repo checkout | test result | no | developer only | committed tests/fixtures | no direct app output | yes as validation command |
| `python demo/run_amcf_software_io_repo_audit.py` | Repo audit/discovery report | repo tree | JSON/Markdown audit | yes | no | no | yes | yes as developer diagnostic |
| `python demo/run_amcf_shared_package_model_demo.py` | Shared package/manifest/update-event model demo | built-in demo data | JSON/Markdown model report | yes | no | no | yes | yes as developer diagnostic |
| `python demo/run_amcf_cross_corridor_reporting_demo.py` | Cross-corridor reporting baseline | built-in model data | JSON/Markdown report | yes | no | no | yes | yes as developer diagnostic |
| `python demo/run_amcf_software_io_fixtures_demo.py` | Fixture baseline report | committed fixtures | JSON/Markdown fixture report | yes | no | yes | yes | yes as developer diagnostic |
| `python demo/run_amcf_pc_to_printer_layout_demo.py` | Abstract PC -> Printer layout prototype | committed shared fixture | layout manifest and report | yes | not yet | yes | yes | yes as prototype command, not user app |
| `python demo/run_amcf_reader_recovery_fixture_demo.py` | Simulated PC <-> Reader recovery | committed simulated captures | recovery, diagnostics, summary | yes | not yet | yes | yes | yes as prototype command, not user app |
| `python demo/run_amcf_player_pc_runtime_fixture_demo.py` | Simulated Player <-> PC bridge | committed shared fixture/profile | session transcript and diagnostics | yes | not yet | yes | yes | yes as prototype command, not user app |
| `python demo/run_amcf_cross_corridor_roundtrip_demo.py` | No-hardware cross-corridor roundtrip | committed fixtures | roundtrip and component reports | yes | not yet | yes | yes | yes as prototype command, not user app |
| `python demo/run_physical_player_state_machine_demo.py` | Physical-player state-machine demo | sample simulator data | timeline/report | yes | no | no | yes | yes as developer diagnostic |
| `python demo/run_physical_player_fail_closed_demo.py` | Fail-closed safety demo | sample simulator data | safety reports | yes | no | no | yes | yes as developer diagnostic |
| `python demo/run_physical_player_reverse_seek_demo.py` | Reverse/seek simulator demo | sample simulator data | reverse/seek reports | yes | no | no | yes | yes as developer diagnostic |
| `python demo/run_physical_player_mechanism_profiles_demo.py` | Mechanism profile report | built-in profiles | profile reports | yes | no | no | yes | yes as developer diagnostic |
| `python demo/run_physical_player_simulator_demo.py` | Integrated physical-player simulator demo | built-in simulator data | integrated reports | yes | no | no | yes | yes as developer diagnostic |
| `python demo/run_physical_player_release_review.py` | Release-review scan | repo tree | release review reports | yes | developer only | no | yes | yes as release diagnostic |
| `python demo/run_public_release_package_refresh.py` | Package inventory/claim scan | repo tree | package reports | yes | developer only | no | yes | yes as release diagnostic |
| `python demo/run_public_github_pages_final_review.py` | Pages/public docs final review | repo tree | public review reports | yes | developer only | no | yes | yes as release diagnostic |
| `python demo/run_public_release_closeout_handoff.py` | Closeout/handoff report | repo tree | closeout reports | yes | developer only | no | yes | yes as release diagnostic |
| `python demo/run_public_release_tag_prep.py` | Tag-prep report | repo tree | tag-prep reports | yes | developer only | no | yes | yes as release diagnostic |
| legacy demo scripts under `demo/` | Existing digital/physical/virtual smoke demos | built-in/generated sample data | demo outputs | yes | developer only | varies | yes or `demo/output/` | package as examples only |

## Current App Status

- Single app entrypoint: no.
- CLI entrypoint: no stable unified CLI exists. Current commands are standalone demo scripts.
- GUI entrypoint: no app GUI exists. The repo contains static viewer/site material, but not a desktop GUI.
- Normal user workflow: not yet. The repo has developer demos and fixture workflows, not a guided user workflow.
- Project/package config for packaging: not present. No `pyproject.toml`, `setup.py`, `setup.cfg`, `requirements.txt`, `Pipfile`, `poetry.lock`, or `package.json` was found.
- Dependency list: not present as a package dependency file. Current new prototypes use the Python standard library.
- Windows executable build path: not present.
- Stable output folder policy: partially present. Demos consistently use `output/` or legacy `demo/output/`; `.gitignore` excludes these generated folders.
- User guide: partial. `README.md`, `QUICKSTART.md`, and public docs explain demos and claim boundaries, but there is no user-facing app guide for a single workflow.

Conclusion: the repo is ready as a developer/demo package, but not yet ready as a user-facing app or packaged executable.

## PC -> Printer Status and Gaps

Inspected:

- `src/amcf_print_layout.py`
- `demo/run_amcf_pc_to_printer_layout_demo.py`
- `tests/test_amcf_pc_to_printer_layout.py`
- `docs/AMCF_PC_TO_PRINTER_SOFTWARE_PATH.md`

| Capability | Status | Notes |
| --- | --- | --- |
| Load a real AMCF package | missing | The prototype loads committed fixtures, not arbitrary user packages. |
| Generate printable layout manifest | implemented / demo-only | `PrintLayoutManifest` and JSON output exist. |
| Generate SVG | missing | Explicitly not implemented. |
| Generate PNG | missing | Explicitly not implemented. |
| Generate PDF | missing | Explicitly not implemented. |
| Talk to a printer | missing | No printer driver or OS print API integration. |
| Handle printer margins | demo-only | Abstract `printer_safe_margin_mm` validation exists. Real printer calibration is missing. |
| Create reprint packs | missing / future | Reader diagnostics can request reprint, but no pack generator exists. |
| Validate output before printing | partial | Abstract layout validation exists; no render or print-preflight validation exists. |

Classification: no-hardware prototype. It is safe as a packaged demo command, but not as an end-user printing feature.

## PC <-> Reader Status and Gaps

Inspected:

- `src/amcf_reader_recovery.py`
- `demo/run_amcf_reader_recovery_fixture_demo.py`
- `tests/test_amcf_reader_recovery_fixture.py`
- `docs/AMCF_PC_READER_SOFTWARE_PATH.md`

| Capability | Status | Notes |
| --- | --- | --- |
| Read real scanned images | missing | No image input path. |
| Read scanner/camera input | missing | No scanner, camera, TWAIN, WIA, SANE, or camera API. |
| Process image folders | missing | No folder/image pipeline. |
| Detect lanes from pixels | missing | Lane status is fixture data, not image-derived. |
| Validate simulated captures | implemented / demo-only | Fixture capture statuses are validated deterministically. |
| Recover section records | implemented / demo-only | Recovery records are produced from simulated captures. |
| Generate rescan/reprint requests | partial | Diagnostic request records exist for simulated failures. |
| Rebuild package data | missing / future | Current recovery reports section status, not rebuilt package artifacts. |
| Avoid OCR/image dependency for now | implemented | `scanner_api_used`, `image_processing_used`, and barcode decoding remain false. |

Classification: no-hardware recovery fixture. It is useful for safety/report shape, but not yet a reader app.

## Player <-> PC Status and Gaps

Inspected:

- `src/amcf_player_pc_runtime.py`
- `demo/run_amcf_player_pc_runtime_fixture_demo.py`
- `tests/test_amcf_player_pc_runtime_fixture.py`
- `docs/AMCF_PLAYER_PC_SOFTWARE_PATH.md`

| Capability | Status | Notes |
| --- | --- | --- |
| Simulate player compatibility | implemented / demo-only | Fixture package compatibility against a simulated capability profile exists. |
| Run package/session transcript | implemented / demo-only | Deterministic command transcript exists. |
| Deny unsafe seek | implemented / demo-only | Arbitrary physical seek is denied in the simulated transcript. |
| Generate diagnostics | implemented / demo-only | Compatibility diagnostics and transcript reasons exist. |
| Communicate with hardware | missing | No hardware communication. |
| Use USB/serial/HID | missing | `usb_used` and `serial_used` remain false; no HID path exists. |
| Detect real player | missing | No hardware detection. |
| Control motors/sensors | missing | No motor or sensor code. |
| Run firmware protocol | missing | No firmware protocol. |

Classification: simulated player-control bridge. It is safe for package/session logic, not hardware runtime.

## Cross-Corridor Status and Gaps

Inspected:

- `src/amcf_cross_corridor_roundtrip.py`
- `demo/run_amcf_cross_corridor_roundtrip_demo.py`
- `tests/test_amcf_cross_corridor_roundtrip.py`
- `docs/AMCF_CROSS_CORRIDOR_ROUNDTRIP.md`

The roundtrip is fixture-based only. It composes:

```text
shared manifest
-> print layout
-> simulated reader recovery
-> player compatibility/session
-> cross-corridor report
```

It can become a CLI workflow, but it needs explicit user-facing input and output choices first.

Likely user inputs:

- source AMCF package path or fixture name
- output directory
- selected workflow: layout, reader fixture, player session, roundtrip, report
- strictness level for validation
- optional profile/layout settings

Useful outputs:

- package/manifest validation report
- print layout manifest
- reader recovery report
- player session transcript
- combined cross-corridor report
- human-readable summary

Recommended first real CLI command:

```text
amcf workflow roundtrip --package <path-or-fixture> --output output/<run-id> --profile folded_ab_motor_encoder_baseline
```

That command should initially support fixtures and later accept real package paths after package loading is defined.

## Packaging Readiness

| Packaging form | Readiness | Recommendation |
| --- | --- | --- |
| Plain Python scripts | ready for developers | Current best form. |
| `python -m ...` module CLI | not ready | Needs a module entrypoint and command routing. |
| Console `.exe` | not ready | Needs stable CLI, package config, dependency policy, user guide, and passing full tests. |
| Desktop GUI `.exe` | not ready | Needs workflow spec and CLI/report baseline first. |
| Portable zip | partially ready | Docs/demos can be zipped, but the repo still needs a user workflow, CLI contract, package metadata, and packaging validation plan. |
| GitHub release artifact | not ready for app release | Current repo is a research/demo release, not an app binary release. |

## Recommended Next Phase

Recommended next phase: `AMCF_APP_WORKFLOW_SPEC_V1`.

Reason: the repo has many working demo/prototype surfaces, but it does not yet define one user-facing workflow. A CLI or EXE built now would mostly wrap demo scripts without resolving input selection, output naming, package loading, error language, or user expectations. A workflow spec should define the first app path before code is added.

The next phase should specify:

- target user
- first supported workflow
- accepted inputs
- output folder layout
- command names
- success/failure messages
- claim-boundary wording shown to users
- which prototypes are exposed and which remain developer-only

After that, `AMCF_CLI_ENTRYPOINT_BASELINE_V1` is the likely implementation phase. A Windows CLI `.exe` should wait until after the CLI exists and tests pass.

## What Should Not Be Built Yet

- Desktop GUI
- Windows `.exe`
- installer
- real printer integration
- real scanner/camera input
- image processing pipeline
- PDF/SVG/PNG renderer as a packaging dependency
- barcode/QR support
- USB/serial/HID player communication
- firmware protocol
- motor/sensor control
- hardware validation reports
- physical Level 5 claims
- manufactured-player claims

## Validation Results

Plain `python -m unittest discover -s tests` could not run because the `python` launcher resolved to the Windows Store stub. The bundled Codex runtime Python was used instead.

Command:

```text
python -m unittest discover -s tests
```

Current result with bundled runtime:

- PASS
- 371 tests run
- 0 failures
- The previous public-doc local-path scan failure was repaired in commit `39ec979`.
- The local-path blocker is resolved. App/executable packaging is still not ready because workflow, CLI, package metadata, user-guide, real package input/output contract, and packaging validation pieces are still missing.

Targeted corridor demo validation:

| Command | Result | Key evidence |
| --- | --- | --- |
| `python demo/run_amcf_pc_to_printer_layout_demo.py` | PASS | `ok: true`, `real_printer_driver_used: false`, `unsafe_acceptance_count: 0` |
| `python demo/run_amcf_reader_recovery_fixture_demo.py` | PASS | `ok: true`, `scanner_api_used: false`, `image_processing_used: false`, `unsafe_acceptance_count: 0` |
| `python demo/run_amcf_player_pc_runtime_fixture_demo.py` | PASS | `ok: true`, `usb_used: false`, `serial_used: false`, `unsafe_acceptance_count: 0` |
| `python demo/run_amcf_cross_corridor_roundtrip_demo.py` | PASS | `ok: true`, `section_count: 3`, `recovered_section_count: 3`, `unsafe_acceptance_count: 0` |

## Claim-Boundary Status

- generated output committed: no
- `git ls-files output`: empty
- unsafe_acceptance_count: 0 in targeted app-readiness demos
- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- real printer integration claimed: false
- real scanner integration claimed: false
- real player hardware claimed: false

## App Readiness Conclusion

AMCF is not ready for a user-facing executable today.

It is ready for:

- developer demo use
- fixture-based software/control validation
- app workflow specification
- later CLI entrypoint design

It is missing, before EXE work:

- single app workflow
- stable CLI entrypoint
- package/project config
- dependency policy
- user guide
- real package input handling
- stable command/output contract
- packaging test plan

