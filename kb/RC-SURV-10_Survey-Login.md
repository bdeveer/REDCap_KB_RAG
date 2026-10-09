

**Survey Login**

| **Article ID** | [RC-SURV-10 — Survey Login](RC-SURV-10_Survey-Login.md) |
|---|---|
| **Domain** | Surveys |
| **Applies To** | All REDCap projects with surveys enabled; field-value Survey Login cannot be applied to a Public Survey |
| **Requires** | Any supported version (Enforce REDCap login protection, §5: REDCap v17.5.0+ and a REDCap+ subscription) |
| **Verified Against** | REDCap v17.5.4 (Standard) / v17.3.18 (LTS) — changelog review; page not re-captured. §5 is from the 17.5.0 release notes only |
| **Prerequisite** | [RC-SURV-01 — Surveys – Basics](RC-SURV-01_Surveys-Basics.md); [RC-SURV-02 — Survey Settings: Basic Options & Design](RC-SURV-02_Survey-Settings-Basic-Options-and-Design.md) |
| **Version** | 1.1 |
| **Last Updated** | 2026-10 |
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

### 30-Minute Authentication Window

Once a respondent has successfully logged in, REDCap does not prompt them again for any survey in the same project for the next 30 minutes. This prevents repeated authentication challenges when a respondent is completing multiple surveys in sequence, such as when working through a Survey Queue.

### Lockout

An optional security measure that temporarily blocks a respondent's ability to attempt login after a defined number of consecutive failed attempts. The lockout duration is configurable in minutes.

### REDCap Login Protection *(REDCap+, 17.5.0+)*

A Survey Login option under which the respondent authenticates through the instance's standard REDCap login — SSO, LDAP, Table-based or whatever the instance uses — instead of entering stored field values. The respondent is identified as a REDCap user, so their user attributes (username, name, email) can be prefilled into the survey.

---

## 3. How Survey Login Works

### 3.1 When the Login Prompt Appears

Survey Login behavior depends on whether a record exists for the respondent at the time they access the survey.

- **No record exists yet (e.g., first visit via a Public Survey):** The survey opens normally. The login prompt is not displayed because there is no record data to validate against.
- **A record already exists:** The respondent is always prompted to log in before the survey loads.

This means Survey Login has no effect on the very first interaction for a new respondent. It becomes active on all subsequent survey accesses once a record has been created — whether by the respondent completing a prior survey, by staff data entry, or by data import.

> **Important:** Survey Login **cannot** be applied to a Public Survey (the first survey in a project accessible via the public survey link). A Public Survey by definition has no record to validate against when a new respondent arrives. Survey Login applies to all other survey access methods.

### 3.2 Where to Configure Survey Login

Survey Login is configured at the **project level**, not per survey. Access it from the **Online Designer** via the **Survey Login** button in the toolbar.

The settings defined here apply globally across the project's surveys, with one exception: which surveys the login is applied to can be restricted per survey (see Section 4.4).

---

## 4. Configuration Settings

### 4.1 Enable Survey Login

Toggle Survey Login on or off for the project. When disabled, all surveys open normally with no authentication prompt. When enabled, the remaining settings become active.

On REDCap+ instances at 17.5.0 or higher, the same dialog also offers **Enforce REDCap login protection** — see Section 5. Sections 4.2–4.5 describe the field-value mode.

### 4.2 Login Fields

Select the fields that respondents must enter to authenticate. Up to three fields can be configured. Fields are selected from a dropdown of all project variables.

**Choosing effective login fields:**

- Use fields whose values are known to the respondent but not easily guessed by others.
- Date of birth and last name are common choices, particularly for studies where participants were pre-enrolled and their data was imported before surveys were distributed.
- Avoid fields with free-text values that have high variability in formatting (e.g., an open-text address field), as minor differences in spacing or capitalization can cause legitimate respondents to fail authentication.
- The values must already be saved in the respondent's record before they attempt to log in. If a field is empty for a record, the respondent cannot match it.

> **Note:** Field values in REDCap are case-insensitive for Survey Login matching purposes. A respondent entering "smith" will match a stored value of "Smith".

### 4.3 Minimum Number of Fields Required for Login

When more than one login field is configured, this setting determines how many must be correctly entered to authenticate. Options are 1, 2, or 3 (the maximum equals the number of configured login fields).

Setting the minimum below the total number of configured fields provides a fallback: a respondent who cannot remember one value may still authenticate using the other fields. This can reduce support burden in studies with longer follow-up periods where participants may forget one of their registered values.

### 4.4 Apply Survey Login To

Controls which surveys in the project require login:

- **All surveys** — Survey Login is applied to every survey in the project.
- **Only selected surveys** — Survey Login applies only to surveys that have been individually configured to use it. Per-survey login opt-in is managed on the **Survey Settings** page for each instrument.

