# Indigenous Crafts Platform — 10-Week Project Plan

**Start:** Mon 12 Oct 2026 · **Complete:** Thu 26 Nov 2026 (M4, v0.8.0) · **Course end:** Sun 20 Dec 2026
**Way of working:** GitHub-driven (Issues, Milestones, Projects board, PRs, Actions CI), 2-week sprints, weekly tagged releases so every week shows a visible increment.

---

## 1. Goal

A website that documents and showcases Indigenous crafts, where registered users can sign in and record crafts with rich, **craft-specific attributes** (a woven textile, a clay vessel, a beaded bag and a carved mask all need different fields). The platform must treat cultural knowledge with care: communities and makers are credited, consent is recorded, and some content can be restricted.

## 2. Milestones & delivery gates

> **Timeline accelerated on 13 Oct 2026.** M1 was delivered in week 1 instead of week 2, so every later milestone moves two weeks earlier.
>
> **M4 is the final milestone (26 Nov 2026).** Three M4 stories (US-21 sensitive photos, US-26 TK labels, US-29 accessibility audit) were dropped; their issues are closed as not planned. The time until the course deadline (20 Dec) is for the final presentation.

| Milestone | Due (new) | Was | Gate | What a viewer can do |
|---|---|---|---|---|
| **M1 — Running Demo** | ✅ **Tue 13 Oct** (wk 1) | 25 Oct | v0.2.0, CI green, deployable | Browse sample crafts, open a craft page, sign up / log in / log out |
| **M2 — Contribute** | ✅ **Sun 25 Oct** (end wk 2) | 8 Nov | v0.4.0 (+ feedback releases v0.4.1–v0.4.5) | Logged-in users add/edit crafts with photos; attributes change by craft type; password reset and profiles |
| **M3 — MVP** | ✅ **Mon 2 Nov** (start wk 4) | 22 Nov | v0.5.0 + v0.6.0 (+ v0.6.1–v0.6.2); user test #1 moved to week 5 | Search & filter, roles (maker / steward / admin), visibility & consent, steward review, reporting, community pages |
| **M4 — Enrich (final)** | ✅ **Thu 26 Nov** (wk 7) | 6 Dec | v0.8.0 (v0.7.0/v0.7.1 of 16 Nov withdrawn) | Admin-managed craft types & fields, names in other languages, favourites & collections, managed taxonomies (merge, alternate spellings), filters by craft-specific fields |
| Until 20 Dec | wk 8–10 | — | Final presentation | Course hand-in |

## 3. Week-by-week

