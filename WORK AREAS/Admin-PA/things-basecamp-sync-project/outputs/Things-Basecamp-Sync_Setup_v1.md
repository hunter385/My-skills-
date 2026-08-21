# Things 3 → Basecamp sync: setup

Everything here runs on your Mac. None of it can run in a remote CoWork session — that's the whole reason the old rule never fired.

---

## What was actually broken

Three separate problems, stacked. The first one alone was enough to kill it.

**1. The Things query looked for the wrong status code.**

Your allowlisted query was:

```sql
SELECT title FROM TMTask WHERE status = 1 AND trashed = 0 AND stopDate > ...
```

In Things 3, `TMTask.status` is `0` incomplete, `2` canceled, `3` completed. There is no `1`. That query has been returning zero rows every single time it ran — which is why `completions` has been `[]` in every committed version of the queue file since June 9, even though you've obviously been completing tasks.

**2. The queue was always written `synced: true`.**

Step 1 of `CLAUDE.md` only fires when `synced` is `false` **and** `completions` is non-empty. Both committed versions of the file have `synced: true`. Even if the query had worked, the gate was shut.

**3. Half the pipeline can't reach the other half.**

`~/.local/bin/basecamp` and your Things database both live on your Mac. Remote CoWork sessions — like the one that ran this task sync — have neither. So the instruction sat in `CLAUDE.md` describing work that only a local session could possibly do, and never announced the difference.

---

## The fix: take Claude out of the mechanical path

An LLM does not belong in a deterministic sync. The script does the whole job on a timer. Claude only sees the cases where the match is genuinely unclear.

```
Things 3 (local SQLite)
        │
        │  things_basecamp_sync.py --apply     ← runs hourly via launchd
        ├──► exact / near-exact match ──► basecamp todos complete <id>   (done, no human)
        ├──► close but not certain   ──► things-completions.json "ambiguous"  (Claude asks you)
        └──► no Basecamp counterpart ──► logged and ignored (personal tasks)
```

**Matching is conservative on purpose.** Momentum Staff HQ and Emily // Hunter are shared — your team sees what gets ticked. A missed completion costs you ten seconds. A wrong completion costs you trust. So:

- Titles are normalized before comparison: lowercased, `Hunter:` prefix stripped, `(45 min)` / `(1 hr)` suffixes stripped, punctuation flattened.
- **≥ 0.90** similarity → completed automatically.
- **0.72 – 0.90** → queued for you to confirm.
- **Two candidates within 0.05 of each other** → queued, never guessed.
- **Below 0.72** → treated as a Things-only task, left alone.

Tested against your real task titles:

| Things title | Result |
|---|---|
| `Film all tools in Loom for new Growth Plan` | auto-completed, 1.00 |
| `Edit Healthy Volunteer Culture and assets` | auto-completed, 1.00 — duration suffix stripped |
| `3rd Kid: Second Conversation` | auto-completed, 1.00 |
| `Outline Keeping First Time Guests (Engagement Pathway)` | auto-completed, 1.00 — correctly beat the near-identical "Send…" to-do, which scored 0.76 |
| `New Rule of Life` | **queued** at 0.86 vs `Hunter: Rule of Life` — close, not certain |
| `Buy milk` | ignored, no match |

---

## Install

**1. Put the script somewhere stable.**

```bash
mkdir -p ~/.claude/bin
cp "$HOME/Desktop/Hunter Wilson/WORK AREAS/Admin-PA/things-basecamp-sync-project/outputs/things_basecamp_sync.py" ~/.claude/bin/
chmod +x ~/.claude/bin/things_basecamp_sync.py
```

**2. Run the test harness first. It touches nothing real.**

```bash
cd "$HOME/Desktop/Hunter Wilson/WORK AREAS/Admin-PA/things-basecamp-sync-project/outputs"
python3 test_things_basecamp_sync.py
```

This builds a throwaway Things database and a fake Basecamp CLI, then runs the real
sync against them. 26 checks covering the status codes, the completion window, the
trashed/heading/canceled exclusions, assignee filtering, the matching thresholds, and
that `--apply` completes exactly the right ids and nothing else. It should end with
`All checks passed.` and it never reads your real Things data or calls the real CLI.

