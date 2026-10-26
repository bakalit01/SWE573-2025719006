# User Stories & Backlog

Source of truth for GitHub issues: `scripts/seed_github.py` turns every `### US-xx` and `### T-xx` section below into an issue (labels + milestone included). Edit here, then re-run the script; existing issue titles are skipped.

**Epics:** E0 Setup & DevOps · E1 Accounts · E2 Craft catalogue · E3 Flexible attributes · E4 Discovery · E5 Media · E6 Cultural protocols · E7 Administration · E8 Quality
**Milestones:** M1 Demo (✅ 13 Oct) · M2 Contribute (✅ 25 Oct) · M3 MVP (wk 4) · M4 Enrich (wk 6) · M5 Final (wk 8) · buffer wk 9–10
**Feedback items** (FB-01–FB-09) are listed at the [end of this file](#feedback-items); their issues are created by hand with the `feedback` label.

## Delivery order

Stories are grouped by epic below. This is the order to build them in (timeline accelerated on 13 Oct; M1 and M2 delivered). Details and dependencies are in [PROJECT_PLAN §3a](PROJECT_PLAN.md#3a-story-sequence-what-to-build-in-order).

| Week | Milestone | Items |
|---|---|---|
| 1 (12–18 Oct) | M1 | T-01 [#24](https://github.com/bakalit01/SWE573-2025719006/issues/24) → T-02 [#25](https://github.com/bakalit01/SWE573-2025719006/issues/25) → T-03 [#26](https://github.com/bakalit01/SWE573-2025719006/issues/26) → T-04 [#27](https://github.com/bakalit01/SWE573-2025719006/issues/27) → T-08 [#29](https://github.com/bakalit01/SWE573-2025719006/issues/29) → T-06 [#30](https://github.com/bakalit01/SWE573-2025719006/issues/30) → T-07 [#31](https://github.com/bakalit01/SWE573-2025719006/issues/31) → T-05 [#28](https://github.com/bakalit01/SWE573-2025719006/issues/28) → US-01 [#32](https://github.com/bakalit01/SWE573-2025719006/issues/32) → US-02 [#33](https://github.com/bakalit01/SWE573-2025719006/issues/33) → US-06 [#37](https://github.com/bakalit01/SWE573-2025719006/issues/37) → US-07 [#38](https://github.com/bakalit01/SWE573-2025719006/issues/38) |
| 1 (14–18 Oct) | M2 | US-08 [#39](https://github.com/bakalit01/SWE573-2025719006/issues/39) → US-11 [#42](https://github.com/bakalit01/SWE573-2025719006/issues/42) → US-12 [#43](https://github.com/bakalit01/SWE573-2025719006/issues/43) |
| 2 (19–25 Oct) | M2 | US-20 [#51](https://github.com/bakalit01/SWE573-2025719006/issues/51) → US-09 [#40](https://github.com/bakalit01/SWE573-2025719006/issues/40) → US-03 [#34](https://github.com/bakalit01/SWE573-2025719006/issues/34) → US-04 [#35](https://github.com/bakalit01/SWE573-2025719006/issues/35) → FB-01–FB-04 [#68](https://github.com/bakalit01/SWE573-2025719006/issues/68)–[#71](https://github.com/bakalit01/SWE573-2025719006/issues/71) ✅ |
| 3 (26 Oct) | M2 feedback | FB-06 [#80](https://github.com/bakalit01/SWE573-2025719006/issues/80) → FB-07 [#81](https://github.com/bakalit01/SWE573-2025719006/issues/81) → FB-05 [#77](https://github.com/bakalit01/SWE573-2025719006/issues/77) ✅ |
| 3 (26 Oct–1 Nov) | M3 | US-05 [#36](https://github.com/bakalit01/SWE573-2025719006/issues/36) → US-22 [#53](https://github.com/bakalit01/SWE573-2025719006/issues/53) → US-15 [#46](https://github.com/bakalit01/SWE573-2025719006/issues/46) → US-16 [#47](https://github.com/bakalit01/SWE573-2025719006/issues/47) |
| 4 (2–8 Nov) | M3 | US-23 [#54](https://github.com/bakalit01/SWE573-2025719006/issues/54) → US-24 [#55](https://github.com/bakalit01/SWE573-2025719006/issues/55) → US-25 [#56](https://github.com/bakalit01/SWE573-2025719006/issues/56) → US-17 [#48](https://github.com/bakalit01/SWE573-2025719006/issues/48) → US-27 [#58](https://github.com/bakalit01/SWE573-2025719006/issues/58) |
| 5 (9–15 Nov) | M4 | US-13 [#44](https://github.com/bakalit01/SWE573-2025719006/issues/44) → US-26 [#57](https://github.com/bakalit01/SWE573-2025719006/issues/57) → US-21 [#52](https://github.com/bakalit01/SWE573-2025719006/issues/52) |
| 6 (16–22 Nov) | M4 | US-10 [#41](https://github.com/bakalit01/SWE573-2025719006/issues/41) → US-18 [#49](https://github.com/bakalit01/SWE573-2025719006/issues/49) → US-28 [#59](https://github.com/bakalit01/SWE573-2025719006/issues/59) → US-29 [#60](https://github.com/bakalit01/SWE573-2025719006/issues/60) → US-19 [#50](https://github.com/bakalit01/SWE573-2025719006/issues/50) |
| 7 (23–29 Nov) | M5 | US-30 [#61](https://github.com/bakalit01/SWE573-2025719006/issues/61) → US-31 [#62](https://github.com/bakalit01/SWE573-2025719006/issues/62) → US-14 [#45](https://github.com/bakalit01/SWE573-2025719006/issues/45) |
| 8 (30 Nov–6 Dec) | M5 | US-32 [#63](https://github.com/bakalit01/SWE573-2025719006/issues/63) |
| 9–10 (7–20 Dec) | — | Buffer: feedback, polish, stretch goals |

---

## Technical tasks

### T-01 · Set up repository, branch protection and project board
**Epic:** E0 · **Milestone:** M1 · **Priority:** Must · **Points:** 1

Create the repo structure, protect `main` (PR + 1 review + green CI), create the GitHub Project board (Backlog → Ready → In progress → In review → Done), add issue/PR templates and CONTRIBUTING.md.

**Acceptance criteria**
- [ ] `main` is protected (PR + CI check `test`; no approving review, as a one-person project)
- [ ] Project board exists and all seeded issues are on it
- [x] Issue and PR templates are in `.github/`

### T-02 · Record Python/Django stack and hosting (ADR-001)
**Epic:** E0 · **Milestone:** M1 · **Priority:** Must · **Points:** 1

Stack is Python: Django 5.2 LTS + PostgreSQL 16, server-rendered templates + HTMX + Tailwind (PROJECT_PLAN §4). Record it in `docs/adr/001-tech-stack.md` and choose hosting for app, DB and images.

**Acceptance criteria**
- [ ] ADR merged with decision, alternatives considered and consequences
- [ ] Hosting (Render / Railway / Fly.io) and image storage (R2 / Supabase) chosen

### T-03 · Scaffold Django project and deploy "hello world"
**Epic:** E0 · **Milestone:** M1 · **Priority:** Must · **Points:** 2

Create the Django project with apps `accounts`, `crafts`, `communities`, `moderation`; settings split into base/dev/prod read from environment variables (`django-environ`); custom `User` model **from the first migration**; `pyproject.toml` (uv); Dockerfile; gunicorn + whitenoise.

**Acceptance criteria**
- [ ] `uv sync && python manage.py migrate && python manage.py runserver` works from README
- [ ] `docker compose up` starts app + PostgreSQL locally
- [ ] Production URL serves the landing page; `manage.py check --deploy` has no errors
- [ ] Each PR gets a preview environment

### T-04 · CI pipeline (ruff, pytest, migrations check)
**Epic:** E0 · **Milestone:** M1 · **Priority:** Must · **Points:** 2

GitHub Actions workflow with a PostgreSQL service container.

**Acceptance criteria**
- [ ] Runs `ruff check`, `ruff format --check`, `python manage.py makemigrations --check --dry-run`, `pytest --cov` on every PR and on `main`
- [ ] `pre-commit` hooks configured for ruff
- [ ] Failing job blocks merge

### T-05 · Django models v1 and sample data
**Epic:** E2 · **Milestone:** M1 · **Priority:** Must · **Points:** 3

Implement `User`, `Community`, `CraftType`, `AttributeDefinition`, `Craft` (with `attributes = JSONField`), `Media` models (REQUIREMENTS §4) and register them in the Django admin. Add a `seed_sample_data` management command creating 10–15 **clearly-marked sample** crafts across at least 4 craft types.

**Acceptance criteria**
- [ ] Migrations run from a clean database
- [ ] `python manage.py seed_sample_data` is idempotent (uses `update_or_create`)
- [ ] Sample records are labelled "Sample data" in the UI
- [ ] Models are editable in `/admin/` by a superuser

### T-08 · Python test setup and factories
**Epic:** E8 · **Milestone:** M1 · **Priority:** Must · **Points:** 2

**Acceptance criteria**
- [ ] `pytest-django` configured; `factory_boy` factories for User, Community, CraftType, Craft
- [ ] One smoke test per page passes in CI
- [ ] Playwright for Python installed with one e2e test (home page loads)

### T-06 · Wireframes for core pages
**Epic:** E0 · **Milestone:** M1 · **Priority:** Should · **Points:** 2

Low-fi wireframes for home, catalogue, craft detail, craft form, login, profile. Link them in the wiki or `docs/design/`.

**Acceptance criteria**
- [ ] Wireframes reviewed by the team and linked from the README

### T-07 · Release process and CHANGELOG
**Epic:** E0 · **Milestone:** M1 · **Priority:** Should · **Points:** 1

**Acceptance criteria**
- [ ] Weekly `v0.x` tags with auto-generated release notes
- [ ] `CHANGELOG.md` updated per release

---

## E1 — Accounts

### US-01 · Register an account
**Epic:** E1 · **Milestone:** M1 · **Priority:** Must · **Points:** 3

As a **visitor**, I want to **create an account with my email and a password**, so that **I can contribute and save crafts**.

**Acceptance criteria**
- [ ] Form validates email format and password strength (≥ 10 chars)
- [ ] Duplicate email shows a clear error
- [ ] Password is stored hashed, never in plain text
- [ ] After registering I am signed in and redirected to the home page

_Implementation: `django-allauth` with email as login; Argon2 hasher._

### US-02 · Log in and log out
**Epic:** E1 · **Milestone:** M1 · **Priority:** Must · **Points:** 2

As a **registered user**, I want to **log in and log out**, so that **my account is secure on shared devices**.

**Acceptance criteria**
- [ ] Wrong credentials show a generic error (no hint which field was wrong)
- [ ] Header shows my name and a logout button when signed in
- [ ] Logging out ends the session server-side (POST logout, CSRF-protected)

### US-03 · Reset a forgotten password
**Epic:** E1 · **Milestone:** M2 · **Priority:** Should · **Points:** 3

As a **registered user**, I want to **reset my password by email**, so that **I can recover my account**.

**Acceptance criteria**
- [ ] Reset link expires after 1 hour and works once
- [ ] Response is the same whether or not the email exists

### US-04 · Manage my profile
**Epic:** E1 · **Milestone:** M2 · **Priority:** Should · **Points:** 3

As a **maker**, I want to **edit my display name, bio, photo and community affiliation**, so that **visitors know who made the work**.

**Acceptance criteria**
- [ ] Profile page is public and lists my published crafts
- [ ] Community affiliation is chosen from the community list (or "request new")

### US-05 · Roles and permissions
**Epic:** E1 · **Milestone:** M3 · **Priority:** Must · **Points:** 5

As an **admin**, I want **users to have roles (member, maker, steward, admin)**, so that **people only do what they are allowed to**.

**Acceptance criteria**
- [ ] Permissions are enforced on the server, not only hidden in the UI
- [ ] Admin can change a user's role
- [ ] Automated tests cover each role's allowed/denied actions

---

## E2 — Craft catalogue

### US-06 · Browse the craft catalogue
**Epic:** E2 · **Milestone:** M1 · **Priority:** Must · **Points:** 3

As a **visitor**, I want to **see a grid of crafts with image, name, craft type and community**, so that **I can explore what is on the site**.

**Acceptance criteria**
- [ ] Only records I'm allowed to see are listed
- [ ] Cards link to the detail page
- [ ] Layout works on phone and desktop

### US-07 · View craft details
**Epic:** E2 · **Milestone:** M1 · **Priority:** Must · **Points:** 3

As a **visitor**, I want to **open a craft page showing its story, makers, community, materials, techniques and images**, so that **I can learn about it**.

**Acceptance criteria**
- [ ] Makers and community are credited prominently
- [ ] Page has a "Report / request removal" link
- [ ] Unauthorized access to a restricted craft returns "not found"

### US-08 · Add a craft
**Epic:** E2 · **Milestone:** M2 · **Priority:** Must · **Points:** 5

As a **maker**, I want to **create a craft record with its core details**, so that **it is documented on the platform**.

**Acceptance criteria**
- [ ] Required: title, craft type, community, maker credit, at least one material
- [ ] I can save as draft before publishing
- [ ] Validation errors are shown next to the field

### US-09 · Edit or delete my craft
**Epic:** E2 · **Milestone:** M2 · **Priority:** Must · **Points:** 3

As a **maker**, I want to **edit or delete crafts I created**, so that **information stays accurate**.

**Acceptance criteria**
- [ ] Only the creator, a steward of that community, or an admin can edit
- [ ] Delete asks for confirmation
- [ ] "My crafts" page lists my drafts and published records

### US-10 · Names in multiple languages
**Epic:** E2 · **Milestone:** M4 · **Priority:** Should · **Points:** 3

As a **maker**, I want to **add the craft's name in my own language alongside other languages**, so that **the original name is preserved and shown first**.

**Acceptance criteria**
- [ ] Multiple (language, name) pairs per craft
- [ ] Indigenous-language name can be marked primary
- [ ] Full Unicode (diacritics, special orthography) renders and searches correctly

---

## E3 — Flexible attributes

### US-11 · Craft-type-specific fields in the form
**Epic:** E3 · **Milestone:** M2 · **Priority:** Must · **Points:** 8

As a **maker**, I want **the form to show fields that fit the craft type I choose** (e.g. firing method for pottery, loom type for weaving), so that **I can describe very different crafts properly**.

**Acceptance criteria**
- [ ] Changing the craft type updates the extra fields without losing core data
- [ ] Supports text, long text, number+unit, single/multi select, boolean, date/period, URL
- [ ] Values are validated against the craft type's definitions on the server
- [ ] At least 4 craft types have attribute definitions seeded

_Implementation: a `build_attribute_fields(craft_type)` helper maps each `AttributeDefinition` to a Django form field; HTMX swaps the fields when the type changes; values saved to `Craft.attributes` (JSONField)._

### US-12 · Show craft-specific attributes on the detail page
**Epic:** E3 · **Milestone:** M2 · **Priority:** Must · **Points:** 2

As a **visitor**, I want to **see the craft-specific details in a readable "Details" section**, so that **I understand what makes this piece distinctive**.

**Acceptance criteria**
- [ ] Labels and units come from the attribute definitions
- [ ] Empty attributes are hidden

### US-13 · Manage craft types and attributes
**Epic:** E3 · **Milestone:** M4 · **Priority:** Should · **Points:** 8

As an **admin**, I want to **create craft types and add, reorder or retire attribute fields in the UI**, so that **new traditions can be documented without a code change**.

**Acceptance criteria**
- [ ] Retiring a field hides it from forms but keeps existing data
- [ ] Changing a field's type is blocked if existing data would become invalid
- [ ] Changes are reflected in forms immediately

_Implementation: start from Django admin with an `AttributeDefinition` inline on `CraftType` (sortable); add validation in `ModelAdmin.save_model`._

### US-14 · Suggest a new craft type or attribute
**Epic:** E3 · **Milestone:** M5 · **Priority:** Could · **Points:** 3

As a **maker**, I want to **suggest a new craft type or field when mine is missing**, so that **the schema grows with real needs**.

**Acceptance criteria**
- [ ] Suggestion goes to the admin queue with my explanation
- [ ] I'm notified when it is accepted or declined

_Progress (FB-05, v0.4.5): makers can already type a new craft type under "Other"; it is added straight away and marked "added by" for review in the admin. Still to do: an explanation, an approve/decline queue and notifications._

---

## E4 — Discovery

### US-15 · Search crafts
**Epic:** E4 · **Milestone:** M3 · **Priority:** Must · **Points:** 5

As a **visitor**, I want to **search by keyword**, so that **I can find crafts by name, material, technique or community**.

**Acceptance criteria**
- [ ] Searches titles, all names, description, materials, techniques
- [ ] Restricted records never appear for unauthorized users
- [ ] Empty state suggests clearing filters

_Implementation: PostgreSQL full-text (`SearchVector` + `SearchRank`) with `TrigramSimilarity` for spelling variants; GIN indexes._

### US-16 · Filter and sort the catalogue
**Epic:** E4 · **Milestone:** M3 · **Priority:** Must · **Points:** 5

As a **visitor**, I want to **filter by craft type, community, region, material and technique, and sort results**, so that **I can narrow what I see**.

**Acceptance criteria**
- [ ] Filters combine (AND) and are reflected in the URL (shareable)
- [x] Pagination of 24 per page

_Progress: craft type, community and tag filters combine and are in the URL. Still to do: region, material and technique filters, and sorting._

_Implementation: `django-filter` FilterSet + Django `Paginator`; HTMX partial reload of results._

### US-17 · Community pages
**Epic:** E4 · **Milestone:** M3 · **Priority:** Should · **Points:** 3

As a **visitor**, I want to **see a page for each community with its self-description and crafts**, so that **I understand crafts in their cultural context**.

**Acceptance criteria**
- [ ] Community's own name is displayed first
- [ ] Description is editable by that community's stewards

_Progress: community links on craft pages open the catalogue filtered to that community; a page of its own is still to do._

### US-18 · Favourites and collections
**Epic:** E4 · **Milestone:** M4 · **Priority:** Could · **Points:** 5

As a **member**, I want to **favourite crafts and group them into named collections**, so that **I can return to them later**.

**Acceptance criteria**
- [ ] Collections are private by default
- [ ] Removing access to a craft also hides it from my collections

### US-19 · Filter by craft-specific attributes
**Epic:** E4 · **Milestone:** M4 · **Priority:** Could · **Points:** 5

As a **researcher**, I want to **filter by attributes of the chosen craft type** (e.g. "natural dyes only"), so that **I can compare techniques**.

**Acceptance criteria**
- [ ] Attribute filters appear once a single craft type is selected
- [ ] Only select/boolean/number attributes are filterable

---

## E5 — Media

### US-20 · Upload images with alt text and credit
**Epic:** E5 · **Milestone:** M2 · **Priority:** Must · **Points:** 5

As a **maker**, I want to **upload several photos, add alt text and a photo credit, and reorder them**, so that **the craft is shown well and accessibly**.

**Acceptance criteria**
- [ ] JPEG/PNG/WebP up to 10 MB; resized server-side or on upload
- [ ] Alt text is required before publishing
- [ ] First image is the cover in the catalogue

### US-21 · Sensitive image notice
**Epic:** E5 · **Milestone:** M4 · **Priority:** Should · **Points:** 2

As a **community steward**, I want to **mark images as culturally sensitive so they are blurred behind a notice**, so that **viewers choose whether to see them**.

**Acceptance criteria**
- [ ] Blurred until the viewer clicks "show"
- [ ] Notice text can be customised per record

---

## E6 — Cultural protocols

### US-22 · Set visibility of a craft
**Epic:** E6 · **Milestone:** M3 · **Priority:** Must · **Points:** 5

As a **maker or steward**, I want to **set a craft as Public, Members only, Community only or Restricted**, so that **knowledge is shared only as the community allows**.

**Acceptance criteria**
- [ ] Visibility is enforced in pages, search, API and image URLs via a single `Craft.objects.visible_to(user)` queryset method
- [x] Default for new records is "Members only" until reviewed
- [ ] Tests cover each visibility level for each role

_Progress: Public and Members only work through `Craft.objects.visible_to(user)` on every page, with tests; drafts are visible only to their author. Still to do: Community only and Restricted (need roles, US-05)._

### US-23 · Record consent
**Epic:** E6 · **Milestone:** M3 · **Priority:** Must · **Points:** 3

As a **contributor**, I want to **record who gave permission to document the craft, when and for what use**, so that **publishing is accountable**.

**Acceptance criteria**
- [ ] Cannot submit for publishing without a consent record
- [ ] Consent details visible to stewards and admins only

### US-24 · Steward review queue
**Epic:** E6 · **Milestone:** M3 · **Priority:** Must · **Points:** 5

As a **community steward**, I want to **review crafts attributed to my community before they go public**, so that **my community controls how it is represented**.

**Acceptance criteria**
- [ ] Queue lists pending records for my communities only
- [ ] Approve, request changes (with comment), or reject
- [ ] Contributor is notified of the decision

### US-25 · Report a record / request removal
**Epic:** E6 · **Milestone:** M3 · **Priority:** Must · **Points:** 3

As **anyone**, I want to **report inaccurate or inappropriate content or request removal**, so that **mistakes and harms can be corrected quickly**.

**Acceptance criteria**
- [ ] Report form available on every craft page (no login required)
- [ ] Reports appear in the steward/admin queue
- [ ] A steward or admin can unpublish immediately

_Progress: every craft page has a "Report or request removal" link that opens a pre-filled GitHub issue. Still to do: an on-site form and queue._

### US-26 · Traditional Knowledge labels
**Epic:** E6 · **Milestone:** M4 · **Priority:** Should · **Points:** 3

As a **community steward**, I want to **attach TK/BC labels (e.g. Local Contexts) to a craft**, so that **viewers understand the cultural conditions of use**.

**Acceptance criteria**
- [ ] Labels show with icon, name and explanation on the detail page
- [ ] Labels are selectable from a managed list

---

## E7 — Administration

### US-27 · Manage users
**Epic:** E7 · **Milestone:** M3 · **Priority:** Must · **Points:** 3

As an **admin**, I want to **search users, change roles, assign stewards to communities and suspend accounts**, so that **the platform stays safe**.

**Acceptance criteria**
- [ ] Suspended users cannot log in
- [ ] Role changes are logged

### US-28 · Manage taxonomies
**Epic:** E7 · **Milestone:** M4 · **Priority:** Should · **Points:** 3

As an **admin**, I want to **manage communities, regions, materials and techniques**, so that **records use consistent terms**.

**Acceptance criteria**
- [ ] Merge duplicate terms without losing links to crafts
- [ ] Terms can have alternate spellings used by search

---

## E8 — Quality

### US-29 · Accessible site
**Epic:** E8 · **Milestone:** M4 · **Priority:** Must · **Points:** 5

As a **visitor using assistive technology**, I want **the site to be keyboard and screen-reader friendly**, so that **I can use it fully**.

**Acceptance criteria**
- [ ] Automated axe checks pass in CI on key pages (`axe-playwright-python`)
- [ ] Manual keyboard walkthrough of all core flows documented
- [ ] Colour contrast meets WCAG AA

### US-30 · Security and privacy hardening
**Epic:** E8 · **Milestone:** M5 · **Priority:** Must · **Points:** 5

As a **user**, I want **my account and restricted community content to be protected**, so that **I can trust the platform**.

**Acceptance criteria**
- [ ] OWASP Top 10 checklist reviewed and findings fixed; `pip-audit` and `bandit` run in CI
- [ ] Rate limiting on login, register and report endpoints (`django-axes` / `django-ratelimit`)
- [ ] Users can delete their account and personal data

### US-31 · Fast on mobile
**Epic:** E8 · **Milestone:** M5 · **Priority:** Should · **Points:** 3

As a **visitor on a slow connection**, I want **pages to load quickly**, so that **I can browse in rural or low-bandwidth areas**.

**Acceptance criteria**
- [ ] Lighthouse performance ≥ 85 on catalogue and detail pages (mobile)
- [ ] Images lazy-loaded and served in modern formats

### US-32 · Final documentation and handover
**Epic:** E8 · **Milestone:** M5 · **Priority:** Must · **Points:** 3

As a **future maintainer**, I want **setup, architecture, data model and content-governance docs**, so that **the project can continue after week 10**.

**Acceptance criteria**
- [ ] README, architecture overview, ADRs, data model diagram, steward guide
- [ ] Final demo recorded and linked from the v1.0 release

---

## Feedback items

Feedback from reviews and demos, delivered as extra items. Each has a closed issue with the `feedback` label.

| ID | Issue | Feedback | Delivered |
|---|---|---|---|
| FB-01 | [#68](https://github.com/bakalit01/SWE573-2025719006/issues/68) | Region should be a geolocation: map pin, place search, place name and country, location precision for sensitive places | v0.4.0 · 25 Oct |
| FB-02 | [#69](https://github.com/bakalit01/SWE573-2025719006/issues/69) | More detail on materials and techniques: where each material comes from, how it is used, how techniques are applied, "How it is made" | v0.4.0 · 25 Oct |
| FB-03 | [#70](https://github.com/bakalit01/SWE573-2025719006/issues/70) | "Made" details: made by, made from (materials summary), made in (year, circa, or period) | v0.4.0 · 25 Oct |
| FB-04 | [#71](https://github.com/bakalit01/SWE573-2025719006/issues/71) | 3D size and units from different countries: H × W × D in mm/cm/m/in/ft, weight in g/kg/oz/lb, converted values, local measure | v0.4.0 · 25 Oct |
| FB-05 | [#77](https://github.com/bakalit01/SWE573-2025719006/issues/77) | "Other (type your own)" for craft type, community, units and choice fields; own details; user tags | v0.4.5 · 26 Oct |
| FB-06 | [#80](https://github.com/bakalit01/SWE573-2025719006/issues/80) | Real-life examples instead of abstract samples: 9 real crafts from public sources with credited photos | v0.4.2–v0.4.3 · 26 Oct |
| FB-09 | [#90](https://github.com/bakalit01/SWE573-2025719006/issues/90) | Crafts from East Asia: Miao silver headdress and Li brocade (China), Atayal weaving (Taiwan), Hahoe masks (Korea), Ryukyuan bingata (Japan) | v0.4.9 · 26 Oct |
| FB-08 | [#88](https://github.com/bakalit01/SWE573-2025719006/issues/88) | Eight more real crafts, four from Türkiye: Yörük kilim, Yörük black tent, Döşemealtı carpet, Midyat telkari; plus Ainu attus, Guna mola, Wayuu mochila, Shipibo-Conibo pottery | v0.4.8 · 26 Oct |
| FB-07 | [#81](https://github.com/bakalit01/SWE573-2025719006/issues/81) | Blue tones based on Boğaziçi University colours (navy #1e4a8b, blue #8cc8ea) | v0.4.4 · 26 Oct |

Bug fixed alongside: [#79](https://github.com/bakalit01/SWE573-2025719006/issues/79) maps and place search failed on the deployed site (v0.4.1).
