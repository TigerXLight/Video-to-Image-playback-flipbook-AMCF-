# AMCF Test 14H Bounded Archive Decoder

`src/amcf_v2_14h_archive.py` reads local Test 14H `.amcfnative.zip` archives without modifying them. It supports WebP keyframes, WebP region patches, and `motion_xor_zlib` residual patches. The reader checks the 14H manifest, ordered decode plan, frame dependencies, payload sizes and hashes, dimensions, and every reconstructed RGB frame hash before reporting success. Unsupported or inconsistent inputs fail closed.

The local Test 14H decision was `COMPONENT_METADATA_USEFUL_BUT_NOT_COMPRESSION_WIN`. This public port preserves a **bounded format/decode ability**, not a claim of a general compression improvement, semantic object tracking, final native playback engine, hardware validation, physical Level 5, or a manufactured player. Pillow is optional in the repo but required when invoking this WebP decoder; no new dependency is installed by this work.

Run against a Test 14H archive:

```text
python demo/run_amcf_v2_14h_archive_demo.py path/to/14h_archive.amcfnative.zip
```

The demo writes only a compact report under ignored `output/amcf_v2_14h_archive_decode/`. Unit tests generate tiny synthetic archives for both payload types and malformed-input rejection. Local 48/96-frame archives provide additional comparison evidence but are not committed as fixtures.

Validation against the 16 available local Test 14H variant archives passed: each reconstructed 48- or 96-frame sequence matched every recorded RGB checksum. This verifies bounded archive reading for those samples, not general encoding, compression superiority, or production playback. The public module can optionally retain decoded RGB frames for callers; the demo writes a report only.

This is one closed code gap from the file-level comparison. The broader `Tests` inventory and accepted-feature parity review remain open.
