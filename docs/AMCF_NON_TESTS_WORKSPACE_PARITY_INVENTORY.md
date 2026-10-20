# AMCF Non-Tests Workspace Parity Inventory

## Purpose

This inventory covers the project workspace outside the already-reviewed `Tests` tree. It separates maintained AMCF source and configuration from handoff material, generated evidence, third-party references, virtual environments, source media, and transfer archives before any further Main/public port work.

| Category | Files | Source decision |
|---|---:|---|
| `Main` | 19 files including 5 Python modules | Primary local app/reference surface; compare file-by-file with public source |
| Physical/research root runners | 7 Python runners plus command launchers | Source-owned research/simulation scripts; compare behavior, do not bulk-copy generated outputs |
| `AMCF_Interactive_Viewer_01` | 11 files | Historical Test 01 viewer bundle and generated comparison media |
| `AMCF_Codex_Handoff_02` | 25 files | Handoff/provenance plus legacy Test 01 snapshot and inspection media |
| `Handoffs` | 2 files | Duplicated handoff/provenance documents |
| `Diagnostics` | 7 files | Environment logs and source sample images |
| `Assets` | 10 files | Media assets, no AMCF source modules |
| `Original` | 21 files | Reference media/assets, no AMCF source modules |
| `Test media` | 1 file | Source media input, not source code |
| `Upstream_Source_Review_01` | 245 files | Third-party/source-review material with separate licenses and provenance |
| Virtual environments | 29,422 files across three environments | Local dependency installations; never public source |
| `Github repos` | 22,940 files | Third-party repositories/reference code; do not vendor wholesale |
| Root plans/transcripts/dossiers | large text/JSON set | Project history and controlling records, not runtime modules |
| Root ZIPs and archives | generated/transfer artifacts | Evidence or handoff packages; not source-of-truth |
| `__pycache__` | generated files | Exclude |

Generated media, caches, environment files, model weights, third-party trees, and private paths are not counted as missing public functionality merely because they are absent from GitHub.

## `Main` File Comparison

The maintained local `Main` surface contains:

- `amcf_test02.py`
- `amcf_tracking_test03a.py`
- `amcf_virtual_hardware.py`
- `amcf_vnext.py`
- `test_archive_decode.py`
- `amcf_config.example.json`
- `requirements.txt`
- README, provenance, canonical-concept, and physical-boundary documents
- three Windows command launchers

The exact SHA-256 comparison against the current public checkout is:

| Local `Main` file | Public file | Result |
|---|---|---|
| `amcf_test02.py` | `src/amcf_local_main_test02.py` | `PUBLIC_EXACT`; SHA-256 `DBFF47FED32450A0F7C7E470CF068B053A5E462DE422C56C123237D1E2EE7B83` |
| `amcf_vnext.py` | `src/amcf_vnext.py` | `PUBLIC_EXACT`; SHA-256 `2786735BD21F4288C317D8E80DCF9F6B806F7C11C10566255611E1ADEC6C3B93` |
| `test_archive_decode.py` | `src/amcf_local_main_archive_decode_check.py` | `PUBLIC_EXACT`; SHA-256 `F6FE29A3B21F9BC62C8B8B711D6933F4820666144560C09D3B1EEAAF81A6CBCA` |
| `amcf_virtual_hardware.py` | `src/amcf_virtual_hardware.py` | `PUBLIC_EXACT`; SHA-256 `4D79EA4FEBAEB8ED6065DD15F2437EEF1D19F1626266A7D50F78E0480C748919` |
| `amcf_tracking_test03a.py` | `src/amcf_local_main_tracking_test03a.py` | `PUBLIC_SAFE_ADAPTATION`; public root discovery removes the local workspace assumption |

The local `Main/requirements.txt` and public `requirements.txt` currently match. The requirements describe optional research/runtime dependencies such as NumPy, Pillow, OpenCV, scikit-image, SciPy, imageio, networkx, tifffile, and lazy-loader; public modules keep optional paths explicit rather than claiming every feature is available without those packages.

### Main versus the newer public branch

`Main` is not the whole current public source tree. The public checkout has 93 tracked Python source files, 53 demos, and 56 tests. The additional public surface includes:

- digital video/source-frame encoding and validation;
- component-event archives and viewers;
- v0 and v2 archive/container, codec, compositor, decode, index, and playback modules;
- quality, optical-flow, motion-truth, semantic-sidecar, and Test 02 diagnostics;
- software I/O package/manifest, print, reader, player-PC, and roundtrip modules;
- physical carrier, virtual hardware, physical-medium, and physical-player simulator modules;
- release/package/Pages/closeout/tag-prep and parity ledgers;
- `amcf_cli.py` as an existing developer-facing command layer.

