---
name: redcap-dd-builder
description: >
  Build a new REDCap Data Dictionary CSV from scratch, or add new instruments and fields to an
  existing one. Use whenever a user wants to create REDCap instruments, design a data dictionary
  from a study protocol or codebook, convert a CRF to REDCap format, or extend a project with new
  forms. Trigger on "build me a data dictionary", "create a DD for my study", "I have a protocol
  that needs to become a REDCap project", "make a REDCap form for", "add a new instrument to my
  project", "convert this codebook to REDCap", "I need to capture these variables in REDCap", or
  when the user describes variables, scales or questionnaires they want formatted as a data
  dictionary. If unsure whether to start fresh or modify an existing DD, use this skill and ask.
  Do NOT use to fix a DD that fails to upload (redcap-dd-fixer) or to summarize, explain or audit
  one (redcap-data-dictionary).
---

# REDCap Data Dictionary Builder

> **REDCap connectors:** before calling any REDCap MCP tool from this skill, read `references/CONNECTOR-RULES.md` (bundled with this skill; the source copy is `claude skills/CONNECTOR-RULES.md` in the REDCap_KB_RAG repo) and follow it — confirm the connector and PID, flag production, stay read-only unless the user explicitly confirms a write on a non-production connector, and never expose the API token.

**Working from a live project.** To add to an existing project's DD, you can pull it with `export_metadata` instead of asking for a CSV: save the JSON to a file and pass it to `--append` (the shared reader accepts `export_metadata` JSON and the output CSV uses the standard upload headers). Hand the finished CSV to the user to upload on the project's **Data Dictionary** page, which previews the changes before committing. Do not call `import_metadata` yourself unless the user asks for it on a non-production connector — it replaces the entire data dictionary.

**Dependency:** `build_dd.py` imports the shared module `dd_common.py`, and validation uses `parse_dd.py`, both from the redcap-data-dictionary skill — that skill must be installed alongside this one.

This skill guides you through building a valid, upload-ready REDCap Data Dictionary CSV — either
from scratch based on a protocol, codebook, or conversation, or by extending an existing DD with
new instruments and fields.

The goal is a CSV that uploads to REDCap on the first try, with sensible variable names, correct
field types, and no structural errors. Decisions made here are hard to undo once data collection
starts, so it is worth taking the time to get the design right.

---

## Step 0: Determine the mode

**Before anything else**, ask the user this one question (use AskUserQuestion if available):

> "Are you building a brand-new data dictionary from scratch, or do you want to add to or modify
> an existing data dictionary?"

- **Building from scratch** → proceed to Step 1
- **Modifying an existing DD** → proceed to Step 1b

---

## Step 1: Gather information (new build)

### What you need before writing any rows

Collect the following context. If the user has uploaded a document (study protocol, codebook, CRF,
questionnaire PDF, Excel codebook), **read it first** and extract as much as you can before asking
questions. The document usually contains: study purpose, variable lists, response options,
validation rules, and skip logic.

If there is no document, ask the user together (not one by one):
- What does the study or project collect? (brief description)
- How many forms/instruments are needed, and what should they be called?
- Is this a longitudinal project (multiple time points or events)?

### When a document is provided

Read the document and extract:
- All instruments/forms mentioned
- For each instrument: all variables, their question text, response options, and any skip/show conditions
- Any scoring or calculation rules
- Any PII fields (name, DOB, MRN, address)

Then present your extracted design to the user as a draft (see Step 3), ask them to confirm or
correct it, and proceed from there. This is faster than asking the user to describe every field
from scratch when the document already contains the information.

---

## Step 1b: Modifying an existing DD

If the user is adding to or modifying an existing data dictionary, parse it first:

```bash
python <skill_path>/../redcap-data-dictionary/scripts/parse_dd.py <path_to_csv> --text
```

This gives you the complete picture of what already exists: all variable names, all form names,
all field types. You need this before designing additions so you can:
- Choose variable names that don't conflict with existing ones
- Understand the naming conventions already in use
- Know which forms already exist

Then ask the user:
- What do you want to add? (new instruments, new fields within an existing form, or both?)
- Are there any existing fields you want to modify? (if so, flag that renaming a variable severs
  the link to all data collected under the old name — REDCap treats a rename as delete + create)

---

## Step 2: Design instruments and fields

Work through each instrument one at a time. For each instrument, gather the fields it should
contain. The subsections below describe how to make good decisions on naming, types, and choices.

### Naming conventions

