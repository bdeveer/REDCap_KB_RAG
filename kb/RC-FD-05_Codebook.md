RC-FD-05

**Codebook**

| **Article ID** | RC-FD-05 |
| --- | --- |
| **Domain** | Form Design |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Prerequisite** | RC-FD-01 — Form Design Overview |
| **Version** | 1.1 |
| **Last Updated** | 2026-04 |
| **Author** | REDCap Support |
| **Related Topics** | RC-FD-01 — Form Design Overview; RC-FD-02 — Online Designer; RC-FD-03 — Data Dictionary; RC-FD-08 — Data Dictionary Column Reference & Advanced Techniques |

# 1. Overview

The Codebook is a read-only, human-readable view of every instrument and
variable in a REDCap project. It provides a comprehensive, always
up-to-date reference of the project's structure without requiring the
user to navigate the Online Designer or parse a CSV file. This article
explains what the Codebook shows, where to find it, and when to use it.

# 2. Key Concepts & Definitions

**Codebook**

A project-level reference view that displays all instruments and their
variables in a structured, human-readable format. The Codebook always
reflects the current live state of the project. It is read-only — it
cannot be used to make changes to instruments or variables directly.

**Read-Only Reference Tool**

The Codebook is not a design tool. You cannot add, edit, delete, or
reorder instruments or variables from the Codebook view. Its purpose is
inspection and reference, not modification.

**Inline Edit Links**

Despite being read-only, the Codebook contains direct links that open
the edit interface for individual variables in the Online Designer, and
links that open the branching logic editor for specific variables. These
links are shortcuts — they take you to the appropriate design tool,
not to an editable state within the Codebook itself.

# 3. Accessing the Codebook

- From the Project Setup page: click **Codebook** in the Design Your Data
    Collection Instruments section.

- From the left-hand menu: click **Codebook** under the Data Collection
    section (available in both Development and Production modes).

- The Codebook opens to a full listing of all instruments and their
    variables, organized by instrument.

# 4. Codebook Layout

The Codebook is structured in three main sections:

## 4.1 Header

At the top of the Codebook (and the PDF export), REDCap displays:

- The label **"Data Dictionary Codebook"**
- The **project title** and **PID** (e.g., *alignment check (PID: 8172)*)
- A **timestamp** of when the codebook was generated (e.g., *04-11-2026 7:27pm*)

This header is useful for documentation and audit purposes — it makes
clear exactly which project and snapshot the codebook represents.

## 4.2 Instruments (and Events) Summary Table

Below the header, the Codebook shows a summary table of all instruments
in the project. Each row lists:

- **Instrument** (display name, clickable to jump to that section)
- **Form Name** (the internal unique name)
- **Events** (for longitudinal projects only — which events the instrument is assigned to)

For **longitudinal projects**, the Codebook also includes an **Events
table** that lists every event with its:

- **Event Name** (display label)
- **Unique event name** (the internal identifier used in expressions, e.g., `enterprise_redcap_arm_1`)
- **Event ID** (numeric ID)
- **Repeating event indicator**: a repeat icon next to an event name in this table signals that the event itself is configured as a repeating event.

This Events table is particularly useful when writing branching logic or
piping expressions that reference specific events, since it provides the
exact unique event names needed in syntax like `[event_name][field_name]`.

The **Instruments table** also uses the repeat icon, but with a different
meaning: when the icon appears next to an event name in an instrument's
row, it means that specific instrument is configured as a **repeating
instrument** within that event. An instrument can repeat in some events
but not others, so it's worth checking each event individually in this
table. Together, the two tables give a complete picture of the project's
repeating structure at a glance — before you even reach the field definitions.

## 4.3 Field Table

The main body of the Codebook is a field-by-field table with three columns:

| Column | Contents |
|--------|----------|
| **#** | Sequential field number, counting across the entire project (not per instrument) |
| **Variable / Field Name** + *Field Note* | The internal variable name (in red/monospaced in the web view), and the branching logic and field note below it |
| **Field Label** | The human-readable label displayed to users; section headers appear here in italics |
| **Field Attributes** | Field type, validation, choices, calculation, annotations, alignment, required/identifier flags |

Each instrument is introduced by a banner row showing the instrument's
display name, form name, and whether it is **Enabled as survey** (shown
in green).

# 5. What the Codebook Shows

For each variable, the Codebook displays the following:

**Variable name**
The internal REDCap identifier shown in the Variable/Field Name column.

**Field note**
If a field note was set, it appears in italics below the field label in
the Field Label column. Field notes provide supplemental instructions to
users during data entry.

**Section headers**
Section headers appear in the Field Label column in italics above the
field label of the first field in that section. They do not have their
own row — they attach to the next field's row.

**Field type**
Shown in the Field Attributes column. Includes all standard types: text,
notes, radio, dropdown, checkbox, calc, yesno, truefalse, file, slider,
descriptive. Matrix groups appear as **radio (Matrix)** and list their
group members together.

**Choices or options**
For radio, dropdown, and checkbox fields: each coded value and its label
are shown in a box. For **checkbox fields**, the Codebook also lists the
**subvariable name** for each option in the format `fieldname___code`
(e.g., `checkbox_rv___1`). This naming convention appears in the Codebook
and in data exports, but it is **not** the syntax used in REDCap
expressions. In branching logic, calculated fields, and action tags,
individual checkbox options are referenced as `[fieldname(code)]`
(e.g., `[checkbox_rv(1)] = '1'`). The Codebook is useful for looking up
the numeric code for a given option; use the expression syntax `[field(code)]`
everywhere else in REDCap.

**Validation type and range**
For text fields with validation (e.g., `text (date_mdy)`, `text (email)`).
Slider fields show their min/max and label values (e.g.,
`slider (Min: 0, Max: 100)` and `Slider labels: Low, , High`).

**Calculation formula**
For calculated fields, the full formula is shown in the Field Attributes
column (e.g., `Calculation: 1+1`).

**Branching logic**
Displayed in the Variable/Field Name column, below the variable name, in
grey text: *"Show the field ONLY if:"* followed by the logic expression.
This is greyed out in both the web view and the PDF export to visually
distinguish it from the variable name itself.

**Field annotations (action tags)**
All action tags and annotations applied to a field are shown in the
Field Attributes column verbatim, exactly as entered in the data
dictionary (e.g., `@DEFAULT='[lastup][previous-instance]'`,
`@PLACEHOLDER="Last, First"`, `@HIDECHOICE='21,3,2,4,1,'`,
`@NONEOFTHEABOVE='98,99'`).

**Required status and Identifier flag**
Appear alongside the field type in the Field Attributes column
(e.g., `text (email), Required, Identifier`).

**Custom alignment**
When field-level alignment has been explicitly set, it appears in the
Field Attributes column (e.g., `Custom alignment: LH`). The four options
are RV (Right Vertical, the default), LV (Left Vertical), LH (Left
Horizontal), and RH (Right Horizontal).

**File attachments in descriptive fields**
Descriptive fields with embedded file attachments show the attachment
filename and display format in the Field Attributes column
(e.g., `Attachment: BERD_FAQs_2024-12-20.pdf, Display format: Link` or
`Display format: Inline image/PDF`).

**Completion status field (`_complete`)**
Every instrument automatically ends with a system-generated completion
status field. Its variable name is `{form_name}_complete` (e.g.,
`application_complete`, `review_1_complete`). It is a dropdown with
three fixed choices: 0 = Incomplete, 1 = Unverified, 2 = Complete.
This field appears in the Codebook — both the web view and PDF export —
just like any user-defined field, and it also appears in all data
exports. However, `_complete` fields are **not** present in the Data
Dictionary CSV, because they are auto-generated by REDCap rather than
user-defined. They cannot be added, modified, or removed through a
Data Dictionary upload.

As a result, the Codebook PDF will always show exactly one more field
per instrument than the Data Dictionary CSV. For a project with N
instruments, the Codebook will have N additional `_complete` fields.
This is expected behavior, not a discrepancy.

Despite not appearing in the Data Dictionary, `_complete` fields are
fully functional and can be referenced in branching logic and
calculated fields using the standard variable name syntax:

```
# Show a field only when a prior form is marked Complete
[intake_complete] = '2'
```

  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Note:** The Codebook always reflects the currently applied state of the project. In Production mode, pending (unapproved) Online Designer changes are not shown — the Codebook shows only what is live.
  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 6. When to Use the Codebook

The Codebook is the right tool in these situations:

- **Writing or debugging branching logic** — the Codebook lets you look
    up variable names, their exact coded values, and checkbox
    subvariable names without switching to the Online Designer or opening
    the Data Dictionary.

