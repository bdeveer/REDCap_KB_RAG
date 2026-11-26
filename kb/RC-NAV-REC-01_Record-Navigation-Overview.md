

**Record Navigation Overview**

| **Article ID** | [RC-NAV-REC-01 — Record Navigation Overview](RC-NAV-REC-01_Record-Navigation-Overview.md) |
|---|---|
| **Domain** | Record Navigation |
| **Applies To** | All project types |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — record navigation and form status icons behaviour checked against source code; pages not re-captured |
| **Prerequisite** | None |
| **Version** | 1.1 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-NAV-REC-02 — Longitudinal Mode & Arms](RC-NAV-REC-02_Longitudinal-Mode-and-Arms.md), [RC-NAV-REC-03 — Repeated Instruments & Repeated Events](RC-NAV-REC-03_Repeated-Instruments-and-Events.md)[RC-NAV-REC-04 — Record Status Dashboard & Other Record Links](RC-NAV-REC-04_Record-Status-Dashboard-and-Links.md), [RC-NAV-UI-01 — Project Navigation UI](RC-NAV-UI-01_Project-Navigation-UI.md), [RC-DE-01 — Record Creation & the Record Home Page](RC-DE-01_Record-Creation-and-Record-Home-Page.md)[RC-DE-02 — Basic Data Entry](RC-DE-02_Basic-Data-Entry.md), [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md), [RC-LONG-02 — Repeated Instruments & Events Setup](RC-LONG-02_Repeated-Instruments-and-Events-Setup.md)[RC-IMP-01 — Data Import Overview](RC-IMP-01_Data-Import-Overview.md), [RC-EXPRT-06 — Custom Reports: Setup & Field Selection](RC-EXPRT-06_Custom-Reports-Setup-and-Field-Selection.md)|
| **Synonyms** | how do i find a record in redcap; how to navigate to a participant record; what do the colored status dots mean; ways to open a record in a project; how to locate data for a subject; where do i go to enter data for a record; understanding instrument status indicators; how to search for a record id |

---

## 1. Overview

This article explains how to navigate to records and locate data within
a REDCap project. It covers the primary navigation paths available to
any REDCap user and explains how to interpret instrument status
indicators (colored dots).

---

## 2. Key Concepts & Definitions

**Record**

The fundamental unit of data in REDCap. Each record corresponds to one
participant, patient, or subject. Every record has a Record ID — the
primary identifier used throughout the system.

**Instrument**

A data-entry form within a REDCap project. Instruments contain fields
(variables) where data is entered. Each instrument has a status dot that
reflects its completion state.

**Record Home Page**

A per-record landing page that displays all instruments associated with
that record. It is the central hub for viewing and navigating to any
instrument for a single record.

**Record Status Dashboard**

A project-level view displaying all records and their instrument
statuses in a grid. Useful for monitoring progress across an entire
study.

**Add/Edit Records Page**

A data-collection menu page that provides lookup tools for finding and
opening individual records.

---

## 3. Step-by-Step: Primary Navigation Paths

### 3.1 Navigating to a Project

- Log in to your REDCap instance.

- On the My Projects page, click the name of the project you want to
    open.

- You are now on the project home page, with the left-hand menu
    available.

### 3.2 Add/Edit Records (Quickest Path to a Single Record)

- In the left-hand menu, find the Data Collection section and click
    Add / Edit Records. If you do not have the right to create records,
    the link reads **View / Edit Records** instead.

- To find a record by ID: use the **Choose an existing [Record ID]**
    dropdown. It lists only the records in your Data Access Group (if
    you are in one) and, in longitudinal projects with several arms, in
    the current arm. Once the project has more than 25,000 records, the
    dropdown is replaced by a text box where you type the record ID.

- To search by value: use the Data Search feature.

- Search across all variables ("All fields") — useful when you only
    know a value but not which field contains it. This option is not
    available once the project has more than 20,000 records.

- Search within a specific variable — faster in large projects
    (e.g., search only the Date of Birth field).

- Data Search limits: multiple-choice (dropdown, radio), checkbox,
    yes/no, true/false, file upload and descriptive fields cannot be
    searched; at most 25 results are shown; results only include
    records in your Data Access Group and instruments you have rights
    to view.

