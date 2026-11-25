

**Survey Settings: Behavior, Access & Termination**

| **Article ID** | [RC-SURV-03 — Survey Settings: Behavior, Access & Termination](RC-SURV-03_Survey-Settings-Behavior-Access-and-Termination.md) |
|---|---|
| **Domain** | Surveys |
| **Applies To** | All REDCap projects with surveys enabled; some settings require additional project features (Repeat Survey needs a repeating instrument; Time Limit needs the Participant List invitation system) |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — survey settings behaviour checked against source code; pages not re-captured |
| **Prerequisite** | [RC-SURV-01 — Surveys – Basics](RC-SURV-01_Surveys-Basics.md); [RC-SURV-02 — Survey Settings: Basic Options & Design](RC-SURV-02_Survey-Settings-Basic-Options-and-Design.md) |
| **Version** | 1.4 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-SURV-01 — Surveys – Basics](RC-SURV-01_Surveys-Basics.md); [RC-SURV-02 — Survey Settings: Basic Options & Design](RC-SURV-02_Survey-Settings-Basic-Options-and-Design.md); [RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md); [RC-PIPE-01 — Piping: Basics, Syntax & Field Types](RC-PIPE-01_Piping-Basics-Syntax-and-Field-Types.md); [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md) |
| **Synonyms** | how do i set a survey expiration date; limit who can access a survey; what happens after a participant submits a survey; survey termination and redirect options; set a survey time limit; save and return later setting; control survey access and behavior; show a custom message when a survey closes |

---

## 1. Overview

This article is the second of a two-part series on the REDCap Survey Settings page. It covers three sections of the settings page: **Survey Customizations** (behavioral options that affect how participants interact with the survey), **Survey Access** (rules that govern who can access the survey and for how long), and **Survey Termination Options** (what happens after a participant submits or is stopped). The companion article, [RC-SURV-02 — Survey Settings: Basic Options & Design](RC-SURV-02_Survey-Settings-Basic-Options-and-Design.md), covers the Basic Options and Design sections.

---

## 2. Key Concepts & Definitions

### Survey Customizations

A collection of settings that govern specific behaviors during survey completion — question numbering, pagination, PDF handling, accessibility, and button labels.

### Pagination

The division of a survey into multiple pages. In REDCap, page breaks are defined by the placement of **Section Header** field types within the instrument. Each section header marks the start of a new page when pagination is enabled.

### Section Header

A field type in REDCap that displays a visual divider and optional heading text in an instrument. When pagination is set to **Multiple Pages**, each section header begins a new survey page.

### Survey Access

Settings that define when, how often, and under what conditions a participant can access a survey: response limits, time limits, expiration dates, and save-and-return behavior.

### Save and Return

A feature that allows a participant to pause a survey mid-completion, receive a return code, and resume later without starting over.

### Return Code

A system-generated alphanumeric code given to a participant when they save their progress. Required to resume a saved survey unless the return-code requirement is disabled.

### Survey Termination Options

Settings that control what happens after a participant submits a survey or triggers a stop action: auto-continue, redirection, completion messages, stop-action behavior, and confirmation emails. (e-Consent and PDF archiving are configured elsewhere — see Section 5.5.)

### Stop Action

A condition attached to a specific answer option in the Online Designer. When a participant selects that option, the survey ends immediately. The Survey Settings page controls what happens to the data and what message the participant sees when a stop action fires.

### e-Consent Framework

A REDCap feature that requires a participant to confirm the accuracy of their responses before the survey is marked complete. Commonly used for electronic consent forms. Generates an auto-archived PDF of the completed consent. It is set up on the **e-Consent** page of the Online Designer, not on the Survey Settings page — see [RC-SURV-08 — e-Consent Framework Setup and Management](RC-SURV-08_e-Consent-Framework-Setup-and-Management.md).

### Auto-Archiver

Automatic generation of a PDF of a completed survey response, stored with the project. In current REDCap this is handled by **PDF Snapshots** (and by e-Consent), configured from the Online Designer rather than the Survey Settings page — see [RC-SURV-09 — PDF Snapshots of Records](RC-SURV-09_PDF-Snapshots-of-Records.md).

### Confirmation Email

An email sent to a participant automatically after they complete a survey. Distinct from Alerts & Notifications — confirmation emails are configured per survey and fire only on completion.

