"""
01-password-auth / 1-1-plaintext — intentionally naive.

DO NOT use this pattern in production.
Passwords are stored in plaintext so you can see them in the DB.
"""

import sqlite3
from pathlib import Path

from flask import Flask, redirect, request, session, url_for

app = Flask(__name__)
# Weakness: secret is hard-coded and committed with the code.
app.secret_key = "dev-secret-change-me"

DB_PATH = Path(__file__).with_name("users.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
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


@app.get("/")
def index():
    user = session.get("username")
    if user:
        return (
            f"<h1>Logged in as {user}</h1>"
            f'<p><a href="{url_for("me")}">/me</a></p>'
            f'<p><a href="{url_for("logout")}">Log out</a></p>'
        )
    return (
        "<h1>Basic password auth (naive)</h1>"
        f'<p><a href="{url_for("register_form")}">Register</a> | '
        f'<a href="{url_for("login_form")}">Log in</a></p>'
    )


@app.get("/register")
def register_form():
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
    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""
    if not username or not password:
        return "Username and password required", 400
    try:
        with get_db() as conn:
            # Weakness: password saved as plaintext.
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password),
            )
    except sqlite3.IntegrityError:
        return "Username already taken", 400
    return redirect(url_for("login_form"))


@app.get("/login")
def login_form():
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
    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""
    with get_db() as conn:
        row = conn.execute(
            "SELECT username, password FROM users WHERE username = ?",
            (username,),
        ).fetchone()
    # Weakness: no rate limiting; direct string compare on plaintext.
    if row is None or row["password"] != password:
        return "Invalid username or password", 401
    session["username"] = row["username"]
    return redirect(url_for("me"))


@app.get("/me")
def me():
    user = session.get("username")
    if not user:
        return redirect(url_for("login_form"))
    return f"<h1>Secret area</h1><p>Hello, {user}.</p><p><a href='/'>Home</a></p>"


@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    # Weakness: HTTP only (no TLS).
    app.run(host="127.0.0.1", port=5000, debug=True)
