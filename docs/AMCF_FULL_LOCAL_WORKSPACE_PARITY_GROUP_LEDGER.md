# AMCF Full Local Workspace Parity Group Ledger

Run context: `AMCF_FULL_WORKSPACE_PARITY_LEDGER_V1`

Latest refinement commit before this group work: `50e66d8`

This ledger tracks the `INSPECT_PRIORITY` groups from the full local workspace inventory. It is intentionally group-oriented: the goal is to work through AMCF-owned candidate groups one by one and mark whether they are already public, newly ported, superseded, third-party reference material, generated output, or still pending review.

This is not a claim of byte-for-byte output identity. It is a practical parity ledger for code, behavior, tests, and useful package surface while preserving the newer public software I/O and physical-player work.

Detailed progression mapping now lives in `docs/AMCF_LOCAL_TESTS_PROGRESSION_INTEGRATION_LEDGER.md`. The first newest-folder diagnostic repair is recorded in `docs/AMCF_TEST02_DIAGNOSTIC_VIEWER_PARITY.md`. The exact top-level folder reconciliation is recorded in `docs/AMCF_TESTS_TOP_LEVEL_FOLDER_RECONCILIATION.md`, source-hash measurements in `docs/AMCF_TESTS_SOURCE_FILE_HASH_RECONCILIATION.md`, and accepted V2 file parity in `docs/AMCF_V2_ACCEPTED_GROUP_FILE_PARITY.md`.

The seven root physical/research runners were inspected at source level and
their dispositions are recorded in `docs/AMCF_ROOT_RUNNER_SOURCE_PARITY_REVIEW.md`.
The public package was then promoted into the local `Main` folder as a tracked
source/docs/tests/demo mirror; the copy evidence and test-context boundary are
recorded in `docs/AMCF_MAIN_PUBLIC_MIRROR_SYNC.md`.
The exact source mirror, bounded CLI output comparison, runtime sample, and
isolated package-build result are recorded in
`docs/AMCF_MAIN_PUBLIC_PARITY_BENCHMARK_AND_PACKAGE_CHECK.md`.
The current Main/Tests/public proof, including the successful wheel and
installed-console validation, is recorded in
`docs/AMCF_CURRENT_MAIN_TESTS_PUBLIC_PARITY_PROOF.md`.
The non-Python `Tests` artifact inventory is recorded in
`docs/AMCF_TESTS_NON_PYTHON_ARTIFACT_PARITY_INVENTORY.md`.

The newest bounded V2/native closeout group is recorded in
`docs/AMCF_TESTS_NEWEST_TO_OLDEST_PART16_V2_NATIVE_AND_CLOSEOUT_REVIEW.md`.
It confirms the accepted 14A-14J bounded behavior and 13M closeout mapping
without promoting the unaccepted 14E/E2/E3 codec investigations or generated
sample evidence.

The next digital diagnostics/native-chain slice is recorded in
`docs/AMCF_TESTS_NEWEST_TO_OLDEST_PART17_DIGITAL_DIAGNOSTICS_AND_NATIVE_CHAIN_REVIEW.md`.
It verifies the latest Test 02 diagnostic contract and maps the accepted
bounded 13F-13P/13M behavior to the existing public V2, archive, quality,
tracking, and viewer layers without duplicating historical experiment trees.

The isolated diagnostic parity slice is recorded in
`Tests/Test AMCF_DIAGNOSTIC_PARITY_REVIEW_V1/20261020_120000/output/DIAGNOSTIC_PARITY_REVIEW_V1.md`.
It re-ran the accepted 08E `Stay Here for 13 Seconds` heat contract, verified
the corrected 12E narrow proxy event, and checked the existing 03M artifacts.
The reusable profile implementation is `src/amcf_diagnostic_profiles.py` and
the standalone entry point is `demo/run_amcf_diagnostic_profiles.py`.

## Current Group Status

