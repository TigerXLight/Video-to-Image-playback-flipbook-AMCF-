# AMCF Workspace Tests Functionality Parity Inventory

This document records the next parity boundary after local `Main` parity.

The goal is code and feature parity, not byte-for-byte identity of generated archives, generated videos, timestamps, or machine-local wrapper files. The public repo must keep the newer software I/O, PC-reader, physical-player, and release-review work while also accounting for AMCF functionality that lived in the broader local workspace `Tests` tree.

This is not a hardware validation document.

## Current Position

The public repo now contains public-safe ports or equivalents for the local `Main` surface, including:

- MP4/source-video to AMCF archive pipeline
- source-frame to AMCF archive pipeline
- component-event archive support
- local `Main` Test02 component archive path
- local `Main` Test03A tracking diagnostic path
- local `Main` archive decode checker
- quality metrics and optional media hooks
- deliverable/viewer package output
- portable wrappers for local launcher abilities
- current software I/O and physical-player modules/docs/tests

That does not automatically prove the broader local `Tests` workspace is fully represented. The broader tree contains many historical experiments, generated reports, review packs, local wrappers, and research probes. Some of that code may be important and should be ported. Some of it is local-only evidence that should not be committed.

The first runnable/source inventory found:

- runnable/source files checked: 1,088
- core AMCF behaviour candidates: 131
- archive-tool candidates: 94
- local release-package candidates: 5
- local regression-proof candidates: 112
- viewer/review package candidates: 163
- optional deep-research or dataset-specific files: 277
- local machine-specific wrappers needing portable equivalents: 233

These counts mean full broad-workspace parity is not yet proven. They also show why the next step should be targeted porting of archive/component/decoder behaviour rather than a bulk copy.

## Inventory Script

Run from the public repo root:

```text
python demo/run_amcf_workspace_tests_functionality_inventory.py
```

The script writes generated inventory output under:

```text
output/amcf_workspace_tests_functionality_inventory/
```

Generated inventory output must not be committed.

## What The Inventory Checks

The inventory scans runnable/source-like files from the broader workspace `Tests` tree and compares them against the public repo by hash and filename. It intentionally focuses on code and command/config wrappers rather than Markdown narrative files, generated reports, local media, or output artifacts. It classifies files as:

- `PUBLIC_EXACT_MATCH`
- `PUBLIC_NAME_MATCH_REVIEW_REQUIRED`
- `CORE_ARCHIVE_TOOL_CANDIDATE`
- `CORE_AMCF_BEHAVIOUR_CANDIDATE`
- `LOCAL_RELEASE_PACKAGE_CANDIDATE`
- `LOCAL_REGRESSION_PROOF_CANDIDATE`
- `VIEWER_OR_REVIEW_PACKAGE_CANDIDATE`
- `OPTIONAL_DEEP_RESEARCH_OR_DATASET_SPECIFIC`
- `LOCAL_MACHINE_SPECIFIC_WRAPPER_NEEDS_PORTABLE_EQUIVALENT`
- `LOCAL_PATH_REVIEW_REQUIRED`
- `NEEDS_MANUAL_REVIEW`

## Why This Is Needed

The wider local workspace contains many more files than `Main`. A bulk copy would import local paths, generated artifacts, old review outputs, machine-specific wrappers, and dependency-heavy research branches. A file-by-file inventory lets the repo prove which code/features are already public, which are intentionally superseded, and which must still be ported.

## Claim Boundary

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- real printer integration claimed: false
- real scanner integration claimed: false
- real player hardware claimed: false
- unsafe_acceptance_count: 0

## Next Step

Review the generated inventory, then port the highest-priority `CORE_ARCHIVE_TOOL_CANDIDATE`, `CORE_AMCF_BEHAVIOUR_CANDIDATE`, and `LOCAL_RELEASE_PACKAGE_CANDIDATE` items that are not already represented by public modules.

Priority areas visible in the first scan include:

- AMCF v0 builder/loader/toolchain scripts
- archive writer/reader integration scripts
- AMCF v1 validation, manifest, inspect, decode-contract, and compare-metric tools
- residual encoder/decoder and native payload decoder experiments
- compositor and selected-candidate decode scripts
- local regression/acceptance harnesses that may need public equivalents
