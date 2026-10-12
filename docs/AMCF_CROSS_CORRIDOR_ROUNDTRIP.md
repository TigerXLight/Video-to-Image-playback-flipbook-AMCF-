# AMCF Cross-Corridor Roundtrip

## Purpose

`AMCF_CROSS_CORRIDOR_ROUNDTRIP_PROTOTYPE_V1` connects the no-hardware AMCF software I/O pieces into one deterministic roundtrip:

```text
shared manifest
-> print layout
-> simulated reader recovery
-> player compatibility/session
-> cross-corridor report
```

## Scope

This is a software/control roundtrip using fixtures and reports. It does not perform real printing, real scanning, image processing, USB/serial communication, or hardware validation.

## Outputs

Generated demo output is written under:

```text
output/amcf_cross_corridor_roundtrip/
```

Generated output is not committed.

## Claim Boundary

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- real printer integration claimed: false
- real reader/scanner integration claimed: false
- real player communication claimed: false

## Demo

Run:

```text
python demo/run_amcf_cross_corridor_roundtrip_demo.py
```

The report requires `unsafe_acceptance_count` to remain `0`.
