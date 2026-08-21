# Project memory: Things 3 → Basecamp completion sync

This is the memory log for this project. It captures progress, decisions, and context specific to this work.

Claude reads this file whenever resuming work on this project. Claude appends to it at the end of each session or when something significant happens.

---

## What belongs here

- **Progress** — What was done, what stage we're at. Example: "Drafted the first three email sequences."
- **Decisions** — Choices made about this project's direction. Example: "Rejected the webinar approach, going with evergreen instead."
- **Blockers** — Things that stopped progress and need resolving. Example: "Waiting on final pricing before completing the sales page."
- **Next steps** — What should happen next time we pick this up. Example: "Write the headline options."
- **Lessons learned** — Insights, workflows, or mistakes worth remembering beyond this project. These get picked up by the System Review and may be promoted to universal memory. Example: "The four-section proposal format (Current state, Problem, Solution, Investment) got great client feedback — worth templating."

## What does not belong here

- Universal decisions that apply across all projects — those go in `ABOUT ME/memory.md`.
- Full drafts or deliverables — those go in the project's `outputs/` folder.

## Format

Each entry follows this pattern:

```
### YYYY-MM-DD — Short title

Category: Progress | Decision | Blocker | Next steps | Lessons learned

[1-3 sentences.]
```

## Rotation rule

When this file exceeds ~150 lines, roll entries older than the current quarter into a sibling `memory-archive-YYYY-QN.md` inside this same project folder (where QN is Q1, Q2, Q3, or Q4). Keep the current and previous quarter live; everything older moves to the archive file. Archive files are reference-only — Claude does not read them unless asked. This keeps the active memory log lean.

---

## Log

### 2026-08-21 — Project created; root cause found and script written

Category: Progress

Hunter asked whether completions in Things 3 could check themselves off in Basecamp. Found that most of the pipeline already existed on his Mac and had never worked, for three reasons: the Things query used `status = 1` when completed is `3`, the queue file was always written `synced: true` so the `CLAUDE.md` gate stayed shut, and remote sessions can't reach either the Basecamp CLI or the Things database but were never told to notice.

Wrote `outputs/things_basecamp_sync.py` — stdlib only, dry-run by default, reads Things directly rather than depending on the old `things-sync.sh`.

### 2026-08-21 — Matching tested against real titles

Category: Progress

Verified the matcher on Hunter's actual Basecamp to-dos. Normalization strips the `Hunter:` prefix and `(45 min)` / `(1 hr)` duration suffixes, which turns three would-be misses into exact matches. The genuinely dangerous pair — "Outline Keeping First Time Guests" vs "Send Keeping First Time Guests… to team" — scores 0.76 against each other, so the right one wins by a clear margin and the wrong one never auto-ticks. "New Rule of Life" vs "Hunter: Rule of Life" lands at 0.86 and correctly queues for review rather than guessing.

### 2026-08-21 — Blocked on a run on the Mac

Category: Blocker

The Things DB read and the `basecamp` CLI calls cannot be tested from a remote session. Next step is Hunter running the dry run: `python3 things_basecamp_sync.py --hours 336`. If the CLI subcommand shape differs from the documented `projects list --json` / `todos list --in` / `todos complete`, the `CMD_*` constants at the top need one edit — the script prints the exact failing command.

### 2026-08-21 — Next steps

Category: Next steps

1. Hunter runs the dry run and pastes the output back.
2. Tighten thresholds if anything under `WOULD COMPLETE` looks wrong.
3. One manual `--apply` run, then the launchd timer (or the one-line addition to `hunter-sync.sh`, which is simpler).
4. Decide on the `CLAUDE.md` step 1 rewrite in outputs.
5. Retire or move aside `~/.claude/things-sync.sh` so two scripts aren't writing the same queue file.

### 2026-08-21 — Fixed a quoted-tilde bug in my own instructions

Category: Lessons learned

The dry-run command I gave Hunter was `python3 "~/Desktop/Hunter Wilson/..."`. Bash only expands a leading tilde when it is unquoted, so that resolves to a literal `~` directory and fails with `can't open file`. Same bug was in the setup doc's `cp` line. Both now use `"$HOME/..."`, which expands inside double quotes while still protecting the spaces in `Hunter Wilson` and `WORK AREAS`. Added a quoting note to the setup doc so it doesn't come back.

When writing shell commands for paths with spaces under the home directory, `"$HOME/path with spaces"` is the only form that gets both halves right.

### 2026-08-21 — Plumbing verified against a synthetic environment

Category: Progress

Couldn't run the script against Hunter's Mac from a remote session, so built the environment instead: `outputs/test_things_basecamp_sync.py` creates a throwaway Things SQLite database and a fake `basecamp` CLI, then runs the real sync against them. 26 checks, all passing.

