RC-INST-01

**Institution-Specific Settings & Policies**

| **Article ID** | RC-INST-01 |
|---|---|
| **Domain** | Institution |
| **Applies To** | All REDCap users at this installation |
| **Prerequisite** | None |
| **Version** | 2.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-CC-02 — General Configuration; RC-CC-03 — Security & Authentication; RC-CC-04 — User Settings; RC-CC-05 — File Storage; RC-CC-06 — Modules & Services; RC-CC-07 — User Management; RC-NAV-UI-01 — Project Navigation UI; RC-NAV-UI-02 — Project Menu Reference; RC-USER-02 — User Rights: Adding Users & Managing Roles; RC-USER-04 — User Rights: User Management; RC-SURV-03 — Survey Settings: Behavior, Access & Termination; RC-API-01 — REDCap API |

---

> ## ⚠️ RAG IMPLEMENTATION NOTICE
>
> **This article is currently a template. It does not yet contain institution- or instance-specific information.**
>
> RC-INST-01 is the single most important article to populate before deploying this KB in a RAG system. Every `[FILL IN]` placeholder in this article represents a question that a real user might ask — and that the RAG system currently cannot answer correctly. Unanswered questions about login method, 2FA, feature availability, file upload limits, and support channels are among the most common support requests at any REDCap installation.
>
> **Before going live with this KB, your REDCap administrator should:**
> 1. Create one copy of this article per active instance (production, test, development, etc.)
> 2. Replace every `[FILL IN]` with the actual value for that instance
> 3. Remove placeholder rows from tables (e.g., the Other Instances table in Section 3, the External Modules table in Section 9)
> 4. Delete feature rows from the Section 8 table that are definitively not available, to avoid confusing the model
> 5. Remove this notice block once the article is fully populated
>
> Until this article is populated, the RAG system will correctly answer generic REDCap questions but will be unable to answer institution-specific questions — and may actively mislead users by returning empty or placeholder responses as if they were answers.

---

# 1. Overview

This article documents the settings, policies, and configurations that apply to a specific REDCap instance at this institution. REDCap is a platform that every institution — and every instance within that institution — configures independently. Feature availability, login method, approval workflows, file size limits, time zones, and support channels all vary by instance. When another KB article says "check with your local support team" or "see institution-specific settings," this is the article to consult.

> **Note for KB maintainers:** Entries marked with `[FILL IN]` require confirmation from the REDCap administrator before publishing. Do not leave placeholder values in the live KB. This article should exist in a separate version for each instance (or with a clearly scoped section per instance — see Section 3).

> **Note on multiple instances:** Most institutions run REDCap on more than one server — typically at minimum a test/staging instance and a production instance, and often a development instance as well. Each is independently configured. Settings documented here apply **only to the instance named in Section 2**. See Section 3 for a summary of other instances available at this institution.

---

# 2. About This Instance

**Instance name:** `[FILL IN — e.g., Production / Test / Development]`

**REDCap URL:** `[FILL IN — e.g., https://redcap.yoursite.nl]`

**Institution name:** `[FILL IN — e.g., University Medical Center Groningen]`

**Support channel ("Contact REDCap Administrator" link):** `[FILL IN — describe what the link opens: e.g., a service desk ticket form at servicedesk.yoursite.nl, an email address, or an intake survey]`

**Support hours:** `[FILL IN — e.g., Monday–Friday, 09:00–17:00 CET]`

**Custom links in the project menu:** `[FILL IN — list any custom links the admin team has added to the left-hand menu, e.g., Training Calendar, SOP Library, Request Form]`

---

# 3. Other Instances at This Institution

Most institutions run REDCap across multiple environments, each with its own URL, configuration, and purpose. Certain settings — authentication method, 2FA, record limits, feature toggles, and External Module availability — commonly differ between instances. **An API token generated on one instance is not valid on another.**

| Instance | URL | Primary Purpose | Notes |
|---|---|---|---|
| Production | `[FILL IN]` | Live research data collection | Full security posture; all approved features active |
| Test / Staging | `[FILL IN]` | Pre-production testing and UAT | May have restricted features; **do not use for real participant data** |
| Development | `[FILL IN]` | Admin, IT, and module development | Often uses local or table-based auth; looser settings |
| `[Other — e.g., Training]` | `[FILL IN]` | `[FILL IN]` | `[FILL IN]` |

