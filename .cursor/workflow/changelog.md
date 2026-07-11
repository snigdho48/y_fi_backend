# Changelog

All changes to `y_fi_backend` must be logged here newest-first.

**Format:** `## YYYY-MM-DD HH:MM (UTC+6) — Title` with `**Time:**` field in every entry.

---

## 2026-07-09 13:15 (UTC+6) — Theme system moved to dashboard-backend

**Time:** 2026-07-09 13:15 (UTC+6)  
**Author:** Cursor AI agent  
**Type:** Refactor

### Removed
- `AppThemeConfig` model, `api/view/theme.py`, `api/theme_serializers.py`
- `POST /api/auth/admin/login/` and all `/api/admin/theme/*`, `GET /api/theme/`

### API impact
- Theme + dashboard admin login now served by `dashboard-backend` only

---

## 2026-07-09 12:28 (UTC+6) — Theme default fallback when none active

**Time:** 2026-07-09 12:28 (UTC+6)  
**Author:** Cursor AI agent  
**Type:** Enhancement

### Changed
- `api/view/theme.py` — `_default_theme_for_app()` when no `is_active` theme; deactivate-only delete message

### API impact
- `GET /api/theme/?app=` returns built-in default palette when no saved theme is active

---

## 2026-07-09 11:30 (UTC+6) — Remote theme system (API + admin panel support)

**Time:** 2026-07-09 11:30 (UTC+6)  
**Author:** Cursor AI agent  
**Type:** Feature

### Added
- `AppThemeConfig` model — palette, font, per-section JSON styles, `app_target` (user/partner)
- Migration `0004_appthemeconfig.py`
- `api/theme_serializers.py` — hex validation, public + admin serializers
- `api/view/theme.py` — public GET `/theme/`, admin CRUD + activate + defaults
- `POST /auth/admin/login/` — admin-group JWT login for Theme Studio
- Django admin registration for `AppThemeConfig`

### Changed
- `api/models.py`, `api/serializer.py`, `api/urls.py`, `api/views.py`, `api/admin.py`, `api/view/auth.py`

### API impact
- New: `GET /api/theme/?app=user|partner` (public)
- New: `GET|POST /api/admin/theme/`, `GET|PATCH|DELETE /api/admin/theme/<id>/`, `POST .../activate/`, `GET .../defaults/`
- New: `POST /api/auth/admin/login/`

### DB impact
- Migration `0004_appthemeconfig` — `AppThemeConfig` table

---

**Time:** 2026-07-09 11:23 (UTC+6)  
**Author:** Cursor AI agent  
**Type:** Documentation

### Changed
- `.cursor/rules/auto-changelog.mdc` — new always-on rule: auto-update changelog on every file change
- `.cursor/rules/freeyfi-backend.mdc` — strengthened automatic post-change documentation
- `.cursor/workflow/changelog.md` — added timestamp format requirement
- `.cursor/workflow/development-workflow.md` — auto-documentation section added

### API impact
- None

### DB impact
- None

---

## 2026-07-09 11:17 (UTC+6) — Initial Cursor workflow documentation

**Time:** 2026-07-09 11:17 (UTC+6)  
**Author:** Cursor AI agent  
**Type:** Documentation

### Added
- `.cursor/workflow/` — full backend documentation suite:
  - `README.md` — index and ecosystem map
  - `architecture.md` — tech stack and layout
  - `database-flow.md` — ER diagram, models, data pipelines
  - `business-logic.md` — income formula, session rules, ad tracking math
  - `api-reference.md` — all endpoints and client mapping
  - `development-workflow.md` — setup, agent rules, multi-model review triggers
  - `changelog.md` — this file
- `.cursor/rules/` — Cursor rules for cross-account consistency

### Documented known issues (no code changes)
- Group name mismatch: `'Partner'` vs `'partner'` in venueinfo.py
- Migration 0003 schema drift (uuid/client_ip vs source_ip)
- Hardcoded secrets in settings.py
- Unused dependencies in requirements.txt

### API contracts documented
- Income: `total_income = round(Σ AdsViewHistory.count × 0.34, 2)`
- Session: clamp 1–10080 min, default 30
- Venue code: `{VENUE_UPPER}_{router_count}`

### API impact
- None (documentation only)

### DB impact
- None

---

<!-- Template for future entries:

## YYYY-MM-DD HH:MM (UTC+6) — Short title

**Time:** YYYY-MM-DD HH:MM (UTC+6)
**Author:** Name / agent
**Type:** Feature | Bugfix | Refactor | Docs | Migration

### Changed
- `path/to/file.py` — what and why

### API impact
- Endpoint: change description (or "None")

### DB impact
- Migration: description (or "None")

-->
