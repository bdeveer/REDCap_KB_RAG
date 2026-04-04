---
name: redcap-data-dictionary
description: |
  Use this skill whenever a REDCap Data Dictionary CSV file is involved — whether the user uploads one, asks you to read or summarize one, analyze its field structure, check for issues, explain what a project does, or compare instruments. Trigger on phrases like "data dictionary", "REDCap CSV", "uploaded DD", "what's in this project", "analyze this instrument", "review this form structure", "what fields does this project have". Also trigger when the user uploads any file whose name contains DataDictionary. This skill is the foundation for any REDCap project analysis task — use it before trying to understand or explain a project's design.
---

# REDCap Data Dictionary Skill

This skill teaches you how to correctly read, parse, and interpret a REDCap Data Dictionary CSV. Use it whenever a data dictionary is in play — as input, output, or analysis target.

---

## What a Data Dictionary Is

A REDCap Data Dictionary is a CSV file that completely defines every variable (field) and instrument (form) in a REDCap project. Uploading it to REDCap replaces the project's instrument configuration wholesale. It is exported with `_DataDictionary_` in the filename, e.g. `MyStudy_DataDictionary_2026-04-03.csv`.

---

## Step 1: Parse the File

Always use the bundled script rather than reading the CSV manually — it handles encoding edge cases (UTF-8 BOM, latin-1 fallback), large HTML fields in descriptive variables, and produces a complete structured analysis.

```bash
python <skill_path>/scripts/parse_dd.py <path_to_csv> --text
```

For machine-readable output (useful when doing follow-up analysis or comparisons):
```bash
python <skill_path>/scripts/parse_dd.py <path_to_csv> --json
```

**Finding `<skill_path>`:** The skill lives in the directory containing this SKILL.md file. Reference it as a relative or absolute path as needed.

**Finding the uploaded CSV:** Data dictionaries uploaded by the user are at `/sessions/.../mnt/uploads/<filename>.csv`. If the user has a mounted workspace folder, they may also be there.

Run the script and read its full output before proceeding with any analysis. The script produces these sections in order: field type distribution, per-instrument breakdown, complexity ranking, cross-instrument dependencies, identifiers, required fields, matrix groups, calc fields, action tags with descriptions, branching logic count, choice value gaps, project hints, and potential issues.

---

## Step 2: Understand the 18-Column Structure

Each row = one variable/field. Row 1 is always the header; row 2 is always the Record ID field.

| Col | Name | Required? | Notes |
|-----|------|-----------|-------|
| A | Variable / Field Name | Mandatory | Lowercase, letters/numbers/underscores only. Unique project-wide. |
| B | Form Name | Mandatory | Groups variables into instruments. Contiguous blocks only. |
| C | Section Header | Optional | Displayed as a divider bar above the variable in that row. |
| D | Field Type | Mandatory | See field type reference below. |
| E | Field Label | Mandatory | Question text shown to users. May contain HTML. |
| F | Choices / Calculation / Slider Labels | Conditional | Required for dropdown/radio/checkbox; formula for calc; endpoint labels for slider. |
| G | Field Note | Optional | Short instructional text below the field. |
| H | Text Validation Type | Optional | Validation code for text fields (e.g. `date_ymd`, `number`, `integer`). |
| I | Text Validation Min | Optional | Min value — text fields with validation only. |
| J | Text Validation Max | Optional | Max value — text fields with validation only. |
| K | Identifier? | Optional | `y` = flagged as PII. Affects de-identified exports; not an access control. |
| L | Branching Logic | Optional | Conditional display logic. Uses `[variable_name]` syntax with single quotes. |
| M | Required Field? | Optional | `y` = must be answered before the form can be saved. Does NOT work on checkboxes. |
| N | Custom Alignment | Optional | `RV`, `LV`, `LH`, `RH` — controls visual layout. Any other value fails upload. |
| O | Question Number | Optional | Survey display number; cosmetic only. |
| P | Matrix Group Name | Matrix only | Groups radio/checkbox variables into a grid. |
| Q | Matrix Ranking? | Matrix only | `y` = ranking matrix (radio only). |
| R | Field Annotation | Optional | Designer notes AND/OR `@ACTION_TAG` codes. |

---

## Step 3: Interpret Key Patterns

### Field Types