What this actually proves, beyond reading the code:

- The SQL is right. `status = 3` returns completed rows; `0` (open), `2` (canceled), trashed rows, `type = 2` headings, `----` separators, and null `stopDate` rows are all correctly excluded. The Core Data timestamp math works — a task completed 900h ago falls outside a 336h window, one completed 100h ago falls inside.
- The CLI plumbing is right. Projects and to-dos parse across multiple projects, already-completed to-dos are skipped, and to-dos assigned to someone else are dropped while unassigned ones stay in play.
- `--apply` completes exactly the confident ids and nothing else. The ambiguous "Hunter: Rule of Life" match was never touched.
- Dry run genuinely writes nothing, and `synced` only flips to `true` after a real push.
- A missing Things database fails loudly with a useful message rather than silently returning nothing — which was bug #3 in the original pipeline.

What remains unverified is only what a simulation can't cover: whether his installed `basecamp` CLI uses the documented `projects list --json` / `todos list --in` / `todos complete` shapes, whether auth is still valid, and how his real Things titles compare to his real Basecamp titles. The harness is now step 2 of the setup doc so he can pre-flight on his own machine without touching live data.

### 2026-08-21 — Lesson: build the environment when you can't reach it

Category: Lessons learned

Twice I told Hunter "I can't run this, only you can" — true, but not useful on its own. The better move when a dependency is out of reach is to simulate it and verify everything up to the boundary. That turned "verified logic on unverified plumbing" into a short, specific list of what's genuinely still unknown. Worth reaching for whenever the blocker is environmental rather than logical.

### 2026-08-21 — Python compatibility verified, caveat removed

Category: Progress

Ran the harness in-session: 26/26 pass on Python 3.11. Then closed the version gap rather than leaving it as a warning — `ast.parse(feature_version=...)` confirms both files are valid syntax back to 3.8, and every stdlib call used landed in 3.7 or earlier (`subprocess.run(capture_output=)` 3.7, `sqlite3` URI mode 3.4, `isoformat(timespec=)` 3.6, `os.replace` 3.3). The `from __future__ import annotations` line is what keeps the `list[dict]` annotations legal that far back.

macOS ships 3.9.x, so `/usr/bin/python3` is sufficient. No Homebrew Python, no pip, no dependencies. Replaced the vague "if it fails it's probably your Python version" line in the setup doc with that, so a failure on his machine now means a real bug worth reporting rather than an environment shrug.

### 2026-08-21 — Matching would have silently done nothing; found it before Hunter ran it

Category: Decision

Found `Things3-Setup_Guide_v1.md` sitting on an unmerged branch and scored the matcher against Hunter's real Things project names. Result was bad: **2 of 13 auto-matched, 6 silently dropped.** The sync would have run clean, reported almost nothing, and looked like it was working.

Root cause is structural, not a threshold tuning problem. Things names a project as a noun ("Growth Plan v2"); Basecamp phrases it as an action ("Ship Growth Plan v2 flow with Mark Brewer"). Whole-string similarity scores that pair at 0.51. No threshold change fixes that without also letting garbage through.

Two additions:

1. **Token containment** — if the Things title's words sit inside the Basecamp title, that counts even when the ratio is low. Damped by how much of the Basecamp title got covered, so a short title landing in a long one doesn't score a perfect match. Requires 2+ tokens and 60% containment before it applies.
2. **An `ALIASES` table** for pairs sharing no words at all — `RSG VSL` / `Create a Video Sales Letter` is unbridgeable by any string method. Four seeded from real data. This is the honest answer: some pairs must be declared, not inferred.

After: **8 auto, 5 queued, 0 dropped.** Safety held — the near-identical Keeping First Time Guests pair still separates by 0.24, and generic titles ("Review", "Email", "Call Mark") stay below 0.28. Locked all of it into the regression suite as sections 7–9 so it can't quietly regress.

**Lesson worth keeping:** testing against invented examples proved the code worked and told me nothing about whether it would *do the job*. The synthetic fixtures I wrote used titles that matched too well because I wrote both sides. Hunter's real naming conventions were the actual test, and they were sitting in the repo on an unmerged branch the whole time. Look for the user's real data before trusting a green test suite.

### 2026-08-21 — Three stale branches found; do not merge them

Category: Context

`claude/things3-areas-projects-setup-70n6o8`, `claude/task-list-8HWEF`, and `claude/tasks-endpoint-review-25DAE` are all cut from `ae34624 Initial commit` — ancient parallel forks, not newer work. They carry older versions of `CLAUDE.md`, `about-me.md`, and `TASKS.md`, so merging any of them now would revert current work.

