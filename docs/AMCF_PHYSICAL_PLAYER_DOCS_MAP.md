# AMCF Physical Player Docs Map

## Overview

The AMCF physical-player branch is a software/control foundation for future compact mechanical/optical AMCF playback hardware. It documents and tests how later hardware should follow the digital AMCF update schedule through folded indexed media, A/B staging, a visible view gate, hidden staging, reader prefetch, transition blanking, fail-closed safety, bounded reverse/seek, and mechanism profiles.

The current repository implements deterministic software/control simulators and reports. It does not claim manufactured hardware or physical validation.

## Reading Order

1. `docs/AMCF_PHYSICAL_PLAYER_CONCEPT.md`
2. `docs/AMCF_PHYSICAL_PLAYER_STATE_MACHINE.md`
3. `docs/AMCF_PHYSICAL_PLAYER_FAIL_CLOSED.md`
4. `docs/AMCF_PHYSICAL_PLAYER_REVERSE_SEEK.md`
5. `docs/AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES.md`
6. `docs/AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO.md`
7. `docs/AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW.md`
8. `docs/AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH.md`
9. `docs/AMCF_PUBLIC_RELEASE_PACKAGE_INVENTORY.md`
10. `docs/AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW.md`
11. `docs/AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF.md`
12. `docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md`
13. `CLAIM_BOUNDARIES.md`
14. `docs/AMCF_HARDWARE_SOFTWARE_PATHS.md`

## Physical-Player Docs

- `docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md` - this public-facing map for the branch.
- `docs/AMCF_PHYSICAL_PLAYER_PUBLIC_SUMMARY.md` - short public-facing summary of the branch.
- `docs/AMCF_PHYSICAL_PLAYER_CONCEPT.md` - compact folded-path physical/optical concept and boundary.
- `docs/AMCF_PHYSICAL_PLAYER_STATE_MACHINE.md` - deterministic software/control state machine.
- `docs/AMCF_PHYSICAL_PLAYER_FAIL_CLOSED.md` - safety decisions and unsafe acceptance prevention.
- `docs/AMCF_PHYSICAL_PLAYER_REVERSE_SEEK.md` - bounded reverse buffer and local-buffer seek rules.
- `docs/AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES.md` - mechanism candidates and default simulator profile.
- `docs/AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO.md` - integrated deterministic simulator demo.
- `docs/AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW.md` - release-style review checks and report output.
- `docs/AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH.md` - public package-refresh checks and report output.
- `docs/AMCF_PUBLIC_RELEASE_PACKAGE_INVENTORY.md` - human-readable package inventory.
- `docs/AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW.md` - final public GitHub Pages and documentation review.
- `docs/AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF.md` - final public-release closeout and handoff record.
- `docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md` - staged development sequence and known commits.
- `docs/AMCF_HARDWARE_SOFTWARE_PATHS.md` - relationship between digital AMCF and physical paths.

## Demo Scripts

- `demo/run_physical_player_state_machine_demo.py`
- `demo/run_physical_player_fail_closed_demo.py`
- `demo/run_physical_player_reverse_seek_demo.py`
- `demo/run_physical_player_mechanism_profiles_demo.py`
- `demo/run_physical_player_simulator_demo.py`
- `demo/run_physical_player_release_review.py`
- `demo/run_public_release_package_refresh.py`

## Test Files

- `tests/test_physical_player_state_machine.py`
- `tests/test_physical_player_fail_closed.py`
- `tests/test_physical_player_reverse_seek.py`
- `tests/test_physical_player_mechanism_profiles.py`
- `tests/test_physical_player_simulator_demo.py`
- `tests/test_physical_player_public_docs_sync.py`
- `tests/test_physical_player_release_review.py`
- `tests/test_public_release_package_refresh.py`

## Output And Report Folders

- `output/physical_player_state_machine_demo/`
- `output/physical_player_fail_closed_demo/`
- `output/physical_player_reverse_seek_demo/`
- `output/physical_player_mechanism_profiles_demo/`
- `output/physical_player_simulator_demo/`
- `output/physical_player_release_review/`
- `output/public_release_package_refresh/`

Generated output is demo output and normally not committed.

## Claim Boundaries

Claimed:

- software/control simulator sequence
- deterministic physical-player demos
- mechanism profile selection
- state-machine orchestration
- fail-closed safety demonstration
- bounded reverse/seek demonstration
- unsafe-acceptance audit
- integrated report generation

Not claimed:

- manufactured physical player
- real physical/optical playback
- real motor validation
- real sensor validation
- real cartridge validation
- real scan validation
- real no-gap physical switching proof
- real reverse hardware
- arbitrary physical seek hardware
- physical Level 5 completion
- hardware validation

## What Is Implemented Now

The current software/control sequence includes the state machine, fail-closed safety model, reverse/seek controls, mechanism profiles, integrated simulator demo, and report generation. The integrated simulator demo keeps `unsafe_acceptance_count` at 0.

## What Remains Future Hardware

Future hardware work includes manufactured player hardware, physical transport validation, real motors and sensors, real cartridges, optical path testing, real reverse mechanics, physical seek characterization, and hardware validation.

## Recommended Next Development Step

The next development step is hardware-adapter alignment or physical-player PC recognition/control simulation, while preserving the current claim boundary until real hardware tests exist.
