# Project brief: Things 3 → Basecamp completion sync

## What is this project?

Make it so that checking a task off in Things 3 automatically checks the matching to-do off in Basecamp, without Hunter touching Basecamp.

## Goal

A script on Hunter's Mac that runs on a schedule, reads what he completed in Things 3, finds the matching Basecamp to-do, and completes it. High-confidence matches complete automatically. Anything ambiguous goes into a queue for Claude to resolve in the next session.

Success looks like: Hunter checks off "Rebuild the GP Google Doc toolkits" in Things, and within the hour it's ticked in Momentum Staff HQ without him opening Basecamp.

## Audience

Internal — Hunter only. Side effects are visible to his team, since Momentum Staff HQ and Emily // Hunter are shared Basecamp projects. That's why wrong matches matter more than missed ones.

## Key constraints

- **Things 3 has no web API.** It's a local SQLite database on the Mac. Nothing that reads Things can run in a remote CoWork session — it has to run on the Mac.
- **Basecamp has no CoWork connector** and none exists in the MCP registry. The mechanism is the official 37signals `basecamp` CLI, already installed at `~/.local/bin/basecamp` and authenticated.
- **One-directional by design.** Things is the source of truth for completion. This does not sync Basecamp completions back into Things, and does not create or delete anything in either system.
- **Never auto-complete on a weak match.** Completing the wrong shared to-do is worse than completing nothing. Ambiguous matches queue for review.
- Dry-run is the default. The script only writes to Basecamp when called with `--apply`.

## Reference material

- Existing pieces already on the Mac: `~/.claude/things-sync.sh`, `~/bin/hunter-sync.sh` + launchd plist (the "Auto-sync" commits in this repo), `~/.local/bin/basecamp`.
- Things DB: `~/Library/Group Containers/JLMPQHK86H.com.culturedcode.ThingsMac/ThingsData-*/Things Database.thingsdatabase/main.sqlite`
- Things schema reference: [things.py database docs](https://thingsapi.github.io/things.py/things/database.html) — `TMTask.status` is 0 incomplete, 2 canceled, **3 completed**.
- Basecamp CLI: [basecamp/basecamp-cli](https://github.com/basecamp/basecamp-cli), [basecamp.com/agents](https://basecamp.com/agents).
- Script: `outputs/things_basecamp_sync.py`
- Proposed replacement for CLAUDE.md step 1: `outputs/CLAUDE-md_Step-1_Proposed-Rewrite.md`

## Status

In progress — script written, untested. Cannot be tested from a remote session; needs one run on the Mac.

---

## Scope extension — 2026-08-21: the import direction

Hunter asked for tasks to flow **from Basecamp into Things 3**. That's the opposite direction from
everything above, and it changes one line of this brief: **"One-directional by design" no longer
holds.** The project now covers both directions. Everything else in the brief still stands.

### What the second direction does

Reads open Basecamp to-dos assigned to Hunter and creates them in Things 3, routed to the matching
Area, tagged `#basecamp`, with the Basecamp due date carried across as a Things deadline and a
`when` date two days earlier.

### Key constraints specific to this direction

- **Things 3 can be written to, just not through SQLite.** The mechanism is the Things URL scheme
  (`things:///json`), driven by `open`. Writing to the database directly is unsupported and would
  risk corrupting it.
- **Adding needs no auth token. Completing does.** `things:///update` requires a token from
  Things → Settings → General. So closing a Things task when its Basecamp to-do is finished is
  opt-in behind `--close-in-things`, off by default.
- **Duplication is the failure mode, not a wrong match.** In the completion direction the danger was
  ticking off the wrong shared to-do. Here it's creating a second copy of a task on every run.
  Defended three ways: a `[bc:id]` marker in the task notes, a persistent link table, and the shared
  matcher — used only on first sight.
- **Default scope is to-dos assigned to Hunter.** Part 9 of the Things 3 guide says team work
  belongs in Basecamp, not Things. Importing only his own to-dos keeps that boundary intact.
  `--include-unassigned` and `--all-assignees` cross it deliberately.
- Dry run is still the default. Nothing is created without `--apply`.

### The link table

`WORK AREAS/Admin-PA/things-basecamp-links.json` maps Basecamp to-do id → Things task uuid. Both
directions read it before falling back to string matching. Every pairing the import settles is one
the completion sync no longer has to guess at, so the fuzzy matching should shrink toward nothing.

### Reference material

- Script: `outputs/basecamp_things_import.py` (imports its matcher from `things_basecamp_sync.py`)
- Harness: `outputs/test_basecamp_things_import.py` — 63 checks
- Setup: `outputs/Basecamp-Things-Import_Setup_v1.md`
- Runner: `outputs/Task-Import_Dry-Run_v1.command`
- Things URL scheme: https://culturedcode.com/things/support/articles/2803573/

### Status

Written and verified against a simulated Mac. Same blocker as the other direction — needs one run on
the real machine.
