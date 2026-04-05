RC-SURV-03

**Survey Settings: Behavior, Access & Termination**

| **Article ID** | RC-SURV-03 |
| --- | --- |
| **Domain** | Surveys |
| **Applies To** | All REDCap projects with surveys enabled; some settings (Survey Response PDF Save, Time Limit) require additional project features such as longitudinal mode or the Participant List |
| **Prerequisite** | RC-SURV-01 — Surveys – Basics; RC-SURV-02 — Survey Settings: Basic Options & Design |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-SURV-01 — Surveys – Basics; RC-SURV-02 — Survey Settings: Basic Options & Design; RC-ALERT-01 — Alerts & Notifications: Setup; RC-PIPE-01 — Piping: Basics, Syntax & Field Types; RC-LONG-01 — Longitudinal Project Setup |

---

# 1. Overview

This article is the second of a two-part series on the REDCap Survey Settings page. It covers three sections of the settings page: **Survey Customizations** (behavioral options that affect how participants interact with the survey), **Survey Access** (rules that govern who can access the survey and for how long), and **Survey Termination Options** (what happens after a participant submits or is stopped). The companion article, RC-SURV-02, covers the Basic Options and Design sections.

---

# 2. Key Concepts & Definitions

## Survey Customizations

A collection of settings that govern specific behaviors during survey completion — question numbering, pagination, PDF handling, accessibility, and button labels.

## Pagination

The division of a survey into multiple pages. In REDCap, page breaks are defined by the placement of **Section Header** field types within the instrument. Each section header marks the start of a new page when pagination is enabled.

## Section Header

A field type in REDCap that displays a visual divider and optional heading text in an instrument. When pagination is set to **Multiple Pages**, each section header begins a new survey page.

## Survey Access

Settings that define when, how often, and under what conditions a participant can access a survey: response limits, time limits, expiration dates, and save-and-return behavior.

## Save and Return

A feature that allows a participant to pause a survey mid-completion, receive a return code, and resume later without starting over.

## Return Code

A system-generated alphanumeric code given to a participant when they save their progress. Required to resume a saved survey unless the return-code requirement is disabled.

## Survey Termination Options

Settings that control what happens after a participant submits a survey or triggers a stop action: redirection, completion messages, stop-action behavior, e-consent archiving, and confirmation emails.

## Stop Action

A condition attached to a specific answer option in the Online Designer. When a participant selects that option, the survey ends immediately. The Survey Settings page controls what happens to the data and what message the participant sees when a stop action fires.

## e-Consent Framework

A REDCap feature that requires a participant to confirm the accuracy of their responses before the survey is marked complete. Commonly used for electronic consent forms. Generates an auto-archived PDF of the completed consent.

## Auto-Archiver

A feature that automatically generates a PDF of a completed survey response and saves it to the project's File Repository. Does not require a dedicated file upload variable.

## Confirmation Email

An email sent to a participant automatically after they complete a survey. Distinct from Alerts & Notifications — confirmation emails are configured per survey and fire only on completion.

---

# 3. Survey Customizations

## 3.1 Question Numbering

REDCap can display a number before each question on the survey. This setting has two modes:

- **Auto-numbering** — REDCap assigns sequential numbers (1, 2, 3...) automatically. This is the default when no branching logic is present.
- **Custom numbering** — Numbers are defined manually, per variable. REDCap automatically switches to this mode — and disables auto-numbering — when the instrument contains branching logic.

**Why branching logic disables auto-numbering:** When questions are conditionally hidden or shown, sequential numbers create gaps in the participant's view (e.g., the participant sees question 1, then question 4). This is confusing. Custom numbering lets you assign context-appropriate labels (e.g., `4a`, `IIIb`, `2.1`) that remain meaningful when questions are skipped.

Custom numbers are set in two ways:
- Per-variable in the **Online Designer** (an extra number field appears when custom numbering is enabled).
- In bulk via the **Data Dictionary** (faster for instruments with many variables).