> **Warning:** Test/staging instances may have the REDCap cron job accessible via browser trigger. If scheduled alerts, invitations, or notifications have been configured on a test project that mirrors production content, triggering the cron manually can send those emails to real recipients. Exercise caution when running background processes on non-production instances.

---

# 4. Authentication & Login

## 4.1 Authentication Method

**Method in use on this instance:** `[FILL IN — e.g., Microsoft Entra ID (SSO) / Shibboleth & Table-based / Table-based only / LDAP / OpenID Connect]`

`[If SSO:]` Users log in with their institutional account via `[FILL IN — e.g., the Microsoft Entra ID button on the login page]`. You do not need a separate REDCap password.

`[If hybrid SSO + Table-based:]` Two login options are shown on the login page: `[FILL IN — button labels]`. Institutional employees should use the SSO option. Local/guest accounts use the table-based option.

`[If table-based only:]` Users log in with a REDCap-specific username and password. See Section 4.4 for password requirements.

## 4.2 Two-Factor Authentication (2FA)

**2FA status on this instance:** `[FILL IN — Disabled / Required for all users / Required for table-based users only]`

`[If enabled:]` After entering your username and password, you will be prompted for a second verification step. Available methods on this instance:

| 2FA Method | Available | Notes |
|---|---|---|
| Google / Microsoft Authenticator app | `[Yes / No]` | Set up via your REDCap Profile page |
| Email (6-digit code) | `[Yes / No]` | Sent to your primary REDCap email |
| SMS via Twilio | `[Yes / No]` | Requires a mobile number on your Profile |
| Duo push notification | `[Yes / No]` | Requires a Duo account |

**Device trust period:** `[FILL IN — e.g., "After completing 2FA, you can choose to trust your device for 30 days, after which 2FA is required again" / "Device trust is not enabled — 2FA is required at every login"]`

**2FA on internal network:** `[FILL IN — e.g., "2FA is not required when connecting from the institutional network or VPN" / "2FA is always required regardless of network location"]`

## 4.3 Session Timeout

**Auto-logout after inactivity:** `[FILL IN — e.g., "30 minutes" / "Disabled"]`

REDCap will display a 2-minute warning before logging you out. Unsaved form data will be lost. Save regularly when entering data on long forms.

## 4.4 Login Lockout

**Failed login lockout:** `[FILL IN — e.g., "After 5 failed attempts, your account is locked for 15 minutes" / "Lockout is not enabled on this instance"]`

If you are locked out, wait for the lockout period to expire and try again, or contact the support team to unlock your account manually.

## 4.5 Password Policy (Table-based accounts only)

This section applies only if your account uses table-based authentication. SSO-managed accounts follow the password policy of the identity provider, not REDCap.

| Policy | Setting |
|---|---|
| Minimum password length | `[FILL IN — e.g., 12 characters]` |
| Complexity requirement | `[FILL IN — e.g., Must include uppercase, lowercase, numbers, and special characters]` |
| Password expiration | `[FILL IN — e.g., Every 90 days / No expiration]` |
| Password reuse limit | `[FILL IN — e.g., Cannot reuse the last 5 passwords / No restriction]` |

**To reset a forgotten password:** Use the "Forgot your password?" link on the login page. `[FILL IN if custom recovery instructions apply, e.g., for hybrid environments where external users should use a different reset process.]`

---

# 5. Server Time Zone

**Server time zone:** `[FILL IN — e.g., Europe/Amsterdam (CET/CEST)]`

REDCap schedules all time-sensitive operations — survey expiration, automated survey invitations, alert send times, and randomization timestamps — using the **server's clock**, not the user's local device time. If you are in a different time zone than the server, you must account for the offset when entering scheduled times.

**Practical guidance:** When scheduling anything in REDCap (invitations, alerts, survey expiration), check the server time shown in the scheduling dialog and calculate the offset relative to your local time before saving.

> See also: RC-SURV-03 (Survey Expiration), RC-SURV-05 (Survey Invitations), RC-SURV-06 (Automated Survey Invitations), RC-ALERT-01 (Alerts & Notifications)

---

# 6. User Accounts & Access

## 6.1 Account Creation

REDCap users must have an active account on **this instance** before they can be added to any project. If a colleague is not found when you search the user list in User Rights, they do not yet have an account on this instance.

**How accounts are created:** `[FILL IN — e.g., "Users self-register via the REDCap login page using their institutional SSO" / "Accounts are provisioned by IT on request — submit a ticket via [link]" / "Accounts are created automatically for all institution employees on first SSO login, provided they are on the User Allowlist"]`

