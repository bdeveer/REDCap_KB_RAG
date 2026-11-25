---
id: RC-FD-08
title: 'Data Dictionary: Column Reference & Advanced Techniques'
domain: Form Design
applies_to:
- All REDCap project types
- requires Project Design and Setup rights
requires: Any supported version
verified_against: REDCap v17.5.4 (Standard) / v17.3.18 (LTS) — changelog review; page
  not re-captured. Data dictionary column rules behaviour checked against source code
  of v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS)
prerequisites:
- RC-FD-03 — Data Dictionary
version: '1.9'
last_updated: 2026-11
related:
- id: RC-FD-01
  title: Form Design Overview
- id: RC-FD-02
  title: Online Designer
- id: RC-BL-01
  title: 'Branching Logic: Overview & Scope'
- id: RC-AT-01
  title: 'Action Tags: Overview'
tags:
- form design
- instruments
synonyms:
- set slider range min max in data dictionary
- what does each data dictionary column mean
- data dictionary column reference
- which columns are required in the data dictionary
- allowed values for choices and validation columns
- advanced excel tips for large data dictionaries
- meaning of the 18 data dictionary fields
- format reference for data dictionary csv
- how to fill in each dictionary column correctly
- make a redcap slider horizontal or vertical
---

# 1. Overview

This article is a 201-level reference for the REDCap Data Dictionary. It assumes familiarity with the Data Dictionary concept and basic workflow covered in [RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md). The article provides a complete column-by-column reference for all 18 Data Dictionary columns, explains which columns are mandatory versus optional, documents the allowed syntax and codes for each column, and covers advanced Excel techniques that make working with large data dictionaries faster and more reliable. It also addresses best practices specific to mobile data collection and longitudinal project designs.

---

# 2. Key Concepts & Definitions

## Data Dictionary Aspects

The term "aspect" refers to a single column in the Data Dictionary. Each column defines one property of a variable — its name, its form assignment, its field type, its display label, and so on. There are 18 aspects (columns A through R) in the Data Dictionary CSV. Not all aspects apply to all field types; some are conditionally mandatory and some are unused for certain field types.

## Mandatory vs. Conditionally Mandatory vs. Non-Mandatory Columns

REDCap classifies each column into one of four tiers:

- **Mandatory:** Must be populated for every variable row. The upload will fail or the variable will be malformed if these are blank.
- **Conditionally Mandatory:** Required only when certain conditions are met (e.g., the field type supports choices).
- **Non-Mandatory:** Optional enrichment — the project functions correctly without these values, but they improve usability and data quality.
- **Matrix Fields:** Applicable only to variables that are part of a matrix group.

The mandatory columns are A (Variable Name), B (Form Name), D (Field Type), and E (Field Label). Column F (Choices, Calculations, or Slider Labels) is conditionally mandatory depending on field type. A blank A, B or D is an upload error; a blank Field Label (E) is only a warning, so the upload goes through and the variable has no visible question text.

## Errors vs. Warnings on Upload

REDCap's upload check reports two kinds of problem, and the difference decides whether your file goes in:

- **Errors** block the upload. Nothing is changed until you fix them and upload again.
- **Warnings** do not block it. Many warnings mean REDCap has **changed your value for you** (for example, converting a variable name to lowercase, or blanking a cell it does not recognise). Read every warning before you commit: the design REDCap saves may differ from the file you wrote.

The rules in Section 5 say which outcome applies to each column.

## Field Type

The field type determines how REDCap renders a variable on the data entry form and what additional columns apply to it. Only REDCap-supported shorthand codes are valid. See Section 3.4 for the full list of accepted field type codes.

## Matrix

A matrix is a grid of variables that share the same answer choices, displayed as a table in REDCap. Matrix variables must be of type `radio` or `checkbox`, must be sequential in the Data Dictionary, must share the same choices, and must all reference the same Matrix Group Name (Column P).

## Action Tags

Action tags are special codes entered in the Field Annotation column (Column R) that modify how a variable behaves in surveys or data entry. They begin with the `@` symbol. Multiple action tags can be applied to a single variable by separating them with spaces.

## Identifier Flag

Marking a variable as an identifier (Column K) does not change how data is entered or stored within REDCap. It does change what users can export: users whose data export rights are **De-Identified**, or who choose **Remove All Identifier Fields** when exporting, get exports with the flagged variables removed. Because of that, the flag works as part of access control through export rights, not just as documentation — a variable that holds identifying data but is not flagged will reach users with de-identified export rights. In Production, flagging new identifiers in a draft can also stop the changes from being approved automatically.

---

# 3. What the Data Dictionary Defines — and What It Does Not

## 3.1 What the Data Dictionary Defines

The Data Dictionary defines every variable and every instrument in a project. Uploading a Data Dictionary completely replaces the existing instrument configuration. It is the authoritative source for:

- Variable names, form assignments, and display order
- Field types and field labels
- Answer choices, calculations, and slider labels
- Field notes and validation rules
- Branching logic and required-field flags
- Identifier flags, custom alignment, and question numbering
- Matrix groupings and action tags

## 3.2 What the Data Dictionary Does NOT Define

Despite its name, the Data Dictionary does not define every aspect of a REDCap project. The following elements are configured separately through other REDCap interfaces and are not affected by uploading a Data Dictionary:

- **Events** — defined in the Longitudinal Setup module
- **Surveys, survey queues, and survey settings** — configured in the Survey Settings module
- **Project settings** — set on the Project Setup page
- **User rights and Data Access Groups** — managed in the User Rights and DAG modules
- **Schedules** — configured in the Scheduling module
- **Randomization** — configured in the Randomization module
- **Data Quality rules** — defined in the Data Quality module
- **Reports** — created in the Reports module

> **Important:** If your project includes events, surveys, or other configuration elements, those must be set up or maintained separately. Uploading a Data Dictionary will not touch them, but it also will not recreate them if they depend on variables that you remove or rename.

> **Critical — removing or renaming an instrument is the exception.** When an upload removes an instrument (no rows left with that Form Name) or renames one (its rows now carry a new Form Name), REDCap permanently deletes the settings tied to the old instrument:
>
> - its event designations (in longitudinal projects)
> - its locking labels, locked-record status and e-signatures
> - its repeating instrument setting
> - instrument-level user rights for that instrument
>
> These are not restored if you change the name back. A survey on the **first** instrument follows a rename. In a classic (non-longitudinal) project, new instruments are designated automatically. Before renaming instruments in a project that has data, check what locking, e-signatures, event designations and user rights you would need to redo.


---

# 4. Data Dictionary Structure

## 4.1 Row Structure

Each row in the Data Dictionary defines exactly one variable. Exceptions:

- **Row 1** contains the column headers. Do not edit or delete row 1. REDCap skips the first row and reads the columns **by position**, not by header text, so a missing header row means your first variable is skipped, and an inserted or reordered column shifts every value into the wrong column.
- **Row 2** defines the REDCap Record ID variable. This row is mandatory in every project. The Record ID variable is always the first variable in the first form. REDCap treats it as a plain `text` field whatever you enter in Column D, and clears any Section Header (Column C) on it.

> **Important:** Whichever variable is in row 2 becomes the record ID. If records already exist and row 2 names a different variable, REDCap shows only a **warning**, not an error, so the upload can go through and change the record ID field. Check row 2 before every upload to a project with data. Uploads through the API do not show warnings at all.

## 4.2 Column Overview

The Data Dictionary has exactly 18 columns. The table below lists each column, its letter designation, its category, and its purpose. Detailed syntax and rules for each column are in Section 5.

| Col | Aspect Name | Category | Purpose |
|-----|-------------|----------|---------|
| A | Variable / Field Name | Mandatory | Unique internal identifier for the variable |
| B | Form Name | Mandatory | Assigns the variable to an instrument |
| C | Section Header | Non-mandatory | Creates a labeled divider bar above the variable |
| D | Field Type | Mandatory | Sets the input type (text, radio, checkbox, etc.) |
| E | Field Label | Mandatory | Sets the question text shown to users |
| F | Choices, Calculations, or Slider Labels | Conditionally Mandatory | Defines answer choices, a formula, or slider endpoint labels |
| G | Field Note | Non-mandatory | Adds a short instructional note below the variable |
| H | Text Validation Type or Show Slider Number | Non-mandatory | Sets the validation format for text fields or shows value on slider |
| I | Text Validation Min | Non-mandatory | Sets the minimum allowed value for validated text fields |
| J | Text Validation Max | Non-mandatory | Sets the maximum allowed value for validated text fields |
| K | Identifier? | Non-mandatory | Flags the variable as containing identifying information |
| L | Branching Logic | Non-mandatory | Defines conditional display logic for the variable |
| M | Required Field? | Non-mandatory | Makes the variable required before the form can be saved |
| N | Custom Alignment | Non-mandatory | Adjusts how the variable is displayed relative to others |
| O | Question Number (surveys only) | Non-mandatory | Adds a custom question number in survey mode |
| P | Matrix Group Name | Matrix fields | Groups radio/checkbox variables into a matrix |
| Q | Matrix Ranking? | Matrix fields | Flags a radio matrix as a ranking matrix |
| R | Field Annotation | Non-mandatory | Stores designer notes and/or action tag codes |

---

# 5. Column-by-Column Reference

## 5.1 Column A — Variable / Field Name (Mandatory)

The Variable Name is the unique internal identifier used throughout REDCap to store and reference the variable. It appears in branching logic expressions, calculation formulas, exports, API calls, piping, and smart variables.

**Rules:**

| Rule | Result if broken |
|---|---|
| Lowercase letters, numbers and underscores only | **Warning** — REDCap converts the name for you (uppercase to lowercase, spaces to underscores, other characters removed; in Development, double underscores become single). Check the converted name in the warning. |
| Must not start with a number or an underscore | Error |
| Must not end with an underscore | Error |
| Must not contain three underscores in a row (`___`) — reserved for checkbox export columns | Error |
| Must be unique across the entire project (not just within an instrument) | Error |
| Longer than 26 characters | Warning (allowed, but discouraged) |
| Longer than 100 characters | Error |
| Must not be a REDCap reserved name, or an instrument name followed by `_complete` or `_timestamp` | Error |

There is no minimum length: a one-letter variable name is accepted.

**Do not:**
- Change a variable name after data collection has begun. To REDCap, a renamed variable is a new, empty variable, and the old one is removed. The old variable's data is no longer accessible in forms, reports or exports. REDCap does not purge it, though, and it can come back if a variable with the old name is created again.

**Example from practice:**
`date_enrolled`, `first_name`, `dob`, `bmi`

---

## 5.2 Column B — Form Name (Mandatory)

The Form Name determines which instrument a variable belongs to. All variables sharing the same Form Name are grouped together as one instrument. The order of instruments in REDCap is determined by the order in which new Form Names first appear in the Data Dictionary.

**Rules:**
- Use lowercase letters, numbers, and underscores in the CSV. REDCap allows the display name to be changed to include spaces and capitalization after import. If the name contains other characters, starts with a number, or has leading, trailing or double underscores, REDCap cleans it up and reports a **warning** with the new name.
- Longer than 50 characters is a warning; longer than 64 characters is an error (unless the instrument already exists with that name).
- All variables belonging to the same instrument must be grouped together sequentially.

**Do not:**
- Use special characters — REDCap will rename the instrument, which may not be the name you expected.
- Interleave rows from different instruments — all rows for a given form must be contiguous. Interleaved rows are an upload **error**.

**Tip:** To split one instrument into two, change the Form Name for a subset of variables to a new value. REDCap creates the new instrument automatically on upload. To merge two instruments, change all variables in the second instrument to match the Form Name of the first.

---

## 5.3 Column C — Section Header (Non-mandatory)

A Section Header creates a labeled divider bar above the variable it is assigned to. It is used to visually organize long instruments and can create page breaks in survey mode.

**Rules:**
- Any text is allowed, including HTML for formatting.
- Assign the section header to the first variable in the group you want to label — not to a standalone row.
- Section headers are linked to the variable in the same row; if that variable has branching logic, the section header appears and disappears with it.

**Do not:**
- Create a dedicated row just for the section header — there is no "section header field type." The value goes in Column C of an existing variable row.
- Assume special characters will display correctly in all browsers without testing.

---

## 5.4 Column D — Field Type (Mandatory)

The Field Type determines how REDCap renders the variable in data entry and survey mode, and which other columns apply to it.

**Allowed shorthand codes:**

| Code | Description |
|------|-------------|
| `text` | Single-line free text; supports validation |
| `notes` | Multi-line free text; no validation |
| `dropdown` | Single-select from a defined list; displayed as a drop-down menu |
| `radio` | Single-select from a defined list; displayed as radio buttons |
| `checkbox` | Multi-select from a defined list |
| `calc` | Calculated field; value is computed from a formula |
| `file` | File upload field |
| `descriptive` | Static text or image; no data is collected |
| `slider` | Visual analog scale (default range 0–100; set a custom range in columns I/J); supports optional numeric display |
| `yesno` | Built-in Yes/No radio; no choices column needed |
| `truefalse` | Built-in True/False radio; no choices column needed |

> **Important:** Do not use the `sql` field type. This is reserved for REDCap system administrators. Do not edit existing `sql` rows. See [RC-FD-12 — Dynamic SQL Field Type](RC-FD-12_Dynamic-SQL-Field-Type.md) for full documentation on this field type.

