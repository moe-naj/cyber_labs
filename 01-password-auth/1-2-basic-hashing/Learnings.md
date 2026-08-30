# Learnings — 1-2 basic hashing

Session notes from implementing and reasoning about this step. Not a substitute for `app.py` W* comments or the README.

## Password storage (W1 / W2)

- Basic hashing closes **both** W1 (plaintext in DB) and W2 (no hash): you still use the DB, but store a digest.
- Base64 / encoding is **not** a mitigation — trivially reversible; W1 stays open.
- Encrypting passwords is reversible secrecy, not the auth ladder’s next step (and is a poor password-store pattern).
- Register and login must use the **same** transform: hash on write; hash submitted secret and compare digests on login.
- SHA-256 is **one-way**: you cannot decrypt a digest back to the password.
- Sites that “decrypt” SHA-256 are doing **lookup / wordlist / preimage search**, not reversing the hash.
- Residual risk after this step was already on the inventory: **W3** (no salt), **W4** (fast hash), **W7** (weak policy). **W15** (pepper) was appended to the track inventory later; it is still OPEN and not this rung.

## Hash representation

- `hashlib.sha256(...)` produces a hash object; the digest can be exposed as:
  - **bytes** — `.digest()` (32 bytes for SHA-256)
  - **hex text** — `.hexdigest()` (64 `0-9a-f` chars)
- The hex string **is** the SHA-256 result in text form, not a wrapper around some other “real” form.
- Choose one encoding for storage and use it on both register and login (this step: hex in `TEXT` column `password_hash`).
- Hash APIs want **bytes** in: `password.encode("utf-8")`.

## Schema / SQLite

- `TEXT` is fine for hex digests; no need for a different SQL type for this rung.
- Renaming `password` → `password_hash` means SELECT / INSERT / `row[...]` keys must all match.
- `CREATE TABLE IF NOT EXISTS` does **not** migrate old tables — delete stale `users.db` when the schema changes.

## Python / tooling

- `import hashlib` is a **stdlib module** (no new pip package for basic SHA-256).
- Prefer **module** / **package** over vague “library”; pip installs distributions.
- Mixed tabs/spaces → `TabError`; this tree indents with spaces.
- `python3 -m py_compile app.py` catches syntax/indent before runtime.
- `sed -n '…p' file | cat -A` shows tabs as `^I`.

## Demos that stick

```bash
sqlite3 users.db "SELECT username, password_hash FROM users;"
# hex digest, not the password

# Same password → same hash (W3 teaser)
# Common passwords → easy lookup (W4 + weak secret)
```

## Ladder takeaway

One control this folder: **basic (fast) hashing**. Next smallest upgrades live in later folders (salt, then slow hash) — don’t multi-jump.

## Next rung

[1-3-salted-hashing](../1-3-salted-hashing/) — per-user salt (W3).
