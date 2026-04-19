RC-NAV-UI-01

**REDCap Project Navigation**

# 1. Document Metadata

| **Article ID** | RC-NAV-UI-01 |
| --- | --- |
| **Topic** | Project-level UI navigation and layout |
| **REDCap Module** | Core UI — applies to all projects |
| **Primary Audience** | New REDCap users, Study Coordinators, PIs |
| **Skill Level** | Beginner |
| **Prerequisites** | Logged into a REDCap instance; familiarity with basic web navigation |
| **REDCap Version** | 13.x+ (UI layout has been stable across recent major versions) |
| **Last Reviewed** | 2025-01 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-NAV-UI-02: Project Menu Reference; RC-DE-02: Basic Data Entry; RC-SURV-01: Survey Setup |

# 2. Overview

## What is this?

Every REDCap project uses a consistent two-panel layout: a persistent
left-hand menu and a variable right-hand workspace. Understanding this
layout is foundational — it is the first thing a new user encounters
and the framework through which all other REDCap features are accessed.

## Why does it matter?

New users often struggle to locate features because REDCap\'s menu is
dynamic — it changes based on user rights, enabled features, and
screen size. Understanding why items appear or disappear prevents
confusion and unnecessary support requests.

**Key terminology**

- **Menu:** The persistent left-hand panel in any REDCap project.
    Contains navigation links to all features the current user can
    access.

- **Workspace:** The right-hand panel. Changes entirely depending on
    which section of REDCap the user is working in.

- **User Rights:** Permission settings that control which menu items
    and features a given user can see and interact with. Set per
    project, not globally.

- **Hamburger mode:** A collapsed view of the left menu that activates
    when the browser window is narrow or on a mobile device. Named after
    the three-line icon used to toggle it.

- **Project Status:** One of four lifecycle stages a REDCap project
    can be in: Development, Production, Analysis/Cleanup, or Completed.
    Controls what changes are allowed.

# 3. Learning Objectives

After completing this module, the user will be able to:

- Identify the two main panels of the REDCap project interface (menu
    and workspace)

- Explain why menu items may differ between users and projects

- Navigate to a project from the REDCap home page

- Recognize and recover from hamburger mode on narrow screens or
    mobile devices

- Describe the four project status stages and their implications for
    data entry and editing

# 4. Step-by-Step Procedure

## 4.1 Navigating to a project

| **Step** | **Action & Detail** |
| --- | --- |
| **1 — Log in** | Open your institution\'s REDCap URL (see RC-INST-01 for this installation\'s URL) and log in with your credentials. You will land on the My Projects page. |
| **2 — Find your project** | Locate your project in the list. Projects can be searched or filtered. Click the project name to open it. |
| **3 — Confirm you are in the project** | The left menu will appear with project-specific sections. The workspace will show the Project Home page by default. |

## 4.2 Using the two-panel layout

Once inside a project, the interface is split into two panels that are
always present:

| **Panel** | **Description** |
| --- | --- |
| **Left — Menu** | Persistent navigation. Always visible (unless in hamburger mode). Organized into labeled sections. Changes based on user rights and enabled features. |
| **Right — Workspace** | Variable content area. Displays whatever section you have navigated to: a form designer, a data entry screen, user rights settings, reports, etc. |

## 4.3 Recovering from hamburger mode

| **Step** | **Action & Detail** |
| --- | --- |
| **1 — Recognize the state** | The left menu has disappeared. You may see a three-line icon (☰) in the upper area of the page. |
| **2 — Option A: Widen the window** | Drag your browser window wider. The menu will reappear automatically once the window exceeds the breakpoint width. |
| **3 — Option B: Click the hamburger icon** | Click the ☰ icon to toggle the menu open without resizing the window. |

> **Note:** *Hamburger mode is useful for previewing how a survey will
> look on a participant\'s mobile device while still working on a
> desktop computer.*

# 5. Questions & Answers

# 6. Common Mistakes & Gotchas

**Assuming a missing menu item is a bug**

- **What happens:** User reports that a feature is \'missing\' from
    their project when it is simply hidden due to insufficient user
    rights or a disabled project feature.

- **Prevention:** Before escalating, check (1) your user rights for
    this specific project, and (2) whether the feature is enabled in
    Project Setup. Both must be true for an item to appear.

- **Recovery:** Contact your project\'s user rights manager to review
    your permissions, or enable the feature in Project Setup if you have
    access to it.

**Collecting real data while in Development status**

- **What happens:** Users begin collecting real participant data
    before moving the project to Production. Development mode is not
    protected — structural changes can be made at any time, risking
    data integrity.

- **Prevention:** Move the project to Production status before
    collecting any real data. Use Development status only for testing
    and piloting.

- **Recovery:** Contact your REDCap administrator. Data collected in
    Development can sometimes be migrated, but this is not guaranteed.

**Marking a project as Completed prematurely**

- **What happens:** Once a project is marked Completed, all users
    (including the project owner) lose access. Only a REDCap
    administrator can reverse this.

- **Prevention:** Use Analysis/Cleanup status when data collection is
    done but you still need access. Only mark Completed when you are
    certain no further access is needed.

- **Recovery:** Contact your REDCap administrator to revert to a prior
    status.

**Confusing the REDCap Mobile App with MyCap**

- **What happens:** Users direct participants to download the wrong
    app, or misunderstand which tool supports their use case.

- **Key distinction:** REDCap Mobile App is for study staff to collect
    data offline across multiple records, then sync. MyCap is for
    individual participants to enter their own data into a single
    record.

- **Prevention:** Clarify the use case before recommending either app.
    Consult your REDCap support team before implementing either.

# 7. Related Topics

- **RC-NAV-UI-02:** Project Menu Reference — detailed guide to every
    item in the REDCap left menu

- **RC-DE-02:** Basic Data Entry — covers Record Status Dashboard
    and Add/Edit Records

- **RC-SURV-01:** Survey Setup — referenced by the Survey
    Distribution Tools menu item

- **RC-RIGHTS-01:** User Rights — how to configure permissions that
    control menu visibility

- **RC-MOB-01:** REDCap Mobile App vs. MyCap — detailed comparison
    of both mobile tools

# 8. Version & Change Notes

| **REDCap Version** | **Notes** |
| --- | --- |
| **13.x+** | Two-panel layout and hamburger mode behavior have been stable across recent major versions. |
| **14.x+** | Project status workflow and menu section names are consistent with this article as of this version. Verify section names if using an older installation. |

REDCap LLM Knowledge Base \| RC-NAV-UI-01 \| Project Navigation UI
