RC-PROF-01

**My Profile — User Profile Settings**

| **Article ID** | RC-PROF-01 |
| --- | --- |
| **Domain** | Profile (PROF) |
| **Applies To** | All REDCap users |
| **Prerequisite** | Active REDCap user account |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-CC-03 — Security & Authentication Configuration; RC-CC-07 — Users & Access Management; RC-USER-01 — User Rights Overview; RC-API-01 — REDCap API; RC-MSG-01 — REDCap Messenger |

---

# 1. Overview

Every REDCap user has a **My Profile** page where they can view and update their personal account information, set display preferences, manage notification settings, and access their API tokens. My Profile is a user-facing page — it controls only your own account and is separate from the administrator tools in the Control Center.

What is available on My Profile depends partly on how your REDCap instance is configured, particularly the authentication method in use. Some settings (such as password management) are only shown for users on table-based authentication; Single Sign-On (SSO) users manage credentials through their institution's external system.

---

# 2. Accessing My Profile

My Profile is accessible from the top of any REDCap page. Click on your username in the global navigation bar to reveal a dropdown menu, then click **Profile**. This takes you directly to your profile settings page.

---

# 3. Basic Information

The **Basic Information** section of My Profile contains your core contact details:

- **First name** and **Last name**
- **Primary email** — the main email address for your account; used for system notifications, password recovery, and 2FA codes sent via email. A confirmation field requires you to enter the address twice when changing it.
- **Phone number** — optional; used for SMS-based 2FA if configured at your institution. Supports extensions (enter a comma between the number and extension).
- **Mobile phone number** — a separate field from the phone number above; also optional.

After editing fields, click **Save Basic Info** to apply changes.

> **Email verification:** If you change your primary email address, REDCap sends a verification email to the new address. Your account will remain inaccessible until you confirm the new address via that email. Do not change your primary email to an address you cannot immediately access.

> **Note for SSO users:** If your institution uses Shibboleth, LDAP, or another external identity provider with automatic profile population enabled, your name and email may be overwritten from the directory on each login. Changes you make manually may not persist. Contact your REDCap administrator if this is a problem.

---

# 4. Additional Email Addresses

The **Additional Options** section allows you to add up to two additional email addresses to your account — a **secondary email** and a **tertiary email**.

These additional addresses have a specific and limited purpose:

- They **can** be used as the "From" address when REDCap sends survey invitations, alerts, and similar outbound emails on your behalf.
- They **cannot** be used for account retrieval or important system notifications — only your primary email address is used for those.

To add a secondary or tertiary email, enter the address and click **Add email**. Addresses can be removed at any time; removing an address means it can no longer be used as a "From" address in REDCap emails, though you can re-add it later.

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

The **Notification Preferences for REDCap Messenger** section controls how REDCap notifies you about incoming messages in the Messenger system when you are not actively logged in.

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

For users authenticated via **table-based (local) authentication**, the profile page includes a section to change your password. Enter your current password and then the new password twice to confirm.

Password requirements (minimum length, complexity, reuse rules) are set by your administrator and are displayed in this section. See RC-CC-03 for a description of the system-level password policy settings.

> **SSO users** (Shibboleth, Google OAuth2, Microsoft Entra ID, LDAP, etc.) do not see a password change section here. Your password is managed through your institution's identity system, not REDCap.

---

# 8. Two-Factor Authentication Setup

If two-factor authentication (2FA) is enabled on your REDCap instance, users can set up their preferred verification method from My Profile.

## 8.1 Authenticator App (TOTP)

If the **Google/Microsoft Authenticator** option is enabled by your administrator, a QR code is displayed on your profile page. Scan this code with the Google Authenticator or Microsoft Authenticator app on your phone to register REDCap. After setup, the app generates a 6-digit code you enter at login.

This setup step must be completed on My Profile before you can use the authenticator app option at login.

## 8.2 Other 2FA Methods

Other methods — email-based codes, SMS via Twilio, Duo push — do not require setup on the profile page. They use the email address or phone number already on your account, or authenticate via the Duo service.

## 8.3 Trusted Devices

If your administrator has enabled device trust, you may see a list of previously trusted devices on your profile page. You can remove trusted devices here to force re-authentication on the next login from those devices.

---

# 9. API Tokens

The My Profile page includes an **API Tokens** section listing all REDCap API tokens associated with your account — one per project for which you have been granted API access.

From this section you can:

- **View** your token for each project (click to reveal or copy)
- **Request a new token** for a project where you have API access but no token yet (subject to administrator approval, depending on system configuration)
- See which projects you currently hold tokens for

> **Tokens are project-specific.** Each token grants API access to exactly one project. If you need access to multiple projects via the API, you will have one token per project.

