---
id: RC-ALERT-01
title: Alerts & Notifications — Setup
domain: Alerts & Notifications
applies_to:
- All REDCap project types
- requires the **Alerts & Notifications** user right
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — alert
  setup behaviour checked against source code; pages not re-captured
prerequisites:
- 'RC-PIPE-01 — Piping: Basics, Syntax & Field Types'
version: '1.8'
last_updated: 2026-11
related:
- id: RC-PIPE-01
  title: 'Piping: Basics, Syntax & Field Types'
- id: RC-PIPE-03
  title: Smart Variables Overview
- id: RC-PIPE-04
  title: 'Piping: Emails, Notifications & Logic Features'
- id: RC-BL-01
  title: 'Branching Logic: Overview & Scope'
- id: RC-SURV-01
  title: Surveys – Basics
- id: RC-ALERT-02
  title: Alert Management & Notification Log
- id: RC-CC-06
  title: 'Control Center: Modules & Services Configuration'
- id: RC-CALC-01
  title: Special Functions Reference
tags:
- alerts & notifications
synonyms:
- how do I send an automated email in REDCap
- email reminders
- automatic notifications when a form is saved
- send an email when a survey is completed
- staff notification email
- confirmation email to participant
- conditional email alert
- trigger an email based on logic
- difference between alerts and ASIs
- set up alerts and notifications
- SMS or text message notification
---

# 1. Overview

This article explains how to create and configure an Alert & Notification in REDCap. Alerts are project-level automated emails (or, depending on your installation, SMS messages or voice calls) that trigger based on data events or logic conditions in your project. Unlike Automated Survey Invitations (ASIs), alerts are not tied to a specific survey — they can respond to any form save event, any logic condition, or a combination of both. This flexibility makes them suitable for confirmation emails, staff notifications, study reminders, and survey invitations sent to multiple recipients simultaneously.

Setting up an alert has three sequential steps: defining the **trigger** (what causes the alert to fire), the **schedule** (when and how often to send it), and the **message** (what to send). This article covers all three steps in full.

---

# 2. Key Concepts & Definitions

**Alert & Notification**
A project feature in REDCap that automatically sends an email (or other message type) when a defined trigger condition is met. Alerts are decoupled from surveys, giving them more recipient and formatting flexibility than Automated Survey Invitations.

**Trigger**
The condition that causes REDCap to queue an alert for sending. A trigger can be a form or survey save event, a logic condition, or a combination of both.

**Completion Trigger**
An alert trigger type that fires when a specific instrument is saved. The trigger does not evaluate any logic — it fires on the save event alone (subject to the form status requirement).

**Combination Trigger**
An alert trigger type that fires when a specific instrument is saved AND a logic condition is simultaneously true. Both conditions must be met.

**Logic Trigger**
An alert trigger type that fires when a logic condition becomes true, regardless of which instrument was saved. This trigger evaluates across data entry, data import, API writes, and time-based logic.

**Trigger Limit**
A setting available in longitudinal projects or projects using repeated instruments that controls how many times a single alert can fire per record. Examples include once per record, once per event, or once per repeat instance.

**Schedule**
The second step of alert setup. Defines when REDCap sends the alert after the trigger fires (immediately, on a future day/time, or after a time delay) and how many times it sends.

**Alert Expiration**
An optional date and time at which REDCap deactivates the alert, so nothing further is sent from it.

**datediff**
A REDCap logic function that compares two dates or date-times and returns the numeric difference in a specified unit (days, hours, minutes, etc.). Commonly used to build time-based trigger logic for alerts. The returned value is **unsigned by default**; pass `true` as a fourth parameter when the direction of the difference matters. See [RC-CALC-01 — Special Functions Reference](RC-CALC-01_Special-Functions-Reference.md).

**Smart Variable**
A special REDCap token that resolves to a dynamic value at send time, such as a survey link, a form link, or a survey queue URL. Smart variables are inserted into alert messages using bracket notation (e.g., `[survey-link:instrument_name]`).

**Ensure Logic is Still True**
An optional checkbox in the alert trigger setup. When enabled, REDCap re-evaluates the trigger logic immediately before sending the alert, and again whenever the record's data is later saved or imported. If the logic is no longer true, REDCap cancels that scheduled alert.

---

# 3. Alert Triggers

Navigate to **Alerts & Notifications** in the project Applications menu. Select **+ Add New Alert** to open the alert creation dialog.

Only users with the **Alerts & Notifications** user right can see this page and create, edit or upload alerts. Project Design and Setup rights alone are not enough.

Before configuring the trigger, give the alert a clear title. This is optional but strongly recommended for any project with more than a few alerts, as titles are the primary way to identify alerts in the management view and notification log.

