RC-FD-06

**Online Designer – Instrument and Field Management**

| **Article ID** | RC-FD-06 |
| --- | --- |
| **Domain** | Form Design |
| **Applies To** | All REDCap project types; requires Project Design and Setup user rights |
| **Prerequisite** | RC-NAV-UI-01 — Project Navigation UI; RC-FD-01 — Form Design Overview; RC-FD-02 — Online Designer |
| **Version** | 1.2 |
| **Last Updated** | 2026-04-11 |
| **Author** | REDCap Support |
| **Related Topics** | RC-FD-02 — Online Designer; RC-FD-03 — Data Dictionary; RC-BL-01 — Branching Logic Overview and Scope |

---

# 1. Overview

## What is this?

This article walks through how to use the Online Designer to build and modify instruments and fields in a REDCap project. It covers the interface layout, instrument-level actions (creating, renaming, copying, deleting, and reordering instruments), field-level actions (adding, editing, moving, and deleting fields), all available field types, the Drag-N-Drop Logic Builder, and matrix field configuration.

## Why does it matter?

The instrument and field structure you create in the Online Designer defines how data is collected in your project. Getting it right before data collection starts prevents problems like orphaned records, invalid branching logic, and variables that are hard to use in analysis. This article gives users the vocabulary and procedural knowledge to build instruments confidently.

## Scope and Assumptions

This article assumes:
- The user is logged into a REDCap instance and has navigated to an existing project.
- The project has surveys, longitudinal mode, and Data Access Groups (DAGs) disabled. Some features and buttons described here may look different or have additional options in projects with those features enabled.
- The user has at minimum the **Project Design and Setup** right assigned in their user profile.

---

# 2. Key Terminology

- **Instrument**: A data collection form in REDCap. A project can have one or many instruments. Also referred to as a "form" in some contexts.
- **Field / Variable**: A single data entry element within an instrument. Every field has a variable name used to identify it in the database, code book, and exports.
- **Variable Name**: The internal identifier for a field. Must be unique across the entire project. REDCap enforces uniqueness and character restrictions automatically.
- **Field Label**: The text displayed to the person entering data, typically phrased as a question or instruction. Can include images, video, and HTML.
- **Branching Logic**: A conditional rule that hides or shows a field depending on values entered in other fields.
- **Matrix**: A group of fields displayed in a grid with shared column headers (answer choices) and individual row labels (field labels).
- **Record ID**: The mandatory first field in the first instrument of every REDCap project. It uniquely identifies each data record.
- **CDE (Common Data Element)**: A standardized, precisely defined field used to collect and share data consistently across studies, systems, or organizations. CDEs ensure that everyone uses the same definitions, formats, and coding for a given piece of information. Using CDEs is particularly important for multi-site studies and grant-funded research that require data harmonization.
- **CDE Library** (formerly **Field Bank**): REDCap's built-in catalog browser for searching and importing CDEs from external repositories (e.g., the NIH CDE Repository). Accessible directly from the instrument editor.

---

# 3. Learning Objectives

After completing this module, the user will be able to:

- Navigate to the Online Designer and identify the key buttons and interface elements.
- Create, rename, copy, delete, move, and open instruments in a project.
- Add, edit, move, copy, and delete individual fields within an instrument.
- Configure all standard REDCap field types and their associated options.
- Apply branching logic to a field using the Drag-N-Drop Logic Builder.
- Create and configure a matrix of fields, including rows, column options, and answer format.

---

# 4. Online Designer Interface

When you open the Online Designer, you see a list of all instruments currently defined in the project, along with a toolbar of action buttons. The buttons available depend on which features are enabled in your project.

## 4.1 Toolbar Buttons

| Button | Description |
| --- | --- |
| **Create Snapshot of Instruments** | Backs up a data dictionary of your current instrument setup. Useful before making significant structural changes. See RC-FD-03 for more on the Data Dictionary. |
| **+ Create** | Opens the instrument creation flow, allowing you to add a new blank instrument to your project. |
| **Import** | Imports a validated instrument from the REDCap Shared Library. See RC-FD-04 for details. |
| **Upload** | Imports a local zip file to create a new instrument. See RC-FD-04 for details. |
| **Form Display Logic** | An advanced feature that controls when certain instruments appear for a record. Requires knowledge of branching logic syntax (see RC-BL-01). |

