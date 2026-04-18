# RC-CC-04 — Control Center: User Settings & Defaults

> **Administrator access required.** This page is only available to REDCap super users via the Control Center.

The **User Settings** page (under **System Configuration**) controls what regular users can and cannot do within REDCap, and what default behaviors new accounts start with. These settings do not require any individual project configuration — they apply system-wide.

---

## Project Creation & Status Changes

**Allow Normal Users to Create New Projects**
Controls whether any authenticated user can create a new project in REDCap. Options:
- *Yes, normal users can create new projects* — Users see a "New Project" button on their My Projects page
- *No, only Administrators can create new projects* — Users instead see a "Request New Project" option that sends a request to an administrator

**Allow Normal Users to Move Projects to Production**
Controls whether project owners can move their own projects to Production status without administrator approval. Options:
- *Yes, normal users can move projects to production*
- *No, only Administrators can move projects to production* — Users instead see a "Request To Move to Production" option that sends a request to an administrator

**Default Instrument-Level User Access (New Instruments in Production)**
Sets the default data access rights applied to all existing project users whenever a new instrument is added to a project that is already in Production status. Options:
- *No Access* — Most restrictive; users must be explicitly granted rights to new instruments
- *View & Edit / De-Identified* — Users can access the new instrument but export rights are de-identified
- *View & Edit / Full Data Set* — Users have full view, edit, and export rights to the new instrument

This setting applies to all projects. Note that the selected access level is applied automatically when draft mode changes are approved.

**Custom Surveys for Project Status Transitions (Optional)**
Presents a public REDCap survey to users when they perform certain project lifecycle actions. Used to collect project metadata (e.g., IRB numbers, PI details, data governance agreements) at key milestones. Each transition can have its own survey project (identified by PID):
- *Create/Copy Project survey* — Triggered when a user creates or copies a project
- *Move to Production status survey* — Triggered when a user moves a project to Production
- *Move to Analysis/Cleanup status survey* — Triggered at the Analysis/Cleanup transition
- *Mark project as Completed survey* — Triggered when a project is marked Complete

Surveys must be one-page public surveys and cannot use Survey Queue, Auto-Continue, or Redirect features. Administrators are exempt from completing these surveys. If a field named `project_id` exists in the survey project, REDCap will automatically populate it with the PID of the project being transitioned, allowing cross-referencing of survey responses to projects.

> See RC-PROJ-01 for context on project lifecycle statuses.

---

## Email Notification Settings

**Notify Admin When a New Account Is Created**
When enabled, the system sends an email to the REDCap administrator whenever a new user account is created via external authentication. Table-based users are excluded because an administrator creates those accounts manually.

**Send a Welcome Email to New Users**
When enabled, REDCap sends a stock welcome email the first time a user logs in via an external authentication method. The email includes:
- A confirmation of the user's username
- A link to the REDCap instance
- Guidance on getting started, training resources, and support contacts

The body of this email contains stock text that can reference your instance URL and links to training/support pages. This setting does not apply to Table-based (local) authentication users.

---

## General User Settings

**Allow Normal Users to Auto-Generate API Tokens**
Controls whether users can generate API tokens for their projects without administrator involvement. Options:
- *No, an administrator must approve each token request* — Most restrictive; admin has full visibility into API usage
- *Yes, allow SELECTED users to generate API tokens on their own* — Individual users can be granted this privilege on the Browse Users page
- *Yes, allow ALL users to generate API tokens on their own* — Any user can self-generate tokens for their projects

**Auto-Suspend Users After Period of Inactivity**
Automatically suspends accounts that have not logged in or used the API for a configurable number of days. Options:
- *Disabled*
- *Enable auto-suspension for all users* — Specify an inactivity period in days (e.g., 180 days) and whether to send a notification email upon suspension

When a user is suspended, if they have a sponsor (secondary contact) listed on their account, the sponsor is CC'd on the notification email. Users who have been manually un-suspended by an administrator within the inactivity window will not be auto-suspended again.

> Note: If using LDAP & Table-based authentication, an additional option appears to enable auto-suspension only for Table-based users.

**Sponsor Dashboard**
An optional module allowing a designated "User Sponsor" to manage accounts they sponsor (e.g., request account suspension, set/extend expiration dates, reset passwords) via a dashboard on their My Projects page. The dashboard reduces administrator burden for managing external or guest user accounts.

Configuration includes a default number of days to add when extending user expiration times (calculated from the existing expiration date or from today if setting a new expiration).

**User Access Dashboard (UAD)**
Provides project-level users a view of all users with access to their projects, prompting periodic review of who should retain access. Enabling options range from a passive notification to active email reminders:
- *Disabled* — UAD is hidden and inaccessible to users
- *Enabled: Notification on page* — Displays a text reminder on the My Projects page
- *Enabled: Notification and warning on page* — Adds a red warning if the user has not visited the UAD in the current calendar month
- *Enabled: Notification and warning on page + Monthly email reminder* — Adds a monthly email on the first weekday of each month

Custom notification text can be configured; otherwise stock text is used. Users without User Rights privileges in any project do not see UAD prompts.

**Allow Users to Edit Survey Responses**
When enabled, project administrators can grant individual users the privilege (via the User Rights page) to edit previously submitted survey responses, whether partially or fully completed.

