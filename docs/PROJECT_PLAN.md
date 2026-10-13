# Indigenous Crafts Platform — 10-Week Project Plan

**Start:** Mon 12 Oct 2026 · **End:** Sun 20 Dec 2026
**Way of working:** GitHub-driven (Issues, Milestones, Projects board, PRs, Actions CI), 2-week sprints, weekly tagged releases so every week shows a visible increment.

---

## 1. Goal

A website that documents and showcases Indigenous crafts, where registered users can sign in and record crafts with rich, **craft-specific attributes** (a woven textile, a clay vessel, a beaded bag and a carved mask all need different fields). The platform must treat cultural knowledge with care: communities and makers are credited, consent is recorded, and some content can be restricted.

## 2. Milestones & delivery gates

| Milestone | Due | Gate | What a viewer can do |
|---|---|---|---|
| **M1 — Running Demo** | Sun 25 Oct (end wk 2) | Deployed URL, CI green | Browse seeded crafts, open a craft page, sign up / log in / log out |
| **M2 — Contribute** | Sun 8 Nov (end wk 4) | v0.4 | Logged-in users add/edit crafts with photos; attributes change by craft type |
| **M3 — MVP** | Sun 22 Nov (end wk 6) | v0.6, user test #1 | Search & filter, roles (maker / steward / admin), visibility & consent, moderation queue, maker profiles |
| **M4 — Enrich** | Sun 6 Dec (end wk 8) | v0.8 | Admin-managed craft types & attributes, Traditional Knowledge labels, multilingual names, favourites/collections, accessibility pass |
| **M5 — Final** | Sun 20 Dec (end wk 10) | v1.0, user test #2 | Hardened, documented, tested, performant production release |

## 3. Week-by-week

| Wk | Dates | Focus | Release |
|---|---|---|---|
| 1 | 12–18 Oct | Requirements, user stories, issues, tech decision (ADR), repo + CI + hosting, data model draft, wireframes | v0.1 — "hello world" deployed |
| 2 | 19–25 Oct | Auth (sign up / log in), craft list + detail from seed data, basic layout | **v0.2 — Demo (M1)** |
| 3 | 26 Oct–1 Nov | Create/edit craft form, craft types, flexible attribute engine v1 | v0.3 |
| 4 | 2–8 Nov | Image upload & gallery, validation, my-crafts page | v0.4 (M2) |
| 5 | 9–15 Nov | Search & filters, roles & permissions, visibility levels | v0.5 |
| 6 | 16–22 Nov | Consent records, moderation queue, maker profiles, user test #1 | **v0.6 — MVP (M3)** |
| 7 | 23–29 Nov | Admin UI for craft types/attributes, TK labels, feedback fixes | v0.7 |
| 8 | 30 Nov–6 Dec | Multilingual names, favourites/collections, accessibility audit | v0.8 (M4) |
| 9 | 7–13 Dec | Security review, performance, test coverage, user test #2 | v0.9 (RC) |
| 10 | 14–20 Dec | Bug fixes, documentation, final demo & handover | **v1.0 — Final (M5)** |

**Incremental-improvement evidence:** each Friday tag a release (`v0.x`) with GitHub-generated release notes listing closed issues; keep a `CHANGELOG.md`; record a 2-minute demo clip or screenshots per release; the Projects board "Done" column per milestone shows burn-down.

## 4. Tech stack — Python (recorded in ADR-001, issue T-02)

| Concern | Choice | Why |
|---|---|---|
| Language | Python 3.12+ | Team requirement |
| Framework | Django 5.2 LTS | Batteries included: auth, sessions, CSRF, forms, ORM, migrations, admin; LTS covers the project and beyond |
| Database | PostgreSQL 16 (managed: Render, Railway, Neon or Supabase) | Relational core + `JSONField` (stored as `jsonb`) for craft-specific attributes; GIN indexes; full-text search via `django.contrib.postgres` |
| Auth | Django auth with a custom `User` model + `django-allauth` | Email login, sign-up, password reset, optional Google login (FR-A6) with little code |
| Roles & permissions | Django groups/permissions + `rules` (django-rules) for object-level checks | "Steward of *this* community", "creator of *this* craft" |
| Dynamic attributes | `AttributeDefinition` model → Django form fields built at runtime; values validated in `clean()` (optionally via `pydantic`) | Forms and validation generated from data, no deploy to add a field |
| Admin back-office | Django admin (customised) | Users, roles, taxonomies and craft types for free in M1–M3; polished admin UI in M4 |
| Front end | Server-rendered Django templates + HTMX + Tailwind CSS (via `django-tailwind` or standalone CLI) | No separate JS app; fast pages on low bandwidth; easier accessibility |
| Images | Pillow + `django-storages` (S3-compatible: Cloudflare R2 / Supabase Storage); `sorl-thumbnail` or `django-imagekit` for resizing | Images outside the DB, resized variants |
| Search | PostgreSQL full-text (`SearchVector`, `TrigramSimilarity`) + `django-filter` | No extra search service needed for v1 |
| Testing | `pytest`, `pytest-django`, `factory_boy`, `coverage`; Playwright for Python + `axe-playwright-python` for e2e/a11y | All Python, all in CI |
| Code quality | `ruff` (lint + format), `mypy` + `django-stubs` (optional), `pre-commit` | Consistent style, fast |
| Dependencies | `uv` with `pyproject.toml` (or pip + `requirements.txt`) | Reproducible installs |
| Serving | `gunicorn` + `whitenoise` for static files, Docker image | Works on any host |
| Hosting / CI | GitHub Actions → Render (or Railway / Fly.io) with PR preview environments | Every PR is demoable |
| Optional API | Django REST Framework or Django Ninja (M4+, only if a mobile app or external partners need it) | Not required for v1 |

**Why Django suits this project:** the built-in admin, auth and forms remove most of the effort behind the week-2 demo, so the team can spend its time on the parts specific to this project: flexible attributes, visibility rules and community review.

## 5. GitHub workflow

- **Issues:** one per user story (`US-xx`) or technical task (`T-xx`), labelled with the repo scheme (`type:`, `priority:`, `effort:`, `area:`, `status:`) plus `epic:`, assigned to a milestone.
- **Project board:** Backlog → Ready → In progress → In review → Done.
- **Branches:** `main` protected; feature branches `us-12-craft-search`; PRs link issues with `Closes #n`; 1 review + green CI to merge.
- **Definition of Done:** acceptance criteria met, tests added, CI green, deployed to preview, accessible (keyboard + screen reader basics), docs updated if needed.
- **Ceremonies:** sprint planning (Mon, wk 1/3/5/7/9), short stand-ups, demo + retro at each milestone.

## 6. Risks

| Risk | Mitigation |
|---|---|
| Craft attributes are too diverse for a fixed schema | Core fields + per-craft-type attribute schemas stored as data (see REQUIREMENTS §4) |
| Cultural harm from publishing restricted/sacred knowledge | Visibility levels, consent records, steward review, TK labels, takedown process |
| Scope creep before MVP | MoSCoW priorities; only `Must` items in M1–M3 |
| Lack of real community input | Involve at least one community advisor; use placeholder/clearly-marked sample data until consent is obtained |
| Image storage costs / sizes | Client-side resize, size limits, CDN |
