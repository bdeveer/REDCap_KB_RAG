

**Codebook**

| **Article ID** | [RC-FD-05 — Codebook](RC-FD-05_Codebook.md) |
|---|---|
| **Domain** | Form Design |
| **Applies To** | All REDCap project types; every project user can open the Codebook (no Project Design and Setup rights needed); the inline edit links appear only for users with Project Design and Setup rights |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — Codebook page checked against source code; pages not re-captured |
| **Prerequisite** | [RC-FD-01 — Form Design Overview](RC-FD-01_Form-Design-Overview.md) (background only; no user rights are needed to view the Codebook) |
| **Version** | 1.2 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-FD-01 — Form Design Overview](RC-FD-01_Form-Design-Overview.md); [RC-FD-02 — Online Designer](RC-FD-02_Online-Designer.md); [RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md); [RC-FD-08 — Data Dictionary: Column Reference & Advanced Techniques](RC-FD-08_Data-Dictionary-Column-Reference-and-Advanced-Techniques.md); [RC-NAV-UI-02 — Project Menu Reference](RC-NAV-UI-02_Project-Menu-Reference.md) |
| **Synonyms** | what is the codebook; view all fields and variables at a glance; read-only list of project variables; where to see all variable names and choices; printable reference of project structure; how do i save the codebook as a pdf; codebook vs data dictionary; look up a field definition quickly; see every instrument and field in one place |

---

## 1. Overview

The Codebook is a read-only, human-readable view of every instrument and
variable in a REDCap project. It provides a comprehensive, always
up-to-date reference of the project's structure without requiring the
user to navigate the Online Designer or parse a CSV file. Every user on
the project can open it. This article explains what the Codebook shows,
where to find it, and when to use it.

---

## 2. Key Concepts & Definitions

**Codebook**

A project-level reference view that displays all instruments and their
variables in a structured, human-readable format. The Codebook always
reflects the current live state of the project. It is read-only — it
cannot be used to make changes to instruments or variables directly.

**Read-Only Reference Tool**

The Codebook is not a design tool. You cannot add, edit, delete, or
reorder instruments or variables from the Codebook view. Its purpose is
inspection and reference, not modification.

**Who can see it**

Every project user can open the Codebook; no Project Design and Setup
rights are needed. The Codebook lists all instruments in the project,
regardless of a user's instrument-level (form) rights.

**Inline Edit Links**

Despite being read-only, the Codebook contains direct links that open
the edit interface for individual variables in the Online Designer, and
links that open the branching logic editor for specific variables. These
links are shortcuts — they take you to the appropriate design tool,
not to an editable state within the Codebook itself. They appear only
for users with Project Design and Setup rights, and only while the
project is in Development or, in Production, while it is in Draft Mode.
After an edit, the Online Designer offers a **Return to Codebook** link.

---

## 3. Accessing the Codebook

- **Left-hand menu:** click **Codebook** in the top panel of the project
    menu (**Project Home · Project Setup · Codebook**). It is visible to all
    project users in both Development and Production.

- **Online Designer / Data Dictionary pages:** use the **Codebook** tab
    next to the **Online Designer** and **Data Dictionary** tabs.

- **Online Designer field-edit dialog:** click the **Codebook** link to
    look up other variables while editing a field.

- **Logic editor:** click the **Codebook** button in the branching logic
    or calculation editor dialog.

- **Data Import Tool:** the page links to the Codebook so you can check
    variable names and codes before importing.

The Codebook opens to a full listing of all instruments and their
variables, organized by instrument.

---

## 4. Codebook Layout

The Codebook is structured in three main sections, followed by optional
tables for missing data codes and languages.

### 4.1 Header

At the top of the Codebook page, REDCap displays the label
**"Data Dictionary Codebook"**. A printout (see §4.6) adds:

- The **project title** and **PID** (e.g., *alignment check (PID: 8172)*)
- A **timestamp** of when the page was printed (e.g., *04-11-2026 7:27pm*)

