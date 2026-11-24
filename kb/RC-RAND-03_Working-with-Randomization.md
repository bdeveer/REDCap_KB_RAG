

**REDCap Randomization – Working with & Managing Randomization**

| **Article ID** | [RC-RAND-03 — Working with & Managing Randomization](RC-RAND-03_Working-with-Randomization.md) |
|---|---|
| **Domain** | Randomization |
| **Applies To** | Study Coordinators and data entry staff (Sections 4–6); REDCap Administrators (Section 7); requires project in Production with a configured randomization model |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — randomization behaviour checked against source code; pages not re-captured |
| **Prerequisite** | [RC-RAND-01 — Randomization Concepts & Terminology](RC-RAND-01_Randomization-Concepts.md); [RC-RAND-02 — Randomization Setup Guide](RC-RAND-02_Randomization-Setup.md) |
| **Version** | 1.5 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-RAND-01 — Randomization Concepts & Terminology](RC-RAND-01_Randomization-Concepts.md); [RC-RAND-02 — Randomization Setup Guide](RC-RAND-02_Randomization-Setup.md); [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md); [RC-EXPRT-01 — Data Export: Overview & Workflow](RC-EXPRT-01_Data-Export-Overview-and-Workflow.md); [RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md); [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md); [RC-PLUS-02 — REDCap+: Project Migration Tool](RC-PLUS-02_Project-Migration-Tool.md); [RC-MOB-01 — REDCap Mobile App](RC-MOB-01_REDCap-Mobile-App.md) |
| **Synonyms** | how do i randomize a participant; randomize a record in production; monitor randomization progress and allocation; who can randomize records; manage randomization after going live; view randomization assignments; troubleshoot randomization in a live project; randomize a subject into a treatment arm; does deleting a randomized record free its allocation; copy a randomized project without losing assignments; randomize a record via the api; copy project randomization values copied without allocation; why did trigger randomization not fire on data import |

---

## 1. Overview

### What is this?

This document covers what happens after a randomization model is set up
and the project is in production. It is organized by audience: regular
users (coordinators, data entry staff) in Sections 4--6, and REDCap
administrators in Section 7. Administrators should read both sections.

### Why does it matter?

Running and monitoring randomization correctly is as important as
setting it up correctly. Errors at this stage — randomizing the wrong
record, misreading the dashboard, or an administrator making an
unnecessary intervention — can compromise study integrity and require
protocol deviations.

---

## 2. Learning Objectives

After reviewing this document, the user will be able to:

- Manually randomize a record using the Randomize button

- Explain when and how automatic trigger randomization fires

- Identify what an unauthorized user sees when they encounter the
    randomization variable

- Navigate the randomization summary table and interpret its columns

- Use the randomization dashboard to monitor allocation progress

- Use randomization smart variables to capture metadata about the
    randomization event

- (Administrators) Append allocations to a production table

- (Administrators) Use allocation-level edit actions and understand
    when they are appropriate

---

## 3. Randomizing a Record

### 3.1 Manual randomization — Randomize button

This is the default trigger option. The randomization variable field is
replaced in the UI by a Randomize button.

