# AMCF Tests File-Level Coverage Baseline

The Parts 1-15 newest-to-oldest review reached the oldest named test folder, but it did **not** inspect all nested files in the `Tests` tree. Its folder summaries cannot establish complete local-to-public code, behavior, diagnostic, or output parity. This document corrects that scope error and starts an auditable file-level review.

## Complete Path Inventory

Run `python demo/run_amcf_tests_file_coverage_inventory.py` from the public repo root. The standard-library script inventories hidden and nested files beneath the local workspace `Tests` tree. It writes split JSONL manifests and `inventory_summary.json` under ignored `output/amcf_tests_file_coverage_inventory/`. The report's own directory is excluded to avoid self-counting; other generated files are inventoried, not treated as source truth. Symlinks are listed but not followed. Each row has a repo-independent relative path, byte count, coarse file kind, and `review_status: UNREVIEWED`. The inventory does not open archive members, read source contents, execute tests, compare outputs, or decide parity.

The initial run completed without traversal errors:

| Kind | Files |
| --- | ---: |
| Code or runnable | 2,320 |
| Data or metadata | 55,137 |
| Documents | 23,650 |
| Media | 58,598 |
| Archive files, members unopened | 423 |
| Other | 2,447 |
| **Total** | **142,575** |

All 185 top-level `Tests` folders contain inventoried files. The manifest is split into 11 parts, each below the release-package test's 5 MB file threshold. Generated inventory is ignored and must not be committed.

## Review Status

- Complete path enumeration: yes, for the current filesystem snapshot.
- Contents reviewed for every file: no.
- Every nested run tested: no.
- Every archive member inspected: no.
- `Main` to public file-by-file comparison complete: no.
- Full digital AMCF functional and diagnostic parity proven: no.
- Full output or performance parity proven: no.

The Part 1-15 documents provide useful evidence for selected folders, files, and runs; they are **not** a per-file sign-off ledger. A literal-name cross-check also found 82 of the 185 top-level folder names absent from those Part documents. Some may be covered by shorthand group descriptions, but that cannot be counted as verified coverage.

The first content-comparison pass is recorded in `docs/AMCF_TESTS_CODE_HASH_COMPARISON.md`. It hashes code/runnable files against `Main` and tracked public code but leaves semantic and acceptance decisions open.

The first complete per-file batch is recorded in `docs/AMCF_TESTS_FILE_REVIEW_TEST02_20261013_071127.md`: all 343 files across seven four-frame `Test 02` reruns were path/hash compared, with the varying archive metadata and decoded state hashes checked separately. Those local runs retain their own final-acceptance FAIL verdict.

The next batch is `docs/AMCF_TESTS_FILE_REVIEW_TEST02_20261003_165701.md`: the older 288-frame `Test 02` run has 275 file-level hash/format records, archive-payload matching, and 288 public-decoder state-hash matches. It also retains its final-acceptance FAIL verdict. These two batches do not close the rest of `Tests`.

The next completed folder-level batch is `docs/AMCF_TESTS_FILE_REVIEW_LEGACY_TEST01_WATERFALL.md`: all 10 files in `Legacy Test 01/AMCF_Waterfall_Test_01` were hashed and inspected, including the four-member custom archive and its manifest/events/audio payloads. The prototype's intermediate decode hashes passed, but its own report rejects quality-equivalent compression at reduced resolution. It is historical failed evidence, not a runtime port, and does not close the remaining `Tests` inventory.

The next implementation-bearing batch is `docs/AMCF_TESTS_FILE_REVIEW_PRE_GITHUB_VIDEO_TO_AMCF_DIGITAL_SMOKE.md`: all 45 files in the pre-GitHub source-frame-to-AMCF run were hashed and accounted for. The clean-package source/demo/test path is exact or publicly superseded by tested extensions; the run-local orchestrator and generated reports/media are not copied. This closes that folder only and does not close the broader `Tests` inventory.

The following batch is `docs/AMCF_TESTS_FILE_REVIEW_PRE_GITHUB_PRINTABLE_PHYSICAL_CARRIER.md`: all 50 files in the pre-GitHub carrier-generator run were hashed and accounted for. The carrier module, demo, and test are exact in the public repo; the run-local wrapper and generated carrier ZIP are not copied. This closes the software carrier-plan folder only and does not claim real printing or broader `Tests` parity.

The next batch is `docs/AMCF_TESTS_FILE_REVIEW_PRE_GITHUB_VIRTUAL_READER.md`: all 55 files in the pre-GitHub virtual-reader recovery/export run were hashed and accounted for. The reader module, demo, and test are exact in the public repo; the run-local wrapper and generated recovery ZIP are not copied. This closes the virtual no-hardware readback folder only and does not claim real scanning or broader `Tests` parity.

