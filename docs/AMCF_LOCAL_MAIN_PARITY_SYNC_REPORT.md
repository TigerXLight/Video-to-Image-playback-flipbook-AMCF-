# AMCF Local Main Parity Sync Report

Run name: `AMCF_PUBLIC_REPO_FULL_LOCAL_MAIN_PARITY_SYNC_V1`

Audit date: 2026-10-12

Public repo branch: `main`

Public repo starting HEAD: `4b40be0144b1f0662ca828bf670edd831ab70fdc`

Local source root inspected: `<local-main>`

Public destination root: `<public-repo>`

This report compares the already-working local AMCF `Main` project against the public GitHub repo and identifies what must be ported for full user-facing parity. It does not copy generated output, caches, local paths, private media, virtual environments, or machine-specific launch scripts into the public repo.

This report now records seven parity ports. It did not bulk-copy generated/local artifacts from the local `Main` tree, but it added a public FFmpeg-backed video pipeline, a public component-event archive layer, optional media parity hooks for WebP/OpenCV/SSIM/static viewer output, an optional optical-flow tracking report, an initial public workflow CLI, deterministic deliverable/viewer package output, and a public archive writer/reader fixture layer while preserving the newer public software I/O and physical-player architecture.

## 1. Public Repo Current HEAD

Current public repo state at the start of this audit:

- branch: `main`
- HEAD: `4b40be0144b1f0662ca828bf670edd831ab70fdc`
- prior parity audit: `docs/AMCF_DIGITAL_AMCF_PARITY_AUDIT.md`
- current public status after this run: source-frame to AMCF is implemented, MP4 to AMCF is partially implemented through an optional FFmpeg-backed adapter, decoded frames are implemented for public frame-payload AMCF archives, and decoded MP4/video export is partially implemented through FFmpeg.

## 2. Local Main Inventory

The local `Main` folder contains a small set of relevant files and generated/cache files. Paths below use `<local-main>` instead of a machine-local absolute path so this public document stays portable.