**User Allowlist:** `[FILL IN — e.g., "This instance uses a User Allowlist. Even if you can authenticate via SSO, you cannot access REDCap until an administrator has added your username to the allowlist. To request access, contact [support channel]." / "No allowlist — any institutional SSO user can access REDCap after first login."]`

**Domain restriction:** `[FILL IN — e.g., "Only email addresses ending in @yoursite.nl can be associated with REDCap accounts on this instance." / "No email domain restriction."]`

> See also: RC-USER-02 — User Rights: Adding Users & Managing Roles

## 6.2 Account Suspension & Expiration

REDCap distinguishes between project-level suspension (managed by project users) and global suspension (managed by administrators only). Global suspension prevents a user from logging in to REDCap at all.

**Automatic suspension for inactivity:** `[FILL IN — e.g., "Accounts that have not logged in or used the API for more than 180 days are automatically suspended. A notification email is sent at the time of suspension." / "No automatic suspension — global suspension is applied manually only."]`

**Account expiration:** `[FILL IN — e.g., "Guest or external user accounts are set with an expiration date. You will receive a reminder email 14 days and 2 days before expiration. Contact the support team or your account sponsor to extend your account." / "Accounts do not expire by default."]`

**Re-activation process:** `[FILL IN — e.g., "Contact the REDCap support team to request reactivation" / "Submit a helpdesk ticket with the affected username"]`

> See also: RC-USER-04 — User Rights: User Management

## 6.3 User Access Dashboard (UAD)

**UAD status:** `[FILL IN — Disabled / Enabled: notification only / Enabled: notification + monthly email reminder]`

`[If enabled:]` The User Access Dashboard (UAD) prompts project owners and users with User Rights privileges to periodically review who has access to their projects. `[FILL IN — e.g., "A reminder appears on your My Projects page. A monthly email reminder is sent on the first weekday of each month."]` The UAD is only visible to users who have User Rights privileges in at least one project.

## 6.4 Access Control Groups

**Access Control Groups (ACGs) in use:** `[FILL IN — Yes / No]`

`[If yes:]` This instance uses Access Control Groups, which define a system-wide ceiling on what user privileges can be granted within projects. If you are a project owner trying to assign a specific right to a colleague and find the checkbox is unavailable or the change is rejected, it may be because the applicable ACG does not permit that right. Contact the support team for assistance.

## 6.5 User Profile Editing

**Can users edit their own name and email in their REDCap Profile?**

| Field | Self-editable |
|---|---|
| First and last name | `[Yes / No]` |
| Primary email address | `[Yes / No]` |

`[If no:]` Profile updates must be requested via `[FILL IN — support channel / IT]`. This restriction is in place for `[FILL IN — e.g., regulatory (21 CFR Part 11) compliance reasons / account integrity reasons]`.

---

# 7. Project Creation & Lifecycle

## 7.1 Creating a New Project

**Can users create projects directly?** `[FILL IN — Yes, any user can create a new project from the My Projects page / No, users must submit a request and an administrator creates the project]`

`[If request-based:]` To request a new project, `[FILL IN — describe the process, e.g., "use the 'Request New Project' button on the My Projects page, which submits a request to the REDCap administrator. You will be notified by email when the project is ready."]`

`[If using a project creation survey:]` When you create or copy a project, you will be redirected to a short intake form. Complete this form to register project metadata (e.g., IRB number, PI details, data classification) with the support team.

## 7.2 Moving a Project to Production

**Can users move projects to Production status themselves?** `[FILL IN — Yes / No, a request is submitted to an administrator]`

`[If request-based:]` Click the "Request To Move to Production" button in Project Setup. Allow `[FILL IN — e.g., 1–2 business days]` for review. Contact the support team if urgent.

`[If using a production move survey:]` You will be prompted to complete a short checklist or certification form before the move is finalized.

> See also: RC-PROJ-01 — Project Lifecycle: Status and Settings

## 7.3 Draft Mode Approval Policy

When a project is in **Production** status, structural changes (adding/editing/deleting fields, forms, or events) must be made in **Draft Mode**. Once submitted, changes either auto-approve or wait for administrator review — this is controlled at the instance level.

**Policy on this instance:** `[FILL IN — choose one:]`

- **Auto-approve** — Minor changes (e.g., adding a new field, editing a field label) are approved automatically. Major changes (e.g., deleting a field with data, changing a field type) always require manual review.
- **Always require admin review** — All Draft Mode submissions are held in a pending queue and reviewed by an administrator before taking effect.
- **[FILL IN with specifics if hybrid]**

