

**Record Creation & the Record Home Page**

| **Article ID** | [RC-DE-01 — Record Creation & the Record Home Page](RC-DE-01_Record-Creation-and-Record-Home-Page.md) |
|---|---|
| **Domain** | Data Entry |
| **Applies To** | All REDCap project types |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — record creation and Record Home Page behaviour checked against source code; pages not re-captured |
| **Prerequisite** | [RC-NAV-REC-01 — Record Navigation Overview](RC-NAV-REC-01_Record-Navigation-Overview.md) |
| **Version** | 1.2 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-DE-02 — Basic Data Entry](RC-DE-02_Basic-Data-Entry.md); [RC-NAV-REC-01 — Record Navigation Overview](RC-NAV-REC-01_Record-Navigation-Overview.md); [RC-NAV-REC-04 — Record Status Dashboard & Other Record Links](RC-NAV-REC-04_Record-Status-Dashboard-and-Links.md)|
| **Synonyms** | how do i create a new record in redcap; add a new participant or record; use the add edit records page; what is the record home page; how does redcap assign a record id; navigate to an existing record; create record data entry; find a record by its id |

---

## 1. Overview

This article explains how to create new records in REDCap and how to
navigate to existing ones using the Add/Edit Records page. It also
describes the Record Home Page — the central hub for any single record
--- and explains how REDCap assigns and uses the Record ID.

---

## 2. Key Concepts & Definitions

**Record**

The fundamental unit of data storage in REDCap. Each record represents
one participant, patient, or subject. All data entered into instruments
is associated with a specific record.

**Record ID**

The primary identifier for every record in a REDCap project. REDCap uses
the Record ID as the internal reference linking all instruments and
events to a single participant. By default, record auto-numbering is
on and REDCap assigns Record IDs as incrementing integers (1, 2, 3...):
the next ID is the highest existing numeric ID plus one, so gaps left by
deleted records are not refilled. Users assigned to a Data Access Group
get IDs prefixed with their group's number (for example, 3-1, 3-2). The
Record ID field is the first field of the first instrument in every
project.

**Add/Edit Records Page**

The main data-collection menu page for finding and creating individual
records. Accessible from the left-hand Data Collection menu. It is the
fastest route to a specific record when you know the Record ID or
another searchable value. Users without the Create Records right see the
same page titled **View / Edit Records**, without the options to create
records. The page header shows the project's total record count (and,
for Data Access Group users, the count in their group); in Development
status it may also show a notice if your instance limits how many
records a Development project can hold.

**Record Home Page**

A per-record landing page showing all instruments associated with that
record as colored status dots. It is the hub for navigating to any form
within a single record.

**Data Search**

A search feature on the Add/Edit Records page that looks up records by
stored variable values, such as text boxes and notes boxes. It does not
search multiple-choice
variables (drop-downs, radio buttons, checkboxes, yes/no, true/false),
file uploads or descriptive text. It matches any value that contains
what you type and lists up to 25 results. Can be scoped to a single
variable for speed in large projects.

---

## 2a. Add/Edit Records Page Behaviour

Several changes make the page easier to work with on projects holding many records.

| Change | Version |
| --- | --- |
| The **record drop-down** and the **Data Search field drop-down** are both searchable — type to filter rather than scrolling | 17.0.7 |
| **User preferences** on the page: remember the last search target in the Data Search section, and force searches to open the record's **Record Home Page** rather than a data entry form. In multi-arm projects, arm selection can be maintained with the Record Status Dashboard | 16.1.4 |

> **Note:** The "Maintain arm selection with Record Status Dashboard" preference appears only in projects with **more than one arm**. It was briefly shown on single-arm projects in 16.1.4 and corrected in 16.1.5.

> **Version caveat (16.x LTS):** The searchable drop-downs and the user preferences above are not present in the 16.x LTS line; they are available in 17.x (Standard and the 17.3 LTS). On 16.x, scroll the drop-downs and use Data Search as described in Section 3.4.

> **Version caveat (below 17.4.1 Standard, and 16.x LTS):** Data Search failed to navigate correctly when the selected record's name contained a **pipe character** (`|`). The current 17.3 LTS is fixed. Relevant only to projects using pipes in record IDs, which is unusual but not unheard of in imported data. On an affected version, open such records from the record drop-down or the Record Status Dashboard instead, or avoid pipes in record IDs.