## 4.2 Instrument List Columns

| Column | Description |
| --- | --- |
| **Instrument Name** | The display name of the instrument. Click the name to open and edit the instrument. |
| **Fields** | The count of variables currently defined in that instrument. |
| **View PDF** | Generates a blank PDF preview of the current version of the instrument. |
| **Instrument Actions** | A dropdown menu for instrument-level operations (rename, copy, delete, download zip). |

---

# 5. Instrument Management

## 5.1 Creating an Instrument

| 1 | Click the **+ Create** button in the Online Designer toolbar. |
| --- | --- |
| 2 | Click **Add instrument here** at the position in the list where you want the new instrument to appear. |
| 3 | Type a name for your instrument in the text box that appears. |
| 4 | Click the **Create** button next to the instrument name field. |

The new instrument appears in the instrument list and is ready to receive fields.

## 5.2 Renaming an Instrument

Open the **Instrument Actions** dropdown next to the instrument and select **Rename**. Type the new name and confirm.

**Best practice:** Keep instrument names unique within the project. REDCap allows two instruments to share a display name, but will internally assign a unique system name for use in the code book and data dictionary — this can cause confusion. Avoid duplicate display names.

## 5.3 Copying an Instrument

Open the **Instrument Actions** dropdown and select **Copy**. REDCap will prompt you to:
- Provide a new **display name** for the cloned instrument.
- Define a **suffix** to append to all field variable names in the cloned instrument.

The suffix requirement exists because every variable name must be unique across the entire project. All fields in the original instrument will have the suffix appended to their variable names in the copy.

## 5.4 Deleting an Instrument

Open the **Instrument Actions** dropdown and select **Delete**.

> **Warning:** Deleting an instrument permanently deletes the instrument itself and all data collected for any records in that instrument. This action cannot be undone. Exercise extreme caution when the project is in Production mode or contains real participant data.

## 5.5 Downloading an Instrument as a Zip File

Open the **Instrument Actions** dropdown and select **Download instrument zip**. This exports the instrument definition as a zip file that can be imported into another REDCap project. See RC-FD-04 for details on instrument zip files.

## 5.6 Reordering Instruments

Drag and drop instruments in the list to change their order. The new order is saved automatically. The order of instruments affects how they appear in the Record Home Page and other navigation views.

## 5.7 Opening an Instrument

Click the instrument's **name** (displayed as a link in the list) to enter the instrument editor and view or modify its fields.

---

# 6. Individual Instrument Design

When you open an instrument, REDCap displays an expanded view of all fields in that instrument, along with controls to add, edit, move, copy, and delete fields.

## 6.1 The Record ID Field

Every REDCap project is created with one instrument that contains exactly one field: the **Record ID** field. The Record ID is always the first field in the first instrument. REDCap enforces this rule strictly — it requires this field to store records in the database.

You may edit limited aspects of the Record ID field (such as its label), but:
- Do not rename or restructure the Record ID field after real data has been collected. Doing so can result in **orphaned records** — records that remain in the backend database but no longer appear in the project interface.
- The Record ID field cannot be moved to a different instrument.

## 6.2 Field Creation Buttons

Throughout the instrument editor, you will see a cluster of buttons between fields. These allow you to insert new content at that position:

| Button | Description |
| --- | --- |
| **Add Field** | Opens the field editor for creating a new standard field from scratch at this position. |
| **Add Matrix of Fields** | Opens the matrix editor to create a group of fields in a grid layout. See Section 10. |
| **Add CDE Field** | Opens the CDE Library — a searchable catalog of Common Data Elements from external repositories. Select a catalog (the default is the NIH CDE Repository), enter a keyword, review the results, and click **Add Field** next to any result to import that standardized field into your instrument. See Section 6.4 for details. |

> **Naming note:** The CDE Library button was previously labeled **Import from Field Bank**. You may see "Field Bank" referenced in older documentation or training materials — it refers to the same feature.

## 6.3 Field-Level Actions

Each field in the instrument editor has the following controls:

