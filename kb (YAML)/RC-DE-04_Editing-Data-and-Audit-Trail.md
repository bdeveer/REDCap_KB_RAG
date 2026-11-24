---
id: RC-DE-04
title: Editing Data & Audit Trail
domain: Data Entry
applies_to:
- All REDCap project types
requires: Any supported version
verified_against: REDCap v17.5.4 (Standard) / v17.3.18 (LTS) — changelog review; page
  not re-captured. Data editing and Data History behaviour checked against source
  code of v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS)
prerequisites:
- RC-DE-02 — Basic Data Entry
version: '1.2'
last_updated: 2026-11
related:
- id: RC-DE-01
  title: Record Creation & the Record Home Page
- id: RC-DE-02
  title: Basic Data Entry
- id: RC-DE-03
  title: Longitudinal Projects & DAGs
tags:
- data entry
synonyms:
- how do i edit data that was already saved
- view the change history for a field
- audit trail for editing data
- who changed this value and when
- edit data that came in from a survey
- see the full history of data changes
- modify previously entered data
- field-level audit trail data entry
- require a reason for change when editing data
- data history popup not showing
---

# 1. Overview

This article explains how to edit previously saved data in REDCap, how
to access the audit trail for individual fields, and how to edit data
that was originally entered via a survey. REDCap records a complete
history of all data changes, and that history is always accessible to
authorized users.

---

# 2. Key Concepts & Definitions

**Data Edit**

The act of opening a previously saved instrument, changing one or more
field values, and saving the form again. REDCap records the old and new
values as part of the audit trail automatically.

**Audit Trail (Logging)**

A complete, timestamped record of every data change made in a REDCap
project. The audit trail records who changed what, when, and from what
value to what value. Users cannot edit or delete individual log entries.
One exception: a REDCap administrator can enable a per-project setting
(Control Center → **Edit a Project's Settings**) that lets users, when they
delete a record, also remove that record's logged data values (replaced with
`[*DATA REMOVED*]`) and its email log entries. This exists for erasure
requests such as GDPR. Without it, a deleted record's earlier data stays
visible in Logging.

**Field History ('H' button)**

An inline audit view available on individual fields during data entry.
Selecting the small 'H' icon next to a field shows a popup with the
complete change history for that specific field in that record.

**Logging Application**

A project-level application (accessible from the left-hand menu for
authorized users) that provides a searchable, filterable view of all
audit trail events across all records, instruments, and users.

**Survey Edit Right ("Edit survey responses")**

A per-instrument user right that must be explicitly granted to allow
editing of instrument data that was originally submitted via a survey. It
is off by default. It sits next to the instrument's data entry rights,
needs **View & Edit** on that instrument, and appears only when the system
setting **Allow users to edit survey responses?** is enabled. Administrators
have it automatically. Without this right, survey responses, including
partial (started but not completed) responses, are read-only.

**Reason for Change**

A project setting, **Require a 'reason' when making changes to existing
records?** (Project Setup → **Additional customizations**), that prompts
users to type a short reason whenever they change existing data. See
section 3.3.

---

# 3. Editing Previously Saved Data

## 3.1 Standard Edit Workflow

Editing data in REDCap follows the same path as entering it for the
first time:

- Navigate to the record using Add/Edit Records, the Record Status
    Dashboard, or any Record ID link.

- On the Record Home Page, select the dot for the instrument you want
    to edit.

- Change the field values you need to update.

- Save the form using any of the available save options.


> **Note:** REDCap automatically logs the old and new values, the user who made the change, and the timestamp. You do not need to do anything special to trigger audit logging — it happens on every save.


## 3.2 What Gets Logged

- Every field value change is recorded, including the previous value
    and the new value.

- The timestamp uses the REDCap server's local time (not the user's
    browser time).

- The username of the user who made the change is always recorded.

- Form status changes (e.g., setting a form to 'Complete') are also
    logged.

- Logging stores the new values from each save. The "old" value you see
    in the history is the previous logged value, not a separate copy.
    Saving a form without changing anything can still create an (empty)
    update entry.

- Data changes from every source are logged: form saves, surveys, Data
    Import Tool, API, auto-calculated values, data fetched from external
    sources (Data Transfer Services / Dynamic Data Pull), deletions and
    record merges.

## 3.3 Requiring a Reason for Change

