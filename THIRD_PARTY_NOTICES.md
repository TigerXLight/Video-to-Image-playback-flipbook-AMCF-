# Third-Party Notices

No third-party deep-tool repositories, checkpoints, model weights, or cloned research projects are bundled in this clean core package.

The current external-runtime adapters for SAM2/SAMURAI and CoTracker are
implemented in `src/amcf_deep_semantic_inference.py`; the bounded HOOT
annotated proof is implemented in `src/amcf_hoot_level5_inference.py`. They
load user-supplied repositories, checkpoints, and dataset input at runtime.
They are executable integrations, but their upstream code, weights, and data
remain outside this package.

Other tools such as AOT, Cutie, DEVA, RAFT, XMem, TAPNet, and
Track-Anything remain reference/future adapters. Their full repositories are
not included here.

Each adapter must preserve its own licence boundary. Non-commercial tooling
must remain visibly labelled as source-available non-commercial or
research-use where applicable. AGPL/copyleft-heavy tooling should not be
copied into the clean core package unless that licence consequence is
explicitly accepted.

## Asset and adapter boundaries

The imported AMCF concept assets are included as AMCF project context references. Third-party materials remain excluded unless explicitly present and documented.

No model weights, checkpoints, copied third-party repositories, or deep-tool code are included in this clean public upload package.

## Canonical AMCF specification

`AMCF_CANONICAL_CONCEPT.md`, `AMCF_PHYSICAL_MEDIUM_BOUNDARY.md`, and their
maintained documentation copies are project-owned specification material.
They define AMCF as a digital component/image flipbook process and define the
physical carrier/reader as a later branch. They are not copied files from the
upstream research repositories listed in the repository manifests.
