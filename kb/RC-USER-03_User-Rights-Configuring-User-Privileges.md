RC-USER-03

**User Rights — Configuring User Privileges**

| **Article ID** | RC-USER-03 |
|---|---|
| **Domain** | User Rights |
| **Applies To** | All REDCap project types; requires User Rights privilege |
| **Prerequisite** | RC-USER-01 — User Rights: Overview & Three-Tier Access |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-USER-02 — Adding Users & Managing Roles; RC-USER-04 — User Management; RC-DAG-01 — Data Access Groups; RC-EXPRT-01 — Data Export: Overview & Workflow |

---

# 1. Overview

This article explains every user rights setting available in the user privileges popup in REDCap — both the Basic Privileges panel and the per-instrument data rights settings. It also covers miscellaneous user rights that exist outside the main User Rights page, including report-level and dashboard-level access controls and smart-variable-based restrictions. The rights described here apply to individual users and to roles. See RC-USER-02 — Adding Users & Managing Roles for how to open the privileges popup.

---

# 2. Key Concepts & Definitions

**Basic Privileges**

The panel on the left side of the user privileges popup containing application-level and feature-level toggles. The options shown depend on which features are enabled in the project — REDCap hides options for disabled features.

**Data Viewing Rights**

Per-instrument settings that control whether a user can see and interact with data in a given instrument.

**Data Export Rights**

Per-instrument settings that control whether a user can export data from a given instrument, and at what level of de-identification.

**Expiration Date**

A date on which REDCap automatically suspends a user from the project. Optional. Set per user — it is not part of a role definition.

**Highest-Level Privileges**

Three settings — Project Design and Setup, User Rights, and Data Access Groups — that grant broad control over the project. Users with these rights can make structural or administrative changes that affect all users in the project.

**Record Locking**

A feature that prevents further edits to a completed instrument or record. Separate from standard data entry rights.

---

# 3. Basic Privileges

The Basic Privileges panel is shown on the left side of the user privileges popup. The available options vary based on which features are enabled in the project.

> **Note:** REDCap hides options that are not relevant to your project's configuration. For example, "Survey Distribution Tools" will not appear if surveys are not enabled.

## 3.1 Expiration Date

An optional date field, blank by default. If set, REDCap will automatically suspend the user from this project when that date arrives. The user's accounts and access to other projects are not affected.

This setting is most useful for temporary contributors such as students, interns, or contract staff. It prevents forgotten access from persisting after someone's involvement ends.

> **Note:** The expiration date is a per-user setting and cannot be pre-defined at the role level.

## 3.2 Highest-Level Privileges

These three settings give users broad administrative power within the project. Best practice is to limit them to one or two users — typically those actively building or managing the project.

- **Project Design and Setup** — grants the ability to modify project structure, including adding, editing, and removing variables; enabling or disabling project features; copying the project; and creating backups. Users with this right can change what the project collects and how it behaves.

- **User Rights** — grants access to the User Rights menu. A user with this right can modify any user's rights in the project, including their own. This is effectively a super-admin right for the project and should be assigned with care.

- **Data Access Groups** — grants access to the DAG management page, where the user can create, edit, and delete DAGs and assign users to them. See RC-DAG-01 — Data Access Groups.

## 3.3 Other Basic Privileges

Most of the remaining basic privileges either show or hide a specific application or feature in REDCap's interface. Hiding a feature cleans up the interface for users who do not need it and prevents unintended use.

Best practice is to grant access only to the features a user is actually expected to use.

Several options have additional behavior worth noting:

**Add/Edit/Organize Reports**

Grants the ability to create and manage reports and to see all reports in the project. If this option is disabled, the user may still have access to individual reports — each report has its own access controls that can grant visibility to specific users, roles, or DAGs independent of this privilege. See Section 6 for report-level rights.

**Manage MyCap Participants**

Grants access to the MyCap Participant Management page, including the ability to invite or add participants, send and view messages, and manage MyCap-related features. This right only appears if MyCap is enabled on the project, and MyCap may not be available at all institutions. PHI exposure: messages with participants may contain PHI.