If the project setting **Require a 'reason' when making changes to
existing records?** is enabled (Project Setup → **Additional
customizations**):

- It applies in any project status, not only Production.
- The prompt appears on save only when the record already exists, the
    instrument already has data, and values were changed (or the data is
    being deleted). Entering data on a new record or a blank instrument
    does not prompt.
- It does not appear on surveys.
- The Data Import Tool and bulk record deletion also ask for a reason.
- The reason is limited to 200 characters.
- The reason is stored with the change and shown in Logging and in the
    'H' popup under **Reason for Data Change(s)**.

## 3.4 Locked Instruments

You cannot save a locked instrument unless you have locking rights and
unlock it first. A locked record cannot be saved at all until it is
unlocked.

---

# 4. Accessing the Audit Trail

## 4.1 Field-Level History: the 'H' Button

- When viewing or editing an instrument, look for a small grey 'H'
    icon next to each field label.

- Select the 'H' button to open the Data History popup, showing every
    saved value for that field in that record, in chronological order.

- Each entry shows the date/time, the username, and the value. Multiple
    choice values show the label and the code; checkboxes show each option
    as checked or unchecked; missing data codes are labelled. The latest
    entry is marked **(most recent data change)**. If the field has never
    been saved, the popup says **No data exists for this field**.

- If reason for change is required, the reason appears in the **Reason for
    Data Change(s)** column.

- For File Upload fields, if file version history is enabled, the popup
    adds **Version** and download columns and shows when and by whom a file
    was deleted. Signature fields do not get version history.

- When the 'H' button appears:

    - Only if the project setting **Enable the Data History popup for all
        data collection instruments?** (Project Setup → **Additional
        customizations**) is enabled.
    - Only once the record exists; it is hidden on a brand-new unsaved
        record and in draft-mode preview.
    - Never on descriptive text, hidden fields, buttons, matrix headers,
        or the lock and e-signature rows.

- If a record is deleted and then re-created with the same record ID, the
    popup shows only the history since re-creation. The earlier history
    remains in Logging.

> **Important:** The 'H' popup shows usernames, reasons for change and
> file downloads to anyone who can view the instrument (read-only or
> higher), even without the Logging right. Data Access Group restrictions
> still apply. Consider this before granting read-only access to
> instruments with sensitive file uploads or reasons for change.

> **Version caveat (older versions):** For **File Upload** fields that should not be editable — survey responses outside edit mode, or fields with `@READONLY` / `@READONLY-FORM` — the history popup still offered **Delete** links. Using them gave misleading confirmations or actually changed the protected file. The fix is in 17.5.1+ Standard, 17.3.14+ LTS and 16.0.61 LTS. On an older version, don't use Delete links in the history popup for protected files, and upgrade.

## 4.2 Project-Level Logging Application

- If you have Logging access rights, the Logging application appears
    in the left-hand menu under Applications.

- Logging provides a full project-level audit trail. You can filter by
    event type (for example, data changes only), user, record, Data Access
    Group, and begin/end date and time. There is no filter by instrument
    or event; to find changes on one instrument, filter by record and
    scan, or export the log.

- The Logging right effectively gives read access to all saved values in
    the project, regardless of the user's instrument-level and export
    rights. Grant it with that in mind.

- Use Logging when you need to audit multiple records or find out what
    a specific user changed across the project.


> **Note:** Access to the Logging application is controlled by user rights. If you do not see it in the left-hand menu, your account has not been granted Logging access. Contact your project administrator.


---

# 5. Editing Survey-Submitted Data

## 5.1 Why Survey Editing Is Restricted

When a participant submits an instrument as a survey (even a partial
response that was started but not completed), REDCap makes the form
read-only, shown with an orange header, to prevent the study team from inadvertently altering
participant-reported data. Editing survey data is treated as a special,
deliberate action that requires an explicit user right.

## 5.2 Checking Whether You Have Survey Edit Rights

- Navigate to the survey-completed instrument. It will display as
    read-only if survey edit rights are not enabled for your account.

- If you have survey edit rights, an **Edit response** button
    appears at the top of the form.

- If you do not see the button and need to edit the data, contact your
    project administrator to request the **Edit survey responses** right
    for that instrument. If the right is not offered in User Rights at
    all, the system setting that allows it is off on your server.

> **Institution-specific:** Whether users may edit survey responses at all
> is a system setting chosen by each REDCap installation. Check with your
> REDCap administrators.

