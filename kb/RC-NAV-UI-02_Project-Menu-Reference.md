**REDCap Project Menu Reference**

*RC-NAV-UI-02 \| Complete guide to the left-hand project menu*

**1. Document Metadata**

  ---------------------- -------------------------------------------------------------------------------------------------------------------
  **Topic**              Left-hand project menu --- all sections and items
  **REDCap Module**      Core UI --- applies to all projects
  **Primary Audience**   New REDCap users, Study Coordinators, PIs
  **Skill Level**        Beginner to Intermediate
  **Prerequisites**      RC-NAV-UI-01: Project Navigation UI (menu/workspace layout, hamburger mode)
  **REDCap Version**     14.x+ (item names and availability may vary slightly in older versions)
  **Last Reviewed**      2025-01
  **Related Topics**     RC-NAV-UI-01: Navigation UI; RC-RIGHTS-01: User Rights; RC-DE-02: Data Entry; RC-SURV-01: Surveys; RC-API-01: API
  ---------------------- -------------------------------------------------------------------------------------------------------------------

**2. Overview**

**What is this?**

This document is a structured reference for every section and item that
can appear in the REDCap left-hand project menu. The menu is divided
into five named sections, each grouping related functionality. Not all
items are visible to all users --- visibility depends on user rights and
project configuration.

**Why does it matter?**

The left menu is the primary navigation system for any REDCap project.
Knowing what each item does --- and why it might or might not appear ---
prevents confusion, reduces support requests, and helps users work more
independently.

**How to use this document**

Each menu section below lists its items in a reference table with three
columns: the item name, whether it is always visible or conditional, and
a plain-language description. Conditional items require either
sufficient user rights, an enabled project feature, or both.

**3. Learning Objectives**

After reviewing this reference, the user will be able to:

-   Identify which menu section contains a given REDCap feature

-   Explain why a menu item might not be visible for a given user or
    project

-   Distinguish between items that are always present and those that are
    conditional

-   Describe the purpose of each menu item at a functional level

-   Identify the correct menu item when trying to accomplish a specific
    task

**4. Menu Section Reference**

> **Note:** *\'Always\' means the item appears for any user in any
> project. \'Conditional\' means it requires specific user rights and/or
> an enabled feature.*

**4.1 Top-Left Navigation**

This group of links sits above the labeled menu sections and handles
global navigation --- they typically take the user out of the current
project.

  ----------------------------------------- ---------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Menu Item**                             **Visibility**   **What it does**
  **REDCap logo**                           Always           Returns to the My Projects page. Equivalent to clicking My Projects.
  **My Projects**                           Always           Returns to the My Projects page. Same destination as clicking the logo.
  **Logged in as \[username\] / Log out**   Always           Displays the current username. The Log Out link ends the session completely.
  **REDCap Messenger**                      Always\*         A HIPAA-compliant in-project messaging tool for user-to-user communication. Cannot send external email, texts, or messages to other REDCap installations. (\*Availability depends on whether your institution has enabled this feature.)
  **Contact REDCap Administrator**          Always           Links to your institution\'s REDCap support channel (email, website, or survey). Configured by your local admin team. See RC-INST-01 for what this link opens at this installation.
  ----------------------------------------- ---------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**4.2 Project Home and Design**

This section covers features related to the setup and design of a
project. It is most relevant during the project build phase and for
ongoing project management.

  ---------------------------------- ---------------- ---------------------------------------------------------------------------------------------------------------------------
  **Menu Item**                      **Visibility**   **What it does**
  **Project Home**                   Always           Opens the Project Home page, which shows basic project information and summary stats.
  **Code Book**                      Always           A human-readable view of all instruments and their variables. Use the Print button to export as PDF for external sharing.
  **Project Setup**                  Conditional      The main project configuration page. Used heavily during project design. Requires Project Setup/Design user rights.
  **Designer (Online Designer)**     Conditional      Direct link to the instrument and field design interface. Requires Project Setup/Design user rights.
  **Dictionary (Data Dictionary)**   Conditional      Direct link to the Data Dictionary --- a spreadsheet-style view of all fields. Requires Project Setup/Design user rights.
  ---------------------------------- ---------------- ---------------------------------------------------------------------------------------------------------------------------

**Project Status**

