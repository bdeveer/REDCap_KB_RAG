---
id: RC-EXPRT-03
title: Data Export — User Rights & Export Access
domain: Exports, Reports & Stats
applies_to:
- All REDCap project types
requires: Any supported version
verified_against: REDCap v17.4.1 (Standard) / v17.3.7 (LTS) — changelog review; page
  not re-captured. Export rights behaviour checked against source code of v17.6.5
  (Standard) / v17.3.31 and v16.0.61 (LTS)
prerequisites:
- 'RC-EXPRT-01 — Data Export: Overview & Workflow'
version: '1.2'
last_updated: 2026-11
related:
- id: RC-EXPRT-01
  title: 'Data Export: Overview & Workflow'
- id: RC-EXPRT-04
  title: 'Data Export: De-identification & Formatting Options'
- id: RC-USER-01
  title: 'User Rights: Overview & Three-Tier Access (when available)'
tags:
- exports, reports & stats
- data
synonyms:
- why cant i export data in redcap
- data export rights not working
- give a user permission to export
- restrict export to de-identified only
- export access denied troubleshooting
- difference between data viewing and export rights
- set export privileges per instrument
- user cannot download data
- de-identified export user can see identifiers in report
---

# 1. Overview

This article explains how REDCap user rights control what data a user
can export, from which instruments, and in what form. Data Export Rights
are configured per instrument and can restrict a user to de-identified
exports only, or block export entirely. Understanding these rights is
essential for troubleshooting export access issues and for correctly
configuring access for project team members.

---

# 2. Key Concepts & Definitions

**Data Viewing Rights**

Controls what a user can see within REDCap's data entry and reporting
interface. A user may have the right to view data on screen without
being permitted to export it. Data Viewing Rights and Data Export Rights
are configured independently. Data Viewing Rights, not Data Export
Rights, decide what a user sees when they open a report or Stats &
Charts in the browser.

**Data Export Rights**

Controls whether and how a user can export data from REDCap. Set per
instrument. There are four levels: No Access, De-identified, Remove All
Identifier Fields, and Full Data Set. A user may have different export
rights for different instruments within the same project.

**Add/Edit/Organize Reports**

A separate user right that controls whether a user can create, edit, or
organize custom reports. This right is independent of Data Export
Rights. A user can have full export rights without being able to create
custom reports, and vice versa.

**Data Access Group (DAG)**

A record-level partitioning feature. Users assigned to a DAG can only
view and export records within their current DAG. Users not assigned to
any DAG can export all records in the project. DAG membership affects exports
even when a user has Full Data Set export rights.

**Identifier Field**

A variable flagged by the project designer as containing potentially
identifying information (e.g., name, date of birth, medical record
number). Identifier flags are set in the Online Designer or via Check
for Identifiers in the Project Setup page. Export rights levels that
include de-identification use this flag to determine which fields to
remove.

---

# 3. Data Export Rights Levels

Export rights are configured per instrument in User Rights. A user may
have different levels for different instruments. The level assigned
determines what the export dialog shows and what options are available.

| **Level** | **What the user can export** |
| --- | --- |
| **No Access** | No data from this instrument can be exported in any form. The instrument's variables are excluded from all exports, including All Data and custom reports. |
| **De-identified** | Removes identifier-flagged fields, unvalidated text fields (including @CALCTEXT fields, which are text fields without validation) and notes (paragraph text) fields. Date and datetime fields are either removed or date-shifted: in the Data Exports dialog the user must pick one (shifting is the default), while API exports and PDFs always remove them. Kept unless flagged as identifiers: calculated fields, multiple-choice fields, sliders, validated text fields (e.g., number, email or phone validation), time-only fields and file upload fields. The user cannot choose to export identified data. |
| **Remove All Identifier Fields** | Removes only fields flagged as identifiers. Text, notes and date fields are included unless the user elects to remove them in the export dialog (see [RC-EXPRT-04 — Data Export: De-identification & Formatting Options](RC-EXPRT-04_Data-Export-De-identification-and-Formatting-Options.md)). |
| **Full Data Set** | Exports all fields including identifiers. The user can choose to export in identified or de-identified form. All de-identification options in the export dialog are optional. |

**Record ID and files.** The record ID variable is never removed. If the
record ID is itself flagged as an identifier and the user has De-identified
or Remove All Identifier Fields rights on the first instrument (the one
that holds the record ID), REDCap replaces it with a hashed value, both in
the Data Exports dialog and in the API. When file upload fields are
exported as a ZIP, only fields from instruments where the user has more
than No Access are included, and identifier-flagged file fields are left
out for De-identified and Remove All Identifier Fields users.

**Where export rights apply.** Data Export Rights govern data leaving
REDCap through the Data Exports page, the API, the Mobile App and PDFs of
instruments containing record data. They do not govern what a user sees
on screen (see section 4b).

> **Note:** REDCap administrators are not restricted by Data Export
> Rights. Test a user's export access by checking their rights, not by
> exporting as an administrator.

