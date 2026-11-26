---
id: RC-EXPRT-01
title: Data Export — Overview & Workflow
domain: Exports, Reports & Stats
applies_to:
- All REDCap project types
- requires Data Export user rights
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — data export
  behaviour checked against source code; pages not re-captured
prerequisites:
- RC-NAV-UI-01 — Project Navigation UI
version: '1.2'
last_updated: 2026-11
related:
- id: RC-EXPRT-02
  title: 'Data Export: Export Formats'
- id: RC-EXPRT-03
  title: 'Data Export: User Rights & Export Access'
- id: RC-EXPRT-04
  title: 'Data Export: De-identification & Formatting Options'
- id: RC-EXPRT-05
  title: 'Data Export: Report Types & Other Export Options'
tags:
- exports, reports & stats
- data
synonyms:
- how do i export my data from redcap
- where is the data export tool
- get my data out of redcap
- run a data export step by step
- download project data
- export reports and stats overview
- how to start an export
- data exports reports and stats application
---

# 1. Overview

This article explains how to export data from a REDCap project. It
covers how to navigate to the Data Exports, Reports, and Stats
application and walks through the standard export workflow from start to
finish. It is the entry point for the Exports, Reports & Stats knowledge
base series.

---

# 2. Key Concepts & Definitions

**Data Exports, Reports, and Stats**

The REDCap application that provides all data export and reporting
functionality. Accessible from the left-hand menu under Applications.
Visibility depends on user rights — if a user has any export access,
the Add/Edit/Organize Reports right, or the Stats & Charts right, this
application appears in their menu.

**Export**

The process of downloading project data from REDCap into an external
file. Exports are generated from within the Data Exports, Reports, and
Stats application. REDCap stores a copy of every export made through the
Export Data dialog in the File Repository for later re-download.

**Report**

A defined selection of data to export. REDCap provides two built-in
reports (All Data and Selected Instruments/Events) and allows users with
the Add/Edit/Organize Reports right to create custom reports. A report
determines which records and variables are included in an export.

**Export Format**

The file format REDCap uses to deliver the exported data. REDCap
supports seven formats: CSV/Excel (raw data), CSV/Excel (labels), SPSS,
SAS, R, Stata, and CDISC ODM (XML). Format selection affects how data
values are represented and how many files are generated. See [RC-EXPRT-02 — Data Export: Export Formats](RC-EXPRT-02_Data-Export-Export-Formats.md)
for full details.

**File Repository**

A project-level storage area where REDCap automatically saves a copy of
every data export made through the Export Data dialog (API exports and
the ZIP of uploaded files are not saved there). Users can re-download a
previous export from the File Repository without repeating the export
process. Access requires the File Repository user right, and what you
can see in the Data Export Files folder also depends on your export
rights (see Section 4).

**De-identification Options**

Optional settings applied during export that remove or transform
potentially identifying information. Available options vary based on the
user's Data Export Rights level. See [RC-EXPRT-04 — Data Export: De-identification & Formatting Options](RC-EXPRT-04_Data-Export-De-identification-and-Formatting-Options.md) for full details.

---

# 3. Navigating to the Data Exports, Reports, and Stats Application

The Data Exports, Reports, and Stats application is accessed from within
a REDCap project. It does not appear if a user has no export rights and
neither the Add/Edit/Organize Reports right nor the Stats & Charts right
is granted.

## 3.1 From the Left-Hand Menu

| **1** | Log in and open your project from the My Projects page. |
| --- | --- |
| **2** | In the left-hand menu, locate the Applications section. |
| **3** | Select Data Exports, Reports, and Stats. The application opens to the report list. |


> **Note:** If Data Exports, Reports, and Stats does not appear in your menu, your account has no Data Export rights and neither the Add/Edit/Organize Reports right nor the Stats & Charts right is enabled. Users who have only Add/Edit/Organize Reports or Stats & Charts see the application but no Export Data buttons. Contact your project administrator to review your user rights.


---

# 4. The Standard Export Workflow

Every export in REDCap follows the same sequence of steps, regardless of
the report type or export format selected.

