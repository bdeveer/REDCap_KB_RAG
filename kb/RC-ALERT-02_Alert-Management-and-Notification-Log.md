RC-ALERT-02

**Alert Management & Notification Log**

| **Article ID** | RC-ALERT-02 |
| --- | --- |
| **Domain** | Alerts & Notifications |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Prerequisite** | RC-ALERT-01 — Alerts & Notifications: Setup |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-ALERT-01 — Alerts & Notifications: Setup; RC-PIPE-04 — Piping: Emails, Notifications & Logic Features |

---

# 1. Overview

This article covers how to manage a collection of alerts in an active REDCap project, and how to use the Notification Log to review past and scheduled alert sends. Once a project has multiple alerts, the Alerts & Notifications management page becomes the primary workspace for organizing, editing, copying, deactivating, and re-evaluating alerts. The Notification Log provides a record of every alert instance that has been sent or is scheduled to be sent, and allows you to cancel individual scheduled sends. This article assumes familiarity with alert creation — see RC-ALERT-01 — Alerts & Notifications: Setup for the full setup workflow.

---

# 2. Key Concepts & Definitions

**Alerts & Notifications Management Page**
The main page for the Alerts & Notifications feature, accessible from the project Applications menu. It serves as both the entry point for creating new alerts and the management interface for all existing alerts in the project.

**Alert Number**
A sequential integer assigned to each alert in the order it was created within the project. Alert numbers are project-specific and are not unique across REDCap installations.

**Unique Alert ID**
A numeric identifier that is globally unique across the entire REDCap installation. Displayed in the alert overview on the management page, primarily used by REDCap administrators for system-level troubleshooting.

**Active Alert**
An alert that is enabled and will trigger and send when its conditions are met.

**Deactivated Alert**
An alert that is disabled. It will not trigger or send, but its configuration is preserved. A deactivated alert can be re-enabled at any time.

**Re-evaluate Alerts**
A project-level action that causes REDCap to check all records against one or more alert conditions. Used when alert conditions have changed after data was already entered. Re-evaluation may schedule new sends for records that now meet the trigger conditions, or cancel scheduled sends for records that no longer do.

**Notification Log**
A project-level log of all individual alert send events — both completed (past) and scheduled (future). Unlike the management page, which shows the configuration of each alert, the Notification Log shows each individual instance of an alert being sent to a specific recipient for a specific record.

**Alert Preview**
A feature on the management page that allows you to view what an alert message will look like, either with placeholder values (generic preview) or with data from a specific record (preview by record).

---

# 3. Alert Management Page

The Alerts & Notifications management page lists all alerts in the project. Each alert entry displays a summary of its configuration and provides access to editing and management actions.

## 3.1 Alert Overview Card

Each alert in the list shows:

**Alert title and number** — the alert number reflects creation order within the project. The title is user-defined. For projects with more than a handful of alerts, clear and consistent titles are essential for navigation.

**Trigger summary** — a condensed description of how the alert fires and how often it sends.

**Activity** — shows the total trigger count (the number of records for which this alert has triggered at any point). Click **View list** to see a popup with all affected record IDs. For large projects with many records, use the Notification Log instead of this popup, as the list can become unwieldy.

**Email overview** — a summary of the from address, recipients, and subject. Includes a **Preview** link with two modes:
- **Preview message** — displays the alert with generic placeholder text substituted for any piped variables. Use this when developing an alert before real records exist.
- **Preview message by record** — select a specific record from a dropdown to display the alert with that record's actual data. Use this to verify what was sent to a specific participant, or to spot-check a fully-configured alert.

## 3.2 Alert Actions Menu

Each alert has an **Edit** button and an **Options** menu. The available Options depend on whether the alert is currently active or deactivated.

**Active alert options:**

| Action | Description |
|---|---|
| Copy alert | Creates a duplicate of the alert configuration. The copy is active. Use when you need multiple alerts that are similar but differ in one or two settings. |
| Deactivate alert | Disables the alert. It stops triggering and sending, but its configuration is fully preserved. It moves to the deactivated list and can be re-enabled at any time. |
| Move alert | Reorders the alert within the management page list. Useful for organizing a large set of alerts into a logical sequence. |

**Deactivated alert options:**

| Action | Description |
|---|---|
| Re-enable alert | Restores the alert to active status. It will begin triggering again immediately based on its configured conditions. |
| Copy alert | Creates a duplicate. The copy is also deactivated. |
| Permanently delete | Removes the alert from the project entirely. This action cannot be undone. If the alert is needed again in the future, it must be recreated from scratch. |
| Move alert | Reorders the alert within the deactivated list. |

