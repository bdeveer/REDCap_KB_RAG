

**Control Center: Overview & Navigation**

| **Article ID** | [RC-CC-21 — Control Center: Overview & Navigation](RC-CC-21_Control-Center-Overview.md) |
|---|---|
| **Domain** | Control Center (Admin) |
| **Applies To** | REDCap administrators |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.5.6 (Standard) — checked live on a test instance, read-only: the menu structure and privilege list; v17.3.7 (LTS) — changelog review only; v16.0.59 (LTS) — checked live on a test instance, read-only: the menu |
| **Prerequisite** | REDCap administrator access |
| **Version** | 1.3 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-CC-01 — Control Center: Notifications & Reporting (Dashboard)](RC-CC-01_Control-Center-Notifications-and-Reporting.md); [RC-CC-02 — Control Center: General System Configuration](RC-CC-02_Control-Center-General-Configuration.md); [RC-CC-07 — Control Center: Users & Access Management](RC-CC-07_Control-Center-User-Management.md); [RC-CC-09 — Control Center: To-Do List](RC-CC-09_To-Do-List.md); [RC-CC-25 — Control Center: Access Control Groups](RC-CC-25_Access-Control-Groups.md)|
| **Synonyms** | control center overview and navigation; what is the redcap control center; how do i access the control center; admin hub for system-wide settings; who can access the control center; control center sidebar navigation; super user administrative area redcap; intro to the control center for admins; control center menu differences on lts 16 |

---

## 1. Overview

The Control Center is the administrative hub of a REDCap instance. It is only accessible to REDCap **administrators** (also called super users). Standard project users and project-level admins do not have access to the Control Center. Administrators reach it via the **Control Center** link in the left-hand navigation menu, which is only visible to accounts with administrator privileges.

From the Control Center, an administrator can configure system-wide settings, manage users, enable or disable features, monitor activity, and control how REDCap behaves across all projects on the instance.

> **Note:** Changes made in the Control Center affect the entire REDCap instance, not individual projects. Use care when modifying settings that are already in active use.

---

## 2. Navigation Overview

The Control Center is organized into several top-level sections, each accessible from a sidebar menu. The sections and their primary purposes are:

> **Version caveat (16.0.59 LTS):** The menu has no **AI Configuration Settings** (AI is on Modules/Services Configuration), **Project Migration Dashboard**, **Project Administrator Groups** or **REDCap SHARE**. Three items also have older labels: **REDCap Plus** (REDCap+), **Language File Creator/Updater** (Language File Updater) and **Fix Legacy Image/File URL** (Fix Legacy Image/File URLs).

### Control Center Home
The landing page of the Control Center, **Notifications & Reporting**, displays server information, system notifications and stats reporting. No configurable settings live here. The **To-Do List** and **REDCap+** are separate pages in this section; **Recent Errors** is under Dashboards & Activity. See **[RC-CC-01 — Control Center: Notifications & Reporting (Dashboard)](RC-CC-01_Control-Center-Notifications-and-Reporting.md)** for full details on the Notifications & Reporting dashboard, and **[RC-CC-09 — Control Center: To-Do List](RC-CC-09_To-Do-List.md)** for the To-Do List.

> **REDCap Plus** — A subscription add-on visible in the Control Center Home menu that unlocks premium features. See **[RC-PLUS-01 — REDCap+: Overview and Subscription](RC-PLUS-01_REDCap-Plus-Overview-and-Subscription.md)** for details.

### Administrator Resources
Links to REDCap community resources, training materials, API documentation, and plugin/hook documentation. Also includes:
- **Language File Updater** — for managing system language files. On 17.5.6 it also has **Validate a Language File**, which checks an uploaded or pasted `.ini` file's syntax in the browser. 16.0.59 LTS doesn't have the validator
- **URL Shortener** — a utility for generating shortened URLs from any link in the system (see **[RC-CC-10 — Control Center: URL Shortener](RC-CC-10_URL-Shortener.md)**)

### Dashboards & Activity
Read-only statistical and monitoring views. Includes:
- **System Statistics** — usage trends across the instance (see **[RC-CC-11 — Control Center: System Statistics](RC-CC-11_System-Statistics.md)**)
- **User Activity Log** — per-user activity history (see **[RC-CC-12 — Control Center: User Activity Log](RC-CC-12_User-Activity-Log.md)**)
- **User Activity Graphs** — visual usage trend charts (see **[RC-CC-13 — Control Center: User Activity Graphs](RC-CC-13_User-Activity-Graphs.md)**)
- **FHIR Statistics** — activity metrics for Clinical Data Interoperability Services (FHIR) if enabled
- **Map of Users** — geographic distribution of user accounts (see **[RC-CC-14 — Control Center: Map of Users](RC-CC-14_Map-of-Users.md)**)
- **Top Usage Report** — engagement summary across projects and users (see **[RC-CC-15 — Control Center: Top Usage Report](RC-CC-15_Top-Usage-Report.md)**)
- **Recent Errors** — system error log; opens in the Database Query Tool, so it stays locked until that tool is enabled
- **Database Activity Monitor** — in-depth query-level monitoring of the database (see **[RC-CC-16 — Control Center: Database Activity Monitor](RC-CC-16_Database-Activity-Monitor.md)**)
- **Database Query Tool** — allows administrators to run SQL queries directly against the REDCap database (see **[RC-CC-17 — Control Center: Database Query Tool](RC-CC-17_Database-Query-Tool.md)**)

