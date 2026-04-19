RC-EXPRT-02

**Data Export — Export Formats**

| **Article ID** | RC-EXPRT-02 |
| --- | --- |
| **Domain** | Exports, Reports & Stats |
| **Applies To** | All REDCap project types; requires Data Export user rights |
| **Prerequisite** | RC-EXPRT-01 — Data Export: Overview & Workflow |
| **Version** | 1.0 |
| **Last Updated** | 2025 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-EXPRT-01 — Overview & Workflow; RC-EXPRT-03 — User Rights & Export Access; RC-EXPRT-04 — De-identification & Formatting Options |

# 1. Overview

This article describes the seven export formats available in REDCap\'s
Data Exports, Reports, and Stats application. It explains what each
format produces, how many files are generated, and when to use each one.
Selecting the wrong format — or failing to download all generated
files — is one of the most common export mistakes.

# 2. Key Concepts & Definitions

**Raw Data**

The coded internal values REDCap stores for structured field types such
as radio buttons, dropdowns, and checkboxes. For example, a Yes/No field
stores \'1\' for Yes and \'0\' for No. Raw data exports use these coded
values. Raw data exports can be re-imported into REDCap.

**Labels**

The human-readable display text associated with each option in a
structured field. For example, a checkbox field exports \'Checked\' or
\'Unchecked\' instead of \'1\' or \'0\'. Label exports are easier to
read but are not suitable for re-import into REDCap.

**Syntax File**

A companion file generated alongside the data file in statistical
software exports (SPSS, SAS, R, Stata). The syntax file contains
variable labels, value labels, and formatting instructions. Without it,
the data file loads as raw numbers with no context. Both files are
always required together.

**CDISC ODM**

Clinical Data Interchange Standards Consortium Operational Data Model
--- a standardized XML format for exchanging data between electronic
data capture (EDC) systems. The CDISC ODM export from REDCap can be
imported into other EDC tools that support the standard, and can also be
re-imported back into REDCap.

# 3. Export Format Reference

REDCap offers seven export formats. Select the format that matches your
analysis tool or downstream use case. If exporting for someone else, ask
them which format they prefer before exporting.

  -------------------------------- ----------- ------------------ --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Format**                       **Files**   **File Type(s)**   **Description & Use Case**
  **CSV / Excel (raw data)**       1           CSV                Exports coded option values (e.g., 1, 0) for structured fields. Best for programmatic analysis and re-importing data into REDCap. Compatible with any spreadsheet application.
  **CSV / Excel (labels)**         1           CSV                Exports display labels (e.g., \'Checked\', \'Yes\') instead of raw coded values. Best for human-readable review. Not suitable for re-import.
  **SPSS Statistical Software**    3           SAV + SPS + TXT    Exports data with embedded variable metadata. All three files required to load data in SPSS. Eliminates manual value labeling.
  **SAS Statistical Software**     2           CSV + SAS          Exports data with a SAS syntax file for variable labels and formats. Both files required.
  **R Statistical Software**       2           CSV + R            Exports data with an R script for labeling and formatting. Both files required. R is open-source; data can also be pulled directly via the REDCap API.
  **Stata Statistical Software**   2           DTA + DO           Exports data with a Stata do-file for variable metadata. Both files required.
  **CDISC ODM (XML)**              1           XML                Standard EDC interchange format. Can be imported into other EDC systems. Also functions as a REDCap re-import format.
  -------------------------------- ----------- ------------------ --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Important:** For formats that generate multiple files (SPSS, SAS, R, Stata), all files must be downloaded and kept together. Opening only the data file without its companion syntax file will result in raw, unlabeled output.
  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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
compatible EDC tools. Use CSV / Excel (raw data) if re-importing into
REDCap using the Data Import Tool.

## 4.4 For programmatic access

R users can also pull data directly from REDCap using the API, bypassing
the manual export process entirely. See RC-API-01 for details.

# 5. Common Questions

  ---------------------------------------------------------------------------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  *What is the difference between CSV raw data and CSV labels?*                            Raw data exports the coded values stored internally by REDCap (e.g., 1, 0, 2). Labels exports the display text shown to users (e.g., \'Yes\', \'No\', \'Checked\'). Raw data is used for analysis and re-import; labels are easier to read but not suitable for re-import.
  *I downloaded my SPSS export but the data file has no variable labels. What happened?*   SPSS exports generate three files — the data file (.sav), a syntax file (.sps), and an instructions file (.txt). You must run the syntax file against the data file in SPSS to apply the variable labels. Download all three files and follow the included instructions.
  *Which format should I use if I\'m not sure?*                                            CSV / Excel (raw data) is the most universally compatible format and works in any spreadsheet application. If you\'re exporting for a statistician, ask them which software they use.
  *Can I re-import a CSV labels export back into REDCap?*                                  No. Only CSV / Excel (raw data) and CDISC ODM (XML) can be re-imported into REDCap. The labels format is for human review only.
  *Does the export format affect which data is included?*                                  No. The export format controls how values are represented and how many files are generated — it does not filter which records or variables are included. Report type and user rights determine what data is exported. See RC-EXPRT-03 and RC-EXPRT-05.
  *What is CDISC ODM and when would I use it?*                                             CDISC ODM is a standard XML format for exchanging data between EDC systems. Use it if you need to transfer data to another EDC tool that supports the CDISC standard, or if you want a complete backup that can be re-imported into REDCap along with its metadata.
  ---------------------------------------------------------------------------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 6. Common Mistakes & Gotchas

**Downloading only the data file for multi-file formats.** SPSS, SAS, R,
and Stata exports each require two or three files. Downloading only the
data file produces an unlabeled dataset. Always download every file
listed in the export dialog and read the accompanying instructions.

**Using CSV labels for re-import.** The CSV labels format is not
compatible with REDCap\'s Data Import Tool. If you plan to modify data
and re-import it, always use CSV / Excel (raw data).

**Choosing a format without asking the analyst.** Exporting in a format
the recipient cannot use wastes time for everyone. If exporting for a
statistician or analyst, confirm their preferred format before running
the export.

**Assuming all formats produce the same values.** Raw data and labels
exports represent the same underlying data differently. Mixing files
from both formats in an analysis will produce mismatched values.

## API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See RC-API-01 — REDCap API for authentication, token management, and setup.

- **RC-API-02 — Export Records API** — supports the same format options (CSV, JSON, XML, SPSS labels) via the `type` and `rawOrLabel` parameters

---


# 7. Related Articles

- RC-EXPRT-01 — Data Export: Overview & Workflow (prerequisite ---
    the standard export process)

- RC-EXPRT-03 — Data Export: User Rights & Export Access (how rights
    affect what you can export)

- RC-EXPRT-04 — Data Export: De-identification & Formatting Options

- RC-EXPRT-05 — Data Export: Report Types

- RC-API-01 — API (pulling data directly into R or other tools via
    the REDCap API)

- RC-FD-03 — Data Dictionary (CSV raw data format is also used for
    Data Dictionary uploads)
