---
id: RC-CC-03
title: 'Control Center: Security & Authentication Configuration'
domain: Control Center (Admin)
applies_to:
- REDCap administrators
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — security
  and authentication behaviour checked against source code; Security & Authentication
  labels checked live on v17.5.6 (read-only)
prerequisites:
- REDCap administrator access
version: '1.5'
last_updated: 2026-11
related:
- id: RC-INST-01
  title: Institution-Specific Settings & Policies — Production
- id: RC-USER-02
  title: 'User Rights: Adding Users & Managing Roles'
- id: RC-USER-04
  title: 'User Rights: User Management'
tags:
- control center (admin)
synonyms:
- control center authentication settings
- configure two-factor authentication for redcap
- set up single sign on shibboleth or saml
- table-based authentication login settings
- google oauth2 or microsoft entra id login
- control center login security policies
- how do users authenticate to redcap
- system-wide authentication method configuration
---

# 1. Overview

The Security & Authentication Configuration page in the Control Center is where REDCap administrators control how users authenticate to the system and what security policies govern login behavior. Settings here are system-wide and apply to all users unless otherwise noted.

This page is organized into the following sections:
- Authentication Settings (system-level)
- Two-Factor Authentication
- Login Settings
- Table-based Authentication Settings
- Provider-specific settings (Google OAuth2, Microsoft Entra ID, OpenID Connect, Shibboleth, AAF, SAMS)
- Other Security Settings

Some related controls live on other pages: automatic suspension of inactive users is on User Settings ([RC-CC-04 — Control Center: User Settings & Defaults](RC-CC-04_Control-Center-User-Settings.md)); the rate limiter that bans IP addresses is on General Configuration ([RC-CC-02 — Control Center: General System Configuration](RC-CC-02_Control-Center-General-Configuration.md)), and the banned IP list is under Users & Access Management ([RC-CC-07 — Control Center: Users & Access Management](RC-CC-07_Control-Center-User-Management.md)); the option to show the announcement on the login page is on the Home Page settings ([RC-CC-08 — Control Center: Home Page, Templates & Project Defaults](RC-CC-08_Control-Center-Home-Page-Templates-and-Defaults.md)).

## 1.1 Defaults on a New Installation

| Setting | Default |
| --- | --- |
| Auto logout time | 30 minutes |
| Failed login lockout | 5 failed attempts / 15 minutes |
| Password minimum length | 9 characters |
| Password complexity | Level 1 |
| Two-Factor Authentication | Disabled. When turned on, the **Email** and **Authenticator app** options are enabled; **Duo** and **Twilio** are off |
| 2FA trust period | 0 days (no device trust) |
| Clickjacking prevention | Off (external websites may embed REDCap pages) |
| CORS domain allowlist | Blank (any domain) |

An instance that was set up or changed earlier keeps its stored values, so check yours on this page.

---

# 2. Authentication Settings (System-level)

## 2.1 Authentication Method

Controls how all users authenticate to REDCap system-wide. This also determines the default authentication method for newly created projects.

| Option | Description |
| --- | --- |
| **None (Public)** | No login at all — every visitor is treated as the single `site_admin` account, which is an administrator account. Only suitable for a private test instance |
| **Table-based** | Username/password stored in REDCap's own user table |
| **LDAP** | Authenticate against an LDAP directory server |
| **LDAP & Table-based** | REDCap tries the Table-based account first, then LDAP. An LDAP login whose username matches an existing Table-based user is refused, so keep the two sets of usernames distinct |
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

> **Version caveat (17.3.x LTS and 16.0.x LTS):** The Entra ID options are labelled **Microsoft Entra ID (formerly Azure AD)** rather than **Microsoft Entra ID**. If you are following this article on an LTS instance, look for that longer label; the settings are the same.

> For detailed configuration and installation instructions for each method, refer to the REDCap Community website's authentication documentation.

REDCap also includes an LDAP troubleshooting page for testing the connection to your LDAP server.

---

# 3. Two-Factor Authentication

Two-factor authentication (2FA), also called 2-step login, adds a verification step after the initial username/password login. Users receive or generate a 6-digit code (or use a push notification with Duo) to complete sign-in.

A code that REDCap sends (by email or SMS) is valid for about **2 minutes** by default. Entering and requesting codes has its own limits, separate from the failed-login lockout in §4.4: a user who enters codes too fast, or asks for too many codes in a short time, is made to wait before trying again.

## 3.1 Enable/Disable 2FA

| Setting | Values |
| --- | --- |
| Two-Factor Authentication | Disabled (default) / Enabled |

