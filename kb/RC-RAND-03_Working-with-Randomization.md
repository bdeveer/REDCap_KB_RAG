RC-RAND-03

**REDCap Randomization – Working with & Managing Randomization**

| **Article ID** | RC-RAND-03 |
| --- | --- |
| **Domain** | Randomization |
| **Applies To** | Study Coordinators and data entry staff (Sections 4–6); REDCap Administrators (Section 7); requires project in Production with a configured randomization model |
| **Prerequisite** | RC-RAND-01 — Randomization Concepts & Terminology; RC-RAND-02 — Randomization Setup Guide |
| **Version** | 1.0 |
| **Last Updated** | 2025-01 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-RAND-01 — Randomization Concepts & Terminology; RC-RAND-02 — Randomization Setup Guide; RC-RIGHTS-01 — User Rights Overview; RC-EXPRT-01 — Data Exports, Reports, and Stats; RC-ALERT-01 — Alerts & Notifications |

---

# 2. Overview

## What is this?

This document covers what happens after a randomization model is set up
and the project is in production. It is organized by audience: regular
users (coordinators, data entry staff) in Sections 4--6, and REDCap
administrators in Section 7. Administrators should read both sections.

## Why does it matter?

Running and monitoring randomization correctly is as important as
setting it up correctly. Errors at this stage — randomizing the wrong
record, misreading the dashboard, or an administrator making an
unnecessary intervention — can compromise study integrity and require
protocol deviations.

# 3. Learning Objectives

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

# 4. Randomizing a Record

## 4.1 Manual randomization — Randomize button

This is the default trigger option. The randomization variable field is
replaced in the UI by a Randomize button.