**Turnaround time for manual review:** `[FILL IN — e.g., 1–2 business days]`

> See also: RC-FD-02 — Online Designer

## 7.4 Production Modifications Without Draft Mode

Some structural changes on Production projects may be allowed without Draft Mode involvement, depending on instance configuration.

| Action | Permitted by normal users on this instance |
|---|---|
| Modify repeating instruments / events setup | `[Yes / No — admin only]` |
| Add or modify events and arms (longitudinal) | `[Yes / No — admin only]` |

## 7.5 Development Project Record Limit

**Maximum records in a Development-status project:** `[FILL IN — e.g., 100 records / No limit]`

`[If a limit is set:]` When the limit is reached, you cannot create additional records until the project moves to Production. This is intentional — it prevents large amounts of test data from accumulating in development projects. If you need a higher limit for a specific project, contact the support team.

## 7.6 Project Deletion

When a user requests project deletion, REDCap does not immediately purge the project. The project is hidden from users but remains in the database during a lag period, during which an administrator can restore it.

**Project deletion lag on this instance:** `[FILL IN — e.g., 30 days / 14 days]`

After this period, the project is permanently deleted and can only be recovered from backup (not guaranteed). If you have accidentally deleted a project, contact the support team immediately.

---

# 8. Feature Availability

Some REDCap features must be enabled at the instance level by an administrator. The table below documents what is available on this instance. Features marked as requiring admin activation must be enabled per project by an administrator — contact the support team.

| Feature | Status | Notes |
|---|---|---|
| **Surveys** | `[Enabled / Disabled]` | Core survey functionality; project-level enable in Project Setup |
| **Randomization** | `[Enabled / Disabled]` | See RC-RAND-01 |
| **REDCap API** | `[Enabled / Disabled]` | See Section 9 and RC-API-01 |
| **REDCap Mobile App** (offline data entry) | `[Enabled / Disabled]` | See RC-MOB-01; users need explicit mobile app rights |
| **MyCap Mobile App** (participant app) | `[Enabled / Disabled / Admin activation required per project]` | See RC-MYCAP-01; mutually exclusive with longitudinal mode |
| **REDCap Messenger** | `[Enabled / Disabled]` | In-platform user-to-user messaging |
| **Text-to-Speech for Surveys** | `[Enabled / Disabled]` | Audio processed by IBM Watson via Vanderbilt; consult IRB before using on sensitive surveys |
| **Data Resolution Workflow** (Queries) | `[Enabled / Disabled]` | Must also be activated per project; see RC-DE-12 |
| **e-Consent Framework** | `[Enabled / Disabled]` | See RC-SURV-08; IRB acceptability is study-specific |
| **E-Signature** | `[Enabled / Disabled]` | Note: not compatible with Shibboleth or OAuth2 authentication |
| **Bulk Record Delete** | `[Enabled / Disabled]` | Available to users with Delete Records rights when enabled |
| **REDCap Shared Library** | `[Enabled / Disabled]` | Import from Consortium instrument library in Online Designer |
| **Field Bank (NLM)** | `[Enabled / Disabled]` | Import from NLM Field Bank in Online Designer |
| **Stats & Charts** | `[Enabled / Disabled]` | Aggregate data visualizations on project Stats & Charts tab |
| **Email Logging** | `[Enabled / Disabled]` | Users with User Rights can access outgoing email history for their project |
| **Protected Email Mode** | `[Enabled / Disabled]` | When active, alert/invitation bodies are replaced with secure links; see project-level settings |
| **Data Entry Trigger** | `[Enabled / Disabled]` | POST to external URL on record save; see RC-INTG-01 |
| **URL Shortening (REDCAP.LINK)** | `[Enabled / Disabled]` | Short links for public surveys, dashboards, and reports |
| **Video Embedding** | `[Enabled / Disabled]` | Embed video on Descriptive fields |
| **Google reCAPTCHA on Public Surveys** | `[Configured / Not configured]` | Per-project toggle available if configured; applies to public survey links only |
| **Twilio (SMS/voice)** | `[Enabled / Disabled / Admin activation required]` | For SMS survey invitations and alerts; see RC-TXT-01 |
| **Send-It (secure file transfer)** | `[Enabled / Disabled / Limited to: File Repository only / Home page only]` | Generates expiring download links for files |
| **File Upload Field Enhancement** (Part 11) | `[Enabled / Disabled]` | Password-verified file access for regulated studies |
| **E-Signature + Record Locking Enhancement** (Part 11) | `[Enabled / Disabled]` | PDF audit trail on lock; for regulated studies only |
| **Sync Calendar to External Application** | `[Enabled / Disabled]` | Calendar feed export from projects |
| **Computer Adaptive Tests (CATs)** | `[Enabled / Disabled]` | PROMIS and similar instruments from Shared Library |
| **Clinical Data Interoperability Services (CDIS)** | `[Enabled / Disabled / Admin activation required]` | EHR/clinical data pull; see RC-CDIS-01 |
| **Multi-Language Management (MLM)** | `[Enabled / Disabled]` | See RC-MLM-01 |
| **Double Data Entry** | `[Enabled / Disabled]` | Project-level feature for parallel data entry and adjudication |

