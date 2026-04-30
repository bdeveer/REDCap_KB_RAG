RC-PROJ-01

**Project Lifecycle: Status and Settings**

| **Article ID** | RC-PROJ-01 |
|---|---|
| **Domain** | Project |
| **Applies To** | All REDCap projects |
| **Prerequisite** | None |
| **Version** | 1.4 |
| **Last Updated** | 2026-04-29 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-CC-04 — Control Center: User Settings & Defaults; RC-CC-09 — Control Center: To-Do List; RC-INST-01 — Institution-Specific Settings & Policies; RC-FD-02 — Online Designer; RC-FD-03 — Data Dictionary; RC-NAV-UI-02 — Project Menu Reference; RC-CALC-01 — Special Functions Reference |

---

# 1. Overview

Every REDCap project passes through a defined lifecycle, from initial build through active data collection to final completion. Understanding which status your project is in — and what that status allows or restricts — is essential for managing your study correctly.

This article covers the four project statuses, how to move between them, how to copy or delete a project, and how to safely make design changes once your project is in Production.

---

# 2. Project Statuses

Every REDCap project exists in one of four lifecycle statuses.

## 2.1 Development

The starting state for all new projects. In Development:

- All design decisions take effect in real time — no approval process is required.
- Data entry and survey features can be tested freely.
- No production safeguards are in place.

Development is intended for building and testing your project before live data collection begins.

**Record limit in Development:** REDCap supports an optional record limit for Development projects. When a limit is configured, the project will not allow new records to be created once the limit is reached — encouraging teams to move to Production for actual data collection. The limit behavior works as follows:

- A default limit can be set institution-wide in the Control Center by a REDCap administrator.
- An administrator can also set or override the limit on a per-project basis.
- **Projects that existed before this feature was introduced are grandfathered in** with no limit initially, even if a default is configured. An administrator can manually assign a limit to a legacy project if needed.

## 2.2 Production

The active data collection state. In Production:

- All structural changes (fields, forms, events) require **Draft Mode** and a review/approval process.
- This protects existing data from accidental modification or deletion.
- Surveys, alerts, automated invitations, and all standard features remain fully active.

**To move to Production:** Click the "Move project to Production" button at the bottom of the Project Setup page. REDCap will prompt you to either delete all test data or retain it. Best practice is to delete all test data before going live.

> **Why move to Production?** Moving to Production preserves data accuracy and integrity. The post-production change control process provides a safety check to prevent accidental deletion, recoding, or overwriting of data that has already been collected.

## 2.3 Analysis/Cleanup

Indicates that formal data collection is complete. In Analysis/Cleanup:

- Most active data collection features are **disabled**: surveys, automated survey invitations, and alerts & notifications.
- **No new records** can be created.
- Existing data remains intact and fully accessible.
- An administrator can set existing records to either **Editable** (existing records only) or **Read-only/Locked**.

From Analysis/Cleanup, a project can return to Production or be moved to Completed.

## 2.4 Completed

Indicates the project is fully done.

- The project is taken **offline** and hidden from all users' project lists.
- Only a REDCap administrator can access the project or change its status.
- To view completed projects, use the **"Show Completed Projects"** link at the bottom of the My Projects page.

> **Note on legacy statuses:** Prior to REDCap version 9.8.0 (standard) / 10.0.5 (LTS), projects used "Inactive" and "Archived" statuses. These were automatically migrated: Inactive → Analysis/Cleanup; Archived → Analysis/Cleanup within the renamed "My Hidden Projects" folder.

---

# 3. Status Transitions

| From | To | Who Can Do It |
|---|---|---|
| Development | Production | Project user (via Project Setup) |
| Production | Analysis/Cleanup | Project user (via Project Setup) |
| Analysis/Cleanup | Production | Project user (via Project Setup) |
| Analysis/Cleanup | Completed | Project user (via Project Setup) |
| Production | Development | **REDCap administrator only** |
| Completed | Any | **REDCap administrator only** |

Moving a Production project back to Development requires a REDCap administrator. Contact your local support team to request this.

---

# 4. Copying and Backing Up a Project

## 4.1 Copying a Project

Users with the right to create projects can navigate to **Project Setup → Other Functionality** to request a copy.

When copying, REDCap presents a checklist of items that can be included:

- Records
- User rights and roles
- Alerts & Notifications
- Reports
- Other project components

