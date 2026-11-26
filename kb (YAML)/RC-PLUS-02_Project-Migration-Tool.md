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
  a live instance. The migration workflow itself (§3–4) has not been observed live,
  because that needs a REDCap+ subscription — see the scope note; migration workflow
  and dashboard checked against source code of v17.6.5 (Standard) / v17.3.31 and v16.0.61
  (LTS)
prerequisites:
- 'RC-PLUS-01 — REDCap+: Overview and Subscription'
version: '1.6'
last_updated: 2026-11
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
- move a project with the redcap+ migration tool
- project migration tool redcap plus
- migrate a whole project including logs and files
- migration key redcap
- move project between institutions with all data
- transfer a redcap project to another instance
- does project migration include randomization and logging
- project migration dashboard
- what does the project migration tool actually copy
---

> **Scope note.** Section 6.2 (the Project Migration Dashboard) is verified against a live instance running 17.3.6 LTS. The rest of the article was first written from REDCap's release notes for 17.0.0 through 17.4.1. The migration workflow (Sections 2–4 and 6.1) and the dashboard's status values (§6.2) have since been **checked against REDCap's source code** (17.6.5 Standard, 17.3.31 and 16.0.61 LTS), but **not yet observed on a live instance with a REDCap+ subscription**. Screen labels and the exact placement of controls in those sections should be confirmed before this article is used as a step-by-step guide.
>
> **Why the rest cannot currently be verified — a standing limitation.** The instance this KB is maintained against does **not** hold a REDCap+ subscription. The dashboard could still be documented because it is reachable without one. (Gating varies by page: some Control Center pages render their REDCap+ settings server-side and merely disable them in the browser, while others replace the interface entirely with a subscription notice — see [RC-PLUS-01](RC-PLUS-01_REDCap-Plus-Overview-and-Subscription.md) §4a.) The migration workflow is different: generating a migration key and receiving a project require the subscription, so §3–4 cannot be observed from this instance at all.
>
> **What would close it:** a walkthrough or page capture from an institution that has run a migration. Until then, treat §3–4 as source-checked behaviour rather than observed behaviour. The version caveats in §5 are drawn from the release notes and are unaffected.

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

How the history arrives matters for auditors. The source project's log is not merged into the destination's own log: it is kept separately and shown on a **Legacy Logging** tab of the destination project's Logging page (next to **Standard Logging**), with its own download button. Email Logging history is likewise kept as a separate file. See §3.3 for history that arrives without the original user names.

The authoritative list of what the tool tracks is the **column set of the Project Migration Dashboard** — see §6.2, which enumerates all fifteen components individually.

When it is available, the PMT is the preferred way to move a project. The Project XML approach is the fallback — for when either instance is below 17.0.0, the destination has no REDCap+ subscription, or you only need the design — see [RC-PROJ-05 — Project Migration: Moving a Project Between REDCap Installations](RC-PROJ-05_Project-Migration.md).

---

# 2. Prerequisites

## 2.1 Both instances must be on 17.0.0 or later

The PMT is not a one-sided feature. **Both the source and the destination instance must be running REDCap 17.0.0 or higher** — in practice, both on a 17.x release with the server trust configuration in §2.1a in place. If either is older, the tool is unavailable and the XML route in [RC-PROJ-05 — Project Migration: Moving a Project Between REDCap Installations](RC-PROJ-05_Project-Migration.md) is the alternative.

> **Version caveat (16.0.x LTS):** A reduced form of the Project Migration Tool also exists on the 16.0 LTS line (checked on 16.0.61). It has no destination Instance ID binding, no completion actions and no Project Migration Dashboard, and every inbound migration needs administrator approval. A 16.0.x server and a 17.x server **cannot migrate projects between each other**, because they use incompatible migration key formats. If one side is on 16.0.x, either upgrade both sides to 17.x before migrating, or use the Project XML route in [RC-PROJ-05](RC-PROJ-05_Project-Migration.md). The rest of this article describes the 17.x tool.

## 2.1a Both servers must be configured to trust each other (17.x)

On 17.x, the migration tool will not work between two servers until **the REDCap server administrators of both servers** have set up a server-side **trust configuration** between them. Each server's configuration names the other as a trusted peer, together with a key pair. This is done at the server level, outside the Control Center, and is separate from the REDCap+ subscription and the Control Center settings in §6.1.

