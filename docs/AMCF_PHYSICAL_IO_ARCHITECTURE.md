# AMCF Physical I/O Architecture

Stage 1 defines the shared Physical I/O Architecture foundation for AMCF.

Digital AMCF is the canonical AMCF representation, scheduler, compositor, and validation model. Physical AMCF is the material embodiment, execution, and recovery branch of the same AMCF schedule and section logic.

```text
DIGITAL AMCF
-> AMCF PHYSICAL MANIFEST
-> shared physical carrier object
-> PC -> Printer output path
-> Reader -> PC recovery path
-> Player <-> PC control/recognition path
```

## Shared Manifest

All physical I/O paths refer back to one `AMCFPhysicalManifest`.

- Printer path writes or exports the physical carrier package.
- Reader path recovers or verifies the physical carrier package back into digital AMCF.
- Player path executes the physical carrier package physically/optically.

The shared rule is that all three paths refer back to the same digital AMCF schedule, section ordering, lane schema, and validation model.

## Primary Carrier

The primary carrier model is the AMCF Indexed Thin-Section Carrier:

- discrete or indexed thin page/section-like carrier units
- visual payload plus timing/index, registration, colour registry, metadata, and checksum/hash lanes
- continuous ribbon/film-track is comparison/reference only, not the default
- left-to-right hand flipbook is rejected as the default
- manual crank is slow scan/recovery only, not primary high-speed playback

## Three Paths

### Computer To Printer

The printer path creates or exports physical AMCF carrier packages. Stage 1 only defines requirements and simulated profiles. It does not implement PDF/SVG/PNG package generation, real printer drivers, print calibration, or print accuracy validation.

### Reader To PC

The reader path recovers or verifies physical AMCF back into digital AMCF. Stage 1 only defines requirements and simulated profiles. It does not implement scanner acquisition, WIA/TWAIN/SANE integration, real marker decoding, or real scanner validation.

### Player To PC

The player path recognizes, controls, or supports a future physical/optical AMCF player. The preferred physical-player direction is a compact tablet-like physical/optical player with a folded internal indexed-media path, dynamic A/B staged view-gate transport, side/top cartridge slot, physical/optical front viewing window, and embedded electronics for control, audio sync, motor/index timing, diagnostics, and safety.

Digital electronics are allowed for motor/index control, audio sync, schedule execution, calibration, diagnostics, device recognition, and fail-closed safety. Digital electronics must not replace the physical/optical visible image path in the physical-player concept.

## Staged Adapter Approach

Stage 1 is the shared manifest and data model only. Later adapters can map the same manifest to OS printer paths, reader/scanner acquisition paths, or player control paths.

Future adapter candidates:

- IPP/OS printer adapter
- WIA/TWAIN/SANE/custom reader adapter
- USB CDC/HID/WinUSB/libusb player adapter

## Claim Boundary

This physical I/O module is a software architecture and simulation foundation. It does not claim manufactured hardware, real print accuracy, real scanner validation, real physical playback proof, or real device-driver integration.
