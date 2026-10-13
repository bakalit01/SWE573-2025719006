# SWE573-2025719006: Indigenous Crafts Platform

A website to document and showcase Indigenous crafts. Registered users can record crafts with attributes specific to each craft type (textiles, pottery, beadwork, basketry, carving, …). Makers and communities are credited, and community cultural protocols are respected: consent, visibility levels and steward review.

| | |
|---|---|
| **Author** | Ege Güçlü Asan |
| **Course** | SWE 573, 2026/2027-1, Suzan Üsküdarlı |
| **Stack** | Python 3.12 · Django 5.2 LTS · PostgreSQL 16 · HTMX + Tailwind · pytest ([ADR-001](docs/adr/001-tech-stack.md)) |
| **Timeline** | 12 Oct – 20 Dec 2026 |

## Project status
Week 1: requirements, user stories and backlog are done; repository and CI setup is in progress.

| Milestone | Due | Deliverable |
|---|---|---|
| [M1 – Running demo](https://github.com/bakalit01/SWE573-2025719006/milestone/2) | 25 Oct (week 2) | Deployed site: browse crafts, craft page, sign up / log in |
| [M2 – Contribute](https://github.com/bakalit01/SWE573-2025719006/milestone/3) | 8 Nov (week 4) | Add/edit crafts with photos, craft-type-specific fields, profiles |
| [M3 – MVP](https://github.com/bakalit01/SWE573-2025719006/milestone/4) | 22 Nov (week 6) | Search & filter, roles, visibility & consent, steward review |
| [M4 – Enrich](https://github.com/bakalit01/SWE573-2025719006/milestone/5) | 6 Dec (week 8) | Admin-managed attributes, TK labels, multilingual names, accessibility |
| [M5 – Final product](https://github.com/bakalit01/SWE573-2025719006/milestone/6) | 20 Dec (week 10) | Hardened, documented, tested v1.0 |

## Documentation
| Document | Contents |
|---|---|
| [Project plan](docs/PROJECT_PLAN.md) | Milestones, week-by-week plan, **story sequence** (§3a), tech stack, workflow, risks |
| [Requirements](docs/REQUIREMENTS.md) | Roles, functional & non-functional requirements, data model, ethics |
| [User stories](docs/USER_STORIES.md) | 32 user stories + 8 technical tasks with acceptance criteria and delivery order |
| [ADR-001 Tech stack](docs/adr/001-tech-stack.md) | Why Python / Django |
| [Issues](https://github.com/bakalit01/SWE573-2025719006/issues) | One issue per story/task (#24–#63); [Roadmap #65](https://github.com/bakalit01/SWE573-2025719006/issues/65) is the weekly checklist |

## Getting started
The Django project is scaffolded in week 1 (issue [#26](https://github.com/bakalit01/SWE573-2025719006/issues/26)). Setup instructions will follow here.

## Working on the backlog
- Branch per issue (`us-11-dynamic-fields`), PR with `Closes #n`, CI must pass.
- Edit stories in `docs/USER_STORIES.md`. Then **Actions → Seed backlog issues → Run workflow** creates any new ones.
