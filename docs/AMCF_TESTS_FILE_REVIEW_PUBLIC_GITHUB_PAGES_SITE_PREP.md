# AMCF Tests File Review: Public GitHub Pages Site Preparation

This record reviews the dated folder:

`<workspace-root>/Tests/Test AMCF_PUBLIC_GITHUB_PAGES_SITE_PREP/20261011_011430`

It covers the public-package handoff and static Pages preparation. It is not a
new runtime implementation and does not by itself prove parity with the whole
local workspace.

## Complete File Disposition

The folder contains 1,166 files. Every file was assigned to one of these
categories:

| Category | Count | Disposition |
| --- | ---: | --- |
| Public package source/docs/tests/site/assets | 355 | compared against current public repo |
| Package-generated demo output | 448 | generated evidence; do not commit as source |
| Package Python cache | 243 | cache; do not commit |
| Audit/status reports | 7 | read as handoff evidence |
| ZIP handoff artifacts | 5 | generated release artifacts; do not copy into source |
| Orchestration scripts | 2 | local run tooling; not runtime source |
| Other evidence/notes | 5 | read and classified as handoff evidence |
| **Total** | **1,166** | every file assigned |

The source count is the reusable package surface, not a count of generated
outputs. The current public repository was compared against that source
surface, excluding `.git`, `__pycache__`, `.pyc`, `output/`, and `demo/output/`.

## Public Package Parity

The package comparison covered all 355 source files at their relative paths:

| Result | Count |
| --- | ---: |
| Same path and SHA-256 | 355 |
| Same path but changed | 0 |
| Missing from current public repo | 0 |
| Unexpected public source extra within this package comparison | 0 |

Source-area counts were:

| Area | Files |
| --- | ---: |
| `src/` | 93 |
| `demo/` | 58 |
| `tests/` | 60 |
| `docs/` | 108 |
| `site/` | 5 |
| `assets/` | 11 |

This is an exact comparison of the Pages-prep package to the current public
checkout. It confirms that the public checkout did not silently lose files from
that package. It does not mean the package itself contains every later local
`Tests` experiment or every file in `Main`.

## Evidence Read

The handoff's input audit identifies the source package, its mixed-licence
notices, documentation, demos, tests, manifest, and concept assets. The
revalidation record reports passing compilation, demos, tests, site/workflow
presence, zero unsafe claims, zero local-path hits, no old test folders, no
cache/checkpoint/weight leakage, and `unsafe_acceptance_count: 0`.

The Pages enablement note correctly treats the site as documentation/context
only. The final status says the site/workflow and package validation passed,
feature work was not added by this run, and no Git operations were performed by
the source run.

The source runner was also read. It creates a static `site/` page and Pages
workflow, patches the README and release manifest, audits claims/hygiene, and
creates a ZIP for handoff. It does not add runtime hardware behavior or claim
physical proof.

## Generated And Local-Only Material

The 448 package-generated files are demo outputs such as generated frames,
carrier sections, manifests, validation logs, and sample archives. The 243
cache files are Python bytecode. The five ZIP artifacts are handoff archives.
None are source parity requirements, and none are to be committed into the
public repository.

The two root orchestration files are dated local-run tooling. They contain
workspace-specific source-package paths and are not needed by the public
runtime. The audit/status notes are evidence records, not runtime modules.

## Public Behavior And Claims

The package handoff preserves the tested public workflow available at that
stage: generated source frames to digital AMCF, software carrier preparation,
virtual reader recovery/export, and mechanical/optical simulator behavior.
Later public software I/O, diagnostic, archive, and physical-player additions
remain in the current repository and were not removed by this comparison.

The Pages material does not claim:

- real printer, scanner, camera, USB, serial, motor, sensor, or cartridge use;
- manufactured hardware or physical Level 5 completion;
- real optical playback or physical validation;
- a final GUI, EXE, or production user-facing application.

## Status

`PUBLIC_PACKAGE_EXACTLY_PRESENT_IN_CURRENT_CHECKOUT`.

This closes the Pages-prep package handoff folder at file level. Continue with
the next newest public-asset and pre-public-context folders, then the older
diagnostic and accepted implementation groups. Do not interpret this exact
package result as 100% parity with all local project files.

Claim boundary: hardware validation false; physical Level 5 false;
manufactured player false; generated output committed no.