When enabled, all applicable users must complete the second step every time they log in (subject to the settings below).

**Project-level exceptions.** Two per-project settings are set by an administrator in **Control Center → Edit a Project's Settings**: one exempts a project from 2FA, the other forces 2FA for it. Force 2FA prompts for the second step even on a device the user has marked as trusted (§3.4).

**API requests are not covered.** A request that uses an API token is not subject to 2FA, the failed-login lockout or the 2FA IP exceptions. Protect API tokens accordingly — see [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md).

> **Version caveat (below 17.5.1 Standard / 17.3.14 LTS / 16.0.52 LTS):** New authenticator-app (TOTP) secrets were generated with a **non-cryptographic random source**, making them more predictable than intended — a major security fix, present in all earlier versions. The fix changes how secrets are generated from then on; it does not replace secrets that already exist.

> **Recommendation — regenerate existing authenticator secrets after upgrading.** Every authenticator-app secret created before the fix was generated by the weak method and stays in use until it is replaced. After upgrading to 17.5.1 Standard / 17.3.14 LTS / 16.0.52 LTS or later:
>
> REDCap has **no built-in way** to reset or regenerate an existing authenticator-app secret — there is no Control Center or My Profile button for it in 17.6.5 Standard, 17.3.31 LTS or 16.0.61 LTS. REDCap only generates a secret for a user who has none. Regenerating therefore requires your REDCap server administrator to clear the user's stored authenticator secret directly in the database; REDCap then generates a new one, using the fixed method, the next time the user reaches authenticator setup.
>
> 1. Raise the plan with the REDCap Community before doing it in bulk, since it is a direct database change rather than a supported REDCap action.
> 2. Send users notice first — once their secret is cleared, the old REDCap entry in their authenticator app stops working until they re-enrol.
> 3. Test on one account first: after the database change, confirm that the account gets a **new** secret (the QR code and the code sequence change).
> 4. Then clear the secrets of enrolled users, starting with administrator accounts and accounts with access to sensitive projects.
> 5. Have each user scan the new QR code on **My Profile** and remove the old REDCap entry from their authenticator app — see [RC-PROF-01 — My Profile: User Profile Settings](RC-PROF-01_My-Profile-User-Profile-Settings.md) §8.1.
>
> REDCap's changelog does not itself call for regeneration. This recommendation follows from the fix: a secret is only as strong as the method that produced it.

## 3.2 Enforce Only for Table-based Users

Only use this with an "X & Table-based" hybrid authentication method.

| Setting | Values |
| --- | --- |
| Enforce 2FA ONLY for Table-based users? | No, enforce on all users (default) / Yes, enforce only on Table-based users |

Under a hybrid method, "Yes" exempts users authenticating via the external provider (e.g., Shibboleth, Entra ID) from all 2FA requirements, while Table-based users still complete 2FA.

> **Critical — leave this on "No" unless you use an "X & Table-based" method.** Under a non-hybrid method (LDAP, Shibboleth, OpenID Connect, Microsoft Entra ID, Google OAuth2 and so on), setting it to "Yes" **turns 2FA off for every user**, because nobody logs in as a Table-based user. REDCap's own help text says the setting is ignored outside hybrid methods; that is wrong. If you are on a non-hybrid method and 2FA seems not to be prompting anyone, check this setting first.

## 3.3 IP Address-based Enforcement

Allows scoping 2FA enforcement by IP range — useful for exempting users on a trusted institutional network or VPN.

| Setting | Values |
| --- | --- |
| Enforce 2FA only for certain IP addresses? | Enforce on all users (default) / Enforce on all users EXCEPT those in a specified range |

When the exception option is selected, you enter IPv4 ranges (wildcard, hyphenated or CIDR notation) or IPv6 subnet masks, comma-separated. There is also a checkbox to automatically include all private network IP ranges in the exceptions; it covers the three standard private IPv4 ranges (10.0.0.0/8, 172.16.0.0/12 and 192.168.0.0/16).

Example format: `1.2.3.*, 1.2.3.0-1.2.3.255, 1.2.3.0/24, 21DA:00D3:0000:2F3B::/64`

> **Version caveat (17.x Standard and 17.3.x LTS) — "Trust the X-Forwarded-For header":** 17.x adds a **Trust the X-Forwarded-For header** setting, default **No**. With it on No, REDCap uses the address of whatever connects to it directly. If REDCap sits behind a load balancer or reverse proxy, that is the load balancer's address, not the user's. If that address is private and the private-ranges checkbox is ticked, **every user skips 2FA**. Before relying on IP exceptions, check which IP address REDCap records for your own logins (in Logging or the login history); if it is the load balancer's, work with your server team on the proxy setup before using IP exceptions.

