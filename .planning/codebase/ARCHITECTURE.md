# Architecture

## Pattern: Monolithic Server-Rendered + SPA-like Frontend

Sonar Vault uses a **monolithic Python backend** that serves both the API and the frontend static files. The frontend is a collection of **standalone HTML pages** (not a SPA) enhanced with vanilla JavaScript for interactivity.

```
┌─────────────────────────────────────────────────┐
│                  Browser Client                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │
│  │ login.js │ │register.js│ │  dashboard.js   │ │
│  │(vanilla) │ │(vanilla)  │ │  (ES module)    │ │
│  └────┬─────┘ └────┬─────┘ └────────┬─────────┘ │
│       │             │                │            │
│       └─────────────┴────────────────┘            │
│                     │ fetch()                     │
└─────────────────────┼─────────────────────────────┘
                      │ HTTP (JSON)
┌─────────────────────┼─────────────────────────────┐
│              FastAPI Application                   │
│  ┌──────────────────┴──────────────────────────┐  │
│  │            app/main.py                       │  │
│  │  ┌─────────────┐  ┌──────────────────────┐  │  │
│  │  │ Page Routes  │  │  StaticFiles Mount   │  │  │
│  │  │ (/, /login,  │  │  (frontend/ dir)     │  │  │
│  │  │  /dashboard) │  │                      │  │  │
│  │  └──────┬──────┘  └──────────────────────┘  │  │
│  │         │                                    │  │
│  │  ┌──────┴──────────────────────────────────┐ │  │
│  │  │         api/v1/auth.py (Router)          │ │  │
│  │  │  /register  /login  /logout              │ │  │
│  │  │  /session/status  /admin/*               │ │  │
│  │  └──────┬──────────────────────────────────┘ │  │
│  └─────────┼────────────────────────────────────┘  │
│            │                                        │
│  ┌─────────┴──────────┐  ┌────────────────────────┐│
│  │  app/ utilities     │  │   models/              ││
│  │  ├─ auth_utils.py   │  │   ├─ base.py           ││
│  │  ├─ token_utils.py  │  │   └─ user.py           ││
│  │  └─ schemas.py      │  │                        ││
│  └─────────────────────┘  └───────────┬────────────┘│
│                                       │              │
│  ┌────────────────────────────────────┴─────────────┐│
│  │          database/db.py                           ││
│  │  SQLAlchemy Engine + SessionLocal + get_db()      ││
│  └────────────────────────┬──────────────────────────┘│
└───────────────────────────┼───────────────────────────┘
                            │
                    ┌───────┴───────┐
                    │  SQLite DB    │
                    │ sonar_vault.db│
                    └───────────────┘
```

## Layers

### 1. Presentation Layer (Frontend)
- **Technology:** Vanilla HTML/JS with Bootstrap 5.3.3
- **Pattern:** Multi-page with page-specific JS files
- **Auth flow:** Token stored in `localStorage`, passed via query param on page navigation
- **Module system:** Mixed — `dashboard.js`/`users.js` use ES modules, `login.js`/`register.js` are traditional scripts

### 2. API Layer
- **Technology:** FastAPI with `APIRouter`
- **Prefix:** `/api/v1/`
- **Auth:** `OAuth2PasswordBearer` + query param fallback for page-level auth
- **Response models:** Pydantic `BaseModel` schemas in `app/schemas.py`

### 3. Business Logic Layer
- Embedded within the API route handlers in `api/v1/auth.py`
- Auth utilities extracted to `app/auth_utils.py` (password hashing) and `app/token_utils.py` (JWT creation)
- No dedicated service/use-case layer

### 4. Data Access Layer
- **Technology:** SQLAlchemy ORM
- **Pattern:** Dependency-injected session via `get_db()` generator
- **Models:** `models/user.py` (single model currently)
- **Base:** `models/base.py` with `DeclarativeBase`

### 5. Database Layer
- **Technology:** SQLite
- **File:** `sonar_vault.db` (project root)
- **Migrations:** Manual Python scripts in `scripts/`

## Data Flow: Login

```
Browser                 FastAPI                  SQLAlchemy         SQLite
  │                       │                        │                 │
  │ POST /api/v1/login    │                        │                 │
  │─────────────────────>│                        │                 │
  │                       │ query User by staff_no │                 │
  │                       │───────────────────────>│ SELECT ...      │
  │                       │                        │────────────────>│
  │                       │                        │<────────────────│
  │                       │<───────────────────────│                 │
  │                       │ verify_password()      │                 │
  │                       │ create_access_token()  │                 │
  │                       │ store JTI in user.     │                 │
  │                       │  current_session_id    │                 │
  │                       │───────────────────────>│ UPDATE ...      │
  │                       │                        │────────────────>│
  │   { access_token,     │                        │                 │
  │     token_type,       │                        │                 │
  │     role, full_name } │                        │                 │
  │<─────────────────────│                        │                 │
  │                       │                        │                 │
  │ localStorage.set()   │                        │                 │
  │ redirect /dashboard   │                        │                 │
```

## Entry Points

| Entry Point | File | Purpose |
|-------------|------|---------|
| App server | `app/main.py` | FastAPI app creation, router mounting, static files |
| Auth API | `api/v1/auth.py` | All authentication and admin endpoints |
| DB seed | `scripts/seed_admin.py` | Initial admin user creation |
| Server start | `start_server.bat` | Windows batch startup |

## Key Abstractions

| Abstraction | Location | Role |
|-------------|----------|------|
| `Base` | `models/base.py` | SQLAlchemy declarative base |
| `get_db()` | `database/db.py` | DB session dependency |
| `get_current_user()` | `api/v1/auth.py` | JWT validation + session check |
| `get_current_active_user()` | `api/v1/auth.py` | Approved + active check |
| `get_current_admin_user()` | `api/v1/auth.py` | Admin role check |
| `SessionManager` | `frontend/static/js/session-manager.js` | Client-side idle timeout |
| `ChartingHelper` | `frontend/static/js/charting-helper.js` | SVG chart rendering |

## Routing Strategy

**Backend routes** serve HTML pages with auth guards:
- `/` → `index.html` (redirector based on localStorage token)
- `/login` → `login.html` (public)
- `/register` → `register.html` (public)
- `/dashboard` → `dashboard.html` (requires `get_current_active_user`)
- `/users` → `users.html` (requires `get_current_admin_user`)

**API routes** are JSON-only under `/api/v1/`.

**Static files** mounted last at `/` to avoid overriding explicit routes.
