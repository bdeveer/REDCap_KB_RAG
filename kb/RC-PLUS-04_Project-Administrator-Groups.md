

**REDCap+: Project Administrator Groups (PAGs)**

| **Article ID** | [RC-PLUS-04 — REDCap+: Project Administrator Groups (PAGs)](RC-PLUS-04_Project-Administrator-Groups.md) |
| --- | --- |
| **Domain** | REDCap+ |
| **Applies To** | System administrators delegating administrative work; users designated as project-level admins |
| **Requires** | REDCap v17.1.0+ and a REDCap+ subscription |
| **Verified Against** | Not yet verified against a live instance — written from the 17.1.0 release notes. See the scope note |
| **Prerequisite** | [RC-PLUS-01 — REDCap+: Overview and Subscription](RC-PLUS-01_REDCap-Plus-Overview-and-Subscription.md) |
| **Version** | 1.0 |
| **Last Updated** | 2026-08 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-CC-25 — Control Center: Access Control Groups](RC-CC-25_Access-Control-Groups.md); [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md); [RC-CC-09 — Control Center: To-Do List](RC-CC-09_To-Do-List.md); [RC-CC-07 — Control Center: Users & Access Management](RC-CC-07_Control-Center-User-Management.md); [RC-PROJ-01 — Project Lifecycle: Status and Settings](RC-PROJ-01_Project-Lifecycle-Status-and-Settings.md); [RC-PLUS-01 — REDCap+: Overview and Subscription](RC-PLUS-01_REDCap-Plus-Overview-and-Subscription.md) |
| **Synonyms** | project administrator groups; PAG redcap; delegate redcap admin tasks; power user admin rights; who approves move to production; project level admin; departmental redcap administration; PAG vs DAG; distribute admin workload redcap |

---

> **Scope note.** This article is written from REDCap's **17.1.0** release notes and has **not** been verified against a live instance. The instance this KB is maintained against does not hold a REDCap+ subscription.
>
> Unlike the project-level sections of [RC-PLUS-02](RC-PLUS-02_Project-Migration-Tool.md) and [RC-PLUS-03](RC-PLUS-03_Reward-Services.md), this gap **is** closable without a subscription: the *Project Administrator Groups* page lives in the Control Center, where REDCap+ gating is cosmetic — settings render server-side and are only disabled in the browser. A capture of that page would let §4 and §5 be verified. What cannot be observed without a subscription is the delegated admin's own experience (§6).
>
> Treat everything below as REDCap's description of the feature rather than as observed behaviour, and expect section 4 to gain detail once the Control Center page is captured.

---

## 1. Overview

**Project Administrator Groups (PAGs)** let projects be administered by **designated project-level administrators** instead of relying solely on system-level administrators.

The problem it solves is workload concentration. In a typical REDCap installation, every routine administrative request — approve this project, move that one to production, approve these draft changes — lands with the same small group of system admins, regardless of which department the project belongs to or how experienced the requester is. PAGs let that work be pushed outward to trusted "power users" who know their own area.

Once a project is assigned to a PAG, the users designated as admins for that group take ownership of routine administrative tasks and user requests for those projects, including:

- **Approving project creation requests**
- **Managing production status changes**
- **Handling draft mode updates**

The stated intent is to distribute administrative workload to experienced users while keeping oversight with people who understand the local context — a departmental REDCap expert is often better placed to judge whether a project in their department is ready for production than a central administrator is.

> **Note:** PAGs delegate *administrative workflow*, not system administration. A project-level admin handles requests for the projects in their group. This is not the same as granting someone the system-level administrator privileges documented in [RC-CC-07 — Control Center: Users & Access Management](RC-CC-07_Control-Center-User-Management.md).

---

## 2. Disambiguation: PAGs vs ACGs vs DAGs

REDCap now has three distinct "group" features, two of which are administrator-facing. They are unrelated to each other and solve different problems. Confusing them is the most likely failure mode when this feature is introduced to a team.

