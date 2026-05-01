RC-CC-07

**Control Center: Users & Access Management**

| **Article ID** | RC-CC-07 |
| --- | --- |
| **Domain** | Control Center (Admin) |
| **Applies To** | REDCap administrators |
| **Prerequisite** | REDCap administrator access |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-CC-03 — Security & Authentication; RC-CC-04 — User Settings & Defaults; RC-INST-01 — Institution-Specific Settings & Policies; RC-USER-01 — User Rights: Overview & Three-Tier Access; RC-API-01 — REDCap API |

---

# 1. Overview

The **Users** section of the Control Center gives administrators tools to manage user accounts across the entire REDCap instance. This is distinct from project-level user management (handled within individual projects) — the Users section here is for system-level account administration.

The Users section contains the following tools:

- **Browse Users** — search and view all user accounts; edit account attributes
- **User Allowlist** — restrict system access to pre-approved usernames (for external auth only)
- **Email Users** — send system-level emails to filtered subsets of users
- **API Tokens** — view and manage API tokens across all projects and users
- **Banned IP Addresses** — view and manage IP addresses blocked from the instance
- **Administrator Privileges** — grant or revoke REDCap super user status
- **Access Control Groups** — (institutional configuration dependent)

---

## Browse Users

A searchable list of all user accounts on the REDCap instance. Administrators can look up users by **username, first name, last name, or primary email address**.

### User Account Details

Selecting a user displays their full account record, including:

**Editable user attributes:**

| Attribute | Notes |
| --- | --- |
| Username | The login identifier (typically email for SSO instances) |
| Name | First and last name |
| Primary email | Verified on account creation |
| Secondary email | Optional; also verifiable |
| Tertiary email | Optional |
| Institution ID | Optional institutional identifier |
| User's sponsor | Secondary contact person for the account |
| Allow create/copy projects | Whether this user can create or copy REDCap projects |
| Comments | Administrator notes on the account |
| Account expiration time | Date/time after which login is blocked (blank = no expiration) |
| Display on 'Email Users' page | Whether this user appears as a target in the Email Users tool |
| Clinical Data Mart access | Whether the user can create projects and pull records via Clinical Data Mart integration (if enabled) |

**Statistics & account history (read-only):**

| Field | Notes |
| --- | --- |
| User currently logged in | Live indicator |
| Projects user can access | Count with a link to the full project list |
| Time of account creation | |
| Time of first login | |
| Time of last login | |
| Time of first activity | |
| Time of last activity | |
| Time of suspension | Populated if account is suspended |

### Account Actions

From the Browse Users page, administrators can:

- **Edit user info** — update any of the editable attributes above
- **Suspend/unsuspend** an account
- **Delete** a user from the REDCap system (not available for administrator accounts)
- **Reset password** (for table-based authentication instances)
- **Grant/revoke administrator privileges**

> **Note:** Administrator accounts cannot be deleted through this interface. To remove administrator access, first revoke admin privileges via the Administrator Privileges page, then delete the account if needed.

### View User List By Criteria

In addition to individual user search, administrators can switch to a **View User List By Criteria** mode to filter and browse users in bulk based on attributes or activity.

---

## User Allowlist

The User Allowlist is only relevant when using an **external authentication method** (e.g., LDAP, Shibboleth, or similar SSO). It does not apply to table-based authentication.

### How it works

**When the allowlist is disabled (default):** REDCap authenticates the user via the external provider and immediately grants access. Anyone with a valid credential for that external system can log into REDCap without any prior approval step.

**When the allowlist is enabled:** An externally authenticated user will be blocked from accessing REDCap until an administrator explicitly adds them to the allowlist. Users who attempt to log in but are not yet on the list receive a message informing them that an administrator must add them before they can access REDCap.

> **Note:** REDCap Administrators are always automatically added to the allowlist when it is enabled, regardless of which option is chosen.

### Enabling the Allowlist

When you first enable the allowlist, REDCap presents two initialization options:

| Option | Effect | When to use |
| --- | --- |---|
| **Option 1** — Add all existing users | All users who have previously accessed REDCap (via external auth) are automatically added to the allowlist | Use when you want to preserve access for current users while gatekeeping all new registrations |
| **Option 2** — Leave allowlist empty | No existing users are added (except Administrators) | Use when you want a hard cutover — no one gets access until explicitly added, even if they used REDCap before |

