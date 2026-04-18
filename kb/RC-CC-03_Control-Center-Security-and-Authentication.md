RC-CC-03

**Control Center: Security & Authentication Configuration**

| **Article ID** | RC-CC-03 |
|---|---|
| **Domain** | Control Center (Admin) |
| **Applies To** | REDCap administrators |
| **Prerequisite** | REDCap administrator access |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-INST-01 — Institution-Specific Settings & Policies; RC-USER-02 — User Rights; RC-USER-04 — User Management |

---

# 1. Overview

The Security & Authentication Configuration page in the Control Center (`ControlCenter/security_settings.php`) is where REDCap administrators control how users authenticate to the system and what security policies govern login behavior. Settings here are system-wide and apply to all users unless otherwise noted.

This page is organized into the following sections:
- Authentication Settings (system-level)
- Two-Factor Authentication
- Login Settings
- Table-based Authentication Settings
- Provider-specific settings (Google OAuth2, Microsoft Entra ID, OpenID Connect, Shibboleth, AAF, SAMS)
- Other Security Settings

---

# 2. Authentication Settings (System-level)

## 2.1 Authentication Method

Controls how all users authenticate to REDCap system-wide. This also determines the default authentication method for newly created projects.

| Option | Description |
|---|---|
| **None (Public)** | No authentication required — pages are publicly accessible |
| **Table-based** | Username/password stored in REDCap's own user table |
| **LDAP** | Authenticate against an LDAP directory server |
| **LDAP & Table-based** | LDAP primary; Table-based as a fallback or for local accounts |
| **Shibboleth** | Federated identity via Shibboleth SP (see Shibboleth settings below) |
| **Shibboleth & Table-based** | Shibboleth primary with Table-based option on login page |
| **Google OAuth2** | Google account authentication (see Google OAuth2 settings below) |
| **Microsoft Entra ID** | Formerly Azure AD (see Entra ID settings below) |
| **Microsoft Entra ID & Table-based** | Entra ID primary with Table-based option |
| **RSA SecurID** | Hardware/software token two-factor authentication |
| **SAMS (for CDC)** | CDC's Secure Access Management Services |
| **AAF** | Australian Access Federation (RapidConnect) |
| **AAF & Table-based** | AAF primary with Table-based option |
| **OpenID Connect** | Generic OIDC provider (see OpenID Connect settings below) |
| **OpenID Connect & Table-based** | OIDC primary with Table-based option |

> For detailed configuration and installation instructions for each method, refer to the REDCap Community website's authentication documentation.

An LDAP troubleshooting tool is available at `ControlCenter/ldap_troubleshoot.php`.

---

# 3. Two-Factor Authentication

Two-factor authentication (2FA), also called 2-step login, adds a verification step after the initial username/password login. Users receive or generate a 6-digit code (or use a push notification with Duo) to complete sign-in.

## 3.1 Enable/Disable 2FA

| Setting | Values |
|---|---|
| Two-Factor Authentication | Disabled (default) / Enabled |

When enabled, all applicable users must complete the second step every time they log in (subject to the settings below).

## 3.2 Enforce Only for Table-based Users

Only relevant when using an "X & Table-based" hybrid authentication method.

| Setting | Values |
|---|---|
| Enforce 2FA ONLY for Table-based users? | No, enforce on all users (default) / Yes, enforce only on Table-based users |

If set to "Yes", users authenticating via the external provider (e.g., Shibboleth, Entra ID) are exempt from all 2FA requirements.

## 3.3 IP Address-based Enforcement

Allows scoping 2FA enforcement by IP range — useful for exempting users on a trusted institutional network or VPN.

| Setting | Values |
|---|---|
| Enforce 2FA only for certain IP addresses? | Enforce on all users (default) / Enforce on all users EXCEPT those in a specified range |

When the exception option is selected, you enter IPv4 ranges (wildcard or hyphenated) or IPv6 subnet masks, comma-separated. There is also a checkbox to automatically include all private network IP ranges (RFC 1918) in the exceptions.

