# AMCF Semantic Level 5 Proof Parity

This document records the public-safe summary of the accepted semantic/object Level 5 proof chain from the local progression folders.

It is not a physical-player proof. It does not claim real hardware validation, physical Level 5 completion, manufactured-player completion, real sensors, real motors, real cartridges, real optical proof, or a built prototype.

## What Was Ported

- controlled canonical lost/recovered proof status
- HOOT dataset-annotated lost/recovered proof status
- Main-facing vnext promotion status
- earlier pre-Level-5 semantic bridge runs marked as not accepted Level 5
- explicit claim-boundary flags
- unsafe-acceptance accounting

The reusable public module is `src/amcf_semantic_level5_proof.py`.

## Accepted Semantic/Object Proof Vectors

| Vector | Status | Scope |
| --- | --- | --- |
| controlled canonical lost/recovered vector | accepted | controlled canonical vector only |
| HOOT dataset-annotated real-world occlusion vector | accepted | dataset-annotated vector only |

The Main-facing promotion is represented by `src/amcf_vnext.py`; this parity layer records the proof timeline around it.

## Earlier Runs

The following kinds of runs are preserved as important progress but not treated as semantic/object Level 5 acceptance:

- segmentation and tracking tool survey
- optional deep semantic toolchain smoke integration
- deep bridge retry runs
- full proxy deep mask-track binding
- high-precision mask cluster validation
- automatic lost/recovered candidate closure that was downgraded after review

## Claim Boundary

- semantic/object Level 5 accepted vectors: 2
- unsafe_acceptance_count: 0
- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- real sensors validated: false
- real motors validated: false
- real cartridges validated: false
- physical-player proof claimed: false

Generated reports go under `output/amcf_semantic_level5_proof/` and must not be committed.
