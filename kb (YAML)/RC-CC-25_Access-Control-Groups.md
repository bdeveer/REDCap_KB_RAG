---
id: RC-CC-25
title: 'Control Center: Access Control Groups'
domain: Control Center (Admin)
applies_to:
- REDCap administrators
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — Access
  Control Group behaviour checked against source code; earlier live check (v17.5.6)
  of page tabs and table columns kept; pages not re-captured
prerequisites:
- REDCap administrator access
- familiarity with REDCap user rights
version: '1.6'
last_updated: 2026-11
related:
- id: RC-CC-07
  title: 'Control Center: Users & Access Management'
- id: RC-USER-01
  title: 'User Rights: Overview & Three-Tier Access'
- id: RC-USER-02
  title: 'User Rights: Adding Users & Managing Roles'
- id: RC-USER-03
  title: 'User Rights: Configuring User Privileges'
tags:
- control center (admin)
synonyms:
- what are access control groups
- limit the maximum privileges a project manager can grant
- set a ceiling on user rights across projects
- prevent certain users from getting export or delete rights
- restrict grantable privileges instance-wide
- acg setup in the control center
- full list of acg permission columns
- compliance control over user rights
- cap user permissions at the system level
---

# 1. Overview

**Access Control Groups (ACGs)** are a system-level feature that lets REDCap administrators define the **maximum set of user privileges** that can be granted within projects across the entire instance.

> **Not to be confused with Project Administrator Groups.** ACGs group **users** and cap **what rights they can be given**. **PAGs** group **projects** and determine **who receives administrative requests** for them — production status changes, draft approvals and other project requests. Both are administrator-facing and both are "groups"; they are otherwise unrelated. See [RC-PLUS-04 — REDCap+: Project Administrator Groups (PAGs)](RC-PLUS-04_Project-Administrator-Groups.md).

ACGs do not directly set what rights a user has in a project. Instead, they define an upper boundary — a ceiling — on the rights that a User Rights manager is permitted to grant. When a user is added to a project or when their privileges are modified, REDCap checks that the privileges being assigned do not exceed what the user's ACG allows. If they do, the assignment is blocked.

This makes ACGs useful in regulated or compliance-sensitive environments where certain capabilities — such as data export, record deletion, or user rights management — should never be grantable to specific user populations, regardless of what an individual project manager might attempt to configure.

Key characteristics:

| Property | Detail |
| --- | --- |
| Defined at | System level (Control Center only) |
| Applied to | All projects system-wide when enabled |
| Enforcement points | When adding a user to a project; when modifying user privileges in a project (including User Rights CSV and API imports); when a project is created, copied or built from a template; when a new instrument is added |
| Feature status | Optional — can be enabled or disabled at any time |
| Scope | Users who don't yet have an assignment, including new accounts, are placed into the Default ACG |

The ACG page is in the Control Center left-hand menu under **Users → Access Control Groups**.

**Who can manage ACGs:** administrators with any of the **Access to all projects and data**, **Manage user accounts** or **Admin rights** privileges.

> **Note:** Enabling or disabling ACGs does not retroactively modify any existing user rights records in projects. The ceiling is enforced only at the point of the next privilege assignment or modification.

While ACGs are enabled, REDCap also applies the ceiling automatically in two places where no one is choosing rights by hand:

- **New projects.** When a project is created, copied or created from a template, every user's rights in the new project are cut back to what their ACG allows.
- **New instruments.** When an instrument is added to a project, the default instrument-level rights given to existing users are reduced so they fit within each user's ACG.

> **Note:** Users who do not have a REDCap account record (for example, externally authenticated usernames that have never logged in) cannot be added to projects while ACGs are enabled. Ask them to log in once first, or create the account, then add them.

