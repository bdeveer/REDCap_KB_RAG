RC-SURV-01

**Surveys – Basics**

| **Article ID** | RC-SURV-01 |
| --- | --- |
| **Domain** | Surveys |
| **Applies To** | All REDCap projects with surveys enabled; single-instrument projects assumed for this guide |
| **Prerequisite** | RC-NAV-UI-01 — Project Navigation UI; RC-FD-02 — Online Designer |
| **Version** | 1.0 |
| **Last Updated** | 2026-04-02 |
| **Author** | REDCap Support |
| **Related Topics** | RC-FD-02 — Online Designer; RC-RIGHTS-01 — User Rights; RC-ALERT-01 — Automated Survey Invitations |

---

# 1. Overview

## What is this?

This article introduces REDCap surveys at a basic level. It covers the end-to-end workflow for enabling and configuring a survey, distributing it to participants, and reviewing the responses. It also describes the survey-related user rights and the key survey settings available in the Survey Settings page.

## Why does it matter?

By default, REDCap instruments can only be filled out by users who are logged in. Surveys extend this by allowing non-users — such as study participants — to enter data directly, without needing a REDCap account. Understanding how to set up, distribute, and manage surveys is fundamental to running participant-facing studies in REDCap.

## Scope and Assumptions

This article assumes:
- The user is logged into a REDCap instance and has navigated to an existing project.
- The project has a single instrument and has longitudinal mode and Data Access Groups (DAGs) disabled. Some interface elements may look different or offer additional options when those features are enabled.
- The user has the **Project Design and Setup** right assigned in their user profile.

---

# 2. Key Terminology

- **Survey**: A version of a REDCap instrument that can be filled out by a participant who is not logged into REDCap. Any instrument can be enabled as a survey.
- **Participant**: The person filling out a survey in REDCap. Participants are not REDCap users — they access the survey through a link, QR code, or email invitation.
- **Public Survey Link**: A URL that opens the first instrument's survey. Anyone with the link can fill it out an unlimited number of times.
- **Participant List**: A feature that lets you send individualized survey links to specific email addresses, enabling tracking and automated reminders.
- **Survey Invitation**: An email sent to a participant containing their unique survey link.
- **Survey Distribution Tools**: A page in the left-hand menu under "Data Collection" that consolidates all methods for distributing surveys in a project.
- **Survey Status**: A per-survey on/off toggle that enables or disables the survey without removing its settings.
- **Partial Completion**: A survey that a participant started but did not finish. Typically occurs when a participant closes the browser mid-way through a multi-page survey.

---

# 3. Learning Objectives

After completing this module, the user will be able to:

- Enable surveys for a project and enable individual instruments as surveys.
- Navigate to and configure survey settings.
- Distribute a survey using the Public Survey Link and the Participant List.
- Identify the correct user rights required for survey-related tasks.
- Review submitted survey responses and enter edit mode to modify a response.
- Identify the survey status icons (grey dot, orange dot with white checkmark, green dot with white checkmark) and what each means.

---

# 4. Survey Setup Workflow

Enabling a survey for the first time requires three steps in order: enable surveys at the project level, enable the specific instrument as a survey, then save the survey settings.

## 4.1 Enabling Survey Functionality in the Project

Before any instrument can be used as a survey, surveys must be turned on for the project as a whole.

| 1 | Navigate to the **Project Setup** page from the left-hand menu. |
| --- | --- |
| 2 | Under **Main Project Settings**, locate the **Use Surveys in this project** option. |
| 3 | If the button is red, surveys are disabled. Click **Enable** to turn surveys on. If the button is green, surveys are already enabled. |

The **Enable/Disable** button toggles between the enabled (green) and disabled (red) state. When surveys are disabled, all survey-related functionality — including survey settings, distribution tools, and survey status icons — is hidden throughout the project.

## 4.2 Enabling an Instrument as a Survey

With surveys enabled at the project level, navigate to the **Online Designer** to enable individual instruments.

The Online Designer now shows additional survey-related columns and buttons:

| Element | Description |
| --- | --- |
| **Survey Options** header | Contains advanced survey features. Out of scope for this training — covered in separate courses. |
| **Enabled as Survey** column | The primary column for enabling instruments as surveys. |
| **Enable** button | Appears behind each instrument that is not yet a survey. Clicking it takes you directly to that instrument's Survey Settings. |
| **Green checkmark shield** | Replaces the Enable button once an instrument has been enabled as a survey. Clicking it has no action — it is informational only. |
| **Survey Related Options** column | Appears for instruments that are already enabled as surveys and contains additional controls. |
| **Survey Settings** button | Returns you to the Survey Settings page for that instrument to adjust settings after initial setup. |
| **Automated Invitations** button | An advanced feature for scheduling email invitations. Covered in a separate course. |

