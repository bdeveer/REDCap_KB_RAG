---
id: RC-DE-13
title: 'Data Entry — Record Administration: Choose Action for Record'
domain: Data Entry
applies_to:
- All project types
requires: Any supported version
verified_against: REDCap v17.4.1 (Standard) / v17.3.7 (LTS) — changelog review; page
  not re-captured. Record actions behaviour checked against source code of v17.6.5
  (Standard) / v17.3.31 and v16.0.61 (LTS)
prerequisites:
- RC-DE-01 — Record Creation & the Record Home Page
version: '1.2'
last_updated: 2026-11
related:
- id: RC-LOCK-01
  title: Record Locking & E-Signatures
- id: RC-DAG-01
  title: Data Access Groups
- id: RC-USER-03
  title: 'User Rights: Configuring User Privileges'
- id: RC-LOG-01
  title: Logging — Project Audit Trail
tags:
- data entry
synonyms:
- how do i delete a record
- lock or unlock an entire record
- rename a record id
- bulk record delete
- does deleting a record remove it from logging
- download a pdf of a record
- assign a record to a data access group
- choose action for record menu options
- record-level administrative actions
- what does the choose action button do
---

# [RC-DE-13 — Record Administration: Choose Action for Record](RC-DE-13_Record-Administration-Choose-Action-for-Record.md)

## Section 1: Overview

The **Choose action for record** button on the Record Home Page is the central control point for record-level administrative operations. From this dropdown, authorized users can download a PDF of the record or a ZIP of its uploaded files, lock or unlock the entire record, assign the record to a Data Access Group, rename it, or permanently delete it. Users with the matching page rights also see shortcut links that filter project logs, alerts and email history to the current record. This article covers every option in the menu, the user rights required to access each one, and the important limitations and consequences of destructive actions like deletion.

---

## Section 2: Key Concepts & Definitions

### Choose Action for Record
A dropdown button on the Record Home Page that exposes record-level administrative functions. It is distinct from instrument-level save options and from the data-editing actions available inside individual instruments. The button only displays actions the current user is permitted to perform; options requiring rights the user does not hold are omitted from the menu.

### Record Home Page
The page that opens when a specific record is selected. It shows the instrument-event grid (in longitudinal projects) or the instrument list (in classic projects), the completion status of each instrument, and the **Choose action for record** button. See [RC-DE-01 — Record Creation & the Record Home Page](RC-DE-01_Record-Creation-and-Record-Home-Page.md).

### Current Arm (Longitudinal Projects)
In longitudinal projects, several record-level actions — rename and delete — apply only to the arm currently being viewed. REDCap treats each arm as a semi-independent context for these operations. Navigating to a different arm and performing the same action affects that arm's data independently.

### Lock/Unlock Entire Record
A setting that prevents any user from editing any instrument in the record until the lock is removed. In a project with several arms it applies to the current arm only. This is distinct from locking an individual instrument. Locking an entire record requires the **Lock/Unlock entire records** user right. See [RC-LOCK-01 — Record Locking & E-Signatures](RC-LOCK-01_Record-Locking-and-E-Signatures.md).

### Data Access Group (DAG)
A project-level grouping that restricts which records a user can see and edit. Assigning a record to a DAG means only users in that group (and those with no DAG assignment) can access it. See [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md).

---

## Section 3: Accessing the Menu

The **Choose action for record** button is located at the top of the Record Home Page, to the right of the record identifier. It is displayed as a button with a small dropdown arrow. Clicking it opens a list of available actions.

The button is shown for every existing record, whatever the user's rights; it does not appear for a new record that has not been saved yet. Which items appear in the dropdown depends on the user's assigned rights and on which features the project uses.

### Steps to access
1. Navigate to **Add/Edit Records** in the left menu.
2. Select an existing record, or use the Record Status Dashboard to open a specific record.
3. On the Record Home Page, click the **Choose action for record** button near the top of the page.
4. Select the desired action from the dropdown.

---

## Section 4: Action Reference

The table below lists every option in the **Choose action for record** menu, the user right required, and the scope of the action.

