# AMCF Virtual Reader Recovery Export

The virtual reader/recovery path is a software-only simulation of how a future physical reader could recover AMCF state from indexed carrier sections.

## What it reads

The recovery module reads a software-generated physical carrier package:

- `physical_carrier_manifest.json`
- `carrier_sections/*.amcfsection.txt`
- lane metadata for timing/index, registration, payload, colour registry, metadata, and hash/checksum lanes

## What it validates

The reader checks section count, section index order, duplicate indices, section file hashes, required lane presence, and payload hash references.

Invalid or corrupted carrier data is rejected fail-closed. Missing section files, missing lanes, tampered section files, malformed manifests, and duplicate/out-of-order section indices do not silently pass.

## What it recovers

The demo recovers AMCF frame payload state and exports recovered PPM frame payloads plus `recovered_amcf_manifest.json`. It may also write a recovered `.amcf.zip` archive for software handoff.

## Relationship to future physical reader hardware

This module models the software contract a future physical reader/scanner would need to satisfy. It does not connect to real scanner hardware and does not perform actual physical scanning.

## Claim boundaries

- No real scanner is used.
- No physical proof is claimed.
- No hardware validation is claimed.
- No final UI is claimed.
- No manufacturing readiness is claimed.
- No MP4/video-container export is claimed by this path.
