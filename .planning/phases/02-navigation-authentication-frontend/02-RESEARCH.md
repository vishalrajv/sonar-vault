# Phase 2: Navigation & Authentication (Frontend) - Research

**Researched:** 2026-03-31
**Domain:** Vanilla JS hierarchical tree navigation, Bootstrap 5.3.3 accordion nesting, WAI-ARIA tree view accessibility
**Confidence:** HIGH

## Summary

This phase requires building three distinct frontend experiences: (1) authentication flows (login/register with approval-pending feedback), (2) an admin approval dashboard, and (3) a recursive 3-level hierarchical tree sidebar for Platforms → Projects → Subsystems. The project is 100% offline with Bootstrap 5.3.3 bundled locally and no CDN dependencies.

The core technical challenge is the recursive tree sidebar. Bootstrap 5.3.3's accordion component supports nesting, but nested accordions require unique ID generation per level and careful `data-bs-parent` scoping to prevent parent panels from collapsing when child panels toggle. For accessibility, the W3C WAI-ARIA Tree View Pattern (APG) and GitHub's 2025 deep-dive on accessible tree views provide the authoritative guidance: use semantic `ul/li` elements with `role="tree/treeitem/group"`, `aria-expanded`, and a roving `tabindex` approach.

**Primary recommendation:** Use Bootstrap 5.3.3 Collapse for expand/collapse animation, but generate accordion markup via a recursive vanilla JS function that creates unique IDs per node. Apply WAI-ARIA tree roles on top of semantic HTML. Use the existing `renderTree()` function in `dashboard.js` as the starting point and enhance it with Bootstrap Collapse, ARIA attributes, keyboard navigation, and skeleton loading states.

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** **Accordion Sidebar.** Use a nested vertical navigation menu (Bootstrap 5.3.3 compatible) to represent the deep Platform-Project-Subsystem hierarchy.
- **D-02:** **Persistent Breadcrumbs.** Maintain a visual path (e.g., `Platforms / Ship Alpha / Project X`) to ground the user in their current hierarchical location.
- **D-03:** **Skeleton Loaders.** Use pulse skeleton components in the dashboard area while the "Full Nested Payload" is being parsed on initial load.
- **D-04:** **Grayed-out Placeholders.** If a Platform or Project has no uploaded software versions (Phase 3 content), still display the node in the tree but with a grayed-out "No Active Builds" label.
- **D-05:** **Approval Pending Splash.** Users who are authenticated but not yet approved by an admin (per Phase 1 logic) see a non-dismissible status message instead of the dashboard.
- **D-06:** **Approval Queue Tab.** The `users.html` view will feature a prioritized "Awaiting Approval" tab using Signal Green badges (`#22C55E`) for clear actionable identification.
- **D-07:** **Tactical Dark Mode.** Follow `design-system/sonar-vault/MASTER.md` for a high-contrast, Deep Black (#020617) and Midnight Blue (#0F172A) aesthetic.
- **D-08:** **Signal Accents.** Use Signal Green (#22C55E) exclusively for positive actions, approvals, and verified builds.
- **D-09:** **Information Density.** Adopt a **Bento Grid** layout for the dashboard to allow simultaneous viewing of hierarchy nav and version metadata without clutter.

### the agent's Discretion
- Specific Bootstrap component choices for the accordion and data tables.
- SVG icon selection from the Heroicons set.

### Deferred Ideas (OUT OF SCOPE)
- (None explicitly listed in CONTEXT.md)
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| AUTH-01 | User can create account with staff number and wait for admin approval | Register form pattern exists; approval-pending splash is D-05 |
| AUTH-02 | User can log in with staff number and password | Login form exists; needs approval-status check post-login |
| FLEET-01 | System maintains Platform → Project → Subsystem hierarchical tree | Backend API `GET /api/v1/hierarchy/` returns nested payload; recursive rendering pattern researched |
| FLEET-02 | Users can navigate the hierarchical tree recursively to view versions | Accordion sidebar (D-01), breadcrumbs (D-02), ARIA tree view pattern |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Bootstrap | 5.3.3 (bundled) | CSS framework, Collapse/accordion animation, grid, utilities | Already bundled in `frontend/static/vendor/bootstrap/`; project constraint |
| Vanilla JS (ES Modules) | ES2020+ | Application logic, DOM manipulation, recursive rendering | No-framework constraint; `type="module"` already used in dashboard.js/users.js |
| Fira Code + Fira Sans | Latest | Typography (headings + body) | Design system locked in MASTER.md |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| Bootstrap Collapse | 5.3.3 (bundled) | Expand/collapse animation for accordion tree | All tree node expand/collapse |
| Bootstrap Breadcrumb | 5.3.3 (bundled) | Hierarchical path display | D-02 persistent breadcrumbs |
| Bootstrap Placeholders | 5.3.3 (bundled) | Skeleton loading states | D-03 skeleton loaders during API fetch |
| Bootstrap Nav Pills | 5.3.3 (bundled) | Tab navigation for admin approval queue | D-06 approval queue tabs |
| Heroicons (inline SVG) | 2.x | Icons for tree nodes, nav, actions | All iconography per design system |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Bootstrap Collapse for tree | Custom CSS transitions | Loses built-in accessibility, event system, animation timing |
| Full WAI-ARIA tree role | Disclosure pattern (simpler) | W3C APG warns tree role is overkill for typical nav; but this project has strict hierarchy requirements and keyboard nav is needed for operator efficiency |
| CSS-only accordion | JS-driven accordion | Cannot support dynamic data loading, breadcrumb sync, or keyboard navigation |
| Third-party tree library | Roll our own | Adds dependency; offline constraint means no CDN; our 3-level fixed hierarchy is simple enough |

**Installation:** N/A — Bootstrap is already bundled. No npm/package.json exists. All JS is vanilla ES modules served as static files.

## Architecture Patterns

### Recommended Project Structure (Frontend Files)
```
frontend/
├── index.html              # Auth redirect (exists)
├── login.html              # Login form (exists, needs enhancement)
├── register.html           # Registration form (exists)
├── dashboard.html          # Main dashboard + sidebar tree (exists, needs enhancement)
├── users.html              # Admin approval queue (exists, needs enhancement)
├── static/
│   ├── vendor/bootstrap/   # Bootstrap 5.3.3 (exists)
│   ├── js/
│   │   ├── login.js        # Login logic (exists)
│   │   ├── register.js     # Registration logic (exists)
│   │   ├── dashboard.js    # Dashboard + tree renderer (exists, needs major enhancement)
│   │   ├── users.js        # Admin approval logic (exists, needs enhancement)
│   │   ├── session-manager.js  # Idle timeout (exists)
│   │   ├── charting-helper.js  # SVG charts (exists, may be deprecated)
│   │   ├── hierarchy-tree.js   # NEW: Extracted recursive tree module
│   │   ├── breadcrumbs.js      # NEW: Breadcrumb state manager
│   │   └── auth-guard.js       # NEW: Shared auth + approval check
│   └── images/
```

### Pattern 1: Recursive Accordion Tree Renderer
**What:** A function that takes a nested data payload and recursively generates Bootstrap accordion markup with unique IDs per node.
**When to use:** Rendering the Platform → Project → Subsystem hierarchy in the sidebar.
**Example:**
```javascript
// Generates nested Bootstrap 5.3.3 accordion with unique IDs
// Source: Bootstrap docs https://getbootstrap.com/docs/5.3/components/accordion/
function renderAccordionTree(data, container, level = 0, parentPath = []) {
  const accordionId = `accordion-level-${level}-${Date.now()}`;

  data.forEach((item, index) => {
    const collapseId = `collapse-${item.id}-${level}-${index}`;
    const hasChildren = (item.projects && item.projects.length > 0) ||
                        (item.subsystems && item.subsystems.length > 0);
    const children = item.projects || item.subsystems || [];
    const currentPath = [...parentPath, item.name];

    const itemEl = document.createElement('div');
    itemEl.className = 'accordion-item border-0';

    if (hasChildren) {
      // Parent node: accordion header + collapse body
      itemEl.innerHTML = `
        <h${Math.min(level + 3, 6)} class="accordion-header" id="heading-${collapseId}">
          <button class="accordion-button collapsed py-2 px-3 small"
                  type="button"
                  data-bs-toggle="collapse"
                  data-bs-target="#${collapseId}"
                  aria-expanded="false"
                  aria-controls="${collapseId}"
                  data-path="${currentPath.join(' > ')}">
            ${getNodeIcon(item.type || getItemType(level))}
            <span class="ms-2">${item.name}</span>
          </button>
        </h${Math.min(level + 3, 6)}>
        <div id="${collapseId}" class="accordion-collapse collapse"
             aria-labelledby="heading-${collapseId}">
          <div class="accordion-body p-0 ps-3">
            <!-- Children rendered recursively here -->
          </div>
        </div>
      `;

      const childContainer = itemEl.querySelector('.accordion-body');
      renderAccordionTree(children, childContainer, level + 1, currentPath);
    } else {
      // Leaf node: no accordion, just clickable item
      itemEl.innerHTML = `
        <div class="d-flex align-items-center gap-2 px-3 py-2 rounded-3
                    cursor-pointer small text-white-50 hover-bg-dark transition-all"
             role="treeitem"
             data-path="${currentPath.join(' > ')}"
             data-id="${item.id}"
             tabindex="-1">
          ${getNodeIcon('subsystem')}
          <span class="ms-2">${item.name}</span>
        </div>
      `;
    }

    container.appendChild(itemEl);
  });
}
```

### Pattern 2: Breadcrumb State Manager
**What:** A reactive breadcrumb component that updates based on the last-clicked tree node path.
**When to use:** Always visible above the main content area, showing `Platforms > Ship Alpha > Project X`.
**Example:**
```javascript
// Breadcrumb manager that syncs with tree navigation
class BreadcrumbManager {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.path = [];
  }

  update(newPath) {
    this.path = newPath;
    this.render();
  }

  render() {
    if (!this.container) return;
    this.container.innerHTML = `
      <nav aria-label="breadcrumb">
        <ol class="breadcrumb mb-0">
          <li class="breadcrumb-item">
            <a href="#" class="text-success text-decoration-none" data-index="0">
              <svg width="16" height="16" fill="none" stroke="currentColor"
                   viewBox="0 0 24 24" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round"
                      stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7..." />
              </svg>
            </a>
          </li>
          ${this.path.map((segment, i) => `
            <li class="breadcrumb-item ${i === this.path.length - 1 ? 'active' : ''}"
                ${i === this.path.length - 1 ? 'aria-current="page"' : ''}>
              ${i === this.path.length - 1 ? segment :
                `<a href="#" class="text-success text-decoration-none"
                    data-index="${i + 1}">${segment}</a>`}
            </li>
          `).join('')}
        </ol>
      </nav>
    `;
  }
}
```

### Pattern 3: Auth Guard with Approval Check
**What:** Shared module that checks token validity AND approval status, redirecting unapproved users to a pending splash.
**When to use:** Every authenticated page (dashboard, users) loads this before rendering content.
**Example:**
```javascript
// auth-guard.js — runs before page content renders
export async function requireAuth(requireAdmin = false) {
  const token = localStorage.getItem('access_token');
  if (!token) {
    window.location.href = '/login?reason=no_token';
    return null;
  }

  try {
    const response = await fetch('/api/v1/me', {
      headers: { 'Authorization': `Bearer ${token}` }
    });

    if (!response.ok) {
      localStorage.clear();
      window.location.href = '/login?reason=expired';
      return null;
    }

    const user = await response.json();

    if (!user.is_approved) {
      // Show approval-pending splash instead of content (D-05)
      showApprovalPendingSplash(user);
      return null;
    }

    if (requireAdmin && user.role !== 'admin') {
      window.location.href = '/dashboard';
      return null;
    }

    return user;
  } catch (e) {
    window.location.href = '/login?reason=network';
    return null;
  }
}
```

### Anti-Patterns to Avoid
- **Don't use `data-bs-parent` on nested accordions without unique IDs:** Bootstrap's `data-bs-parent` uses `querySelector`. If inner accordion collapse elements match the outer parent selector, clicking an inner item will close the outer panel. Fix: each accordion level needs its own unique container ID.
- **Don't use `innerHTML` for the entire tree at once:** Build DOM nodes with `createElement` for the tree structure, then use `innerHTML` only for leaf content. This preserves event listeners on parent containers.
- **Don't use the full WAI-ARIA `tree` role if not implementing keyboard nav:** Per W3C APG, the disclosure pattern is simpler and sufficient if arrow-key navigation isn't needed. Since operators need keyboard efficiency, implement the full tree pattern with roving tabindex.
- **Don't forget `aria-hidden="true"` on decorative SVG icons:** Screen readers will announce SVG content otherwise (per GitHub's 2025 tree view accessibility guide).
- **Don't hardcode tree depth:** The recursive function must handle any nesting level, even though the current schema is fixed at 3 levels.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Expand/collapse animation | Custom CSS height transitions with JS measurement | Bootstrap Collapse (`bootstrap.Collapse`) | Handles max-height calculation, transition timing, `collapsing` class management, event dispatch, and `prefers-reduced-motion` automatically |
| Skeleton loading placeholders | Custom shimmer CSS animation | Bootstrap Placeholders (`.placeholder-glow`, `.placeholder`) | Already bundled, consistent with design system, supports responsive sizing |
| Breadcrumb separators | Custom CSS ::before pseudo-elements | Bootstrap Breadcrumb (`.breadcrumb`, `.breadcrumb-item`) | Auto-generates separators, supports `aria-current`, responsive |
| Icon set | Custom drawn SVGs | Heroicons (inline SVG, MIT license) | Consistent design language, already partially used in existing code |
| Idle session timeout | Custom `setTimeout` polling | Existing `session-manager.js` | Already implemented and working |
| Form validation | Custom regex/error display | HTML5 validation attrs + Bootstrap `.is-invalid` / `.invalid-feedback` | Native browser support, accessible by default |

**Key insight:** Bootstrap 5.3.3 already solves the animation, layout, and accessibility infrastructure for accordions, breadcrumbs, skeletons, and forms. Hand-roll only the **data-to-DOM mapping** (recursive tree renderer) and **state management** (breadcrumb sync, auth guard).

## Common Pitfalls

### Pitfall 1: Nested Accordion ID Collisions
**What goes wrong:** When generating nested Bootstrap accordions dynamically, if IDs are not globally unique, clicking an inner accordion button can trigger collapse on outer panels or fail entirely.
**Why it happens:** Bootstrap's Collapse uses `document.querySelector(data-bs-target)`. If two collapse elements share an ID, only the first is found. Also, `data-bs-parent` matching is too broad if IDs overlap.
**How to avoid:** Generate IDs using a composite key: `collapse-{nodeId}-{level}-{index}`. Never use just the database ID alone.
**Warning signs:** Clicking a subsystem collapses the parent platform; console errors about missing elements.

### Pitfall 2: Event Bubbling on Nested Clicks
**What goes wrong:** Clicking a child accordion button also triggers the parent accordion's click handler, causing immediate open-then-close behavior.
**Why it happens:** Without `e.stopPropagation()`, click events bubble from inner buttons to outer accordion headers.
**How to avoid:** Rely on Bootstrap's own event handling (it checks `data-bs-target` specificity). If building custom click handlers alongside Bootstrap, call `e.stopPropagation()` on child handlers.
**Warning signs:** Accordion items flash open then immediately close.

### Pitfall 3: Missing `aria-level` on Recursive Tree Items
**What goes wrong:** Screen readers cannot determine the nesting depth of tree items. Users hear "list item" without knowing if it's a Platform, Project, or Subsystem.
**Why it happens:** Browsers are not required to compute `aria-level` from DOM nesting. GitHub's 2025 research confirmed this gap across multiple assistive technologies.
**How to avoid:** Explicitly set `aria-level={level+1}` on each treeitem. The W3C APG and GitHub's guide both recommend this.
**Warning signs:** Screen reader testing with NVDA/JAWS shows no depth information.

### Pitfall 4: Focus Loss After Collapse
**What goes wrong:** When a parent accordion collapses, keyboard focus is lost (moves to `<body>`), forcing the user to Tab back into the sidebar.
**Why it happens:** Bootstrap Collapse removes the container from the DOM layout. If focus was inside the collapsing element, it has nowhere to go.
**How to avoid:** Listen for `hidden.bs.collapse` event and programmatically move focus to the accordion header button. Use roving tabindex pattern so focus management is explicit.
**Warning signs:** Keyboard-only users lose their place after collapsing a section.

### Pitfall 5: Full Nested Payload Blocking the Main Thread
**What goes wrong:** If the hierarchy has many platforms/projects, rendering the entire tree synchronously blocks the UI, causing a visible freeze.
**Why it happens:** The existing code calls `renderTree(fleetData, treeContainer)` synchronously. With a full payload, this creates hundreds of DOM elements at once.
**How to avoid:** Show skeleton placeholders immediately, fetch the payload, then render incrementally using `requestAnimationFrame` batching or `DocumentFragment` to minimize reflows. For this project's scale (~10-50 nodes max), synchronous rendering is acceptable but show skeletons during the fetch.
**Warning signs:** Dashboard appears frozen for 1-2 seconds after login.

### Pitfall 6: Token Expiry During Long Sessions
**What goes wrong:** User navigates the tree, clicks a subsystem, but the API call fails silently because the JWT expired.
**Why it happens:** The existing auth pattern stores token in localStorage but only checks on page load. Tree navigation doesn't trigger page loads.
**How to avoid:** Wrap all API calls (including hierarchy fetch) in a try/catch that detects 401 responses and redirects to login. The existing `session-manager.js` handles idle timeout but not JWT expiration.
**Warning signs:** Silent failures when clicking tree nodes after extended sessions.

## Code Examples

### Recursive Tree Rendering with Bootstrap Collapse
```javascript
// Source: Bootstrap 5.3.3 Accordion docs
// https://getbootstrap.com/docs/5.3/components/accordion/
// Enhanced with unique ID generation and ARIA attributes

/**
 * Render a hierarchical tree using Bootstrap 5.3.3 accordion components.
 * @param {Array} data - Array of node objects with nested children
 * @param {HTMLElement} container - DOM element to render into
 * @param {number} level - Current nesting depth (0 = platform)
 * @param {BreadcrumbManager} breadcrumbMgr - Breadcrumb updater
 */
function renderHierarchyTree(data, container, level = 0, breadcrumbMgr) {
  data.forEach((item, index) => {
    const children = item.projects || item.subsystems || [];
    const hasChildren = children.length > 0;
    const nodeId = item.id;
    const uniqueId = `sv-${level}-${nodeId}-${index}`;
    const collapseId = `collapse-${uniqueId}`;
    const headingId = `heading-${uniqueId}`;
    const itemType = level === 0 ? 'Platform' : level === 1 ? 'Project' : 'Subsystem';

    const itemEl = document.createElement('div');
    itemEl.className = 'sv-tree-node';

    if (hasChildren) {
      itemEl.innerHTML = `
        <div class="accordion accordion-flush" id="accordion-${uniqueId}">
          <div class="accordion-item border-0">
            <h3 class="accordion-header" id="${headingId}">
              <button class="accordion-button collapsed py-2 px-3 small text-white-50
                              bg-transparent shadow-none"
                      type="button"
                      data-bs-toggle="collapse"
                      data-bs-target="#${collapseId}"
                      aria-expanded="false"
                      aria-controls="${collapseId}"
                      data-node-id="${nodeId}"
                      data-node-name="${item.name}"
                      data-node-type="${itemType}">
                <svg class="text-success flex-shrink-0" width="16" height="16"
                     fill="none" stroke="currentColor" viewBox="0 0 24 24"
                     aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round"
                        stroke-width="2" d="${getIconPath(itemType)}" />
                </svg>
                <span class="ms-2 text-truncate">${item.name}</span>
              </button>
            </h3>
            <div id="${collapseId}" class="accordion-collapse collapse"
                 aria-labelledby="${headingId}">
              <div class="accordion-body p-0 ps-2 ms-2 border-start
                          border-secondary border-opacity-25">
              </div>
            </div>
          </div>
        </div>
      `;

      // Render children recursively
      const childContainer = itemEl.querySelector('.accordion-body');
      renderHierarchyTree(children, childContainer, level + 1, breadcrumbMgr);

      // Update breadcrumb on expand
      const collapseEl = itemEl.querySelector(`#${collapseId}`);
      collapseEl.addEventListener('show.bs.collapse', () => {
        // Build path from ancestors
        const path = getAncestorPath(itemEl).concat([item.name]);
        if (breadcrumbMgr) breadcrumbMgr.update(path);
      });
    } else {
      // Leaf node — no accordion, just clickable item
      itemEl.innerHTML = `
        <div class="d-flex align-items-center gap-2 px-3 py-2 rounded-3
                    cursor-pointer small text-white-50 sv-tree-leaf"
             role="treeitem"
             tabindex="-1"
             data-node-id="${nodeId}"
             data-node-name="${item.name}"
             data-node-type="${itemType}">
          <svg class="text-success flex-shrink-0" width="12" height="12"
               fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
            <path d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z" />
          </svg>
          <span class="text-truncate">${item.name}</span>
        </div>
      `;

      // Grayed-out placeholder for empty nodes (D-04)
      if (!item.has_versions) {
        const label = document.createElement('span');
        label.className = 'badge bg-secondary bg-opacity-25 text-white-50 ms-auto';
        label.style.fontSize = '9px';
        label.textContent = 'No Active Builds';
        itemEl.querySelector('.sv-tree-leaf').appendChild(label);
      }
    }

    container.appendChild(itemEl);
  });
}

