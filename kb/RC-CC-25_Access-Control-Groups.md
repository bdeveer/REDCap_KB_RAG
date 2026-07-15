

**Control Center: Access Control Groups**

| **Article ID** | [RC-CC-25 — Control Center: Access Control Groups](RC-CC-25_Access-Control-Groups.md) |
| --- | --- |
| **Domain** | Control Center (Admin) |
| **Applies To** | REDCap administrators |
| **Prerequisite** | REDCap administrator access; familiarity with REDCap user rights |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-CC-07 — Control Center: Users & Access Management](RC-CC-07_Control-Center-User-Management.md); [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md); [RC-USER-02 — User Rights: Adding Users & Managing Roles](RC-USER-02_User-Rights-Adding-Users-and-Managing-Roles.md); [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) |
| Synonyms | what are access control groups; limit the maximum privileges a project manager can grant; set a ceiling on user rights across projects; prevent certain users from getting export or delete rights; restrict grantable privileges instance-wide; acg setup in the control center; compliance control over user rights; cap user permissions at the system level |

---

## 1. Overview

**Access Control Groups (ACGs)** are a system-level feature that lets REDCap administrators define the **maximum set of user privileges** that can be granted within projects across the entire instance.

ACGs do not directly set what rights a user has in a project. Instead, they define an upper boundary — a ceiling — on the rights that a User Rights manager is permitted to grant. When a user is added to a project or when their privileges are modified, REDCap checks that the privileges being assigned do not exceed what the user's ACG allows. If they do, the assignment is blocked.

This makes ACGs useful in regulated or compliance-sensitive environments where certain capabilities — such as data export, record deletion, or user rights management — should never be grantable to specific user populations, regardless of what an individual project manager might attempt to configure.

Key characteristics:

| Property | Detail |
| --- | --- |
| Defined at | System level (Control Center only) |
| Applied to | All projects system-wide when enabled |
| Enforcement points | When adding a user to a project; when modifying user privileges in a project |
| Feature status | Optional — can be enabled or disabled at any time |
| Scope | Every user on the instance receives an ACG assignment when the feature is enabled |

The ACG page is located at `ControlCenter/access_control_groups.php`.

> **Note:** Enabling or disabling ACGs does not retroactively modify any existing user rights records in projects. The ceiling is enforced only at the point of the next privilege assignment or modification.

---

## 2. Enabling and Disabling ACGs

The ACG feature is toggled via the **ACG enabled** toggle at the top right of the page. The feature is off by default and must be explicitly turned on by an administrator.

### Enabling ACGs for the First Time

Before enabling, read the warning carefully. When ACGs are first turned on:

- **Every existing user is immediately assigned to the Default ACG.** The built-in default is the **"No Rights"** group, which has no rights (or minimal rights) across all privilege categories.
- If you have not yet created a custom Default ACG, User Rights managers in every project will be unable to add users or modify user privileges until you have created ACGs and assigned users to them. This can cause an immediate operational disruption if done without preparation.

> **Recommended sequence:** Create your ACGs first → assign users to them via CSV import → then enable the feature.

### Disabling ACGs

Disabling the feature removes the enforcement ceiling across all projects. Existing user rights in individual projects are not changed, but User Rights managers will no longer be constrained by ACG rules when adding or modifying users.

---

## 3. Page Tabs

The ACG page has three tabs:

| Tab | Purpose |
| --- | --- |
| **User Assignments** | View all users and their current ACG assignment; change assignments individually or in bulk via CSV |
| **Access Control Groups** | View, create, edit, copy, and delete ACG definitions; configure the rights ceiling for each group |
| **Reports** | Run compliance reports to identify users and projects with non-compliant rights system-wide |

---

## 4. User Assignments Tab

This tab lists every user registered on the instance along with their current ACG assignment.

### Viewing and Changing Assignments

The user list displays each user's **name** and their **Access Control Group**. To change a user's assignment:

1. Click **Enter edit mode**.
2. Use the drop-down next to each user to select a new ACG.
3. Exit edit mode to save.

Once the feature is enabled, every user has an ACG assignment. Users are initially placed in the Default ACG and can subsequently be moved to any defined group.

### Bulk Assignment via CSV

For large-scale assignments, the tab provides CSV export and import:

| Action | Description |
| --- | --- |
| **Download user assignments (CSV)** | Export the current assignment table |
| **Upload user assignments (CSV)** | Import a modified assignment file to reassign users in bulk |

Before the import is committed, REDCap displays a **review dialog** showing the proposed changes so administrators can confirm before applying them.

---

## 5. Access Control Groups Tab

This tab is where ACG definitions are created and managed. Each ACG specifies the maximum allowed value for every configurable user right.

### Creating a New ACG

Enter a name in the **Create new Access Control Group** field and click **Create ACG**. The new group appears in the table and can be immediately configured.

### ACG Table Actions

