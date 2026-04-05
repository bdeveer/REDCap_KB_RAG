RC-INST-01

**Institution-Specific Settings & Policies**

| **Article ID** | RC-INST-01 |
|---|---|
| **Domain** | Institution |
| **Applies To** | All REDCap users at this installation |
| **Prerequisite** | None |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-NAV-UI-01 — Project Navigation UI; RC-NAV-UI-02 — Project Menu Reference; RC-USER-04 — User Rights: User Management; RC-SURV-03 — Survey Settings: Behavior, Access & Termination |

---

# 1. Overview

This article documents settings, policies, and configurations that are specific to this REDCap installation. REDCap is a platform that each institution configures independently — feature availability, approval workflows, time zones, and support channels all vary by site. When another KB article refers you to "check with your local support team" or "see institution-specific settings," this is the article to consult.

> **Note for KB maintainers:** Entries marked with `[FILL IN]` require confirmation from the REDCap administrator before publishing. Do not leave placeholder values in the live KB.

---

# 2. Institution Identity & Support

**Institution name:** `[FILL IN — e.g., University Medical Center Groningen]`

**REDCap URL:** `[FILL IN — e.g., https://redcap.yoursite.nl]`

**Support channel ("Contact REDCap Administrator" link):** `[FILL IN — describe what the link opens: e.g., a service desk ticket form at servicedesk.yoursite.nl, an email address, or an intake survey]`

**Support hours:** `[FILL IN — e.g., Monday–Friday, 09:00–17:00 CET]`

**Custom Links in the project menu:** `[FILL IN — list any custom links the admin team has added to the left-hand menu, e.g., Training Calendar, SOP Library, Request Form]`

---

# 3. Server Time Zone

**Server time zone:** `[FILL IN — e.g., Europe/Amsterdam (CET/CEST)]`

REDCap schedules all time-sensitive operations — survey expiration, automated survey invitations, alert send times, and randomization timestamps — using the **server's clock**, not the user's local device time. If you are in a different time zone than the server, you must account for the offset when entering scheduled times.

**Practical guidance:** When scheduling anything in REDCap (invitations, alerts, survey expiration), always check the server time displayed in the scheduling dialog and calculate the offset relative to your local time before saving.

> See also: RC-SURV-03 (Survey Expiration), RC-SURV-05 (Survey Invitations), RC-SURV-06 (Automated Survey Invitations), RC-ALERT-01 (Alerts & Notifications)

---

# 4. Draft Mode Approval Policy

When a project is in **Production** status, structural changes (adding/editing/deleting fields, forms, or events) must be made in **Draft Mode**. Once submitted, changes either go through automatically or wait for administrator review — this is controlled at the installation level.

**Policy at this institution:** `[FILL IN — choose one:]`

- **Auto-approve** — Minor changes (e.g., adding a new field, editing a field label) are approved automatically without administrator review. Major changes (e.g., deleting a field with data) always require manual review regardless of this setting.
- **Always require admin review** — All Draft Mode submissions are held in a pending queue and reviewed by an administrator before taking effect.
- **[FILL IN with specifics if hybrid or nuanced]**

**What this means for you:** If your Draft Mode changes do not appear immediately after submission, they are in the pending queue awaiting administrator approval. Allow `[FILL IN — e.g., 1–2 business days]` for review. Contact the support team if urgent.

> See also: RC-FD-02 — Online Designer, RC-NAV-UI-02 — Project Menu Reference

---

# 5. User Account Creation

REDCap users must have an active account in this installation before they can be added to any project. If a colleague is not found when you search the user list in User Rights, they do not yet have an account.

**How accounts are created at this institution:** `[FILL IN — e.g., "Users self-register via the REDCap login page" / "Accounts are provisioned by IT on request — submit a ticket via [link]" / "Accounts are created automatically for all institution employees via SSO"]`

**Who to contact for account issues:** `[FILL IN — e.g., the REDCap support team via the Contact REDCap Administrator link, or IT helpdesk]`

> See also: RC-USER-02 — User Rights: Adding Users & Managing Roles

---

# 6. Global User Suspension Policy

REDCap distinguishes between project-level suspension (managed by project users) and global suspension (managed by administrators only). Global suspension prevents a user from logging in to REDCap at all.

**Automatic global suspension at this institution:** `[FILL IN — e.g., "Accounts inactive for more than 12 months are automatically suspended" / "No automatic suspension — global suspension is only applied manually upon request"]`

**Re-activation process:** `[FILL IN — e.g., "Contact the REDCap support team to request reactivation" / "Submit a helpdesk ticket with the affected username"]`

> See also: RC-USER-04 — User Rights: User Management

---

# 7. Optional Feature Availability

Some REDCap features are optional and must be enabled at the system level by an administrator. The availability of these features at this installation is documented below.

## 7.1 MyCap Mobile App

**Status:** `[FILL IN — Enabled / Not enabled]`

MyCap allows participants to interact with a REDCap project via a mobile app. If MyCap is not enabled at the system level, projects cannot use MyCap Participant Management and MyCap smart variables will return blank.

`[If enabled:]` To enable MyCap for a specific project, contact the REDCap support team. Note that MyCap is mutually exclusive with longitudinal mode.

