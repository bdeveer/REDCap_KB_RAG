

**Form Display Logic CSV — Column Reference and Format Guide**

| **Article ID** | [RC-IMP-08 — Form Display Logic CSV — Column Reference and Format Guide](RC-IMP-08_Form-Display-Logic-CSV.md) |
|---|---|
| **Domain** | Data Import |
| **Applies To** | All REDCap project types |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — Form Display Logic CSV upload behaviour checked against source code; pages not re-captured |
| **Prerequisite** | [RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap](RC-IMP-03_CSV-Upload-Reference.md); [RC-FDL-01 — Form Display Logic](RC-FDL-01_Form-Display-Logic.md) |
| **Skill Level** | Intermediate |
| **Version** | 1.1 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap](RC-IMP-03_CSV-Upload-Reference.md); [RC-FDL-01 — Form Display Logic](RC-FDL-01_Form-Display-Logic.md); [RC-MYCAP-02 — MyCap: Designing Instruments for MyCap](RC-MYCAP-02_Designing-Instruments-for-MyCap.md)|
| **Synonyms** | how do i import form display logic via csv; bulk edit fdl rules in a spreadsheet; copy form display logic to another project; upload form display logic csv; enable or disable whole instruments based on field values; fdl vs branching logic difference; empty-string conditions in fdl csv escaping; export and re-import form display logic rules |

---

## 1. Overview

The Form Display Logic (FDL) module supports CSV export and import of FDL rules. FDL controls which entire instruments are enabled or disabled to users based on field values or user attributes — distinct from branching logic, which operates at the field level.

**Location:** Online Designer → Form Display Logic → "Upload or download form display logic" option.

**Upload behavior — Replace:** The upload **replaces all existing FDL conditions** in the project with the conditions in the file. Instruments that are not in the file lose their FDL. The upload is all-or-nothing: if any row has an error, REDCap reports it and saves nothing. A file with no condition rows offers to delete all existing conditions (and resets the two FDL options in the setup dialog).

> **Important:** FDL is not part of Draft Mode. In a production project an uploaded file takes effect immediately for all users, so download the current setup first and test the new file in a development copy of the project.

**Rights required:** Project Design and Setup.

**Always download first.** Start from an exported file to ensure correct column order and to have a recovery snapshot, particularly because empty-string conditions in FDL use CSV double-quote escaping that plain-text editors frequently corrupt.

For full coverage of Form Display Logic and its use cases, see [RC-FDL-01 — Form Display Logic](RC-FDL-01_Form-Display-Logic.md).

---

## 2. Column Reference

The columns depend on the project type:

- **Longitudinal projects:** six columns, in the order shown below.
- **Classic (non-longitudinal) projects:** five columns — the same list without `event_name`. A file that contains an `event_name` column is rejected in a classic project.

| Column | Required | Accepted Values | Notes |
|---|---|---|---|
| `form_name` | Yes | Any valid instrument name (internal name, no spaces) | Must match the instrument's `form_name` exactly as it appears in the Data Dictionary. |
| `event_name` | No | A valid unique event name, or blank | Longitudinal projects only. Leave blank to apply the condition to **all events** where the form appears. Classic projects do not have this column. |
| `control_condition` | Yes | Any valid REDCap logic expression | Same syntax as branching logic. When the expression evaluates to true the form is enabled; when false the form is disabled. |
| `apply_to_data_entry` | Yes | `y` or `n` (lowercase) | `y` — the condition controls whether the form is accessible in the standard data entry UI. |
| `apply_to_survey_autocontinue` | Yes | `y` or `n` (lowercase) | `y` — the condition also controls Survey Auto-Continue behavior for this instrument. |
| `apply_to_mycap_tasks` | Yes | `y` or `n` (lowercase) | `y` — the condition controls whether this instrument appears as a task in MyCap. `n` leaves MyCap out of this condition's control; it does not hide the task. |

> **Flag values are lowercase.** REDCap exports `y`/`n`, and on upload only a lowercase `y` counts as yes. Anything else — including `Y` or `yes` — is silently read as `n`, with no error. A row whose three flags all end up `n` is rejected.

> **Identical conditions are merged.** Rows with exactly the same `control_condition` text are combined into one condition covering all their forms and events. The flags of the first such row are kept for the combined condition, so give rows that need different flags different condition text.

> **Multiple rows for the same form use OR logic.** If the same instrument appears in two rows, the form is enabled when *either* condition is true. To require multiple simultaneous conditions, combine them with `and` in a single `control_condition` cell.

---

## 3. Annotated Example

