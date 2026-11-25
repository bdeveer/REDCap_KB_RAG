---
id: RC-SURV-04
title: Surveys — Survey Link Types & Access Methods
domain: Surveys
applies_to:
- All projects with surveys enabled
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — survey
  behaviour checked against source code; pages not re-captured
prerequisites:
- RC-SURV-01 — Surveys – Basics
version: '1.1'
last_updated: 2026-11
related:
- id: RC-SURV-01
  title: Surveys – Basics
- id: RC-SURV-05
  title: Participant List & Manual Survey Invitations
- id: RC-PIPE-03
  title: Smart Variables Overview
- id: RC-LONG-01
  title: Longitudinal Project Setup
tags:
- surveys
synonyms:
- difference between public and individual survey links
- how do i find a survey link
- get the public survey url
- where is the survey link for a specific record
- one survey link per participant
- survey-url and survey-link smart variables
- reuse a survey link or fill it out multiple times
- how survey links work in longitudinal projects
---

# 1. Overview

This article explains the two types of survey links in REDCap — public and individual — including how each works, how they behave in longitudinal projects, and how to locate any specific survey link using REDCap's built-in tools. It covers the Survey Options menu inside an instrument, the survey-related smart variables (`[survey-url]` and `[survey-link]`), and the participant list as a link lookup. This article is part of the Surveys knowledge base series.

---

# 2. Key Concepts & Definitions

**Public Survey Link**

A single survey URL that can be filled out an unlimited number of times. Each new response creates a new record. The public survey link always points to the first instrument in a project (in the first event of each arm for longitudinal projects). It is the standard method for open-enrollment distribution — email campaigns, flyers, and similar scenarios.

**Individual Survey Link**

Any survey link tied to a specific record, instrument, (in longitudinal projects) event and (for repeating surveys) repeat instance. Individual survey links can typically be completed only once. Each "dot" on the Record Home Page corresponds to a unique individual survey link.

**Survey Options Menu**

A dropdown menu visible inside an open instrument in a record. It provides quick access to that instrument's survey link and related tools. Requires the instrument to be enabled as a survey and sufficient user rights.

**Smart Variable**

A placeholder token that REDCap replaces with dynamic content at runtime. The survey-related smart variables return the URL or clickable link for a specific survey. Full coverage of smart variables is in [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md).

**Instrument Unique Name**

The internal name REDCap assigns to each instrument. It may differ slightly from the user-defined display name (e.g., display name "Baseline Vital Signs" → unique name `baseline_vital_signs`). Smart variables require the unique name, not the display name. The Codebook ([RC-FD-05 — Codebook](RC-FD-05_Codebook.md)) lists both.

**Survey Access Code**

A short code that participants can enter on REDCap's general survey page to reach a specific survey. Useful when a long URL is impractical (e.g., phone-based distribution). See Section 4.4.

**QR Code**

An auto-generated image that encodes a survey URL. Participants scan it with a smartphone to open the survey directly. REDCap generates a QR code for every individual survey link and public survey link automatically.

---

# 3. Public vs. Individual Survey Links

## 3.1 Public Survey Links

REDCap generates a public survey link automatically the moment the first instrument in a project is enabled as a survey. No additional configuration is required.

Each time a participant starts a new response on the public survey link, REDCap creates a new record. The record is created as soon as the participant submits the first page (or clicks **Save & Return Later**), so partially completed responses become records too. From that point the participant continues on that record's individual survey link, not the public link. Because it can be used repeatedly, the same link can be shared with any number of participants. Common use cases include email campaigns, paper flyers, and embedded website forms.

Survey Distribution Tools also offers ways to share the public link: send the URL by email, get embed code for a website, create a short link, or create a custom `redcap.link` URL (the last two depend on settings your REDCap administrator controls). See [RC-SURV-01 — Surveys – Basics](RC-SURV-01_Surveys-Basics.md).

You can optionally add a Google reCAPTCHA check to the public survey link (your REDCap administrator must set up reCAPTCHA first). Once a respondent passes it, they are not asked again that day.

> **Version caveat (17.6):** In 17.6 a passed reCAPTCHA check applies per survey and lasts until midnight. When testing, expect to see the check again on each public survey you open.

