RC-PIPE-04

**Piping — Emails, Notifications & Logic Features**

| **Article ID** | RC-PIPE-04 |
|---|---|
| **Domain** | Piping |
| **Applies To** | All REDCap project types with survey or notification features; Project Design and Setup rights required |
| **Prerequisite** | RC-PIPE-01 — Piping Basics, Syntax & Field Types |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-PIPE-01 — Piping Basics, Syntax & Field Types; RC-PIPE-03 — Smart Variables Overview; RC-BL-01 — Branching Logic Overview & Scope |

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

Confirmation emails are configured within the survey settings for each instrument. When a participant submits the survey, REDCap sends the confirmation email to an address you specify — typically piped in from a field capturing the participant's email.

**What can be piped:** Any field value from the survey just completed, as well as any other field value in the record and any applicable smart variable.

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

**Common uses:** Personalizing invitations with participant names, including direct survey links, specifying the survey queue link for participants enrolled in a multi-survey sequence.

> **Institution-specific:** Local policies around automated survey invitations and email-sending from REDCap vary by installation. Contact your REDCap administrator to confirm any approval steps or institutional requirements before setting up automated communications.

## 4.3 Piping Identifiable Information in Invitations

Standard piping of identifiable information (such as participant names) works in survey invitations by default, provided that the relevant field values are available in the record at the time the invitation is sent.

---

# 5. Piping in Alerts & Notifications

The Alerts & Notifications module provides more flexibility than confirmation emails and ASIs. Alerts are not bound to a specific instrument or event — they can be triggered by any data change or logic condition across the project.

**What can be piped:** Any field value in the entire project record, plus a broad range of smart variables.

**Recipients:** Alerts can be sent to specified email addresses, piped email addresses (e.g., `[participant_email]`), or specific user roles and data access groups.

**Trigger logic:** The condition that fires an alert uses the same logic syntax as branching logic and can incorporate piped values and smart variables.

**Piping identifiable information:** As a privacy safeguard, the ability to pipe identifiable information (such as a participant's name) is **disabled by default** in Alerts & Notifications. This setting must be enabled individually for each alert in its configuration menu. There is no global toggle to enable it for all alerts at once.

> **Important:** Always review whether an alert should include identifiable information before enabling that setting. Once enabled per alert, piping will include whatever identifiable fields are referenced in the message body.

**Alerts vs. ASIs:** Use an ASI when the communication is directly tied to completing a specific survey. Use an Alert when the trigger is a data event (e.g., a value crossing a threshold, a checkbox being checked, a date being reached) or when recipients or conditions are more complex than a single instrument's completion.

> Alerts & Notifications is a large topic covered in its own dedicated training course. This section covers only the piping-specific aspects. See RC-ALERT-01 — Alerts & Notifications: Setup for full coverage.

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

---

# 7. Piping in Action Tags

Action tags modify or extend field behavior. Several accept piped values or smart variables as parameters, enabling dynamic configuration.

**`@DEFAULT`**

Pre-fills a field with a specified value when the record is first loaded. Accepts a hard-coded value, a piped variable reference, or a smart variable.

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

> **Note:** Action tags as a whole are a separate topic covered in dedicated training. This section covers only the piping-relevant examples. See RC-AT-01 — Action Tags: Overview for a full reference.

---

# 8. Common Questions

**Q: Can I include a participant's name in a survey invitation email?**

**A:** Yes — place `[first_name]` (or whatever variable holds the name) in the invitation body. The value available at send time is pulled from the record. Ensure the name field is filled in before the invitation is triggered.

**Q: Why is my participant's name showing as blank in the confirmation email?**

**A:** The most common cause is that the name field was not completed or saved before the confirmation email was triggered. Confirmation emails fire immediately on survey submission — if the name came from a prior instrument, it must have been saved before the survey was completed.

**Q: Why isn't my piped identifiable information appearing in an Alert?**

**A:** Piping identifiable information in Alerts & Notifications is disabled by default. Open the alert's configuration and enable the "Allow piping of identifiable fields" option (exact label may vary by REDCap version) for that specific alert.

**Q: What is the difference between an Automated Survey Invitation and an Alert?**

**A:** An ASI is tied to a specific instrument and fires when conditions related to that instrument are met (typically, when it is completed). An Alert is not tied to any instrument — it fires based on any configurable trigger condition in the project. Alerts also offer more flexibility in recipients and trigger logic.

**Q: Can I use smart variables in branching logic?**

**A:** Yes. Some smart variables are specifically designed for use in logic conditions. `[is-survey]` is the most commonly used — it returns 1 in survey context and 0 in data entry context, allowing instrument behavior to differ based on access type.

**Q: Does @DEFAULT use the label or raw value of a piped reference?**

**A:** It depends on the field type and modifier used. Without a modifier, structured field types (dropdowns, radio buttons) return the label. If the target field expects a raw coded value — for example, if it is itself a dropdown — you may need the `:value` modifier on the source reference. Test carefully.

---

# 9. Common Mistakes & Gotchas

**Not enabling identifiable piping in Alerts.** The most common reason piped names and contact information are blank in alerts is that the per-alert setting to allow identifiable piping has not been enabled. Check each alert's configuration individually — there is no global enable.

**Removing the default survey link from an ASI template.** REDCap pre-populates new ASIs with smart variable survey links. Deleting those links means participants receive an invitation with no way to access the survey. Modify the surrounding text, but preserve the link smart variables.

**Assuming branching logic uses display labels.** When writing logic conditions, always use the raw coded value (e.g., `[dropdown]="1"`) not the label (e.g., `[dropdown]="Vanilla"`). The piping behavior (which returns labels by default) does not carry over to logic evaluation.

**Piping a value into @DEFAULT without accounting for blank source variables.** If the source variable is empty when the record loads, @DEFAULT pre-fills the field with a blank — overwriting any value the user might have typed if they reload. Use branching logic or conditional @DEFAULT syntax to guard against pre-filling from an empty source.

**Triggering an Alert before the relevant data is saved.** Alerts fire based on a data-save event. If an alert references a field whose value is saved in a later step than the trigger, the value will be blank in the outgoing message. Align trigger conditions with the save event that captures the relevant data.

---

# 10. Related Articles

- RC-PIPE-01 — Piping Basics, Syntax & Field Types (core piping syntax)
- RC-PIPE-03 — Smart Variables Overview (smart variables for links, user info, survey metadata)
- RC-BL-01 — Branching Logic Overview & Scope (using field references and smart variables in logic conditions)
- RC-SURV-01 — Surveys – Basics (survey settings, confirmation emails, survey distribution)
- RC-ALERT-01 — Alerts & Notifications: Setup (full coverage of the alerts module)
