**Data Export -- Overview & Workflow**

  -------------------- -------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Article ID**       RC-EXPRT-01
  **Domain**           Exports, Reports & Stats
  **Applies To**       All REDCap project types; requires Data Export user rights
  **Prerequisite**     RC-NAV-UI-01 --- Project Navigation UI
  **Version**          1.0
  **Last Updated**     2025
  **Author**           REDCap Support
  **Related Topics**   RC-EXPRT-02 --- Export Formats; RC-EXPRT-03 --- User Rights & Export Access; RC-EXPRT-04 --- De-identification & Formatting Options; RC-EXPRT-05 --- Report Types
  -------------------- -------------------------------------------------------------------------------------------------------------------------------------------------------------------

**1. Overview**

This article explains how to export data from a REDCap project. It
covers how to navigate to the Data Exports, Reports, and Stats
application and walks through the standard export workflow from start to
finish. It is the entry point for the Exports, Reports & Stats knowledge
base series.

**2. Key Concepts & Definitions**

**Data Exports, Reports, and Stats**

The REDCap application that provides all data export and reporting
functionality. Accessible from the left-hand menu under Applications.
Visibility depends on user rights --- if a user has any export access or
the Add/Edit/Organize Reports right, this application appears in their
menu.

**Export**

The process of downloading project data from REDCap into an external
file. Exports are generated from within the Data Exports, Reports, and
Stats application. REDCap stores a copy of every export in the File
Repository for later re-download.

**Report**

A defined selection of data to export. REDCap provides two built-in
reports (All Data and Selected Instruments/Events) and allows users with
the Add/Edit/Organize Reports right to create custom reports. A report
determines which records and variables are included in an export.

**Export Format**

The file format REDCap uses to deliver the exported data. REDCap
supports seven formats: CSV/Excel (raw data), CSV/Excel (labels), SPSS,
SAS, R, Stata, and CDISC ODM (XML). Format selection affects how data
values are represented and how many files are generated. See RC-EXPRT-02
for full details.

**File Repository**

A project-level storage area where REDCap automatically saves a copy of
every data export. Users can re-download any previous export from the
File Repository without repeating the export process. Access requires
the File Repository user right.

**De-identification Options**

Optional settings applied during export that remove or transform
potentially identifying information. Available options vary based on the
user\'s Data Export Rights level. See RC-EXPRT-04 for full details.

**3. Navigating to the Data Exports, Reports, and Stats Application**

The Data Exports, Reports, and Stats application is accessed from within
a REDCap project. It does not appear if a user has no export rights and
the Add/Edit/Organize Reports right is not granted.

**3.1 From the Left-Hand Menu**

  ------- -----------------------------------------------------------------------------------
  **1**   Log in and open your project from the My Projects page.
  **2**   In the left-hand menu, locate the Applications section.
  **3**   Click Data Exports, Reports, and Stats. The application opens to the report list.
  ------- -----------------------------------------------------------------------------------

  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Note:** If Data Exports, Reports, and Stats does not appear in your menu, your account has no Data Export rights and the Add/Edit/Organize Reports right is not enabled. Contact your project administrator to review your user rights.
  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**4. The Standard Export Workflow**