| Action | Description |
| --- | --- |
| **Edit** (pencil icon) | Opens the field editor for that field. See Section 7. |
| **Copy** | Duplicates the field. REDCap automatically assigns a new unique variable name to the copy. All other field settings are preserved. |
| **Move** | Opens a dialog to move the field to a specific position within the instrument, or to a different instrument in the project entirely. |
| **Drag handle** | Drag and drop the field to reorder it within the instrument. Note: drag-and-drop cannot move a field to a different instrument — use the Move button for that. |
| **Delete** (trash icon) | Permanently deletes the field and all data collected in records for that field. Use with caution when real data exists. |
| **Branching Logic** (fork icon) | Opens the branching logic editor for this field. See Section 9. |

## 6.4 Using the CDE Library

The CDE Library lets you search external repositories of Common Data Elements and import standardized field definitions directly into your instrument.

**To add a CDE field:**

| 1 | Click the **Add CDE Field** button at the position in the instrument where you want to insert the field. |
| --- | --- |
| 2 | Select a **catalog** from the dropdown. The default catalog is the **NIH CDE Repository**. Other catalogs may be available depending on your institution's REDCap configuration. |
| 3 | Enter a keyword in the search box (e.g., "pain intensity", "race", "smoking status") and run the search. |
| 4 | Review the results. Each result shows the CDE's name, source, and field type. |
| 5 | Click **Add Field** next to the CDE you want to import. The field is inserted into your instrument with its standardized label, variable name, choices, and validation pre-configured. |

**Why use CDEs?**
- Ensures your data uses the same definitions and coding as other studies, enabling data sharing and comparison.
- Required or recommended by many NIH funding programs and regulatory frameworks.
- Saves time — the field definition is already built and validated.

**What happens after import?**
The imported field appears in your instrument like any other field. You can edit the field label, add branching logic, or adjust other settings after import. However, changing the coding (raw values) of an imported CDE defeats the purpose of standardization — avoid changing codes unless absolutely necessary and document any deviations.

## 6.5 Field Preview

After creating or editing a field, REDCap displays a preview of it within the instrument editor. The preview shows the field label, variable name, answer choices (if applicable), whether the field is required, and any branching logic attached to it.

## 6.6 Preview Instrument

The **Preview Instrument** button (available in the instrument editor toolbar) collapses the exploded design view into a rendering that more closely resembles the final data entry form. Note that branching logic is not active in this preview — it only reflects the form layout. To test branching logic in context, create a test record and complete data entry.

---

# 7. Edit Field Menu

Clicking **Add Field** or the edit (pencil) icon on an existing field opens the field editor. The options available depend on the selected field type.

## 7.1 Field Type

The first and mandatory choice for any field is its **field type**. The field type determines what kind of data the field can capture and what additional options become available. Field types are described in detail in Section 8.

## 7.2 Field Label

The text displayed to the person entering data. This is typically phrased as a question ("What is the patient's date of birth?") but can also include contextual instructions, images, video embeds, audio files, and downloadable documents. HTML is supported when the rich text editor is enabled (see below). The field label may be left blank, though this is generally not recommended.

## 7.3 Choices

For field types that present a list of options (dropdown, radio buttons, checkboxes), you must define the available choices. Each choice is entered on its own line in the format:

```
raw_value, Label
```

The raw value is the value stored in the database (typically a number, but text is allowed). The raw value must be unique within the field. REDCap uses the raw value in exports, branching logic, and API responses; the label is what the data entry person sees.

**Example:**
```
1, Yes
2, No
99, Unknown
```

At least one choice must be defined before the field can be saved.

## 7.4 Variable Name

The internal identifier for the field. Variable names:
- Must be unique across the entire project (not just within the instrument).
- Are limited to lowercase letters, numbers, and underscores; no spaces or special characters.
- REDCap enforces these rules automatically and will alert you if a name is invalid or already in use.

**Best practice:** Keep variable names short but human-readable. For example, use `dob` rather than `date_of_birth`. Variable names are permanent identifiers used in exports, branching logic syntax, and API calls — changing them after data collection has started can break downstream references.

## 7.5 Required

Determines whether the field must be completed before a data entry form can be saved. The default is **No**. When set to **Yes**, the field is marked with a red asterisk in the data entry form, and REDCap will prompt the user if they attempt to save without completing it.

## 7.6 Identifier

