# Testing

## Framework & Tooling

| Tool | Purpose | Configuration |
|------|---------|---------------|
| `pytest` | Main test runner | Defaults |
| `pytest-cov` | Coverage reporting | `--cov=app --cov-report=html` |
| `FastAPI TestClient`| Route integration tests | Native Starlette client |
| SQLite | Test Database | `sqlite:///./test.db` (file-based) |

## Test Structure

All tests reside in the `tests/` root directory using a flat structure.

### File Naming
- Functional/Unit Tests: `test_<module_or_feature>.py` (e.g., `test_login_api.py`)
- Scaffolding/Bootstrap Tests: `test_phase<N>_<focus>.py` (e.g., `test_phase1_bootstrap.py`)

### Current Test Manifest (18 Files)
- **API/Integration:** `test_login_api.py`, `test_registration_api.py`, `test_admin_approval_api.py`, `test_session_api.py`, `test_integration.py`
- **Models/DB:** `test_user_model.py`, `test_user_model_session.py`, `test_db.py`
- **Utils:** `test_auth_utils.py`
- **Scaffolding:** `test_phase*`, `test_frontend_scaffolding.py`, `test_dashboard_scaffolding.py`, `test_dashboard_components.py`

## Fixtures & Database Pattern

The `tests/conftest.py` file manages shared global configurations:

### `test_db` Fixture
Module-scoped database lifecycle:
1. Creates total schema (`Base.metadata.create_all()`)
2. Seeds initial data (e.g., `ADMIN000` user)
3. Yields session to tests
4. Drops schema after module execution (`Base.metadata.drop_all()`)

### `client` Fixture
Provides the `TestClient` while overriding FastAPI dependencies:
- Overrides `get_db` to inject the test database session.

## Coverage Requirements

- **Minimum Threshold:** >80% statement coverage for all application modules.
- **Validation:** Enforced as a Quality Gate in `conductor/workflow.md`.

## Deficits & Gaps

1. **JavaScript Testing:** Complete absence of frontend JS testing (no Jest/Vitest). Complex logic in `dashboard.js` and `charting-helper.js` is untested.
2. **Missing Unit Tests:** Route handlers (`api/v1/auth.py`) lack isolated unit tests (heavily reliant on `TestClient` integration scope).
3. **Fixture State Leakage:** Module-scoped database lifecycles could introduce cross-test state contamination if modifications aren't carefully managed.
4. **Mocking:** No usage of `unittest.mock` for external constraints or isolation.
