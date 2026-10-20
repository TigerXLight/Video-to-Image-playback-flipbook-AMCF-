# AMCF Tests Newest-To-Oldest Part 12 Runtime Optimisation Review

Part 12 reviewed the runtime/archive optimisation and manual semantic review band below the V2/native archive chain.

## Folder Band Reviewed

- `Test 13C3_STREAMABLE_ARCHIVE_LAYOUT`
- `Test 13E_PLAYBACK_READER_PROTOTYPE`
- `Test 13C2_DECODE_PLAN_SEEK_INDEX`
- `Test 13C_RUNTIME_PLAYBACK_ARCHIVE_LAYOUT`
- `Test 13B_CODEC_BITRATE_SWEEP`
- `Test 13A_OPTIMISATION_BASELINE`
- `Test 12J_REVIEW_ASSIST`
- `Test 12J`
- `Test 12I`
- `Test 12H`
- `Test 12G`
- `Test 12F`
- `Test 12E`
- `Test 12D_SCREENSHOT_REVIEW`
- `Test 12D_FIX`
- `Test 12D`
- `Test 12C`
- `Test 12B`
- `Test 11B`
- `Test 11A_12A_13A`
- `Test 10A_10B`
- `Test 09A_09B`
- `Test 08E`
- `Test 08B_08C_08D`

## Findings

This band contains two different progression lanes.

The runtime/archive lane produced useful planning behavior:

- 13A started optimisation baselines but did not solve final optimisation.
- 13B produced codec/bitrate sweep evidence.
- 13C identified decode-plan and seek-index layout as the recommended playback optimisation.
- 13C2 created an external decode/seek index prototype.
- 13E created an indexed playback reader prototype with startup and playback plans.
- 13C3 explored streamable layout but did not solve native playback or final playback engine.

The semantic review/mask lane produced important review packs, masks, and human-review scaffolding, but it kept `semantic_object_solved` false and `human_review_required` true. Later accepted public ports cover the reusable sidecar overlay diagnostics and Level 5 proof summaries without reimporting local review packs or generated masks.

## Public Action

Part 12 adds:

- `src/amcf_playback_index_planner.py`
- `demo/run_amcf_playback_index_planner_demo.py`
- `tests/test_amcf_playback_index_planner.py`
- `docs/AMCF_PLAYBACK_INDEX_PLANNER_PARITY.md`

## Progression Interpretation

The public repo should keep the 13C2/13E archive planning idea because it is a reusable code path: load indexes, plan startup metadata reads, plan playback media reads, and validate fingerprints before accepting an archive.

The public repo should not bulk-copy:

- generated review images
- generated review ZIPs
- generated benchmark videos
- local generated archives
- local absolute paths
- manual-review CSV drafts as final truth
- semantic review artifacts that explicitly remained unsolved

## Claim Boundary

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- final playback engine claimed by this part: false
- semantic object solved by this part: false
- generated output committed: false
- unsafe_acceptance_count: 0