## 5.3 Editing a Survey Response (If You Have Rights)

- Navigate to the survey-completed instrument.

- Select the **Edit response** button at the top of the form. The header
    shows **(now editing)**.

- Make your changes to the field values. For a completed response, the
    **Save & Mark Response as Complete** option is removed and Form Status
    stays read-only.

- Save the form using any of the available save options. Do not navigate
    away without saving — unsaved changes are lost.


> **Important:** Editing a survey response does not notify the original survey respondent. The edit is logged in the project's audit trail with your username and timestamp. Document any such edits in your study's data management notes per your protocol SOPs.

- **View all contributors to this response** lists everyone who changed
    the response.
- e-Consent responses stay read-only unless the project allows editing
    of e-Consent responses.
- PROMIS adaptive and auto-scoring instruments can never be edited.


---

# 6. Common Questions

**Q: Does REDCap keep a record of what data looked like before I edited
it?**

**A:** Yes. REDCap logs every change automatically. The old value, new
value, user, and timestamp are all preserved in the audit trail. Use the
'H' button next to any field or the Logging application to view the
full history.

**Q: Can I undo a change after saving?**

**A:** Not directly. REDCap has no undo button. To revert a value, you must
manually re-enter the original value and save the form again. The audit
trail will record the revert as a separate edit.

**Q: A form was completed as a survey and now shows as read-only. How do
I edit it?**

**A:** You need the **Edit survey responses** user right for that
instrument (plus View & Edit). If you have it, an **Edit response** button
appears at the top of the form. If you
do not have this right, contact your project administrator.

**Q: I can see the 'H' button but the history only shows one entry. Is
that normal?**

**A:** Yes. If the field has only been saved once, the history will show
only one entry — the initial value. A history with one entry simply
means the field has never been edited since it was first saved.

**Q: Can I delete an individual data point rather than editing it?**

**A:** In most cases, you clear a field by editing the instrument and
removing the value (leaving the field blank), then saving. Some field
types (like radio buttons) have a reset option. Deleting a whole record
requires the **Delete Records** user right (not administrator rights).
Deleting all data on a single instrument for a record uses the
instrument-level delete permission in user rights.

**Q: Who can see the audit trail?**

**A:** Users with the Logging user right can access the full project-level
audit trail via the Logging application. When the Data History popup is
enabled for the project, the field-level 'H' button is visible to all users
who can view the instrument (read-only or higher), regardless of Logging
rights, and shows usernames, reasons for change and file downloads.

---

# 7. Common Mistakes & Gotchas

- Editing a survey form and forgetting to save: survey edit mode works
    like any other data entry — you must select a save button before
    navigating away or changes are lost.

- Expecting an undo function: REDCap has no undo. Reversion requires
    manually re-entering the previous value. The audit trail provides
    the reference for what the old value was.

- Not documenting survey response edits: editing a survey-submitted
    response is an unusual action that may require documentation in your
    study's data management records. Check your protocol SOPs before
    editing.

- Looking for the 'H' button and not finding it: the 'H' button is
    only visible when the instrument is open in edit or view mode, the
    record already exists, and **Enable the Data History popup for all
    data collection instruments?** is on in Project Setup →
    **Additional customizations**. It does not appear on the Record Home
    Page or Record Status Dashboard, in draft-mode preview, or on
    descriptive, hidden or button fields.

- Expecting the reason-for-change prompt only in Production: once
    enabled, it applies in every project status whenever existing data
    is changed.

- Confusing field history with the Logging application: the 'H'
    button shows history for one specific field in one specific record.
    The Logging application shows all changes across all fields and
    records in the project.

## API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) for authentication, token management, and setup.

- **[RC-API-39 — Export Logging API](RC-API-39_Export-Logging.md)** — programmatically retrieve the project audit log, including data change events, user actions, and timestamps

---


# 8. Related Articles

- [RC-DE-01 — Record Creation & the Record Home Page](RC-DE-01_Record-Creation-and-Record-Home-Page.md)

- [RC-DE-02 — Basic Data Entry](RC-DE-02_Basic-Data-Entry.md) (prerequisite — covers save options
    and form navigation)

- [RC-DE-03 — Longitudinal Projects & DAGs](RC-DE-03_Longitudinal-Projects-and-DAGs.md)
