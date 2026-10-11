# AMCF Hardware / Software Paths

The AMCF package is software-first. Current implementation is software and virtual hardware support. Future physical paths are represented by abstractions and documentation only.

## Path A - Pure software

```text
source video -> AMCF digital -> software runtime/player/viewer
```

This is the canonical software path. It does not require physical media or hardware.

## Path B - Virtual hardware

```text
AMCF digital -> virtual cartridge -> virtual reader -> virtual scan gate -> player handoff -> software player/viewer
```

This path emulates future physical-reader behavior in software. It supports validation/fail-closed behavior and player-facing state without requiring real sensors, cartridges, motors, or scans.

## Path C - Future physical reader/recovery

```text
AMCF physical media -> physical reader/scanner -> validation/recovery -> AMCF digital state/export
```

The physical reader/recovery path is scan oriented. It reads AMCF physical media lanes and can reconstruct, validate, diagnose, or export digital AMCF state if needed.

## Path D - Future physical mechanical/optical playback

```text
AMCF physical media -> indexed transport -> fixed physical view gate -> illumination/optical presentation -> direct human viewing without digital screen
```

This is the corrected physical-player path. Playback is physical/mechanical/optical and should not be collapsed into a software UI viewer, tablet, monitor, or normal digital display path.

## Path E - Hybrid reader-player appliance

```text
AMCF physical media -> shared transport -> physical view gate for direct viewing + reader lane for optional recovery/diagnostics
```

A future appliance may combine physical playback and reader/recovery, but the roles remain separate.

## Current implementation status

- Implemented now: Path A support and Path B virtual hardware support.
- Documented/future: Path C, Path D, and Path E.
- No manufactured hardware exists in this package.
- No hardware validation, physical proof, physical Level 5, final UI, manufacturing readiness, or prototype build is claimed.
