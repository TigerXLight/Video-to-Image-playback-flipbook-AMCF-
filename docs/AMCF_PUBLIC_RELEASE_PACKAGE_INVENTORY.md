# AMCF Public Release Package Inventory

## 1. Core Repo Files

- `README.md`
- `CLAIM_BOUNDARIES.md`
- `PUBLICATION_STATUS.md`
- `LICENSE_MAP.md`
- `THIRD_PARTY_NOTICES.md`
- `RELEASE_MANIFEST.json`
- `.gitignore`

## 2. Physical-Player Source Modules

- `src/amcf_physical_player_state_machine.py`
- `src/amcf_physical_player_state_machine_reports.py`
- `src/amcf_physical_player_mechanism_profiles.py`
- `src/amcf_physical_player_mechanism_profile_reports.py`
- `src/amcf_physical_player_integrated_demo_reports.py`

## 3. Physical-Player Demos

- `demo/run_physical_player_state_machine_demo.py`
- `demo/run_physical_player_fail_closed_demo.py`
- `demo/run_physical_player_reverse_seek_demo.py`
- `demo/run_physical_player_mechanism_profiles_demo.py`
- `demo/run_physical_player_simulator_demo.py`
- `demo/run_physical_player_release_review.py`
- `demo/run_public_release_package_refresh.py`

## 4. Physical-Player Tests

- `tests/test_physical_player_state_machine.py`
- `tests/test_physical_player_fail_closed.py`
- `tests/test_physical_player_reverse_seek.py`
- `tests/test_physical_player_mechanism_profiles.py`
- `tests/test_physical_player_simulator_demo.py`
- `tests/test_physical_player_public_docs_sync.py`
- `tests/test_physical_player_release_review.py`
- `tests/test_public_release_package_refresh.py`

## 5. Physical-Player Docs

- `docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md`
- `docs/AMCF_PHYSICAL_PLAYER_PUBLIC_SUMMARY.md`
- `docs/AMCF_PHYSICAL_PLAYER_CONCEPT.md`
- `docs/AMCF_PHYSICAL_PLAYER_STATE_MACHINE.md`
- `docs/AMCF_PHYSICAL_PLAYER_FAIL_CLOSED.md`
- `docs/AMCF_PHYSICAL_PLAYER_REVERSE_SEEK.md`
- `docs/AMCF_PHYSICAL_PLAYER_MECHANISM_PROFILES.md`
- `docs/AMCF_PHYSICAL_PLAYER_SIMULATOR_DEMO.md`
- `docs/AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW.md`
- `docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md`
- `docs/AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH.md`
- `docs/AMCF_PUBLIC_RELEASE_PACKAGE_INVENTORY.md`

## 6. Site / Public Pages

- `site/index.html`
- `site/styles.css`
- `site/README.md`
- `site/assets/amcf_mechanical_optical_physical_player_concept.svg`

## 7. Claim-Boundary Files

- `CLAIM_BOUNDARIES.md`
- `docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md`
- `docs/AMCF_PHYSICAL_PLAYER_PUBLIC_SUMMARY.md`
- `docs/AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW.md`
- `docs/AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH.md`

## 8. Generated-Output Policy

Generated demo/report folders are local artifacts and should remain uncommitted:

- `output/`
- `demo/output/`
- `__pycache__/`
- `*.pyc`

## 9. Excluded Files / Folders

- generated output folders
- local virtual environments
- checkpoints
- model weights
- copied third-party repositories
- old run folders
- machine-specific local paths

## 10. Package-Refresh Command

```cmd
python demo/run_public_release_package_refresh.py
```

This command writes local ignored reports under `output/public_release_package_refresh/`. The reports are software release/package artifacts, not hardware proof.
