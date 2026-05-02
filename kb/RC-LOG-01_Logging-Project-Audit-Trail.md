RC-LOG-01

**Logging — Project Audit Trail**

| **Article ID** | RC-LOG-01 |
|---|---|
| **Domain** | Logging |
| **Applies To** | All REDCap project types |
| **Prerequisite** | RC-USER-03 — User Rights: Configuring User Privileges |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-DE-04 — Editing Data & Audit Trail; RC-API-39 — Export Logging API; RC-CC-12 — Control Center: User Activity Log |

---

# 1. Overview

This article explains REDCap's project-level Logging module — the built-in audit trail that records every action taken within a project. Logging captures data changes, record creation and deletion, user access, exports, API calls, project configuration changes, and page views. It provides a tamper-evident, timestamped record that supports data integrity verification, user activity review, and regulatory compliance. This article covers how to access Logging, how to read log entries, how to use the filter and export options, and how the project-level log relates to other audit tools in REDCap.

> **Note:** Email Logging is a separate application in REDCap (also under the Applications menu) that tracks outgoing emails sent by the project. It is not the same as the audit trail Logging module covered here. See Section 8.5 for more detail.

---

# 2. Key Concepts & Definitions

### Logging Module
The project-level application in REDCap that displays a searchable, filterable history of all actions taken within a single project. Accessible from the left-hand Applications menu when the user has the Logging user right.

### Audit Trail
The complete, chronological record of project activity stored by REDCap. Every save, export, import, login, and configuration change generates at least one log entry. The audit trail cannot be edited or deleted by any project user or administrator.

### Log Entry
A single record in the audit trail. Each entry captures: the timestamp of the action, the username of the person who performed it, an action category and description, and — for data changes — the specific field and value details.

### Logging User Right
A project-level user permission that grants access to the Logging module. Users without this right do not see the Logging link in the left menu. It is separate from the field-level field history ('H' button), which is available to all users who can open an instrument.

### Data History Popup
A project-level setting (enabled under Project Setup → Additional Customizations) that adds a clock icon next to every field on every instrument. Clicking the icon opens a popup showing a chronological history of all values that field has held for that record — including the previous value, who made each change, and the timestamp. This is the per-field complement to the project-level Logging module. The Data History popup must be enabled for the File Version History feature to work. See RC-PROJ-04 — Project Setup: Additional Customizations.

### Server Timestamp
All log entries record the date and time as reported by the REDCap server, not the user's local browser time. For multi-time-zone teams, confirm the server's timezone with your administrator when reviewing time-sensitive entries.

### Page Views
A distinct event type that records every URL visited within the project by each user. Page views are **excluded from the default Logging view** and must be selected explicitly via the event type filter. They can produce a very high volume of entries.

---

# 3. Accessing the Logging Module

## 3.1 Navigation

The Logging module is accessible from the left-hand navigation menu under **Applications**. If you do not see a "Logging" link, you have not been granted the Logging user right for this project. Contact your project administrator to request access.

> **Note:** In projects where you have administrator or project design rights, Logging access is typically granted by default. For data entry accounts, it must be granted explicitly.

## 3.2 Default View

When you first open the Logging page, the display defaults to:

- **Event type**: All event types, **excluding page views**
- **Time range**: Past week

A notice at the top of the log confirms this: "By default, only the logged events from the past week are displayed." To see older data or page view entries, use the filters described in Section 5.

## 3.3 Required User Rights

The Logging user right is a single checkbox in **User Rights** (left menu → User Rights) labeled "Logging." Granting this right gives the user full read access to the project's audit trail — there is no partial or filtered access at the user-rights level.

To use the API Export Logging endpoint programmatically, the user must also have **API Export** privilege. Both rights are required; neither alone is sufficient for API access. See RC-API-39 — Export Logging API.

> **Institution-specific:** [Note any local policy about who routinely receives the Logging right — leave blank until confirmed with your REDCap support team]

