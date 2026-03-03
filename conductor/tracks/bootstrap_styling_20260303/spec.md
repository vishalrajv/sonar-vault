# Specification: Bootstrap Styling Integration (Sonar Vault)

## Overview
This track involves migrating the existing styling of the Sonar Vault application from Tailwind CSS to **Bootstrap 5.3.3 (Stable)** to achieve a more consistent and robust UI for BEL staff members. Since the environment is 100% offline, the Bootstrap kit will be downloaded and bundled locally.

## Goals
- **Full Migration:** Transition the global styling architecture from Tailwind utility classes to Bootstrap's component-based approach.
- **Offline Reliability:** Bundle all Bootstrap CSS/JS assets within the project to ensure 100% functionality without internet access.
- **Modern Clean UI:** Maintain the high-contrast design philosophy while leveraging Bootstrap's standardized layouts.

## Functional Requirements
1.  **Offline Asset Bundling:**
    -   Download and store Bootstrap 5.3.3 (CSS, JS, and dependencies like Popper.js if needed) in `frontend/static/vendor/bootstrap/`.
    -   Update all HTML templates to link to local Bootstrap files.
2.  **Layout Redesign:**
    -   Implement Bootstrap's grid system (`container`, `row`, `col`) for the overall page structure.
    -   Rebuild the **Navbar**, **Sidebar**, and **Page Headers** using Bootstrap components.
3.  **Interactive Components:**
    -   Integrate Bootstrap **Modals**, **Alerts**, and **Tooltips** for system communications and user feedback.
4.  **Style Cleanup:**
    -   Systematically remove Tailwind CSS classes from existing HTML templates.
    -   Uninstall Tailwind CSS from the `package.json` and build scripts.

## Non-Functional Requirements
- **High Contrast:** Ensure the Bootstrap theme (colors, borders) maintains high visibility for shipboard operational safety.
- **Performance:** Minimize the number of custom CSS overrides by leveraging Bootstrap's Sass variables (if needed) or CSS variables.
- **Responsive Design:** Adhere to Bootstrap's standard breakpoints for cross-device compatibility.

## Acceptance Criteria
- [ ] Bootstrap 5.3.3 assets are correctly linked and served from the local filesystem.
- [ ] The **Fleet Dashboard** and **Login Page** are fully styled using Bootstrap components.
- [ ] The application remains fully functional and visually coherent without any internet connection.
- [ ] Tailwind CSS is completely removed from the project repository.
- [ ] All interactive elements (Modals, Dropdowns) work correctly using Bootstrap's JS.

## Out of Scope
- Migrating the custom SVG Charting Helper (this remains custom logic).
- Changing the backend FastAPI or database logic.
