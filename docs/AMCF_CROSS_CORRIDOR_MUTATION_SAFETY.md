# AMCF Cross-Corridor Mutation Safety

## Purpose

`AMCF_CROSS_CORRIDOR_MUTATION_SAFETY_V1` adds negative safety tests for the no-hardware AMCF software I/O baseline.

These tests prove unsafe fixture mutations are rejected or denied instead of silently accepted.

## Tested Unsafe Cases

- duplicate section ID
- missing checksum/hash lane
- payload hash mismatch
- reader hash mismatch
- missing reader capture / wrong section path
- unsupported arbitrary seek
- manifest mismatch for player compatibility
- invalid print layout margins

## Required Safety Result

- `unsafe_acceptance_count`: 0
- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false

## Claim Boundary

This phase does not add hardware support, printer drivers, scanner/camera APIs, image processing, barcode decoding, USB/serial communication, firmware protocol, or GUI support.

It is a software/no-hardware mutation safety test phase only.
