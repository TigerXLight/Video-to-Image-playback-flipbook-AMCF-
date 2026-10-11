# AMCF Physical I/O Claim Boundaries

Stage 1 proves that AMCF has a shared software architecture foundation for physical I/O paths. It defines deterministic data models, simulated device profiles, validation rules, and demo output for a shared `AMCFPhysicalManifest`.

## What Stage 1 Proves

- Digital AMCF can reference a shared physical manifest.
- Printer, reader, and player paths can share the same carrier object and section schedule.
- Required physical lanes can be represented and validated.
- Simulated device profiles can describe future printer, reader, and player responsibilities.
- Claim boundaries can be attached directly to manifests, material profiles, device profiles, and reports.

## What Stage 1 Does Not Prove

- No manufactured hardware is claimed.
- No real printer or real print accuracy is claimed.
- No real reader/scanner or real scanner validation is claimed.
- No real physical player is claimed.
- No real physical playback proof is claimed.
- No real device-driver integration is claimed.
- No final UI is claimed.

## Physical Player Boundary

The future physical player is a physical/optical path. It may use digital electronics for motor/index control, audio sync, schedule execution, calibration, diagnostics, recognition, and fail-closed safety. Those electronics must not redefine the physical player as normal LCD/OLED screen playback.

The visible AMCF image path remains physical/optical in the physical-player concept.

## Compression Boundary

CompressorJS and UPNG.js are optional reference tools only. They are not bundled dependencies and are not required by Stage 1.

Canonical scan/recovery images should remain original/lossless until marker/hash/colour decoding is complete. Lossy compression before marker/hash/colour decoding is disabled by default.