### Adding Users to the Allowlist

Users can be added individually or in bulk:

- Paste one or more **usernames** into the text box, **one per line**
- Save to add them to the allowlist

Users can also be removed individually, or the entire allowlist can be cleared with **Delete all**.

---

## Email Users

A tool for sending a system-level email to all users or a targeted subset of users on the REDCap instance.

> **Note:** Suspended user accounts cannot be emailed through this tool.

### Composing a Message

The **Compose Message** tab is where administrators write and send emails. Before sending, a **User Filter** can be applied to target a specific subset of users.

### User Filters

User filters allow administrators to define which users will receive an email. Filters are built using a rule-based interface:

- **Categories:** Rules can be based on user activity, user privileges, account attributes, and other criteria
- **Logic operators:** AND, OR, AND NOT, OR NOT
- **Grouping:** Rules can be grouped together and groups can be chained using the same logic operators
- **Drag-and-drop reordering:** Rules and groups can be rearranged to adjust hierarchy

**Filter toolbar icons:**

| Icon | Action |
| --- | --- |
| Edit (pencil) | Edit the selected user filter |
| List | Show the list of users matched by the selected filter |
| Plus | Create a new user filter |
| Preview | Preview the message before sending |

**User Filter Manager controls:**

| Control | Action |
| --- | --- |
| Add new rule | Add a single filter condition |
| Add new group | Add a grouped block of conditions |
| Move up / Move down | Reorder nodes within the hierarchy |
| Promote node | Move a node one level up in the hierarchy |
| Delete node | Remove a rule or group |

The **test button** (show list) previews the specific users who match the current filter before sending.

### Message History

The **Message History** tab shows all previously sent emails. Administrators can reuse a past message by clicking the **import icon**, which loads its content into the Compose Message tab for editing or resending.

---

## API Tokens

The API Tokens page is the system-level view of all API tokens across the entire REDCap instance.

> **Note:** API tokens are specific to a single user for a single project. A project can have multiple tokens (one per user with API access), and an individual user can hold multiple tokens (one per project they have API access to).

### Viewing Tokens

Two drop-down filters allow administrators to view tokens by:

- **Individual user** — see all tokens held by a specific user across all their projects
- **Project** — see all users who have an API token for a specific project

### Token Actions

For any existing token, administrators can:

- **Delete** the token — immediately revokes API access for that user/project combination
- **Regenerate** the token — replaces the existing token with a new one; the old token is immediately invalidated

Administrators can also **create a new API token** for a user who does not yet have one for a given project.

### Super API Tokens

In addition to standard project-level tokens, REDCap supports **Super API Tokens**. These grant the holder the ability to create new REDCap projects via the API without requiring administrator approval.

Key characteristics:

| Property | Detail |
| --- | --- |
| Length | 64 characters (vs. 32 characters for standard project-level tokens) |
| Scope | System-wide; not tied to a single project |
| Limit per user | One super token per user |
| Project token on create | When a user creates a project via Super API Token, they also receive the new project's API token without needing admin approval |
| Recommended for | Only the most trusted users |

> **Best practice:** Super API Tokens carry significant system-level access and bypass the normal token approval workflow. Grant them sparingly and with explicit authorization.

### Related Token Settings

- **Auto-generation of tokens:** Controlled in **User Settings** (RC-CC-04). When disabled, users must request a token; when enabled, users can self-generate.
- **API rate limiting / IP banning:** Configured in **General Configuration** (RC-CC-02).
- Tokens do not expire by default — they must be explicitly deleted or regenerated by an administrator.

See RC-API-01 for a full overview of the REDCap API and how tokens are used.

---

## Banned IP Addresses

The Banned IP Addresses page lists all IP addresses that are blocked from the REDCap installation. Any user attempting to load any REDCap page — **including public surveys** — from a banned IP address immediately receives a message stating they cannot use REDCap. No partial access is granted.

Both **IPv4 and IPv6** addresses are supported.

### How IPs Get Banned

- **Manually** by an administrator on this page — for example to block a suspicious actor, a known source of abusive traffic, or an IP involved in unauthorized access attempts.
- **Automatically** by the **Rate Limiter**, when an IP exceeds the configured request threshold. The Rate Limiter is configured on the General Configuration page (RC-CC-02).

