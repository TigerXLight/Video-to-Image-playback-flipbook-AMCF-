# AMCF Software Development and I/O Control Dossier Collection

## Scope

This dossier collection defines the software-development plan for AMCF I/O control:

- PC → Printer
- PC ↔ Reader
- Player ↔ PC
- shared AMCF package / manifest / update-event / physical-section model
- cross-corridor reporting, validation, fail-closed, audit, and fixture strategy
- staged Codex implementation phases

This document is a software planning and implementation-control document. It does not claim real hardware validation, manufactured player completion, or physical Level 5 completion.


## Collection Metadata

- Collection name: AMCF Software Development and I/O Control Dossier Collection
- Intended repo path: docs/AMCF_SOFTWARE_DEVELOPMENT_AND_IO_CONTROL_DOSSIER_COLLECTION.md
- Baseline checkpoint: e7e13155db3441887c5982cb0dfa9bd91383390a
- Suggested baseline tag: amcf-physical-player-software-control-v1
- Recommended development branch: dev/amcf-software-io-control
- First implementation phase: AMCF_SOFTWARE_IO_REPO_AUDIT_V1
- Hardware validation claimed: false
- Physical Level 5 claimed: false
- Manufactured player claimed: false

## Source Anchors from Physical-Player Dossier

This collection is derived from the AMCF software dossier source record `software plan.txt` and from the prior AMCF physical-player design/control sequence. In repo form, ChatGPT-only citation placeholders from the source record are converted into this normal source-note wording.

The source anchors preserved here are:

- PC -> Printer, PC <-> Reader, and Player <-> PC are treated as software I/O corridors.
- The physical player is modelled as a future executor of digital AMCF schedule/update-event data through a physical carrier and optical viewing window.
- The shared AMCF package, manifest, update-event, physical-section, report, fixture, and safety models are central to all corridors.
- Physical hardware validation, manufactured player completion, and physical Level 5 completion are not claimed.

## Claim Boundary

This dossier describes software planning, software architecture, simulated control, package models, reports, fixtures, and implementation sequencing.

Current claim-boundary values:

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false

This dossier does not claim real hardware validation, manufactured player completion, physical Level 5 completion, real printer/scanner/player integration, or hardware proof.

## Corridor Summary

### PC -> Printer

Prepare digital AMCF package data for future printable/exported physical carrier packages using shared schedule, manifest, section, lane, registration, colour, metadata, hash, and report models.

### PC <-> Reader

Recover or verify physical AMCF carrier data back into digital AMCF through no-hardware-first fixtures, captures, lane recognition, hash/checksum validation, diagnostics, and audit reports.

### Player <-> PC

Support future physical/optical player alignment through package compatibility checks, capability profiles, runtime simulation, fail-closed decisions, bounded reverse/seek control, diagnostics, and future protocol boundaries.

## Implementation Phase Index

0. `AMCF_SOFTWARE_IO_BRANCH_BASELINE_V1`
1. `AMCF_SOFTWARE_IO_REPO_AUDIT_V1`
2. Shared AMCF package / manifest / update-event / physical-section model foundation
3. Cross-corridor report, claim-boundary, and safety model foundation
4. PC -> Printer software path planning and no-hardware fixture path
5. PC <-> Reader software path planning and no-hardware fixture path
6. Player <-> PC software path alignment and simulator-control bridge
7. Cross-corridor fixture and regression strategy
8. Public docs / release / package refresh for software I/O work

## First Implementation Phase

The first Codex implementation phase after this collection is:

`AMCF_SOFTWARE_IO_REPO_AUDIT_V1`

That phase should audit the existing repo and classify current source, docs, demos, tests, reports, schemas, and generated-output conventions by corridor. It should not implement printer, reader, player runtime, package-model, or report-model modules yet.

## Implementation Control Rules

1. Implement one phase at a time.
2. Run repo audit before creating new models.
3. Do not introduce hardware APIs before no-hardware fixtures pass.
4. Do not introduce GUI before CLI/report flows pass.
5. Do not introduce dependencies unless the current phase justifies them.
6. Keep generated output under `output/`.
7. Do not commit generated output.
8. Keep `unsafe_acceptance_count` at 0.
9. Keep hardware claim flags false.
10. Run `python -m unittest discover -s tests` before commit.
11. Commit only intended files.
12. Do not push unless explicitly instructed.

## Do Not Do Yet

Do not implement yet:

- real printer driver integration
- real scanner API
- camera capture
- USB/HID/serial player protocol
- firmware protocol
- GUI application
- local web UI
- image-processing dependency
- PDF dependency
- barcode/QR dependency
- hardware-in-the-loop tests
- physical-player hardware validation claims
- `AMCF_SOFTWARE_IO_REPO_AUDIT_V1` implementation in this collection-file task

---

From now on, the part numbers are not a fixed outline. A “Part” is just one maximum-useful response chunk. If one subject needs three responses, then it becomes Part 1, Part 2, Part 3, etc. If another subject fits in one response, it gets one part. The information controls the part count, not the other way around.

# AMCF Software Development and I/O Control Dossier  
## Part 1 — Scope Reset, Software Boundary, I/O Corridors, and Development Philosophy

## 1. Why this dossier exists

The previous attached collection was the **AMCF Physical Player Design and Structure Dossier**. It was about the future physical-player object: what the player should be, how it should look, how the carrier path should work, how A/B staging works, what mechanisms are plausible, and what is unresolved. The file itself begins by separating that physical-player dossier from the earlier I/O scope, which covered **PC → Printer**, **Reader → PC**, and **Player ↔ PC software recognition/control**. This new dossier is not the same thing as the physical-player design dossier.

This new dossier is about the **software system around AMCF**.

It should answer:

```text
What software needs to exist so AMCF can move between:
- PC software
- printer output
- reader/scanner recovery
- physical-player simulation/control
- AMCF package files
- manifests
- update-event schedules
- reports
- tests
- future hardware interfaces
```

The physical-player dossier asked:

```text
What should the AMCF physical player be?
What should it look like?
How should the internal carrier path work?
How does it physically/optically execute digital AMCF?
What mechanisms are plausible?
What remains unresolved?
```

Those questions are explicitly listed in the attached physical-player plan. The software dossier asks a different set of questions:

```text
What software should generate physical AMCF output?
What software should read physical AMCF back into the PC?
What software should control or simulate the physical player?
What package/manifest format connects all of this?
What tools should be used?
What should be implemented first?
What must remain only simulated until hardware exists?
How should Codex build this in a controlled progression?
```

So this dossier is the **software counterpart** to the physical-player design dossier.

---

## 2. The core mistake to avoid

The mistake would be to treat this as only:

```text
physical-player runtime integration
```

That is too narrow.

The full software system must cover:

```text
PC → Printer
PC ↔ Reader
Player ↔ PC
AMCF package / manifest / update-event data
Physical-player simulator/runtime
Tests, reports, fixtures, public docs, release process
```

So the software dossier should not jump straight to one module.

It should first define the whole AMCF software environment.

---

## 3. The three main I/O corridors

The software system should be organised around three main corridors.

```text
Corridor 1 — PC → Printer
Corridor 2 — PC ↔ Reader
Corridor 3 — Player ↔ PC
```

These correspond to the earlier I/O scope mentioned at the start of the physical-player plan. Each corridor has its own software requirements, but they must all share the same AMCF package, manifest, timing, section, hash, and report logic.

---

# Corridor 1 — PC → Printer

## 4. What PC → Printer means

This corridor is about converting digital AMCF data into a printable physical carrier.

The software chain is:

```text
Digital AMCF package
→ print/export manifest
→ printable section layout
→ registration/index/timing lanes
→ colour/hash/checksum lanes
→ PDF/SVG/PNG/print output
→ printed AMCF physical carrier
```

The physical-player dossier already defines the physical chain as:

```text
Digital AMCF
→ AMCF schedule / update events
→ physical AMCF carrier
→ physical player transport
→ physical/optical viewing window
```

That means the printer corridor is responsible for creating the **physical AMCF carrier** part of that chain. So the PC → Printer software must decide:

```text
What exactly is printed?
How is each physical AMCF section represented?
How are update events encoded physically?
How are section indexes encoded?
How are timing markers encoded?
How are registration marks placed?
How are hash/checksum lanes printed?
How does the print package prove that the carrier matches the AMCF manifest?
```

This is not just “print screenshots.”

It is structured AMCF physical output.

---

## 5. PC → Printer software responsibilities

This corridor needs software for:

```text
- AMCF package loading
- AMCF schedule extraction
- visible-state / update-event selection
- physical section generation
- page/strip/card layout
- registration marks
- timing/index lanes
- hash/checksum lanes
- colour calibration marks
- printer-safe margins
- page numbering / section numbering
- print preview
- print manifest generation
- print audit report
- reprint support for damaged sections
```

The physical-player dossier repeatedly states that the player must follow **AMCF update events**, not fixed-FPS page flipping. For example, it says the physical player should hold the current visible state, preload the next required state, and switch at the update timestamp. That rule affects printing.

The printer path should not blindly print every video frame.

It should print the physical AMCF sections required by the AMCF update schedule.

---

## 6. Software choices that must be researched for PC → Printer

This dossier eventually needs to research or decide:

```text
- Should print output be PDF, SVG, PNG sheets, or multiple formats?
- Should layout generation be Python-only?
- Should there be a GUI print-preview tool?
- Should section geometry be expressed in JSON?
- Should print lanes use QR/barcode-like markers or custom visible lane marks?
- How should colour calibration marks be represented?
- How should hash/checksum data be encoded?
- How should print validation happen before the user prints?
- How should damaged-section reprint packs be generated?
```

Possible software areas to research later:

```text
- Python PDF generation
- SVG generation
- image rendering/export
- print layout validation
- colour management basics
- printer-safe margin handling
- checksum/hash encoding
- barcode/marker libraries if needed
```

But Part 1 does not choose the final tools yet.

Part 1 only establishes that tool research is part of the software dossier.

---

# Corridor 2 — PC ↔ Reader

## 7. What PC ↔ Reader means

This corridor is about reading physical AMCF media back into the PC.

The physical-player plan distinguishes the reader/recovery path from the physical-player path. It says the reader/scanner path recovers or validates AMCF media, while the physical-player path physically/optically presents AMCF media for direct viewing. So reader software is not the same as player software.

The reader corridor is:

```text
Physical AMCF carrier
→ reader/scanner capture
→ PC-side image/lane processing
→ section detection
→ index/timing recovery
→ hash/checksum verification
→ reconstructed AMCF package or audit report
```

It is **PC ↔ Reader**, not only Reader → PC, because the PC may also need to configure the reader:

```text
- scan resolution
- calibration
- lighting
- capture mode
- batch mode
- lane-detection parameters
- retry/rescan instructions
```

---

## 8. Reader software responsibilities

The reader corridor needs software for:

```text
- reader/scanner detection
- reader configuration
- calibration capture
- raw scan/image capture
- section boundary detection
- lane detection
- timing/index lane recognition
- registration marker detection
- colour reference reading
- hash/checksum lane reading
- damaged-section diagnosis
- section reconstruction
- AMCF package recovery
- reader audit reports
```

The physical-player dossier says the player-prefetch reader lane should read section index, timing marks, registration marks, colour registry, metadata/transform lane, hash/checksum lane, and damage/missing marker status. Those same software ideas matter for the PC reader, but with a different purpose:

```text
Player prefetch reader:
read ahead fast enough to allow or block display.

PC reader/recovery:
recover, validate, reconstruct, diagnose, and archive.
```

The software should eventually support both.

---

## 9. Software choices that must be researched for PC ↔ Reader

This dossier later needs to research:

```text
- image acquisition method
- scanner API options
- camera/capture options
- Windows compatibility
- offline image-folder input as a no-hardware fallback
- lane detection method
- registration mark detection
- barcode/marker decoding if used
- colour reference extraction
- OCR avoidance unless necessary
- checksum/hash validation
- damaged-section recovery workflow
```

Very important boundary:

```text
The first software implementation should not require real reader hardware.
```

It should allow:

```text
- fixture images
- generated test sheets
- scanned-image folders
- simulated reader output
```

Real device support can come later.

---

# Corridor 3 — Player ↔ PC

## 10. What Player ↔ PC means

The physical-player dossier defines the corrected player branch as:

```text
compact tablet-like optical player
+ folded internal indexed media path
+ side-loaded cartridge/card/section stack
+ visible view gate
+ hidden preload/staging gate
+ shutter/illumination blanking
+ reader/prefetch lanes
+ dynamic AMCF schedule
+ physical/optical viewing window
```

That description appears directly in the attached plan. Software-wise, Player ↔ PC means:

```text
PC prepares the package / manifest / schedule.
PC simulates whether the player can execute it.
PC may later transfer package/control data to the player.
Player may later report playback state, errors, diagnostics, and audit logs.
```

For now, because no hardware exists, this corridor begins as:

```text
PC-side player simulator
+ future protocol model
+ device capability model
+ report/log model
```

Not real USB/hardware control yet.

---

## 11. Player ↔ PC software responsibilities

This corridor needs software for:

```text
- player capability profiles
- mechanism profile selection
- package compatibility check
- cartridge/package recognition model
- playback schedule transfer model
- state-machine execution
- fail-closed safety decisions
- reverse/seek command limits
- audio sync status
- diagnostics
- playback logs
- PC-side report viewer
- later device communication protocol
```

The attached physical-player plan says the player must decide whether the next section is ready, verified, whether the A/B gate is ready, whether audio sync is acceptable, and whether to continue, pause, or fail closed. That becomes a software-control problem.

The PC/player software must eventually answer:

```text
Can this package be played safely by this player profile?
What mechanism profile is assumed?
What update events are too fast?
Where would fail-closed occur?
Can reverse/seek be supported?
What does the playback report say?
```

---

## 12. The shared AMCF software core

The three corridors cannot be separate unrelated tools.

They need one shared core.

```text
Shared AMCF Software Core:
- package model
- manifest schema
- update-event schema
- physical-section schema
- timing model
- validation model
- hash/checksum model
- report model
- fixture model
- claim-boundary model
```

The same manifest should support:

```text
- digital playback
- printer output
- reader recovery
- player simulation
- later player control
```

If each corridor invents its own format, AMCF becomes fragmented.

So the software dossier must eventually define the shared data model before implementing too much corridor-specific software.

---

## 13. Dynamic schedule as the centre of the software system

The physical-player dossier says the physical transport must not move one physical page for every fixed 24/30/60 FPS frame. Instead, it should move physical media according to AMCF update events, hold the current visible state, preload the next required state, switch at the update timestamp, and fail closed if the next state is not verified. This is the most important software rule.

It affects every corridor:

```text
PC → Printer:
print AMCF update sections, not every video frame.

PC ↔ Reader:
recover indexed AMCF update sections, not generic scanned pages.

Player ↔ PC:
execute AMCF update events, not fixed-FPS page flipping.

Shared package model:
store timing/update events as first-class data.
```

So the software architecture should be built around:

```text
AMCF update events
```

not:

```text
video frame numbers only
```

Frame numbers may still exist as metadata, but the AMCF update schedule is the key.

---

## 14. Software stack research belongs in this dossier

Yes, this dossier should research what software to use.

But it should not pick tools randomly.

The research should be organised by software layer:

```text
A. Core language/runtime
B. CLI tooling
C. Desktop UI
D. Local web UI
E. Data formats
F. Print/export generation
G. Reader/image processing
H. Device communication
I. Testing framework
J. Reporting format
K. Packaging/release tooling
```

For each layer, later parts should compare:

```text
- candidate tools
- why they fit AMCF
- Windows compatibility
- offline compatibility
- repo compatibility
- testability
- future hardware compatibility
- risk of overbuilding
- implementation order
```

This is important because software stack choice affects the whole project.

For example:

```text
Printer path may prefer PDF/SVG generation.
Reader path may need image-processing tools.
Player ↔ PC may start as JSON reports before real device protocol.
Desktop UI may be later than CLI.
```

The first implementations should likely stay standard-library/Python-heavy where possible, because the current repo and tests are already moving that way.

But formal selection belongs in a later part.

---

## 15. Implementation belongs in this dossier too

This dossier is not only research.

It should also define implementation progression.

The correct structure is:

```text
research
→ decision
→ implementation phase
→ tests
→ reports
→ public docs refresh
→ next phase
```

So each future software area should be described in two ways:

```text
Research:
What should we use and why?

Implementation:
What should Codex build first, second, third?
```

Example:

```text
PC → Printer

Research:
PDF vs SVG vs PNG, layout engine, print calibration.

Implementation:
manifest-to-print-layout module,
print-sheet fixture,
print preview report,
tests for margins/sections/lane positions.
```

This avoids endless research without code, and avoids coding without a proper plan.

---

## 16. The progression-cycle model

We should keep using a staged progression cycle, but not a fixed artificial part count.

The cycle should be:

```text
1. Dossier parts are written as much as needed.
2. Each part expands only as far as the subject requires.
3. When a subject is too large, the next answer continues it.
4. After the software dossier is complete, all parts are collected into one file.
5. The final Codex prompt references that collection file.
6. Codex then implements one phase at a time from the collection.
```

The final collection file should eventually be something like:

```text
docs/AMCF_SOFTWARE_DEVELOPMENT_AND_IO_CONTROL_DOSSIER_COLLECTION.md
```

The final Codex prompt should not repeat the whole dossier.

It should say:

```text
Read docs/AMCF_SOFTWARE_DEVELOPMENT_AND_IO_CONTROL_DOSSIER_COLLECTION.md first.
Treat it as the controlling software-development plan.
Implement Phase 1 only.
Do not skip ahead.
Preserve claim boundaries.
```

---

## 17. Do not constrain information to a fixed part list

The part numbering is not a promise that the dossier has a fixed number of sections.

The correct rule is:

```text
The amount of information decides the number of parts.
```

So if “software stack research” needs several parts, it should get several parts.

If “PC → Printer” needs multiple parts, it should get multiple parts.

If “Player ↔ PC” needs multiple parts, it should get multiple parts.

We should not compress a large subject into one part just because the plan says “Part 6.”

That was the useful pattern from the physical-player dossier.

---

## 18. Revised title and scope

The correct title should now be:

```text
AMCF Software Development and I/O Control Dossier
```

Subtitle:

```text
PC → Printer, PC ↔ Reader, Player ↔ PC, Shared AMCF Package Model, Runtime Integration, Software Stack Research, and Codex Implementation Progression
```

This makes clear that the software plan covers the full ecosystem.

---

## 19. What Part 1 decides

Part 1 decides:

```text
- this is a new dossier, not a continuation of the physical-player design dossier
- the part count will be driven by information density, not a fixed outline
- the software scope includes PC → Printer, PC ↔ Reader, and Player ↔ PC
- software stack research is included
- implementation planning is included
- shared package/manifest/update-event modelling is central
- physical-player runtime integration is only one corridor within the wider
- no final single Codex prompt should be written yet
- the final Codex prompt will come only after the software dossier parts are complete
```

---

## 20. What Part 2 should continue with

Part 2 should continue naturally into:

```text
Current AMCF software baseline and existing repo surface
```

That means:

```text
- what software already exists
- what the current repo has already implemented
- what the physical-player software/control checkpoint contains
- what is missing for PC → Printer
- what is missing for PC ↔ Reader
- what is missing for Player ↔ PC
- what must be discovered from the repo before implementation
- how to separate public-release checkpoint work from new dev-branch work
```

----
# AMCF Software Development and I/O Control Dossier  
## Part 2 — Current Software Baseline, Existing Repo Surface, and Discovery Boundaries

## 1. Purpose of Part 2

Part 1 reset the new dossier correctly.

This dossier is now:

```text
AMCF Software Development and I/O Control Dossier
```

not:

```text
AMCF Physical Player Design and Structure Dossier
```

The attached physical-player collection confirms that the earlier physical-player dossier was created as a separate staged dossier, and that it was different from the earlier Physical I/O scope of **PC → Printer**, **Reader → PC**, and **Player ↔ PC software recognition/control**. Part 2 now defines the **current software baseline**.

That means:

```text
What software already exists?
What has already been pushed?
What is only documented/planned?
What is missing?
What must Codex discover from the repo before implementation?
What is the clean boundary between the public checkpoint and new development?
```

This part is not implementation yet.

It is the software inventory and baseline map.

---

## 2. Current public checkpoint

The latest pushed checkpoint from the ongoing work is:

```text
AMCF_PUBLIC_RELEASE_TAG_PREP_V1
Commit: e7e13155db3441887c5982cb0dfa9bd91383390a
```

That commit prepared release-tag materials but did not create the tag.

Suggested tag:

```text
amcf-physical-player-software-control-v1
```

The meaning of that tag should be:

```text
This is the clean public checkpoint for the AMCF physical-player software/control foundation.
```

It should not mean:

```text
hardware exists
physical playback is proven
motors/sensors/cartridges are validated
Level 5 is complete
```

So the recommended sequence is:

```text
1. tag the current public software/control checkpoint
2. create a new development branch
3. begin software development from that branch
```

Recommended commands:

```cmd id="m4y2cy"
cd /d "<repo-root>" && git status --short && git tag -a amcf-physical-player-software-control-v1 -m "AMCF physical-player software-control public release v1" && git push origin amcf-physical-player-software-control-v1
```

Then:

```cmd id="v6idju"
cd /d "<repo-root>" && git checkout -b dev/amcf-software-io-control
```

The branch name should be broader than physical-player runtime only, because the new software dossier covers:

```text
PC → Printer
PC ↔ Reader
Player ↔ PC
shared AMCF package/manifest model
runtime integration
software stack research
implementation progression
```

---

## 3. What already exists from the physical-player software/control work

The current repo has already developed a **physical-player software/control foundation**.

Known completed layers:

```text
1. physical-player state machine
2. fail-closed safety
3. reverse/seek controls
4. mechanism profiles
5. integrated simulator demo
6. public docs sync
7. release review
8. package refresh
9. GitHub Pages final review
10. closeout handoff
11. tag prep
```

These are useful, but they are not the whole software system.

They mostly cover:

```text
Player-side simulator/control foundation
```

They do not yet fully cover:

```text
PC → Printer production software
PC ↔ Reader recovery software
shared AMCF package schema across all corridors
real package/manifest-driven runtime integration
software stack decisions
full progression plan
```

So the current state is strong, but partial.

---

## 4. Existing physical-player source surface

The known physical-player software/control modules include:

```text
src/amcf_physical_player_state_machine.py
src/amcf_physical_player_state_machine_reports.py
src/amcf_physical_player_mechanism_profiles.py
src/amcf_physical_player_mechanism_profile_reports.py
src/amcf_physical_player_integrated_demo_reports.py
```

These represent the current player simulator/control foundation.

Their likely roles are:

```text
amcf_physical_player_state_machine.py
- cartridge/state-machine flow
- visible gate / hidden gate logic
- transition blanking
- fail-closed decisions
- reverse/seek control

amcf_physical_player_state_machine_reports.py
- playback/safety/reverse/seek reports

amcf_physical_player_mechanism_profiles.py
- mechanism profile catalogue
- default folded A/B motor/encoder baseline
- research/support profiles
- claim-boundary profile flags

amcf_physical_player_mechanism_profile_reports.py
- mechanism profile reports and comparisons

amcf_physical_player_integrated_demo_reports.py
- integrated simulator summary/report helpers
```

These should not be replaced.

Future software should reuse them.

---

## 5. Existing physical-player demos

Known demo scripts include:

```text
demo/run_physical_player_state_machine_demo.py
demo/run_physical_player_fail_closed_demo.py
demo/run_physical_player_reverse_seek_demo.py
demo/run_physical_player_mechanism_profiles_demo.py
demo/run_physical_player_simulator_demo.py
demo/run_physical_player_release_review.py
demo/run_public_release_package_refresh.py
demo/run_public_github_pages_final_review.py
demo/run_public_release_closeout_handoff.py
demo/run_public_release_tag_prep.py
```

These are valuable because they already give the project a tested public/review scaffold.

But most of these demos are review, report, or deterministic simulator demos.

The next actual software development should add demos that use real or fixture AMCF package data.

Future examples:

```text
demo/run_amcf_print_package_demo.py
demo/run_amcf_reader_recovery_demo.py
demo/run_player_pc_package_control_demo.py
demo/run_amcf_software_io_end_to_end_demo.py
```

Those names are examples, not final decisions.

---

## 6. Existing physical-player tests

Known test files include:

```text
tests/test_physical_player_state_machine.py
tests/test_physical_player_fail_closed.py
tests/test_physical_player_reverse_seek.py
tests/test_physical_player_mechanism_profiles.py
tests/test_physical_player_simulator_demo.py
tests/test_physical_player_public_docs_sync.py
tests/test_physical_player_release_review.py
tests/test_public_release_package_refresh.py
tests/test_public_github_pages_final_review.py
tests/test_public_release_closeout_handoff.py
tests/test_public_release_tag_prep.py
```

The latest known full suite result was:

```text
294 tests passing
```

This matters because future software development should not break these tests.

The new software dossier should treat the existing tests as a regression baseline.

---

## 7. Existing physical-player docs/public surface

Known docs include:

```text
docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md
docs/AMCF_PHYSICAL_PLAYER_PUBLIC_SUMMARY.md
docs/AMCF_PHYSICAL_PLAYER_CONCEPT.md
docs/AMCF_PHYSICAL_PLAYER_STATE_MACHINE.md
docs/AMCF_PHYSICAL_PLAYER_FAIL_CLOSED.md
docs/AMCF_PHYSICAL_PLAYER_REVERSE_SEEK.md
docs/AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES.md
docs/AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO.md
docs/AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW.md
docs/AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH.md
docs/AMCF_PUBLIC_RELEASE_PACKAGE_INVENTORY.md
docs/AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW.md
docs/AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF.md
docs/AMCF_PUBLIC_RELEASE_TAG_PREP.md
docs/AMCF_PUBLIC_RELEASE_NOTES_DRAFT.md
docs/AMCF_PUBLIC_RELEASE_TAG_CHECKLIST.md
docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md
docs/AMCF_HARDWARE_SOFTWARE_PATHS.md
```

These docs preserve the current physical-player software/control story.

But the new software dossier will need its own docs later, probably under names like:

```text
docs/AMCF_SOFTWARE_DEVELOPMENT_AND_IO_CONTROL_DOSSIER_COLLECTION.md
docs/AMCF_SOFTWARE_IO_CONTROL_ROADMAP.md
docs/AMCF_PC_TO_PRINTER_SOFTWARE_PLAN.md
docs/AMCF_PC_READER_SOFTWARE_PLAN.md
docs/AMCF_PLAYER_PC_SOFTWARE_PLAN.md
docs/AMCF_SHARED_PACKAGE_MANIFEST_MODEL.md
docs/AMCF_SOFTWARE_STACK_RESEARCH.md
```

Those should not be created until the dossier has enough content.

---

## 8. What the current baseline already proves

The current baseline proves that the repo has a working software/control scaffold for the physical-player concept.

It proves:

```text
- deterministic physical-player state-machine simulation exists
- fail-closed safety logic exists
- reverse/seek bounds exist
- mechanism profiles exist
- integrated simulator reporting exists
- public docs/site/package/review tooling exists
- generated-output exclusion checks exist
- local-path and unsafe-claim scans exist
- unsafe_acceptance_count can remain zero in demos
```

This is a strong foundation for software development.

But it does not yet prove:

```text
- PC → Printer pipeline exists
- PC ↔ Reader recovery pipeline exists
- Player ↔ PC protocol exists
- real AMCF package manifest is connected to physical-player runtime
- print layouts exist
- reader image processing exists
- complete shared AMCF package schema exists
- desktop UI exists
- real hardware communication exists
```

So the next software work should be based on the existing foundation, not confused with it.

---

## 9. The physical-player plan already gives software requirements

The attached physical-player plan is not software code, but it contains many software requirements.

For example, it says the physical player must use AMCF update events, preloading, verification, staging, transition blanking, and fail-closed behaviour, rather than fixed FPS page movement. That implies software must model:

```text
- update events
- dwell durations
- preload deadlines
- verification windows
- transition blanking
- gate lock timing
- fail-closed decisions
```

It also says the player needs a prefetch reader lane that reads timing/index/hash/checksum, registration, colour registry, metadata/transform, and damage/missing marker status. That implies software must model:

```text
- section index
- timing marks
- registration marks
- colour reference data
- metadata lanes
- hash/checksum lanes
- damage/missing marker status
```

So the software dossier should extract software requirements from the physical-player plan, not treat it as unrelated.

---

## 10. Existing software baseline by corridor

Now the important part: what exists per corridor.

# Corridor 1 — PC → Printer

## 10.1 Current known status

Current known status:

```text
partly conceptual / not yet fully implemented as a dedicated corridor
```

The physical-player work implies the need for printable physical AMCF sections, but the currently known completed sequence focused more on player simulation and public docs.

So for PC → Printer, the repo must be audited for existing:

```text
- print/export modules
- package/export scripts
- layout files
- sheet generation
- PDF/SVG/PNG output
- manifest-to-print logic
- printer metadata
- registration mark generation
- hash/checksum lane generation
- print audit reports
```

Do not assume absent until Codex searches the repo.

But based on the current sequence, this corridor is not yet the main implemented path.

## 10.2 Missing software questions

PC → Printer still needs to answer:

```text
- What is the print unit? page, strip, card, section sheet, cartridge insert?
- What format is exported? PDF, SVG, PNG, JSON + assets, or all?
- How does print output map to AMCF update events?
- How are physical sections laid out?
- How are lane marks encoded?
- How is colour calibration represented?
- How is hash/checksum data printed?
- How is printer-safe margin handled?
- How does the user reprint a damaged section?
- How is a print job audited?
```

## 10.3 Implementation surface likely needed

Likely future modules:

```text
src/amcf_print_layout.py
src/amcf_print_manifest.py
src/amcf_print_export.py
src/amcf_print_reports.py
```

Likely future demos:

```text
demo/run_amcf_print_layout_demo.py
demo/run_amcf_print_package_demo.py
```

Likely future tests:

```text
tests/test_amcf_print_layout.py
tests/test_amcf_print_manifest.py
tests/test_amcf_print_export.py
```

Those names are placeholders for planning. Codex should inspect repo style before creating names.

---

# Corridor 2 — PC ↔ Reader

## 11.1 Current known status

Current known status:

```text
partly conceptual / partly represented through player-prefetch ideas / not yet fully implemented as a dedicated reader-recovery pipeline
```

The attached plan distinguishes reader/recovery from player presentation. It says the reader/scanner path recovers or validates AMCF media, while the physical-player path physically/optically presents AMCF media for direct viewing. That means the reader software should not be collapsed into the player software.

The repo must be audited for existing:

```text
- reader modules
- scanner/capture abstractions
- virtual reader code
- lane detection
- image processing
- recovery reports
- physical carrier emulator
- fixture scanned sheets/images
```

## 11.2 Missing software questions

PC ↔ Reader still needs to answer:

```text
- What input does the reader software accept first? scanner, image folder, fixture images, camera capture?
- What is the no-hardware reader simulation mode?
- How are section boundaries detected?
- How are timing/index lanes read?
- How are registration marks detected?
- How is colour calibration checked?
- How are hashes/checksums recovered?
- How are damaged sections diagnosed?
- How does the PC request rescan/retry?
- How does recovery become a valid AMCF package again?
```

## 11.3 Implementation surface likely needed

Likely future modules:

```text
src/amcf_reader_input.py
src/amcf_reader_lane_detection.py
src/amcf_reader_recovery.py
src/amcf_reader_reports.py
```

Likely future demos:

```text
demo/run_amcf_reader_fixture_recovery_demo.py
demo/run_amcf_reader_lane_detection_demo.py
```

Likely future tests:

```text
tests/test_amcf_reader_input.py
tests/test_amcf_reader_recovery.py
tests/test_amcf_reader_lane_detection.py
```

Again, names are provisional.

Codex should inspect existing repo conventions first.

---

# Corridor 3 — Player ↔ PC

## 12.1 Current known status

Current known status:

```text
most developed corridor so far, but still simulator/control only
```

The current repo has:

```text
- physical-player state machine
- fail-closed model
- reverse/seek model
- mechanism profiles
- integrated simulator demo
- reports/review scripts
```

That means the Player ↔ PC corridor already has a strong simulator foundation.

But it does not yet have:

```text
- real device protocol
- real player hardware detection
- real USB/serial communication
- firmware protocol
- PC-side live player control UI
- real cartridge read from hardware
```

That is fine.

Those should remain future work.

## 12.2 What Player ↔ PC should become next

The next useful software step is not hardware control.

It is:

```text
AMCF package/manifest → physical-player runtime simulator
```

This means:

```text
- load real or fixture AMCF package data
- extract update events
- build physical-player section records
- run existing state machine
- produce reports
- preserve fail-closed and reverse/seek limits
```

This is the software bridge between the general AMCF package and the physical-player control model.

## 12.3 Future Player ↔ PC layers

Later, after runtime integration, this corridor can develop:

```text
- player capability negotiation model
- player protocol schema
- command schema
- diagnostic event schema
- playback report schema
- simulated PC/player session
- hardware adapter interface placeholder
```

But actual hardware communication should wait.

---

## 13. Shared package/manifest baseline is the missing centre

The biggest missing piece is probably the shared AMCF package/manifest model.

The three corridors all need it:

```text
PC → Printer needs a manifest to print from.
PC ↔ Reader needs a manifest to recover to.
Player ↔ PC needs a manifest to play/simulate from.
```

So before building too much corridor-specific code, the repo needs a clear answer to:

```text
What is an AMCF package?
What is an AMCF manifest?
What is an AMCF update event?
What is a physical section?
What is a printed section?
What is a recovered section?
What is a player section?
Are these the same object or related views of one object?
```

That is likely the most important software architecture issue.

---

## 14. Shared data objects that need definition

The software dossier should eventually define or discover these objects:

```text
AMCFPackage
AMCFManifest
AMCFUpdateEvent
AMCFVisibleState
AMCFPhysicalSection
AMCFPrintedSection
AMCFReaderCapture
AMCFRecoveredSection
AMCFPlayerSection
AMCFPlaybackSchedule
AMCFValidationResult
AMCFHashLane
AMCFRegistrationLane
AMCFColourReference
AMCFReport
```

Some may already exist under different names.

Codex must inspect the repo before inventing replacements.

The goal is not to create duplicate schemas.

The goal is to align existing code or create missing adapters.

---

## 15. What must be discovered from the repo

The next software planning part needs a repo audit strategy.

Codex eventually needs to search for:

```text
manifest
package
export
AMCF
frame
update
timeline
component
playback
schedule
hash
checksum
section
print
printer
reader
scanner
capture
report
fixture
```

The audit should answer:

```text
What package schema already exists?
What export paths already exist?
What manifest examples already exist?
What test fixtures already exist?
What print or reader code already exists?
What physical-player code can be reused?
What should be adapted instead of rewritten?
```

The software dossier should not assume this in advance.

---

## 16. Software stack baseline

Current known implementation style appears to be:

```text
- Python
- standard library where possible
- deterministic demos
- unittest tests
- JSON reports
- Markdown docs
- generated output under output/
- generated output not committed
```

This has worked well for the public physical-player sequence.

So the initial software-development default should be:

```text
Use Python + standard library + JSON + Markdown + unittest unless a corridor proves it needs more.
```

This is not a final software-stack decision.

It is a baseline rule to avoid overbuilding.

Later research may justify dependencies for:

```text
- PDF generation
- SVG rendering
- image processing
- barcode/marker recognition
- GUI
- device communication
```

But dependencies should be introduced deliberately, not casually.

---

## 17. Public release checkpoint versus development branch

A clean separation is needed.

The public release checkpoint is:

```text
main at e7e13155db3441887c5982cb0dfa9bd91383390a
optional tag: amcf-physical-player-software-control-v1
```

Development should happen on a branch.

Recommended branch:

```text
dev/amcf-software-io-control
```

Why not only:

```text
dev/physical-player-runtime-integration
```

Because the software dossier now covers more than runtime integration.

A narrower branch can still be created later for one phase, but the broad software dossier branch should reflect the full scope.

Possible branch structure:

```text
dev/amcf-software-io-control
  → phase/package-manifest-audit
  → phase/pc-printer-layout
  → phase/reader-recovery-fixtures
  → phase/player-runtime-integration
```

But do not overcomplicate branch management until Codex begins implementation.

---

## 18. What should not be touched yet

At this stage, the following should not be changed without a specific implementation part:

```text
- existing physical-player state-machine behaviour
- fail-closed logic
- reverse/seek logic
- mechanism profile ranking
- public release review scripts
- tag-prep docs
- site/public pages except for intentional docs links
```

The software dossier should first define what to build.

Then Codex should implement one phase at a time.

---

## 19. What Part 2 decides

Part 2 decides:

```text
- the current repo baseline is a physical-player software/control checkpoint
- the Player ↔ PC simulator/control corridor is the most developed so far
- PC → Printer is not yet fully developed and needs its own software path
- PC ↔ Reader is not yet fully developed and needs its own software path
- the shared AMCF package/manifest/update-event model is the missing centre
- future code should reuse existing physical-player modules, not replace them
- the initial software-stack baseline should remain Python/standard-library/unittest/JSON/Markdown where possible
- a broad development branch like dev/amcf-software-io-control fits the new dossier better than a player-only branch
- repo discovery must happen before implementation assumptions
```

