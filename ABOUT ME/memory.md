# Memory

This is the universal memory log. It captures decisions, preferences, and context that matter across all projects and sessions.

Claude reads this file at the start of every session. Claude appends to it when something significant happens that future sessions should know about.

---

## What belongs here

- **Decisions** — Choices about how you work, tools you use, approaches you've committed to.
- **Preferences** — Things you've expressed a preference about that aren't captured in other About Me files.
- **System changes** — Updates to the folder structure, installed plugins, or any part of the CoWork setup.
- **Important context** — Facts or background that would be costly to rediscover.

## What does not belong here

- Project-specific progress, decisions, or blockers — those go in the project's own memory log inside `WORK AREAS/[area]/[project-name]-project/`.
- Anything already captured in another About Me file (don't duplicate).
- Minor session details that won't matter next week.

## Format

Each entry follows this pattern:

```
### YYYY-MM-DD — Short title

Category: Decision | Preference | System change | Context

[1-3 sentences describing what happened and why it matters.]
```

## Rotation rule

When this file exceeds ~150 lines, roll entries older than the current quarter into `ABOUT ME/memory-archive-YYYY-QN.md` (where QN is the quarter — Q1, Q2, Q3, or Q4). Keep the current and previous quarter live; everything older moves to the archive file. Archive files are reference-only — Claude does not read them into the session unless asked. This keeps memory.md lean enough to load every session without bloating context.

---

## Log

### 2026-05-31 — Active Projects interview + WORK AREAS restructured into PARA

Category: System change

Ran the scheduled Active Projects interview. Captured 13 active projects across three contexts. Restructured WORK AREAS to reflect the two-business reality:

- Renamed `WORK AREAS/Business/` → `WORK AREAS/RSG/`.
- Created new work area `WORK AREAS/NeoWorld/` (Hunter's COO role with Dillon).
- Scaffolded 13 project folders with `project-brief.md`, `memory.md`, and `outputs/`:
  - **RSG (4):** a-team-workshop, growth-plan-v2 (with Mark Brewer, due before Jun 30), rsg-vsl, middle-method-podcast-batch (filming Thu).
  - **NeoWorld (6):** shipping-team-restructure, shipping-team-gamification, nwu-qr-onepager, brand-deals-review, triangle-model-nw, june-lead-gen-coaching.
  - **Personal (3):** rule-of-life, emotional-honesty-emily, basecamp-emily-workspace.
- Replaced the placeholder on line 95 of `about-me.md` with the active projects list organised by RSG / NeoWorld / Personal.
- Created `WORK AREAS/_active-projects-index.md` as the at-a-glance live view of all active projects.

Hunter's instruction: track all 13 through to end of cycle, not just 2–3. PARA mapping: Work areas = Areas, project folders = Projects, RESOURCES/ = Resources, `_archive/` folders = Archive.

### 2026-05-30 — NeoWorld interview Pass 1+2 captured; neoworld_kb spun up

Category: System change / Context

Hunter clarified NeoWorld is a separate business (he's COO with brother Dillon). Spun up `KNOWLEDGE/neoworld_kb/`, moved 12 NeoWorld files out of rsg_kb. Captured Pass 1 + Pass 2 interview transcripts into `neoworld_kb/Outputs/Hunter-Interview-2026-05-30.md`. Wrote 4 seed wiki articles: NeoWorld-Overview, Monthly-Cycle, NeoWorld-Team, NeoWorld-University.

Key strategic facts captured:
- NeoWorld = Pokemon card streaming + sales on Whatnot. $4.5M projected revenue 2026; stretch $5.5M + ≥$750k profit.
- Team: Dillon (CEO/streamer/buyer), Hunter (COO), Laura Abshere (Ops/CFO), Ian (streamer/buyer/shipping lead). Keela + Nolan no longer on the team — outdated references annotated in RAW.
- Streaming volume: Dillon 35 hrs/wk, Ian 10 hrs/wk = 45 stream-hours/week production capacity.
- Revenue today: 100% auction sales. Growth levers: brand deals + University ($50/mo coaching subscription) + operational efficiency.
- NeoWorld University target customer: aspiring Whatnot streamers in any niche. Promise: become a full-time streamer.

### 2026-05-30 — Cadence-by-context insight captured (about-me.md updated)

Category: Decision / Context

Hunter runs THREE different Cycle cadences in parallel:
- RSG (his own business): 6-week cycles. Content business, weekly publishing rhythm.
- NeoWorld (COO role): monthly cycles. Streaming + inventory market turns over fast.
- What RSG teaches churches: 90-day cycles. Cultural change is slower in church teams.

The Middle Method is cadence-agnostic. Principle stays — pick the longest cycle the market allows, then protect it.

Updated:
- `ABOUT ME/about-me.md` — added the three-cadence picture under "What makes me tick" and added a "My second business — NeoWorld" section.
- `KNOWLEDGE/rsg_kb/Wiki/Middle-Method.md` — added "Cycle length is calibrated to the business, not fixed" section with the three-rhythm table.

This is important — every future framework Hunter builds for RSG vs. NeoWorld vs. church audiences should respect the cadence-by-context principle.

### 2026-05-30 — Three housekeeping resolutions

Category: Decision / System change

- **RSG Magic Model** file (empty) deleted at Hunter's request.
- **The Problem** file turned out to be NeoWorld content, not RSG. Moved to neoworld_kb/RAW/Strategy/.
- **Breaking 500** removed from rsg_kb INDEX — it's a product name in The Five Ones, not a framework.
- **RSG System vs. The System** reconciled: Taki Moore's framework is the upstream source. RSG System is Hunter's build on top. Both kept in INDEX with attribution.

### 2026-05-30 — Obsidian vault imported, three KBs spun up, wiki seeded

Category: System change

Hunter dropped his full Obsidian vault into `KNOWLEDGE/_intake/`. 373 markdown files + ~200 paired images/PDFs triaged into three knowledge bases:

- `KNOWLEDGE/rsg_kb/` — all RSG frameworks (80 markdown + 74 Excalidraw drawings + 157 screenshots), 14 workshop files, 15 program files. Wiki seeded with 9 load-bearing articles (Middle-Method, Growth-Plan, 365, Cycle-Rocks, Weekly-3-Daily-3, Five-Ones, Messy-Middle, Planet-Builder, HOOK-BUILD-PAYOFF-INVITATION, Six-Responsibilities, Ideal-Week). INDEX.md catalogs 60+ frameworks with status tags. QUESTIONS.md flags gaps for future compile passes.
- `KNOWLEDGE/reading_kb/` — 131 Readwise books + 19 articles + 7 tweets + 1 podcast. Wiki layer empty — first compile pass should start with author pages for the reference shelf.
- `KNOWLEDGE/lifeplan_kb/` — 28 personal items (Marriage IGP, Teddy + Charlie, Spirituality, Health, Hobbies, Friends, Finances, Areas, Priorities, Values, North Star, Rhythms, Ideal Week, etc.). PRIVATE by default per CLAUDE.md rule — never surface in public content unless Hunter explicitly asks.

Templates (3), Obsidian Bases (6), Fonts (3), Brand Palette (1) routed to `RESOURCES/TEMPLATES/from-obsidian/` and `RESOURCES/from-obsidian-*/`.

Originals preserved in `KNOWLEDGE/_intake/` — `cp` not `mv`. Intake folder can be cleaned up later after Hunter verifies routing.

### 2026-05-30 — Initial CoWork OS setup completed

Category: System change

Ran the Onboarding Coach end-to-end. All six ABOUT ME files populated: about-me.md, writing-rules.md, voice-profile.md, my-context-map.md, specialist-routing.md, memory.md. Integrated two uploaded source documents — the Notion voice fingerprint (writing laws, communication laws, hard refusals, phrase bank, signature tells, golden examples) and the LifePlan archive (identity, family, internal wiring, 10-year vision, Opus Gloria, replenishment).

### 2026-05-30 — CLAUDE.md cleanup

Category: System change

Removed the PRIORITY ZERO bootstrap block from CLAUDE.md since the four skills are installed and onboarding has run. Skill override block kept intact (still routes future "set up" requests to setup-guide instead of generic setup-cowork).

### 2026-05-30 — Two anchoring truths confirmed as the load-bearing claim set

Category: Context

Every RSG piece should be weight-checked against:
1. You don't need more ideas. You need a system that actually gets your team executing.
2. The problem isn't starting strong. It's not falling apart in the middle.

Use this as the primary alignment check in future content audits and System Reviews.

### 2026-05-30 — Audience tension noted

Category: Context

Hunter currently serves pastors (RSG core business with dad) but his Opus Gloria is "He helped entrepreneurs find a better way to live and run their businesses." 10-year vision is an independent entrepreneur platform alongside Ready Set Grow. Wishlist domain "Entrepreneur-platform positioning" added to specialist-routing.md to keep this on the system's radar.

### 2026-05-30 — Voice profile depth confirmed at fingerprint-level

Category: Decision

Voice-profile.md and writing-rules.md were populated directly from Hunter's uploaded Notion voice fingerprint — already deeper than the standard onboarding flow produces. No further deepening needed. System Review can re-audit if voice drift appears in published content.

### 2026-05-30 — First System Review run; all findings actioned

Category: System change

Ran the first System Review. Headline: strong day-one setup, 0 critical, 2 high-value, 3 nice-to-have. All findings actioned in the walkthrough:

- Added Basecamp row to `ABOUT ME/about-me.md` "My tools and platforms" so the NeoWorld toolstack appears in both about-me.md and my-context-map.md.
- Registered five installed marketplace plugins (Personal Assistant, Specialist Sub-Agent Builder, Productivity, Marketing, Cowork Plugin Management) in `ABOUT ME/specialist-routing.md` Marketplace plugins table. Removed the "Plan to install" note since both originally-planned plugins are now active.
- Archived `WORK AREAS/Marketing/Website-Redesign-Example-project/` to `WORK AREAS/Marketing/_archive/` so it no longer clutters the live Marketing area.
- Scheduled Active Projects interview for 2026-05-31 at 09:00 to fill the placeholder on line 95 of about-me.md.
- Scheduled fortnightly System Review re-run for 2026-06-13 at 09:00 once real-use memory entries have accumulated.

Report marked acknowledged in `_index.md`.

### 2026-06-15 — Ikigai mapping [RETRACTED — misread]

Category: Context

**RETRACTED:** Claude pulled intersection content from a reference/example image, not Hunter's actual words, and built a visual + analysis on that wrong basis. Do not trust the earlier "Profession↔Ikigai gap" read or the synthesized intersections. Hunter is re-uploading his real Ikigai; rebuild only from his exact words. Earlier output files in `WORK AREAS/Personal/ikigai-project/outputs/` are based on the misread and should be replaced, not referenced.

### 2026-06-15 — Ikigai rebuilt from Hunter's real four lists (v2)

Category: Context

Replaced the retracted v1. Built v2 from Hunter's actual Love / Good at / World needs / Paid-for lists, using only his vocabulary. Center / Ikigai statement: "Teach frameworks and build systems that give entrepreneurs clarity and the right strategy for growth — coached through Growth Plan sessions and productized into an incubator with my Middle Method tools." Recurring across all four lists: Frameworks, Systems, Teaching/Coaching, Helping Entrepreneurs, Growth Plan, Strategy for growth, Clarity. Outputs: `WORK AREAS/Personal/ikigai-project/outputs/Hunter-Ikigai_Visual_v2.html` + `_Analysis_v2.md`. Lesson for future work: when a user uploads a reference example alongside their own data, do not pull content from the reference image — confirm which words are theirs.

### 2026-06-15 — Ikigai v3: insight-driven design (nature/purpose/present/path)

Category: Context

Reframed Hunter's four intersections from word-piles into a four-stage narrative he responded strongly to: Passion = your nature (Love×Good-at), Mission = your purpose (Love×World-needs), Profession = your present / "the comfortable trap" (Good-at×Paid), Vocation = your path / "the bridge" (World-needs×Paid). Center: "Productize your frameworks into systems, courses, and an incubator... so the work scales past the room you're standing in." Key breakthroughs that landed: (1) "Church" appears only in the Paid-for list, never in Love or Good-at — the data already favors the entrepreneur direction; question is timing/bridge, not direction. (2) He monetizes delivery (drains him) and gives away invention (his genius). (3) Income requires him in the room; his loves don't — productization is the move. (4) NeoWorld University is proof he can build the leveraged-membership model — he built it for Dillon, not himself. (5) Photography = the one non-monetized item; protect it (Enneagram-3 "would I want this if no one was impressed?"). Output: Hunter-Ikigai_Visual_v3.html. This entrepreneur-platform / productization thesis is a strong anchor for future positioning work.

### 2026-06-25 — HEIT is now the default short-form structure

Category: Decision (system change)

Hunter adopted HEIT (Hook → Explain → Illustrate → Teach) from the Martell Ultimate Content Playbook as the new default per-video structure for all RSG short-form, replacing HOOK → BUILD → PAYOFF → INVITATION. Full playbook (topic four-test, HEIT spine, voice/POV, cadence, metrics, 45-min workflow) translated into RSG voice and saved at `WORK AREAS/RSG/short-form-system-project/outputs/Short-Form-System_Playbook_v1.md`. New project folder created: `WORK AREAS/RSG/short-form-system-project/`. When building short-form going forward, default to HEIT and run the four topic tests first.

**Open conflict:** the `/short-form-engine` skill SKILL.md still hardcodes HOOK → BUILD → PAYOFF → INVITATION and the five archetypes. This playbook overrides it on paper, but the skill will keep generating on the old spine until its SKILL.md is edited in Settings > Capabilities. Decision pending: rewrite the skill around HEIT, or keep it as an archetype-generator feeding HEIT scripts.

### 2026-08-21 — Task sync run; task system had gone 10 weeks stale

Category: System change

Ran a task sync across every task surface in the workspace. `TASKS.md` had not been touched since 2026-06-11 and `_active-projects-index.md` since 2026-05-31, so all urgency labels were wrong. Rebuilt both.

What the sync found:

- **10 tasks overdue**, the worst by 78 days (Outline June Lead Generator Calls, was due Jun 4). Growth Plan v2 is 52 days past its Jun 30 date. Rule of Life and the 3rd Kid conversation are both 56 days over.
- **NWU QR One-Pager** has sat on "waiting on Dillon" for 71 days. That's not waiting anymore.
- **Three untracked open commitments** pulled out of project memory logs: the HEIT / `/short-form-engine` decision (open since Jun 25, still blocking short-form), the ambiguous A-Team Workshop status (work logged Jun 30 after it was ticked done Jun 14), and the unread 2026-07-01 System Review with 5 high-value findings.
- **Duplicate tasks** across the local list and the Basecamp block — Rule of Life and the Emily emotional-honesty item were each tracked twice. Merged.
- **Five NeoWorld projects** are ticked done in `TASKS.md` but their project memory logs contain nothing but the scaffolding entry. The 2026-06-13 System Review already flagged this exact gap ("project memory logs are dead while real work ships"). It hasn't been fixed.

Sync limits worth knowing, because they'll recur every time:

- **Basecamp is not an available *connector*** in this workspace, so remote sessions can't reach it. ⚠️ **Partially wrong as originally written — see the 2026-08-21 correction below.** There IS a mechanism: the official 37signals `basecamp` CLI, installed and authenticated on Hunter's Mac. The "Assigned to Hunter" block in `TASKS.md` is still a manual snapshot from 2026-05-31.
- **Google Calendar** is connected at account level but not enabled in-chat, so `/tasks-with-calendar` cannot do the calendar half of its job.
- **Notion** exposes only a folder-update tool in-session, so the 4 Notion-linked Content Tracking tasks stay unreadable.

Two setup bugs found and flagged, not fixed (both need Hunter's call):

1. **Filename case mismatch.** The PA plugin commands (`/tasks`, `/briefing`, `/eod`), the `tasks-with-calendar` skill, and the scheduled-task recipes all read `WORK AREAS/Admin-PA/tasks.md` lowercase. The real file is `TASKS.md`. Works on macOS, silently returns nothing anywhere case-sensitive.
2. **Missing PA files.** `WORK AREAS/Admin-PA/captains-log/` and `output-log.md` were never created, so `/briefing` and `/eod` have no sources to read. PA setup is half-applied.

Memory rotation checked: file is over 150 lines but every entry is Q2 or Q3 2026, so nothing is old enough to archive yet. First rotation will be due at the start of Q1 2027.

### 2026-08-21 — Dead tasks cleared; only 3 of 10 overdue items were actually dead

Category: Decision

Hunter said clear the dead ones. Worked through all ten overdue items. Three were dead, seven were live work that had just lost its date.

**Cleared as dead** (recorded in `TASKS.md`, not deleted):

1. **Outline June Lead Generator Calls** — the month expired. NeoWorld runs monthly cycles, so a June deliverable in August is two cycles gone. If lead-gen calls still matter it's a fresh task, not a resurrection.
2. **Create a Video Sales Letter** (Basecamp) — duplicate of "Film RSG VSL for YouTube." Kept the RSG one.
3. **Curriculum + workshop items (4 Notion-linked tasks)** — a placeholder with no names, no dates, and unreadable links. A task you can't act on isn't a task. Replaced with a re-pull action.

**The useful principle from this:** almost nothing on that list had genuinely expired. Time-boxed items die when their window closes (the June calls). Duplicates and unworkable placeholders were never alive. Everything else — the Growth Plan v2 chain, the Content Tracking chain, Rule of Life, the 3rd Kid conversation — was real work that looked dead only because it had been undated for ten weeks. Staleness is not death. Default to redating, not killing.

Redated the seven live items against a cycle starting Mon Aug 24, marked **Proposed** so Hunter confirms rather than inherits dates he never set. Sequenced the two dependency chains in order: GP toolkits → cue sheet → Loom films → ship with Mark; Healthy Volunteer Culture → Keeping First Time Guests outline → send to team.

**Flag raised, unresolved:** the RSG VSL is scoped as "following Taki's VSL process," but the Taki program was cancelled and refunded on Jun 1. Confirm the process is still in hand before that project starts, or it'll stall on a missing dependency.

**Not done, needs Hunter's call:** `NeoWorld/june-lead-gen-coaching-project/` is now a dead project folder. Left in place rather than moved to `_archive/`, because rescoping it to the current month is more likely than archiving it.

### 2026-08-21 — CORRECTION: Basecamp does have a mechanism. Three real bugs found instead.

Category: System change

Earlier today I logged that the `things-completions.json` step in `CLAUDE.md` "has no mechanism behind it." That was wrong, and it matters — future sessions would have read it and stopped looking.

**What's actually there.** `.claude/settings.local.json` shows the official 37signals `basecamp` CLI installed at `~/.local/bin/basecamp` and authenticated, with `basecamp todos`, `basecamp todo`, `basecamp todolists`, `basecamp done`, `basecamp projects`, `basecamp people`, `basecamp message`, `basecamp search` all allowlisted. Also `~/.claude/things-sync.sh`, the Things SQLite path, and `~/bin/hunter-sync.sh` + a launchd plist that git-pushes this repo (that's what the "Auto-sync:" commits are). The pipeline was designed and mostly built. It just never worked.

**Three stacked bugs, the first fatal on its own:**

1. **Wrong status code.** The allowlisted Things query used `status = 1` for completed. Things 3 uses `0` incomplete, `2` canceled, **`3` completed** — there is no `1`. The query has returned zero rows every run since June. That's why `completions` has been `[]` in every committed version of the queue file.
2. **Queue always written `synced: true`.** Step 1 only fires when `synced` is `false` and `completions` is non-empty. The gate was shut even if the query had worked.
3. **Capability blindness.** Step 1 needs the CLI and the Mac filesystem. Remote sessions have neither and the wording never told them to notice — so they failed silently rather than saying "can't reach Basecamp from here."

**The lesson worth keeping:** "the connector doesn't exist" is not the same as "the capability doesn't exist." Check `.claude/settings.local.json` before concluding Claude can't do something — the allowlist is a map of what Hunter has already wired up locally, and it's the best record of his real toolchain. I should have read it before making the claim.

**Design decision made:** take the LLM out of the mechanical path. A script on the Mac reads Things, matches, and completes in Basecamp on an hourly timer. Claude only handles matches the script explicitly refuses to guess. Matching is deliberately conservative because Momentum Staff HQ and Emily // Hunter are shared projects — a wrong tick costs more than a missed one. Thresholds: ≥0.90 auto, 0.72–0.90 queued for review, two candidates within 0.05 never guessed.

Built in `WORK AREAS/Admin-PA/things-basecamp-sync-project/`. Matching logic tested against Hunter's real task titles and handles the traps: `(45 min)` suffixes, the `Hunter:` prefix, and the near-identical "Outline / Send Keeping First Time Guests" pair. Untestable from here: the Things DB read and the CLI calls. Needs one dry run on the Mac.

**Open, needs Hunter's decision:** the proposed `CLAUDE.md` step 1 rewrite in that project's outputs. Not applied — it changes every session's startup.