| Local path | Public equivalent | Purpose | Dependencies | Input handled | Output produced | Needed for parity | Safe to port now | Port recommendation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<local-main>/amcf_test02.py` | partial equivalents: `src/amcf_digital_encoder.py`, `src/amcf_digital_validator.py`, `src/amcf_video_pipeline.py`, `src/amcf_component_event_archive.py`, `src/amcf_adaptive_component_scheduler.py`, `src/amcf_quality_metrics.py`, `src/amcf_component_event_viewer.py`, `src/amcf_optical_flow_tracking.py`, `src/amcf_deliverable_package.py`, `src/amcf_cli.py`, `src/amcf_physical_carrier.py`, `src/amcf_virtual_carrier_reader.py` | Main MP4/component archive pipeline: reads source video, segments/tracks components, writes AMCF archive, decodes/reconstructs video, compares quality, creates viewer/report/package outputs. | `cv2`, `numpy`, `PIL`, `skimage.metrics`, FFmpeg command-line tools, standard library. | local MP4 source video. | `.amcf.zip`, component WebP events, audio copy, decoded frames/hashes, reconstructed MP4, viewer MP4s, quality metrics, reports, deliverable zip. | PORT_REQUIRED for full local component-event parity. | Partially ported. The FFmpeg video/audio/frame boundary and public archive decode/export are in `src/amcf_video_pipeline.py`. Public component-event archive support now includes WebP when Pillow is available, deterministic PPM fallback, optional OpenCV changed-region segmentation, optional optical-flow tracking reports, SSIM/PSNR-style reporting, static viewer output, clean track-taxonomy metadata, comparison frames/video when FFmpeg is available, deliverable zip packaging, and workflow CLI commands. Exact source-specific contour-overlay browser parity remains future work. | Continue with dependency/package policy and installed command setup. Do not bulk copy generated/local artifacts. |
| `<local-main>/test_archive_decode.py` | partial public equivalents: `tests/test_amcf_component_event_archive.py`, `src/amcf_component_event_archive.py` | Checks a local AMCF archive has manifest, base, audio, component events, and expected source resolution. | standard library only. | `.amcf.zip` from local component archive. | pass/fail console result. | TEST_REQUIRED after component archive format is ported. | Partially ported as public schema-aware tests for the new component-event archive fallback. | Add local-Main schema compatibility tests later if full WebP/OpenCV component archive parity is ported. |
| `<local-main>/amcf_vnext.py` | identical public file: `src/amcf_vnext.py` | Main-facing integration CLI for proof status, archive inspection, optional toolchain checks, GitHub manifest guidance, and smoke validation. | standard library; optional imports checked by name. | config files, proof-run folders, `.amcfvnext.zip` archives. | JSON/CSV status reports. | Already present in public repo. | Already ported. | Keep public version; do not duplicate. |
| `<local-main>/amcf_virtual_hardware.py` | identical public file: `src/amcf_virtual_hardware.py` | Software-only virtual reader/cartridge/player handoff support. | standard library only. | virtual sections/cartridge records. | handoff state, lane validation, reader/player status. | Already present in public repo. | Already ported. | Keep public version; no action. |
| `<local-main>/amcf_tracking_test03a.py` | no public equivalent | Tracking-only OpenCV baseline that probes local source video and writes overlay/report artifacts. It explicitly does not build AMCF archive/reconstruction. | `cv2`, `numpy`, FFmpeg probe, standard library. | local MP4 source video. | tracking overlay/video, masks, reports, zip outputs. | PORT_OPTIONAL. Useful research, not required for core public parity. | No. It is local-source-specific and not a full AMCF archive path. | Defer. Borrow concepts only if component tracking is redesigned. |
| `<local-main>/AMCF_CANONICAL_CONCEPT.md` | related public docs: `docs/AMCF_APP_WORKFLOW_SPEC.md`, `docs/AMCF_DIGITAL_AMCF_PARITY_AUDIT.md` | Defines canonical AMCF idea: source video to component/image representation to playback to decoded video, storage ceiling, audio, manifests, verification. | none. | documentation only. | concept guidance. | DOC_ONLY / PORT_OPTIONAL. | Yes, as carefully merged wording. | Public docs already capture much of this; use as reference for future component archive spec. |
| `<local-main>/AMCF_PHYSICAL_MEDIUM_BOUNDARY.md` | related public physical-player and claim-boundary docs | Separates digital AMCF proof from future physical medium. | none. | documentation only. | boundary guidance. | DOC_ONLY. | Mostly already covered. | No immediate port. |
| `<local-main>/DEPENDENCIES_AND_PROVENANCE.md` | related public docs: `PUBLICATION_STATUS.md`, `THIRD_PARTY_NOTICES.md`, `CLAIM_BOUNDARIES.md` | Local dependency/provenance notes for FFmpeg, Pillow, NumPy, scikit-image, OpenCV, and optional deep tools. | none. | documentation only. | dependency guidance. | PORT_REQUIRED as a public dependency decision before MP4 parity work. | Not as-is. It references local proof context and source-media constraints. | Convert later into public dependency policy for video adapter work. |
| `<local-main>/requirements.txt` | no public equivalent | Lists local Python media dependencies. | external packages. | dependency specification. | dependency list. | PORT_LATER. | No. Public repo has intentionally avoided dependencies so far. | Do not add until the MP4/video dependency policy is approved. |
| `<local-main>/amcf_config.example.json` | related public `src/amcf_vnext.py` config expectations | Configures local proof-run and optional tool paths. | local proof folders, optional tool paths. | local config. | config resolution. | PORT_OPTIONAL. | No. Local path structure is not public-package-safe. | Keep out or rewrite later as public sample config without local evidence paths. |
| `<local-main>/RUN_AMCF_VNEXT.cmd` | no public equivalent | Windows command wrapper for local Python selection. | local interpreter layout. | CLI args. | invokes local `amcf_vnext.py`. | LOCAL_MACHINE_SPECIFIC_DO_NOT_COPY. | No. | Do not copy. A future public CLI should use package/module entrypoints. |
| `<local-main>/RUN_TEST02.cmd` | no public equivalent | Local wrapper for the Test 02 MP4 component archive run. | local interpreter and workspace assumptions. | none/user shell. | invokes local script. | LOCAL_MACHINE_SPECIFIC_DO_NOT_COPY. | No. | Do not copy. Replace later with public CLI/demo once dependency policy is settled. |
| `<local-main>/RUN_TRACKING_TEST03A.cmd` | no public equivalent | Local wrapper for tracking baseline. | local interpreter and workspace assumptions. | none/user shell. | invokes tracking script. | LOCAL_MACHINE_SPECIFIC_DO_NOT_COPY. | No. | Do not copy. |
| `<local-main>/README.md` | public `README.md` | Local Main usage and local evidence references. | none. | documentation only. | local instructions. | DOC_ONLY. | No as-is. It includes local evidence/source-media references. | Use as reference only; do not copy into public docs unchanged. |
| `<local-main>/__pycache__/...` | none | Python bytecode caches. | generated cache. | none. | `.pyc` files. | GENERATED_DO_NOT_COPY. | No. | Never port. |

## 3. Behaviour Parity Matrix

| Behaviour | Local Main | Public repo | Parity label | Notes |
| --- | --- | --- | --- | --- |
| MP4 input | LOCAL_IMPLEMENTED | PUBLIC_PARTIAL | PORT_REQUIRED | Local `amcf_test02.py` opens a source MP4 through OpenCV. Public `amcf_video_pipeline.py` now extracts frames with FFmpeg and feeds the existing AMCF encoder. |
| Source frame input | not the primary local route | PUBLIC_IMPLEMENTED | PUBLIC_IMPLEMENTED | Public repo can encode deterministic PPM frames to `.amcf.zip`. |
| Image sequence input | not clearly separated from MP4 pipeline | PUBLIC_PARTIAL | PORT_LATER | Public source-frame manifest is close, but no general image folder scanner exists. |
| Frame extraction | LOCAL_IMPLEMENTED | PUBLIC_PARTIAL | PORT_REQUIRED | Local uses OpenCV capture; public now supports FFmpeg frame extraction. |
| Timestamps | LOCAL_IMPLEMENTED | PUBLIC_PARTIAL | PORT_REQUIRED | Local records `pts_seconds` and FPS-derived timing; public records fps/frame index but not a full schedule in the digital archive. |
| Component decomposition | LOCAL_IMPLEMENTED | PUBLIC_PARTIAL | PORT_REQUIRED | Local uses source-specific OpenCV segmentation/tracking and WebP component events. Public now has deterministic changed-region events, optional OpenCV changed-region segmentation, optional optical-flow track reports, and track-taxonomy metadata; exact source-specific contour-overlay parity remains future work. |
| Adaptive component update schedule | LOCAL_IMPLEMENTED | PUBLIC_PARTIAL | PORT_REQUIRED | Public now has `amcf_adaptive_component_scheduler.py` and timestamped component-event archive updates; full local motion/shape tracking policy remains future work. |
| AMCF archive/package creation | LOCAL_IMPLEMENTED | PUBLIC_PARTIAL | PORT_REQUIRED | Public now supports both frame-payload smoke archives and component-event archives with WebP or PPM payloads. Exact local schema parity remains incomplete. |
| Manifest generation | LOCAL_IMPLEMENTED | PUBLIC_IMPLEMENTED | PUBLIC_PARTIAL | Public component-event manifests now include base payload, components, events, dependency status, claim boundaries, unsafe acceptance count, and size-ceiling status. |
| Audio handling | LOCAL_IMPLEMENTED | PUBLIC_PARTIAL | PORT_REQUIRED | Local extracts/copies audio to archive and reconstructed video. Public video pipeline can copy audio into the archive and decoded MP4 when FFmpeg can extract it. |
| Archive size ceiling | LOCAL_IMPLEMENTED | PUBLIC_PARTIAL | PORT_REQUIRED | Public component-event archive reports `under_source_size_ceiling`; hard fail policy and broader video-source ceiling enforcement remain future work. |
| Decoded frames | LOCAL_IMPLEMENTED | PUBLIC_PARTIAL | PORT_REQUIRED | Local decoder reconstructs frame states from base plus events. Public now decodes public frame-payload AMCF archives to PPM frames and can still recover frames through virtual carrier path. |
| Decoded MP4/video | LOCAL_IMPLEMENTED | PUBLIC_PARTIAL | PORT_REQUIRED | Local pipes reconstructed raw frames to FFmpeg. Public now exports decoded MP4 from public frame-payload AMCF archives through FFmpeg. |
| Reconstruction quality checks | LOCAL_IMPLEMENTED | PUBLIC_PARTIAL | PORT_LATER | Public has PPM MAE, PSNR-style metrics, optional SSIM when scikit-image/numpy are available, static viewer output, comparison frames, and optional FFmpeg comparison video. Exact local browser overlay parity remains future work. |
| Print process | MISSING_BOTH for real printing | PUBLIC_PARTIAL | PUBLIC_IMPLEMENTED for no-hardware planning | Public has stronger print-process software prototypes than local Main. |
| Virtual reader | LOCAL_IMPLEMENTED in virtual hardware support | PUBLIC_IMPLEMENTED | PUBLIC_IMPLEMENTED | `amcf_virtual_hardware.py` is already identical in public. Public also has newer reader recovery fixtures. |
| Physical carrier export | not central in local Main | PUBLIC_IMPLEMENTED | PUBLIC_IMPLEMENTED | Public has carrier generation from digital AMCF smoke archives. |
| Player/simulator handoff | LOCAL_IMPLEMENTED in virtual hardware support | PUBLIC_IMPLEMENTED | PUBLIC_IMPLEMENTED | Public has same virtual hardware plus newer physical-player simulator/control sequence. |
| User-facing app workflow | LOCAL_PARTIAL via scripts | PUBLIC_PARTIAL via CLI/docs/demos | PORT_REQUIRED | Public now has an initial workflow CLI for encode, component-archive, print-plan, and decode. Packaging/user-guide polish remains future work. |
| CLI or app entrypoint | LOCAL_IMPLEMENTED for local proof CLI | PUBLIC_PARTIAL | PORT_REQUIRED | Public now has `src/amcf_cli.py` and `demo/run_amcf_cli_workflow_demo.py`. It is not yet an installed `amcf` command or EXE. |
| Deliverable package | LOCAL_IMPLEMENTED | PUBLIC_PARTIAL | PORT_REQUIRED | Public now has `src/amcf_deliverable_package.py` and `demo/run_amcf_deliverable_package_demo.py` for archive, comparison frames/video when FFmpeg is available, viewer files, quality report, taxonomy, and zip packaging. |
| Dependency handling | LOCAL_IMPLEMENTED for local environment | MISSING in public package | PORT_REQUIRED | Public repo has no dependency file for media pipeline; this is intentional so far. |
| Tests | LOCAL_PARTIAL helper tests/checks | PUBLIC_IMPLEMENTED for current smoke/prototypes | PUBLIC_PARTIAL | Public now includes MP4 pipeline tests and component-event archive/scheduler/quality tests. More local-Main WebP/OpenCV parity tests remain future work. |

## 4. Dependency Comparison

| Dependency | Local use | Public currently has it | Essential for parity | Optional/graceful handling | Blocks clean parity now |
| --- | --- | --- | --- | --- | --- |
| FFmpeg command-line tools | audio extraction/copy, raw-frame-to-MP4 reconstruction, viewer comparison videos, baseline encode/probe | no package dependency | Yes for decoded MP4/video and audio copy if keeping local approach. | Should be optional with clear missing-tool error and skipped tests where unavailable. | Yes, until dependency policy is approved. |
| OpenCV / `cv2` | MP4 capture, frame processing, masks, contours, optical flow, overlays, VideoWriter | no public dependency | Yes for the local MP4/component pipeline as written. | Could be optional behind adapter checks. Alternative is FFmpeg frame extraction plus simpler standard-library frame ingestion. | Yes. |
| Pillow / `PIL` | WebP encode/decode, RGBA compositing, image save/resizing | no public dependency | Yes for local component archive and reconstruction as written. | Could be optional; needed if using WebP component patches. | Yes. |
| NumPy | image arrays, masks, flow stats, frame hashing, raw FFmpeg pipe | no public dependency | Yes for local implementation. | Could be optional but practically required for media pipeline. | Yes. |
| scikit-image | PSNR/SSIM quality metrics | no public dependency | No for first encode/decode parity; useful for validation metrics. | Optional quality-metrics extra. | Not for basic MP4 ingestion, yes for local quality report parity. |
| scipy, imageio, networkx, tifffile, lazy-loader | Listed in local requirements; not clearly central in inspected core MP4 archive path. | no public dependency | Unknown / likely optional. | Should not be added until proven required. | Yes if blindly copied. |
| SAM2 / CoTracker local tools | optional proof/deep semantic adapter references in `amcf_vnext.py` config. | not bundled; checked as optional | No for core archive playback. | Keep optional and external. | No if kept optional. |
| Browser/static viewer | local HTML viewer output for comparison playback. | public has static site/viewer stubs | Optional for parity; not required for first archive support. | Generate only as optional demo output. | No. |
| Windows command wrappers | local convenience scripts. | no public workflow wrapper | No. | Replace with Python module CLI later. | No, should not be ported. |

Dependency conclusion:

The local Main project proves useful behaviour, but it is not a standard-library-only implementation. The public repo now accepts FFmpeg/FFprobe, Pillow, OpenCV, NumPy, and scikit-image as optional capability paths where available. They are still not required dependencies for the no-hardware public baseline.

## 5. Port Plan

### Stage 1 - Public repo compatibility shell

Goal:

- define public module boundaries for video input, component archive model, audio adapter, decode/reconstruct, validation report, and CLI command wrappers
- keep the current source-frame encoder intact
- keep full tests passing
- avoid external dependencies until an adapter boundary and missing-dependency behaviour are in place

Candidate files:

- `src/amcf_video_input_adapter.py`
- `src/amcf_component_archive.py`
- `src/amcf_component_archive_validator.py`
- `docs/AMCF_LOCAL_MAIN_PARITY_PORT_PLAN.md`
- `tests/test_amcf_video_input_adapter.py`

### Stage 2 - Port local Main MP4 ingestion boundary

Goal:

- support MP4/video input through a narrow adapter
- make dependencies explicit
- avoid local source-path assumptions
- expose clear errors when FFmpeg/OpenCV/Pillow/NumPy are missing

Important:

- no hidden dependency import at module import time
- no local media path baked into code
- no generated videos committed

### Stage 3 - Feed extracted frames into existing public AMCF archive pipeline

Goal:

- reuse `src/amcf_digital_encoder.py` where possible
- define whether initial MP4 support creates frame-payload smoke archives first or jumps directly to component-event archives
- avoid maintaining two incompatible archive formats without an explicit compatibility report

Recommended approach:

1. MP4 to extracted deterministic frame folder.
2. Extracted frames to existing source-frame AMCF path.
3. Then separately add component-event archive format.

This gets user-visible video input working sooner without confusing it with full component parity.

### Stage 4 - Port audio handling

Goal:

- decide whether audio is copied, extracted, re-encoded, ignored, or planned
- represent audio status in the manifest
- never fake audio parity

Recommended first behaviour:

- if audio extraction is unavailable, report `audio_status: not_exported`
- if FFmpeg is available and policy allows it, copy audio into archive with checksum and bytes

### Stage 5 - Port decoded frame/video reconstruction

Goal:

- decoded frames first
- decoded MP4 only after dependencies and audio policy are settled
- keep direct archive decode separate from virtual carrier recovery

Recommended first behaviour:

- decode public `.amcf.zip` to frame folder
- add component archive decode later
- add MP4/video container export only through an optional FFmpeg adapter

### Stage 6 - Add parity tests

Goal:

- tiny generated test media if media tooling is available
- deterministic generated frames fallback if media tooling is unavailable
- optional MP4 tests should skip clearly when FFmpeg/OpenCV are missing
- source-frame tests should remain standard-library and always run

Required tests:

- missing dependency reports safe failure
- MP4 adapter does not assume local paths
- extracted-frame manifest feeds current encoder
- audio status is explicit
- decoded frames match expected count and hashes
- generated output remains ignored

### Stage 7 - Add user-facing command layer only after parity is proven

Goal:

- add `amcf encode`, `amcf print-plan`, `amcf decode`
- keep user-facing messages accurate
- do not build GUI or EXE until CLI behaviour is stable

## 6. Port Completed In This Run

Code ported in this run: yes

Added:

- `src/amcf_video_pipeline.py`
- `demo/run_amcf_video_pipeline_demo.py`
- `tests/test_amcf_video_pipeline.py`
- audio payload support in `src/amcf_digital_encoder.py`
- audio payload validation in `src/amcf_digital_validator.py`

Behaviour added:

- MP4-style video input to AMCF using FFmpeg/FFprobe.
- Extracted source frames feed the existing public AMCF archive encoder.
- Optional copied audio payload inclusion when the source has extractable audio.
- Direct public archive decode to PPM frames.
- Direct public archive decode to MP4 when FFmpeg is available.
- Tests covering the video adapter, audio payload validation, decoded frames, decoded MP4, and missing-tool diagnostics.

Second parity port:

- `src/amcf_component_event_archive.py`
- `src/amcf_adaptive_component_scheduler.py`
- `src/amcf_quality_metrics.py`
- `demo/run_amcf_component_event_archive_demo.py`
- `demo/run_amcf_quality_metrics_demo.py`
- `tests/test_amcf_component_event_archive.py`
- `tests/test_amcf_adaptive_component_scheduler.py`
- `tests/test_amcf_quality_metrics.py`

Behaviour added:

- local-Main-style component-event archive schema with base payload and timestamped changed-region events
- deterministic changed-region bounding boxes
- WebP payload support when Pillow is available, with a standard-library PPM fallback
- decode/reconstruction to PPM frames without rereading source pixels
- archive size-ceiling status reporting
- standard-library frame quality comparison
- optional dependency status for Pillow, OpenCV, and scikit-image
- claim-boundary flags remain false and `unsafe_acceptance_count` remains 0

Third parity port:

- `src/amcf_component_event_viewer.py`
- optional OpenCV changed-region segmentation in `src/amcf_component_event_archive.py`
- optional WebP payload path in component-event archives
- optional SSIM reporting in `src/amcf_quality_metrics.py`
- viewer package generation from `demo/run_amcf_component_event_archive_demo.py`

Behaviour added:

- WebP component payloads are used when Pillow is available.
- OpenCV changed-region segmentation is used when requested and cv2/numpy are available.
- SSIM is reported when scikit-image/numpy are available.
- A static viewer package is generated for component-event archive inspection.

Fourth parity port:

- `src/amcf_optical_flow_tracking.py`
- `demo/run_amcf_optical_flow_tracking_demo.py`
- `tests/test_amcf_optical_flow_tracking.py`

Behaviour added:

- Optional OpenCV Farneback optical-flow tracking report.
- Per-frame motion median, p95, direction, update reason, flow sample count, and bounding box records.
- JSON and CSV report output under `output/`.
- Claim-boundary flags remain false and `unsafe_acceptance_count` remains 0.

Fifth parity port:

- `src/amcf_cli.py`
- `demo/run_amcf_cli_workflow_demo.py`
- `tests/test_amcf_cli.py`

Behaviour added:

- Initial public workflow CLI in `src/amcf_cli.py`.
- Commands for status, encode, component-archive, decode, and print-plan.
- CLI demo under `output/amcf_cli_workflow_demo/`.
- Tests for parser exposure, status, encode/decode/print-plan, and component archive command.

### AMCF_LOCAL_MAIN_DELIVERABLE_VIEWER_PARITY_V1

Behaviour added:

- Local-Main-style track taxonomy data as clean public metadata.
- Deterministic source/decoded/diff comparison frames.
- Optional FFmpeg comparison video when FFmpeg is available.
- Viewer, quality report, taxonomy manifest, component archive, and summary bundled into a deterministic zip under `output/`.
- Tests for taxonomy claim boundaries, comparison frames, viewer inclusion, and zip contents.

### AMCF_ARCHIVE_WRITER_READER_PARITY_PORT_V1

Behaviour added:

- Public `.amcfvnext.zip` archive fixture writer and reader.
- Manifest, claim-boundary, component-sidecar, semantic-sidecar, payload, mask, polygon, and checksum members.
- Archive inspection, JSON member reading, frame listing, component listing, and semantic-object listing.
- Checksum verification.
- Fail-closed validation for missing payloads, checksum issues, fake Level 5 claims, and fake user approval.
- Valid and intentionally invalid demo archives under `output/amcf_archive_writer_reader_demo/`.
- Tests proving `unsafe_acceptance_count` stays 0 and claim-boundary flags remain false.

Remaining parity gap:

- This is not yet the exact local `Main` OpenCV contour-overlay browser player or source-specific waterfall segmentation policy. The public repo now has equivalent clean package pieces, but not the private source media or machine-specific local proof folder.

## 7. Recommended Next Phase

Completed phase: `AMCF_LOCAL_MAIN_DELIVERABLE_VIEWER_PARITY_V1`

Purpose:

- bundled archive, comparison frames/video, viewer files, quality report, taxonomy, and summary into deterministic local output
- preserved optional dependency checks for FFmpeg, Pillow, OpenCV, NumPy, and scikit-image
- kept generated output under `output/`
- did not require GUI, real media downloads, hardware APIs, or executable packaging

Recommended next phase: `AMCF_LOCAL_MAIN_DEPENDENCY_AND_PACKAGING_POLICY_V1`

- The required user-facing workflow now has an initial CLI baseline and deliverable package output.
- Public MP4 ingestion, component-event archives, optional WebP, optional OpenCV changed-region segmentation, optional optical-flow tracking, optional SSIM, static viewer package, workflow CLI, and deliverable zip packaging now exist.
- The remaining local `Main` gaps are packaging policy, dependency declaration, installed command setup, and any optional source-specific contour overlay research that can be generalized without private media.
- The next work should decide how FFmpeg/Pillow/OpenCV/NumPy/scikit-image are declared for users before any EXE.

CLI ready now: partial initial baseline

EXE ready now: no

## 8. Tests And Demos Required For This Report

Validation commands for this run:

```text
python -m unittest discover -s tests
python demo/run_source_frames_to_amcf_digital_demo.py
python demo/run_amcf_to_physical_carrier_demo.py
python demo/run_virtual_reader_recovery_export_demo.py
python demo/run_amcf_shared_package_model_demo.py
python demo/run_amcf_cross_corridor_roundtrip_demo.py
```

Expected status after this report:

- existing public tests pass
- existing public digital demos pass
- no generated output committed
- no code behaviour changed

## 9. Claim-Boundary Status

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- real printer integration claimed: false
- real scanner integration claimed: false
- real player hardware claimed: false
- full MP4 parity claimed: false
- decoded MP4/video export claimed: false
- generated output committed: false

This report does not claim full parity. It identifies the local Main behaviours needed for parity and explains why the first safe public action should be a dependency-aware video adapter boundary rather than a bulk copy of local research scripts.
