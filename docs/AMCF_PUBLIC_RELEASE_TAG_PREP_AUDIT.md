# AMCF Public Release Tag Prep Audit

Run name: `AMCF_PUBLIC_RELEASE_TAG_PREP_V1`

This audit records the input state for release-tag preparation. It is tag preparation only. No Git tag is created by this run, and no physical hardware validation is claimed.

## Baseline

- Current baseline commit: `331848fdf10ff18eab0a9426441f0f00e91a8f03`
- Baseline run: `AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF_V1`
- Expected branch state before edits: clean `main` at the pushed closeout handoff commit.

## Existing Tag / Release Context

- Existing tags may be inspected by the tag-prep script with `git tag --list`.
- Any existing tag list is report data only.
- This run does not create a Git tag and does not create a GitHub release.

## Release Notes And Closeout Files Found

- `README.md`
- `CLAIM_BOUNDARIES.md`
- `docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md`
- `docs/AMCF_PHYSICAL_PLAYER_PUBLIC_SUMMARY.md`
- `docs/AMCF_PHYSICAL_PLAYER_RELEASE_REVIEW.md`
- `docs/AMCF_PUBLIC_RELEASE_PACKAGE_REFRESH.md`
- `docs/AMCF_PUBLIC_RELEASE_PACKAGE_INVENTORY.md`
- `docs/AMCF_PUBLIC_GITHUB_PAGES_FINAL_REVIEW.md`
- `docs/AMCF_PUBLIC_RELEASE_CLOSEOUT_HANDOFF.md`
- `docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md`

## Generated Output Folders

Generated output folders may exist locally under `output/`. They are demo/report artifacts and should remain uncommitted.

## Files To Create

- `demo/run_public_release_tag_prep.py`
- `docs/AMCF_PUBLIC_RELEASE_TAG_PREP.md`
- `docs/AMCF_PUBLIC_RELEASE_NOTES_DRAFT.md`
- `docs/AMCF_PUBLIC_RELEASE_TAG_CHECKLIST.md`
- `docs/AMCF_PUBLIC_RELEASE_TAG_PREP_AUDIT.md`
- `tests/test_public_release_tag_prep.py`

## Files To Edit

- `README.md`
- `docs/AMCF_PHYSICAL_PLAYER_DOCS_MAP.md`
- `docs/AMCF_PHYSICAL_PLAYER_DEVELOPMENT_SEQUENCE.md`
- `site/index.html`

## Boundary

This is release-tag preparation only. It prepares tag-readiness materials, a release-notes draft, a checklist, and a deterministic report. It does not create a tag, push a tag, create a GitHub release, claim manufactured hardware, claim physical proof, claim physical Level 5 completion, or claim hardware validation.