## 3.1 Step 1A — How Will the Alert Be Triggered?

Choose one of three trigger types. This selection determines what Step 1B asks for, so always start here.

| Trigger Type | When It Fires | Also Called |
|---|---|---|
| When a record is saved on a specific form/survey | On any save of a specific instrument (conditional on form status) | Completion trigger |
| If conditional logic is TRUE when a record is saved on a specific form/survey | On a save of a specific instrument, only if a logic condition is also true | Combination trigger |
| When conditional logic is TRUE during data import, data entry, or as the result of time-based logic | When a logic condition becomes true, regardless of save source | Logic trigger |

> **Note:** Completion triggers and combination triggers do not fire when data is written via the Data Import tool or the API. Only direct data entry and survey completion activate them. Logic triggers evaluate across all write methods including imports and API calls.

## 3.2 Step 1B — Trigger Details

**For completion triggers and combination triggers:**

Select the instrument from the dropdown. In longitudinal projects, the dropdown shows instrument-event combinations rather than instruments alone, plus an **[Any event]** option for each instrument when the alert should fire whichever event the instrument is saved in.

Then select a form status requirement:

- **"Is saved with any form status"** — fires the moment the instrument is saved, regardless of completion status. This is the default for a new alert.
- **"Is saved with Complete status only"** — fires only when the instrument's completion status is set to Complete (status value 2). Surveys completed by participants receive this status automatically. Partially saved surveys are excluded.

**For combination triggers and logic triggers:**

Enter a logic statement in the logic editor. The editor is the same interface used for branching logic. If you are unfamiliar with logic syntax, see [RC-BL-01 — Branching Logic: Overview & Scope](RC-BL-01_Branching-Logic-Overview-and-Scope.md).

> **Version caveat (below 17.5.1 Standard / 17.3.14 LTS):** Alert logic containing **comment lines** (`//` or `#`) might not be evaluated correctly, so an alert that should have fired did not. On older instances, keep comments out of alert logic. See [RC-BL-02 — Branching Logic: Syntax & Atomic Statements](RC-BL-02_Branching-Logic-Syntax-and-Atomic-Statements.md) §3.6.

The logic evaluates at the record level. You cannot write logic that counts records across the entire project (e.g., "trigger if 20 survey responses have arrived"). All logic must reference variables within a single record.

**The "Ensure logic is still true before sending" checkbox**

This checkbox appears beneath the logic editor for combination and logic triggers. When checked, REDCap re-evaluates the logic condition immediately before sending the alert, and also each time the record is saved or imported while the alert is waiting to send. If the condition is no longer true, REDCap cancels that queued alert instance. In practice it works as a kill switch: change the data so the logic is false and the pending alert is removed.

This option is most valuable when the alert schedule includes a time delay. Example: an alert set to send a clinic visit reminder 14 days before the visit date should check at send time whether the participant is still enrolled. Without this check, a participant who has withdrawn would still receive the reminder.

> **Note:** The check only has no practical effect when the alert sends **immediately and just once** — the alert fires and sends in the same moment. For any delayed or recurring alert it matters, because it is what stops later sends once the condition no longer holds.

## 3.3 Step 1B Sidebar — Date/Time Logic with datediff

To trigger an alert based on a date or date-time value, use the `datediff` function. This function compares two dates and returns the numeric difference in a specified time unit.

Basic syntax:

```
datediff(date1, date2, "unit", returnSignedValue)
```

Units: `"d"` (days), `"h"` (hours), `"m"` (minutes), `"M"` (months), `"y"` (years), `"s"` (seconds).

The fourth parameter is optional and defaults to `false`, which makes the result **unsigned**: `datediff` returns the same positive number regardless of which date is later. Pass `true` when the direction of the difference matters, which in alert logic it usually does. See [RC-CALC-01 — Special Functions Reference](RC-CALC-01_Special-Functions-Reference.md) for the full signature.

**Static comparison:**
```
datediff("2025-01-01", "2025-01-07", "d")
```
Returns `6`. The result never changes because both dates are hard-coded.

> **Write hard-coded dates as year-month-day.** A date typed into `datediff` must use the `YYYY-MM-DD` form, whatever display format the date fields use. A value such as `"01/07/2025"` makes `datediff` return blank, so the logic is never true and the alert never fires. Test any hard-coded date in the logic editor before relying on it.

**Dynamic comparison using "today":**
```
datediff("2025-01-01", "today", "d")
```
Returns the number of days since January 1, 2025, and increases by 1 each day.

