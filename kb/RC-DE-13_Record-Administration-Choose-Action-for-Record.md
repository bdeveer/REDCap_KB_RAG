

**Data Entry — Record Administration: Choose Action for Record**

| **Article ID** | [RC-DE-13 — Record Administration: Choose Action for Record](RC-DE-13_Record-Administration-Choose-Action-for-Record.md) |
|---|---|
| **Domain** | Data Entry |
| **Applies To** | All project types |
| **Prerequisite** | [RC-DE-01 — Record Creation & the Record Home Page](RC-DE-01_Record-Creation-and-Record-Home-Page.md) |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | [RC-LOCK-01 — Record Locking & E-Signatures](RC-LOCK-01_Record-Locking-and-E-Signatures.md); [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md); [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md); [RC-LOG-01 — Logging — Project Audit Trail](RC-LOG-01_Logging-Project-Audit-Trail.md) |
| **Synonyms** | how do i delete a record; lock or unlock an entire record; rename a record id; download a pdf of a record; assign a record to a data access group; choose action for record menu options; record-level administrative actions; what does the choose action button do |

---

## [RC-DE-13 — Record Administration: Choose Action for Record](RC-DE-13_Record-Administration-Choose-Action-for-Record.md)

### Section 1: Overview

The **Choose action for record** button on the Record Home Page is the central control point for record-level administrative operations. From this dropdown, authorized users can download a PDF of the record, lock or unlock the entire record, assign the record to a Data Access Group, rename it, or permanently delete it. Administrators also see a set of diagnostic shortcut links that filter project logs, alerts, and email history to the current record. This article covers every option in the menu, the user rights required to access each one, and the important limitations and consequences of destructive actions like deletion.

---

### Section 2: Key Concepts & Definitions

#### Choose Action for Record
A dropdown button on the Record Home Page that exposes record-level administrative functions. It is distinct from instrument-level save options and from the data-editing actions available inside individual instruments. The button only displays actions the current user is permitted to perform; options requiring rights the user does not hold are omitted from the menu.

#### Record Home Page
The page that opens when a specific record is selected. It shows the instrument-event grid (in longitudinal projects) or the instrument list (in classic projects), the completion status of each instrument, and the **Choose action for record** button. See [RC-DE-01 — Record Creation & the Record Home Page](RC-DE-01_Record-Creation-and-Record-Home-Page.md).

#### Current Arm (Longitudinal Projects)
In longitudinal projects, several record-level actions — rename and delete — apply only to the arm currently being viewed. REDCap treats each arm as a semi-independent context for these operations. Navigating to a different arm and performing the same action affects that arm's data independently.

#### Lock/Unlock Entire Record
A setting that prevents any user from editing any instrument in the record until the lock is removed. This is distinct from locking an individual instrument. Locking an entire record requires the **Lock/Unlock entire records** user right. See [RC-LOCK-01 — Record Locking & E-Signatures](RC-LOCK-01_Record-Locking-and-E-Signatures.md).

#### Data Access Group (DAG)
A project-level grouping that restricts which records a user can see and edit. Assigning a record to a DAG means only users in that group (and those with no DAG assignment) can access it. See [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md).

---

### Section 3: Accessing the Menu

The **Choose action for record** button is located at the top of the Record Home Page, to the right of the record identifier. It is displayed as a button with a small dropdown arrow. Clicking it opens a list of available actions.

The button is visible to any user who can view the Record Home Page. However, which items appear in the dropdown depends on the user's assigned rights. Users who hold none of the rights required for any action in the menu will see a reduced or empty list; the button itself may be hidden if no actions are available.

#### Steps to access
1. Navigate to **Add/Edit Records** in the left menu.
2. Select an existing record, or use the Record Status Dashboard to open a specific record.
3. On the Record Home Page, click the **Choose action for record** button near the top of the page.
4. Select the desired action from the dropdown.

---

### Section 4: Action Reference

