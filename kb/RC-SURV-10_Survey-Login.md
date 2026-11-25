

**Survey Login**

| **Article ID** | [RC-SURV-10 — Survey Login](RC-SURV-10_Survey-Login.md) |
|---|---|
| **Domain** | Surveys |
| **Applies To** | All REDCap projects with surveys enabled; field-value Survey Login cannot be applied to a Public Survey |
| **Requires** | Any supported version (Enforce REDCap login protection, §5: REDCap v17.5.0+ and a REDCap+ subscription) |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — Survey Login behaviour checked against source code; pages not re-captured |
| **Prerequisite** | [RC-SURV-01 — Surveys – Basics](RC-SURV-01_Surveys-Basics.md); [RC-SURV-02 — Survey Settings: Basic Options & Design](RC-SURV-02_Survey-Settings-Basic-Options-and-Design.md) |
| **Version** | 1.3 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-SURV-01 — Surveys – Basics](RC-SURV-01_Surveys-Basics.md); [RC-SURV-03 — Survey Settings: Behavior, Access & Termination](RC-SURV-03_Survey-Settings-Behavior-Access-and-Termination.md); [RC-SURV-04 — Survey Link Types & Access Methods](RC-SURV-04_Survey-Link-Types-and-Access-Methods.md); [RC-SURV-05 — Participant List & Manual Survey Invitations](RC-SURV-05_Participant-List-and-Manual-Survey-Invitations.md); [RC-PLUS-01 — REDCap+: Overview and Subscription](RC-PLUS-01_REDCap-Plus-Overview-and-Subscription.md) |
| **Synonyms** | how do i make participants log in to a survey; require authentication before completing a survey; verify respondent identity with field values; add a security check to survey access; survey login setup; ask for date of birth before opening a survey; restrict survey access to the correct person; password-style verification for surveys; require redcap username and password to take a survey; enforce redcap login protection on a survey; prefill survey with the logged-in user's name and email |

---

## 1. Overview

### What is this?

Survey Login is a project-level security feature that forces respondents to authenticate before they can view or complete a survey. In its standard form, respondents do not use a username and password; they prove their identity by entering one or more field values already stored in their record — such as a last name, date of birth, or participant ID. REDCap checks those entered values against the record and only grants access if they match.

From 17.5.0, REDCap+ subscribers have a second mode, **Enforce REDCap login protection**, which replaces the field-value challenge with REDCap's normal login. It is covered in Section 5.

### Why does it matter?

By default, anyone who possesses a survey link can open and complete a survey. Survey Login adds a verification layer that ties survey access to data that only the legitimate respondent should know. This is useful in studies where surveys are distributed broadly (e.g., via bulk email) and the research team wants assurance that the correct person is completing each record's survey.

### Scope and Assumptions

This article covers Survey Login configuration, including REDCap login protection for surveys. Applying REDCap login protection to public reports and public dashboards is covered in [RC-EXPRT-06 — Custom Reports: Setup & Field Selection](RC-EXPRT-06_Custom-Reports-Setup-and-Field-Selection.md) and [RC-PROJ-03 — Project Dashboards](RC-PROJ-03_Project-Dashboards.md). It assumes:
- Surveys are already enabled for the project (see [RC-SURV-01 — Surveys – Basics](RC-SURV-01_Surveys-Basics.md)).
- At least one instrument is enabled as a survey.
- The relevant login fields already exist in the project's data dictionary and contain values for each record that will be prompted to log in.

---

## 2. Key Concepts & Definitions

### Survey Login

A project-level feature that displays an authentication prompt before a respondent can access a survey. The respondent must enter values matching field data already saved in their record.

### Login Fields

The project fields — up to three — that REDCap uses as the authentication challenge. REDCap compares what the respondent types against what is stored in the record. If the values match (subject to the minimum required fields setting), the respondent is granted access.

### Minimum Required Fields

When more than one login field is configured, this setting controls how many of those fields must be correctly entered before access is granted. For example, if three login fields are configured but the minimum is set to 2, the respondent only needs to match any two of the three fields.

### Authentication Window