---

## 20. What Part 3 should continue with

Part 3 should now go deeper into:

```text
Repo audit and discovery strategy
```

That should include:

```text
- exact search terms
- how Codex should inspect the repo
- what files/modules it should look for
- how to classify existing code by corridor
- how to detect duplicate schemas
- how to decide whether to adapt or create modules
- how to record findings
- what audit docs/scripts/tests should eventually be created
```

----
# AMCF Software Development and I/O Control Dossier  
## Part 3 — Repo Audit, Discovery Strategy, Corridor Classification, and Schema-Control Method

## 1. Purpose of Part 3

Part 1 reset the dossier.

Part 2 defined the current baseline:

```text
- current repo = strong physical-player software/control checkpoint
- Player ↔ PC simulator/control path = most developed so far
- PC → Printer path = needs discovery and planning
- PC ↔ Reader path = needs discovery and planning
- shared AMCF package/manifest/update-event model = likely missing centre
```

Part 3 now defines how the repo should be audited before implementation.

This is important because the next Codex work must not blindly create new modules if the repo already has partial package, manifest, export, reader, printer, or report structures.

The audit needs to answer:

```text
What already exists?
What is duplicated?
What should be reused?
What should be adapted?
What is genuinely missing?
Which corridor does each file belong to?
What software schema already controls AMCF data?
```

This part is still not implementation.

It is the discovery method that should prevent bad implementation later.

---

## 2. Why repo discovery must come before coding

The new software dossier covers the full I/O software system:

```text
PC → Printer
PC ↔ Reader
Player ↔ PC
shared AMCF package / manifest / update-event model
```

The attached physical-player dossier already separates those concerns. It begins by distinguishing the earlier I/O scope — **PC → Printer**, **Reader → PC**, and **Player ↔ PC software recognition/control** — from the later physical-player object dossier. That means the software repo may already contain pieces from earlier I/O thinking, even if they were not part of the later physical-player work.

So Codex must not assume:

```text
there is no printer code
there is no reader code
there is no manifest schema
there is no package model
there is no export model
```

It must search first.

The rule for future Codex runs should be:

```text
Do not invent a new AMCF software structure until the existing repo structure has been audited.
```

---

## 3. Audit goal

The audit should produce a corridor map of the repo.

The corridor map should classify existing files into:

```text
A. Shared AMCF core
B. PC → Printer
C. PC ↔ Reader
D. Player ↔ PC
E. Physical-player simulator/control
F. Reports/logs/audits
G. Tests/fixtures
H. Docs/site/release tooling
I. Generated output / ignored artifacts
J. Unclear or duplicate structures
```

This is the first major software-development task after the dossier is complete.

Not implementation.

Discovery.

---

## 4. The three-corridor audit model

The audit should classify everything against the three main software corridors.

```text
Corridor 1 — PC → Printer
Corridor 2 — PC ↔ Reader
Corridor 3 — Player ↔ PC
```

But it also needs to recognise shared layers.

The full classification should be:

```text
Shared AMCF Core
    package, manifest, schema, update events, timing, validation

PC → Printer
    print layout, export, sheet/card/strip generation, lanes, manifests

PC ↔ Reader
    scanner/reader input, image capture, lane detection, recovery, validation

Player ↔ PC
    package transfer model, capability model, player reports, control protocol

Physical-Player Simulator
    current state machine, fail-closed, reverse/seek, mechanism profiles

Public/Release Infrastructure
    docs, site, release review, package refresh, closeout, tag prep

Tests/Fixtures
    deterministic examples, fixtures, regression tests
```

The physical-player simulator is related to Player ↔ PC, but should be kept as a sub-area because it already has a lot of implementation.

---

## 5. Search terms Codex should use

Codex should audit the repo using broad search terms.

The search should include exact filename and content searches.

Recommended search terms:

```text
manifest
package
export
AMCF
frame
frames
component
components
update
update_event
update event
timeline
schedule
timing
playback
section
sections
physical
print
printer
PDF
SVG
PNG
layout
sheet
card
strip
carrier
reader
scanner
scan
capture
image
lane
marker
registration
colour
color
hash
checksum
digest
report
audit
fixture
fixtures
demo
output
metadata
schema
```

It should also search for existing file prefixes:

```text
amcf_
physical_player
release
package
manifest
reader
printer
print
export
layout
recovery
playback
```

The audit should not only search Python files.

It should inspect:

```text
- src/
- demo/
- tests/
- docs/
- site/
- fixtures or examples if present
- release/package metadata files
- README and claim-boundary docs
- JSON manifests if present
- ignored output only for structure, not for committed source claims
```

---

## 6. What to discover in Shared AMCF Core

The shared AMCF core is the most important missing or partially hidden layer.

Codex should search for any existing object, schema, or convention for:

```text
AMCFPackage
AMCFManifest
AMCFUpdateEvent
AMCFVisibleState
AMCFComponent
AMCFFrame
AMCFTimeline
AMCFPlaybackSchedule
AMCFSection
AMCFPhysicalSection
AMCFValidationResult
AMCFReport
```

The audit should answer:

```text
Does the repo already have a package model?
Does it already have a manifest format?
Does it already store update events?
Does it store frames instead of update events?
Does it store components separately?
Does it already have hash/checksum conventions?
Does it already have report structures?
Are those structures documented?
Are they tested?
Are they used by demos?
```

The key discovery question:

```text
Is there one shared AMCF data model, or are there several partial models?
```

If several partial models exist, future work should adapt/unify rather than create yet another one.

---

## 7. What to discover for PC → Printer

For PC → Printer, Codex should search for software connected to:

```text
print
printer
layout
PDF
SVG
PNG
sheet
page
card
strip
carrier
registration
margin
DPI
colour calibration
hash lane
checksum lane
index lane
timing lane
print manifest
```

It should classify any file found into:

```text
- active print/export code
- prototype/demo code
- documentation only
- old/unused plan
- tests
- generated output
```

The audit should answer:

```text
Is there already a print/export pipeline?
If yes, what does it output?
Does it output normal images or structured AMCF physical sections?
Does it have layout tests?
Does it encode timing/index/hash lanes?
Does it produce a print manifest?
Does it support reprint of damaged sections?
Does it fit dynamic AMCF update events?
```

Important: the printer path should not be assumed to mean “print every frame.”

The physical-player plan says the player follows AMCF update events rather than fixed-FPS page movement. So the print audit must check whether print/export code is update-event-based or frame-based.

---

## 8. What to discover for PC ↔ Reader

For PC ↔ Reader, Codex should search for:

```text
reader
scanner
scan
capture
image
input
camera
CIS
line sensor
lane
marker
registration
alignment
colour
color
hash
checksum
OCR
barcode
QR
recovery
reconstruct
damage
rescan
```

The physical-player plan says the prefetch reader lane needs to read section index, timing marks, registration marks, colour registry/reference, metadata/transform lane, hash/checksum lane, and damage/missing-marker status. That gives the reader audit a checklist.

The audit should answer:

```text
Is there reader/recovery software already?
Does it accept real scanner input?
Does it accept image-folder input?
Does it have fixture images?
Does it detect section boundaries?
Does it detect lanes?
Does it validate hashes/checksums?
Does it reconstruct AMCF packages?
Does it generate reader audit reports?
Does it separate reader/recovery from player-prefetch?
```

The distinction matters because the physical-player plan explicitly separates reader/scanner recovery from physical-player direct presentation. So the audit should flag if the repo conflates:

```text
reader/recovery scan gate
```

with:

```text
player visible view gate
```

Those should be related but not identical.

---

## 9. What to discover for Player ↔ PC

For Player ↔ PC, Codex should search for:

```text
player
physical_player
state_machine
mechanism
profile
capability
cartridge
manifest
control
command
protocol
diagnostic
log
report
fail_closed
reverse
seek
audio_sync
prefetch
view_gate
hidden_gate
```

This is the corridor with the most known completed work.

The audit should distinguish:

```text
already implemented:
- simulator state machine
- fail-closed
- reverse/seek
- mechanism profiles
- integrated reports

not yet implemented:
- real device detection
- real protocol
- real hardware communication
- real player firmware bridge
```

Future Player ↔ PC software should not jump to hardware protocol first.

It should likely move next into:

```text
AMCF package/manifest → physical-player runtime simulator
```

But Part 3 still only defines discovery.

---

## 10. What to discover for reports, logs, and audits

The repo already has a strong pattern of deterministic reports.

Codex should search for:

```text
report
audit
summary
scan
claim_boundary
unsafe_acceptance
final_passed
generated_output
local_path
hardware_claim
```

The audit should identify existing report conventions:

```text
- JSON report shape
- Markdown summary shape
- output folder convention
- final_passed booleans
- unsafe_acceptance_count fields
- claim-boundary booleans
- generated-output policy fields
```

This matters because future PC → Printer and PC ↔ Reader tools should reuse the same reporting style.

For example, future printer reports should probably include:

```text
final_passed
print_layout_valid
section_count
lane_count
hash_lane_present
registration_marks_present
generated_output_committed false
hardware_validation_claimed false
```

Future reader reports should probably include:

```text
final_passed
sections_detected
lanes_detected
hashes_verified
damaged_sections
recovery_passed
generated_output_committed false
hardware_validation_claimed false
```

---

## 11. What to discover for tests and fixtures

Codex should search for:

```text
fixtures
fixture
sample
example
testdata
golden
expected
input
output
```

The audit should answer:

```text
Are there existing AMCF package fixtures?
Are there existing manifest fixtures?
Are there image fixtures?
Are there print-layout fixtures?
Are there player-section fixtures?
Are there release-review fixtures?
Where do tests expect fixture files to live?
Are tests ignored by .gitignore and require force-add?
```

The current workflow repeatedly encountered broad ignore rules around tests. Future Codex prompts need to know that test files may require force-add.

That should become part of the software implementation method.

---

## 12. What to discover for docs and public site

Codex should search docs/site for the software public surface.

Important files:

```text
README.md
CLAIM_BOUNDARIES.md
docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md
docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md
docs/AMCF_HARDWARE_SOFTWARE_PATHS.md
site/index.html
```

The audit should answer:

```text
Where should future software docs be linked?
Is there already a docs map pattern?
Is there already a public summary pattern?
How should new software/I/O docs be linked without bloating README?
Does site/index.html have a section where software docs belong?
```

Future software docs should probably become their own map:

```text
docs/AMCF_SOFTWARE_IO_CONTROL_DOCS_MAP.md
```

But this should be decided after the audit.

---

## 13. What to discover for release/package tooling

Codex should inspect:

```text
RELEASE_MANIFEST.json
PACKAGE_MANIFEST.md
MANIFEST.md
RELEASE_NOTES.md
CHANGELOG.md
PUBLICATION_STATUS.md
docs/AMCF_PUBLIC_RELEASE_PACKAGE_INVENTORY.md
docs/AMCF_PUBLIC_RELEASE_TAG_PREP.md
```

The audit should answer:

```text
What release/package metadata exists?
Is it current or historical?
Does it include the new physical-player docs?
Does it include future software/I/O docs?
Should it be updated only after implementation phases?
```

Part 2 already noted that older release metadata may exist and should not be rewritten blindly.

The audit should classify release files as:

```text
current
historical
generated
manual
stale-but-preserved
needs later refresh
```

---

## 14. Duplicate schema detection

One of the biggest risks is duplicate schema creation.

Codex should detect whether the repo already has multiple ways to represent:

```text
manifest
package
update event
timeline
section
physical section
player section
print section
reader recovered section
report
```

The audit should flag possible duplicates.

Example duplicate risk:

```text
AMCFUpdateEvent in one module
update_event dict in another module
timeline_event in a third module
physical_section timing fields in another module
```

The goal is not to immediately merge them.

The goal is to identify them and decide:

```text
reuse
adapt
wrap
deprecate later
leave separate
```

Do not create new schemas until this is done.

---

## 15. Adapt versus create rule

Future implementation should follow this rule:

```text
Adapt existing models if they already express the needed concept.
Create new models only when no existing model covers the need cleanly.
```

Decision method:

```text
1. Search existing code.
2. Identify candidate models.
3. Check tests/demos using them.
4. Check docs describing them.
5. Decide if they are active and stable.
6. Prefer adapter/wrapper over replacement.
7. Only create new canonical structure if existing structures are missing or clearly insufficient.
```

This prevents the repo from accumulating disconnected AMCF package formats.

---

## 16. No-hardware discovery boundary

The audit can search for hardware-facing references, but it should not create hardware code.

It can classify future hardware terms:

```text
USB
serial
HID
scanner
printer
device
firmware
driver
sensor
motor
```

But first implementation should stay in:

```text
simulated input
file-based fixtures
JSON reports
deterministic demos
```

No real hardware APIs should be introduced unless a later dossier part explicitly justifies them.

The physical-player plan itself makes clear that physical proof remains unclaimed and that Level 5 future hardware is not achieved. So audit can prepare for hardware, but implementation should not jump there.

---

## 17. Expected audit output later

When Codex eventually performs this audit, it should produce a report.

Suggested future file:

```text
docs/AMCF_SOFTWARE_IO_REPO_AUDIT.md
```

Suggested future script:

```text
demo/run_amcf_software_io_repo_audit.py
```

Suggested output folder:

```text
output/amcf_software_io_repo_audit/
```

Suggested output files:

```text
software_io_repo_audit_report.json
corridor_file_map.json
schema_discovery_report.json
printer_path_discovery.json
reader_path_discovery.json
player_pc_discovery.json
release_docs_discovery.json
SOFTWARE_IO_REPO_AUDIT_SUMMARY.md
```

Generated output should not be committed.

---

## 18. Expected audit report fields

The future audit report should include:

```text
run_name
current_head
current_branch
tag_status
shared_core_files_found
printer_corridor_files_found
reader_corridor_files_found
player_pc_corridor_files_found
physical_player_simulator_files_found
docs_files_found
tests_found
fixtures_found
release_files_found
possible_duplicate_schemas
package_manifest_candidates
update_event_candidates
print_export_candidates
reader_recovery_candidates
recommended_next_phase
physical_hardware_claimed
hardware_validation_claimed
physical_level_5_claimed
generated_output_tracked
local_path_leak_found
unsafe_hardware_claim_found
final_passed
```

Claim booleans should remain false:

```text
physical_hardware_claimed = false
hardware_validation_claimed = false
physical_level_5_claimed = false
manufactured_player_claimed = false
```

---

## 19. How Codex should record uncertainty

The audit must be honest.

If Codex cannot determine whether a module is active or stale, it should say:

```text
status: uncertain
reason: file exists but no tests/imports/docs found
```

Not:

```text
this is unused
```

unless proven.

Possible classification states:

```text
active
tested
documented
demo-only
docs-only
generated
historical
stale
uncertain
missing
```

This is important because the repo may contain older package/release artifacts.

---

## 20. How Codex should avoid over-reading generated output

The audit can inspect whether output folders exist, but should not treat generated output as canonical source.

Rule:

```text
Committed source/docs/tests define the repo baseline.
Generated output can be inspected for report shape, but should not be treated as source of truth unless the repo explicitly tracks it.
```

This follows the existing release review and package refresh pattern.

---

## 21. How Codex should handle .gitignore and ignored tests

The previous sequence repeatedly showed that test files may be hidden by `.gitignore`.

Future Codex runs should:

```text
- check git status --short
- check whether intended test files are ignored
- force-add only the intended test file if needed
- never force-add broad directories
- never commit __pycache__
- never commit output/
```

This should become standard.

---

## 22. The audit is not the implementation

Part 3 decides that the next major software step after the dossier should not immediately implement printer/reader/player modules.

It should first run a repo audit.

The audit should produce:

```text
- a map of existing software by corridor
- a map of existing schemas
- a list of gaps
- a list of reuse candidates
- a list of duplicate risks
- a recommended implementation order
```

Only after that should Codex implement the first software module.

---

## 23. What Part 3 decides

Part 3 decides:

```text
- repo discovery must precede implementation
- the audit should classify files by software corridor
- the audit must search for existing package/manifest/update-event structures
- the audit must search PC → Printer, PC ↔ Reader, and Player ↔ PC separately
- the audit must identify duplicate schema risks
- the audit must prefer adapt/wrap over create/replace
- generated output should not be treated as source of truth
- hardware-facing terms may be noted but not implemented
- uncertainty must be recorded honestly
- the first future Codex implementation after the dossier should likely be a repo-audit run, not runtime integration directly
```

---

## 24. What Part 4 should continue with

Part 4 should continue naturally into:

```text
Shared AMCF package, manifest, update-event, and section model requirements
```

That part should define the shared software objects that all corridors need before tool selection or implementation:

```text
AMCFPackage
AMCFManifest
AMCFUpdateEvent
AMCFPlaybackSchedule
AMCFPhysicalSection
AMCFPrintSection
AMCFReaderCapture
AMCFRecoveredSection
AMCFPlayerSection
AMCFValidationResult
AMCFReport
```

It should not yet pick final software libraries.

-----
# AMCF Software Development and I/O Control Dossier  
## Part 3 — Repo Audit, Discovery Strategy, Corridor Classification, and Schema-Control Method

## 1. Purpose of Part 3

Part 1 reset the dossier.

Part 2 defined the current baseline:

```text
- current repo = strong physical-player software/control checkpoint
- Player ↔ PC simulator/control path = most developed so far
- PC → Printer path = needs discovery and planning
- PC ↔ Reader path = needs discovery and planning
- shared AMCF package/manifest/update-event model = likely missing centre
```

Part 3 now defines how the repo should be audited before implementation.

This is important because the next Codex work must not blindly create new modules if the repo already has partial package, manifest, export, reader, printer, or report structures.

The audit needs to answer:

```text
What already exists?
What is duplicated?
What should be reused?
What should be adapted?
What is genuinely missing?
Which corridor does each file belong to?
What software schema already controls AMCF data?
```

This part is still not implementation.

It is the discovery method that should prevent bad implementation later.

---

## 2. Why repo discovery must come before coding

The new software dossier covers the full I/O software system:

```text
PC → Printer
PC ↔ Reader
Player ↔ PC
shared AMCF package / manifest / update-event model
```

The attached physical-player dossier already separates those concerns. It begins by distinguishing the earlier I/O scope — **PC → Printer**, **Reader → PC**, and **Player ↔ PC software recognition/control** — from the later physical-player object dossier. That means the software repo may already contain pieces from earlier I/O thinking, even if they were not part of the later physical-player work.

So Codex must not assume:

```text
there is no printer code
there is no reader code
there is no manifest schema
there is no package model
there is no export model
```

It must search first.

The rule for future Codex runs should be:

```text
Do not invent a new AMCF software structure until the existing repo structure has been audited.
```

---

## 3. Audit goal

The audit should produce a corridor map of the repo.

The corridor map should classify existing files into:

```text
A. Shared AMCF core
B. PC → Printer
C. PC ↔ Reader
D. Player ↔ PC
E. Physical-player simulator/control
F. Reports/logs/audits
G. Tests/fixtures
H. Docs/site/release tooling
I. Generated output / ignored artifacts
J. Unclear or duplicate structures
```

This is the first major software-development task after the dossier is complete.

Not implementation.

Discovery.

---

## 4. The three-corridor audit model

The audit should classify everything against the three main software corridors.

```text
Corridor 1 — PC → Printer
Corridor 2 — PC ↔ Reader
Corridor 3 — Player ↔ PC
```

But it also needs to recognise shared layers.

The full classification should be:

```text
Shared AMCF Core
    package, manifest, schema, update events, timing, validation

PC → Printer
    print layout, export, sheet/card/strip generation, lanes, manifests

PC ↔ Reader
    scanner/reader input, image capture, lane detection, recovery, validation

Player ↔ PC
    package transfer model, capability model, player reports, control protocol

Physical-Player Simulator
    current state machine, fail-closed, reverse/seek, mechanism profiles

Public/Release Infrastructure
    docs, site, release review, package refresh, closeout, tag prep

Tests/Fixtures
    deterministic examples, fixtures, regression tests
```

The physical-player simulator is related to Player ↔ PC, but should be kept as a sub-area because it already has a lot of implementation.

---

## 5. Search terms Codex should use

Codex should audit the repo using broad search terms.

The search should include exact filename and content searches.

Recommended search terms:

```text
manifest
package
export
AMCF
frame
frames
component
components
update
update_event
update event
timeline
schedule
timing
playback
section
sections
physical
print
printer
PDF
SVG
PNG
layout
sheet
card
strip
carrier
reader
scanner
scan
capture
image
lane
marker
registration
colour
color
hash
checksum
digest
report
audit
fixture
fixtures
demo
output
metadata
schema
```

It should also search for existing file prefixes:

```text
amcf_
physical_player
release
package
manifest
reader
printer
print
export
layout
recovery
playback
```

The audit should not only search Python files.

It should inspect:

```text
- src/
- demo/
- tests/
- docs/
- site/
- fixtures or examples if present
- release/package metadata files
- README and claim-boundary docs
- JSON manifests if present
- ignored output only for structure, not for committed source claims
```

---

## 6. What to discover in Shared AMCF Core

The shared AMCF core is the most important missing or partially hidden layer.

Codex should search for any existing object, schema, or convention for:

```text
AMCFPackage
AMCFManifest
AMCFUpdateEvent
AMCFVisibleState
AMCFComponent
AMCFFrame
AMCFTimeline
AMCFPlaybackSchedule
AMCFSection
AMCFPhysicalSection
AMCFValidationResult
AMCFReport
```

The audit should answer:

```text
Does the repo already have a package model?
Does it already have a manifest format?
Does it already store update events?
Does it store frames instead of update events?
Does it store components separately?
Does it already have hash/checksum conventions?
Does it already have report structures?
Are those structures documented?
Are they tested?
Are they used by demos?
```

The key discovery question:

```text
Is there one shared AMCF data model, or are there several partial models?
```

If several partial models exist, future work should adapt/unify rather than create yet another one.

---

## 7. What to discover for PC → Printer

For PC → Printer, Codex should search for software connected to:

```text
print
printer
layout
PDF
SVG
PNG
sheet
page
card
strip
carrier
registration
margin
DPI
colour calibration
hash lane
checksum lane
index lane
timing lane
print manifest
```

It should classify any file found into:

```text
- active print/export code
- prototype/demo code
- documentation only
- old/unused plan
- tests
- generated output
```

The audit should answer:

```text
Is there already a print/export pipeline?
If yes, what does it output?
Does it output normal images or structured AMCF physical sections?
Does it have layout tests?
Does it encode timing/index/hash lanes?
Does it produce a print manifest?
Does it support reprint of damaged sections?
Does it fit dynamic AMCF update events?
```

Important: the printer path should not be assumed to mean “print every frame.”

The physical-player plan says the player follows AMCF update events rather than fixed-FPS page movement. So the print audit must check whether print/export code is update-event-based or frame-based.

---

## 8. What to discover for PC ↔ Reader

For PC ↔ Reader, Codex should search for:

```text
reader
scanner
scan
capture
image
input
camera
CIS
line sensor
lane
marker
registration
alignment
colour
color
hash
checksum
OCR
barcode
QR
recovery
reconstruct
damage
rescan
```

The physical-player plan says the prefetch reader lane needs to read section index, timing marks, registration marks, colour registry/reference, metadata/transform lane, hash/checksum lane, and damage/missing-marker status. That gives the reader audit a checklist.

The audit should answer:

```text
Is there reader/recovery software already?
Does it accept real scanner input?
Does it accept image-folder input?
Does it have fixture images?
Does it detect section boundaries?
Does it detect lanes?
Does it validate hashes/checksums?
Does it reconstruct AMCF packages?
Does it generate reader audit reports?
Does it separate reader/recovery from player-prefetch?
```

The distinction matters because the physical-player plan explicitly separates reader/scanner recovery from physical-player direct presentation. So the audit should flag if the repo conflates:

```text
reader/recovery scan gate
```

with:

```text
player visible view gate
```

Those should be related but not identical.

---

## 9. What to discover for Player ↔ PC

For Player ↔ PC, Codex should search for:

```text
player
physical_player
state_machine
mechanism
profile
capability
cartridge
manifest
control
command
protocol
diagnostic
log
report
fail_closed
reverse
seek
audio_sync
prefetch
view_gate
hidden_gate
```

This is the corridor with the most known completed work.

The audit should distinguish:

```text
already implemented:
- simulator state machine
- fail-closed
- reverse/seek
- mechanism profiles
- integrated reports

not yet implemented:
- real device detection
- real protocol
- real hardware communication
- real player firmware bridge
```

Future Player ↔ PC software should not jump to hardware protocol first.

It should likely move next into:

```text
AMCF package/manifest → physical-player runtime simulator
```

But Part 3 still only defines discovery.

---

## 10. What to discover for reports, logs, and audits

The repo already has a strong pattern of deterministic reports.

Codex should search for:

```text
report
audit
summary
scan
claim_boundary
unsafe_acceptance
final_passed
generated_output
local_path
hardware_claim
```

The audit should identify existing report conventions:

```text
- JSON report shape
- Markdown summary shape
- output folder convention
- final_passed booleans
- unsafe_acceptance_count fields
- claim-boundary booleans
- generated-output policy fields
```

This matters because future PC → Printer and PC ↔ Reader tools should reuse the same reporting style.

For example, future printer reports should probably include:

```text
final_passed
print_layout_valid
section_count
lane_count
hash_lane_present
registration_marks_present
generated_output_committed false
hardware_validation_claimed false
```

Future reader reports should probably include:

```text
final_passed
sections_detected
lanes_detected
hashes_verified
damaged_sections
recovery_passed
generated_output_committed false
hardware_validation_claimed false
```

---

## 11. What to discover for tests and fixtures

Codex should search for:

```text
fixtures
fixture
sample
example
testdata
golden
expected
input
output
```

The audit should answer:

```text
Are there existing AMCF package fixtures?
Are there existing manifest fixtures?
Are there image fixtures?
Are there print-layout fixtures?
Are there player-section fixtures?
Are there release-review fixtures?
Where do tests expect fixture files to live?
Are tests ignored by .gitignore and require force-add?
```

The current workflow repeatedly encountered broad ignore rules around tests. Future Codex prompts need to know that test files may require force-add.

That should become part of the software implementation method.

---

## 12. What to discover for docs and public site

Codex should search docs/site for the software public surface.

Important files:

```text
README.md
CLAIM_BOUNDARIES.md
docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md
docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md
docs/AMCF_HARDWARE_SOFTWARE_PATHS.md
site/index.html
```

The audit should answer:

```text
Where should future software docs be linked?
Is there already a docs map pattern?
Is there already a public summary pattern?
How should new software/I/O docs be linked without bloating README?
Does site/index.html have a section where software docs belong?
```

Future software docs should probably become their own map:

```text
docs/AMCF_SOFTWARE_IO_CONTROL_DOCS_MAP.md
```

But this should be decided after the audit.

---

## 13. What to discover for release/package tooling

Codex should inspect:

```text
RELEASE_MANIFEST.json
PACKAGE_MANIFEST.md
MANIFEST.md
RELEASE_NOTES.md
CHANGELOG.md
PUBLICATION_STATUS.md
docs/AMCF_PUBLIC_RELEASE_PACKAGE_INVENTORY.md
docs/AMCF_PUBLIC_RELEASE_TAG_PREP.md
```

The audit should answer:

```text
What release/package metadata exists?
Is it current or historical?
Does it include the new physical-player docs?
Does it include future software/I/O docs?
Should it be updated only after implementation phases?
```

Part 2 already noted that older release metadata may exist and should not be rewritten blindly.

The audit should classify release files as:

```text
current
historical
generated
manual
stale-but-preserved
needs later refresh
```

---

## 14. Duplicate schema detection

One of the biggest risks is duplicate schema creation.

Codex should detect whether the repo already has multiple ways to represent:

```text
manifest
package
update event
timeline
section
physical section
player section
print section
reader recovered section
report
```

The audit should flag possible duplicates.

Example duplicate risk:

```text
AMCFUpdateEvent in one module
update_event dict in another module
timeline_event in a third module
physical_section timing fields in another module
```

The goal is not to immediately merge them.

The goal is to identify them and decide:

```text
reuse
adapt
wrap
deprecate later
leave separate
```

Do not create new schemas until this is done.

---

## 15. Adapt versus create rule

Future implementation should follow this rule:

```text
Adapt existing models if they already express the needed concept.
Create new models only when no existing model covers the need cleanly.
```

Decision method:

```text
1. Search existing code.
2. Identify candidate models.
3. Check tests/demos using them.
4. Check docs describing them.
5. Decide if they are active and stable.
6. Prefer adapter/wrapper over replacement.
7. Only create new canonical structure if existing structures are missing or clearly insufficient.
```

This prevents the repo from accumulating disconnected AMCF package formats.

---

## 16. No-hardware discovery boundary

The audit can search for hardware-facing references, but it should not create hardware code.

It can classify future hardware terms:

```text
USB
serial
HID
scanner
printer
device
firmware
driver
sensor
motor
```

But first implementation should stay in:

```text
simulated input
file-based fixtures
JSON reports
deterministic demos
```

No real hardware APIs should be introduced unless a later dossier part explicitly justifies them.

The physical-player plan itself makes clear that physical proof remains unclaimed and that Level 5 future hardware is not achieved. So audit can prepare for hardware, but implementation should not jump there.

---

## 17. Expected audit output later

When Codex eventually performs this audit, it should produce a report.

Suggested future file:

```text
docs/AMCF_SOFTWARE_IO_REPO_AUDIT.md
```

Suggested future script:

```text
demo/run_amcf_software_io_repo_audit.py
```

Suggested output folder:

```text
output/amcf_software_io_repo_audit/
```

Suggested output files:

```text
software_io_repo_audit_report.json
corridor_file_map.json
schema_discovery_report.json
printer_path_discovery.json
reader_path_discovery.json
player_pc_discovery.json
release_docs_discovery.json
SOFTWARE_IO_REPO_AUDIT_SUMMARY.md
```

Generated output should not be committed.

---

## 18. Expected audit report fields

The future audit report should include:

```text
run_name
current_head
current_branch
tag_status
shared_core_files_found
printer_corridor_files_found
reader_corridor_files_found
player_pc_corridor_files_found
physical_player_simulator_files_found
docs_files_found
tests_found
fixtures_found
release_files_found
possible_duplicate_schemas
package_manifest_candidates
update_event_candidates
print_export_candidates
reader_recovery_candidates
recommended_next_phase
physical_hardware_claimed
hardware_validation_claimed
physical_level_5_claimed
generated_output_tracked
local_path_leak_found
unsafe_hardware_claim_found
final_passed
```

Claim booleans should remain false:

```text
physical_hardware_claimed = false
hardware_validation_claimed = false
physical_level_5_claimed = false
manufactured_player_claimed = false
```

---

## 19. How Codex should record uncertainty

The audit must be honest.

If Codex cannot determine whether a module is active or stale, it should say:

```text
status: uncertain
reason: file exists but no tests/imports/docs found
```

Not:

```text
this is unused
```

unless proven.

Possible classification states:

```text
active
tested
documented
demo-only
docs-only
generated
historical
stale
uncertain
missing
```

This is important because the repo may contain older package/release artifacts.

---

## 20. How Codex should avoid over-reading generated output

The audit can inspect whether output folders exist, but should not treat generated output as canonical source.

Rule:

```text
Committed source/docs/tests define the repo baseline.
Generated output can be inspected for report shape, but should not be treated as source of truth unless the repo explicitly tracks it.
```

This follows the existing release review and package refresh pattern.

---

## 21. How Codex should handle .gitignore and ignored tests

The previous sequence repeatedly showed that test files may be hidden by `.gitignore`.

Future Codex runs should:

```text
- check git status --short
- check whether intended test files are ignored
- force-add only the intended test file if needed
- never force-add broad directories
- never commit __pycache__
- never commit output/
```

This should become standard.

---

## 22. The audit is not the implementation

Part 3 decides that the next major software step after the dossier should not immediately implement printer/reader/player modules.

It should first run a repo audit.

The audit should produce:

```text
- a map of existing software by corridor
- a map of existing schemas
- a list of gaps
- a list of reuse candidates
- a list of duplicate risks
- a recommended implementation order
```

Only after that should Codex implement the first software module.

---

## 23. What Part 3 decides

Part 3 decides:

```text
- repo discovery must precede implementation
- the audit should classify files by software corridor
- the audit must search for existing package/manifest/update-event structures
- the audit must search PC → Printer, PC ↔ Reader, and Player ↔ PC separately
- the audit must identify duplicate schema risks
- the audit must prefer adapt/wrap over create/replace
- generated output should not be treated as source of truth
- hardware-facing terms may be noted but not implemented
- uncertainty must be recorded honestly
- the first future Codex implementation after the dossier should likely be a repo-audit run, not runtime integration directly
```

---

## 24. What Part 4 should continue with

Part 4 should continue naturally into:

```text
Shared AMCF package, manifest, update-event, and section model requirements
```

That part should define the shared software objects that all corridors need before tool selection or implementation:

```text
AMCFPackage
AMCFManifest
AMCFUpdateEvent
AMCFPlaybackSchedule
AMCFPhysicalSection
AMCFPrintSection
AMCFReaderCapture
AMCFRecoveredSection
AMCFPlayerSection
AMCFValidationResult
AMCFReport
```

It should not yet pick final software libraries.

----
# AMCF Software Development and I/O Control Dossier  
## Part 4 — Shared AMCF Package, Manifest, Update-Event, and Section Model Requirements

## 1. Purpose of Part 4

Part 3 defined the repo-audit method.

Part 4 now defines the **shared software model** that the repo audit should look for, protect, adapt, or create.

This is the centre of the software system.

The three I/O corridors all depend on it:

```text
PC → Printer
PC ↔ Reader
Player ↔ PC
```

If each corridor invents its own data format, the AMCF software will fragment.

So Part 4 asks:

```text
What shared package, manifest, update-event, section, validation, and report objects does AMCF need so printer, reader, player, simulator, tests, and future hardware can all speak the same language?
```

This part does not implement the schema yet.

It defines what the schema must support.

---

## 2. Why the shared model matters

The physical-player plan already defines the chain:

```text
Digital AMCF
→ AMCF schedule / update events
→ physical AMCF carrier
→ physical player transport
→ physical/optical viewing window
```

The software version of that chain must become:

```text
AMCF source/package
→ AMCF manifest
→ AMCF update-event schedule
→ printable/recoverable/player section records
→ validation and report objects
```

The player design requires physical-section update events, dwell duration, preload deadline, transition blank duration, and optical presentation timing. So the software model must not be only:

```text
frame_000001.png
frame_000002.png
frame_000003.png
```

It needs richer AMCF event data.

The physical-player plan even gives an example event with:

```text
timestamp_ms
visible_section
next_section
dwell_ms
preload_required_by_ms
transition_blank_ms
requires_verified_next_section
```

That gives us a direct starting point for shared model requirements. ---

## 3. Core principle: update events are first-class

The shared AMCF model should be built around:

```text
AMCF update events
```

not only:

```text
video frames
```

Frames may still exist as source references, preview frames, or fallback data.

But AMCF physical output should be driven by:

```text
when visible state changes
what section becomes visible
what section is next
how long it dwells
what must be prefetched
what must be verified
what happens if verification fails
```

The physical-player plan states that physical AMCF follows source timing into physical section update events, view-gate dwell duration, and optical presentation timing, and that the physical transport follows the dynamic schedule rather than constant FPS movement. So the shared software schema must make this impossible to lose.

---

## 4. Required shared objects

The shared AMCF software model should eventually define or discover these object categories:

```text
AMCFPackage
AMCFManifest
AMCFAsset
AMCFSourceReference
AMCFPlaybackSchedule
AMCFUpdateEvent
AMCFVisibleState
AMCFComponentState
AMCFPhysicalSection
AMCFPrintSection
AMCFReaderCapture
AMCFRecoveredSection
AMCFPlayerSection
AMCFValidationResult
AMCFFailClosedDecision
AMCFReverseSeekState
AMCFMechanismProfileReference
AMCFReport
```

These do not all have to become Python classes immediately.

Some may begin as dictionaries or JSON schema-like conventions.

But the software dossier should treat them as distinct concepts.

---

## 5. AMCFPackage

## 5.1 Purpose

`AMCFPackage` is the outer container.

It should answer:

```text
What AMCF item is this?
What files/assets/manifests belong to it?
What schema version is it?
What software produced it?
What can it be used for?
```

It should be usable by:

```text
- digital playback
- PC → Printer export
- PC ↔ Reader recovery
- Player ↔ PC simulation/control
- release/package verification
```

## 5.2 Required fields

A package should eventually expose:

```text
package_id
package_schema_version
created_by
created_at
source_media_reference
manifest_path
assets
reports
hashes
claim_boundary_metadata
compatibility_metadata
```

## 5.3 Why it matters

Without a package object, each corridor will ask for different inputs.

The printer will want one layout source.

The reader will output something else.

The player simulator will accept another structure.

That must be avoided.

The package is the top-level shared container.

---

## 6. AMCFManifest

## 6.1 Purpose

`AMCFManifest` is the structured description of the AMCF content.

It should answer:

```text
What does this package contain?
What is the playback schedule?
What sections exist?
What assets do they reference?
What hashes/validation data apply?
What outputs are allowed?
```

