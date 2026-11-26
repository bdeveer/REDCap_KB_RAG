

**Alert Management & Notification Log**

| **Article ID** | [RC-ALERT-02 — Alert Management & Notification Log](RC-ALERT-02_Alert-Management-and-Notification-Log.md) |
|---|---|
| **Domain** | Alerts & Notifications |
| **Applies To** | All REDCap project types; requires the **Alerts & Notifications** user right |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — alert management and Notification Log behaviour checked against source code; pages not re-captured |
| **Prerequisite** | [RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md) |
| **Version** | 1.5 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md); [RC-PIPE-04 — Piping: Emails, Notifications & Logic Features](RC-PIPE-04_Piping-in-Emails-and-Notifications.md); [RC-IMP-05 — Alerts & Notifications CSV — Column Reference and Format Guide](RC-IMP-05_Alerts-Notifications-CSV.md) |
| **Synonyms** | how do i manage multiple alerts in redcap; where is the notification log; cancel a scheduled alert send; copy or deactivate an existing alert; re-evaluate alerts in redcap; queue an alert for records that already meet its logic; view history of sent alerts; edit alerts on the management page; what is a unique alert id |

---

## 1. Overview

This article covers how to manage a collection of alerts in an active REDCap project, and how to use the Notification Log to review past and scheduled alert sends. Once a project has multiple alerts, the Alerts & Notifications management page becomes the primary workspace for organizing, editing, copying, deactivating, and re-evaluating alerts. The Notification Log records every alert notification that has been sent and every notification that is scheduled to be sent, and lets you delete scheduled sends for a record. This article assumes familiarity with alert creation — see [RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md) for the full setup workflow.

Managing alerts requires the **Alerts & Notifications** user right. It is a separate right from Project Design and Setup.

---

## 2. Key Concepts & Definitions

**Alerts & Notifications Management Page**
The main page for the Alerts & Notifications feature, accessible from the project Applications menu. It serves as both the entry point for creating new alerts and the management interface for all existing alerts in the project.

**Alert Number**
The number shown after # for each alert. It reflects the alert's current position in the list, not a fixed ID, so it can change when alerts are moved or deleted. Do not use alert numbers to refer to an alert in documentation or support requests — use the Unique Alert ID.

**Unique Alert ID**
An identifier (format `A-XXXX`) that never changes for the life of the alert and is unique across the entire REDCap installation. Displayed in the alert overview on the management page and in the Notification Log. Use it whenever you need a stable reference to a specific alert, including in the alert CSV.

**Active Alert**
An alert that is enabled and will trigger and send when its conditions are met.

**Deactivated Alert**
An alert that is disabled. It will not trigger or send, but its configuration is preserved. A deactivated alert can be re-enabled at any time.

**Re-evaluate Alerts**
A project-level action that causes REDCap to check all records against one or more alert conditions. Used when alert conditions have changed after data was already entered. Re-evaluation may schedule new sends for records that now meet the trigger conditions. It removes scheduled sends for records that no longer meet them only for alerts with **Ensure logic is still true** enabled.

**Notification Log**
A project-level log of individual alert notifications — those sent successfully (past) and those scheduled (future). Unlike the management page, which shows the configuration of each alert, the Notification Log shows each individual instance of an alert being sent for a specific record. Failed sends are not listed.

**Alert Preview**
A feature on the management page that allows you to view what an alert message will look like, either with placeholder values (generic preview) or with data from a specific record (preview by record).

---

## 3. Alert Management Page

The Alerts & Notifications management page lists all alerts in the project. Each alert entry displays a summary of its configuration and provides access to editing and management actions.

### 3.1 Alert Overview Card

Each alert in the list shows:

**Alert title and number** — the number reflects the alert's current position in the list and can change; the Unique Alert ID does not. The title is user-defined. For projects with more than a handful of alerts, clear and consistent titles are essential for navigation.

**Trigger summary** — a condensed description of how the alert fires and how often it sends.

