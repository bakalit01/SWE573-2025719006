"""Traditional Art Gallery - a small Flask app with accounts and an artwork collection."""
import os
import re
import secrets
import sqlite3
import uuid
from functools import wraps

from flask import (Flask, abort, flash, g, redirect, render_template, request,
                   session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.environ.get("DATABASE_PATH", os.path.join(BASE_DIR, "gallery.db"))
UPLOAD_DIR = os.path.join(BASE_DIR, "static", "uploads")
ALLOWED_EXT = {"png", "jpg", "jpeg", "gif", "webp"}
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

# Set REQUIRE_LOGIN_TO_VIEW=1 to make the whole gallery members-only.
REQUIRE_LOGIN_TO_VIEW = os.environ.get("REQUIRE_LOGIN_TO_VIEW", "0") == "1"

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-me")
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB uploads

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT,
    password_hash TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS artworks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    artist TEXT,
    tradition TEXT,
    year TEXT,
    description TEXT,
    image TEXT NOT NULL,
    added_by INTEGER REFERENCES users(id),
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""

SAMPLES = [
    ("Marbled Sea", "Sample artwork", "Ebru (paper marbling)", "",
     "Swirling pigments floated on thickened water and lifted onto paper.",
     "samples/ebru.svg"),
    ("Tulip Tile", "Sample artwork", "Iznik ceramics", "",
     "Cobalt, turquoise and coral-red floral motifs on a white glaze.",
     "samples/iznik.svg"),
    ("Anatolian Diamonds", "Sample artwork", "Kilim weaving", "",
     "Flat-woven geometric pattern of stacked diamonds and borders.",
     "samples/kilim.svg"),
    ("Garden Pavilion", "Sample artwork", "Miniature painting", "",
     "A flat, jewel-toned garden scene in the miniature tradition.",
     "samples/miniature.svg"),
]


# ---------- database ----------
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    db = sqlite3.connect(DB_PATH)
    db.executescript(SCHEMA)
    if db.execute("SELECT COUNT(*) FROM artworks").fetchone()[0] == 0:
        db.executemany(
            "INSERT INTO artworks (title, artist, tradition, year, description, image)"
            " VALUES (?, ?, ?, ?, ?, ?)", SAMPLES)
    db.commit()
    db.close()


# ---------- auth helpers ----------
def current_user():
    uid = session.get("user_id")
    if uid is None:
        return None
    return get_db().execute("SELECT * FROM users WHERE id = ?", (uid,)).fetchone()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if current_user() is None:
            flash("Please log in first.")
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


def gallery_view(view):
    """Public by default; members-only if REQUIRE_LOGIN_TO_VIEW=1."""
    return login_required(view) if REQUIRE_LOGIN_TO_VIEW else view


# ---------- simple CSRF protection ----------
@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session.get("csrf_token")
        if not token or token != request.form.get("csrf_token"):
            abort(400, "Invalid form token - please reload the page and try again.")


@app.context_processor
def inject_globals():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)
    return {"user": current_user(), "csrf_token": session["csrf_token"]}


def clean_email(raw):
    """Returns (email_or_None, error_or_None). Email is optional."""
    email = (raw or "").strip().lower()
    if not email:
        return None, None
    if not EMAIL_RE.match(email):
        return None, "That email address doesn't look right."
    return email, None


# ---------- routes: gallery ----------
@app.route("/")
@gallery_view
def index():
    db = get_db()
    tradition = request.args.get("tradition", "")
    q = request.args.get("q", "").strip()
    sql, params = "SELECT * FROM artworks WHERE 1=1", []
    if tradition:
        sql += " AND tradition = ?"
        params.append(tradition)
    if q:
        sql += " AND (title LIKE ? OR artist LIKE ? OR description LIKE ?)"
        params += [f"%{q}%"] * 3
    artworks = db.execute(sql + " ORDER BY created_at DESC, id DESC", params).fetchall()
    traditions = [r[0] for r in db.execute(
        "SELECT DISTINCT tradition FROM artworks WHERE tradition != '' ORDER BY tradition")]
    return render_template("index.html", artworks=artworks, traditions=traditions,
                           tradition=tradition, q=q)


