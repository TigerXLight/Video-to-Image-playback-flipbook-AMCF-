# AMCF Tests File Review: Physical Analog Player Context Packages

This record covers the two physical-player concept folders immediately before
the early pre-GitHub functional coverage audit:

- `Test AMCF_PHYSICAL_ANALOG_PLAYER_CONCEPT_PART1_ARCHITECTURE_CORRECTION/20261010_190646`
- `Test AMCF_PHYSICAL_ANALOG_PLAYER_CONCEPT_PART2_CLEAN_PACKAGE_DOCS/20261010_191435`

These folders correct public wording and package context. They are not claims
of a built physical device.

## Complete File Disposition

| Folder | Total | Package source | Evidence/other | Orchestration | ZIP |
| --- | ---: | ---: | ---: | ---: | ---: |
| Part 1 architecture correction | 15 | 0 | 13 | 2 | 0 |
| Part 2 clean-package docs | 49 | 26 | 20 | 2 | 1 |
| **Combined** | **64** | **26** | **33** | **4** | **1** |

All 64 files were accounted for. Part 1 is planning/evidence only. Part 2's
26 reusable package files were compared with the current public checkout after
excluding generated output and caches.

## Part 1: Architecture Correction

Part 1 produced and documented the corrected distinction between:

- the software player and UI state viewer;
- the physical reader/scanner recovery path;
- the future mechanical/optical physical player;
- a possible hybrid reader-player appliance.

It explicitly rejected treating the physical player as a normal tablet,
monitor, digital-screen viewer, left-to-right flipbook, or manual-crank-first
device. It also supplied the Part 2 documentation patch plan and did not modify
Main or the clean package.

The 13 non-orchestration files are correction maps, notes, JSON records, and
the Part 2 prompt. They are `GENERATED_EVIDENCE_NOT_SOURCE`; the two runner
files are `LOCAL_MACHINE_SPECIFIC_DO_NOT_COPY`.

## Part 2: Clean-Package Documentation

The 26 reusable package files were compared to the current public checkout:

| Result | Count |
| --- | ---: |
| Exact SHA-256 match | 17 |
| Changed but present as newer public equivalents | 9 |
| Missing from current public checkout | 0 |

The nine changed files are the README, claim/release metadata, canonical and
physical-player docs, and current digital/physical-player source/test files.
They remain changed because the public checkout includes later software I/O,
diagnostic, physical-player, and release-review work. No package source file
from Part 2 was lost.

The Part 2 evidence says the copied package was patched with the corrected
mechanical/optical physical-player definition, physical reader/player boundary
docs, visual-reference note, optional adapter guidance, and release manifest.
Its validation passed compilation, demos, tests, claim scans, local-path scans,
and generated-output exclusion with `unsafe_acceptance_count: 0`.

## Progression Finding

The concept correction was integrated into the public documentation sequence,
then extended by the later physical-player simulator/state-machine and public
release reviews. The older package wording must not replace the newer public
docs; the newer files are the correct supersets for the current branch.

The source records explicitly keep the physical implementation future-facing:
no real motors, sensors, cartridges, optics, printing, scanning, hardware
validation, physical Level 5, manufacturing, or prototype completion is
claimed.

## Status

`PUBLIC_CONTEXT_CORRECTION_PRESENT_AND_SUPERSEDED_BY_NEWER_PUBLIC_DOCS`.

This closes all 64 files in both concept-context folders. Continue downward to
the older clean-package preparation, release-readiness, virtual-reader, and
diagnostic groups. This record does not close the full local workspace or prove
100% parity.

Claim boundary: hardware validation false; physical Level 5 false;
manufactured player false; generated output committed no.