| **State** | **What the user sees** |
| --- | --- |
| **Record not yet randomized** | A Randomize button appears where the randomization variable field would be. |
| **User clicks Randomize button** | A confirmation popup appears showing the record, the randomization variable and the stratification/DAG inputs. It does **not** show the group that will be assigned. Click the Randomize button in the popup to confirm. |
| **Result message** | After you confirm, a message states the record was randomized and the value assigned. This is the first point at which the assignment is shown. Dismiss it with the **Close** button inside the message itself (not in the dialog's bottom button bar), which matters if you script UAT against the form. |
| **Record successfully randomized (open)** | The randomization variable shows the assigned group label (e.g., 'Intervention'). |
| **Record successfully randomized (blinded)** | The randomization variable shows an opaque code. The study team cannot determine the group from this value. |
| **Stratification or DAG values missing** | REDCap displays a prompt stating how many stratification/criteria fields still lack a value; it does not list which ones. Check the strata (and DAG) in the dialog, complete the blank ones and retry. |
| **Strata on instruments the user cannot edit** | A stratum on an instrument the user has **No Access** to is shown in the dialog with its current value but disabled, so its value (including PHI) is visible but cannot be set there. A user with **Read Only** rights to that instrument *can* set the stratum in the dialog. |

> **Note:** *In Development mode, REDCap shows a yellow banner warning
> not to randomize real participants. This warning does not appear in
> Production mode.*

> **Note:** *Randomization is unavailable in **Draft Preview**, on
> **locked** records or instruments, and while the project is in
> **Analysis/Cleanup** status. In Analysis/Cleanup the Randomize dialog
> refuses; on 17.x its message wrongly says no allocation table has been
> uploaded, but the real reason is the project status.*

### 3.2 Automatic trigger randomization

If the randomization model was configured with one of the two trigger
logic options, randomization can fire automatically in addition to (or
instead of) the manual button.

| **Trigger Option** | **When randomization fires automatically** |
| --- | --- |
| **Trigger logic — users with Randomize rights only** | All three conditions must be true simultaneously: (1) the trigger option is set to this mode, (2) the defined trigger logic evaluates to true, (3) a user with Randomize rights saves the defined instrument/event. |
| **Trigger logic — all users including survey respondents** | Both conditions must be true: (1) the defined trigger logic evaluates to true, (2) any user saves the form OR a survey respondent completes the survey form. Randomize rights are NOT required to trigger this mode. |

A record is randomized only once. Saving the form again while the
trigger logic is still true does not re-randomize it.

Triggers are evaluated only when an instrument is saved on a data entry
form or a survey page is submitted (on a multi-page survey, at every
page submit). They do **not** fire on Data Import Tool uploads, API
record imports or Mobile App sync, even if the imported data makes the
trigger logic true. If a stratum is blank when the trigger fires, the
record is not randomized and the log notes that randomization failed
because of missing stratification data.

### 3.2a Randomizing through the API

The API **Randomize Record** method randomizes one record without the
form. The API token's user needs the Randomize right (or must be an
administrator). It refuses a record that is already randomized, a
record with missing strata, and a record outside the caller's DAG. It
does not retry: a refused call simply fails. For a blinded model the
response gives `*` in place of the alternate number. Parameters and
examples: [RC-API-52 — Randomize Record API](RC-API-52_Randomize-Record.md).

> **Note:** *Even with automatic triggers configured, a user with
> Randomize rights can still manually click the Randomize button at any
> time. A user without Randomize rights will see the field greyed out
> and non-interactive regardless of trigger mode.*

### 3.3 What unauthorized users see

Users who do not have the Randomize right assigned to their account see
the randomization variable as a greyed-out, non-interactive field ---
for both open and blinded randomization types. They cannot click the
Randomize button or interact with the field in any way. This is by
design and is not a bug.

---

## 3a. Version Caveats Affecting Allocation Integrity

Five defects affected randomization itself. For a randomised trial these matter more than most, because the allocation table is the auditable record of assignment.

> **Critical — deleted records did not free their allocation (below 15.0.26 Standard; present since 14.7.0).** In a longitudinal project with multiple arms, deleting a record **after it had been randomized** left its allocation in place in the allocation table. The slot was never returned to the pool.
>
> The consequence accumulates silently: a long-running trial that has deleted any randomized records on an affected version may have **fewer usable allocations remaining than the table appears to show**, and the discrepancy grows with each deletion. This is worth checking directly against the allocation table if your project began before 15.0.26 and records have ever been deleted post-randomization.

> **Version caveat (below 15.0.23 Standard; present since 14.7.0):** Where the instrument containing the randomization field is also enabled as a survey, randomizing a record **on the data entry form while a participant was completing that same instrument as a survey** could corrupt the result.

> **Version caveat (below 15.5.23 Standard):** Triggering randomization by submitting a form **at the same moment as locking that form** produced a **partial randomization** — the record was logged as randomized but the assignment was not fully applied. A record in this state looks randomized in the log while not being properly allocated.

> **Version caveat (below 16.0.23 Standard):** In the randomization dialog on a data entry form, clicking the **choice label** of a strata field — rather than the radio button itself — did not register the selection. A user could believe they had set a stratum and randomize against a different value than intended. Fixed in 16.0.23.

