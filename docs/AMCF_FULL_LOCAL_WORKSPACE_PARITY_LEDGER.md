# AMCF Full Local Workspace Parity Ledger

This document records the plan for turning the complete local AMCF workspace inventory into a useful parity ledger.

It does not claim the public GitHub repo is already 100 percent equivalent to every historical local test folder. It creates the controlled process for proving and closing that gap.

## Scope

The local workspace includes `Main`, `Tests`, local generated outputs, historical experiments, media assets, prototype archives, third-party/reference research folders, command wrappers, and the public GitHub package.

The generated hierarchy address list index is written to:

`output/amcf_full_workspace_parity_ledger/local_workspace_file_hierarchy_address_list.txt`

The complete list is split into smaller `.txt` part files in the same folder so release-package checks do not treat the hierarchy as a huge generated artifact. These files are generated output and are not committed.

## Classification Values

- `INSPECT_PRIORITY`: AMCF-owned code or runnable script candidate that should be reviewed for parity.
- `LEDGER_REVIEW`: AMCF documentation or metadata that may describe behavior, formats, gates, or reports.
- `GENERATED_DO_NOT_COPY`: archive/output/scratch artifact that should not be copied directly into the public repo.
- `REFERENCE_OR_DEPENDENCY_REVIEW`: third-party, model, or research dependency surface that should be wrapped or documented rather than bulk-copied.
- `ASSET_REVIEW`: media/sample asset that may be useful for tests or documentation but should not be copied blindly.
- `DO_NOT_COPY`: cache, dependency, build, or transient folder content.
- `LOW_PRIORITY_REVIEW`: non-AMCF or non-source file.

## Parity Ledger Status Values

Every useful local candidate should eventually be marked as one of:

- `PORTED`
- `ALREADY_PUBLIC`
- `GENERATED_DO_NOT_COPY`
- `THIRD_PARTY_REFERENCE`
- `SUPERSEDED`
- `NEEDS_MANUAL_REVIEW`

## Current Useful Inspection Areas

The first useful groups to inspect are:

- AMCF v0/v1 builder, loader, archive writer, archive reader, and validation tools.
- AMCF component-stream and selected-candidate decode scripts.
- AMCF reconstruction, compositor, and quality gate scripts.
- AMCF viewer/review package scripts that are not only generated HTML.
- AMCF regression and acceptance harnesses that encode behavior not yet represented in public tests.
- Local command wrappers that need portable public equivalents, not machine-local paths.
- Package/deliverable polish that is source behavior rather than generated output.

## Boundaries

- Do not bulk-copy generated outputs.
- Do not commit local media unless a small fixture is explicitly justified.
- Do not copy cache folders or virtual environments.
- Do not copy third-party repositories as AMCF source.
- Do not add hardware APIs, GUI, EXE packaging, printer/scanner/camera/USB/serial support as part of this ledger step.
- Generated output remains under `output/`.

Claim-boundary values:

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- `unsafe_acceptance_count`: 0

## How To Regenerate

Run:

```bash
python demo/run_amcf_full_workspace_parity_ledger.py
```

Then inspect the generated hierarchy address list and ledger summary under:

`output/amcf_full_workspace_parity_ledger/`