| Wk | Dates | Focus | Release |
|---|---|---|---|
| 1 | 12–18 Oct | ✅ Planning, Django project, models, sample data, sign-up/login, catalogue, detail, CI, tests (done 13 Oct). Then add-craft form with craft-type fields | ✅ v0.1.0 + **v0.2.0 Demo (M1)**; v0.3 merged into v0.4 |
| 2 | 19–25 Oct | ✅ Image upload, edit/delete, password reset, profiles, feedback FB-01–FB-04 | ✅ **v0.4.0 (M2)**, v0.4.1 map fix |
| 3 | 26 Oct–1 Nov | ✅ Feedback FB-05–FB-09 (real examples, Boğaziçi colours, "Other" + tags, crafts from Türkiye and East Asia; 26 Oct) | ✅ v0.4.2–v0.4.9 |
| 4 | 2–8 Nov | ✅ Roles, visibility levels, search & filters (from week 3), consent records, steward review queue, reporting, community pages (2 Nov); feedback FB-10–FB-11 (stories, location search); admin login fix (3 Nov) | ✅ v0.5.0, **v0.6.0 — MVP (M3)**, v0.6.1, v0.6.2 |
| 5–6 | 9–22 Nov | Admin UI for craft types/fields, multilingual names, TK labels and sensitive photos (16 Nov; released as v0.7.0/v0.7.1, then withdrawn the same day after a failed deploy caused by an expired database) | v0.7.0, v0.7.1 (withdrawn) |
| 7 | 23–29 Nov | ✅ Craft types and names rebuilt without TK labels and sensitive photos; favourites & collections, managed taxonomies, filters by craft-specific fields (26 Nov); scope closed at M4 | ✅ **v0.8.0 — Enrich (M4, final)** |
| 8–10 | 30 Nov–20 Dec | Final presentation | — |

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
| | | | | ➜ Release v0.3 (Sun 18 Oct): skipped, shipped with v0.4 · 15 pts | | |
| 2 | 19–25 Oct | US-20 | [#51](https://github.com/bakalit01/SWE573-2025719006/issues/51) | Upload images with alt text & credit | 5 | US-08 |
|  |  | US-09 | [#40](https://github.com/bakalit01/SWE573-2025719006/issues/40) | Edit or delete my craft | 3 | US-08 |
|  |  | US-03 | [#34](https://github.com/bakalit01/SWE573-2025719006/issues/34) | Reset a forgotten password | 3 | US-02 |
|  |  | US-04 | [#35](https://github.com/bakalit01/SWE573-2025719006/issues/35) | Manage my profile | 3 | US-02 |
|  |  | FB-01 | [#68](https://github.com/bakalit01/SWE573-2025719006/issues/68) | Place as geolocation (feedback) | — | US-08 |
|  |  | FB-02 | [#69](https://github.com/bakalit01/SWE573-2025719006/issues/69) | Materials & techniques in detail (feedback) | — | US-08 |
|  |  | FB-03 | [#70](https://github.com/bakalit01/SWE573-2025719006/issues/70) | Made by / from / in (feedback) | — | US-08 |
|  |  | FB-04 | [#71](https://github.com/bakalit01/SWE573-2025719006/issues/71) | 3D size and international units (feedback) | — | US-08 |
| | | | | ➜ Release **v0.4.0: contribute (M2)** ✅ 25 Oct · 14 pts + feedback | | |
|  |  | BUG | [#79](https://github.com/bakalit01/SWE573-2025719006/issues/79) | Maps fail on the deployed site | — | FB-01 |
| | | | | ➜ Release v0.4.1 ✅ 25 Oct | | |
| 3 | 26 Oct | FB-06 | [#80](https://github.com/bakalit01/SWE573-2025719006/issues/80) | Real-life craft examples (feedback) | — | US-06 |
|  |  | FB-07 | [#81](https://github.com/bakalit01/SWE573-2025719006/issues/81) | Boğaziçi University colours (feedback) | — | — |
|  |  | FB-09 | [#90](https://github.com/bakalit01/SWE573-2025719006/issues/90) | Five crafts from East Asia (feedback) | — | FB-06 |
|  |  | FB-08 | [#88](https://github.com/bakalit01/SWE573-2025719006/issues/88) | Eight more real crafts, four from Türkiye (feedback) | — | FB-06 |
|  |  | FB-05 | [#77](https://github.com/bakalit01/SWE573-2025719006/issues/77) | "Other" for type, community, units; tags (feedback) | — | US-11 |
| | | | | ➜ Releases v0.4.2–v0.4.9 ✅ 26 Oct | | |
| 3 | 26 Oct–1 Nov | US-05 | [#36](https://github.com/bakalit01/SWE573-2025719006/issues/36) | Roles and permissions | 5 | US-02 |
|  |  | US-22 | [#53](https://github.com/bakalit01/SWE573-2025719006/issues/53) | Set visibility of a craft | 5 | US-05 |
|  |  | US-15 | [#46](https://github.com/bakalit01/SWE573-2025719006/issues/46) | Search crafts | 5 | US-22 |
|  |  | US-16 | [#47](https://github.com/bakalit01/SWE573-2025719006/issues/47) | Filter and sort the catalogue | 5 | US-15 |
| | | | | ➜ Release **v0.5.0** ✅ 2 Nov (built in week 4, after the week-3 feedback rounds) · 20 pts | | |
| 4 | 2–8 Nov | US-23 | [#54](https://github.com/bakalit01/SWE573-2025719006/issues/54) | Record consent | 3 | US-22 |
|  |  | US-24 | [#55](https://github.com/bakalit01/SWE573-2025719006/issues/55) | Steward review queue | 5 | US-05, US-23 |
|  |  | US-25 | [#56](https://github.com/bakalit01/SWE573-2025719006/issues/56) | Report a record / request removal | 3 | US-24 |
|  |  | US-17 | [#48](https://github.com/bakalit01/SWE573-2025719006/issues/48) | Community pages | 3 | US-06 |
|  |  | US-27 | [#58](https://github.com/bakalit01/SWE573-2025719006/issues/58) | Manage users (largely Django admin) | 3 | US-05 |
| | | | | ➜ Release **v0.6.0: MVP (M3)** ✅ 2 Nov · 17 pts (user test #1 moved to week 5) | | |
| 5–7 | 16–26 Nov | US-13 | [#44](https://github.com/bakalit01/SWE573-2025719006/issues/44) | Manage craft types and attributes | 8 | US-11 |
|  |  | US-10 | [#41](https://github.com/bakalit01/SWE573-2025719006/issues/41) | Names in multiple languages | 3 | US-08 |
|  |  | US-18 | [#49](https://github.com/bakalit01/SWE573-2025719006/issues/49) | Favourites and collections | 5 | US-22 |
|  |  | US-28 | [#59](https://github.com/bakalit01/SWE573-2025719006/issues/59) | Manage taxonomies | 3 | US-27 |
|  |  | US-19 | [#50](https://github.com/bakalit01/SWE573-2025719006/issues/50) | Filter by craft-specific attributes | 5 | US-16, US-13 |
| | | | | ➜ Release **v0.8.0: enrich (M4, final)** ✅ 26 Nov · 24 pts | | |
| — | dropped 26 Nov | US-21, US-26, US-29 | [#52](https://github.com/bakalit01/SWE573-2025719006/issues/52), [#57](https://github.com/bakalit01/SWE573-2025719006/issues/57), [#60](https://github.com/bakalit01/SWE573-2025719006/issues/60) | Not planned | 10 | |

**Capacity note:** roughly 12–20 points per week. Delivered: M1–M4. Dropped on 26 Nov: 10 points (see the last row).

## 4. Tech stack — Python (recorded in ADR-001, issue T-02)

| Concern | Choice | Why |
|---|---|---|
| Language | Python 3.12+ | Team requirement |
| Framework | Django 5.2 LTS | Batteries included: auth, sessions, CSRF, forms, ORM, migrations, admin; LTS covers the project and beyond |
| Database | PostgreSQL 16 (managed: Render, Railway, Neon or Supabase) | Relational core + `JSONField` (stored as `jsonb`) for craft-specific attributes; GIN indexes; full-text search via `django.contrib.postgres` |
| Auth | Django auth with a custom `User` model + `django-allauth` | Email login, sign-up, password reset, optional Google login (FR-A6) with little code |
| Roles & permissions | A `role` field (member, maker, steward, admin), stewards assigned per community, and plain functions in `accounts/permissions.py` for object-level checks *(django-rules not needed)* | "Steward of *this* community", "creator of *this* craft" |
| Dynamic attributes | `AttributeDefinition` model → Django form fields built at runtime; values validated in `clean()` (optionally via `pydantic`) | Forms and validation generated from data, no deploy to add a field |
| Admin back-office | Django admin (customised) | Users, roles, taxonomies and craft types for free in M1–M3; in M4, craft types with sortable, retirable fields and checks that protect stored values, and the TK / BC label list |
| Front end | Server-rendered Django templates, hand-written CSS (Boğaziçi colours) and small plain-JavaScript enhancements; HTMX only if pages need partial reloads *(Tailwind dropped: no build step needed)* | No separate JS app; fast pages on low bandwidth; easier accessibility |
| Images | Pillow resizes uploads to 1600 px; stored on the server disk for the demo (reset on Render redeploys). Object storage (`django-storages`) was not added. Real examples show Wikimedia Commons photos | Images outside the DB, resized variants |
| Search | Every word matched across fields (incl. names in every language, materials, techniques, community, tags), ignoring accents (PostgreSQL `unaccent`), ranked with PostgreSQL full-text (`SearchVector`, `SearchRank`); filters in the view *(django-filter not needed)* | No extra search service needed for v1 |
| Testing | `pytest`, `pytest-django`, `factory_boy`, `coverage`; Playwright for Python for browser tests (`axe-playwright-python` was planned for US-29, dropped) | All Python, all in CI |
| Code quality | `ruff` (lint + format), `mypy` + `django-stubs` (optional), `pre-commit` | Consistent style, fast |
| Dependencies | `uv` with `pyproject.toml` (or pip + `requirements.txt`) | Reproducible installs |
| Serving | `gunicorn` + `whitenoise` for static files, Docker image | Works on any host |
| Hosting / CI | GitHub Actions CI; Render Blueprint (`render.yaml`) deploys `main` | Every PR is demoable |
| Optional API | Django REST Framework or Django Ninja (only if a mobile app or external partners need it) | Not built |

**Why Django suits this project:** the built-in admin, auth and forms remove most of the effort behind the week-2 demo, so the team can spend its time on the parts specific to this project: flexible attributes, visibility rules and community review.

## 5. GitHub workflow

- **Issues:** one per user story (`US-xx`) or technical task (`T-xx`), labelled with the repo scheme (`type:`, `priority:`, `effort:`, `area:`, `status:`) plus `epic:`, assigned to a milestone.
- **Project board:** Backlog → Ready → In progress → In review → Done (still to be created, T-01). Until then, milestones and the [Roadmap issue #65](https://github.com/bakalit01/SWE573-2025719006/issues/65) show progress.
- **Branches:** feature branches `us-12-craft-search`; PRs link issues with `Closes #n`; green CI to merge. `main` is to be protected (PR + CI check `test`); as a one-person project no approving review is required, since GitHub does not allow approving your own PR.
- **Feedback:** each piece of instructor or user feedback becomes an `FB-xx` issue with the `feedback` label, in the milestone where it is delivered.
- **Definition of Done:** acceptance criteria met, tests added, CI green, deployed to preview, accessible (keyboard + screen reader basics), docs updated if needed.
- **Ceremonies:** sprint planning (Mon, wk 1/3/5/7/9), short stand-ups, demo + retro at each milestone.

## 6. Risks

| Risk | Mitigation |
|---|---|
| Craft attributes are too diverse for a fixed schema | Core fields + per-craft-type attribute schemas stored as data (see REQUIREMENTS §4) |
| Cultural harm from publishing restricted/sacred knowledge | Visibility levels, consent records, steward review, takedown process (TK labels were dropped with US-26) |
| Scope creep before MVP | MoSCoW priorities; only `Must` items in M1–M3 |
| Lack of real community input | Involve at least one community advisor; use placeholder/clearly-marked sample data until consent is obtained |
| Image storage costs / sizes | Client-side resize, size limits, CDN |
