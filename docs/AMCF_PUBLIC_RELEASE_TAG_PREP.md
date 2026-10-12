# AMCF Public Release Tag Prep

## Purpose

`AMCF_PUBLIC_RELEASE_TAG_PREP_V1` prepares release-tag materials for the AMCF physical-player software/control simulator and public documentation sequence.

This run does not create a Git tag. It prepares a deterministic tag-readiness report, release-notes draft, and checklist for later human review.

## Baseline Commit

`331848fdf10ff18eab0a9426441f0f00e91a8f03`

## What Tag Prep Checks

- current HEAD and branch are readable
- existing tags can be listed without creating a tag
- closeout handoff, release review, package refresh, final Pages review, docs map, site, and claim boundaries exist
- development sequence includes Stages 2 through 12 and known commits through Stage 11
- generated output is not tracked or staged
- public docs and site contain no local workspace paths
- public docs and site contain no unsafe affirmative hardware claims
- `unsafe_acceptance_count` remains 0 through the integrated simulator summary
- tag creation remains unperformed

## Suggested Tag Name

`amcf-physical-player-software-control-v1`

Alternate date-style suggestion:

`amcf-public-release-2026-10-12`

## Suggested Release Title

AMCF physical-player software-control public release v1

## Release Notes Draft Summary

The release-notes draft summarizes the software/control simulator sequence, public docs, release review, package inventory, final Pages review, and closeout handoff. It preserves the boundary that the project has not manufactured or validated physical hardware.

## Validation Checklist

- py_compile passes for tag-prep and public review scripts
- unittest discovery passes
- integrated simulator demo passes
- release review passes
- package refresh passes
- final Pages review passes
- closeout handoff passes
- tag-prep report passes
- generated output remains untracked
- local path scan passes
- unsafe hardware claim scan passes

## Claim-Boundary Checklist

The prepared release materials do not claim:

- manufactured physical player
- real physical/optical playback proof
- real motor validation
- real sensor validation
- real cartridge validation
- real scan validation
- real no-gap physical switching proof
- real reverse hardware
- arbitrary physical seek hardware
- physical Level 5 completion
- hardware validation

## How To Run

```bash
python demo/run_public_release_tag_prep.py
```

## Expected Output Folder

`output/public_release_tag_prep/`

Generated output is local report output and should not be committed.

## Next Step

Review the release notes draft and checklist, push the tag-prep commit, then create an annotated tag only after explicit human approval in a later run.