Once a respondent has successfully logged in, REDCap does not ask them to log in again for other surveys of the same record within the instance's auto-logout period (30 minutes by default). This prevents repeated authentication challenges when a respondent is completing multiple surveys in sequence, such as when working through a Survey Queue. A survey link for a different record always prompts for login again.

> **Version caveat (17.6 Standard vs 17.3 and 16.0 LTS):** On 17.6, the login holds for the auto-logout period even if the browser is closed and reopened, and changing the Survey Login settings ends existing logins. On LTS 17.3 and 16.0, the login generally lasts until the browser is closed. On all versions, tell respondents who use a shared computer to close the browser when they are done.

### Lockout

An optional security measure, off by default, that temporarily blocks login attempts on a survey link after too many failed attempts within a set number of minutes. See Section 6.

### REDCap Login Protection *(REDCap+, 17.5.0+)*

A Survey Login option under which the respondent authenticates through the instance's standard REDCap login — SSO, LDAP, Table-based or whatever the instance uses — instead of entering stored field values. The respondent is identified as a REDCap user, so their user attributes (username, name, email) can be prefilled into the survey.

---

## 3. How Survey Login Works

### 3.1 When the Login Prompt Appears

Survey Login behavior depends on whether a record exists for the respondent at the time they access the survey.

- **No record exists yet (e.g., first visit via a Public Survey, or a Participant List invitation to the first survey before a record has been created):** The survey opens normally. The login prompt is not displayed because there is no record data to validate against.
- **A record already exists:** The respondent is prompted to log in before the survey loads.
- **The response is already completed and the survey does not allow changes:** No login prompt appears, because the respondent cannot reopen the response anyway; they see REDCap's usual message that the survey has already been completed. To let respondents log in and change a completed response, enable **Allow respondents to return and modify completed responses** (Section 3.4).

This means Survey Login has no effect on the very first interaction for a new respondent. It becomes active on all subsequent survey accesses once a record has been created — whether by the respondent completing a prior survey, by staff data entry, or by data import.

> **Important:** Field-value Survey Login is **never** applied to the public survey link (the first survey in a project accessible via the public survey link). A Public Survey by definition has no record to validate against when a new respondent arrives. Survey Login applies to all other survey access methods. REDCap login protection (Section 5) is different: it does cover the Public Survey link.

### 3.2 Where to Configure Survey Login

Survey Login is configured at the **project level**, not per survey. Access it from the **Online Designer** via the **Survey Login** button in the toolbar.

The settings defined here apply globally across the project's surveys, with one exception: which surveys the login is applied to can be restricted per survey (see Section 4.4).

### 3.3 The Login Form

The login form shows each login field's label and field note, so respondents can see what to enter and in what format. What the respondent types is masked, with a **show** option to reveal it.

Login fields that are empty for the record are left off the form. If fewer filled-in login fields remain than the minimum required (Section 4.3), the respondent cannot get in: they see an error together with your custom error message (Section 4.5). Choose login fields that are filled in for every record before the survey is sent — otherwise respondents can be locked out of the survey.

### 3.4 Save & Return Later and Completed Responses

When field-value Survey Login applies to a survey, the login replaces the Return Code: a respondent with **Save & Return Later** enabled resumes a partial response by logging in rather than entering a Return Code. Returning to a **completed** response still requires **Allow respondents to return and modify completed responses** to be enabled on that survey (see [RC-SURV-03 — Survey Settings: Behavior, Access & Termination](RC-SURV-03_Survey-Settings-Behavior-Access-and-Termination.md)).

---

## 4. Configuration Settings

### 4.1 Enable Survey Login

Toggle Survey Login on or off for the project. When disabled, all surveys open normally with no authentication prompt. When enabled, the remaining settings become active.

On REDCap+ instances at 17.5.0 or higher, the same dialog also offers **Enforce REDCap login protection** — see Section 5. Sections 4.2–4.5 describe the field-value mode.

### 4.2 Login Fields

Select the fields that respondents must enter to authenticate. Up to three fields can be configured.

**Which fields can be used:**

- Only **Text Box** fields can be chosen, with or without validation (e.g., a date- or number-validated text box).
- The record ID field cannot be chosen.
- Fields on repeating instruments or in repeating events do not work as login fields.
- In longitudinal projects, you also pick the **event** each login field is read from.

