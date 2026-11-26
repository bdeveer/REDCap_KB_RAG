---
id: RC-PLUS-04
title: 'REDCap+: Project Administrator Groups (PAGs)'
domain: REDCap+
applies_to:
- System administrators delegating administrative work
- users designated as project-level admins
requires: REDCap v17.1.0+ and a REDCap+ subscription
verified_against: REDCap 17.3.6 (LTS) — page description and constraints (§3–4) verified
  from a live capture. The management interface is **hard-gated** without a REDCap+
  subscription and could not be observed — see the scope note; the whole article checked
  against source code of v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS)
prerequisites:
- 'RC-PLUS-01 — REDCap+: Overview and Subscription'
version: '1.3'
last_updated: 2026-11
related:
- id: RC-CC-25
  title: 'Control Center: Access Control Groups'
- id: RC-DAG-01
  title: Data Access Groups
- id: RC-CC-09
  title: 'Control Center: To-Do List'
- id: RC-CC-07
  title: 'Control Center: Users & Access Management'
- id: RC-PROJ-01
  title: 'Project Lifecycle: Status and Settings'
- id: RC-PLUS-01
  title: 'REDCap+: Overview and Subscription'
tags:
- redcap+
synonyms:
- project administrator groups
- PAG redcap
- delegate redcap admin tasks
- power user admin rights
- who approves move to production
- project level admin
- departmental redcap administration
- PAG vs DAG
- distribute admin workload redcap
- cannot remove last project-level admin
- delete a PAG
- who can manage PAGs
- what can a PAG admin do
- PAG admin after REDCap+ subscription lapses
---

> **Scope note.** The page description and the constraints in §3 and §4 are taken from a capture of the Control Center page on a live instance running **17.3.6 LTS**. The rest of the article — page layout (§4), who can manage PAGs, request routing and what project-level admins can do (§6) — has since been checked against REDCap's source code (17.6.5 Standard, 17.3.31 and 16.0.61 LTS), but **not yet on a subscribed live instance**.
>
> **The management interface itself could not be observed, and this page gates harder than other REDCap+ pages.** On the *Modules/Services Configuration* page, REDCap+ settings render server-side and are merely disabled in the browser, so they can be read without a subscription. The Project Administrator Groups page does **not** behave that way: without an active subscription it shows either a notice (as seen on 17.3.6: *"NOTICE: The page has been disabled because a REDCap+ subscription is not active."*) or a plain access-denied error, depending on version. No group table, no forms.
>
> What made §4 documentable at first is that REDCap still emits the page's **language keys** — every column heading, button, dialog and validation message — even when it refuses to render the interface. The layout and flow in §4 now come from the source-code check; expect small differences in wording or placement when you see the live page.
>
> **REDCap+ gating is not uniform across pages.** Do not assume a page is readable without a subscription because another one was.

---

# 1. Overview

**Project Administrator Groups (PAGs)** let projects be administered by **designated project-level administrators** instead of relying solely on system-level administrators.

The problem it solves is workload concentration. In a typical REDCap installation, every routine administrative request — approve this project, move that one to production, approve these draft changes — lands with the same small group of system admins, regardless of which department the project belongs to or how experienced the requester is. PAGs let that work be pushed outward to trusted "power users" who know their own area.

Once a project is assigned to a PAG, the users designated as admins for that group take ownership of routine administrative tasks and user requests for those projects, including:

- **Managing production status changes**
- **Handling draft mode updates**
- **Receiving other project-level requests** (API tokens, External Module enablement and more — see §6)
- **Being notified of new-project requests** from users assigned to the group (see §6 for why a central administrator may still have to complete these)

The stated intent is to distribute administrative workload to experienced users while keeping oversight with people who understand the local context — a departmental REDCap expert is often better placed to judge whether a project in their department is ready for production than a central administrator is.

> **Note:** PAGs delegate administration *of a defined set of projects*, not of the system. Inside the projects in their group, a project-level admin acts with **full administrator rights** (see §6). Outside those projects they have no system-level administrator privileges of the kind documented in [RC-CC-07 — Control Center: Users & Access Management](RC-CC-07_Control-Center-User-Management.md).

---

# 2. Disambiguation: PAGs vs ACGs vs DAGs

