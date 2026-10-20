# AMCF Tests Newest-to-Oldest Part 16: V2 Native and Closeout Review

Run context: `AMCF_TESTS_NEWEST_TO_OLDEST_DEEP_REVIEW_CONTINUE_V1`

This part reviews the newest bounded digital AMCF groups from `14H` back through
`14A`, together with the `13M` closeout evidence that those groups import. The
purpose is to determine which behavior is accepted runtime behavior and which
files are only benchmark evidence, generated output, historical runners, or
unaccepted codec investigations.

## Reviewed Groups

| Local group | Evidence reviewed | Public disposition |
| --- | --- | --- |
| `Test 14H_LARGER_BOUNDED_V2_SAMPLE_GENERALISATION` | bounded sample decision, decoder report, failure modes, benchmark and size reports, 16 variant archives | `PORTED_AND_TESTED` for the bounded archive reader in `src/amcf_v2_14h_archive.py`; generated samples and the local runner remain evidence |
| `Test 14J_WEBP_DEMO_CODEC_COMPONENT_METADATA_SIDECAR` | sidecar schema, reader, evaluation, regression results, recommendation, 48/96-frame sidecar evidence | `PORTED_AND_TESTED` through `src/amcf_v2_sidecar_metadata.py`, its demo, and tests |
| `Test 14I_EXTERNAL_REVIEW_DOCUMENTATION_PACKAGE` | claim ledger, evidence summary, codec decision, limitation ledger, external review documents | `DOCS_AND_EVIDENCE`; no additional runtime source was required |
| `Test 14G_V2_OFFLINE_VIEWER_REPORT_UI` | offline viewer/report evaluation, failure modes, imported 14F package references | `CONSOLIDATED_PUBLIC_VIEWER`; generated HTML and sample evidence remain local |
| `Test 14F_V2_INTEGRATED_BOUNDED_PROTOTYPE_PACKAGE` | package manifest, package status, 39-file `amcf_v2` source package, bounded validation | `PUBLIC_EXACT_WITH_ONE_SAFE_DEPENDENCY_DIFF`; public has all 39 package paths and 38 byte-identical files |
| `Test 14E`, `14E2`, `14E3` | codec investigations, component-delta variants, motion metadata, decision reports | `RESEARCH_EVIDENCE_NOT_RUNTIME`; no general codec acceptance was recorded, so these are not copied wholesale |
| `Test 14D_V2_PLAYBACK_LOOP_DRY_RUN` | reader/decode/cache/seek/compositor/playback dry-run evidence | `PORTED_AND_TESTED` through public V2 playback modules and tests |
| `Test 14C_V2_WEBP_CODEC_DECODE_ADAPTER` | bounded WebP decode adapter and exact frame checks | `PORTED_AND_TESTED` through public V2 codec/decode modules and tests |
| `Test 14B_V2_READONLY_ARCHIVE_READER` | archive/index/manifest read contracts | `PORTED_AND_TESTED` through public V2 container/decode modules and tests |
| `Test 14A_V2_NATIVE_CODEC_PLAYER_ARCHITECTURE` | architecture/contracts/failure modes and 13M imported evidence | `PORTED_AND_TESTED` as the public bounded V2 package contract |
| `Test 13M_FINAL_BENCHMARK_VALIDATION_SPEC` | final proof ledger, benchmark summary, playback readiness, limitation ledger, 07G/08B/13I/13J/13J2/13P imported evidence | `ACCEPTED_BOUNDED_PROTOTYPE_EVIDENCE`; public V2, archive writer/reader, quality gates, playback index, and release acceptance layers represent the accepted bounded behavior |

## Accepted Behavior Confirmed

The public repository contains tested representations of the accepted bounded
chain:

```text
bounded native archive
-> manifest/index read
-> payload decode
-> frame reconstruction/compositing
-> cache/seek/playback dry run
-> sidecar metadata and diagnostics
-> fail-closed validation and claim-boundary reporting
```

The public V2 demo and focused V2 tests pass. The 14H reader was also validated
against the available local 48- and 96-frame variant archives, with recorded RGB
frame checksums matching. This is a bounded archive/read proof, not a claim that
the local research experiments produced a generally superior codec.

## Deliberate Exclusions

The following are not missing accepted application behavior:

- generated 14A–14J HTML, JSON, CSV, image, video, and archive evidence;
- repeated imported copies of earlier groups inside 14H and 14J;
- dated runner scripts and local command wrappers;
- 14E/E2/E3 codec investigations without final general acceptance;
- local media, checkpoints, caches, and environment-specific launch files.

The 13M limitation records still state that production playback, a general
full-video native archive, a generally solved custom component codec, and the
semantic/object branch were not accepted as final product claims. The public
repository preserves those boundaries rather than converting research evidence
into an unsupported completeness claim.

## Result

No missing accepted runtime behavior was identified in this group. No source
port is required from the reviewed 14A–14J/13M files at this point. The next
parity work continues with the older `13F`–`13P` source progression and then the
earlier v0/diagnostic groups, resolving each source candidate or explicitly
marking it as superseded, historical, generated evidence, or third-party.

`unsafe_acceptance_count`: `0`.

Hardware validation claimed: `false`.

Physical Level 5 claimed: `false`.

Manufactured player claimed: `false`.
