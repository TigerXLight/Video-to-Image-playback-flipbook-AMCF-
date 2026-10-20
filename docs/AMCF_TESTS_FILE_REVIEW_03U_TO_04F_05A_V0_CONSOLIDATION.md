# AMCF Tests File Review: 03U Through 04F/05A

## Scope

This review covers the next older code and evidence band:

- `Test 03U`, `03V`, `03W`, `03X`, `03Y`, `03Z`
- `Test 04A`, `04B`, `04C`, `04D`, `04E`, `04F_05A`

The band contains 1,106 files. The primary runner in each folder was inspected along with the status reports, selected/rejected decisions, archive/viewer code, and the public modules that represent the retained behavior.

## Chronological Progression

| Folder | Actual code path | Result and later decision | Public parity decision |
|---|---|---|---|
| `03U` | OpenCV support-accounting continuation loop, registered/static regions, current-frame fallback accounting, repeated candidate renders | Reported numerical `STRONG PASS` and 0% measured fallback in its own artifact, but the visual result later showed trunk/static texture swimming, drift, smear, popping, and temporal instability | Treat as a negative control; metrics alone must not win |
| `03V` | Visual artifact gate comparing 03P/03Q/03T/03U, crop audits, smoothness and static-region review | `PASS` as a visual-gate package; selected 03P as the best watchable baseline and explicitly rejected 03U | Retain visual-first gate and artifact-warning policy |
| `03W` | Component-swap ablation from locked 03V baseline, cumulative safe active-motion swaps, rejection of static/trunk swaps | `PASS`; active-motion swaps were retained, static/trunk registered replacement was rejected | Retain safe-swap/rollback logic, not the source-specific component map |
| `03X` | Playback fidelity audit, frame/fps/timestamp checks, crop audits, waterfall temporal metrics, candidate-only high-quality export | Partial/diagnostic fidelity audit; useful evidence that apparent loss can be export/presentation softness rather than frame-rate loss | Retain generic quality/timing metrics; do not import source-specific media paths |
| `03Y` | Parallax and waterfall fidelity metrics, optical-flow measurements, sharpness variants, static-registration retry, high-quality candidate export | `PASS` for the best watchable candidate; static registration remained quarantined and texture attachment still required human review | Retain visual gate, parallax warning, and active-motion preference |
| `03Z` | Consolidation runner, package manifest/rules, rejected-strategy list, component rules, viewer, evidence and future-work reports | Consolidated the accepted visual baseline into an AMCF v0 review package; not final production AMCF | Public v0/archive/report layers cover the safe package contract |
| `04A` | v0 viewer/archive prototype creation and package layout | Viewer/archive prototype established; archive structure and metadata were the target, not final codec behavior | Public v0 archive package contract |
| `04B` | Hardened viewer/archive validation, relative-link checks, forbidden-content checks, visual gate rules | Hardened the review package and fail-closed packaging rules | Public v0 loader/builder validation |
| `04C` | Portable archive roundtrip and extraction checks | Demonstrated archive build/extract portability and path-safe roundtrip behavior | Public v0 roundtrip and extraction tests |
| `04D` | Archive loader and manifest/media/viewer validation | Added a loader-facing validation surface around the v0 package | Public v0 loader and manifest checks |
| `04E` | Builder/loader toolchain, safe relative paths, viewer-link parser, media probing, checksums, archive reports, regression tests | Hardened the reusable v0 package toolchain; explicitly described the archive as a prototype, not a final codec | Public `src/amcf_v0/` builder/loader/toolchain and tests |
| `04F_05A` | Copies/hardens v0 builder/loader, adds schema/error codes, component manifest, update schedules, diagnostic seed ROIs/streams, viewer and package checks | Path A hardens the v0 toolchain; Path B creates a diagnostic component-stream seed, not final segmentation/tracking/compression | Public v0 contracts plus newer component/event and diagnostics modules; source-specific seed media stays local |

## Code Findings

The code inspected in this band establishes several important rules:

- visual quality overrides support-accounting percentages;
- source-fps playback and every-frame updates remain allowed where motion requires them;
- static/background registration is quarantined until texture attachment and parallax pass;
- candidate-only high-quality review output is distinct from a compressed side-by-side review video;
- archive builders reject unsafe relative paths, traversal, prior ZIPs, environment folders, model/checkpoint material, raw frame trees, and external viewer links;
- archive loaders validate manifests, viewer links, media, required docs, and extraction behavior;
- component manifests carry IDs, labels, source basis, update schedules, mask/stream/compositor policy, limitations, and visual-gate notes;
- 05A’s seed masks/ROIs and component streams are diagnostic scaffolding, not a final semantic or compression solution.

The source runners use OpenCV/NumPy/Pillow and FFmpeg/FFprobe for video reading, frame comparison, optical-flow and blur metrics, H.264 review exports, contact sheets, archive checks, and generated evidence. Those dependencies are part of the historical local research environment, not proof that every public path requires them.

## What Was Integrated into Main and Public

The progression explains why the public repository contains selected behavior rather than a literal copy of every runner:

| Behavior | Main/public status |
|---|---|
| v0 archive manifest/layout, safe packaging, extraction, loader validation, viewer-link checks | Represented by public `src/amcf_v0/` and tests |
| Visual-first acceptance and artifact warnings | Represented by public residual/visual acceptance helpers and review docs |
| Generic frame quality and timing metrics | Represented by public quality-metric and video/diagnostic modules |
| Motion/overlay/zone diagnostic ideas | Represented by public diagnostic modules where reusable and source-independent |
| Exact waterfall coordinates, source media, generated crops/videos, and manual map files | Not ported; local evidence and generated output only |
| 03U static-registration candidate | Not ported as accepted behavior; explicitly rejected by later visual review |
| 05A diagnostic seed component codec and generated streams | Not ported as the final codec; later public component/event paths are the cleaner contract |

## Progression Answers

1. These folders contain a connected progression, not isolated improvements. Later tests compare against and sometimes invalidate earlier candidates.
2. The archive/viewer/toolchain progression was integrated into reusable Main/public package surfaces. The source-specific waterfall component candidates were not all integrated into Main, and should not be treated as missing merely because their generated artifacts are absent.
3. A correct GitHub completeness package must separate accepted contracts from historical evidence and rejected candidates.
4. Newer public component/event, v2 archive, diagnostics, and physical/software I/O modules remain authoritative where they supersede this early v0 research.
5. The local test folders remain the evidence source for this progression; they are not themselves the public runtime.
6. Tracking, masks, overlays, zone/parallax checks, and visual gates are represented only where their behavior is reusable and claim-safe. Source-specific masks and media remain excluded.
7. The digital public closeout should use the later accepted archive/reader/compositor paths, while this band supplies the historical origin and safety rules.

## Port Decision

- `PORTED_AND_TESTED`: safe archive builder/loader/manifest/extraction/relative-link validation behavior.
- `PORTED_AND_TESTED`: visual-first gate and explicit rejection of metric-only acceptance.
- `PORTED_AS_GENERIC_DIAGNOSTICS`: quality, timing, motion, and artifact-report concepts.
- `SUPERSEDED_BY_LATER_PUBLIC_PATH`: exact 05A seed stream and early v0 component viewer as a runtime codec.
- `LOCAL_ONLY`: source-specific waterfall ROIs, manual component maps, media, generated videos, and review ZIPs.
- `DO_NOT_PORT`: 03U static/background registered replacement and any candidate rejected by later visual gates.

No new runtime code is required from this band in the current review pass. The public v0 and newer archive paths already carry the reusable package behavior without importing local media or rejected candidates.

## Claim Boundary

- `unsafe_acceptance_count`: `0` in the public safety/report layer.
- Hardware validation claimed: `false`.
- Physical Level 5 claimed: `false`.
- Manufactured physical player claimed: `false`.
- Real printer, scanner, reader, camera, motors, sensors, cartridges, or player hardware claimed: `false`.
- The v0 package and visual gates are software/research behavior only.

## Status

This band is reviewed and recorded. The next chronological work continues through the remaining older `03A–03T` lineage and then the non-`Tests` workspace inventory. Existing grouped docs cover the broad 03A–03T progression, but the universal parity ledger remains open until every relevant file group and Main/public mapping is accounted for.
