# 1-3 — salted hashing

> ⚠️ **Educational only.** Intentionally weak. Do not deploy. Use at your own risk. See the [repo disclaimer](../../README.md#-disclaimer).

**Control added:** unique **per-user random salt** mixed into SHA-256 (still not a slow KDF).

| ID | Status |
|----|--------|
| W1 | MITIGATED — from 1-2; digest, not the password |
| W2 | MITIGATED — from 1-2; `hashlib.sha256` |
| **W3** | **MITIGATED** — `os.urandom(16)` per user; hash is SHA-256(salt \|\| password) |
| W4–W14 | OPEN — including fast hash (W4) |

Same app shape as [1-2-basic-hashing](../1-2-basic-hashing/): register + login + session. Only the salt column and hash construction changed.

**Track:** [01-password-auth](../) · **Notes:** [Learnings.md](./Learnings.md)

## Run

```bash
cd 01-password-auth/1-3-salted-hashing
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

If you still have an old `users.db` without a `salt` column, delete it so `init_db` can create the new schema.

## What exists

| Piece | Role |
|--------|------|
| `POST /register` | new salt, SHA-256(salt \|\| password), insert `salt` + `password_hash` |
| `POST /login` | load that user's salt, hash submitted password the same way, compare digests |
| `GET /me` | "secret" page if logged in |
| `users.db` | SQLite user store (`username`, `password_hash`, `salt`) |

## What changed vs 1-2

| Before (1-2) | After (1-3) |
|--------------|-------------|
| `sha256(password)` | `sha256(salt_bytes \|\| password_bytes)` |
| one column: `password_hash` | `password_hash` + `salt` (hex text) |
| same password → same digest | same password → different digest (different salts) |

Salt is stored in the clear. That is expected: it is not a secret; it only makes each hash unique.

## Try / notice

```bash
# After two registers with the same password — salts differ, hashes differ
sqlite3 users.db "SELECT username, salt, password_hash FROM users;"

# Salt is readable; the password still is not
# Fast salted SHA-256 is still cheap to brute-force per hash (W4)
```

## Weaknesses (W1–W14)

Same IDs as the top of `app.py`:

| ID | Status | Issue | Try / notice |
|----|--------|--------|----------------|
| W1 | MITIGATED | Was plaintext storage | DB row is hex, not the password |
| W2 | MITIGATED | Was no hashing | `hashlib.sha256` on register + login |
| W3 | **MITIGATED** | Was no per-user salt | Two users, same password → different digest |
| W4 | OPEN | No slow hash | SHA-256 is fast; per-row wordlist still cheap |
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
| `1-4-slow-hash` | W4 (bcrypt/argon2) |
| … | one control / name per step |

Those folders are **not created until the step is built**.
