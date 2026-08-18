

**Record Data CSV Import — Column Reference and Format Guide**

| **Article ID** | [RC-IMP-04 — Record Data CSV Import — Column Reference and Format Guide](RC-IMP-04_Record-Data-CSV-Import.md) |
|---|---|
| **Domain** | Data Import |
| **Applies To** | All REDCap project types |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.4.1 (Standard) / v17.3.7 (LTS) — changelog review; page not re-captured |
| **Prerequisite** | [RC-IMP-01 — Data Import Overview](RC-IMP-01_Data-Import-Overview.md); [RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap](RC-IMP-03_CSV-Upload-Reference.md)|
| **Skill Level** | Intermediate |
| **Version** | 1.1 |
| **Last Updated** | 2026-05-07 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-IMP-01 — Data Import Overview](RC-IMP-01_Data-Import-Overview.md); [RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap](RC-IMP-03_CSV-Upload-Reference.md); [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md); [RC-LONG-02 — Repeated Instruments & Events Setup](RC-LONG-02_Repeated-Instruments-and-Events-Setup.md); [RC-API-03 — Import Records API](RC-API-03_Import-Records.md) |
| **Synonyms** | how do i import record data from a csv file; upload participant data with the data import tool; bulk import records into redcap; csv column format for importing data; re-import an exported csv back into the project; overwrite existing data with blank values on import; why is my imported data not saving; partial data import for specific fields or events |

---

## 1. Overview

The REDCap Data Import Tool accepts a CSV file containing participant record data. Any REDCap data export in CSV format can be re-imported into the same project as-is. Partial imports — covering specific fields, specific records, or specific events — are also fully supported.

**Location:** Applications → Data Import Tool.

**Upload behavior:** Additive by default — blank cells in the import file are ignored and existing values are preserved. An optional setting ("Overwrite data with blank values") can be enabled to erase existing values with blank cells.

> **Important:** Clicking "Upload File" only stages a preview. The data is not saved until you scroll down and click **Import Data** on the results screen. Navigating away after "Upload File" discards the staged import without saving anything.

For a general overview of the Data Import Tool workflow, see [RC-IMP-01 — Data Import Overview](RC-IMP-01_Data-Import-Overview.md), Sections 8 and 9.

---

## 2. Column Reference

Every record data CSV — whether built from scratch or downloaded from REDCap — uses the same set of column types. The columns below appear in the order REDCap places them in a standard export.

| **Column** | **Required?** | **Notes** |
|---|---|---|
| `record_id` *(or project-specific name)* | Always | First column. The variable name must match the project's Record ID field exactly (e.g., `participant_id`, `patient_id`). |
| `redcap_event_name` | Longitudinal projects | Unique event name in the format `uniqueeventname_arm_N` (e.g., `baseline_arm_1`). Find all values under Project Setup → Define My Events. |
| `redcap_repeat_instrument` | Repeating instruments | The instrument's variable name (lowercase, underscored) for the repeating instrument this row belongs to. Empty for regular event rows and for repeating-event rows. |
| `redcap_repeat_instance` | Repeating instruments or events | Integer instance number starting at 1. When `redcap_repeat_instrument` is empty but this column has a value, REDCap treats the row as a repeating-event instance. Use the value `new` to let REDCap assign the next available instance number automatically. |
| `redcap_survey_identifier` | Never import | Present in exports — holds the survey participant identifier (e.g., name or email used for survey invitations). **Read-only system value. Omit this column or leave it blank on import; the Data Import Tool ignores it.** |
| `redcap_data_access_group` | Conditional | Required only when the uploading user is assigned to one or more DAGs. Omit entirely if the project does not use DAGs. |
| *Instrument fields* (e.g., `screen_age_over_18`) | As needed | Include only the variables you want to set. Omitting a column leaves existing data unchanged (additive behavior). Values must be raw-coded (numbers, dates, text) — not choice labels. |
| `fieldname___N` *(checkbox choices)* | As needed | Checkbox fields produce one column per answer choice. `N` is the raw coded value for that choice (e.g., `demo_race___1`, `demo_race___2`). Values are `1` (checked) or `0` (unchecked). Omitting a checkbox column leaves existing checked state unchanged. |
| `*_timestamp` *(e.g., `demographics_timestamp`)* | Never import | Present in exports — auto-generated timestamp recording when a survey instrument was submitted. **Read-only system value. Omit or leave blank; values in these columns are ignored by the Data Import Tool.** |
| `*_complete` *(e.g., `demographics_complete`)* | Optional | Form completion status. Integer: `0` = Incomplete, `1` = Unverified, `2` = Complete. Import to set or update form status. When omitted, existing status is unchanged. |

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
- **Same repeating instrument at multiple events** — `medication_list` has instances at both `baseline_arm_1` and `3_month_arm_1`. Instance numbers are independent per event — instance 1 at baseline and instance 1 at 3 months are separate records.
- **Most cells are empty in any given row** — a row carries data only for the fields belonging to that event or instrument instance. In a wide project with many instruments, the vast majority of cells will be empty. This is correct and expected — not a sign of file corruption.
- **Complete status columns (`*_complete`) appear at the end of each instrument's field group** — they can be imported alongside data fields or omitted.

