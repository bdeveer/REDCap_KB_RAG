RC-FD-08

**Data Dictionary: Column Reference & Advanced Techniques**

| **Article ID** | RC-FD-08 |
| --- | --- |
| **Domain** | Form Design |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Prerequisite** | RC-FD-03 — Data Dictionary |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-FD-01 — Form Design Overview; RC-FD-02 — Online Designer; RC-BL-01 — Branching Logic: Overview & Scope; RC-AT-01 — Action Tags: Overview |

---

# 1. Overview

This article is a 201-level reference for the REDCap Data Dictionary. It assumes familiarity with the Data Dictionary concept and basic workflow covered in RC-FD-03 — Data Dictionary. The article provides a complete column-by-column reference for all 18 Data Dictionary columns, explains which columns are mandatory versus optional, documents the allowed syntax and codes for each column, and covers advanced Excel techniques that make working with large data dictionaries faster and more reliable. It also addresses best practices specific to mobile data collection and longitudinal project designs.

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

The mandatory columns are A (Variable Name), B (Form Name), D (Field Type), and E (Field Label). Column F (Choices, Calculations, or Slider Labels) is conditionally mandatory depending on field type.

## Field Type

The field type determines how REDCap renders a variable on the data entry form and what additional columns apply to it. Only REDCap-supported shorthand codes are valid. See Section 3.4 for the full list of accepted field type codes.

## Matrix

A matrix is a grid of variables that share the same answer choices, displayed as a table in REDCap. Matrix variables must be of type `radio` or `checkbox`, must be sequential in the Data Dictionary, must share the same choices, and must all reference the same Matrix Group Name (Column P).

## Action Tags

Action tags are special codes entered in the Field Annotation column (Column R) that modify how a variable behaves in surveys or data entry. They begin with the `@` symbol. Multiple action tags can be applied to a single variable by separating them with spaces.

## Identifier Flag

Marking a variable as an identifier (Column K) does not change how data is entered or stored within REDCap. It affects the data export: variables flagged as identifiers are excluded by default when users export de-identified data. The flag is a documentation and governance tool, not an access control.

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

---

# 4. Data Dictionary Structure

## 4.1 Row Structure

Each row in the Data Dictionary defines exactly one variable. Exceptions:

- **Row 1** contains the column headers. Do not edit or delete row 1.
- **Row 2** defines the REDCap Record ID variable. This row is mandatory in every project. The Record ID variable is always the first variable in the first form and must be of field type `text`.

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
- Use only lowercase letters, numbers, and underscores.
- Must be at least 2 characters long.
- Must be unique across the entire project (not just within an instrument).
- Maximum recommended length: 26 characters.

**Do not:**
- Start the name with a number.
- Use special characters (`#`, `$`, `%`, `!`, `?`, spaces, etc.).
- Change a variable name after data collection has begun — renaming creates a new variable and deletes the old one, including its data.

**Example from practice:**
`date_enrolled`, `first_name`, `dob`, `bmi`

---

## 5.2 Column B — Form Name (Mandatory)

The Form Name determines which instrument a variable belongs to. All variables sharing the same Form Name are grouped together as one instrument. The order of instruments in REDCap is determined by the order in which new Form Names first appear in the Data Dictionary.

**Rules:**
- Use lowercase letters, numbers, and underscores in the CSV. REDCap allows the display name to be changed to include spaces and capitalization after import.
- Must be at least 2 characters long.
- All variables belonging to the same instrument must be grouped together sequentially.

**Do not:**
- Use special characters.
- Interleave rows from different instruments — all rows for a given form must be contiguous.

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
| `slider` | Visual analog scale (0–100); supports optional numeric display |
| `yesno` | Built-in Yes/No radio; no choices column needed |
| `truefalse` | Built-in True/False radio; no choices column needed |

> **Important:** Do not use the `sql` field type. This is reserved for REDCap system administrators. Do not edit existing `sql` rows.

---

