# AMCF Tests File Review: Semantic Lost/Recovered Progression

## Scope

This review covers the three folders immediately preceding the Level 5 Main promotion:

- `Test AMCF_REAL_WORLD_OCCLUSION_SOURCE_ACQUISITION/20261009_220119`
- `Test AMCF_CONTROLLED_LOST_RECOVERED_LEVEL5_PROOF/20261009_213727`
- `Test AMCF_HOOT_REAL_WORLD_LOST_RECOVERED_LEVEL5_SOLVER/20261009_220908`

They are a progression: source acquisition and ranking, controlled proof, then dataset-annotated real-world proof. They are not three interchangeable implementations.

## File-Level Findings

| Folder | Files | Useful source | Evidence/generated content | Public status |
| --- | ---: | --- | --- | --- |
| Real-world source acquisition | 528 | one OpenCV/NumPy/Pillow acquisition-and-ranking runner plus audit/status docs | downloaded AVI clips, sampled JPEGs, contact sheets, manifests | `LOCAL_ONLY` runner; source-acquisition result represented as historical evidence |
| Controlled lost/recovered proof | 501 | one deterministic OpenCV/NumPy/Pillow generator/validator with synthetic MP4, masks, overlays, and semantic sidecar | 160-frame MP4, PNG frame/mask/overlay sets, reports, CSV/JSON | accepted proof scope represented publicly; original generator not copied |
| HOOT lost/recovered solver | 163 | one network/SAM2/OpenCV/NumPy/Pillow runner with official annotation parsing, event selection, masks, overlays, and sidecar construction | downloaded dataset ZIP, extracted frames, masks, overlays, sheets, reports, CSV/JSON | accepted proof scope represented publicly; external runner/data not copied |

The three folders contain 1,192 files in total. The large majority are generated media, downloaded source data, or run-specific reports. The source runners were read and classified; they are not being treated as source merely because they are Python files.

## Progression and Acceptance

### Source acquisition

The acquisition runner downloaded seven preview clips, sampled frames with OpenCV, ranked occlusion candidates, and explicitly ended with “source acquisition/ranking only.” It did not solve lost/recovered reconstruction or Level 5. This is historical input-selection evidence, not a missing public core encoder/decoder.

### Controlled proof

The controlled runner generated a deterministic synthetic sequence, stable object masks, an occluded interval, recovery state, semantic sidecar, and Level 5 status. Its claim was limited to the controlled canonical vector. It used OpenCV, NumPy, and Pillow and generated private media; the public repo does not claim to reproduce this run’s exact files.

### HOOT proof

The HOOT runner parsed official frame-level annotations, selected a visible-present -> full-occlusion -> visible-present event, generated visible-frame SAM2 masks, and wrote a semantic sidecar. Its final claim was limited to that dataset-annotated vector and explicitly excluded unrelated videos. It requires network access, downloaded data, SAM2 checkpoints, OpenCV, NumPy, and Pillow. Those requirements are intentionally outside the standard-library public core.

## Public Mapping

The reusable public mapping is `src/amcf_semantic_level5_proof.py` with its tests, demo, and report. It preserves:

- the two accepted vector identities;
- the distinction between acquisition, candidate, controlled, and dataset-annotated evidence;
- the earlier non-accepted deep-tool and mask/tracking runs;
- the bounded claim scopes;
- `unsafe_acceptance_count: 0`;
- false physical hardware, physical Level 5, and manufactured-player flags.

The public mapping is a claim-safe evidence/proof index, not a replacement for the original deep-tool runners. The original runners are therefore classified as `LOCAL_ONLY` / `NEEDS_MANUAL_REVIEW` for any future optional semantic-toolchain package.

## What Must Not Be Copied as Public Core

- downloaded HOOT or BU/LGM source media;
- SAM2 checkpoints or model caches;
- generated frame, mask, overlay, and contact-sheet floods;
- private absolute paths;
- network-download behavior in the standard public demos;
- a general Level 5 claim for arbitrary videos;
- hardware or physical-player claims.

## Parity Decision

The accepted semantic/object proof *scope* is represented and tested publicly. The exact deep-tool execution and its source/generated outputs are not ported. This is an intentional dependency/data boundary, not an accidental omission. If full local semantic-runner parity is later required, it needs a separate optional-dependency phase with explicit provenance, checkpoint configuration, bounded fixtures, and tests; it should not be folded into the default CLI or public standard-library path.

## Claim Boundary

- hardware validation claimed: false;
- physical Level 5 claimed: false;
- manufactured player claimed: false;
- real motors/sensors/cartridges/physical optics: not claimed;
- `unsafe_acceptance_count`: 0 for the public semantic proof report;
- generated output committed: no.

