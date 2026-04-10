---
name: redcap-dd-builder
description: |
  Build a new REDCap Data Dictionary CSV from scratch, or add new instruments and fields to an
  existing one. Use this skill whenever a user wants to create REDCap instruments, design a data
  dictionary from a study protocol or codebook, convert a CRF to REDCap format, or extend an
  existing project with new forms. Trigger on: "build me a data dictionary", "create a DD for my
  study", "I have a protocol that needs to become a REDCap project", "make a REDCap form for",
  "add a new instrument to my project", "design these fields in REDCap", "convert this codebook
  to REDCap", "help me set up my REDCap project variables", "create a data collection form for",
  "I need to capture these variables in REDCap". Also trigger when the user describes variables,
  scales, or questionnaires they want to collect and needs them formatted as a REDCap data
  dictionary. If the user is not sure whether to start fresh or modify an existing DD, use this
  skill and ask them.
---

# REDCap Data Dictionary Builder

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
python <data_dictionary_skill_path>/scripts/parse_dd.py <path_to_csv> --text
```

`<data_dictionary_skill_path>` = `/sessions/.../mnt/.claude/skills/redcap-data-dictionary`

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
- Max 26 characters
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
| URL | `url` |

Default to `date_ymd` for dates unless the study specifies a different format.

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
- Use `redcap-syntax-builder` skill to write the scoring formula if it has conditional components

**Calculated fields**
For any calc field, use the `redcap-syntax-builder` skill if the formula is non-trivial. Describe
what the field should calculate, list the source variable names, and note whether the project is
longitudinal. Common patterns:
- Total score: `sum([q1],[q2],[q3],[q4])`
- BMI: `([weight_kg])/(([height_m])^(2))`
- Age at enrollment: `datediff([dob],[consent_date],'y')`

**Branching logic**
For anything beyond a simple single-condition show/hide, use the `redcap-syntax-builder` skill.
For simple cases:
- Show if a radio = a value: `[field_name] = '1'`
- Show if checkbox option is checked: `[field_name(coded_value)] = '1'`
- Show if field has any value: `[field_name] <> ''`

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
| `validation` | If text | Validation type code |
| `validation_min` | No | Min value (text fields with validation only) |
| `validation_max` | No | Max value (text fields with validation only) |
| `identifier` | No | `true` = flag as containing PII |
| `branching_logic` | No | REDCap branching logic expression |
| `required` | No | `true` = must be answered to save the form |
| `field_annotation` | No | Action tags (e.g., `@HIDDEN`, `@CALCTEXT(...)`) |
| `matrix_group` | No | Groups radio/checkbox fields into a matrix grid |

### Running the build script

```bash
# Save the spec to a JSON file, then:

# New build from scratch:
python <skill_path>/scripts/build_dd.py spec.json \
  --output "/sessions/.../mnt/workspace/MyStudy_DataDictionary.csv"

# Appending to an existing DD:
python <skill_path>/scripts/build_dd.py spec.json \
  --append existing_dd.csv \
  --output "/sessions/.../mnt/workspace/MyStudy_DataDictionary_updated.csv"
```

`<skill_path>` = the directory containing this SKILL.md file.

The script will warn you about any issues it detects (missing choices, invalid variable names,
duplicate names). Review the warnings before proceeding.

---

## Step 5: Validate the output

Run the parser on the generated CSV to catch any remaining structural issues:

```bash
python <data_dictionary_skill_path>/scripts/parse_dd.py <output_csv> --text
```

If the parser reports issues:
- **Missing choices on a choice field** → ask the user for the options, then rebuild
- **Missing formula on a calc field** → use `redcap-syntax-builder` to write it
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
