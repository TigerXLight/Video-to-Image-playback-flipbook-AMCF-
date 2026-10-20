# AMCF Main/Public Mirror Synchronization

## Purpose

This record documents the deliberate promotion of the current public AMCF
package into the local `Main` project folder. The goal is to let the local
project carry the newer public software-I/O, digital AMCF, diagnostic,
physical-player, release, and CLI functionality while retaining the older
Main-facing root launchers and source files.

This is a source/docs/tests/demo mirror operation. It is not a hardware
validation result and does not claim a manufactured player, physical Level 5,
real motors, real sensors, real cartridges, real optics, or real printer/reader
integration.

## Copy Evidence

The public checkout contained `379` tracked files at synchronization time:

| Public area | Tracked files |
| --- | ---: |
| `src/` | 93 |
| `demo/` | 58 |
| `tests/` | 61 |
| `docs/` | 130 |
| `site/` | 5 |
| root/config/command/assets files | remaining tracked files |

All `379` tracked public files were copied into the local `<workspace-root>/Main`
folder. Generated `output/`, caches, virtual environments, private media, and
the public Git metadata directory were not copied.

The pre-existing Main files were retained. The older Main `README.md` and
`DEPENDENCIES_AND_PROVENANCE.md` were preserved under `_legacy_main_docs/`
before the public versions replaced those root documentation files. The
pre-existing `amcf_config.example.json` and `requirements.txt` already matched
the public versions.

## Runtime Check

From the synchronized Main folder, the following public workflow paths passed:

```text
python src/amcf_cli.py status
python demo/run_amcf_cli_workflow_demo.py
```

The workflow demo completed all five command calls:

- `status`
- `encode`
- `component-archive`
- `decode`
- `print-plan`

The generated Main output remains local under `output/` and is not public
source. The CLI report preserved `unsafe_acceptance_count: 0` and false
hardware/physical-player claim flags.

## Test Context Boundary

The public `tests/` tree was copied as source evidence, but seven of its
workspace-discovery tests are intentionally coupled to the public checkout
layout: they resolve the sibling local `Main`, `Tests`, and public checkout
roots from the public repository's nested path. Running that copied suite from
the standalone Main folder therefore resolves those sibling roots differently.

This does not change public validation: the public checkout's full suite passed
`500` tests after the packaging phase. Main's direct CLI smoke path also passed.
The copied public tests should be run from the public checkout, or later
refactored into a standalone Main test harness as a separate task. They must
not be weakened merely to make an isolated folder look green.

## Synchronization Status

- public digital AMCF functionality mirrored into Main: yes;
- public software-I/O functionality mirrored into Main: yes;
- public physical-player/control functionality mirrored into Main: yes;
- public CLI and package metadata mirrored into Main: yes;
- Main CLI smoke workflow: passed;
- public full regression suite: passed, `500` tests;
- generated output committed: no;
- hardware validation claimed: false;
- physical Level 5 claimed: false;
- manufactured player claimed: false;
- `unsafe_acceptance_count`: `0` in the reviewed CLI paths.

This mirror is a significant completeness improvement, but it is not a claim
of byte-identical generated media or of identical elapsed performance across
all environments. Those require a separate controlled benchmark/output proof.