> **Version caveat (below 17.5.7 Standard; still present in 16.0.61 LTS):** Two randomize requests arriving at the same moment (e.g., a double click, a trigger and a manual click together, or two records in the **same stratum** randomized near-simultaneously) could claim the **same allocation slot**: the second **overwrote the first** in the allocation table, and randomizing a record that already had an allocation could cause a database error. A record could end up holding a different allocation from the one first shown. Fixed in 17.5.7 Standard. The fix is present in 17.3.31 LTS (the exact LTS fix version was not determined) and **not** in 16.0.61 LTS. Upgrade; on LTS 16, coordinate so randomizations are not done simultaneously and check the allocation table for slots claimed twice, reconciling as below.

If your project randomized records on any of these versions, the allocation table and the randomization log are the two places to reconcile against each other.

Three older defects can also explain a mismatch you find while reconciling:

> **Version caveat (below 15.6.0 Standard):** The administrator **Auto-fill** option on a data entry form also filled the randomization field, giving the record a value no allocation explains.

> **Version caveat (below 15.5.5 Standard):** If a stratum value broke a custom Data Quality rule with real-time execution, randomization could fail part-way and leave the record inconsistent.

> **Version caveat (below 15.7.0 Standard):** With automatic triggers, **Erase all data** in development (or deleting all records on the move to production) left the "Randomize record" log events behind, so the log shows randomizations with no matching records.
>
> On current versions (checked on 16.0.61 LTS, 17.3.31 LTS and 17.6.5), Erase all data and deleting records on the move to production remove the "Randomize record" and "Randomize record (via trigger)" log events but **not** "Randomize record (API)" events. If records were randomized through the API in development, expect those log entries to remain with no matching records.

---

## 4. Randomization Summary Table

Navigate to Applications → Randomization to see the summary table for
all randomization models in the project. Each row is one model.

| **Column** | **What it shows** |
| --- | --- |
| **\# (Order)** | The sequence in which randomization models were created in this project. |
| **Target** | The variable name of the randomization variable for this model. If automatic triggers are configured, an expandable option shows the trigger logic. |
| **Allocation type** | Open randomization: green open envelope icon. Blinded randomization: red closed envelope icon. |
| **Stratification** | Red X if no stratification. Variable names of all stratification variables if stratification is configured. |
| **Total allocations (Dev / Prod)** | How many allocation slots have been defined for development and production. The Development sub-column shows only while the project is in Development; in Production only the production count appears. Counts include slots marked unavailable, so they can exceed the slots actually usable. |
| **Setup (icon)** | Opens the randomization model setup page for review or editing (Development mode only for structural changes). |
| **Dashboard (icon)** | Opens the randomization dashboard for that model. Requires Dashboard user right. |
| **Randomization ID** | A system-generated global ID for the model. Primarily used by REDCap administrators for backend database lookups. |

---

## 5. Randomization Dashboard

The dashboard provides a real-time view of allocation usage for a
specific randomization model. Access it via the Dashboard icon in the
summary table. Requires the Dashboard user right.

### 5.1 What all users see

| **Column** | **What it shows** |
| --- | --- |
| **Grey dot / Green checkmark** | Grey dot = allocations still available. Green checkmark = all allocations for this row have been assigned. |
| **Used** | Number of allocations assigned to records so far for this row. |
| **Not Used** | Number of allocations still available for this row. |
| **Allocated records** | Record IDs of the records that used allocations in this row. IDs are clickable and navigate directly to that record. |
| **Dynamic columns** | Additional columns appear based on configuration: DAG column, stratification variable columns and, for open models only, the randomization variable (group) column. Headers show field labels and variable names — these differ per project. |

> **Note:** *What a row represents depends on the allocation type.*
>
> - ***Open** (dropdown/radio target):* *each row is a unique
>   combination of group, DAG and stratification values. A model with 2
>   groups and 2 stratification levels has 4 rows (2 groups × 2 strata).*
> - ***Blinded** (text target):* *the group column is left out. Each row
>   is a unique combination of DAG and stratification values, with its
>   used/unused counts and record list per stratum. The same 2-group,
>   2-stratum model has 2 rows.*
>
> *Because the next record takes the next free slot for its stratum and
> DAG **regardless of group**, a group row in an open model reaching
> zero does not block new records. A record cannot be randomized only
> when every slot for its stratum/DAG combination is used.*

### 5.2 What administrators additionally see

Administrators see one additional column: View. Clicking the dashboard
icon in the View column drills into that specific allocation group and
reveals the full allocation table with individual slot-level actions.
See Section 7 for administrator actions.

