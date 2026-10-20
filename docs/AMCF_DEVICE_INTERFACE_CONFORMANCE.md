# AMCF Universal Device Interface Conformance

## Purpose

`device-conformance` runs the complete software-only corridor contract in one
report. It combines the maintained fixture, adapter, provider-runtime,
software-control, provider-discovery, and profile-validation paths.

The normalized corridors are:

- `pc_to_printer`: carrier output and print/export handoff;
- `reader_to_pc`: reader/scanner capture and recovery;
- `pc_to_player`: player control, staging, verification, and event timing.

The phrase `reader_to_printer` is not used as a separate AMCF corridor: reader
recovery returns to the PC, and the PC then owns any later carrier output.

## Run

```text
amcf device-conformance --project-root . --output output/device_conformance
```

The run writes one report containing:

- shared manifest and timestamped update-event checks;
- legacy fixture and adapter results;
- provider-neutral hardware runtime results;
- versioned software-control results;
- concrete file/folder/loopback provider results;
- profile-selected provider results;
- ordered fail-closed and unsafe-acceptance checks;
- generic transport/profile templates.

The editable template is
`profiles/amcf_universal_device_interface.template.json`. It is guidance only,
not a directly executable hardware profile. A completed profile must be
converted to the validated `amcf-device-profile-bundle-v1` schema.

## Boundary

The default conformance run does not open hardware, authorize a physical
transition, claim a real driver, or claim physical Level 5. It proves that a
future printer, reader/scanner, or player provider can map onto the shared
AMCF manifest, event schedule, hash, status, and fail-closed contract without
changing the AMCF archive format.

Actual WIA/TWAIN, printer, USB, serial, network, or player-specific binding is
added only after a device profile and transport contract are selected.
