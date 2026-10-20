# AMCF Tests File Review: 05B Through 06F

## Scope

This review covers the next chronological digital-AMCF evidence band after the previously reviewed 07A/07B/07E residual and adaptive work:

- `Test 05B`
- `Test 05C_06A`
- `Test 05C2_06B`
- `Test 05C3_06C`
- `Test 05C4_06D`
- `Test 05C5_06E`
- `Test 05C5B_06E2`
- `Test 05C6_06F`

The band contains 5,178 files in total. The review inspected the primary runner for each folder, the generated status/validation reports, the archive and decoder helpers, and the public modules that cover the reusable behavior.

This is historical progression evidence. It is not a request to promote every experiment into the public runtime.

## Progression Summary

| Folder | Code and behavior inspected | Evidence result | Public disposition |
|---|---|---|---|
| `05B` | OpenCV/NumPy component extraction, seed and motion masks, crop streams, diagnostic overlays, compositor candidates, archive update, viewer, regression checks | Technical media/archive checks passed; diagnostic composite required human review and was not final playback | Reusable diagnostics and archive/report ideas retained; waterfall-specific compositor not promoted |
| `05C_06A` | Candidate compositor loop, alpha blending, fallback accounting, v0.2 archive, decoder and MP4 export | `PARTIAL_NEEDS_HUMAN_REVIEW`; decoded MP4 existed, but fallback/reference support remained and true component reconstruction was not established | Historical fallback/decode evidence only; not final codec parity |
| `05C2_06B` | Exhaustive component strategies, fallback accounting, candidate selection, v0.3 archive, decoder and MP4 export | `PARTIAL_EXHAUSTED`; best honest hybrid still used about 42% fallback; non-fallback decode was false | Do not promote the reduced-fallback candidates as final |
| `05C3_06C` | Parallax/tracking loop, component composite candidates, fallback accounting, v0.4 archive, selected decoder | Technical path passed, but selected output retained about 10.46% fallback; full zero-fallback decode was false | Progression evidence only; later visual acceptance rejected the mosaic/seam behavior |
| `05C4_06D` | Micro-component overlapping tiles, optical-flow/affine probes, no-mosaic gate, selected decoder, v0.5 archive | Accepted visual control baseline; no-mosaic gate passed, fallback was 0%, and component stream coverage was 100%; still not final compression or semantic segmentation | Preserve as the accepted visual/control reference, not as a claim of final codec completion |
| `05C5_06E` | Adaptive microcomponent rendering, motion thresholds, tile hold/update decisions, smoothness gate, v0.6 archive, MP4 export | Technical pass with about 19.897% update reduction, but later human review rejected visible instability/artifacts | Do not replace the 05C4 control with this reduction strategy |
| `05C5B_06E2` | Stability/recovery loop, hysteresis/hold behavior, jitter gate, temporal stability metrics, v0.6.1 archive, MP4 export | Small update reduction of about 0.202%; later review rejected artifacts and the result did not supersede 05C4 | Keep as rejected regression evidence; no runtime promotion |
| `05C6_06F` | Artifact audit, comparison of 05C4/05C5/05C5B, ultra-safe probes, artifact gate, rollback/freeze logic | `PASS_FREEZE_05C4`; 05C4 remained the selected full-rate control and later reductions were not accepted | Public claim boundary should reflect the freeze and visual-first rule |

## What the Code Shows

The primary runners are real executable research code, not documentation-only placeholders. They use optional local media tooling for:

- video probing and frame iteration;
- OpenCV masks, crops, overlays, blurs, optical-flow/affine probes, and video writing;
- NumPy metric/accounting arrays;
- Pillow contact sheets in the stability review;
- FFmpeg/FFprobe archive and video checks;
- archive extraction, generated decoder scripts, manifests, and regression reports.

The progression is coherent:

1. `05B` establishes component extraction and diagnostics.
2. `05C_06A` introduces a decoder and back-to-video path, but with fallback.
3. `05C2_06B` tries to reduce fallback and exhausts candidate strategies without achieving clean reconstruction.
4. `05C3_06C` improves component coverage but still leaves fallback and then fails visual acceptance.
5. `05C4_06D` restores visual quality through a full-rate micro-component control.
6. `05C5_06E` and `05C5B_06E2` attempt update reduction while protecting visual stability.
7. `05C6_06F` audits the artifacts and freezes the 05C4 control when the reduced-update candidates are not trustworthy.

This means a later folder can contain a genuine improvement in one dimension while still being rejected overall. Folder order alone is therefore not a sufficient promotion rule.

## Public Mapping

The public repository already contains reusable contracts and newer paths for the safe portions of this band:

- `src/amcf_v0/` contains public v0 archive validation, manifest, template, builder, and loader behavior.
- `src/amcf_residual_visual_acceptance.py` preserves visual-gate and accounting distinctions without claiming the old waterfall codec is final.
- `src/amcf_adaptive_component_scheduler.py` provides a deterministic scheduling primitive; it is not a claim that the rejected 05C5/05C5B codec strategies are accepted.
- `src/amcf_component_event_archive.py` and `src/amcf_video_pipeline.py` provide newer public component/event and video-package paths.
- `src/amcf_quality_metrics.py` provides public metric helpers.
- `src/amcf_motion_truth_diagnostics.py`, `src/amcf_test02_diagnostic_viewer.py`, and related public diagnostics preserve inspectable tracking/overlay/report behavior.
- Public v2 archive and archive writer/reader modules cover later, cleaner package contracts rather than copying the generated v0 waterfall experiment tree.

## Port Decision

| Evidence class | Decision |
|---|---|
| Archive structure, manifests, decoder status, regression shape | `PORTED_AND_TESTED` through public v0/v2/archive/report layers |
| Visual-first gate and explicit fallback accounting | `PORTED_AND_TESTED` through public acceptance/report helpers |
| Deterministic update scheduling abstraction | `PORTED_AND_TESTED` as a reusable primitive |
| Exact 05B-06F waterfall-specific component extraction/compositor | `LOCAL_ONLY` / `HISTORICAL_EXPERIMENT` |
| Generated MP4s, masks, crop streams, archives, contact sheets, and viewers | `GENERATED_DO_NOT_COPY` |
| Optional OpenCV/NumPy/Pillow/FFmpeg environment setup | `LOCAL_ENVIRONMENT`, not a public dependency claim |

No new runtime code is required from this band at this point. Porting the historical scripts wholesale would duplicate rejected strategies, import machine-specific media assumptions, and blur the distinction between a validated visual control and an experimental compression attempt.

## Relationship to Main and the Tests Folders

This band answers the progression question for these folders:

- The folders were not isolated unrelated attempts. They form a directed sequence where each later folder evaluates or modifies the previous candidate.
- Improvements were sometimes local to a dimension: lower fallback, fewer updates, or better artifact behavior. A later result could therefore be rejected even when one metric improved.
- The accepted `05C4` visual control and the later `05C6` freeze decision are the important historical outcomes; the rejected adaptive variants should not overwrite them.
- The public repository has the reusable behavior as safer, smaller, newer modules and diagnostics. It does not contain every generated artifact or every historical runner, and it should not claim that it does.
- This review does not establish full parity with every older or newer Tests folder. The newest-to-oldest review continues with the next older chronological band.

## Claim Boundary

- `unsafe_acceptance_count`: `0` for the public review layer.
- Hardware validation claimed: `false`.
- Physical Level 5 claimed: `false`.
- Manufactured physical player claimed: `false`.
- Real printer, reader, scanner, motors, sensors, cartridges, or player hardware claimed: `false`.
- The v0/v2 and diagnostic paths are software and fixture/research behavior only.

## Generated Output Policy

The historical folders contain generated videos, masks, archives, crops, contact sheets, reports, extracted trees, and environment-specific paths. Those are evidence inputs, not public source-of-truth files. They remain excluded from the public repository; only reviewed reusable logic and claim-safe documentation are retained.

## Status

This band is reviewed and recorded. The next step is to continue downward through the older chronological folders, then review the remaining non-`Tests` workspace directories and compare the resulting ledger against `Main` and the public repository before planning CLI/app completion.
