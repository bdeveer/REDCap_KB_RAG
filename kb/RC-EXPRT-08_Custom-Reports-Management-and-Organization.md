| Field | Value |
|---|---|
| Article ID | RC-EXPRT-08 |
| Domain | Exports, Reports & Stats |
| Applies To | All project types; requires Add/Edit/Organize Reports privilege for most actions |
| Prerequisite | RC-EXPRT-06 — Custom Reports: Setup & Field Selection |
| Version | 1.0 |
| Last Updated | 2026 |
| Author | REDCap Support |
| Related Topics | RC-EXPRT-06 — Custom Reports: Setup & Field Selection; RC-EXPRT-07 — Custom Reports: Filtering & Ordering; RC-USER-03 — User Rights: Configuring User Privileges |

## 1. Overview

This article covers saving custom reports and working with the My Reports & Exports overview — including the options available after saving, the per-report action buttons, report identifiers, and the tools for organizing reports into folders. It is the third article in the Custom Reports series and assumes you have already created a report using RC-EXPRT-06 and optionally configured filters using RC-EXPRT-07.

---

## 2. Key Concepts & Definitions

**My Reports & Exports Overview**
The main landing page of the Data Exports, Reports & Stats menu. It lists all available report options — built-in options at the top, followed by all custom reports — along with action buttons and management controls for each.

**Report ID**
A short numeric identifier that is unique across the entire REDCap installation. Primarily used for API calls that export a specific report. Assigned automatically when a report is saved.

**Unique Report Name**
A longer alphanumeric identifier, also unique across the entire REDCap installation. Primarily used to reference a report in the Project Dashboard feature for building charts and visualizations from report data.

**Report Folder**
A named grouping that organizes custom reports in the My Reports & Exports overview. Reports can be assigned to one or more folders. Folders are visible to all users who have view access to at least one report in the folder.

**Public Link**
A URL generated for reports that have been made public. Clicking the public link in the overview opens the report in a new browser tab without requiring a login. See RC-EXPRT-06 for the criteria and considerations for making a report public.

---

## 3. Saving a Report

Once you have configured your report settings, fields, and any filters, click **Save Report** to save the report. If you are editing an existing report, this button updates it in place.

After saving, REDCap presents three options:

| Option | Description |
|---|---|
| View Report | Immediately runs the report and displays the results. Use this to verify the report looks as expected. |
| Return to My Reports & Exports | Returns to the report overview without running the report. |
| Continue Editing Report | Stays in the report builder. Use this to save progress periodically during a longer editing session without leaving the editor. |

There is no auto-save. Use **Continue Editing Report** to checkpoint your work if you are building a complex report over an extended session.

---

## 4. My Reports & Exports Overview

The overview lists all custom reports below the built-in export options. Each custom report row includes a set of action buttons and, after the report is saved, two unique identifiers.

### 4.1 Standard Action Buttons

All custom reports share the same three primary action buttons available on built-in reports:

| Button | Description |
|---|---|
| View Report | Runs and displays the report results. |
| Export Data | Exports the report's data in your chosen file format (CSV, SPSS, SAS, R, Stata). |
| Stats & Charts | Displays basic descriptive statistics and charts for the report's variables. |

> **Note:** Users without sufficient user rights may not see all three buttons. Export Data, in particular, requires the appropriate export privilege.

### 4.2 Management Options (Custom Reports Only)

Each custom report also has three management buttons in the Management Options column:

| Button | Description |
|---|---|
| Edit | Opens the report builder for that report. Only available if the user has edit access to the report and holds the Add/Edit/Organize Reports privilege. |
| Copy | Clones the entire report — all settings, fields, filters, and access rules — into a new report. The copy appears in the overview and can be renamed and modified independently. Useful for building a new report based on an existing one. |
| Delete | Permanently removes the report from the project. **This action does not delete any data.** Only the report definition is removed. |

> **Important:** The Delete button removes the report immediately without a secondary confirmation step in all REDCap versions. Verify you are deleting the correct report before clicking.

### 4.3 Report Identifiers

Each saved custom report displays two identifiers in the overview:

**Report ID:** A short numeric ID unique to the entire REDCap installation. Used primarily in API calls to export a specific report. Refer to your installation's API documentation or the API Playground for details on report-based API exports.

**Unique Report Name:** A longer alphanumeric string, also unique installation-wide. Used in the Project Dashboard feature to build charts and graphs sourced from a specific report's data.

### 4.4 Public Link

