---
id: RC-PROF-01
title: My Profile — User Profile Settings
domain: Profile (PROF)
applies_to:
- All REDCap users
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — My Profile
  behaviour checked against source code; pages not re-captured. The username answer
  was checked on v17.5.6 and v16.0.59 test instances, read-only
prerequisites:
- Active REDCap user account
version: '1.5'
last_updated: 2026-11
related:
- id: RC-CC-03
  title: 'Control Center: Security & Authentication'
- id: RC-CC-07
  title: 'Control Center: Users & Access Management'
- id: RC-USER-01
  title: 'User Rights: Overview & Three-Tier Access'
- id: RC-API-01
  title: REDCap API
- id: RC-MSG-01
  title: REDCap Messenger
tags:
- profile (prof)
synonyms:
- how do i change my account settings
- update my email address in redcap
- where are my api tokens
- change my password
- edit my display name and preferences
- manage notification settings for my account
- access my profile page
- update my personal account information
- can i change my redcap username
---

# 1. Overview

Every REDCap user has a **My Profile** page where they can view and update their personal account information, set display preferences, manage notification settings and, if they hold one, see their Super API Token. My Profile is a user-facing page — it controls only your own account and is separate from the administrator tools in the Control Center.

What is available on My Profile depends partly on how your REDCap instance is configured, particularly the authentication method in use. Some settings (such as password management) are only shown for users on table-based authentication; Single Sign-On (SSO) users manage credentials through their institution's external system.

---

# 2. Accessing My Profile

Open My Profile from the top navigation bar of the REDCap home-area pages (such as **Home** and **My Projects**): click **Profile**. On medium-width screens the link is tucked into the **More** menu in that bar. The link is not shown inside a project, so leave the project (for example via **My Projects**) first.

The whole page is a single form behind its several **Save** buttons, so it is safest to edit and save one section at a time.

Your profile also shows your **user sponsor**, if an administrator has assigned one to your account.

---

# 3. Basic Information

The **Basic Information** section of My Profile contains your core contact details:

- **First name** and **Last name**
- **Primary email** — the main email address for your account; used for system notifications, password recovery, and 2FA codes sent via email. A confirmation field requires you to enter the address twice when changing it.
- **Phone number** — optional; used for 2FA by phone call. Supports extensions (enter a comma between the number and extension).
- **Mobile phone** — optional; used for 2FA codes sent by SMS text message.

Both phone fields only appear when your institution has enabled the matching 2FA method (SMS or phone call).

After editing fields, click **Save Basic Info** to apply changes.

> **Institution-specific:** administrators can lock the name and email fields so users cannot edit them, and can restrict which email domains are accepted. Your primary email also cannot be the same as your secondary or tertiary email. If a field is read-only or an address is rejected, check with your REDCap administrators.

> **Email verification:** If you change your primary email address, REDCap sends a verification email to the new address. Your account will remain inaccessible until you confirm the new address via that email. Do not change your primary email to an address you cannot immediately access.

> **Note for SSO users:** If your institution uses Shibboleth, LDAP, or another external identity provider with automatic profile population enabled, your name and email may be overwritten from the directory on each login. Changes you make manually may not persist. Contact your REDCap administrator if this is a problem.

---

# 4. Additional Email Addresses

The **Additional Options** section allows you to add up to two additional email addresses to your account — a **secondary email** and a **tertiary email**.

These additional addresses have a specific and limited purpose:

- They **can** be used as the "From" address when REDCap sends survey invitations, alerts, and similar outbound emails on your behalf.
- They **cannot** be used for account retrieval or important system notifications — only your primary email address is used for those.

To add a secondary or tertiary email, enter the address and click **Add email**. REDCap sends a verification email to the new address, and it becomes usable once you confirm it. Addresses can be removed at any time; removing an address means it can no longer be used as a "From" address in REDCap emails, though you can re-add it later.

