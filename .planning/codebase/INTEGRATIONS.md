# External Integrations

## Overview

Sonar Vault is designed as a **100% offline** application. It has **no external API calls, no cloud services, and no network dependencies**. All functionality runs locally on the host machine.

## Database

| Integration | Type | Details |
|-------------|------|---------|
| SQLite | Local file DB | `sonar_vault.db` in project root |
| SQLAlchemy ORM | DB abstraction | Session-based, dependency-injected via `get_db()` |

- Connection configured in `database/db.py`
- Env-driven connection string (`DATABASE_URL`)
- Schema created via `Base.metadata.create_all()` (no Alembic)

## Authentication (Internal)

| Component | Protocol | Implementation |
|-----------|----------|----------------|
| JWT Tokens | HS256 signing | `python-jose` library in `app/token_utils.py` |
| Password Hashing | bcrypt | Direct `bcrypt` module in `app/auth_utils.py` |
| Session Control | JTI-based concurrency | UUID stored in `User.current_session_id` |

**Token endpoints:**
- `POST /api/v1/login` — Issues JWT with JTI, stores session in DB
- `POST /api/v1/logout` — Clears `current_session_id` in DB
- `GET /api/v1/session/status` — Validates current token/session

## Frontend ↔ Backend Communication

| Pattern | Details |
|---------|---------|
| REST API | JSON over HTTP, prefix `/api/v1/` |
| Token delivery | `localStorage` + query param `?token=` for page navigation |
| Static file serving | FastAPI `StaticFiles` mount at `/` for `frontend/` directory |

**API Routes (all under `/api/v1/`):**
- `POST /register` — User registration (returns `UserSchema`)
- `POST /login` — Authentication (returns `Token` with JWT)
- `POST /logout` — Session invalidation
- `GET /session/status` — Session validation
- `GET /admin/pending-users` — List unapproved users (admin only)
- `POST /admin/approve-user/{user_id}` — Approve pending user (admin only)

## File Storage

- **Current:** No file upload/storage implemented yet
- **Planned:** Local "Vault" folder for binary storage (per PRD)
  - Software binaries uploaded by D&E/BSTC departments
  - Auto-captured metadata (upload date) + manual fields (version, compiled date)

## External Services

**None.** The application is explicitly designed for an air-gapped environment (Bharat Electronics Limited naval sonar systems). Key constraints:
- No CDN dependencies
- No external font loading
- No analytics/telemetry
- No email services
- No cloud storage
- Bootstrap 5.3.3 bundled locally in `frontend/static/vendor/bootstrap/`

## Planned Integrations (from PRD)

| Feature | Status | Notes |
|---------|--------|-------|
| Software Repository (Vault) | Not implemented | Binary upload with version metadata |
| Defect Tracking | Not implemented | Ticket system with .pcap/.pdf attachments |
| Hierarchical Tree Navigation | Partially implemented | Mock data in `dashboard.js`, not DB-driven |
| Visualization / Charts | Partially implemented | `ChartingHelper` exists but not connected to real data |
