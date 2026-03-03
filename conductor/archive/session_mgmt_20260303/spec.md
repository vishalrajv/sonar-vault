# Track Specification: Session Management System

## Overview
Implement a robust session management system for Sonar Vault to ensure secure, department-based access while maintaining a smooth user experience for BEL staff. This includes session persistence, timeout handling, and concurrent session restrictions.

## Functional Requirements
1.  **Session Lifecycle:**
    *   **Default Duration:** Sessions are active for **8 hours**.
    *   **Remember Me:** Implement a checkbox on the login page to persist the session across browser restarts (using long-lived JWT).
    *   **Idle Timeout:** Automatically log the user out after **30 minutes** of inactivity.
2.  **Concurrency Control:**
    *   **Single Session Only:** Logging in with the same staff number from a new browser/device will invalidate the previous active session.
3.  **Authentication Handlers:**
    *   Provide unified middleware to protect sensitive routes (`/dashboard`, `/api/v1/vault/*`).
    *   Expose a `/api/v1/logout` endpoint to explicitly terminate the session.
    *   Expose a `/api/v1/session/status` endpoint to verify the current session's health.

## Non-Functional Requirements
- **Security:** All tokens must be signed using the `SECRET_KEY` defined in `.env`.
- **Integrity:** Session invalidation must be handled on the server (e.g., storing the latest issued `jti` or similar in the database for each user).
- **UX:** Provide a subtle visual notification 2 minutes before the idle timeout occurs.

## Acceptance Criteria
- [ ] User can log in with "Remember Me" and stay authenticated after closing/reopening the browser.
- [ ] User is redirected to `/login` after 8 hours of continuous use (if "Remember Me" is not checked).
- [ ] User is automatically logged out after 30 minutes of no interaction.
- [ ] Logging in on Browser B with Staff ID 12345 immediately invalidates the session on Browser A.
- [ ] The logout button correctly clears all local storage tokens and informs the server.

## Out of Scope
- OAuth2/OpenID integration (Not needed for air-gapped BEL environment).
- Two-Factor Authentication (MFA).
- IP-based session locking.
