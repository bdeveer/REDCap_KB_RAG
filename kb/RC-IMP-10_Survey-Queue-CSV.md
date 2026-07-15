

**Survey Queue CSV — Column Reference and Format Guide**

| **Article ID** | [RC-IMP-10 — Survey Queue CSV — Column Reference and Format Guide](RC-IMP-10_Survey-Queue-CSV.md) |
|---|---|
| **Domain** | Data Import |
| **Applies To** | REDCap projects with surveys and Survey Queue enabled |
| **Prerequisite** | [RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap](RC-IMP-03_CSV-Upload-Reference.md); [RC-SURV-07 — Survey Queue](RC-SURV-07_Survey-Queue.md) |
| **Skill Level** | Intermediate |
| **Version** | 1.0 |
| **Last Updated** | 2026-05-07 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap](RC-IMP-03_CSV-Upload-Reference.md); [RC-SURV-07 — Survey Queue](RC-SURV-07_Survey-Queue.md); [RC-IMP-06 — Automated Survey Invitations CSV — Column Reference and Format Guide](RC-IMP-06_Automated-Survey-Invitations-CSV.md)|
| **Synonyms** | how do i import a survey queue via csv; bulk edit survey queue conditions in a spreadsheet; copy survey queue setup to another project; upload survey queue configuration csv; set the order surveys appear to participants; conditional logic for which survey shows next; export and re-import survey queue settings; survey queue csv column reference |

---

## 1. Overview

The Survey Queue module supports CSV export and import of queue configurations. The survey queue defines the order and conditional logic that governs which surveys are presented to a participant after completing a prior survey.

**Location:** Online Designer → Survey Queue → "Upload or download survey queue" option.

**Upload behavior — Additive/update:** Rows matching the `form_name`/`event_name` key are updated; rows for instruments not in the file are left unchanged.

**Rights required:** Project Design and Setup.

**Always download first.** Start from a file exported from the project rather than building from scratch. This ensures the correct column structure and gives you a recovery snapshot. The Survey Queue must already be enabled in the project before this option appears.

For full coverage of configuring the Survey Queue through the REDCap UI, see [RC-SURV-07 — Survey Queue](RC-SURV-07_Survey-Queue.md).

---

## 2. Column Reference

The Survey Queue CSV always has exactly eight columns in this order:

| Column | Required | Accepted Values | Notes |
|---|---|---|---|
| `form_name` | Yes | Any survey-enabled instrument variable name | The instrument being added to the queue. Must match the instrument's internal name (lowercase, underscored) exactly. |
| `event_name` | No | A valid unique event name, or blank | Longitudinal projects only. Leave blank in classic projects. When blank in a longitudinal project, the queue entry applies to the instrument at any event where it appears. |
| `active` | Yes | `1` or `0` | `1` = the instrument is activated in the queue and will be presented to participants when its condition is met. `0` = the entry exists in the queue configuration but is currently deactivated. |
| `condition_surveycomplete_form_name` | No | Instrument variable name, or blank | Completion trigger — specifies which survey must be completed before this instrument is offered in the queue. Leave blank for logic-only triggers. |
| `condition_surveycomplete_event_name` | No | Unique event name, or blank | Event of the completion-trigger survey. May reference an event from a different arm. Leave blank for logic-only triggers or classic projects. |
| `condition_andor` | Yes | `AND` or `OR` | Relationship between the completion trigger and the logic condition. **Always populate this column** — even when only one trigger type is configured, REDCap expects a value here. Using `AND` with only one trigger type is equivalent to using that trigger alone. |
| `condition_logic` | No | Any valid REDCap branching logic expression, or blank | Additional logic condition that must be true for the survey to be offered. Cross-event field references use the format `[event_name][field_name]`. Leave blank for completion-trigger-only entries. Empty-string comparisons (`""`) are double-escaped in the raw CSV (see Common Mistakes). |
| `auto_start` | Yes | `1` or `0` | `1` = REDCap automatically advances the participant to the next survey in the queue upon completion of the current survey. `0` = the participant is returned to the survey queue overview page and must manually select the next survey. |

---

## 3. Annotated Example

The file below shows a three-survey queue from a classic (non-longitudinal) project. After completing `screening`, participants are automatically advanced to `demographics`. After completing `demographics`, they are advanced to `phq9` — but only if a screening eligibility field is set to `1`.

```csv
form_name,event_name,active,condition_surveycomplete_form_name,condition_surveycomplete_event_name,condition_andor,condition_logic,auto_start
demographics,,1,screening,,AND,,1
phq9,,1,demographics,,AND,[eligible]=1,1
```

Key points illustrated:

- **`event_name` is blank** — this is a classic project; the column is present but always empty.
- **`condition_andor` is always populated** — both rows use `AND` even though only one trigger type is configured per row.
- **`auto_start = 1`** — participants are pushed directly to the next survey without returning to the queue overview.
- **`condition_logic` is blank for `demographics`** — no logic condition is required; completion of `screening` alone is sufficient.
- **`condition_logic = [eligible]=1` for `phq9`** — the instrument is only queued if the participant passed the eligibility check recorded during screening.

---

## 4. Common Mistakes

**Leaving `condition_andor` blank.** REDCap expects this column to be populated even when only a completion trigger or only a logic condition is configured. A blank value may cause the row to be rejected or the trigger to behave unexpectedly.

**Using the instrument display label instead of the variable name.** Both `form_name` and `condition_surveycomplete_form_name` expect the internal instrument variable name (lowercase, underscored), not the display label shown in the Online Designer. For example, use `social_history`, not `Social History`.

**Editing empty-string conditions in a plain text editor.** If `condition_logic` contains an empty-string comparison (`""`), the raw CSV encodes it with doubled double-quotes (`""""`). Plain-text editors that don't handle CSV quoting will corrupt this, causing the logic to fail on re-import. Use a spreadsheet application to edit these values.

**Forgetting `event_name` in longitudinal projects.** In a longitudinal project where the same instrument appears at multiple events, a blank `event_name` applies the queue entry to the instrument at every event. If you intend to queue the instrument only at a specific event, populate `event_name` with the unique event name.

**Expecting the upload to add new instruments to the queue from scratch.** The queue upload updates existing queue entries. If an instrument has never been added to the Survey Queue, it should first be added through the Online Designer UI before attempting a CSV update.

---

## 5. Related Articles

- [RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap](RC-IMP-03_CSV-Upload-Reference.md)(index of all CSV upload types in REDCap)
- [RC-SURV-07 — Survey Queue](RC-SURV-07_Survey-Queue.md) (full module reference including UI configuration)
- [RC-IMP-06 — Automated Survey Invitations CSV — Column Reference and Format Guide](RC-IMP-06_Automated-Survey-Invitations-CSV.md)(related: ASI format reference)
- [RC-SURV-01 — Surveys – Basics](RC-SURV-01_Surveys-Basics.md)(survey fundamentals)
- [RC-BL-01 — Branching Logic: Overview & Scope](RC-BL-01_Branching-Logic-Overview-and-Scope.md)(logic expression syntax used in `condition_logic`)
