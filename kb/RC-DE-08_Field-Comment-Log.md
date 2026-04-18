RC-DE-08

**Data Entry — Field Comment Log**

| **Article ID** | RC-DE-08 |
|---|---|
| **Domain** | Data Entry |
| **Applies To** | All REDCap project types; data entry users with appropriate access |
| **Prerequisite** | RC-DE-02 — Basic Data Entry |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-DE-02 — Basic Data Entry; RC-DE-04 — Editing Data & Audit Trail; RC-DE-12 — Data Resolution Workflow; RC-CC-02 — Control Center: General System Configuration |

---

# 1. Overview

This article explains REDCap's field comment log — what it is, when to use it, and how to add and review comments. The field comment log lets data entry users attach notes to individual variables within an instrument without modifying the stored data value. It is primarily a data quality tool: it allows teams to track questions, flag uncertain entries, and document data issues directly within REDCap rather than in external spreadsheets or emails. Use of the field comment log is optional unless required by your study protocol.

---

# 2. Key Concepts & Definitions

**Field Comment Log**

A per-variable annotation system in REDCap that allows data entry users to leave timestamped, attributed comments on any variable in an instrument. Comments are stored separately from the data and do not alter the variable's value in the dataset.

**Comment Balloon**

A small icon (depicted as a speech bubble or text balloon) displayed next to each variable in an instrument. Clicking the balloon opens the comment entry interface for that variable. A grey balloon indicates no existing comments; a yellow balloon indicates one or more comments have already been recorded.

**Field Comment Log Application**

A dedicated module accessible from the project menu that displays all comments across all instruments and records in a project. It provides filtering and search capabilities for data quality review.

---

# 3. When to Use the Field Comment Log

The field comment log is the appropriate place to document a data quality concern without leaving the variable blank or entering a potentially incorrect value. Common use cases include:

**Missing data.** You are transcribing a paper form and a value is absent. Note that the field was blank on the source document.

**Uncertain or illegible data.** A handwritten paper form has a smudged or ambiguous entry that needs verification before it can be recorded accurately.

**Incomplete data.** A participant recalls a relevant fact but cannot provide the precise value required by the validation (e.g., they know they quit smoking but cannot recall the exact date).

**Protocol-mandated annotation.** Some study protocols require data entry staff to comment on specific types of entries (e.g., imputed values, estimated dates). Check your protocol documentation for any such requirements.

> **Note:** The field comment log is optional except where mandated by protocol. Agree on commenting standards with your study team before data collection begins — inconsistent use makes the log harder to interpret during data review.

---

# 4. Adding a Comment

### 4.1 Locating the Comment Balloon

Every variable in an instrument displays a small comment balloon icon next to it. The color of the balloon tells you its status:

- **Grey balloon** — no comments have been recorded for this variable in this record
- **Yellow balloon** — one or more comments already exist; clicking will open the existing comments and allow you to add another

### 4.2 Opening the Comment Interface

Click the balloon icon next to the variable you want to comment on. A popup or panel opens showing the comment history for that variable in the current record.

### 4.3 Entering and Saving a Comment

Type your comment in the comment box. When finished, click the **Comment** button to save. Your comment is recorded with your REDCap username and a timestamp. It is immediately visible to any other user with access to that instrument.

You can add multiple comments to the same variable. Each is stored as a separate entry with its own timestamp and author attribution.

---

# 5. When the Comment Balloon Is Not Available

The field comment balloon is not displayed in the following situations:

**Feature disabled for the project.** If the project administrator has turned off the field comment log, no balloons will appear anywhere in the project and the field comment log application will not be accessible.

**Embedded variables.** Variables that have been embedded into the body of an instrument (using the field embedding feature) typically lose the balloon because the UI element that hosts the balloon is not rendered in the embedded context. See RC-FD-07 — Field Embedding.

**Survey mode.** When an instrument is presented as a participant-facing survey, the field comment feature is not available. Comments can only be added when the instrument is accessed by a staff user in data entry mode.

---

# 6. Reviewing Comments

### 6.1 Navigating Back to an Instrument

You can return to any instrument in any record at any time to review comments on individual variables. The balloon color indicates whether comments are present.

### 6.2 Using the Field Comment Log Application

For a cross-record, cross-instrument overview of all comments, use the **Field Comment Log** application in the project menu. This is the most efficient way to conduct a data quality review across the entire dataset.

Each row in the results list displays the record, the instrument, the variable, the comment text, the author, and the timestamp.

### 6.3 Filtering Comments

The Field Comment Log application supports multiple filters that can be combined to narrow results. Filters do not apply automatically — click **Apply filters** after making your selections. Use the **Reset** link to return all filters to their defaults.

| Filter | Description |
|---|---|
| Records | Filter to a single record. The list is populated from all existing records in the project, even those without comments. |
| Events | Filter to a specific event (longitudinal projects only; one event at a time). |
| Fields | Filter to a specific variable — for example, to see all comments attached to the Date of Birth variable across all records. |
| Users | Filter to comments made by a specific user. |
| Data Access Group | Filter to comments from a specific DAG. Useful for site-by-site data quality review in multi-site projects. |
| Keyword | Search the text of comments for one or more words. Multiple keywords can be entered, separated by a space — REDCap will return comments containing any of the entered terms. Supports partial-word matches. |

### 6.4 Replying Directly from the Log

Each row in the comment log includes a **Comment** button. Clicking it opens the comment popup for that variable directly within the log, without navigating to the record. This allows you to respond to comments across multiple records efficiently without opening each record individually.

### 6.5 Navigating from the Log to a Record

