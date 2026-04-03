| Field | Value |
|---|---|
| Article ID | RC-EXPRT-06 |
| Domain | Exports, Reports & Stats |
| Applies To | All project types; requires Add/Edit/Organize Reports privilege |
| Prerequisite | RC-EXPRT-05 — Data Export: Report Types & Other Export Options |
| Version | 1.0 |
| Last Updated | 2026 |
| Author | REDCap Support |
| Related Topics | RC-EXPRT-07 — Custom Reports: Filtering & Ordering; RC-EXPRT-08 — Custom Reports: Management & Organization; RC-DAG-01 — Data Access Groups; RC-USER-03 — User Rights: Configuring User Privileges |

## 1. Overview

This article explains how to create a custom report in REDCap and select the variables it displays. Custom reports let you define a persistent, reusable view of specific fields across your project's records — unlike the built-in "All Data" or single-instrument options, which are fixed. This is the first article in the Custom Reports series (RC-EXPRT-06 through RC-EXPRT-08); it covers navigation to the report builder, report-level settings (name, public access, description, user access), and all methods for adding and arranging variables. Filtering and result ordering are covered in RC-EXPRT-07; saving and report management in RC-EXPRT-08.

---

## 2. Key Concepts & Definitions

**Custom Report**
A named, saved report that you define by selecting specific variables, optional filters, and access rules. Custom reports persist in the project and can be run, exported, or shared repeatedly without reconfiguration.

**Data Exports, Reports & Stats Menu**
The left-hand project menu item that provides access to all export and reporting features. Custom reports are created and managed from this menu.

**Report Builder**
The interface used to create or edit a custom report. It is divided into numbered steps: Step 1 (user access), Step 2 (field selection), Step 3 (filters), and Step 4 (ordering). Steps 3 and 4 are optional.

**Public Report**
A report made accessible via a shareable URL to anyone who has the link, including people who are not REDCap users on the project. Requires meeting three system-enforced criteria before activation.

**Live Filter**
A variable designated as an on-the-fly filter for a report. Live filters let users narrow report results without editing the report itself. Covered in RC-EXPRT-07.

**Add/Edit/Organize Reports Privilege**
The user right that controls who can create, edit, copy, and delete custom reports. A user without this right can view reports they have been granted access to, but cannot modify them.

---

## 3. Navigating to the Report Builder

Custom reports are accessed through the Data Exports, Reports & Stats menu in the left-hand project navigation.

From the project home page, click the project name to open it, then locate **Data Exports, Reports & Stats** in the left menu. This page lists all available report options, including built-in options (All Data, single-instrument reports) and any existing custom reports.

To create a new custom report from scratch, click the **+ Create New Report** button in the report name column header.

Alternatively, if you want to base a new custom report on one of the built-in options (e.g., a single-instrument view you have already filtered), configure that view and then click **+ Create report based on the selections above**. This opens the report builder with your current selections pre-filled, which you can then refine.

---

## 4. Report-Level Settings

Before selecting fields, the report builder presents several report-level settings. These control the report's identity and access rules.

### 4.1 Title

The report name is required. It appears in the report list and in any export filenames. Best practice is to use a short, descriptive title that is meaningful to any user who will interact with the report. Titles can be changed at any time after saving.

### 4.2 Public Reports

The public report option, when enabled, generates a shareable URL that allows anyone with the link to view the report — no REDCap login required. This is useful for sharing non-sensitive lists (e.g., a public sign-up sheet) with people outside your project.

Before a report can be made public, REDCap automatically checks three criteria:

| Criterion | Description |
|---|---|
| User Rights privilege | The user enabling public access must have User Rights privileges in the project |
| No Identifier fields | The report must not contain any fields marked as identifiers |
| Report viewed | The user must have viewed the report to confirm the correct report is being made public |

If any criterion is not met, REDCap blocks activation. When all three pass, REDCap also requires you to attest that you understand the data will be fully accessible to anyone with the link. This action is logged in the audit trail.