| **1** | Navigate to the Data Exports, Reports, and Stats application (see Section 3). |
| --- | --- |
| **2** | Locate the report you want to export — All Data, Selected Instruments/Events, or a custom report. Select Export Data for that report. |
| **3** | Choose an export format from the seven available options. See [RC-EXPRT-02 — Data Export: Export Formats](RC-EXPRT-02_Data-Export-Export-Formats.md) for guidance on which format to choose. |
| **4** | Set de-identification options if required or desired. Options available depend on your Data Export Rights level. See [RC-EXPRT-04 — Data Export: De-identification & Formatting Options](RC-EXPRT-04_Data-Export-De-identification-and-Formatting-Options.md) for full details. |
| **5** | Review additional export options and data formatting options. The defaults are appropriate for most exports. See [RC-EXPRT-04 — Data Export: De-identification & Formatting Options](RC-EXPRT-04_Data-Export-De-identification-and-Formatting-Options.md) for details on each option. REDCap remembers your CSV delimiter and decimal character choices for the next export. |
| **6** | Select the Export Data button to generate the export files. Large exports can take a while; if an export runs longer than about three minutes, REDCap shows a notice and a Cancel button. |
| **7** | Download all generated files. The number of files depends on the export format — some formats generate multiple files that must all be downloaded. Read the included format-specific instructions carefully. The dialog also shows how to cite REDCap (and any other publications relevant to the project) in your work. |
| **8** | Select the Close button to finish. REDCap saves a copy of this export in the File Repository automatically. |


> **Tip:** If you need to re-download an export you generated previously, navigate to the File Repository application in the left-hand menu and open the Data Export Files folder. REDCap stores a copy of every export made through the Export Data dialog there. You do not need to run the export again.

> **Note:** What you can see and download in the Data Export Files folder depends on your rights. The folder appears empty if you have no export rights, or if your export rights are De-identified on every instrument or Remove Identifiers on every instrument; downloading a listed file requires Full Data Set rights on every instrument in that file; and users in a Data Access Group see only exports made by users in their own group.

> **Note:** Saved export files are not kept forever. An administrator can set a project to delete them automatically after a number of days, and they are removed when all project data is erased (including when the project is moved to production with the option to delete data). Keep your own copy of any export you need to retain.

> **Institution-specific:** Whether saved export files are deleted automatically, and after how long, is set by your REDCap administrators. Check with them if you rely on the File Repository copy.

**Other ways to get data out.** Two related options sit alongside the standard workflow:

- **REDCap Project (XML)** — exports the project's metadata and, optionally, its data as a single file that can be used to create a copy of the project. It is only offered if your administrators have enabled it, you have export rights above No Access, and you have the Project Design and Setup right.
- **ZIP of uploaded files** — downloads the files stored in the project's File Upload fields. It respects your export rights, but the ZIP is not saved to the File Repository.

See [RC-EXPRT-05 — Data Export: Report Types & Other Export Options](RC-EXPRT-05_Data-Export-Report-Types-and-Other-Export-Options.md) for these and other export options.


---

# 5. Common Questions

