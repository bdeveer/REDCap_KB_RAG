RC-PROF-01

**My Profile — User Profile Settings**

| **Article ID** | RC-PROF-01 |
| --- | --- |
| **Domain** | Profile (PROF) |
| **Applies To** | All REDCap users |
| **Prerequisite** | Active REDCap user account |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-CC-03 — Security & Authentication Configuration; RC-CC-07 — Users & Access Management; RC-USER-01 — User Rights Overview; RC-API-01 — REDCap API |

---

# 1. Overview

Every REDCap user has a **My Profile** page where they can view and update their personal account information, manage security settings, and access their API tokens. My Profile is a user-facing page — it controls only your own account and is separate from the administrator tools in the Control Center.

What is available on My Profile depends partly on how your REDCap instance is configured, particularly the authentication method in use. Some settings (such as password management) are only shown for users on table-based authentication; Single Sign-On (SSO) users manage credentials through their institution's external system.

---

# 2. Accessing My Profile

My Profile is accessible from the top of any REDCap page. Look for your username or a **"My Profile"** link in the global navigation bar at the top of the screen. Clicking it takes you directly to your profile page.

Alternatively, the profile page can be reached by navigating to `redcap_v{version}/Profile/index.php` directly — though using the navigation link is the standard approach.

---

# 3. Personal Information

The top section of My Profile displays your basic account information. Users can typically edit:

- **First name** and **Last name**
- **Email address** — used for system notifications, password recovery, and 2FA codes sent via email
- **Institution / Affiliation** — your organization or department
- **Phone number** — optional; used for SMS-based 2FA if enabled at your institution
- **Sponsor** — at some institutions, a sponsor name is required for account creation and is displayed here
- **Title / Position** — optional descriptive field

After editing any field, click the **Save** button to apply changes.

> **Note for SSO users:** If your institution uses Shibboleth, LDAP, or another external identity provider, and the administrator has enabled automatic profile population from that provider, your name and email may be overwritten from the directory on each login. Changes you make manually may not persist. Contact your REDCap administrator if this is a problem.

---

# 4. Password Management

For users authenticated via **table-based (local) authentication**, the profile page includes a section to change your password. Enter your current password and then the new password twice to confirm.

Password requirements (minimum length, complexity, reuse rules) are set by your administrator and are displayed in this section. See RC-CC-03 for a description of the system-level password policy settings.

> **SSO users** (Shibboleth, Google OAuth2, Microsoft Entra ID, LDAP, etc.) do not see a password change section here. Your password is managed through your institution's identity system, not REDCap.

---

# 5. Two-Factor Authentication Setup

If two-factor authentication (2FA) is enabled on your REDCap instance, users can set up their preferred verification method from My Profile.

## 5.1 Authenticator App (TOTP)

If the **Google/Microsoft Authenticator** option is enabled by your administrator, a QR code is displayed on your profile page. Scan this code with the Google Authenticator or Microsoft Authenticator app on your phone to register REDCap. After setup, the app generates a 6-digit code you enter at login.

This setup step must be completed on My Profile before you can use the authenticator app option at login.

## 5.2 Other 2FA Methods

Other methods — email-based codes, SMS via Twilio, Duo push — do not require setup on the profile page. They use the email address or phone number already on your account, or authenticate via the Duo service.

## 5.3 Trusted Devices

If your administrator has enabled device trust, you may see a list of previously trusted devices on your profile page. You can remove trusted devices here to force re-authentication on the next login from those devices.

---

# 6. Email Notification Preferences

REDCap can send email notifications for project activity. The profile page may include controls for:

- **Daily digest** — a scheduled summary email of recent project notifications, as an alternative to receiving individual emails immediately as events occur
- Whether to receive notifications at all for certain event types

Available options depend on your administrator's configuration. If no notification preferences appear, your institution may not have enabled user-level control over these settings.

---

# 7. API Tokens

