---
id: RC-PLUS-02
title: 'REDCap+: Project Migration Tool'
domain: REDCap+
applies_to:
- Users moving a whole project between REDCap instances
- REDCap Administrators (Sections 6–7)
requires: REDCap v17.0.0+ on **both** instances. A REDCap+ subscription is required
  on the **destination** instance only — see §2
verified_against: REDCap 17.3.6 (LTS) — Project Migration Dashboard verified against
  a live instance. The migration workflow itself (§3–4) is from release notes only
  and **cannot be verified without a REDCap+ subscription** — see the scope note
prerequisites:
- 'RC-PLUS-01 — REDCap+: Overview and Subscription'
version: '1.2'
last_updated: 2026-08
related:
- id: RC-PROJ-05
  title: 'Project Migration: Moving a Project Between REDCap Installations'
- id: RC-PLUS-01
  title: 'REDCap+: Overview and Subscription'
- id: RC-API-01
  title: REDCap API
- id: RC-PROJ-01
  title: 'Project Lifecycle: Status and Settings'
- id: RC-INFRA-03
  title: REDCap Versions, Release Lines & Patching
tags:
- redcap+
synonyms:
- how do i move a project to another redcap server
- project migration tool redcap plus
- migrate a whole project including logs and files
- migration key redcap
- move project between institutions with all data
- transfer a redcap project to another instance
- does project migration include randomization and logging
- project migration dashboard
- what does the project migration tool actually copy
---

> **Scope note.** Section 6.2 (the Project Migration Dashboard) is verified against a live instance running 17.3.6 LTS. The rest of the article is written from REDCap's release notes for 17.0.0 through 17.4.1 and has **not** been verified against an instance with a REDCap+ subscription. The mechanics in Sections 3–5 follow REDCap's own description of the feature; screen labels and the exact placement of controls in those sections should be confirmed before this article is used as a step-by-step guide.
>
> **Why the rest cannot currently be verified — a standing limitation.** The instance this KB is maintained against does **not** hold a REDCap+ subscription. The dashboard could still be documented because it is reachable without one, and because REDCap+ gating in the Control Center is cosmetic — settings render server-side and are merely disabled in the browser. The migration workflow is different: generating a migration key and receiving a project require the subscription, so §3–4 cannot be observed from this instance at all.
>
> **What would close it:** a walkthrough or page capture from an institution that has run a migration. Until then, treat §3–4 as REDCap's own description of the feature rather than as observed behaviour. The version caveats in §5 are drawn from the release notes and are unaffected.

---

# 1. Overview

The **Project Migration Tool (PMT)** moves a project *in its entirety* from one REDCap instance to another — structure, metadata, data, files, logs and more. REDCap describes it as the most complete solution it has offered for moving projects between instances.

The distinction from the long-standing Project XML approach is what it carries. A Project XML export moves the project's design and, optionally, its data. The PMT additionally migrates things that previously could not be moved at all:

- **Record locking statuses and timestamps**
- **Survey participants and survey timestamps**
- **Field Comment Log**
- **Data Resolution Workflow**, including its files
- **Calendar events**, including record scheduling
- **Randomization assignments and allocation tables**
- **Logging** and **Email Logging**
- **File Repository** folders and files, and the **PDF Snapshot Archive**
- **External Module configuration settings**

For a regulated study, that list is the point. A project moved by XML arrives with no audit trail, no randomization history and no query history; a project moved by PMT arrives with all three.

The authoritative list of what the tool tracks is the **column set of the Project Migration Dashboard** — see §6.2, which enumerates all fifteen components individually.

For the XML-based approach — which remains the right tool when the destination is not on 17.0.0+, or when you only need the design — see [RC-PROJ-05 — Project Migration: Moving a Project Between REDCap Installations](RC-PROJ-05_Project-Migration.md).

---

# 2. Prerequisites

## 2.1 Both instances must be on 17.0.0 or later

The PMT is not a one-sided feature. **Both the source and the destination instance must be running REDCap 17.0.0 or higher.** If either is older, the tool is unavailable and the XML route in `RC-PROJ-05` is the alternative.

## 2.2 The subscription requirement is asymmetric

This is the most commonly misunderstood point about the feature:

| Direction | REDCap+ required? |
| --- | --- |
| Moving a project **off** your instance (source) | **No** |
| Moving a project **to** your instance (destination) | **Yes** |

An institution without a REDCap+ subscription can therefore **send** projects away but cannot **receive** them. If you are consolidating instances, the subscription is needed on the instance you are consolidating *into*.

> **Version caveat (17.0.0–17.4.0 Standard):** The **Project Migration Dashboard** link in the Control Center behaved inconsistently around this asymmetry. It was displayed even without a subscription (fixed 17.0.4), then greyed out to look disabled when no subscription was present (fixed 17.4.1) — which was also wrong, because the dashboard is meant to be usable by any institution. From 17.4.1 the link is never greyed out, and is hidden only when the system setting allowing migrations *to* this server is Disabled.

