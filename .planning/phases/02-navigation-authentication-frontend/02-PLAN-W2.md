---
wave: 2
depends_on:
  - 02-PLAN.md
files_modified:
  - frontend/static/js/dashboard.js
  - frontend/dashboard.html
  - frontend/static/js/users.js
  - frontend/users.html
autonomous: true
requirements_addressed:
  - AUTH-02
  - FLEET-02
---

# Phase 2: Navigation & Authentication (Frontend) — Wave 2

<objective>
Enhance the dashboard and admin users page using the Wave 1 modules. Wire the real hierarchy API, add skeleton loaders, breadcrumbs, approval queue tabs, and align all pages with the tactical dark mode design system.
</objective>

## Task 5: Enhance Dashboard JS with Real API and Tree
<read_first>
- frontend/static/js/dashboard.js
- frontend/static/js/hierarchy-tree.js
- frontend/static/js/breadcrumbs.js
- frontend/static/js/auth-guard.js
- frontend/dashboard.html
- .planning/phases/02-navigation-authentication-frontend/02-CONTEXT.md
</read_first>

<action>
Modify `frontend/static/js/dashboard.js`:
1. Import `requireApprovedUser` from `./auth-guard.js`.
2. Import `renderAccordionTree` from `./hierarchy-tree.js`.
3. Import `BreadcrumbManager` from `./breadcrumbs.js`.
4. At the top of `DOMContentLoaded`, call `const user = await requireApprovedUser()`. If `null`, return early (splash is already showing).
5. Remove the mock `fleetData` array entirely.
6. Replace `renderTree(fleetData, treeContainer)` with:
   a. Show skeleton placeholders in `#sidebar-tree` using Bootstrap `.placeholder-glow` (D-03).
   b. Fetch `GET /api/v1/hierarchy/` with `Authorization: Bearer {token}` header.
   c. On 401: redirect to `/login?reason=expired`.
   d. On success: instantiate `new BreadcrumbManager('breadcrumb-container')`.
   e. Call `renderAccordionTree(data, treeContainer, breadcrumbMgr)`.
   f. Remove skeleton placeholders before rendering.
7. Keep existing logout button, profile menu, sidebar admin link, search shortcut, stats cards, and fleet status widget logic intact.
8. Move `renderTree` function out — replaced by `hierarchy-tree.js`.

Modify `frontend/dashboard.html`:
9. Add a breadcrumb container `<div id="breadcrumb-container" class="px-4 py-2 bg-white border-bottom small"></div>` between the header and main content.
10. Update the sidebar tree section: replace "Loading tree..." text with skeleton placeholders matching Bootstrap Placeholders component.
11. Align color scheme: replace emerald/green variables with design system colors (#020617 background, #0F172A sidebar, #22C55E accents).

</action>

<acceptance_criteria>
- Dashboard fetches `/api/v1/hierarchy/` and renders the real nested tree.
- Skeleton placeholders appear during fetch, replaced by tree on load.
- Breadcrumb container is present and updates when tree nodes expand.
- Unapproved users see approval-pending splash, not the dashboard.
- Existing stats cards, fleet status widget, and session manager still work.
</acceptance_criteria>

## Task 6: Enhance Admin Users Page
<read_first>
- frontend/static/js/users.js
- frontend/users.html
- frontend/static/js/auth-guard.js
- .planning/phases/02-navigation-authentication-frontend/02-CONTEXT.md
</read_first>

<action>
Modify `frontend/static/js/users.js`:
1. Import `requireAdmin` from `./auth-guard.js`.
2. At the top of `DOMContentLoaded`, call `const user = await requireAdmin()`. If `null`, return early.
3. Remove the manual `userRole !== 'admin'` alert check (replaced by `requireAdmin`).
4. Update `approveUser` function to include `Content-Type: application/json` header and send optional `update_data` body (department, role_designation) if admin edits are added later. For now, send empty body `{}`.
5. Keep existing logout, profile menu, token link update, and fetch/render logic.

Modify `frontend/users.html`:
6. Add nav pills tabs: "Awaiting Approval" (active) and "All Users" (future, disabled).
7. Use Signal Green (#22C55E) badge for pending count instead of warning yellow: `badge bg-success-subtle text-success`.
8. Update color scheme to tactical dark mode: dark sidebar (#0F172A), Deep Black background accents.
9. Add breadcrumb container `<div id="breadcrumb-container" class="px-4 py-2 bg-white border-bottom small">` with static text "User Management".

</action>

<acceptance_criteria>
- Users page uses `requireAdmin()` — non-admins redirect to `/dashboard`.
- Pending count badge uses Signal Green styling.
- Approval queue has tab navigation structure.
- Non-approved users see approval-pending splash if they somehow reach this page.
</acceptance_criteria>

## Task 7: Align Register Page
<read_first>
- frontend/register.html
- frontend/static/js/register.js
- design-system/sonar-vault/MASTER.md
</read_first>

<action>
Modify `frontend/register.html`:
1. Update page background to `#020617` (Deep Black).
2. Update card styling: dark card (#0F172A), light text, green submit button (#22C55E).
3. Add "SONAR VAULT" header bar matching login page.
4. Use Fira Code for heading, Fira Sans for body.
5. Keep existing form fields and registration logic intact.

</action>

<acceptance_criteria>
- Register page uses tactical dark mode styling consistent with login page.
- Form fields and registration logic unchanged.
</acceptance_criteria>

## Task 8: Add Backend Session Endpoint
<read_first>
- api/v1/auth.py
- .planning/phases/02-navigation-authentication-frontend/02-CONTEXT.md
</read_first>

<action>
Modify `api/v1/auth.py`:
1. Add `GET /api/v1/me` endpoint that:
   - Requires `current_user = Depends(get_current_user)` (validates token).
   - Returns user object: `{id, username, staff_number, role, is_active, is_approved, department, full_name}`.
   - Use `UserSchema` as response model.
2. This endpoint is needed by `auth-guard.js` to check approval status on page load without relying on stale localStorage data.

</action>

<acceptance_criteria>
- `GET /api/v1/me` returns the authenticated user's full profile.
- Response includes `is_approved` and `role` fields for frontend auth guard.
</acceptance_criteria>

---

<verification>
### Goal-Backward Verification
1. Can users navigate Platform → Project → Subsystem on the dashboard? Confirmed by `renderAccordionTree` rendering real API data.
2. Do breadcrumbs show the current hierarchical path? Confirmed by `BreadcrumbManager.update()` on tree expand events.
3. Does the admin see a green approval queue? Confirmed by Signal Green badge in `users.html`.
4. Are unapproved users blocked from all authenticated pages? Confirmed by `requireApprovedUser()` in dashboard and `requireAdmin()` in users.

### must_haves
- Dashboard tree loads from `/api/v1/hierarchy/` without errors.
- Skeleton placeholders visible during API fetch.
- Login, register, and dashboard pages all use consistent dark theme.
- All existing tests still pass after frontend changes.
</verification>
