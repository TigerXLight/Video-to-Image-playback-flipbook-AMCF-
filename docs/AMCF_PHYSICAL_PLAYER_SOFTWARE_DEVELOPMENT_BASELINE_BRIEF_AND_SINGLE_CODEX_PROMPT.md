# AMCF Physical Player Software Development Baseline Brief and Single Codex Prompt

This file consolidates the physical-player software/control planning, public review, closeout, and tag-prep sequence into one baseline reference.

Recommended repo destination:

```text
docs/AMCF_PHYSICAL_PLAYER_SOFTWARE_DEVELOPMENT_BASELINE_BRIEF.md
```

The single Codex prompt near the end references this file so future software development can proceed from one consolidated baseline instead of many separate prompts.

---

# 1. Release Tag Decision

The release tag is useful because it marks the clean public checkpoint before deeper software development begins.

Suggested tag:

```text
amcf-physical-player-software-control-v1
```

Meaning:

```text
Public release checkpoint for the AMCF physical-player software/control foundation.
```

It covers:

```text
- physical-player state machine
- fail-closed safety
- reverse/seek controls
- mechanism profiles
- integrated simulator demo
- public docs/site/package/release review
- closeout handoff
- tag-prep release materials
- claim boundaries preserved
```

It does not mean:

```text
- manufactured hardware exists
- real motors were validated
- real sensors were validated
- real cartridges were validated
- physical optical playback was proven
- no-gap physical switching was proven
- physical reverse hardware was proven
- arbitrary physical seek was proven
- physical Level 5 is complete
```

Tag command:

```cmd
git tag -a amcf-physical-player-software-control-v1 -m "AMCF physical-player software-control public release v1" && git push origin amcf-physical-player-software-control-v1
```

---

# 2. Current Pushed Baseline

Current pushed commit after tag-prep:

```text
e7e13155db3441887c5982cb0dfa9bd91383390a
```

Completed run:

```text
AMCF_PUBLIC_RELEASE_TAG_PREP_V1
```

Known validation from that run:

```text
- py_compile: PASS
- unittest discover: PASS, 294 tests
- integrated simulator demo: PASS
- release review: PASS
- package refresh: PASS
- final Pages review: PASS
- closeout handoff: PASS
- tag prep final_passed: yes
- tag created: no
- generated output committed: no
- local path leak found: no
- unsafe hardware claim found: no
- unsafe_acceptance_count: 0
- physical hardware claimed: no
- hardware validation claimed: no
- physical Level 5 claimed: no
- real sensors/motors/cartridges/scans required: no
- manufactured physical player claimed: no
```

Recommended development branch after tagging:

```cmd
git checkout -b dev/physical-player-runtime-integration
```

---

# 3. Completed Commit Trail

Stage 1 model-foundation was not a separate pushed commit in this sequence. Early model structures were folded into the state-machine run.

```text
Stage 2 — AMCF_PHYSICAL_PLAYER_STATE_MACHINE_V1
Commit: f8b6e91e1dfd9b57345ee38ac262635d446f47c8
Purpose: software/control state-machine foundation.

Stage 3 — AMCF_PHYSICAL_PLAYER_FAIL_CLOSED_V1
Commit: 4716c3b3df25b63f39b2d1430bdccfbc2f0bfb0e
Purpose: fail-closed safety decisions, reason catalogue, failure hooks, unsafe-acceptance audit.

Stage 4 — AMCF_PHYSICAL_PLAYER_REVERSE_SEEK_V1
Commit: 802042b5395ac860c437188e0d79031d7dd5f591
Purpose: limited reverse buffer, local-buffer seek, arbitrary seek denial, reverse/seek reports.

Stage 5 — AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES_V1
Commit: 01093024f9bbd11d10615a0f526b4440e5f8f41b
Purpose: mechanism profile model, folded A/B motor/encoder default, research/support profiles.

Stage 6 — AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO_V1
Commit: fea00409262dea39d5c9068daac0a206c02d07f5
Purpose: integrated simulator demo covering profiles, forward playback, fail-closed, reverse/seek, unsafe audit.

Stage 7 — AMCF_PHYSICAL_PLAYER_PUBLIC_DOCS_SYNC_V1
Commit: c7c2658877f04d40b94b127c6e44fe30d3597a18
Purpose: public docs map, public summary, README/site/claim-boundary sync.

Stage 8 — AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW_V1
Commit: 659bd3e74a9e4dd254600558aec6e76309ba596f
Purpose: release review script, docs-link scan, claim-boundary scan, generated-output scan, local-path scan.

Stage 9 — AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH_V1
Commit: 8f76d7528e4f6399ef719a99f15e1b248ce8e2ff
Purpose: package refresh script, package inventory, package-refresh docs/tests.

Stage 10 — AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW_V1
Commit: 8082f0a1134ea33df330c0508f06cc3ff7130e59
Purpose: final GitHub Pages/public docs review, README/docs map/site link sync.

Stage 11 — AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF_V1
Commit: 331848fdf10ff18eab0a9426441f0f00e91a8f03
Purpose: final closeout handoff, commit trail, docs/site/package/review state.

Stage 12 — AMCF_PUBLIC_RELEASE_TAG_PREP_V1
Commit: e7e13155db3441887c5982cb0dfa9bd91383390a
Purpose: tag prep script, release notes draft, tag checklist, suggested tag, no tag created.
```

