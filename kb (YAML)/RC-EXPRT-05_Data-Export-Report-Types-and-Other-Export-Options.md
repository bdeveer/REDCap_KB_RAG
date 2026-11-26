---
id: RC-EXPRT-05
title: Data Export — Report Types & Other Export Options
domain: Exports, Reports & Stats
applies_to:
- All REDCap project types
- requires Data Export user rights
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — report
  types and other export options checked against source code; pages not re-captured
prerequisites:
- 'RC-EXPRT-01 — Data Export: Overview & Workflow'
version: '1.2'
last_updated: 2026-11
related:
- id: RC-EXPRT-01
  title: 'Data Export: Overview & Workflow'
- id: RC-EXPRT-03
  title: 'Data Export: User Rights & Export Access'
- id: RC-EXPRT-04
  title: 'Data Export: De-identification & Formatting Options'
tags:
- exports, reports & stats
- data
synonyms:
- what report types can i export
- export all data vs selected instruments
- other export options tab
- export survey return codes for save and return later
- export only certain forms or events
- built-in report options in redcap
- which records and fields get exported
- difference between report and export format
---

# 1. Overview

This article describes the types of reports available in REDCap's Data
Exports, Reports, and Stats application — what each one exports and
when to use it — as well as the additional bulk export options
available under the Other Export Options tab. Report type determines
which records and variables are included in an export. Export format and
de-identification options are applied after the report is selected.

---

# 2. Key Concepts & Definitions

**Report**

A defined selection of records and variables to export. REDCap provides
two built-in reports (All Data and Selected Instruments/Events) that are
always present. Any number of custom reports can be created by users
with the Add/Edit/Organize Reports right and are listed below the
built-in reports.

**All Data Report**

The built-in report that exports every record and every variable in the
project at the time of export. It is always the first report listed and
requires no configuration.

**Selected Instruments/Events Report**

The built-in report that allows the user to choose a subset of
instruments to export. In longitudinal projects, events can also be
selected; if no event is chosen, all events are included. This report
does not filter by record — it exports all records for the chosen
instruments and events.

**Custom Report**

A user-defined report that can filter by individual variables, apply
logic conditions, restrict visibility to specific users, roles or data
access groups, and organize results in a custom order. Custom reports
require the Add/Edit/Organize Reports user right to create or edit. Once
created, they appear in the report list and in the left-hand menu for
quick access.

**Other Export Options**

A separate tab at the top of the Data Exports, Reports, and Stats page
that provides bulk export options not available through the standard
report workflow — including full project XML backup, bulk file
download, PDF of all records, survey return codes, and Tableau
integration. The tab is shown only to users with data export rights.

---

# 3. Built-in Report Types

## 3.1 All Data

Exports the complete dataset — every record, every instrument, every
variable — at the current point in time. This is the quickest path to
a full project export and requires no configuration beyond selecting an
export format.

- Use when you need a complete snapshot of all project data.

- User's Data Export Rights still apply — instruments where the
    user has No Access are excluded.

- DAG membership still limits which records are included.

## 3.2 Selected Instruments and/or Events

Allows the user to select one or more instruments to include in the
export. All records are included for the selected instruments — this
report does not filter by record.

- Use when you need data from specific instruments without exporting
    the entire project.

- In longitudinal projects, you can also limit the export to one or
    more events. The event list defaults to **-- All events --**, so
    selecting events is optional; when you do select them, the export
    includes only the chosen instrument-event combinations.

- Useful for sharing data from a single instrument with an external
    collaborator without exposing the full dataset.

- Choose **Make custom selections** to pick the instruments and events.
    **Create report based on selections** turns the current choice into
    a new custom report (requires the Add/Edit/Organize Reports right).

---

# 4. Custom Reports

## 4.1 What Custom Reports Can Do

Custom reports extend beyond the built-in options by allowing
fine-grained control over what is included in an export.

| **Capability** | **Description** |
| --- | --- |
| **Variable selection** | Choose individual variables to include rather than entire instruments. |
| **Record filtering by logic** | Apply a REDCap logic expression to include only records that meet specific criteria (e.g., only consented participants, only records with a specific diagnosis). |
| **User visibility control** | Restrict the report so it only appears for specific users, user roles or data access groups. Who can view a report and who can edit it are set separately. |
| **Left-menu shortcut** | Custom reports automatically appear in the left-hand menu for quick access, in addition to the report list. |
| **Folder organization** | Reports can be organized into named folders in the left-hand menu, created with the **Organize** link in the Reports panel. A report can be placed in more than one folder. Use folders when a project has accumulated many reports to keep navigation manageable. See [RC-EXPRT-08 — Custom Reports: Management & Organization](RC-EXPRT-08_Custom-Reports-Management-and-Organization.md). |