**Dynamic comparison using a record variable:**
```
datediff("today", [visit_date], "d", true) = "14"
```
Becomes true when today's date is exactly 14 days before the value in `[visit_date]`. Use this pattern to trigger alerts a fixed number of days before a date stored in the record.

> **The `true` is required here.** Without it `datediff` returns an unsigned value, so the condition would match a record whose visit date was 14 days in the *past* just as readily as one 14 days in the future. A version of this condition written as `datediff([visit_date], "today", "d") = "-14"`, with no sign parameter, is never true at all.

> **Important:** When using date-based logic triggers with the "Ensure logic is still true" checkbox, be aware that the logic will only be true for exactly one day (the day the datediff equals the target value). The alert must be scheduled to send on that same day, or the logic check will return false and cancel it.

> **Pro tip:** Build and validate `datediff` logic in a calculated field first. This lets you see the live numeric output for real records before writing the trigger condition.

> **Note — which alerts REDCap re-checks on its own.** A condition using `"today"` or `"now"` can become true without anyone saving the record. REDCap's scheduled background check picks this up only for **logic triggers** (conditional logic TRUE during data import, data entry, or time-based logic) whose logic uses `datediff` or `dayoftheweek` with `"today"` or `"now"`. A **combination trigger** is evaluated only when its instrument is saved, so a time-based condition in it will not fire on its own. Use a logic trigger for time-based alerts.

## 3.4 Step 1C — Trigger Limits (Longitudinal & Repeated Projects Only)

Step 1C appears only when a project uses longitudinal mode or repeated instruments. It controls how many times per record the alert is allowed to fire.

| Option | Fires | Example Use |
|---|---|---|
| Once per record | At most once across the entire record, regardless of events or repeats | "Thank you for completing the study" email |
| Once per instrument regardless of event | Once per instrument, ignoring which event triggered it | Family medical history confirmation — updates don't re-trigger |
| Once per event per record | Once for each event in which the trigger fires | Visit reminder sent separately for each study visit event |
| Once per event and every repeat instance | Once for each event-instance combination | Serious Adverse Event notification sent for every repeat instance |

> **Note:** The available options in Step 1C depend on which features (longitudinal mode, repeated instruments, repeated events) are enabled in the project. A new alert defaults to once per record. REDCap shows a warning if you combine a logic trigger with a per-instance option, because time-based logic can then fire for every instance of every record.

---

# 4. Alert Schedule

> **Note — unsubscribed participants (REDCap+, 17.3.0+).** Where a project uses the Email Unsubscribe feature, a participant who has unsubscribed will **still have alerts scheduled** for them; REDCap refuses the email at send time instead. The schedule therefore shows sends that will never happen. To prevent scheduling in the first place, add `[email-unsubscribed] = "0"` to the alert's trigger logic. See [RC-PLUS-05 — REDCap+: Email Verification & Unsubscribe](RC-PLUS-05_Email-Verification-and-Unsubscribe.md).

The second step of alert setup defines when the alert is sent after the trigger fires, and how many times it can be sent per trigger.

## 4.1 When to Send the Alert

| Option | Description |
|---|---|
| Immediately | REDCap sends the alert as soon as the trigger fires. |
| Send on next... | Sends on the next occurrence of a specified day type (e.g., next Monday, next weekday) at a specified time. Use when consistent day-of-week timing matters regardless of when the trigger fires. |
| Send after time lapse | Sends after a defined delay (days, hours, minutes, or a combination). The delay can be counted from when the trigger fired, or **before or after a date/date-time field** in the record (e.g. 2 days before `[visit_date]`). A delay of 0 sends immediately. If the chosen date field is blank (or holds a missing-data code), nothing is scheduled. Use for time-horizon alerts such as a 90-day follow-up or an appointment reminder. |
| Send at exact date/time | Sends at a specific future date and time. REDCap uses its server's internal time zone for this option — account for time zone differences when entering the value. |

## 4.2 How Many Times to Send

There are three choices:

**Just once** — the alert sends a single time per trigger event. This is the default and safest choice.

**Every time the form is saved** — available only for the form-based triggers (completion and combination) when the alert sends immediately. A sub-option controls which saves count: any save, only saves that add new or modified data, or saves with new or modified data ignoring changes to calculated fields.

**Multiple times on a recurring basis** — the alert sends repeatedly after the initial send. Requires two additional settings:

- **Send every...** — the time delay between each recurring send (number + unit: days, hours, or minutes; decimals such as 1.5 are accepted).
- **Send up to...** — the total number of sends, including the first (2 to 9999). If left blank, REDCap will continue sending indefinitely. Always set a cap.

