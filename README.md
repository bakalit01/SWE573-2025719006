# SWE573-2025719006: Indigenous Crafts Platform

A website to document and showcase Indigenous crafts. Registered users can record crafts with attributes specific to each craft type (textiles, pottery, beadwork, basketry, carving, …). Makers and communities are credited, and community cultural protocols are respected: consent, visibility levels and steward review.

| | |
|---|---|
| **Author** | Ege Güçlü Asan |
| **Course** | SWE 573, 2026/2027-1, Suzan Üsküdarlı |
| **Stack** | Python 3.12 · Django 5.2 LTS · PostgreSQL 16 · server-rendered templates · pytest + Playwright ([ADR-001](docs/adr/001-tech-stack.md)) |
| **Timeline** | 12 Oct – 6 Dec 2026 (feature-complete), buffer to 20 Dec |

## Project status
**M2 Contribute delivered on 25 Oct 2026: [release v0.4.0](https://github.com/bakalit01/SWE573-2025719006/releases/tag/v0.4.0).** Signed-in users can add, edit and delete crafts with photos, a map location, detailed materials and techniques, and sizes in their own units. (M1 running demo: 13 Oct, v0.2.0.)

| Milestone | Due | Deliverable |
|---|---|---|
| [M1 – Running demo](https://github.com/bakalit01/SWE573-2025719006/milestone/2) | ✅ 13 Oct (week 1) | Browse sample crafts, craft page, sign up / log in / log out |
| [M2 – Contribute](https://github.com/bakalit01/SWE573-2025719006/milestone/3) | ✅ 25 Oct (week 2) | Add/edit crafts with photos, craft-type-specific fields, profiles |
| [M3 – MVP](https://github.com/bakalit01/SWE573-2025719006/milestone/4) | 8 Nov (week 4) | Search & filter, roles, visibility & consent, steward review |
| [M4 – Enrich](https://github.com/bakalit01/SWE573-2025719006/milestone/5) | 22 Nov (week 6) | Admin-managed attributes, TK labels, multilingual names, accessibility |
| [M5 – Final product](https://github.com/bakalit01/SWE573-2025719006/milestone/6) | 6 Dec (week 8) | Hardened, documented, tested v1.0 |
| Buffer | 7–20 Dec (weeks 9–10) | Feedback, polish, stretch goals, final presentation |

![Craft page](docs/design/screenshots/09-craft-page-m2.png)

## Documentation
| Document | Contents |
|---|---|
| [Project plan](docs/PROJECT_PLAN.md) | Milestones, week-by-week plan, **story sequence** (§3a), tech stack, workflow, risks |
| [Requirements](docs/REQUIREMENTS.md) | Roles, functional & non-functional requirements, data model, ethics |
| [User stories](docs/USER_STORIES.md) | 32 user stories + 8 technical tasks with acceptance criteria and delivery order |
| [ADR-001 Tech stack](docs/adr/001-tech-stack.md) | Why Python / Django, hosting on Render |
| [UI design](docs/design/README.md) | Screenshots of every page (desktop and phone) |
| [Changelog](CHANGELOG.md) | What changed in each release |
| [Issues](https://github.com/bakalit01/SWE573-2025719006/issues) | One issue per story/task (#24–#63); [Roadmap #65](https://github.com/bakalit01/SWE573-2025719006/issues/65) is the weekly checklist |

## Getting started

**Requirements:** Python 3.12+, [uv](https://docs.astral.sh/uv/), PostgreSQL 16 (or Docker).

```bash
# Option A: Docker (app + database)
docker compose up --build            # → http://localhost:8000

# Option B: local Python
cp .env.example .env                 # edit DATABASE_URL if needed
uv sync --all-groups
uv run python manage.py migrate
uv run python manage.py seed_reference_crafts  # 9 real examples from public sources
uv run python manage.py seed_sample_data --fictional  # optional: fictional samples used by tests
uv run python manage.py createsuperuser       # for /admin/
uv run python manage.py runserver             # → http://localhost:8000
```

**Tests:** `uv run pytest` (unit + integration). For the browser tests, first run `uv run playwright install chromium`.

**Deploy (Render, free tier):** in Render choose **New → Blueprint**, then pick this repository. `render.yaml` creates the web service and the PostgreSQL database, then runs migrations and loads the sample data on start.

### Demo script (M2)
1. **Browse crafts**, then open a real example (e.g. the Pomo basket by Jenny Hughes). Show the "At a glance" card (made by / from / in, size with its converted value, weight, local measure) and the Materials and Techniques sections.
2. **Sign up** (password ≥ 10 characters), then open **Add a craft**.
3. Pick a **craft type**: its own fields appear under "Craft details". Search a place or click the map to drop a pin; the place name fills in. Add two materials with origins, a technique, a size in inches or cm, and a photo with alt text.
4. **Publish**. The craft page shows everything, with the size converted. Click **Edit**, change the year, then **Save as draft**: the record is now visible only to you (**My crafts**).
5. Open your name in the header to see your **maker profile**; **Edit profile** to add a bio and community.
6. Log out, then use **Forgot your password?** on the login page. The reset email appears in the server console in development.

**Adding crafts as an admin:** `/admin/` → Crafts. Materials, techniques and photos are inline rows.

## Working on the backlog
- Branch per issue (`us-11-dynamic-fields`), PR with `Closes #n`, CI must pass.
- Edit stories in `docs/USER_STORIES.md`. Then **Actions → Seed backlog issues → Run workflow** creates any new ones.
