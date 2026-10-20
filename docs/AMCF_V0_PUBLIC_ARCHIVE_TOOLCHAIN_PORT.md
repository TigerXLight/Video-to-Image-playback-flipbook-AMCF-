# AMCF v0 Public Archive Toolchain Port

This document records the public-port surface for the local AMCF v0 archive tooling found in the local workspace test history.

## Purpose

The port brings the AMCF-owned v0 archive builder, loader, shared safety helpers, and component-manifest toolchain checks into the public repo without copying generated archives, media payloads, local scratch folders, or machine-specific paths.

## Ported Surface

- `src/amcf_v0/common.py`
- `src/amcf_v0/builder.py`
- `src/amcf_v0/loader.py`
- `src/amcf_v0/toolchain.py`
- `demo/run_amcf_v0_public_archive_toolchain_demo.py`
- `tests/test_amcf_v0_public_archive_toolchain.py`

## Current Status

The public repo now includes the v0 archive safety and inspection code path for:

- unsafe archive-entry rejection
- source checksum inventory
- template source scaffolding
- safe archive extraction
- manifest/viewer/docs/media presence validation
- component stream manifest validation

The demo uses a synthetic no-hardware archive fixture and writes generated output under `output/amcf_v0_public_archive_toolchain_demo/`.

## Boundaries

- This is software archive tooling only.
- Generated output is not committed.
- No generated local media from the workspace is copied.
- No real printer, reader, scanner, USB, or player hardware is required.
- Hardware validation claimed: false
- Physical Level 5 claimed: false
- Manufactured player claimed: false
- `unsafe_acceptance_count`: 0

## Remaining Parity Work

This does not yet mean the whole local workspace is fully public-equivalent. Remaining local candidates still include older v0/v1 regression harnesses, selected-candidate decode scripts, archive writer/reader integration scripts, local viewer wrappers, and local package polish that need the same selective public-port treatment.

