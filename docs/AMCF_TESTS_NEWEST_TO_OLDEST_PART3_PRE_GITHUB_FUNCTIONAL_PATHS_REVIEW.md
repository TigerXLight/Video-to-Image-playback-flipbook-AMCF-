# AMCF Tests Newest-To-Oldest Part 3 Pre-GitHub Functional Paths Review

Run context: `AMCF_TESTS_NEWEST_TO_OLDEST_PART3_PRE_GITHUB_FUNCTIONAL_PATHS_REVIEW_V1`

Part 3 continues downward through the implementation-bearing pre-GitHub functional path folders. This review compares source/demo/test files from the latest combined pre-GitHub clean package against the current public repo, runs the matching public demos, and records whether anything must be ported.

This is a code-surface and behavior check, not a generated-output identity claim.

## Claim Boundary

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- real printer integration claimed: false
- real scanner integration claimed: false
- real player hardware claimed: false
- unsafe_acceptance_count: 0

## Folders Reviewed

| Local Tests folder | Final status evidence | Public repo result |
| --- | --- | --- |
| `Test AMCF_PRE_GITHUB_VIDEO_TO_AMCF_DIGITAL_SMOKE_DEMO` | Source-frame generator, digital encoder, digital validator, demo, and tests passed for generated source frames to AMCF digital. Arbitrary real video was not claimed in that run. | Public source-frame demo and tests are present. The public encoder/validator are newer because they also support optional audio payload metadata from later video-pipeline parity work. |
| `Test AMCF_PRE_GITHUB_AMCF_TO_PRINTABLE_PHYSICAL_CARRIER_GENERATOR` | AMCF digital to printable/indexed physical carrier package passed as no-hardware output. Actual physical printing was not claimed. | Public carrier module, demo, and tests are byte-identical to the latest pre-GitHub clean package. |
| `Test AMCF_PRE_GITHUB_VIRTUAL_READER_RECOVERY_EXPORT_DEMO` | Virtual carrier reader, recovered AMCF state, and recovered frame export passed. Real scanning and MP4 container export were not claimed in that run. | Public virtual reader module, demo, and tests are byte-identical to the latest pre-GitHub clean package. |
| `Test AMCF_PRE_GITHUB_MECHANICAL_OPTICAL_PLAYER_SIMULATOR` | Mechanical/optical player simulator passed as software-only; controls, timeline validation, view-gate states, and unsafe acceptance protection passed. | Public demo is byte-identical. Public simulator and tests are newer because they add dynamic update scheduling, A/B staging, hidden gate, transition blanking, prefetch timing, and fail-closed validation for unverified next staging sections. |

## File Comparison

The comparison used the latest combined clean package from the mechanical/optical player simulator run because it contains the earlier pre-GitHub source-frame, physical-carrier, virtual-reader, and mechanical-player files together.

| File | Comparison result | Decision |
| --- | --- | --- |
| `src/amcf_digital_encoder.py` | Different | Public version is a superset. It keeps source-frame archive behavior and adds optional audio payload handling, source-video metadata, and capability flags. Do not replace with older code. |
| `src/amcf_digital_validator.py` | Different | Public version is a superset. It keeps frame-payload validation and adds optional audio payload validation. Do not replace with older code. |
| `src/amcf_physical_carrier.py` | Byte-identical | Covered. |
| `src/amcf_virtual_carrier_reader.py` | Byte-identical | Covered. |
| `src/amcf_mechanical_optical_player.py` | Different | Public version is a superset. It adds dynamic update schedule, hidden staging gate, visible gate state fields, transition blanking, prefetch timing, reverse buffer depth, and stricter fail-closed checks. Do not replace with older code. |
| `demo/run_source_frames_to_amcf_digital_demo.py` | Byte-identical | Covered. |
| `demo/run_amcf_to_physical_carrier_demo.py` | Byte-identical | Covered. |
| `demo/run_virtual_reader_recovery_export_demo.py` | Byte-identical | Covered. |
| `demo/run_mechanical_optical_player_simulator_demo.py` | Byte-identical | Covered. |
| `tests/test_source_frames_to_amcf_digital.py` | Byte-identical | Covered. |
| `tests/test_amcf_to_physical_carrier.py` | Byte-identical | Covered. |
| `tests/test_virtual_reader_recovery_export.py` | Byte-identical | Covered. |
| `tests/test_mechanical_optical_player_simulator.py` | Different | Public tests are a superset. They add dynamic A/B staging field coverage and fail-closed rejection for an unverified next staging section. |

## Public Demo Validation

The current public repo demos passed for this Part 3 slice:

- `demo/run_source_frames_to_amcf_digital_demo.py`: passed, archive created, 8 frame payloads validated, `unsafe_acceptance_count: 0`
- `demo/run_amcf_to_physical_carrier_demo.py`: passed, 8 carrier sections generated, lane layout present, `unsafe_acceptance_count: 0`
- `demo/run_virtual_reader_recovery_export_demo.py`: passed, 8 sections recovered, recovered AMCF archive and recovered frames created, `unsafe_acceptance_count: 0`
- `demo/run_mechanical_optical_player_simulator_demo.py`: passed, carrier loaded, view-gate states generated, timeline generated, controls simulated, `unsafe_acceptance_count: 0`

The demos wrote local generated artifacts under `demo/output/`. Those artifacts are generated output and are not part of the committed source package.

## Part 3 Decision

Part 3 is closed as `COVERED_BY_PUBLIC_SOURCE_WITH_NEWER_SUPERSETS`.

No runtime code port is needed from these folders because:

- the physical-carrier and virtual-reader modules are already byte-identical
- the source-frame encoder/validator are present and have been extended for later optional audio/video parity work
- the mechanical/optical player simulator is present and has been extended with the later folded A/B staging and fail-closed behavior
- the public demos for this slice still pass
- no hardware, manufacturing, physical Level 5, real printer, real scanner, or real player claims are introduced

## Next Part

Continue downward through the next local `Tests` folders, using the same pattern:

1. read final status/report files
2. inspect source/demo/test code and manifests
3. compare against public repo code, not just folder names
4. run the matching public demos/tests where possible
5. port only missing accepted behavior, not rejected older methods or generated outputs