> **Important — Mobile App right.** A user with the Mobile App right
> who is allowed to download all data to the app gets all data on every
> instrument through the app, whatever their Data Export Rights. Their
> DAG still applies. Grant the Mobile App right only to users who may
> hold the full data set — see
> [RC-MOB-01 — REDCap Mobile App](RC-MOB-01_REDCap-Mobile-App.md).

---

# 4. How Rights Affect the Export Dialog

The export dialog adapts based on the user's rights. Options are only
pre-checked and locked when the user has the **same** restricted level
on every instrument. A user with mixed rights (for example Full Data Set
on one instrument and De-identified on another) sees unlocked options
and a notice that some fields may be removed automatically based on
their instrument-level Data Export Rights. REDCap still removes those
fields instrument by instrument when it builds the file, and any option
the user ticks is applied to all remaining fields.

## 4.1 Full Data Set users

See all export options. De-identification options are presented as
optional checkboxes. The user can export in fully identified or fully
de-identified form.

## 4.2 Remove All Identifier Fields users

When every instrument is at this level, the Remove All Identifier Fields
option is pre-checked and cannot be unchecked. Additional
de-identification options remain optional. The user can further restrict
but cannot export identifiers.

## 4.3 De-identified users

When every instrument is at this level, these options are pre-checked
and locked: Remove All Identifier Fields, removal of unvalidated text
fields, and removal of notes fields. For dates the user must choose
either to remove them or to shift them; shifting is selected by default.
The option to hash the record ID is locked on only if the record ID is
flagged as an identifier. The user has no way to include identified
data.

## 4.4 No Access users

Instruments where the user has No Access are excluded from the export
entirely. The Data Exports, Reports, and Stats application still appears
in the menu if the user has export rights above No Access on any
instrument, the Add/Edit/Organize Reports right, or the Stats & Charts
right. Reports shared with the user are also listed in the left-hand
Reports panel whatever their export rights.


> **Tip:** To remove the Data Exports, Reports, and Stats application from a user's menu, set their export rights to No Access for all instruments and uncheck both the Add/Edit/Organize Reports and the Stats & Charts rights. Reports shared with them can still be opened from the left-hand menu; to stop them seeing data, restrict their Data Viewing Rights (see section 4b).

---

# 4b. Viewing Reports in the Browser

Data Export Rights only control downloads. When a user opens a report or
Stats & Charts on screen, REDCap filters what they see by their **Data
Viewing Rights** and their DAG, not by their export rights. A user with
De-identified export rights and View & Edit or Read Only viewing rights
on an instrument sees that instrument's identifier fields, free text and
dates on screen, even though they could not export them.

> **Important:** De-identified export rights are not a privacy control
> for on-screen access. If a user must not see identifiers at all, set
> their Data Viewing Rights to No Access for the instruments holding
> those fields, or move the identifiers to an instrument they cannot
> view.


---

# 4a. Printing a Form Without Full Data Set Rights

Printing a data entry form through the browser is a way of taking data out of REDCap that bypasses the export dialog entirely. REDCap addressed this in two steps, and the outcome differs by version.

| Version | Behaviour |
| --- | --- |
| Below 17.0.2 | No restriction. Any user who can view a form can print it |
| **17.0.2** | Users **without** Full Data Set export privileges for that instrument see an error on the print version of the page instead of the form |
| **17.0.4 and higher** | The 17.0.2 change was **reverted** and replaced by a system-level setting on the **User Settings** page in the Control Center, applying to all users in all projects |

The setting is labelled **Prevent users from printing data entry forms
via their browser if they lack Full Data Set export privileges for the
form?** When it is set to Yes, the check is made per instrument: a user
can print an instrument only if they have Full Data Set export rights on
that instrument. Otherwise they see an error saying they are not allowed
to print/export the form.

> **Version caveat (16.0 LTS):** The setting does not exist in 16.0 LTS (checked in 16.0.61). Any user who can view a form can print it. Treat browser printing as uncontrolled on 16.0 LTS and restrict Data Viewing Rights where printing must be prevented.

> **Important — verify the setting after upgrading.** Instances that upgraded to 17.0.4 or later have the setting switched **off** (printing allowed); new installations start with it switched on. Check the setting on the Control Center User Settings page rather than assuming, and set it to Yes if your instance wants the deterrent — see [RC-CC-04 — Control Center: User Settings & Defaults](RC-CC-04_Control-Center-User-Settings.md).

> **Critical — this is a deterrent, not a control.** REDCap states the restriction plainly: it "is not meant to be a completely impenetrable feature since all client-side solutions for this can be subverted and thus are inherently bypassable." It is designed to stop users *accidentally* exporting data by printing to PDF. It does not stop a determined user, and it must not be relied on as a safeguard for data a user should not be able to see at all. If a user must not have the data, restrict Data Viewing Rights — see [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md).

---

