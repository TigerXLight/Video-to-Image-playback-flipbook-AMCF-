# AMCF Public GitHub Pages Final Review

## Purpose

`AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW_V1` performs a final public GitHub Pages and documentation review after the physical-player software/control simulator sequence.

Baseline commit: `8f76d7528e4f6399ef719a99f15e1b248ce8e2ff`.

This review is a public documentation/release-readiness artifact. It is not hardware proof.

## What The Final Review Checks

- README public entry points
- docs map completeness
- public summary availability
- `site/index.html` navigation
- release review links
- package refresh and inventory links
- claim-boundary visibility
- generated-output exclusion
- local-path scan
- unsafe hardware claim scan
- integrated simulator `unsafe_acceptance_count`

## README Entry-Point Checks

README should link to the physical-player docs map, public summary or simulator docs, package refresh or inventory docs, and this final review doc.

## Docs Map Checks

The docs map should link the physical-player concept, state machine, fail-closed, reverse/seek, mechanism profiles, integrated simulator demo, release review, package refresh, package inventory, final Pages review, development sequence, claim boundaries, and hardware/software paths.

## Public Summary Checks

`docs/AMCF_PHYSICAL_PLAYER_PUBLIC_SUMMARY.md` should remain the short public-facing explanation of what is implemented in software/control and what is not claimed.

## Site Checks

`site/index.html` should expose the physical-player docs map or public summary, integrated simulator or release/package docs, and claim boundaries. The site remains documentation/context only.

## Release Review And Package Inventory Checks

The final review checks that `docs/AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW.md`, `docs/AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH.md`, and `docs/AMCF_PUBLIC_RELEASE_PACKAGE_INVENTORY.md` are publicly reachable from the docs map and site navigation.

## Claim-Boundary Checks

The review scans public docs and site files for unsafe affirmative hardware claims while allowing negative boundary wording such as "not claimed" or "no hardware validation".

## Generated-Output Checks

Generated `output/` and `demo/output/` folders may exist locally. They should remain ignored and uncommitted.

## Local-Path Checks

Public docs and site files should not include machine-specific local Windows paths, local run folders, package working-copy paths, or Codex runtime paths.

## What Is Not Claimed

This review does not claim manufactured hardware, real motors, real sensors, real cartridge validation, real optical playback proof, real no-gap physical switching proof, real reverse hardware, arbitrary physical seek hardware, physical Level 5 completion, or hardware validation.

## How To Run

```cmd
python demo/run_public_github_pages_final_review.py
```

Expected output folder:

`output/public_github_pages_final_review/`

## Next Development Step

Push the final public Pages review commit, then verify the published GitHub Pages action output in the browser.