Use the "only selected surveys" option when your project contains a mix of staff-distributed and publicly accessible surveys, or when Survey Login should only apply to sensitive instruments.

### 4.5 Custom Error Message

An optional message displayed on the login form when a respondent fails authentication. Supports HTML, including hyperlinks.

Use this to provide respondents with a contact point for login problems. Example:

```
If you have any trouble logging in to the survey, please contact
<a href="mailto:study-support@example.edu">study-support@example.edu</a> for help.
```

If no custom message is provided, REDCap displays a generic error.

---

## 5. Enforce REDCap Login Protection *(REDCap+, 17.5.0+)*

> **⚠️ REDCap+ Feature Tag**
> Enforce REDCap login protection requires REDCap 17.5.0 (Standard) or higher and an active REDCap+ subscription on the installation. See [RC-PLUS-01 — REDCap+: Overview and Subscription](RC-PLUS-01_REDCap-Plus-Overview-and-Subscription.md).

> **Scope note:** This section is written from the REDCap 17.5.0 release notes. It has not been checked against a live subscribed instance, so exact labels and dialog layout may differ.

### 5.1 What It Does

When **Enforce REDCap login protection** is selected in the Survey Login settings, REDCap uses its standard login flow instead of asking the respondent for stored field values. A respondent who is already logged in to REDCap goes straight to the survey; anyone else is sent through the instance's normal authentication first.

Use it when respondents are institutional users — staff surveys, internal evaluations, training sign-offs — where knowing *which user account* completed the survey matters more than matching record data.

| | Field-value Survey Login (Section 4) | REDCap login protection |
|---|---|---|
| Respondent proves identity with | 1–3 values stored in their record | Their REDCap / institutional credentials |
| Needs record data before login | Yes | No |
| Subscription | None | REDCap+ |
| Minimum version | Any supported | 17.5.0 (Standard) |
| Can prefill user details | No | Yes (Section 5.2) |

### 5.2 Prefilling Fields from the Logged-in User

Optionally, project fields on **page 1** of the survey can be prefilled with attributes REDCap obtains at login, where available — the REDCap username, first name, last name, email address and others.

Prefilled fields are ordinary fields and remain editable unless you prevent it. To lock them, add `@READONLY` (still visible) or `@HIDDEN-SURVEY` (not shown) — see [RC-AT-02 — @HIDDEN & @READONLY — Visibility Control](RC-AT-02_Action-Tags-Hidden-and-Readonly.md).

Prefill applies to page 1 only. Fields on later pages of a multi-page survey are not prefilled.

### 5.3 Allow Access for Internal Users Only

If the instance uses one of the **"X & Table-based"** authentication methods (for example LDAP & Table-based, or Entra ID & Table-based), an extra option appears: **Allow access for internal users only**. When it is selected, Table-based users — normally external collaborators with REDCap-managed accounts — are blocked from the survey while REDCap login protection is on.

This option does not appear on instances that use only one authentication method.

### 5.4 Who Can Get In

Under any authentication method **other than Table-based**, a person who has never used REDCap and has no REDCap account can still reach the survey, provided they pass the institution's authentication (for example, the institutional SSO). REDCap login protection therefore means "anyone who can authenticate to this REDCap instance", not "existing REDCap users" or "users of this project". Project user rights are not checked.

> **Institution-specific:** Who can pass authentication depends on how the instance's SSO or LDAP is scoped — sometimes the whole institution, sometimes a subset, sometimes affiliates too. Ask your REDCap administrator before relying on REDCap login protection to restrict a survey to a particular group.

### 5.5 Public Reports and Public Dashboards

The same protection can be applied to any **public report** or **public project dashboard**. Once the report or dashboard is public, a button immediately beneath it (labelled **"Enabled REDCap login protection"** in the 17.5.0 release notes) turns it on. Viewers then have to log in to REDCap, if not already logged in, before the report or dashboard is displayed. See [RC-EXPRT-06 — Custom Reports: Setup & Field Selection](RC-EXPRT-06_Custom-Reports-Setup-and-Field-Selection.md) §4.2 and [RC-PROJ-03 — Project Dashboards](RC-PROJ-03_Project-Dashboards.md) §5.

### 5.6 Save & Return Later

A respondent who logs in does not need a Return Code to resume a survey with **Save & Return Later** enabled.

> **Version caveat (17.5.0–17.5.3 Standard):** REDCap login protection could still ask the respondent for a **Return Code** on surveys with Save & Return Later enabled. Fixed in 17.5.4.

---

## 6. Security Settings (Optional)

### 6.1 Failed Login Attempt Limit

Sets the number of consecutive failed login attempts allowed before the respondent is temporarily locked out. Set to **0** to disable lockouts entirely.

Enabling a lockout limit is recommended for studies where the login field values could be guessed systematically (e.g., when only a single date-of-birth field is required).

### 6.2 Lockout Duration