> **Note:** Edits made to an alert's configuration apply only to future trigger events. Alert instances that are already scheduled are not retroactively updated — they will send with the configuration that was in effect when they were queued.

## 3.3 Search and Filter

A **search box** at the top of the management page filters the alert list. The search applies to alert titles only — it does not search within alert message bodies or trigger logic.

A **Show deactivated alerts** checkbox toggles the view between active and deactivated alerts.

---

# 4. Bulk Alert Operations

## 4.1 Re-evaluate Alerts

Re-evaluating alerts causes REDCap to check all current records against the trigger conditions of one or more alerts. This is useful when an alert's conditions are modified after data collection has begun — records that were entered before the change may not have triggered the alert under the new conditions.

Re-evaluation can:
- Schedule new alert sends for records that now meet the trigger conditions.
- Cancel scheduled sends for records that no longer meet the trigger conditions.

Re-evaluation does **not** modify any alert instances that have already been sent.

**Scope options:** You can choose to re-evaluate all active alerts in the project, or select a specific subset. For larger projects, re-evaluate one alert at a time. This is faster and avoids unintentionally triggering large numbers of alerts simultaneously.

> **Important:** Only use re-evaluation when you are certain of the intended effect across all records in the project. Re-evaluation can trigger a large number of alert sends at once, depending on how many records match the updated conditions.

**Enable Test Run** — before committing to a full re-evaluation, enable this option to preview the results without actually queuing any sends. The test run shows which records would be affected and what action would be taken, allowing you to verify the outcome before proceeding.

## 4.2 Upload and Download Alerts (CSV)

Alert configurations can be exported to a CSV file and imported back into the project. This is useful for:
- Bulk-editing alert settings in a spreadsheet application.
- Copying alert configurations from one project to another.
- Mass-activating or mass-deactivating alerts.

Access this feature via the upload/download dropdown on the management page. Click the question mark icon next to the dropdown for a reference guide on the CSV format.

> **Note:** The alert CSV format is comprehensive. Bulk editing is a powerful feature but is also complex — treat the CSV carefully and validate changes before re-importing.

> **Note:** If you import an alert CSV from a different REDCap installation or a copied project, delete the Unique Alert ID values from the CSV before uploading. Importing with existing unique IDs from another installation will cause an error.

**Pro tip — Mass alert activation after project migration:** When a project is copied or migrated, all alerts are deactivated by default. To re-enable a large number of alerts without clicking through each one individually:
1. Download the "Alerts (CSV)" file.
2. In the CSV, find the `alert-deactivated` column. Replace every `Y` with `N` for the alerts you want to activate.
3. Save the file and upload it back into the project.

---

# 5. Notification Log

The Notification Log is accessible from the Alerts & Notifications management page. It provides a complete record of every alert instance in the project — both those already sent and those scheduled for future delivery.

> **Note:** The Notification Log covers only alerts created through the Alerts & Notifications feature. Emails scheduled by Automated Survey Invitations (ASIs) do not appear in this log.

## 5.1 Filters

Use the filter controls at the top of the log to narrow the displayed entries:

| Filter | Description |
|---|---|
| Displaying selector | Paginates results in groups of 100 when the log is large. |
| View past / View future buttons | Quickly switch between sends that have already occurred and those scheduled for the future. These buttons set the Begin time and End time filters. |
| Begin time | Lower bound of the time range. Leave blank to show all entries from the beginning of the project. |
| End time | Upper bound of the time range. Leave blank to show all entries through the indefinite future. |
| Display alert types | Filter by a specific alert (by alert number) or show all alerts. |
| Display record | Filter by a specific record ID. For large record lists, type the record ID directly into the dropdown to jump to it rather than scrolling. |
| Apply filters | Applies all currently selected filter values to the log. |
| Reset | Returns all filters to their defaults. |

## 5.2 Notification Log Table

