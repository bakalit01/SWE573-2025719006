# Traditional Art Gallery

A small Python (Flask) website that shows a collection of traditional artwork — Ebru, Iznik ceramics, kilims, miniatures and more.

**Features**
- Sign up / log in / log out (passwords are hashed, forms are CSRF-protected)
- Email is **optional** — users can sign up without one and add, change or remove it later on their profile page
- Public gallery with search and a filter by tradition
- Logged-in users can upload artworks (title, artist, tradition, year, description, image) and remove their own
- Optional members-only mode: set `REQUIRE_LOGIN_TO_VIEW=1` so only logged-in users can see the gallery
- SQLite database, created automatically on first run, with four sample artworks

## Run it on your computer

```bash
git clone https://github.com/<your-username>/art-gallery.git
cd art-gallery
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

## Put it on GitHub

```bash
git init
git add .
git commit -m "Traditional art gallery"
git branch -M main
git remote add origin https://github.com/<your-username>/art-gallery.git
git push -u origin main
```

## Make it live on the internet

GitHub stores the code, but **GitHub Pages cannot run Python** (it only serves static HTML), so logins wouldn't work there. Deploy the GitHub repo to a free Python host instead:

**Render (easiest — uses the included `render.yaml`)**
1. Sign in at https://render.com with your GitHub account.
2. New → Blueprint → pick this repository → Apply.
3. Render installs the requirements, starts `gunicorn app:app`, and generates a `SECRET_KEY` for you.

**PythonAnywhere** also works: clone the repo there, create a Flask web app pointing at `app.py`, and set `SECRET_KEY` in the WSGI file.

> Note: free hosting plans often reset the disk on redeploy, which wipes the SQLite database and uploaded images. For a permanent site, attach a persistent disk and set `DATABASE_PATH` to a file on it (and keep uploads there too), or move to a hosted database later.

## Settings (environment variables)

| Variable | Default | What it does |
|---|---|---|
| `SECRET_KEY` | `dev-only-change-me` | Signs login sessions. **Always set a long random value in production.** |
| `REQUIRE_LOGIN_TO_VIEW` | `0` | `1` = gallery is members-only |
| `DATABASE_PATH` | `gallery.db` | Where the SQLite file lives |

## Project layout

```
app.py              # all routes, database and login logic
templates/          # HTML pages (Jinja2)
static/style.css    # styling (light + dark mode)
static/samples/     # sample artwork images
static/uploads/     # user uploads (git-ignored)
requirements.txt
render.yaml         # one-click deploy on Render
```
