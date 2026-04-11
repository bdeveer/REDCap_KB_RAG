RC-DE-09

**Data Entry — Working with Data Access Groups**

| **Article ID** | RC-DE-09 |
|---|---|
| **Domain** | Data Entry |
| **Applies To** | Projects with Data Access Groups enabled; data entry users assigned to one or more DAGs |
| **Prerequisite** | RC-DE-02 — Basic Data Entry |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-DAG-01 — Data Access Groups; RC-DE-01 — Record Creation & the Record Home Page; RC-DE-02 — Basic Data Entry |

---

# 1. Overview

This article explains how Data Access Groups (DAGs) affect the data entry experience in REDCap. DAGs partition records within a project so that users from one group cannot see records belonging to another group — a common requirement in multi-site studies. This article covers the practical implications of DAGs for data entry users: what you can and cannot see, how record creation and assignment works, how record IDs behave when DAGs are active, and how to switch between DAGs if you are assigned to more than one. For information on how DAGs are created and configured, see RC-DAG-01 — Data Access Groups.

---

# 2. Key Concepts & Definitions

**Data Access Group (DAG)**

A named partition within a REDCap project that restricts which records a user can view and interact with. Users assigned to a DAG can only see records that belong to that DAG. DAGs are typically used to separate data by study site, institution, or team.

**DAG Assignment (Record)**

The association between a record and a DAG. Once a record is assigned to a DAG, only users in that DAG (and users with no DAG assignment) can view it. DAG assignment can be automatic (at record creation) or manual (set by a user without a DAG assignment).

**DAG Assignment (User)**

The association between a REDCap user account and one or more DAGs. A user's DAG assignment determines which records they can access. Users with no DAG assignment can see all records in the project.

**Active DAG**

When a user is assigned to multiple DAGs, the active DAG is the one currently in effect. Only records belonging to the active DAG are visible. The user can switch their active DAG between records.

---

# 3. Single DAG Assignment

If your user account is assigned to exactly one DAG, the experience is straightforward:

**Record visibility.** You can only see records that belong to your DAG. Records assigned to other DAGs are not visible to you anywhere in the project — not in the record list, the Record Status Dashboard, or search results.

**Record creation.** When you create a new record, it is automatically assigned to your DAG. No manual assignment step is required.

**Record ID numbering.** If the project uses auto-numbering for record IDs and DAGs are enabled, record IDs are generated from a combination of your DAG's group identifier and a sequential number (e.g., `Site-A-001`, `Site-A-002`). The exact format depends on how the project was configured.

---

# 4. Multiple DAG Assignment

If your user account is assigned to more than one DAG, the experience involves an additional concept: the active DAG.

**You are in one DAG at a time.** At any given moment, only one DAG is active for your session. You can only see and interact with records that belong to the currently active DAG.

**Switching your active DAG.** You can switch between your assigned DAGs at any time, provided you are not currently inside a record. Navigate out of any open record first, then click the blue **Switch** button displayed at the top of the screen and follow the prompts to select a different DAG. Once switched, you will see the records for the newly selected DAG.

**Record creation and viewing after switching.** After switching to a different active DAG, creating new records and viewing existing records works exactly as it does in the single-DAG scenario — all records you see belong to the currently active DAG, and any new record you create is automatically assigned to it.

> **Important:** You cannot switch your active DAG while you are inside a record. Navigate to the record list or Record Status Dashboard first, then switch.

---

# 5. No DAG Assignment

If your user account is not assigned to any DAG, your behavior is different from DAG-assigned users in several ways. This configuration is typically reserved for project managers and data managers rather than standard data entry staff.

**Record visibility.** You can see all records in the project, regardless of which DAG they belong to (or whether they belong to any DAG).

**Record creation — automatic assignment.** Creating a new record does not automatically assign it to a DAG. The record initially exists without a DAG assignment.

**Record creation — manual assignment at first instrument.** After creating the record and opening the first instrument, a DAG assignment dropdown appears in the top-right corner of the instrument. Use this dropdown to assign the record to the appropriate DAG. The assignment can also be left blank, in which case the record remains unassigned and visible to all users without a DAG restriction.