This printed header is useful for documentation and audit purposes — it
makes clear exactly which project and snapshot the printout represents.

> **Version caveat (timestamp):** In 16.0.x LTS and 17.3.x LTS the
> timestamp also shows on screen. In 17.6 Standard it appears only in the
> printout. If you need a dated record, print the page rather than
> relying on a screenshot of the screen view.

### 4.2 Instruments (and Events) Summary Table

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

The **Instruments table** uses a repeat badge with a different meaning:
a badge next to the **instrument name** means that instrument is set up
as a **repeating instrument** in at least one event. It does not tell you
which events. In a classic (non-longitudinal) project, this badge is the
Codebook's only repeating indicator. To see exactly which events an
instrument repeats in, open the repeating instruments and events setup
on the Project Setup page.

> **Navigation additions.** From **15.0.3** the form names in the Instruments table are **internal links** to that form's section of the field table, so you can jump straight to a form on a long codebook. In longitudinal projects, the Events table shows **event IDs** from **15.4.1**, which is useful when you need the numeric ID for an API call or a smart variable rather than the display name.

> **Version caveat (download icon, v17):** In v17 (Standard and 17.3.x LTS),
> users with Project Design and Setup rights see a download icon on each
> instrument row. It downloads the **instrument ZIP** (the same file as
> **Download instrument ZIP** in the Online Designer), not a codebook for
> that instrument. The icon is absent in 16.0.61 LTS; there, download the
> ZIP from the Online Designer instead. See
> [RC-FD-04 — Instrument Library and Zip Files](RC-FD-04_Instrument-Library-and-Zip-Files.md).

### 4.3 Field Table

The main body of the Codebook is a field-by-field table, one per
instrument, with these columns:

| Column | Contents |
|--------|----------|
| *(edit)* | Edit and branching logic links (Design rights only; see §2) |
| **#** | Sequential field number, counting across the entire project (not per instrument) |
| **Variable / Field Name** | The internal variable name (red, monospaced), with branching logic below it |
| **Field Label** | The label displayed to users, with the field note below it; section headers appear here in italics |
| **Field Attributes (Field Type, Validation, Choices, Calculations, etc.)** | Field type, validation, choices, calculation, annotations, alignment, required/identifier flags and other settings |

Each instrument is introduced by a banner row showing the instrument's
display name, form name, and whether it is **Enabled as survey** (shown
in green).

> **Version caveat (17.6+):** In 17.6 Standard you can click a variable
> name to copy it to the clipboard, and fields used by a chatbot
> configuration carry a **Connected** badge. On 16.0.x or 17.3.x LTS,
> select and copy the name manually; no such badge exists.

### 4.4 Finding and collapsing instruments

- **Field finder:** use the field finder at the top of the page to jump
  to a specific variable instead of scrolling.
- **Expand / collapse:** each instrument's field table can be collapsed
  or expanded individually, and there is a control to collapse or expand
  all instruments at once. Your collapse choices are saved, so the
  Codebook reopens the same way next time.

### 4.5 Missing data codes and languages

- **Missing Data Codes:** if the project defines missing data codes, the
  Codebook shows them in their own table with each code and its label.
- **Multi-Language Management:** if the project uses Multi-Language
  Management, the Codebook shows a table of the project's languages, and
  each field gets extra rows with its translations. **???** marks a
  missing translation, which makes the Codebook a quick way to spot
  untranslated fields.

### 4.6 Printing and saving as PDF

The Codebook has no PDF export of its own. To get a file, click
**Print page** and use your browser's print dialog to save as PDF.

- The printout includes the project title, PID and a timestamp (§4.1).
- Each table has an **include in printout** checkbox, so you can leave
  out tables you don't need.
- An instrument that is collapsed on screen prints only as its header,
  marked as collapsed. Expand any instrument whose fields you want in the
  printout.

> **Note:** **Download PDF of All Instruments** is a different output: it
> produces blank data-entry forms, not the Codebook's attribute tables.

