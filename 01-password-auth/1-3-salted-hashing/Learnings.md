# Learnings — 1-3 salted hashing

Session notes from this step. Not a substitute for `app.py` W* comments or the README.

## What W3 actually mitigates

- Threat model: **stolen user table** (hash **and** salt in the same row).
- Stops **shared digests** (same password → same hash → one crack, many accounts).
- Stops **precomputed / rainbow tables** of unsalted `sha256("password")`.
- Does **not** assume the attacker has hash-only and no salt. Salt is stored on purpose; it is not a secret.
- A secret extra value *not* in the DB would be a **pepper** (**W15**, not this rung; not Flask `secret_key` / W5).

## Hash construction this step

- Register: `os.urandom(16)` → mix **into** the hash: `sha256(salt_bytes || password_bytes)` → store `salt.hex()` and hex digest.
- Login: `bytes.fromhex(row["salt"])`, same concat order, compare hex.
- Concat order is a convention; both sides must match. Salt after the digest (glue onto `hexdigest()`) is **not** a salt.

## Residual (already on the inventory)

- **W4**: still fast SHA-256. Stolen row → wordlist still works: for each guess, `sha256(that_salt || word)` vs `password_hash`.
- Delay vs 1-2 is mostly **per user** (N salts), not per guess.

## Schema / SQLite

- `salt TEXT NOT NULL`. Uniqueness comes from `urandom`, not a SQL `UNIQUE` on salt.
- `CREATE TABLE IF NOT EXISTS` does not migrate 1-2 DBs — delete stale `users.db`.

## Demos that stick

```bash
sqlite3 users.db "SELECT username, salt, password_hash FROM users;"
# same password, two users → two salts, two hashes
```

## Ladder takeaway

One control this folder: **per-user salt**. Next smallest upgrade is a slow hash (W4).

## Next rung

[1-4-slow-hash](../1-4-slow-hash/) — slow hash (W4, bcrypt).
