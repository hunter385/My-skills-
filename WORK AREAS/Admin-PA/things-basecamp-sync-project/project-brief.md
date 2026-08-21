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
