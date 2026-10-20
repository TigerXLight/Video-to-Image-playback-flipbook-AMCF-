# AMCF Device System

This layer implements the software paths that sit between a digital AMCF
package and a future physical carrier, reader, or player. It is deliberately
provider-neutral: the deterministic provider is complete and testable now,
while Windows and device providers are optional adapters.

## End-to-end command

Start with a generated physical carrier package:

```text
amcf print-plan --input <archive.amcf.zip> --output <carrier-package>
amcf carrier-payload --input-archive <archive.amcf.zip> --output <payload-output>
amcf device-system --carrier-package <carrier-package> --output <system-output>
```

The system run performs:

1. Carrier rendering to SVG, PNG, and PDF.
2. Printer preflight, job creation, spool copy, completion status, and retry/cancel state handling.
3. Pixel-based reader recovery from the rendered images.
4. Registration-marker, lane-presence, and colour-registry checks.
5. Reconstruction of a recovered physical AMCF package with scan evidence.
6. Exact native AMCF archive payload framing into printable binary pages, image recovery, archive hash verification, corruption rejection, and direct AMCF reader decode when the source archive is available.
7. Persistent device configuration and calibration profile creation.
8. Player handshake, manifest loading, section staging, verification, switching, status, seek, reverse, motor, shutter, illumination, stop, and cancel commands.
9. Provider discovery for Windows printers, WIA/TWAIN readers, serial players, HID devices, and simulation devices.

The output contains `device_system_report.json`, `carrier_render/`,
`spool/`, `reader_recovery/`, `device_config.json`, and
`calibration_profile.json`.

## Provider boundary

The default run is a software simulation and is not a claim that a physical
printer, scanner, carrier, or player has been validated. Optional providers
are available for:

- Windows Print Spooler submission and job status/cancellation.
- WIA image acquisition.
- TWAIN image acquisition.
- Serial JSON-line player control.
- HID discovery for future player transports.

The player command also accepts `--player-backend serial --player-port COM5`
or `--player-backend hid --player-device <hid-path>`. These transports use a
versioned JSON protocol envelope, but the firmware-specific electrical and
report layout still belongs in the selected device profile.

Providers fail closed when their operating system, package, device, or
profile is unavailable. A successful simulation therefore proves the protocol
and action sequencing, not physical print accuracy, scan tolerance, firmware
compatibility, or manufacturing readiness.

## Native payload and reader recovery

The control carrier contains indexed lanes, markers, calibration swatches,
hashes, and metadata. The separate native payload carrier encodes the actual
AMCF archive bytes into framed binary page modules. Each page carries a magic,
sequence number, total size, archive hash, and CRC. Recovery is source-free:
the page images are decoded, concatenated, hash-checked, and opened by the
normal AMCF reader. The corruption probe must reject a damaged page.

The native payload command does not embed the source MP4 and does not use a
complete-video fallback. `native_component_payload_embedded` refers to the
actual AMCF archive bytes, including its component/event payloads, not merely
the control manifest.

The current result is still a software/rendered-carrier proof. It does not
claim that a physical printer or scanner preserves module geometry, colour,
registration, or page transport without measured calibration.

## Calibration and persistence

`device_config.json` records the selected provider names and device handles.
`calibration_profile.json` records printer, reader, and player calibration
parameters. The baseline profile is explicitly marked software-only; a real
calibration session can replace it without changing the protocol schema.

## Validation

The focused tests are in `tests/test_amcf_device_system.py` and
`tests/test_amcf_carrier_payload.py`. The test suite checks successful
end-to-end simulation, exact native archive recovery and direct decode,
corruption rejection, pixel-level registration failure, device discovery,
retry, and cancellation. Every report carries
`unsafe_acceptance_count: 0` and an explicit physical-hardware claim boundary.
