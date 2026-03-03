# Implementation Plan: Dashboard Core Design & Scaffolding

## Phase 1: Dashboard Layout and Navigation
This phase focuses on the high-level application layout, including the Sidebar and Header.

- [x] Task: Create the base Dashboard HTML structure (`frontend/dashboard.html`). [2d8f2c7]
    - [ ] Define the `main-container` with Sidebar and Header areas.
    - [ ] Implement the `Sidebar` container with logo area and navigation links.
    - [ ] Implement the `Header` with Global Search bar and User Profile area.
- [ ] Task: Implement the Dashboard CSS and Theming.
    - [ ] Configure `tailwind.config.js` with the Emerald/Gray palette (Emerald-900, Emerald-600).
    - [ ] Define custom utility classes for `rounded-2xl` and soft shadows.
    - [ ] Create basic responsive styling for the dashboard layout.
- [ ] Task: Implement the Hierarchical Tree View component.
    - [ ] Create a recursive JS function in `frontend/static/js/dashboard.js` to render the Platform -> Project -> Subsystem tree.
    - [ ] Define the mock tree data structure (Platforms: INS Vikrant, INS Mormugao).
    - [ ] Add collapsible/expandable functionality to the tree nodes.
- [ ] Task: Implement the Global Search bar (UI-only).
    - [ ] Add the ⌘F shortcut hint and interaction logic (focus search on shortcut).
    - [ ] Style the search results area (placeholder for now).
- [ ] Task: Conductor - User Manual Verification 'Dashboard Layout and Navigation' (Protocol in workflow.md)

## Phase 2: Core Dashboard Components
This phase focuses on the primary data visualization components.

- [ ] Task: Implement Stats Cards (System Metrics).
    - [ ] Create the HTML template for a metric card with large text and icon area.
    - [ ] Implement a `renderStats()` function in `dashboard.js` to populate mock data (Total Builds, Active Ships, Resolved Defects).
    - [ ] Apply the Emerald-600 accent styling to the icons and key data points.
- [ ] Task: Implement the Project Progress (Fleet Status) widget.
    - [ ] Create the visual component showing the % of ships running the latest approved version.
    - [ ] Use the `charting-helper.js` (if appropriate) or custom SVG/CSS for the progress visualization.
    - [ ] Mock data for 2-3 projects showing varying fleet update percentages.
- [ ] Task: Conductor - User Manual Verification 'Core Dashboard Components' (Protocol in workflow.md)

## Phase 3: Final Integration and UI Polish
Final touches to ensure the dashboard feels "alive" and polished.

- [ ] Task: Implement User Profile and Notification Area interactions.
    - [ ] Add a simple dropdown menu for the user profile (Settings, Logout).
    - [ ] Mock the notification bell behavior (show a red dot/counter).
- [ ] Task: Final UI Polish and Consistency Check.
    - [ ] Audit spacing, typography, and color usage against `PRD/dashboard-design.md`.
    - [ ] Ensure all assets are bundled locally and the page works in a full offline environment.
- [ ] Task: Conductor - User Manual Verification 'Final Integration and UI Polish' (Protocol in workflow.md)
