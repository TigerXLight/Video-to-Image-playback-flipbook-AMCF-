# AMCF Software I/O Fixture Regression Baseline

## Purpose

`AMCF_SOFTWARE_IO_FIXTURE_REGRESSION_BASELINE_V1` creates small deterministic fixtures for later no-hardware AMCF software I/O phases.

The fixtures are committed under:

```text
tests/fixtures/amcf_software_io/
```

They are intentionally small and reviewable.

## Fixture Files

- `shared_package_fixture.json`
- `reader_capture_fixture.json`
- `player_profile_fixture.json`

## What They Cover

- shared package / manifest / update-event / physical-section data
- required AMCF section lanes
- simulated reader capture status
- bounded player profile controls
- degraded colour warning path
- fail-closed/no-hardware claim boundaries

## Claim Boundary

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- real printer required: false
- real reader required: false
- real player required: false
- real scanner required: false
- real USB required: false

## Demo

Run:

```text
python demo/run_amcf_software_io_fixtures_demo.py
```

Generated output is written to:

```text
output/amcf_software_io_fixtures/
```

Generated output is not source truth and should not be committed.

## Not Implemented In This Phase

- printer layout generation
- reader recovery logic
- player runtime bridge
- scanner/camera/image/PDF/barcode/USB/serial support
- GUI
- hardware validation