- **Getting event names for longitudinal expressions** — the Events
    table at the top of the Codebook lists the exact unique event names
    needed when writing cross-event expressions like
    `[enterprise_redcap_arm_1][field_name]`.

- **Human-readable overview of project structure** — the Codebook is
    easier to read than the raw Data Dictionary CSV and more navigable
    than the Online Designer for purely reviewing content.

- **Verifying choice coding** — especially useful when writing branching
    logic or checking what values will appear in a data export.

- **Quickly navigating to a variable's edit interface** — use the
    inline edit link rather than scrolling through the Online Designer.

- **Onboarding to an unfamiliar project** — the Codebook gives a rapid,
    readable summary of what the project collects and how it is
    structured, including all branching logic conditions and annotations.

- **Documentation and archival** — generating the PDF export captures
    the project structure at a point in time, useful for IRB submissions,
    handoffs, or version records.

- **LLM-assisted project analysis** — the Codebook (or its PDF export)
    is the most efficient way to give a large language model a complete
    understanding of a REDCap project's structure. It consolidates in a
    single document everything that would otherwise require ingesting
    multiple files (data dictionary CSV, longitudinal events CSV) or
    making multiple API calls and interpreting their combined output.
    This is especially true for repeating instrument and repeating event
    configuration: the Instruments and Events summary tables are the
    only place in the REDCap UI where this information is directly
    visible in one view. The alternatives — an API call to the repeating
    instruments endpoint, or inferring repeating setup from the shape of
    a data export — are indirect and require additional steps. A single
    Codebook PDF gives an LLM the full picture: instruments, events,
    arm/event assignments, repeating setup, field types, choices, branching
    logic, and action tags, all in one structured document.

# 7. Codebook vs. Other Reference Options

  ---------------------------------- ----------------------------------------- ------------------------------- ------------------------------------------------------------------
  **Reference Tool**                 **Format**                                **Editable?**                   **Best For**
  Codebook                           Web view, organized by instrument         No (links to editors)           Human-readable review; looking up variable names while designing; getting event names
  Data Dictionary (downloaded CSV)   Spreadsheet                               Yes (upload to apply changes)   Bulk editing; offline reference; version control
  Download PDF of All Instruments    PDF                                       No                              Documentation; IRB submissions; stakeholder review
  Online Designer                    Web interface, one instrument at a time   Yes                             Making edits; previewing form appearance
  ---------------------------------- ----------------------------------------- ------------------------------- ------------------------------------------------------------------

> **Note:** The **PDF export of the Codebook** (accessible from the Design Your Data Collection Instruments section) and the
> **Download PDF of All Instruments** option produce similar outputs but differ in layout. The Codebook PDF follows the
> tabular structure described in this article and includes the header, instruments/events summary tables, and the full
> field-by-field table with all attributes. Use it when you need a compact, attribute-rich snapshot of your project structure.

# 8. Common Questions

**Q: Can I edit variables directly from the Codebook?**

A: No. The Codebook is read-only. It contains inline links that open the
Online Designer's edit interface or branching logic editor for
individual variables, but the editing itself happens in those tools —
not in the Codebook.

**Q: Does the Codebook update in real time as I make changes?**

A: Yes, for applied changes. In Development mode, changes made in the
Online Designer or via Data Dictionary upload are reflected immediately.
In Production mode, pending (unapproved) changes are not shown — the
Codebook reflects only the live project state.

**Q: Is the Codebook the same as the Data Dictionary?**

A: No. The Data Dictionary is a CSV file that defines your project's
variables and can be uploaded to modify them. The Codebook is a
read-only web view of the same information in a more readable format.
They present similar content but serve entirely different purposes.

**Q: Can I export the Codebook as a file?**

A: Not directly as a Codebook export from the Codebook page itself.
For a portable version, use **Download the current Data Dictionary
(CSV)** or **Download PDF of All Instruments**, both available from
the Design Your Data Collection Instruments section. The PDF option
produces a structured document similar to what you see in the web
Codebook view.

**Q: I'm new to a project and need to understand its structure quickly.
Is the Codebook the best starting point?**

A: Yes. The Codebook gives you a structured, human-readable view of all
instruments and variables — including branching logic conditions, action
tags, and (for longitudinal projects) the events each instrument is
assigned to — without requiring you to interpret a CSV or navigate the
Online Designer instrument by instrument.

