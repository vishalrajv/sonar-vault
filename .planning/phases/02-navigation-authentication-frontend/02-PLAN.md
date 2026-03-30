---
wave: 1
depends_on: []
files_modified:
  - frontend/static/js/auth-guard.js
  - frontend/static/js/hierarchy-tree.js
  - frontend/static/js/breadcrumbs.js
  - frontend/static/js/login.js
autonomous: true
requirements_addressed:
  - AUTH-02
  - FLEET-02
---

# Phase 2: Navigation & Authentication (Frontend) — Wave 1

<objective>
Create the standalone JS modules (auth-guard, hierarchy-tree, breadcrumbs) and enhance the login flow with approval-pending handling. These modules have no cross-dependencies and serve as the foundation for Wave 2.
</objective>

## Task 1: Create Auth Guard Module
<read_first>
- frontend/static/js/login.js
- frontend/static/js/session-manager.js
- .planning/phases/02-navigation-authentication-frontend/02-CONTEXT.md
- .planning/phases/02-navigation-authentication-frontend/02-RESEARCH.md
</read_first>

<action>
Create `frontend/static/js/auth-guard.js`:
1. Export an async function `requireAuth(requireAdmin = false)` that:
   - Reads `access_token` from `localStorage`.
   - If missing, redirects to `/login?reason=no_token` and returns `null`.
   - Fetches `/api/v1/session/status` with `Authorization: Bearer {token}` header.
   - On 401: clears `localStorage`, redirects to `/login?reason=expired`, returns `null`.
   - On network error: redirects to `/login?reason=network`, returns `null`.
   - On success: returns the user object `{username, staff_number, role, is_active, is_approved}`.
2. Export an async function `requireApprovedUser()` that:
   - Calls `requireAuth()`.
   - If user is not `is_approved`, calls `showApprovalPendingSplash(user)` and returns `null`.
   - Otherwise returns the user.
