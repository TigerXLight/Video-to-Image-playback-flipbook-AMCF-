# AMCF Software I/O Release Review Refresh

## Purpose

`AMCF_SOFTWARE_IO_PUBLIC_DOCS_REFRESH_V1` records the public documentation refresh for the AMCF software I/O baseline.

It links the dossier, repo audit, shared models, fixture baseline, no-hardware printer/reader/player prototypes, cross-corridor roundtrip, mutation safety tests, and implementation progress.

## Checks Covered

- README entry point for software I/O docs
- software I/O docs map
- public summary
- no-hardware claim boundaries
- generated-output policy
- mutation safety visibility
- `unsafe_acceptance_count` remains 0

## Claim Boundary

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- generated output committed: no

## Not Claimed

This refresh does not claim hardware validation, physical Level 5 completion, manufactured player completion, real printer integration, real scanner/reader integration, real player communication, PDF/image/barcode support, or USB/serial/firmware support.

## Validation

Run:

```text
python -m unittest discover -s tests
```

Run the AMCF software I/O demos as needed from `demo/`.