### 5.3 Monitoring best practices

- **Check 'Not Used' counts regularly:** Add up the 'Not Used' counts
    for a stratum/DAG combination (across all its group rows in an open
    model). If that total is approaching zero, contact your REDCap
    administrator to append more allocations before they run out.

- **Read the green checkmark correctly:** In a blinded model, a
    checkmark means that stratum/DAG combination is exhausted and new
    matching records cannot be randomized until more slots are added.
    In an open model it means only that one group's slots for that
    combination are used; matching records still randomize into the
    remaining slots of the other groups, which can unbalance the
    allocation. Treat it as a prompt to check the combination's total.

- **Record IDs are clickable:** Use the dashboard to navigate directly
    to randomized records for quick auditing.

- **Export the table:** An **Export** button above the dashboard table
    downloads the current counts and record lists as CSV. The export is
    logged.

> **Version caveat (16.0.61 LTS):** The dashboard **Export** button is
> absent; it is present in 17.3.31 LTS and 17.6.5. On LTS 16, copy the
> counts from the page or use a report on the randomization variable.

- **Blinding and the Dashboard right:** For a blinded model the
    dashboard does not show groups, so it cannot unblind; it shows which
    records were randomized in each stratum. For an open model it shows
    groups, which are already visible on the form. Administrators'
    **View** drill-down (5.2) still shows the slot-level values, including
    for blinded models.

---

## 6. Randomization Smart Variables

REDCap provides three smart variables that capture metadata about the
randomization event. These can be piped into fields, alerts, or reports
to create an audit trail or trigger downstream logic.

| **Smart Variable** | **What it returns**                                          **Notes** |
| --- | --- |
| **\[rand-time\]** | Date and time the record was randomized                      Uses server time (not local device time). If server is in Eastern time and user is in Pacific time, Eastern time is recorded. |
| **\[rand-utc-time\]** | Date and time in Coordinated Universal Time (UTC)            Use this for cross-timezone consistency or international studies. |
| **\[rand-number\]** | The randomization number assigned to the record — never the group   For blinded randomization: the randomization number, equivalent to piping the randomization field. For open randomization: the **alternate** number from the allocation table (optional column); blank if none was uploaded. To show an open model's group, pipe the randomization variable itself. See [RC-PIPE-13 — Smart Variables: Randomization](RC-PIPE-13_Smart-Variables-Randomization.md). |

> **Note:** *For projects with multiple randomization models, add `:n`
> for model n: `[rand-number:2]`, `[rand-time:2]`, `[rand-utc-time:2]`,
> and `[rand-time:2:value]` for the raw value. With no number, model 1
> is used. See [RC-PIPE-13 — Smart Variables: Randomization](RC-PIPE-13_Smart-Variables-Randomization.md).*

---

## 7. Administrator Options

This section is for REDCap administrators only. Regular users cannot
perform these actions. Intervention at the allocation level should be
rare — if frequent administrator intervention is needed for a project,
the randomization setup should be re-evaluated.

> **⚠ Warning:** *All administrator allocation actions require
> specifying a reason, which is logged. They also require typing
> 'confirm' to execute. This is intentional — these actions can
> affect study data integrity. The reason and CONFIRM requirement is
> enforced in the browser dialog, not re-checked by the server.*

### 7.1 Appending allocations to a production table

The most common administrator action. Required when a project runs out
of allocation slots in production.

- **Location:** Applications → Randomization → Setup icon for the
    model → Step 3 (Production allocation table) → 'Upload more
    allocations (Administrators only)' link

- **How it works:** Upload a new allocation table file. It appends to
    the existing table rather than replacing it. For example: 100
    existing slots + uploading 100 more = 200 total slots. Can be done
    as many times as needed, one file at a time.

- **Existing rows are locked:** Once the project is in production, the
    rows already in the table cannot be changed by upload. Appending
    only adds rows; the per-slot actions in 7.2 are the only way to
    change an individual slot.

- **Audit trail:** On newer Standard versions the "Randomize record"
    log entry also records the ID of the allocation-table row assigned,
    which helps when reconciling the log against the allocation table.

