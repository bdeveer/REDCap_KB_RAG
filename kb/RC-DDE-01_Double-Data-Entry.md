

**Double Data Entry**

| **Article ID** | [RC-DDE-01 — Double Data Entry](RC-DDE-01_Double-Data-Entry.md) |
|---|---|
| **Domain** | Double Data Entry |
| **Applies To** | All REDCap project types (except survey-only projects; see Section 7) |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — double data entry and Data Comparison Tool behaviour checked against source code; pages not re-captured |
| **Prerequisite** | [RC-DE-02 — Basic Data Entry](RC-DE-02_Basic-Data-Entry.md) |
| **Version** | 1.2 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-DE-04 — Editing Data & Audit Trail](RC-DE-04_Editing-Data-and-Audit-Trail.md); [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md); [RC-EXPRT-01 — Data Export: Overview & Workflow](RC-EXPRT-01_Data-Export-Overview-and-Workflow.md) |
| **Synonyms** | how do i enable double data entry; enter each record twice and compare; catch transcription errors with two data entry users; reconcile and merge discrepant entries; set up dde reviewer role; two independent data entry users workflow; compare two versions of a record; double key data entry for clinical trials |

---

## 1. Overview

Double Data Entry (DDE) is a data quality feature where every record is entered independently by two separate users, then compared and merged by a reviewer. The goal is to catch transcription errors: when both entries agree, confidence in the data is high; when they disagree, the discrepancy is surfaced and resolved before the data is finalized. DDE is common in clinical trials and any study context where the cost of a transcription error is high.

This article covers what DDE is, how to enable it, the three user roles it introduces, the full entry-and-merge workflow, and its limitations.

---

## 2. Key Concepts & Definitions

**Double Data Entry (DDE)**

A REDCap feature where each record is entered twice — once by a first data entry user and once by a second, independent user. The two entries are then reconciled by a reviewer who resolves any fields where the two entries differ.

**DDE Copy**

When DDE is enabled, each record ID exists as two parallel copies: one entered by Data Entry Person #1 (identified by the suffix `--1`) and one entered by Data Entry Person #2 (identified by `--2`). Each person creates their own copy; REDCap adds the suffix when the record is saved. The copies are independent — each data entry person sees only their own copy, everywhere in the project. Reviewers see both.

**Merged Record**

The final, authoritative version of the record created after the reviewer reconciles both copies. Fields where both entries agreed are carried over automatically. For fields where the two copies disagreed, the reviewer picks the value to keep. The merged record has no suffix. It is the version to analyse, but it is not the only version in a Reviewer's exports — see §5.4.

**Reviewer**

The DDE role responsible for comparing the two copies and resolving discrepancies. Every project user who is not Data Entry Person #1 or #2 is a Reviewer, and sees all records: the `--1` copies, the `--2` copies and the merged records.

**Data Comparison Tool**

The REDCap page used to compare two records. It exists in every project (where it compares any two records) and appears in the left-hand project menu for users with the **Data Comparison Tool** user right. When DDE is enabled, the tool switches to DDE mode: it compares the `--1` and `--2` copies of a record and lets a Reviewer merge them. Only records where both data entry persons have saved a copy appear in its record list, and the comparison works per event. Data Entry Person #1 and #2 cannot open it.

---

> **Version caveat (below 15.8.2 Standard):** For users acting as **DDE person 1 or 2**, clicking some form status icons on the Record Status Dashboard or Record Home Page did not open the expected form. Fixed in 15.8.2. Separately, below 17.0.2 a DDE person 1 or 2 attempting to **rename a record** from the Record Home Page saw a confusing error and was blocked; the message was corrected in 17.0.2.

---

## 3. Enabling Double Data Entry

#### 3.1 Enabling the Feature

DDE is disabled by default and cannot be enabled by project owners or designers. It is controlled exclusively through a **project-specific setting** in the REDCap Control Center, which is only accessible to REDCap system administrators. If you want DDE enabled for your project, you must contact your REDCap administrator and request it.