| Action | Description |
| --- | --- |
| Edit | Modify the rights configuration for an existing ACG |
| Copy Group | Duplicate an existing ACG under a new name |
| Delete Group | Permanently delete the ACG (cannot be undone) |
| Set as Default | Mark this ACG as the default for newly enabled instances |

> **Note:** The built-in **"No Rights"** group is the system default and cannot be deleted. It serves as the initial default ACG when the feature is first enabled.

### CSV Export and Import for ACG Definitions

The ACG table itself can also be exported and re-imported:

| Action | Description |
| --- | --- |
| **Download ACGs (CSV raw)** | Export ACG definitions using raw coded values |
| **Download ACGs (CSV labels)** | Export ACG definitions using human-readable labels |
| **Upload ACGs (CSV)** | Import new or updated ACG definitions in bulk |
| **Download ACG import template (CSV)** | Download a blank template to use when building a new import file |

Before import, REDCap displays a **review dialog** showing all proposed ACG changes for confirmation.

---

## 6. Configuring an ACG — Rights Categories

When you edit an ACG, you set the maximum allowed value for each privilege category. The categories mirror the user rights options available in project-level User Rights management. What you configure here is not the value the user will have — it is the highest value they can be given.

### User Rights

Controls the maximum level of User Rights access a user may be granted.

| Level | Description |
| --- | --- |
| No Access | Cannot be granted any User Rights access |
| Read Only | Can view the User Rights page but cannot make changes |
| Full Access | Can add, modify, and remove users and roles in projects |

> **Important:** Users whose ACG does not allow Full Access User Rights are also blocked from **creating or copying projects**. This is because a user who creates a project and cannot manage their own User Rights would immediately be locked out of administering that project.

### Data Viewing Rights (Form-Level)

Controls the maximum data viewing rights that can be granted at the form level. Options roughly correspond to the standard form-level viewing options in User Rights:

- No Access (Hidden)
- Read Only
- View & Edit
- View & Edit + Edit Survey Responses
- View & Edit + Delete
- View & Edit + Edit Survey Responses + Delete

### Data Export Rights (Form-Level)

Controls the maximum data export rights that can be granted per form:

- No Access
- De-Identified
- Remove All Identifier Fields
- Full Data Set

### Survey Distribution Tools

Controls the maximum level of access to survey distribution features:

- No Access
- View Only
- Open Only
- Respond
- Open and Respond
- Open, Close, Respond

### Randomization

Controls access to the randomization module:

| Level | Description |
| --- | --- |
| No Access | Cannot access randomization |
| Setup | Can configure the randomization setup |
| Dashboard | Can view the randomization dashboard |
| Randomize | Can perform randomizations |
| Setup & Dashboard | Setup plus dashboard access |
| Setup & Perform | Setup plus the ability to randomize |
| Dashboard & Perform | Dashboard access plus the ability to randomize |
| Setup + Dashboard + Perform | Full randomization access |

There is also a separate **Randomization (Setup)** right that controls access to the randomization setup independently.

### API Access

Controls the maximum API rights that can be granted:

- No Access
- Import
- Export
- Import & Export
- External Modules API
- Import + External Modules API
- Export + External Modules API

### Calendar & Scheduling

On/off toggle: controls whether users may be granted access to the Calendar & Scheduling module.

### Double Data Entry (DDE) Person

On/off toggle: controls whether users may be assigned as a Double Data Entry person.

### Lock/Unlock Records

Controls whether users can be granted the ability to lock or unlock records:

- No Access
- Lock/Unlock Records (instrument level)
- E-signature (implies locking authority with e-signature capability)

### Mobile App Download Data

On/off toggle: controls whether users may be granted the ability to download project data via the REDCap Mobile App.

### Clinical Data Pull from EHR / Dynamic Data Pull from External Source System

On/off toggle: controls whether users may be granted access to clinical data pull or dynamic data pull integrations (when those modules are enabled on the instance).

---

## 7. Custom ACG Error Message

Administrators can configure an **optional custom error message** that is shown to User Rights managers when they attempt to set privileges that violate a user's ACG. This message appears in the violation popup in addition to the list of non-compliant rights.

If no custom message is configured, a default system message is displayed. The custom message can be useful for directing project managers to contact an administrator or to a specific policy reference.

The custom message field is found at the bottom of the Access Control Groups tab.

---

## 8. ACG Smart Variables

ACGs support **ACG-specific Smart Variables** that can be used in certain REDCap expressions and contexts. The ACG page includes a tip referencing this capability. For details on Smart Variables in general, see the Smart Variables documentation.

---

## 9. Reports Tab

The Reports tab provides system-wide compliance visibility. Administrators can run reports to identify users or projects where existing rights exceed what the assigned ACG permits.

> **Note:** All reports in this tab consider only table-based users (not externally-authenticated-only users without a REDCap account record).

### Available Reports