The next batch is `docs/AMCF_TESTS_FILE_REVIEW_PRE_GITHUB_MECHANICAL_OPTICAL_PLAYER.md`: all 60 files in the pre-GitHub mechanical/optical simulator run were hashed and accounted for. The public simulator demo is exact, while the current simulator module and tests are newer tested supersets. This closes that software-only physical-player folder without claiming hardware or broader `Tests` parity.

The next completed batch is `docs/AMCF_TESTS_FILE_REVIEW_PRE_GITHUB_FINAL_FUNCTIONAL_CONFIDENCE.md`: all 183 files in the dated pre-GitHub confidence audit were assigned a disposition. The 48 reviewable package files are all present at the same public paths; 34 are exact and 14 are newer public equivalents. Audit reports, orchestration, generated outputs, and caches were kept as evidence or excluded from source parity. This closes the confidence folder only and does not close the broader `Tests` inventory.

The next completed batch is `docs/AMCF_TESTS_FILE_REVIEW_PUBLIC_GITHUB_PAGES_SITE_PREP.md`: all 1,166 files in the Pages-prep handoff were assigned a disposition. Its 355 non-generated package files match the current public checkout at the same paths and SHA-256 hashes; generated demo output, caches, ZIPs, orchestration, and evidence remain excluded from source parity. This closes the Pages-prep folder only and does not close the broader local workspace.

The next completed batch is `docs/AMCF_TESTS_FILE_REVIEW_PUBLIC_ASSETS_AND_PREPUBLIC_CONTEXT.md`: all 175 files across the public asset/upload and pre-public Main/context folders were assigned a disposition. Their 116 package source files are all present in the current public checkout, with no missing paths; changed files are newer public metadata, assets, docs, or tested modules. Generated output, caches, ZIPs, and handoff evidence remain excluded from source parity.

The next completed batch is `docs/AMCF_TESTS_FILE_REVIEW_PRE_GITHUB_FULL_FUNCTIONAL_COVERAGE_AUDIT.md`: all 24 files in the earlier full-coverage audit were accounted for. Its historical missing/partial path statuses are superseded by the later source-frame, carrier, reader, and mechanical-player evidence; all 26 referenced reusable package files are present today, with 17 exact and 9 newer public equivalents.

The next completed batch is `docs/AMCF_TESTS_FILE_REVIEW_PHYSICAL_ANALOG_PLAYER_CONTEXT.md`: all 64 files across the Part 1 architecture-correction and Part 2 clean-package documentation folders were accounted for. The 26 reusable Part 2 package files are all present publicly, with 17 exact and 9 newer public equivalents; Part 1 remains evidence/planning only.

The next completed batch is `docs/AMCF_TESTS_FILE_REVIEW_PACKAGE_PREP_VIRTUAL_HARDWARE_VIEWER.md`: all 208 files across eight package-prep, release-readiness, virtual-hardware, viewer, reader-emulator, and concept groups were accounted for. The reusable package source from the package-producing groups is all present publicly; historical behavior is represented by consolidated current modules and tests, without duplicating run-local files or generated output.

The next completed batch is `docs/AMCF_TESTS_FILE_REVIEW_PHYSICAL_RESEARCH_BENCH_PLANS.md`: all 494 files across the 12 physical-research, sensor, transport, dummy-carrier, coupon, and concept groups were accounted for. They are planning/evidence artifacts with no physical validation and no runtime port justified; their software implications remain represented by the existing virtual/carrier/player safety layers.

The next completed batch is `docs/AMCF_TESTS_FILE_REVIEW_PHYSICAL_MEDIUM_SIMULATION_CHAIN.md`: all 2,317 files across the physical-medium, vertical-stack, non-ideal, transport, and concept-alignment groups were accounted for. The current public ideal physical-medium simulation passes; local Main does not yet contain that reusable module, so Main promotion remains an explicit later parity task. Generated captures and bench evidence are not source.

The next completed batch is `docs/AMCF_TESTS_FILE_REVIEW_PHYSICAL_MEDIUM_AND_SINGLE_APP.md`: all 1,196 files across the ideal physical-medium and single-app/Main-entrypoint folders were accounted for. `Main/amcf_vnext.py` and public `src/amcf_vnext.py` are byte-identical, as are the virtual-hardware modules; physical page/frame outputs remain generated evidence.

## Required Continuation

Work from the newest local run to the oldest, using the transcript summary and source verdicts to identify accepted, superseded, and failed work. For each folder and nested file:

1. Record its role, provenance, and whether it is AMCF-owned source, test, configuration, report, generated media, archive, dependency, or cache.
2. Read relevant source, tests, configurations, and verdicts; inspect generated outputs and archive members where needed to establish behavior. Do not equate a filename heuristic with reading a file.
3. Compare useful code and behavior against local `Main` and current public source. Check exact hashes where exact code is expected; run bounded parity tests where behavior equivalence is claimed.
4. Record an explicit evidence-backed decision: `PUBLIC_EXACT`, `PUBLIC_EQUIVALENT_TESTED`, `PORTED_AND_TESTED`, `SUPERSEDED_BY_LATER_ACCEPTED_WORK`, `HISTORICAL_FAILED`, `GENERATED_EVIDENCE_NOT_SOURCE`, `THIRD_PARTY_REFERENCE`, or `OPEN`.
5. Keep newer public software I/O and physical-player work intact. Do not promote historically rejected tracking, quality, or compression methods merely because they ran.

A folder is complete only when each contained file has a defensible disposition, its useful source/tests/outputs have been compared, and any claimed parity has a reproducible check. The current inventory begins with every row `UNREVIEWED`; no 100% claim follows from it.

Hardware validation claimed: false. Physical Level 5 claimed: false. Manufactured player claimed: false. Generated output committed: no.

The Level 5 Main integration evidence folder was reviewed next. Its accepted reusable surface is represented by public semantic proof, v-next, archive writer/reader, release acceptance, viewer, and V2 layers; `Main/amcf_vnext.py` and public `src/amcf_vnext.py` were byte-identical. Candidate release archives, vectors, HTML, JSON, CSV, and command outputs remain generated/evidence artifacts and were not copied. The detailed finding is in `docs/AMCF_TESTS_FILE_REVIEW_LEVEL5_PROMOTION_MAIN_INTEGRATION.md`.

The next semantic progression batch covered source acquisition, controlled lost/recovered proof, and HOOT dataset-annotated proof (1,192 files). The accepted proof scope is represented by the public semantic proof module and tests; the original OpenCV/SAM2/network runners, downloaded media, checkpoints, masks, overlays, and run outputs remain local-only evidence. The detailed finding is in `docs/AMCF_TESTS_FILE_REVIEW_SEMANTIC_LOST_RECOVERED_PROGRESSION.md`.

The next older semantic batch covered nine Tower Bridge, tool-survey, deep-tool, mask/track, cluster, and lost/recovered closure folders (2,736 files). Their source runners and verdicts were inspected; they remain historical, dependency-heavy, candidate, failed, or parked progression evidence. Public quality, tracking, sidecar, diagnostics, and accepted-proof modules preserve the reusable behavior without importing checkpoints/media or promoting rejected candidates. The detailed finding is in `docs/AMCF_TESTS_FILE_REVIEW_SEMANTIC_PROGRESSION_PRE_LEVEL5.md`.

The next older digital codec batch covered 07A, 07B/07C/07D, and 07E/07F/07G/07H/08A (452 files). 07A established original-truth compositor sanity, 07B selected full-rate control with no update reduction, and 07E selected residual-stream compression with decoded output and explicit accounting. Public residual gates, adaptive scheduling, v0 archive validation, and newer digital archive paths are present; the private waterfall residual codec and generated media are not copied. The detailed finding is in `docs/AMCF_TESTS_FILE_REVIEW_07A_07B_07E_RESIDUAL_AND_ADAPTIVE_PROGRESSION.md`.

The next older band covered `05B` through `05C6_06F` (5,178 files). It traced the component extraction/compositor prototype through fallback-supported decoders, parallax/tracking experiments, the accepted 05C4 full-rate visual control, rejected adaptive reductions, and the final 05C6 freeze. Public v0/v2 archive contracts, visual gates, accounting, scheduling primitives, and diagnostics represent the reusable behavior; historical waterfall-specific runners and generated media remain local evidence. The detailed finding is in `docs/AMCF_TESTS_FILE_REVIEW_05B_TO_06F_EARLY_V0_PROGRESSION.md`.

The next older band covered `03U` through `04F_05A` (1,106 files). It traced the 03U numerical support pass through the later 03V visual rejection, 03W safe component swaps, 03X fidelity audit, 03Y watchable/parallax baseline, 03Z v0 consolidation, and the 04A-04F/05A archive/viewer/builder/loader/component-schema hardening sequence. Public v0 toolchain, visual-gate, metric, diagnostic, and newer archive modules represent the reusable behavior; source-specific waterfall media, maps, generated outputs, and rejected candidates remain local evidence. The detailed finding is in `docs/AMCF_TESTS_FILE_REVIEW_03U_TO_04F_05A_V0_CONSOLIDATION.md`.

The exact file-level inventory for the `03T` through `03A` band covered 1,162 files, including 22 Python files, 148 MP4 files, 582 PNG/JPG files, 40 ZIP files, and the full report/config/script surface. The source inspection confirms early deep-segmentation failures, later motion/zone diagnostics, and visual/support experiments with selective promotion only. The detailed inventory is in `docs/AMCF_TESTS_FILE_REVIEW_03A_TO_03T_EXACT_INVENTORY.md`.
