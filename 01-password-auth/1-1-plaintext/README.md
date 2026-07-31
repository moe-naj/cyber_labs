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

Do these yourself after registering a user:

1. **Passwords stored in plaintext** — open the DB:
   ```bash
   sqlite3 users.db "SELECT * FROM users;"
   # or: strings users.db
   ```
2. **No rate limit** — spam login guesses; nothing blocks you.
3. **HTTP only** — traffic is cleartext on the wire (fine on localhost; deadly on a real network).
4. **Weak/no password rules** — `a` is a valid password.
5. **Session cookie is simple** — signed with a hard-coded secret in source.

None of this is "how to build prod auth." It's "what the boring parts are and why people add hashing, lockouts, TLS, etc."

## Ladder from here

| Next step | Upgrade |
|-----------|---------|
| 1-2 | Fast hash, no salt |
| 1-3 | Hash + per-user salt |
| 1-4 | bcrypt / argon2 |