Where the problem shows up depends on which side is missing the configuration:

- **Missing or incomplete on the source server** — clicking the button to generate the key on the source produces an error there, and **no key is created**. The details are recorded in the server's logs.
- **Missing on the destination server, or the destination's configuration does not list the source** — the key is generated normally, but the destination reports it as **not valid** ("The migration key provided was not valid").

The trust configuration also has network requirements. The two servers must be able to reach each other **directly over HTTPS by their public hostnames**. Outbound proxies and private (internal) network addresses are not supported. Ask your server team to confirm this before you plan a migration date.

> **Important — check this before anything else.** If key generation fails on the source, or a key is rejected as not valid at the destination even though it was generated recently and for the right destination, a missing or mismatched trust configuration is a likely cause. Ask the REDCap server administrators of **both** servers to confirm that each lists the other as a trusted peer, that the servers can reach each other as described above, and to check the server logs for the error. Users and Control Center administrators cannot fix this from the REDCap interface. "Not valid" has other causes too — see the troubleshooting list in §3.1.

## 2.2 The subscription requirement is asymmetric

This is the most commonly misunderstood point about the feature:

| Direction | REDCap+ required? |
| --- | --- |
| Moving a project **off** your instance (source) | **No** |
| Moving a project **to** your instance (destination) | **Yes** |

An institution without a REDCap+ subscription can therefore **send** projects away but cannot **receive** them. If you are consolidating instances, the subscription is needed on the instance you are consolidating *into*.

> **Version caveat (17.0.0+ Standard):** The **Project Migration Dashboard** link in the Control Center has behaved inconsistently around this asymmetry. It was displayed even without a subscription (fixed 17.0.4), and release notes for 17.4.1 describe a fix for the link being greyed out without a subscription. Source code of 17.6.5 still shows the link **greyed out** when no subscription is present, and **hidden** when the system setting allowing migrations *to* this server is Disabled. A greyed-out link does not mean the dashboard is unavailable: the dashboard itself works without a subscription (§6.2). If the link is missing altogether, check the setting in §6.1.

## 2.3 The initiating user needs API access and Project Design rights

The PMT works **through the REDCap API**. To generate a migration key, the user starting a migration must have, in the source project:

- **API Export** privileges,
- an **API token** for that project,
- **Project Design and Setup** rights (not needed if the user is a REDCap administrator), and
- project rights that have **not expired**. A user whose project access has an expiration date in the past cannot generate a key.

> **Version caveat (16.0.x LTS):** the expired-rights check is 17.x only. On a 16.0.x server, do not rely on an expiration date to stop a former team member from starting a migration; remove their API token or rights instead.

The API token is used for the whole migration, not only to create the key. **Keep the source token valid until the migration has completed**: do not regenerate or delete it, and do not change the initiating user's rights or the project's settings mid-way. If the final step fails because the token no longer works, the migration is still shown as completed on the destination, but the completion action is **not** applied to the source project — check the source and apply it by hand.

See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md).

Data export rights also limit which records move: the user needs data export privileges for an instrument to migrate its data, and **Full Data Set** export privileges on every instrument to migrate all records and instruments. REDCap shows a notice on the migration page when the user's export rights only cover some instruments. A user assigned to a **Data Access Group** migrates only the records of their own DAG, so a full migration should be run by a user who is not in a DAG.

> **Note — randomization:** the migration page may offer the randomization component to a user who holds only the Randomization **Dashboard** right, but the server only migrates randomization for a user with the Randomization **Setup** right. In that case the randomization component fails and holds up completion of the whole migration until it is finished automatically after several days (§3.4). Have the migration run by a user with Randomization Setup rights if the project uses randomization.

> **Important — you can only migrate what you can already access.** If the initiating user lacks privileges for a specific project component — Logging or the File Repository, for example — that component **cannot be migrated**. The tool does not elevate the user's access. A migration run by someone with partial rights produces a partial project, so the person initiating it should hold full rights in the source project.

## 2.4 Before you start — checklist

