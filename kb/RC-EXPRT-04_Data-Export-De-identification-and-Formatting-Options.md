**Data Export -- De-identification & Formatting Options**

  -------------------- -----------------------------------------------------------------------------------------------
  **Article ID**       RC-EXPRT-04
  **Domain**           Exports, Reports & Stats
  **Applies To**       All REDCap project types; availability varies by Data Export Rights level
  **Prerequisite**     RC-EXPRT-01 --- Data Export: Overview & Workflow; RC-EXPRT-03 --- User Rights & Export Access
  **Version**          1.0
  **Last Updated**     2025
  **Author**           REDCap Support
  **Related Topics**   RC-EXPRT-03 --- User Rights & Export Access; RC-EXPRT-02 --- Export Formats
  -------------------- -----------------------------------------------------------------------------------------------

**1. Overview**

This article covers the optional de-identification settings and data
formatting options available in REDCap\'s export dialog.
De-identification options allow you to remove or transform potentially
identifying information before downloading your data. Formatting options
control how values are represented in the exported file. The
availability of these options depends on the user\'s Data Export Rights
level --- see RC-EXPRT-03 for details on rights levels.

**2. Key Concepts & Definitions**

**De-identification**

The process of removing or transforming data elements that could be used
to identify an individual participant. REDCap\'s export
de-identification options target four categories: identifier-flagged
fields, free-form text fields, the Record ID field, and date/datetime
fields.

**Identifier Field**

A variable that has been flagged by the project designer as containing
potentially identifying information. Examples include name, date of
birth, and medical record number. The identifier flag is set in the
Online Designer or via the Check for Identifiers tool in Project Setup.

**Date Shifting**

A de-identification technique that adds a random number of days (between
0 and 364) to all date and datetime fields in a record. The same random
offset is applied consistently within a single record, preserving the
relative time relationships between dates while making the actual dates
less identifiable. The offset differs between records.

**Hash (Record ID Hashing)**

A one-way transformation applied to the Record ID field. Hashing
scrambles the Record ID value in a deterministic but irreversible way.
Two exports hashed with the same algorithm will produce the same hashed
values, allowing records to be linked across exports without revealing
the original identifier. Only relevant when the Record ID contains an
actual identifier such as a medical record number.

**CSV Delimiter**

The character used to separate values in a CSV file. The standard
delimiter is a comma, but some regional configurations (common in
Europe) use a semicolon or tab instead. Mismatched delimiters cause CSV
files to display incorrectly in spreadsheet applications.

**3. De-identification Options**

De-identification options appear in the export dialog under a dedicated
section. Options available to a user depend on their Data Export Rights
level --- users with De-identified rights have these options pre-checked
and locked; users with Full Data Set rights have them optional.

**3.1 Known Identifier Options**

  ---------------------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Option**                         **What it does**
  **Remove all Identifier Fields**   Removes all variables flagged as identifiers from the export. This is the simplest and most reliable way to de-identify an export, provided the project designer has correctly flagged all sensitive fields.
  **Hash the Record ID Field**       Replaces the Record ID with a hashed (scrambled) value. Use this only if the Record ID itself contains an identifier such as a medical record number, phone number, or social security number. If the Record ID is an auto-assigned integer, hashing is unnecessary.
  ---------------------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**3.2 Free-Form Text Options**

  ------------------------------------ -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Option**                           **What it does**
  **Remove unvalidated Text fields**   Removes all text box fields that have no validation rule applied. Validated text fields (e.g., those with date, number, or email validation) are still included. Use this when unvalidated text fields may contain participant-entered narrative content.
  **Remove Notes/Essay box fields**    Removes all Notes box fields from the export. Notes fields can contain large amounts of free-form text that may include identifying information. This option errs on the side of caution by removing all notes fields regardless of content.
  ------------------------------------ -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**3.3 Date and Datetime Options**

For date de-identification, only one of the two options can be selected.

  ----------------------------------------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Option**                                            **What it does**
  **Remove all date and datetime fields**               Removes all variables with a date or datetime validation from the export entirely. This is the most aggressive date de-identification option.
  **Shift all dates by value between 0 and 364 days**   Adds a random offset (0--364 days) to all date and datetime values in the export. The same offset is applied to all dates within a single record, preserving relative date relationships. Different records receive different offsets. Use when date values have research utility but exact dates are a privacy concern.
  ----------------------------------------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Important:** Date shifting preserves relative time relationships within a record (e.g., days between enrollment and first visit) but makes absolute dates less identifiable. It does not prevent re-identification if the shifted dates are combined with other identifying information.
  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**4. Advanced Data Formatting Options**