Project status is displayed and managed from the Project Home or Project
Setup pages. Any user with sufficient rights can advance the status
forward. Reverting to an earlier status requires a REDCap administrator.

  ------------------------ ---------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Status**               **Visibility**   **What it means**
  **Development**          Always           Default status. All changes are immediate. No real participant data should be collected in this status. Use for building and testing.
  **Production**           Always           Active data collection status. Structural changes require Draft Mode and may need admin approval. Protects data from accidental field edits.
  **Analysis / Cleanup**   Always           Data collection complete. Most functionality disabled. Data intact. Can be returned to Production at any time by a user or admin.
  **Completed**            Always           Locks the project entirely. Only REDCap administrators can access or revert a completed project. Use only when absolutely certain no further access is needed.
  ------------------------ ---------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------

**Other Functionality & Project Revision History**

Accessible as tabs from the Project Home or Project Setup pages (for
users with appropriate rights):

-   **Other Functionality:** Infrequently used administrative tools:
    advance project status, request project deletion, back up the
    project (useful when migrating between REDCap installations).

-   **Project Revision History:** Shows project statistics and a full
    log of official revisions. Allows downloading any prior revision as
    a Data Dictionary and rolling back structural changes. Note: the
    Data Dictionary only restores instruments and fields --- not user
    rights, survey settings, or longitudinal configuration.

**4.3 Data Collection**

The primary section for day-to-day data entry and participant
management. Users with any data entry rights will see at least the two
core items.

  ---------------------------------- ---------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Menu Item**                      **Visibility**   **What it does**
  **Record Status Dashboard**        Always           Overview of form completion status across all records. Shows which forms are complete, incomplete, or unverified at a glance.
  **Add / Edit Records**             Always           Create new records or look up and edit existing ones. Primary data entry entry point.
  **Survey Distribution Tools**      Conditional      Appears when surveys are enabled in the project. Manage survey links, send email/SMS invitations, and view the invitation log.
  **MyCap Participant Management**   Conditional      Manage participants using the MyCap mobile app. Requires MyCap to be enabled; mutually exclusive with longitudinal mode. Consult your support team before using.
  **Record shortcuts**               Conditional      When a user is actively viewing a record, shortcuts to that record\'s instruments and record home page appear dynamically in this section.
  ---------------------------------- ---------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------

**4.4 Applications**

Features that fall outside the core design and data collection
workflows. Availability is based on user rights and project settings.
Each application is self-contained.

  ----------------------------------------------- ---------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Menu Item**                                   **Visibility**   **What it does**
  **Project Dashboards**                          Conditional      Create aggregate data dashboards to track project progress (e.g. enrollment rates, survey responses). Dashboards can be made public --- never include PHI in public dashboards. Use as an operational tool, not an analysis tool.
  **Alerts & Notifications**                      Conditional      Configure rule-based email alerts triggered by data entry events, survey completions, date comparisons, or custom logic. Supports piped (merged) REDCap field values in email content.
  **Multi-Language Management (MLM)**             Conditional      Apply multiple language translations to instruments and parts of the REDCap interface. Useful for multilingual survey populations. REDCap identifies text that needs translation but does not translate it --- use a native speaker.
  **Calendar**                                    Conditional      Originally designed for longitudinal projects to track participant follow-up schedules. Not a replacement for hospital scheduling systems or a survey scheduler. Can sync with external calendaring systems.
  **Data Exports, Reports, and Stats**            Conditional      Export project data in multiple formats (Excel, CSV, SPSS, SAS, Stata, R). Create and save custom filtered reports. Includes basic visualizations and connections to tools like Tableau.
  **Data Import Tool**                            Conditional      Import data into the project using a generated template. Validates formatting before import and shows a preview of changes including overwrite conflicts.
  **Data Comparison Tool**                        Conditional      Compare two records side by side. Primarily used with the Double Data Entry feature to identify discrepancies between two independent data entry attempts.
  **Logging**                                     Conditional      Full audit log of all user activity in the project, down to page views. Filterable by user, event type, and date. Exportable --- useful for regulatory compliance.
  **Email Logging**                               Conditional      Audit log of all emails sent from this project. Allows resending emails. Caution: in anonymous survey projects, this log may inadvertently link email addresses to records.
  **Field Comment Log**                           Conditional      Review and edit all comments added to specific fields across all records. Useful for capturing data situations not anticipated during design.
  **Data Resolution Workflow (Resolve Issues)**   Conditional      Replaces the Field Comment Log when enabled. Adds the ability to assign field-level issues to specific users for resolution. Used in teams with formal data validation roles.
  **File Repository**                             Conditional      Access files uploaded to the project repository or auto-generated files (e.g., e-consent PDFs, data export files). Note: files uploaded within a record are accessed from that record, not here.
  **User Rights**                                 Conditional      Manage user permissions for this project. Assign individual rights or create roles (e.g., Data Entry, Statistician, Data Coordinator) and add users to those roles.
  **DAGs (Data Access Groups)**                   Conditional      Designate record-level access groups so users only see records in their assigned group. Common use case: multi-site studies where site A users should not see site B records.
  **Customize & Manage Locking / E-signatures**   Conditional      Configure record and instrument locking for projects requiring independent validation. Locked instruments cannot be edited by regular users.
  **Data Quality**                                Conditional      Run predefined or custom rules across the entire dataset to identify data issues (blank required fields, validation errors, custom logic violations). Used primarily during data cleaning.
  **API**                                         Conditional      Generate or request an API token to allow external programs to interact with the project programmatically. Advanced feature requiring programming skills.
  **API Playground**                              Conditional      Explore and test available API methods with built-in documentation and code examples in multiple languages (PHP, Python, R, Java, etc.).
  **REDCap Mobile App**                           Conditional      Manage device connections for the REDCap Mobile App. Used for offline data collection by study staff in the field. See note below on Mobile App vs. MyCap.
  **Custom Links**                                Conditional      Links added by your local REDCap admin team pointing to institution-specific support resources (ticketing systems, training calendars, LMS portals, etc.). See RC-INST-01 for the specific links available at this installation.
  ----------------------------------------------- ---------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

