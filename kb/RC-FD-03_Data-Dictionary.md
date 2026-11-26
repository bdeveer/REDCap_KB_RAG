

**Data Dictionary**

| **Article ID** | [RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md) |
|---|---|
| **Domain** | Form Design |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.4.1 (Standard) / v17.3.7 (LTS) — changelog review; page not re-captured. Data dictionary upload behaviour checked against source code of v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) |
| **Prerequisite** | [RC-FD-01 — Form Design Overview](RC-FD-01_Form-Design-Overview.md); familiarity with spreadsheet editing |
| **Skill Level** | Advanced |
| **Version** | 1.2 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-FD-01 — Form Design Overview](RC-FD-01_Form-Design-Overview.md); [RC-FD-02 — Online Designer](RC-FD-02_Online-Designer.md); [RC-FD-05 — Codebook](RC-FD-05_Codebook.md) |
| **Synonyms** | what is the data dictionary; build instruments with a spreadsheet; upload a data dictionary csv; download and edit the data dictionary; design forms in excel and upload; data dictionary overwrites my project warning; bulk edit fields via csv; how to use the redcap data dictionary; restore a previous data dictionary snapshot |

---

## 1. Overview

The Data Dictionary is REDCap's spreadsheet-based instrument design
tool. It allows you to define or modify every variable and instrument in
a project by editing a CSV file and uploading it back into REDCap. The
upload overwrites the existing instrument configuration. This article
explains what the Data Dictionary is, when to use it, and the essential
safety practices that prevent data loss.

---

## 2. Key Concepts & Definitions

**Data Dictionary**

A CSV file that contains a complete definition of every variable in a
REDCap project — including field type, field label, choices,
validation rules, branching logic, and instrument assignment. Uploading
a Data Dictionary to REDCap overwrites the current instrument
configuration entirely.

**Overwrite Behavior**

When a Data Dictionary is uploaded, REDCap replaces its current variable
and instrument definitions with those in the uploaded file. Variables
present in the current project but absent from the uploaded file are
deleted. This behavior makes the Data Dictionary powerful for
restructuring but dangerous if used carelessly.

When a variable is deleted, its collected data is no longer accessible
in forms, reports or exports. REDCap does not purge it, and it can
reappear if a variable with the same name is created again — so
deleting a variable is not a way to remove sensitive data, and you
should avoid reusing old variable names for new purposes.

**Data Dictionary Snapshot**

A saved copy of the Data Dictionary as it was at a point in time. REDCap
takes one automatically every time a Data Dictionary upload is committed
(and every time metadata is imported through the API); in Draft Mode the
snapshot is of the drafted version. You can also take one at any time
with the **Create snapshot of instruments** button. All snapshots are
listed on **Project Setup → Project Revision History**, where they can be
downloaded and compared. Downloading your own dated copy before a
significant edit is still good practice — it is the file you edited
from, and it is to hand if you need to roll back quickly.

**Variable Name**

The unique internal identifier for a field within a REDCap project.
Variable names are used in branching logic expressions, exports, API
calls, and smart variables. They must be lowercase, contain only
letters, numbers, and underscores, and be unique across the entire
project. On upload, REDCap auto-corrects uppercase letters, spaces and
illegal characters and reports this as a warning; the remaining naming
problems are hard errors (see §3.3).

**Instrument Name (Form Name)**

The internal identifier for an instrument. In the Data Dictionary, each
row's instrument assignment is defined by the form\_name column. Rows
with the same form\_name belong to the same instrument. Changing the
form\_name for a group of variables in the Data Dictionary moves them to
a different instrument — this is how instrument splitting and merging
works.

Changing the form\_name of an *entire* existing instrument is treated as
deleting that instrument and creating a new one, not as a rename. See
§8 for what is lost when that happens.

---

## 3. Accessing the Data Dictionary

### 3.1 Downloading the Current Data Dictionary

- From the Project Setup page or Designer page, click Download the
    current Data Dictionary in the Design Your Data Collection
    Instruments section.

- Alternatively, click the Data Dictionary button in the Online
    Designer to download and access the upload interface.

- The downloaded file is a CSV. Open it in spreadsheet software
    (Excel, Google Sheets, LibreOffice Calc) for editing.

### 3.2 Uploading a Modified Data Dictionary

- From the Project Setup page or Designer page, click the Data
    Dictionary button to open the upload interface.

- Choose the date format used in the file (DMY or MDY) and the
    delimiter (comma, tab or semicolon), select your modified CSV file
    and click **Upload File**. Only .csv files are accepted; Excel files
    (.xls/.xlsx) are rejected with a specific error, as are files that
    are not UTF-8 encoded.

