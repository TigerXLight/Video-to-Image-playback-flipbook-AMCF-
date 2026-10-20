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
- shared physical software-adapter contract with ordered status/feedback events
- mutation safety tests

## Safety And Claims

The software I/O branch keeps:

- `unsafe_acceptance_count`: 0
- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false

## What Is Not Claimed

This branch does not claim real printer integration, real scanner or reader integration, real player communication, hardware validation, physical Level 5 completion, manufactured player completion, PDF/image/barcode support, or USB/serial/firmware support.

## Physical Software Adapter Contract

Run the adapter-roundtrip command to execute the printer/carrier, reader
recovery, player control, and shared validator corridors under one fail-closed
status contract. A passing run is software-only and keeps display and physical
transition permissions disabled.

## Hardware Adapter Planning

The hardware-plan command records concrete Windows-facing printer/carrier,
reader/scanner, and player-control interface contracts. It first reruns the
software-only baseline and keeps display and transition permissions disabled.
No physical validation is claimed by the plan.

## Provider Runtime

The hardware-providers command executes provider-neutral printer, reader, and
player interfaces against deterministic software fixtures. It includes a
negative test that blocks an unverified visible-gate switch. Future device
providers can implement these interfaces without changing the AMCF status or
fail-closed contract.

## Software Control Protocol

The software-control command adds the versioned command/session layer above
those providers. It negotiates capabilities, enforces session identity and
sequence ordering, records all corridor commands and responses, bounds local
seek/reverse, and rejects unverified visible switches. It remains software-only
and keeps physical display and transition permissions disabled. See
`docs/AMCF_SOFTWARE_CONTROL_PROTOCOL.md`.

## Device Provider Adapters

The `device-providers` command now exercises concrete `file`, `folder`, and
`loopback` adapters for the three corridors. Windows Print Spooler, WIA, and
serial adapters are explicit opt-in transport hooks. They require a selected
device profile and `--enable-hardware`, and they reject missing dependencies,
failed probes, invalid hashes, and malformed replies without authorizing a
physical transition. See `docs/AMCF_DEVICE_PROVIDER_ADAPTERS.md`.

## Device Profiles

The `device-profiles` command validates one profile for each software corridor
and then runs the selected adapters. The default bundle is file/folder/loopback
and is safe without hardware. A hardware profile requires both profile intent
and the explicit `--enable-hardware` flag. See
`docs/AMCF_DEVICE_PROFILE_LAYER.md`.
