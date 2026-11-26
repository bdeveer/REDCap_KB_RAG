---
id: RC-IMP-05
title: Alerts & Notifications CSV — Column Reference and Format Guide
domain: Data Import
applies_to:
- All REDCap project types
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — alerts
  CSV upload behaviour checked against source code; pages not re-captured
prerequisites:
- 'RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap'
- 'RC-ALERT-01 — Alerts & Notifications: Setup'
version: '1.4'
last_updated: 2026-11
related:
- id: RC-IMP-03
  title: 'CSV Upload Reference: All Bulk Upload Options in REDCap'
- id: RC-ALERT-01
  title: 'Alerts & Notifications: Setup'
- id: RC-ALERT-02
  title: Alert Management & Notification Log
tags:
- data import
- data
synonyms:
- how do i import alerts via csv
- bulk edit alerts and notifications in a spreadsheet
- copy alert configurations from one project to another
- upload alert definitions csv
- alert-unique-id column format for import
- export and re-import alerts and notifications
- duplicate alerts across projects without rebuilding
- a&n csv column reference
- recurring alert reminders in the alerts csv
- send-on-date format for alert upload
- alert date imported as the wrong month
---

# 1. Overview

The Alerts & Notifications module supports CSV export and import of alert definitions. This allows bulk editing of alerts outside of REDCap and copying alert configurations from one project to another without rebuilding them by hand.

**Location:** Applications → Alerts & Notifications → "Upload or download alerts" button.

**Upload behavior — Additive:** Imported alerts are added to the existing list. Existing alerts are not overwritten unless you are re-importing with matching `alert-unique-id` values. A row with a blank `alert-unique-id` creates a new alert, added at the end of the list; an ID that doesn't exist in the project is an error. The CSV can't delete alerts: set `alert-deactivated` to `Y`, or delete the alert on the Alerts & Notifications page.

**Two steps, all or nothing:** REDCap first shows a preview of the changes, and nothing is saved until you confirm it. If any row has an error, no rows are imported.

**Columns are matched by header name**, so column order doesn't matter, but every column in the destination project's template must be present. The file must use the CSV delimiter set in your My Profile preferences.

**Rights required:** Alerts & Notifications user right.

**Always download first.** Start from a file exported from the source project rather than building from scratch. This guarantees the correct column order and gives you a recovery snapshot.

For general coverage of the Alerts & Notifications module, see [RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md).

---

# 2. Column Reference

Each row in the file represents one alert. The table below documents every column, in the order an export writes them.

Every column header must be present, but many values can be left blank. "Required" below refers to the value: where a column shows a default, a blank cell gets that default. A value that isn't one of the listed codes is **not** rejected; REDCap silently replaces it with the default, so a misspelled code produces a working but wrong alert. Check the preview before confirming.

