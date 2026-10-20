# AMCF Tests File Review: 07A, 07B/07C/07D, and 07E/07F/07G/07H/08A

## Scope

This batch covers the older waterfall digital reconstruction progression immediately before the 07I decision and later v2 work:

- `Test 07A/20261006_021146`;
- `Test 07B_07C_07D/20261006_022713`;
- `Test 07E_07F_07G_07H_08A/20261006_024118`.

The three folders contain 452 files. They are historical codec/compositor experiments with generated videos, archives, metrics, and viewers; they are not three separate current archive formats to copy wholesale.

## Progression Results

| Folder | Actual implementation inspected | Recorded result | Public parity decision |
| --- | --- | --- | --- |
| 07A | FFmpeg truth baseline, non-overlap compositor, overlap-weighted compositor, MAE/MSE/PSNR/temporal metrics, v0.7 archive | `PASS_ORIGINAL_TRUTH_FULLRATE`; selected overlap-weighted compositor; no compression proof | `PUBLIC_EQUIVALENT_TESTED` for bounded quality/visual-gate behavior; generated waterfall archive/media not copied |
| 07B/07C/07D | eight adaptive tile strategies, protected regions, hysteresis/hold experiments, update accounting, component schedule, v0.8 archive, decoded MP4 | `PASS_FULLRATE_TRUTH_FREEZE`; selected full-rate control with `0.0%` update reduction; no compression proof | `SUPERSEDED_BY_LATER_ACCEPTED_WORK` for the specific adaptive codec; schedule and claim-safe archive contracts are represented by public scheduler/archive layers |
| 07E/07F/07G/07H/08A | twelve residual strategies, keyframe/residual reconstruction, raw/compressed residual accounting, visual gate, v0.9 archive, decoded MP4, deferred generalisation/semantic tracking | `PASS_RESIDUAL_COMPRESSION_SAFE`; selected long keyframe interval; 84.342503% reduction against full-rate component estimate; generalisation not run; semantic tracking deferred | `PORTED_AND_TESTED` for gate/accounting/report behavior; `LOCAL_ONLY` for the waterfall-specific encoder/decoder and generated archive |

## Important Interpretation

The 07E claim is specifically residual-stream compression versus a full-rate component-stream estimate. It is not a claim that the residual stream beat the source MP4, and it is not proof that the public component-event archive uses the same codec. The public parity documentation correctly preserves this distinction.

The 07B selected result is full-rate control, not a successful adaptive update reduction. The public `src/amcf_adaptive_component_scheduler.py` is a reusable deterministic scheduling primitive, not evidence that the rejected/unstable 07B strategies should replace the later public component-event path.

## Public Mapping

- `src/amcf_residual_visual_acceptance.py` ports the 07E visual thresholds, temporal checks, residual-size accounting distinction, human-review gate, and false claim flags.
- `src/amcf_v0/` plus `demo/run_amcf_v0_public_archive_toolchain_demo.py` and tests preserve the safe v0 archive/template/manifest validation surface without copying private media or old ZIPs.
- `src/amcf_adaptive_component_scheduler.py` provides a small tested update-decision/schedule contract.
- `src/amcf_component_event_archive.py` and `src/amcf_video_pipeline.py` are newer public digital archive/decode paths; they are not asserted to be byte-identical to the 07E local residual codec.

## Files Not Copied

- waterfall source video and derived truth baselines;
- generated candidate MP4s and side-by-side comparison videos;
- `*.amcfv0.zip` run archives and residual binary streams;
- run-local FFmpeg/OpenCV/NumPy/Pillow orchestration;
- machine-local paths and output folders;
- rejected adaptive strategies or older compositor methods as default behavior.

## Parity Decision

The 07A/07B/07E progression is represented at the level of accepted metrics, safety gates, scheduling contracts, v0 validation, and newer public digital archive behavior. Exact local waterfall codec parity remains open and would require a separate bounded port with a reproducible fixture and dependency policy. It must not be inferred from the existence of a decoded MP4 or from a smaller residual stream alone.

## Claim Boundary

- `unsafe_acceptance_count`: 0 in the public residual/v0 report layers;
- hardware validation claimed: false;
- physical Level 5 claimed: false;
- manufactured player claimed: false;
- real printer/scanner/player/motor/sensor/cartridge/optical validation: not claimed;
- generated output committed: no.