The manifest is more important than any individual file.

## 6.2 Required fields

A manifest should eventually expose:

```text
manifest_id
manifest_schema_version
package_id
source_duration_ms
timebase
update_events
visible_states
sections
assets
validation
print_profile_refs
reader_profile_refs
player_profile_refs
reports
```

## 6.3 Manifest should support all corridors

```text
PC → Printer:
uses manifest to decide what physical sections to print.

PC ↔ Reader:
uses manifest to verify/recover physical sections.

Player ↔ PC:
uses manifest to schedule playback and validate player capability.
```

So the manifest is not just a metadata file.

It is the shared software contract.

---

## 7. AMCFPlaybackSchedule

## 7.1 Purpose

`AMCFPlaybackSchedule` is the ordered timing structure.

It should answer:

```text
What happens at each AMCF update timestamp?
```

It should not be merely a frame list.

It should represent the AMCF dynamic schedule.

## 7.2 Required fields

```text
schedule_id
timebase
source_duration_ms
events
event_count
min_event_spacing_ms
max_event_spacing_ms
average_event_spacing_ms
static_hold_ranges
high_motion_ranges
audio_sync_reference
```

## 7.3 Why not frame-only

The physical plan is clear that AMCF physical transport should not chase constant FPS movement, but should follow component/update events and reconstruction timing. So the playback schedule should be event-based.

A frame list can be derived from it if needed, but should not replace it.

---

## 8. AMCFUpdateEvent

## 8.1 Purpose

`AMCFUpdateEvent` is the central object.

It says:

```text
At this time, this visible AMCF state or physical section must become visible.
```

The physical-player plan’s example event already points to the needed software shape:

```text
timestamp_ms
visible_section
next_section
dwell_ms
preload_required_by_ms
transition_blank_ms
requires_verified_next_section
```

The plan explicitly uses those fields in its event example. ## 8.2 Required fields

A software update event should eventually include:

```text
event_id
event_index
timestamp_ms
visible_state_id
visible_section_id
next_section_id
previous_section_id
dwell_ms
preload_required_by_ms
verification_deadline_ms
transition_blank_ms
requires_verified_next_section
audio_sync_tolerance_ms
event_source
metadata
```

## 8.3 Event source

`event_source` should identify why the event exists:

```text
component_change
full_visible_state_change
timing_boundary
manual_marker
reader_recovery_marker
print_section_boundary
player_runtime_boundary
```

This matters because not every event is the same kind of update.

Some may be visual.

Some may be physical-carrier boundaries.

Some may be recovery or diagnostic boundaries.

---

## 9. AMCFVisibleState

## 9.1 Purpose

`AMCFVisibleState` represents what should be visible at a given time.

It is not necessarily the same thing as a physical section.

A visible state is the logical image state.

A physical section is how that state is represented physically.

## 9.2 Required fields

```text
visible_state_id
state_index
timestamp_start_ms
timestamp_end_ms
duration_ms
component_refs
composited_asset_ref
source_frame_refs
section_refs
hash
metadata
```

## 9.3 Why this distinction matters

The physical-player plan leaves open whether AMCF is represented as precomposited physical sections or more advanced layer/component physical systems.

So the software should distinguish:

```text
logical visible state
```

from:

```text
physical section
```

A simple first implementation can map:

```text
one visible state → one physical section
```

But the model should not prevent future:

```text
one visible state → multiple physical component layers
```

---

## 10. AMCFComponentState

## 10.1 Purpose

`AMCFComponentState` represents component-level AMCF logic.

This matters because AMCF is not just ordinary video frame playback.

Even if early physical output uses precomposited sections, software should not erase the component model.

## 10.2 Required fields

```text
component_id
component_type
active_from_ms
active_to_ms
asset_ref
transform
opacity_or_mask
z_order
hash
metadata
```

## 10.3 Use by corridors

```text
PC → Printer:
may precompose components into physical sections.

PC ↔ Reader:
may recover component metadata lanes if printed.

Player ↔ PC:
may later support component-aware physical sections or layered mechanisms.
```

Component support should be part of the shared model, even if early implementation uses precomposited physical states.

---

## 11. AMCFPhysicalSection

## 11.1 Purpose

`AMCFPhysicalSection` is the abstract physical-unit record.

It should answer:

```text
What physical AMCF section exists, what visible state does it represent, when is it used, and how is it verified?
```

This is the object that links printer, reader, and player software.

## 11.2 Required fields

```text
section_id
section_index
carrier_id
visible_state_id
event_id
timestamp_start_ms
timestamp_end_ms
dwell_ms
payload_ref
section_hash
metadata_hash
expected_hash_status
timing_lane
registration_lane
colour_reference_lane
metadata_lane
hash_checksum_lane
damage_status
display_eligibility
```

## 11.3 Section lanes

The physical-player plan says the prefetch lane should read section index, timing marks, registration marks, colour registry/reference, metadata/transform lane, hash/checksum lane, and damage/missing marker status. So the shared section object must include lane concepts.

Those lanes are not only hardware ideas.

They are software validation fields.

---

## 12. AMCFPrintSection

## 12.1 Purpose

`AMCFPrintSection` is the printer-facing version of a physical section.

It should answer:

```text
How should this section be laid out for printing?
```

It should reference `AMCFPhysicalSection`, not replace it.

## 12.2 Required fields

```text
print_section_id
physical_section_id
print_sheet_id
page_index
position_on_page
section_bounds
payload_bounds
timing_lane_bounds
registration_lane_bounds
colour_reference_bounds
metadata_lane_bounds
hash_lane_bounds
printer_margin_status
dpi
units
export_asset_refs
```

## 12.3 Why print sections are separate

A physical section is the logical physical unit.

A print section is its print layout representation.

This distinction allows:

```text
same physical section
→ printed on sheet
→ printed as card
→ printed on strip
→ printed as cartridge insert
```

without redefining the AMCF section itself.

---

## 13. AMCFReaderCapture

## 13.1 Purpose

`AMCFReaderCapture` represents what the reader/scanner captured.

It should answer:

```text
What raw input did the reader capture, under what settings, and what section might it contain?
```

## 13.2 Required fields

```text
capture_id
capture_source
capture_mode
captured_at
image_ref
dpi_or_resolution
colour_mode
calibration_ref
candidate_section_id
detected_bounds
detected_lanes
reader_profile_id
metadata
```

## 13.3 Reader capture should be no-hardware first

The first implementation should accept:

```text
fixture image
image folder
generated print output
simulated reader capture
```

Real hardware capture can come later.

---

## 14. AMCFRecoveredSection

## 14.1 Purpose

`AMCFRecoveredSection` is the reader-derived reconstruction of a physical section.

It should answer:

```text
What did the reader recover from this captured physical section?
```

## 14.2 Required fields

```text
recovered_section_id
capture_id
physical_section_id_candidate
section_index_detected
timing_lane_result
registration_lane_result
colour_reference_result
metadata_lane_result
hash_checksum_result
payload_recovery_result
damage_status
confidence
requires_rescan
recovery_status
```

## 14.3 Reader decisions

Reader recovery should be able to say:

```text
valid
valid_with_warning
requires_rescan
unrecoverable
wrong_section
hash_mismatch
registration_failed
metadata_corrupt
```

The physical-player plan says the prefetch lane should decide whether the section is correct, in expected order, aligned enough, hash-valid, colour degraded but usable, safe to display, or should cause continue/rescan/skip/pause/fail-closed. The PC reader can use similar decision fields, but for recovery rather than immediate display.

---

## 15. AMCFPlayerSection

## 15.1 Purpose

`AMCFPlayerSection` is the player-facing runtime version of a physical section.

It should answer:

```text
Can this section be safely staged, displayed, parked, reversed to, or denied?
```

## 15.2 Required fields

```text
player_section_id
physical_section_id
section_index
event_id
visible_state_id
timestamp_start_ms
dwell_ms
preload_required_by_ms
verification_deadline_ms
transition_blank_ms
verified_before_display
gate_lock_required
display_allowed
prefetch_status
staging_status
reverse_buffer_eligible
seek_eligible
fail_closed_reason
metadata
```

## 15.3 Why this is separate from AMCFPhysicalSection

The same physical section may have different runtime states.

Example:

```text
Physical section section_00041 exists.

At runtime:
- it may be prefetched
- verified
- staged
- visible
- parked
- reverse-buffered
- denied
- failed closed
```

So `AMCFPlayerSection` is the runtime state wrapper.

---

## 16. AMCFValidationResult

## 16.1 Purpose

`AMCFValidationResult` is the generic validation object shared by all corridors.

It should answer:

```text
Did this thing pass validation, fail validation, or pass with warning?
```

## 16.2 Required fields

```text
validation_id
target_type
target_id
passed
severity
status
reasons
warnings
errors
checked_at
checker
metadata
```

## 16.3 Status values

Recommended statuses:

```text
passed
passed_with_warning
failed
requires_rescan
requires_reprint
requires_manual_review
not_checked
```

## 16.4 Severity values

```text
info
warning
recoverable_error
critical_error
fail_closed
```

This should be shared by printer, reader, and player tools.

---

## 17. AMCFFailClosedDecision

## 17.1 Purpose

`AMCFFailClosedDecision` records why software refused an unsafe action.

This is essential because the physical-player model repeatedly depends on fail-closed behaviour.

The physical-player dossier explicitly preserves the rule that `unsafe_acceptance_count` must remain zero. ## 17.2 Required fields

```text
decision_id
target_type
target_id
action_requested
allowed
fail_closed
reason_code
reason_text
critical_lane
recovery_action
display_blank_required
rescan_allowed
reprint_allowed
manual_review_required
metadata
```

## 17.3 Reason codes

Potential reason codes:

```text
missing_section
wrong_section_index
hash_mismatch
metadata_hash_mismatch
registration_failed
colour_reference_unusable
timing_lane_unreadable
marker_missing
prefetch_timeout
gate_not_locked
reverse_buffer_miss
arbitrary_seek_denied
audio_sync_exceeded
unknown_critical_state
```

Reason codes should be shared.

Printer, reader, and player software should not invent incompatible failure labels.

---

## 18. AMCFReverseSeekState

## 18.1 Purpose

`AMCFReverseSeekState` records what reverse/seek operations are allowed.

The physical-player design prefers limited reverse/short step-back through a reverse buffer, not arbitrary instant seek across the whole cartridge.

So the shared model needs reverse/seek constraints.

## 18.2 Required fields

```text
reverse_seek_state_id
current_section_id
reverse_buffer_section_ids
local_seek_section_ids
requested_target_section_id
requested_operation
allowed
denial_reason
buffer_depth
arbitrary_seek_allowed
metadata
```

## 18.3 Required rule

The default should be:

```text
arbitrary_seek_allowed = false
```

until later research proves a mechanism/profile supports more.

---

## 19. AMCFMechanismProfileReference

## 19.1 Purpose

`AMCFMechanismProfileReference` connects package/runtime decisions to mechanism assumptions.

The existing default profile is:

```text
folded_ab_motor_encoder_baseline
```

But package compatibility may eventually depend on mechanism capability.

## 19.2 Required fields

```text
profile_id
profile_version
carrier_layout
staging_model
actuator_family
gate_model
prefetch_model
reverse_model
seek_model
safety_model
hardware_validated
physical_level_5_claimed
metadata
```

## 19.3 Required boundary

For now:

```text
hardware_validated = false
physical_level_5_claimed = false
```

This preserves the claim boundary.

---

## 20. AMCFReport

## 20.1 Purpose

`AMCFReport` is the shared report structure.

It should unify the existing pattern from physical-player demos, release reviews, package refresh, closeout, and tag prep.

## 20.2 Required fields

```text
report_id
run_name
created_at
input_refs
output_refs
final_passed
summary
counts
validation_results
fail_closed_decisions
unsafe_acceptance_count
claim_boundary_flags
generated_output_status
local_path_scan_status
unsafe_hardware_claim_scan_status
metadata
```

## 20.3 Report must support all corridors

```text
PC → Printer:
print layout report, print manifest report, reprint report.

PC ↔ Reader:
reader capture report, recovery report, lane-detection report.

Player ↔ PC:
runtime playback report, fail-closed report, reverse/seek report.

Shared:
repo audit report, package validation report, release review report.
```

The existing physical-player tooling already depends on report-style summaries. The software model should standardize that pattern.

---

## 21. Package-to-corridor object flow

The shared model should allow this flow:

```text
AMCFPackage
→ AMCFManifest
→ AMCFPlaybackSchedule
→ AMCFUpdateEvent
→ AMCFVisibleState
→ AMCFPhysicalSection
```

Then corridor-specific views:

```text
AMCFPhysicalSection
→ AMCFPrintSection
→ printed carrier

AMCFPhysicalSection
→ AMCFReaderCapture
→ AMCFRecoveredSection

AMCFPhysicalSection
→ AMCFPlayerSection
→ runtime playback state
```

Then shared results:

```text
AMCFValidationResult
AMCFFailClosedDecision
AMCFReport
```

This keeps the system coherent.

---

## 22. Printer corridor model flow

PC → Printer should eventually use:

```text
AMCFPackage
→ AMCFManifest
→ AMCFPlaybackSchedule
→ AMCFUpdateEvent
→ AMCFPhysicalSection
→ AMCFPrintSection
→ PrintExport
→ PrintReport
```

The printer should not invent section timing independently.

It should use manifest/update-event timing.

The print path should know:

```text
which sections exist
where they print
which marks/lane data they carry
which hashes/checksums protect them
how they map back to the manifest
```

---

## 23. Reader corridor model flow

PC ↔ Reader should eventually use:

```text
AMCFManifest
+ ReaderCapture
→ RecoveredSection
→ ValidationResult
→ RecoveredPackage or ReaderReport
```

Reader recovery should be able to compare:

```text
expected section from manifest
vs
detected section from capture
```

It should be able to report:

```text
correct
wrong section
damaged
hash mismatch
registration failed
requires rescan
unrecoverable
```

This reader path should remain distinct from player visible playback.

The physical-player plan separates scan/recovery from physical-player direct presentation, so the software should preserve that separation. ---

## 24. Player corridor model flow

Player ↔ PC should eventually use:

```text
AMCFPackage
→ AMCFManifest
→ AMCFPlaybackSchedule
→ AMCFPlayerSection list
→ state-machine execution
→ playback report
```

At runtime, the player model should decide the same things listed in the physical-player plan:

```text
Can I execute this update safely?
Is the next section ready?
Is it verified?
Is the A/B gate ready?
Is audio sync acceptable?
Should I continue, pause, or fail closed?
```

Those questions are directly listed in the plan after the sample event. So the shared model must carry enough information for those decisions.

---

## 25. Required timing fields

Every relevant schedule/event/section object should support consistent timing fields.

Recommended common timing fields:

```text
timestamp_start_ms
timestamp_end_ms
duration_ms
dwell_ms
preload_start_ms
preload_required_by_ms
verification_deadline_ms
transition_blank_ms
reader_prefetch_ahead_ms
gate_lock_timeout_ms
audio_sync_tolerance_ms
```

Not every object needs every field.

But field names should be consistent.

Do not allow one module to call it:

```text
start
```

another:

```text
time_ms
```

another:

```text
event_timestamp
```

unless there is a clear adapter.

Consistent naming reduces confusion.

---

## 26. Required identity fields

AMCF software should have stable identifiers.

Recommended ID fields:

```text
package_id
manifest_id
schedule_id
event_id
visible_state_id
component_id
section_id
print_section_id
capture_id
recovered_section_id
player_section_id
report_id
```

IDs should be deterministic where possible.

For tests and fixtures, deterministic IDs are important.

A package should be able to trace:

```text
event_id
→ visible_state_id
→ physical_section_id
→ print_section_id / recovered_section_id / player_section_id
```

Traceability is essential for debugging.

---

## 27. Required hash/checksum fields

Hash/checksum must be modeled centrally.

The physical-player plan says the hash/checksum lane protects section identity, payload integrity, metadata integrity, lane corruption detection, and fail-closed safety. So shared fields should include:

```text
payload_hash
metadata_hash
section_hash
manifest_hash
expected_hash
observed_hash
hash_algorithm
hash_status
checksum_status
```

Recommended statuses:

```text
not_checked
match
mismatch
missing
unreadable
degraded
not_required
```

A hash mismatch should never be silently accepted.

---

## 28. Required lane fields

The shared model should support lanes.

Core lane categories:

```text
timing_index_lane
registration_lane
colour_reference_lane
metadata_transform_lane
hash_checksum_lane
payload_area
service_debug_marks
```

These come from the physical-player plan’s section/prefetch requirements: section index, timing, registration, colour reference, metadata/transform, hash/checksum, and damage/missing marker status. Lane fields should be abstract.

The first software model does not need to decide final barcode/QR/custom mark design.

It just needs to preserve the lane concepts.

---

## 29. Required validation statuses

Validation statuses should be shared.

Recommended statuses:

```text
valid
valid_with_warning
invalid
missing
unreadable
degraded
requires_rescan
requires_reprint
fail_closed
not_checked
```

Do not let each corridor invent separate names like:

```text
ok
good
pass
clean
safe
```

without mapping them.

Shared statuses make reports comparable.

---

## 30. Required claim-boundary fields

Every public-facing report should include claim-boundary booleans.

Required fields:

```text
physical_hardware_claimed
hardware_validation_claimed
physical_level_5_claimed
manufactured_player_claimed
real_sensors_required
real_motors_required
real_cartridges_required
real_scans_required
```

Default values for current software:

```text
false
```

This keeps future tools aligned with the existing physical-player public-release boundary.

---

## 31. Required unsafe-acceptance field

The shared report model should include:

```text
unsafe_acceptance_count
```

It should remain:

```text
0
```

The physical-player plan explicitly says the simulator must preserve `unsafe_acceptance_count` at zero. This should not be only a player-simulator field.

It should apply across corridors:

```text
PC → Printer:
unsafe print package accepted = bad.

PC ↔ Reader:
corrupt section accepted as valid = bad.

Player ↔ PC:
unverified section displayed = bad.
```

---

## 32. Schema versioning

The shared model should include schema versions.

Minimum version fields:

```text
package_schema_version
manifest_schema_version
event_schema_version
section_schema_version
report_schema_version
```

Why:

```text
AMCF will evolve.
Printer/reader/player software must know which format they are handling.
```

Do not rely only on file names.

Put schema version in the data.

---

## 33. Backward compatibility rule

The first formal schema does not need to be perfect.

But it should be versioned so later changes are manageable.

Rule:

```text
Add fields in a backward-compatible way where possible.
Do not silently reinterpret old fields.
When behaviour changes, bump schema version.
```

This matters for physical print/recovery, because old printed carriers may later be read by newer software.

---

## 34. JSON as first shared format

For the first implementation, the shared manifest/report format should likely remain:

```text
JSON
```

Reason:

```text
- current repo appears to use JSON reports
- standard library support
- easy tests
- easy diffing
- good for Codex-generated fixtures
- no new dependency required
```

This does not prevent later formats.

Possible future formats:

```text
CBOR
SQLite
binary package bundle
ZIP package
```

But the first shared model should stay simple and inspectable.

---

## 35. Object relationship summary

The shared model should be understood like this:

```text
AMCFPackage
  contains AMCFManifest

AMCFManifest
  contains AMCFPlaybackSchedule
  contains AMCFVisibleState records
  contains AMCFPhysicalSection records
  references assets and reports

AMCFPlaybackSchedule
  contains AMCFUpdateEvent records

AMCFUpdateEvent
  references visible state
  references current/next physical section
  defines timing/deadline/blanking requirements

AMCFPhysicalSection
  represents the abstract physical unit

AMCFPrintSection
  represents layout/export of that physical unit

AMCFReaderCapture
  represents captured input from reader/scanner/fixture

AMCFRecoveredSection
  represents reader reconstruction of a physical section

AMCFPlayerSection
  represents runtime player state for a physical section

AMCFValidationResult
  records checks across all corridors

AMCFFailClosedDecision
  records denied unsafe actions

AMCFReport
  summarizes outputs, counts, safety, and claim boundaries
```

---

## 36. What should not happen

Avoid this:

```text
printer_manifest.json has one structure
reader_manifest.json has another structure
player_manifest.json has a third structure
release_manifest.json uses unrelated names
tests create a fifth fixture format
```

Instead:

```text
one shared AMCF manifest model
corridor-specific views/adapters
shared validation/report vocabulary
```

---

## 37. What Part 4 decides

Part 4 decides:

```text
- the shared AMCF model is the centre of the software system
- AMCF update events must be first-class
- frames alone are not enough
- printer, reader, and player software should use the same package/manifest/update-event model
- physical sections should be abstract shared records
- print sections, recovered sections, and player sections should be corridor-specific views
- validation, fail-closed decisions, report fields, claim-boundary fields, and unsafe_acceptance_count should be shared
- JSON is the safest first shared interchange format unless the repo audit proves another active format already exists
- schema versioning is required from the start
- Codex must audit existing repo schemas before creating new ones
```

---

## 38. What Part 5 should continue with

Part 5 should continue naturally into:

```text
Software stack research and selection criteria
```

It should not pick tools casually.

It should define how to choose software for:

```text
- core runtime/language
- CLI
- desktop UI
- local web UI
- JSON/schema handling
- print/PDF/SVG/PNG generation
- reader/image processing
- marker/lane detection
- device communication
- testing
- reporting
- packaging/release
```

----
# AMCF Software Development and I/O Control Dossier  
## Part 5 — Software Stack Research Method, Selection Criteria, Dependency Policy, and Tooling Boundaries

## 1. Purpose of Part 5

Part 4 defined the shared AMCF software model:

```text
AMCFPackage
AMCFManifest
AMCFPlaybackSchedule
AMCFUpdateEvent
AMCFPhysicalSection
AMCFPrintSection
AMCFReaderCapture
AMCFRecoveredSection
AMCFPlayerSection
AMCFValidationResult
AMCFFailClosedDecision
AMCFReport
```

Part 5 now defines how software choices should be researched and selected.

This part should not simply list random libraries.

It should answer:

```text
How do we decide what software stack AMCF should use?
Which parts should stay Python/standard-library?
Which parts may need dependencies later?
Which parts should stay simulated until hardware exists?
Which tools fit PC → Printer?
Which tools fit PC ↔ Reader?
Which tools fit Player ↔ PC?
How do we avoid overbuilding?
How do we avoid dependency mess?
How do we keep everything testable, offline, Windows-friendly, and Codex-friendly?
```

The software choices must serve the AMCF model, not replace it.

The physical-player plan already established that AMCF’s software/control chain must respect dynamic update events, verification, physical-section timing, and fail-closed logic rather than ordinary fixed-FPS page flipping. So the software stack should be chosen around:

```text
data correctness
deterministic reports
testability
print/recovery/player integration
future hardware compatibility
```

not around flashy UI or premature hardware drivers.

---

## 2. The core software-stack rule

The default rule should be:

```text
Use the simplest deterministic software stack that can correctly express AMCF packages, manifests, update events, physical sections, validation, reports, and corridor-specific adapters.
```

That means:

```text
Start with Python + standard library + JSON + Markdown + unittest where possible.
Add dependencies only when a corridor genuinely needs them.
Keep every new dependency justified, documented, tested, and optional where practical.
```

This matches the existing repo style from the physical-player sequence:

```text
- Python modules
- demo scripts
- JSON reports
- Markdown docs
- unittest tests
- generated output under output/
- no generated output committed
- claim-boundary checks
```

That existing style worked for the physical-player state-machine, fail-closed, reverse/seek, mechanism-profile, release-review, package-refresh, closeout, and tag-prep layers.

The software stack should extend that style rather than replace it.

---

## 3. Dependency policy

The AMCF software should use a tiered dependency policy.

```text
Tier 0 — Standard library only
Tier 1 — Lightweight optional dependency
Tier 2 — Corridor-specific dependency
Tier 3 — UI/application dependency
Tier 4 — Hardware/device dependency
```

## Tier 0 — Standard library only

Use for:

```text
- package/manifest JSON
- schema-like validation helpers
- deterministic fixtures
- CLI demos
- reports
- audits
- file discovery
- unit tests
- docs generation helpers
```

Likely modules:

```text
json
pathlib
hashlib
dataclasses
typing
argparse
datetime
subprocess
unittest
html
csv
zipfile
```

Tier 0 should be the default.

## Tier 1 — Lightweight optional dependency

Use only when it improves a corridor clearly without taking over the project.

Possible later examples:

```text
- JSON schema validation library
- lightweight image library
- small PDF/SVG helper
- QR/barcode helper
```

Do not add yet without a specific phase.

## Tier 2 — Corridor-specific dependency

Use when a corridor cannot realistically work well with only the standard library.

Examples:

```text
PC → Printer:
PDF/SVG/image layout dependency may become justified.

PC ↔ Reader:
image-processing dependency may become justified.

Player ↔ PC:
serial/USB/device dependency may become justified later.
```

Tier 2 should be isolated to corridor modules.

## Tier 3 — UI/application dependency

Use only after CLI/report flows are stable.

Examples:

```text
desktop GUI
local web UI
visual print preview
reader recovery dashboard
player diagnostics UI
```

UI should not be the first implementation layer.

## Tier 4 — Hardware/device dependency

Use only when real hardware exists or a specific interface is being tested.

Examples:

```text
printer driver APIs
scanner APIs
USB/HID
serial
microcontroller bridge
firmware update tooling
```

Current state:

```text
Do not add Tier 4 yet.
```

The physical-player plan still treats real hardware as future. It explicitly keeps Level 5 future physical hardware unachieved. ---

## 4. General selection criteria

Any software choice should be judged against these criteria.

```text
1. Does it support AMCF’s update-event model?
2. Does it preserve manifest/package traceability?
3. Does it work offline?
4. Does it work on Windows?
5. Is it deterministic enough for tests?
6. Can Codex modify it safely?
7. Does it avoid hardware claims?
8. Does it keep generated output out of Git?
9. Does it keep reports inspectable?
10. Does it avoid unnecessary dependencies?
11. Does it allow future hardware adapters?
12. Does it preserve unsafe_acceptance_count = 0?
```

The final question matters because the physical-player plan states that unsafe acceptance must remain zero. A software library is not useful if it makes validation opaque or hard to test.

---

## 5. Corridor-specific selection logic

Software choices should be evaluated differently per corridor.

```text
PC → Printer:
layout correctness, physical dimensions, print repeatability, section traceability.

PC ↔ Reader:
image input, lane detection, recovery accuracy, damage diagnosis.

Player ↔ PC:
runtime scheduling, safety state, diagnostics, command/report models.
```

A good tool for one corridor may be irrelevant for another.

Example:

```text
A PDF library may be useful for PC → Printer.
It does not help much with Player ↔ PC runtime state.
```

Example:

```text
An image-processing library may be useful for PC ↔ Reader.
It should not become a dependency of the shared AMCF manifest model.
```

So dependencies should be corridor-local wherever possible.

---

# Category A — Core Language / Runtime

## 6. Baseline choice

The current baseline should remain:

```text
Python
```

Reason:

```text
- current repo is already Python-heavy
- Codex can patch Python easily
- standard library is strong enough for manifests/reports/tests
- existing demos and tests already use Python
- Windows execution is already established
- deterministic JSON/Markdown reports are easy
```

This does not mean every future interface must be Python forever.

It means the first coherent software system should use the language the repo already uses.

## 7. Core runtime requirements

Python code should support:

```text
- typed dataclasses or structured dicts
- JSON manifest loading/writing
- deterministic ID generation
- hash/checksum helpers
- report generation
- fixture generation
- CLI scripts
- unittest tests
```

## 8. Avoid early multi-language split

Do not start with:

```text
Python core
+ TypeScript UI
+ C++ scanner bridge
+ Rust package core
+ Electron GUI
```

That may become useful later, but not before the shared model and corridor demos exist.

First target:

```text
one reliable Python software core
```

Then expand.

---

# Category B — CLI Tooling

## 9. CLI should come before GUI

Every major AMCF software function should first work through a CLI/demo script.

Reason:

```text
- easier to test
- easier for Codex to run
- easier to produce reports
- easier to debug
- does not require UI decisions
- works before hardware exists
```

Recommended first CLI style:

```text
python demo/run_<feature>_demo.py
```

Later, this can become:

```text
python -m amcf_tools <command>
```

But early demos should remain simple.

## 10. CLI requirements

Every CLI/demo should:

```text
- accept repo-local fixture/default input
- write output under output/<run_name>/
- produce JSON report
- produce Markdown summary
- return nonzero on failure if appropriate
- not require internet
- not require real hardware
- not commit generated output
```

This matches the existing repo pattern.

---

# Category C — Data Formats

## 11. JSON as first manifest/report format

The first shared AMCF data format should be:

```text
JSON
```

Reason:

```text
- standard library support
- human-readable
- test-friendly
- easy to diff
- easy to generate fixtures
- already consistent with JSON report style
```

JSON should cover:

```text
- package manifests
- update events
- section records
- print manifests
- reader recovery reports
- player runtime reports
- audit outputs
```

## 12. Markdown for human summaries

Use Markdown for:

```text
- docs
- human-readable reports
- summaries
- handoff files
- release notes
```

## 13. Future formats

Possible later formats:

```text
CBOR
SQLite
ZIP package bundle
binary package bundle
HTML reports
PDF reports
```

But they should not replace JSON/Markdown too early.

## 14. Schema handling

First phase:

```text
manual schema-like validation in Python
```

Later:

```text
formal JSON Schema or equivalent
```

Do not add schema dependencies before the repo audit shows what formats already exist.

---

# Category D — PC → Printer Tooling

## 15. Printer software needs

The PC → Printer corridor needs software for:

```text
- physical section layout
- page/sheet/card/strip positioning
- timing/index lane placement
- registration mark placement
- colour-reference placement
- hash/checksum lane placement
- print manifest creation
- print preview/reporting
- reprint package generation
```

The physical-player plan already identifies timing/index, registration, colour registry/reference, metadata/transform, and hash/checksum lanes as relevant section/prefetch concepts. Printer software must create those fields physically or at least prepare layout records for them.

## 16. Candidate print/export formats

The software dossier should later research:

```text
PDF
SVG
PNG
JSON layout manifest
HTML preview
```

Each has a role.

## PDF

Potential role:

```text
final print-ready sheets
```

Strength:

```text
page-oriented
print-friendly
stable for users
```

Risk:

```text
PDF generation may require dependency
physical dimensions must be handled carefully
harder to inspect than JSON/SVG
```

## SVG

Potential role:

```text
precise vector layout and lane geometry
```

Strength:

```text
human-readable XML
good for marks/lane layout
can be converted later
```

Risk:

```text
print fidelity depends on renderer
fonts/units must be controlled
```

## PNG

Potential role:

```text
raster preview or simple printed test sheets
```

Strength:

```text
simple visual fixture
easy to inspect
```

Risk:

```text
DPI and physical size can become ambiguous
not ideal as only canonical print layout
```

## JSON layout manifest

Potential role:

```text
canonical layout metadata
```

Strength:

```text
testable
traceable
machine-readable
can drive multiple export formats
```

Risk:

```text
not directly printable by itself
```

## 17. Recommended printer-stack direction

The likely progression should be:

```text
1. JSON print layout manifest
2. SVG sheet export
3. PNG preview if useful
4. PDF export later if needed
```

Reason:

```text
JSON defines the truth.
SVG exposes geometry.
PNG previews visual output.
PDF becomes user-facing print output later.
```

But this should be confirmed after repo audit.

---

# Category E — PC ↔ Reader / Image Processing Tooling

## 18. Reader software needs

The PC ↔ Reader corridor needs software for:

```text
- image input
- section boundary detection
- lane detection
- marker detection
- registration correction
- colour reference reading
- hash/checksum reading
- damage diagnosis
- recovery reports
```

The physical-player plan says the prefetch reader lane should read section index, timing marks, registration marks, colour registry/reference, metadata/transform lane, hash/checksum lane, and damage/missing marker status. The reader software must eventually interpret those things from captured media.

## 19. No-hardware reader first

The first reader implementation should not require a scanner.

It should accept:

```text
- generated fixture images
- existing image files
- image folders
- simulated reader captures
```

Only later:

```text
- scanner API
- camera capture
- reader hardware API
```

## 20. Reader tool dependency levels

Tier 0 reader work can use:

```text
- JSON fixtures
- generated synthetic capture metadata
- simple file inspection
- deterministic lane-coordinate fixtures
```

Tier 1/2 reader work may need:

```text
- image library
- computer vision library
- barcode/marker decoder
```

But do not add image-processing dependencies before the first reader model is defined.

## 21. Recommended reader-stack direction

The likely progression should be:

```text
1. reader capture JSON fixture
2. synthetic lane geometry fixture
3. generated print-layout-to-reader fixture
4. simple image input support
5. lane detection dependency only when needed
6. real scanner/camera input later
```

This avoids jumping to complex CV too early.

---

# Category F — Marker / Lane Detection

## 22. Lane software must be abstract first

The software should first define lane semantics:

```text
timing/index lane
registration lane
colour reference lane
metadata/transform lane
hash/checksum lane
payload area
damage/missing marker status
```

Only later should it decide exact encoding:

```text
QR code
barcode
custom fiducial marks
printed microtext
geometric marks
colour patches
hybrid lane symbols
```

The physical-player plan already gives lane categories, but not final encoding. It identifies the hash/checksum lane as protecting section identity, payload integrity, metadata integrity, lane corruption detection, and fail-closed safety. So software must preserve the lane role before choosing the visual code.

## 23. Marker research criteria

Any marker/lane encoding should be judged by:

```text
- printability
- scan readability
- damage tolerance
- offline decoding
- deterministic tests
- low dependency burden
- ability to encode section identity
- ability to encode checksum/hash reference
- margin/space overhead
- compatibility with small physical sections
```

## 24. Recommended marker/lane direction

First phase:

```text
abstract lane records and coordinates
```

Second phase:

```text
simple visible test marks
```

Third phase:

```text
formal marker encoding research
```

Do not overcommit early.

---

# Category G — Player ↔ PC Tooling

## 25. Player ↔ PC needs

This corridor needs:

```text
- package compatibility checking
- capability profiles
- mechanism profile selection
- runtime state-machine execution
- fail-closed reporting
- reverse/seek command limits
- simulated command/report protocol
- future device protocol placeholder
```

The physical-player plan says the player must decide whether the next section is ready, verified, whether the A/B gate is ready, whether audio sync is acceptable, and whether to continue, pause, or fail closed. So Player ↔ PC tooling must preserve decision-making and logs.

## 26. No hardware protocol first

The first Player ↔ PC stack should be:

```text
JSON package/control/report files
+ Python simulator
+ deterministic demos
```

Not:

```text
USB device control
firmware protocol
real-time hardware link
```

## 27. Future protocol choices

Later protocol options may include:

```text
JSON-over-serial
USB HID
custom binary protocol
local network protocol
firmware RPC style
```

But those belong after:

```text
- package model is stable
- simulator works from real package data
- player capability model exists
- command/report schema exists
```

---

# Category H — Desktop UI

## 28. UI should not come first

A desktop UI will probably become useful, but not yet.

The first software should be:

```text
CLI + reports + deterministic fixtures
```

UI should come after:

```text
- package schema exists
- printer layout works
- reader recovery path exists
- player runtime simulation works
- reports are stable
```

## 29. Possible future UI roles

A desktop UI could eventually provide:

```text
- package browser
- print preview
- reader recovery review
- section damage dashboard
- player simulation playback timeline
- fail-closed event viewer
- reverse/seek report viewer
```

But these UI functions should consume existing reports.

They should not become the source of truth.

## 30. UI stack research later

Future UI research may compare:

```text
- simple desktop GUI
- local web UI
- static HTML report viewer
- notebook-like internal tools
```

But Part 5 does not choose.

---

# Category I — Local Web UI / HTML Reports

## 31. HTML may be useful before full UI

A useful middle path is:

```text
static HTML reports
```

These can show:

```text
- print sheets preview
- reader capture overlay
- playback timeline
- fail-closed events
- report summaries
```

They do not require a running app.

They can be generated under `output/`.

This may be safer than starting with a full UI framework.

## 32. Local web UI later

A local web UI might eventually help with:

```text
- browsing packages
- selecting print outputs
- reviewing recovered sections
- simulating player playback
```

But it should be later than CLI/report stabilisation.

---

# Category J — Testing Framework

## 33. Baseline test stack

The baseline should remain:

```text
unittest
```

Reason:

```text
- standard library
- current repo uses it successfully
- no dependency
- Codex can run it easily
- works on Windows
```

## 34. Testing requirements

Every new software phase should add tests for:

```text
- imports
- fixture loading
- deterministic output shape
- schema fields
- validation decisions
- fail-closed behaviour
- generated-output policy
- claim-boundary booleans
```

For PC → Printer:

```text
- print section count
- lane coordinate presence
- margin validation
- hash lane present
- report final_passed
```

For PC ↔ Reader:

```text
- fixture capture loads
- lanes detected or simulated
- recovered section status
- hash mismatch caught
- rescan status produced
```

For Player ↔ PC:

```text
- package-derived sections load
- state machine runs
- unsafe_acceptance_count stays zero
- reverse/seek bounded
```

## 35. Future test dependencies

Later, if tests become large, the repo could consider other test tooling.

But there is no need now.

Keep the current pattern until it fails.

---