> **Practical use case:** If you want survey invitation emails to appear to come from a study-specific address rather than your personal institutional address, add that address here and select it as the "From" address in your alert or invitation settings.

---

# 5. User Preferences

The **User Preferences** section controls how dates, numbers, and data exports are displayed to you personally within REDCap. These are per-user settings and do not affect how data is stored or how other users see the interface.

## 5.1 Date and Time Format

Choose your preferred format for how dates and timestamps are displayed. REDCap supports many combinations of ordering (month-day-year vs. day-month-year vs. year-month-day) and separators (hyphen, slash, period), as well as 12-hour (AM/PM) or 24-hour time. Examples:

- `MM/DD/YYYY and 12-hour AM/PM time` (e.g., 12/31/2004 10:57pm)
- `DD/MM/YYYY and 24-hour time` (e.g., 31/12/2004 22:57)
- `YYYY-MM-DD and 24-hour time` (e.g., 2004-12-31 22:57)

## 5.2 Number Format — Decimal Character

Choose whether a period (`.`) or comma (`,`) is used as the decimal separator when displaying numbers (e.g., `3.14` vs `3,14`).

## 5.3 Number Format — Thousands Separator

Choose the character used to group thousands in large numbers. Options include comma, period, apostrophe, blank space, or no separator (e.g., `1,000,000` vs `1.000.000` vs `1 000 000`).

## 5.4 CSV File Download Delimiter

Choose the field delimiter used when you download data as a CSV file. Options include comma, semicolon, tab, blank space, pipe (`|`), or caret (`^`). This is useful if your statistical software or spreadsheet application expects a specific delimiter.

After adjusting any preference, click **Save Preferences**.

---

# 6. Messenger Notification Preferences

The **Notification Preferences for REDCap Messenger** section appears only when REDCap Messenger is enabled on your server. It controls how REDCap notifies you about incoming messages in the Messenger system when you are not actively logged in.

## 6.1 Message Digest Frequency

Choose how often REDCap sends you an email notifying you of unread Messenger messages. Note: the notification email tells you that messages are waiting — it does not include the message content itself. Options are:

- 2-hour digest
- 4-hour digest
- 6-hour digest
- 8-hour digest
- 12-hour digest
- Daily digest
- None (email notifications disabled)

## 6.2 Instant Notifications for Important or Tagged Messages

A separate checkbox lets you override the digest frequency for high-priority messages: if enabled, REDCap sends an immediate email notification whenever you receive a message marked as **Important** or whenever you are tagged with **@username** in a conversation. This applies even if your digest is set to a long interval or disabled.

## 6.3 General and System Notifications

A second checkbox controls whether you receive email notifications for **General Notifications** (broadcast messages sent by REDCap administrators) and **System Notifications** (announcements about new features and system updates).

After adjusting settings, click **Save Messenger Preferences**.

---

# 7. Password Management

For users authenticated via **table-based (local) authentication**, the profile page includes a **Reset password** button. Clicking it sets a temporary password on your account and takes you to a password reset page, where you enter your new password twice. You are not asked for your current password.

Password requirements (minimum length, complexity, reuse rules) are set by your administrator and are shown on the password reset page. See [RC-CC-03 — Control Center: Security & Authentication](RC-CC-03_Control-Center-Security-and-Authentication.md) for a description of the system-level password policy settings.

> **SSO users** (Shibboleth, Google OAuth2, Microsoft Entra ID, LDAP, etc.) do not see the **Reset password** button here. Your password is managed through your institution's identity system, not REDCap.

---

# 8. Two-Factor Authentication Setup

If two-factor authentication (2FA) is enabled on your REDCap instance, users can set up their preferred verification method from My Profile.

## 8.1 Authenticator App (TOTP)

If the **Google/Microsoft Authenticator** option is enabled by your administrator, a QR code is displayed on your profile page. Scan this code with the Google Authenticator or Microsoft Authenticator app on your phone to register REDCap. After setup, the app generates a 6-digit code you enter at login.

