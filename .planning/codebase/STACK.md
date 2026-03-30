# Technology Stack

## Languages & Runtimes

| Layer | Language | Version | Notes |
|-------|----------|---------|-------|
| Backend | Python | 3.x | Primary server language |
| Frontend | JavaScript (ES Modules) | Vanilla | No build step, native `import`/`export` |
| Frontend | HTML5 / CSS3 | — | Bootstrap 5.3.3 for UI components |
| Scripts | Python | 3.x | Migrations, seeding |
| Scripts | Batch (.bat) | — | Windows server startup |

## Backend Framework

- **FastAPI** — Async-capable ASGI framework
  - Entry point: `app/main.py`
  - Single `FastAPI()` instance, mounted with `StaticFiles` for frontend serving
  - No separate ASGI middleware configured
  - Server: **Uvicorn** with `--reload` for development (port `8654`)

## Database

- **SQLite** — File-based relational database (`sonar_vault.db`)
  - Connection string: `sqlite:///./sonar_vault.db` (from env or default)
  - `check_same_thread=False` for SQLite compatibility
  - No migration framework (Alembic not used) — manual migration scripts in `scripts/`

## ORM

- **SQLAlchemy** — ORM with `DeclarativeBase` pattern
  - Base class: `models/base.py` → `class Base(DeclarativeBase)`
  - Session factory: `database/db.py` → `SessionLocal`
  - Dependency injection: `get_db()` generator yields session, closes on teardown

## Authentication & Security

| Component | Library | Pattern |
|-----------|---------|---------|
| Password hashing | `bcrypt` (via `import bcrypt`) | `gensalt()` + `hashpw()` / `checkpw()` |
| JWT tokens | `python-jose[cryptography]` | HS256 algorithm, env-configurable |
| Session concurrency | JTI-based | Unique `uuid4()` per login, stored in `User.current_session_id` |
| Token auth | OAuth2PasswordBearer | FastAPI dependency + query param fallback |

**Token flow:**
1. Login → `create_access_token()` returns `(jwt, jti)`
2. JTI stored in `User.current_session_id` (DB)
3. Each request validates token JTI matches DB → single-session enforcement
4. "Remember Me" extends expiry to 7 days (vs default 30 min)

## Frontend Stack

- **Bootstrap 5.3.3** — Locally bundled (`frontend/static/vendor/bootstrap/`)
  - `bootstrap.min.css` + `bootstrap.bundle.min.js`
  - No CDN dependencies (offline-first requirement)
- **Custom SVG Charting Helper** — `frontend/static/js/charting-helper.js`
  - Pure JS line/bar chart rendering via inline SVG
  - No external charting libraries
- **ES Modules** — `dashboard.js` and `users.js` use `import`/`export`
  - `login.js` and `register.js` are traditional scripts (no module system)

## Dependencies

### Python (`requirements.txt`)
```
fastapi
uvicorn[standard]
sqlalchemy
python-dotenv
passlib[bcrypt]
python-multipart
pytest
pytest-cov
```

> **Note:** `passlib[bcrypt]` is listed in requirements but the code directly uses `import bcrypt`. `python-jose` is used in code but not listed in requirements — this is a gap.

### Node.js (`package.json`)
```json
{
  "name": "sonar-vault",
  "version": "1.0.0"
}
```
Minimal `package.json` — no Node.js dependencies are actually used at runtime. This file exists for project metadata only.

## Configuration

- **Environment variables** via `.env` file (loaded by `python-dotenv`):
  - `DATABASE_URL` — SQLite connection string
  - `SECRET_KEY` — JWT signing key
  - `ALGORITHM` — JWT algorithm (default `HS256`)
  - `ACCESS_TOKEN_EXPIRE_MINUTES` — Token TTL (default `30`)
- Template: `.env.template` provides defaults
- **Virtual environment:** `.venv/` (Python venv)

## Development Tooling

| Tool | Purpose |
|------|---------|
| `pytest` | Unit + integration testing |
| `pytest-cov` | Code coverage reporting |
| `.venv` | Python virtual environment |
| `start_server.bat` | Windows startup script |

## Build & Deployment

- **No build step** — Frontend served as static files directly
- **No containerization** — Runs directly on host OS (Windows)
- **Offline-first** — All dependencies bundled locally, no network required
- **Server startup:** `uvicorn app.main:app --reload --port 8654`
