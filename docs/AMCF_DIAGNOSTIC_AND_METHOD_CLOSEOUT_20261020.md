# AMCF Diagnostic and Method Closeout

Run: `AMCF_DIAGNOSTIC_AND_METHOD_CLOSEOUT_20261020`

This is the current local `Main` status after the diagnostic coverage audit. It
is a claim-boundary document, not a claim that every historical generated file
belongs in the maintained source package.

## Diagnostic Coverage

The maintained Main audit passed every named diagnostic family requested by the
local progression:

| Family | Current status | What it measures |
| --- | --- | --- |
| Test 02 | Integrated | Polygon contours, masks, component IDs, optical-flow fields, update reasons, and component-owned event geometry. |
| Test 03M | Passed as a complete family | Raw screen motion, camera compensation, green residual zone motion, residual mask, component coverage, camera vectors, missing-motion regions, original reference, and side-by-side motion-truth comparison. |
| Test 08E | Passed | Farneback/TURBO motion heat and `diff x8` comparison behavior. |
| Test 10A/10B | Passed | Water and people/scene crop review, truth/full-rate/selected comparisons, and ROI motion ratios. |
| Test 12B | Passed with proxy boundary | Original green object/orange fluid candidate overlay and persistent proxy tracks. Boxes are not masks or verified identities. |
| Test 12D | Passed with review boundary | Calibrated proxy candidates and temporal box trajectories. Boxes are not masks. |
| Test 12E | Passed with review boundary | Reviewed proxy taxonomy and narrow event review. It remains human-review evidence, not universal semantic tracking. |
| HOOT | Bounded proof retained | Dataset-annotated lost/recovered semantic Level 5 evidence, not a universal arbitrary-video claim. |

Authoritative report:

```text
Main/output/amcf_diagnostic_coverage_audit_20261020_full/DIAGNOSTIC_COVERAGE_REPORT.md
```

The corrected 12B-specific audit is also recorded at:

```text
Main/output/amcf_diagnostic_coverage_audit_20261020_12b_v3/DIAGNOSTIC_COVERAGE_REPORT.md
```

## Proxy Direction Answer

The proxy renderer does move boxes over time when a track has multiple frame
observations. The current evidence does **not** prove that the white-dot people
in the timelapse are moving right-to-left under the reviewed proxy taxonomy:

- 12B has the original green object/orange fluid candidate behavior and 224
  thresholded leftward person/object proxy candidates in the Main audit, but
  those are not confirmed identities.
- 12D has 215 leftward candidate trajectories, but they were not semantically
  confirmed as people.
- 12E has zero reviewed leftward person tracks.
- The only reviewed `person_or_moving_object` positive is `track_282`, frames
  45-60, with `dx=+4`, `dy=+3`; it moves slightly right, not right-to-left.
- The 03M white/green zone view is a fixed camera-compensated measurement zone,
  not an individual-person tracker.

This means temporal proxy behavior is present, but the requested specific
right-to-left people behavior still needs a confirmed human-reviewed track if
that claim is required. The Main result is not allowed to silently promote
candidate boxes, water motion, or uncertain tracks into people.

## AMCF Method Profiles

### Strict native component-event profile

The Main component-event path is source-independent and directly decodable from
AMCF events. It retains event/component identity, timestamps, masks/geometry,
exact payload closure, and decoded frame verification. The current bounded
Main acceptance archive is approximately 58.3 MB for the 3.6 MB source-frame
reference, so the source-size requirement is **not** closed by this profile.

### Diagnostics-rich native profile

The diagnostic-state integration embeds the normalized path-free diagnostic
state, state hash, process contracts, and exact event/frame closure. Its current
generated archive is approximately 209.6 MB. This is a correctness and
diagnostic-completeness proof, not a compact storage result.

### Source-seeded compact profile

The 2026-10-19 source-seeded profile is 7,595,523 bytes, retains 2,592/2,592
logical events, exact canonical event hashes, exact canonical frame hashes,
component compositing, event ablation, corruption rejection, and remuxed audio.
It embeds a 6,097,016-byte exact visual seed and derives native event values
from that seed. It is therefore a useful compact/source-seeded profile, but it
is not a replacement for source-independent native component payload storage.

### Physical and software-I/O profiles

The PC-to-printer, PC-to-reader, PC-to-player, virtual carrier, and physical
medium paths are represented as software simulations, manifests, control
reports, and fail-closed demos. No real printer, scanner, player, motor,
sensor, manufactured carrier, or physical Level 5 validation is claimed.

## What Can Be Closed Now

- Named diagnostic families are runnable through Main and their boundaries are
  explicit.
- Test 02 contour-backed state can drive component events while exact residual
  closure protects uncovered changed pixels.
- Main has an installable `amcf` CLI with encode, component-archive, decode,
  print-plan, and status paths; wheel build/install smoke passed.
- The maintained Main suite passes when run from the package root: 520 tests.
- The Windows EXE was built and smoke-tested: `Main/output/amcf_cli_exe_20261020/amcf.exe`.

## Still Open Before Public GitHub Closeout

- A confirmed reviewed right-to-left person track, if that specific semantic
  claim is required.
- A source-independent native archive at or below the source-size ceiling.
- The public GitHub remote still needs the authenticated push of the two local
  parity commits; the downloaded public checkout itself has been tested.
- Hardware implementation and validation remain outside the current claim.

Generated videos, archives, source-specific manifests, and local output folders
remain evidence. They should not be copied into the maintained package as
source code or treated as universal behavior without their acceptance contract.
