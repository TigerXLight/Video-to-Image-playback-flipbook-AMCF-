# AMCF Playback Index Planner Parity

This document records the public-safe parity port for the 13C2/13E runtime playback archive planning layer.

The local 13C2 and 13E runs created external decode/seek indexes and an indexed playback reader prototype. Their useful public behavior is role-based archive planning:

- eager startup metadata reads
- lazy/streamed media reads
- decode-index and seek-index separation
- archive fingerprint validation
- startup plan construction
- playback plan construction
- bounded fail-closed mismatch reporting

## Public Code

- `src/amcf_playback_index_planner.py`

The module provides:

- role-based entry lookup
- startup plan construction
- playback plan construction
- selected fingerprint validation against ZIP metadata
- eager startup-entry read checks
- a consolidated playback-index report

## Demo

Run from the public repo root:

```text
python demo/run_amcf_playback_index_planner_demo.py
```

Generated output is written under:

```text
output/amcf_playback_index_planner_demo/
```

Generated output must not be committed.

## Relationship To Later V2 Work

The public `src/amcf_v2/` package already contains the later V2 archive reader, manifest/index loader, seek controller, playback loop contracts, and codec registry. This module preserves the earlier 13C2/13E planning contract in a small reusable form so the public repo keeps the archived progression without duplicating the V2 package.

## Claim Boundary

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- final playback engine claimed: false
- generated output committed: false
- unsafe_acceptance_count: 0

This is a software archive planning and diagnostics layer. It is not a final playback engine, not a GUI, and not hardware proof.
