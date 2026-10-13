# Indigenous Crafts Platform: project docs

A website to document and showcase Indigenous crafts, with accounts, craft-specific attributes, and cultural protocols (consent, visibility, community review).

**Stack:** Python 3.12 · Django 5.2 LTS · PostgreSQL 16 · HTMX + Tailwind · pytest · see [ADR-001](adr/001-tech-stack.md)

**Timeline:** 12 Oct – 20 Dec 2026 · Demo end of week 2 · MVP end of week 6 · Final end of week 10

## Docs
- [Project plan](PROJECT_PLAN.md) — milestones, week-by-week, stack, workflow, risks
- [Requirements](REQUIREMENTS.md) — roles, functional & non-functional requirements, data model
- [User stories](USER_STORIES.md) — backlog; source of truth for GitHub issues
- [ADR-001 Tech stack](adr/001-tech-stack.md)

## Seed GitHub issues
**From GitHub:** open **Actions → Seed backlog issues → Run workflow**. It creates any missing labels, the 5 milestones and any missing issues using the repo's own token (already run once on 13 Oct 2026: issues #24–#63).

**Or from your machine:**
```bash
gh auth login
python3 scripts/seed_github.py --repo OWNER/REPO --dry-run   # preview
python3 scripts/seed_github.py --repo OWNER/REPO             # create missing labels, milestones and issues
```
Then create a Project board (Backlog → Ready → In progress → In review → Done) and add the issues.
