# AMCF Release Candidate Acceptance Parity

This document records the public-safe summary of the local release-candidate acceptance and signoff band.

It does not copy local generated ZIPs, local package folders, generated media, caches, private paths, or old run output. It records the behavior and acceptance facts that should remain visible in the public repo.

## What Was Ported

- runtime and validator readiness facts
- canonical valid/invalid vector contract
- acceptance harness result contract
- viewer/runtime handoff readiness facts
- archive writer/reader readiness facts
- release-candidate package and signoff facts
- claim-boundary flags and unsafe-acceptance accounting

The reusable public module is `src/amcf_release_candidate_acceptance.py`.

## Acceptance Facts

| Item | Public summary |
| --- | --- |
| valid vectors passed | 9 |
| invalid vectors rejected | 9 |
| tiny archive fixtures | 6 |
| claim-boundary tests | passed |
| acceptance badge | AMCF_ACCEPTANCE: PASS |
| local generated release ZIP copied | no |

## Public Coverage

The archive writer/reader behavior is represented by `src/amcf_archive_writer_reader.py`, its demo, and tests. The Main-facing vnext surface is represented by `src/amcf_vnext.py`. This parity layer adds the release acceptance timeline and signoff facts around those public modules.

## Claim Boundary

- unsafe_acceptance_count: 0
- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- real printer integration claimed: false
- real scanner integration claimed: false
- real player hardware claimed: false
- semantic Level 5 claimed by this release package: false

Generated reports go under `output/amcf_release_candidate_acceptance/` and must not be committed.
