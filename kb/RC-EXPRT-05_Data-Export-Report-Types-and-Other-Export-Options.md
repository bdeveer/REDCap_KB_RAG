**Data Export -- Report Types & Other Export Options**

  -------------------- ------------------------------------------------------------------------------------------------------------------------------------------
  **Article ID**       RC-EXPRT-05
  **Domain**           Exports, Reports & Stats
  **Applies To**       All REDCap project types; requires Data Export user rights
  **Prerequisite**     RC-EXPRT-01 --- Data Export: Overview & Workflow
  **Version**          1.0
  **Last Updated**     2025
  **Author**           REDCap Support
  **Related Topics**   RC-EXPRT-01 --- Overview & Workflow; RC-EXPRT-03 --- User Rights & Export Access; RC-EXPRT-04 --- De-identification & Formatting Options
  -------------------- ------------------------------------------------------------------------------------------------------------------------------------------

**1. Overview**

This article describes the types of reports available in REDCap\'s Data
Exports, Reports, and Stats application --- what each one exports and
when to use it --- as well as the additional bulk export options
available under the Other Export Options tab. Report type determines
which records and variables are included in an export. Export format and
de-identification options are applied after the report is selected.

**2. Key Concepts & Definitions**

**Report**

A defined selection of records and variables to export. REDCap provides
two built-in reports (All Data and Selected Instruments/Events) that are
always present. Any number of custom reports can be created by users
with the Add/Edit/Organize Reports right and are listed below the
built-in reports.

**All Data Report**

The built-in report that exports every record and every variable in the
project at the time of export. It is always the first report listed and
requires no configuration.

**Selected Instruments/Events Report**

The built-in report that allows the user to choose a subset of
instruments to export. In longitudinal projects, one or more events must
also be selected. This report does not filter by record --- it exports
all records for the chosen instruments and events.

**Custom Report**

A user-defined report that can filter by individual variables, apply
logic conditions, restrict visibility to specific users, and organize
results in a custom order. Custom reports require the Add/Edit/Organize
Reports user right to create or edit. Once created, they appear in the
report list and in the left-hand menu for quick access.

**Other Export Options**

A separate tab at the top of the Data Exports, Reports, and Stats page
that provides bulk export options not available through the standard
report workflow --- including full project XML backup, bulk file
download, PDF of all records, and Tableau integration.

**3. Built-in Report Types**

**3.1 All Data**

Exports the complete dataset --- every record, every instrument, every
variable --- at the current point in time. This is the quickest path to
a full project export and requires no configuration beyond selecting an
export format.

-   Use when you need a complete snapshot of all project data.

-   User\'s Data Export Rights still apply --- instruments where the
    user has No Access are excluded.

-   DAG membership still limits which records are included.

**3.2 Selected Instruments and/or Events**

Allows the user to select one or more instruments to include in the
export. All records are included for the selected instruments --- this
report does not filter by record.

-   Use when you need data from specific instruments without exporting
    the entire project.

-   In longitudinal projects, at least one event must also be selected.
    The export includes only the instrument-event combinations that are
    chosen.

-   Useful for sharing data from a single instrument with an external
    collaborator without exposing the full dataset.

**4. Custom Reports**

**4.1 What Custom Reports Can Do**

Custom reports extend beyond the built-in options by allowing
fine-grained control over what is included in an export.

  ------------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Capability**                  **Description**
  **Variable selection**          Choose individual variables to include rather than entire instruments.
  **Record filtering by logic**   Apply a REDCap logic expression to include only records that meet specific criteria (e.g., only consented participants, only records with a specific diagnosis).
  **User visibility control**     Restrict the report so it only appears for specific users or user roles.
  **Left-menu shortcut**          Custom reports automatically appear in the left-hand menu for quick access, in addition to the report list.
  **Folder organization**         Reports can be organized into named folders in the left-hand menu. Use folders when a project has accumulated many reports to keep navigation manageable.
  ------------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------

**4.2 Creating and Editing Custom Reports**

Creating and editing custom reports requires the Add/Edit/Organize
Reports user right. This right is independent of Data Export Rights. A
user can have the ability to create reports without being able to export
the resulting data, and vice versa. See RC-EXPRT-03 for details on
rights levels.

  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Note:** Detailed guidance on creating and configuring custom reports is covered in a separate training. This article covers report types from an export perspective only.
  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**5. Other Export Options**