---

# 4. Core Physical-Player Software/Control Baseline

The physical-player branch is a software/control foundation for a future mechanical/optical AMCF player.

Preferred concept:

```text
compact tablet-like mechanical/optical AMCF player
+ side/top cartridge
+ folded indexed carrier path
+ reader-prefetch lane
+ hidden staging gate
+ visible view gate
+ shutter/illumination blanking
+ folded optical viewing path
+ limited reverse/park buffer
+ fail-closed safety
```

Preferred simulator default:

```text
mechanism profile: folded_ab_motor_encoder_baseline
carrier_layout: folded_indexed_carrier
staging_model: abstract_ab_staging
actuator_family: motor_encoder
gate_model: single_visible_gate_plus_hidden_staging
prefetch_model: reader_prefetch_ahead
reverse_model: limited_reverse_buffer
seek_model: local_buffer_seek_only
safety_model: fail_closed_required
```

Dynamic AMCF physical rule:

```text
The physical player should not advance one page for every fixed video frame.
It should advance according to AMCF update events.
```

Core runtime flow:

```text
current section visible
→ next section prefetched
→ next section verified
→ next section staged
→ transition blanking
→ visible switch
→ old section parked
→ reverse/seek limited to safe local buffers
→ fail-closed blocks unsafe states
→ unsafe_acceptance_count remains zero
```

---

# 5. Software Development Should Start Now

The review/documentation/public-package sequence is complete enough. The next useful development phase should be real runtime integration.

Recommended next run:

```text
AMCF_PHYSICAL_PLAYER_RUNTIME_INTEGRATION_V1
```

Purpose:

```text
Connect the physical-player simulator to real AMCF package/manifest data instead of only deterministic sample/demo data.
```

This begins software development because it moves from controlled sample data to actual AMCF package structures.

Development should not start with hardware. It should start with software runtime integration:

```text
1. identify real AMCF package/manifest files already produced by the repo
2. define an adapter from AMCF manifest/update-event data to physical-player section records
3. map AMCF visual update events to physical section timing
4. run the existing physical-player state machine on real AMCF package input
5. generate playback, fail-closed, reverse/seek, unsafe-acceptance, and mechanism-profile reports
6. preserve all claim boundaries
7. keep hardware proof explicitly out of scope
```

---

# 6. Development Rules Going Forward

Always preserve:

```text
- software/control framing
- fail-closed safety
- unsafe_acceptance_count == 0
- local-buffer-only seek unless later explicitly expanded
- no arbitrary physical seek claim
- no real hardware validation claim
- no physical Level 5 completion claim
- no local Windows paths in public docs
- no generated output committed
- all public review scripts remain passing
```

Do not claim:

```text
- manufactured hardware
- real motors
- real sensors
- real cartridge validation
- real optical playback proof
- real no-gap physical switching proof
- physical reverse hardware
- arbitrary physical seek hardware
- physical Level 5 completion
- hardware validation
```

Can claim if implemented and tested:

```text
- AMCF package manifest adapter
- real package metadata parsing
- update-event to section-timing mapping
- physical-player state-machine run against real AMCF package input
- report generation from real package input
- deterministic public demo using fixture package data
- preserved fail-closed behaviour
- preserved unsafe_acceptance_count == 0
```

---

# 7. Single Codex Prompt for the Next Development Phase