**Choosing effective login fields:**

- Use fields whose values are known to the respondent but not easily guessed by others.
- Date of birth and last name are common choices, particularly for studies where participants were pre-enrolled and their data was imported before surveys were distributed.
- Avoid fields with free-text values that have high variability in formatting (e.g., an open-text address field). Capitalization is ignored, but extra spaces before or after the value cause a mismatch, so small typing differences can make legitimate respondents fail authentication.
- The values must already be saved in every respondent's record before the survey is sent. Empty login fields are left off the login form, and if too few filled-in fields remain the respondent cannot get in (Section 3.3) — otherwise respondents can be locked out of the survey.

> **Note:** Survey Login matching ignores capitalization: a respondent entering "smith" matches a stored value of "Smith". Only plain letters are treated this way — accented letters in different case (for example "É" and "é") do not match. Extra spaces before or after the value are not ignored and cause a mismatch.

> **Note:** For dates in MDY or DMY format, the respondent enters the date in the field's own format (the field note shows it on the login form); REDCap converts it before comparing with the stored value.

### 4.3 Minimum Number of Fields Required for Login

When more than one login field is configured, this setting determines how many must be correctly entered to authenticate. Options are 1, 2, or 3 (the maximum equals the number of configured login fields). If the minimum is set higher than the number of login fields chosen, REDCap lowers it automatically to match.

Setting the minimum below the total number of configured fields provides a fallback: a respondent who cannot remember one value may still authenticate using the other fields. This can reduce support burden in studies with longer follow-up periods where participants may forget one of their registered values.

### 4.4 Apply Survey Login To

Controls which surveys in the project require login:

- **All surveys** — Survey Login is applied to every survey in the project.
- **Only selected surveys (set on Survey Settings page)** — Survey Login applies only to surveys that have been individually configured to use it. Per-survey login opt-in is managed on the **Survey Settings** page for each instrument.

Use the "only selected surveys" option when your project contains a mix of staff-distributed and publicly accessible surveys, or when Survey Login should only apply to sensitive instruments.

### 4.5 Custom Error Message

A message shown to respondents when login does not go through: after a failed login attempt, on the lockout page, and when the login form cannot be shown (for example, too few login fields are filled in for the record). It is **required** when using field-value Survey Login — the settings cannot be saved without it. HTML is allowed, including hyperlinks. In projects using Multi-Language Management, the custom message can be translated.

Make the message useful: tell respondents who to contact for login problems. Example:

```
If you have any trouble logging in to the survey, please contact
<a href="mailto:study-support@example.edu">study-support@example.edu</a> for help.
```

---

## 5. Enforce REDCap Login Protection *(REDCap+, 17.5.0+)*

> **⚠️ REDCap+ Feature Tag**
> Enforce REDCap login protection requires REDCap 17.5.0 (Standard) or higher and an active REDCap+ subscription on the installation. It is not in LTS 17.3 or 16.0. See [RC-PLUS-01 — REDCap+: Overview and Subscription](RC-PLUS-01_REDCap-Plus-Overview-and-Subscription.md).

> **Version caveat (LTS 17.3 and 16.0):** REDCap login protection is not available on the LTS 17.3 or 16.0 lines; the option does not exist there. On those servers, use field-value Survey Login (Section 4) to control who can open a survey.

> **Scope note:** This section's behaviour was checked against REDCap source code. It has not yet been checked on a live subscribed instance, so exact dialog layout may differ.

### 5.1 What It Does

When **Enforce REDCap login protection** is selected in the Survey Login settings, REDCap uses its standard login flow instead of asking the respondent for stored field values. A respondent who is already logged in to REDCap goes straight to the survey; anyone else is sent through the instance's normal authentication first.

**Which links are covered.** Protection applies to all surveys or to selected surveys, using the same **Apply survey login to** choice as Section 4.4. On a protected survey it covers both the **Public Survey link** and participant-list (private) links. The **Survey Queue** page itself is not protected, but each protected survey opened from the queue asks for login.

**How long the login lasts.** Access lasts for the instance's auto-logout timer (30 minutes if none is set), within the respondent's REDCap session. A logged-in respondent who moves on to another protected survey is not asked to log in again while their REDCap session is active.