> **Note:** *REDCap Mobile App vs. MyCap: These are two separate apps
> with different purposes. REDCap Mobile App is for study staff to
> collect data offline across multiple records and then sync. MyCap is
> for individual participants to enter their own data into a single
> record on their personal device.*

**4.5 Custom Reports & Project Dashboards (Dynamic Sections)**

When a user creates custom reports or project dashboards, REDCap
automatically adds new labeled sections to the left menu listing those
reports or dashboards. These sections only appear if at least one report
or dashboard has been created and the user has access to it.

-   **Reports section:** Lists all custom reports the user has access
    to. Reports can be organized into folders (defined by name, then
    reports are added to the folder) --- useful for projects with large
    numbers of reports.

-   **Project Dashboards section:** Lists all dashboards accessible to
    the user.

**4.6 External Modules**

External modules are community-developed add-ons that extend REDCap\'s
functionality. They must be downloaded and enabled by your local REDCap
admin team. This menu section only appears if at least one module is
active in the project and has a dedicated page. For the list of modules
available at this installation and the local policy on enabling them, see
**RC-INST-01 — Institution-Specific Settings & Policies, Section 8**.

-   Click Manage in the External Modules section header to see available
    modules and enable/disable them (depending on your permissions and
    local policy).

-   View Logs is available for module developers and troubleshooting ---
    not typically needed by end users.

> **⚠ Warning:** *External modules are reviewed by Vanderbilt at
> submission time, but that is not an ongoing guarantee of functionality
> or continued support. All modules are built by volunteers. Use at your
> own risk and consult your REDCap admin before enabling unfamiliar
> modules.*

**4.7 Help & Information**

Support and documentation resources. Always visible to all users.

  ---------------------------------- ---------------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Menu Item**                      **Visibility**   **What it does**
  **Help & FAQ**                     Always           Links to the Help & FAQ section on the REDCap home page. Good first stop for common questions.
  **Video Tutorials**                Always           Links to Vanderbilt\'s official REDCap training videos. These are generic and do not reflect institution-specific configurations.
  **Suggest a New Feature**          Always           Submits a feature idea to the Vanderbilt REDCap development team. Not a support channel --- no direct response is given. Suggestions may influence the development roadmap over time.
  **Contact REDCap Administrator**   Always           Connects to your institution\'s support team. Includes project metadata automatically so the support team knows which project you are asking about. This is the correct channel for immediate assistance.
  ---------------------------------- ---------------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**5. Questions & Answers**

  ---------------------------------------------------------------------------------------------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  *Where do I go to export my data?*                                                             Applications → Data Exports, Reports, and Stats. You need sufficient user rights for this item to appear.
  *Where do I manage who has access to my project?*                                              Applications → User Rights. You need User Rights management permissions to see and use this item.
  *I want to send survey invitations by email. Where do I find that?*                            Data Collection → Survey Distribution Tools. This only appears if surveys are enabled in the project setup.
  *Where can I see a log of everything that has happened in my project?*                         Applications → Logging. Shows a full audit trail filterable by user, event, and date.
  *How do I back up my project before making major changes?*                                     Project Home or Project Setup → Other Functionality → Back up the project. This is especially useful when migrating between REDCap installations.
  *Can I roll back a change I made to my instruments?*                                           Yes --- Project Home or Project Setup → Project Revision History. You can download a prior Data Dictionary version or roll back to it. Note: this only restores instruments and fields, not user rights or survey settings.
  *What is the difference between Logging and Email Logging?*                                    Logging tracks all user activity (page views, edits, record creation, etc.). Email Logging specifically tracks emails sent from the project and allows resending them.
  *Where do I find files that were generated by REDCap, like exported data or e-consent PDFs?*   Applications → File Repository. Note: files uploaded within a specific record are accessed from that record directly, not from the File Repository.
  *I need to compare two data entry attempts for the same record. What do I use?*                Applications → Data Comparison Tool. This is designed for use with the Double Data Entry feature.
  *What is the API and do I need it?*                                                            The API allows external programs to interact with REDCap programmatically. Most study coordinators and PIs will never need it. It is an advanced feature for users with programming skills or an IT partner.
  *Where do I go to clean up data quality issues before analysis?*                               Applications → Data Quality. Run predefined or custom rules across your dataset to identify and flag issues.
  *Can I see which emails were sent to my participants?*                                         Yes --- Applications → Email Logging. Use caution in anonymous survey projects, as this log may link email addresses to records.
  *How do I set up automated email alerts based on data entry?*                                  Applications → Alerts & Notifications. Configure triggers based on data entry events, survey completions, or date/logic comparisons.
  ---------------------------------------------------------------------------------------------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**6. Common Mistakes & Gotchas**