**Data Quality**

Split into two separate rights:
- *Create & edit rules* — allows the user to write custom data quality rules.
- *Execute rules* — allows the user to run any rule defined in the project, including custom rules created by others. Users without form-level access to an instrument referenced in a rule will not see results for that instrument.

**Data Resolution Workflow**

Disabled by default in most projects and hidden unless the feature is enabled. When enabled, multiple options appear covering different levels of participation in the data query process (view only, respond to queries, open queries, close queries). The default is view-only. Any project using this feature must review and configure these settings for all users.

> **Tip:** If roles are in use, updating the role propagates the data resolution workflow settings to all users in that role simultaneously — you do not need to update each user individually.

**API**

Two separate rights:
- *API Export* — allows the user to pull data from REDCap programmatically via an API token.
- *API Import/Update* — allows the user to push data into REDCap via an API token.

> **Important:** API rights are scoped by the user's other rights. A user with API Export access can only export the data they would be able to export manually. Their API token does not grant additional access beyond their user rights configuration.

**Mobile App**

Two separate rights:
- *Use mobile app* — allows the user to use the REDCap mobile app with this project.
- *Download data for offline use* — allows the user to download project data to a mobile device for offline data collection.

If the mobile app is not part of your project's data collection workflow, leave both unchecked.

## 3.4 Record Settings

These three settings govern how a user can interact with records globally across the project.

- **Create records** — allows the user to create new records. Most users who do data entry will need this enabled.
- **Rename records** — allows the user to change the record ID of an existing record. This is rarely needed and carries risk: REDCap relies on the record ID to associate all data. Rename only with a clear purpose and caution.
- **Delete records** — allows the user to delete entire or partial records (all forms, all events, all repeating instances). Deleted records **cannot** be restored. Disabled by default to prevent accidental data loss. If deletion is needed, the recommended approach is to grant the right temporarily, perform the deletion, and remove the right again. Users with Delete Records automatically inherit Form-Level Delete for all instruments.
- **Form-Level Delete Rights** *(new in REDCap v15.7.0)* — allows deletion of data on specific instruments only, without deleting an entire record. This provides finer-grained control when you want a user to be able to remove data from one form (e.g., to correct a mis-entry) without risking accidental deletion of the entire record. Form-Level Delete rights are configured per instrument in the Data Viewing Rights section. Requirements: the user must have View & Edit access for the instrument; if the instrument is enabled as a survey, the user must also have Edit Survey Responses rights. This right may not appear at all institutions depending on local configuration or REDCap version.

## 3.5 Record Locking and E-Signatures

Record locking is useful for larger projects where completed instruments should be protected from further edits, or where a formal sign-off process is required.

- **Record locking customization** — grants access to the locking configuration page where the project's overall record locking behavior is defined.
- **Lock/unlock records (instrument level)** — the first two options allow locking and unlocking individual instruments in a record. The third option adds the ability to apply an e-signature, which requires the user to enter their password to confirm each lock or unlock action.
- **Lock/Unlock entire records** — grants the ability to lock or unlock a complete record (all instruments at once).

> **Note:** A user with locking rights can lock and unlock anything in the project — including instruments locked by other users. Plan your locking roles carefully.
>
> **Important:** The e-signature option requires password entry for every action and has known compatibility issues with certain SSO authentication methods. Confirm compatibility with your authentication setup before enabling it.

## 3.6 Administrator-Granted Rights

Certain advanced features — such as Clinical Data Pull or SMS texting integrations (Twilio, Mosio) — require an administrator to enable and in some cases to assign at the user level. These will appear in the privileges popup only if enabled for your installation.

> **Yale-specific:** [Describe which administrator-granted features are available at Yale and how users can request access — leave blank until confirmed with Yale REDCap support team]

---

# 4. Data Viewing Rights

The data viewing rights section controls what data a user can see, configured per instrument.

There are three access levels for each instrument:

| Level | Description |
|---|---|
| **No Access** | The entire instrument is hidden from the user. It will not appear during data entry or browsing. |
| **Read Only** | The user can see and navigate the instrument but cannot edit any data. |
| **View & Edit** | The user can both view and modify data in the instrument. This is the default. |

For instruments enabled as surveys, a fourth option appears:

| Level | Description |
|---|---|
| **Edit Survey Responses** | Allows the user to edit data that was entered via the survey interface. Without this right, survey responses are locked from editing through the project's data entry view. The user must manually put the survey into edit mode using a button on the instrument. Users without this right will not see that button. |

> **Note for longitudinal projects:** Data viewing rights apply at the instrument level across all events and repeating instances. A user with Read Only access to an instrument will have that restriction across every event and every repeating instance.

> **Best practice:** When a new instrument is added to the project, immediately review user rights and role configurations to ensure the new instrument has the correct access levels for all users.

---

# 5. Data Export Rights

The data export rights section controls what data a user can export out of REDCap, configured per instrument. These settings are independent of data viewing rights — it is possible for a user to have edit access to an instrument but be restricted from exporting its data, or vice versa.

> **Note:** This mismatch can be intentional. A common use case is allowing a user to view and enter data but preventing them from exporting a full or identified dataset.

There are four export access levels for each instrument:

| Level | Description |
|---|---|
| **No Access** | The user cannot export any data from this instrument. |
| **De-identified** | The user can export data with all identifier fields removed, all free-text fields removed, and all date/time fields removed. |
| **Remove Identifier Fields Only** | Similar to De-identified, but only designated identifier fields are stripped. Free-text and date/time fields are included. |
| **Full Data Set** | The user can export all data from this instrument without restriction. This is the default. The user can optionally apply de-identification settings during the export process. |

See RC-EXPRT-01 — Data Export: Overview & Workflow and RC-EXPRT-03 — Data Export: User Rights & Export Access for how export rights interact with the export workflow.

> **Note for longitudinal projects:** Like data viewing rights, export rights apply per instrument across all events and repeating instances.

> **Important — PHI exposure:** The "De-identified" and "Remove All Tagged Identifier Fields" export levels depend entirely on correct identifier tagging in the project design. If PHI fields have not been tagged as identifiers, they will appear in supposedly de-identified exports. Always mark all PHI fields as identifiers and restrict export access to Full Data Set only for users who genuinely need it. Once data is downloaded, the user is responsible for securing it according to institutional policies (e.g., HIPAA). Data Export Rights are independent of Data Viewing Rights — a user can have Full Data Set export rights even with Read Only viewing rights, or vice versa.

---

# 6. Miscellaneous User Rights

Beyond the User Rights page, REDCap has several other places where access is controlled for specific features.

## 6.1 Report-Level Access

Each custom report in REDCap has its own user rights section, accessible from the report's edit page. By default, all project users can view and edit reports (provided they have the "Add/Edit/Organize Reports" basic privilege). However, report-level rights allow much finer control:

- Access and edit rights can be restricted to specific users, specific roles, specific DAGs, or any combination.
- Users who lack the "Add/Edit/Organize Reports" basic privilege can still be granted access to individual reports through this mechanism.

To configure report-level rights:
1. Go to **Data Exports, Reports, and Stats**.
2. Find the report and click **Edit** in the management options column.
3. Scroll to Step 1 in the report editor.
4. Configure access and edit rights as needed.
5. Click **Save Report**.

## 6.2 Project Dashboard Access

Each Project Dashboard also has its own user rights section. By default, all project users can view dashboards. Only users with the "Project Design and Setup" privilege can create or edit dashboards.

Dashboard access can be restricted by user, role, DAG, or combinations.

To configure dashboard-level rights:
1. Find the **Add/Edit** link next to the Project Dashboards section in the left menu.
2. Find the dashboard and click **Edit**.
3. Scroll to the user access section.
4. Configure access as needed.
5. Click **Save Dashboard**.

## 6.3 Smart Variable–Based Access Restrictions

