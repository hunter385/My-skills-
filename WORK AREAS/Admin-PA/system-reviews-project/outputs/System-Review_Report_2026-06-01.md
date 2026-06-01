# System Health Report — 2026-06-01

## System health score

Strong foundation holding. All six About Me files are substantive. 13 active project folders scaffolded. Real work has now begun, but no real execution sessions captured yet — all project memories are still at "scaffolded" status. Two weeks of use have passed since setup; first real recurring patterns visible. Two high-value gaps found.

---

## System health

### About Me files

| File | Status | Notes |
|------|--------|-------|
| about-me.md | Strong | Active projects section updated 2026-05-31 with all 13 current projects. Identity, voice, tools, terms fully populated. |
| voice-profile.md | Strong | Fingerprint-level depth. Imported from Notion voice doc. No gaps detected. |
| writing-rules.md | Strong | Banned words, anti-AI patterns, communication laws, hard refusals, formatting rules, 8-point test all live. |
| my-context-map.md | Good | All connectors listed. CoWork connectors (Calendar, Gmail, Drive, Notion) documented. No gaps. |
| specialist-routing.md | Strong | 9 RSG content skills + system skills + 5 marketplace plugins registered. Wishlist domains listed. Production flow documented. |
| memory.md | Good | 10 entries, all meaningful (setup + Active Projects interview + Active Projects scaffolding). 159 lines — approaching rotation threshold. |

### CLAUDE.md status

Active and followed. Folder conventions match documented structure. Skill override for setup-cowork is intact. No drift detected.

### Specialist routing

Aligned. All five installed marketplace plugins registered in `ABOUT ME/specialist-routing.md`. The mismatch flagged in the 2026-05-30 review was resolved — Productivity, Marketing, and Cowork Plugin Management plugins registered during that review walkthrough.

Two `.plugin` files in `RESOURCES/PLUGINS/` (personal-assistant.plugin, specialist-sub-agent-builder-v0.8.1.plugin) are reference copies, as clarified. No new mismatches.

### Memory health

10 entries. Date range: 2026-05-30 — 2026-05-31 (2 days). Format correct. `memory.md` is at 159 lines — the rotation threshold is ~150 lines. Technically over. All entries are from Q2 2026, so no rotation is needed yet (only entries older than the current quarter rotate). But it's close — the next entry will push it past 150 and trigger the rotation check.

---

## Patterns found

### Recurring corrections

None from actual use sessions yet. All project memory logs are scaffold-only ("project folder scaffolded, status: not started / in progress"). No session work has been captured in project memories, meaning no correction patterns have accumulated since the last review.

**This is the real finding.** The system is scaffolded but not yet being actively used to capture session work. Project memory logs exist but are not being updated. If this continues, the system loses its value — Claude will start every project session without context from prior sessions.

### Common task types

From universal memory and TASKS.md:

1. **Content production** (podcast batch filming, A-Team Workshop editing, short-form video scripts) — this is the weekly engine. Skills for this are all installed.
2. **NeoWorld operations** (shipping team restructure/gamification, June lead-gen calls, ManyChat setup) — COO-level execution tasks. NeoWorld has no skill coverage.
3. **Framework/curriculum builds** (Growth Plan v2, Middle Method re-recording, VSL) — multi-session projects all under WORK AREAS/RSG/.
4. **Admin / comms tasks** (email Brian Woods, cancel Taki program, get finance report from Laura) — captured in TASKS.md, not in project folders. Appropriate.
5. **Personal rhythms** (Rule of Life, Emily workspace, emotional honesty practice) — three active projects under WORK AREAS/Personal/.

### Missing context

1. **NeoWorld operations lacks a skill or routing rule.** `ABOUT ME/specialist-routing.md` has 9 RSG skills and 5 marketplace plugins but nothing specific to NeoWorld COO work. Six active NeoWorld projects are live. When working on those, Claude falls back to general knowledge — no NeoWorld-specific voice, ops context, or team knowledge is loaded automatically. The `KNOWLEDGE/neoworld_kb/` exists but there's no routing trigger that points COO-work sessions to it.

