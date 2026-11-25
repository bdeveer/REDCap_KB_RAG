---
id: RC-PIPE-04
title: Piping — Emails, Notifications & Logic Features
domain: Piping
applies_to:
- All REDCap project types with survey or notification features
- Project Design and Setup rights required
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — piping
  timing, identifier handling and recipients checked against source code; pages not
  re-captured
prerequisites:
- 'RC-PIPE-01 — Piping: Basics, Syntax & Field Types'
version: '1.0'
last_updated: 2026-11
related:
- id: RC-PIPE-01
  title: 'Piping: Basics, Syntax & Field Types'
- id: RC-PIPE-03
  title: Smart Variables Overview
- id: RC-BL-01
  title: 'Branching Logic: Overview & Scope'
tags:
- piping
synonyms:
- how to personalize an alert email with piped data
- piping participant data into notifications
- using piping inside branching logic and action tags
- how to pipe a survey link into an email
- pre-fill a field using piping
- inserting record values into outgoing messages
- piping smart variable links into emails
- dynamic email content with piping
---

# 1. Overview

This article covers how piping is used beyond instrument field labels — specifically in outgoing emails and notifications, and as input to REDCap's branching logic and action tag features. Piping in emails allows you to personalize messages with participant data and smart variable links. Piping as input to logic and action tags enables dynamic pre-filling and conditional behavior driven by stored or context-level values.

---

# 2. Key Concepts & Definitions

**Confirmation Email**

An automated email sent to a survey respondent immediately after they submit a survey. Configured within the survey's settings for a specific instrument.

**Survey Invitation**

An email (or SMS) sent to a participant before they complete a survey, typically containing a link to the survey. Invitations can be sent manually through the Survey Distribution Tools or triggered automatically through Automated Survey Invitations.

**Automated Survey Invitation (ASI)**

A rule-based system that sends a survey invitation automatically when specified conditions are met — for example, when a prior instrument is marked complete or when a calculated date is reached.

**Alerts & Notifications**

A module that sends automated emails or SMS messages based on configurable trigger conditions. Unlike confirmation emails and ASIs, alerts are not tied to a specific instrument or survey — they can reference any data in the project and be sent to any recipient.

**Action Tag**

A special instruction added to a field's Action Tags field in the Online Designer that modifies or extends the field's behavior. Several action tags accept piped values or smart variables as their parameters.

---

# 3. Piping in Confirmation Emails

Confirmation emails are configured within the survey settings for each instrument. When a participant submits the survey, REDCap sends the confirmation email to the respondent's email address that REDCap already knows — the address in the Participant List, or the value of the project's designated email field. There is no separate "To" field to pipe into. On a public survey where REDCap has no email address for the respondent, the respondent can type an address on the survey completion page to receive the confirmation.

**What can be piped:** In the subject and body — any field value from the survey just completed, as well as any other field value in the record and any applicable smart variable. Values are filled in when the email is sent (on submission), so they reflect the data saved at that moment.

**Attachments:** The confirmation email can attach a PDF of the completed response and one static file that you upload.

**Common uses:** Personalizing the greeting with the participant's name, confirming the data they submitted, providing a direct survey queue link for next steps, or including a summary of entered values.

**Example:**

```
Dear [first_name],

Thank you for completing our survey! We have received your responses.

Your next survey will be available at: [survey-queue-url]
```

---

# 4. Piping in Survey Invitations

Both manual survey invitations and automated survey invitations support piping.

## 4.1 Manual Invitations

Sent through the Survey Distribution Tools. If REDCap can associate the invitation with a specific record, you can pipe any field value from that record into the invitation body.

## 4.2 Automated Survey Invitations (ASI)

ASIs are linked to a specific instrument and trigger automatically based on conditions. Because they are record-specific, they support the full range of piping — field values, smart variables, and instrument-specific links.

**Default ASI content:** By default, REDCap pre-populates new ASIs with smart variables that link directly to the relevant survey. These smart variable links are functional and important — modify them carefully. Removing the survey link from an invitation defeats its purpose.

