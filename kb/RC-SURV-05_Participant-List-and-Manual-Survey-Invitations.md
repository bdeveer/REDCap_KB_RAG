RC-SURV-05

**Surveys — Participant List & Manual Survey Invitations**

| **Article ID** | RC-SURV-05 |
|---|---|
| **Domain** | Surveys |
| **Applies To** | All projects with surveys enabled |
| **Prerequisite** | RC-SURV-04 — Survey Link Types & Access Methods |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-SURV-04 — Survey Link Types & Access Methods; RC-SURV-06 — Automated Survey Invitations; RC-PIPE-03 — Smart Variables Overview; RC-PIPE-01 — Piping: Basics, Syntax & Field Types |

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

An enhanced state of the participant list where record IDs are visible and clickable, linking directly to the corresponding record. Identified mode is enabled by adding a participant identifier alongside an email address, or by designating an email field at the project level.

**Participant Identifier**

An optional name or label added alongside an email address when uploading participants. Used to make the participant list run in identified mode and to help staff associate survey links with the correct person.

**Designated Email Field**

A project-level setting (configured in Project Setup → Enable Optional Modules and Customizations) that tells REDCap which variable in the project should be used as the communication email for all records. The variable must have email validation. Once set, REDCap uses the value in that field as the participant's email address for invitation purposes.

**Compose Survey Invitations**

A workflow within the participant list that allows staff to draft, schedule, and send survey invitation emails to a selected group of participants. Supports immediate sending, scheduled future sending, and up to five automatic reminders.

**Survey Invitation Log**

A project-wide log of all past and future survey invitations. It covers both manually composed invitations and those scheduled through Automated Survey Invitations (ASIs). Invitations from Alerts & Notifications are not included.

---

# 3. Participant List Overview

The participant list is accessed through Survey Distribution Tools in the project menu. It is instrument-specific: a dropdown in the top-left of the participant list selects which survey (and, in longitudinal projects, which event) the list applies to.

## 3.1 Anonymous vs. Identified Mode

Every project starts in anonymous mode. In anonymous mode, record IDs in the participant list are replaced with a "hidden" symbol, meaning staff cannot directly click through to a record from the list. REDCap still tracks which response belongs to which record internally — the restriction is only on direct navigation.

Identified mode makes the Record ID column clickable and links it to the corresponding record. There are two ways to enable it:

- **Add a participant identifier** when uploading participants (see Section 3.3).
- **Designate an email field** in Project Setup → Enable Optional Modules and Customizations. Once a valid email is entered in that field for a given record, that record becomes identified in the participant list.

> **Note:** Identified mode is per-record, not per-project. A record is identified only if it has an email or participant identifier associated with it. Records without either remain anonymous.

## 3.2 Feature Buttons

| Button | Function |
|---|---|
| Survey selector (top-left dropdown) | Selects which survey and event the participant list displays. |
| Displaying selector | Paginates the list in groups of 100. |
| Add Participants | Opens a text box for entering email addresses, one per line. Optionally, append a participant identifier: `email@example.com, Jane Doe`. Adding a participant does not create a record — the record is only created when the participant completes their first survey. |
| Compose Survey Invitations | Opens the invitation composer (see Section 4). |
| Remove All Participants | Removes all participants who have not yet submitted any data. Does not affect participants who have responded. |
| Export List | Downloads an Excel file containing all participants, their response status, invitation status, and survey links/codes. Useful for importing into external mailing systems (e.g., Epic MyChart, mail merge tools). |

## 3.3 Participant List Table Columns