> **Version caveat (17.5.7+ Standard; checked on 17.6.5):** The
> allocation-row ID appears in the "Randomize record" log entry only on
> these versions. It is not recorded on 17.3.31 LTS or 16.0.61 LTS, and
> never on "Randomize record (API)" entries. On those, match log entries
> to allocation rows by record name instead (the administrator View in
> 5.2 shows which record used each slot).

- **File format:** Same format as a regular allocation table. Download
    a fresh template from the setup page if needed.

### 7.2 Allocation-level actions (via the View column in the dashboard)

After clicking the dashboard icon in the View column, administrators see
the full allocation table with an Edit column. Each unassigned slot has
up to four action icons; assigned slots have one.

| **Action** | **What it does**                                                                                                                                                                                                                                         **Available for** |
| --- | --- |
| **Remove randomization** | Removes the randomization assignment from a record, freeing that allocation slot for reassignment to another record. The record returns to an un-randomized state. The record's randomization variable value is deleted **without a normal data-change entry** in the log; only the allocation change and its reason are logged. Note the old value before removing it.   *Assigned slots only* |
| **Edit target field** | Remaps the allocation to a different cohort group. Requires: reason (logged), new value, and typing 'confirm'.                                                                                                                                         *Unassigned slots only* |
| **Edit target alternate** | Changes the slot's alternate value. For open models this is what the \[rand-number\] smart variable returns; it does not affect which group is assigned. Requires: reason (logged), new value, and typing 'confirm'.   *Unassigned slots only* |
| **Manual randomization** | Manually assigns a specific record to this allocation slot. The record must not already be randomized, must be in the arm that holds the randomization event, and its DAG and strata values must match the slot. Requires: reason (logged), valid record ID, and typing 'confirm'.                                                                               *Unassigned slots only* |
| **Make sequence unavailable** | Removes the allocation slot entirely from the pool — it will not be used for any future randomizations. Displayed with a stop symbol. Requires: reason (logged) and typing 'confirm'.                                                                *Unassigned slots only* |
| **Restore availability** | Reverses a 'Make sequence unavailable' action. Only available on slots previously made unavailable. Requires: reason (logged) and typing 'confirm'.                                                                                                  *Unavailable slots only* |

### 7.2a Moving a project with randomized records to production

If records have already been randomized when you click **Move project to Production**, REDCap shows an additional warning in the dialog about the consequences. Records randomized in development were allocated from the **development** allocation table, which is not the table your production study runs on. Decide deliberately whether to keep those records. If you keep them, REDCap keeps the records and their other data but **clears the randomization variable on its event for every model** and frees any production slots marked used, so the records are un-randomized and will draw from the production table when randomized again. Normally, delete test data on the move and randomize real participants only in production.

> **Version caveat (17.4.4+ Standard; confirmed on 17.6.5, absent on 17.3.31 LTS):** The extra warning about development-randomized records appears only on these versions. On LTS, check the Randomization dashboard before moving to production; if any record was randomized in development, decide about it before clicking the button.

From 17.5.0 Standard / 17.3.13 LTS, administrators can no longer upload a **development** allocation table (Randomization Setup, Step 3) once the project is in production; REDCap shows a message instead of the upload form (confirmed on 17.3.31 LTS and 17.6.5).

> **Version caveat (16.0.61 LTS):** The development-table upload form is still shown to administrators in production, but the upload is refused. Nothing changes in the development table.

### 7.2b Deleting a randomized record

Deleting a randomized record, whatever its position in the sequence, returns its allocation to the pool for a future record. This is normal behaviour (the 15.0.26 defect in Section 3a was the exception). The consequence in production: deleting test or duplicate records that were randomized gives their slots back, and the next matching record will take one of them.

In a longitudinal project with **multiple arms**, the slot is freed only when the record is deleted from an arm that contains the randomization event. Deleting the record from another arm leaves its allocation in use.

### 7.2c Viewing allocations in Analysis/Cleanup status

Allocation tables cannot be viewed while the project is in Analysis/Cleanup status, and records cannot be randomized (Section 3.1). The block itself is expected.

> **Version caveat (16.0.61 LTS):** The dashboard message in Analysis/Cleanup gives the wrong reason for the block. 17.3.31 LTS and 17.6.5 show the correct one. Either way, return the project to Production if allocations must be viewed or records randomized.

### 7.3 Redoing a randomization model in production

This scenario should be avoided at all costs. If a randomization model
in a production project needs to be rebuilt from scratch, the options
are limited and all have significant consequences.

