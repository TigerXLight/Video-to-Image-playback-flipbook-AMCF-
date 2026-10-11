# AMCF Test 02 Dependencies And Provenance

Generated: 2026-10-03T17:02:17

## Local application code

All Test 02 application code in `Main` was newly written for this workspace. No files or functions were copied from `Github repos`.

`amcf_vnext.py` was added as a Main-facing integration layer after the v-next runtime, validator, archive writer/reader, acceptance harness, controlled Level 5 proof, and HOOT real-world/dataset-annotated Level 5 proof were established in isolated test runs. It is newly written glue/validation code for this workspace and does not copy SAM2, CoTracker, HOOT, or other upstream repository source. `amcf_config.example.json` provides configurable local paths for proof runs and optional SAM2/CoTracker assets.

## Runtime dependencies

| Component | Version / source | Licence note | Use |
|---|---|---|---|
| Python | 3.11+ available as `py -3` or `python` on PATH | PSF | scripts |
| FFmpeg | local `ffmpeg` on PATH, GPL-enabled build per `ffmpeg -L` | GPLv3+ build notice applies | video/audio decode, encode, mux |
| NumPy | 2.4.6 | BSD-style | arrays |
| Pillow | 12.3.0 | HPND | WebP image IO |
| OpenCV Python | 5.0.0.93 | Apache-2.0 package/source family | masks, contours, optical flow |
| scikit-image | 0.26.0 | BSD-3-Clause + notices | PSNR/SSIM metrics |
| SAM2 | local optional install/checkpoint outside Main | Apache-2.0 upstream family; distribution plan must be checked before bundling | optional deep segmentation proof runs only |
| CoTracker | local optional install/checkpoint outside Main | non-commercial/restricted upstream; do not bundle without explicit project/license decision | optional point tracking proof runs only |

## Reference repositories inspected

See `Github repos\REPOSITORY_MANIFEST.tsv`. OpenCV and scikit-image are used through installed package APIs only. FFmpeg is used as an installed executable.

SAM2 and CoTracker were used in isolated proof runs through local optional installs and checkpoints, not copied into Main. Other repositories remain research references unless separately integrated with a license/provenance decision. AGPL/copyleft repositories should not be copied into Main unless the project explicitly accepts those effects or reimplements only general mechanisms.

## GitHub upload boundary

Include lightweight Main scripts and docs. Do not upload:

- `.venv*`
- `Github repos`
- SAM2 / CoTracker / other upstream repository clones
- model checkpoints
- downloaded datasets
- source videos
- generated frame/mask/overlay floods
- large historical test folders
- `.zip` release/archive artifacts unless intentionally publishing a small release asset

Recommended Main files for a compact repository:

- `Main/amcf_vnext.py`
- `Main/amcf_config.example.json`
- `Main/RUN_AMCF_VNEXT.cmd`
- `Main/README.md`
- `Main/DEPENDENCIES_AND_PROVENANCE.md`
- legacy proof scripts only if still needed: `amcf_test02.py`, `amcf_tracking_test03a.py`, `test_archive_decode.py`

## Media

Original local proof/demo media and source-video URLs are not bundled in this clean core package. Included sample JSON is synthetic/demo data and should not be treated as redistributed source media.


## Clean GitHub package note

This clean package removes machine-specific paths and does not bundle model checkpoints, copied third-party deep-tool repositories, source videos, or old generated Tests folders.