> **Important:** Recurring alerts multiply quickly in projects with repeated instruments. An alert set to send 5 times for a repeated instrument with 5 instances will generate 25 total alert sends. Plan repeat counts carefully before enabling.

> **Critical — alerts and ASIs could silently fail to trigger (15.0.35 LTS / 15.5.5 Standard through 15.5.9).** An internal data-caching issue during logic evaluation meant some alerts and ASIs were **not triggered as expected** when a form or survey page was submitted. Fixed in 15.5.10.
>
> This is the hardest class of alert failure to notice: an alert that never fires produces no error, no log entry and no bounce. Nobody reports the email they didn't receive. If an affected version was in use and a study depended on alert delivery, the Notification Log is the place to reconcile expected sends against actual ones — see [RC-ALERT-02 — Alert Management & Notification Log](RC-ALERT-02_Alert-Management-and-Notification-Log.md).

### Pausing Recurrences *(15.4.0+)*

When an alert uses conditional logic with **"Ensure logic is still true..."** checked, a further option appears: **"Allow pausing of recurrences? (Existing interval will continue if the logic becomes true again after becoming false.)"**

The difference this makes:

| Setting | What happens when the logic becomes false |
| --- | --- |
| Unchecked (default) | Already-scheduled recurrences are **deleted** |
| Checked | Already-scheduled recurrences are **paused**, and resume on the existing interval if the logic becomes true again |

Use it where the logic is expected to flip back — time-based conditions using `datediff()` are the typical case, as are alerts tied to a status field that may move back and forth.

> **Version caveat (≤17.2.x Standard; ≤16.0.38 LTS):** On unpausing, REDCap could send **more alerts than expected** — firing at one-minute intervals up to the number that would have been sent had the alert never been paused. From a participant's perspective this is a burst of near-identical emails arriving minutes apart, which is exactly the outcome pausing was meant to avoid. Fixed in 17.3.0 Standard / 16.0.39 LTS. If you are on an affected version, either avoid this option or keep a low "Send up to" cap.

## 4.2a Re-evaluate Send Time *(17.2.0+)*

For Alerts and ASIs scheduled relative to a stored date/time — the **"When to send AFTER conditions are met"** option — REDCap can re-evaluate the scheduled send time whenever that date/time field changes. If a participant's appointment moves, the reminder moves with it, instead of firing against the original date.

Scope, which is narrower than it first appears:

- It applies only to **scheduled but unsent** notifications and invitations.
- **Only the send time changes.** Sender, subject and message content are not re-evaluated.
- For **ASIs with reminders**, if the initial invitation has already gone out, subsequent unsent reminders are **not** rescheduled.

> **Note on defaults:** The option is **off by default** — for new Alerts and ASIs as well as for anything created before the upgrade. If you want a reminder to follow a changed appointment date, tick the checkbox on that alert yourself, and check existing date-relative alerts for whether they have it.

> **Version caveat (16.0 LTS):** Re-evaluate send time is not available in 16.0.61 LTS. On that line a scheduled reminder keeps its original send time when the date field changes; when an appointment moves, check that record's scheduled entry in the Notification Log and correct it by hand, or plan an upgrade to a 17.x line.

> **Version caveat (17.2.0–17.4.0 Standard; ≤17.3.6 LTS):** This feature was unreliable for its entire life before 17.4.1. The checkbox **might not save**, leaving the feature permanently off however many times it was ticked; and where it did work, it could reschedule alerts and invitations **at incorrect times whenever any data was modified** — not only the date field it was supposed to watch. Both fixed in 17.4.1 Standard / 17.3.7 LTS. Separately, the setting's column was missing from the Alerts CSV upload and download files between 17.2.0 and 17.3.0 (fixed 17.3.1), so bulk-managed alerts could not carry it. **Treat this feature as requiring 17.4.1 / 17.3.7 or later.**

> **Version caveat (below 17.5.1 Standard / 17.3.14 LTS):** Alerts with **scheduled send times** could be **re-sent several times** after a server restart or a REDCap upgrade, because duplicate recurrence entries were created in the backend tables. If recipients reported duplicate alerts around an upgrade on an older instance, this is the cause; check the Notification Log for repeated sends to the same record.

## 4.3 Alert Expiration (Optional)

Set a hard expiration date and time. At that point REDCap deactivates the alert, so nothing further is sent from it. Already-scheduled entries are not deleted from the queue; if you re-activate the alert later, check the Notification Log first, because overdue entries may then go out. Useful for studies with a defined end date, ensuring no alerts send after the study closes.

---

# 5. Message Settings

The third step defines what the alert sends and to whom.

## 5.1 Alert Type

Select the message delivery method. The available options depend on your REDCap installation:

- **Email** (always available)
- SMS Text Message (if enabled — via Twilio or Mosio)
- Voice Call (if enabled — Twilio only)
- SendGrid (if configured)

This article covers email only. SMS, Voice Call, and SendGrid delivery are covered in RC-ALERT-03 — Alternative Alert Delivery Types *(coming soon)*.

## 5.2 From Email

Select a "from" address from the dropdown. The dropdown is populated with the verified primary, secondary and tertiary email addresses of current project users (each user may have up to 3 emails linked to their profile via My Profile). If an alert carries a From address that does not belong to a project user (for example after a CSV upload or project copy), REDCap replaces it with the email of the person saving the alert, without warning — check the From address after uploading or copying alerts.

Best practices:
- Use a study-specific or team email rather than a personal address. This ensures continuity if the individual leaves the project.
- If you need to use a non-institutional email domain (e.g., a Gmail address), confirm with your REDCap administrator that the domain is permitted. Unrecognized sender domains may be blocked by recipient spam filters.

If your administrator has enabled it, you may optionally set a **display name** for the from address (e.g., "Heart Congestion Study 2024" for `hs24@institution.edu`). Test display names with a test participant — some spam filters flag unfamiliar display names.

## 5.3 To, CC, and BCC

REDCap supports standard To, Carbon Copy (CC), and Blind Carbon Copy (BCC) fields. CC and BCC are hidden by default; select **+ Show more options** to reveal them. All three fields work identically.

There are several ways to specify recipients:

**User emails** — select any email linked to a current project user from the "select recipients" dropdown. Open the dropdown again to add additional users. Best for alerts sent to study team members.

**Variables** — any text field with email validation in your project appears in the dropdown below user emails. Selecting a variable dynamically resolves to that record's email value at send time. Best for alerts sent to participants. In longitudinal projects, use event-prefixed piping syntax in the CSV (e.g., `[baseline_arm_1][contact_email]`) to pull the email from a specific event — this is required if the same field appears in multiple events and you need a specific event's value. In the GUI recipient dropdown, longitudinal projects list each email variable as **[Current Event]** (the event that triggered the alert) plus one entry per event.

**Survey Participant** — sends to the participant's email address as REDCap knows it for surveys (for example from the participant list or the project's designated email field).

**Manual entry** — type one or more email addresses directly into the "Or manually enter emails" field. Separate multiple addresses with a semicolon (commas are also accepted). Any valid email address is accepted, including addresses not associated with any project user. If your administrator does not allow free-form addresses, this box is not shown.

> **Version caveat (17.6+ Standard; not in 17.3 LTS or 16.0 LTS):** Alerts can also be sent to **user roles** or to all project users, optionally limited by Data Access Group. When roles are used, REDCap sends an individual email to every recipient rather than one shared message, and CC/BCC are not used. On LTS instances, select the users individually instead.

**Email failure notification:** Select a user email to receive a notification if REDCap fails to deliver the alert. Only one address is allowed for this field.

## 5.4 Subject Line

Type a subject directly, or pipe in variable values. Avoid piping sensitive or identifying information into the subject line — email subjects are visible in many clients before the message is opened and may appear in notification previews. See [RC-PIPE-01 — Piping: Basics, Syntax & Field Types](RC-PIPE-01_Piping-Basics-Syntax-and-Field-Types.md) for piping syntax.

## 5.5 Message Body

The message body supports:

- **Plain text and rich text formatting** via the built-in rich text editor (comparable to a basic word processor).
- **HTML and inline images** for custom layout.

> **Version caveat (17.5.1–17.5.3 Standard):** Images embedded through the rich text editor arrived as **broken images** in the recipient's email — for alerts, ASIs and other outgoing messages. Fixed in 17.5.4. The LTS line was not affected.
- **Piped variables** — any project variable can be inserted using standard piping syntax. See [RC-PIPE-01 — Piping: Basics, Syntax & Field Types](RC-PIPE-01_Piping-Basics-Syntax-and-Field-Types.md) and [RC-PIPE-04 — Piping: Emails, Notifications & Logic Features](RC-PIPE-04_Piping-in-Emails-and-Notifications.md) for full reference.
- **Smart variables** — REDCap-specific tokens that resolve to dynamic links and values at send time. Access them via the green **Smart Variables** button below the message body.

> **Important:** If you pipe a field designated as an Identifier in the project, you must **uncheck** the "Prevent piping of data for Identifier fields" checkbox that appears in the alert setup (it is checked by default on a new alert). If this box remains checked, REDCap will send the alert but will replace each Identifier field's value in the subject and message with the text **[\*DATA REMOVED\*]**. The setting does not affect recipient fields, so an email variable marked as Identifier still works as a recipient. Fields not marked as Identifier pipe normally either way.