---

# 4. Reading Log Entries

## 4.1 Table Columns

The log table has four columns:

| Column | Description |
|---|---|
| **Time / Date** | Timestamp in server local time (format: MM/DD/YYYY H:MMam/pm in the UI; YYYY-MM-DD HH:MM in the CSV export) |
| **Username** | REDCap username of the person who performed the action, or `[survey respondent]` for unauthenticated survey submissions, or `SYSTEM` for automated system actions |
| **Action** | Action category and description (see Section 4.2 for examples) |
| **List of Data Changes OR Fields Exported** | For data entry actions: every changed field and its new value. For exports and API calls: what was exported. For page views: the full URL visited. |

## 4.2 Action Format Examples

The Action column uses plain-language descriptions. The format varies by action type:

**Record actions (longitudinal projects):**
`Update record 1 (Baseline (Arm 1: Control))`
`Create record 1 (Screening (Arm 1: Control))`
`Update record (Auto calculation) 1 (3 Month (Arm 1: Control))`

The event name and arm are shown in parentheses for longitudinal projects. Auto-calculated field saves are logged separately with "(Auto calculation)" in the action.

**Manage/Design actions:**
`Manage/Design` — generic label for project configuration changes
`Manage/Design Modify alert` — alert creation or modification (full alert config in the data column)
`Manage/Design Copy alert` — alert duplication
`Manage/Design Create alert` — new alert created

**User management actions:**
`Add user [username]`
`(Admin only) View project as user "[username]"`
`(Admin only) Stop viewing project as user "[username]"`

**Page Views:**
`Page View` — shown in blue text; data column contains the full URL accessed

## 4.3 Data Changes Column Format

For record saves, each changed field is listed on a single line:
```
field_variable_name = 'new_value', other_field = 'new_value'
```

Checkbox fields use the notation `field_name(choice_code) = checked` or `= unchecked`.

For **repeating instrument** instances, the entry begins with `[instance = N]`:
```
[instance = 2], med_name = 'Aspirin', med_dose = '100mg'
```

For **alert modifications**, the full alert configuration is captured in the data column (all parameters, including message body, schedule settings, and recipient addresses).

> **Note:** The data column shows the **values as saved** at the time of the action, not old-vs-new comparisons. To see what a value was before an edit, use the field-level 'H' button on the data entry form. See RC-DE-04 — Editing Data & Audit Trail.

---

# 5. Filtering the Log

## 5.1 Filter Controls

All filters are displayed in a blue panel at the top of the Logging page. Every filter can be combined with others.

| Filter | Description |
|---|---|
| **Filter by event** | Dropdown — select an event type (see Section 5.2). Defaults to "All event types (excluding page views)" |
| **Filter by user** | Dropdown — lists all users who have activity in the project; includes `SYSTEM` and `[survey respondent]` |
| **Filter by record** | Dropdown — lists all record IDs in the project |
| **Filter by time range** | Date/time range with quick-select buttons (see Section 5.3) |
| **DAG filter** | Available via URL parameter (`dag`); filters by Data Access Group |

## 5.2 Event Type Options

The "Filter by event" dropdown contains these options (internal API values in parentheses):

| Dropdown Label | API logtype value |
|---|---|
| All event types (excluding page views) | *(empty string)* |
| Data export | `export` |
| Manage/Design | `manage` |
| User or role created-updated-deleted | `user` |
| Record created (only) | `record_add` |
| Record updated (only) | `record_edit` |
| Record deleted (only) | `record_delete` |
| Record locking & e-signatures | `lock_record` |
| Page Views | `page_view` |

> **Important:** Page Views are deliberately excluded from the default "all event types" view. On active projects, page view logging can generate thousands of entries. Select "Page Views" explicitly when you need to trace which pages a specific user accessed and when.

## 5.3 Time Range Quick Buttons

Below the date fields, five quick-select buttons pre-fill the time range:

- **Custom range** — clears buttons and lets you type dates manually
- **Past Day** — from 24 hours ago to now
- **Past Week** — from 7 days ago to now *(default on page load)*
- **Past Month** — from 30 days ago to now
- **Past Year** — from 365 days ago to now
- **No limit** — clears both date fields, returning all log entries

---

# 6. Exporting the Log

## 6.1 CSV Export Buttons

Three CSV export buttons appear in the upper-right corner of the Logging page:

| Button | What it exports |
|---|---|
| **All logging** | Every entry in the project's entire audit trail, regardless of current filters |
| **All pages using current filters** | All entries matching the current event type, user, record, and date filters — ignores pagination |
| **Current page** | Only the entries visible in the current page of results |

For compliance purposes, "All pages using current filters" is usually the most useful: it applies your date range and event type filter while returning all matching rows, not just the visible page.

## 6.2 CSV Column Structure

The exported CSV has five columns:

| Column | Notes |
|---|---|
| `Time / Date` | Format: `YYYY-MM-DD HH:MM` (24-hour, server time) |
| `Username` | REDCap username |
| `Action` | Action category and description (same as the UI) |
| `List of Data Changes OR Fields Exported` | Full data change or export detail text |
| `Record` | Record ID if applicable; empty for Manage/Design and user-level actions |

## 6.3 API Export

The same audit data is accessible programmatically via the Export Logging API endpoint, which supports additional filter parameters and returns JSON, CSV, or XML. See RC-API-39 — Export Logging API.

---

# 7. Using Logging for Regulatory Compliance

## 7.1 GCP and 21 CFR Part 11 Context

REDCap's audit trail is frequently cited in regulated research environments as a mechanism for meeting the audit trail requirements of:

- **ICH E6(R2) Good Clinical Practice (GCP):** Section 5.18.4(n) requires that all changes to source data be documented, and that original data and audit trails be preserved.
- **21 CFR Part 11 (FDA electronic records):** Requires computer-generated, time-stamped audit trails that record when operator entries and actions create, modify, or delete records.

REDCap's logging meets these requirements at the data capture level: every field save is recorded automatically with a timestamp and username, and the record cannot be altered. However, Part 11 compliance also involves controls outside REDCap (system validation, access control policies, training records). The audit log alone does not constitute full regulatory compliance.

## 7.2 Preparing an Audit Package

A common workflow for a formal audit or inspection:

1. Open Logging and set the event type to "Record updated (only)" and the time range to the period under review.
2. Optionally filter by record if reviewing a specific subject.
3. Export using "All pages using current filters" → CSV.
4. Repeat with "Record created (only)" and "Record deleted (only)" to capture the full record lifecycle.
5. Supplement with the record's data export showing final values (see RC-EXPRT-01 — Data Export: Overview & Workflow).
6. Document user rights in effect during the period (user additions and removals are also in the log under "User or role created-updated-deleted").

---

# 8. Relationship to Other Audit Tools in REDCap

## 8.1 Project Logging vs. Control Center User Activity Log

| Feature | Project Logging (RC-LOG-01) | CC User Activity Log (RC-CC-12) |
|---|---|---|
| **Scope** | Single project only | All projects on the REDCap instance |
| **Who can access** | Users with Logging right in the project | REDCap system administrators only |
| **Filter options** | Event type, user, record, DAG, date range | Project title, date range |
| **Use case** | Project-level audit, compliance, user activity review | Instance-wide monitoring, security investigation |
| **Access location** | Project left menu → Applications → Logging | Control Center → Dashboards & Activity → User Activity Log |

## 8.2 Project Logging vs. Data History Popup

The Data History popup (clock icon on each field) shows the complete value history for one specific field in one specific record, including the old value before each change. It requires the "Data History Popup" setting to be enabled under Project Setup → Additional Customizations (see RC-PROJ-04). No Logging user right is required to view field history — any user who can open the instrument can access it.

