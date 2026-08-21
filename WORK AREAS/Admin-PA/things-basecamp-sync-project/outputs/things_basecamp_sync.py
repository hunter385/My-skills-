#!/usr/bin/env python3
"""
Things 3 -> Basecamp completion sync.

Reads what you completed in Things 3, finds the matching Basecamp to-do, and
completes it. High-confidence matches are applied automatically. Anything
ambiguous is written to a queue for Claude to resolve in the next session.

MUST run on the Mac. Things 3 has no web API -- it is a local SQLite database,
so this cannot run in a remote CoWork session.

Dry run by default. Nothing is written to Basecamp unless you pass --apply.

    python3 things_basecamp_sync.py                 # show what would happen
    python3 things_basecamp_sync.py --apply         # actually complete them
    python3 things_basecamp_sync.py --hours 168     # look back a week

Requires: python3 (stdlib only) and the 37signals basecamp CLI, authenticated.
"""

from __future__ import annotations

import argparse
import difflib
import glob
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone

# --------------------------------------------------------------------------
# Config -- adjust these two blocks if your setup differs.
# --------------------------------------------------------------------------

# Where the queue file lives, so Claude can pick up whatever needs a decision.
QUEUE_PATH = os.path.expanduser(
    "~/Desktop/Hunter Wilson/WORK AREAS/Admin-PA/things-completions.json"
)
LOG_PATH = os.path.expanduser(
    "~/Desktop/Hunter Wilson/WORK AREAS/Admin-PA/things-basecamp-sync.log"
)

BASECAMP_BIN = os.path.expanduser("~/.local/bin/basecamp")

# Basecamp CLI command shapes. If your installed CLI differs, fix them here --
# the script prints the exact failing command so you can see what to change.
CMD_PROJECTS = [BASECAMP_BIN, "projects", "list", "--json"]
CMD_TODOS = [BASECAMP_BIN, "todos", "list", "--in", "{project_id}", "--json"]
CMD_COMPLETE = [BASECAMP_BIN, "todos", "complete", "{todo_id}"]

# Only sync to-dos assigned to this person. Set to None to consider all to-dos.
ASSIGNEE = "Hunter"

# Core Data stores timestamps as seconds since 2001-01-01, not 1970-01-01.
CORE_DATA_EPOCH_OFFSET = 978307200

# Things 3 TMTask.status: 0 = incomplete, 2 = canceled, 3 = completed.
# See https://thingsapi.github.io/things.py/things/database.html
STATUS_COMPLETED = 3

# TMTask.type: 0 = to-do, 1 = project, 2 = heading. Headings are not tasks.
TYPE_HEADING = 2

# Match confidence. Above AUTO we complete it; between REVIEW and AUTO we ask.
AUTO_THRESHOLD = 0.90
REVIEW_THRESHOLD = 0.72

THINGS_DB_GLOB = os.path.expanduser(
    "~/Library/Group Containers/JLMPQHK86H.com.culturedcode.ThingsMac/"
    "ThingsData-*/Things Database.thingsdatabase/main.sqlite"
)

# Prefixes Basecamp to-dos carry that Things titles won't, e.g. "Hunter: Rule of Life".
STRIP_PREFIXES = ("hunter:", "hunter -", "hunter —", "hw:")


# --------------------------------------------------------------------------
# Things
# --------------------------------------------------------------------------

def find_things_db() -> str:
    matches = sorted(glob.glob(THINGS_DB_GLOB))
    if not matches:
        die(
            "Could not find the Things database.\n"
            f"  Looked for: {THINGS_DB_GLOB}\n"
            "  If Things is installed, the ThingsData-XXXXX folder name differs -- "
            "check the path and update THINGS_DB_GLOB."
        )
    return matches[-1]