3. Export function `showApprovalPendingSplash(user)` that:
   - Replaces `document.body.innerHTML` with a centered, non-dismissible splash screen.
   - Uses tactical dark mode styling (#020617 background, Fira Code heading).
   - Shows staff number, "Awaiting Admin Approval" heading, and "Status: Pending" badge.
   - Includes a logout button that clears localStorage and redirects to `/login`.
4. Export function `requireAdmin()` that:
   - Calls `requireApprovedUser()`.
   - If user role is not `admin`, redirects to `/dashboard` and returns `null`.
   - Otherwise returns the user.

</action>

<acceptance_criteria>
- `frontend/static/js/auth-guard.js` exists and exports `requireAuth`, `requireApprovedUser`, `showApprovalPendingSplash`, `requireAdmin`.
- Unapproved users see the approval-pending splash instead of page content.
- Missing/expired tokens redirect to login with a reason query param.
</acceptance_criteria>

## Task 2: Create Hierarchy Tree Module
<read_first>
- frontend/static/js/dashboard.js
- frontend/dashboard.html
- design-system/sonar-vault/MASTER.md
- .planning/phases/02-navigation-authentication-frontend/02-RESEARCH.md
</read_first>

<action>
Create `frontend/static/js/hierarchy-tree.js`:
1. Export a function `renderAccordionTree(data, container, breadcrumbMgr)` that:
   - Takes an array of Platform objects (each with `projects`, each project with `subsystems`).
   - Takes a container DOM element to render into.
   - Takes an optional `breadcrumbMgr` instance for breadcrumb sync.
   - Recursively generates Bootstrap 5.3.3 accordion markup.
2. Node ID generation: use composite key `collapse-{nodeId}-{level}-{index}` for every collapse element to avoid nested accordion ID collisions (per research Pitfall 1).
3. Platform nodes (level 0): accordion-button with platform info SVG icon, expandable.
4. Project nodes (level 1): accordion-button with folder SVG icon, nested under platform, expandable.
5. Subsystem nodes (level 2): leaf div with cog SVG icon, not expandable, clickable.
6. Empty nodes (no children): render as non-expandable leaf with grayed-out "No Active Builds" badge (D-04).
7. ARIA attributes on every node: `aria-expanded`, `aria-controls`, `aria-level={level+1}`, `role="treeitem"` on leaves.
8. On expand (`show.bs.collapse` event): update breadcrumb via `breadcrumbMgr.update(path)` if provided.
9. Decorative SVG icons must have `aria-hidden="true"`.
10. Use `document.createElement` for tree structure; `innerHTML` only for leaf content.
11. Export a helper `getNodeIcon(type)` returning the appropriate Heroicon SVG path string for 'Platform', 'Project', 'Subsystem'.

</action>

<acceptance_criteria>
- `frontend/static/js/hierarchy-tree.js` exists and exports `renderAccordionTree` and `getNodeIcon`.
- Renders nested Bootstrap accordion markup with unique composite IDs per node.
- Empty nodes show "No Active Builds" grayed-out label.
- ARIA tree roles and `aria-level` are present on all nodes.
</acceptance_criteria>

## Task 3: Create Breadcrumbs Module
<read_first>
- frontend/dashboard.html
- design-system/sonar-vault/MASTER.md
- .planning/phases/02-navigation-authentication-frontend/02-RESEARCH.md
</read_first>

<action>
Create `frontend/static/js/breadcrumbs.js`:
1. Export a class `BreadcrumbManager` with:
   - `constructor(containerId)`: stores reference to `document.getElementById(containerId)`, initializes `this.path = []`.
   - `update(newPath)`: sets `this.path` to `newPath` array, calls `this.render()`.
   - `render()`: generates Bootstrap 5.3.3 breadcrumb markup inside the container.
   - Home icon as first breadcrumb item (Heroicon home SVG, links to root).
   - Each path segment as a `breadcrumb-item`. Last item has class `active` and `aria-current="page"`.
   - Non-last items are clickable links with `text-success` styling.
   - Clear method `clear()` that resets path to `[]` and re-renders showing only home.

</action>

<acceptance_criteria>
- `frontend/static/js/breadcrumbs.js` exists and exports `BreadcrumbManager` class.
- Breadcrumb renders Bootstrap `.breadcrumb` markup with home icon and path segments.
- Last segment is marked `active` with `aria-current="page"`.
</acceptance_criteria>

## Task 4: Enhance Login Flow
<read_first>
- frontend/static/js/login.js
- frontend/login.html
- frontend/static/js/auth-guard.js
- .planning/phases/02-navigation-authentication-frontend/02-CONTEXT.md
</read_first>

<action>
Modify `frontend/static/js/login.js`:
1. On successful login response, store `access_token`, `token_type`, `user_role`, `user_full_name`, `user_department` in localStorage (already done).
2. After storing, redirect to `/dashboard?token={access_token}` (already done).
3. Add handling for `?reason=` query param on the login page:
   - `reason=logout`: show info message "You have been logged out."
   - `reason=expired`: show warning message "Session expired. Please log in again."
   - `reason=timeout`: show warning message "Session timed out due to inactivity."
   - `reason=no_token`: show info message "Please log in to continue."
   - `reason=network`: show danger message "Network error. Please check your connection."
4. Display the reason message in the existing `#error-message` div (use appropriate Bootstrap alert classes: `alert-info`, `alert-warning`, `alert-danger`).

Modify `frontend/login.html`:
5. Add dark theme header bar with "SONAR VAULT" branding (matching dashboard sidebar style).
6. Update page background to `#020617` (Deep Black from design system).
7. Update card styling: dark card background (#0F172A), light text, green accent on submit button (#22C55E).
8. Use Fira Code for heading, Fira Sans for body (add font import or reference bundled fonts).

</action>

<acceptance_criteria>
- Login page displays contextual messages based on `?reason=` query param.
- Login page uses tactical dark mode styling consistent with the design system.
- Successful login still stores token and redirects to dashboard.
</acceptance_criteria>

---

<verification>
### Goal-Backward Verification
1. Can an unapproved user see the approval-pending splash? Confirmed by `auth-guard.js` `showApprovalPendingSplash()`.
2. Does the tree renderer avoid nested accordion ID collisions? Confirmed by composite ID pattern `collapse-{id}-{level}-{index}`.
3. Do breadcrumbs update when a tree node expands? Confirmed by `show.bs.collapse` event calling `breadcrumbMgr.update(path)`.

### must_haves
- `auth-guard.js` is importable as ES module from dashboard.js and users.js.
- `hierarchy-tree.js` renders without errors when given the API payload shape.
- Login page reason messages display correctly for all 5 reason values.
</verification>
