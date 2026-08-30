# Cyber Labs — Grok notes

Educational password-auth ladder. Intentionally weak early rungs. Do not treat as production code.

## How we work

- One control per folder. If it is not in the step name, it does not get added.
- Weakness IDs **W1–W15** are **append-only** (new IDs at the end; never renumber). Flip only what that step fixed.
- Scaffolding: copy the previous folder, user implements, **then** comments/README/Learnings.
- Teaching mode unless the user asks you to write the patch: Socratic, no surprise implementations. Docstring sweeps wait until the user says so.
- John/hashcat only against **this repo’s lab DBs**, for W4-style demos.

## Git

- User stages with `git add -A` at repo root. Keep `.gitignore` covering env dirs: `.venv/`, `venv/`, `.myenv/`, `myenv/`. Also `*.db`.
- Do not commit venvs, `users.db`, or cracker dump files (`hash`, `hashes.txt`, john.pot).

## Track 01 status (leave-off)

**Done:** 1-1-base, 1-2-basic-hashing, 1-3-salted-hashing, **1-4-slow-hash (W4 bcrypt, MITIGATED)**.

**This session, not necessarily committed yet:** 1-4 implementation + docs; W15 (pepper) appended as OPEN on 1-1…1-4; `.gitignore` `myenv/` + `.myenv/`.

**Next rung (not built):** password-store leftover is **W15 pepper** (`…-pepper`). W5–W14 still OPEN. Same rule: copy 1-4, one control, user implements, then comments/docs.

Read first: `01-password-auth/README.md`, then `01-password-auth/1-4-slow-hash/{README,Learnings,app.py}`.

To continue **this** conversation instead of a fresh tree: `/resume` in the TUI (or `grok --resume` in this directory).