Marks the field as containing personally identifiable information (PII). The default is **No**. Setting this to **Yes** does not change the data entry experience, but it enables REDCap to automatically de-identify exports when the de-identification option is selected during data export. Mark fields containing names, dates of birth, addresses, phone numbers, and similar data as identifiers.

## 7.7 Custom Alignment

Controls how the field (particularly its answer choices) is displayed on screen. Different field types respond differently to alignment options. The available choices are typically Left Horizontal, Right Horizontal, Left Vertical, and Right Vertical. This is primarily a cosmetic preference — experiment to find what works best for your instrument. **Best practice:** Apply alignment choices consistently across all instruments in the project.

## 7.8 Field Note

An optional short note displayed below the field in the data entry form. Use this to provide context or instructions that are too specific to include in the field label. Common examples:
- "Check all that apply" (for checkbox fields)
- "Enter in millimeters" (for a numeric text box)
- "Leave blank if not applicable"

## 7.9 Action Tags / Field Annotation

Action tags are special codes entered in the annotation box that modify field behavior in specific, pre-defined ways (e.g., hiding a field from the instrument header, auto-populating values, restricting who can edit a field). Action tags are an advanced topic outside the scope of this article. See the RC-AT series for details.

## 7.10 Rich Text Editor

A checkbox in the upper-right corner of the field label area enables the **Rich Text Editor** — a toolbar similar to a word processor that allows you to apply bold, italic, underline, font size, color, lists, and other formatting to the field label. It also exposes an HTML editor mode for users comfortable embedding raw HTML. Enabling the rich text editor is useful for formatting complex instructions or embedding media.

## 7.11 Save and Cancel

- **Save** commits all changes to the field and returns to the instrument editor.
- **Cancel** discards changes and returns to the instrument editor.

---

# 8. Field Types

REDCap provides the following field types. Each type captures or displays data in a different way.

## 8.1 Text Box

A single-line text input. At its most basic, it accepts free text. It supports two enhancements:

**Validation:** REDCap can validate the entered value against a selected format — for example, date formats (MM-DD-YYYY, YYYY-MM-DD, etc.), time, phone number, email address, integer, number, and more. Available validation types depend on your institution's REDCap configuration.

**Min / Max values:** For numeric and date validations, you can set a minimum value, maximum value, or both. By default, these constraints are soft — REDCap displays a warning if the entered value falls outside the range, but the value can still be saved (to accommodate legitimate outliers). To enforce a hard limit that REDCap will not accept, add the action tag **@FORCE-MINMAX** to the field. Example: set a minimum of 0 for a field asking about number of pregnancies to prevent negative values.

**Ontology lookup (if enabled):** If your institution has configured biomedical ontology services, you can attach an ontology (e.g., ICD-10, RxNorm, SNOMED CT) to the text box. The field becomes a search box that looks up valid terms from that ontology. Contact your REDCap administrator to determine whether this feature is available at your institution.

## 8.2 Notes Box

A multi-line text area — essentially the text box's larger counterpart. Does not support validation, min/max, or ontology. Use for free-text fields where respondents may need to write longer narratives, comments, or descriptions. Both text boxes and notes boxes can store up to 65,535 characters.

## 8.3 Dropdown List

Displays a list of choices in a collapsed dropdown menu. The data entry person can select **one option only**. An optional **auto-complete** mode converts the dropdown into a search-as-you-type input, making it practical for long lists (e.g., a full list of countries or ICD codes).

Choices are defined in the `raw_value, Label` format, one per line.

## 8.4 Radio Buttons

Displays all choices directly on screen (not collapsed into a dropdown). The data entry person can select **one option only**. Better suited for short lists where all options should be visible at a glance.

Choices are defined in the `raw_value, Label` format, one per line.

## 8.5 Checkboxes

Displays all choices directly on screen. The data entry person may select **multiple options**. REDCap stores each checkbox option as a separate binary variable in the database (e.g., `symptoms___1`, `symptoms___2`), with 1 meaning checked and 0 meaning unchecked. Because of this storage structure, checkbox data looks different in exports than single-select fields — it is good practice to enter test data and review the export file before collecting real data, to confirm you understand how your data will be structured.

Choices are defined in the `raw_value, Label` format, one per line.