If a report has been made public (see RC-EXPRT-06, Section 4.2), a blue **Public** link appears in its row in the overview. Clicking this link opens the public report in a new browser tab. This provides a quick way to preview or verify the public report without navigating through the report edit menu.

---

## 5. Report Folders

Projects with many custom reports can become difficult to navigate. Report folders allow you to group related reports under named headings in the My Reports & Exports overview.

### 5.1 Accessing the Folder Manager

The folder management interface is accessed via the **Organize** link in the report section header in the **left-hand project menu** — not from within the Data Exports, Reports & Stats page itself. This is a common point of confusion.

### 5.2 Creating a Folder

In the folder manager, enter a name in the **New Folder** text box and click **Add**. The folder is created immediately and will appear in the overview for all users who have view access to at least one report assigned to it.

Folder names should be meaningful to all users of the project, not just the creator.

### 5.3 Assigning Reports to a Folder

1. Select a folder from the dropdown in the folder manager.
2. REDCap displays a list of all reports in the project. Check the box next to each report you want to assign to that folder.
3. Unchecking a report removes it from the folder.

A report can be assigned to more than one folder simultaneously. This is useful when a report is relevant to multiple working groups or purposes.

### 5.4 Search and Edit Links

The report section header also includes two additional navigation links:

**Search:** Opens a search box that filters all reports by name. Useful when a project has a large number of reports and you need to locate one quickly. Clicking a result in the search navigates directly to that report.

**Edit:** Returns you to the Data Exports, Reports & Stats overview page. This link is relevant when you have navigated away to the folder manager and want to return to the main report list.

---

## 6. Common Questions

**Q: I deleted a report by accident. Can I recover it?**
A: No. Deleting a report is permanent and there is no undo. The report definition is gone; you would need to recreate it from scratch. The data the report displayed is not affected — only the report configuration is lost.

**Q: What is the difference between the Report ID and the Unique Report Name?**
A: Both are unique identifiers, but they are used in different contexts. The Report ID (short numeric) is used in API calls to export a specific report's data programmatically. The Unique Report Name (longer alphanumeric) is used in the Project Dashboard feature to build charts from a report. Neither is user-facing in the report itself.

**Q: Can I assign a report to more than one folder?**
A: Yes. A report can belong to multiple folders simultaneously. This is intentional — if a report is relevant to two different teams, it can appear in both teams' folders.

**Q: Who can see report folders?**
A: All project users who have view access to at least one report in a folder will see the folder in the overview. Users with no access to any report in a folder will not see that folder.

**Q: Can I reorder reports within the overview?**
A: Custom reports appear in the order they were created by default. Report folders provide the primary means of organization. Within a folder, the order is determined by the order reports were assigned to it.

**Q: Where do I find the Report ID for an API call?**
A: The Report ID is displayed in the My Reports & Exports overview, in the row for the report. It is a short numeric value. You can also find it in the report URL when editing the report (the `id=` parameter in the URL).

**Q: I don't see the Organize link to access report folders. Why?**
A: The Organize link is located in the left-hand project menu under the reports section header — not on the Data Exports, Reports & Stats page. If you do not see it, your version of REDCap may not support report folders, or you may not have the Add/Edit/Organize Reports privilege.

---

## 7. Common Mistakes & Gotchas

**Looking for report folders in the Data Exports menu.** The folder manager is accessed via the left-hand project menu (the Organize link), not from within the Data Exports, Reports & Stats page. Users who expect it on the export page will not find it there.

**Clicking Delete assuming there is a confirmation step.** REDCap may not prompt for confirmation before deleting a report. Double-check you have selected the correct report before clicking Delete. There is no recovery option.

**Confusing Copy with Export.** The Copy button clones the report definition (settings, fields, filters), not the report's data. It creates a new report that can be edited independently. It is not the same as exporting data from the report.

**Assigning a report to a folder and assuming all users can see it.** Folders are visible only to users who have view access to at least one report inside the folder. If all reports in a folder are restricted to a small group, other users will not see the folder at all.

**Expecting the Search link to search data, not report names.** The Search function in the report header searches report names only. It does not search the data within reports. Use the View Report and Export Data buttons to interact with report data.

---

## 8. Related Articles

- RC-EXPRT-06 — Custom Reports: Setup & Field Selection (prerequisite — creating a report and selecting fields)
- RC-EXPRT-07 — Custom Reports: Filtering & Ordering (configuring filters and result ordering)
- RC-USER-03 — User Rights: Configuring User Privileges (covers Add/Edit/Organize Reports and export privileges)
- RC-DAG-01 — Data Access Groups (background on DAG-based report access and filtering)
