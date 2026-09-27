# 1-5 — pepper

> ⚠️ **Educational only.** Intentionally weak. Do not deploy. Use at your own risk. See the [repo disclaimer](../../README.md#-disclaimer).

**Control added:** an app **pepper** mixed in before bcrypt on register and login. The pepper is an HMAC-SHA256 key loaded from `app.env`, outside the users table. It is separate from the Flask `secret_key` (W5).

| ID | Status |
|----|--------|
| W1 | MITIGATED — from 1-2; digest, not the password |
| W2 | MITIGATED — from 1-2; one-way hash |
| W3 | MITIGATED — from 1-3; per-hash salt (inside the bcrypt string) |
| W4 | MITIGATED — from 1-4; bcrypt cost 12 |
| W5–W14 | OPEN |
| **W15** | **MITIGATED** — `get_mac` then `bcrypt.hashpw` / `checkpw` |

Same app shape as [1-4-slow-hash](../1-4-slow-hash/): register + login + session. Only the bytes passed into bcrypt changed.

**Track:** [01-password-auth](../) · **Notes:** [Learnings.md](./Learnings.md)

## Run

```bash
cd 01-password-auth/1-5-pepper
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

`app.env` has to sit next to `app.py` (mode `600`, `[config]` / `pepper` = one base64 line from `openssl rand -base64 32`). `.gitignore` pattern `*.env` skips it, so a fresh clone does not include the pepper. A `users.db` copied from 1-4 will not log in: those rows were bcrypt of the raw password.

## What exists

| Piece | Role |
|--------|------|
| `POST /register` | `hashpw(get_mac(password, pepper), gensalt())`, store the ASCII bcrypt string |
| `POST /login` | same `get_mac`, then `checkpw` (library reads cost + salt out of the stored string) |
| `GET /me` | "secret" page if logged in |
| `users.db` | SQLite user store (`username`, `password_hash`) |
| `app.env` | Pepper file. Not a column in `users` |

## What changed vs 1-4

| Before (1-4) | After (1-5) |
|--------------|-------------|
| `bcrypt.hashpw(password, gensalt())` | `bcrypt.hashpw(HMAC-SHA256(pepper, password), gensalt())` |
| Stolen bcrypt row is enough to start guessing | Guessing also needs the pepper |
| No app secret in the hash | 32-byte key from `app.env` |

Salt and cost are unchanged. Same password still stores two different `$2b$12$…` strings, because each register calls `gensalt()`. The MAC for that shared password is the same.

A copy of this whole directory still includes `app.env`. The lab file is a stand-in for a secret store such as an HSM.

## Try / notice

```bash
# Two registers, same password — two bcrypt strings; both log in
sqlite3 users.db "SELECT username, password_hash FROM users;"
```

John `--format=bcrypt` on a stolen row, without `app.env`, is guessing the 32-byte MAC. A password wordlist does not hit. Use this lab's files only.

## Weaknesses (W1–W15)

Same IDs as the top of `app.py`:

| ID | Status | Issue | Try / notice |
|----|--------|--------|----------------|
| W1 | MITIGATED | Was plaintext storage | DB row is `$2b$12$…`, not the password |
| W2 | MITIGATED | Was no hashing | `hashpw` on register, `checkpw` on login |
| W3 | MITIGATED | Was no per-user salt | Same password → different bcrypt string |
| W4 | MITIGATED | Was fast SHA-256 | bcrypt cost 12 still wraps the MAC |
| W5 | OPEN | Hard-coded `secret_key` | Read it in `app.py`. It is not the pepper |
| W6 | OPEN | No rate limit / lockout | Spam login guesses |
| W7 | OPEN | No password strength rules | Register with `a` |
| W8 | OPEN | HTTP only (no TLS) | `app.run(...)` has no TLS |
| W9 | OPEN | `debug=True` | Stack traces / debugger risk |
| W10 | OPEN | Weak session cookie flags | `SESSION_COOKIE_*` set weak in code |
| W11 | OPEN | Long-lived permanent session | 365 days; `session.permanent = True` |
| W12 | OPEN | No session regenerate on login | Login only sets `session["username"]` |
| W13 | OPEN | User enumeration | `"Unknown username"` vs `"Wrong password"` |
| W14 | OPEN | No CSRF tokens | Register/login forms are bare POSTs |
| W15 | **MITIGATED** | Was no pepper | HMAC key is in `app.env`, outside `users` |

## Naming for later steps

| Planned folder | Implies closed (mainly) |
|----------------|-------------------------|
| … | one control / name per step |

Those folders are **not created until the step is built**. W5–W14 are still open. This track has not named the next folder.
