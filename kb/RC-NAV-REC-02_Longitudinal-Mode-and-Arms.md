

**Longitudinal Mode and Arms**

| **Article ID** | [RC-NAV-REC-02 — Longitudinal Mode & Arms](RC-NAV-REC-02_Longitudinal-Mode-and-Arms.md) |
|---|---|
| **Domain** | Record Navigation |
| **Applies To** | Longitudinal projects |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — longitudinal and repeating data entry behaviour checked against source code; pages not re-captured |
| **Prerequisite** | [RC-NAV-REC-01 — Record Navigation Overview](RC-NAV-REC-01_Record-Navigation-Overview.md) |
| **Version** | 1.1 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-NAV-REC-01 — Record Navigation Overview](RC-NAV-REC-01_Record-Navigation-Overview.md), [RC-NAV-REC-03 — Repeated Instruments & Repeated Events](RC-NAV-REC-03_Repeated-Instruments-and-Events.md)[RC-NAV-REC-04 — Record Status Dashboard & Other Record Links](RC-NAV-REC-04_Record-Status-Dashboard-and-Links.md), [RC-NAV-UI-01 — Project Navigation UI](RC-NAV-UI-01_Project-Navigation-UI.md), [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md), [RC-DE-03 — Longitudinal Projects & DAGs](RC-DE-03_Longitudinal-Projects-and-DAGs.md)[RC-DE-10 — Longitudinal & Repeated Data Entry](RC-DE-10_Longitudinal-and-Repeated-Data-Entry.md)|
| **Synonyms** | how do arms work in a longitudinal project; navigating events and timepoints in redcap; what is longitudinal mode; how to switch between arms for a record; how to move between baseline week 4 and month 6 events; difference between arms and events; collecting data across multiple timepoints; how to navigate the event grid |

---

## 1. Overview

This article explains REDCap's Longitudinal mode and the concept of
Arms — two features that allow data collection across multiple
timepoints and participant cohorts. It describes how these features
affect record navigation.

---

## 2. Key Concepts & Definitions

**Longitudinal Mode**

A project setting that enables data collection at multiple timepoints.
Instead of a single set of instruments, a longitudinal project defines
Events — named timepoints (e.g., Baseline, Week 4, Month 6) — and
assigns instruments to each event.

**Event**

A named timepoint within a longitudinal project. Each event can have any
subset of the project's instruments assigned to it. When viewing a
record, each event appears as a separate column on the Record Home Page.

**Arm**

A named collection of events within a longitudinal project. A project
can have multiple arms, each with a different set of events and
instrument assignments. Each record ID should exist in only one arm.
Arms are typically used to separate participant cohorts (e.g.,
intervention group vs. placebo group).

> **Note:** REDCap does not strictly stop the same record ID from having
> data in more than one arm — it can happen through a data import, or by
> typing an existing record ID while another arm is selected. This leads
> to confusing behaviour: the Record Home Page notes that the record
> "also exists on another arm", and **Rename Record** and **Delete
> Record** act only on the arm you are viewing. Keep each record in one
> arm.

---

## 3. How Longitudinal Mode Affects Navigation

### 3.1 Record Home Page in a Longitudinal Project

- Instead of a single row of instrument dots, you see a grid: rows are
    instruments, columns are events.

- Each dot represents a specific instrument within a specific event.

- Click any dot to open that instrument for that event.

- Only the events of the record's arm are shown, and instruments that
    are not designated to any event in that arm are left out of the
    grid.

### 3.2 Record Status Dashboard in a Longitudinal Project

- The dashboard displays the same grid layout — rows are records,
    columns are events and instruments.

- If the project has multiple arms, the dashboard adds a tab for each
    arm at the top of the page.

- Click a tab to view records belonging to that arm.

- A custom dashboard that is set to show a single arm does not show the
    arm tabs.

### 3.3 Add/Edit Records in a Project with Arms

- An additional dropdown appears at the top of the Add/Edit Records
    page asking you to select an arm. An arm is always preselected, so
    check it before you look up or add a record.

- The record drop-down and the record ID autocomplete list only the
    records in the selected arm.

- The field search on the same page (searching for a value within a
    chosen field) covers all arms and opens the matching record in its
    own arm.

