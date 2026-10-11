# AMCF Physical Manifest Schema

`AMCFPhysicalManifest` is the shared schema that connects digital AMCF to future printer, reader, and player paths.

Digital AMCF remains canonical. The physical manifest describes how the same AMCF schedule and section logic can be embodied, exported, recovered, or physically/optically executed.

## Manifest Fields

- `manifest_id`
- `source_amcf_id`
- `carrier_id`
- `carrier_format_version`
- `carrier_type`
- `section_count`
- `sections`
- `material_profile`
- `lane_schema`
- `printer_requirements`
- `reader_requirements`
- `player_requirements`
- `compression_policy`
- `claim_boundary`

The Stage 1 carrier type is `indexed_thin_section_carrier`.

## Section Fields

Each `AMCFPhysicalSection` describes one indexed thin-section carrier unit:

- `section_id`
- `section_index`
- `timestamp_start_ms`
- `timestamp_end_ms`
- `dwell_ms`
- `layout_mm`
- `lanes`
- `payload_ref`
- `payload_hash`
- `metadata_ref`
- `required_for_playback`
- `recovery_policy`

The timestamps and dwell values connect the physical section back to the digital AMCF dynamic update schedule.

## Lane Schema

Required lanes:

- `timing_lane`
- `index_lane`
- `registration_lane`
- `image_payload_lane`
- `colour_registry_lane`
- `metadata_lane`
- `checksum_hash_lane`

Optional/support lane:

- `damage_recovery_lane`

Required lanes must be present before a manifest can be accepted as valid.

## Material Profile

`MaterialProfile` is parameterized in Stage 1. It records reference material properties such as thickness, stiffness proxy, friction proxy, curl risk, humidity sensitivity, marker contrast proxy, colour stability proxy, and scanner reflectance proxy.

Stage 1 material profiles are simulated/parameterized, not measured physical validation.

## Printer Requirements

Printer requirements define the software export path for physical AMCF carrier packages. Stage 1 does not generate a full print package and does not claim real print accuracy.

## Reader Requirements

Reader requirements define the future recovery and verification path from physical AMCF back into digital AMCF. Stage 1 does not perform real scanner acquisition or real scanner validation.

## Player Requirements

Player requirements define the future physical/optical player recognition and control path. The preferred physical-player concept is dynamic A/B staged folded-path physical/optical playback. The visible AMCF image path remains physical/optical, not normal LCD/OLED screen playback.

## Compression Policy

Canonical scan/recovery images should remain original/lossless until marker, hash, and colour decoding is complete.

Compressed previews are allowed after validation.

Lossy compression before marker/hash/colour decoding is disabled by default.

CompressorJS and UPNG.js are listed as optional reference tools only, not dependencies.

## Validation Rules

Validation must fail if:

- required lanes are missing
- `section_count` does not match the section list
- the carrier type is unsupported

Validation should warn when material profiles are simulated/parameterized instead of measured.
