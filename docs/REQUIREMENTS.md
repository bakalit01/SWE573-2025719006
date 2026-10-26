# Requirements — Indigenous Crafts Platform

Version 0.2 · 26 Oct 2026 · Status: updated after M2 and feedback FB-01–FB-07 (✅ = delivered)

## 1. Purpose & scope

The platform documents, preserves and showcases Indigenous crafts. It lets registered contributors record crafts with attributes appropriate to each craft tradition, credits makers and communities, and respects cultural protocols about what may be shared and with whom.

**In scope:** public catalogue, accounts & roles, craft records with flexible attributes, media, search/filter, cultural protocols (consent, visibility, TK labels), moderation, admin taxonomy management.
**Out of scope (v1):** e-commerce/payments, native mobile apps, real-time chat, federated login with community identity systems.

## 2. Users & roles

| Role | Description | Key permissions |
|---|---|---|
| Visitor | Not signed in | View public crafts, search, view maker/community pages |
| Member | Registered user | Everything a visitor can + favourites/collections, view members-only crafts |
| Maker / Contributor | Artisan or documenter | Create/edit own craft records, manage own profile |
| Community Steward | Trusted representative of a community | Approve/reject records attributed to their community, set restrictions, request takedown |
| Admin | Platform operator | Manage users/roles, craft types & attribute schemas, taxonomies, moderation |

## 3. Functional requirements

Priority uses MoSCoW. Milestone: M1 Demo (delivered 13 Oct), M2 (delivered 25 Oct), M3 MVP (wk 4), M4 (wk 6), M5 Final (wk 8); weeks 9–10 buffer. ✅ marks delivered requirements.

### 3.1 Accounts & authentication
| ID | Requirement | Priority | Milestone |
|---|---|---|---|
| FR-A1 | Users can register with email + password | Must | M1 ✅ |
| FR-A2 | Users can log in and log out; sessions persist securely | Must | M1 ✅ |
| FR-A3 | Users can reset a forgotten password via email | Should | M2 ✅ |
| FR-A4 | Role-based access control (member, maker, steward, admin) | Must | M3 |
| FR-A5 | Users can edit their profile (display name, bio, community affiliation, photo) | Should | M2 ✅ (photo later) |
| FR-A6 | Optional social login (Google) | Could | M4 |
| FR-A7 | Users can delete their account and personal data | Should | M5 |

### 3.2 Craft records
| ID | Requirement | Priority | Milestone |
|---|---|---|---|
| FR-C1 | View a list of crafts and a craft detail page | Must | M1 ✅ |
| FR-C2 | Makers can create, edit and delete their own craft records | Must | M2 ✅ |
| FR-C3 | Each craft has core fields (see §4.1) | Must | M2 ✅ |
| FR-C4 | Each craft belongs to a craft type that determines additional attributes | Must | M2 ✅ |
| FR-C5 | Craft-specific attributes are rendered dynamically in forms and detail pages | Must | M2 ✅ |
| FR-C6 | Attributes support types: text, long text, number+unit, single select, multi select, boolean, date/period, URL | Must | M2 ✅ |
| FR-C7 | Upload multiple images per craft with alt text and credit/caption | Must | M2 ✅ |
| FR-C8 | Records keep an edit history (who/when) | Could | M5 |
| FR-C9 | Crafts can have multiple names in different languages (incl. Indigenous language name) | Should | M4 |
| FR-C10 | Where a list doesn't fit, users choose "Other (type your own)": craft type, community, size and weight units, and choice fields; typed craft types and communities are added and marked for review (FB-05) | Should | M2 ✅ |
| FR-C11 | Users add their own details (any label + value) and their own tags; tags link to the crafts that share them (FB-05) | Should | M2 ✅ |
| FR-C12 | Place recorded as a geolocation (map pin, place, country) with exact / approximate / hidden precision (FB-01) | Must | M2 ✅ |