| 1 | In the **Enabled as Survey** column, click the **Enable** button behind the instrument you want to enable as a survey. |
| --- | --- |
| 2 | You are taken directly to the Survey Settings page for that instrument. |

## 4.3 Choosing and Saving Survey Settings

The Survey Settings page contains a long list of options that control the appearance and behavior of your survey. For a first-time setup, you do not need to change any settings — the defaults are appropriate for most surveys.

> **Critical:** Your instrument is not enabled as a survey until you scroll to the bottom of the Survey Settings page and click **Save Changes**. Do not navigate away without saving.

See Section 5 for a reference guide to all available settings.

## 4.4 Distributing the Survey

Once your instrument is saved as a survey, you need to get the survey link to participants. REDCap provides multiple distribution methods, all accessible from the **Survey Distribution Tools** page in the left-hand menu under **Data Collection**.

See Section 6 for a detailed walkthrough of each distribution method.

---

# 5. Survey Settings Reference

The Survey Settings page contains the following sections. All options are described at a high level here. Advanced options are covered in separate training courses.

## 5.1 Survey Status

Allows you to turn the survey on or off without removing any of the configured settings. This is useful when you need to temporarily pause a survey — for example, if registration is full or you are making updates to the instrument.

| Status | Effect |
| --- | --- |
| **Online and active** | Participants can access and fill out the survey. |
| **Offline** | The survey link returns an "offline" message to participants. Survey settings and collected data are preserved. |

## 5.2 Basic Survey Options

Allows you to customize the **survey title** and **introductory text** displayed to participants at the top of the survey. By default, the title matches the instrument name. Change it here if you want the participant-facing title to differ from the instrument name.

## 5.3 Survey Design Options

Controls the visual appearance of the survey — including the color scheme, font, and text size. These are purely cosmetic options with no effect on data collection.

## 5.4 Survey Customizations

A collection of behavioral settings that modify how your survey works — for example, whether participants can save and return later, whether response limits are enforced, or how fields are presented. The standard settings are appropriate for most basic surveys. All options in this section are covered in more advanced training.

## 5.5 Survey Access

Allows you to automatically close the survey based on:
- A specific **date and time**
- A maximum **number of responses**
- A maximum **duration** the survey has been open

The default settings leave the survey open indefinitely. These options are appropriate for most basic surveys.

## 5.6 Survey Termination Options

Governs what participants see and what happens after they submit a completed survey — for example, whether they are shown a confirmation message, redirected to a URL, or allowed to print a copy of their responses. All options in this section are covered in more advanced training.

## 5.7 Deleting Survey Settings

This button appears at the very bottom of the Survey Settings page, but **only** when you return to the page after a survey has already been enabled (it is not visible during initial setup). Clicking it removes all survey configuration and reverts the instrument back to a standard instrument.

> **Important:** Deleting survey settings does **not** delete the instrument or any data collected through the survey. Only the survey-specific configuration is removed.

## 5.8 Save Changes / Cancel

| Button | Action |
| --- | --- |
| **Save Changes** | Saves all settings and returns you to the Online Designer. |
| **Cancel** | Discards any changes made since the page loaded and returns you to the Online Designer. |

---

# 6. Survey Distribution Tools

The **Survey Distribution Tools** page is the central hub for distributing surveys to participants. Access it from the left-hand menu under **Data Collection**. The page has three tabs.

## 6.1 Public Survey Link

The Public Survey Link is a single URL that anyone can use to fill out the survey. It always refers to the **first instrument** in the project. There is no limit on the number of times it can be filled out, and no login is required — if you have the link, you can complete the survey.

**Distribution options available on this tab:**

| Option | Description |
| --- | --- |
| **Public Survey URL** | The direct, unique URL for your survey. Copy and share this link directly. |
| **Open Public Survey** | Opens the survey in a new browser tab so you can preview it. |
| **Open Public Survey + Log Out** | Opens the survey and simultaneously logs you out of REDCap. Use this when you need to hand your device to a participant without giving them access to your REDCap session. |
| **Send me URL via email** | Sends the survey link to the primary email address associated with your REDCap account. |
| **Survey Access Code** | A short alphanumeric code participants can enter in the REDCap general survey portal to reach your survey, as an alternative to the full URL. |
| **QR Code** | A scannable QR code automatically generated for every survey. Most smartphones can scan it directly, opening the survey in the participant's browser. Saving the QR code and placing it on a flyer or poster is an effective way to recruit participants in person. |

**Link customization options:**

