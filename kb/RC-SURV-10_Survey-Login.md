RC-SURV-10

**Survey Login**

| **Article ID** | RC-SURV-10 |
| --- | --- |
| **Domain** | Surveys |
| **Applies To** | All REDCap projects with surveys enabled; Survey Login cannot be applied to a Public Survey |
| **Prerequisite** | RC-SURV-01 — Surveys – Basics; RC-SURV-02 — Survey Settings: Basic Options & Design |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-SURV-01 — Surveys – Basics; RC-SURV-03 — Survey Settings: Behavior, Access & Termination; RC-SURV-04 — Survey Link Types & Access Methods; RC-SURV-05 — Participant List & Manual Survey Invitations |

---

# 1. Overview

## What is this?

Survey Login is a project-level security feature that forces respondents to authenticate before they can view or complete a survey. Instead of a traditional username and password, respondents prove their identity by entering one or more field values already stored in their record — such as a last name, date of birth, or participant ID. REDCap checks those entered values against the record and only grants access if they match.

## Why does it matter?

By default, anyone who possesses a survey link can open and complete a survey. Survey Login adds a verification layer that ties survey access to data that only the legitimate respondent should know. This is useful in studies where surveys are distributed broadly (e.g., via bulk email) and the research team wants assurance that the correct person is completing each record's survey.

## Scope and Assumptions

This article covers Survey Login configuration only. It assumes:
- Surveys are already enabled for the project (see RC-SURV-01).
- At least one instrument is enabled as a survey.
- The relevant login fields already exist in the project's data dictionary and contain values for each record that will be prompted to log in.

---

# 2. Key Concepts & Definitions

## Survey Login

A project-level feature that displays an authentication prompt before a respondent can access a survey. The respondent must enter values matching field data already saved in their record.

## Login Fields

The project fields — up to three — that REDCap uses as the authentication challenge. REDCap compares what the respondent types against what is stored in the record. If the values match (subject to the minimum required fields setting), the respondent is granted access.

## Minimum Required Fields

When more than one login field is configured, this setting controls how many of those fields must be correctly entered before access is granted. For example, if three login fields are configured but the minimum is set to 2, the respondent only needs to match any two of the three fields.

## 30-Minute Authentication Window

Once a respondent has successfully logged in, REDCap does not prompt them again for any survey in the same project for the next 30 minutes. This prevents repeated authentication challenges when a respondent is completing multiple surveys in sequence, such as when working through a Survey Queue.

## Lockout

An optional security measure that temporarily blocks a respondent's ability to attempt login after a defined number of consecutive failed attempts. The lockout duration is configurable in minutes.

---

# 3. How Survey Login Works

## 3.1 When the Login Prompt Appears

Survey Login behavior depends on whether a record exists for the respondent at the time they access the survey.

- **No record exists yet (e.g., first visit via a Public Survey):** The survey opens normally. The login prompt is not displayed because there is no record data to validate against.
- **A record already exists:** The respondent is always prompted to log in before the survey loads.

This means Survey Login has no effect on the very first interaction for a new respondent. It becomes active on all subsequent survey accesses once a record has been created — whether by the respondent completing a prior survey, by staff data entry, or by data import.

> **Important:** Survey Login **cannot** be applied to a Public Survey (the first survey in a project accessible via the public survey link). A Public Survey by definition has no record to validate against when a new respondent arrives. Survey Login applies to all other survey access methods.

## 3.2 Where to Configure Survey Login

Survey Login is configured at the **project level**, not per survey. Access it from the **Online Designer** via the **Survey Login** button in the toolbar.

The settings defined here apply globally across the project's surveys, with one exception: which surveys the login is applied to can be restricted per survey (see Section 4.4).

---

# 4. Configuration Settings

## 4.1 Enable Survey Login

Toggle Survey Login on or off for the project. When disabled, all surveys open normally with no authentication prompt. When enabled, the remaining settings become active.

## 4.2 Login Fields

Select the fields that respondents must enter to authenticate. Up to three fields can be configured. Fields are selected from a dropdown of all project variables.

**Choosing effective login fields:**

- Use fields whose values are known to the respondent but not easily guessed by others.
- Date of birth and last name are common choices, particularly for studies where participants were pre-enrolled and their data was imported before surveys were distributed.
- Avoid fields with free-text values that have high variability in formatting (e.g., an open-text address field), as minor differences in spacing or capitalization can cause legitimate respondents to fail authentication.
- The values must already be saved in the respondent's record before they attempt to log in. If a field is empty for a record, the respondent cannot match it.

> **Note:** Field values in REDCap are case-insensitive for Survey Login matching purposes. A respondent entering "smith" will match a stored value of "Smith".

## 4.3 Minimum Number of Fields Required for Login

When more than one login field is configured, this setting determines how many must be correctly entered to authenticate. Options are 1, 2, or 3 (the maximum equals the number of configured login fields).