Automatic bans from the Rate Limiter persist until deleted by an administrator. A recurring pattern of automatic bans may indicate a misconfigured automated process or an active unauthorized access attempt.

### Adding IPs to the Blocklist

Paste one or more IP addresses into the input field — **one per line** — and submit. Bulk entries are supported. The list shows each banned IP address and its **Time of Ban**. Individual entries can be deleted, and a **Delete All** button clears the entire blocklist at once.

> **Note:** REDCap's IP banning operates at the application layer only. For network-level blocking or advanced threat protection, coordinate with your institutional IT security team.

---

## Access Control Groups

Access Control Groups (ACGs) allow administrators to define the **maximum set of user privileges** that can be granted within projects across the instance.

### What ACGs Do

ACGs do not define what rights a user actually has in a project — they define the **upper boundary** of what rights can be granted. A User Rights manager can assign any subset of the rights permitted by the applicable ACG, but cannot grant rights that exceed it.

This is particularly useful in regulated or compliance-sensitive environments where certain capabilities (such as data export, record deletion, or user rights management) should never be grantable in specific contexts, regardless of what a project manager might attempt to configure.

### Scope and Behavior

| Property | Detail |
| --- | --- |
| Defined at | System level (Control Center) |
| Applied to | All projects system-wide when enabled |
| Enforcement points | When adding a user to a project; when modifying existing user privileges |
| Feature status | Optional — can be enabled or disabled at any time |

Enabling or disabling ACGs does not retroactively change any existing user rights records. The ceiling is enforced only at the next privilege assignment or modification.

### ACG Compliance for Existing Projects

When ACGs are first enabled on an instance that already has projects and users, those existing rights are not automatically adjusted. Each project has an **ACG Compliance** page where administrators can:

- Identify users whose current rights exceed what the applicable ACG permits.
- **Notify** the project's User Rights manager(s) about non-compliant users.
- **Expire** non-compliant users directly from the compliance page.

### Page Tabs

| Tab | Purpose |
| --- | --- |
| **User Assignments** | View and manage which ACG is assigned to each user |
| **Access Control Groups** | Define and configure the ACGs themselves |
| **Reports** | View compliance status and non-compliant counts across all projects |

> **Note:** The ACG section is locked until the feature has been enabled. The feature can be turned on at any point without affecting existing user records.

---

## Administrator Privileges

Located at `ControlCenter/superusers.php`, this page manages which user accounts have REDCap administrator privileges and controls exactly what each administrator can do. Administrator access in REDCap is **granular** — not all-or-nothing — and is composed of seven independent privilege flags that can be mixed and matched per user.

Any user who has been granted at least one administrator privilege gains access to the Control Center, but they will only be able to access and use the sections corresponding to their specific granted privileges.

### The Seven Administrator Privilege Types

**Set Administrator Privileges (`admin_rights`)**
The user can access the Administrator Privileges page and can grant or revoke admin rights for any user. This is effectively a meta-privilege — it lets a user control who else has admin access.

**Access to All Projects and Data with Maximum User Privileges (`super_user`)**
The user has full access to every REDCap project in the system with maximum user-level privileges within those projects. Within the Control Center, this unlocks project administration pages: To-Do List, Edit Project Settings, Link Lookup, and API Tokens.

**Manage User Accounts (`account_manager`)**
The user can access, modify, and (when using Table-based authentication) create REDCap user accounts. This grants access to Browse Users, Add Users, User Allowlist, and Email Users.

**Modify System Configuration Pages (`access_system_config`)**
The user can modify settings on all system configuration pages in the Control Center — everything listed under "Miscellaneous Modules" and "System Configuration" in the sidebar.

> **Read-only fallback:** If a user does *not* have this privilege but *does* have at least one other admin privilege, they can still access system configuration pages in **read-only mode** — they can view settings but cannot save changes.

**Perform REDCap Upgrades (`access_system_upgrade`)**
The user can access upgrade tools, including notifications about new REDCap versions and the Easy Upgrade feature (when enabled by the instance). This privilege does not apply to traditional server-side upgrades that take place outside the REDCap UI.

**Install, Upgrade, and Configure External Modules (`access_external_module_install`)**
The user can install External Modules from the REDCap Repository and enable and configure them at the system level. This does not govern enabling or configuring a module within a specific project, which is controlled by project-level user privileges.

