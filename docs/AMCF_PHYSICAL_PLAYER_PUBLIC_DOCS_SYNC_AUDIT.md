# AMCF Physical Player Public Docs Sync Audit

Run name: `AMCF_PHYSICAL_PLAYER_PUBLIC_DOCS_SYNC_V1`

## Baseline

Current git HEAD before edits was `fea00409262dea39d5c9068daac0a206c02d07f5`, which includes `AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO_V1`.

This run is a public documentation and navigation sync. It does not change runtime behaviour and does not add physical-player hardware support.

## Physical-Player Docs Found

- `docs/AMCF_PHYSICAL_PLAYER_CONCEPT.md`
- `docs/AMCF_PHYSICAL_PLAYER_STATE_MACHINE.md`
- `docs/AMCF_PHYSICAL_PLAYER_FAIL_CLOSED.md`
- `docs/AMCF_PHYSICAL_PLAYER_REVERSE_SEEK.md`
- `docs/AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES.md`
- `docs/AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO.md`
- `docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md`

## Physical-Player Demos Found

- `demo/run_physical_player_state_machine_demo.py`
- `demo/run_physical_player_fail_closed_demo.py`
- `demo/run_physical_player_reverse_seek_demo.py`
- `demo/run_physical_player_mechanism_profiles_demo.py`
- `demo/run_physical_player_simulator_demo.py`

## Physical-Player Tests Found

- `tests/test_physical_player_state_machine.py`
- `tests/test_physical_player_fail_closed.py`
- `tests/test_physical_player_reverse_seek.py`
- `tests/test_physical_player_mechanism_profiles.py`
- `tests/test_physical_player_simulator_demo.py`

## Site And Navigation Files Found

- `README.md`
- `CLAIM_BOUNDARIES.md`
- `docs/AMCF_HARDWARE_SOFTWARE_PATHS.md`
- `site/index.html`
- `site/README.md`

## Public Docs Gaps Found

- No single public map linked the physical-player concept, state machine, fail-closed, reverse/seek, mechanism-profile, and integrated-demo docs.
- README mentioned the mechanical/optical simulator but did not link the whole software/control sequence.
- Claim boundaries did not list the newer physical-player software/control simulator pieces together.
- The Pages site did not include a focused physical-player software/control simulator link group.
- The development sequence listed stages but did not include known commit IDs or the current docs-sync stage.

## Files Edited

- `README.md`
- `CLAIM_BOUNDARIES.md`
- `docs/AMCF_HARDWARE_SOFTWARE_PATHS.md`
- `docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md`
- `site/index.html`

## Files Created

- `docs/AMCF_PHYSICAL_PLAYER_PUBLIC_DOCS_SYNC_AUDIT.md`
- `docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md`
- `docs/AMCF_PHYSICAL_PLAYER_PUBLIC_SUMMARY.md`
- `tests/test_physical_player_public_docs_sync.py`

## Boundary

This is a public documentation/navigation sync. No physical hardware validation is claimed. No manufactured physical player, real motors, real sensors, real cartridge validation, real optical playback proof, real no-gap physical switching proof, real reverse hardware, arbitrary physical seek hardware, physical Level 5 completion, or hardware validation is claimed.
