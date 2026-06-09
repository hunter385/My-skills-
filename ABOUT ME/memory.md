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

### 2026-06-09 — RSG core responsibilities updated

Category: Decision

Hunter updated his RSG core responsibilities from 6 to 4. Removed: short-form videos (5/week), newsletter (weekly), CEO duties as a listed item. Changed: coaching call prep is now weekly (was bi-weekly). Renamed: "Read and shape the next cycle" → "Book or course — weekly." Updated `ABOUT ME/about-me.md` and `WORK AREAS/Admin-PA/Things3-Setup_Guide_v1.md` to reflect the new list.
