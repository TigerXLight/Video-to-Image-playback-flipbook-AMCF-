# AMCF Physical Player Fail-Closed Safety Model

## Purpose

AMCF is software-first. The physical-player fail-closed layer defines the software/control safety contract that a future compact mechanical/optical AMCF player must obey.

The hardware is not present yet, but unsafe conditions and safe responses can be modeled now. Later hardware should conform to this logic before any physical validation claim is made.

## Safety Rule

A section may be displayed only if it is verified, staged, gate-locked, and safe.

If a critical lane, section identity, gate state, transition state, feed state, illumination state, shutter state, or sync state fails, the simulator must pause, request rescan, hold the previous safe state, stop motion, or fail closed. It must never display an unsafe section.

## Structured Fail-Closed Reasons

The state machine uses explicit reason strings including:

- `fail_closed_unverified_section`
- `fail_closed_wrong_section`
- `fail_closed_hash_mismatch`
- `fail_closed_missing_marker`
- `fail_closed_registration_failure`
- `fail_closed_gate_unlocked`
- `fail_closed_prefetch_timeout`
- `fail_closed_shutter_failure`
- `fail_closed_illumination_failure`
- `fail_closed_jam`
- `fail_closed_double_feed`
- `fail_closed_misfeed`
- `fail_closed_manifest_mismatch`
- `fail_closed_unsupported_carrier`
- `fail_closed_audio_sync_limit`
- `fail_closed_unsafe_transition`
- `fail_closed_hidden_gate_not_ready`
- `fail_closed_view_gate_not_locked`
- `fail_closed_unknown_critical_lane`

## Safety Decision Model

Each safety decision records:

- decision id
- timestamp
- decision
- reason
- severity
- current and next section
- display, motion, and transition permissions
- rescan, retry, and hold-previous-state permissions
- recommended action
- unsafe acceptance flag
- notes

Critical failures set `display_allowed` false and `unsafe_acceptance` false.

## Section Failure Scenarios

The deterministic sample data covers:

- valid section
- degraded colour section
- hash mismatch
- missing marker
- wrong section index or identity
- invalid timing/index
- invalid registration
- unsupported section type
- missing critical metadata
- unknown hash status

Degraded colour may be accepted with warning only when hash, marker, timing, identity, and registration checks pass.

## Prefetch Timeout

The prefetch timeout path blocks transition if the next section is not verified and staged by the update timestamp. The simulator records `fail_closed_prefetch_timeout` and keeps unsafe acceptance at zero.

## Gate Failures

The model checks:

- visible view gate locked before display
- hidden gate ready before transition
- blanking active before switching
- next section verified before becoming visible

Gate failures deny display or transition rather than allowing uncertain output.

## Shutter And Illumination Placeholders

The simulator includes software placeholders for:

- shutter stuck open
- shutter stuck closed
- illumination fault
- illumination cannot blank

These are future hardware-reportable states. No real shutter, lamp, LED, optical bench, or sensor driver is implemented here.

## Jam And Misfeed Placeholders

The simulator includes deterministic placeholders for:

- jam
- double feed
- misfeed

Jam can enter `mechanical_stop`. Double feed and misfeed fail closed. These are software safety states for future hardware to report later.

## Audio Sync Limit

Audio drift can be checked against a software threshold. Minor drift can warn/resync. Major drift pauses or holds the previous verified state until resync, and denies unsafe transition.

No real audio playback is required by this stage.

## Unsafe Acceptance Audit

The unsafe acceptance audit checks safety decisions, event logs, fail-closed events, and display permissions for invalid sections. The expected result is:

- `passed`: true
- `unsafe_acceptance_count`: 0

## What Is Not Claimed

This stage does not claim:

- manufactured hardware
- real sensors
- real motors
- real cartridge validation
- real optical playback proof
- real no-gap proof
- physical Level 5 completion
- hardware validation

It does claim a deterministic software/control safety model and future hardware-support safety contract.
