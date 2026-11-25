---
id: RC-SURV-05
title: Surveys — Participant List & Manual Survey Invitations
domain: Surveys
applies_to:
- All projects with surveys enabled
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — survey
  behaviour checked against source code; pages not re-captured
prerequisites:
- RC-SURV-04 — Survey Link Types & Access Methods
version: '1.2'
last_updated: 2026-11
related:
- id: RC-SURV-04
  title: Survey Link Types & Access Methods
- id: RC-SURV-06
  title: Automated Survey Invitations (ASI)
- id: RC-PIPE-03
  title: Smart Variables Overview
- id: RC-PIPE-01
  title: 'Piping: Basics, Syntax & Field Types'
- id: RC-NAV-UI-02
  title: Project Menu Reference
- id: RC-NAV-REC-04
  title: Record Status Dashboard & Other Record Links
tags:
- surveys
synonyms:
- how do i email survey invitations to participants
- upload participant email addresses
- send individual survey links manually
- track who has responded to a survey
- participant list setup
- survey invitation log
- send a survey invite to one person
- review sent and scheduled survey invitations
---

# 1. Overview

This article covers the participant list and the manual survey invitation workflow — the tools REDCap provides for sending individualized survey links to participants via email, tracking who has responded, and reviewing the history of all sent and scheduled invitations. It also documents the Survey Invitation Log, the central place for monitoring and managing past and future invitations across an entire project. This article is part of the Surveys knowledge base series.

---

# 2. Key Concepts & Definitions

**Participant List**

A table within Survey Distribution Tools that allows project staff to upload participant email addresses, send individualized survey invitations, and monitor survey response status. Each survey (and each survey-event combination in longitudinal projects) has its own participant list.

**Anonymous Mode**

The default state of the participant list. REDCap knows which response belongs to which record internally, but the participant list does not display record IDs in a clickable form, making it harder to associate a specific response with a specific participant at a glance.

**Identified Mode**

An enhanced state of the participant list where record IDs are visible and clickable, linking directly to the corresponding record. Identified mode is enabled by adding a participant identifier alongside an email address, or by designating an email field at the project level. Even in identified mode, the Record column shows a record ID only once the participant has started or finished the survey, because the record does not exist before then.

**Participant Identifier**

An optional name or label added alongside an email address when uploading participants. Used to make the participant list run in identified mode and to help staff associate survey links with the correct person.

**Designated Email Field**

A project-level setting (configured in Project Setup → Enable Optional Modules and Customizations) that tells REDCap which variable in the project should be used as the communication email for all records. The variable must have email validation. Once set, REDCap uses the value in that field as the participant's email address for invitation purposes. In production, only a REDCap administrator can change this setting. A survey can also have its own survey-level email field (set in Survey Settings), which works the same way for that survey.

**Compose Survey Invitations**

A workflow within the participant list that allows staff to draft, schedule, and send survey invitation emails to a selected group of participants. Supports immediate sending, scheduled future sending, and up to five automatic reminders.

**Survey Invitation Log**

A project-wide log of all past and future survey invitations. It covers both manually composed invitations and those scheduled through Automated Survey Invitations (ASIs). Invitations from Alerts & Notifications are not included.

---

> **Note (15.0.0) — performance.** Rapid Retrieval caching was applied to the Participant List page, its CSV export, and the API Export Participant List method. On large participant lists this is the difference between a usable page and a slow one.

> **Version caveat (16.0.x LTS):** Because of this caching, the participant list and its export can briefly show an out-of-date sent/scheduled invitation status. 17.x reads invitation status live. On 16.0.x, refresh the page or check the Survey Invitation Log before acting on an invitation's status.

> **Version caveat (below 15.2.5 Standard):** In the **Compose Survey Invitations** dialog, selecting a previously sent email left **hardcoded links from the original message** in the template rather than regenerating them. Sending that template to a different participant could therefore include a link belonging to someone else. Fixed in 15.2.5.

---

# 3. Participant List Overview

The participant list is accessed through Survey Distribution Tools in the project menu. It is instrument-specific: a dropdown in the top-left of the participant list selects which survey (and, in longitudinal projects, which event) the list applies to.

In projects with Data Access Groups, records in other DAGs are hidden from DAG-restricted users.

## 3.1 Anonymous vs. Identified Mode

