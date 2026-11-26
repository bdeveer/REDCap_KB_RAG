---
id: RC-DAG-01
title: Data Access Groups
domain: Data Access Groups
applies_to:
- All REDCap project types
- requires Data Access Groups privilege to manage
requires: Any supported version
verified_against: REDCap v17.5.4 (Standard) / v17.3.18 (LTS) — changelog review; page
  not re-captured. DAG behaviour checked against source code of v17.6.5 (Standard)
  / v17.3.31 and v16.0.61 (LTS)
prerequisites:
- 'RC-USER-01 — User Rights: Overview & Three-Tier Access'
version: '1.3'
last_updated: 2026-11
related:
- id: RC-USER-01
  title: 'User Rights: Overview & Three-Tier Access'
- id: RC-USER-02
  title: 'User Rights: Adding Users & Managing Roles'
- id: RC-USER-03
  title: 'User Rights: Configuring User Privileges'
- id: RC-USER-04
  title: 'User Rights: User Management'
- id: RC-EXPRT-03
  title: 'Data Export: User Rights & Export Access'
- id: RC-RAND-01
  title: Randomization Concepts & Terminology
- id: RC-CC-25
  title: 'Control Center: Access Control Groups'
- id: RC-NAV-UI-02
  title: Project Menu Reference
- id: RC-NAV-REC-04
  title: Record Status Dashboard & Other Record Links
tags:
- data access groups
synonyms:
- how do i set up data access groups
- restrict users to only see their own records
- separate sites in a multi-site study
- create and manage dags in redcap
- assign users to a data access group
- partition records by group
- hide records from other study sites
- what is a dag and how does it work
---

> **Important — DAG isolation is an application-layer control that has needed patching.** DAGs are presented throughout this article as a data-separation boundary, and on a current instance they are. But the boundary has leaked in six separate places, each fixed individually: a DAG user could **modify data outside their DAG** on data entry forms via a crafted request (fixed 15.5.37); **calendar events** were reachable across DAGs (15.5.38); and three groups of API methods returned survey links, access codes, queue links and return codes for records **outside the caller's DAG** (16.0.28, and 17.1.0 Standard / 16.0.31 LTS). The User Rights page also misbehaved for DAG-assigned users holding User Rights privileges (16.0.18). A sixth gap concerned DAG *administration*: some DAG setup actions did not check the **Data Access Groups** privilege, so authenticated users without it could perform them — present in all versions, fixed in 17.5.1 Standard / 17.3.14 LTS / 16.0.52 LTS.
>
> None of these were misconfigurations — the DAG assignment was correct and REDCap returned the data anyway. If your institution relies on DAG separation for a compliance argument, that argument is only as strong as the patch level. See [RC-INFRA-03 — REDCap Versions, Release Lines & Patching](RC-INFRA-03_REDCap-Versions-Release-Lines-and-Patching.md) and [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) §9a.

# 1. Overview

This article explains Data Access Groups (DAGs) — what they are, how they restrict record-level access, how to create and manage them, and how to assign users. DAGs are a feature for projects where different groups of users should only see their own records, such as multi-site studies where each site's staff should be separated from the others.

> **Not to be confused with Project Administrator Groups (PAGs).** DAGs are a **project-level** feature controlling **which records a user can see**. PAGs are a **system-level** REDCap+ feature (17.1.0+) controlling **who receives administrative requests** for a set of projects — production status changes, draft approvals and other project requests. The names are similar and REDCap's own 17.1.0 release notes contain a typo saying "DAG" where they mean "PAG". See [RC-PLUS-04 — REDCap+: Project Administrator Groups (PAGs)](RC-PLUS-04_Project-Administrator-Groups.md).

---

# 2. Key Concepts & Definitions

**Data Access Group (DAG)**

A named project-level grouping that restricts which records a user can see and interact with. A user assigned to a DAG can only access records that belong to that DAG. Users not assigned to any DAG can access all records.

**DAG Assignment (Record)**

The DAG that a record belongs to. A record is assigned to a DAG automatically when it is created by a user who is in a DAG. A user who is **not** in a DAG can set or change a record's DAG, and this does not need the Data Access Groups right:

- on the **Record Home Page**, with the **Assign to Data Access Group** option;
- with the DAG dropdown shown on the first instrument when creating a new record;
- by data import, using the `redcap_data_access_group` column.

DAG-assigned users cannot use any of these to move a record to another DAG.

**DAG Assignment (User)**

The DAG a user is assigned to in a given project. A user is in at most one DAG at any moment. The DAG Switcher lets a user move between several DAGs, but it does this by changing that single assignment; there is no separate "primary" DAG.

**DAG Switcher**

A feature on the DAG management page that lists, for each user, the DAGs they are allowed to switch into. The user works in one DAG at a time and sees only the records of the DAG they are currently in.

**DAG Management Privilege**

A user right ("Data Access Groups") that grants access to the DAG management page, where DAGs are created, renamed and deleted and users are assigned. It does **not** widen record access: a user who holds this right but is assigned to a DAG still sees only their own DAG's records, and cannot open the DAG page at all. Only users who are not in a DAG can use the DAG page.

A user with the **User Rights** privilege who is not in a DAG can also set another user's DAG in the user or role popups on the User Rights page without holding the Data Access Groups right (see §5.2).

---

# 3. How DAGs Work

A DAG controls record-level access within a project. The key behavior:

- When a user assigned to a DAG **creates a new record**, that record is automatically associated with the user's DAG.
- When a user assigned to a DAG **navigates the project**, they can only see records belonging to their DAG.
- **Users with no DAG assignment** can see all records, regardless of which DAG those records belong to.
- **The "Data Access Groups" user right does not change record visibility.** A DAG-assigned user with this right still sees only their DAG's records. Cross-DAG access comes only from being unassigned (all records) or from the DAG Switcher (one DAG at a time).
- **REDCap administrators ignore DAGs** in the interface and the API and see all records, even if assigned to a DAG.
- **Auto-numbered records created by a DAG user** get the DAG's numeric group ID as a prefix, for example `98-1`, `98-2`.

DAG restrictions also reach beyond the record lists. For a DAG-assigned user:

| Area | What the user sees |
|---|---|
| **Logging** | Events on records in their own DAG, plus non-record events by users in the same DAG. The user filter lists only same-DAG users. |
| **Calendar** | Entries for records in their own DAG, plus entries not attached to a record. |
| **File Repository** | Folders with no DAG restriction plus folders restricted to their own DAG. Data export files are listed only if created by users in the same DAG. |
| **Data exports and API exports** | Only their DAG's records. The `redcap_data_access_group` column is included only for users not in a DAG. |
| **Data import** | They cannot import into existing records outside their DAG; new records they import go into their DAG. |
| **Reports and dashboards** | Reports and project dashboards can be restricted to selected DAGs in their access settings. |
| **User Rights page** | A user with User Rights privileges who is in a DAG sees and edits only users in their own DAG, and users they add go into their DAG. |

DAGs operate independently of instrument-level user rights (data viewing rights and data export rights). Both layers apply simultaneously: a user's DAG restricts which records they can see, and their data viewing/export rights restrict what they can see within those records.

> **Note:** DAGs control record access, not instrument access or feature access. They do not replace or substitute for the standard user rights configuration.

---

# 4. Setting Up DAGs

## 4.1 Accessing the DAG Page

The DAG management page can be accessed in two ways:

- From the **Applications menu**, click **DAGs**.
- From the **User Rights page**, click the **Data Access Group** tab.

## 4.2 Creating a DAG

1. On the DAG page, type a name for the new group in the **"Enter new group name"** text box.
2. Click **+ Add Group**.
3. The new DAG will appear in the table below.

For creating many DAGs at once, use the **Upload or download DAGs/User-DAG assignments** button on the DAG page to upload a structured file.

**Unique group name.** REDCap derives each DAG's unique group name (the one used in `[record-dag-name]`, `[user-dag-name]`, imports and the API) from its current label: characters other than letters, numbers and spaces are removed, spaces become underscores, the result is lowercased and cut to 18 characters. If two DAGs produce the same name, REDCap adds a letter suffix (`b`, `c`, `d`…) in DAG order. Because the name is recalculated from the label:

- **renaming a DAG's label changes its unique name**;
- **deleting a DAG can change the suffix of another DAG** whose name collided with it.

Check the unique names on the DAG page after renaming or deleting any DAG (see §9).

## 4.3 Deleting a DAG

Click the red **X** in the "Delete group" column next to the DAG you want to remove.

> **Important:** On the DAG page, REDCap will not delete a DAG that still has **records**, **users** or **roles** assigned to it, or that has a **File Repository** folder restricted to it. It also blocks deletion of a DAG used for randomization by DAG. Reassign or remove these first.

> **Critical — deleting through the API is not blocked.** The **Delete DAGs** API method does none of these checks. When a DAG is deleted through the API:
> - users who were in it become **unassigned and can then see all records**;
> - File Repository folders restricted to that DAG are **deleted**;
> - randomization allocations tied to that DAG lose their DAG;
> - its records are left pointing at a DAG that no longer exists.
>
> Before deleting a DAG through the API, reassign its users and records to another DAG (and move any restricted File Repository content) exactly as the interface would require.

---

# 5. Assigning Users to a DAG

There are several ways to assign a user to a single DAG.

## 5.1 From the DAG Page

1. On the DAG page, in the **"Assign user to a group"** section, select the user from the **Select user** dropdown.
   > **Note:** Only users who have already been added to the project appear in this list.
2. Select the target DAG from the dropdown to the right of the user dropdown. The dropdown will show the user's current DAG assignment (or "no assignment").
3. Click **Assign**.

## 5.2 From the User Rights Page

A user can also be assigned to a DAG from within the User Rights menu, in any of three ways:

1. **Through the individual user privileges popup** — the popup includes a DAG dropdown at the bottom.
2. **When adding a user directly to a role** — the Role assignment popup includes an optional DAG assignment step.
3. **By clicking the DAG cell in the user rights table** — each user in the table has a DAG column; clicking it opens an assignment prompt.

Options 1 and 2 need only the **User Rights** privilege (and the user doing it must not be in a DAG); only option 3 needs the **Data Access Groups** right. If someone should not decide site membership, do not give them User Rights privileges while they are DAG-unassigned.

---

# 6. Multi-DAG Access (DAG Switcher)

If a user needs access to records across multiple DAGs — for example, a monitor who oversees two sites — use the DAG Switcher feature on the DAG page.

1. On the DAG page, scroll to the **DAG Switcher** section.
2. Check the box for each user/DAG combination you want to enable.

The DAG Switcher lists the DAGs a user may switch into. Switching **replaces** the user's single DAG assignment: while in a DAG they see only that DAG's records, and new records they create go into it. There is no "primary" DAG to return to; the user is simply in whichever DAG they last switched to. Other points:

- The user's current DAG must also be ticked in their switcher list.
- The switcher banner is not shown on record pages; the user switches from other project pages.
- Administrators see all records regardless of the switcher.

See [RC-DE-09 — Data Entry with DAGs](RC-DE-09_Data-Entry-with-DAGs.md) §4 for the full switching workflow.

> **Important — "[No Assignment]" in the switcher means all records.** **[No Assignment]** can be ticked as a switcher option. A user who has it can switch to being unassigned and then sees every record in the project. Tick it only for users who are meant to have project-wide access.

> **Note:** The **Upload or download DAGs/User-DAG assignments** function sets only each user's single DAG assignment (one row per user; duplicate users are rejected). It cannot manage DAG Switcher lists, which are set on the DAG page.

---

# 7. Bulk DAG Management

The **Upload or download DAGs/User-DAG assignments** button on the DAG page allows you to:

- **Download** the current DAG setup and all user-DAG assignments as structured files.
- **Upload** modified files to create DAGs or update each user's single DAG assignment in bulk. DAG Switcher lists are not included.

This is useful for initial project setup with many sites or for migrating a DAG structure from another project.

---

# 8. Common Questions

**Q: What does a DAG restrict exactly?**

