---
id: RC-EXPRT-02
title: Data Export — Export Formats
domain: Exports, Reports & Stats
applies_to:
- All REDCap project types
- requires Data Export user rights
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — export
  format behaviour checked against source code; pages not re-captured
prerequisites:
- 'RC-EXPRT-01 — Data Export: Overview & Workflow'
version: '1.1'
last_updated: 2026-11
related:
- id: RC-EXPRT-01
  title: 'Data Export: Overview & Workflow'
- id: RC-EXPRT-03
  title: 'Data Export: User Rights & Export Access'
- id: RC-EXPRT-04
  title: 'Data Export: De-identification & Formatting Options'
tags:
- exports, reports & stats
- data
synonyms:
- what export formats does redcap support
- export to spss sas stata or r
- raw vs labeled data export
- export data as csv excel
- which file format should i pick for export
- why did my export create multiple files
- statistical package export options
- difference between coded and label export values
---

# 1. Overview

This article describes the seven export formats available in REDCap's
Data Exports, Reports, and Stats application. It explains what each
format produces, how many files are generated, and when to use each one.
Selecting the wrong format — or failing to download all generated
files — is one of the most common export mistakes.

---

# 2. Key Concepts & Definitions

**Raw Data**

The coded internal values REDCap stores for structured field types such
as radio buttons, dropdowns, and checkboxes. For example, a Yes/No field
stores '1' for Yes and '0' for No. Raw data exports use these coded
values and variable names as column headers. Raw data exports can be
re-imported into REDCap.

**Labels**

The human-readable display text associated with each option in a
structured field. For example, a checkbox field exports 'Checked' or
'Unchecked' instead of '1' or '0'. The labels export also uses field
labels as column headers and shows event names and repeating instrument
names as labels. Label exports are easier to read but are not suitable
for re-import into REDCap.

**Syntax File**

A companion file generated alongside the data file in statistical
software exports (SPSS, SAS, R, Stata). The syntax file contains
variable labels, value labels, and formatting instructions, and reads
the data file when you run it. Without it, the data file loads as raw
numbers with no context. Both files are always required together.

**CDISC ODM**

Clinical Data Interchange Standards Consortium Operational Data Model
--- a standardized XML format for exchanging data between electronic
data capture (EDC) systems. The CDISC ODM export from REDCap can be
imported into other EDC tools that support the standard, and can also be
re-imported back into REDCap. When chosen as a data export format it
contains the exported data only, not the project's metadata. A full copy
of the project's design and data is the separate whole-project REDCap
XML export — see [RC-EXPRT-05 — Data Export: Report Types & Other Export Options](RC-EXPRT-05_Data-Export-Report-Types-and-Other-Export-Options.md).

---

# 3. Export Format Reference

REDCap offers seven export formats. Select the format that matches your
analysis tool or downstream use case. If exporting for someone else, ask
them which format they prefer before exporting.

| **Format** | **Files** | **File Type(s)** | **Description & Use Case** |
| --- | --- | --- | --- |
| **CSV / Excel (raw data)** | 1 | CSV | Exports coded option values (e.g., 1, 0) for structured fields. Best for programmatic analysis and re-importing data into REDCap. Compatible with any spreadsheet application. |
| **CSV / Excel (labels)** | 1 | CSV | Exports display labels (e.g., 'Checked', 'Yes') instead of raw coded values. Best for human-readable review. Not suitable for re-import. |
| **SPSS Statistical Software** | 3 | SPS + CSV + BAT | An SPSS syntax file (.sps), a data file (.csv with no header row), and an optional Windows helper (Pathway Mapper, .bat) that points the syntax file at the folder holding the data file. Run the .sps in SPSS; it reads the CSV and applies variable and value labels. Eliminates manual value labeling. |
| **SAS Statistical Software** | 2 | CSV + SAS | Exports data with a SAS syntax file for variable labels and formats. Both files required. |
| **R Statistical Software** | 2 | CSV + R | Exports data (CSV with a header row) with an R script for labeling and formatting. Both files required. The script uses the Hmisc package, so install it in R first. R is open-source; data can also be pulled directly via the REDCap API. |
| **Stata Statistical Software** | 2 | DO + CSV | A Stata do-file (.do) and a data file (.csv with no header row). Run the do-file; it reads the CSV and applies variable labels and value labels. Both files required. |
| **CDISC ODM (XML)** | 1 | XML | Standard EDC interchange format. Contains the exported data only, not the project's metadata. Can be imported into other EDC systems. Also functions as a REDCap re-import format. |


