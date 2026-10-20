# AMCF Root Runner Source Parity Review

## Purpose

This review records the source-level comparison of the seven AMCF-owned Python
runners at the workspace root, outside `Main/` and `Tests/`. It is part of the
universal local-workspace comparison and prevents generated research runs from
being mistaken for missing public application modules.

The review is about software and evidence parity only. It does not claim real
hardware validation, a manufactured player, physical Level 5 completion, or
physical printer/scanner/motor/sensor validation.

## Scope

The inspected local runners were:

- `run_amcf_canonical_concept_alignment.py`
- `run_amcf_non_ideal_physical_carrier_simulation.py`
- `run_amcf_physical_carrier_research_matrix_and_simulation_plan.py`
- `run_amcf_physical_medium_flipbook_simulation.py`
- `run_amcf_primary_adapters_and_vertical_stack_physical_design.py`
- `run_amcf_single_app_main_entrypoint_config_github_layout.py`
- `run_amcf_vertical_stack_physical_medium_simulation.py`

The comparison checked imports, inputs, output roots, subprocess/tool usage,
and the public source, demo, test, and documentation correspondence.

## Findings

| Local runner | Observed behavior | Public correspondence | Disposition |
| --- | --- | --- | --- |
| canonical concept alignment | Writes canonical concept/boundary/alignment documents and records the corrected digital/physical boundary. | `docs/AMCF_CANONICAL_CONCEPT.md`, `docs/AMCF_HARDWARE_SOFTWARE_PATHS.md`, physical-player docs. | `PUBLIC_EQUIVALENT_DOCS` |
| non-ideal physical carrier simulation | Uses OpenCV, NumPy, Pillow, private dated runs, local source media, marker distortion, rectification, color correction, and generated images/video/reports. | `src/amcf_physical_medium_simulation.py`, its demo/test, and physical-medium docs provide a bounded deterministic no-hardware summary. | `PUBLIC_EQUIVALENT_TESTED`; private orchestration/media remain local evidence |
| physical-carrier research matrix and simulation plan | Generates material, energy, actuation, recovery, transport, and reference matrices from the physical dossier and local run history. | mechanism-profile, physical-medium, and physical-player docs. | `DOC_ONLY` / future design research |
| physical-medium flipbook simulation | Reads private source/AMCF video and manifests, creates proxy pages, recovers pages, computes metrics, and emits contact sheets/video. | public physical-medium simulation and physical-player modules. | `LOCAL_RESEARCH_EVIDENCE`; generated media not copied |
| primary adapters and vertical-stack physical design | Orchestrates local subprocesses and summarizes adapter/vertical-stack outputs in a dated `Tests` run. | public physical-medium and physical-player software boundaries. | `PUBLIC_EQUIVALENT_PARTIAL`; local orchestration is workspace-specific |
| single-app Main entrypoint/config/GitHub layout | Checks local `Main/amcf_vnext.py`, local config, and staged toolchain layout. | `src/amcf_vnext.py`, `src/amcf_cli.py`, `docs/AMCF_APP_WORKFLOW_SPEC.md`. | `APP_LAYOUT_EVIDENCE`; not a finished app |
| ideal vertical-stack physical-medium simulation | Uses OpenCV, NumPy, Pillow, private media, and generated aligned pages/recovered frames/video. | `src/amcf_physical_medium_simulation.py`, demo, and tests. | `PUBLIC_EQUIVALENT_TESTED` for the bounded software model |

## Dependency and Path Findings

The non-ideal and vertical-stack runners import optional scientific/image
libraries and use FFmpeg through subprocesses. They also refer to private
workspace media, dated test-run folders, and a local Python environment. Those
references are valid for historical evidence runners but are not suitable for a
public installed command.

The public implementation keeps this boundary explicit:

- the physical-medium module uses deterministic report data and no private
  workspace paths;
- public demos write only under `output/`;
- optional computer-vision/media paths are not presented as hardware support;
- third-party/reference trees are not vendored wholesale;
- generated images, videos, CSVs, and dated run folders are not source parity
  requirements.

## Main and Public Relationship

The local `Main` folder contains the maintained v-next, Test 02, tracking, and
virtual-hardware sources. It does not contain the root physical-medium runners
or the public software I/O/physical-player module tree. The public checkout
therefore intentionally contains newer public modules that are not present in
the older `Main` snapshot.

The correct next action is not to copy these runners into `Main` or GitHub.
Their accepted reusable behavior is already represented by tested public
modules and reports. Any future promotion of a specific runner behavior must
identify a concrete user-facing contract, remove private path coupling, add a
public test, and make an explicit dependency/provenance decision.

## Review Result

- Root runner source files inspected: `7`
- Public runtime modules required from these runners: `0` additional bulk copies
- Public bounded physical-medium correspondence: present and tested
- Workspace-specific generated orchestration: intentionally not copied
- Local path leak in this review document: none
- `unsafe_acceptance_count`: `0` in the public bounded paths
- Hardware validation claimed: `false`
- Physical Level 5 claimed: `false`
- Manufactured player claimed: `false`

This closes the root physical/research runner comparison as a dispositioned
group. It does not by itself prove byte-for-byte parity with every generated
local artifact.