REDCap now has three distinct "group" features, two of which are administrator-facing. They are unrelated to each other and solve different problems. Confusing them is the most likely failure mode when this feature is introduced to a team.

| Feature | What it groups | What it controls | Article |
| --- | --- | --- | --- |
| **Project Administrator Groups (PAG)** | Projects and users, for administrative purposes | **Who handles administrative requests** for those projects — production status, draft approvals and other project requests | This article |
| **Access Control Groups (ACG)** | Users | The **ceiling on privileges** a User Rights manager may grant to a user in any project | [RC-CC-25](RC-CC-25_Access-Control-Groups.md) |
| **Data Access Groups (DAG)** | Users within a single project | **Which records a user can see** — data partitioning, typically by site | [RC-DAG-01](RC-DAG-01_Data-Access-Groups.md) |

The short version:

- A **PAG** decides *who approves your request*.
- An **ACG** decides *what rights you can be given*.
- A **DAG** decides *whose records you can see*.

> **Note on a typo in REDCap's own documentation.** The text describing user assignment ends with the sentence *"any projects that those users create will automatically get assigned to the DAG."* This should read **PAG** — the mechanism described is PAG auto-assignment and has nothing to do with Data Access Groups.
>
> This is **not** only a release-note error. The same sentence is the on-page help text on the Project Administrator Groups page itself, confirmed present in 17.3.6 LTS. An administrator reading the product will meet the same confusion.

---

# 3. How Membership Works

Three rules govern assignment, and the asymmetry between them is the part worth remembering:

| Entity | Rule |
| --- | --- |
| **Project-level admins per PAG** | A PAG may have **one or more** admins |
| **A user serving as admin** | A user may be a project-level admin for **multiple PAGs** |
| **Projects** | A project may be assigned to **only one PAG at a time** |
| **Users** | A user may be assigned to **only one PAG at a time** |

So the *admin* role is many-to-many, while *membership* is strictly one-to-one.

> **Important — reassignment is silent.** If you add a project or user to a PAG while it already belongs to another PAG, REDCap moves it to the new group without a warning. Check the current assignment first, especially when two departments share administrators.

> **Critical — a project belongs to exactly one PAG.** This is the constraint that shapes how you design your groups. A project run jointly by two departments cannot be administered by both departments' PAGs; you must choose one, or administer it centrally. Similarly, a user who genuinely works across two departments can only be a member of one PAG — though they *can* be an admin of both, which is often the workaround.

You may create as many PAGs as you wish, and assign as many projects and users to a given PAG as you wish.

---

# 4. The Project Administrator Groups Page

*Page description and constraints verified against 17.3.6 LTS; layout checked against source code, not yet on a subscribed live instance — see the scope note.*

**Where:** Control Center → **Users** section → **Project Administrator Groups**, which carries a `REDCap+` badge.

> **Who can manage PAGs.** The page is open to administrators who have **full administrator rights**, or who hold the **account-manager** privilege or the **admin-rights** (manage administrator privileges) privilege — and only while a REDCap+ subscription is active. It is not limited to full system admins, so review which administrators hold those two privileges before you roll PAGs out. Project-level admins do **not** gain access to this page through their PAG role; this is what keeps the delegation bounded — a delegate cannot widen their own delegation.

There is **no separate system-level on/off switch** for PAGs. The feature becomes operative by creating a group on this page.

## 4.1 The group list

Groups are listed in a table with a search box above it and a **Create new PAG** button next to the search box. Columns, left to right:

| Column | Contents |
| --- | --- |
| **Project Administrator Group** | The group name, with a pencil icon (**Edit PAG Name**) to rename it |
| **Project-level Admins** | Each admin's username and name, with a pencil icon (**Add or remove admins**) |
| **Projects Assigned to PAG** | A count of projects, with a pencil icon to add or remove projects |
| **Users Assigned to PAG** | A count of users whose new projects auto-join the group (§5), with a pencil icon and a **?** help popup |
| **PAG ID** | System identifier for the group |
| *(no heading)* | A red **X** to delete the group |

There is no separate "open the group" column; "View & Manage" is the hover text on the pencil icons.

When no groups exist the list reads *"No groups to display"* — which is also the state of a fresh instance, since there is nothing to enable first.

## 4.2 Creating a group