---

## 5. What the Codebook Shows

For each variable, the Codebook displays the following. All text is shown
as plain text: HTML formatting in labels and notes is stripped.

**Variable name**
The internal REDCap identifier shown in the Variable / Field Name column.

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
descriptive. Radio fields in a matrix appear as **radio (Matrix)** or
**radio (Matrix - ranking)**. Checkbox fields in a matrix appear as plain
checkbox, and the matrix group name is not shown. To confirm matrix
grouping, check the Online Designer or the Data Dictionary.

**Choices or options**
For radio, dropdown, and checkbox fields: each coded value and its label
are shown in a box. For **checkbox fields**, the Codebook also lists the
**subvariable name** for each option in the format `fieldname___code`
(e.g., `checkbox_rv___1`). Negative or decimal codes have the minus sign
or decimal point turned into an underscore in these names (as in data
exports). This naming convention appears in the Codebook and in data
exports, but it is **not** the syntax used in REDCap expressions. In
branching logic, calculated fields, and action tags, individual checkbox
options are referenced as `[fieldname(code)]` (e.g.,
`[checkbox_rv(1)] = '1'`). The Codebook is useful for looking up the
numeric code for a given option; use the expression syntax
`[field(code)]` everywhere else in REDCap.

**Validation type and range**
For text fields with validation (e.g., `text (date_mdy)`, `text (email)`).
Slider fields show their min/max and label values (e.g.,
`slider (Min: 0, Max: 100)` and `Slider labels: Low, , High`).

**Calculation formula**
For calculated fields, the full formula is shown in the Field Attributes
column (e.g., `Calculation: 1+1`).

**Branching logic**
Displayed in the Variable / Field Name column, below the variable name:
*"Show the field ONLY if:"* followed by the logic expression. The prefix
is greyed out; the expression itself is shown in normal text.

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

**Other attributes**
Where set, the Field Attributes column also shows the question number
(surveys with custom numbering), survey stop actions, a media/video URL,
and the SQL query of a dynamic SQL field.

**Completion status field (`_complete`)**
Every instrument automatically ends with a system-generated completion
status field. Its variable name is `{form_name}_complete` (e.g.,
`application_complete`, `review_1_complete`). It is a dropdown with
three fixed choices: 0 = Incomplete, 1 = Unverified, 2 = Complete.
This field appears in the Codebook — both on screen and in a printout —
just like any user-defined field, and it also appears in all data
exports. However, `_complete` fields are **not** present in the Data
Dictionary CSV, because they are auto-generated by REDCap rather than
user-defined. They cannot be added, modified, or removed through a
Data Dictionary upload.

As a result, the Codebook will always show exactly one more field
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


> **Note:** The Codebook always reflects the currently applied state of the project. In Production mode, pending (unapproved) Online Designer changes are not shown — the Codebook shows only what is live.


---

## 6. When to Use the Codebook

The Codebook is the right tool in these situations:

- **Writing or debugging branching logic** — the Codebook lets you look
    up variable names, their exact coded values, and checkbox
    subvariable names without switching to the Online Designer or opening
    the Data Dictionary. The **Codebook** button in the logic editor
    opens it right where you need it.

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

- **Checking translations** — in Multi-Language Management projects,
    look for **???** in the translation rows to find missing translations.

- **Onboarding to an unfamiliar project** — the Codebook gives a rapid,
    readable summary of what the project collects and how it is
    structured, including all branching logic conditions and annotations.

- **Documentation and archival** — use **Print page** and save as PDF
    from your browser to capture the project structure at a point in
    time, useful for IRB submissions, handoffs, or version records.

