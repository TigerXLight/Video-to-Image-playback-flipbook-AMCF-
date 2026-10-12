# AMCF Physical Player Simulator Demo

## Purpose

AMCF is software-first. The integrated physical-player simulator demo shows how the existing software/control modules work together as a future hardware-support contract.

The hardware is not present yet. The demo can still orchestrate mechanism-profile selection, safe playback state transitions, fail-closed responses, bounded reverse/seek limits, unsafe-acceptance auditing, and claim-boundary reporting.

## Modules Integrated

- `amcf_physical_player_state_machine`
- `amcf_physical_player_state_machine_reports`
- `amcf_physical_player_mechanism_profiles`
- `amcf_physical_player_mechanism_profile_reports`
- `amcf_physical_player_integrated_demo_reports`

## Phases

1. Mechanism profile phase
2. Nominal forward playback phase
3. Fail-closed safety phase
4. Reverse/seek phase
5. Unsafe-acceptance audit phase
6. Unified report phase

## Mechanism Profile Phase

The demo builds all mechanism profiles, selects `folded_ab_motor_encoder_baseline`, and confirms no profile claims hardware validation or physical Level 5 completion.

## Forward Playback Phase

The demo creates a sample cartridge and state machine, recognizes the manifest, verifies the current section, locks the visible gate, enters playback-ready state, and runs safe forward transitions through the hidden staging gate and transition blanking path.

## Fail-Closed Phase

The demo exercises deterministic fail-closed scenarios for hash mismatch, missing marker, wrong section, invalid registration, prefetch timeout, hidden-gate failure, view-gate unlock, shutter/illumination placeholders, jam, double feed, misfeed, and audio drift limit.

## Reverse/Seek Phase

The demo populates the local reverse buffer through safe forward transitions, performs a successful bounded reverse, performs a local seek, denies arbitrary seek outside the local buffer, and denies or fails closed on invalid seek targets.

## Unsafe-Acceptance Audit

The audit checks that no invalid, hash-mismatch, wrong, unverified, or denied reverse/seek target becomes visible as an unsafe accepted state. Expected `unsafe_acceptance_count` is zero.

## Output Files

The demo writes:

- `integrated_simulation_summary.json`
- `mechanism_profile_report.json`
- `forward_playback_timeline.json`
- `fail_closed_safety_report.json`
- `reverse_seek_report.json`
- `unsafe_acceptance_audit.json`
- `claim_boundary_report.json`
- `PHYSICAL_PLAYER_SIMULATOR_DEMO_SUMMARY.md`
- `NEXT_STEPS.md`

Generated outputs are demo artifacts and are not hardware proof.

## Claim Boundary

This demo claims integrated software/control simulation and a future hardware-support control contract.

It does not claim:

- manufactured hardware
- real motors
- real sensors
- real cartridge validation
- real optical playback proof
- real no-gap physical switching proof
- real reverse hardware
- arbitrary physical seek
- physical Level 5 completion
- hardware validation
