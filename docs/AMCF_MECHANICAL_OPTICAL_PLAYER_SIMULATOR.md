# AMCF Mechanical / Optical Player Simulator

The mechanical/optical player simulator is a software model of a future physical playback path:

`AMCF physical media -> indexed physical transport -> fixed physical view gate -> illumination / optical presentation -> direct human viewing`

## What it models

- Indexed AMCF carrier sections.
- A fixed physical view gate.
- Illumination and visibility state.
- Section alignment at the view gate.
- Playback timeline generation.
- Controls: play, pause, step forward, step backward, seek, and reverse.
- Fail-closed rejection for missing, tampered, malformed, out-of-order, or misaligned carrier sections.

## How it differs from the software UI viewer

The AMCF Player UI viewer is a software inspection surface for playback state. The mechanical/optical player simulator models a future physical viewing path and should not be read as a normal monitor/tablet playback concept.

## How it differs from reader/recovery

The virtual reader/recovery path reconstructs AMCF state from carrier sections. The mechanical/optical player simulator models direct physical presentation through a view gate. A future appliance could combine both roles, but they remain distinct.

## Claim boundaries

- No physical proof is claimed.
- No hardware validation is claimed.
- No manufactured prototype is claimed.
- No final UI is claimed.
- No digital-screen physical-player definition is claimed.
- No real optical bench or mechanical transport is used.
