# AMCF Archive Writer Reader Parity Port

Run name: `AMCF_ARCHIVE_WRITER_READER_PARITY_PORT_V1`

Source priority group: `Tests/Test AMCF_ARCHIVE_WRITER_READER_INTEGRATION`

Public files:

- `src/amcf_archive_writer_reader.py`
- `demo/run_amcf_archive_writer_reader_demo.py`
- `tests/test_amcf_archive_writer_reader.py`

Generated output folder:

- `output/amcf_archive_writer_reader_demo/`

## Purpose

This port brings the useful local archive writer/reader integration behavior into the public repo as a clean, reusable, standard-library-only layer.

The local priority group contained a writer script, a reader script, and a larger workspace-specific integration harness. The public port keeps the core behavior and leaves behind the hardcoded local run paths, generated archives, historical logs, and local machine wrappers.

## What Is Implemented

The public module can:

- create small `.amcfvnext.zip` fixture archives
- write `manifest.json`
- write `claim_boundaries.json`
- write component and semantic sidecars
- write payload, mask, and polygon fixture members
- write checksums for present archive members
- inspect archive structure
- list archive files
- read manifest, sidecar, and claim-boundary JSON
- list frames, components, and semantic objects
- verify checksums
- extract summary data
- run fail-closed validation

The demo creates valid and intentionally invalid archives:

- `minimal_valid`
- `component_demo`
- `semantic_parked_reference`
- `invalid_fake_level5`
- `invalid_missing_payload`
- `invalid_fake_user_approval`

## Fail-Closed Rules

The reader rejects:

- missing archives
- non-zip archives
- missing required archive members
- missing payload entries
- checksum target mismatches
- checksum digest mismatches
- Level 5 claims without checklist pass
- fake user approval where the reviewer source is machine-generated
- sidecar references to missing payload, mask, polygon, or source-frame paths

`unsafe_acceptance_count` remains `0`.

## Claim Boundaries

This parity port does not claim:

- real hardware validation
- physical Level 5 completion
- manufactured player completion
- semantic Level 5 proof
- real scanner integration
- real printer integration
- real player hardware integration

Claim-boundary flags are false in the generated report.

## What Was Not Copied

The local integration harness was not copied wholesale because it contains local workspace paths and references to historical run folders. Generated archives and reports from the local `Tests/` workspace were not committed.

The public repo now has the archive writer/reader behavior as source, tests, and a demo that writes only under `output/`.

## Validation

Run:

```text
python -m unittest discover -s tests
python demo/run_amcf_archive_writer_reader_demo.py
```

Generated output is local demo output and should not be committed.
