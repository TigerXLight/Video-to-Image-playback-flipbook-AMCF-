# AMCF Physical Player Mechanism Profiles

## Purpose

AMCF is software-first. Mechanism profiles define software/control contracts for possible future physical-player mechanisms before hardware exists.

The profiles let the simulator compare assumptions about transport, staging, actuation, guide/clamp support, reverse capability, seek capability, energy support, material branch, and claim status.

Mechanism profiles are not physical validation.

## Default Profile

The default simulator profile is:

`folded_ab_motor_encoder_baseline`

It represents:

- folded indexed carrier
- abstract A/B staging
- motor/encoder actuator family
- single visible gate plus hidden staging
- reader prefetch ahead
- limited reverse buffer
- local-buffer seek only
- fail-closed required

This default is the first software-control profile for simulator work. It is not manufactured hardware and not motor validation.

## Research Profiles

Research profiles include:

- `folded_ab_inchworm_research`
- `two_track_ab_shuttle_candidate`
- `cartridge_stack_shuttle_candidate`
- `chain_indexed_carrier_research`
- `spring_governor_brake_comparison`
- `soft_actuator_experimental_branch`
- `material_aligned_carrier_branch`

These are comparison records for future investigation. They remain unvalidated unless later physical evidence exists.

## Support Layers

Support-layer profiles include:

- `magnetic_guided_clamp_support`
- `energy_recovery_support_layer`

Support layers are not primary transport mechanisms and must not become the simulator default. Energy recovery is support only; it is not a claim that the system powers itself.

## Experimental And Material Branches

The soft-actuator branch is experimental only. The material-aligned branch is a material profile branch, not an actuator/default profile.

## Ranking Criteria

Profiles are scored with simple deterministic integers for:

- AMCF schedule fit
- A/B staging fit
- view-gate stability fit
- reader prefetch fit
- reverse fit
- seek fit
- fail-closed fit
- tablet form-factor fit
- simulator readiness
- hardware uncertainty

The score is for comparison only. It is not a measurement and not hardware validation.

## Claim Boundaries

All mechanism profiles default to:

- hardware validated: false
- physical Level 5 claimed: false
- software/control profile only

Validation fails if any current profile claims hardware validation or physical Level 5 completion.

## What Is Not Claimed

This stage does not claim:

- manufactured hardware
- real motor validation
- real piezo validation
- real chain carrier validation
- real cartridge shuttle validation
- real folded-path mechanism validation
- real physical random access
- real no-gap optical switching proof
- physical Level 5 completion
- hardware validation
- energy recovery powering the system

It does claim deterministic software/control mechanism profiles and a future hardware-support decision layer.
