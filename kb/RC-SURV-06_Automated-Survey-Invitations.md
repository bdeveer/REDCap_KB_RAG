RC-SURV-06

**Surveys — Automated Survey Invitations (ASI)**

| **Article ID** | RC-SURV-06 |
|---|---|
| **Domain** | Surveys |
| **Applies To** | All projects with surveys enabled |
| **Prerequisite** | RC-SURV-05 — Participant List & Manual Survey Invitations |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-SURV-05 — Participant List & Manual Survey Invitations; RC-SURV-07 — Survey Queue; RC-BL-01 — Branching Logic: Overview & Scope; RC-BL-02 — Branching Logic: Syntax & Atomic Statements; RC-PIPE-01 — Piping: Basics, Syntax & Field Types; RC-PIPE-03 — Smart Variables Overview |

---

# 1. Overview

This article covers Automated Survey Invitations (ASIs) — REDCap's mechanism for automatically scheduling and sending survey invitation emails based on defined trigger conditions and time delay settings. ASIs are the standard tool for distributing follow-up surveys without manual intervention. This article explains the ASI setup screen, the three trigger types, time delay options, reminders, and how to manage ASIs across a project's lifetime. This article is part of the Surveys knowledge base series.

---

# 2. Key Concepts & Definitions

**Automated Survey Invitation (ASI)**

A configured rule that tells REDCap to automatically schedule a survey invitation email when specified conditions are met. Each survey can have one ASI configured. In longitudinal projects, each survey-event combination can have its own ASI.

**Completion Trigger**

An ASI trigger condition that fires when a specified survey is marked as completed.

**Logic Trigger**

An ASI trigger condition that fires when a specified branching logic statement evaluates to true.

**Combination Trigger**

An ASI configuration that uses both a completion trigger and a logic trigger simultaneously, with an AND or OR relationship between them.

**Active Status**

A required ASI setting. An ASI set to **Active** monitors records and schedules invitations automatically. An ASI set to **Not Active** saves the configuration without triggering any emails. New ASIs default to Not Active.

**Re-evaluate ASIs**

A manual action that forces REDCap to check the trigger conditions for all ASIs against all records in the project at once. Does not modify already-scheduled invitations — it only evaluates conditions.

**Save & Copy**

A save option in the ASI setup screen that saves the current ASI configuration and then copies it to another ASI setup, useful when multiple surveys need similar invitation logic.

---

# 3. ASI Setup Location

The ASI configuration for any survey is accessed through the Online Designer. On the instrument list, each instrument that is enabled as a survey has a **+ Automated Invitations** button next to its **Survey Settings** button. Clicking it opens the ASI setup screen for that instrument.

**In longitudinal projects:** Instead of going directly to the setup screen, REDCap first asks you to select an event. The list shows only events in which that instrument is enabled as a survey. Each survey-event combination has its own independent ASI configuration.

---

# 4. ASI Setup: The Four Required Elements

Every ASI must define four elements before it will function: the message, trigger conditions, time delay settings, and active status.

## 4.1 Crafting the Message

The message composer in the ASI setup works similarly to the manual invitation composer (see RC-SURV-05 — Participant List & Manual Survey Invitations). The key fields are:

**From Email** — Selected from the dropdown of emails associated with project users (up to three per user, configurable in My Profile). Best practice is to use a study-specific or shared team email rather than a personal address.

**To Email** — Not configurable directly. REDCap sends to "all participants who meet the trigger conditions." REDCap determines the correct email address by checking three locations in priority order:

1. **Survey-specific email field** — A variable with email validation designated in that survey's settings. Used when you want to direct a specific survey to a different person (e.g., a caregiver or spouse rather than the primary participant).
2. **Participant list** — If the participant was added via the participant list, REDCap uses that email for all ASIs.
3. **Designated email field** — A project-level email field configured in Project Setup → Enable Optional Modules and Customizations. Applies to the entire record rather than a single survey.

> **Note:** REDCap applies this hierarchy in order. A survey-specific email field overrides the participant list, which overrides the designated email field.

**Subject Line** — Free text. Piping variables is supported, though sensitive data in the subject line is not recommended.

