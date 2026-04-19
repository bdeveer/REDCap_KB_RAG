RC-USER-02

**User Rights — Adding Users & Managing Roles**

| **Article ID** | RC-USER-02 |
|---|---|
| **Domain** | User Rights |
| **Applies To** | All REDCap project types; requires User Rights privilege |
| **Prerequisite** | RC-USER-01 — User Rights: Overview & Three-Tier Access |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-USER-01 — Overview & Three-Tier Access; RC-USER-03 — Configuring User Privileges; RC-USER-04 — User Management; RC-DAG-01 — Data Access Groups |

---

# 1. Overview

This article covers how to add users to a REDCap project, how to use roles to apply pre-configured rights to multiple users at once, and how to manage roles. It is part of the User Rights series. Before a user can be added to a project, they must already have an active account in the REDCap installation — see RC-USER-01 for an explanation of the three-tier access model.

---

# 2. Key Concepts & Definitions

**User Rights Menu**

The section of a REDCap project where users are added, rights are configured, and roles are managed. Access to this menu is itself a user right — only users with the "User Rights" privilege can see it.

**Individual User Rights**

A custom rights configuration set directly on a single user, independent of any role. Each setting can be tailored specifically for that user.

**User Role**

A named, saved set of user rights that can be assigned to multiple users. When a role is updated, the change applies to all users currently in that role. Roles do not include per-user settings like expiration dates or DAG assignments.

**Ghost User**

An entry in the user list that looks like a real user but is not tied to an actual REDCap account. Ghost users are created by skipping the step of selecting a user from the search results dropdown and instead pressing Enter or clicking Add with a free-typed name.

**DAG (Data Access Group)**

A project-level grouping that restricts which records a user can see or interact with. A user can be assigned to a DAG at the time they are added to a project. See RC-DAG-01 — Data Access Groups for full details.

**Bulk User Management**

A feature accessible from the User Rights page that allows downloading and uploading users, roles, and role assignments as structured files, enabling large-scale changes without editing each user manually.

---

# 3. Prerequisites for Adding a User

Two conditions must be true before you can add someone to your project:

1. **The user must have an active account in the REDCap installation.** They cannot be added if they have no account or if their account has been suspended system-wide.
2. **You must have the "User Rights" privilege in that project.** If you do not see the User Rights menu, you do not have this privilege and cannot add users.

If the User Rights menu is visible in the project's application menu or on the Project Setup page, you have the necessary access.

---

# 4. Adding Users

There are two methods for adding users to a project: individually with custom rights, or directly into a role.

## 4.1 Individual Method

Use this method when you want to configure a user's rights specifically, without applying a role.

1. Navigate to the **User Rights** menu.
2. In the section labeled "Add new user," enter the user's name, email address, or username in the search box.
3. Select the correct user from the dropdown list of search results that appears.
4. Click **+ Add with custom rights**.
5. Configure the user's rights in the popup. See RC-USER-03 — Configuring User Privileges for details on each setting.
6. Click **Add user** in the bottom right of the popup.

If successful, the project will appear in the user's My Projects page.

> **Important:** Always select the user from the dropdown list — do not type a name and press Enter without selecting from the results. Partial names are accepted; REDCap will return all matching users. Skipping the selection step creates a ghost user (see Section 6).

## 4.2 Role Method

Use this method when you want to add a user with a predefined set of rights (a role). This is faster when onboarding multiple users who need the same level of access.

1. Navigate to the **User Rights** menu.
2. In the section labeled "Assign new user to role," enter the user's name, email address, or username in the search box.
3. Select the correct user from the dropdown list of search results.
4. Click **Assign to role**.
5. In the popup, select the desired role from the **Select role** dropdown.
6. Optionally, assign the user to a Data Access Group using the **Assign to DAG** dropdown. See RC-DAG-01 for more on DAGs.
7. The **Notify user via email** checkbox is checked by default. This sends the user an automated email confirming they have been added to a new project. This email is a useful way to confirm you selected the right user.
8. Click **Assign** in the bottom right of the popup.

If successful, the project will appear in the user's My Projects page.

---

# 5. Creating and Managing Roles

## 5.1 Why Use Roles

Roles are most valuable when multiple users need identical access — for example, a team of data entry staff or a group of co-investigators. When you update a role's rights, the change propagates automatically to all users assigned to that role. Roles are also useful for compliance-aligned project setups (e.g., projects designed to meet 21 CFR Part 11 or GDPR requirements).

## 5.2 Creating a Role

1. On the User Rights page, find the "Enter new role name" text box.
2. Type a descriptive name for the role.
3. Click **Create role**.
4. Configure the desired user rights in the popup. See RC-USER-03 — Configuring User Privileges for details.
5. Click **Create role** in the bottom right of the popup.

