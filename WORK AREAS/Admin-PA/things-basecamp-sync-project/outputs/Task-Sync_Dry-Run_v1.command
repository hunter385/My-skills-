#!/bin/bash
# Double-click this in Finder. No terminal typing needed.
#
# Pulls the latest, runs the test harness, runs the Things -> Basecamp dry run,
# then commits the output back to the repo so Claude can read it without you
# copy-pasting anything.
#
# Writes NOTHING to Basecamp. Dry run only.

cd "$(dirname "$0")" || exit 1
REPO="$(cd ../../../.. && pwd)"
OUT="$(pwd)/last-dry-run.txt"

{
  echo "=============================================="
  echo " Things -> Basecamp dry run"
  echo " $(date '+%Y-%m-%d %H:%M:%S %Z')"
  echo " host: $(hostname -s)   python: $(python3 --version 2>&1)"
  echo "=============================================="

  echo
  echo "### [1/4] Pulling latest ###"
  git -C "$REPO" pull --ff-only origin main 2>&1 | tail -5

  echo
  echo "### [2/4] Basecamp CLI check ###"
  BC="$HOME/.local/bin/basecamp"
  if [ ! -x "$BC" ]; then
    echo "NOT FOUND at $BC"
    echo "PATH lookup: $(command -v basecamp || echo 'not on PATH')"
  else
    echo "found: $BC"
    echo "--- version ---";  "$BC" --version 2>&1 | head -3
    echo "--- accounts ---"; "$BC" accounts 2>&1 | head -10
    echo "--- projects list --json (first 25 lines) ---"
    "$BC" projects list --json 2>&1 | head -25
  fi

  echo
  echo "### [3/4] Test harness (no auth, no real data) ###"
  python3 test_things_basecamp_sync.py 2>&1 | tail -25

  echo
  echo "### [4/4] Dry run — 14 day lookback, writes nothing ###"
  python3 things_basecamp_sync.py --hours 336 2>&1

  echo
  echo "=============================================="
  echo " Done. Nothing was written to Basecamp."
  echo "=============================================="
} 2>&1 | tee "$OUT"

echo
echo "Sending results back to Claude..."
BRANCH="$(git -C "$REPO" rev-parse --abbrev-ref HEAD 2>/dev/null)"
if [ "$BRANCH" != "main" ]; then
  echo "NOTE: your checkout is on '$BRANCH', not main. Pushing that branch instead."
fi
git -C "$REPO" add "WORK AREAS/Admin-PA/things-basecamp-sync-project/outputs/last-dry-run.txt" \
                   "WORK AREAS/Admin-PA/things-completions.json"
if git -C "$REPO" commit -q -m "Dry run output from $(hostname -s) $(date '+%Y-%m-%d %H:%M')"; then
  git -C "$REPO" push origin "$BRANCH" 2>&1 | tail -2
else
  echo "Nothing new to commit — output unchanged since last run."
fi

echo
echo "Pushed. Tell Claude 'the dry run is in' and it will read the output."
echo
echo "Press Return to close this window."
read -r _
