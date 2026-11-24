

**Record Data CSV Import — Column Reference and Format Guide**

| **Article ID** | [RC-IMP-04 — Record Data CSV Import — Column Reference and Format Guide](RC-IMP-04_Record-Data-CSV-Import.md) |
|---|---|
| **Domain** | Data Import |
| **Applies To** | All REDCap project types |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.5.4 (Standard) / v17.3.18 (LTS) — changelog review; page not re-captured. Record data CSV import behaviour checked against source code of v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) |
| **Prerequisite** | [RC-IMP-01 — Data Import Overview](RC-IMP-01_Data-Import-Overview.md); [RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap](RC-IMP-03_CSV-Upload-Reference.md)|
| **Skill Level** | Intermediate |
| **Version** | 1.3 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-IMP-01 — Data Import Overview](RC-IMP-01_Data-Import-Overview.md); [RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap](RC-IMP-03_CSV-Upload-Reference.md); [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md); [RC-LONG-02 — Repeated Instruments & Events Setup](RC-LONG-02_Repeated-Instruments-and-Events-Setup.md); [RC-API-03 — Import Records API](RC-API-03_Import-Records.md) |
| **Synonyms** | how do i import record data from a csv file; upload participant data with the data import tool; bulk import records into redcap; csv column format for importing data; re-import an exported csv back into the project; overwrite existing data with blank values on import; why is my imported data not saving; partial data import for specific fields or events |

---

## 1. Overview

The REDCap Data Import Tool accepts a CSV file containing participant record data. Any REDCap data export in CSV format can be re-imported into the same project as-is. Partial imports — covering specific fields, specific records, or specific events — are also fully supported.

**Location:** Applications → Data Import Tool. Importing requires the **Data Import Tool** user right.

**Upload behavior:** By default, blank cells in the import file are ignored and existing values are preserved — but any **non-blank** value in the file **replaces** the value already saved in that field. "Additive" applies only to blank cells and omitted columns. The optional overwrite setting also erases existing values wherever the file has a blank cell (for a checkbox column, a blank cell unchecks that choice). Blank `redcap_data_access_group` cells are ignored even in overwrite mode.

**Real-time vs background import.** The tool offers two modes, and they behave differently:

| | **Import in real time** | **Import as background process** |
|---|---|---|
| Preview before saving | Yes — "Upload File" stages the file and shows the results (and the data comparison table, if chosen) before you click **Import Data** | No — after a header check and a confirmation, the file is queued and imported; no comparison table |
| When some rows have errors | All-or-nothing: any error blocks the whole file and nothing is saved (warnings do not block) | Records without errors are imported; failed records can be downloaded afterwards |
| Suggested for | Smaller files | Larger files (REDCap suggests it for files over 1 MB) |

> **Important (real-time mode):** Clicking "Upload File" only stages a preview. The data is not saved until you scroll down and click **Import Data** on the results screen. Navigating away after "Upload File" discards the staged import without saving anything. In **background** mode there is no preview step — confirming the upload starts the import.

For a general overview of the Data Import Tool workflow, see [RC-IMP-01 — Data Import Overview](RC-IMP-01_Data-Import-Overview.md), Sections 8 and 9.

---

## 2. Column Reference

Every record data CSV — whether built from scratch or downloaded from REDCap — uses the same set of column types. The columns below appear in the order REDCap places them in a standard export.

