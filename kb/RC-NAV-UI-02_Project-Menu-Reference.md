

**Project Menu Reference**

| **Article ID** | [RC-NAV-UI-02 — Project Menu Reference](RC-NAV-UI-02_Project-Menu-Reference.md) |
| --- | --- |
| **Domain** | Project Navigation |
| **Applies To** | All project types |
| **Prerequisite** | [RC-NAV-UI-01 — Project Navigation UI](RC-NAV-UI-01_Project-Navigation-UI.md) |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-NAV-UI-01 — Project Navigation UI](RC-NAV-UI-01_Project-Navigation-UI.md), [RC-NAV-REC-01 — Record Navigation Overview](RC-NAV-REC-01_Record-Navigation-Overview.md), [RC-NAV-REC-04 — Record Status Dashboard & Other Record Links](RC-NAV-REC-04_Record-Status-Dashboard-and-Links.md)[RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md)[RC-DE-02 — Basic Data Entry](RC-DE-02_Basic-Data-Entry.md), [RC-PROJ-01 — Project Lifecycle: Status and Settings](RC-PROJ-01_Project-Lifecycle-Status-and-Settings.md)[RC-FD-01 — Form Design Overview](RC-FD-01_Form-Design-Overview.md), [RC-FD-05 — Codebook](RC-FD-05_Codebook.md), [RC-EXPRT-01 — Data Export: Overview & Workflow](RC-EXPRT-01_Data-Export-Overview-and-Workflow.md)[RC-MLM-01 — Multi-Language Management](RC-MLM-01_Multi-Language-Management.md), [RC-IMP-01 — Data Import Overview](RC-IMP-01_Data-Import-Overview.md), [RC-DQ-01 — Data Quality Module](RC-DQ-01_Data-Quality-Module.md), [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md), [RC-DE-08 — Field Comment Log](RC-DE-08_Field-Comment-Log.md), [RC-DE-12 — Data Resolution Workflow](RC-DE-12_Data-Resolution-Workflow.md), [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md), [RC-SURV-01 — Surveys – Basics](RC-SURV-01_Surveys-Basics.md)[RC-SURV-05 — Participant List & Manual Survey Invitations](RC-SURV-05_Participant-List-and-Manual-Survey-Invitations.md)[RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md)[RC-RAND-01 — Randomization Concepts & Terminology](RC-RAND-01_Randomization-Concepts.md)[RC-PROJ-03 — Project Dashboards](RC-PROJ-03_Project-Dashboards.md), [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md), [RC-MOB-01 — REDCap Mobile App](RC-MOB-01_REDCap-Mobile-App.md), [RC-MYCAP-01 — MyCap: Overview & Enabling](RC-MYCAP-01_MyCap-Overview-and-Enabling.md)|
| **Synonyms** | what does each project menu item do; reference list of all left-hand menu sections; where do i find a specific feature in the menu; explanation of project menu sections and items; what menu items appear and who can see them; redcap menu item glossary; which menu option opens reports or codebook; list of every section in the project sidebar |

---

## 1. Overview

This article is a structured reference for every section and item that can appear in the REDCap left-hand project menu. The menu is divided into labeled sections, each grouping related functionality. Not all items are visible to all users — visibility depends on user rights and project configuration. Each section below lists its items in a reference table with the item name, its visibility rule, and a plain-language description of what it does.

---

## 2. Key Concepts & Definitions

**Always** — A menu item with this designation appears for any user in any project, regardless of user rights or feature configuration.

**Conditional** — A menu item with this designation appears only when the required user rights are granted and/or the relevant feature is enabled in Project Setup. Both conditions must be satisfied.

**User Rights** — Per-project permission settings that control which menu items and features a given user can see and interact with. Managed under the User Rights section of the project menu.

**External Module** — A community-developed add-on that extends REDCap functionality. Must be enabled by a REDCap administrator. Enabled modules may add their own entries to the left menu.

**Project Bookmarks** — Custom links added by a project manager that appear in the left menu. Can point to internal REDCap pages, other REDCap projects, or external websites. Configurable per user or Data Access Group. See [RC-NAV-UI-03 — Project Bookmarks](RC-NAV-UI-03_Project-Bookmarks.md).

---

## 3. Menu Section Reference

### 3.1 Top-Left Navigation

This group of links sits above the labeled menu sections and handles
global navigation — they typically take the user out of the current
project.

