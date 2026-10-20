# AMCF Tests Newest-To-Oldest Part 7 Physical Medium Simulation Review

Part 7 reviewed the physical-medium and integrated transport simulation band immediately below the material-coupon planning folders.

## Folder Band Reviewed

- physical pre-prototype overnight continuation
- integrated transport scan-gate simulation
- detailed scan-gate sensor model
- detailed indexed-feed mechanism simulation
- physical transport actuation feasibility model
- non-ideal physical-carrier simulation
- physical-carrier research matrix and simulation plan
- canonical concept alignment
- primary adapters and vertical-stack physical design
- vertical-stack physical-medium simulation
- physical-medium flipbook simulation
- single-app main entrypoint configuration and layout evidence

## Findings

The newest folders in this band are mostly planning, acceptance-gate, and physical design evidence. They should not be copied wholesale into the public repo because they are local generated run folders and contain planning artifacts rather than maintained public source modules.

The useful public-safe behavior is the no-hardware simulation summary:

- ideal vertical-stack transport preserves AMCF playback under aligned capture
- ideal sequential carrier simulation preserves AMCF playback under aligned capture
- non-ideal carrier recovery cases preserve order and recovery in the accepted summarized cases
- control-event summaries track pause, restart, reverse, seek, recovery, and damage-risk proxy values
- all claim-boundary flags stay false
- unsafe_acceptance_count remains 0

## Public Action

Part 7 adds:

- `src/amcf_physical_medium_simulation.py`
- `demo/run_amcf_physical_medium_simulation_demo.py`
- `tests/test_amcf_physical_medium_simulation.py`
- `docs/AMCF_PHYSICAL_MEDIUM_SIMULATION_PARITY.md`

This is a software diagnostics parity layer only. It is not a hardware validation layer.

## Claim Boundary

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- real sensor validation claimed: false
- real motor validation claimed: false
- real cartridge validation claimed: false
- real optics validation claimed: false
- unsafe_acceptance_count: 0