**Attachments:** ASIs cannot include file attachments. If a message needs an attachment, use an alert instead (see Section 5).

**Common uses:** Personalizing invitations with participant names, including direct survey links, specifying the survey queue link for participants enrolled in a multi-survey sequence.

> **Institution-specific:** Local policies around automated survey invitations and email-sending from REDCap vary by installation. Contact your REDCap administrator to confirm any approval steps or institutional requirements before setting up automated communications.

## 4.3 When Piped Values Are Filled In

Timing differs between email types, and it matters whenever the data you pipe might be entered or changed after the trigger.

- **Survey invitations (ASIs and the Participant List):** Piped values are filled in at the moment the invitation is **scheduled** or composed — not when it goes out. The finished text is stored and sent later as is. This includes ASIs with a delay and manual invitations scheduled for a later date. Reminders reuse the same stored text, with "[Reminder]" added to the subject. Data entered or changed after scheduling does not appear.
- **Alerts & Notifications and confirmation emails:** Piped values are filled in at **send** time, so they use the record's current data.

| Email type | Piped values filled in | Picks up data entered after the trigger? |
|---|---|---|
| Automated Survey Invitation (immediate or delayed) | When the invitation is scheduled | No |
| Manual invitation from the Participant List (now or scheduled) | When the invitation is composed | No |
| Invitation reminders | Reuse the original invitation text | No |
| Alerts & Notifications (immediate or delayed) | When the alert is sent | Yes |
| Survey confirmation email | When sent, on survey submission | Data saved up to submission |

> **Tip:** If an invitation must show data that's entered later — for example, an appointment date added a few days after enrollment — use an alert with a survey link smart variable (such as `[survey-link:instrument_name]`) instead of a delayed ASI, or make sure the data exists before the ASI condition becomes true.

## 4.4 Identifiable Information and Blank Values in Invitations

Survey invitations and confirmation emails have no option to block identifier piping: fields marked as **Identifier** (such as participant names) pipe normally, provided the value is in the record when the invitation is scheduled (see 4.3).

If a piped field is blank, invitations, ASIs and confirmation emails show a line of underscores (`______`) in its place. Add `:hideunderscore` to show nothing instead — for example, `Dear [first_name:hideunderscore],`.

---

# 5. Piping in Alerts & Notifications

The Alerts & Notifications module provides more flexibility than confirmation emails and ASIs. Alerts are not bound to a specific instrument or event — they can be triggered by any data change or logic condition across the project.

**What can be piped:** Any field value in the entire project record, plus a broad range of smart variables, in the subject and body. Values are filled in when the alert is sent, so a delayed alert uses the record's current data. A blank piped field shows as nothing (no underscores). The From address and display name cannot be piped.