These options control how the exported data is structured and formatted.
They appear below the de-identification section in the export dialog.
The defaults are appropriate for most exports.

  -------------------------------------------------------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Option**                                               **What it does**
  **Export blank values for gray Form Status?**            Controls whether an instrument with no data saved (gray dot / status 0) exports as \'0\' or as a blank value. The default exports \'0\'. Change this only if you are using the export as a re-import file and need blank to mean \'no data\' rather than \'incomplete\'.
  **Set CSV delimiter character**                          Changes the character used to separate values in CSV exports. The default is a comma. If your analysis software or regional settings expect a semicolon or tab delimiter, set this accordingly. Mismatched delimiters cause CSV files to open as a single column in spreadsheet applications.
  **Force all numbers into a specified decimal format?**   Standardizes the decimal separator used in numeric values. Use this when your analysis software or regional settings expect a period (.) or comma (,) as the decimal character. Mismatched decimal formats cause numeric fields to be read as text in some applications.
  -------------------------------------------------------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**4.1 Additional Options (Feature-Dependent)**

When certain project features are enabled, additional options appear in
the export dialog automatically. For example, if one or more Data Access
Groups are configured in the project, an option appears to export an
additional variable containing each record\'s DAG assignment. These
options are contextual and only appear when relevant.

**5. Common Questions**

  ------------------------------------------------------------------------------------------ ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  *My de-identification options are grayed out and pre-checked. Why can\'t I change them?*   Your Data Export Rights level for one or more instruments is set to De-identified or Remove All Identifier Fields. At these levels, certain de-identification options are mandatory and cannot be unchecked. Contact your project administrator if you need a higher access level.
  *Should I use date shifting or remove all dates?*                                          Use date shifting when date values have research utility and you want to preserve relative time relationships between events. Use remove all dates when the analysis does not require date values at all and you want the simplest approach to de-identification.
  *When should I use the Hash Record ID option?*                                             Only when the Record ID field contains an actual identifier, such as a medical record number, phone number, or social security number. If the Record ID is an auto-assigned integer (the REDCap default), there is no reason to hash it.
  *My exported CSV opens as a single column in Excel. What is wrong?*                        The CSV delimiter does not match what Excel expects for your regional settings. Open the export dialog and change the delimiter to match your system --- typically a semicolon for European regional settings. Alternatively, use Excel\'s Text Import Wizard to specify the delimiter manually.
  *Does removing unvalidated text fields also remove validated text fields?*                 No. The Remove unvalidated Text fields option only removes text boxes that have no validation rule applied. Text boxes with date, number, email, or other validation are still included in the export.
  *What does the gray Form Status export option actually affect?*                            It only affects instruments with no data saved (gray dot). Changing this from \'0\' to blank is only relevant if you are using the export as a data import file and your import logic distinguishes between \'incomplete\' (0) and \'no data entered\' (blank). For most analysis purposes, the default is fine.
  ------------------------------------------------------------------------------------------ ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**6. Common Mistakes & Gotchas**

**Hashing the Record ID when it is an auto-assigned integer.** Record ID
hashing is only meaningful when the Record ID contains a real
identifier. Hashing an auto-assigned integer (1, 2, 3\...) provides no
privacy benefit and may complicate downstream data linkage.

**Assuming de-identification is complete when identifier flagging is
incomplete.** De-identification options act on fields flagged as
identifiers. If the project designer did not flag all sensitive
variables during project design, those variables will still appear in
de-identified exports. Verify the project\'s identifier flags before
relying on export de-identification as a privacy safeguard.

**Selecting both date de-identification options.** REDCap only allows
one date de-identification option --- remove all dates or shift all
dates. Selecting both is not possible; choosing one disables the other.

**Ignoring the delimiter setting when exporting for international
collaborators.** Regional CSV delimiter differences are a common source
of data formatting problems. When sharing exports internationally,
confirm the expected delimiter with the recipient before exporting.

**7. Related Articles**

-   RC-EXPRT-01 --- Data Export: Overview & Workflow (the full export
    process)

-   RC-EXPRT-03 --- Data Export: User Rights & Export Access (how rights
    levels affect which de-identification options are mandatory)

-   RC-EXPRT-02 --- Data Export: Export Formats (format selection
    affects how values are represented)

-   RC-FD-01 --- Form Design Overview (Check for Identifiers --- where
    identifier flags are set)