---

## 3. Survey Customizations

### 3.1 Question Numbering

REDCap can display a number before each question on the survey. This setting has two modes:

- **Auto-numbering** — REDCap assigns sequential numbers (1, 2, 3...) automatically. Not available when the instrument contains branching logic.
- **Custom numbered** — Numbers are defined manually, per variable. This is the default for a newly enabled survey, so a new survey shows no question numbers until you either enter custom numbers or switch to auto-numbering.

**Why branching logic disables auto-numbering:** When questions are conditionally hidden or shown, sequential numbers create gaps in the participant's view (e.g., the participant sees question 1, then question 4). This is confusing. Custom numbering lets you assign context-appropriate labels (e.g., `4a`, `IIIb`, `2.1`) that remain meaningful when questions are skipped.

Custom numbers are set in two ways:
- Per-variable in the **Online Designer** (an extra number field appears when custom numbering is enabled).
- In bulk via the **Data Dictionary** (faster for instruments with many variables).

> **Note:** With custom numbering and no numbers defined, your survey displays no question numbers at all. Because **Custom numbered** is the default for new surveys, this is what a new survey looks like out of the box. It is a valid choice if you prefer an unnumbered survey.

### 3.2 Pagination

This setting controls whether the entire survey is displayed as a single scrolling page or broken into multiple pages.

- **Single Page** (default) — all questions appear on one page.
- **Multiple Pages** — the survey is split at each **Section Header** field. Each section header starts a new page.

When **Multiple Pages** is selected, two additional options become available:

- **Display page numbers** — shows participants how far through the survey they are (e.g., "Page 2 of 5").
- **Hide the "Previous Page" button** — removes the back-navigation button, preventing participants from returning to earlier pages. Useful when you display calculated scores on a final page and do not want participants to go back and alter the inputs that feed those calculations.

### 3.3 PDF Download

This toggle controls whether participants are offered a **Download PDF** button after completing the survey. When enabled, participants can download a PDF of their own responses.

This is a popular option for registration forms and consent-adjacent surveys where participants want a copy of what they submitted.

### 3.4 Saving a PDF of the Response to the Record

Saving a PDF copy of a completed response automatically — into a file upload variable, to the File Repository, or in a translated language — is **not** configured on the Survey Settings page. It is set up from the Online Designer:

- For consent workflows, use the **e-Consent** page — see [RC-SURV-08 — e-Consent Framework Setup and Management](RC-SURV-08_e-Consent-Framework-Setup-and-Management.md).
- For any other automatic PDF copy, use **PDF Snapshots** — see [RC-SURV-09 — PDF Snapshots of Records](RC-SURV-09_PDF-Snapshots-of-Records.md).

### 3.5 Survey-Specific Email Invitation Field

By default, REDCap sends survey invitations to the email address stored in the project's designated global email variable, or to the address entered in the Participant List for that record.

This setting overrides both with an instrument-specific email variable. Use this when different people should receive different surveys within the same record.

Example scenarios:
- A pediatric study where one parent is the primary contact but a second consent form goes to the other parent at a different email address.
- A thesis evaluation where each reviewer has their own copy of the same evaluation survey.

> **Note:** You must select a variable — you cannot type an email address directly. The variable must be of type **Text Box** with **Email** validation enabled.

### 3.6 Required Field Hints

Controls whether participants see a hint indicating which variables are required. Options:

- **No** — no hints are displayed.
- **Yes** — each required variable shows the text `* must provide value`.
- **Display only the red asterisk** — only the `*` symbol is shown, without the accompanying text.

> **Note:** Regardless of this setting, REDCap will still prevent survey submission and highlight unfilled required variables when a participant tries to submit without completing them.

### 3.7 Font Resize Options

Controls whether participants can resize the survey text using the resize control built into the survey interface. Disable this if you want to lock in a specific text size for all participants.

### 3.8 Aggregate Survey Results

Enables a summary display at the end of the survey showing aggregated responses across all records — useful for polling-style surveys. Options include graphical plots, numeric summaries, or both.

Two privacy safeguards are built in:
- **Minimum responses threshold** — the aggregate is not displayed until at least N responses have been collected (default: 10). Set this higher for surveys with sensitive questions.
- **Diversity check** — hides the plot or summary for an individual question when its responses are not diverse enough (for example, everyone chose the same option), which could effectively identify individual responses. The rest of the results page still displays.