The Other Export Options tab at the top of the Data Exports, Reports,
and Stats page provides bulk export options that operate at the project
level rather than at the report level. These options are infrequently
used but serve specific purposes.

  ---------------------------------------------------------------------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Option**                                                             **What it does & when to use it**
  **Export entire project as REDCap XML**                                Exports the complete project --- instrument definitions, data, and configuration --- as a single XML file. This is the most comprehensive backup option available. The resulting file can be used to recreate the entire project in a new REDCap instance. More complete than a Data Dictionary download, which only captures instrument structure.
  **ZIP file of uploaded files (all records)**                           Downloads all files uploaded through File Upload field types across all records as a single ZIP archive. Standard data exports do not include uploaded files. Use this when you need to bulk-download participant-uploaded documents, images, or other files. May take significant time to generate on large projects.
  **PDF of data collection instruments with saved data (all records)**   Generates a single PDF containing every record\'s data across all instruments, formatted as filled-in forms. Useful for audits, regulatory submissions, or human-readable archives. File size and generation time can be substantial for large projects. A PDF of a single record can also be downloaded from within the record itself.
  **Tableau Export**                                                     Connects REDCap directly to Tableau for data visualization. Requires Tableau and uses the REDCap API. Considered an advanced feature --- consult your REDCap support team before using.
  ---------------------------------------------------------------------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Note:** Standard data exports (CSV, SPSS, R, etc.) do not include files uploaded through File Upload fields. If your project uses file upload fields and you need those files, use the ZIP file of uploaded files option under Other Export Options.
  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**6. Common Questions**

  ------------------------------------------------------------------------------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  *What is the difference between All Data and Selected Instruments?*                         All Data exports every instrument and every variable in the project for all records. Selected Instruments lets you choose specific instruments to include --- useful when you only need a subset of the data. Both include all records you have access to.
  *I need to export data from only consented participants. Which report type should I use?*   A custom report with a logic filter applied (e.g., \[consent\_status\]=\'1\'). The built-in All Data and Selected Instruments reports do not filter by record. You need the Add/Edit/Organize Reports right to create a custom report.
  *Can I export uploaded files (PDFs, images) through a standard data export?*                No. Standard exports (CSV, SPSS, etc.) do not include files uploaded through File Upload fields. Use the ZIP file of uploaded files option under Other Export Options to bulk-download all uploaded files.
  *What is the REDCap XML export and how is it different from a Data Dictionary download?*    The REDCap XML export includes the full project --- instrument structure, data, and configuration settings. A Data Dictionary download includes only the instrument and variable definitions. Use the XML export for a complete project backup; use the Data Dictionary for instrument structure only.
  *My project has many custom reports and the left menu is cluttered. What can I do?*         Organize reports into folders. Folders are created by naming them consistently and grouping reports under each name. Users with the Add/Edit/Organize Reports right can manage folder organization. This is covered in the custom reports training.
  *Does a custom report export all records or only filtered ones?*                            Only filtered ones, if a logic filter is applied. If no filter is set, the custom report exports all records you have access to for the selected variables.
  ------------------------------------------------------------------------------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**7. Common Mistakes & Gotchas**

**Using All Data when only a subset is needed.** Exporting the full
dataset when only one instrument\'s data is required shares more data
than necessary and produces larger files. Use Selected Instruments or a
custom report to limit the export scope.

**Expecting standard exports to include uploaded files.** Files attached
via File Upload fields are not included in CSV, SPSS, or other standard
exports. Use the ZIP file of uploaded files option under Other Export
Options if you need those files.

**Accumulating too many unorganized custom reports.** Projects with many
custom reports can have cluttered left-hand menus and report lists.
Organize reports into folders and remove reports that are no longer
needed. This requires the Add/Edit/Organize Reports right.

**Confusing the REDCap XML export with a Data Dictionary download.** The
Data Dictionary (CSV) captures instrument and variable structure only.
The REDCap XML export captures the full project including data. Use the
XML export for complete backups; use the Data Dictionary for instrument
structure management.

**API Access**

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See RC-API-01 — REDCap API for authentication, token management, and setup.

-   **RC-API-38 — Export Reports API** — export a saved report programmatically by its numeric report ID

---


**8. Related Articles**

-   RC-EXPRT-01 --- Data Export: Overview & Workflow (prerequisite ---
    the full export process)

-   RC-EXPRT-02 --- Data Export: Export Formats (format selection after
    report type is chosen)

-   RC-EXPRT-03 --- Data Export: User Rights & Export Access (rights
    required for custom reports and export access)

-   RC-EXPRT-04 --- Data Export: De-identification & Formatting Options

-   RC-FD-03 --- Data Dictionary (the Data Dictionary download vs.
    REDCap XML backup)
