

**Data Export — De-identification & Formatting Options**

| **Article ID** | [RC-EXPRT-04 — Data Export: De-identification & Formatting Options](RC-EXPRT-04_Data-Export-De-identification-and-Formatting-Options.md) |
|---|---|
| **Domain** | Exports, Reports & Stats |
| **Applies To** | All REDCap project types; availability varies by Data Export Rights level |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.4.1 (Standard) / v17.3.7 (LTS) — changelog review; page not re-captured. Export de-identification and formatting options behaviour checked against source code of v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) |
| **Prerequisite** | [RC-EXPRT-01 — Data Export: Overview & Workflow](RC-EXPRT-01_Data-Export-Overview-and-Workflow.md); [RC-EXPRT-03 — Data Export: User Rights & Export Access](RC-EXPRT-03_Data-Export-User-Rights-and-Export-Access.md)|
| **Version** | 1.1 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-EXPRT-03 — Data Export: User Rights & Export Access](RC-EXPRT-03_Data-Export-User-Rights-and-Export-Access.md); [RC-EXPRT-02 — Data Export: Export Formats](RC-EXPRT-02_Data-Export-Export-Formats.md)|
| **Synonyms** | how to deidentify exported data; remove identifiers from my export; export data without phi; hide free text and dates on export; shift dates for de-identification; export formatting options explained; mask identifying fields when downloading; remove names and mrn from export |

---

## 1. Overview

This article covers the optional de-identification settings and data
formatting options available in REDCap's export dialog.
De-identification options allow you to remove or transform potentially
identifying information before downloading your data. Formatting options
control how values are represented in the exported file. The
availability of these options depends on the user's Data Export Rights
level — see [RC-EXPRT-03 — Data Export: User Rights & Export Access](RC-EXPRT-03_Data-Export-User-Rights-and-Export-Access.md) for details on rights levels.

---

## 2. Key Concepts & Definitions

**De-identification**

The process of removing or transforming data elements that could be used
to identify an individual participant. REDCap's export
de-identification options target four categories: identifier-flagged
fields, free-form text fields, the Record ID field, and date/datetime
fields. The Record ID field itself is never removed from an export; at
most it is hashed.

**Identifier Field**

A variable that has been flagged by the project designer as containing
potentially identifying information. Examples include name, date of
birth, and medical record number. The identifier flag is set in the
Online Designer or via the Check for Identifiers tool in Project Setup.

**Date Shifting**

A de-identification technique that moves all date and datetime values in a
record **back in time** by a number of days, up to a per-project maximum.
The maximum defaults to 364 days; a REDCap administrator can change it for
an individual project in the Control Center, and the export dialog shows
the project's current maximum in the option label. The shift amount is
worked out from the record name, so it is the same for every date within a
record (across all events) and the same every time that record is
exported, preserving the intervals between dates. Different records get
different shifts. The saved data in the project is never changed.

**Hash (Record ID Hashing)**

A one-way transformation applied to the Record ID field. Hashing
replaces the Record ID with a 32-character scrambled value that cannot be
reversed. Within the same project, a record gets the same hashed value in
every export, so records can be linked across exports without revealing
the original identifier. The hashed value changes if the record is
renamed, and the same record name hashes differently in different
projects, so hashed IDs cannot be used to link records across projects.
Only relevant when the Record ID contains an actual identifier such as a
medical record number.

**CSV Delimiter**

The character used to separate values in a CSV file. The standard
delimiter is a comma, but some regional configurations (common in
Europe) use a semicolon or tab instead. Mismatched delimiters cause CSV
files to display incorrectly in spreadsheet applications.

---

## 3. De-identification Options

De-identification options appear in the export dialog under a dedicated
section. Options available to a user depend on their Data Export Rights
level:

- **Full Data Set on every instrument:** all options are optional.
- **De-identified on every instrument:** Remove All Identifier Fields,
  Remove unvalidated Text fields, Remove Notes/Essay box fields and the
  survey completion timestamp shift are pre-checked and locked. For dates
  you must choose either remove or shift (shift is selected by default).
  Hash the Record ID field is locked on only when the Record ID field is
  itself flagged as an identifier.
- **Remove All Identifier Fields on every instrument:** Remove All
  Identifier Fields is pre-checked and cannot be unchecked.