### 3.9 Text-to-Speech Functionality

An accessibility feature that reads survey text aloud to participants. Designed for participants with visual impairments or literacy challenges.

> **Note — this is not screen-reader support.** Text-to-speech is a convenience for participants who do not use assistive technology of their own. A participant running their own screen reader is not helped by it, and the two can compete. It also does nothing for keyboard navigation, contrast or label quality. See [RC-SURV-11 — Accessibility in REDCap Surveys & Forms](RC-SURV-11_Accessibility-in-Surveys-and-Forms.md).

Options:
- **Disabled**
- **Enabled, but turned off by default** — participants can activate it manually. Choose this if only a subset of your participants may need the feature.
- **Enabled, but turned on by default** — all participants hear text-to-speech unless they turn it off. Choose this if the majority of your participants need it.

A **Language Selector** lets you choose the voice and language. This setting controls pronunciation, not translation — if your survey is in English and you select Dutch, the English words will be pronounced with Dutch phonetics, which produces unintelligible output. Always match the language selector to the language of the survey content.

> **Important:** Text vocalized by this feature is sent to a third-party text-to-speech service. This may raise privacy concerns for surveys collecting sensitive information. Consult your local IRB and REDCap support team before using this feature.

> **Note:** Your institution's REDCap administrator can disable this feature system-wide. If you do not see this option, or if you are unsure whether it is permitted at this installation, see **[RC-INST-01 — Institution-Specific Settings & Policies — Production](RC-INST-01_Institution-Specific-Settings-and-Policies.md) — Institution-Specific Settings & Policies, Section 7.3: Text-to-Speech in Surveys**.

### 3.10 Hiding Submit Buttons

If you are using a survey purely for informational display — and do not want to collect any data — you can hide the submit buttons entirely. Participants will see the content but cannot submit a response.

### 3.11 Submit Button Customizations

Three navigation buttons can each be given custom label text: **<< Previous Page**, **Next Page >>** and **Submit**. The **Save & Return Later** button is not one of them. Keep labels short — button display space is limited.

> **Note:** If you use the **Multi-Language Module**, custom button text set here only applies to the base language. The Multi-Language Module can translate these labels for other languages.

### 3.12 Repeat Survey

This option is offered only when the instrument is set up as a **repeating instrument**. When enabled, a button lets the participant start a **new instance** of the same survey **in the same record** — for example, logging another medication, visit or incident without needing a new link.

Configuration options:
- **Button text** — customize the label on the button (e.g., "Add another medication"). If left blank, REDCap uses **Take this survey again**.
- **Button location**:
  - **Before completion** — shown next to the **Submit** button on the survey.
  - **After completion** — shown on the completion screen, below the survey completion text.
  - **Do not display** — no button on the survey.

When the option is on, the repeat option also appears in the **Survey Queue**.

> **Note:** Repeat Survey does **not** create a new record. If you want separate, anonymous submissions from one link (polling, a suggestion box), use the **public survey link** instead: every visit to the public link creates a new record.

> **Note:** Repeat Survey is distinct from **Modify Completed Response** (Section 4.5). Repeat Survey starts a new instance; Modify Completed Response reopens the participant's prior submission for editing. Do not confuse the two — see also Section 7 (Common Mistakes & Gotchas).

---

## 4. Survey Access

### 4.1 Response Limit

Sets a maximum number of responses. Once the limit is reached, anyone trying to **start** the survey sees the limit message instead. The survey itself is not switched offline.

This is useful when you have a fixed capacity: for example, a class with 30 available seats. Setting the response limit to 30 prevents over-registration without requiring manual monitoring.

Configuration options:
- **Which responses count** — by default both partial (started but not submitted) and completed responses count toward the limit. You can choose to count completed responses only.
- **Custom message** — define the message shown to new participants once the limit is reached.

How the limit behaves:
- **People already in progress can still finish.** A participant who started before the limit was reached — or who returns later with a return code — can still complete the survey. With a "completed responses only" limit, the final count can therefore slightly exceed the number you set.
- **Counted per event.** In a longitudinal project, each event has its own count.
- **Once reached**, the survey drops out of the **Survey Queue** and **Auto-Continue**, and Automated Survey Invitations no longer schedule it.
- **Deleting responses reopens it.** If responses are deleted and the count falls below the limit, new participants can start again. Invitations that were not scheduled while the limit was reached are not sent retroactively.

