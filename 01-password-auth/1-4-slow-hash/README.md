# 1-4 — slow hash

> ⚠️ **Educational only.** Intentionally weak. Do not deploy. Use at your own risk. See the [repo disclaimer](../../README.md#-disclaimer).

**Control added:** **bcrypt** on register and login (slow KDF; salt + cost live in the stored string).

| ID | Status |
|----|--------|
| W1 | MITIGATED — from 1-2; digest, not the password |
| W2 | MITIGATED — from 1-2; one-way hash |
| W3 | MITIGATED — from 1-3; per-hash salt (now inside the bcrypt string, not a column) |
| **W4** | **MITIGATED** — `bcrypt.hashpw` / `checkpw` (default cost 12) |
| W5–W15 | OPEN — including no pepper (W15) |

Same app shape as [1-3-salted-hashing](../1-3-salted-hashing/): register + login + session. Only the hash construction and schema (dropped `salt` column) changed.

**Track:** [01-password-auth](../) · **Notes:** [Learnings.md](./Learnings.md)

## Run

```bash
cd 01-password-auth/1-4-slow-hash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

If you still have an old `users.db` with a `salt` column (1-3 schema), delete it so `init_db` can create the new table. `CREATE TABLE IF NOT EXISTS` does not migrate.

## What exists

| Piece | Role |
|--------|------|
| `POST /register` | `hashpw(password, gensalt())`, store ASCII bcrypt string in `password_hash` |
| `POST /login` | `checkpw` against that string (library reads cost + salt out of it) |
| `GET /me` | "secret" page if logged in |
| `users.db` | SQLite user store (`username`, `password_hash`) |

## What changed vs 1-3

| Before (1-3) | After (1-4) |
|--------------|-------------|
| `sha256(salt \|\| password)` | `bcrypt.hashpw` / `checkpw` |
| `password_hash` + `salt` columns | `password_hash` only (`$2b$12$…`) |
| Fast per-guess SHA-256 | Slow per-guess bcrypt (cost 12 → 4096 Blowfish iterations) |

Salt is still not a secret. It is just no longer a second column: bcrypt’s stored value is version + cost + salt + digest.

## Try / notice

```bash
# After two registers with the same password — hashes differ; no salt column
sqlite3 users.db "SELECT username, password_hash FROM users;"

# Own lab hashes only — W4 wall clock vs 1-2:
# john --format=bcrypt hash --wordlist=/usr/share/wordlists/rockyou.txt
# john --format=Raw-SHA256 hash --wordlist=/usr/share/wordlists/rockyou.txt
```

Expect bcrypt in tens–hundreds of guesses/s on CPU; raw SHA-256 in millions–billions. Login still feels instant (one hash). Stolen file × wordlist does not.

## Weaknesses (W1–W15)

Same IDs as the top of `app.py`:

| ID | Status | Issue | Try / notice |
|----|--------|--------|----------------|
| W1 | MITIGATED | Was plaintext storage | DB row is `$2b$12$…`, not the password |
| W2 | MITIGATED | Was no hashing | `hashpw` on register, `checkpw` on login |
| W3 | MITIGATED | Was no per-user salt | Same password → different bcrypt string |
| W4 | **MITIGATED** | Was fast SHA-256 | Wordlist against bcrypt is slow; see john/hashcat on **this** DB only |
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
| W15 | OPEN | No password pepper | Stolen bcrypt row is still enough (no app secret outside the DB; not W5) |

## Naming for later steps

| Planned folder | Implies closed (mainly) |
|----------------|-------------------------|
| `…-pepper` | W15 |
| … | one control / name per step |

Those folders are **not created until the step is built**.