REDCap only shows options that are active in the source project.

> **Important:** Project logging is **never** copied. This includes record creation timestamps, survey timestamps, and project management history. The copy starts with a clean log.

## 4.2 Downloading a Backup (XML / CDISC ODM)

REDCap can export the entire project — or just its structure — as an XML file in **CDISC ODM format**. Two options are available from **Other Functionality**:

- **Download metadata only (XML)** — Exports all instruments, fields, project attributes, and settings, but no record data.
- **Download metadata & data (XML)** — Exports the full project including all records and data.

The resulting XML file can be used to:
- Clone the project on the same REDCap server or on a different REDCap server (upload it on the Create New Project page).
- Import the project into another ODM-compatible system.

> **Note:** Like a project copy, the exported XML does **not** contain the project's logging history (audit trail). Download the full log from the top of the Logging page if you need it.

---

# 5. Data Management

## 5.1 Deleting a Project

**Development projects** can be deleted by project users via **Other Functionality → Delete the project**.

**Production projects** require a deletion request, which is sent to the REDCap administrator for approval.

After an administrator deletes a project:

- The project persists in the database for a configurable grace period (default: **30 days**) before permanent removal. During this window, a REDCap administrator can recover the project. The grace period duration is set by the administrator in the Control Center and may differ at your institution — check with your local support team if you need to know the exact window.
- Associated files take an additional 30 days beyond the grace period to be fully removed.

## 5.2 Erasing All Data

**Other Functionality → Erase all data** removes all currently collected data while keeping the project structure (instruments, fields, settings) intact. This is distinct from deleting the project entirely.

**What IS erased:**
- All record data (including survey responses)
- Calendar events
- Documents uploaded onto forms and surveys
- Archived data export files stored in the File Repository
- Logged events that pertain to data collection

**What is NOT erased:**
- File attachments uploaded to File Upload fields (stored separately from record data)
- Survey logos
- Survey participants in the Participant List
- Files uploaded by users directly into the File Repository (as opposed to files attached to records via forms)

> **Caution:** This action is irreversible. REDCap will ask you to confirm before proceeding. Use this only when you are certain all data in the project should be discarded — for example, when cleaning up after a test phase before real data collection begins.

## 5.3 Bulk Record Delete

**Other Functionality → Bulk Record Delete** allows you to delete multiple records in a single operation, or to delete data for multiple instruments across multiple records without removing the records themselves.

This is useful when you need to selectively clear data — for example, deleting a batch of test records, or removing all data for a specific instrument across a cohort of records before re-collecting it.

The Bulk Record Delete page presents filter options to select which records (and optionally which instruments) to target before deletion.

## 5.4 Clearing Record and Page Caches

**(Administrators only)** If records appear to be missing from the project, or if some pages (reports, Record Status Dashboard, etc.) are not reflecting recent data changes, the internal caches may be out of sync. Use **Other Functionality → Clear all record & page caches** to resolve this.

Two caches are cleared by this action:

- **Record List Cache** — A secondary index of all record names maintained by REDCap for performance. If this falls out of sync, certain records may not appear in drop-down lists or the Record Status Dashboard even though the underlying data is intact.
- **Rapid Retrieval** — A page-level cache that stores rendered versions of frequently accessed pages to speed up load times. If a page is returning stale data, clearing this cache forces REDCap to re-render it from the database.

Clearing both caches causes the Record List Cache to regenerate and removes all stored page-level caches for the project. This is safe to do at any time, though REDCap notes it is normally not needed.

---

# 6. Making Production Changes

Once your project is in Production, all instrument design changes must go through **Draft Mode**.

## 6.1 Process Overview

1. Click **"Enter Draft Mode"** on the Online Designer or Data Dictionary page.
2. Make your changes within Draft Mode.
3. Review a detailed summary of all drafted changes by clicking the hyperlink at the top of the page.
4. Click **"Submit Changes for Review."**

Depending on your institution's configuration, some changes are processed automatically while others require REDCap administrator approval. See RC-INST-01 for your institution's specific policy and expected review times.

> **The project does not go offline during review.** All functionality — including survey collection and data entry — continues normally while changes await approval.

## 6.2 Change Risk Flags

During draft review, REDCap flags potentially harmful changes:

| Flag | Meaning |
|---|---|
| **\*Possible label mismatch** | A coded value's label was changed, which may alter the meaning of existing data |
| **\*Possible data loss** | A change may cause stored data to become ambiguous |
| **\*Data WILL be lost** | The change will permanently delete stored data (e.g., deleting a checkbox option) |

Review these flags carefully before submitting. Changes flagged as **Data WILL be lost** cannot be undone.

## 6.3 Rules for Safe Production Changes

Follow these rules to protect your data when modifying a production project:

**Do not rename existing variable names.** Data stored for those variables will be lost. To recover, revert to the original variable name immediately.

**Do not rename existing form names via a data dictionary upload.** Form completeness data will be lost. Form names *can* be changed within the Online Designer without data loss.

**Do not modify codes for existing dropdown, radio, or checkbox choices.** Existing data will be lost or misinterpreted. To reorder or add choices, keep existing codes unchanged and use the next available code number.

> **Example:** If choices are `1, red | 2, yellow | 3, blue` and you want to add "green" and display in alphabetical order, do **not** recode existing choices. Instead, extend the list: `3, blue | 4, green | 1, red | 2, yellow`. The display order can be changed freely; the underlying codes must stay the same.

**Adding new choices** has no impact on existing stored data. Note, however, that analytically it changes the question for records that completed the instrument before the new option existed.

**Deleting a radio or dropdown choice** does not change stored data but removes that option from future data entry.

**Deleting a checkbox choice** permanently deletes the stored 0/1 values for that option. REDCap flags this as **Data WILL be lost**.

## 6.4 Events in Longitudinal Projects

Deleting events in a longitudinal project requires administrator action. If events are deleted:

- Data tied to those events is **not erased** — it becomes "orphaned" in the system.
- Data for remaining events is not affected unless branching logic or calculations referenced the deleted events.

## 6.5 Draft Preview Mode

Draft Preview Mode lets you test your drafted changes — including branching logic, calculations, action tags, and embedded fields — exactly as they would behave if approved and live, before you submit them for review.

**Activating Draft Preview Mode:** While your project is in Draft Mode, open the Online Designer and enable Draft Preview Mode from there. It is active only for your own user account and only for the duration of your current REDCap session. Other users are not affected.

**How it works:** Draft Preview Mode simulates live data entry on your existing forms using the currently drafted (not yet approved) design. Any data you enter is *ephemeral* — it is held in your session only and is never saved to the project. When you exit Draft Preview Mode or your session ends, all entered data disappears.

**Limitations:** The following restrictions apply while in Draft Preview Mode:

- No new records can be created
- No data is saved to the project — all data entry is transient and disappears when you leave Draft Preview Mode
- Only changes to **already-existing forms** can be previewed; new forms added in Draft Mode cannot be previewed
- Delete operations (deleting whole records or form/event data) are disabled
- Record locking and form-level locking/unlocking are disabled
- Randomization and the Randomization module are disabled
- Field Comment Log, Data Resolution Workflow, and Data History Popup are disabled
- No Alerts, Automated Survey Invitations (ASIs), or Data Entry Triggers will fire
- Form Display Logic is disabled
- Draft Preview Mode operates only on data entry pages, the Record Status Dashboard, and the Record Home Page — it does not affect other pages and **does not work on survey pages**

> See also: RC-FD-02 — Online Designer; RC-FD-03 — Data Dictionary; RC-LONG-01 — Longitudinal Project Setup

---

# 7. Common Questions

**Q: How do I move my project from Development to Production?**

**A:** Go to the **Project Setup** page and click "Move project to Production" at the bottom of the page. REDCap will prompt you to delete or retain test data — best practice is to delete all test data before going live.

---

**Q: Can I move a Production project back to Development?**

**A:** Yes, but only a REDCap administrator can do this. Contact your local support team with the request.

---

**Q: My Draft Mode changes haven't appeared after submission. Are they lost?**

**A:** They are not lost. They are most likely in the administrator review queue. See RC-INST-01 for your institution's expected review time. Contact the support team if the wait seems excessive or if the change is urgent.

---

**Q: Can I copy a project and bring over all existing records?**

**A:** Yes. When copying, REDCap presents a checklist of items to include — records is one of the available options. Note that project logging (timestamps, history) is never copied.

---

**Q: I accidentally renamed a variable in my Data Dictionary upload to a Production project. What do I do?**

