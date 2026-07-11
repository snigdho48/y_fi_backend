# FreeYFi Main API (`y_fi_backend`)

Django REST API for the FreeYFi mobile apps and marketing site: user/partner auth, venues, Wi‑Fi sessions, ads, partner dashboard, contact form, and APK metadata.

**Production:** `https://app.freeyfi.com/api/`  
**Local:** `http://127.0.0.1:8000/api/`

> Theme Studio and admin login are **not** in this service — use [`dashboard-backend`](../dashboard-backend/).

See the [monorepo README](../README.md) for full architecture, deployment, and GitLab CI.

---

## Quick start

```bash
cd y_fi_backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/macOS
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

OpenAPI schema: `http://127.0.0.1:8000/api/schema/`

---

## Who uses this API

| Client | Features |
|--------|----------|
| `y_fi` (user app) | Login, venue QR, Wi‑Fi connect, ads, telemetry |
| `y_fi_partner` | Partner auth, venues, dashboard, earnings |
| `y_fi_frontend` | Contact form, APK download links (`APP_API_BASE`) |

---

## Stack

- Django 5 + Django REST Framework
- MySQL (production)
- JWT, Channels/Daphne (WebSockets where used)
- Celery + Redis (background tasks)

---

## Documentation

| Doc | Path |
|-----|------|
| Workflow index | [`.cursor/workflow/README.md`](.cursor/workflow/README.md) |
| API reference | [`.cursor/workflow/api-reference.md`](.cursor/workflow/api-reference.md) |
| Architecture | [`.cursor/workflow/architecture.md`](.cursor/workflow/architecture.md) |
| Local dev & deploy | [`.cursor/workflow/development-workflow.md`](.cursor/workflow/development-workflow.md) |

---

## Deploy (summary)

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
# restart Gunicorn/Daphne + reload nginx
```

Push-to-deploy may use GitHub Actions or GitLab CI — see root [README](../README.md#deployment).

---

## Security

Do not commit production secrets. Never commit `.env` with DB/SMTP credentials.
