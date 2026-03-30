<!-- GSD:project-start source:PROJECT.md -->
## Project

**Sonar Vault**

Sonar Vault is a specialized offline software version control and repository platform designed for the air-gapped environment of Bharat Electronics Limited (BEL). It manages the software lifecycle for naval sonar systems installed across various Indian Naval Ships (Platforms). It allows departments (D&E, BSTC, Testing) to upload software binaries, track versions hierarchically (Platform -> Project -> Subsystem), and raise defect tickets with forensic attachments.

**Core Value:** A 100% offline, highly structured repository and ticketing system tailored specifically to the strict Platform-Project-Subsystem hierarchy of naval sonar deployments.

### Constraints

- **Security**: 100% Offline, no external CDNs or cloud dependencies.
- **Tech Stack**: FastAPI for the backend (architecture established instead of Flask as per PRD) and React/Vanilla JS.
- **Access Control**: Users must be manually approved by Admin.
<!-- GSD:project-end -->

<!-- GSD:stack-start source:codebase/STACK.md -->
## Technology Stack

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
## Database
- **SQLite** — File-based relational database (`sonar_vault.db`)
## ORM
- **SQLAlchemy** — ORM with `DeclarativeBase` pattern
## Authentication & Security
| Component | Library | Pattern |
|-----------|---------|---------|
| Password hashing | `bcrypt` (via `import bcrypt`) | `gensalt()` + `hashpw()` / `checkpw()` |
| JWT tokens | `python-jose[cryptography]` | HS256 algorithm, env-configurable |
| Session concurrency | JTI-based | Unique `uuid4()` per login, stored in `User.current_session_id` |
| Token auth | OAuth2PasswordBearer | FastAPI dependency + query param fallback |
## Frontend Stack
- **Bootstrap 5.3.3** — Locally bundled (`frontend/static/vendor/bootstrap/`)
- **Custom SVG Charting Helper** — `frontend/static/js/charting-helper.js`
- **ES Modules** — `dashboard.js` and `users.js` use `import`/`export`
## Dependencies
### Python (`requirements.txt`)
### Node.js (`package.json`)
## Configuration
- **Environment variables** via `.env` file (loaded by `python-dotenv`):
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
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

## Code Style Guides
## Python Backend (FastAPI)
### Code Style (Google Python Style Guide)
- **Formatting:** 4-space indentation, 80-character line limit.
- **Naming:** `snake_case` for variables/functions/modules, `PascalCase` for classes, `ALL_CAPS` for constants.
- **Docstrings:** Use Google format `"""triple double quotes"""` for public modules, classes, and methods.
- **Type Annotations:** Strongly encouraged for all public APIs.
- **Imports:** Grouped by standard library, third-party, and application. Avoid wildcard or implicit relative imports.
### FastAPI Patterns
- **Dependency Injection:** Use `Depends()` for database sessions (`get_db`) and authentication (`get_current_user`).
- **Routing:** Use `APIRouter` to modularize endpoints (e.g., in `api/v1/auth.py`). 
- **Error Handling:** Raise `HTTPException` directly in route handlers with appropriate status codes (400, 401, 403, 404).
## JavaScript Frontend
### Code Style (Google JavaScript Style Guide)
- **Formatting:** +2 spaces indentation for blocks, 80 column limit. K&R style braces.
- **Variables:** Use `const` and `let`. **`var` is strictly forbidden.**
- **Functions:** Prefer arrow functions for preserving `this` context.
- **Modules:** Use ES Modules (`import`/`export`). **Do not use default exports**; use named exports only.
- **JSDoc:** Required for all classes, methods, and fields.
### Application Patterns
- **Initialization:** Use `document.addEventListener('DOMContentLoaded', ...)` for page setup.
- **API Calls:** Use `fetch()` with `async`/`await`. Handle errors uniformly.
- **State:** Use `localStorage` for session tokens and user context.
## HTML/CSS
### Code Style (Google HTML/CSS Style Guide)
- **HTML Formatting:** 2-space indent, double quotes `""` for attributes. No `type` attribute on scripts/stylesheets.
- **CSS Formatting:** Alphabetize declarations, use 2-space indent, single quotes `''` within CSS.
- **Class Naming:** Use kebab-case for CSS classes (`.site-navigation`). Avoid ID selectors for styling.
### Application Patterns
- **Componentization:** Use localized Bootstrap 5.3.3 utilities and custom utility classes (e.g., `.bg-sv-primary`).
- **Icons:** Use inline SVG paths to maintain offline capabilities without external font dependencies.
## Git & Workflow Conventions
### Commit Messages
### Workflow (`conductor/workflow.md`)
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

## Pattern: Monolithic Server-Rendered + SPA-like Frontend
```
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
- `/` → `index.html` (redirector based on localStorage token)
- `/login` → `login.html` (public)
- `/register` → `register.html` (public)
- `/dashboard` → `dashboard.html` (requires `get_current_active_user`)
- `/users` → `users.html` (requires `get_current_admin_user`)
<!-- GSD:architecture-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->



<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