# Category K — Reporting Format

## 36. Report stack baseline

Use:

```text
JSON report
+ Markdown summary
```

Every run should write:

```text
output/<run_name>/*.json
output/<run_name>/*SUMMARY.md
```

Generated output should not be committed.

## 37. Report consistency

Every report should include:

```text
run_name
final_passed
input_refs
output_refs
counts
validation_results
unsafe_acceptance_count
claim_boundary_flags
generated_output_status
metadata
```

This matches the pattern built during the physical-player release/review sequence.

## 38. Corridor-specific reports

PC → Printer:

```text
print_layout_report.json
print_manifest_report.json
print_validation_report.json
```

PC ↔ Reader:

```text
reader_capture_report.json
reader_recovery_report.json
lane_detection_report.json
```

Player ↔ PC:

```text
player_runtime_report.json
fail_closed_report.json
reverse_seek_report.json
```

---

# Category L — Packaging / Release Tooling

## 39. Current release tooling should be preserved

The current repo already has:

```text
release review
package refresh
final Pages review
closeout handoff
tag prep
```

Future software work should eventually refresh those after implementation phases.

But not after every tiny change.

## 40. Release refresh timing

A release refresh should happen after:

```text
- shared package model exists
- one corridor has meaningful implementation
- tests pass
- docs are updated
- generated-output policy is preserved
```

Do not create a release-review layer after every planning doc.

---

# Category M — Device Communication

## 41. Device communication should be last, not first

Device communication matters for future:

```text
PC ↔ Reader
Player ↔ PC
possibly PC → Printer if direct printer control is needed
```

But current work should not start there.

First:

```text
file-based package/control/report model
```

Later:

```text
simulated protocol
```

Later:

```text
hardware adapter interface
```

Only then:

```text
real USB/serial/device integration
```

## 42. Device communication research criteria

When this becomes relevant, evaluate:

```text
- Windows support
- driver burden
- offline capability
- testability without device
- simulator fallback
- protocol logging
- safe failure behaviour
- no false hardware validation claims
```

---

## 43. Software selection by implementation phase

The software stack should be chosen progressively.

## Phase 1 — Repo audit and shared model

Use:

```text
Python standard library
JSON
Markdown
unittest
```

No dependencies.

## Phase 2 — Package/manifest model

Use:

```text
Python dataclasses/dicts
JSON fixtures
manual validation helpers
unittest
```

No dependencies unless existing repo already uses one.

## Phase 3 — PC → Printer prototype

Use initially:

```text
JSON layout manifest
SVG text generation
Markdown/JSON reports
```

Maybe later:

```text
PDF dependency
PNG preview dependency
```

## Phase 4 — PC ↔ Reader prototype

Use initially:

```text
reader capture JSON fixtures
synthetic lane coordinates
generated print-layout fixtures
```

Maybe later:

```text
image library
computer vision library
barcode/marker decoder
```

## Phase 5 — Player ↔ PC runtime

Use:

```text
existing Python physical-player simulator
JSON package fixtures
runtime adapter
unittest
```

No hardware dependency.

## Phase 6 — UI/report viewer

Use first:

```text
static HTML report output
```

Maybe later:

```text
desktop UI or local web UI
```

## Phase 7 — Hardware adapters

Only after simulator/protocol/report layers are stable.

Use:

```text
optional hardware-specific modules
simulator fallback
strict claim-boundary docs
```

---

## 44. What should be researched later with current sources

Some choices require later real research, not guessing.

Later web/current-doc research should be done for:

```text
- best Python PDF generation options
- best SVG/PDF conversion options on Windows
- practical scanner/image acquisition options on Windows
- robust image-processing libraries
- barcode/QR/fiducial marker libraries
- USB/HID/serial libraries
- desktop GUI options
- local web UI packaging options
```

Because software libraries change, those choices should be verified at the time of implementation.

Part 5 deliberately does not lock them.

---

## 45. Dependency documentation rule

When a dependency is introduced, the repo should add:

```text
- why it is needed
- which corridor uses it
- whether it is optional
- how to test without it if possible
- Windows install notes
- fallback behaviour
- generated-output policy
```

This can live in a future file like:

```text
docs/AMCF_SOFTWARE_DEPENDENCY_POLICY.md
```

But do not create it until implementation needs it.

---

## 46. Tool choice anti-patterns

Avoid:

```text
- adding a GUI before CLI works
- adding scanner APIs before image fixtures work
- adding printer driver control before print layouts exist
- adding USB protocol before package/control schemas exist
- adding PDF dependency before SVG/JSON layout is proven
- adding CV dependencies before lane model is defined
- creating multiple manifest formats
- treating generated output as source of truth
- using dependencies that make tests nondeterministic
```

These would slow the project.

---

## 47. Recommended near-term stack

For the next actual Codex implementation phase, use:

```text
Python
standard library
JSON
Markdown
unittest
repo-local fixtures
deterministic output reports
```

Do not add new dependencies in the first software implementation unless repo audit proves an existing dependency is already used and appropriate.

Near-term implementation should focus on:

```text
- repo audit
- shared package/manifest discovery
- corridor classification
- schema candidates
- deterministic reports
```

not printer rendering or image processing yet.

---

## 48. What Part 5 decides

Part 5 decides:

```text
- Python remains the baseline software runtime
- standard library remains the default dependency policy
- JSON and Markdown remain the first data/report formats
- unittest remains the baseline test system
- CLI/report flows should come before GUI
- device communication should come after simulated file-based protocols
- PC → Printer may later need PDF/SVG/PNG tooling, but should start with JSON layout/SVG-style geometry
- PC ↔ Reader may later need image-processing tooling, but should start with fixtures and synthetic lane models
- Player ↔ PC should start with package/control/report simulation, not real hardware protocols
- dependency choices must be corridor-specific and justified
- current software-library research should be delayed until the implementation phase that actually needs it
```

---

## 49. What Part 6 should continue with

Part 6 should continue into:

```text
PC → Printer software path
```

That should cover:

```text
- printer corridor purpose
- print package inputs
- print manifest
- printable physical sections
- sheet/card/strip/cartridge layout options
- lane placement
- registration marks
- colour/hash/checksum lanes
- print preview/reporting
- reprint workflow
- what should be implemented first
- what should remain future
```

-----
# AMCF Software Development and I/O Control Dossier  
## Part 6 — PC → Printer Software Path: Digital AMCF to Printable Physical Carrier

## 1. Purpose of Part 6

Part 6 begins the first major corridor:

```text
PC → Printer
```

This corridor answers:

```text
How does digital AMCF become a printable physical AMCF carrier?
```

The physical-player dossier already defines the larger chain:

```text
Digital AMCF
→ AMCF schedule / update events
→ physical AMCF carrier
→ physical player transport
→ physical/optical viewing window
```

So the printer corridor is responsible for creating the **physical AMCF carrier** part of that chain. This is not just ordinary printing.

It is not:

```text
print every video frame
```

It is:

```text
convert AMCF package/update-event data into structured printable physical sections with timing, index, registration, colour, metadata, and hash/checksum lanes.
```

---

## 2. Why PC → Printer is a software corridor

The printer is not just a peripheral.

In AMCF, printing is part of the physical media generation pipeline.

The software must decide:

```text
- what sections exist
- what visible state each section represents
- what timing/update event each section belongs to
- what marks/lanes must be printed
- how the section is physically laid out
- how the printed section will later be read, verified, recovered, or played
```

So PC → Printer software must produce more than a picture.

It must produce a **printable AMCF carrier package**.

That package should be usable by:

```text
- a future physical player
- a PC reader/recovery path
- a validation tool
- a reprint workflow
- a package audit report
```

---

## 3. Correct boundary

The PC → Printer corridor should be defined as:

```text
Software that converts AMCF package/manifest/update-event data into validated printable physical AMCF carrier layouts, print manifests, preview assets, and print audit reports.
```

It should not be defined as:

```text
a printer driver
```

or:

```text
hardware printer control
```

at first.

The first implementation should not require direct control over a physical printer.

It should produce:

```text
- print layout manifests
- printable files
- preview files
- audit reports
```

Actual OS printer-driver integration can come later.

---

## 4. PC → Printer input

The printer corridor should take input from the shared AMCF package/manifest model defined in Part 4.

Minimum input:

```text
AMCFPackage
AMCFManifest
AMCFPlaybackSchedule
AMCFUpdateEvent list
AMCFVisibleState list
AMCFPhysicalSection list
assets / payload references
hash/checksum metadata
print profile or layout profile
```

The key input is the update-event schedule.

The physical-player plan gives an example event containing timestamp, visible section, next section, dwell time, preload deadline, transition blank duration, and verification requirement. The printer software should preserve those relationships.

It should know:

```text
section_00041 is not just an image.
It is the visible section required at timestamp 1200 ms,
with a dwell duration,
a next section,
a verification requirement,
and a role in the AMCF schedule.
```

---

## 5. PC → Printer output

The printer corridor should eventually produce a package like:

```text
Printable AMCF Carrier Package
```

Containing:

```text
- print layout manifest
- printable sheets/cards/strips/cartridge inserts
- section-to-update-event map
- registration mark definitions
- timing/index lane definitions
- colour reference definitions
- metadata lane definitions
- hash/checksum lane definitions
- print preview files
- print audit report
- reprint index
```

Early implementation can be simpler:

```text
JSON print layout manifest
+ SVG-style or text-based geometry
+ Markdown/JSON report
```

Later implementation can add:

```text
PDF export
PNG preview
print calibration sheet
direct print command support
```

But the first step should define the layout data correctly.

---

## 6. The central object: AMCFPrintSection

Part 4 defined:

```text
AMCFPhysicalSection
→ AMCFPrintSection
```

That distinction is important.

`AMCFPhysicalSection` means:

```text
the abstract physical AMCF unit
```

`AMCFPrintSection` means:

```text
the layout/export representation of that physical unit on a printable sheet/card/strip/carrier
```

So the printer corridor should not directly print arbitrary visible states.

It should map:

```text
AMCFPhysicalSection
→ AMCFPrintSection
→ printable carrier output
```

A print section should know:

```text
- which physical section it represents
- which update event it belongs to
- where it appears on a sheet/card/strip
- what payload area it has
- where its lanes are
- where its registration marks are
- what hash/checksum protects it
- how it maps back to the manifest
```

---

## 7. Update-event-driven printing

This is the most important print rule.

The printer corridor should not begin from:

```text
video frame 1
video frame 2
video frame 3
...
```

It should begin from:

```text
AMCF update event 1
AMCF update event 2
AMCF update event 3
...
```

The physical-player dossier repeatedly states that physical AMCF follows update events rather than fixed-FPS page movement: source timing becomes physical section update events, view-gate dwell duration, and optical presentation timing. That means the print software should ask:

```text
Which visible states actually need physical sections?
Which states can be held/dwelled?
Which states represent meaningful AMCF updates?
Which sections need next/previous references?
Which sections need verification lanes?
```

Not:

```text
How many frames are in the source video?
```

Frame extraction may still be used internally, but the AMCF print output should be event/section based.

---

## 8. Print package hierarchy

A clean print package hierarchy should look like:

```text
AMCFPrintPackage
  AMCFPrintManifest
    PrintJob
    PrintSheet[]
      AMCFPrintSection[]
        PayloadArea
        TimingIndexLane
        RegistrationLane
        ColourReferenceLane
        MetadataLane
        HashChecksumLane
        ServiceMarks
    PrintAuditReport
    ReprintIndex
```

This should map back to:

```text
AMCFPackage
  AMCFManifest
    AMCFPlaybackSchedule
      AMCFUpdateEvent[]
    AMCFPhysicalSection[]
```

The printer-specific objects should be views/adapters, not a separate AMCF universe.

---

## 9. AMCFPrintPackage

## 9.1 Purpose

`AMCFPrintPackage` is the outer printer-export container.

It should answer:

```text
What printable output was generated from this AMCF package?
```

## 9.2 Required fields

```text
print_package_id
source_package_id
source_manifest_id
print_profile_id
created_at
created_by
sheet_count
print_section_count
export_formats
print_manifest_path
preview_refs
audit_report_ref
reprint_index_ref
schema_version
```

## 9.3 Why needed

The print output must be traceable.

A later reader should be able to say:

```text
This scanned section came from print_package_id X,
sheet 3,
section 12,
which maps to AMCF physical section section_00041.
```

Without this, recovery and player validation become weak.

---

## 10. AMCFPrintManifest

## 10.1 Purpose

The print manifest records the exact printable layout.

It should answer:

```text
What was printed, where, at what size, with what lane data, and how does it map back to the AMCF manifest?
```

## 10.2 Required fields

```text
print_manifest_id
source_manifest_id
print_schema_version
units
dpi
page_size
margin_profile
sheet_count
sheets
section_count
section_map
lane_encoding_profile
registration_profile
colour_profile
hash_profile
export_refs
validation_results
```

## 10.3 Print manifest role

The print manifest is not only for the printer.

It is also for:

```text
- reader recovery
- reprint workflow
- audit/debugging
- player compatibility checks
- package validation
```

So it should be stored as JSON even if printable output is SVG/PDF/PNG.

---

## 11. Print profile

The print profile defines the intended layout style.

Possible print profiles:

```text
sheet_grid_profile
card_stack_profile
strip_carrier_profile
folded_carrier_profile
cartridge_insert_profile
test_fixture_profile
```

Each profile should define:

```text
- units
- DPI or vector scale
- page size
- margins
- section size
- lane placement
- registration mark style
- colour reference style
- hash/checksum encoding style
- service/debug mark style
```

Early implementation should probably start with:

```text
test_fixture_profile
```

or:

```text
sheet_grid_profile
```

because they are easiest to test.

Do not start with a complex cartridge insert format before the section model is stable.

---

## 12. Layout forms

PC → Printer should support several possible physical layouts over time.

Do not force one final layout too early.

The main candidates are:

```text
A. sheet grid
B. individual cards
C. strip / folded strip
D. cartridge insert
E. calibration / test sheet
```

---

# A. Sheet grid layout

## 13. Sheet grid

This is the simplest first software target.

```text
one printable sheet
→ multiple physical sections arranged in a grid
```

Advantages:

```text
- easy to test
- easy to preview
- easy to inspect visually
- good for early reader fixtures
- good for section/lane layout development
```

Problems:

```text
- not necessarily the final cartridge form
- may require manual cutting
- may not match future player transport exactly
```

Best use:

```text
first print-layout prototype
reader/recovery fixture
software validation
```

---

# B. Individual card layout

## 14. Cards

```text
one physical section per card
```

Advantages:

```text
- clear section identity
- easy to handle in small tests
- easier damaged-section replacement
```

Problems:

```text
- loose-card handling is not ideal for final player
- ordering errors are possible
- not as aligned with folded-carrier product direction
```

Best use:

```text
bench tests
reader fixtures
low-speed prototypes
```

---

# C. Strip / folded strip layout

## 15. Strip / folded carrier

```text
sections printed in sequence along a strip or folded path
```

Advantages:

```text
- closer to folded indexed carrier concept
- preserves section order
- fits future transport thinking
```

Problems:

```text
- harder to print accurately
- harder to handle without material decisions
- longer layouts may be awkward
```

Best use:

```text
later physical-carrier prototype
not first software-only fixture
```

---

# D. Cartridge insert layout

## 16. Cartridge insert

```text
print output designed for insertion into a cartridge/carrier assembly
```

Advantages:

```text
- closer to future product direction
- supports protected media
```

Problems:

```text
- cartridge mechanics are unresolved
- material/assembly assumptions may overclaim hardware readiness
```

Best use:

```text
future hardware-facing design phase
```

Not first.

---

# E. Calibration / test sheet

## 17. Calibration sheet

The printer corridor should eventually generate test sheets for:

```text
- registration accuracy
- margin checking
- colour reference
- lane readability
- scaling/DPI validation
- scanner/reader calibration
```

This may become very useful for PC ↔ Reader.

But first, the shared section/lane model must exist.

---

## 18. Section anatomy for print

Each printable AMCF section should be treated as a structured area.

Baseline section anatomy:

```text
+------------------------------------------------+
| service/debug marks                            |
| timing/index lane                              |
| registration marks / lane                      |
|                                                |
|         image / payload area                   |
|                                                |
| colour reference lane                          |
| metadata/transform lane                        |
| hash/checksum lane                             |
+------------------------------------------------+
```

The physical-player plan identifies section/prefetch lane concepts including timing/index, registration, colour registry/reference, metadata/transform, hash/checksum, and damage/missing marker status. The print path should create the printable representation of those lanes.

---

## 19. Payload area

The payload area is the visible image area.

It should contain:

```text
- precomposited visible state for early implementation
- or later component/layer representation
```

First implementation should probably use:

```text
one visible state → one payload image/section
```

Do not begin with physical component layering unless the shared model is already stable.

The physical-player dossier leaves room for future layered AMCF-native designs, but the practical baseline is precomposited physical sections.

---

## 20. Timing/index lane

The timing/index lane tells software and reader/player systems where the section belongs.

It should encode or reference:

```text
section_id
section_index
event_id
timestamp_start_ms
timestamp_end_ms
dwell_ms
previous_section_id
next_section_id
manifest_id
carrier_id
```

This lane lets the reader/player answer:

```text
Is this the correct section?
Is it in the expected order?
Is it the required next section?
```

The physical-player plan says the prefetch lane should answer whether the section is correct, in expected order, aligned enough, hash-valid, degraded but usable, safe to display, or should trigger continue/rescan/skip/pause/fail-closed. So the print output must include enough information for those later decisions.

---

## 21. Registration lane / marks

Registration marks allow the reader or player to align the section.

They should support:

```text
- position detection
- rotation/skew detection
- crop boundary detection
- scale checking
- gate alignment reference
```

Print software should define:

```text
registration_mark_positions
registration_mark_size
registration_mark_style
registration_tolerance
expected_reader_detection_area
```

Early software can represent them as abstract geometry.

The first implementation does not need advanced fiducials.

It needs deterministic layout records.

---

## 22. Colour reference lane

The colour reference lane supports colour/brightness correction and degradation checks.

It may include:

```text
- neutral patch
- black/white references
- primary colour patches
- grayscale strip
- expected colour metadata
```

Reader use:

```text
detect colour shift / fading / print error
```

Player use:

```text
decide whether colour degradation is warning-only or display-blocking
```

The first implementation can model colour references abstractly.

It does not need full colour science yet.

---

## 23. Metadata / transform lane

The metadata lane should carry or reference information such as:

```text
manifest_id
package_id
section_id
component info
transform info
payload type
schema version
profile IDs
```

This may be encoded as:

```text
plain text
symbol marks
compact JSON reference
QR/barcode later
custom lane later
```

The first software should not lock encoding.

It should define the field structure and layout position.

---

## 24. Hash/checksum lane

The hash/checksum lane protects integrity.

The physical-player plan says this lane should support section identity verification, payload integrity, metadata integrity, lane corruption detection, and fail-closed safety. For print software, it should include or reference:

```text
section_hash
payload_hash
metadata_hash
hash_algorithm
checksum_value
manifest_hash_reference
```

Reader/player use:

```text
- confirm this is the expected section
- detect print corruption
- detect scan misread
- prevent wrong section display
- trigger rescan/reprint/fail-closed
```

Important rule:

```text
A critical hash mismatch should never be silently accepted.
```

---

## 25. Service/debug marks

Service/debug marks may help early testing.

Possible marks:

```text
human-readable section ID
sheet number
grid coordinate
orientation arrow
debug border
crop boundary
```

These are useful for development.

But final physical media may hide or reduce them.

Print profiles should allow:

```text
debug_marks_enabled = true/false
```

---

## 26. Print manifest validation

Before generating printable output, software should validate:

```text
- source package exists
- manifest exists
- update events exist
- physical sections exist
- each print section maps to one physical section
- section IDs are unique
- section indexes are sequential or explicitly mapped
- lane bounds do not overlap wrongly
- payload bounds are within section bounds
- page margins are respected
- hash/checksum fields exist where required
- schema versions are present
```

Validation output:

```text
AMCFValidationResult[]
```

If critical validation fails, print export should fail.

Do not generate a print package that later cannot be verified.

---

## 27. Print audit report

Every print export should produce a report.

Suggested report:

```text
print_audit_report.json
```

Fields:

```text
run_name
source_package_id
source_manifest_id
print_package_id
print_profile_id
sheet_count
section_count
event_count
layout_valid
margins_valid
lanes_present
hash_lanes_present
registration_marks_present
colour_reference_present
generated_exports
validation_results
warnings
errors
final_passed
unsafe_acceptance_count
claim_boundary_flags
```

The report should also include:

```text
physical_hardware_claimed = false
hardware_validation_claimed = false
manufactured_player_claimed = false
```

Because generating print layouts is not hardware validation.

---

## 28. Unsafe acceptance in printer corridor

The printer corridor also needs the unsafe-acceptance rule.

For printing, unsafe acceptance means:

```text
- missing section printed without warning
- duplicate section ID accepted
- hash lane omitted when required
- wrong event-to-section mapping accepted
- layout overlap accepted
- margin violation accepted
- schema mismatch accepted
```

The report should include:

```text
unsafe_acceptance_count
```

It should remain:

```text
0
```

The physical-player plan uses `unsafe_acceptance_count` as a key safety invariant. The printer path should inherit that invariant.

---

## 29. Reprint workflow

A real physical workflow needs reprints.

If a section is damaged or misprinted, the software should support:

```text
reprint section_00041
reprint sheet_003
reprint all failed sections
reprint calibration sheet
```

This requires:

```text
- stable section IDs
- print manifest
- sheet/section mapping
- reprint index
- hash/checksum preservation
```

A future reader may report:

```text
section_00041 hash mismatch
```

Then printer software should generate:

```text
reprint package for section_00041
```

This is why print package traceability matters.

---

## 30. Print preview

Print preview should be treated as software output.

Early preview can be:

```text
- SVG layout
- HTML preview
- JSON geometry summary
- PNG preview later
```

Preview should show:

```text
- sheet boundary
- margins
- section boxes
- payload area
- timing/index lane
- registration marks
- colour reference lane
- metadata lane
- hash/checksum lane
```

Preview is not the source of truth.

The source of truth should remain:

```text
print layout manifest
```

---

## 31. Print calibration

Print calibration should be planned but not overbuilt at first.

Future calibration needs:

```text
- scale check
- margin check
- skew check
- colour reference check
- lane readability check
- scanner roundtrip check
```

A future calibration sheet could include:

```text
- ruler marks
- registration marks
- colour patches
- lane samples
- hash/checksum sample
- section ID sample
```

This will matter when PC ↔ Reader is implemented.

But first:

```text
define print sections and lanes.
```

---

## 32. Print export formats

The software stack Part 5 suggested this progression:

```text
1. JSON print layout manifest
2. SVG sheet export
3. PNG preview if useful
4. PDF export later if needed
```

Part 6 confirms that is a good implementation direction.

## 32.1 JSON layout manifest

Should be first.

It is testable and canonical.

## 32.2 SVG export

Good early printable/preview output.

Can represent:

```text
rectangles
text labels
lane boxes
registration marks
payload placeholders
```

Can be generated with standard-library string/XML writing.

No dependency needed initially.

## 32.3 PNG preview

Useful later.

May require image dependency.

Do not start here unless repo already has image rendering support.

## 32.4 PDF export

Important eventually for users.

But it may require dependency.

Do not make PDF the first canonical format.

---

## 33. First implementation target for PC → Printer

The first implementation should not attempt a full print system.

It should implement:

```text
AMCF print layout manifest prototype
```

Using:

```text
- deterministic fixture manifest
- small number of update events
- small number of physical sections
- sheet-grid layout
- abstract lane geometry
- JSON report
- optional SVG preview
- unittest tests
```

Suggested future run name:

```text
AMCF_PC_TO_PRINTER_LAYOUT_PROTOTYPE_V1
```

But this should come only after the repo-audit phase and shared model phase.

---

## 34. First fixture shape

A minimal fixture could contain:

```text
package_id: fixture_package_001
manifest_id: fixture_manifest_001
events:
  - event_0001 at 0 ms → section_0001
  - event_0002 at 1200 ms → section_0002
  - event_0003 at 2400 ms → section_0003
physical_sections:
  - section_0001
  - section_0002
  - section_0003
```

Each section should include:

```text
section_id
section_index
timestamp_start_ms
dwell_ms
payload_ref
section_hash
timing_lane data
registration_lane data
colour_reference_lane data
metadata_lane data
hash_checksum_lane data
```

Then printer layout maps each to:

```text
sheet_001
grid position
payload bounds
lane bounds
debug label
```

---

## 35. Tests for first printer prototype

Future tests should verify:

```text
- fixture manifest loads
- print layout manifest builds
- section count matches event count
- section IDs are stable
- sheet count is deterministic
- lane bounds exist
- payload bounds exist
- no invalid overlap
- margins valid
- hash lane present
- registration lane present
- colour reference present
- SVG preview generated if implemented
- report final_passed true
- unsafe_acceptance_count == 0
- hardware claim booleans false
```

No physical printer should be required.

---

## 36. Generated output policy

Printer demos will generate output.

Generated output should go under:

```text
output/amcf_pc_to_printer_layout/
```

Possible files:

```text
print_layout_manifest.json
print_audit_report.json
print_sheet_001.svg
PRINT_LAYOUT_SUMMARY.md
```

These should not be committed unless explicitly intended as fixtures.

If a fixture is needed for tests, place it under a controlled fixture path, not `output/`.

---

## 37. Relationship to PC ↔ Reader

The printer path should be designed with reader recovery in mind.

Every printed section should be recoverable.

That means print layout should include enough data for later reader software to recover:

```text
- section ID
- event ID
- timing
- registration
- colour reference
- hash/checksum
- payload bounds
```

The reader path should not have to guess the print layout.

It should use the print manifest.

So the long-term flow is:

```text
PC → Printer:
create print manifest and physical output

PC ↔ Reader:
use print manifest to recover/validate scanned output
```

This is why the print manifest is central.

---

## 38. Relationship to Player ↔ PC

The printer path should also support the physical-player model.

The physical-player plan says the player prefetch lane should read section index, timing marks, registration marks, colour reference, metadata/transform lane, hash/checksum lane, and damage/missing marker status. Therefore printed sections should include the data future player-prefetch needs.

Even if early software uses only simulated player sections, print layout should not ignore those requirements.

Long-term flow:

```text
PC → Printer:
prints sections with lanes

Player ↔ PC:
uses manifest/player model to know what sections should be staged/displayed

Future player prefetch:
reads printed lanes to verify the upcoming section
```

---

## 39. Avoiding overclaim

Printing a layout does not mean:

```text
a physical player can play it
```

It only means:

```text
the software generated a structured printable representation that follows the AMCF manifest and lane model.
```

So reports/docs should say:

```text
print layout generated
print manifest valid
section mapping valid
lane geometry present
```

Not:

```text
not hardware validated
physical player proven
printer output proven playable
```

Actual print fidelity, reader recovery, and player execution require later stages.

---

## 40. What should remain future

Do not do these first:

```text
- direct printer driver integration
- automatic printer calibration
- real physical print validation
- high-density micro-mark encoding
- full PDF production pipeline
- GUI print preview
- automatic cut/assembly instructions
- cartridge manufacturing instructions
- hardware-ready print claims
```

These may come later.

First establish:

```text
manifest → print layout → report
```

---

## 41. What Part 6 decides

Part 6 decides:

```text
- PC → Printer is a full software corridor, not just a print command
- printer software should generate structured AMCF physical carrier layouts
- printing should be update-event/section-driven, not fixed-frame-driven
- AMCFPrintSection should be a print-layout view of AMCFPhysicalSection
- print manifest should be canonical for printable layout
- initial layout target should be simple sheet-grid/test-fixture output
- JSON print layout manifest should come before PDF
- SVG is a good early preview/export target
- print sections must include timing/index, registration, colour, metadata, and hash/checksum lane concepts
- print audit reports should include unsafe_acceptance_count and claim-boundary flags
- reprint workflow should be planned from the start
- no direct printer hardware control should be added in the first implementation
```

---

## 42. What Part 7 should continue with

Part 7 should continue into:

```text
PC ↔ Reader software path
```

That should cover:

```text
- reader corridor purpose
- no-hardware reader-first model
- reader capture objects
- fixture image/folder input
- lane detection
- section boundary detection
- print-manifest-assisted recovery
- validation and rescan/reprint decisions
- recovered package output
- reader audit reports
- first implementation target
```

----
# AMCF Software Development and I/O Control Dossier  
## Part 7 — PC ↔ Reader Software Path: Physical Carrier Capture, Lane Recovery, Validation, and Rebuild Workflow

## 1. Purpose of Part 7

Part 6 defined:

```text
PC → Printer
```

as the corridor that creates structured printable AMCF physical carrier output.

Part 7 now defines:

```text
PC ↔ Reader
```

This corridor answers:

```text
How does a physical AMCF carrier get read, recovered, validated, diagnosed, and turned back into useful AMCF package data?
```

This corridor is not the same as the physical-player visible playback path.

The attached physical-player plan already makes that distinction: the reader/scanner path recovers or validates AMCF media, while the physical-player path physically/optically presents AMCF media for direct viewing. So Part 7 must keep two ideas separate:

```text
Reader/recovery software:
reads physical AMCF media into the PC for validation, recovery, diagnosis, and reconstruction.

Player/prefetch software:
reads ahead inside a player to decide whether an upcoming section is safe to display.
```

They share lane concepts, but they are not the same workflow.

---

## 2. Correct boundary

The PC ↔ Reader corridor should be defined as:

```text
Software that accepts captured physical AMCF carrier input, detects sections and lanes, validates section identity and integrity, diagnoses damage or misread data, and reconstructs or audits AMCF package data.
```

It should not initially be defined as:

```text
a hardware scanner driver
```

or:

```text
a real-time physical-player prefetch system
```

The first implementation should work without real reader hardware.

It should support:

```text
- fixture captures
- generated print-layout fixtures
- image-folder input later
- simulated reader capture records
- print-manifest-assisted recovery
```

Real hardware support comes later.

---

## 3. Why PC ↔ Reader is bidirectional

The corridor should be written as:

```text
PC ↔ Reader
```

not only:

```text
Reader → PC
```

because the PC may need to send or define:

```text
- reader profile
- capture profile
- calibration profile
- expected print manifest
- expected package/manifest ID
- section range to scan
- rescan instructions
- retry instructions
- damaged-section reprint request
```

And the reader side sends back:

```text
- raw capture
- detected section candidates
- lane extraction results
- validation results
- recovery status
- damaged-section reports
- reconstructed package data
```

So it is a software control and recovery loop, not just raw scanning.

---

## 4. Reader path compared with printer path

Part 6 defined:

```text
AMCFPackage
→ AMCFManifest
→ AMCFPhysicalSection
→ AMCFPrintSection
→ printed carrier
```

Part 7 defines the reverse/recovery direction:

```text
printed carrier / physical AMCF section
→ reader capture
→ section detection
→ lane extraction
→ validation
→ recovered section
→ recovered package / recovery report
```

So the reader path should be able to use the print manifest.

The printer path creates:

```text
print_manifest.json
```

The reader path should use it to answer:

```text
What section should be here?
Where should the lanes be?
What hash/checksum should be expected?
What bounds should the payload area have?
What registration marks should be present?
```

This is better than making the reader guess everything.

---

## 5. Core reader input types

The reader software should support several input types over time.

```text
A. simulated reader capture JSON
B. generated print-layout fixture
C. static image file
D. image folder / batch capture
E. scanner output
F. camera capture
G. dedicated reader hardware output
```

The order matters.

First implementation should begin with:

```text
A. simulated reader capture JSON
B. generated print-layout fixture
```

not:

```text
real scanner hardware
```

because software correctness must come first.

---

# A. Simulated reader capture JSON

## 6. Purpose

This is the easiest first reader input.

It represents what a reader would have detected, without requiring image processing yet.

Example shape:

```json id="yu816x"
{
  "capture_id": "capture_0001",
  "capture_source": "fixture",
  "source_print_manifest_id": "print_manifest_001",
  "candidate_section_id": "section_0001",
  "detected_bounds": {
    "x": 10,
    "y": 20,
    "width": 400,
    "height": 260
  },
  "detected_lanes": {
    "timing_index_lane": "present",
    "registration_lane": "present",
    "colour_reference_lane": "present",
    "metadata_lane": "present",
    "hash_checksum_lane": "present"
  }
}
```

This lets the software test:

```text
- section matching
- lane status
- hash/checksum comparison
- recovery decisions
- rescan/reprint recommendations
```

without requiring CV/image tooling.

---

# B. Generated print-layout fixture

## 7. Purpose

The reader should eventually read what the printer path generated.

The most useful early closed loop is:

```text
PC → Printer fixture
→ reader fixture
→ validation/recovery report
```

Even before real images, the reader can consume:

```text
print layout manifest
+ simulated capture positions
+ expected lane records
```

This creates a clean software roundtrip.

First roundtrip target:

```text
AMCF manifest
→ print layout manifest
→ simulated reader capture
→ recovered section report
```

That is more valuable than trying to read a real scan too early.

---

# C. Static image file

## 8. Purpose

Later, reader software should accept actual images:

```text
PNG
JPG
TIFF
BMP if needed
```

But this requires image-processing choices.

Part 5 already set the boundary:

```text
Start with fixtures and synthetic lane geometry.
Add image-processing dependencies only when needed.
```

Static image support should come after:

```text
- section/lane model is defined
- print manifest exists
- expected lane geometry exists
- validation decisions exist
```

---

# D. Image folder / batch capture

## 9. Purpose

A practical reader workflow will often involve a folder of scanned pages or photos.

Example:

```text
captures/
  scan_001.png
  scan_002.png
  scan_003.png
```

The software should eventually produce:

```text
reader_batch_report.json
recovered_sections.json
damaged_sections.json
rescan_needed.md
```

But this should not be first.

---

# E/F/G. Real scanner, camera, or dedicated reader

## 10. Purpose

Real hardware input is future.

Examples:

```text
flatbed scanner
document scanner
camera capture
dedicated AMCF reader
player-prefetch reader hardware
```

But current implementation should not depend on any of these.

The first reader software should have a no-hardware path.

---

## 11. Core reader software stages

The reader corridor should be structured as stages.

```text
Stage 1 — Capture input
Stage 2 — Capture normalization
Stage 3 — Section detection
Stage 4 — Lane localization
Stage 5 — Lane decoding / extraction
Stage 6 — Section identity validation
Stage 7 — Payload validation
Stage 8 — Recovery decision
Stage 9 — Recovered-section output
Stage 10 — Reader audit report
Stage 11 — Rescan/reprint workflow
```

Each stage should produce structured data.

Do not make the reader a black box.

---

# Stage 1 — Capture input

## 12. Capture input

This stage loads the reader input.

Inputs may be:

```text
- capture JSON
- print-manifest fixture
- image file
- image folder
- scanner output later
```

Output object:

```text
AMCFReaderCapture
```

Fields from Part 4:

```text
capture_id
capture_source
capture_mode
captured_at
image_ref
dpi_or_resolution
colour_mode
calibration_ref
candidate_section_id
detected_bounds
detected_lanes
reader_profile_id
metadata
```

For fixture-only work, `image_ref` can be absent or point to a generated placeholder.

---

# Stage 2 — Capture normalization

## 13. Capture normalization

This stage normalizes capture metadata.

For image input later, this may include:

```text
- orientation normalization
- scale/DPI interpretation
- colour mode detection
- crop boundary assumption
- page/sheet coordinate mapping
```

For fixture input, it should normalize:

```text
- coordinate units
- section bounds
- lane names
- status values
- source print manifest references
```

Do not skip normalization.

It prevents each reader step from inventing its own assumptions.

---

# Stage 3 — Section detection

## 14. Section detection

This stage identifies candidate AMCF sections in the capture.

For simulated fixtures:

```text
read detected_bounds from capture JSON
```

For print-manifest-assisted recovery:

```text
use expected sheet/grid positions from print manifest
```

For image input later:

```text
detect section boxes, borders, registration marks, or printed section boundaries
```

Output:

```text
candidate_section_records
```

Each candidate should include:

```text
candidate_id
capture_id
bounds
confidence
expected_section_id if known
detected_section_id if decoded
status
```

---

# Stage 4 — Lane localization

## 15. Lane localization

This stage identifies the lane regions inside a section.

Expected lane categories:

```text
timing_index_lane
registration_lane
colour_reference_lane
metadata_transform_lane
hash_checksum_lane
payload_area
service_debug_marks
```

The physical-player plan lists the needed reader/prefetch lane concepts: section index, timing marks, registration marks, colour reference, metadata/transform lane, hash/checksum lane, and damage/missing marker status. So the reader software must preserve these lane categories.

For fixture input:

```text
lane bounds come from fixture or print manifest
```

For image input later:

```text
lane bounds are detected or refined
```

---

# Stage 5 — Lane decoding / extraction

## 16. Lane extraction

This stage extracts information from each lane.

## 16.1 Timing/index lane

Should extract or verify:

```text
section_id
section_index
event_id
timestamp_start_ms
timestamp_end_ms
dwell_ms
manifest_id
carrier_id
previous_section_id
next_section_id
```

## 16.2 Registration lane

Should extract or verify:

```text
registration_marks_present
skew_status
scale_status
crop_status
alignment_status
```