Each result row includes a clickable link in the record column. Clicking it opens a new browser tab, navigates directly to the relevant instrument within that record, and jumps to the variable with the comment. This is useful when you need to review or correct the data entry in context.

### 6.6 Exporting the Comment Log

Click **Export the entire log** from the Field Comment Log application to download a CSV file of all comments accessible to your user account. The export includes the comment author, timestamp, and variable identification. For longitudinal and repeated-instruments projects, the export also includes event and instance information.

---

# 7. Enabling and Configuring the Field Comment Log

### 7.1 Enabling the Feature

The Field Comment Log is enabled by default for most REDCap projects. To confirm or change the active mode:

1. Navigate to the **Project Setup** page.
2. Scroll down to **Enable optional modules and customizations**.
3. Click **Additional customizations**.
4. Scroll to the section labeled **Enable the Field Comment Log or Data Resolution Workflow (Data Queries)?**
5. Confirm **Field Comment Log** is selected, or select it if another mode is active.
6. Click **Save**.

REDCap projects support three modes: Field Comment Log, Data Resolution Workflow, and None. Only one mode can be active at a time. For more on the differences between modes and guidance on when to use DRW instead of the Field Comment Log, see RC-DE-12 — Data Resolution Workflow.

### 7.2 Enabling Comment Editing and Deletion

By default, comments cannot be edited or deleted after they are saved. To allow users to modify comments:

1. Follow steps 1–4 above to open the Additional customizations panel.
2. Locate the **Field Comment Log** settings section.
3. Check the box to enable editing and deletion.
4. Click **Save**.

When enabled, a pencil (edit) icon and a red X (delete) icon appear next to each comment in the popup. These actions are auditable — both edits and deletions are recorded in the project log.

---

# 8. Common Questions

**Q: Does adding a comment change the value stored in the dataset?**

**A:** No. Comments are stored in a separate system from the data values. Adding, editing, or reviewing a comment has no effect on the variable's value in the dataset or in any export.

**Q: Can I delete or edit a comment after saving it?**

**A:** This depends on a project-level setting. By default, comments are permanent once saved. A project administrator can enable the ability to edit and delete comments in **Project Setup → Additional customizations**. When enabled, an edit (pencil) icon and a delete (red X) icon appear next to each comment in the popup. Note that editing or deleting a comment is recorded in the overall project log — these actions are auditable even when permitted.

**Q: I cannot see any comment balloons in my instrument. Why?**

**A:** The most likely reasons are: (1) the field comment log feature has been disabled for this project by an administrator, (2) the variable is embedded within the instrument (see RC-FD-07 — Field Embedding), or (3) you are viewing the instrument in survey mode rather than data entry mode.

**Q: Who can see the comments I add?**

**A:** Any REDCap user with data entry access to the instrument can see comments on its variables. Comments are not private. Coordinate with your project manager if your team needs guidance on appropriate comment content.

**Q: Is there a way to search for comments about a specific issue across all records?**

**A:** Yes. The Field Comment Log application includes a keyword search that scans comment text across all records and instruments. Navigate to the application from the project menu and use the search field to find comments containing specific words or phrases.

**Q: Can I add a comment to a variable in a record I didn't create?**

**A:** Yes, provided you have data entry access to the relevant instrument. The comment will be attributed to your user account with a timestamp. You do not need to be the creator of the record.

---

# 9. Common Mistakes & Gotchas

**Assuming comments affect the dataset.** Comments are entirely separate from data values. A comment documenting a missing value does not count as an entry — the field is still blank in the dataset and exports. Take care that downstream data cleaning processes account for the distinction between "blank with a comment" and "blank without a comment."

**Expecting comments to be visible in survey mode.** If a participant is completing an instrument as a survey, they will not see staff comments and cannot add their own. Likewise, staff reviewing survey responses after submission may find the comment balloon missing for certain embedded or survey-specific fields.

**Not establishing team commenting standards before data collection.** If some team members use comments extensively and others never do, the field comment log becomes an unreliable data quality signal. Agree on when and how comments should be used at the project kickoff.

**Assuming comments are always permanent — or always editable.** By default, comments cannot be edited or deleted by any user. A project-level setting can enable this ability. Regardless of whether editing is enabled, always treat comments as part of the project's audit record: avoid including sensitive information, speculation, or preliminary conclusions. If your project does allow editing, be aware that edits and deletions are logged in the project log and are not truly erased from the audit trail.

---

# 10. Administrator Configuration

The Field Comment Log is available in all REDCap projects but has a system-level default setting that affects new projects. Administrators can configure whether the Field Comment Log is **enabled by default** for all newly created projects in the Control Center under System Configuration → General Configuration (see **RC-CC-02**, "Field Comment Log Default" setting).

When set to enabled by default, every new project starts with the Field Comment Log active. Project administrators can change this per project from Project Setup → Additional Customizations.

The Field Comment Log and the Data Resolution Workflow (RC-DE-12) are mutually exclusive — a project runs in one mode at a time. The system-level default affects which mode new projects start in, but the mode can always be changed at the project level.

> **See also:** RC-CC-02 — Control Center: General System Configuration

---

# 11. Related Articles

- RC-DE-02 — Basic Data Entry (foundational data entry skills)
- RC-DE-04 — Editing Data & Audit Trail (related audit and annotation features)
- RC-DE-05 — Field Validations (the field comment log is often used in conjunction with validation errors to document data issues)
- RC-DE-12 — Data Resolution Workflow (the structured alternative to the Field Comment Log, with query tracking, assignment, and resolution metrics)
- RC-FD-07 — Field Embedding (explains why embedded variables may lack a comment balloon)
- RC-CC-02 — Control Center: General System Configuration (system-level Field Comment Log default for new projects)