- Both servers are on 17.x, and both server teams have confirmed the trust configuration and the direct HTTPS connection between the servers (§2.1a).
- The destination has an active REDCap+ subscription that will stay active for the whole migration (§2.2, §3).
- You have the destination's **Instance ID** (§3.1).
- The initiating user has an API token, API Export, Project Design and Setup, Full Data Set export rights, Randomization Setup (if used), Logging and File Repository access, unexpired rights, and no DAG assignment (§2.3).
- Smart variables that return ID numbers have been replaced with name-based ones (§3.3).
- The External Modules the project uses are installed on the destination (§6.2.2).
- Data entry and survey collection on the source are paused for the migration window (§3).
- You have chosen the completion action deliberately — not **Delete project** (§4).

---

# 3. How a Migration Works

The PMT is a two-sided handshake built around a **migration key**.

1. **On the source instance** — a user generates a migration key from the project's **Other Functionality** page.
2. **On the destination instance** — a user creates a new project using that migration key.
3. The destination instance then **pulls** the project's components from the source using backend API processes driven by the REDCap **cron job**.

Because step 3 is cron-driven rather than interactive, a migration completes over time rather than instantly. On the destination, the new project shows a **Migration in Progress** dialog with how many of the selected components have finished ("X of Y"). Destination administrators can watch progress on the Project Migration Dashboard (§6). The source side has no equivalent dashboard: source administrators only see migrations as a count on the System Statistics page and as entries in the project's logging.

The cron job is the server's own scheduled task, not something set per project; if it is not running on the destination server, no migration progresses. The background jobs also stop if the destination's REDCap+ subscription lapses part-way through a migration.

> **Important — pause data entry on the source.** Records are pulled from the source **once**. Data entered or changed on the source after records have been pulled does not follow the project. Stop data entry and survey collection on the source (for example by telling the team and setting the surveys offline) before the destination project is created, and keep it stopped until the migration has completed.

## 3.1 The migration key

Two constraints on the key matter operationally:

- **It expires after three days.** A key generated and not used within that window is dead, and a new one must be generated.
- **It is bound to one destination.** Before the key is generated, the user enters the **Instance ID** of the intended destination. The key works only for the instance matching that ID.

The binding is a safety property rather than an obstacle — a leaked or mistakenly-shared key cannot be used to pull a project onto an arbitrary server. It does mean you need the destination's Instance ID before you start. The Instance ID is tied to the destination server's base URL, so if that server's address changes, its Instance ID changes too; get the current ID from the destination's administrators.

A key used on the wrong server is not rejected with a specific message. The destination shows the same generic error as every other key problem.

**Troubleshooting "The migration key provided was not valid".** This message is a catch-all. Check, in order:

- the key is less than three days old;
- the Instance ID entered on the source matches the destination exactly;
- the destination's trust configuration lists the source server (§2.1a);
- the user on the destination is allowed to create projects from a migration key under the destination's settings (§6.1);
- the destination could connect to the source when it tested the key;
- the initiating user on the source still has Project Design and Setup rights and unexpired project access (§2.3).

## 3.2 Choosing components

When generating the key, the user selects which components to migrate — and also the **completion action** for the source project (§4). Both are fixed into the key at that moment. The essential project features (fields, instruments, events) always come across. Components that hang off records — **File Upload and Signature files, record locking, survey participants and timestamps, the Field Comment Log and the Data Resolution Workflow** — can only be migrated if **Records** is also selected.

The Field Comment Log and the Data Resolution Workflow are offered as alternatives, not together: the page offers whichever of the two the source project uses.

## 3.3 What does not migrate, and what changes on arrival

| Item | What happens |
| --- | --- |
| Individual user rights assignments | Not migrated. Usernames differ between servers. User **role definitions** migrate; download the user rights CSV, update usernames and re-upload on the destination |
| User-to-DAG assignments | Not migrated. **DAG definitions** migrate; reassign users with the DAG CSV upload |
| Survey hash codes (survey links) | Change. Every survey link is new on the destination — see the redirect option in §4 |
| Event IDs and DAG IDs | Change. Smart variables that return an ID number, such as `[project-id]`, `[event-id]` or `[record-dag-id]`, will not work as expected. Replace them with name-based equivalents, such as `[event-name]` or `[record-dag-name]`, before migrating |
| Dynamic SQL fields | Converted to static drop-down fields |
| Alerts & Notifications send history (Notification Log), Survey Invitation Log | Not migrated. Alert and ASI *settings* migrate, but sent statuses do not |
| Alerts and ASIs on arrival | Arrive **enabled**. Review them, and deactivate any that should not fire, as soon as the destination project exists |
| Scheduled survey invitations | Not migrated. Reschedule them on the destination |
| ASIs | ASIs using `datediff` with today/now start triggering again on the destination; guard against re-sends (for example with `[form_complete]<>'2'` in the logic). Other ASIs must be re-evaluated |
| Project Bookmarks | Not migrated |
| MyCap participants | App configuration can migrate, but participants who already joined must rejoin and restart their scheduled tasks |
| Data Resolution Workflow queries | Migrated with timestamps, but the user on each query is shown as **"System"** |
| Field Comment Log entries | Migrated, but also lose the original user name |
| Record locks | Re-created on the destination, with **SYSTEM** shown as the user who locked |
| E-signatures | Not migrated. Records that were e-signed on the source arrive without the e-signature |
| Logging and Email Logging | Kept as separate pre-migration history (the **Legacy Logging** tab on the Logging page), not merged into the destination's log — see §1 |

