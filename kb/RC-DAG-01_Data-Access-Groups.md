RC-DAG-01

**Data Access Groups**

| **Article ID** | RC-DAG-01 |
|---|---|
| **Domain** | Data Access Groups |
| **Applies To** | All REDCap project types; requires Data Access Groups privilege to manage |
| **Prerequisite** | RC-USER-01 — User Rights: Overview & Three-Tier Access |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-USER-01 — Overview & Three-Tier Access; RC-USER-02 — Adding Users & Managing Roles; RC-USER-03 — Configuring User Privileges; RC-USER-04 — User Management; RC-EXPRT-03 — Data Export: User Rights & Export Access; RC-RAND-01 — Randomization Concepts & Terminology |

---

# 1. Overview

This article explains Data Access Groups (DAGs) — what they are, how they restrict record-level access, how to create and manage them, and how to assign users. DAGs are a feature for projects where different groups of users should only see their own records, such as multi-site studies where each site's staff should be separated from the others.

---

# 2. Key Concepts & Definitions

**Data Access Group (DAG)**

A named project-level grouping that restricts which records a user can see and interact with. A user assigned to a DAG can only access records that belong to that DAG. Users not assigned to any DAG can access all records.

**DAG Assignment (Record)**

The DAG that a record belongs to. A record is assigned to a DAG either automatically (when created by a user who is in a DAG) or manually by a user with DAG management privileges.

**DAG Assignment (User)**

The DAG a user is assigned to in a given project. A user can be in at most one DAG at a time as their primary assignment. Users with the DAG Switcher feature enabled can also be granted access to multiple DAGs.

**DAG Switcher**

A feature on the DAG management page that allows a user to be associated with multiple DAGs simultaneously, enabling access to records across those groups.

**DAG Management Privilege**

A user right ("Data Access Groups") that grants access to the DAG management page. Without this right, users cannot create, edit, or delete DAGs, or change user-DAG assignments.

---

# 3. How DAGs Work

A DAG controls record-level access within a project. The key behavior:

- When a user assigned to a DAG **creates a new record**, that record is automatically associated with the user's DAG.
- When a user assigned to a DAG **navigates the project**, they can only see records belonging to their DAG.
- **Users with no DAG assignment** can see all records, regardless of which DAG those records belong to.
- **Users with DAG management privileges** (the "Data Access Groups" user right) can see and manage records across all DAGs.

DAGs operate independently of instrument-level user rights (data viewing rights and data export rights). Both layers apply simultaneously: a user's DAG restricts which records they can see, and their data viewing/export rights restrict what they can see within those records.

> **Note:** DAGs control record access, not instrument access or feature access. They do not replace or substitute for the standard user rights configuration.

---

# 4. Setting Up DAGs

## 4.1 Accessing the DAG Page

The DAG management page can be accessed in two ways:

- From the **Applications menu**, click **DAGs**.
- From the **User Rights page**, click the **Data Access Group** tab.

## 4.2 Creating a DAG

1. On the DAG page, type a name for the new group in the **"Enter a new group name"** text box.
2. Click **+ Add Group**.
3. The new DAG will appear in the table below.

For creating many DAGs at once, use the **Upload or download DAGs/User-DAG assignments** button to upload a structured file.

## 4.3 Deleting a DAG

Click the red **X** in the "Delete group" column next to the DAG you want to remove.

> **Important:** REDCap will not allow deletion of a DAG that has records currently assigned to it. You must reassign or remove those records from the DAG before it can be deleted.

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

---

# 6. Multi-DAG Access (DAG Switcher)

If a user needs access to records across multiple DAGs — for example, a monitor who oversees two sites — use the DAG Switcher feature on the DAG page.

1. On the DAG page, scroll to the **DAG Switcher** section.
2. Check the box for each user/DAG combination you want to enable.

The DAG Switcher grants access to additional DAGs beyond the user's primary DAG assignment. It does not override the primary DAG assignment — the user's records are still attributed to their primary DAG when they create new records.