> **Critical — if you use the "Security Access Groups" External Module, read this before upgrading.** Access Control Groups is the productised form of Andrew Poppe's *Security Access Groups* module, introduced in **16.0.0**. Upgrading **does not disable the module and does not migrate its settings**. An instance that had the module enabled ends up running both systems side by side, each with its own configuration, each enforcing a ceiling on user rights, and neither aware of the other. Decide which implementation to keep and disable the other deliberately. See [RC-EM-01 — External Modules: Overview & Manager](RC-EM-01_External-Modules-Overview-and-Manager.md) §7a for the other core features absorbed from community modules.

---

# 2. Enabling and Disabling ACGs

The ACG feature is toggled via the **ACG enabled** toggle at the top right of the page. The feature is off by default and must be explicitly turned on by an administrator.

While the feature is off, the page is locked: you **cannot create ACGs or assign users to them before enabling**. Setup happens after the toggle is switched on.

## Enabling ACGs for the First Time

Before enabling, read the warning carefully. When ACGs are first turned on:

- **Existing users go into the Default ACG immediately** — REDCap's own enable warning says so. The built-in default is the **"No Rights"** group, which has no rights (or minimal rights) across all privilege categories.
- Until you have created your ACGs and assigned users to them, User Rights managers will be unable to grant those users anything beyond the Default ACG's ceiling. This can cause operational disruption if you leave a gap between enabling and setup.

> **Recommended sequence:** Enable ACGs at a quiet time (outside working hours) → right away create your groups → mark one as the Default → bulk-assign users with the **Upload user assignments (CSV)** option. Plan the groups and prepare the assignment CSV in advance so the gap is as short as possible.

If you later disable ACGs, your saved groups and user assignments stay in place and are used again when you re-enable.

> **Version caveat — the first weeks of ACGs were rough (16.0.0 to 16.1.8).** Two blocking defects shipped with or shortly after the feature: with ACGs enabled, **non-admin users could not access any project at all** — every page failed with a fatal PHP error (fixed 16.1.9 Standard / 16.0.20 LTS) — and **uploading a Data Dictionary** with ACGs enabled could fail fatally (fixed 17.0.2). Several further fixes followed for report loading, compliance evaluation and CSV import. If you are enabling ACGs, do it on a current version rather than an older one that happens to include the feature.

> **Version caveat (below 16.1.4 Standard):** ACG compliance checks could be **bypassed entirely** by uploading user rights or role assignments via the User Rights CSV import or the API. The ceiling held in the interface but not through those paths. Fixed in 16.1.4 — see [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) §9a. The 16.0.x LTS line already enforces compliance for CSV and API imports on 16.0.61; if you run an older Standard release, upgrade before relying on ACGs for imported rights.

## Disabling ACGs

Disabling the feature removes the enforcement ceiling across all projects. Existing user rights in individual projects are not changed, but User Rights managers will no longer be constrained by ACG rules when adding or modifying users.

---

# 3. Page Tabs

The ACG page has three tabs:

| Tab | Purpose |
| --- | --- |
| **User Assignments** | View all users and their current ACG assignment; change assignments individually or in bulk via CSV |
| **Access Control Groups** | View, create, edit, copy, and delete ACG definitions; configure the rights ceiling for each group |
| **Reports** | Run compliance reports to identify users and projects with non-compliant rights system-wide |

---

# 4. User Assignments Tab

This tab lists every user registered on the instance along with their current ACG assignment.

## Viewing and Changing Assignments

The user list displays each user's **name** and their **Access Control Group**. To change a user's assignment:

1. Click **Enter edit mode**.
2. Use the drop-down next to each user to select a new ACG. Each change saves immediately — there is no separate save step.

Users who don't yet have an assignment, including new accounts, are placed into the Default ACG and can then be moved to any defined group.

> **From 16.1.8 Standard (17.x):** a user's ACG can also be set **at the point of account creation** for table-based users, changed later from the **Edit User** page, and is shown on **View User**. See [RC-CC-07 — Control Center: Users & Access Management](RC-CC-07_Control-Center-User-Management.md).

