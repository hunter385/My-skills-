# Specialist routing

Specialist domain knowledge is delivered through skills and plugins. Each skill has a description that triggers automatically based on the request — no manual setup required.

This file tracks which domains are covered and which are on the wishlist.

---

## How it works

1. Installed skills and plugins have descriptions that auto-match against requests.
2. When a match is found, the skill loads its domain knowledge and working method.
3. If the task also relates to a live project in `WORK AREAS/`, Claude reads that project folder too.
4. If the task involves a content type with a matching template in `RESOURCES/TEMPLATES/`, Claude studies that template.
5. If no skill matches, Claude works from the About Me files, voice profile, writing rules, and general knowledge.

**What if two skills could match?** Claude picks the one that best fits the specific request. I can override by saying "use [skill name] for this."

---

## Installed RSG content skills

These are the skills I've built for Ready Set Grow. They cover the full content production stack — from raw idea to camera-ready / room-ready output.

| Skill | Domain | Triggers on |
|-------|--------|-------------|
| `/framework-architect` | Framework design | Turning raw insights, patterns, or half-formed ideas into clean, teachable RSG frameworks. Upstream of all execution. |
| `/idea-audit` | Idea pressure-testing | Auditing any new framework, content series, offer, or workshop idea across six dimensions before I invest time building it. |
| `/messy-middle-test` | Framework stress-testing | Six-part diagnostic on a completed framework: Week 1 friction, Week 4 drift, urgency hijack, new idea disruption, role clarity gap, readiness rating. |
| `/framework-visualizer` | Visual design | Turning a finished framework into a rendered teaching visual (Lilita One typeface, reMarkable-style layout, downloadable HTML). |
| `/workshop-builder` | Live workshop curriculum | Turning a finished framework into a complete workshop — hook, teaching script, live application worksheet, slide outline, facilitator notes. |
| `/podcast-brief` | Podcast episodes | Complete brief for a podcast episode — arc, reframe, framework, close — so I can teach from a drawing, not a manuscript. Run once per episode before filming. |
| `/short-form-engine` | Short-form video scripts | Turn one core idea into five short-form video scripts for the week (Instagram + YouTube) using the five video archetypes. |
| `/email-architect` | Weekly newsletter | One newsletter to Breaking 1000 pastors. Always produces 3 subject lines, full formatted email, and a reply prompt. |
| `/coaching-call-prep` | Group coaching call segment | My segment for the week's RSG group coaching call — hook, tension build, framework, live application, close, coaching triggers, banter note. |

---

## NeoWorld routing rule

When working on any project under `WORK AREAS/NeoWorld/`, Claude should:
1. Read `KNOWLEDGE/neoworld_kb/Wiki/NeoWorld-Overview.md` for business context.
2. Use NeoWorld voice: operational, COO-level, not pastoral/church-growth.
3. Do not apply RSG content skills to NeoWorld work.

---

## RSG content production flow

This is how the skills fan out across the production stack. Use this to know which skill runs upstream of which.

**Idea pipeline**

```
Raw insight → /idea-audit → /framework-architect → /messy-middle-test → /framework-visualizer
```

**Live workshop**

```
Framework (built above) → /workshop-builder
```

**Podcast episode**

```
Episode topic → /podcast-brief → film
```

**Short-form (weekly)**

```
One core idea → /short-form-engine → five scripts → film
```

**Newsletter (weekly)**

```
Topic or framework → /email-architect → send
```

**Coaching call (weekly, alternating weeks)**

```
Framework or teaching point → /coaching-call-prep → deliver
```

---

## CoWork OS system skills

These ship with CoWork OS and run system maintenance.

| Skill | Domain | Triggers on |
|-------|--------|-------------|
| `setup-guide` | Onboarding & setup review | "Set up my system", "review my setup", "update my writing rules." |
| `system-review` | System self-improvement | "Review my system", "system health check", monthly scheduled task. |
| `first-week-guide` | First-week learning path | "First week guide", "day 1–5." |
| `knowledge-base-health-check` | KB audit | "Run a health check", "audit the [name] KB", monthly scheduled task. |
| `schedule` | Scheduled tasks | "Every morning…", "weekly…", "remind me to…" |

---

## Built-in capability skills

| Skill | Domain | Triggers on |
|-------|--------|-------------|
| `docx` | Word documents | Creating, reading, editing .docx files. |
| `pptx` | Presentations | Slide decks, pitch decks, .pptx workflows. |
| `xlsx` | Spreadsheets | Excel, CSVs, data tables. |
| `pdf` | PDFs | Reading, creating, splitting, merging PDFs. |
| `deep-research` | Multi-source research reports | Deep, fact-checked research with citations. |

---

## Domains I want covered (wishlist)

Areas where I'd benefit from specialist help beyond what's already installed.

| Domain | What I'd want help with |
|--------|-------------------------|
| Entrepreneur-platform positioning | Translating RSG frameworks for an entrepreneur audience (the 10-year vision audience pivot). |
| Naming & offer architecture | Donald Miller / Strategic Coach style outcome-first naming for new programs and digital products. |
| Sales / pitch language | Founder-story builder, transformation-list builder, pitch practice. (Overcoming imposter syndrome around sales.) |
| Replenishment / personal systems | Building the Replenishment Cycle (Physical / Intellectual / Emotional / Spiritual) into a sticky weekly rhythm. |
| Family rhythm design | Sacred family rhythms — weekly date nights, monthly one-on-ones with the boys, creative adventures. |

If a Better Creating marketplace plugin matches one of these later, install it. Otherwise, the Specialist Sub-Agent Builder can spin up a custom one when ready.

---

## Marketplace plugins installed

Update this as marketplace plugins get installed.

| Plugin | Domain | Triggers on |
|--------|--------|-------------|
| Personal Assistant | Captain's log, task tracking, contact register, daily briefing, end-of-day summary | `/briefing`, `/eod`, `/log`, `/tasks`, `/tidy`, "what's on my plate", "morning briefing", "end of day", "organize my [folder]" |
| Specialist Sub-Agent Builder | Building custom specialist sub-agents with their own knowledge bases | "build a specialist", "create a sub-agent", "make a plugin with a knowledge base", "turn my expertise into an AI assistant" |
| Productivity | Two-tier memory + simple task management (CLAUDE.md working memory, memory/ knowledge base, TASKS.md) | `/start`, `/update`, decoding nicknames/acronyms/project codenames in todos |
| Marketing | Brand review, campaign plans, competitive briefs, content drafting, email sequences, performance reports, SEO audits | "review this against brand voice", "draft a campaign plan", "competitive brief", "write a newsletter", "build an email sequence", "SEO audit" |
| Cowork Plugin Management | Customising and creating CoWork plugins | "customize plugin", "create a plugin", "build a plugin", "tailor plugin to my workflow" |
