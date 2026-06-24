

**Automated Survey Invitations CSV — Column Reference and Format Guide**

| **Article ID** | [RC-IMP-06 — Automated Survey Invitations CSV — Column Reference and Format Guide](RC-IMP-06_Automated-Survey-Invitations-CSV.md) |
|---|---|
| **Domain** | Data Import |
| **Applies To** | All REDCap project types with surveys enabled |
| **Prerequisite** | [RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap](RC-IMP-03_CSV-Upload-Reference.md); [RC-SURV-06 — Automated Survey Invitations (ASI)](RC-SURV-06_Automated-Survey-Invitations.md)|
| **Skill Level** | Intermediate |
| **Version** | 1.0 |
| **Last Updated** | 2026-05-07 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap](RC-IMP-03_CSV-Upload-Reference.md); [RC-SURV-06 — Automated Survey Invitations (ASI)](RC-SURV-06_Automated-Survey-Invitations.md); [RC-SURV-07 — Survey Queue](RC-SURV-07_Survey-Queue.md) |
| **Synonyms** | how do i import automated survey invitations via csv; bulk edit asi schedules in a spreadsheet; copy automated survey invitation setup to another project; asi csv column reference and format; upload survey invitation configurations csv; form_name and event_name key for asi import; duplicate complex invitation schedules across projects; 32-column asi import file structure |

---

## 1. Overview

The Automated Survey Invitations (ASI) module supports CSV export and import of invitation configurations. This allows bulk editing of invitation schedules outside of REDCap and copying a complex invitation setup from one project to another.

**Location:** Online Designer → "Automated Survey Invitations" button (project-level, not per-instrument).

**Upload behavior — Additive/update:** ASIs matching the `form_name`/`event_name` key are updated; others are left unchanged.

**Rights required:** Project Design and Setup (at least one survey must be enabled in the project).

**Always download first.** Start from an exported file rather than building from scratch, both to get the correct 32-column structure and to have a recovery snapshot.

For full coverage of configuring ASIs through the REDCap UI, see [RC-SURV-06 — Automated Survey Invitations (ASI)](RC-SURV-06_Automated-Survey-Invitations.md) — Automated Survey Invitations.

---

## 2. Column Reference

| **Column** | **Values / Format** | **Notes** |
|---|---|---|
| `form_name` | Instrument variable name | The survey being invited |
| `event_name` | Unique event name (e.g. `baseline_arm_1`) | Longitudinal only; blank in classic projects |
| `condition_surveycomplete_form_name` | Instrument variable name | Completion trigger: instrument that must complete before the invitation fires |
| `condition_surveycomplete_event_name` | Unique event name | Completion trigger: at which event (longitudinal) |
| `num_recurrence` | Integer | Delay between repeating instances; `0` in non-repeating configs |
| `units_recurrence` | `DAYS` / `HOURS` / `MINUTES` | Unit for the recurrence delay |
| `max_recurrence` | Integer or blank | Maximum repeats; blank = unlimited |
| `active` | `1` / `0` | `1` = Active, `0` = Not Active |
| `email_subject` | Plain text | Subject line |
| `email_content` | HTML | Full email body as HTML; piping and smart variables stored literally (e.g. `[survey-link]`) |
| `email_sender` | Email address | From address |
| `email_sender_display` | Text or blank | From display name; blank = email address used as display |
| `condition_andor` | `AND` / `OR` | Relationship between completion and logic triggers; present even when only one trigger type is configured |
| `condition_logic` | Branching logic expression | Empty-string comparisons (`""`) are double-escaped in CSV — `[record_id]<>""` appears as `[record_id]<>""""` in the raw file |
| `condition_send_time_option` | `IMMEDIATELY` / `TIME_LAG` / `NEXT_OCCURRENCE` / `FIELD_DATE` / `EXACT_TIME` | Selects the timing mode (see Section 3 below) |
| `condition_send_time_lag_days` | Integer or blank | Lag days; used when `TIME_LAG` |
| `condition_send_time_lag_hours` | Integer or blank | Lag hours; used when `TIME_LAG` |
| `condition_send_time_lag_minutes` | Integer or blank | Lag minutes; used when `TIME_LAG` |
| `condition_send_time_lag_field` | Field variable name or blank | Date/datetime field to schedule relative to; used when `FIELD_DATE` |
| `condition_send_time_lag_field_after` | `before` / `after` or blank | Direction relative to the field date; used when `FIELD_DATE` |
| `condition_send_next_day_type` | `after` / `same` / `before` or blank | Day relative to trigger; used when `NEXT_OCCURRENCE` |
| `condition_send_next_time` | `WEEKDAY` / `EVERYDAY` / `WEEKEND` or blank | Day type to target; used when `NEXT_OCCURRENCE` |
| `condition_send_time_exact` | `HH:MM:SS` or blank | Exact time of day; used when `NEXT_OCCURRENCE` or `EXACT_TIME` |
| `delivery_type` | `EMAIL` / `SMS` / `VOICE` / `PREFERENCE` | Delivery method; `SMS` and `VOICE` require texting to be enabled |
| `reminder_type` | `TIME_LAG` / `NEXT_DAY` / `EXACT_TIME` or blank | Reminder timing mode; blank = no reminders |
| `reminder_timelag_days` | Integer or blank | Reminder lag days; used when `reminder_type = TIME_LAG` |
| `reminder_timelag_hours` | Integer or blank | Reminder lag hours; used when `TIME_LAG` |
| `reminder_timelag_minutes` | Integer or blank | Reminder lag minutes; used when `TIME_LAG` |
| `reminder_nextday_type` | Day type or blank | Used when `reminder_type = NEXT_DAY` |
| `reminder_nexttime` | Time or blank | Used when `NEXT_DAY` reminder |
| `reminder_exact_time` | `HH:MM:SS` or blank | Used when `EXACT_TIME` reminder |
| `reminder_num` | Integer `0`–`5` | Number of reminders; `0` = none |
| `reeval_before_send` | `1` / `0` | `1` = "Ensure logic is still true before sending invitation" is enabled |

