---
id: RC-NAV-UI-01
title: Project Navigation UI
domain: Project Navigation
applies_to:
- All project types
requires: Any supported version
verified_against: REDCap v17.4.1 (Standard) / v17.3.7 (LTS) — changelog review; page
  not re-captured
prerequisites:
- None
version: '1.1'
last_updated: '2026'
related:
- id: RC-NAV-UI-02
  title: 'Project Menu Reference, RC-NAV-UI-04 — My Projects Page, RC-NAV-REC-01 —
    Record Navigation Overview, RC-PROJ-01 — Project Lifecycle: Status and SettingsRC-DE-02
    — Basic Data Entry, RC-SURV-01 — Surveys – BasicsRC-USER-01 — User Rights: Overview
    & Three-Tier AccessRC-MYCAP-01 — MyCap: Overview & EnablingRC-FD-01 — Form Design
    Overview, RC-MOB-01 — REDCap Mobile App'
tags:
- project navigation
synonyms:
- how is the redcap project screen laid out
- what is the left-hand menu
- why do some menu items not show up for me
- how to expand the collapsed hamburger menu
- understanding the project layout and workspace
- where are project features located on screen
- why does the menu change between users
- redcap two-panel project interface
---

# 1. Overview

Every REDCap project uses a consistent two-panel layout: a persistent left-hand menu and a variable right-hand workspace. Understanding this layout is foundational — it is the first thing a new user encounters and the framework through which all other REDCap features are accessed. New users often struggle to locate features because REDCap's menu is dynamic — it changes based on user rights, enabled features, and screen size. Understanding why items appear or disappear prevents confusion and unnecessary support requests.

---

# 2. Key Concepts & Definitions

**Menu** — The persistent left-hand panel in any REDCap project. Contains navigation links to all features the current user can access. Organized into labeled sections (see [RC-NAV-UI-02 — Project Menu Reference](RC-NAV-UI-02_Project-Menu-Reference.md) for a full breakdown).

**Workspace** — The right-hand panel. Changes entirely depending on which section of REDCap the user is working in: a form designer, a data entry screen, user rights settings, reports, and so on.

**User Rights** — Permission settings that control which menu items and features a given user can see and interact with. Set per project, not globally.

**Hamburger mode** — A collapsed view of the left menu that activates when the browser window is narrow or on a mobile device. Named after the three-line icon (☰) used to toggle it. The menu is still accessible; it is just hidden by default to save screen space.

**Project Status** — One of four lifecycle stages a REDCap project can be in: Development, Production, Analysis/Cleanup, or Completed. Controls what changes are allowed and whether certain menu items appear. See [RC-PROJ-01 — Project Lifecycle: Status and Settings](RC-PROJ-01_Project-Lifecycle-Status-and-Settings.md) for full details.

---

# 3. Step-by-Step Procedure

## 3.1 Navigating to a project

| **Step** | **Action & Detail** |
| --- | --- |
| **1 — Log in** | Open your institution's REDCap URL (see [RC-INST-01 — Institution-Specific Settings & Policies — Production](RC-INST-01_Institution-Specific-Settings-and-Policies.md) for this installation's URL) and log in with your credentials. You will land on the My Projects page. |
| **2 — Find your project** | Locate your project in the list. Projects can be searched or filtered. Click the project name to open it. |
| **3 — Confirm you are in the project** | The left menu will appear with project-specific sections. The workspace will show the Project Home page by default. |

## 3.2 Using the two-panel layout

Once inside a project, the interface is split into two panels that are always present:

| **Panel** | **Description** |
| --- | --- |
| **Left — Menu** | Persistent navigation. Always visible (unless in hamburger mode). Organized into labeled sections. Changes based on user rights and enabled features. |
| **Right — Workspace** | Variable content area. Displays whatever section you have navigated to: a form designer, a data entry screen, user rights settings, reports, etc. |

## 3.3 Recovering from hamburger mode

| **Step** | **Action & Detail** |
| --- | --- |
| **1 — Recognize the state** | The left menu has disappeared. You may see a three-line icon (☰) in the upper area of the page. |
| **2 — Option A: Widen the window** | Drag your browser window wider. The menu will reappear automatically once the window exceeds the breakpoint width. |
| **3 — Option B: Click the hamburger icon** | Click the ☰ icon to toggle the menu open without resizing the window. |

> **Note:** Hamburger mode is useful for previewing how a survey will look on a participant's mobile device while still working on a desktop computer.

---

# 4. Common Questions

**Q: Why can't I see a feature I expect to find in the menu?**
Menu items are only visible when two conditions are both true: (1) your user rights for this specific project include access to that feature, and (2) the feature is enabled in Project Setup. Check both before concluding something is missing.

**Q: Why does the menu look different on someone else's screen?**
Each user's menu reflects their individual user rights and the project's feature settings. Two users in the same project can see different menus if their rights differ.

**Q: The left menu has disappeared — what happened?**
The browser window is likely too narrow, triggering hamburger mode. Widen the window or click the ☰ icon to restore the menu.

**Q: Can I get back to My Projects without logging out?**
Yes. Click the REDCap logo or the My Projects link at the top of the left menu from within any project.

---

# 5. Common Mistakes & Gotchas

**Assuming a missing menu item is a bug.** Before escalating, check (1) your user rights for the specific project, and (2) whether the feature is enabled in Project Setup. Both must be true for an item to appear. Contact the project's user rights manager to review permissions, or enable the feature in Project Setup if you have access.

**Collecting real data while in Development status.** Development mode is not protected — structural changes can be made at any time, risking data integrity. Move the project to Production status before collecting any real participant data. If data has already been collected in Development, contact your REDCap administrator; migration is possible but not guaranteed.

**Marking a project as Completed prematurely.** Once a project is marked Completed, all users (including the project owner) lose access. Only a REDCap administrator can reverse this. Use Analysis/Cleanup status when data collection is done but access is still needed.

**Confusing the REDCap Mobile App with MyCap.** The REDCap Mobile App is for study staff to collect data offline across multiple records, then sync. MyCap is for individual participants to enter their own data into a single record. Directing participants to the wrong app causes onboarding failures. Clarify the use case before recommending either.

---

# 6. Related Articles

- [RC-NAV-UI-02 — Project Menu Reference](RC-NAV-UI-02_Project-Menu-Reference.md) — detailed guide to every item in the REDCap left menu
- [RC-NAV-REC-01 — Record Navigation Overview](RC-NAV-REC-01_Record-Navigation-Overview.md) — how to navigate to records and instruments once inside a project
- [RC-PROJ-01 — Project Lifecycle: Status and Settings](RC-PROJ-01_Project-Lifecycle-Status-and-Settings.md) — detailed coverage of Development, Production, Analysis/Cleanup, and Completed stages
- [RC-DE-02 — Basic Data Entry](RC-DE-02_Basic-Data-Entry.md) — covers Record Status Dashboard and Add/Edit Records
- [RC-SURV-01 — Surveys – Basics](RC-SURV-01_Surveys-Basics.md) — referenced by the Survey Distribution Tools menu item
- [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md) — how to configure permissions that control which menu items a user can see
- [RC-FD-01 — Form Design Overview](RC-FD-01_Form-Design-Overview.md) — covers the Online Designer and Data Dictionary accessible from the Project Home and Design menu section
- [RC-MOB-01 — REDCap Mobile App](RC-MOB-01_REDCap-Mobile-App.md) — offline data collection for study staff
- [RC-MYCAP-01 — MyCap: Overview & Enabling](RC-MYCAP-01_MyCap-Overview-and-Enabling.md) — participant-facing mobile data entry; distinct from the REDCap Mobile App