> **Version caveat (16.0.x LTS):** Data Resolution Workflow import is 17.x only. If you migrate between two 16.0.x servers, expect the query history not to arrive; export the Data Resolution Workflow from the source first, or upgrade both servers to 17.x.

## 3.4 When the migration completes

Once all selected components have arrived:

- the new project takes the **status the source project had** (REDCap states this status in the confirmation dialog before the request is submitted),
- the user who created the project on the destination is **emailed a confirmation**, and
- the chosen **completion action** (§4) is applied to the source project **automatically**. There is no separate confirmation step at this point; the action was fixed when the key was generated.

**Migrations that do not finish on their own.** If some components never finish — for example the randomization case in §2.3 — REDCap finishes the migration automatically: after **2 days** if the records have arrived, or after **5 days** in any case. The migration is then marked completed and the chosen completion action is still applied to the source project, including **Delete project** if that was chosen. The only sign that something was left behind is the list of unfinished components in the confirmation email. Read that email carefully, and compare it with the dashboard row (§6.2).

---

# 4. Completion Actions

When generating the migration key, the user chooses what should happen to the **source** project once the migration completes. The choice is stored in the key and applied automatically at the end (§3.4) — there is no later opportunity to verify the destination first and then confirm. To change it, generate a new key.

| Option | Effect on the source project | When it is offered |
| --- | --- | --- |
| Leave as is | Nothing changes; the project remains fully active | Only if the source server's **Completion Action setting** displays the "Leave as is" option, or the user is a REDCap administrator. When offered, it is the **default** |
| Move to Analysis/Cleanup status | Moved to Analysis/Cleanup — data collection stops, data remains accessible | When the source project is not already in Analysis/Cleanup |
| Keep in Analysis/Cleanup | Nothing changes; the project stays in Analysis/Cleanup | Replaces both options above when the source project is already in Analysis/Cleanup (offered regardless of the setting) |
| Mark project as Completed | Hidden from users' project lists; members keep their place on the project but have no rights in it | Always. It is the **default** when "Leave as is" is not offered |
| Mark as Completed **and redirect public survey(s) to the new project** | As above, plus public survey links follow the project to its new home | Only if the project has public survey links |
| Delete project | Deleted, **restorable by an administrator** for the number of days set by the server's project-deletion delay (the page shows the number) | Always |

> **Institution-specific:** whether users see "Leave as is" is set by the administrators of the **source** server, in the Project Migration Tool settings on **Modules/Services Configuration** ("Completion Action setting"). If you need the source project to stay fully active and the option is missing, ask your REDCap administrators.

> **The redirect option is the one to think about.** If a project has public survey links in circulation — printed on materials, embedded in a web page, sent in an email — those links point at the *source* instance. Choosing "Mark as Completed and redirect public survey(s)" is what keeps them working after the move. Any other option leaves them pointing at a project that is no longer collecting data.

> **Important — do not choose "Delete project".** Because the completion action runs automatically, including when a stuck migration is finished after 2 or 5 days (§3.4), choosing Delete means the source can be deleted before anyone has checked the destination. Choose **Leave as is** or **Mark project as Completed** (or the redirect variant) instead, verify the destination project, and then delete the source project by hand. A deleted project is recoverable by an administrator for the server's project-deletion delay (shown on the page as "can be restored up to N days later by an admin"), but that is a grace period, not a backup.

