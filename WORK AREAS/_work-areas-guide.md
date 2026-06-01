# Work areas guide

How CoWork OS organises your work — and how Claude navigates it.

---

## What are work areas?

Work areas are the broad, ongoing parts of your life where work happens. They don't have deadlines or finish lines — they're always active. Think of them as departments in a one-person business, or rooms in a house. "Content and Marketing" is a work area. "Business" is a work area. "Finance" is a work area.

CoWork OS ships with five starter areas: Admin-PA, Marketing, Business, Finance, and Personal. Rename them, add new ones, or remove any that don't fit — except Admin-PA, which is required (more on that below).

---

## What are projects?

Projects are specific pieces of work with a goal and an end point. They live inside the work area they belong to. "Website Redesign" is a project inside the Marketing area. "Q3 Tax Filing" is a project inside Finance.

Project folders are always named with a `-project` suffix so they're instantly recognisable — e.g., `website-redesign-project/`, `q3-tax-filing-project/`.

Every project folder contains three things:

- **project-brief.md** — what this project is, the goal, constraints, and status
- **memory.md** — session history, decisions, and lessons learned
- **outputs/** — everything Claude creates for this project

This keeps everything together in one place. No hunting across separate folders for the brief vs the deliverables.

---

## How Claude decides where to put things

When you ask Claude to do something, it follows this logic:

1. **Does this relate to an existing project?** Claude checks WORK AREAS/ for a matching project folder. If it finds one, it works there — reads the brief and memory, saves outputs to that project's outputs/ folder.

2. **Is this a new project?** If the work is substantial (multiple sessions, a clear goal, not a one-off task), Claude creates a new project folder (with the `-project` suffix) in the most relevant work area. It scaffolds the brief and memory from the templates in RESOURCES/TEMPLATES/.

3. **Is this a quick task?** For one-off tasks, admin jobs, or anything that doesn't belong to a specific project, Claude creates a project folder in Admin-PA/. Even quick tasks get a folder — it keeps things findable later.

If Claude picks the wrong area, just tell it. "Move this to Business" or "This belongs in Marketing, not Admin-PA."

---

## Admin-PA: the catch-all

Admin-PA is the default area for general tasks. System Review reports go here. Quick tasks go here. Anything that doesn't clearly belong to another area goes here.

Admin-PA cannot be deleted or renamed. It's always available as a home for miscellaneous work.

---

## Creating and managing areas

**Adding a new area:** Just create a folder inside WORK AREAS/. Name it whatever makes sense for your life. Claude will start using it immediately.

**Renaming an area:** Rename the folder. Claude reads the folder names fresh each session.

**Removing an area:** Delete the folder if it's empty, or move its contents elsewhere first. Don't delete Admin-PA.

**Archiving projects:** When a project is done, you can move its folder into an `_archive/` subfolder within the work area. This keeps completed work accessible without cluttering the active view. Claude won't actively scan archived projects but can access them if you ask.

---

## The naming convention

Files Claude creates follow this format: `project_content-type_v1.ext`

Examples:
- `Website-Redesign_Brief_v1.md`
- `Q3-Launch_Deck_v1.pptx`
- `Monthly-Review_Report_v2.docx`

The version number increments if a file with the same name already exists.

---

## Memory

Each project has its own memory log. Claude updates it after each session with decisions, progress, and lessons learned. Universal memory (things that apply across all your work) goes in `ABOUT ME/memory.md`.

The memory system is what makes CoWork OS a living system — Claude reads the relevant memory at the start of each session and picks up where you left off.
