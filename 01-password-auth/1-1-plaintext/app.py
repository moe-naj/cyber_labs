"""
01-password-auth / 1-1-plaintext — intentionally naive.

DO NOT use this pattern in production.

Weakness list (open in 1-1). Later steps mark items MITIGATED and leave the rest open.
Only the control for that step should change.
"""

import sqlite3
from pathlib import Path

from flask import Flask, redirect, request, session, url_for

# ---------------------------------------------------------------------------
# Weaknesses in this step (1-1)
# Status: OPEN | MITIGATED (in a later step — update comment there)
# ---------------------------------------------------------------------------
# W1 OPEN — passwords stored in plaintext (readable via sqlite3 / strings)
# W2 OPEN — no password hashing at all
# W3 OPEN — no per-user salt
# W4 OPEN — no slow hash (bcrypt/argon2)
# W5 OPEN — Flask secret_key hard-coded in source (forgable sessions if leaked)
# W6 OPEN — no login rate limiting / account lockout
# W7 OPEN — no password strength rules
# W8 OPEN — HTTP only (no TLS); credentials can be sniffed off-host
# W9 OPEN — debug mode enabled (extra attack surface; stack traces, etc.)
# ---------------------------------------------------------------------------

# --- App setup ---------------------------------------------------------------
app = Flask(__name__)
# W5: secret is hard-coded and committed with the code.
app.secret_key = "dev-secret-change-me"

DB_PATH = Path(__file__).with_name("users.db")


# --- Database helpers --------------------------------------------------------
def get_db():
    """Open SQLite connection; rows behave like dicts (row['username'])."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create users table if missing. password column holds the raw secret (W1)."""
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
            """
        )


# --- Pages: home -------------------------------------------------------------
@app.get("/")
def index():
    """Landing page: links change if a session cookie already says you're logged in."""
    user = session.get("username")
    if user:
        return (
            f"<h1>Logged in as {user}</h1>"
            f'<p><a href="{url_for("me")}">/me</a></p>'
            f'<p><a href="{url_for("logout")}">Log out</a></p>'
        )
    return (
        "<h1>1-1 plaintext password auth</h1>"
        f'<p><a href="{url_for("register_form")}">Register</a> | '
        f'<a href="{url_for("login_form")}">Log in</a></p>'
    )


# --- Register: show form + create user ---------------------------------------
@app.get("/register")
def register_form():
    """HTML form; browser POSTs username/password to /register."""
    return """
    <h1>Register</h1>
    <form method="post">
      <label>Username <input name="username" required></label><br>
      <label>Password <input name="password" type="password" required></label><br>
      <button type="submit">Create account</button>
    </form>
    <p><a href="/">Home</a></p>
    """


@app.post("/register")
def register():
    """
    Create account.
    W1/W2/W3/W4: store password as submitted (plaintext).
    W7: any non-empty password is accepted.
    """
    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""
    if not username or not password:
        return "Username and password required", 400
    try:
        with get_db() as conn:
            # W1: password column = literal password string.
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password),
            )
    except sqlite3.IntegrityError:
        return "Username already taken", 400
    return redirect(url_for("login_form"))


# --- Login: show form + check password + start session -----------------------
@app.get("/login")
def login_form():
    """HTML form; browser POSTs credentials to /login."""
    return """
    <h1>Log in</h1>
    <form method="post">
      <label>Username <input name="username" required></label><br>
      <label>Password <input name="password" type="password" required></label><br>
      <button type="submit">Log in</button>
    </form>
    <p><a href="/">Home</a></p>
    """


@app.post("/login")
def login():
    """
    Verify credentials, then set session cookie.
    W1/W2: compare submitted password to plaintext DB value.
    W6: unlimited attempts.
    """
    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""
    with get_db() as conn:
        row = conn.execute(
            "SELECT username, password FROM users WHERE username = ?",
            (username,),
        ).fetchone()
    # W1 + W6: plain string compare; no lockout / rate limit.
    if row is None or row["password"] != password:
        return "Invalid username or password", 401
    # Session cookie signed with app.secret_key (W5).
    session["username"] = row["username"]
    return redirect(url_for("me"))


# --- Authenticated page + logout ---------------------------------------------
@app.get("/me")
def me():
    """Protected page: requires session['username'] from a prior successful login."""
    user = session.get("username")
    if not user:
        return redirect(url_for("login_form"))
    return f"<h1>Secret area</h1><p>Hello, {user}.</p><p><a href='/'>Home</a></p>"


@app.get("/logout")
def logout():
    """Clear session cookie data on the server side of the session object."""
    session.clear()
    return redirect(url_for("index"))


# --- Process entrypoint ------------------------------------------------------
if __name__ == "__main__":
    init_db()
    # W8: HTTP only (no TLS). W9: debug=True.
    app.run(host="127.0.0.1", port=5000, debug=True)