| Action | User Right Required | Scope |
|---|---|---|
| Download PDF of record data (standard) | Data export rights | All instruments and events the user may export. Instruments set to No Access are left out and de-identified settings are applied |
| Download PDF of record data (compact) | Data export rights | Same as standard, but leaves out empty fields, unselected choices and instruments never entered |
| Download ZIP file of all uploaded documents | Data export rights; shown only if the project has file upload fields | All files uploaded to the record |
| Lock entire record | Lock/Unlock entire records | All instruments and events on the current arm |
| Assign to Data Access Group | No separate right; shown only when the project has DAGs and the user is **not** assigned to a DAG | The record's DAG assignment |
| Rename record | Rename Records | Current arm only (multi-arm projects) |
| Delete record (all forms/events) | Delete Records | All data for the current arm only |
| Survey Queue | Survey Distribution Tools; surveys enabled and the survey queue set up | Opens the record's Survey Queue page. Includes a sub-option to copy the survey queue link to the clipboard |
| Logging | Logging | Opens project Logging filtered to this record |
| Notification Log | Alerts & Notifications | Opens the Alerts & Notifications log filtered to this record |
| Email Logging | Email Logging (if enabled on your system) | Opens Email Logging filtered to this record |
| Survey Invitation Log | Survey Distribution Tools; surveys enabled | Opens Survey Invitation Log filtered to this record |
| Database Query Tool *(admin only)* | Administrator, with the Database Query Tool enabled | Opens the Database Query Tool for this record |

> **Note:** The exact menu labels vary slightly by project type and version — for example **Delete record (all forms)** in a classic project and **Delete record (all forms/events)** in a longitudinal one — and the confirmation wording varies to match.

> **Correction — these diagnostic links are privilege-gated, not admin-only.** The Logging, Notification Log, Email Logging and Survey Invitation Log entries appear for **any user holding the corresponding page privilege**, with the current record pre-selected as a filter. Only the **Database Query Tool** is restricted to system administrators. The links are separated from the standard actions by a horizontal rule in the menu.
>
> The four log links were added in **15.0.3**, integrating Luke Stevens' "Record Logging Links" External Module; **Email Logging** was extended to non-admin users with page access in **15.7.2**.

> **Survey Queue behaviour (15.0.6).** The Survey Queue option is now shown whenever surveys are enabled and the survey queue is set up in the project (and the user has Survey Distribution Tools rights), even if this record's queue is currently empty. Previously it appeared only when the queue held at least one item, which made it look as though the feature was unavailable for records that simply had nothing queued yet. The same release stopped the Survey Queue and Survey Invitation Log options appearing at all in projects where surveys are not enabled.

---

## Section 5: Action Details

### 5.1 Download PDF

Two PDF options are available:

- **Standard** — generates a PDF containing all data fields for all instruments and events, with each instrument on its own section.
- **Compact** — generates a condensed version of the same data, useful for printing or attaching to a physical chart.

Both PDFs include the current data at the moment of generation and follow the user's data export rights: instruments the user has No Access to export are left out, and de-identified or remove-identifiers settings are applied. The compact version also leaves out empty fields, unselected choices and instruments never entered. They are downloaded directly to the browser; no file is stored in the project's File Repository.

The separate **Download ZIP file of all uploaded documents** option appears when the project has file upload fields and the user has export rights; it downloads the record's uploaded files in one ZIP.

### 5.2 Lock / Unlock Entire Record

Selecting **Lock entire record** displays a confirmation dialog: *"This will lock the ENTIRE record, not just a single instrument. After doing this, no one will be able to edit this record until it is unlocked by someone with Lock/Unlock privileges."*

After confirming:
- All instruments in the record become read-only for all users.
- The lock applies to all events on the **current arm**. In a project with several arms, the record's data on other arms is not locked.
- The Record Home Page shows one large lock icon next to the record name; hover over it to see who locked the record and when. Lock icons on individual instruments in the grid show instrument-level locks, not the whole-record lock.
- A whole-record lock does **not** stop the record from being deleted by a user with **Delete Records** rights.
- Only a user with **Lock/Unlock entire records** rights can reverse it by selecting **Unlock entire record** from the same menu.