| **Column** | **Required?** | **Notes** |
|---|---|---|
| `record_id` *(or project-specific name)* | Always | First column. The variable name must match the project's Record ID field exactly (e.g., `participant_id`, `patient_id`). |
| `redcap_event_name` | Longitudinal projects | Unique event name in the format `uniqueeventname_arm_N` (e.g., `baseline_arm_1`). Find all values under Project Setup → Define My Events. |
| `redcap_repeat_instrument` | Repeating instruments | The instrument's unique name (lowercase, underscored) for the repeating instrument this row belongs to. Empty for regular event rows and for repeating-event rows — an instrument name on a row for a **repeating event** is an error. |
| `redcap_repeat_instance` | Repeating instruments or events | Integer instance number from 1 to 32767. Use the value `new` to let REDCap assign the next available instance number automatically. REDCap reads each row according to the **project's repeating setup**, not according to which columns are blank: a row for a repeating event must have an instance number, and repeat values on an event or instrument that is not set up to repeat are rejected with an error. |
| `redcap_survey_identifier` | Never import | Present in exports — holds the survey participant identifier (e.g., name or email used for survey invitations). **Read-only system value. Omit this column or leave it blank on import; the Data Import Tool ignores it.** |
| `redcap_data_access_group` | Conditional | Only for users who are **not** assigned to a DAG: enter the DAG's unique group name to place the record in that DAG. Users who **are** assigned to a DAG must leave the column out — including it gives the error "Illegal use of 'redcap_data_access_group' field!". Their new records go into their own DAG automatically, and they cannot import into records outside their DAG. Blank cells are ignored, so an import cannot remove a record from a DAG. Omit entirely if the project does not use DAGs. |
| *Instrument fields* (e.g., `screen_age_over_18`) | As needed | Include only the variables you want to set. Omitting a column leaves existing data unchanged (additive behavior). Values must be raw-coded (numbers, dates, text) — not choice labels. |
| `fieldname___N` *(checkbox choices)* | As needed | Checkbox fields produce one column per answer choice. `N` is the raw coded value for that choice (e.g., `demo_race___1`, `demo_race___2`). Values are `1` (checked) or `0` (unchecked). Omitting a checkbox column leaves existing checked state unchanged. |
| `*_timestamp` *(e.g., `demographics_timestamp`)* | Never import | Present in exports — auto-generated timestamp recording when a survey instrument was submitted. **Read-only system value. Omit or leave blank; values in these columns are ignored by the Data Import Tool (with a warning, not an error).** |
| `*_complete` *(e.g., `demographics_complete`)* | Optional | Form completion status. Integer: `0` = Incomplete, `1` = Unverified, `2` = Complete. Import to set or update form status. When omitted, existing status is unchanged. The status of an instrument that holds a **survey response** cannot be changed by import. |

---

## 3. Example: Longitudinal Project with a Repeating Instrument

The table below illustrates how a single record spans multiple rows in a longitudinal project that also has a repeating instrument (`medication_list`). Only selected columns are shown — a real export includes all project fields across all instruments, so most cells in any given row will be empty.

| `record_id` | `redcap_event_name` | `redcap_repeat_instrument` | `redcap_repeat_instance` | `screen_date` | `phq9_total` | `med_name` | `med_start_date` | `screening_complete` | `phq9_complete` | `medication_list_complete` |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `screening_arm_1` | *(empty)* | *(empty)* | 2026-04-30 | *(empty)* | *(empty)* | *(empty)* | 1 | *(empty)* | *(empty)* |
| 1 | `baseline_arm_1` | *(empty)* | *(empty)* | *(empty)* | 12 | *(empty)* | *(empty)* | *(empty)* | 0 | *(empty)* |
| 1 | `3_month_arm_1` | *(empty)* | *(empty)* | *(empty)* | 10 | *(empty)* | *(empty)* | *(empty)* | 1 | *(empty)* |
| 1 | `baseline_arm_1` | `medication_list` | 1 | *(empty)* | *(empty)* | Metformin | 2026-05-01 | *(empty)* | *(empty)* | 2 |
| 1 | `baseline_arm_1` | `medication_list` | 2 | *(empty)* | *(empty)* | Lisinopril | 2026-05-01 | *(empty)* | *(empty)* | 1 |
| 1 | `3_month_arm_1` | `medication_list` | 1 | *(empty)* | *(empty)* | Metformin | 2026-05-01 | *(empty)* | *(empty)* | 0 |

Key points illustrated by this example:

- **One row per event** — regular (non-repeating) event data goes in a row where both repeat columns are empty. REDCap includes a row for every event in an export, even events with no data entered.
- **One row per repeating instrument instance** — each instance of a repeating instrument gets its own row with `redcap_repeat_instrument` and `redcap_repeat_instance` filled in.
- **Same repeating instrument at multiple events** — `medication_list` has instances at both `baseline_arm_1` and `3_month_arm_1`. Instance numbers are independent per event — instance 1 at baseline and instance 1 at 3 months are separate instances of the same record.
- **Most cells are empty in any given row** — a row carries data only for the fields belonging to that event or instrument instance. In a wide project with many instruments, the vast majority of cells will be empty. This is correct and expected — not a sign of file corruption.
- **Complete status columns (`*_complete`) appear at the end of each instrument's field group** — they can be imported alongside data fields or omitted.

---

## 4. Getting the Right Header Row

Two methods reliably produce the correct column layout for your project:

- **Download the Data Import Template** from within the Data Import Tool. The template is header-only (no data rows) and includes the exact column set and coordinate variables your project requires. It leaves out fields that cannot be imported (calculated, file upload and descriptive fields), and it includes `redcap_data_access_group` only if the project has DAGs and you are not assigned to one.
- **Export existing data** from Applications → Data Exports, Reports & Stats. The export uses the same header structure and, if records already exist, provides real examples of correctly formatted values.

Building the header row manually is error-prone. Always start from one of these two sources. The record ID column must be the first column (cell A1), and its header must match the Record ID variable name exactly — a header typed in capital letters does not match.

