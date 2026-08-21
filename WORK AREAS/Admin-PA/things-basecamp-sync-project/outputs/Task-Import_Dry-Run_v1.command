#!/bin/bash
# Double-click this in Finder. No terminal typing needed.
#
# Pulls the latest, checks both ends of the sync, runs the regression harness,
# then runs the Basecamp -> Things import in DRY RUN and commits the output back
# so Claude can read it without you copy-pasting anything.
#
# Creates NOTHING in Things. Writes NOTHING to Basecamp. Dry run only.

cd "$(dirname "$0")" || exit 1
REPO="$(cd ../../../.. && pwd)"
OUT="$(pwd)/last-import-dry-run.txt"
BRANCH="$(git -C "$REPO" rev-parse --abbrev-ref HEAD 2>/dev/null)"

{
  echo "=============================================="
  echo " Basecamp -> Things 3 import — DRY RUN"
  echo " $(date '+%Y-%m-%d %H:%M:%S %Z')"
  echo " host: $(hostname -s)   python: $(python3 --version 2>&1)"
  echo " branch: $BRANCH"
  echo "=============================================="

  echo
  echo "### [1/5] Pulling latest ###"
  git -C "$REPO" pull --ff-only origin "$BRANCH" 2>&1 | tail -5

  echo
  echo "### [2/5] Things 3 check ###"
  DB=$(ls -d "$HOME/Library/Group Containers/JLMPQHK86H.com.culturedcode.ThingsMac/"ThingsData-*/"Things Database.thingsdatabase/main.sqlite" 2>/dev/null | tail -1)
  if [ -z "$DB" ]; then
    echo "Things database NOT FOUND. Is Things 3 installed?"
  else
    echo "database: $DB"
    echo "areas and projects Things knows about:"
    sqlite3 "$DB" "SELECT title FROM TMTask WHERE type=1 AND trashed=0 AND status=0 ORDER BY title;" 2>&1 | sed 's/^/    project: /'
    sqlite3 "$DB" "SELECT title FROM TMArea WHERE visible=1 ORDER BY title;" 2>&1 | sed 's/^/    area:    /'
    echo "tags (the import needs a 'basecamp' tag to exist):"
    sqlite3 "$DB" "SELECT title FROM TMTag ORDER BY title;" 2>&1 | sed 's/^/    tag:     /'
  fi

  echo
  echo "### [3/5] Basecamp CLI check ###"
  BC="$HOME/.local/bin/basecamp"
  if [ ! -x "$BC" ]; then
    echo "NOT FOUND at $BC"
    echo "PATH lookup: $(command -v basecamp || echo 'not on PATH')"
  else
    echo "found: $BC"
    echo "--- version ---";  "$BC" --version 2>&1 | head -3
    echo "--- projects list --json (first 25 lines) ---"
    "$BC" projects list --json 2>&1 | head -25
  fi

  echo
  echo "### [4/5] Regression harness (no auth, no real data, nothing touched) ###"
  python3 test_basecamp_things_import.py 2>&1 | tail -20

  echo
  echo "### [5/5] Import dry run — creates nothing ###"
  python3 basecamp_things_import.py 2>&1

  echo
  echo "=============================================="
  echo " Done. Nothing was created in Things."
  echo "=============================================="
} 2>&1 | tee "$OUT"

echo
echo "Sending results back to Claude..."
git -C "$REPO" add "WORK AREAS/Admin-PA/things-basecamp-sync-project/outputs/last-import-dry-run.txt" \
                   "WORK AREAS/Admin-PA/basecamp-import-review.json" 2>/dev/null
if git -C "$REPO" commit -q -m "Import dry run from $(hostname -s) $(date '+%Y-%m-%d %H:%M')"; then
  git -C "$REPO" push origin "$BRANCH" 2>&1 | tail -2
else
  echo "Nothing new to commit — output unchanged since last run."
fi

echo
echo "Pushed. Tell Claude 'the import dry run is in' and it will read the output."
echo
echo "Press Return to close this window."
read -r _