**Allow Production Draft Mode Changes to Be Approved Automatically**
Controls whether certain Draft Mode submissions bypass the administrator approval queue. Options (from most to least strict):
1. *Never* — Admin approval always required
2. *Yes, if no existing fields were modified* — Auto-approves only if changes are additions or reordering (no modifications to existing fields)
3. *Yes, if project has no records OR if has records and no existing fields were modified* — Auto-approves for empty projects or field-addition-only changes
4. *Yes, if no critical issues exist* — Auto-approves unless critical changes are present (e.g., deleted fields, modified choice options, changed field types)
5. *Yes, if project has no records OR if has records and no critical issues exist* — Most permissive; auto-approves unless the project both has records AND has critical changes

An optional additional condition can restrict auto-approval if any new fields have labels or variable names matching keywords from the 'Check For Identifiers' page.

> Note: Even with auto-approval enabled, an administrator is still required to review changes if critical issues exist AND the project contains one or more records.

**Allow Normal Users to Modify Repeating Instruments & Events in Production**
Controls whether project-level administrators can change repeating instrument/event configurations on a production project without super-user involvement. Options:
- *No, only Administrators can modify the repeating instance setup in production*
- *Yes, normal users can modify the repeating instance setup in production*

**Allow Normal Users to Add or Modify Events and Arms in Production**
Controls whether project-level administrators can add or modify events and arms on a longitudinal project's Define My Events page while the project is in Production status. Options:
- *No, only Administrators can add/modify events in production*
- *Yes, normal users can add/modify events in production*

> Note: Even when set to Yes, only administrators can *delete* events in production. Normal users can designate instruments to events that have not yet been designated, but cannot un-designate instruments that are already designated.

**Domain Allowlist for User Email Addresses**
Restricts the email domains that can be used for REDCap accounts. Enter one domain per line (e.g., `university.edu`). When set, only email addresses from listed domains can be associated with a REDCap account. Useful for limiting access to institutional users.

**Allow Normal Users to Edit Their Name and Primary Email**
Two independent controls governing whether users can update their own first/last name and primary email address from their Profile page:
- *Do not allow editing*
- *Allow editing*

Administrators retain the ability to edit these fields regardless of the setting. These restrictions may be appropriate in 21 CFR Part 11 regulated environments.

**Display Variable Auto-Naming Feature**
Controls visibility of the "suggest variable name" feature in the Add Field popup in the Online Designer. Options:
- *No, hide it for all users*
- *Yes, display it for all users*
- *Only display it for administrators*

---

## Default Settings for New Users

These settings define the starting state of new user accounts. They primarily affect users created via external authentication methods (LDAP, Shibboleth, etc.). Table-based user accounts have these values set manually by an administrator at account creation.

**Allow new users to create projects by default**
- *No* — New users cannot create projects until an administrator grants that right
- *Yes* — New accounts immediately have project creation rights

**Date and time format**
Sets the display format for dates and times across REDCap. Options include combinations of:
- Format: MM-DD-YYYY, MM/DD/YYYY, MM.DD.YYYY, DD-MM-YYYY, DD/MM/YYYY, DD.MM.YYYY, YYYY-MM-DD, YYYY/MM/DD, YYYY.MM.DD
- Clock: 24-hour or 12-hour AM/PM

**Number format — decimal character**
- `. (period / full stop)` (e.g., 3.14)
- `, (comma)` (e.g., 3,14)

**Number format — thousands separator**
- `, (comma)` (e.g., 1,000,000)
- `. (period / full stop)` (e.g., 1.000.000)
- `' (apostrophe)`
- `(blank space)`
- `[no thousands separator]`

**Delimiter for CSV file downloads**
Applies to all CSV exports. Options include comma, semicolon, tab, space, pipe (`|`), and caret (`^`). For locales that use a comma as a decimal separator, semicolon or tab is recommended to avoid parse errors.

---

## Public Reports, Project Dashboards & Smart Charts

**Allow Reports to Be Made Public**
When enabled, project users with User Rights privileges can generate publicly accessible URLs for reports. Public report URLs do not require REDCap authentication. Options:
- *No, do not allow reports to be made public*
- *Yes, allow users to make reports public on their own*
- *Yes, but an administrator must approve the request*

Before making a report public, the user (or admin) must confirm they have viewed the report, acknowledge that all data in the report will be publicly accessible, and accept responsibility for any sensitive data exposure.

> Note: Administrators always retain the ability to make a report public, regardless of this setting.

**Allow Project Dashboards to Be Made Public**
Controls whether project-level administrators can generate public URLs for project dashboards (including Smart Charts and Smart Tables). Options mirror those for public reports. If set to require admin approval, the admin receives the request via the To-Do List page.

**Minimum Number of Data Points Required for Public Smart Charts/Tables/Functions**
Sets a system-level floor on the number of data points required before a Smart Chart, Smart Table, or Smart Function will display on a public project dashboard, public report, or survey page. If a chart or function has fewer data points than the minimum, it will show the message `[INSUFFICIENT AMOUNT OF DATA FOR DISPLAY]` instead.

This setting does not apply when viewing charts/reports from inside a REDCap project — only via their public links. It can be overridden per project on the 'Edit Project Settings' page.

---

## Account Expiration Email Templates (Optional)

Custom email text can be configured for the two automated account expiration reminder emails REDCap sends: 14 days before expiration and 2 days before expiration. Separate templates can be defined for users without a sponsor and users with a sponsor. Dynamic variables can be included to personalize the email with the user's information. If no custom text is provided, REDCap uses stock email text.

---

## Related Articles

- RC-CC-01 — Control Center: Overview & Navigation
- RC-CC-02 — General System Configuration
- RC-CC-07 — Users & Access Management
- RC-PROJ-01 — Project Lifecycle: Status and Settings
- RC-USER-01 — User Rights: Overview & Three-Tier Access
