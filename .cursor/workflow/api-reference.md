# API Reference

**Base URL:** `https://app.freeyfi.com/api/`  
**Auth header:** `Authorization: Bearer <jwt_token>`  
**Docs:** Swagger `/api/test/` · ReDoc `/api/` · Schema `/api/schema/`

---

## Auth

### POST `/auth/login/` — End-user login (auto-register)

**Auth:** None  
**Body:**
```json
{
  "email": "user@example.com",
  "password": "<firebase_uid>",
  "username": "Display Name",
  "device_id": "abc123",
  "device_name": "Pixel 7",
  "device_os": "Android 14",
  "device_brand": "Google"
}
```
**Response 200:**
```json
{
  "refresh": "...",
  "username": "...",
  "email": "...",
  "user_group": "user",
  "token": "<access_jwt>"
}
```

### POST `/auth/partner/login/` — Partner login

**Body:** `{ "email", "password" }`  
**Response:** `{ token, username, email, user_group, partner_id }`

### POST `/auth/partner/register/` — Partner registration

**Body:** venue_name, email, password, address, phone_number, ssid, password (wifi)  
**Response:** JWT + partner profile data

### POST `/auth/token/refresh/` — Refresh JWT

**Body:** `{ "refresh": "..." }`

### GET `/auth/logout/` — Blacklist refresh token

**Auth:** Required · Pass refresh token in `Authorization` header

---

### POST `/auth/admin/login/` — Admin login (Theme Studio)

**Auth:** None  
**Body:** `{ "email", "password" }`  
**Requires:** user in `admin` group  
**Response:** `{ token, username, email, user_group: "admin" }`

---

## Theme (remote app styling)

### GET `/theme/?app=user|partner` — Active theme (public)

**Auth:** None  
**Response:**
```json
{
  "name": "Default Dark",
  "app_target": "user",
  "primary_color": "#191B41",
  "scaffold_color": "#191B41",
  "accent_color": "#B2FF59",
  "on_primary_color": "#FFFFFF",
  "font_family": "",
  "background_color": "#191B41",
  "background_image_url": null,
  "section_styles": {
    "home": { "background": "#191B41", "font_color": "#FFFFFF", "heading_color": "#B2FF59" },
    "login": { "background": "#191B41", "font_color": "#FFFFFF", "heading_color": "#B2FF59" }
  }
}
```

### GET|POST `/admin/theme/` — List / create themes

**Auth:** JWT, group=`admin`

### GET|PATCH|DELETE `/admin/theme/<id>/` — Theme detail

**Auth:** JWT, group=`admin`

### POST `/admin/theme/<id>/activate/` — Set active theme for app_target

**Auth:** JWT, group=`admin`

### GET `/admin/theme/defaults/` — Default section keys and colors

**Auth:** JWT, group=`admin`

---

## Venue / Wi-Fi (Partner JWT)

### POST `/venue/data/` — Resolve QR code

**Body:** `{ "code": "VENUE_1" }`  
**Response:** `{ ssid, password, code, session_duration_minutes }`

### GET `/venue/data/list/` — List partner venues

**Response:** Array of PartnerProfile fields

### POST `/venue/wifi/add/` — Add Wi-Fi network

**Body:** `{ ssid, password, session_duration_minutes? }`  
**Side effect:** Generates code, QR image, emails partner

### POST `/venue/wifi/update/` — Update Wi-Fi

**Body:** `{ code, ssid?, password?, session_duration_minutes? }`

### POST `/venue/wifi/delete/` — Delete venue

**Body:** `{ "code": "VENUE_1" }`

### GET `/venue/wifi/qrcode/?code=VENUE_1` — QR image

**Response:** JPEG bytes

---

## Data collection

### POST `/data/collect/` — Save connection telemetry

**Auth:** JWT (user)  
**Body:** user, partner (PK), ip, device_os, device_name, device_brand, device_id  
**Side effect:** Forwards to CMS, deletes on success

### GET `/venue/passdata/` — Batch CMS sync

**Auth:** Public · Streams sync of all pending ConnectedHistory

---

## Ads

### GET `/ad/load/`

**Auth:** None  
**Query params:**

| Param | Required | Type | Description |
|-------|----------|------|-------------|
| `adsize` | Yes | string | e.g. `320x50` |
| `location` | Yes | string | e.g. `connecting` |
| `partner` | No | int | PartnerProfile.id |
| `users` | No | string | device_id for unique tracking |

**Response:** `{ adSize, adUrl, adLanding, created_at }`

---

## Partner dashboard

### GET `/partner/dashboard/data/`

**Auth:** JWT, group=`partner`  
**Response:**
```json
{
  "total_ads_campaign": 12,
  "total_users_viewed": 45,
  "total_ads_viewed": 150,
  "start_date": "01.Jan.2026",
  "end_date": "09.Jul.2026",
  "total_income": 51.0
}
```

### GET `/partner/dashboard/` — Legacy venudata proxy

**Auth:** JWT · Proxies to `venudata.in`

---

## App distribution

### GET `/release/app/` — User APK

**Response:** `{ "url": "https://..." }` · Increments download count

### GET `/partner/app/` — Partner APK

**Response:** `{ "url": "https://..." }`

---

## Venue geo & admin

### GET/POST `/venue/details/` — Lat/long CRUD

**Auth:** JWT

### GET `/partner/list/` — List partners

**Auth:** JWT, admin group

---

## Public

### POST `/contact/` — Contact form

**Body:** `{ name, message, email }`  
**Validation:** message min 10 chars

---

## Client consumers

| Endpoint group | y_fi (user) | y_fi_partner | y_fi_frontend |
|----------------|-------------|--------------|---------------|
| auth/login | ✅ | — | — |
| auth/partner/* | — | ✅ | — |
| venue/data | ✅ | — | — |
| venue/wifi/* | — | ✅ | — |
| data/collect | ✅ | — | — |
| ad/load | ✅ | — | — |
| partner/dashboard/data | — | ✅ | — |
| release/app, partner/app | — | — | ✅ |
| contact | — | — | ✅ |
