# AMCF Player PC Software Path

## Purpose

`AMCF_PLAYER_PC_RUNTIME_FIXTURE_PROTOTYPE_V1` adds a simulated Player <-> PC software-control bridge.

It checks fixture package compatibility against a simulated capability profile and writes a command/session transcript for later hardware alignment.

## Allowed In This Phase

- simulated player profile
- package compatibility check
- command/session transcript
- bounded reverse/seek handling
- fail-closed denial for arbitrary physical seek
- diagnostics

## Not Implemented

- real player hardware
- USB
- serial
- firmware protocol
- hardware detection
- real motors, sensors, or cartridges

## Claim Boundary

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- real player communication claimed: false
- arbitrary physical seek claimed: false

## Demo

Run:

```text
python demo/run_amcf_player_pc_runtime_fixture_demo.py
```

Generated output is written under:

```text
output/amcf_player_pc_runtime_fixture/
```

Generated output should not be committed.
