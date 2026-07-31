# 01 — Password authentication

Same small web app, stepped up one control at a time.

> ⚠️ **Educational only.** Intentionally weak at early rungs. Do not deploy. See the [repo disclaimer](../README.md#-disclaimer).

## Ladder

| Step | Folder | What changes | Status |
|------|--------|--------------|--------|
| 1-1 | [1-1-plaintext](./1-1-plaintext/) | Passwords stored in plaintext | ready |
| 1-2 | [1-2-unsalted-hash](./1-2-unsalted-hash/) | Fast hash, no salt (e.g. MD5/SHA-256) | empty |
| 1-3 | [1-3-salted-hash](./1-3-salted-hash/) | Hash + per-user salt | empty |
| 1-4 | [1-4-bcrypt](./1-4-bcrypt/) | Slow hash (bcrypt/argon2) | empty |

Each step keeps the same base (register / login / session). Only password storage (and related checks) should change unless a later step says otherwise.

## Rule: one rung at a time

Do **not** jump multiple hardening controls in one step.

Each gap is the **next smallest meaningful upgrade** only — enough to change the attack story, nothing extra.

- Good: plaintext → unsalted hash → salted hash → bcrypt  
- Bad: plaintext → OAuth2 + MFA + rate limits + TLS in one go  

If it isn’t in the step title, it doesn’t get added yet.
