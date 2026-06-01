# KNOWLEDGE

This folder is your local second brain. It contains one or more knowledge bases — each focused on a specific topic — that get smarter the longer you use them.

The system is based on Andrej Karpathy's LLM Knowledge Base pattern, adapted to run locally with Claude as the librarian. Drop sources into a KB's `RAW/` folder; Claude reads them, distils them into linked articles in `Wiki/`, and answers questions against the corpus with full source provenance.

## How a knowledge base is structured

Each knowledge base is a folder. The bundled example is `eg_productivity_kb/` — the `eg_` prefix marks it as the example you can keep, customise, or replace. KBs you create yourself follow the convention `[topic]_kb` — lowercase, snake_case, ending in `_kb`. For example: `ai_research_kb`, `business_systems_kb`, `theatre_kb`.

Inside each KB:

```
[topic]_kb/
├── CLAUDE.md       — operating instructions for this specific KB
├── RAW/            — unprocessed source material (verbatim, never edited)
│   └── _INGESTED.md — registry of every source in RAW
├── Wiki/           — the librarian's compiled, cross-linked knowledge
│   ├── INDEX.md
│   ├── QUESTIONS.md — open threads, gaps, held tensions
│   └── *.md        — wiki articles
├── Outputs/        — generated answers, reports, charts
└── CHANGELOG.md    — running log; top entry = current state
```

Knowledge bases are independent. Each has its own focus, sources, and rules. They don't share data unless you explicitly cross-reference them.

## How the system works

- **RAW** is the dump zone. You drop articles, papers, transcripts, screenshots, and links here. Verbatim only — never summarised.
- **Wiki** is the librarian's domain. Claude reads RAW, compiles concept articles, maintains backlinks and indexes. You rarely edit Wiki files directly.
- **Outputs** is where queries land. Reports, answers, charts. Promising outputs get filed back into the Wiki to make it smarter over time.

## Creating a new knowledge base

The canonical template lives at `_KB_CLAUDE_TEMPLATE.md` in this folder. Every new KB starts from a copy of that file.

When you ask the librarian to spin up a new KB, it should:

1. Confirm the KB name (use `[topic]_kb` format, lowercase, snake_case) and the focus areas.
2. Create the folder `KNOWLEDGE/[topic]_kb/` with three subfolders: `RAW/`, `Wiki/`, `Outputs/`.
3. Copy `_KB_CLAUDE_TEMPLATE.md` into the new KB's root and rename it to `CLAUDE.md`. Replace the placeholder sections (KB name, "What This Is", "Focus Areas") with content specific to the new KB. Leave the rest as-is.
4. Create empty `CHANGELOG.md` at the new KB's root, `RAW/_INGESTED.md`, `Wiki/INDEX.md`, and `Wiki/QUESTIONS.md`.
5. If this is the first KB in the workspace, offer to set up the monthly health check scheduled task. If you accept, the librarian uses the setup section near the bottom of the `knowledge-base-health-check-skill` body, passing the prompt and cron to Cowork's built-in `schedule` skill. Only one task is needed across all KBs — it audits every KB on each run, so this only happens once per workspace.

## Verbatim-only RAW ingestion

When material lands in a KB's `RAW/` folder, the librarian preserves it word-for-word. RAW is for unprocessed source material. Never summarise, paraphrase, condense, or reword on ingest. Distillation happens at the Wiki layer.

Required frontmatter in every RAW file:

```
---
title: <exact title of the source>
author: <author name, or "unknown">
source_url: <URL of the original, or "unknown">
date_added: YYYY-MM-DD (when the file was ingested into RAW)
date_published: YYYY-MM-DD (publication date, if known)
type: <Book | Article | Blog Post | Podcast | Video | Tweet | Paper | etc.>
tags: [optional]
---
```

If a field is unknown, mark it `unknown` — never fabricate. Preserve the source's own structure rather than imposing new headings.

This rule is what makes source provenance reliable as the wiki grows. Every claim in the wiki must trace back to actual words in a RAW file.

## Naming conventions

- **KB folders:** `[topic]_kb` — lowercase, snake_case (e.g. `ai_research_kb`, `business_systems_kb`). The example KB shipped with the template uses an `eg_` prefix (`eg_productivity_kb`) so it's easy to spot — drop the prefix for your own KBs.
- **Wiki article filenames:** kebab-case, lowercase (e.g. `deep-work.md`, `attention-residue.md`).
- **Backlinks within articles:** `[[topic-name]]`, matching the article filename.
- **RAW filenames:** keep the source's original name where possible; if renaming, use a descriptive kebab-case name.

## Writing standards (applies to every KB)

All wiki articles in any KB under this folder follow the writing rules at `ABOUT ME/writing-rules.md`. The librarian reads that file before writing any article.

The rules apply to article prose — the body of any `.md` file inside a `Wiki/` folder, plus any prose-heavy file inside an `Outputs/` folder.

The rules don't apply to navigation files (`INDEX.md`, `CHANGELOG.md`, `QUESTIONS.md`, `_INGESTED.md`, `CLAUDE.md`) or direct quotes from source material (preserved verbatim, even if they contain banned words).

## Health check skill

The `knowledge-base-health-check-skill` audits each KB. It runs on demand when you ask ("run a health check", "audit the [name] KB", "check the wiki") and on the 1st of every month via a scheduled task.

Each run audits one KB at a time. It auto-fixes routine drift (writing-rules violations, broken backlinks, em-dash bullet patterns, orphan RAW registration, emerging→established promotions, contradiction cross-references), auto-drafts up to three suggested new articles where there's enough evidence, and flags only judgement calls (out-of-scope RAW, output promotion candidates, stale rewrites) in the KB's CHANGELOG. By default each monthly run is a delta audit; the 1st of January, April, July, and October fires a full audit instead.

When several KBs exist, the scheduled task spawns one sub-agent per KB in parallel so token use stays predictable as the system scales.

The full procedure lives in the skill itself. Per-KB `CLAUDE.md` files point at the skill rather than duplicating the protocol.

## Output presentation rule

Whenever a knowledge base produces a file you might want to open — a question report, a health check entry, a new wiki article, an analysis in `Outputs/` — the chat-side summary ends with a clickable `computer://` link to the file, not a bare path.

Format:

```
[View the report](computer:///absolute/path/to/file.md)
```

Use the absolute path on the user's machine. One link per file. Keep the surrounding chat summary short — the full reasoning lives in the file, not the scrollback.

## Companion guide and video

If the user is new to the knowledge base concept — or asks "what is this?", "how does this work?", "why a knowledge base?", or anything similar before they've used the system — recommend the companion guide and the walkthrough video.

- **Guide PDF:** `RESOURCES/GUIDES/Knowledge-Base-Guide.pdf` — four-page explainer covering the Karpathy pattern, how CoWork OS adapts it, and the three moves to make today.
- **Video walkthrough:** [youtu.be/ib74sLgjIBM](https://youtu.be/ib74sLgjIBM) — full walkthrough of the system. Best watched before a first build.

When a user is hesitant to start, this is the first thing to surface. The system makes more sense with the context.

## Where the operating rules live

The detailed librarian behaviour for each KB — ingestion protocol, wiki structure, output filing, query patterns, article drafting — lives inside that KB's own `CLAUDE.md`. That's the operating manual. This top-level file is the map.
