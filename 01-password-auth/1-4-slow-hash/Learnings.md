# Learnings — 1-4 slow hash

Session notes from this step. Not a substitute for `app.py` W* comments or the README.

## What W4 actually mitigates

- Threat model: **stolen user table**. Each password guess must run bcrypt (cost 12 → 4096 iterations), not a fast SHA-256.
- Login is still one check; it feels fine. Offline wordlist against the dump does not.
- Does **not** make a weak password unguessable — it makes guessing **expensive**. `alice123` on 1-2 was instant; the same class of secret on bcrypt is a long wait, not magic immunity.
- **W15** (pepper) is still OPEN: a stolen bcrypt row is enough to start guessing. A pepper would be an app secret **outside** the DB. Not Flask `secret_key` (W5).

## Salt is still there (no column)

- bcrypt’s stored string is version + cost + salt + digest (`$2b$12$…`).
- `gensalt()` on register; `checkpw` **parses** salt/cost out of the stored value. Do **not** `gensalt()` again on login (new salt → never matches).
- Dropping the 1-3 `salt` column is not “no salt”; it is not storing salt twice.

## Types / schema

- `hashpw` / `checkpw` want **bytes**. Form password is `str` → `encode("utf-8")`.
- Store the bcrypt value as **ASCII text** in `TEXT` (`decode("ascii")` on write, `encode("ascii")` on verify).
- `CREATE TABLE IF NOT EXISTS` does not migrate a 1-3 DB that still has `salt` — delete stale `users.db`.
- `bcrypt` is a **pip package** (`bcrypt==5.0.0` in this step’s `requirements.txt`), not stdlib.

## Demos that stick

```bash
sqlite3 users.db "SELECT username, password_hash FROM users;"
# $2b$12$… ; same password → two strings

# Own lab files only
john --format=bcrypt hash --wordlist=/usr/share/wordlists/rockyou.txt
john --format=Raw-SHA256 hash --wordlist=/usr/share/wordlists/rockyou.txt
```

On this box: bcrypt ~85 guesses/s (days of ETA on rockyou); Raw-SHA256 ~13 million/s and a common password in 0s. John reports bcrypt “Cost 1 (iteration count) is 4096” for `$2b$12$`.

Two bcrypt rows with the same password are still **two** independent attacks (two salts). Unsalted 1-2 SHA-256: one hit covers every matching account.

## Ladder takeaway

One control this folder: **slow hash (bcrypt)**. Next password-store extra is pepper (W15), not more KDF work in this folder.

## Next rung

Not built. W15 (`…-pepper`) is the leftover password-store control; W5–W14 stay on the inventory too. Same rule: copy this step, one control, then comments/docs.
