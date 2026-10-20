# AMCF Physical Software Adapter Layer

## Purpose

This layer is the software contract between the digital AMCF process and the
future physical carrier, reader, and player adapters. It makes the existing
no-hardware corridor simulations observable through one deterministic run.

The contract does not redefine AMCF. Digital AMCF remains the canonical
component/image representation, scheduler, synchronised compositor, and
decoded-video path. A future physical player must execute the same update
schedule through a physical/optical medium; it is not a fixed-FPS page machine
or a screen replacement.

## Corridors

The adapter roundtrip covers four cooperating boundaries:

1. PC-to-printer/carrier: validate indexed carrier layout, timing/index lanes,
   registration, image payload, colour registry, metadata, and checksum lanes.
2. Reader-to-PC: recover sections from the maintained fixture, validate
   registration and hashes, emit diagnostics, and reject an unsafe display
   state.
3. PC-to-player: validate the folded indexed-carrier profile, prefetch and
   stage sections, switch a verified section, and exercise bounded reverse and
   local seek behaviour.
4. Shared core: rerun the shared manifest, reporting, and cross-corridor
   validator so the individual adapters cannot pass with incompatible shared
   assumptions.

The physical player model remains the dossier model: a compact
tablet-like mechanical/optical device, folded internal indexed-media path,
current visible view gate, hidden staging gate, prefetch, illumination or
blanking during transitions, timing/index feedback, and a dynamic AMCF update
schedule. The software contract does not claim that this mechanism has been
manufactured or validated.

## Status and fail-closed feedback

Every adapter emits an ordered status event with:

- adapter and corridor identity;
- state and machine-readable code;
- accepted/rejected result and severity;
- display and transition permissions;
- retry/rescan recommendation;
- fail-closed state;
- unsafe-acceptance marker.

The successful software-only run deliberately reports
display_allowed=false and transition_allowed=false. It means the software
contract is ready for device-specific adapter planning, not that a physical
device may move or display media.

If a fixture fails, raises an exception, or reports unsafe acceptance, the
contract records a rejected/fault state and keeps the system fail-closed.
Reader failures may request a rescan; other recovery actions remain explicit
in the event stream.

## Command

From the repository root:

    python src/amcf_cli.py adapter-roundtrip --project-root . --output output/physical_adapter_layer

The installed console command is equivalent:

    amcf adapter-roundtrip --project-root . --output output/physical_adapter_layer

The output contains:

- physical_software_adapter_report.json
- adapter_status_events.json
- adapter_feedback.json
- PHYSICAL_SOFTWARE_ADAPTER_ROUNDTRIP_SUMMARY.md
- pc_to_printer/
- reader_to_pc/
- pc_to_player/
- shared_core/

## Current boundary

This is a deterministic software-only contract. It does not use or claim:

- a real printer or printer driver;
- a real scanner, camera, OCR, or barcode reader;
- USB, serial, firmware, motor, sensor, or cartridge hardware;
- a manufactured player;
- physical Level 5 or physical-medium proof.

The next hardware-specific phase must select concrete device interfaces and
add a separate adapter implementation for each device. The offline planning
layer now records those Windows-facing provider choices and their capability,
feedback, and safety contracts. See
docs/AMCF_HARDWARE_ADAPTER_PLANNING_LAYER.md.
