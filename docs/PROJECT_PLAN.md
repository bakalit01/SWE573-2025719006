# Indigenous Crafts Platform — 10-Week Project Plan

**Start:** Mon 12 Oct 2026 · **Feature-complete:** Sun 6 Dec 2026 · **Course end:** Sun 20 Dec 2026
**Way of working:** GitHub-driven (Issues, Milestones, Projects board, PRs, Actions CI), 2-week sprints, weekly tagged releases so every week shows a visible increment.

---

## 1. Goal

A website that documents and showcases Indigenous crafts, where registered users can sign in and record crafts with rich, **craft-specific attributes** (a woven textile, a clay vessel, a beaded bag and a carved mask all need different fields). The platform must treat cultural knowledge with care: communities and makers are credited, consent is recorded, and some content can be restricted.

## 2. Milestones & delivery gates

> **Timeline accelerated on 13 Oct 2026.** M1 was delivered in week 1 instead of week 2, so every later milestone moves two weeks earlier. Weeks 9–10 are now buffer for user feedback, polish and stretch goals before the course deadline (20 Dec).

| Milestone | Due (new) | Was | Gate | What a viewer can do |
|---|---|---|---|---|
| **M1 — Running Demo** | ✅ **Tue 13 Oct** (wk 1) | 25 Oct | v0.2.0, CI green, deployable | Browse sample crafts, open a craft page, sign up / log in / log out |
| **M2 — Contribute** | Sun 25 Oct (end wk 2) | 8 Nov | v0.4 | Logged-in users add/edit crafts with photos; attributes change by craft type; password reset and profiles |
| **M3 — MVP** | Sun 8 Nov (end wk 4) | 22 Nov | v0.6, user test #1 | Search & filter, roles (maker / steward / admin), visibility & consent, steward review, reporting, community pages |
| **M4 — Enrich** | Sun 22 Nov (end wk 6) | 6 Dec | v0.8 | Admin-managed craft types & attributes, Traditional Knowledge labels, multilingual names, favourites/collections, accessibility pass |
| **M5 — Final** | Sun 6 Dec (end wk 8) | 20 Dec | v1.0, user test #2 | Hardened, documented, tested, performant production release |
| Buffer | 7–20 Dec (wk 9–10) | — | Final presentation | Feedback fixes, stretch goals, course hand-in |

## 3. Week-by-week

| Wk | Dates | Focus | Release |
|---|---|---|---|
| 1 | 12–18 Oct | ✅ Planning, Django project, models, sample data, sign-up/login, catalogue, detail, CI, tests (done 13 Oct). Then add-craft form with craft-type fields | ✅ v0.1.0 + **v0.2.0 Demo (M1)**, v0.3 |
| 2 | 19–25 Oct | Image upload, edit/delete, password reset, profiles | **v0.4 (M2)** |
| 3 | 26 Oct–1 Nov | Search & filters, roles & permissions, visibility levels | v0.5 |
| 4 | 2–8 Nov | Consent records, steward review queue, reporting, community pages, user test #1 | **v0.6 — MVP (M3)** |
| 5 | 9–15 Nov | Admin UI for craft types/attributes, TK labels, sensitive images | v0.7 |
| 6 | 16–22 Nov | Multilingual names, favourites/collections, taxonomies, accessibility audit | **v0.8 (M4)** |
| 7 | 23–29 Nov | Security review, performance, user test #2 | v0.9 (RC) |
| 8 | 30 Nov–6 Dec | Documentation, final fixes | **v1.0 — Final (M5)** |
| 9–10 | 7–20 Dec | Buffer: feedback, polish, stretch goals, final presentation | v1.x |

**Incremental-improvement evidence:** each release is tagged (`v0.x`) with GitHub-generated release notes listing closed issues; `CHANGELOG.md` is updated; screenshots per release live in `docs/design/`; milestone progress is visible on GitHub.

## 3a. Story sequence (what to build, in order)

