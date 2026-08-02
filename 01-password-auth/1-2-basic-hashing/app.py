"""
01-password-auth / 1-2-basic-hashing — SHA-256 digests, no salt.

DO NOT use this pattern in production.

Control added this step: basic (fast) password hashing.
Marks W1/W2 MITIGATED; leaves the rest open (no multi-jump).
"""

from datetime import timedelta
import sqlite3
from pathlib import Path
import hashlib  # W1/W2: one-way digest; still no salt (W3) / slow KDF (W4)

from flask import Flask, redirect, request, session, url_for

# ---------------------------------------------------------------------------
# Weaknesses in this step (1-2-basic-hashing) — full inventory for track 01
# Status: OPEN | MITIGATED (only flip what this step fixed)
# ---------------------------------------------------------------------------
# W1  MITIGATED — password_hash column stores SHA-256 hex, not the password
# W2  MITIGATED — register + login use hashlib.sha256 (one-way compare)
# W3  OPEN — no per-user salt (same password → same digest; rainbow-friendly)
# W4  OPEN — SHA-256 is fast (not bcrypt/argon2); offline cracking stays cheap
# W5  OPEN — Flask secret_key hard-coded in source (forgable sessions if leaked)
# W6  OPEN — no login rate limiting / account lockout
# W7  OPEN — no password strength rules
# W8  OPEN — HTTP only (no TLS); credentials can be sniffed off-host
# W9  OPEN — debug mode enabled (extra attack surface; stack traces, etc.)
# W10 OPEN — session cookie flags weak (HttpOnly/Secure/SameSite not hardened)
# W11 OPEN — no meaningful session expiry / idle timeout
# W12 OPEN — session not regenerated on login (session fixation class)
# W13 OPEN — user enumeration via distinct error messages
# W14 OPEN — no CSRF tokens on state-changing forms (register/login)
# ---------------------------------------------------------------------------

# --- App setup ---------------------------------------------------------------
app = Flask(__name__)
# W5: secret is hard-coded and committed with the code.
app.secret_key = "dev-secret-change-me"

# W10: intentionally weak cookie flags (defaults are safer in modern Flask).
app.config["SESSION_COOKIE_HTTPONLY"] = False  # readable by document.cookie / XSS
app.config["SESSION_COOKIE_SECURE"] = False  # sent over plain HTTP
app.config["SESSION_COOKIE_SAMESITE"] = None  # no SameSite restriction

# W11: long-lived permanent sessions; no short idle timeout.
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=365)

DB_PATH = Path(__file__).with_name("users.db")


# --- Database helpers --------------------------------------------------------
def get_db():
    """Open SQLite connection; rows behave like dicts (row['username'])."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create users table if missing. password_hash holds SHA-256 hex (W1/W2)."""
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
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
        "<h1>1-2 basic hashing (W1/W2 mitigated)</h1>"
        f'<p><a href="{url_for("register_form")}">Register</a> | '
        f'<a href="{url_for("login_form")}">Log in</a></p>'
    )


# --- Register: show form + create user ---------------------------------------
@app.get("/register")
def register_form():
    """HTML form; browser POSTs username/password to /register. W14: no CSRF token."""
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
    W1/W2: store SHA-256 hex digest (not the password).
    W3/W4: still unsalted and fast.
    W7: any non-empty password is accepted.
    W14: no CSRF check on this POST.
    """
    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""
    if not username or not password:
        return "Username and password required", 400
    try:
        with get_db() as conn:
            # W1/W2: one-way digest only. W3: no salt. W4: fast SHA-256.
            password_hash = hashlib.sha256(password.encode("utf-8"))
            hex_digest = password_hash.hexdigest()
            conn.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, hex_digest),
            )
    except sqlite3.IntegrityError:
        return "Username already taken", 400
    return redirect(url_for("login_form"))


# --- Login: show form + check password + start session -----------------------
@app.get("/login")
def login_form():
    """HTML form; browser POSTs credentials to /login. W14: no CSRF token."""
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
    W1/W2: hash submitted password; compare digests (not raw password to DB).
    W6: unlimited attempts.
    W12: does not regenerate session before elevating privilege.
    W13: different errors for unknown user vs bad password.
    W14: no CSRF check on this POST.
    """
    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""
    with get_db() as conn:
        row = conn.execute(
            "SELECT username, password_hash FROM users WHERE username = ?",
            (username,),
        ).fetchone()

    # W13: distinct messages enable username enumeration.
    if row is None:
        return "Unknown username", 401
    # W1/W2: same SHA-256 hex as register. W6: no lockout / rate limit.
    hash_object = hashlib.sha256(password.encode("utf-8"))
    hex_digest = hash_object.hexdigest()
    if row["password_hash"] != hex_digest:
        return "Wrong password", 401

    # W12: reuse existing session cookie; only add identity (no rotate/clear).
    # W5: cookie signed with hard-coded secret_key.
    # W10/W11: weak flags + permanent long-lived session.
    session.permanent = True
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
    """Clear session data in the cookie. (Signed-cookie model: no server session store.)"""
    session.clear()
    return redirect(url_for("index"))


# --- Process entrypoint ------------------------------------------------------
if __name__ == "__main__":
    init_db()
    # W8: HTTP only (no TLS). W9: debug=True.
    app.run(host="127.0.0.1", port=5000, debug=True)
