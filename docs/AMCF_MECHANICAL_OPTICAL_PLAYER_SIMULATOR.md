# AMCF Mechanical / Optical Player Simulator

The mechanical/optical player simulator is a software model of a future physical playback path:

`AMCF physical media -> folded indexed transport -> A/B staging gates -> fixed physical view gate -> shuttered illumination / optical presentation -> direct human viewing`

## What it models

- Indexed AMCF carrier sections.
- A dynamic AMCF update schedule rather than fixed-FPS page playback.
- A compact folded-path A/B staged transport model.
- A current visible view gate and hidden next-section staging gate.
- A preload queue and reader/prefetch timing.
- Transition blanking through shutter/illumination timing.
- A fixed physical view gate.
- Illumination and visibility state.
- Section alignment at the view gate.
- Playback timeline generation.
- Controls: play, pause, step forward, step backward, seek, and reverse.
- Fail-closed rejection for missing, tampered, malformed, out-of-order, misaligned, or unverified next-staged carrier sections.

## How it differs from the software UI viewer

The AMCF Player UI viewer is a software inspection surface for playback state. The mechanical/optical player simulator models a future physical viewing path and should not be read as a normal monitor, LCD/OLED tablet, or digital-screen playback concept. Digital electronics may control motors, timing, calibration, audio sync, and error handling; the visible playback act remains physical/optical.

## How it differs from reader/recovery

The virtual reader/recovery path reconstructs AMCF state from carrier sections. The mechanical/optical player simulator models direct physical presentation through a view gate. A future appliance could combine both roles, but they remain distinct.

## Claim boundaries

- No physical proof is claimed.
- No hardware validation is claimed.
- No manufactured prototype is claimed.
- No final UI is claimed.
- No digital-screen physical-player definition is claimed.
- No real optical bench or mechanical transport is used.