- With auto-numbering on, the next record ID is the highest ID across
    all arms plus 1, so auto-numbering never reuses an ID that already
    exists in another arm.

> **Version caveat (LTS 16):** the Add/Edit Records page always
> preselects Arm 1. From 17.x (LTS 17.3 and later, and Standard) it
> remembers the arm you last used, and offers an option to keep the arm
> selection in step with the Record Status Dashboard. On LTS 16, select
> the arm every time before adding a record.

---

## 4. Step-by-Step: Working with Events and Arms

### 4.1 Navigating to a Record in a Specific Event

- Go to Add/Edit Records or the Record Status Dashboard.

- If arms exist, select the appropriate arm first.

- Select or search for the record.

- On the Record Home Page, locate the column for the event you want.

- Click the dot for the instrument within that event.

### 4.2 Identifying Which Arm a Record Belongs To

- The Record Home Page header or the arm tab on the Record Status
    Dashboard indicates the active arm.

- Each record should exist in only one arm. If you cannot find a record
    in one arm, check another arm, or use the field search on Add/Edit
    Records, which searches all arms.

---

## 5. Common Questions

**Q: What is the difference between an event and an arm?**

**A:** An event is a single timepoint (e.g., 'Baseline visit'). An arm is
a collection of events that defines the overall study timeline for a
particular cohort. Multiple arms let you define different timelines for
different groups of participants.

**Q: Can a record move from one arm to another?**

**A:** There is no move feature, for administrators either. To move a
record, export its data first, then:

1. Enter the record's data in the new arm — either by a data import
    into that arm's events, or (when auto-numbering is off) by entering
    the same record ID on Add/Edit Records with the new arm selected.
2. Check that the data in the new arm is complete and correct.
3. Open the record in the old arm and use **Delete Record**, which
    deletes only that arm's data.

This needs the **Create Records** or **Data Import Tool** right, plus the
**Delete Records** right.

**Q: Do all instruments appear in every event?**

**A:** No. The project designer assigns specific instruments to specific
events. An instrument only appears in the events it has been designated
for.

**Q: I cannot find a record in Add/Edit Records. What should I check?**

**A:** First confirm you have selected the correct arm from the dropdown.
The record list only shows records in the selected arm. If you are not
sure of the arm, use the field search on the same page, which searches
all arms.

---

## 6. Common Mistakes & Gotchas

- Looking for a record in the wrong arm: the record drop-down is
    arm-specific. If the arm dropdown is set incorrectly, the record
    will not appear in it (the field search still finds it).

- Creating the same record ID in a second arm: this is not blocked
    when auto-numbering is off or during data import, but it causes
    confusing behaviour (see Section 2). Keep each record in one arm.

- Expecting all instruments in every event: instruments are assigned
    to events individually. An instrument that is not assigned to a
    given event will not appear in that event's column.

- Confusing events with arms: events are timepoints within a study
    timeline; arms are parallel timelines for different cohorts. These
    are related but distinct concepts.

---

## 7. Related Articles

- [RC-NAV-REC-01 — Record Navigation Overview](RC-NAV-REC-01_Record-Navigation-Overview.md) — foundational article
    covering navigation paths and instrument status dots

- [RC-NAV-REC-03 — Repeated Instruments & Repeated Events](RC-NAV-REC-03_Repeated-Instruments-and-Events.md) — how
    stacked dots and repeated columns work alongside longitudinal mode

- [RC-NAV-REC-04 — Record Status Dashboard & Other Record Links](RC-NAV-REC-04_Record-Status-Dashboard-and-Links.md) —
    the arm tabs and event grid on the dashboard

- [RC-NAV-UI-01 — Project Navigation UI](RC-NAV-UI-01_Project-Navigation-UI.md) — the two-panel layout
    and menu that contains the longitudinal navigation entry points

- [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md) — how to configure events,
    arms, and instrument-event mappings; the setup side of what this
    article covers from a navigation perspective

- [RC-DE-03 — Longitudinal Projects & DAGs](RC-DE-03_Longitudinal-Projects-and-DAGs.md)
    specific to longitudinal projects with events and arms

- [RC-DE-10 — Longitudinal & Repeated Data Entry](RC-DE-10_Longitudinal-and-Repeated-Data-Entry.md) — detailed data
    entry procedures for events and repeated instruments