## 4.2 Creating and Editing Custom Reports

Creating and editing custom reports requires the Add/Edit/Organize
Reports user right. This right is independent of Data Export Rights. A
user can have the ability to create reports without being able to export
the resulting data, and vice versa. See [RC-EXPRT-03 — Data Export: User Rights & Export Access](RC-EXPRT-03_Data-Export-User-Rights-and-Export-Access.md) for details on
rights levels.


> **Note:** Detailed guidance on creating and configuring custom reports is covered in [RC-EXPRT-06 — Custom Reports: Setup & Field Selection](RC-EXPRT-06_Custom-Reports-Setup-and-Field-Selection.md). This article covers report types from an export perspective only.


---

# 5. Other Export Options

The Other Export Options tab at the top of the Data Exports, Reports,
and Stats page provides bulk export options that operate at the project
level rather than at the report level. These options are infrequently
used but serve specific purposes.

| **Option** | **What it does & when to use it** |
| --- | --- |
| **Export entire project as REDCap XML** | Exports the complete project — instrument definitions, data, and configuration — as a single XML file. This is the most comprehensive backup option available. The resulting file can be used to recreate the project in a new REDCap instance (see [RC-PROJ-05 — Project Migration: Moving a Project Between REDCap Installations](RC-PROJ-05_Project-Migration.md)). More complete than a Data Dictionary download, which only captures instrument structure. Shown only if your administrator has enabled it and you have both data export rights and the Project Design and Setup right; it is also offered under **Project Setup → Other Functionality**. An **Include all uploaded files and signatures?** checkbox adds uploaded files to the XML. User accounts, user rights and logging are not included. |
| **ZIP file of uploaded files (all records)** | Downloads all files uploaded through File Upload fields (including signatures) across all records as a single ZIP archive. Appears only when the project has at least one File Upload field. Your data export rights and data access group still apply, so you receive only files you are allowed to export. Standard data exports do not include uploaded files. Use this when you need to bulk-download participant-uploaded documents, images, or other files. May take significant time to generate on large projects. The ZIP is not saved to the File Repository. |
| **PDF of data collection instruments with saved data (all records)** | Generates a single PDF containing every record's data across all instruments, formatted as filled-in forms; a compact version is also offered. Useful for audits, regulatory submissions, or human-readable archives. File size and generation time can be substantial for large projects. A copy is saved in the File Repository. A PDF of a single record can also be downloaded from within the record itself. |
| **Return Codes for Surveys** | Downloads a file listing each record ID with the form status and return code for surveys that use Save & Return Later. It covers only surveys on instruments where you have Full Data Set export rights, limited to records in your data access group. |
| **Tableau Export** | Connects REDCap directly to Tableau (version 10 or later) for data visualization. Shown only when the API is enabled on your REDCap server, and requires a project API token. Considered an advanced feature — consult your REDCap support team before using. |

> **Important:** The REDCap XML export is built from the All Data report, so your own data export rights, de-identification settings and data access group apply. A user with restricted export rights, or who is in a data access group, gets a partial backup. Run full-project backups from an account with Full Data Set rights and no data access group.


> **Note:** Standard data exports (CSV, SPSS, R, etc.) do not include files uploaded through File Upload fields. If your project uses file upload fields and you need those files, use the ZIP file of uploaded files option under Other Export Options, the **Download Files (zip)** button on a report, or tick **Include all uploaded files and signatures?** on the REDCap XML export.

## 5.1 Citation Prompts in the Export Dialog *(15.5.0+)*

The download dialog shown after an export file is generated surfaces publications that may need citing in manuscripts arising from the project:

- Where **Randomization** is enabled and a randomization model has been set up, the dialog cites the REDCap randomization publication.
- Where one or more **External Modules** are enabled, it cites the External Module Framework publication.

These appear at the point of export rather than in project setup, on the reasoning that the person pulling data for analysis is the one who needs them. Worth capturing when you export rather than reconstructing at manuscript stage — check your institution's or journal's citation requirements alongside them.


---

# 6. Common Questions