> **Version caveat (16.0.x LTS):** there is no ACG picker on the Create User or Edit User pages, and View User does not show the ACG. Create the account first, then assign its ACG on this tab (individually or by CSV).

## Bulk Assignment via CSV

For large-scale assignments, the tab provides CSV export and import:

| Action | Description |
| --- | --- |
| **Download user assignments (CSV)** | Export the current assignment table |
| **Upload user assignments (CSV)** | Import a modified assignment file to reassign users in bulk |

Before the import is committed, REDCap displays a **review dialog** showing the proposed changes so administrators can confirm before applying them.

---

# 5. Access Control Groups Tab

This tab is where ACG definitions are created and managed. Each ACG specifies the maximum allowed value for every configurable user right.

## Creating a New ACG

Enter a name in the **Create new Access Control Group** field and click **Create ACG**. The new group appears in the table and can be immediately configured.

## ACG Table Actions

Click a group's name in the table to open its options:

| Action | Description |
| --- | --- |
| Edit | Modify the rights configuration for an existing ACG |
| Copy Group | Duplicate an existing ACG under a new name |
| Delete Group | Permanently delete the ACG (cannot be undone). Its members lose their assignment and go to the Default ACG |

**Setting the Default ACG:** tick **Make this ACG the Default Group?** in the group's edit dialog. The Default is marked with a star in the table. It applies to any user who doesn't have an assignment — not only at the moment the feature is first enabled.

> **Note:** The built-in **"No Rights"** group is the system default and cannot be deleted. It serves as the initial default ACG when the feature is first enabled.

## CSV Export and Import for ACG Definitions

The ACG table itself can also be exported and re-imported:

| Action | Description |
| --- | --- |
| **Download ACGs (CSV raw)** | Export ACG definitions using raw coded values |
| **Download ACGs (CSV labels)** | Export ACG definitions using human-readable labels |
| **Upload ACGs (CSV)** | Import new or updated ACG definitions in bulk |
| **Download ACG import template (CSV)** | Download a blank template to use when building a new import file |

Before import, REDCap displays a **review dialog** showing all proposed ACG changes for confirmation.

---

# 6. Configuring an ACG — Rights Categories

When you edit an ACG, you set the maximum allowed value for each privilege category. The categories mirror the user rights options available in project-level User Rights management. What you configure here is not the value the user will have — it is the highest value they can be given.

On 17.5.6 the ACG table has 34 permission columns: Create Project; Project Design and Setup; User Rights; Data Access Groups; Data Viewing Rights; Data Export Rights; Alerts & Notifications; Add/Edit Reports; Stats & Charts; Survey Distribution Tools; Calendar & Scheduling; Data Import Tool; Data Comparison Tool; Logging; Email Logging; File Repository; Double Data Entry; Record Locking Customization; Lock/Unlock Entire Records; Lock/Unlock Records; Randomization; Data Quality (create/edit rules); Data Quality (execute rules); Data Resolution Workflow; API; REDCap Mobile App; Mobile App Download Data; CDP/DDP Setup / Mapping; CDP/DDP Adjudicate Data; DTS; Manage MyCap Participants; Create Records; Rename Records; Delete Records.

The subsections below explain the categories that have several levels or special rules. They do not cover every column.

## User Rights

Controls the maximum level of User Rights access a user may be granted.

| Level | Description |
| --- | --- |
| No Access | Cannot be granted any User Rights access |
| Read Only | Can view the User Rights page but cannot make changes |
| Full Access | Can add, modify, and remove users and roles in projects |

> **Important:** Users whose ACG does not allow Full Access User Rights are also blocked from **creating or copying projects**. This is because a user who creates a project and cannot manage their own User Rights would immediately be locked out of administering that project. REDCap administrators are exempt from this block.

## Data Viewing Rights (Form-Level)

