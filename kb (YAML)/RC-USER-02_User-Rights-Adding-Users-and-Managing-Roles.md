---
id: RC-USER-02
title: User Rights — Adding Users & Managing Roles
domain: User Rights
applies_to:
- All REDCap project types
- requires User Rights privilege
requires: Any supported version
verified_against: REDCap v17.4.1 (Standard) / v17.3.7 (LTS) — changelog review; page
  not re-captured
prerequisites:
- 'RC-USER-01 — User Rights: Overview & Three-Tier Access'
version: '1.1'
last_updated: 2026-08
related:
- id: RC-USER-01
  title: 'User Rights: Overview & Three-Tier Access'
- id: RC-USER-03
  title: 'User Rights: Configuring User Privileges'
- id: RC-USER-04
  title: 'User Rights: User Management'
- id: RC-DAG-01
  title: Data Access Groups
- id: RC-CC-25
  title: 'Control Center: Access Control Groups'
tags:
- user rights
- user management
synonyms:
- how do i add a user to my project
- give someone access to my redcap project
- create a user role
- apply the same rights to multiple users
- assign a role to a user
- manage roles in user rights
- invite a colleague to a project
- set up user roles for a team
---

> **Critical — version caveat: roles imported via CSV or API got the wrong form-level rights.** Creating a user role by **CSV import or API** could fail to set the role's **form-level data viewing rights** correctly (below 15.9.1 Standard), and separately, adding a user or role to a project did not save data viewing rights correctly between 15.7.0 and 15.7.2. Both produce roles whose actual permissions differ from what was submitted — in a direction nobody verifies, because the import reports success. If roles were provisioned in bulk on those versions, audit the resulting per-instrument rights rather than trusting the source file.
>
> A related defect: importing user roles from a **Project XML** file failed to create them at all until 16.0.26.

# 1. Overview

This article covers how to add users to a REDCap project, how to use roles to apply pre-configured rights to multiple users at once, and how to manage roles. It is part of the User Rights series. Before a user can be added to a project, they must already have an active account in the REDCap installation — see [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md) for an explanation of the three-tier access model.

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

A project-level grouping that restricts which records a user can see or interact with. A user can be assigned to a DAG at the time they are added to a project. See [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) for full details.

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
5. Configure the user's rights in the popup. See [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md)
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
6. Optionally, assign the user to a Data Access Group using the **Assign to DAG** dropdown. See [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) for more on DAGs.
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
4. Configure the desired user rights in the popup. See [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md)
5. Click **Create role** in the bottom right of the popup.

> **Note:** Roles cannot have a pre-assigned Data Access Group or a default expiration date. Both of those settings are configured per user, not per role. See [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) for DAG assignment options, and [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) for expiration date configuration.

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

Ghost users have no real account attached and are harmless in terms of data access, but they clutter the user list and should be cleaned up. Remove a ghost user the same way you would remove a real user — see [RC-USER-04 — User Rights: User Management](RC-USER-04_User-Rights-User-Management.md) — User Management.

---

# 7. Bulk User Management

The **Upload or download users, roles, and assignments** button (top right of the User Rights page) allows you to:

- **Download** the current configuration of all users, roles, and role assignments as separate structured CSV files.
- **Upload** modified versions of those files to apply changes in bulk.

This is useful for large projects, for migrating a user configuration from one project to another, or for onboarding many users at once without editing each individually.

**Upload behavior:** Additive/update — new entries are added and existing entries are updated to match the uploaded file. Users present in the project but absent from the uploaded file are **not** removed.

> **Golden rule:** Always download first, then edit the downloaded file. The CSV formats contain encoded values (especially for form-level permissions) that are impractical to construct from scratch. Starting from a downloaded template avoids column order mistakes and encoding errors.

## 7.1 Users CSV

**Filename produced by download:** `[ProjectName]_Users_[Date].csv`

Each row represents one project user. The full column set:

| Column | Type | Description |
|---|---|---|
| `username` | string | REDCap username. Must match an existing account in this installation. Required. |
| `expiration` | date (`YYYY-MM-DD`) | Account expiration date. Leave blank for no expiration. |
| `data_access_group` | string | Unique DAG name (not the label) to assign the user to a DAG. Leave blank if not in a DAG. |
| `data_access_group_id` | integer | Numeric ID of the DAG. Informational — REDCap uses `data_access_group` as the key. |
| `data_access_group_label` | string | Human-readable DAG label. Informational only. |
| `design` | 0/1 | Project Design & Setup rights. |
| `alerts` | 0/1 | Alerts & Notifications access. |
| `user_rights` | 0/1 | Ability to manage other users' rights. |
| `data_access_groups` | 0/1 | Ability to create and manage DAGs. |
| `reports` | 0/1 | Create and edit reports. |
| `stats_and_charts` | 0/1 | View Stats & Charts. |
| `manage_survey_participants` | 0/1 | Manage survey participants and distribution. |
| `calendar` | 0/1 | Access the Calendar. |
| `data_import_tool` | 0/1 | Access the Data Import Tool. |
| `data_comparison_tool` | 0/1 | Access the Data Comparison Tool. |
| `logging` | 0/1 | View project logging. |
| `email_logging` | 0/1 | View email logging. |
| `file_repository` | 0/1 | Access the File Repository. |
| `data_quality_create` | 0/1 | Create Data Quality rules. |
| `data_quality_execute` | 0/1 | Execute Data Quality rules. |
| `api_export` | 0/1 | API token with export rights. |
| `api_import` | 0/1 | API token with import/write rights. |
| `api_modules` | 0/1 | Access to API playground and modules. |
| `mobile_app` | 0/1 | Access the REDCap Mobile App. |
| `mobile_app_download_data` | 0/1 | Allow data download via Mobile App. |
| `record_create` | 0/1 | Create new records. |
| `record_rename` | 0/1 | Rename existing records. |
| `record_delete` | 0/1 | Delete records. |
| `lock_records_all_forms` | 0/1 | Lock/unlock records across all forms. |
| `lock_records` | 0/1 | Lock/unlock individual records. |
| `lock_records_customization` | 0/1 | Customize locking behavior per form. |
| `forms` | encoded string | Per-form data-entry access. Quoted, comma-separated list of `form_name:access_level` pairs (e.g., `"screening:130,demographics:130"`). See note on form encoding below. |
| `forms_export` | encoded string | Per-form export access. Same format as `forms`, using `1` to grant export access (e.g., `"screening:1,demographics:1"`). Leave blank to deny export access on all forms. |

**Form access encoding.** The integer values in the `forms` column are REDCap's internal encoded permission levels — they are not simple 0/1 flags. Values observed in downloaded files include `130` (read/write) and `138` (a different access variant, likely read-only or a survey-specific permission). Do not attempt to construct these values from memory; always use a downloaded file as your template and modify only the specific forms you need to change.

## 7.2 User Roles CSV

**Filename produced by download:** `[ProjectName]_UserRoles_[Date].csv`

Each row represents one custom user role. Columns are nearly identical to the Users CSV with these differences:

1. **First column is `unique_role_name`** — the system-generated role identifier (format: `U-XXXXXXXXX`). Do not modify this value when editing an existing role; REDCap uses it to match the import row to the correct role. To create a new role via import, you can leave this blank — REDCap will assign an ID.
2. **Second column is `role_label`** — the human-readable role name shown in the UI (e.g., `"demo role"`).
3. **No user-level columns** — `expiration`, `data_access_group`, `data_access_group_id`, and `data_access_group_label` are absent. Those are per-user settings, not role-level settings.

> **Column order difference:** The three locking columns appear in a different order than in the Users CSV. In the Users file: `lock_records_all_forms`, `lock_records`, `lock_records_customization`. In the User Roles file: `lock_records_customization`, `lock_records`, `lock_records_all_forms`. This is one more reason to always start from a downloaded template rather than building manually.

## 7.3 User–Role Assignments CSV

**Filename produced by download:** `[ProjectName]_UserRoleAssignments_[Date].csv`

The simplest of the three files — just two columns:

| Column | Description |
|---|---|
| `username` | REDCap username. Must match a user already in the project. |
| `unique_role_name` | System-generated role ID (e.g., `U-594WK7W9KY`). Leave blank if the user is not assigned to any role (individual rights). |

All project users appear in this file, including those without a role assignment (their `unique_role_name` is blank). Uploading this file assigns or clears role assignments — it does not add or remove users from the project.

> **Cross-file consistency:** The `unique_role_name` values here must match the IDs in the User Roles CSV. If you are migrating a role configuration from another project, do not hardcode old role IDs in the assignments file. Instead: upload the User Roles CSV to the new project first, then re-download the User Roles CSV to get the newly assigned IDs, then build or update the assignments file using those new IDs.

---

# 8. Common Questions

**Q: I entered a user's name but they didn't appear in the search results — what's wrong?**

**A:** The user does not have an account in this REDCap installation. They need to register or be provisioned before they can be added to any project. See **[RC-INST-01 — Institution-Specific Settings & Policies — Production](RC-INST-01_Institution-Specific-Settings-and-Policies.md)

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