**Gating is enforced on the server.** Without an active REDCap+ subscription the option cannot be saved.

> **Warning — subscription lapse:** If the installation's REDCap+ subscription lapses, REDCap login protection silently switches off. Protected surveys (and protected public reports and dashboards, Section 5.5) open to anyone with the link again, while the setting still shows as on. Before letting a subscription lapse, list the projects that rely on REDCap login protection and switch their surveys to field-value Survey Login (Section 4), or take the links out of circulation.

Use it when respondents are institutional users — staff surveys, internal evaluations, training sign-offs — where knowing *which user account* completed the survey matters more than matching record data.

| | Field-value Survey Login (Section 4) | REDCap login protection |
|---|---|---|
| Respondent proves identity with | 1–3 values stored in their record | Their REDCap / institutional credentials |
| Needs record data before login | Yes | No |
| Subscription | None | REDCap+ |
| Minimum version | Any supported | 17.5.0 (Standard); not on LTS 17.3 or 16.0 |
| Covers the Public Survey link | No | Yes |
| Can prefill user details | No | Yes (Section 5.2) |

### 5.2 Prefilling Fields from the Logged-in User

Optionally, project fields on **page 1** of the survey can be prefilled with attributes REDCap obtains at login: username, first name, last name, email, phone, employee ID, and alternative username, each where the instance has it.

An option lets you prefill **only empty fields**, so values already saved in the record are not overwritten.

Prefilled fields are ordinary fields and remain editable unless you prevent it. To lock them, add `@READONLY` (still visible) or `@HIDDEN-SURVEY` (not shown) — see [RC-AT-02 — @HIDDEN & @READONLY — Visibility Control](RC-AT-02_Action-Tags-Hidden-and-Readonly.md).

Prefill applies to page 1 only. Fields on later pages of a multi-page survey are not prefilled.

### 5.3 Allow Access for Internal Users Only

If the instance uses one of the **"X & Table-based"** authentication methods (for example LDAP & Table-based, or Entra ID & Table-based), an extra option appears: **Allow access for internal users only**. When it is selected, Table-based users — normally external collaborators with REDCap-managed accounts — are blocked from the survey while REDCap login protection is on.

This option does not appear on instances that use only one authentication method.

### 5.4 Who Can Get In

Under any authentication method **other than Table-based**, a person who has never used REDCap and has no REDCap account can still reach the survey, provided they pass the institution's authentication (for example, the institutional SSO). REDCap login protection therefore means "anyone who can authenticate to this REDCap instance", not "existing REDCap users" or "users of this project". The respondent does not need to be a user of the project, and project user rights are not checked. The REDCap account must be active, however: a suspended or expired account cannot get in.

> **Institution-specific:** Who can pass authentication depends on how the instance's SSO or LDAP is scoped — sometimes the whole institution, sometimes a subset, sometimes affiliates too. Ask your REDCap administrator before relying on REDCap login protection to restrict a survey to a particular group.

### 5.5 Public Reports and Public Dashboards

The same protection can be applied to any **public report** or **public project dashboard**. Once the report or dashboard is public, a button immediately beneath it, **Enable REDCap login protection**, turns it on. Viewers then have to log in to REDCap, if not already logged in, before the report or dashboard is displayed. See [RC-EXPRT-06 — Custom Reports: Setup & Field Selection](RC-EXPRT-06_Custom-Reports-Setup-and-Field-Selection.md) §4.2 and [RC-PROJ-03 — Project Dashboards](RC-PROJ-03_Project-Dashboards.md) §5.

### 5.6 Save & Return Later

A respondent who logs in does not need a Return Code to resume a survey with **Save & Return Later** enabled, **provided they use a participant-specific (private) link**. On the Public Survey link, a Return Code is still needed to resume. If respondents will need to come back to a partial response, send them participant-specific links.

> **Version caveat (17.5.0–17.5.3 Standard):** REDCap login protection could still ask the respondent for a **Return Code** on surveys with Save & Return Later enabled. Fixed in 17.5.4.

---

## 6. Security Settings (Optional)

### 6.1 Failed Login Attempt Limit