The public survey link is found in the **Survey Distribution Tools** section of the project menu. See [RC-SURV-01 — Surveys – Basics](RC-SURV-01_Surveys-Basics.md) for the full Survey Distribution Tools walkthrough.

> **Note:** The public survey link is only available when the **first instrument** in the project is enabled as a survey. If the first instrument is not a survey, REDCap will not generate a public link.

**Why the public survey link always points to the first instrument**

REDCap stores all data in a record based on the Record ID, which lives on the first variable of the first instrument. REDCap enforces this rule to maintain database integrity — a new record cannot be created without a Record ID, and that ID must come from the first instrument.

## 3.2 Public Survey Links in Longitudinal Projects

In a standard longitudinal project, the public survey link works the same as in a classic project. The only additional requirement is that the first instrument must be assigned to the first event.

When a project has multiple arms, REDCap generates a separate public survey link for each arm where the first instrument is designated in that arm's first event and is enabled as a survey. Each arm's public link always opens the first instrument in that arm's first event. In the Survey Distribution Tools section, a dropdown appears prompting you to select an arm before the corresponding public link is displayed. This arm-specific routing ensures newly created records are placed in the correct arm.

## 3.3 Individual Survey Links

Every instrument enabled as a survey in a specific record gets its own individual survey link. In longitudinal projects, links are also specific to each event — the link for an instrument in Event 1 is different from the link for the same instrument in Event 2, even within the same record. For repeating surveys, each repeat instance has its own link. A response that starts on the public link becomes instance 1 of a new record.

Each survey link ends in `?s=` followed by a long random code (16 characters on current versions) that identifies the record, instrument, event and instance.

A practical shortcut: every "dot" on the Record Home Page represents one individual survey link.

Individual survey links can be completed only once by default. After submission, reloading the link shows a "survey already completed" message.

**Exception — Save and Return Later**

Participants can return to a completed survey and edit their responses only when the survey has **Save & Return Later** enabled together with its sub-option **Allow respondents to return and modify completed responses**. Both are off by default. Returning participants must enter their return code (8 characters) unless the survey also allows returning without a return code — and with that combination, anyone who has the link can view and change the response. The modify option cannot be used on a survey with e-Consent. Only enable it when the use case explicitly requires participant-editable responses. See [RC-SURV-03 — Survey Settings: Behavior, Access & Termination](RC-SURV-03_Survey-Settings-Behavior-Access-and-Termination.md).

---

# 4. Finding a Specific Survey Link

REDCap provides three methods for locating an individual survey link for a specific record. Section 4.4 covers access codes and QR codes.

## 4.1 Survey Options Menu (Inside the Instrument)

When you open an instrument for a specific record, a **Survey Options** dropdown is visible at the top of the data entry page (provided the instrument is enabled as a survey and you have the **Survey Distribution Tools** user right). Its main options are:

| Option | What It Does |
|---|---|
| Open Survey | Opens the survey in a new browser tab. Copy the URL from the address bar. |
| Log Out + Open Survey | Opens the survey in a new tab and logs you out of REDCap simultaneously. Use this when handing your device directly to a participant. |
| Compose Survey Invitation | Opens the invitation composer for that specific survey in that record. Useful for sending a one-off email invitation. |
| Survey Access Code + QR Code | Displays the access code and the QR code for that specific survey link. |

When the Survey Queue is enabled, the menu also offers the record's survey queue. The survey options are greyed out when the response is already completed or the survey is offline.

## 4.2 Survey Smart Variables

Smart variables can be used anywhere REDCap processes piped content — survey invitation emails, Alerts & Notifications, instrument fields (with some restrictions). There are two survey link smart variables: `[survey-url]` and `[survey-link]`. Full details are in [RC-PIPE-08 — Smart Variables: Survey](RC-PIPE-08_Smart-Variables-Survey.md).

### `[survey-url]` — Returns the full URL as plain text

| Syntax | When to Use |
|---|---|
| `[survey-url]` | Uses the current instrument: the form or survey page being viewed, the survey in a survey invitation, or the instrument that triggered an alert. Blank when there is no current instrument or the current instrument is not enabled as a survey. |
| `[survey-url:instrument]` | Works anywhere piping is supported and names the survey explicitly (best practice). Requires the instrument's unique name. Example: `[survey-url:baseline_vitals]` |
| `[event][survey-url:instrument]` | Use in longitudinal projects to point to a specific event. Without an event prefix, the current event is used. Example: `[event_1_arm_1][survey-url:baseline_vitals]` |

