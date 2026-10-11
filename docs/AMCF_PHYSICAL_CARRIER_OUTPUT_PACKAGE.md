# AMCF Physical Carrier Output Package

An AMCF physical carrier output package is a software-generated preparation artifact for a future indexed physical medium. It converts an AMCF digital archive into deterministic carrier section files and a manifest.

## Relationship to AMCF digital

The AMCF digital archive remains the canonical software object. The carrier package references the AMCF frame payloads, preserves payload hashes, and creates one indexed carrier section per source payload.

## Relationship to the future physical reader

A future physical reader/scanner could use the carrier lanes as recovery and validation targets:

- timing/index lane
- registration lane
- payload lane
- colour registry lane
- metadata lane
- hash/checksum lane

This package does not connect to a real reader, scanner, printer, or motorized transport.

## Relationship to the future mechanical/optical player

The carrier package uses vertical-stack / indexed-section physical-medium framing. A future mechanical/optical player could present indexed AMCF physical media through a view gate with illumination or projection.

The physical player is not a normal digital-screen player. The software carrier package prepares data for a possible physical viewing path; it does not replace the physical viewing act.

## Why indexed sections are used

Indexed sections preserve per-section registration, timing, and validation boundaries. That is better aligned with AMCF recovery and fail-closed validation than a default left-to-right flipbook assumption.

## What this is not

- Not physical proof.
- Not hardware validation.
- Not real printing.
- Not manufacturing readiness.
- Not a built physical prototype.
- Not a left-to-right flipbook default.
- Not a continuous ribbon default.

Physical manufacture and real material experiments remain optional future work.
