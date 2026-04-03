RC-DE-08

**Data Entry — Field Comment Log**

| **Article ID** | RC-DE-08 |
|---|---|
| **Domain** | Data Entry |
| **Applies To** | All REDCap project types; data entry users with appropriate access |
| **Prerequisite** | RC-DE-02 — Basic Data Entry |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-DE-02 — Basic Data Entry; RC-DE-04 — Editing Data & Audit Trail |

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

The application allows you to:

- Filter comments by instrument, record, variable, or user
- Search the text of comments for specific keywords
- View a list of all matching comment entries

Each row in the results list displays the record, the instrument, the variable, the comment text, the author, and the timestamp.

### 6.3 Navigating from the Log to a Record

From the field comment log application, each result row includes a clickable record ID under the "Record" column. Clicking the record ID navigates directly to the corresponding instrument within that record, where you can review the variable in context, add a new comment, or correct the data entry.

Clicking the **X comment** button (where X is the number of comments on that variable) opens the comment popup for that variable, allowing you to read existing comments or add a new one without navigating away from the log.

---

# 7. Common Questions

**Q: Does adding a comment change the value stored in the dataset?**

**A:** No. Comments are stored in a separate system from the data values. Adding, editing, or reviewing a comment has no effect on the variable's value in the dataset or in any export.

**Q: Can I delete or edit a comment after saving it?**

**A:** Standard user accounts cannot edit or delete existing comments — they are permanent once saved. Project administrators may have additional options. Comments are timestamped and attributed, making them part of the audit record for the project.

**Q: I cannot see any comment balloons in my instrument. Why?**

**A:** The most likely reasons are: (1) the field comment log feature has been disabled for this project by an administrator, (2) the variable is embedded within the instrument (see RC-FD-07 — Field Embedding), or (3) you are viewing the instrument in survey mode rather than data entry mode.

**Q: Who can see the comments I add?**

**A:** Any REDCap user with data entry access to the instrument can see comments on its variables. Comments are not private. Coordinate with your project manager if your team needs guidance on appropriate comment content.

**Q: Is there a way to search for comments about a specific issue across all records?**

**A:** Yes. The Field Comment Log application includes a keyword search that scans comment text across all records and instruments. Navigate to the application from the project menu and use the search field to find comments containing specific words or phrases.

**Q: Can I add a comment to a variable in a record I didn't create?**

**A:** Yes, provided you have data entry access to the relevant instrument. The comment will be attributed to your user account with a timestamp. You do not need to be the creator of the record.

---

# 8. Common Mistakes & Gotchas

**Assuming comments affect the dataset.** Comments are entirely separate from data values. A comment documenting a missing value does not count as an entry — the field is still blank in the dataset and exports. Take care that downstream data cleaning processes account for the distinction between "blank with a comment" and "blank without a comment."

**Expecting comments to be visible in survey mode.** If a participant is completing an instrument as a survey, they will not see staff comments and cannot add their own. Likewise, staff reviewing survey responses after submission may find the comment balloon missing for certain embedded or survey-specific fields.

**Not establishing team commenting standards before data collection.** If some team members use comments extensively and others never do, the field comment log becomes an unreliable data quality signal. Agree on when and how comments should be used at the project kickoff.

**Forgetting that comments are permanent.** Comments cannot be deleted by standard users. Avoid including sensitive information, speculation, or preliminary conclusions in comments — they form part of the permanent project record.

---

# 9. Related Articles

- RC-DE-02 — Basic Data Entry (foundational data entry skills)
- RC-DE-04 — Editing Data & Audit Trail (related audit and annotation features)
- RC-DE-05 — Field Validations (the field comment log is often used in conjunction with validation errors to document data issues)
- RC-FD-07 — Field Embedding (explains why embedded variables may lack a comment balloon)
