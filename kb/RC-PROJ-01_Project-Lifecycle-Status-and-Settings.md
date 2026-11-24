

**Project Lifecycle: Status and Settings**

| **Article ID** | [RC-PROJ-01 — Project Lifecycle: Status and Settings](RC-PROJ-01_Project-Lifecycle-Status-and-Settings.md) |
|---|---|
| **Domain** | Project |
| **Applies To** | All REDCap projects |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.5.4 (Standard) / v17.3.18 (LTS) — changelog review; page not re-captured. Completed-project listing and access checked against source code of v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS). Project status, Draft Mode and project management behaviour checked against source code of v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) |
| **Prerequisite** | None |
| **Version** | 1.12 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-CC-04 — Control Center: User Settings & Defaults](RC-CC-04_Control-Center-User-Settings.md); [RC-CC-09 — Control Center: To-Do List](RC-CC-09_To-Do-List.md); [RC-INST-01 — Institution-Specific Settings & Policies — Production](RC-INST-01_Institution-Specific-Settings-and-Policies.md); [RC-FD-02 — Online Designer](RC-FD-02_Online-Designer.md); [RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md); [RC-NAV-UI-02 — Project Menu Reference](RC-NAV-UI-02_Project-Menu-Reference.md); [RC-CALC-01 — Special Functions Reference](RC-CALC-01_Special-Functions-Reference.md) |
| **Synonyms** | how do i move my project to production; what are the project statuses; difference between development and production mode; how to copy or delete a project; make design changes after going to production; enter draft mode to edit a live project; project lifecycle stages explained; change project status settings |

---

## 1. Overview

Every REDCap project passes through a defined lifecycle, from initial build through active data collection to final completion. Understanding which status your project is in — and what that status allows or restricts — is essential for managing your study correctly.

This article covers the four project statuses, how to move between them, how to copy or delete a project, and how to safely make design changes once your project is in Production.

---

## 2. Project Statuses

Every REDCap project exists in one of four lifecycle statuses.

### 2.1 Development

The starting state for all new projects. In Development:

- All design decisions take effect in real time — no approval process is required.
- Data entry and survey features can be tested freely.
- No production safeguards are in place.

Development is intended for building and testing your project before live data collection begins.

**Record limit in Development:** REDCap supports an optional record limit for Development projects. When a limit is configured, the project will not allow new records to be created once the limit is reached — encouraging teams to move to Production for actual data collection. The limit behavior works as follows:

- A default limit can be set institution-wide in the Control Center by a REDCap administrator.
- An administrator can also set a different limit on a per-project basis. A project-level value greater than zero overrides the default; a value of zero means "use the system default".
- The limit applies to every Development project, including ones created before the limit was configured. There is no grandfathering and no way to exempt a single project: an administrator can only give it a different (higher) positive limit.
- Records that already exist above the limit are kept; only the creation of new records is blocked.

### 2.2 Production

The active data collection state. In Production:

- Changes to fields and instruments require **Draft Mode** and a review/approval process.
- Events and arms are **not** part of Draft Mode. In Production, only a REDCap administrator can add or edit events and arms, unless a Control Center setting allows normal users to add or modify them. Deleting or renaming events and arms stays administrator-only.
- This protects existing data from accidental modification or deletion.
- Surveys, alerts, automated invitations, and all standard features remain fully active.

**To move to Production:** Click the "Move project to Production" button at the bottom of the Project Setup page. REDCap will prompt you to either delete all test data or retain it. Best practice is to delete all test data before going live. Choosing to delete removes all records and survey responses, survey invitations, record locking and e-signatures, and data export files stored in the File Repository; files that users uploaded to the File Repository themselves are kept. If randomization is enabled and records have already been randomized, the dialog shows an extra warning (17.4.4+ Standard; not in 17.3.31 LTS or 16.0.61 LTS, where only the generic confirmation appears). If you retain the records, REDCap keeps them but clears the randomization variable for every model, so they are no longer randomized — see [RC-RAND-03 — Working with & Managing Randomization](RC-RAND-03_Working-with-Randomization.md).

> **Why move to Production?** Moving to Production preserves data accuracy and integrity. The post-production change control process provides a safety check to prevent accidental deletion, recoding, or overwriting of data that has already been collected.

