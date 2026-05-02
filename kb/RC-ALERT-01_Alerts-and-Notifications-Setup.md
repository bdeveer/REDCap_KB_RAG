RC-ALERT-01

**Alerts & Notifications — Setup**

| **Article ID** | RC-ALERT-01 |
| --- | --- |
| **Domain** | Alerts & Notifications |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Prerequisite** | RC-PIPE-01 — Piping: Basics, Syntax & Field Types |
| **Version** | 1.2 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-PIPE-01 — Piping: Basics, Syntax & Field Types; RC-PIPE-03 — Smart Variables Overview; RC-PIPE-04 — Piping: Emails, Notifications & Logic Features; RC-BL-01 — Branching Logic: Overview & Scope; RC-SURV-01 — Surveys – Basics; RC-ALERT-02 — Alert Management & Notification Log; RC-CC-06 — Control Center: Modules & Services Configuration |

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
An optional date and time after which REDCap will not send any further alerts, and will cancel any already-scheduled ones.

**datediff**
A REDCap logic function that compares two dates or date-times and returns the numeric difference in a specified unit (days, hours, minutes, etc.). Commonly used to build time-based trigger logic for alerts.

**Smart Variable**
A special REDCap token that resolves to a dynamic value at send time, such as a survey link, a form link, or a survey queue URL. Smart variables are inserted into alert messages using bracket notation (e.g., `[survey-link:instrument_name]`).

**Ensure Logic is Still True**
An optional checkbox in the alert trigger setup. When enabled, REDCap re-evaluates the trigger logic immediately before sending the alert. If the logic is no longer true at send time, REDCap cancels that scheduled alert.

---

# 3. Alert Triggers

Navigate to **Alerts & Notifications** in the project Applications menu. Click **+ Add New Alert** to open the alert creation dialog.

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

Select the instrument from the dropdown. In longitudinal projects, the dropdown shows instrument-event combinations rather than instruments alone.

Then select a form status requirement:

- **"Is saved with any form status"** — fires the moment the instrument is saved, regardless of completion status.
- **"Is saved with Complete status only"** — fires only when the instrument's completion status is set to Complete (status value 2). Surveys completed by participants receive this status automatically. Partially saved surveys are excluded.

**For combination triggers and logic triggers:**

Enter a logic statement in the logic editor. The editor is the same interface used for branching logic. If you are unfamiliar with logic syntax, see RC-BL-01 — Branching Logic: Overview & Scope.

The logic evaluates at the record level. You cannot write logic that counts records across the entire project (e.g., "trigger if 20 survey responses have arrived"). All logic must reference variables within a single record.

**The "Ensure logic is still true before sending" checkbox**

This checkbox appears beneath the logic editor for combination and logic triggers. When checked, REDCap re-evaluates the logic condition immediately before sending the alert. If the condition is no longer true at send time, REDCap cancels that queued alert instance.

This option is most valuable when the alert schedule includes a time delay. Example: an alert set to send a clinic visit reminder 14 days before the visit date should check at send time whether the participant is still enrolled. Without this check, a participant who has withdrawn would still receive the reminder.

> **Note:** If the alert is set to send immediately (no delay), the "ensure logic" check has no practical effect — the alert fires and sends in the same moment.

## 3.3 Step 1B Sidebar — Date/Time Logic with datediff

To trigger an alert based on a date or date-time value, use the `datediff` function. This function compares two dates and returns the numeric difference in a specified time unit.

Basic syntax:

```
datediff(date1, date2, "unit")
```

Units: `"d"` (days), `"h"` (hours), `"m"` (minutes), `"M"` (months), `"y"` (years).

**Static comparison:**
```
datediff("01/01/2025", "01/07/2025", "d")
```
Returns `7`. The result never changes because both dates are hard-coded.

**Dynamic comparison using "today":**
```
datediff("01/01/2025", "today", "d")
```
Returns the number of days since January 1, 2025, and increases by 1 each day.

**Dynamic comparison using a record variable:**
```
datediff([visit_date], "today", "d") = "-14"
```
Becomes true when today's date is exactly 14 days before the value in `[visit_date]`. Use this pattern to trigger alerts a fixed number of days before a date stored in the record.

> **Important:** When using date-based logic triggers with the "Ensure logic is still true" checkbox, be aware that the logic will only be true for exactly one day (the day the datediff equals the target value). The alert must be scheduled to send on that same day, or the logic check will return false and cancel it.

> **Pro tip:** Build and validate `datediff` logic in a calculated field first. This lets you see the live numeric output for real records before writing the trigger condition.

## 3.4 Step 1C — Trigger Limits (Longitudinal & Repeated Projects Only)

