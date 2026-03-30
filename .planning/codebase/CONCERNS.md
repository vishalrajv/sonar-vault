# Concerns & Technical Debt

## Critical Issues

### 1. Missing Dependency: `python-jose`
- **File:** `app/token_utils.py` (line 4), `api/v1/auth.py` (line 5)
- **Issue:** `from jose import JWTError, jwt` is used but `python-jose[cryptography]` is NOT listed in `requirements.txt`
- **Impact:** Fresh installs will fail with `ModuleNotFoundError`
- **Fix:** Add `python-jose[cryptography]` to `requirements.txt`

### 2. Hardcoded Fallback Secret Key
- **File:** `app/token_utils.py` (line 9)
- **Code:** `SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")`
- **Issue:** If `.env` is missing or `SECRET_KEY` is unset, the fallback `"supersecretkey"` is used in production
- **Impact:** Security vulnerability — tokens signed with a known key
- **Fix:** Remove default or fail-fast if `SECRET_KEY` is not configured

### 3. Token Exposure via URL Query Parameters
- **Files:** `frontend/static/js/login.js` (line 45), `frontend/static/js/dashboard.js` (lines 60-68)
- **Pattern:** `window.location.href = '/dashboard?token=${data.access_token}'`
- **Issue:** JWT token visible in browser URL bar, browser history, server access logs, and any referrer headers
- **Impact:** Token leakage risk — anyone viewing the screen, browser history, or server logs can steal sessions
- **Fix:** Use HTTP-only cookies or header-only auth (remove query param pattern)

### 4. `datetime.utcnow()` Deprecation
- **File:** `app/token_utils.py` (lines 16, 18)
- **Issue:** `datetime.utcnow()` is deprecated in Python 3.12+ in favor of `datetime.now(timezone.utc)`
- **Impact:** Will raise deprecation warnings and may break in future Python versions

## Architectural Concerns

### 5. No Migration Framework
- **Files:** `scripts/migrate_*.py`
- **Issue:** Database migrations are manual Python scripts using raw SQL (`ALTER TABLE`)
- **Impact:** Schema changes are error-prone, un-versioned, and not reversible
- **Recommendation:** Adopt Alembic for versioned, repeatable migrations

### 6. Single API Router File
- **File:** `api/v1/auth.py` (192 lines, 7.1 KB)
- **Issue:** All endpoints (registration, login, logout, session, admin approval) live in one file
- **Impact:** Will become unwieldy as features are added (Vault, Defects, etc.)
- **Recommendation:** Split into `auth.py`, `admin.py`, `session.py` routers

### 7. No Service Layer
- **Issue:** Business logic is embedded directly in route handlers
- **Impact:** Difficult to test logic in isolation, hard to reuse across different endpoints
- **Example:** Login flow (verify password → create token → update session) is all in the route handler

### 8. Duplicated Theme CSS
- **Files:** `frontend/dashboard.html` (lines 10-38), `frontend/users.html` (lines 10-38)
- **Issue:** Identical CSS variables and utility classes copy-pasted between pages
- **Impact:** Theme changes require updating multiple files
- **Fix:** Extract to `frontend/static/css/theme.css`

### 9. Duplicated JS Logic
- **Files:** `frontend/static/js/dashboard.js` (lines 8-68), `frontend/static/js/users.js` (lines 7-68)
- **Issue:** Logout handler, user profile population, admin link visibility, and token link injection are identical across both files
- **Impact:** Any change to shared behavior requires editing multiple files
- **Fix:** Extract to a shared `app-shell.js` module

## Security Concerns

### 10. Admin Password in Seed Script
- **File:** `scripts/seed_admin.py` (line 26)
- **Code:** `hash_password("admin123")`
- **Issue:** Default admin password is hardcoded and weak
- **Mitigation:** Comment says "Change after first login" but no enforcement exists

### 11. No Input Validation on Registration
- **File:** `api/v1/auth.py` (lines 72-102)
- **Issue:** No validation on `staff_number` format, password strength, email format, phone format
- **Impact:** Users can register with empty strings or invalid data
- **Note:** `EmailStr` is imported in `schemas.py` but not used on `personal_email`/`official_email` fields

### 12. No CORS Configuration
- **File:** `app/main.py`
- **Issue:** No CORS middleware configured
- **Impact:** Currently not an issue (single-origin), but will be if API is consumed from different origins

### 13. No Rate Limiting
- **Files:** `api/v1/auth.py` (login, register endpoints)
- **Issue:** No protection against brute-force login attempts or registration spam
- **Impact:** Password could be brute-forced without any throttling

## Data Model Gaps

### 14. No Platform/Project/Subsystem Models
- **Current:** Only `User` model exists
- **PRD requires:** Platform → Project → Subsystem hierarchy
- **Impact:** Core Vault functionality (software uploads, version tracking) cannot be implemented without data models

### 15. No File Upload Model
- **PRD requires:** Software binary uploads with metadata (version, compiled date, upload date)
- **Impact:** The "Vault" (core feature) is not implemented

### 16. No Defect Tracking Model
- **PRD requires:** Defect tickets with forensic attachments (.pcap, .pdf)
- **Impact:** Testing department workflow is not supported

## Frontend Concerns

### 17. Mock/Hardcoded Data
- **File:** `frontend/static/js/dashboard.js`
  - Fleet hierarchy is hardcoded (lines 81-115)
  - Stats data is hardcoded (lines 168-172)
  - Fleet status data is hardcoded (lines 194-197)
- **Impact:** Dashboard shows fake data — not connected to any real backend data

### 18. No Error Page
- **Issue:** No 404 or error pages configured
- **Impact:** Users hitting undefined routes see raw FastAPI JSON errors

### 19. Sidebar Not Componentized
- **Issue:** Full sidebar HTML is duplicated between `dashboard.html` and `users.html`
- **Impact:** Adding new pages requires copy-pasting the entire sidebar

## Performance Concerns

### 20. No Database Indexing Strategy
- **Current indexes:** `id` (PK), `username` (unique), `staff_number` (unique)
- **Issue:** Adequate for current scale but no indexing plan for future models
- **Impact:** Query performance could degrade as data grows

### 21. No Caching
- **Issue:** No caching layer for static data or frequently accessed records
- **Impact:** Every request hits SQLite directly

## Fragile Areas

| Area | Risk | Trigger |
|------|------|---------|
| Token query param auth | Token leakage | Any page navigation |
| Module-scoped test fixtures | Test ordering bugs | Adding new tests to existing modules |
| Manual migration scripts | Schema drift | Adding new model columns |
| localStorage auth state | Stale UI data | User role/profile changes without re-login |
| Hardcoded mock data in dashboard | Misleading display | Users believing fake metrics are real |
