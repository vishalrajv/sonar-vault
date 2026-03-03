# Product Guide: Sonar Vault

## Initial Concept
Sonar Vault is a specialized offline software version control and repository platform designed for the air-gapped environment of Bharat Electronics Limited (BEL). It manages the software lifecycle for naval sonar systems (e.g., HUMSA-NG, USHUS) installed across various Indian Naval Ships. The system provides a centralized repository where the Design & Engineering (D&E) and BEL Software Technology Centre (BSTC) departments can upload software binaries, while Testing departments use it to download versions and log defects.

## Target Audience & Priorities
The primary user groups for the initial implementation are the **Design & Engineering (D&E)** and **BEL Software Technology Centre (BSTC)** departments. Their workflow centers around securely uploading software binaries, entering version numbers, compilation dates, and viewing the fleet-wide software state.

## Core Features (MVP)
The core features for the initial release include:
- **Software Vault (Upload/View):** A centralized repository to track software builds using automated metadata (upload date) and manual entries (version number, compiled date) from the uploading agency. It will feature a preview grid for users to view the current state of software across the fleet.
- **Fleet Dashboard:** A high-level overview page providing key metrics (Total Builds, Active Ships), software upload trends via charts, and a summary of recent activity across the fleet.
- **Session Management:** Secure access control featuring "Remember Me" persistence, automatic idle timeouts (30 mins), and concurrency restrictions (single active session per staff number).

## Technical Constraints & Design Principles
- **100% Offline Environment:** The system must operate entirely offline. To achieve this while maintaining a high-quality UI, **all assets (including Tailwind/React dependencies, fonts, and icons) must be bundled locally** within the project folder. No external cloud or CDN dependencies are permitted.
- **Hierarchical Structure:** The data is organized based on the relationship between naval platforms (ships) and sonar projects. Projects and subsystems are categorized as either Common or Platform-Specific.

## Future Expansion
While the pilot phase focuses exclusively on **Project A** to ensure the integrity of the versioning logic, the system architecture should be designed to support a scale of **1-5 additional projects** in future iterations.