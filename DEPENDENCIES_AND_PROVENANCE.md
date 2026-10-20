# AMCF Test 02 Dependencies And Provenance

Generated: 2026-10-15T09:20:45

## Local application code

All Test 02 application code in `Main` was newly written for this workspace. No files or functions were copied from `Github repos`.

## Runtime dependencies

| Component | Version / source | Licence note | Use |
|---|---|---|---|
| Python | 3.11.4 at `C:\Users\fahad\AppData\Local\Programs\Python\Python311\python.exe` | PSF | scripts |
| FFmpeg | local `ffmpeg` on PATH, GPL-enabled build per `ffmpeg -L` | GPLv3+ build notice applies | video/audio decode, encode, mux |
| NumPy | 2.4.6 | BSD-style | arrays |
| Pillow | 12.3.0 | HPND | WebP image IO |
| OpenCV Python | 5.0.0.93 | Apache-2.0 package/source family | masks, contours, optical flow |
| scikit-image | 0.26.0 | BSD-3-Clause + notices | PSNR/SSIM metrics |

## Reference repositories inspected

See `Github repos\REPOSITORY_MANIFEST.tsv`. OpenCV and scikit-image are used through installed package APIs only. FFmpeg is used as an installed executable. SAM 2, RAFT, PySceneDetect, Cutie, XMem and CoTracker remain research references only; CoTracker is explicitly not copied because its majority licence is CC-BY-NC.

## Deep-inference runtime boundary

The Main adapter `src/amcf_deep_semantic_inference.py` now executes the
accepted SAM2 mask and CoTracker tracking path when the user supplies the
external repositories, compatible Python runtime, and checkpoints. Those
repositories and weights are not copied into the AMCF package. The adapter
writes bounded masks, tracks, overlays, and integrity sidecars; it does not
silently convert stored proof artifacts into a claim of fresh inference.

SAM2/SAMURAI and CoTracker retain their upstream licence and distribution
terms. In particular, the local CoTracker audit records a non-commercial or
research boundary. The AMCF project does not apply a single licence to those
upstream files and does not describe the full mixed repository as strict OSI
open source.

## Media

The source video is `Free Waterfall 4k Videoclip | Nature Videos | Youstock`, URL recorded in the handoff as https://www.youtube.com/watch?v=w6uX9jamcwQ. This test does not grant redistribution rights beyond the local experiment.
