#!/usr/bin/env python3
"""
Regression test for things_basecamp_sync.py.

Builds a synthetic Things 3 database and a fake Basecamp CLI, then runs the real
sync against them. This verifies the parts that can't be checked by reading the
code: the SQL (status codes, Core Data timestamp math, the exclusion filters),
the CLI plumbing, and that --apply completes exactly the right to-do ids.

    python3 test_things_basecamp_sync.py

Exits non-zero on the first failed assertion.
"""

import importlib.util
import json
import os
import sqlite3
import stat
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CORE_DATA_OFFSET = 978307200

FAKE_CLI = '''#!/usr/bin/env python3
import json, os, sys
args = sys.argv[1:]
store = os.environ["FAKE_BC_DIR"]
if args[:2] == ["projects", "list"]:
    print(json.dumps({"data": json.load(open(os.path.join(store, "projects.json")))}))
elif args[:2] == ["todos", "list"]:
    pid = args[args.index("--in") + 1]
    todos = json.load(open(os.path.join(store, "todos.json")))
    print(json.dumps({"data": [t for t in todos if str(t["_project_id"]) == pid]}))
elif args[:2] == ["todos", "complete"]:
    with open(os.path.join(store, "completed.log"), "a") as fh:
        fh.write(args[2] + "\\n")
    print(json.dumps({"ok": True}))
else:
    sys.stderr.write("unknown subcommand: %s\\n" % " ".join(args))
    sys.exit(2)
'''


def build_things_db(path):
    """A Things DB holding one row for every case the query must handle."""
    now = time.time()

    def cd(hours_ago):
        return (now - hours_ago * 3600) - CORE_DATA_OFFSET

    conn = sqlite3.connect(path)
    conn.execute(
        "CREATE TABLE TMTask (uuid TEXT PRIMARY KEY, title TEXT, notes TEXT, "
        "status INTEGER, trashed INTEGER, type INTEGER, stopDate REAL, dueDate REAL)"
    )
    rows = [
        # (uuid, title, status, trashed, type, stopDate, should_be_returned, why)
        ("u1", "Film all tools in Loom for new Growth Plan", 3, 0, 0, cd(2), True, "completed, in window"),
        ("u2", "Edit Healthy Volunteer Culture and assets", 3, 0, 0, cd(50), True, "completed, in window"),
        ("u3", "New Rule of Life", 3, 0, 0, cd(100), True, "completed, in window"),
        ("u4", "Buy milk", 3, 0, 0, cd(5), True, "completed, no Basecamp twin"),
        ("u5", "Ancient finished thing", 3, 0, 0, cd(900), False, "outside the 336h window"),
        ("u6", "Still open task", 0, 0, 0, None, False, "status 0 = incomplete"),
        ("u7", "Cancelled task", 2, 0, 0, cd(3), False, "status 2 = canceled, not completed"),
        ("u8", "Trashed but completed", 3, 1, 0, cd(3), False, "trashed"),
        ("u9", "Some Heading", 3, 0, 2, cd(3), False, "type 2 = heading, not a task"),
        ("u10", "---- separator", 3, 0, 0, cd(3), False, "---- title convention"),
        ("u11", "Completed with null stopDate", 3, 0, 0, None, False, "no stopDate"),
        ("u12", "3rd Kid: Second Conversation", 3, 0, 0, cd(20), True, "completed, in window"),
    ]
    for uuid, title, status, trashed, type_, stop, _, _ in rows:
        conn.execute(
            "INSERT INTO TMTask (uuid, title, status, trashed, type, stopDate) "
            "VALUES (?,?,?,?,?,?)",
            (uuid, title, status, trashed, type_, stop),
        )
    conn.commit()
    conn.close()
    return rows