**Save & Go To Next Record** — from **15.7.0**, selecting this on the last record when record auto-numbering is enabled behaves sensibly rather than leaving the user in an undefined state.

---

## 3. Step-by-Step Procedures

### 3.1 Navigating to the Add/Edit Records Page

- Log in to your REDCap instance and open the project from the My
    Projects page.

- In the left-hand menu, under Data Collection, select Add / Edit
    Records.

### 3.2 Creating a New Record

- On the Add/Edit Records page, select the Add new record button. In
    a project with more than one arm, first choose the arm; the button
    then reads "Add new record for the arm selected above".

- REDCap automatically assigns the next available Record ID
    (incrementing integer).

- If the project contains only a single instrument (or the arm has one
    event with one instrument), REDCap opens that instrument directly.

- If the project contains multiple instruments or events, REDCap opens
    the Record Home Page first.

- The record does not exist until you save data on an instrument. The
    Record Status Dashboard has its own Add new record button that works
    the same way.

The Add new record button appears only when record auto-numbering is
enabled and you have the Create Records right. When auto-numbering is
off, the page instead shows a box labelled "Enter a new or existing
[Record ID]" (using your project's Record ID label): type the ID you
want and press Enter to create that record, or to open it if it already
exists.


> **Important:** A Record ID is never edited on the data entry form. To change one later, a user with the **Rename Records** user right uses the record action menu on the Record Home Page (see [RC-DE-13 — Record Administration: Choose Action for Record](RC-DE-13_Record-Administration-Choose-Action-for-Record.md)). In practice, treat the Record ID as fixed and as an opaque system identifier — avoid using it as a meaningful clinical or participant identifier.


### 3.3 Finding an Existing Record by ID

- On the Add/Edit Records page, use the Choose an existing record
    dropdown.

- The dropdown lists all Record IDs in the project (in your own Data
    Access Group, if you are assigned to one). If the project defines a
    custom record label or a secondary unique field, those values are
    shown next to each ID. Select the one you want.

- Selecting a Record ID takes you directly to the Record Home Page for
    that record.

- In projects with more than 25,000 records the dropdown is replaced
    by a text box: type the exact Record ID and press Enter. For large
    projects in general, Data Search (Section 3.4) is often quicker.

### 3.4 Finding an Existing Record by Value (Data Search)

- On the Add/Edit Records page, locate the Data Search section.

- Type a value (e.g., a name, date of birth, email, or Record ID) into
    the search box. Matching results appear in a list as you type;
    select a result to open it. Pressing Enter alone does not open a
    record here.

- **Best practice:** when you know the exact Record ID and the page
    offers a Record ID text box (auto-numbering off, or a project over
    25,000 records), type the ID there and press Enter — it is the
    fastest path.

- By default REDCap searches all searchable variables (see Section 2).
    Values from a custom record label or secondary unique field are
    found too.

- To narrow the search: select a specific variable from the variable
    dropdown before searching. This is significantly faster in large
    projects, and in projects with more than 20,000 records you must
    choose a variable (the all-variables option is not offered).

- Selecting a result takes you directly to the instrument and record
    where that value was found. It opens the Record Home Page instead if
    you have set the user preference to do so, or if you have no access
    to that instrument.

### 3.5 The Record Home Page

- The Record Home Page displays all instruments for a record as
    colored status dots.

- In simple projects (single instrument, no events), the page shows
    one dot.

- In complex projects (multiple instruments, longitudinal events), the
    page shows a grid of dots — one per instrument-event combination.

- Select any dot to open the corresponding instrument for that record.

- Once inside an instrument, the left-hand menu shows a list of all
    instruments in the project for quick switching.


> **Note:** The 'Choose action for record' button on the Record Home Page provides advanced administrative functions (moving records, deleting records, etc.). These are covered in [RC-DE-13 — Record Administration: Choose Action for Record](RC-DE-13_Record-Administration-Choose-Action-for-Record.md).


---

## 4. Common Questions

**Q: What is the Record ID and why does REDCap need it?**

**A:** The Record ID is the unique identifier that REDCap uses to link all
forms, events, and data to a single participant. Every piece of data in
a REDCap project is associated with a Record ID. With record
auto-numbering on (the default), it is automatically assigned as an
incrementing integer when a new record is created.

