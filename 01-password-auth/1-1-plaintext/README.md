# 1-1 — Plaintext passwords

> ⚠️ **Educational only.** Intentionally weak. Do not deploy. Use at your own risk. See the [repo disclaimer](../../README.md#-disclaimer).

Tiny app: register + login with a username/password. Built **naive on purpose** so the weaknesses are visible.

**Track:** [01-password-auth](../) · **Next:** [1-2-unsalted-hash](../1-2-unsalted-hash/) (empty)

## Run

```bash
cd 01-password-auth/1-1-plaintext
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

## What exists

| Piece | Role |
|--------|------|
| `POST /register` | create user |
| `POST /login` | check password, set session cookie |
| `GET /me` | "secret" page if logged in |
| `users.db` | SQLite user store |

## Weaknesses to observe

Same IDs as the top of `app.py` (all **OPEN** in 1-1):

| ID | Issue | Try |
|----|--------|-----|
| W1–W4 | Password storage (plaintext / no real hash stack) | `sqlite3 users.db "SELECT * FROM users;"` or `strings users.db` |
| W5 | Hard-coded `secret_key` | Read it in `app.py` |
| W6 | No rate limit | Spam login guesses |
| W7 | No password rules | Register with `a` |
| W8–W9 | HTTP + debug | Note `app.run(...)` |

Later steps mark the fixed IDs **MITIGATED** and leave the rest open.

None of this is "how to build prod auth." It's "what the boring parts are and why people add hashing, lockouts, TLS, etc."

## Ladder from here

| Next step | Upgrade |
|-----------|---------|
| 1-2 | Fast hash, no salt |
| 1-3 | Hash + per-user salt |
| 1-4 | bcrypt / argon2 |
