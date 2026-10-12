# AMCF Physical Player Simulator Demo Audit

Run name: `AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO_V1`

## Baseline

Current git HEAD before edits was `0109302`, which includes `AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES_V1`.

## Existing Files Found

State-machine files:

- `src/amcf_physical_player_state_machine.py`
- `src/amcf_physical_player_state_machine_reports.py`

Fail-closed files:

- `docs/AMCF_PHYSICAL_PLAYER_FAIL_CLOSED.md`
- `demo/run_physical_player_fail_closed_demo.py`
- `tests/test_physical_player_fail_closed.py`

Reverse/seek files:

- `docs/AMCF_PHYSICAL_PLAYER_REVERSE_SEEK.md`
- `demo/run_physical_player_reverse_seek_demo.py`
- `tests/test_physical_player_reverse_seek.py`

Mechanism-profile files:

- `src/amcf_physical_player_mechanism_profiles.py`
- `src/amcf_physical_player_mechanism_profile_reports.py`
- `docs/AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES.md`
- `demo/run_physical_player_mechanism_profiles_demo.py`
- `tests/test_physical_player_mechanism_profiles.py`

Existing demos found:

- `demo/run_physical_player_state_machine_demo.py`
- `demo/run_physical_player_fail_closed_demo.py`
- `demo/run_physical_player_reverse_seek_demo.py`
- `demo/run_physical_player_mechanism_profiles_demo.py`

Existing tests found:

- `tests/test_physical_player_state_machine.py`
- `tests/test_physical_player_fail_closed.py`
- `tests/test_physical_player_reverse_seek.py`
- `tests/test_physical_player_mechanism_profiles.py`

## What This Run Adds

This run adds a top-level deterministic integrated simulator demo that combines:

- mechanism profile selection
- nominal forward playback orchestration
- fail-closed safety scenario orchestration
- bounded reverse/seek orchestration
- unsafe-acceptance audit
- unified report package

## Files Edited

- `docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md`

## Files Created

- `src/amcf_physical_player_integrated_demo_reports.py`
- `demo/run_physical_player_simulator_demo.py`
- `docs/AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO_AUDIT.md`
- `docs/AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO.md`
- `tests/test_physical_player_simulator_demo.py`

## Boundary

This is software/control simulator integration. It orchestrates existing simulator modules into a deterministic demo package for future hardware alignment.

No physical hardware validation is claimed. No manufactured hardware, real motors, real sensors, real cartridge validation, real optical playback proof, real no-gap physical switching proof, real reverse hardware, arbitrary physical seek, or physical Level 5 completion is claimed.