**A:** A DAG restricts which records a user can see and interact with. A user in a DAG sees only records that belong to that DAG. It does not affect which instruments, features, or applications a user can access — those are governed by standard user rights.

**Q: Can a user be in more than one DAG at the same time?**

**A:** No. A user is in one DAG at any moment. If they need records in several DAGs, add those DAGs to their DAG Switcher list; they then switch between them and see one DAG's records at a time. Switching changes their DAG assignment.

**Q: What happens to records when a DAG is deleted?**

**A:** On the DAG page, REDCap will not delete a DAG that still has records, users, roles or a restricted File Repository folder. The **Delete DAGs** API method does not check: its users become unassigned (seeing all records), its restricted File Repository folders are deleted, and its records are left pointing at a DAG that no longer exists. Reassign users and records before deleting through the API.

**Q: If I add a user to a project without assigning them to a DAG, what records can they see?**

**A:** All records. Users with no DAG assignment have unrestricted record-level access across the project. This is intentional — it supports roles like project coordinators or data managers who need to see everything.

**Q: Does a user's DAG assignment affect what data they can export?**

**A:** Yes. Data export rights and DAG assignment both constrain what a user can export. A user in a DAG can only export records belonging to that DAG, and within those records, only the instruments their export rights allow. See [RC-EXPRT-03 — Data Export: User Rights & Export Access](RC-EXPRT-03_Data-Export-User-Rights-and-Export-Access.md).

**Q: Can a user create records in a DAG other than their own?**

**A:** No. When a DAG-assigned user creates a record, it is automatically assigned to their current DAG, and holding the Data Access Groups right does not change this. A user with the DAG Switcher can switch to another DAG first; records they then create go into that DAG. Only users not in a DAG can choose a record's DAG at creation or move it afterwards.

**Q: Do DAGs interact with randomization?**

**A:** Yes. DAG membership can affect randomization access — specifically which DAG a randomized record is associated with and who can view or perform randomization. See [RC-RAND-01 — Randomization Concepts & Terminology](RC-RAND-01_Randomization-Concepts.md) for details.

---

# 9. Common Mistakes & Gotchas

**Adding a user to a project without assigning a DAG when they should have one.** A user without a DAG assignment sees all records. For multi-site or restricted-access projects, always verify DAG assignment at the time of user addition. Review the user list regularly to confirm all users have the correct DAG configuration.

**Trying to delete a DAG that still has records.** The DAG page blocks this, and also blocks deletion while users, roles or a restricted File Repository folder are assigned. If the goal is to remove a site from the project, reassign or delete those records and users first. Plan ahead when retiring a site, and take extra care with the **Delete DAGs** API method, which does not block deletion (see §4.3).

**Giving the Data Access Groups right to a site user and expecting it to show all sites.** The right does not widen record access. A DAG-assigned user with it still sees only their own DAG and cannot open the DAG page. Give cross-site access through the DAG Switcher instead.

**Ticking [No Assignment] in a user's DAG Switcher list.** This lets the user switch to unassigned and see every record. Tick it only for users meant to have project-wide access.

**Confusing DAGs with Access Control Groups (ACGs).** These are separate, unrelated features. DAGs restrict which *records* a user can see within a project. ACGs (a system-level Control Center feature) restrict which *user privileges* can be granted to a user across all projects. A user can be subject to both simultaneously — their ACG caps what rights they can be given, and their DAG assignment caps which records they can access. See [RC-CC-25 — Control Center: Access Control Groups](RC-CC-25_Access-Control-Groups.md).

**Assuming DAG assignment controls instrument or feature access.** DAGs only restrict records — not instruments, features, or applications. A user in a DAG still has whatever instrument-level and feature-level rights are configured for them in User Rights.

**Overlooking the DAG Switcher for monitoring roles.** Monitors, auditors, or cross-site coordinators often need access to records across multiple sites. The DAG Switcher is the correct tool for this — not making them DAG-unassigned.

**Not accounting for DAGs when setting up export rights.** Because DAGs further restrict which records can be exported, a user's effective export scope is the intersection of their export rights and their DAG. Test export behavior with representative DAG-assigned user accounts to confirm the results match expectations.

