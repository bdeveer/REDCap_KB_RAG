RC-FD-03

**Data Dictionary**

| **Article ID** | RC-FD-03 |
| --- | --- |
| **Domain** | Form Design |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Prerequisite** | RC-FD-01 — Form Design Overview; familiarity with spreadsheet editing |
| **Skill Level** | Advanced |
| **Version** | 1.0 |
| **Last Updated** | 2025 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-FD-01 — Form Design Overview; RC-FD-02 — Online Designer; RC-FD-05 — Codebook |

---

# 1. Overview

The Data Dictionary is REDCap\'s spreadsheet-based instrument design
tool. It allows you to define or modify every variable and instrument in
a project by editing a CSV file and uploading it back into REDCap. The
upload overwrites the existing instrument configuration. This article
explains what the Data Dictionary is, when to use it, and the essential
safety practices that prevent data loss.

---

# 2. Key Concepts & Definitions

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

**Data Dictionary Snapshot**

A saved copy of the current Data Dictionary downloaded before making
changes. A snapshot is the primary recovery tool if an upload produces
unintended results. Downloading a snapshot before any significant edit
is a non-negotiable best practice.

**Variable Name**

The unique internal identifier for a field within a REDCap project.
Variable names are used in branching logic expressions, exports, API
calls, and smart variables. They must be lowercase, contain only
letters, numbers, and underscores, and be unique across the entire
project.

**Instrument Name (Form Name)**

The internal identifier for an instrument. In the Data Dictionary, each
row\'s instrument assignment is defined by the form\_name column. Rows
with the same form\_name belong to the same instrument. Changing the
form\_name for a group of variables in the Data Dictionary moves them to
a different instrument — this is how instrument splitting and merging
works.

---

# 3. Accessing the Data Dictionary

## 3.1 Downloading the Current Data Dictionary

- From the Project Setup page or Designer page, click Download the
    current Data Dictionary in the Design Your Data Collection
    Instruments section.

- Alternatively, click the Data Dictionary button in the Online
    Designer to download and access the upload interface.

- The downloaded file is a CSV. Open it in spreadsheet software
    (Excel, Google Sheets, LibreOffice Calc) for editing.

## 3.2 Uploading a Modified Data Dictionary

- From the Project Setup page or Designer page, click the Data
    Dictionary button to open the upload interface.

- Select your modified CSV file and click Upload File.

- REDCap validates the file before applying it. Errors are surfaced
    with row-level detail so they can be corrected before re-uploading.

- If no errors are found, REDCap displays a summary of what will
    change. Confirm the upload to apply the changes.

---

# 4. What the Data Dictionary Can Do

- Define any number of variables and instruments in a single upload
    — far more efficient than the Online Designer for large projects.

- Split one instrument into two or more by changing the form\_name
    values for a subset of variables.

- Merge variables from multiple instruments into one by assigning them
    all the same form\_name.

- Rename variables and instruments in bulk.

- Set or modify branching logic, field labels, choices, and validation
    rules for many variables at once.

- Reorder variables by changing their row order in the CSV.

- **What it cannot do:** provide the real-time guardrails that the
    Online Designer offers. Errors in the Data Dictionary are only
    caught at upload time, not as you edit the file.

---

# 5. Essential Safety Practices

  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Critical:** The Data Dictionary overwrites your existing project configuration on upload. Always download and save a snapshot of the current Data Dictionary before making any significant changes. This is your only reliable recovery path if an upload produces unintended results.
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 5.1 Before Uploading

- Download the current Data Dictionary and save it as a backup ---
    label it with the date (e.g.,
    data\_dict\_2025-03-15\_before\_edit.csv).

- Make your edits on a copy, not on the only copy.

- Review REDCap\'s validation output before confirming the upload. The
    summary tells you exactly what will be added, changed, or deleted.

## 5.2 Recovering from a Bad Upload

- If an upload produces unintended results, re-upload the snapshot you
    saved before making changes.

- If no snapshot exists, use the Codebook (RC-FD-05) or the current
    Online Designer view to manually reconstruct what was there before
    — a slow and error-prone process.

- In Production mode, bad changes may have already entered the change
    queue. Cancel pending changes before they are approved if possible.

---

# 6. When to Use the Data Dictionary

The Data Dictionary is the right tool in these situations:

- You are an advanced REDCap user *familiar with the variable
    definition schema and comfortable editing CSVs.*

