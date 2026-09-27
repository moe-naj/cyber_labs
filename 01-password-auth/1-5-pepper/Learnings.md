# Learnings — 1-5 pepper

Session notes from this step. Not a substitute for `app.py` W* comments or the README.

## What W15 actually mitigates

- Threat model: **stolen `users.db`**. On 1-4 the bcrypt row is enough to start guessing. Here the value bcrypt stores is `bcrypt(HMAC-SHA256(pepper, password))`.
- A password wordlist does not match that row unless the guess is mixed with the same pepper first.
- Login is still one HMAC plus one bcrypt. It feels the same as 1-4.
- A copy of the whole `1-5-pepper/` directory still includes `app.env`. The lab file is a stand-in. The production place for this secret is an HSM or something with that job.
- **W5** stays OPEN. `app.secret_key` still only signs the session cookie. The pepper is a separate secret.

## Pepper is not the salt

- Same password and same pepper produce the **same** 32-byte MAC for every account.
- `gensalt()` still runs on each register, so two accounts with the same password still store two `$2b$12$…` strings. `moe` and `baba` were that case, and both logged in.
- `checkpw` reads salt and cost from the stored string. Checking the raw password bytes against that string fails.

## Why HMAC

- There is no pepper module. `hashpw` and `checkpw` take the same two arguments as in 1-4.
- bcrypt 5 raises `ValueError` on input longer than 72 bytes. Gluing the pepper onto the password spends that budget.
- `hmac.new(pepper_bytes, password.encode(), hashlib.sha256).digest()` is always 32 bytes, and every password byte affects it.
- HMAC is fast. bcrypt stays the slow step.
- No new dependency. `hmac`, `hashlib`, `base64`, and `configparser` are stdlib. bcrypt is still the 1-4 package (`bcrypt==5.0.0`).

## Where the 32 bytes live

- `openssl rand -base64 32` writes one 44-character base64 line. That line is the file encoding. The HMAC key is the decoded 32 bytes.
- `app.env` sits next to `app.py`, mode `600`:

```ini
[config]
pepper = <one base64 line, no quotes>
```

- `configparser` keeps quote characters as part of the value. A quoted line does not decode to 32 bytes.
- `cfg.read("app.env")` follows the process working directory. `Path(__file__).with_name("app.env")` follows the file, including when the server is started from another directory.
- `.gitignore` pattern `*.env` matches `app.env`, so `git add -A` skips it. `*.db` still skips `users.db`.
- A `users.db` copied from 1-4 will not log in. This folder started empty; the first run created the table.

## Types that bit us

- `cfg["config"]["pepper"]` is `str`. The HMAC key has to be `bytes` from `base64.b64decode`. A `str` key raises `TypeError`.
- The message is `password.encode()` (UTF-8). `str.encoded()` does not exist.
- Return `.digest()`. `base64.b64encoded` does not exist, and encoding the digest would make bcrypt hash a different value than the MAC.
- Register and login both call `get_mac(password, pepper_decoded)`.

## Demos that stick

```bash
sqlite3 users.db "SELECT username, password_hash FROM users;"
# same password, two $2b$12$ strings, both accounts log in
```

John with `--format=bcrypt` on a stolen row, and without `app.env`, is guessing that 32-byte MAC. A password wordlist does not hit.

## Ladder takeaway

One control this folder: **pepper** before the bcrypt already added in 1-4. Salt and cost are unchanged.

## Next rung

Not built. Password-store items in this track (W1–W4 and W15) are mitigated here. W5–W14 stay open. The track has not named the next folder.