Controls the maximum data viewing rights that can be granted at the form level. Options roughly correspond to the standard form-level viewing options in User Rights:

- No Access (Hidden)
- Read Only
- View & Edit
- View & Edit + Edit Survey Responses
- View & Edit + Delete
- View & Edit + Edit Survey Responses + Delete

## Data Export Rights (Form-Level)

Controls the maximum data export rights that can be granted per form:

- No Access
- De-Identified
- Remove All Identifier Fields
- Full Data Set

## Survey Distribution Tools

On/off toggle: controls whether users may be granted the Survey Distribution Tools right.

## Data Resolution Workflow

Controls the maximum level of Data Resolution Workflow access (when the workflow is enabled on the instance):

- No Access
- View Only
- Open Only
- Respond
- Open and Respond
- Open, Close, Respond

## Randomization

Randomization is three separate checkboxes in the edit dialog, each allowing or blocking one part of the module:

| Checkbox | Allows the user to be granted |
| --- | --- |
| **Setup** | Configuring the randomization setup |
| **Dashboard** | Viewing the randomization dashboard |
| **Randomize** | Randomizing records |

The ACG CSV has a separate column for each, such as **Randomization (Setup)**. The table shows a combined summary label in a single **Randomization** column.

> **Version caveat (below 16.1.0 Standard):** When importing ACG assignments by CSV, the review dialog misreported changes to **API** and **Randomization** privileges. Check those columns on the User Rights page after an import on an older version rather than trusting the review summary.

## API Access

API is also three separate checkboxes: **API Export**, **API Import** and **External Modules API**. The ACG CSV has a separate column for each, such as **API (Import)**; the table shows a combined summary label in a single **API** column.

## Calendar & Scheduling

On/off toggle: controls whether users may be granted access to the Calendar & Scheduling module.

## Double Data Entry (DDE) Person

On/off toggle: controls whether users may be assigned as a Double Data Entry person.

## Lock/Unlock Records

Controls whether users can be granted the ability to lock or unlock records:

- No Access
- Lock/Unlock Records (instrument level)
- E-signature (implies locking authority with e-signature capability)

## Mobile App Download Data

On/off toggle: controls whether users may be granted the ability to download project data via the REDCap Mobile App.

## Clinical Data Pull from EHR / Dynamic Data Pull from External Source System

On/off toggle: controls whether users may be granted access to clinical data pull or dynamic data pull integrations (when those modules are enabled on the instance).

---

# 7. Custom ACG Error Message

Administrators can configure an **optional custom error message** that is shown to User Rights managers when they attempt to set privileges that violate a user's ACG. This message appears in the violation popup in addition to the list of non-compliant rights.

If no custom message is configured, a default system message is displayed. The custom message can be useful for directing project managers to contact an administrator or to a specific policy reference.

The custom message field is found at the bottom of the Access Control Groups tab.

---

# 7a. Project Creation Privilege *(17.1.0+)*

From REDCap **17.1.0**, an ACG can also govern whether its members may **create projects** — or request project creation where approval is required. When editing or creating an ACG, administrators choose to:

- **grant** project creation for everyone in the group,
- **deny** it for everyone in the group, overriding the user-level setting, or
- **defer** to the user-level project creation privilege set on each account (the default).

This is a departure from the rest of ACG behaviour and worth noting: elsewhere an ACG defines the *ceiling* of rights a user may be granted within a project, whereas this setting can grant or deny an instance-level capability outright.

> **From 17.3.3, the deny setting also blocks project copying.** Setting project creation to "No (overrides the user-level setting)" originally did not stop a user copying an existing project — an obvious way around the restriction. Copying now requires **both** project creation permission and Full Access user rights. On 17.1.0–17.3.2 the restriction is incomplete.

