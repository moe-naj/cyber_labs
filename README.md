# cyber_labs

Small hands-on labs for learning security by building.

Each **track** (`01-…`, `02-…`) is one problem family. Steps inside a track (`1-1`, `1-2`, …) are the same base app with one security upgrade at a time.

## ⚠️ Disclaimer

**Educational use only.**

These labs are intentionally simplified and often **intentionally weak** so you can see how authentication and related controls fail. They are training aids, not production templates.

- Do **not** deploy this code to real users, public servers, or production systems.
- Do **not** use these patterns as a guide for building real security controls without further hardening.
- You are responsible for how you use this material. Use at your own risk.
- The author assumes no liability for misuse, damage, or security incidents arising from this repository.

If a lab stores secrets in plaintext, skips TLS, omits rate limits, or hard-codes keys — that is usually **on purpose**. Read each lab’s README before running it.

## Tracks

| Track | Topic | Status |
|-------|--------|--------|
| [01-password-auth](./01-password-auth/) | Password auth ladder (plaintext → hash → salt → bcrypt) | 1-1 ready |

## Layout

```
cyber_labs/
  README.md
  01-password-auth/
    README.md
    1-1-plaintext/
    1-2-unsalted-hash/
    1-3-salted-hash/
    1-4-bcrypt/
  02-…/
```
