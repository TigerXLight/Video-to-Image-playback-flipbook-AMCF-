# AMCF GitHub Clean Package

AMCF is a software-first runtime and validation path for indexed component playback. The AMCF digital representation/process is canonical. This clean package focuses on the reusable AMCF core plus virtual hardware support for future physical reader and physical player integrations.

## What is included

- AMCF v-next runtime source in `src/amcf_vnext.py`.
- Virtual cartridge, virtual reader, virtual scan-gate lane validation, player handoff state, and playback device abstraction in `src/amcf_virtual_hardware.py`.
- Sample virtual cartridge and player UI state JSON in `examples/`.
- Static AMCF Player UI state viewer stub in `viewer/`.
- Release demo and standard-library tests in `demo/` and `tests/`.
- Documentation for software-first hardware support, mechanical/optical physical-player boundaries, optional future deep-tool adapters, and claim boundaries.

## Software-first hardware support

No real hardware is required. Hardware support is represented through software abstractions and future adapter hooks:

- virtual cartridge
- virtual reader
- virtual scan gate
- lane validation
- player handoff state
- `SoftwarePlaybackDevice`
- `FuturePhysicalReaderAdapter`
- `FuturePhysicalPlaybackDevice`
- `ReaderPlayerApplianceAdapter`

The package works now in software through virtual hardware abstractions. Future physical work can connect through adapters, but this package does not require sensors, motors, cartridges, real scans, manufacturing, or a physical prototype.

## Physical reader and mechanical/optical physical player support

Physical reader support means future devices that read or scan AMCF physical media back into AMCF digital state for validation, recovery, diagnostics, or export.

Physical player support means future mechanical/optical devices that physically present AMCF media for direct viewing through controlled motion and a fixed view gate. A physical player may use indexed thin-section AMCF media, vertical-stack or indexed-section transport, illumination, optical viewing, projection, a window, speed regulation, brake/latch/pause, and reverse/seek/index where practical.

The physical player is not the same thing as the software UI viewer. It is not merely a digital monitor, tablet, or screen appliance. A combined reader-player appliance is possible later, with shared media/transport plus separate reader/recovery and physical view/playback roles.

The clean package provides software abstractions and docs now, not a manufactured device.

## Player UI state viewer

The static HTML viewer displays player-facing JSON state: reconstructed playback status, section timeline, reader/cartridge status, validation status, component payloads, alpha/object mask status, transform metadata, residual/tile payload state, validation log rows, and fail-closed decisions.

The viewer is a software inspection stub, not a final UI, not the physical player, and not playback proof.

## Optional future deep semantic adapters

The clean core package does not bundle SAM2, SAMURAI, CoTracker, AOT, Cutie, DEVA, RAFT, XMem, TAPNet, Track-Anything, copied third-party repositories, model checkpoints, or deep-tool weights.

Future optional deep semantic adapters require their own licence and provenance boundaries. If commercial use is restricted for an adapter, describe that work as source-available non-commercial or non-commercial research software, not strict OSI open source.

## Claim boundaries

This package does not claim physical proof, physical Level 5, hardware validation, manufacturing readiness, final UI, real scans, physical player proof, or a built prototype.

Physical reader/player concepts are future-facing support targets. The physical-medium language should stay vertical-stack / indexed section physical-medium concept, not left-to-right flipbook-first.

## Licence / publication status

No final licence has been selected. Public GitHub upload should choose and document a licence or publication status first. Private GitHub upload can proceed with no licence only if intentionally private/no-license.

Until licence and commercial-use status are finalised, avoid describing the package as strict open source.

## Quickstart

See `QUICKSTART.md` for demo and test commands.

## Source frames/video to AMCF digital smoke demo

The package includes a deterministic source-frame to AMCF digital smoke demo. It generates a tiny standard-library PPM frame set, encodes those frames into an actual `.amcf.zip` archive, writes manifest metadata and per-frame SHA-256 checksums, then validates the archive by reading it back.

This proves the clean package can create AMCF digital output from source frames. Arbitrary real-world video ingestion may require later optional tooling and is not claimed by this smoke demo.

This smoke path does not claim physical proof, hardware validation, final UI status, manufacturing readiness, or a built physical prototype.

## AMCF digital to printable/indexed physical carrier package

The package can generate a software physical-carrier output package from an AMCF digital archive. The output uses vertical-stack / indexed-section carrier framing and includes timing/index, registration, payload, colour registry, metadata, and hash/checksum lanes.

This is a software-generated carrier preparation package. It is not proof of physical printing, hardware validation, manufacturing readiness, or a built physical prototype. Real physical printing and manufacture remain optional future work.

## Virtual reader recovery/export demo

The package can simulate a reader/recovery path from generated carrier sections. It reads the software-generated indexed carrier package, validates lanes, indices, hashes, and section count, then recovers AMCF state and exports recovered PPM frame payloads.

This is a virtual reader/recovery demo, not real scanner hardware validation. MP4/video-container export is not claimed by this smoke path.

## Mechanical / optical physical player simulator

The package can simulate the future mechanical/optical physical-player path. It models indexed carrier sections moving through a fixed view gate, including illumination, alignment, playback timeline state, and controls for play, pause, step, reverse, and seek.

This is not a digital-screen physical player. It is not real physical playback and not hardware validation. Real physical manufacture and testing remain optional future work.

## Concept assets and physical-player correction

`assets/concepts/` contains current and legacy AMCF concept references. Old diagrams may be superseded and are retained for context only.

The corrected mechanical/optical physical-player concept is the current physical-player reference. In this package, physical player means mechanical/optical playback through indexed media, a fixed view/playback gate, illumination, and an optical viewing path for direct human viewing.

The physical player is not a digital-screen player, not the software UI viewer, and not the reader/scanner path. Concept assets do not claim hardware validation, physical proof, final UI, manufacturing readiness, or a built prototype.

## GitHub Pages site

Static site files live in `site/`.

The GitHub Pages workflow lives in `.github/workflows/pages.yml`.

After uploading to GitHub, enable Pages using GitHub Actions if needed. The Pages site is documentation/context only. It does not change AMCF functionality and does not claim hardware validation, physical proof, final UI, manufacturing readiness, or a built prototype.
