# Basecamp → Things 3 import: setup

The other half of the sync. `things_basecamp_sync.py` pushes your completions from Things out to
Basecamp. This pulls Basecamp's open to-dos into Things, so what your team assigns you shows up in
Today and Upcoming without you opening Basecamp.

Everything here runs on your Mac. Neither end is reachable from a remote CoWork session.

---

## One thing to decide before you run it

Part 9 of your Things 3 guide draws a hard line: *"Things 3 = what YOU need to do. Basecamp = what
the NeoWorld team needs to do. Crossing this line is how task systems collapse."*

Importing everything from Basecamp crosses that line. So the default doesn't import everything — it
imports **only to-dos assigned to you**, which is the same thing as "what you need to do." The line
holds. Two flags let you cross it if you decide you want to:

| Flag | What it pulls in |
|---|---|
| *(default)* | Only to-dos assigned to Hunter |
| `--include-unassigned` | Plus to-dos nobody has picked up |
| `--all-assignees` | Everyone's to-dos. Your team's backlog, in your personal list. Noisy. |

My read: stay on the default. If you want visibility into what the team is carrying, that's a
Basecamp view, not a Things list.

---

## What it does

```
Basecamp (via the 37signals CLI)
        │
        │  basecamp_things_import.py --apply
        ├──► no counterpart in Things ──► created in Things, tagged #basecamp
        ├──► already in Things         ──► linked, never duplicated
        ├──► close but not certain     ──► basecamp-import-review.json (your call)
        └──► done in Basecamp          ──► reported, optionally ticked off in Things
```

### Duplication is the failure mode that matters

A sync that creates a second copy of "Growth Plan v2" every hour is worse than no sync. Three
defenses, in order of how much they can be trusted:

1. **A marker in the notes.** Every imported task carries `[bc:12345]` at the bottom of its notes,
   plus a link back to the Basecamp to-do. On the next run the marker is matched exactly. This is
   certain — we wrote it.
2. **The link table** at `WORK AREAS/Admin-PA/things-basecamp-links.json`. Maps Basecamp to-do id →
   Things task uuid. Survives you editing the task's title in Things.
3. **The matcher** — only ever used the first time a to-do is seen. This is the same `normalize()`,
   `score()` and `ALIASES` table the completion sync uses, imported rather than copied. Fix a
   normalization bug once and both directions get it.

Section 8 of the regression harness runs the whole import twice and asserts the second pass creates
nothing. It also empties the link table and asserts the notes marker catches the duplicates on its own.

### The link table is the real prize

Right now the completion sync guesses, every time, using string similarity. Every pairing this
import settles gets written to the link table — so over the next few weeks the guessing shrinks to
nothing and both directions become id-to-id. That's what makes this safe to leave running.

---

## Where imported tasks land

| Basecamp project | Things Area |
|---|---|
| Momentum Staff HQ | RSG — CEO |
| Content Tracking | RSG — Content |
| Emily // Hunter | Personal |
| anything else | Inbox |

Unmapped projects go to the Inbox on purpose — capture first, decide later, exactly like Part 8 of
your guide. Edit `PROJECT_ROUTING` at the top of the script to add a project.

Tasks land in the **Area**, not inside the matching Things project. So "Film all tools in Loom for
new Growth Plan" arrives in RSG — CEO rather than inside your Growth Plan v2 project. Drag it in
once; the marker keeps the link stable and it won't move again.

**Dates.** A Basecamp due date is a hard stop, so it becomes the Things **deadline**, and the
**when** date is set two days earlier — Part 4 of your guide, applied automatically. No due date in
Basecamp means no dates in Things.

**Tag.** Everything imported gets `#basecamp`. Things ignores tags that don't already exist, so
create that tag once before the first run or the tag is silently dropped.

---

## Running it

### Step 1 — create the `basecamp` tag in Things

Things → any task → add a tag called `basecamp`. One time only. Skip this and the import still
works, you just can't filter by where a task came from.

### Step 2 — the dry run

Double-click `Task-Import_Dry-Run_v1.command` in Finder.

It pulls the latest, lists the Areas, projects and tags Things actually has, probes the Basecamp
CLI, runs the 63-check harness, then runs the import in dry run. Nothing is created. The output is
committed straight back to the repo, so you don't copy-paste anything — just tell me "the import
dry run is in."

If you'd rather type it:

```bash
python3 "$HOME/Desktop/Hunter Wilson/WORK AREAS/Admin-PA/things-basecamp-sync-project/outputs/basecamp_things_import.py"
```