**Message Body** — Free text with rich text editor support. Supports HTML, images, and piped variables. REDCap pre-fills the body with placeholder text and the smart variables `[survey-link]` and `[survey-url]`. Keep at least one of these in the message — without a link, recipients cannot reach the survey. For guidance on piping, see RC-PIPE-01 — Piping: Basics, Syntax & Field Types.

> **Tip — Test Emails:** A small **send test email** link appears between the subject and message body. Clicking it sends the current draft to your REDCap account's primary email. Use this to verify formatting, piped values, and smart variables before the ASI goes live.

## 4.2 Trigger Conditions

Step 2 defines when REDCap schedules the invitation. There are three options.

### Completion Trigger

Check **"When the following survey is completed:"** and select the survey (or survey-event combination in longitudinal projects) that should precede this one.

This is the most common trigger for sequential workflows — for example, send a follow-up survey immediately after the baseline survey is completed.

### Logic Trigger

Check **"When the following logic becomes true:"** and enter a branching logic statement. The ASI fires the moment that statement first evaluates to true for any record.

Example use case: only send the follow-up survey if the participant indicated consent (`[consent]="1"`).

For help writing logic statements, see RC-BL-01 — Branching Logic: Overview & Scope and RC-BL-02 — Branching Logic: Syntax & Atomic Statements.

**Testing your logic:** Below the logic input box, a **Select a Record** dropdown lets you test the logic against an existing record in the project. REDCap evaluates the logic and returns "True" or "False." This is a practical way to verify trigger logic without waiting for a new submission.

### Combination Trigger

Configure both a completion trigger and a logic trigger. Then set the relationship between them using the **AND / OR** dropdown:

- **AND** — Both conditions must be true before the invitation is scheduled.
- **OR** — Either condition being true is sufficient.

**Ensure logic is still true before sending invitation**

This checkbox becomes valuable when combined with a time delay (Section 4.3). If checked, REDCap re-evaluates the trigger logic at the actual send time, not just when the invitation was originally scheduled. If the logic is no longer true at send time, REDCap cancels the invitation.

Use case: A participant enrolled in the study triggers an ASI, but later withdraws. If withdrawal sets the logic condition to false and this checkbox is enabled, the queued invitation is automatically cancelled at send time.

## 4.3 Time Delay Settings

Step 3 defines when the invitation is sent relative to the trigger event. Options include:

- **Immediately** — The invitation is sent as soon as the trigger conditions are met.
- **At a specific date and time** — The invitation is sent at an absolute date and time you define.
- **After a time delay** — The invitation is sent a set number of minutes, hours, days, weeks, or months after the trigger.
- **Based on a date/time field in the project** — REDCap looks at a specific variable with a date or datetime validation and calculates the send time relative to that value.

This last option enables participant-specific scheduling. For example, if participants have a clinic visit date stored in a field, you can configure the ASI to send a survey one day before that date — customized automatically for each record.

## 4.4 Active Status

In the top-left of the ASI setup screen, a radio button toggles between **Active** and **Not Active**.

- **Active** — REDCap begins monitoring records for the trigger conditions immediately after saving. Any record that already meets the conditions at save time will be evaluated.
- **Not Active** — Saves the configuration without enabling it. Use this mode during project development to finalize the setup without triggering premature emails.

> **Important:** A newly configured ASI defaults to Not Active. The ASI will not send any invitations until it is explicitly set to Active.

## 4.5 Reminders

Below the time delay settings, an optional **Enable Reminders** section is available. Checking the box opens the reminder configuration. REDCap supports up to five reminders per ASI. Reminders use the same time delay mechanism as the initial invitation. REDCap automatically cancels any remaining reminders once the participant completes the survey — you do not need to manage this manually.

---

# 5. Saving an ASI

Two save options are available:

**Save** — Saves the current ASI configuration.

**Save & Copy** — Saves the current configuration and opens a dialog to copy the setup to another ASI. Particularly useful when setting up multiple surveys with similar invitation logic, since the message and trigger conditions can be reused and then adjusted.

Once an ASI is saved and set to Active, REDCap begins monitoring records immediately.

---

# 6. Managing ASIs

## 6.1 Editing an Existing ASI