### 3.3 Discovery
| ID | Requirement | Priority | Milestone |
|---|---|---|---|
| FR-D1 | Keyword search across names, descriptions, materials, techniques | Must | M3 |
| FR-D2 | Filter by craft type, community/nation, region, material, technique, tag | Must | M3 (type, community, tag ✅) |
| FR-D3 | Filter by craft-type-specific attributes | Could | M4 |
| FR-D4 | Pagination and sorting | Must | M3 |
| FR-D5 | Maker and community pages listing related crafts | Should | M3 |
| FR-D6 | Members can favourite crafts and build named collections | Could | M4 |
| FR-D7 | Map view by region (each craft page already shows its own map) | Won't (v1) / stretch | M5 |

### 3.4 Cultural protocols & governance
| ID | Requirement | Priority | Milestone |
|---|---|---|---|
| FR-P1 | Each record has a visibility level: Public, Members only, Community only, Restricted (steward/admin only) | Must | M3 |
| FR-P2 | Contributors record consent (who gave permission, date, scope) before publishing | Must | M3 |
| FR-P3 | Records attributed to a community enter a moderation queue for steward review before going public | Must | M3 |
| FR-P4 | Records can carry Traditional Knowledge / Biocultural labels (e.g. Local Contexts TK labels) shown on the detail page | Should | M4 |
| FR-P5 | Anyone can report a record; stewards/admins can unpublish within the workflow | Must | M3 |
| FR-P6 | Makers and communities are always credited; credit fields cannot be blank on published records | Must | M2 ✅ |
| FR-P7 | Sacred/sensitive images can be hidden behind a content notice | Should | M4 |

### 3.5 Administration
| ID | Requirement | Priority | Milestone |
|---|---|---|---|
| FR-M1 | Admins manage craft types and their attribute definitions without code changes | Should | M4 |
| FR-M2 | Admins manage taxonomies: communities/nations, regions, materials, techniques | Should | M4 |
| FR-M3 | Admins manage users and roles | Must | M3 |
| FR-M4 | Audit log of moderation actions | Could | M5 |

## 4. Data model (draft)

