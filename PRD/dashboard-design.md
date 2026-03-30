# Sonar Vault Dashboard Design Document

## 1. Vision & Objective
The Sonar Vault Dashboard serves as the central command center for monitoring the software lifecycle across naval sonar systems. Inspired by modern productivity interfaces, the design prioritizes **high-density information visualization** while maintaining **extreme clarity** for shipboard operational safety.

## 2. Design System (Based on Reference Image)

### 2.1 Color Palette
| Category | Color (Hex/Tailwind) | Usage |
| :--- | :--- | :--- |
| **Primary** | `#064E3B` (Emerald-900) | Sidebar, Primary Buttons, Success States |
| **Accent** | `#059669` (Emerald-600) | Active Stats, Highlighted Charts |
| **Background** | `#F9FAFB` (Gray-50) | Main Layout Background |
| **Surface** | `#FFFFFF` (White) | Cards, Modals, Header |
| **Border** | `#F3F4F6` (Gray-100) | Subtle separators and Card borders |
| **Text (Heading)** | `#111827` (Gray-900) | Titles and key data points |
| **Text (Body)** | `#6B7280` (Gray-500) | Subtitles and labels |

### 2.2 Typography & UI Elements
- **Font:** Inter or similar sans-serif (Clean, highly legible).
- **Radius:** Large rounded corners (`rounded-2xl` / `1rem`) for cards to match the modern aesthetic.
- **Shadows:** Soft, diffused shadows (`shadow-sm` or custom `0 10px 15px -3px rgba(0,0,0,0.05)`) for depth.

## 3. Layout Architecture

### 3.1 Sidebar (Enhanced)
- **Logo Area:** "Donezo" style branding with a custom Sonar Vault SVG icon.
- **Navigation Groups:**
  - **Menu:** Dashboard, Vault (Files), Defect Tracker, Analytics.
  - **General:** Settings, Help, Logout.
- **Contextual Card:** A bottom-docked card showing "System Health" or "Offline Sync Status".

### 3.2 Header (Search & Identity)
- **Global Search:** Command-palette style search bar (`⌘F` shortcut hint) for quick access to Platforms, Projects, or Versions.
- **Quick Actions:** Notifications (Bell), System Alerts (Mail icon for admin notifications).
- **User Profile:** Avatar with name and department (e.g., "D&E Admin").

### 3.3 Main Content Grid
- **Title Section:** "Dashboard Overview" with a descriptive subtitle.
- **Primary Actions:** "+ Upload Binary" and "View Fleet Tree" buttons.

## 4. Component Mapping (Domain Translation)

| Reference Element | Sonar Vault Translation | Data Source |
| :--- | :--- | :--- |
| **Stats Cards** | **System Metrics** | Counts of total builds, active ships, resolved defects. |
| **Project Analytics** | **Build Frequency** | Weekly distribution of software uploads per project. |
| **Project Progress** | **Fleet Update Status** | % of ships running the latest approved version. |
| **Team Collaboration** | **Recent Activity** | Real-time feed of uploads/defects by department users. |
| **Project List** | **Active Defects** | List of open defect tickets with severity icons. |
| **Time Tracker** | **Session Audit** | Counter showing time spent on current audit/upload session. |

## 5. Module-Specific Design Details

### 5.1 The Hierarchical Tree View (Module 3)
The Sidebar or a dedicated secondary panel will feature a recursive tree:
- **Level 1:** Platform (e.g., INS Vikrant)
- **Level 2:** Project (e.g., Project A)
- **Level 3:** Subsystem (e.g., A1 Common)
- **Visuals:** Use collapsible folders and specialized icons for Ship types vs. Sonar types.

### 5.2 Defect Tracking Widget
A dedicated card showing:
- **Donut Chart:** Open vs. Fixed defects.
- **List:** Top 5 critical defects with direct links to forensics (.pcap/.pdf).

### 5.3 Visualization & History (Software Version Tree)
In the main view, a graphical "lineage" chart showing version divergence:
- **Node-Link Diagram:** Visualizing when a "Common" version splits into a "Platform-Specific" variant.

## 6. Implementation Strategy
1. **CSS Refactor:** Update `tailwind.config.js` to include the specific Emerald/Gray palette and custom spacing.
2. **Component Library:** Build reusable Vanilla JS components for the Cards, Charts (extending `charting-helper.js`), and Tree View.
3. **Data Binding:** Connect the frontend to the FastAPI `/api/v1` endpoints to populate real-time stats.
