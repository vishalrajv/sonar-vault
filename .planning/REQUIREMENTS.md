# Requirements

## v1 Requirements

### Authentication
- [ ] **AUTH-01**: User can create account with staff number and wait for admin approval
- [ ] **AUTH-02**: User can log in with staff number and password

### Software Repository
- [ ] **REPO-01**: D&E/BSTC users can upload software binaries with Version Number and Compiled Date explicitly entered
- [ ] **REPO-02**: System automatically captures Upload Date for binaries
- [ ] **REPO-03**: All users can view a Dashboard preview grid of software across the fleet

### Fleet Hierarchy
- [ ] **FLEET-01**: System maintains Platform -> Project -> Subsystem hierarchical tree with distinct Platform-Specific tracking
- [ ] **FLEET-02**: Users can navigate the hierarchical tree recursively to view versions

### Defect Tracking
- [ ] **DEF-01**: Testing users can log defect tickets linked to a specific Platform, Project, and Version
- [ ] **DEF-02**: Testing users can attach multiple forensic files (.pcap and .pdf) to tickets
- [ ] **DEF-03**: System supports defect lifecycle: New -> Open -> Fixed -> Verified -> Closed

## v2 Requirements (Deferred)
- [ ] Support for multiple projects (e.g., Project B integration beyond the pilot scope)

## Out of Scope
- [Cloud Storage] — Must be 100% offline and localized due to security constraints
- [Secondary Roles] — Permissions are strictly tied to Department identity

---
## Traceability
*(To be populated by Roadmap)*
