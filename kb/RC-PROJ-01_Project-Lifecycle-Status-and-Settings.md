RC-PROJ-01

**Project Lifecycle: Status and Settings**

| **Article ID** | RC-PROJ-01 |
|---|---|
| **Domain** | Project |
| **Applies To** | All REDCap projects |
| **Prerequisite** | None |
| **Version** | 1.2 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-INST-01 — Institution-Specific Settings & Policies; RC-FD-02 — Online Designer; RC-FD-03 — Data Dictionary; RC-NAV-UI-02 — Project Menu Reference; RC-CALC-01 — Special Functions Reference |

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

# 4. Copying a Project

Users with the right to create projects can navigate to **Project Setup → Other Functionality** to request a copy.

When copying, REDCap presents a checklist of items that can be included:

- Records
- User rights and roles
- Alerts & Notifications
- Reports
- Other project components

REDCap only shows options that are active in the source project.

> **Important:** Project logging is **never** copied. This includes record creation timestamps, survey timestamps, and project management history. The copy starts with a clean log.

---

# 5. Deleting a Project

**Development projects** can be deleted by project users via **Other Functionality → Delete the project**.

**Production projects** require a deletion request, which is sent to the REDCap administrator for approval.

After an administrator deletes a project:

- The project persists in the database for a configurable grace period (default: **30 days**) before permanent removal. During this window, a REDCap administrator can recover the project. The grace period duration is set by the administrator in the Control Center and may differ at your institution — check with your local support team if you need to know the exact window.
- Associated files take an additional 30 days beyond the grace period to be fully removed.

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
