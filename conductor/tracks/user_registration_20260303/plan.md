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

## Phase 3: Admin Approval API (TDD)
*Goal: Implement administrative endpoints for managing pending users.*
- [ ] Task: Write failing unit tests for `GET /api/v1/admin/pending-users` and `POST /api/v1/admin/approve-user/{id}` (check RBAC - only admins).
- [ ] Task: Implement admin endpoints in `api/v1/auth.py`.
- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4: Auth and Login Logic Updates (TDD)
...