function getIconPath(type) {
  switch (type) {
    case 'Platform': return 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z';
    case 'Project': return 'M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z';
    default: return 'M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1z';
  }
}
```

### Skeleton Loader During Hierarchy Fetch
```html
<!-- Bootstrap 5.3.3 Placeholders -->
<!-- Source: https://getbootstrap.com/docs/5.3/components/placeholders/ -->
<div id="sidebar-tree">
  <div class="placeholder-glow px-3 py-2">
    <span class="placeholder col-8 rounded mb-2"></span>
  </div>
  <div class="placeholder-glow px-3 py-2 ms-3">
    <span class="placeholder col-6 rounded mb-2"></span>
  </div>
  <div class="placeholder-glow px-3 py-2 ms-3">
    <span class="placeholder col-7 rounded mb-2"></span>
  </div>
  <div class="placeholder-glow px-3 py-2 ms-5">
    <span class="placeholder col-5 rounded mb-2"></span>
  </div>
  <div class="placeholder-glow px-3 py-2 ms-5">
    <span class="placeholder col-4 rounded mb-2"></span>
  </div>
</div>
```

### Approval Pending Splash (D-05)
```javascript
// Show non-dismissible status for unapproved users
function showApprovalPendingSplash(user) {
  document.body.innerHTML = `
    <div class="d-flex align-items-center justify-content-center vh-100"
         style="background: #020617;">
      <div class="text-center p-5" style="max-width: 480px;">
        <div class="rounded-circle bg-warning-subtle text-warning
                    d-flex align-items-center justify-content-center mx-auto mb-4"
             style="width: 80px; height: 80px;">
          <svg width="48" height="48" fill="none" stroke="currentColor"
               viewBox="0 0 24 24" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round"
                  stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h2 class="h3 fw-bold text-white mb-3"
            style="font-family: 'Fira Code', monospace;">
          Awaiting Admin Approval
        </h2>
        <p class="text-white-50 mb-4">
          Your account (<strong class="text-white">${user.staff_number}</strong>)
          has been registered successfully. An administrator will review and
          approve your access shortly.
        </p>
        <div class="badge bg-success bg-opacity-10 text-success px-4 py-2 rounded-pill">
          Status: Pending
        </div>
      </div>
    </div>
  `;
}
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| jQuery accordion plugins | Bootstrap 5 Collapse component | Bootstrap 5.0 (2021) | Native JS API, no jQuery dependency, CSS variable customization |
| `div` soup for tree views | Semantic `ul/li` + ARIA roles | GitHub Primer 2025 | Better screen reader support, Forced Color Mode support |
| `aria-activedescendant` for focus | Roving `tabindex` | GitHub 2025 research | Better VoiceOver support on macOS/iOS |
| `role="tree"` for all navigation | Disclosure pattern for simple nav, tree for complex | W3C APG updated 2025 | Right tool for the job; tree role only when keyboard nav is essential |
| `innerHTML` for full tree rebuild | DOM diffing / targeted updates | Industry standard 2024+ | Preserves event listeners, better performance |