---

## 4b. What the Import Rejects, Ignores or Changes

Errors stop the affected data from importing (in real-time mode, the whole file); warnings are shown but do not block. Nothing listed as an error is skipped silently.

| **Situation** | **Result** |
|---|---|
| Invalid choice codes, values failing field validation, values outside a hard min/max (or @FORCE-MINMAX) | Error |
| Value outside a soft (non-forced) min/max range | Warning; value imported |
| Duplicate rows for the same record, event and instance | Error |
| Repeat columns that do not match the project's repeating setup | Error |
| Form or record is **locked** | Error — unlock first |
| Completed **e-Consent** response | Error, unless the project allows e-Consent responses to be edited |
| Values for a randomized record's randomization or stratification fields | Error |
| Calculated fields, @CALCDATE and @CALCTEXT fields | Ignored with a warning; REDCap recalculates them |
| File upload fields | Skipped — files cannot be imported by CSV |
| Two-digit years (e.g., `3/15/24`) | Converted to four digits with a warning — check the result |
| Development record limit reached (if your administrators set one) | New records beyond the limit are rejected |
| Project in Analysis/Cleanup status with data locked (read-only) | Imports are blocked |

**Import options on the upload page:**

- **Date format** — "MM/DD/YYYY or YYYY-MM-DD" or "DD/MM/YYYY or YYYY-MM-DD" (defaults from your user profile). YYYY-MM-DD works under either; a date/time value may use a `T` between date and time.
- **Delimiter** — comma, tab or semicolon.
- **Records in rows or columns.**
- **Auto-number or overwrite record IDs?** — with auto-numbering, every row is treated as a new record and REDCap assigns the record IDs.
- **Overwrite data with blank values** — see Section 1.
- **Display the data comparison table?** (real-time mode) — forced on when the project requires a reason for changing data.

**File format:** `.csv`, saved as UTF-8; a byte-order mark (BOM) at the start of the file is handled automatically. There is no fixed row or column limit, but large files are better run as a background import.

---

## 4a. Version Caveats — Silent Data Loss on Import

Several defects caused imports to **report success while dropping data**. There is no error to notice, which makes these worth knowing when reconciling an import that appears complete but is not.

> **Critical — rows with extra columns were silently ignored (below 15.0.17 Standard).** In a CSV import via the Data Import Tool, the API, or `REDCap::saveData()`, any row after the first containing **more columns than the header** was skipped **with no error reported**. Ragged CSVs are a common artefact of Excel exports, so this is not an exotic failure mode. Fixed in 15.0.17, which also fixed rows being silently dropped generally (15.0.16).

> **Critical — background imports dropped data when rows were not grouped by record (below 15.5.10 Standard).** Importing via the background process, whether through the API or the Data Import Tool, could **quietly fail to import some data, with no error**, where rows for the same record were not adjacent in the file.
>
> **Sorting an import file by record ID remains good practice regardless of version** — it costs nothing and removes the entire class of problem.

> **Version caveat — `redcap_repeat_instance = "new"` (15.0.13 and 15.0.17 Standard).** Two separate defects: an unexpected error or a value of `0` saved as the instance number (fixed 15.0.13), and **all repeating instances for a record-instrument failing to import except the last one** (fixed 15.0.17). Both were regressions within the 15.0.x line.

> **Version caveat (below 15.5.9 Standard):** CSV files containing data for **more than one repeating form** failed to import outright.

> **Version caveat (below 15.0.15 Standard):** Imports failed where the file's delimiter did not match the delimiter set in the **importing user's own profile** — a per-user failure mode that explains "it works for me but not for my colleague". A first fix in 15.0.14 did not take; 15.0.15 resolved it.

> **Version caveat (below 16.0.35 Standard):** Importing a **blank value into an already-blank form status field** left the field in an incorrect state, as did importing all-blank values for a fresh non-repeating instrument. Three releases were needed to settle this (16.0.30, 16.0.31, 16.0.35).

> **Version caveat (below 15.5.10 Standard):** Imports in **EAV format** via the Import Records API or `REDCap::saveData()` misbehaved where the payload included a blank `redcap_event_name` column on a **non-longitudinal** project.

---

> **Version caveat (Analysis/Cleanup status — 17.x vs 16.0 LTS):** On 17.x (Standard and LTS), an import cannot create **new** records while the project is in Analysis/Cleanup status. 16.0 LTS has no such block, so a file with mistyped record IDs can add records to a project you considered closed. On 16.0, check the real-time import results for new records before clicking **Import Data**.