Creating a PAG requires **two** things, not one:

1. A descriptive **group name**
2. **At least one user designated as its initial project-level admin**

Attempting to create a group without both is rejected: *"You must enter a name for the PAG and select a user to be the project-level admin of that PAG."* Additional admins and projects are assigned after creation.

> **Critical — every PAG must always have at least one project-level admin.** The interface enforces this on removal as well as on creation; trying to remove the last admin shows: *"Sorry, but you cannot remove all project-level admins from the PAG. Each Project Administrator Group must always have at least one project-level admin. Try adding another user first, after which you can then remove this one."*
>
> The practical consequence is a **staffing order of operations**. When the sole admin of a group leaves, you cannot remove them first and appoint a replacement afterwards — you must add the replacement, then remove the departing admin. A leavers process that revokes access before naming a successor will hit this wall. This is an interface safeguard applied by the page.

## 4.3 Managing a group

There is no separate view inside a group. Every operation is a dialog opened from the group's row in the list:

| Operation | How |
| --- | --- |
| **Edit PAG Name** | Pencil next to the group name |
| **Add or remove project-level admins** | Pencil in **Project-level Admins**. Type a username (autocomplete) to add; each admin has its own **Remove** link. Subject to the at-least-one rule above |
| **Add or remove projects** | Pencil in **Projects Assigned to PAG**. The project picker searches by project title or PID and shows **up to 20 matches**; deleted projects and **Completed** projects are not offered. Each assigned project has its own **Remove** link: *"Do you wish to remove the project below from the PAG?"* |
| **Assign or unassign users** | Pencil in **Users Assigned to PAG**. Type a username (autocomplete) to assign; each user has its own **Remove** link. Governs auto-assignment of that user's future projects (§5) |
| **Delete PAG** | Red **X** at the end of the row: *"Do you wish to delete the Project Administrator Group below?"* |

If a project you expect to find is missing from the picker, check whether it is marked Completed, or refine the search — only the first 20 matches are shown.

When a user is unassigned, the confirmation reads *"The user was successfully removed from the PAG!"*

> **Note:** Removing a project from a PAG returns that one project to system-admin handling. Deleting a PAG goes further: it removes all of the group's project-level admins and unassigns all of its projects and users, which all return to central handling.

Changes made on this page are recorded in Control Center logging, so you can trace who changed a delegation and when.

---

# 5. Auto-Assignment via User Membership

Assigning **users** to a PAG is optional, and it exists for one purpose: **any project created by an assigned user is automatically added to that user's PAG**.

Without it, projects are assigned to a PAG manually after creation — which always works, but does not scale. Where a set of users functionally belongs to a department or functional area, assigning those users to the PAG means their future projects land in the right group without anyone having to remember.

> **Note:** Auto-assignment applies at project *creation*. Projects that already exist when a user is assigned to a PAG are not retroactively moved — assign those manually.
>
> Projects created through the API with a super API token are **not** auto-assigned either, even when the token belongs to an assigned user. If you provision projects that way, assign them to the PAG afterwards.

---

# 6. The Project-Level Admin Experience

*Checked against source code; not yet observed on a subscribed live instance — see the scope note.*

A user designated as a project-level admin for a PAG takes on the routine administrative tasks and user requests for the projects in that group — managing production status changes and handling draft mode updates, among others.

**Inside an assigned project**, a project-level admin acts with **full administrator rights** — the same as a system administrator in that project, including when using the API. This is much more than "handling requests": they can do anything an administrator can do in those projects. Inside those projects REDCap labels them as a **Project-level Administrator**, so they can tell where their elevated rights apply.

**Requests and the To-Do List.** For projects in the group, request emails go to the PAG's project-level admins **instead of** the system contact — this covers move to production, draft mode changes, API token requests, External Module enablement, Rewards, public reports and dashboards, and Data Mart requests. Their **To-Do List** shows only requests for projects in their PAG(s). The To-Do entries still appear for central administrators too, marked with a **Managed by PAG** note. See [RC-CC-09 — Control Center: To-Do List](RC-CC-09_To-Do-List.md).

**New-project requests.** Based on how REDCap handles these requests (confirm on your server), when a user assigned to a PAG requests a new project:

- The request email goes to that PAG's project-level admins instead of the central contact.
- The request does **not** appear in the PAG admins' To-Do List; central administrators still see it in theirs.
- If your instance allows only administrators to create projects, the PAG admins most likely cannot complete the request themselves, so a central administrator has to.

In practice, central administrators should keep watching the To-Do List for new-project requests, because they no longer get the email for users assigned to a PAG. Tell PAG admins that these emails are for awareness and that the central team completes the request.

**Outside a project**, a project-level admin gets a cut-down **Control Center** whose menu offers only:

- **To-Do List**
- **Browse Projects**
- **Edit a Project's Settings**
- **API Tokens**

Each of these is scoped to the projects in their PAG(s). System configuration pages and the Project Administrator Groups page are not in their menu, and they cannot change system settings.

> **Critical — PAG admin rights do not depend on the subscription.** The management page locks when a REDCap+ subscription is no longer active, but existing project-level admins **keep administrator-level rights in their assigned projects**. A lapsed subscription therefore leaves elevated access in place that you can no longer review or change on the PAG page. **Before letting a REDCap+ subscription lapse, remove the PAG assignments** (admins and projects) while the page is still available.

---

# 7. Version History

| Version | Change |
| --- | --- |
| **17.1.0 Standard** | Project Administrator Groups introduced as a REDCap+ feature |
| **17.3.3 Standard** | **System Statistics** gained counters for Project Administrator Groups, shown when a REDCap+ subscription is active. See [RC-CC-11 — Control Center: System Statistics](RC-CC-11_System-Statistics.md) |
| **Article v1.3 (2026-11)** | Request routing, new-project requests, PAG deletion, silent reassignment, super-token projects and logging checked against source code |

No PAG-specific defects appear in the Standard or LTS changelogs through 17.4.1 — unusual for a feature this young, and a point in its favour. As with any recent feature, see [RC-INFRA-03 — REDCap Versions, Release Lines & Patching](RC-INFRA-03_REDCap-Versions-Release-Lines-and-Patching.md) for why an LTS instance may not have it yet.

> **Version caveat (LTS):** PAGs arrived in **17.1.0 Standard**. An LTS instance only receives the feature once its line is cut from a Standard release at or above that version. An LTS 16.0.x instance does not have PAGs and will not gain them through patching.

---

# 8. Common Questions

**Q: What is the difference between a Project Administrator Group and a Data Access Group?**

**A:** They are unrelated. A PAG determines **who handles administrative requests** for a set of projects — production status changes, draft approvals and other project requests. A DAG determines **which records a user can see** inside a single project. See §2, which also covers Access Control Groups.

**Q: Can a project belong to two PAGs?**

**A:** No. A project is assigned to one PAG at a time, as is a user. Only the *admin* role is many-to-many: one user can be a project-level admin for several PAGs.

**Q: We have a project run jointly by two departments. How do we handle it?**

**A:** Pick one PAG to own it administratively, or leave it with the central administrators. If the concern is that both departments need a say, note that a single user can be an admin of multiple PAGs — so an individual can cover both groups even though the project cannot belong to both.

**Q: Does a project-level admin become a system administrator?**

