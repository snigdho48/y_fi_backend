# Changelog

All changes to `y_fi_backend` must be logged here newest-first.

**Format:** `## YYYY-MM-DD HH:MM (UTC+6) — Title` with `**Time:**` field in every entry.

---

## 2026-07-09 11:23 (UTC+6) — Auto-documentation rules + timestamp format

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