Step 1C appears only when a project uses longitudinal mode or repeated instruments. It controls how many times per record the alert is allowed to fire.

| Option | Fires | Example Use |
|---|---|---|
| Once per record | At most once across the entire record, regardless of events or repeats | "Thank you for completing the study" email |
| Once per instrument regardless of event | Once per instrument, ignoring which event triggered it | Family medical history confirmation — updates don't re-trigger |
| Once per event per record | Once for each event in which the trigger fires | Visit reminder sent separately for each study visit event |
| Once per event and every repeat instance | Once for each event-instance combination | Serious Adverse Event notification sent for every repeat instance |

> **Note:** The available options in Step 1C depend on which features (longitudinal mode, repeated instruments, repeated events) are enabled in the project.

---

# 4. Alert Schedule

The second step of alert setup defines when the alert is sent after the trigger fires, and how many times it can be sent per trigger.

## 4.1 When to Send the Alert

| Option | Description |
|---|---|
| Immediately | REDCap sends the alert as soon as the trigger fires. |
| Send on next... | Sends on the next occurrence of a specified day type (e.g., next Monday, next weekday) at a specified time. Use when consistent day-of-week timing matters regardless of when the trigger fires. |
| Send after time lapse | Sends after a defined delay (days, hours, minutes, or a combination). Use for time-horizon alerts such as a 90-day follow-up. |
| Send at exact date/time | Sends at a specific future date and time. REDCap uses its server's internal time zone for this option — account for time zone differences when entering the value. |

## 4.2 How Many Times to Send

**Just once** — the alert sends a single time per trigger event. This is the default and safest choice.

**Multiple times on a recurring basis** — the alert sends repeatedly after the initial send. Requires two additional settings:

- **Send every...** — the time delay between each recurring send (number + unit: days, hours, or minutes).
- **Send up to...** — the total number of sends, including the first. If left blank, REDCap will continue sending indefinitely. Always set a cap.

> **Important:** Recurring alerts multiply quickly in projects with repeated instruments. An alert set to send 5 times for a repeated instrument with 5 instances will generate 25 total alert sends. Plan repeat counts carefully before enabling.

## 4.3 Alert Expiration (Optional)

Set a hard expiration date and time. After this point, REDCap will not send any further alerts from this configuration and will cancel any queued instances. Useful for studies with a defined end date, ensuring no alerts send after the study closes.

---

# 5. Message Settings

The third step defines what the alert sends and to whom.

## 5.1 Alert Type

Select the message delivery method. The available options depend on your REDCap installation:

- **Email** (always available)
- SMS Text Message (if enabled)
- Voice Call (if enabled)
- SendGrid (if configured)

This article covers email only. SMS, Voice Call, and SendGrid delivery are covered in RC-ALERT-03 — Alternative Alert Delivery Types *(coming soon)*.

## 5.2 From Email

Select a "from" address from the dropdown. The dropdown is populated with email addresses associated with all current project users (each user may have up to 3 emails linked to their profile via My Profile).

Best practices:
- Use a study-specific or team email rather than a personal address. This ensures continuity if the individual leaves the project.
- If you need to use a non-institutional email domain (e.g., a Gmail address), confirm with your REDCap administrator that the domain is permitted. Unrecognized sender domains may be blocked by recipient spam filters.

You may optionally set a **display name** for the from address (e.g., "Heart Congestion Study 2024" for `hs24@institution.edu`). Test display names with a test participant — some spam filters flag unfamiliar display names.

## 5.3 To, CC, and BCC

REDCap supports standard To, Carbon Copy (CC), and Blind Carbon Copy (BCC) fields. CC and BCC are hidden by default; click **+ Show more options** to reveal them. All three fields work identically.

There are three ways to specify recipients:

**User emails** — select any email linked to a current project user from the "select recipients" dropdown. Click the dropdown again to add additional users. Best for alerts sent to study team members.

**Variables** — any text field with email validation in your project appears in the dropdown below user emails. Selecting a variable dynamically resolves to that record's email value at send time. Best for alerts sent to participants. In longitudinal projects, use event-prefixed piping syntax in the CSV (e.g., `[baseline_arm_1][contact_email]`) to pull the email from a specific event — this is required if the same field appears in multiple events and you need a specific event's value. The GUI recipient dropdown typically handles this automatically based on the triggering event.

**Manual entry** — type one or more email addresses directly into the "Or manually enter emails" field. Separate multiple addresses with a semicolon. Any valid email address is accepted, including addresses not associated with any project user.

**Email failure notification:** Select a user email to receive a notification if REDCap fails to deliver the alert. Only one address is allowed for this field.

## 5.4 Subject Line

