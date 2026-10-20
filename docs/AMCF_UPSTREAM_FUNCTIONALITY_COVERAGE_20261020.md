# AMCF Upstream Functionality Coverage

This is the current code-level boundary between the local `Github repos`
collection and the AMCF-owned Main/public package. It answers whether an
upstream repository is a missing AMCF capability or simply a reference/dependency
that should remain outside the project licence.

## Runtime-integrated capabilities

| Upstream surface | Main/public use | Current evidence |
|---|---|---|
| OpenCV | Image/video loading, masks, contours, optical-flow/diagnostic operations, and the deep adapter frame/overlay path | Installed API use; Main tests and the 2026-10-20 deep run passed |
| scikit-image | Image-quality metrics and comparison gates | Installed API use; full Main/public suites passed |
| FFmpeg/FFprobe | Video/audio extraction, MP4 export, and decoded-video checks | External executable boundary; existing video pipeline and acceptance runs passed |
| SAM2/SAMURAI | Box-prompt segmentation masks for the semantic component/diagnostic path and the bounded HOOT annotated Level-5 proof | `src/amcf_deep_semantic_inference.py` and `src/amcf_hoot_level5_inference.py`; Main and public five-frame CPU runs plus a 54-frame/18-mask HOOT reproduction passed |
| CoTracker | Point tracks and visibility for persistent motion/identity evidence | `src/amcf_deep_semantic_inference.py`; Main and public five-frame CPU runs passed |

The deep adapters retain the upstream repositories and checkpoints outside the
AMCF package. They are real execution bridges, not sidecar-only validators.

## Reference-only or separately bounded surfaces

RAFT, PySceneDetect, Cutie, XMem, XMem2, DEVA, TAPNet, Track-Anything, AOT,
the flipbook reference collection, CompressorJS, and UPNG.js were inspected as
research or implementation references. Their entire repositories are not
copied into Main, and their complete feature sets are not claimed as AMCF
runtime capabilities. The accepted AMCF progression does not require silently
substituting any of those tools for the canonical component/event archive,
decoder, diagnostics, or physical software simulation.

This is intentional rather than an omission: repository-wide source copying
would create licence and distribution errors, and an upstream tool is not
automatically an AMCF feature. A new adapter becomes part of the claim only
when its actual runtime contract, output mapping, licensing, and tests are
implemented.

## Completeness statement

The local and downloaded public trees now contain byte-identical Main/public
source, demo, documentation, and test surfaces. Both full suites pass at
`523/523`. The accepted digital AMCF archive/decode, diagnostics, software
I/O/physical simulation, bounded controlled/HOOT proof records, generic
SAM2/CoTracker bridge, and parameterized HOOT inference reproduction remain
present. The previously missing executable deep-inference bridge is now
present and has been run in both trees; the standalone HOOT path has also been
run against the local annotated sequence.

This does not claim that every arbitrary-video semantic identity problem is
solved, that every upstream research repository is embedded, or that physical
hardware has been validated. Those are different claims from preserving the
accepted AMCF functionality.
