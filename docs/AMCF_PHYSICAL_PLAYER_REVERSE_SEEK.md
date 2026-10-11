# AMCF Physical Player Reverse/Seek Controls

## Purpose

AMCF is software-first. The reverse/seek layer defines bounded control behaviour that a future compact mechanical/optical AMCF player should obey.

The hardware is not present yet, but software can define safe reverse and seek rules now. Later hardware can conform to these limits and safety decisions before any hardware validation claim is made.

## Limited Reverse Buffer

Reverse starts as a limited local-buffer step-back model. The reverse buffer stores records for sections that were actually verified, displayed, gate-locked, and parked safely.

Each reverse buffer record includes:

- section id
- section index
- timestamp
- dwell estimate
- verification decision
- display permission
- gate-locked status
- parked timestamp
- safe-for-reverse flag

Invalid, corrupted, wrong, or unverified sections are not safe reverse targets.

## Safe Step-Back

`step_reverse()`:

1. checks that reverse is enabled
2. checks that the reverse buffer has a previous safe target
3. resolves the previous section
4. verifies it again
5. stages it in the hidden gate
6. requires transition blanking
7. switches it into the visible gate
8. parks the old visible section
9. records timeline events

If the buffer is empty, reverse is denied safely without pretending that arbitrary physical reverse exists.

## Local-Buffer Seek

Local seek is allowed only for sections in the verified local reverse buffer or the current prefetch queue. It is not a claim of whole-cartridge random access.

If a local seek target verifies safely, it uses the same A/B staging, hidden gate, transition blanking, visible gate switch, and parking path as forward/reverse playback.

## Arbitrary Seek Denial

Arbitrary seek outside the local buffer is denied by default. The simulator records a denial reason and does not transition or display unsafe media.

This is deliberate: future physical hardware may support richer seek mechanisms, but this repository does not claim real random-access hardware.

## A/B Staging And Gates

Reverse and seek use the same safety structure as forward playback:

- target section must verify
- hidden gate must be ready
- transition blanking must occur
- visible switch must not happen without blanking
- old visible section must park safely

## Fail-Closed Integration

Fail-closed logic blocks:

- unverified target sections
- hash-mismatch targets
- wrong section targets
- hidden-gate-not-ready transitions
- unsafe switches without blanking
- shutter or illumination failures

Unsafe acceptance remains zero in the expected path.

## What Is Not Claimed

This stage does not claim:

- manufactured hardware
- real motor reverse
- real random-access hardware
- real physical cartridge reverse validation
- real optical playback proof
- real no-gap reverse proof
- physical Level 5 completion
- hardware validation

It does claim a deterministic software/control reverse-seek model and a future hardware-support control contract.
