# Cyber Labs

Small hands-on labs for learning security by building. A "ladder" of increasingly more secure iterations of the same base use case.

Each **track** (`01-…`, `02-…`) is one problem family. Steps inside a track (`1-1`, `1-2`, …) share the same base app; the folder name is the control that step adds. **1-1-base** = all weaknesses open.

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
| [01-password-auth](./01-password-auth/) | Password auth ladder | 1-1-base ready |

## Layout

```
cyber_labs/
  README.md
  01-password-auth/
    README.md
    1-1-base/              # all weaknesses open
    1-2-basic-hashing/     # created when built
    …
```
