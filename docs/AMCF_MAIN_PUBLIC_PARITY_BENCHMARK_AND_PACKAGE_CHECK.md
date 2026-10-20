# AMCF Main/Public Parity Benchmark and Package Check

This record closes the first measurable `Main` versus public-checkout parity
checks. It is deliberately bounded: it does not claim that every historical
workspace experiment is an application feature, and it does not claim universal
performance identity across machines.

## Source Mirror

The maintained public checkout and the synchronized local `Main` mirror were
compared by relative path and SHA-256:

- public files checked: `381`;
- public files missing from `Main`: `0`;
- differing public files: `0`;
- `Main` extras: legacy documentation/context files and ignored/generated output.

This proves the maintained public package is mirrored exactly in `Main` for the
checked source/docs/demo/test tree.

## Deterministic Workflow Output Check

The `demo/run_amcf_cli_workflow_demo.py` smoke workflow was run from both
trees. Both runs returned five zero exit codes, `ok: true`,
`unsafe_acceptance_count: 0`, and false hardware/physical/manufactured claim
flags. The generated report contents match after removing the expected root
path field. Generated archives contain runtime timestamps and root paths, so
their raw ZIP bytes are not used as the equality criterion.

## Bounded Runtime Benchmark

Three local runs of the same CLI workflow were measured in the same Python
3.11 environment:

| Tree | Run 1 | Run 2 | Run 3 | Mean |
| --- | ---: | ---: | ---: | ---: |
| `Main` | 1.351 s | 1.695 s | 1.475 s | 1.507 s |
| public checkout | 1.358 s | 1.377 s | 1.356 s | 1.364 s |

All six runs passed. This is evidence that the synchronized public smoke path
is not slower in this bounded local comparison. It is not a complete benchmark
of every AMCF path, media size, optional dependency, or machine environment.

## Isolated Package Check

The public `pyproject.toml` was first exercised with:

```text
python -m pip wheel --no-deps --no-build-isolation <public-repo> --wheel-dir <temporary-folder> --no-cache-dir
```

The first attempt reached metadata generation but stopped because the
runtime did not have the `bdist_wheel` command. No project source was changed.
The missing build-time tool was then installed and the same package was built
successfully as:

```text
amcf_public_workflow-0.1.0-py3-none-any.whl
```

That wheel was installed with `--no-deps` into an isolated temporary Python
environment. The installed `amcf status` and `amcf --help` commands both
passed. Therefore:

- source-tree CLI smoke: passed;
- isolated wheel build: passed;
- installed console-script smoke: passed;
- EXE readiness: no.

The build-time wheel tool was used only for validation; it is not a runtime
dependency of the AMCF package. Optional research packages and FFmpeg/FFprobe
remain separately documented and were not installed by this check.

## Current Closure Status

The maintained `Main` and public source trees remain exact for the previously
mirrored public package; the current comparison is recorded in
`docs/AMCF_CURRENT_MAIN_TESTS_PUBLIC_PARITY_PROOF.md`. The bounded CLI workflow
has matching behavior and measured local runtime, while raw generated artifact
identity is intentionally not claimed. Full workspace parity remains open
until every AMCF-owned `Tests` candidate has an explicit accepted, superseded,
historical, generated, or third-party disposition and the accepted workflows
have their own bounded output/performance checks.

`unsafe_acceptance_count`: `0`.

Hardware validation claimed: `false`.

Physical Level 5 claimed: `false`.

Manufactured player claimed: `false`.