> **Note:** If you enable custom numbering but do not define numbers for any variables, your survey will display no question numbers at all. This is a valid choice if you prefer an unnumbered survey.

## 3.2 Pagination

This setting controls whether the entire survey is displayed as a single scrolling page or broken into multiple pages.

- **Single Page** (default) — all questions appear on one page.
- **Multiple Pages** — the survey is split at each **Section Header** field. Each section header starts a new page.

When **Multiple Pages** is selected, two additional options become available:

- **Display page numbers** — shows participants how far through the survey they are (e.g., "Page 2 of 5").
- **Hide the "Previous Page" button** — removes the back-navigation button, preventing participants from returning to earlier pages. Useful when you display calculated scores on a final page and do not want participants to go back and alter the inputs that feed those calculations.

## 3.3 PDF Download

This toggle controls whether participants are offered a **Download PDF** button after completing the survey. When enabled, participants can download a PDF of their own responses.

This is a popular option for registration forms and consent-adjacent surveys where participants want a copy of what they submitted.

## 3.4 Survey Response PDF Save

Similar to PDF Download, but instead of offering the PDF to the participant, REDCap saves it automatically into a designated **file upload variable** in the project dataset. The saved PDF becomes part of the record.

This is useful when you need an immutable copy of the response — for example, in consent workflows where you want to store a timestamped record of what the participant agreed to.

- You must designate a file upload variable to receive the PDF. The variable must exist in the same event as the survey (in longitudinal projects, REDCap will prompt you to specify the event).
- If the project uses the **Multi-Language Module**, a checkbox lets you save the PDF in the translated language version.

> **Important:** If the designated file upload variable does not exist in the specified event, REDCap will return an error when a participant completes the survey. Verify the variable's event assignment before going live.

## 3.5 Survey-Specific Email Invitation Field

By default, REDCap sends survey invitations to the email address stored in the project's designated global email variable, or to the address entered in the Participant List for that record.

This setting overrides both with an instrument-specific email variable. Use this when different people should receive different surveys within the same record.

Example scenarios:
- A pediatric study where one parent is the primary contact but a second consent form goes to the other parent at a different email address.
- A thesis evaluation where each reviewer has their own copy of the same evaluation survey.

> **Note:** You must select a variable — you cannot type an email address directly. The variable must be of type **Text Box** with **Email** validation enabled.

## 3.6 Required Field Hints

Controls whether participants see a hint indicating which variables are required. Options:

- **No** — no hints are displayed.
- **Yes** — each required variable shows the text `* must provide value`.
- **Display only the red asterisk** — only the `*` symbol is shown, without the accompanying text.

> **Note:** Regardless of this setting, REDCap will still prevent survey submission and highlight unfilled required variables when a participant tries to submit without completing them.

## 3.7 Font Resize Options

Controls whether participants can resize the survey text using the resize control built into the survey interface. Disable this if you want to lock in a specific text size for all participants.

## 3.8 Aggregate Survey Results

Enables a summary display at the end of the survey showing aggregated responses across all records — useful for polling-style surveys. Options include graphical plots, numeric summaries, or both.

Two privacy safeguards are built in:
- **Minimum responses threshold** — the aggregate is not displayed until at least N responses have been collected (default: 10). Set this higher for surveys with sensitive questions.
- **Diversity toggle** — suppresses the aggregate display if all respondents selected the same option, which could effectively identify individual responses.

## 3.9 Text-to-Speech Functionality

An accessibility feature that reads survey text aloud to participants. Designed for participants with visual impairments or literacy challenges.

Options:
- **Disabled**
- **Enabled, but turned off by default** — participants can activate it manually. Choose this if only a subset of your participants may need the feature.
- **Enabled, but turned on by default** — all participants hear text-to-speech unless they turn it off. Choose this if the majority of your participants need it.