### `[survey-link]` — Returns a clickable hyperlink

| Syntax | When to Use |
|---|---|
| `[survey-link]` | Uses the current instrument, in the same way as `[survey-url]`; blank when there is no current instrument or it is not a survey. The link label is the survey title. |
| `[survey-link:instrument]` | Works anywhere piping is supported. The link label is the survey title. |
| `[survey-link:instrument:Custom Text]` | Same as above, but the link label is the text you define. Example: `[survey-link:baseline_vitals:Take Our Baseline Survey]` |

> **Tip — Finding the Instrument Unique Name:** Smart variables require the unique name of an instrument, not its display name. The easiest way to find it is in the Codebook (under Project Home and Design), where instruments are listed as: `Display Name (unique_name)`. See [RC-FD-05 — Codebook](RC-FD-05_Codebook.md).

> **Tip — Longitudinal projects:** Without an event prefix, REDCap uses the current event (the event of the form, survey, invitation or alert trigger). Include a unique event name, e.g. `[event_1_arm_1][survey-url:baseline_vitals]`, whenever you want a different event or the text is used where the event is not obvious. `[previous-event-name]` and `[next-event-name]` take the literally adjacent event, even if the survey is not designated there, so a specific unique event name is safer.

## 4.3 Participant List

The participant list in Survey Distribution Tools displays individual survey links for records that meet either of these conditions:

- At least one data point has been saved in the record.
- An email address has been added for that record via the **Add Participant** function.

To locate a specific link: navigate to the participant list, select the correct instrument (and event, in longitudinal projects), find the record or email in the list, and click the link icon in the **Link** column. The **Link** column shows "-" instead of an icon for responses that are already completed (unless the survey allows respondents to modify completed responses) and for links whose survey time limit has expired.

Full documentation of the participant list is in [RC-SURV-05 — Participant List & Manual Survey Invitations](RC-SURV-05_Participant-List-and-Manual-Survey-Invitations.md).

**Identified vs. anonymous mode in the participant list**

By default, the participant list runs in anonymous mode, which makes it difficult to associate a specific link with a specific person. To switch to identified mode (enabling a clickable Record ID column), either:

- Add a **participant identifier** (name) alongside the email when using **Add Participant**. Note: the Participant Identifier feature must first be activated by clicking the **Enable** button in the Participant Identifier column header of the participant list — see [RC-SURV-05 — Participant List and Manual Survey Invitations](RC-SURV-05_Participant-List-and-Manual-Survey-Invitations.md), Section 3.3 for details and an important warning about disabling the feature.
- Designate an email field for the project in Project Setup → Enable Optional Modules and Customizations, or an email or phone field in the survey's own settings.

## 4.4 Access Codes and QR Codes

Every individual survey link and the public survey link has an access code and a QR code (shown under **Survey Access Code + QR Code** in the Survey Options menu, and in Survey Distribution Tools for the public link). The participant goes to the base survey URL of your REDCap server and types the code instead of the full link.

| Code | Format | Notes |
|---|---|---|
| Survey access code | 9 characters, capital letters and digits (characters that are easy to confuse are left out) | Entered at the base survey URL. |
| Short code | 2 letters followed by 3 digits | Single use; expires after 60 minutes. Generate a new one if it lapses. |
| Numeral code | 10 digits | Only when Twilio telephony is enabled for the project. Entering it with a "V" in front requests a phone call for a voice survey instead. |

A QR code simply encodes the survey URL; scanning it opens the survey.

---

# 5. Common Questions

**Q: What is the difference between a public survey link and an individual survey link?**

**A:** A public survey link can be used any number of times; each new response creates a new record. An individual survey link is tied to one specific record, instrument, event and repeat instance, and can typically only be submitted once.

**Q: Can I use the public survey link for follow-up surveys?**

**A:** No. The public survey link always points to the first instrument in the project (in the first event for longitudinal projects) because that is where the Record ID lives. Follow-up surveys are reached via individual survey links, sent through the participant list, Automated Survey Invitations, or the Survey Queue.

**Q: A participant says they see "this survey has already been completed" when they click the link. What happened?**

