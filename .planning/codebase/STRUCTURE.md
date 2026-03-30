# Directory Structure

## Project Root

```
sonar-vault/
├── .agents/                    # GSD agent workflows + config
├── .env.template               # Environment variable template
├── .gitignore                  # Git exclusions
├── .venv/                      # Python virtual environment
├── PRD/                        # Product Requirements Documents
│   ├── PRD.md                  #   Full product requirements
│   ├── dashboard-design.md     #   Dashboard design spec
│   ├── navbar-design.md        #   Navbar design spec
│   └── image.png               #   Reference design image
├── api/                        # REST API layer
│   └── v1/                     #   API version 1
│       └── auth.py             #     Authentication routes (all endpoints)
├── app/                        # Application core
│   ├── main.py                 #   FastAPI app setup, page routes, static mount
│   ├── auth_utils.py           #   Password hashing (bcrypt)
│   ├── schemas.py              #   Pydantic request/response models
│   └── token_utils.py          #   JWT creation utilities
├── conductor/                  # Project governance docs
│   ├── archive/                #   Archived plans
│   ├── code_styleguides/       #   Code style guides (Python, JS, HTML/CSS, General)
│   │   ├── general.md
│   │   ├── html-css.md
│   │   ├── javascript.md
│   │   └── python.md
│   ├── index.md                #   Conductor index
│   ├── product.md              #   Product guide
│   ├── product-guidelines.md   #   Design philosophy & UX guidelines
│   ├── setup_state.json        #   Setup progress state
│   ├── tech-stack.md           #   Technology stack decisions
│   ├── tracks.md               #   Work tracks
│   └── workflow.md             #   TDD workflow & commit guidelines
├── database/                   # Database layer
│   └── db.py                   #   SQLAlchemy engine, session factory, get_db()
├── frontend/                   # Frontend layer (served as static)
│   ├── index.html              #   Root redirector (checks localStorage token)
│   ├── login.html              #   Login page
│   ├── register.html           #   Registration page
│   ├── dashboard.html          #   Main dashboard (sidebar + content)
│   ├── users.html              #   Admin user management page
│   └── static/                 #   Static assets
│       ├── images/
│       │   └── logo.svg        #     App logo
│       ├── js/
│       │   ├── charting-helper.js  # SVG chart utilities (ES module)
│       │   ├── dashboard.js        # Dashboard interactivity (ES module)
│       │   ├── login.js            # Login form handler
│       │   ├── register.js         # Registration form handler
│       │   ├── session-manager.js  # Idle timeout manager (ES module)
│       │   └── users.js            # Admin user management (ES module)
│       └── vendor/
│           └── bootstrap/      #     Bootstrap 5.3.3 (locally bundled)
├── models/                     # SQLAlchemy models
│   ├── base.py                 #   DeclarativeBase
│   └── user.py                 #   User model (all columns)
├── scripts/                    # Utility scripts
│   ├── migrate_session_id.py   #   Adds current_session_id column
│   ├── migrate_user_registration.py  # Adds registration fields
│   └── seed_admin.py           #   Creates initial admin user
├── tests/                      # Test suite
│   ├── conftest.py             #   Pytest fixtures (test DB, client)
│   ├── test_admin_approval_api.py
│   ├── test_auth_utils.py
│   ├── test_dashboard_components.py
│   ├── test_dashboard_scaffolding.py
│   ├── test_db.py
│   ├── test_frontend_scaffolding.py
│   ├── test_integration.py
│   ├── test_login_api.py
│   ├── test_login_updates.py
│   ├── test_phase1_bootstrap.py
│   ├── test_phase1_db_schema.py
│   ├── test_phase2_login_bootstrap.py
│   ├── test_phase3_dashboard_bootstrap.py
│   ├── test_registration_api.py
│   ├── test_session_api.py
│   ├── test_user_model.py
│   └── test_user_model_session.py
├── package.json                # Node.js metadata (minimal, no deps used)
├── package-lock.json           # Node.js lock file
├── requirements.txt            # Python dependencies
└── start_server.bat            # Windows server startup script
```

## Key Locations

| What | Where | Notes |
|------|-------|-------|
| FastAPI app instance | `app/main.py` | Entry point for `uvicorn` |
| All API endpoints | `api/v1/auth.py` | Single router file for all auth + admin endpoints |
| Database config | `database/db.py` | Engine, SessionLocal, get_db |
| User model | `models/user.py` | Only data model (no platforms, projects, etc. yet) |
| Pydantic schemas | `app/schemas.py` | `UserLogin`, `Token`, `UserSchema`, `UserRegister` |
| Frontend pages | `frontend/*.html` | 5 HTML pages served by FastAPI |
| JavaScript modules | `frontend/static/js/` | 6 JS files (mix of ES modules and scripts) |
| Bootstrap assets | `frontend/static/vendor/bootstrap/` | Locally bundled CSS + JS |
| Migration scripts | `scripts/` | 3 manual migration/seed scripts |
| Test suite | `tests/` | 18 test files + conftest.py |
| Product docs | `PRD/` + `conductor/` | Requirements, guidelines, workflow docs |

## Naming Conventions

| Convention | Examples | Scope |
|------------|----------|-------|
| `snake_case.py` | `auth_utils.py`, `token_utils.py` | Python files |
| `kebab-case.js` | `charting-helper.js`, `session-manager.js` | JavaScript files |
| `kebab-case.html` | `login.html`, `dashboard.html` | HTML pages |
| `kebab-case.md` | `tech-stack.md`, `product-guidelines.md` | Documentation |
| `PascalCase` | `User`, `UserLogin`, `SessionManager` | Classes |
| `snake_case` | `get_db()`, `hash_password()` | Python functions |
| `camelCase` | `fetchPendingUsers()`, `renderTree()` | JavaScript functions |
| `SCREAMING_SNAKE` | `SECRET_KEY`, `DATABASE_URL` | Constants/env vars |

## File Size Indicators

| File | Size | Significance |
|------|------|-------------|
| `api/v1/auth.py` | 7.1 KB (192 lines) | Largest backend file — all API logic |
| `frontend/dashboard.html` | 17 KB (283 lines) | Largest frontend file — full layout |
| `frontend/static/js/dashboard.js` | 9.6 KB (221 lines) | Most complex JS — tree, stats, fleet widget |
| `conductor/workflow.md` | 14.5 KB (334 lines) | Comprehensive TDD workflow documentation |
| `PRD/PRD.md` | 6.9 KB (122 lines) | Full product requirements |
