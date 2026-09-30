# Learnings — 1-6 debug off

Session notes from this step. Not a substitute for `app.py` W* comments or the README.

## What W9 actually mitigates

- Threat model: **a client who can trigger an error**. On 1-5, `debug=True` turns that error into the Werkzeug debugger in the browser.
- With `debug=False`, the browser gets a generic Internal Server Error page. No source, no locals, no PIN, no console.
- The traceback still prints in the terminal that is running `python app.py`. This rung hides the detail from the client. It does not stop the operator log.
- **W5** stays OPEN. `app.secret_key` is still a literal in `app.py`. Debug mode was what would have shown that source to the browser.

## What `debug=True` was already leaking before any crash

- Banner: `Debug mode: on`.
- `Restarting with stat` is the reloader. Saving `app.py` restarts the process.
- `Debugger is active!` and a PIN on stdout. Anyone who can read that log and reach the app has the key to the interactive debugger.

A normal `/` response does not show any of that. The extra page appears on an unhandled exception.

## What the debugger page showed

- One temporary line at the top of `index()`: `raise RuntimeError("w9 debug check")`.
- The browser loaded `debugger.js` and `console.png`. The page is the interactive debugger, not a plain traceback.
- The frame that mattered was `app.py` / `index`. It showed the `raise` and the home-page source under it.
- Frames above it are Flask itself, from `myenv`. Those show library source and the absolute path of this lab, including the virtualenv and the Python version.
- This crash ran before `session.get`, so the frame had no username or password in it. A crash later in login can include the form values for that frame.
- The page says you can execute arbitrary Python in the stack frames, and it names `dump()` as a helper. That console runs inside the app process, so it can see `pepper_decoded`, `app.env`, and `users.db`. We did not open it.

## What `debug=False` showed

- Banner: `Debug mode: off`. No reloader line. No PIN.
- The same `raise` produced: "The server encountered an internal error and was unable to complete your request."
- The terminal still printed `RuntimeError: w9 debug check` and the traceback.
- The `raise` has to come back out, and `index()` has to be the original function again. A duplicated `session.get` and a docstring stranded under the `raise` will not run, because the raise returns first.

## Ladder takeaway

One control this folder: **`debug=False`**. Pepper, salt, and bcrypt are unchanged from 1-5.

## Next rung

Not built. Next in the complexity order we used is **W10**, cookie flags (`HttpOnly`, `SameSite`). Leave `Secure` until TLS exists, or the session cookie will not stick on `http://127.0.0.1`. W5–W8 and W11–W14 stay open too.
