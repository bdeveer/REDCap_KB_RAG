RC-SURV-04

**Surveys — Survey Link Types & Access Methods**

| **Article ID** | RC-SURV-04 |
|---|---|
| **Domain** | Surveys |
| **Applies To** | All projects with surveys enabled |
| **Prerequisite** | RC-SURV-01 — Surveys – Basics |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-SURV-01 — Surveys – Basics; RC-SURV-05 — Participant List & Manual Survey Invitations; RC-PIPE-03 — Smart Variables Overview; RC-LONG-01 — Longitudinal Project Setup |

---

# 1. Overview

This article explains the two types of survey links in REDCap — public and individual — including how each works, how they behave in longitudinal projects, and how to locate any specific survey link using REDCap's built-in tools. It covers the Survey Options menu inside an instrument, the survey-related smart variables (`[survey-url]` and `[survey-link]`), and the participant list as a link lookup. This article is part of the Surveys knowledge base series.

---

# 2. Key Concepts & Definitions

**Public Survey Link**

A single survey URL that can be filled out an unlimited number of times. Each submission creates a new record. The public survey link always points to the first instrument in a project (in the first event for longitudinal projects). It is the standard method for open-enrollment distribution — email campaigns, flyers, and similar scenarios.

**Individual Survey Link**

Any survey link tied to a specific record, instrument, and (in longitudinal projects) a specific event. Individual survey links can typically be completed only once. Each "dot" on the Record Home Page corresponds to a unique individual survey link.

**Survey Options Menu**

A dropdown menu visible inside an open instrument in a record. It provides quick access to that instrument's survey link and related tools. Requires the instrument to be enabled as a survey and sufficient user rights.

**Smart Variable**

A placeholder token that REDCap replaces with dynamic content at runtime. The survey-related smart variables return the URL or clickable link for a specific survey. Full coverage of smart variables is in RC-PIPE-03 — Smart Variables Overview.

**Instrument Unique Name**

The internal name REDCap assigns to each instrument. It may differ slightly from the user-defined display name (e.g., display name "Baseline Vital Signs" → unique name `baseline_vital_signs`). Smart variables require the unique name, not the display name. The Codebook (RC-FD-05) lists both.

**Survey Access Code**

A short alphanumeric code that participants can enter into REDCap's general survey portal to reach a specific survey. Useful when a long URL is impractical (e.g., phone-based distribution).

**QR Code**

An auto-generated image that encodes a survey URL. Participants scan it with a smartphone to open the survey directly. REDCap generates a QR code for every individual survey link and public survey link automatically.

---

# 3. Public vs. Individual Survey Links

## 3.1 Public Survey Links

REDCap generates a public survey link automatically the moment the first instrument in a project is enabled as a survey. No additional configuration is required.

Each time a participant fully submits the public survey link, REDCap creates a new record. Because it can be submitted repeatedly, the same link can be shared with any number of participants. Common use cases include email campaigns, paper flyers, and embedded website forms.

The public survey link is found in the **Survey Distribution Tools** section of the project menu. See RC-SURV-01 — Surveys – Basics for the full Survey Distribution Tools walkthrough.

> **Note:** The public survey link is only available when the **first instrument** in the project is enabled as a survey. If the first instrument is not a survey, REDCap will not generate a public link.

**Why the public survey link always points to the first instrument**

REDCap stores all data in a record based on the Record ID, which lives on the first variable of the first instrument. REDCap enforces this rule to maintain database integrity — a new record cannot be created without a Record ID, and that ID must come from the first instrument.

## 3.2 Public Survey Links in Longitudinal Projects

In a standard longitudinal project, the public survey link works the same as in a classic project. The only additional requirement is that the first instrument must be assigned to the first event.

When a project has multiple arms, REDCap generates a separate public survey link for each arm where the first instrument in the first event of that arm is enabled as a survey. In the Survey Distribution Tools section, a dropdown appears prompting you to select an arm before the corresponding public link is displayed. This arm-specific routing ensures newly created records are placed in the correct arm.