| *What is the difference between All Data and Selected Instruments?* | All Data exports every instrument and every variable in the project for all records. Selected Instruments lets you choose specific instruments to include — useful when you only need a subset of the data. Both include all records you have access to. |
| --- | --- |
| *I need to export data from only consented participants. Which report type should I use?* | A custom report with a logic filter applied (e.g., [consent_status]='1'). The built-in All Data and Selected Instruments reports do not filter by record. You need the Add/Edit/Organize Reports right to create a custom report. |
| *Can I export uploaded files (PDFs, images) through a standard data export?* | No. Standard exports (CSV, SPSS, etc.) do not include files uploaded through File Upload fields. Use the ZIP file of uploaded files option under Other Export Options (or the **Download Files (zip)** button on a report) to bulk-download uploaded files, or include them in a REDCap XML export with the **Include all uploaded files and signatures?** checkbox. |
| *What is the REDCap XML export and how is it different from a Data Dictionary download?* | The REDCap XML export includes the full project — instrument structure, data, and configuration settings (but not users or logging). A Data Dictionary download includes only the instrument and variable definitions. Use the XML export for a complete project backup; use the Data Dictionary for instrument structure only. Your export rights and data access group limit which data goes into the XML. |
| *I don't see the REDCap XML option. Why?* | It appears only if your administrator has enabled it and you have both data export rights and the Project Design and Setup right. |
| *How do I get a list of survey return codes?* | Use **Return Codes for Surveys** under Other Export Options. It lists record ID, form status and return code for Save & Return Later surveys on instruments where you have Full Data Set export rights, limited to your data access group. |
| *My project has many custom reports and the left menu is cluttered. What can I do?* | Organize reports into folders. Use the **Organize** link in the Reports panel of the left-hand menu to create folders and assign reports to them; a report can sit in more than one folder. This requires the Add/Edit/Organize Reports right. See [RC-EXPRT-08 — Custom Reports: Management & Organization](RC-EXPRT-08_Custom-Reports-Management-and-Organization.md). |
| *Does a custom report export all records or only filtered ones?* | Only filtered ones, if a logic filter is applied. If no filter is set, the custom report exports all records you have access to for the selected variables. |

---

# 7. Common Mistakes & Gotchas

**Using All Data when only a subset is needed.** Exporting the full
dataset when only one instrument's data is required shares more data
than necessary and produces larger files. Use Selected Instruments or a
custom report to limit the export scope.

**Expecting standard exports to include uploaded files.** Files attached
via File Upload fields are not included in CSV, SPSS, or other standard
exports. Use the ZIP file of uploaded files option under Other Export
Options, or the uploaded-files checkbox on the REDCap XML export, if you
need those files.

**Accumulating too many unorganized custom reports.** Projects with many
custom reports can have cluttered left-hand menus and report lists.
Organize reports into folders and remove reports that are no longer
needed. This requires the Add/Edit/Organize Reports right.

**Confusing the REDCap XML export with a Data Dictionary download.** The
Data Dictionary (CSV) captures instrument and variable structure only.
The REDCap XML export captures the full project including data. Use the
XML export for complete backups; use the Data Dictionary for instrument
structure management.

**Taking an XML backup with restricted export rights.** The REDCap XML
export only contains the data you are allowed to export. A user with
de-identified or partial export rights, or one assigned to a data access
group, produces an incomplete backup. Take full backups from an account
with Full Data Set rights and no data access group.

## API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) for authentication, token management, and setup.

- **[RC-API-38 — Export Reports API](RC-API-38_Export-Reports.md)** — export a saved report programmatically by its numeric report ID

---


# 8. Related Articles

- [RC-EXPRT-01 — Data Export: Overview & Workflow](RC-EXPRT-01_Data-Export-Overview-and-Workflow.md) (prerequisite ---
    the full export process)

- [RC-EXPRT-02 — Data Export: Export Formats](RC-EXPRT-02_Data-Export-Export-Formats.md) (format selection after
    report type is chosen)

- [RC-EXPRT-03 — Data Export: User Rights & Export Access](RC-EXPRT-03_Data-Export-User-Rights-and-Export-Access.md) (rights
    required for custom reports and export access)

- [RC-EXPRT-04 — Data Export: De-identification & Formatting Options](RC-EXPRT-04_Data-Export-De-identification-and-Formatting-Options.md)

- [RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md) (the Data Dictionary download vs.
    REDCap XML backup)

- [RC-EXPRT-06 — Custom Reports: Setup & Field Selection](RC-EXPRT-06_Custom-Reports-Setup-and-Field-Selection.md)

- [RC-EXPRT-08 — Custom Reports: Management & Organization](RC-EXPRT-08_Custom-Reports-Management-and-Organization.md) (report folders)

- [RC-FILE-01 — File Repository](RC-FILE-01_File-Repository.md) (where export files and all-records PDFs are saved)

- [RC-PROJ-05 — Project Migration: Moving a Project Between REDCap Installations](RC-PROJ-05_Project-Migration.md) (using the REDCap XML file)