> **Important:** For formats that generate multiple files (SPSS, SAS, R, Stata), all files must be downloaded and kept together. Opening only the data file without its companion syntax file will result in raw, unlabeled output — and for SPSS and Stata the data file has no header row, so it will not even show variable names.

**Recognising the downloaded files.** File names include the project
name, a marker for the type of file and a date-time stamp. CSV raw data
files contain `_DATA_`, CSV labels files contain `_DATA_LABELS_`, the
header-less data file used by SPSS and Stata contains
`_DATA_NOHDRS_`, and CDISC ODM files contain `_CDISC_ODM_`. A
whole-project REDCap XML file ends in `.REDCap.xml`.

**Other format details:**

- **Delimiter and encoding.** The **CSV delimiter** choice applies only
  to the two CSV / Excel formats. Data files for SPSS, SAS, R and Stata
  are always comma-delimited so their syntax files can read them. CSV
  files are written as UTF-8 so that special characters display
  correctly when opened in Excel.
- **Leading space on formula-like values.** In CSV exports from the Data
  Exports page, values that begin with `=`, `+`, `-` or `@` get a leading
  space so spreadsheet programs don't treat them as formulas. The Data
  Import Tool removes that space if you re-import the file. Statistical
  package exports and API exports do not add it.
- **Missing data codes.** If the project uses missing data codes, the
  export dialog shows a warning about how those codes are handled in
  the statistical package formats. Read it and check how the codes come
  through before analysing.
- **Very wide exports.** When an export has more than 255 columns, REDCap
  warns that older versions of Excel cannot open all of them. Use a
  current version of Excel, a statistical package, or split the export
  across reports.


---

# 4. Choosing a Format

## 4.1 For general data review or sharing

Use CSV / Excel (labels) for human-readable output. Use CSV / Excel (raw
data) if the recipient needs to do quantitative analysis or re-import
the data into REDCap.

## 4.2 For statistical analysis

Ask your statistician or analyst which software they use and export in
that format. SPSS, SAS, R, and Stata exports include embedded metadata
that eliminates the need to manually map variable labels — a
significant time saving for large projects.

## 4.3 For data transfer between REDCap instances or EDC systems

Use CDISC ODM (XML) to move data between REDCap installations or into
compatible EDC tools. It carries data only, so the receiving project
must already have matching instruments and variables. To copy a whole
project (design and data), use the whole-project REDCap XML export
instead — see [RC-EXPRT-05 — Data Export: Report Types & Other Export Options](RC-EXPRT-05_Data-Export-Report-Types-and-Other-Export-Options.md).
Use CSV / Excel (raw data) if re-importing into REDCap using the Data
Import Tool — see [RC-IMP-01 — Data Import Overview](RC-IMP-01_Data-Import-Overview.md).

## 4.4 For programmatic access

R users can also pull data directly from REDCap using the API, bypassing
the manual export process entirely. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) for details.

---

# 5. Common Questions