> **Version caveat (16.0.x LTS):** there is no per-ACG project creation setting. Control project creation with the user-level privilege on each account (see [RC-CC-07 — Control Center: Users & Access Management](RC-CC-07_Control-Center-User-Management.md)). Copying a project on 16 requires only Full Access user rights in the source project, so a user without create permission can still copy; if that matters, restrict Full Access user rights in their ACG.

> **17.x only:** the Project Migration Tool (REDCap+) applies the same ACG check as copying a project. See [RC-PLUS-02 — Project Migration Tool](RC-PLUS-02_Project-Migration-Tool.md).

---

# 8. ACG Smart Variables

ACGs support **ACG-specific Smart Variables** that can be used in certain REDCap expressions and contexts, chiefly for telling users what is non-compliant about their rights:

| Smart Variable | Purpose |
| --- | --- |
| `[user-acg-name]` | The name of the user's assigned ACG |
| `[user-acg-noncompliant-rights]` | Lists the recipient's own non-compliant rights |
| `[acg-noncompliance-table]` | Renders the non-compliance table for the project. The recipient must have User Rights access in the project (all versions) |

> **From 17.1.3:** `[user-acg-noncompliant-rights]` no longer requires the *recipient* to hold the User Rights privilege. The requirement was dropped because the variable only ever shows a user their own non-compliant rights, never anyone else's — so gating it behind User Rights prevented exactly the people who needed the message from receiving it.

> **Version caveat (16.0.x LTS):** in alerts, `[user-acg-noncompliant-rights]` still shows only when the recipient has User Rights access in the project. To reach users without it, list the non-compliant rights in the alert text yourself, or upgrade to 17.x.

For details on Smart Variables in general, see [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md).

---

# 9. Reports Tab

The Reports tab provides system-wide compliance visibility. Administrators can run reports to identify users or projects where existing rights exceed what the assigned ACG permits.

> **Note:** All reports in this tab consider only table-based users (not externally-authenticated-only users without a REDCap account record).

## Available Reports

| Report | Description |
| --- | --- |
| **Users with Non-compliant Rights (non-expired)** | All users whose current project rights exceed their ACG, excluding expired users |
| **Users with Non-compliant Rights (all)** | Same as above, including expired users |
| **Projects with Non-compliant Rights (non-expired)** | All projects with at least one non-compliant user, excluding expired users |
| **Projects with Non-compliant Rights (all)** | Same as above, including expired users |
| **Users and Projects with Non-compliant Rights (non-expired)** | Every user-project combination where rights are non-compliant, excluding expired users |
| **Users and Projects with Non-compliant Rights (all)** | Same as above, including expired users |

Reports can be **exported as CSV** for further analysis or record-keeping.

## Report Filters

Each report table supports filtering by user, ACG, project, and specific non-compliant rights, as well as a search field for quick lookup.

---

# 10. ACG Compliance at the Project Level

In addition to the system-wide Reports tab, each individual project has an **ACG Compliance** page accessible to administrators, opened from the **ACGs** link in the project menu. It has two tabs: **Project Compliance** and **Compliance Alert Logs**. This is most relevant when:

1. ACGs are first enabled on a system that already has projects and users — existing rights are not automatically trimmed.
2. A user's ACG assignment is changed — their existing project rights may now exceed the new ACG's ceiling.

From the project-level ACG Compliance page, an administrator can:

- View all users in the project whose current rights exceed their ACG.
- See exactly which rights are non-compliant for each user.
- **Email users** (or User Rights managers) a Compliance Alert about the violation, optionally with reminders.
- **Expire users** from the compliance view — set the expiration a number of days out, or enter 0 to expire them now.

Compliance alerts are sent on a schedule that runs every 15 minutes, so allow a short delay before they arrive. The **Compliance Alert Logs** tab records past compliance alert emails for audit purposes.

---

# 11. Common Questions

**Q: If I enable ACGs and a user already has rights in a project that exceed their ACG, do those rights get removed automatically?**
No. Enabling ACGs does not retroactively modify existing user rights in existing projects (only new projects, copies and new instruments are trimmed automatically). The ACG ceiling is only enforced at the point of a future rights assignment or modification. Use the ACG Compliance page (per project) or the Reports tab to identify and remediate existing violations.