Python version is not a risk here. Both files parse clean as far back as 3.8, and
every stdlib call used landed in 3.7 or earlier (`subprocess.run(capture_output=)`,
`sqlite3` URI mode, `isoformat(timespec=)`, `os.replace`). macOS ships 3.9.x, so
`/usr/bin/python3` is enough — no Homebrew Python, no pip installs, no dependencies.

If it fails anyway, paste the traceback. That's a real bug, not an environment gap.

**3. Confirm the Basecamp CLI still answers.**

```bash
~/.local/bin/basecamp accounts
~/.local/bin/basecamp projects list --json | head -40
```

If `projects list --json` isn't the right shape for your installed version, fix the `CMD_PROJECTS` / `CMD_TODOS` / `CMD_COMPLETE` constants at the top of the script. It prints the exact command it tried when one fails, so you'll see precisely what to change.

> **Quoting note.** Use `"$HOME/..."`, not `"~/..."`. Bash only expands a tilde when it's
> unquoted, so `python3 "~/Desktop/..."` looks for a directory literally named `~` and fails
> with `can't open file`. `$HOME` expands inside double quotes and the quotes keep the spaces
> in `Hunter Wilson` and `WORK AREAS` safe.

**4. Dry run first. Do not skip this.**

```bash
python3 ~/.claude/bin/things_basecamp_sync.py --hours 336
```

Two weeks of lookback, nothing written. Read every line. `WOULD COMPLETE` is what it intends to tick; `NEEDS A CALL` is what it's unsure about. If anything under `WOULD COMPLETE` looks wrong, tell me and I'll tighten the matching before you go live.

**5. Go live once, by hand.**

```bash
python3 ~/.claude/bin/things_basecamp_sync.py --hours 336 --apply
```

**6. Then put it on a timer.**

Save as `~/Library/LaunchAgents/com.hunter.things-basecamp-sync.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.hunter.things-basecamp-sync</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>/Users/huntergwilson/.claude/bin/things_basecamp_sync.py</string>
    <string>--hours</string>
    <string>6</string>
    <string>--apply</string>
  </array>
  <key>StartInterval</key>
  <integer>3600</integer>
  <key>RunAtLoad</key>
  <false/>
  <key>StandardOutPath</key>
  <string>/Users/huntergwilson/.claude/things-basecamp-sync.out</string>
  <key>StandardErrorPath</key>
  <string>/Users/huntergwilson/.claude/things-basecamp-sync.err</string>
</dict>
</plist>
```

```bash
launchctl load ~/Library/LaunchAgents/com.hunter.things-basecamp-sync.plist
launchctl list | grep things-basecamp
```

Hourly, six-hour lookback. The overlap is deliberate — a to-do already completed in Basecamp is skipped, so re-covering the same window is harmless and means a missed run self-heals on the next one.

---

## One ordering detail

Your `hunter-sync.sh` launchd job git-pushes this repo (those `Auto-sync:` commits). The queue file lives inside the repo, so **the Things sync should run before the git push**, or remote CoWork sessions see a stale queue. Either give this job an earlier `StartInterval` offset, or simpler: add this line to the top of `hunter-sync.sh`:

```bash
/usr/bin/python3 "$HOME/.claude/bin/things_basecamp_sync.py" --hours 6 --apply || true
```

`|| true` so a Basecamp hiccup never blocks your git backup. Do that and you can skip the separate plist entirely.

---

## Reconcile with what's already there

You have `~/.claude/things-sync.sh` from an earlier attempt. This script doesn't call it and doesn't need it — it reads Things directly. Once the new one is running, either delete the old script or move it aside so two things aren't writing the same queue file. I couldn't read it from here to tell you which parts are worth keeping.

## Sources

- [things.py database docs](https://thingsapi.github.io/things.py/things/database.html) — the `TMTask.status` values
- [basecamp/basecamp-cli](https://github.com/basecamp/basecamp-cli) and [basecamp.com/agents](https://basecamp.com/agents) — the official CLI
