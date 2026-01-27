# Twin Earth NYC — Runbook

## Canonical Truth

**Canonical branch:** `main`

All authoritative data lives on `main`. There are no secondary truth branches. A commit on `main` is the single source of truth for:

- `data/anchors.json` — geo-anchor and scale-anchor registry
- `schemas/*.schema.json` — data contracts
- `docs/` — design specs

## Promote Mechanism

"Promote" means "merge a validated feature branch into `main`."

### Workflow

```
1. Create branch     git checkout -b feat/my-change main
2. Make changes       (edit data, docs, schemas)
3. Validate           python tools/validate_anchors.py
                      python tools/validate_schemas.py
                      python tools/validate_invariants.py
                      python -m pytest tests/ -v
4. Commit             git add -A && git commit
5. Promote to main    git checkout main && git merge --no-ff feat/my-change
6. Tag (optional)     git tag -a v0.x.y -m "description"
7. Delete branch      git branch -d feat/my-change
```

### Rules

- **No direct commits to `main`** except initial setup. All changes go through feature branches.
- **Promote = merge to `main`** after all validators pass. There is no staging branch.
- **Tags** mark milestones (e.g., `v0.1.0` = initial bundle). Tags are immutable.
- **`tools/demo.sh`** creates a throwaway branch to demonstrate the workflow. It does not merge to `main`. The demo branch is illustrative.

### Validation Gates (must pass before promote)

| Gate | Command | Blocks Merge? |
|------|---------|---------------|
| Anchor integrity | `python tools/validate_anchors.py` | Yes |
| Schema validity | `python tools/validate_schemas.py` | Yes |
| Cross-references | `python tools/validate_invariants.py` | Yes |
| Test suite | `python -m pytest tests/` | Yes |

### What "Promoted" Means in Demo Output

When `tools/demo.sh` prints `status=PROMOTED`, it means "the change passed validation and was committed to the feature branch." It does **not** mean "merged to main." The demo script never merges to `main`. Promotion to `main` requires the explicit merge step above.