- REDCap validates the file before applying it. Errors are surfaced
    with row-level detail so they can be corrected before re-uploading.
    Warnings do not block the upload.

- If no errors are found, REDCap shows any warnings and a single
    summary line stating that the file contains N fields, which will
    replace the M fields that currently exist. It does **not** list
    field by field what will be added, changed or deleted. Click
    **Commit Changes** to apply the upload.

- In Production, the upload is only possible while the project is in
    Draft Mode, and committing writes to the draft rather than the live
    project (see §7).

### 3.3 What the Upload Checks

Columns are read **by position**, not by header name: REDCap skips the
header row. Reordering, inserting or deleting columns shifts every value
into the wrong column. A legacy file with a "Field Units" column in
position C is rejected outright.

| Check | Result |
|---|---|
| Variable name starts with a digit or underscore, ends with an underscore, contains three underscores in a row, or is longer than 100 characters | Error |
| Variable name longer than 26 characters | Warning |
| Uppercase letters, spaces or illegal characters in a variable name | Auto-corrected, warning |
| Reserved variable names, names ending in the form name plus `_complete`, duplicate names | Error |
| Rows for one instrument not contiguous in the file | Error |
| Form name longer than 64 characters, or invalid field type | Error |
| Calculated field with no equation | Error |
| Deleting a randomization field, editing a PROMIS instrument, or adding an SQL field as a non-administrator | Error |
| Moving or deleting the record ID field (the first row) while records exist | **Warning only** — check this carefully |

The record ID is always the first field. REDCap forces it to be a text
field and clears any section header on it.

> **Version caveat (16.0 LTS vs 17.x):** On 17.x, invalid branching logic or calculation syntax is an error for every user unless that expression is unchanged from what is already in the project; 17.x also warns about an SQL field with no query. On 16.0 LTS, administrators uploading a file get only a warning for invalid branching or calculation syntax, so the upload can go through with broken expressions. If you are an administrator on 16.0, read every warning before committing and fix any flagged expression.

---

## 4. What the Data Dictionary Can Do

- Define any number of variables and instruments in a single upload
    — far more efficient than the Online Designer for large projects.

- Split one instrument into two or more by changing the form\_name
    values for a subset of variables.

- Merge variables from multiple instruments into one by assigning them
    all the same form\_name. Instruments whose form\_name disappears
    from the file are deleted (see §8).

- Rename variables and instruments in bulk — but REDCap treats a
    renamed variable or instrument as a deletion plus a new creation
    (see §8).

- Set or modify branching logic, field labels, choices, and validation
    rules for many variables at once.

- Reorder variables by changing their row order in the CSV.

- **What it cannot do:** provide the real-time guardrails that the
    Online Designer offers. Errors in the Data Dictionary are only
    caught at upload time, not as you edit the file.

---

> **Upload validation changes.** From **15.9.2**, uploading a data dictionary containing **multiple-choice fields with no choices defined** returns a **warning** rather than an error, matching the Online Designer's behaviour — the upload proceeds. From **17.0.3**, creating a project from a **Project XML** file **automatically comments out** any syntactically invalid branching logic, calculations or CALCTEXT, so the project is created rather than the import failing outright. The commented-out expressions remain visible in the field for repair, but they are **inactive** — check for them after importing an XML project rather than assuming everything came across live.

> **Version caveat (16.0 LTS):** The automatic commenting-out of invalid logic when creating a project from Project XML exists only on 17.0.3 and later; 16.0 LTS does not have it. On 16.0, fix any invalid branching logic or calculations in the source project before exporting the XML, as the import may otherwise fail.

> **Note (15.0.1):** The Data Dictionary page interface was simplified to make the edit-and-upload cycle clearer.

---

## 5. Essential Safety Practices


> **Critical:** The Data Dictionary overwrites your existing project configuration on upload. Always download and save a copy of the current Data Dictionary before making any significant changes. REDCap also keeps an automatic snapshot of the previous version on **Project Revision History**, but some things lost with a deleted or renamed instrument (see §8) cannot be restored from any snapshot.


### 5.1 Before Uploading

- Download the current Data Dictionary and save it as a backup ---
    label it with the date (e.g.,
    data\_dict\_2025-03-15\_before\_edit.csv).

- Make your edits on a copy, not on the only copy.

