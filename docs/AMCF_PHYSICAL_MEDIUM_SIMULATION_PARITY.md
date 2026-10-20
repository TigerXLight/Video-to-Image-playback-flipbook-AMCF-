# AMCF Physical Medium Simulation Parity

This document records the public-safe port of accepted no-hardware physical-medium simulation evidence from the local progression folders.

The port is a software diagnostics layer. It does not claim real hardware validation, physical Level 5 completion, manufactured-player completion, real sensor validation, real motor validation, real cartridge validation, or real optical validation.

## What Was Ported

- ideal vertical-stack aligned page transport equivalence summary
- ideal sequential carrier equivalence summary
- non-ideal physical-carrier recovery case summaries
- control-event recovery summaries for pause, restart, reverse, and seek behavior
- claim-boundary flags and unsafe-acceptance accounting

The reusable public module is `src/amcf_physical_medium_simulation.py`.

## Source Evidence

This parity layer summarizes the local physical-medium simulation band reviewed in newest-to-oldest Part 7:

- physical pre-prototype continuation planning
- integrated transport and scan-gate simulation
- detailed scan-gate sensor model
- detailed indexed-feed mechanism simulation
- physical transport actuation feasibility model
- non-ideal physical-carrier simulation
- physical-carrier research matrix
- canonical concept alignment
- primary adapters and vertical-stack physical design
- vertical-stack physical-medium simulation
- physical-medium flipbook simulation
- single-app main entrypoint and layout evidence

These folders are treated as local evidence, not as generated public release assets.

## Current Public Status

| Area | Status |
| --- | --- |
| vertical-stack equivalence | public summary implemented |
| ideal sequential carrier equivalence | public summary implemented |
| non-ideal marker/order recovery | public summary implemented |
| pause/restart/reverse/seek control-event summary | public summary implemented |
| real physical sensor input | not claimed |
| real physical transport validation | not claimed |
| manufactured-player proof | not claimed |

## Validation

Run:

```text
python demo/run_amcf_physical_medium_simulation_demo.py
python -m unittest tests.test_amcf_physical_medium_simulation
python -m unittest discover -s tests
```

Generated reports go under `output/amcf_physical_medium_simulation/` and must not be committed.

## Claim Boundary

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- real sensors validated: false
- real motors validated: false
- real cartridges validated: false
- real optics validated: false
- unsafe_acceptance_count: 0
