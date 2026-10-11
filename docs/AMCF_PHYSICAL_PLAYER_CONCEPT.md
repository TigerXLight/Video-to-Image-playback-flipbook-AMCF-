# AMCF Mechanical / Optical Physical Player Concept

## 1. Definition

The AMCF physical player is a future mechanical/optical playback device that uses controlled physical transport of AMCF media through a fixed view gate, with illumination or optical presentation, so the AMCF sequence can be viewed physically without requiring a digital display.

Digital AMCF is the canonical AMCF representation, scheduler, and validation model. Physical AMCF is the material embodiment of the same AMCF timing/update structure. The physical player does not replace AMCF logic; it physically/optically executes the AMCF schedule that is defined, tested, and validated digitally.

The preferred future mechanism is a dynamic folded-path A/B staged indexed-section player: a compact tablet-like handheld body with a folded internal media path, side-loaded cartridge/card/section stack, a visible view gate, a hidden preload/staging gate, shutter/illumination blanking, and reader/prefetch lanes for timing/index/hash checks.

## 2. What it is not

- It is not the AMCF Player UI viewer.
- It is not a normal tablet/screen player.
- It is not merely software playback.
- It is not merely the physical reader/scanner.
- It is not a manufactured prototype yet.
- It is not a left-to-right flipbook by default.
- It is not manual-crank-first for primary fluid playback.
- It is not a fixed-FPS physical page machine.
- It is not a long straight roller path by default.

## 3. Physical playback path

```text
AMCF digital
-> prepared AMCF physical media
-> folded indexed physical transport with A/B staging
-> fixed physical view gate
-> illumination / optical presentation
-> direct human viewing
```

The intended carrier language is vertical-stack / indexed section physical-medium concept. The default carrier assumption is indexed thin-section AMCF physical media, not a continuous ribbon-first or film-first design.

Physical AMCF playback should remain dynamic like digital AMCF. The player should move media according to the AMCF update schedule, hold visible states at the view gate, preload the next required section in a hidden staging gate, blank the optical path during the section switch, and fail closed if the next section cannot be verified in time.

## 4. Reader vs player

The physical reader/scanner path reads physical AMCF media lanes and validates timing/index, registration, colour, metadata, hash/checksum, and related recovery data. Its role is recovery, diagnostics, validation, and optional export back into digital AMCF state.

The physical player path presents the physical media directly. It uses transport, illumination, and a view gate so a person can view the AMCF sequence without relying on a digital display system for the playback act. It presents AMCF media according to the same dynamic update schedule validated by digital AMCF.

## 5. Combined reader-player appliance

A future combined reader-player appliance may share cartridge, media, transport, alignment, and control systems. It should still keep two roles distinct:

- physical view/playback gate for direct optical viewing
- reader/scanner lane for recovery, diagnostics, validation, and optional software export

## 6. Software support role

Software creates, validates, simulates, prepares, and optionally recovers or exports AMCF. Software can model virtual cartridges, virtual readers, virtual scan gates, validation events, and player handoff state.

Software does not replace the physical viewing act in the physical-player concept.

## 7. Current implementation status

The clean package currently implements software and virtual hardware support. It does not implement a real physical player, real physical reader, real scan gate, manufactured cartridge, optical mechanism, or hardware interface.

## 8. Future work

Future work may explore:

- indexed thin-section media preparation
- compact tablet-like folded internal media path
- three-pass folded path: input/preload, active view-gate, and return/park/reverse
- two-track A/B shuttle with visible/ready Track A and hidden preload/staging Track B
- indexed section stack, individual page/card shuttle, or linked indexed carrier
- magnetic, electrostatic, or mechanical guide tracks with stop gates
- fixed physical view gate geometry
- illumination/backlight/front-light options
- shutter/dwell timing and optical blanking during transitions
- optical window or projection path
- dynamic update schedule rather than fixed-FPS page motion
- motor/encoder feed, piezo/electrostatic inchworm feed, or constant-force spring with governor/brake
- reader/prefetch lane that scans timing/index/hash lanes ahead of playback
- sensor feedback and index lock
- fail-closed behavior if the next staged section is unverified
- brake/latch/pause
- reverse/seek/index where practical
- optional reader/recovery lane
- diagnostics and fail-closed policies

## 9. Claim boundaries

This document does not claim physical proof, physical Level 5, hardware validation, final UI, manufacturing readiness, physical player proof, or prototype completion.