**Deprecated/outdated:**
- jQuery-based accordion plugins — not needed with Bootstrap 5's native JS API
- `aria-activedescendant` for tree focus management — has VoiceOver bugs; use roving tabindex instead
- Using `div` elements for tree structure — GitHub's 2025 research showed semantic `ul/li` provides better Forced Color Mode and assistive technology support

## Open Questions

1. **Does the backend expose a `GET /api/v1/me` endpoint for checking user approval status?**
   - What we know: `GET /api/v1/admin/pending-users` exists; login response includes `role`, `full_name`, `department`
   - What's unclear: Whether there's a dedicated endpoint to re-check auth status on page load
   - Recommendation: If no `/me` endpoint exists, decode the JWT client-side to check `is_approved`, or add a lightweight endpoint in Phase 1's backend scope

2. **How should the tree behave when a node has zero children?**
   - What we know: D-04 says show grayed-out "No Active Builds" label
   - What's unclear: Should empty Platforms/Projects be expandable (showing empty state inside) or non-expandable (just a label)?
   - Recommendation: Make them non-expandable (no accordion toggle). Show the grayed-out label inline. This prevents confusing empty expand panels.

3. **Should the sidebar tree persist expand/collapse state across page navigation?**
   - What we know: The tree is in the sidebar, visible on dashboard and users pages
   - What's unclear: Whether navigating to `/users` and back to `/dashboard` should preserve which nodes were expanded
   - Recommendation: Store expand state in `sessionStorage` keyed by node ID. Restoring on page load is cheap and improves UX for operators browsing multiple levels.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Bootstrap 5.3.3 (bundled) | Accordion, grid, utilities, placeholders | ✓ | 5.3.3 | — |