def read_things_completions(hours: int) -> list[dict]:
    """Tasks completed in Things within the last `hours`."""
    src = find_things_db()

    # Copy before reading. Things holds the live DB open, and a copy sidesteps
    # any lock or partial-write weirdness entirely.
    with tempfile.TemporaryDirectory() as tmp:
        copy = os.path.join(tmp, "things.sqlite")
        shutil.copy2(src, copy)
        for suffix in ("-wal", "-shm"):
            if os.path.exists(src + suffix):
                shutil.copy2(src + suffix, copy + suffix)

        cutoff_core_data = (time.time() - hours * 3600) - CORE_DATA_EPOCH_OFFSET

        conn = sqlite3.connect(f"file:{copy}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        try:
            rows = conn.execute(
                """
                SELECT uuid, title, stopDate
                FROM TMTask
                WHERE status = ?
                  AND trashed = 0
                  AND type != ?
                  AND stopDate IS NOT NULL
                  AND stopDate > ?
                ORDER BY stopDate DESC
                """,
                (STATUS_COMPLETED, TYPE_HEADING, cutoff_core_data),
            ).fetchall()
        finally:
            conn.close()

    out = []
    for r in rows:
        title = (r["title"] or "").strip()
        if not title or title.startswith("----"):
            continue
        completed_at = datetime.fromtimestamp(
            r["stopDate"] + CORE_DATA_EPOCH_OFFSET, tz=timezone.utc
        )
        out.append(
            {
                "things_uuid": r["uuid"],
                "title": title,
                "completed_at": completed_at.isoformat(),
            }
        )
    return out


# --------------------------------------------------------------------------
# Basecamp
# --------------------------------------------------------------------------

def run_cli(cmd: list[str]) -> str:
    if not os.path.exists(BASECAMP_BIN):
        die(
            f"Basecamp CLI not found at {BASECAMP_BIN}\n"
            "  Install it:  curl -fsSL https://basecamp.com/install-cli | bash\n"
            "  Then:        basecamp auth"
        )
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    except subprocess.TimeoutExpired:
        die(f"Basecamp CLI timed out.\n  Command: {' '.join(cmd)}")
    if proc.returncode != 0:
        die(
            "Basecamp CLI failed.\n"
            f"  Command: {' '.join(cmd)}\n"
            f"  Exit:    {proc.returncode}\n"
            f"  Stderr:  {proc.stderr.strip()}\n"
            "  If the subcommand shape is wrong for your CLI version, fix the "
            "CMD_* constants at the top of this script."
        )
    return proc.stdout


def parse_json(raw: str, what: str) -> list[dict]:
    raw = raw.strip()
    if not raw:
        return []
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        die(f"Could not parse Basecamp {what} as JSON: {exc}\n  Got: {raw[:400]}")
    if isinstance(data, dict):
        data = data.get("data", data.get("results", []))
    return data if isinstance(data, list) else []


def fetch_open_basecamp_todos() -> list[dict]:
    """Every incomplete to-do assigned to ASSIGNEE, across all projects."""
    projects = parse_json(run_cli(CMD_PROJECTS), "projects")
    todos = []

    for proj in projects:
        pid = proj.get("id")
        if pid is None:
            continue
        pname = proj.get("name") or proj.get("title") or str(pid)

        cmd = [part.replace("{project_id}", str(pid)) for part in CMD_TODOS]
        for todo in parse_json(run_cli(cmd), f"to-dos for {pname}"):
            if todo.get("completed"):
                continue
            title = (todo.get("title") or todo.get("content") or "").strip()
            if not title:
                continue
            if ASSIGNEE:
                names = [
                    (a.get("name") or "")
                    for a in (todo.get("assignees") or [])
                    if isinstance(a, dict)
                ]
                # Keep unassigned to-dos in play; only drop ones owned by others.
                if names and not any(ASSIGNEE.lower() in n.lower() for n in names):
                    continue
            todos.append({"id": todo.get("id"), "title": title, "project": pname})

    return todos


def complete_basecamp_todo(todo_id) -> None:
    run_cli([part.replace("{todo_id}", str(todo_id)) for part in CMD_COMPLETE])


# --------------------------------------------------------------------------
# Matching
# --------------------------------------------------------------------------

def normalize(title: str) -> str:
    t = title.strip().lower()
    for prefix in STRIP_PREFIXES:
        if t.startswith(prefix):
            t = t[len(prefix):]
            break
    t = re.sub(r"\((?:\d+\s*(?:min|mins|minutes|hr|hrs|hour|hours))\)", " ", t)
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return " ".join(t.split())


def score(a: str, b: str) -> float:
    na, nb = normalize(a), normalize(b)
    if not na or not nb:
        return 0.0
    if na == nb:
        return 1.0
    return difflib.SequenceMatcher(None, na, nb).ratio()


def match(done: list[dict], todos: list[dict]) -> tuple[list, list, list]:
    """Split Things completions into (confident, ambiguous, unmatched)."""
    confident, ambiguous, unmatched = [], [], []
    claimed = set()

    for item in done:
        scored = sorted(
            ((score(item["title"], t["title"]), t) for t in todos),
            key=lambda pair: pair[0],
            reverse=True,
        )
        scored = [(s, t) for s, t in scored if t["id"] not in claimed]

        if not scored or scored[0][0] < REVIEW_THRESHOLD:
            unmatched.append(item)
            continue

        best_score, best = scored[0]
        runner_up = scored[1][0] if len(scored) > 1 else 0.0

        candidate = {
            **item,
            "basecamp_id": best["id"],
            "basecamp_title": best["title"],
            "basecamp_project": best["project"],
            "confidence": round(best_score, 3),
        }

        # Two near-equal candidates means we genuinely don't know which one.
        too_close = best_score - runner_up < 0.05 and runner_up >= REVIEW_THRESHOLD

        if best_score >= AUTO_THRESHOLD and not too_close:
            claimed.add(best["id"])
            confident.append(candidate)
        else:
            candidate["reason"] = (
                "two candidates scored within 0.05 of each other"
                if too_close
                else f"confidence {best_score:.2f} below the {AUTO_THRESHOLD} auto threshold"
            )
            candidate["other_candidates"] = [
                {"basecamp_id": t["id"], "basecamp_title": t["title"],
                 "basecamp_project": t["project"], "confidence": round(s, 3)}
                for s, t in scored[1:4]
            ]
            ambiguous.append(candidate)

    return confident, ambiguous, unmatched


# --------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------

def write_queue(applied, pending, ambiguous, unmatched) -> None:
    payload = {
        "date": datetime.now(timezone.utc).date().isoformat(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        # synced=false only when there is something Claude still needs to push.
        "synced": not pending,
        "completions": pending,
        "applied": applied,
        "ambiguous": ambiguous,
        "unmatched": unmatched,
    }
    os.makedirs(os.path.dirname(QUEUE_PATH), exist_ok=True)
    tmp = QUEUE_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
        fh.write("\n")
    os.replace(tmp, QUEUE_PATH)


def log(line: str) -> None:
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    try:
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        with open(LOG_PATH, "a", encoding="utf-8") as fh:
            fh.write(f"{stamp}  {line}\n")
    except OSError:
        pass


def die(msg: str) -> None:
    print(f"\nStopped: {msg}\n", file=sys.stderr)
    log(f"ERROR {msg.splitlines()[0]}")
    sys.exit(1)


# --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--hours", type=int, default=48,
                    help="how far back to look for Things completions (default 48)")
    ap.add_argument("--apply", action="store_true",
                    help="actually complete the matched to-dos in Basecamp")
    args = ap.parse_args()

    done = read_things_completions(args.hours)
    if not done:
        print(f"Nothing completed in Things in the last {args.hours}h.")
        write_queue([], [], [], [])
        log(f"no completions in last {args.hours}h")
        return 0

    print(f"Completed in Things (last {args.hours}h): {len(done)}")

    todos = fetch_open_basecamp_todos()
    print(f"Open Basecamp to-dos in play: {len(todos)}\n")

    confident, ambiguous, unmatched = match(done, todos)

    applied, pending, failed = [], [], []
    for item in confident:
        label = f"{item['title']}  ->  {item['basecamp_project']} / {item['basecamp_title']}"
        if not args.apply:
            print(f"  WOULD COMPLETE  {label}  ({item['confidence']})")
            pending.append(item)
            continue
        try:
            complete_basecamp_todo(item["basecamp_id"])
        except SystemExit:
            print(f"  FAILED          {label}")
            failed.append(item)
            log(f"FAILED {item['basecamp_id']} {item['basecamp_title']}")
        else:
            print(f"  COMPLETED       {label}  ({item['confidence']})")
            applied.append(item)
            log(f"completed bc:{item['basecamp_id']} \"{item['basecamp_title']}\" "
                f"from things \"{item['title']}\"")

    for item in ambiguous:
        print(f"  NEEDS A CALL    {item['title']}  ~  "
              f"{item['basecamp_project']} / {item['basecamp_title']}  "
              f"({item['confidence']} -- {item['reason']})")

    for item in unmatched:
        print(f"  no match        {item['title']}")

    write_queue(applied, pending + failed, ambiguous, unmatched)

    print()
    if not args.apply and pending:
        print(f"Dry run. {len(pending)} would be completed -- rerun with --apply.")
    print(f"applied {len(applied)} · pending {len(pending + failed)} · "
          f"needs a call {len(ambiguous)} · no match {len(unmatched)}")
    log(f"applied={len(applied)} pending={len(pending + failed)} "
        f"ambiguous={len(ambiguous)} unmatched={len(unmatched)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
