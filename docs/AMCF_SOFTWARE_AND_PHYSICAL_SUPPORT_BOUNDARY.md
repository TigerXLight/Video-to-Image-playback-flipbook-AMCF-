# AMCF Software And Physical Support Boundary

AMCF core is software-first. Digital AMCF is the canonical AMCF representation, scheduler, and validation model. The AMCF digital runtime, validation path, and playback/reconstruction process are canonical.

Physical AMCF is the material embodiment of the same AMCF timing/update structure. It is not a separate unrelated invention and does not replace AMCF logic. A future physical player would physically/optically execute the AMCF schedule that is defined, tested, and validated digitally.

Physical manufacture is later optional work. The physical carrier/reader/player branch is represented now by simulation, virtual hardware, documentation, and adapter concepts.

## Physical reader branch

The physical reader branch is scan/recovery oriented. A future physical reader or scanner would read AMCF physical media lanes, validate timing/index, registration, colour, metadata, hash/checksum, and related recovery data, then reconstruct or export AMCF digital state if needed.

## Physical player branch

The physical player branch is mechanical/optical, not a digital-screen dependency. A future AMCF Mechanical / Optical Physical Player would move indexed AMCF physical media through a fixed view gate and use illumination, optical viewing, projection, or a viewing window for direct human viewing without requiring a digital display for the playback act.

## Shared media and transport

Physical reader and physical player designs may share cartridges, media, transport, alignment, and controls, but they have different roles:

- reader/scanner: recovery, diagnostics, validation, optional export back into digital AMCF
- physical player: direct mechanical/optical viewing according to the digital AMCF dynamic update schedule
- hybrid reader-player appliance: shared transport with both roles kept distinct

The intended physical-medium language is vertical-stack / indexed section physical-medium concept, not left-to-right flipbook-first.

No physical proof, physical Level 5, hardware validation, manufacturing readiness, final UI, or built prototype is claimed by this package.
