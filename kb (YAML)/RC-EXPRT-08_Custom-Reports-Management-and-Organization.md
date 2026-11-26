---
id: RC-EXPRT-08
title: 'Custom Reports: Management & Organization'
domain: Exports, Reports & Stats
applies_to:
- All project types
- requires Add/Edit/Organize Reports privilege for most actions
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — report
  management and folder behaviour checked against source code; pages not re-captured
prerequisites:
- 'RC-EXPRT-06 — Custom Reports: Setup & Field Selection'
version: '1.2'
last_updated: 2026-11
related:
- id: RC-EXPRT-06
  title: 'Custom Reports: Setup & Field Selection'
- id: RC-EXPRT-07
  title: 'Custom Reports: Filtering & Ordering'
- id: RC-USER-03
  title: 'User Rights: Configuring User Privileges'
tags:
- exports, reports & stats
- data
synonyms:
- how to save and edit a custom report
- organize reports into folders
- my reports and exports page
- find a report id for the api
- copy delete or rename a report
- manage existing reports
- where are my saved reports
- unique report name for dashboards
---

> **Public report access codes (16.0.5+).** A public report can be protected with an access code, set manually or auto-generated, and retrievable via `[report-access-code:unique_report_name]`. Configuration is covered in [RC-EXPRT-06 — Custom Reports: Setup & Field Selection](RC-EXPRT-06_Custom-Reports-Setup-and-Field-Selection.md) §4.2; the smart variable in [RC-PIPE-15 — Smart Variables: Public Reports](RC-PIPE-15_Smart-Variables-Public-Reports.md). The **unique report name** needed for the smart variable appears in the far-right column of the reports list on this page.

# 1. Overview

This article covers saving custom reports and working with the My Reports & Exports overview — including the options available after saving, the per-report action buttons, report identifiers, and the tools for organizing reports into folders. It is the third article in the Custom Reports series and assumes you have already created a report using [RC-EXPRT-06 — Custom Reports: Setup & Field Selection](RC-EXPRT-06_Custom-Reports-Setup-and-Field-Selection.md) and optionally configured filters using [RC-EXPRT-07 — Custom Reports: Filtering & Ordering](RC-EXPRT-07_Custom-Reports-Filtering-and-Ordering.md).

---

# 2. Key Concepts & Definitions

**My Reports & Exports Overview**
The main landing page of the Data Exports, Reports & Stats menu. It lists all available report options — built-in options at the top, followed by all custom reports — along with action buttons and management controls for each.

**Report ID**
A short numeric identifier that is unique across the entire REDCap installation. Primarily used for API calls that export a specific report. Assigned automatically when a report is saved. It also appears in your browser's address bar as `report_id=` when you view or edit the report.

**Unique Report Name**
A text identifier made of "R-" followed by 10 letters and digits (for example, `R-2554F4TCNT`). It is unique **within the project**, not across the installation: a copied project keeps the same unique report names as the original. Used to reference a report in Smart Charts, Smart Tables and Smart Functions (for example, on Project Dashboards) and in the `[report-access-code]` smart variable.

**Report Folder**
A named grouping that organizes custom reports in the **Reports** panel of the left-hand project menu. Folders are created explicitly by a user with the Add/Edit/Organize Reports privilege, and a report can be assigned to one or more folders. Folders do not appear in the My Reports & Exports list itself. A folder is shown only to users who have view access to at least one report in it.

**Public Link**
A URL generated for reports that have been made public. Clicking the public link in the overview opens the report in a new browser tab. By default no login is required to view it (for the REDCap+ login-protection exception, see Section 4.4). See [RC-EXPRT-06 — Custom Reports: Setup & Field Selection](RC-EXPRT-06_Custom-Reports-Setup-and-Field-Selection.md) for the criteria and considerations for making a report public.

---

# 3. Saving a Report

Once you have configured your report settings, fields, and any filters, click **Save Report** to save the report. If you are editing an existing report, this button updates it in place.

After saving, REDCap presents three options:

| Option | Description |
|---|---|
| View Report | Immediately runs the report and displays the results. Use this to verify the report looks as expected. |
| Return to My Reports & Exports | Returns to the report overview without running the report. |
| Continue Editing Report | Stays in the report builder. Use this to save progress periodically during a longer editing session without leaving the editor. |

There is no auto-save. Use **Continue Editing Report** to checkpoint your work if you are building a complex report over an extended session.

---

# 4. My Reports & Exports Overview

The overview lists all custom reports below the built-in export options. Each custom report row includes a set of action buttons and, after the report is saved, two unique identifiers.

Users with the Add/Edit/Organize Reports privilege see every custom report in this list, regardless of the report's View Access setting. The **Reports** panel in the left-hand menu shows each user only the reports they have view access to.

## 4.1 Standard Action Buttons

All custom reports share the same three primary action buttons available on built-in reports:

| Button | Description |
|---|---|
| View Report | Runs and displays the report results. |
| Export Data | Exports the report's data in your chosen file format (CSV, SPSS, SAS, R, Stata). |
| Stats & Charts | Displays basic descriptive statistics and charts for the report's variables. |

