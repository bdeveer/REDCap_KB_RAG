RC-DE-03

**Longitudinal Projects & Data Access Groups**

| **Article ID** | RC-DE-03 |
| --- | --- |
| **Domain** | Data Entry |
| **Applies To** | REDCap projects with Longitudinal mode or Data Access Groups enabled |
| **Prerequisite** | RC-DE-01 — Record Creation; RC-DE-02 — Basic Data Entry |
| **Version** | 1.0 |
| **Last Updated** | 2025 |
| **Author** | REDCap Support |
| **Related Topics** | RC-NAV-REC-02 — Longitudinal Mode & Arms; RC-NAV-REC-04 — Record Status Dashboard; RC-DE-01; RC-DE-02 |

# 1. Overview

This article explains how two common project features — Longitudinal
mode and Data Access Groups (DAGs) — affect the data entry experience.
Both features change what you see when navigating records and what you
are permitted to access. Understanding them prevents confusion when
working in projects that use either or both features.

# 2. Longitudinal Mode

## 2.1 What It Is

Longitudinal mode allows a single instrument to be reused across
multiple timepoints (events) within the same record. Instead of creating
a separate form for \'Baseline Vitals\' and \'Week 4 Vitals\', the same
Vital Signs instrument is assigned to both a Baseline event and a Week 4
event.

- **Example:** A study collects vital signs at Baseline, Week 4, and
    Month 6. In longitudinal mode, one Vital Signs instrument is
    assigned to all three events. Each event gets its own independent
    copy of the data.

- The number and names of events are defined by the project designer.
    Data entry users cannot add or remove events.

## 2.2 How Longitudinal Mode Changes the Interface

When longitudinal mode is active, three areas of the interface change:

  ---------------------------------------- -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Location**                             **What Changes**
  Record Home Page                         Displays a grid instead of a single row. Rows are instruments; columns are events. Each dot represents one instrument in one event. Click any dot to open that specific instrument-event combination.
  Record Status Dashboard                  Same grid layout as the Record Home Page, but across all records. If the project has multiple arms, tabs appear at the top — one per arm.
  Data Collection menu (within a record)   Shows the event context when navigating between instruments. The current event is indicated, and switching instruments keeps you within the same event unless you explicitly click into a different event\'s dot.
  ---------------------------------------- -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 2.3 Navigating a Longitudinal Record

- On the Record Home Page, each column represents an event. Instrument
    dots in that column correspond to that event.

- Click a dot in the Baseline column to open that instrument at
    Baseline. Click the same instrument\'s dot in the Week 4 column to
    open it at Week 4. These are independent data entries — one does
    not affect the other.

- Use the event-column layout to quickly assess which instruments have
    been completed at which timepoints without opening each one
    individually.

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Note:** Longitudinal mode does not change how data is entered within an individual instrument. The field types, required fields, branching logic, form status, and save options all work identically to a non-longitudinal project.
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 3. Data Access Groups (DAGs)

## 3.1 What They Are

Data Access Groups (DAGs) partition the records in a project into named
subsets. Each DAG typically corresponds to a study site, department, or
other organizational unit. When DAGs are enabled, users are assigned to
one DAG and can only see and access records within their own DAG.

- **Example:** A multi-site study has three sites: Boston, Chicago,
    and Denver. Each site is a separate DAG. A data entry user at the
    Boston site can only see and create records assigned to Boston.

## 3.2 How DAGs Affect Data Entry

  ---------------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Action**                   **Behavior When DAGs Are Enabled**
  Creating a new record        The new record is automatically assigned to your DAG. You do not need to (and cannot) select a DAG manually during record creation.
  Looking up a record          The record dropdown and Data Search on the Add/Edit Records page only show records in your DAG. Records from other DAGs are invisible to you.
  Record Status Dashboard      Only shows records from your DAG. Records from other DAGs do not appear, even on the default dashboard.
  Reporting a missing record   If you cannot find a record that you expect to exist, the most likely explanation is that the record belongs to a different DAG. Contact your project administrator.
  ---------------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 3.3 Key Rules for DAG Users

- You can only create records that are automatically assigned to your
    DAG.

- You cannot see, edit, or delete records that belong to a different
    DAG.

- DAG assignment for a record is set at creation and cannot be changed
    by a regular data entry user.

- If you are not assigned to any DAG, you can see all records in the
    project (subject to other access controls).

  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Troubleshooting:** DAG filtering is not the same as a custom dashboard filter. If a record appears to be missing, check first whether DAGs are enabled and whether the record might belong to a different site.
  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 4. Common Questions

**Q: In a longitudinal project, does filling in an instrument at
Baseline affect the same instrument at Week 4?**

A: No. Each instrument-event combination is an independent data entry.
Entering Baseline data does not prefill, affect, or overwrite the same
instrument at any other event.

**Q: How do I know which event I am currently in when entering data?**

A: The current event context is shown at the top of the instrument and
in the left-hand navigation menu. In the Record Home Page and Record
Status Dashboard, the column header shows the event name.

**Q: I cannot find a record I just created. Where did it go?**

A: If DAGs are enabled, the record was automatically assigned to your
DAG and should appear in your Add/Edit Records dropdown. If it still
does not appear, check whether you navigated away before the record was
fully created, or contact your project administrator.

**Q: Can I be assigned to more than one DAG?**

A: No. A user can be assigned to only one DAG at a time. If you need
access to records across multiple DAGs, you must be unassigned from any
DAG — which gives you access to all records in the project.

**Q: A record exists but I cannot access it. What should I check?**

A: First check whether DAGs are enabled in the project. If they are, the
record may belong to a DAG you are not assigned to. Second, check
whether your user rights restrict access to certain instruments. Contact
your project administrator if you need access that your current rights
do not provide.

**Q: Does longitudinal mode change how I save data?**

A: No. The four save options (Save and Exit Form, Save and Stay, Save
and Exit Record, Save and Go to Next Record) work identically in
longitudinal and non-longitudinal projects.

# 5. Common Mistakes & Gotchas

- Entering data in the wrong event column: in longitudinal projects,
    clicking the dot in the wrong column opens the instrument in the
    wrong event. Always verify the column (event) header before entering
    data.

- Assuming a missing record was deleted: in DAG-enabled projects, a
    record that appears missing is almost always in a different DAG, not
    deleted. Check with your administrator before concluding data is
    missing.

- Expecting to choose a DAG when creating a record: DAG assignment
    happens automatically at record creation. There is no DAG selection
    step for regular data entry users.

- Confusing events with arms: events are individual timepoints; arms
    are collections of events for different cohorts. A record belongs to
    one arm, which contains multiple events. See RC-NAV-REC-02 for a full
    explanation.

# 6. Related Articles

- RC-DE-01 — Record Creation & the Record Home Page (prerequisite)

- RC-DE-02 — Basic Data Entry (prerequisite)

- RC-DE-04 — Editing Data & Audit Trail

- RC-NAV-REC-02 — Longitudinal Mode & Arms (deeper navigation detail for
    longitudinal projects)

- RC-NAV-REC-04 — Record Status Dashboard & Other Record Links