A **Language Selector** lets you choose the voice and language. This setting controls pronunciation, not translation — if your survey is in English and you select Dutch, the English words will be pronounced with Dutch phonetics, which produces unintelligible output. Always match the language selector to the language of the survey content.

> **Important:** Text vocalized by this feature is sent to a third-party text-to-speech service. This may raise privacy concerns for surveys collecting sensitive information. Consult your local IRB and REDCap support team before using this feature.

> **Note:** Your institution's REDCap administrator can disable this feature system-wide. If you do not see this option, or if you are unsure whether it is permitted at this installation, see **RC-INST-01 — Institution-Specific Settings & Policies, Section 7.3: Text-to-Speech in Surveys**.

## 3.10 Hiding Submit Buttons

If you are using a survey purely for informational display — and do not want to collect any data — you can hide the submit buttons entirely. Participants will see the content but cannot submit a response.

## 3.11 Submit Button Customizations

The three submit-related buttons (the mid-survey next/submit button, the final submit button, and the save-and-return button) can each be given custom label text. Keep labels short — button display space is limited.

> **Note:** If you use the **Multi-Language Module**, custom button text set here only applies to the base language. Labels for other languages must be configured within the Multi-Language Module.

---

# 4. Survey Access

## 4.1 Response Limit

Sets a maximum number of completed responses. Once the limit is reached, REDCap automatically takes the survey offline.

This is useful when you have a fixed capacity: for example, a class with 30 available seats. Setting the response limit to 30 prevents over-registration without requiring manual monitoring.

Configuration options:
- **Count partial completions** — choose whether incomplete responses (surveys started but not submitted) count toward the limit.
- **Custom offline message** — define a message to display when the limit is reached, similar to the standard offline message in Basic Options.

> **Note:** Partial completions are common on multi-page surveys where participants navigate away mid-survey. If you exclude partial completions from the count, some seats may appear available longer than expected.

## 4.2 Time Limit

When using REDCap's survey invitation system, this setting adds an expiration window to each individual invitation link. After the time limit elapses from the moment the invitation is sent, the link becomes invalid.

Example: You send a weekly symptom survey every Monday. Setting a 7-day time limit ensures each invitation expires before the next one is sent, so participants cannot fill out the previous week's survey after receiving a new one.

> **Note:** If you use a short time limit (minutes rather than hours), account for email and SMS delivery delays. An invitation that takes 5 minutes to arrive with a 10-minute limit gives the participant only 5 minutes to complete the survey.

> **Note:** The Time Limit setting only applies when surveys are sent via the Participant List invitation system. It does not affect the public survey link.

## 4.3 Survey Expiration

Takes the survey offline at a specific date and time — regardless of how many responses have been collected and regardless of individual invitation timing.

Example: You want registration for an event to close at midnight on the day before the event.

> **Note:** REDCap uses the **server's time zone** for the expiration, not the participant's local time zone. If your server is in a different time zone than your participants, adjust the expiration time accordingly. For this installation's server time zone, see **RC-INST-01 — Institution-Specific Settings & Policies, Section 3**.

## 4.4 Save and Return

When enabled, participants who click the **Save & Return Later** button receive a return code and a link they can use to resume their saved progress. If disabled, participants must complete the survey in a single session.

### Return Codes

By default, returning to a saved survey requires the return code provided at the time of saving. If you disable the return code requirement, anyone with the original survey link can return to and view all previously entered responses without needing the code.

- **Keep return codes enabled** for surveys collecting sensitive data.
- **Disable return codes** only when losing the code is a common support burden and the survey data is not sensitive.

## 4.5 Modifying Completed Responses

When enabled, participants can return to a survey they have already submitted and change their answers. This is useful for surveys used to collect information that participants may need to update over time — for example, contact information or availability preferences.

---

# 5. Survey Termination Options

## 5.1 Auto-Continue

If your survey is part of a sequence, **Auto-Continue** automatically advances the participant to the next survey in the sequence after they submit. You can optionally attach branching logic to make this conditional.

