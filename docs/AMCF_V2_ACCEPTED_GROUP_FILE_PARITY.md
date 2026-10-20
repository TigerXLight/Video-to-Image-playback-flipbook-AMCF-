# AMCF V2 Accepted Group File Parity

## Scope

This review compares the local V2 progression from 14A through 14J with the public V2 package and its tests. It distinguishes the accepted bounded package from adjacent codec investigations, viewer/report packaging, and generated sample evidence.

## 14F package comparison

The local 14F package contains 39 Python files under its `amcf_v2` package. The public `src/amcf_v2/` contains all 39 corresponding paths:

- same-path files: `39/39`;
- byte-identical files: `38/39`;
- intentional public-safe difference: `decode/decode_pipeline.py`.

The public difference hardens optional Pillow handling so the package reports a controlled missing-dependency condition instead of failing at import time. No V2 package capability was removed by that change.

## Progression disposition

| Local group | Public status | Disposition |
|---|---|---|
| 14A native codec/player architecture | represented by public V2 package structure and contracts | covered |
| 14B read-only archive reader | represented by V2 container/index/manifest readers | covered |
| 14C WebP decode adapter | represented by public WebP codec and decode pipeline | covered |
| 14D playback-loop dry run | represented by public playback loop/cache/seek modules and tests | covered |
| 14E custom component-aware codec investigation | research candidate; not the accepted bounded package | do not port wholesale |
| 14E2 hybrid component-delta refinement | research candidate; no final codec acceptance | do not port wholesale |
| 14E3 motion-aware component delta | research candidate; no final codec acceptance | do not port wholesale |
| 14F integrated bounded prototype package | public V2 package | exact/consolidated parity |
| 14G offline viewer/report UI | public viewer/report demos and release surfaces | consolidated |
| 14H larger bounded sample generalisation | generated/sample evidence around the bounded package | evidence only |
| 14I external review documentation package | review/provenance material | docs/evidence only |
| 14J WebP component metadata sidecar | public V2 sidecar metadata module, demo, and tests | covered |

## Validation

The public V2 tests passed: `12` focused tests covering the package, sidecar metadata, and playback-index planning. The public V2 demo passed with:

- `final_passed: true`;
- archive entries and indexes valid;
- 3-frame dependency graph and seek index valid;
- `unsafe_acceptance_count: 0`;
- hardware validation, physical Level 5, and manufactured-player claims false.

## Conclusion

The accepted V2 package is present in the public repository. The unmatched 14E/E2/E3 files are not a missing public feature; they are unaccepted codec investigations. The 14H/14I outputs are sample/review evidence and should not be bulk-copied into public source.
