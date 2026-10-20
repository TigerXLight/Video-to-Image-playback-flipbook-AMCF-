# AMCF Tests Top-Level Folder Reconciliation

## Purpose

The public review docs already covered many folders through ranges such as `03A-03T`, `03U-05A`, `05B-06F`, and the semantic/V2 progression groups. A direct-name scan found 52 top-level `Tests` folders that were not individually named in those docs. This reconciliation removes that bookkeeping gap.

The scan is a coverage reconciliation, not a claim that every historical artifact is public runtime code. Python sources were enumerated and symbol-inspected; status/decision records were read for each group; accepted behavior was compared with the current public modules and tests. Generated media, imported experiment copies, caches, and local setup artifacts remain excluded.

## Direct-name reconciliation

| Local folder | Evidence classification | Public disposition | Further work |
|---|---|---|---|
| `Test 03V` | visual rejection/selection gate | public visual-gate rules and v0 docs | no runtime port |
| `Test 03W` | component-swap safety/ablation | public visual acceptance and claim-safe diagnostics | no runtime port |
| `Test 03X` | playback fidelity audit, partial | public metrics/validation concepts | source-specific evidence only |
| `Test 03Y` | accepted watchable/parallax reference with rejected static retry | public visual/metric contracts | no media port |
| `Test 03Z` | v0 consolidation package | public `src/amcf_v0/` and archive docs | covered |
| `Test 04B` | archive/viewer hardening | public v0 archive/viewer validation | covered |
| `Test 04C` | portable archive roundtrip | public v0 roundtrip/toolchain | covered |
| `Test 04D` | loader/manifest/media validation | public v0 loader/validator | covered |
| `Test 04E` | builder/loader/toolchain | public v0 builder/loader and tests | covered |
| `Test AMCF_ACCEPTANCE_HARNESS_AND_CI_STYLE_REGRESSION` | acceptance harness; invalid vectors rejected as designed | public release-candidate acceptance and fail-closed tests | covered by consolidation |
| `Test AMCF_AUTONOMOUS_POST_ACCEPTANCE_ROADMAP_EXECUTOR` | roadmap/report orchestration | public release and parity docs | evidence only |
| `Test AMCF_CAL12C_0117_MASK_DRAFT_UNBLOCK` | manual semantic-mask draft | semantic branch evidence; not solved runtime | do not port |
| `Test AMCF_CAL12C_0117_POST_APPROVAL_SEMANTIC_MICRO_TEST` | semantic micro-test | semantic-sidecar/diagnostic concepts | no product claim |
| `Test AMCF_CAL12C_0117_VISUAL_MASK_REVIEW_AUTONOMOUS` | mask review assistant | semantic review evidence | no runtime port |
| `Test AMCF_CANONICAL_TEST_VECTOR_AND_VALIDATOR_INTEGRATION` | canonical vectors/validator | public release-candidate acceptance and validator modules | covered by consolidation |
| `Test AMCF_CONTINUOUS_HARD_SOLVER_SEMANTIC_PLAYBACK_GENERALISATION` | unresolved semantic solver attempt | historical semantic evidence | do not port |
| `Test AMCF_CONTINUOUS_SEMANTIC_OBJECT_SOLVER_DEEP` | unresolved semantic/object attempt | historical evidence; safe flags remain false | do not port |
| `Test AMCF_DEEP_SEMANTIC_OBJECT_LEVEL5_RETRY_WITH_SAM2_COTRACKER` | deep-tool retry/probe | third-party-assisted research evidence | do not port wholesale |
| `Test AMCF_FULL_AUTONOMOUS_FUTURE_WORK_RUN` | future-work orchestration | roadmap/docs only | no runtime port |
| `Test AMCF_FULL_PROXY_DEEP_MASK_TRACK_BINDING_AND_LEVEL5_CLOSURE` | proxy mask/track binding | semantic diagnostics, not accepted full solution | do not port |
| `Test AMCF_FULL_ROADMAP_AUTONOMOUS_CAMPAIGN` | roadmap campaign report | project history | no runtime port |
| public-package preparation folder | public-package preparation | current public package/docs/release checks | covered |
| `Test AMCF_HARD_PROBLEM_SOLVER_AUTONOMOUS` | hard-problem research attempt | historical evidence | do not port |
| `Test AMCF_HIGH_PRECISION_MASK_CLUSTER_AND_OBJECT_IDENTITY_PROMOTION` | mask/identity promotion experiment | semantic evidence and safe diagnostics only | do not port |
| `Test AMCF_LEVEL5_GAP_CLOSURE_TARGETED_SOLVER` | Level 5 gap-closure attempt | public semantic Level 5 proof is the bounded accepted surface | no further runtime port |
| `Test AMCF_LOCAL_DEEP_SEMANTIC_TOOLCHAIN_INTEGRATION` | local deep-tool integration | upstream/provenance and semantic docs | no bulk port |
| `Test AMCF_LOST_RECOVERED_AND_FULL_SEMANTIC_CLOSURE` | lost/recovered semantic evidence | public semantic proof/sidecar diagnostics | preserve conservative limits |
| `Test AMCF_LOWRES_FULL_SOURCE_PROXY_SEMANTIC_RECONSTRUCTION` | low-resolution proxy reconstruction | source-specific experiment | do not port |
| `Test AMCF_MACHINE_REVIEWED_SEMANTIC_OBJECT_ADVANCEMENT` | machine-reviewed semantic advancement | semantic evidence | no runtime port |
| `Test AMCF_MACHINE_VALIDATED_SEMANTIC_OBJECT_SOLVER` | machine-validated solver attempt | semantic evidence with no full-solution claim | do not port |
| `Test AMCF_MASTER_AUTONOMOUS_REMAINING_WORK_CLOSEOUT` | closeout/backlog orchestration | public closeout/tag/release docs | covered as docs |
| `Test AMCF_MULTI_ANCHOR_SOURCE_SEMANTIC_OBJECT_EXPANSION` | multi-anchor semantic experiment | historical semantic evidence | do not port |
| `Test AMCF_MULTI_TRACK_SEMANTIC_ADVANCEMENT_CONTINUOUS` | multi-track semantic experiment | diagnostics/progression evidence | do not port |
| `Test AMCF_OVERNIGHT_SEMANTIC_OBJECT_ADVANCEMENT_CAMPAIGN` | overnight semantic campaign | historical evidence | do not port |
| `Test AMCF_POST_LEVEL5_ROADMAP_CONTINUATION` | post-Level-5 planning | public roadmap/release docs | docs only |
| `Test AMCF_RELEASE_CANDIDATE_LIGHTWEIGHT_PACKAGE` | release-candidate package evidence | public release-candidate acceptance and package checks | covered |
| `Test AMCF_RELEASE_CANDIDATE_REVIEW_AND_SIGNOFF` | release signoff evidence | public release review/closeout docs | covered |
| `Test AMCF_ROADMAP_AUTONOMOUS_EXECUTOR_BATCH_01` | roadmap executor batch | project-control evidence | no runtime port |
| `Test AMCF_RUNTIME_VALIDATOR_SPEC_V_NEXT` | validator/runtime specification | public vnext validator and claim-boundary tests | covered by consolidation |
| `Test AMCF_SEMANTIC_CONTINUITY_EXPANSION_AUTONOMOUS` | semantic continuity attempt | historical evidence | do not port |
| `Test AMCF_SEMANTIC_CONTINUITY_USER_APPROVED_UPDATE` | user-reviewed semantic update | historical evidence | do not port |
| `Test AMCF_SEMANTIC_IDENTITY_VALIDATION_RECONSTRUCTION_UPGRADE` | semantic identity diagnostics | public semantic sidecar/metrics concepts | no product claim |
| `Test AMCF_SEMANTIC_MASK_AND_PLAYER_HARDENING_AUTONOMOUS` | semantic/player hardening attempt | public player/semantic safety layers | preserve bounded scope |
| `Test AMCF_SEMANTIC_MICRO_AMCF_INTEGRATION` | semantic micro integration | public semantic sidecar overlay | covered |
| `Test AMCF_SOURCE_ANCHORED_SEMANTIC_REDISCOVERY` | source-anchored semantic research | historical evidence | do not port |
| `Test AMCF_SOURCE_EVIDENCE_REPAIR_SEMANTIC_SOLVER` | source-evidence repair attempt | historical evidence | do not port |
| `Test AMCF_TARGETED_IDENTITY_EXPANSION_FULL_RECONSTRUCTION_PUSH` | targeted identity expansion | historical semantic evidence | do not port |
| `Test AMCF_TOOL_SEARCH_SEGMENTATION_TRACKING_SURVEY` | third-party tool survey | provenance/reference only | no runtime port |
| `Test AMCF_TOWER_BRIDGE_PROXY_AMCF_RECONSTRUCTION_AND_BENCHMARK` | source-specific proxy benchmark | diagnostic evidence only | no media port |
| `Test AMCF_TOWER_BRIDGE_PROXY_GENERALISATION_AND_SOURCE_ROI_PREP` | source-specific proxy/ROI preparation | diagnostic evidence only | no media port |
| `Test AMCF_UPSTREAM_REPO_INTEGRATION_AND_DEEP_SEMANTIC_BRIDGE` | upstream integration research | provenance/reference only | no bulk port |
| `Test AMCF_VIEWER_DEMO_POLISH_AND_RUNTIME_INTEGRATION` | viewer/demo polish | public viewer/demo/release surfaces | covered |

## What this proves

The 52 names were not missing because they were forgotten source modules. They divide into:

1. folders already covered by public v0/V2/archive/release/viewer/diagnostic consolidation;
2. historical, rejected, or unresolved semantic experiments that should not be promoted as product functionality;
3. planning, provenance, and release-control records;
4. source-specific generated evidence and media.

The public tree therefore retains the newer accepted software-I/O, digital archive, diagnostics, physical-player, and release tooling while avoiding wholesale copying of rejected or local-only experiments.

## Remaining boundary

This closes the **folder-name reconciliation** gap. It is not a claim of byte-for-byte parity with every local file or generated output. The next step is to run the public full suite and all public digital/diagnostic demos, then review any specific accepted behavior that still lacks a public test. Only after that should CLI/app packaging work begin.

## Claim boundary

- `unsafe_acceptance_count`: `0` in the public safety/review paths;
- hardware validation claimed: `false`;
- physical Level 5 claimed: `false`;
- manufactured player claimed: `false`;
- real printer/scanner/player hardware claimed: `false`.
