# AMCF Deep-Inference Runtime

The accepted AMCF progression used deep semantic tooling for mask generation,
tracking, proxy binding, and later semantic evidence.  Main previously stored
the resulting proof records and checked whether the external repositories and
checkpoints existed, but it did not reproduce the SAM2/CoTracker execution.
That was a real functionality gap under a requirement for standalone deep
inference.

## Executable boundary

`src/amcf_deep_semantic_inference.py` is the Main adapter.  It loads the
external repositories and checkpoints at runtime and writes bounded evidence:

- sampled input frames;
- SAM2 box-prompt masks and mask hashes;
- CoTracker grid tracks and visibility values;
- separate SAM2, CoTracker, and combined diagnostic overlays;
- an event-indexed CSV and `deep_inference_manifest.json`.

The adapter is invoked through:

```text
RUN_AMCF_VNEXT.cmd deep-inference --input <video-or-frame-directory> --output <evidence-directory>
```

The default local configuration points at the existing deep Python runtime,
SAM2/SAMURAI tree, CoTracker tree, and checkpoints.  A public checkout must
provide those paths explicitly or supply an equivalent compatible runtime.

## Integrity and boundaries

The output is inference evidence used by the AMCF diagnostic/event process; it
is not a replacement AMCF archive.  The manifest records:

- `source_video_embedded: false`;
- `complete_video_fallback: false`;
- `semantic_level5_claimed: false` until the relevant acceptance vector passes;
- hashes for generated masks and tracks;
- the external licence boundaries for SAM2 and CoTracker.

The adapter does not copy third-party source trees or model weights into Main
or GitHub.  SAM2/SAMURAI remains subject to its upstream notices.  CoTracker
remains an external non-commercial/research-bounded dependency according to
the local repository audit.  This keeps the execution capability reproducible
without falsely relicensing upstream material.

## Local acceptance run

The first Main-facing execution was run against the same five-frame proxy
sample used by the historical toolchain test.  It passed with five SAM2 masks,
five frames of CoTracker output shaped `1 x 5 x 16 x 2`, separate diagnostic
overlays, and no source-video fallback.  Evidence was written under
`Main/output/deep_inference_acceptance_20261020/` and is generated output, not
release source.

This closes the specific “Main only validates stored deep evidence” gap.  It
does not claim universal semantic identity for arbitrary videos, and it does
not turn the bounded controlled/HOOT Level-5 proofs into a blanket claim.
Other research repositories remain separate adapters until their actual
runtime contract and licence boundary are implemented and tested.