Setting the minimum below the total number of configured fields provides a fallback: a respondent who cannot remember one value may still authenticate using the other fields. This can reduce support burden in studies with longer follow-up periods where participants may forget one of their registered values.

## 4.4 Apply Survey Login To

Controls which surveys in the project require login:

- **All surveys** — Survey Login is applied to every survey in the project.
- **Only selected surveys** — Survey Login applies only to surveys that have been individually configured to use it. Per-survey login opt-in is managed on the **Survey Settings** page for each instrument.

Use the "only selected surveys" option when your project contains a mix of staff-distributed and publicly accessible surveys, or when Survey Login should only apply to sensitive instruments.

## 4.5 Custom Error Message

An optional message displayed on the login form when a respondent fails authentication. Supports HTML, including hyperlinks.

Use this to provide respondents with a contact point for login problems. Example:

```
If you have any trouble logging in to the survey, please contact
<a href="mailto:study-support@example.edu">study-support@example.edu</a> for help.
```

If no custom message is provided, REDCap displays a generic error.

---

# 5. Security Settings (Optional)

## 5.1 Failed Login Attempt Limit

Sets the number of consecutive failed login attempts allowed before the respondent is temporarily locked out. Set to **0** to disable lockouts entirely.

Enabling a lockout limit is recommended for studies where the login field values could be guessed systematically (e.g., when only a single date-of-birth field is required).

## 5.2 Lockout Duration

The number of minutes a respondent remains locked out after exceeding the failed attempt limit. Set to **0** to disable. This setting has no effect unless the Failed Login Attempt Limit is also set above 0.

---

# 6. Common Questions

**Q: A respondent says they cannot log in even though their information is correct. What should I check?**
Verify that the login field values stored in their record exactly match what they are entering. Pay attention to field validation — for example, if the date field uses a specific date format, the respondent must enter the date in that format. Also check whether the respondent has been locked out due to too many failed attempts; lockout status can be checked and cleared through the Survey Distribution Tools.

**Q: Will Survey Login interrupt a Survey Queue flow?**
No. Once a respondent has logged in, REDCap will not prompt them again for any survey in the same project within the 30-minute authentication window. A respondent moving through a Survey Queue will only log in once at the start and then proceed through the queue without interruption.

**Q: Can I use Survey Login on a Public Survey?**
No. Survey Login cannot be applied to the Public Survey (the survey accessible via the public survey link). Because public surveys are designed for first-time respondents who do not yet have a record, there is no data to validate against. Survey Login applies once a record exists.

**Q: Does Survey Login apply to survey invitations sent through the Participant List?**
Yes, if Survey Login is enabled for that survey. Respondents who click their individualized invitation link will be prompted to enter their login field values before the survey loads.

**Q: What happens if a login field is empty for a record?**
If the stored value for a required login field is empty (null), the respondent cannot match that field. If the minimum required fields setting means the empty field is not required (e.g., minimum is 2 out of 3 configured fields and the other two have values), the respondent can still authenticate using the populated fields.

**Q: Can I configure different login fields for different surveys?**
No. Login fields are project-wide. All surveys that use Survey Login in the project use the same login fields.

**Q: What if I want to restrict which surveys require login?**
Set **Apply survey login to** to *Only selected surveys*, then enable Survey Login per instrument on each survey's Survey Settings page.

---

# 7. Common Mistakes & Gotchas

**Enabling Survey Login before login field values are populated.** Survey Login is only effective if the respondent's record already contains values for the login fields. If you distribute surveys before populating those fields (e.g., before importing participant data), respondents may fail authentication even though they are legitimate participants. Always confirm data is loaded before enabling Survey Login.

**Choosing login fields with inconsistent formatting.** Fields like phone numbers or addresses can be stored in many formats. If your project was populated from an external source, values may have inconsistent formatting (e.g., "01-01-1980" vs "1980-01-01"). This causes legitimate respondents to fail authentication. Use fields with controlled, predictable values — especially validated date or number fields.

**Expecting Survey Login to work on a Public Survey.** A common misconception is that Survey Login can be used to gate who can fill out the first survey. It cannot — Survey Login only activates once a record exists. For access control on initial enrollment, consider using a different approach such as a unique access code managed outside of REDCap.

**Setting the minimum required fields too low for sensitive data.** A minimum of 1 out of 3 configured fields means a respondent only needs to get one field right to gain access. For studies with sensitive data, set the minimum to 2 or 3 to require more than a single correct value.

**Not providing a custom error message.** Without a custom error message, failed respondents see a generic REDCap error with no guidance on how to get help. Always configure a custom error message with a contact point so respondents know who to reach when they cannot log in.

---

# 8. Related Articles

- RC-SURV-01 — Surveys – Basics
- RC-SURV-02 — Survey Settings: Basic Options & Design
- RC-SURV-03 — Survey Settings: Behavior, Access & Termination
- RC-SURV-04 — Survey Link Types & Access Methods
- RC-SURV-05 — Participant List & Manual Survey Invitations
- RC-SURV-07 — Survey Queue