**Editing DAG assignment for existing records.** Users with no DAG assignment can reassign existing records to a different DAG (or remove a DAG assignment). To do this:

1. Navigate to the record's home page.
2. Click the **Choose Action for Record** button.
3. Select **Assign to Data Access Group** from the menu.
4. Choose the desired DAG from the dropdown in the popup.
5. Click **Assign to Data Access Group** to confirm.

> **Note:** The ability to reassign record DAGs is a data management function. Confirm with your project manager whether this action is expected of you before making changes.

---

# 6. Common Questions

**Q: I can't find a record that I know exists. What should I check?**

**A:** If you are assigned to multiple DAGs, verify which DAG is currently active. A record that belongs to a different DAG will not appear in your record list or dashboard until you switch to the correct DAG. Use the blue **Switch** button to change your active DAG.

**Q: I created a record but now I can't find it. What happened?**

**A:** If you switched your active DAG after creating the record, you are now viewing a different DAG's records and the record you created is not visible in the current context. Switch back to the DAG that was active when you created the record.

**Q: Can I move a record from one DAG to another?**

**A:** Only users with no DAG assignment can reassign records between DAGs. If you are assigned to one or more DAGs, you cannot change a record's DAG assignment. Contact your project manager if a record needs to be reassigned.

**Q: My record IDs look different from what I expected — they have a prefix I don't recognize. Why?**

**A:** When auto-numbering is active and DAGs are enabled, REDCap generates record IDs from a combination of the DAG's group identifier and a sequential number. The prefix is your site's DAG identifier. This behavior is configured at the project level.

**Q: I have no DAG assignment. Does that mean I can edit records from any DAG?**

**A:** Having no DAG assignment allows you to view all records, but your ability to edit those records depends on your user rights (instrument-level access, data entry rights, etc.), not on your DAG assignment. Data editing rights are controlled separately. See RC-USER-03 — User Rights: Configuring User Privileges.

**Q: Can I switch DAGs while I am inside a record?**

**A:** No. The option to switch your active DAG is only available when you are not inside a record. Save your work and navigate out of the current record first.

---

# 7. Common Mistakes & Gotchas

**Switching DAGs and then creating records unintentionally in the wrong DAG.** After switching your active DAG, any new records you create are automatically assigned to the newly active DAG. Confirm which DAG is active before creating new records, especially if you frequently switch between sites.

**Looking for records in the wrong active DAG.** The most common cause of "I can't find my record" for multi-DAG users is a stale active DAG selection. Always check the displayed active DAG before concluding that a record is missing.

**Leaving a new record unassigned when no DAG is set.** Users with no DAG assignment must manually assign new records to a DAG at the first instrument. If you skip this step, the record remains unassigned — visible to all unassigned users but potentially outside normal workflows for DAG-specific sites.

**Attempting to switch DAGs from within a record.** The DAG switch button is not available while a record is open. This is a system constraint, not a display error. Navigate back to the record list first.

---

## API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See RC-API-01 — REDCap API for authentication, token management, and setup.

- **RC-API-28 — Export DAGs API** — retrieve DAG definitions programmatically
- **RC-API-29 — Import DAGs API** — create or update DAG definitions programmatically
- **RC-API-30 — Delete DAGs API** — remove DAG definitions programmatically
- **RC-API-31 — Export User-DAG Assignments API** — retrieve which users are assigned to which DAGs
- **RC-API-32 — Import User-DAG Assignments API** — assign users to DAGs programmatically
- **RC-API-33 — Switch DAG API** — change the active DAG context for the token user programmatically

---


# 8. Related Articles

- RC-DAG-01 — Data Access Groups (covers DAG creation, configuration, and administrator management)
- RC-DE-01 — Record Creation & the Record Home Page (record creation workflow and the Choose Action for Record menu)
- RC-DE-02 — Basic Data Entry (foundational data entry skills)
- RC-USER-03 — User Rights: Configuring User Privileges (how data entry rights interact with DAG access)
