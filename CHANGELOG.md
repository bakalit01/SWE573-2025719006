# Changelog

All notable changes per release. Releases are tagged on GitHub (`vX.Y.Z`).

## [v0.2.0] – 13 Oct 2026 · M1 Running demo
### Added
- Django 5.2 project (`accounts`, `communities`, `crafts` apps) with split dev/test/prod settings and a custom email-login user model (#26).
- Data model: communities, craft types with per-type attribute definitions, crafts with JSON attributes, media, materials, techniques (#28).
- `seed_sample_data` command: 12 clearly labelled fictional crafts across 6 craft types and 4 sample communities (#28).
- Sign up with email + password (≥ 10 characters, Argon2-hashed), duplicate-email error (#32).
- Log in with a generic error message, name shown in header, CSRF-protected logout (#33).
- Craft catalogue with type/community filters and pagination of 24 (#37).
- Craft detail page: credits, materials, techniques, craft-type details, cultural context, report/removal link (#38).
- Visibility rules in one place (`Craft.objects.visible_to`): visitors see public crafts, members also see members-only crafts, and hidden records return 404.
- Test suite: 31 tests (unit, integration, Playwright end-to-end, phone layout), 93 % coverage (#29).
- CI: ruff, Django checks, migration check, deploy check, tests with coverage ≥ 80 %, dependency audit (#27).
- Deployment: Dockerfile, docker-compose, Render Blueprint (`render.yaml`), `/healthz` (#26).
- UI screenshots as the design reference in `docs/design/` (#30).

## [v0.1.0] – 13 Oct 2026 · Planning
### Added
- Project plan, requirements, 32 user stories + 8 tasks, ADR-001 (Python/Django), issue and PR templates, issue-seeding workflow (#64).
