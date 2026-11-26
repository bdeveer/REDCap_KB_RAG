

**Surveys — Automated Survey Invitations (ASI)**

| **Article ID** | [RC-SURV-06 — Automated Survey Invitations (ASI)](RC-SURV-06_Automated-Survey-Invitations.md) |
|---|---|
| **Domain** | Surveys |
| **Applies To** | All projects with surveys enabled |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — automated survey invitation behaviour checked against source code; pages not re-captured |
| **Prerequisite** | [RC-SURV-05 — Participant List & Manual Survey Invitations](RC-SURV-05_Participant-List-and-Manual-Survey-Invitations.md) |
| **Version** | 1.3 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-SURV-05 — Participant List & Manual Survey Invitations](RC-SURV-05_Participant-List-and-Manual-Survey-Invitations.md); [RC-SURV-07 — Survey Queue](RC-SURV-07_Survey-Queue.md); [RC-BL-01 — Branching Logic: Overview & Scope](RC-BL-01_Branching-Logic-Overview-and-Scope.md); [RC-BL-02 — Branching Logic: Syntax & Atomic Statements](RC-BL-02_Branching-Logic-Syntax-and-Atomic-Statements.md); [RC-PIPE-01 — Piping: Basics, Syntax & Field Types](RC-PIPE-01_Piping-Basics-Syntax-and-Field-Types.md); [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md) |
| **Synonyms** | how do i send automatic survey invitations; schedule survey emails based on logic; set up automated survey invitations asi; send follow-up surveys without manual work; trigger a survey invite when a condition is met; add a time delay before sending a survey invite; configure survey reminders automatically; automated email invitations for surveys |

---

## 1. Overview

This article covers Automated Survey Invitations (ASIs) — REDCap's mechanism for automatically scheduling and sending survey invitation emails based on defined trigger conditions and time delay settings. ASIs are the standard tool for distributing follow-up surveys without manual intervention. This article explains the ASI setup screen, the three trigger types, time delay options, reminders, and how to manage ASIs across a project's lifetime. This article is part of the Surveys knowledge base series.

---

## 2. Key Concepts & Definitions

**Automated Survey Invitation (ASI)**

A configured rule that tells REDCap to automatically schedule a survey invitation email when specified conditions are met. Each survey can have one ASI configured. In longitudinal projects, each survey-event combination can have its own ASI.

**Completion Trigger**

