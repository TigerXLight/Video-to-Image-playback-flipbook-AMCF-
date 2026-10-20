# Residual Visual Acceptance Parity

Part 13 ports the 07E visual-gate thresholds and residual-stream accounting distinction into a reusable public helper. `src/amcf_residual_visual_acceptance.py` checks frame count, frame rate, resolution, MAE, PSNR, temporal similarity, and suspected artifacts. Missing metrics reject; uncertain visual results require human review. It records `unsafe_acceptance_count: 0` and false physical hardware claims.

The original 07E trial selected `tile_residual_keyframe_interval_long`. Its compressed residual stream was 97,246,316 bytes against a 621,084,672-byte full-rate component-stream estimate, a reported 84.342503% reduction. The source MP4 was only 6,097,016 bytes. Therefore the result is **residual-stream compression evidence**, not a claim that its archive or final video beat the source MP4. The trial's second-clip generalisation was `NOT_RUN`.

The later 07I decision was `ACCEPT_07G_WITH_HUMAN_REVIEW`. It kept 07A as the visual reference and did not claim 07G was visually better or close to 07A. The 03Y parallax closeout also kept a suspected texture-swimming warning and required human inspection despite its `PASS` verdict. The public helper keeps an artifact warning out of automatic acceptance.

Run `python demo/run_amcf_residual_visual_acceptance_demo.py`. Local JSON and Markdown output goes under `output/amcf_residual_visual_acceptance_demo/` and is not committed.

This port covers report and gate behavior only. The 07E media encoder used NumPy, OpenCV, FFmpeg, and a local waterfall source; its generated archive and decoded MP4 were not copied. Public component-event and V2 modules have separate archive/decode paths. Their equivalence to the complete 07E residual codec is not established by this part.

Hardware validation claimed: false. Physical Level 5 claimed: false. Manufactured player claimed: false.