@app.route("/art/<int:art_id>")
@gallery_view
def artwork(art_id):
    art = get_db().execute(
        "SELECT a.*, u.username FROM artworks a LEFT JOIN users u ON u.id = a.added_by"
        " WHERE a.id = ?", (art_id,)).fetchone()
    if art is None:
        abort(404)
    return render_template("artwork.html", art=art)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add_artwork():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        file = request.files.get("image")
        if not title:
            flash("A title is required.")
        elif not file or not file.filename:
            flash("Please choose an image.")
        else:
            ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
            if ext not in ALLOWED_EXT:
                flash("Image must be PNG, JPG, GIF or WEBP.")
            else:
                name = f"{uuid.uuid4().hex}.{ext}"
                file.save(os.path.join(UPLOAD_DIR, secure_filename(name)))
                db = get_db()
                cur = db.execute(
                    "INSERT INTO artworks (title, artist, tradition, year, description, image, added_by)"
                    " VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (title, request.form.get("artist", "").strip(),
                     request.form.get("tradition", "").strip(),
                     request.form.get("year", "").strip(),
                     request.form.get("description", "").strip(),
                     f"uploads/{name}", session["user_id"]))
                db.commit()
                flash("Artwork added.")
                return redirect(url_for("artwork", art_id=cur.lastrowid))
    return render_template("add.html")


@app.route("/art/<int:art_id>/delete", methods=["POST"])
@login_required
def delete_artwork(art_id):
    db = get_db()
    art = db.execute("SELECT * FROM artworks WHERE id = ?", (art_id,)).fetchone()
    if art is None:
        abort(404)
    if art["added_by"] != session["user_id"]:
        abort(403)
    if art["image"].startswith("uploads/"):
        try:
            os.remove(os.path.join(BASE_DIR, "static", art["image"]))
        except FileNotFoundError:
            pass
    db.execute("DELETE FROM artworks WHERE id = ?", (art_id,))
    db.commit()
    flash("Artwork removed.")
    return redirect(url_for("index"))


# ---------- routes: accounts ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        email, email_err = clean_email(request.form.get("email"))
        if len(username) < 3:
            flash("Username must be at least 3 characters.")
        elif len(password) < 8:
            flash("Password must be at least 8 characters.")
        elif email_err:
            flash(email_err)
        else:
            db = get_db()
            try:
                cur = db.execute(
                    "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                    (username, email, generate_password_hash(password)))
                db.commit()
            except sqlite3.IntegrityError:
                flash("That username is taken.")
            else:
                session.clear()
                session["user_id"] = cur.lastrowid
                flash("Welcome! Your account is ready.")
                return redirect(url_for("index"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        u = get_db().execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if u is None or not check_password_hash(u["password_hash"], password):
            flash("Wrong username or password.")
        else:
            session.clear()
            session["user_id"] = u["id"]
            nxt = request.args.get("next", "")
            return redirect(nxt if nxt.startswith("/") and not nxt.startswith("//")
                            else url_for("index"))
    return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("You've been logged out.")
    return redirect(url_for("index"))


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        email, err = clean_email(request.form.get("email"))
        if err:
            flash(err)
        else:
            db = get_db()
            db.execute("UPDATE users SET email = ? WHERE id = ?", (email, session["user_id"]))
            db.commit()
            flash("Email saved." if email else "Email removed.")
        return redirect(url_for("profile"))
    count = get_db().execute("SELECT COUNT(*) FROM artworks WHERE added_by = ?",
                             (session["user_id"],)).fetchone()[0]
    return render_template("profile.html", art_count=count)


init_db()

if __name__ == "__main__":
    app.run(debug=True)
