# AMCF Tests File Review: Physical Medium Simulation Chain

This record covers the next ten physical-medium folders in descending
chronology:

- `Test AMCF_PHYSICAL_PRE_PROTOTYPE_OVERNIGHT_CONTINUATION`
- `Test AMCF_INTEGRATED_TRANSPORT_SCAN_GATE_SIMULATION`
- `Test AMCF_DETAILED_SCAN_GATE_SENSOR_MODEL`
- `Test AMCF_DETAILED_INDEXED_FEED_MECHANISM_SIMULATION`
- `Test AMCF_PHYSICAL_TRANSPORT_ACTUATION_FEASIBILITY_MODEL`
- both dated runs under `Test AMCF_NON_IDEAL_PHYSICAL_CARRIER_SIMULATION`
- `Test AMCF_PHYSICAL_CARRIER_RESEARCH_MATRIX_AND_SIMULATION_PLAN`
- `Test AMCF_CANONICAL_CONCEPT_ALIGNMENT`
- `Test AMCF_PRIMARY_ADAPTERS_AND_VERTICAL_STACK_PHYSICAL_DESIGN`
- `Test AMCF_VERTICAL_STACK_PHYSICAL_MEDIUM_SIMULATION`

## Complete File Disposition

| Group | Files | Disposition |
| --- | ---: | --- |
| Pre-prototype overnight continuation | 53 | physical planning/evidence |
| Integrated transport/scan-gate simulation | 45 | generated simulation evidence |
| Detailed scan-gate sensor model | 45 | model/planning evidence |
| Detailed indexed-feed simulation | 39 | generated simulation evidence |
| Transport actuation feasibility | 38 | mechanism model/evidence |
| Non-ideal physical carrier, both runs | 874 | generated simulation evidence |
| Physical carrier research matrix | 38 | research/planning evidence |
| Canonical concept alignment | 5 | concept/docs; one Main docs update recorded |
| Primary adapters and vertical-stack design | 11 | architecture/planning evidence |
| Ideal vertical-stack simulation | 1,169 | generated simulation evidence |
| **Total** | **2,317** | every file assigned |

The very large counts are primarily generated frames, captures, preview
sheets, CSV/JSON measurements, and reports. The source-run records and final
statuses were read; no generated media is a public runtime dependency.

## Accepted Digital/Software Meaning

The canonical-alignment run corrected the project definition to:

```text
video -> AMCF component/image representation -> AMCF playback -> reconstructed video
```

The physical branch is a later material carrier/reader/viewing path. The ideal
vertical-stack run simulated 288 aligned pages and 288 captured frames with
zero AMCF-versus-capture MAE and 99.0 PSNR under ideal registration. The older
physical-medium flipbook language was subsequently corrected toward
vertical-stack/indexed-section transport, fixed gates, timing markers, and
recovery logic.

The non-ideal run expanded the simulation with material proxies, feed modes,
ideal/mild/moderate/severe tiers, marker recovery, colour registry recovery,
reconstitution, pause/restart/reverse/seek, and tolerance thresholds. Its final
record says `NON_IDEAL_PHYSICAL_CARRIER_SIMULATION_READY`, but also says no
physical Level 5, mechanism proof, prototype, or hardware validation.

## Public And Main Comparison

The current public checkout contains a bounded software physical-medium
simulation surface:

- `src/amcf_physical_medium_simulation.py`;
- `demo/run_amcf_physical_medium_simulation_demo.py`;
- `tests/test_amcf_physical_medium_simulation.py`.

That public demo was run during this review and passed with
`final_passed: True` and `unsafe_acceptance_count: 0`.

The local `Main` folder does **not** currently contain those physical-medium,
physical-carrier, virtual-reader, or mechanical-player modules. Its current
surface contains the earlier `amcf_virtual_hardware.py` integration plus the
older Test 02/tracking/v-next files. This is a real Main-versus-public
integration gap to address in a later controlled sync; it is not a reason to
copy generated physical evidence or claim hardware.

The public physical-player sequence and software I/O branch are the newer
public implementation path. They should remain intact while deciding whether
the reusable physical-medium simulation module should also be promoted into
Main.

## Port Decision

| Material | Decision |
| --- | --- |
| Ideal software physical-medium simulation | Already present and tested publicly; compare/promote to Main later if desired |
| Non-ideal generated captures and preview media | Do not port as source; retain as local evidence |
| Sensor/transport/actuation plans | Documentation/future hardware evidence only |
| Main concept wording | Preserve corrected canonical definition |
| Real hardware interfaces | Do not implement in this parity pass |

No physical bench result in this group is accepted as real-world proof. The
public software simulation may be useful for the future CLI/app workflow, but
it must remain explicitly simulated.

## Status

`PUBLIC_IDEAL_SIMULATION_PRESENT; MAIN_PROMOTION_REVIEW_OPEN; PHYSICAL_EVIDENCE_NOT_CLAIMED`.

All 2,317 files are accounted for. Continue with the older public app/Level 5
and digital roadmap groups after this physical-medium chain. Keep the immediate
parity focus on digital AMCF, decoded playback, diagnostics, and reusable
software modules.

Claim boundary: hardware validation false; physical Level 5 false;
manufactured player false; real motors, sensors, cartridges, optics, printing,
scanning, and transport not validated; generated output committed no.