## 3.4 Device Trust Period (Authentication Interval)

If enabled, users who complete 2FA can opt to have their device remembered for a specified number of days, after which they must complete 2FA again.

| Setting | Values |
| --- | --- |
| Trust period | Number of days (0 = Disabled, the default; decimals allowed for partial days) |

Trust is stored per browser, not per account: a different browser on the same computer needs 2FA again, and anyone else who logs in on that same trusted browser also skips the second step. Avoid enabling device trust where users share computers. Projects with "force 2FA" set (§3.1) prompt for 2FA even on a trusted device.

## 3.5 Secondary Authentication Interval for Specific IP Ranges

An optional alternative trust period that applies to users within specified IP ranges. This allows different trust durations for different network contexts (e.g., 30 days on a semi-secure network, 1 day for other networks).

- Enter the number of days and the IP ranges to which that interval applies.
- If set to 0, the feature is disabled.

## 3.6 E-Signature with 2FA PIN

Allows users to substitute their 2FA PIN (or Duo push) for their password when performing an e-signature on data entry forms or when using the File Upload field enhancement. This is also how users of an SSO method (who have no REDCap password) can e-sign.

| Setting | Values |
| --- | --- |
| Allow e-signing with 2FA PIN or Duo push | Disabled (default) / Enabled |

This is commonly used for 21 CFR Part 11 compliance in FDA-regulated trials. On 17.x the setting is labeled for both the 2FA PIN and Duo push, so Duo users can e-sign this way too; see the version notes in §3.8. REDCap's help text on 17.x still says the PIN cannot be used with Duo; the setting label is the accurate one.

> **Version caveat (16.0.x LTS):** E-signing with a Duo push is not available; the setting covers the 6-digit 2FA PIN only. Users who rely on Duo must use one of the code-based 2FA options (email, authenticator app or SMS) to e-sign, or upgrade to 17.x.

### 3.6.1 E-Sign Once Per Session

When the setting above is enabled, this allows users to provide their 2FA PIN only once per REDCap session rather than for every e-signature action.

| Setting | Values |
| --- | --- |
| E-sign once per session | Disabled (default) / Enabled |

This system-wide choice can be overridden for an individual project, so check the project's own setting before assuming the system value applies.

## 3.7 Two-Factor Login Options

These settings control which verification methods are available to users when 2FA is enabled. Multiple options can be enabled simultaneously; users choose their preferred method.

### 3.7.1 Google/Microsoft Authenticator App

Users generate a 6-digit TOTP code from the Google Authenticator or Microsoft Authenticator app on their mobile device. Users must set up the app using a QR code on their REDCap Profile page before using this option.

| Setting | Default |
| --- | --- |
| Authenticator App | Enabled (default in all supported versions) |

### 3.7.2 Email

A 6-digit code is sent to the user's primary email address registered in their REDCap account. Enabled by default; recommended to leave enabled as a fallback option.

| Setting | Notes |
| --- | --- |
| Email option | The code originates from the configured administrator email address |

### 3.7.3 Twilio SMS

Uses the Twilio third-party service to send a 6-digit code via SMS to the user's registered mobile number. Requires a funded Twilio account with a purchased phone number. Off by default.

**Required Twilio configuration fields:**
- Twilio Account SID
- Twilio Auth Token
- Twilio phone number (digits only)
- Alternate Twilio phone number for Voice Call verification (optional — if omitted, the primary number handles both SMS and Voice Call)

The REDCap server must have outbound HTTP/HTTPS access to `https://api.twilio.com`. A "Test Twilio credentials" button verifies credentials before saving.

### 3.7.4 Duo

Uses the Duo Security service for push notification or app-based verification. Requires a Duo account and a configured Web SDK application. Off by default.

**Required Duo configuration fields:**
- Duo Integration Key
- Duo Secret Key
- Duo API Hostname

> Note: The e-signature settings in sections 3.6 and 3.6.1 cover Duo push as well as the PIN on 17.x (not on 16.0.x LTS). The once-per-session behaviour for Duo push arrived in 16.1.2 (§3.8).

---

## 3.8 E-Signature with 2FA — Version Notes

| Change | Version |
| --- | --- |
| Users can supply the **6-digit PIN only once per session** when e-signing, rather than for every signature | 15.4.0 |
| The **Duo push** equivalent of the same behaviour | 16.1.2 |
| Wording of the E-signature dialog corrected under "X & Table-based" 2FA, excluding "LDAP & Table-based" | 15.2.6 |

---

# 3a. Provider-Specific Notes