ASI configurations can be modified at any time. However, **edits are not retroactive.** If 100 invitations are already queued when you update the message body, those 100 invitations will still use the old message. Only invitations scheduled after the edit will reflect the new configuration. If you need to update queued invitations, you must delete and reschedule them manually through the Survey Invitation Log.

## 6.2 Bulk ASI Management via CSV

The Online Designer's **Auto Invitation Options** menu provides options to download and upload ASI configurations as a CSV file. This is useful when setting up or modifying a large number of ASIs simultaneously, since editing the CSV in a spreadsheet application is faster than navigating individual setup screens. This is considered an advanced feature.

## 6.3 Re-evaluate Automated Survey Invitations

The **Re-evaluate Automated Survey Invitations** option (also in Auto Invitation Options) forces REDCap to re-check the trigger conditions for all active ASIs against every record in the project. For large projects, this process may take several minutes.

> **Important:** Re-evaluate only triggers new invitation scheduling for records that now meet the conditions but have not yet received an invitation. It does not modify, cancel, or reschedule invitations that are already queued.

## 6.4 ASIs and Texting

If texting is enabled for a project, the ASI setup screen gains an additional step that lets you specify the delivery method: email, voice call, text message, or based on the participant's preference. Texting configuration is outside the scope of this article.

---

# 7. Common Questions

**Q: How is an ASI different from a manual survey invitation?**

**A:** A manual invitation requires a staff member to log in, select participants, and click Send. An ASI fires automatically when configured trigger conditions are met, with no staff action required. ASIs are the standard tool for follow-up surveys in longitudinal or multi-visit study designs.

**Q: What email address does REDCap use when sending an ASI?**

**A:** REDCap checks three locations in priority order: (1) the survey-specific email field, (2) the participant list, (3) the project-level designated email field. If none of these are configured, REDCap has no email address and will not send the invitation.

**Q: I updated the message body of an active ASI, but participants are still getting the old message. Why?**

**A:** ASI edits are not retroactive. Invitations already queued before the edit retain the old message. Only newly scheduled invitations use the updated content. To change an already-queued invitation, delete it in the Survey Invitation Log and allow the ASI to reschedule it.

**Q: Can I set up an ASI to trigger based on both a survey completion and a logic condition?**

**A:** Yes. Use a combination trigger. Configure both the completion condition and the logic condition, then set the AND/OR relationship between them using the dropdown in the trigger section.

**Q: Can I test my trigger logic without creating a new test record?**

**A:** Yes. Below the logic input box in the ASI setup, a "Select a Record" dropdown evaluates your logic statement against any existing record and returns True or False immediately.

**Q: Will REDCap cancel an invitation if a participant withdraws from the study after the invitation was queued?**

