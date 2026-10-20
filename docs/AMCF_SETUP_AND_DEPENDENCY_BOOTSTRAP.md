# AMCF Setup and Dependency Bootstrap

## Purpose

The maintained AMCF repository contains the core archive, compositor, decoded
video, diagnostic, virtual-reader, print-plan, and software-control paths.  The
deep inference adapters are executable, but their large upstream repositories,
model checkpoints, and HOOT data are external runtime resources.

`amcf setup` makes that boundary reproducible without silently copying those
resources into the public repository.

## Safe check

From the repository root:

```text
python src/amcf_cli.py setup --check --existing-config amcf_config.example.json --report-output output/amcf_setup_report.json
```

The command checks Python modules, `ffmpeg`/`ffprobe`, pinned repository paths,
checkpoint hashes, and the core/deep claim boundary.  It also writes a local
`amcf_runtime_config.json` that is ignored by Git.

The core AMCF archive does not require SAM2, CoTracker, their checkpoints, or a
source MP4 at decode time.  Those resources are required only for the external
deep-inference and bounded semantic evidence paths.

## Research setup

Install the ordinary research dependencies only:

```text
python src/amcf_cli.py setup --install-research
```

Prepare the complete optional deep runtime explicitly:

```text
python src/amcf_cli.py setup --install-deep \
  --accept-upstream-licenses \
  --accept-noncommercial \
  --config-output amcf_runtime_config.json \
  --report-output output/amcf_deep_setup_report.json
```

On Windows the equivalent maintained wrapper is:

```text
cmd\RUN_AMCF_SETUP.cmd --install-deep --accept-upstream-licenses --accept-noncommercial
```

`--install-deep` performs these bounded actions:

1. Installs the declared PyTorch/SAM2 runtime packages into the selected
   Python environment.
2. Clones the pinned SAMURAI/SAM2 and CoTracker repositories into
   `.amcf-runtime/repositories/`.
3. Installs those external repositories in editable mode for the selected
   environment.
4. Downloads the selected SAM2 tiny and CoTracker offline checkpoints into
   `.amcf-runtime/checkpoints/`.
5. Verifies the declared SHA-256 values and emits a runtime config.

To fetch the bounded HOOT proof vector without bundling it:

```text
cmd\RUN_AMCF_SETUP.cmd --download-hoot --accept-hoot-terms
```

This downloads `potted_plant/008.zip` to `.amcf-runtime/datasets/HOOT/`,
verifies its declared SHA-256, and leaves the archive outside the repository.
It is not included in `--install-deep` automatically.

The repository and checkpoint bytes are not copied into `Main` or the public
GitHub checkout.  CoTracker has a non-commercial/research licence boundary,
so the explicit `--accept-noncommercial` confirmation is required before its
tree or checkpoint is prepared.  SAM2/SAMURAI notices remain external and
must be retained alongside any local installation.

## FFmpeg and HOOT

FFmpeg is checked but not downloaded automatically.  A Windows build has its
own LGPL/GPL selection and notice obligations; users should install a build
they are permitted to use and place `ffmpeg.exe` and `ffprobe.exe` on `PATH`.

The HOOT dataset may be supplied by the user or fetched explicitly with
`--download-hoot --accept-hoot-terms`; setup never downloads it implicitly or
redistributes it. After the deep runtime is ready, pass the generated config to
the bounded adapter, for example:

```text
cmd\RUN_AMCF_VNEXT.cmd deep-inference --config amcf_runtime_config.json --input input.mp4 --output output/deep_evidence
cmd\RUN_AMCF_VNEXT.cmd hoot-level5 --config amcf_runtime_config.json --input path\to\hoot\008 --output output/hoot_evidence
```

## Claim boundary

Successful setup means the selected external runtime is available.  It does
not by itself claim universal semantic identity, hardware Level 5, a physical
reader/printer/player, or a new AMCF archive format.  Deep outputs remain
diagnostic/event-generation evidence and must pass the existing AMCF acceptance
gates before a bounded semantic claim is made.