> **Note:** Partial completions are common on multi-page surveys where participants navigate away mid-survey. If you exclude partial completions from the count, some seats may appear available longer than expected.

### 4.2 Time Limit

When using REDCap's survey invitation system, this setting adds an expiration window to each participant's survey link.

- **When the clock starts:** at the **first** invitation REDCap sends for that survey — from **Compose Survey Invitations** or an Automated Survey Invitation. Reminders and re-sent invitations do not reset it.
- **When it runs out:** the participant can no longer begin or continue the survey, even with a return code. Data they already saved is kept.
- **Links shared other ways never expire.** A survey link piped into an email or alert, or copied and sent by hand, is not subject to the time limit.
- **Per-participant override:** you can set a different limit for an individual participant in the **Participant List**. If you later change the survey's time limit, REDCap recalculates the deadline for everyone except participants with an override.

Example: You send a weekly symptom survey every Monday. Setting a 7-day time limit ensures each invitation expires before the next one is sent, so participants cannot fill out the previous week's survey after receiving a new one.

> **Note:** If you use a short time limit (minutes rather than hours), account for email and SMS delivery delays. An invitation that takes 5 minutes to arrive with a 10-minute limit gives the participant only 5 minutes to complete the survey.

> **Note:** The Time Limit setting only applies when surveys are sent via REDCap's invitation system. It does not apply to the public survey link.

### 4.3 Survey Expiration

Takes the survey offline at a specific date and time — regardless of how many responses have been collected and regardless of individual invitation timing.

Example: You want registration for an event to close at midnight on the day before the event.

The survey goes offline as soon as the set time passes: REDCap checks the expiration whenever someone opens the survey, so there is no grace period. A scheduled background job also takes expired surveys offline.

> **Version caveat (Standard 17.6 only; not LTS):** On 17.6 an **Expire survey** entry is written to the project's logging when a survey expires, but it may be missing if a participant opened the survey after the expiration time had passed. LTS versions (17.3.x, 16.0.x) do not log it at all. Do not rely on the logging to prove when a survey closed — keep your own record of the expiration date you set, and check the **Survey Status** on the Survey Settings page.

**Re-activating an expired survey:** clear or change the expiration date first. If you only set the survey back online and leave the past date in place, it goes offline again.

> **Note:** REDCap uses the **server's time zone** for the expiration (the time shown is server time), not the participant's local time zone. If your server is in a different time zone than your participants, adjust the expiration time accordingly. For this installation's server time zone, see **[RC-INST-01 — Institution-Specific Settings & Policies — Production](RC-INST-01_Institution-Specific-Settings-and-Policies.md) — Institution-Specific Settings & Policies, Section 3**.

### 4.4 Save and Return

When enabled, participants who click the **Save & Return Later** button receive a return code and a link they can use to resume their saved progress. If disabled, participants must complete the survey in a single session.

#### Return Codes

By default, returning to a saved survey requires the return code provided at the time of saving. If you disable the return code requirement, anyone with the original survey link can return to and view all previously entered responses without needing the code.

- **Keep return codes enabled** for surveys collecting sensitive data.
- **Disable return codes** only when losing the code is a common support burden and the survey data is not sensitive.

Both **return without a return code** and **modify completed responses** (Section 4.5) are sub-options of Save & Return — they only work when Save & Return is enabled. When **Survey Login** applies to the survey, the login replaces return codes as the way a participant gets back in (see [RC-SURV-10 — Survey Login](RC-SURV-10_Survey-Login.md)).

> **Note:** A return code does not override other access rules. If the survey is offline, has passed its expiration date, or the participant's time limit has run out, the return code no longer gets them in. Their partial data is kept.

**Scope of a return code.** A return code is valid **only for the participant-specific survey link it was issued against**. It is not a project-wide password: entering a valid code on a different participant's link must not grant access to that participant's responses.

> **Critical — version caveat (all versions below 17.4.1 Standard / 17.3.7 LTS):** That scoping did not hold. If a participant obtained another participant's individual survey link — not the public survey link — their **own** return code would let them open the other participant's saved responses. Fixed in 17.4.1 / 17.3.7. On any earlier version, a return code effectively works against any individual link in the project, so the confidentiality of partially-completed responses depends on individual survey links never being shared or guessed. If you run partially-completed surveys containing sensitive data on an affected version, this is a reason to prioritise the upgrade.