| Report | Description |
| --- | --- |
| **Users with Non-compliant Rights (non-expired)** | All users whose current project rights exceed their ACG, excluding expired users |
| **Users with Non-compliant Rights (all)** | Same as above, including expired users |
| **Projects with Non-compliant Rights (non-expired)** | All projects with at least one non-compliant user, excluding expired users |
| **Projects with Non-compliant Rights (all)** | Same as above, including expired users |
| **Users and Projects with Non-compliant Rights (non-expired)** | Every user-project combination where rights are non-compliant, excluding expired users |
| **Users and Projects with Non-compliant Rights (all)** | Same as above, including expired users |

Reports can be **exported as CSV** for further analysis or record-keeping.

### Report Filters

Each report table supports filtering by user, ACG, project, and specific non-compliant rights, as well as a search field for quick lookup.

---

## 10. ACG Compliance at the Project Level

In addition to the system-wide Reports tab, each individual project has an **ACG Compliance** page accessible to administrators. This is most relevant when:

1. ACGs are first enabled on a system that already has projects and users — existing rights are not automatically trimmed.
2. A user's ACG assignment is changed — their existing project rights may now exceed the new ACG's ceiling.

From the project-level ACG Compliance page, an administrator can:

- View all users in the project whose current rights exceed their ACG.
- See exactly which rights are non-compliant for each user.
- **Email users** (or User Rights managers) a Compliance Alert about the violation.
- **Expire users** directly from the compliance view to immediately remove their project access.

An **alert log** records past compliance alert emails for audit purposes.

---

## 11. Common Questions

**Q: If I enable ACGs and a user already has rights in a project that exceed their ACG, do those rights get removed automatically?**
No. Enabling ACGs does not retroactively modify existing user rights. The ACG ceiling is only enforced at the point of a future rights assignment or modification. Use the ACG Compliance page (per project) or the Reports tab to identify and remediate existing violations.

**Q: Can I create an ACG that allows everything?**
Yes — configure all rights at their maximum values. This effectively removes the ceiling for users in that group, making ACG enforcement a no-op for them. This can be useful for trusted power users or administrators who should not be restricted.

**Q: What happens to users who are not yet assigned to an ACG when I enable the feature?**
All users are immediately assigned to the Default ACG at the moment the feature is enabled. If you have not defined a custom Default ACG, they are placed in the built-in "No Rights" group, which prevents User Rights managers from granting them any privileges.

**Q: Can I disable ACGs temporarily and re-enable them later?**
Yes. The feature can be toggled at any time without affecting existing project rights. When re-enabled, enforcement resumes from the point of the next rights assignment or modification.

**Q: How do I bulk-reassign all users to a new ACG?**
Use the CSV export from the User Assignments tab, modify the ACG column in the exported file, and re-upload using the Upload user assignments (CSV) option. Review the proposed changes in the confirmation dialog before committing.

**Q: What is the difference between an ACG and a User Role?**
User Roles (defined within an individual project) are templates that specify what rights a user *will* have in that project. ACGs are a system-level ceiling that constrains what rights *can* be granted — they operate independently of roles. A User Role cannot grant rights that exceed the user's ACG, even if the role itself is defined with higher privileges.

---

## 12. Common Mistakes & Gotchas

**Enabling ACGs without first assigning users to appropriate groups.** The moment ACGs are enabled, all users are placed in the Default ACG. If that default is "No Rights" (the system default), User Rights managers across every project immediately lose the ability to add or modify users. Always create and populate your ACGs before enabling the feature, and set an appropriate default group.

**Not planning for non-compliant users in existing projects.** Existing rights are not automatically adjusted when ACGs are enabled. Projects with active users may immediately be out of compliance once the feature is on. Run a compliance review (using the Reports tab or per-project ACG Compliance page) as part of your rollout plan.

**Granting "Full Access" User Rights in an ACG too broadly.** Users whose ACG permits Full Access User Rights can manage all user privileges in every project they are added to. Reserve this level for researchers and coordinators who genuinely need it.

**Confusing ACGs with Data Access Groups (DAGs).** DAGs (configured within individual projects) restrict which *records* a user can see. ACGs (configured system-wide) restrict which *privileges* a user can be granted. They serve different purposes and operate independently. See [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) for DAG documentation.

**Forgetting to update ACG assignments when institutional roles change.** ACG assignments are static until manually changed. If a user's role or affiliation changes, their ACG assignment must be updated in the User Assignments tab (or via CSV import) to reflect their new privilege ceiling.

---

## 13. Related Articles

- [RC-CC-07 — Control Center: Users & Access Management](RC-CC-07_Control-Center-User-Management.md) (brief ACG overview and broader user management context)
- [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md) (user privilege concepts at project level)
- [RC-USER-02 — User Rights: Adding Users & Managing Roles](RC-USER-02_User-Rights-Adding-Users-and-Managing-Roles.md) (how users are added to projects; where ACG enforcement occurs)
- [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) (the full set of configurable user rights that ACGs control)
- [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) (record-level access restriction, distinct from ACGs)