Checked whether they contradict the overdue list: they don't. None of the 10 overdue items is marked complete on any of them. Their completions (editing rounds, podcast briefs, Taki cancellation, Brian Woods email, finance report) are all already in the Done — June cycle archive. One minor discrepancy: `task-list-8HWEF` dates the finance report and Brian Woods email as Jun 3 where `TASKS.md` says Jun 11. Not material to overdue status.

Worth salvaging from `things3-areas-projects-setup`: `WORK AREAS/Admin-PA/Things3-Setup_Guide_v1.md`, which documents the four Areas (RSG — Content, RSG — CEO, NeoWorld, Personal) and the project layout. It's the source of the naming conventions the matcher now handles. Not cherry-picked yet — Hunter's call, since he may have abandoned that branch deliberately.

### 2026-08-21 — Things 3 setup guide cherry-picked; picked the older of two versions on purpose

Category: Decision

Brought `WORK AREAS/Admin-PA/Things3-Setup_Guide_v1.md` onto main from the abandoned `claude/things3-areas-projects-setup-70n6o8` branch. Real cherry-pick of `e9fc445`, not a file copy — that commit touches only this file, so authorship and the original message survived.

**Two versions existed and they disagreed.** A later commit on that branch (`618cf52`) revised the repeating-tasks table: dropped the short-form and newsletter rows, changed coaching call prep from bi-weekly to weekly, and swapped "Read + cycle shaping" for "Book or course". Took the **earlier** version anyway, because `618cf52` also rewrote `about-me.md` to match, and that branch's `about-me.md` predates the six core responsibilities entirely and still lists HOOK → BUILD → PAYOFF as the short-form structure — which HEIT replaced on 2026-06-25. The later guide was consistent with a divergent about-me, not with the live one.

The earlier version lines up with main's `about-me.md`: five short-form per week, bi-weekly coaching call prep alternating with Mark, protected read-and-shape block. That's the one that's true.

Added a dated banner rather than editing his content: the structure holds, the dates ("Wednesday", "June 30", "End of June") don't, and the banner points at `TASKS.md` for live status. Also noted that renaming an Area or project here means checking the sync's `ALIASES` table — the guide and the matcher are now coupled.

### 2026-08-21 — Built a double-clickable runner; Hunter is on iOS

Category: Lessons learned

Confirmed via `list_sessions` that this session's origin is **iOS** and every other session is cloud or bridge, all disconnected. `ListAgents` returns nothing. There is no shell on Hunter's Mac reachable from here, and — more to the point — he has been on his phone this whole time. I spent four exchanges handing him terminal commands he had no way to run.

Built `outputs/Task-Sync_Dry-Run_v1.command` instead. `.command` files are double-clickable in Finder, so when he's next at the Mac it's one action, no typing. It pulls, probes the Basecamp CLI (`--version`, `accounts`, `projects list --json`), runs the harness, runs the dry run, tees everything to `last-dry-run.txt`, and commits that back — so the result returns through git rather than copy-paste. Files arriving via `git pull` aren't Gatekeeper-quarantined, so double-click works without a security prompt.

Tested end-to-end in the container: all four stages run and degrade cleanly where the Mac-only pieces are absent. One false alarm worth recording — the push-back appeared to fail, but that was my own `| head -45` closing the pipe and killing the script early. Verified the staging works when the pipe stays open. Hardened it anyway: it now reports the current branch, pushes that branch rather than assuming main, and says "nothing new to commit" instead of failing silently.

**The lesson:** check *how* the user is connected before prescribing the interface. Session origin was in `list_sessions` the whole time and would have saved four rounds. A phone can't run a terminal command no matter how correct the command is.

### 2026-08-21 — Task sync run; harness still green, still blocked on the Mac

Category: Progress

Ran a task sync from a remote container. Confirmed the queue is genuinely empty (`synced: true`, `completions: []`) rather than assuming it, and re-ran the regression harness — all checks pass, including sections 7–9 that caught the six-silently-dropped bug. So the logic hasn't rotted.

Nothing else moved, because nothing else can from here: no `basecamp` CLI, no Things database, Linux container. Checked for a `last-dry-run.txt` coming back through git — none, so `Task-Sync_Dry-Run_v1.command` has still never been double-clicked.

**The one change worth noting:** that blocker was not on `TASKS.md` at all. The project was blocked, the index didn't list Admin-PA, and the task list didn't carry the action — so the single thing standing between Hunter and a working sync was invisible in all three places he'd look. Added it to `TASKS.md` and added an Admin-PA section to `_active-projects-index.md`.

**Lesson:** a blocker recorded only in a project memory log is not tracked. Memory is where you explain a blocker; the task list is where it gets seen. If the next action lives on someone else's machine, it belongs in `TASKS.md` too.
