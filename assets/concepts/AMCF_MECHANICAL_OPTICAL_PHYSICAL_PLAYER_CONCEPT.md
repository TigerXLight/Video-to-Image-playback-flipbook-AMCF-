# AMCF Mechanical / Optical Physical Player Concept

This is the current physical-player concept reference for AMCF public repository context.

This richer concept follows the AMCF physical-plan direction more closely than the earlier simple flow diagram. It shows the indexed thin-page / section carrier, compact folded-path transport, A/B visible/hidden staging gates, section selector/feed stage, fixed scan/view gate, shutter/dwell timing, AMCF section lane structure, controlled-drive candidate families, sensor feedback / index lock, energy/recovery layers, optical viewing path, and secondary reader/recovery lane.

The physical player means:

AMCF physical media -> folded indexed section transport -> A/B staging gates -> fixed physical view/playback gate -> shuttered illumination / optical viewing path -> direct human viewing.

The player is intended to be dynamic. It should not move one physical section for every fixed video frame. It should follow the AMCF update schedule, keep the current section locked at the visible gate, preload and verify the next required section in a hidden staging gate, blank the optical path during transition, and switch sections at the update timestamp.

It is not:

- a normal digital monitor, tablet, or screen player
- the AMCF software UI viewer
- the physical reader/scanner path
- left-to-right flipbook playback as the default
- continuous film/ribbon playback as the default
- fixed-FPS physical page playback
- a long straight roller-path machine as the preferred form
- physical proof, hardware validation, final UI, CAD, or manufacturing-ready design

The optional reader/recovery lane is secondary and exists for validation, diagnostics, recovery, or export. The physical viewing act remains mechanical/optical in this concept.

Mechanism candidate families shown:

- motor/encoder feed as the strongest controlled baseline
- piezo/electrostatic inchworm as the strongest indexed-feed research candidate
- constant-force / spring + governor as a self-contained mechanical candidate
- electret, triboelectric, piezo charge recovery, capacitive recovery, and regenerative braking as recovery/buffering layers only
- pause, latch/brake, reverse, seek/index, sensor feedback, and index lock as control concepts
- three-pass folded path: input/preload, active view-gate, and return/park/reverse
- two-track A/B shuttle: one visible or ready-to-visible track and one hidden preload/staging track

The diagram still does not decide the final real-world mechanism. It is a public context asset for the current research direction.
