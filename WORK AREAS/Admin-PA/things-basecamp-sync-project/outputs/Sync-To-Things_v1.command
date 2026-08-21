#!/bin/bash
# Double-click this in Finder. It does the whole thing.
#
#   1. pulls the latest
#   2. checks both ends are actually reachable
#   3. runs the import in DRY RUN and shows you exactly what it would do
#   4. asks you to confirm
#   5. only then creates anything in Things
#
# It will not write a single task without you typing yes first.

cd "$(dirname "$0")" || exit 1
REPO="$(cd ../../../.. && pwd)"
OUT="$(pwd)/last-import-run.txt"

pause_and_exit() {
  echo
  echo "$1"
  echo
  echo "Press Return to close this window."
  read -r _
  exit "${2:-1}"
}

echo "=============================================="
echo " Basecamp  ->  Things 3"
echo " $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "=============================================="

echo
echo "### Pulling latest ###"
BRANCH="$(git -C "$REPO" rev-parse --abbrev-ref HEAD 2>/dev/null)"
git -C "$REPO" pull --ff-only origin "$BRANCH" 2>&1 | tail -3

# ---- preflight: stop here rather than half-run ----
echo
echo "### Checking both ends ###"
FAIL=0

DB=$(ls -d "$HOME/Library/Group Containers/JLMPQHK86H.com.culturedcode.ThingsMac/"ThingsData-*/"Things Database.thingsdatabase/main.sqlite" 2>/dev/null | tail -1)
if [ -z "$DB" ]; then
  echo "  Things 3 database:  NOT FOUND"
  FAIL=1
else
  echo "  Things 3 database:  ok"
fi

BC="$HOME/.local/bin/basecamp"
if [ ! -x "$BC" ]; then
  echo "  Basecamp CLI:       NOT FOUND at $BC"
  FAIL=1
else
  echo "  Basecamp CLI:       ok"
  if ! "$BC" projects list --json >/dev/null 2>&1; then
    echo "  Basecamp auth:      FAILED — run '$BC auth' in Terminal once"
    FAIL=1
  else
    echo "  Basecamp auth:      ok"
  fi
fi

if [ -n "$DB" ]; then
  TAG=$(sqlite3 "$DB" "SELECT title FROM TMTag WHERE lower(title)='basecamp' LIMIT 1;" 2>/dev/null)
  if [ -z "$TAG" ]; then
    echo "  'basecamp' tag:     missing — tasks import fine, just untagged"
  else
    echo "  'basecamp' tag:     ok"
  fi
fi

[ "$FAIL" -eq 1 ] && pause_and_exit "Stopping. Nothing was touched. Tell Claude what's shown above."

# ---- dry run ----
echo
echo "### What it WOULD do (nothing created yet) ###"
echo
python3 basecamp_things_import.py 2>&1 | tee "$OUT"
DRY_STATUS=${PIPESTATUS[0]}

[ "$DRY_STATUS" -ne 0 ] && pause_and_exit "The dry run failed. Nothing was created. Send the output above to Claude."

if ! grep -q "WOULD CREATE" "$OUT"; then
  pause_and_exit "Nothing new to import — Things is already up to date." 0
fi

# ---- confirm ----
echo
echo "=============================================="
echo " Create the tasks marked WOULD CREATE above?"
echo "=============================================="
echo
printf "Type yes to go ahead, anything else to cancel: "
read -r ANSWER

case "$(echo "$ANSWER" | tr '[:upper:]' '[:lower:]')" in
  yes|y) ;;
  *) pause_and_exit "Cancelled. Nothing was created." 0 ;;
esac

# ---- apply ----
echo
echo "### Creating them in Things ###"
echo
python3 basecamp_things_import.py --apply 2>&1 | tee -a "$OUT"

echo
echo "### Sending the result back to Claude ###"
git -C "$REPO" add "WORK AREAS/Admin-PA/things-basecamp-sync-project/outputs/last-import-run.txt" \
                   "WORK AREAS/Admin-PA/things-basecamp-links.json" \
                   "WORK AREAS/Admin-PA/basecamp-import-review.json" 2>/dev/null
if git -C "$REPO" commit -q -m "Import run from $(hostname -s) $(date '+%Y-%m-%d %H:%M')"; then
  git -C "$REPO" push origin "$BRANCH" 2>&1 | tail -2
else
  echo "Nothing new to commit."
fi

echo
echo "=============================================="
echo " Done. Check Things — new tasks are tagged #basecamp."
echo "=============================================="
echo
echo "If anything showed as NEEDS A CALL, tell Claude 'the import ran'"
echo "and it'll settle those with you."
pause_and_exit "" 0