**Form names** (what goes in the DD's Form Name column):
- Lowercase letters, digits, underscores — no spaces, no hyphens
- Descriptive but concise: `demographics`, `baseline_vitals`, `phq9`, `adverse_events`
- REDCap displays these with underscores replaced by spaces and title-cased in the interface

**Variable names** (the field's machine-readable identifier):
- Lowercase letters, digits, underscores — must start with a letter
- Keep to 26 characters or fewer — RC-FD-08 §5.1: "Maximum recommended length: 26 characters."
  This is a recommendation, not an upload error; the build script warns on longer names.
- **Unique across the entire project** (not just within one form)
- Use consistent prefixes to group related fields: `phq9_q1` through `phq9_q9`, `phq9_total`
- Be specific enough to avoid future collisions: `visit_date` not `date`; `ae_notes` not `notes`

**Converting labels to variable names** — common patterns:
| Label | Suggested variable name |
|---|---|
| Date of Birth | `dob` |
| Weight (kg) | `weight_kg` |
| PHQ-9 Question 1 | `phq9_q1` |
| Were there adverse events? | `ae_present` |
| Blood Pressure Systolic | `bp_systolic` |
| Primary Diagnosis | `primary_dx` |
| Treatment Start Date | `tx_start_dt` |

When a good name is not obvious, suggest one and let the user confirm.

---

### Field type selection guide

| What the field collects | Use this type |
|---|---|
| Free text (names, comments, open-ended) | `text` |
| Long free text, multi-line | `notes` |
| Yes / No — nothing else | `yesno` |
| True / False — nothing else | `truefalse` |
| A date (no time component) | `text` + date validation |
| A date and time | `text` + datetime validation |
| A number (age, weight, score, count) | `text` + integer or number validation |
| Single choice from 2–4 options | `radio` |
| Single choice from 5+ options | `dropdown` |
| Multiple choices (check all that apply) | `checkbox` |
| Auto-calculated value | `calc` |
| Instructions, consent text, images, headers | `descriptive` |
| File upload (PDF, image) | `file` |
| Analog visual scale (0–100 slider) | `slider` |

> **Rule of thumb on radio vs. dropdown:** Use `radio` when options fit on screen together (≤4);
> use `dropdown` for longer lists. For Yes/No, prefer the native `yesno` type over a radio with
> two choices — it's cleaner and more compact.

### Validation types for text fields

| What to validate | Code |
|---|---|
| Date (YYYY-MM-DD) | `date_ymd` |
| Date (MM-DD-YYYY) | `date_mdy` |
| Date and time | `datetime_ymd` |
| Whole number | `integer` |
| Any decimal number | `number` |
| Decimal, 2 places | `number_2dp` |
| Email address | `email` |
| US phone number | `phone` |
| US ZIP code | `zipcode` |

Default to `date_ymd` for dates unless the study specifies a different format.

Column H is not text-only (RC-FD-08 §5.7): on a `file` field, `signature` makes it a classic
signature and `enhanced_signature` an Enhanced Signature (17.1.0+); on a `slider` field, `number`
shows the selected value. Leave it empty for every other non-text type. Min/max apply to `text`
fields only.

### Standard choices for common fields

Use these NIH-standard codings for demographic fields:

**Biological sex:**
`1, Male | 2, Female | 3, Other | 99, Unknown / Not reported`

**Race (NIH categories):**
`1, American Indian or Alaska Native | 2, Asian | 3, Black or African American | 4, Native Hawaiian or Other Pacific Islander | 5, White | 6, More than one race | 99, Unknown / Not reported`

**Ethnicity:**
`1, Hispanic or Latino | 2, Not Hispanic or Latino | 99, Unknown / Not reported`

**Generic Yes / No / Unknown:**
`1, Yes | 0, No | 99, Unknown`

---

### Design patterns

**"Other, please specify"**
When a choice-type field has an "Other" option, add a companion `text` field with branching logic
so it only appears when "Other" is selected:
```
Field: insurance_type (radio)
Choices: 1, Private | 2, Medicare | 3, Medicaid | 4, Self-pay | 5, Other

Field: insurance_type_other (text)
Branching logic: [insurance_type] = '5'
```

**Validated questionnaire instruments (PHQ-9, GAD-7, SF-36, etc.)**
- Use consistent variable names: `phq9_q1` through `phq9_q9`
- If all items share the same response options, group them in a matrix (Column P = Matrix Group Name)
- Add a `calc` field for the total score: `sum([phq9_q1],[phq9_q2],...,[phq9_q9])`
- Open with a `descriptive` field containing the instrument's standard instructions
- Use `redcap-syntax` skill to write the scoring formula if it has conditional components

**Calculated fields**
For any calc field, use the `redcap-syntax` skill if the formula is non-trivial. Describe
what the field should calculate, list the source variable names, and note whether the project is
longitudinal. Common patterns:
- Total score: `sum([q1],[q2],[q3],[q4])`
- BMI: `([weight_kg])/(([height_m])^(2))`
- Age at enrollment: `age_at_date([dob],[consent_date],false)` (calendar-accurate; avoid `datediff(...,'y')` for age)

**Branching logic**
For anything beyond a simple single-condition show/hide, use the `redcap-syntax` skill.
For simple cases:
- Show if a radio = a value: `[field_name] = '1'`
- Show if checkbox option is checked: `[field_name(coded_value)] = '1'`
- Show if field has any value: `[field_name] <> ''`

---

### Style conventions

Before finalizing field designs, apply the best practices from `kb/RC-DSGN-01_REDCap-Project-Design-Best-Practices.md`
in the REDCap_KB_RAG repo. Read it if you need the full rationale. The conventions most relevant to DD
building:

**Field alignment (Column N — Custom Alignment)**
- `notes` fields: always use `LH` or `LV` — the half-width default (`RV`) makes text areas
  cramped. There is rarely a reason to use a half-width notes field.
- `radio` and `checkbox` fields: `LH` for 2–4 short choices; `LV` for 5+ choices or long labels.
  Prefer Left (`L`) over Right for the page-position component.
- `text`, `dropdown`, `yesno`, `truefalse`: leave blank (accept `RV` default) unless there is a
  specific layout reason to override.
- Avoid mixing Left and Right fields in the same section without a clear layout purpose —
  alternating widths creates a visually fragmented form.

When building the JSON spec, set the `custom_alignment` property on fields where the convention
calls for a non-default value (i.e., `notes` fields and any `radio`/`checkbox` field). Only `LH`,
`LV`, `RH`, `RV` are valid; the script flags anything else.

**Field Note (Column G) vs. Field Annotation (Column R)**
- **Field Note** (`field_note` in the spec) — visible to everyone completing the form, including
  survey participants. Use for: units (`mg/L`, `kg`), date format reminders (`YYYY-MM-DD`),
  scope clarifications (`Include prescribed medications only`), acceptable ranges. Keep it to
  one or two lines — longer notes get ignored.
- **Field Annotation** (`field_annotation` in the spec) — visible only in the Data Dictionary
  and Online Designer, never on the form. Use for: design rationale, outstanding to-do notes
  for designers, coding decisions. Action tags also go here (e.g., `@HIDDEN-SURVEY @READONLY`).

When combining a plain-text designer note with action tags in `field_annotation`, put the note
first and the action tags after, separated by a space or line break.

> **Never put user-facing instructions in `field_annotation`** — they will not be seen by
> anyone completing the form. Use `field_note` for anything the data entry user needs to read.

When gathering field details from the user, ask separately: (a) what, if anything, data entry
users need to see on the form, and (b) any notes intended only for project designers.

---

## Step 3: Confirm the design before building

Before generating the CSV, present a summary of what you're about to build. This is important —
changes are much easier to make now than after data collection starts.

A good summary includes:
- **Instruments**: list with field count per instrument
- **For each instrument**: field name, type, and brief description — one line per field
- **Any calculated fields**: name and what they compute
- **Any branching logic**: which fields are conditional and what triggers them
- **PII-flagged fields**: any marked as identifiers

If working from a document, show the user what you extracted and ask them to confirm or correct it.
If built through conversation, recap the agreed design and ask for a final thumbs-up.

Do not run the build script until the user has confirmed (or explicitly says to proceed).

---

## Step 4: Build the JSON spec and generate the CSV

Once confirmed, assemble the JSON spec and run the build script.

### JSON spec format

```json
{
  "project": {
    "record_id_variable": "record_id",
    "record_id_label": "Record ID"
  },
  "instruments": [
    {
      "form_name": "demographics",
      "fields": [
        {
          "variable": "dob",
          "label": "Date of Birth",
          "field_type": "text",
          "validation": "date_ymd",
          "required": false,
          "identifier": true
        },
        {
          "variable": "sex",
          "label": "Biological Sex",
          "field_type": "radio",
          "choices": [
            {"value": "1", "label": "Male"},
            {"value": "2", "label": "Female"},
            {"value": "3", "label": "Other"},
            {"value": "99", "label": "Unknown / Not reported"}
          ]
        },
        {
          "variable": "bmi",
          "label": "BMI (calculated)",
          "field_type": "calc",
          "formula": "([weight_kg])/(([height_m])^(2))"
        }
      ]
    }
  ]
}
```

### Field spec properties

| Property | Required? | Notes |
|---|---|---|
| `variable` | Yes | REDCap variable name (see naming rules) |
| `label` | Yes | Question text shown to the user |
| `field_type` | Yes | One of the valid field types |
| `section_header` | No | Divider bar displayed above this field |
| `choices` | If radio/dropdown/checkbox | List of `{value, label}` dicts |
| `formula` | If calc | The calculation expression (plain string) |
| `field_note` | No | Instructional text displayed below the field |
| `validation` | No | Column H: any validation code on `text`; `signature`/`enhanced_signature` on `file`; `number` on `slider` |
| `validation_min` | No | Min value (text fields with validation only) |
| `validation_max` | No | Max value (text fields with validation only) |
| `identifier` | No | `true` = flag as containing PII |
| `branching_logic` | No | REDCap branching logic expression |
| `required` | No | `true` = must be answered to save the form |
| `custom_alignment` | No | `LH`, `LV`, `RH`, or `RV` (blank = `RV` default) |
| `question_number` | No | Survey question number |
| `field_annotation` | No | Action tags (e.g., `@HIDDEN`, `@CALCTEXT(...)`) |
| `matrix_group` | No | Groups radio/checkbox fields into a matrix grid — rows must be contiguous, same type, identical choices |
| `matrix_ranking` | No | `true` = ranking matrix (radio matrices only) |

Numbers in the JSON (e.g., `"validation_min": 0`) are fine; the script converts them to text.

### Running the build script

```bash
# Save the spec to a JSON file, then:

# New build from scratch:
python <skill_path>/scripts/build_dd.py spec.json \
  --output "<output_folder>/MyStudy_DataDictionary.csv"

# Appending to an existing DD:
python <skill_path>/scripts/build_dd.py spec.json \
  --append existing_dd.csv \
  --output "<output_folder>/MyStudy_DataDictionary_updated.csv"
```

**Finding `<skill_path>`:** The skill's base directory, shown when the skill loads (normally `~/.claude/skills/<skill-name>`). `<output_folder>` = the folder the existing DD is in, or one the user names (never a temp folder).

With `--append`, fields for a form that already exists are inserted right after that form's last
existing row (REDCap rejects a DD whose form rows are split); new forms go at the end. The output
keeps the input's header style — display headers (`Variable / Field Name`, ...) or API-style
headers (`field_name`, `form_name`, ...). If the headers are unrecognised, the script stops
without writing anything.

The script will warn you about any issues it detects (missing choices, invalid variable names,
duplicate names across the existing DD and the spec, non-contiguous forms, matrix group problems,
invalid alignment codes, validation values dropped for the field type). Review the warnings
before proceeding.

---

## Step 5: Validate the output

Run the parser on the generated CSV to catch any remaining structural issues:

```bash
python <skill_path>/../redcap-data-dictionary/scripts/parse_dd.py <output_csv> --text
```

If the parser reports issues:
- **Missing choices on a choice field** → ask the user for the options, then rebuild
- **Missing formula on a calc field** → use `redcap-syntax` to write it
- **Duplicate variable names** → rename the duplicate (and confirm with the user before doing so)
- **Other structural errors** → use the `redcap-dd-fixer` skill

---

## Step 6: Deliver

Save two files to the workspace:
1. **The CSV** — named `ProjectName_DataDictionary.csv` — this is what uploads to REDCap
2. **The JSON spec** — named `ProjectName_dd_spec.json` — preserves the design for future modifications

Tell the user the CSV is ready to upload via **Project Setup → Data Dictionary → Upload Data Dictionary**.

If there were warnings from the build script or parser, list them clearly so the user knows what
still needs attention before uploading.

---

## Reference: what the data dictionary controls and what it doesn't

The CSV controls all field and instrument definitions. It does **not** control:
- Event setup and event-instrument assignments (longitudinal projects — set up in Project Setup)
- Survey settings (queue, auto-continue, theme, completion text)
- Repeating instrument/event configuration
- User rights and Data Access Groups
- Randomization, reports, data quality rules

If the user asks about these, note that they're configured separately in REDCap's interface.
For the full 18-column DD structure and all field-type rules, the `redcap-data-dictionary` skill
has the complete reference.
