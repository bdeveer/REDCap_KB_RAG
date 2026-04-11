RC-USER-04

**User Rights — User Management**

| **Article ID** | RC-USER-04 |
|---|---|
| **Domain** | User Rights |
| **Applies To** | All REDCap project types; requires User Rights privilege for project-level actions |
| **Prerequisite** | RC-USER-01 — User Rights: Overview & Three-Tier Access |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-USER-02 — Adding Users & Managing Roles; RC-USER-03 — Configuring User Privileges; RC-DAG-01 — Data Access Groups |

---

# 1. Overview

This article covers the ongoing management of users in a REDCap project: editing rights, suspending access, removing users, and managing roles. It also explains the four methods REDCap provides for revoking access, and how to identify the difference between project-level and system-level suspension.

---

# 2. Key Concepts & Definitions

**Expiration Date**

The date on which REDCap automatically suspends a user from a specific project. Suspension is at the project level only — the user retains access to all other projects. An expiration date in the past (or set to today) means the user is currently suspended.

**Project-Level Suspension**

A state in which a user has an expired expiration date and can no longer access the project. They can still log in to REDCap and access other projects. Suspension can be reversed by updating the expiration date.

**Global Suspension**

A system-level suspension applied by an administrator. A globally suspended user cannot log in to REDCap at all and cannot access any projects. Only an administrator can reverse this.

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

Project-level actions (suspension and removal) are the tools available to project users. Global actions require administrator intervention.

> **Institution-specific:** For this installation's policy on automatic global suspension (e.g., inactivity-based) and the process to request reactivation, see **RC-INST-01 — Institution-Specific Settings & Policies, Section 6: Global User Suspension Policy**.

---

# 4. Editing User Rights

To edit an individual user's rights, click on their username in the User Rights page. This opens the user privileges popup. From here you can:

- Directly edit individual user rights (if the user is not in a role)
- Assign the user to a different role
- Remove the user from their current role

> **Note:** If the user is assigned to a role, you cannot directly edit their individual user rights. The popup will offer you the option to reassign them to another role or remove them from the role. A user removed from a role retains the role's rights as their individual rights until you explicitly edit them.

---

# 5. Suspending a User (Project Level)

Project-level suspension is controlled entirely by the expiration date.

- A user is **suspended** if their expiration date is today or in the past.
- A user is **active** if their expiration date is blank or in the future.

You can update the expiration date in two ways:

1. **Directly from the User Rights page** — click on the date (or the word "never") shown next to the user's name in the user list. A date picker will appear.
2. **Through the user privileges popup** — open the user's rights, update the expiration date field, and save.

> **Note:** Expiration dates are independent of roles. If a user is in a role, their expiration date is still a per-user setting that you edit directly on that user — not on the role.

**Reading the user list:**
- A user with a **red expiration date** is currently suspended at the project level.
- A user showing "**user suspended**" below their name is suspended at the global level (by an administrator). It is possible for a user to be suspended at both levels simultaneously.

---

# 6. Removing a User (Project Level)

To remove a user from your project:

1. Click on the user's name in the User Rights page to open their privileges popup.
2. Click the **Remove user** button in the bottom right of the popup.

The project will disappear from the user's My Projects list. Any direct links or bookmarks to the project will show an error for that user.

> **Note:** You cannot remove a user who is currently assigned to a role. First remove them from the role (by opening their privileges popup and selecting the option to remove the role), then remove them from the project as described above.

---

# 7. Managing Roles

## 7.1 Editing a Role

Click on a role name in the User Rights page to open the role's edit popup. All setting changes save immediately and propagate to all users currently in that role — you do not need to update users individually.

## 7.2 Copying a Role

Within the role edit popup, use the **Copy role** option to create a new role with identical rights. This is useful when you need a variant of an existing role with minor differences.

## 7.3 Deleting a Role

Use the **Delete role** option within the role edit popup. REDCap will block deletion if any users are currently assigned to the role. Remove all users from the role first.

> **Tip:** When you remove a user from a role without re-assigning them to another, they retain the role's rights as their individual rights. Their rights remain unchanged until you edit them directly. This means deleting a role does not remove users from the project — they simply shift to individual rights.

---

# 8. Common Questions

**Q: I need to temporarily remove someone's access — should I suspend them or remove them?**

**A:** Use suspension (set the expiration date to today or the past) if you may need to restore their access later. Use removal if you want to fully remove their project access. Re-adding a removed user requires going through the add-user process again and reconfiguring their rights.

**Q: A user says they can see the project but can't log in at all — is that a project-level or system-level issue?**

**A:** If they cannot log in to REDCap at all, it is a Tier 1 / global issue — either a login credential problem or a global suspension. Contact a REDCap administrator. Project-level suspensions only block access to the specific project — a project-suspended user can still log in.

**Q: Can I restore a globally suspended user myself?**

**A:** No. Global suspensions are managed exclusively by REDCap administrators. Contact your local REDCap support team.

**Q: What happens to a user's data if I remove them from the project?**

**A:** Nothing. Data in REDCap is not owned by users. Removing a user from the project does not delete or alter any records they entered or modified. The audit trail also retains their actions.

**Q: Can I set an expiration date on a role rather than individual users?**

**A:** No. Expiration dates are a per-user setting and cannot be defined at the role level. You must set or update expiration dates on each user individually.

**Q: I removed a user from a role but now they still have those rights — is that a bug?**

**A:** No, this is expected behavior. When a user is removed from a role, they retain the role's rights as their individual rights. You need to explicitly edit their individual rights if you want to change them after role removal.

---

# 9. Common Mistakes & Gotchas

**Trying to remove a user who is still in a role.** REDCap blocks removal of role-assigned users. Remove them from the role first, then remove them from the project. The option to remove the role is in the user's privileges popup.

**Confusing project suspension with global suspension.** A project-suspended user can still log in to REDCap and access other projects. A globally suspended user cannot log in at all. Reading the visual indicators on the User Rights page (red expiration date vs. "user suspended" text) clarifies which is which.

**Assuming removed users lose their data.** Removing a user from a project does not delete or affect any data they entered. The audit trail preserves all their actions. If data cleanup is needed, that must be done separately.

**Deleting a role and assuming users lose access.** Deleting a role only removes the role definition — users who were in that role keep their rights as individual rights. If the goal is to revoke those rights, you must remove or edit each user separately after clearing the role.

**Not using expiration dates for temporary users.** For anyone with time-limited access (students, interns, contractors), set an expiration date at the time you add them. Most access issues involving former contributors come from not setting this date when the user was first added.

---

## API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See RC-API-01 — REDCap API for authentication, token management, and setup.

- **RC-API-22 — Export Users API** — retrieve a complete list of project users and their permissions
- **RC-API-23 — Import Users API** — add users or update user permissions programmatically
- **RC-API-24 — Delete Users API** — remove a user from the project programmatically

---


# 10. Related Articles

- RC-USER-01 — User Rights: Overview & Three-Tier Access (troubleshooting access issues)
- RC-USER-02 — User Rights: Adding Users & Managing Roles (how to add users and create roles)
- RC-USER-03 — User Rights: Configuring User Privileges (all rights settings explained)
- RC-DAG-01 — Data Access Groups (DAG assignment and management)