- **LLM-assisted project analysis** — the Codebook (or a PDF saved from
    its **Print page**) is the most efficient way to give a large language
    model a complete understanding of a REDCap project's structure. It
    consolidates in a single document everything that would otherwise
    require ingesting multiple files (data dictionary CSV, longitudinal
    events CSV) or making multiple API calls and interpreting their
    combined output. This is especially true for repeating instrument and
    repeating event configuration: apart from the repeating instruments
    and events setup on the Project Setup page, the Instruments and Events
    summary tables are the easiest place to see this information in one
    view. The alternatives — an API call to the repeating instruments
    endpoint, or inferring repeating setup from the shape of a data
    export — are indirect and require additional steps. A single Codebook
    PDF gives an LLM the full picture: instruments, events, arm/event
    assignments, repeating setup, field types, choices, branching logic,
    and action tags, all in one structured document. Expand all
    instruments before printing so none are left out.

---

## 7. Codebook vs. Other Reference Options

| **Reference Tool** | **Format** | **Editable?** | **Best For** |
| --- | --- | --- | --- |
| Codebook | Web view, organized by instrument; **Print page** to save as PDF | No (links to editors) | Human-readable review; looking up variable names while designing; getting event names; attribute-rich printed snapshot |
| Data Dictionary (downloaded CSV) | Spreadsheet | Yes (upload to apply changes) | Bulk editing; offline reference; version control |
| Download PDF of All Instruments | PDF | No | Blank data-entry forms for paper collection or showing stakeholders what participants see |
| Online Designer | Web interface, one instrument at a time | Yes | Making edits; previewing form appearance |

> **Note:** There is no Codebook PDF export. A PDF saved from the Codebook's **Print page** follows the tabular
> structure described in this article: the header, instruments/events summary tables, and the field-by-field table
> with all attributes. **Download PDF of All Instruments** is a different document: blank data-entry forms that show
> how instruments look, without the attribute tables. Use the Codebook printout when you need a compact,
> attribute-rich snapshot of your project structure.

---

## 8. Common Questions

**Q: Can I edit variables directly from the Codebook?**

**A:** No. The Codebook is read-only. Users with Project Design and Setup
rights see inline links that open the Online Designer's edit interface or
branching logic editor for individual variables (in Development, or in
Production while in Draft Mode), but the editing itself happens in those
tools — not in the Codebook.

**Q: Do I need design rights to see the Codebook?**

**A:** No. Every project user can open the Codebook, and it lists all
instruments regardless of the user's instrument-level rights. Only the
edit links require Project Design and Setup rights.

**Q: Does the Codebook update in real time as I make changes?**

**A:** Yes, for applied changes. In Development mode, changes made in the
Online Designer or via Data Dictionary upload are reflected immediately.
In Production mode, pending (unapproved) changes are not shown — the
Codebook reflects only the live project state.

**Q: Is the Codebook the same as the Data Dictionary?**

**A:** No. The Data Dictionary is a CSV file that defines your project's
variables and can be uploaded to modify them. The Codebook is a
read-only web view of the same information in a more readable format.
They present similar content but serve entirely different purposes.

**Q: Can I export the Codebook as a file?**

**A:** Not as a download. Click **Print page** on the Codebook and save as
PDF from your browser's print dialog. The printout includes the project
title, PID and a timestamp; use the **include in printout** checkboxes to
choose tables, and expand any collapsed instruments first, since
collapsed instruments print only as a header. For a machine-readable
version, use **Download the current Data Dictionary (CSV)** instead.
**Download PDF of All Instruments** gives blank data-entry forms, not the
Codebook.

**Q: I'm new to a project and need to understand its structure quickly.
Is the Codebook the best starting point?**

**A:** Yes. The Codebook gives you a structured, human-readable view of all
instruments and variables — including branching logic conditions, action
tags, and (for longitudinal projects) the events each instrument is
assigned to — without requiring you to interpret a CSV or navigate the
Online Designer instrument by instrument.

**Q: Where do I find the exact unique event names I need for branching logic or piping?**

**A:** The Events table in the Codebook header section lists all events with
their unique event names (the internal identifiers used in expressions).
This is the fastest way to confirm the exact string you need.