The My Profile page includes an **API Tokens** section listing all REDCap API tokens associated with your account — one per project for which you have been granted API access.

From this section you can:

- **View** your token for each project (click to reveal or copy)
- **Request a new token** for a project where you have API access but no token yet (subject to administrator approval, depending on system configuration)
- See which projects you currently hold tokens for

> **Tokens are project-specific.** Each token grants API access to exactly one project. If you need access to multiple projects via the API, you will have one token per project.

> **Administrators** have a system-wide API Tokens view in the Control Center (RC-CC-07) that shows all tokens across all users and projects. Standard users only see their own tokens.

If you need a token revoked or regenerated (for example, if a token was accidentally shared), contact your REDCap administrator — only administrators can delete or regenerate tokens.

---

# 8. What Cannot Be Changed on My Profile

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

# 9. Common Questions

**Q: How do I access My Profile?**
Click your username or the "My Profile" link in the global navigation bar at the top of any REDCap page. This takes you directly to your profile settings.

**Q: I changed my email address but I'm still receiving notifications at the old address. Why?**
Email changes on the profile page take effect immediately for future system-generated emails. If you are still receiving messages at your old address, check whether there are any pending emails already queued from before the change, and verify the new address saved successfully. If your institution uses SSO and the administrator has enabled automatic profile population from the identity provider, your email may have been overwritten back to the directory value at your next login.

**Q: Why don't I see a password change section on my profile?**
If your institution uses Single Sign-On (such as Shibboleth, LDAP, or Google OAuth2), your password is managed outside of REDCap. The password change section only appears for table-based (local) authentication accounts. Change your password through your institution's standard password management tools.

**Q: I set up the Google Authenticator app on my profile, but now I've lost access to my phone. What do I do?**
Contact your REDCap administrator. Administrators can reset or bypass 2FA for a user account through the Control Center. You cannot self-service this recovery from the profile page.

**Q: Where do I find my API token?**
API tokens are listed in the API Tokens section of My Profile. You will see one token listed per project for which you have been granted API access. If no token is listed for a project, you may need to request one (from the project's API page or from your profile, depending on system configuration), which may require administrator approval.

**Q: Can I change my REDCap username?**
In most REDCap installations, usernames cannot be changed after the account is created. If you need a username change, contact your REDCap administrator — it typically requires direct database intervention and should be considered exceptional.

**Q: Can I delete my own account?**
No. User account deletion is an administrator function. Contact your REDCap administrator if you need your account removed.

---

# 10. Common Mistakes & Gotchas

**Changing your email without realizing SSO will overwrite it.** In Shibboleth and some LDAP configurations, the administrator may have enabled automatic population of profile fields from the identity provider on each login. If so, any email address you enter in My Profile will be silently overwritten at your next login. If persistent manual profile values are important to you, confirm with your administrator whether auto-population is enabled and whether it can be disabled for your account.

**Expecting the profile page to control project access.** My Profile only manages your own account details. It has no controls for which projects you are a member of or what your user rights are within those projects. Project access is managed by the project owner or a user with User Rights privileges on each individual project.

**Sharing a screenshot of your profile that includes your API token.** The API Tokens section displays your actual token values. If you take a screenshot of your profile page for any reason (to share with support staff, for documentation, etc.), be careful to redact the token values. An exposed token grants API access to your project data immediately — without a password. Contact your administrator to regenerate a token if one is accidentally shared.

**Not completing authenticator app setup before a login is required.** If your administrator has enforced 2FA with the authenticator app option, you must complete the QR code setup on My Profile before your next login that requires 2FA. If you skip this step, you may find yourself unable to complete login. Complete the setup while you still have password access, not after you are locked out.

---

# 11. Related Articles

- RC-CC-03 — Control Center: Security & Authentication Configuration
- RC-CC-07 — Control Center: Users & Access Management
- RC-USER-01 — User Rights: Overview & Three-Tier Access
- RC-API-01 — REDCap API