> **If a feature listed as enabled is not visible in your project**, it may need to be activated at the project level, or your user rights may not include it. Contact the support team.

**IRB acceptability for e-Consent at this institution:** `[FILL IN — e.g., "Electronic consent collected via REDCap is accepted by [Institution IRB name] for studies meeting the following criteria: [list criteria]" / "Check with your study's IRB — acceptability is determined per study, not institution-wide"]`

---

# 9. External Modules

External modules extend REDCap's functionality and are developed by the REDCap community. They must be downloaded and enabled by the administrator before being available to projects.

**Modules available on this instance:** `[FILL IN — list enabled modules]`

| Module | Description | Activation | Notes |
|--------|-------------|------------|-------|
| `[Module name]` | `[Brief description]` | `[Self-serve / Request required]` | `[Any local restrictions or contact info]` |

**Requesting a new module:** `[FILL IN — e.g., "Submit a request via the REDCap support channel. Requests are reviewed monthly." / "Contact the REDCap administrator directly."]`

**Policy on enabling modules per project:** `[FILL IN — e.g., "Users can enable approved modules themselves from the External Modules section in Project Setup." / "All module activations must be requested from the support team."]`

> See also: RC-EM-01 — External Modules Overview

---

# 10. File Upload & Storage

Upload limits and available features differ by context. The values below apply to this instance.

## 10.1 Upload Size Limits

| Upload Location | Maximum File Size |
|---|---|
| File Repository (user-uploaded) | `[FILL IN — e.g., 50 MB / Server default]` |
| File Upload fields on forms/surveys | `[FILL IN — e.g., 20 MB / Server default]` |
| Send-It | `[FILL IN — e.g., 100 MB / Disabled]` |
| General attachments (DRW, Descriptive fields) | `[FILL IN — e.g., 20 MB / Server default]` |
| File Repository storage per project (total) | `[FILL IN — e.g., 500 MB / No limit]` |

If you receive an error when uploading a file, it is likely exceeding the limit for that context. Contact the support team if you need the limit raised for a specific project.

## 10.2 Restricted File Types

Certain file extensions are blocked from upload system-wide for security reasons. Blocked extensions include executables, scripts, and installer formats (.exe, .bat, .js, .php, .vbs, and others). You cannot upload these file types anywhere in REDCap, including the File Repository and file upload fields.

`[FILL IN — if the institution has added custom blocked types beyond REDCap defaults, list them here]`

## 10.3 File Version History

**File version history for File Upload fields:** `[Enabled by default / Disabled]`

`[If enabled:]` When you upload a new file to a File Upload field that already has a file, the previous file is retained as a version rather than deleted. Previous versions are accessible from the Data History popup on the field.

## 10.4 Public File Sharing from the File Repository

**Public file links from File Repository:** `[Enabled / Disabled]`

`[If enabled:]` Users can generate a public URL for any file in the File Repository that allows download without REDCap authentication. Use this only for files that do not contain personal data or other restricted information, in line with Section 11.3.

`[If disabled:]` Public file links are not available on this instance. All file access requires REDCap authentication.

---

# 11. API Access

**REDCap API status on this instance:** `[Enabled / Disabled]`

`[If enabled:]` The REDCap API allows external applications and scripts to interact with REDCap programmatically for importing data, exporting data, creating records, and more. API access requires a token specific to each user-project combination and to this instance — tokens from other instances are not valid here.

**How to obtain an API token:** `[FILL IN — e.g., "Any user with API Export or API Import rights in a project can generate their own token directly from the API section of that project." / "API token requests must be submitted to the support team. Navigate to the API section of your project and click 'Request API Token'."]`

