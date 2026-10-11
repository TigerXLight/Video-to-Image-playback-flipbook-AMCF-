# AMCF Physical I/O Development Sequence

## Stage 1

`AMCF_PHYSICAL_IO_ARCHITECTURE_V1`

Shared manifest/data model only.

Creates:

- `AMCFPhysicalManifest`
- indexed thin-section carrier model
- shared lane schema
- material profile model
- simulated printer, reader, and player profiles
- claim boundaries
- deterministic architecture demo

## Stage 2

`AMCF_PRINTER_OUTPUT_PACKAGE_V1`

Physical carrier output package generator.

This stage may create the full printer/export package path from the shared manifest. It should still avoid claiming real print accuracy until measured physical testing exists.

## Stage 3

`AMCF_READER_PC_RECOGNITION_AND_RECOVERY_V1`

Reader recovery/recognition simulator.

This stage may simulate reader-to-PC recognition, marker decoding, lane checks, and recovery into digital AMCF.

## Stage 4

`AMCF_PLAYER_PC_RECOGNITION_AND_CONTROL_V1`

Player recognition/control/safety simulator.

This stage may simulate recognition and PC-side control of a future physical/optical player, including schedule execution, motor/index control, diagnostics, audio sync, and fail-closed policy.

## Stage 5

`AMCF_PHYSICAL_IO_END_TO_END_DEMO_V1`

Unified printer -> reader -> player simulation.

This stage may connect the printer/export, reader/recovery, and player/control simulations through the shared `AMCFPhysicalManifest`.

## Future Adapters

- IPP/OS printer adapter
- WIA/TWAIN/SANE/custom reader adapter
- USB CDC/HID/WinUSB/libusb player adapter

Future adapters must keep claim boundaries explicit until real hardware validation exists.
