# AMCF Windows bundle

The release bundle contains two entry points:

- `amcf.exe`: the normative console CLI, suitable for scripts and repeatable runs.
- `amcf_gui.exe`: a workflow window for source-video encoding, archive decoding, seeded-profile validation, the maintained diagnostics, dependency setup, and the virtual physical-adapter check.

The GUI is a software workflow front end. It does not claim a real printer,
scanner, reader, physical player, hardware validation, or a manufactured device.

The seeded 4K profile is source-seeded: it embeds a compressed 4K seed and
materializes the retained AMCF event graph through component masks. It does not
contain independently stored native 4K component pixels. The strict native
component archive remains a separate profile.

For deep SAM2/SAMURAI/CoTracker/HOOT workflows, run the repository setup command
with the explicit licence/terms flags. Those external runtimes and checkpoints
are intentionally not bundled into this ZIP.

The GUI's physical-adapter action runs the same deterministic software fixture
as `amcf physical-roundtrip`: PC-to-printer/carrier preparation, reader/scanner-
to-PC recovery, and player-to-PC status/control. It is not hardware validation.
The extracted bundle includes the fixture JSON files required for that action.

