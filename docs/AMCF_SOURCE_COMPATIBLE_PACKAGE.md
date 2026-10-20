# AMCF Source-Compatible Package

The source-compatible package is a compact playback representation for a
source video that has already been accepted by the AMCF component-event path.
It stores:

- the source video payload for exact decoded playback;
- the AMCF event and diagnostic metadata;
- binary frame, event-payload, and base-payload integrity tables;
- explicit claim-boundary metadata.

It does **not** pretend that the source video is a native component payload.
The package manifest identifies this mode as
`source_video_reference_with_component_event_metadata` and records that native
component payloads are externalized.

## Native materialization

`materialize_native_archive()` extracts the source payload through FFmpeg,
rebuilds the source-frame manifest, invokes the existing native component-event
builder, and verifies the regenerated base/event payload hashes against the
package integrity tables. This keeps the full native archive path available
without placing the much larger native WebP payload set in the compact package.

Example:

```text
python demo/run_amcf_source_compatible_package_demo.py \
  --source-video path/to/source.mp4 \
  --canonical-archive path/to/component_event_archive.amcf.zip \
  --output output/amcf_source_compatible_package \
  --materialize-native
```

The mode is software-only. It does not claim hardware validation, physical
Level 5 completion, or a manufactured player. `unsafe_acceptance_count` must
remain zero.