## 5.5 Column F — Choices, Calculations, or Slider Labels (Conditionally Mandatory)

This column serves three distinct purposes depending on the field type:

**For `dropdown`, `radio`, and `checkbox` fields:** Define the answer choices using pipe-separated pairs of raw value and display label.

```
raw_value, Display Label | raw_value, Display Label | raw_value, Display Label
```

Example: `0, No | 1, Yes | 98, Unknown`

- Raw values must be numeric or alphanumeric; do not include commas within a raw value.
- Labels can contain any text, including HTML.
- The raw value is what is stored in the database and used in logic; the label is what participants and data entry users see.

**For `calc` fields:** Enter a calculation formula using the same syntax as branching logic. The formula must resolve to a numeric value, not a true/false statement.

Example: `round(datediff([dob],'today','y'),0)` (calculates age in years)

**For `slider` fields:** Optionally provide one, two, or three labels for the left endpoint, midpoint, and right endpoint.

```
Left label | Right label
Left label | Middle label | Right label
```

**Do not:**
- Leave this column blank for dropdown, radio, or checkbox fields — the upload will fail or produce unusable fields.
- Include a comma within a raw value — this will break the CSV parsing.

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

For `slider` fields, entering `number` in this column displays the current numeric value next to the slider handle.

> **Important:** Do not populate this column for field types other than `text` or `slider`. REDCap will reject the upload.

---

## 5.8 Columns I & J — Text Validation Min / Text Validation Max (Non-mandatory)

These two columns define acceptable lower and upper bounds for validated `text` fields. Both are optional — you may set a minimum only, a maximum only, or both.

**Rules:**
- The value entered must match the validation type. For a `date_ymd` field, enter dates in YYYY-MM-DD format; for a `number` or `integer` field, enter numeric values.
- Build in a reasonable buffer to accommodate outliers rather than setting hard biological or logical limits that legitimate data could exceed.

**Do not:**
- Populate these columns for non-text or non-validated field types.

**Example from practice:** A height field validated as `number` might have a min of `130` and a max of `215` (centimeters).

---

## 5.9 Column K — Identifier? (Non-mandatory)

Flagging a variable as an identifier affects how data is handled during export. Identifier-flagged variables are excluded from de-identified data exports by default.

**Allowed values:**
- `y` — flag as identifier
- Blank — not an identifier

**Do not:**
- Mark every variable as an identifier. Apply the flag only to variables that directly identify a participant: name, date of birth, contact information, addresses, government IDs, and similar.
- Use any value other than `y`.

---

## 5.10 Column L — Branching Logic (Non-mandatory)

Branching logic controls whether a variable is displayed based on the value of other variables. The syntax is identical to branching logic in the Online Designer.

**Key syntax rules:**
- Reference variable values with square brackets: `[variable_name]`
- Use single quotes for string comparisons: `[sex] = '0'`
- Do not use double quotes — REDCap will not accept the upload.
- Combine conditions with `and` / `or`.
- For longitudinal projects, reference event-specific values: `[baseline_arm_1][dob]`

**Tip:** For bulk logic changes, use Excel's Find & Replace or cell references to craft logic across many rows efficiently. See Section 7 for advanced Excel techniques.

> **Cross-reference:** See RC-BL-01 — RC-BL-04 for comprehensive branching logic syntax documentation.

---

## 5.11 Column M — Required Field? (Non-mandatory)

Marking a variable as required prevents the instrument from being saved as Complete until the variable has a value. It does not affect data exports.

**Allowed values:**
- `y` — required
- Blank — optional

**Do not:**
- Make `checkbox` fields required — REDCap cannot enforce "at least one selected" as a required constraint.
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

The V/H letter controls how selectable answer choices are arranged. It only has a visible effect on fields that have choices: `radio`, `checkbox`, `yesno`, and `truefalse`.

- **V** — each choice is a block-level element displayed on its own line (stacked vertically).
- **H** — choices are inline elements displayed side by side in a horizontal row.

