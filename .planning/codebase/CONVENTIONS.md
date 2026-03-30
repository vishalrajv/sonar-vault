# Code Conventions

## Code Style Guides
This project strictly adheres to the official Google Style Guides, summarized in `conductor/code_styleguides/`. All code must comply with these guidelines.

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
Follow conventional commits: `<type>(<scope>): <description>`
Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.

### Workflow (`conductor/workflow.md`)
1. Track everything in `plan.md`.
2. Follow TDD: Red → Green → Refactor.
3. Validate tests and coverage (>80%).
4. Document architectural deviations in `tech-stack.md`.
5. Attach task summary via `git notes`.
