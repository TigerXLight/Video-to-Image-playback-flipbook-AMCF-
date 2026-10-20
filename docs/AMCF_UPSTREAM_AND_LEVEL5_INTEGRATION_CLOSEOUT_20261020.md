# AMCF Upstream and Level 5 Integration Closeout

Date: 2026-10-20

This document records exactly what was integrated into Main and what remains
an external research dependency. It prevents the accepted Level 5 result from
being confused with bundling every upstream tracking repository.

## Local availability

The local workspace contains the inspected repository clones under
`Github repos/`, including the SAMURAI/SAM2 material and CoTracker, and the
Level 5 research run contains the associated local checkpoints. Main's
`amcf_vnext.py toolchain-status` check found the configured repository and
checkpoint paths.

The same check deliberately reports:

- `deep_tools_run: false`
- `sam2` Python import not resolvable in the maintained runtime
- `cotracker` Python import not resolvable in the maintained runtime
- no deep inference executed by the status command

This is intentional. The status command verifies optional local availability;
it is not a deep-tool inference runner.

## What Main contains

The accepted AMCF functionality and Level 5 promotion surface are present in
the maintained package:

- `src/amcf_semantic_level5_proof.py` records the progression, rejected or
  parked pre-Level-5 runs, accepted controlled proof, accepted HOOT proof, and
  Main promotion.
- `src/amcf_vnext.py` validates the controlled and HOOT evidence, preserves the
  claim boundary, and exposes status, validation, archive inspection, and
  optional-toolchain status commands.
- The native AMCF archive, reader, compositor, diagnostics, decoded playback,
  software-I/O, and physical-player simulation modules are maintained source,
  not references to an upstream implementation.
- Tests and demos cover the accepted proof index and keep physical hardware
  claims fail-closed.

The exact-file audit found zero exact file-hash matches between the maintained
Main code/text set and the third-party reference code/text set. There are no
upstream deep-tool source trees or model checkpoints inside the clean Main
package.

## What was not integrated

Main does not embed the SAM2/SAMURAI, CoTracker, RAFT, Cutie, XMem, DEVA,
TAPNet, AOT, Track-Anything, or Segment-and-Track-Anything repositories,
checkpoints, or weights. These remain optional research material. The public
clone intentionally excludes them and excludes the local Test evidence.

Therefore the precise result is:

| Capability | Status |
| --- | --- |
| Accepted controlled and HOOT Level 5 result represented in Main | Integrated and validated |
| Core AMCF archive/playback requiring deep tools | Not required; direct playback is source-independent |
| Re-running SAM2/CoTracker inference from a clean Main checkout | Not included; external local research dependencies required |
| Full upstream repository source copied into Main | No; intentionally excluded |

## Why this is not a missing core feature

The accepted Level 5 closeout is an evidence and claim-boundary integration,
not a requirement that every experimental inference engine become part of the
AMCF archive/player. The deep repositories were used to produce bounded local
research evidence. Main preserves the accepted result and validates its
scope; it does not falsely claim that a clean public checkout can rerun those
deep models without their separate repositories, checkpoints, and licences.

If reproducible deep inference from a clean checkout becomes a requirement,
that must be a separate adapter package with explicit per-repository licence,
checkpoint, dependency, and distribution decisions. It should not be created
by copying the current research repositories into the core package.

## Final result

Within the current project contract, no missing maintained AMCF functionality
was found. The local Main workspace has the optional external research inputs
and the accepted Level 5 evidence; the maintained Main/public package has the
accepted proof/status and core playback behavior. The distinction between
integrated AMCF functionality and external deep inference is now explicit.