### 2.3 Analysis/Cleanup

Indicates that formal data collection is complete. In Analysis/Cleanup:

- Most active data collection features are **disabled**: surveys, automated survey invitations, and alerts & notifications.
- **No new records** can be created.
- Existing data remains intact and fully accessible.
- Existing records can be set to either **Editable** (existing records only) or **Read-only/Locked**. Changing this mode needs Project Design rights.
- In **Read-only/Locked** mode, users lose the ability to rename, delete and lock records, and record imports through the Data Import Tool and the API are blocked.
- Scheduled alerts and automated survey invitations are held, not discarded: they send once the project is returned to Production.
- An administrator can optionally configure surveys that users must complete before changing a project's status.

From Analysis/Cleanup, a project can return to Production or be moved to Completed.

### 2.4 Completed

Indicates the project is fully done.

- It is removed from the main My Projects list for every user, including the project owner.
- Members can still see it under the **"Show Completed Projects"** link at the bottom of the My Projects page, marked **Completed**, and the project name is still a link.
- Opening it gives a member no access. REDCap removes all of that user's project rights for as long as the project is Completed, so the project menu is essentially empty and no data can be viewed, entered or exported. Their rights are kept, not deleted, and work again if the project is returned to its previous status.
- REDCap's confirmation message says marking a project Completed takes it **offline**. In practice the project's online/offline setting is not changed: what blocks members is the removal of their rights.
- Only a REDCap administrator can return a Completed project to its previous status.

> **Note on legacy statuses:** Prior to REDCap version 9.8.0 (standard) / 10.0.5 (LTS), projects used "Inactive" and "Archived" statuses. These were automatically migrated: Inactive → Analysis/Cleanup; Archived → Analysis/Cleanup within the renamed "My Hidden Projects" folder.

---

## 3. Status Transitions

| From | To | Who Can Do It |
|---|---|---|
| Development | Production | User with Project Design rights (via Project Setup); where your institution requires approval, the user submits a request and an administrator makes the move |
| Production | Analysis/Cleanup | User with Project Design rights (via Project Setup) |
| Analysis/Cleanup | Production | User with Project Design rights (via Project Setup) |
| Any status (Development, Production or Analysis/Cleanup) | Completed | User with Project Design rights (**Other Functionality → Mark project as Completed**) |
| Production | Development | **REDCap administrator only** |
| Completed | Previous status | **REDCap administrator only** |

Moving a Production project back to Development requires a REDCap administrator. Contact your local support team to request this. REDCap does not offer this move for projects that use randomization or Data Transfer Services (DTS). When it is done, any pending draft is discarded and the project's moved-to-production time is reset.

---

## 4. Copying and Backing Up a Project

### 4.1 Copying a Project

Users with **Project Design** rights in the source project can copy it from **Project Setup → Other Functionality**. The copy is made directly, unless project creation at your institution is restricted to administrators, in which case the copy becomes a request to an administrator.

When copying, REDCap presents a checklist of items that can be included:

- Records (unchecked by default)
- User rights and roles
- Alerts & Notifications
- Reports
- Other project components

Options that do not apply to the source project are disabled.

- **Alerts and automated survey invitations are copied deactivated.** Re-activate the ones you need in the copy. Alerts that were already deactivated in the source are not copied at all.
- Where a Development record limit is set, a non-administrator cannot copy records into a new project if the record count is over the limit.

> **Important:** Project logging is **never** copied. This includes record creation timestamps, survey timestamps, and project management history. The copy starts with a clean log.

> **Version caveat (below 17.4.3 Standard / 17.3.9 LTS):** The **Record-level Locking Enhancement** setting (PDF confirmation and automatic external file storage) was not carried over to the copy. Re-enable it by hand in copies made on older versions.

> **Version caveat (below 17.5.1 Standard / 17.3.14 LTS):** Where project creation is admin-only and an administrator performed the copy for a requesting user, the new project used the **administrator's** email as the From address for ASIs, Alerts & Notifications and survey confirmation emails. Check From addresses in copies made this way on older versions.

### 4.2 Downloading a Backup (XML / CDISC ODM)

REDCap can export the entire project — or just its structure — as an XML file in **CDISC ODM format**. Two options are available from **Other Functionality**:

- **Download metadata only (XML)** — Exports all instruments, fields, project attributes, and settings, but no record data.
- **Download metadata & data (XML)** — Exports the full project including all records and data.

The resulting XML file can be used to:
- Clone the project on the same REDCap server or on a different REDCap server (upload it on the Create New Project page).
- Import the project into another ODM-compatible system.

> **Note:** Like a project copy, the exported XML does **not** contain the project's logging history (audit trail). Download the full log from the top of the Logging page if you need it.

---

> **Record limit and project copying (15.5.5+).** Where the system-level "Record limit for development projects" is enabled, **administrators can bypass the limit when copying a project**, so a legitimate copy of a large project is not blocked by a limit intended to constrain new development work.

> **Project deletion purge delay (15.2.6+).** A system setting defines the number of days between a project being deleted and being **purged** from the system. Until the purge runs, a deleted project is recoverable — which makes this setting the practical answer to "can we get it back?" See [RC-CC-02 — Control Center: General System Configuration](RC-CC-02_Control-Center-General-Configuration.md).

> **Project Home statistics.** The stats table on the Project Home page shows the **number of instruments**, and for longitudinal projects the **number of events and arms** (16.0.7), plus **when the project was created, moved to production, and moved to analysis/cleanup** (16.0.9). Those timestamps are the quickest way to establish a project's lifecycle history without reading the log.

> **Cache clearing without admin rights (16.1.8+).** Non-admin users holding **Project Design** rights can clear the Record List Cache and the page-level Rapid Retrieval cache from the Other Functionality page. Previously this required an administrator, which made a routine troubleshooting step into a support request.

---

## 5. Data Management

### 5.1 Deleting a Project

**Development projects** can be deleted by users with Project Design rights via **Other Functionality → Delete the project**.

**Production and Analysis/Cleanup projects** cannot be deleted by non-administrators. Instead they see **Request delete project**, which sends the request to the REDCap administrator for approval.

After any project is deleted, whoever deleted it:

- The project persists in the database for a configurable grace period (default: **30 days**, minimum 1 day) before it is purged. During this window, a REDCap administrator can recover the project. The grace period is set by the administrator in the Control Center (General Configuration) and may differ at your institution — check with your local support team if you need to know the exact window.
- Administrators also have a **delete immediately** option, which skips the grace period. A project deleted this way cannot be recovered.
- Associated files are removed 30 days after the project is purged.

### 5.2 Erasing All Data

> **Bulk Record Delete.** The page has gained several capabilities: **background deletion** as an alternative to synchronous processing, useful on large record sets (15.6.0); clearer instructional text (15.8.4); a UI rule where unselecting an instrument within a selected event also unselects the event, with improved arm validation in multi-arm projects (17.2.0); and an option to delete **all records from a report**, so a report becomes the selection mechanism for a bulk delete (17.4.0).
>
> **Critical — the "all records from a report" option deserves care.** It makes it trivial to delete a large, precisely-specified set of records in one action. Verify the report returns exactly what you expect *before* using it as a delete target, and remember that report filters can behave unexpectedly against form status fields on older versions — see [RC-NAV-REC-04 — Record Status Dashboard & Other Record Links](RC-NAV-REC-04_Record-Status-Dashboard-and-Links.md).

> **Version caveat (below 17.1.4 Standard):** Partial record deletion via Bulk Record Delete **ignored record-level locks** — the selected forms had their data deleted inside a locked record. REDCap's own wording: locked records should not be editable in any way. Fixed in 17.1.4, which also clarified that the "Delete entire records" option deliberately deletes regardless of lock status, while **partial** deletes now respect locking. If record locking was part of your data-integrity controls before 17.1.4, it did not cover this path.

**Other Functionality → Erase all data** removes all currently collected data while keeping the project structure (instruments, fields, settings) intact. This is distinct from deleting the project entirely.

**Who can use it:** users with Project Design rights while the project is in **Development**. In Production and Analysis/Cleanup, only a REDCap administrator can erase all data.

**What IS erased:**
- All record data (including survey responses)
- Documents uploaded to File Upload fields on forms and surveys (marked for deletion and removed by a scheduled background job)
- Calendar events
- Archived data export files stored in the File Repository
- Logged events that pertain to data collection (the data-related part of the audit trail)
- Queued automated survey invitations
- E-signatures, record locking and randomization assignments
- Survey participants who had responded, and placeholder Participant List entries created for follow-up surveys that have no email address or phone number

