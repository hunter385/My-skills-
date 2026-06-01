# CoWork OS — Version updates

This file tracks what's changed in each release of CoWork OS so you can see what's new, what's fixed, and what's coming.

You don't need to do anything when a new version drops — the template itself is yours to keep and customise, and plugin updates flow through the Better Creating marketplace automatically (`bettercreating/cowork-os-plugins`). When something does need your attention, it's called out under "What you might need to do" for that version.

Newest at the top.

---

## v1.0 — 22 May 2026

CoWork OS leaves beta. v1.0 wraps up the Knowledge Base integration, applies a round of usability polish from beta feedback, and ships the architectural changes that fix the context-pressure pattern power users were hitting.

The headline: **v1.0 fixes the heavy operations.** The biggest change is that System Review now runs in its own context window via a subagent — so it doesn't pile 120 KB of file reads into the conversation you were already in. That's the single most-requested fix, diagnosed in detail by Jon Rios (whose review and follow-up Agent investigation directly shaped what shipped here).

### What's new for you

**Architectural changes (the v1.0 headline)**

- **System Review now runs in its own context window.** When you ask Claude to review your system, the heavy reading (every About Me file, every project memory log, every recent report) happens in a separate subagent with its own 200 KB window. Your main conversation only sees the headline summary and a path to the saved report. The "my session got slow / autocompacted mid-review" pattern goes away. Credit to Jon Rios for the diagnosis.
- **CLAUDE.md slimmed by ~25%.** Identity content — WHO I AM, HOW I LIKE TO WORK, MY PREFERENCES, WHAT I USUALLY NEED HELP WITH, WORKING WITH MY TOOLS — used to live in CLAUDE.md AND about-me.md. Now it lives only in `ABOUT ME/about-me.md`. Less duplication, less to load every session, one source of truth.
- **Memory rotation rule.** When `ABOUT ME/memory.md` grows past ~150 lines, Claude rolls older entries into a quarterly archive file (`memory-archive-YYYY-QN.md`) that's reference-only — never loaded into the session unless you ask. Same rule applies to project memory logs. Prevents memory.md from becoming the next bloat vector.
- **System Review reports cite paths, not content.** Reports used to embed snippets of your About Me files and memory entries. Now they reference source files by path only. Reports stay small (2–5 KB instead of 50–100 KB) so the session-start check stays lightweight.
- **System Review reports auto-archive.** Reports older than 30 days that you've already walked through move to `WORK AREAS/Admin-PA/system-reviews-project/_archive/` automatically. CLAUDE.md no longer reads old report bodies on session start — it reads a tiny index file instead.

**Knowledge Base integration**

- **The KNOWLEDGE folder is part of the template.** A fourth top-level folder alongside ABOUT ME, WORK AREAS, and RESOURCES. Your local second brain — a system of topic-focused knowledge bases that Claude maintains as your librarian. Drop sources into RAW/, ask Claude to compile, ask questions. Every question becomes a permanent dated report with citations. One example KB ships in the template (`eg_productivity_kb/`).
- **Knowledge Base Guide PDF** (`RESOURCES/GUIDES/Knowledge-Base-Guide.pdf`). Four pages covering what it is, the Karpathy pattern behind it, how CoWork OS adapts it, and the three moves to make today. Pairs with a 12-minute walkthrough at **youtu.be/ib74sLgjIBM**.
- **`knowledge-base-health-check-skill`** ships with the system. Audits your KNOWLEDGE folder monthly, auto-fixes routine drift, drafts new wiki articles, flags anything that needs your judgement.
- **The Onboarding Coach includes a Knowledge Base step.** During setup, you can spin up your first KB and schedule the monthly health check — or skip and come back later.

**Documentation and onboarding polish**