The file below comes from a classic project (five columns, no `event_name`) where two baseline forms are enrolled in FDL with an always-true condition, so data entry and Survey Auto-Continue are never restricted.

```csv
form_name,control_condition,apply_to_data_entry,apply_to_survey_autocontinue,apply_to_mycap_tasks
demographics,"[record_id]<>""""",y,y,n
contact_info,"[record_id]<>""""",y,y,n
```

In a longitudinal project the same rows carry an `event_name` column after `form_name`; a blank `event_name` applies the condition at every event where the form appears.

**`demographics` row:**
- `control_condition` is `[record_id]<>""` — always true for any saved record, so data entry is never blocked.
- `apply_to_data_entry=y`, `apply_to_survey_autocontinue=y` — the always-true condition keeps both enabled.
- `apply_to_mycap_tasks=n` — this condition does not control MyCap. It does **not** hide or suppress the form as a MyCap task.

**`contact_info` row:** identical pattern applied to a second instrument. Because both rows have the same condition text, REDCap stores them as one condition covering both forms.

**Why enroll a form in FDL with an always-true condition?** This pattern keeps a form in the FDL setup without actually restricting access. It is also useful as a placeholder row you plan to tighten later.

**MyCap and the `n` flag.** If no condition in the project applies to MyCap Tasks, FDL has no effect in MyCap. Once any condition applies to MyCap Tasks, MyCap uses only those MyCap-flagged conditions, and a task whose form has no MyCap-flagged condition is not shown. To keep a MyCap task always available in that situation, set `apply_to_mycap_tasks` to `y` on its always-true row. See [RC-FDL-01 — Form Display Logic](RC-FDL-01_Form-Display-Logic.md) for details.

**Note on the raw CSV escaping.** The file follows standard CSV quoting: every `"` inside a cell is doubled, and the cell is wrapped in quotes. So the condition `[record_id]<>""` (comparing against an empty string) is written `"[record_id]<>"""""` in the raw file — four quotes for the two literal `"` characters, plus the closing quote of the cell. Spreadsheet applications display this correctly as `[record_id]<>""`. If you edit the file in a plain text editor or parse it programmatically, account for standard CSV double-quote escaping — writing the wrong number of quotes will cause the import to fail or the logic to behave unexpectedly.

---

## 4. Common Mistakes

**Using uppercase `Y`/`N` or `yes` for flags.** REDCap exports lowercase `y`/`n`. On upload anything other than a lowercase `y` is silently read as `n` — the row is not flagged as an error, so the condition simply stops applying to that area. A row that ends up with all three flags `n` is rejected. Use lowercase `y`.

**Uploading a partial file.** The upload replaces every FDL condition in the project. A file containing only the conditions you changed removes all the others. Start from a full download.

**Adding an `event_name` column in a classic project.** Classic projects use five columns; a file with `event_name` is rejected. Download from the target project to get the right layout.

**Using `apply_to_mycap_tasks=n` to hide a MyCap task.** An `n` flag only leaves MyCap out of that condition's control; it never hides a task by itself. To control a task in MyCap, set the flag to `y` on a condition that is false when the task should be unavailable.

**Editing empty-string conditions in a plain text editor.** Conditions like `[record_id]<>""` are escaped in the raw CSV as `"[record_id]<>"""""`. Editors that don't respect CSV quoting rules will corrupt the escaping and break the logic on re-import.

**Leaving `event_name` blank unintentionally (longitudinal projects).** A blank `event_name` applies the condition to *every* event where the form appears. If you only intended to restrict one event, specify the event name explicitly.

**Expecting AND behavior from multiple rows.** Two rows for the same form combine with OR — the form is enabled if either condition is true. To enforce multiple simultaneous requirements, write them as a single `control_condition` joined by `and`.

**Using `[user-role-id]` in conditions for projects that may be copied.** Role IDs are installation-wide and change when a project is duplicated. Use `[user-role-name]` instead; role names are preserved on copy.

---

## 5. Related Articles

- [RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap](RC-IMP-03_CSV-Upload-Reference.md) (index of all CSV upload types in REDCap)
- [RC-FDL-01 — Form Display Logic](RC-FDL-01_Form-Display-Logic.md) (full module reference)
- [RC-BL-01 — Branching Logic: Overview & Scope](RC-BL-01_Branching-Logic-Overview-and-Scope.md) (logic expression syntax used in `control_condition`)
- [RC-MYCAP-02 — MyCap: Designing Instruments for MyCap](RC-MYCAP-02_Designing-Instruments-for-MyCap.md) (`apply_to_mycap_tasks` context)
- [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md) (`[user-role-name]` smart variable context)