> **⚠ Warning:** *Moving a production project back to Development status
> to erase a randomization model is disabled — even for administrators
> — through the standard 'Other Functionality' interface. The only
> paths forward involve backend database manipulation or cloning the
> project and starting over. Neither is straightforward. This reinforces
> why thorough testing before production is essential.*

If you clone with **Copy Project** and copy the records, what happens to randomization depends on the record-logging option:

- **Record logging not added (the default):** all data is copied, **including the randomization variable values**. Allocation tables are never copied (only the model settings, if you choose to copy them). Copied records therefore keep their group or number with **no allocation behind it**, and they cannot be re-randomized: the form reports that the record already has a value. Treat a copy made this way as an archive of the assignments, not as a project that can keep randomizing those records. If the copy is to randomize afresh, copy without records (or with record logging added) and upload new allocation tables.
- **Record logging added, with randomization settings copied:** the randomization variable values are left out, so every copied record starts un-randomized in the new project.

To move a project to another REDCap instance with its randomization assignments and allocation tables intact, use the Project Migration Tool instead ([RC-PLUS-02 — REDCap+: Project Migration Tool](RC-PLUS-02_Project-Migration-Tool.md), REDCap+ only).

> **Version caveat (below 15.8.4 Standard):** Copy Project could fail outright (redirecting to Home) for a project using randomization together with PDF Snapshots or e-Consent.

---

## 8. Questions & Answers

**Q: If I delete a randomized record, is its allocation lost?**

No. Its allocation is freed and will be used by a future record. Be careful deleting randomized records in production for that reason. In a multi-arm project, the slot is freed only when the record is deleted from the arm that contains the randomization event (Section 7.2b).

**Q: I imported data that makes the trigger logic true. Why wasn't the record randomized?**

Trigger randomization fires only when an instrument is saved on a data entry form or a survey page is submitted. Data Import Tool uploads, API record imports and Mobile App sync never fire it. Open and save the trigger instrument, click **Randomize**, or use the API **Randomize Record** method (Section 3.2a).

**Q: Can I randomize records through the API?**

Yes, with the **Randomize Record** method, if the token's user has the Randomize right or is an administrator. It refuses records that are already randomized, have missing strata or are outside the user's DAG, and does not retry. See Section 3.2a.

**Q: Why is there no Randomize button in Draft Preview or on a locked form?**

Randomization is disabled in Draft Preview, on locked records and instruments, and in Analysis/Cleanup status. Leave Draft Preview, or have the record or instrument unlocked, then randomize.

**Q: Can an External Module change how records are allocated?**

Yes. An External Module enabled on the project can override which allocation a record receives. If assignments do not follow the allocation table's sequence, ask your REDCap administrator which modules are enabled on the project.

**Q: Can I randomize from the Mobile App?**

No. The app works offline and cannot reach the allocation table, so it does not show the Randomize button. See [RC-MOB-01 — REDCap Mobile App](RC-MOB-01_REDCap-Mobile-App.md).

**Q: Where do I cite REDCap's randomization module in a manuscript?**

When randomization is set up, the data export dialog (15.5.0+) names the REDCap randomization publication to cite alongside the standard REDCap citation.

---

## 9. Common Mistakes & Gotchas

**Reading the randomization field from the wrong event**

- **What happens:** The instrument with the randomization field is also
    designated on later events (e.g., annual visits). A report or logic
    that reads the field from a later event finds it blank or `0`, and
    randomized participants show as "not randomized".

- **Prevention:** Always reference the randomization field on the
    randomization event, e.g. `[baseline_arm_1][rand_group]`, and filter
    reports on that event.

**Confusing the randomization dashboard with project dashboards**

- **What happens:** User navigates to Applications → Project
    Dashboards looking for randomization information and finds only
    their custom data visualizations.

- **Prevention:** The randomization dashboard is accessed via
    Applications → Randomization, then clicking the Dashboard icon for a
    specific model. It is a separate feature from Project Dashboards.

**Reading one group's green checkmark as "randomization is blocked"**

- **What happens:** In an open model, one group's row for a stratum
    reaches zero 'Not Used' and shows a green checkmark. Staff assume
    new records in that stratum cannot be randomized, or that the next
    record will wait for more slots. In fact REDCap gives the next
    record the next free slot for its stratum and DAG in any group.