Unlike Automated Survey Invitations (which pre-fill the message body with stock text and survey link tokens), alert message bodies start blank. REDCap does not know what kind of message you intend to send.

**Commonly used smart variables in alert messages:**

| Smart Variable | What It Produces |
|---|---|
| `[survey-link:instrument_name]` | A clickable hyperlink to the named survey, using the survey name as link text. Specify the instrument name because alerts are not tied to a default survey. |
| `[survey-link:instrument_name:Custom text]` | Same as above, but with custom display text. The third colon-delimited segment replaces the default link label (e.g., `[survey-link:phq9:Click here to start]`). |
| `[survey-url:instrument_name]` | The raw URL to the named survey (not a styled hyperlink). |
| `[survey-queue-link]` | A clickable hyperlink to the survey queue for the record that triggered the alert. No instrument name needed — each record has one queue. |
| `[survey-queue-url]` | The raw URL to that record's survey queue (not a styled hyperlink). |
| `[form-link:instrument_name]` | A clickable link that opens the named instrument directly in REDCap's data entry interface (not as a survey). Useful for staff notification alerts. |

For a complete smart variable reference, see [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md).

## 5.6 Attachments

Select the green **Add Attachments** button at the bottom of the message panel.

**File upload fields** — select one or more file upload fields from your project. If a record has a file in that field when the alert fires, REDCap attaches that file to the email. Common uses: attaching a completed e-consent PDF or supporting documents to a confirmation or notification email.

**Direct attachments** — upload a file that will be attached to every alert instance regardless of record. Up to 5 files allowed. Best for static documents like study flyers or protocol summaries.

> **Note:** REDCap limits each attachment to 20 MB. An attachment over the limit is dropped: the alert is still sent without it, and the failure-notification address (if set) is told. Recipients' email providers may enforce lower limits (typically 10–25 MB in total). For large files, consider using piping to link to the file instead of attaching it directly. For example, `[protocol_pdf:link]` produces a clickable download link for a file stored in a file upload field. Recipients select the link to download rather than receiving the file as an attachment.

---

# 6. Common Questions

**Q: What is the difference between an Alert & Notification and an Automated Survey Invitation (ASI)?**

**A:** ASIs can only trigger when a survey is completed, and they can only send to the survey participant. Alerts can trigger on any instrument save (form or survey) or on any logic condition, and they can send to any combination of project users, participant email variables, and manually entered addresses. Alerts also support CC and BCC. For any scenario that requires multiple recipients or non-survey triggers, use an alert.

**Q: Will an alert fire if data is uploaded via the Data Import tool or the API?**

**A:** It depends on the trigger type. Completion triggers and combination triggers do not fire on import or API writes — they only respond to direct data entry and survey completion events. Logic triggers do fire when import or API writes cause a logic condition to become true.

**Q: Can I use branching logic syntax in an alert trigger?**

**A:** Yes. The alert logic editor uses the same syntax as branching logic. Any valid branching logic expression is valid as an alert trigger condition. If you are new to logic syntax, review [RC-BL-01 — Branching Logic: Overview & Scope](RC-BL-01_Branching-Logic-Overview-and-Scope.md) and [RC-BL-02 — Branching Logic: Syntax & Atomic Statements](RC-BL-02_Branching-Logic-Syntax-and-Atomic-Statements.md)

**Q: What does the "Ensure logic is still true" checkbox do, and when should I use it?**

**A:** When enabled, REDCap checks whether the trigger logic is still true immediately before sending the alert, and again whenever the record is saved or imported while the alert is waiting. If the logic is false, REDCap cancels that alert instance. Use this option whenever your alert has a scheduled delay or recurs — especially for time-sensitive reminders or follow-ups where participant status may change between the trigger event and the send date.

**Q: My alert fires for date-based logic, but the datediff condition is only true for one day. Will the "Ensure logic is still true" checkbox cause REDCap to cancel it?**

**A:** Yes, if the alert is not sent on the same day the condition becomes true. If `datediff("today", [visit_date], "d", true) = "14"` is only true on one specific calendar day, the alert must be sent that day. Keep the "Ensure logic" checkbox ticked — it is what stops sends once the condition no longer holds (for example, the visit date changes or the participant withdraws) — and schedule the send for immediately or later the same day. If you want the email to go out on a different day, change the number in the logic to match the send day rather than adding a delay.

**Q: Can I send an alert to someone who is not a project user?**

**A:** Yes. Use the manual entry option in the To field to type any valid email address. That address does not need to be associated with any REDCap account or project role.