**Activity** — shows the total trigger count (the number of records for which this alert has triggered at any point). Click **View list** to see a popup with all affected record IDs. For large projects with many records, use the Notification Log instead of this popup, as the list can become unwieldy.

**Email overview** — a summary of the from address, recipients, and subject. Includes a **Preview** link with two modes:
- **Preview message** — displays the alert with generic placeholder text substituted for any piped variables. Use this when developing an alert before real records exist.
- **Preview message by record** — select a specific record from a dropdown to display the alert with that record's data. The record dropdown may not be offered in longitudinal projects or projects with a large number of records (more than about 1,000).

> **Note:** Preview always uses the alert's **current** settings and the record's **current** data. To see exactly what was sent in the past, open the message from the envelope icon in the Notification Log instead.

### 3.2 Alert Actions Menu

Each alert has an **Edit** button and an **Options** menu. The available Options depend on whether the alert is currently active or deactivated.

**Active alert options:**

| Action | Description |
|---|---|
| Copy alert | Creates a duplicate of the alert configuration. The copy is active. Use when you need multiple alerts that are similar but differ in one or two settings. |
| Deactivate alert | Disables the alert. It stops triggering and sending, but its configuration is fully preserved. It moves to the deactivated list and can be re-enabled at any time. |
| Move alert | Reorders the alert. Active and deactivated alerts share one combined order, so moving an alert changes the alert numbers of others. |

**Deactivated alert options:**

| Action | Description |
|---|---|
| Re-enable alert | Restores the alert to active status. It will begin triggering again based on its configured conditions. |
| Copy alert | Creates a duplicate. The copy is also deactivated. |
| Permanently delete | Removes the alert from the project entirely, together with its history in the Notification Log (project Logging still records the actions). This cannot be undone. If you may need the send history, export the Notification Log first. |
| Move alert | Reorders the alert within the combined list. |

> **Important:** Deactivating an alert does not delete the notifications it had already scheduled. They are hidden from the Notification Log while the alert is off, and when you re-enable it, any whose scheduled time has passed may go out within minutes. If you do not want those sent later, delete them in the Notification Log *before* you deactivate the alert. If an alert has been off for a while, check the Notification Log straight after re-enabling it and delete anything you do not want sent.

> **Note:** Scheduled notifications are built from the alert's **current** settings and the record's **current** data at the moment they send. Edits to the message, subject, recipients or attachments therefore do apply to notifications already in the queue, and changing a recurrence interval shifts the timing of future recurrences. If you change **when** notifications are sent (the send-on setting), REDCap offers to reschedule existing notifications — accept it. Otherwise notifications already scheduled under the old setting might never be sent.

Alerts also deactivate automatically when their expiration date (if set) passes. Creating, editing, copying, deactivating and deleting alerts are all recorded in project Logging.

### 3.3 Search and Filter

A **search box** at the top of the management page filters the alert list. The search matches any text visible in the alert's row — title, trigger summary, from address, recipients and subject — not just the title. It does not search message bodies.

A **Show deactivated alerts** checkbox toggles the view between active and deactivated alerts.

---

## 4. Bulk Alert Operations

### 4.1 Re-evaluate Alerts

Re-evaluating alerts causes REDCap to check all current records against the trigger conditions of one or more alerts. This is useful when an alert's conditions are modified after data collection has begun — records that were entered before the change may not have triggered the alert under the new conditions.

Re-evaluation can:
- Schedule new alert sends for records that now meet the trigger conditions.
- Remove scheduled sends for records that no longer meet the trigger conditions — **only** for alerts with **Ensure logic is still true** enabled. For other alerts, sends already scheduled stay scheduled.

Re-evaluation does **not** modify any notifications that have already been sent, and it does not send a once-only alert again to a record that already received it.

**Scope options:** You can choose to re-evaluate all active alerts in the project, or select a specific subset. For larger projects, re-evaluate one alert at a time. This is faster and avoids unintentionally triggering large numbers of alerts simultaneously.

