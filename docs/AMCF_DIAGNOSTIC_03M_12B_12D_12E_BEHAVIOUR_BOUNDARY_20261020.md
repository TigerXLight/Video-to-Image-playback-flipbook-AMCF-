# AMCF Diagnostic 03M / 12B / 12D / 12E Behaviour Boundary

Run: `AMCF_DIAGNOSTIC_03M_12B_12D_12E_BEHAVIOUR_BOUNDARY_20261020`

This note records the distinction between the historical green motion view and
the later proxy/object-candidate views. They are related process diagnostics,
but they are not interchangeable tracking or mask contracts.

## 03M Green Motion Designation

03M compares consecutive frames after estimating camera registration. Its
green overlay marks residual local motion inside named zones. The zone map
includes areas such as the waterfall, leaves, branches, the white-figure area,
tree body, and static background.

That means 03M is a **camera-compensated motion designation**. It answers:

```text
Where is motion left after the apparent camera movement is removed?
```

It does not answer:

```text
Which pixels are a confirmed person with a persistent identity?
```

The 03M zone, residual mask, missing-region, and component-coverage views are
therefore process diagnostics. Test 02 contour state remains the only geometry
allowed to drive component-owned AMCF event masks in Main.

## 12B Original Proxy Behaviour

The reference behavior is:

```text
Tests/Test 12B/20261006_164238/diagnostic_overlays/semantic_proxy_water_vs_object_overlay_12B.mp4
```

The original 12B runner uses classical motion proposals plus simple IoU/
centroid-style matching. Its palette is:

| Layer | Color | Meaning |
| --- | --- | --- |
| object candidate | green | person or moving-object candidate |
| fluid candidate | orange | water/fluid-motion candidate |
| uncertain | yellow | unresolved motion region |
| global motion | magenta | camera/global-motion candidate |

The 12B manifest contains 1,403 persistent proxy tracks:

```text
proxy_person_or_moving_object: 1,092
proxy_water_or_fluid_motion:       4
proxy_uncertain:                 307
```

12B explicitly says that these are proxy IDs, not verified object identities;
semantic object AMCF is not solved and human review is required. The water vs
object overlay is nevertheless the correct historical diagnostic for showing
the process distinguishing object candidates from fluid motion.

Main now renders this exact 12B palette and schema as the separate profile
`12B_semantic_proxy_candidates`. The current audit found 224 leftward
person/object proxy candidates using its 2-pixel direction threshold. That is
candidate motion evidence only, not a confirmed person result.

## 12D Calibration and 12E Review

12D carries the calibrated 12C candidate set. Main reports 215 leftward
person/object candidate tracks from that set, while keeping proxy boxes out of
component masks.

12E is the later conservative reviewed taxonomy. It preserves all reviewed
tracks, but only one reviewed `person_or_moving_object` example was confirmed
in the local evidence (`cal12c_0117` / `track_282`), and it moves slightly to
the right. The reviewed evidence has zero confirmed leftward person tracks.

This is not a contradiction:

```text
12B = broad green proxy candidates
12D = calibrated candidate proxies
12E = conservative reviewed proxy labels
03M = camera-compensated residual motion zones
Test 02 = contour-backed component geometry
```

## Main Coverage Result

The expanded audit is:

```text
Main/output/amcf_diagnostic_coverage_audit_20261020_12b/DIAGNOSTIC_COVERAGE_REPORT.md
```

It passes these profiles from Main:

```text
03M complete motion-truth family
08E heat and diff-x8 behavior
10A third-water ROI review
10B fourth-people ROI review
12B original green proxy candidate behavior
12D calibrated proxy behavior
12E reviewed proxy behavior
```

The diagnostic layer is therefore represented without falsely claiming that a
proxy box is a segmentation mask or that a moving box is a verified identity.
HOOT remains the separate bounded dataset-annotated semantic Level 5 proof.

## Remaining Claim Boundaries

- Universal arbitrary-video person/object identity tracking is not claimed.
- Source-independent compact native AMCF storage at or below the source-size
  ceiling is still a separate unresolved requirement.
- The physical PC-to-reader/player/printer path remains software simulation and
  planning; no hardware validation is claimed.
- Generated diagnostic videos remain evidence, not release source payloads.

