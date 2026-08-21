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