Type a subject directly, or pipe in variable values. Avoid piping sensitive or identifying information into the subject line — email subjects are visible in many clients before the message is opened and may appear in notification previews. See RC-PIPE-01 for piping syntax.

## 5.5 Message Body

The message body supports:

- **Plain text and rich text formatting** via the built-in rich text editor (comparable to a basic word processor).
- **HTML and inline images** for custom layout.
- **Piped variables** — any project variable can be inserted using standard piping syntax. See RC-PIPE-01 and RC-PIPE-04 for full reference.
- **Smart variables** — REDCap-specific tokens that resolve to dynamic links and values at send time. Access them via the green **Smart Variables** button below the message body.

> **Important:** If you pipe a field designated as an Identifier in the project, you must **uncheck** the "Prevent piping of data for Identifier fields" checkbox that appears in the alert setup. If this box remains checked, REDCap will send the alert but will strip the identifier value from the message, resulting in blank placeholders.

Unlike Automated Survey Invitations (which pre-fill the message body with stock text and survey link tokens), alert message bodies start blank. REDCap does not know what kind of message you intend to send.

**Commonly used smart variables in alert messages:**

| Smart Variable | What It Produces |
|---|---|
| `[survey-link:instrument_name]` | A clickable hyperlink to the named survey, using the survey name as link text. Specify the instrument name because alerts are not tied to a default survey. |
| `[survey-link:instrument_name:Custom text]` | Same as above, but with custom display text. The third colon-delimited segment replaces the default link label (e.g., `[survey-link:phq9:Click here to start]`). |
| `[survey-url:instrument_name]` | The raw URL to the named survey (not a styled hyperlink). |
| `[survey-queue-url]` | A clickable hyperlink to the survey queue for the record that triggered the alert. No instrument name needed — each record has one queue. |
| `[form-link:instrument_name]` | A clickable link that opens the named instrument directly in REDCap's data entry interface (not as a survey). Useful for staff notification alerts. |

For a complete smart variable reference, see RC-PIPE-03 — Smart Variables Overview.

## 5.6 Attachments

Click the green **Add Attachments** button at the bottom of the message panel.

**File upload fields** — select one or more file upload fields from your project. If a record has a file in that field when the alert fires, REDCap attaches that file to the email. Common uses: attaching a completed e-consent PDF or supporting documents to a confirmation or notification email.

**Direct attachments** — upload a file that will be attached to every alert instance regardless of record. Up to 5 files allowed. Best for static documents like study flyers or protocol summaries.

> **Note:** Most email providers enforce a maximum attachment size (typically 10–25 MB). For large files, consider using piping to link to the file instead of attaching it directly. For example, `[protocol_pdf:link]` produces a clickable download link for a file stored in a file upload field. Recipients click to download rather than receiving the file as an attachment.

---

# 6. Common Questions

**Q: What is the difference between an Alert & Notification and an Automated Survey Invitation (ASI)?**

**A:** ASIs can only trigger when a survey is completed, and they can only send to the survey participant. Alerts can trigger on any instrument save (form or survey) or on any logic condition, and they can send to any combination of project users, participant email variables, and manually entered addresses. Alerts also support CC and BCC. For any scenario that requires multiple recipients or non-survey triggers, use an alert.

**Q: Will an alert fire if data is uploaded via the Data Import tool or the API?**

**A:** It depends on the trigger type. Completion triggers and combination triggers do not fire on import or API writes — they only respond to direct data entry and survey completion events. Logic triggers do fire when import or API writes cause a logic condition to become true.

**Q: Can I use branching logic syntax in an alert trigger?**

**A:** Yes. The alert logic editor uses the same syntax as branching logic. Any valid branching logic expression is valid as an alert trigger condition. If you are new to logic syntax, review RC-BL-01 — Branching Logic: Overview & Scope and RC-BL-02 — Syntax & Atomic Statements.

**Q: What does the "Ensure logic is still true" checkbox do, and when should I use it?**

**A:** When enabled, REDCap checks whether the trigger logic is still true immediately before sending the alert. If the logic is false at send time, REDCap cancels that alert instance. Use this option whenever your alert has a scheduled delay — especially for time-sensitive reminders or follow-ups where participant status may change between the trigger event and the send date.

**Q: My alert fires for date-based logic, but the datediff condition is only true for one day. Will the "Ensure logic is still true" checkbox cause REDCap to cancel it?**

**A:** Yes, if the alert is not sent on the same day the condition becomes true. If `datediff([visit_date], "today", "d") = "-14"` is only true on one specific calendar day, the alert must be sent that day. Schedule the alert for immediate send, or do not use the "Ensure logic" checkbox for this pattern.

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