> **Important:** Only use re-evaluation when you are certain of the intended effect across all records in the project. Re-evaluation can trigger a large number of alert sends at once, depending on how many records match the updated conditions. Sends set to go out immediately are sent right away.

**Enable Test Run** — before committing to a full re-evaluation, enable this option to preview the results without changing anything. The test run shows which records would be affected and what action would be taken, and offers a CSV of the affected records (available for about an hour).

Projects in Analysis/Cleanup or Completed status neither send alerts nor re-evaluate them.

### 4.2 Upload and Download Alerts (CSV)

Alert configurations can be exported to a CSV file and imported back into the project. This is useful for:
- Bulk-editing alert settings in a spreadsheet application.
- Copying alert configurations from one project to another.
- Mass-activating or mass-deactivating alerts.

Access this feature via the upload/download dropdown on the management page. Click the question mark icon next to the dropdown for a reference guide on the CSV format.

Upload can create and update alerts, but cannot delete or reorder them; new alerts are added at the end of the list. If the upload changes how existing alerts are scheduled, REDCap asks whether to reschedule existing notifications.

> **Note:** The alert CSV format is comprehensive. Bulk editing is a powerful feature but is also complex — treat the CSV carefully and validate changes before re-importing.

> **Note:** Any Unique Alert ID that does not belong to an alert in the target project causes an error. When importing an alert CSV taken from another project or installation, delete the Unique Alert ID values first so the rows are created as new alerts.

> **Version caveat (16.0.x LTS):** The alert CSV on 16.0.x has no column for the **Re-evaluate send time** option, which exists only on 17.x. When moving an alert CSV between a 17.x server and a 16.0.x server, start from a CSV downloaded on the target server's version where possible, and check send timing in the UI after upload.

#### CSV Column Reference

The table below covers the most commonly edited or misunderstood columns. The full column set is documented in the question mark reference on the management page.

**Create vs. update behavior:** The `alert-unique-id` column controls whether an imported row creates a new alert or updates an existing one. Leave it **empty** to create a new alert. Populate it with an existing ID (format `A-XXXX`) to overwrite that alert's configuration. When editing alerts in bulk, download the CSV first so the IDs are pre-filled — never guess or fabricate an ID.

Reusing an existing ID isn't limited to literal in-place edits — it's also the correct approach when **splitting one alert's scope into several**. For example, if an alert currently fires on either of two conditions and you want to break it into one alert per condition, narrow the original alert's `alert-condition` (and adjust its message if needed) under its existing ID, then add separate row(s) with `alert-unique-id` left blank for the condition(s) being split out into new alerts. Each of those blank-ID rows becomes its own new alert on import.

> **Important:** Some columns silently replace a value they do not recognise instead of rejecting the row — for example, an unknown `send-on` value becomes `NOW` and an unknown `alert-type` becomes `EMAIL`. After every upload, open the changed alerts in the UI and confirm the trigger, timing and type.