Each week's items build on the previous week's. "Depends on" lists what must be merged first. A live checklist is kept in the [Roadmap issue #65](https://github.com/bakalit01/SWE573-2025719006/issues/65).

| Week | Dates | ID | Issue | Story / task | Pts | Depends on |
|---|---|---|---|---|---|---|
| 1 | 12–18 Oct | T-01 | [#24](https://github.com/bakalit01/SWE573-2025719006/issues/24) | Repo, branch protection, project board | 1 | — |
|  |  | T-02 | [#25](https://github.com/bakalit01/SWE573-2025719006/issues/25) | Stack & hosting ADR | 1 | — |
|  |  | T-03 | [#26](https://github.com/bakalit01/SWE573-2025719006/issues/26) | Scaffold Django project, deploy config | 2 | T-02 |
|  |  | T-04 | [#27](https://github.com/bakalit01/SWE573-2025719006/issues/27) | CI pipeline | 2 | T-03 |
|  |  | T-08 | [#29](https://github.com/bakalit01/SWE573-2025719006/issues/29) | Test setup & factories | 2 | T-03 |
|  |  | T-06 | [#30](https://github.com/bakalit01/SWE573-2025719006/issues/30) | UI design reference | 2 | — |
|  |  | T-07 | [#31](https://github.com/bakalit01/SWE573-2025719006/issues/31) | Release process & CHANGELOG | 1 | T-03 |
|  |  | T-05 | [#28](https://github.com/bakalit01/SWE573-2025719006/issues/28) | Django models v1 + sample data | 3 | T-03 |
|  |  | US-01 | [#32](https://github.com/bakalit01/SWE573-2025719006/issues/32) | Register an account | 3 | T-05 |
|  |  | US-02 | [#33](https://github.com/bakalit01/SWE573-2025719006/issues/33) | Log in and log out | 2 | US-01 |
|  |  | US-06 | [#37](https://github.com/bakalit01/SWE573-2025719006/issues/37) | Browse the craft catalogue | 3 | T-05 |
|  |  | US-07 | [#38](https://github.com/bakalit01/SWE573-2025719006/issues/38) | View craft details | 3 | US-06 |
| | | | | ➜ Release **v0.2.0: running demo (M1), delivered Tue 13 Oct** · 25 pts | | |
| 1 | 14–18 Oct | US-08 | [#39](https://github.com/bakalit01/SWE573-2025719006/issues/39) | Add a craft | 5 | US-02, T-05 |
|  |  | US-11 | [#42](https://github.com/bakalit01/SWE573-2025719006/issues/42) | Craft-type-specific fields in the form | 8 | US-08 |
|  |  | US-12 | [#43](https://github.com/bakalit01/SWE573-2025719006/issues/43) | Show craft-specific attributes | 2 | US-11 |
| | | | | ➜ Release v0.3 (Sun 18 Oct) · 15 pts | | |
| 2 | 19–25 Oct | US-20 | [#51](https://github.com/bakalit01/SWE573-2025719006/issues/51) | Upload images with alt text & credit | 5 | US-08 |
|  |  | US-09 | [#40](https://github.com/bakalit01/SWE573-2025719006/issues/40) | Edit or delete my craft | 3 | US-08 |
|  |  | US-03 | [#34](https://github.com/bakalit01/SWE573-2025719006/issues/34) | Reset a forgotten password | 3 | US-02 |
|  |  | US-04 | [#35](https://github.com/bakalit01/SWE573-2025719006/issues/35) | Manage my profile | 3 | US-02 |
| | | | | ➜ Release **v0.4: contribute (M2)** · 14 pts | | |
| 3 | 26 Oct–1 Nov | US-05 | [#36](https://github.com/bakalit01/SWE573-2025719006/issues/36) | Roles and permissions | 5 | US-02 |
|  |  | US-22 | [#53](https://github.com/bakalit01/SWE573-2025719006/issues/53) | Set visibility of a craft | 5 | US-05 |
|  |  | US-15 | [#46](https://github.com/bakalit01/SWE573-2025719006/issues/46) | Search crafts | 5 | US-22 |
|  |  | US-16 | [#47](https://github.com/bakalit01/SWE573-2025719006/issues/47) | Filter and sort the catalogue | 5 | US-15 |
| | | | | ➜ Release v0.5 · 20 pts | | |
| 4 | 2–8 Nov | US-23 | [#54](https://github.com/bakalit01/SWE573-2025719006/issues/54) | Record consent | 3 | US-22 |
|  |  | US-24 | [#55](https://github.com/bakalit01/SWE573-2025719006/issues/55) | Steward review queue | 5 | US-05, US-23 |
|  |  | US-25 | [#56](https://github.com/bakalit01/SWE573-2025719006/issues/56) | Report a record / request removal | 3 | US-24 |
|  |  | US-17 | [#48](https://github.com/bakalit01/SWE573-2025719006/issues/48) | Community pages | 3 | US-06 |
|  |  | US-27 | [#58](https://github.com/bakalit01/SWE573-2025719006/issues/58) | Manage users (largely Django admin) | 3 | US-05 |
| | | | | ➜ Release **v0.6: MVP (M3)** + user test #1 · 17 pts | | |
| 5 | 9–15 Nov | US-13 | [#44](https://github.com/bakalit01/SWE573-2025719006/issues/44) | Manage craft types and attributes | 8 | US-11 |
|  |  | US-26 | [#57](https://github.com/bakalit01/SWE573-2025719006/issues/57) | Traditional Knowledge labels | 3 | US-24 |
|  |  | US-21 | [#52](https://github.com/bakalit01/SWE573-2025719006/issues/52) | Sensitive image notice | 2 | US-20 |
| | | | | ➜ Release v0.7 · 13 pts | | |
| 6 | 16–22 Nov | US-10 | [#41](https://github.com/bakalit01/SWE573-2025719006/issues/41) | Names in multiple languages | 3 | US-08 |
|  |  | US-18 | [#49](https://github.com/bakalit01/SWE573-2025719006/issues/49) | Favourites and collections | 5 | US-22 |
|  |  | US-28 | [#59](https://github.com/bakalit01/SWE573-2025719006/issues/59) | Manage taxonomies | 3 | US-27 |
|  |  | US-29 | [#60](https://github.com/bakalit01/SWE573-2025719006/issues/60) | Accessible site | 5 | — |
|  |  | US-19 | [#50](https://github.com/bakalit01/SWE573-2025719006/issues/50) | Filter by craft-specific attributes *(stretch)* | 5 | US-16, US-13 |
| | | | | ➜ Release **v0.8: enrich (M4)** · 21 pts | | |
| 7 | 23–29 Nov | US-30 | [#61](https://github.com/bakalit01/SWE573-2025719006/issues/61) | Security and privacy hardening | 5 | — |
|  |  | US-31 | [#62](https://github.com/bakalit01/SWE573-2025719006/issues/62) | Fast on mobile | 3 | — |
|  |  | US-14 | [#45](https://github.com/bakalit01/SWE573-2025719006/issues/45) | Suggest a new craft type or attribute *(stretch)* | 3 | US-13 |
| | | | | ➜ Release v0.9: release candidate + user test #2 · 11 pts | | |
| 8 | 30 Nov–6 Dec | US-32 | [#63](https://github.com/bakalit01/SWE573-2025719006/issues/63) | Final documentation and handover | 3 | all |
| | | | | ➜ Release **v1.0: final product (M5)** · 3 pts | | |
| 9–10 | 7–20 Dec | | | Buffer: user feedback, polish, stretch goals (map view, edit history), final presentation | | |

**Capacity note:** roughly 12–20 points per week. Items marked *stretch* are dropped first if time runs short; weeks 9–10 absorb any slip.

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