| Column | Description |
|---|---|
| Notification send time | The exact date and time an alert was sent or is scheduled to send. Uses the REDCap server's time zone, which may differ from the user's local time zone. Past sends are colored **green** (successful) or **red** (failed). Future scheduled sends are **grey**, with a red ✕ icon that allows you to cancel that individual scheduled instance. |
| Alert | The alert number (after #) and the unique alert ID (in parentheses). |
| View notification | An envelope icon that opens the full alert message as it was (or will be) sent, including any piped data resolved at send time. |
| Record | The record ID associated with this alert instance. Clickable — links directly to the record's home page. In longitudinal projects, also shows the associated event and arm. |
| Recipient | The email address(es) to which this alert instance was or will be sent. |
| Subject | The subject line of the alert. |

## 5.3 Exporting the Notification Log

Two export options are available:

- **"Entire log" button** — generates an Excel file containing all log entries for the project, without any filters applied.
- **"All pages using current filters" button** — generates an Excel file containing only the entries currently displayed based on active filter settings.

Both exports can be generated multiple times without restriction.

---

# 6. Common Questions

**Q: How do I re-activate all my alerts after copying or migrating a project?**

**A:** All alerts are deactivated by default when a project is copied. The fastest approach is to download the alert CSV, change every `Y` to `N` in the `alert-deactivated` column for the alerts you want to activate, and re-upload the file. Avoid doing this one alert at a time if you have more than a few to reactivate.

**Q: I edited an alert, but participants who were already scheduled to receive it are still getting the old version. Is this expected?**

**A:** Yes. Alert edits apply only to future trigger events. Any alert instances that were queued before you made the edit will send with the original configuration. To apply updated settings to already-scheduled instances, you would need to manually cancel them in the Notification Log and allow the alert to re-trigger, or use Re-evaluate Alerts if appropriate.

**Q: What is the difference between the alert Activity list and the Notification Log?**

**A:** The Activity list on the management page shows which records triggered the alert — it is a record-level summary. The Notification Log shows individual send events — it is a message-level log. For one record, a recurring alert may generate multiple entries in the Notification Log but only one entry in the Activity trigger list. Use the Notification Log when you need to see specific send times, recipients, message content, or delivery status.

**Q: Can I cancel a scheduled alert for just one record without affecting other records?**

**A:** Yes. In the Notification Log, filter by the relevant record ID and locate the scheduled instance. Click the red ✕ icon next to the scheduled send time to cancel that instance only. Other scheduled instances for different records are unaffected.

**Q: The Notification Log shows a send as red (failed). What should I do?**

**A:** A red entry means REDCap attempted to send the alert but encountered an error. Common causes include an invalid recipient email address, a recipient email domain blocked by the server, or attachment size limits exceeded. Review the from and to addresses in the alert configuration, confirm that the recipient address is valid, and check with your REDCap administrator if the issue persists. If you configured an email failure notification address in the alert setup, that address should have received an error notification as well.

**Q: The Activity "View list" popup shows too many records to be useful. What should I use instead?**

**A:** Use the Notification Log with the Display alert types filter set to that specific alert. The log provides a more structured and exportable view of all sends for that alert across all records.

**Q: How do I tell whether a future scheduled send will use updated alert settings or the original ones?**

**A:** Alert instances are queued with the configuration at the time the trigger fired. If you edited the alert after the instance was queued, the queued instance retains the old settings. To force the updated settings, cancel the queued instance in the Notification Log and re-trigger the alert (either via Re-evaluate Alerts or by having the trigger condition fire again naturally).

---

# 7. Common Mistakes & Gotchas

**Permanently deleting an alert instead of deactivating it.** Permanent deletion removes the alert and all its configuration entirely. If you think you might need the alert again — even after a study phase ends — deactivate it instead. Deactivated alerts are preserved indefinitely and can be re-enabled at any time. Reserve permanent deletion for alerts that are definitively no longer needed.

**Re-evaluating all alerts at once in a large project.** Re-evaluating all active alerts simultaneously in a project with many records and many alerts can trigger an unexpectedly large number of email sends. Always use the Test Run option first to preview the effect, and consider re-evaluating one alert at a time to control the outcome.

**Forgetting to remove Unique Alert IDs when importing a CSV from another project.** If you export an alert CSV from one project and import it into another, the Unique Alert IDs in the CSV belong to the source installation. Importing with those IDs will generate an error. Always clear the unique ID column before importing across projects.

**Assuming the Notification Log covers ASI emails.** Automated Survey Invitation emails do not appear in the Notification Log. If you are looking for a sent survey invitation and it was configured as an ASI rather than an alert, check the ASI's own send log, not the Notification Log.

**Using the search box to find alerts by message content.** The search box on the management page filters by alert title only. If you need to find an alert based on a recipient address, subject line, or trigger logic content, you must review each alert individually or use the Notification Log's Subject column as an indirect reference.

---

# 8. Related Articles

- RC-ALERT-01 — Alerts & Notifications: Setup (required prerequisite — trigger types, scheduling, message settings)
- RC-PIPE-04 — Piping: Emails, Notifications & Logic Features (piping and smart variable usage in alert messages)
- RC-PIPE-03 — Smart Variables Overview (reference for smart variables used in alert message bodies)
- RC-LONG-02 — Repeated Instruments & Events Setup (context for trigger limits and repeated-instrument alert behavior)