| **Menu Item** | **Visibility**   **What it does** |
| --- | --- |
| **REDCap logo** | Always           Returns to the My Projects page. Equivalent to clicking My Projects. |
| **My Projects** | Always           Returns to the My Projects page. Same destination as clicking the logo. |
| **Logged in as \[username\] / Log out** | Always           Displays the current username. The Log Out link ends the session completely. |
| **REDCap Messenger** | Always\*         A HIPAA-compliant in-project messaging tool for user-to-user communication. Cannot send external email, texts, or messages to other REDCap installations. (\*Availability depends on whether your institution has enabled this feature.) |
| **Contact REDCap Administrator** | Always           Links to your institution's REDCap support channel (email, website, or survey). Configured by your local admin team. See [RC-INST-01 — Institution-Specific Settings & Policies — Production](RC-INST-01_Institution-Specific-Settings-and-Policies.md) for what this link opens at this installation. |

### 3.2 Project Home and Design

This section covers features related to the setup and design of a
project. It is most relevant during the project build phase and for
ongoing project management.

| **Menu Item** | **Visibility**   **What it does** |
| --- | --- |
| **Project Home** | Always           Opens the Project Home page, which shows basic project information and summary stats. |
| **Code Book** | Always           A human-readable view of all instruments and their variables. Use the Print button to export as PDF for external sharing. |
| **Project Setup** | Conditional      The main project configuration page. Used heavily during project design. Requires Project Setup/Design user rights. |
| **Designer (Online Designer)** | Conditional      Direct link to the instrument and field design interface. Requires Project Setup/Design user rights. |
| **Dictionary (Data Dictionary)** | Conditional      Direct link to the Data Dictionary — a spreadsheet-style view of all fields. Requires Project Setup/Design user rights. |

**Project Status**

Project status is displayed and managed from the Project Home or Project
Setup pages. Any user with sufficient rights can advance the status
forward. Reverting to an earlier status requires a REDCap administrator.

| **Status** | **Visibility**   **What it means** |
| --- | --- |
| **Development** | Always           Default status. All changes are immediate. No real participant data should be collected in this status. Use for building and testing. |
| **Production** | Always           Active data collection status. Structural changes require Draft Mode and may need admin approval. Protects data from accidental field edits. |
| **Analysis / Cleanup** | Always           Data collection complete. Most functionality disabled. Data intact. Can be returned to Production at any time by a user or admin. |
| **Completed** | Always           Locks the project entirely. Only REDCap administrators can access or revert a completed project. Use only when absolutely certain no further access is needed. |

**Other Functionality & Project Revision History**

Accessible as tabs from the Project Home or Project Setup pages (for
users with appropriate rights):

- **Other Functionality:** Infrequently used administrative tools:
    advance project status, request project deletion, back up the
    project (useful when migrating between REDCap installations).

- **Project Revision History:** Shows project statistics and a full
    log of official revisions. Allows downloading any prior revision as
    a Data Dictionary and rolling back structural changes. Note: the
    Data Dictionary only restores instruments and fields — not user
    rights, survey settings, or longitudinal configuration.

### 3.3 Data Collection

The primary section for day-to-day data entry and participant
management. Users with any data entry rights will see at least the two
core items.

| **Menu Item** | **Visibility**   **What it does** |
| --- | --- |
| **Record Status Dashboard** | Always           Overview of form completion status across all records. Shows which forms are complete, incomplete, or unverified at a glance. |
| **Add / Edit Records** | Always           Create new records or look up and edit existing ones. Primary data entry entry point. |
| **Survey Distribution Tools** | Conditional      Appears when surveys are enabled in the project. Manage survey links, send email/SMS invitations, and view the invitation log. |
| **MyCap Participant Management** | Conditional      Manage participants using the MyCap mobile app. Requires MyCap to be enabled. As of MyCap 2.0 (September 2023, REDCap v13.10.0+), longitudinal projects are supported. Consult your support team before using. |
| **Record shortcuts** | Conditional      When a user is actively viewing a record, shortcuts to that record's instruments and record home page appear dynamically in this section. |

### 3.4 Applications

Features that fall outside the core design and data collection
workflows. Availability is based on user rights and project settings.
Each application is self-contained.