**Q: Can I create an ACG that allows everything?**
Yes — configure all rights at their maximum values. This effectively removes the ceiling for users in that group, making ACG enforcement a no-op for them. This can be useful for trusted power users or administrators who should not be restricted.

**Q: What happens to users who are not yet assigned to an ACG when I enable the feature?**
Users who don't yet have an assignment, including new accounts, are placed into the Default ACG. Right after you first enable the feature that is the built-in "No Rights" group, which prevents User Rights managers from granting them any privileges — so create your groups, mark your own Default and bulk-assign users straight after enabling.

**Q: Can I create my ACGs and assign users before I turn the feature on?**
No. The ACG page is locked while the feature is off. Enable it at a quiet time and do the setup immediately afterwards (see §2).

**Q: Can I disable ACGs temporarily and re-enable them later?**
Yes. The feature can be toggled at any time without affecting existing project rights, and your saved ACGs and user assignments stay in place. When re-enabled, enforcement resumes from the point of the next rights assignment or modification.

**Q: How do I bulk-reassign all users to a new ACG?**
Use the CSV export from the User Assignments tab, modify the ACG column in the exported file, and re-upload using the Upload user assignments (CSV) option. Review the proposed changes in the confirmation dialog before committing.

**Q: What is the difference between an ACG and a User Role?**
User Roles (defined within an individual project) are templates that specify what rights a user *will* have in that project. ACGs are a system-level ceiling that constrains what rights *can* be granted — they operate independently of roles. A User Role cannot grant rights that exceed the user's ACG, even if the role itself is defined with higher privileges.

---

# 12. Common Mistakes & Gotchas

**Enabling ACGs without a plan to assign users straight away.** The moment ACGs are enabled, existing users are placed in the Default ACG. If that default is "No Rights" (the system default), User Rights managers cannot grant those users anything until they are reassigned. You cannot set up groups before enabling, so enable at a quiet time and then immediately create your groups, mark an appropriate Default and bulk-assign users by CSV — with the groups planned and the CSV prepared in advance.

**Deleting an ACG that still has members.** Its members lose their assignment and fall back to the Default ACG. Reassign them first if the Default is more restrictive than you intend.

**Not planning for non-compliant users in existing projects.** Existing rights are not automatically adjusted when ACGs are enabled. Projects with active users may immediately be out of compliance once the feature is on. Run a compliance review (using the Reports tab or per-project ACG Compliance page) as part of your rollout plan.

**Granting "Full Access" User Rights in an ACG too broadly.** Users whose ACG permits Full Access User Rights can manage all user privileges in every project they are added to. Reserve this level for researchers and coordinators who genuinely need it.

**Confusing ACGs with Data Access Groups (DAGs).** DAGs (configured within individual projects) restrict which *records* a user can see. ACGs (configured system-wide) restrict which *privileges* a user can be granted. They serve different purposes and operate independently. See [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) for DAG documentation.

**Forgetting to update ACG assignments when institutional roles change.** ACG assignments are static until manually changed. If a user's role or affiliation changes, their ACG assignment must be updated in the User Assignments tab (or via CSV import) to reflect their new privilege ceiling.

---

# 13. Related Articles

- [RC-CC-07 — Control Center: Users & Access Management](RC-CC-07_Control-Center-User-Management.md) (brief ACG overview and broader user management context)
- [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md) (user privilege concepts at project level)
- [RC-USER-02 — User Rights: Adding Users & Managing Roles](RC-USER-02_User-Rights-Adding-Users-and-Managing-Roles.md) (how users are added to projects; where ACG enforcement occurs)
- [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) (the full set of configurable user rights that ACGs control)
- [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) (record-level access restriction, distinct from ACGs)