| Column | Required | Accepted Values / Notes |
|---|---|---|
| `alert-unique-id` | No (new) / Yes (update) | REDCap-assigned identifier in the format `A-XXXX` (e.g., `A-2482`). Leave blank when creating new alerts — REDCap assigns the ID on import. Required when updating specific existing alerts; an ID that doesn't exist in the project is rejected. |
| `alert-title` | No | Free-text display name. Optional but strongly recommended; this is the primary identifier in the Alerts management view and the notification log. |
| `alert-trigger` | Yes | `SUBMIT` — "When a record is saved on a specific form/survey" (completion trigger). `SUBMIT-LOGIC` — "If conditional logic is TRUE when a record is saved on a specific form/survey" (combination trigger). `LOGIC` — "When conditional logic is TRUE during a data import, data entry, or as the result of time-based logic" (logic trigger). With `SUBMIT`, any `alert-condition` in the row is discarded on upload. |
| `unique-form-name` | Yes (`SUBMIT`, `SUBMIT-LOGIC`) | The instrument's unique name (variable name, not display label); specifies which instrument save activates the alert. Leave blank for `LOGIC` triggers. |
| `unique-event-name` | No | The event's unique name (e.g., `baseline_arm_1`). This column only exists in longitudinal projects; a classic project's template doesn't have it. When blank in a longitudinal project, the alert applies to any event where the instrument appears. Event context for recipients and message content is specified via piping syntax inside `email-to` and `alert-message` instead. |
| `saved-with-form-status` | No (default `ANY`) | `COMPLETE` — fires only when the instrument is saved with Complete status (value 2). `ANY` — fires on any save status; this is what an export writes for `LOGIC` alerts. Blank means `ANY`. |
| `alert-condition` | Conditional | Logic expression string (same syntax as branching logic). Required for `SUBMIT-LOGIC` and `LOGIC` triggers. Leave blank for `SUBMIT`. |
| `ensure-logic-still-true` | No (default `N`) | `Y` or `N`. When `Y`, REDCap re-evaluates the trigger logic immediately before sending. If the logic is no longer true at send time, the queued alert is cancelled. Most useful when the alert has a scheduled delay. |
| `do-not-clear-recurrences` | No (default `N`) | `Y` or `N`. Controls whether a new trigger event clears previously queued recurrences for the same record. |
| `alert-stop-type` | No (default `RECORD`) | Trigger limit — how many times the alert can fire. `RECORD` — only once per record (never re-trigger). `RECORD_INSTRUMENT` — only once per instrument, regardless of event. `RECORD_EVENT` — only once per event in a record. `RECORD_EVENT_INSTRUMENT` — only once per instrument per event (will not re-trigger on each repeating instance). `RECORD_EVENT_INSTRUMENT_INSTANCE` — once per event and also on every instance of a repeating instrument/event. |
| `send-on` | No (default `NOW`) | When to send after the trigger fires. `NOW` — immediately. `NEXT_OCCURRENCE` — on the next occurrence of a day type at a set time (configure with `send-on-next-day-type` and `send-on-next-time`). `TIME_LAG` — after a delay (configure with the three `send-on-time-lag-*` columns); to send relative to a date stored in a project field, also fill `send-on-field` and `send-on-field-after`. `DATE` — at a specific date/time (configure with `send-on-date`). There is no separate code for field-based sends. Columns that belong to a different `send-on` option are cleared on upload. |
| `send-on-next-day-type` | Conditional (default `DAY`) | For `NEXT_OCCURRENCE` sends: `DAY`, `WEEKDAY`, `WEEKENDDAY`, `SUNDAY`, `MONDAY`, `TUESDAY`, `WEDNESDAY`, `THURSDAY`, `FRIDAY` or `SATURDAY`. Leave blank otherwise. |
| `send-on-next-time` | Conditional | Time component (HH:MM) for `NEXT_OCCURRENCE` sends. Leave blank otherwise. |
| `send-on-time-lag-days` | Conditional | Number of days for `TIME_LAG` delay. All three lag columns (`days`, `hours`, `minutes`) must be specified together — use `0` for units not needed. |
| `send-on-time-lag-hours` | Conditional | Hours component of `TIME_LAG` delay. Use `0` if not needed. |
| `send-on-time-lag-minutes` | Conditional | Minutes component of `TIME_LAG` delay. Use `0` if not needed. |
| `send-on-field-after` | Conditional (default `AFTER`) | For `TIME_LAG` sends: `AFTER` or `BEFORE`. With `send-on-field` filled, the lag is counted after or before the date in that field. Leave blank for other `send-on` options. |
| `send-on-field` | Conditional | For `TIME_LAG` sends relative to a date: the project field holding the reference date. Copy the format from an export of a working alert. Leave blank otherwise. |
| `reevaluate-send-time` | No (default `N`) | `Y` or `N`. The UI option "Re-evaluate the send-time for scheduled notifications when this field's value is updated?" Only relevant when `send-on-field` is used. See the version caveat below this table. |
| `send-on-date` | Conditional | Specific date/time for `DATE` sends, in the server's time zone. The error message asks for `M/D/Y H:M`, but the date is read using the uploading user's own date format from My Profile: see Common Mistakes. Always check the date in the UI after uploading. Leave blank otherwise. |
| `alert-send-how-many` | No (default `ONCE`) | `ONCE` — "Just once". `EVERY` — "Every time the form/survey in Step 1B is saved" (choose the variant in `every-time-type`). `SCHEDULE` — "Multiple times on a recurring basis" (configure with `repeat-for`, `repeat-for-units`, `repeat-for-max`). **Not `MULTIPLE`**: Observed on REDCap 17.5.10 (Standard) it is rejected. |
| `every-time-type` | Conditional (default `EVERY`) | Only for `alert-send-how-many` = `EVERY`: `EVERY` — every time the instrument is saved. `EVERY-CHANGE` — every time it is saved with new or modified data, ignoring calc fields. `EVERY-CHANGE-CALCS` — every time it is saved with new or modified data, including calc fields. Leave blank for `ONCE` and `SCHEDULE`; it is cleared on upload for those. |
| `repeat-for` | Conditional | Numeric interval between recurring sends. |
| `repeat-for-units` | Conditional (default `DAYS`) | Unit for `repeat-for`: `DAYS`, `HOURS` or `MINUTES`. |
| `repeat-for-max` | Conditional | Maximum number of sends including the first. **Always set this** — leaving it blank causes REDCap to send indefinitely. |
| `alert-expiration` | No | Date/time after which REDCap will not send any further instances of this alert, and will cancel any already-queued ones. Read with your My Profile date format, like `send-on-date`. |
| `alert-type` | No (default `EMAIL`) | `EMAIL` — standard email (always available). `SMS` — text message (if enabled). `VOICE_CALL` — voice call (if enabled). `SENDGRID_TEMPLATE` — SendGrid template delivery (if configured). |
| `email-from-display` | No | Optional display name for the from address (e.g., `Heart Study Team`). Leave blank to use the raw email address as the display name. |
| `email-from` | Yes (email) | The from email address. Must be the primary, secondary or tertiary email address of a current project user, and must be written in **lowercase** in the file: see Common Mistakes. |
| `email-to` | Yes (email) | Recipient(s). Accepts: a static email address; a project field variable (`[field_name]`); or an event-prefixed field variable for longitudinal projects (`[event_name][field_name]`, e.g., `[baseline_arm_1][contact_email]`). Multiple recipients separated by semicolons. Whether free-form addresses and piped recipients are allowed depends on your administrator's settings. |
| `email-cc` | No | CC recipient(s). Same syntax as `email-to`. |
| `email-bcc` | No | BCC recipient(s). Same syntax as `email-to`. |
| `email-failed` | No | Email address to notify if REDCap fails to deliver the alert. Only one address is accepted. |
| `email-subject` | Yes (email) | Subject line. Supports piping syntax. Avoid piping identifiers here unless the `prevent-piping-identifiers` column is set to `N`. |
| `alert-message` | Yes | The message body. Supports HTML, piped variables, and smart variables (e.g., `[survey-link:instrument_name:Link text]`). In longitudinal projects, prefix survey link smart variables with the target event: `[event_name][survey-link:instrument_name:Link text]`. The field can span multiple lines in the CSV — the entire value is quoted. |
| `prevent-piping-identifiers` | No (default `Y`) | `Y` or `N`. When `Y` (the default in the UI), REDCap strips identifier field values from piped content before sending. Set to `N` only when intentional identifier piping has been confirmed as appropriate with your IRB. |
| `file-upload-fields` | No | Semicolon-separated list of file upload fields, written as `[field_name]`, or `[event_name][field_name]` in longitudinal projects. Files stored in these fields for the triggering record are attached to the alert email. Leave blank if no attachments are needed. |
| `phone-number-to` | Conditional | Phone number for SMS or voice call alerts. Leave blank for email. |
| `alert-deactivated` | No | `Y` — alert is inactive and will not fire. `N` — alert is active. Blank means `N` for a new alert and keeps the current status for an existing one. |
| `sendgrid-template-id` | Conditional | SendGrid template ID. Leave blank for standard email alerts. |
| `sendgrid-template-data` | No | JSON object of SendGrid template variables. Only checked for `SENDGRID_TEMPLATE` alerts; blank is fine otherwise. An export writes `{}`. |
| `sendgrid-mail-send-configuration` | No | JSON object of custom SendGrid mail send configuration. Only checked for `SENDGRID_TEMPLATE` alerts; blank is fine otherwise. An export writes `{}`. |