| Feature | What it groups | What it controls | Article |
| --- | --- | --- | --- |
| **Project Administrator Groups (PAG)** | Projects and users, for administrative purposes | **Who handles administrative requests** for those projects — project creation, production status, draft approvals | This article |
| **Access Control Groups (ACG)** | Users | The **ceiling on privileges** a User Rights manager may grant to a user in any project | [RC-CC-25](RC-CC-25_Access-Control-Groups.md) |
| **Data Access Groups (DAG)** | Users within a single project | **Which records a user can see** — data partitioning, typically by site | [RC-DAG-01](RC-DAG-01_Data-Access-Groups.md) |

The short version:

- A **PAG** decides *who approves your request*.
- An **ACG** decides *what rights you can be given*.
- A **DAG** decides *whose records you can see*.

> **Note on a typo in REDCap's own release notes.** The 17.1.0 entry describing user assignment ends with the sentence *"any projects that those users create will automatically get assigned to the DAG."* This should read **PAG** — the mechanism described is PAG auto-assignment and has nothing to do with Data Access Groups. Worth knowing if you are reading the release notes alongside this article.

---

## 3. How Membership Works

Three rules govern assignment, and the asymmetry between them is the part worth remembering:

| Entity | Rule |
| --- | --- |
| **Project-level admins per PAG** | A PAG may have **one or more** admins |
| **A user serving as admin** | A user may be a project-level admin for **multiple PAGs** |
| **Projects** | A project may be assigned to **only one PAG at a time** |
| **Users** | A user may be assigned to **only one PAG at a time** |

So the *admin* role is many-to-many, while *membership* is strictly one-to-one.

> **Critical — a project belongs to exactly one PAG.** This is the constraint that shapes how you design your groups. A project run jointly by two departments cannot be administered by both departments' PAGs; you must choose one, or administer it centrally. Similarly, a user who genuinely works across two departments can only be a member of one PAG — though they *can* be an admin of both, which is often the workaround.

You may create as many PAGs as you wish, and assign as many projects and users to a given PAG as you wish.

---

## 4. Enabling and Configuring PAGs

**Where:** Control Center → **Project Administrator Groups** (in the **Users** section of the Control Center menu, where it carries a `REDCap+` badge).

> **Only system-level admins can access that page.** Project-level admins administer projects within their group; they do not gain access to the page that defines the groups themselves. This is what keeps the delegation bounded.

From there you create groups and assign projects and users to them.

> **This section will expand once the Control Center page has been captured.** The release notes describe what the page does but not its individual controls. See the scope note.

---

## 5. Auto-Assignment via User Membership

Assigning **users** to a PAG is optional, and it exists for one purpose: **any project created by an assigned user is automatically added to that user's PAG**.

Without it, projects are assigned to a PAG manually after creation — which always works, but does not scale. Where a set of users functionally belongs to a department or functional area, assigning those users to the PAG means their future projects land in the right group without anyone having to remember.

> **Note:** Auto-assignment applies at project *creation*. Projects that already exist when a user is assigned to a PAG are not retroactively moved — assign those manually.

---

## 6. The Project-Level Admin Experience

> **Not verified.** This section cannot be observed without a REDCap+ subscription and active PAGs. It reflects what the release notes state.

A user designated as a project-level admin for a PAG takes on the routine administrative tasks and user requests for the projects in that group — approving project creation requests, managing production status changes, and handling draft mode updates.

Requests of this kind normally surface on the system administrator's **To-Do List**; how PAG-scoped requests are presented to a project-level admin is not described in the release notes. See [RC-CC-09 — Control Center: To-Do List](RC-CC-09_To-Do-List.md).

---

## 7. Version History

| Version | Change |
| --- | --- |
| **17.1.0 Standard** | Project Administrator Groups introduced as a REDCap+ feature |
| **17.3.3 Standard** | **System Statistics** gained counters for Project Administrator Groups, shown when a REDCap+ subscription is active. See [RC-CC-11 — Control Center: System Statistics](RC-CC-11_System-Statistics.md) |

No PAG-specific defects appear in the Standard or LTS changelogs through 17.4.1 — unusual for a feature this young, and a point in its favour. As with any recent feature, see [RC-INFRA-03 — REDCap Versions, Release Lines & Patching](RC-INFRA-03_REDCap-Versions-Release-Lines-and-Patching.md) for why an LTS instance may not have it yet.

> **Version caveat (LTS):** PAGs arrived in **17.1.0 Standard**. An LTS instance only receives the feature once its line is cut from a Standard release at or above that version. An LTS 16.0.x instance does not have PAGs and will not gain them through patching.