> See also: RC-PIPE-16 — Smart Variables: MyCap, RC-NAV-UI-02 — Project Menu Reference

## 7.2 REDCap Messenger

**Status:** `[FILL IN — Enabled / Not enabled]`

REDCap Messenger is a HIPAA-compliant in-project messaging tool for user-to-user communication within the same REDCap installation. It cannot send messages to external email addresses or to other REDCap installations.

> See also: RC-NAV-UI-02 — Project Menu Reference

## 7.3 Text-to-Speech in Surveys

**Status:** `[FILL IN — Enabled / Disabled by administrator]`

When enabled, participants can have survey questions read aloud via a third-party text-to-speech service. Because audio is processed externally, this feature may raise privacy concerns for surveys collecting sensitive information.

`[If enabled:]` Consult your local IRB before enabling text-to-speech on surveys that collect sensitive or identifiable data. The IRB contact for REDCap-related questions at this institution is `[FILL IN]`.

`[If disabled:]` This feature has been disabled system-wide by the REDCap administrator and is not available in any project at this institution.

> See also: RC-SURV-03 — Survey Settings: Behavior, Access & Termination

## 7.4 Data Resolution Workflow (Queries)

**Status:** `[FILL IN — Enabled / Not enabled]`

The Data Resolution Workflow allows project staff to log, track, and resolve data queries (field-level discrepancy notes) within REDCap. It must be enabled at the system level and then activated per project.

> See also: RC-DE-12 — Data Resolution Workflow

## 7.5 e-Consent Framework

**Status:** `[FILL IN — Available / Not available]`

The e-Consent Framework allows REDCap to capture and archive signed electronic consent forms.

**IRB acceptability at this institution:** `[FILL IN — e.g., "Electronic consent collected via REDCap is accepted by [Institution IRB name] for studies meeting the following criteria: [list criteria]" / "Check with your study's IRB — acceptability is determined per study, not institution-wide"]`

> **Important:** The e-Consent Framework is a tool, not a legal determination. Always confirm with your local Institutional Review Board (IRB) that electronic consent is acceptable for your specific study before using it.

> See also: RC-SURV-08 — e-Consent Framework: Setup & Management, RC-SURV-03 — Survey Settings

---

# 8. External Modules

External modules extend REDCap's functionality and are developed by the REDCap community. They must be downloaded and enabled by the administrator. Availability varies by installation.

**Modules available at this institution:** `[FILL IN — list enabled modules, e.g.:]`

| Module | Description | Notes |
|--------|-------------|-------|
| `[Module name]` | `[Brief description]` | `[Any local restrictions or contact info]` |

**Requesting a new module:** `[FILL IN — e.g., "Submit a request via the REDCap support channel. Requests are reviewed monthly." / "Contact the REDCap administrator directly."]`

**Policy on enabling modules per project:** `[FILL IN — e.g., "Users can enable approved modules themselves from the External Modules section." / "All module activations must be requested from the support team."]`

> See also: RC-NAV-UI-02 — Project Menu Reference (External Modules section)

---

# 9. Local Policies & Procedures

## 9.1 Project Request Process

`[FILL IN — describe how users create a new REDCap project: e.g., "Any user with a REDCap account can create a new project directly from the My Projects page" / "New projects must be requested via [form/link]; a REDCap administrator will create it and assign you as owner."]`

## 9.2 Data Storage & Retention

`[FILL IN — e.g., "REDCap data is stored on institution-managed servers located in [location]. Retention policies follow [policy name/link]. Projects in 'Completed' status are retained for [X years] before archiving."]`

## 9.3 Data Classification & Permitted Data Types

`[FILL IN — e.g., "This installation is approved for storage of [pseudonymous / anonymized / identifiable] research data. Directly identifiable data such as BSN (Dutch citizen service number) may not be stored. For questions about data classification, contact the Data Protection Officer at [email]."]`

## 9.4 Training Requirements

`[FILL IN — e.g., "All new REDCap users must complete the introductory e-learning module before accessing production projects. Training is available at [link]."]`

---

# 10. Common Questions

**Q: I can't find a colleague in the user search when adding them to my project. What should I do?**

**A:** The user does not have a REDCap account at this installation. Refer them to the account creation process described in Section 5.

---

**Q: My Draft Mode changes haven't appeared yet. Are they lost?**

**A:** They are not lost. Depending on the approval policy (Section 4), they may be awaiting administrator review. Allow the stated turnaround time, then contact the support team if still pending.

---

**Q: I need to schedule something at a specific local time. How do I convert to server time?**

**A:** Check the server time zone in Section 3. REDCap also displays the current server time in scheduling dialogs — use that as your reference point.

---

**Q: A feature I read about in the KB doesn't appear in my project. Why?**

**A:** The feature may be disabled at this installation, or it may need to be enabled per-project by an administrator. Check Section 7 for optional feature availability. If a feature is listed as enabled but still does not appear, contact the support team.

---

**Q: Where do I report a bug or a REDCap problem?**

**A:** Use the **Contact REDCap Administrator** link in the left-hand project menu (or at the bottom of any REDCap page outside a project). This routes directly to the local support team and automatically includes your project context.
