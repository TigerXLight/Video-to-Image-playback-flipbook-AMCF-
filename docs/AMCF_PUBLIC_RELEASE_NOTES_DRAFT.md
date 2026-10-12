# AMCF Physical-Player Software-Control Public Release Draft

## Proposed Title

AMCF physical-player software-control public release v1

## Suggested Tag Name

`amcf-physical-player-software-control-v1`

Alternate date-style suggestion:

`amcf-public-release-2026-10-12`

## Baseline Commit

`331848fdf10ff18eab0a9426441f0f00e91a8f03`

## Summary

This draft summarizes a possible public release tag for the AMCF physical-player software/control simulator and public documentation sequence. AMCF remains software-first. The physical-player branch defines and tests deterministic control behaviour that later mechanical/optical hardware should follow, but it does not prove manufactured hardware exists.

## What Changed

- deterministic physical-player state machine
- structured fail-closed safety model
- bounded reverse and local-buffer seek controls
- mechanism profiles with default `folded_ab_motor_encoder_baseline`
- integrated simulator demo and report package
- public docs map and summary
- release review, package refresh, final Pages review, and closeout handoff
- generated-output, local-path, unsafe-claim, and claim-boundary checks

## Physical-Player Software/Control Sequence

- Stage 2: `f8b6e91e1dfd9b57345ee38ac262635d446f47c8`
- Stage 3: `4716c3b3df25b63f39b2d1430bdccfbc2f0bfb0e`
- Stage 4: `802042b5395ac860c437188e0d79031d7dd5f591`
- Stage 5: `01093024f9bbd11d10615a0f526b4440e5f8f41b`
- Stage 6: `fea00409262dea39d5c9068daac0a206c02d07f5`
- Stage 7: `c7c2658877f04d40b94b127c6e44fe30d3597a18`
- Stage 8: `659bd3e74a9e4dd254600558aec6e76309ba596f`
- Stage 9: `8f76d7528e4f6399ef719a99f15e1b248ce8e2ff`
- Stage 10: `8082f0a1134ea33df330c0508f06cc3ff7130e59`
- Stage 11: `331848fdf10ff18eab0a9426441f0f00e91a8f03`

Stage 1 model-foundation was not a separate pushed commit in this sequence; early model structures were folded into the state-machine run because no standalone model module existed at that time.

## Public Documentation And Pages

The public docs include the physical-player docs map, public summary, simulator demo docs, release review, package inventory, final Pages review, and closeout handoff. The Pages site links to the physical-player software/control documentation and preserves the no-hardware-validation boundary.

## Release / Package Review

The release review, package refresh, final Pages review, and closeout handoff report that generated output remains uncommitted, local path scans pass, unsafe hardware claim scans pass, and `unsafe_acceptance_count` remains 0.

## Tests And Demos

Suggested verification before creating a tag:

```bash
python -m py_compile demo/run_public_release_tag_prep.py
python -m unittest discover -s tests
python demo/run_physical_player_simulator_demo.py
python demo/run_physical_player_release_review.py
python demo/run_public_release_package_refresh.py
python demo/run_public_github_pages_final_review.py
python demo/run_public_release_closeout_handoff.py
python demo/run_public_release_tag_prep.py
```

## Claim Boundaries

This draft claims software/control simulator work, deterministic demos, public docs, release/package checks, and tag-prep materials. It does not claim manufactured hardware, hardware validation, physical Level 5 completion, real optical playback proof, real reverse hardware, or arbitrary physical seek hardware.

## What Is Not Claimed

- manufactured physical player
- real motors or sensors
- real cartridge validation
- real optical playback proof
- real no-gap physical switching proof
- real reverse hardware
- arbitrary physical seek hardware
- physical Level 5 completion
- hardware validation

## Suggested Verification Commands

Run the validation commands listed in `docs/AMCF_PUBLIC_RELEASE_TAG_PREP.md` and `docs/AMCF_PUBLIC_RELEASE_TAG_CHECKLIST.md` before any tag is created.

## Tag Creation Is Not Performed In This Run

This run prepares release-tag materials only. No Git tag is created, no tag is pushed, and no GitHub release is created.
