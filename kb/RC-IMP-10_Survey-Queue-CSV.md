

**Survey Queue CSV — Column Reference and Format Guide**

| **Article ID** | [RC-IMP-10 — Survey Queue CSV — Column Reference and Format Guide](RC-IMP-10_Survey-Queue-CSV.md) |
|---|---|
| **Domain** | Data Import |
| **Applies To** | REDCap projects with surveys and Survey Queue enabled |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — Survey Queue CSV upload behaviour checked against source code; pages not re-captured |
| **Prerequisite** | [RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap](RC-IMP-03_CSV-Upload-Reference.md); [RC-SURV-07 — Survey Queue](RC-SURV-07_Survey-Queue.md) |
| **Skill Level** | Intermediate |
| **Version** | 1.1 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap](RC-IMP-03_CSV-Upload-Reference.md); [RC-SURV-07 — Survey Queue](RC-SURV-07_Survey-Queue.md); [RC-IMP-06 — Automated Survey Invitations CSV — Column Reference and Format Guide](RC-IMP-06_Automated-Survey-Invitations-CSV.md)|
| **Synonyms** | how do i import a survey queue via csv; bulk edit survey queue conditions in a spreadsheet; copy survey queue setup to another project; upload survey queue configuration csv; set the order surveys appear to participants; conditional logic for which survey shows next; export and re-import survey queue settings; survey queue csv column reference |

---

## 1. Overview

The Survey Queue module supports CSV export and import of queue configurations. The survey queue defines the order and conditional logic that governs which surveys are presented to a participant after completing a prior survey.

**Location:** Online Designer → Survey Queue → "Upload or download survey queue" option.

**Upload behavior — Additive/update:** Each row is keyed on its survey (`form_name`, plus `event_name` in longitudinal projects). A row that matches an existing queue entry replaces it; a row for a survey that is not yet in the queue adds it. Queue entries not in the file are left unchanged. Uploading a file with no queue rows offers to delete the whole Survey Queue setup.

> **Important:** the Survey Queue is not part of Draft Mode. In a production project an uploaded file takes effect immediately for participants, so download the current setup first and test the file in a development copy of the project.

**Rights required:** Project Design and Setup.

**Always download first.** Start from a file exported from the project rather than building from scratch. This ensures the correct column structure and gives you a recovery snapshot. The upload option is available as soon as surveys are enabled in the project; the download option stays greyed out until at least one survey is active in the queue, so set up one entry in the Online Designer first if you need a template.

For full coverage of configuring the Survey Queue through the REDCap UI, see [RC-SURV-07 — Survey Queue](RC-SURV-07_Survey-Queue.md).

---

## 2. Column Reference

The columns depend on the project type:

- **Longitudinal projects:** eight columns, in the order shown below.
- **Classic (non-longitudinal) projects:** six columns — the same list without `event_name` and `condition_surveycomplete_event_name`.

The CSV holds only the per-survey queue entries. The queue's custom text and the setting that hides the queue from participants are not in the file; set them in the Survey Queue dialog.

| Column | Required | Accepted Values | Notes |
|---|---|---|---|
| `form_name` | Yes | Any survey-enabled instrument variable name | The instrument being added to the queue. Must match the instrument's internal name (lowercase, underscored) exactly. |
| `event_name` | Longitudinal: yes | A valid unique event name | Longitudinal projects only (classic projects do not have this column). Every row must name the event; a blank `event_name` is rejected as an invalid event name. |
| `active` | Yes | `1` or `0` | `1` = the instrument is activated in the queue and will be presented to participants when its condition is met. `0` (or blank) = the entry is deactivated. |
| `condition_surveycomplete_form_name` | No | Instrument variable name, or blank | Completion trigger — specifies which survey must be completed before this instrument is offered in the queue. Leave blank for logic-only triggers. |
| `condition_surveycomplete_event_name` | Longitudinal: with a completion trigger | Unique event name, or blank | Longitudinal projects only. Event of the completion-trigger survey. May reference an event from a different arm. Fill it in whenever `condition_surveycomplete_form_name` is set: a completion trigger without an event is dropped without an error. Leave blank for logic-only triggers. |
| `condition_andor` | Yes | `AND` or `OR` | Relationship between the completion trigger and the logic condition. **Always populate this column** — even when only one trigger type is configured, a blank value is rejected. Lowercase `and`/`or` is also accepted. Using `AND` with only one trigger type is equivalent to using that trigger alone. |
| `condition_logic` | No | Any valid REDCap branching logic expression, or blank | Additional logic condition that must be true for the survey to be offered. Cross-event field references use the format `[event_name][field_name]`. Leave blank for completion-trigger-only entries. Empty-string comparisons (`""`) are double-escaped in the raw CSV (see Common Mistakes). |
| `auto_start` | Yes | `1` or `0` (required) | `1` = REDCap automatically advances the participant to the next survey in the queue upon completion of the current survey. `0` = the participant is returned to the survey queue overview page and must manually select the next survey. |

