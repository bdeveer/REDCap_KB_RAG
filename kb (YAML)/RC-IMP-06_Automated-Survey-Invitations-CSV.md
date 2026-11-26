---
id: RC-IMP-06
title: Automated Survey Invitations CSV — Column Reference and Format Guide
domain: Data Import
applies_to:
- All REDCap project types with surveys enabled
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — ASI CSV
  upload behaviour checked against source code; pages not re-captured
prerequisites:
- 'RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap'
- RC-SURV-06 — Automated Survey Invitations (ASI)
version: '1.1'
last_updated: 2026-11
related:
- id: RC-IMP-03
  title: 'CSV Upload Reference: All Bulk Upload Options in REDCap'
- id: RC-SURV-06
  title: Automated Survey Invitations (ASI)
- id: RC-SURV-07
  title: Survey Queue
tags:
- data import
- data
synonyms:
- how do i import automated survey invitations via csv
- bulk edit asi schedules in a spreadsheet
- copy automated survey invitation setup to another project
- asi csv column reference and format
- upload survey invitation configurations csv
- form_name and event_name key for asi import
- duplicate complex invitation schedules across projects
- asi import file column structure
---

# 1. Overview

The Automated Survey Invitations (ASI) module supports CSV export and import of invitation configurations. This allows bulk editing of invitation schedules outside of REDCap and copying a complex invitation setup from one project to another.

**Location:** Online Designer → "Auto Invitation options" dropdown (project-level, not per-instrument).

**Upload behavior — Additive/update:** ASIs matching the `form_name`/`event_name` key are updated; a row with no existing ASI for that survey and event creates one; ASIs not in the file are left unchanged. The upload cannot delete an ASI.

**Rights required:** Project Design and Setup (at least one survey must be enabled in the project).

**Always download first.** Start from an exported file rather than building from scratch, both to get the correct column structure and to have a recovery snapshot. A current export has 34 columns in a longitudinal project and 32 in a classic project (no `event_name` or `condition_surveycomplete_event_name`).

Columns are matched by their header name, so column order does not matter, and a column missing from the file is given its default value rather than causing an error. However, a row whose number of cells does not match the header row is skipped without a warning — check after upload that every ASI you expected was updated.

> **Version caveat (LTS 16.0):** The `condition_reevaluate_send_time` column is present in 17.3 LTS and 17.6 but not in 16.0 LTS, where an export has 33 columns (31 in a classic project). If you copy ASIs from a 16.0 project to a newer one, the column is simply given its default (off); set it in the file or in the Online Designer afterwards if you need it.

**All-or-nothing.** If any row fails validation (for example an unknown `form_name` or `event_name`, or a missing required value), no changes from the file are saved. Fix the reported rows and upload again.

For full coverage of configuring ASIs through the REDCap UI, see [RC-SURV-06 — Automated Survey Invitations (ASI)](RC-SURV-06_Automated-Survey-Invitations.md) — Automated Survey Invitations.

---

# 2. Column Reference