> **Version caveat (17.x vs 16.0 LTS):** The `reevaluate-send-time` column is present in 17.6 Standard and 17.3 LTS but not in 16.0 LTS. Because every template column must be present, a file downloaded from a 16.0 LTS server fails on a 17.x server until you add a `reevaluate-send-time` column (`N` keeps the old behaviour); remove the column when uploading to 16.0 LTS. Simplest: download a fresh template from the destination project.

---

# 3. Annotated Example

The file below contains two alerts from a longitudinal project with two arms (`baseline_arm_1` and `3_month_arm_1`). It uses the 17.x column set; on 16.0 LTS the `reevaluate-send-time` column doesn't exist (see the version caveat in Section 2):

**Alert A-2482 — "Invite baseline"**
Fires immediately when the `screening` form is saved with Complete status. Sends once per record. Emails the participant at the address stored in `[baseline_arm_1][contact_email]`. The message body contains a survey link to the `demographics` instrument at the baseline event.

**Alert A-2483 — "Invite 3 months"**
Same trigger as A-2482 (screening form Complete), but scheduled to send 90 days later (`TIME_LAG`, 90 days, 0 hours, 0 minutes). The message links to the `phq9` instrument at the `3_month_arm_1` event. The event prefix on the survey link (`[3_month_arm_1][survey-link:phq9:Start here]`) ensures REDCap generates a link to the correct event, not the baseline event.

