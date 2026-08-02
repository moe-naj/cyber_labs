# 1-1 — base

> ⚠️ **Educational only.** Intentionally weak. Do not deploy. Use at your own risk. See the [repo disclaimer](../../README.md#-disclaimer).

**Baseline** for track 01: register + login + session. **All weaknesses (W1–W14) are OPEN.**

Later folders are named for the control they add (e.g. basic hashing, salting). Each step closes only the matching W* items.

**Track:** [01-password-auth](../) · **Notes:** [Learnings.md](./Learnings.md)

## Run

```bash
cd 01-password-auth/1-1-base
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

## Weaknesses (W1–W14, all OPEN)

Same IDs as the top of `app.py`:

| ID | Issue | Try / notice |
|----|--------|----------------|
| W1 | Passwords in plaintext | `sqlite3 users.db "SELECT * FROM users;"` or `strings users.db` |
| W2 | No hashing | DB holds the real password |
| W3 | No per-user salt | (nothing to salt yet) |
| W4 | No slow hash | (nothing expensive to crack yet) |
| W5 | Hard-coded `secret_key` | Read it in `app.py` |
| W6 | No rate limit / lockout | Spam login guesses |
| W7 | No password strength rules | Register with `a` |
| W8 | HTTP only (no TLS) | `app.run(...)` has no TLS |
| W9 | `debug=True` | Stack traces / debugger risk |
| W10 | Weak session cookie flags | `SESSION_COOKIE_HTTPONLY/SECURE/SAMESITE` set weak in code |
| W11 | Long-lived permanent session | `PERMANENT_SESSION_LIFETIME` = 365 days; `session.permanent = True` |
| W12 | No session regenerate on login | Login only sets `session["username"]` |
| W13 | User enumeration | Unknown user → `"Unknown username"`; bad pw → `"Wrong password"` |
| W14 | No CSRF tokens | Register/login forms are bare POSTs |

## Naming for later steps

| Planned folder | Implies closed (mainly) |
|----------------|-------------------------|
| `1-2-basic-hashing` | W1, W2 (fast hash, still no salt) |
| `1-3-salting` | W3 |
| `1-4-slow-hash` | W4 (bcrypt/argon2) |
| … | one control / name per step |

Those folders are **not created until the step is built**.
