# Implementation Plan: Session Management System

## Phase 1: Database & Model Updates [checkpoint: a05ae53]
*Goal: Prepare the database to track active session IDs for concurrency control.*
- [x] **Task:** Update `models/user.py` to include `current_session_id` (String, Nullable). d2393dd
- [x] **Task:** Run database migration or update schema to reflect new field. d1042d1
- [x] **Task:** Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Backend API Enhancements [checkpoint: dee6022]
*Goal: Implement logout, concurrency logic, and session status checks.*
- [x] **Task:** Update `api/v1/auth.py` Login endpoint to generate a unique session ID (JTI) and update the user record. f8b5b2f
- [x] **Task:** Write Tests: Verify that a second login invalidates the previous session ID in the database. f8b5b2f
- [x] **Task:** Implement: Concurrency logic in Login. f8b5b2f
- [x] **Task:** Write Tests: `/api/v1/logout` clears the session ID and returns 200. 7402a0e
- [x] **Task:** Implement: Logout endpoint. 7402a0e
- [x] **Task:** Write Tests: `/api/v1/session/status` returns user info if valid, 401 if invalid. 7402a0e
- [x] **Task:** Implement: Session status endpoint. 7402a0e
- [x] **Task:** Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: Security Middleware & Token Logic
*Goal: Enforce session validity on protected routes and handle "Remember Me".*
- [~] **Task:** Update `app/token_utils.py` to handle `expires_delta` for "Remember Me" (e.g., 7 days vs 8 hours).
- [ ] **Task:** Implement FastAPI dependency `get_current_active_user` that checks `current_session_id` against the token's JTI.
- [ ] **Task:** Apply security dependency to `/dashboard` and `/api/v1/vault` routes in `app/main.py`.
- [ ] **Task:** Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4: Frontend Logic (Session Control)
*Goal: Implement idle timeout, "Remember Me" UI, and automatic logout.*
- [ ] **Task:** Update `login.html` and `login.js` to include and handle the "Remember Me" checkbox.
- [ ] **Task:** Implement `session-manager.js` to handle the 30-minute idle timeout (resetting on mouse/keyboard events).
- [ ] **Task:** Add a 2-minute "Session Expiring" warning modal/notification.
- [ ] **Task:** Update `dashboard.js` to integrate with the session manager and handle 401 redirects.
- [ ] **Task:** Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)

## Phase 5: Final Integration & Cleanup
*Goal: End-to-end verification of the session lifecycle.*
- [ ] **Task:** Perform integration testing for "Single Session Only" across multiple browser tabs.
- [ ] **Task:** Verify idle timeout triggers correctly in a headless/automated environment.
- [ ] **Task:** Conductor - User Manual Verification 'Phase 5' (Protocol in workflow.md)
