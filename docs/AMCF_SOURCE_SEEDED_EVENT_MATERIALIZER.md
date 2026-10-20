# Source-Seeded 4K Event Materializer

This profile is the compact 4K AMCF display profile. It is separate from the
strict native-pixel AMCF archive.

## Contract

The archive contains:

- the canonical AMCF event graph;
- canonical 640x320 masks and their mask-delta stream;
- all 2,592 logical events;
- a compressed 3840x1920 seed payload;
- materialized 4K event hashes and composed-frame hashes;
- an explicit decoder contract.

At decode time the original source MP4 is not needed. The decoder reads the
embedded seed, expands each canonical mask by the declared integer scale, samples
the seed pixels into each event-owned component state, and composites the scene.
Direct playback of the seed is forbidden by the contract and is checked by the
validator.

## What the profile proves

The accepted local checkpoint was:

- archive size: `6,547,011` bytes;
- display: `3840x1920`;
- frames: `288`;
- logical events: `2,592`;
- full scaled-mask coverage;
- event hashes equal after archive reopen;
- frame hashes equal after archive reopen;
- event ablation rejected;
- corrupted seed rejected;
- `unsafe_acceptance_count: 0`.

## What it does not claim

The 4K component pixel values are derived from the embedded seed. Therefore the
profile does **not** contain independently stored native 4K component pixel
payloads. It is source-seeded and compact, not the strict seed-free native-pixel
archive required for an independent physical carrier. The larger strict native
archive remains the authoritative profile for independently recoverable component
pixels, hidden/occluded state, and exact native event payloads.

The seed itself is not an external source video requirement: it is embedded in
the archive. The distinction is about where the 4K component pixels come from,
not whether the decoder needs a separate file.

## CLI

Validate an existing profile:

```text
amcf seeded-materializer --input-archive <profile.amcf.zip> --output <report-dir>
```

Build one from a compressed 4K seed profile plus a canonical event/mask archive:

```text
amcf seeded-materializer --profile-archive <seed-profile.amcf.zip> --canonical-archive <canonical.amcf.zip> --output <output-dir>
```

Add `--render-video` when a component-composited review MP4 is needed. Review
video generation is presentation output; the archive validation is based on the
event and frame hashes, not on the encoded review file.

