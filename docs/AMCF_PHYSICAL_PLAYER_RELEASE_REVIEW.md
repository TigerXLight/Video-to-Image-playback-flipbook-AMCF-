# AMCF Physical Player Release Review

## Purpose

`AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW_V1` reviews the public physical-player software/control simulator branch before release-style publishing or continued development.

Baseline commit: `c7c2658877f04d40b94b127c6e44fe30d3597a18`.

This review is a software/control release-review artifact. It is not physical hardware proof.

## What The Review Checks

- required physical-player docs exist
- required demo scripts exist
- required test files exist
- README links to the docs map and simulator demo docs
- claim boundaries include the physical-player software/control simulator boundary
- docs map links to all physical-player docs and demos
- site navigation links to physical-player docs
- development sequence mentions Stages 2 through 7 and known commits
- integrated simulator summary can be generated
- `unsafe_acceptance_count` remains 0
- generated demo output is not tracked or staged
- public docs do not leak local Windows workspace paths
- public docs do not contain unsafe affirmative hardware claims

## Tests And Demos Included

The release review is validated with unittest discovery and the integrated simulator demo. The physical-player demo family includes:

- `demo/run_physical_player_state_machine_demo.py`
- `demo/run_physical_player_fail_closed_demo.py`
- `demo/run_physical_player_reverse_seek_demo.py`
- `demo/run_physical_player_mechanism_profiles_demo.py`
- `demo/run_physical_player_simulator_demo.py`
- `demo/run_physical_player_release_review.py`

## Docs And Site Checks

The review checks `README.md`, `CLAIM_BOUNDARIES.md`, `docs/*.md`, and `site/index.html` for the expected public navigation and claim-boundary wording.

## Claim Boundary Checks

The review allows negative boundary wording such as "not claimed" or "no hardware validation". It flags unsafe affirmative overclaims such as real hardware validation, manufactured physical player existence, real optical playback proof, arbitrary physical seek proof, or physical Level 5 completion.

## Generated-Output Checks

Generated `output/physical_player_*` folders may exist locally after demos run. They should remain ignored and uncommitted.

## Local-Path Checks

Public docs and site files should not contain machine-specific local paths such as user directories, AppData, local test roots, Codex runtime paths, or package working-copy paths.

## What Is Not Claimed

This review does not claim manufactured hardware, real motors, real sensors, real cartridge validation, real optical playback proof, real no-gap physical switching proof, real reverse hardware, arbitrary physical seek hardware, physical Level 5 completion, or hardware validation.

## How To Run

```cmd
python demo/run_physical_player_release_review.py
```

The script writes deterministic output to:

`output/physical_player_release_review/`

## Next Step

If the review passes, push the release-review commit and continue future hardware-adapter alignment without hardware validation claims.