Two action tags are commonly used with checkbox fields:
- **@NONEOFTHEABOVE** — when applied to a specific answer choice, selecting that choice automatically unchecks all other selections. Use this for "None of the above" or "Not applicable" options.
- **@MAXCHECKED** — limits the number of choices a respondent can select. For example, `@MAXCHECKED='3'` prevents more than three boxes from being checked at once.

## 8.6 Yes – No

A radio button field with two pre-defined choices: **Yes** (coded as 1) and **No** (coded as 0). No choices need to be defined — REDCap supplies them automatically. The codes cannot be changed. If you need to add a third option (e.g., "Not Applicable"), change the field type to **Radio Buttons** and manually define Yes (1), No (0), and any additional choices with appropriate coding.

## 8.7 True – False

A radio button field with two pre-defined choices: **True** (coded as 1) and **False** (coded as 0). Functionally identical to Yes – No but with different labels. The same workaround applies if additional options are needed: convert to Radio Buttons and manually define the choices.

## 8.8 Signature

Captures a handwritten signature as an image. Data entry users can sign with a mouse on a desktop or with their finger on a touchscreen device. Commonly used in electronic consent (e-consent) workflows.

## 8.9 File Upload

Allows the data entry person to upload any file up to a defined size limit (the REDCap default is 12 MB, but this can be increased by your REDCap administrator). Common uses include uploading photos, scanned documents, or PDF reports.

## 8.10 Slider

Displays a horizontal slider ranging from 0 to 100 by default. Options include:
- Defining 2 or 3 custom labels positioned at points along the slider.
- Choosing whether to display the numeric value alongside the slider handle.
- Adjusting the minimum and maximum values.

## 8.11 Descriptive Text

Does not collect any data. Used to display information to the person entering data. Supports several content modes:

- **Plain or rich text** — enter text directly; use the Rich Text Editor for formatting.
- **External media** — embed a video or website by providing a URL; choose to display the media inline or as a popup link.
- **Uploaded files** — upload a PDF, image, or audio file from your computer; these can be displayed inline or as downloadable links. Audio files are rendered in an embedded audio player.

Useful for instructions, section introductions, consent language, or visual aids within a form.

## 8.12 Begin New Section

A formatting field that renders as a horizontal divider line across the instrument. Does not collect data. Used to visually separate sections of a long form. In surveys, section breaks take on additional functionality: you can configure the **Survey Settings** to advance to a new page each time a section break is encountered, turning a single survey into a multi-page experience without creating separate instruments.

## 8.13 Calculated Field

Performs a calculation using values from other fields in the record and displays the result. The equation is defined using variable names (e.g., `[weight] / ([height] * [height])`). REDCap executes the calculation once the referenced fields have data and displays the result on the form. The result is saved when the form is saved. Use the **Special Functions** button in the field editor for help building calculations. Test calculated fields thoroughly in Development mode before beginning real data collection. See **RC-CALC-02 — Calculated Fields** for full coverage.

## 8.14 Dynamic Query (SQL)

An advanced, administrator-only field type. Accepts an SQL query that retrieves a list of options directly from the REDCap backend database. Requires knowledge of REDCap's database schema and SQL. Typically configured by REDCap administrators only and is not editable by standard project users.

---

# 9. Drag-N-Drop Logic Builder

Branching logic controls whether a field is visible or hidden during data entry, based on values entered in other fields.

**Rule:** If the defined logical statement evaluates to **true**, the field is **shown**. If it evaluates to **false**, the field is **hidden**.

REDCap has a powerful branching logic syntax that supports complex conditional expressions. For beginners, the **Drag-N-Drop Logic Builder** provides a guided, no-code interface.

## 9.1 Opening the Logic Builder

| 1 | In the instrument editor, click the **Branching Logic** icon on the field you want to conditionally show or hide. |
| --- | --- |
| 2 | In the branching logic editor that opens, select the **Drag-N-Drop Logic Builder** option. |

## 9.2 Choosing a Logic Operator

Select one of two logic modes:

| Mode | Behavior |
| --- | --- |
| **All below are true** | AND logic. Every condition you define must be true for the field to be shown. |
| **Any below are true** | OR logic. The field is shown if at least one of the conditions you define is true. |

## 9.3 Building the Logic Statement

