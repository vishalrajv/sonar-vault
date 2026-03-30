# Project Roadmap

## Phase 1: Fleet Modeling & Admin Setup (Backend)

**Goal:** Establish the foundational hierarchical data models and the backend administrative controls required for the platform.

**Requirements Mapped:**
- [x] AUTH-01: User can create account with staff number and wait for admin approval
- [x] FLEET-01: System maintains Platform -> Project -> Subsystem hierarchical tree with distinct Platform-Specific tracking

**Success Criteria:**
1. Database schema holds distinct mappings for Platforms, Projects, and Subsystems (including Common vs Platform-Specific).
2. API endpoints exist to register users and query their pending approval status.
3. API endpoint exists for an Admin to view and approve pending users.

---

## Phase 2: Navigation & Authentication (Frontend)

**Goal:** Implement the frontend authentication flow, admin approval dashboard, and the recursive hierarchical tree navigation.

**Requirements Mapped:**
- [x] AUTH-02: User can log in with staff number and password
- [x] FLEET-02: Users can navigate the hierarchical tree recursively to view versions

**Success Criteria:**
1. Unapproved users are blocked from logging in.
2. Admins can approve users from a dedicated UI dashboard.
3. Users can visually navigate the Platform -> Project -> Subsystem tree on the frontend.
**UI hint:** yes

---

## Phase 3: Software Repository Upload & Dashboard

**Goal:** Allow D&E and BSTC departments to upload software binaries and provide a unified dashboard preview grid.

**Requirements Mapped:**
- [x] REPO-01: D&E/BSTC users can upload software binaries with Version Number and Compiled Date explicitly entered
- [x] REPO-02: System automatically captures Upload Date for binaries
- [x] REPO-03: All users can view a Dashboard preview grid of software across the fleet

**Success Criteria:**
1. Authorized users can securely upload binaries via the frontend to a local "Vault" folder.
2. Metadata (Version, Compiled Date, Upload Date) is correctly parsed and saved upon upload.
3. The Dashboard aggregates and displays software versions cleanly in a preview grid.
**UI hint:** yes

---

## Phase 4: Defect Tracking Initialization (Backend)

**Goal:** Create the backend APIs to support the defect tracking state machine and file attachments.

**Requirements Mapped:**
- [x] DEF-01: Testing users can log defect tickets linked to a specific Platform, Project, and Version
- [x] DEF-02: Testing users can attach multiple forensic files (.pcap and .pdf) to tickets
- [x] DEF-03: System supports defect lifecycle: New -> Open -> Fixed -> Verified -> Closed

**Success Criteria:**
1. APIs can create a new ticket linked to the appropriate hierarchical software node.
2. File upload endpoints are capable of receiving and securely storing `.pcap` and `.pdf` files.
3. Ticket status transitions (e.g., Open -> Fixed) are strictly enforced and recorded.

---

## Phase 5: Defect Tracking Integration (Frontend)

**Goal:** Build the testing department's UI for raising tickets, uploading forensic attachments, and tracking lifecycle status.

**Requirements Mapped:**
- All DEF modules are fully integrated into the frontend (UI mapping for Phase 4 requirements).

**Success Criteria:**
1. Testing users have a dedicated interface to log incidents without breaking the workflow.
2. Forensic files can be attached seamlessly via drag-and-drop or standard file inputs.
3. The UI correctly renders the ticket lifecycle and allows permitted state transitions.
**UI hint:** yes

---

## Phase 6: End-to-End Walkthrough & Policy Hardening

**Goal:** Ensure all offline, air-gapped constraints are globally respected and perform full integration testing across the fleet hierarchy.

**Requirements Mapped:**
- Global validation of all v1 scope offline policies and edge cases.

**Success Criteria:**
1. The entire application runs 100% offline with zero cloud requests.
2. Departmental role permissions hold true across every single endpoint and view.
3. Full integration test spanning from user registration -> software upload -> defect raising succeeds.