Every project starts in anonymous mode. In anonymous mode, record IDs in the participant list are replaced with a "hidden" symbol, meaning staff cannot directly click through to a record from the list. REDCap still tracks which response belongs to which record internally — the restriction is only on direct navigation.

Identified mode makes the Record ID column clickable and links it to the corresponding record. There are two ways to enable it:

- **Add a participant identifier** when uploading participants (see Section 3.3).
- **Designate an email field** in Project Setup → Enable Optional Modules and Customizations (or a survey-level email field in Survey Settings). Once a valid email is entered in that field for a given record, that record becomes identified in the participant list.

A banner above the participant list states whether responses on that list are considered anonymous, based on the current settings. In identified mode, the record ID appears only after the participant has started or finished the survey; until then there is no record to link to.

> **Note:** Identified mode is per-record, not per-project. A record is identified only if it has an email or participant identifier associated with it. Records without either remain anonymous.

> **Before adding participant identifiers:** activate the feature by clicking the **Enable** button in the Participant Identifier column header of the participant list table (see Section 3.3). This makes the column active and adds instructional help text to the Add Participants dialog. Be aware that clicking **Disable** later will wipe all stored identifiers, except those belonging to participants who have already started (partial) or completed a response. The setting applies to the whole project, not just one survey, and in production only a REDCap administrator can change it.

## 3.2 Feature Buttons

| Button | Function |
|---|---|
| Survey selector (top-left dropdown) | Selects which survey and event the participant list displays. |
| Displaying selector | Paginates the list in groups of 50. |
| Add Participants | Opens a text box for entering email addresses, one per line. Optionally, append a participant identifier: `email@example.com, Jane Doe`. If participant identifiers have not been enabled, a batch that includes identifiers is rejected. The same email can be added more than once; duplicates are numbered so each gets its own link. Adding a participant does not create a record — the record is only created when the participant submits the first page of the survey. Available only on the first instrument (see Section 3.4). |
| Compose Survey Invitations | Opens the invitation composer (see Section 4). |
| Remove All Participants | Removes all participants who have not yet submitted any data. Does not affect participants who have responded. Available only on the participant list of the first survey (in the first event, for longitudinal projects). |
| Export List | Downloads a CSV file containing all participants, their response status, invitation status, and survey links/codes. Useful for importing into external mailing systems (e.g., Epic MyChart, mail merge tools). |

## 3.3 Participant List Table Columns

| Column | Description |
|---|---|
| Email | The uploaded email address. Displays `[no email listed]` for records entered via the public survey link without an associated email. |
| Phone | Displayed only when the texting feature is enabled for the project. |
| Record | Visible in identified mode. Shows a clickable Record ID that links directly to the record, once the participant has started or finished the survey. Displays a "hidden eye" icon for anonymous participants. |
| Participant Identifier | Shows any identifier added at upload. The **Enable** button in this column header activates the participant identifier feature, which adds instructional help text to the Add Participants dialog. Once enabled, the button changes to **Disable**. Disabling wipes all identifiers except those belonging to participants with a partial or completed response. |
| Invitation Preference | Displayed only when texting is enabled. Shows the participant's preferred contact method (email, phone, or both). |
| Responded? | A colored dot indicating survey completion status: grey = not started; orange checkmark = partially completed; green checkmark = completed. |
| Invitation Scheduled? | A clock icon appears if a future invitation is queued for this participant. |
| Invitation Sent? | Blank envelope = not sent; envelope with green checkmark = sent successfully; envelope with green arrow = currently sending (large batch in progress). |
| Link | A link icon opens the individual survey for that participant in a new tab. Displays a dash if the survey is already completed or its time limit has expired. |
| Survey Access Code & QR Code | A QR icon opens the access code and QR code for that participant's specific survey link. Displays a dash if the survey is completed or its time limit has expired. |
| Link Expiration | Shows when the participant's link stops working, if a time limit applies. |
| Survey Queue | A survey queue icon opens the survey queue for that record. Appears for any participant who has a record (data exists), whether or not the list is identified. |
| Remove | Appears for participants who have not yet submitted data. Clicking it removes that individual participant from the list. |

## 3.4 Follow-Up Surveys and Projects Whose First Instrument Is Not a Survey

**Add Participants** is available only on the participant list of the project's first instrument (in the first event, for longitudinal projects), and only when that instrument is a survey. For every other survey — a follow-up survey, or any survey in a project whose first instrument is a data entry form — the participant list cannot be added to directly. Instead:

- The list is filled from existing records. A record appears once it has been created, by staff data entry, import or an earlier survey.
- The email address comes from the first survey's participant list (when the first instrument is a survey), or from the designated email field or the survey-level email field.
- Records with no email from any of these sources show `[no email listed]` and cannot be sent an email invitation until one is entered.

When the first instrument is not a survey, set up a designated email field (or a survey-level email field) so invitations have an address to go to. When a participant opens a survey from a participant-list invitation, the designated email field on that survey is pre-filled with their email and locked.

---

# 4. Composing Manual Survey Invitations

The **Compose Survey Invitations** button opens the "Send a Survey Invitation to Participant" dialog. This dialog is specific to the survey and event currently selected in the participant list dropdown.

## 4.1 Info Banner

A yellow info box at the top of the dialog confirms which survey (and event, for longitudinal projects) the invitations will be sent for. Always verify this before proceeding.

## 4.2 Timing Options

**Immediately** — REDCap queues the invitations when you click **Send Invitations**, and the scheduler sends them, usually within about a minute.

**At a specified time** — Enter a future date and time. REDCap uses the server's internal clock and time zone, which may differ from your local time zone. The help text in the dialog shows the current server time — use it to calculate the correct local-to-server time offset.

## 4.3 Reminders

Check the **Enable Reminder** box to configure automated follow-ups. REDCap supports up to five reminders per invitation. Reminders continue sending at the defined intervals until either all reminders are exhausted or the participant completes the survey — whichever comes first. REDCap automatically cancels any unsent reminders once the response is completed; a partial response does not stop them.

Composing a new invitation for a participant who already has a queued invitation for the same survey replaces that queued invitation and its reminders.

## 4.4 Composing the Message

**From Email** — Select a "from" address from the dropdown, which is populated by the email addresses associated with all users in the project (up to three per user, configurable in My Profile). Best practice: use a study-specific or shared team email rather than a personal account.

**Delivery method** — If texting (Twilio or Mosio) is enabled for the project, a selector lets you choose how the invitation is delivered (email, SMS or voice, depending on the setup).

**Display Name** — Appears only if your REDCap administrator has enabled it. An optional label that recipients see as the sender name in their email client (e.g., "Heart Congestion Study 2024"). Test any display name with a test participant before broad distribution — some spam filters flag display names that differ from the sending domain.

**Subject Line** — Free text. Piping variables is supported.

**Message Body** — Free text with a rich text editor. Supports HTML, images, and piping. REDCap pre-fills the body with placeholder text and the smart variables `[survey-link]` and `[survey-url]`. Keep at least one of these in the message — without them, recipients have no way to reach the survey.

> **Note on piping in initial invitations:** If a participant is being invited before their record contains any data (i.e., they have not yet filled out any survey), avoid piping field values from the project — there is nothing to pull yet. For follow-up invitations where a record exists, piping field values works normally.

> **Tip — Test Emails:** A small **send test email** link appears between the subject and message body fields. Clicking it immediately sends the current message draft to the primary email of your REDCap account. The test fails if the selected From address is not one of your own account's addresses. Use this to verify formatting, piping, and smart variables before sending to participants.

**Load a Previously Sent Email** — A dropdown at the bottom of the compose section lets you load an invitation message sent in the last 12 months (DAG-restricted users see only messages from their own DAG). Useful when sending to multiple cohorts with the same or similar content.

## 4.5 Selecting Participants

The participant selection table at the bottom of the dialog pre-checks all participants who have not yet been sent an invitation, do not have one scheduled, and have not started the survey. Manually check or uncheck individual participants to include or exclude them.

For larger participant lists, use the **Actions** dropdown in the top-right corner of the selection table to bulk-select participants based on criteria such as response status or invitation status.

## 4.6 Sending

Click **Send Invitations** to send or schedule the invitations. Click **Cancel** to close without sending.

---

# 5. Survey Invitation Log

The Survey Invitation Log is accessible from the Survey Distribution Tools menu. It provides a complete view of all past and future survey invitations for the entire project, including both manually composed invitations and those generated by Automated Survey Invitations (ASIs).

> **Important:** The log does not include emails sent by Alerts & Notifications. For alerts-related email history, see [RC-ALERT-02 — Alert Management & Notification Log](RC-ALERT-02_Alert-Management-and-Notification-Log.md).