Example format: `1.2.3.*, 1.2.3.0-1.2.3.255, 21DA:00D3:0000:2F3B::/64`

## 3.4 Device Trust Period (Authentication Interval)

If enabled, users who complete 2FA can opt to have their device remembered for a specified number of days, after which they must complete 2FA again.

| Setting | Values |
|---|---|
| Trust period | Number of days (0 = Disabled; decimals allowed for partial days) |

## 3.5 Secondary Authentication Interval for Specific IP Ranges

An optional alternative trust period that applies to users within specified IP ranges. This allows different trust durations for different network contexts (e.g., 30 days on a semi-secure network, 1 day for other networks).

- Enter the number of days and the IP ranges to which that interval applies.
- If set to 0, the feature is disabled.

## 3.6 E-Signature with 2FA PIN

Allows users to substitute their 2FA PIN (or Duo push) for their password when performing an e-signature on data entry forms or when using the File Upload field enhancement.

| Setting | Values |
|---|---|
| Allow e-signing with 2FA PIN or Duo push | Disabled (default) / Enabled |

This is commonly used for 21 CFR Part 11 compliance in FDA-regulated trials. Note: not compatible with the Duo two-factor option.

### 3.6.1 E-Sign Once Per Session

When the setting above is enabled, this allows users to provide their 2FA PIN only once per REDCap session rather than for every e-signature action.

| Setting | Values |
|---|---|
| E-sign once per session | Disabled (default) / Enabled |

## 3.7 Two-Factor Login Options

These settings control which verification methods are available to users when 2FA is enabled. Multiple options can be enabled simultaneously; users choose their preferred method.

### 3.7.1 Google/Microsoft Authenticator App

Users generate a 6-digit TOTP code from the Google Authenticator or Microsoft Authenticator app on their mobile device. Users must set up the app using a QR code on their REDCap Profile page before using this option.

| Setting | Default |
|---|---|
| Authenticator App | Enabled (default in REDCap 16.x) |

### 3.7.2 Email

A 6-digit code is sent to the user's primary email address registered in their REDCap account. Recommended to leave enabled as a fallback option.

| Setting | Notes |
|---|---|
| Email option | The code originates from the configured administrator email address |

### 3.7.3 Twilio SMS

Uses the Twilio third-party service to send a 6-digit code via SMS to the user's registered mobile number. Requires a funded Twilio account with a purchased phone number.

**Required Twilio configuration fields:**
- Twilio Account SID
- Twilio Auth Token
- Twilio phone number (digits only)
- Alternate Twilio phone number for Voice Call verification (optional — if omitted, the primary number handles both SMS and Voice Call)

The REDCap server must have outbound HTTP/HTTPS access to `https://api.twilio.com`. A "Test Twilio credentials" button verifies credentials before saving.

### 3.7.4 Duo

Uses the Duo Security service for push notification or app-based verification. Requires a Duo account and a configured Web SDK application.

**Required Duo configuration fields:**
- Duo Integration Key
- Duo Secret Key
- Duo API Hostname

> Note: The Duo option is not compatible with the 2FA e-signature PIN feature (sections 3.6 and 3.6.1).

---

# 4. Login Settings

These settings apply to all authentication methods except Shibboleth (which manages its own session behavior).

## 4.1 Auto Logout Time

Controls how long a user can be inactive before REDCap automatically logs them out.

| Setting | Values |
|---|---|
| Auto logout time | Number of minutes (0 = disabled; minimum 3 if non-zero, maximum 1440) |

Users receive a two-minute warning dialog before being logged out.

## 4.2 Login Logo

An optional custom logo displayed on the REDCap login page. Enter the full URL of the image (maximum display width: 750 pixels).

## 4.3 Custom Login Text

A rich text field for custom content displayed on the login page, appearing above the login form (and below the login logo, if used). Supports the REDCap rich text editor.

## 4.4 Failed Login Lockout

Two settings work together to lock out users after repeated failed login attempts:

| Setting | Values |
|---|---|
| Failed login attempt limit | Number of failures before lockout (0 = disabled) |
| Lockout duration | Minutes the user is locked out after exceeding the limit (0 = disabled) |

## 4.5 Login Page Autocomplete

Controls whether users' browsers are allowed to autofill the username and password fields on the REDCap login page.

| Setting | Notes |
|---|---|
| Allow autocomplete (default) | Browsers may suggest saved credentials |
| Disable autocomplete | Improves security, especially for shared/public computers |

---

# 5. Table-based Authentication Settings

These settings apply only when Table-based authentication is in use (either exclusively or as part of a hybrid method).

## 5.1 Password Recovery Custom Text

Custom text included in the email response when a user enters an **invalid username** during password recovery. Useful in hybrid environments to redirect external users to their institution's own password reset process.

If left blank, REDCap displays the default message: *"The password for the user XXXXXX cannot be reset in REDCap because it can only be reset using an outside authentication resource at your institution."*

## 5.2 Password Reuse Limit

| Setting | Values |
|---|---|
| Enforce password re-use limit | No (default) / Yes |

When enabled, users may not reuse any of their 5 most recent passwords.

## 5.3 Password Expiration

| Setting | Values |
|---|---|
| Force password change after X days | Number of days (0 = disabled) |

Users receive advance notice prompting them to change their password before expiration.

## 5.4 Password Minimum Length

| Setting | Values |
|---|---|
| Minimum length | Integer between 6 and 99 (default: 9) |

## 5.5 Password Complexity

| Level | Requirement |
|---|---|
| 0 | Letters and numbers |
| 1 | Lowercase + uppercase letters + numbers (default) |
| 2 | Lowercase + uppercase letters + either numbers or special characters |
| 3 | Lowercase + uppercase letters + numbers + special characters |

