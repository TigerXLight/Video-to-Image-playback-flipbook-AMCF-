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

Commit: current run, not committed yet.

Purpose: synchronize public docs, navigation, claim boundaries, Pages links, docs map, public summary, and docs-link tests.

Validation summary: to be recorded by this run.

Claim boundary: documentation/navigation sync only; no runtime behaviour change and no hardware validation claim.

## Later Stages

Later work may add richer physical-player model bundles, PC recognition/control simulation, hardware adapter boundaries, and end-to-end Physical I/O simulation. Those later stages must preserve the claim boundary: no hardware validation is claimed until real hardware tests exist.
