# Project brief: System Reviews

## What is this project?

Ongoing system health reviews and improvement tracking for the CoWork OS workspace.

## Goal

A self-improving feedback loop: monthly (or on-demand) System Review reports that catch setup drift, surface recurring corrections, and propose specific edits the user can approve.

## Audience

Internal — Hunter and the System Review skill.

## Key constraints

- Reports go in `outputs/` using the convention `System-Review_Report_YYYY-MM-DD.md`.
- `_index.md` is the lightweight session-start lookup — never load full report bodies on session start.
- Acknowledged reports older than 30 days move to `_archive/`.

## Reference material

- `RESOURCES/MY SKILLS/system-review.skill`
- `CLAUDE.md` BEFORE EVERY TASK step 6.

## Status

In progress