---

# 5. Known Issues by Version

The PMT is a young feature and several defects affected what actually arrived at the destination. Each of these fails *quietly* — the migration reports success while something is missing.

> **Critical — files and signatures could be silently omitted (below 17.0.6 Standard).** Migrating a **longitudinal** project containing File Upload field files and/or Signature field files could fail to migrate some of those files, in specific situations. Fixed in 17.0.6. If a longitudinal project was migrated on 17.0.0–17.0.5, verify file and signature completeness at the destination rather than assuming it.

> **Critical — records could be silently dropped for failing validation (below 17.0.2 Standard).** Records containing data that **did not pass the field validation** of a field would not be migrated. Legacy projects commonly hold values that no longer satisfy current validation rules, so this is not a rare edge case. Fixed in 17.0.2. Compare record counts between source and destination.

> **Critical — the Development record limit could truncate a migration (below 17.1.4 Standard).** Where the system-level **Development Max Record Limit** was set, migrating a project with more records than that limit would fail to migrate all records — **even where the source project was in Production or Analysis/Cleanup status**, and so should not have been subject to a development limit at all. Fixed in 17.1.4. This one is particularly worth checking, because a large production project is exactly the kind you would migrate and exactly the kind that exceeds a development limit.

> **Version caveat (below 17.2.0 Standard):** In **longitudinal** projects, record-level **locking statuses and timestamps** might not be migrated. Since record locking is often part of a data-integrity or 21 CFR Part 11 posture, a migrated project could arrive with locks silently absent.

> **Version caveat (17.0.0 Standard only):** Migration log entries recorded the wrong values — the source instance's log listed the **source** URL where it should have listed the destination, and the destination's "Create project using Project Migration Tool" entry listed the **destination** Instance ID rather than the source. Fixed in 17.0.1. Migration audit entries from 17.0.0 should be read with that in mind.

> **Version caveat (below 17.1.4 Standard):** A PMT-related cron job could fail with a fatal PHP error when creating a new project, in rare cases.

**Practical implication:** on any version — and especially below 17.2.0 — treat a migration as needing verification rather than confirmation. Because the completion action is applied automatically when the migration ends, verification happens *after* it: choose a completion action that keeps the source (§4), then compare record counts, file counts and locking status between source and destination, and only then delete the source by hand if you need to.

---

# 6. Administrator Controls

## 6.1 Who may migrate projects in

Settings on the **Modules/Services Configuration** page in the Control Center govern migration into the instance. See [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md).

The main one is **"Allow users to use the Project Migration Tool to move projects TO THIS SERVER?"**, which requires a REDCap+ subscription. Its values:

| Value | Effect |
| --- | --- |
| Disabled: Hidden from everyone | No inbound migrations. The Project Migration Dashboard link is also hidden from the Control Center menu |
| Enabled: Visible only to administrators | Only administrators can create a project from a migration key |
| Enabled: Visible to all users (requires admin approval) | Users can submit a migration; an administrator must approve it before it starts |
| Enabled: Visible to all users (admin approval is NOT required) | Users can create the migrated project without administrator approval — but only users who are already allowed to create projects on this server, and only when project creation is not restricted to administrators. Everyone else still needs approval |

The note under this setting says an administrator will always be required to approve every migration request. On 17.x that only holds for the first three values; the last value lets users who may already create projects migrate without approval.

> **Version caveat (16.0.x LTS):** on the 16.0 LTS line there is no no-approval value: every inbound migration needs administrator approval. Plan for an approval step on a 16.0.x server, or upgrade to 17.x if users need to migrate without one.

The source server has a matching setting for migrating projects **off** the server (no subscription needed), with the **Completion Action setting** that controls whether users see the "Leave as is" completion action (§4).

## 6.2 Project Migration Dashboard

*Verified against 17.3.6 LTS.*

**Where:** Control Center → **Projects** section → **Project Migration Dashboard**. The menu entry carries a `REDCap+` badge and sits directly below *Edit Project Settings* and *Link Lookup*.

The page's stated purpose is to *"monitor the progress of all projects being migrated to this REDCap server instance using the Project Migration Tool."* Because migrations run through cron rather than interactively, this is where an administrator checks whether a migration is progressing, stalled or complete.