Example: Auto-continue only if the participant indicated consent in a prior question. Participants who did not consent are not advanced.

> **Note:** For projects with many surveys or complex routing, use the **Survey Queue** feature in the Online Designer instead of Auto-Continue. Survey Queue offers more flexibility and is easier to manage at scale.

## 5.2 Redirect to a URL

After survey completion, you can redirect participants to an external website. Paste the full URL (including `https://`) into the field.

Advanced users can pipe record or survey data into the URL if needed, but this is outside the scope of this article.

> **Note:** Redirect to URL and Survey Completion Text are mutually exclusive — you can configure one or the other, not both.

## 5.3 Survey Completion Text

An alternative to URL redirection. Displays a custom message to participants after they submit. Supports rich text editing and piping of values from the survey.

Example using piping:
```
Dear [first_name],
Thank you for completing the survey.
```
Becomes, for a participant with `first_name = "Maria"`:
```
Dear Maria,
Thank you for completing the survey.
```

For more on piping syntax, see RC-PIPE-01 — Piping: Basics, Syntax & Field Types.

> **Note:** Redirect to URL and Survey Completion Text are mutually exclusive — you can configure one or the other, not both.

## 5.4 Survey Stop Actions

When an instrument variable is configured with a **Stop Action** in the Online Designer (attached to a specific answer option), selecting that option ends the survey immediately. The Survey Settings dropdown controls what happens next:

- **Do NOT save the survey response** — REDCap discards the response. Use this for cleaner data when stopped responses are not meaningful.
- **Save the responses regardless** (default) — REDCap saves whatever was entered up to the point of the stop action.

### Alternate Survey Completion Text

An optional message displayed to participants when a stop action fires, separate from the standard completion text. Use this to provide a contextually appropriate message.

Example: "Thank you for your interest, but based on your responses you do not meet the eligibility criteria for this study."

## 5.5 e-Consent Framework and PDF Auto-Archiver

This setting has three levels:

- **Disabled** — survey completes normally with no extra steps or archiving.
- **Auto-Archiver enabled** — REDCap generates a PDF of the completed response and saves it to the **File Repository**. This is different from the Survey Response PDF Save setting in Section 3.4: no file upload variable is needed, and the PDF is stored in the File Repository rather than the dataset.
- **Auto-Archiver + e-Consent Framework** — in addition to archiving, REDCap adds a final confirmation step requiring the participant to verify that their responses are accurate before the survey is marked complete. Used primarily for electronic consent collection.

### e-Consent Variable Requirements

To use the e-Consent Framework, you must collect the participant's name and signature:
- First and last name collected as two separate text variables (best practice).
- Signature collected in a variable using the **Signature** field type.

> **Important:** Before using the e-Consent Framework for a study, confirm with your local Institutional Review Board that electronic consent collected via REDCap is acceptable at your institution. For this installation's IRB guidance on e-consent, see **RC-INST-01 — Institution-Specific Settings & Policies, Section 7.5: e-Consent Framework**.

## 5.6 Confirmation Emails

Sends an email to the participant automatically upon survey completion. When set to **Yes**, the following configuration fields appear:

- **To (email address):** REDCap determines the recipient in this order: (1) the survey-specific email field if configured (see Section 3.5), (2) the project's designated global email variable, (3) the email address in the Participant List for the record. If none of these apply, REDCap prompts the participant to enter an email address at the end of the survey. This address is not saved to the record.
- **From email:** Select from any email addresses associated with authorized project users. Optionally add a display name (e.g., "Cardiology Study Team").
- **Subject:** The email subject line. Supports piping.
- **Body:** The email body. Supports rich text editing and piping.
- **Attachment:** Attach a static file (e.g., a study flyer). You can also check a box to attach a PDF of the participant's survey responses.

Use the **Send Test Email** link in the body field header to send a preview to your own user account email address before going live.

