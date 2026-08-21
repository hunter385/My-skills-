# SessionStart hook: salvage report

**Verdict: the idea is worth keeping. The implementation isn't.**

> **INSTALLED 2026-08-21.** Live at `.claude/hooks/session-start.sh`, registered in
> `.claude/settings.json`. It takes effect on the **next** session — hooks load at startup, so the
> session that installed it isn't running it. The copy in this folder
> (`Session-Start-Hook_Script_v1.sh`) is a reference backup; edit the one in `.claude/hooks/`, that's
> the one that runs.

---

## What was on the branch

`claude/tasks-endpoint-review-25DAE` (2026-06-01) had `.claude/hooks/session-start.sh` plus a
`.claude/settings.json` registering it. It fired on fresh startup and asked Claude to print the full
tasks report before your first request.

I ran it. Three problems, in order of severity.

**1. It hardcoded a path that doesn't exist on your Mac.**

```bash
TASKS_FILE="/home/user/My-skills-/WORK AREAS/Admin-PA/TASKS.md"
```

That's a remote container path. On your Mac the file check fails, the hook writes a warning to
stderr, and exits 0. **It has only ever worked in remote sessions.** Same class of bug as the
Basecamp instruction — written against the wrong environment, failing quietly.

**2. Its output format isn't in the spec.**

It emits `{"type":"user","content":"SESSION_START: ..."}`. The documented SessionStart contract
covers `{"async": true, ...}` for background mode and plain stdout for context; that shape is not
part of it. I verified the hook emits the string, but I could not verify from a remote session that
Claude Code interprets it as a prompt injection. Treat it as unproven.

**3. Dumping the full list every startup fights your own rules.**

`CLAUDE.md` says don't give you a wall of text. You already have `/morning` for a styled brief and
`/briefing` from the PA plugin. A forced full report on every session — including sessions you opened
to do something unrelated — is noise you'd learn to skip past.

**Do not cherry-pick either commit.** `e057cb4` also carries an old `.claude/settings.local.json`
with 55 allowlist entries against main's 91. Taking it reverts 36 permissions.

---

## What the rewrite does instead

The genuinely good idea buried in there: a hook is **deterministic**, where `CLAUDE.md` instructions
are advisory. Your task list rotted for ten weeks because nothing forced the staleness into view.
That's worth fixing — but with one line, not a report.

Three changes:

- **`$CLAUDE_PROJECT_DIR` instead of a hardcoded path**, falling back to `pwd`. Works on the Mac and
  in remote containers with no edits.
- **Plain stdout**, not the undocumented JSON shape.
- **Silence unless something is actually wrong.** It speaks only when a task is past its date or the
  file hasn't been synced in over two weeks, and it explicitly tells Claude to mention it in one line
  rather than dump the list.

It also skips parked and archived sections, so Future Ideas and the Done archive never inflate the
count.

### Tested output

Against a `TASKS.md` in the state yours was in this morning:

```
TASKS.md: 2 task(s) past their date — worst is "Outline June Lead Generator Calls" at 78 days.
TASKS.md was last synced 71 days ago — run a task sync. (4 open in total.) Mention this in one
line, then wait for my request — do not dump the list.
```

Against `TASKS.md` as it stands now: **nothing.** Every date is in the future and the sync stamp is
today, so there's nothing to say and it says nothing. That's the behavior you want — it only ever
speaks when it has news.

Verified: silent on `resume` and `compact`, silent when the file is missing (no stderr noise),
correct with and without `$CLAUDE_PROJECT_DIR` set, and parked/archived sections excluded from both
counts.

---

## Verifying it works

Pull, then run it by hand:

```bash
cd "$HOME/Desktop/Hunter Wilson"
git pull origin main
echo '{"source":"startup"}' | CLAUDE_PROJECT_DIR="$PWD" .claude/hooks/session-start.sh
```

**Expect silence.** Every date in `TASKS.md` is currently in the future and the sync stamp is today,
so it has nothing to report. Silence is the hook working, not the hook broken.

To watch it actually fire, run it against a backdated copy — this leaves your real file alone:

```bash
T=$(mktemp -d); mkdir -p "$T/WORK AREAS/Admin-PA"
sed -e 's/Proposed: Wed Aug 26/Proposed: Wed Aug 12/' \
    -e 's/_Last synced: 2026-08-21/_Last synced: 2026-07-15/' \
    "WORK AREAS/Admin-PA/TASKS.md" > "$T/WORK AREAS/Admin-PA/TASKS.md"
echo '{"source":"startup"}' | CLAUDE_PROJECT_DIR="$T" .claude/hooks/session-start.sh
```

That printed, when I ran it here:

```
TASKS.md: 1 task(s) past their date — worst is "Rebuild the GP Google Doc toolkits and send to
Mark and Emily" at 9 days. TASKS.md was last synced 37 days ago — run a task sync. (15 open in
total.) Mention this in one line, then wait for my request — do not dump the list.
```

Note the count: **15 open**, not the 22 raw `- [ ]` lines in the file. Future Ideas and the Done
archive are correctly excluded.

## Turning it off

Delete the `hooks` block from `.claude/settings.json`, or rename the script. The hook file alone does
nothing — registration is what activates it.

**One caveat I can't clear from here:** whether a hook registered in `.claude/settings.json` runs in
the CoWork desktop app the same way it does in Claude Code. If you install it and see nothing on a
fresh session even with a backdated task, that's the likely reason — tell me and I'll find another
way to force the check.