REDCap's "User" category of smart variables allows field-level or instrument-level visibility to be conditioned on the identity of the currently logged-in user. This goes beyond the instrument-level access controls in the standard user rights popup.

Smart variables in this category reflect properties of the logged-in user — their username, role, DAG, and so on. These variables can be used anywhere branching logic is accepted: on individual fields or in the Form Display Logic feature.

**Example:** To hide a specific field from a user with the username `test_user`, add this branching logic to that field:

```
[user_name]<>'test_user'
```

This approach is flexible but should be used deliberately. It creates implicit access rules that are not visible in the standard User Rights page, making the project harder to audit. Use it when standard user rights do not provide the granularity you need.

---

# 7. Common Questions

**Q: Some options don't appear in the user rights popup for my project — why?**

**A:** REDCap hides options for features that are not enabled in the project. For example, Survey Distribution Tools only appears if surveys are on, and the Mobile App options only appear if mobile app support is enabled. If you expect an option to be there and it isn't, the feature may need to be turned on under Project Setup.

**Q: Can a user see data they can't export, or export data they can't see?**

**A:** Both are possible. Data viewing rights and data export rights are set independently per instrument. This is intentional — a common policy is to allow data entry staff to view and edit data but restrict them from exporting it.

**Q: If a user has Full Data Set export rights but I want to restrict them to de-identified exports, do I need to change user rights?**

**A:** Not necessarily. A user with Full Data Set rights can still choose to export a de-identified version during the export process. The right only sets the maximum they are allowed — not what they must do. If you want to enforce de-identified exports, change their right to De-identified.

**Q: Does giving a user API Export rights give them access to data they can't see manually?**

**A:** No. API rights are scoped by the user's other rights. If a user doesn't have viewing rights for an instrument, they cannot export it via the API either.

**Q: What is the difference between "De-identified" and "Remove Identifier Fields Only" in export rights?**

**A:** "De-identified" removes identifier fields, all free-text fields, and all date/time fields. "Remove Identifier Fields Only" removes just the designated identifier fields but leaves free text and dates intact. The correct choice depends on your data governance requirements.

**Q: Can I use smart variables instead of standard user rights to control data access?**

**A:** Yes, but with caution. Smart variable–based restrictions are not visible in the standard User Rights page and require knowledge of branching logic to configure and audit. Use them when you need field-level granularity that standard rights cannot provide.

---

# 8. Common Mistakes & Gotchas

**Granting the User Rights privilege too broadly.** A user with the User Rights privilege can change anyone's rights in the project — including giving themselves any privilege they want. Treat this right like a project administrator role. Limit it to one or two users.

**Forgetting to review rights after adding a new instrument.** New instruments inherit no special access configuration. When you add an instrument, check the user rights for all users (or roles) to make sure the new instrument has the correct viewing and export access levels.

**Expecting the API to bypass user rights.** API rights are bounded by the user's other project rights. A user cannot use the API to access data or features their user rights would normally prevent.

**Not testing the e-signature feature before deploying it.** The e-signature option requires password input for every record locking action and has known compatibility issues with SSO authentication. Test thoroughly in Development before enabling on a Production project with real users.

**Setting export rights to Full Data Set by default without reviewing.** The default for data export rights is Full Data Set, meaning all users start with unrestricted export access. If your project handles sensitive data, actively review and restrict export rights to De-identified or No Access for users who should not have full export capability.

---

## API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See RC-API-01 — REDCap API for authentication, token management, and setup.

- **RC-API-22 — Export Users API** — retrieve a full list of users with their current privilege settings
- **RC-API-23 — Import Users API** — set or update user privileges programmatically using the same field names documented in this article

---


# 9. Related Articles

- RC-USER-01 — User Rights: Overview & Three-Tier Access
- RC-USER-02 — User Rights: Adding Users & Managing Roles
- RC-USER-04 — User Rights: User Management (editing, suspending, removing users)
- RC-DAG-01 — Data Access Groups
- RC-EXPRT-01 — Data Export: Overview & Workflow
- RC-EXPRT-03 — Data Export: User Rights & Export Access