> **Note:** Multi-DAG access can also be managed in bulk using the **Upload or download DAGs/User-DAG assignments** function.

---

# 7. Bulk DAG Management

The **Upload or download DAGs/User-DAG assignments** button (top right of the User Rights page) allows you to:

- **Download** the current DAG setup and all user-DAG assignments as structured files.
- **Upload** modified files to create DAGs or update assignments in bulk.

This is useful for initial project setup with many sites or for migrating a DAG structure from another project.

---

# 8. Common Questions

**Q: What does a DAG restrict exactly?**

**A:** A DAG restricts which records a user can see and interact with. A user in a DAG sees only records that belong to that DAG. It does not affect which instruments, features, or applications a user can access — those are governed by standard user rights.

**Q: Can a user be in more than one DAG at the same time?**

**A:** A user has one primary DAG assignment. If they need access to records in additional DAGs, use the DAG Switcher feature to grant multi-DAG access. The DAG Switcher does not replace the primary assignment.

**Q: What happens to records when a DAG is deleted?**

**A:** REDCap will not allow deletion of a DAG that has records assigned to it. You must reassign or remove those records first.

**Q: If I add a user to a project without assigning them to a DAG, what records can they see?**

**A:** All records. Users with no DAG assignment have unrestricted record-level access across the project. This is intentional — it supports roles like project coordinators or data managers who need to see everything.

**Q: Does a user's DAG assignment affect what data they can export?**

**A:** Yes. Data export rights and DAG assignment both constrain what a user can export. A user in a DAG can only export records belonging to that DAG, and within those records, only the instruments their export rights allow. See RC-EXPRT-03 — Data Export: User Rights & Export Access.

**Q: Can a user create records in a DAG other than their own?**

**A:** No. When a DAG-assigned user creates a record, it is automatically assigned to their DAG. They cannot create a record in a different DAG unless they have DAG management privileges or multi-DAG access via the DAG Switcher.

**Q: Do DAGs interact with randomization?**

**A:** Yes. DAG membership can affect randomization access — specifically which DAG a randomized record is associated with and who can view or perform randomization. See RC-RAND-01 — Randomization Concepts & Terminology for details.

---

# 9. Common Mistakes & Gotchas

**Adding a user to a project without assigning a DAG when they should have one.** A user without a DAG assignment sees all records. For multi-site or restricted-access projects, always verify DAG assignment at the time of user addition. Review the user list regularly to confirm all users have the correct DAG configuration.

**Trying to delete a DAG that still has records.** REDCap blocks this. If the goal is to remove a site from the project, reassign or delete those records first. Plan ahead when retiring a site.

**Assuming DAG assignment controls instrument or feature access.** DAGs only restrict records — not instruments, features, or applications. A user in a DAG still has whatever instrument-level and feature-level rights are configured for them in User Rights.

**Overlooking the DAG Switcher for monitoring roles.** Monitors, auditors, or cross-site coordinators often need access to records across multiple sites. The DAG Switcher is the correct tool for this — not removing them from their primary DAG or making them DAG-unassigned.

**Not accounting for DAGs when setting up export rights.** Because DAGs further restrict which records can be exported, a user's effective export scope is the intersection of their export rights and their DAG. Test export behavior with representative DAG-assigned user accounts to confirm the results match expectations.

---

# 10. Related Articles

- RC-USER-01 — User Rights: Overview & Three-Tier Access
- RC-USER-02 — User Rights: Adding Users & Managing Roles (DAG assignment when adding users)
- RC-USER-03 — User Rights: Configuring User Privileges (DAG management privilege and other rights)
- RC-USER-04 — User Rights: User Management
- RC-EXPRT-03 — Data Export: User Rights & Export Access (how DAGs affect exports)
- RC-RAND-01 — Randomization Concepts & Terminology (DAGs and randomization)