## 2.3 The initiating user needs API access

The PMT works **through the REDCap API**. The user starting a migration must have:

- **API Export** privileges in the source project, and
- an **API token** for that project.

See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md).

> **Important — you can only migrate what you can already access.** If the initiating user lacks privileges for a specific project component — Logging or the File Repository, for example — that component **cannot be migrated**. The tool does not elevate the user's access. A migration run by someone with partial rights produces a partial project, so the person initiating it should hold full rights in the source project.

---

# 3. How a Migration Works

The PMT is a two-sided handshake built around a **migration key**.

1. **On the source instance** — a user generates a migration key from the project's **Other Functionality** page.
2. **On the destination instance** — a user creates a new project using that migration key.
3. The destination instance then **pulls** the project's components from the source using backend API processes driven by the REDCap **cron job**.

Because step 3 is cron-driven rather than interactive, a migration completes over time rather than instantly. Administrators can watch progress on the Project Migration Dashboard (§6).

## 3.1 The migration key

Two constraints on the key matter operationally:

- **It expires after three days.** A key generated and not used within that window is dead, and a new one must be generated.
- **It is bound to one destination.** Before the key is generated, the user enters the **Instance ID** of the intended destination. The key works only for the instance matching that ID.

The binding is a safety property rather than an obstacle — a leaked or mistakenly-shared key cannot be used to pull a project onto an arbitrary server. It does mean you need the destination's Instance ID before you start.

---

# 4. Completion Actions

When initiating a migration, the user chooses what should happen to the **source** project once the migration completes:

| Option | Effect on the source project |
| --- | --- |
| Keep the project as is | Nothing changes; the project remains fully active |
| Keep in Analysis/Cleanup status | Moved to Analysis/Cleanup — data collection stops, data remains accessible |
| Mark project as Completed | Taken offline and hidden from users' project lists |
| Mark as Completed **and redirect public survey(s) to the new project** | As above, plus public survey links follow the project to its new home |
| Delete project | Deleted, **restorable by an administrator for up to 30 days** |

> **The redirect option is the one to think about.** If a project has public survey links in circulation — printed on materials, embedded in a web page, sent in an email — those links point at the *source* instance. Choosing "Mark as Completed and redirect public survey(s)" is what keeps them working after the move. Any other option leaves them pointing at a project that is no longer collecting data.

> **Note:** "Delete project" is recoverable for 30 days by an administrator, but that is a grace period, not a backup. Confirm the migration completed and the destination project is correct before relying on it.

---

# 5. Known Issues by Version

The PMT is a young feature and several defects affected what actually arrived at the destination. Each of these fails *quietly* — the migration reports success while something is missing.

> **Critical — files and signatures could be silently omitted (below 17.0.6 Standard).** Migrating a **longitudinal** project containing File Upload field files and/or Signature field files could fail to migrate some of those files, in specific situations. Fixed in 17.0.6. If a longitudinal project was migrated on 17.0.0–17.0.5, verify file and signature completeness at the destination rather than assuming it.

> **Critical — records could be silently dropped for failing validation (below 17.0.2 Standard).** Records containing data that **did not pass the field validation** of a field would not be migrated. Legacy projects commonly hold values that no longer satisfy current validation rules, so this is not a rare edge case. Fixed in 17.0.2. Compare record counts between source and destination.

> **Critical — the Development record limit could truncate a migration (below 17.1.4 Standard).** Where the system-level **Development Max Record Limit** was set, migrating a project with more records than that limit would fail to migrate all records — **even where the source project was in Production or Analysis/Cleanup status**, and so should not have been subject to a development limit at all. Fixed in 17.1.4. This one is particularly worth checking, because a large production project is exactly the kind you would migrate and exactly the kind that exceeds a development limit.

> **Version caveat (below 17.2.0 Standard):** In **longitudinal** projects, record-level **locking statuses and timestamps** might not be migrated. Since record locking is often part of a data-integrity or 21 CFR Part 11 posture, a migrated project could arrive with locks silently absent.

> **Version caveat (17.0.0 Standard only):** Migration log entries recorded the wrong values — the source instance's log listed the **source** URL where it should have listed the destination, and the destination's "Create project using Project Migration Tool" entry listed the **destination** Instance ID rather than the source. Fixed in 17.0.1. Migration audit entries from 17.0.0 should be read with that in mind.

> **Version caveat (below 17.1.4 Standard):** A PMT-related cron job could fail with a fatal PHP error when creating a new project, in rare cases.