- Selecting a result opens the record either on the data entry form
    where the value was found or on the Record Home Page, depending on
    your version (see the caveat below).

> **Version caveat (17.x vs 16.x LTS):** In 17.x, Data Search lets you
> choose whether a result opens on the **Data Entry Form** or the
> **Record Home Page**, and REDCap remembers your choice. 17.x also
> offers **Remember this selection** for the search field and
> **Maintain arm selection with Record Status Dashboard**. In 16.x LTS
> none of these options exist: a result always opens the form where the
> value was found (the Record Home Page for hits on the record ID). If
> you are on 16.x and want the Record Home Page, note the record ID and
> select it from the **Choose an existing [Record ID]** dropdown
> instead.

### 3.3 Record Status Dashboard

- In the left-hand menu, click Record Status Dashboard under Data
    Collection.

- The default dashboard shows all records, events, and instruments you
    have access to.

- Click any colored dot to open the corresponding instrument for that
    record.

### 3.4 Reports

- In the left-hand menu, click Data Exports, Reports, and Stats, then
    select a report.

- A Record ID displayed in a report is a clickable link. Where it
    goes depends on the row:

    - Classic projects: the first instrument you have access to for
        that record.
    - Longitudinal projects, rows that are not repeating instances: the
        Record Home Page.
    - Rows for a repeating instrument or repeating event instance: that
        instrument or event instance.

- Record IDs are not links when the project is in Analysis/Cleanup or
    Completed status.

### 3.5 Using the Record Home Page

- Once on the Record Home Page, you see all instruments for that
    record displayed as colored dots.

- Click any dot to open the corresponding instrument.

- After opening an instrument, the left-hand menu displays a list of
    all instruments for quick switching.

---

## 4. Instrument Status Dot Colors

Every instrument in REDCap is represented by a colored dot. The color
encodes the completion status of that instrument for a given record.

| **Dot Appearance** | **Meaning** |
| --- | --- |
| Grey | Not started — no form status has been saved for this instrument yet. This is the default state. |
| Red | The instrument has been saved (or data imported into it), but the Form Status field is still set to Incomplete. |
| Yellow | Form Status field is set to Unverified by a user. |
| Green | Form Status field is set to Complete by a user. |
| Orange with white checkmark | A survey response was started but not finished (partial response, e.g. the participant left mid-survey), or a completed survey whose Form Status was later changed to Incomplete or Unverified. |
| Green with white checkmark | The survey was completed in full and its Form Status is still Complete. |
| Blue stacked icon | Several instances (repeating instrument or event) with mixed statuses. |
| Stacked icon in one colour | Several instances, all with that status. |

> **Version caveat (present in 17.6 Standard, not in 17.3 LTS):** A
> purple **Partial MyCap Response** icon marks an instrument a
> participant started but did not finish in the MyCap app. If you use
> MyCap on 17.3 LTS, such responses show with the ordinary form status
> icons; check the MyCap task data rather than relying on the icon.

**Important distinctions:**

- REDCap sets grey and red automatically: an instrument stays grey
    until it is saved or data is imported into it, then turns red
    while its Form Status is Incomplete.

- Values saved in the background from another instrument (for example
    a calculated field updated when a different form is saved) do not
    turn a grey dot red. The dot changes only when that instrument
    itself is saved or data is imported into it.

- Importing data into an instrument without its `[instrument]_complete`
    column sets its Form Status to Incomplete, so the dot turns red.

- Yellow and green statuses are set manually by the study team ---
    they are optional but recommended for projects with many
    instruments.

- Survey icons (orange and green with checkmarks) come from the survey
    response itself: REDCap marks a response as partial when it was
    started but not finished, and complete when the participant
    finished it. The icon then combines that with the Form Status.


> **Technical Note:** Form completion status is stored in `[instrument]_complete` with three coded values: 0 = Incomplete, 1 = Unverified, 2 = Complete. Grey (not started) and red both export as 0 by default; an API export option can return a blank value for grey instruments instead (`exportBlankForGrayFormStatus`). There is no separate coded survey-status field, and survey status cannot be set through data import or the API. Exports only include the survey timestamp column (`[instrument]_timestamp`), which holds the completion date-time or "[not completed]" and is ignored on import.


