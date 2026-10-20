# AMCF Windows bundle

The release bundle contains these entry points:

- `amcf.exe`: the normative console CLI, suitable for scripts and repeatable runs.
- `RUN_AMCF_GUI.cmd`: a one-click launcher for the workflow window.
- `amcf_gui/amcf_gui.exe`: the GUI executable and its onedir runtime files.

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