> **Version caveat (below 17.5.1 Standard / 17.3.14 LTS):** Return codes were not always **reserved atomically** when a response was first created or Save & Return was first used. Under concurrent activity a code could be reused, or associated with the wrong response. This is a different defect from the scoping problem above, and fixed later.

> **Version caveat (≤17.0.2):** In a project with a public survey using Save & Return Later, where records were created through a data entry form rather than through the public survey, a participant entering their return code on the **public** survey link was told the code was incorrect. They must use their own unique survey link. Fixed in 17.0.3.

> **Note (15.4.5+):** The text beneath the Save & Return Later email option now tells participants that while their email address is not stored with their survey responses, it **is** retained in the system's email logs. This was a deliberate transparency change; if your consent materials describe what happens to a participant's email address, they should match.

### 4.5 Modifying Completed Responses

When enabled, participants can return to a survey they have already submitted and change their answers. This is useful for surveys used to collect information that participants may need to update over time — for example, contact information or availability preferences.

- Requires **Save & Return** to be enabled.
- Is switched off automatically when the **e-Consent Framework** is enabled for the survey.
- A modified response stays **complete**; its completion time is updated to the time of the latest submission.

> **Important:** If you combine **return without a return code** with **modify completed responses**, anyone who has the survey link can open and change a completed response. Use this combination only for non-sensitive surveys where links are not shared.

### 4.6 CAPTCHA on the Public Survey Link

A CAPTCHA option can be enabled to help stop automated (bot) submissions. It applies only to the **public survey link**; participant-specific links are not affected.

---

## 5. Survey Termination Options

### 5.1 Auto-Continue

If your survey is part of a sequence, **Auto-Continue** automatically advances the participant to the next survey in the sequence after they submit. You can optionally attach branching logic to make this conditional.

Example: Auto-continue only if the participant indicated consent in a prior question. Participants who did not consent are not advanced.

- Auto-Continue only moves to the next survey **within the same event**. In a longitudinal project it does not jump to a survey in a later event.
- REDCap skips any next survey that is offline, past its expiration date, at its response limit, or hidden by **Form Display Logic**, and moves on to the one after it.
- The end-of-survey **Download PDF** option (Section 3.3) is not offered when Auto-Continue — or a Survey Queue survey set to start automatically — takes the participant straight to another survey.

> **Version caveat (17.x only):** Auto-Continue can optionally show a REDCap SHARE prompt before the next survey. This option does not exist on 16.0.x LTS; if you rely on it, confirm your instance is on 17.x.

> **Note:** For projects with many surveys or complex routing, use the **Survey Queue** feature in the Online Designer instead of Auto-Continue. Survey Queue offers more flexibility and is easier to manage at scale.

### 5.2 Redirect to a URL

After survey completion, you can redirect participants to an external website. Paste the full URL (including `https://`) into the field.

Advanced users can pipe record or survey data into the URL if needed, but this is outside the scope of this article.

> **Note:** Redirect to URL and Survey Completion Text are mutually exclusive — you can configure one or the other, not both.

### 5.3 Survey Completion Text

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

For more on piping syntax, see [RC-PIPE-01 — Piping: Basics, Syntax & Field Types](RC-PIPE-01_Piping-Basics-Syntax-and-Field-Types.md).

> **Note:** Redirect to URL and Survey Completion Text are mutually exclusive — you can configure one or the other, not both.

### 5.4 Survey Stop Actions

When an instrument variable is configured with a **Stop Action** in the Online Designer (attached to a specific answer option), selecting that option ends the survey immediately. The Survey Settings dropdown controls what happens next:

- **Do NOT save the survey response** — REDCap discards the response, including data saved on earlier pages of the survey. If the record has no other data, the record itself is deleted. The event is logged as the survey ending via a Stop Action. No Auto-Continue, redirect or confirmation email follows. Data on a locked record or locked instrument is not deleted. Use this for cleaner data when stopped responses are not meaningful.
- **Save the responses regardless** (default) — REDCap saves whatever was entered up to the point of the stop action.

#### Alternate Survey Completion Text

An optional message displayed to participants when a stop action fires, separate from the standard completion text. Use this to provide a contextually appropriate message.