> **Administrators** have a system-wide API Tokens view in the Control Center (RC-CC-07) that shows all tokens across all users and projects. Standard users only see their own tokens.

If you need a token revoked or regenerated (for example, if a token was accidentally shared), contact your REDCap administrator — only administrators can delete or regenerate tokens.

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
Click your username in the global navigation bar at the top of any REDCap page and select "Profile" from the dropdown menu.

**Q: I changed my primary email address but now I can't log in. What happened?**
When you change your primary email, REDCap sends a verification email to the new address. Your account is inaccessible until you click the confirmation link in that email. Check your inbox (and spam folder) for the verification message. If you cannot access the new email address, contact your REDCap administrator to resolve the account.

**Q: What is the difference between my primary, secondary, and tertiary email addresses?**
Your primary email is the one REDCap uses for all system notifications, password recovery, and 2FA codes — it is the authoritative contact address for your account. Secondary and tertiary emails are optional extras that can only be used as the "From" address on outbound survey invitations and alerts. They cannot be used to recover your account.

**Q: Why don't I see a password change section on my profile?**
If your institution uses Single Sign-On (such as Shibboleth, LDAP, or Google OAuth2), your password is managed outside of REDCap. The password change section only appears for table-based (local) authentication accounts. Change your password through your institution's standard password management tools.

**Q: I set up the Google Authenticator app on my profile, but now I've lost access to my phone. What do I do?**
Contact your REDCap administrator. Administrators can reset or bypass 2FA for a user account through the Control Center. You cannot self-service this recovery from the profile page.

**Q: Where do I find my API token?**
API tokens are listed in the API Tokens section of My Profile. You will see one token listed per project for which you have been granted API access. If no token is listed for a project, you may need to request one (from the project's API page or your profile), which may require administrator approval.

**Q: My date format preference doesn't seem to apply everywhere in REDCap. Is that expected?**
User preferences affect how dates and numbers are displayed in the data entry interface and similar views. Some system-generated outputs (such as exported files or reports) may use a fixed format regardless of your personal preference setting. If a specific downstream tool requires a particular date or CSV format, use the export options at the time of download rather than relying solely on your profile preference.

**Q: Can I change my REDCap username?**
In most REDCap installations, usernames cannot be changed after the account is created. If you need a username change, contact your REDCap administrator — it typically requires direct database intervention and should be considered exceptional.

**Q: Can I delete my own account?**
No. User account deletion is an administrator function. Contact your REDCap administrator if you need your account removed.

---

# 12. Common Mistakes & Gotchas

**Changing your primary email to an address you don't yet control.** Because REDCap locks your account until the new email is verified, entering a typo or an address you cannot immediately access will lock you out. Double-check the address using the re-entry confirmation field before saving.

**Assuming secondary/tertiary email addresses receive system notifications.** Only your primary email receives important REDCap system messages, password resets, and 2FA codes. Secondary and tertiary addresses exist solely to serve as "From" addresses on outbound emails. Do not instruct colleagues to contact you via a secondary address with the expectation that REDCap will notify you there.

**Changing your email without realizing SSO will overwrite it.** In Shibboleth and some LDAP configurations, the administrator may have enabled automatic population of profile fields from the identity provider on each login. If so, any email address you enter in My Profile will be silently overwritten at your next login. Confirm with your administrator whether auto-population is enabled.

**Ignoring the CSV delimiter preference when switching between tools.** If you export data for use in different statistical packages, you may need to adjust the CSV delimiter preference to match each tool's expectations. R, SPSS, and Excel generally handle comma-delimited files, but some European software defaults to semicolon. Adjust the preference before downloading, or use the export dialog options at export time.

**Expecting the profile page to control project access.** My Profile only manages your own account details. It has no controls for which projects you are a member of or what your user rights are within those projects. Project access is managed by the project owner or a user with User Rights privileges on each individual project.

**Sharing a screenshot of your profile that includes your API token.** The API Tokens section displays your actual token values. Redact token values in any screenshot shared with support staff or used for documentation. An exposed token grants API access to your project data immediately — without a password. Contact your administrator to regenerate a token if one is accidentally shared.

**Not completing authenticator app setup before a login is required.** If your administrator has enforced 2FA with the authenticator app option, you must complete the QR code setup on My Profile before your next login that requires 2FA. Complete the setup proactively, not after you are locked out.

---

# 13. Related Articles

- RC-CC-03 — Control Center: Security & Authentication Configuration
- RC-CC-07 — Control Center: Users & Access Management
- RC-USER-01 — User Rights: Overview & Three-Tier Access
- RC-API-01 — REDCap API
- RC-MSG-01 — REDCap Messenger
