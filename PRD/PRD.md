# Sonar Vault: Offline Software Version Control & Lifecycle Management

**Developer:** Vishal Raj V, E218023  
**Organization:** Sonar Systems Department, Bharat Electronics Limited (BEL)

---

## 1. Project Overview

Sonar Vault is a specialized offline software version control and repository platform designed for the air-gapped environment of Bharat Electronics Limited (BEL). The platform manages the software lifecycle for naval sonar systems (e.g., HUMSA-NG, USHUS) installed across various Indian Naval Ships (Platforms).

The system provides a centralized repository where the **Design & Engineering (D&E)** and **BEL Software Technology Centre (BSTC)** departments can upload software binaries. The **Testing** department uses the platform to download specific software versions and log technical defects encountered during onboard trials. Access and functionality are governed entirely by the user's department.

**Implementation Note:** The platform will initially be implemented for a single project to validate the departmental workflows and hierarchical data model. Support for additional projects will be integrated once the initial deployment is proven successful.

---

## 2. Departmental Framework & Access Control

In this system, the user's department acts as their functional role. There are no secondary roles; permissions are assigned directly to the department identity.

### 2.1 Department-Based Permissions

| Department (Acting as Role) | System Permissions |
| :--- | :--- |
| **Admin** | Approves sign-up requests, manages the user database, and performs initial system scaffolding. |
| **D&E (Design & Engineering)** | Uploads software binaries, manually enters Version Number and Compiled Date, creates changelogs, and downloads software. |
| **BSTC (BEL Software Tech Centre)** | Uploads verified software binaries, enters Version Number/Compiled Date, and performs software downloads for audit. |
| **Testing** | Downloads software for shipboard use, creates defect tickets, and attaches forensic files (Wireshark/PDF). |

### 2.2 Authentication Workflow

* **Identifier:** BEL Staff Number.
* **Sign-up:** Users register by providing their staff number, password, and selecting their Department (D&E, BSTC, or Testing).
* **Approval:** Accounts remain "Locked" until the Admin manually approves the request.
* **Initial Setup:** A single master admin account is created during scaffolding to manage all subsequent user approvals.

---

## 3. Hierarchical Structural Model

The platform organizes data based on the unique relationship between naval platforms (ships) and sonar projects as outlined in the department's technical diagrams.

### 3.1 Platform-Project-Subsystem Hierarchy

**Initial Scope:** For the pilot phase, the system focuses exclusively on **Project A** to ensure the integrity of the versioning and defect tracking logic. Support for Project B and others will be added after successful implementation.

Projects and subsystems are categorized as either **Common** (shared across ships) or **Platform-Specific** (unique to a specific vessel).

* **Platform 1 (e.g., INS Mormugao):**
  * Project A: Subsystem A1 (Common), A2 (Common), Subsystem A3.1 (Specific to Platform 1).
* **Platform 2 (e.g., INS Kochi):**
  * Project A: Subsystem A1 (Common), A2 (Common), Subsystem A3.2 (Specific to Platform 2).

**Key Logic:** The versioning system distinguishes between common builds (e.g., Subsystem A1 v1.0) and hull-targeted builds (e.g., Subsystem A3.1 v2.5).

---

## 4. Functional Module Specifications

### Module 1: Software Repository (The Vault)

This module tracks software builds using automated metadata and manual entries from the uploading agency.

* **Binary Upload:** D&E or BSTC users upload the software file.
* **Automatic Metadata:** The system automatically captures the **Upload Date** when the file is saved.
* **Manual Entry Fields:** The uploader must explicitly provide:
  * **Software Version Number:** (e.g., v1.0.5).
  * **Compiled Date:** The date the software was built by the agency (e.g., 2026-02-15).
* **Preview Grid:** A dashboard for all users to view the current state of software across the fleet:

| Platform | Project | Subsystem | Version | Compiled Date | Upload Date (Auto) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Platform 1 | Project A | A3.1 | v2.5.0 | 2026-02-15 | 2026-02-28 |

### Module 2: Defect Tracking & Forensics

The Testing department logs incidents encountered during sea trials.

* **One Ticket Per Problem:** Each ticket represents a single issue linked to a specific Platform, Project, and Software Version.
* **Forensic Attachments:**
  * **Wireshark Captures (.pcap):** For network traffic analysis between processing racks and consoles.
  * **Defect Reports (.pdf):** Formal documents containing screen captures and environmental data (Sea State, Depth).
* **Status Lifecycle:** New -> Open -> Fixed -> Verified -> Closed.

### Module 3: Visualization & History

* **Hierarchical Tree View:** A recursive navigation menu allowing users to drill down from Platform -> Project -> Subsystem.
* **Software Version Tree:** A graphical representation showing the evolution of a subsystem, highlighting when a version diverges into a platform-specific variant (A3.1 vs A3.2).

---

## 5. Technical Implementation Roadmap

### Phase 1: Backend & Database

* **Backend Framework:** Python Flask (Class-based structure for modularity).
* **API Architecture:** RESTful API for handling departmental workflows.
* **Database:** SQLite for relational data mapping (Users, Platforms, Subsystems).
* **ORM:** SQLAlchemy for database interactions and session management.
* **Environment Management:** `python-dotenv` for configuration and `.venv` for dependency isolation.
* **Local Storage:** A dedicated "Vault" folder on the local server for binary storage. No external cloud dependencies.

### Phase 2: Frontend & Navigation

* **Stack:** React.js with Tailwind CSS for an offline-ready UI.
* **Tree Navigation:** Use a recursive component to render the fleet hierarchy as per the user's diagram.

### Phase 3: Workflow Implementation

* **Upload API:** Implementation of the departmental upload logic, extracting system time for `upload_date`.
* **Ticketing API:** A defect management system where Testing users can upload multiple forensic files.
* **Admin Dashboard:** Interface for the Admin to approve or reject pending staff sign-up requests based on their department.

---

## 6. Project Constraints

* **Network Status:** Must be 100% offline. All assets must be bundled locally.
* **Security:** Access restricted to BEL Staff only via Departmental identity; the department itself is the role.
* **Integrity:** Responsibility for version accuracy and compiled dates lies with the D&E/BSTC uploading agencies.