| **Column** | **Values / Format** | **Notes** |
|---|---|---|
| `form_name` | Instrument variable name | The survey being invited |
| `event_name` | Unique event name (e.g. `baseline_arm_1`) | Longitudinal only; the column is not in a classic project's file. Together with `form_name` it identifies the ASI |
| `condition_surveycomplete_form_name` | Instrument variable name | Completion trigger: instrument that must complete before the invitation fires |
| `condition_surveycomplete_event_name` | Unique event name | Completion trigger: at which event (longitudinal only; required when `condition_surveycomplete_form_name` is set) |
| `num_recurrence` | Integer | Delay between repeating instances; `0` in non-repeating configs. Forced to `0` if the survey is not a repeating instrument or in a repeating event |
| `units_recurrence` | `DAYS` / `HOURS` / `MINUTES` | Unit for the recurrence delay |
| `max_recurrence` | Integer or blank | Maximum repeats; blank = unlimited |
| `active` | `1` / `0` | `1` = Active, `0` = Not Active. A blank or any other value is saved as `0`, which deactivates the ASI |
| `email_subject` | Plain text | Subject line |
| `email_content` | HTML | Full email body as HTML; piping and smart variables stored literally (e.g. `[survey-link]`) |
| `email_sender` | Email address | From address. Required, and must be the email address of a user in the project |
| `email_sender_display` | Text or blank | From display name; blank = email address used as display |
| `condition_andor` | `AND` / `OR` | Relationship between completion and logic triggers; present even when only one trigger type is configured. Blank is read as `AND` |
| `condition_logic` | Branching logic expression | Empty-string comparisons (`""`) are double-escaped in CSV — `[record_id]<>""` appears as `[record_id]<>""""` in the raw file |
| `condition_send_time_option` | `IMMEDIATELY` / `TIME_LAG` / `NEXT_OCCURRENCE` / `EXACT_TIME` | Selects the timing mode (see Section 3 below). There is no separate field-date mode: scheduling relative to a date field is `TIME_LAG` plus `condition_send_time_lag_field` |
| `condition_send_time_lag_days` | Integer or blank | Lag days; used when `TIME_LAG` |
| `condition_send_time_lag_hours` | Integer or blank | Lag hours; used when `TIME_LAG` |
| `condition_send_time_lag_minutes` | Integer or blank | Lag minutes; used when `TIME_LAG` |
| `condition_send_time_lag_field` | Field variable name or blank | Date/datetime field to schedule relative to; used with `TIME_LAG` (the lag is then counted from the field's date instead of from the trigger) |
| `condition_send_time_lag_field_after` | `before` / `after` or blank | Direction relative to the field date; used with `condition_send_time_lag_field` |
| `condition_reevaluate_send_time` | `1` / `0` | **17.3 LTS and 17.6 only (see the version caveat in Section 1).** `1` = "Re-evaluate the send-time for scheduled invitations when this field's value is updated?" is enabled: when the date field in `condition_send_time_lag_field` changes, REDCap moves the send time of invitations that are still scheduled. Only applies to `TIME_LAG` ASIs that use a date field |
| `condition_send_next_day_type` | `DAY` / `WEEKDAY` / `WEEKENDDAY` / `SUNDAY` … `SATURDAY` or blank | Day type to target; used when `NEXT_OCCURRENCE` |
| `condition_send_next_time` | `HH:MM` or blank | Time of day; used when `NEXT_OCCURRENCE` |
| `condition_send_time_exact` | `YYYY-MM-DD HH:MM:SS` or blank | Full date and time; used when `EXACT_TIME`. Use this format: other date formats are read using your own My Profile date format |
| `delivery_type` | `EMAIL` / `PARTICIPANT_PREF` / `VOICE_INITIATE` / `SMS_INITIATE` / `SMS_INVITE_MAKE_CALL` / `SMS_INVITE_RECEIVE_CALL` / `SMS_INVITE_WEB` | Delivery method; every value other than `EMAIL` requires texting/voice calls to be enabled for surveys in the project |
| `reminder_type` | `TIME_LAG` / `NEXT_OCCURRENCE` / `EXACT_TIME` or blank | Reminder timing mode; blank = no reminders |
| `reminder_timelag_days` | Integer or blank | Reminder lag days; used when `reminder_type = TIME_LAG` |
| `reminder_timelag_hours` | Integer or blank | Reminder lag hours; used when `TIME_LAG` |
| `reminder_timelag_minutes` | Integer or blank | Reminder lag minutes; used when `TIME_LAG` |
| `reminder_nextday_type` | `DAY` / `WEEKDAY` / `WEEKENDDAY` / `SUNDAY` … `SATURDAY` or blank | Used when `reminder_type = NEXT_OCCURRENCE` |
| `reminder_nexttime` | `HH:MM` or blank | Used when `NEXT_OCCURRENCE` reminder |
| `reminder_exact_time` | `YYYY-MM-DD HH:MM:SS` or blank | Used when `EXACT_TIME` reminder |
| `reminder_num` | Integer `0`–`5` | Number of reminders; `0` = none |
| `reeval_before_send` | `1` / `0` | `1` = "Ensure logic is still true before sending invitation" is enabled |

---

# 3. Timing Modes (`condition_send_time_option`)

| **Mode** | **Active columns** | **Behavior** |
|---|---|---|
| `IMMEDIATELY` | — | Invitation sent as soon as trigger fires |
| `TIME_LAG` | `condition_send_time_lag_days/hours/minutes` | Sent N days/hours/minutes after the trigger |
| `TIME_LAG` with a date field | lag columns, `condition_send_time_lag_field`, `condition_send_time_lag_field_after` (and, on 17.3 LTS / 17.6, `condition_reevaluate_send_time`) | Sent N days/hours/minutes before or after a date stored in a project field |
| `NEXT_OCCURRENCE` | `condition_send_next_day_type`, `condition_send_next_time` | Sent on the next matching day at a specific time. Example: `WEEKDAY` + `10:32` = next weekday at 10:32 AM |
| `EXACT_TIME` | `condition_send_time_exact` | Sent at an absolute date and time (`YYYY-MM-DD HH:MM:SS`) |

---

# 4. Common Mistakes

**Quote escaping in logic.** When `condition_logic` contains an empty-string comparison (`""`), the raw CSV value will have doubled double-quotes — `[record_id]<>""` appears as `[record_id]<>""""` in the file. Spreadsheet applications handle this transparently; plain-text editors will show the raw encoding and can corrupt it.

**HTML in `email_content`.** The body is stored as HTML. Prefer editing email content within the REDCap UI, or use a dedicated HTML editor and paste the result into the cell.

**Removing columns from the export.** Columns are matched by name, so reordering is harmless, but keep every column from the export: a missing column silently falls back to its default (a missing `active` column, for example, turns every ASI in the file off). Reminder columns are always present even when `reminder_num = 0`. Make sure every row has the same number of cells as the header — a row that doesn't is skipped without a warning.

**Leaving `active` blank.** A blank `active` cell is saved as `0` (Not Active). Set it to `1` for every ASI that should keep sending.

**Missing trigger or sender.** Each row needs `email_sender` (a project user's email address) and at least one trigger: `condition_surveycomplete_form_name` or `condition_logic`. A row without them fails the upload, and because the upload is all-or-nothing, nothing in the file is saved.

**`condition_andor` is always populated.** It contains `AND` or `OR` even when only one trigger type is configured. Leave it as-is; a blank value is read as `AND`.

---

# 5. Related Articles

- [RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap](RC-IMP-03_CSV-Upload-Reference.md) (index of all CSV upload types in REDCap)
- [RC-SURV-06 — Automated Survey Invitations (ASI)](RC-SURV-06_Automated-Survey-Invitations.md) (full module reference)
- [RC-SURV-07 — Survey Queue](RC-SURV-07_Survey-Queue.md) (survey queue CSV format — [RC-IMP-07 — Survey Settings CSV — Column Reference and Format Guide](RC-IMP-07_Survey-Settings-CSV.md))
- [RC-PIPE-01 — Piping: Basics, Syntax & Field Types](RC-PIPE-01_Piping-Basics-Syntax-and-Field-Types.md) (piping syntax used in email content)