The Logging module, by contrast, shows all saved values across all fields and all records but does not show old-vs-new comparisons — it shows the state as saved in each transaction. Use the Data History popup when you need to see what a value was before a specific edit; use the Logging module for cross-record or cross-user investigation.

See RC-DE-04 — Editing Data & Audit Trail for more on field-level history.

## 8.3 Project Logging vs. Data Resolution Workflow Log

The Data Resolution Workflow (DRW) has its own dedicated query and response log showing the history of each data discrepancy note. That log is visible within individual records under the DRW interface and is separate from the main Logging module, although DRW actions do also appear in the project audit trail.

See RC-DE-12 — Data Resolution Workflow.

## 8.4 Project Logging vs. Field Comment Log

The Field Comment Log captures structured comments attached to individual fields. These appear in the Logging module as a logged event but are also accessible separately through the comment log interface.

See RC-DE-08 — Field Comment Log.

## 8.5 Reason for Change and the Logging Module

The **Require a Reason When Making Changes to Existing Records** setting (Project Setup → Additional Customizations) adds a prompt whenever a user saves an instrument that already contains data. The user must enter a short explanation (up to 200 characters) before the save completes.

That reason text is stored in the project's Logging and appears in the data column of the relevant log entry — alongside the field values that were changed. Reviewers can see both what changed and why in a single log entry. The prompt fires on UI saves only; data imported via the Data Import Tool or API does not trigger it.

This setting is commonly used in studies with regulatory requirements for audit trails. Enable it under Project Setup → Additional Customizations. See RC-PROJ-04 — Project Setup: Additional Customizations.

---

## 8.6 Email Logging — a Separate Application

**Email Logging** (Applications menu → Email Logging) is a distinct feature from the audit trail Logging module. It provides a searchable record of all outgoing emails sent by the project, including:

- Survey invitations (manually sent, scheduled, and Automated Survey Invitations)
- Survey notification and confirmation emails
- Alerts & Notifications
- REDCap 2-step login emails

Email Logging supports keyword search across subject, body, sender, and recipient, and includes a "Resend" option for individual messages. It does not record data changes — it is an email delivery log, not an audit trail.

---

# 9. Log Retention and Immutability

## 9.1 Entries Cannot Be Deleted

REDCap's audit trail is immutable at the project level. No project user, including users with project design rights, can delete, modify, or suppress log entries. This is a core requirement for data integrity and regulatory compliance.

> **Note:** At the system administrator level, a REDCap system admin with direct database access could theoretically alter the underlying database. In practice, this is outside normal operations and would represent a serious compliance deviation. Institutional policies typically prohibit this.

## 9.2 Retention Period

REDCap does not apply a default expiration to project-level log entries. Logs persist for the life of the project on the server.

> **Institution-specific:** [Note any local retention or archival policy for project logs — leave blank until confirmed with your REDCap support team]

---

# 10. Common Questions

**Q: I don't see "Logging" in the left menu. Why?**
You have not been granted the Logging user right for this project. Contact your project administrator. Users with project design or admin rights typically have it by default; data entry accounts usually do not.

**Q: The log only shows entries from the past week. How do I see older data?**
The default view limits results to the past week to keep the page fast. Use the time range buttons (Past Month, Past Year, No limit) or type a custom start date to expand the range. Click the "No limit" button to remove all date restrictions.

**Q: Can I see which pages a user visited?**
Yes — select "Page Views" from the event type dropdown. Each page view entry shows "Page View" in the Action column and the full URL accessed in the data column. Page views are excluded from the default "all event types" view because of their high volume.

**Q: Can I delete entries from the log?**
No. The audit trail is immutable — no project user or administrator can delete or edit log entries. To correct a data entry error, fix the field value (which creates a new log entry showing the correction) and document the circumstances per your study's SOPs.

