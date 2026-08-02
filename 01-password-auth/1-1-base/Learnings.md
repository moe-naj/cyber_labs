# Learnings — 1-1 base

Session notes from reading the baseline app (boilerplate, sessions, cookies). Not a substitute for `app.py` W* comments or the README.

## Flask shape

- Typical small-app pieces: `Flask(__name__)`, `secret_key` / `app.config`, route decorators, `request.form`, `session`, `redirect` + `url_for`, `app.run(...)`.
- `url_for("view_function_name")` builds paths so renames break fewer links.
- `return body, status` sets HTTP status (e.g. 400, 401).
- Default Flask session = **signed cookie** (client-held; integrity via `secret_key`), not a server session store.
- `if __name__ == "__main__":` runs the dev server only when executing the file directly.

## Cookies / HttpOnly

- `HttpOnly=true` → JS cannot read the cookie (`document.cookie` skips it).
- `HttpOnly=false` is only intentional when **client JS must read that value**.
- **Session / auth cookies** should stay HttpOnly; readable session ≈ XSS → account theft.
- Other cookies sometimes non-HttpOnly: CSRF double-submit token, UI prefs, analytics — not login identity.

## CSRF vs session

- **Session cookie** proves “who you are.”
- **CSRF token** proves “this state-changing request was intentional from our front end,” not a blind cross-site POST.
- Stealing only a CSRF token does **not** let an attacker replay a session on their own machine; they still need the victim’s session context (or XSS on your origin).
- “Decrypter” / cracker language for hashes is separate (see 1-2 learnings).

## Lab process

- Run: venv → `pip install -r requirements.txt` → `python app.py` → http://127.0.0.1:5000
- Repo git root is `cyber_labs/`; `.venv/` is already gitignored.
- Weakness IDs W1–W14 are fixed in base so later steps don’t renumber; only flip what a step actually fixed.

## Next rung

[1-2-basic-hashing](../1-2-basic-hashing/) — store/verify SHA-256 digests (W1, W2).