**Generating tokens without admin approval:** `[FILL IN — Yes, users can self-generate / No, each request requires admin approval / Approval is required for some users only]`

**Super API Tokens:** `[FILL IN — e.g., "Super API Tokens (which allow project creation via API) are available only to designated users. Contact the support team if your integration requires project creation." / "Super API Tokens are not issued on this instance."]`

> See also: RC-API-01 — REDCap API

---

# 12. User & Display Defaults

These system defaults apply to all new accounts on this instance. Individual users can typically change these in their Profile.

| Setting | Default on This Instance |
|---|---|
| Date/time display format | `[FILL IN — e.g., DD-MM-YYYY, 24-hour]` |
| Decimal separator | `[FILL IN — e.g., Period (3.14) / Comma (3,14)]` |
| Thousands separator | `[FILL IN — e.g., Period (1.000.000) / Comma (1,000,000) / None]` |
| CSV export delimiter | `[FILL IN — e.g., Semicolon / Comma / Tab]` |

> If you export data and the file does not open correctly in Excel or another tool, check whether the delimiter matches what your application expects — especially if the decimal separator is a comma, in which case a semicolon delimiter is standard.

---

# 13. Local Policies & Procedures

## 13.1 Data Storage & Retention

`[FILL IN — e.g., "REDCap data is stored on institution-managed servers located in [location]. Retention policies follow [policy name/link]. Projects in 'Completed' status are retained for [X years] before archiving/deletion."]`

## 13.2 Backup & Disaster Recovery

`[FILL IN — e.g., "The REDCap database is backed up nightly. Backups are retained for [X days]. In the event of accidental deletion or corruption, contact the support team immediately — recovery from backup may be possible if the request is made promptly."]`

## 13.3 Data Classification & Permitted Data Types

`[FILL IN — e.g., "This instance is approved for storage of [pseudonymous / anonymized / identifiable] research data. Directly identifiable data such as BSN (Dutch citizen service number) may not be stored. For questions about data classification, contact the Data Protection Officer at [email]."]`

Different instances at this institution may have different data classification approvals. Verify the classification level of the instance you are using before uploading participant data.

## 13.4 Training Requirements

`[FILL IN — e.g., "All new REDCap users must complete the introductory e-learning module before accessing production projects. Training is available at [link]."]`

## 13.5 Maintenance & Downtime

`[FILL IN — e.g., "Scheduled maintenance takes place on [day/time]. An announcement is posted on the REDCap home page at least [X days] in advance. Emergency maintenance may occur with shorter notice; check [status page URL] for current system status."]`

---

# 14. Common Questions

**Q: I can't find a colleague in the user search when adding them to my project. What should I do?**

**A:** The user does not have a REDCap account on this instance. Refer them to the account creation process described in Section 6.1. If this instance uses a User Allowlist, they may have an account but not yet be on the list.

---

**Q: My Draft Mode changes haven't appeared yet. Are they lost?**

**A:** They are not lost. Depending on the approval policy (Section 7.3), they may be awaiting administrator review. Allow the stated turnaround time, then contact the support team if still pending.

---

**Q: I need to schedule something at a specific local time. How do I convert to server time?**

**A:** Check the server time zone in Section 5. REDCap also displays the current server time in scheduling dialogs — use that as your reference point.

---

**Q: A feature I read about in the KB doesn't appear in my project. Why?**

**A:** Several possibilities: (1) the feature is disabled at the instance level — check Section 8; (2) the feature needs per-project activation by an administrator — contact the support team; (3) your user rights do not include it — check with your project owner. If still unclear, contact the support team.

---

**Q: My API script worked on test but fails on production. Why?**

**A:** API tokens are instance-specific and project-specific. The token you generated on the test instance is not valid on production. You need a separate token for the production version of the project. Refer to Section 11 for how to request one.

---

**Q: I accidentally deleted my project. Can it be recovered?**

**A:** Possibly. Projects are not immediately purged — there is a deletion lag period (Section 7.6). Contact the support team immediately. If the lag period has not expired, the project can be restored. After the lag period, recovery requires a database backup restore and is not guaranteed.

---

**Q: Where do I report a bug or a REDCap problem?**

**A:** Use the **Contact REDCap Administrator** link in the left-hand project menu (or at the bottom of any REDCap page outside a project). This routes directly to the local support team and automatically includes your project context.