---

## 4. Getting the Right Header Row

Two methods reliably produce the correct column layout for your project:

- **Download the Data Import Template** from within the Data Import Tool. The template is header-only (no data rows) and includes the exact column set and coordinate variables your project requires.
- **Export existing data** from Applications → Data Exports, Reports & Stats. The export uses the same header structure and, if records already exist, provides real examples of correctly formatted values.

Building the header row manually is error-prone. Always start from one of these two sources.

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

## 5. Common Questions

**Q: What columns do I need in my CSV file for a record data import?**

**A:** The minimum required column is the Record ID. If your project is longitudinal, you must also include `redcap_event_name`. If you have repeating instruments or events, add `redcap_repeat_instrument` and `redcap_repeat_instance`. If you are assigned to a Data Access Group, add `redcap_data_access_group`. The Data Import Tool provides a download template with the correct column structure for your specific project — use that template as a starting point rather than building a CSV from scratch.

**Q: Can I import a file exported from REDCap directly back into the same project without any changes?**

**A:** Yes. Any CSV file exported from REDCap's data export feature can be re-imported directly into the same project without modification. The column structure will be correct, including all required fields and event names. This is useful for recovering from accidental deletions, sharing participant data with external analysts (who can make edits and return the file), or migrating records between projects with the same structure.

---

## 6. Common Mistakes

**Assuming "Upload File" in the Data Import Tool saves the data.** The upload step only stages a preview. The data is committed only after you scroll down and click "Import Data" at the bottom of the results screen. If you navigate away after clicking "Upload File," nothing is saved.

**Including read-only system columns from an export.** REDCap data exports include columns that cannot be written back via the Data Import Tool: `redcap_survey_identifier` and any `*_timestamp` column (e.g., `screening_timestamp`). These are auto-generated by REDCap and silently ignored on import — they will not cause an error, but their values cannot be set or overwritten this way. When building an import file from a full export, it is safe to leave these columns in; just be aware their values have no effect.

**Using choice labels instead of raw coded values.** Field values in the import file must be raw-coded (the numeric code, not the label). For example, use `1` not `Yes`, and `2` not `Female`. REDCap will reject or misinterpret label-based values.

**Setting `redcap_repeat_instance` without `redcap_repeat_instrument`.** If `redcap_repeat_instrument` is empty but `redcap_repeat_instance` has a value, REDCap treats the row as a repeating-event instance (not a repeating instrument instance). This is the correct behavior for repeating events, but if you intended a repeating instrument, always populate both columns.

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
- [RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap](RC-IMP-03_CSV-Upload-Reference.md)(index of all CSV upload types in REDCap)
- [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md) (arms, events, and unique event name reference)
- [RC-LONG-02 — Repeated Instruments & Events Setup](RC-LONG-02_Repeated-Instruments-and-Events-Setup.md)(repeating instance reference)
- [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) (DAG assignment and the `redcap_data_access_group` column)
- [RC-API-02 — Export Records API](RC-API-02_Export-Records.md)
- [RC-API-03 — Import Records API](RC-API-03_Import-Records.md)
- [RC-API-04 — Delete Records API](RC-API-04_Delete-Records.md)