2. **TASKS.md is the single source of truth for current urgents, but it's not referenced anywhere in the routing rules.** `ABOUT ME/my-context-map.md` doesn't mention TASKS.md. If Hunter starts a session without mentioning tasks, Claude has no instruction to check it. The Productivity plugin exists and owns `/tasks` — but there's no rule saying "check TASKS.md at session start for urgent items."

3. **RSG cycle status is not captured anywhere.** `about-me.md` says RSG runs 6-week cycles. Current cycle started approximately 2026-06-01. But there's no file recording cycle start/end date, current cycle Rocks, or cooldown status. Claude has to infer the cycle from the active projects list, which is an approximation, not the actual cycle definition.

### Cross-project insights

NeoWorld and RSG projects are running in parallel under the same COO/CEO identity, but the system treats them identically. Six NeoWorld projects are scaffolded with no session work captured. NeoWorld has a full KB but it's not triggering automatically on NeoWorld-area work. The two businesses need differentiated defaults — not the same voice profile and content skills being applied to shipping team restructure decisions.

### Stale content

1. `WORK AREAS/Admin-PA/first-week-guide-project/` — the First Week Guide project has a memory log and outputs but appears to have been a setup artifact. If the guide has been delivered and is no longer active, archive it to `WORK AREAS/Admin-PA/_archive/`.

2. `ABOUT ME/memory.md` is at 159 lines. The rotation rule says roll at ~150 lines. All entries are Q2 2026. No rotation needed yet — but flag this: the next significant entry should trigger a rotation check. Entries should roll into `ABOUT ME/memory-archive-2026-Q2.md` once the file meaningfully exceeds 150 lines.

---

## Recommendations

### Critical

None.

### High value

1. **Add NeoWorld routing rule to specialist-routing.md.** File: `/Users/huntergwilson/Desktop/Hunter Wilson/ABOUT ME/specialist-routing.md`. After the "RSG content production flow" section, add:

   ```
   ## NeoWorld routing rule
   
   When working on any project under `WORK AREAS/NeoWorld/`, Claude should:
   1. Read `KNOWLEDGE/neoworld_kb/Wiki/NeoWorld-Overview.md` for business context.
   2. Use NeoWorld voice: operational, COO-level, not pastoral/church-growth.
   3. Do not apply RSG content skills to NeoWorld work.
   ```

   Why it matters: six active NeoWorld projects are live. Without a routing rule, every NeoWorld session starts cold. The KB exists — it just needs a trigger.

2. **Add TASKS.md reference to my-context-map.md.** File: `/Users/huntergwilson/Desktop/Hunter Wilson/ABOUT ME/my-context-map.md`. Under "Key databases or folders to know about," add a row:

   | Location | What's there | When to check it |
   | `WORK AREAS/Admin-PA/TASKS.md` | Current urgent, this-cycle, and ongoing tasks across RSG + NeoWorld + Personal | Check at every session start if Hunter mentions tasks or asks what to work on |

   Why it matters: the Productivity plugin owns task management, but TASKS.md has no guaranteed discovery path without this entry.

### Nice to have

1. **Add RSG cycle tracking file.** Create `WORK AREAS/RSG/current-cycle.md` with a simple template: cycle start, cycle end, 3 Rocks, Cooldown status. Update at cycle start and end. This gives Claude a single source of truth for "what cycle are we in and what matters this cycle" instead of inferring from the scattered projects list.

2. **Archive first-week-guide-project if complete.** If the First Week Guide deliverable has been reviewed and there are no further sessions planned, move to `WORK AREAS/Admin-PA/_archive/`. File path: `/Users/huntergwilson/Desktop/Hunter Wilson/WORK AREAS/Admin-PA/first-week-guide-project/`.

3. **Begin capturing session work in project memories.** This is a behavior prompt, not a system fix. The 13 project memory files are all identical scaffolds. When Hunter works on a project, logging decisions and progress in the project's memory.md is what makes the system compound over time. The infrastructure is there. The habit isn't yet.

---

## Changes applied this review

None — scheduled task, no interactive changes.

## Changes skipped

All recommendations above — awaiting user review.