The action is logged in the project's Logging module. For e-signature functionality and instrument-level locking, see [RC-LOCK-01 — Record Locking & E-Signatures](RC-LOCK-01_Record-Locking-and-E-Signatures.md).

### 5.3 Assign to Data Access Group

This option needs no separate user right. It appears only when the project has at least one DAG and the current user is **not** assigned to a DAG; users in a DAG never see it, and REDCap blocks the change for them on the server too.

Selecting **Assign to Data Access Group** opens a dialog with a dropdown listing all DAGs defined in the project, plus an option to remove the current DAG assignment (assign to no group).

After selecting a group and confirming:
- The record becomes visible only to users assigned to that DAG and to users with no DAG assignment.
- The assignment change is logged.

For full context on how DAGs affect data access, see [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md).

### 5.4 Rename Record

Selecting **Rename record** opens a dialog pre-populated with the current record name and a text field for the new name.

Renaming requires the **Rename Records** user right.

Behavior:
- The new name must not already exist on the current arm. In a project with several arms, renaming to an ID that exists on another arm links the two, so they become the same record across arms (the case must match).
- In a project with several arms, the rename applies to the **current arm only**. The record retains its original name in other arms. The dialog displays this note: *"NOTE: This will rename the record for the current arm ONLY."*
- In a project with one arm (including all classic projects), the rename applies to the whole record.
- The new name must pass any validation set on the record ID field.
- Everything attached to the record follows the new name: survey responses, the survey queue, invitations, alerts, randomization, locks and e-signatures. Existing survey links keep working.
- The rename is logged, and REDCap also rewrites the record ID on **all earlier log entries** to the new name. The rename entry itself shows the new ID, so the old ID no longer appears anywhere in Logging. Note the old ID somewhere else if you will need it.

> **Important:** Renaming a record does not retroactively update any piped or Smart Variable references that may have captured the old name in saved data. Calculated fields and piping that reference `[record-name]` will reflect the new name on next evaluation, but previously saved text values are not updated.

For the API equivalent, see [RC-API-05 — Rename Record API](RC-API-05_Rename-Record.md).

### 5.5 Delete Record (All Forms/Events)

Selecting **Delete record (all forms/events)** opens a confirmation dialog:

> *"Are you sure you wish to PERMANENTLY delete this record and its data? This will delete ALL DATA for ALL EVENTS for ONLY THE CURRENT ARM. This process is permanent and CANNOT BE REVERSED."*

Key behaviors:
- Deletion requires the **Delete Records** user right. A whole-record lock does not block it.
- **Longitudinal projects**: deletion removes all data for all events on the **current arm only**. Data on other arms is not affected. To delete data on multiple arms, navigate to each arm and delete separately.
- **Classic projects**: deletion removes all data for all instruments (the project has one arm).
- What is removed on the current arm: the data, uploaded files (marked deleted and purged later), locks, e-signatures, calendar entries, scheduled survey invitations, survey responses, data quality statuses, alert history and recurrences, PDF archives and rewards. Some items are removed for the record in every arm, not just the current one: survey queue links, MyCap participant and messages, and Dynamic Data Pull data.
- The record ID can be reused. Auto-numbering assigns the highest numeric record ID plus one, so deleting the highest-numbered record makes that number available again; there is no counter to reset.
- **Randomized records:** deleting a randomized record frees its allocation slot, which can then be given to another record. In a project with several arms this happens only if the randomization field is on the arm being deleted. Check with your statistician before deleting randomized records.
- The deletion is logged in the project Logging module, with the username of who performed it. The delete entry records only the record ID.
- **Earlier log entries keep the record's data.** Deleting a record does not remove its earlier Logging entries, so the values that were entered stay readable to anyone with the Logging right. See *Deleting the record's logging* below.
- Deleted data **cannot be restored** through the REDCap interface. Recovery requires a database-level backup restore by a system administrator.

**Deleting the record's logging.** An administrator can turn on a per-project setting, **Delete a record's logging activity when deleting the record** (Control Center → Edit Project Settings). When it is on, the delete dialog adds a checkbox, and the user must type DELETE to confirm. REDCap then replaces the data values in that record's earlier log entries with `[*DATA REMOVED*]` and scrubs the record from the email log. This applies to the current arm only. Use it when a participant's data must be fully removed, for example after consent is withdrawn.

