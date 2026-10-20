# AMCF Tests Non-Python Artifact Parity Inventory

## Purpose

This inventory closes the non-Python artifact boundary for the local `Tests`
workspace. It uses an actual recursive file inventory rather than treating
filenames as source code. The result distinguishes maintained source/control
files from generated reports, media, archives, model data, and local evidence.

It does not claim that generated local artifacts should be copied to GitHub,
and it does not claim hardware validation, physical Level 5, or a manufactured
player.

## Measured Workspace

The recursive inventory found:

- `142,150` files;
- approximately `28,239,612,688` bytes;
- `1,155` Python source files;
- `490` Python bytecode files;
- `310` Windows command launchers;
- `379` public tracked files in the current public checkout after the parity
  and packaging updates.

The Python source files were already compared by hash/basename in
`docs/AMCF_TESTS_SOURCE_FILE_HASH_RECONCILIATION.md`. This document covers the
remaining non-Python artifact classes.

## Extension Inventory

The largest measured classes were:

| Extension | Count | Approximate bytes | Disposition |
| --- | ---: | ---: | --- |
| `.json` | 47,572 | 667 MB | mostly generated manifests/reports; inspect only accepted fixtures/configs |
| `.md` | 22,948 | 12.6 MB | mostly generated run reports; retain normalized decisions in public docs |
| `.png` | 28,660 | 1.95 GB | generated previews/contact sheets/masks; do not bulk-copy |
| `.jpg` | 26,823 | 1.12 GB | generated evidence/contact sheets/media; do not bulk-copy |
| `.mp4` | 1,161 | 10.27 GB | generated source/reconstruction/proof media; do not bulk-copy |
| `.zip` | 423 | 10.81 GB | transfer/release/generated archives; do not bulk-copy |
| `.csv` | 7,546 | 289 MB | generated metrics/benchmark tables; port accepted schema only |
| `.py` | 1,155 | 11.5 MB | source and runners; covered by source-hash reconciliation and group reviews |
| `.cmd` | 310 | 82 KB | local runners/wrappers; retain only portable accepted commands |
| `.webp` | 1,751 | 201 MB | generated payload/evidence media; public code handles payload format |
| `.bin`, `.pt`, `.pth` | 23 | about 2.2 GB | model/checkpoint/binary data; third-party or local evidence, not public source |

Other classes include `.m4a`, `.mkv`, `.avi`, `.ppm`, `.svg`, `.html`, `.js`,
`.jsonl`, `.zlib`, `.zlib_i16_bgr`, `.idx`, `.pack`, `.rev`, `.sample`, and
environment/control files. Their presence is consistent with generated media,
archive experiments, viewer bundles, compression experiments, and local
toolchain evidence.

## Accepted Non-Python Surface

The accepted public non-Python surface is represented by curated files and
tests, not by copying every run output:

- AMCF manifests, sidecars, checksums, and invalid-archive fixtures in the
  public archive writer/reader and V2 package tests;
- source-frame manifests and deterministic fixture JSON used by public demos;
- public Markdown docs and claim-boundary records;
- static viewer HTML/JavaScript that is intentionally a report/viewer package,
  not a final desktop GUI;
- public `pyproject.toml`, `requirements.txt`, release metadata, and Pages
  workflow files;
- bounded physical-medium and physical-player reports with
  `unsafe_acceptance_count: 0`.

## Artifact Classes Intentionally Not Copied

- generated images, videos, contact sheets, masks, overlays, and audio;
- dated run folders and benchmark output;
- generated ZIP/release packages and caches;
- virtual environments and Python bytecode;
- model checkpoints and downloaded media;
- copied third-party repositories and their build artifacts;
- legacy/rejected experiment outputs whose accepted behavior is superseded by
  later public modules;
- private workspace paths and machine-specific launchers.

## Completeness Interpretation

The entire non-Python inventory has been counted and classified at artifact
class level. A generated artifact is not a missing application feature merely
because it is absent from GitHub. A future artifact promotion requires all of:

1. an accepted behavior or user-facing contract;
2. a source/config schema that can be reproduced without private paths;
3. a public test or deterministic fixture;
4. license/provenance clearance where external material is involved; and
5. a generated-output policy that keeps bulk evidence out of source control.

The current public checkout satisfies this rule for the accepted digital AMCF,
diagnostic, software-I/O, physical-player simulation, release, and CLI paths.
It does not claim byte-for-byte identity with every local generated artifact.

## Status

- non-Python `Tests` artifact inventory completed: yes;
- generated output committed: no;
- public source/docs/test parity boundary documented: yes;
- `unsafe_acceptance_count`: `0` in reviewed public paths;
- hardware validation claimed: `false`;
- physical Level 5 claimed: `false`;
- manufactured player claimed: `false`.
