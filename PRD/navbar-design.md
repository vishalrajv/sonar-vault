# Sonar Vault Navigation Bar Design Document

## 1. Vision & Objective
The Navigation Bar (Navbar) of Sonar Vault is designed to be the primary gateway for fleet-wide software discovery. Inspired by the "Discovery-First" architecture of Fireart Studio, it transforms a static menu into an interactive "Command Center" that provides immediate context to the user's department and project focus.

## 2. Design System (Alignment with Dashboard)

### 2.1 Visual Style & Effects
- **Background:** Semi-transparent "Glassmorphism" effect (`backdrop-blur-md` with `bg-white/80`).
- **Border:** Subtle bottom border (`border-b border-gray-100`) to separate it from the main content.
- **Shadow:** Ultra-soft elevation (`shadow-sm`) to create depth without clutter.
- **Color Palette:**
    - **Links:** `text-gray-500` (Default), `text-emerald-900` (Hover/Active).
    - **CTA Button:** `bg-emerald-900` with `text-white`.

### 2.2 Typography
- **Logo:** Custom Sonar Vault SVG (Emerald-900) with bold "SONAR VAULT" text.
- **Links:** Medium weight sans-serif (Inter), 14px for high density and legibility.

## 3. Layout Architecture (Fireart-Inspired)

### 3.1 Global Structure
| Position | Element | Description |
| :--- | :--- | :--- |
| **Left** | **Logo & Branding** | Identity and "Home" trigger. |
| **Center** | **Discovery Links** | Mega-menu triggers for Platforms, Projects, and Departments. |
| **Right** | **Action & Profile** | Search icon, Notifications, and Department-Specific CTA. |

### 3.2 The "Discovery" Mega-Menus
Following the Fireart pattern, clicking "Platforms" or "Projects" reveals a multi-column mega-menu:
- **Column 1 (Featured):** Quick links to "Active Trials" or "Recent Uploads."
- **Column 2 (Hierarchical):** Recursive list of Platforms (e.g., INS Vikrant, INS Mormugao).
- **Column 3 (Status):** Visual indicators (icons) for software health or pending defects per platform.

## 4. Interactive States & Micro-interactions

- **Hover States:** Links transition from Gray-500 to Emerald-900 with a subtle underline animation (sliding from left to right).
- **Active State:** The current section (e.g., "The Vault") is highlighted with a small emerald dot below the text.
- **CTA Pulse:** The "+ Upload Binary" button (for D&E/BSTC) has a subtle glow effect to draw attention.

## 5. Department-Specific Logic

The Navbar dynamically adjusts based on the authenticated user's department:
- **Admin:** Adds a "User Approvals" badge with a notification count.
- **D&E / BSTC:** Displays the primary "+ Upload Binary" CTA.
- **Testing:** Displays a "Report Defect" CTA and a link to "Shipboard Forensics."

## 6. Responsive Behavior (Shipboard Optimization)
- **Tablet/Mobile:** Collapses into a "Hamburger" menu.
- **Full-Screen Modal:** The mobile menu opens as a full-screen overlay (similar to Fireart's "Menu" mode) to maximize touch targets for engineers in cramped shipboard environments.
- **Search Focus:** Global search expands to fill the entire width of the navbar when activated.

## 7. Accessibility (WCAG Compliance)
- **Contrast:** Minimum 4.5:1 ratio for all text elements against the blurred background.
- **Aria Labels:** `aria-haspopup="true"` and `aria-expanded` for all mega-menu triggers.
- **Keyboard Nav:** Logical tab order from Logo -> Discovery -> CTA -> Profile.