| 3 | In the left-hand panel, browse available fields and their choices. If your project has multiple instruments, use the instrument selector to browse fields from any instrument. Mixing conditions across instruments is allowed. |
| --- | --- |
| 4 | Drag a field choice from the left panel into the right-hand condition box. |
| 5 | For fields that require a comparison (e.g., a text box or slider), define a value and select a Boolean operator from the following options: |

| Operator | Meaning |
| --- | --- |
| `=` | Equal to |
| `<>` | Not equal to |
| `>` | Greater than |
| `>=` | Greater than or equal to |
| `<` | Less than |
| `<=` | Less than or equal to |

> **Pro tip:** Drag the same field choice twice to define a range — for example, `age >= 18` AND `age <= 65`.

| 6 | Click **Save** when the logic is complete. |
| --- | --- |

REDCap will display the equivalent branching logic syntax below the builder. This is useful for learning the syntax or for copying it elsewhere. For more on advanced branching logic syntax, see RC-BL-01 through RC-BL-04.

---

# 10. Matrix of Fields

A matrix groups a set of fields together in a grid layout, where each row is an individual field and all rows share a common set of column options (answer choices).

> **Important:** You cannot group or ungroup existing individual fields into a matrix directly in the Online Designer. If you need to restructure existing fields as a matrix, use the Data Dictionary (RC-FD-03).

## 10.1 Opening the Matrix Editor

Click the **Add Matrix of Fields** button in the instrument editor at the position where you want to insert the matrix.

## 10.2 Matrix Header Text

An optional text label displayed above the matrix in a highlighted bar (similar to a section header). Although REDCap marks this as optional, providing a header is recommended to orient data entry users.

## 10.3 Matrix Rows

Each row in the matrix is an individual field. Define the following for each row:

| Setting | Required | Description |
| --- | --- | --- |
| **Field Label** | Optional | The row label displayed to the left of the answer choices. May be left blank, as with regular fields. |
| **Variable Name** | Required | Unique identifier for this row/field, following the same rules as regular variable names. REDCap can auto-generate variable names based on the field label text. |
| **Required** | Optional | Whether data entry for this row is required before saving. Use with care in checkbox or ranking matrices — test thoroughly, as required validation can behave unexpectedly in those types. |
| **Field Annotation** | Optional | Internal notes for the instrument designer (not visible during data entry). Can also contain action tags to modify the row's behavior. |

Add additional rows with the **Add another row** button.

> **Pro tip:** In older REDCap versions, best practice was to keep matrices to approximately 5–6 rows because the column headers would scroll off screen in longer matrices. Modern REDCap versions introduced **floating headers** — the column header row stays visible at the top of the screen as users scroll through long matrices.

## 10.4 Matrix Column Options

Define the answer choices that apply to **all rows** in the matrix. Use the `raw_value, Label` format, one per line. The raw value must be unique across all options in the matrix. At least one column option is required.

Note: column options are shared by all rows — it is not possible to define different answer choices for individual rows within the same matrix.

## 10.5 Matrix Group Name

A required internal identifier for the matrix. This name is not shown to data entry users — it is used by REDCap to group the fields together in the database and data dictionary. **Best practice:** Keep this name short and descriptive (e.g., `phq9`, `family_hx`).

## 10.6 Answer Format

Choose one of two matrix types:

| Type | Description |
| --- | --- |
| **Checkboxes** | Each row allows the selection of multiple column options. |
| **Radio Buttons** | Each row allows the selection of one column option only. |

Radio button matrices have an optional **Ranking** mode. When ranking is enabled, each column option can only be selected once across all rows — forcing the respondent to assign each choice to exactly one row. Use this when you want respondents to rank or prioritize items.

## 10.7 Reordering Matrix Rows

Rows can be reordered by drag-and-drop, but **only within the matrix editor** (Edit Matrix of Fields). If you attempt to drag a row within the main instrument editor view, you will move the entire matrix — not an individual row.

## 10.8 Branching Logic on Matrix Rows

Each matrix row is an independent field and supports its own branching logic. Click the branching logic icon on any row to open the standard branching logic editor for that row.

---

# 11. Questions & Answers