| *What is the difference between CSV raw data and CSV labels?* | Raw data exports the coded values stored internally by REDCap (e.g., 1, 0, 2). Labels exports the display text shown to users (e.g., 'Yes', 'No', 'Checked'). Raw data is used for analysis and re-import; labels are easier to read but not suitable for re-import. |
| --- | --- |
| *I downloaded my SPSS export but the data file has no variable labels. What happened?* | SPSS exports generate a syntax file (.sps), a data file (.csv with no header row) and a Pathway Mapper helper (.bat). The CSV on its own has no variable names or labels. Keep the files in the same folder, open the .sps in SPSS and run it — it reads the CSV and applies the variable and value labels. The Pathway Mapper, or editing the file path in the syntax, makes sure SPSS can find the CSV. |
| *Which format should I use if I'm not sure?* | CSV / Excel (raw data) is the most universally compatible format and works in any spreadsheet application. If you're exporting for a statistician, ask them which software they use. |
| *Can I re-import a CSV labels export back into REDCap?* | No. Only CSV / Excel (raw data) and CDISC ODM (XML) can be re-imported into REDCap. The labels format is for human review only. |
| *Does the export format affect which data is included?* | No. The export format controls how values are represented and how many files are generated — it does not filter which records or variables are included. Report type and user rights determine what data is exported. See [RC-EXPRT-03 — Data Export: User Rights & Export Access](RC-EXPRT-03_Data-Export-User-Rights-and-Export-Access.md) and [RC-EXPRT-05 — Data Export: Report Types & Other Export Options](RC-EXPRT-05_Data-Export-Report-Types-and-Other-Export-Options.md). |
| *What is CDISC ODM and when would I use it?* | CDISC ODM is a standard XML format for exchanging data between EDC systems. Use it if you need to transfer data to another EDC tool that supports the CDISC standard, or to re-import data into a REDCap project that already has the same instruments. As a data export format it contains data only, not the project's metadata. For a complete backup of design and data, use the whole-project REDCap XML export described in [RC-EXPRT-05 — Data Export: Report Types & Other Export Options](RC-EXPRT-05_Data-Export-Report-Types-and-Other-Export-Options.md). |
| *Why do some values in my CSV export start with a space?* | Values that begin with `=`, `+`, `-` or `@` get a leading space in CSV exports from the Data Exports page so spreadsheet programs don't treat them as formulas. The Data Import Tool removes the space on re-import. If you process the file in other software, trim it there. |
| *My R script fails when I run it. Why?* | The R syntax file uses the Hmisc package to apply labels. Install the Hmisc package in R before running the script, and keep the CSV in the same folder as the script (or R's working directory). |

---

# 6. Common Mistakes & Gotchas

**Downloading only the data file for multi-file formats.** SPSS, SAS, R,
and Stata exports each require two or three files. Downloading only the
data file produces an unlabeled dataset (for SPSS and Stata, one with no
header row at all). Always download every file
listed in the export dialog and read the accompanying instructions.

**Using CSV labels for re-import.** The CSV labels format is not
compatible with REDCap's Data Import Tool. If you plan to modify data
and re-import it, always use CSV / Excel (raw data).

**Choosing a format without asking the analyst.** Exporting in a format
the recipient cannot use wastes time for everyone. If exporting for a
statistician or analyst, confirm their preferred format before running
the export.

**Assuming all formats produce the same values.** Raw data and labels
exports represent the same underlying data differently. Mixing files
from both formats in an analysis will produce mismatched values.

## API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) for authentication, token management, and setup.

- **[RC-API-02 — Export Records API](RC-API-02_Export-Records.md)** — returns records as CSV, JSON, XML or CDISC ODM via the `format` parameter; `type` chooses flat (one row per record) or EAV output, and `rawOrLabel` / `rawOrLabelHeaders` choose raw values or labels for the data and the column headers. The API does not produce SPSS, SAS, R or Stata syntax files.

---


# 7. Related Articles

- [RC-EXPRT-01 — Data Export: Overview & Workflow](RC-EXPRT-01_Data-Export-Overview-and-Workflow.md) (prerequisite ---
    the standard export process)

- [RC-EXPRT-03 — Data Export: User Rights & Export Access](RC-EXPRT-03_Data-Export-User-Rights-and-Export-Access.md) (how rights
    affect what you can export)

- [RC-EXPRT-04 — Data Export: De-identification & Formatting Options](RC-EXPRT-04_Data-Export-De-identification-and-Formatting-Options.md)

- [RC-EXPRT-05 — Data Export: Report Types & Other Export Options](RC-EXPRT-05_Data-Export-Report-Types-and-Other-Export-Options.md)

- [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) (pulling data directly into R or other tools via
    the REDCap API)

- [RC-API-02 — Export Records API](RC-API-02_Export-Records.md) (export formats available through the API)

- [RC-IMP-01 — Data Import Overview](RC-IMP-01_Data-Import-Overview.md) (re-importing raw data or CDISC ODM files)

- [RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md) (CSV raw data format is also used for
    Data Dictionary uploads)