| Change | Version |
| --- | --- |
| **OIDC scopes** can be specified manually by administrators; earlier versions used a fixed set | 15.4.2 |
| **OpenID Connect** authentication errors produce a more specific, actionable message rather than a generic failure | 15.7.0 |
| Custom button text for the **"Local REDCap Login"** button under "OpenID Connect & Table-based" and "Entra ID & Table-based" | 16.1.2 |
| **Duo** two-factor library updated to its then-current version | 15.9.2 |

> **Note (15.7.2):** With Table-based or "X & Table-based" authentication, REDCap warns the user if **Caps Lock is on** while they type their password. A small change, but it removes one of the more common causes of repeated failed logins — and repeated failures trigger the lockout described in §4.4.

---

# 4. Login Settings

These settings apply to all authentication methods except Shibboleth (which manages its own session behavior). The failed-login lockout (§4.4) applies only to Table-based and LDAP logins.

## 4.1 Auto Logout Time

Controls how long a user can be inactive before REDCap automatically logs them out.

| Setting | Values |
| --- | --- |
| Auto logout time | Number of minutes (default 30; the page accepts 3 to 1440). **0 or blank does not disable auto logout** — REDCap treats it as 24 hours |

Users receive a two-minute warning dialog before being logged out. The idle timeout is enforced by the server, not only by the browser, so closing the warning dialog or leaving a tab open does not extend the session.

Table-based and LDAP sessions also have a fixed maximum of 24 hours, however active the user is. The session cookie ends when the browser is closed, so users log in again after restarting their browser.

## 4.2 Login Logo

An optional custom logo displayed on the REDCap login page. Enter the full URL of the image (maximum display width: 750 pixels).

## 4.3 Custom Login Text

A rich text field for custom content displayed on the login page, appearing above the login form (and below the login logo, if used). Supports the REDCap rich text editor.

To show the system announcement on the login page as well, see [RC-CC-08 — Control Center: Home Page, Templates & Project Defaults](RC-CC-08_Control-Center-Home-Page-Templates-and-Defaults.md).

## 4.4 Failed Login Lockout

Two settings work together to lock out users after repeated failed login attempts:

| Setting | Values |
| --- | --- |
| Failed login attempt limit | Number of failures before lockout (default 5; 0 = disabled) |
| Lockout duration | Minutes (default 15; 0 = disabled) |

How the lockout works:

- **Sliding window.** REDCap counts failed attempts within the last N minutes, where N is the lockout-duration value — the same field is also the counting window. A user is blocked while the number of failures in that window is at or over the limit. Because older failures drop out of the window, a block can lift sooner than N minutes after it starts.
- **What resets the count.** Failures before the user's last successful login, or before an administrator resets their password, are not counted.
- **Which logins.** Only Table-based and LDAP logins are subject to the lockout. SSO methods (Shibboleth, OpenID Connect, Entra ID, Google OAuth2, AAF and so on) rely on the identity provider's own lockout.
- **2FA codes** have their own limits (§3), separate from this lockout.

> **Version caveat (17.x Standard and 17.3.x LTS vs 16.0.x LTS):** On 17.x a locked-out user sees the ordinary failed-login message, so the lockout is not disclosed and the user may believe they are mistyping their password. On 16.0.x LTS the user sees an explicit "locked out for N minutes" message. Support staff on 17.x should check the user's recent failed logins in Logging, and the lockout settings above, before assuming a wrong password.

The IP-based rate limiter, which bans an address after too many page requests, is a separate control on General Configuration — see [RC-CC-02 — Control Center: General System Configuration](RC-CC-02_Control-Center-General-Configuration.md).

## 4.5 Login Page Autocomplete

Controls whether users' browsers are allowed to autofill the username and password fields on the REDCap login page.

| Setting | Notes |
| --- | --- |
| Allow autocomplete (default) | Browsers may suggest saved credentials |
| Disable autocomplete | Asks the browser not to autofill — useful on shared/public computers |

Disabling autocomplete is only a hint to the browser. Many browsers and password managers ignore it, so do not rely on it as a security control.

---

# 5. Table-based Authentication Settings

These settings apply only when Table-based authentication is in use (either exclusively or as part of a hybrid method).

## 5.1 Password Recovery Custom Text

Custom text included in the password-recovery email sent to a user whose account cannot be reset in REDCap. Useful in hybrid environments to redirect external users to their institution's own password reset process.

The email goes only to an existing account that is **not** Table-based and has an email address on file. A username that does not exist gets no email. Whatever was entered, the screen shows the same generic message, so the page does not reveal whether a username exists.