| Code | Collects Data? | Notes |
|------|----------------|-------|
| `text` | Yes | Free text; supports validation via Column H. |
| `notes` | Yes | Multi-line text; no validation. |
| `dropdown` | Yes | Single-select. Choices in Column F. |
| `radio` | Yes | Single-select. Choices in Column F. All displayed as buttons. |
| `checkbox` | Yes | Multi-select. Exports as one variable per option: `[var(raw_value)]`. |
| `calc` | Computed | Formula in Column F. Value recalculates on save; not directly editable. |
| `file` | Yes | File upload. |
| `descriptive` | No | Static text/image. Used for instructions, consent text, embedded images. |
| `slider` | Yes | 0–100 visual analog scale. Optional endpoint labels in Column F. |
| `yesno` | Yes | Built-in Yes/No. No choices column needed. |
| `truefalse` | Yes | Built-in True/False. No choices column needed. |
| `sql` | Admin-only | **Never edit these rows.** Driven by REDCap admin database queries; breaks if touched in CSV. |

### Choices Syntax (Column F for dropdown/radio/checkbox)

Format: `raw_value, Display Label | raw_value, Display Label`

Example: `0, No | 1, Yes | 99, Unknown`

- Raw values are stored in the database and used in branching logic.
- Labels are shown to users.
- For checkbox fields, each option exports as its own variable: `[var_name(raw_value)]`.

**Choice value gaps:** The parser flags fields where numeric choice codes are non-consecutive (e.g., codes 0, 1, 3 — missing 2). These are warnings, not errors — gaps are often intentional (e.g., sentinel values like -77 or -88 for "not applicable" or "refused"). Review each one in context.

### Branching Logic (Column L)

- Uses square brackets: `[variable_name]`
- String comparisons use single quotes: `[status] = '1'` — double quotes cause upload failure
- Checkbox options: `[diet(3)] = '1'` means "option 3 is checked"
- Longitudinal event references: `[baseline_arm_1][dob]` reads the value of `dob` at the baseline event
- Operators: `=`, `<>`, `<`, `>`, `<=`, `>=`, `and`, `or`

**Cross-instrument dependencies:** When branching logic on one instrument references a variable defined on a different instrument, REDCap resolves this in real-time during data entry — but this creates a design dependency. If the source instrument hasn't been filled in yet, the dependent field's condition may behave unexpectedly. The parser surfaces all such form-to-form dependency pairs and gives an example variable for each. This is especially important in longitudinal projects where instrument completion order varies by event.

### Action Tags (Column R)

Action tags start with `@` and modify field behavior beyond what the standard columns offer. Multiple tags are space-separated. The parser provides a description for each tag it encounters.

Key tags to understand when reviewing a project:

| Tag | Effect |
|-----|--------|
| `@NOMISSING` | Prevents saving with a missing value even when not in Required list — common in clinical trials |
| `@HIDDEN` / `@HIDDEN-SURVEY` / `@HIDDEN-FORM` | Selectively hides field by context |
| `@HIDDEN-PDF` | Excludes from PDF/print view |
| `@READONLY` / `@READONLY-SURVEY` | Makes field non-editable |
| `@IF` | Conditionally applies another tag: `@IF([cond],'@TAG','')` |
| `@CALCTEXT` / `@CALCDATE` | Displays calculated text/date in a descriptive field; value not stored |
| `@DEFAULT` / `@SETVALUE` / `@NOW` / `@TODAY` | Auto-fill behaviors |
| `@NONEOFTHEABOVE` | Adds a "None of the above" option that unchecks all other checkboxes |
| `@NOMISSING` | Forces completeness beyond the Required flag |
| `@FORCE-MINMAX` | Enforces validation range even when user tries to override |
| `@CHARLIMIT` | Limits character count in text/notes fields |

> **Note:** A full KB article (RC-AT-01 — Action Tags) has not yet been written. The parser includes descriptions for all commonly encountered tags, but the list is not exhaustive. When you encounter an unfamiliar tag, look it up in REDCap's action tag documentation.

> **Important (Excel):** Column R cells must be formatted as Text before typing `@` tags — Excel interprets `@` as a formula prefix in General-formatted cells and will flag an error.

### Matrix Groups (Column P)

- All variables in a matrix must be contiguous rows with the same Matrix Group Name.
- All must be `radio` or `checkbox` type.
- All must share identical choices (Column F).
- Matrix Group Name must be unique project-wide (separate namespace from variable names).
- A section header on the first matrix row becomes the matrix header.
- Wide matrices render poorly on mobile — flag if choices exceed ~6 options.

### Repeating Instruments

The parser detects instruments that reference `[current-instance]` in their formulas or branching logic — this is the REDCap system variable that holds the current repeat instance number. Instruments using this are configured as repeating in REDCap's longitudinal/repeated setup (not in the Data Dictionary itself). Note this when reviewing: repeating instruments generate instance-numbered records and require special branching logic syntax to reference previous instances.