- **Mixed rights across instruments:** nothing is locked. Instead, the
  dialog shows a notice that some fields may be removed automatically,
  and REDCap removes them instrument by instrument according to your
  right on each one. Any option you tick on top of that is applied to all
  remaining fields in the export.

Whatever the dialog shows, the removal required by your rights is applied
by the server when the file is built, not only by the checkboxes. If the
Record ID field is flagged as an identifier and your rights are limited,
the Record ID is hashed automatically. REDCap administrators are not
subject to these restrictions.

### 3.1 Known Identifier Options

| **Option** | **What it does** |
| --- | --- |
| **Remove All Identifier Fields** | Removes all variables flagged as identifiers from the export, and also leaves out the survey identifier column. Unflagged text, notes and date fields stay in. This is the simplest and most reliable way to de-identify an export, provided the project designer has correctly flagged all sensitive fields. Variables such as email or phone are removed only if they are flagged. |
| **Hash the Record ID Field** | Replaces the Record ID with a hashed (scrambled) value. Use this only if the Record ID itself contains an identifier such as a medical record number, phone number, or social security number. If the Record ID is an auto-assigned integer, hashing is unnecessary. |

### 3.2 Free-Form Text Options

| **Option** | **What it does** |
| --- | --- |
| **Remove unvalidated Text fields** | Removes all text box fields that have no validation rule applied. This includes `@CALCTEXT` fields, which are text boxes without validation. Validated text fields (e.g., those with date, number, or email validation) are still included. Use this when unvalidated text fields may contain participant-entered narrative content. |
| **Remove Notes/Essay box fields** | Removes all Notes box fields from the export. Notes fields can contain large amounts of free-form text that may include identifying information. This option errs on the side of caution by removing all notes fields regardless of content. |

### 3.3 Date and Datetime Options

For date de-identification, only one of the two options can be selected.

| **Option** | **What it does** |
| --- | --- |
| **Remove all date and datetime fields** | Removes all text fields with a date or datetime validation from the export entirely. This is the most aggressive date de-identification option. It does **not** remove survey completion timestamps, and time-only fields are not removed. |
| **Shift all dates by value between 0 and [maximum] days** | Moves all date and datetime values in the export back in time, by up to the project's maximum (364 days unless an administrator has changed it). The same shift is applied to all dates within a single record, preserving relative date relationships, and the record gets the same shift in every export. Different records receive different shifts. Use when date values have research utility but exact dates are a privacy concern. |
| **Also shift all survey completion timestamps by value between 0 and [maximum] days** | Applies the same per-record shift to the survey completion timestamp columns. Locked on for users with De-identified rights on every instrument. |

Fields of other types are never removed by the date or free-text options:
calculated fields, multiple-choice fields, sliders, time fields, validated
text and File Upload fields stay in the export unless they are flagged as
identifiers.


> **Important:** Date shifting preserves relative time relationships within a record (e.g., days between enrollment and first visit) but makes absolute dates less identifiable. It does not prevent re-identification if the shifted dates are combined with other identifying information. Survey completion timestamps are real dates too: if you remove or shift dates, check that the survey timestamp columns are either excluded or shifted as well.


---

## 4. Advanced Data Formatting Options

These options control how the exported data is structured and formatted.
They appear below the de-identification section in the export dialog.
The defaults are appropriate for most exports. REDCap remembers your
choices here for your next export.

| **Option** | **What it does** |
| --- | --- |
| **Export blank values for gray Form Status?** | Controls whether an instrument with no data saved (gray dot / status 0) exports as '0' or as a blank value. The default exports '0'. Change this only if you are using the export as a re-import file and need blank to mean 'no data' rather than 'incomplete'. |
| **Set CSV delimiter character** | Changes the character used to separate values in CSV exports (CSV Raw Data and CSV Labels only). Choices are comma (default), tab, semicolon, pipe and caret (^). If your analysis software or regional settings expect a semicolon or tab delimiter, set this accordingly. Mismatched delimiters cause CSV files to open as a single column in spreadsheet applications. |
| **Force all numbers into a specified decimal format?** | Standardizes the decimal separator used in calculated fields and number-validated text fields. The default is to use each field's native decimal format. Use this when your analysis software or regional settings expect a period (.) or comma (,) as the decimal character. Mismatched decimal formats cause numeric fields to be read as text in some applications. |

