#!/usr/bin/env bash
# demo.sh — Anchor change workflow demo
#
# Shows: branch → change anchor → diff + invariant warning → promote → confirm
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

# ─────────────────────────────────────────────────
step 1 "Create feature branch"
git checkout -b demo/move-anchor-009 2>/dev/null || git checkout demo/move-anchor-009
echo "Branch: demo/move-anchor-009"

# ─────────────────────────────────────────────────
step 2 "Modify anchor ANC-009 (TKTS Red Steps top edge)"
echo "Before:"
python -c "
import json
d = json.load(open('data/anchors.json'))
a = next(x for x in d['anchors'] if x['id'] == 'ANC-009')
print(f'  ANC-009 lat={a[\"lat\"]} lon={a[\"lon\"]} elev={a[\"elev\"]} tol={a[\"tolerance_m\"]}m')
"

# Move the anchor 0.4m north (just over tolerance)
python -c "
import json
with open('data/anchors.json', 'r') as f:
    d = json.load(f)
for a in d['anchors']:
    if a['id'] == 'ANC-009':
        a['lat'] = 40.7591 + 0.0000036  # ~0.4m north
        a['elev'] = 14.8  # unchanged
        break
with open('data/anchors.json', 'w') as f:
    json.dump(d, f, indent=2)
"

echo "After:"
python -c "
import json
d = json.load(open('data/anchors.json'))
a = next(x for x in d['anchors'] if x['id'] == 'ANC-009')
print(f'  ANC-009 lat={a[\"lat\"]} lon={a[\"lon\"]} elev={a[\"elev\"]} tol={a[\"tolerance_m\"]}m')
"

# ─────────────────────────────────────────────────
step 3 "Show diff + run invariant check"
echo -e "${YELLOW}Git diff:${NC}"
git diff --stat data/anchors.json
echo ""
git diff data/anchors.json | head -30
echo ""

echo -e "${YELLOW}Running anchor validation...${NC}"
python tools/validate_anchors.py || true
echo ""

echo -e "${RED}>>> INVARIANT WARNING: ANC-009 moved ~0.4m from baseline.${NC}"
echo -e "${RED}>>> Tolerance for ANC-009 (structure) is 0.3m. EXCEEDS TOLERANCE.${NC}"
echo -e "${RED}>>> This change would FAIL the nightly anchor regression.${NC}"

# ─────────────────────────────────────────────────
step 4 "Fix: move anchor within tolerance, then promote"
python -c "
import json
with open('data/anchors.json', 'r') as f:
    d = json.load(f)
for a in d['anchors']:
    if a['id'] == 'ANC-009':
        a['lat'] = 40.7591 + 0.0000018  # ~0.2m north (within 0.3m tolerance)
        break
with open('data/anchors.json', 'w') as f:
    json.dump(d, f, indent=2)
"

echo "Corrected to ~0.2m offset (within 0.3m tolerance)."
echo ""
echo -e "${YELLOW}Re-running anchor validation...${NC}"
python tools/validate_anchors.py
echo ""

echo -e "${GREEN}Validation passed. Promoting change.${NC}"
git add data/anchors.json
git commit -m "feat(anchors): adjust ANC-009 TKTS top edge +0.2m north

Based on updated survey data. Within 0.3m structure tolerance.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>" 2>/dev/null || echo "(commit skipped — already committed or no changes)"

# ─────────────────────────────────────────────────
step 5 "Confirm baseline updated"
echo "Current HEAD:"
git log --oneline -1
echo ""
echo "Anchor ANC-009 state:"
python -c "
import json
d = json.load(open('data/anchors.json'))
a = next(x for x in d['anchors'] if x['id'] == 'ANC-009')
print(f'  id:        {a[\"id\"]}')
print(f'  name:      {a[\"name\"]}')
print(f'  lat:       {a[\"lat\"]}')
print(f'  lon:       {a[\"lon\"]}')
print(f'  elev:      {a[\"elev\"]}m')
print(f'  tolerance: {a[\"tolerance_m\"]}m')
print(f'  status:    PROMOTED (within tolerance)')
"
echo ""
echo -e "${GREEN}Demo complete. Baseline updated.${NC}"

# Return to main
git checkout main 2>/dev/null || git checkout master 2>/dev/null || true