---

## 8. Common Questions

**Q: What is the difference between a Project Administrator Group and a Data Access Group?**

**A:** They are unrelated. A PAG determines **who handles administrative requests** for a set of projects — project creation approvals, production status changes, draft approvals. A DAG determines **which records a user can see** inside a single project. See §2, which also covers Access Control Groups.

**Q: Can a project belong to two PAGs?**

**A:** No. A project is assigned to one PAG at a time, as is a user. Only the *admin* role is many-to-many: one user can be a project-level admin for several PAGs.

**Q: We have a project run jointly by two departments. How do we handle it?**

**A:** Pick one PAG to own it administratively, or leave it with the central administrators. If the concern is that both departments need a say, note that a single user can be an admin of multiple PAGs — so an individual can cover both groups even though the project cannot belong to both.

**Q: Does a project-level admin become a system administrator?**

**A:** No. They handle administrative requests for the projects in their group. They cannot reach the Project Administrator Groups page in the Control Center — only system-level admins can — so they cannot alter the scope of their own delegation.

**Q: If we assign a user to a PAG, do their existing projects move into it?**

**A:** No. User assignment auto-adds projects **created after** the assignment. Existing projects must be assigned to the PAG manually.

**Q: Do we have to assign users at all?**

**A:** No, it is optional. Projects can always be assigned to a PAG after creation. User assignment is a scalability convenience for cases where a set of people clearly belongs to one department or functional area.

**Q: Our LTS instance doesn't have this. Why?**

**A:** PAGs shipped in 17.1.0 Standard. An LTS line only picks up features present in the Standard release it was cut from, and patches do not add features. An LTS instance below that point will not gain PAGs until the institution moves to a newer LTS line.

---

## 9. Common Mistakes & Gotchas

**Confusing PAGs with DAGs.** Both are "groups," both are abbreviated to three letters ending in G, and REDCap's own 17.1.0 release notes contain a typo that says "DAG" where it means "PAG". They control completely different things — administrative workflow versus record visibility. See §2.

**Designing PAGs around org charts rather than around projects.** Because a project can only belong to one PAG, a group structure that mirrors a matrixed organisation will produce projects that genuinely belong in two places. Group by who should *approve requests*, which is usually a simpler structure than the org chart.

**Assigning users to a PAG and expecting their existing projects to follow.** Auto-assignment is forward-looking only.

**Assuming delegation is bounded by the delegate.** It is bounded by the system admin — project-level admins cannot see or edit the Project Administrator Groups page. Worth stating explicitly when introducing the feature, because it is the reassurance that usually gets asked for.

**Treating a project-level admin as a lower-privilege system admin.** They are not a tier of system administration; they are the recipient of specific delegated workflows for a defined set of projects.

**Expecting the feature on LTS.** 17.1.0 Standard only. See §7.

---

## 10. Related Articles

- [RC-CC-25 — Control Center: Access Control Groups](RC-CC-25_Access-Control-Groups.md) — the other administrator-facing "group" feature; sets privilege ceilings rather than delegating workflow
- [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) — record-level partitioning within a project; unrelated to PAGs despite the similar name
- [RC-CC-07 — Control Center: Users & Access Management](RC-CC-07_Control-Center-User-Management.md) — system-level administrator privileges, which PAGs do not grant
- [RC-CC-09 — Control Center: To-Do List](RC-CC-09_To-Do-List.md) — where administrative requests are normally processed
- [RC-CC-11 — Control Center: System Statistics](RC-CC-11_System-Statistics.md) — PAG counters added in 17.3.3
- [RC-PROJ-01 — Project Lifecycle: Status and Settings](RC-PROJ-01_Project-Lifecycle-Status-and-Settings.md) — production status changes and draft mode, the workflows PAGs delegate
- [RC-PLUS-01 — REDCap+: Overview and Subscription](RC-PLUS-01_REDCap-Plus-Overview-and-Subscription.md) — what the subscription covers
- [RC-INFRA-03 — REDCap Versions, Release Lines & Patching](RC-INFRA-03_REDCap-Versions-Release-Lines-and-Patching.md) — why an LTS instance may not have this feature