> **Critical:** The **Delete Records** user right is disabled by default. Grant it only temporarily for users who need to perform a deletion, then remove it. Avoid granting this right as a permanent standing permission.

A separate delete operation — **Delete all data on event** — is available as a row of X icons at the bottom of the instrument-event grid on the Record Home Page. This deletes all instrument data for a single event (or a single repeating event instance) without deleting the record itself. It is governed by the same **Delete Records** right. Unlike whole-record deletion, it refuses to delete an event that is locked or that holds randomization data.

For the API equivalent, see [RC-API-04 — Delete Records API](RC-API-04_Delete-Records.md).

### 5.6 Diagnostic Links

Below a separator, the menu includes shortcut links that each open a page filtered to the current record. Each link is shown only to users who hold the right for that page:

- **Logging** (Logging right) — the project audit trail filtered to this record ID. Shows all create, edit, delete, and export events involving this record.
- **Notification Log** (Alerts & Notifications right) — the Alerts & Notifications log filtered to this record. Shows which alerts fired, when, and to whom.
- **Email Logging** (Email Logging right, where your system has Email Logging enabled) — the email log filtered to this record. Shows automated emails sent in connection with this record (ASI invitations, alerts, etc.).
- **Survey Invitation Log** (Survey Distribution Tools right, surveys enabled) — the survey invitation log filtered to this record. Shows manual and automated invitation history.
- **Database Query Tool** (administrators only, when the tool is enabled) — opens the tool for this record's stored data. Useful for diagnosing unexpected values.

These links are for diagnostic use only and do not perform any action on the record.

---

## Section 6: Audit Trail Behavior

All record-level administrative actions performed through the **Choose action for record** menu are captured in the project's **Logging** module. Each log entry includes:

- The username of the user who performed the action
- The timestamp
- The record identifier — after a rename, earlier entries show the **new** ID, because renaming rewrites the record ID on all earlier log entries
- A description of the action performed

For deletion specifically, the log keeps an entry showing that the record was deleted. Earlier entries for the record also stay, **including the data values entered**, unless an administrator has turned on the project setting to delete a record's logging when the record is deleted (see Section 5.5). For more on the logging module, see [RC-LOG-01 — Logging — Project Audit Trail](RC-LOG-01_Logging-Project-Audit-Trail.md).

---

## Section 7: Common Questions

**Q: Can I undo a record deletion?**
No. Deletion through the Choose action for record menu is permanent and cannot be reversed through the REDCap interface. The only recovery path is a database-level restore by a system administrator from a backup taken before the deletion. Contact your REDCap administrator immediately if a deletion was made in error.

**Q: When I delete a record in a longitudinal project, does it remove all arms?**
No. Deletion removes data for the current arm only. You must navigate to each arm separately and repeat the deletion to remove data across all arms. The record identifier is not freed until data on all arms has been deleted. A few items, such as survey queue links and MyCap participant data, are removed for every arm.

**Q: Who can rename a record?**
Users with the **Rename Records** user right.

**Q: What happens to survey responses when I delete a record?**
Survey response data is stored as part of the record. Deleting the record removes all associated survey responses, including any partially completed ones. The survey participant list entry (email address, invitation status) is not deleted automatically — that must be removed separately from the Participant List if needed.

**Q: Does renaming a record in one arm affect the record's name in other arms?**
In a project with several arms, renaming applies to the current arm only. The record keeps its original name in other arms. In a project with one arm, renaming applies to the whole record.

**Q: Can I move a record from one arm to another?**
No. REDCap does not support moving a record between arms within the same project. Arm assignment is determined by how the record was created, and it cannot be changed after the fact through the interface. Moving data between arms would require deleting and recreating the record, or using the API.

**Q: Can any user see the Database Query Tool and Logging links in the menu?**
Only the Database Query Tool link is limited to administrators. The Logging, Notification Log, Email Logging and Survey Invitation Log links are shown to any user who holds the right for that page.

