#!/usr/bin/env bash
# demo.sh — Anchor change workflow demo
#
# Shows: branch → change anchor → diff + invariant warning → promote → confirm
#
# Uses tools/anchor_io.py for all writes to ensure canonical formatting.
# Validators are read-only — they never rewrite anchors.json.
#
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

step() { echo -e "\n${CYAN}=== STEP $1: $2 ===${NC}\n"; }

# Clean up any leftover demo branch
git branch -D demo/move-anchor-009 2>/dev/null || true

# ─────────────────────────────────────────────────
step 1 "Create feature branch"
git checkout -b demo/move-anchor-009
echo "Branch: demo/move-anchor-009"

# ─────────────────────────────────────────────────
step 2 "Modify anchor ANC-009 (TKTS Red Steps top edge)"
echo "Before:"
python -c "
import sys; sys.path.insert(0, 'tools')
from anchor_io import load
a = next(x for x in load()['anchors'] if x['id'] == 'ANC-009')
print(f'  ANC-009 lat={a[\"lat\"]} lon={a[\"lon\"]} elev={a[\"elev\"]} tol={a[\"tolerance_m\"]}m')
"

# Move the anchor 0.4m north (just over 0.3m tolerance) using anchor_io
python -c "
import sys; sys.path.insert(0, 'tools')
from anchor_io import modify_anchor
modify_anchor('ANC-009', lat=40.7591 + 0.0000036)  # ~0.4m north
"

echo "After:"
python -c "
import sys; sys.path.insert(0, 'tools')
from anchor_io import load
a = next(x for x in load()['anchors'] if x['id'] == 'ANC-009')
print(f'  ANC-009 lat={a[\"lat\"]} lon={a[\"lon\"]} elev={a[\"elev\"]} tol={a[\"tolerance_m\"]}m')
"

# ─────────────────────────────────────────────────
step 3 "Show diff + run invariant check"
echo -e "${YELLOW}Git diff:${NC}"
git diff --stat data/anchors.json
echo ""
git diff data/anchors.json
echo ""

echo -e "${YELLOW}Running anchor validation (read-only)...${NC}"
python tools/validate_anchors.py || true
echo ""

echo -e "${RED}>>> INVARIANT WARNING: ANC-009 moved ~0.4m from baseline.${NC}"
echo -e "${RED}>>> Tolerance for ANC-009 (structure) is 0.3m. EXCEEDS TOLERANCE.${NC}"
echo -e "${RED}>>> This change would FAIL the nightly anchor regression.${NC}"

# ─────────────────────────────────────────────────
step 4 "Fix: move anchor within tolerance, then promote"
# Correct to ~0.2m north (within 0.3m tolerance) using anchor_io
python -c "
import sys; sys.path.insert(0, 'tools')
from anchor_io import modify_anchor
modify_anchor('ANC-009', lat=40.7591 + 0.0000018)  # ~0.2m north
"

echo "Corrected to ~0.2m offset (within 0.3m tolerance)."
echo ""
echo -e "${YELLOW}Git diff after correction:${NC}"
git diff --stat data/anchors.json
echo ""
git diff data/anchors.json
echo ""

echo -e "${YELLOW}Re-running anchor validation (read-only)...${NC}"
python tools/validate_anchors.py
echo ""

echo -e "${GREEN}Validation passed. Committing to feature branch.${NC}"
git add data/anchors.json
git commit -m "$(cat <<'COMMITMSG'
feat(anchors): adjust ANC-009 TKTS top edge +0.2m north

Based on updated survey data. Within 0.3m structure tolerance.
This commit is on a feature branch, NOT merged to main.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
COMMITMSG
)" 2>/dev/null || echo "(commit skipped — already committed or no changes)"

# ─────────────────────────────────────────────────
step 5 "Confirm baseline on feature branch (not main)"
echo "Feature branch HEAD:"
git log --oneline -1
echo ""
echo "Anchor ANC-009 state:"
python -c "
import sys; sys.path.insert(0, 'tools')
from anchor_io import load
a = next(x for x in load()['anchors'] if x['id'] == 'ANC-009')
print(f'  id:        {a[\"id\"]}')
print(f'  name:      {a[\"name\"]}')
print(f'  lat:       {a[\"lat\"]}')
print(f'  lon:       {a[\"lon\"]}')
print(f'  elev:      {a[\"elev\"]}m')
print(f'  tolerance: {a[\"tolerance_m\"]}m')
print(f'  status:    VALIDATED (on feature branch, not yet merged to main)')
"
echo ""
echo -e "${YELLOW}To promote to canonical truth:${NC}"
echo "  git checkout main && git merge --no-ff demo/move-anchor-009"
echo ""
echo -e "${GREEN}Demo complete.${NC}"

# Return to main, delete demo branch
git checkout main 2>/dev/null || git checkout master 2>/dev/null || true
git branch -D demo/move-anchor-009 2>/dev/null || true