**What is NOT erased:**
- Survey logos
- Participant List entries that never responded, and public survey link entries
- Files uploaded by users directly into the File Repository (as opposed to files attached to records via forms)

> **Caution:** This action is irreversible. REDCap will ask you to confirm before proceeding. Use this only when you are certain all data in the project should be discarded — for example, when cleaning up after a test phase before real data collection begins.

### 5.3 Bulk Record Delete

**Other Functionality → Bulk Record Delete** allows you to delete multiple records in a single operation, or to delete data for multiple instruments across multiple records without removing the records themselves.

This is useful when you need to selectively clear data — for example, deleting a batch of test records, or removing all data for a specific instrument across a cohort of records before re-collecting it.

The Bulk Record Delete page presents filter options to select which records (and optionally which instruments) to target before deletion.

### 5.4 Clearing Record and Page Caches

**(Users with Project Design rights; administrators only on 16.0 LTS)** If records appear to be missing from the project, or if some pages (reports, Record Status Dashboard, etc.) are not reflecting recent data changes, the internal caches may be out of sync. Use **Other Functionality → Clear all record & page caches** to resolve this.

Two caches are cleared by this action:

- **Record List Cache** — A secondary index of all record names maintained by REDCap for performance. If this falls out of sync, certain records may not appear in drop-down lists or the Record Status Dashboard even though the underlying data is intact.
- **Rapid Retrieval** — A page-level cache that stores rendered versions of frequently accessed pages to speed up load times. If a page is returning stale data, clearing this cache forces REDCap to re-render it from the database.

Clearing both caches causes the Record List Cache to regenerate and removes all stored page-level caches for the project. This is safe to do at any time, though REDCap notes it is normally not needed.

> **Version caveat (16.0 LTS):** On 16.0.x LTS (checked on 16.0.61), **Clear all record & page caches** is available to REDCap administrators only. From 16.1.8 Standard, and on 17.x Standard and LTS, any user with Project Design rights can use it. On 16.0 LTS, ask your REDCap administrator to clear the caches.

While the Record List Cache is rebuilding (status **Processing**), REDCap blocks **renaming records** and **changing a record's DAG assignment** until the build finishes (17.5.3 Standard / 17.3.16 LTS onward), to keep the cache consistent. If either action is refused shortly after clearing caches or a large import, wait and retry.

---

## 6. Making Production Changes

Once your project is in Production, all instrument design changes must go through **Draft Mode**.

### 6.1 Process Overview

1. Click **"Enter Draft Mode"** on the Online Designer or Data Dictionary page.
2. Make your changes within Draft Mode.
3. Review a detailed summary of all drafted changes by clicking the hyperlink at the top of the page.
4. Click **"Submit Changes for Review."**

Depending on your institution's configuration, some changes are processed automatically while others require REDCap administrator approval. See [RC-INST-01 — Institution-Specific Settings & Policies — Production](RC-INST-01_Institution-Specific-Settings-and-Policies.md) for your institution's specific policy and expected review times.

> **The project does not go offline during review.** All functionality — including survey collection and data entry — continues normally while changes await approval.

### 6.2 Change Risk Flags

During draft review, REDCap flags potentially harmful changes to fields that already hold data:

| Flag (as shown on screen) | Meaning |
|---|---|
| **\*Possible data loss if field type changes. Check if okay.** | The field's type was changed, so existing values may no longer fit it |
| **\*Data MIGHT be lost due to deleted choice(s)** | One or more choices were removed from a radio, dropdown or checkbox field that has data |
| **\*Possible label mismatch because of label changes** | The label of a choice that has data was changed, which may alter the meaning of existing data |
| **\*Possible data loss if a matrix field's label changes** | A matrix field's label was changed |

Review these flags carefully before submitting. A flagged change on a field that has data counts as a **critical issue** for draft auto-approval (see section 8).

### 6.3 Rules for Safe Production Changes

Follow these rules to protect your data when modifying a production project:

**Do not rename existing variable names.** Data stored for those variables will be lost from view: it is no longer accessible in forms, reports or exports. To recover, restore the original variable name in a new draft; the values reappear because REDCap does not purge them.

