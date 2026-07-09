# Development Workflow

## Local setup

```bash
cd y_fi_backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

API available at `http://127.0.0.1:8000/api/`

## Before every change

1. Read [README.md](./README.md) and relevant workflow docs
2. Identify which clients consume the endpoint (`api-reference.md` client table)
3. Plan migration if models change

## After every change (automatic)

Agents MUST do this before responding — user does not need to ask:

1. Prepend [changelog.md](./changelog.md) with `## YYYY-MM-DD HH:MM (UTC+6) — Title`
2. Update `api-reference.md` if endpoints/contracts change
3. Update `database-flow.md` if models change
4. Update `business-logic.md` if formulas/constants change
5. Run `python manage.py makemigrations` + `migrate` for model changes
6. Notify mobile/frontend teams if API contract breaks

Enforced by `.cursor/rules/auto-changelog.mdc` and root `auto-documentation.mdc`.

## Deploy

Push to `master` → GitHub Actions SSH deploy → Gunicorn + Nginx restart.

## AI agent guidelines

### Scope discipline
- Only modify files required for the task
- Match existing patterns in `api/view/` and `api/serializer.py`
- Do not add unused dependencies

### Security (known issues — fix carefully)
- `SECRET_KEY`, DB creds, SMTP creds are hardcoded in `settings.py`
- `DEBUG=True`, `ALLOWED_HOSTS=['*']`, `CORS_ALLOW_ALL_ORIGINS=True` in production settings
- Prefer env vars when touching settings (but coordinate with deploy)

### When to use multi-model review

Use `/multi-model-review` or parallel Task agents when:
- Changing `business-logic.md` formulas (income rate, session limits)
- Modifying auth flows or JWT handling
- Changing `ConnectedHistory` sync pipeline
- Any migration affecting `PartnerProfile` or `AdsViewHistory`

Recommended models for review: `claude-4.6-sonnet-medium-thinking`, `gpt-5.3-codex`, `gemini-3.1-pro` (run in parallel).

### Testing

`api/tests.py` is currently empty. When adding tests:
- Place in `api/tests/` or expand `tests.py`
- Cover serializer math (income = views × 0.34)
- Cover session_duration clamping (1–10080)
- Cover ad load count increment

## Code conventions

- Views: class-based `APIView` in `api/view/`
- Serializers: `api/serializer.py`
- OpenAPI: `@extend_schema` decorators on views
- Timezone: always `Asia/Dhaka` via model default
- Partner group name: lowercase `'partner'` (fix `'Partner'` bug in venueinfo.py when touching that file)
