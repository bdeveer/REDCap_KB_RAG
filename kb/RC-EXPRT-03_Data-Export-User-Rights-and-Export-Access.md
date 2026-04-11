RC-EXPRT-03

**Data Export — User Rights & Export Access**

| **Article ID** | RC-EXPRT-03 |
| --- | --- |
| **Domain** | Exports, Reports & Stats |
| **Applies To** | All REDCap project types |
| **Prerequisite** | RC-EXPRT-01 — Data Export: Overview & Workflow |
| **Version** | 1.0 |
| **Last Updated** | 2025 |
| **Author** | REDCap Support |
| **Related Topics** | RC-EXPRT-01 — Overview & Workflow; RC-EXPRT-04 — De-identification & Formatting Options; RC-USER-01 — User Rights (when available) |

# 1. Overview

This article explains how REDCap user rights control what data a user
can export, from which instruments, and in what form. Data Export Rights
are configured per instrument and can restrict a user to de-identified
exports only, or block export entirely. Understanding these rights is
essential for troubleshooting export access issues and for correctly
configuring access for project team members.

# 2. Key Concepts & Definitions

**Data Viewing Rights**

Controls what a user can see within REDCap\'s data entry and reporting
interface. A user may have the right to view data on screen without
being permitted to export it. Data Viewing Rights and Data Export Rights
are configured independently.

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
view and export records within their DAG. Users not assigned to any DAG
can export all records in the project. DAG membership affects exports
even when a user has Full Data Set export rights.

**Identifier Field**

A variable flagged by the project designer as containing potentially
identifying information (e.g., name, date of birth, medical record
number). Identifier flags are set in the Online Designer or via Check
for Identifiers in the Project Setup page. Export rights levels that
include de-identification use this flag to determine which fields to
remove.

# 3. Data Export Rights Levels

Export rights are configured per instrument in User Rights. A user may
have different levels for different instruments. The level assigned
determines what the export dialog shows and what options are available.

  ---------------------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Level**                          **What the user can export**
  **No Access**                      No data from this instrument can be exported in any form. The instrument\'s variables are excluded from all exports, including All Data and custom reports.
  **De-identified**                  Exports the instrument with all free-form text fields, date/time fields, and identifier-flagged fields automatically removed. The de-identification options in the export dialog become required rather than optional. The user cannot choose to export identified data.
  **Remove All Identifier Fields**   Exports all fields except those flagged as identifiers. The user can optionally apply further de-identification in the export dialog (see RC-EXPRT-04). Free-form text and date fields are included unless the user elects to remove them.
  **Full Data Set**                  Exports all fields including identifiers. The user can choose to export in identified or de-identified form. All de-identification options in the export dialog are optional.
  ---------------------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 4. How Rights Affect the Export Dialog

The export dialog adapts based on the user\'s rights. Users with
restricted rights see fewer options, and some options become mandatory
rather than optional.

## 4.1 Full Data Set users

See all export options. De-identification options are presented as
optional checkboxes. The user can export in fully identified or fully
de-identified form.

## 4.2 Remove All Identifier Fields users

The Remove All Identifier Fields de-identification option is pre-checked
and cannot be unchecked. Additional de-identification options remain
optional. The user can further restrict but cannot export identifiers.

## 4.3 De-identified users

All de-identification options (remove identifiers, remove free-form
text, remove dates) are pre-checked and locked. The user sees a
restricted export dialog with no ability to include identified data.

## 4.4 No Access users

Instruments where the user has No Access are excluded from the export
entirely. If all instruments are set to No Access and the user also
lacks the Add/Edit/Organize Reports right, the Data Exports, Reports,
and Stats application may not appear in the menu at all.

  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Tip:** To remove the Data Exports, Reports, and Stats application from a user\'s menu entirely, set their export rights to No Access for all instruments and uncheck the Add/Edit/Organize Reports right.
  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 5. Data Access Groups and Export Scope

DAG membership limits which records a user can export, regardless of
their Data Export Rights level.

- A user assigned to one or more DAGs can only export records that
    belong to those DAGs.

- A user not assigned to any DAG can export all records in the
    project.

- DAG filtering applies to all export types — All Data, Selected
    Instruments, and custom reports.

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Important:** If a user reports that their export is missing records, check whether they are assigned to a DAG. Their export rights may be Full Data Set, but DAG membership still limits which records they can access.
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 6. Common Questions

  ------------------------------------------------------------------------------------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  *Why can\'t I see the Data Exports, Reports, and Stats application in the menu?*      The application only appears if you have at least one instrument with export rights above No Access, or if the Add/Edit/Organize Reports right is enabled. If neither applies, the application is hidden. Contact your project administrator to review your rights.
  *I have Full Data Set rights but my export is missing some records. Why?*             You are likely assigned to a Data Access Group. DAG membership restricts exports to records in your DAG regardless of your export rights level. Contact your project administrator if you need access to records outside your DAG.
  *Can I have different export rights for different instruments?*                       Yes. Data Export Rights are configured per instrument. You may have Full Data Set rights for one instrument and De-identified rights for another within the same project.
  *What is the difference between Data Viewing Rights and Data Export Rights?*          Data Viewing Rights control what you can see in REDCap\'s interface during data entry and reporting. Data Export Rights control whether and how you can download that data. A user can have full viewing rights with no export rights, or vice versa.
  *I need to create a custom report but don\'t see the option. What right do I need?*   The Add/Edit/Organize Reports right must be enabled for your account. This is separate from Data Export Rights. Contact your project administrator to request this right.
  *Does the De-identified export level remove all sensitive data automatically?*        It removes free-form text fields, date/time fields, and fields flagged as identifiers. However, de-identification depends on the project designer having correctly flagged identifier fields. If identifier flagging was incomplete during project design, some sensitive fields may still appear in de-identified exports.
  ------------------------------------------------------------------------------------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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
check both.

**Not removing the application from the menu when export should be fully
blocked.** Setting export rights to No Access for all instruments still
leaves the application visible if the Add/Edit/Organize Reports right is
enabled. To hide the application entirely, both conditions must be
addressed.

# 8. Related Articles

- RC-EXPRT-01 — Data Export: Overview & Workflow (prerequisite)

- RC-EXPRT-04 — Data Export: De-identification & Formatting Options
    (how de-identification options work in the export dialog)

- RC-EXPRT-05 — Data Export: Report Types

- RC-NAV-REC-04 — Record Status Dashboard & Other Record Links (DAG
    filtering behavior)