### Projects
Tools for looking up and managing individual projects:
- **Browse Projects** — search and view any project on the instance
- **Edit Project Settings** — modify settings for a specific project directly; individual project defaults are configured in other sections of the Control Center
- **Link Lookup** — reverse-lookup which project and record a given REDCap link belongs to. Rebranded from "Survey Link Lookup" in 15.9.0 and expanded beyond survey links to also search **survey queue links, public report links and public project dashboard links**
- **Fix Legacy Image/File URLs** — regenerates a working URL from a broken legacy link (see [RC-CC-02 — Control Center: General System Configuration](RC-CC-02_Control-Center-General-Configuration.md))
- **Project Migration Dashboard** — REDCap+ label; monitors migrations into this server (see [RC-PLUS-02 — REDCap+: Project Migration Tool](RC-PLUS-02_Project-Migration-Tool.md))

### Users
Administrative tools for user account management. See **[RC-CC-07 — Control Center: Users & Access Management](RC-CC-07_Control-Center-User-Management.md)** for full details. Includes:
- Browse Users
- Add Users (Table-based Only)
- User Allowlist
- Email Users
- API Tokens
- Banned IP Addresses
- Administrator Privileges
- Project Administrator Groups (REDCap+; see [RC-PLUS-04 — REDCap+: Project Administrator Groups (PAGs)](RC-PLUS-04_Project-Administrator-Groups.md))
- [Access Control Groups](RC-CC-25_Access-Control-Groups.md)

### Miscellaneous Modules
Configuration for optional or institution-specific modules:
- **Multi-Language Management (MLM)** — Control Center configuration covered in **[RC-CC-20 — Control Center: Multi-Language Management](RC-CC-20_Multi-Language-Management.md)**; full feature documentation in [RC-MLM-01 — Multi-Language Management](RC-MLM-01_Multi-Language-Management.md)
- **Clinical Data Interoperability Services (CDIS)** — integration with clinical data sources (e.g., EHR systems)
- **REDCap SHARE** — REDCap+ label; participant-driven sharing of EHR data (see [RC-PLUS-01 — REDCap+: Overview and Subscription](RC-PLUS-01_REDCap-Plus-Overview-and-Subscription.md))
- **Dynamic Data Pull (DDP)** — custom real-time data pull from external systems
- **Custom Application Links** — add institution-specific links to the left-hand project menu (e.g., help desk, training portal, external applications). See [RC-CC-18 — Control Center: Custom Application Links](RC-CC-18_Custom-Application-Links.md).
- **Publication Matching** — automated nightly PubMed search to associate research projects with PI publications. See [RC-CC-19 — Control Center: Publication Matching](RC-CC-19_Publication-Matching.md).

### System Configuration
The largest section of the Control Center, containing all system-wide behavioral and technical settings. Sub-pages include:

| Sub-page | KB Article | Summary |
| --- | --- |---|
| Configuration Check | [RC-CC-02 — Control Center: General System Configuration](RC-CC-02_Control-Center-General-Configuration.md) | Diagnostic tests for the installation |
| MyCap Configuration Check | [RC-CC-02 — Control Center: General System Configuration](RC-CC-02_Control-Center-General-Configuration.md) | Diagnostic tests for MyCap |
| General Configuration | [RC-CC-02 — Control Center: General System Configuration](RC-CC-02_Control-Center-General-Configuration.md) | Server settings, email config, system-wide text and branding |
| Security & Authentication | [RC-CC-03 — Control Center: Security & Authentication](RC-CC-03_Control-Center-Security-and-Authentication.md) | Authentication method, 2FA, login rules, security settings |
| User Settings | [RC-CC-04 — Control Center: User Settings & Defaults](RC-CC-04_Control-Center-User-Settings.md) | Project creation permissions, user defaults, public report access |
| File Upload Settings | [RC-CC-05 — Control Center: File Storage & Upload Settings](RC-CC-05_Control-Center-File-Storage-Settings.md) | Storage method, upload limits, file type-specific settings |
| Modules/Services Configuration | [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md) | Feature toggles, SMS services, e-Consent, external modules |
| AI Configuration Settings | [RC-CC-26 — Control Center: AI Configuration Settings](RC-CC-26_Control-Center-AI-Configuration-Settings.md) | Named AI configurations and their scope |
| Field Validation Types | [RC-CC-08 — Control Center: Home Page, Templates & Project Defaults](RC-CC-08_Control-Center-Home-Page-Templates-and-Defaults.md) | Enabled/disabled validation types, custom validations |
| Home Page Settings | [RC-CC-08 — Control Center: Home Page, Templates & Project Defaults](RC-CC-08_Control-Center-Home-Page-Templates-and-Defaults.md) | Contact info, announcement text, grant display |
| Project Templates | [RC-CC-08 — Control Center: Home Page, Templates & Project Defaults](RC-CC-08_Control-Center-Home-Page-Templates-and-Defaults.md) | Default templates available to users when creating new projects |
| Default Project Settings | [RC-CC-08 — Control Center: Home Page, Templates & Project Defaults](RC-CC-08_Control-Center-Home-Page-Templates-and-Defaults.md) | Language, encoding, logo, date format defaults for all projects |
| Footer Settings (All Projects) | [RC-CC-08 — Control Center: Home Page, Templates & Project Defaults](RC-CC-08_Control-Center-Home-Page-Templates-and-Defaults.md) | Links and text displayed in the footer across all projects |
| Cron Jobs | — | View and manage scheduled background tasks (cron job list; max concurrency configured in [RC-CC-02 — Control Center: General System Configuration](RC-CC-02_Control-Center-General-Configuration.md)) |

