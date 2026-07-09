# Business Logic & Mathematical Formulas

All formulas and rules implemented in `api/serializer.py` and `api/view/*.py`.

---

## 1. Partner income calculation

**Location:** `PartnerDashboardDataSerializer.get_total_income()` in `api/serializer.py`

```
total_income = round(total_ad_views × 0.34, 2)
```

Where:
```
total_ad_views = Σ AdsViewHistory.count   (for all partner profiles owned by the logged-in user)
```

| Variable | Source | Unit |
|----------|--------|------|
| `total_ad_views` | `obj.aggregate(total=Sum('count'))['total']` | impressions |
| `0.34` | Hardcoded constant | BDT per impression |
| `total_income` | Rounded to 2 decimal places | BDT |

**Example:**
```
If partner has 3 AdsViewHistory rows with count = [10, 25, 15]:
  total_ad_views = 10 + 25 + 15 = 50
  total_income = round(50 × 0.34, 2) = 17.00 BDT
```

---

## 2. Dashboard metrics (partner)

**Endpoint:** `GET /api/partner/dashboard/data/`  
**Serializer:** `PartnerDashboardDataSerializer`

| Metric | Formula | Code |
|--------|---------|------|
| `total_ads_campaign` | `COUNT(AdsViewHistory rows)` | `obj.count()` |
| `total_ads_viewed` | `Σ count` | `Sum('count')` aggregate |
| `total_users_viewed` | `COUNT(DISTINCT users.device_id)` | `values('users__device_id').distinct().count()` |
| `start_date` | `MIN(created_at)` formatted `%d.%b.%Y` | e.g. `09.Jul.2026` |
| `end_date` | `MAX(created_at)` formatted `%d.%b.%Y` | |
| `total_income` | See §1 | `round(total × 0.34, 2)` |

**Scope:** All `AdsViewHistory` where `partner.user.id == request.user.id` (all venues under one partner account).

---

## 3. Ad impression increment

**Endpoint:** `GET /api/ad/load/`  
**Location:** `api/view/adload.py`

Per request:
```
AdsViewHistory.count ← count + 1
```

Unique user tracking:
```
IF users (device_id) provided:
  Adusers.get_or_create(device_id=users)
  IF device_id NOT IN ad_view_history.users:
    ad_view_history.users.add(user_obj)
```

Ad selection:
```
ad = Adsmodel.filter(adSize, location, is_active=True).order_by('?').first()
```
Uniform random selection among matching active ads.

---

## 4. Session duration rules

**Location:** `api/view/venudata.py` — `_parse_session_duration_minutes()`

```
session_duration_minutes = clamp(input, min=1, max=10080)
default = 30
```

| Constraint | Value | Meaning |
|------------|-------|---------|
| Minimum | 1 minute | |
| Maximum | 10080 minutes | 7 days = 7 × 24 × 60 |
| Default | 30 minutes | If not provided |

**Client-side (y_fi app):** Session timer counts down from `session_duration_minutes × 60` seconds; auto-disconnect when timer reaches 0.

---

## 5. Venue code generation

**Location:** `api/view/venudata.py` — add Wi-Fi endpoint

```
venue_slug = venue_name.upper().replace(" ", "_")
router_count = PartnerProfile.objects.filter(user=partner_user).count() + 1
code = venue_slug + str(router_count)
```

**Example:** Venue "Cafe Dhaka", 2nd router → `CAFE_DHAKA_2`

**SSID uniqueness:** Per partner account, case-insensitive duplicate check before add/update.

---

## 6. End-user auto-registration

**Endpoint:** `POST /api/auth/login/`  
**Location:** `MyTokenObtainPairSerializer.validate()`

```
IF CustomUser.objects.filter(email=email) does NOT exist:
  CREATE user with email + password (Firebase UID from mobile)
  ADD to group 'user'
  CREATE UserProfile with device metadata
AUTHENTICATE → return JWT token
```

Password on mobile = Firebase UID (not user-chosen password).

---

## 7. Partner registration

**Endpoint:** `POST /api/auth/partner/register/`

Creates:
- `CustomUser` (email-based)
- `PartnerProfile` (venue_name, address, phone, ssid, password, code)
- Assigns group `partner`

---

## 8. QR code content

```
URL encoded: https://app.freeyfi.com/?code={partner_profile.code}
```

Styled JPEG emailed to partner on Wi-Fi add; also served via `GET /api/venue/wifi/qrcode/?code=`.

---

## 8. APK download counter

```
GET /api/release/app/  → latest ReleaseApp by created_at → count += 1 → return {url}
GET /api/partner/app/  → latest PartnerApp by created_at → count += 1 → return {url}
```

---

## Constants reference (do not change without updating all clients)

| Constant | Value | Used by |
|----------|-------|---------|
| Income rate | `0.34` BDT/view | Partner dashboard (backend + partner app) |
| Default session | `30` min | Partner Wi-Fi add, user connect flow |
| Max session | `10080` min (7 days) | Partner Wi-Fi config |
| Ad gate (client) | `30` seconds | y_fi app connecting overlay |
| JWT access lifetime | ~100 years | settings.SIMPLE_JWT |
| JWT refresh lifetime | ~2 years | settings.SIMPLE_JWT |