| **State** | **What the user sees** |
| --- | --- |
| **Record not yet randomized** | A Randomize button appears where the randomization variable field would be. |
| **User clicks Randomize button** | A confirmation popup appears showing the record and group assignment that will be made. Click the Randomize button in the popup to confirm. |
| **Record successfully randomized (open)** | The randomization variable shows the assigned group label (e.g., \'Intervention\'). |
| **Record successfully randomized (blinded)** | The randomization variable shows an opaque code. The study team cannot determine the group from this value. |
| **Stratification or DAG values missing** | REDCap displays a prompt listing the missing values before allowing randomization. Complete those fields and retry. |

> **Note:** *In Development mode, REDCap shows a yellow banner warning
> not to randomize real participants. This warning does not appear in
> Production mode.*

## 4.2 Automatic trigger randomization

If the randomization model was configured with one of the two trigger
logic options, randomization can fire automatically in addition to (or
instead of) the manual button.

| **Trigger Option** | **When randomization fires automatically** |
| --- | --- |
| **Trigger logic — users with Randomize rights only** | All three conditions must be true simultaneously: (1) the trigger option is set to this mode, (2) the defined trigger logic evaluates to true, (3) a user with Randomize rights saves the defined instrument/event. |
| **Trigger logic — all users including survey respondents** | Both conditions must be true: (1) the defined trigger logic evaluates to true, (2) any user saves the form OR a survey respondent completes the survey form. Randomize rights are NOT required to trigger this mode. |

> **Note:** *Even with automatic triggers configured, a user with
> Randomize rights can still manually click the Randomize button at any
> time. A user without Randomize rights will see the field greyed out
> and non-interactive regardless of trigger mode.*

## 4.3 What unauthorized users see

Users who do not have the Randomize right assigned to their account see
the randomization variable as a greyed-out, non-interactive field ---
for both open and blinded randomization types. They cannot click the
Randomize button or interact with the field in any way. This is by
design and is not a bug.

# 5. Randomization Summary Table

Navigate to Applications → Randomization to see the summary table for
all randomization models in the project. Each row is one model.

| **Column** | **What it shows** |
| --- | --- |
| **\# (Order)** | The sequence in which randomization models were created in this project. |
| **Target** | The variable name of the randomization variable for this model. If automatic triggers are configured, an expandable option shows the trigger logic. |
| **Allocation type** | Open randomization: green open envelope icon. Blinded randomization: red closed envelope icon. |
| **Stratification** | Red X if no stratification. Variable names of all stratification variables if stratification is configured. |
| **Total allocations (Dev / Prod)** | Two sub-columns showing how many allocation slots have been defined for development mode and production mode respectively. |
| **Setup (icon)** | Opens the randomization model setup page for review or editing (Development mode only for structural changes). |
| **Dashboard (icon)** | Opens the randomization dashboard for that model. Requires Dashboard user right. |
| **Randomization ID** | A system-generated global ID for the model. Primarily used by REDCap administrators for backend database lookups. |

# 6. Randomization Dashboard

The dashboard provides a real-time view of allocation usage for a
specific randomization model. Access it via the Dashboard icon in the
summary table. Requires the Dashboard user right.

## 6.1 What all users see

| **Column** | **What it shows** |
| --- | --- |
| **Grey dot / Green checkmark** | Grey dot = allocations still available. Green checkmark = all allocations for this row have been assigned. A quick indicator that you are at maximum for a group. |
| **Used** | Number of allocations assigned to records so far for this row. |
| **Not Used** | Number of allocations still available for this row. |
| **Allocated records** | Record IDs of all records assigned to this group. IDs are clickable and navigate directly to that record. |
| **Dynamic columns** | Additional columns appear based on configuration: DAG column, stratification variable columns, randomization variable column. Headers show field labels and variable names — these differ per project. |

> **Note:** *Each row in the dashboard represents a unique combination
> of cohort, DAG, and stratification values (if applicable). A project
> with 2 cohorts and 2 stratification levels will have 4 rows per cohort
> combination, not 2.*

## 6.2 What administrators additionally see

Administrators see one additional column: View. Clicking the dashboard
icon in the View column drills into that specific allocation group and
reveals the full allocation table with individual slot-level actions.
See Section 7 for administrator actions.

## 6.3 Monitoring best practices

- **Check \'Not Used\' counts regularly:** If a group is approaching
    zero remaining slots, contact your REDCap administrator to append
    more allocations before they run out.

- **Use the green checkmark as an alert:** A checkmark means that
    group\'s allocations are exhausted. New records matching that
    combination will not be randomizable until more slots are added.

- **Record IDs are clickable:** Use the dashboard to navigate directly
    to randomized records for quick auditing.

# 6. Randomization Smart Variables

REDCap provides three smart variables that capture metadata about the
randomization event. These can be piped into fields, alerts, or reports
to create an audit trail or trigger downstream logic.

| **Smart Variable** | **What it returns**                                          **Notes** |
| --- | --- |
| **\[rand-time\]** | Date and time the record was randomized                      Uses server time (not local device time). If server is in Eastern time and user is in Pacific time, Eastern time is recorded. |
| **\[rand-utc-time\]** | Date and time in Coordinated Universal Time (UTC)            Use this for cross-timezone consistency or international studies. |
| **\[rand-number\]** | The randomization allocation number assigned to the record   For blinded randomization: equivalent to piping the randomization field. For open randomization: the randomization number from the allocation table (optional field in table setup). |

> **Note:** *For projects with multiple randomization models, each smart
> variable can be targeted to a specific model. Consult the REDCap smart
> variable documentation within REDCap for the exact syntax.*

# 7. Administrator Options

This section is for REDCap administrators only. Regular users cannot
perform these actions. Intervention at the allocation level should be
rare — if frequent administrator intervention is needed for a project,
the randomization setup should be re-evaluated.

> **⚠ Warning:** *All administrator allocation actions require
> specifying a reason, which is logged. They also require typing
> \'confirm\' to execute. This is intentional — these actions can
> affect study data integrity.*

## 7.1 Appending allocations to a production table

The most common administrator action. Required when a project runs out
of allocation slots in production.

- **Location:** Applications → Randomization → Setup icon for the
    model → Step 3 (Production allocation table) → \'Upload more
    allocations (Administrators only)\' link

- **How it works:** Upload a new allocation table file. It appends to
    the existing table rather than replacing it. For example: 100
    existing slots + uploading 100 more = 200 total slots. Can be done
    as many times as needed, one file at a time.

- **File format:** Same format as a regular allocation table. Download
    a fresh template from the setup page if needed.

## 7.2 Allocation-level actions (via the View column in the dashboard)

After clicking the dashboard icon in the View column, administrators see
the full allocation table with an Edit column. Each unassigned slot has
up to four action icons; assigned slots have one.

| **Action** | **What it does**                                                                                                                                                                                                                                         **Available for** |
| --- | --- |
| **Remove randomization** | Removes the randomization assignment from a record, freeing that allocation slot for reassignment to another record. The record returns to an un-randomized state.                                                                                       *Assigned slots only* |
| **Edit target field** | Remaps the allocation to a different cohort group. Requires: reason (logged), new value, and typing \'confirm\'.                                                                                                                                         *Unassigned slots only* |
| **Edit target alternate** | Remaps the randomization group (alternate number). Mostly relevant for blinded randomizations — affects the \[rand-number\] smart variable but not direct randomization functionality. Requires: reason (logged), new value, and typing \'confirm\'.   *Unassigned slots only* |
| **Manual randomization** | Manually assigns a specific record to this allocation slot. The record must not already be randomized. Requires: reason (logged), valid record ID, and typing \'confirm\'.                                                                               *Unassigned slots only* |
| **Make sequence unavailable** | Removes the allocation slot entirely from the pool — it will not be used for any future randomizations. Displayed with a stop symbol. Requires: reason (logged) and typing \'confirm\'.                                                                *Unassigned slots only* |
| **Restore availability** | Reverses a \'Make sequence unavailable\' action. Only available on slots previously made unavailable. Requires: reason (logged) and typing \'confirm\'.                                                                                                  *Unavailable slots only* |

## 7.3 Redoing a randomization model in production

This scenario should be avoided at all costs. If a randomization model
in a production project needs to be rebuilt from scratch, the options
are limited and all have significant consequences.

> **⚠ Warning:** *Moving a production project back to Development status
> to erase a randomization model is disabled — even for administrators
> — through the standard \'Other Functionality\' interface. The only
> paths forward involve backend database manipulation or cloning the
> project and starting over. Neither is straightforward. This reinforces
> why thorough testing before production is essential.*

# 8. Questions & Answers

# 9. Common Mistakes & Gotchas

**Confusing the randomization dashboard with project dashboards**

- **What happens:** User navigates to Applications → Project
    Dashboards looking for randomization information and finds only
    their custom data visualizations.

- **Prevention:** The randomization dashboard is accessed via
    Applications → Randomization, then clicking the Dashboard icon for a
    specific model. It is a separate feature from Project Dashboards.

**Not monitoring allocation counts proactively**

- **What happens:** Allocation slots run out mid-study. New enrollees
    cannot be randomized. Study operations are disrupted while an
    administrator locates and appends more allocations.

- **Prevention:** Establish a regular cadence for checking the \'Not
    Used\' counts in the dashboard. Build an alert or report that flags
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

# 10. Related Articles

- **RC-RAND-01:** Randomization Concepts & Terminology ---
    foundational concepts

- **RC-RAND-02:** Randomization Setup Guide — pre-flight checklist
    and setup procedure

- **RC-RIGHTS-01:** User Rights & DAGs — managing Randomize, Setup,
    and Dashboard rights

- **RC-EXPRT-01:** Data Exports, Reports, and Stats — building
    reports that include randomization variable data

- **RC-ALERT-01:** Alerts & Notifications — setting up alerts based
    on randomization events using smart variables

- **RC-PIPE-13:** Smart Variables: Randomization — reference for the
    \[rand-time\], \[rand-utc-time\], and \[rand-number\] smart variables

# 11. Version & Change Notes

| **REDCap Version** | **Notes** |
| --- | --- |
| **15.4.4+** | Randomization 2.0: automatic trigger options available. Smart variable behavior and dashboard columns consistent with this document. |
| **Pre-15.x** | Automatic triggers not available. Section 4.2 (automatic trigger behavior) does not apply. Manual-only randomization. Smart variables \[rand-time\], \[rand-utc-time\], \[rand-number\] — verify availability in your version. |

REDCap LLM Knowledge Base \| RC-RAND-03 \| Working with & Managing
Randomization
