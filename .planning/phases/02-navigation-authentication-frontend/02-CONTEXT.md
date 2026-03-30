# Phase 2: Navigation & Authentication (Frontend) - Context

**Gathered:** 2026-03-30
**Status:** Ready for planning

<domain>
## Phase Boundary

Implement the visual experience for user authentication and fleet-wide hierarchical navigation. This includes the login/register flows (with approval pending feedback), a dedicated admin dashboard for user approval, and a recursive tree viewer for Browsing Platforms -> Projects -> Subsystems.

</domain>

<decisions>
## Implementation Decisions

### Fleet Hierarchy Navigation
- **D-01:** **Accordion Sidebar.** Use a nested vertical navigation menu (Bootstrap 5.3.3 compatible) to represent the deep Platform-Project-Subsystem hierarchy.
- **D-02:** **Persistent Breadcrumbs.** Maintain a visual path (e.g., `Platforms / Ship Alpha / Project X`) to ground the user in their current hierarchical location.
- **D-03:** **Skeleton Loaders.** Use pulse skeleton components in the dashboard area while the "Full Nested Payload" is being parsed on initial load.
- **D-04:** **Grayed-out Placeholders.** If a Platform or Project has no uploaded software versions (Phase 3 content), still display the node in the tree but with a grayed-out "No Active Builds" label.

### Authentication & Admin Workflow
- **D-05:** **Approval Pending Splash.** Users who are authenticated but not yet approved by an admin (per Phase 1 logic) see a non-dismissible status message instead of the dashboard.
- **D-06:** **Approval Queue Tab.** The `users.html` view will feature a prioritized "Awaiting Approval" tab using Signal Green badges (`#22C55E`) for clear actionable identification.

### UI/UX Design System (Naval/Technical)
- **D-07:** **Tactical Dark Mode.** Follow `design-system/sonar-vault/MASTER.md` for a high-contrast, Deep Black (#020617) and Midnight Blue (#0F172A) aesthetic.
- **D-08:** **Signal Accents.** Use Signal Green (#22C55E) exclusively for positive actions, approvals, and verified builds.
- **D-09:** **Information Density.** Adopt a **Bento Grid** layout for the dashboard to allow simultaneous viewing of hierarchy nav and version metadata without clutter.

### the agent's Discretion
- Specific Bootstrap component choices for the accordion and data tables.
- SVG icon selection from the Heroicons set.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Design & Specs
- `.planning/PROJECT.md` — Defines 100% offline constraint and department roles.
- `.planning/REQUIREMENTS.md` — Traceability for AUTH-02 and FLEET-02.
- `design-system/sonar-vault/MASTER.md` — Global design tokens and typography.
- `design-system/sonar-vault/pages/dashboard.md` — Layout and density overrides.

### Context
- `.planning/phases/01-fleet-modeling-admin-setup-backend/01-CONTEXT.md` — Prior decisions on many-to-many project mapping.
</canonical_refs>
