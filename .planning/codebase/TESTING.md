# Testing

## Framework & Tooling

| Tool | Purpose | Config |
|------|---------|--------|
| `pytest` | Test runner | Default config, no `pytest.ini` or `pyproject.toml` |
| `pytest-cov` | Coverage reporting | CLI flag: `--cov=app --cov-report=html` |
| `FastAPI TestClient` | HTTP integration tests | Via `from fastapi.testclient import TestClient` |
| SQLite (in-memory/file) | Test database | `sqlite:///./test.db` in `conftest.py` |

## Test Structure

### Location
All tests live in `tests/` directory at project root. No subdirectories — flat structure.

### Test Files (18 total)

| Test File | Focus | Lines |
|-----------|-------|-------|
| `conftest.py` | Shared fixtures (test DB, client, admin seed) | 52 |
| `test_phase1_bootstrap.py` | Phase 1 scaffolding validation | 1611 |
| `test_phase1_db_schema.py` | Database schema verification | 713 |
| `test_phase2_login_bootstrap.py` | Login page/API bootstrapping | 1324 |
| `test_phase3_dashboard_bootstrap.py` | Dashboard scaffolding | 2024 |
| `test_auth_utils.py` | Password hash/verify functions | 324 |
| `test_db.py` | Database connection/session | 322 |
| `test_user_model.py` | User SQLAlchemy model | 461 |
| `test_user_model_session.py` | User session ID field | 672 |
| `test_login_api.py` | Login endpoint | 1010 |
| `test_login_updates.py` | Login flow updates (Remember Me) | 1704 |
| `test_registration_api.py` | Registration endpoint | 1689 |
| `test_admin_approval_api.py` | Admin approval endpoint | 2949 |
| `test_session_api.py` | Session status/concurrency | 5099 |
| `test_frontend_scaffolding.py` | Frontend file existence checks | 733 |
| `test_dashboard_scaffolding.py` | Dashboard HTML structure | 2931 |
| `test_dashboard_components.py` | Dashboard widget verification | 1982 |
| `test_integration.py` | End-to-end flow | 989 |

### Naming Convention
- Files: `test_<feature_or_module>.py`
- Phase-prefixed: `test_phase<N>_<area>.py` for scaffolding validation
- Functions: `test_<behavior>()` (standard pytest convention)

## Fixture Pattern

### `conftest.py` provides:

```python
# Module-scoped fixtures (shared across test module):

@pytest.fixture(scope="module")
def test_db():
    """Creates test DB, seeds admin user, yields session, cleans up."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    # Seed admin user (username="admin", staff="ADMIN000")
    # ...
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client(test_db):
    """FastAPI TestClient with overridden DB dependency."""
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]
```

**Key pattern:** A `SessionManager` class holds the shared `db` reference for the `get_db` override.

### Test Database
- Separate `test.db` SQLite file (not in-memory)
- Full schema created/dropped per module
- Admin user pre-seeded for authenticated tests

## Testing Patterns

### API Tests
```python
# Standard API test pattern:
def test_login_success(client, test_db):
    response = client.post("/api/v1/login", json={
        "username": "ADMIN000",
        "password": "adminpass"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
```

### Frontend Tests
- File existence checks (`os.path.exists()`)
- HTML content parsing (string matching or basic structure checks)
- No browser-based tests (no Playwright/Selenium)

### Mocking
- No mocking framework (no `unittest.mock` usage observed)
- DB dependency override via `app.dependency_overrides` instead of mocking
- Real SQLite database used for all test data

## Coverage

- **Target:** >80% (per `conductor/workflow.md`)
- **Command:** `pytest --cov=app --cov-report=html`
- **Current status:** `.coverage` file exists (53 KB) — coverage has been run
- **Coverage scope:** `app/` module (auth_utils, token_utils, schemas, main)

## Gaps & Notes

1. **No dedicated API module tests** — `api/v1/auth.py` tested via integration (TestClient) not unit tests
2. **No frontend JS tests** — No Jest, Vitest, or browser testing setup
3. **Module-scoped fixtures** may cause test ordering issues (shared state across tests)
4. **`test.db` file** persists on disk — could cause stale state if tests crash
5. **No CI pipeline** — Tests run manually only
6. **No test for charting helper** — `charting-helper.js` has zero test coverage
7. **Phase-prefixed tests** validate scaffolding only — could be removed once code matures