These are newer public additions, not files missing from the older local `Main` snapshot. The parity task is to retain them while proving that the local `Main` behavior and the accepted `Tests` behavior are represented, not to reduce the public tree to the old `Main` file count.

## Root Physical/Research Runners

The maintained root runners are:

- `run_amcf_canonical_concept_alignment.py`
- `run_amcf_non_ideal_physical_carrier_simulation.py`
- `run_amcf_physical_carrier_research_matrix_and_simulation_plan.py`
- `run_amcf_physical_medium_flipbook_simulation.py`
- `run_amcf_primary_adapters_and_vertical_stack_physical_design.py`
- `run_amcf_single_app_main_entrypoint_config_github_layout.py`
- `run_amcf_vertical_stack_physical_medium_simulation.py`

Their code uses standard-library orchestration, and some use OpenCV/NumPy/Pillow/FFmpeg for generated physical-medium or non-ideal-capture evidence. They produce reports, page/capture media, transport matrices, and design implications under dated local run folders. The public repository already contains selected software-only physical-medium and physical-player modules/tests/demos, but these root runners are not byte-identical public replacements and their generated outputs are not public source.

Disposition:

- canonical concept and boundary content: `PUBLIC_EQUIVALENT_DOCS`;
- deterministic no-hardware physical-medium behavior: `PUBLIC_EQUIVALENT_TESTED` through the public simulation module;
- research matrix/planning content: `DOC_ONLY` / physical-future planning;
- non-ideal capture runner and generated images/videos: `LOCAL_RESEARCH_EVIDENCE`;
- single-app layout runner: `APP_LAYOUT_EVIDENCE`, not proof of a finished app;
- physical hardware, scanner, printer, camera, motor, or sensor behavior: not implemented or claimed.

The runner-level comparison is:

| Local runner behavior | Public correspondence | Parity disposition |
|---|---|---|
| canonical concept alignment and claim wording | physical-player/public concept and boundary docs | `PUBLIC_EQUIVALENT_DOCS` |
| non-ideal physical-carrier capture simulation | physical-medium simulation modules and demos | `PUBLIC_EQUIVALENT_TESTED`, with optional CV dependencies kept explicit |
| physical-carrier research matrices and design plans | physical-player mechanism/profile and physical-medium docs | `DOC_ONLY` / future design material |
| ideal vertical-stack page/capture/recovery simulation | physical-medium simulation source/tests | `PUBLIC_EQUIVALENT_TESTED` for the bounded no-hardware path |
| primary adapters and Main-facing physical design | public physical-player modules plus release docs | `PUBLIC_EQUIVALENT_PARTIAL`; the local orchestration remains workspace-specific |
| single-app Main/config/toolchain layout checks | `src/amcf_vnext.py` and `src/amcf_cli.py` | `APP_LAYOUT_EVIDENCE`; not a finished end-user app |
| generated pages, contact sheets, MP4s, and metric CSVs | no direct source requirement | `GENERATED_DO_NOT_COPY` |

The physical-medium runners reference local source media, dated Test 02 outputs, local interpreter paths, and generated output roots. That coupling is why they are evidence runners rather than safe public application entrypoints. The public modules preserve the accepted software/control behavior without importing those private paths.

## Historical Viewer and Handoff Bundles

`AMCF_Interactive_Viewer_01` contains a standard-library local HTTP launcher, viewer metadata builder, self-test, HTML/JavaScript controls, a synchronized comparison MP4, and hashes. Its own documentation describes Test 01 as a failed quality-equivalent compression baseline and says the viewer does not decode AMCF live. The public Test 02 diagnostic viewer and later public archive/component viewers are the maintained successors. The bundle is historical/generated evidence, not a missing public runtime.

`AMCF_Codex_Handoff_02` contains setup/handoff/provenance scripts, a copy of the failed Legacy Test 01 prototype, and screen/inspection media. `Handoffs` duplicates the handoff/provenance documents. These are source-history records, not additional accepted AMCF modules.

## Diagnostics, Assets, and Media

`Diagnostics` contains environment audits and a small set of source samples. `Assets`, `Original`, and `Test media` contain media inputs or visual references. They are not portable source logic and should not be committed to the public package without an explicit asset/license decision. Public diagnostics use deterministic synthetic fixtures or documented local inputs instead.

## Upstream and Environment Material

`Upstream_Source_Review_01` contains selected upstream repositories, source snapshots, hierarchy/manifests, and the current AMCF context. The provenance record explicitly distinguishes ideas, API dependencies, adapted code, and copied code, and flags restricted or model/data-specific terms. These repositories are reference material and must not be bulk-copied into the public repo.

The local `Github repos` tree was also enumerated by repository. Its current file counts and parity dispositions are:

| Reference tree | Files | Disposition |
|---|---:|---|
| `AMCF_flipbook_reference_collection` | 738 | Third-party/reference collection; inspect licenses and provenance before any narrow reuse |
| `AOT` | 34 | Third-party tracker reference; not AMCF-owned runtime |
| `co-tracker` | 120 | Third-party tracking reference; not AMCF-owned runtime |
| `Cutie` | 212 | Third-party video object tracking reference; not AMCF-owned runtime |
| `DEVA` | 149 | Third-party video segmentation/reference implementation |
| `EXTRA_03B_SELECTED_DOCS` | 14 | Selected reference documentation |
| `FFmpeg` | 10,847 | External media tool/source reference; use as an explicit optional runtime dependency |
| `opencv` | 7,423 | External computer-vision dependency/source reference |
| `PySceneDetect` | 232 | External scene-detection reference |
| `RAFT` | 64 | Third-party optical-flow reference |
| `sam2` | 598 | Third-party segmentation/reference implementation |
| `SAMURAI` | 535 | Third-party tracking/reference implementation |
| `scikit-image` | 1,491 | External image-analysis dependency/source reference |
| `Segment-and-Track-Anything` | 212 | Third-party segmentation/tracking reference |
| `TAPNet` | 127 | Third-party tracking reference |
| `Track-Anything` | 98 | Third-party tracking reference |
| `XMem` | 158 | Third-party video-memory reference |
| `XMem2` | 405 | Third-party video-memory reference |

These counts are inventory evidence, not a license determination and not a claim that the public package embeds these trees. The public repository should keep dependency declarations, provenance, and narrowly adapted AMCF logic only. It should not vendor the full reference trees.

The selected `Upstream_Source_Review_01` material contains the following source-review groups: `co-tracker`, `Cutie`, `FFmpeg`, `opencv`, `PySceneDetect`, `RAFT`, `sam2`, `scikit-image`, and `XMem`, plus AMCF context and inventory manifests. Its selected-file lists are provenance evidence, not public runtime requirements.

### Root-level non-runtime records

The workspace root also contains controlling dossiers, plans, handoffs, transcript summaries, hierarchy listings, ZIP archives, and a concept image. These are classified as follows:

- dossiers, plans, and roadmaps: project-control records; normalize decisions into public docs when needed;
- transcript/history files and reading ledgers: audit context; not executable behavior;
- project hierarchy listings: inventory evidence; not source modules;
- handoff Markdown/TXT/ZIP files: provenance and transfer records;
- Test 02 deliverable ZIPs and other archives: generated evidence/transfer artifacts;
- concept and physical-design media: design reference, not a runtime dependency;
- root `.cmd` launchers and Python runners: source-owned research/simulation scripts already inventoried in this document.

No root archive, transcript, plan, hierarchy file, or concept asset is being treated as an unaccounted executable parity gap. A future port would require a specific accepted behavior, source file, license/provenance review, and a public test.

The three `.venv*` directories are local dependency environments. `Github repos` is a large third-party/reference tree. Neither is an AMCF source directory. Their absence from the public repo is correct; only a curated dependency/provenance document belongs in public source.

## Root Plans, Transcripts, and Archives

The root dossiers, plans, handoffs, transcript summaries, full transcript, hierarchy lists, and ZIPs explain project history and accepted/rejected decisions. They are useful for this parity review, but they are not executable application behavior. Public docs should carry normalized decisions and claim boundaries rather than private absolute paths or every chat artifact.

## Universal Comparison Result So Far

- Local `Main` core source: mapped; four files are exact and one is a deliberate public-safe adaptation.
- Newer public software-I/O and physical-player functionality: present in the public tree and intentionally absent from the older local `Main` snapshot.
- Root physical/research scripts: inventoried; selected no-hardware behavior is represented publicly, while generated and hardware-planning material remains local evidence.
- Handoff/viewer/diagnostic/media/reference folders: dispositioned as historical, generated, provenance, or third-party material; no unaccounted accepted runtime module has been established from them in this pass.
- CLI/app: a developer-facing `src/amcf_cli.py` exists publicly, but a polished user workflow, dependency installation contract, and packaged executable are still separate readiness questions.

This is a non-`Tests` inventory checkpoint, not a final 100% workspace parity claim. Remaining work is to reconcile any outstanding `Tests` ledger rows, inspect any non-generated AMCF-owned files discovered in the full workspace manifests, run the public parity/test surface, and only then decide whether a CLI/app closeout is justified.

## Claim Boundary

- generated output committed: `no`;
- unsafe acceptance count: `0` in the public review/report layer;
- hardware validation claimed: `false`;
- physical Level 5 claimed: `false`;
- manufactured player claimed: `false`;
- real printer/scanner/reader/player hardware claimed: `false`.