Example: "Thank you for your interest, but based on your responses you do not meet the eligibility criteria for this study."

### 5.5 e-Consent and PDF Archiving

The e-Consent Framework and automatic PDF archiving of responses are **not** set on the Survey Settings page. They are configured from the Online Designer:

- **e-Consent** — the consent confirmation step, required name and signature variables, and the archived consent PDF. See [RC-SURV-08 — e-Consent Framework Setup and Management](RC-SURV-08_e-Consent-Framework-Setup-and-Management.md).
- **PDF Snapshots** — automatic PDF copies of responses saved to a file upload variable or the File Repository. See [RC-SURV-09 — PDF Snapshots of Records](RC-SURV-09_PDF-Snapshots-of-Records.md).

> **Important:** Before using the e-Consent Framework for a study, confirm with your local Institutional Review Board that electronic consent collected via REDCap is acceptable at your institution. For this installation's IRB guidance on e-consent, see **[RC-INST-01 — Institution-Specific Settings & Policies — Production](RC-INST-01_Institution-Specific-Settings-and-Policies.md) — Institution-Specific Settings & Policies, Section 7.5: e-Consent Framework**.

### 5.6 Confirmation Emails

Sends an email to the participant automatically upon survey completion. When set to **Yes**, the following configuration fields appear:

- **To (email address):** if a survey-specific email field is configured (see Section 3.5) and has a value, that address wins. If it is blank, REDCap uses the participant's email address in the **Participant List**. If no address is available, REDCap prompts the participant to enter an email address at the end of the survey. This address is not saved to the record.
- **From email:** Select from any email addresses associated with authorized project users. Optionally add a display name (e.g., "Cardiology Study Team").
- **Subject:** The email subject line. Supports piping.
- **Body:** The email body. Supports rich text editing and piping.
- **Attachment:** Attach a static file (e.g., a study flyer). You can also check a box to attach a PDF of the participant's survey responses.

Use the **Send Test Email** link in the body field header to send a preview to your own user account email address before going live.

> **Note:** Confirmation emails fire on every survey completion with no conditional logic. If you need conditional emails — for example, different emails for eligible and ineligible participants — use **Alerts & Notifications** instead ([RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md)). Alerts & Notifications supports trigger conditions, making it more flexible for complex scenarios.

---

## 6. Common Questions

**Q: How do I prevent participants from going back and changing their answers on a previous page?**
Enable **Multiple Pages** pagination and check the **Hide the "Previous Page" button** option. Participants will not be able to navigate backwards through the survey.

**Q: Can I automatically take a survey offline on a specific date?**
Yes. Use **Survey Expiration** to set a specific date and time. Note that REDCap uses the server's time zone, not the participant's.

**Q: What's the difference between Survey Expiration and the Time Limit?**
Survey Expiration sets a single absolute end date and time for the entire survey — it goes offline for everyone at once. Time Limit is per participant and starts counting from the first invitation REDCap sends them (Compose Survey Invitations or an Automated Survey Invitation); reminders do not reset it, and links shared other ways never expire. They can be used independently or together.

**Q: A participant lost their return code. What are my options?**
Return codes are not shown in the Participant List. Open the record's instrument on the data entry form and use the survey options menu — it shows **Return Code for participant to continue survey**. Return codes can also be exported with the **Return Codes for Surveys** option in Data Export, or retrieved through the API. Alternatively, if lost codes are a recurring support burden, consider disabling the return code requirement — but only do this for non-sensitive surveys.

**Q: Can participants submit the same survey more than once?**
It depends on what you want. If the instrument is a repeating instrument, enable **Repeat Survey** (Section 3.12): the participant can start a new instance of the survey in the **same record**, with the button shown next to Submit or after completion. If you want separate, anonymous submissions from one link, use the **public survey link** — every visit creates a new record. Both are different from **Modify Completed Response** (Section 4.5), which reopens the existing submitted response for editing.

**Q: Can I use both a redirect URL and a completion message?**
No. These two options are mutually exclusive. Configure one or the other.

**Q: How do I send a consent form PDF to the participant automatically?**
Enable **Confirmation Emails** and check the box to attach a PDF of the survey responses. This sends the participant a copy of what they submitted, including any consent they acknowledged.