**Using DAG names in branching logic without treating them as frozen.** In multi-site projects it is common to reference `[record-dag-name]` or `[user-dag-name]` in branching logic to show or hide site-specific fields (e.g., a consent section required at one site but not others). This is a legitimate pattern, but the DAG's unique name must then be treated as immutable for the life of the project. The unique name is the lowercase identifier (spaces become underscores, at most 18 characters) that REDCap recalculates from the DAG's current label, so renaming the label changes it, and deleting one DAG can change the suffix of another DAG with a similar name (see §4.2). Renaming or deleting a DAG that is referenced in branching logic silently breaks every condition that references it: the field becomes permanently hidden or permanently visible with no error message. Before renaming a DAG, search the data dictionary for every occurrence of its name in branching logic, calculated fields, and action tags, and update all references at the same time. If a project uses DAG-based branching across many fields, maintain a site configuration document that lists each DAG name, the fields it controls, and the intended behaviour — this makes change impact assessment practical.

**Hardcoding site-specific branching across too many fields.** Centralising multi-site variation in branching logic rather than separate instruments is efficient up to roughly five or six sites. Beyond that, the number of fields with DAG-conditional logic becomes difficult to audit, and adding a new site requires modifying many fields rather than a simple configuration change. If site expansion is anticipated, consider whether site-specific requirements can be harmonised at the protocol level, or document all DAG-conditional fields explicitly so the scope of any future change is clear before it is made.

---

## API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) for authentication, token management, and setup.

- **[RC-API-28 — Export DAGs API](RC-API-28_Export-DAGs.md)** — retrieve all DAG definitions (unique names and labels)
- **[RC-API-29 — Import DAGs API](RC-API-29_Import-DAGs.md)** — create or update DAG definitions programmatically
- **[RC-API-30 — Delete DAGs API](RC-API-30_Delete-DAGs.md)** — remove DAG definitions programmatically
- **[RC-API-31 — Export User-DAG Assignments API](RC-API-31_Export-User-DAG-Assignments.md)** — retrieve which users are assigned to which DAGs
- **[RC-API-32 — Import User-DAG Assignments API](RC-API-32_Import-User-DAG-Assignments.md)** — assign users to DAGs programmatically
- **[RC-API-33 — Switch DAG API](RC-API-33_Switch-DAG.md)** — change the active DAG context for the API token user

The Import DAGs and Delete DAGs methods need the **Data Access Groups** right on the token's user; unlike the DAG page, they do not require that user to be DAG-unassigned. The Delete DAGs method does not run the interface's safety checks — reassign the DAG's users and records before calling it (see §4.3).

---


# 10. Related Articles

- [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md)
- [RC-USER-02 — User Rights: Adding Users & Managing Roles](RC-USER-02_User-Rights-Adding-Users-and-Managing-Roles.md) (DAG assignment when adding users)
- [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) (DAG management privilege and other rights)
- [RC-USER-04 — User Rights: User Management](RC-USER-04_User-Rights-User-Management.md)
- [RC-CC-25 — Control Center: Access Control Groups](RC-CC-25_Access-Control-Groups.md) (system-level privilege ceiling, distinct from DAGs — ACGs restrict what rights a user can be granted; DAGs restrict which records they can see)
- [RC-EXPRT-03 — Data Export: User Rights & Export Access](RC-EXPRT-03_Data-Export-User-Rights-and-Export-Access.md) (how DAGs affect exports)
- [RC-RAND-01 — Randomization Concepts & Terminology](RC-RAND-01_Randomization-Concepts.md) (DAGs and randomization)
- [RC-NAV-UI-02 — Project Menu Reference](RC-NAV-UI-02_Project-Menu-Reference.md) (the DAGs item appears in the Applications section; requires appropriate user rights to see)
- [RC-NAV-REC-04 — Record Status Dashboard & Other Record Links](RC-NAV-REC-04_Record-Status-Dashboard-and-Links.md) (DAG membership filters which records are visible on the dashboard — only records in the user's assigned DAG appear)