> **Note:** Confirmation emails fire on every survey completion with no conditional logic. If you need conditional emails — for example, different emails for eligible and ineligible participants — use **Alerts & Notifications** instead (RC-ALERT-01). Alerts & Notifications supports trigger conditions, making it more flexible for complex scenarios.

---

# 6. Common Questions

**Q: How do I prevent participants from going back and changing their answers on a previous page?**
Enable **Multiple Pages** pagination and check the **Hide the "Previous Page" button** option. Participants will not be able to navigate backwards through the survey.

**Q: Can I automatically take a survey offline on a specific date?**
Yes. Use **Survey Expiration** to set a specific date and time. Note that REDCap uses the server's time zone, not the participant's.

**Q: What's the difference between Survey Expiration and the Time Limit?**
Survey Expiration sets a single absolute end date and time for the entire survey — it goes offline for everyone at once. Time Limit is per-invitation and starts counting from the moment each invitation is sent via the Participant List. They can be used independently or together.

**Q: A participant lost their return code. What are my options?**
You can look up the return code for a specific record in the Participant List. Alternatively, if lost codes are a recurring support burden, consider disabling the return code requirement — but only do this for non-sensitive surveys.

**Q: Can I use both a redirect URL and a completion message?**
No. These two options are mutually exclusive. Configure one or the other.

**Q: How do I send a consent form PDF to the participant automatically?**
Enable **Confirmation Emails** and check the box to attach a PDF of the survey responses. This sends the participant a copy of what they submitted, including any consent they acknowledged.

**Q: The e-Consent Framework is not visible in my survey settings. Why?**
Your REDCap administrator may have restricted access to e-consent features, or the feature may require additional configuration at the system level. Contact your REDCap support team.

**Q: Can a confirmation email be sent only when a certain condition is met?**
No — confirmation emails always fire on completion. For conditional emails, use **Alerts & Notifications** (RC-ALERT-01), which supports trigger logic.

---

# 7. Common Mistakes & Gotchas

**Setting Survey Expiration in the wrong time zone.** REDCap uses the server's time zone for survey expiration, not the participant's local time. Always check the server time zone (see RC-INST-01, Section 3) and calculate the correct offset before entering an expiration time. For example, if the server is set to UTC and your participants are in Central European Time (UTC+1/+2), a midnight local expiration becomes 23:00 or 22:00 UTC.

**Designating a file upload variable in the wrong event for PDF Save.** In longitudinal projects, if the file upload variable you designate for Survey Response PDF Save does not exist in the event where the survey runs, REDCap will throw an error when participants submit. Verify the variable exists in the correct event before enabling this feature.

**Using Auto-Continue instead of Survey Queue for complex multi-survey projects.** Auto-Continue works well for simple two-survey sequences. For projects with branching paths, many surveys, or conditional routing, Survey Queue provides much more control. Retrofitting a complex Auto-Continue setup to Survey Queue later is time-consuming.

**Expecting confirmation emails to handle conditional scenarios.** Confirmation emails fire for every completion. If your study has different outcomes for different participants (eligible vs. ineligible, consented vs. not consented), set up Alerts & Notifications with appropriate trigger conditions instead of relying on confirmation emails.

**Forgetting to set custom numbering after enabling it.** If you enable custom numbering but do not define numbers in the Online Designer or Data Dictionary, the survey will display no question numbers at all. This can surprise participants who expect numbered questions. Define numbers immediately after enabling, or use the auto-numbering option if branching logic has been removed.

---

# 8. Related Articles

- RC-SURV-01 — Surveys – Basics
- RC-SURV-02 — Survey Settings: Basic Options & Design
- RC-ALERT-01 — Alerts & Notifications: Setup
- RC-PIPE-01 — Piping: Basics, Syntax & Field Types
- RC-PIPE-03 — Smart Variables Overview
- RC-LONG-01 — Longitudinal Project Setup
- RC-FD-02 — Online Designer