### External Modules
A separate section of the menu with two pages: **Manage** (enable, configure and update modules) and **View Logs**. See [RC-EM-01 — External Modules: Overview & Manager](RC-EM-01_External-Modules-Overview-and-Manager.md).

---

## 3. Who Can Access the Control Center?

The Control Center is visible **only to REDCap administrators** (super users). On the left navigation, regular users will not see the Control Center link. Administrator accounts are managed under **Users → Administrator Privileges** in the Control Center itself (see [RC-CC-07 — Control Center: Users & Access Management](RC-CC-07_Control-Center-User-Management.md)).

Administrator access is split into seven separate privileges, and a user can hold any mix of them. See [RC-CC-07 — Control Center: Users & Access Management](RC-CC-07_Control-Center-User-Management.md).

---

## 4. Common Questions

**Q: If I make a change in the Control Center, how quickly does it take effect across all projects?**
Most Control Center changes take effect immediately. For example, disabling a feature, enabling a module, or changing email settings updates the behavior system-wide right away. However, some changes may require users to log out and log back in to see the effect, or may only apply to new data created after the change. Always document when you make changes so you can explain timing to affected users.

**Q: Can I restrict certain administrators to have limited Control Center access (e.g., only certain sections)?**
Yes. The **Administrator Privileges** page has seven separate privileges, such as Manage user accounts and Modify system configuration pages, granted per user. Project-level admins never have Control Center access.

**Q: What happens if two administrators make changes to the Control Center settings at the same time?**
REDCap typically handles concurrent changes gracefully, but if two administrators save contradictory settings simultaneously, the last save will overwrite the previous one. To avoid confusion, coordinate major changes with your administration team or use a change management log to document who is making what changes and when.

**Q: Can project users see the Control Center?**
No. Standard project users and project-level admins do not have access to the Control Center. The Control Center link only appears in the left-hand menu for accounts with super-user administrator privileges. Project-level admins can configure their own project settings, but they cannot access system-wide Control Center functions.

**Q: How do I know which Control Center changes are safe to make on a live (production) instance?**
Many Control Center changes are low-risk (e.g., updating contact information, adding custom links). However, some changes are disruptive (e.g., disabling a feature used by active projects, changing authentication settings). Review the documentation for each setting, test changes in a development instance first if possible, and communicate planned changes to relevant project managers before implementing on production.

---

## 5. Common Mistakes & Gotchas

**Making system-wide changes without considering impacts on active projects.** Control Center settings affect all projects on the instance. For example, disabling file uploads, changing field validation types, or modifying default project settings impacts every project immediately. Always assess the downstream effects before making changes, and communicate with project managers when you are making system-wide modifications.

**Forgetting to save changes before navigating away from a Control Center page.** Some Control Center pages do not auto-save. If you make changes and navigate away without clicking "Save" or pressing CTRL+S, your changes will be lost. Make it a habit to explicitly save before moving to another page or section.

**Assuming Control Center changes automatically apply to existing projects or data.** Many Control Center settings establish defaults for *new* projects or *new* data created after the change. Existing projects and historical data may not be affected by system-wide changes. For example, changing the default language or date format applies to new projects, but projects created before the change retain their previous settings. Always clarify whether a setting applies retroactively or only to new items.

---

## 6. Related Articles

- [RC-CC-01 — Control Center: Notifications & Reporting (Dashboard)](RC-CC-01_Control-Center-Notifications-and-Reporting.md)
- [RC-CC-02 — Control Center: General System Configuration](RC-CC-02_Control-Center-General-Configuration.md)
- [RC-CC-07 — Control Center: Users & Access Management](RC-CC-07_Control-Center-User-Management.md)
- [RC-CC-09 — Control Center: To-Do List](RC-CC-09_To-Do-List.md)
- [RC-CC-25 — Control Center: Access Control Groups](RC-CC-25_Access-Control-Groups.md)