> **Note:** Roles cannot have a pre-assigned Data Access Group or a default expiration date. Both of those settings are configured per user, not per role. See RC-DAG-01 for DAG assignment options, and RC-USER-03 for expiration date configuration.

## 5.3 Editing a Role

Click the role name on the User Rights page to open the role's edit popup. Change any settings and save. All users currently assigned to that role will immediately reflect the updated rights.

## 5.4 Copying and Deleting a Role

Within the role edit popup, you have options to copy or delete the role.

- **Copy:** Creates a new role with the same rights configuration. Useful for creating a variant of an existing role.
- **Delete:** Permanently removes the role. REDCap will not allow deletion if any users are currently assigned to that role — remove all users from the role first.

---

# 6. Ghost Users

A ghost user is an entry in the user list that is not tied to a real REDCap account. Ghost users are created when someone types a name into the "Add new user" or "Assign new user to role" box and activates the action without selecting an account from the search results dropdown.

Ghost users can look nearly identical to legitimate users in the list. The way to distinguish them is to look for the user's real name in parentheses after their username. A properly added user will have this (e.g., `jsmith123 (Jane Smith)`). A ghost user will not.

Ghost users have no real account attached and are harmless in terms of data access, but they clutter the user list and should be cleaned up. Remove a ghost user the same way you would remove a real user — see RC-USER-04 — User Management.

---

# 7. Bulk User Management

The **Upload or download users, roles, and assignments** button (top right of the User Rights page) allows you to:

- **Download** the current configuration of all users, roles, and role assignments as structured files.
- **Upload** modified versions of those files to apply changes in bulk.

This is useful for large projects or when migrating user configurations from another project.

---

# 8. Common Questions

**Q: I entered a user's name but they didn't appear in the search results — what's wrong?**

**A:** The user does not have an account in this REDCap installation. They need to register or be provisioned before they can be added to any project. See **RC-INST-01 — Institution-Specific Settings & Policies, Section 5: User Account Creation** for the process at this installation.

**Q: Can I add someone to multiple projects at once?**

**A:** No. Users are added to projects one at a time from within each project's User Rights menu. For bulk additions across many projects, contact a REDCap administrator.

**Q: What's the difference between adding a user individually vs. adding them to a role?**

**A:** Both result in the user being added to the project. The difference is how their rights are managed afterward. Individual users have rights you configure directly for them. Role users inherit rights from the role and cannot have their individual rights edited until they are removed from the role.

**Q: Can I assign a user to a role and also give them custom individual rights on top of it?**

**A:** No. A user is either in a role or has individual rights — not both simultaneously. If you remove a user from a role, they retain the role's rights as their individual rights, which you can then edit.

**Q: Can a user be in multiple roles at once?**

**A:** No. A user can only be assigned to one role at a time within a given project.

**Q: The "notify user via email" box is checked — should I always send the notification?**

**A:** In most cases, yes. The email confirms to the user that they have been added and helps you verify you selected the right person. You might uncheck it if you are adding many users at once and plan to notify them separately.

---

# 9. Common Mistakes & Gotchas

**Skipping the dropdown selection and creating ghost users.** This is the most common error when adding users. Always wait for the search results to appear and click the correct user from the list. Never press Enter or click Add without selecting a result. Ghost users do not have real accounts and contribute nothing except confusion.

**Trying to edit individual rights for a role user.** If a user is in a role, you cannot edit their rights directly. The popup will tell you to either reassign them to another role or remove them from the role first. If you need a one-off adjustment for a specific user, remove them from the role and edit their individual rights.

**Deleting a role before removing its users.** REDCap blocks role deletion if any users are assigned to it. Remove all users from the role first, then delete it.

**Not reviewing rights after adding a new instrument.** When a new instrument is added to the project, existing user rights do not automatically update to include it. Review all user rights (or role configurations) after adding instruments to ensure access is set correctly for the new instrument.

---

## API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See RC-API-01 — REDCap API for authentication, token management, and setup.

- **RC-API-23 — Import Users API** — add users or update user permissions programmatically
- **RC-API-25 — Export User Roles API** — retrieve all custom role definitions
- **RC-API-26 — Import User Roles API** — create or modify custom user roles programmatically
- **RC-API-27 — Delete User Roles API** — remove a role from the project programmatically

---


# 10. Related Articles

- RC-USER-01 — User Rights: Overview & Three-Tier Access (prerequisites and the three-tier model)
- RC-USER-03 — User Rights: Configuring User Privileges (all individual right settings explained)
- RC-USER-04 — User Rights: User Management (editing, suspending, and removing users)
- RC-DAG-01 — Data Access Groups (assigning users to DAGs)
