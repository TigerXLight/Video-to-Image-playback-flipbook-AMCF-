# AMCF Universal Hardware Simulation

## Purpose

This run is the software base for the future physical AMCF layer. It exercises
the shared package, timing/update-event model, carrier artifact path, capture
feedback, staged player control, and fail-closed decisions without requiring
hardware.

It is a simulation of the software contracts, not a claim that a printer,
scanner, reader, motor, optical player, or physical carrier has been built or
validated.

The simulation is action-level: it records command/response transcripts and
fault decisions, rather than only checking static provider descriptors.

## Command

From the project root:

```cmd
amcf hardware-simulation --project-root . --output output\universal_hardware_simulation
```

The direct source-tree form is:

```cmd
python src\amcf_cli.py hardware-simulation --project-root . --output output\universal_hardware_simulation
```

## Simulated paths

The run covers the following paths. `Reader -> Printer` is a validated relay
through the software control plane; it is not a separate physical bus claim.

1. `PC -> Printer`: create a carrier artifact, verify the canonical manifest
   hash, poll the result, close the session, and reject a bad manifest hash.
2. `PC -> Reader`: open a reader session, inspect status, select and read a
   section, request a rescan, reread it, reject an out-of-range selection, and
   close the session.
3. `Reader -> PC`: recover section captures and require registration and
   payload-hash agreement. Invalid captures remain fail-closed and request a
   rescan.
4. `Reader -> Printer`: attach capture attestations to a reprint manifest and
   create a second carrier artifact only after every capture is accepted.
5. `Player <-> PC`: load the manifest, prefetch a hidden staging section,
   verify it, and permit the software switch only after verification.
6. `Player -> PC`: return playback, validation, output, and fault status after
   load, play, pause, seek, and reverse actions.
7. Virtual reader/player: run indexed sections through a scan gate and a
   folded A/B staged-player timeline. The model includes timing markers,
   registration, component payload, alpha/object masks, colour registry,
   metadata/transform, and hash/checksum lanes.
8. Existing mechanical/optical physical method: generate a deterministic
   physical-carrier fixture, run folded indexed transport with A/B staging,
   hidden/view gates, play/pause/step/seek/reverse, and verify alignment and
   unverified-staging faults fail closed.

## Outputs

The output directory contains:

- `00_device_interface_conformance/`: the existing universal fixture,
  provider, profile, and software-control contract run;
- `01_device_profiles/`: profile validation report;
- `02_pc_to_printer/`: carrier artifact and printer contract;
- `03_reader_to_pc/`: capture files and reader contract;
- `04_reader_to_printer/`: attested reprint artifact and relay contract;
- `05_virtual_reader_and_player/`: virtual scan-gate, playback, A/B timeline,
  and fault-probe evidence;
- `06_pc_to_player/`: loopback player transcript;
- `07_action_level_device_channels/`: PC-to-reader command/response
  transcript and invalid-command fail-closed evidence;
- `08_mechanical_optical_player/`: generated carrier fixture, physical-method
  timeline, player validation, and alignment/staging fault probes;
- `universal_hardware_simulation_report.json`: final machine-readable result;
- `universal_hardware_simulation_feedback.json`: display/transition feedback;
- `UNIVERSAL_HARDWARE_SIMULATION_SUMMARY.md`: short human-readable summary.


## Safety and claim boundary

The final report must keep these values false:

- `hardware_connected`;
- `real_driver_or_protocol_used`;
- `physical_transition_authorized`;
- `physical_level_5_claimed`;
- `manufactured_player_claimed`.

The fault probe corrupts or removes required information and checks that the
reader/player path rejects it rather than continuing with an unsafe accept.
The existing physical-method simulator is now part of this run; it remains a
software model only. The later hardware-specific provider layer must preserve
these contracts.