Once a system administrator enables DDE for a project, the **Data Comparison Tool** works in DDE mode for Reviewers who have the Data Comparison Tool user right. Data Entry Person #1 and #2 cannot open it.

> **Important:** Do not combine DDE with record auto-numbering. REDCap warns that this combination will produce errors, because both data entry persons must create their copy under the same record ID. Turn auto-numbering off and agree on record IDs in advance (for example, the ID on the paper case report form).

> **Important:** REDCap also warns that DDE is not compatible with randomization. Discuss this with your administrator before enabling both in one project.

> **Important:** Once DDE is enabled and data collection has begun, disabling it is not recommended. Contact your REDCap administrator before requesting any change to this setting on a live project.

#### 3.2 Effect on Existing Records

If DDE is enabled after records already exist in the project, those records do not automatically get split into two copies. The DDE workflow applies to newly created records going forward. Pre-existing records remain in a single-copy state and cannot participate in the standard DDE merge workflow.

---

## 4. DDE User Roles

Enabling DDE adds a DDE setting to every user's configuration in **User Rights**. There are three DDE roles:

| DDE Role | Can See | Can Enter Data |
|---|---|---|
| **Data Entry Person #1** | Their own copy only (`--1` records) | Yes — first data entry copy |
| **Data Entry Person #2** | Their own copy only (`--2` records) | Yes — second data entry copy |
| **Reviewer** | All records: `--1` copies, `--2` copies and merged records | Yes — merges copies in the Data Comparison Tool and can edit records |

There is no "unassigned" state: every user who is not Data Entry Person #1 or #2 is a Reviewer. This includes the project creator and anyone added later, so check the DDE setting of every user before data collection begins.

> **Note:** DDE user rights are separate from standard user rights. A user can have full data entry access in standard user rights but still be restricted to one DDE role. Assign DDE roles deliberately based on who is responsible for first entry, second entry, and reconciliation.

**One user per slot.** Only one user at a time can be Data Entry Person #1, and only one can be Data Entry Person #2. Once a user holds a slot, User Rights no longer offers it to other users. To hand a slot to someone else, first change the current holder to Reviewer.

**What data entry persons cannot do.** To keep the two passes independent, Data Entry Person #1 and #2 cannot open pages that would show the other copy or other users' activity, including Logging, File Repository, Data Import Tool, Data Exports, Reports and Stats, Data Quality, Calendar, the Data Comparison Tool, and e-signature and locking management. They cannot export or import data through the API either. They can delete or rename only records that carry their own suffix.

---

## 5. Workflow: From Creation to Merge

#### 5.1 Record Creation

Each data entry person creates their own copy of the record in the usual way (Add/Edit Records → enter the record ID). Both persons use the same record ID; REDCap adds the suffix when the record is saved.

- Data Entry Person #1 enters record `101`; on saving, it is stored as `101--1`.
- Data Entry Person #2 enters record `101`; on saving, it is stored as `101--2`.
- Each person's Record Status Dashboard and record lists show only their own copies.

Creating one copy does not create the other. There is no enforced sequence — the copies can be entered in any order, and REDCap does not prevent one copy from being complete while the other does not exist yet.

#### 5.2 First and Second Data Entry

Each data entry user works through their copy as they would in a normal project: opening instruments, entering data, and saving. The standard instrument save options (incomplete, unverified, complete) apply to each copy independently.

Neither data entry user can see what the other has entered. This independence is intentional — it prevents one user's entries from influencing the other's, which would undermine the error-detection purpose of DDE.

#### 5.3 Merging Records (Reviewer Workflow)

Once both copies are ready to be reviewed, the reviewer uses the **Data Comparison Tool**:

1. Navigate to **Data Comparison Tool** in the left-hand project menu.
2. Select a record (in longitudinal projects, a record and event) from the list. Only records where both data entry persons have saved a copy appear — records with only one copy will not be available.
3. Click **Compare selected record**. REDCap lists only the fields where the two copies **differ**. Fields where both entries agree are not shown; they are copied from the `--1` copy into the merged record automatically.
   - Alternatively, click **Compare all records** to see the differences for every eligible record on one page.
4. Click the link to merge the two records. For each differing field, choose:
   - the value from Copy 1 (pre-selected by default),
   - the value from Copy 2, or
   - a new, corrected value.
5. Save the merge.

REDCap saves the result as the **merged record** (the record ID without a suffix) and logs the action as **Merge records**. If both copies belong to the same Data Access Group, the merged record is placed in that group too. The two copies remain in the project after merging and Reviewers can still open them.

> **Important:** Copy 1 is pre-selected for every differing field, so the merge can be saved without touching anything — in which case Copy 1 wins every discrepancy. Review each listed field deliberately before saving.

Once a record has been merged for an event, the Data Comparison Tool shows it as merged and does not offer a second merge. To correct a merged value afterwards, edit the merged record directly; the change is captured in its audit trail.

#### 5.4 Exporting Merged Data

Only Reviewers can export. Data Entry Person #1 and #2 cannot open Data Exports or reports and cannot export through the API.

A Reviewer's exports and reports include **all** records: the `--1` copies, the `--2` copies and the merged records. To get an analysis dataset of reconciled data only, filter to the merged records — for example, build a report with a filter that excludes record names ending in `--1` or `--2`, and export that report. Records not yet merged then drop out of the dataset, which is usually what you want.

---

## 6. Common Questions

**Q: Do both data entry users have to finish their copy before the reviewer can merge?**

**A:** No. REDCap does not check the instrument status of either copy before the reviewer can merge; it only requires that both copies exist. However, if one copy is incomplete when the merge is performed, fields that were not entered in that copy will appear blank in the comparison and the reviewer will need to resolve the discrepancy. Best practice is to ensure both copies are fully entered before merging.

**Q: Can one person do both first and second entry?**

**A:** Not as Person #1 and Person #2 — each slot holds one user, so one user cannot hold both. A Reviewer can open and edit both copies, though, so in practice one person could key both. This defeats the purpose of DDE. The error-detection value of DDE depends on the two entries being genuinely independent. If the same person does both, or if one person knows what the other entered, the second pass is not a meaningful check. Ensure your team structure maintains actual independence between the two data entry passes.

**Q: What happens to the --1 and --2 copies after a merge?**

**A:** They remain in the system. The copies are not deleted after merging, and Reviewers can still open them. They also stay in Reviewers' exports and reports, so filter to merged records when you build your analysis dataset (see §5.4).

**Q: Can the reviewer change a value to something neither copy entered?**

**A:** Yes, for most field types. During the merge, the reviewer can type a new value into any discrepant field instead of selecting one of the two copies' entries. File upload fields are the exception (see §7). This is appropriate when both entries appear to be wrong and the reviewer has determined the correct value from another source (e.g., original source documents).

**Q: Can I use DDE with a longitudinal project?**

**A:** Yes. DDE is compatible with longitudinal projects. The `--1` and `--2` copies exist across all events and arms in the same way they do in a classic project, and the Data Comparison Tool compares and merges one event at a time.

**Q: Does DDE interact with the Data Resolution Workflow?**

**A:** The Data Resolution Workflow (DRW) can be enabled alongside DDE. Each data entry person can open queries on their own copy, and Reviewers can open queries on either copy or the merged record. However, the interaction between DDE and DRW adds complexity — plan both features carefully before enabling them together.

---

## 7. Limitations