| FastAPI backend | API endpoints (hierarchy, auth, admin) | ✓ | — | — |
| Python 3.13 | Test runner (pytest) | ✓ | 3.13 | — |
| pytest | Backend tests | ✓ | 9.0.2 | — |
| Node.js | — (not needed for this phase) | — | — | — |
| Heroicons SVGs | Icon set | ✓ (inline SVG) | 2.x | Lucide or custom SVGs |

**Missing dependencies with no fallback:**
- None — all dependencies are available

**Missing dependencies with fallback:**
- None

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 9.0.2 (Python, for backend integration tests) |
| Config file | `tests/conftest.py` |
| Quick run command | `pytest tests/test_frontend_scaffolding.py -x` |
| Full suite command | `pytest tests/ -x` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| AUTH-01 | Registration form submits to `/api/v1/register`, shows success message | integration | `pytest tests/test_registration_api.py -x` | ✅ |
| AUTH-02 | Login form submits to `/api/v1/login`, stores token, redirects | integration | `pytest tests/test_login_api.py -x` | ✅ |
| AUTH-02 | Unapproved user sees approval-pending splash | unit (HTML structure) | New: `test_approval_pending_splash.py` | ❌ Wave 0 |
| FLEET-01 | Hierarchy endpoint returns nested platforms/projects/subsystems | integration | `pytest tests/test_admin_approval_api.py -x` (partial) | ✅ |
| FLEET-02 | Dashboard HTML contains `#sidebar-tree` container | unit (HTML structure) | `pytest tests/test_dashboard_components.py::test_line_chart_exists -x` | ✅ |
| FLEET-02 | Tree renderer generates Bootstrap accordion markup | unit (JS structure) | New: `test_hierarchy_tree.py` (HTML structure checks) | ❌ Wave 0 |
| D-02 | Breadcrumb component present in dashboard | unit (HTML structure) | New: `test_breadcrumbs.py` | ❌ Wave 0 |
| D-06 | Users page has approval queue tab with Signal Green badges | unit (HTML structure) | New: `test_approval_queue.py` | ❌ Wave 0 |