| Option | Description |
| --- | --- |
| **Get Short Survey Link** | Generates a shortened URL suitable for sharing in text messages or platforms with character limits. |
| **Create Custom Survey Link** | Lets you create a memorable, human-readable URL (e.g., `redcap.link/mystudy24`). The custom path must not already be in use by another REDCap survey. |
| **Get Embed Code** | Generates HTML code you can paste into a website to embed the survey directly on that page. |

**Captcha:**

A checkbox option that adds a Google reCAPTCHA (v2) screen before the survey loads. This verifies that a person — not an automated bot — is accessing the survey. Enabling this is strongly recommended if you offer any form of monetary incentive for participation.

## 6.2 Participant List

The Participant List allows you to send each participant an individualized survey link via email. Unlike the Public Survey Link, individualized links enable REDCap to track which specific participant has (or has not) completed the survey, and to send targeted follow-up reminders.

Using the Participant List is a two-step process:

**Step 1 — Add Participants:**

| 1 | Click the **Add Participants** button. |
| --- | --- |
| 2 | Paste participant email addresses into the input box, one email address per line. |
| 3 | Optionally add an identifier alongside each email (useful for matching responses to your own records). |
| 4 | Save the participant list. |

**Step 2 — Compose and Send Survey Invitations:**

| 1 | Click the **Compose Survey Invitations** button. A popup window opens. |
| --- | --- |
| 2 | Fill in the **From Address**, **Subject**, and **Body** of the invitation email. |
| 3 | Select which participants from the list should receive this invitation. |
| 4 | Optionally set a **send delay** to schedule the invitation for a future time. |
| 5 | Optionally configure up to **5 reminder emails** to be sent automatically to participants who have not yet completed the survey. |
| 6 | Click **Send Invitations**. |

> **Note:** REDCap automatically cancels any pending reminders for a participant as soon as they complete the survey. For example, if a participant completes the survey after the second reminder, reminders three through five are automatically deleted.

## 6.3 Survey Invitation Log

The Survey Invitation Log provides a complete record of all invitations and reminders associated with the project. On this page you can:

- View all invitations and reminders that have already been sent.
- View all scheduled future invitations and reminders.
- Edit the content or timing of scheduled (not yet sent) invitations.
- Cancel scheduled invitations or reminders before they are sent.

---

# 7. Survey User Rights

Only a few user rights in REDCap affect survey functionality.

| Right | Effect |
| --- | --- |
| **Project Design and Setup** | Required to enable surveys for the project, enable individual instruments as surveys, and modify survey settings. Without this right, a user cannot access the Survey Settings page or the survey-related columns in the Online Designer. |
| **Survey Distribution Tools** | Required to access the Survey Distribution Tools page (Public Survey Link, Participant List, Survey Invitation Log). Without this right, the page does not appear in the left-hand menu. |
| **Edit Survey Responses** | Controls whether a user can modify survey responses after they have been submitted. By default, submitted survey responses are locked — users can view them but not edit them. Granting this right unlocks the Edit Response button for that user. This right must be granted **per instrument** (not project-wide) and only appears for instruments that are enabled as surveys. It is turned off by default. |

---

# 8. Reviewing and Editing Survey Results

Once participants begin submitting responses, you can navigate to any survey response the same way you access any instrument record. (See the Data Entry Basics course for a refresher on record navigation.)

## 8.1 Survey Status Icons

Surveys use dedicated status icons that differ from those used for standard instruments.

| Icon | Meaning |
| --- | --- |
| **Grey dot** | The survey has not been opened or touched by any participant. Shared with regular (non-survey) instruments. |
| **Orange dot with white checkmark** | The survey was partially completed. This typically occurs in multi-page surveys where the participant closed the browser or navigated away before reaching the last page. |
| **Green dot with white checkmark** | The survey was fully completed by a participant. |

> **Note on partial completions:** Partial completions most commonly occur in surveys that use the "one section per page" setting. If a participant closes the browser after filling out page one but before reaching page two, an orange checkmark is recorded.

## 8.2 Viewing and Modifying Survey Responses

Submitted survey responses open in **view-only mode** by default. To modify a response (for example, to correct contact information a participant submitted):

| 1 | Navigate to the survey response in question using the Record Home Page or the record navigation tools. |
| --- | --- |
| 2 | Click the **Edit Response** button, found in the highlighted green information box at the top of the survey view. |
| 3 | Modify the data as needed. |
| 4 | Save your changes. |

> **Note:** You must click **Edit Response** each time you want to modify a given survey response. The form does not remain in edit mode between sessions.

> **Permission required:** The user must have the **Edit Survey Responses** right for the specific instrument in order for the Edit Response button to appear. See Section 7.

---

# 9. Questions & Answers

