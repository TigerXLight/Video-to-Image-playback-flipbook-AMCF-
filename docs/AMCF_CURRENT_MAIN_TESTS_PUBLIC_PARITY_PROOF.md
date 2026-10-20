# AMCF Current Main, Tests, and Public Parity Proof

This is the current evidence record for comparing the public GitHub checkout with the local `Main` project and the accepted local `Tests` progression. It is a code/behavior/coverage comparison, not a byte-identity claim for generated archives or videos.

## Roots Compared

- Public checkout: `<public-checkout>`
- Local maintained project: `<workspace-root>/Main`
- Local evidence tree: `<workspace-root>/Tests`
- Context timeline: `<workspace-root>/transcript summary.txt`
- Current public HEAD: `f9da61ec4100e5f271a234dbaedc5791fd868054`

## Public Checkout versus Main Source Mirror

The current tracked-file comparison found:

| Measure | Result |
| --- | ---: |
| Public tracked files checked | 384 |
| Public files byte-identical in Main | 380 |
| Public files missing from Main | 3 |
| Public files differing in Main | 1 |
| Main-only files | 588 |

The three missing files are the newest parity records created after the previous Main mirror checkpoint:

- `docs/AMCF_MAIN_PUBLIC_PARITY_BENCHMARK_AND_PACKAGE_CHECK.md`
- `docs/AMCF_TESTS_NEWEST_TO_OLDEST_PART16_V2_NATIVE_AND_CLOSEOUT_REVIEW.md`
- `docs/AMCF_TESTS_NEWEST_TO_OLDEST_PART17_DIGITAL_DIAGNOSTICS_AND_NATIVE_CHAIN_REVIEW.md`

The one differing file is `docs/AMCF_FULL_LOCAL_WORKSPACE_PARITY_GROUP_LEDGER.md`, which has the newer Part 16/17 entries in the public checkout. No public runtime source file was found missing or changed by this comparison.

The Main-only files are retained root launchers, legacy context, assets, and local workspace material. They are not evidence that public runtime behavior is missing. They still require the separate Tests/workspace disposition process described below.

## Strict Main/Public Workflow Proof

The repository strict proof checked 14 relevant Main files and mapped 13 public equivalents. It reported:

- functional output parity: `true`;
- local and public component archive: both `620,094` bytes;
- component events: both `9`;
- track taxonomy: both `8` matching IDs;
- requested frames: both `4`;
- local and public output under source-size ceiling: `true`;
- local and public decoded video present: `true`;
- local and public viewer/deliverable outputs present: `true`;
- public not slower in the bounded run: `true`;
- `unsafe_acceptance_count`: `0`.

Measured bounded runtime was approximately `98.824322` seconds for the local Main proof and `14.016375` seconds for the public proof. This is evidence for the tested case, not a universal performance guarantee.

## Exact Differences That Are Expected or Intentional

The strict proof correctly reports that raw generated identities are not equal:

- archive hashes differ;
- deliverable ZIP hashes differ;
- reconstructed video hashes differ;
- elapsed seconds are not identical.

The reasons are packaging layout, timestamps, paths, encoder/container details, and the public clean-package architecture. The public behavior proof is based on output classes, frame/event counts, taxonomy, size ceiling, decode/reconstruction presence, and validation—not on pretending those generated artifacts are byte-identical.

The public `amcf_local_main_tracking_test03a.py` differs from the Main root script only in workspace discovery: it accepts `AMCF_WORKSPACE_ROOT` and searches for the workspace marker instead of assuming the script lives directly under `Main`. The tracking algorithm, seeds, expected source metadata, diagnostics, and fail-closed behavior remain aligned.

## Accepted Tests Evidence Mapped to Public Code

The accepted or bounded evidence used for the current public surface is:

| Local evidence | Public mapping | Result |
| --- | --- | --- |
| Pre-GitHub source frames/video to AMCF | `amcf_digital_encoder`, `amcf_video_pipeline`, validators, demos, tests | Present and tested |
| Pre-GitHub AMCF to decoded frames/video | video pipeline, component archive, deliverable package, decode tests | Present and tested |
| Test 02 diagnostics | `amcf_test02_diagnostic_viewer`, tracking/quality modules, demo/test | Present and tested on deterministic manifests |
| 13I/13J/13K/13J2/13N bounded native chain | `src/amcf_v2/` archive/decode/compositor/playback layers | Present and tested for bounded fixtures |
| 13D/13L and 13D2/13O bounded payload experiments | V2 codec/decode contracts and archive tests | Represented without claiming general compression solved |
| 13P WebP-lossless feasibility | V2 WebP codec adapter and registry | Present with optional Pillow handling |
| 14F/14H/14J bounded V2 package and sidecar | V2 public package, 14H archive, sidecar modules/tests | Present and tested |
| PC -> printer, reader, player-control, physical-player layers | Existing public software-I/O and physical-player modules/docs/tests | Preserved |

## Tests Workspace Status

The full local Tests inventory is complete as an inventory, but not every file is an accepted runtime feature:

- `142,261` files inventoried;
- `185` top-level folders with files;
- `2,421` code/runnable files hashed;
- `318` exact public code matches;
- `143` same-name/different-content review records;
- `1,642` unmatched code/runnable records requiring explicit semantic disposition;
- automated scan semantic reviews completed by that scan: `0`.

Therefore the public repo is not yet allowed to claim universal full-workspace parity. Historical/rejected experiments, generated evidence, third-party repositories, local wrappers, and accepted runtime behavior must continue to be distinguished file by file.

## Packaging Proof

The existing `pyproject.toml` was built successfully after installing only the missing build-time `wheel` tool:

```text
amcf_public_workflow-0.1.0-py3-none-any.whl
```

The wheel was installed into an isolated temporary environment with `--no-deps`. The installed console command passed:

```text
amcf status   -> ok: true
amcf --help   -> exit 0
```

No project runtime dependency was added. The base package remains dependency-free; research packages remain optional, and FFmpeg/FFprobe remain external requirements for video input/export paths.

## Current Conclusion

The public repo now has the accepted digital workflow, diagnostics, bounded native playback chain, software I/O layers, physical-player software-control layers, and an installable CLI package represented and tested.

It is **not** yet a defensible claim of 100% whole-workspace parity because the remaining 1,642 unmatched code/runnable records still need explicit source-level acceptance, supersession, rejection, generated-output, or third-party dispositions. That is the next parity task; it is not a reason to copy every historical Test folder wholesale.

## Claim Boundary

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- real motors/sensors/cartridges/printer/scanner/player validated: false
- generated output committed: false
- `unsafe_acceptance_count`: `0` in the reviewed proof paths