## 16.3 Colour reference lane

Should extract or verify:

```text
colour_reference_present
colour_reference_status
brightness_status
degradation_status
```

## 16.4 Metadata/transform lane

Should extract or verify:

```text
schema_version
package_id
manifest_id
section_id
payload_type
profile_refs
component_refs if present
```

## 16.5 Hash/checksum lane

Should extract or verify:

```text
hash_algorithm
expected_hash
observed_hash
hash_status
checksum_status
```

The physical-player plan says the hash/checksum lane protects section identity, payload integrity, metadata integrity, lane corruption detection, and fail-closed safety. So hash/checksum extraction is a safety-critical reader function.

---

# Stage 6 — Section identity validation

## 17. Section identity validation

The reader must decide:

```text
Is this the section it claims to be?
Is it the section expected at this position?
Is it in the expected order?
Does it match the manifest?
```

Inputs:

```text
- detected section_id
- detected section_index
- source print manifest
- source AMCF manifest
- expected sheet/grid position
- hash/checksum lane
```

Possible statuses:

```text
valid
valid_with_warning
wrong_section
section_unknown
duplicate_section
missing_section
manifest_mismatch
requires_manual_review
```

The reader should not silently accept a wrong section.

---

# Stage 7 — Payload validation

## 18. Payload validation

This stage validates the visible payload area.

In early fixture mode, this may be:

```text
payload_ref exists
payload_hash matches expected
```

Later, with image input, this may include:

```text
image crop hash
perceptual comparison
colour reference correction
damage mask
reader confidence
```

Do not start with complex image comparison.

Start with hash/checksum and fixture validation.

---

# Stage 8 — Recovery decision

## 19. Recovery decision

After lane extraction and validation, reader software should produce a recovery decision.

Suggested statuses:

```text
recovered
recovered_with_warning
requires_rescan
requires_reprint
wrong_section
hash_mismatch
registration_failed
unrecoverable
manual_review_required
```

This should become:

```text
AMCFRecoveredSection
```

Fields from Part 4:

```text
recovered_section_id
capture_id
physical_section_id_candidate
section_index_detected
timing_lane_result
registration_lane_result
colour_reference_result
metadata_lane_result
hash_checksum_result
payload_recovery_result
damage_status
confidence
requires_rescan
recovery_status
```

---

# Stage 9 — Recovered-section output

## 20. Recovered section output

The recovered output should be structured.

Possible file:

```text
recovered_sections.json
```

It should contain:

```text
- recovered section records
- validation results
- source capture refs
- source print manifest refs
- source AMCF manifest refs
- warnings/errors
```

If recovery is good enough, later software can rebuild or verify:

```text
Recovered AMCF package
```

But first, the reader should produce recovery reports.

---

# Stage 10 — Reader audit report

## 21. Reader report

Every reader run should produce a report.

Suggested file:

```text
reader_recovery_report.json
```

Fields:

```text
run_name
source_manifest_id
source_print_manifest_id
capture_count
candidate_section_count
recovered_section_count
valid_section_count
warning_section_count
rescan_required_count
reprint_required_count
unrecoverable_count
hash_mismatch_count
registration_failed_count
wrong_section_count
final_passed
unsafe_acceptance_count
claim_boundary_flags
validation_results
```

Also produce:

```text
READER_RECOVERY_SUMMARY.md
```

Human-readable summary should list:

```text
- recovered sections
- failed sections
- rescan needed
- reprint needed
- damaged sections
- manifest mismatches
```

---

# Stage 11 — Rescan/reprint workflow

## 22. Rescan workflow

If a section cannot be read, the reader should request:

```text
rescan section
rescan sheet
rescan capture
manual review
```

Rescan output:

```text
rescan_requests.json
```

## 23. Reprint workflow

If a section is physically damaged or misprinted, the reader should request:

```text
reprint section
reprint sheet
reprint damaged group
```

Reprint output:

```text
reprint_requests.json
```

This connects directly back to the PC → Printer corridor.

So the corridor loop becomes:

```text
PC → Printer
→ physical carrier
→ PC ↔ Reader
→ recovery report
→ rescan or reprint requests
→ PC → Printer reprint package
```

This loop is one of the most important practical software cycles in AMCF.

---

## 24. Print-manifest-assisted recovery

The reader should not begin by guessing everything from pixels.

The best early recovery mode is:

```text
print-manifest-assisted recovery
```

That means the reader receives:

```text
- print manifest
- expected sheet layout
- expected section positions
- expected lane bounds
- expected hashes/checksums
- expected section IDs
```

Then reader validation becomes:

```text
expected vs observed
```

This is far easier and safer than blind recognition.

Blind recognition can be added later.

---

## 25. Blind recovery mode

Blind recovery means:

```text
recover AMCF section identity without already knowing the print manifest
```

This may require:

```text
- robust metadata lane
- manifest ID lane
- section ID lane
- package ID lane
- hash/checksum lane
- marker decoding
```

This is valuable later, especially for archival recovery.

But first implementation should use print-manifest-assisted mode.

Blind recovery should be future.

---

## 26. Reader profiles

Reader software should support profiles.

Possible profiles:

```text
fixture_reader_profile
print_manifest_assisted_reader_profile
image_folder_reader_profile
scanner_reader_profile
camera_reader_profile
future_hardware_reader_profile
```

Each profile should define:

```text
- input type
- expected resolution or units
- section detection method
- lane localization method
- validation strictness
- allowed warnings
- recovery output mode
```

First profile:

```text
fixture_reader_profile
```

Second profile:

```text
print_manifest_assisted_reader_profile
```

---

## 27. Reader safety model

Reader safety is not about visible display, but it still needs fail-closed logic.

Unsafe reader acceptance means:

```text
- corrupted section marked valid
- wrong section accepted
- hash mismatch ignored
- registration failure ignored
- unreadable lane treated as present
- damaged payload accepted without warning
- manifest mismatch accepted silently
```

The reader report should include:

```text
unsafe_acceptance_count
```

It must remain:

```text
0
```

The physical-player plan already treats unsafe acceptance as a core invariant. That invariant should apply to reader recovery too.

---

## 28. Reader failure modes

The reader path should explicitly model failure modes.

```text
- capture missing
- capture unreadable
- section boundary not found
- multiple section candidates overlap
- section ID missing
- section index unreadable
- timing/index lane unreadable
- registration marks missing
- registration skew too high
- colour reference missing
- hash/checksum lane unreadable
- hash mismatch
- metadata lane corrupt
- payload damaged
- wrong section detected
- duplicate section detected
- manifest mismatch
- print manifest mismatch
```

Each failure should map to a decision:

```text
rescan
reprint
manual review
fail recovery
accept with warning
```

Critical failures should not be accepted.

---

## 29. Reader decisions table

A future reader implementation should include a table like this.

```text
Condition                         Decision
----------------------------------------------------------
section ID readable + hash match  recovered
minor colour warning              recovered_with_warning
registration warning              recovered_with_warning or rescan
section ID unreadable             requires_rescan
hash mismatch                     requires_rescan or reprint
wrong section                     wrong_section / manual review
payload damaged                   requires_reprint
metadata lane corrupt             requires_rescan
manifest mismatch                 manual_review_required
critical lane missing             recovery failed
```

This table should eventually become test cases.

---

## 30. Relationship to physical-player prefetch lane

The player’s internal prefetch lane is time-sensitive.

It needs to answer quickly:

```text
Is the next section safe to display?
```

The PC reader is slower and deeper.

It can answer:

```text
What exactly is damaged?
Can it be recovered?
Should the user rescan?
Should the user reprint?
Can a package be reconstructed?
```

So the two share concepts:

```text
section ID
timing lane
registration
colour
metadata
hash/checksum
damage status
```

But differ in purpose:

```text
player prefetch = immediate display safety
PC reader = recovery/validation/diagnosis
```

Do not merge them into one unclear system.

---

## 31. Reader output should support package reconstruction

A long-term reader goal is:

```text
physical AMCF carrier
→ recovered AMCF package
```

That means the reader should output enough data to reconstruct:

```text
- package ID
- manifest ID
- section list
- update-event mapping
- payload references or recovered payloads
- validation results
- missing/damaged sections
- recovery confidence
```

Early work can stop at recovery reports.

Later work can rebuild package objects.

---

## 32. Reader output should support printer reprint

Reader recovery should directly support printer reprint.

If it detects:

```text
section_00041 damaged
```

it should produce a reprint request:

```json id="m0ge0t"
{
  "request_type": "reprint_section",
  "section_id": "section_00041",
  "reason": "hash_mismatch",
  "source_capture_id": "capture_0017",
  "source_print_manifest_id": "print_manifest_001"
}
```

This closes the PC ↔ Reader and PC → Printer loop.

---

## 33. Reader output should support player safety

Reader reports can also inform Player ↔ PC.

Example:

```text
reader says section_00041 has colour warning but hash valid
```

Then Player ↔ PC software may decide:

```text
display allowed with warning
```

But if reader says:

```text
hash mismatch
```

Player ↔ PC should decide:

```text
display denied / fail closed
```

So the reader report can feed player compatibility reports.

---

## 34. First implementation target for PC ↔ Reader

The first reader implementation should not do image processing.

It should implement:

```text
AMCF reader recovery fixture prototype
```

Suggested future run name:

```text
AMCF_PC_READER_RECOVERY_FIXTURE_V1
```

Purpose:

```text
Use a deterministic print manifest / physical section fixture and simulated reader capture records to validate reader recovery logic.
```

Inputs:

```text
- fixture AMCF manifest
- fixture print manifest
- simulated reader capture JSON
```

Outputs:

```text
- recovered_sections.json
- reader_recovery_report.json
- rescan_requests.json
- reprint_requests.json
- READER_RECOVERY_SUMMARY.md
```

No real scanner.

No image-processing dependency.

---

## 35. Suggested future modules

Future implementation may create:

```text
src/amcf_reader_capture.py
src/amcf_reader_recovery.py
src/amcf_reader_reports.py
```

Maybe later:

```text
src/amcf_reader_image_input.py
src/amcf_reader_lane_detection.py
src/amcf_reader_marker_decode.py
```

But do not create image-processing modules before fixture recovery exists.

---

## 36. Suggested future demos

Future demos may include:

```text
demo/run_amcf_reader_recovery_fixture_demo.py
demo/run_amcf_reader_print_manifest_assisted_demo.py
demo/run_amcf_reader_batch_recovery_demo.py
```

Later:

```text
demo/run_amcf_reader_image_folder_demo.py
demo/run_amcf_reader_lane_detection_demo.py
```

---

## 37. Suggested future tests

Reader tests should verify:

```text
- fixture capture loads
- print manifest loads
- expected section detected
- section ID validation works
- hash match passes
- hash mismatch fails
- wrong section fails
- missing timing lane fails
- missing registration lane warns or fails based on strictness
- damaged payload creates reprint request
- unreadable capture creates rescan request
- recovered_sections output shape stable
- unsafe_acceptance_count remains 0
- hardware claim booleans false
```

Likely test file:

```text
tests/test_amcf_reader_recovery_fixture.py
```

---

## 38. Generated output policy

Reader demo output should go under:

```text
output/amcf_reader_recovery_fixture/
```

Possible files:

```text
reader_capture_normalized.json
recovered_sections.json
reader_recovery_report.json
rescan_requests.json
reprint_requests.json
READER_RECOVERY_SUMMARY.md
```

Do not commit generated output.

Fixtures should go under a controlled fixture path only if needed.

---

## 39. Reader fixture shape

A minimal reader fixture should include:

```json id="epgpbp"
{
  "capture_id": "capture_0001",
  "source_print_manifest_id": "print_manifest_fixture_001",
  "candidate_section_id": "section_0001",
  "observed_section_id": "section_0001",
  "observed_hash": "expected_hash_value",
  "detected_lanes": {
    "timing_index_lane": "present",
    "registration_lane": "present",
    "colour_reference_lane": "present",
    "metadata_transform_lane": "present",
    "hash_checksum_lane": "present"
  },
  "damage_status": "none"
}
```

A failure fixture should include:

```json id="ios8o5"
{
  "capture_id": "capture_hash_mismatch",
  "candidate_section_id": "section_0002",
  "observed_section_id": "section_0002",
  "observed_hash": "wrong_hash",
  "detected_lanes": {
    "timing_index_lane": "present",
    "registration_lane": "present",
    "colour_reference_lane": "present",
    "metadata_transform_lane": "present",
    "hash_checksum_lane": "present"
  },
  "damage_status": "suspected"
}
```

This gives deterministic recovery tests.

---

## 40. Reader should not rely on OCR

The reader should not depend on OCR as its main recovery mechanism.

Reasons:

```text
- OCR is fragile
- section IDs should be encoded structurally
- hash/checksum lanes should be machine-readable
- registration and timing should not depend on natural-language text
```

Human-readable labels may be useful for debugging, but the software should rely on structured lanes.

---

## 41. Reader and colour degradation

Colour degradation should be treated carefully.

Possible statuses:

```text
colour_ok
colour_warning
colour_degraded_but_usable
colour_unusable
not_checked
```

A colour warning may not always block recovery.

But a critical colour/payload failure may require:

```text
rescan
reprint
manual review
```

The reader should record the distinction.

---

## 42. Reader and registration failure

Registration failure may have levels.

```text
minor_skew_warning
scale_warning
crop_warning
registration_failed
```

A minor warning may allow recovery.

A critical registration failure should block recovery or require rescan.

Do not silently accept a badly skewed section as valid.

---

## 43. Reader and hash mismatch

Hash mismatch should be critical unless the manifest says otherwise.

Decisions:

```text
hash match → recovered
hash unreadable → rescan
hash mismatch → rescan or reprint
hash missing where required → fail recovery
```

No silent acceptance.

---

## 44. Reader and manifest mismatch

Manifest mismatch occurs when:

```text
capture claims manifest A
but expected print manifest is B
```

or:

```text
section belongs to another package
```

Decision:

```text
manual_review_required
wrong_package_or_manifest
do not merge into recovered package automatically
```

---

## 45. Reader and duplicate sections

Duplicate detection matters.

Example:

```text
section_0007 appears twice
section_0008 missing
```

The reader should report:

```text
duplicate_section_count
missing_section_count
```

It should not assume the duplicate is harmless.

---

## 46. Reader and package reconstruction

Later, once recovery is stable, reader software can rebuild:

```text
RecoveredAMCFPackage
```

But reconstruction should require:

```text
- enough valid sections
- manifest consistency
- hash consistency
- missing-section report
- recovery confidence
```

Do not reconstruct silently if critical pieces are missing.

---

## 47. Reader as archive/recovery tool

PC ↔ Reader is not only for the future physical player.

It is also an archive/recovery tool.

Use cases:

```text
- recover old printed AMCF carrier
- verify a printed carrier is intact
- diagnose damaged sections
- rebuild missing package metadata
- compare physical output to digital manifest
```

This makes the reader corridor important even before physical-player hardware exists.

---

## 48. Reader implementation should come after print manifest basics

The strongest order is:

```text
1. shared package/manifest model
2. print layout manifest
3. simulated reader capture from print manifest
4. reader recovery fixture
5. image input later
```

Reader recovery needs a source of expected layout and section data.

So PC ↔ Reader should follow or pair with the PC → Printer prototype.

---

## 49. What should remain future

Do not start with:

```text
- real scanner hardware
- TWAIN/WIA/SANE integration
- camera calibration
- complex computer vision
- QR/barcode dependency
- OCR-based section recovery
- automatic damaged-image repair
- real-time player prefetch hardware
```

Those can be researched later.

First build:

```text
print-manifest-assisted fixture recovery
```

---

## 50. What Part 7 decides

Part 7 decides:

```text
- PC ↔ Reader is a full software corridor
- it is distinct from physical-player visible playback
- the first reader implementation should be no-hardware and fixture-based
- reader recovery should use print-manifest-assisted validation first
- reader software should model capture, section detection, lane extraction, validation, recovery, rescan, and reprint
- AMCFReaderCapture and AMCFRecoveredSection are central objects
- reader reports should include unsafe_acceptance_count and claim-boundary flags
- hash mismatch, wrong section, missing critical lane, and manifest mismatch must not be silently accepted
- OCR should not be the primary recovery method
- real scanner/image-processing work should come later
```

---

## 51. What Part 8 should continue with

Part 8 should continue into:

```text
Player ↔ PC software path
```

That should cover:

```text
- player corridor purpose
- PC-side player simulator
- package-to-player runtime adapter
- player capability profiles
- mechanism profile negotiation
- command/report model
- fail-closed runtime decisions
- reverse/seek command limits
- diagnostics/logging
- future device protocol boundary
- first implementation target
```

----
# AMCF Software Development and I/O Control Dossier  
## Part 8 — Player ↔ PC Software Path: Package Control, Runtime Simulation, Capability Profiles, Diagnostics, and Future Protocol Boundary

## 1. Purpose of Part 8

Part 6 covered:

```text
PC → Printer
```

Part 7 covered:

```text
PC ↔ Reader
```

Part 8 now covers:

```text
Player ↔ PC
```

This is the software corridor around the AMCF physical player.

The attached physical-player dossier describes the corrected player branch as a compact tablet-like optical player with a folded internal indexed media path, side-loaded cartridge/card/section stack, visible view gate, hidden preload/staging gate, shutter/illumination blanking, reader/prefetch lanes, dynamic AMCF schedule, and physical/optical viewing window. The software question is:

```text
How does PC software prepare, simulate, control, verify, log, and eventually communicate with an AMCF physical player?
```

This is not the same as:

```text
making real hardware work today
```

It is the software path that gets the project ready for player control, while still staying honest that the physical hardware does not exist yet.

---

## 2. Correct boundary

The Player ↔ PC corridor should be defined as:

```text
Software that lets the PC prepare AMCF package/player data, simulate player execution, validate player capability, model commands and responses, generate diagnostics and playback reports, and later provide a safe bridge to real player hardware.
```

It should not initially be defined as:

```text
USB hardware control
firmware control
real motor control
real sensor control
real cartridge detection
```

Those are future hardware-interface layers.

The first Player ↔ PC software should be:

```text
PC-side package/runtime simulator
+ player capability model
+ command/report model
+ diagnostics
+ future protocol placeholder
```

---

## 3. Why this corridor is bidirectional

It is:

```text
Player ↔ PC
```

not only:

```text
PC → Player
```

because the PC and player exchange different types of information.

The PC may send or prepare:

```text
- AMCF package
- manifest
- playback schedule
- physical section list
- cartridge manifest
- player profile
- mechanism profile
- playback command
- pause / resume / step / reverse / seek request
- diagnostic request
- calibration profile later
```

The player or simulated player reports back:

```text
- cartridge recognized
- section verified
- current state
- visible section
- staged section
- fail-closed reason
- reverse/seek denial
- playback timeline
- diagnostic logs
- unsafe acceptance count
- completion/failure report
```

So this is a control/report corridor.

---

## 4. Current status of this corridor

This is the most developed corridor so far.

The current repo already has a physical-player software/control foundation:

```text
- state machine
- fail-closed logic
- reverse/seek controls
- mechanism profiles
- integrated simulator demo
- public docs/release review/checks
```

But it does not yet have the full Player ↔ PC software corridor.

What exists is mainly:

```text
physical-player simulator/control foundation
```

What is still missing:

```text
- package-to-player runtime adapter
- player capability profile model
- simulated PC/player session model
- command schema
- player response schema
- diagnostic log schema
- package compatibility report
- future hardware protocol boundary
```

So the next Player ↔ PC work should extend the existing simulator rather than replace it.

---

## 5. The key Player ↔ PC software chain

The software chain should be:

```text
AMCFPackage
→ AMCFManifest
→ AMCFPlaybackSchedule
→ AMCFPhysicalSection list
→ AMCFPlayerSection list
→ PlayerCapabilityProfile
→ MechanismProfileReference
→ PlayerRuntimeSession
→ State-machine execution
→ Playback / safety / diagnostics report
```

This connects Part 4’s shared model to the existing physical-player simulator.

The physical-player dossier’s event model already includes fields like timestamp, visible section, next section, dwell time, preload deadline, transition blank time, and verified-next-section requirement. The Player ↔ PC software must preserve those fields because the player must decide:

```text
Can I execute this update safely?
Is the next section ready?
Is it verified?
Is the A/B gate ready?
Is the audio sync still acceptable?
Should I continue, pause, or fail closed?
```

Those questions are directly identified in the physical-player plan. ---

## 6. Player ↔ PC should begin with simulation

Because there is no real player hardware yet, the first implementation target should be:

```text
PC-side simulated player session
```

That means:

```text
- no real device needed
- no USB needed
- no firmware needed
- no sensor input needed
- no motor control needed
```

Instead, the simulated player receives:

```text
- package/manifest data
- update events
- physical/player sections
- mechanism profile
- capability profile
- command sequence
```

Then outputs:

```text
- playback timeline
- state transitions
- fail-closed events
- reverse/seek decisions
- diagnostics
- final report
```

This lets AMCF develop the Player ↔ PC software safely before hardware exists.

---

## 7. Difference between physical-player simulator and Player ↔ PC corridor

The existing physical-player simulator models internal playback logic:

```text
visible gate
hidden staging gate
preload
verify
transition blank
switch section
park old section
reverse/seek
fail closed
```

The Player ↔ PC corridor wraps that simulator in a wider software context:

```text
PC package loading
→ player compatibility check
→ command/session setup
→ simulator execution
→ player report/diagnostics
→ future hardware protocol boundary
```

So the Player ↔ PC corridor is not a replacement for the simulator.

It is the software system around the simulator.

---

## 8. Core objects for Player ↔ PC

The Player ↔ PC corridor needs these main objects:

```text
AMCFPlayerProfile
AMCFPlayerCapabilityProfile
AMCFPlayerRuntimeSession
AMCFPlayerCommand
AMCFPlayerResponse
AMCFPlayerStateSnapshot
AMCFPlayerDiagnosticEvent
AMCFPlayerPlaybackReport
AMCFPlayerProtocolEnvelope
```

Some of these may begin as dictionaries or JSON structures.

They do not all need to become classes immediately.

But the concepts should be separate.

---

# AMCFPlayerProfile

## 9. Purpose

`AMCFPlayerProfile` describes a player model.

At first this is simulated.

Later it may represent real hardware.

It should answer:

```text
What kind of player is this software targeting?
```

## 10. Required fields

```text
player_profile_id
player_profile_version
player_type
supported_manifest_versions
supported_section_versions
supported_mechanism_profiles
default_mechanism_profile_id
supports_audio_sync
supports_reverse
supports_local_seek
supports_arbitrary_seek
supports_reader_prefetch
supports_diagnostics
hardware_backed
hardware_validated
physical_level_5_claimed
metadata
```

For now:

```text
hardware_backed = false
hardware_validated = false
physical_level_5_claimed = false
```

---

# AMCFPlayerCapabilityProfile

## 11. Purpose

`AMCFPlayerCapabilityProfile` describes what a player can handle.

It should answer:

```text
Can this player profile execute this AMCF package safely?
```

## 12. Required capability fields

```text
max_section_count
min_update_spacing_ms
max_required_prefetch_ahead_ms
supported_transition_blank_ms_range
supported_reverse_buffer_depth
supported_seek_mode
supported_lane_requirements
supported_hash_algorithms
supported_colour_reference_modes
supported_registration_modes
audio_sync_tolerance_ms
fail_closed_required
```

This object matters because some AMCF packages may be too demanding for a given player profile.

Example:

```text
Package requires 12 ms section transitions.
Player profile only supports 40 ms safe minimum.
→ compatibility warning or fail.
```

This does not require hardware.

It is a software compatibility check.

---

# AMCFPlayerRuntimeSession

## 13. Purpose

`AMCFPlayerRuntimeSession` represents one playback/control session.

It should answer:

```text
What package was loaded, what player profile was used, what commands occurred, what states happened, and how did the session end?
```

## 14. Required fields

```text
session_id
package_id
manifest_id
player_profile_id
mechanism_profile_id
started_at
commands
state_snapshots
diagnostic_events
playback_timeline
fail_closed_decisions
reverse_seek_events
unsafe_acceptance_count
final_status
report_ref
metadata
```

The runtime session is the bridge between package data and report output.

---

# AMCFPlayerCommand

## 15. Purpose

`AMCFPlayerCommand` records what the PC asks the player or simulated player to do.

Initial commands:

```text
load_package
recognize_cartridge
prepare_playback
play
pause
resume
step_forward
step_backward
reverse
seek_local
seek_absolute
stop
request_diagnostics
export_report
```

Important:

```text
seek_absolute should be denied by default unless the player profile explicitly supports it.
```

The physical-player design supports limited reverse/short step-back first, not arbitrary instant seek across the whole cartridge.

## 16. Command fields

```text
command_id
command_type
timestamp_ms
target_section_id
target_event_id
parameters
issued_by
requires_safety_check
metadata
```

---

# AMCFPlayerResponse

## 17. Purpose

`AMCFPlayerResponse` records how the player or simulator responded.

Fields:

```text
response_id
command_id
accepted
executed
denied
denial_reason
state_after_command
diagnostic_event_refs
fail_closed_decision_ref
metadata
```

Example:

```text
command: seek_absolute section_0500
response: denied
denial_reason: arbitrary_seek_not_supported
```

This should be tested.

---

# AMCFPlayerStateSnapshot

## 18. Purpose

`AMCFPlayerStateSnapshot` records player state at a moment.

Fields:

```text
snapshot_id
timestamp_ms
state
visible_section_id
hidden_staging_section_id
current_event_id
next_event_id
visible_gate_locked
hidden_gate_ready
prefetch_status
verification_status
audio_sync_status
reverse_buffer_section_ids
fail_closed_reason
metadata
```

The physical-player dossier already identifies state-machine stages such as prefetch, verify, load view gate, view gate locked, playback ready, prefetch next, verify next, stage next, wait update timestamp, transition blank, switch visible section, and park old section. Those states should be visible in player snapshots or playback timelines.

---

# AMCFPlayerDiagnosticEvent

## 19. Purpose

`AMCFPlayerDiagnosticEvent` records what happened inside the player/simulator.

Examples:

```text
cartridge_recognized
manifest_loaded
section_prefetched
section_verified
view_gate_locked
transition_blank_started
visible_section_switched
old_section_parked
reverse_buffer_updated
command_denied
fail_closed_triggered
audio_sync_warning
```

Fields:

```text
diagnostic_event_id
timestamp_ms
event_type
severity
section_id
event_id
message
details
metadata
```

Diagnostics are essential for debugging AMCF playback.

---

# AMCFPlayerPlaybackReport

## 20. Purpose

`AMCFPlayerPlaybackReport` summarizes the session.

Fields:

```text
run_name
session_id
package_id
manifest_id
player_profile_id
mechanism_profile_id
event_count
section_count
commands_count
state_snapshot_count
diagnostic_event_count
visible_switch_count
fail_closed_event_count
reverse_attempt_count
reverse_success_count
reverse_denial_count
seek_attempt_count
seek_success_count
seek_denial_count
unsafe_acceptance_count
final_passed
claim_boundary_flags
```

This report should preserve the existing style of JSON + Markdown summary.

---

# AMCFPlayerProtocolEnvelope

## 21. Purpose

`AMCFPlayerProtocolEnvelope` is a future-proof wrapper for commands/responses.

Even before hardware exists, the PC/player software can define a file-based protocol shape.

Example:

```json id="4k2fpi"
{
  "protocol_version": "0.1",
  "message_type": "command",
  "message_id": "cmd_0001",
  "session_id": "session_001",
  "payload": {
    "command_type": "play"
  }
}
```

This does not mean real hardware communication exists.

It means:

```text
future device protocol messages can be simulated and tested as files first.
```

---

## 22. Package-to-player runtime adapter

The first major Player ↔ PC implementation should probably be:

```text
package/manifest → player runtime adapter
```

This adapter converts:

```text
AMCFManifest
AMCFUpdateEvent
AMCFPhysicalSection
```

into:

```text
AMCFPlayerSection
PlayerRuntimeSession input
```

It should not replace the existing state machine.

It should feed it.

Suggested future module:

```text
src/amcf_player_runtime_adapter.py
```

or:

```text
src/amcf_physical_player_runtime_adapter.py
```

The exact name should follow repo conventions after audit.

---

## 23. Player section mapping

The adapter should map each AMCF physical section into a runtime player section.

Input fields:

```text
section_id
section_index
event_id
timestamp_start_ms
dwell_ms
hash/checksum status
registration status
colour status
metadata status
```

Runtime output fields:

```text
player_section_id
physical_section_id
event_id
timestamp_start_ms
dwell_ms
preload_required_by_ms
verification_deadline_ms
transition_blank_ms
verified_before_display
gate_lock_required
display_allowed
reverse_buffer_eligible
seek_eligible
fail_closed_reason
```

The physical-player plan’s event fields already include `preload_required_by_ms`, `transition_blank_ms`, and `requires_verified_next_section`. The adapter should carry these into player runtime.

---

## 24. Player compatibility check

Before playback, the PC should check package compatibility.

Inputs:

```text
AMCFManifest
AMCFPlaybackSchedule
AMCFPhysicalSection list
AMCFPlayerCapabilityProfile
MechanismProfileReference
```

Checks:

```text
- manifest schema supported
- section schema supported
- update-event spacing within capability
- preload deadlines realistic for selected profile
- transition blank duration supported
- required lanes present
- required hash algorithms supported
- reverse/seek assumptions compatible
- audio sync tolerance compatible
```

Output:

```text
player_compatibility_report.json
```

This report should not claim hardware validation.

It should say:

```text
compatible with simulated profile
```

not:

```text
compatible with real player hardware
```

---

## 25. Mechanism profile selection

The current default mechanism profile is:

```text
folded_ab_motor_encoder_baseline
```

The Player ↔ PC software should use mechanism profiles as assumptions.

It should report:

```text
selected_profile_id
carrier_layout
staging_model
actuator_family
gate_model
prefetch_model
reverse_model
seek_model
safety_model
hardware_validated
physical_level_5_claimed
```

For now:

```text
hardware_validated = false
physical_level_5_claimed = false
```

Mechanism profiles help simulate capability.

They do not prove hardware.

---

## 26. Player command model

The Player ↔ PC corridor should model commands even before hardware exists.

First command set:

```text
load_package
prepare_playback
play
pause
resume
step_forward
step_backward
reverse_one
seek_local
seek_absolute
stop
request_report
```

Required command rules:

```text
- load_package must validate manifest first
- prepare_playback must build player sections
- play must not display unverified section
- step_forward must require verified next section
- reverse_one must require reverse buffer
- seek_local must require local buffered section
- seek_absolute must deny by default
- stop must leave safe final state
```

This command model can later become protocol messages.

---

## 27. Playback state model

The runtime should reuse existing state-machine concepts.

Core states:

```text
EMPTY
PACKAGE_LOADED
CARTRIDGE_RECOGNIZED
PREFETCH_CURRENT
VERIFY_CURRENT
LOAD_VIEW_GATE
VIEW_GATE_LOCKED
PLAYBACK_READY
PREFETCH_NEXT
VERIFY_NEXT
STAGE_NEXT
WAIT_UPDATE_TIMESTAMP
TRANSITION_BLANK
SWITCH_VISIBLE_SECTION
PARK_OLD_SECTION
PAUSED
REVERSE_READY
SEEKING
FAIL_CLOSED
STOPPED
```

The physical-player dossier includes a gate-level state machine with states like EMPTY, CARTRIDGE_INSERTED, SECTION_PREFETCH, SECTION_STAGED, SECTION_VERIFIED, VISIBLE_LOCKED, TRANSITION_BLANK, SECTION_SWITCH, OLD_SECTION_PARK, NEXT_PREFETCH, PAUSED, REVERSE_READY, SEEKING, and FAIL_CLOSED. The software can adapt names, but it should preserve the logic.

---

## 28. Normal playback cycle

Normal Player ↔ PC simulated playback should look like:

```text
load_package
→ validate manifest
→ build player sections
→ select mechanism profile
→ check capability
→ prefetch current section
→ verify current section
→ load view gate
→ lock visible gate
→ prefetch next section
→ verify next section
→ wait update timestamp
→ transition blank
→ switch visible section
→ park old section
→ repeat
```

This mirrors the physical-player dossier’s normal playback cycle where the section is prefetched, staged, verified, locked visible, transition blank occurs, the visible section switches, and the old section parks. ---

## 29. Failure cycle

Failure branch:

```text
prefetch next
→ next section missing / wrong / hash mismatch / lane unreadable
→ verification fails
→ transition denied
→ display not changed
→ pause/blank/fail closed
→ diagnostic event recorded
→ fail-closed report generated
```

The software must not show or accept the wrong section.

The physical-player dossier repeatedly preserves fail-closed logic and zero unsafe acceptance. It explicitly states that `unsafe_acceptance_count` must remain zero. So Player ↔ PC reports must include this field.

---

## 30. Reverse / seek cycle

Reverse should be bounded.

Supported first:

```text
step back to previous verified section in local reverse buffer
```

Not supported first:

```text
arbitrary seek across the whole cartridge
```

Reverse cycle:

```text
reverse command
→ check reverse buffer
→ if previous section verified, stage it
→ transition blank
→ switch visible section
→ update buffer
```

The physical-player dossier includes a reverse cycle where a reverse request checks the reverse buffer, preloads a previous verified section, transition blank happens, the previous section becomes visible, and the old section is parked. Player ↔ PC software should report:

```text
reverse_attempt_count
reverse_success_count
reverse_denial_count
seek_attempt_count
seek_success_count
seek_denial_count
arbitrary_seek_denied_count
```

---

## 31. Audio sync

The Player ↔ PC corridor should include audio sync reporting.

Even before audio playback is implemented, the runtime model should track:

```text
audio_sync_reference
audio_sync_tolerance_ms
visual_schedule_position_ms
audio_position_ms
drift_ms
audio_sync_status
```

Possible statuses:

```text
in_sync
warning
drift_exceeded
not_checked
```

If audio drift exceeds tolerance, possible decisions:

```text
continue_with_warning
pause
resync
fail_closed
```

Do not overbuild audio yet.

But include fields so the model does not ignore it.

---

## 32. Diagnostics and logging

Diagnostics are central to Player ↔ PC.

Logs should capture:

```text
- package loaded
- manifest parsed
- player profile selected
- mechanism profile selected
- compatibility check passed/failed
- section prefetched
- section verified
- view gate locked
- transition blank started
- visible section switched
- old section parked
- reverse buffer updated
- command denied
- fail-closed triggered
```

Logs should be structured JSON.

Human-readable Markdown summaries should be generated from them.

---

## 33. Capability negotiation

Real capability negotiation is future hardware work.

But simulated capability negotiation can begin now.

A file-based capability profile can say:

```json id="cudmt9"
{
  "player_profile_id": "sim_folded_ab_player_v1",
  "supported_manifest_versions": ["1.0"],
  "default_mechanism_profile_id": "folded_ab_motor_encoder_baseline",
  "supports_reverse": true,
  "supports_local_seek": true,
  "supports_arbitrary_seek": false,
  "hardware_backed": false,
  "hardware_validated": false
}
```

The PC then checks:

```text
Can this profile run this package?
```

This is useful now and later.

---

## 34. Cartridge recognition model

The physical-player plan uses a side/top cartridge and carrier recognition/index reading in the concept.

Software should model cartridge recognition without real hardware.

A simulated cartridge recognition step should check:

```text
cartridge_id
package_id
manifest_id
section_count
section_index_range
hash_manifest
schema_version
compatibility profile
```

Possible statuses:

```text
recognized
recognized_with_warning
unknown_cartridge
manifest_mismatch
section_count_mismatch
unsupported_schema
```

This prepares for future hardware while remaining file-based.

---

## 35. Package compatibility report

Before simulated playback, produce:

```text
player_package_compatibility_report.json
```

Fields:

```text
package_id
manifest_id
player_profile_id
mechanism_profile_id
compatible
warnings
errors
unsupported_features
min_update_spacing_ms
profile_min_update_spacing_ms
reverse_supported
local_seek_supported
arbitrary_seek_supported
required_lanes_present
hash_algorithm_supported
final_passed
claim_boundary_flags
```

This report should be a gate before runtime playback.

---

## 36. Player runtime report

After simulated playback, produce:

```text
player_runtime_report.json
```

Fields:

```text
session_id
package_id
manifest_id
player_profile_id
mechanism_profile_id
command_count
state_transition_count
visible_switch_count
fail_closed_event_count
reverse_attempt_count
seek_attempt_count
unsafe_acceptance_count
final_state
final_passed
claim_boundary_flags
```

Also produce:

```text
PLAYER_RUNTIME_SUMMARY.md
```

---

## 37. Command/response transcript

The Player ↔ PC corridor should eventually produce a transcript:

```text
player_command_response_transcript.json
```

Example:

```json id="683yz2"
[
  {
    "command": "load_package",
    "accepted": true,
    "state_after": "PACKAGE_LOADED"
  },
  {
    "command": "play",
    "accepted": true,
    "state_after": "PLAYBACK_READY"
  },
  {
    "command": "seek_absolute",
    "accepted": false,
    "denial_reason": "arbitrary_seek_not_supported"
  }
]
```

This will be useful for later PC UI and device protocol work.

---

## 38. Future protocol boundary

