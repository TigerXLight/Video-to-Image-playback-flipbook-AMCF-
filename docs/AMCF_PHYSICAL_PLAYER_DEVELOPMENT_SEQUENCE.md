# AMCF Physical Player Development Sequence

## Stage 1

`AMCF_PHYSICAL_PLAYER_SIMULATOR_MODELS_V1`

Model foundation for folded-path A/B physical-player simulation. In this repository, the current foundation is represented by the mechanical/optical simulator and Physical I/O architecture files.

## Stage 2

`AMCF_PHYSICAL_PLAYER_STATE_MACHINE_V1`

Implemented in this run.

Provides:

- safe forward playback cycle
- deterministic state transitions
- event logs
- fail-closed integration
- local reverse/seek denial basics
- software/control simulator framing

This stage does not mark physical hardware as complete.

## Stage 3

`AMCF_PHYSICAL_PLAYER_FAIL_CLOSED_V1`

Implemented in this run.

Provides:

- failure hardening for section verification and transition safety
- structured safety decisions
- expanded fail-closed reason catalogue
- unsafe acceptance audit
- deterministic failure demo
- unit tests for marker, hash, index, gate, shutter, illumination, jam, feed, and audio-sync safety paths

This stage does not mark physical hardware as complete and does not claim hardware validation.

## Later Stages

Later work may add richer physical-player model bundles, PC recognition/control simulation, hardware adapter boundaries, and end-to-end Physical I/O simulation. Those later stages must preserve the claim boundary: no hardware validation is claimed until real hardware tests exist.
