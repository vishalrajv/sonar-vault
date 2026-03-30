# Code Conventions

## Python Backend

### Code Style
- Standard Python formatting, no formatter enforced (no black/ruff config found)
- 4-space indentation
- Single quotes and double quotes mixed (no strict preference observed)
- Type hints used on function signatures: `def hash_password(password: str) -> str:`
- Docstrings present on route handlers (one-line style)

### Import Organization
```python
# Pattern observed in api/v1/auth.py:
from fastapi import APIRouter, Depends, HTTPException, status, Query  # Framework
from fastapi.security import OAuth2PasswordBearer                     # Framework extensions
from sqlalchemy.orm import Session                                     # ORM
from datetime import timedelta                                         # Stdlib
from jose import JWTError, jwt                                         # Third-party
from database.db import get_db                                         # Internal
from models.user import User                                            # Internal models
from app.schemas import UserLogin, Token, UserRegister, UserSchema     # Internal schemas
from app.auth_utils import verify_password, hash_password              # Internal utils
```

### Dependency Injection
- FastAPI `Depends()` used for DB sessions and auth guards
- Chained dependencies: `get_current_user` → `get_current_active_user` → `get_current_admin_user`
- DB session scoped per request via generator pattern

### Error Handling
- `HTTPException` raised directly in route handlers
- Status codes used correctly (`401`, `403`, `400`, `404`, `201`)
- Custom error messages in `detail` field
- No global exception handlers configured
- `WWW-Authenticate: Bearer` headers on 401 responses

### Model Patterns
```python
# SQLAlchemy model pattern (models/user.py):
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    # ...
    def __repr__(self):
        return f"<User(username='{self.username}')>"
```

### Schema Patterns
```python
# Pydantic schema pattern (app/schemas.py):
class UserSchema(BaseModel):
    id: int
    username: str
    model_config = ConfigDict(from_attributes=True)  # SQLAlchemy compat
```

## JavaScript Frontend

### Module System
- **ES Modules** for complex pages: `dashboard.js`, `users.js`, `session-manager.js`, `charting-helper.js`
  - Use `import`/`export` syntax
  - Loaded with `<script type="module">`
- **Traditional scripts** for simple pages: `login.js`, `register.js`
  - No module system, loaded with `<script src="...">`

### Event Handling Pattern
```javascript
// Consistent DOMContentLoaded wrapper:
document.addEventListener('DOMContentLoaded', async () => {
    // Page initialization
    const sessionManager = new SessionManager();
    // ...
});
```

### API Communication Pattern
```javascript
// fetch()-based with consistent error handling:
const response = await fetch('/api/v1/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password, remember_me: rememberMe }),
});
const data = await response.json();
if (response.ok) { /* success */ }
else { /* show error from data.detail */ }
```

### State Management
- **localStorage** for auth state: `access_token`, `token_type`, `user_role`, `user_full_name`, `user_department`
- Token passed via query param for server-side auth on page routes
- Links dynamically updated with `?token=` on authenticated pages

### DOM Manipulation
- Direct `document.getElementById()` / `querySelector()` usage
- Template literals for dynamic HTML rendering (no templating library)
- Bootstrap classes for show/hide (`d-none`, `hidden` attribute)

## HTML/CSS

### Page Structure
- All HTML pages are self-contained with full `<!DOCTYPE html>` structure
- Each page includes Bootstrap CSS + JS from local vendor path
- Custom CSS variables via `:root` on pages requiring theming:
```css
:root {
    --sv-emerald-900: #064e3b;
    --sv-emerald-600: #059669;
    /* ... */
}
```

### Component Patterns
- Sidebar + main content layout on authenticated pages
- Bootstrap card components for forms and widgets
- SVG icons inline (no icon library)
- Placeholder loading states using Bootstrap `.placeholder-glow`

### Theming
- Emerald-based color scheme (Sonar Vault brand)
- Custom utility classes: `.bg-sv-sidebar`, `.text-sv-emerald-400`, `.btn-sv-primary`
- Theme CSS duplicated across `dashboard.html` and `users.html` (not extracted to shared file)

## Commit & Workflow Conventions

### Commit Message Format
```
<type>(<scope>): <description>
```
Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### TDD Workflow (from `conductor/workflow.md`)
1. Write failing tests (Red)
2. Implement to pass (Green)
3. Refactor
4. Verify coverage (>80% target)
5. Document deviations in `tech-stack.md`
6. Commit with conventional message
7. Attach task summary via `git notes`

### Quality Gates
- All tests passing
- Code coverage >80%
- Code follows style guides in `conductor/code_styleguides/`
- No hardcoded secrets
- Input validation present