**Practical implication:** on any version below 17.2.0, treat a migration as needing verification rather than confirmation. Compare record counts, file counts, and locking status between source and destination before acting on the completion action — particularly before choosing "Delete project".

---

# 6. Administrator Controls

## 6.1 Who may migrate projects in

Settings on the **Modules/Services Configuration** page in the Control Center govern migration into the instance. Administrators can allow users to migrate projects in **on their own**, or require **administrator approval** for each migration. See [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md).

There is also a system-level setting **"Allow users to use the Project Migration Tool to move projects TO THIS SERVER?"**. When it is Disabled, the Project Migration Dashboard link is hidden from the Control Center menu (from 17.4.1).

## 6.2 Project Migration Dashboard

*Verified against 17.3.6 LTS.*

**Where:** Control Center → **Projects** section → **Project Migration Dashboard**. The menu entry carries a `REDCap+` badge and sits directly below *Edit Project Settings* and *Link Lookup*.

The page's stated purpose is to *"monitor the progress of all projects being migrated to this REDCap server instance using the Project Migration Tool."* Because migrations run through cron rather than interactively, this is where an administrator checks whether a migration is progressing, stalled or complete.

> **The dashboard is reachable without a subscription.** This was confirmed on a 17.3.6 LTS instance whose Control Center menu showed *"REDCap Plus Not Active"* — the page still loaded and rendered normally. That is the intended behaviour: any institution may use it, since any institution may be a migration *destination's* counterpart. See the version caveat in §2.2 for the two releases where the link's display was wrong.

### 6.2.1 Per-migration identification columns

Each row is one migration into this instance:

| Column | What it tells you |
| --- | --- |
| Status | Overall state of this migration |
| PID | The project ID assigned **on this instance** |
| Start Date / End Date | When the migration began and finished. A start date with no end date is a migration still in progress — or stalled |
| Source REDCap URL | The instance the project came from |
| **Source REDCap Version** | The version the source was running. Read this against §5 — it is how you tell whether a completed migration is subject to one of the silent-omission defects |
| Source PID | The project ID on the source instance |
| Source Title | The project's title on the source instance |
| Source Project Status | Development / Production / Analysis-Cleanup / Completed at the source |
| Source Completion Action | Which of the five §4 actions was chosen for the source project |

### 6.2.2 Per-component status columns

The remaining fifteen columns each report the migration status of **one component**. This column set is the most precise available statement of what the tool moves:

| # | Component |
| --- | --- |
| 1 | Records |
| 2 | Files uploaded for File Upload fields (including signatures) |
| 3 | Record-locking statuses and timestamps |
| 4 | Survey participants and survey timestamps |
| 5 | Field Comment Log |
| 6 | Data Resolution Workflow |
| 7 | Data Resolution Workflow Files |
| 8 | Calendar events (including record scheduling) |
| 9 | Randomization assignments and allocation tables |
| 10 | Logging |
| 11 | Email Logging |
| 12 | File Repository folders (and seeding of files) |
| 13 | File Repository files (all folders and user-uploaded files) |
| 14 | PDF Snapshot Archive files |
| 15 | External Module configuration settings |

Three of these are worth calling out because they are easy to assume *would not* move:

- **Field Comment Log and Data Resolution Workflow (5–7)** — the query and resolution history travels with the project, files included. For a study that has been running data queries for years, this is the difference between a migration and a re-creation.
- **Calendar events (8)** — including record scheduling, so a longitudinal project's schedule survives the move.
- **External Module configuration settings (15)** — module *settings* migrate. The modules themselves are a separate matter: an EM that is not installed and enabled on the destination has nothing for those settings to attach to. Confirm the destination instance has the same modules available before migrating. See [RC-EM-01 — External Modules: Overview & Manager](RC-EM-01_External-Modules-Overview-and-Manager.md).

### 6.2.3 Using it to verify a migration

The per-component breakdown is what makes §5's silent-failure problem tractable. Rather than comparing the source and destination project by hand, read the row: if a component's status column does not report success, that component did not fully arrive — regardless of whether the migration as a whole reported completion.

The table is searchable and pageable (10 / 25 / 50 / 100 / 500 / All rows, defaulting to 25) and is **unsorted by default**, so rows appear in the order REDCap returns them rather than newest-first.

---

# 7. Common Questions

**Q: What does the Project Migration Tool move that a Project XML export does not?**

**A:** Record locking statuses and timestamps, survey participants and timestamps, File Repository folders and files including PDF Snapshots, randomization assignments and allocation tables, Logging, and Email Logging. A Project XML export carries the design and optionally the data, but none of those.

**Q: Do we need a REDCap+ subscription to use it?**

**A:** Only to receive projects. Moving a project **off** your instance does not require a subscription; moving a project **to** your instance does. An institution without REDCap+ can send but not receive.

**Q: Both instances need to be on 17.0.0?**