Sets how many failed login attempts are allowed (0–99) before the survey link is temporarily locked. Lockout is **off by default**.

Lockout works only when **both** this limit and the lockout minutes (Section 6.2) are above 0. Fill in both or neither — REDCap does not let you save only one of them.

How it counts and what it blocks:

- REDCap counts failed attempts within the last N minutes (N = the lockout minutes), separately for each record and each survey link.
- When the limit is reached, that survey link is blocked for **everyone** until the lockout period has passed — including the real respondent, not just the person who was guessing.

Enabling a lockout is recommended for studies where the login field values could be guessed systematically (e.g., when only a single date-of-birth field is required). Weigh this against the support cost: a respondent who mistypes repeatedly also locks themselves out.

### 6.2 Lockout Duration

The number of minutes (0–999) used both as the window in which failed attempts are counted and as the length of the lockout. It has no effect unless the failed attempt limit is also above 0.

---

## 7. Common Questions

**Q: A respondent says they cannot log in even though their information is correct. What should I check?**
Verify that the login field values stored in their record match what they are entering, including any extra spaces before or after the stored value. Pay attention to field validation — for example, if the date field uses a specific date format, the respondent must enter the date in that format. Check that enough login fields are filled in for the record (Section 3.3). Also check whether the survey link has been locked out after too many failed attempts. There is no screen to view or clear a lockout; the respondent has to wait until the lockout period has passed. **Survey Login Success** and **Survey Login Failure** entries in **Logging** show the attempts for the record — use them for troubleshooting.

**Q: Will Survey Login interrupt a Survey Queue flow?**
No. Once a respondent has logged in, REDCap does not prompt them again for other surveys of the same record within the instance's auto-logout period (30 minutes by default; see the version caveat under **Authentication Window** in Section 2). A respondent moving through a Survey Queue logs in once at the start and then proceeds through the queue without interruption. Under REDCap login protection, the queue page itself opens without login; the first protected survey asks for it, and later protected surveys do not ask again while the respondent's REDCap session is active.

**Q: Can I use Survey Login on a Public Survey?**
No, not in field-value mode. Survey Login is never applied to the Public Survey (the survey accessible via the public survey link). Because public surveys are designed for first-time respondents who do not yet have a record, there is no data to validate against. Survey Login applies once a record exists. REDCap login protection (Section 5) does not need record data and does cover the Public Survey link, on REDCap+ instances at 17.5.0 or higher (not LTS 17.3 or 16.0).

**Q: Can I make people log in with their REDCap account to take a survey?**
Yes, on REDCap+ instances at 17.5.0 or higher — select **Enforce REDCap login protection** in the Survey Login settings (Section 5). Without REDCap+, or on LTS 17.3 and 16.0, the only built-in option is field-value Survey Login.

**Q: Can I capture who completed a survey without asking them to type their name and email?**
With REDCap login protection, yes: prefill page-1 fields with the logged-in user's username, name and email, and lock them with `@READONLY` or `@HIDDEN-SURVEY` (Section 5.2).

**Q: Can I pre-fill survey questions from URL parameters when Survey Login is on?**
Yes, on current versions.

> **Version caveat (below 17.5.1 Standard / 17.3.14 LTS):** URL-parameter prefill silently failed on surveys with Survey Login enabled — the values were dropped and the fields loaded blank. Fixed in 17.5.1 Standard and 17.3.14 LTS.

> **Version caveat (LTS 16.0):** The fix is not in the LTS 16.0 line; URL-parameter prefill still fails with Survey Login on 16.0.61. On LTS 16.0, do not rely on URL prefill for surveys that use Survey Login — load the values into the record by data entry or import instead.

**Q: Does Survey Login apply to survey invitations sent through the Participant List?**
Yes, if Survey Login is enabled for that survey and a record already exists. For an invitation to the first survey sent before any record exists, no login prompt appears (Section 3.1). Respondents whose record exists and who click their individualized invitation link will be prompted to enter their login field values before the survey loads.

**Q: What happens if a login field is empty for a record?**
Empty login fields are left off the login form. If the remaining filled-in fields still meet the minimum (e.g., minimum is 2 out of 3 configured fields and the other two have values), the respondent can authenticate using those. If fewer filled-in fields remain than the minimum, the respondent cannot get in and sees an error with your custom error message. Choose login fields that are filled in for every record before the survey is sent — otherwise respondents can be locked out of the survey.