You do not have to set this up on My Profile in advance. If you have not yet registered an authenticator app, REDCap shows you a one-time setup QR code at the 2FA step of login, which you can scan there. My Profile remains the place to view the QR code again later.

> **If your administrator asks you to re-enrol:** secrets issued before REDCap 17.5.1 Standard / 17.3.14 LTS / 16.0.52 LTS were generated by a weaker method, so administrators may arrange for your authenticator secret to be regenerated after upgrading. REDCap has no reset button for this: your REDCap server administrator has to make the change behind the scenes. Once it is done, scan the new QR code on My Profile, then delete the old REDCap entry from your authenticator app, because the old one will no longer produce valid codes.

## 8.2 Other 2FA Methods

Other methods — email-based codes, SMS text messages, phone calls, Duo push — do not require setup on the profile page. Email codes go to your primary email, SMS codes to your **Mobile phone**, phone calls to your **Phone number**, and Duo authenticates through the Duo service.

## 8.3 Trusted Devices

My Profile has no list of trusted devices. If your administrator allows REDCap to remember a device after 2FA, that trust is stored in the browser you logged in with, one browser at a time. To stop a browser being trusted, clear that browser's cookies for the REDCap site.

---

# 9. API Tokens

My Profile does **not** list your project API tokens. The only token it can show is a **Super API Token**, and only if an administrator has issued you one; it is displayed masked. Most users have no Super API Token, so most users see no token on My Profile at all.

Project API tokens live on each project's **API** page (in the project's left-hand menu, visible to users with API rights in that project). There you can:

- **View** your token for that project
- **Request** a token if you have API rights but no token yet (subject to administrator approval, depending on system configuration)
- **Regenerate** or **Delete** your own token, for example if it was accidentally shared. These actions are logged.

> **Tokens are project-specific.** Each token grants API access to exactly one project. If you need access to multiple projects via the API, you will have one token per project, each found on that project's API page.

> **Administrators** have a system-wide API Tokens view in the Control Center ([RC-CC-07 — Control Center: Users & Access Management](RC-CC-07_Control-Center-User-Management.md)) that shows all tokens across all users and projects. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) for requesting and using tokens.

---

# 10. What Cannot Be Changed on My Profile

The following account properties are not user-editable from My Profile:

| Property | Who Controls It |
| --- | --- |
| Username | REDCap administrator (cannot be changed after account creation in most installations) |
| Account status (active / suspended) | REDCap administrator |
| Administrator privileges | REDCap super-administrator |
| Project access | Project owner or user with User Rights privileges on that project |
| Authentication method (table-based vs. SSO) | REDCap administrator (system-level configuration) |

If you need to change your username or resolve an account access issue, contact your REDCap administrator.

---

# 11. Common Questions

**Q: How do I access My Profile?**
Click **Profile** in the top navigation bar of a home-area page such as **Home** or **My Projects** (on medium-width screens, look under **More**). The link does not appear inside a project, so leave the project first.

**Q: I changed my primary email address but now I can't log in. What happened?**
When you change your primary email, REDCap sends a verification email to the new address. Your account is inaccessible until you click the confirmation link in that email. Check your inbox (and spam folder) for the verification message. If you cannot access the new email address, contact your REDCap administrator to resolve the account.

**Q: What is the difference between my primary, secondary, and tertiary email addresses?**
Your primary email is the one REDCap uses for all system notifications, password recovery, and 2FA codes — it is the authoritative contact address for your account. Secondary and tertiary emails are optional extras that can only be used as the "From" address on outbound survey invitations and alerts. They cannot be used to recover your account.

**Q: Why don't I see a Reset password button on my profile?**
If your institution uses Single Sign-On (such as Shibboleth, LDAP, or Google OAuth2), your password is managed outside of REDCap. The **Reset password** button only appears for table-based (local) authentication accounts. Change your password through your institution's standard password management tools.