Copy this prompt into Codex after:

1. the release tag is created and pushed, and
2. this file is saved in the repo at:

```text
docs/AMCF_PHYSICAL_PLAYER_SOFTWARE_DEVELOPMENT_BASELINE_BRIEF.md
```

---

```text
You are working on my AMCF project.

Run name:
AMCF_PHYSICAL_PLAYER_RUNTIME_INTEGRATION_V1

Public repo:
https://github.com/TigerXLight/Video-to-Image-playback-flipbook-AMCF-

Local workspace:
T:\References\to go\Media\tools\Video to Image

If Codex is already inside the repo root, use the current repo root.

================================================================================
MANDATORY BASELINE FILE
================================================================================

Before making changes, read this file:

docs/AMCF_PHYSICAL_PLAYER_SOFTWARE_DEVELOPMENT_BASELINE_BRIEF.md

Treat it as the baseline dossier for the physical-player software/control sequence.

Use it to avoid needing many separate Codex messages.

================================================================================
CURRENT BASELINE
================================================================================

Expected latest commit before branching:

e7e13155db3441887c5982cb0dfa9bd91383390a

Expected optional tag:

amcf-physical-player-software-control-v1

If the tag exists, report it.
If the tag does not exist, do not create it unless explicitly instructed.
Continue the runtime-integration work either way, but clearly report tag status.

This run begins the next software-development phase.
Do not add more review-only layers unless needed for runtime integration.

================================================================================
CORE PURPOSE
================================================================================

Implement the first real software-development bridge between actual AMCF package/manifest data and the physical-player software/control simulator.

This means:

- discover existing AMCF package/manifest structures in the repo
- define a stable adapter from AMCF package/manifest data to physical-player section records
- map AMCF update events to physical-player section timing
- run the existing physical-player state machine against real or fixture AMCF package input
- generate deterministic playback/safety/reverse/seek reports from package-derived sections
- keep claim boundaries intact

This is still software/control integration.
It is not hardware validation.

================================================================================
CORRECT FRAMING
================================================================================

AMCF is software-first.

The physical-player branch now has:

- state machine
- fail-closed safety
- reverse/seek controls
- mechanism profiles
- integrated simulator demo
- release review
- package inventory
- final Pages review
- closeout handoff
- tag-prep docs

Now development should connect that foundation to real AMCF package data.

Correct framing:

The hardware is not present yet, but the software can now map AMCF packages into the physical-player control model that future hardware must obey.

Do not claim:

- manufactured hardware
- real motors
- real sensors
- real cartridge validation
- real optical playback proof
- real no-gap physical switching proof
- real reverse hardware
- arbitrary physical seek hardware
- physical Level 5 completion
- hardware validation

Do claim if implemented and tested:

- AMCF package adapter
- manifest parsing
- update-event mapping
- package-derived physical sections
- runtime state-machine execution from package input
- package-derived reports
- preserved fail-closed safety
- preserved unsafe_acceptance_count == 0

================================================================================
FILES TO INSPECT FIRST
================================================================================

Read first:

README.md
CLAIM_BOUNDARIES.md
docs/AMCF_PHYSICAL_PLAYER_SOFTWARE_DEVELOPMENT_BASELINE_BRIEF.md

Then inspect the physical-player docs, source modules, demos, and tests.

Also inspect existing AMCF package/manifest/export modules and demos.
Search the repo for likely manifest/package terms:

- manifest
- package
- AMCF
- export
- playback
- frame
- update
- update event
- timing
- component
- section
- metadata
- hash
- checksum

Do not assume the package format before inspecting the repo.

================================================================================
DO NOT DO
================================================================================

Do not install packages.
Do not download anything.
Do not use real hardware APIs.
Do not add USB/HID/WinUSB/libusb code.
Do not add WIA/TWAIN/SANE scanner code.
Do not add printer-driver code.
Do not generate images.
Do not push.
Do not create or move Git tags.
Do not modify unrelated files.
Do not weaken claim boundaries.
Do not remove existing review/package/public scripts.
Do not commit generated output folders.
Do not commit generated ZIPs.
Do not claim hardware validation.

================================================================================
00 — INPUT AUDIT
================================================================================

Create:

docs/AMCF_PHYSICAL_PLAYER_RUNTIME_INTEGRATION_AUDIT.md

Include:

- current git HEAD
- current branch
- whether tag amcf-physical-player-software-control-v1 exists
- whether baseline brief file exists
- physical-player source files found
- AMCF package/manifest files/modules found
- package format assumptions discovered
- runtime integration gaps found
- files to edit
- files to create
- confirmation this is software/runtime integration only
- confirmation no physical hardware validation is claimed

================================================================================
01 — PACKAGE / MANIFEST DISCOVERY
================================================================================

Add a small discovery helper or script if useful:

demo/run_physical_player_runtime_manifest_discovery.py

It should inspect repo-local fixture/sample/package files and existing modules.

It should write output under:

output/physical_player_runtime_integration/

Suggested output files:

- manifest_discovery_report.json
- manifest_discovery_summary.md

Do not commit generated output.

If no real package fixture exists, create a small deterministic fixture under tests/fixtures/ or docs/examples/ only if consistent with repo style.

Prefer:

tests/fixtures/amcf_runtime_package_fixture.json

if no fixture convention exists.

The fixture should be tiny and claim-safe.

================================================================================
02 — RUNTIME ADAPTER MODULE
================================================================================

Create:

src/amcf_physical_player_runtime_adapter.py

Purpose:

Convert AMCF package/manifest/update-event data into physical-player section records that can be consumed by the existing state machine.

Use standard library only.

Expose functions such as:

- load_amcf_manifest(path)
- normalize_amcf_manifest(manifest)
- extract_update_events(manifest)
- build_physical_player_sections_from_manifest(manifest)
- build_runtime_cartridge_from_manifest(manifest)
- build_runtime_integration_report(manifest, sections, machine_result)

Do not overfit to unknown data.
Use defensive parsing.
Preserve unknown fields under metadata/notes where useful.

================================================================================
03 — SECTION MAPPING
================================================================================

The adapter should map update events to physical-player section-like records.

Each mapped section should include at least:

- section_id
- section_index
- timestamp_start_ms
- dwell_ms or duration_ms
- event_id if present
- source_manifest_id if present
- source_update_id if present
- content_hash or stable synthetic hash
- expected_hash_status
- registration_status
- marker_status
- colour_status
- metadata

If the existing state machine requires a specific object type, adapt into that type.

Do not weaken verification.
Do not mark unknown unsafe fields as valid without a deterministic reason.

================================================================================
04 — RUNTIME STATE MACHINE EXECUTION
================================================================================

Create a demo:

demo/run_physical_player_runtime_integration_demo.py

It should:

1. load a deterministic AMCF runtime manifest fixture or discovered sample
2. map it to physical-player sections
3. build a runtime cartridge/state-machine input
4. run nominal forward playback over package-derived sections
5. run fail-closed checks against at least one invalid package-derived or mutated section
6. run bounded reverse/seek where possible
7. run unsafe acceptance audit
8. write reports

Output folder:

output/physical_player_runtime_integration/

Output files:

- runtime_manifest_normalized.json
- runtime_physical_sections.json
- runtime_playback_timeline.json
- runtime_fail_closed_report.json
- runtime_reverse_seek_report.json
- runtime_unsafe_acceptance_audit.json
- runtime_integration_report.json
- RUNTIME_INTEGRATION_SUMMARY.md

Generated output should not be committed.

================================================================================
05 — DOCS
================================================================================

Create:

docs/AMCF_PHYSICAL_PLAYER_RUNTIME_INTEGRATION.md

Include:

- purpose
- baseline tag/commit
- relationship to the baseline brief
- package/manifest discovery
- adapter design
- update-event to section mapping
- runtime state-machine execution
- fail-closed integration
- reverse/seek integration
- unsafe acceptance audit
- output files
- what is not claimed
- how to run the demo

Update:

docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md

Add the new runtime integration stage after tag prep.

Claim boundary:

- software/runtime integration only
- no physical hardware validation
- no physical Level 5 claim
- no manufactured physical player claim

Update docs map / README only if appropriate and concise.

================================================================================
06 — TESTS
================================================================================

Create:

tests/test_physical_player_runtime_integration.py

Tests should verify:

1. baseline brief file exists
2. runtime adapter module imports
3. deterministic fixture manifest loads
4. manifest normalizes deterministically
5. update events extract in stable order
6. physical sections are built from manifest
7. section IDs are stable
8. section indexes are sequential
9. timestamp_start_ms values are stable
10. section hash/status fields exist
11. missing required fields fail safely
12. runtime cartridge can be built
13. runtime integration demo/report can build a report dict
14. runtime playback has at least one transition
15. fail-closed path still records an event for invalid/mutated section
16. reverse/seek remains bounded
17. unsafe_acceptance_count remains 0
18. hardware_validation_claimed false
19. physical_level_5_claimed false
20. manufactured_player_claimed false
21. generated output is not required for tests
22. full unittest suite passes

Use unittest and standard library.

If tests are ignored by .gitignore, force-add only this intended test file.

================================================================================
07 — VALIDATION COMMANDS
================================================================================

Run from repo root:

python -m py_compile src/amcf_physical_player_runtime_adapter.py
python -m py_compile demo/run_physical_player_runtime_manifest_discovery.py
python -m py_compile demo/run_physical_player_runtime_integration_demo.py
python -m py_compile demo/run_physical_player_simulator_demo.py
python -m unittest discover -s tests
python demo/run_physical_player_runtime_manifest_discovery.py
python demo/run_physical_player_runtime_integration_demo.py
python demo/run_physical_player_simulator_demo.py
python demo/run_public_release_tag_prep.py

Also run the existing public review scripts if practical:

python demo/run_physical_player_release_review.py
python demo/run_public_release_package_refresh.py
python demo/run_public_github_pages_final_review.py
python demo/run_public_release_closeout_handoff.py

If Windows Store python.exe fails, use the same local Codex runtime Python used in previous successful runs, but report the exact command.

Also run:

git status --short
git diff --stat

Do not push.

================================================================================
08 — COMMIT
================================================================================

If all tests pass and only intended files changed, commit with:

git add README.md docs src demo tests

If tests are ignored by .gitignore, force-add only:

git add -f tests/test_physical_player_runtime_integration.py

If you added a fixture under tests/fixtures/ and it is ignored, force-add only that fixture.

Commit message:

git commit -m "Add physical player runtime manifest integration"

Do not push.

================================================================================
09 — FINAL REPORT
================================================================================

In final response, report:

- run name
- base commit
- tag status
- corrected framing preserved yes/no
- files created
- files modified
- fixture created yes/no
- runtime adapter created yes/no
- manifest discovery demo created yes/no
- runtime integration demo created yes/no
- docs updated yes/no
- validation commands run
- test results
- manifest/update-event count
- physical section count
- runtime playback transition count
- fail-closed event count
- reverse/seek bounded yes/no
- unsafe_acceptance_count
- generated output committed: no
- local path leak found: no if checked
- unsafe hardware claim found: no if checked
- physical hardware claimed: no
- hardware validation claimed: no
- physical Level 5 claimed: no
- real sensors/motors/cartridges/scans required: no
- manufactured physical player claimed: no
- commit hash if committed
- push command only if committed

Expected push command if committed:

git push

Do not invent a commit hash.
Do not claim physical hardware is proven.
Do not claim real no-gap optical switching is proven.
Do not claim physical reverse hardware is proven.
Do not claim arbitrary physical seek is proven.
Do not claim a manufactured physical player exists.
```

---

# 8. Recommended Manual Commands

## Step 1 — create the public checkpoint tag

```cmd
cd /d "T:\References\to go\Media\tools\Video to Image\Tests\Test AMCF_PUBLIC_GITHUB_PAGES_SITE_PREP\20261011_011430\01_UPDATED_PUBLIC_PACKAGE_WITH_PAGES\AMCF_GITHUB_CLEAN_PACKAGE" && git status --short && git tag -a amcf-physical-player-software-control-v1 -m "AMCF physical-player software-control public release v1" && git push origin amcf-physical-player-software-control-v1
```

## Step 2 — create the runtime integration branch

```cmd
cd /d "T:\References\to go\Media\tools\Video to Image\Tests\Test AMCF_PUBLIC_GITHUB_PAGES_SITE_PREP\20261011_011430\01_UPDATED_PUBLIC_PACKAGE_WITH_PAGES\AMCF_GITHUB_CLEAN_PACKAGE" && git checkout -b dev/physical-player-runtime-integration
```

## Step 3 — save this brief into the repo

Save this file as:

```text
docs/AMCF_PHYSICAL_PLAYER_SOFTWARE_DEVELOPMENT_BASELINE_BRIEF.md
```

Then run the single Codex prompt above.
