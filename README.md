# SWE573-2025719006: Indigenous Crafts Platform

A website to document and showcase Indigenous crafts. Registered users can record crafts with attributes specific to each craft type (textiles, pottery, beadwork, basketry, carving, …). Makers and communities are credited, and community cultural protocols are respected: consent, visibility levels and steward review.

| | |
|---|---|
| **Author** | Ege Güçlü Asan |
| **Course** | SWE 573, 2026/2027-1, Suzan Üsküdarlı |
| **Stack** | Python 3.12 · Django 5.2 LTS · PostgreSQL 16 · server-rendered templates · pytest + Playwright ([ADR-001](docs/adr/001-tech-stack.md)) |
| **Timeline** | 12 Oct – 6 Dec 2026 (feature-complete), buffer to 20 Dec |

## Project status
**M1 running demo delivered on 13 Oct 2026 (week 1, ahead of plan): [release v0.2.0](https://github.com/bakalit01/SWE573-2025719006/releases/tag/v0.2.0).** The timeline was pulled forward by two weeks.

| Milestone | Due | Deliverable |
|---|---|---|
| [M1 – Running demo](https://github.com/bakalit01/SWE573-2025719006/milestone/2) | ✅ 13 Oct (week 1) | Browse sample crafts, craft page, sign up / log in / log out |
| [M2 – Contribute](https://github.com/bakalit01/SWE573-2025719006/milestone/3) | 25 Oct (week 2) | Add/edit crafts with photos, craft-type-specific fields, profiles |
| [M3 – MVP](https://github.com/bakalit01/SWE573-2025719006/milestone/4) | 8 Nov (week 4) | Search & filter, roles, visibility & consent, steward review |
| [M4 – Enrich](https://github.com/bakalit01/SWE573-2025719006/milestone/5) | 22 Nov (week 6) | Admin-managed attributes, TK labels, multilingual names, accessibility |
| [M5 – Final product](https://github.com/bakalit01/SWE573-2025719006/milestone/6) | 6 Dec (week 8) | Hardened, documented, tested v1.0 |
| Buffer | 7–20 Dec (weeks 9–10) | Feedback, polish, stretch goals, final presentation |

![Craft detail page](docs/design/screenshots/03-craft-detail.png)

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
uv run python manage.py seed_sample_data      # 12 fictional sample crafts
uv run python manage.py createsuperuser       # for /admin/
uv run python manage.py runserver             # → http://localhost:8000
```

**Tests:** `uv run pytest` (unit + integration). For the browser tests, first run `uv run playwright install chromium`.

**Deploy (Render, free tier):** in Render choose **New → Blueprint**, then pick this repository. `render.yaml` creates the web service and the PostgreSQL database, then runs migrations and loads the sample data on start.

### Demo script (M1)
1. Open the home page, then **Browse crafts**. A visitor sees 10 public sample crafts.
2. Filter by **Pottery** and open a craft. It shows credits, materials, *Pottery details* (fields specific to the craft type) and a report link.
3. **Sign up** with a password under 10 characters to show the validation message. Then sign up properly: you are signed in and your name appears in the header.
4. **Browse crafts** again. Members now see 12 crafts, including the members-only ones.
5. **Log out**, then log in with a wrong password to show the generic error message.

## Working on the backlog
- Branch per issue (`us-11-dynamic-fields`), PR with `Closes #n`, CI must pass.
- Edit stories in `docs/USER_STORIES.md`. Then **Actions → Seed backlog issues → Run workflow** creates any new ones.
