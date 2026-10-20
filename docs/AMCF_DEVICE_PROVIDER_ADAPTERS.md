# AMCF Device Provider Adapters

## Purpose

This layer maps the versioned AMCF software-control protocol onto selectable
printer/carrier, reader/scanner, and player transports. The protocol and
fail-closed status contract remain stable when a transport changes.

The default run is fully software-only:

- `file` printer/carrier provider writes a hash-checked carrier artifact;
- `folder` reader provider resolves captured sections and returns registration,
  colour, and hash feedback;
- `loopback` player provider exercises manifest loading, hidden prefetch,
  verification, and visible-state gating in memory.

These providers are concrete and runnable, but they do not claim that a
physical printer, scanner, reader, motor, or player has been operated.

## Discovery Command

From the repository root:

```text
python src/amcf_cli.py device-providers --project-root . --output output/device_provider_discovery
```

The installed console command is:

```text
amcf device-providers --project-root . --output output/device_provider_discovery
```

The run writes a provider report, capability descriptors, probe results,
feedback, and a software carrier artifact. A passing default run has
`hardware_connected: false`, `unsafe_acceptance_count: 0`, and all physical
transition permissions disabled.

## Optional Windows Transports

The adapter module also contains explicit opt-in transport hooks:

- `windows-spooler`: raw Windows Print Spooler submission through `win32print`;
- `windows-wia`: Windows Image Acquisition discovery through `win32com`;
- `serial`: JSON-line player control through `pyserial`.

Example selection command:

```text
amcf device-providers --project-root . --output output/device_provider_probe --printer-backend windows-spooler --reader-backend windows-wia --player-backend serial --printer-name "Printer Name" --reader-device "Scanner Name" --player-port COM5 --enable-hardware
```

The `--enable-hardware` flag is required. Missing dependencies, missing device
profiles, failed probes, malformed replies, and hash mismatches remain rejected
and fail closed. The command does not infer a printer, scanner, or player model.

The WIA adapter currently provides device discovery and the safe capture gate;
device-specific image-transfer/profile binding is intentionally still required
before real scanning can be claimed. The serial adapter requires a player that
implements the documented JSON-line command/response contract. The spooler
adapter requires a hash-checked print artifact path in the submitted manifest.

## Contract Boundary

The adapters preserve:

- ordered provider status and feedback;
- manifest, section, event, and payload hash gates;
- hidden staging before visible switching;
- rescan/retry feedback for reader failures;
- no direct physical transition authorization;
- no physical Level 5 or manufactured-player claim.

This layer is ready for device-specific providers once the actual printer,
carrier, reader/scanner, and player interfaces are selected and profiled.
