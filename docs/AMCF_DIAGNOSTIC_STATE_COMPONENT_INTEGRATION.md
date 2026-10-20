# AMCF Diagnostic State Component Integration

Run contract: `AMCF_DIAGNOSTIC_PROFILE_BUNDLE_COMPLETION_V1`

This document defines the diagnostic handoff used by the local `Main` component-event path. It keeps the historical diagnostic progression visible without pretending that every visual diagnostic is a segmentation mask or a semantic proof.

## State Flow

```text
Test 02 track manifest
        |
        v
normalized amcf-diagnostic-state-v1
        |
        +--> contour-backed component events
        |        + exact residual closure for uncovered changes
        |
        +--> embedded diagnostics/diagnostic_state.json
        |
        +--> 03M / 08E / 10A_10B / 12E / HOOT process contracts
```

The state bundle is path-free and source-independent. It contains source dimensions, frame timing, normalized tracks, component IDs, polygon contours where available, update reasons, motion fields, taxonomy, process contracts, claim boundaries, and a state hash. Generated videos, absolute local paths, and the source MP4 are not embedded in the state bundle.

## What Drives Events

Only normalized Test 02 polygon contours are allowed to drive masked component events in this integration. Bbox-only rows are rejected as component masks. For every non-base frame, the encoder applies eligible contour-backed events and then emits an exact residual event for every changed pixel not covered by those masks. The encoder asserts byte-identical frame closure before writing the archive.

This means the diagnostic layer can influence component ownership and state reading without dropping information. The residual event is not a fallback video; it is the explicit lossless closure of the same AMCF frame state.

Held or unchanged rows are accounted for explicitly. A logical Test 02 track row can have no payload event when its masked pixels do not change, but the row remains in the embedded diagnostic state with its component ID, geometry, timing, visibility, motion, and update reason. The archive report distinguishes `logical_diagnostic_track_row_count` from `track_event_count`; this prevents normal AMCF hold-state behavior from being mistaken for event loss.

## Profile Boundaries

| Profile | Role in the contract | Used as component mask? |
| --- | --- | --- |
| Test 02 | track IDs, contours, masks, motion fields, event geometry | Yes, polygon contours only |
| Test 03M | camera-compensated green zone motion and missing-motion review | No, diagnostic measurement |
| Test 08E | Farneback/TURBO motion heat and `diff x8` comparison behavior | No, diagnostic measurement |
| Test 10A/10B | crop review, `diff x8`, and ROI motion ratios; runnable through the Main coverage audit | No, review evidence |
| Test 12D | calibrated semantic proxy candidates and water/object review overlays | No, proxy boxes are not masks |
| Test 12E | reviewed proxy taxonomy and narrow event review | No, proxy boxes are not masks |
| HOOT | bounded real-world/dataset-annotated lost/recovered semantic proof | No, separate semantic claim |

The normalized bundle records whether a profile was active in a run, rendered only as a bounded artifact, or retained as historical evidence. A profile marked as not embedded is not silently upgraded to a universal claim.

## Coverage Audit

The maintained profile runner is:

```text
Main/demo/run_amcf_diagnostic_coverage_audit.py
```

It runs the accepted local evidence through six profile families: the complete
03M motion-truth family, 08E motion heat/diff, 10A water ROI, 10B people ROI,
12D calibrated proxy, and 12E reviewed proxy. The 03M family itself emits the
raw screen-motion, camera-compensated residual, residual mask, zone-motion,
component-coverage, camera-vector, missing-region, original-reference, and
side-by-side comparison views. The audit writes generated evidence under
`Main/output/` and records the exact profile status, motion ratios, proxy
direction counts, review boundaries, and `unsafe_acceptance_count`.

The 2026-10-20 run passed all six profile renders and the complete 03M family.
It found 215 leftward 12D person/object-labelled candidate tracks, but zero
12E reviewed leftward person tracks. The only reviewed person/object positive
(`track_282`, frames 45-60) moves slightly right (`dx=+4`, `dy=+3`). Therefore
temporal box motion is implemented, but a confirmed right-to-left white-dot /
person semantic claim remains unproven. A fixed 03M zone is not a per-person
tracker and must not be used as evidence for that claim.

The authoritative generated audit is:

```text
Main/output/amcf_diagnostic_coverage_audit_20261020_full/DIAGNOSTIC_COVERAGE_REPORT.md
```

## Acceptance Requirements

- all source frame hashes remain the canonical frame reference;
- every diagnostic-driven component event has a payload checksum;
- every uncovered changed pixel is closed by an exact residual event;
- archive decoding does not require the source MP4;
- decoded frame hashes match the source manifest frame bytes;
- `unsafe_acceptance_count` remains zero;
- hardware, physical Level 5, manufactured-player, and universal semantic claims remain false unless separately proven.

The 288-frame integration is a functional diagnostic-state proof, not a size-ceiling proof. Generated archives remain under `Main/output/` and must not be copied into source or release packages as if they were maintained code.