The table below lists every option in the **Choose action for record** menu, the user right required, and the scope of the action.

| Action | User Right Required | Scope |
|---|---|---|
| Download PDF of record data (standard) | Export Data | All instruments and events in the project |
| Download PDF of record data (compact) | Export Data | All instruments and events; condensed layout |
| Lock entire record | Lock/Unlock entire records | All instruments across all events |
| Assign to Data Access Group | DAG management (or specific DAG assignment right) | The record's DAG assignment globally |
| Rename record | Create records (or Rename record right) | Current arm only (longitudinal); all arms (classic) |
| Delete record (all forms/events) | Delete records | All data for the current arm only (longitudinal) |
| Database Query Tool *(admin only)* | Super User / Admin | Opens Database Query Tool filtered to this record |
| Logging *(admin only)* | Super User / Admin | Opens project Logging filtered to this record |
| Notification Log *(admin only)* | Super User / Admin | Opens Alerts & Notifications log filtered to this record |
| Email Logging *(admin only)* | Super User / Admin | Opens Email Logging filtered to this record |
| Survey Invitation Log *(admin only)* | Super User / Admin | Opens Survey Invitation Log filtered to this record |

> **Note:** The admin diagnostic links (Database Query Tool, Logging, Notification Log, Email Logging, Survey Invitation Log) appear only for system administrators. They are separated from the standard actions by a horizontal rule in the menu.

---

### Section 5: Action Details

#### 5.1 Download PDF

Two PDF options are available:

- **Standard** — generates a PDF containing all data fields for all instruments and events, with each instrument on its own section.
- **Compact** — generates a condensed version of the same data, useful for printing or attaching to a physical chart.

Both PDFs include the current data at the moment of generation. They are downloaded directly to the browser; no file is stored in the project's File Repository. The **Export Data** user right is required.

#### 5.2 Lock / Unlock Entire Record

Selecting **Lock entire record** displays a confirmation dialog: *"This will lock the ENTIRE record, not just a single instrument. After doing this, no one will be able to edit this record until it is unlocked by someone with Lock/Unlock privileges."*

After confirming:
- All instruments in the record become read-only for all users.
- The lock applies across all events and arms.
- The lock is visible in the instrument grid as a lock icon on each instrument.
- Only a user with **Lock/Unlock entire records** rights can reverse it by selecting **Unlock entire record** from the same menu.

The action is logged in the project's Logging module. For e-signature functionality and instrument-level locking, see [RC-LOCK-01 — Record Locking & E-Signatures](RC-LOCK-01_Record-Locking-and-E-Signatures.md).

#### 5.3 Assign to Data Access Group

Selecting **Assign to Data Access Group** opens a dialog with a dropdown listing all DAGs defined in the project, plus an option to remove the current DAG assignment (assign to no group).

After selecting a group and confirming:
- The record becomes visible only to users assigned to that DAG and to users with no DAG assignment.
- If the performing user belongs to a DAG themselves, they may lose visibility of the record after assignment (if assigning to a different DAG).
- The assignment change is logged.

For full context on how DAGs affect data access, see [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md).

#### 5.4 Rename Record

Selecting **Rename record** opens a dialog pre-populated with the current record name and a text field for the new name.

Behavior:
- The new name must be unique within the project.
- In **longitudinal projects**, the rename applies to the **current arm only**. The record retains its original name in other arms. The dialog displays this note: *"NOTE: This will rename the record for the current arm ONLY."*
- In **classic projects**, the rename applies globally (there is only one arm).
- If the project uses auto-numbering, the new name must still be a valid record identifier.
- The rename is logged.

> **Important:** Renaming a record does not retroactively update any piped or Smart Variable references that may have captured the old name in saved data. Calculated fields and piping that reference `[record-name]` will reflect the new name on next evaluation, but previously saved text values are not updated.

For the API equivalent, see [RC-API-05 — Rename Record API](RC-API-05_Rename-Record.md).

