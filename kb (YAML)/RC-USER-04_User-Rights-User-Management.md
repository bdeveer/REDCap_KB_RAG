---
id: RC-USER-04
title: User Rights — User Management
domain: User Rights
applies_to:
- All REDCap project types
- requires User Rights privilege for project-level actions
requires: Any supported version
verified_against: REDCap v17.4.1 (Standard) / v17.3.7 (LTS) — changelog review; page
  not re-captured. User management, expiration and suspension behaviour checked against
  source code of v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS)
prerequisites:
- 'RC-USER-01 — User Rights: Overview & Three-Tier Access'
version: '1.2'
last_updated: 2026-11
related:
- id: RC-USER-02
  title: 'User Rights: Adding Users & Managing Roles'
- id: RC-USER-03
  title: 'User Rights: Configuring User Privileges'
- id: RC-DAG-01
  title: Data Access Groups
tags:
- user rights
- user management
synonyms:
- how do i remove a user from a project
- suspend a user's access
- edit an existing user's rights
- set a user expiration date
- revoke access to a project
- difference between project and system suspension
- manage users after they have been added
- ways to remove someone's access
- user access dashboard bulk expire or remove users
---

# 1. Overview

This article covers the ongoing management of users in a REDCap project: editing rights, suspending access, removing users, and managing roles. It also explains the four methods REDCap provides for revoking access, and how to identify the difference between project-level and system-level suspension.

---

# 2. Key Concepts & Definitions

**Expiration Date**

The date on which REDCap automatically suspends a user from a specific project. Suspension is at the project level only — the user retains access to all other projects. An expiration date in the past (or set to today) means the user is currently suspended.

**Project-Level Suspension**

A state in which a user has an expired expiration date and can no longer access the project. They can still log in to REDCap and access other projects. Suspension can be reversed by updating the expiration date.

**Account-Level Expiration**

A separate expiration date that an administrator sets on the user's REDCap **account** (in the Control Center), not on a project. It is unrelated to the project expiration date above. REDCap emails the user a warning 14 days and 2 days before the date; on the date, the account is globally suspended and the user is emailed (with their sponsor copied, if they have one).

**Global Suspension**

A system-level suspension of the user's account. A globally suspended user cannot log in to REDCap at all, cannot access any projects, and cannot use their API tokens. It can be applied manually by an administrator, automatically when an account-level expiration date passes, or automatically after a period of inactivity if the installation has that setting on. Only an administrator can reverse it.

**Project-Level Removal**

Permanently removing a user from a project. The project disappears from their project list, and any direct bookmarks or links to the project will display an error. The user's account and access to other projects are unaffected.

**Global Removal**

Deleting a user's account from the REDCap installation entirely. Performed by administrators only. The user loses access to all projects and all data.

---

# 3. The Four Methods of Revoking Access

REDCap provides four distinct ways to restrict or remove a user's access. They operate at different scopes and are managed by different people.

| Method | Scope | Who Can Do It | Reversible? |
|---|---|---|---|
| **Global removal** | Entire installation | Administrators only | No (account deleted) |
| **Global suspension** | Entire installation | Administrators only | Yes (admin reversal) |
| **Project-level suspension** | One project only | Any user with User Rights privilege | Yes (update expiration date) |
| **Project-level removal** | One project only | Any user with User Rights privilege | Not directly (must re-add the user) |

Project-level actions (suspension and removal) are the tools available to project users. Global actions require administrator intervention. "Administrators" here includes administrators who hold only the user-account management privilege: they can suspend or delete accounts other than full administrators' accounts. A sponsor (on the Sponsor Dashboard) can only request these actions.

> **Note:** A user who has the User Rights privilege but is assigned to a Data Access Group can only manage (suspend, edit, remove) users in their own DAG.

