# Proposed rewrite: CLAUDE.md "BEFORE EVERY TASK" step 1

**Not applied.** This changes how every session starts, so it's your call. Say the word and I'll swap it in.

---

## Current text

> 1. Check `WORK AREAS/Admin-PA/things-completions.json`. If `synced` is `false` and `completions` is non-empty, silently mark each task complete in Basecamp by exact name match, then update `synced` to `true` in that file. Do this before anything else — no announcement needed unless you hit a mismatch.

## What's wrong with it

**It assumes a capability the session may not have.** Marking something complete in Basecamp needs the `basecamp` CLI, which only exists on your Mac. In a remote session the instruction is unrunnable, and nothing in the wording tells the session to notice that. It just silently does nothing.

**"Exact name match" is the wrong matching rule.** Your Things titles don't equal your Basecamp titles. `New Rule of Life` vs `Hunter: Rule of Life`. `Edit Healthy Volunteer Culture and assets` vs the same thing with `(45 min)` on the end. Exact matching finds neither. The script's normalized matching finds both.

**It puts an LLM in a mechanical path.** Reading a queue and calling a CLI per row is deterministic work. It should run on a timer and be reviewable in a log, not depend on a session starting.

---

## Proposed replacement

> 1. Check `WORK AREAS/Admin-PA/things-completions.json`.
>
>    The hourly sync script on the Mac handles confident matches on its own — you don't push those. Your job is only the leftovers:
>
>    - **`ambiguous` is non-empty** → these are Things completions the script matched to a Basecamp to-do but wasn't sure enough to tick. Ask me about them, one at a time, showing the Things title, the Basecamp candidate, and the confidence. Don't guess and don't batch them into one question.
>    - **`completions` is non-empty and `synced` is `false`** → the script matched these confidently but couldn't push them (it ran dry, or Basecamp errored). If `~/.local/bin/basecamp` exists in this session, push them with `basecamp todos complete <basecamp_id>` and set `synced` to `true`. If it doesn't exist, say so in one line and leave the file alone — do not mark it synced.
>    - **Everything empty, or `synced` is `true`** → nothing to do. Say nothing.
>
>    Never mark the file synced for work you didn't actually do.

---

## Why this shape

- **Names the capability check.** A remote session says "can't reach Basecamp from here" instead of failing silently. That was the actual bug — not a missing mechanism, a missing signal.
- **Stops it lying.** The old rule set `synced: true` as a matter of course. The new one forbids that unless the completion really landed.
- **Ambiguity gets a human.** The script deliberately refuses to guess between two close candidates. This is where that refusal gets resolved — and one question at a time, per your no-multiple-questions rule.
- **Silence when there's nothing to say**, which is what you asked for originally.