| **Menu Item** | **Visibility**   **What it does** |
| --- | --- |
| **Project Dashboards** | Conditional      Create aggregate data dashboards to track project progress (e.g. enrollment rates, survey responses). Dashboards can be made public — never include PHI in public dashboards. Use as an operational tool, not an analysis tool. |
| **Alerts & Notifications** | Conditional      Configure rule-based email alerts triggered by data entry events, survey completions, date comparisons, or custom logic. Supports piped (merged) REDCap field values in email content. |
| **Multi-Language Management (MLM)** | Conditional      Apply multiple language translations to instruments and parts of the REDCap interface. Useful for multilingual survey populations. REDCap identifies text that needs translation but does not translate it — use a native speaker. |
| **Calendar** | Conditional      Originally designed for longitudinal projects to track participant follow-up schedules. Not a replacement for hospital scheduling systems or a survey scheduler. Can sync with external calendaring systems. |
| **Data Exports, Reports, and Stats** | Conditional      Export project data in multiple formats (Excel, CSV, SPSS, SAS, Stata, R). Create and save custom filtered reports. Includes basic visualizations and connections to tools like Tableau. |
| **Data Import Tool** | Conditional      Import data into the project using a generated template. Validates formatting before import and shows a preview of changes including overwrite conflicts. |
| **Data Comparison Tool** | Conditional      Compare two records side by side. Primarily used with the Double Data Entry feature to identify discrepancies between two independent data entry attempts. |
| **Logging** | Conditional      Full audit log of all user activity in the project, down to page views. Filterable by user, event type, and date. Exportable — useful for regulatory compliance. |
| **Email Logging** | Conditional      Audit log of all emails sent from this project. Allows resending emails. Caution: in anonymous survey projects, this log may inadvertently link email addresses to records. |
| **Field Comment Log** | Conditional      Review and edit all comments added to specific fields across all records. Useful for capturing data situations not anticipated during design. |
| **Data Resolution Workflow (Resolve Issues)** | Conditional      Replaces the Field Comment Log when enabled. Adds the ability to assign field-level issues to specific users for resolution. Used in teams with formal data validation roles. |
| **File Repository** | Conditional      Access files uploaded to the project repository or auto-generated files (e.g., e-consent PDFs, data export files). Note: files uploaded within a record are accessed from that record, not here. |
| **User Rights** | Conditional      Manage user permissions for this project. Assign individual rights or create roles (e.g., Data Entry, Statistician, Data Coordinator) and add users to those roles. |
| **DAGs (Data Access Groups)** | Conditional      Designate record-level access groups so users only see records in their assigned group. Common use case: multi-site studies where site A users should not see site B records. |
| **Customize & Manage Locking / E-signatures** | Conditional      Configure record and instrument locking for projects requiring independent validation. Locked instruments cannot be edited by regular users. |
| **Data Quality** | Conditional      Run predefined or custom rules across the entire dataset to identify data issues (blank required fields, validation errors, custom logic violations). Used primarily during data cleaning. |
| **API** | Conditional      Generate or request an API token to allow external programs to interact with the project programmatically. Advanced feature requiring programming skills. |
| **API Playground** | Conditional      Explore and test available API methods with built-in documentation and code examples in multiple languages (PHP, Python, R, Java, etc.). |
| **REDCap Mobile App** | Conditional      Manage device connections for the REDCap Mobile App. Used for offline data collection by study staff in the field. See note below on Mobile App vs. MyCap. |
| **Custom Links** | Conditional      Links added by your local REDCap admin team pointing to institution-specific support resources (ticketing systems, training calendars, LMS portals, etc.). See [RC-INST-01 — Institution-Specific Settings & Policies — Production](RC-INST-01_Institution-Specific-Settings-and-Policies.md) for the specific links available at this installation. |

> **Note:** *REDCap Mobile App vs. MyCap: These are two separate apps
> with different purposes. REDCap Mobile App is for study staff to
> collect data offline across multiple records and then sync. MyCap is
> for individual participants to enter their own data into a single
> record on their personal device.*

### 3.5 Custom Reports & Project Dashboards (Dynamic Sections)

When a user creates custom reports or project dashboards, REDCap
automatically adds new labeled sections to the left menu listing those
reports or dashboards. These sections only appear if at least one report
or dashboard has been created and the user has access to it.

- **Reports section:** Lists all custom reports the user has access
    to. Reports can be organized into folders (defined by name, then
    reports are added to the folder) — useful for projects with large
    numbers of reports.

- **Project Dashboards section:** Lists all dashboards accessible to
    the user.

### 3.6 External Modules

