# 1-6 — debug off

> ⚠️ **Educational only.** Intentionally weak. Do not deploy. Use at your own risk. See the [repo disclaimer](../../README.md#-disclaimer).

**Control added:** `app.run(debug=False)`. An unhandled exception is a generic 500 in the browser. The traceback still prints in the server terminal. There is no debugger PIN and no interactive console.

| ID | Status |
|----|--------|
| W1 | MITIGATED — from 1-2; digest, not the password |
| W2 | MITIGATED — from 1-2; one-way hash |
| W3 | MITIGATED — from 1-3; per-hash salt (inside the bcrypt string) |
| W4 | MITIGATED — from 1-4; bcrypt cost 12 |
| W5–W8 | OPEN |
| **W9** | **MITIGATED** — `debug=False` |
| W10–W14 | OPEN |
| W15 | MITIGATED — from 1-5; pepper MAC then bcrypt |

Same app shape as [1-5-pepper](../1-5-pepper/): register + login + session + pepper. Only the debug flag changed.

**Track:** [01-password-auth](../) · **Notes:** [Learnings.md](./Learnings.md)

## Run

```bash
cd 01-password-auth/1-6-debug-off
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

The banner says `Debug mode: off`. There is no `Restarting with stat` line and no debugger PIN.

`app.env` still has to sit next to `app.py` (mode `600`). `.gitignore` pattern `*.env` skips it. A `users.db` copied from 1-4 will not log in.

## What exists

| Piece | Role |
|--------|------|
| `POST /register` | `hashpw(get_mac(password, pepper), gensalt())`, store the ASCII bcrypt string |
| `POST /login` | same `get_mac`, then `checkpw` |
| `GET /me` | "secret" page if logged in |
| `users.db` | SQLite user store (`username`, `password_hash`) |
| `app.env` | Pepper file. Not a column in `users` |
| `app.run(..., debug=False)` | No Werkzeug debugger |

## What changed vs 1-5

| Before (1-5) | After (1-6) |
|--------------|-------------|
| `debug=True` | `debug=False` |
| Unhandled exception opens the interactive debugger in the browser | Browser shows a generic Internal Server Error page |
| Terminal prints a debugger PIN and starts the reloader | Terminal still prints the traceback. No PIN, no reloader |

Password storage is unchanged. Pepper, salt, and bcrypt cost are the same as 1-5.

## Try / notice

Put this on the first line of `index()`, save, and open `/`:

```python
raise RuntimeError("w9 debug check")
```

The browser says the server encountered an internal error. It does not show `app.py`, local variables, or a console. The terminal still prints `RuntimeError: w9 debug check`.

Delete the `raise` and restore `index()` when you are done. Leaving it in makes every visit to `/` a 500.

On 1-5, the same `raise` with `debug=True` served the Werkzeug debugger (`debugger.js`, source frames, a PIN-gated console). Use this lab's process only.

## Weaknesses (W1–W15)

Same IDs as the top of `app.py`:

| ID | Status | Issue | Try / notice |
|----|--------|--------|----------------|
| W1 | MITIGATED | Was plaintext storage | DB row is `$2b$12$…`, not the password |
| W2 | MITIGATED | Was no hashing | `hashpw` on register, `checkpw` on login |
| W3 | MITIGATED | Was no per-user salt | Same password → different bcrypt string |
| W4 | MITIGATED | Was fast SHA-256 | bcrypt cost 12 still wraps the MAC |
| W5 | OPEN | Hard-coded `secret_key` | Still a literal in `app.py` |
| W6 | OPEN | No rate limit / lockout | Spam login guesses |
| W7 | OPEN | No password strength rules | Register with `a` |
| W8 | OPEN | HTTP only (no TLS) | `app.run(...)` has no TLS |
| W9 | **MITIGATED** | Was `debug=True` | Generic 500 in the browser. Traceback stays on the server terminal |
| W10 | OPEN | Weak session cookie flags | `SESSION_COOKIE_*` set weak in code |
| W11 | OPEN | Long-lived permanent session | 365 days; `session.permanent = True` |
| W12 | OPEN | No session regenerate on login | Login only sets `session["username"]` |
| W13 | OPEN | User enumeration | `"Unknown username"` vs `"Wrong password"` |
| W14 | OPEN | No CSRF tokens | Register/login forms are bare POSTs |
| W15 | MITIGATED | Was no pepper | HMAC key is in `app.env`, outside `users` |

## Naming for later steps

| Planned folder | Implies closed (mainly) |
|----------------|-------------------------|
| `…-cookie-flags` | W10 (HttpOnly, SameSite) |
| … | one control / name per step |

Those folders are **not created until the step is built**. `Secure` waits until TLS exists (W8). W5–W8 and W10–W14 are still open.
