# AMCF Physical Player Fail-Closed Audit

Run name: `AMCF_PHYSICAL_PLAYER_FAIL_CLOSED_V1`

## Baseline

Current git HEAD before edits was `f8b6e91`, which includes the physical-player software/control state-machine foundation.

Existing state-machine files:

- `src/amcf_physical_player_state_machine.py`
- `src/amcf_physical_player_state_machine_reports.py`
- `demo/run_physical_player_state_machine_demo.py`
- `tests/test_physical_player_state_machine.py`
- `docs/AMCF_PHYSICAL_PLAYER_STATE_MACHINE.md`
- `docs/AMCF_PHYSICAL_PLAYER_STATE_MACHINE_AUDIT.md`
- `docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md`

## Existing Fail-Closed Support

The baseline already included:

- structured fail-closed events
- hash mismatch rejection
- manifest mismatch rejection
- unsupported carrier rejection
- gate-lock checks before playback
- hidden staging checks before transition
- transition blanking checks
- local seek denial
- unsafe acceptance count held at zero

Existing fail-closed scenarios already tested:

- invalid manifest
- hash mismatch on next section
- load view gate before verification
- stage next before verification
- transition without hidden gate readiness
- switch without blanking
- invalid next section during `step_forward()`
- unsupported arbitrary seek denial

## Scenarios Added In This Run

This run adds deterministic coverage for:

- degraded colour warning accepted without unsafe acceptance
- missing marker
- wrong section identity
- invalid timing/index
- invalid registration
- unsupported section type
- missing critical metadata
- unknown hash status
- explicit prefetch timeout
- view gate not locked
- hidden gate not ready
- unsafe transition without blanking
- unverified next section switch attempt
- shutter failure placeholders
- illumination failure placeholders
- jam placeholder
- double-feed placeholder
- misfeed placeholder
- audio sync drift limit
- unsafe acceptance audit report

## Files Edited

- `src/amcf_physical_player_state_machine.py`
- `src/amcf_physical_player_state_machine_reports.py`
- `docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md`

## Files Created

- `docs/AMCF_PHYSICAL_PLAYER_FAIL_CLOSED_AUDIT.md`
- `docs/AMCF_PHYSICAL_PLAYER_FAIL_CLOSED.md`
- `demo/run_physical_player_fail_closed_demo.py`
- `tests/test_physical_player_fail_closed.py`

## Boundary

This is a software/control safety implementation. It defines unsafe conditions, structured decisions, and safe responses that future physical-player hardware should conform to.

No physical hardware validation is claimed. No manufactured hardware, real sensors, real motors, real cartridge validation, real optical playback proof, real no-gap proof, or physical Level 5 completion is claimed.