External modules are community-developed add-ons that extend REDCap's
functionality. They must be downloaded and enabled by your local REDCap
admin team. This menu section only appears if at least one module is
active in the project and has a dedicated page. For the list of modules
available at this installation and the local policy on enabling them, see
**[RC-INST-01 — Institution-Specific Settings & Policies — Production](RC-INST-01_Institution-Specific-Settings-and-Policies.md)

- Click Manage in the External Modules section header to see available
    modules and enable/disable them (depending on your permissions and
    local policy).

- View Logs is available for module developers and troubleshooting ---
    not typically needed by end users.

> **⚠ Warning:** *External modules are reviewed by Vanderbilt at
> submission time, but that is not an ongoing guarantee of functionality
> or continued support. All modules are built by volunteers. Use at your
> own risk and consult your REDCap admin before enabling unfamiliar
> modules.*

### 3.7 Help & Information

Support and documentation resources. Always visible to all users.

| **Menu Item** | **Visibility**   **What it does** |
| --- | --- |
| **Help & FAQ** | Always           Links to the Help & FAQ section on the REDCap home page. Good first stop for common questions. |
| **Video Tutorials** | Always           Links to Vanderbilt's official REDCap training videos. These are generic and do not reflect institution-specific configurations. |
| **Suggest a New Feature** | Always           Submits a feature idea to the Vanderbilt REDCap development team. Not a support channel — no direct response is given. Suggestions may influence the development roadmap over time. |
| **Contact REDCap Administrator** | Always           Connects to your institution's support team. Includes project metadata automatically so the support team knows which project you are asking about. This is the correct channel for immediate assistance. |

---

## 4. Common Questions

**Q: Why is a menu item not visible for a specific user?**
Two conditions must both be true for a menu item to appear: the user's rights for this project must include the relevant permission, and the feature must be enabled in Project Setup. Check both before concluding something is missing or broken.

**Q: Why does the same user see a different menu in different projects?**
User rights are set per project, not globally. A user may have full rights in one project and read-only access in another, resulting in different visible menus.

**Q: What is the difference between "Custom Links" and "Project Bookmarks"?**
Custom Links are added by the local REDCap administrator and point to institution-wide resources (support portals, training calendars, etc.). Project Bookmarks are added by a project manager within a specific project and point to project-relevant resources. Both appear in the left menu but are configured in different places. See [RC-NAV-UI-03 — Project Bookmarks](RC-NAV-UI-03_Project-Bookmarks.md).

**Q: Can I add items to the left menu?**
Project managers can add Project Bookmarks (custom links visible to project users) via the Project Bookmarks section. REDCap administrators can add Custom Links visible across all projects. End users cannot add items to the menu.

---

## 5. Common Mistakes & Gotchas

**Using 'Suggest a New Feature' for support requests**

- **What happens:** User submits a support request through the feature
    suggestion tool and never receives a response. The Vanderbilt team
    does not reply to suggestions individually.

- **Prevention:** For immediate help, always use Contact REDCap
    Administrator, which reaches your local support team and includes
    helpful project metadata.

**Including PHI in a public Project Dashboard**

- **What happens:** A dashboard containing participant health
    information is made publicly accessible without login, creating a
    potential HIPAA/data privacy violation.

- **Prevention:** Before making any dashboard public, audit every
    field and visualization for PHI. When in doubt, keep it private.

**Relying on the Calendar app for survey scheduling**

- **What happens:** Users expect the Calendar to schedule survey sends
    or appointment reminders, but it does not — it is a display tool,
    not a scheduler.

- **Prevention:** Use Automated Survey Invitations (in the Online
    Designer) or Alerts & Notifications to trigger time-based survey
    sends.

**Downloading files from File Repository instead of the record**

- **What happens:** User looks in the File Repository for a file that
    was uploaded within a specific record and cannot find it there.

- **Prevention:** Files uploaded in a record field (e.g., a file
    upload field in a form) are stored in the record, not the File
    Repository. Navigate to the record and the relevant instrument to
    access them. The File Repository holds project-level files and
    REDCap-generated outputs.

**Enabling external modules without vetting them**

- **What happens:** An external module causes unexpected behavior or
    breaks when REDCap is updated, with no support pathway available.

- **Prevention:** Check with your REDCap admin before enabling any
    module. Understand that modules are community-maintained and support
    is not guaranteed.

---

## 6. Related Articles