## 5.1 Header Bar Filters

| Control | Function |
|---|---|
| Displaying selector | Paginates the log in groups of 100. |
| View Past / View Future | Quick-filter buttons that set the Begin Time and End Time fields to show past or future invitations respectively. Clear both time fields and click Apply to show all invitations at once. |
| Begin Time | Lower bound of the time window. Leave blank to include all invitations from the beginning. |
| End Time | Upper bound of the time window. Leave blank to include all invitations to the end. |
| Display Invitation Types | Filter by status type (e.g., scheduled, sent). Single selection only. |
| Display Response Status | Filter by survey completion status (e.g., unresponded, partially completed). Single selection only. |
| Display Surveys | Filter by a specific survey or survey-event combination. Single selection only. |
| Display Records | Filter by Record ID. For large projects, type a Record ID to jump to it instead of scrolling. Single selection only. |
| Display Invitation Reminders | Checkbox (checked by default). When checked, individual reminders appear as separate rows. Enabling this in a project with many reminders can substantially expand the list. |
| Apply Filters | Applies all current filter settings to the displayed list. |
| Reset | Returns all filters to their defaults. |
| Download Log | Downloads a CSV file of all invitations that match the current filters, across all pages (not just the page on screen). Can be run multiple times. |
| Delete All Selected | Permanently deletes all checked future invitations. A confirmation popup appears before deletion. A deleted ASI invitation can be scheduled again if the record meets the ASI conditions again, unless you tick the option to permanently cancel it in the confirmation popup — tick it when you mean to stop that ASI for good (e.g., withdrawing a participant from a study). |

## 5.2 Log Table Columns

| Column | Description |
|---|---|
| Invitation Send Time | The exact timestamp when the invitation was sent (past) or is scheduled to send (future), based on the server's time zone. Green = sent successfully; red = send failed; grey = scheduled. Future invitations show a pencil icon (reschedule that one invitation) and a red X (delete the invitation). Reminders display a bell icon with a number in parentheses indicating which reminder in the sequence it is. |
| View Invite | An envelope icon. Click to review the message content for that invitation, including any piped-in values. Piping is filled in when the invitation is composed (or scheduled), not when it goes out, so data entered after that does not appear. |
| Participant Email | The email address the invitation is or was sent to. |
| Participant Phone | Displayed only when texting is enabled for the project. |
| Record | In identified mode, shows a clickable Record ID linking to the record. |
| Participant Identifier | Displays the identifier if one was defined for that participant. |
| Survey | The survey (or survey-event combination in longitudinal projects) this invitation is for. |
| Survey Link | Link icon opens the survey in a new tab. Dash = survey already completed. |
| Responded? | Status dot: grey = not started; orange checkmark = partially completed; green checkmark = completed. In identified mode, the dot is clickable and links to the survey response. |
| Errors (if any) | Displays a short error message in the rare event that REDCap failed to send the invitation from the server side. Note: REDCap only confirms server-side sending — it cannot detect if an invitation was caught by a spam filter on the recipient's end. |
| Checkbox (no header) | Appears for future invitations only. Check to select for bulk deletion using **Delete All Selected**. Checking the header checkbox selects or deselects all visible invitations. |

---

# 6. Common Questions

**Q: How do I send a survey invitation to a participant?**

**A:** Navigate to Survey Distribution Tools → Participant List, select the correct survey (and event) in the dropdown, click **Add Participants** to enter the email address, then click **Compose Survey Invitations** to draft and send the invitation.

**Q: What is the difference between anonymous and identified mode in the participant list?**

**A:** In anonymous mode, the participant list does not display clickable record IDs — you can see that a survey was completed but cannot navigate directly to the record from the list. In identified mode, record IDs are clickable and link to the record. Enable identified mode by adding a participant identifier when uploading emails, or by designating a project-level email field in Project Setup.

**Q: How many reminders can I set up for a manual survey invitation?**

**A:** Up to five reminders per invitation. REDCap automatically cancels any remaining reminders once the participant completes the survey. A partial response does not stop them.

**Q: I added participant emails to the participant list, but their records are not showing up in REDCap. Is that normal?**

**A:** Yes. Adding a participant to the list does not create a record. A record is only created when the participant submits the first page of the survey.

