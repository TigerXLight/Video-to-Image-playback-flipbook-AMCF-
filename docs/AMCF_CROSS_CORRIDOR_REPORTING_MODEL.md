# AMCF Cross-Corridor Reporting Model

## Purpose

`AMCF_CROSS_CORRIDOR_REPORTING_BASELINE_V1` adds a shared software/no-hardware reporting layer for the AMCF software I/O corridors.

This phase does not implement printer, reader, or player runtime modules. It defines report, safety-decision, and claim-boundary primitives that later corridor phases can reuse.

## Corridors Covered

- Shared AMCF core
- PC -> Printer
- PC <-> Reader
- Player <-> PC

## Model Objects

- `AMCFClaimBoundaryReport`
- `AMCFSafetyDecision`
- `AMCFCorridorCheck`
- `AMCFCrossCorridorReport`

The report consumes the shared package/manifest model and records whether each corridor has the shared data it needs before corridor-specific implementations exist.

## Claim Boundary

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- real printer required: false
- real reader required: false
- real player required: false
- real scanner required: false
- real USB required: false

## Safety Rule

`unsafe_acceptance_count` must remain `0`. A safe accepted decision must not hide a denied display, transition, or validation state.

## Demo

Run:

```text
python demo/run_amcf_cross_corridor_reporting_demo.py
```

Generated output is written to:

```text
output/amcf_cross_corridor_reporting/
```

Generated output is a local demo artifact and should not be committed.

## Not Implemented In This Phase

- printer driver integration
- scanner or camera capture
- image processing
- barcode or QR decoding
- PDF generation
- USB, serial, or firmware protocol
- GUI
- hardware validation