- Review REDCap's validation output before clicking **Commit
    Changes**. It shows errors, warnings and only a total field count
    ("contains N fields, which will replace the M fields that currently
    exist") — not a list of what will be added, changed or deleted.
    Compare your file with the backup yourself (row counts and variable
    names) to confirm no rows went missing. In
    Development, REDCap gives **no warning** that fields being deleted
    contain data.

- In Production, a field-by-field review (including "Deleted fields
    that contain data") appears only on the draft review page after you
    commit — check it before submitting the changes.

### 5.2 Recovering from a Bad Upload

- If an upload produces unintended results, re-upload the copy you
    saved before making changes.

- If you did not save a copy, download the automatic snapshot taken
    just before the upload from **Project Setup → Project Revision
    History** and re-upload it.

- Re-creating a deleted variable with its original name makes its
    earlier data visible again. Instrument-level items listed in §8
    (locking, e-signatures, event designations and so on) do not come
    back and must be set up again.

- The Codebook ([RC-FD-05 — Codebook](RC-FD-05_Codebook.md)) is a
    last resort for reconstructing the design by hand.

- In Production, a bad upload lands in the draft. You can discard the
    draft only **before** you submit it for review; after submitting,
    only an administrator can reset or reject it.

---

## 6. When to Use the Data Dictionary

The Data Dictionary is the right tool in these situations:

- You are an advanced REDCap user *familiar with the variable
    definition schema and comfortable editing CSVs.*

- You need to define a large number of variables quickly *--- building
    an instrument with dozens or hundreds of fields is far faster in a
    spreadsheet than one-by-one in the Online Designer.*

- You need to split an instrument *--- changing form\_name values for
    a group of variables is the fastest way to move many variables
    between instruments (the Online Designer's **Move field(s)** option
    also works for smaller moves).*

- You want to make the same change across many variables at once *---
    bulk edits to labels, choices, or branching logic are easily done
    with spreadsheet find-and-replace.*

---

## 7. Common Questions

**Q: What happens to data already collected if I delete a variable via
the Data Dictionary?**

**A:** The data is no longer accessible in forms, reports or exports, so
for users it is effectively gone. REDCap does not purge it, though: it
reappears if a variable with the same name is created again (for
example, by re-uploading an earlier snapshot). That means deleting a
variable is not a way to remove sensitive data, and reusing an old
variable name for a new question re-exposes the old values. Two
exceptions do destroy data: in Production, files stored in a deleted
File Upload field are marked for deletion when the draft is approved;
and deleting an instrument permanently removes its locking and
e-signature records.

REDCap gives **no warning** in Development that a deleted variable
contains data. In Production the warning appears only on the draft
review page after the upload is committed. Never remove a variable that
contains real participant data without first exporting that data.

**Q: Can I use the Data Dictionary to split one instrument into two?**

**A:** Yes. This is one of the Data Dictionary's key capabilities. Change
the form\_name value for the variables you want to move to a new
instrument. If the new form\_name doesn't yet exist, REDCap creates it.
If it matches an existing instrument, the variables are merged into it.
New instruments give existing users access to them. In a longitudinal
project a new instrument is not designated to any event until you add
it on **Define My Events**.

**Q: I uploaded a Data Dictionary and now some variables are missing.
What happened?**

**A:** Variables present in the existing project but absent from the
uploaded CSV are deleted during the upload. If you accidentally left
rows out of your edited file, re-upload your pre-edit copy, or the
automatic snapshot on **Project Revision History**, to restore the
original state. The data in those variables becomes visible again once
the variables are back.

**Q: Does the Data Dictionary work the same way in Production mode as in
Development mode?**

**A:** In Development mode, uploads apply immediately. In Production mode:

- The upload is blocked unless the project is in Draft Mode, and also
    while submitted drafts are awaiting review.
- Committing the upload writes it into the draft; nothing is live yet.
- You must then submit the draft for review, as with Online Designer
    changes. Depending on a Control Center setting it may be approved
    automatically (for example, when no fields with data are deleted
    and there are no critical issues); otherwise an administrator
    reviews it.
- You can discard the draft before submitting; after submitting, only
    an administrator can reset or reject it.

> **Institution-specific:** Whether drafts can be approved automatically, and under which conditions, is set by your REDCap administrators. Check with them before relying on it.

**Q: Can I edit the Data Dictionary in Google Sheets or LibreOffice
instead of Excel?**

**A:** Yes. The Data Dictionary is a standard CSV file and can be edited in
any spreadsheet application. Be aware that some applications may change
date formats or add unwanted characters. Always validate the upload in
REDCap before confirming, and check for encoding issues if REDCap flags
unexpected errors.

**Q: Is there a limit to how many variables I can define in one Data
Dictionary upload?**

**A:** There is no hard documented limit, but very large uploads (thousands
of variables) can take time to validate and apply. Test large uploads in
Development mode before doing them in Production.

**Q: Why do I see `_complete` fields in my Codebook and data exports but
not in my Data Dictionary?**

**A:** The `_complete` fields (e.g., `application_complete`, `intake_complete`)
are auto-generated by REDCap for every instrument. They record the
instrument's completion status using three fixed values: 0 = Incomplete,
1 = Unverified, 2 = Complete. Because they are system-managed rather than
user-defined, they do not appear in the Data Dictionary CSV and cannot be
added, edited, or removed through a Data Dictionary upload.

They are always present in:
- The **Codebook** (on screen and when printed) — appearing as the final field in each instrument section
- **Data exports** — with the variable name `{form_name}_complete`

They are intentionally absent from:
- The **Data Dictionary CSV** download
- The **Data Dictionary upload** schema

This explains why the field count in the Codebook is always higher
than in the corresponding Data Dictionary: the Codebook will have exactly
one additional field per instrument (the `_complete` field for each).
Despite not being in the Data Dictionary, `_complete` fields are fully
usable in branching logic and calculated fields — for example,
`[intake_complete] = '2'` to check whether a form has been marked Complete.

---

## 8. Common Mistakes & Gotchas

- Uploading without a backup: the most common and costliest mistake.
    Always download a copy of the current Data Dictionary before
    uploading a modified version. There is no undo button; recovery
    means re-uploading your copy or the automatic snapshot from
    **Project Revision History**, and instrument-level settings lost
    along the way must be rebuilt by hand.

- Accidentally omitting rows from the upload file: if you filter or
    sort your spreadsheet and accidentally delete rows before saving,
    the upload will delete those variables from the project.
    Double-check row counts before uploading.

- Changing variable names for existing variables: renaming a variable
    in the Data Dictionary creates a new, empty variable and deletes the
    old one. The old variable's data is no longer accessible in forms,
    reports or exports (it comes back only if the old name is restored).
    Variable names should be treated as permanent once data collection
    begins.

- Renaming an instrument (changing the form\_name of all its rows):
    REDCap deletes the old instrument and creates a new one. The old
    instrument's event designations, repeating-instrument settings,
    locking records, e-signatures, MyCap tasks and instrument-level
    user rights are permanently removed; its
    completion status is left behind and the new instrument starts with
    a fresh, empty `_complete` field; in a longitudinal project the new
    instrument is not designated to any event. If the instrument is a
    survey, the survey settings follow the rename only for the first
    instrument in the project. Use the Online Designer to change an
    instrument's label instead.

- Rearranging columns: columns are read by position, so moving,
    inserting or deleting a column (for example, hiding one and
    re-saving, or adding a notes column) shifts values into the wrong
    columns. Keep the downloaded column order exactly.

- Editing the file in a tool that corrupts the CSV format: some
    applications convert numbers, change dates or re-save the file in
    a non-UTF-8 encoding, which REDCap rejects. Save as **CSV UTF-8**.
    A byte-order mark (BOM) is harmless — REDCap's own downloads
    include one.

- Assuming the Data Dictionary validates study design: like the Online
    Designer, the Data Dictionary only catches technical errors (invalid
    field types, malformed logic syntax). It does not assess whether
    your instrument is appropriate for your research goals.

- Expecting `_complete` fields to appear in the Data Dictionary: the
    completion status fields (e.g., `application_complete`) are
    auto-generated by REDCap and do not appear in the Data Dictionary CSV.
    They show up in the Codebook and in data exports, but they are not
    user-definable and cannot be managed through a Data Dictionary upload.
    If you notice the field counts differ between your Codebook and your
    Data Dictionary, this is the reason.

### API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) for authentication, token management, and setup.

- **[RC-API-07 — Export Metadata (Data Dictionary) API](RC-API-07_Export-Metadata.md)** — export the full data dictionary as JSON or CSV programmatically
- **[RC-API-08 — Import Metadata (Data Dictionary) API](RC-API-08_Import-Metadata.md)** — upload a new or modified data dictionary to the project programmatically

---


## 9. Related Articles

- [RC-FD-01 — Form Design Overview](RC-FD-01_Form-Design-Overview.md) (prerequisite — tool selection
    and navigation)

- [RC-FD-02 — Online Designer](RC-FD-02_Online-Designer.md) (the guardrailed alternative for
    smaller changes)

- [RC-FD-05 — Codebook](RC-FD-05_Codebook.md) (useful as a reference when building or
    reviewing the Data Dictionary)
