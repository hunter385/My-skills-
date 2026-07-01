# System Health Report — 2026-07-01

## System health score

Setup is still strong. Execution is still leaking — and now it's leaking in a new place.

All six About Me files hold. CLAUDE.md is active. But two high-value fixes from the last review never got applied, and this run found two fresh ones: a due date that passed in silence, and a skill that's now running on the wrong script. Same root cause every time — starts clean, drifts in the middle, nobody circles back. 0 critical, 5 high value, 5 nice to have.

### About Me files

| File | Status | Notes |
|------|--------|-------|
| about-me.md | Strong | No placeholders. Active projects section still lists relative dates ("Due Wednesday," "Filming Thursday") from the 2026-05-31 interview — now a month stale. Not a placeholder issue, just worth a refresh next time projects change. |
| voice-profile.md | Strong | Unchanged, fingerprint-level. |
| writing-rules.md | Strong | Unchanged, full banned-word list and 8-point test live. |
| my-context-map.md | Strong | Two stale folder references carried over from last two reviews — see Nice to have. |
| specialist-routing.md | Strong | `/short-form-engine` row now contradicts the HEIT decision — see High value. |
| memory.md | Good | 184 lines. Third straight review over the ~150-line trigger. Never rotated. |

### CLAUDE.md status

Active. Root `CLAUDE.md` is 137 lines — well under 200, no length action needed. No `.claude/CLAUDE.md` override, only `.claude/settings.local.json`. Evidence of active use: outputs are landing in the right `outputs/` folders with correct naming (e.g. `A-Team-Staff-Finds-Fixes-Problems_Why-Builder_v1.md`), and three project memory logs (`a-team-workshop-project`, `growth-plan-v2-project`, `short-form-system-project`) show real session entries, not just scaffolding.

### Specialist routing

Aligned, with one drift. `RESOURCES/PLUGINS/` holds 2 `.plugin` files (Personal Assistant, Specialist Sub-Agent Builder); `specialist-routing.md`'s Marketplace table lists 5 (also Productivity, Marketing, Cowork Plugin Management). Confirmed for the second review running — those three are active plugins without saved reference copies, not a real mismatch. The new drift: `specialist-routing.md`'s `/short-form-engine` row still describes "the five video archetypes" structure, but `WORK AREAS/RSG/short-form-system-project/memory.md` (2026-06-25) shows Hunter replaced that structure with HEIT. The routing file is now describing a retired process.

### Memory health

Active, not empty — but uneven. `ABOUT ME/memory.md`: 16 entries, 2026-05-30 to 2026-06-25, 184 lines. Of 16 project memory logs checked, 3 have real session content (`a-team-workshop-project`, `growth-plan-v2-project`, `short-form-system-project`); 11 still show only their original 2026-05-31 scaffolding line despite work happening against them in `WORK AREAS/Admin-PA/TASKS.md`.

## Patterns found

### Recurring corrections

1. **Project-memory capture still isn't happening, second review running.** The 2026-06-13 report recommended a CLAUDE.md rule tying task completion to memory logging. It was never added. Evidence unchanged and worse: `WORK AREAS/Admin-PA/TASKS.md` marks Shipping Team Restructure, Shipping Team Gamification, Brand Deals Review, and Triangle Model all "Done 2026-06-11" — all four project memory logs still read "Status: Not started," dated 2026-05-31. See High value #1.
2. **`_active-projects-index.md` staleness, second review running.** Flagged 2026-06-13, not fixed. Still dated "Last updated: 2026-05-31," still lists four NeoWorld projects as "Not started" that TASKS.md shows done. See High value #2.

### Common task types

