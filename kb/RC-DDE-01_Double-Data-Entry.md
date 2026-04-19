RC-DDE-01

**Double Data Entry**

| **Article ID** | RC-DDE-01 |
|---|---|
| **Domain** | Double Data Entry |
| **Applies To** | All REDCap project types (except survey-only projects; see Section 7) |
| **Prerequisite** | RC-DE-02 — Basic Data Entry |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-DE-04 — Editing Data & Audit Trail; RC-USER-03 — User Rights: Configuring User Privileges; RC-EXPRT-01 — Data Export: Overview & Workflow |

---

# 1. Overview

Double Data Entry (DDE) is a data quality feature where every record is entered independently by two separate users, then compared and merged by a reviewer. The goal is to catch transcription errors: when both entries agree, confidence in the data is high; when they disagree, the discrepancy is surfaced and resolved before the data is finalized. DDE is common in clinical trials and any study context where the cost of a transcription error is high.

This article covers what DDE is, how to enable it, the three user roles it introduces, the full entry-and-merge workflow, and its limitations.

---

# 2. Key Concepts & Definitions

**Double Data Entry (DDE)**

A REDCap feature where each record is entered twice — once by a first data entry user and once by a second, independent user. The two entries are then reconciled by a reviewer who resolves any fields where the two entries differ.

**DDE Copy**

When DDE is enabled, each record ID becomes two parallel copies: one for the first data entry user (identified by the suffix `--1`) and one for the second user (identified by `--2`). These copies are independent — each user sees only their own copy. The reviewer sees both.

**Merged Record**

The final, authoritative version of the record created after the reviewer reconciles both copies. Fields where both entries agreed are accepted automatically. Fields where the two copies disagreed must be resolved by the reviewer before the merge can be saved. The merged record has no suffix and is the only copy included in exports.

**Reviewer**

The DDE-specific role responsible for comparing the two copies side by side and resolving discrepancies. The reviewer is the only user who can see both copies and the merged record simultaneously.

**Data Comparison Tool**

The REDCap interface used by the reviewer to compare and merge DDE copies. It presents a side-by-side comparison table showing differences between the two copies. Only records where both data entry persons have entered data appear in the tool's record selection list. The Data Comparison Tool is accessible from the left-hand project menu and only appears when DDE is enabled for the project.

---

# 3. Enabling Double Data Entry

### 3.1 Enabling the Feature

DDE is disabled by default and cannot be enabled by project owners or designers. It is controlled exclusively through a **project-specific setting** in the REDCap Control Center, which is only accessible to REDCap system administrators. If you want DDE enabled for your project, you must contact your REDCap administrator and request it.

