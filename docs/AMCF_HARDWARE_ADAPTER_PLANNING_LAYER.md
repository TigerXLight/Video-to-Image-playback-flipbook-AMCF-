# AMCF Hardware Adapter Planning Layer

## Purpose

This layer turns the physical software corridors into concrete Windows-facing
interface plans. It is deliberately offline: it specifies providers, input
contracts, output contracts, feedback, and fail-closed safety rules without
opening a printer, scanner, camera, USB endpoint, serial endpoint, firmware,
motor, sensor, or manufactured player.

The plan preserves the physical-player dossier boundary. The proposed player
is a folded indexed-media path with a visible view gate and a hidden staging
gate. AMCF timestamps and event ordering drive the transport. It is not a
fixed-FPS page machine and it is not an LCD/OLED replacement for the physical
optical image path.

## Planned interfaces

### PC to printer or carrier

The Windows provider is the Print Spooler API or a deterministic print-to-file
provider. The planned contract accepts a validated physical manifest, lane
geometry, timing/index metadata, printer margins, and an artifact hash. It
returns a carrier artifact or spooler job identity, hash feedback, and ordered
print-gate status events.

No print job is submitted by the planning command. A future adapter must not
acknowledge physical output until the selected provider confirms the job and
the artifact identity.

### Reader or scanner to PC

The preferred Windows providers are WIA or TWAIN. OpenCV remains a useful
offline capture fallback for development and test fixtures. The contract
covers device enumeration, capture, registration-marker recovery, colour
registry calibration, section hashes, and rescan feedback.

A section is not considered recovered until registration and hash checks pass.
Missing markers, unreadable lanes, and timing ambiguity remain fail-closed.

### PC to physical player

The planned control endpoint is AMCF Player Control Protocol v1 over USB or
serial. It accepts the validated AMCF manifest, timestamped event schedule,
A/B section index, audio/timing clock, and player safety profile. It returns
acknowledgements, view-gate and staging-gate state, timing feedback, and
fault/recovery events.

The player contract requires prefetch into the hidden staging gate, verification
before a visible-gate switch, blanking or safe stop on faults, and bounded
seek/reverse behaviour. The displayed image remains physical and optical in
the dossier model.

## Command

From the repository root:

    python src/amcf_cli.py hardware-plan --project-root . --output output/hardware_adapter_plan

The installed console command is:

    amcf hardware-plan --project-root . --output output/hardware_adapter_plan

The command first reruns the existing software-only adapter baseline, then
writes:

- hardware_adapter_plan_report.json
- hardware_adapter_interface_specs.json
- hardware_adapter_capability_matrix.json
- hardware_adapter_status_events.json
- hardware_adapter_feedback.json
- HARDWARE_ADAPTER_PLANNING_SUMMARY.md

## Claim boundary

A passing plan means the interfaces and safety contracts are complete on paper
and the existing software baseline passed. It does not mean that a Windows
device was detected, a driver or protocol was used, a carrier was printed, a
scan was captured, or a physical player was operated. Display and physical
transition permissions remain disabled.

The provider-neutral runtime layer now supplies abstract printer, reader, and
player interfaces plus simulated implementations. See
docs/AMCF_HARDWARE_PROVIDER_RUNTIME_LAYER.md. The next implementation step is
to place one selected real device provider behind one interface.