## 3.3 Individual Survey Links

Every instrument enabled as a survey in a specific record gets its own individual survey link. In longitudinal projects, links are also specific to each event — the link for an instrument in Event 1 is different from the link for the same instrument in Event 2, even within the same record.

A practical shortcut: every "dot" on the Record Home Page represents one individual survey link.

Individual survey links can be completed only once by default. After submission, reloading the link shows a "survey already completed" message.

**Exception — Save and Return Later**

If a survey has the **Save and Return Later** feature enabled, participants can return to a completed survey and view or edit their responses. This is disabled by default due to privacy considerations — anyone who possesses that link can view and modify the stored data. Only enable this option when the use case explicitly requires participant-editable responses.

---

# 4. Finding a Specific Survey Link

REDCap provides three methods for locating an individual survey link for a specific record.

## 4.1 Survey Options Menu (Inside the Instrument)

When you open an instrument for a specific record, a **Survey Options** dropdown is visible at the top of the data entry page (provided the instrument is enabled as a survey and you have sufficient user rights). It contains four options:

| Option | What It Does |
|---|---|
| Open Survey | Opens the survey in a new browser tab. Copy the URL from the address bar. |
| Log Out + Open Survey | Opens the survey in a new tab and logs you out of REDCap simultaneously. Use this when handing your device directly to a participant. |
| Compose Survey Invitation | Opens the invitation composer for that specific survey in that record. Useful for sending a one-off email invitation. |
| Survey Access Code + QR Code | Displays the short access code and the QR code for that specific survey link. |

## 4.2 Survey Smart Variables

Smart variables can be used anywhere REDCap processes piped content — survey invitation emails, Alerts & Notifications, instrument fields (with some restrictions). There are two survey smart variables: `[survey-url]` and `[survey-link]`.

### `[survey-url]` — Returns the full URL as plain text

| Syntax | When to Use |
|---|---|
| `[survey-url]` | Only in the survey invitation composer for that instrument. REDCap infers which instrument to link to automatically. Does not work in alerts, notifications, or instrument fields. |
| `[survey-url:instrument]` | Works anywhere piping is supported. Requires the instrument's unique name. Example: `[survey-url:baseline_vitals]` |
| `[event][survey-url:instrument]` | Use in longitudinal projects to also specify the event. Example: `[event_1_arm_1][survey-url:baseline_vitals]` |

### `[survey-link]` — Returns a clickable hyperlink

| Syntax | When to Use |
|---|---|
| `[survey-link]` | Only in the survey invitation composer. The link label is the instrument's display name. |
| `[survey-link:instrument]` | Works anywhere piping is supported. The link label is the instrument's display name. |
| `[survey-link:instrument:Custom Text]` | Same as above, but the link label is the text you define. Example: `[survey-link:baseline_vitals:Take Our Baseline Survey]` |

> **Tip — Finding the Instrument Unique Name:** Smart variables require the unique name of an instrument, not its display name. The easiest way to find it is in the Codebook (under Project Home and Design), where instruments are listed as: `Display Name (unique_name)`. See RC-FD-05 — Codebook.

> **Tip — Longitudinal projects:** Always include the event qualifier when using an instrument-specific smart variable in a longitudinal project. Without it, REDCap may not resolve the link correctly if the instrument appears in multiple events.

## 4.3 Participant List

The participant list in Survey Distribution Tools displays individual survey links for records that meet either of these conditions:

- At least one data point has been saved in the record.
- An email address has been added for that record via the **Add Participant** function.

To locate a specific link: navigate to the participant list, select the correct instrument (and event, in longitudinal projects), find the record or email in the list, and click the link icon in the **Link** column. The link icon is absent for surveys that are already completed.

Full documentation of the participant list is in RC-SURV-05 — Participant List & Manual Survey Invitations.

**Identified vs. anonymous mode in the participant list**

By default, the participant list runs in anonymous mode, which makes it difficult to associate a specific link with a specific person. To switch to identified mode (enabling a clickable Record ID column), either:

- Add a **participant identifier** (name) alongside the email when using **Add Participant**, or
- Designate an email field for the project in Project Setup → Enable Optional Modules and Customizations.

---

# 5. Common Questions

**Q: What is the difference between a public survey link and an individual survey link?**

**A:** A public survey link can be submitted any number of times; each submission creates a new record. An individual survey link is tied to one specific record, instrument, and event, and can typically only be submitted once.

**Q: Can I use the public survey link for follow-up surveys?**

**A:** No. The public survey link always points to the first instrument in the project (in the first event for longitudinal projects) because that is where the Record ID lives. Follow-up surveys are reached via individual survey links, sent through the participant list, Automated Survey Invitations, or the Survey Queue.

**Q: A participant says they see "this survey has already been completed" when they click the link. What happened?**

**A:** They received an individual survey link that was already submitted. If you want participants to be able to return and edit their responses, enable the **Save and Return Later** option (with the sub-option to allow returning to completed surveys) in that survey's settings. If they should be starting a fresh response, use the public survey link or create a new record.

**Q: Where do I find the instrument's unique name for use in smart variables?**

**A:** In the Codebook (Project Home and Design → Codebook). Each instrument is listed with its display name followed by its unique name in parentheses. See RC-FD-05 — Codebook.

**Q: Can I use `[survey-url]` (without the instrument name) in an Alert & Notification?**

**A:** No. The bare `[survey-url]` token only works inside a survey invitation composer, where REDCap already knows which instrument the invitation is for. In Alerts & Notifications, use `[survey-url:instrument_name]` and specify the instrument explicitly.

**Q: Does a QR code expire?**

**A:** A QR code is simply an encoded version of the underlying survey URL. It remains valid as long as the survey link itself is active. The link becomes inactive when the survey is completed (for individual links) or when the project is taken offline.

**Q: In a multi-arm longitudinal project, how many public survey links are there?**

**A:** One per arm, provided the first instrument in the first event of each arm is enabled as a survey. REDCap displays an arm selector in Survey Distribution Tools so you can retrieve the correct link for each arm.

---

# 6. Common Mistakes & Gotchas

**Distributing an individual survey link as if it were a public link.** An individual survey link can only be completed once. If the wrong link is shared broadly, participants will see the "already completed" error after the first submission. Always verify you are sharing the public link (found in Survey Distribution Tools) when open-enrollment behavior is intended.

**Using `[survey-url]` in an Alert or Notification without specifying the instrument name.** The bare token only resolves inside the survey invitation composer. In any other context, include the instrument's unique name: `[survey-url:instrument_name]`.

**Using the display name instead of the unique name in smart variables.** `[survey-url:Baseline Vital Signs]` will not work. REDCap requires the unique name (e.g., `[survey-url:baseline_vital_signs]`). Spaces and capitalization differences are common sources of failure.

**Expecting a survey link to appear in the participant list for a brand-new record with no data.** REDCap only generates individual survey links once at least one data point is saved, or once a participant's email has been added via Add Participant. Empty records do not appear.

**Omitting the event qualifier in longitudinal smart variables.** When the same instrument exists in multiple events, REDCap cannot determine which event's link to return without an explicit event qualifier. Always include `[event_name]` before the smart variable in longitudinal projects.

---

## API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See RC-API-01 — REDCap API for authentication, token management, and setup.

- **RC-API-40 — Export Survey Link API** — programmatically retrieve a unique survey link for a specific record and instrument

---


# 7. Related Articles

- RC-SURV-01 — Surveys – Basics (enabling surveys, Survey Distribution Tools, public link walkthrough)
- RC-SURV-02 — Survey Settings: Basic Options & Design
- RC-SURV-03 — Survey Settings: Behavior, Access & Termination (Save and Return Later setting)
- RC-SURV-05 — Participant List & Manual Survey Invitations (full participant list documentation)
- RC-PIPE-03 — Smart Variables Overview (full catalog of smart variables)
- RC-FD-05 — Codebook (finding instrument unique names)
- RC-LONG-01 — Longitudinal Project Setup (arms, events)