**Q: Why does my field label in the Codebook show something like `[enterprise_redcap_arm_1][field_name]` instead of a real label?**

**A:** In longitudinal projects with repeated instruments, field labels are
sometimes built using piping syntax that pulls values from another event.
The Codebook displays the raw syntax as it was entered — it does not
resolve piped values. The actual label a user sees during data entry will
be different.

---

## 9. Common Mistakes & Gotchas

- **Expecting to edit from the Codebook:** the Codebook is read-only. Use
    the inline links to jump to the Online Designer if you need to make
    a change, but the edit happens there.

- **Looking for a Codebook PDF export:** there isn't one. Use **Print
    page** and save as PDF from the browser, or download the Data
    Dictionary CSV. **Download PDF of All Instruments** produces blank
    forms, not a codebook.

- **Printing with instruments collapsed:** collapsed instruments print
    only as a header marked collapsed. Expand everything you need before
    printing.

- **Relying on the Codebook in Production when changes are pending:** the
    Codebook only reflects the live, approved project state. Pending
    Online Designer changes in Production are not visible until
    approved. If you recently made a change and don't see it in the
    Codebook, check whether it is still in the approval queue.

- **Overlooking the inline edit links:** the Codebook's inline links to
    the Online Designer and branching logic editor are easy to miss but
    save significant time. They let you jump directly to a specific
    variable's edit interface without scrolling through the full Online
    Designer. If you don't see them, you either lack Project Design and
    Setup rights or the project is in Production without Draft Mode.

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

---

## 10. Related Articles

- [RC-FD-01 — Form Design Overview](RC-FD-01_Form-Design-Overview.md) (prerequisite)

- [RC-FD-02 — Online Designer](RC-FD-02_Online-Designer.md) (the editing tool linked from the
    Codebook's inline edit links)

- [RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md) (the CSV-format alternative reference
    and design tool)

- [RC-FD-04 — Instrument Library and Zip Files](RC-FD-04_Instrument-Library-and-Zip-Files.md) (the
    instrument ZIP downloaded from the Codebook's instrument table in v17)

- [RC-FD-08 — Data Dictionary: Column Reference & Advanced Techniques](RC-FD-08_Data-Dictionary-Column-Reference-and-Advanced-Techniques.md)
    (deeper reference for what each field attribute means)

- [RC-BL-02 — Branching Logic: Syntax & Atomic Statements](RC-BL-02_Branching-Logic-Syntax-and-Atomic-Statements.md) (using
    variable names and choice codes found in the Codebook)

- [RC-BL-04 — Branching Logic: Structured Fields & Checkboxes](RC-BL-04_Branching-Logic-Structured-Fields-and-Checkboxes.md) (using
    checkbox option codes found in the Codebook to construct
    `[field(code)]` expressions)

- [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md) (background on arms,
    events, and instrument-event assignments shown in the Codebook
    summary tables)

- [RC-LONG-02 — Repeated Instruments & Events Setup](RC-LONG-02_Repeated-Instruments-and-Events-Setup.md) (the repeating
    instruments and events setup that the Codebook's repeating
    indicators summarize)

- [RC-AT-01 — Action Tags: Overview](RC-AT-01_Action-Tags-Overview.md) (action tags are displayed
    verbatim in the Codebook's Field Attributes column; this article
    explains what they do)

- [RC-SURV-01 — Surveys – Basics](RC-SURV-01_Surveys-Basics.md) (the Codebook flags each instrument
    that is enabled as a survey)

- [RC-PIPE-01 — Piping: Basics, Syntax & Field Types](RC-PIPE-01_Piping-Basics-Syntax-and-Field-Types.md) (piping
    expressions in field labels appear as raw syntax in the Codebook
    rather than resolved values)

- [RC-NAV-UI-02 — Project Menu Reference](RC-NAV-UI-02_Project-Menu-Reference.md) (the Codebook link appears
    in the Project Home and Design menu section; always visible to
    all users regardless of rights)