| Column | Valid Values / Notes |
|---|---|
| `alert-unique-id` | Empty = create new alert. `A-XXXX` (e.g., `A-2482`) = update that alert. |
| `alert-title` | Free text. Shown on the management page. |
| `alert-trigger` | `SUBMIT` = instrument save (completion trigger). `LOGIC` = logic trigger (fires when logic becomes true regardless of save source). `SUBMIT-LOGIC` = instrument save combined with logic (combination trigger). |
| `unique-form-name` | The instrument's variable name (not its display label). Required for `SUBMIT` and `SUBMIT-LOGIC` triggers. |
| `unique-event-name` | Event unique name (longitudinal projects only). Leave blank for classic projects. |
| `saved-with-form-status` | `COMPLETE` = fire only when instrument status is Complete. `ANY` = fire on any save. |
| `alert-condition` | Branching logic expression. Leave blank if no condition (completion trigger only). |
| `ensure-logic-still-true` | `Y` / `N`. Re-checks logic immediately before sending. Recommended when a time delay is set. |
| `alert-stop-type` | `RECORD` = once per record. Other options control per-event or per-instance limits. |
| `send-on` | `NOW` = immediately. `TIME_LAG` = after a defined delay. `NEXT_OCCURRENCE` = next occurrence of a day type (not `NEXT_DAY`). `DATE` = specific date/time, set in `send-on-date` (server time; check the date in the UI after upload, see [RC-IMP-05 — Alerts & Notifications CSV — Column Reference and Format Guide](RC-IMP-05_Alerts-Notifications-CSV.md)). Unknown values become `NOW`. |
| `send-on-time-lag-days` / `send-on-time-lag-hours` / `send-on-time-lag-minutes` | Numeric values defining the delay when `send-on` is `TIME_LAG`. |
| `alert-send-how-many` | `ONCE` = send a single time. `SCHEDULE` = recurring sends (requires `repeat-for`, `repeat-for-units` and `repeat-for-max`; the max counts the first send). Not `MULTIPLE`, which is rejected (observed on 17.5.10). |
| `alert-type` | `EMAIL` (standard). `SMS`, `VOICE_CALL` and `SENDGRID_TEMPLATE` if enabled on your installation. Unknown values become `EMAIL`. |
| `email-from` | Sender email address. Must be an email address of a project user; any other address is replaced with the uploading user's email. |
| `email-to` | Recipient(s). Accepts static addresses, piped variables (e.g., `[contact_email]`), or event-prefixed variables in longitudinal projects (e.g., `[baseline_arm_1][contact_email]`). |
| `prevent-piping-identifiers` | `Y` = strip identifier field values from the sent message. `N` = allow identifier piping. |
| `alert-deactivated` | `N` = active. `Y` = deactivated. |

**Pro tip — Mass alert activation after project copy or migration:** When a project is copied with its alerts, only the active alerts are copied and they arrive deactivated; From addresses that do not belong to a user of the new project are replaced. To re-enable a large number of alerts without clicking through each one individually:
1. Download the "Alerts (CSV)" file.
2. In the CSV, find the `alert-deactivated` column. Replace every `Y` with `N` for the alerts you want to activate.
3. Save the file and upload it back into the project.

---

## 5. Notification Log

The Notification Log is accessible from the Alerts & Notifications management page. It lists alert notifications sent successfully in the project and those scheduled for future delivery. Users assigned to a Data Access Group see only rows for records in their group.

> **Note:** The Notification Log covers only alerts created through the Alerts & Notifications feature. Emails scheduled by Automated Survey Invitations (ASIs) do not appear in this log.

> **Version caveat (below 17.5.1 Standard / 17.3.14 LTS):** For alerts with a **start date in the past**, the log could omit overdue one-time notifications and show recurring notifications with dates **shifted forward**. The log, not the sending, was wrong — but on affected versions do not treat the log as proof of what is scheduled.

Log rows are removed in some situations: deleting a record removes its scheduled and logged notifications, permanently deleting an alert removes its history, and erasing all project data (including when moving to production with data deletion) clears the log. Export the log first if you need to keep the history.

### 5.1 Filters

Use the filter controls at the top of the log to narrow the displayed entries. The log opens at the current time, showing upcoming notifications only — use **View past** to see what has been sent.

| Filter | Description |
|---|---|
| Displaying selector | Paginates results in groups of 100 when the log is large. |
| View past / View future buttons | Quickly switch between sends that have already occurred and those scheduled for the future. These buttons set the Begin time and End time filters. |
| Begin time | Lower bound of the time range. Leave blank to show all entries from the beginning of the project. |
| End time | Upper bound of the time range. Leave blank to show future entries over REDCap's projection window; recurring alerts show at most 100 upcoming occurrences. |
| Display alert types | Filter by a specific alert or show all alerts. Only active alerts are listed. |
| Display record | Filter by a specific record ID. For large record lists, type the record ID directly into the dropdown to jump to it rather than scrolling. |
| Apply filters | Applies all currently selected filter values to the log. |
| Reset | Returns all filters to their defaults. |

