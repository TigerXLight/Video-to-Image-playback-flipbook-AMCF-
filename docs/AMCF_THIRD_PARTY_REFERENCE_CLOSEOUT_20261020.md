# AMCF Third-Party and Reference Provenance Closeout

Date: 2026-10-20

This document closes the provenance and maintained-functionality review for
the local AMCF workspace and the downloaded public checkout. It distinguishes
runtime dependencies, optional research references, generated evidence, and
historical material. The presence of a repository in the local research
collection does not mean that its code belongs in the maintained AMCF package.

## Maintained code result

- The local `Main` source, demos, tests, and maintained documentation were
  compared with `Github_Public_Current`.
- The maintained source and demo surfaces are byte-identical: 99 `src` files
  and 65 `demo` files.
- The maintained test surface is byte-identical: 67 test files.
- The documentation surface is byte-identical after this closeout document is
  synchronized: 144 documentation files.
- Both trees pass the complete 520-test suite and the unified digital
  acceptance runner.
- The CLI status/help smoke tests, wheel install tests, Windows executable
  smoke tests, and the PC-to-printer, PC-to-reader, PC-to-player, virtual
  carrier, and cross-corridor software simulations pass in both trees.
- The exact-file hash audit compared 231 maintained Main code/text files with
  11,955 third-party reference code/text files and found zero exact file-hash
  matches.

This is evidence that no complete third-party repository file was copied into
the maintained package. It is not a legal opinion and cannot prove that no
small algorithmic idea was independently reimplemented. The source and
dependency records identify the APIs and research boundaries used by the
project.

## Runtime dependencies

The maintained runtime uses installed packages or executables rather than
bundling the upstream repositories:

- NumPy for array and numeric operations.
- Pillow for image and WebP I/O.
- OpenCV Python APIs for masks, contours, and optical-flow operations.
- scikit-image APIs for image-quality metrics.
- FFmpeg as the configured video/audio executable.

The exact versions, notices, and build notes remain in
`DEPENDENCIES_AND_PROVENANCE.md`, `LICENSE_MAP.md`, and
`THIRD_PARTY_NOTICES.md`.

## Research repositories and license boundary

The repository manifests record the inspected upstream repositories and their
commit/license metadata:

- `REPOSITORY_MANIFEST.tsv`: OpenCV, scikit-image, FFmpeg, SAM2, RAFT,
  PySceneDetect, Cutie, XMem, and CoTracker.
- `REPOSITORY_MANIFEST_EXTRA_03B.tsv`: SAMURAI, TAPNet, DEVA,
  Segment-and-Track-Anything, AOT, Track-Anything, and XMem2.

SAM2, SAMURAI, RAFT, PySceneDetect, Cutie, XMem, TAPNet, DEVA, AOT,
Segment-and-Track-Anything, Track-Anything, XMem2, and CoTracker are optional
research references or future adapters. They are not required by the
maintained AMCF runtime, and their source trees, checkpoints, and model
weights are not bundled in the clean package. CoTracker remains explicitly
research-only because its majority license is non-commercial.

The project-owned package is currently mixed-licence/source-available. A
single final legal license has not been selected, so the package must not be
described as uniformly OSI-licensed.

Mixed licence does not erase an upstream open-source licence. Apache-2.0,
MIT, BSD, GPL, and LGPL components retain their own terms. Conversely,
non-commercial, research-only, or field-of-use-restricted terms are not
described as OSI open source merely because their source is public. The exact
dependency classification is recorded in `LICENSE_MAP.md` and the repository
manifests.

## Later reference-only collections

Two workspace collections were inventoried separately from the repository
manifests:

- `Github repos/image compression`: CompressorJS and UPNG.js references,
  JPEG XL material, and Zstandard tools. CompressorJS and UPNG.js are MIT
  references; the collection retains the applicable JPEG XL, dependency, and
  tool notices. None is a maintained AMCF runtime dependency.
- `Github repos/AMCF_flipbook_reference_collection`: research and concept
  material used for comparison and design context, not copied runtime code.

These collections are now explicitly documented as reference-only. They do
not represent missing AMCF functionality, and they must not be copied into
the public package without a separate file-level license review.

## Functionality and physical/software corridors

The maintained package contains the software implementation and fail-closed
tests for:

- source video to digital AMCF packaging;
- direct AMCF event/component reading and decoded-video reconstruction;
- component, residual/native, diagnostics, and exact frame-hash checks;
- the 03M zone-motion, 08E heat/diff-x8, 10A/10B crop-review, 12B/12D/12E
  proxy-review, and bounded HOOT diagnostic/semantic contracts;
- PC-to-printer layout planning;
- PC-to-reader virtual recovery;
- PC-to-player control/runtime communication;
- virtual carrier, scan-gate, mechanical/optical, and cross-corridor software
  simulations.

These are software paths and simulations. No physical printer, scanner,
player, motor, sensor, manufactured carrier, or physical Level 5 validation
is claimed. HOOT remains a bounded dataset proof; universal person/object
identity is separate research.

## Archive claim boundary

The strict native component-event profile is directly decodable without the
source MP4 and retains the canonical event/frame contract, but its current
archive is approximately 58.3 MB against the approximately 3.6 MB
source-frame reference. The source-seeded compact profile is a separate
source-assisted option and is not a replacement for the strict native
profile. This storage-size gap is an open research problem, not a missing
runtime or third-party integration.

## Closeout result

Within the audited maintained scope, no missing runtime capability was found
between local `Main` and the downloaded public checkout. Historical test
folders, generated archives/media, third-party repositories, checkpoints, and
reference-only outputs were intentionally not copied because they are
evidence, superseded branches, or external dependencies rather than missing
maintained functionality.

The downloaded public checkout is locally verified and clean. Its local branch
is ahead of the configured online `origin/main`; the final push remains an
authentication/credential action outside this file audit. The online remote
should not be described as updated until that push succeeds.