For all other field types (`text`, `notes`, `dropdown`, `calc`, `file`, `slider`), V and H produce identical rendering. `LV` and `LH` look the same; `RV` and `RH` look the same.

**Effect on specific field types**

- **`text`, `notes`, `dropdown`, `calc`, `file`, `slider`:** Only the L/R letter has any visual effect. Width changes are most noticeable on `notes` — a Right-aligned notes box is roughly half the page width, which is narrow and awkward to type in. The V/H letter has no effect on these types; `LV` and `LH` are interchangeable, as are `RV` and `RH`.
- **`radio`, `checkbox`, `yesno`, `truefalse`:** Both letters affect rendering. L/R controls full vs. half width; V/H controls whether choices stack vertically or run horizontally. Choose H for short lists (2–4 choices) and V for longer lists.
- **`descriptive`:** Alignment has no visual effect. Descriptive fields always render at full width regardless of which code is entered.
- **`sql`:** Behaves identically to `dropdown` for alignment purposes.

**Interaction with Enhanced Radio Buttons and Checkboxes**

When the Enhanced Radios and Checkboxes survey setting is active (see RC-SURV-02), standard choice rendering is replaced with large block-style buttons. The alignment code continues to apply in enhanced mode:

- **V codes (RV, LV):** Enhanced buttons each fill the full container width, stacking one per row.
- **H codes (LH, RH):** Enhanced buttons are rendered in a two-column grid (approximately 50% width each), producing a side-by-side layout on medium and larger screens.
- The L/R width effect is also preserved — L codes produce a full-width container; R codes produce a half-width container.

**Practical guidance**

- Leave the column blank to accept the REDCap default (`RV`).
- For `notes` fields, prefer `LH` or `LV` to get full-width text areas.
- For `radio` and `checkbox`, choose H vs. V based on the number of choices: short lists (2–4 choices) are readable horizontally; longer lists are cleaner vertically.
- Consistency across an instrument improves readability. Mixing Left and Right fields in the same instrument can create a visually fragmented layout.

> **Important:** Use only these four codes exactly as written. Any other value will cause the upload to fail.

> **Cross-reference:** See the project STYLE-GUIDE.md for team conventions on default alignment choices. See RC-SURV-02 — Survey Settings: Basic Options & Design for documentation of the Enhanced Radio Buttons and Checkboxes survey setting.

---

## 5.13 Column O — Question Number (Non-mandatory, surveys only)

Question numbering adds a custom number prefix to a variable when displayed in survey mode. This is purely cosmetic and has no effect on data entry mode.

**Tip:** When branching logic creates conditional variables, use sub-numbers (e.g., `1a`, `1b`) to maintain a logical numbering sequence even when some questions are hidden.

**Do not:**
- Add question numbers to variables in non-survey instruments — they will appear in data entry mode, where they are irrelevant and confusing.

---

## 5.14 Column P — Matrix Group Name (Matrix fields only)

The Matrix Group Name groups radio or checkbox variables into a matrix (grid) display. All variables sharing the same Matrix Group Name are rendered as rows in a table, with the answer choices as columns.

**Rules:**
- Use only lowercase letters, numbers, and underscores.
- Must be at least 2 characters long.
- Must be unique within the project (separate from variable names).
- All matrix variables must be sequential in the Data Dictionary.
- All variables in a matrix must share the same answer choices defined in Column F.
- A section header placed on the first variable in a matrix becomes the matrix header.

**Do not:**
- Apply a Matrix Group Name to field types other than `radio` or `checkbox`.
- Create matrices with a very large number of choices — they render poorly on small screens.

---

## 5.15 Column Q — Matrix Ranking? (Matrix fields only)

Flags whether a radio matrix is a ranking matrix, where participants assign each row a unique rank.

**Allowed values:**
- `y` — ranking matrix
- Blank — standard matrix

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

> **Cross-reference:** See RC-AT-01 — Action Tags: Overview for a complete action tag reference.

---