> **Read-only fallback:** If a user does *not* have this privilege but *does* have at least one other admin privilege, they can still access the External Modules page in the Control Center in **read-only mode**.

**Access to Control Center Dashboards (`access_admin_dashboards`)**
The user can access all pages under the "Dashboards & Activity" section of the Control Center sidebar: System Statistics, FHIR Statistics, User Activity Log, User Activity Graphs, Map of Users, Top Usage Report, Database Activity Monitor, Database Query Tool, and Recent Errors.

### Assigning and Removing Privileges

Privileges are granted per user via checkboxes on the Administrator Privileges page. Use the "add a new admin" link at the bottom of the page to add a user — they must already have a valid REDCap account.

Unchecking all privilege checkboxes for a user removes all admin access. REDCap displays a notice confirming the user is no longer an administrator and will no longer appear on this page. Their regular account is unaffected and admin access can be restored at any time.

### Multiple Environments

On instances with separate environments (development, test, production), administrator access is configured independently per environment. It is common for administrators to have broader access in lower environments and more restricted access in production.

> **Best practice:** Limit the number of administrators — especially those with the `super_user` or `admin_rights` flags — to those with an active operational need. Use the granular privilege system to grant only the access each person actively requires.

---

# 2. Common Questions

**Q: Can I recover a deleted user account?**
Once a user is deleted from the Browse Users page, they are permanently removed from the system. Deletion is not reversible through the REDCap UI. If you need to preserve a user's access but prevent future logins, use the Suspend option instead, which can be reversed later. If a user is truly no longer needed, delete them; if there is any chance they might need access again, suspend them instead.

**Q: What is the difference between suspending a user and expiring their account?**
Suspending a user (from Browse Users) immediately blocks login and marks the suspension timestamp. Suspension can be reversed at any time. Account expiration (set on the user's account record) automatically blocks login on a specified date but is less reversible — you must manually change the expiration date to reactivate them. Suspension is used for immediate action (security incident, termination); expiration is used for planned future disablement (contract end date, leave of absence).

**Q: How do I prevent specific users from accessing the API?**
Users can be granted or denied API privileges on their account record in Browse Users. Alternatively, administrators can delete or revoke API tokens from the API Tokens page, preventing that user from using the API for their projects. To prevent all users from generating tokens, modify the "Allow Normal Users to Auto-Generate API Tokens" setting in the User Settings page.

**Q: What happens if an administrator leaves but they are the only one with certain privileges?**
If you have only one user with the `admin_rights` privilege and they leave, you will be unable to change administrator privileges until the owner/super-administrator manually restores access (likely via direct database intervention). Always maintain at least two users with `admin_rights` and `super_user` privileges for continuity. Document your administrator role distribution.

**Q: Can I bulk-edit user attributes for many users at once?**
The Browse Users interface allows one-at-a-time editing. For bulk operations (e.g., changing email domain, suspending a group of users, or assigning expiration dates), there is no built-in bulk UI — you would need to edit each user individually or contact Vanderbilt for a custom database script. Plan ahead for predictable bulk operations (e.g., suspending seasonal researchers at end of season).

---

# 3. Common Mistakes & Gotchas

**Deleting a user account instead of suspending it when the account might be needed again.** User deletion is permanent and cannot be undone through the UI. If there is any possibility the user will need access again (leave of absence, temporary contractor, role change), suspend them instead. Only delete users when you are certain they will never need REDCap access.

**Granting the `super_user` privilege too broadly.** The `super_user` flag grants full access to every project with maximum user-level privileges. Only grant this to administrators with an active need to manage all projects. For administrators who only need to manage specific projects or features, use the granular privileges (e.g., `access_system_config`, `account_manager`) instead.

**Not monitoring API token usage and forgetting which tokens are in use.** Active API tokens that are no longer needed or whose purpose is forgotten create unnecessary security risk. Regularly review the API Tokens page and delete tokens that are no longer actively used. Regenerate tokens if there is any concern they may be compromised.

---

# 4. Related Articles

- RC-CC-03 — Control Center: Security & Authentication (authentication methods affecting user login)
- RC-CC-04 — Control Center: User Settings & Defaults (system-wide user behavior controls)
- RC-USER-01 — User Rights: Overview & Three-Tier Access (user privilege concepts at project level)
- RC-API-01 — REDCap API (API token usage and configuration)
- RC-INST-01 — Institution-Specific Settings & Policies (user management governance)