---

## 5. Common Questions

**Q: What is the fastest way to find a specific record in a large
project?**

**A:** Use Add/Edit Records and the Data Search feature. Searching within a
specific variable (such as Record ID or email) is faster than searching
across all variables.

**Q: Can I navigate to an instrument directly without going through the
Record Home Page?**

**A:** Yes. Clicking any colored dot in the Record Status Dashboard takes
you directly to the corresponding instrument without visiting the Record
Home Page first. Reports have no status dots, but in classic projects a
Record ID link in a report opens the first instrument you can access, and
for repeating-instance rows it opens that instance.

**Q: What does a red dot mean — is something wrong?**

**A:** No. A red dot simply means data has been entered but the Form Status
field has not been changed from its default value of Incomplete. It does
not indicate an error.

**Q: Can I change instrument statuses for many records at once?**

**A:** Yes. Instrument statuses are stored in the dataset and can be set in
bulk using REDCap's data import tools. Use coded values: 0 =
incomplete, 1 = unverified, 2 = complete. Survey status (partial or
complete) cannot be imported; it comes only from the survey response.

**Q: What happens to the dot color if I enter a single data point but
leave everything else blank?**

**A:** The dot turns red. Saving the instrument — even with a single
field filled in — changes the dot from grey to red. Values written in the
background from another instrument (such as calculations) do not.

---

## 6. Common Mistakes & Gotchas

- Confusing grey and red: grey means no form status has been saved
    yet; red means the instrument has been saved but the form status is
    still Incomplete. Both export as 0 by default, but have different
    visual meanings. A grey instrument can still hold background values
    such as calculations saved from another form.

- Ignoring optional statuses: teams that skip yellow/green statuses on
    large projects often lose track of which instruments have been
    reviewed vs. just filled in.

- Searching all variables in a large project: this can be slow. Always
    prefer variable-specific search when you know which field to look
    in.

- Expecting survey statuses on non-survey instruments: orange and
    green-checkmark dots only appear on instruments that are enabled as
    surveys.

---

## 7. Related Articles

- [RC-NAV-UI-01 — Project Navigation UI](RC-NAV-UI-01_Project-Navigation-UI.md) — the two-panel layout and
    how to navigate to a project from the REDCap home page

- [RC-NAV-REC-02 — Longitudinal Mode & Arms](RC-NAV-REC-02_Longitudinal-Mode-and-Arms.md) — how events and arms
    change the Record Home Page and dashboard layout

- [RC-NAV-REC-03 — Repeated Instruments & Repeated Events](RC-NAV-REC-03_Repeated-Instruments-and-Events.md) — visual
    indicators and navigation for repeated entries

- [RC-NAV-REC-04 — Record Status Dashboard & Other Record Links](RC-NAV-REC-04_Record-Status-Dashboard-and-Links.md) —
    detailed guide to the dashboard and all locations that link to
    records

- [RC-DE-01 — Record Creation & the Record Home Page](RC-DE-01_Record-Creation-and-Record-Home-Page.md) — creating new
    records and the full anatomy of the Record Home Page

- [RC-DE-02 — Basic Data Entry](RC-DE-02_Basic-Data-Entry.md) — step-by-step data entry on
    instruments reached via the navigation paths described here

- [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md) — how events and arms are
    configured; prerequisite for understanding longitudinal navigation

- [RC-LONG-02 — Repeated Instruments & Events Setup](RC-LONG-02_Repeated-Instruments-and-Events-Setup.md) — how repeated
    instruments and events are configured; prerequisite for
    understanding repeated-entry navigation

- [RC-IMP-01 — Data Import Overview](RC-IMP-01_Data-Import-Overview.md) — bulk-updating instrument
    status values (the colored dots) via data import

- [RC-EXPRT-06 — Custom Reports: Setup & Field Selection](RC-EXPRT-06_Custom-Reports-Setup-and-Field-Selection.md)
    — building custom reports; Record IDs in reports link back to the
    record (see §3.4 for where each link opens)