Allowed special characters: `!@#$%^&*()/_+|~=',-*+:";?.` (excluding `><\`)

---

# 6. Google OAuth2 Authentication Settings

Required when authentication method is set to **Google OAuth2**.

**Setup overview:**
1. Create a project in the Google Developers Console.
2. Under APIs & auth → Credentials, create a new OAuth Client ID (Web Application type).
3. Add the REDCap base URL to "Authorized Redirect URIs".
4. Copy the generated Client ID and Client Secret into REDCap.

**Configuration fields:**
- Google API Client ID
- Google API Client Secret

---

# 7. Microsoft Entra ID Authentication Settings

Required when authentication method is set to **Microsoft Entra ID** (formerly Azure AD) or **Microsoft Entra ID & Table-based**.

**Configuration fields:**

| Field | Notes |
|---|---|
| API Client ID | Application (client) ID from Azure App Registration |
| API Client Secret | Client secret from Azure App Registration |
| Endpoint Version | V1 (default) or V2 — V2 supports multi-tenant authentication |
| Tenant | GUID of your tenant; leave blank or use `common` for default |
| AD attribute for username | `userPrincipalName` (default), `onPremisesSamAccountName`, `mail`, or `employeeId` |
| Primary Admin | First-time login grants full admin privileges |
| Secondary Admin | Backup admin; same privilege grant on first login |
| Entra ID button text | Custom label for the Entra ID button on the login page (default: "Microsoft Entra ID") |
| Local REDCap Login button text | Custom label for the Table-based login button (default: "Local REDCap Login") |

`userPrincipalName` uses the fully qualified UPN (e.g., `user@domain.com`). `onPremisesSamAccountName` uses the legacy domain username for on-premises-synced accounts.

For V2 endpoints, ensure "Accounts in any organizational directory" is enabled in the Azure portal under Supported account types.

---

# 8. OpenID Connect Authentication Settings

Required when authentication method is set to **OpenID Connect** or **OpenID Connect & Table-based**.

Before configuring, set the following values on the Identity Provider (IdP) server:
- `REDIRECT_URL` = `https://[your-redcap-url]/index.php`
- `POST_LOGOUT_REDIRECT_URI` = `https://[your-redcap-url]/index.php?logout=1`

**Configuration fields:**

| Field | Notes |
|---|---|
| Client ID | Application client ID from the OIDC provider |
| Client Secret | Client secret from the OIDC provider |
| Additional scope (optional) | May be needed for Azure B2C (enter Application client ID) |
| Manual scope override (optional) | Comma-delimited list; overrides REDCap's automatic scope detection |
| Provider Base URL | Base URL of the OIDC provider |
| Provider Metadata Document URL | Typically ends with `/.well-known/openid-configuration` |
| Attribute for REDCap username | `username` (default), `preferred_username`, `email`, `nickname`, or `sub` |
| Response Mode (`response_mode`) | `query` (default) or `form_post` |
| Primary Admin | First-time login grants full admin privileges |
| Secondary Admin | Backup admin; same privilege grant on first login |
| OpenID Connect button text | Custom label for OIDC button on login page (default: "OpenID Connect") |
| Local REDCap Login button text | Custom label for the Table-based login button (default: "Local REDCap Login") |
| Custom Logout Page URL | Full URL for the OIDC provider's logout page (e.g., end-session endpoint) |

If the selected username attribute has no value for a user, REDCap falls back to the user's email address as their username.

---

# 9. Shibboleth Authentication Settings

Required when authentication method is set to **Shibboleth** or **Shibboleth & Table-based**. Full configuration documentation is available in REDCap's built-in Shibboleth help (`Help/shib_table_help.php`).

## 9.1 Core Shibboleth Settings

| Field | Notes |
|---|---|
| Shibboleth Username Login Field | The `$_SERVER` variable containing the username (e.g., `REMOTE_USER`, `HTTP_REMOTE_USER`, `HTTP_AUTH_USER`, `HTTP_SHIB_EDUPERSON_PRINCIPAL_NAME`, `Shib-EduPerson-Principal-Name`, or a custom value) |
| URL for Shibboleth Logout Page | Full URL with qualifiers for the IdP logout endpoint |

## 9.2 Shibboleth User Information Settings

Controls whether REDCap auto-populates user profile fields (name, email) from Shibboleth attributes on login.

| Setting | Values |
|---|---|
| Set user information using Shibboleth | Disabled (default) / Enabled |
| Set user information on each login | No (default) / Yes — if Yes, overrides stored values on every login |
| Shibboleth User First Name Field | `$_SERVER` variable name (default: `givenName`) |
| Shibboleth User Last Name Field | `$_SERVER` variable name (default: `sn`) |
| Shibboleth User Email Field | `$_SERVER` variable name (default: `mail`) |

## 9.3 Shibboleth & Table Splash Page Customization

When using Shibboleth & Table-based authentication, a splash/landing page lets users choose their login method.

| Setting | Notes |
|---|---|
| Default login method | Table-based (default) or a configured Shibboleth IdP |
| Table login selection title | Clickable text for Table-based login (default: "Use local REDCap login") |

### 9.3.1 Shibboleth Login Options (per IdP)

Multiple Identity Providers can be configured. Each IdP entry includes:

| Field | Notes |
|---|---|
| Shibboleth login selection title | Clickable text for this IdP's login option |
| Shibboleth login descriptive text | Descriptive text displayed with the login option |
| Shibboleth Link Image URL | URL of an image to display for this IdP's login link |
| URL for Shibboleth SP Session Initiator | If blank, defaults to `$_SERVER['Shib-Handler']` |

Additional IdPs can be added or removed dynamically on the configuration page.

---

# 10. Australian Access Federation (AAF) Authentication Settings

Required when authentication method is set to **AAF** or **AAF & Table-based**. AAF uses RapidConnect for federated authentication. See the REDCap Community for the AAF RapidConnect setup guide.

| Field | Notes |
|---|---|
| Access URL (required) | URL provided by AAF when registering your service |
| Audience URL (required) | URL users are redirected to after authentication (typically the REDCap base URL) |
| Issuer URL (required) | `https://rapid.test.aaf.edu.au` (test) or `https://rapid.aaf.edu.au` (production) |
| Local identifier | `eduPersonScopedAffiliation` values identifying local users (one per line; e.g., `staff@university.edu.au`) |
| Allow locals to create/copy projects | No (default) / Yes — overrides the default User Settings value for new users |
| Display users on 'Email Users' page | None (default) / Locals only / All users |
| AAF attribute for username | `cn` (default), `mail`, `displayname`, `edupersontargetedid`, or `edupersonprincipalname` |

> **Attribute note:** `mail` is most commonly used as a username. `eduPersonTargetedID` is recommended by AAF for uniqueness (it never changes) but is a long non-human-readable string. `cn` and `displayname` are discouraged due to potential name collisions.

---

# 11. SAMS Authentication Settings (CDC)

Required when authentication method is set to **SAMS (for CDC)**.

| Field | Notes |
|---|---|
| URL for SAMS Logout Page | Full URL with qualifiers for the SAMS logout endpoint |

---

# 12. Other Security Settings

## 12.1 Domain Allowlist for Cross-Domain HTTP Access Control (CORS)

By default, AJAX requests (via JavaScript) can be made to REDCap from any domain. To restrict cross-domain access to specific trusted domains, enter domain names (not full URLs) one per line.

- Leave blank to allow cross-domain AJAX from any domain (default).
- Restricting to specific domains reduces exposure to Cross-Site Scripting (XSS) attacks.

**Format example:**
```
http://example.com
http://www.yoursite.edu
```

## 12.2 Clickjacking Prevention

Controls whether REDCap pages can be embedded inside `<iframe>` elements on external websites.

| Setting | Technical Effect |
|---|---|
| Allow external websites to embed REDCap pages | No HTTP header restriction added |
| Prevent clickjacking (default) | Adds `X-Frame-Options: SAMEORIGIN` HTTP header |

The "Prevent clickjacking" option is selected by default and is the recommended setting. It allows REDCap pages to be embedded only within the same domain, preventing malicious actors from overlaying REDCap pages on external sites to trick users into unintended clicks.

> Note: Enabling clickjacking prevention may affect legitimate use cases such as embedding surveys in external websites. Evaluate this trade-off based on your institution's security requirements.

---

# 13. Saving Settings

All changes on this page take effect after clicking **Save Changes** at the bottom of the form. There is a single save action for the entire page — partial saves are not supported.

---

# 14. Frequently Asked Questions

**Q: Can I use two-factor authentication with Shibboleth?**
A: Yes. When using Shibboleth & Table-based authentication, you can optionally enforce 2FA only on Table-based users using the setting in section 3.2, which leaves Shibboleth-authenticated users exempt.

**Q: What happens if a user gets locked out after failed login attempts?**
A: The user cannot attempt to log in again until the lockout window (section 4.4) expires. Administrators can manually unlock accounts through user management.

**Q: Which 2FA option should we use if we have no Twilio or Duo account?**
A: The Email option (section 3.7.2) requires no third-party service and is recommended as a minimum baseline. The Google/Microsoft Authenticator option (section 3.7.1) is also free and does not require REDCap to send anything externally — it is generally the most reliable option.

**Q: What does "Trust a device for X days" mean exactly?**
A: After completing 2FA, the user is given the option to mark their browser/device as trusted. During the trust period, they only need to enter their username and password — the second factor is skipped. After the trust period expires, they must complete 2FA again.

**Q: Does clickjacking prevention affect survey embedding?**
A: Yes. If you embed REDCap public surveys in external websites using iframes, the "Prevent clickjacking" setting will block that embedding. You would need to set the option to "Allow external websites to embed REDCap pages" to support survey embedding.

**Q: What is the difference between OpenID Connect "username" and "preferred_username" attributes?**
A: Both map to OIDC standard claims, but `preferred_username` is the human-readable login name as preferred by the user, while `username` is the canonical account identifier. The correct choice depends on what your OIDC provider populates. If the selected attribute is empty for a user, REDCap falls back to the user's email address.
