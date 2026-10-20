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
| `docs` | 142 | 142 | 0 | 142 |
| `tests` | 67 | 67 | 0 | 67 |
| `packaging` | 3 | 3 | 0 | 3 |
| repository-root files | 23 | 23 | 0 | 23 |

The public checkout passes the maintained suite from its package root after
the 12B diagnostic profile is included:

```text
Ran 520 tests
OK
```

The public wheel also builds successfully, and `python src/amcf_cli.py status`
passes. The Windows console EXE was built and smoke-tested from the same
source set at `Main/output/amcf_cli_exe_20261020/amcf.exe`.

## Commit and Remote State

The downloaded public checkout contains the local parity commits on its local
`main` branch. Its exact current commit is recorded by:

```text
git -C Github_Public_Current rev-parse HEAD
```

At the time of this reconciliation it is at least five commits ahead of
`origin/main`, including the 12B correction, complete tracked test suite, and
diagnostic-state contract. The push was attempted with
the OpenSSL Git transport but Git Credential Manager returned no credentials,
so the remote GitHub branch was not changed by this run. No claim of a pushed
GitHub update is made until authentication is available.

## Scope Boundary

This reconciliation ports maintained code, tests, docs, CLI packaging, and
software-only physical I/O/player layers. It does not copy generated media or
archives, and it does not claim physical hardware validation. The strict
source-independent compact archive requirement remains separate from this
repository parity result.
