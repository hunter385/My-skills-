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
