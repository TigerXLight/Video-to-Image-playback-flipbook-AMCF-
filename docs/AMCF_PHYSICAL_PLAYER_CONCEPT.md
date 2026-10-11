# AMCF Mechanical / Optical Physical Player Concept

## 1. Definition

The AMCF physical player is a future mechanical/optical playback device that uses controlled physical transport of AMCF media through a fixed view gate, with illumination or optical presentation, so the AMCF sequence can be viewed physically without requiring a digital display.

## 2. What it is not

- It is not the AMCF Player UI viewer.
- It is not a normal tablet/screen player.
- It is not merely software playback.
- It is not merely the physical reader/scanner.
- It is not a manufactured prototype yet.
- It is not a left-to-right flipbook by default.
- It is not manual-crank-first for primary fluid playback.

## 3. Physical playback path

```text
AMCF digital
-> prepared AMCF physical media
-> indexed physical transport
-> fixed physical view gate
-> illumination / optical presentation
-> direct human viewing
```

The intended carrier language is vertical-stack / indexed section physical-medium concept. The default carrier assumption is indexed thin-section AMCF physical media, not a continuous ribbon-first or film-first design.

## 4. Reader vs player

The physical reader/scanner path reads physical AMCF media lanes and validates timing/index, registration, colour, metadata, hash/checksum, and related recovery data. Its role is recovery, diagnostics, validation, and optional export back into digital AMCF state.

The physical player path presents the physical media directly. It uses transport, illumination, and a view gate so a person can view the AMCF sequence without relying on a digital display system for the playback act.

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
- vertical-stack / indexed-section transport
- fixed physical view gate geometry
- illumination/backlight/front-light options
- optical window or projection path
- speed governor or regulated transport
- brake/latch/pause
- reverse/seek/index where practical
- optional reader/recovery lane
- diagnostics and fail-closed policies

## 9. Claim boundaries

This document does not claim physical proof, physical Level 5, hardware validation, final UI, manufacturing readiness, physical player proof, or prototype completion.
