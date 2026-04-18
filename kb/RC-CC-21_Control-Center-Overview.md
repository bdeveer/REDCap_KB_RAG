RC-CC-21

**Control Center: Overview & Navigation**

| **Article ID** | RC-CC-21 |
| --- | --- |
| **Domain** | Control Center (Admin) |
| **Applies To** | REDCap administrators |
| **Prerequisite** | REDCap administrator access |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-CC-01 — Notifications & Reporting; RC-CC-02 — General Configuration; RC-CC-07 — Users & Access Management; RC-CC-09 — To-Do List |

---

# What Is the Control Center?

The Control Center is the administrative hub of a REDCap instance. It is only accessible to REDCap **administrators** (also called super users). Standard project users and project-level admins do not have access to the Control Center. Administrators reach it via the **Control Center** link in the left-hand navigation menu, which is only visible to accounts with administrator privileges.

From the Control Center, an administrator can configure system-wide settings, manage users, enable or disable features, monitor activity, and control how REDCap behaves across all projects on the instance.

> **Note:** Changes made in the Control Center affect the entire REDCap instance, not individual projects. Use care when modifying settings that are already in active use.

---

# Navigation Overview

The Control Center is organized into several top-level sections, each accessible from a sidebar menu. The sections and their primary purposes are:

## Control Center Home
The landing page of the Control Center. Displays system notifications, recent errors, and a to-do list for items that may need administrator attention. No configurable settings live here — it is an informational dashboard. See **RC-CC-01** for full details on the Notifications & Reporting dashboard, and **RC-CC-09** for the To-Do List.

> **REDCap Plus** — A new feature area visible in the Control Center Home menu (labeled "coming soon" as of REDCap 16.x). Details to be added as the feature becomes available.

## Administrator Resources
Links to REDCap community resources, training materials, API documentation, and plugin/hook documentation. Also includes:
- **Language File Creator/Updater** — for managing system language files
- **URL Shortener** — a utility for generating shortened URLs from any link in the system (see **RC-CC-10**)

## Dashboards & Activity
Read-only statistical and monitoring views. Includes:
- **System Statistics** — usage trends across the instance (see **RC-CC-11**)
- **User Activity Log** — per-user activity history (see **RC-CC-12**)
- **User Activity Graphs** — visual usage trend charts (see **RC-CC-13**)
- **FHIR Statistics** — activity metrics for Clinical Data Interoperability Services (FHIR) if enabled
- **Map of Users** — geographic distribution of user accounts (see **RC-CC-14**)
- **Top Usage Report** — engagement summary across projects and users (see **RC-CC-15**)
- **Recent Errors** — system error log
- **Database Activity Monitor** — in-depth query-level monitoring of the database (see **RC-CC-16**)
- **Database Query Tool** — allows administrators to run SQL queries directly against the REDCap database (see **RC-CC-17**)

## Projects
Tools for looking up and managing individual projects:
- **Browse Projects** — search and view any project on the instance
- **Edit Project Settings** — modify settings for a specific project directly; individual project defaults are configured in other sections of the Control Center
- **Link Lookup** — reverse-lookup which project a given survey or other REDCap link belongs to

## Users
Administrative tools for user account management. See **RC-CC-07** for full details. Includes:
- Browse Users
- User Allowlist
- Email Users
- API Tokens
- Banned IP Addresses
- Administrator Privileges
- Access Control Groups

## Miscellaneous Modules
Configuration for optional or institution-specific modules:
- **Multi-Language Management (MLM)** — Control Center configuration covered in **RC-CC-20**; full feature documentation in RC-MLM-01
- **Clinical Data Interoperability Services (CDIS)** — integration with clinical data sources (e.g., EHR systems)
- **Dynamic Data Pull (DDP)** — custom real-time data pull from external systems
- **Custom Application Links** — add institution-specific links to the left-hand project menu (e.g., help desk, training portal, external applications). See RC-CC-18.
- **Publication Matching** — automated nightly PubMed search to associate research projects with PI publications. See RC-CC-19.

## System Configuration
The largest section of the Control Center, containing all system-wide behavioral and technical settings. Sub-pages include:

| Sub-page | KB Article | Summary |
| --- | --- |---|
| General Configuration | RC-CC-02 | Server settings, email config, system-wide text and branding |
| Security & Authentication | RC-CC-03 | Authentication method, 2FA, login rules, security settings |
| User Settings | RC-CC-04 | Project creation permissions, user defaults, public report access |
| File Upload Settings | RC-CC-05 | Storage method, upload limits, file type-specific settings |
| Modules/Services Configuration | RC-CC-06 | Feature toggles, SMS services, e-Consent, external modules |
| Field Validation Types | RC-CC-08 | Enabled/disabled validation types, custom validations |
| Home Page Settings | RC-CC-08 | Contact info, announcement text, grant display |
| Project Templates | RC-CC-08 | Default templates available to users when creating new projects |
| Default Project Settings | RC-CC-08 | Language, encoding, logo, date format defaults for all projects |
| Footer Settings (All Projects) | RC-CC-08 | Links and text displayed in the footer across all projects |
| Cron Jobs | — | View and manage scheduled background tasks (cron job list; max concurrency configured in RC-CC-02) |
| External Modules | — | See your institution's External Modules policy |

---

# Who Can Access the Control Center?

The Control Center is visible **only to REDCap administrators** (super users). On the left navigation, regular users will not see the Control Center link. Administrator accounts are managed under **Users → Administrator Privileges** in the Control Center itself (see RC-CC-07).

Different tiers of administrator access may exist depending on instance configuration — for example, some administrators may have full system access while others are granted limited privileges for specific environments (development, test, production).
