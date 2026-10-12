# AMCF Public Release Package Refresh

## Purpose

`AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH_V1` refreshes the public release/package layer after the physical-player software/control simulator sequence.

Baseline commit: `659bd3e74a9e4dd254600558aec6e76309ba596f`.

This is a software release/package review artifact. It is not hardware proof.

## What The Package Refresh Checks

- required source files exist
- required demo scripts exist
- required test files exist
- required docs exist
- README links to the physical-player docs map and package refresh docs
- docs map includes release review, public summary, package refresh, and inventory docs
- development sequence includes Stages 2 through 9
- release review doc and script exist
- site navigation links to physical-player docs
- generated demo output is not tracked or staged
- public docs and site files do not leak local Windows workspace paths
- public docs and site files do not contain unsafe affirmative hardware claims
- package inventory includes new physical-player docs, scripts, and tests
- integrated simulator summary keeps `unsafe_acceptance_count` at 0

## Required Source Files

- `src/amcf_physical_player_state_machine.py`
- `src/amcf_physical_player_state_machine_reports.py`
- `src/amcf_physical_player_mechanism_profiles.py`
- `src/amcf_physical_player_mechanism_profile_reports.py`
- `src/amcf_physical_player_integrated_demo_reports.py`

## Required Demo Scripts

- `demo/run_physical_player_state_machine_demo.py`
- `demo/run_physical_player_fail_closed_demo.py`
- `demo/run_physical_player_reverse_seek_demo.py`
- `demo/run_physical_player_mechanism_profiles_demo.py`
- `demo/run_physical_player_simulator_demo.py`
- `demo/run_physical_player_release_review.py`
- `demo/run_public_release_package_refresh.py`

## Required Test Files

- `tests/test_physical_player_state_machine.py`
- `tests/test_physical_player_fail_closed.py`
- `tests/test_physical_player_reverse_seek.py`
- `tests/test_physical_player_mechanism_profiles.py`
- `tests/test_physical_player_simulator_demo.py`
- `tests/test_physical_player_public_docs_sync.py`
- `tests/test_physical_player_release_review.py`
- `tests/test_public_release_package_refresh.py`

## Required Docs

- `docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md`
- `docs/AMCF_PHYSICAL_PLAYER_PUBLIC_SUMMARY.md`
- `docs/AMCF_PHYSICAL_PLAYER_CONCEPT.md`
- `docs/AMCF_PHYSICAL_PLAYER_STATE_MACHINE.md`
- `docs/AMCF_PHYSICAL_PLAYER_FAIL_CLOSED.md`
- `docs/AMCF_PHYSICAL_PLAYER_REVERSE_SEEK.md`
- `docs/AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES.md`
- `docs/AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO.md`
- `docs/AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW.md`
- `docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md`
- `docs/AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH.md`
- `docs/AMCF_PUBLIC_RELEASE_PACKAGE_INVENTORY.md`

## Site / Navigation Inclusion

The public Pages site remains under `site/`. It is documentation/context only and does not change runtime behaviour or claim physical validation.

## Generated-Output Exclusion

Generated demo/report folders under `output/` and `demo/output/` may exist locally. They should remain ignored and uncommitted.

## Local-Path Scan

The refresh script checks public docs and site files for local Windows workspace paths, user directories, AppData paths, local package working-copy names, and Codex runtime paths.

## Claim-Boundary Scan

The refresh script checks public docs and site files for unsafe affirmative hardware claims while allowing negative boundary wording such as "not claimed" and "no hardware validation".

## What Is Not Claimed

This package refresh does not claim manufactured hardware, real motors, real sensors, real cartridge validation, real optical playback proof, real no-gap physical switching proof, real reverse hardware, arbitrary physical seek hardware, physical Level 5 completion, or hardware validation.

## How To Run

```cmd
python demo/run_public_release_package_refresh.py
```

Expected output folder:

`output/public_release_package_refresh/`

## Next Development Step

Push the package-refresh commit after review, then continue future hardware-adapter alignment without hardware validation claims.
