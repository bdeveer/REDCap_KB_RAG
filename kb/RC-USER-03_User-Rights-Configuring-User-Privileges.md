

**User Rights — Configuring User Privileges**

| **Article ID** | [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) |
|---|---|
| **Domain** | User Rights |
| **Applies To** | All REDCap project types; requires User Rights privilege |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.4.1 (Standard) / v17.3.7 (LTS) — changelog review; page not re-captured. Randomization rights and all other user privileges checked against source code of v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS). API import rights checked against source code of v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) |
| **Prerequisite** | [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md) |
| **Version** | 1.5 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-USER-02 — User Rights: Adding Users & Managing Roles](RC-USER-02_User-Rights-Adding-Users-and-Managing-Roles.md); [RC-USER-04 — User Rights: User Management](RC-USER-04_User-Rights-User-Management.md); [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md); [RC-EXPRT-01 — Data Export: Overview & Workflow](RC-EXPRT-01_Data-Export-Overview-and-Workflow.md); [RC-CC-25 — Control Center: Access Control Groups](RC-CC-25_Access-Control-Groups.md); [RC-RAND-01 — Randomization Concepts & Terminology](RC-RAND-01_Randomization-Concepts.md) |
| **Synonyms** | how do i configure user privileges; what does each user rights setting do; give a user export or import permissions; set per-instrument data access; restrict a user to view-only access; limit who can see reports or dashboards; configure permissions in the privileges popup; explain basic privileges settings; can the randomization dashboard right unblind users; what rights does a new user get by default; does the mobile app bypass export rights; why can't my users e-sign |

---

## 1. Overview

This article explains every user rights setting available in the user privileges popup in REDCap — both the Basic Privileges panel and the per-instrument data rights settings. It also covers miscellaneous user rights that exist outside the main User Rights page, including report-level and dashboard-level access controls and smart-variable-based restrictions. The rights described here apply to individual users and to roles. See [RC-USER-02 — User Rights: Adding Users & Managing Roles](RC-USER-02_User-Rights-Adding-Users-and-Managing-Roles.md) — Adding Users & Managing Roles for how to open the privileges popup.

---

## 2. Key Concepts & Definitions

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

## 3. Basic Privileges

The Basic Privileges panel is shown on the left side of the user privileges popup. The available options vary based on which features are enabled in the project.

> **Note:** REDCap hides options that are not relevant to your project's configuration. For example, "Survey Distribution Tools" will not appear if surveys are not enabled.

### 3.1 Expiration Date

An optional date field, blank by default. If set, REDCap will automatically suspend the user from this project when that date arrives. The user's accounts and access to other projects are not affected.

This setting is most useful for temporary contributors such as students, interns, or contract staff. It prevents forgotten access from persisting after someone's involvement ends.

> **Note:** The expiration date is a per-user setting and cannot be pre-defined at the role level.

### 3.2 Highest-Level Privileges

These three settings give users broad administrative power within the project. Best practice is to limit them to one or two users — typically those actively building or managing the project.

- **Project Design and Setup** — grants the ability to modify project structure, including adding, editing, and removing variables; enabling or disabling project features; copying the project; and creating backups. Users with this right can change what the project collects and how it behaves. While the project is in Development they can also erase all records and delete the project, so treat this right as carefully as User Rights.