---

## 3. Timing Modes (`condition_send_time_option`)

| **Mode** | **Active columns** | **Behavior** |
|---|---|---|
| `IMMEDIATELY` | — | Invitation sent as soon as trigger fires |
| `TIME_LAG` | `condition_send_time_lag_days/hours/minutes` | Sent N days/hours/minutes after the trigger |
| `NEXT_OCCURRENCE` | `condition_send_next_day_type`, `condition_send_next_time`, `condition_send_time_exact` | Sent on the next matching day type at a specific time. Example: `after` + `WEEKDAY` + `10:32:00` = next weekday at 10:32 AM |
| `FIELD_DATE` | `condition_send_time_lag_field`, `condition_send_time_lag_field_after`, lag columns | Sent N days/hours/minutes before or after a date stored in a project field |
| `EXACT_TIME` | `condition_send_time_exact` | Sent at an absolute date and time |

---

## 4. Common Mistakes

**Quote escaping in logic.** When `condition_logic` contains an empty-string comparison (`""`), the raw CSV value will have doubled double-quotes — `[record_id]<>""` appears as `[record_id]<>""""` in the file. Spreadsheet applications handle this transparently; plain-text editors will show the raw encoding and can corrupt it.

**HTML in `email_content`.** The body is stored as HTML. Prefer editing email content within the REDCap UI, or use a dedicated HTML editor and paste the result into the cell.

**All 32 columns must be present.** Do not add, remove, or reorder columns — REDCap expects the exact structure on import. Reminder columns are always present even when `reminder_num = 0`.

**`condition_andor` is always populated.** It contains `AND` or `OR` even when only one trigger type is configured. Leave it as-is — do not blank it out.

---

## 5. Related Articles

- [RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap](RC-IMP-03_CSV-Upload-Reference.md)(index of all CSV upload types in REDCap)
- [RC-SURV-06 — Automated Survey Invitations (ASI)](RC-SURV-06_Automated-Survey-Invitations.md)(full module reference)
- [RC-SURV-07 — Survey Queue](RC-SURV-07_Survey-Queue.md) (survey queue CSV format — [RC-IMP-07 — Survey Settings CSV — Column Reference and Format Guide](RC-IMP-07_Survey-Settings-CSV.md))
- [RC-PIPE-01 — Piping: Basics, Syntax & Field Types](RC-PIPE-01_Piping-Basics-Syntax-and-Field-Types.md)(piping syntax used in email content)