> **Important — removed fields and choices are hidden, not purged.** When a field is deleted or renamed, its data is no longer accessible in forms, reports or exports, but REDCap does not purge it, and it can reappear if a field with the same variable name is created again. So deleting a field is not a way to remove sensitive data, and avoid reusing old variable names for new questions. Download a backup of your data before approving destructive changes. REDCap also keeps an automatic data dictionary snapshot before every Data Dictionary upload and API metadata import, listed on **Project Revision History**, which helps you restore a previous design.
>
> Deleting or renaming an **instrument** is different: its record locking, e-signatures, event designations, repeating settings, MyCap tasks and instrument-level user rights are permanently lost. Files in deleted File Upload fields are marked for deletion when the draft is approved.

**Do not rename existing form names via a data dictionary upload.** Form completeness data will be lost. Form names *can* be changed within the Online Designer without data loss.

**Do not modify codes for existing dropdown, radio, or checkbox choices.** Existing data will be lost or misinterpreted. To reorder or add choices, keep existing codes unchanged and use the next available code number.

> **Example:** If choices are `1, red | 2, yellow | 3, blue` and you want to add "green" and display in alphabetical order, do **not** recode existing choices. Instead, extend the list: `3, blue | 4, green | 1, red | 2, yellow`. The display order can be changed freely; the underlying codes must stay the same.

**Adding new choices** has no impact on existing stored data. Note, however, that analytically it changes the question for records that completed the instrument before the new option existed.

**Deleting a radio, dropdown or checkbox choice** removes that option from future data entry, and values already stored for it are no longer accessible in forms, reports or exports. REDCap does not purge them: if a choice with the same code is added back, the old values reappear. If the field has data, REDCap flags the change as **\*Data MIGHT be lost due to deleted choice(s)**. Never reuse a deleted choice's code for a different answer.

### 6.4 Events in Longitudinal Projects

Deleting events in a longitudinal project requires administrator action. If events are deleted:

- Data tied to those events is **not erased** — it becomes "orphaned" in the system.
- Data for remaining events is not affected unless branching logic or calculations referenced the deleted events.

### 6.5 Draft Preview Mode

Draft Preview Mode lets you test your drafted changes — including branching logic, calculations, action tags, and embedded fields — exactly as they would behave if approved and live, before you submit them for review.

**Activating Draft Preview Mode:** While your project is in Draft Mode, open the Online Designer and enable Draft Preview Mode from there. It is active only for your own user account and only for the duration of your current REDCap session. Other users are not affected.

**How it works:** Draft Preview Mode simulates live data entry on your existing forms using the currently drafted (not yet approved) design. Any data you enter is *ephemeral* — it is held in your session only and is never saved to the project. When you exit Draft Preview Mode or your session ends, all entered data disappears.

**Limitations:** The following restrictions apply while in Draft Preview Mode:

- No new records can be created
- No data entered on forms is saved to the project — form data entry is transient and disappears when you leave Draft Preview Mode. This does **not** cover imports: data imported (Data Import Tool or API) while you are in Draft Preview Mode changes the real project data.
- Only changes to **already-existing forms** can be previewed; new forms added in Draft Mode cannot be previewed
- Delete operations (deleting whole records or form/event data) are disabled
- Record locking and form-level locking/unlocking are disabled
- Randomization and the Randomization module are disabled
- Field Comment Log, Data Resolution Workflow, and Data History Popup are disabled
- No Alerts, Automated Survey Invitations (ASIs), or Data Entry Triggers will fire
- Form Display Logic is disabled
- Draft Preview Mode operates only on data entry pages, the Record Status Dashboard, and the Record Home Page — it does not affect other pages and **does not work on survey pages**

> See also: [RC-FD-02 — Online Designer](RC-FD-02_Online-Designer.md); [RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md); [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md)

---

## 7. Common Questions

**Q: How do I move my project from Development to Production?**

**A:** Go to the **Project Setup** page and click "Move project to Production" at the bottom of the page. REDCap will prompt you to delete or retain test data — best practice is to delete all test data before going live.

---

**Q: Can I move a Production project back to Development?**

**A:** Yes, but only a REDCap administrator can do this. Contact your local support team with the request.

---

**Q: My Draft Mode changes haven't appeared after submission. Are they lost?**

