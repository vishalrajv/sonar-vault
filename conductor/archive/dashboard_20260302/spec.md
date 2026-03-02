# Specification: Dashboard Page Implementation (TailAdmin Inspiration)

## Overview
Implement a centralized Dashboard Page for Sonar Vault, drawing aesthetic and layout inspiration from the TailAdmin VueJS dashboard. The page will provide a high-level overview of the fleet's software state, recent activity, and key performance metrics.

## Functional Requirements
- **Stat Cards:**
    - Display 4 key metrics using TailAdmin-style stat cards (e.g., Total Builds, Successful Uploads, Active Ships, Pending Defects).
- **Charts/Graphs:**
    - Implementation of at least two charts (e.g., a line chart for 'Software Uploads Over Time' and a bar chart for 'Project Distribution').
- **Recent Activity Table:**
    - A table displaying the last 5-10 software version uploads across different ships and projects.
- **Filtering UI:**
    - Interactive filters for 'Ship Name' and 'Sonar Project' to simulate data segmentation.
- **Data Handling:**
    - Use hardcoded mock data for all UI components in this phase.

## Non-Functional Requirements
- **Visual Style:** Adhere to the TailAdmin aesthetic (clean, modern, sidebar-driven).
- **Styling Framework:** Tailwind CSS (locally bundled).
- **Responsiveness:** Desktop-first design optimized for office workstation resolutions.
- **Offline Integrity:** No external CDN dependencies for charts or icons.

## Acceptance Criteria
- [ ] Dashboard page is accessible via a dedicated route (`/dashboard.html` or through SPA routing).
- [ ] 4 Stat Cards are visible with accurate labels and mock values.
- [ ] At least 2 charts render correctly using mock data.
- [ ] Recent Activity Table displays data and includes column headers.
- [ ] Filter dropdowns are functional (UI state updates, even if data is static).
- [ ] All assets (CSS, JS, Fonts, Icons) are loaded locally.

## Out of Scope
- Backend API integration (Live data).
- Real-time data synchronization.
- Customizable widget layout.
- Exporting dashboard data to PDF/Excel.