1. **NeoWorld COO execution** — highest completion rate of any area per TASKS.md (4+ items done Jun 11), lowest memory capture rate (0 of 6 project logs updated). System is well-built for this; the habit isn't landing.
2. **RSG framework-to-teaching production** — A-Team Workshop shows the full pipeline working as designed: `/framework-architect` → `/coaching-call-prep`, six real entries between 2026-06-30, framework name still open ("OPEN DECISION" appears in 3 of 4 entries). This is the one project where the system is working end to end.
3. **Branded document builds** — Growth Plan v2's HTML playbook (2026-06-09) hit a real tool limit: Drive MCP can't style a live Google Doc, so the team built a standalone HTML file instead. Useful lesson, not yet captured anywhere future sessions would see it before hitting the same wall.
4. **Admin one-offs** (Brian Woods email, Taki cancellation, finance report) — correctly living in TASKS.md, not cluttering project folders. Working as designed.

### Missing context

1. **HEIT vs. `/short-form-engine`, open 6 days.** `WORK AREAS/RSG/short-form-system-project/memory.md` (2026-06-25) flags that the skill still hardcodes the old HOOK → BUILD → PAYOFF → INVITATION structure and five archetypes, while the playbook it's supposed to feed now runs on HEIT. No decision has been logged since. See High value #5.
2. **Drive MCP limitation still uncaptured.** Same gap flagged 2026-06-13. Source: `WORK AREAS/RSG/growth-plan-v2-project/memory.md`, 2026-06-09. See Nice to have #3.

### Cross-project insights

The gap between "task done" and "memory written" is now visible in two places at once, not one. Last review it was contained to NeoWorld. This review it also shows up in Personal (`basecamp-emily-workspace-project` marked "Not started" in the index despite TASKS.md showing it "Done 2026-06-01"). The lesson from 2026-06-13 — checked box, no memory entry, system learns nothing — is spreading rather than closing. Meanwhile A-Team Workshop proves the opposite is possible when the habit is followed: six dated entries, clear open decisions, a usable trail. That's the model to copy everywhere else.

### Stale content

1. `ABOUT ME/memory.md` — 184 lines, third review over the ~150 trigger.
2. `ABOUT ME/my-context-map.md` — still references `WORK AREAS/Business/` (renamed to RSG on 2026-05-31) and lists `WORK AREAS/Marketing/` as active content storage when it now holds only an archived example project.
3. `WORK AREAS/Admin-PA/first-week-guide-project/` — no activity since 2026-05-31, second review flagging it unconfirmed.
4. `WORK AREAS/Admin-PA/TASKS.md` — "_Last updated: 2026-06-11_" while at least 5 dated items (Jun 4, Jun 15, Jun 17 x2, Jun 26) are unchecked and past due.

## Recommendations

### Critical

None.

### High value

1. **Make memory capture ride on task completion, not a separate habit.** File: `CLAUDE.md`, "AFTER EVERY TASK" section. Current text: "Log anything significant to the appropriate memory file. This is not optional." Add: "When a task is checked off in `WORK AREAS/Admin-PA/TASKS.md`, write the matching entry in that project's own `memory.md` in the same session. A checked box with no memory entry means the system logged nothing." Rationale: this exact fix was recommended 2026-06-13 and skipped. The evidence has only grown — 4 NeoWorld projects and 1 Personal project are marked done in TASKS.md with zero trace in their own memory logs. This is the messy-middle failure Hunter teaches against, running inside his own system.

2. **Refresh `_active-projects-index.md` to match TASKS.md.** File: `WORK AREAS/_active-projects-index.md`. Before: "Last updated: 2026-05-31" with Shipping Team Restructure, Shipping Team Gamification, Brand Deals Review, Triangle Model, and Basecamp Workspace with Emily all listed "Not started." After: mark each "Done" (or move to `_archive/` if fully closed) and update the header to "Last updated: 2026-07-01." Rationale: second consecutive review flagging this. It's the one-screen source of truth and it's been wrong for a month.