**Q: Can I pipe an identifier field value (like a participant's first name) into an alert message?**

**A:** Yes, but you must uncheck the "Prevent piping of data for Identifier fields" checkbox in the alert setup. If the checkbox remains checked, the piped value will be silently removed from the sent message.

**Q: How do I include a survey link in an alert?**

**A:** Use the `[survey-link:instrument_name]` smart variable, where `instrument_name` is the REDCap variable name of the instrument (not its display label). Unlike ASIs, alerts are not pre-associated with a specific survey, so you must specify the instrument name explicitly.

**Q: Can I customize the link text for a survey link in an alert?**

**A:** Yes. Add a third colon-delimited segment to the smart variable: `[survey-link:instrument_name:Link text]`. For example, `[survey-link:phq9:Start here]` produces a hyperlink that says "Start here" and opens the PHQ-9 survey. In longitudinal projects, prefix with the event name: `[baseline_arm_1][survey-link:demographics:Start here]`.

**Q: How do I include a survey link that goes to a specific event in a longitudinal project?**

**A:** Prefix the smart variable with the event's unique name in brackets: `[event_name][survey-link:instrument_name]`. For example, `[3_month_arm_1][survey-link:phq9:Start here]` generates a link to the PHQ-9 instrument at the 3-month event. Without the event prefix, REDCap may not resolve the link correctly if the instrument exists at multiple events.

**Q: Will alerts fire when a project is in draft/development mode?**

**A:** Yes. Active alerts trigger and send in **Development** status exactly as they do in **Production**. They stop only when the project is in **Analysis/Cleanup** or **Completed** status (or deleted). While developing, use test records and your own or a team test email address as recipients, so no real participant receives a test message. Before moving to production, review every alert's recipients, logic and schedule, and check the Notification Log for test entries still waiting to send.

---

# 7. Common Mistakes & Gotchas

**Using a completion trigger when data comes in via import or API.** Completion triggers only fire on direct data entry and survey completion events. If your workflow loads data via the Data Import tool or the REDCap API, a completion trigger will never fire. Use a logic trigger instead, since logic triggers evaluate on all write methods.

**Not setting a repeat cap on recurring alerts.** If "Send how many times" is set to "Multiple times on a recurring basis" and the "Send up to" field is left blank, REDCap sends the alert indefinitely. In projects with repeated instruments, this can generate an extremely large number of alert sends. Always set a numeric cap.

**Forgetting the instrument name in survey smart variables.** Unlike ASIs — which are pre-linked to a single survey — alerts require you to specify the instrument name inside the smart variable token. Writing `[survey-link]` without the instrument name will not produce a working link, and REDCap will not let you save the alert with it. The correct format is `[survey-link:instrument_name]`.

**Using a personal email address as the "from" address.** If the team member whose email is used leaves the project, the alert may fail or generate confusion for recipients. Use a study-specific or shared team email as the from address whenever possible.

**Leaving the "Prevent piping of identifier fields" checkbox checked when piping identifiers.** When this box is checked (the default), REDCap strips identifier field values from the subject and message without warning. The alert sends successfully — but with **[\*DATA REMOVED\*]** where names or other identifiers should appear. Uncheck the box if identifier piping is intentional, and verify with your IRB that including identifiers in email is appropriate for your study.

**Using `[survey-link:instrument_name]` without an event prefix in a longitudinal project.** If the instrument appears at multiple events, REDCap may not know which event's link to generate, resulting in a broken or incorrect link. In longitudinal alerts, always prefix with the target event: `[event_name][survey-link:instrument_name]`. When constructing this in the CSV, this goes directly in the `alert-message` field as part of the HTML body.

**Scheduling a delayed alert with date-based datediff logic without the "Ensure logic is still true" checkbox.** If the trigger fires and the alert is delayed, the datediff condition may no longer be true at send time (it was only true on one day). Always pair time-based datediff logic with the "Ensure logic is still true" option, and schedule the send for the same day the condition becomes true.

---

# 8. Administrator Configuration

Several Alerts & Notifications behaviors are controlled by system-level settings in the Control Center (see **[RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md)** — Control Center: Modules & Services Configuration, Alerts & Notifications Settings section):

- **Allow normal users to use project variables for email fields** — Controls whether the To/CC/BCC recipient fields can reference project fields containing email addresses. If this is disabled at the system level, dynamic email routing via project fields is unavailable to project users.
- **Allow normal users to manually enter freeform email addresses** — Controls whether free-text email entry is permitted in recipient fields. Administrators can further restrict this by domain allowlist.
- **Domain allowlist for freeform email entry** — If set, only email addresses at approved domains can be entered manually.
- **Universal DO-NOT-REPLY Email Address** *(15.4.0+)* — Set on the General Configuration page rather than Modules/Services. When configured, REDCap uses it as both the **From** and **Reply-To** address for automated emails that originate from the system rather than a person. Without it, replies to automated mail land in the catch-all administrator mailbox, which is where most "why am I getting this?" replies end up. See [RC-CC-02 — Control Center: General System Configuration](RC-CC-02_Control-Center-General-Configuration.md).

> **Version caveat (≤15.7.4):** The Universal DO-NOT-REPLY address was **not** applied to the automated email a participant receives after selecting **Save & Return Later** on a survey — that message still went out from the previous From address. Fixed in 15.7.5. Worth knowing if participants on an older instance report replying to a survey email and reaching a mailbox nobody monitors.
- **Allow normal users to use project variables for phone fields** — Controls whether phone number fields for SMS alerts can reference project data fields.
- **Allow normal users to enter freeform phone numbers** — Controls whether manual phone number entry is permitted for SMS alerts.

If you find that certain recipient options are unavailable in your alert configuration (e.g., the "Or manually enter emails" box is not shown), a system-level restriction is likely in place. Contact your REDCap administrator.

> **See also:** [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md)

---

# 9. Bulk Management via CSV

REDCap allows you to export and import all alert definitions for a project as a CSV file. This is the fastest way to copy a full alert configuration from one project to another (with the ID column cleared — see Import below), or to make batch edits (e.g., updating subject lines, swapping a from address, or adjusting time lags across many alerts at once) outside of the REDCap interface.

**Location:** Applications → Alerts & Notifications → "Upload or download alerts" button.

**Export:** Downloads a CSV file containing every alert in the project. Each row is one alert. Use this file as a starting template for new alerts, or import it into a different project to replicate the configuration.

**Import:** Upload a CSV in the same format. What happens to each row depends on its **Unique Alert ID** column:

- **ID of an existing alert in this project** — that alert is **updated** with the row's values.
- **Blank ID** — a new alert is created and added at the end of the list.
- **ID from another project** — the row is rejected with an error.

The upload cannot delete or reorder alerts. **To copy alerts into another project**, export them, clear the Unique Alert ID column, and upload the file in the target project. Check the From addresses afterwards (see §5.2).

**Rights required:** Alerts & Notifications.

**Starting a file from scratch:** Always start from an exported file rather than building the column headers by hand — the column order and required JSON fields (`sendgrid-template-data`, `sendgrid-mail-send-configuration`) are easy to get wrong. Export even a single placeholder alert to get the correct structure.

For the full column-by-column reference, accepted values, an annotated example, and common mistakes, see **[RC-IMP-05 — Alerts & Notifications CSV — Column Reference and Format Guide](RC-IMP-05_Alerts-Notifications-CSV.md) — Alerts & Notifications CSV**.

---

# 10. Related Articles

- [RC-ALERT-02 — Alert Management & Notification Log](RC-ALERT-02_Alert-Management-and-Notification-Log.md) (managing multiple alerts, using the notification log)
- [RC-PIPE-01 — Piping: Basics, Syntax & Field Types](RC-PIPE-01_Piping-Basics-Syntax-and-Field-Types.md) (piping syntax used in alert subjects and message bodies)
- [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md) (full reference for smart variables usable in alert messages)
- [RC-PIPE-04 — Piping: Emails, Notifications & Logic Features](RC-PIPE-04_Piping-in-Emails-and-Notifications.md) (advanced piping in email contexts)
- [RC-BL-01 — Branching Logic: Overview & Scope](RC-BL-01_Branching-Logic-Overview-and-Scope.md) (prerequisite for writing logic triggers)
- [RC-BL-02 — Branching Logic: Syntax & Atomic Statements](RC-BL-02_Branching-Logic-Syntax-and-Atomic-Statements.md) (logic syntax reference)
- [RC-CALC-01 — Special Functions Reference](RC-CALC-01_Special-Functions-Reference.md) (full `datediff` signature and the other functions usable in trigger logic)
- [RC-SURV-01 — Surveys – Basics](RC-SURV-01_Surveys-Basics.md) (survey fundamentals; alerts can send survey invitations)
- [RC-SURV-02 — Survey Settings: Basic Options & Design](RC-SURV-02_Survey-Settings-Basic-Options-and-Design.md) (Survey Notifications feature — simple per-survey email alerts without custom logic)
- [RC-LONG-02 — Repeated Instruments & Events Setup](RC-LONG-02_Repeated-Instruments-and-Events-Setup.md) (context for trigger limits in Step 1C)
- [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md) (system-level recipient field permissions for alerts)