> **The dashboard is reachable without a subscription.** This was confirmed on a 17.3.6 LTS instance whose Control Center menu showed *"REDCap Plus Not Active"* — the page still loaded and rendered normally. That is the intended behaviour: any institution may use it, since any institution may be a migration *destination's* counterpart. See the version caveat in §2.2 for how the link is displayed (it can look greyed out without a subscription).

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
| Source Project Status | Development, Production or Analysis/Cleanup at the source (a Completed project cannot be migrated) |
| Source Completion Action | Which §4 completion action was chosen for the source project |

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

The per-component breakdown is the quickest first check, but it is not proof that everything arrived. Each component column shows only **"-"** (not finished) or **Completed**; a blank cell means the component was not selected. Read it this way:

- A component still showing "-" did **not** finish — whatever the overall status says. This is what you will see for a component left behind by a migration that was finished automatically after 2 or 5 days (§3.4).
- **Completed** means the tool has finished its part, not that every item arrived. **Records** shows Completed once the records have been handed to a background import on the destination, before that import has necessarily finished. File Upload files that fail to transfer twice are dropped, and the file component still shows Completed.

So use the dashboard to spot what clearly did not finish, then confirm the important things by hand: compare record counts, spot-check file and signature fields, and check locking and randomization on the destination before deleting anything on the source.

The table is searchable and pageable (10 / 25 / 50 / 100 / 500 / All rows, defaulting to 25) and shows the **newest migrations first** by default.

---

# 7. Common Questions

**Q: What does the Project Migration Tool move that a Project XML export does not?**

**A:** Record locking statuses and timestamps, survey participants and timestamps, File Repository folders and files including PDF Snapshots, randomization assignments and allocation tables, Logging, and Email Logging. A Project XML export carries the design and optionally the data, but none of those.

**Q: Do we need a REDCap+ subscription to use it?**

**A:** Only to receive projects. Moving a project **off** your instance does not require a subscription; moving a project **to** your instance does. An institution without REDCap+ can send but not receive.

**Q: The destination doesn't have REDCap+. Can we still move the project?**

**A:** Yes, by Project XML — the fallback route in [RC-PROJ-05 — Project Migration: Moving a Project Between REDCap Installations](RC-PROJ-05_Project-Migration.md). It moves the design and, optionally, the records and uploaded files, but not logging, randomization history, locking statuses or survey participants. If that history matters, ask whether the destination can subscribe before you move.

**Q: Both instances need to be on 17.0.0?**

**A:** Yes — in practice both on a 17.x release, with the server trust configuration (§2.1a) set up between them. The 16.0 LTS line has a reduced version of the tool, but a 16.0.x server and a 17.x server cannot migrate projects between each other because their migration keys are incompatible. Where one side cannot be upgraded, use the Project XML approach in [RC-PROJ-05 — Project Migration](RC-PROJ-05_Project-Migration.md).

**Q: The destination says the migration key is not valid, but it was generated today for the right server. Why?**

**A:** "Not valid" is a catch-all message. A common cause is that the destination server's trust configuration is missing or does not list the source server; ask the server administrators on both sides to check (§2.1a). (If the configuration is missing on the *source*, you would not have a key at all: generating it fails with an error on the source.) Other causes are a wrong Instance ID, a user on the destination who is not allowed to create migrated projects, a failed connection between the servers, or the source user having lost Project Design rights or access. Work through the troubleshooting list in §3.1.

**Q: Will user rights and survey links come across?**

**A:** Role definitions and DAG definitions do; individual user and DAG assignments do not, because usernames differ between servers. Survey links change, because survey hash codes are regenerated. See §3.3 for the full list.

**Q: How long is a migration key valid?**

**A:** Three days, and it only works for the destination instance whose Instance ID was entered before the key was generated. You need that Instance ID before you start. A wrong Instance ID is not reported specifically — the destination just says the key is not valid.

**Q: Our public survey links are printed on recruitment materials. Will they still work after migrating?**

**A:** Only if you choose the completion action **"Mark project as Completed and redirect public survey(s) to new project"**. Every other option leaves circulating links pointing at the source instance, where the project is no longer collecting data.

**Q: Why is the migration taking so long?**

