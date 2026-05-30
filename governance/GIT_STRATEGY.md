# GIT STRATEGY — BASELINE V6

## Branch Strategy

```
main                  BASELINE_V6 (stable, frozen)
  ├── sprint/*        Authorized sprints (A1, A2, B1...)
  ├── hotfix/*        Emergency fixes (rare, authorized)
  └── experiment/*    Research (no merge to main without RFC)
```

### Rules
- **main** = BASELINE_V6 frozen. Only tagged releases. No direct commits.
- **sprint/*** = authorized work. One sprint per branch. Merged to main after completion + validation.
- **hotfix/*** = only for production-blocking bugs. Requires INCIDENT_PROTOCOL.md.
- **experiment/*** = no merge guarantee. Discard or RFC.

## Release Policy

| Type | Tag | Trigger | Audit |
|---|---|---|---|
| Baseline | `BASELINE_V<N>` | Full validation + freeze | ALL regressions PASS |
| Sprint | `SPRINT_<name>_<date>` | Sprint completion | 14/14 regressions + new tests |
| Hotfix | `HOTFIX_<date>` | Incident | Root cause + minimal patch |

### Version numbering
- BASELINE_V6 = current stable. Next: BASELINE_V7 (only after RFC + full validation).
- Pre-release: `BASELINE_V7-rc1`, `BASELINE_V7-rc2` ...
- Hotfixes increment patch: BASELINE_V6-hf1, BASELINE_V6-hf2 ...

## Rollback Policy

1. `git checkout main`
2. `git revert <commit>` (preferred — preserves history)
3. Validate: `pytest tests/ -v --tb=short` → 14/14 PASS
4. If revert impossible: restore from snapshot in `data/db/snapshot_*`

### Snapshot fallback
- Every baseline has a snapshot directory under `data/db/`
- To rollback: copy snapshot DB file over current, restore code from git tag
- Document in INCIDENT_PROTOCOL.md

## Protection Rules
- ⛔ No force push to main
- ⛔ No `git push --force` without authorization
- ✅ Commits must reference change ticket when applicable
- ✅ Tag every stable state

## Current State
- BASELINE_V6: `data/db/snapshot_baseline_v6_20260529_105928/`
- V6 SHA256: `e1e341ef44e0a61c4e846d34e05d14a4c291dcd904869f20fdf6e9a37fef1c29`
- 414,314 rows | $1,507,835,610
