# Sonar Vault

## What This Is

Sonar Vault is a specialized offline software version control and repository platform designed for the air-gapped environment of Bharat Electronics Limited (BEL). It manages the software lifecycle for naval sonar systems installed across various Indian Naval Ships (Platforms). It allows departments (D&E, BSTC, Testing) to upload software binaries, track versions hierarchically (Platform -> Project -> Subsystem), and raise defect tickets with forensic attachments.

## Core Value

A 100% offline, highly structured repository and ticketing system tailored specifically to the strict Platform-Project-Subsystem hierarchy of naval sonar deployments.

## Requirements

### Validated

- ✓ Authentication system using BEL Staff Number
- ✓ Department-based Role Access Control (Admin, D&E, BSTC, Testing)
- ✓ Monolithic Python backend serving an SPA-like html/js frontend
- ✓ SQLite Database initialized with User schemas

### Active

- [ ] Software Repository module for binary uploads
- [ ] Automatic and manual metadata capture (Upload Date, Compiled Date, Version)
- [ ] Hierarchical Tree View (Platform -> Project -> Subsystem)
- [ ] Defect Tracking & Forensics module (PCAP and PDF attachments)
- [ ] Dashboard preview grid of software across the fleet
- [ ] Software Version Tree visualization

### Out of Scope

- [Cloud Storage] — Must be 100% offline and localized due to security constraints
- [Secondary Roles] — Permissions are strictly tied to Department identity
- [Multi-Project rollout in Phase 1] — Pilot phase applies only to Project A to validate logic first

## Context

The system operates within an air-gapped BEL environment. The users are broken down into specific departments with distinct capabilities:
- **Admin**: Approves sign-ups
- **D&E**: Uploads builds, downloads
- **BSTC**: Uploads verified builds
- **Testing**: Downloads for shipboard use, raises defects

The existing architecture includes FastAPI, SQLite, and vanilla JS. It supports login/register routes but lacks the core repository and workflow pipelines.

## Constraints

- **Security**: 100% Offline, no external CDNs or cloud dependencies.
- **Tech Stack**: FastAPI for the backend (architecture established instead of Flask as per PRD) and React/Vanilla JS.
- **Access Control**: Users must be manually approved by Admin.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Retain FastAPI vs Flask | Existing codebase already uses FastAPI and SQLAlchemy for Auth. Standardizing on the existing codebase saves time and aligns closely with the PRD's goals. | — Pending |
| Focus only on Project A | Minimizes initial complexity to ensure versioning and defect tracking logic is sound before branching to other projects. | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-03-30 after initialization*
