# Changelog

All notable changes per release. Releases are tagged on GitHub (`vX.Y.Z`).

## [v0.4.0] – 25 Oct 2026 · M2 Contribute
### Added
- **Add a craft** page for signed-in users, in nine sections: basics, made, place, materials & techniques, size & weight, craft details, photos, story, sharing (#39).
- **Craft-type-specific fields** load as soon as a craft type is chosen and are validated on the server (#42, #43).
- **Photos**: several per craft, required alt text, credit and caption, resized to 1600 px; thumbnails on the craft page (#51).
- **Edit, delete and My crafts**: drafts are visible only to their author; only the author or staff can edit or delete (#40).
- **Place as geolocation**: address search and click-to-pin map (OpenStreetMap), place name and country filled in automatically, and an exact, approximate or hidden precision setting for sensitive places (#68).
- **Materials and techniques in detail**: where each material comes from, how it is used, how each technique is applied, and a "How it is made" section (#69).
- **Made summary**: "Made by", "Made from" (materials) and "Made in" (year, with circa, or a period) in an "At a glance" card (#70).
- **Size in 3D with international units**: height × width × depth in mm, cm, m, in or ft; weight in g, kg, oz or lb; converted values shown; free-text local or traditional measure (#71).
- **Maker profiles** with display name, bio, community and location; "Added by" links on craft pages (#35).
- **Password reset by email** with the same response whether or not the email has an account (#34).
- Unsaved add-form text is kept in the browser and restored on return.
- Tests: 69 (unit, integration, browser), 91 % coverage.

### Changed
- Craft page redesigned: gallery, "At a glance" facts card, location map, materials and techniques sections. On phones the facts follow the photo.
- Free-text "region" replaced by place name, country and coordinates (existing values kept as the place name).

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
- Release workflow: publishing a version in this file creates the GitHub release and tag (#31).

## [v0.1.0] – 13 Oct 2026 · Planning
### Added
- Project plan, requirements, 32 user stories + 8 tasks, ADR-001 (Python/Django), issue and PR templates, issue-seeding workflow (#64).
