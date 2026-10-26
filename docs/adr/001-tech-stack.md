# ADR-001: Python / Django tech stack

- **Status:** Accepted
- **Date:** 12 Oct 2026

## Context
The project must be Python-based and deliver a running demo by week 2, an MVP by week 6 and v1.0 by week 10. Core needs: accounts with roles, very diverse craft attributes, an admin back-office, strict visibility rules, and good performance on low-bandwidth connections.

## Decision
- **Django 5.2 LTS** on Python 3.12+, **PostgreSQL 16**
- Craft-specific attributes in a `JSONField` (jsonb), validated against `AttributeDefinition` rows; forms built at runtime
- Server-rendered templates (no separate SPA); plain CSS for M1, with HTMX added when pages need partial updates (M2)
- `django-allauth` for sign-up/login/reset; `rules` (django-rules) for object-level permissions
- Django admin as the back-office for M1–M3
- `django-storages` + S3-compatible storage for images; Pillow for resizing
- pytest / pytest-django / factory_boy / Playwright for Python; ruff; uv
- Docker + gunicorn + whitenoise; **hosting: Render** (free web service + PostgreSQL, defined in `render.yaml`), chosen on 13 Oct 2026

## Alternatives considered
- **FastAPI + SQLAlchemy + separate front end:** more flexible API, but auth, admin, forms and migrations would all be built by hand, putting the week-2 demo at risk.
- **Flask:** lightweight, but needs many extensions to match Django's built-ins.
- **Wagtail (Django CMS):** strong for editorial pages, but heavier than needed; could be added later for static content pages.
- **EAV tables for attributes:** fully relational, but many joins and complex queries; JSONField + definitions gives the same flexibility more simply.

## Consequences
- Fast M1: auth, admin and CRUD come almost for free.
- Attribute filtering relies on PostgreSQL JSON operators and GIN indexes, so the app is tied to PostgreSQL (SQLite isn't supported, not even for local development; use Docker).
- If a public API is needed later, add Django REST Framework or Django Ninja.

## Update · 26 Oct 2026 (after M2)
What was built differs from the plan above in a few places. The decision (Python / Django / PostgreSQL) stands.
- **Front end:** plain CSS and small plain-JavaScript enhancements were enough for M1–M2 (dynamic craft-type fields, map picker, repeatable rows). HTMX was not needed; it can still be added if later pages need partial reloads.
- **Images:** Pillow resizes uploads; files are stored on the server disk, which Render resets on each deploy. `django-storages` with S3-compatible storage is still planned before v1.0. The real examples show photos from Wikimedia Commons.
- **Permissions:** author-or-staff checks in views so far; `rules` (django-rules) arrives with roles in M3 (US-05).
- **Hosting:** Render, deployed from `main` by the Blueprint in `render.yaml`.