| Does enabling surveys prevent users from entering data directly into the instrument? | No. Enabling an instrument as a survey does not remove the ability to enter data as a logged-in user. Both data entry modes (user-entered and survey participant) remain available simultaneously. |
| --- | --- |
| What is the difference between the Public Survey Link and the Participant List? | The Public Survey Link is a single URL anyone can use — no tracking of individual participants. The Participant List sends each participant a unique link, enabling response tracking and automated reminders. |
| What happens to survey settings and data if I click "Delete Survey Settings"? | Only the survey configuration is deleted. The instrument definition and all collected data are preserved. The instrument reverts to a standard, non-survey instrument. |
| Why does the "Edit Survey Responses" checkbox not appear in the user rights page? | The checkbox only appears after an instrument has been enabled as a survey. If you don't see it, verify that the instrument is enabled as a survey first. |
| Can I temporarily disable a survey without losing its settings? | Yes. Use the **Survey Status** toggle in the Survey Settings page to switch the survey to Offline. The settings and data are preserved; participants who visit the link will see an offline message. |
| What is the Survey Access Code used for? | It is a shorter alternative to the full Public Survey URL. Participants can enter this code in the REDCap general survey portal (if your institution has one configured) instead of using the full URL. |
| How many reminders can I set up in the Participant List? | Up to 5 reminder emails per invitation. REDCap automatically cancels pending reminders for any participant who completes the survey. |
| Can I use both the Public Survey Link and the Participant List at the same time? | Yes. They are independent distribution methods and can be used concurrently. |

---

# 10. Common Mistakes & Gotchas

## Forgetting to click Save Changes after enabling a survey

- The user clicks Enable behind an instrument, reviews the Survey Settings, but navigates away without scrolling to the bottom and clicking Save Changes.
- The instrument is not enabled as a survey. The green checkmark shield does not appear.
- **Prevention:** Always scroll to the bottom of the Survey Settings page and confirm the Save Changes click before navigating away.
- **Recovery:** Return to the Online Designer, click Enable behind the instrument again, and save.

## Distributing the survey before saving settings

- The user shares the Public Survey Link before completing the Survey Settings save step.
- The instrument is not yet enabled as a survey, so the link either returns an error or does not display as expected.
- **Prevention:** Complete and save survey settings before distributing any links.

## Confusing the orange and green checkmarks

- Users interpret the orange checkmark as a completed response.
- Partial completions mean the participant did not finish the survey — some fields may be empty.
- **Prevention:** Understand the distinction between orange (partial) and green (complete) before analyzing or acting on survey data.

## Expecting to edit a survey response without the correct user right

- The user navigates to a completed survey response but does not see the Edit Response button.
- The user does not have the **Edit Survey Responses** right granted for that specific instrument.
- **Prevention:** Verify user rights for each instrument that needs to be editable. Remember this right is per-instrument, not project-wide, and only appears after the instrument is enabled as a survey.

## Using the Public Survey Link when individual tracking is needed

- The user distributes the Public Survey Link but later wants to know which participants have completed the survey.
- The Public Survey Link does not track individual respondents — all submissions appear as anonymous.
- **Prevention:** If tracking completion by individual participant is a requirement, use the Participant List instead of (or in addition to) the Public Survey Link.

## Missing scheduled reminders because the survey was re-enabled

- The user disables and re-enables the survey during the data collection period, which can affect scheduled reminders.
- **Prevention:** Avoid toggling the Survey Status on and off during active data collection. If you must take the survey offline briefly, verify the Invitation Log afterward to confirm scheduled reminders are still intact.

---

# 11. Related Articles

- RC-FD-02 — Online Designer (navigating to the Online Designer, the instrument list, and the instrument editor — required context for Section 4.2)
- RC-FD-01 — Form Design Overview (understanding instruments and fields before adding survey functionality)
- RC-RIGHTS-01 — User Rights (full reference for all REDCap user rights, including the three survey-related rights described in Section 7)
- RC-ALERT-01 — Automated Survey Invitations (advanced feature for triggering survey invitations based on data conditions — referenced in Section 4.2 as out of scope)
- RC-SURV-02 — Survey Customizations (covers the advanced settings in Survey Customizations, Survey Access, and Survey Termination Options left out of scope in this article)
- RC-SURV-03 — Survey Queue (managing sequential multi-survey workflows)

---

# 12. Version & Change Notes

| REDCap Version | Note |
| --- | --- |
| General | This article covers the baseline survey setup with longitudinal mode and DAGs disabled. Projects with those features enabled will see additional options in the Online Designer and Survey Distribution Tools. |
| General | The "Automated Invitations" button visible in the Online Designer's Survey Related Options column is covered separately in RC-ALERT-01 and is intentionally out of scope here. |