**Q: Can I assign my own Record ID instead of using the
auto-incrementing number?**

**A:** Yes, if record auto-numbering is turned off for the project. The
Record ID cannot be typed on the data entry form; instead, users with
the Create Records right type the new ID into the "Enter a new or
existing [Record ID]" box on the Add/Edit Records page. Once a record
exists, its ID can be changed only by a user with the Rename Records
user right, from the Record Home Page. For most projects, the
auto-assigned ID is the recommended approach.

**Q: What happens if I select 'Add new record' by accident?**

**A:** REDCap creates a record and assigns it a Record ID as soon as you
save any data. If you selected 'Add new record' but have not saved
anything yet, you can navigate away without creating a record. If data
was already saved, contact your project administrator to delete the test
record.

**Q: What is the fastest way to find a record when I know the Record
ID?**

**A:** If the Add/Edit Records page shows a Record ID text box
(auto-numbering off, or more than 25,000 records), type the ID there and
press Enter. Otherwise, type the ID into the searchable record dropdown
or the Data Search box and pick it from the matching results. Either is
faster than scrolling through the dropdown in large projects.

**Q: I can see the Record Home Page but some dots are missing. Why?**

**A:** The most likely reasons are: (1) your user access does not include
permission to view certain instruments, or (2) the project is
longitudinal and those instruments are not assigned to every event, or
(3) Form Display Logic is hiding or disabling those instruments until its
conditions are met. In a project with Data Access Groups, you may also
only see records from your own group.

**Q: Can I navigate directly to an instrument without going through the
Record Home Page?**

**A:** Yes. You can select any dot in the Record Status Dashboard to go
directly to that instrument for that record, bypassing the Record Home
Page entirely.

**Q: How can I bulk create multiple records at once instead of adding them one by one?**

**A:** You can import multiple records at once using the CSV import feature or the REDCap API. For CSV import, select **Data Import Tool** in the left-hand menu. Creating new records this way requires the Create Records right in addition to data import rights. For programmatic creation, use the [RC-API-03 — Import Records API](RC-API-03_Import-Records.md) to create records in batch. Both methods are faster than manually creating records through the Add/Edit Records page.

---

## 5. Common Mistakes & Gotchas

- Searching all variables in a large project: searching across all
    variables can be slow in projects with thousands of records and many
    fields. Always scope your search to a specific variable when you
    know which field to search in.

- Confusing the Add/Edit Records dropdown with Data Search: the
    dropdown lists Record IDs (plus any custom record label or secondary
    unique field); Data Search finds records by stored text values. Use
    Data Search when you know a value but not the Record ID.

- Searching for a multiple-choice answer: Data Search does not look in
    drop-down, radio, checkbox, yes/no or true/false variables. Use a
    report with a filter to find records by those answers.

- Creating duplicate records by accident: selecting 'Add new record'
    more than once does not create extra records — nothing is created
    until you save, and the same ID is offered again. Duplicates arise
    when someone saves a new record for a participant who already has
    one. Check whether a record already exists via Data Search before
    creating a new one.

- Expecting the Record Home Page to look the same in every project:
    simple projects show a single dot; longitudinal projects show a
    grid. The layout depends entirely on the project configuration.

### API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) for authentication, token management, and setup.

- **[RC-API-03 — Import Records API](RC-API-03_Import-Records.md)** — create new records programmatically by importing data; a new record is created if the record ID does not exist
- **[RC-API-05 — Rename Record API](RC-API-05_Rename-Record.md)** — rename an existing record ID to a new value programmatically

---


## 6. Related Articles

- [RC-DE-02 — Basic Data Entry](RC-DE-02_Basic-Data-Entry.md) (field types, saving, form status)

- [RC-DE-03 — Longitudinal Projects & DAGs](RC-DE-03_Longitudinal-Projects-and-DAGs.md) (how project
    structure affects the Record Home Page)

- [RC-NAV-REC-01 — Record Navigation Overview](RC-NAV-REC-01_Record-Navigation-Overview.md) (dot colors, navigation
    paths)

- [RC-NAV-REC-04 — Record Status Dashboard & Other Record Links](RC-NAV-REC-04_Record-Status-Dashboard-and-Links.md)