**A:** They are not lost. They are most likely in the administrator review queue. See [RC-INST-01 — Institution-Specific Settings & Policies — Production](RC-INST-01_Institution-Specific-Settings-and-Policies.md) for your institution's expected review time. Contact the support team if the wait seems excessive or if the change is urgent.

---

**Q: Can I copy a project and bring over all existing records?**

**A:** Yes. When copying, REDCap presents a checklist of items to include — records is one of the available options. Note that project logging (timestamps, history) is never copied.

---

**Q: I accidentally renamed a variable in my Data Dictionary upload to a Production project. What do I do?**

**A:** Revert to the original variable name immediately, before the draft is approved. If the change has already been approved and applied, restore the original variable name in a new draft: REDCap does not purge the old values, so they reappear once a field with that name exists again. The automatic data dictionary snapshot on **Project Revision History** shows the previous design. Contact your REDCap administrator if you need help.

---

**Q: What happens to data when I delete a checkbox option in Production?**

**A:** The values stored for that option are no longer accessible in forms, reports or exports, and REDCap warns you with the **\*Data MIGHT be lost due to deleted choice(s)** flag during draft review. REDCap does not purge the values: if the option is added back with the same code, they reappear. So deleting an option is not a way to remove sensitive data, and never reuse its code for a different answer.

---

**Q: Where can I view projects in "Completed" status?**

**A:** On the **My Projects** page, scroll to the bottom and click **"Show Completed Projects."** That lists the Completed projects you were a member of. You can click a project's name, but you will have no rights inside it: the menu is essentially empty. Only a REDCap administrator can return it to its previous status.

---

**Q: Can I test my drafted changes before submitting them for approval?**

**A:** Yes — use **Draft Preview Mode**, available from the Online Designer while your project is in Draft Mode. It lets you interact with your forms as if the drafted changes were live, including branching logic, calculations, action tags, and embedded fields. Any data you enter on forms is ephemeral and never saved to the project (imports made during preview do change real data). Note that Draft Preview Mode does not work on survey pages and cannot preview forms that are entirely new in the current draft.

---

**Q: Will Draft Preview Mode affect other users or trigger any automations?**

**A:** No. Draft Preview Mode is active only for your own user account and only for your current session. Other users see and work with the project normally. No alerts, automated survey invitations, or Data Entry Triggers will fire while you are in Draft Preview Mode.

---

**Q: What is the difference between "Erase all data" and "Delete the project"?**

**A:** "Erase all data" removes all records and collected data while keeping the project structure (instruments, fields, settings) fully intact. You can continue using the project afterward. "Delete the project" removes the entire project — structure and data — and it can only be recovered during a brief administrator-controlled grace period. Use "Erase all data" when you want to discard test data and start fresh; use "Delete the project" only when the project itself is no longer needed.

---

**Q: Records seem to be missing from the Record Status Dashboard or reports. Is the data gone?**

**A:** Probably not. This symptom is often caused by the Record List Cache falling out of sync with the actual data. Go to **Other Functionality → Clear all record & page caches** (users with Project Design rights; administrators only on 16.0 LTS) to force the cache to rebuild. The records should reappear after the page refreshes. If the issue persists after clearing the cache, contact your REDCap administrator.

---

**Q: Some pages in my project show old data even after I updated records. How do I fix this?**

**A:** This is typically the Rapid Retrieval page cache serving a stored version of the page. Go to **Other Functionality → Clear all record & page caches** (users with Project Design rights; administrators only on 16.0 LTS) to clear the page cache and force REDCap to re-render from the database.

---

**Q: I'm copying a real study project to use as a demonstration or training template. What should I review before sharing it?**

**A:** Projects derived from real studies frequently contain institution-specific content that should be removed or replaced before the project is shared outside your team or used as a generic template. The most common categories to review:

- **Staff and provider names in field choices.** Radio, dropdown, and checkbox fields that let users select an interviewer, clinician, or coordinator often list real names as coded options. Export the Data Dictionary CSV and search for names; replace them with generic placeholders (e.g., "Provider 1," "Staff Member A").
- **Institution or program names in field labels and field notes.** Descriptive text, section headers, and field notes may reference your site, department, or sponsor. Search the Label and Field Note columns of the exported Data Dictionary.
- **Protocol- or program-specific identifiers in eligibility or tracking forms.** Eligibility waiver forms, screening logs, or tracking instruments may name a specific protocol, grant, or care program. Replace with a generic study program label.
- **Contact information.** Phone validation fields, or descriptive fields containing an email address or URL, should be cleared or replaced with placeholder values.
- **Project title and project notes.** These are visible to anyone with project access. Genericize the title and clear the notes field before sharing.

