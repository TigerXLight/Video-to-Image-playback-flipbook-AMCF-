# AMCF Software I/O Public Summary

## What This Branch Is

The AMCF software I/O branch is a no-hardware software/control foundation for moving AMCF data across the three software corridors:

- PC -> Printer
- PC <-> Reader
- Player <-> PC

It also defines shared package, manifest, update-event, physical-section, reporting, fixture, and safety structures used by all corridors.

## What Is Implemented

- repo audit and discovery
- shared package / manifest / update-event / physical-section model
- cross-corridor report and claim-boundary model
- deterministic no-hardware fixtures
- abstract PC -> Printer layout prototype
- simulated PC <-> Reader recovery fixture
- simulated Player <-> PC control bridge
- cross-corridor roundtrip
- mutation safety tests

## Safety And Claims

The software I/O branch keeps:

- `unsafe_acceptance_count`: 0
- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false

## What Is Not Claimed

This branch does not claim real printer integration, real scanner or reader integration, real player communication, hardware validation, physical Level 5 completion, manufactured player completion, PDF/image/barcode support, or USB/serial/firmware support.

## Next Development Step

Review the no-hardware baseline and decide whether the next work should remain in software fixtures or move to a separately approved adapter-planning phase.