Once a system administrator enables DDE for a project, the **Data Comparison Tool** appears in the left-hand project menu for users with Reviewer rights. Data entry users (#1 and #2) will not see this tool — it is only visible to reviewers.

> **Important:** Once DDE is enabled and data collection has begun, disabling it is not recommended. Contact your REDCap administrator before requesting any change to this setting on a live project.

### 3.2 Effect on Existing Records

If DDE is enabled after records already exist in the project, those records do not automatically get split into two copies. The DDE workflow applies to newly created records going forward. Pre-existing records remain in a single-copy state and cannot participate in the standard DDE merge workflow.

---

# 4. DDE User Roles

Enabling DDE adds a new setting to every user's configuration in **User Rights**. There are three DDE-specific roles:

| DDE Role | Can See | Can Enter Data |
|---|---|---|
| **Data Entry Person #1** | Their own copy only (`--1` records) | Yes — first data entry copy |
| **Data Entry Person #2** | Their own copy only (`--2` records) | Yes — second data entry copy |
| **Reviewer** | Both copies and the merged record | Yes — resolves discrepancies during merge |

> **Note:** DDE user rights are separate from standard user rights. A user can have full data entry access in standard user rights but still be restricted to one DDE role. Assign DDE roles deliberately based on who is responsible for first entry, second entry, and reconciliation.

Multiple users can share the same DDE role. For example, a team of five data entry coordinators can all be assigned Data Entry Person #1 — they will collectively enter first-pass copies across all records.

---

# 5. Workflow: From Creation to Merge

### 5.1 Record Creation

A user creates a new record in the usual way (Add/Edit Records → Add new record). REDCap creates both copies simultaneously: `[recordID]--1` and `[recordID]--2`.

- Data Entry Person #1 sees and enters data into `[recordID]--1`.
- Data Entry Person #2 sees and enters data into `[recordID]--2`.
- Each user's Record Status Dashboard shows only their own copies.

There is no enforced sequence — both copies can be entered in any order and are independent of each other. REDCap does not prevent one copy from being complete while the other is still empty.

### 5.2 First and Second Data Entry

Each data entry user works through their copy as they would in a normal project: opening instruments, entering data, and saving. The standard instrument save options (incomplete, unverified, complete) apply to each copy independently.

Neither data entry user can see what the other has entered. This independence is intentional — it prevents one user's entries from influencing the other's, which would undermine the error-detection purpose of DDE.

### 5.3 Merging Records (Reviewer Workflow)

Once both copies are ready to be reviewed, the reviewer uses the **Data Comparison Tool**:

1. Navigate to **Data Comparison Tool** in the left-hand project menu (visible only to reviewers).
2. Select a record from the list. Only records where both data entry persons have submitted data appear in this list — records with only one copy entered will not be available.
3. Click **Compare**. REDCap displays a comparison table showing all fields side by side.
4. Fields where both entries agree are shown in green and accepted automatically — no reviewer action is needed.
5. Fields where the entries differ are highlighted and require the reviewer to select a value:
   - Choose the value from Copy 1
   - Choose the value from Copy 2
   - Enter a new, corrected value

6. After resolving all discrepancies, the reviewer saves the merge.

REDCap saves the resolved values as the **merged record** (the record without a suffix). The two copies remain in the system after merging and can still be accessed by the reviewer for audit purposes.

> **Best practice:** Resolve all discrepancies in a single session. REDCap requires that all flagged fields be resolved before the merge can be saved — any unresolved field will prevent saving.

### 5.4 Exporting Merged Data

Only merged records are included in standard data exports. The `--1` and `--2` copies are excluded from exports by default. If a record has not yet been merged, it will not appear in the export output.

This means that a project's exported dataset reflects only the reconciled, reviewer-approved data — not interim copies.

---

# 6. Common Questions

**Q: Do both data entry users have to finish their copy before the reviewer can merge?**

**A:** No. REDCap does not enforce a completion requirement before the reviewer can access the Data Comparison Tool. However, if one copy is incomplete when the merge is performed, fields that were not entered in that copy will appear blank in the comparison and the reviewer will need to resolve the discrepancy. Best practice is to ensure both copies are fully entered before merging.

**Q: Can one person do both first and second entry?**

**A:** Technically yes — a user can be assigned Reviewer rights, which allows them to access both copies. However, this defeats the purpose of DDE. The error-detection value of DDE depends on the two entries being genuinely independent. If the same person does both, or if one person knows what the other entered, the second pass is not a meaningful check. Ensure your team structure maintains actual independence between the two data entry passes.

**Q: What happens to the --1 and --2 copies after a merge?**

**A:** They remain in the system. The copies are not deleted after merging. Reviewers and administrators can still access them for audit purposes. They are simply excluded from standard data exports.

**Q: Can the reviewer change a value to something neither copy entered?**

**A:** Yes. During the merge, the reviewer can type a new value into any discrepant field instead of selecting one of the two copies' entries. This is appropriate when both entries appear to be wrong and the reviewer has determined the correct value from another source (e.g., original source documents).

**Q: Can I use DDE with a longitudinal project?**

**A:** Yes. DDE is compatible with longitudinal projects. The `--1` and `--2` copies exist across all events and arms in the same way they do in a classic project.

**Q: Does DDE interact with the Data Resolution Workflow?**

**A:** The Data Resolution Workflow (DRW) can be enabled alongside DDE. DRW queries can be opened on either the `--1` or `--2` copy by the reviewer. However, the interaction between DDE and DRW adds complexity — plan both features carefully before enabling them together.

---

# 7. Limitations

**Repeating instruments and events have partial support only.** The Data Comparison Tool does not fully support the Repeating Instruments and Events feature. If repeating instruments or repeating events are enabled in the project, comparison and merging is limited to **Instance #1** only. All other repeating instances (Instance #2, #3, etc.) are ignored by the tool and will not be compared or merged. Non-repeating data is not affected and can be compared and merged normally. If your project relies heavily on repeated data collection, evaluate this limitation carefully before using DDE.

**Surveys are not compatible with DDE.** Instruments enabled as surveys are not collected in the DDE workflow. If a participant submits a survey response, that response is stored once and does not generate two independent copies. Projects that rely primarily on survey-based data collection should not use DDE.

**Records created before DDE was enabled cannot be merged.** Pre-existing records are in a single-copy state. The Data Comparison Tool is only available for records that were created after DDE was enabled.

**Calculated fields compute independently on each copy.** Calculated field values are computed on each copy based on that copy's data. After merging, calculated fields are recomputed on the merged record. If you resolve a discrepancy in a field that feeds a calculated field, the calculation will update to reflect the merged value.

**Action tags operate per copy.** Action tags such as `@HIDDEN`, `@READONLY`, and autofill tags apply to each copy independently during data entry.

**File upload fields.** Both copies require a file to be uploaded independently. During the merge, the reviewer selects which copy's file attachment to keep.

---

# 8. Common Mistakes & Gotchas

**Not assigning DDE roles before data collection begins.** When DDE is first enabled by the administrator, users retain their standard access but have no DDE role assigned. A user without a DDE role assigned may see both copies or no copies depending on REDCap version and configuration. Once the administrator confirms DDE is active, assign DDE roles to all project users before data collection starts.

**Using DDE with instruments that are also surveys.** Survey-completed instruments do not participate in the DDE workflow. If a project has a mix of staff-entered and survey-completed instruments, only the staff-entered instruments go through the two-copy entry and merge process. Design your project to account for this hybrid behavior before enabling DDE.

**Performing the merge before both copies are complete.** If one copy is partially entered at the time of merge, blank fields in that copy will appear as discrepancies against the other copy's values. The reviewer will need to manually select the correct value for every such field — a tedious and error-prone process. Establish a team workflow that confirms both copies are complete before any merge is initiated.

**Expecting the --1 and --2 copies to appear in exports.** Data managers who are unfamiliar with DDE sometimes look for all three copies in an export (both entry copies plus the merged record) and are confused when only the merged record appears. Exports contain only the merged record. To review the raw entry copies, use the REDCap interface directly.

**Misunderstanding what "independent" means.** DDE only provides error-detection value if the two data entry passes are genuinely independent. If data entry users communicate about their entries, or if one user sees a source document that was annotated by the other, the second pass will tend to agree with the first regardless of accuracy. Train your team that the integrity of DDE depends on strict independence.

---

# 9. Related Articles

- RC-DE-02 — Basic Data Entry (foundational data entry skills required before using DDE)
- RC-DE-04 — Editing Data & Audit Trail (audit trail behavior in DDE; the --1 and --2 copies each have their own audit trail)
- RC-USER-03 — User Rights: Configuring User Privileges (DDE role assignment; how DDE rights interact with standard user rights)
- RC-EXPRT-01 — Data Export: Overview & Workflow (understanding that only merged records appear in exports)
- RC-DE-12 — Data Resolution Workflow (can be used alongside DDE for additional data quality tracking)