**Renaming a role that is referenced in branching logic.** REDCap allows branching logic to reference the current user's role by name using the `[user-role-label]` smart variable — for example, to restrict a sensitive field to a specific reviewer role. This is useful for enforcing role-based access within a form, but it creates a hidden dependency: the role's display name as shown in User Rights becomes a hard-coded string in the data dictionary. If that role is later renamed (even a capitalisation change, e.g., `"data manager"` → `"Data Manager"`), every branching condition referencing the old name silently breaks — the field becomes invisible or permanently visible to everyone in that role, with no error message. Before renaming any role, search the data dictionary for its name in branching logic, calculated fields, and action tags. Treat role names referenced in logic as frozen identifiers for the life of the project, and document them separately from the User Rights configuration so the dependency is visible.

**Querying per-user rights columns directly without accounting for roles.** When pulling user rights from the backend database (rather than the web interface), the per-user permission columns on `redcap_user_rights` are unreliable for users assigned to a role. Resolve effective rights by coalescing with `redcap_user_roles` — see [Querying User Rights in the Backend Database](#querying-user-rights-in-the-backend-database) below. A query that reads only the per-user columns will return the wrong set of users.

---

## Querying User Rights in the Backend Database

> **Scope:** This is a database-administration topic, relevant only when querying REDCap's MySQL/MariaDB tables directly — for example, to build a list of who holds design or user-rights across many projects on an instance. It does **not** apply to the User Rights web interface, which always shows correct effective rights.

**The gotcha.** When a user is assigned to a **role**, their effective permissions come from `redcap_user_roles`, not from the per-user permission columns on `redcap_user_rights`. Those per-user columns (`design`, `user_rights`, and the others) are **not reliable** for role-assigned users — they can retain stale or default values that do not reflect the role. In practice:

- the per-user `user_rights` column is frequently left at `1` for role members regardless of the role's actual setting, so a filter like `rights.user_rights = 1` sweeps in nearly the entire project roster — data-entry staff, site monitors, and external collaborators included; and
- the per-user `design` column can be `0` for users who are in fact designers **through their role**, so a filter like `rights.design = 1` silently misses them.

A query that reads only the per-user columns is therefore both over- and under-inclusive. In one real cross-instance pull, the naive form returned more than double the correct number of users (~43 → ~98 rows) and included outside-institution email addresses that should never have been in the result.

**The fix.** Join `redcap_user_roles` on `role_id` and resolve each permission with `COALESCE(role_value, per_user_value)` — this uses the role's value when the user is in a role (`role_id` is set) and falls back to the per-user value otherwise:

```sql
SELECT
    rights.project_id      AS pid,
    projects.app_title     AS project_title,
    projects.status        AS project_status,
    rights.username,
    info.user_email,
    COALESCE(roles.design,      rights.design)      AS effective_design,
    COALESCE(roles.user_rights, rights.user_rights) AS effective_user_rights,
    info.user_suspended_time
FROM redcap_user_rights rights
    LEFT JOIN redcap_user_information info ON info.username    = rights.username
    LEFT JOIN redcap_projects       projects ON projects.project_id = rights.project_id
    LEFT JOIN redcap_user_roles     roles ON roles.role_id    = rights.role_id
WHERE rights.project_id IN ( /* one or more project_ids */ )
    AND (
        COALESCE(roles.design,      rights.design)      = 1
        OR COALESCE(roles.user_rights, rights.user_rights) = 1
    )
ORDER BY pid;
```

Notes:

- Add `AND info.user_suspended_time IS NULL` to limit the result to accounts that can currently act (suspended users cannot log in).
- `project_status` distinguishes Development (0), Production (1), and Inactive/Completed (2) if you want to narrow scope.
- `user_email` can be blank for shared/service accounts — check before using the output for a mailing.

---

## API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) for authentication, token management, and setup.

- **[RC-API-23 — Import Users API](RC-API-23_Import-Users.md)** — add users or update user permissions programmatically
- **[RC-API-25 — Export User Roles API](RC-API-25_Export-User-Roles.md)** — retrieve all custom role definitions
- **[RC-API-26 — Import User Roles API](RC-API-26_Import-User-Roles.md)** — create or modify custom user roles programmatically
- **[RC-API-27 — Delete User Roles API](RC-API-27_Delete-User-Roles.md)** — remove a role from the project programmatically

---


# 10. Related Articles

- [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md) (prerequisites and the three-tier model)
- [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) (all individual right settings explained)
- [RC-USER-04 — User Rights: User Management](RC-USER-04_User-Rights-User-Management.md) (editing, suspending, and removing users)
- [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) (assigning users to DAGs)
- [RC-CC-25 — Control Center: Access Control Groups](RC-CC-25_Access-Control-Groups.md) (system-level ceiling on what privileges can be assigned; enforced at the point of user addition and privilege modification)