The `"$HOME/..."` form matters. A quoted `~` doesn't expand, and the path has spaces in it — that
combination has bitten this project once already.

### Step 3 — settle whatever it queued

Anything the matcher isn't sure about gets listed as `NEEDS A CALL` and written to
`basecamp-import-review.json`. Nothing is created and nothing is linked until you say which it is:

```bash
python3 basecamp_things_import.py --apply --accept 204,206        # same thing, link them
python3 basecamp_things_import.py --apply --create-anyway 204     # different things, import it
```

The script prints both commands with the ids already filled in, so it's a copy-paste.

### Step 4 — the real run

```bash
python3 basecamp_things_import.py --apply
```

### Step 5 — put it on a timer

Add one line to `~/bin/hunter-sync.sh`, next to the completion sync. Order matters — push your
completions out first, then pull what's new in:

```bash
python3 "$HOME/Desktop/Hunter Wilson/WORK AREAS/Admin-PA/things-basecamp-sync-project/outputs/things_basecamp_sync.py" --apply
python3 "$HOME/Desktop/Hunter Wilson/WORK AREAS/Admin-PA/things-basecamp-sync-project/outputs/basecamp_things_import.py" --apply
```

---

## What the first run will probably do

Scored against your real Basecamp to-dos from `TASKS.md` and your real Things projects from
`Things3-Setup_Guide_v1.md`:

| Basecamp to-do | Outcome |
|---|---|
| Rebuild the GP Google Doc toolkits and send to Mark and Emily | create |
| Update the GP cue sheet template in coaching call cue sheet | create |
| Film all tools in Loom for new Growth Plan | create |
| Edit Healthy Volunteer Culture and assets (45 min) | create |
| Outline Keeping First Time Guests (Engagement Pathway) (1 hr) | create |
| Send Keeping First Time Guests to team for editing | create |
| 3rd Kid: Second Conversation | create |
| Hunter: Rule of Life | link to your `Rule of Life` project |
| Create a Video Sales Letter | link to `RSG VSL` via the alias table |
| Proactive Emotional Honesty with Emily | link to `Emotional Honesty with Emily` |
| Ship Growth Plan v2 flow with Mark Brewer | queue — 0.75 against `Growth Plan v2` |
| Review Brand Deals with Tanner Milson | queue — 0.80 against `Brand Deals Review` |

**7 created, 3 linked, 2 queued, 0 wrong.** The seven creates are all genuinely new — they're
to-dos underneath projects you already have, not copies of the projects themselves.

The two queued ones are the honest cases. `Ship Growth Plan v2 flow with Mark Brewer` scores 0.75
against your `Growth Plan v2` project — the exact same score the completion sync gives that pair.
Both directions agree it's a maybe, which is the whole reason they share one matcher.

---

## Closing the loop the other way

When a teammate finishes a to-do in Basecamp, the Things copy sits there open. The import spots it
and reports `DONE IN BC`, but doesn't touch it by default — silently ticking things off your list is
the kind of thing that makes you stop trusting a tool.

To let it:

1. Things → Settings → General → Enable Things URLs → Manage → copy the token.
2. `export THINGS_AUTH_TOKEN="..."` in your shell profile.
3. Run with `--close-in-things`.

Adding tasks needs no token. Completing them does — that's Things' design, not an oversight here.

---

## What's verified and what isn't

`test_basecamp_things_import.py` builds a throwaway Things database, a fake Basecamp CLI, and a fake
`open` that actually applies the `things:///` URL to the database. So the round trip is genuinely
exercised, not just the half of it that's visible from here. 63 checks, all passing, plus the
existing 26 for the completion sync — that suite still passes untouched, which is the proof that
importing its matcher didn't disturb it.

Still unknown, because a simulation can't reach it:

- Whether your installed Basecamp CLI uses the documented `projects list --json` / `todos list --in`
  shapes. If not, the `CMD_*` constants at the top of `things_basecamp_sync.py` need one edit — the
  script prints the exact failing command.
- Whether your Basecamp to-dos carry `due_on`. If the field is named differently, dates are skipped
  and everything else still works.
- Whether your Areas are named exactly `RSG — CEO` and `RSG — Content`, with an em dash. A mismatch
  isn't an error — Things quietly puts the task in the Inbox instead. Step 2 of the runner prints
  your real Area names so you can check.

Stdlib only. No pip, no Homebrew. macOS ships Python 3.9; this runs on 3.8+.