| What is the separator between raw values and labels in choice fields? | A comma. Each choice is defined as `raw_value, Label` on its own line. The raw value is stored in the database; the label is shown during data entry. |
| --- | --- |
| Can I have two instruments with the same name? | Technically yes, but it is not recommended. REDCap will assign unique system names internally, which can cause confusion in the code book and data dictionary. Keep display names unique. |
| Which field types allow multiple selections? | Only the **Checkbox** field type and **Checkbox matrix** allow multiple selections per field. All other selection types (dropdown, radio, yes-no, true-false) are single-select. |
| Can I move a field from one instrument to another? | Yes — use the **Move button** on the field (not drag-and-drop). The Move button opens a dialog that allows you to select a target instrument. Drag-and-drop only repositions a field within the same instrument. |
| What happens if I delete a field that has data in it? | The data is permanently lost. In Development mode, deletion is allowed without warning. In Production mode, fields with data cannot be deleted. Always verify whether a field contains real data before deleting. |
| Can I edit the Record ID field? | You can edit some aspects of the Record ID field (such as its label), but you should not restructure or rename it after real data collection has begun, as this can create orphaned records in the backend database. |
| What is the difference between "Add Field" and "Add CDE Field"? | **Add Field** creates a new field from scratch via the field editor — you define the label, type, choices, and all other settings yourself. **Add CDE Field** (formerly "Import from Field Bank") opens the CDE Library, where you search a catalog of standardized Common Data Elements and import a pre-built field definition. CDE fields are useful when your study requires data harmonization, when your funder mandates specific CDEs, or when you want to adopt a validated field definition without building it from scratch. |
| What is Bio-Medical Ontology and is it a field type? | No. Biomedical ontology lookup is an optional enhancement to the **Text Box** field type — not a standalone field type. It converts a text box into an ontology search input. It must be enabled by your REDCap administrator. |
| Is the CDE Library the same as the Field Bank? | Yes — the CDE Library was formerly called the Field Bank. The feature is the same; the name was updated to better reflect its purpose as a catalog of Common Data Elements. Older documentation or training materials may still use "Field Bank." |
| What catalogs are available in the CDE Library? | The default catalog is the NIH CDE Repository. Additional catalogs may be available depending on your institution's REDCap configuration. Contact your REDCap administrator to find out which catalogs are enabled at your site. |
| My first instrument had 20 fields. I moved it to the fifth position and now it only has 19. Why? | REDCap requires the Record ID field to be the first field in the first instrument. When you moved the instrument out of the first position, REDCap automatically relocated the Record ID field to comply with this rule — reducing the original instrument's field count by one. |
| What are the available matrix types? | Checkbox matrix (unranked), Radio button matrix (unranked), and Radio button matrix (ranked). There is no ranked checkbox matrix or slider matrix. |
| Can I copy answer choices from one field to another? | Yes. In the Online Designer, the answer choice editor for dropdown, radio, and checkbox fields includes a copy option that lets you pull in the choices from any existing field in the project. This is the best way to maintain consistent coding and ordering across fields that share the same response set. |
| Do raw values (codes) in choice fields need to be in numeric order? | No. REDCap accepts raw values in any order, and gaps between numbers are fine. This means you can safely add a new answer choice with a new code at any time without renumbering existing choices. If you use a scored instrument, using the score value as the code is a valid strategy — gaps in the sequence are expected and do not affect REDCap's behavior. |

---

# 12. Common Mistakes & Gotchas

## Changing an answer choice label after data collection has started
- The user edits the label (display text) of an answer choice after real records have already been collected.
- The data already stored retains the original raw code — but the label that code maps to has now changed, silently altering the meaning of existing data. For example, renaming "Strawberry" to "Mint" for code 3 means all records previously coded as 3 now read as "Mint" even though "Strawberry" was selected.
- **Prevention:** Treat answer choice labels as permanent once data collection begins. If a label is genuinely wrong, consult your REDCap administrator before changing it. Adding a new choice (with a new code) is safe at any time; changing an existing label is not.
- **Recovery:** No automated recovery through the interface — a record-level data audit is required to assess impact.

## Deleting an answer choice instead of retiring it
- The user deletes an answer choice from a dropdown, radio, or checkbox field after data has been collected using that choice.
- All records that selected the deleted choice lose the associated data — it is permanently removed from the field.
- **Prevention:** Use the action tag **@HIDECHOICE** to retire an answer choice without deleting it. @HIDECHOICE hides the choice from new data entry but preserves it in records where it was already selected.
- **Recovery:** None through the interface. Contact your REDCap administrator — data may be recoverable from a database backup.