### Sampling Rate
- **Per task commit:** `pytest tests/test_frontend_scaffolding.py tests/test_dashboard_components.py -x`
- **Per wave merge:** `pytest tests/ -x`
- **Phase gate:** Full suite green before `/gsd-verify-work`

### Wave 0 Gaps
- [ ] `tests/test_hierarchy_tree.py` — Verify dashboard.html and dashboard.js contain accordion tree markup/rendering logic
- [ ] `tests/test_approval_pending_splash.py` — Verify login.js or auth-guard handles unapproved user redirect
- [ ] `tests/test_breadcrumbs.py` — Verify breadcrumb container exists in dashboard.html
- [ ] `tests/test_approval_queue.py` — Verify users.html contains approval queue tab markup

*(No framework install needed — pytest already available)*

## Sources

### Primary (HIGH confidence)
- Bootstrap 5.3.3 Accordion docs — https://getbootstrap.com/docs/5.3/components/accordion/ — Nested accordion structure, `data-bs-parent`, CSS variables, Collapse API
- Bootstrap 5.3.3 Breadcrumb docs — https://getbootstrap.com/docs/5.3/components/breadcrumb/ — Semantic breadcrumb markup
- Bootstrap 5.3.3 Placeholders docs — https://getbootstrap.com/docs/5.3/components/placeholders/ — Skeleton loader markup
- W3C WAI-ARIA Tree View Pattern — https://www.w3.org/WAI/ARIA/apg/patterns/treeview/ — Keyboard interaction spec, ARIA roles/states/properties
- W3C Navigation Treeview Example — https://www.w3.org/WAI/ARIA/apg/patterns/treeview/examples/treeview-navigation/ — Working example with `ul/li` semantic foundation, roving tabindex, `aria-current`
- GitHub Engineering Blog — "Considerations for making a tree view component accessible" (Jan 2025) — https://github.blog/engineering/user-experience/considerations-for-making-a-tree-view-component-accessible/ — Real-world tree view accessibility: semantic HTML, `aria-level` requirement, roving tabindex vs `aria-activedescendant`, `aria-labelledby` for VoiceOver fix

