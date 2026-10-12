# AMCF Hardware / Software Paths

The AMCF package is software-first. Current implementation is software and virtual hardware support. Future physical paths are represented by abstractions and documentation only.

Digital AMCF is the canonical AMCF representation, scheduler, and validation model. Physical AMCF is the material embodiment of the same AMCF timing/update structure. Reader paths recover or verify physical AMCF back into digital AMCF; player paths physically/optically present AMCF media according to that same dynamic schedule.

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
AMCF physical media -> folded indexed transport -> A/B staging gates -> fixed physical view gate -> shuttered illumination/optical presentation -> direct human viewing without digital screen
```

This is the corrected physical-player path. Playback is physical/mechanical/optical and should not be collapsed into a software UI viewer, LCD/OLED tablet, monitor, or normal digital display path.

The preferred future physical mechanism is dynamic rather than fixed-FPS page playback. It should hold the current section at the visible gate, preload the next required section in a hidden A/B staging gate, blank the optical path during the transition, and fail closed if the next section is not verified in time. This physical motion follows the AMCF update schedule defined and validated digitally.

Current software/control stages for this path include the physical-player state machine, fail-closed safety model, bounded reverse/seek controls, mechanism profiles, and integrated simulator demo. Future hardware should align to these control contracts. Hardware proof remains future work.

## Path E - Hybrid reader-player appliance

```text
AMCF physical media -> shared folded transport -> physical view gate for direct viewing + reader/prefetch lane for optional recovery/diagnostics
```

A future appliance may combine physical playback and reader/recovery, but the roles remain separate.

## Current implementation status

- Implemented now: Path A support, Path B virtual hardware support, and Path D software/control simulator stages for future physical-player alignment.
- Documented/future hardware: Path C, physical Path D hardware, and Path E.
- No manufactured hardware exists in this package.
- No hardware validation, physical proof, physical Level 5, final UI, manufacturing readiness, or prototype build is claimed.