**Q: The e-Consent Framework is not visible in my survey settings. Why?**
It is not on the Survey Settings page. e-Consent is configured from the **e-Consent** page of the Online Designer — see [RC-SURV-08 — e-Consent Framework Setup and Management](RC-SURV-08_e-Consent-Framework-Setup-and-Management.md). If you cannot find it there either, your REDCap administrator may have restricted it; contact your REDCap support team.

**Q: Can a confirmation email be sent only when a certain condition is met?**
No — confirmation emails always fire on completion. For conditional emails, use **Alerts & Notifications** ([RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md)), which supports trigger logic.

---

## 7. Common Mistakes & Gotchas

**Setting Survey Expiration in the wrong time zone.** REDCap uses the server's time zone for survey expiration, not the participant's local time. Always check the server time zone (see [RC-INST-01 — Institution-Specific Settings & Policies — Production](RC-INST-01_Institution-Specific-Settings-and-Policies.md), Section 3) and calculate the correct offset before entering an expiration time. For example, if the server is set to UTC and your participants are in Central European Time (UTC+1/+2), a midnight local expiration becomes 23:00 or 22:00 UTC.

**Expecting "Do NOT save" to keep earlier pages.** On a multi-page survey, a stop action set to **Do NOT save the survey response** discards everything the participant entered — including pages already saved — and deletes the record if it has nothing else in it. Use **Save the responses regardless** if you need to keep screening answers.

**Combining "return without a return code" with "modify completed responses".** Together these let anyone who has the survey link change a completed response. Keep return codes on for any survey whose completed responses matter.

**Using Auto-Continue instead of Survey Queue for complex multi-survey projects.** Auto-Continue works well for simple two-survey sequences. For projects with branching paths, many surveys, or conditional routing, Survey Queue provides much more control. Retrofitting a complex Auto-Continue setup to Survey Queue later is time-consuming.

**Expecting confirmation emails to handle conditional scenarios.** Confirmation emails fire for every completion. If your study has different outcomes for different participants (eligible vs. ineligible, consented vs. not consented), set up Alerts & Notifications with appropriate trigger conditions instead of relying on confirmation emails.

**Expecting question numbers on a new survey.** New surveys default to **Custom numbered**, so unless you define numbers in the Online Designer or Data Dictionary, the survey displays no question numbers at all. Define custom numbers, or switch to auto-numbering (available only if the instrument has no branching logic).

**Confusing Repeat Survey with Modify Completed Response.** Both features let a participant "go back to a survey," but they are fundamentally different. Repeat Survey (repeating instruments only) adds a new instance in the same record; Modify Completed Response reopens the existing submitted response for editing. For studies where you want one authoritative response per participant that can be updated, use Modify Completed Response. For repeated entries by the same participant (another visit, another medication), use Repeat Survey. For anonymous or polling surveys where each visit should be a separate record, use the public survey link. Using the wrong one creates either extra instances or unintended overwrites.

**Child-setting defaults persist in the CSV export even when the parent feature is off.** When you export Survey Settings, fields like `response_limit_include_partials`, `min_responses_view_results`, and `repeat_survey_btn_location` always carry default values regardless of whether their parent feature (response limit, aggregate results, repeat survey) is enabled. If you copy these settings to another project via CSV, those defaults become active if the parent feature is later turned on — without any further configuration needed or expected. This is generally convenient, but verify child settings whenever enabling a feature for the first time on a project that was set up via CSV copy.

---

### API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) for authentication, token management, and setup.

- **[RC-API-42 — Export Survey Return Code API](RC-API-42_Export-Survey-Return-Code.md)** — programmatically retrieve the return code for a specific participant, used to re-enter a partially completed survey

---


## 8. Related Articles

- [RC-SURV-01 — Surveys – Basics](RC-SURV-01_Surveys-Basics.md)
- [RC-SURV-02 — Survey Settings: Basic Options & Design](RC-SURV-02_Survey-Settings-Basic-Options-and-Design.md)
- [RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md)
- [RC-PIPE-01 — Piping: Basics, Syntax & Field Types](RC-PIPE-01_Piping-Basics-Syntax-and-Field-Types.md)
- [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md)
- [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md)
- [RC-FD-02 — Online Designer](RC-FD-02_Online-Designer.md)
- [RC-SURV-10 — Survey Login](RC-SURV-10_Survey-Login.md)
