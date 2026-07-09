# FreeYFi Backend — Cursor Workflow Index

> **Product:** FreeYFi (Y-Fi) — venue-based free Wi-Fi with ad monetization  
> **Repo path:** `y_fi_backend/`  
> **Production API:** `https://app.freeyfi.com/api/`  
> **Last updated:** 2026-07-09

## What this folder is

This `.cursor/workflow/` directory is the **single source of truth** for how the Django backend works, how data flows, and how every AI/human contributor should document changes. Any Cursor account opening this repo should read these files before making changes.

## Documents

| File | Purpose |
|------|---------|
| [architecture.md](./architecture.md) | Tech stack, folder layout, deployment |
| [database-flow.md](./database-flow.md) | ER diagram, models, relationships, migrations |
| [business-logic.md](./business-logic.md) | Financial formulas, session rules, ad tracking math |
| [api-reference.md](./api-reference.md) | All REST endpoints, auth, request/response shapes |
| [development-workflow.md](./development-workflow.md) | Local setup, testing, deploy, AI agent rules |
| [changelog.md](./changelog.md) | Chronological log of all documented changes |

## Ecosystem map

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  y_fi (user)    │────▶│  y_fi_backend    │◀────│ y_fi_partner    │
│  Flutter app    │     │  Django REST API │     │ Flutter app     │
└─────────────────┘     └────────┬─────────┘     └─────────────────┘
                                 │
                    ┌────────────┼────────────┐
                    ▼            ▼            ▼
              MySQL DB    cms.freeyfi.com  venudata.in
┌─────────────────┐
│ y_fi_frontend   │  Marketing site (APK download, contact form)
│ React + Vite    │
└─────────────────┘
```

## Mandatory documentation rule

**Automatic on every agent turn** — no user prompt required.

Every file change MUST prepend [changelog.md](./changelog.md) with timestamp `YYYY-MM-DD HH:MM (UTC+6)` and update relevant workflow docs. Enforced by `.cursor/rules/auto-changelog.mdc` and root `auto-documentation.mdc`.