#### 5.5 Delete Record (All Forms/Events)

Selecting **Delete record (all forms/events)** opens a confirmation dialog:

> *"Are you sure you wish to PERMANENTLY delete this record and its data? This will delete ALL DATA for ALL EVENTS for ONLY THE CURRENT ARM. This process is permanent and CANNOT BE REVERSED."*

Key behaviors:
- **Longitudinal projects**: deletion removes all data for all events on the **current arm only**. Data on other arms is not affected. To delete data on multiple arms, navigate to each arm and delete separately.
- **Classic projects**: deletion removes all data for all instruments (the project has one arm).
- The record identifier is freed and can be reused (if the project does not use auto-increment, or if auto-increment is reset).
- The deletion is logged in the project Logging module, creating a permanent audit entry that the record existed and was deleted, including the username of who performed the deletion.
- Deleted data **cannot be restored** through the REDCap interface. Recovery requires a database-level backup restore by a system administrator.

> **Critical:** The **Delete Records** user right is disabled by default. Grant it only temporarily for users who need to perform a deletion, then remove it. Avoid granting this right as a permanent standing permission.

A separate delete operation — **Delete all data on event** — is available as a row of X icons at the bottom of the instrument-event grid on the Record Home Page. This deletes all instrument data for a single event (or a single repeating event instance) without deleting the record itself. It is governed by the same **Delete Records** right.

For the API equivalent, see [RC-API-04 — Delete Records API](RC-API-04_Delete-Records.md).

#### 5.6 Admin Diagnostic Links

For users with system administrator access, the menu includes a separator followed by five shortcut links. Each opens a separate page pre-filtered to show information related only to the current record:

- **Database Query Tool** — queries the `redcap_data` table for this record's raw data rows. Useful for diagnosing unexpected values or confirming what was saved at the database level.
- **Logging** — the project audit trail filtered to this record ID. Shows all create, edit, delete, and export events involving this record.
- **Notification Log** — the Alerts & Notifications log filtered to this record. Shows which alerts fired, when, and to whom.
- **Email Logging** — the system email log filtered to this record. Shows all automated emails sent in connection with this record (ASI invitations, alerts, etc.).
- **Survey Invitation Log** — the survey invitation log filtered to this record. Shows manual and automated invitation history.

These links are for diagnostic use only and do not perform any action on the record.

---

### Section 6: Audit Trail Behavior

All record-level administrative actions performed through the **Choose action for record** menu are captured in the project's **Logging** module. Each log entry includes:

- The username of the user who performed the action
- The timestamp
- The record identifier (before any rename)
- A description of the action performed

For deletion specifically, the log retains a record that the entry existed and was removed, even though the data itself is gone. This provides a permanent evidence trail that satisfies audit and regulatory requirements. For more on the logging module, see [RC-LOG-01 — Logging — Project Audit Trail](RC-LOG-01_Logging-Project-Audit-Trail.md).

---

### Section 7: Common Questions

**Q: Can I undo a record deletion?**
No. Deletion through the Choose action for record menu is permanent and cannot be reversed through the REDCap interface. The only recovery path is a database-level restore by a system administrator from a backup taken before the deletion. Contact your REDCap administrator immediately if a deletion was made in error.

**Q: When I delete a record in a longitudinal project, does it remove all arms?**
No. Deletion removes data for the current arm only. You must navigate to each arm separately and repeat the deletion to remove data across all arms. The record identifier is not freed until data on all arms has been deleted.

**Q: Who can rename a record?**
Users with the **Create records** right (or a dedicated rename right, depending on REDCap version and local configuration) can rename records. Check User Rights for the project to confirm which right controls this at your institution.

**Q: What happens to survey responses when I delete a record?**
Survey response data is stored as part of the record. Deleting the record removes all associated survey responses, including any partially completed ones. The survey participant list entry (email address, invitation status) is not deleted automatically — that must be removed separately from the Participant List if needed.

