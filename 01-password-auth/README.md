# 01 — Password authentication

Same small web app, stepped up one control at a time.

> ⚠️ **Educational only.** Intentionally weak at early rungs. Do not deploy. See the [repo disclaimer](../README.md#-disclaimer).

## Ladder

| Step | Folder | Meaning | Status |
|------|--------|---------|--------|
| 1-1 | [1-1-base](./1-1-base/) | Baseline — **all W1–W15 OPEN** | ready |
| 1-2 | [1-2-basic-hashing](./1-2-basic-hashing/) | SHA-256 digests — **W1, W2 MITIGATED** | ready |
| 1-3 | [1-3-salted-hashing](./1-3-salted-hashing/) | Per-user salt — **W3 MITIGATED** | ready |
| 1-4 | [1-4-slow-hash](./1-4-slow-hash/) | bcrypt (mainly W4) | ready |

Only create the next folder when that step is implemented. Empty placeholders are not kept.

Each step keeps the same base (register / login / session). The folder name says what was hardened; the W* list in `app.py` says what is OPEN vs MITIGATED.

## Rule: one rung at a time

Do **not** jump multiple hardening controls in one step.

Each gap is the **next smallest meaningful upgrade** only — enough to change the attack story, nothing extra.

- Good: base → basic hashing → salting → slow hash  
- Bad: base → OAuth2 + MFA + rate limits + TLS in one go  

If it isn’t in the step name, it doesn’t get added yet.

## Code comment convention

Each step’s `app.py` keeps the full **W1–W15** weakness list at the top (`OPEN` or `MITIGATED`).

- Base inventory lives in **1-1-base** and is **append-only** (new IDs at the end; never renumber).
- Only mark **MITIGATED** what this step actually fixed.
- Leave other items `OPEN`.
- Inline comments at the relevant lines reference the same IDs (e.g. `# W1:`).

### Base inventory (W1–W15)

| ID | Concern |
|----|---------|
| W1 | Plaintext password storage |
| W2 | No password hashing |
| W3 | No per-user salt |
| W4 | No slow hash (bcrypt/argon2) |
| W5 | Hard-coded `secret_key` |
| W6 | No rate limit / lockout |
| W7 | No password strength rules |
| W8 | No TLS (HTTP only) |
| W9 | Debug mode on |
| W10 | Weak session cookie flags |
| W11 | No meaningful session expiry |
| W12 | Session not regenerated on login |
| W13 | User enumeration via errors |
| W14 | No CSRF protection on forms |
| W15 | No password pepper (app secret mixed into the hash, kept outside the user table; not Flask `secret_key`) |