---

## 5.5 Column F — Choices, Calculations, or Slider Labels (Conditionally Mandatory)

This column serves three distinct purposes depending on the field type:

**For `dropdown`, `radio`, and `checkbox` fields:** Define the answer choices using pipe-separated pairs of raw value and display label.

```
raw_value, Display Label | raw_value, Display Label | raw_value, Display Label
```

Example: `0, No | 1, Yes | 98, Unknown`

- REDCap splits each choice at its **first** comma: everything before it is the raw value, everything after it is the label. Commas inside a label are therefore fine (`1, Yes, confirmed` gives raw value `1` and label `Yes, confirmed`), but a raw value can never contain a comma.
- Raw values must be a number (negative and decimal numbers are allowed) or contain only letters, numbers, periods, underscores and hyphens. Any other character (a space, for example) is an upload **error**, and REDCap suggests a corrected code.
- Duplicate raw values within one variable are an **error**.
- A `dropdown` or `radio` with only one choice gets a **warning** (a single-choice `checkbox` is accepted silently).
- A blank Column F on a `dropdown`, `radio` or `checkbox` is a **warning**, not an error: the upload goes through and the variable has no choices to select.
- Labels can contain any text, including HTML.
- The raw value is what is stored in the database and used in logic; the label is what participants and data entry users see.
- For `notes`, `file`, `yesno`, `truefalse` and `descriptive` fields, REDCap clears anything you put in Column F.

**For `calc` fields:** Enter a calculation formula using the same syntax as branching logic. The formula must resolve to a numeric value, not a true/false statement. A blank formula is an **error**, and so is a reference to a variable that is not in Column A, unbalanced brackets or parentheses, or a syntax error in the formula.

Example: `round(datediff([dob],'today','y'),0)` (calculates age in years)

**For `slider` fields:** Optionally provide one, two, or three labels for the left endpoint, midpoint, and right endpoint.

```
Left label | Right label
Left label | Middle label | Right label
```

**Do not:**
- Leave this column blank for dropdown, radio, or checkbox fields — the upload goes through with only a warning, leaving a variable nobody can answer.
- Include a comma within a raw value — REDCap treats everything after the first comma as the label.

---

## 5.6 Column G — Field Note (Non-mandatory)

The Field Note displays a short instructional text below the variable in both survey and data entry mode. It is commonly used to specify date formats, units of measure, or other brief instructions.

**Rules:**
- Any text is allowed, including HTML.
- Keep notes brief — long notes clutter the interface and are rarely read.

**Example from practice:** A date field with validation `date_ymd` might have a field note of `YYYY-MM-DD` to prompt the correct format.

---

## 5.7 Column H — Text Validation Type or Show Slider Number (Non-mandatory)

For `text` fields, this column sets the validation format. REDCap will only accept values matching the specified format.

**Allowed validation shorthand codes include:**

| Code | Validates |
|------|-----------|
| `date_ymd` | Date in YYYY-MM-DD format |
| `date_mdy` | Date in MM-DD-YYYY format |
| `date_dmy` | Date in DD-MM-YYYY format |
| `datetime_ymd` | Date and time |
| `number` | Any numeric value |
| `integer` | Whole numbers only |
| `email` | Email address format |
| `phone` | US phone number format |
| `zipcode` | US ZIP code format |
| `mrn_10d` | 10-digit medical record number |
| `signature` | Marks a `file` field as a classic (drawn) Signature field |
| `enhanced_signature` | Marks a `file` field as an Enhanced Signature field — typed or drawn *(17.1.0+)* |
| `audio` / `video` | Marks a `file` field as an audio or video recording field *(newer Standard releases only — see the caveat below)* |
| `autocomplete` | On a `dropdown` field, turns the drop-down into a type-ahead search box |

- Codes are case-insensitive in the file: REDCap converts them to lowercase and reports a **warning**.
- The older codes `int`, `float`, `date`, `datetime` and `datetime_seconds` are still accepted and converted to `integer`, `number`, `date_ymd`, `datetime_ymd` and `datetime_seconds_ymd`.
- Validation types that your administrator has hidden from the Online Designer list are still accepted on upload.
- An unknown code is an upload **error**.

> **Version caveat (file field codes differ by release):** Which Column H values a `file` field accepts depends on the version. 16.0 LTS accepts only `signature`. 17.3 LTS also accepts `enhanced_signature`. 17.6 Standard also accepts `audio` and `video`. Anything else on a `file` field is an upload **error**, so a dictionary exported from a newer instance can fail on an older one. Before moving a dictionary between instances, check the target's version and clear or change any Column H values on `file` rows that it does not support.

> **Note:** The date codes describe the *entry and display* format enforced on the instrument, not the storage format. REDCap stores all dates as YYYY-MM-DD and the API returns them that way regardless of which validation code the field carries — a `date_mdy` field exports as `2026-04-30`. (Verified by API export, REDCap v17, 2026-09.) A user's own date display preference can change how dates appear in an interface download, but not what is stored or what the API returns.

For `slider` fields, entering `number` in this column displays the current numeric value next to the slider handle.

> **Important:** Leave this column empty for field types other than `text`, `slider`, `file` and (for `autocomplete` only) `dropdown`. A value on any other field type is an upload **error**.
>
> The `file` case is the one people miss: signature fields are **not** a separate field type. A **classic Signature** is `file` + `signature`, and an **Enhanced Signature** is `file` + `enhanced_signature`. Converting between them is a change to this column alone — the field type stays `file`. See [RC-FD-06 — Online Designer: Instrument & Field Management](RC-FD-06_Online-Designer-Instrument-and-Field-Management.md) §8.8.

---

## 5.8 Columns I & J — Text Validation Min / Text Validation Max (Non-mandatory)

These two columns define acceptable lower and upper bounds for validated `text` fields, and the range of `slider` fields. Both are optional — you may set a minimum only, a maximum only, or both.

**For `slider` fields:** the columns set the slider's lower and upper bound — e.g. `0` and `10` for a 0–10 scale. Left empty, a slider runs from 0 to 100. The Column F labels (left, middle, right) are placed along whatever range you set. (Verified by Data Dictionary export, REDCap 16.0.49 LTS, 2026-10.)

**Rules:**
- The value entered must match the validation type. For a `date_ymd` field, enter dates in YYYY-MM-DD format; for a `number` or `integer` field, enter numeric values. A value that does not match is an upload **error**.
- Date and datetime min/max can also be typed as M/D/Y or D/M/Y (with slashes). REDCap converts them using the date format you pick on the upload page, so make sure that choice matches your file.
- Instead of a fixed value, a `text` field's min or max can be `today`, `now`, or a variable in square brackets such as `[visit_date]`.
- A `slider`'s min and max must be whole numbers; anything else is an **error**.
- Min or max on a `text` field with **no** validation type in Column H is an **error**.
- Build in a reasonable buffer to accommodate outliers rather than setting hard biological or logical limits that legitimate data could exceed.