- **New guide: "Working alongside your other tools"** (`RESOURCES/GUIDES/Working-Alongside-Your-Tools.md`). Answers the most common question from new users: do I switch from Notion / Office / Drive, or work alongside? Short answer: alongside. Covers Notion, Google Drive, Microsoft 365, Gmail, Slack.
- **Microsoft 365 connectors in onboarding.** The Onboarding Coach now suggests Outlook, OneDrive, SharePoint, and Teams alongside the Google equivalents — instead of defaulting to Google. Detects which stack you use based on your Step 3 answers.
- **Better docs for "tasks that run outside your session."** The Good Practices Guide now has a dedicated page covering scheduled tasks (Claude must be open; tasks open a fresh session that doesn't inherit your folder; fix with absolute paths + a folder-context line) and Dispatch routing (mobile-to-desktop actions land in whatever session is open on desktop; fix by favouriting your CoWork folder as a Project, or by including the folder path in the dispatched message). The PA and KB health check scheduled tasks ship with these patterns baked in.
- **First Install Guide leads with the prompt to paste.** A prominent "Paste this prompt" callout sits at the top of page 1 — anyone scanning the page sees what to actually paste before they get bogged down in detail.
- **Voice input recommendation** in the Good Practices Guide. Wispr Flow gets a small plug as the system-wide dictation tool that pays for itself the first day.
- **Licence and affiliate redistribution** (`Licence-and-Affiliate-Redistribution.md` at root). Clearer statement that the file isn't for sharing, with an affiliate sign-up link for anyone who wants to recommend CoWork OS and earn commission.
- **Cleaner first-session experience.** The Onboarding Coach silently removes its one-time bootstrap trigger from CLAUDE.md once setup begins, so future sessions skip the "fresh install" check entirely.
- **Getting Started PDF folder map** split across two pages — was overflowing, now reads cleanly with the skill install on its own page.
- **Plugin installs go through the marketplace, full stop.** All references to dragging `.plugin` files have been removed from the onboarding flow. Offline `.plugin` snapshots still live in `RESOURCES/PLUGINS/` as a fallback.
- **Skill installs go through the in-chat cards, full stop.** The onboarding coach presents skills as interactive cards you click to install. The manual fallback (if cards don't appear) is Customise → Personal Skills → +.
- **Feedback link baked into the onboarding coach and the System Review skill** when each wraps up.
- **Skills work in CoWork *and* Claude Code.** The System Review and KB Health Check skills now use plain numbered options for interactive presentation instead of the `AskUserQuestion` API. Same UX, zero API dependency, identical behaviour in both environments. Surfaced from a live System Review test on a real workspace.
- **Live-tested on a real workspace.** System Review ran end-to-end against an active production system on 23 May: 42 file reads, 103,314 tokens consumed inside the sub-agent, only a short summary returned to the main conversation. ~99.5% context savings compared with running inline. Architecture validated, findings substantive.

### What you might need to do

- **Nothing required to use v1.0.** If you're upgrading from Beta-1.4 or earlier, replacing your `cowork-os-1.0/` folder with the new one picks up everything. Your existing ABOUT ME files, WORK AREAS, and KNOWLEDGE bases stay where they are.
- **If your CLAUDE.md has identity content (WHO I AM, HOW I LIKE TO WORK, MY PREFERENCES, etc.):** v1.0 expects that content to live in `ABOUT ME/about-me.md` instead. The new template ships with placeholder sections for it. If you migrate, move those sections across from your old CLAUDE.md into about-me.md. The onboarding coach handles this automatically for new installs.
- **If you have a heavily customised existing Claude workspace:** the new `If-You-Already-Have-A-Claude-Setup.md` guide walks through the merge step by step.

### Coming in v1.1 (target: 2–4 weeks)

- **`writing-rules` and `specialist-routing` converted to triggerable skills.** Currently always-loaded, which means every session reads them even when you're not writing. In v1.1 they become real skills with descriptions — same depth, ~95%+ reliable application via CoWork's skill matching, even less baseline overhead.
- **Migration skill for existing Claude users.** A dedicated skill the Onboarding Coach loads when it detects you already have a working Claude setup. Scans your existing folder, classifies what you've got (light user with a CLAUDE.md, power user with full folder structure, knowledge base setup, etc.), and walks you through a tailored merge into CoWork OS without breaking references. Design source is `CoWork-OS_Migration-Analysis-Report_v1.md`. For v1.0, the Onboarding Coach handles existing-setup users conversationally — but the dedicated skill makes it reliable and tested.
- **PA duplicate-commands bug fix.**
- **Plugin hygiene check** in System Review — flags installed plugins not triggered in 30+ days (advice, not auto-disable).
- **Multi-Device Sync Guide PDF.**
- **Cross-platform / Claude Code condensed instructions.**
- **Two-week First Week Guide variant.**
- **Setup video re-record** that leads with the automated path.

The narrative: **v1.0 fixes the heavy operations. v1.1 fixes the baseline.**

### Behind the scenes (for the curious)

- CLAUDE.md slimmed from 181 to 139 lines. Memory rotation rule added to AFTER EVERY TASK. Admin-PA report check restructured to read a small index file rather than full report bodies.
- System Review SKILL.md restructured: new "Execution architecture" section dispatches the heavy reading to a general-purpose subagent via the Agent tool. Inline fallback documented for environments where the Agent tool isn't available. Report writing rules updated: cite source files by path, never embed content. Index-maintenance + archive-after-30-days behaviour added.
- about-me.md template expanded with five new receiving sections: "How I like to work", "My preferences", "What I usually need help with", "Working with my tools", and adjustments to existing identity sections. Onboarding Coach Step 9 redirected to customise about-me.md instead of CLAUDE.md.
- KB integration finalised in `cowork-os-1.0/KNOWLEDGE/`. Top-level `KNOWLEDGE/CLAUDE.md` covers the system rules; `_KB_CLAUDE_TEMPLATE.md` is the canonical per-KB template.
- Onboarding Coach SKILL.md updated for: Microsoft 365 connector suggestions (Step 6 + Step 3 tool options), four-skill install, priority-zero cleanup, Step 9 redirect to about-me.md.
- All three changed skills repackaged via skill-creator's `package_skill.py`: onboarding-coach, system-review, knowledge-base-health-check-skill.
- Good Practices Guide PDF generator extended with a new page on "Tasks that run outside your session" covering both scheduled tasks and Dispatch routing. Matching HTML slide deck slide added.
- First Install Guide PDF generator restructured so the paste-this-prompt block is the hero element of page 1.
- New guides: `Working-Alongside-Your-Tools.md`, `If-You-Already-Have-A-Claude-Setup.md`, `Licence-and-Affiliate-Redistribution.md`.
- Pre-v1.0 checkpoint zipped at `Versions_Archive_Zips/CoWork-OS-Beta-1.5-Checkpoint_pre-v1.0.zip` for clean rollback.
- **System Review SKILL.md optimised (Task C edits, 23 May).** Three targeted cuts against the Meta-Agent Prompt Engineering 2.0 framework: deduplicated subagent dispatch prompt (was enumerating Phase 1/2/3 detail twice), collapsed "Handling edge cases" into the relevant Phases inline, merged "Scheduled task mode" into Execution Architecture. ~8% line reduction with no loss of functionality. Five further cuts identified for a potential Task B rewrite in v1.1 (rationale paragraphs, Phase 2 example consolidation, duplicated Report Format template, imperative-sentence pass, Communication style trim — combined ~30% additional potential).
- **AskUserQuestion replaced with numbered text options in System Review and KB Health Check (23 May).** Live test surfaced a Cowork failure mode: an `AskUserQuestion` call placed immediately after a sub-agent dispatch in the same turn errors out. Both skills now use plain numbered options in chat (`> 1. Show me the critical issues first`, `> 2. ...`) with explicit "Do not use AskUserQuestion" directives at the point of use. Cross-skill lesson captured: any future skill following the "sub-agent does the work → main conversation presents findings" pattern should use numbered text for the interactive layer.
- **KB Health Check propagated** to all four shipping locations (Simon's canonical source, cowork-os-1.0/RESOURCES/MY SKILLS, Upgrade-Pack drop-in, standalone Knowledge Base Kit). Packaging accident fixed in the process — the canonical .skill had been zipping a recursive copy of itself; new builds don't.

---

## In-between updates since Beta-1.4

These shipped to existing users automatically via the GitHub marketplace — no zip rebuild required. Bundled into the Beta-1.5 release for completeness.

### Personal Assistant v1.1.0 — 12 May 2026

Based on community feedback from Melvin: the `/tidy` slash command got a substantial upgrade.

**What's new:**
- Scoped trigger phrases — "organize my [folder]", "clean up [folder]", "find duplicates", "my [folder] is a mess".
- Conservative-vs-comprehensive mode question before scanning, so you choose how aggressive the cleanup should be.
- Content-hash duplicate detection (not just filename matching) — now spots true duplicates even if they've been renamed.
- Cross-platform support — works on macOS, Linux/WSL, and Windows PowerShell.
- Folder-structure proposal gated behind comprehensive mode.
- Naming conventions applied on rename (date prefix, kebab-case, strip download artifacts).
- One-line maintenance tip per folder type after each tidy.

### Specialist Sub-Agent Builder v0.8.1 — 12 May 2026

Based on community feedback from Luigi: clearer validator-constraint docs to prevent silent "Plugin validation failed" errors.

**What's new:**
- Description length warning at ~1000 characters in Step 6b.
- Slug must start with a letter (now enforced in Step 6).
- New "Cowork Validator Constraints" section near the end of SKILL.md covering description length, name-starts-with-letter rule, `user_invocable: true` as a safe optional, and a note to keep the folded `description: >` style.

### First Install Guide Step 3 — 12 May 2026

The old wording told you to "click the paperclip icon and select Add folder" — that UI no longer exists. Fixed to match Claude's current flow:

1. Open the drop-down that says "Work in a project" under the main chat window.
2. Find and select your CoWork OS folder.
3. Click the star icon to favourite it for quick access.

---

## Beta-1.4 — 14 April 2026

This was the big plugin-delivery overhaul. Plugin install had been the rockiest part of the setup experience — multiple users hit errors with the previous local-file methods. Beta-1.4 fixed this with a proper marketplace.

### What's new for you

- **GitHub plugin marketplace launched at `bettercreating/cowork-os-plugins`.** This is now the canonical way to install the Specialist Sub-Agent Builder and the Personal Assistant. One marketplace add, one click per plugin, done. Updates flow through automatically — no more reinstalls when versions bump.
- **INSTALL-PLUGINS Guide added** in `RESOURCES/PLUGINS/` covering three install paths: CoWork desktop UI (Option 1), Claude Code desktop tab (Option 2), Terminal for Claude Code users (Option 3). Plus a Safety Warning explainer (the "Anthropic can't guarantee third-party plugin safety" message is normal — it appears for every non-Anthropic marketplace).
- **Plugin file permissions fixed** — older plugin packages had restrictive permissions (600) that caused install errors on some systems. Now 644 across the board.
- **Quarantine attributes stripped** — both plugins now install cleanly without macOS Gatekeeper warnings.
- **Onboarding Coach updated** — Steps 7 and 11 now reference the marketplace install method instead of the old local-file paths.
- **Local marketplace structure added** — `RESOURCES/PLUGINS/` now contains a `.claude-plugin/marketplace.json` and unpacked plugin folders, making it a valid offline marketplace source if you ever need to install without internet.

### What you might need to do

- If you had install errors with the older `.plugin` file methods, retry via the marketplace — it's the reliable path now.
- If you'd previously installed plugins manually, you can leave them as they are. Future updates flow through the marketplace either way.

---

## Earlier beta releases

Beta-1.0 through Beta-1.3 were development iterations. The shape of the system was being decided across:

- **PARA-inspired folder restructure** (Beta-1.0) — moved from a flat `PROJECTS/` + `CLAUDE OUTPUTS/` layout to the current three top-level folders (`ABOUT ME/`, `WORK AREAS/`, `RESOURCES/`), with WORK AREAS broken down by area of responsibility and each project containing its own brief, memory, and outputs.
- **Setup-cowork bypass** (Beta-1.2) — added a CLAUDE.md instruction to use the CoWork OS Onboarding Coach instead of Claude's built-in generic setup-cowork skill. The built-in skill doesn't understand the CoWork OS folder structure and would derail setup.
- **Voice profile checkpoint** (Beta-1.2) — added a mid-onboarding decision point in Step 5: continue with starter-depth voice profile, or go 10–15 minutes deeper now. Either is fine — the choice is logged to memory so it surfaces in future System Reviews.
- **Marketplace plugin suggestions in Step 7** (Beta-1.2) — the Onboarding Coach started suggesting relevant plugins from the marketplace based on what you do.
- **Bonus Skills Easter egg** (Beta-1.2) — Copywriting Expert, Weekly Review, and PDF Creator skills added to `RESOURCES/MY SKILLS/Wonderful Bonus Skills from Better Creating/`. Not announced — discovered by users who explore.
- **Personal Assistant plugin shipped beta** (Beta-1.2) — captain's log, automatic task extraction, contacts register, daily briefing and end-of-day summaries. Optional, installed from the marketplace.

---

## How to read this log

- **"What's new for you"** is the user-facing changes — anything that affects what you see, type, or do.
- **"What you might need to do"** flags any setup or migration steps. Usually "nothing" — the template is yours, plugin updates flow through the marketplace.
- **"Behind the scenes"** is for the curious — what changed structurally, what was rebuilt, what files moved.

If you've spotted something this log doesn't explain, share it via the feedback form: <https://separate-pressure-d28.notion.site/68531cf2262144ef884fabe3964c801d?pvs=105>