### 5.2 Notification Log Table

| Column | Description |
|---|---|
| Notification send time | The date and time an alert was sent or is scheduled to send. Uses the REDCap server's time zone, which may differ from the user's local time zone. Past rows are sends that succeeded. Future scheduled sends are **grey**, with a red ✕ icon that deletes the scheduled notification — for a recurring alert, it removes **all** future recurrences for that record, event and instance. |
| Alert | The alert number (after #) and the Unique Alert ID (in parentheses). The number can change; the ID does not. |
| View notification | An envelope icon that opens the message. For past sends it shows the message as sent; for scheduled sends the final message is built when it sends. |
| Record | The record ID associated with this alert instance. Clickable — links directly to the record's home page. In longitudinal projects, also shows the associated event and arm. |
| Recipient | The recipient(s) of this alert instance. For scheduled rows this may show the raw, un-piped setting (e.g. `[contact_email]`). |
| Subject | The subject line of the alert. For scheduled rows this may show the un-piped subject. |

> **Important:** Failed sends do not appear in the Notification Log. If an expected notification is missing from the past list, check the alert's email failure notification address (if configured) and the project **Logging** page, and contact your REDCap administrator if needed.

### 5.3 Exporting the Notification Log

Two export options are available:

- **"Entire log" button** — downloads a CSV file containing all log entries for the project, without any filters applied.
- **"All pages using current filters" button** — downloads a CSV file containing only the entries matching the active filter settings.

Both exports can be generated multiple times without restriction. Data Access Group users export only rows for their group.

> **Important:** The export contains the full message body of each notification. If your alerts pipe participant data, treat the file as potentially containing sensitive or identifying information and store it accordingly.

---

## 6. Common Questions

**Q: When I upload an alert CSV, how does REDCap know whether to create a new alert or update an existing one?**

**A:** REDCap uses the `alert-unique-id` column to decide. If that field is empty for a row, REDCap creates a new alert. If it contains the ID of an alert in this project (format `A-XXXX`), REDCap updates that alert. Any other ID causes an import error. When bulk-editing, always start by downloading the existing CSV so the IDs are pre-populated — never enter IDs manually.

**Q: How do I re-activate all my alerts after copying or migrating a project?**

**A:** Copied alerts arrive deactivated. The fastest approach is to download the alert CSV, change every `Y` to `N` in the `alert-deactivated` column for the alerts you want to activate, and re-upload the file. Avoid doing this one alert at a time if you have more than a few to reactivate. Check the From addresses after the copy, since addresses not belonging to a project user are replaced.

**Q: I edited an alert. Will notifications that were already scheduled use my changes?**

**A:** Yes, for content. Scheduled notifications are built from the alert's current settings and the record's current data when they send, so changes to the message, subject or recipients apply to them. If you changed **when** notifications are sent, accept REDCap's offer to reschedule existing notifications; otherwise already-scheduled ones might never be sent. Check the scheduled list in the Notification Log afterwards.

**Q: What is the difference between the alert Activity list and the Notification Log?**

**A:** The Activity list on the management page shows which records triggered the alert — it is a record-level summary. The Notification Log shows individual send events — it is a message-level log. For one record, a recurring alert may generate multiple entries in the Notification Log but only one entry in the Activity trigger list. Use the Notification Log when you need to see specific send times, recipients or message content.

**Q: Can I cancel a scheduled alert for just one record without affecting other records?**

**A:** Yes. In the Notification Log, filter by the relevant record ID and locate the scheduled send. Click the red ✕ icon next to the scheduled send time. For a recurring alert this removes all future recurrences for that record, event and instance, not just the one row. Scheduled sends for other records are unaffected.

**Q: An alert I expected is not in the Notification Log as sent. What should I do?**

**A:** Failed sends are not listed in the log. Check the email failure notification address configured in the alert setup (if any) for an error message, and review the project **Logging** page. Common causes include an invalid or blank recipient address, a recipient domain blocked by the server, or attachment size limits. Also confirm the alert was active, its logic was true, and the project was not in Analysis/Cleanup or Completed status. Contact your REDCap administrator if the cause is unclear.

**Q: The Activity "View list" popup shows too many records to be useful. What should I use instead?**

**A:** Use the Notification Log with the Display alert types filter set to that specific alert. The log provides a more structured and exportable view of all sends for that alert across all records.

**Q: Why did the alert numbers change?**

**A:** Alert numbers are list positions. Moving or deleting an alert renumbers the others. Use the Unique Alert ID (`A-XXXX`) when you need to identify an alert reliably.

---

## 7. Common Mistakes & Gotchas

**Permanently deleting an alert instead of deactivating it.** Permanent deletion removes the alert, all its configuration and its Notification Log history. If you think you might need the alert again — even after a study phase ends — deactivate it instead. Deactivated alerts are preserved indefinitely and can be re-enabled at any time. If you do delete, export the Notification Log first if the send history matters.

**Re-enabling an alert without thinking about its queue.** Notifications scheduled before the alert was deactivated are kept, and any whose time passed while it was off may go out within minutes of re-enabling. Delete unwanted scheduled notifications in the Notification Log before deactivating the alert; they are not visible there while it is off.

**Changing the send timing without rescheduling.** If you change when an alert sends and decline the offer to reschedule existing notifications, already-scheduled notifications might never be sent.

**Re-evaluating all alerts at once in a large project.** Re-evaluating all active alerts simultaneously in a project with many records and many alerts can trigger an unexpectedly large number of email sends. Always use the Test Run option first to preview the effect, and consider re-evaluating one alert at a time to control the outcome.

**Expecting re-evaluation to cancel sends for every alert.** Re-evaluation removes scheduled sends that no longer match only for alerts with **Ensure logic is still true** enabled. For other alerts, delete unwanted scheduled sends in the Notification Log.

**Forgetting to remove Unique Alert IDs when importing a CSV from another project.** If you export an alert CSV from one project and import it into another, the Unique Alert IDs belong to the source project. Importing with those IDs will generate an error. Always clear the unique ID column before importing across projects.

**Trusting an uploaded CSV without checking.** Unrecognised values in some columns are silently replaced (for example, an unknown `send-on` value becomes `NOW`). Review the changed alerts in the UI after every upload.

**Assuming the Notification Log covers ASI emails.** Automated Survey Invitation emails do not appear in the Notification Log. If you are looking for a sent survey invitation and it was configured as an ASI rather than an alert, check the ASI's own send log, not the Notification Log.

**Treating the Notification Log as a record of failures.** Only successful sends appear as past rows. Use the failure notification email and project Logging to investigate missing sends.

**Switching on an alert and expecting it to queue sends for existing records.** Logic is checked when a record is saved or imported, not when an alert is activated. For records that already meet the logic, save or import them after activating the alert, or run **Re-evaluate Alerts** (Section 4.1) with Test Run first.

**Referring to alerts by number.** Alert numbers change when alerts are moved or deleted. Use the Unique Alert ID in notes, documentation and support requests.

---

## 8. Related Articles

- [RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md) (required prerequisite — trigger types, scheduling, message settings)
- [RC-PIPE-04 — Piping: Emails, Notifications & Logic Features](RC-PIPE-04_Piping-in-Emails-and-Notifications.md) (piping and smart variable usage in alert messages)
- [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md) (reference for smart variables used in alert message bodies)
- [RC-LONG-02 — Repeated Instruments & Events Setup](RC-LONG-02_Repeated-Instruments-and-Events-Setup.md) (context for trigger limits and repeated-instrument alert behavior)
- [RC-IMP-05 — Alerts & Notifications CSV — Column Reference and Format Guide](RC-IMP-05_Alerts-Notifications-CSV.md) (full column reference for the alerts CSV upload)