**Repeating instruments and events have partial support only.** The Data Comparison Tool does not fully support the Repeating Instruments and Events feature. If repeating instruments or repeating events are enabled in the project, comparison and merging is limited to **Instance #1** only. All other repeating instances (Instance #2, #3, etc.) are ignored by the tool and will not be compared or merged. Non-repeating data is not affected and can be compared and merged normally. If your project relies heavily on repeated data collection, evaluate this limitation carefully before using DDE.

**Surveys are not compatible with DDE.** Instruments enabled as surveys are not collected in the DDE workflow. A survey response is saved once, under the record ID without a suffix, and does not generate two independent copies. REDCap warns that if the first instrument is a survey, DDE will not function. Projects that rely primarily on survey-based data collection should not use DDE.

**Records created before DDE was enabled cannot be merged.** Pre-existing records are in a single-copy state. The Data Comparison Tool is only available for records that were created after DDE was enabled.

**Calculated fields compute independently on each copy.** Calculated field values are computed on each copy based on that copy's data. After merging, calculated fields are recomputed on the merged record. If you resolve a discrepancy in a field that feeds a calculated field, the calculation will update to reflect the merged value.

**Action tags operate per copy.** Action tags such as `@HIDDEN`, `@READONLY`, and autofill tags apply to each copy independently during data entry.

**File upload fields.** Both copies require a file to be uploaded independently. During the merge, the reviewer selects which copy's file to keep; there is no option to enter a new value for a file field.

---

## 8. Common Mistakes & Gotchas

**Not assigning DDE roles before data collection begins.** When DDE is first enabled, every user is a Reviewer and sees all records. Before data collection starts, set the one user who will be Data Entry Person #1 and the one user who will be Data Entry Person #2. Everyone else stays a Reviewer, so make sure only people who should see both copies and the merged records remain on the project.

**Saving a merge without reviewing the selections.** Copy 1 is pre-selected for every differing field, so saving straight away silently accepts Copy 1's value for every discrepancy. Check each listed field before saving the merge.

**Using DDE with instruments that are also surveys.** Survey-completed instruments do not participate in the DDE workflow. If a project has a mix of staff-entered and survey-completed instruments, only the staff-entered instruments go through the two-copy entry and merge process. Design your project to account for this hybrid behavior before enabling DDE.

**Performing the merge before both copies are complete.** If one copy is partially entered at the time of merge, blank fields in that copy will appear as discrepancies against the other copy's values. The reviewer will need to check the correct value for every such field — a tedious and error-prone process — and the record cannot be merged again once the missing data is entered. Establish a team workflow that confirms both copies are complete before any merge is initiated.

**Analysing an export that still contains the --1 and --2 copies.** A Reviewer's export contains all three versions of each merged record: both entry copies plus the merged record. Analysing it as-is counts each participant up to three times. Filter to merged records first — for example, a report filtered to exclude record names ending in `--1` or `--2` (see §5.4).

**Misunderstanding what "independent" means.** DDE only provides error-detection value if the two data entry passes are genuinely independent. If data entry users communicate about their entries, or if one user sees a source document that was annotated by the other, the second pass will tend to agree with the first regardless of accuracy. Train your team that the integrity of DDE depends on strict independence.

---

## 9. Related Articles

- [RC-DE-02 — Basic Data Entry](RC-DE-02_Basic-Data-Entry.md) (foundational data entry skills required before using DDE)
- [RC-DE-04 — Editing Data & Audit Trail](RC-DE-04_Editing-Data-and-Audit-Trail.md) (audit trail behavior in DDE; the --1 and --2 copies each have their own audit trail)
- [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) (DDE role assignment; how DDE rights interact with standard user rights)
- [RC-EXPRT-01 — Data Export: Overview & Workflow](RC-EXPRT-01_Data-Export-Overview-and-Workflow.md) (exports include the --1, --2 and merged records; filter to merged records for analysis)
- [RC-DE-12 — Data Resolution Workflow](RC-DE-12_Data-Resolution-Workflow.md) (can be used alongside DDE for additional data quality tracking)