Once public, you can optionally create a custom short link to make the URL easier to share.

> **Important:** Never make a report public if it contains sensitive, identifiable, or protected information. Some REDCap installations have disabled the public report feature entirely to comply with data privacy requirements.

> **Yale-specific:** [Confirm whether public reports are enabled at this installation and any applicable data governance requirements — leave blank until confirmed with Yale REDCap support team]

### 4.3 Description

An optional free-text description that accepts basic rich-text formatting. The description is displayed above the report results when the report is viewed. Use this to explain the report's purpose, document any filters applied, or provide context for users who did not create the report.

---

## 5. Step 1: User Access

Step 1 defines who can view and edit the report. By default, all project users can view and edit a new report, subject to their existing user rights.

> **Note:** A user can only edit a report if they also hold the Add/Edit/Organize Reports privilege. The report-level edit access setting does not override that user right.

### 5.1 Access by Individual User, Role, or DAG

The access controls offer three selection boxes — individual users, user roles, and Data Access Groups (DAGs) — for both view and edit rights independently.

| Selection type | Behavior |
|---|---|
| Individual user | Grants access to that specific user |
| User role | Grants access to all current members of the role |
| DAG | Grants access to all current members of the DAG |

Selecting a role or DAG is preferred over selecting individual users when the project has a defined team structure, because these selections are **dynamic**: users added to a role or DAG later will automatically gain access to the report. Selecting individual users requires manual updates each time someone joins the project.

The three selection boxes are not mutually exclusive. You can combine individual users, roles, and DAGs in any combination for either view or edit access.

### 5.2 Verifying Access

To check exactly which users will have access based on your current selections, click **View user access list**. REDCap evaluates your selections and displays the resulting list of users, which is helpful when users belong to overlapping roles and DAGs.

> **Note:** A user's report access does not override their instrument-level user rights. If a report includes variables from an instrument the user cannot view, those variables will be hidden from that user's view of the report — but the report itself will still appear to them.

---

## 6. Step 2: Field Selection

Step 2 is where you choose which variables the report displays. REDCap provides four methods for adding variables; all four can be used in combination within the same report.

### 6.1 Four Methods for Adding Variables

**Choose Instrument method**
Select an instrument from the dropdown in the top-right of the field section. REDCap adds every variable in that instrument to the report at once. Useful for quickly adding all fields from a known instrument. Note that adding a large instrument may cause a brief slowdown as REDCap loads all variables into the list.

**+ Quick Add method**
Click the **+ Quick Add** button to open a popup listing all variables in the project, organized by instrument. Check the box next to each variable you want to add. Use the **Select all** or **Deselect all** links in each instrument header to add or remove an entire instrument's variables in one click.

**Look Up method**
Below the field list header, there is always one blank row. Clicking it opens a search box where you can type a variable name or text from its field label. REDCap filters results as you type. This method is best for adding a specific variable quickly when you know its name or label. Clicking an already-populated row in look-up mode searches for a replacement variable, removing the original — use with care.

**Dropdown method**
Click the small icon next to the look-up search box to switch it to a dropdown menu. The dropdown lists all available variables for scrolling and selection. Selecting a variable from the dropdown adds it to that row.

> **Note:** REDCap will not add the same variable to a report twice. All four methods check for duplicates automatically.

### 6.2 Reordering Variables

Variables in the report can be reordered freely regardless of the order in which they were added. Hover over the area to the left of the word "field" for any row — a drag handle (up-down arrow) will appear. Click and drag the row to its desired position.

### 6.3 Removing Variables

To remove a variable from the report, click the small red **X** at the far right of its row, or uncheck it in the Quick Add menu. Removing a variable does not delete any data — it only removes that variable from this report's display. The variable can be re-added at any time.

### 6.4 Additional Report Options

These options appear below the field list and apply to the full report. The defaults are appropriate for most use cases.

