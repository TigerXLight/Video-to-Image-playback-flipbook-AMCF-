# AMCF Windows bundle

The release bundle contains two entry points:

- `amcf.exe`: the normative console CLI, suitable for scripts and repeatable runs.
- `amcf_gui.exe`: a small workflow window for source-video encoding, archive decoding, seeded-profile validation, and virtual print-plan preparation.

The GUI is a software workflow front end. It does not claim a real printer,
scanner, reader, physical player, hardware validation, or a manufactured device.

The seeded 4K profile is source-seeded: it embeds a compressed 4K seed and
materializes the retained AMCF event graph through component masks. It does not
contain independently stored native 4K component pixels. The strict native
component archive remains a separate profile.

For deep SAM2/SAMURAI/CoTracker/HOOT workflows, run the repository setup command
with the explicit licence/terms flags. Those external runtimes and checkpoints
are intentionally not bundled into this ZIP.