**Recipients:** Alerts can be sent to specified email addresses, piped email fields (e.g., `[participant_email]`), project users, or specific user roles (optionally only users in the record's data access group). Email fields marked as Identifier still work as alert recipients.

> **Version caveat (recipients by user role):** Choosing recipients by user role, optionally limited to users in the record's data access group, is a recent Standard-release feature (present in v17.6; the exact release it arrived in was not checked). It is not in LTS 17.3 or 16, where recipients are explicit addresses, piped email fields and project users. On LTS, pipe an email field or list the addresses directly.

**Attachments:** Alerts can attach files from File Upload fields in the record plus up to 5 static files that you upload.

**Trigger logic:** The condition that fires an alert uses the same logic syntax as branching logic and can incorporate piped values and smart variables.

**Piping identifiable information:** As a privacy safeguard, each alert has an option **Prevent piping of data for Identifier fields**, which is **checked by default** for every alert. There is no project-wide toggle — it is set per alert. It affects only fields marked as **Identifier** in the Online Designer: in the message, those show `[*DATA REMOVED*]` instead of their value. Fields not marked as Identifier — including a name field that hasn't been flagged — pipe normally. To pipe Identifier fields, uncheck the option in that alert and confirm the warning.

> **Important:** Always review whether an alert should include identifiable information before unchecking that option. Once unchecked, the alert includes whatever Identifier fields are referenced in the message.

> **Protected Email Mode:** If your project uses Protected Email Mode set to trigger when identifier fields are piped, piping an Identifier field into an alert, ASI or confirmation email sends that message as a protected email (the recipient gets a link to read it securely in REDCap) instead of a regular email.

**Alerts vs. ASIs:** Use an ASI when the communication is directly tied to completing a specific survey. Use an Alert when the trigger is a data event (e.g., a value crossing a threshold, a checkbox being checked, a date being reached) or when recipients or conditions are more complex than a single instrument's completion. For "a date being reached": alerts whose logic uses `datediff` with `"today"` or `"now"` are re-checked automatically on a schedule, so they can fire without anyone saving data.

> Alerts & Notifications is a large topic covered in its own dedicated training course. This section covers only the piping-specific aspects. See [RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md) for full coverage.

---

# 6. Piping as Input to Branching Logic

Branching logic and piping use the same bracket syntax, but their roles differ:

- **Piping** substitutes a value into displayed text (field labels, emails, notes).
- **Branching logic** evaluates a condition using field values to show or hide a field.

When a field value is referenced in a branching logic condition, REDCap uses the **raw coded value** — not the display label. This differs from piping's default behavior (which returns the label for most structured field types).

**Example:**

A dropdown where option 1 = "Vanilla" behaves differently in each context:

- Piping: `[flavor]` in a field label displays "Vanilla"
- Branching logic: `[flavor] = "1"` compares against the raw code "1" (not the label "Vanilla")

Smart variables can also be used in branching logic conditions. A common example is `[is-survey]`, which evaluates to 1 when the instrument is accessed as a survey and 0 when accessed as a data entry form — allowing you to show different fields depending on the access context.

> **Checkbox exception:** Checkboxes behave differently from other field types in both contexts. In piping, `[checkbox(code)]` returns the text "Checked" or "Unchecked" — not a raw coded value. In branching logic, each checkbox option is referenced individually using `[field_name(code)]` and compared to `1` (checked) or `0` (unchecked) — the option's coded value acts as a *selector* identifying which option to test, not as the comparison value itself. See [RC-PIPE-02 — Piping: Longitudinal, Repeated Instruments & Modifiers](RC-PIPE-02_Piping-Longitudinal-Repeated-Instruments-and-Modifiers.md) for the full set of checkbox modifiers.

---

# 7. Piping in Action Tags

Action tags modify or extend field behavior. Several accept piped values or smart variables as parameters, enabling dynamic configuration.

**`@DEFAULT`**

Pre-fills an empty field with a specified value when the form is first opened (before it has been saved). Accepts a hard-coded value, a piped variable reference, or a smart variable.

Use case: carry a value forward from a previous event or instance.

```
@DEFAULT='[previous-event][med_name]'
```

This pre-fills the field with the medication name from the previous event.

**`@CALCTEXT`**

Pre-fills a text field based on a logic expression — similar to a calculated field but for text output.

Use case: display a preferred name based on a participant's stated preference.

```
@CALCTEXT(if([pref]=1,[nick_name],[formal_name]))
```

If `pref` equals 1, the field is pre-filled with the value of `nick_name`; otherwise, it uses `formal_name`.

> **Note:** Action tags as a whole are a separate topic covered in dedicated training. This section covers only the piping-relevant examples. See [RC-AT-01 — Action Tags: Overview](RC-AT-01_Action-Tags-Overview.md) for a full reference.

---

# 8. Common Questions

**Q: Can I include a participant's name in a survey invitation email?**

**A:** Yes — place `[first_name]` (or whatever variable holds the name) in the invitation body. The value is filled in when the invitation is scheduled, not when it is sent — so make sure the name field is saved before the ASI condition becomes true (or before you compose the invitation from the Participant List). A name added afterward will not appear, not even in reminders.

**Q: Why is my participant's name showing as blank in the confirmation email?**

**A:** The most common cause is that the name field was not completed or saved before the confirmation email was triggered. Confirmation emails fire immediately on survey submission — if the name came from a prior instrument, it must have been saved before the survey was completed. When a piped field is empty, confirmation emails and invitations show a line of underscores (`______`); use `[first_name:hideunderscore]` to show nothing instead. (In alerts, an empty field simply shows as nothing.)

**Q: Why isn't my piped identifiable information appearing in an Alert?**

**A:** If the alert shows `[*DATA REMOVED*]` where the value should be, the field is marked as **Identifier** and the alert's **Prevent piping of data for Identifier fields** option is checked (the default for every alert). Open that alert, uncheck the option and confirm the warning. If nothing at all appears, the field isn't being blocked — it was most likely empty when the alert was sent.

**Q: What is the difference between an Automated Survey Invitation and an Alert?**

**A:** An ASI is tied to a specific instrument and fires when conditions related to that instrument are met (typically, when it is completed). An Alert is not tied to any instrument — it fires based on any configurable trigger condition in the project. Alerts also offer more flexibility in recipients and trigger logic, and they fill in piped values when sent rather than when scheduled.

**Q: Can I use smart variables in branching logic?**

**A:** Yes. Some smart variables are specifically designed for use in logic conditions. `[is-survey]` is the most commonly used — it returns 1 in survey context and 0 in data entry context, allowing instrument behavior to differ based on access type.

**Q: Does @DEFAULT use the label or raw value of a piped reference?**

**A:** It depends on the field type and modifier used. Without a modifier, structured field types (dropdowns, radio buttons) return the label. If the target field expects a raw coded value — for example, if it is itself a dropdown — you may need the `:value` modifier on the source reference. Test carefully.

---

# 9. Common Mistakes & Gotchas

**Not unchecking identifier blocking in Alerts.** If an alert shows `[*DATA REMOVED*]` instead of a name or contact detail, that field is marked as Identifier and the alert's **Prevent piping of data for Identifier fields** option is still checked (the default). Uncheck it in each alert that needs it — there is no project-wide setting. Fields not marked as Identifier pipe normally.

**Expecting a delayed ASI to pick up data entered after it was scheduled.** ASI and Participant List invitations are filled in when scheduled, and reminders reuse that text. If the invitation must include data entered later, use an alert with a survey link smart variable instead, or make sure the data exists before the ASI condition becomes true.

**Removing the default survey link from an ASI template.** REDCap pre-populates new ASIs with smart variable survey links. Deleting those links means participants receive an invitation with no way to access the survey. Modify the surrounding text, but preserve the link smart variables.

**Assuming branching logic uses display labels.** When writing logic conditions, always use the raw coded value (e.g., `[dropdown]="1"`) not the label (e.g., `[dropdown]="Vanilla"`). The piping behavior (which returns labels by default) does not carry over to logic evaluation.

**Expecting @DEFAULT to fill in later from a source that was empty.** @DEFAULT fills the field only when the field is empty, the piped default isn't empty, and the form hasn't been saved before — it never overwrites a typed or saved value. If the source variable is empty when the form is first opened, there is simply no default, and it won't fill in later once the form has been saved. Make sure the source data is entered before the form is first opened and saved.

**Triggering an Alert before the relevant data is saved.** Most alerts fire based on a data-save event. If an alert references a field whose value is saved in a later step than the trigger, the value will be blank in the outgoing message. Align trigger conditions with the save event that captures the relevant data. (Alerts whose logic uses `datediff` with `"today"` or `"now"` are also re-checked on a schedule, so they can fire without a save — but they still pipe only the data that exists when they are sent.)

---

# 10. Related Articles

- [RC-PIPE-01 — Piping: Basics, Syntax & Field Types](RC-PIPE-01_Piping-Basics-Syntax-and-Field-Types.md) (core piping syntax)
- [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md) (smart variables for links, user info, survey metadata)
- [RC-BL-01 — Branching Logic: Overview & Scope](RC-BL-01_Branching-Logic-Overview-and-Scope.md) (using field references and smart variables in logic conditions)
- [RC-SURV-01 — Surveys – Basics](RC-SURV-01_Surveys-Basics.md) (survey settings, confirmation emails, survey distribution)
- [RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md) (full coverage of the alerts module)
