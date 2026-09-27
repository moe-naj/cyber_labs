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

**Done:** 1-1-base, 1-2-basic-hashing, 1-3-salted-hashing, 1-4-slow-hash (W4 bcrypt), **1-5-pepper (W15 pepper, MITIGATED)**.

**This session, not necessarily committed yet:** 1-5 implementation + comments, README, and Learnings. Pepper file is `1-5-pepper/app.env` (mode 600, gitignored by `*.env`). `.gitignore` uses `*.env`, which also covers `app.env`.

**Next rung (not built):** not named. Password-store items in this track (W1–W4, W15) are mitigated on 1-5. W5–W14 still OPEN. Same rule: copy 1-5, one control, user implements, then comments/docs.

Read first: `01-password-auth/README.md`, then `01-password-auth/1-5-pepper/{README,Learnings,app.py}`.

To continue **this** conversation instead of a fresh tree: `/resume` in the TUI (or `grok --resume` in this directory).
