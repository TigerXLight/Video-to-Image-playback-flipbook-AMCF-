# AMCF Tests Source-File Hash Reconciliation

## Scope

This is the source-level companion to the top-level folder reconciliation. It scans every local `Tests/**/*.py` file, excludes `__pycache__`, hashes the actual file contents, and compares those hashes and basenames with public `src/`, `demo/`, and `tests/` Python files.

This is not a claim that generated artifacts or every historical experiment must be copied. Hashes are used to separate exact reuse from files that need semantic disposition.

## Current measured result

| Measure | Count |
|---|---:|
| Local `Tests/**/*.py` files scanned | 1,154 |
| Public Python files searched (`src/`, `demo/`, `tests/`) | 202 |
| Unique local Python content hashes | 623 |
| Local files with an exact public SHA-256 match | 459 |
| Unique local hashes with an exact public match | 196 |
| Local files whose basename exists publicly but content differs | 112 |
| Local files with no public basename match | 583 |
| Unique local hashes with no exact public match | 427 |

The difference between file counts and unique hashes is expected. The local `Tests` tree contains copied source inside extracted archives, validation workspaces, imported experiment packages, and repeated regression fixtures. Those copies are not independent missing implementations.

## Exact matches

The exact matches cover substantial maintained behavior, including:

- public v0 archive/toolchain pieces;
- selected public V2 package modules;
- accepted public physical-player and software-I/O modules;
- regression helpers and public demos copied from accepted package stages;
- selected Main-facing sources.

Exact hash presence is evidence of code identity, but it does not by itself prove that the public package exposes the same command path or tests the same behavior. Public tests and demos remain the acceptance evidence.

## Non-exact and unmatched disposition

The non-exact/unmatched set is grouped by source role:

| Source role | Examples | Disposition |
|---|---|---|
| early SAM2/SAMURAI/track experiments | `03B` through early `03T` runners | historical/rejected or diagnostic evidence; selected motion-truth behavior was ported |
| visual-gate and v0 consolidation runners | `03V` through `04E` | consolidated into public v0 archive/viewer/validation modules; no runner bulk-copy |
| fallback/compositor/residual experiments | `05B` through `08E` | accepted contracts and diagnostics ported selectively; rejected/partial codecs remain local evidence |
| V1 archive/validator progression | `11A`/`11B` | public validator/archive contracts and acceptance harness cover the reusable behavior |
| semantic/mask/object research | `12B` through `12J` and named semantic campaigns | unresolved or review-gated research; public semantic sidecar/diagnostic layers preserve bounded behavior |
| playback/native payload progression | `13C` through `13P` | public playback-index, V2 archive, sidecar, reader/compositor, and bounded playback surfaces cover accepted contracts; experiment runners remain evidence |
| V2 package/viewer progression | `14A` through `14J` | public `src/amcf_v2/`, sidecar metadata, viewer, and tests cover the accepted bounded package |
| release/acceptance tooling | acceptance harness, runtime-validator, release-candidate groups | public release-candidate/review/closeout/tag tooling covers the required public checks |
| physical/reader planning | virtual reader, physical medium, transport/scan-gate groups | public software-only virtual-reader/physical-medium/player modules cover bounded no-hardware behavior |
| generated/imported copies | `built_archives_source`, `decoded_outputs`, `imported_*`, extracted packages | do not copy; source-of-truth is the selected maintained module or public consolidation |

## What remains intentionally unmatched

The unmatched hash set still contains real local code, but much of it is intentionally not public runtime:

- source-specific waterfall/Tower Bridge experiments;
- deep-tool wrappers requiring local models, media, or third-party trees;
- rejected fixed-tile, fallback, static-registration, and visually unstable approaches;
- benchmark and overnight orchestration scripts;
- local regression scripts tied to dated evidence directories;
- copied package sources whose accepted public successor is already present;
- physical planning and hardware-adapter placeholders;
- generated-output builders and report packagers.

These need no public port unless a later review identifies a specific accepted behavior with no public equivalent, test, or demo. The current reconciliation therefore avoids the unsafe inference that every unmatched hash is a missing feature.

## Next source-level action

The next review should work through the unmatched **maintained** candidates by group, beginning with any accepted native/V2 reader/compositor behavior whose public tests do not yet exercise the same contract. The review should compare symbols and fixtures, run the relevant local regression only when its inputs are available, and port narrowly only when a public test can prove the behavior.

## Claim boundary

- generated output committed: `no`;
- `unsafe_acceptance_count`: `0` in public safety/review paths;
- hardware validation claimed: `false`;
- physical Level 5 claimed: `false`;
- manufactured player claimed: `false`;
- real printer/scanner/player hardware claimed: `false`.
