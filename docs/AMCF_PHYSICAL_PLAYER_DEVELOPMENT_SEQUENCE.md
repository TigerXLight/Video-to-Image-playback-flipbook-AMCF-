# AMCF Physical Player Development Sequence

This sequence tracks the software/control simulator branch for a future compact mechanical/optical AMCF player. It does not mark physical hardware complete and does not claim hardware validation.

## Stage 1

`AMCF_PHYSICAL_PLAYER_SIMULATOR_MODELS_V1`

Purpose: model foundation for folded-path A/B physical-player simulation.

Commit: no separate known commit in this public sequence. The model structures were effectively folded into the later state-machine and Physical I/O architecture work.

Validation summary: represented by later state-machine, fail-closed, reverse/seek, mechanism-profile, and integrated-demo validation.

Claim boundary: software/control model framing only; no physical hardware validation.

## Stage 2

`AMCF_PHYSICAL_PLAYER_STATE_MACHINE_V1`

Commit: `f8b6e91e1dfd9b57345ee38ac262635d446f47c8`

Purpose: implement the deterministic physical-player control state machine.

Validation summary: py_compile PASS, unittest discovery PASS, state-machine demo PASS, final playback state `park_old_section`, fail-closed event count 1, `unsafe_acceptance_count` 0.

Claim boundary: safe forward playback cycle, state transitions, event logs, fail-closed integration, and local reverse/seek denial basics are software/control simulator behaviour only.

## Stage 3

`AMCF_PHYSICAL_PLAYER_FAIL_CLOSED_V1`

Commit: `4716c3b3df25b63f39b2d1430bdccfbc2f0bfb0e`

Purpose: harden the fail-closed safety layer.

Validation summary: py_compile PASS, unittest discovery PASS with 121 tests, fail-closed demo PASS, fail-closed scenario count 21, fail-closed event count 10, `unsafe_acceptance_count` 0.

Claim boundary: structured safety decisions and failure scenarios are software/control simulator behaviour only; no real sensors, motors, cartridges, or hardware validation.

## Stage 4

`AMCF_PHYSICAL_PLAYER_REVERSE_SEEK_V1`

Commit: `802042b5395ac860c437188e0d79031d7dd5f591`

Purpose: add bounded reverse and local-buffer seek controls.

Validation summary: reverse/seek demo PASS, reverse attempts/successes/denials 2 / 1 / 1, seek attempts/successes/denials 2 / 1 / 1, arbitrary seek denied count 1, `unsafe_acceptance_count` 0.

Claim boundary: reverse and seek are limited software/control behaviours. Real reverse hardware and arbitrary physical seek hardware are not claimed.

## Stage 5

`AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES_V1`

Commit: `01093024f9bbd11d10615a0f526b4440e5f8f41b`

Purpose: add mechanism profiles and the default simulator profile.

Validation summary: py_compile PASS, unittest discovery PASS with 166 tests, mechanism profiles demo PASS, profile count 10, default profile ID `folded_ab_motor_encoder_baseline`, hardware-validated profile count 0, physical-Level-5-claimed profile count 0.

Claim boundary: mechanism profiles are software/control references and research candidates; no mechanism is physically validated.

## Stage 6

`AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO_V1`

Commit: `fea00409262dea39d5c9068daac0a206c02d07f5`

Purpose: integrate mechanism profiles, forward playback, fail-closed safety, reverse/seek, unsafe-acceptance audit, and unified reports.

Validation summary: py_compile PASS, unittest discovery PASS with 185 tests, integrated simulator demo PASS, state-machine demo PASS, fail-closed demo PASS, reverse/seek demo PASS, mechanism profiles demo PASS, `unsafe_acceptance_count` 0, integrated report passed.

Claim boundary: integrated deterministic software/control simulator package only; no manufactured physical player, real optical playback proof, physical Level 5, or hardware validation.

## Stage 7

`AMCF_PHYSICAL_PLAYER_PUBLIC_DOCS_SYNC_V1`

Commit: `c7c2658877f04d40b94b127c6e44fe30d3597a18`

Purpose: synchronize public docs, navigation, claim boundaries, Pages links, docs map, public summary, and docs-link tests.

Validation summary: py_compile PASS, unittest discovery PASS with 197 tests, integrated simulator demo PASS, docs map created, public summary created, README updated, claim boundaries updated.

Claim boundary: documentation/navigation sync only; no runtime behaviour change and no hardware validation claim.

## Stage 8

`AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW_V1`

Commit: `659bd3e74a9e4dd254600558aec6e76309ba596f`

Purpose: release-style review of the physical-player software/control branch. It verifies tests, demos, docs, site navigation, claim boundaries, generated-output policy, local-path scan, and release review report.

Validation summary: py_compile PASS, unittest discovery PASS with 214 tests, integrated simulator demo PASS, release review script PASS, all physical-player demos PASS, release review final_passed yes, `unsafe_acceptance_count` 0.

Claim boundary: software/control release review only; no physical hardware validation and no physical Level 5 claim.

## Stage 9

`AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH_V1`

Commit: `8f76d7528e4f6399ef719a99f15e1b248ce8e2ff`

Purpose: public package/release inventory refresh. It verifies source, docs, demos, tests, site inclusion, generated-output exclusion, claim-boundary scan, local-path scan, and package refresh report.

Validation summary: py_compile PASS, unittest discovery PASS with 233 tests, integrated simulator demo PASS, release review script PASS, package refresh script PASS, package refresh final_passed yes, `unsafe_acceptance_count` 0.

Claim boundary: software/control release-package refresh only; no physical hardware validation, no physical Level 5 claim, and no manufactured physical player claim.

## Stage 10

`AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW_V1`

Commit: `8082f0a1134ea33df330c0508f06cc3ff7130e59`

Purpose: final GitHub Pages/public documentation review. It verifies README entry points, docs map and public summary, site navigation, release review and package inventory links, generated-output exclusion, local-path scan, and unsafe hardware claim scan.

Validation summary: py_compile PASS, unittest discovery PASS with 253 tests, integrated simulator demo PASS, release review script PASS, package refresh script PASS, final Pages review script PASS, all physical-player demos PASS, final Pages review final_passed yes, `unsafe_acceptance_count` 0.

Claim boundary: software/control public-docs review only; no physical hardware validation, no physical Level 5 claim, and no manufactured physical player claim.

## Stage 11

`AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF_V1`

Commit: current run, not committed yet.

Purpose: final public-release closeout handoff. It summarizes commits, tests, demos, docs, site, package state, claim boundaries, generated-output policy, local-path scan, and unsafe-claim scan.

Validation summary: to be recorded by this run.

Claim boundary: software/control closeout handoff only; no physical hardware validation, no physical Level 5 claim, and no manufactured physical player claim.

## Later Stages

Later work may add richer physical-player model bundles, PC recognition/control simulation, hardware adapter boundaries, and end-to-end Physical I/O simulation. Those later stages must preserve the claim boundary: no hardware validation is claimed until real hardware tests exist.