> **Version caveat (below 17.4.3 Standard / 17.3.9 LTS):** When a new record was created by import — or by creating a project from a Project XML file — and the **record ID was the only field with data on the first instrument** (no `*_complete` value), that instrument's Form Status was set to `0` **Incomplete** (red) instead of blank (gray). Records imported this way on older versions look as if someone opened and saved the form. Data Quality checks and reports filtering on `[form_complete]=''` will miss them.

## 5. Common Questions

**Q: What columns do I need in my CSV file for a record data import?**

**A:** The minimum required column is the Record ID. If your project is longitudinal, you must also include `redcap_event_name`. If you have repeating instruments or events, add `redcap_repeat_instrument` and `redcap_repeat_instance`. If you are **not** assigned to a Data Access Group and want to place records in DAGs, add `redcap_data_access_group`; if you **are** assigned to a DAG, leave it out (your new records go to your DAG automatically). The Data Import Tool provides a download template with the correct column structure for your specific project — use that template as a starting point rather than building a CSV from scratch.

**Q: Can I import a file exported from REDCap directly back into the same project without any changes?**

**A:** Yes, provided it was exported as **raw** values (not labels). The column structure will be correct, including all required fields and event names; calculated values and survey timestamps in the file are ignored with warnings. If you are assigned to a DAG, delete the `redcap_data_access_group` column first. Every non-blank value in the file replaces what is currently saved, so re-importing an old export rolls those fields back to their old values. This is useful for recovering from accidental deletions, sharing participant data with external analysts (who can make edits and return the file), or migrating records between projects with the same structure.

---

## 6. Common Mistakes

**Assuming "Upload File" in the Data Import Tool saves the data (real-time mode).** In real-time mode the upload step only stages a preview; the data is committed only after you scroll down and click "Import Data" at the bottom of the results screen. If you navigate away after clicking "Upload File," nothing is saved. In **background** mode the opposite holds: there is no preview, and confirming the upload imports the data.

**Assuming a background import is all-or-nothing.** A real-time import with any error saves nothing; a background import saves the records that pass and reports the failed ones. Download the failed records, fix them and re-import only those.

**Including read-only system columns from an export.** REDCap data exports include columns that cannot be written back via the Data Import Tool: `redcap_survey_identifier` and any `*_timestamp` column (e.g., `screening_timestamp`). These are auto-generated by REDCap and ignored on import — the timestamp columns produce a warning rather than an error, and their values cannot be set or overwritten this way. When building an import file from a full export, it is safe to leave these columns in; just be aware their values have no effect.

**Using choice labels instead of raw coded values.** Field values in the import file must be raw-coded (the numeric code, not the label). For example, use `1` not `Yes`, and `2` not `Female`. REDCap will reject or misinterpret label-based values.

**Mismatching the repeat columns and the project's repeating setup.** REDCap reads each row according to how the event and instrument are set up, not according to which columns are blank. For a repeating instrument, fill in both `redcap_repeat_instrument` and `redcap_repeat_instance`. For a repeating event, fill in `redcap_repeat_instance` and leave `redcap_repeat_instrument` empty. Repeat values on a non-repeating event or instrument, a missing instance number on a repeating-event row, or an instrument name on a repeating-event row all produce errors.

**Including `redcap_data_access_group` as a DAG-assigned user.** The column is only for users who are not assigned to a DAG. A DAG user who includes it gets "Illegal use of 'redcap_data_access_group' field!" — delete the column; new records go to your DAG automatically.

---

## 7. API Equivalent

The API equivalent of the Data Import Tool CSV upload is the Import Records endpoint.

| **Feature** | **Export** | **Import** | **Delete** |
|---|---|---|---|
| Record Data | [RC-API-02 — Export Records API](RC-API-02_Export-Records.md) | [RC-API-03 — Import Records API](RC-API-03_Import-Records.md) | [RC-API-04 — Delete Records API](RC-API-04_Delete-Records.md) |

See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) for authentication, token management, and setup.

---

## 8. Related Articles

- [RC-IMP-01 — Data Import Overview](RC-IMP-01_Data-Import-Overview.md) (full workflow and import tool walkthrough)
- [RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap](RC-IMP-03_CSV-Upload-Reference.md) (index of all CSV upload types in REDCap)
- [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md) (arms, events, and unique event name reference)
- [RC-LONG-02 — Repeated Instruments & Events Setup](RC-LONG-02_Repeated-Instruments-and-Events-Setup.md) (repeating instance reference)
- [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) (DAG assignment and the `redcap_data_access_group` column)
- [RC-API-02 — Export Records API](RC-API-02_Export-Records.md)
- [RC-API-03 — Import Records API](RC-API-03_Import-Records.md)
- [RC-API-04 — Delete Records API](RC-API-04_Delete-Records.md)