```csv
alert-unique-id,alert-title,alert-trigger,unique-form-name,unique-event-name,saved-with-form-status,alert-condition,ensure-logic-still-true,do-not-clear-recurrences,alert-stop-type,send-on,send-on-next-day-type,send-on-next-time,send-on-time-lag-days,send-on-time-lag-hours,send-on-time-lag-minutes,send-on-field-after,send-on-field,reevaluate-send-time,send-on-date,alert-send-how-many,every-time-type,repeat-for,repeat-for-units,repeat-for-max,alert-expiration,alert-type,email-from-display,email-from,email-to,email-cc,email-bcc,email-failed,email-subject,alert-message,prevent-piping-identifiers,file-upload-fields,phone-number-to,alert-deactivated,sendgrid-template-id,sendgrid-template-data,sendgrid-mail-send-configuration
A-2482,"Invite baseline",SUBMIT,screening,,COMPLETE,,N,N,RECORD,NOW,,,,,,,,N,,ONCE,,,,,,EMAIL,,study@institution.edu,[baseline_arm_1][contact_email],,,,"Invite for baseline","<p>Hi,</p><p>Please complete the baseline forms:</p><p>[baseline_arm_1][survey-link:demographics:Start here]</p><p>thanks,</p><p>Study team</p>",N,,,N,,{},{}
A-2483,"Invite 3 months",SUBMIT,screening,,COMPLETE,,N,N,RECORD,TIME_LAG,,,90,0,0,AFTER,,N,,ONCE,,,,,,EMAIL,,study@institution.edu,[baseline_arm_1][contact_email],,,,"Invite for 3 months","<p>Hi,</p><p>Please complete the 3-month forms:</p><p>[3_month_arm_1][survey-link:phq9:Start here]</p><p>thanks,</p><p>Study team</p>",N,,,N,,{},{}
```

---

# 4. Common Mistakes

**Misspelling a code.** A value that isn't one of the listed codes doesn't cause an error: REDCap quietly replaces it with the column's default. For example, `VOICE` in `alert-type` becomes `EMAIL` (the code is `VOICE_CALL`), and `FIELD` in `send-on` becomes `NOW` (field-based sends use `TIME_LAG` with `send-on-field`). Copy codes from Section 2 or from an export, and read the preview before confirming.

**Using `SUBMIT` for a combination trigger.** With `alert-trigger` = `SUBMIT`, the upload discards whatever is in `alert-condition`, so the alert fires on every qualifying save. For "form saved and logic true", use `SUBMIT-LOGIC`.

**Omitting the event prefix on `email-to` in a longitudinal project.** Writing `[contact_email]` without an event prefix may resolve to the wrong event or fail entirely if the field appears at multiple events. Always use `[event_name][field_name]` form for longitudinal recipients.

**Omitting the event prefix in `alert-message` survey links.** `[survey-link:phq9]` without an event prefix is ambiguous in a longitudinal project where the instrument appears at multiple events. Always write `[event_name][survey-link:instrument_name:Link text]`.

**Specifying only `send-on-time-lag-days` for a TIME_LAG send.** All three lag columns — days, hours, and minutes — must be present. Use `0` for the units you don't need; don't leave them blank.