**A:** Only if the **"Ensure logic is still true before sending invitation"** checkbox is enabled in the ASI setup. If it is, REDCap re-evaluates the trigger logic at send time — if the logic is no longer true (because the participant's withdrawal status changed a field), the invitation is cancelled. If the checkbox is not enabled, the invitation sends regardless.

**Q: How often does REDCap check whether ASI trigger conditions are true?**

**A:** REDCap checks ASI conditions every time a record is created or modified through the user interface or via a data import. Additionally, for ASIs whose logic uses `datediff` with `'today'` or `'now'` (conditions that can change from day to day without any record edit), a background cron job re-checks those ASIs every 4 hours. Once an invitation is scheduled by these checks, a separate cron job runs every minute to send any pending invitations whose send time has arrived.

**Q: I set up an ASI after data collection had already started. Why didn't it fire for existing records?**

**A:** REDCap does not retroactively evaluate new or modified ASI configurations against records that already exist. After creating or editing an ASI, you must resave each relevant record to cause REDCap to evaluate the new logic for it. The exception is ASIs containing a `datediff` expression — the 4-hour cron job will pick those up automatically without any manual resave.

**Q: Will participants with partially completed surveys continue to receive ASI reminders?**

**A:** Yes. Reminders continue to be sent as long as the survey is not fully completed. REDCap cancels remaining reminders automatically once the survey reaches completed status. Partial responses do not stop the reminder schedule.

**Q: Will an ASI send an invitation for a survey that has already been completed?**

**A:** No. Even if an invitation is already queued in the Survey Invitation Log, REDCap will not deliver it if the target survey is already marked as completed at send time.

**Q: Are piped variables in ASI messages resolved at scheduling time or at send time?**

**A:** At scheduling time. When REDCap determines that an invitation should be scheduled, it resolves any piped variables at that moment and stores the resolved values in the queued invitation. If a piped field value changes between scheduling and the actual send time, the invitation still uses the value that was captured when it was scheduled, not the current value.

**Q: I'm using `datediff` with a datetime field to schedule an ASI. Why is the result unexpected on the same day?**

**A:** REDCap's server-side `datediff` function treats the `'today'` keyword as the very first second of the day (midnight). If a timestamp field has a value of 6:00 PM on a given day, an ASI checking `datediff` on that same day will calculate approximately 0.75 days difference — not 0. On the next day it will return approximately 0.25 days, and on subsequent days 1.25, 2.25, 3.25, and so on. Account for this behavior when writing ASI conditions that compare against datetime fields.

**Q: Can I set up an ASI to send invitations for a survey used in repeating forms?**

**A:** Yes, starting in REDCap version 12.5.0. In the ASI setup for a repeating survey, a Step 4 option appears that lets you configure the ASI to repeat — either infinitely or a limited number of times — with a configurable delay between each repeat (X minutes, X hours, or X days; decimal values accepted from version 13.0.1 onward). In earlier versions (12.4.5 and below), the ASI only fires for the first instance of the repeating form and cannot automatically re-invite for subsequent instances.

---

# 8. Common Mistakes & Gotchas

**Leaving the ASI set to Not Active.** The ASI setup saves successfully but sends nothing until the Active radio button is selected. Always verify the Active status before finishing setup, especially when going live in Production.

**Assuming ASI edits update already-queued invitations.** They do not. Existing queued invitations keep the message and settings from the time they were scheduled. If you need to update them, delete them in the Survey Invitation Log and let the ASI reschedule.

**Forgetting to configure an email source.** If none of the three email sources (survey-specific field, participant list, designated email field) are set up for a record, REDCap cannot send the ASI and the invitation will simply not go out — silently. Always confirm that at least one email source is active before relying on ASIs.

**Setting a time delay using local time but forgetting server time zone.** "At a specific date and time" scheduling uses the server's clock, not the user's local clock. A mismatch can send invitations hours early or late. Check the server time zone before setting absolute timestamps.

**Using Re-evaluate expecting it to update existing queued invitations.** Re-evaluate only looks for records that newly meet trigger conditions and have not yet been scheduled. It does not touch invitations already in the queue.

**Not adding a kill switch field for emergency stops.** Best practice is to include a radio or checkbox field (e.g., `[stop_emails]`) that can be toggled to stop all ASIs for a specific record when a participant drops out or is no longer eligible. Add this field to every ASI's logic condition with something like: `[stop_emails] <> '1'`. Combined with "Ensure logic is still true," toggling this field will automatically cancel any pending invitations at send time.

**Using `'today'` in a calc field instead of an ASI `datediff` condition.** Using `'today'` or `'now'` in calculated fields causes the calculation to update every time the form is opened and saved — for example, an age calculated as of today will become one year older when the form is accessed a year later. Reserve `'today'` and `'now'` for ASI logic or Data Quality rules where this dynamic behavior is intentional. For stored values like age at enrollment, compute from two static date fields instead.

---

# 9. Related Articles

- RC-SURV-05 — Participant List & Manual Survey Invitations (manual invitation workflow and Survey Invitation Log)
- RC-SURV-07 — Survey Queue (directing participants through multiple surveys after invitation delivery)
- RC-BL-01 — Branching Logic: Overview & Scope (logic syntax used in ASI trigger conditions)
- RC-BL-02 — Branching Logic: Syntax & Atomic Statements (writing logic conditions)
- RC-PIPE-01 — Piping: Basics, Syntax & Field Types (using piped variables in ASI messages)
- RC-PIPE-03 — Smart Variables Overview (`[survey-link]`, `[survey-url]` in messages)
- RC-ALERT-01 — Alerts & Notifications: Setup (alternative automated messaging tool)
- RC-LONG-01 — Longitudinal Project Setup (event-based ASI configuration)
