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
- local proof-script output classes
- public equivalent output classes
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

Generated proof output is local evidence and should not be committed.

## What Counts As Same

The public repo is not required to be a byte-for-byte copy of local `Main`.

It is required to preserve the same useful AMCF behavior in public-safe form:

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
- no hardware claim boundary violations

## What Is Intentionally Not Copied

- local source media
- generated evidence folders
- generated zips
- caches and `__pycache__`
- virtual environments
- machine-specific `.cmd` wrappers
- local absolute paths
- private workspace-only proof folders

## Current Expected Result

The current public repo should pass functional output parity for a bounded local-source run.

It should not claim byte-for-byte identity with local `Main`, because the public repo uses clean public modules and schemas instead of committing the monolithic local proof script and its generated artifacts.

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