**A:** No. Alerts only fire once a project has been moved to **Production status**. Projects in draft mode can have fully configured alerts, but they remain inactive and will not trigger or send until the project status is changed to production. This prevents unwanted alert sends during the design and testing phases of project development. To move a project to production, a user with Project Design and Setup rights must access the Project Home page and change the project status.

---

# 7. Common Mistakes & Gotchas

**Using a completion trigger when data comes in via import or API.** Completion triggers only fire on direct data entry and survey completion events. If your workflow loads data via the Data Import tool or the REDCap API, a completion trigger will never fire. Use a logic trigger instead, since logic triggers evaluate on all write methods.

**Not setting a repeat cap on recurring alerts.** If "Send how many times" is set to "Multiple times on a recurring basis" and the "Send up to" field is left blank, REDCap sends the alert indefinitely. In projects with repeated instruments, this can generate an extremely large number of alert sends. Always set a numeric cap.

**Forgetting the instrument name in survey smart variables.** Unlike ASIs — which are pre-linked to a single survey — alerts require you to specify the instrument name inside the smart variable token. Writing `[survey-link]` without the instrument name will not produce a working link. The correct format is `[survey-link:instrument_name]`.

**Using a personal email address as the "from" address.** If the team member whose email is used leaves the project, the alert may fail or generate confusion for recipients. Use a study-specific or shared team email as the from address whenever possible.

**Leaving the "Prevent piping of identifier fields" checkbox checked when piping identifiers.** When this box is checked (the default), REDCap strips identifier field values from the sent message without warning. The alert sends successfully — but with blank spaces where names or other identifiers should appear. Uncheck the box if identifier piping is intentional, and verify with your IRB that including identifiers in email is appropriate for your study.

**Using `[survey-link:instrument_name]` without an event prefix in a longitudinal project.** If the instrument appears at multiple events, REDCap may not know which event's link to generate, resulting in a broken or incorrect link. In longitudinal alerts, always prefix with the target event: `[event_name][survey-link:instrument_name]`. When constructing this in the CSV, this goes directly in the `alert-message` field as part of the HTML body.

**Scheduling a delayed alert with date-based datediff logic without the "Ensure logic is still true" checkbox.** If the trigger fires and the alert is delayed, the datediff condition may no longer be true at send time (it was only true on one day). Always pair time-based datediff logic with the "Ensure logic is still true" option, and schedule the send for the same day the condition becomes true.

---

# 8. Administrator Configuration

Several Alerts & Notifications behaviors are controlled by system-level settings in the Control Center (see **RC-CC-06** — Control Center: Modules & Services Configuration, Alerts & Notifications Settings section):

- **Allow normal users to use project variables for email fields** — Controls whether the To/CC/BCC recipient fields can reference project fields containing email addresses. If this is disabled at the system level, dynamic email routing via project fields is unavailable to project users.
- **Allow normal users to manually enter freeform email addresses** — Controls whether free-text email entry is permitted in recipient fields. Administrators can further restrict this by domain allowlist.
- **Domain allowlist for freeform email entry** — If set, only email addresses at approved domains can be entered manually.
- **Allow normal users to use project variables for phone fields** — Controls whether phone number fields for SMS alerts can reference project data fields.
- **Allow normal users to enter freeform phone numbers** — Controls whether manual phone number entry is permitted for SMS alerts.

If you find that certain recipient options are unavailable in your alert configuration (e.g., the "enter email address" option is greyed out), a system-level restriction is likely in place. Contact your REDCap administrator.

> **See also:** RC-CC-06 — Control Center: Modules & Services Configuration

---

# 9. Related Articles

- RC-ALERT-02 — Alert Management & Notification Log (managing multiple alerts, using the notification log)
- RC-PIPE-01 — Piping: Basics, Syntax & Field Types (piping syntax used in alert subjects and message bodies)
- RC-PIPE-03 — Smart Variables Overview (full reference for smart variables usable in alert messages)
- RC-PIPE-04 — Piping: Emails, Notifications & Logic Features (advanced piping in email contexts)
- RC-BL-01 — Branching Logic: Overview & Scope (prerequisite for writing logic triggers)
- RC-BL-02 — Branching Logic: Syntax & Atomic Statements (logic syntax reference)
- RC-SURV-01 — Surveys – Basics (survey fundamentals; alerts can send survey invitations)
- RC-SURV-02 — Survey Settings: Basic Options & Design (Survey Notifications feature — simple per-survey email alerts without custom logic)
- RC-LONG-02 — Repeated Instruments & Events Setup (context for trigger limits in Step 1C)
- RC-CC-06 — Control Center: Modules & Services Configuration (system-level recipient field permissions for alerts)
