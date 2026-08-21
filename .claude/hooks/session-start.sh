#!/bin/bash
# SessionStart hook — surface only what's rotting, in one line.
set -uo pipefail

INPUT=$(cat 2>/dev/null || echo '{}')
SOURCE=$(printf '%s' "$INPUT" | python3 -c \
  "import sys,json;print(json.load(sys.stdin).get('source',''))" 2>/dev/null || echo "")
[ "$SOURCE" = "startup" ] || exit 0

# Portable: works on the Mac and in remote containers alike.
ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
TASKS="$ROOT/WORK AREAS/Admin-PA/TASKS.md"
[ -f "$TASKS" ] || exit 0

python3 - "$TASKS" <<'PYEOF'
import datetime, re, sys

MONTHS = {m: i for i, m in enumerate(
    ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"], 1)}
SKIP = ("future ideas", "done", "cleared", "basecamp", "sync notes")

today = datetime.date.today()
text = open(sys.argv[1], encoding="utf-8").read()

overdue, open_count, skipping = [], 0, False
for line in text.splitlines():
    if line.startswith("## ") or line.startswith("### "):
        head = line.lstrip("# ").lower()
        if line.startswith("## "):
            skipping = any(k in head for k in SKIP)
        continue
    if skipping or not line.startswith("- [ ]"):
        continue
    open_count += 1
    m = re.search(r"(?:was due|due|proposed:)\s*(?:\w{3,9}\s+)?([a-z]{3})[a-z]*\s+(\d{1,2})",
                  line, re.I)
    if not m:
        continue
    mon = MONTHS.get(m.group(1).lower())
    if not mon:
        continue
    when = datetime.date(today.year, mon, int(m.group(2)))
    if when < today:
        label = re.sub(r"\s*\|.*$", "", line[5:]).strip()
        overdue.append(((today - when).days, label))

bits = []
if overdue:
    overdue.sort(reverse=True)
    worst_days, worst_label = overdue[0]
    bits.append(f"{len(overdue)} task(s) past their date — worst is "
                f"\"{worst_label}\" at {worst_days} days.")

stamp = re.search(r"_Last synced:\s*(\d{4})-(\d{2})-(\d{2})", text)
if stamp:
    age = (today - datetime.date(*map(int, stamp.groups()))).days
    if age > 14:
        bits.append(f"TASKS.md was last synced {age} days ago — run a task sync.")

if bits:
    print("TASKS.md: " + " ".join(bits) + f" ({open_count} open in total.) "
          "Mention this in one line, then wait for my request — do not dump the list.")
PYEOF