The file-based command/response model should be designed so it can later map to real transport.

Possible future transports:

```text
JSON-over-serial
USB HID
USB bulk protocol
local network protocol
firmware RPC
```

But current implementation should use:

```text
JSON files and simulator calls
```

Do not add hardware protocol dependencies now.

---

## 39. PC application role

Eventually the PC software may have a user-facing app.

But the first Player ↔ PC implementation should be CLI/report based.

Later UI can consume:

```text
- compatibility reports
- runtime reports
- diagnostic logs
- command transcripts
- playback timelines
```

The UI should not be the source of truth.

The reports should be.

---

## 40. Safety model

The Player ↔ PC corridor must be strict.

Unsafe acceptance means:

```text
- unverified section displayed
- wrong section accepted
- hash mismatch accepted
- missing critical lane accepted
- unsupported seek accepted
- unsupported package treated as playable
- gate not locked but display allowed
- fail-closed condition ignored
```

All reports should include:

```text
unsafe_acceptance_count
```

And it must remain:

```text
0
```

This keeps the corridor aligned with the physical-player safety invariant. ---

## 41. Claim-boundary fields

Every Player ↔ PC report should include:

```text
physical_hardware_claimed
hardware_validation_claimed
physical_level_5_claimed
manufactured_player_claimed
real_sensors_required
real_motors_required
real_cartridges_required
real_scans_required
```

For current software:

```text
all false
```

Player ↔ PC software can claim:

```text
simulated player profile compatibility
simulated runtime playback
simulated fail-closed decision
simulated reverse/seek denial
```

It cannot claim:

```text
real physical player hardware validation
```

---

## 42. First implementation target for Player ↔ PC

The first Player ↔ PC implementation should be:

```text
AMCF player runtime package-control fixture prototype
```

Suggested future run name:

```text
AMCF_PLAYER_PC_RUNTIME_CONTROL_FIXTURE_V1
```

Purpose:

```text
Use a deterministic AMCF manifest/package fixture and simulated player capability profile to run the existing physical-player state machine through a PC/player command session.
```

Inputs:

```text
- fixture AMCF manifest
- fixture physical sections
- simulated player profile
- default mechanism profile
- command script
```

Outputs:

```text
- player_package_compatibility_report.json
- player_runtime_report.json
- player_command_response_transcript.json
- player_diagnostics.json
- PLAYER_RUNTIME_SUMMARY.md
```

No hardware.

No device protocol.

No GUI.

---

## 43. Suggested future modules

Future implementation may create:

```text
src/amcf_player_profile.py
src/amcf_player_runtime_adapter.py
src/amcf_player_session.py
src/amcf_player_commands.py
src/amcf_player_reports.py
```

But if the repo already has similar modules, Codex should adapt existing structures.

Do not create duplicates before repo audit.

---

## 44. Suggested future demos

Possible demos:

```text
demo/run_amcf_player_pc_runtime_fixture_demo.py
demo/run_amcf_player_package_compatibility_demo.py
demo/run_amcf_player_command_session_demo.py
```

Later:

```text
demo/run_amcf_player_protocol_simulation_demo.py
```

---

## 45. Suggested future tests

Tests should verify:

```text
- player profile loads
- capability profile validates
- manifest/package fixture loads
- player sections are built from physical sections
- compatibility report passes for valid fixture
- compatibility report fails for unsupported schedule
- command session accepts play
- command session denies arbitrary seek
- reverse succeeds only with buffer
- reverse denied without buffer
- unverified section triggers fail-closed
- hash mismatch triggers fail-closed
- unsafe_acceptance_count remains 0
- hardware claim booleans false
```

Likely test file:

```text
tests/test_amcf_player_pc_runtime_fixture.py
```

---

## 46. Generated output policy

Player ↔ PC demo output should go under:

```text
output/amcf_player_pc_runtime_fixture/
```

Possible files:

```text
player_package_compatibility_report.json
player_runtime_report.json
player_command_response_transcript.json
player_diagnostics.json
PLAYER_RUNTIME_SUMMARY.md
```

Do not commit generated output.

Fixtures should live under a controlled fixture path only if needed.

---

## 47. Relationship to PC → Printer

Player ↔ PC needs data that PC → Printer also uses.

Shared objects:

```text
AMCFManifest
AMCFUpdateEvent
AMCFPhysicalSection
hash/checksum data
section IDs
timing data
```

The print path creates physical sections and lanes.

The player path simulates whether those sections can be played.

Long-term loop:

```text
PC → Printer creates carrier sections.
Player ↔ PC checks whether the package/carrier schedule is playable.
```

---

## 48. Relationship to PC ↔ Reader

Reader reports can affect player safety.

Example:

```text
Reader says section_0007 hash mismatch.
Player ↔ PC should mark section_0007 unsafe to display.
```

Example:

```text
Reader says section_0009 colour warning only.
Player ↔ PC may allow display with warning depending on profile.
```

So Player ↔ PC should eventually consume reader validation status.

Long-term loop:

```text
PC ↔ Reader validates carrier.
Player ↔ PC uses reader validation to decide playback safety.
```

---

## 49. Relationship to physical-player mechanism profiles

Player ↔ PC should not ignore mechanism assumptions.

Mechanism profile affects:

```text
- preload timing
- transition blank support
- reverse buffer depth
- local seek support
- fail-closed behaviour
- unsupported capability detection
```

But mechanism profile is still a software assumption.

It is not hardware proof.

---

## 50. What should remain future

Do not start with:

```text
- USB player detection
- firmware protocol
- real motor control
- real sensor polling
- live hardware playback
- GUI player dashboard
- automatic cartridge hardware recognition
- real-time audio playback sync
```

Those can come after:

```text
- shared manifest model
- package-to-player adapter
- player profile model
- command/report model
- simulated runtime session
```

---

## 51. What Part 8 decides

Part 8 decides:

```text
- Player ↔ PC is the most developed corridor but still needs a full software wrapper
- the existing physical-player simulator should be reused, not replaced
- the first implementation should be simulated/file-based, not hardware-based
- player profiles and capability profiles are needed
- package compatibility checks are needed before playback
- player command/response schemas should be modeled before real protocols
- runtime session reports and diagnostics should be first-class outputs
- reverse/seek must remain bounded
- arbitrary seek should be denied by default
- unsafe_acceptance_count must remain zero
- hardware claim booleans must remain false
- future hardware protocols should be designed only after file-based command/report models work
```

---

## 52. What Part 9 should continue with

Part 9 should continue into the shared cross-corridor layer:

```text
Cross-corridor reports, logs, safety, validation, and audit model
```

That should cover:

```text
- shared report structure
- shared validation result structure
- shared fail-closed decision structure
- unsafe_acceptance_count across all corridors
- claim-boundary booleans
- generated-output policy
- local-path scan policy
- error/warning/severity vocabulary
- report compatibility across PC → Printer, PC ↔ Reader, and Player ↔ PC
```

----
# AMCF Software Development and I/O Control Dossier  
## Part 9 — Cross-Corridor Reports, Logs, Safety, Validation, and Audit Model

## 1. Purpose of Part 9

Parts 6–8 defined the three main software corridors:

```text
Part 6 — PC → Printer
Part 7 — PC ↔ Reader
Part 8 — Player ↔ PC
```

Part 9 now defines the shared safety/reporting layer that sits across all three.

This matters because AMCF cannot have separate, incompatible report systems for each corridor.

The same safety logic needs to appear everywhere:

```text
PC → Printer:
do not generate unsafe or unverifiable physical carrier output.

PC ↔ Reader:
do not accept corrupted or wrong physical sections as valid.

Player ↔ PC:
do not display or simulate display of unverified sections.
```

The physical-player dossier already uses the key invariant:

```text
unsafe_acceptance_count must remain zero
```

That rule is explicit in the source dossier. Part 9 expands that into a shared software reporting and audit model.

---

## 2. Why this layer is needed

Without a shared reporting layer, each corridor may invent its own terms:

```text
Printer:
layout_ok, print_good, export_passed

Reader:
scan_ok, recovered, partial_fail

Player:
safe, fail_closed, display_denied
```

That creates confusion.

Instead, the software should use shared report concepts:

```text
AMCFReport
AMCFValidationResult
AMCFFailClosedDecision
AMCFAuditEvent
AMCFClaimBoundaryFlags
AMCFGeneratedOutputStatus
AMCFLineageRecord
```

The corridors can have their own specific report fields, but the core vocabulary should stay consistent.

---

## 3. Cross-corridor safety principle

The shared rule should be:

```text
A corridor may warn, deny, rescan, reprint, pause, or fail closed,
but it must not silently accept a critical unsafe condition.
```

In practice:

```text
PC → Printer:
Do not silently generate a print package with missing lanes, duplicate section IDs, invalid margins, or bad hashes.

PC ↔ Reader:
Do not silently mark a wrong, corrupted, unreadable, or mismatched section as valid.

Player ↔ PC:
Do not silently allow an unverified, wrong, unsupported, or unsafe section to be displayed.
```

The physical-player dossier’s safety language is strongest around player logic, but the same invariant should become a whole-software invariant.

---

## 4. Central shared report object: AMCFReport

Every major run should produce an `AMCFReport`.

This should be the base report structure for:

```text
- repo audit
- shared model audit
- printer layout/export
- reader capture/recovery
- player runtime/control
- release refresh
- package validation
- compatibility checks
```

## 4.1 Required common fields

```text
report_id
run_name
created_at
tool_name
tool_version
repo_head
repo_branch
input_refs
output_refs
final_passed
summary
counts
validation_results
fail_closed_decisions
audit_events
unsafe_acceptance_count
claim_boundary_flags
generated_output_status
local_path_scan_status
unsafe_hardware_claim_scan_status
lineage
metadata
```

Not every early implementation needs every field immediately, but the structure should move in this direction.

---

## 5. Corridor-specific report types

The base `AMCFReport` can be specialised by corridor.

```text
AMCFPrintReport
AMCFReaderRecoveryReport
AMCFPlayerRuntimeReport
AMCFRepoAuditReport
AMCFPackageValidationReport
```

These should all share:

```text
final_passed
validation_results
unsafe_acceptance_count
claim_boundary_flags
generated_output_status
```

That way, a later tool can compare reports across corridors.

---

# PC → Printer Reporting

## 6. Printer report purpose

A printer report should answer:

```text
Was this AMCF package converted into a valid printable physical carrier layout?
```

It should not answer:

```text
Was the physical carrier printed perfectly?
Can real hardware play it?
```

Those require later physical validation.

## 7. Printer report fields

Suggested printer report:

```text
print_audit_report.json
```

Fields:

```text
run_name
source_package_id
source_manifest_id
print_package_id
print_profile_id
sheet_count
print_section_count
update_event_count
layout_valid
margins_valid
section_ids_unique
section_event_map_valid
payload_bounds_valid
lane_bounds_valid
registration_marks_present
colour_reference_present
metadata_lane_present
hash_checksum_lane_present
hash_algorithm
reprint_index_created
generated_exports
validation_results
warnings
errors
unsafe_acceptance_count
claim_boundary_flags
final_passed
```

## 8. Printer unsafe acceptance

Printer unsafe acceptance includes:

```text
- missing section accepted
- duplicate section ID accepted
- event-to-section mismatch accepted
- section printed outside margins
- payload/lane overlap accepted
- required hash lane missing
- required registration lane missing
- invalid schema version accepted
- report says passed despite critical validation failure
```

If any of these happen, the report should not be passed.

---

# PC ↔ Reader Reporting

## 9. Reader report purpose

A reader report should answer:

```text
Was the captured physical AMCF carrier input recovered, validated, diagnosed, or rejected correctly?
```

It should track both recovery and safety.

## 10. Reader report fields

Suggested reader report:

```text
reader_recovery_report.json
```

Fields:

```text
run_name
source_manifest_id
source_print_manifest_id
capture_count
candidate_section_count
recovered_section_count
valid_section_count
warning_section_count
rescan_required_count
reprint_required_count
manual_review_required_count
unrecoverable_count
hash_mismatch_count
registration_failed_count
wrong_section_count
duplicate_section_count
missing_section_count
manifest_mismatch_count
validation_results
rescan_requests
reprint_requests
unsafe_acceptance_count
claim_boundary_flags
final_passed
```

The reader/prefetch lane requirements in the physical-player dossier include section index, timing marks, registration marks, colour reference, metadata/transform lane, hash/checksum lane, and damage/missing marker status. The reader report should therefore show whether those expected lane categories were detected, extracted, simulated, missing, or invalid.

## 11. Reader unsafe acceptance

Reader unsafe acceptance includes:

```text
- wrong section marked valid
- hash mismatch marked valid
- critical lane missing but section accepted
- unreadable metadata accepted as clean
- manifest mismatch accepted silently
- duplicate section ignored
- damaged payload accepted without warning
- rescan-needed section treated as recovered
```

Reader software should be strict.

If recovery is uncertain, it should say so.

---

# Player ↔ PC Reporting

## 12. Player report purpose

A player report should answer:

```text
Could the simulated player profile execute this AMCF package safely under the selected mechanism/profile assumptions?
```

It should not answer:

```text
Did real hardware play it?
```

## 13. Player report fields

Suggested reports:

```text
player_package_compatibility_report.json
player_runtime_report.json
player_command_response_transcript.json
player_diagnostics.json
```

Runtime report fields:

```text
run_name
session_id
package_id
manifest_id
player_profile_id
mechanism_profile_id
command_count
state_transition_count
visible_switch_count
fail_closed_event_count
reverse_attempt_count
reverse_success_count
reverse_denial_count
seek_attempt_count
seek_success_count
seek_denial_count
arbitrary_seek_denied_count
diagnostic_event_count
unsafe_acceptance_count
claim_boundary_flags
final_state
final_passed
```

The physical-player source says the player must decide whether it can execute an update safely, whether the next section is ready and verified, whether the A/B gate is ready, whether audio sync is acceptable, and whether to continue, pause, or fail closed. The player report should expose those decisions.

## 14. Player unsafe acceptance

Player unsafe acceptance includes:

```text
- unverified section displayed
- wrong section displayed
- hash mismatch accepted
- missing critical lane accepted
- unsupported arbitrary seek accepted
- unsupported package treated as playable
- gate not locked but display allowed
- fail-closed condition ignored
```

This is the most direct form of the physical-player safety invariant.

---

## 15. AMCFValidationResult

All corridors need a shared validation result object.

## 15.1 Purpose

`AMCFValidationResult` records a single check.

It should answer:

```text
What was checked?
Did it pass?
If not, how serious is it?
What should happen next?
```

## 15.2 Required fields

```text
validation_id
target_type
target_id
check_name
passed
status
severity
reason_code
reason_text
recommended_action
blocking
corridor
source_ref
metadata
```

## 15.3 Target types

```text
package
manifest
update_event
physical_section
print_section
reader_capture
recovered_section
player_section
player_command
player_profile
report
generated_output
```

## 15.4 Status values

Recommended shared statuses:

```text
passed
passed_with_warning
failed
missing
unreadable
invalid
requires_rescan
requires_reprint
requires_manual_review
fail_closed
not_checked
```

## 15.5 Severity values

```text
info
warning
recoverable_error
critical_error
fail_closed
```

The key is consistency.

A `critical_error` in the reader path should not be called `minor_fail` in the player path.

---

## 16. AMCFFailClosedDecision

## 16.1 Purpose

`AMCFFailClosedDecision` records a denied unsafe action.

It should be used when the software refuses to proceed.

Examples:

```text
Printer:
refuse export because required hash lane is missing.

Reader:
refuse recovery because hash mismatch is critical.

Player:
refuse transition because next section is unverified.
```

## 16.2 Required fields

```text
decision_id
corridor
target_type
target_id
action_requested
allowed
fail_closed
reason_code
reason_text
critical_lane
recovery_action
rescan_allowed
reprint_allowed
manual_review_required
display_blank_required
source_validation_ids
metadata
```

## 16.3 Shared reason codes

Recommended reason codes:

```text
missing_section
duplicate_section
wrong_section_index
manifest_mismatch
unsupported_schema
hash_mismatch
metadata_hash_mismatch
registration_failed
colour_reference_unusable
timing_lane_unreadable
metadata_lane_unreadable
hash_lane_unreadable
marker_missing
payload_bounds_invalid
layout_margin_invalid
prefetch_timeout
gate_not_locked
reverse_buffer_miss
arbitrary_seek_denied
audio_sync_exceeded
unsupported_player_profile
unknown_critical_state
```

Shared reason codes help later UI, logs, and reports.

---

## 17. AMCFAuditEvent

## 17.1 Purpose

`AMCFAuditEvent` is a structured log entry.

It records what happened during a run.

It is different from `AMCFValidationResult`.

A validation result says:

```text
This check passed or failed.
```

An audit event says:

```text
This event happened during the run.
```

## 17.2 Required fields

```text
audit_event_id
timestamp
corridor
event_type
severity
target_type
target_id
message
details
related_validation_ids
related_decision_ids
metadata
```

## 17.3 Example event types

```text
run_started
input_loaded
manifest_loaded
section_mapped
print_layout_created
reader_capture_loaded
lane_extracted
section_recovered
player_profile_loaded
command_received
command_denied
state_transition
fail_closed_triggered
report_written
run_completed
```

Audit events make debugging easier.

---

## 18. Claim-boundary flags

Every report should include claim-boundary flags.

Suggested object:

```text
AMCFClaimBoundaryFlags
```

Fields:

```text
physical_hardware_claimed
hardware_validation_claimed
physical_level_5_claimed
manufactured_player_claimed
real_sensors_required
real_motors_required
real_cartridges_required
real_scans_required
real_printer_required
real_reader_required
real_player_required
```

Current software defaults:

```text
false
```

The physical-player dossier keeps Level 5 as future and not achieved. Therefore software reports must not imply hardware completion.

---

## 19. Claim-boundary wording

Reports should use careful wording.

Allowed:

```text
simulated player runtime passed
print layout manifest generated
reader fixture recovery passed
package compatibility with simulated profile passed
fail-closed decision recorded
unsafe_acceptance_count remained zero
```

Not allowed:

```text
physical player proven
not hardware validated
cartridge validated
real sensor verified
manufactured player ready
printer output physically proven playable
reader hardware proven
```

This distinction must appear in public docs and reports.

---

## 20. Generated-output status

All corridors generate output.

The report should include:

```text
AMCFGeneratedOutputStatus
```

Fields:

```text
output_dir
generated_files
generated_file_count
committed_generated_output_found
ignored_output_dir_expected
unexpected_tracked_output_files
status
```

Status values:

```text
clean
warning
failed
not_checked
```

Generated output should normally remain uncommitted.

This applies to:

```text
output/amcf_pc_to_printer_layout/
output/amcf_reader_recovery_fixture/
output/amcf_player_pc_runtime_fixture/
output/amcf_software_io_repo_audit/
```

---

## 21. Local-path scan status

Public-facing docs and generated release reports should avoid leaking local Windows paths unless they are intentionally local instructions.

A scan status object should include:

```text
local_path_scan_status
local_path_leak_found
local_path_matches
allowed_local_path_contexts
status
```

This matters because your workflow uses local paths for commands, but public repo docs should not accidentally embed private working paths.

For Codex final reports, local path commands can be reported to you, but committed public docs should avoid unnecessary local path leakage.

---

## 22. Unsafe hardware claim scan

Public-facing docs should be scanned for unsafe claims.

Suggested scan targets:

```text
not hardware validated
physical proof
manufactured player
real player proven
Level 5 complete
real sensors validated
real motor control proven
cartridge hardware proven
```

Report fields:

```text
unsafe_hardware_claim_scan_status
unsafe_hardware_claim_found
unsafe_hardware_claim_matches
status
```

This should remain clean.

---

## 23. Lineage and traceability

Every corridor should preserve lineage.

Suggested object:

```text
AMCFLineageRecord
```

Fields:

```text
source_package_id
source_manifest_id
source_event_ids
source_section_ids
print_package_id
print_manifest_id
reader_capture_ids
recovered_section_ids
player_session_id
report_ids
```

This lets the software trace:

```text
AMCFUpdateEvent
→ AMCFPhysicalSection
→ AMCFPrintSection
→ AMCFReaderCapture
→ AMCFRecoveredSection
→ AMCFPlayerSection
→ AMCFReport
```

Traceability is one of the main reasons the shared model exists.

---

## 24. Error and warning vocabulary

A shared severity vocabulary should be used.

```text
info
warning
recoverable_error
critical_error
fail_closed
```

Meaning:

```text
info:
not a problem, informational.

warning:
non-blocking issue, report should mention it.

recoverable_error:
operation can recover through rescan/reprint/retry.

critical_error:
operation cannot safely continue unless fixed.

fail_closed:
software intentionally denied unsafe action.
```

Each corridor should use these meanings consistently.

---

## 25. Recommended actions vocabulary

Shared `recommended_action` values:

```text
continue
continue_with_warning
rescan
reprint
retry
pause
blank_display
fail_closed
manual_review
deny_command
stop_run
fix_manifest
fix_layout
unsupported
```

Examples:

```text
Printer margin violation:
fix_layout

Reader unreadable section:
rescan

Reader hash mismatch:
rescan or reprint

Player unverified next section:
fail_closed / blank_display

Player arbitrary seek:
deny_command
```

---

## 26. Final pass logic

Every report should compute `final_passed`.

General rule:

```text
final_passed = true only if all required critical checks passed, unsafe_acceptance_count is zero, and no blocking validation result remains unresolved.
```

A report may pass with warnings if warnings are non-blocking:

```text
final_passed = true
warnings_count > 0
```

But it must not pass with unresolved critical errors.

---

## 27. Corridor pass rules

## 27.1 Printer pass rule

Printer report passes only if:

```text
- manifest loaded
- print sections generated
- section/event map valid
- layout bounds valid
- required lanes present
- hash/checksum data present when required
- no critical margin/layout overlap
- unsafe_acceptance_count == 0
```

## 27.2 Reader pass rule

Reader report passes only if:

```text
- captures loaded
- expected sections processed
- validation results recorded
- no wrong/corrupt section accepted
- rescan/reprint/manual-review requests are explicit
- unsafe_acceptance_count == 0
```

A reader run may still report damaged sections and pass as a diagnostic run if the damage was correctly detected.

So distinguish:

```text
recovery_success
```

from:

```text
audit_success
```

## 27.3 Player pass rule

Player report passes only if:

```text
- package/profile compatibility checked
- required player sections built
- state machine completed expected run or failed closed correctly
- unsupported commands denied
- unverified sections not displayed
- unsafe_acceptance_count == 0
```

A player run can pass if it fails closed correctly.

That is important.

---

## 28. Passing fail-closed runs

Fail-closed does not always mean the software failed.

Example:

```text
Input intentionally contains hash mismatch.
Player refuses display.
Report records fail_closed.
unsafe_acceptance_count remains zero.
```

That test should pass.

So reports need two concepts:

```text
operation_completed_normally
safety_behaviour_correct
```

A safety test may have:

```text
operation_completed_normally = false
safety_behaviour_correct = true
final_passed = true
```

This avoids treating safe refusal as failure.

---

## 29. Human-readable summaries

Every JSON report should have a Markdown summary.

Examples:

```text
PRINT_LAYOUT_SUMMARY.md
READER_RECOVERY_SUMMARY.md
PLAYER_RUNTIME_SUMMARY.md
SOFTWARE_IO_REPO_AUDIT_SUMMARY.md
```

The summary should include:

```text
- run name
- inputs
- outputs
- pass/fail
- counts
- warnings
- fail-closed decisions
- unsafe_acceptance_count
- claim-boundary status
- next recommended action
```

Markdown summaries are for humans.

JSON reports are for tools.

---

## 30. Report compatibility for future UI

A future desktop UI or local web UI should consume these reports.

Therefore reports should be stable and predictable.

Do not make the UI parse random Markdown.

UI should read:

```text
JSON reports
```

and display:

```text
- validation results
- lane status
- recovered sections
- player timeline
- fail-closed decisions
- warnings/errors
```

This is why the report schema matters before UI work.

---

## 31. Output folder policy

Suggested output folders:

```text
output/amcf_software_io_repo_audit/
output/amcf_shared_model_validation/
output/amcf_pc_to_printer_layout/
output/amcf_reader_recovery_fixture/
output/amcf_player_pc_runtime_fixture/
output/amcf_cross_corridor_audit/
```

Each output folder should contain:

```text
*.json
*SUMMARY.md
optional preview/export files
```

Generated output should not be committed.

---

## 32. Fixture versus generated output

Keep fixtures separate from generated output.

```text
fixtures:
stable test inputs committed intentionally.

output:
generated run results not committed.
```

Possible fixture paths later:

```text
tests/fixtures/amcf_software_io/
tests/fixtures/amcf_print_layout/
tests/fixtures/amcf_reader_recovery/
tests/fixtures/amcf_player_runtime/
```

But Codex should respect repo conventions after audit.

---

## 33. Cross-corridor audit report

Eventually there should be a report that checks consistency across the corridors.

Suggested future run:

```text
AMCF_CROSS_CORRIDOR_AUDIT_V1
```

Purpose:

```text
Verify that printer, reader, and player reports use compatible schema, IDs, statuses, safety fields, and claim-boundary flags.
```

Suggested output:

```text
cross_corridor_audit_report.json
CROSS_CORRIDOR_AUDIT_SUMMARY.md
```

Checks:

```text
- report schemas share common fields
- validation statuses are known
- severity statuses are known
- reason codes are known
- unsafe_acceptance_count exists
- claim-boundary flags exist
- generated output policy checked
- local-path scan checked
- hardware-claim scan checked
```

---

## 34. Tests for the cross-corridor layer

Future tests should verify:

```text
- AMCFReport base fields exist
- AMCFValidationResult status vocabulary works
- AMCFFailClosedDecision reason codes work
- unsafe_acceptance_count defaults to 0
- reports fail when unsafe_acceptance_count > 0
- printer report has shared fields
- reader report has shared fields
- player report has shared fields
- claim-boundary flags default false
- generated output not committed
- local path scan detects forbidden public paths
- unsafe hardware claim scan catches banned phrases
```

Possible test file:

```text
tests/test_amcf_cross_corridor_reports.py
```

---

## 35. First implementation target for this layer

The first implementation should probably not build all printer/reader/player reports at once.

It should build the shared report/audit primitives.

Suggested future run name:

```text
AMCF_CROSS_CORRIDOR_REPORTING_BASELINE_V1
```

Purpose:

```text
Create shared report, validation, fail-closed, claim-boundary, generated-output, and audit-event helpers that printer, reader, and player corridors can reuse.
```

Possible modules:

```text
src/amcf_report_model.py
src/amcf_validation_model.py
src/amcf_audit_model.py
```

But only after repo audit confirms there are no existing equivalents.

---

## 36. Do not overbuild the report system

The first report layer should not become a huge framework.

It should be:

```text
simple
JSON-friendly
dataclass/dict friendly
standard-library
easy to test
```

Avoid:

```text
database logging
complex event bus
network logging
external observability stack
GUI-only reporting
```

The current AMCF project benefits from deterministic files and simple reports.

Keep that pattern.

---

## 37. Relationship to release tooling

The release tooling should eventually consume these reports.

For example:

```text
public release review
package refresh
closeout handoff
tag prep
```

can check:

```text
- all relevant reports final_passed
- unsafe_acceptance_count == 0
- no generated output committed
- no unsafe hardware claims
- no local path leaks
```

This would align new software corridors with the existing physical-player release-review approach.

---

## 38. What remains future

Do not start with:

```text
- central database
- web dashboard
- external telemetry
- cloud logging
- complex schema registry
- UI-first report viewer
```

First establish:

```text
shared JSON reports
shared validation statuses
shared fail-closed decisions
shared claim-boundary flags
shared generated-output policy
```

---

## 39. What Part 9 decides

Part 9 decides:

```text
- reports, validation results, audit events, fail-closed decisions, and claim-boundary flags must be shared across all corridors
- unsafe_acceptance_count is a cross-corridor invariant, not only a player-simulator field
- PC → Printer, PC ↔ Reader, and Player ↔ PC should each have corridor-specific reports built on a common AMCFReport base
- fail-closed can be a successful safety result if unsafe acceptance stays zero
- generated output should remain separate from committed fixtures
- local-path and unsafe-hardware-claim scans should be part of public-facing report/release hygiene
- JSON reports are for machines; Markdown summaries are for humans
- future UI should consume JSON reports, not become the source of truth
- the first implementation should build simple shared report primitives, not a complex logging framework
```

---

## 40. What Part 10 should continue with

Part 10 should continue into:

```text
Test fixtures, regression strategy, generated-output policy, and Codex implementation safety rules
```

That should cover:

```text
- fixture design
- deterministic sample packages
- printer fixture packages
- reader capture fixtures
- player runtime fixtures
- cross-corridor roundtrip fixtures
- unittest strategy
- generated output exclusion
- ignored test-file handling
- force-add rules
- validation command pattern
- how Codex should prove changes before commit
```

----
# AMCF Software Development and I/O Control Dossier  
## Part 10 — Test Fixtures, Regression Strategy, Generated-Output Policy, and Codex Implementation Safety Rules

## 1. Purpose of Part 10

Part 9 defined the shared report, audit, validation, fail-closed, and claim-boundary model.

Part 10 now defines how the software work should be tested and controlled so that Codex can safely implement the system in stages.

This part answers:

```text
What fixtures should exist?
What should be generated output?
What should be committed?
How should printer, reader, and player software be tested?
How should cross-corridor tests work?
How should Codex avoid breaking existing physical-player tests?
How should Codex prove each change before commit?
How should ignored files and force-add be handled?
```

This matters because the software system will eventually touch:

```text
PC → Printer
PC ↔ Reader
Player ↔ PC
shared AMCF package/manifest/update-event model
reports
fixtures
generated outputs
release checks
```

Without a strict fixture and regression strategy, the repo can easily become messy.

---

## 2. Core testing principle

The testing principle should be:

```text
Every AMCF software corridor must be testable without real hardware first.
```

That means:

```text
PC → Printer:
test with fixture manifests and generated layout records, not a physical printer.

PC ↔ Reader:
test with simulated captures and print-manifest-assisted fixtures, not a real scanner first.

Player ↔ PC:
test with simulated player profiles and command sessions, not real player hardware first.
```

This preserves the existing claim boundary. The physical-player source keeps Level 5 future physical hardware as not achieved yet. So tests should prove software behaviour, not physical hardware.

---

## 3. Fixture versus generated output

The repo needs a hard distinction between:

```text
fixtures
```

and:

```text
generated output
```

## 3.1 Fixtures

Fixtures are committed test inputs.

They should be:

```text
- small
- deterministic
- hand-reviewable
- stable
- intentionally versioned
- used by tests
```

Examples:

```text
fixture_manifest_basic.json
fixture_update_events_basic.json
fixture_physical_sections_basic.json
fixture_print_manifest_basic.json
fixture_reader_captures_basic.json
fixture_player_profile_basic.json
fixture_player_commands_basic.json
```

## 3.2 Generated output

Generated output is produced by demo or test runs.

It should normally live under:

```text
output/
```

and should not be committed.

Examples:

```text
output/amcf_pc_to_printer_layout/print_audit_report.json
output/amcf_reader_recovery_fixture/reader_recovery_report.json
output/amcf_player_pc_runtime_fixture/player_runtime_report.json
output/amcf_cross_corridor_audit/cross_corridor_audit_report.json
```

Generated output can be inspected, but it should not become the source of truth.

---

## 4. Why deterministic fixtures are necessary

AMCF software will use update events, physical sections, print layouts, reader captures, player runtime sessions, and reports.

If those are not deterministic, tests become unreliable.

The physical-player plan depends on precise schedule concepts such as physical section update events, view-gate dwell duration, preload deadline, transition blank duration, and optical presentation timing. So fixture data should be fixed and predictable.

A basic fixture should always produce the same:

```text
section IDs
event IDs
timestamps
hash values
lane statuses
report counts
unsafe_acceptance_count
final_passed value
```

---

## 5. Fixture hierarchy

A clean fixture hierarchy could be:

```text
tests/fixtures/amcf_software_io/
  shared/
    fixture_package_basic.json
    fixture_manifest_basic.json
    fixture_update_events_basic.json
    fixture_physical_sections_basic.json

  printer/
    fixture_print_profile_sheet_grid.json
    fixture_print_manifest_expected.json

  reader/
    fixture_reader_capture_valid.json
    fixture_reader_capture_hash_mismatch.json
    fixture_reader_capture_wrong_section.json
    fixture_reader_capture_missing_lane.json

  player/
    fixture_player_profile_sim_folded_ab.json
    fixture_player_commands_basic.json
    fixture_player_commands_reverse_seek.json
    fixture_player_commands_invalid_seek.json

  cross_corridor/
    fixture_roundtrip_basic.json
```

The exact path should follow repo conventions after audit, but the separation should exist.

---

## 6. Minimal shared fixture package

The first shared fixture should be deliberately small.

Example:

```text
package_id: fixture_package_basic
manifest_id: fixture_manifest_basic
source_duration_ms: 3000
events:
  event_0001 at 0 ms → section_0001
  event_0002 at 1000 ms → section_0002
  event_0003 at 2000 ms → section_0003
sections:
  section_0001
  section_0002
  section_0003
```

The event shape should preserve the physical-player timing concepts:

```json id="zcjrqv"
{
  "event_id": "event_0002",
  "event_index": 2,
  "timestamp_ms": 1000,
  "visible_section_id": "section_0002",
  "previous_section_id": "section_0001",
  "next_section_id": "section_0003",
  "dwell_ms": 1000,
  "preload_required_by_ms": 950,
  "transition_blank_ms": 8,
  "requires_verified_next_section": true
}
```

This mirrors the physical-player source’s own example event fields. ---

## 7. Shared fixture requirements

Every shared fixture should include:

```text
- package_id
- manifest_id
- schema_version
- source_duration_ms
- update events
- physical sections
- deterministic hashes
- expected lane status
- claim-boundary defaults
```

Every physical section fixture should include:

```text
section_id
section_index
event_id
timestamp_start_ms
dwell_ms
payload_ref
section_hash
timing_index_lane
registration_lane
colour_reference_lane
metadata_transform_lane
hash_checksum_lane
damage_status
```

The lane categories come from the physical-player source’s reader/prefetch lane requirements: section index, timing marks, registration marks, colour reference, metadata/transform lane, hash/checksum lane, and damage/missing marker status. ---

# PC → Printer Fixtures

## 8. Printer fixture purpose

Printer fixtures should test:

```text
AMCF manifest / physical sections
→ print profile
→ print layout manifest
→ print audit report
```

They should not require a real printer.

## 9. Printer fixture types

Printer fixtures should include:

```text
valid sheet-grid fixture
invalid duplicate-section fixture
invalid margin-overflow fixture
missing hash-lane fixture
missing registration-lane fixture
event-section mismatch fixture
```

## 10. Printer expected outputs

Tests should verify:

```text
- print manifest created
- section count matches physical sections
- event-to-section map is valid
- section IDs are unique
- lane bounds exist
- payload bounds exist
- required lanes are present
- margins are valid
- report final_passed is true for valid fixture
- report final_passed is false for critical invalid fixture
- unsafe_acceptance_count remains 0
- claim-boundary flags remain false
```

A failed printer fixture can still be a successful test if the software correctly rejects it.

---

# PC ↔ Reader Fixtures

## 11. Reader fixture purpose

Reader fixtures should test:

```text
print manifest / expected sections
+ simulated reader captures
→ recovered sections
→ rescan/reprint decisions
→ reader recovery report
```

They should not require scanner hardware or image-processing dependencies at first.

## 12. Reader fixture types

Reader fixtures should include:

```text
valid capture
hash mismatch capture
wrong section capture
missing timing/index lane capture
missing registration lane capture
metadata corrupt capture
damaged payload capture
duplicate section capture
manifest mismatch capture
```

## 13. Reader expected outputs

Tests should verify:

```text
- valid capture recovers
- hash mismatch does not recover silently
- wrong section is flagged
- missing critical lane triggers rescan or failure
- damaged payload creates reprint request
- duplicate section is reported
- manifest mismatch requires manual review
- rescan_requests.json is produced when needed
- reprint_requests.json is produced when needed
- unsafe_acceptance_count remains 0
- claim-boundary flags remain false
```

Reader software should not silently accept corrupted or wrong sections.

---

# Player ↔ PC Fixtures

## 14. Player fixture purpose

Player fixtures should test:

```text
AMCF manifest / player sections
+ simulated player profile
+ command script
→ state-machine execution
→ diagnostics
→ player runtime report
```

They should not require a real player.

## 15. Player fixture types

Player fixtures should include:

```text
valid playback fixture
unverified next section fixture
hash mismatch fixture
missing next section fixture
reverse-buffer success fixture
reverse-buffer miss fixture
local seek success fixture
arbitrary seek denied fixture
unsupported update-spacing fixture
unsupported schema fixture
```

## 16. Player expected outputs

Tests should verify:

```text
- package loads
- compatibility check runs
- player sections are built
- play command succeeds on valid fixture
- unverified section fails closed
- hash mismatch fails closed
- reverse succeeds only when buffer allows
- reverse denial is reported
- arbitrary seek is denied by default
- unsupported package is not treated as playable
- command transcript is produced
- diagnostics are produced
- unsafe_acceptance_count remains 0
- claim-boundary flags remain false
```