### 4.1 Core entities
- **User** — id, email, password hash, display name, bio, avatar, role(s), community affiliations, created_at
- **Community** — id, name(s) (self-designated name first), region, description, steward users, added_by (set when a user typed it under "Other")
- **Craft** — id, slug, title, names[] (lang, text), summary, description, process (how it is made), craft_type_id, community_id, maker credit (made by), year made + circa flag or period (made in), **place name, country, latitude, longitude, location precision (exact / approximate / hidden)**, **height × width × depth + length unit (or a typed unit), weight + weight unit (or a typed unit), local/traditional measure**, materials[] and techniques[] (via CraftMaterial: origin, notes; CraftTechnique: notes), cultural_context, **attributes (JSONB)**, extra_details (the contributor's own label/value pairs), tags[], sources and is_reference (real examples from public sources), visibility, status (draft / pending review / published / unpublished), consent_id, tk_labels[], created_by, timestamps
- **CraftType** — id, name (Textile, Pottery, Beadwork, Basketry, Carving, Metalwork, Leatherwork, Jewellery, …), description, attribute definitions, added_by (set when a user typed it under "Other")
- **AttributeDefinition** — id, craft_type_id, key, label, data type, unit, options[], required, help text, order
- **Media** — id, craft_id, url, alt_text, caption, credit, is_sensitive, order
- **Consent** — id, craft_id, granted_by (name/role), date, scope, notes, document (optional)
- **Material / Technique** — controlled vocabularies with a short description; linked to crafts through CraftMaterial / CraftTechnique, which hold per-craft detail
- **Units** — lengths mm, cm, m, in, ft; weights g, kg, oz, lb; values shown as entered plus a converted metric/imperial value. Any other unit can be typed; it is shown as typed, without conversion
- **Tag** — name, slug; free keywords added by contributors, shared across crafts
- **Favourite / Collection** — user_id, craft_id(s)
- **Report / ModerationAction** — who, what, reason, status, timestamps

### 4.2 Handling diverse attributes
Crafts share a **core** (title, community, makers, materials, techniques, images, consent) but differ strongly in specifics. Approach:

1. **Core fields** are proper columns — searchable and consistent across all crafts.
2. **Craft-specific fields** live in `Craft.attributes` (a Django `JSONField`, stored as `jsonb` in PostgreSQL) and are **validated against the craft type's `AttributeDefinition`s** in the model/form `clean()` at save time.
3. Django forms and detail templates are **generated at runtime from the definitions** (each definition maps to a form field class: `CharField`, `DecimalField`, `ChoiceField`, `MultipleChoiceField`, `BooleanField`, `DateField`, `URLField`), so adding "Glass beads: size (mm)" or "Pottery: firing method" requires no deployment.
4. Common filterable attributes get a GIN index on the JSONB column.
5. **Nothing is forced into a list.** Every choice field also offers "Other (type your own)", contributors can add their own label/value details, and tags capture anything else. New craft types typed by users start with no set fields; admins can later turn recurring "own details" into proper attribute definitions.

Example attribute schemas:

| Craft type | Example attributes |
|---|---|
| Textile / weaving | loom type, fibre, dye source (natural/synthetic), dye plants, weave structure, thread count |
| Pottery | clay source, temper, forming method (coil/pinch/wheel), firing method, slip/paint, vessel form |
| Beadwork | bead material, bead size, stitch technique, backing material, motif |
| Basketry | plant materials, harvest season, weave (coil/twine/plait), watertight (yes/no) |
| Carving | material (wood species, stone, bone), tools, finish, ceremonial use (restricted flag) |
| Jewellery / metalwork | metal, stones, technique (repoussé, filigree, casting), hallmark |

## 5. Non-functional requirements

| ID | Category | Requirement |
|---|---|---|
| NFR-1 | Accessibility | WCAG 2.1 AA; keyboard navigable; alt text required on images |
| NFR-2 | Security | Passwords hashed with Argon2 (Django `Argon2PasswordHasher`); HTTPS; Django CSRF middleware on; authorization enforced server-side; `manage.py check --deploy` passes; OWASP Top 10 reviewed |
| NFR-3 | Privacy | Minimal personal data; GDPR/KVKK-aware; account deletion; restricted content never exposed via API or search to unauthorized users |
| NFR-4 | Performance | Catalogue page LCP < 2.5 s on 4G; images resized and lazy-loaded |
| NFR-5 | Reliability | Daily DB backups; preview deploy per PR; production deploy from `main` only |
| NFR-6 | Quality | `pytest` unit/integration + Playwright (Python) e2e tests in CI; `ruff` clean; ≥ 60 % coverage on core logic by M5 |
| NFR-10 | Technology | Python 3.12+, Django 5.2 LTS, PostgreSQL 16; no separate JavaScript framework (small plain-JavaScript enhancements; pages work without them) |
| NFR-7 | i18n | UI strings externalized; Unicode-safe for Indigenous language orthographies |
| NFR-8 | Maintainability | README, setup guide, ADRs, documented data model |
| NFR-9 | Responsiveness | Usable on 360 px wide phones up to desktop |

## 6. Ethics & cultural guidelines
- Follow the **CARE Principles for Indigenous Data Governance** (Collective benefit, Authority to control, Responsibility, Ethics).
- Use communities' own names and spellings; let communities correct them.
- Until community partners contribute their own records, the site shows **reference records**: publicly documented, non-restricted crafts summarised from museum and encyclopedia sources, with openly licensed photos credited to their authors, a Sources section, and an invitation to the community to correct or remove them. Sacred or restricted items are excluded.
- Other demo data is clearly marked as sample.
- Provide a visible takedown/contact route on every craft page.

## 7. Open questions
1. Who are the community partners/advisors, and who acts as steward during development?
2. Is there a preferred hosting region or data-residency requirement?
3. Which languages must the UI support at launch?
4. Will sales/links to makers' shops be needed later?
5. ~~Final stack choice~~ Decided: Python / Django + PostgreSQL, hosted on Render (`render.yaml`). Still open: long-term image storage (uploads currently reset on Render redeploys; R2 vs Supabase).
