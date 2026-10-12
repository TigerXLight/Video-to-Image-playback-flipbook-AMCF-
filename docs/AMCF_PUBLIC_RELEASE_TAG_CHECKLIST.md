# AMCF Public Release Tag Checklist

Use this checklist before creating a future public release tag.

- [ ] repo clean
- [ ] latest commit pushed
- [ ] tests pass
- [ ] integrated simulator demo passes
- [ ] release review passes
- [ ] package refresh passes
- [ ] final Pages review passes
- [ ] closeout handoff passes
- [ ] tag-prep report passes
- [ ] generated output untracked
- [ ] local path scan passes
- [ ] unsafe hardware claim scan passes
- [ ] claim boundaries present
- [ ] release notes reviewed
- [ ] tag name chosen
- [ ] explicit human approval to create tag
- [ ] tag creation command not run yet
- [ ] push tag command not run yet

## Suggested Future Manual Commands

Do not run these commands unless explicitly instructed.

```bash
git tag -a amcf-physical-player-software-control-v1 -m "AMCF physical-player software-control public release v1"
```

```bash
git push origin amcf-physical-player-software-control-v1
```

These commands are future manual commands only. They are not run by `AMCF_PUBLIC_RELEASE_TAG_PREP_V1`.