**A:** Yes — the tool is unavailable if either side is older. Where the destination cannot be upgraded, use the Project XML approach in [RC-PROJ-05 — Project Migration](RC-PROJ-05_Project-Migration.md).

**Q: How long is a migration key valid?**

**A:** Three days, and it only works for the destination instance whose Instance ID was entered before the key was generated. You need that Instance ID before you start.

**Q: Our public survey links are printed on recruitment materials. Will they still work after migrating?**

**A:** Only if you choose the completion action **"Mark project as Completed and redirect public survey(s) to new project"**. Every other option leaves circulating links pointing at the source instance, where the project is no longer collecting data.

**Q: Why is the migration taking so long?**

**A:** The destination pulls components through backend API processes driven by the cron job, so a migration progresses over time rather than completing on submission. Administrators can check progress on the Project Migration Dashboard. If a project's cron is not running, migrations will not progress — see [RC-CC-02 — Control Center: General System Configuration](RC-CC-02_Control-Center-General-Configuration.md).

**Q: How do I check whether everything actually arrived?**

**A:** Use the **Project Migration Dashboard** in the Control Center. It reports a separate status for each of fifteen components — records, file-field uploads, locking, survey participants, Field Comment Log, Data Resolution Workflow and its files, calendar events, randomization, Logging, Email Logging, File Repository folders and files, PDF Snapshot Archive, and External Module settings. Read the row rather than comparing projects by hand. The **Source REDCap Version** column tells you whether the migration was exposed to one of the defects in §5.

**Q: Do External Module settings come across?**

**A:** The *settings* do — the dashboard tracks them as a component. The *modules* do not. Settings for a module that is not installed and enabled on the destination have nothing to attach to, so confirm the destination has the same modules available before migrating.

**Q: Does the Data Resolution Workflow / query history survive?**

**A:** Yes. The Field Comment Log, the Data Resolution Workflow and its files are all migrated components. So are Calendar events including record scheduling. This is a substantial difference from the Project XML route, which carries none of them.

**Q: A colleague ran the migration and the logs did not come across. Why?**

**A:** A user can only migrate components they have privileges for. Someone without Logging rights in the source project cannot migrate the log. Have the migration initiated by a user with full rights in the source project.

---

# 8. Common Mistakes & Gotchas

**Assuming a completed migration is a verified migration.** On versions below 17.2.0, several defects caused records, files, signatures and locking statuses to be omitted without any error. Check the **per-component status columns on the Project Migration Dashboard** (§6.2) before treating the move as done — and certainly before choosing a completion action that deletes the source. The dashboard reports each component separately precisely because the overall result can look fine while a component did not arrive.

**Migrating a project whose External Modules are not present on the destination.** Module configuration settings migrate; the modules do not. Settings arriving for a module the destination does not have are settings with nothing to attach to.

**Choosing "Delete project" before checking the destination.** The source is recoverable for 30 days by an administrator, which is a safety net rather than a plan. Verify first, delete afterwards.

**Forgetting that circulating survey links point at the old instance.** Public survey links do not follow the project unless you pick the redirect completion action. Recruitment materials, emails and embedded links keep pointing at the source.

**Running the migration as a user with partial rights.** The tool migrates only the components the initiating user can access. A migration run by someone without File Repository or Logging rights produces a project missing exactly those things, with nothing to indicate it.

**Generating a migration key too early.** Keys expire after three days and are bound to one destination Instance ID. Generate the key when you are ready to migrate, not while still planning.

**Expecting to receive projects without a subscription.** The asymmetry catches institutions consolidating instances: the subscription is required on the instance being consolidated *into*, not the ones being retired.

---

# 9. Related Articles

- [RC-PROJ-05 — Project Migration: Moving a Project Between REDCap Installations](RC-PROJ-05_Project-Migration.md) — the Project XML approach, which remains the route where either instance is below 17.0.0 or only the design is needed
- [RC-PLUS-01 — REDCap+: Overview and Subscription](RC-PLUS-01_REDCap-Plus-Overview-and-Subscription.md) — what the subscription covers
- [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) — API Export privileges and tokens, which the tool depends on
- [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md) — administrator controls over inbound migration
- [RC-EM-01 — External Modules: Overview & Manager](RC-EM-01_External-Modules-Overview-and-Manager.md) — module settings migrate, but the modules themselves must already exist on the destination
- [RC-PROJ-01 — Project Lifecycle: Status and Settings](RC-PROJ-01_Project-Lifecycle-Status-and-Settings.md) — project statuses referenced by the completion actions
- [RC-INFRA-03 — REDCap Versions, Release Lines & Patching](RC-INFRA-03_REDCap-Versions-Release-Lines-and-Patching.md) — why an LTS instance may not be on 17.0.0 yet