**Using \'Suggest a New Feature\' for support requests**

-   **What happens:** User submits a support request through the feature
    suggestion tool and never receives a response. The Vanderbilt team
    does not reply to suggestions individually.

-   **Prevention:** For immediate help, always use Contact REDCap
    Administrator, which reaches your local support team and includes
    helpful project metadata.

**Including PHI in a public Project Dashboard**

-   **What happens:** A dashboard containing participant health
    information is made publicly accessible without login, creating a
    potential HIPAA/data privacy violation.

-   **Prevention:** Before making any dashboard public, audit every
    field and visualization for PHI. When in doubt, keep it private.

**Relying on the Calendar app for survey scheduling**

-   **What happens:** Users expect the Calendar to schedule survey sends
    or appointment reminders, but it does not --- it is a display tool,
    not a scheduler.

-   **Prevention:** Use Automated Survey Invitations (in the Online
    Designer) or Alerts & Notifications to trigger time-based survey
    sends.

**Downloading files from File Repository instead of the record**

-   **What happens:** User looks in the File Repository for a file that
    was uploaded within a specific record and cannot find it there.

-   **Prevention:** Files uploaded in a record field (e.g., a file
    upload field in a form) are stored in the record, not the File
    Repository. Navigate to the record and the relevant instrument to
    access them. The File Repository holds project-level files and
    REDCap-generated outputs.

**Enabling external modules without vetting them**

-   **What happens:** An external module causes unexpected behavior or
    breaks when REDCap is updated, with no support pathway available.

-   **Prevention:** Check with your REDCap admin before enabling any
    module. Understand that modules are community-maintained and support
    is not guaranteed.

**7. Related Topics**

-   **RC-NAV-UI-01:** Project Navigation UI --- the two-panel layout,
    hamburger mode, and project status overview

-   **RC-RIGHTS-01:** User Rights --- how to configure permissions that
    control menu item visibility

-   **RC-DE-02:** Basic Data Entry --- covers Record Status Dashboard
    and Add/Edit Records in depth

-   **RC-SURV-01:** Survey Setup --- covers survey enabling, instrument
    survey settings, and Survey Distribution Tools

-   **RC-ALERT-01:** Alerts & Notifications --- detailed configuration
    guide

-   **RC-EXPORT-01:** Data Exports, Reports, and Stats --- detailed
    guide to exporting and custom reports

-   **RC-API-01:** API --- introduction to the REDCap API for technical
    users

-   **RC-MOB-01:** REDCap Mobile App vs. MyCap --- full comparison of
    the two mobile tools

**8. Version & Change Notes**

  -------------------- ---------------------------------------------------------------------------------------------------------------------------------- --
  **REDCap Version**   **Notes**                                                                                                                          
  **14.x+**            Menu item names and section structure consistent with this document as of this version.                                            
  **13.x**             Data Resolution Workflow, MLM, and MyCap were available but may have had different enable/disable paths. Verify with your admin.   
  **Any version**      External module availability is entirely installation-dependent. Always check with your local admin team.                          
  -------------------- ---------------------------------------------------------------------------------------------------------------------------------- --

REDCap LLM Knowledge Base \| RC-NAV-UI-02 \| Project Menu Reference