**Q: How do I find all changes made by a specific user?**
Select the user's name from the "Filter by user" dropdown (all users with activity in the project are listed). Set a date range if needed. To narrow by type, also select "Record updated (only)" from the event type dropdown.

**Q: What does "SYSTEM" appear as the username?**
The `SYSTEM` username indicates an automated REDCap action with no specific logged-in user — typically a scheduled task or calculated field update triggered by the server rather than a human interaction.

**Q: Are API calls logged?**
Yes. Every API call is logged under the username of the account whose token was used. The action typically appears as `Manage/Design` with a description like "Export instrument-event mappings (API)" or "Upload data dictionary (API)" in the data column.

**Q: How do I export the full log for an audit?**
Use the "All pages using current filters" export button (CSV) to download all entries matching your filters. For programmatic access, use the Export Logging API — see RC-API-39 — Export Logging API.

**Q: Alert modifications appear in the log with all their settings. Why is there so much detail?**
When an alert is created or modified, REDCap logs the full configuration including schedule, recipient addresses, and message body. This ensures a complete audit trail of exactly what each alert was set up to do at any point in time. For complex alerts, this makes the log entry very long — it is by design.

---

# 11. Common Mistakes & Gotchas

**Not realizing the default view is limited to the past week.** The logging page opens showing only the last 7 days. If you are looking for an event that happened more than a week ago and see no results, check the time range — use "No limit" or "Past Year" to expand the scope before concluding the event wasn't logged.

**Looking for page views in the default view and finding none.** Page Views are deliberately excluded from the "All event types" default filter. Select "Page Views" explicitly from the event type dropdown to see them. On busy projects, page views can be very numerous — filter by user and date range before loading page view results.

**Confusing the Logging module with Email Logging.** Both appear in the Applications menu. Logging is the project audit trail (data changes, exports, user actions). Email Logging is a separate tool showing outgoing email delivery history. They are distinct pages and serve different purposes.

**Confusing the project Logging module with the Control Center User Activity Log.** The Logging module (project left menu → Applications → Logging) is project-scoped and accessible to project users with the Logging right. The Control Center User Activity Log is system-scoped and admin-only.

**Assuming the data column shows old vs. new values.** The data column shows the field values as saved in that transaction — not a before/after comparison. To see what a value was before an edit, use the 'H' button next to the field in the data entry form.

**Granting Logging rights without awareness of its scope.** The Logging right gives the user full read access to all audit entries in the project — including other users' activity, export history, and full alert configurations. Grant it deliberately and per your project's data access plan.

**Expecting deleted records to be visible in the log.** The deletion event itself is logged, but the record's data is gone. If you need the data values from a deleted record, they cannot be recovered from the audit trail — the log shows the deletion event, not the data that was deleted.

---

# 12. Related Articles

- RC-DE-04 — Editing Data & Audit Trail (field-level 'H' button; covers old vs. new value comparison)
- RC-API-39 — Export Logging API (programmatic access to the same audit trail data)
- RC-CC-12 — Control Center: User Activity Log (system-wide activity log; admin-only; distinct from project Logging)
- RC-USER-03 — User Rights: Configuring User Privileges (where the Logging right is granted)
- RC-DE-12 — Data Resolution Workflow (separate query/response log within records)
- RC-DE-08 — Field Comment Log (field-level comments, separately accessible)
- RC-LOCK-01 — Record Locking & E-Signatures *(coming soon)* (lock/unlock events selectable via "Record locking & e-signatures" event type filter)
- RC-DE-13 — Record Administration *(coming soon)* (record rename, delete, DAG move — all logged under Manage/Design)
- RC-EXPRT-01 — Data Export: Overview & Workflow (export actions are logged; relevant for compliance packages)
- RC-ALERT-01 — Alerts & Notifications: Setup (alert create/modify events appear in detail in the Logging module)
- RC-PROJ-04 — Project Setup: Additional Customizations (Data History Popup and Reason for Change settings)