**A:** Revert to the original variable name immediately, before the draft is approved. If the change has already been approved and applied, contact your REDCap administrator — recovery may still be possible depending on the database backup policy at your institution.

---

**Q: What happens to data when I delete a checkbox option in Production?**

**A:** The stored 0/1 values for that checkbox option are permanently deleted. REDCap warns you with the **Data WILL be lost** flag during draft review. This cannot be undone.

---

**Q: Where can I view projects in "Completed" status?**

**A:** On the **My Projects** page, scroll to the bottom and click **"Show Completed Projects."** Only a REDCap administrator can change a project's status once it reaches Completed.

---

**Q: Can I test my drafted changes before submitting them for approval?**

**A:** Yes — use **Draft Preview Mode**, available from the Online Designer while your project is in Draft Mode. It lets you interact with your forms as if the drafted changes were live, including branching logic, calculations, action tags, and embedded fields. Any data you enter is ephemeral and never saved to the project. Note that Draft Preview Mode does not work on survey pages and cannot preview forms that are entirely new in the current draft.

---

**Q: Will Draft Preview Mode affect other users or trigger any automations?**

**A:** No. Draft Preview Mode is active only for your own user account and only for your current session. Other users see and work with the project normally. No alerts, automated survey invitations, or Data Entry Triggers will fire while you are in Draft Preview Mode.

---

**Q: What is the difference between "Erase all data" and "Delete the project"?**

**A:** "Erase all data" removes all records and collected data while keeping the project structure (instruments, fields, settings) fully intact. You can continue using the project afterward. "Delete the project" removes the entire project — structure and data — and it can only be recovered during a brief administrator-controlled grace period. Use "Erase all data" when you want to discard test data and start fresh; use "Delete the project" only when the project itself is no longer needed.

---

**Q: Records seem to be missing from the Record Status Dashboard or reports. Is the data gone?**

**A:** Probably not. This symptom is often caused by the Record List Cache falling out of sync with the actual data. Go to **Other Functionality → Clear all record & page caches** (administrators only) to force the cache to rebuild. The records should reappear after the page refreshes. If the issue persists after clearing the cache, contact your REDCap administrator.

---

**Q: Some pages in my project show old data even after I updated records. How do I fix this?**

**A:** This is typically the Rapid Retrieval page cache serving a stored version of the page. Go to **Other Functionality → Clear all record & page caches** (administrators only) to clear the page cache and force REDCap to re-render from the database.

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

# 8. Administrator Configuration

Several aspects of the project lifecycle are controlled by system-wide settings in the Control Center under System Configuration → User Settings & Defaults (see **RC-CC-04**):

**Project creation rights** — Administrators configure whether all authenticated users can create new projects, or whether users must submit a request that goes to the administrator for approval. In restricted environments, users see a "Request New Project" button instead of a "New Project" button, and the resulting request appears in the administrator's To-Do List (see **RC-CC-09**).

**Moving projects to Production** — Administrators control whether project owners can self-approve production moves, or whether an administrator must approve the transition. In environments that require approval, users see a "Request To Move to Production" button and the request enters the administrator's To-Do List.

**Draft Mode auto-approval** — Administrators configure whether certain categories of Draft Mode changes are automatically approved without requiring manual administrator review. Options range from "never auto-approve" (all changes require admin sign-off) to "auto-approve if no critical issues exist." In most production environments, a conservative threshold is used to protect data integrity. Changes that do require review appear in the To-Do List.

> **See also:** RC-CC-04 — Control Center: User Settings & Defaults; RC-CC-09 — Control Center: To-Do List

---

# 9. Related Articles

- RC-CC-04 — Control Center: User Settings & Defaults (project creation rights, production approval, draft auto-approval)
- RC-CC-09 — Control Center: To-Do List (where draft approvals and project requests appear)
- RC-FD-02 — Online Designer (making design changes in Development and Draft Mode)
- RC-FD-03 — Data Dictionary (alternative approach to making structural changes)
- RC-INST-01 — Institution-Specific Settings & Policies (institution-level guidance on production approval timelines)
- RC-PROJ-02 — Project Setup Checklist (dependency-ordered checklist covering all phases of project configuration from creation through go-live)
- RC-NAV-UI-01 — Project Navigation UI (how project status is displayed in the interface and what changes at each stage)
- RC-NAV-UI-02 — Project Menu Reference (the Project Home and Design menu section where status is shown and managed)
