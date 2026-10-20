# AMCF V2 Sidecar Metadata Parity

This document records the public-safe parity port for the accepted 14J-style WebP demo payload plus component metadata sidecar layer.

The local 14J run kept WebP lossless whole-frame payloads as the bounded demo codec and attached a component metadata sidecar for reviewability, editability evidence, proxy-region lifespan inspection, and claim-boundary preservation.

## Public Code

- `src/amcf_v2_sidecar_metadata.py`

The module provides:

- deterministic demo sidecar archive creation
- read-only sidecar archive inspection
- native manifest, payload manifest, sidecar, seek-index, and region-table readers
- frame listing
- per-frame proxy region lookup
- proxy region lifespan summary
- payload checksum validation
- fail-closed required-entry validation
- claim flag verification

## Demo

Run from the public repo root:

```text
python demo/run_amcf_v2_sidecar_metadata_demo.py
```

Generated output is written under:

```text
output/amcf_v2_sidecar_metadata_demo/
```

Generated output must not be committed.

## Relationship To V2

The existing public `src/amcf_v2/` package already covers the V2 archive reader, manifest/index loading, payload codec registry, optional WebP decode adapter, bounded frame cache, seek controller, playback loop contracts, and benchmark/visual gate contracts.

This sidecar module adds the missing 14J metadata-sidecar reader contract. It does not replace the existing V2 package and does not copy local generated archives.

## Claim Boundary

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- full native playback solved by this sidecar module: false
- final playback engine solved by this sidecar module: false
- custom component codec solved by this sidecar module: false
- proxy regions are semantic objects: false
- unsafe_acceptance_count: 0

This is a software metadata/diagnostic parity layer. It is not hardware proof, not a physical player claim, and not a final GUI/runtime claim.