If left blank, the email contains the default message: *"The password for the user XXXXXX cannot be reset in REDCap because it can only be reset using an outside authentication resource at your institution."*

## 5.2 Password Reuse Limit

| Setting | Values |
| --- | --- |
| Enforce password re-use limit | No (default) / Yes |

When enabled, users may not reuse any of their last 5 passwords, counting the current one.

## 5.3 Password Expiration

| Setting | Values |
| --- | --- |
| Force password change after X days | Number of days (0 = disabled) |

Users are warned 7 days before their password expires. Expiry is checked when the user logs in, so an expired password is caught at the next login rather than mid-session.

## 5.4 Password Minimum Length

| Setting | Values |
| --- | --- |
| Minimum length | Integer between 6 and 99 (default: 9) |

## 5.5 Password Complexity

| Level | Requirement |
| --- | --- |
| 0 | Letters and numbers |
| 1 | Lowercase + uppercase letters + numbers (default) |
| 2 | Lowercase + uppercase letters + either numbers or special characters |
| 3 | Lowercase + uppercase letters + numbers + special characters |

Allowed special characters: `!@#$%^&*()/_+|~=’,-*+:";?.` (excluding `><\`)

The apostrophe in that list is the curly ’ character, not the straight ' that most keyboards type.

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
| --- | --- |
| API Client ID | Application (client) ID from Azure App Registration |
| API Client Secret | Client secret from Azure App Registration |
| Endpoint Version | V1 (default) or V2 — V2 supports multi-tenant authentication |
| Tenant | GUID of your tenant; leave blank or use `common` for default |
| AD attribute for username | `userPrincipalName` (default), `onPremisesSamAccountName`, `mail`, or `employeeId` |
| Primary Admin | First-time login grants full admin privileges |
| Secondary Admin | Backup admin; same privilege grant on first login |
| Entra ID button text | Custom label for the Entra ID button on the login page (default: "Microsoft Entra ID") |
| Local REDCap Login button text | Custom label for the Table-based login button (default: "Local REDCap Login") |

> **Version caveat (16.0.x LTS):** There is no **Local REDCap Login button text** field; the Table-based button uses REDCap's built-in wording. Nothing to configure — just expect the field to be missing. On 17.3.x and 16.0.x LTS the Entra ID authentication option is labelled **Microsoft Entra ID (formerly Azure AD)** (§2.1).

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
| --- | --- |
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

> **Version caveat (16.0.x LTS):** There is no **Local REDCap Login button text** field; the Table-based button uses REDCap's built-in wording. Nothing to configure — just expect the field to be missing.

If the selected username attribute has no value for a user, REDCap falls back to the user's email address as their username.

---

# 9. Shibboleth Authentication Settings

Required when authentication method is set to **Shibboleth** or **Shibboleth & Table-based**. Full configuration documentation is available in REDCap's built-in Shibboleth help.

## 9.1 Core Shibboleth Settings

| Field | Notes |
| --- | --- |
| Shibboleth Username Login Field | The server variable containing the username (e.g., `REMOTE_USER`, `HTTP_REMOTE_USER`, `HTTP_AUTH_USER`, `HTTP_SHIB_EDUPERSON_PRINCIPAL_NAME`, `Shib-EduPerson-Principal-Name`, or a custom value) |
| URL for Shibboleth Logout Page | Full URL with qualifiers for the IdP logout endpoint |

## 9.2 Shibboleth User Information Settings

Controls whether REDCap auto-populates user profile fields (name, email) from Shibboleth attributes on login.

| Setting | Values |
| --- | --- |
| Set user information using Shibboleth | Disabled (default) / Enabled |
| Set user information on each login | No (default) / Yes — if Yes, overrides stored values on every login |
| Shibboleth User First Name Field | Server variable name (default: `givenName`) |
| Shibboleth User Last Name Field | Server variable name (default: `sn`) |
| Shibboleth User Email Field | Server variable name (default: `mail`) |

## 9.3 Shibboleth & Table Splash Page Customization

When using Shibboleth & Table-based authentication, a splash/landing page lets users choose their login method.

| Setting | Notes |
| --- | --- |
| Default login method | Table-based (default) or a configured Shibboleth IdP |
| Table login selection title | Clickable text for Table-based login (default: "Use local REDCap login") |

### 9.3.1 Shibboleth Login Options (per IdP)

Multiple Identity Providers can be configured. Each IdP entry includes:

| Field | Notes |
| --- | --- |
| Shibboleth login selection title | Clickable text for this IdP's login option |
| Shibboleth login descriptive text | Descriptive text displayed with the login option |
| Shibboleth Link Image URL | URL of an image to display for this IdP's login link |
| URL for Shibboleth SP Session Initiator | If blank, defaults to the Shibboleth handler provided by the web server |

Additional IdPs can be added or removed dynamically on the configuration page.

---

# 10. Australian Access Federation (AAF) Authentication Settings

Required when authentication method is set to **AAF** or **AAF & Table-based**. AAF uses RapidConnect for federated authentication. See the REDCap Community for the AAF RapidConnect setup guide.

| Field | Notes |
| --- | --- |
| Access URL (required) | URL provided by AAF when registering your service |
| Audience URL (required) | URL users are redirected to after authentication (typically the REDCap base URL) |
| Issuer URL (required) | `https://rapid.test.aaf.edu.au` (test) or `https://rapid.aaf.edu.au` (production) |
| Local identifier | `eduPersonScopedAffiliation` values identifying local users (one per line; e.g., `staff@university.edu.au`) |
| Allow locals to create/copy projects | No (default) / Yes — overrides the default User Settings value for new users |
| Display users on 'Email Users' page | None (default) / Locals only / All users |
| AAF attribute for username | `cn` (shown first), `mail`, `displayname`, `edupersontargetedid`, or `edupersonprincipalname` |

> **Attribute note:** `mail` is most commonly used as a username. `eduPersonTargetedID` is recommended by AAF for uniqueness (it never changes) but is a long non-human-readable string. `cn` and `displayname` are discouraged due to potential name collisions.

> **Important — saving this page can change how AAF usernames are formed.** Until the Security & Authentication page is saved for the first time, REDCap uses the user's email address as the AAF username. The dropdown has no blank option, so the first save stores whatever it shows — `cn` unless you change it. Saving the page for any reason (for example, to change the auto logout time) can therefore switch new AAF users from email-based to `cn`-based usernames. Check this setting every time before you save the page.

---

# 11. SAMS Authentication Settings (CDC)

Required when authentication method is set to **SAMS (for CDC)**.

| Field | Notes |
| --- | --- |
| URL for SAMS Logout Page | Full URL with qualifiers for the SAMS logout endpoint |

---

# 12. Other Security Settings

## 12.1 Domain Allowlist for Cross-Domain HTTP Access Control (CORS)

By default, AJAX requests (via JavaScript) can be made to REDCap from any domain. To restrict cross-domain access to specific trusted sites, enter their origins one per line.

- Leave blank to allow cross-domain AJAX from any domain (default).
- Each entry must match the requesting site's origin exactly, including the scheme: `https://example.com` does not match `http://example.com` or `https://www.example.com`.
- REDCap's own address is added automatically; you do not need to list it.
- Restricting to specific domains reduces exposure to Cross-Site Scripting (XSS) attacks.

**Format example:**
```
https://example.com
https://www.yoursite.edu
```

## 12.2 Clickjacking Prevention

Controls whether REDCap pages can be embedded inside `<iframe>` elements on external websites.

| Setting | Technical Effect |
| --- | --- |
| Allow external websites to embed REDCap pages (default) | No HTTP header restriction added |
| Prevent clickjacking / prevent external websites from embedding REDCap | Adds `X-Frame-Options: SAMEORIGIN` HTTP header |

A new 17.5.6 installation starts on **Allow external websites to embed REDCap pages**, so protection is **off** until an administrator turns it on. An instance that was set up or changed earlier keeps its stored value, so check yours on this page. The "Prevent" option allows REDCap pages to be embedded only within the same domain, preventing malicious actors from overlaying REDCap pages on external sites to trick users into unintended clicks. The password recovery page always sends `X-Frame-Options: SAMEORIGIN`, whatever this setting says.

> Note: Turning on clickjacking prevention may affect legitimate use cases such as embedding surveys in external websites. Evaluate this trade-off based on your institution's security requirements.

## 12.3 Security Headers Set by REDCap

Several HTTP security headers are applied by REDCap itself rather than configured on this page. They are listed here because they are frequently investigated alongside the settings above.

| Header | Behaviour | Introduced |
| --- | --- | --- |
| **Content-Security-Policy (CSP)** | REDCap sets a CSP header meeting minimum security requirements while remaining permissive enough not to break External Modules and legacy code in REDCap's own codebase. The 17.6 default is stricter than 17.3.x and 16.0.x LTS: it adds rules for images, workers, the base URI and web app manifests, and blocks mixed (HTTP-on-HTTPS) content | 15.5.1 |
| **Strict-Transport-Security (HSTS)** | Sent on HTTPS only, for one year, with the `includeSubDomains` attribute | 15.4.5 |
| **X-Content-Type-Options** | Always `nosniff` | — |
| **Referrer-Policy** | Always sent | — |
| **Permissions-Policy** | Always sent | — |

If an External Module or embedded content worked on 17.3 but breaks after moving to 17.6, check the browser console for CSP violations before treating it as a module fault.

> **Important — a server-level CSP does not replace REDCap's.** REDCap only notices a Content-Security-Policy that has already been set within REDCap itself (for example by an External Module). A CSP added by Apache, nginx or a reverse proxy is sent **in addition to** REDCap's, and the browser enforces both. A stricter server policy therefore tightens things (and can break External Modules in ways that look like module faults), but a looser server policy does **not** loosen REDCap's — content must satisfy both.

> **Version caveat (16.0.x LTS):** Any CSP header set within REDCap, including a `Content-Security-Policy-Report-Only` header, makes REDCap skip its own CSP entirely. If an External Module sends a report-only policy on 16.0.x, those pages have no enforced REDCap CSP. Check the response headers on affected pages, or upgrade to 17.x.

## 12.4 Session Cookie Name

From REDCap **15.7.0** the authenticated user session cookie is no longer named `PHPSESSID`. REDCap generates an installation-specific name.

This was introduced to allow a user to hold sessions in **multiple REDCap installations on the same server and domain simultaneously**. On earlier versions the shared cookie name meant logging into a second installation silently destroyed the session in the first — a recurring annoyance for anyone running production and test on one host.

> **Version caveat (upgrading across 15.7.0):** Anything that references the session cookie by name — load balancer session affinity, an SSO or reverse-proxy integration, a monitoring probe — must be updated. The failure mode is users being logged out unpredictably or bounced between application servers, which does not obviously implicate a cookie name.

---

# 13. Saving Settings

All changes on this page take effect after clicking **Save Changes** at the bottom of the form. There is a single save action for the entire page — partial saves are not supported. Because every field is saved together, check the AAF username attribute (§10) before saving if you use AAF.

---

# 14. Frequently Asked Questions

**Q: Can I use two-factor authentication with Shibboleth?**
A: Yes. When using Shibboleth & Table-based authentication, you can optionally enforce 2FA only on Table-based users using the setting in section 3.2, which leaves Shibboleth-authenticated users exempt. With plain Shibboleth (no Table-based option), leave that setting on "No" — "Yes" turns 2FA off for everyone.

**Q: What happens if a user gets locked out after failed login attempts?**
A: The user cannot log in until enough failed attempts fall outside the lockout window (section 4.4). There is no "unlock account" button. Failed attempts before the user's last successful login, or before an administrator resets their password, are not counted — so for a Table-based user, resetting their password clears the lockout. LDAP users must wait until the lockout window passes.

**Q: Which 2FA option should we use if we have no Twilio or Duo account?**
A: The Email option (section 3.7.2) requires no third-party service and is recommended as a minimum baseline. The Google/Microsoft Authenticator option (section 3.7.1) is also free and does not require REDCap to send anything externally — it is generally the most reliable option.

**Q: What does "Trust a device for X days" mean exactly?**
A: After completing 2FA, the user is given the option to mark their browser as trusted. During the trust period, they only need to enter their username and password — the second factor is skipped. After the trust period expires, they must complete 2FA again. Trust belongs to the browser, not the account (section 3.4).

**Q: Does clickjacking prevention affect survey embedding?**
A: Yes. If you embed REDCap public surveys in external websites using iframes, the "Prevent clickjacking" option will block that embedding. Embedding needs "Allow external websites to embed REDCap pages", which is the install default on 17.5.6.

**Q: What is the difference between OpenID Connect "username" and "preferred_username" attributes?**
A: Both map to OIDC standard claims, but `preferred_username` is the human-readable login name as preferred by the user, while `username` is the canonical account identifier. The correct choice depends on what your OIDC provider populates. If the selected attribute is empty for a user, REDCap falls back to the user's email address.

**Q: Do 2FA and the login lockout apply to the API?**
A: No. Requests made with an API token skip 2FA, the failed-login lockout and the 2FA IP exceptions (section 3.1).

---

# 15. Common Questions

**Q: Should I enable two-factor authentication for all users or just certain groups?**
Enabling 2FA for all users provides the strongest security but may reduce usability, especially for less technical users. A common approach is to enable 2FA for all users but use IP-based exceptions (section 3.3) to exempt users on trusted institutional networks or VPNs — after confirming that REDCap records users' real IP addresses rather than a load balancer's. For external users or those accessing from public networks, 2FA should always be enforced.

**Q: What is the best two-factor authentication method to use?**
The Google/Microsoft Authenticator app (section 3.7.1) is the most reliable because it does not require outbound communication from REDCap — the user generates the code locally. Email (3.7.2) is a good fallback and requires no third-party service. Twilio SMS (3.7.3) and Duo (3.7.4) both require paid accounts and third-party services but offer additional flexibility (SMS and push notifications). Ideally, enable multiple options and let users choose their preferred method.

**Q: How do I prevent users from bypassing the auto logout setting?**
The auto logout time setting (section 4.1) is enforced by the server after the specified period of inactivity. Users are notified before being logged out and must re-authenticate. The setting cannot be bypassed — if you set it to 30 minutes, users will be logged out after 30 minutes of inactivity regardless of whether they object. Do not enter 0 expecting to switch it off: 0 or blank means 24 hours. Very short timeout periods (less than 10 minutes) can negatively impact usability for long data entry sessions.

**Q: What password complexity level should we require?**
Complexity level 1 (lowercase + uppercase + numbers, default) is a good balance between security and usability. Level 3 (lowercase + uppercase + numbers + special characters) is more secure but increases the likelihood of users writing passwords down or forgetting them. Level 0 is not recommended for production systems handling sensitive data. Combine your complexity choice with a reasonable minimum length (at least 9 characters) and, if appropriate, password expiration (section 5.3).

**Q: Can we use both Shibboleth and Table-based authentication at the same time?**
Yes. The "Shibboleth & Table-based" option (section 2.1) presents a splash page where users choose their authentication method. Table-based users can continue using local accounts while Shibboleth users authenticate via your institutional IdP. This is useful during a migration from local to federated authentication or when supporting both internal and external users.

---

# 16. Common Mistakes & Gotchas

**Enabling complex password policies without testing ease of use.** Very strict password complexity requirements (level 3 + long minimum length) can create user frustration and lead to passwords being written down or stored insecurely. Pilot any new password policy with a subset of users first to gauge impact and identify training needs.

**Misconfiguring the OAuth2 redirect URI or OIDC metadata endpoint.** A common issue with Google OAuth2 and OIDC configurations is entering the wrong redirect URL or metadata endpoint. Google must have the exact REDCap base URL in its Authorized Redirect URIs, and the OIDC metadata endpoint must point to the correct `.well-known/openid-configuration` path. Double-check these values and test login before rolling out to production users.

**Assuming clickjacking prevention is on by default.** On a new 17.5.6 installation it is off (section 12.2): the default allows external websites to embed REDCap pages. If nothing needs to be embedded, choose the "Prevent" option, which adds the `X-Frame-Options: SAMEORIGIN` HTTP header. If surveys must be embedded in iframes on external websites, leave embedding allowed deliberately, knowing that this leaves pages without clickjacking protection.

**Setting "Enforce 2FA ONLY for Table-based users?" to Yes under a non-hybrid method.** Under LDAP, Shibboleth, OpenID Connect, Entra ID and other non-hybrid methods this turns 2FA off for all users, despite REDCap's help text saying it is ignored (section 3.2).

**Using IP exceptions behind a load balancer.** On 17.x with **Trust the X-Forwarded-For header** set to No, REDCap sees the load balancer's address. If that address is private and private ranges are exempt, nobody is asked for 2FA (section 3.3).

**Saving the page on an AAF instance without checking the username attribute.** The first save can switch new AAF usernames from email to `cn` (section 10).

**Expecting a server-level CSP to loosen REDCap's.** Both policies are enforced; content must satisfy both (section 12.3).

---

# 17. Related Articles

- [RC-CC-02 — Control Center: General System Configuration](RC-CC-02_Control-Center-General-Configuration.md) (rate limiter and automatic IP banning)
- [RC-CC-04 — Control Center: User Settings & Defaults](RC-CC-04_Control-Center-User-Settings.md) (user creation, account defaults and automatic suspension of inactive users)
- [RC-CC-07 — Control Center: Users & Access Management](RC-CC-07_Control-Center-User-Management.md) (user account management, suspension and the banned IP list)
- [RC-CC-08 — Control Center: Home Page, Templates & Project Defaults](RC-CC-08_Control-Center-Home-Page-Templates-and-Defaults.md) (showing the announcement on the login page)
- [RC-USER-02 — User Rights: Adding Users & Managing Roles](RC-USER-02_User-Rights-Adding-Users-and-Managing-Roles.md) (authentication relationship to project-level permissions)
- [RC-INST-01 — Institution-Specific Settings & Policies — Production](RC-INST-01_Institution-Specific-Settings-and-Policies.md) (institutional security policies and authentication strategy)