## Using duplicate variable names
- The user creates two fields with the same variable name in different instruments.
- REDCap will not allow this and will display an error when you attempt to save.
- **Prevention:** Choose descriptive variable names that include context (e.g., `visit1_sbp` instead of `sbp`) if the same concept is captured at multiple points.
- **Recovery:** Rename one of the conflicting variables.

## Deleting an instrument or field with real data
- The user deletes an instrument or field without realizing it contains participant data.
- The data is permanently lost and cannot be recovered through the interface.
- **Prevention:** Before any deletion, check whether the instrument or field contains data. In Production mode, REDCap will block deletion of fields with data; in Development mode it will not.
- **Recovery:** None through the interface. Contact your REDCap administrator — data may be recoverable from a database backup depending on your institution's backup policy.

## Modifying the Record ID field after data collection
- The user renames or restructures the Record ID field after real records have been created.
- Existing records may become orphaned — they remain in the backend database but no longer appear in the project.
- **Prevention:** Finalize the Record ID field configuration before beginning real data collection.
- **Recovery:** Requires REDCap administrator intervention.

## Dragging matrix rows in the main instrument view
- The user attempts to reorder rows within a matrix by dragging them in the instrument editor.
- REDCap treats the drag as an attempt to move the entire matrix, not an individual row.
- **Prevention:** Always reorder matrix rows from within the **Edit Matrix of Fields** dialog.

## Making checkbox or ranking matrix rows required
- The user marks rows in a checkbox or ranking matrix as required without testing.
- Validation can behave unexpectedly — for example, REDCap may require that at least one checkbox option be selected, but the enforcement logic varies.
- **Prevention:** Thoroughly test any required checkbox or ranking matrix in Development mode before collecting real data.

## Changing the raw values of an imported CDE field
- The user imports a CDE and then changes the choice codes to match their existing project coding.
- The raw values are the entire point of standardization — they ensure the field's data can be compared and merged with other studies using the same CDE. Changing them makes your data non-interoperable.
- **Prevention:** If your project needs different coding, use a regular **Add Field** instead of importing the CDE, and document the deviation. If you have already changed the codes, note this prominently in your data documentation.

## Inconsistent alignment choices across instruments
- The user applies different Custom Alignment settings to similar fields across instruments.
- The data entry interface looks inconsistent, which can confuse users.
- **Prevention:** Agree on an alignment standard at the start of project design and apply it consistently.

## Expecting the Preview Instrument button to test branching logic
- The user uses the Preview Instrument view to verify that branching logic works correctly.
- Branching logic is not active in the Preview Instrument view — it only shows the form layout.
- **Prevention:** Always test branching logic by creating a test record and entering data through the standard data entry interface.

---

# 13. Related Articles

- RC-FD-02 — Online Designer (conceptual overview: what it is, when to use it, Development vs. Production mode behavior)
- RC-FD-01 — Form Design Overview (prerequisite: covers the overall form design workflow and tool selection)
- RC-FD-03 — Data Dictionary (bulk editing alternative to the Online Designer; required for restructuring matrices or moving many fields at once)
- RC-FD-04 — Instrument Library and Zip Files (importing and exporting instruments)
- RC-FD-05 — Codebook (read-only reference for the variable definitions created in the Online Designer)
- RC-BL-01 — Branching Logic Overview and Scope (prerequisite for understanding branching logic concepts used in Section 9)
- RC-BL-02 — Branching Logic Syntax and Atomic Statements (next step after mastering the Drag-N-Drop Logic Builder)
- RC-CALC-02 — Calculated Fields (full coverage of calculated field syntax and configuration)
- RC-DE-05 — Field Validations (how min/max and @FORCE-MINMAX constraints work from the data entry side)

---

# 14. Version & Change Notes

| REDCap Version | Note |
| --- | --- |
| Modern versions (14.x+) | Floating matrix headers introduced — column headers remain visible when scrolling through long matrices. Prior to this, best practice was to limit matrices to 5–6 rows. |
| General | The Online Designer interface may display additional buttons (e.g., Survey Settings, Form Display Logic options) when surveys, longitudinal mode, or DAGs are enabled in the project. This article covers the baseline interface with those features disabled. |
