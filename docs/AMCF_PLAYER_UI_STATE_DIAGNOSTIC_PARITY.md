# AMCF Player UI State Diagnostic Parity

Run context: `AMCF_PLAYER_UI_STATE_DIAGNOSTIC_PARITY_V1`

This document records the public-safe port of the accepted player UI state diagnostic helpers from the local player UI state viewer work.

The public repo already contains the static viewer stub and sample player UI state. This parity layer adds reusable code for:

- required player UI state key validation
- fail-closed rejection when `unsafe_acceptance_count` is nonzero
- normalized viewer-state JSON
- Markdown diagnostic report generation
- claim-boundary flags showing this is not a final UI or hardware proof

## Claim Boundary

- final UI claimed: false
- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- physical proof claimed: false
- unsafe_acceptance_count: 0

## Public Files

- `src/amcf_player_ui_state.py`
- `demo/run_amcf_player_ui_state_demo.py`
- `tests/test_amcf_player_ui_state.py`

Generated output from the demo is written under:

- `output/amcf_player_ui_state/`

Generated output is not committed.

## What This Does Not Claim

This is a diagnostic/reporting surface for a software viewer state. It does not claim a finished product UI, real scanner input, real printer output, real player hardware, physical validation, or manufactured player completion.