**Q: If I delete a record, is its data gone from Logging?**
Not by default. Earlier log entries keep the values that were entered. If the data must be fully removed, ask an administrator to turn on the project setting **Delete a record's logging activity when deleting the record**, then delete the record and tick the extra checkbox in the delete dialog.

**Q: Can I delete many records at once?**
Yes, where an administrator has enabled the **Bulk Record Delete** page. Open it from the options dropdown on the Record Status Dashboard or from **Project Setup → Other Functionality**. Deleting whole records needs **Delete Records**; deleting data on selected instruments needs Delete Records or instrument-level delete rights. The job runs in the background, and the page offers a checkbox to remove the logged data as well.

**Q: Will I lose visibility of the record if I reassign it to a DAG I'm not in?**
No. Only users who are not assigned to any DAG see the **Assign to Data Access Group** option, and those users can see records in every DAG.

---

## Section 8: Common Mistakes & Gotchas

**Deleting in the wrong arm.** In longitudinal projects, the delete operation targets the current arm. Users sometimes delete on Arm 1 intending to remove all data, then discover data on Arm 2 is still present. Verify which arm you are on before confirming a deletion, and repeat the operation for each arm if full removal is needed.

**Renaming only affects the current arm.** In projects with several arms, a renamed record has a different identifier on the renamed arm and its original identifier on all other arms. This can cause confusion in reports and exports, which may show two different IDs for what the team thinks of as a single participant. If consistent identifiers across arms matter, consider whether renaming is the right approach.

**Granting Delete Records as a permanent right.** Because deletion is irreversible, the Delete Records right should be granted only temporarily for specific deletion tasks and then removed. Projects where this right is permanently assigned to multiple users are at elevated risk of accidental data loss.

**Lock entire record vs. lock individual instruments.** Locking the entire record from this menu is an all-or-nothing action. It prevents editing of every instrument. If only one instrument needs to be locked (e.g., to freeze a baseline form while keeping follow-up forms editable), use instrument-level locking instead. See [RC-LOCK-01 — Record Locking & E-Signatures](RC-LOCK-01_Record-Locking-and-E-Signatures.md).

**Assuming the rename updates saved pipe/calculation values.** Renaming a record does not retroactively update saved text values that previously captured the old record name via piping. Fields that dynamically display `[record-name]` will update, but any text field that was saved with the old name embedded will retain the old name.

**Losing the old record ID after a rename.** Renaming rewrites the record ID on every earlier log entry, so Logging no longer shows the old ID. Record the old-to-new mapping yourself before renaming.

**Assuming deletion clears Logging.** Deleting a record leaves its earlier data readable in Logging unless the project setting to delete the record's logging is on. Locking the record does not protect it from deletion either.

**Deleting from the Record Home Page vs. the Record Status Dashboard.** The Record Home Page delete removes data for the current arm. The Record Status Dashboard does not offer a delete option for individual records. For many records, use the **Bulk Record Delete** page (if your administrator has enabled it), reached from the Record Status Dashboard options dropdown or **Project Setup → Other Functionality**, or the API.

---

## Related Articles

- [RC-DE-01 — Record Creation & the Record Home Page](RC-DE-01_Record-Creation-and-Record-Home-Page.md) *(prerequisite — covers the Record Home Page layout and context)*
- [RC-DE-02 — Basic Data Entry](RC-DE-02_Basic-Data-Entry.md)
- [RC-DE-04 — Editing Data & Audit Trail](RC-DE-04_Editing-Data-and-Audit-Trail.md)
- [RC-LOCK-01 — Record Locking & E-Signatures](RC-LOCK-01_Record-Locking-and-E-Signatures.md) *(instrument-level locking, e-signatures)*
- [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) *(DAG setup and access control)*
- [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) *(Delete Records, Lock/Unlock, and other relevant rights)*
- [RC-LOG-01 — Logging — Project Audit Trail](RC-LOG-01_Logging-Project-Audit-Trail.md) *(what the audit trail captures)*
- [RC-API-04 — Delete Records API](RC-API-04_Delete-Records.md) *(programmatic record deletion)*
- [RC-API-05 — Rename Record API](RC-API-05_Rename-Record.md) *(programmatic record renaming)*
