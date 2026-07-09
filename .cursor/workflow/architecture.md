# Backend Architecture

## Tech stack

| Layer | Technology | Version (requirements.txt) |
|-------|------------|---------------------------|
| Language | Python 3 | — |
| Framework | Django | 5.2.4 |
| API | Django REST Framework | 3.16.0 |
| Auth | djangorestframework-simplejwt | 5.5.0 |
| Database | MySQL via mysqlclient | 2.2.7 |
| API docs | drf-spectacular | 0.28.0 |
| CORS | django-cors-headers | 4.7.0 |
| Media | Pillow + qrcode | QR generation |
| HTTP client | requests | CMS / venudata proxy |
| Server | Gunicorn + Nginx | Ubuntu production |
| Timezone | Asia/Dhaka | All `created_at` timestamps |

## Project layout

```
y_fi_backend/
├── manage.py
├── requirements.txt
├── .github/workflows/django.yml    # CI/CD: SSH deploy on push to master
├── legal/PRIVACY_POLICY.md
├── y_fi_backend/                   # Django project settings
│   ├── settings.py                 # All config (currently hardcoded)
│   ├── urls.py                     # /admin/ + /api/
│   ├── wsgi.py / asgi.py
└── api/                            # Single app — all business logic
    ├── models.py
    ├── serializer.py
    ├── urls.py
    ├── views.py                    # Re-exports view classes
    ├── admin.py
    ├── migrations/
    └── view/                       # APIView implementations
        ├── auth.py
        ├── venudata.py
        ├── datacollect.py
        ├── adload.py
        ├── Releaseapp.py
        ├── partnerDashbaord.py
        ├── venueinfo.py
        └── contact.py
```

## Architecture pattern

- **Monolithic single-app Django** — no `services/`, `repositories/`, or Celery workers in active use.
- Business logic lives in `api/view/*.py` and `api/serializer.py`.
- JWT is the runtime auth mechanism (`JWTAuthentication` on protected views).
- Default `REST_FRAMEWORK` auth is `TokenAuthentication` but views override to JWT.

## Auth groups

| Group name | Created by | Used for |
|------------|------------|----------|
| `user` | Auto on first `auth/login/` | End-user mobile app |
| `partner` | `auth/partner/register/` | Partner mobile app |
| `admin` | Manual / Django admin | Partner list endpoint |

> **Known bug:** `venueinfo.py` checks group `'Partner'` (capital P) on GET, but registration assigns `'partner'` (lowercase).

## External integrations

| Service | URL | Purpose |
|---------|-----|---------|
| CMS | `https://cms.freeyfi.com/api/v1/app_connection_data/` | Sync `ConnectedHistory` telemetry |
| VenueData | `https://venudata.in/api/partner/dashboard` | Legacy dashboard proxy |
| SMTP | `mail.adcelerete.com:465` | QR code email to partners |
| QR deep link | `https://app.freeyfi.com/?code={code}` | Encoded in venue QR images |

## Deployment

GitHub Actions (`.github/workflows/django.yml`):
1. SSH to Ubuntu server on push to `master`
2. `git pull` → `pip install -r requirements.txt`
3. Restart `gunicorn` + `nginx`

## Unused dependencies (present in requirements.txt but not wired)

Celery, Channels, Redis, django-allauth, numpy, pandas, python-dotenv (not loaded in settings).
