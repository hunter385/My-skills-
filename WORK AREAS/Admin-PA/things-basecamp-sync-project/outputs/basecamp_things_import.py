#!/usr/bin/env python3
"""
Basecamp -> Things 3 task import.

The other half of the sync. `things_basecamp_sync.py` pushes completions from
Things to Basecamp; this pulls open to-dos from Basecamp into Things so they
show up in Today and Upcoming without you opening Basecamp.

MUST run on the Mac. Things 3 has no web API -- it is a local SQLite database
plus a URL scheme, so this cannot run in a remote CoWork session.

Dry run by default. Nothing is written to Things unless you pass --apply.

    python3 basecamp_things_import.py               # show what would be created
    python3 basecamp_things_import.py --apply       # actually create them
    python3 basecamp_things_import.py --all-assignees   # not just yours

Requires: python3 (stdlib only), Things 3, and the 37signals basecamp CLI,
authenticated. Shares its matcher, alias table and CLI plumbing with
things_basecamp_sync.py -- fix a normalization bug once, both directions get it.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
import urllib.parse
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

# The completion sync owns normalize(), score(), containment() and ALIASES.
# Importing rather than copying is deliberate: two matchers that drift apart
# would create duplicates in Things for pairs the other direction thinks match.
import things_basecamp_sync as core  # noqa: E402

# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------

BASE_DIR = os.path.expanduser("~/Desktop/Hunter Wilson/WORK AREAS/Admin-PA")

# The link table. Maps a Basecamp to-do id to the Things task it corresponds to.
# This is the point of the whole exercise: once a pair is in here, neither
# direction has to guess again. Fuzzy matching is only ever used on first sight.
LINKS_PATH = os.path.join(BASE_DIR, "things-basecamp-links.json")

# Pairs the matcher wasn't confident enough to link on its own.
REVIEW_PATH = os.path.join(BASE_DIR, "basecamp-import-review.json")

# Deliberately NOT things-basecamp-sync.log. Two writers, two logs.
LOG_PATH = os.path.join(BASE_DIR, "basecamp-things-import.log")

# Which Things Area each Basecamp project lands in. Names must match your Areas
# exactly -- Things sends an unrecognised list name to the Inbox rather than
# failing, so a typo here looks like "it worked but everything went to Inbox".
# Unmapped projects go to the Inbox on purpose: capture first, decide later.
PROJECT_ROUTING = {
    "momentum staff hq": "RSG — CEO",
    "content tracking": "RSG — Content",
    "emily // hunter": "Personal",
}
DEFAULT_LIST = ""  # empty = Things Inbox

# One tag, not five. Lets you see at a glance what came from the team system,
# which is the boundary Part 9 of the Things 3 guide is protecting.
# Things ignores tags that don't already exist -- create it before the first run.
IMPORT_TAG = "basecamp"

# Part 4 of the guide: deadline is the hard stop, when is the day you start.
# A Basecamp due date is a hard stop, so it becomes the deadline and the task
# surfaces this many days earlier.
WHEN_LEAD_DAYS = 2

ASSIGNEE = "Hunter"

# Things URL scheme limits. Chunked so a big first import doesn't build one
# enormous URL that `open` refuses.
MAX_ITEMS_PER_URL = 12
MAX_URL_CHARS = 8000
CHUNK_PAUSE_SECONDS = 1.5

# Things processes the URL asynchronously, so the new rows aren't in the
# database the instant `open` returns.
VERIFY_ATTEMPTS = 6
VERIFY_PAUSE_SECONDS = 1.5

CORE_DATA_EPOCH_OFFSET = core.CORE_DATA_EPOCH_OFFSET
TYPE_HEADING = 2
STATUS_INCOMPLETE = 0

# Don't re-create something you finished in Things last week but which is still
# open in Basecamp -- that's the completion sync's job, not ours.
RECENT_COMPLETION_HOURS = 720


# --------------------------------------------------------------------------
# Things: reading
# --------------------------------------------------------------------------

def _columns(conn, table: str) -> set:
    return {row[1] for row in conn.execute(f"PRAGMA table_info({table})")}


def read_things_tasks() -> list[dict]:
    """
    Every live task and project in Things, with enough context to dedupe against.

    Includes type 1 (projects), not just to-dos. This matters: 'Growth Plan v2'
    is a project in Things but a to-do in Basecamp, so a to-do-only read would
    happily create a duplicate to-do alongside the project.
    """
    src = core.find_things_db()

    with tempfile.TemporaryDirectory() as tmp:
        copy = os.path.join(tmp, "things.sqlite")
        shutil.copy2(src, copy)
        for suffix in ("-wal", "-shm"):
            if os.path.exists(src + suffix):
                shutil.copy2(src + suffix, copy + suffix)

        conn = sqlite3.connect(f"file:{copy}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        try:
            have = _columns(conn, "TMTask")
            wanted = ["uuid", "title", "status", "type", "stopDate"]
            optional = [c for c in ("notes", "creationDate") if c in have]
            cols = ", ".join(wanted + optional)
            rows = conn.execute(
                f"SELECT {cols} FROM TMTask WHERE trashed = 0 AND type != ?",
                (TYPE_HEADING,),
            ).fetchall()
        finally:
            conn.close()

    cutoff = (time.time() - RECENT_COMPLETION_HOURS * 3600) - CORE_DATA_EPOCH_OFFSET
    out = []
    for r in rows:
        title = (r["title"] or "").strip()
        if not title or title.startswith("----"):
            continue
        keys = r.keys()
        status = r["status"]
        stop = r["stopDate"]
        # Open tasks, plus anything finished recently enough to still be a
        # plausible duplicate.
        if status != STATUS_INCOMPLETE and not (stop and stop > cutoff):
            continue
        out.append({
            "uuid": r["uuid"],
            "title": title,
            "notes": (r["notes"] or "") if "notes" in keys else "",
            "status": status,
            "type": r["type"],
            "created": r["creationDate"] if "creationDate" in keys else None,
        })
    return out


def things_uuids_present() -> set:
    """Every uuid in the database, whatever its state. Used to spot deletions."""
    src = core.find_things_db()
    with tempfile.TemporaryDirectory() as tmp:
        copy = os.path.join(tmp, "things.sqlite")
        shutil.copy2(src, copy)
        for suffix in ("-wal", "-shm"):
            if os.path.exists(src + suffix):
                shutil.copy2(src + suffix, copy + suffix)
        conn = sqlite3.connect(f"file:{copy}?mode=ro", uri=True)
        try:
            return {row[0] for row in conn.execute("SELECT uuid FROM TMTask")}
        finally:
            conn.close()


# --------------------------------------------------------------------------
# Things: writing, via the URL scheme
# --------------------------------------------------------------------------

def marker(todo_id) -> str:
    return f"[bc:{todo_id}]"


def build_payload(item: dict) -> dict:
    """One Things JSON operation for one Basecamp to-do."""
    notes_lines = [f"From Basecamp · {item['project']}"]
    if item.get("url"):
        notes_lines.append(item["url"])
    notes_lines += ["", marker(item["id"])]

    attributes = {
        "title": item["title"],
        "notes": "\n".join(notes_lines),
    }

    listname = PROJECT_ROUTING.get(item["project"].strip().lower(), DEFAULT_LIST)
    if listname:
        attributes["list"] = listname
    if IMPORT_TAG:
        attributes["tags"] = [IMPORT_TAG]

    due = parse_due(item.get("due_on"))
    if due:
        attributes["deadline"] = due.isoformat()
        when = due - timedelta(days=WHEN_LEAD_DAYS)
        today = datetime.now().date()
        attributes["when"] = (when if when > today else today).isoformat()

    return {"type": "to-do", "attributes": attributes}


def parse_due(value):
    if not value:
        return None
    text = str(value).strip()[:10]
    try:
        return datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        return None


def chunk_payloads(payloads: list[dict]) -> list[list[dict]]:
    """Split into URL-sized batches."""
    chunks, current = [], []
    for p in payloads:
        trial = current + [p]
        encoded = urllib.parse.quote(json.dumps(trial, ensure_ascii=False), safe="")
        if current and (len(trial) > MAX_ITEMS_PER_URL or len(encoded) > MAX_URL_CHARS):
            chunks.append(current)
            current = [p]
        else:
            current = trial
    if current:
        chunks.append(current)
    return chunks


def send_to_things(payloads: list[dict]) -> None:
    for i, chunk in enumerate(chunk_payloads(payloads)):
        data = urllib.parse.quote(json.dumps(chunk, ensure_ascii=False), safe="")
        url = f"things:///json?data={data}"
        # -g so Things doesn't steal focus mid-import.
        proc = subprocess.run(["open", "-g", url], capture_output=True, text=True)
        if proc.returncode != 0:
            core.die(
                "Could not hand the tasks to Things.\n"
                f"  open exited {proc.returncode}: {proc.stderr.strip()}\n"
                "  Is Things 3 installed, and are Things URLs enabled in\n"
                "  Things → Settings → General?"
            )
        log(f"sent chunk {i + 1} with {len(chunk)} task(s) to Things")
        time.sleep(CHUNK_PAUSE_SECONDS)


def complete_in_things(uuid: str, token: str) -> bool:
    """Tick a task off in Things. Unlike adding, this needs an auth token."""
    query = urllib.parse.urlencode({"auth-token": token, "id": uuid, "completed": "true"})
    proc = subprocess.run(["open", "-g", f"things:///update?{query}"],
                          capture_output=True, text=True)
    return proc.returncode == 0


# --------------------------------------------------------------------------
# Basecamp
# --------------------------------------------------------------------------

def fetch_basecamp_todos(include_unassigned: bool, all_assignees: bool) -> list[dict]:
    """
    Every to-do across every project, open and completed, with due dates.

    The completion sync's fetch drops completed to-dos and most fields; this
    direction needs both, so it does its own read over the same CLI plumbing.
    """
    projects = core.parse_json(core.run_cli(core.CMD_PROJECTS), "projects")
    todos = []

    for proj in projects:
        pid = proj.get("id")
        if pid is None:
            continue
        pname = proj.get("name") or proj.get("title") or str(pid)

        cmd = [part.replace("{project_id}", str(pid)) for part in core.CMD_TODOS]
        for todo in core.parse_json(core.run_cli(cmd), f"to-dos for {pname}"):
            title = (todo.get("title") or todo.get("content") or "").strip()
            if not title:
                continue

            names = [(a.get("name") or "")
                     for a in (todo.get("assignees") or [])
                     if isinstance(a, dict)]
            if not all_assignees:
                mine = any(ASSIGNEE.lower() in n.lower() for n in names)
                if not mine and not (include_unassigned and not names):
                    continue

            todos.append({
                "id": todo.get("id"),
                "title": title,
                "project": pname,
                "completed": bool(todo.get("completed")),
                "due_on": todo.get("due_on") or todo.get("due_at"),
                "url": todo.get("app_url") or todo.get("url"),
                "assignees": names,
            })

    return todos


# --------------------------------------------------------------------------
# Link table
# --------------------------------------------------------------------------

def load_links() -> dict:
    if not os.path.exists(LINKS_PATH):
        return {}
    try:
        with open(LINKS_PATH, encoding="utf-8") as fh:
            data = json.load(fh)
    except (json.JSONDecodeError, OSError) as exc:
        core.die(f"Could not read the link table at {LINKS_PATH}: {exc}")
    return data.get("links", {}) if isinstance(data, dict) else {}


def save_links(links: dict) -> None:
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "note": ("Maps Basecamp to-do id -> the Things task it corresponds to. "
                 "Both sync directions read this before falling back to fuzzy "
                 "matching. Safe to delete an entry to force a re-match."),
        "links": links,
    }
    write_json(LINKS_PATH, payload)


def write_json(path: str, payload: dict) -> None:
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    os.replace(tmp, path)


def log(line: str) -> None:
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    try:
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        with open(LOG_PATH, "a", encoding="utf-8") as fh:
            fh.write(f"{stamp}  {line}\n")
    except OSError:
        pass


# --------------------------------------------------------------------------
# Planning
# --------------------------------------------------------------------------

def find_existing(bc_todo: dict, things_tasks: list[dict]) -> tuple:
    """
    Best existing Things task for this Basecamp to-do, if any.

    Two signals, checked in order of trustworthiness:
      1. The [bc:id] marker in the notes -- certain, we wrote it.
      2. The shared fuzzy matcher -- a guess, so it obeys the same thresholds
         the completion sync uses.
    """
    mark = marker(bc_todo["id"])
    for task in things_tasks:
        if mark in (task.get("notes") or ""):
            return task, 1.0, "marker"

    scored = sorted(
        ((core.score(t["title"], bc_todo["title"]), t) for t in things_tasks),
        key=lambda pair: pair[0],
        reverse=True,
    )
    if not scored or scored[0][0] < core.REVIEW_THRESHOLD:
        return None, 0.0, "none"

    best_score, best = scored[0]
    runner_up = scored[1][0] if len(scored) > 1 else 0.0
    too_close = best_score - runner_up < 0.05 and runner_up >= core.REVIEW_THRESHOLD
    if too_close:
        return best, best_score, "ambiguous"
    if best_score >= core.AUTO_THRESHOLD:
        return best, best_score, "confident"
    return best, best_score, "ambiguous"


def plan(todos: list[dict], things_tasks: list[dict], links: dict,
         accept: set = frozenset(), force_create: set = frozenset()) -> dict:
    by_uuid = {t["uuid"]: t for t in things_tasks}
    live_uuids = things_uuids_present()

    result = {
        "create": [],        # no counterpart in Things -- import it
        "linked": [],        # already there, link recorded, nothing to do
        "relink": [],        # matched an existing task; record the pairing
        "review": [],        # close but not certain -- your call
        "closed_in_bc": [],  # done in Basecamp, still open in Things
        "stale_links": [],   # linked Things task no longer exists
    }

    for todo in todos:
        key = str(todo["id"])
        link = links.get(key)

        if link:
            uuid = link.get("things_uuid")
            if uuid and uuid not in live_uuids:
                result["stale_links"].append({**todo, "things_uuid": uuid})
                # Fall through and re-match: he deleted it, or Things reassigned it.
            else:
                task = by_uuid.get(uuid)
                if todo["completed"] and task and task["status"] == STATUS_INCOMPLETE:
                    result["closed_in_bc"].append({**todo, "things_uuid": uuid,
                                                   "things_title": task["title"]})
                else:
                    result["linked"].append({**todo, "things_uuid": uuid})
                continue

        if todo["completed"]:
            # Completed in Basecamp and never in Things. Importing a finished
            # task just to tick it off is noise.
            continue

        existing, confidence, kind = find_existing(todo, things_tasks)

        if kind in ("marker", "confident"):
            result["relink"].append({
                **todo,
                "things_uuid": existing["uuid"],
                "things_title": existing["title"],
                "confidence": round(confidence, 3),
                "how": kind,
            })
        elif kind == "ambiguous":
            # You've already looked at this pair and told us what it is.
            if key in force_create:
                result["create"].append(todo)
                continue
            if key in accept:
                result["relink"].append({
                    **todo,
                    "things_uuid": existing["uuid"],
                    "things_title": existing["title"],
                    "confidence": round(confidence, 3),
                    "how": "accepted",
                })
                continue
            result["review"].append({
                **todo,
                "things_uuid": existing["uuid"],
                "things_title": existing["title"],
                "confidence": round(confidence, 3),
                "reason": (f"confidence {confidence:.2f} is below the "
                           f"{core.AUTO_THRESHOLD} auto threshold, or two "
                           "candidates scored within 0.05 of each other"),
            })
        else:
            result["create"].append(todo)

    return result


def resolve_new_uuids(created: list[dict], before: set) -> dict:
    """
    Find the uuids Things assigned to what we just created.

    The URL scheme doesn't hand back ids, so we look for rows that weren't there
    before, matched on the marker we embedded in the notes.
    """
    wanted = {marker(item["id"]): str(item["id"]) for item in created}
    found = {}

    for attempt in range(VERIFY_ATTEMPTS):
        time.sleep(VERIFY_PAUSE_SECONDS)
        for task in read_things_tasks():
            if task["uuid"] in before:
                continue
            for mark, bc_id in wanted.items():
                if bc_id not in found and mark in (task.get("notes") or ""):
                    found[bc_id] = task["uuid"]
        if len(found) == len(wanted):
            break
        log(f"verify attempt {attempt + 1}: matched {len(found)}/{len(wanted)}")

    return found


# --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true",
                    help="actually create the tasks in Things")
    ap.add_argument("--include-unassigned", action="store_true",
                    help="also pull to-dos nobody is assigned to")
    ap.add_argument("--all-assignees", action="store_true",
                    help="pull everyone's to-dos, not just yours (noisy)")
    ap.add_argument("--accept", default="",
                    help="comma-separated Basecamp ids from the review list to "
                         "accept as correct matches, e.g. --accept 204,206")
    ap.add_argument("--create-anyway", default="",
                    help="comma-separated Basecamp ids from the review list that "
                         "are NOT the same thing -- import them as new tasks")
    ap.add_argument("--close-in-things", action="store_true",
                    help="tick off Things tasks whose Basecamp to-do is done. "
                         "Needs THINGS_AUTH_TOKEN set.")
    args = ap.parse_args()

    todos = fetch_basecamp_todos(args.include_unassigned, args.all_assignees)
    open_count = sum(1 for t in todos if not t["completed"])
    print(f"Basecamp to-dos in play: {len(todos)}  ({open_count} open)")

    things_tasks = read_things_tasks()
    print(f"Live tasks and projects in Things: {len(things_tasks)}\n")

    accept = {i.strip() for i in args.accept.split(",") if i.strip()}
    force_create = {i.strip() for i in args.create_anyway.split(",") if i.strip()}
    overlap = accept & force_create
    if overlap:
        core.die("An id can't be both accepted and created: "
                 + ", ".join(sorted(overlap)))

    links = load_links()
    p = plan(todos, things_tasks, links, accept, force_create)

    settled = {str(t["id"]) for t in p["relink"] + p["create"]}
    for unknown in sorted((accept | force_create) - settled):
        print(f"  note: {unknown} was not waiting for a decision -- ignored")

    for item in p["create"]:
        listname = PROJECT_ROUTING.get(item["project"].strip().lower(), "Inbox")
        due = f"  due {item['due_on']}" if item.get("due_on") else ""
        verb = "WOULD CREATE " if not args.apply else "CREATING     "
        print(f"  {verb}   {item['title']}  ->  {listname}{due}")

    for item in p["relink"]:
        print(f"  ALREADY THERE  {item['title']}  ~  Things: {item['things_title']}  "
              f"({item['confidence']} {item['how']})")

    for item in p["review"]:
        print(f"  NEEDS A CALL   {item['title']}  ~  Things: {item['things_title']}  "
              f"({item['confidence']})")

    for item in p["closed_in_bc"]:
        print(f"  DONE IN BC     {item['things_title']}  is still open in Things")

    for item in p["stale_links"]:
        print(f"  LINK BROKEN    {item['title']}  (Things task was deleted)")

    if p["linked"]:
        print(f"  {len(p['linked'])} already linked and unchanged")

    # ---- writes ----
    created_ok = 0
    if args.apply and p["create"]:
        before = {t["uuid"] for t in things_tasks}
        send_to_things([build_payload(i) for i in p["create"]])
        resolved = resolve_new_uuids(p["create"], before)
        created_ok = len(resolved)

        for item in p["create"]:
            uuid = resolved.get(str(item["id"]))
            if not uuid:
                print(f"  UNVERIFIED     {item['title']}  "
                      "(sent to Things but not found afterwards)")
                log(f"unverified create bc:{item['id']} \"{item['title']}\"")
                continue
            links[str(item["id"])] = {
                "basecamp_title": item["title"],
                "basecamp_project": item["project"],
                "things_uuid": uuid,
                "things_title": item["title"],
                "linked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "source": "imported",
            }
            log(f"created things task for bc:{item['id']} \"{item['title']}\"")

    if args.apply:
        for item in p["relink"] + p["stale_links"]:
            uuid = item.get("things_uuid")
            if not uuid or uuid not in {t["uuid"] for t in things_tasks}:
                continue
            links[str(item["id"])] = {
                "basecamp_title": item["title"],
                "basecamp_project": item["project"],
                "things_uuid": uuid,
                "things_title": item.get("things_title", item["title"]),
                "linked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "source": item.get("how", "matched"),
            }

    closed = 0
    if args.apply and args.close_in_things and p["closed_in_bc"]:
        token = os.environ.get("THINGS_AUTH_TOKEN", "").strip()
        if not token:
            print("\n  Skipped --close-in-things: THINGS_AUTH_TOKEN is not set.\n"
                  "  Things → Settings → General → Enable Things URLs → Manage.")
        else:
            for item in p["closed_in_bc"]:
                if complete_in_things(item["things_uuid"], token):
                    closed += 1
                    log(f"closed things task {item['things_uuid']} "
                        f"(bc:{item['id']} already done)")
                time.sleep(0.4)

    if args.apply:
        save_links(links)

    write_json(REVIEW_PATH, {
        "date": datetime.now(timezone.utc).date().isoformat(),
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "resolved": not p["review"],
        "needs_a_call": p["review"],
        "completed_in_basecamp_open_in_things": p["closed_in_bc"],
        "broken_links": p["stale_links"],
    })

    if p["review"]:
        ids = ",".join(str(i["id"]) for i in p["review"])
        print(f"\n  To settle those: --accept {ids}  (same thing) or "
              f"--create-anyway {ids}  (different things)")

    print()
    if not args.apply and p["create"]:
        print(f"Dry run. {len(p['create'])} would be created in Things "
              "-- rerun with --apply.")
    print(f"created {created_ok} · already there {len(p['relink']) + len(p['linked'])} "
          f"· needs a call {len(p['review'])} · closed in Things {closed}")
    log(f"created={created_ok} relink={len(p['relink'])} linked={len(p['linked'])} "
        f"review={len(p['review'])} closed={closed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