**A:** Not system-wide. Inside the projects in their group they act with full administrator rights, including over the API, and they get a cut-down Control Center (To-Do List, Browse Projects, Edit a Project's Settings, API Tokens) scoped to those projects. System configuration pages and the Project Administrator Groups page are not in their menu and they cannot change system settings — only administrators with full administrator rights, or the account-manager or admin-rights privilege, can manage PAGs — so they cannot alter the scope of their own delegation. See §6.

**Q: What happens to PAG admins if our REDCap+ subscription lapses?**

**A:** The Project Administrator Groups page locks, but existing project-level admins keep administrator-level rights in their assigned projects. Remove PAG assignments before letting the subscription lapse. See §6.

**Q: If we assign a user to a PAG, do their existing projects move into it?**

**A:** No. User assignment auto-adds projects **created after** the assignment. Existing projects must be assigned to the PAG manually.

**Q: Do we have to assign users at all?**

**A:** No, it is optional. Projects can always be assigned to a PAG after creation. User assignment is a scalability convenience for cases where a set of people clearly belongs to one department or functional area.

**Q: Our only project-level admin for a group is leaving. How do we swap them out?**

**A:** Add the replacement as a project-level admin first, then remove the departing one. The Project Administrator Groups page will not let you remove the last admin from a PAG — each group must always have at least one.

**Q: Is there a system setting to turn PAGs on?**

**A:** No. The feature becomes operative when you create a group on the Control Center page. Creating one requires a group name *and* at least one initial project-level admin.

**Q: Our Control Center says the Project Administrator Groups page has been disabled. Is it broken?**

**A:** No — that message means no REDCap+ subscription is active. Unlike the Modules/Services Configuration page, which shows its REDCap+ settings in a disabled state, this page shows no interface at all: a notice (as seen on 17.3.6) or a plain access-denied error, depending on version.

**Q: Who handles new-project requests from users assigned to a PAG?**

**A:** Based on how REDCap handles these requests (confirm on your server), the request email goes to the PAG's project-level admins instead of the central contact, but the request only appears in central administrators' To-Do List. If only administrators can create projects on your instance, a central administrator most likely has to complete it. Central administrators should therefore keep watching the To-Do List. See §6.

**Q: Our LTS instance doesn't have this. Why?**

**A:** PAGs shipped in 17.1.0 Standard. An LTS line only picks up features present in the Standard release it was cut from, and patches do not add features. An LTS instance below that point will not gain PAGs until the institution moves to a newer LTS line.

---

# 9. Common Mistakes & Gotchas

**Confusing PAGs with DAGs.** Both are "groups," both are abbreviated to three letters ending in G, and REDCap's own 17.1.0 release notes contain a typo that says "DAG" where it means "PAG". They control completely different things — administrative workflow versus record visibility. See §2.

**Designing PAGs around org charts rather than around projects.** Because a project can only belong to one PAG, a group structure that mirrors a matrixed organisation will produce projects that genuinely belong in two places. Group by who should *approve requests*, which is usually a simpler structure than the org chart.

**Removing a group's only admin before naming a replacement.** The page blocks removing the last project-level admin of a PAG, so the order is add-then-remove. A standard leavers process that revokes first will fail here.

**Assigning users to a PAG and expecting their existing projects to follow.** Auto-assignment is forward-looking only.

**Assuming delegation is bounded by the delegate.** It is bounded by the administrators who manage PAGs — those with full administrator rights, or the account-manager or admin-rights privilege. Project-level admins cannot see or edit the Project Administrator Groups page. Worth stating explicitly when introducing the feature, because it is the reassurance that usually gets asked for.

**Underestimating what a project-level admin can do.** They are not limited to approving requests: inside their assigned projects they have full administrator rights, including over the API. Choose PAG admins as you would choose administrators for those projects.

**Letting REDCap+ lapse with PAGs still in place.** Project-level admins keep administrator-level rights in their projects after the subscription ends, while the management page locks. Remove PAG assignments first. See §6.

**Expecting the feature on LTS.** 17.1.0 Standard only. See §7.

---

# 10. Related Articles

- [RC-CC-25 — Control Center: Access Control Groups](RC-CC-25_Access-Control-Groups.md) — the other administrator-facing "group" feature; sets privilege ceilings rather than delegating workflow
- [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) — record-level partitioning within a project; unrelated to PAGs despite the similar name
- [RC-CC-07 — Control Center: Users & Access Management](RC-CC-07_Control-Center-User-Management.md) — system-level administrator privileges, which PAGs grant only within the group's projects
- [RC-CC-09 — Control Center: To-Do List](RC-CC-09_To-Do-List.md) — where administrative requests are normally processed
- [RC-CC-11 — Control Center: System Statistics](RC-CC-11_System-Statistics.md) — PAG counters added in 17.3.3
- [RC-PROJ-01 — Project Lifecycle: Status and Settings](RC-PROJ-01_Project-Lifecycle-Status-and-Settings.md) — production status changes and draft mode, the workflows PAGs delegate
- [RC-PLUS-01 — REDCap+: Overview and Subscription](RC-PLUS-01_REDCap-Plus-Overview-and-Subscription.md) — what the subscription covers
- [RC-INFRA-03 — REDCap Versions, Release Lines & Patching](RC-INFRA-03_REDCap-Versions-Release-Lines-and-Patching.md) — why an LTS instance may not have this feature