- [RC-NAV-UI-01 — Project Navigation UI](RC-NAV-UI-01_Project-Navigation-UI.md) — the two-panel layout, hamburger mode, and project status overview
- [RC-NAV-UI-03 — Project Bookmarks](RC-NAV-UI-03_Project-Bookmarks.md) — creating custom links on the left-hand project menu
- [RC-NAV-REC-01 — Record Navigation Overview](RC-NAV-REC-01_Record-Navigation-Overview.md) — navigating to records and instruments from the Data Collection section
- [RC-NAV-REC-04 — Record Status Dashboard & Other Record Links](RC-NAV-REC-04_Record-Status-Dashboard-and-Links.md) — detailed guide to the dashboard, custom dashboards, and all locations that link to records
- [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md) — how to configure permissions that control which menu items a user can see
- [RC-PROJ-01 — Project Lifecycle: Status and Settings](RC-PROJ-01_Project-Lifecycle-Status-and-Settings.md) — detailed guide to the four project status stages shown in the Project Home and Design section
- [RC-FD-01 — Form Design Overview](RC-FD-01_Form-Design-Overview.md) — background for the Designer, Dictionary, and Code Book menu items
- [RC-FD-05 — Codebook](RC-FD-05_Codebook.md) — the read-only instrument/field reference listed under Project Home and Design
- [RC-DE-02 — Basic Data Entry](RC-DE-02_Basic-Data-Entry.md) — covers Record Status Dashboard and Add/Edit Records in depth

- **[RC-SURV-01 — Surveys – Basics](RC-SURV-01_Surveys-Basics.md):** Surveys – Basics — covers survey enabling and the
    Survey Distribution Tools menu item

- **[RC-SURV-05 — Participant List & Manual Survey Invitations](RC-SURV-05_Participant-List-and-Manual-Survey-Invitations.md):** Participant List & Manual Survey Invitations —
    detailed guide to the participant list accessible from Survey
    Distribution Tools

- **[RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md):** Alerts & Notifications: Setup — detailed
    configuration guide for the Alerts & Notifications menu item

- **[RC-MLM-01 — Multi-Language Management](RC-MLM-01_Multi-Language-Management.md):** Multi-Language Management — detailed guide to the
    MLM application listed under Applications

- **[RC-EXPRT-01 — Data Export: Overview & Workflow](RC-EXPRT-01_Data-Export-Overview-and-Workflow.md):** Data Export: Overview & Workflow — detailed
    guide to the Data Exports, Reports, and Stats menu item

- **[RC-IMP-01 — Data Import Overview](RC-IMP-01_Data-Import-Overview.md):** Data Import Overview — detailed guide to the Data
    Import Tool menu item

- **[RC-DQ-01 — Data Quality Module](RC-DQ-01_Data-Quality-Module.md):** Data Quality Module — detailed guide to the Data
    Quality menu item

- **[RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md):** Data Access Groups — detailed guide to the DAGs
    menu item

- **[RC-DE-08 — Field Comment Log](RC-DE-08_Field-Comment-Log.md):** Field Comment Log — detailed guide to the Field
    Comment Log menu item under Applications

- **[RC-DE-12 — Data Resolution Workflow](RC-DE-12_Data-Resolution-Workflow.md):** Data Resolution Workflow — detailed guide to the
    Data Resolution Workflow (Resolve Issues) menu item

- **[RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md):** Longitudinal Project Setup — background for the
    Calendar application, which is designed for longitudinal
    follow-up tracking

- **[RC-RAND-01 — Randomization Concepts & Terminology](RC-RAND-01_Randomization-Concepts.md):** Randomization Concepts — background for the
    Randomization application (appears when randomization is enabled)

- **[RC-PROJ-03 — Project Dashboards](RC-PROJ-03_Project-Dashboards.md):** Project Dashboards — creating and configuring
    custom project dashboards (Custom Reports & Project Dashboards
    menu section)

- **[RC-API-01 — REDCap API](RC-API-01_REDCap-API.md):** REDCap API — introduction to the API and API
    Playground menu items

- **[RC-MOB-01 — REDCap Mobile App](RC-MOB-01_REDCap-Mobile-App.md):** REDCap Mobile App — detailed guide to the REDCap
    Mobile App menu item for offline data collection

- **[RC-MYCAP-01 — MyCap: Overview & Enabling](RC-MYCAP-01_MyCap-Overview-and-Enabling.md):** MyCap: Overview & Enabling — detailed guide to
    the MyCap Participant Management menu item