Each row needs at least one trigger: a completion trigger (`condition_surveycomplete_form_name`), a `condition_logic` expression, or both.

> **What the download contains.** The downloaded file lists only **active** queue entries; deactivated entries are not exported. If the project is set to hide the survey queue from participants, the downloaded rows show `auto_start` as `1`. Check both points before re-uploading a downloaded file to another project.

---

## 3. Annotated Example

The file below shows a three-survey queue from a classic (non-longitudinal) project, so it has six columns. After completing `screening`, participants are automatically advanced to `demographics`. After completing `demographics`, they are advanced to `phq9` — but only if a screening eligibility field is set to `1`.

```csv
form_name,active,condition_surveycomplete_form_name,condition_andor,condition_logic,auto_start
demographics,1,screening,AND,,1
phq9,1,demographics,AND,[eligible]=1,1
```

Key points illustrated:

- **No event columns** — this is a classic project, so `event_name` and `condition_surveycomplete_event_name` are absent. In a longitudinal project both are filled in on every row that has a completion trigger.
- **`condition_andor` is always populated** — both rows use `AND` even though only one trigger type is configured per row.
- **`auto_start = 1`** — participants are pushed directly to the next survey without returning to the queue overview.
- **`condition_logic` is blank for `demographics`** — no logic condition is required; completion of `screening` alone is sufficient.
- **`condition_logic = [eligible]=1` for `phq9`** — the instrument is only queued if the participant passed the eligibility check recorded during screening.

---

## 4. Common Mistakes

**Leaving `condition_andor` blank.** REDCap requires this column even when only a completion trigger or only a logic condition is configured. A blank value is rejected. Use `AND` when only one trigger type is set.

**Using the instrument display label instead of the variable name.** Both `form_name` and `condition_surveycomplete_form_name` expect the internal instrument variable name (lowercase, underscored), not the display label shown in the Online Designer. For example, use `social_history`, not `Social History`.

**Editing empty-string conditions in a plain text editor.** If `condition_logic` contains an empty-string comparison (`""`), the raw CSV doubles every `"` and wraps the cell in quotes, so `[field]<>""` is written `"[field]<>"""""`. Plain-text editors that don't handle CSV quoting will corrupt this, causing the logic to fail on re-import. Use a spreadsheet application to edit these values.

**Forgetting `event_name` in longitudinal projects.** In a longitudinal project every row must name the survey's event; a blank `event_name` is rejected. Add one row per survey-event combination you want in the queue, using the unique event name.

**Leaving out the completion-trigger event in longitudinal projects.** If `condition_surveycomplete_form_name` is filled in but `condition_surveycomplete_event_name` is blank, the completion trigger is dropped without an error. Always fill in both, and check the queue in the Online Designer after uploading.

**Using a six- or eight-column file in the wrong project type.** Classic projects use six columns and longitudinal projects eight. Download from the target project to get the right layout.

**Assuming a re-uploaded download restores deactivated entries.** The download contains only active entries, so deactivated ones are not in the file. The upload itself can add new surveys to the queue as well as update existing ones, but a deactivated entry that is missing from the file stays as it is.

---

## 5. Related Articles

- [RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap](RC-IMP-03_CSV-Upload-Reference.md) (index of all CSV upload types in REDCap)
- [RC-SURV-07 — Survey Queue](RC-SURV-07_Survey-Queue.md) (full module reference including UI configuration)
- [RC-IMP-06 — Automated Survey Invitations CSV — Column Reference and Format Guide](RC-IMP-06_Automated-Survey-Invitations-CSV.md) (related: ASI format reference)
- [RC-SURV-01 — Surveys – Basics](RC-SURV-01_Surveys-Basics.md) (survey fundamentals)
- [RC-BL-01 — Branching Logic: Overview & Scope](RC-BL-01_Branching-Logic-Overview-and-Scope.md) (logic expression syntax used in `condition_logic`)
