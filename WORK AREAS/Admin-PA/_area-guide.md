# Admin-PA

Your personal assistant's home base. This is where quick tasks, system maintenance, and general admin work lives — anything that doesn't belong to a specific work area.

---

## What goes here

- **Quick tasks and one-offs.** Need a quick email drafted, a document converted, or some research done? If it's not part of a bigger project, it lives here.
- **System reviews.** The System Review skill saves its reports here, inside a `system-reviews-project/` folder. This is how the self-improving feedback loop stays organised.
- **General admin.** Invoices, receipts, scheduling, anything that's more "running your life" than "working on a project."
- **First Week Guide outputs.** When you run through the First Week Guide, your practice outputs land here.

---

## Your Personal Assistant

Admin-PA ships with an included Personal Assistant plugin that turns this area into an active second brain. Once activated, it handles task logging, daily briefings, contact tracking, and prompted reflections through conversational interaction — you just talk to it.

The PA is opt-in. You activate it when you're ready (drag the plugin file into chat or say "set up my personal assistant"), and it slots into this area naturally because the infrastructure is already here. It adds a captain's log, task tracking, a contact CRM, and scheduled daily briefings — all powered by plain text files, no external tools required.

---

## How Claude uses this area

When you ask for something that doesn't clearly belong to another work area, Claude puts it here. If you'd rather it go somewhere else, just say so — "move this to Business" or "this belongs in Marketing."

System Review reports always live here, regardless of what they're reviewing. This keeps all your system maintenance in one place.

---

## Organising within Admin-PA

Even quick tasks get project folders (with the `-project` suffix) so everything stays findable. A one-off research task becomes `quick-research-project/` with an outputs/ folder. It might feel like overhead for small things, but it means you can always find what Claude produced — and the memory log captures context for next time.

If Admin-PA starts getting cluttered, move completed project folders to an `_archive/` subfolder. Claude won't actively scan archived projects but can access them if you ask.