- **User Rights** — grants access to the User Rights menu. It has three levels: **No Access**, **Read Only** (can see everyone's rights but cannot add users, change rights or assign roles) and **Full Access**. A user with Full Access can modify any user's rights in the project, including their own. This is effectively a super-admin right for the project and should be assigned with care. A User Rights manager who is assigned to a Data Access Group can only manage users in their own DAG.

- **Data Access Groups** — grants access to the DAG management page, where the user can create, edit, and delete DAGs and assign users to them. See [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md).

### 3.3 Other Basic Privileges

Most of the remaining basic privileges either show or hide a specific application or feature in REDCap's interface. Hiding a feature cleans up the interface for users who do not need it and prevents unintended use.

Best practice is to grant access only to the features a user is actually expected to use.

Several options have additional behavior worth noting:

**Add/Edit/Organize Reports**

Grants the ability to create and manage reports and to see all reports in the project. If this option is disabled, the user may still have access to individual reports — each report has its own access controls that can grant visibility to specific users, roles, or DAGs independent of this privilege. A user who has this privilege sees every report, whatever the report-level access settings say. See Section 6 for report-level rights.

**Manage MyCap Participants**

Grants access to the MyCap Participant Management page, including the ability to invite or add participants, send and view messages, and manage MyCap-related features. This right only appears if MyCap is enabled on the project, and MyCap may not be available at all institutions. PHI exposure: messages with participants may contain PHI.

**Data Quality**

Split into two separate rights:
- *Create & edit rules* — allows the user to write custom data quality rules.
- *Execute rules* — allows the user to run any rule defined in the project, including custom rules created by others. If a rule uses a field on an instrument the user has No Access to, the user cannot view the results for that rule at all; REDCap shows a message instead.

**Data Resolution Workflow**

Disabled by default in most projects and hidden unless the feature is enabled. When enabled, six options appear: No Access, View only, Respond only to opened queries, Open queries only, Open and respond to queries, and Open, close, and respond to queries. The default is view-only. Any project using this feature must review and configure these settings for all users.

> **Tip:** If roles are in use, updating the role propagates the data resolution workflow settings to all users in that role simultaneously — you do not need to update each user individually.

**API**

Two separate rights:
- *API Export* — allows the user to pull data from REDCap programmatically via an API token.
- *API Import/Update* — allows the user to push data into REDCap via an API token.

> **Important:** API rights are scoped by the user's other rights. API record exports follow the user's **Data Export Rights** (not their Data Viewing Rights): fields on instruments set to No Access for export are left out, and De-identified or Remove All Identifier Fields rights strip fields in the same way as a manual export. API imports are different: the **API Import/Update** right lets the token write to **any** instrument, including ones the user can only view or cannot see, and create new records even without **Create Records**. Only DAG restrictions and record locking still apply. Grant API Import/Update only to users who may edit every instrument. On the export side the one exception is the Mobile App right (below).

**Mobile App**

Two separate rights:
- *Use mobile app* — allows the user to use the REDCap mobile app with this project.
- *Download data for offline use* — allows the user to download project data to a mobile device for offline data collection.

> **Important — PHI exposure:** A user with the Mobile App right can download all data on every instrument through the app (which uses the API), whatever their Data Export Rights and API rights say. Their DAG still applies. Treat granting the Mobile App right as granting Full Data Set export, and do not rely on export rights or on leaving *Download data for offline use* unticked to limit what such a user can take off the server. REDCap shows a warning about this when you tick the right.

If the mobile app is not part of your project's data collection workflow, leave both unchecked.

**Randomization**

Three separate rights, shown only when randomization is enabled on the project. Each carries more exposure than its name suggests:
- *Setup* — define the randomization model and upload **and download** allocation tables. While the project is in Development, downloading a table reveals the full allocation sequence, including the production table prepared for go-live. In Production only an administrator can download the tables.
- *Dashboard* — view allocation progress (used / not used) per stratum, with the records in each. For an open model (dropdown or radio randomization variable) it also breaks this down by group. For a blinded model (text randomization variable) it never shows the group. A study that is meant to be blinded but uses an open variable **can be unblinded** through the dashboard.
- *Randomize* — randomize records from the form or survey. The randomization dialog shows the stratification fields with their current values **even without form-level rights** to those fields, so if a stratum is PHI (e.g., location), the user sees it regardless of Data Viewing Rights. Strata on instruments set to **No Access** are shown but can't be changed. Users with **Read Only** access to that instrument can set them in the dialog.

Enabling the module later in Project Setup grants none of the three rights to existing users, including the creator. The project creator gets all three only if **Randomization** was ticked when the project was created. Once randomization is enabled, the Add User popup pre-ticks **Randomize** (not Setup or Dashboard) for each new user added that way, so untick it for users who should not randomize. The **Randomization** link appears in the project menu only for users with Setup or Dashboard.

See [RC-RAND-01 — Randomization Concepts & Terminology](RC-RAND-01_Randomization-Concepts.md) for who should get each right.

### 3.4 Record Settings

These three settings govern how a user can interact with records globally across the project.

- **Create records** — allows the user to create new records. Most users who do data entry will need this enabled.
- **Rename records** — allows the user to change the record ID of an existing record. This is rarely needed and carries risk: REDCap relies on the record ID to associate all data. Rename only with a clear purpose and caution.
- **Delete records** — allows the user to delete entire or partial records (all forms, all events, all repeating instances). Deleted records **cannot** be restored. Disabled by default to prevent accidental data loss. If deletion is needed, the recommended approach is to grant the right temporarily, perform the deletion, and remove the right again. Users with Delete Records automatically inherit Form-Level Delete for all instruments.
- **Form-Level Delete Rights** *(new in REDCap v15.7.0)* — allows deletion of data on specific instruments only, without deleting an entire record. This provides finer-grained control when you want a user to be able to remove data from one form (e.g., to correct a mis-entry) without risking accidental deletion of the entire record. Form-Level Delete rights are configured per instrument in the Data Viewing Rights section. Requirements: the user must have View & Edit access for the instrument; if the instrument is enabled as a survey, the user must also have Edit Survey Responses rights in order to delete a response submitted through the survey interface. Granting it enables the **Delete Data** button at the bottom of the data entry form for those instruments.

> **Requires REDCap 15.7.0 or higher.** On earlier versions the only deletion privilege is Delete Records, which is all-or-nothing. If you do not see per-instrument Delete options in the Data Viewing Rights section, check your instance version before assuming a local configuration difference.

### 3.5 Record Locking and E-Signatures

Record locking is useful for larger projects where completed instruments should be protected from further edits, or where a formal sign-off process is required.

- **Record locking customization** — grants access to the locking configuration page where the project's overall record locking behavior is defined.
- **Lock/unlock records (instrument level)** — three options: **No Access**; **Locking / Unlocking**, which allows locking and unlocking individual instruments in a record; and **Locking / Unlocking with E-signature authority**, which adds the ability to e-sign, confirmed by re-entering credentials. Granting e-signature authority does not switch the e-signature on: it must also be enabled per instrument (**Display E-signature Option**) on the Record Locking Customization page.
- **Lock/Unlock entire records** — grants the ability to lock or unlock a complete record (all instruments at once).

> **Note:** A user with locking rights can lock and unlock anything in the project — including instruments locked by other users. Plan your locking roles carefully.
>
> **Important:** E-signing requires REDCap to re-check the user's identity, so it is only available when the administrator has enabled e-signatures for the installation and one of these applies:
> - REDCap uses table-based, LDAP or LDAP/table-based authentication (or no authentication), or the user has a table-based account;
> - REDCap uses Shibboleth and the administrator has configured Shibboleth for e-signatures;
> - two-factor authentication is on with the option to e-sign using a 2FA PIN, which works with any authentication method.
>
> Otherwise (for example, OAuth2, or Shibboleth without the e-signature configuration and no 2FA PIN) users cannot e-sign. Certain external modules also provide alternative e-signature workflows. Contact your REDCap administrator to find out which applies at your institution.

### 3.6 Administrator-Granted Rights

Certain advanced features — such as Clinical Data Pull or SMS texting integrations (Twilio, Mosio) — require an administrator to enable and in some cases to assign at the user level. These will appear in the privileges popup only if enabled for your installation.

> **Institution-specific:** The features available through administrator-granted access vary by installation. Contact your REDCap administrator to learn which elevated permissions are available and how to request them.

### 3.7 Default Rights for New Users and the Project Creator

**Users added in the Add User popup** start with these rights ticked: Create Records, Add/Edit/Organize Reports, Stats & Charts, Calendar, File Repository, Survey Distribution Tools and Manage MyCap Participants (where those features are on), plus Randomize if randomization is enabled. Data Resolution Workflow starts at view only. Everything else, including the highest-level privileges, API, record deletion and locking, starts off. Instrument-level defaults depend on project status:

- **Development:** View & Edit and Full Data Set export on every instrument, plus Edit Survey Responses on survey instruments where your administrator allows it.
- **Production:** **No Access** for both Data Viewing and Data Export on every instrument. Set instrument rights before the user starts work, or they will see no forms.

Users added through the API or a user CSV upload get only the rights included in the upload; anything left out is off.

**The project creator** gets full rights: User Rights, Project Design and Setup, Data Access Groups, View & Edit and Full Data Set export on every instrument, and most other privileges. A few start switched off: Delete Records, Rename Records, record locking, API Export and Import, and Edit Survey Responses. Because the creator holds the User Rights privilege, they can switch these on for themselves in User Rights when needed. Randomization rights are included only if Randomization was ticked at creation, and Mobile App rights only if the mobile app and API are enabled for the installation.

---

## 4. Data Viewing Rights

The data viewing rights section controls what data a user can see, configured per instrument.

There are three access levels for each instrument:

| Level | Description |
|---|---|
| **No Access** | The entire instrument is hidden from the user. It will not appear during data entry or browsing. |
| **Read Only** | The user can see and navigate the instrument but cannot edit any data. |
| **View & Edit** | The user can both view and modify data in the instrument. This is the default for new users while the project is in Development (see Section 3.7 for Production). |

For instruments enabled as surveys, an extra option appears (if your administrator allows it): an **Edit Survey Responses** checkbox that goes with View & Edit. In Development it is ticked by default for new users.

| Option | Description |
|---|---|
| **Edit Survey Responses** | Allows the user to edit data that was entered via the survey interface. Without this right, survey responses are locked from editing through the project's data entry view. The user must manually put the survey into edit mode using a button on the instrument. Users without this right will not see that button. |

> **Note for longitudinal projects:** Data viewing rights apply at the instrument level across all events and repeating instances. A user with Read Only access to an instrument will have that restriction across every event and every repeating instance.

> **Best practice:** REDCap adds every new instrument to all users and roles automatically. In Development they get View & Edit and Full Data Set export on it. In Production (instruments added in Draft Mode) they get whatever a Control Center setting specifies: No Access, View & Edit with Full Data Set export (the default) or View & Edit with De-identified export. An Access Control Group can lower this. So the risk is over-granting, not under-granting: review user rights and role configurations immediately after adding an instrument, especially one that collects PHI.

---

## 5. Data Export Rights

The data export rights section controls what data a user can export out of REDCap, configured per instrument. These settings are independent of data viewing rights — it is possible for a user to have edit access to an instrument but be restricted from exporting its data, or vice versa.

> **Note:** This mismatch can be intentional. A common use case is allowing a user to view and enter data but preventing them from exporting a full or identified dataset.

There are four export access levels for each instrument:

| Level | Description |
|---|---|
| **No Access** | The user cannot export any data from this instrument. |
| **De-identified** | Identifier fields, unvalidated text fields, notes fields and date/datetime fields are removed. Text fields with validation (other than dates) and time fields are kept. On the Data Exports page the user may shift dates instead of removing them. |
| **Remove All Identifier Fields** | Similar to De-identified, but only designated identifier fields are stripped. Free-text and date/time fields are included. |
| **Full Data Set** | The user can export all data from this instrument without restriction. This is the default for new users while the project is in Development; in Production new users start with No Access (see Section 3.7). The user can optionally apply de-identification settings during the export process. |

See [RC-EXPRT-01 — Data Export: Overview & Workflow](RC-EXPRT-01_Data-Export-Overview-and-Workflow.md) and [RC-EXPRT-03 — Data Export: User Rights & Export Access](RC-EXPRT-03_Data-Export-User-Rights-and-Export-Access.md) for how export rights interact with the export workflow.

> **Note for longitudinal projects:** Like data viewing rights, export rights apply per instrument across all events and repeating instances.

> **Important — PHI exposure:** The "De-identified" and "Remove All Identifier Fields" export levels depend entirely on correct identifier tagging in the project design. If PHI fields have not been tagged as identifiers, they will appear in supposedly de-identified exports. Always mark all PHI fields as identifiers and restrict export access to Full Data Set only for users who genuinely need it. Once data is downloaded, the user is responsible for securing it according to institutional policies (e.g., HIPAA). Data Export Rights are independent of Data Viewing Rights — a user can have Full Data Set export rights even with Read Only viewing rights, or vice versa.

---

## 6. Miscellaneous User Rights

Beyond the User Rights page, REDCap has several other places where access is controlled for specific features.

### 6.1 Report-Level Access

Each custom report in REDCap has its own user rights section, accessible from the report's edit page. By default, all project users can view and edit reports (provided they have the "Add/Edit/Organize Reports" basic privilege). However, report-level rights allow much finer control:

- Access and edit rights can be restricted to specific users, specific roles, specific DAGs, or any combination.
- Users who lack the "Add/Edit/Organize Reports" basic privilege can still be granted access to individual reports through this mechanism.

To configure report-level rights:
1. Go to **Data Exports, Reports, and Stats**.
2. Find the report and click **Edit** in the management options column.
3. Scroll to Step 1 in the report editor.
4. Configure access and edit rights as needed.
5. Click **Save Report**.

### 6.2 Project Dashboard Access

Each Project Dashboard also has its own user rights section. By default, all project users can view dashboards. Only users with the "Project Design and Setup" privilege can create or edit dashboards.

Dashboard access can be restricted by user, role, DAG, or combinations.

To configure dashboard-level rights:
1. Find the **Add/Edit** link next to the Project Dashboards section in the left menu.
2. Find the dashboard and click **Edit**.
3. Scroll to the user access section.
4. Configure access as needed.
5. Click **Save Dashboard**.

### 6.3 Smart Variable–Based Access Restrictions

REDCap's "User" category of smart variables allows field-level or instrument-level visibility to be conditioned on the identity of the currently logged-in user. This goes beyond the instrument-level access controls in the standard user rights popup.

Smart variables in this category reflect properties of the logged-in user — their username, role, DAG, and so on. These variables can be used anywhere branching logic is accepted: on individual fields or in the Form Display Logic feature.

**Example:** To hide a specific field from a user with the username `test_user`, add this branching logic to that field:

```
[user-name]<>'test_user'
```

> **Important:** Branching logic and Form Display Logic only hide things on screen. They are not access controls: the hidden data still appears in reports, exports and the API according to the user's Data Viewing and Data Export Rights. Use instrument-level rights for anything that must stay confidential.

This approach is flexible but should be used deliberately. It creates implicit access rules that are not visible in the standard User Rights page, making the project harder to audit. Use it when standard user rights do not provide the granularity you need.

---

## 7. Common Questions

**Q: Some options don't appear in the user rights popup for my project — why?**

**A:** REDCap hides options for features that are not enabled in the project. For example, Survey Distribution Tools only appears if surveys are on, and the Mobile App options only appear if your administrator has enabled the mobile app and the API for the installation. If you expect an option to be there and it isn't, the feature may need to be turned on under Project Setup, or (for system-level features such as the Mobile App and API) by your administrator.

**Q: Can a user see data they can't export, or export data they can't see?**

**A:** Both are possible. Data viewing rights and data export rights are set independently per instrument. This is intentional — a common policy is to allow data entry staff to view and edit data but restrict them from exporting it.

**Q: If a user has Full Data Set export rights but I want to restrict them to de-identified exports, do I need to change user rights?**

**A:** Not necessarily. A user with Full Data Set rights can still choose to export a de-identified version during the export process. The right only sets the maximum they are allowed — not what they must do. If you want to enforce de-identified exports, change their right to De-identified.

**Q: Does giving a user API Export rights give them access to data they can't see manually?**

**A:** No. API exports follow the user's Data Export Rights, not their viewing rights: if a user has No Access export rights for an instrument, the API leaves that instrument's fields out, and De-identified rights strip fields as in a manual export. The exception is the Mobile App right, which lets the user download all data on every instrument through the app (DAG restrictions still apply).

**Q: What is the difference between "De-identified" and "Remove All Identifier Fields" in export rights?**

**A:** "De-identified" removes identifier fields, unvalidated text and notes fields, and date/datetime fields (time fields and validated text fields stay). "Remove All Identifier Fields" removes just the designated identifier fields but leaves free text and dates intact. The correct choice depends on your data governance requirements.

**Q: Can I use smart variables instead of standard user rights to control data access?**

**A:** Yes, but with caution. Smart variable–based restrictions are not visible in the standard User Rights page and require knowledge of branching logic to configure and audit. Use them when you need field-level granularity that standard rights cannot provide.

---

## 8. Common Mistakes & Gotchas

**Granting the User Rights privilege too broadly.** A user with the User Rights privilege can change anyone's rights in the project — including giving themselves any privilege they want. Treat this right like a project administrator role. Limit it to one or two users.

**Forgetting to review rights after adding a new instrument.** REDCap gives every user and role access to a new instrument automatically: View & Edit and Full Data Set export in Development, and the Control Center default (usually the same) in Production. When you add an instrument, check the user rights for all users (or roles) to make sure the new instrument has the correct viewing and export access levels.

**Expecting the API to bypass user rights.** API rights are bounded by the user's other project rights; record exports follow Data Export Rights. For reading data, a user cannot use the API to get more than their rights allow, except through the Mobile App right, which gives full data download through the app. For writing data it is the other way round: API Import/Update lets a token write to any instrument and create records, so grant it only to users who may edit every instrument.

**Planning on e-signatures without checking your authentication method.** E-signing needs REDCap to re-check the user's credentials. It works with table-based and LDAP logins, with Shibboleth only if your administrator has configured it for e-signatures, and with any login method if two-factor authentication with a 2FA PIN for e-signing is on. Confirm with your REDCap administrator before building a sign-off process around it; certain external modules provide alternative e-signature workflows.

**Setting export rights to Full Data Set by default without reviewing.** While the project is in Development, the default for data export rights is Full Data Set, meaning users added then start with unrestricted export access (and keep it when the project moves to Production). If your project handles sensitive data, actively review and restrict export rights to De-identified or No Access for users who should not have full export capability.

---

### API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) for authentication, token management, and setup.

- **[RC-API-22 — Export Users API](RC-API-22_Export-Users.md)** — retrieve a full list of users with their current privilege settings
- **[RC-API-23 — Import Users API](RC-API-23_Import-Users.md)** — set or update user privileges programmatically using the same field names documented in this article

---


## 9. Related Articles

- [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md)
- [RC-USER-02 — User Rights: Adding Users & Managing Roles](RC-USER-02_User-Rights-Adding-Users-and-Managing-Roles.md)
- [RC-USER-04 — User Rights: User Management](RC-USER-04_User-Rights-User-Management.md) (editing, suspending, removing users)
- [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md)
- [RC-RAND-01 — Randomization Concepts & Terminology](RC-RAND-01_Randomization-Concepts.md) (who should get the Setup, Dashboard and Randomize rights)
- [RC-CC-25 — Control Center: Access Control Groups](RC-CC-25_Access-Control-Groups.md) (system-level ceiling on the privileges documented in this article; if a right appears unavailable when assigning a user, the user's ACG may be restricting it)
- [RC-EXPRT-01 — Data Export: Overview & Workflow](RC-EXPRT-01_Data-Export-Overview-and-Workflow.md)
- [RC-EXPRT-03 — Data Export: User Rights & Export Access](RC-EXPRT-03_Data-Export-User-Rights-and-Export-Access.md)