- **Prevention:** Judge exhaustion by the total 'Not Used' across all
    group rows for the stratum/DAG combination (Section 5.3).

**Expecting imports to fire trigger randomization**

- **What happens:** Records are loaded with the Data Import Tool, the
    API or Mobile App sync, and the trigger logic is true, but nothing is
    randomized.

- **Prevention:** Triggers fire only on data entry form saves and
    survey submissions. Randomize imported records with the button or
    the API **Randomize Record** method.

**Not monitoring allocation counts proactively**

- **What happens:** Allocation slots run out mid-study. New enrollees
    cannot be randomized. Study operations are disrupted while an
    administrator locates and appends more allocations.

- **Prevention:** Establish a regular cadence for checking the 'Not
    Used' counts in the dashboard. Build an alert or report that flags
    when a group drops below a defined threshold (e.g., 20 remaining
    slots).

**Administrator intervening in allocation table without logging the
reason properly**

- **What happens:** An allocation edit is made without a clear reason,
    creating audit trail gaps that become problematic during regulatory
    review.

- **Prevention:** Always enter a specific, meaningful reason when
    performing allocation-level actions. REDCap logs these reasons ---
    treat them as protocol documentation.

**Frequent administrator interventions indicating a setup problem**

- **What happens:** Administrators are regularly asked to correct
    individual allocations — removing randomizations, remapping
    groups, manually assigning records. Each intervention is a study
    integrity risk.

- **Prevention:** If administrator interventions are happening
    frequently for the same project, schedule a review of the
    randomization setup. The root cause is almost always a design issue:
    insufficient allocation table size, incorrect stratification setup,
    or inadequate user training.

---

## 10. Related Articles

- **[RC-RAND-01 — Randomization Concepts & Terminology](RC-RAND-01_Randomization-Concepts.md):** Randomization Concepts & Terminology ---
    foundational concepts

- **[RC-RAND-02 — Randomization Setup Guide](RC-RAND-02_Randomization-Setup.md):** Randomization Setup Guide — pre-flight checklist
    and setup procedure

- **[RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md):** User Rights: Overview & Three-Tier Access — managing Randomize, Setup,
    and Dashboard rights

- **[RC-EXPRT-01 — Data Export: Overview & Workflow](RC-EXPRT-01_Data-Export-Overview-and-Workflow.md):** Data Exports, Reports, and Stats — building
    reports that include randomization variable data

- **[RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md):** Alerts & Notifications — setting up alerts based
    on randomization events using smart variables

- **[RC-PIPE-13 — Smart Variables: Randomization](RC-PIPE-13_Smart-Variables-Randomization.md):** Smart Variables: Randomization — reference for the
    \[rand-time\], \[rand-utc-time\], and \[rand-number\] smart variables

---

## 11. Version & Change Notes

| **REDCap Version** | **Notes** |
| --- | --- |
| **15.4.4+** | Randomization 2.0: automatic trigger options available. Smart variable behavior and dashboard columns consistent with this document. Verified compatible through REDCap 17. |
| **Pre-15.x** | Automatic triggers not available. Section 3.2 (automatic trigger behavior) does not apply. Manual-only randomization. Smart variables \[rand-time\], \[rand-utc-time\], \[rand-number\] — verify availability in your version. |

REDCap LLM Knowledge Base \| [RC-RAND-03 — Working with & Managing Randomization](RC-RAND-03_Working-with-Randomization.md) \| Working with & Managing
Randomization

---

## 12. Related Articles

- [RC-RAND-01 — Randomization Concepts & Terminology](RC-RAND-01_Randomization-Concepts.md)
- [RC-RAND-02 — Randomization Setup Guide](RC-RAND-02_Randomization-Setup.md)
- [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md)
- [RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md)
- [RC-EXPRT-01 — Data Export: Overview & Workflow](RC-EXPRT-01_Data-Export-Overview-and-Workflow.md)
- [RC-PIPE-13 — Smart Variables: Randomization](RC-PIPE-13_Smart-Variables-Randomization.md)
- [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md)
- [RC-PLUS-02 — REDCap+: Project Migration Tool](RC-PLUS-02_Project-Migration-Tool.md)
- [RC-MOB-01 — REDCap Mobile App](RC-MOB-01_REDCap-Mobile-App.md)
