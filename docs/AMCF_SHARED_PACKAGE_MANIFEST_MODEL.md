# AMCF Shared Package / Manifest Model Baseline

## Purpose

`AMCF_SHARED_PACKAGE_MANIFEST_MODEL_V1` creates the first shared, no-hardware software model foundation after the repo audit.

It defines reusable data objects for:

- AMCF package identity
- AMCF manifest identity
- AMCF update events
- AMCF physical sections
- required physical-section lanes
- claim-boundary flags
- deterministic validation report

## Scope Boundary

This phase does not implement:

- PC -> Printer layout
- PC <-> Reader recovery
- Player <-> PC runtime/session bridge
- GUI
- hardware APIs
- scanner/camera/USB/serial support
- PDF/image/barcode dependencies

## Claim Boundary

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- real printer required: false
- real reader required: false
- real player required: false
- real scanner required: false
- real USB required: false

## Model Objects

- `AMCFClaimBoundary`
- `AMCFUpdateEvent`
- `AMCFPhysicalSection`
- `AMCFManifest`
- `AMCFPackage`
- `AMCFPackageValidationReport`

## Validation Rules

The validator checks:

- supported model version
- section count matches section list
- section IDs are unique
- every section has a matching update event
- every section includes required lanes
- every section has a payload hash
- claim-boundary flags remain false

## Demo

Run:

```bash
python demo/run_amcf_shared_package_model_demo.py
```

Generated output is written under:

`output/amcf_shared_package_model/`

Generated output is not committed.
