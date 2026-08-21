#!/usr/bin/env python3
"""
Regression test for basecamp_things_import.py.

Builds a synthetic Things 3 database, a fake Basecamp CLI, and a fake `open`
that actually applies the things:/// URL to the database -- so the round trip
is really exercised, not just the half of it we can see.

The test that matters most is section 8: running twice must not create
anything the second time. A sync that duplicates on every run is worse than
no sync at all.

    python3 test_basecamp_things_import.py

Exits non-zero if any check fails.
"""

import importlib.util
import json
import os
import sqlite3
import stat
import sys
import tempfile
import time
import uuid as uuidlib

HERE = os.path.dirname(os.path.abspath(__file__))
CORE_DATA_OFFSET = 978307200

FAKE_BC_CLI = '''#!/usr/bin/env python3
import json, os, sys
args = sys.argv[1:]
store = os.environ["FAKE_BC_DIR"]
if args[:2] == ["projects", "list"]:
    print(json.dumps({"data": json.load(open(os.path.join(store, "projects.json")))}))
elif args[:2] == ["todos", "list"]:
    pid = args[args.index("--in") + 1]
    todos = json.load(open(os.path.join(store, "todos.json")))
    print(json.dumps({"data": [t for t in todos if str(t["_project_id"]) == pid]}))
else:
    sys.stderr.write("unknown subcommand: %s\\n" % " ".join(args))
    sys.exit(2)
'''

# Stands in for macOS `open`. Applies the URL to the synthetic Things DB the
# way Things itself would, so resolve_new_uuids() has something real to find.
FAKE_OPEN = '''#!/usr/bin/env python3
import json, os, sqlite3, sys, time, urllib.parse, uuid as uuidlib
CD = 978307200
db = os.environ["FAKE_THINGS_DB"]
url = [a for a in sys.argv[1:] if a.startswith("things:")][0]
with open(os.environ["FAKE_OPEN_LOG"], "a") as fh:
    fh.write(url + "\\n")
parsed = urllib.parse.urlparse(url)
q = urllib.parse.parse_qs(parsed.query)
conn = sqlite3.connect(db)
if parsed.path.lstrip("/") == "json":
    for op in json.loads(q["data"][0]):
        a = op["attributes"]
        conn.execute(
            "INSERT INTO TMTask (uuid,title,notes,status,trashed,type,stopDate,creationDate)"
            " VALUES (?,?,?,0,0,0,NULL,?)",
            (str(uuidlib.uuid4()).upper(), a["title"], a.get("notes", ""),
             time.time() - CD))
elif parsed.path.lstrip("/") == "update":
    conn.execute("UPDATE TMTask SET status=3, stopDate=? WHERE uuid=?",
                 (time.time() - CD, q["id"][0]))
conn.commit()
conn.close()
'''


def build_things_db(path):
    """Hunter's real Things structure: Areas hold projects, projects hold to-dos."""
    now = time.time()

    def cd(hours_ago):
        return (now - hours_ago * 3600) - CORE_DATA_OFFSET

    conn = sqlite3.connect(path)
    conn.execute(
        "CREATE TABLE TMTask (uuid TEXT PRIMARY KEY, title TEXT, notes TEXT, "
        "status INTEGER, trashed INTEGER, type INTEGER, stopDate REAL, "
        "dueDate REAL, creationDate REAL)"
    )
    rows = [
        # (uuid, title, notes, status, trashed, type, stopDate, visible, why)
        ("t1", "Growth Plan v2", "", 0, 0, 1, None, True, "open project"),
        ("t2", "RSG VSL", "", 0, 0, 1, None, True, "open project"),
        ("t3", "Rule of Life", "", 0, 0, 1, None, True, "open project"),
        ("t4", "Short-form video", "", 0, 0, 0, None, True, "open to-do"),
        ("t5", "Buy milk", "", 0, 0, 0, None, True, "open to-do, personal"),
        ("t6", "Edit Healthy Volunteer Culture and assets", "", 3, 0, 0, cd(100),
         True, "completed recently, still a duplicate risk"),
        ("t7", "Ancient finished thing", "", 3, 0, 0, cd(2000), False,
         "completed long ago, outside the dedupe window"),
        ("t8", "Some Heading", "", 0, 0, 2, None, False, "type 2 = heading"),
        ("t9", "---- separator", "", 0, 0, 0, None, False, "---- convention"),
        ("t10", "Trashed thing", "", 0, 1, 0, None, False, "trashed"),
    ]
    for u, title, notes, status, trashed, type_, stop, _, _ in rows:
        conn.execute(
            "INSERT INTO TMTask (uuid,title,notes,status,trashed,type,stopDate,creationDate)"
            " VALUES (?,?,?,?,?,?,?,?)",
            (u, title, notes, status, trashed, type_, stop, cd(5000)))
    conn.commit()
    conn.close()
    return rows


