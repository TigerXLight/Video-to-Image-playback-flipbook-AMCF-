# AMCF Physical Player Public Summary

## What This Branch Is

The AMCF physical-player branch is a software/control simulator sequence for a future compact mechanical/optical AMCF player. It defines how later hardware should obey the digital AMCF update schedule while keeping the visible image path physical/optical rather than normal LCD/OLED screen playback.

## What Is Implemented In Software/Control

Implemented now:

- physical-player concept documentation
- deterministic state-machine control flow
- fail-closed safety model
- bounded reverse/seek model
- mechanism profile model
- integrated simulator demo and reports
- unittest coverage for the public software/control sequence

## What The Integrated Demo Covers

The integrated demo combines mechanism profile selection, nominal forward playback, fail-closed scenarios, reverse/seek limits, unsafe-acceptance auditing, and claim-boundary reporting.

## What The Mechanism Profiles Represent

Mechanism profiles describe candidate future transport/control approaches. The default simulator profile is `folded_ab_motor_encoder_baseline`. These profiles are software/control references, not hardware validation.

## What Fail-Closed Means

Fail-closed means unsafe or unverified states are denied before display. A section should not become visible unless it is verified, staged, gate-locked, and safe. The current demos and tests preserve `unsafe_acceptance_count` at 0.

## Why Reverse/Seek Is Bounded

Reverse and seek are modeled as local-buffer behaviours. The simulator may step back or seek only to safe verified local targets. Arbitrary physical seek across a full cartridge is not claimed.

## What Is Not Claimed

This branch does not claim manufactured hardware, real motors, real sensors, real cartridge validation, real optical playback proof, real no-gap physical switching proof, real reverse hardware, arbitrary physical seek hardware, physical Level 5 completion, or hardware validation.

## Next Development Step

The next useful stage is hardware-adapter alignment or physical-player PC recognition/control simulation. Any later physical work should conform to the software/control contract and should not be described as validated until real hardware tests exist.