### Instrument Complexity Score

The parser computes a complexity score per instrument: `field_count + (branching_logic_count × 2) + (calc_count × 3) + action_tag_count`. This is a relative ranking within the project, not an absolute threshold. Use the top-5 ranking to know which instruments will be hardest to review, maintain, or troubleshoot.

---

## Step 4: Issue Detection

The parser flags these issues automatically:

**Upload-blocking errors:**
- Missing choices on dropdown/radio/checkbox fields
- Missing formula on calc fields
- Validation min/max set on non-text field types
- Duplicate variable names
- Unknown/unsupported field types

**Silent design problems (won't block upload, but produce wrong behavior):**
- Required checkboxes — REDCap silently ignores the required flag on checkbox fields; it cannot enforce "at least one selected." This is a very common mistake. Alternatives: @NOMISSING on individual sub-options, or branching logic.
- SQL fields present — flag prominently; these must never be edited in the CSV.

**Warnings requiring review:**
- Choice value gaps — non-consecutive numeric codes. May be intentional (sentinel values) or accidental (coding error). Review each in context.

---

## Step 5: Report to the User

After parsing, present a clear summary. A well-structured report covers these points in order:

1. **Project type and scale** — what kind of project it is (clinical trial, survey, admin tool), total fields, number of instruments, whether it's longitudinal.
2. **Instruments** — walk through each form: what it captures, its field type mix, whether it's a survey, whether it's likely repeating.
3. **Complexity** — call out the most complex instruments. Explain why (heavy branching logic, many calc fields, etc.).
4. **Cross-instrument dependencies** — explain which forms depend on values from other forms, and why this matters for data entry workflow.
5. **Notable patterns** — matrices, calculated scoring instruments, action tag usage and what it implies about the design intent.
6. **Data governance** — identifier-flagged fields, required fields, @NOMISSING usage.
7. **Issues** — anything flagged as a structural problem. Distinguish between upload-blocking errors and silent design problems.
8. **Choice gaps** — mention if significant; note they may be intentional coding.

Keep the summary in plain language. Surface what's actually interesting about *this specific project's* design. If the project uses non-English labels (non-ASCII characters or HTML with non-English text), note this.

---

## What the Data Dictionary Does NOT Capture

These are configured separately in REDCap and are not in the CSV:
- **Events** — defined in the Longitudinal Setup module; the DD only defines instruments and variables
- **Event-instrument assignments** — which instruments appear at which events
- **Repeating instrument/event configuration** — the DD can hint at repeating instruments (via `[current-instance]`), but the repeating setup itself is elsewhere
- **Survey settings** — survey queue, auto-continue, completion text, theme, timestamps
- **Project-level settings** — record auto-naming, data resolution workflow, production mode
- **User rights and Data Access Groups**
- **Randomization setup**
- **Data Quality rules**
- **Reports and custom exports**
- **Alerts and notifications**

When a user asks about any of these, note that this information is not in the data dictionary and would need to be viewed or configured in REDCap directly.

---

## Common Scenarios

**Analyzing what a project collects:** Run `--text`, then walk through each instrument and explain what data is being captured, based on field labels and types. Note any standardized instruments (MoCA, KCCQ, SF-12, etc.) by name if you recognize them.

**Checking if a DD is ready to upload:** Run `--text` and go straight to the Potential Issues section. Also confirm: no double quotes in branching logic; all choice-type fields have choices; calc fields have formulas; no duplicate variable names.

**Explaining cross-instrument dependencies:** Run `--json` and examine `branching_logic.cross_instrument_deps`. For each dep pair, explain what data must be entered in the source instrument before the dependent instrument's conditions will behave correctly.

**Reviewing action tag usage:** The parser lists all tags found with counts and descriptions. High counts of `@NOMISSING` indicate clinical trial-style completeness enforcement. `@CALCTEXT`/`@CALCDATE` in descriptive fields means those fields display dynamic content but store nothing. `@IF` indicates conditional tag application — find the full annotation to understand the condition.

**Identifying required checkbox problems:** Any checkbox flagged as required is a design error the parser will catch. Explain to the user that REDCap cannot enforce "at least one selected" and suggest alternatives.

**Comparing two data dictionaries:** Parse both with `--json`. Compare `instruments` arrays (added/removed forms, field count changes), `field_type_distribution`, `branching_logic.count`, and `potential_issues`.
