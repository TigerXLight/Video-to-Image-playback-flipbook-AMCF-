# AMCF Material Coupon Analysis Parity

Run context: `AMCF_MATERIAL_COUPON_ANALYSIS_PARITY_V1`

This document records the public-safe port of the software-only material coupon analysis helper from the local material-coupon scan planning run.

The helper analyzes synthetic or provided coupon images for marker, registration, timing/index, colour, grey-ramp, fine-line, checkerboard, metadata, and hash-lane proxy scores. It is a diagnostic model only.

## Public Files

- `src/amcf_material_coupon_analysis.py`
- `demo/run_amcf_material_coupon_analysis_demo.py`
- `tests/test_amcf_material_coupon_analysis.py`

Generated output from the demo is written under:

- `output/amcf_material_coupon_analysis/`

Generated output is not committed.

## Optional Dependency Boundary

The analyzer uses Pillow if available. If image support is unavailable, it fails closed and reports that analysis could not be performed. No dependency is added by this port.

## Claim Boundary

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- real sensor validation claimed: false
- real scanner required: false
- real coupon test claimed: false
- unsafe_acceptance_count: 0

This is not a real scan result, not hardware validation, and not physical proof.
