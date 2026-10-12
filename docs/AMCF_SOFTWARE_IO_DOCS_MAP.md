# AMCF Software I/O Docs Map

## Overview

The AMCF software I/O branch organizes no-hardware software paths for:

- shared AMCF package / manifest / update-event / physical-section models
- cross-corridor reporting, validation, claim-boundary, and safety primitives
- deterministic fixture and regression data
- PC -> Printer abstract layout
- PC <-> Reader simulated recovery
- Player <-> PC simulated control bridge
- cross-corridor roundtrip and mutation safety tests

This branch does not claim hardware validation, physical Level 5 completion, or manufactured player completion.

## Reading Order

1. `docs/AMCF_SOFTWARE_DEVELOPMENT_AND_IO_CONTROL_DOSSIER_COLLECTION.md`
2. `docs/AMCF_SOFTWARE_IO_REPO_AUDIT.md`
3. `docs/AMCF_SHARED_PACKAGE_MANIFEST_MODEL.md`
4. `docs/AMCF_CROSS_CORRIDOR_REPORTING_MODEL.md`
5. `docs/AMCF_SOFTWARE_IO_FIXTURE_REGRESSION_BASELINE.md`
6. `docs/AMCF_PC_TO_PRINTER_SOFTWARE_PATH.md`
7. `docs/AMCF_PC_READER_SOFTWARE_PATH.md`
8. `docs/AMCF_PLAYER_PC_SOFTWARE_PATH.md`
9. `docs/AMCF_CROSS_CORRIDOR_ROUNDTRIP.md`
10. `docs/AMCF_CROSS_CORRIDOR_MUTATION_SAFETY.md`
11. `docs/AMCF_SOFTWARE_IO_PUBLIC_SUMMARY.md`
12. `docs/AMCF_SOFTWARE_IO_RELEASE_REVIEW_REFRESH.md`
13. `docs/AMCF_SOFTWARE_IO_IMPLEMENTATION_PROGRESS.md`

## Demo Scripts

- `demo/run_amcf_software_io_repo_audit.py`
- `demo/run_amcf_shared_package_model_demo.py`
- `demo/run_amcf_cross_corridor_reporting_demo.py`
- `demo/run_amcf_software_io_fixtures_demo.py`
- `demo/run_amcf_pc_to_printer_layout_demo.py`
- `demo/run_amcf_reader_recovery_fixture_demo.py`
- `demo/run_amcf_player_pc_runtime_fixture_demo.py`
- `demo/run_amcf_cross_corridor_roundtrip_demo.py`

## Test Files

- `tests/test_amcf_software_io_repo_audit.py`
- `tests/test_amcf_shared_package_model.py`
- `tests/test_amcf_cross_corridor_reporting.py`
- `tests/test_amcf_software_io_fixtures.py`
- `tests/test_amcf_pc_to_printer_layout.py`
- `tests/test_amcf_reader_recovery_fixture.py`
- `tests/test_amcf_player_pc_runtime_fixture.py`
- `tests/test_amcf_cross_corridor_roundtrip.py`
- `tests/test_amcf_cross_corridor_mutation_safety.py`
- `tests/test_amcf_software_io_public_docs.py`

## Output Folders

- `output/amcf_software_io_repo_audit/`
- `output/amcf_shared_package_model/`
- `output/amcf_cross_corridor_reporting/`
- `output/amcf_software_io_fixtures/`
- `output/amcf_pc_to_printer_layout/`
- `output/amcf_reader_recovery_fixture/`
- `output/amcf_player_pc_runtime_fixture/`
- `output/amcf_cross_corridor_roundtrip/`

Generated output is local demo output and should not be committed.

## Claim Boundaries

Claimed:

- software package/manifest model baseline
- deterministic no-hardware fixtures
- abstract printer-layout prototype
- simulated reader recovery fixture
- simulated player-control bridge
- cross-corridor roundtrip report
- mutation safety tests

Not claimed:

- real printer integration
- real reader/scanner integration
- real player hardware integration
- USB, serial, firmware, scanner, camera, image-processing, PDF, or barcode support
- hardware validation
- physical Level 5 completion
- manufactured player completion

## Recommended Next Step

The next step is a human review of the no-hardware software I/O baseline before any optional future hardware-adapter, GUI, image/PDF, barcode, scanner, printer, USB, serial, or firmware work.
