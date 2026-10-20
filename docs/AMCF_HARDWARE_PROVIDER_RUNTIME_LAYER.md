# AMCF Hardware Provider Runtime Layer

## Purpose

This layer gives future device-specific drivers a stable provider API. The
current implementations are deterministic software providers only. They
exercise the same handshake a real provider must implement without opening a
printer, scanner, camera, USB endpoint, serial endpoint, firmware, motor,
sensor, or physical player.

The provider API is divided into three roles:

- PrinterCarrierProvider: submit a validated carrier artifact and receive job
  identity and hash acknowledgement.
- ReaderCaptureProvider: capture a section, return registration, colour, and
  hash feedback, and request a rescan when required.
- PlayerControlProvider: load the AMCF manifest, prefetch into the hidden
  staging gate, verify the section, and update the virtual visible-gate state.

Future Windows providers can implement these interfaces for Print Spooler,
WIA/TWAIN, OpenCV capture, USB, serial, or another explicitly selected
transport. The AMCF event schedule and physical-player safety rules remain
authoritative.

## Safety behaviour

Every provider response carries explicit acceptance and fail-closed fields.
The runtime keeps physical display and transition permissions disabled. The
player provider must verify a staged section before a visible-gate switch. The
runtime includes a negative safety probe proving that an unverified switch is
blocked.

The virtual provider runtime does not convert a software acknowledgement into
a physical claim. It reports:

- hardware_connected: false
- real_driver_or_protocol_used: false
- direct_hardware_transition_authorized: false
- unsafe_acceptance_count: 0

## Command

From the repository root:

    python src/amcf_cli.py hardware-providers --project-root . --output output/hardware_provider_runtime

The installed console command is:

    amcf hardware-providers --project-root . --output output/hardware_provider_runtime

The newer `device-providers` command sits above this provider-neutral runtime
and selects concrete file/folder/loopback adapters or explicitly enabled
Windows transport hooks without changing the status contract.

The command writes:

- hardware_provider_runtime_report.json
- hardware_provider_capabilities.json
- hardware_provider_status_events.json
- hardware_provider_feedback.json
- hardware_provider_command_transcript.json
- HARDWARE_PROVIDER_RUNTIME_SUMMARY.md

## Boundary

A passing run proves that the provider-neutral interfaces and software
handshake are executable against the maintained fixture. It does not prove
printer accuracy, scanner accuracy, physical carrier recovery, USB or serial
communication, firmware behaviour, motor timing, or physical optical
playback.

The next hardware step is to implement one selected real provider behind one
of these interfaces, beginning with device discovery and acknowledgement
feedback while retaining the same claim boundary.
