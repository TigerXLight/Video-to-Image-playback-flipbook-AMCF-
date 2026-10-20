# AMCF Software Control Protocol

## Purpose

This layer defines the versioned software session that future printer,
reader/scanner, and player providers must implement. It is deliberately
hardware-neutral: the current run uses the maintained deterministic fixtures
and simulated providers only.

The protocol sits above a provider and below the AMCF workflow:

```text
AMCF package / physical manifest
        -> capability negotiation
        -> ordered command envelopes
        -> provider operation
        -> ordered response/status transcript
```

It does not redefine digital AMCF, component events, or the physical-player
design. It transports the existing package, update-event, section, timing,
verification, and fail-closed decisions between software layers.

## Contract

Protocol version: `amcf-software-control-protocol-v1`

Every command contains:

- session ID;
- monotonically increasing sequence number;
- command ID;
- corridor (`pc_to_printer`, `reader_to_pc`, `pc_to_player`, or `shared_core`);
- command name;
- structured payload.

The session first negotiates the protocol version and required capabilities.
Sequence gaps, replayed commands, unknown commands, malformed payloads, and
capability mismatches are rejected fail-closed.

The current command set covers:

- carrier submission with manifest-hash acknowledgement;
- reader section capture and rescan feedback;
- player manifest loading;
- hidden-gate prefetch;
- staged-section hash verification;
- verified visible-state switching;
- local verified-buffer seek and reverse;
- safe stop;
- clean session close.

## Safety rules

The protocol keeps these decisions separate:

- software command accepted;
- physical display allowed;
- physical transition allowed;
- retry or rescan allowed;
- fail-closed;
- unsafe acceptance.

The software-only runtime always reports physical display and transition as
disabled. A visible switch without a verified staged section is rejected, and
an out-of-order command closes the affected session. Neither is counted as an
unsafe acceptance.

## Command

From the repository root:

    python src/amcf_cli.py software-control --project-root . --output output/software_control_protocol

The installed console command is:

    amcf software-control --project-root . --output output/software_control_protocol

The run writes:

- `software_control_protocol_report.json`;
- `software_control_capabilities.json`;
- `software_control_command_transcript.json`;
- `software_control_feedback.json`;
- `SOFTWARE_CONTROL_PROTOCOL_SUMMARY.md`.

## Future providers

A real provider should map its transport to these envelopes and responses,
then implement the existing provider interfaces. Candidate transports remain
device-specific and unselected: Windows print-to-file or Print Spooler, WIA
or TWAIN/OpenCV capture, and USB or serial player control.

No provider may turn a command acknowledgement into a hardware-validation
claim. Device discovery, transport errors, registration/hash feedback, gate
state, timing feedback, and stop/recovery events must remain visible in the
same transcript and preserve the same fail-closed decisions.

## Boundary

A passing protocol run proves an executable software command/session contract.
It does not prove a real printer, reader, scanner, USB/serial endpoint,
firmware, motor, sensor, carrier, or manufactured physical player.