def build_fake_cli(store):
    projects = [{"id": 7001, "name": "Momentum Staff HQ"},
                {"id": 7002, "name": "Emily // Hunter"}]
    todos = [
        {"_project_id": 7001, "id": 101, "title": "Film all tools in Loom for new Growth Plan",
         "completed": False, "assignees": [{"name": "Hunter Wilson"}]},
        {"_project_id": 7001, "id": 102, "title": "Edit Healthy Volunteer Culture and assets (45 min)",
         "completed": False, "assignees": [{"name": "Hunter Wilson"}]},
        {"_project_id": 7001, "id": 103, "title": "Create a Video Sales Letter",
         "completed": True, "assignees": [{"name": "Hunter Wilson"}]},
        {"_project_id": 7001, "id": 104, "title": "Something owned by Mark",
         "completed": False, "assignees": [{"name": "Mark Brewer"}]},
        {"_project_id": 7002, "id": 105, "title": "Hunter: Rule of Life",
         "completed": False, "assignees": [{"name": "Hunter Wilson"}]},
        {"_project_id": 7002, "id": 106, "title": "3rd Kid: Second Conversation",
         "completed": False, "assignees": [{"name": "Hunter Wilson"}]},
    ]
    json.dump(projects, open(os.path.join(store, "projects.json"), "w"))
    json.dump(todos, open(os.path.join(store, "todos.json"), "w"))
    cli = os.path.join(store, "basecamp")
    with open(cli, "w") as fh:
        fh.write(FAKE_CLI)
    os.chmod(cli, os.stat(cli).st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    return cli


def load_module(db_path, cli_path, queue_path, log_path):
    spec = importlib.util.spec_from_file_location(
        "sync", os.path.join(HERE, "things_basecamp_sync.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.THINGS_DB_GLOB = db_path
    mod.BASECAMP_BIN = cli_path
    mod.CMD_PROJECTS = [cli_path, "projects", "list", "--json"]
    mod.CMD_TODOS = [cli_path, "todos", "list", "--in", "{project_id}", "--json"]
    mod.CMD_COMPLETE = [cli_path, "todos", "complete", "{todo_id}"]
    mod.QUEUE_PATH = queue_path
    mod.LOG_PATH = log_path
    return mod


FAILURES = []


def check(label, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {label}" + (f"   {detail}" if detail and not ok else ""))
    if not ok:
        FAILURES.append(label)


def main():
    tmp = tempfile.mkdtemp()
    store = os.path.join(tmp, "bc"); os.makedirs(store)
    db = os.path.join(tmp, "main.sqlite")
    queue = os.path.join(tmp, "things-completions.json")
    logf = os.path.join(tmp, "sync.log")

    rows = build_things_db(db)
    cli = build_fake_cli(store)
    os.environ["FAKE_BC_DIR"] = store
    mod = load_module(db, cli, queue, logf)

    print("\n[1] Things query — status codes, window, and exclusions")
    got = {c["title"] for c in mod.read_things_completions(336)}
    for uuid, title, *_rest, expected, why in [(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]) for r in rows]:
        check(f"{'include' if expected else 'exclude'} {title!r} ({why})",
              (title in got) == expected)

    print("\n[2] Basecamp CLI plumbing")
    todos = mod.fetch_open_basecamp_todos()
    ids = {t["id"] for t in todos}
    check("parses projects + todos across both projects", len(todos) == 4, str(ids))
    check("drops already-completed to-dos (id 103)", 103 not in ids)
    check("drops to-dos assigned to someone else (id 104)", 104 not in ids)
    check("keeps Hunter's to-dos", {101, 102, 105, 106} <= ids, str(ids))

    print("\n[3] Matching")
    done = mod.read_things_completions(336)
    conf, amb, un = mod.match(done, todos)
    conf_ids = {c["basecamp_id"] for c in conf}
    check("auto-completes exact match (101)", 101 in conf_ids)
    check("auto-completes across stripped '(45 min)' suffix (102)", 102 in conf_ids)
    check("auto-completes exact match with colon (106)", 106 in conf_ids)
    check("queues 'New Rule of Life' vs 'Hunter: Rule of Life' instead of guessing",
          any(a["basecamp_id"] == 105 for a in amb), str([a['basecamp_id'] for a in amb]))
    check("leaves 'Buy milk' unmatched", any(u["title"] == "Buy milk" for u in un))

    print("\n[4] Dry run writes nothing to Basecamp")
    sys.argv = ["x", "--hours", "336"]
    mod.main()
    completed_log = os.path.join(store, "completed.log")
    check("no completions sent", not os.path.exists(completed_log))
    q = json.load(open(queue))
    check("queue synced=false while work is pending", q["synced"] is False)
    check("pending completions recorded", len(q["completions"]) == 3, str(len(q["completions"])))
    check("ambiguous recorded for review", len(q["ambiguous"]) == 1)

    print("\n[5] --apply completes exactly the confident ids")
    sys.argv = ["x", "--hours", "336", "--apply"]
    mod.main()
    sent = [l.strip() for l in open(completed_log)] if os.path.exists(completed_log) else []
    check("completed exactly 101, 102, 106", sorted(sent) == ["101", "102", "106"], str(sent))
    check("did NOT complete the ambiguous 105", "105" not in sent)
    q = json.load(open(queue))
    check("queue synced=true once pushed", q["synced"] is True)
    check("applied recorded for audit", len(q["applied"]) == 3)

    print("\n[6] Missing Things DB fails loudly, not silently")
    mod2 = load_module(os.path.join(tmp, "nope-*.sqlite"), cli, queue, logf)
    try:
        mod2.read_things_completions(48)
        check("raises on missing DB", False, "returned normally")
    except SystemExit:
        check("raises on missing DB with a real message", True)

    print()
    if FAILURES:
        print(f"{len(FAILURES)} FAILED: {FAILURES}")
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