**Using `MULTIPLE` for recurring sends.** The value for "Multiple times on a recurring basis" is `SCHEDULE`. Observed on REDCap 17.5.10 (Standard): a row with `MULTIPLE` is rejected with "repeat-for should be 0 or blank if alert-send-how-many='ONCE'", because REDCap doesn't recognise the value and treats the row as `ONCE`. Use `SCHEDULE` with `repeat-for`, `repeat-for-units` and `repeat-for-max`. `repeat-for-max` counts the first send: 3 means the first send plus two reminders.

**Trusting the error message about the `send-on-date` format.** If the date can't be parsed, the upload error says "Date must be in the M/D/Y H:M format". Observed on REDCap 17.5.10 (Standard): an uploaded `11/10/2026 06:00`, meant as 10 November in M/D/Y, was stored as **11 October**, so the value was read day-first. The export, though, writes the date month-first (that same alert exported as `10/11/2026 06:00`), so an exported file can't safely be re-uploaded unchanged when the day is 12 or lower. The cause: the date is checked against M/D/Y but saved using the uploading user's own date format from My Profile (the same applies to `alert-expiration`). Write dates as M/D/Y in the file only if your My Profile date format is M/D/Y; otherwise write them in your profile's format, or switch your profile to M/D/Y before uploading. After every upload, open the alert and check the date and time it shows, and remember the time is server time.

**Expecting a newly activated alert to pick up records that already meet its logic.** A `LOGIC` alert is checked when a record is saved or imported, so switching an alert on, or uploading it, doesn't queue anything for records that were already true. Either save or import those records after the alert is active (an API import that sets the trigger field works), or use **Re-evaluate Alerts** on the management page, with Test Run first. See [RC-ALERT-02 — Alert Management & Notification Log](RC-ALERT-02_Alert-Management-and-Notification-Log.md).

**Leaving `alert-send-how-many` blank or omitting the repeat cap.** For recurring alerts, always set `repeat-for-max`. Without it, REDCap sends indefinitely.

**Building the import file from scratch instead of from an export.** Columns are matched by header name, so order doesn't matter, but every column in the destination project's template must be present. The column set varies: a classic (non-longitudinal) project's template has no `unique-event-name` column, and 17.x templates have a `reevaluate-send-time` column that 16.0 LTS templates lack. Always download an existing alert from the destination project first and edit that file, so the column set matches exactly. This is the same reason Section 1 advises "Always download first."

**Copying longitudinal recipients into a classic project.** When alerts are copied from a longitudinal project into a classic one, an error that points at an email column usually means a recipient is still written as `[event_name][field_name]`. Classic projects have no events: change those to `[field_name]` in the recipient columns, and check `alert-message` and `file-upload-fields` for event prefixes too.

**Using capital letters in `email-from`.** The upload compares the address exactly as typed against the lowercase form of every current project user's email addresses (primary, secondary and tertiary). An address with any capital letter (e.g., `REDCap@example.edu`) is rejected with "Alert sender is invalid", even though the address genuinely exists on a profile. Write the address in all lowercase (`redcap@example.edu`).

**Pro tip — splitting one existing alert into two or more.** If you need to break an existing alert's scope into separate alerts (for example, an alert covering two instance/branch conditions gets split into one alert per condition so each can have its own message body), you don't need to invent brand-new IDs for all of them. Reuse the existing alert's ID for one of the new conditions — narrow its `alert-condition` logic and edit its message as needed — and leave `alert-unique-id` **blank** on the additional row(s) for the new condition(s) you're spinning off. This preserves the original alert's send history/notification-log continuity for the condition that stays on its ID, while cleanly creating the rest as new alerts. Inventing IDs for the new rows (rather than reusing a real one or leaving the column blank) will fail on import with "unique alert ID does not exist."

---

# 5. Related Articles

- [RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap](RC-IMP-03_CSV-Upload-Reference.md) (index of all CSV upload types in REDCap)
- [RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md) (full module reference)
- [RC-ALERT-02 — Alert Management & Notification Log](RC-ALERT-02_Alert-Management-and-Notification-Log.md)
- [RC-PIPE-01 — Piping: Basics, Syntax & Field Types](RC-PIPE-01_Piping-Basics-Syntax-and-Field-Types.md) (piping syntax used in `email-to` and `alert-message`)
- [RC-SURV-04 — Survey Link Types & Access Methods](RC-SURV-04_Survey-Link-Types-and-Access-Methods.md) (survey link smart variable syntax)