The safest workflow is: copy the project → erase all data in the copy → export the copy's Data Dictionary as CSV → review and edit the CSV offline → re-upload the sanitized Data Dictionary. Do not rely on the Online Designer alone — searching a CSV for real names is far faster and more reliable than clicking through each field individually. Re-import the metadata while the copy is still in Development so no draft approval is needed.

---

## 8. Administrator Configuration

Several aspects of the project lifecycle are controlled by system-wide settings in the Control Center under System Configuration → User Settings & Defaults (see **[RC-CC-04 — Control Center: User Settings & Defaults](RC-CC-04_Control-Center-User-Settings.md)**):

**Project creation rights** — Administrators configure whether all authenticated users can create new projects, or whether users must submit a request that goes to the administrator for approval. In restricted environments, users see a "Request New Project" button instead of a "New Project" button, and the resulting request appears in the administrator's To-Do List (see **[RC-CC-09 — Control Center: To-Do List](RC-CC-09_To-Do-List.md)**).

**Moving projects to Production** — Administrators control whether project owners can self-approve production moves, or whether an administrator must approve the transition. In environments that require approval, users see a "Request To Move to Production" button and the request enters the administrator's To-Do List.

**Draft Mode auto-approval** — Administrators configure whether certain categories of Draft Mode changes are automatically approved without requiring manual administrator review. There are five options, from strictest to most permissive:

| Option (summarised) | A draft is auto-approved when |
|---|---|
| Never | Never — every draft needs an administrator |
| No existing fields modified | The draft only adds new fields |
| No records, or no existing fields modified | The project has no records, or the draft only adds new fields |
| No critical issues | The draft has no critical issues |
| No records, or no fields with data deleted and no critical issues | The project has no records (then **any** draft is approved), or the draft deletes no fields that hold data and has no critical issues |

A **critical issue** is a flagged change (section 6.2) on a field that has data, a change to the record ID field while records exist, or deleting or moving the e-Consent anchor field. Deleting fields that hold data is assessed separately from critical issues. Administrators can also block auto-approval when new fields match identifier keywords. In most production environments, a conservative threshold is used to protect data integrity. Changes that do require review appear in the To-Do List.

> **See also:** [RC-CC-04 — Control Center: User Settings & Defaults](RC-CC-04_Control-Center-User-Settings.md); [RC-CC-09 — Control Center: To-Do List](RC-CC-09_To-Do-List.md)

---

## 9. Related Articles

- [RC-CC-04 — Control Center: User Settings & Defaults](RC-CC-04_Control-Center-User-Settings.md) (project creation rights, production approval, draft auto-approval)
- [RC-CC-09 — Control Center: To-Do List](RC-CC-09_To-Do-List.md) (where draft approvals and project requests appear)
- [RC-FD-02 — Online Designer](RC-FD-02_Online-Designer.md) (making design changes in Development and Draft Mode)
- [RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md) (alternative approach to making structural changes)
- [RC-INST-01 — Institution-Specific Settings & Policies — Production](RC-INST-01_Institution-Specific-Settings-and-Policies.md) (institution-level guidance on production approval timelines)
- [RC-PROJ-02 — Project Setup Checklist](RC-PROJ-02_Project-Setup-Checklist.md) (dependency-ordered checklist covering all phases of project configuration from creation through go-live)
- [RC-NAV-UI-01 — Project Navigation UI](RC-NAV-UI-01_Project-Navigation-UI.md) (how project status is displayed in the interface and what changes at each stage)
- [RC-NAV-UI-02 — Project Menu Reference](RC-NAV-UI-02_Project-Menu-Reference.md) (the Project Home and Design menu section where status is shown and managed)
- [RC-NAV-UI-04 — My Projects Page](RC-NAV-UI-04_My-Projects-Page.md) (project list, folders, search, and how Completed projects appear)
