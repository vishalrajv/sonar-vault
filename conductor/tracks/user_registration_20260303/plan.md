# Implementation Plan: User Registration and Admin Approval

## Phase 1: Database Schema Expansion [checkpoint: c5dc837]
*Goal: Update the User model to support registration details and approval status.*
- [x] Task: Expand `models/user.py` with new fields (staff_number, full_name, department, role_designation, dob, phone_number, personal_email, official_email, is_approved).
- [x] Task: Create and run a migration script to update the `users` table.
- [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Registration API (TDD) [checkpoint: 4ee91c6]
*Goal: Implement the public endpoint for user registration.*
- [x] Task: Write failing unit tests for `POST /api/v1/register` (check uniqueness, required fields).
- [x] Task: Implement `register` endpoint in `api/v1/auth.py`.
- [x] Task: Verify registration sets `is_active=False` and `is_approved=False`.
- [x] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: Admin Approval API (TDD) [checkpoint: acff84e]
*Goal: Implement administrative endpoints for managing pending users.*
- [x] Task: Write failing unit tests for `GET /api/v1/admin/pending-users` and `POST /api/v1/admin/approve-user/{id}` (check RBAC - only admins).
- [x] Task: Implement admin endpoints in `api/v1/auth.py`.
- [x] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4: Auth and Login Logic Updates (TDD) [checkpoint: 3a150ce]
*Goal: Transition login to use Staff Number and enforce approval checks.*
- [x] Task: Write failing tests for login using Staff Number and rejecting unapproved users. [81a344b]
- [x] Task: Update login endpoint in `api/v1/auth.py`. [cead19e]
- [x] Task: Update `get_current_user` dependency to handle new schema. [cead19e]
- [x] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md) [3a150ce]

## Phase 5: Frontend - User Registration [checkpoint: 51d6030]
*Goal: Implement the registration UI and connect it to the backend.*
- [x] Task: Create `frontend/register.html` with the required fields.
- [x] Task: Create `frontend/static/js/register.js` to handle form submission.
- [x] Task: Add `/register` route to `app/main.py` to serve the registration page.
- [x] Task: Update `frontend/login.html` with a link to the registration page.
- [x] Task: Update `frontend/dashboard.html` and `frontend/static/js/dashboard.js` to include the Admin Pending Approvals widget.
- [x] Task: Conductor - User Manual Verification 'Phase 5' (Protocol in workflow.md) [51d6030]

## Phase 6: User Management Refactoring
*Goal: Move pending approvals to a dedicated User Management page.*
- [x] Task: Create `frontend/users.html` for user management.
- [x] Task: Create `frontend/static/js/users.js` to handle user management logic.
- [x] Task: Update Sidebar in `frontend/dashboard.html` and `frontend/users.html` to include "User Management" (Admin Only).
- [x] Task: Add `/users` route to `app/main.py`.
- [x] Task: Remove pending approvals widget from `frontend/dashboard.html` and `frontend/static/js/dashboard.js`.
- [~] Task: Conductor - User Manual Verification 'Phase 6' (Protocol in workflow.md)