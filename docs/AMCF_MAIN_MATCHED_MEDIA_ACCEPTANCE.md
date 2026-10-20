# AMCF Main Matched-Media Acceptance

Run: `AMCF_MAIN_V2_APPLES_TO_APPLES_COMPARISON_V2`

This is a bounded acceptance checkpoint for the maintained local `Main` project. It compares accepted AMCF outputs against the correct source truth for each video. It does not claim that generated media is byte-identical, that every historical experiment is an application feature, or that physical hardware exists.

## Matched Comparisons

The waterfall outputs are compared only with the accepted 07A normalized truth:

- accepted 07A decoded output: `<workspace-root>/Tests/Test 07A/20261006_021146/decoded_outputs/AMCF_07A_DECODED_BACK_TO_VIDEO.mp4`
- 07A truth baseline: `<workspace-root>/Tests/Test 07A/20261006_021146/baseline_downscale/ORIGINAL_TRUTH_640x320_23p976.mp4`
- Main component output: `<workspace-root>/Tests/Test AMCF_MAIN_PUBLIC_MEDIA_ACCEPTANCE/20261015_131327/local_main_component_native/component_decoded.mp4`

The 13C3 output is a different 30-second river-boat source and is compared only with its own archive truth:

- 13C3 archive: `<workspace-root>/Tests/Test 13C3_STREAMABLE_ARCHIVE_LAYOUT/20261007_032419/experimental_archive/AMCF_V1_EXPERIMENTAL_STREAMABLE_LAYOUT_13C3.amcfv1stream.zip`
- 13C3 decoded output: `media/decoded_output.mp4` inside that archive
- 13C3 truth: `media/truth_baseline.mp4` inside that archive

## Results

| matched path | frames | mean MAE | duration | motion result |
| --- | ---: | ---: | ---: | --- |
| 07A decoded vs 07A truth | 288/288 | 2.0067 | 12.012 s | matched; mean translation difference 0.0033 |
| Main component vs 07A truth | 288/288 | 2.6247 | 12.000 s | matched; mean translation difference 0.0070 |
| 13C3 decoded vs 13C3 truth | 901/901 | 2.5393 | 30.063 s | matched; mean translation difference 0.0351 |

The Main output is approximately `0.1%` shorter than the 07A truth because it is encoded at `24/1` rather than `24000/1001`. This is not a meaningful playback speedup. The 13C3 output duration ratio is effectively `1.0`, so it also shows no measured speedup.

The pixel comparisons are made after MP4 decoding and therefore are not expected to be byte-identical. The measured differences are encoding/compositor differences, not evidence that the frame sequence was accelerated.

## What This Checkpoint Proves

- the accepted 07A waterfall output and current Main component output preserve the same frame count;
- Main preserves the waterfall camera/motion profile within the measured bounded tolerance;
- the experimental 13C3 streamable output preserves its own 901-frame sequence and duration;
- the earlier cross-video comparison was invalid and has been replaced by matched-source comparisons;
- no source or public-repository runtime code was changed by the comparison;
- `unsafe_acceptance_count` remains `0`;
- hardware validation, physical Level 5, and manufactured-player completion remain unclaimed.

## What It Does Not Prove

This checkpoint does not by itself prove that Main has one integrated command which creates every accepted historical artifact from a source video through the full residual/native/V2 progression. Main already contains the relevant component, diagnostic, V2, archive, and CLI modules. The Main/public-checkout path assumptions in the test harness have been repaired; the full Main suite now passes 500 tests. The progression is still represented by bounded modules and accepted evidence rather than one universal historical replay.

The remaining work is therefore completion orchestration and harness cleanup, not a conclusion that the measured Main output is playing faster or that the accepted decoded-video result is absent.

## Unified Main Acceptance Runner

Run:

```text
<codex-runtime-python> demo/run_amcf_main_unified_digital_acceptance.py
```

The runner performs a bounded source-video roundtrip, consumes the existing component/native/residual evidence by reference, checks diagnostics and matched media comparisons, and writes its report under `Main/output/amcf_main_unified_digital_acceptance/`. It does not copy historical generated evidence into Main.

The runner's `final_passed` value means that the bounded acceptance checks passed. The runner now connects the source-video, component, diagnostics, native-reader, residual-evidence, and decoded-video checks in one reproducible acceptance command. `main_completion_ready` remains false until a generated canonical component archive satisfies both the source-size ceiling and visual gate, and the residual/native/V2 path is generated end-to-end rather than consumed as accepted historical evidence.

## Evidence

Generated comparison evidence is kept outside tracked source and docs under:

`<workspace-root>/Tests/Test AMCF_MAIN_V2_APPLES_TO_APPLES_COMPARISON/20261015_151031/`

Important files:

- `APPLES_TO_APPLES_COMPARISON.md`
- `apples_to_apples_comparison.json`
- `waterfall_truth_07a_main_comparison.mp4`
- `13c3_truth_decoded_comparison.mp4`

Generated media is evidence only and is not copied into `Main` or committed to the public repository.

## Claim Boundary

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- real motors/sensors/cartridges validated: false
- unsafe_acceptance_count: 0