### Secondary (MEDIUM confidence)
- Design system files: `design-system/sonar-vault/MASTER.md` — Color tokens, typography, anti-patterns
- Design system files: `design-system/sonar-vault/pages/dashboard.md` — Layout overrides, density settings
- Existing codebase: `frontend/static/js/dashboard.js` — Current `renderTree()` implementation, mock data shape
- Existing codebase: `frontend/static/js/users.js` — Admin approval flow pattern
- API schema: `app/schemas.py` — `PlatformSchema`, `ProjectSchema`, `SubsystemSchema` — exact payload shape
- API endpoint: `api/v1/hierarchy.py` — `GET /api/v1/hierarchy/` with `joinedload`

### Tertiary (LOW confidence)
- WebSearch: "Bootstrap 5 nested accordion programmatically generate recursive tree JavaScript 2024 2025" — Community patterns for nested Bootstrap accordions
- WebSearch: "common pitfalls accordion tree navigation nested expand collapse" — SO posts about max-height issues and event bubbling in nested accordions
- Stack Overflow: "Problem updating parent max-height in nested accordions" (Jan 2025) — Confirms max-height measurement issue in custom nested accordions

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — Bootstrap 5.3.3 is confirmed bundled, version matches, no alternatives needed
- Architecture: HIGH — Recursive accordion tree pattern is well-documented by Bootstrap and W3C; existing codebase provides starting point
- Pitfalls: HIGH — Nested accordion ID collision and event bubbling confirmed by multiple SO posts; accessibility gaps confirmed by GitHub's 2025 deep-dive and W3C APG

**Research date:** 2026-03-31
**Valid until:** 2026-04-30 (30 days — Bootstrap 5.3.x is stable, WAI-ARIA patterns are stable)