# 5. Data Access Groups and Export Scope

DAG membership limits which records a user can export, regardless of
their Data Export Rights level.

- A user assigned to a DAG can only export records in their current
    DAG. A user who has access to several DAGs through the DAG switcher
    exports only the DAG that is active at the time; to export another
    DAG's records they switch to it first.

- A user not assigned to any DAG can export all records in the
    project.

- DAG filtering applies to all export types — All Data, Selected
    Instruments, and custom reports — and to reports viewed on screen.


> **Important:** If a user reports that their export is missing records, check whether they are assigned to a DAG, and for DAG switcher users, which DAG is active. Their export rights may be Full Data Set, but DAG membership still limits which records they can access.


---

# 6. Common Questions

| *Why can't I see the Data Exports, Reports, and Stats application in the menu?* | The application only appears if you have at least one instrument with export rights above No Access, the Add/Edit/Organize Reports right, or the Stats & Charts right. If none applies, the application is hidden. Contact your project administrator to review your rights. |
| --- | --- |
| *I have Full Data Set rights but my export is missing some records. Why?* | You are likely assigned to a Data Access Group. DAG membership restricts exports to records in your current DAG regardless of your export rights level. If you use the DAG switcher, switch to the other DAG and export again. Contact your project administrator if you need access to records outside your DAG. |
| *Can I have different export rights for different instruments?* | Yes. Data Export Rights are configured per instrument. You may have Full Data Set rights for one instrument and De-identified rights for another within the same project. |
| *What is the difference between Data Viewing Rights and Data Export Rights?* | Data Viewing Rights control what you can see in REDCap's interface during data entry and reporting. Data Export Rights control whether and how you can download that data. A user can have full viewing rights with no export rights, or vice versa. Reports opened in the browser follow viewing rights, so a user with De-identified export rights can still see identifiers on screen. |
| *I need to create a custom report but don't see the option. What right do I need?* | The Add/Edit/Organize Reports right must be enabled for your account. This is separate from Data Export Rights. Contact your project administrator to request this right. |
| *Does the De-identified export level remove all sensitive data automatically?* | It removes fields flagged as identifiers, unvalidated text fields (including @CALCTEXT) and notes fields. Dates and datetimes are removed or date-shifted (in the export dialog the user chooses, with shifting as the default; API exports and PDFs always remove them). Validated text fields (e.g., number, email or phone format), time-only fields, calculated and multiple-choice fields and file uploads are retained unless flagged as identifiers. The export rights also do not limit what the user sees on screen. However, de-identification depends on the project designer having correctly flagged identifier fields. If identifier flagging was incomplete during project design, some sensitive fields may still appear in de-identified exports. |

---

# 7. Common Mistakes & Gotchas

**Assuming Full Data Set rights means all records are accessible.**
Export rights control what data can be exported from accessible records.
DAG membership is a separate layer that controls which records are
accessible. Both must be considered when troubleshooting incomplete
exports.

**Relying on de-identification without verifying identifier flags.** The
De-identified and Remove All Identifier Fields export levels remove
fields flagged as identifiers. If the project designer did not flag all
sensitive fields during design, those fields will still appear in
de-identified exports. Always verify identifier flagging in the project
before granting de-identified export access as a privacy safeguard.

**Confusing Data Viewing Rights and Data Export Rights.** A user who can
see data on screen is not automatically allowed to export it. These are
independently configured rights. When troubleshooting export issues,
check both. The reverse also holds: a user with De-identified export
rights but viewing access to an instrument sees its identifiers on
screen in data entry forms and reports.

**Not removing the application from the menu when export should be fully
blocked.** Setting export rights to No Access for all instruments still
leaves the application visible if the Add/Edit/Organize Reports right or
the Stats & Charts right is enabled. To hide the application, all three
must be addressed. Reports shared with the user remain reachable from the
left-hand menu.

**Assuming the export dialog locks options for mixed rights.** The
de-identification options are only locked when the user has the same
restricted level on every instrument. With mixed rights the checkboxes
look optional, but REDCap still removes fields per instrument. Check the
exported file, not the dialog, when confirming what a user receives.

---

# 8. Related Articles

- [RC-EXPRT-01 — Data Export: Overview & Workflow](RC-EXPRT-01_Data-Export-Overview-and-Workflow.md) (prerequisite)

- [RC-EXPRT-04 — Data Export: De-identification & Formatting Options](RC-EXPRT-04_Data-Export-De-identification-and-Formatting-Options.md)
    (how de-identification options work in the export dialog)

- [RC-EXPRT-05 — Data Export: Report Types & Other Export Options](RC-EXPRT-05_Data-Export-Report-Types-and-Other-Export-Options.md)

- [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) (DAG
    assignment and the DAG switcher)

- [RC-NAV-REC-04 — Record Status Dashboard & Other Record Links](RC-NAV-REC-04_Record-Status-Dashboard-and-Links.md) (DAG
    filtering behavior)
