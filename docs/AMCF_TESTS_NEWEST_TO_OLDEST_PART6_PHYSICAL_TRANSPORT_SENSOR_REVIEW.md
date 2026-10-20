# AMCF Tests Newest-To-Oldest Part 6 Physical Transport Sensor Review

Run context: `AMCF_TESTS_NEWEST_TO_OLDEST_PART6_PHYSICAL_TRANSPORT_SENSOR_REVIEW_V1`

Part 6 reviews the physical transport, sensor, scan-gate, material-coupon, and pre-prototype device planning band. Most of this band is future-hardware planning evidence. One software-only diagnostic helper from the material-coupon run was useful enough to port into the public repo.

## Claim Boundary

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- real printer integration claimed: false
- real scanner integration claimed: false
- real sensor validation claimed: false
- real player hardware claimed: false
- real coupon test claimed: false
- unsafe_acceptance_count: 0

## Folders Reviewed

| Local Tests folder | Evidence read | Result |
| --- | --- | --- |
| `Test AMCF_DUMMY_CARRIER_TRANSPORT_BUILD_CHECKLIST` | final status, build checklist, dummy carrier prep checklist, fixture prep checklist, logging templates, risk checklist | Planning/checklist package only. It explicitly does not claim real dummy transport tests, physical proof, or hardware validation. |
| `Test AMCF_DUMMY_CARRIER_TRANSPORT_TEST_PLAN` | final status, carrier design options, fixture concepts, test sequences, metrics logging, fail-closed policy | Planning/test protocol only. No public runtime code target. |
| `Test AMCF_TRANSPORT_SENSOR_INTEGRATED_BENCH_PLAN` | final status, integrated architecture, staged integration plan, sensor/transport interface model, sync/error/acceptance models | Planning/model package only. No real coupon scans, no integrated physical bench build, and no hardware validation. |
| `Test AMCF_MOTOR_ENCODER_TRANSPORT_DETAIL_MODEL` | final status, transport architecture, kinematic timing, feed variants, encoder feedback, error/stress models | Design/model evidence only. It identifies capstan encoder feed and hybrid marker feedback as planning candidates, not validated hardware. |
| `Test AMCF_BENCH_SENSOR_MOCKUP_BUILD_CHECKLIST` | final status, build prep, coupon prep, fixture prep, first real scan session plan | Checklist package only. Real scans were not performed. |
| `Test AMCF_PHYSICAL_BENCH_SENSOR_MOCKUP_SPEC` | final status, bench architecture, mechanical layout, scan fixture designs, acceptance criteria | Future bench mockup spec only. No full reader prototype or real scan validation claimed. |
| `Test AMCF_CIS_SENSOR_BENCH_TEST_PROTOCOL_EXPANSION` | final status, test objectives, material matrix, logging schema, procedures, analysis handoff | Protocol expansion only. It recommends future PET/Mylar-like coupon tests, but does not contain runtime code needing direct port. |
| `Test AMCF_SCAN_GATE_CIS_SENSOR_DETAIL_MODEL` | final status, CIS model, illumination/lane/timing/error/material matrices, synthetic sensor read simulation | Software/model evidence only. It remains a future bench protocol input, not real sensor validation. |
| `Test AMCF_PHYSICAL_DEVICE_PRE_PROTOTYPE_LAYOUT_PACKAGE` | final status, module geometry, dimensions, cartridge and scan-gate interfaces, risk package | Device layout package only. No prototype built. |
| `Test AMCF_PHYSICAL_DEVICE_CONCEPT_LAYOUT_REFINEMENT` | final status, form factor, carrier path, cartridge placement, scan gate placement, controls | Concept layout evidence only. No hardware or runtime code port target. |
| `Test AMCF_PHYSICAL_DEVICE_CONCEPT_APPEARANCE_SHEET` | final status and appearance/design docs | Concept appearance package only. No code port target. |
| `Test AMCF_MATERIAL_COUPON_SCAN_TEST_PLAN_EXPANSION_AND_SENSOR_PREP` | final status, coupon layout, simulated scan conditions, analysis script, synthetic analysis results, colour/marker robustness reports | Contains a reusable software-only coupon image analysis helper. This was ported as a public diagnostic module. |

## Ported In Part 6

The material-coupon analysis helper was ported as:

- `src/amcf_material_coupon_analysis.py`
- `demo/run_amcf_material_coupon_analysis_demo.py`
- `tests/test_amcf_material_coupon_analysis.py`
- `docs/AMCF_MATERIAL_COUPON_ANALYSIS_PARITY.md`

The port preserves the useful behavior:

- marker/registration/timing/index/colour/metadata/hash-lane proxy scoring
- synthetic coupon fixture generation for no-hardware testing
- JSON and CSV report output
- optional Pillow image analysis
- fail-closed behavior if image support is unavailable
- false claim-boundary flags for hardware validation, physical Level 5, manufactured player, real sensor validation, real scanner requirement, and real coupon test claims

## Validation

Focused validation passed:

- `python -m py_compile src/amcf_material_coupon_analysis.py demo/run_amcf_material_coupon_analysis_demo.py tests/test_amcf_material_coupon_analysis.py`
- `python -m unittest tests.test_amcf_material_coupon_analysis`
- `python demo/run_amcf_material_coupon_analysis_demo.py`

The demo writes generated output under:

- `output/amcf_material_coupon_analysis/`

Generated output is not committed.

## Part 6 Decision

Part 6 is closed as `PHYSICAL_TRANSPORT_SENSOR_PLANS_REVIEWED_MATERIAL_COUPON_ANALYSIS_PORTED`.

Most of this band stays as planning evidence because it describes future physical transport/sensor/mockup/prototype work. The material-coupon analyzer is the only accepted software diagnostic port from this slice.

## Next Part

Continue downward through the earlier non-ideal physical carrier, integrated transport/scan-gate simulation, detailed indexed feed mechanism, transport actuation feasibility, vertical-stack physical medium, canonical concept alignment, and physical medium simulation folders.

Those runs may include more simulation code, so inspect scripts and generated reports before deciding whether they are already covered by the current physical-player simulator or need a public-safe port.