# 6. Uploading and Validating the Data Dictionary

## 6.1 The Upload Workflow

The recommended Data Dictionary workflow has four stages:

1. **Download and back up** — download the current Data Dictionary from the Project Setup page or the Online Designer. Save a local copy labeled with the date before making any edits.
2. **Modify** — make changes in a spreadsheet application. Work only in one mode at a time (Data Dictionary or Online Designer) to prevent overwrites.
3. **Upload** — navigate to the Data Dictionary upload interface, select your modified CSV, and click Upload. REDCap validates the file and reports any errors with row-level detail. Correct errors and re-upload as needed.
4. **Commit** — once no critical errors are reported, review REDCap's change summary and confirm. Changes take effect immediately in Development mode. In Production mode, changes enter the pending approval queue.

## 6.2 Using Snapshots

The Data Dictionary Snapshot feature allows you to save a named copy of the current instrument configuration directly in REDCap, separate from any local files you keep.

**Creating a snapshot:**

1. Navigate to the Online Designer.
2. Click "Create a snapshot of instruments."

**Viewing revision history:**

All project history revisions are accessible from Project Setup → Project Revision History tab.

> **Note:** Snapshots are a convenience feature, not a substitute for downloading and storing local backups. Always maintain at least one local copy of the pre-edit Data Dictionary.

## 6.3 Validation Errors

REDCap's upload validator catches technical errors — invalid field type codes, malformed choice syntax, duplicate variable names, and similar issues. It does not assess whether the instrument design is clinically appropriate or logically sound. Common validation errors include:

- Invalid characters in Variable Name (Column A)
- Unknown field type code in Column D
- Missing choices for dropdown, radio, or checkbox fields (Column F)
- Invalid validation code in Column H
- Validation min/max populated for a non-validated field type
- Duplicate variable names within the project

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

> **Warning:** Always save a backup before sorting. If you sort and accidentally delete rows before re-saving, the upload will delete those variables from REDCap. Verify row counts before uploading after any sort operation.

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

- **Splitting and merging instruments** is done in the Data Dictionary by changing Form Name (Column B). This is the only way to restructure instruments in bulk — the Online Designer cannot move variables between instruments.
- **The Record ID variable** must always be in the first instrument and must be assigned to the first event in longitudinal setup. Do not move it.
- **Branching logic in longitudinal projects** often needs event identifiers: `[baseline_arm_1][dob]` references the value of `dob` collected at the `baseline_arm_1` event. Without the event identifier, REDCap uses the value from the current event, which may not be the intended behavior.

---

# 9. Common Questions

**Q: What exactly does REDCap delete when I upload a Data Dictionary that is missing some rows?**

A: Any variable present in the current project but absent from the uploaded CSV is deleted — including any data collected for that variable. REDCap warns you during the upload review if variables with existing data are about to be removed, but the deletion is irreversible once confirmed. Always verify your row count before uploading.

**Q: What is the difference between `dropdown` and `radio`?**

A: Both field types allow single-select from a defined list and use the same choices syntax (Column F). The difference is purely visual: `dropdown` renders as a compact drop-down menu (better when there are many choices), while `radio` renders all choices as visible radio buttons (better for short lists where seeing all options at once is helpful).

**Q: Can I add or change action tags using the Online Designer instead of the Data Dictionary?**

A: Yes. The Online Designer's field editor includes a Field Annotation box where you can add or edit action tags for individual variables. The Data Dictionary is more efficient when you need to add the same action tag to many variables at once.

**Q: Can I use the Data Dictionary to rename an instrument?**

A: Partially. Changing the value in Column B (Form Name) changes the internal instrument identifier. REDCap also allows you to separately set a display name (with spaces and capitalization) in the Online Designer after import. If you change the Form Name for an existing instrument, REDCap treats it as a new instrument — the old one is deleted if no variables remain assigned to it.

**Q: My upload was rejected with a validation error in Column F. What is the most likely cause?**