| Column | Description |
|---|---|
| Email | The uploaded email address. Displays `[no email listed]` for records entered via the public survey link without an associated email. |
| Phone | Displayed only when the texting feature is enabled for the project. |
| Record | Visible in identified mode. Shows a clickable Record ID that links directly to the record. Displays a "hidden eye" icon for anonymous participants. |
| Participant Identifier | Shows any identifier added at upload. The **Enable** button in this column header activates the participant identifier feature, which adds instructional help text to the Add Participants dialog. Once enabled, the button changes to **Disable**. Disabling wipes all identifiers except those belonging to records with a completed survey. |
| Invitation Preference | Displayed only when texting is enabled. Shows the participant's preferred contact method (email, phone, or both). |
| Responded? | A colored dot indicating survey completion status: grey = not started; orange checkmark = partially completed; green checkmark = completed. |
| Invitation Scheduled? | A clock icon appears if a future invitation is queued for this participant. |
| Invitation Sent? | Blank envelope = not sent; envelope with green checkmark = sent successfully; envelope with green arrow = currently sending (large batch in progress). |
| Link | A link icon opens the individual survey for that participant in a new tab. Displays a dash if the survey is already completed. |
| Survey Access Code & QR Code | A QR icon opens the access code and QR code for that participant's specific survey link. Displays a dash if the survey is completed. |
| Survey Queue | A survey queue icon (visible in identified mode only) opens the survey queue for that record. Only appears when data exists in the record. |
| Remove | Appears for participants who have not yet submitted data. Clicking it removes that individual participant from the list. |

---

# 4. Composing Manual Survey Invitations

The **Compose Survey Invitations** button opens the "Send a Survey Invitation to Participant" dialog. This dialog is specific to the survey and event currently selected in the participant list dropdown.

## 4.1 Info Banner

A yellow info box at the top of the dialog confirms which survey (and event, for longitudinal projects) the invitations will be sent for. Always verify this before proceeding.

## 4.2 Timing Options

**Immediately** — REDCap sends invitations the moment you click **Send Invitations**.

**At a specified time** — Enter a future date and time. REDCap uses the server's internal clock and time zone, which may differ from your local time zone. The help text in the dialog shows the current server time — use it to calculate the correct local-to-server time offset.

## 4.3 Reminders

Check the **Enable Reminder** box to configure automated follow-ups. REDCap supports up to five reminders per invitation. Reminders continue sending at the defined intervals until either all reminders are exhausted or the participant completes the survey — whichever comes first. REDCap automatically cancels any unsent reminders once a response is recorded.

## 4.4 Composing the Message

**From Email** — Select a "from" address from the dropdown, which is populated by the email addresses associated with all users in the project (up to three per user, configurable in My Profile). Best practice: use a study-specific or shared team email rather than a personal account.

**Display Name** — An optional label that recipients see as the sender name in their email client (e.g., "Heart Congestion Study 2024"). Test any display name with a test participant before broad distribution — some spam filters flag display names that differ from the sending domain.

**Subject Line** — Free text. Piping variables is supported.

**Message Body** — Free text with a rich text editor. Supports HTML, images, and piping. REDCap pre-fills the body with placeholder text and the smart variables `[survey-link]` and `[survey-url]`. Keep at least one of these in the message — without them, recipients have no way to reach the survey.

> **Note on piping in initial invitations:** If a participant is being invited before their record contains any data (i.e., they have not yet filled out any survey), avoid piping field values from the project — there is nothing to pull yet. For follow-up invitations where a record exists, piping field values works normally.

> **Tip — Test Emails:** A small **send test email** link appears between the subject and message body fields. Clicking it immediately sends the current message draft to the primary email of your REDCap account. Use this to verify formatting, piping, and smart variables before sending to participants.

**Load a Previously Sent Email** — A dropdown at the bottom of the compose section lets you load a previously used invitation message. Useful when sending to multiple cohorts with the same or similar content.

## 4.5 Selecting Participants

The participant selection table at the bottom of the dialog defaults to all participants who have not yet received a sent or scheduled invitation. Manually check or uncheck individual participants to include or exclude them.

For larger participant lists, use the **Actions** dropdown in the top-right corner of the selection table to bulk-select participants based on criteria such as response status or invitation status.

## 4.6 Sending

Click **Send Invitations** to send or schedule the invitations. Click **Cancel** to close without sending.

---

# 5. Survey Invitation Log

The Survey Invitation Log is accessible from the Survey Distribution Tools menu. It provides a complete view of all past and future survey invitations for the entire project, including both manually composed invitations and those generated by Automated Survey Invitations (ASIs).

> **Important:** The log does not include emails sent by Alerts & Notifications. For alerts-related email history, see RC-ALERT-02 — Alert Management & Notification Log.

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
| Display Invitation Reminders | Checkbox (unchecked by default). When checked, individual reminders appear as separate rows. Enabling this in a project with many reminders can substantially expand the list. |
| Apply Filters | Applies all current filter settings to the displayed list. |
| Reset | Returns all filters to their defaults. |
| Download Log | Generates an Excel file of the invitations currently displayed on screen. Can be run multiple times. |
| Delete All Selected | Permanently deletes all checked future invitations. A confirmation popup appears before deletion. Deleted future invitations cannot be re-generated by ASIs — use this intentionally (e.g., withdrawing a participant from a study). |