The physical-player source explicitly preserves `unsafe_acceptance_count` as zero. That must become a standard fixture assertion.

---

# Cross-Corridor Fixtures

## 17. Why cross-corridor fixtures matter

The three corridors must eventually work together.

A cross-corridor fixture should test:

```text
shared manifest
→ print layout
→ simulated reader recovery
→ player runtime compatibility
```

This proves that the corridors are not inventing incompatible formats.

## 18. Minimal cross-corridor roundtrip

A minimal roundtrip should be:

```text
fixture AMCF manifest
→ fixture physical sections
→ print layout manifest
→ simulated reader capture
→ recovered section report
→ player runtime session
```

Expected result:

```text
- same package_id preserved
- same manifest_id preserved
- same section IDs preserved
- same event IDs preserved
- same hash statuses preserved
- reports use shared validation/status vocabulary
- unsafe_acceptance_count remains 0 everywhere
```

## 19. Cross-corridor failure fixture

A failure fixture should show propagation.

Example:

```text
section_0002 hash mismatch in reader recovery
```

Expected effects:

```text
Reader:
section_0002 requires rescan/reprint.

Player:
section_0002 is not display-eligible.

Printer:
can produce reprint request for section_0002.
```

This is where the software system becomes coherent.

---

## 20. Golden outputs versus structural assertions

The repo should be careful with golden files.

A golden file is an expected output committed to the repo.

Golden files can be useful, but they can also become brittle.

Better first approach:

```text
structural assertions
```

Tests should assert:

```text
- required fields exist
- counts match
- IDs match
- statuses match
- unsafe_acceptance_count == 0
- final_passed is correct
```

Do not require exact full JSON text unless necessary.

Use golden files only for small stable fixtures.

---

## 21. Mutation fixtures

Mutation tests are important.

Mutation fixture means:

```text
take a valid fixture
change one thing
verify the software rejects or warns correctly
```

Examples:

```text
- duplicate section ID
- missing hash lane
- wrong next_section_id
- unreadable timing lane
- hash mismatch
- unsupported schema version
- unsupported arbitrary seek
- invalid margin
```

Mutation tests are excellent for preserving fail-closed behaviour.

---

## 22. Regression categories

The test suite should be organised by regression category:

```text
A. import tests
B. schema/fixture load tests
C. shared model tests
D. printer corridor tests
E. reader corridor tests
F. player corridor tests
G. cross-corridor tests
H. report/audit tests
I. generated-output policy tests
J. claim-boundary tests
```

Each new implementation phase should add at least one test in the relevant category.

---

## 23. Import tests

Every new module should have a basic import test.

Example:

```text
import src.amcf_report_model
import src.amcf_validation_model
import src.amcf_player_runtime_adapter
```

This catches syntax/import problems early.

---

## 24. Fixture load tests

Every fixture should load deterministically.

Tests should verify:

```text
- valid JSON
- required top-level fields
- schema version present
- deterministic IDs
- expected section count
- expected event count
```

No test should depend on wall-clock time except generated report timestamps, and even those should not be used for deterministic equality.

---

## 25. Shared model tests

Shared model tests should verify:

```text
- update events map to physical sections
- physical sections map to print/player/recovered views
- validation statuses are known
- reason codes are known
- claim-boundary defaults are false
- unsafe_acceptance_count defaults to 0
```

---

## 26. Printer corridor tests

Printer tests should verify:

```text
- layout manifest builds
- print sections map to physical sections
- lane bounds exist
- margin checks work
- duplicate section ID is rejected
- missing required lane is rejected
- report final_passed logic works
```

---

## 27. Reader corridor tests

Reader tests should verify:

```text
- simulated captures normalize
- expected section matching works
- lane statuses are interpreted
- hash mismatch triggers rescan/reprint/failure
- wrong section is not accepted
- duplicate section is reported
- reader report uses shared validation statuses
```

---

## 28. Player corridor tests

Player tests should verify:

```text
- package-to-player section adapter works
- player profile loads
- compatibility check runs
- command session records responses
- arbitrary seek denied by default
- reverse buffer limits enforced
- fail-closed decisions recorded
- unsafe sections not displayed
```

The physical-player plan’s normal and failure state-machine logic includes prefetch, verify, view gate lock, transition blank, visible switch, old section park, and fail-closed paths. Player tests should exercise that logic through package-derived runtime data.

---

## 29. Report and audit tests

Report tests should verify:

```text
- report has common fields
- final_passed computed correctly
- unsafe_acceptance_count present
- claim-boundary flags present
- fail-closed decisions included
- generated-output status included
- local-path scan status included where relevant
- unsafe-hardware-claim scan status included where relevant
```

---

## 30. Generated-output policy tests

Generated-output tests should verify:

```text
- output files go under output/
- output/ is not committed
- demo writes expected JSON/Markdown outputs
- report lists generated files
- no unexpected generated artifacts are tracked
```

This should be part of every major demo/release review.

---

## 31. Claim-boundary tests

Claim-boundary tests should check that reports do not claim:

```text
physical hardware not validated
physical Level 5 achieved
manufactured player exists
real sensors required
real motors required
real cartridges required
real scans required
```

For current software, those booleans should be false.

This protects the project’s public framing.

---

## 32. Test file naming

Likely future test files:

```text
tests/test_amcf_software_io_repo_audit.py
tests/test_amcf_shared_package_model.py
tests/test_amcf_cross_corridor_reports.py
tests/test_amcf_pc_to_printer_layout.py
tests/test_amcf_reader_recovery_fixture.py
tests/test_amcf_player_pc_runtime_fixture.py
tests/test_amcf_cross_corridor_roundtrip.py
tests/test_amcf_generated_output_policy.py
tests/test_amcf_claim_boundaries.py
```

But Codex should inspect existing naming conventions first.

---

## 33. Existing tests must remain passing

The existing physical-player tests remain the regression baseline.

The software work should not break:

```text
physical-player state machine
fail-closed safety
reverse/seek controls
mechanism profiles
integrated simulator demo
public docs/release review
package refresh
GitHub Pages final review
closeout handoff
tag prep
```

Any future Codex run should run the full suite:

```cmd id="cmeaf3"
python -m unittest discover -s tests
```

not only the new test file.

---

## 34. Validation command pattern

Each Codex implementation phase should run:

```cmd id="ou6tcs"
python -m unittest discover -s tests
```

Then relevant demos, for example:

```cmd id="x4prct"
python demo/run_amcf_software_io_repo_audit.py
python demo/run_amcf_pc_to_printer_layout_demo.py
python demo/run_amcf_reader_recovery_fixture_demo.py
python demo/run_amcf_player_pc_runtime_fixture_demo.py
```

And existing release/check demos when relevant:

```cmd id="y4vwe7"
python demo/run_physical_player_simulator_demo.py
python demo/run_public_release_tag_prep.py
```

Codex should only run demos that exist in the repo.

It should not invent success for missing scripts.

---

## 35. Codex final report requirements

Every Codex run should report:

```text
- run name
- base commit
- branch
- files changed
- tests run
- demos run
- generated output path
- generated output committed: yes/no
- unsafe_acceptance_count
- claim-boundary flags
- local-path leak found: yes/no
- unsafe hardware claim found: yes/no
- final pass/fail
- commit hash if committed
- push command if committed
```

Do not invent a commit hash.

Do not claim a commit if Codex did not commit.

---

## 36. Handling ignored tests and force-add

Your previous workflow showed that some test files may be ignored by `.gitignore`.

Codex should use this rule:

```text
If an intended new test file is ignored, force-add only that exact intended test file.
```

Allowed:

```cmd id="cj5adm"
git add -f tests/test_amcf_player_pc_runtime_fixture.py
```

Not allowed:

```cmd id="7d9pbp"
git add -f tests/
git add -f .
git add -f output/
```

This avoids accidentally committing generated output or junk files.

---

## 37. Git status discipline

Codex should always inspect:

```cmd id="5l1xal"
git status --short
git diff --stat
```

Before commit.

It should confirm:

```text
- only intended source/docs/tests changed
- output/ is not staged
- __pycache__ is not staged
- generated files are not staged
- local-only files are not staged
```

Then commit only intended files.

---

## 38. Commit discipline

For each implementation phase, commit message should be specific.

Examples:

```text
Add AMCF software IO repo audit
Add shared AMCF report model
Add PC to printer layout prototype
Add reader recovery fixture prototype
Add player PC runtime fixture
Add cross-corridor roundtrip fixtures
```

Do not make one huge vague commit.

Good commits should map to one implementation phase.

---

## 39. Branch discipline

The broad software work should happen on:

```text
dev/amcf-software-io-control
```

Or phase branches under it.

Possible phase branches:

```text
phase/software-io-repo-audit
phase/shared-report-model
phase/pc-printer-layout
phase/reader-recovery-fixture
phase/player-pc-runtime
phase/cross-corridor-roundtrip
```

But do not overcomplicate if the repo workflow is simpler.

---

## 40. No hardware dependency in tests yet

Tests should not require:

```text
- real printer
- real scanner
- real reader
- real physical player
- real USB device
- real serial port
- camera
- internet
```

Everything should run offline.

This is essential for Codex and repeatable development.

---

## 41. Time and nondeterminism policy

Avoid nondeterministic tests.

Do not depend on:

```text
current time
random IDs
filesystem ordering
internet availability
hardware availability
system printer configuration
camera/scanner availability
```

If timestamps are generated in reports, tests should not require exact timestamp equality.

If IDs are generated, use deterministic fixture IDs.

---

## 42. Hash determinism policy

Hashes should be deterministic.

Fixture hashes should be:

```text
- stable
- reproducible
- documented
- based on fixture payload or fixed strings
```

For early fixtures, synthetic hashes are acceptable if clearly marked as fixture hashes.

Do not pretend synthetic fixture hashes are physical scan validation.

---

## 43. Roundtrip regression strategy

Eventually, a complete software roundtrip test should do:

```text
fixture AMCF manifest
→ build physical sections
→ build print layout
→ simulate reader capture
→ recover sections
→ build player sections
→ run player session
→ produce cross-corridor report
```

Expected:

```text
same package_id
same manifest_id
same event IDs
same section IDs
hashes match
no unsafe acceptance
claim-boundary false
final_passed true
```

This should become the central regression test after the corridor prototypes exist.

---

## 44. Negative roundtrip regression

A negative roundtrip should introduce one fault.

Example:

```text
hash mismatch in section_0002
```

Expected:

```text
Printer:
original layout remains valid.

Reader:
section_0002 requires rescan/reprint.

Player:
section_0002 display denied.

Cross-corridor report:
fault propagated correctly.
unsafe_acceptance_count remains 0.
```

This is more valuable than only testing happy paths.

---

## 45. Release/review integration

After major software phases, release review should check:

```text
- tests pass
- demos run
- reports generated
- generated output not committed
- claim-boundary flags false
- unsafe_acceptance_count zero
- public docs do not overclaim
```

But not every small development commit needs a public release refresh.

Release refresh should happen at planned milestones.

---

## 46. First implementation target for fixtures/regression

A future implementation run could be:

```text
AMCF_SOFTWARE_IO_FIXTURE_REGRESSION_BASELINE_V1
```

Purpose:

```text
Create the first shared fixture structure and tests that future PC → Printer, PC ↔ Reader, and Player ↔ PC implementations can reuse.
```

But it should probably come after:

```text
repo audit
shared model baseline
shared report baseline
```

because fixtures should match discovered repo conventions.

---

## 47. What should remain future

Do not start with:

```text
- hardware-in-the-loop tests
- printer driver tests
- scanner API tests
- camera calibration tests
- real-time player protocol tests
- GUI tests
- complex image-processing tests
```

Those come later.

First establish deterministic fixtures and no-hardware regression tests.

---

## 48. What Part 10 decides

Part 10 decides:

```text
- fixtures and generated output must be strictly separated
- all three corridors must be testable without hardware first
- deterministic fixtures are required for package, manifest, events, physical sections, print layout, reader captures, player profiles, and command scripts
- unsafe_acceptance_count must be asserted across printer, reader, player, and cross-corridor tests
- claim-boundary booleans must remain false in current software
- mutation/negative tests are essential
- cross-corridor roundtrip tests should become the central regression target
- tests should use structural assertions before broad golden-output files
- generated output should stay under output/ and not be committed
- ignored tests should be force-added only by exact file path
- Codex must run tests, inspect git status/diff, and report honestly before commit
```

---

## 49. What Part 11 should continue with

Part 11 should continue into:

```text
Implementation order, branch strategy, Codex progression cycle, and phase sequencing
```

That should cover:

```text
- what Codex should implement first
- why repo audit comes before new modules
- whether shared report/model helpers come before corridor prototypes
- phase order for PC → Printer, PC ↔ Reader, Player ↔ PC
- branch naming
- commit naming
- when to refresh public docs/release tooling
- how the final single Codex prompt should reference the completed dossier collection
```

-----
# AMCF Software Development and I/O Control Dossier  
## Part 11 — Implementation Order, Branch Strategy, Codex Progression Cycle, and Phase Sequencing

## 1. Purpose of Part 11

Part 11 defines how the software dossier should become actual repo work.

The earlier parts defined:

```text
Part 1 — software scope reset
Part 2 — current baseline and existing repo surface
Part 3 — repo audit and discovery method
Part 4 — shared package/manifest/update-event/section model
Part 5 — software stack research method
Part 6 — PC → Printer corridor
Part 7 — PC ↔ Reader corridor
Part 8 — Player ↔ PC corridor
Part 9 — cross-corridor reports/safety/audits
Part 10 — fixtures, regression, generated-output policy
```

Part 11 now answers:

```text
What should Codex implement first?
What should wait?
What branch should be used?
How should phases be ordered?
How do we stop Codex jumping too far?
How do we turn the final dossier collection into one reusable Codex baseline?
```

The order matters because the physical-player dossier already keeps a strict boundary between digital AMCF, physical carrier, reader/recovery, simulator, and future Level 5 hardware; Level 5 is explicitly not achieved yet. So implementation must progress from **repo audit → shared software model → corridor prototypes → cross-corridor roundtrip**, not straight to hardware.

---

## 2. Core implementation rule

The core implementation rule should be:

```text
Do not implement corridor-specific systems before the repo has been audited and the shared AMCF model/reporting baseline is understood.
```

That means Codex should not begin with:

```text
PDF printer output
scanner/image processing
USB device protocol
desktop GUI
real player control
```

It should begin with:

```text
repo audit
shared model discovery
shared report/safety primitives
deterministic fixtures
```

Only after those exist should the three corridors be implemented.

---

## 3. Why repo audit must be first

The repo may already contain package, manifest, export, reader, printer, report, or physical-player structures.

So the first implementation phase must answer:

```text
What already exists?
What should be reused?
What should be adapted?
What is missing?
What would duplicate existing work?
```

This follows Part 3.

The risk is that Codex creates:

```text
new manifest model
new package model
new report model
new section model
```

when the repo already has partial equivalents.

That would fragment AMCF software.

So the first actual Codex phase should be:

```text
AMCF_SOFTWARE_IO_REPO_AUDIT_V1
```

not:

```text
AMCF_PLAYER_PC_RUNTIME_INTEGRATION_V1
```

Runtime integration matters, but it comes later.

---

## 4. Current checkpoint and tag point

The current public software/control checkpoint is:

```text
e7e13155db3441887c5982cb0dfa9bd91383390a
```

Suggested tag:

```text
amcf-physical-player-software-control-v1
```

That tag should mean:

```text
Clean public checkpoint for the physical-player software/control foundation.
```

It should not mean:

```text
not hardware validated
physical player manufactured
physical Level 5 not complete
real sensors/motors/cartridge proven
```

The physical-player source keeps the future physical hardware level separate and unachieved, so the tag wording must remain software/control only. ---

## 5. Recommended branch structure

After the tag, create a broad development branch:

```text
dev/amcf-software-io-control
```

Reason:

```text
The new work is broader than physical-player runtime integration.
It covers PC → Printer, PC ↔ Reader, Player ↔ PC, shared package/manifest model, reports, fixtures, and cross-corridor tests.
```

A narrower branch like:

```text
dev/physical-player-runtime-integration
```

is too narrow for the software dossier.

Possible later phase branches:

```text
phase/software-io-repo-audit
phase/shared-model-baseline
phase/cross-corridor-reporting
phase/fixture-regression-baseline
phase/pc-printer-layout
phase/reader-recovery-fixture
phase/player-pc-runtime-fixture
phase/cross-corridor-roundtrip
```

But if the repo workflow is simpler, one branch is acceptable:

```text
dev/amcf-software-io-control
```

with one clean commit per phase.

---

## 6. Safe tag command

Use a clean-tree checked command, not a blind tag command.

```cmd
cd /d "<repo-root>" && powershell -NoProfile -ExecutionPolicy Bypass -Command "$ErrorActionPreference='Stop'; if((git status --short)){ throw 'Working tree is not clean; do not tag yet.' }; git fetch --tags; if(git tag --list 'amcf-physical-player-software-control-v1'){ throw 'Tag already exists locally.' }; git tag -a amcf-physical-player-software-control-v1 -m 'AMCF physical-player software-control public release v1'; git push origin amcf-physical-player-software-control-v1"
```

Then branch:

```cmd
cd /d "<repo-root>" && git checkout -b dev/amcf-software-io-control
```

---

# Implementation Phase Order

## 7. Phase 0 — Tag and branch setup

Run name:

```text
AMCF_SOFTWARE_IO_BRANCH_BASELINE_V1
```

Purpose:

```text
Confirm current clean baseline, optional tag status, and create development branch.
```

Should do:

```text
- confirm HEAD
- confirm clean tree
- confirm tag exists or report missing
- create/check branch dev/amcf-software-io-control
```

Should not do:

```text
- create software modules
- change docs
- change tests
- implement corridors
```

This is setup only.

---

## 8. Phase 1 — Repo audit

Run name:

```text
AMCF_SOFTWARE_IO_REPO_AUDIT_V1
```

Purpose:

```text
Discover existing package, manifest, update-event, printer, reader, player, report, fixture, and release structures before creating new ones.
```

Expected outputs:

```text
docs/AMCF_SOFTWARE_IO_REPO_AUDIT.md
demo/run_amcf_software_io_repo_audit.py
tests/test_amcf_software_io_repo_audit.py
```

Generated output:

```text
output/amcf_software_io_repo_audit/
```

Report files:

```text
software_io_repo_audit_report.json
corridor_file_map.json
schema_discovery_report.json
SOFTWARE_IO_REPO_AUDIT_SUMMARY.md
```

This phase should classify files into:

```text
shared core
PC → Printer
PC ↔ Reader
Player ↔ PC
physical-player simulator
reports/audits
fixtures/tests
docs/release tooling
generated output
uncertain/duplicate schemas
```

This phase should not implement the new shared model yet.

It discovers.

---

## 9. Phase 2 — Shared AMCF model baseline

Run name:

```text
AMCF_SHARED_PACKAGE_MANIFEST_MODEL_BASELINE_V1
```

Purpose:

```text
Define or adapt the shared AMCF package, manifest, update-event, physical-section, validation, and report model based on the repo audit.
```

Possible files:

```text
src/amcf_package_model.py
src/amcf_manifest_model.py
src/amcf_section_model.py
docs/AMCF_SHARED_PACKAGE_MANIFEST_MODEL.md
tests/test_amcf_shared_package_model.py
```

But only create those if the repo audit shows no better existing location.

Objects to define/adapt:

```text
AMCFPackage
AMCFManifest
AMCFPlaybackSchedule
AMCFUpdateEvent
AMCFPhysicalSection
AMCFValidationResult
AMCFFailClosedDecision
AMCFReport
```

The update-event model should preserve physical-player timing fields such as timestamp, visible section, next section, dwell time, preload deadline, transition blank duration, and verified-next-section requirement. This phase should not implement printer, reader, or player corridors fully.

It creates the shared foundation.

---

## 10. Phase 3 — Cross-corridor report and safety baseline

Run name:

```text
AMCF_CROSS_CORRIDOR_REPORTING_BASELINE_V1
```

Purpose:

```text
Create shared report, validation, fail-closed, audit-event, claim-boundary, generated-output, and unsafe-acceptance primitives.
```

Possible files:

```text
src/amcf_report_model.py
src/amcf_validation_model.py
src/amcf_audit_model.py
docs/AMCF_CROSS_CORRIDOR_REPORTING_MODEL.md
tests/test_amcf_cross_corridor_reports.py
```

Core invariants:

```text
unsafe_acceptance_count exists
unsafe_acceptance_count defaults to 0
claim-boundary booleans default false
fail-closed decisions can be successful safety outcomes
generated output is not committed
```

The physical-player plan explicitly preserves `unsafe_acceptance_count` as zero, so this must become shared infrastructure, not only a player-simulator detail. ---

## 11. Phase 4 — Fixture and regression baseline

Run name:

```text
AMCF_SOFTWARE_IO_FIXTURE_REGRESSION_BASELINE_V1
```

Purpose:

```text
Create deterministic shared fixtures and regression tests that later corridor prototypes can reuse.
```

Possible fixture tree:

```text
tests/fixtures/amcf_software_io/
  shared/
  printer/
  reader/
  player/
  cross_corridor/
```

Core fixture package:

```text
fixture_package_basic
fixture_manifest_basic
event_0001 → section_0001
event_0002 → section_0002
event_0003 → section_0003
```

Tests should verify:

```text
fixtures load
schema versions exist
IDs are stable
event/section mapping works
claim-boundary defaults false
unsafe_acceptance_count defaults 0
```

No printer/reader/player full prototype yet.

This phase prepares the test bed.

---

## 12. Phase 5 — PC → Printer layout prototype

Run name:

```text
AMCF_PC_TO_PRINTER_LAYOUT_PROTOTYPE_V1
```

Purpose:

```text
Implement the first no-hardware PC → Printer corridor prototype.
```

Scope:

```text
shared fixture manifest
→ physical sections
→ print layout manifest
→ optional SVG preview
→ print audit report
```

Possible files:

```text
src/amcf_print_layout.py
src/amcf_print_reports.py
demo/run_amcf_pc_to_printer_layout_demo.py
tests/test_amcf_pc_to_printer_layout.py
docs/AMCF_PC_TO_PRINTER_SOFTWARE_PATH.md
```

Generated output:

```text
output/amcf_pc_to_printer_layout/
```

This phase should use update-event/section-driven printing, not fixed-frame printing. The physical-player source states that AMCF physical transport follows update events and does not chase constant FPS movement. No real printer.

No PDF dependency unless already justified.

Start with JSON layout manifest and maybe SVG.

---

## 13. Phase 6 — PC ↔ Reader fixture recovery prototype

Run name:

```text
AMCF_PC_READER_RECOVERY_FIXTURE_V1
```

Purpose:

```text
Implement the first no-hardware reader/recovery corridor prototype.
```

Scope:

```text
print manifest fixture
+ simulated reader capture
→ recovered section records
→ rescan/reprint decisions
→ reader recovery report
```

Possible files:

```text
src/amcf_reader_capture.py
src/amcf_reader_recovery.py
src/amcf_reader_reports.py
demo/run_amcf_reader_recovery_fixture_demo.py
tests/test_amcf_reader_recovery_fixture.py
docs/AMCF_PC_READER_SOFTWARE_PATH.md
```

Generated output:

```text
output/amcf_reader_recovery_fixture/
```

No scanner.

No image-processing dependency.

No OCR dependency.

The physical-player plan identifies lane concepts such as section index, timing marks, registration marks, colour reference, metadata/transform lane, hash/checksum lane, and damage/missing marker status; the reader fixture should preserve these fields even before image processing exists. ---

## 14. Phase 7 — Player ↔ PC runtime/control fixture prototype

Run name:

```text
AMCF_PLAYER_PC_RUNTIME_CONTROL_FIXTURE_V1
```

Purpose:

```text
Wrap the existing physical-player simulator in a PC/player package-control session using fixture package data.
```

Scope:

```text
fixture manifest
→ player sections
→ simulated player profile
→ command session
→ state machine execution
→ diagnostics/report
```

Possible files:

```text
src/amcf_player_profile.py
src/amcf_player_runtime_adapter.py
src/amcf_player_session.py
src/amcf_player_commands.py
src/amcf_player_reports.py
demo/run_amcf_player_pc_runtime_fixture_demo.py
tests/test_amcf_player_pc_runtime_fixture.py
docs/AMCF_PLAYER_PC_SOFTWARE_PATH.md
```

Generated output:

```text
output/amcf_player_pc_runtime_fixture/
```

No hardware protocol.

No USB.

No firmware.

The player should answer the safety questions identified in the physical-player plan: whether an update can be executed safely, whether the next section is ready and verified, whether A/B gate state is ready, whether audio sync is acceptable, and whether to continue, pause, or fail closed. ---

## 15. Phase 8 — Cross-corridor roundtrip prototype

Run name:

```text
AMCF_CROSS_CORRIDOR_ROUNDTRIP_V1
```

Purpose:

```text
Prove that the shared fixture can move through printer, reader, and player software without incompatible schemas.
```

Scope:

```text
shared fixture manifest
→ print layout
→ simulated reader capture/recovery
→ player runtime compatibility/session
→ cross-corridor audit report
```

Possible files:

```text
src/amcf_cross_corridor_roundtrip.py
demo/run_amcf_cross_corridor_roundtrip_demo.py
tests/test_amcf_cross_corridor_roundtrip.py
docs/AMCF_CROSS_CORRIDOR_ROUNDTRIP.md
```

Generated output:

```text
output/amcf_cross_corridor_roundtrip/
```

Assertions:

```text
same package_id preserved
same manifest_id preserved
same event IDs preserved
same section IDs preserved
hash statuses preserved
unsafe_acceptance_count remains 0
claim-boundary flags remain false
```

This is the first major point where the software system becomes coherent.

---

## 16. Phase 9 — Negative cross-corridor mutation tests

Run name:

```text
AMCF_CROSS_CORRIDOR_MUTATION_SAFETY_V1
```

Purpose:

```text
Prove that faults propagate safely and are not silently accepted.
```

Fault examples:

```text
hash mismatch
wrong section ID
missing timing lane
missing hash lane
duplicate section
unsupported arbitrary seek
invalid print margin
reader manifest mismatch
```

Expected behaviour:

```text
printer rejects invalid layout
reader requests rescan/reprint
player denies display/fails closed
unsafe_acceptance_count remains 0
```

This phase is important because happy-path tests are not enough.

---

## 17. Phase 10 — Software stack dependency research phase

Run name:

```text
AMCF_SOFTWARE_STACK_RESEARCH_REFRESH_V1
```

Purpose:

```text
Research current software libraries only after the no-dependency prototypes define what is actually needed.
```

This is where web/current research may be needed.

Categories:

```text
PDF generation
SVG/PDF conversion
image processing
barcode/QR/fiducial marker decoding
scanner/camera acquisition on Windows
desktop UI
local web UI
USB/HID/serial libraries
```

This phase should not happen first.

It should happen after the project knows what problem needs a dependency.

---

## 18. Phase 11 — Public docs and release review refresh

Run name:

```text
AMCF_SOFTWARE_IO_PUBLIC_DOCS_REFRESH_V1
```

Purpose:

```text
Update docs and public/release review after meaningful software functionality exists.
```

Should update or create:

```text
docs/AMCF_SOFTWARE_IO_CONTROL_DOCS_MAP.md
docs/AMCF_SOFTWARE_IO_CONTROL_ROADMAP.md
docs/AMCF_PC_TO_PRINTER_SOFTWARE_PATH.md
docs/AMCF_PC_READER_SOFTWARE_PATH.md
docs/AMCF_PLAYER_PC_SOFTWARE_PATH.md
docs/AMCF_CROSS_CORRIDOR_ROUNDTRIP.md
```

Should also update:

```text
README.md
docs map
development sequence
release review docs
```

But only after implementation exists.

Do not bloat README during planning.

---

## 19. Phase 12 — Software I/O release checkpoint

Run name:

```text
AMCF_SOFTWARE_IO_CONTROL_RELEASE_CANDIDATE_V1
```

Purpose:

```text
Prepare a clean software I/O release checkpoint after repo audit, shared model/reporting, fixtures, three corridor prototypes, and cross-corridor roundtrip exist.
```

Possible future tag:

```text
amcf-software-io-control-v1
```

Only after:

```text
tests pass
demos pass
generated output not committed
unsafe_acceptance_count zero
claim-boundary flags false
docs updated
release review clean
```

This is a later milestone, not now.

---

# Codex Progression Cycle

## 20. How each Codex phase should work

Each Codex phase should follow the same structure:

```text
1. Read the dossier collection.
2. Read the repo audit / relevant docs.
3. Confirm current branch and HEAD.
4. Implement only the named phase.
5. Do not skip ahead.
6. Add tests.
7. Run full unittest suite.
8. Run relevant demo scripts.
9. Check generated output policy.
10. Check claim-boundary / unsafe hardware wording.
11. Commit only intended files.
12. Report honestly.
```

This prevents Codex from turning one phase into ten phases.

---

## 21. Final single Codex prompt should reference the collection

After all dossier parts are complete, we should create one collection file, likely:

```text
docs/AMCF_SOFTWARE_DEVELOPMENT_AND_IO_CONTROL_DOSSIER_COLLECTION.md
```

The final Codex prompt should not repeat all the dossier content.

It should say:

```text
Read docs/AMCF_SOFTWARE_DEVELOPMENT_AND_IO_CONTROL_DOSSIER_COLLECTION.md first.
Treat it as the controlling software-development plan.
Implement only Phase 1: AMCF_SOFTWARE_IO_REPO_AUDIT_V1.
Do not skip ahead.
```

Then future prompts can say:

```text
Read the same collection.
Implement Phase 2 only.
```

This is exactly why we are building the dossier in parts first.

---

## 22. Codex prompt template structure

Every phase prompt should include:

```text
RUN_NAME
BASE_COMMIT
BRANCH
DOSSIER_COLLECTION_PATH
PHASE_OBJECTIVE
FILES_TO_INSPECT
FILES_TO_CREATE_OR_MODIFY
DO_NOT_DO
IMPLEMENTATION_STEPS
TESTS_TO_ADD
VALIDATION_COMMANDS
COMMIT_RULES
FINAL_REPORT_FIELDS
```

This template should be created after the dossier collection is complete.

---

## 23. Codex “do not skip ahead” rule

Every Codex prompt should say:

```text
Implement only this phase.
Do not implement later phases.
Do not add dependencies unless this phase explicitly requires them.
Do not add hardware APIs.
Do not add GUI.
Do not update public release docs unless this phase asks for it.
Do not create a tag unless explicitly asked.
Do not push unless explicitly asked.
```

This is essential.

---

## 24. Codex validation commands

Standard validation block:

```cmd
python -m unittest discover -s tests
```

Then phase-specific demos, only if they exist:

```cmd
python demo/run_amcf_software_io_repo_audit.py
python demo/run_amcf_pc_to_printer_layout_demo.py
python demo/run_amcf_reader_recovery_fixture_demo.py
python demo/run_amcf_player_pc_runtime_fixture_demo.py
python demo/run_amcf_cross_corridor_roundtrip_demo.py
```

And when relevant:

```cmd
python demo/run_physical_player_simulator_demo.py
python demo/run_public_release_tag_prep.py
```

Codex must not claim it ran missing scripts.

---

## 25. Commit rules

Each phase should commit only intended files.

Before commit:

```cmd
git status --short
git diff --stat
```

Do not commit:

```text
output/
__pycache__/
generated ZIPs
local-only files
broad ignored folders
```

If a new test file is ignored:

```cmd
git add -f tests/test_exact_file.py
```

Never:

```cmd
git add -f tests/
git add -f .
git add -f output/
```

---

## 26. Commit naming

Suggested commit messages:

```text
Add AMCF software IO repo audit
Add shared AMCF package manifest model
Add cross-corridor reporting baseline
Add AMCF software IO fixture regression baseline
Add PC to printer layout prototype
Add reader recovery fixture prototype
Add player PC runtime fixture prototype
Add cross-corridor roundtrip prototype
Add cross-corridor mutation safety tests
Refresh AMCF software IO public docs
```

Each commit should match one phase.

---

## 27. Push policy

Codex should normally commit but not push, unless the user explicitly asks.

Final report should provide:

```cmd
git push
```

or:

```cmd
git push origin dev/amcf-software-io-control
```

only after a successful commit.

Do not invent remote state.

---

## 28. When to update public docs

Do not update public docs after every internal phase.

Update public docs after milestone phases:

```text
after repo audit if it creates a new docs map
after shared model/reporting baseline if public explanation is needed
after first corridor prototype
after cross-corridor roundtrip
before release checkpoint
```

README should stay concise.

Detailed docs belong under `docs/`.

---

## 29. When to run release review

Release review should run after meaningful public-facing changes.

Examples:

```text
after cross-corridor roundtrip
after public docs refresh
before software I/O release checkpoint
```

Not necessarily after every fixture-only commit.

---

## 30. What should not happen in the first software implementation

Do not begin with:

```text
real printer driver integration
real scanner API
camera capture
USB/HID/serial player protocol
desktop GUI
local web UI
image-processing dependency
PDF dependency
barcode dependency
hardware-in-the-loop tests
```

Those are later, after file-based models work.

---

## 31. First actual Codex run after dossier completion

The first real Codex run after the final dossier collection should be:

```text
AMCF_SOFTWARE_IO_REPO_AUDIT_V1
```

Its instruction should be:

```text
Read the dossier collection.
Audit the repo.
Map existing files by corridor.
Map existing schemas.
Do not implement new corridor modules yet.
Create audit docs/report/tests.
Run tests.
Commit.
Do not push.
```

That should be the first final Codex prompt.

---

## 32. What Part 11 decides

Part 11 decides:

```text
- implementation should start with repo audit, not runtime integration
- shared model/reporting/fixtures should come before corridor prototypes
- PC → Printer should come before reader recovery because reader recovery can use print manifests
- Player ↔ PC runtime should reuse the existing simulator after shared model/reporting exists
- cross-corridor roundtrip should come after the three corridor prototypes
- dependency research should happen after no-dependency prototypes reveal actual needs
- public docs/release refresh should happen at milestones, not after every small phase
- broad branch dev/amcf-software-io-control fits this work
- Codex prompts should implement one phase only and reference the final dossier collection
```

---

## 33. What Part 12 should continue with

Part 12 should continue into:

```text
Final dossier collection structure and file layout
```

That should define:

```text
- what the final collection file should be called
- where it should be saved
- how parts should be combined
- what headings it should preserve
- whether to include the physical-player source summary
- how to include implementation phases
- what the final single Codex prompt should reference
- how future phase prompts should reference the same collection
```

----
# AMCF Software Development and I/O Control Dossier  
## Part 12 — Final Dossier Collection Structure, File Layout, Source Anchors, and Handoff Format

## 1. Purpose of Part 12

Part 12 defines how the separate dossier parts should become one final reference document.

The final document should be the controlling software-development baseline that Codex reads before implementation.

It should not be a loose chat transcript.

It should become a structured repo document.

Working title:

```text
AMCF Software Development and I/O Control Dossier Collection
```

Recommended repo path:

```text
docs/AMCF_SOFTWARE_DEVELOPMENT_AND_IO_CONTROL_DOSSIER_COLLECTION.md
```

Purpose:

```text
Collect the full software-development plan for PC → Printer, PC ↔ Reader, Player ↔ PC, shared AMCF package/manifest/update-event models, reporting, fixtures, implementation sequencing, and Codex phase control.
```

This collection is the document future Codex prompts should reference.

---

## 2. What the collection is

The collection should be:

```text
one consolidated Markdown dossier
```

containing:

```text
- the software scope reset
- current repo baseline
- repo audit strategy
- shared package/manifest/update-event model
- software stack method
- PC → Printer path
- PC ↔ Reader path
- Player ↔ PC path
- cross-corridor reports/safety/audits
- fixture/regression strategy
- implementation phase order
- Codex handoff rules
```

It should become the controlling reference for the next development cycle.

---

## 3. What the collection is not

The collection is not:

```text
- a replacement for the physical-player design dossier
- a claim that physical hardware exists
- a direct hardware implementation plan
- a printer/scanner/USB driver specification
- a GUI design document
- a final API specification
```

It is a software-development control document.

It should stay honest about the boundary between:

```text
software simulation / package models / reports
```

and:

```text
real manufactured hardware
```

The attached physical-player source keeps Level 5 future physical hardware separate and unachieved, so this collection must preserve that boundary. ---

## 4. Why it should be one collection file

One collection file is needed because Codex should not have to infer the plan from scattered chat responses.

The final Codex prompt should be able to say:

```text
Read docs/AMCF_SOFTWARE_DEVELOPMENT_AND_IO_CONTROL_DOSSIER_COLLECTION.md first.
Treat it as the controlling plan.
Implement Phase 1 only.
```

That only works if the collection is complete, coherent, and structured.

---

## 5. Recommended final file path

Recommended:

```text
docs/AMCF_SOFTWARE_DEVELOPMENT_AND_IO_CONTROL_DOSSIER_COLLECTION.md
```

Optional companion docs later:

```text
docs/AMCF_SOFTWARE_IO_CONTROL_ROADMAP.md
docs/AMCF_SOFTWARE_IO_REPO_AUDIT.md
docs/AMCF_SHARED_PACKAGE_MANIFEST_MODEL.md
docs/AMCF_CROSS_CORRIDOR_REPORTING_MODEL.md
docs/AMCF_PC_TO_PRINTER_SOFTWARE_PATH.md
docs/AMCF_PC_READER_SOFTWARE_PATH.md
docs/AMCF_PLAYER_PC_SOFTWARE_PATH.md
docs/AMCF_CROSS_CORRIDOR_ROUNDTRIP.md
```

But the first collection should be one file.

Do not split it too early.

---

## 6. Recommended collection title block

The top of the collection should be:

```markdown
# AMCF Software Development and I/O Control Dossier Collection

## Scope

This dossier collection defines the software-development plan for AMCF I/O control:

- PC → Printer
- PC ↔ Reader
- Player ↔ PC
- shared AMCF package / manifest / update-event / physical-section model
- cross-corridor reporting, validation, fail-closed, audit, and fixture strategy
- staged Codex implementation phases

This document is a software planning and implementation-control document. It does not claim real hardware validation, manufactured player completion, or physical Level 5 completion.
```

This title block should appear before any part content.

---

## 7. Required metadata block

The collection should include a metadata block near the top.

Suggested:

```markdown
## Collection Metadata

- Collection name: AMCF Software Development and I/O Control Dossier Collection
- Intended repo path: docs/AMCF_SOFTWARE_DEVELOPMENT_AND_IO_CONTROL_DOSSIER_COLLECTION.md
- Baseline checkpoint: e7e13155db3441887c5982cb0dfa9bd91383390a
- Suggested baseline tag: amcf-physical-player-software-control-v1
- Recommended development branch: dev/amcf-software-io-control
- First implementation phase: AMCF_SOFTWARE_IO_REPO_AUDIT_V1
- Hardware validation claimed: false
- Physical Level 5 claimed: false
- Manufactured player claimed: false

## Source Anchors from Physical-Player Dossier

This collection is derived from the AMCF software dossier source record `software plan.txt` and from the prior AMCF physical-player design/control sequence. In repo form, ChatGPT-only citation placeholders from the source record are converted into this normal source-note wording.

The source anchors preserved here are:

- PC -> Printer, PC <-> Reader, and Player <-> PC are treated as software I/O corridors.
- The physical player is modelled as a future executor of digital AMCF schedule/update-event data through a physical carrier and optical viewing window.
- The shared AMCF package, manifest, update-event, physical-section, report, fixture, and safety models are central to all corridors.
- Physical hardware validation, manufactured player completion, and physical Level 5 completion are not claimed.

## Claim Boundary

This dossier describes software planning, software architecture, simulated control, package models, reports, fixtures, and implementation sequencing.

Current claim-boundary values:

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false

This dossier does not claim real hardware validation, manufactured player completion, physical Level 5 completion, real printer/scanner/player integration, or hardware proof.

## Corridor Summary

### PC -> Printer

Prepare digital AMCF package data for future printable/exported physical carrier packages using shared schedule, manifest, section, lane, registration, colour, metadata, hash, and report models.

### PC <-> Reader

Recover or verify physical AMCF carrier data back into digital AMCF through no-hardware-first fixtures, captures, lane recognition, hash/checksum validation, diagnostics, and audit reports.

### Player <-> PC

Support future physical/optical player alignment through package compatibility checks, capability profiles, runtime simulation, fail-closed decisions, bounded reverse/seek control, diagnostics, and future protocol boundaries.

## Implementation Phase Index

0. `AMCF_SOFTWARE_IO_BRANCH_BASELINE_V1`
1. `AMCF_SOFTWARE_IO_REPO_AUDIT_V1`
2. Shared AMCF package / manifest / update-event / physical-section model foundation
3. Cross-corridor report, claim-boundary, and safety model foundation
4. PC -> Printer software path planning and no-hardware fixture path
5. PC <-> Reader software path planning and no-hardware fixture path
6. Player <-> PC software path alignment and simulator-control bridge
7. Cross-corridor fixture and regression strategy
8. Public docs / release / package refresh for software I/O work

## First Implementation Phase

The first Codex implementation phase after this collection is:

`AMCF_SOFTWARE_IO_REPO_AUDIT_V1`

That phase should audit the existing repo and classify current source, docs, demos, tests, reports, schemas, and generated-output conventions by corridor. It should not implement printer, reader, player runtime, package-model, or report-model modules yet.

## Implementation Control Rules

1. Implement one phase at a time.
2. Run repo audit before creating new models.
3. Do not introduce hardware APIs before no-hardware fixtures pass.
4. Do not introduce GUI before CLI/report flows pass.
5. Do not introduce dependencies unless the current phase justifies them.
6. Keep generated output under `output/`.
7. Do not commit generated output.
8. Keep `unsafe_acceptance_count` at 0.
9. Keep hardware claim flags false.
10. Run `python -m unittest discover -s tests` before commit.
11. Commit only intended files.
12. Do not push unless explicitly instructed.

## Do Not Do Yet

Do not implement yet:

- real printer driver integration
- real scanner API
- camera capture
- USB/HID/serial player protocol
- firmware protocol
- GUI application
- local web UI
- image-processing dependency
- PDF dependency
- barcode/QR dependency
- hardware-in-the-loop tests
- physical-player hardware validation claims
- `AMCF_SOFTWARE_IO_REPO_AUDIT_V1` implementation in this collection-file task

---
```

This keeps the handoff clear.

---

## 8. Required source-anchor section

The collection should include a source-anchor section that explains what it inherits from the earlier physical-player dossier.

Suggested heading:

```markdown
## Source Anchors from Physical-Player Dossier
```

This section should say:

```text
The software dossier builds on the existing AMCF physical-player planning, but it is not the same document.
```

The attached source already distinguishes the earlier Physical I/O scope — **PC → Printer**, **Reader → PC**, and **Player ↔ PC software recognition/control** — from the physical-player object dossier. That is the source basis for the three software corridors.

The same source also defines the physical player as an executor of the digital AMCF chain:

```text
Digital AMCF
→ AMCF schedule / update events
→ physical AMCF carrier
→ physical player transport
→ physical/optical viewing window
```

That chain is what the software plan supports. ---

## 9. Source-anchor rules

The source-anchor section should preserve these rules:

```text
- The software dossier does not replace the physical-player design dossier.
- The software dossier uses the physical-player dossier as design input.
- Physical hardware remains future unless separately validated.
- Update events, section timing, prefetch, verification, and fail-closed logic must be preserved.
- PC → Printer, PC ↔ Reader, and Player ↔ PC are the controlling software corridors.
```

This prevents Codex from treating the software dossier as a hardware-completion claim.

---

## 10. Recommended table of contents

The collection should include a table of contents.

Suggested:

```markdown
## Table of Contents

1. Scope and Source Anchors
2. Part 1 — Scope Reset, Software Boundary, I/O Corridors, and Development Philosophy
3. Part 2 — Current Software Baseline, Existing Repo Surface, and Discovery Boundaries
4. Part 3 — Repo Audit, Discovery Strategy, Corridor Classification, and Schema-Control Method
5. Part 4 — Shared AMCF Package, Manifest, Update-Event, and Section Model Requirements
6. Part 5 — Software Stack Research Method, Selection Criteria, Dependency Policy, and Tooling Boundaries
7. Part 6 — PC → Printer Software Path
8. Part 7 — PC ↔ Reader Software Path
9. Part 8 — Player ↔ PC Software Path
10. Part 9 — Cross-Corridor Reports, Logs, Safety, Validation, and Audit Model
11. Part 10 — Test Fixtures, Regression Strategy, Generated-Output Policy, and Codex Implementation Safety Rules
12. Part 11 — Implementation Order, Branch Strategy, Codex Progression Cycle, and Phase Sequencing
13. Part 12 — Final Dossier Collection Structure, File Layout, Source Anchors, and Handoff Format
14. Implementation Phase Index
15. Codex Handoff Rules
16. First Codex Prompt Template
```

This should remain readable and direct.

---

## 11. How to preserve part structure

Each part should be inserted under its own heading.

Use this pattern:

```markdown
---

# Part 1 — Scope Reset, Software Boundary, I/O Corridors, and Development Philosophy

[Part 1 content]

---

# Part 2 — Current Software Baseline, Existing Repo Surface, and Discovery Boundaries

[Part 2 content]
```

Do not merge all parts into one giant undifferentiated essay.

The part boundaries matter because they show how the logic developed.

---

## 12. What to remove during collection

When converting the chat parts into the collection, remove conversational filler such as:

```text
Part 6 stops here because...
What Part 7 should continue with...
```

But do not remove the actual decisions.

For example, this can be removed:

```text
```

But this should stay:

```text
Part 6 decides:
- PC → Printer is a full software corridor
- printer software should generate structured AMCF physical carrier layouts
- printing should be update-event/section-driven
```

The final collection should read like a document, not a chat continuation.

---

## 13. What to keep during collection

Keep:

```text
- definitions
- decisions
- corridor models
- object names
- phase names
- implementation rules
- tests
- generated-output policies
- claim-boundary rules
- Codex safety rules
- exact run names
- branch/tag recommendations
```

Do not compress away the detailed logic.

The user specifically wanted the parts to be based on how much information exists, not forced into a short outline.

So the final collection should preserve depth.

---

## 14. Required collection sections before Part 1

Before Part 1, add:

```markdown
# AMCF Software Development and I/O Control Dossier Collection

## Scope

## Collection Metadata

## Source Anchors from Physical-Player Dossier

## Claim Boundary

## Corridor Summary

## Implementation Phase Index
```

Then include the parts.

This gives Codex the high-level control points before the long dossier content.

---

## 15. Claim-boundary section

The claim-boundary section should say:

```markdown
## Claim Boundary

This dossier describes software architecture, simulated control, package models, reports, fixtures, and implementation sequencing.

It does not claim:

- real physical-player hardware validation
- manufactured-player completion
- physical Level 5 completion
- real printer output validation
- real reader/scanner validation
- real USB/firmware/player communication
- real motor/sensor/cartridge validation

All early implementations must keep these flags false:

- physical_hardware_claimed
- hardware_validation_claimed
- physical_level_5_claimed
- manufactured_player_claimed
```

This should be near the top, not buried at the end.

---

## 16. Corridor summary section

Add a short corridor summary near the top.

Suggested:

```markdown
## Corridor Summary

### PC → Printer

Converts AMCF package / manifest / update-event / physical-section data into printable carrier layouts, print manifests, previews, reprint indexes, and print audit reports.

### PC ↔ Reader

Accepts physical-carrier captures or simulated reader captures, detects/reconstructs section and lane data, validates against manifests, produces recovered-section records, and creates rescan/reprint requests.

### Player ↔ PC

Uses AMCF package and player-profile data to simulate package compatibility, command sessions, state-machine execution, fail-closed decisions, diagnostics, and future protocol boundaries.
```

This gives Codex immediate orientation.

---

## 17. Implementation phase index

The collection should include a phase index before the full part text.

Suggested:

```markdown
## Implementation Phase Index

0. AMCF_SOFTWARE_IO_BRANCH_BASELINE_V1
1. AMCF_SOFTWARE_IO_REPO_AUDIT_V1
2. AMCF_SHARED_PACKAGE_MANIFEST_MODEL_BASELINE_V1
3. AMCF_CROSS_CORRIDOR_REPORTING_BASELINE_V1
4. AMCF_SOFTWARE_IO_FIXTURE_REGRESSION_BASELINE_V1
5. AMCF_PC_TO_PRINTER_LAYOUT_PROTOTYPE_V1
6. AMCF_PC_READER_RECOVERY_FIXTURE_V1
7. AMCF_PLAYER_PC_RUNTIME_CONTROL_FIXTURE_V1
8. AMCF_CROSS_CORRIDOR_ROUNDTRIP_V1
9. AMCF_CROSS_CORRIDOR_MUTATION_SAFETY_V1
10. AMCF_SOFTWARE_STACK_RESEARCH_REFRESH_V1
11. AMCF_SOFTWARE_IO_PUBLIC_DOCS_REFRESH_V1
12. AMCF_SOFTWARE_IO_CONTROL_RELEASE_CANDIDATE_V1
```

This lets Codex see the intended order before reading all details.

---

## 18. First implementation phase must be clearly marked

The collection should mark this strongly:

```markdown
## First Implementation Phase

The first Codex implementation phase after this collection is:

AMCF_SOFTWARE_IO_REPO_AUDIT_V1

Purpose:

Audit the repo and map existing AMCF package, manifest, update-event, printer, reader, player, report, fixture, and release structures before implementing new software modules.

Do not implement printer, reader, player runtime, GUI, scanner APIs, printer drivers, image processing, USB, or hardware protocols in this phase.
```

This prevents Codex from jumping ahead.

---

## 19. Handoff file layout

The final handoff could consist of:

```text
docs/AMCF_SOFTWARE_DEVELOPMENT_AND_IO_CONTROL_DOSSIER_COLLECTION.md
docs/AMCF_SOFTWARE_IO_CONTROL_ROADMAP.md
```

But initially, only one file is necessary.

Recommended first file only:

```text
docs/AMCF_SOFTWARE_DEVELOPMENT_AND_IO_CONTROL_DOSSIER_COLLECTION.md
```

Later, Codex Phase 1 may create:

```text
docs/AMCF_SOFTWARE_IO_REPO_AUDIT.md
```

Phase 2 may create:

```text
docs/AMCF_SHARED_PACKAGE_MANIFEST_MODEL.md
```

Do not create every future doc at once.

---

## 20. How to include local repo path

The local repo path can be used in the user-facing command prompt, but it should not be embedded as a public committed doc requirement unless necessary.

Local working path:

```text
<repo-root>
```

Use it in the final Codex/user command context.

But the collection file should avoid overusing local machine paths.

Public docs should be portable.

---

## 21. How to include baseline tag information

Include the baseline tag in metadata:

```text
Suggested baseline tag: amcf-physical-player-software-control-v1
```

But phrase it carefully:

```text
software/control checkpoint
```

not:

```text
hardware release
```

The tag marks a stable software/control baseline before broad software I/O development.

---

## 22. How to include citations/source notes

The final collection can include a short source-note section instead of file citations if it is going into the repo.

Example:

```markdown
## Source Notes

This software dossier is derived from the prior AMCF Physical Player Design and Structure Dossier and the current public repo development sequence. It preserves the prior design boundaries:

- PC → Printer, Reader → PC, and Player ↔ PC software recognition/control are treated as software I/O corridors.
- The physical player is modelled as an executor of digital AMCF schedule/update-event data through a physical carrier and optical viewing window.
- Physical hardware validation and Level 5 completion are not claimed.
```

Inside ChatGPT, we cite the uploaded source.

Inside repo docs, Codex can include source-note wording rather than ChatGPT file-citation syntax, unless you want the citation markers preserved as notes.

---

## 23. Should the collection include exact citations?

For a repo Markdown file, I would not include ChatGPT-only file citation markers like:

```text

```

Those are useful in this chat, but they will not be meaningful in GitHub Markdown.

Instead, the repo file should include source notes such as:

```text
Based on the earlier AMCF Physical Player Design and Structure Dossier section defining Physical I/O as PC → Printer, Reader → PC, and Player ↔ PC software recognition/control.
```

If the physical-player plan file itself is added to the repo, then internal repo links can be used later.

---

## 24. Collection should include an “Implementation Control Rules” section

Add this near the end:

```markdown
## Implementation Control Rules

1. Implement one phase at a time.
2. Run repo audit before creating new models.
3. Do not introduce hardware APIs before no-hardware fixtures pass.
4. Do not introduce GUI before CLI/report flows pass.
5. Do not introduce dependencies unless the current phase justifies them.
6. Keep generated output under output/.
7. Do not commit generated output.
8. Keep unsafe_acceptance_count at 0.
9. Keep hardware claim flags false.
10. Run python -m unittest discover -s tests before commit.
11. Commit only intended files.
12. Do not push unless explicitly instructed.
```

This gives Codex a checklist.

---

## 25. Collection should include “Do Not Do Yet”

Add a clear “do not do yet” section.

```markdown
## Do Not Do Yet

Do not implement yet:

- real printer driver integration
- real scanner API
- camera capture
- USB/HID/serial player protocol
- firmware protocol
- GUI application
- local web UI
- image-processing dependency
- PDF dependency
- barcode/QR dependency
- hardware-in-the-loop tests
- physical-player hardware validation claims
```

This is important because Codex tends to over-implement if a prompt is broad.

---

## 26. Collection should include “Current First Prompt Target”

Near the bottom:

```markdown
## Current First Prompt Target

The first implementation prompt after this collection should target:

AMCF_SOFTWARE_IO_REPO_AUDIT_V1

The prompt should instruct Codex to:

- read this collection first
- audit the existing repo
- classify existing files by corridor
- discover existing schemas and report conventions
- create audit docs/report/tests
- run the full unittest suite
- commit only intended files
- not implement later phases
```

This makes the next action unambiguous.

---

## 27. Final collection skeleton

The collection file should roughly look like this:

```markdown
# AMCF Software Development and I/O Control Dossier Collection

## Scope

## Collection Metadata

## Source Anchors from Physical-Player Dossier

## Claim Boundary

## Corridor Summary

## Implementation Phase Index

## First Implementation Phase

## Implementation Control Rules

## Do Not Do Yet

---

# Part 1 — Scope Reset, Software Boundary, I/O Corridors, and Development Philosophy

[content]

---

# Part 2 — Current Software Baseline, Existing Repo Surface, and Discovery Boundaries

[content]

---

# Part 3 — Repo Audit, Discovery Strategy, Corridor Classification, and Schema-Control Method

[content]

---

# Part 4 — Shared AMCF Package, Manifest, Update-Event, and Section Model Requirements

[content]

---

# Part 5 — Software Stack Research Method, Selection Criteria, Dependency Policy, and Tooling Boundaries

[content]

---

# Part 6 — PC → Printer Software Path: Digital AMCF to Printable Physical Carrier

[content]

---

# Part 7 — PC ↔ Reader Software Path: Physical Carrier Capture, Lane Recovery, Validation, and Rebuild Workflow

[content]

---

# Part 8 — Player ↔ PC Software Path: Package Control, Runtime Simulation, Capability Profiles, Diagnostics, and Future Protocol Boundary

[content]

---

# Part 9 — Cross-Corridor Reports, Logs, Safety, Validation, and Audit Model

[content]

---

# Part 10 — Test Fixtures, Regression Strategy, Generated-Output Policy, and Codex Implementation Safety Rules

[content]

---

# Part 11 — Implementation Order, Branch Strategy, Codex Progression Cycle, and Phase Sequencing

[content]

---

# Part 12 — Final Dossier Collection Structure, File Layout, Source Anchors, and Handoff Format

[content]

---

# Codex Handoff Template

[template]

---

# First Codex Phase Prompt

[prompt for AMCF_SOFTWARE_IO_REPO_AUDIT_V1]
```

The first Codex phase prompt can be in the same file or separate.

My recommendation:

```text
Keep the template in the collection file.
Put the actual first Codex prompt in the chat when ready.
```

That avoids committing a prompt that may need last-minute local path or branch edits.

---

## 28. Should Part 13 be the final Codex prompt?

Yes.

After Part 12, the next useful part should be:

```text
Part 13 — Final Single Codex Prompt for AMCF_SOFTWARE_IO_REPO_AUDIT_V1
```

That prompt should not implement all phases.

It should instruct Codex to:

```text
- create the dossier collection file from the provided parts
- or read it if already created
- implement Phase 1 only: repo audit
- create audit docs/report/tests
- run tests
- commit
- do not push
```

But before that, we may need one more step depending on your workflow:

```text
A. create the final collection text first
B. then write the Codex prompt that references it
```

If Codex is going to create the collection file itself, the prompt needs to include all collection content or tell Codex where to find it. Since Codex cannot read this chat unless pasted, the safest path is:

```text
1. I provide the complete collection text.
2. You save it or give it to Codex.
3. Then I provide the first implementation Codex prompt referencing the collection.
```

---

## 29. Recommended immediate next sequence

Recommended next sequence:

```text
Part 13:
Final collection file text / collection-building instruction.

Part 14:
Single Codex prompt for creating the collection file and/or starting AMCF_SOFTWARE_IO_REPO_AUDIT_V1.

Part 15 if needed:
A shorter phase-only Codex prompt after the collection is already committed.
```

But if you want fewer steps, Part 13 can be:

```text
Single Codex prompt that creates the collection file and implements Phase 1.
```

I do not recommend combining those two unless necessary.

Creating the collection and implementing the audit are two separate tasks.

Better:

```text
Codex Task 1:
Create dossier collection file.

Codex Task 2:
Implement Phase 1 repo audit.
```

This keeps changes reviewable.

---

## 30. What Part 12 decides

Part 12 decides:

```text
- the final collection should be one Markdown file under docs/
- recommended path is docs/AMCF_SOFTWARE_DEVELOPMENT_AND_IO_CONTROL_DOSSIER_COLLECTION.md
- the collection should include scope, metadata, source anchors, claim boundary, corridor summary, phase index, and implementation control rules before the part content
- ChatGPT file citations should not be copied literally into repo docs unless deliberately converted into source notes
- local Windows paths should be kept out of public docs except where necessary for user-facing commands
- the first implementation phase remains AMCF_SOFTWARE_IO_REPO_AUDIT_V1
- Codex should not skip ahead to printer, reader, player runtime, dependencies, GUI, or hardware
- creating the collection file and implementing the repo audit should preferably be separate Codex tasks
```

---

## 31. What Part 13 should continue with

Part 13 should provide:

```text
the first complete Codex handoff prompt
```

There are two possible versions:

```text
Version A:
Codex creates only the dossier collection file.

Version B:
Codex reads an already-created dossier collection and implements AMCF_SOFTWARE_IO_REPO_AUDIT_V1.
```

The safer order is Version A first, then Version B.

----
The source record `software plan.txt` identifies the collection as the AMCF Software Development and I/O Control Dossier Collection, covering **PC → Printer**, **PC ↔ Reader**, **Player ↔ PC**, the shared package/manifest/update-event model, cross-corridor reporting, and staged Codex implementation phases. It also records the intended repo path, baseline commit, suggested tag, branch, first implementation phase, and false hardware/Level 5/manufactured-player claims. # AMCF Software Development and I/O Control Dossier  
## Part 13 — First Complete Codex Handoff Prompt: Create the Dossier Collection File Only

## 1. Purpose of Part 13

Part 13 provides the first complete Codex handoff prompt.

Because the dossier record is now attached, the safest first Codex task is not yet to implement the repo audit.

The safest first Codex task is:

```text
Create the committed dossier collection file from the provided software plan record.
```

The attached plan itself says Part 13 should provide “the first complete Codex handoff prompt,” and it distinguishes two versions: Version A creates only the dossier collection file, while Version B reads an already-created collection and implements `AMCF_SOFTWARE_IO_REPO_AUDIT_V1`. It says the safer order is Version A first, then Version B. So Part 13 should be **Version A**.

That means:

```text
Codex Task 1:
Create docs/AMCF_SOFTWARE_DEVELOPMENT_AND_IO_CONTROL_DOSSIER_COLLECTION.md
from software plan.txt.

Do not implement the repo audit yet.
```

The repo audit comes after the collection exists.

---

## 2. Why this should be a separate Codex task

Creating the collection file and implementing the audit should not be merged.

Reason:

```text
Creating the dossier file is documentation/handoff preservation.

Repo audit is implementation Phase 1.
```

If Codex does both at once, it may:

```text
- over-edit the dossier
- skip collection cleanup
- start implementing modules too early
- mix documentation commit with audit code
- make the first commit too broad
```

The attached plan explicitly says creating the collection file and implementing the repo audit should preferably be separate Codex tasks. ---

## 3. What Codex should create

Codex should create:

```text
docs/AMCF_SOFTWARE_DEVELOPMENT_AND_IO_CONTROL_DOSSIER_COLLECTION.md
```

using the attached/source file:

```text
software plan.txt
```

The attached record already names the intended repo path as:

```text
docs/AMCF_SOFTWARE_DEVELOPMENT_AND_IO_CONTROL_DOSSIER_COLLECTION.md
```

and identifies the first implementation phase as:

```text
AMCF_SOFTWARE_IO_REPO_AUDIT_V1
```
---

## 4. What Codex should not do in this task

Codex should not implement anything beyond the dossier collection file.

Do not implement:

```text
- repo audit script
- printer path
- reader path
- player runtime path
- shared package model
- report model
- fixtures
- tests for future modules
- GUI
- PDF generation
- image processing
- scanner API
- printer driver integration
- USB/HID/serial protocol
- hardware validation
```

The attached plan’s “Do Not Do Yet” section specifically lists real printer driver integration, real scanner API, camera capture, USB/HID/serial player protocol, firmware protocol, GUI application, local web UI, image-processing dependency, PDF dependency, barcode/QR dependency, hardware-in-the-loop tests, and physical-player hardware validation claims as not-yet tasks. ---

## 5. Copyable Codex prompt

```text
RUN_NAME: AMCF_SOFTWARE_IO_DOSSIER_COLLECTION_FILE_V1

You are working in the AMCF public repo.

Goal:
Create the dossier collection file only.

Source record:
Use the provided dossier source record named:

software plan.txt

Create this repo file:

docs/AMCF_SOFTWARE_DEVELOPMENT_AND_IO_CONTROL_DOSSIER_COLLECTION.md

This task is Version A from the dossier plan:
Create only the dossier collection file.
Do not implement AMCF_SOFTWARE_IO_REPO_AUDIT_V1 yet.

Repository baseline context:
- Baseline checkpoint: e7e13155db3441887c5982cb0dfa9bd91383390a
- Suggested baseline tag: amcf-physical-player-software-control-v1
- Recommended development branch: dev/amcf-software-io-control
- First implementation phase after this collection: AMCF_SOFTWARE_IO_REPO_AUDIT_V1
- Hardware validation claimed: false
- Physical Level 5 claimed: false
- Manufactured player claimed: false

## Source Anchors from Physical-Player Dossier

This collection is derived from the AMCF software dossier source record `software plan.txt` and from the prior AMCF physical-player design/control sequence. In repo form, ChatGPT-only citation placeholders from the source record are converted into this normal source-note wording.

The source anchors preserved here are:

- PC -> Printer, PC <-> Reader, and Player <-> PC are treated as software I/O corridors.
- The physical player is modelled as a future executor of digital AMCF schedule/update-event data through a physical carrier and optical viewing window.
- The shared AMCF package, manifest, update-event, physical-section, report, fixture, and safety models are central to all corridors.
- Physical hardware validation, manufactured player completion, and physical Level 5 completion are not claimed.

## Claim Boundary

This dossier describes software planning, software architecture, simulated control, package models, reports, fixtures, and implementation sequencing.

Current claim-boundary values:

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false

This dossier does not claim real hardware validation, manufactured player completion, physical Level 5 completion, real printer/scanner/player integration, or hardware proof.

## Corridor Summary

### PC -> Printer

Prepare digital AMCF package data for future printable/exported physical carrier packages using shared schedule, manifest, section, lane, registration, colour, metadata, hash, and report models.

### PC <-> Reader

Recover or verify physical AMCF carrier data back into digital AMCF through no-hardware-first fixtures, captures, lane recognition, hash/checksum validation, diagnostics, and audit reports.

### Player <-> PC

Support future physical/optical player alignment through package compatibility checks, capability profiles, runtime simulation, fail-closed decisions, bounded reverse/seek control, diagnostics, and future protocol boundaries.

## Implementation Phase Index

0. `AMCF_SOFTWARE_IO_BRANCH_BASELINE_V1`
1. `AMCF_SOFTWARE_IO_REPO_AUDIT_V1`
2. Shared AMCF package / manifest / update-event / physical-section model foundation
3. Cross-corridor report, claim-boundary, and safety model foundation
4. PC -> Printer software path planning and no-hardware fixture path
5. PC <-> Reader software path planning and no-hardware fixture path
6. Player <-> PC software path alignment and simulator-control bridge
7. Cross-corridor fixture and regression strategy
8. Public docs / release / package refresh for software I/O work

## First Implementation Phase

The first Codex implementation phase after this collection is:

`AMCF_SOFTWARE_IO_REPO_AUDIT_V1`

That phase should audit the existing repo and classify current source, docs, demos, tests, reports, schemas, and generated-output conventions by corridor. It should not implement printer, reader, player runtime, package-model, or report-model modules yet.

## Implementation Control Rules

1. Implement one phase at a time.
2. Run repo audit before creating new models.
3. Do not introduce hardware APIs before no-hardware fixtures pass.
4. Do not introduce GUI before CLI/report flows pass.
5. Do not introduce dependencies unless the current phase justifies them.
6. Keep generated output under `output/`.
7. Do not commit generated output.
8. Keep `unsafe_acceptance_count` at 0.
9. Keep hardware claim flags false.
10. Run `python -m unittest discover -s tests` before commit.
11. Commit only intended files.
12. Do not push unless explicitly instructed.

## Do Not Do Yet

Do not implement yet:

- real printer driver integration
- real scanner API
- camera capture
- USB/HID/serial player protocol
- firmware protocol
- GUI application
- local web UI
- image-processing dependency
- PDF dependency
- barcode/QR dependency
- hardware-in-the-loop tests
- physical-player hardware validation claims
- `AMCF_SOFTWARE_IO_REPO_AUDIT_V1` implementation in this collection-file task

---

Required work:

1. Confirm repository status:
   - print current branch
   - print current HEAD
   - print git status --short

2. Create or update:
   docs/AMCF_SOFTWARE_DEVELOPMENT_AND_IO_CONTROL_DOSSIER_COLLECTION.md

3. Use software plan.txt as the source text.

4. Preserve the dossier’s structure and content:
   - Scope
   - Collection Metadata
   - Source Anchors from Physical-Player Dossier
   - Claim Boundary
   - Corridor Summary
   - Implementation Phase Index
   - First Implementation Phase
   - Implementation Control Rules
   - Do Not Do Yet
   - Part 1 through Part 12
   - Codex handoff / first phase prompt placeholders if present

5. Clean only obvious chat/file-transfer artifacts.
   Do not rewrite the technical meaning.

Allowed cleanup:
   - remove duplicated chat phrases that only say “Part X stops here…”
   - normalize headings
   - keep the part structure
   - keep run names
   - keep branch/tag/baseline metadata
   - keep implementation phase names
   - keep the claim-boundary rules
   - keep “Do Not Do Yet” restrictions

Do not remove:
   - PC → Printer content
   - PC ↔ Reader content
   - Player ↔ PC content
   - shared package/manifest/update-event model content
   - cross-corridor report/safety model
   - fixture/regression strategy
   - implementation phase order
   - Codex safety rules
   - unsafe_acceptance_count requirements
   - hardware claim boundary rules

Important source-note cleanup:
   If the source contains ChatGPT-only citation text or placeholder text such as:
   “physical player plan”
   then convert it into normal repo-readable source-note wording where appropriate.

Do not include ChatGPT-only file citation markers in the committed Markdown unless they are intentionally converted into normal source notes.

The repo Markdown should be readable on GitHub.

Required top-of-file wording:
The file must clearly state that this is a software planning and implementation-control document and that it does not claim:
   - real hardware validation
   - manufactured player completion
   - physical Level 5 completion

The document must keep these current claim-boundary values:
   - hardware validation claimed: false
   - physical Level 5 claimed: false
   - Manufactured player claimed: false

## Source Anchors from Physical-Player Dossier

This collection is derived from the AMCF software dossier source record `software plan.txt` and from the prior AMCF physical-player design/control sequence. In repo form, ChatGPT-only citation placeholders from the source record are converted into this normal source-note wording.

The source anchors preserved here are:

- PC -> Printer, PC <-> Reader, and Player <-> PC are treated as software I/O corridors.
- The physical player is modelled as a future executor of digital AMCF schedule/update-event data through a physical carrier and optical viewing window.
- The shared AMCF package, manifest, update-event, physical-section, report, fixture, and safety models are central to all corridors.
- Physical hardware validation, manufactured player completion, and physical Level 5 completion are not claimed.

## Claim Boundary

This dossier describes software planning, software architecture, simulated control, package models, reports, fixtures, and implementation sequencing.

Current claim-boundary values:

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false

This dossier does not claim real hardware validation, manufactured player completion, physical Level 5 completion, real printer/scanner/player integration, or hardware proof.

## Corridor Summary

### PC -> Printer

Prepare digital AMCF package data for future printable/exported physical carrier packages using shared schedule, manifest, section, lane, registration, colour, metadata, hash, and report models.

### PC <-> Reader

Recover or verify physical AMCF carrier data back into digital AMCF through no-hardware-first fixtures, captures, lane recognition, hash/checksum validation, diagnostics, and audit reports.

### Player <-> PC

Support future physical/optical player alignment through package compatibility checks, capability profiles, runtime simulation, fail-closed decisions, bounded reverse/seek control, diagnostics, and future protocol boundaries.

## Implementation Phase Index

0. `AMCF_SOFTWARE_IO_BRANCH_BASELINE_V1`
1. `AMCF_SOFTWARE_IO_REPO_AUDIT_V1`
2. Shared AMCF package / manifest / update-event / physical-section model foundation
3. Cross-corridor report, claim-boundary, and safety model foundation
4. PC -> Printer software path planning and no-hardware fixture path
5. PC <-> Reader software path planning and no-hardware fixture path
6. Player <-> PC software path alignment and simulator-control bridge
7. Cross-corridor fixture and regression strategy
8. Public docs / release / package refresh for software I/O work

## First Implementation Phase

The first Codex implementation phase after this collection is:

`AMCF_SOFTWARE_IO_REPO_AUDIT_V1`

That phase should audit the existing repo and classify current source, docs, demos, tests, reports, schemas, and generated-output conventions by corridor. It should not implement printer, reader, player runtime, package-model, or report-model modules yet.

## Implementation Control Rules

1. Implement one phase at a time.
2. Run repo audit before creating new models.
3. Do not introduce hardware APIs before no-hardware fixtures pass.
4. Do not introduce GUI before CLI/report flows pass.
5. Do not introduce dependencies unless the current phase justifies them.
6. Keep generated output under `output/`.
7. Do not commit generated output.
8. Keep `unsafe_acceptance_count` at 0.
9. Keep hardware claim flags false.
10. Run `python -m unittest discover -s tests` before commit.
11. Commit only intended files.
12. Do not push unless explicitly instructed.

## Do Not Do Yet

Do not implement yet:

- real printer driver integration
- real scanner API
- camera capture
- USB/HID/serial player protocol
- firmware protocol
- GUI application
- local web UI
- image-processing dependency
- PDF dependency
- barcode/QR dependency
- hardware-in-the-loop tests
- physical-player hardware validation claims
- `AMCF_SOFTWARE_IO_REPO_AUDIT_V1` implementation in this collection-file task

---

Do not implement any software phase in this task.

Do not create:
   - demo/run_amcf_software_io_repo_audit.py
   - tests/test_amcf_software_io_repo_audit.py
   - src/amcf_package_model.py
   - src/amcf_report_model.py
   - printer modules
   - reader modules
   - player runtime modules

Do not add dependencies.

Do not add GUI.

Do not add hardware APIs.

Do not add PDF/image/barcode/scanner/USB support.

Do not alter existing physical-player simulator logic.

Do not alter existing release/tag prep logic.

Validation:

Run:
   python -m unittest discover -s tests

Also run:
   git status --short
   git diff --stat

If tests fail because of pre-existing unrelated issues, report that clearly and do not hide it.

Commit rules:

Stage only:
   docs/AMCF_SOFTWARE_DEVELOPMENT_AND_IO_CONTROL_DOSSIER_COLLECTION.md

Do not stage:
   output/
   __pycache__/
   generated files
   broad directories
   unrelated files

Commit message:
   Add AMCF software IO dossier collection

Do not push unless explicitly instructed.

Final report must include:
   - run name
   - branch
   - base HEAD
   - files created/changed
   - tests run
   - test result
   - git diff --stat
   - whether generated output was committed
   - whether hardware validation is claimed
   - whether physical Level 5 is claimed
   - whether manufactured player is claimed
   - commit hash if committed
   - push command if applicable

Expected result:
A single committed Markdown file exists at:

docs/AMCF_SOFTWARE_DEVELOPMENT_AND_IO_CONTROL_DOSSIER_COLLECTION.md

No implementation of AMCF_SOFTWARE_IO_REPO_AUDIT_V1 has happened yet.
```

---

## 6. What Part 13 decides

Part 13 decides:

```text
- the first Codex handoff should be Version A
- Version A creates the dossier collection file only
- the attached software plan.txt is now the source record
- Codex should preserve the dossier structure and clean only obvious chat artifacts
- Codex should not implement AMCF_SOFTWARE_IO_REPO_AUDIT_V1 yet
- repo audit becomes the next prompt after the collection file is committed
```

## 7. What Part 14 should be

Part 14 should provide:

```text
Version B — Codex prompt for AMCF_SOFTWARE_IO_REPO_AUDIT_V1
```

That prompt should assume this file already exists:

```text
docs/AMCF_SOFTWARE_DEVELOPMENT_AND_IO_CONTROL_DOSSIER_COLLECTION.md
```

Then it should instruct Codex to read it and implement only:

```text
AMCF_SOFTWARE_IO_REPO_AUDIT_V1
```
-----