**Q: Does renaming a record in one arm affect the record's name in other arms?**
In a longitudinal project, renaming applies to the current arm only. The record keeps its original name in other arms. In a classic project (no arms), renaming applies globally.

**Q: Can I move a record from one arm to another?**
No. REDCap does not support moving a record between arms within the same project. Arm assignment is determined by how the record was created, and it cannot be changed after the fact through the interface. Moving data between arms would require deleting and recreating the record, or using the API.

**Q: Can any user see the Database Query Tool and Logging links in the menu?**
No. Those diagnostic links are only visible to system administrators. Regular project users, even those with full project-level rights, do not see that section of the menu.

**Q: Will I lose visibility of the record if I reassign it to a DAG I'm not in?**
Yes. If you belong to a specific DAG and reassign the record to a different DAG, you will no longer be able to see or access the record after the page reloads. Plan DAG reassignments carefully if you need to take additional steps on the record afterward.

---

### Section 8: Common Mistakes & Gotchas

**Deleting in the wrong arm.** In longitudinal projects, the delete operation targets the current arm. Users sometimes delete on Arm 1 intending to remove all data, then discover data on Arm 2 is still present. Verify which arm you are on before confirming a deletion, and repeat the operation for each arm if full removal is needed.

**Renaming only affects the current arm.** In longitudinal projects, a renamed record has a different identifier on the renamed arm and its original identifier on all other arms. This can cause confusion in reports and exports, which may show two different IDs for what the team thinks of as a single participant. If consistent identifiers across arms matter, consider whether renaming is the right approach.

**Granting Delete Records as a permanent right.** Because deletion is irreversible, the Delete Records right should be granted only temporarily for specific deletion tasks and then removed. Projects where this right is permanently assigned to multiple users are at elevated risk of accidental data loss.

**Lock entire record vs. lock individual instruments.** Locking the entire record from this menu is an all-or-nothing action. It prevents editing of every instrument. If only one instrument needs to be locked (e.g., to freeze a baseline form while keeping follow-up forms editable), use instrument-level locking instead. See [RC-LOCK-01 — Record Locking & E-Signatures](RC-LOCK-01_Record-Locking-and-E-Signatures.md).

**Assuming the rename updates saved pipe/calculation values.** Renaming a record does not retroactively update saved text values that previously captured the old record name via piping. Fields that dynamically display `[record-name]` will update, but any text field that was saved with the old name embedded will retain the old name.

**Deleting from the Record Home Page vs. the Record Status Dashboard.** The Record Home Page delete removes data for the current arm. The Record Status Dashboard does not offer a delete option for individual records; deletion must be initiated from the Record Home Page. Bulk deletions (across many records) require the Data Quality module, a report-based workflow, or API access.

---

### Related Articles

- [RC-DE-01 — Record Creation & the Record Home Page](RC-DE-01_Record-Creation-and-Record-Home-Page.md) *(prerequisite — covers the Record Home Page layout and context)*
- [RC-DE-02 — Basic Data Entry](RC-DE-02_Basic-Data-Entry.md)
- [RC-DE-04 — Editing Data & Audit Trail](RC-DE-04_Editing-Data-and-Audit-Trail.md)
- [RC-LOCK-01 — Record Locking & E-Signatures](RC-LOCK-01_Record-Locking-and-E-Signatures.md) *(instrument-level locking, e-signatures)*
- [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) *(DAG setup and access control)*
- [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) *(Delete Records, Lock/Unlock, and other relevant rights)*
- [RC-LOG-01 — Logging — Project Audit Trail](RC-LOG-01_Logging-Project-Audit-Trail.md) *(what the audit trail captures)*
- [RC-API-04 — Delete Records API](RC-API-04_Delete-Records.md) *(programmatic record deletion)*
- [RC-API-05 — Rename Record API](RC-API-05_Rename-Record.md) *(programmatic record renaming)*