**A:** The destination pulls components through backend API processes driven by the cron job, so a migration progresses over time rather than completing on submission. The destination project shows a **Migration in Progress** dialog with how many components have finished, and destination administrators can check progress on the Project Migration Dashboard. The cron job is server-wide: if it is not running on the destination server, no migration progresses, and the jobs also stop if the destination's REDCap+ subscription lapses mid-migration. A component that never finishes (for example randomization run without Setup rights) holds the migration open until it is finished automatically after 2 or 5 days (§3.4). See [RC-CC-02 — Control Center: General System Configuration](RC-CC-02_Control-Center-General-Configuration.md).

**Q: How do I check whether everything actually arrived?**

**A:** Use the **Project Migration Dashboard** in the Control Center. It reports a separate status for each of fifteen components — records, file-field uploads, locking, survey participants, Field Comment Log, Data Resolution Workflow and its files, calendar events, randomization, Logging, Email Logging, File Repository folders and files, PDF Snapshot Archive, and External Module settings. Start there: any component still showing "-" did not finish. But **Completed** does not prove every item arrived (records may still be importing in the background, and files that failed twice are dropped), so also compare record counts and spot-check files, locking and randomization by hand, and read the confirmation email's list of unfinished components (§6.2.3). The **Source REDCap Version** column tells you whether the migration was exposed to one of the defects in §5.

**Q: Do External Module settings come across?**

**A:** The *settings* do — the dashboard tracks them as a component. The *modules* do not. Settings for a module that is not installed and enabled on the destination have nothing to attach to, so confirm the destination has the same modules available before migrating.

**Q: Does the Data Resolution Workflow / query history survive?**

**A:** Yes, on 17.x. The Field Comment Log, the Data Resolution Workflow and its files are all migrated components, although the original user names are replaced (queries show "System"). So are Calendar events including record scheduling. This is a substantial difference from the Project XML route, which carries none of them. On the 16.0 LTS line, Data Resolution Workflow import is not available (§3.3).

**Q: A colleague ran the migration and the logs did not come across. Why?**

**A:** A user can only migrate components they have privileges for. Someone without Logging rights in the source project cannot migrate the log. Have the migration initiated by a user with full rights in the source project.

---

# 8. Common Mistakes & Gotchas

**Assuming a completed migration is a verified migration.** On versions below 17.2.0, several defects caused records, files, signatures and locking statuses to be omitted without any error. On any version, a stuck migration is finished automatically after 2 or 5 days and reported as completed even if components were left behind (§3.4), and a component showing Completed on the dashboard is not proof that every item arrived (§6.2.3). Check the dashboard row, the confirmation email and record and file counts before treating the move as done.

**Migrating a project whose External Modules are not present on the destination.** Module configuration settings migrate; the modules do not. Settings arriving for a module the destination does not have are settings with nothing to attach to.

**Choosing "Delete project" as the completion action.** The completion action is fixed when the key is generated and runs automatically when the migration ends — including when a stuck migration is finished after 2 or 5 days. Choosing Delete therefore deletes the source before anyone can check the destination. Choose Leave as is or Mark project as Completed, verify the destination, then delete the source by hand. The administrator restore window after deletion is a safety net, not a plan.

**Letting data entry continue on the source.** Records are pulled once. Anything entered on the source afterwards stays behind. Pause data entry and surveys on the source for the whole migration (§3).

**Regenerating the source API token or changing rights mid-migration.** The migration uses the token until the end. If the final step fails, the migration still shows as completed but the completion action is not applied to the source (§2.3).

**Forgetting that alerts and ASIs arrive enabled.** Review them on the destination straight away so participants are not contacted twice (§3.3).

**Forgetting that circulating survey links point at the old instance.** Public survey links do not follow the project unless you pick the redirect completion action. Recruitment materials, emails and embedded links keep pointing at the source.

**Running the migration as a user with partial rights.** The tool migrates only the components the initiating user can access. A migration run by someone without File Repository or Logging rights produces a project missing exactly those things, with nothing to indicate it.

**Generating a migration key too early.** Keys expire after three days and are bound to one destination Instance ID. Generate the key when you are ready to migrate, not while still planning.

**Assuming the subscription and Control Center settings are enough.** On 17.x the two servers must also be configured, at server level by their server administrators, to trust each other, and must be able to reach each other directly over HTTPS by public hostname (no outbound proxy, no private addresses). Without that, key generation fails on the source or the key is reported as not valid at the destination. Arrange it with both sides' server teams before planning a migration date.

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
