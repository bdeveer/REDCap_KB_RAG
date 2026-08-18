---
id: RC-DE-01
title: Record Creation & the Record Home Page
domain: Data Entry
applies_to:
- All REDCap project types
requires: Any supported version
verified_against: REDCap v17.4.1 (Standard) / v17.3.7 (LTS) — changelog review; page
  not re-captured
prerequisites:
- RC-NAV-REC-01 — Record Navigation Overview
version: '1.1'
last_updated: 2026-08
related:
- id: RC-DE-02
  title: Basic Data Entry
- id: RC-NAV-REC-01
  title: Record Navigation Overview
- id: RC-NAV-REC-04
  title: Record Status Dashboard & Other Record Links
tags:
- data entry
synonyms:
- how do i create a new record in redcap
- add a new participant or record
- use the add edit records page
- what is the record home page
- how does redcap assign a record id
- navigate to an existing record
- create record data entry
- find a record by its id
---

# 1. Overview

This article explains how to create new records in REDCap and how to
navigate to existing ones using the Add/Edit Records page. It also
describes the Record Home Page — the central hub for any single record
--- and explains how REDCap assigns and uses the Record ID.

---

# 2. Key Concepts & Definitions

**Record**

The fundamental unit of data storage in REDCap. Each record represents
one participant, patient, or subject. All data entered into instruments
is associated with a specific record.

**Record ID**

The primary identifier for every record in a REDCap project. REDCap uses
the Record ID as the internal reference linking all instruments and
events to a single participant. By default, REDCap auto-assigns Record
IDs as incrementing integers (1, 2, 3...). The Record ID field is the
first field of the first instrument in every project.

**Add/Edit Records Page**

The main data-collection menu page for finding and creating individual
records. Accessible from the left-hand Data Collection menu. It is the
fastest route to a specific record when you know the Record ID or any
other identifying value.

**Record Home Page**

A per-record landing page showing all instruments associated with that
record as colored status dots. It is the hub for navigating to any form
within a single record.

**Data Search**

A search feature on the Add/Edit Records page that allows lookup by any
variable value across all records in a project. Can be scoped to a
single variable for speed in large projects.

---

# 2a. Add/Edit Records Page Behaviour

Several changes make the page easier to work with on projects holding many records.

| Change | Version |
| --- | --- |
| The **record drop-down** and the **Data Search field drop-down** are both searchable — type to filter rather than scrolling | 17.0.7 |
| **User preferences** on the page: remember the last search target in the Data Search section, and force searches to open the record's **Record Home Page** rather than a data entry form. In multi-arm projects, arm selection can be maintained with the Record Status Dashboard | 16.1.4 |

> **Note:** The "Maintain arm selection with Record Status Dashboard" preference appears only in projects with **more than one arm**. It was briefly shown on single-arm projects in 16.1.4 and corrected in 16.1.5.

> **Version caveat (below 17.4.1 Standard):** Data Search failed to navigate correctly when the selected record's name contained a **pipe character** (`|`). Relevant only to projects using pipes in record IDs, which is unusual but not unheard of in imported data.

**Save & Go To Next Record** — from **15.7.0**, clicking this on the last record when record auto-numbering is enabled behaves sensibly rather than leaving the user in an undefined state.

---

# 3. Step-by-Step Procedures

## 3.1 Navigating to the Add/Edit Records Page

- Log in to your REDCap instance and open the project from the My
    Projects page.

- In the left-hand menu, under Data Collection, click Add / Edit
    Records.

## 3.2 Creating a New Record

- On the Add/Edit Records page, click the Add new record button.

- REDCap automatically assigns the next available Record ID
    (incrementing integer).

- If the project contains only a single instrument, REDCap opens that
    instrument directly.

- If the project contains multiple instruments or events, REDCap opens
    the Record Home Page first.


> **Important:** The Record ID is permanent once assigned. It cannot be changed through normal data entry. Treat it as an opaque system identifier — avoid using it as a meaningful clinical or participant identifier.


## 3.3 Finding an Existing Record by ID

- On the Add/Edit Records page, use the Choose an existing record
    dropdown.

- The dropdown lists all Record IDs in the project. Select the one you
    want.

- Selecting a Record ID takes you directly to the Record Home Page for
    that record.

- In projects with a large number of records, use Data Search (Section
    3.4) instead — the dropdown becomes unwieldy at scale.

## 3.4 Finding an Existing Record by Value (Data Search)

- On the Add/Edit Records page, locate the Data Search section.

- **Best practice:** type the Record ID directly into the search box
    and press Enter. This is the fastest path to any record when the ID
    is known.

- To search by a different value (e.g., name, date of birth, email):
    enter the value in the search box. REDCap searches across all
    variables in all records by default.

