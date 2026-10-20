# AMCF Windows bundle

The release bundle contains these entry points:

- `amcf.exe`: the normative console CLI, suitable for scripts and repeatable runs.
- `RUN_AMCF_GUI.cmd`: a one-click launcher for the workflow window.
- `amcf_gui/amcf_gui.exe`: the GUI executable and its onedir runtime files.
- `INSTALL_AMCF.cmd`: per-user installer with Start Menu/Desktop shortcuts.
- `UNINSTALL_AMCF.cmd`: removes the per-user installation and shortcuts.

The ZIP is portable. To install it, extract the bundle and run
`INSTALL_AMCF.cmd`. The installer does not require administrator rights and
defaults to `%LOCALAPPDATA%\AMCF`; use `install_amcf.ps1 -InstallDir ...`
for a different location.

The GUI is a software workflow front end. It does not claim a real printer,
scanner, reader, physical player, hardware validation, or a manufactured device.

The seeded 4K profile is source-seeded: it embeds a compressed 4K seed and
materializes the retained AMCF event graph through component masks. It does not
contain independently stored native 4K component pixels. The strict native
component archive remains a separate profile.

For deep SAM2/SAMURAI/CoTracker/HOOT workflows, run the repository setup command
with the explicit licence/terms flags. Those external runtimes and checkpoints
are intentionally not bundled into this ZIP.

The GUI's physical-adapter action runs the shared deterministic software
contract: PC-to-printer/carrier preparation, reader/scanner-to-PC recovery,
player-to-PC status/control, and the shared fail-closed validator. It is not
hardware validation. The extracted bundle includes the fixture JSON files
required for that action.

The complete physical software layer is available through the CLI:

```text
amcf carrier-render --carrier-root <carrier-package> --output <render-output>
amcf carrier-payload --input-archive <archive.amcf.zip> --output <payload-output>
amcf device-system --carrier-package <carrier-package> --output <system-output>
amcf device-discover --output <system-output>\device_discovery.json
```

`device-system` exercises printable SVG/PNG/PDF generation, a persistent
printer job and spool lifecycle, pixel-based registration/lane/colour recovery,
reader-to-package reconstruction, exact native AMCF payload recovery and
direct archive decode, persistent calibration/configuration, and a
player protocol session with handshake, sensors, motor, shutter, illumination,
seek, reverse, stop, retry, and cancellation. Its default providers are
deterministic and do not claim real hardware.

Optional Windows/device providers are listed in `requirements-device.txt`.
Install them only when the corresponding device is present and configured:
`pywin32` for Windows print/WIA access, `pyserial` for serial players, and
`twain` or `hidapi` for matching reader/player hardware. The runtime remains
fail-closed when a provider or device is unavailable.

