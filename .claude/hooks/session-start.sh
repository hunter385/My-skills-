#!/bin/bash
set -euo pipefail

# Only inject tasks prompt on fresh startup, not resume/compact
INPUT=$(cat)
SOURCE=$(echo "$INPUT" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('source',''))" 2>/dev/null || echo "")

if [ "$SOURCE" != "startup" ]; then
  exit 0
fi

TASKS_FILE="/home/user/My-skills-/WORK AREAS/Admin-PA/TASKS.md"

if [ ! -f "$TASKS_FILE" ]; then
  echo "Warning: TASKS.md not found at $TASKS_FILE" >&2
  exit 0
fi

# Output a prompt injection so Claude displays the tasks report at session start
cat <<'EOF'
{"type":"user","content":"SESSION_START: Automatically display my morning tasks report now using the /tasks format before waiting for my first request. Read /home/user/My-skills-/WORK AREAS/Admin-PA/TASKS.md and present it grouped by urgency (overdue, due today, due this week, waiting, no date)."}
EOF