**Do not:**
- Populate these columns for field types other than validated `text` and `slider`. On other types (`radio`, `checkbox`, `calc` and so on) the upload does not fail, but the values are stored and ignored, which misleads anyone reading the dictionary later.

**Example from practice:** A height field validated as `number` might have a min of `130` and a max of `215` (centimeters). A pain-rating slider might use `0` and `10`, with Column F labels `No pain | | Worst pain`.

---

## 5.9 Column K — Identifier? (Non-mandatory)

Flagging a variable as an identifier affects how data is handled during export. Identifier-flagged variables are removed from exports for users with **De-Identified** export rights and whenever **Remove All Identifier Fields** is chosen.

**Allowed values:**
- `y` or `Y` — flag as identifier
- Blank — not an identifier

**Do not:**
- Mark every variable as an identifier. Apply the flag only to variables that directly identify a participant: name, date of birth, contact information, addresses, government IDs, and similar.
- Use any value other than `y`. Anything else (`yes`, `1`, `x`) is blanked with a **warning**, so the variable ends up *not* flagged.

---

## 5.10 Column L — Branching Logic (Non-mandatory)

Branching logic controls whether a variable is displayed based on the value of other variables. The syntax is identical to branching logic in the Online Designer.

**Key syntax rules:**
- Reference variable values with square brackets: `[variable_name]`
- Use single quotes for string comparisons: `[sex] = '0'`. Double quotes are also accepted as long as they are balanced; an odd number of quote marks is an upload **error**. Single quotes are still the safer habit, because they avoid CSV escaping problems.
- Combine conditions with `and` / `or`.
- For longitudinal projects, reference event-specific values: `[baseline_arm_1][dob]`
- Every variable referenced in square brackets must exist in Column A (or be an instrument's `_complete` status field); a reference to a missing variable is an upload **error**, as is a syntax error in the logic.

**Tip:** For bulk logic changes, use Excel's Find & Replace or cell references to craft logic across many rows efficiently. See Section 7 for advanced Excel techniques.

> **Cross-reference:** See [RC-BL-01 — Branching Logic: Overview & Scope](RC-BL-01_Branching-Logic-Overview-and-Scope.md) — [RC-BL-04 — Branching Logic: Structured Fields & Checkboxes](RC-BL-04_Branching-Logic-Structured-Fields-and-Checkboxes.md) for comprehensive branching logic syntax documentation.

---

## 5.11 Column M — Required Field? (Non-mandatory)

Marking a variable as required makes REDCap check that the variable has a value when the instrument is saved. It does not affect data exports. The check behaves differently on data entry forms and surveys:

- **Data entry forms:** a missing required value does **not** stop the save. The record is saved, and REDCap then tells the user which required fields are empty.
- **Surveys:** the participant cannot move on or submit the page until the required fields are answered.

For a `checkbox` field, don't rely on **Required** to force a selection: in practice it does not reliably make the user tick at least one option. If at least one option must be chosen, test the behaviour on your own server, or add a separate check (for example a data quality rule or a warning field shown by branching logic when no option is ticked).

**Allowed values:**
- `y` or `Y` — required
- Blank — optional

Any other value is blanked with a **warning** (the variable ends up optional). `y` on a `descriptive` field is also blanked with a warning, since there is nothing to answer.

**Do not:**
- Make a variable required without providing a clearly labeled "not applicable" or exit option for cases where a valid answer genuinely cannot be given.

---

## 5.12 Column N — Custom Alignment (Non-mandatory)

Custom alignment adjusts how REDCap renders a variable on the form. The code is a two-letter combination: the first letter controls field width (L = full-width, R = half-width); the second controls choice orientation (V = stacked vertically, H = inline horizontally). The second letter only has a visible effect on fields that display selectable choices.

**Allowed codes:**

| Code | Width | Choice orientation | Default? |
|------|-------|--------------------|----------|
| `RV` | Half-width | Choices stacked vertically | Yes — applied when blank |
| `LV` | Full-width | Choices stacked vertically | No |
| `LH` | Full-width | Choices inline horizontally | No |
| `RH` | Half-width | Choices inline horizontally | No |

**What "Left" and "Right" mean in practice**

The L/R letter controls how much horizontal space the variable occupies. REDCap uses a two-column layout:

- **`LH` and `LV`** — the variable spans the full width of the form (both columns merged into one).
- **`RH` and `RV`** — the variable occupies approximately half the form width, with the label and input each in a separate column.

**What "Vertical" and "Horizontal" mean in practice**

The V/H letter controls how selectable answer choices are arranged. It has a visible effect on fields that have choices (`radio`, `checkbox`, `yesno`, and `truefalse`) and on `slider` fields, where it sets the direction of the slider bar.

- **V** — each choice is a block-level element displayed on its own line (stacked vertically).
- **H** — choices are inline elements displayed side by side in a horizontal row.

On a `slider`, **V** draws the bar vertically (up and down) and **H** draws it horizontally (left to right).

For all other field types (`text`, `notes`, `dropdown`, `calc`, `file`), V and H produce identical rendering. `LV` and `LH` look the same; `RV` and `RH` look the same.

**Effect on specific field types**

- **`text`, `notes`, `dropdown`, `calc`, `file`:** Only the L/R letter has any visual effect. Width changes are most noticeable on `notes` — a Right-aligned notes box is roughly half the page width, which is narrow and awkward to type in. The V/H letter has no effect on these types; `LV` and `LH` are interchangeable, as are `RV` and `RH`.
- **`radio`, `checkbox`, `yesno`, `truefalse`:** Both letters affect rendering. L/R controls full vs. half width; V/H controls whether choices stack vertically or run horizontally. Choose H for short lists (2–4 choices) and V for longer lists.
- **`slider`:** Both letters affect rendering. L/R controls full vs. half width; V/H controls the bar's direction: V gives a vertical bar, H a horizontal one. Use `LH` for a full-width horizontal slider, the layout most people expect for a rating scale.
- **`descriptive`:** Alignment has no visual effect. Descriptive fields always render at full width regardless of which code is entered.
- **`sql`:** Behaves identically to `dropdown` for alignment purposes.

**Interaction with Enhanced Radio Buttons and Checkboxes**

When the Enhanced Radios and Checkboxes survey setting is active (see [RC-SURV-02 — Survey Settings: Basic Options & Design](RC-SURV-02_Survey-Settings-Basic-Options-and-Design.md)), standard choice rendering is replaced with large block-style buttons. The alignment code continues to apply in enhanced mode:

- **V codes (RV, LV):** Enhanced buttons each fill the full container width, stacking one per row.
- **H codes (LH, RH):** Enhanced buttons are rendered in a two-column grid (approximately 50% width each), producing a side-by-side layout on medium and larger screens.
- The L/R width effect is also preserved — L codes produce a full-width container; R codes produce a half-width container.

**Practical guidance**

- Leave the column blank to accept the REDCap default (`RV`).
- For `notes` fields, prefer `LH` or `LV` to get full-width text areas.
- For `radio` and `checkbox`, choose H vs. V based on the number of choices: short lists (2–4 choices) are readable horizontally; longer lists are cleaner vertically.
- Consistency across an instrument improves readability. Mixing Left and Right fields in the same instrument can create a visually fragmented layout.

> **Important:** Use only these four codes, in uppercase, exactly as written. Any other value — including lowercase `lh` or `rv` — does not fail the upload: REDCap blanks it with a **warning**, and the variable falls back to the default `RV`.

> **Cross-reference:** See the project STYLE-GUIDE.md for team conventions on default alignment choices. See [RC-SURV-02 — Survey Settings: Basic Options & Design](RC-SURV-02_Survey-Settings-Basic-Options-and-Design.md) for documentation of the Enhanced Radio Buttons and Checkboxes survey setting.

---

## 5.13 Column O — Question Number (Non-mandatory, surveys only)

Question numbering adds a custom number prefix to a variable when displayed in survey mode. This is purely cosmetic and has no effect on data entry mode. The numbers are shown only on instruments enabled as surveys whose survey settings use custom question numbering; with automatic numbering, Column O is ignored.

**Rules:**
- Up to 10 characters. Longer values are cut to the first 10.

**Tip:** When branching logic creates conditional variables, use sub-numbers (e.g., `1a`, `1b`) to maintain a logical numbering sequence even when some questions are hidden.

**Do not:**
- Expect question numbers on non-survey instruments — they are not shown in data entry mode, so values there only clutter the dictionary.

---

## 5.14 Column P — Matrix Group Name (Matrix fields only)

The Matrix Group Name groups radio or checkbox variables into a matrix (grid) display. All variables sharing the same Matrix Group Name are rendered as rows in a table, with the answer choices as columns.

**Rules:**
- Use only lowercase letters, numbers, and underscores. Other characters are cleaned up with a **warning**.
- Longer than 60 characters is an **error**.
- Must be unique within the project (separate from variable names).
- All matrix variables must be sequential in the Data Dictionary; a group split by other rows is an **error**.
- All variables in a matrix must share the same answer choices defined in Column F.
- All variables in a matrix should share one field type. If a group mixes `radio` and `checkbox` rows, REDCap converts them to one type and reports a **warning** — check which type it chose.
- A section header placed on the first variable in a matrix becomes the matrix header.

**Do not:**
- Apply a Matrix Group Name to field types other than `radio` or `checkbox`.
- Create matrices with a very large number of choices — they render poorly on small screens.

---

## 5.15 Column Q — Matrix Ranking? (Matrix fields only)

Flags whether a radio matrix is a ranking matrix, where participants assign each row a unique rank.

**Allowed values:**
- `y` or `Y` — ranking matrix
- Blank — standard matrix

Any other value is blanked with a **warning**. Every row in the group must carry the same Column Q value; a group where some rows say `y` and others are blank is an upload **error**.

**Do not:**
- Apply ranking to `checkbox` matrices — ranking is only supported for radio matrices.

---

## 5.16 Column R — Field Annotation (Non-mandatory)

The Field Annotation column serves two purposes: it stores designer notes visible only in the Data Dictionary (not to participants or data entry users), and it holds action tag codes that modify variable behavior.

**Notes:** Any plain text is acceptable as a designer annotation.

**Action tag syntax:** Action tags begin with `@` and are entered as uppercase codes. Multiple action tags are separated by spaces.

**Commonly used action tags:**

| Tag | Effect |
|-----|--------|
| `@HIDDEN` | Hides the variable in both survey and data entry mode |
| `@HIDDEN-SURVEY` | Hides the variable in survey mode only |
| `@HIDDEN-FORM` | Hides the variable in data entry mode only |
| `@READONLY` | Makes the variable read-only in both modes |
| `@READONLY-SURVEY` | Makes the variable read-only in survey mode only |
| `@DEFAULT='value'` | Pre-fills the variable with a specified value |
| `@NOW` | Pre-fills with the current date and time |
| `@TODAY` | Pre-fills with today's date |
| `@PASSWORDMASK` | Masks input as asterisks |
| `@LATITUDE` / `@LONGITUDE` | Captures GPS coordinates |
| `@BARCODE` | Enables barcode scanning (mobile app) |

> **Important:** Format the cell as plain text before typing an action tag in Excel. If the cell is formatted as General and you type `@`, Excel may interpret it as a formula prefix and flag an error.

On upload through the Data Dictionary page, REDCap removes **one** leading space in front of an `@` (the space Excel users add to stop `@` being read as a formula). `@CALCTEXT` and `@CALCDATE` expressions in Column R are syntax-checked on upload; an invalid one is an **error**.

> **Version caveat (exported Column R cells, 16.0 LTS vs 17.3+):** When you download the Data Dictionary, REDCap protects spreadsheet users by putting an apostrophe in front of Column R cells that start with `=`, `+`, `-` or `@`. In 16.0 LTS this includes action tags, so exported cells look like `'@HIDDEN`. From 17.3 LTS, action tags are left alone. Either way, REDCap strips the added apostrophe when you upload the file again, so you do not need to remove it by hand — but do not add your own apostrophes, and expect the `'` when you open a 16.0 export in a text editor.

> **Cross-reference:** See [RC-AT-01 — Action Tags: Overview](RC-AT-01_Action-Tags-Overview.md) for a complete action tag reference.

---

# 6. Uploading and Validating the Data Dictionary

## 6.1 The Upload Workflow

The recommended Data Dictionary workflow has four stages:

1. **Download and back up** — download the current Data Dictionary from the Project Setup page or the Online Designer. Save a local copy labeled with the date before making any edits.
2. **Modify** — make changes in a spreadsheet application. Work only in one mode at a time (Data Dictionary or Online Designer) to prevent overwrites.
3. **Upload** — navigate to the Data Dictionary upload interface, select your modified CSV, and click Upload. REDCap validates the file and reports any errors with row-level detail. Correct errors and re-upload as needed.
4. **Commit** — once no critical errors are reported, review REDCap's change summary and confirm. Changes take effect immediately in Development mode. In Production mode, you must first enter **Draft Mode**; the upload changes the draft, and the draft then goes through the usual review and approval.

## 6.2 Using Snapshots

The Data Dictionary Snapshot feature allows you to save a named copy of the current instrument configuration directly in REDCap, separate from any local files you keep.

**Creating a snapshot:**

1. Navigate to the Online Designer.
2. Click "Create a snapshot of instruments."
3. *(17.5.0+)* Optionally enter a **comment** and attach a **file** — for example, the change request or protocol amendment that prompted the edit.

**Viewing revision history:**

All project history revisions are accessible from Project Setup → Project Revision History tab. Snapshot comments and attachments are shown there, and from 17.5.0 the comment can be edited afterwards on the same page.

A snapshot comment that names *why* the structure is about to change ("Before amendment 3 — adding AE follow-up instrument") is far more useful a year later than the timestamp alone.

**Automatic snapshots:** REDCap also takes a snapshot of the current design automatically just before it commits any Data Dictionary upload (and before any metadata import through the API). These appear on **Project Revision History** too, so if an upload goes wrong you can download the pre-upload Data Dictionary from there and upload it again to restore the design.

> **Note:** Snapshots are a convenience feature, not a substitute for downloading and storing local backups. Always maintain at least one local copy of the pre-edit Data Dictionary.

## 6.3 Validation Errors

REDCap's upload validator catches technical errors — invalid field type codes, malformed choice syntax, duplicate variable names, and similar issues. It does not assess whether the instrument design is clinically appropriate or logically sound. Common validation **errors** (which block the upload) include:

- A variable name that starts with a number or underscore, ends with an underscore, contains `___`, or is reserved (Column A)
- Duplicate variable names within the project
- Unknown field type code in Column D
- Rows from one instrument interleaved with another (Column B)
- Illegal or duplicate raw values in a choice list, or a blank or invalid calculation (Column F)
- Invalid validation code in Column H, or a Column H value on a field type that does not use it
- Min/max on a `text` field with no validation type, or a min/max that does not match the validation type (Columns I/J)
- Branching logic or calculations that reference a variable not in Column A

Common **warnings** (the upload goes through, often with REDCap changing your value) include:

- Uppercase letters, spaces or special characters in a variable, form or matrix group name (converted automatically)
- Variable names longer than 26 characters
- Blank Field Label, or blank choices on a `dropdown`, `radio` or `checkbox`
- Unrecognised values in Columns K, M, N or Q (blanked)

> **Version caveat (16.0 LTS):** In 16.0 LTS, REDCap administrators (super users) uploading a dictionary get some branching logic syntax errors reported as warnings instead, so an administrator's upload can succeed where a regular user's would be blocked. If an administrator uploads on your behalf on 16.0, review branching logic afterwards.

---

# 7. Excel Techniques for Efficient Data Dictionary Editing

Working efficiently in Excel can significantly reduce the time required to build or modify large data dictionaries.

## 7.1 Freeze Panes

Freezing panes keeps the header row and variable name column visible as you scroll through large files.

1. Navigate to the **View** tab.
2. Select cell **B2**.
3. Click **Freeze Panes**.

With B2 selected as the anchor, Row 1 (headers) and Column A (variable names) remain fixed while you scroll right and down.

## 7.2 Sorting and Filtering

Sorting on Form Name (Column B) groups all variables by instrument, making bulk changes faster. Sorting on Field Type (Column D) lets you quickly locate and modify all variables of a given type.

> **Warning:** Always save a backup before sorting. If you sort and accidentally delete rows before re-saving, the upload will remove those variables from the project, and their data will no longer be accessible in forms, reports or exports. Verify row counts before uploading after any sort operation.

## 7.3 Find and Replace

Use Excel's Find & Replace (`Ctrl+H` / `Cmd+H`) to update variable names, branching logic expressions, or choice values across many rows simultaneously. This is particularly useful when renaming a variable that appears in branching logic throughout the file.

## 7.4 Crafting Dynamic Branching Logic with Cell References

When the same branching logic pattern repeats across many rows with only a variable name changing, you can use cell references to have Excel construct the logic string automatically. For example, if Column A contains the variable name and you want Column L to contain `[variable_name_from_col_a] = '1'`, a formula in Column L referencing Column A can generate this across hundreds of rows at once.

## 7.5 Auto-Fill Variable Names

Excel's **Fill Series** feature can automatically increment variable names that end in a number. For a series like `symptom_1`, `symptom_2`, `symptom_3`:

1. Enter `symptom_1` in the first cell.
2. Select the cell and drag the fill handle down (or use Fill → Series).
3. Excel increments the trailing number automatically.

This works only when the variable name ends in a number.

---

# 8. Best Practices

## 8.1 Mobile and Small-Screen Considerations

REDCap instruments are often accessed on smartphones and tablets, particularly in clinical settings. To optimize for mobile:

- Prefer field types that are touch-friendly: `radio`, `checkbox`, `dropdown`, `yesno`, `truefalse`, and `slider` work well on touchscreens. Long `text` and `notes` fields are more cumbersome to complete on mobile.
- Keep questions short and labels concise.
- Limit matrices on mobile — wide matrices truncate or require horizontal scrolling.
- Limit instruments to 500 variables or fewer for use in the REDCap Mobile App. Instruments with many calculations and branching logic expressions should be kept well below this limit.
- Test your instruments on a real device before deploying.

> **Note:** The REDCap Mobile App has limited functionality compared to the browser interface due to its offline-first design. Features such as Ontology Lookup (Bioportal) do not function offline.

## 8.2 Longitudinal Project Considerations

In longitudinal projects, the Data Dictionary defines the variables and instruments but does not assign instruments to events. Event assignment is managed separately in the longitudinal setup. Keep these points in mind when working with the Data Dictionary in a longitudinal project:

- **Splitting and merging instruments** is done in the Data Dictionary by changing Form Name (Column B). This is the fastest way to restructure instruments in bulk. The Online Designer can also move individual fields, or a whole matrix, to another instrument or to a new one.
- **The Record ID variable** must always be in the first instrument and must be assigned to the first event in longitudinal setup. Do not move it.
- **Branching logic in longitudinal projects** often needs event identifiers: `[baseline_arm_1][dob]` references the value of `dob` collected at the `baseline_arm_1` event. Without the event identifier, REDCap uses the value from the current event, which may not be the intended behavior.

---

# 9. Common Questions

**Q: What exactly does REDCap delete when I upload a Data Dictionary that is missing some rows?**

**A:** Any variable present in the current project but absent from the uploaded CSV is removed from the project. Its data is no longer accessible in forms, reports or exports. REDCap does not purge it, and it can reappear if a field with the same variable name is created again — so deleting a field is not a way to remove sensitive data, and avoid reusing old variable names for something new.

In Production, the draft review warns you if variables that hold data are about to be removed; in Development there is no such warning. If an upload removed variables by mistake, download the automatic snapshot taken just before the upload from **Project Revision History** and upload it again (see Section 6.2). Removing or renaming an *instrument* is different: its event designations, locking, e-signatures, repeating setting and instrument-level user rights are deleted permanently (see Section 3.2). Always download a backup and verify your row count before uploading.

**Q: What is the difference between `dropdown` and `radio`?**

**A:** Both field types allow single-select from a defined list and use the same choices syntax (Column F). The difference is purely visual: `dropdown` renders as a compact drop-down menu (better when there are many choices), while `radio` renders all choices as visible radio buttons (better for short lists where seeing all options at once is helpful).

**Q: Can I add or change action tags using the Online Designer instead of the Data Dictionary?**

**A:** Yes. The Online Designer's field editor includes a Field Annotation box where you can add or edit action tags for individual variables. The Data Dictionary is more efficient when you need to add the same action tag to many variables at once.

**Q: Can I use the Data Dictionary to rename an instrument?**

**A:** Partially. Changing the value in Column B (Form Name) changes the internal instrument identifier. REDCap also allows you to separately set a display name (with spaces and capitalization) in the Online Designer after import. If you change the Form Name for an existing instrument, REDCap treats it as a new instrument — the old one is deleted if no variables remain assigned to it. The variables and their data carry over, but the old instrument's event designations, locking records, e-signatures, repeating setting and instrument-level user rights are deleted (see Section 3.2). To change only the name people see, rename the instrument in the Online Designer instead.

**Q: My upload was rejected with a validation error in Column F. What is the most likely cause?**

**A:** The most common causes are: (1) a raw value containing a character other than letters, numbers, periods, underscores and hyphens (a space, for example — remember that REDCap splits each choice at its first comma, so `yes no, Yes or no` gives the illegal raw value `yes no`), (2) the same raw value used twice in one list, or (3) a calc field with a blank or invalid formula. A comma inside a *label* (`1, Yes, confirmed`) is fine, and a blank choices column on a dropdown, radio or checkbox is only a warning.

**Q: My branching logic worked in the Online Designer but REDCap rejected it in the Data Dictionary upload. Why?**

**A:** The most common causes are a reference to a variable that is not in Column A of your file (for example, one you renamed or removed), and quote marks that do not pair up. Balanced double quotes are accepted, but CSV escaping in a spreadsheet can easily leave an odd number of `"` in the cell; using single quotes for string values avoids the problem.

**Q: Can I include HTML in the Field Label or Field Note columns?**

**A:** Yes. Both columns support HTML formatting. Common uses include `<b>bold</b>` for emphasis, `<br>` for line breaks, and `<i>italic</i>`. Test HTML rendering in both survey mode and data entry mode, as display may differ slightly.

REDCap has progressively widened the set of permitted tags in user input such as field labels and survey instructions: **`<blockquote>`** from 15.0.1, **`<wbr>`** from 15.4.5, and **`<ruby>`** from 15.5.6. If a tag renders as literal text rather than taking effect, check whether the instance is old enough to predate its support.

> **Important — user-supplied HTML is a recurring attack surface.** Stored XSS vulnerabilities have repeatedly been found in exactly these fields. That is not a reason to avoid HTML in labels, but it is a reason to keep the instance patched and to be wary of pasting markup from untrusted sources into a project. See [RC-INFRA-03 — REDCap Versions, Release Lines & Patching](RC-INFRA-03_REDCap-Versions-Release-Lines-and-Patching.md).

---

# 10. Common Mistakes & Gotchas

**Formatting Column R before typing an action tag.** Excel interprets cells beginning with `@` as formula errors if the cell is formatted as General. Before entering any action tag, right-click the cell, select Format Cells, and set the format to Text. If you have already encountered the error, delete the cell content, reformat, and retype.

**Sorting or filtering without verifying row count before save.** Sorting a filtered view can move rows out of the visible range, and re-saving a file while a filter is active may save only the visible rows. Before uploading, clear all filters, verify the total row count matches expectations, and check that Row 1 (headers) is still in position 1.

**Changing variable names after data collection begins.** Renaming a variable in Column A creates a new, empty variable and removes the old one. The old variable's data is no longer accessible in forms, reports or exports; REDCap does not purge it, and it can reappear if a variable with the old name is created again. Variable names must be treated as permanent once data collection is underway. Use the Field Annotation (Column R) for designer notes if you need to document what a variable represents without changing its name.

**Interleaving rows from different instruments.** All variables belonging to the same instrument must appear as a contiguous block in the Data Dictionary. If rows from two instruments are interleaved (e.g., `form_a`, `form_b`, `form_a`), REDCap rejects the upload with an error. Sort by Form Name (Column B) to verify grouping before uploading.

**Using the Data Dictionary and Online Designer simultaneously.** If you download a Data Dictionary, make edits in Excel, and then someone else makes changes in the Online Designer while you are editing, uploading your file will overwrite the Online Designer changes. Use only one design mode at a time and communicate with other project designers to avoid conflicts.

**Setting validation min/max for the wrong field type.** Columns I and J apply only to `text` fields that have a validation type set in Column H, and to `slider` fields. Min/max on a `text` field with no validation type is an upload error. On other types (`radio`, `checkbox`, `calc`) the upload does not fail, but the values are stored and ignored, so the range you meant to enforce is not enforced.

**Expecting "required" to block saving on data entry forms.** On a data entry form, a required variable left empty does not stop the save: the record is saved and the user is then told which required fields are missing. Only surveys hold the participant until required fields are answered. For a required `checkbox`, at least one box must be checked; this is enforced on both forms and surveys. If you need more than one box checked, no Column M value or action tag sets a minimum (`@MAXCHECKED` only caps the maximum), so catch it with a Data Quality rule or a validation calc field.

---

# 11. Annotated Example: Key Real-World Patterns

This section documents notable patterns observed in real Data Dictionary files. Use these as reference when building or reviewing a Data Dictionary from scratch.

## 11.1 Non-Numeric Raw Values in Choice Lists

The `|`-separated choices format (Column F) does not require numeric raw values. Raw values can be strings. A US state dropdown commonly uses two-letter postal codes as raw values:

```
AL, Alabama | AK, Alaska | AZ, Arizona | ...
```

The raw value (`AL`) is what gets stored in the database and referenced in branching logic: `[contact_state] = 'AL'`. The label (`Alabama`) is what the user sees. Either convention (numeric codes or string codes) is valid — pick one and be consistent within a project.

## 11.2 `@CALCTEXT` on a Text Field

`@CALCTEXT` is the action tag for `text` fields that need a calculated *text* result. The calculated value is displayed in the field and **saved**, just like a `calc` field's value, so it appears in reports and exports and can be used in logic. Use it when you need a computed label (e.g., a severity category derived from a score) that a numeric `calc` field cannot produce.

```
Field type:  text
Column R:    @CALCTEXT(if([phq9_total]>=20,"Severe",if([phq9_total]>=15,"Moderately Severe",if([phq9_total]>=10,"Moderate",if([phq9_total]>=5,"Mild","Minimal or None")))))
```

> **Note:** Double quotes inside `@CALCTEXT(...)` are valid within REDCap's expression engine. However, in the CSV file itself, the entire Column R cell must be wrapped in double quotes, and any literal double quotes inside the cell must be escaped as `""` (two double quotes). When REDCap reads the CSV, it resolves the `""` back to a single `"`.

## 11.3 Calc Fields with Branching Logic

`calc` fields support branching logic in Column L just like any other field type. When the branching logic condition is false, the calc field is hidden and its value is blank. This is useful for computations that only apply to a subset of participants:

```
Variable:           soc_pack_years
Field type:         calc
Column F (formula): [soc_smoking_packs_per_day] * [soc_smoking_years]
Column L (logic):   [soc_smoking_status] = '2' or [soc_smoking_status] = '3' or [soc_smoking_status] = '4'
```

The calc runs only when the participant is a former or current smoker; for never-smokers the field is hidden and the value is blank rather than zero.

> **Important:** Branching logic only controls what is *shown* on forms and surveys. When REDCap recalculates on the server (after a data import, or when you run the Data Quality rule that fixes incorrect calculated values), it ignores branching logic, so a hidden calc field can still hold a value. Write the condition into the formula itself (for example `if([soc_smoking_status] >= 2, [soc_smoking_packs_per_day] * [soc_smoking_years], '')`) if the value must be blank whenever the field is hidden.

## 11.4 Leading Whitespace in Column R Is Valid

A leading space before an action tag in Column R (`" @TODAY"` instead of `"@TODAY"`) is valid — REDCap strips leading and trailing whitespace from the annotation before parsing it. This frequently appears in real exported files because the Online Designer's annotation editor sometimes inserts a leading space. It does not cause an upload error.

## 11.5 PHQ-9 Matrix Pattern

Standardized instruments that use a uniform response scale map naturally to a matrix layout. All nine PHQ-9 items share identical choices and a single Matrix Group Name:

```
Variable:          phq9_1 … phq9_9
Field type:        radio
Column F (shared): 0, Not at all | 1, Several days | 2, More than half the days | 3, Nearly every day
Column P:          phq9_matrix
Column M:          y (required)
Question numbers:  1–9 (Column O)
```

Every row in the matrix block must carry the same Column F choices and the same Column P group name. The first row's Column C (Section Header) becomes the matrix header row label in REDCap.

## 11.6 Descriptive Fields as Summary Panels

A `descriptive` field can contain arbitrarily complex HTML, including inline CSS tables that pull piped values from multiple events. This pattern is used to surface a participant's longitudinal data all on one screen at the end of study. Key syntax elements:

- `[event_name][field_name]` — pipes the value of `field_name` from a specific event into the HTML
- `[field_name:hideunderscore]` — pipe modifier that replaces underscores with spaces in the displayed label
- Combined: `[baseline_arm_1][demo_age:hideunderscore]` — age from the baseline arm 1 event, displayed without underscores

Descriptive fields with heavy HTML and many piped values are the most complex rows in a Data Dictionary. Their Column E (Field Label) cell typically contains thousands of characters of HTML. When editing these in Excel, be aware that Excel's cell size limits and CSV quoting rules can corrupt the HTML if you do not work carefully with a plain-text editor.

## 11.7 Repeating Instrument Pre-Population with Nested `@IF`/`@DEFAULT`

When a repeating instrument appears at multiple longitudinal events, you may want each new instance to pre-fill its fields from the matching instance at the previous event (e.g., carrying a medication list forward). The pattern uses nested `@IF` blocks checking `[current-instance]` and reading from a prior event's named instances:

```
@IF([current-instance]=1 AND [prior_event_arm_1][med_name][1]<>'',
    @DEFAULT='[prior_event_arm_1][med_name][1]',
@IF([current-instance]=2 AND [prior_event_arm_1][med_name][2]<>'',
    @DEFAULT='[prior_event_arm_1][med_name][2]',
    @DEFAULT=''))
```

This nesting must be repeated for each instance you wish to pre-populate (typically up to the maximum expected number of instances). The placeholder `[prior_event_arm_1]` must be replaced with the actual unique event name for the preceding event in your project. REDCap reads `[current-instance]` at runtime, so the correct branch evaluates automatically.

> **Column R cell size warning:** This pattern produces very long annotation strings (often thousands of characters). These are valid but can exceed Excel's visible cell display limit. Use a text editor or verify the full string programmatically before uploading.

---

## API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) for authentication, token management, and setup.

- **[RC-API-06 — Export Field Names API](RC-API-06_Export-Field-Names.md)** — retrieve field variable names, export field names, and choice labels programmatically
- **[RC-API-07 — Export Metadata (Data Dictionary) API](RC-API-07_Export-Metadata.md)** — export the full data dictionary (all columns described in this article) programmatically
- **[RC-API-08 — Import Metadata (Data Dictionary) API](RC-API-08_Import-Metadata.md)** — import a CSV matching the column structure described in this article to update the project design

---


# 12. Related Articles

- [RC-FD-01 — Form Design Overview](RC-FD-01_Form-Design-Overview.md) (concept overview and tool selection)
- [RC-FD-02 — Online Designer](RC-FD-02_Online-Designer.md) (guardrailed alternative; use alongside the Data Dictionary)
- [RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md) (prerequisite; covers workflow, safety practices, and when to use the Data Dictionary)
- [RC-FD-05 — Codebook](RC-FD-05_Codebook.md) (reference for reviewing variable definitions without editing)
- [RC-BL-01 — Branching Logic: Overview & Scope](RC-BL-01_Branching-Logic-Overview-and-Scope.md) (required for Column L)
- [RC-BL-02 — Branching Logic: Syntax & Atomic Statements](RC-BL-02_Branching-Logic-Syntax-and-Atomic-Statements.md) (Column L syntax reference)
- [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md) (event setup, which the Data Dictionary does not cover)
- [RC-AT-01 — Action Tags: Overview](RC-AT-01_Action-Tags-Overview.md) (complete reference for Column R action tag codes)
- [RC-SURV-02 — Survey Settings: Basic Options & Design](RC-SURV-02_Survey-Settings-Basic-Options-and-Design.md) (Enhanced Radio Buttons setting and its interaction with Column N alignment codes)
- [RC-FD-12 — Dynamic SQL Field Type](RC-FD-12_Dynamic-SQL-Field-Type.md) (full documentation on the admin-only `sql` field type code)