| *Where do I find the Data Exports, Reports, and Stats application?* | In the left-hand project menu under Applications. If it does not appear, you have no Data Export rights, no Add/Edit/Organize Reports right and no Stats & Charts right. Contact your project administrator. |
| --- | --- |
| *I ran an export this morning and accidentally deleted the file. Do I have to run it again?* | Usually not. Navigate to the File Repository application in the left-hand menu and open Data Export Files. REDCap automatically saves a copy of every export made through the Export Data dialog there. Download it directly without repeating the export process, provided your rights let you see it and the file has not since been deleted (see Section 4). |
| *How many files does REDCap generate when I export?* | It depends on the export format. CSV/Excel generates one file. SPSS generates three files (the third is an optional Windows Pathway Mapper file that helps SPSS locate the data file). SAS, R, and Stata each generate two files. CDISC ODM generates one XML file. All files for a given format must be downloaded together for the data to load correctly in the target application. |
| *Do I have to set de-identification options every time?* | No. De-identification options are optional if your export rights allow a Full Data Set export. They are required only if your rights are set to De-identified or Remove All Identifier Fields. See [RC-EXPRT-03 — Data Export: User Rights & Export Access](RC-EXPRT-03_Data-Export-User-Rights-and-Export-Access.md) and [RC-EXPRT-04 — Data Export: De-identification & Formatting Options](RC-EXPRT-04_Data-Export-De-identification-and-Formatting-Options.md) for details. |
| *Why can't I see the Data Exports, Reports, and Stats application in my menu?* | The application only appears if you have at least one of the following: any Data Export right above No Access, the Add/Edit/Organize Reports right, or the Stats & Charts right. If none is granted, the application is hidden entirely. |
| *Can I export data from multiple instruments at once?* | Yes. Use the Selected Instruments/Events report to choose which instruments to include. For longitudinal projects, you can also choose specific events; if you leave the event selection at its default (all events), every event is included. See [RC-EXPRT-05 — Data Export: Report Types & Other Export Options](RC-EXPRT-05_Data-Export-Report-Types-and-Other-Export-Options.md) for details on report types. |
| *What happens if I close the export dialog before downloading my files?* | The files are still saved in the File Repository. Navigate there to download them, subject to your rights and as long as the files have not been deleted. |
| *Why does the export dialog mention a randomization paper?* | When the project uses the Randomization module, the export dialog (15.5.0+) names the REDCap randomization publication, which you may need to cite in manuscripts alongside the standard REDCap citation. See [RC-RAND-03 — Working with & Managing Randomization](RC-RAND-03_Working-with-Randomization.md). |

---

# 6. Common Mistakes & Gotchas

**Not downloading all generated files.** Some export formats (SPSS, SAS,
R, Stata) generate two or three files that must be used together.
Downloading only the data file without the accompanying syntax or label
file will result in an incomplete or unreadable dataset. Always download
every file listed in the export dialog.

**Re-running an export to get a previous snapshot.** Re-running an
export generates a new snapshot of the current data — it does not
recover the state of the data at the time of the original export. Use
the File Repository to retrieve a previous export file.

**Assuming the application is missing when it is simply hidden.** The
Data Exports, Reports, and Stats application only appears when the user
has appropriate rights. Before reporting it as missing, check your user
rights with the project administrator.

**Closing the export dialog before downloading.** The export dialog
times out or may be dismissed before all files are downloaded. If this
happens, the files are still accessible in the File Repository ---
navigate there to complete the download.

**Expecting API exports or uploaded-file ZIPs in the File Repository.**
Only exports made through the Export Data dialog are saved there. Keep
your own copy of data retrieved through the API or of a ZIP of uploaded
files.

## API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) for authentication, token management, and setup.

- **[RC-API-02 — Export Records API](RC-API-02_Export-Records.md)** — programmatically retrieve project records in CSV, JSON, or XML
- **[RC-API-38 — Export Reports API](RC-API-38_Export-Reports.md)** — programmatically export data from a saved custom report by report ID

---


# 7. Related Articles

- [RC-EXPRT-02 — Data Export: Export Formats](RC-EXPRT-02_Data-Export-Export-Formats.md) (the seven available
    formats and when to use each)

- [RC-EXPRT-03 — Data Export: User Rights & Export Access](RC-EXPRT-03_Data-Export-User-Rights-and-Export-Access.md) (how rights
    affect what you can export)

- [RC-EXPRT-04 — Data Export: De-identification & Formatting Options](RC-EXPRT-04_Data-Export-De-identification-and-Formatting-Options.md)

- [RC-EXPRT-05 — Data Export: Report Types & Other Export Options](RC-EXPRT-05_Data-Export-Report-Types-and-Other-Export-Options.md) (All Data, Selected
    Instruments, custom reports, other export options)

- [RC-NAV-UI-01 — Project Navigation UI](RC-NAV-UI-01_Project-Navigation-UI.md) (prerequisite — left-hand
    menu and application access)

- [RC-NAV-UI-02 — Project Menu Reference](RC-NAV-UI-02_Project-Menu-Reference.md) (Data Exports, Reports, and
    Stats menu item reference)
