# AMCF Canonical Concept

AMCF means Adaptive Multi-Rate Component Flipbook.

The core idea is not that AMCF must be a literal paper flipbook. The core idea is that video can be represented as image-motion playback: a source video is converted into an AMCF archive made of visual components, component updates, timing, masks, placement, audio, indexes, and reconstruction rules. Playback is then produced by synchronising and compositing those image/component states so the viewer receives the same motion result as the original video.

Digital AMCF is the canonical AMCF representation, scheduler, and validation model. Physical AMCF is the material embodiment of the same AMCF timing/update structure, not a separate unrelated invention. A physical reader path recovers or verifies physical AMCF back into digital AMCF. A physical player path physically/optically presents AMCF media according to the same dynamic update schedule that is defined, tested, and validated digitally.

In simple terms:

```text
source video -> AMCF component/image representation -> AMCF playback -> conventional decoded video if needed
```

The physical flipbook idea is the inspiration and possible future material carrier. The current AMCF proof is digital: it shows that a video can be transformed into AMCF and reconstructed back into playable video with the same intended playback timing and motion behaviour.

## Conventional Video

Conventional video stores one complete scene frame per display moment.

```text
one complete frame = one complete scene
```

At 60 FPS, a conventional video presents 60 complete scene frames per second.

## AMCF

AMCF stores and schedules visual information as components.

```text
multiple component states + timing + compositor = one reconstructed scene
```

Components may include:

- static or slow-changing background regions
- independently moving trees, branches, leaves, water, foam, reflections, people, vehicles, or other objects
- masks or alpha information
- crop/placement coordinates
- timestamps
- component identifiers
- residual or delta updates
- motion or transformation metadata when useful

The component scheduler does not assign every object one permanent FPS. Instead, components receive timestamped updates according to observed behaviour and required reconstruction accuracy.

AMCF distinguishes:

- source FPS: temporal information available from the original video
- component update rate: independent variable frequency of component changes
- reconstruction FPS: the final display rate of reconstructed scenes

The combined component update count may exceed the source frame rate because multiple components can update inside the same source moment. This does not create new source time; it represents the source motion through separately behaving visual information.

## Digital Flipbook Mechanism

AMCF behaves like a digital flipbook of components rather than a sequence of complete pages.

```text
SOURCE VIDEO
  -> VISUAL DECOMPOSITION
  -> COMPONENT UPDATE STREAMS
  -> DYNAMIC COMPONENT SCHEDULER
  -> SYNCHRONISED SCENE COMPOSITOR
  -> RECONSTRUCTED PLAYBACK
```

The compositor maintains the current state of each component, applies scheduled updates, layers the components correctly, and emits reconstructed scenes at the target reconstruction FPS.

## Storage Requirement

Storage efficiency is a project requirement, not an assumption. The AMCF archive should not exceed the original source video's file size unless the run explicitly reports that the size ceiling failed.

The archive budget includes:

- compressed component images
- residual/delta streams
- audio
- component indexes
- masks
- timing metadata
- reconstruction metadata
- validation or checksum data needed for playback

If the size ceiling cannot be met within the selected quality tolerance, the system must report the failure honestly.

## Reconstruction Requirement

AMCF must support decoding back to conventional playable video while preserving:

- original scene timing
- correct component placement
- independent component behaviour
- layer order and transparency
- audio timing
- reconstruction claim boundaries

Exact pixel identity is not guaranteed when lossy compression is used. Quality must be measured, not assumed.

## Current Relationship To Physical Media

Physical construction is a later branch. AMCF is the digital process/view of the same principle: video represented as image/component motion rather than normal monolithic video frames.

A physical AMCF device would be a material carrier, reader, or player for the AMCF sequence. It would not replace the AMCF logic; it would physically execute, recover, or verify the AMCF schedule that remains canonical in digital AMCF. The current preferred physical-player direction is a dynamic folded-path A/B staged indexed-section mechanism for optical presentation, while reader/recovery remains a verification/export path back into digital AMCF.

No real manufactured hardware, hardware validation, or physical proof is claimed here. Physical AMCF remains future material embodiment and testing of the same canonical digital AMCF model.
