# AMCF Semantic Sidecar Overlay Parity

This document records the public-safe port of the semantic micro-test sidecar and overlay diagnostic idea from the older local semantic progression band.

The source band was not final semantic/object Level 5. It contained useful mask, sidecar, approval, and overlay-player behavior that later fed the accepted semantic proof chain. This public port preserves that diagnostic shape without claiming that the micro sidecar solves general semantic AMCF.

## What Was Ported

- semantic sidecar loading and frame flattening
- persistent object and track metadata listing
- reviewer-approved frame validation
- fail-closed rejection of fake solved claims
- optional Pillow overlay rendering when image support is available
- deterministic JSON/Markdown report generation

The reusable public module is `src/amcf_semantic_sidecar_overlay.py`.

## Scope

This is a diagnostics helper for semantic sidecars and overlay review. It is not a full deep-tool integration, not a generated-media import, and not a final semantic proof by itself.

## Claim Boundary

- semantic object AMCF solved by this micro sidecar: false
- unsafe_acceptance_count: 0
- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- fake user approval accepted: false

Generated reports go under `output/amcf_semantic_sidecar_overlay/` and must not be committed.
