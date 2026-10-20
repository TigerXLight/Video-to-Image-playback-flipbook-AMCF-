# AMCF Tests Newest-To-Oldest Part 4 Pre-GitHub Audit And Concept Review

Run context: `AMCF_TESTS_NEWEST_TO_OLDEST_PART4_PRE_GITHUB_AUDIT_AND_CONCEPT_REVIEW_V1`

Part 4 continues downward through the pre-GitHub coverage-audit, physical analog/player concept correction, clean-package preparation, and release-readiness folders immediately below the Part 3 functional path runs.

This band is important historically because it explains why later pre-GitHub implementation runs were created. It is not the newest accepted implementation surface for source-frame AMCF encoding, physical carrier generation, virtual reader recovery, or mechanical/optical player simulation.

## Claim Boundary

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- real printer integration claimed: false
- real scanner integration claimed: false
- real player hardware claimed: false
- unsafe_acceptance_count: 0

## Folders Reviewed

| Local Tests folder | Evidence read | Result |
| --- | --- | --- |
| `Test AMCF_PRE_GITHUB_FULL_FUNCTIONAL_COVERAGE_AUDIT_PART1` | `FINAL_STATUS.md`, required path coverage matrix, path-specific checks | Historical audit. It reported Path A source video/source frames to AMCF digital as `MISSING` and recommended the later `AMCF_PRE_GITHUB_VIDEO_TO_AMCF_DIGITAL_SMOKE_DEMO` run. Part 3 already reviewed that later run and verified the public repo contains the corresponding source-frame path. |
| `Test AMCF_PHYSICAL_ANALOG_PLAYER_CONCEPT_PART2_CLEAN_PACKAGE_DOCS` | final status, clean package source/docs/tests, validation result | Clean package docs/status pass. Source modules `src/amcf_virtual_hardware.py`, `src/amcf_vnext.py`, and `demo/run_virtual_hardware_demo.py` are byte-identical in the current public repo. Several docs differ because public docs have since expanded substantially. |
| `Test AMCF_PHYSICAL_ANALOG_PLAYER_CONCEPT_PART1_ARCHITECTURE_CORRECTION` | final status and patch-plan outputs | Concept/architecture correction only. It did not modify Main or the clean package directly; later Part 2 clean package docs applied the correction. |
| Clean package prep test folder | final status and package-prep reports | Historical clean-package preparation. It passed validation, path cleanup, generated-output policy, README patching, tests, and demo, while leaving public license/publication decisions for later. Current public repo contains later license/publication and package-review layers. |
| `Test AMCF_GITHUB_RELEASE_READINESS_AUDIT` | final status and final readiness verdict | Historical release-readiness audit. It was `READY_AFTER_MINOR_CLEANUP`, with later cleanup required for license/publication and security/privacy. Current public repo contains later clean-package prep, public-docs, release-review, package-refresh, closeout, and tag-prep work. |

## Code Comparison

The Part 4 implementation-bearing clean package snapshot was compared against the current public repo:

| File | Comparison result | Decision |
| --- | --- | --- |
| `src/amcf_virtual_hardware.py` | Byte-identical | Covered. |
| `src/amcf_vnext.py` | Byte-identical | Covered. |
| `demo/run_virtual_hardware_demo.py` | Byte-identical | Covered. |
| `tests/test_release_package.py` | Different | Public version is the same test surface with a small public-safe artifact scan adjustment for `.git`, `__pycache__`, and `.pyc` files. Do not replace with older code. |
| `docs/AMCF_PHYSICAL_MEDIUM_BOUNDARY.md` | Byte-identical | Covered. |
| `docs/PHYSICAL_PLAYER_VISUAL_REFERENCE_NOTE.md` | Byte-identical | Covered. |
| `docs/PLAYER_UI_VIEWER_STUB.md` | Byte-identical | Covered. |
| `docs/SOFTWARE_FIRST_HARDWARE_SUPPORT.md` | Byte-identical | Covered. |
| `docs/OPTIONAL_DEEP_TOOL_ADAPTERS.md` | Byte-identical | Covered. |
| `examples/sample_virtual_cartridge.json` | Byte-identical | Covered. |
| `examples/sample_player_ui_state.json` | Byte-identical | Covered. |

The differing README, quickstart, claim-boundary, canonical concept, physical-player concept, hardware/software paths, and software/physical boundary files are expected: the public repo now includes newer software I/O, physical-player, release/package, and app workflow documentation. The older docs should not overwrite the newer public package.

## Validation

Current public demo run:

- `demo/run_virtual_hardware_demo.py`: passed
- accepted count: `6`
- rescanned count: `3`
- rejected count: `2`
- degraded count: `1`
- unsafe_acceptance_count: `0`

## Part 4 Decision

Part 4 is closed as `COVERED_OR_SUPERSEDED_BY_LATER_PUBLIC_PACKAGE`.

No runtime code port is needed from this band because:

- the implementation-bearing virtual-hardware and vnext modules are byte-identical
- the relevant demo is byte-identical and passes in the current repo
- the older Path A missing finding was deliberately resolved by the later source-frame to AMCF run reviewed in Part 3
- the older release/package cleanup findings are superseded by later public package, release-review, closeout, tag-prep, and app-readiness work
- the current public docs are newer and should not be overwritten by earlier concept/package docs

## Next Part

Continue downward through the virtual-hardware release refresh, player UI state viewer, virtual reader/main integration, software virtual physical reader emulator, visual-stage closeout, player UI playback interface concept, and related physical-device planning folders.

For the next slice, inspect code and runnable demos first, because some folders may contain actual virtual hardware/player UI behavior while others are planning evidence only.