> **Version caveat (17.6.5 Standard; not in 17.3 LTS or 16.0 LTS):** When an administrator suspends an account in the Control Center, the suspend dialog offers **Suspend & Expire in All Projects**. This also sets the user's expiration date in every project to yesterday. Unsuspending the account later does **not** restore those project expiration dates, so the user is still blocked in each project. To restore access, clear or reset the expiration date in each project's User Rights page (or ask the project's User Rights managers to). On 17.3 LTS and 16.0 LTS the dialog suspends the account only.

> **Note on inactivity suspension:** Automatic suspension after a period of inactivity is an administrator setting with no default. Users get no warning before it happens; the installation may email them afterwards.

> **Institution-specific:** For this installation's policy on automatic global suspension (e.g., inactivity-based) and the process to request reactivation, see **[RC-INST-01 — Institution-Specific Settings & Policies — Production](RC-INST-01_Institution-Specific-Settings-and-Policies.md) — Institution-Specific Settings & Policies, Section 6: Global User Suspension Policy**.

---

# 4. Editing User Rights

To manage a user, click on their username in the User Rights page. This opens a small **User actions:** menu next to the name. The options depend on whether the user is in a role:

| User is... | Options in the User actions menu |
|---|---|
| Not in a role | **Edit user privileges**, **Assign to role**, **Remove from project** |
| In a role | **Re-assign to role**, **Remove from role**, **Remove from project** |

**Edit user privileges** opens the user privileges popup, where you edit the user's individual rights and click **Save Changes**.

> **Note:** If the user is assigned to a role, you cannot directly edit their individual user rights; there is no Edit option. Re-assign them to another role or remove them from the role. A user removed from a role through **Remove from role** retains the role's rights as their individual rights until you explicitly edit them.

---

# 5. Suspending a User (Project Level)

Project-level suspension is controlled entirely by the expiration date.

- A user is **suspended** if their expiration date is today or in the past.
- A user is **active** if their expiration date is blank or in the future.

You can update the expiration date in two ways:

1. **Directly from the User Rights page** — click on the date (or the word "never") shown next to the user's name in the user list. A date picker will appear.
2. **Through the user privileges popup** — choose **Edit user privileges**, update the expiration date field, and click **Save Changes**. (For a user in a role, use the date in the user list.)

> **Note:** Expiration dates are independent of roles. If a user is in a role, their expiration date is still a per-user setting that you edit directly on that user — not on the role.

**What an expired user sees:** an **ACCESS DENIED!** message telling them their access to the project has expired. The project still appears in their My Projects list, and their API token for the project is refused. Their rights, DAG assignment and API token are kept, so moving the date into the future (or clearing it) restores access exactly as before. REDCap does not warn the user before a project expiration date arrives.

**Reading the user list:**
- A user with a **red expiration date** is currently suspended at the project level.
- A user showing a red **[account suspended]** label beside their username is suspended at the global level. It is possible for a user to be suspended at both levels simultaneously.

> **Note:** A user whose expiration date is **today** is already blocked, but the date is not shown in red until tomorrow. Don't rely on the red colour alone; read the date.

## 5.1 User Access Dashboard

The **User Access Dashboard** lists the users of the projects you manage. From it you can expire users in bulk (it sets their expiration date to yesterday) or remove them from projects, which is the quickest way to clear out former staff across many projects. You can also opt in to a monthly email reminder, sent on the first weekday of the month, to review your projects' users.

---

# 6. Removing a User (Project Level)

To remove a user from your project:

1. Click on the user's name in the User Rights page to open the **User actions:** menu.
2. Choose **Remove from project** and confirm. (For a user who is not in a role, the **Remove user** button at the bottom of the user privileges popup does the same.)

This works whether or not the user is in a role; you do not need to remove them from the role first.

The project will disappear from the user's My Projects list. Any direct links or bookmarks to the project will show an error for that user. Removal is logged as "Delete user", and the user's past actions stay in the Logging.

**What removal deletes.** Removing a user deletes their whole rights record for the project, including:

- their **API token** for the project (any script using it stops working; a re-added user needs a new token);
- their **DAG assignment** (a re-added user starts unassigned, which means they see all records unless you assign them a DAG again);
- their entries in **report access** lists and **project bookmark** access lists (reports and bookmarks limited to specific users no longer include them, and re-adding the user does not put them back).

> **Note:** If the user collects data in the REDCap Mobile App, REDCap warns you before removal that data not yet synced from their device may be lost. Ask them to sync first.

---

# 7. Managing Roles

## 7.1 Editing a Role

Click on a role name in the User Rights page to open the role's edit popup. Make your changes and click **Save Changes**; nothing is saved until you do. Saved changes apply to all users currently in that role — you do not need to update users individually.

## 7.2 Copying a Role

Within the role edit popup, use the **Copy role** option to create a new role with identical rights. This is useful when you need a variant of an existing role with minor differences.

## 7.3 Deleting a Role

Use the **Delete role** option within the role edit popup. On the User Rights page, REDCap blocks deletion if any users are currently assigned to the role. Remove all users from the role first (or re-assign them).

> **Tip:** When you remove a user from a role with **Remove from role** without re-assigning them to another, they retain the role's rights as their individual rights. Their rights remain unchanged until you edit them directly. Clearing a role does not remove users from the project — they simply shift to individual rights.

> **Important — deleting a role through the API:** The API **Delete User Roles** method, unlike the User Rights page, is **not** blocked when users are assigned to the role. Those users stay in the project and keep only their leftover individual rights, not the role's rights. For a user who was added straight into the role, those leftover rights are REDCap's defaults, which can include the **User Rights** privilege. After deleting a role through the API, review every user who was in it and re-assign them or edit their rights. See [RC-API-27 — Delete User Roles API](RC-API-27_Delete-User-Roles.md).

---

# 7a. Administrator-Side Improvements

Changes to the Control Center pages used for user administration.

| Change | Version |
| --- | --- |
| The **"Delete all"** button on the User Allowlist page uses a modern confirmation dialog rather than a browser JavaScript alert, making it harder to dismiss accidentally | 15.6.1 |
| **Sponsor Dashboard** approval pages show only the users affected by the request, rather than every user the sponsor manages | 15.6.1 |
| "Password was last reset on X" reworded to **"Password was last reset by an admin on X"** on the Browse Users page, which is a materially different statement | 16.1.1 |
| "Manage All Project Tokens" indicates when a user is **suspended** | 15.8.2 |
| The **API Tokens** page has searchable drop-downs for selecting a user and project | 17.1.0 |
| Adding a table-based user shows an error **as you type the username** if it already exists, rather than on submit | 17.0.6 |

> **Note on the 16.1.1 wording change.** "Password was last reset on X" could be read as the user having changed their own password. The corrected text makes clear it was an **administrator** action — which matters when you are reconstructing who did what to an account.

---

# 8. Common Questions

**Q: I need to temporarily remove someone's access — should I suspend them or remove them?**

**A:** Use suspension (set the expiration date to today or the past) if you may need to restore their access later. Use removal if you want to fully remove their project access. Re-adding a removed user requires going through the add-user process again and reconfiguring their rights.

**Q: A user says they can see the project but can't log in at all — is that a project-level or system-level issue?**

**A:** If they cannot log in to REDCap at all, it is a Tier 1 / global issue — either a login credential problem or a global suspension. Contact a REDCap administrator. Project-level suspensions only block access to the specific project — a project-suspended user can still log in.

**Q: Can I restore a globally suspended user myself?**

**A:** No. Global suspensions are managed exclusively by REDCap administrators. Contact your local REDCap support team.

**Q: What happens to a user's data if I remove them from the project?**

**A:** Nothing. Data in REDCap is not owned by users. Removing a user from the project does not delete or alter any records they entered or modified. The audit trail also retains their actions. What *is* deleted is the user's own project setup: their rights, API token, DAG assignment, and their place in report and bookmark access lists. If you might need them back, suspend them instead.

**Q: A user's expiration date has passed. Can they still use their API token?**

**A:** No. The API refuses a token whose user has expired in the project, and refuses all tokens of a globally suspended user. The token is kept, so it works again once you restore the user's access.

**Q: Can I set an expiration date on a role rather than individual users?**

**A:** No. Expiration dates are a per-user setting and cannot be defined at the role level. You must set or update expiration dates on each user individually.

**Q: I removed a user from a role but now they still have those rights — is that a bug?**

**A:** No, this is expected behavior. When a user is removed from a role, they retain the role's rights as their individual rights. You need to explicitly edit their individual rights if you want to change them after role removal.

---

# 9. Common Mistakes & Gotchas

**Removing a user when you only meant to pause them.** Removal deletes the user's API token, DAG assignment and report/bookmark access. Re-adding them means rebuilding all of that, and a re-added user with no DAG sees every record. Use an expiration date for a temporary pause.

**Confusing project suspension with global suspension.** A project-suspended user can still log in to REDCap and access other projects. A globally suspended user cannot log in at all. Reading the visual indicators on the User Rights page (red expiration date vs. the red "[account suspended]" label) clarifies which is which.

**Confusing the project expiration date with an account expiration date.** The expiration date on the User Rights page affects one project. An account-level expiration date is set by an administrator and globally suspends the whole account when it passes. Only an administrator can change it.

**Assuming removed users lose their data.** Removing a user from a project does not delete or affect any data they entered. The audit trail preserves all their actions. If data cleanup is needed, that must be done separately.

**Clearing a role and assuming users lose access.** Removing users from a role with **Remove from role** leaves them in the project with the role's rights as individual rights. If the goal is to revoke those rights, you must remove or edit each user separately after clearing the role. Deleting a role through the API is worse: its users are left with leftover or default individual rights, which can include the User Rights privilege. Review them afterwards.

**Not using expiration dates for temporary users.** For anyone with time-limited access (students, interns, contractors), set an expiration date at the time you add them. Most access issues involving former contributors come from not setting this date when the user was first added.

---

## API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) for authentication, token management, and setup.

- **[RC-API-22 — Export Users API](RC-API-22_Export-Users.md)** — retrieve a complete list of project users and their permissions
- **[RC-API-23 — Import Users API](RC-API-23_Import-Users.md)** — add users or update user permissions programmatically
- **[RC-API-24 — Delete Users API](RC-API-24_Delete-Users.md)** — remove a user from the project programmatically (works for users in a role too; deletes the same items as removal in the interface)
- **[RC-API-27 — Delete User Roles API](RC-API-27_Delete-User-Roles.md)** — delete a role; unlike the interface, not blocked when users are assigned (see section 7.3)

---


# 10. Related Articles

- [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md) (troubleshooting access issues)
- [RC-USER-02 — User Rights: Adding Users & Managing Roles](RC-USER-02_User-Rights-Adding-Users-and-Managing-Roles.md) (how to add users and create roles)
- [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) (all rights settings explained)
- [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) (DAG assignment and management)