- You need to define a large number of variables quickly *--- building
    an instrument with dozens or hundreds of fields is far faster in a
    spreadsheet than one-by-one in the Online Designer.*

- You need to split an instrument *--- changing form\_name values for
    a group of variables is the only way to move variables between
    instruments in bulk.*

- You want to make the same change across many variables at once *---
    bulk edits to labels, choices, or branching logic are easily done
    with spreadsheet find-and-replace.*

---

# 7. Common Questions

**Q: What happens to data already collected if I delete a variable via
the Data Dictionary?**

**A:** Collected data in that variable is permanently deleted from the
project. REDCap will warn you during the upload review if variables with
data are about to be removed, but the deletion is irreversible once
confirmed. Never remove a variable that contains real participant data
without first exporting that data.

**Q: Can I use the Data Dictionary to split one instrument into two?**

**A:** Yes. This is one of the Data Dictionary\'s key capabilities. Change
the form\_name value for the variables you want to move to a new
instrument. If the new form\_name doesn\'t yet exist, REDCap creates it.
If it matches an existing instrument, the variables are merged into it.

**Q: I uploaded a Data Dictionary and now some variables are missing.
What happened?**

**A:** Variables present in the existing project but absent from the
uploaded CSV are deleted during the upload. If you accidentally left
rows out of your edited file, re-upload your pre-edit snapshot to
restore the original state.

**Q: Does the Data Dictionary work the same way in Production mode as in
Development mode?**

**A:** In Development mode, uploads apply immediately. In Production mode,
Data Dictionary uploads go through the same change queue review process
as Online Designer changes. The upload itself is allowed, but changes
are not live until approved.

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
- The **Codebook** (web view and PDF export) — appearing as the final field in each instrument section
- **Data exports** — with the variable name `{form_name}_complete`

They are intentionally absent from:
- The **Data Dictionary CSV** download
- The **Data Dictionary upload** schema

This explains why the field count in a Codebook PDF is always higher
than in the corresponding Data Dictionary: the Codebook will have exactly
one additional field per instrument (the `_complete` field for each).
Despite not being in the Data Dictionary, `_complete` fields are fully
usable in branching logic and calculated fields — for example,
`[intake_complete] = '2'` to check whether a form has been marked Complete.

---

# 8. Common Mistakes & Gotchas

- Uploading without a backup: the most common and costliest mistake.
    Always download a snapshot of the current Data Dictionary before
    uploading a modified version. There is no undo once a bad upload is
    confirmed.

- Accidentally omitting rows from the upload file: if you filter or
    sort your spreadsheet and accidentally delete rows before saving,
    the upload will delete those variables from the project.
    Double-check row counts before uploading.

- Changing variable names for existing variables: renaming a variable
    in the Data Dictionary creates a new variable and deletes the old
    one — including any data stored in it. Variable names should be
    treated as permanent once data collection begins.

- Editing the file in a tool that corrupts the CSV format: some
    applications convert numbers, add BOM characters, or change line
    endings in ways that cause REDCap to reject the file. If uploads
    fail with unexpected encoding errors, try saving the file as UTF-8
    CSV without BOM.

- Assuming the Data Dictionary validates study design: like the Online
    Designer, the Data Dictionary only catches technical errors (invalid
    field types, malformed logic syntax). It does not assess whether
    your instrument is appropriate for your research goals.

- Expecting `_complete` fields to appear in the Data Dictionary: the
    completion status fields (e.g., `application_complete`) are
    auto-generated by REDCap and do not appear in the Data Dictionary CSV.
    They show up in the Codebook and in data exports, but they are not
    user-definable and cannot be managed through a Data Dictionary upload.
    If you notice the field counts differ between your Codebook PDF and your
    Data Dictionary, this is the reason.

## API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See RC-API-01 — REDCap API for authentication, token management, and setup.

- **RC-API-07 — Export Metadata (Data Dictionary) API** — export the full data dictionary as JSON or CSV programmatically
- **RC-API-08 — Import Metadata (Data Dictionary) API** — upload a new or modified data dictionary to the project programmatically

---


# 9. Related Articles

- RC-FD-01 — Form Design Overview (prerequisite — tool selection
    and navigation)

- RC-FD-02 — Online Designer (the guardrailed alternative for
    smaller changes)

- RC-FD-05 — Codebook (useful as a reference when building or
    reviewing the Data Dictionary)