- To narrow the search: select a specific variable from the variable
    dropdown before searching. This is significantly faster in large
    projects.

- Matching results appear in a dropdown. Selecting a result takes you
    directly to the instrument and record where that value was found.

## 3.5 The Record Home Page

- The Record Home Page displays all instruments for a record as
    colored status dots.

- In simple projects (single instrument, no events), the page shows
    one dot.

- In complex projects (multiple instruments, longitudinal events), the
    page shows a grid of dots — one per instrument-event combination.

- Click any dot to open the corresponding instrument for that record.

- Once inside an instrument, the left-hand menu shows a list of all
    instruments in the project for quick switching.


> **Note:** The 'Choose action for record' button on the Record Home Page provides advanced administrative functions (moving records, deleting records, etc.). These are covered in [RC-DE-13 — Record Administration: Choose Action for Record](RC-DE-13_Record-Administration-Choose-Action-for-Record.md).


---

# 4. Common Questions

**Q: What is the Record ID and why does REDCap need it?**

**A:** The Record ID is the unique identifier that REDCap uses to link all
forms, events, and data to a single participant. Every piece of data in
a REDCap project is associated with a Record ID. It is automatically
assigned as an incrementing integer when a new record is created.

**Q: Can I assign my own Record ID instead of using the
auto-incrementing number?**

**A:** Yes. The Record ID field is the first field of the first instrument,
and it can be edited like any other text field before the record is
saved for the first time. However, once a record ID is assigned and data
has been entered, changing it requires administrative intervention. For
most projects, the auto-assigned ID is the recommended approach.

**Q: What happens if I click 'Add new record' by accident?**

**A:** REDCap creates a record and assigns it a Record ID as soon as you
save any data. If you clicked 'Add new record' but have not saved
anything yet, you can navigate away without creating a record. If data
was already saved, contact your project administrator to delete the test
record.

**Q: What is the fastest way to find a record when I know the Record
ID?**

**A:** Use the Data Search box on the Add/Edit Records page. Type the Record
ID and press Enter. This is faster than scrolling through the dropdown
in large projects.

**Q: I can see the Record Home Page but some dots are missing. Why?**

**A:** The most likely reasons are: (1) your user access does not include
permission to view certain instruments, or (2) the project is
longitudinal and those instruments are not assigned to every event. In a
project with Data Access Groups, you may also only see records from your
own group.

**Q: Can I navigate directly to an instrument without going through the
Record Home Page?**

**A:** Yes. You can click any dot in the Record Status Dashboard to go
directly to that instrument for that record, bypassing the Record Home
Page entirely.

**Q: How can I bulk create multiple records at once instead of adding them one by one?**

**A:** You can import multiple records at once using the CSV import feature or the REDCap API. For CSV import, go to Data Import & Export on the left menu and use the Bulk Upload feature. For programmatic creation, use the [RC-API-03 — Import Records API](RC-API-03_Import-Records.md) to create records in batch. Both methods are faster than manually creating records through the Add/Edit Records page.

---

# 5. Common Mistakes & Gotchas

- Searching all variables in a large project: searching across all
    variables can be slow in projects with thousands of records and many
    fields. Always scope your search to a specific variable when you
    know which field to search in.

- Confusing the Add/Edit Records dropdown with Data Search: the
    dropdown lists Record IDs only; Data Search can find records by any
    field value. Use Data Search when you know a value but not the
    Record ID.

- Creating duplicate records by accident: if 'Add new record' is
    clicked more than once, multiple records are created. Check whether
    a record already exists via Data Search before creating a new one.

- Expecting the Record Home Page to look the same in every project:
    simple projects show a single dot; longitudinal projects show a
    grid. The layout depends entirely on the project configuration.

## API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) for authentication, token management, and setup.

- **[RC-API-03 — Import Records API](RC-API-03_Import-Records.md)** — create new records programmatically by importing data; a new record is created if the record ID does not exist
- **[RC-API-05 — Rename Record API](RC-API-05_Rename-Record.md)** — rename an existing record ID to a new value programmatically

---


# 6. Related Articles

- [RC-DE-02 — Basic Data Entry](RC-DE-02_Basic-Data-Entry.md) (field types, saving, form status)

- [RC-DE-03 — Longitudinal Projects & DAGs](RC-DE-03_Longitudinal-Projects-and-DAGs.md)(how project
    structure affects the Record Home Page)

- [RC-NAV-REC-01 — Record Navigation Overview](RC-NAV-REC-01_Record-Navigation-Overview.md) (dot colors, navigation
    paths)

- [RC-NAV-REC-04 — Record Status Dashboard & Other Record Links](RC-NAV-REC-04_Record-Status-Dashboard-and-Links.md)