**A:** They received an individual survey link that was already submitted. If you want participants to be able to return and edit their responses, enable **Save & Return Later** with the sub-option **Allow respondents to return and modify completed responses** in that survey's settings. If they should be starting a fresh response, use the public survey link or create a new record.

**Q: Where do I find the instrument's unique name for use in smart variables?**

**A:** In the Codebook (Project Home and Design → Codebook). Each instrument is listed with its display name followed by its unique name in parentheses. See [RC-FD-05 — Codebook](RC-FD-05_Codebook.md).

**Q: Can I use `[survey-url]` (without the instrument name) in an Alert & Notification?**

**A:** Yes, if the instrument that triggers the alert is enabled as a survey: the bare `[survey-url]` uses that instrument (and the current event). It is blank when the triggering instrument is not a survey or there is no instrument context. Best practice is to name the instrument explicitly, `[survey-url:instrument_name]`, so the link is unambiguous wherever the text is reused.

**Q: Does a QR code expire?**

**A:** A QR code is simply an encoded version of the underlying survey URL. It remains valid as long as the survey link itself is active. The link stops accepting responses when:

- the response is completed (individual links), unless the survey allows respondents to modify completed responses;
- the survey is taken offline or passes its expiration date;
- the survey's time limit for that link has expired;
- the project is taken offline or moved to Analysis/Cleanup or Completed status. For Completed projects, your REDCap administrator may redirect respondents to another page.

**Q: In a multi-arm longitudinal project, how many public survey links are there?**

**A:** One per arm, provided the first instrument is designated in the first event of each arm and is enabled as a survey. Each arm's link always opens the first instrument in that arm's first event. REDCap displays an arm selector in Survey Distribution Tools so you can retrieve the correct link for each arm.

---

# 6. Common Mistakes & Gotchas

**Distributing an individual survey link as if it were a public link.** An individual survey link can only be completed once. If the wrong link is shared broadly, participants will see the "already completed" error after the first submission. Always verify you are sharing the public link (found in Survey Distribution Tools) when open-enrollment behavior is intended.

**Using bare `[survey-url]` or `[survey-link]` where there is no survey context.** Without an instrument name, these use the current instrument (the form or survey page, the survey in an invitation, or the instrument that triggered an alert). They are blank when there is no current instrument or it is not enabled as a survey — for example, an alert triggered by a non-survey form. Include the instrument's unique name to be safe: `[survey-url:instrument_name]`.

**Using the display name instead of the unique name in smart variables.** `[survey-url:Baseline Vital Signs]` will not work. REDCap requires the unique name (e.g., `[survey-url:baseline_vital_signs]`). Spaces and capitalization differences are common sources of failure.

**Expecting a survey link to appear in the participant list for a brand-new record with no data.** REDCap only generates individual survey links once at least one data point is saved, or once a participant's email has been added via Add Participant. Empty records do not appear.

**Omitting the event prefix when you need a different event.** Without an event prefix, REDCap returns the link for the current event. If you need the survey in another event (for example, a follow-up link sent from a baseline alert), put that event's unique name in front: `[followup_arm_1][survey-url:instrument_name]`.

---

## API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) for authentication, token management, and setup.

- **[RC-API-40 — Export Survey Link API](RC-API-40_Export-Survey-Link.md)** — programmatically retrieve a unique survey link for a specific record and instrument

---


# 7. Related Articles

- [RC-SURV-01 — Surveys – Basics](RC-SURV-01_Surveys-Basics.md) (enabling surveys, Survey Distribution Tools, public link walkthrough)
- [RC-SURV-02 — Survey Settings: Basic Options & Design](RC-SURV-02_Survey-Settings-Basic-Options-and-Design.md)
- [RC-SURV-03 — Survey Settings: Behavior, Access & Termination](RC-SURV-03_Survey-Settings-Behavior-Access-and-Termination.md) (Save and Return Later setting)
- [RC-SURV-05 — Participant List & Manual Survey Invitations](RC-SURV-05_Participant-List-and-Manual-Survey-Invitations.md) (full participant list documentation)
- [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md) (full catalog of smart variables)
- [RC-FD-05 — Codebook](RC-FD-05_Codebook.md) (finding instrument unique names)
- [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md) (arms, events)