Every export in REDCap follows the same sequence of steps, regardless of
the report type or export format selected.

  ------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **1**   Navigate to the Data Exports, Reports, and Stats application (see Section 3).
  **2**   Locate the report you want to export --- All Data, Selected Instruments/Events, or a custom report. Click Export Data for that report.
  **3**   Choose an export format from the seven available options. See RC-EXPRT-02 for guidance on which format to choose.
  **4**   Set de-identification options if required or desired. Options available depend on your Data Export Rights level. See RC-EXPRT-04 for full details.
  **5**   Review additional export options and data formatting options. The defaults are appropriate for most exports. See RC-EXPRT-04 for details on each option.
  **6**   Click the Export Data button to generate the export files.
  **7**   Download all generated files. The number of files depends on the export format --- some formats generate multiple files that must all be downloaded. Read the included format-specific instructions carefully.
  **8**   Click the Close button to finish. REDCap saves a copy of this export in the File Repository automatically.
  ------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Tip:** If you need to re-download an export you generated previously, navigate to the File Repository application in the left-hand menu. REDCap stores a copy of every export there. You do not need to run the export again.
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**5. Common Questions**

  ---------------------------------------------------------------------------------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  *Where do I find the Data Exports, Reports, and Stats application?*                            In the left-hand project menu under Applications. If it does not appear, you do not have Data Export rights or the Add/Edit/Organize Reports right. Contact your project administrator.
  *I ran an export this morning and accidentally deleted the file. Do I have to run it again?*   No. Navigate to the File Repository application in the left-hand menu. REDCap automatically saves a copy of every export there. Download it directly without repeating the export process.
  *How many files does REDCap generate when I export?*                                           It depends on the export format. CSV/Excel generates one file. SPSS generates three files. SAS, R, and Stata each generate two files. CDISC ODM generates one XML file. All files for a given format must be downloaded together for the data to load correctly in the target application.
  *Do I have to set de-identification options every time?*                                       No. De-identification options are optional if your export rights allow a Full Data Set export. They are required only if your rights are set to De-identified or Remove All Identifier Fields. See RC-EXPRT-03 and RC-EXPRT-04 for details.
  *Why can\'t I see the Data Exports, Reports, and Stats application in my menu?*                The application only appears if you have at least one of the following: any Data Export right above No Access, or the Add/Edit/Organize Reports right. If neither is granted, the application is hidden entirely.
  *Can I export data from multiple instruments at once?*                                         Yes. Use the Selected Instruments/Events report to choose which instruments to include. For longitudinal projects, you must also select one or more events. See RC-EXPRT-05 for details on report types.
  *What happens if I close the export dialog before downloading my files?*                       The files are still saved in the File Repository. Navigate there to download them at any time.
  ---------------------------------------------------------------------------------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**6. Common Mistakes & Gotchas**

**Not downloading all generated files.** Some export formats (SPSS, SAS,
R, Stata) generate two or three files that must be used together.
Downloading only the data file without the accompanying syntax or label
file will result in an incomplete or unreadable dataset. Always download
every file listed in the export dialog.

**Re-running an export to get a previous snapshot.** Re-running an
export generates a new snapshot of the current data --- it does not
recover the state of the data at the time of the original export. Use
the File Repository to retrieve a previous export file.

**Assuming the application is missing when it is simply hidden.** The
Data Exports, Reports, and Stats application only appears when the user
has appropriate rights. Before reporting it as missing, check your user
rights with the project administrator.

**Closing the export dialog before downloading.** The export dialog
times out or may be dismissed before all files are downloaded. If this
happens, the files are still accessible in the File Repository ---
navigate there to complete the download.

**API Access**

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See RC-API-01 — REDCap API for authentication, token management, and setup.

-   **RC-API-02 — Export Records API** — programmatically retrieve project records in CSV, JSON, or XML
-   **RC-API-38 — Export Reports API** — programmatically export data from a saved custom report by report ID

---


**7. Related Articles**

-   RC-EXPRT-02 --- Data Export: Export Formats (the seven available
    formats and when to use each)

-   RC-EXPRT-03 --- Data Export: User Rights & Export Access (how rights
    affect what you can export)

-   RC-EXPRT-04 --- Data Export: De-identification & Formatting Options

-   RC-EXPRT-05 --- Data Export: Report Types (All Data, Selected
    Instruments, custom reports, other export options)

-   RC-NAV-UI-01 --- Project Navigation UI (prerequisite --- left-hand
    menu and application access)

-   RC-NAV-UI-02 --- Project Menu Reference (Data Exports, Reports, and
    Stats menu item reference)