def build_fake_bc(store):
    """Titles taken from TASKS.md and the Things 3 setup guide, not invented."""
    projects = [{"id": 7001, "name": "Momentum Staff HQ"},
                {"id": 7002, "name": "Emily // Hunter"},
                {"id": 7003, "name": "Content Tracking"}]
    H = [{"name": "Hunter Wilson"}]
    todos = [
        # New work with no Things counterpart -- these should be created.
        {"_project_id": 7001, "id": 201, "completed": False, "assignees": H,
         "title": "Rebuild the GP Google Doc toolkits and send to Mark and Emily",
         "due_on": "2026-08-26", "app_url": "https://3.basecamp.com/1/todos/201"},
        {"_project_id": 7003, "id": 202, "completed": False, "assignees": H,
         "title": "Outline Keeping First Time Guests (Engagement Pathway) (1 hr)",
         "due_on": None},
        {"_project_id": 7002, "id": 203, "completed": False, "assignees": H,
         "title": "3rd Kid: Second Conversation", "due_on": None},
        # Already in Things as a project -- must NOT be duplicated.
        {"_project_id": 7001, "id": 204, "completed": False, "assignees": H,
         "title": "Ship Growth Plan v2 flow with Mark Brewer", "due_on": "2026-09-11"},
        # Alias pair: shares no words with "RSG VSL". Must not duplicate.
        {"_project_id": 7001, "id": 205, "completed": False, "assignees": H,
         "title": "Create a Video Sales Letter", "due_on": None},
        # Near-miss against the Things project "Rule of Life" -- ambiguous.
        {"_project_id": 7002, "id": 206, "completed": False, "assignees": H,
         "title": "Hunter: New Rule of Life (Practicing the Way)", "due_on": None},
        # Someone else's work.
        {"_project_id": 7001, "id": 207, "completed": False,
         "assignees": [{"name": "Mark Brewer"}], "title": "Mark reviews the toolkits"},
        # Nobody's work.
        {"_project_id": 7001, "id": 208, "completed": False, "assignees": [],
         "title": "Unassigned housekeeping"},
        # Already done in Basecamp, never in Things -- importing it is noise.
        {"_project_id": 7003, "id": 209, "completed": True, "assignees": H,
         "title": "A-Team Workshop"},
        # Completed in Basecamp, matches an open Things task after linking.
        {"_project_id": 7003, "id": 210, "completed": True, "assignees": H,
         "title": "Short-form video"},
    ]
    json.dump(projects, open(os.path.join(store, "projects.json"), "w"))
    json.dump(todos, open(os.path.join(store, "todos.json"), "w"))
    cli = os.path.join(store, "basecamp")
    open(cli, "w").write(FAKE_BC_CLI)
    os.chmod(cli, os.stat(cli).st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    return cli


def build_fake_open(bindir, db, logpath):
    path = os.path.join(bindir, "open")
    open(path, "w").write(FAKE_OPEN)
    os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    os.environ["FAKE_THINGS_DB"] = db
    os.environ["FAKE_OPEN_LOG"] = logpath
    os.environ["PATH"] = bindir + os.pathsep + os.environ["PATH"]


def load_module(db, cli, links, review, logf):
    spec = importlib.util.spec_from_file_location(
        "importer", os.path.join(HERE, "basecamp_things_import.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.core.THINGS_DB_GLOB = db
    mod.core.BASECAMP_BIN = cli
    mod.core.CMD_PROJECTS = [cli, "projects", "list", "--json"]
    mod.core.CMD_TODOS = [cli, "todos", "list", "--in", "{project_id}", "--json"]
    mod.LINKS_PATH = links
    mod.REVIEW_PATH = review
    mod.LOG_PATH = logf
    # Keep the suite fast; the pauses exist for a real Things, not a fake one.
    mod.CHUNK_PAUSE_SECONDS = 0
    mod.VERIFY_PAUSE_SECONDS = 0.01
    return mod


FAILURES = []


def check(label, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {label}" + (f"   {detail}" if detail and not ok else ""))
    if not ok:
        FAILURES.append(label)


def main():
    tmp = tempfile.mkdtemp()
    store = os.path.join(tmp, "bc"); os.makedirs(store)
    bindir = os.path.join(tmp, "bin"); os.makedirs(bindir)
    db = os.path.join(tmp, "main.sqlite")
    links = os.path.join(tmp, "links.json")
    review = os.path.join(tmp, "review.json")
    logf = os.path.join(tmp, "import.log")
    openlog = os.path.join(tmp, "open.log")

    rows = build_things_db(db)
    cli = build_fake_bc(store)
    build_fake_open(bindir, db, openlog)
    os.environ["FAKE_BC_DIR"] = store
    mod = load_module(db, cli, links, review, logf)

    print("\n[1] Things read — projects count, headings and stale completions don't")
    titles = {t["title"] for t in mod.read_things_tasks()}
    for u, title, _n, _s, _t, _ty, _stop, visible, why in rows:
        check(f"{'include' if visible else 'exclude'} {title!r} ({why})",
              (title in titles) == visible)

    print("\n[2] Basecamp read — assignee filtering")
    mine = mod.fetch_basecamp_todos(include_unassigned=False, all_assignees=False)
    ids = {t["id"] for t in mine}
    check("keeps Hunter's to-dos", {201, 202, 203, 204, 205, 206} <= ids, str(sorted(ids)))
    check("drops Mark's to-do (207)", 207 not in ids)
    check("drops unassigned by default (208)", 208 not in ids)
    check("keeps completed to-dos for reconciliation (209, 210)", {209, 210} <= ids)
    check("--include-unassigned picks up 208",
          208 in {t["id"] for t in mod.fetch_basecamp_todos(True, False)})
    check("--all-assignees picks up Mark's 207",
          207 in {t["id"] for t in mod.fetch_basecamp_todos(False, True)})
    check("due date parsed through", next(t for t in mine if t["id"] == 201)["due_on"]
          == "2026-08-26")

    print("\n[3] Payload — routing, tag, marker, dates")
    pay = {t["id"]: mod.build_payload(t) for t in mine if not t["completed"]}
    a201 = pay[201]["attributes"]
    check("Momentum Staff HQ routes to RSG — CEO", a201.get("list") == "RSG — CEO",
          str(a201.get("list")))
    check("Content Tracking routes to RSG — Content",
          pay[202]["attributes"].get("list") == "RSG — Content")
    check("Emily // Hunter routes to Personal",
          pay[203]["attributes"].get("list") == "Personal")
    check("carries the basecamp tag", a201.get("tags") == ["basecamp"])
    check("embeds the [bc:id] marker", "[bc:201]" in a201["notes"])
    check("keeps the Basecamp link in notes",
          "https://3.basecamp.com/1/todos/201" in a201["notes"])
    check("due date becomes the deadline", a201.get("deadline") == "2026-08-26")
    check("when is set two days before the deadline", a201.get("when") == "2026-08-24",
          str(a201.get("when")))
    check("no due date means no deadline", "deadline" not in pay[202]["attributes"])

    print("\n[4] Chunking respects the URL limits")
    many = [mod.build_payload(dict(mine[0], id=900 + i, title=f"Task {i}"))
            for i in range(30)]
    chunks = mod.chunk_payloads(many)
    check("splits 30 into multiple URLs", len(chunks) > 1, str(len(chunks)))
    check("no chunk exceeds the item cap",
          all(len(c) <= mod.MAX_ITEMS_PER_URL for c in chunks))
    check("nothing is dropped in chunking", sum(len(c) for c in chunks) == 30)

    print("\n[5] Plan — what gets created and what gets left alone")
    p = mod.plan(mine, mod.read_things_tasks(), {})
    create_ids = {t["id"] for t in p["create"]}
    relink_ids = {t["id"] for t in p["relink"]}
    review_ids = {t["id"] for t in p["review"]}
    check("creates genuinely new work (201, 202, 203)", {201, 202, 203} <= create_ids,
          str(sorted(create_ids)))
    check("does NOT duplicate the Growth Plan v2 project (204)", 204 not in create_ids)
    check("queues Growth Plan v2 at the same 0.75 the completion sync gives it (204)",
          204 in review_ids, str(sorted(review_ids)))
    check("does NOT duplicate RSG VSL via the alias table (205)", 205 not in create_ids)
    check("links 205 through ALIASES", 205 in relink_ids)
    check("queues the near-miss Rule of Life rather than guessing (206)",
          206 in review_ids, str(sorted(review_ids)))
    check("never creates a to-do already completed in Basecamp (209)",
          209 not in create_ids)

    print("\n[6] Dry run writes nothing")
    sys.argv = ["x"]
    mod.main()
    check("no things:// URL was opened", not os.path.exists(openlog))
    check("no link table written", not os.path.exists(links))
    check("review file written for the ambiguous pair", os.path.exists(review))
    r = json.load(open(review))
    check("review flags it as unresolved", r["resolved"] is False)
    check("review names the ambiguous to-do",
          any(x["id"] == 206 for x in r["needs_a_call"]))

    print("\n[7] --apply creates in Things and records the links")
    before = {t["title"] for t in mod.read_things_tasks()}
    sys.argv = ["x", "--apply"]
    mod.main()
    after = mod.read_things_tasks()
    after_titles = [t["title"] for t in after]
    check("the three new to-dos now exist in Things",
          all(t in after_titles for t in [
              "Rebuild the GP Google Doc toolkits and send to Mark and Emily",
              "Outline Keeping First Time Guests (Engagement Pathway) (1 hr)",
              "3rd Kid: Second Conversation"]), str(sorted(set(after_titles) - before)))
    check("nothing else was created", len(set(after_titles) - before) == 3,
          str(sorted(set(after_titles) - before)))
    saved = json.load(open(links))["links"]
    check("link table records the created tasks", {"201", "202", "203"} <= set(saved))
    check("link table records the matched-not-created one (205)",
          "205" in saved, str(sorted(saved)))
    check("every link resolved to a real uuid",
          all(v["things_uuid"] in {t["uuid"] for t in after} for v in saved.values()))
    check("created links are marked as imported", saved["201"]["source"] == "imported")
    check("matched links are not marked as imported", saved["205"]["source"] != "imported")

    print("\n[7b] Settling a queued pair — --accept and --create-anyway")
    n_before = len(mod.read_things_tasks())
    sys.argv = ["x", "--apply", "--accept", "204", "--create-anyway", "206"]
    mod.main()
    saved = json.load(open(links))["links"]
    check("--accept records the pairing without creating anything",
          "204" in saved and saved["204"]["source"] == "accepted", str(saved.get("204")))
    check("--accept links to the existing Growth Plan v2 project",
          saved.get("204", {}).get("things_uuid") == "t1", str(saved.get("204")))
    check("--create-anyway imports the one that wasn't a match",
          len(mod.read_things_tasks()) == n_before + 1)
    check("the forced import is linked too", "206" in saved)
    r = json.load(open(review))
    check("review queue is empty once both are settled", r["resolved"] is True,
          str([x["id"] for x in r["needs_a_call"]]))
    sys.argv = ["x", "--apply", "--accept", "99999"]
    mod.main()
    check("an id that wasn't queued is ignored, not crashed on", True)

    print("\n[8] Running again is a no-op — the duplication test")
    count_before = len(mod.read_things_tasks())
    sys.argv = ["x", "--apply"]
    mod.main()
    count_after = len(mod.read_things_tasks())
    check("second run creates nothing", count_after == count_before,
          f"{count_before} -> {count_after}")
    p2 = mod.plan(mod.fetch_basecamp_todos(False, False), mod.read_things_tasks(),
                  json.load(open(links))["links"])
    check("plan sees nothing left to create", not p2["create"],
          str([t["id"] for t in p2["create"]]))
    check("marker dedupe works even with the link table emptied",
          not mod.plan(mod.fetch_basecamp_todos(False, False),
                       mod.read_things_tasks(), {})["create"],
          "notes marker should catch these on its own")

    print("\n[9] Reconciling a to-do finished in Basecamp")
    lk = json.load(open(links))["links"]
    t4_uuid = next(t["uuid"] for t in mod.read_things_tasks() if t["title"] == "Short-form video")
    lk["210"] = {"basecamp_title": "Short-form video", "basecamp_project": "Content Tracking",
                 "things_uuid": t4_uuid, "things_title": "Short-form video",
                 "linked_at": "2026-08-21T00:00:00+00:00", "source": "matched"}
    mod.save_links(lk)
    p3 = mod.plan(mod.fetch_basecamp_todos(False, False), mod.read_things_tasks(), lk)
    check("spots the Things task left open after Basecamp closed it",
          any(x["id"] == 210 for x in p3["closed_in_bc"]))
    check("does not close it without --close-in-things",
          next(t for t in mod.read_things_tasks() if t["uuid"] == t4_uuid)["status"] == 0)
    os.environ["THINGS_AUTH_TOKEN"] = "faketoken"
    sys.argv = ["x", "--apply", "--close-in-things"]
    mod.main()
    still = [t for t in mod.read_things_tasks() if t["uuid"] == t4_uuid]
    check("--close-in-things ticks it off",
          not still or still[0]["status"] == 3,
          str(still[0]["status"]) if still else "gone")

    print("\n[10] A broken link is noticed, not ignored")
    lk = json.load(open(links))["links"]
    lk["201"]["things_uuid"] = "DELETED-BY-HAND"
    mod.save_links(lk)
    p4 = mod.plan(mod.fetch_basecamp_todos(False, False), mod.read_things_tasks(), lk)
    check("stale link reported", any(x["id"] == 201 for x in p4["stale_links"]))
    check("marker still prevents a duplicate re-create",
          201 not in {t["id"] for t in p4["create"]},
          "the notes marker should still match")

    print("\n[11] Safety — a missing Things database fails loudly")
    mod.core.THINGS_DB_GLOB = os.path.join(tmp, "nope-*", "main.sqlite")
    try:
        mod.read_things_tasks()
        check("missing database raises rather than returning nothing", False)
    except SystemExit:
        check("missing database raises rather than returning nothing", True)

    print()
    if FAILURES:
        print(f"{len(FAILURES)} FAILED:")
        for f in FAILURES:
            print(f"  - {f}")
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