A: The most common causes are: (1) a comma embedded in a raw value (e.g., `1, Yes, confirmed` has a comma in the label preceding a pipe separator), (2) the column is blank for a dropdown, radio, or checkbox field, or (3) the choice list uses incorrect syntax (missing commas between raw values and labels, or missing pipe separators between choices).

**Q: My branching logic worked in the Online Designer but REDCap rejected it in the Data Dictionary upload. Why?**

A: The most common cause is using double quotes instead of single quotes around string values. The Online Designer accepts double quotes, but the Data Dictionary validator requires single quotes. Replace all `"` with `'` in Column L before uploading.

**Q: Can I include HTML in the Field Label or Field Note columns?**

A: Yes. Both columns support HTML formatting. Common uses include `<b>bold</b>` for emphasis, `<br>` for line breaks, and `<i>italic</i>`. Test HTML rendering in both survey mode and data entry mode, as display may differ slightly.

---

# 10. Common Mistakes & Gotchas

**Formatting Column R before typing an action tag.** Excel interprets cells beginning with `@` as formula errors if the cell is formatted as General. Before entering any action tag, right-click the cell, select Format Cells, and set the format to Text. If you have already encountered the error, delete the cell content, reformat, and retype.

**Sorting or filtering without verifying row count before save.** Sorting a filtered view can move rows out of the visible range, and re-saving a file while a filter is active may save only the visible rows. Before uploading, clear all filters, verify the total row count matches expectations, and check that Row 1 (headers) is still in position 1.

**Changing variable names after data collection begins.** Renaming a variable in Column A creates a new variable and deletes the old one — including all collected data for that variable. Variable names must be treated as permanent once data collection is underway. Use the Field Annotation (Column R) for designer notes if you need to document what a variable represents without changing its name.

**Interleaving rows from different instruments.** All variables belonging to the same instrument must appear as a contiguous block in the Data Dictionary. If rows from two instruments are interleaved (e.g., `form_a`, `form_b`, `form_a`), REDCap may create multiple instruments or assign variables incorrectly. Sort by Form Name (Column B) to verify grouping before uploading.

**Using the Data Dictionary and Online Designer simultaneously.** If you download a Data Dictionary, make edits in Excel, and then someone else makes changes in the Online Designer while you are editing, uploading your file will overwrite the Online Designer changes. Use only one design mode at a time and communicate with other project designers to avoid conflicts.

**Setting validation min/max for the wrong field type.** Populating Columns I or J for a field type that does not support validation (e.g., `radio`, `checkbox`, `calc`) will cause the upload to fail. These columns apply only to `text` fields that also have a validation type set in Column H.

---

## API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See RC-API-01 — REDCap API for authentication, token management, and setup.

- **RC-API-06 — Export Field Names API** — retrieve field variable names, export field names, and choice labels programmatically
- **RC-API-07 — Export Metadata (Data Dictionary) API** — export the full data dictionary (all columns described in this article) programmatically
- **RC-API-08 — Import Metadata (Data Dictionary) API** — import a CSV matching the column structure described in this article to update the project design

---


# 11. Related Articles

- RC-FD-01 — Form Design Overview (concept overview and tool selection)
- RC-FD-02 — Online Designer (guardrailed alternative; use alongside the Data Dictionary)
- RC-FD-03 — Data Dictionary (prerequisite; covers workflow, safety practices, and when to use the Data Dictionary)
- RC-FD-05 — Codebook (reference for reviewing variable definitions without editing)
- RC-BL-01 — Branching Logic: Overview & Scope (required for Column L)
- RC-BL-02 — Branching Logic: Syntax & Atomic Statements (Column L syntax reference)
- RC-LONG-01 — Longitudinal Project Setup (event setup, which the Data Dictionary does not cover)
- RC-AT-01 — Action Tags: Overview (complete reference for Column R action tag codes)
- RC-SURV-02 — Survey Settings: Basic Options & Design (Enhanced Radio Buttons setting and its interaction with Column N alignment codes)