**Q: A participant says they never received the invitation. How do I check if it was sent?**

**A:** Check the Survey Invitation Log. Find the participant's email and look at the icon in the **Invitation Send Time** column: a green checkmark means REDCap sent it from the server side, a grey clock means it is still scheduled, and red means sending failed. The **Invitation Sent?** column in the Participant List shows the same for that survey. If the invitation shows as sent but the participant didn't receive it, the most likely cause is a spam filter — REDCap cannot detect delivery failures on the recipient's end.

**Q: Can I use the Survey Invitation Log to cancel a scheduled invitation?**

**A:** Yes. In the log, find the future invitation, check its checkbox, and use **Delete All Selected**. You can also delete a single future invitation using the red X icon next to its timestamp. A deleted ASI invitation can be scheduled again if the record meets the ASI conditions again; tick the permanently cancel option in the confirmation popup to prevent that.

**Q: What is the difference between the participant list and the Survey Invitation Log?**

**A:** The participant list is where you manage participants and compose invitations for a specific survey. The Survey Invitation Log is a project-wide read-and-manage view of all past and future invitations across every survey, including those scheduled by ASIs.

---

# 7. Common Mistakes & Gotchas

**Expecting a record to be created when adding a participant.** Adding an email to the participant list does not create a record. The record is only created when the participant fills out the first survey. This is by design — avoid confusing "participants in the list" with "records in the project."

**Sending invitations in the wrong time zone.** REDCap schedules invitations based on the server's time zone. If you are in a different time zone, calculate the offset carefully using the server time displayed in the invite composer. Sending an invitation "at 9 AM" using your local time when the server is in a different time zone will result in an off-schedule send.

**Piping field values in an initial invitation before any record exists.** If a participant has not yet completed any survey, their record contains no data. Piping field values from the project into an invitation sent before they respond will produce blank or broken placeholders. Reserve piping for follow-up invitations where data already exists.

**Using a personal email as the From address.** Personal email addresses are tied to individuals who may leave the project. Use a study-specific or shared account. A personal-domain From address can also trigger spam filters in some institutional environments.

**Deleting all future invitations without realizing ASI-generated invitations are included.** The Survey Invitation Log shows both manually composed invitations and ASI-generated ones together. **Delete All Selected** removes all checked entries, including those scheduled by ASIs. A deleted ASI invitation can be scheduled again if the record meets the ASI conditions again, so tick the permanently cancel option when you mean to stop it for good, and leave it unticked if the ASI should be able to fire again.

---

## API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) for authentication, token management, and setup.

- **[RC-API-43 — Export Survey Participants API](RC-API-43_Export-Survey-Participants.md)** — retrieve the participant list for a survey instrument, including invitation and response status
- **[RC-API-40 — Export Survey Link API](RC-API-40_Export-Survey-Link.md)** — retrieve a unique survey link for a specific record without accessing the Participant List UI

---


# 8. Related Articles

- [RC-SURV-04 — Survey Link Types & Access Methods](RC-SURV-04_Survey-Link-Types-and-Access-Methods.md) (public vs. individual links, smart variables, Survey Options menu)
- [RC-SURV-06 — Automated Survey Invitations (ASI)](RC-SURV-06_Automated-Survey-Invitations.md) (automated, trigger-based invitation scheduling)
- [RC-SURV-07 — Survey Queue](RC-SURV-07_Survey-Queue.md) (controlling multi-survey flow for participants)
- [RC-ALERT-02 — Alert Management & Notification Log](RC-ALERT-02_Alert-Management-and-Notification-Log.md) (email history for Alerts & Notifications)
- [RC-PIPE-01 — Piping: Basics, Syntax & Field Types](RC-PIPE-01_Piping-Basics-Syntax-and-Field-Types.md) (using piped variables in email bodies)
- [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md) (`[survey-link]`, `[survey-url]`, and related tokens)
- [RC-NAV-UI-02 — Project Menu Reference](RC-NAV-UI-02_Project-Menu-Reference.md) (the Participant List is accessed via Survey Distribution Tools in the Data Collection section of the left menu)
- [RC-NAV-REC-04 — Record Status Dashboard & Other Record Links](RC-NAV-REC-04_Record-Status-Dashboard-and-Links.md) (Record ID links in the invitation log and participant list navigate to the Record Home Page only in identified mode; links are disabled in anonymous surveys)
