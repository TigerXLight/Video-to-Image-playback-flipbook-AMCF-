# AMCF Tests Newest-To-Oldest Part 5 Virtual Hardware Player UI Review

Run context: `AMCF_TESTS_NEWEST_TO_OLDEST_PART5_VIRTUAL_HARDWARE_PLAYER_UI_REVIEW_V1`

Part 5 reviews the virtual-hardware, virtual-reader, player handoff, and player UI viewer band below the pre-GitHub audit/concept folders.

This band matters because it contains accepted software-only reader/player support code and diagnostic UI state behavior that predates the later source-frame, carrier, virtual-reader recovery, and mechanical/optical simulator package work.

## Claim Boundary

- hardware validation claimed: false
- physical Level 5 claimed: false
- manufactured player claimed: false
- real printer integration claimed: false
- real scanner integration claimed: false
- real player hardware claimed: false
- final UI claimed: false
- unsafe_acceptance_count: 0

## Folders Reviewed

| Local Tests folder | Evidence read | Result |
| --- | --- | --- |
| `Test AMCF_VIRTUAL_HARDWARE_RELEASE_REFRESH` | final status, release package source/docs/viewer/tests | Release package validation, demo, and tests passed. Public `src/amcf_virtual_hardware.py`, `src/amcf_vnext.py`, and `demo/run_virtual_hardware_demo.py` were already byte-identical from Part 4. |
| `Test AMCF_PLAYER_UI_STATE_VIEWER_STUB` | final status, HTML viewer, JSON normalizer, CLI report helper, tests | Static HTML viewer and sample state already existed publicly. The reusable JSON normalizer and Markdown report helper were not present as public source code, so they were ported into `src/amcf_player_ui_state.py`. |
| `Test AMCF_VIRTUAL_READER_MAIN_INTEGRATION_PLAYER_PLAYBACK_ABSTRACTION` | final status, sample virtual cartridge, virtual hardware demo, player handoff, UI state stub | Consolidated into current public `src/amcf_virtual_hardware.py`, examples, viewer, and player UI state diagnostic layer. |
| `Test AMCF_SOFTWARE_VIRTUAL_PHYSICAL_READER_EMULATOR` | final status, split virtual cartridge/reader/scan-gate/handoff modules, demo summary | Functionality is consolidated in `src/amcf_virtual_hardware.py`. Demo behavior is represented by `demo/run_virtual_hardware_demo.py`, which still reports accepted/rescanned/rejected/degraded counts with `unsafe_acceptance_count: 0`. |
| `Test AMCF_VISUAL_STAGE_CLOSEOUT_AND_REAL_EVIDENCE_HANDOFF` | closeout status and done/not-done notes | Evidence and boundary record only. It confirms physical reader/player visuals are concepts, not hardware proof. No code port target. |
| `Test AMCF_PLAYER_UI_PLAYBACK_INTERFACE_CONCEPT` | concept boundary note | Concept UI only. It reinforces viewer boundary wording and physical-reader corrections. No runtime code port target. |

## Ported In Part 5

Part 5 added the missing public-safe player UI diagnostic helper layer:

- `src/amcf_player_ui_state.py`
- `demo/run_amcf_player_ui_state_demo.py`
- `tests/test_amcf_player_ui_state.py`
- `docs/AMCF_PLAYER_UI_STATE_DIAGNOSTIC_PARITY.md`

The port preserves the accepted local behavior:

- required player UI state keys are checked
- nonzero `unsafe_acceptance_count` is rejected
- normalized viewer-state JSON can be written
- Markdown player UI state reports can be generated
- claim-boundary flags remain false
- the viewer/report remains a software diagnostic surface, not a final UI

## Validation

Focused validation passed:

- `python -m py_compile src/amcf_player_ui_state.py demo/run_amcf_player_ui_state_demo.py tests/test_amcf_player_ui_state.py`
- `python -m unittest tests.test_amcf_player_ui_state`
- `python demo/run_amcf_player_ui_state_demo.py`

The demo writes generated output under:

- `output/amcf_player_ui_state/`

Generated output is not committed.

## Part 5 Decision

Part 5 is closed as `VIRTUAL_HARDWARE_COVERED_PLAYER_UI_DIAGNOSTICS_PORTED`.

The consolidated virtual reader/player code was already present. The missing piece was the accepted player UI state normalizer/report diagnostic layer, which is now ported and tested.

## Next Part

Continue downward through the transport, bench sensor, CIS sensor, scan-gate, pre-prototype physical device, non-ideal physical carrier, vertical stack, and physical-medium planning/simulation folders.

Those folders should be handled carefully as physical-branch evidence. They should not be confused with the digital AMCF parity closeout unless they contain reusable software-only diagnostics or fixture logic that belongs in the public repo.