## 5.2 Log Table Columns

| Column | Description |
|---|---|
| Invitation Send Time | The exact timestamp when the invitation was sent (past) or is scheduled to send (future), based on the server's time zone. Green = sent successfully; red = send failed; grey = scheduled. Future invitations show a pencil icon (edit the scheduled time) and a red X (delete the invitation). Reminders display a bell icon with a number in parentheses indicating which reminder in the sequence it is. |
| View Invite | An envelope icon. Click to review the message content for that invitation, including any piped-in values at the time of sending. |
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

**A:** Up to five reminders per invitation. REDCap automatically cancels any remaining reminders once the participant completes the survey.

**Q: I added participant emails to the participant list, but their records are not showing up in REDCap. Is that normal?**

**A:** Yes. Adding a participant to the list does not create a record. A record is only created when the participant submits their first survey response.

**Q: A participant says they never received the invitation. How do I check if it was sent?**

**A:** Check the Survey Invitation Log. Find the participant's email and verify the **Invitation Sent?** column. A green checkmark confirms REDCap sent it from the server side. If the invitation shows as sent but the participant didn't receive it, the most likely cause is a spam filter — REDCap cannot detect delivery failures on the recipient's end.

**Q: Can I use the Survey Invitation Log to cancel a scheduled invitation?**

**A:** Yes. In the log, find the future invitation, check its checkbox, and use **Delete All Selected**. You can also delete a single future invitation using the red X icon next to its timestamp. Deleted invitations cannot be regenerated by ASIs.

**Q: What is the difference between the participant list and the Survey Invitation Log?**

**A:** The participant list is where you manage participants and compose invitations for a specific survey. The Survey Invitation Log is a project-wide read-and-manage view of all past and future invitations across every survey, including those scheduled by ASIs.

---

# 7. Common Mistakes & Gotchas

**Expecting a record to be created when adding a participant.** Adding an email to the participant list does not create a record. The record is only created when the participant fills out the first survey. This is by design — avoid confusing "participants in the list" with "records in the project."

**Sending invitations in the wrong time zone.** REDCap schedules invitations based on the server's time zone. If you are in a different time zone, calculate the offset carefully using the server time displayed in the invite composer. Sending an invitation "at 9 AM" using your local time when the server is in a different time zone will result in an off-schedule send.

**Piping field values in an initial invitation before any record exists.** If a participant has not yet completed any survey, their record contains no data. Piping field values from the project into an invitation sent before they respond will produce blank or broken placeholders. Reserve piping for follow-up invitations where data already exists.

**Using a personal email as the From address.** Personal email addresses are tied to individuals who may leave the project. Use a study-specific or shared account. A personal-domain From address can also trigger spam filters in some institutional environments.

**Deleting all future invitations without realizing ASI-generated invitations are included.** The Survey Invitation Log shows both manually composed invitations and ASI-generated ones together. **Delete All Selected** permanently removes all checked entries, including those scheduled by ASIs. Deleted ASI invitations cannot be regenerated.

---

## API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See RC-API-01 — REDCap API for authentication, token management, and setup.

- **RC-API-43 — Export Survey Participants API** — retrieve the participant list for a survey instrument, including invitation and response status
- **RC-API-40 — Export Survey Link API** — retrieve a unique survey link for a specific record without accessing the Participant List UI

---


# 8. Related Articles

- RC-SURV-04 — Survey Link Types & Access Methods (public vs. individual links, smart variables, Survey Options menu)
- RC-SURV-06 — Automated Survey Invitations (automated, trigger-based invitation scheduling)
- RC-SURV-07 — Survey Queue (controlling multi-survey flow for participants)
- RC-ALERT-02 — Alert Management & Notification Log (email history for Alerts & Notifications)
- RC-PIPE-01 — Piping: Basics, Syntax & Field Types (using piped variables in email bodies)
- RC-PIPE-03 — Smart Variables Overview (`[survey-link]`, `[survey-url]`, and related tokens)
