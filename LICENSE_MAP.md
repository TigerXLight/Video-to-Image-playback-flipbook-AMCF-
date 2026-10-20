# License Map

This repository is published as a mixed-licence, source-available AMCF research repository.

Project-owned code, documentation, generated assets, and any third-party materials are governed by the licence notices that apply to their specific paths/files. Do not assume one licence applies to every file unless explicitly stated.

A final single legal licence has not been selected for all project-owned material.

## Path status

| Path | Current status |
| --- | --- |
| `src/` | Project-owned AMCF software code; final licence/publication terms still require a decision. |
| `demo/` | Project-owned runnable demonstrations; final licence/publication terms still require a decision. |
| `tests/` | Project-owned tests; final licence/publication terms still require a decision. |
| `docs/` | Project-owned documentation unless a file states otherwise; final licence/publication terms still require a decision. |
| `assets/` | Project-owned deterministic concept assets unless a file states otherwise; final licence/publication terms still require a decision. |
| `viewer/` | Project-owned static viewer stub; final licence/publication terms still require a decision. |
| Root project specification files | Project-owned AMCF methodology and design-boundary documents. This includes `AMCF_CANONICAL_CONCEPT.md`, `AMCF_PHYSICAL_MEDIUM_BOUNDARY.md`, `README.md`, and the licence/provenance notices. |
| Canonical concept and physical-boundary docs under `docs/` | Project-owned specification text. These documents define the digital component/image flipbook process and keep the physical carrier/reader branch separate from the digital proof. |
| Optional future adapters | Not included in this clean core package. Licence-specific notices are required if added later. |
| Third-party materials | Not bundled in this clean core package. |
| Generated outputs | Regenerated locally and ignored by default. |
| Checkpoints/model weights | Excluded. |
| Copied third-party repos | Excluded. |

If commercial use is restricted later, describe the relevant parts as source-available non-commercial or non-commercial research software, not strict OSI open source.

The AMCF concept definition, component-event methodology, digital flipbook
description, storage requirements, reconstruction requirements, and physical
medium boundary are project-owned specification material. They are not copied
files from SAMURAI, SAM2, OpenCV, or another reference repository. Examining
or being influenced by an upstream research project does not by itself attach
that project's licence to the AMCF specification; copied code, adapted code,
data, weights, and direct quotations still require their own source and licence
review.

## Licence vocabulary and upstream status

"Mixed licence" means that different project paths and dependencies retain
their own applicable terms. It does not erase an upstream open-source licence.
Apache-2.0, MIT, BSD, GPL, and LGPL material remains governed by those
licences where applicable. A source-available, non-commercial, research-only,
or field-of-use-restricted term should not be described as OSI open source,
even when the source is publicly readable.

| Source or dependency group | Current classification | Main treatment |
| --- | --- | --- |
| OpenCV, scikit-image, RAFT, PySceneDetect, Cutie, XMem | Apache-2.0, BSD, or MIT terms as recorded by the manifests | Installed APIs or reference-only; no upstream source tree copied into Main. |
| FFmpeg | GPL/LGPL depending on the selected build | Installed executable; build licence and notices remain applicable. |
| SAM2 | Apache-2.0 as recorded in the manifest | Local optional research dependency; not bundled in the clean core package. |
| CompressorJS and UPNG.js | MIT reference material | Compression research references only; not AMCF runtime dependencies. |
| CoTracker | Majority CC-BY-NC with file-level exceptions | Research-only; not copied into the AMCF core. |
| SAMURAI, TAPNet, DEVA, Segment-and-Track-Anything, AOT, Track-Anything, XMem2 | Repository/file-level research terms require their own review | Reference repositories only; no blanket OSI claim is made. |
| Project-owned AMCF code and specification | No final single project licence selected | Do not infer a project licence from upstream dependencies. |

## Public concept assets

Mixed-licence, source-available AMCF research repository.

Project-owned code, documentation, generated assets, and any third-party materials are governed by the licence notices that apply to their specific paths/files. Do not assume one licence applies to every file unless explicitly stated.

Additional asset path status:

| Path | Current status |
| --- | --- |
| `assets/concepts/` | Project-owned generated concept assets unless a file states otherwise. Final licence/publication terms still require a decision. |
| `assets/concepts/existing/` | Imported generated/previous AMCF concept references for context. Old diagrams may be legacy or superseded. Final licence/publication terms still require a decision. |
| Legacy/superseded assets | Historical context only; not current physical-player definition. |
| Model/checkpoint files | Excluded. |
| Copied third-party repos | Excluded. |
