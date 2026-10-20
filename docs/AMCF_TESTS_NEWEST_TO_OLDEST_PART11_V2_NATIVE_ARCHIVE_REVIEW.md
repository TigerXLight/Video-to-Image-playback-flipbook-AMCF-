# AMCF Tests Newest-To-Oldest Part 11 V2 Native Archive Review

Part 11 reviewed the local V2/native archive and playback progression band.

## Folder Band Reviewed

- `Test 14J_WEBP_DEMO_CODEC_COMPONENT_METADATA_SIDECAR`
- `Test 14I_EXTERNAL_REVIEW_DOCUMENTATION_PACKAGE`
- `Test 14H_LARGER_BOUNDED_V2_SAMPLE_GENERALISATION`
- `Test 14E3_MOTION_AWARE_COMPONENT_DELTA`
- `Test 14E2_HYBRID_COMPONENT_DELTA_REFINEMENT`
- `Test 14E_V2_CUSTOM_COMPONENT_AWARE_CODEC_INVESTIGATION`
- `Test 14G_V2_OFFLINE_VIEWER_REPORT_UI`
- `Test 14F_V2_INTEGRATED_BOUNDED_PROTOTYPE_PACKAGE`
- `Test 14D_V2_PLAYBACK_LOOP_DRY_RUN`
- `Test 14C_V2_WEBP_CODEC_DECODE_ADAPTER`
- `Test 14B_V2_READONLY_ARCHIVE_READER`
- `Test 14A_V2_NATIVE_CODEC_PLAYER_ARCHITECTURE`
- `Test 13M_FIX_13Q_13R_12K_GATE_CLOSEOUT`
- `Test 13M_FINAL_BENCHMARK_VALIDATION_SPEC`
- `Test 13P_NATIVE_PAYLOAD_CODEC_FEASIBILITY`
- `Test 13D2_13O_SPARSE_RESIDUAL_PAYLOAD_OPTIMISATION`
- `Test 13J2_13N_LONGER_NATIVE_ARCHIVE_SAMPLE`
- `Test 13D_13L_RESIDUAL_KEYFRAME_SCHEDULING_OPTIMISATION`
- `Test 13J_13K_NATIVE_READER_COMPOSITOR_INTEGRATION`
- `Test 13I_REAL_NATIVE_PAYLOAD_ARCHIVE`
- `Test 13H_NATIVE_RESIDUAL_COMPONENT_DECODER_INVESTIGATION`
- `Test 13G_NATIVE_COMPOSITOR_FRAME_RECONSTRUCTION`
- `Test 13F_NATIVE_READER_COMPOSITOR_SKELETON`

## Findings

This band is the local progression from a native reader/compositor skeleton into a bounded V2 archive reader, WebP decode adapter, playback-loop dry run, integrated V2 prototype package, review package, and 14J sidecar decision.

The public repo already represents the 14F V2 package through `src/amcf_v2/`, the V2 public package demo, and tests. Earlier ledger work found the public package has matching Python file coverage with one intentional public-safe dependency-handling difference.

The useful missing piece in this part was the 14J metadata sidecar contract:

- WebP remains the bounded demo payload codec.
- Component metadata is carried in a sidecar.
- Proxy regions remain review/editability metadata, not semantic-object proof.
- Claim flags remain false.
- Generated local archives are not copied.

## Public Action

Part 11 adds:

- `src/amcf_v2_sidecar_metadata.py`
- `demo/run_amcf_v2_sidecar_metadata_demo.py`
- `tests/test_amcf_v2_sidecar_metadata.py`
- `docs/AMCF_V2_SIDECAR_METADATA_PARITY.md`

## Progression Interpretation

The 13F through 14J folders do contain separate locked progressions. The later 14F/14J folders supersede the earlier skeleton-only and investigation-only folders for public packaging purposes.

The public repo should keep:

- the existing `src/amcf_v2/` V2 package surface
- the optional WebP decode boundary
- fail-closed unsupported codec handling
- bounded seek/playback contracts
- the 14J sidecar metadata reader added in this part

The public repo should not bulk-copy:

- generated local V2 archives
- generated media outputs
- imported benchmark folders
- local review packs with machine-specific paths
- investigation-only files that explicitly kept solved flags false

## Claim Boundary

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- full native playback solved by this part: false
- final playback engine solved by this part: false
- custom component codec solved by this part: false
- proxy regions are semantic objects: false
- generated output committed: false
- unsafe_acceptance_count: 0
