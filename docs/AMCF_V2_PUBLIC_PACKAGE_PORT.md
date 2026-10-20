# AMCF V2 Public Package Port

This document records the first public port of the local AMCF V2 package surface from the local test workspace.

The port adds a public `src/amcf_v2/` package derived from the local AMCF V2 integrated bounded prototype package. It preserves the newer public software I/O and physical-player work and does not import generated local archives, media, review outputs, caches, or machine-specific wrappers.

## Included Public Code

- AMCF V2 archive reader helpers
- manifest and index loaders
- payload codec contracts and registry
- WebP decode adapter with optional Pillow availability checks
- fail-closed PNG and zlib residual codec stubs
- checksum helper
- decode-plan/dependency graph contracts
- bounded frame cache
- seek controller
- playback clock/loop contracts
- visual gate and benchmark contracts

## Public Demo

Run from the public repo root:

```text
python demo/run_amcf_v2_public_package_demo.py
```

The demo writes generated output under:

```text
output/amcf_v2_public_package_demo/
```

Generated output must not be committed.

## Claim Boundary

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- real player hardware claimed: false
- unsafe_acceptance_count: 0

## Remaining Parity Work

This port does not complete all broader local workspace parity. Remaining candidates include older AMCF v0/v1 tooling, archive writer/reader integration scripts, residual/native payload experiments, selected-candidate decoder scripts, regression harnesses, and the local interactive viewer package.
