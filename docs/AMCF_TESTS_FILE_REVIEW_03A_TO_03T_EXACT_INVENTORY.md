# AMCF Tests File Review: 03A Through 03T Exact Inventory

## Scope and Method

This is the exact inventory supplement for the twenty-folder `03T` down through `03A` band. Every file in each folder was enumerated by extension and artifact type. Every Python source file was identified and its imports and top-level functions/classes were inspected. The existing Part 14 review supplies the per-folder acceptance decisions; this document adds the complete folder counts and the public/Main mapping.

This does not promote generated media or private experiment environments into the public source tree. Images, videos, ZIPs, masks, checkpoints, logs, and reports are evidence artifacts unless their behavior has a source-independent public implementation.

## Complete Folder Inventory

| Folder | Total | Python | Markdown | JSON | CSV | MP4 | ZIP | PNG/JPG | HTML | CMD | Primary code / classification |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `03T` | 92 | 1 | 20 | 33 | 13 | 13 | 7 | 0 | 0 | 1 | closeout/support loop; diagnostic, later superseded |
| `03S` | 27 | 1 | 8 | 3 | 0 | 5 | 2 | 3 | 0 | 2 | corrected component map; manual-review evidence |
| `03R` | 35 | 1 | 9 | 5 | 3 | 11 | 2 | 1 | 0 | 1 | manual-map smooth retest; support experiment |
| `03Q` | 42 | 1 | 9 | 4 | 4 | 16 | 2 | 2 | 0 | 1 | reduced-support ladder; 75% selected, not final |
| `03P` | 35 | 1 | 9 | 3 | 3 | 11 | 2 | 2 | 0 | 1 | smooth visual baseline reference |
| `03O` | 42 | 1 | 10 | 6 | 0 | 0 | 3 | 17 | 1 | 1 | manual ROI editor; map-preparation tool |
| `03N` | 39 | 1 | 9 | 6 | 4 | 8 | 2 | 3 | 1 | 1 | corrected motion component map |
| `03M` | 40 | 1 | 8 | 6 | 5 | 9 | 2 | 3 | 1 | 1 | camera/residual motion truth audit |
| `03L` | 42 | 1 | 10 | 4 | 5 | 9 | 2 | 4 | 1 | 1 | single-layer review preview |
| `03K` | 36 | 1 | 7 | 2 | 3 | 16 | 2 | 3 | 0 | 1 | camera-registered hold preview |
| `03J` | 34 | 1 | 7 | 2 | 2 | 15 | 2 | 3 | 0 | 1 | physical-speed/smoothness preview |
| `03I` | 27 | 1 | 6 | 2 | 2 | 10 | 1 | 3 | 0 | 1 | watchable component-layer preview |
| `03H` | 23 | 1 | 6 | 2 | 1 | 7 | 2 | 1 | 0 | 1 | review playback with held contours |
| `03G` | 120 | 1 | 6 | 16 | 1 | 3 | 1 | 90 | 0 | 0 | plain-SAM2 fluid/solid diagnostic |
| `03F` | 149 | 1 | 6 | 14 | 1 | 3 | 1 | 122 | 0 | 0 | plain-SAM2 hybrid-resolution diagnostic |
| `03E` | 77 | 1 | 6 | 14 | 1 | 3 | 1 | 50 | 0 | 0 | plain-SAM2 prompt study |
| `03D` | 80 | 2 | 6 | 8 | 1 | 1 | 1 | 60 | 0 | 0 | plain-SAM2 multi-target diagnostic |
| `03C` | 59 | 4 | 6 | 8 | 1 | 1 | 1 | 36 | 0 | 0 | SAMURAI crash diagnosis/microproof |
| `03B` | 156 | 1 | 6 | 1 | 0 | 0 | 1 | 144 | 0 | 0 | failed SAMURAI multi-object attempt |
| `03A` | 67 | 0 | 9 | 13 | 3 | 1 | 3 | 35 | 0 | 0 | artifact/report-only continuation; no Python source |
| **Total** | **1,162** | **22** | **169** | **162** | **52** | **148** | **40** | **582** | **5** | **15** | |

## Source-Level Findings

The source files fall into these groups:

### Tracking and segmentation diagnostics

`03A–03G` contain the early tracking/segmentation attempts. They use combinations of subprocess calls, OpenCV, NumPy, image masks, contour statistics, IoU, optical-flow statistics, prompt studies, and optional SAM2/checkpoint environments. `03B` failed its multi-object SAMURAI path; `03C` diagnosed the failure; `03D–03G` produced bounded diagnostics rather than accepted reconstruction.

These files are not safe to copy into the public runtime because they assume local media, model/checkpoint state, optional deep dependencies, and generated image trees. The public repository keeps the claim-safe diagnostic/report abstractions instead.

### Motion truth and map preparation

`03H–03O` move from held contour previews to camera registration, residual masks, zone metrics, corrected component definitions, and a manual ROI editor. The most reusable source-independent behavior is the 03M camera/residual/zone diagnostic, which is represented publicly by `src/amcf_motion_truth_diagnostics.py` with tests and a deterministic demo. The 03N/03O maps and editor remain source-specific evidence.

### Visual and support experiments

`03P–03T` render candidate playback variants, support ladders, manual-map retests, and closeout loops. The sequence demonstrates that lower nominal support is not enough: measured current-frame support and visible playback quality must be checked. The later `03V` and `03Y` decisions govern this band, so 03P remains a visual reference while 03T remains partial.

## Main and Public Integration

| Local progression | Main/public state | Decision |
|---|---|---|
| `03A` bounded tracking diagnostic | A bounded Main-facing diagnostic and a public-safe adaptation exist | Keep as diagnostic only; not an accepted tracker |
| `03M` camera/residual/zone analysis | Public motion-truth diagnostic module, demo, tests, and docs exist | Ported as generic diagnostics |
| `03N` corrected component taxonomy | No source-specific map promoted as universal truth | Keep local evidence; reuse concepts only |
| `03O` manual ROI editor | No GUI/editor runtime promoted | Keep as local research tooling |
| `03P–03T` playback/support candidates | No runner copied as the public default | Preserve visual-first and support-accounting rules |
| `03D–03G` deep segmentation | No SAM2/deep model runner or checkpoint copied | Keep optional research evidence local |
| `03B–03C` failed/crash paths | No failed backend restored | Keep failure history and diagnostics only |

## Completeness Interpretation

This inventory confirms that the 03A–03T folders contain a progression of goals and revisions rather than a set of independent final implementations. Improvements were frequently locked to a folder because each folder preserved a different experiment, generated output, or review decision. Later folders did not automatically integrate every earlier script into `Main`; accepted behavior was selectively promoted.

The public repository therefore has the reusable, claim-safe behavior from this band, but not byte-for-byte parity with all 22 Python/source/report artifacts and generated media. That is intentional for rejected or local-only material and remains a documented parity distinction, not a hidden omission.

## Claim Boundary

- `unsafe_acceptance_count`: `0`.
- Hardware validation claimed: `false`.
- Physical Level 5 claimed: `false`.
- Manufactured physical player claimed: `false`.
- Real motors, sensors, cartridges, optics, scanners, cameras, or player hardware claimed: `false`.
- No public claim is made that the source-specific 03A–03T semantic reconstruction runners are complete codecs.

## Status

The 03A–03T band is inventoried and source-inspected. The next older source groups are already represented by the reviewed v0 consolidation band above; after the remaining `Tests` chronology is reconciled, the review must continue through the non-`Tests` project folders and then compare the resulting inventory against `Main` and the public repository before implementing CLI/app packaging.
