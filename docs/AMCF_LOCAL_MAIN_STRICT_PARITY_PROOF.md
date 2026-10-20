# AMCF Local Main Strict Parity Proof

## Purpose

This document records the strict parity proof process between the local working `Main` project and the public GitHub AMCF repo.

The goal is to prove what is the same, what is functionally equivalent, what is intentionally excluded from public Git, and what still needs packaging/dependency policy before a user-facing release.

This is not a hardware validation document.

## Scope

Local source of truth:

```text
<workspace-root>/Main
```

Public repo:

```text
<public-repo>
```

The proof checks:

- local `Main` file inventory
- public equivalents
- exact hash matches where files are expected to be identical
- public-safe ports of local `Main` scripts, config, dependency pins, and archive checks
- local proof-script output classes
- public equivalent output classes
- local/public output hashes and artifact sizes
- local/public elapsed runtime for the bounded proof run
- strict identity status
- generated-output policy
- claim-boundary flags

## Repeatable Command

Run from the public repo root:

```text
python demo/run_amcf_local_main_strict_parity_proof.py --frames 4
```

Output is written under:

```text
output/amcf_local_main_strict_parity_proof/
```

Generated proof reports are local evidence and should not be committed.
Large public-equivalent artifacts are created in a temporary directory, measured,
hashed, and removed so release-package tests do not treat them as committed
package material.

## What Counts As Same

The proof separates three different meanings of "same":

1. Functional parity: both projects produce the required AMCF output classes for
   the same input.
2. Performance parity: the bounded public run is measured against the bounded
   local run.
3. Strict identity: generated archives, deliverables, reconstructed videos, and
   timing are exactly identical.

The public repo is expected to preserve the same useful AMCF behavior in
public-safe form:

- MP4/source-video input path
- source-frame input path
- digital AMCF archive output
- decoded frame output
- decoded MP4/video output when FFmpeg is available
- component-event archive path
- WebP payload support when Pillow is available
- OpenCV segmentation / optical-flow support when available
- SSIM quality metrics when available
- viewer/deliverable package output
- CLI workflow entrypoint
- local `Main` Test02 component archive path
- local `Main` Test03A tracking diagnostic path
- local `Main` archive decode checker
- local `Main` config/dependency expectations
- portable public wrappers for local launcher abilities
- no hardware claim boundary violations

The proof must not turn functional parity into a byte-for-byte identity claim.
If strict identity is false, the report must say so.

## What Is Intentionally Not Copied

- local source media
- generated evidence folders
- generated zips
- caches and `__pycache__`
- virtual environments
- machine-specific absolute-path `.cmd` wrappers
- local absolute paths
- private workspace-only proof folders

Machine-specific wrappers are replaced by portable public wrappers under `cmd/`.

## Current Expected Result

The current public repo should pass functional output parity for a bounded local-source run.

It should not claim byte-for-byte identity with local `Main` unless the generated
hashes and exact timing checks also pass. At the time this proof layer was
added, the public repo uses clean public modules and schemas instead of
committing the monolithic local proof script and its generated artifacts.

## Claim Boundary

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- real printer required: false
- real reader required: false
- real player required: false
- real scanner required: false
- real USB required: false
- unsafe_acceptance_count: 0
