# Phase 1: Fleet Modeling & Admin Setup (Backend) - Context

**Gathered:** 2026-03-30
**Status:** Ready for planning

<domain>
## Phase Boundary

Establish the foundational hierarchical data models and backend administrative controls required for the platform. This encompasses modeling Platforms, Projects, and Subsystems natively in SQLite and defining the admin user approval workflows.

</domain>

<decisions>
## Implementation Decisions

### Hierarchy Data Model
- **D-01:** **Projects** are standalone entities that sit on multiple **Platforms** (Many-to-Many architecture). 
- **D-02:** **Subsystems** belong to a **Project**. If assigned a `platform_id`, the subsystem is platform-specific. If `platform_id` is null, the subsystem is common across all platforms hosting that project.

### Approval Workflow
- **D-03:** The Admin must explicitly review the requested department role (provided by the user during signup), and then approve the login to grant access.

### API Tree Traversal
- **D-04:** Backend API endpoints serving the hierarchy should return the **Full Nested Payload** (Platforms -> Projects -> Subsystems) in a single response payload to enable rapid frontend filtering and display without subsequent requests.

### the agent's Discretion
- Database schema naming conventions and structure for mapping tables linking platforms, projects, and subsystems.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Specs
- `.planning/PROJECT.md` — Defines phase constraints, air-gapped nature, and existing SQLite layout.
- `.planning/REQUIREMENTS.md` — Defines AUTH-01 and FLEET-01 verification requirements.
</canonical_refs>