### 4.1 Additional Options (Feature-Dependent)

When certain project features are enabled, additional options appear in
the export dialog automatically. For example, if one or more Data Access
Groups are configured in the project and you are not assigned to a DAG,
an option appears (checked by default) to export an additional variable
containing each record's DAG assignment. These
options are contextual and only appear when relevant.

---

## 5. Common Questions

| *My de-identification options are grayed out and pre-checked. Why can't I change them?* | Your Data Export Rights level is De-identified or Remove All Identifier Fields on every instrument. At these levels, certain de-identification options are mandatory and cannot be unchecked. If your rights differ between instruments, nothing is locked; you see a notice instead, and REDCap removes the restricted fields instrument by instrument when it builds the file. Contact your project administrator if you need a higher access level. |
| --- | --- |
| *Should I use date shifting or remove all dates?* | Use date shifting when date values have research utility and you want to preserve relative time relationships between events. Use remove all dates when the analysis does not require date values at all and you want the simplest approach to de-identification. Either way, deal with survey completion timestamps separately: removing dates does not remove them. |
| *Which way are dates shifted, and by how much?* | Back in time, by up to the project's maximum (364 days by default; an administrator can change it per project). The shift is fixed per record, so repeated exports give the same shifted dates. |
| *When should I use the Hash Record ID option?* | Only when the Record ID field contains an actual identifier, such as a medical record number, phone number, or social security number. If the Record ID is an auto-assigned integer (the REDCap default), there is no reason to hash it. |
| *My exported CSV opens as a single column in Excel. What is wrong?* | The CSV delimiter does not match what Excel expects for your regional settings. Open the export dialog and change the delimiter to match your system — typically a semicolon for European regional settings. Alternatively, use Excel's Text Import Wizard to specify the delimiter manually. |
| *Does removing unvalidated text fields also remove validated text fields?* | No. The Remove unvalidated Text fields option only removes text boxes that have no validation rule applied. Text boxes with date, number, email, or other validation are still included in the export. |
| *What does the gray Form Status export option actually affect?* | It only affects instruments with no data saved (gray dot). Changing this from '0' to blank is only relevant if you are using the export as a data import file and your import logic distinguishes between 'incomplete' (0) and 'no data entered' (blank). For most analysis purposes, the default is fine. |

---

## 6. Common Mistakes & Gotchas

**Hashing the Record ID when it is an auto-assigned integer.** Record ID
hashing is only meaningful when the Record ID contains a real
identifier. Hashing an auto-assigned integer (1, 2, 3\...) provides no
privacy benefit and may complicate downstream data linkage.

**Assuming de-identification is complete when identifier flagging is
incomplete.** De-identification options act on fields flagged as
identifiers. If the project designer did not flag all sensitive
variables during project design, those variables will still appear in
de-identified exports. Variables such as email addresses and phone
numbers are removed only if they are flagged. Verify the project's identifier flags before
relying on export de-identification as a privacy safeguard.

**Assuming "Remove all date and datetime fields" removes every date.**
It removes date- and datetime-validated text fields only. Survey
completion timestamps stay in the export unless you leave them out or
shift them, and dates typed into unvalidated text or notes fields stay
unless you also remove those fields.

**Selecting both date de-identification options.** REDCap only allows
one date de-identification option — remove all dates or shift all
dates. Selecting both is not possible; choosing one disables the other.

**Ignoring the delimiter setting when exporting for international
collaborators.** Regional CSV delimiter differences are a common source
of data formatting problems. When sharing exports internationally,
confirm the expected delimiter with the recipient before exporting.

---

## 7. Related Articles

- [RC-EXPRT-01 — Data Export: Overview & Workflow](RC-EXPRT-01_Data-Export-Overview-and-Workflow.md) (the full export
    process)

- [RC-EXPRT-03 — Data Export: User Rights & Export Access](RC-EXPRT-03_Data-Export-User-Rights-and-Export-Access.md) (how rights
    levels affect which de-identification options are mandatory)

- [RC-EXPRT-02 — Data Export: Export Formats](RC-EXPRT-02_Data-Export-Export-Formats.md) (format selection
    affects how values are represented)

- [RC-FD-01 — Form Design Overview](RC-FD-01_Form-Design-Overview.md) (Check for Identifiers — where
    identifier flags are set)
