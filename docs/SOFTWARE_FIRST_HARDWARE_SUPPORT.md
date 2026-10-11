# Software-First Hardware Support

AMCF is software-first. Hardware support exists here as software abstractions:

- virtual cartridge
- virtual reader
- virtual scan gate
- lane validation
- player handoff state
- playback device abstraction
- `SoftwarePlaybackDevice`
- `FuturePhysicalReaderAdapter` placeholder
- `FuturePhysicalPlaybackDevice` placeholder
- `ReaderPlayerApplianceAdapter` placeholder

The virtual reader/player abstractions are hooks for future physical reader, reader-player appliance, and mechanical/optical physical playback-device work. They do not require real hardware and do not implement real physical playback.

The future physical player should be understood as an AMCF Mechanical / Optical Physical Player: a device that presents physical AMCF media through controlled transport, a view gate, and illumination/optical presentation, without requiring a digital screen for the playback act.

No real hardware is required. No physical proof or hardware validation is claimed.
