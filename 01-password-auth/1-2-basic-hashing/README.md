# 1-2 — basic hashing

> ⚠️ **Educational only.** Intentionally weak. Do not deploy. Use at your own risk. See the [repo disclaimer](../../README.md#-disclaimer).

**Control added:** store and verify **SHA-256** password digests (no salt, not a slow KDF).

| ID | Status |
|----|--------|
| **W1** | **MITIGATED** — DB holds hex digest, not the password |
| **W2** | **MITIGATED** — register + login use `hashlib.sha256` |
| W3–W14 | OPEN — including no salt (W3) and fast hash (W4) |

Same app shape as [1-1-base](../1-1-base/): register + login + session. Only the password store/verify path changed.

**Track:** [01-password-auth](../) · **Notes:** [Learnings.md](./Learnings.md)

## Run

```bash
cd 01-password-auth/1-2-basic-hashing
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

If you still have an old `users.db` from a schema with a `password` column, delete it so `init_db` can create `password_hash`.

## What exists

| Piece | Role |
|--------|------|
| `POST /register` | hash password (SHA-256 hex), insert `password_hash` |
| `POST /login` | hash submitted password, compare digests, set session |
| `GET /me` | "secret" page if logged in |
| `users.db` | SQLite user store (`username`, `password_hash`) |

## What changed vs 1-1

| Before (1-1) | After (1-2) |
|--------------|-------------|
| `INSERT` raw password | `INSERT` `sha256(password).hexdigest()` |
| Login compares plaintext | Login hashes input, compares to `password_hash` |
| `SELECT` shows real password | `SELECT` shows 64-char hex |

## Try / notice

```bash
# After register — digest, not the password
sqlite3 users.db "SELECT username, password_hash FROM users;"

# Same password → same hash (W3 teaser; no salt yet)
# Register alice/password and bob/password; compare digests.

# Fast unsalted SHA-256 is lookup/crack friendly (W4) — e.g. online hash DBs
# for common passwords. That is not "decrypting" SHA-256; it is preimage search.
```

## Weaknesses (W1–W14)

Same IDs as the top of `app.py`:

| ID | Status | Issue | Try / notice |
|----|--------|--------|----------------|
| W1 | **MITIGATED** | Was plaintext storage | DB row is hex, not the password |
| W2 | **MITIGATED** | Was no hashing | `hashlib.sha256` on register + login |
| W3 | OPEN | No per-user salt | Two users, same password → same digest |
| W4 | OPEN | No slow hash | SHA-256 is fast; wordlist/lookup still cheap |
| W5 | OPEN | Hard-coded `secret_key` | Read it in `app.py` |
| W6 | OPEN | No rate limit / lockout | Spam login guesses |
| W7 | OPEN | No password strength rules | Register with `a` |
| W8 | OPEN | HTTP only (no TLS) | `app.run(...)` has no TLS |
| W9 | OPEN | `debug=True` | Stack traces / debugger risk |
| W10 | OPEN | Weak session cookie flags | `SESSION_COOKIE_*` set weak in code |
| W11 | OPEN | Long-lived permanent session | 365 days; `session.permanent = True` |
| W12 | OPEN | No session regenerate on login | Login only sets `session["username"]` |
| W13 | OPEN | User enumeration | `"Unknown username"` vs `"Wrong password"` |
| W14 | OPEN | No CSRF tokens | Register/login forms are bare POSTs |

## Naming for later steps

| Planned folder | Implies closed (mainly) |
|----------------|-------------------------|
| `1-3-salting` | W3 |
| `1-4-slow-hash` | W4 (bcrypt/argon2) |
| … | one control / name per step |

Those folders are **not created until the step is built**.
