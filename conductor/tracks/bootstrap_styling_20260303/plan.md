# Implementation Plan: Bootstrap Styling Integration

## Phase 1: Preparation & Environment Setup
*Goal: Download Bootstrap 5.3.3 and prepare the project structure for migration.*
- [ ] **Task:** Download Bootstrap 5.3.3 (Compiled CSS and JS) and Popper.js 2.11.8.
- [ ] **Task:** Create the directory `frontend/static/vendor/bootstrap/` and store the downloaded assets.
- [ ] **Task:** Update `frontend/index.html` to include links to the local Bootstrap CSS/JS files.
- [ ] **Task:** Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Login Page Styling (Proof of Concept)
*Goal: Stylize the login page using Bootstrap as a baseline for the full migration.*
- [ ] **Task:** Update `frontend/login.html` to use Bootstrap's layout and form components.
- [ ] **Task:** Remove all Tailwind CSS classes from `frontend/login.html`.
- [ ] **Task:** Verify that the "Remember Me" checkbox and Login button are styled correctly.
- [ ] **Task:** Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: Dashboard Layout Migration
*Goal: Implement Bootstrap's grid system and rebuild core layout components on the dashboard.*
- [ ] **Task:** Redesign the **Navbar** and **Sidebar** in `frontend/dashboard.html` using Bootstrap.
- [ ] **Task:** Implement the main content area with Bootstrap's grid system (`container-fluid`, `row`, `col`).
- [ ] **Task:** Convert **Modals** and **Alerts** in `frontend/dashboard.html` to Bootstrap components.
- [ ] **Task:** Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4: Full Stylization & Component Updates
*Goal: Ensure all page elements across the application are styled consistently with Bootstrap.*
- [ ] **Task:** Systematically update all remaining UI elements (e.g., page headers, data grids, buttons) in the dashboard.
- [ ] **Task:** Ensure high contrast is maintained for all Bootstrap components (colors, typography).
- [ ] **Task:** Verify that the custom SVG Charting Helper integrates seamlessly with the new Bootstrap layout.
- [ ] **Task:** Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)

## Phase 5: Tailwind Removal & Cleanup
*Goal: Remove all Tailwind-related files and configurations from the project.*
- [ ] **Task:** Final check to ensure no Tailwind classes remain in the HTML templates.
- [ ] **Task:** Uninstall Tailwind CSS from `package.json` and remove `tailwind.config.js`.
- [ ] **Task:** Update build/start scripts (`start_server.bat` if applicable) to remove Tailwind-related steps.
- [ ] **Task:** Conductor - User Manual Verification 'Phase 5' (Protocol in workflow.md)