| Option | Effect |
|---|---|
| Include DAG name for each record | Adds a Data Access Group column to the report. DAGs are not stored as variables, so this is the only way to display DAG membership in a report. |
| Combine checkbox options into single column | By default, each checkbox option becomes its own column. This option merges all options into a single column showing only the checked values. Affects export output as well as the on-screen display. |
| Remove line breaks from text data | Strips carriage returns from text and notes fields. Improves readability when exporting reports as CSV files that contain multi-line free-text responses. |
| Header display | Controls whether report column headers show the field label, variable name, or both. Affects display only — does not affect exports. |
| Data display | Controls whether values appear as option labels, raw values, or both. Affects display only — does not affect exports. |

---

## 7. Common Questions

**Q: Do I need a special permission to create custom reports?**
A: Yes. You must have the **Add/Edit/Organize Reports** privilege in your user rights. Without it, you can view reports you have been granted access to, but cannot create, edit, copy, or delete them.

**Q: Can I build a report that pulls from multiple instruments?**
A: Yes. You can mix variables from any combination of instruments in a single report. Use the Quick Add method or the Look Up method to add variables from different instruments.

**Q: What does "public report" actually mean — who can see it?**
A: Anyone who has the public link can view the report, with no login required. There is no authentication barrier. Only make a report public if the data it contains is safe for unrestricted public access.

**Q: Why does adding a large instrument slow down the report builder?**
A: REDCap is loading all the variable rows into your browser's interface. The slowdown is a client-side rendering issue, not a server problem. For very large instruments, use Quick Add and select only the variables you need instead of using Choose Instrument.

**Q: If I grant a role view access to a report, will users added to that role later see the report automatically?**
A: Yes. Role and DAG selections are dynamic. Users added to the role or DAG after the report is saved gain access automatically, with no manual update needed.

**Q: A user says they can see the report but some data is missing. Why?**
A: The most likely reason is that the user's instrument-level access rights exclude some of the instruments whose variables appear in the report. Data from instruments they cannot view will not be displayed, even if the report includes those variables. Check the user's instrument access in User Rights.

**Q: Can I add the same variable to a report more than once?**
A: No. REDCap prevents duplicate variables in a report, regardless of which method you use to add them.

---

## 8. Common Mistakes & Gotchas

**Confusing report-level access with user rights.** Granting a user edit access to a report does not give them the Add/Edit/Organize Reports privilege — they still need that user right. Conversely, taking away report-level access for a user does not prevent them from seeing the report if they have broad user rights. The two systems operate in parallel.

**Making a report public before reviewing it.** REDCap requires you to have viewed the report before enabling public access, but the requirement is a checkbox confirmation, not a content review. Always open the report, review its contents, and confirm there is no sensitive data before enabling public access. The action is logged under your name.

**Using Choose Instrument on very large instruments.** Selecting a large instrument (dozens of variables) via the dropdown can cause the browser to freeze briefly. For instruments with many fields, use Quick Add with selective checking, or use the Look Up method for specific variables.

**Assuming checkbox columns match other field types.** By default, each checkbox option generates its own column in a report. A 10-option checkbox produces 10 columns. If you are building a report that includes checkboxes with many options, decide early whether to use the "Combine checkbox options" setting — it affects both the display and any CSV exports.

**Forgetting that removing a variable does not affect the data.** Newly trained users sometimes hesitate to remove a variable from a report because they fear deleting data. Removing a variable from a report only removes it from that report's view — it has no effect on the data stored in REDCap.

---

## 9. Related Articles

- RC-EXPRT-05 — Data Export: Report Types & Other Export Options (prerequisite — covers the built-in report options this article builds on)
- RC-EXPRT-07 — Custom Reports: Filtering & Ordering (next article — filters, logic builder, live filters, and result ordering)
- RC-EXPRT-08 — Custom Reports: Management & Organization (saving, copying, deleting, and organizing reports into folders)
- RC-DAG-01 — Data Access Groups (background on DAGs referenced in user access configuration)
- RC-USER-03 — User Rights: Configuring User Privileges (covers Add/Edit/Organize Reports and instrument-level access)