3. **Reconcile `TASKS.md` — it hasn't been touched in three weeks.** File: `WORK AREAS/Admin-PA/TASKS.md`. Evidence: footer reads "_Last updated: 2026-06-11_" (line 79); "Outline June Lead Generator Calls | NeoWorld | Due Jun 4 ⚠️" still unchecked 27 days later; four Basecamp-synced items (Jun 15, Jun 17 x2, Jun 26 due dates) also still unchecked. Action: run a status pass — check off what's done, flag what's blocked, update the date stamp to 2026-07-01. Rationale: a task tracker that's 3 weeks behind isn't tracking anything. It's a snapshot of a moment that's already passed.

4. **Growth Plan v2 hit its due date with no status update.** File: `WORK AREAS/RSG/growth-plan-v2-project/memory.md` and `WORK AREAS/Admin-PA/TASKS.md` (line 26: "- [ ] Ship Growth Plan v2 flow with Mark Brewer | RSG | Due Jun 30"). Last memory entry is 2026-06-09 (the branded HTML build); nothing logged since, and the due date (Jun 30) is now one day past. Action: log whether it shipped, slipped, or is blocked, and update the TASKS.md line accordingly. Rationale: this is a Mark Brewer co-build with a hard date — the kind of commitment that shouldn't go dark exactly when it's due.

5. **Resolve the HEIT vs. `/short-form-engine` conflict before it produces the wrong output.** File: `ABOUT ME/specialist-routing.md`. Before: "`/short-form-engine` | Short-form video scripts | Turn one core idea into five short-form video scripts for the week (Instagram + YouTube) using the five video archetypes." After (once decided): either rewrite the skill's SKILL.md around HEIT, or update this row to read "...using the five video archetypes, scripted on the HEIT spine (Hook → Explain → Illustrate → Teach) per `WORK AREAS/RSG/short-form-system-project/outputs/Short-Form-System_Playbook_v1.md`." Rationale: flagged as a blocker in `short-form-system-project/memory.md` on 2026-06-25 and still open 6 days later. Every short-form script run through the skill in the meantime risks shipping on the retired structure.

### Nice to have

1. **Rotate `ABOUT ME/memory.md`.** File: `ABOUT ME/memory.md` (184 lines). Move the 2026-05-30 setup-day entries (there are 8) into `ABOUT ME/memory-archive-2026-Q2.md`, keep 2026-05-31 onward live. Third review flagging this — it's a small edit that's been deferred twice.

2. **Fix two stale folder references in `my-context-map.md`.** File: `ABOUT ME/my-context-map.md`. Before (line 60): "| WORK AREAS/Business/ | RSG strategy, offer design, program builds | Business-side projects |". After: "| WORK AREAS/RSG/ | RSG strategy, offer design, program builds | Business-side projects |" (renamed 2026-05-31 per `ABOUT ME/memory.md`). Also update the Marketing row (line 59) to note it currently holds only an archived example project, not active content.

3. **Document the Drive MCP styling limit.** File: `ABOUT ME/my-context-map.md`, under the Google Drive connector row. Add: "Drive connector can't apply styling to a live Google Doc. For branded/printable output, build a standalone HTML file instead." Source: `WORK AREAS/RSG/growth-plan-v2-project/memory.md`, 2026-06-09. Second review flagging this — it already cost one project a rebuild; codify it before it costs another.

4. **Confirm and close `first-week-guide-project`.** File: `WORK AREAS/Admin-PA/first-week-guide-project/`. No activity since 2026-05-31. If it's done, move it to `WORK AREAS/Admin-PA/_archive/`. Second review flagging it unconfirmed.

5. **Clear the System Review backlog.** File: `WORK AREAS/Admin-PA/system-reviews-project/_index.md`. Two prior reports (2026-06-01, 2026-06-13) are still marked "unread," carrying 10 unactioned recommendations between them. Worth one sit-down session to walk through both before a fourth review stacks on top.

## Changes applied this review

None — scheduled run.

## Changes skipped

None — scheduled run, awaiting review.