> **Note:** Users without sufficient user rights may not see all three buttons. Export Data, in particular, requires the appropriate export privilege.

## 4.2 Management Options (Custom Reports Only)

Each custom report also has three management buttons in the Management Options column:

| Button | Description |
|---|---|
| Edit | Opens the report builder for that report. |
| Copy | After a confirmation prompt, clones the report — settings, fields, filters, and access rules — into a new report. The copy is titled with " (copy)" added to the original name and is placed directly after the original in the list. It gets its own report ID and unique report name, is **not** public (even if the original was), and is **not** placed in the original's folders. Rename and modify it independently. Useful for building a new report based on an existing one. |
| Delete | After a confirmation prompt, permanently removes the report from the project. **This action does not delete any data.** Only the report definition is removed. The deletion is recorded in the project's Logging. |

All three management buttons require the Add/Edit/Organize Reports privilege **and** edit access to that specific report. REDCap checks this on the server, not just by hiding the buttons.

> **Important:** REDCap asks you to confirm before deleting, but once confirmed the deletion cannot be undone. Read the report name in the prompt before confirming.

> **Note:** A report cannot be edited while it is public. To change a public report, turn public access off, edit and save the report, then make it public again (see [RC-EXPRT-06 — Custom Reports: Setup & Field Selection](RC-EXPRT-06_Custom-Reports-Setup-and-Field-Selection.md) §4.2).

## 4.3 Report Identifiers

Each saved custom report displays two identifiers in the overview:

**Report ID:** A short numeric ID unique to the entire REDCap installation. Used primarily in API calls to export a specific report. Clicking the ID opens a short explanation of where it is used (the API and Smart Charts). Refer to your installation's API documentation or the API Playground for details on report-based API exports.

**Unique Report Name:** "R-" followed by 10 letters and digits (for example, `R-2554F4TCNT`), unique within the project. A copied project keeps the same unique report names. Used to point Smart Charts, Smart Tables and Smart Functions at a specific report's data (see [RC-PIPE-14 — Smart Variables: Project Dashboards](RC-PIPE-14_Smart-Variables-Project-Dashboards.md)) and in the `[report-access-code]` smart variable.

## 4.4 Public Link

If a report has been made public (see [RC-EXPRT-06 — Custom Reports: Setup & Field Selection](RC-EXPRT-06_Custom-Reports-Setup-and-Field-Selection.md), Section 4.2), a blue **Public** link appears in its row in the overview. Clicking this link opens the public report in a new browser tab. This provides a quick way to preview or verify the public report without navigating through the report edit menu. The link is shown only to users who hold the User Rights privilege, and only when public reports are enabled on your instance.

> **Version caveat (REDCap+, 17.5.0+):** A public link normally opens without a login, but on instances with an active REDCap+ subscription the report may be set to require a REDCap login first. This option does not exist on 17.3 or 16.0 LTS. If a colleague reports being asked to log in, check the report's login protection setting (see [RC-EXPRT-06 — Custom Reports: Setup & Field Selection](RC-EXPRT-06_Custom-Reports-Setup-and-Field-Selection.md) §4.2).

---

# 5. Report Folders

Projects with many custom reports can become difficult to navigate. Report folders allow you to group related reports under named, collapsible headings in the **Reports** panel of the left-hand project menu. Folders appear only in that panel; the My Reports & Exports list on the Data Exports, Reports & Stats page is not grouped by folder.

## 5.1 Accessing the Folder Manager

The folder management interface is accessed via the **Organize** link in the report section header in the **left-hand project menu** — not from within the Data Exports, Reports & Stats page itself. This is a common point of confusion. The link is shown only to users with the Add/Edit/Organize Reports privilege.

## 5.2 Creating, Renaming and Deleting Folders

In the folder manager, enter a name (up to 64 characters) in the **New Folder** text box and click **Add**. The folder is created immediately and will appear in the left-hand Reports panel for all users who have view access to at least one report assigned to it.

Existing folders can be renamed or deleted from the same manager. Deleting a folder does not delete the reports in it. Creating, renaming and deleting folders is recorded in the project's Logging.

Folder names should be meaningful to all users of the project, not just the creator.

## 5.3 Assigning Reports to a Folder

1. Select a folder from the dropdown in the folder manager.
2. REDCap displays a list of all reports in the project. Check the box next to each report you want to assign to that folder. Use the **hide reports already assigned** option to shorten the list to reports you have not yet placed in a folder.
3. Unchecking a report removes it from the folder.

A report can be assigned to more than one folder simultaneously. This is useful when a report is relevant to multiple working groups or purposes.

## 5.4 Reordering Reports and Folders

Users with the Add/Edit/Organize Reports privilege can drag and drop reports into a new order, and can also reorder folders. Within a folder, reports follow the overall report order.

## 5.5 Search and Edit Links

The report section header also includes two additional navigation links:

**Search:** Opens a search box that filters all reports by title. Type at least 2 characters; each word is matched separately (a report matching any of the words is listed), and up to 20 results are shown. Useful when a project has a large number of reports and you need to locate one quickly. Clicking a result in the search navigates directly to that report.

**Edit:** Returns you to the Data Exports, Reports & Stats overview page. This link is relevant when you have navigated away to the folder manager and want to return to the main report list.

> **Note:** The **Reports** header itself in the left-hand menu is also a link to My Reports & Exports (present in 17.6). On older versions, use the Edit link or the Data Exports, Reports & Stats menu item.

---

# 6. Common Questions

**Q: I deleted a report by accident. Can I recover it?**
**A:** No. REDCap asks for confirmation first, but once confirmed, deleting a report is permanent and there is no undo. The report definition is gone; you would need to recreate it from scratch. The data the report displayed is not affected — only the report configuration is lost.

**Q: What is the difference between the Report ID and the Unique Report Name?**
**A:** Both are unique identifiers, but they are used in different contexts. The Report ID (short numeric) is used in API calls to export a specific report's data programmatically. The Unique Report Name ("R-" plus 10 letters and digits) is used in Smart Charts, Smart Tables and Smart Functions to build charts and tables from a report, and in the `[report-access-code]` smart variable. The Report ID is unique across the installation; the Unique Report Name is unique only within the project, and a copied project keeps the same names. Neither is user-facing in the report itself.

**Q: Can I assign a report to more than one folder?**
**A:** Yes. A report can belong to multiple folders simultaneously. This is intentional — if a report is relevant to two different teams, it can appear in both teams' folders.

**Q: Who can see report folders?**
**A:** All project users who have view access to at least one report in a folder will see the folder in the left-hand Reports panel (folders are not shown in the My Reports & Exports list). Users with no access to any report in a folder will not see that folder.

**Q: Can I reorder reports within the overview?**
**A:** Yes, if you have the Add/Edit/Organize Reports privilege. New reports are added at the end of the list (a copy is placed directly after its original), and you can drag and drop reports into a different order. Folders can be reordered the same way. Within a folder, reports follow the overall report order.

**Q: Where do I find the Report ID for an API call?**
**A:** The Report ID is displayed in the My Reports & Exports overview, in the row for the report. It is a short numeric value. You can also find it in your browser's address bar when viewing or editing the report (the `report_id=` parameter in the URL).

**Q: I don't see the Organize link to access report folders. Why?**
**A:** The Organize link is located in the left-hand project menu under the reports section header — not on the Data Exports, Reports & Stats page. If you do not see it, your version of REDCap may not support report folders, or you may not have the Add/Edit/Organize Reports privilege.

---

# 7. Common Mistakes & Gotchas

**Looking for report folders in the Data Exports menu.** The folder manager is accessed via the left-hand project menu (the Organize link), not from within the Data Exports, Reports & Stats page. Users who expect it on the export page will not find it there.

**Treating the Delete confirmation as a safety net.** REDCap asks you to confirm before deleting a report, but there is no recovery once you confirm. Check the report name in the prompt before clicking through.

**Expecting a copy to keep the original's folders or public status.** A copied report is not public and is not in any folder. Add it to folders and make it public again if needed.

**Confusing Copy with Export.** The Copy button clones the report definition (settings, fields, filters), not the report's data. It creates a new report that can be edited independently. It is not the same as exporting data from the report.

**Looking for folders in the My Reports & Exports list.** Folders group reports only in the left-hand Reports panel; the list on the Data Exports, Reports & Stats page is not grouped by folder.

**Assigning a report to a folder and assuming all users can see it.** Folders are visible only to users who have view access to at least one report inside the folder. If all reports in a folder are restricted to a small group, other users will not see the folder at all.

**Expecting the Search link to search data, not report names.** The Search function in the report header searches report titles only. It does not search the data within reports. Use the View Report and Export Data buttons to interact with report data.

---

## API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) for authentication, token management, and setup.

- **[RC-API-38 — Export Reports API](RC-API-38_Export-Reports.md)** — use the numeric report ID (visible in the report URL) to export any report programmatically

---


# 8. Related Articles

- [RC-EXPRT-06 — Custom Reports: Setup & Field Selection](RC-EXPRT-06_Custom-Reports-Setup-and-Field-Selection.md) (prerequisite — creating a report and selecting fields)
- [RC-EXPRT-07 — Custom Reports: Filtering & Ordering](RC-EXPRT-07_Custom-Reports-Filtering-and-Ordering.md) (configuring filters and result ordering)
- [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) (covers Add/Edit/Organize Reports and export privileges)
- [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) (background on DAG-based report access and filtering)
- [RC-PIPE-14 — Smart Variables: Project Dashboards](RC-PIPE-14_Smart-Variables-Project-Dashboards.md) (using a unique report name in Smart Charts, Tables and Functions)
- [RC-PIPE-15 — Smart Variables: Public Reports](RC-PIPE-15_Smart-Variables-Public-Reports.md) (the `[report-access-code]` smart variable)