**Q: Can I configure different login fields for different surveys?**
No. Login fields are project-wide. All surveys that use Survey Login in the project use the same login fields.

**Q: What if I want to restrict which surveys require login?**
Set **Apply survey login to** to *Only selected surveys*, then enable Survey Login per instrument on each survey's Survey Settings page.

---

## 8. Common Mistakes & Gotchas

**Enabling Survey Login before login field values are populated.** Survey Login is only effective if the respondent's record already contains values for the login fields. If you distribute surveys before populating those fields (e.g., before importing participant data), respondents may fail authentication even though they are legitimate participants. Always confirm data is loaded before enabling Survey Login.

**Choosing login fields with inconsistent formatting.** Fields like phone numbers or addresses can be stored in many formats. If your project was populated from an external source, values may have inconsistent formatting (e.g., "01-01-1980" vs "1980-01-01"). This causes legitimate respondents to fail authentication. Use fields with controlled, predictable values — especially validated date or number fields.

**Expecting Survey Login to work on a Public Survey.** A common misconception is that Survey Login can be used to gate who can fill out the first survey. It cannot — Survey Login only activates once a record exists. For access control on initial enrollment, consider REDCap login protection (Section 5), which does cover the Public Survey link on REDCap+ instances, or a different approach such as a unique access code managed outside of REDCap.

**Letting the REDCap+ subscription lapse without checking protected surveys.** REDCap login protection switches off silently when the subscription ends, while the setting still shows as on (Section 5.1). Move those surveys to field-value Survey Login before the subscription lapses.

**Setting the minimum required fields too low for sensitive data.** A minimum of 1 out of 3 configured fields means a respondent only needs to get one field right to gain access. For studies with sensitive data, set the minimum to 2 or 3 to require more than a single correct value.

**Treating REDCap login protection as a project user list.** Under SSO or LDAP, anyone who can authenticate to the instance can open the survey, including people who have never used REDCap (Section 5.4). Project user rights are not checked. If only specific people should respond, check the prefilled username against an expected list — for example with branching logic or a Data Quality rule — or use field-value Survey Login against pre-loaded records.

**Leaving prefilled user fields editable.** Prefilled username, name and email fields can be overwritten by the respondent unless they carry `@READONLY` or `@HIDDEN-SURVEY`. If the values are your record of who responded, lock them.

**Writing a custom error message that doesn't help.** The custom error message is required, and it is what respondents see after a failed login, on the lockout page and when the login form cannot be shown. Make it useful — say who to contact and how — so respondents know who to reach when they cannot log in.

**Turning on lockout without planning for it.** A lockout blocks the survey link for everyone, including the real respondent, and there is no screen to clear it — the respondent has to wait out the lockout period (Section 6). Keep the lockout minutes short enough that a locked-out participant can try again the same day, and mention the wait in the custom error message.

---

## 9. Related Articles

- [RC-SURV-01 — Surveys – Basics](RC-SURV-01_Surveys-Basics.md)
- [RC-SURV-02 — Survey Settings: Basic Options & Design](RC-SURV-02_Survey-Settings-Basic-Options-and-Design.md)
- [RC-SURV-03 — Survey Settings: Behavior, Access & Termination](RC-SURV-03_Survey-Settings-Behavior-Access-and-Termination.md)
- [RC-SURV-04 — Survey Link Types & Access Methods](RC-SURV-04_Survey-Link-Types-and-Access-Methods.md)
- [RC-SURV-05 — Participant List & Manual Survey Invitations](RC-SURV-05_Participant-List-and-Manual-Survey-Invitations.md)
- [RC-SURV-07 — Survey Queue](RC-SURV-07_Survey-Queue.md)
- [RC-AT-02 — @HIDDEN & @READONLY — Visibility Control](RC-AT-02_Action-Tags-Hidden-and-Readonly.md)
- [RC-PLUS-01 — REDCap+: Overview and Subscription](RC-PLUS-01_REDCap-Plus-Overview-and-Subscription.md)
