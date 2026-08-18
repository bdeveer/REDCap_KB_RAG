---
id: RC-IMP-08
title: Form Display Logic CSV — Column Reference and Format Guide
domain: Data Import
applies_to:
- All REDCap project types
requires: Any supported version
verified_against: REDCap v17.4.1 (Standard) / v17.3.7 (LTS) — changelog review; page
  not re-captured
prerequisites:
- 'RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap'
- RC-FDL-01 — Form Display Logic
version: '1.0'
last_updated: '2026-05-07'
related:
- id: RC-IMP-03
  title: 'CSV Upload Reference: All Bulk Upload Options in REDCap'
- id: RC-FDL-01
  title: Form Display Logic
- id: RC-MYCAP-02
  title: 'MyCap: Designing Instruments for MyCap'
tags:
- data import
- data
synonyms:
- how do i import form display logic via csv
- bulk edit fdl rules in a spreadsheet
- copy form display logic to another project
- upload form display logic csv
- enable or disable whole instruments based on field values
- fdl vs branching logic difference
- empty-string conditions in fdl csv escaping
- export and re-import form display logic rules
---

# 1. Overview

The Form Display Logic (FDL) module supports CSV export and import of FDL rules. FDL controls which entire instruments are enabled or disabled to users based on field values or user attributes — distinct from branching logic, which operates at the field level.

**Location:** Online Designer → Form Display Logic → "Upload or download form display logic" option.

**Upload behavior — Additive/update:** Imported rules replace or update the existing FDL configuration for the instruments named in the file.

**Rights required:** Project Design and Setup.

**Always download first.** Start from an exported file to ensure correct column order and to have a recovery snapshot, particularly because empty-string conditions in FDL use CSV double-quote escaping that plain-text editors frequently corrupt.

For full coverage of Form Display Logic and its use cases, see [RC-FDL-01 — Form Display Logic](RC-FDL-01_Form-Display-Logic.md).

---

# 2. Column Reference

The FDL CSV always has exactly six columns in this order:

| Column | Required | Accepted Values | Notes |
|---|---|---|---|
| `form_name` | Yes | Any valid instrument name (internal name, no spaces) | Must match the instrument's `form_name` exactly as it appears in the Data Dictionary. |
| `event_name` | No | A valid unique event name, or blank | Leave blank to apply the condition to **all events** where the form appears. In classic (non-longitudinal) projects this column is always blank. |
| `control_condition` | Yes | Any valid REDCap logic expression | Same syntax as branching logic. When the expression evaluates to true the form is enabled; when false the form is disabled. |
| `apply_to_data_entry` | Yes | `y` or `n` (lowercase) | `y` — the condition controls whether the form is accessible in the standard data entry UI. |
| `apply_to_survey_autocontinue` | Yes | `y` or `n` (lowercase) | `y` — the condition also controls Survey Auto-Continue behavior for this instrument. |
| `apply_to_mycap_tasks` | Yes | `y` or `n` (lowercase) | `y` — the condition controls whether this instrument appears as a task in MyCap. |

> **Flag values are lowercase.** REDCap exports and expects `y`/`n`, not `Y`/`N`. Using uppercase will cause the import to fail.

> **Multiple rows for the same form use OR logic.** If the same instrument appears in two rows, the form is enabled when *either* condition is true. To require multiple simultaneous conditions, combine them with `and` in a single `control_condition` cell.

---

# 3. Annotated Example

The file below comes from a classic project where two baseline forms are enrolled in FDL solely to suppress them as MyCap tasks, without restricting data entry access.

```csv
form_name,event_name,control_condition,apply_to_data_entry,apply_to_survey_autocontinue,apply_to_mycap_tasks
demographics,,"[record_id]<>""""",y,y,n
contact_info,,"[record_id]<>""""",y,y,n
```

**`demographics` row:**
- `event_name` is blank → the condition applies at every event where the form appears.
- `control_condition` is `[record_id]<>""` — always true for any saved record, so data entry is never blocked.
- `apply_to_data_entry=y`, `apply_to_survey_autocontinue=y` — the always-true condition keeps both enabled.
- `apply_to_mycap_tasks=n` — MyCap task visibility is excluded from FDL control; the form's MyCap task state is governed separately.

**`contact_info` row:** identical pattern applied to a second instrument.

**Why enroll a form in FDL with an always-true condition?** This pattern is used when you only want to set one or two flags (such as `apply_to_mycap_tasks=n`) without actually restricting data entry. It is also useful as a placeholder row you plan to tighten later.

**Note on the raw CSV escaping.** The condition `[record_id]<>""` (comparing against an empty string) exports as `"[record_id]<>""""`  in the raw file. The outer double-quotes delimit the CSV cell; the inner `""` is the CSV escape for a literal `"` character. Spreadsheet applications display this correctly as `[record_id]<>""`. If you edit the file in a plain text editor or parse it programmatically, account for standard CSV double-quote escaping — writing the wrong number of quotes will cause the import to fail or the logic to behave unexpectedly.

---

# 4. Common Mistakes

**Using uppercase `Y`/`N` for flags.** REDCap exports lowercase `y`/`n` and expects the same on import. Uppercase values will cause the row to be rejected.

**Editing empty-string conditions in a plain text editor.** Conditions like `[record_id]<>""` are double-escaped in the raw CSV (`""""`). Editors that don't respect CSV quoting rules will corrupt the escaping and break the logic on re-import.

**Leaving `event_name` blank unintentionally.** A blank `event_name` applies the condition to *every* event where the form appears. If you only intended to restrict one event, specify the event name explicitly.

**Expecting AND behavior from multiple rows.** Two rows for the same form combine with OR — the form is enabled if either condition is true. To enforce multiple simultaneous requirements, write them as a single `control_condition` joined by `and`.

**Using `[user-role-id]` in conditions for projects that may be copied.** Role IDs are installation-wide and change when a project is duplicated. Use `[user-role-name]` instead; role names are preserved on copy.

---

# 5. Related Articles

- [RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap](RC-IMP-03_CSV-Upload-Reference.md)(index of all CSV upload types in REDCap)
- [RC-FDL-01 — Form Display Logic](RC-FDL-01_Form-Display-Logic.md) (full module reference)
- [RC-BL-01 — Branching Logic: Overview & Scope](RC-BL-01_Branching-Logic-Overview-and-Scope.md)(logic expression syntax used in `control_condition`)
- [RC-MYCAP-02 — MyCap: Designing Instruments for MyCap](RC-MYCAP-02_Designing-Instruments-for-MyCap.md)(`apply_to_mycap_tasks` context)
- [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md)(`[user-role-name]` smart variable context)