| Group | Status | Public coverage | Notes |
| --- | --- | --- | --- |
| `Main` | PORTED / COVERED | `src/amcf_video_pipeline.py`, `src/amcf_component_event_archive.py`, `src/amcf_quality_metrics.py`, `src/amcf_component_event_viewer.py`, `src/amcf_optical_flow_tracking.py`, `src/amcf_deliverable_package.py`, `src/amcf_cli.py` | Local `Main` behavior has been ported as public-safe modules with optional dependency handling. Exact private-media output identity is not claimed. |
| `Tests/Test 14F_V2_INTEGRATED_BOUNDED_PROTOTYPE_PACKAGE` | PORTED / COVERED | `src/amcf_v2/`, `demo/run_amcf_v2_public_package_demo.py`, `tests/test_amcf_v2_public_package.py` | V2 bounded package concepts are represented in the public v2 package surface. |
| `Tests/Test 04F_05A` | PORTED / COVERED | `src/amcf_v0/`, `demo/run_amcf_v0_public_archive_toolchain_demo.py`, `tests/test_amcf_v0_public_archive_toolchain.py` | V0 archive toolchain behavior has a public module and tests. |
| `Tests/Test AMCF_ARCHIVE_WRITER_READER_INTEGRATION` | PORTED IN THIS PHASE | `src/amcf_archive_writer_reader.py`, `demo/run_amcf_archive_writer_reader_demo.py`, `tests/test_amcf_archive_writer_reader.py`, `docs/AMCF_ARCHIVE_WRITER_READER_PARITY_PORT.md` | Ported writer/reader fixture archives, sidecars, checksums, fail-closed validation, and claim-boundary report behavior without local run paths. |
| `Tests/Test 14A` through `Test 14J` plus `Test 13M_FINAL_BENCHMARK_VALIDATION_SPEC` | PORTED / COVERED / EVIDENCE-DISPOSITIONED | `src/amcf_v2/`, `src/amcf_v2_14h_archive.py`, `src/amcf_v2_sidecar_metadata.py`, public archive/quality/playback/report layers | Part 16 confirms the accepted bounded V2/native behavior is represented and tested; generated evidence, imported duplicates, and unaccepted codec investigations remain excluded. |
| `Tests/Test 02/20261013_071127` plus `Tests/Test 13F-13P` and `13M` closeout | REVIEWED / COVERED | `src/amcf_test02_diagnostic_viewer.py`, `src/amcf_v2/`, `src/amcf_v2_14h_archive.py`, public tracking/quality/archive/viewer tests | Part 17 confirms diagnostic taxonomy/viewer behavior and accepted bounded native-chain behavior are represented; failed final-fidelity evidence and historical generated outputs remain excluded. |
| `Test 03M`, `Test 08E`, `Test 10A_10B`, and reviewed `Test 12E` diagnostics | PORTED / TESTED | `src/amcf_diagnostic_profiles.py`, `demo/run_amcf_diagnostic_profiles.py`, unified Main diagnostics, `tests/test_amcf_diagnostic_profiles.py` | The seven 03M zones, exact 08E Farneback/TURBO heat contract, and conservative 12E proxy/narrow-event semantics are reusable. Historical generated media stays local evidence; semantic masks/object AMCF remain unclaimed. |
| `<historical-public-package-snapshots>` | ALREADY PUBLIC | Current repo | Historical public-package snapshots should not be copied back into themselves. |
| `Github repos/` | THIRD_PARTY_REFERENCE | Not copied | Third-party repositories and model/tool references require separate license/provenance decisions. |
| Generated output groups under `Tests/` | GENERATED_DO_NOT_COPY | Not copied | Generated archives, videos, reports, caches, and run outputs should stay out of Git unless explicitly curated. |

## Universal Comparison Checkpoint

The current local-workspace comparison has now covered:

- all `185` top-level folders under the local `Tests` root by exact folder-name reconciliation;
- all `1,154` local `Tests/**/*.py` files by hash/basename comparison;
- the maintained local `Main` files by exact SHA-256 or documented public-safe adaptation;
- root physical/research runners, handoff/viewer bundles, diagnostics/assets/media, archives, plans, transcripts, virtual environments, and third-party/reference trees;
- accepted V2 14F package files at same-path level (`39/39` present, `38/39` byte-identical);
- the 13M closeout evidence and software virtual-reader emulator source concepts.
- all seven root physical/research runners, including their private-path,
  dependency, subprocess, and generated-output coupling.
- the public-to-`Main` mirror: `379` tracked public files copied, with the
  public CLI smoke workflow passing from the synchronized Main folder.
- the remaining non-Python `Tests` surface classified by actual extension,
  size, and generated/source disposition.

Measured source-hash results are documented rather than hidden: `459` local Python files have exact public hashes, while unmatched hashes are predominantly historical/rejected experiments, copied/imported package duplicates, local regression harnesses, generated builders, or unresolved research candidates. The comparison therefore does not claim that all unmatched local files are missing public features.

Public acceptance checkpoint: the local Main suite passed `509` tests after the diagnostic-profile port; the unified Main digital acceptance runner passed with 7 zones and 288 processed diagnostic frames; the 08E Main profile output matched the historical heat artifact byte-for-byte; generated output remains under `Main/output/`; and `unsafe_acceptance_count` remained `0` in the reviewed paths.

## Next Phase Boundary

The parity audit is ready to move from inventory into a deliberate implementation decision. The public repository already has a developer-facing `src/amcf_cli.py`, but the next user-facing phase should define and test the unified CLI contract before packaging an EXE or GUI. Any remaining unmatched research code must not be bulk-copied; it needs a specific accepted behavior, public test, and dependency/provenance decision.

Each group should be handled narrowly:

- inspect source files first
- do not copy generated output
- do not copy local absolute paths
- do not bulk-copy third-party repos
- port useful AMCF-owned behavior into clean public modules
- add focused tests and demos
- keep generated output under `output/`
- keep `unsafe_acceptance_count` at `0`
- keep hardware validation, physical Level 5, and manufactured-player claims false

## Claim Boundary

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- real motors/sensors/cartridges validated: false
- generated output committed: false