An ASI trigger condition that fires when a specified survey is completed — either submitted by the participant or marked complete by a user (including setting the instrument's Form Status to Complete).

**Logic Trigger**

An ASI trigger condition that fires when a specified branching logic statement evaluates to true at the time REDCap checks it (see Section 4.2).

**Combination Trigger**

An ASI configuration that uses both a completion trigger and a logic trigger simultaneously, with an AND or OR relationship between them.

**Active Status**

A required ASI setting. An ASI set to **Active** monitors records and schedules invitations automatically. An ASI set to **Not Active** schedules nothing new — but invitations already queued are not cancelled. A new ASI has neither option selected; you must choose one before saving.

**Re-evaluate ASIs**

A manual action that forces REDCap to check the trigger conditions for all active ASIs against all records in the project at once. It schedules invitations for records that now qualify and, for ASIs with "Ensure logic is still true" enabled, removes queued invitations whose logic is now false. It never changes the text, sender or send time of invitations that stay queued.

**Save & Copy**

A save option in the ASI setup screen that saves the current ASI configuration and then copies it to another ASI setup, useful when multiple surveys need similar invitation logic. It copies everything, including Active status, and overwrites the target's existing configuration.

---

## 3. ASI Setup Location

The ASI configuration for any survey is accessed through the Online Designer. On the instrument list, each instrument that is enabled as a survey has a **+ Automated Invitations** button next to its **Survey Settings** button. Clicking it opens the ASI setup screen for that instrument.

**In longitudinal projects:** Instead of going directly to the setup screen, REDCap first asks you to select an event. The list shows only events in which that instrument is enabled as a survey. Each survey-event combination has its own independent ASI configuration.

---

## 4. ASI Setup: The Four Required Elements

Every ASI must define four elements before it will function: the message, trigger conditions, time delay settings, and active status.

### 4.1 Crafting the Message

The message composer in the ASI setup works similarly to the manual invitation composer (see [RC-SURV-05 — Participant List & Manual Survey Invitations](RC-SURV-05_Participant-List-and-Manual-Survey-Invitations.md)). The key fields are:

**From Email** — Selected from the dropdown of emails associated with project users (up to three per user, configurable in My Profile). Best practice is to use a study-specific or shared team email rather than a personal address.

**To Email** — Not configurable directly. REDCap sends to "all participants who meet the trigger conditions." REDCap determines the correct email address by checking three locations in priority order:

1. **Survey-specific email field** — A variable with email validation designated in that survey's settings. Used when you want to direct a specific survey to a different person (e.g., a caregiver or spouse rather than the primary participant).
2. **Designated email field** — A project-level email field configured in Project Setup → Enable Optional Modules and Customizations. Applies to the entire record rather than a single survey.
3. **Participant list** — If the participant's email was entered in the participant list, REDCap uses it when neither field above holds a value.

> **Note:** REDCap applies this hierarchy in order. A survey-specific email field overrides the designated email field, which overrides the participant list email.

**Subject Line** — Free text. Piping variables is supported, though sensitive data in the subject line is not recommended.

**Message Body** — Free text with rich text editor support. Supports HTML, images, and piped variables. REDCap pre-fills the body with placeholder text and the smart variables `[survey-link]` and `[survey-url]`. Keep at least one of these in the message — without a link, recipients cannot reach the survey. For guidance on piping, see [RC-PIPE-01 — Piping: Basics, Syntax & Field Types](RC-PIPE-01_Piping-Basics-Syntax-and-Field-Types.md).

> **Tip — Test Emails:** A small **send test email** link appears between the subject and message body. Clicking it sends the current draft to your REDCap account's primary email. Use this to verify formatting and layout before the ASI goes live. The test is not tied to a record, so piped variables and smart variables show placeholder values rather than real data — check piping on a test record in Development instead.

### 4.2 Trigger Conditions

Step 2 defines when REDCap schedules the invitation. There are three options.

#### Completion Trigger

Check **"When the following survey is completed:"** and select the survey (or survey-event combination in longitudinal projects) that should precede this one.

This is the most common trigger for sequential workflows — for example, send a follow-up survey immediately after the baseline survey is completed. The trigger also fires when a user completes the instrument on the data entry form (for example by setting its Form Status to Complete), not only when the participant submits the survey.

#### Logic Trigger

Check **"When the following logic becomes true:"** and enter a branching logic statement. REDCap does not watch the logic continuously; it checks it when record data is saved (data entry forms, surveys, data import, API, Data Quality fixes), when the 4-hour `datediff` check runs (see Section 7), and when you run **Re-evaluate Automated Survey Invitations**. If the logic is true at one of those checks, the invitation is scheduled.

An invitation is scheduled only once per record (per event/instance). If the data later changes so the logic is false again, the queued invitation stays in place unless **Ensure logic is still true before sending invitation** is enabled (below).

In longitudinal projects, a variable written without an event prefix refers to the ASI's own event. Prefix variables from other events explicitly (e.g. `[baseline_arm_1][consent]`).

Example use case: only send the follow-up survey if the participant indicated consent (`[consent]="1"`).

For help writing logic statements, see [RC-BL-01 — Branching Logic: Overview & Scope](RC-BL-01_Branching-Logic-Overview-and-Scope.md) and [RC-BL-02 — Branching Logic: Syntax & Atomic Statements](RC-BL-02_Branching-Logic-Syntax-and-Atomic-Statements.md).

**Testing your logic:** Below the logic input box, a **Select a Record** dropdown lets you test the logic against an existing record in the project. REDCap evaluates the logic and returns "True" or "False." This is a practical way to verify trigger logic without waiting for a new submission.

#### Combination Trigger

Configure both a completion trigger and a logic trigger. Then set the relationship between them using the **AND / OR** dropdown:

- **AND** — Both conditions must be true before the invitation is scheduled.
- **OR** — Either condition being true is sufficient.

**Ensure logic is still true before sending invitation**

This checkbox becomes valuable when combined with a time delay (Section 4.3). If checked, REDCap re-checks the trigger logic at the actual send time, and also whenever the record is saved and when Re-evaluate is run — not just when the invitation was originally scheduled. If the logic is no longer true at any of those checks, REDCap removes the queued invitation. If the logic later becomes true again, the invitation can be scheduled again.

Use case: A participant enrolled in the study triggers an ASI, but later withdraws. If withdrawal sets the logic condition to false and this checkbox is enabled, the queued invitation is removed automatically.

**Re-evaluate send time** *(17.2.0+)*

A distinct setting, and easily confused with the checkbox above. "Ensure logic is still true" decides **whether** a scheduled invitation still goes out; **Re-evaluate send time** decides **when** it goes out.

It applies only to ASIs scheduled relative to a stored date/time — the time-lapse option in **When to send AFTER conditions are met** with a date or datetime field selected (Section 4.3). With it enabled, changing that date/time field reschedules the queued invitation to match. Move a participant's appointment date and the reminder follows it.

Limits worth knowing:

- Only **scheduled but unsent** invitations are affected.
- Only the send time changes — sender, subject and content are not re-evaluated.
- **For reminders, if the initial invitation has already been sent, subsequent unsent reminders are not rescheduled.**
- It is **unchecked by default** and becomes available only once a date field is chosen. Tick it explicitly on each ASI that should follow date changes; ASIs where it is unchecked keep their original send time.

> **Version caveat (16.0.61 LTS):** Re-evaluate send time does not exist on the 16.0 LTS line — it is present in 17.3 and later. On 16.0, a queued invitation keeps its original send time when the date field changes; delete it in the Survey Invitation Log (without ticking **Permanently cancel**) and run Re-evaluate to reschedule it from the new date.

> **Version caveat (17.2.0–17.4.0 Standard; ≤17.3.6 LTS):** Unreliable for its entire life before 17.4.1. The checkbox could fail to save, and where it worked it could reschedule invitations and reminders **at incorrect times whenever any data changed** — not only the date field concerned. Both fixed in 17.4.1 Standard / 17.3.7 LTS. The setting was also missing from the Alerts CSV upload and download files until 17.3.1. See [RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md) §4.2a, which covers the same feature for Alerts.

> **Version caveat (below 17.5.1 Standard / 17.3.14 LTS):** Even after the 17.4.1 fixes, **reminders** could be scheduled at the wrong time for an ASI that combined a **time lag relative to a stored date** with **Re-evaluate send time**. Check reminder times in the Survey Invitation Log on affected versions.

### 4.3 Time Delay Settings

Step 3, **When to send AFTER conditions are met**, defines when the invitation is sent. There are four radio options:

- **Immediately** — The invitation is sent as soon as the trigger conditions are met.
- **On the next matching day at a specific time** — The invitation is sent on the next occurrence of a matching day type (any day, weekday, or weekend day) at a time you specify. For example: "next weekday at 10:30 AM." In the CSV column reference this mode is `NEXT_OCCURRENCE`; see [RC-IMP-06](RC-IMP-06_Automated-Survey-Invitations-CSV.md) for the full column mapping.
- **After a lapse of time** — The invitation is sent a set number of **days, hours and minutes** after a reference point. There are no week or month units — enter 7 days for a week, or about 30.44 days for a month. By default the reference point is when the conditions were met (either the exact time triggered or midnight of that day). Optionally, choose a date or datetime variable and send the invitation a set time **before or after** that stored value.
- **At a specific date and time** — The invitation is sent at an absolute date and time you define.

The date-variable choice within the time-lapse option enables participant-specific scheduling. For example, if participants have a clinic visit date stored in a field, you can configure the ASI to send a survey one day before that date — customized automatically for each record. If that date variable is blank, or holds a missing data code, for a record, nothing is scheduled for that record.

### 4.4 Active Status

In the top-left of the ASI setup screen, a radio button toggles between **Active** and **Not Active**.

- **Active** — REDCap evaluates the trigger conditions for a record the next time that record's data is saved. Saving the ASI does **not** check records that already exist; after saving, REDCap offers to run Re-evaluate, which is the way to pick up existing records (Section 6.3). ASIs whose logic uses `datediff` with `'today'`/`'now'` are also picked up by the 4-hour background check.
- **Not Active** — Saves the configuration without scheduling anything new. Use this mode during project development to finalize the setup without triggering premature emails.

> **Important:** A new ASI has neither Active nor Not Active selected — you must choose one. The ASI will not schedule any invitations until it is set to Active.

> **Important:** Switching an ASI to Not Active does **not** cancel invitations that are already queued. To stop them, delete them in the Survey Invitation Log.

No invitations are sent while the project is in Analysis/Cleanup status or marked Completed. Invitations are also not scheduled once the survey's response limit has been reached, or for records that do not belong to the ASI's arm.

### 4.5 Reminders

Below the time delay settings, an optional **Enable Reminders** section is available. Checking the box opens the reminder configuration. REDCap supports up to five reminders per ASI. Key behaviours:

- Each reminder is timed from the **previous** send (the invitation or the prior reminder), not from the original trigger.
- Reminder emails reuse the invitation message with **[Reminder]** added to the start of the subject line.
- If reminders are set to go at an exact date and time, only one reminder is possible.
- If the survey has a time limit for completion and that limit has passed, remaining reminders are not sent.
- Queued invitations and reminders are removed when the participant submits the survey or a user marks the survey response complete. Completing the instrument by other routes — setting Form Status to Complete on the data entry form, or importing data — may not remove them. If you complete a survey that way and the participant should not be contacted, delete the queued items in the Survey Invitation Log.

---

## 5. Saving an ASI

Two save options are available:

**Save** — Saves the current ASI configuration.

**Save & Copy** — Saves the current configuration and opens a dialog to copy the setup to another ASI. Particularly useful when setting up multiple surveys with similar invitation logic, since the message and trigger conditions can be reused and then adjusted. The copy includes **everything**, including Active status, and overwrites whatever the target ASI already had — review the target (especially its Active setting) after copying.

Once an ASI is saved and set to Active, it applies to records as they are next saved. Existing records are not checked at save time — accept the prompt to run Re-evaluate (Section 6.3) if existing records should be picked up.

---

## 6. Managing ASIs

### 6.1 Editing an Existing ASI

ASI configurations can be modified at any time. However, **edits are not retroactive.** If 100 invitations are already queued when you update the message body, those 100 invitations will still use the old message. Only invitations scheduled after the edit will reflect the new configuration. If you need to update queued invitations, delete them in the Survey Invitation Log. A deleted invitation is rescheduled (with the new configuration) only when the record is next saved or Re-evaluate is run — and never if you tick **Permanently cancel** when deleting.

Other changes that affect queued invitations:

- **Deleting a record** removes its queued invitations.
- **Removing the instrument from an event** (longitudinal designation) sets that ASI to Not Active and marks its queued invitations as not sent.

### 6.2 Bulk ASI Management via CSV

The Online Designer's **Auto Invitation Options** menu provides options to download and upload ASI configurations as a CSV file. This is useful when setting up or modifying a large number of ASIs simultaneously, since editing the CSV in a spreadsheet application is faster than navigating individual setup screens. This is considered an advanced feature.

Always download the existing configuration first before uploading. The number of columns depends on your REDCap version and project type (for example, only 17.x includes a column for Re-evaluate send time), so build from your own download. The full format reference — including all accepted values, timing mode details, and CSV gotchas — is documented in [RC-IMP-06 — Automated Survey Invitations CSV — Column Reference and Format Guide](RC-IMP-06_Automated-Survey-Invitations-CSV.md).

### 6.3 Re-evaluate Automated Survey Invitations

The **Re-evaluate Automated Survey Invitations** option (also in Auto Invitation Options) forces REDCap to re-check the trigger conditions for all active ASIs against every record in the project. Use it after creating or changing an ASI so that existing records are evaluated. For large projects, this process may take several minutes.

A **Test Run** option previews what Re-evaluate would schedule or remove without making changes — use it first. On a real run, invitations set to send immediately go out straight away.

> **Important:** Re-evaluate schedules invitations for records that now meet the conditions and have not yet been scheduled. For ASIs with **Ensure logic is still true** enabled, it also **removes** queued invitations whose logic is now false. It never changes the message, sender or send time of invitations that stay in the queue.

### 6.4 ASIs and Texting

If texting is enabled for a project, the ASI setup screen gains an additional step that lets you specify the delivery method: email, voice call, text message, or based on the participant's preference. Texting configuration is outside the scope of this article.

---

## 7. Common Questions

**Q: How is an ASI different from a manual survey invitation?**

**A:** A manual invitation requires a staff member to log in, select participants, and click Send. An ASI fires automatically when configured trigger conditions are met, with no staff action required. ASIs are the standard tool for follow-up surveys in longitudinal or multi-visit study designs.

**Q: What email address does REDCap use when sending an ASI?**

**A:** REDCap checks three locations in priority order: (1) the survey-specific email field, (2) the project-level designated email field, (3) the participant list email. If none of these holds an address for the record, REDCap cannot send the invitation; the Survey Invitation Log shows it as not sent because no email address was found.

**Q: I updated the message body of an active ASI, but participants are still getting the old message. Why?**

**A:** ASI edits are not retroactive. Invitations already queued before the edit retain the old message. Only newly scheduled invitations use the updated content. To change an already-queued invitation, delete it in the Survey Invitation Log (without ticking **Permanently cancel**), then run Re-evaluate or resave the record so the ASI reschedules it with the new content.

**Q: Can I set up an ASI to trigger based on both a survey completion and a logic condition?**

**A:** Yes. Use a combination trigger. Configure both the completion condition and the logic condition, then set the AND/OR relationship between them using the dropdown in the trigger section.

**Q: Can I test my trigger logic without creating a new test record?**

**A:** Yes. Below the logic input box in the ASI setup, a "Select a Record" dropdown evaluates your logic statement against any existing record and returns True or False immediately.

**Q: Will REDCap cancel an invitation if a participant withdraws from the study after the invitation was queued?**

**A:** Only if the **"Ensure logic is still true before sending invitation"** checkbox is enabled in the ASI setup. If it is, REDCap re-checks the trigger logic when the record is saved, when Re-evaluate is run, and at send time — if the logic is no longer true (because the participant's withdrawal status changed a field), the invitation is removed. If the checkbox is not enabled, the invitation sends regardless unless you delete it in the Survey Invitation Log.

**Q: How often does REDCap check whether ASI trigger conditions are true?**

**A:** REDCap checks ASI conditions every time record data is saved — on data entry forms and surveys, via data import or the API, and through Data Quality fixes — and when a user runs Re-evaluate. Additionally, for ASIs whose logic uses `datediff` with `'today'` or `'now'` (conditions that can change from day to day without any record edit), a background cron job re-checks those ASIs, with each record re-checked roughly every 4 hours. Once an invitation is scheduled by these checks, a separate cron job runs every minute to send any pending invitations whose send time has arrived. This means an "immediate" invitation triggered by a data import or API call is sent when that mailer job next runs, usually within a minute or two.

**Q: I set up an ASI after data collection had already started. Why didn't it fire for existing records?**

**A:** Saving an ASI does not evaluate records that already exist. After creating or editing an ASI, run **Re-evaluate Automated Survey Invitations** (Auto Invitation Options in the Online Designer; REDCap also offers it when you save the ASI). Use its Test Run first to preview the result. Resaving an individual record also works, but Re-evaluate covers the whole project at once. ASIs containing a `datediff` expression with `'today'`/`'now'` are also picked up by the 4-hour background check.

**Q: Will participants with partially completed surveys continue to receive ASI reminders?**

**A:** Yes. Reminders continue to be sent as long as the survey is not fully completed. Partial responses do not stop the reminder schedule. Remaining reminders are removed when the participant submits the survey or a user marks the response complete; if the instrument is completed another way (Form Status set on the data entry form, or data import), check the Survey Invitation Log and delete any reminders still queued.

**Q: Will an ASI send an invitation for a survey that has already been completed?**

**A:** No. Even if an invitation is already queued in the Survey Invitation Log, REDCap will not deliver it if the target survey is already marked as completed at send time.

**Q: Are piped variables in ASI messages resolved at scheduling time or at send time?**

**A:** At scheduling time. When REDCap determines that an invitation should be scheduled, it resolves any piped variables at that moment and stores the resolved values in the queued invitation. If a piped field value changes between scheduling and the actual send time, the invitation still uses the value that was captured when it was scheduled, not the current value.

**Q: I'm using `datediff` with a datetime field to schedule an ASI. Why is the result unexpected on the same day?**

**A:** REDCap's server-side `datediff` function treats the `'today'` keyword as the very first second of the day (midnight). If a timestamp field has a value of 6:00 PM on a given day, an ASI checking `datediff` on that same day will calculate approximately 0.75 days difference — not 0. On the next day it will return approximately 0.25 days, and on subsequent days 1.25, 2.25, 3.25, and so on. Account for this behavior when writing ASI conditions that compare against datetime fields.

**Q: Can I set up an ASI to send invitations for a survey used in repeating forms?**

**A:** Yes, starting in REDCap version 12.5.0. In the ASI setup for a repeating survey, a Step 4 option appears that lets you configure the ASI to repeat — either infinitely or a limited number of times — with a configurable delay between each repeat (X minutes, X hours, or X days; decimal values accepted from version 13.0.1 onward). Without that recurring option, an ASI on a repeating survey only fires for the first instance — this is also the only behaviour in earlier versions (12.4.5 and below).

---

## 8. Common Mistakes & Gotchas

**Leaving the ASI set to Not Active.** The ASI setup saves successfully but sends nothing until the Active radio button is selected. Always verify the Active status before finishing setup, especially when going live in Production.

**Setting an ASI to Not Active to stop emails that are already queued.** Not Active only stops new scheduling; queued invitations still go out. Delete them in the Survey Invitation Log.

**Expecting a newly saved ASI to catch existing records.** Saving the ASI does not evaluate records that already exist. Run Re-evaluate (Test Run first) after creating or changing an ASI.

**Assuming ASI edits update already-queued invitations.** They do not. Existing queued invitations keep the message and settings from the time they were scheduled. If you need to update them, delete them in the Survey Invitation Log (leave **Permanently cancel** unticked), then run Re-evaluate or resave the record so the ASI reschedules them.

**Forgetting to configure an email source.** If none of the three email sources (survey-specific field, designated email field, participant list) holds an address for a record, REDCap cannot send the ASI. It is not silent — the Survey Invitation Log shows the invitation as not sent because no email was found — but nobody is alerted, so check the log. Always confirm that at least one email source is populated before relying on ASIs.

> **Version caveat (17.3+):** If a participant has unsubscribed from emails, an ASI invitation to them is recorded in the Survey Invitation Log as opted out. This logging is present in 17.3 and later, not on the 16.0 LTS line. If participants report missing invitations, check the log for an opted-out entry before resending.

**Setting a time delay using local time but forgetting server time zone.** "At a specific date and time" scheduling uses the server's clock, not the user's local clock. A mismatch can send invitations hours early or late. Check the server time zone before setting absolute timestamps.

**Using Re-evaluate expecting it to update existing queued invitations.** Re-evaluate schedules records that newly meet trigger conditions and, where "Ensure logic is still true" is enabled, removes queued invitations whose logic is now false. It never updates the message, sender or send time of invitations that remain queued.

**Not adding a kill switch field for emergency stops.** Best practice is to include a radio or checkbox field (e.g., `[stop_emails]`) that can be toggled to stop all ASIs for a specific record when a participant drops out or is no longer eligible. Add this field to every ASI's logic condition with something like: `[stop_emails] <> '1'`. Combined with "Ensure logic is still true," toggling this field will automatically remove any pending invitations for that record.

**Using `'today'` in a calc field instead of an ASI `datediff` condition.** Using `'today'` or `'now'` in calculated fields causes the calculation to update every time the form is opened and saved — for example, an age calculated as of today will become one year older when the form is accessed a year later. Reserve `'today'` and `'now'` for ASI logic or Data Quality rules where this dynamic behavior is intentional. For stored values like age at enrollment, compute from two static date fields instead.

---

## 9. Related Articles

- [RC-SURV-05 — Participant List & Manual Survey Invitations](RC-SURV-05_Participant-List-and-Manual-Survey-Invitations.md) (manual invitation workflow and Survey Invitation Log)
- [RC-SURV-07 — Survey Queue](RC-SURV-07_Survey-Queue.md) (directing participants through multiple surveys after invitation delivery)
- [RC-BL-01 — Branching Logic: Overview & Scope](RC-BL-01_Branching-Logic-Overview-and-Scope.md) (logic syntax used in ASI trigger conditions)
- [RC-BL-02 — Branching Logic: Syntax & Atomic Statements](RC-BL-02_Branching-Logic-Syntax-and-Atomic-Statements.md) (writing logic conditions)
- [RC-PIPE-01 — Piping: Basics, Syntax & Field Types](RC-PIPE-01_Piping-Basics-Syntax-and-Field-Types.md) (using piped variables in ASI messages)
- [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md) (`[survey-link]`, `[survey-url]` in messages)
- [RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md) (alternative automated messaging tool)
- [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md) (event-based ASI configuration)