**Q: Where do I find the exact unique event names I need for branching logic or piping?**

A: The Events table in the Codebook header section lists all events with
their unique event names (the internal identifiers used in expressions).
This is the fastest way to confirm the exact string you need.

**Q: Why does my field label in the Codebook show something like `[enterprise_redcap_arm_1][field_name]` instead of a real label?**

A: In longitudinal projects with repeated instruments, field labels are
sometimes built using piping syntax that pulls values from another event.
The Codebook displays the raw syntax as it was entered — it does not
resolve piped values. The actual label a user sees during data entry will
be different.

# 9. Common Mistakes & Gotchas

- **Expecting to edit from the Codebook:** the Codebook is read-only. Use
    the inline links to jump to the Online Designer if you need to make
    a change, but the edit happens there.

- **Treating the Codebook as an export:** the Codebook is a live web view,
    not a downloadable file. Use the Data Dictionary download or the PDF
    export for portable versions of your project structure.

- **Relying on the Codebook in Production when changes are pending:** the
    Codebook only reflects the live, approved project state. Pending
    Online Designer changes in Production are not visible until
    approved. If you recently made a change and don't see it in the
    Codebook, check whether it is still in the approval queue.

- **Overlooking the inline edit links:** the Codebook's inline links to
    the Online Designer and branching logic editor are easy to miss but
    save significant time. They let you jump directly to a specific
    variable's edit interface without scrolling through the full Online
    Designer.

- **Misreading action tag syntax:** action tags shown in the Codebook are
    displayed verbatim as entered in the data dictionary. They show the
    raw syntax (e.g., `@DEFAULT='[field][previous-instance]'`), not the
    tag's behavior or resolved value. If you see unfamiliar syntax,
    consult the action tag documentation for what it does.

- **Confusing Codebook checkbox display with expression syntax:** the Codebook
    shows checkbox options using the `fieldname___code` format (e.g.,
    `inactive___1`). This is a display and export convention only — do not
    use it in branching logic or other REDCap expressions. The correct
    expression syntax for referencing a checkbox option is
    `[fieldname(code)]` (e.g., `[inactive(1)] = '1'`). Use the Codebook
    to look up the numeric code for the option you need, then use that
    code in the `[field(code)]` expression syntax.

- **Missing the Events table in longitudinal projects:** the unique event
    names listed in the Events summary table at the top of the Codebook
    are the exact strings needed in cross-event branching logic and piping
    expressions. It's easy to scroll past this table, but it's one of the
    most useful parts of the Codebook for longitudinal project work.

- **Unexpected field count difference between the Codebook and the Data
    Dictionary:** if you compare the total number of fields in the Codebook
    to those in your downloaded Data Dictionary CSV, the Codebook will
    always show more — exactly one extra per instrument. Those are the
    auto-generated `_complete` completion status fields. They appear in
    the Codebook and in data exports but are intentionally absent from
    the Data Dictionary. This is expected behavior, not a project error.

# 10. Related Articles

- RC-FD-01 — Form Design Overview (prerequisite)

- RC-FD-02 — Online Designer (the editing tool linked from the
    Codebook's inline edit links)

- RC-FD-03 — Data Dictionary (the CSV-format alternative reference
    and design tool)

- RC-FD-08 — Data Dictionary: Column Reference & Advanced Techniques
    (deeper reference for what each field attribute means)

- RC-BL-02 — Branching Logic: Syntax & Atomic Statements (using
    variable names and choice codes found in the Codebook)

- RC-BL-04 — Branching Logic: Structured Fields & Checkboxes (using
    checkbox option codes found in the Codebook to construct
    `[field(code)]` expressions)

- RC-LONG-01 — Longitudinal Project Setup (background on arms,
    events, and instrument-event assignments shown in the Codebook
    summary tables)

- RC-LONG-02 — Repeated Instruments & Events Setup (the repeating
    instrument and repeating event indicators shown in the Codebook
    summary tables are the only direct UI view of this configuration)

- RC-AT-01 — Action Tags: Overview (action tags are displayed
    verbatim in the Codebook's Field Attributes column; this article
    explains what they do)

- RC-SURV-01 — Surveys – Basics (the Codebook flags each instrument
    that is enabled as a survey)

- RC-PIPE-01 — Piping: Basics, Syntax & Field Types (piping
    expressions in field labels appear as raw syntax in the Codebook
    rather than resolved values)
