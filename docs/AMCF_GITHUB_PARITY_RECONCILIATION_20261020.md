# AMCF GitHub Parity Reconciliation

Run: `AMCF_GITHUB_PARITY_RECONCILIATION_20261020`

The public repository was checked out separately at:

```text
Github_Public_Current/
```

The maintained local `Main` trees were synchronized into that checkout without
copying generated `output/`, caches, virtual environments, or third-party
repositories.

## Byte Comparison

| Tree | Local files | Public files | Missing from public | Byte-identical |
| --- | ---: | ---: | ---: | ---: |
| `src` | 99 | 99 | 0 | 99 |
| `demo` | 65 | 65 | 0 | 65 |
| `docs` | 140 | 140 | 0 | 140 |
| `tests` | 67 | 67 | 0 | 67 |
| `packaging` | 3 | 3 | 0 | 3 |
| repository-root files | 23 | 23 | 0 | 23 |

The public checkout passes the maintained suite from its package root:

```text
Ran 518 tests
OK
```

The public wheel also builds successfully, and `python src/amcf_cli.py status`
passes. The Windows console EXE was built and smoke-tested from the same
source set at `Main/output/amcf_cli_exe_20261020/amcf.exe`.

## Commit and Remote State

Local public-checkout commit:

```text
5b41afa0a5f9bee2164937cbaddccc3529059279
Reconcile Main diagnostics CLI and workflow parity
```

The commit is one commit ahead of `origin/main`. The push was attempted with
the OpenSSL Git transport but Git Credential Manager returned no credentials,
so the remote GitHub branch was not changed by this run. No claim of a pushed
GitHub update is made until authentication is available.

## Scope Boundary

This reconciliation ports maintained code, tests, docs, CLI packaging, and
software-only physical I/O/player layers. It does not copy generated media or
archives, and it does not claim physical hardware validation. The strict
source-independent compact archive requirement remains separate from this
repository parity result.