The number of minutes a respondent remains locked out after exceeding the failed attempt limit. Set to **0** to disable. This setting has no effect unless the Failed Login Attempt Limit is also set above 0.

---

## 7. Common Questions

**Q: A respondent says they cannot log in even though their information is correct. What should I check?**
Verify that the login field values stored in their record exactly match what they are entering. Pay attention to field validation — for example, if the date field uses a specific date format, the respondent must enter the date in that format. Also check whether the respondent has been locked out due to too many failed attempts; lockout status can be checked and cleared through the Survey Distribution Tools.

**Q: Will Survey Login interrupt a Survey Queue flow?**
No. Once a respondent has logged in, REDCap will not prompt them again for any survey in the same project within the 30-minute authentication window. A respondent moving through a Survey Queue will only log in once at the start and then proceed through the queue without interruption.

**Q: Can I use Survey Login on a Public Survey?**
No, not in field-value mode. Survey Login cannot be applied to the Public Survey (the survey accessible via the public survey link). Because public surveys are designed for first-time respondents who do not yet have a record, there is no data to validate against. Survey Login applies once a record exists. REDCap login protection (Section 5) does not need record data, but the 17.5.0 release notes do not say whether it covers the Public Survey — test it on your instance before relying on it.

**Q: Can I make people log in with their REDCap account to take a survey?**
Yes, on REDCap+ instances at 17.5.0 or higher — select **Enforce REDCap login protection** in the Survey Login settings (Section 5). Without REDCap+, the only built-in option is field-value Survey Login.

**Q: Can I capture who completed a survey without asking them to type their name and email?**
With REDCap login protection, yes: prefill page-1 fields with the logged-in user's username, name and email, and lock them with `@READONLY` or `@HIDDEN-SURVEY` (Section 5.2).

**Q: Can I pre-fill survey questions from URL parameters when Survey Login is on?**
Yes, on current versions.

> **Version caveat (below 17.5.1 Standard / 17.3.14 LTS):** URL-parameter prefill silently failed on surveys with Survey Login enabled — the values were dropped and the fields loaded blank. Fixed in 17.5.1 Standard and 17.3.14 LTS.

**Q: Does Survey Login apply to survey invitations sent through the Participant List?**
Yes, if Survey Login is enabled for that survey. Respondents who click their individualized invitation link will be prompted to enter their login field values before the survey loads.

**Q: What happens if a login field is empty for a record?**
If the stored value for a required login field is empty (null), the respondent cannot match that field. If the minimum required fields setting means the empty field is not required (e.g., minimum is 2 out of 3 configured fields and the other two have values), the respondent can still authenticate using the populated fields.

**Q: Can I configure different login fields for different surveys?**
No. Login fields are project-wide. All surveys that use Survey Login in the project use the same login fields.

**Q: What if I want to restrict which surveys require login?**
Set **Apply survey login to** to *Only selected surveys*, then enable Survey Login per instrument on each survey's Survey Settings page.

---

## 8. Common Mistakes & Gotchas

**Enabling Survey Login before login field values are populated.** Survey Login is only effective if the respondent's record already contains values for the login fields. If you distribute surveys before populating those fields (e.g., before importing participant data), respondents may fail authentication even though they are legitimate participants. Always confirm data is loaded before enabling Survey Login.

**Choosing login fields with inconsistent formatting.** Fields like phone numbers or addresses can be stored in many formats. If your project was populated from an external source, values may have inconsistent formatting (e.g., "01-01-1980" vs "1980-01-01"). This causes legitimate respondents to fail authentication. Use fields with controlled, predictable values — especially validated date or number fields.

**Expecting Survey Login to work on a Public Survey.** A common misconception is that Survey Login can be used to gate who can fill out the first survey. It cannot — Survey Login only activates once a record exists. For access control on initial enrollment, consider using a different approach such as a unique access code managed outside of REDCap.

**Setting the minimum required fields too low for sensitive data.** A minimum of 1 out of 3 configured fields means a respondent only needs to get one field right to gain access. For studies with sensitive data, set the minimum to 2 or 3 to require more than a single correct value.

**Treating REDCap login protection as a project user list.** Under SSO or LDAP, anyone who can authenticate to the instance can open the survey, including people who have never used REDCap (Section 5.4). Project user rights are not checked. If only specific people should respond, check the prefilled username against an expected list — for example with branching logic or a Data Quality rule — or use field-value Survey Login against pre-loaded records.

**Leaving prefilled user fields editable.** Prefilled username, name and email fields can be overwritten by the respondent unless they carry `@READONLY` or `@HIDDEN-SURVEY`. If the values are your record of who responded, lock them.

**Not providing a custom error message.** Without a custom error message, failed respondents see a generic REDCap error with no guidance on how to get help. Always configure a custom error message with a contact point so respondents know who to reach when they cannot log in.

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
