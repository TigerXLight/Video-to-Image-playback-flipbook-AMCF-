# AMCF Tests File Review: Physical Research And Bench Plans

This record covers the next 12 physical-research folders in descending
chronology:

- `Test AMCF_DUMMY_CARRIER_TRANSPORT_BUILD_CHECKLIST`
- `Test AMCF_DUMMY_CARRIER_TRANSPORT_TEST_PLAN`
- `Test AMCF_TRANSPORT_SENSOR_INTEGRATED_BENCH_PLAN`
- `Test AMCF_MOTOR_ENCODER_TRANSPORT_DETAIL_MODEL`
- `Test AMCF_BENCH_SENSOR_MOCKUP_BUILD_CHECKLIST`
- `Test AMCF_PHYSICAL_BENCH_SENSOR_MOCKUP_SPEC`
- `Test AMCF_CIS_SENSOR_BENCH_TEST_PROTOCOL_EXPANSION`
- `Test AMCF_SCAN_GATE_CIS_SENSOR_DETAIL_MODEL`
- `Test AMCF_PHYSICAL_DEVICE_PRE_PROTOTYPE_LAYOUT_PACKAGE`
- `Test AMCF_PHYSICAL_DEVICE_CONCEPT_LAYOUT_REFINEMENT`
- `Test AMCF_PHYSICAL_DEVICE_CONCEPT_APPEARANCE_SHEET`
- `Test AMCF_MATERIAL_COUPON_SCAN_TEST_PLAN_EXPANSION_AND_SENSOR_PREP`

These groups are physical planning and future-evidence preparation. They are
not digital AMCF runtime implementations and must not be treated as hardware
validation.

## Complete File Disposition

| Folder | Files | File character | Disposition |
| --- | ---: | --- | --- |
| Dummy-carrier build checklist | 37 | plans, CSV schemas, board, JSON | `GENERATED_EVIDENCE_NOT_SOURCE` |
| Dummy-carrier transport test plan | 33 | plans, error rules, logs, board | `GENERATED_EVIDENCE_NOT_SOURCE` |
| Integrated transport/sensor bench plan | 39 | bench plan, metrics, reports | `GENERATED_EVIDENCE_NOT_SOURCE` |
| Motor/encoder transport detail model | 44 | mechanism comparisons, models, reports | `GENERATED_EVIDENCE_NOT_SOURCE` |
| Bench sensor mockup build checklist | 35 | build/checklist planning | `GENERATED_EVIDENCE_NOT_SOURCE` |
| Physical bench sensor mockup spec | 39 | sensor/fixture specification | `GENERATED_EVIDENCE_NOT_SOURCE` |
| CIS sensor bench protocol expansion | 39 | protocol, analysis, CSV/JSON | `GENERATED_EVIDENCE_NOT_SOURCE` |
| Scan-gate CIS sensor detail model | 39 | scan-gate model and reports | `GENERATED_EVIDENCE_NOT_SOURCE` |
| Physical device pre-prototype layout | 38 | layout package and board | `GENERATED_EVIDENCE_NOT_SOURCE` |
| Physical device layout refinement | 36 | appearance/layout decisions | `GENERATED_EVIDENCE_NOT_SOURCE` |
| Physical device appearance sheet | 11 | concept board and descriptions | `DOC_ONLY` |
| Material-coupon scan/sensor preparation | 104 | protocols, synthetic media, reports | `GENERATED_EVIDENCE_NOT_SOURCE` |
| **Total** | **494** | every file assigned | no runtime port justified |

The `.cmd` and `run_*.py` files orchestrate local planning/report generation;
they are not public runtime modules. CSV/JSON/Markdown files are plans or
evidence structures. HTML/SVG/PNG/JPG files are visual/reference or synthetic
planning artifacts. No source file in this block is an accepted digital AMCF
encoder, decoder, archive, reader, or player implementation.

## What The Records Establish

The progression is coherent and directional:

1. device appearance and internal layout were explored;
2. indexed feed and scan-gate concepts were detailed;
3. CIS sensor and bench mockup protocols were expanded;
4. transport/sensor integration and motor/encoder options were compared;
5. dummy-carrier transport fixtures, error injection, logging, and fail-closed
   decisions were prepared;
6. real coupon/sensor scans and repeatable transport evidence remained the
   required next physical evidence.

The plans preserve useful future requirements such as timing/index markers,
registration, colour lanes, checksum/hash lanes, repeatability metrics,
position error, slip/skew/curl/jam flags, rescan/reject decisions, and
`unsafe_acceptance` staying zero. Those concepts already align with the public
software carrier/reader and physical-player safety models, but the planning
records themselves are not runtime code to copy.

## Main And Public Comparison

The final status records for these folders consistently report:

- `Main modified: false`;
- `prior runs modified: false`;
- packages installed: false;
- deep tools run: false;
- physical Level 5 claimed: false;
- physical mechanism proven: false;
- physical prototype built: false;
- real scans performed: false;
- hardware validated: false;
- transport proof claimed: false.

Therefore these separated physical progressions were **not** integrated into
Main as real hardware behavior. Their accepted software implications were
already represented elsewhere through the virtual reader, fail-closed lane
validation, carrier metadata, physical-medium simulation, and physical-player
simulator documentation. The public repository must keep those software models
without pretending that a CIS sensor, motor/encoder bench, coupon, or dummy
carrier has been built or validated.

## Port Decision

`DO_NOT_PORT_AS_RUNTIME_HARDWARE`.

No implementation change is justified from these folders. A later physical
evidence run may use their schemas and acceptance rules, but that would be a
separate hardware/evidence task requiring real artifacts and explicit review.
For the present digital parity goal, these folders are context and future-test
requirements, not missing video-to-AMCF or AMCF-to-decoded-video code.

## Status

`CLOSED_AS_PHYSICAL_PLANNING_EVIDENCE`.

All 494 files are accounted for. No generated planning output, visual board,
bench checklist, sensor protocol, or local orchestrator is to be added to the
public runtime package merely because it exists in `Tests`.

Claim boundary: hardware validation false; physical Level 5 false;
manufactured player false; real motors, sensors, cartridges, optics, printing,
scanning, and transport not validated; generated output committed no.