**Q: I set up the Google Authenticator app on my profile, but now I've lost access to my phone. What do I do?**
Contact your REDCap administrator. From the Control Center, an administrator can email you the authenticator-app setup instructions, so you can add your existing REDCap entry to the app on a new phone. If other 2FA methods are enabled on your server (such as email), you can also choose one of those at login.

**Q: Where do I find my API token?**
Project API tokens are on each project's **API** page, not on My Profile. Open the project, click **API** in the left-hand menu (you need API rights in that project), and your token for that project is shown there. If you have none yet, request one on that page; this may require administrator approval. My Profile only shows a Super API Token, and only if an administrator has issued you one.

**Q: My date format preference doesn't seem to apply everywhere in REDCap. Is that expected?**
User preferences affect how dates and numbers are displayed in the data entry interface and similar views. Some system-generated outputs (such as exported files or reports) may use a fixed format regardless of your personal preference setting. If a specific downstream tool requires a particular date or CSV format, use the export options at the time of download rather than relying solely on your profile preference.

**Q: Can I change my REDCap username?**
You can't change it yourself, but a REDCap administrator can. From REDCap 17.5.0, administrators have a **Change Username** button on the user's Browse Users page. On earlier versions, including 16.0.59 LTS, the page has no such option, and a change typically requires direct database intervention. Either way, contact your REDCap administrator and treat it as exceptional.

**Q: Can I delete my own account?**
No. User account deletion is an administrator function. Contact your REDCap administrator if you need your account removed.

---

# 12. Common Mistakes & Gotchas

**Changing your primary email to an address you don't yet control.** Because REDCap locks your account until the new email is verified, entering a typo or an address you cannot immediately access will lock you out. Double-check the address using the re-entry confirmation field before saving.

**Assuming secondary/tertiary email addresses receive system notifications.** Only your primary email receives important REDCap system messages, password resets, and 2FA codes. Secondary and tertiary addresses exist solely to serve as "From" addresses on outbound emails. Do not instruct colleagues to contact you via a secondary address with the expectation that REDCap will notify you there.

**Changing your email without realizing SSO will overwrite it.** In Shibboleth and some LDAP configurations, the administrator may have enabled automatic population of profile fields from the identity provider on each login. If so, any email address you enter in My Profile will be silently overwritten at your next login. Confirm with your administrator whether auto-population is enabled.

**Ignoring the CSV delimiter preference when switching between tools.** If you export data for use in different statistical packages, you may need to adjust the CSV delimiter preference to match each tool's expectations. R, SPSS, and Excel generally handle comma-delimited files, but some European software defaults to semicolon. Adjust the preference before downloading, or use the export dialog options at export time.

**Expecting the profile page to control project access.** My Profile only manages your own account details. It has no controls for which projects you are a member of or what your user rights are within those projects. Project access is managed by the project owner or a user with User Rights privileges on each individual project.

**Sharing a screenshot of a project's API page that includes your token.** The project API page displays your actual token value. Redact it in any screenshot shared with support staff or used for documentation. An exposed token grants API access to your project data immediately — without a password. If a token is accidentally shared, regenerate or delete it yourself on that project's API page.

**Looking for project API tokens on My Profile.** They are not there. Each project token is on that project's API page; My Profile only shows a Super API Token if you have one.

**Entering your SMS number in the wrong phone field.** SMS 2FA codes go to **Mobile phone**; **Phone number** is used for phone-call 2FA. Put your cell number in **Mobile phone** if you want codes by text message.

---

# 13. Related Articles

- [RC-CC-03 — Control Center: Security & Authentication](RC-CC-03_Control-Center-Security-and-Authentication.md) Configuration
- [RC-CC-07 — Control Center: Users & Access Management](RC-CC-07_Control-Center-User-Management.md)
- [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md)
- [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md)
- [RC-MSG-01 — REDCap Messenger](RC-MSG-01_REDCap-Messenger.md)
