# AMCF Physical Player State Machine

## Purpose

The physical-player state machine defines the software/control structure that a later physical AMCF player would need.

The hardware is not present yet. The software state machine can still be implemented now. Later hardware should conform to this software/control logic.

## Corrected Framing

AMCF is software-first. Digital AMCF is the canonical representation, scheduler, compositor, and validation model. A future physical/optical player executes the AMCF schedule using material carrier sections.

This state machine is a deterministic software/control simulator. It is not manufactured hardware, real sensor validation, real motor validation, real physical cartridge validation, real optical playback proof, real no-gap proof, physical Level 5 completion, or hardware validation.

## State List

- `no_cartridge`
- `cartridge_inserted`
- `manifest_recognized`
- `prefetch_current`
- `verify_current`
- `load_view_gate`
- `view_gate_locked`
- `playback_ready`
- `prefetch_next`
- `verify_next`
- `stage_next`
- `wait_update_timestamp`
- `transition_blank`
- `switch_visible_section`
- `park_old_section`
- `paused_safe`
- `rescan_required`
- `retry_allowed`
- `fail_closed`
- `mechanical_stop`
- `playback_complete`

## Normal Forward Chain

```text
no_cartridge
-> cartridge_inserted
-> manifest_recognized
-> prefetch_current
-> verify_current
-> load_view_gate
-> view_gate_locked
-> playback_ready
-> prefetch_next
-> verify_next
-> stage_next
-> wait_update_timestamp
-> transition_blank
-> switch_visible_section
-> park_old_section
-> prefetch_next
```

The core principle is:

```text
current section visible
-> next section prefetched
-> next section verified
-> next section staged hidden
-> update timestamp reached
-> transition blanking
-> staged section becomes visible
-> old section parks
-> repeat
```

## Failure Branch

The state machine fails closed for unverified sections, wrong sections, hash mismatch, registration failure when it cannot safely proceed, unlocked gates, prefetch timeout, shutter/illumination failure, jam, manifest mismatch, unsupported carrier, or audio sync limits.

Fail-closed mode disables playback, motion, and transitions. It does not count unsafe acceptance as a success path.

## Reverse Branch

Reverse is limited to the local reverse/park buffer. It does not claim arbitrary physical reverse.

## Seek Branch

Seek is local-buffer only in this stage. Unsupported arbitrary seek is denied safely with `unsupported_or_not_in_local_buffer`.

## What Can Be Tested Without Hardware

- cartridge insertion and manifest recognition policy
- section prefetch and verification decisions
- visible view-gate loading and locking
- hidden-gate staging
- transition blanking
- switch and park sequence
- local reverse-buffer behavior
- local seek denial
- fail-closed event creation
- event log serialization

## What Is Not Claimed

- manufactured hardware
- real sensors
- real motors
- real physical cartridge validation
- real optical playback proof
- real no-gap proof
- physical Level 5 completion
- hardware validation
