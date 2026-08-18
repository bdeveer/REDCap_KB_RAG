

**Alerts & Notifications CSV — Column Reference and Format Guide**

| **Article ID** | [RC-IMP-05 — Alerts & Notifications CSV — Column Reference and Format Guide](RC-IMP-05_Alerts-Notifications-CSV.md) |
|---|---|
| **Domain** | Data Import |
| **Applies To** | All REDCap project types |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.4.1 (Standard) / v17.3.7 (LTS) — changelog review; page not re-captured |
| **Prerequisite** | [RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap](RC-IMP-03_CSV-Upload-Reference.md); [RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md) |
| **Skill Level** | Intermediate |
| **Version** | 1.2 |
| **Last Updated** | 2026-07-27 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap](RC-IMP-03_CSV-Upload-Reference.md); [RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md); [RC-ALERT-02 — Alert Management & Notification Log](RC-ALERT-02_Alert-Management-and-Notification-Log.md)|
| **Synonyms** | how do i import alerts via csv; bulk edit alerts and notifications in a spreadsheet; copy alert configurations from one project to another; upload alert definitions csv; alert-unique-id column format for import; export and re-import alerts and notifications; duplicate alerts across projects without rebuilding; a&n csv column reference |

---

## 1. Overview

The Alerts & Notifications module supports CSV export and import of alert definitions. This allows bulk editing of alerts outside of REDCap and copying alert configurations from one project to another without rebuilding them by hand.

**Location:** Applications → Alerts & Notifications → "Upload or download alerts" button.

**Upload behavior — Additive:** Imported alerts are added to the existing list. Existing alerts are not overwritten unless you are re-importing with matching `alert-unique-id` values.

**Rights required:** Project Design and Setup.

**Always download first.** Start from a file exported from the source project rather than building from scratch. This guarantees the correct column order and gives you a recovery snapshot.

For general coverage of the Alerts & Notifications module, see [RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md).

---

## 2. Column Reference

Each row in the file represents one alert. The table below documents every column.

| Column | Required | Accepted Values / Notes |
|---|---|---|
| `alert-unique-id` | No (new) / Yes (update) | REDCap-assigned identifier in the format `A-XXXX` (e.g., `A-2482`). Leave blank when creating new alerts — REDCap assigns the ID on import. Required when updating or copying specific existing alerts. |
| `alert-title` | No | Free-text display name. Optional but strongly recommended; this is the primary identifier in the Alerts management view and the notification log. |
| `alert-trigger` | Yes | `SUBMIT` — completion or combination trigger (fires on instrument save). `LOGIC` — logic trigger (fires when logic becomes true, regardless of save source, including imports and API writes). |
| `unique-form-name` | Yes (SUBMIT) | The instrument's unique name (variable name, not display label). Required for `SUBMIT` triggers; specifies which instrument save activates the alert. |
| `unique-event-name` | No | The event's unique name (e.g., `baseline_arm_1`). Leave blank for classic (non-longitudinal) projects. When blank in a longitudinal project, the alert applies to any event where the instrument appears. Event context for recipients and message content is specified via piping syntax inside `email-to` and `alert-message` instead. |
| `saved-with-form-status` | No | `COMPLETE` — fires only when the instrument is saved with Complete status (value 2). Leave blank to fire on any save status. |
| `alert-condition` | No | Logic expression string (same syntax as branching logic). Required for combination triggers and logic triggers. Leave blank for pure completion triggers. |
| `ensure-logic-still-true` | Yes | `Y` or `N`. When `Y`, REDCap re-evaluates the trigger logic immediately before sending. If the logic is no longer true at send time, the queued alert is cancelled. Most useful when the alert has a scheduled delay. |
| `do-not-clear-recurrences` | Yes | `Y` or `N`. Controls whether a new trigger event clears previously queued recurrences for the same record. |
| `alert-stop-type` | Yes | Trigger limit — how many times the alert can fire per record. `RECORD` — once per record. Additional values for longitudinal/repeated projects include `EVENT` (once per event), `INSTANCE` (once per repeat instance), and `EVENT_INSTANCE` (once per event-instance combination). |
| `send-on` | Yes | When to send after the trigger fires. `NOW` — immediately. `TIME_LAG` — after a specified delay (configure with `send-on-time-lag-days`, `send-on-time-lag-hours`, `send-on-time-lag-minutes`). `NEXT_DAY` — next occurrence of a specified day type (configure with `send-on-next-day-type` and `send-on-next-time`). `EXACT_DATE` — at a specific date/time (configure with `send-on-date`). `FIELD` — relative to a date stored in a project field (configure with `send-on-field`). |
| `send-on-next-day-type` | Conditional | Day-type value for `NEXT_DAY` sends (e.g., weekday, Monday). Leave blank otherwise. |
| `send-on-next-time` | Conditional | Time component (HH:MM) for `NEXT_DAY` sends. Leave blank otherwise. |
| `send-on-time-lag-days` | Conditional | Number of days for `TIME_LAG` delay. All three lag columns (`days`, `hours`, `minutes`) must be specified together — use `0` for units not needed. |
| `send-on-time-lag-hours` | Conditional | Hours component of `TIME_LAG` delay. Use `0` if not needed. |
| `send-on-time-lag-minutes` | Conditional | Minutes component of `TIME_LAG` delay. Use `0` if not needed. |
| `send-on-field-after` | Conditional | Direction for `TIME_LAG` sends: `after` (send N days/hours/minutes after the trigger). Leave blank for `NOW` sends. |
| `send-on-field` | Conditional | The project field name used as a reference date for `FIELD` sends. Leave blank otherwise. |
| `send-on-date` | Conditional | Specific date/time for `EXACT_DATE` sends (server time zone applies). Leave blank otherwise. |
| `alert-send-how-many` | Yes | `ONCE` — send a single time per trigger event. `MULTIPLE` — send on a recurring basis (configure with `every-time-type`, `repeat-for`, `repeat-for-units`, `repeat-for-max`). |
| `every-time-type` | Conditional | Required when `alert-send-how-many` = `MULTIPLE`. The unit for the recurrence interval. |
| `repeat-for` | Conditional | Numeric interval between recurring sends. |
| `repeat-for-units` | Conditional | Unit for `repeat-for` (days, hours, or minutes). |
| `repeat-for-max` | Conditional | Maximum number of sends including the first. **Always set this** — leaving it blank causes REDCap to send indefinitely. |
| `alert-expiration` | No | Date/time after which REDCap will not send any further instances of this alert, and will cancel any already-queued ones. |
| `alert-type` | Yes | `EMAIL` — standard email (always available). `SMS` — text message (if enabled). `VOICE` — voice call (if enabled). `SENDGRID` — SendGrid delivery (if configured). |
| `email-from-display` | No | Optional display name for the from address (e.g., `Heart Study Team`). Leave blank to use the raw email address as the display name. |
| `email-from` | Yes (email) | The from email address. Must be an address associated with a current project user's REDCap profile. |
| `email-to` | Yes (email) | Recipient(s). Accepts: a static email address; a project field variable (`[field_name]`); or an event-prefixed field variable for longitudinal projects (`[event_name][field_name]`, e.g., `[baseline_arm_1][contact_email]`). Multiple recipients separated by semicolons. |
| `email-cc` | No | CC recipient(s). Same syntax as `email-to`. |
| `email-bcc` | No | BCC recipient(s). Same syntax as `email-to`. |
| `email-failed` | No | Email address to notify if REDCap fails to deliver the alert. Only one address is accepted. |
| `email-subject` | Yes (email) | Subject line. Supports piping syntax. Avoid piping identifiers here unless the `prevent-piping-identifiers` column is set to `N`. |
| `alert-message` | Yes | The message body. Supports HTML, piped variables, and smart variables (e.g., `[survey-link:instrument_name:Link text]`). In longitudinal projects, prefix survey link smart variables with the target event: `[event_name][survey-link:instrument_name:Link text]`. The field can span multiple lines in the CSV — the entire value is quoted. |
| `sendgrid-template-id` | No | SendGrid template ID. Leave blank for standard email alerts. |
| `sendgrid-template-data` | Yes | JSON object. Use `{}` when not supplying SendGrid template variables. **Do not leave blank** — an empty JSON object is required. |
| `sendgrid-mail-send-configuration` | Yes | JSON object. Use `{}` when not using custom SendGrid mail send configuration. **Do not leave blank.** |
| `prevent-piping-identifiers` | Yes | `Y` or `N`. When `Y` (the default in the UI), REDCap strips identifier field values from piped content before sending. Set to `N` only when intentional identifier piping has been confirmed as appropriate with your IRB. |
| `file-upload-fields` | No | Comma-separated list of file upload field names. Files stored in these fields for the triggering record are attached to the alert email. Leave blank if no attachments are needed. |
| `phone-number-to` | Conditional | Phone number for SMS or voice call alerts. Leave blank for email. |
| `alert-deactivated` | Yes | `Y` — alert is inactive and will not fire. `N` — alert is active. |

---

## 3. Annotated Example

The file below contains two alerts from a longitudinal project with two arms (`baseline_arm_1` and `3_month_arm_1`):

**Alert A-2482 — "Invite baseline"**
Fires immediately when the `screening` form is saved with Complete status. Sends once per record. Emails the participant at the address stored in `[baseline_arm_1][contact_email]`. The message body contains a survey link to the `demographics` instrument at the baseline event.

**Alert A-2483 — "Invite 3 months"**
Same trigger as A-2482 (screening form Complete), but scheduled to send 90 days later (`TIME_LAG`, 90 days, 0 hours, 0 minutes). The message links to the `phq9` instrument at the `3_month_arm_1` event. The event prefix on the survey link (`[3_month_arm_1][survey-link:phq9:Start here]`) ensures REDCap generates a link to the correct event, not the baseline event.

```csv
alert-unique-id,alert-title,alert-trigger,unique-form-name,unique-event-name,saved-with-form-status,alert-condition,ensure-logic-still-true,do-not-clear-recurrences,alert-stop-type,send-on,send-on-next-day-type,send-on-next-time,send-on-time-lag-days,send-on-time-lag-hours,send-on-time-lag-minutes,send-on-field-after,send-on-field,send-on-date,alert-send-how-many,every-time-type,repeat-for,repeat-for-units,repeat-for-max,alert-expiration,alert-type,email-from-display,email-from,email-to,email-cc,email-bcc,email-failed,email-subject,alert-message,sendgrid-template-id,sendgrid-template-data,sendgrid-mail-send-configuration,prevent-piping-identifiers,file-upload-fields,phone-number-to,alert-deactivated
A-2482,"Invite baseline",SUBMIT,screening,,COMPLETE,,N,N,RECORD,NOW,,,,,,,,,ONCE,,,,,,EMAIL,,study@institution.edu,[baseline_arm_1][contact_email],,,,"Invite for baseline","<p>Hi,</p><p>Please complete the baseline forms:</p><p>[baseline_arm_1][survey-link:demographics:Start here]</p><p>thanks,</p><p>Study team</p>",,{},{},N,,,N
A-2483,"Invite 3 months",SUBMIT,screening,,COMPLETE,,N,N,RECORD,TIME_LAG,,,90,0,0,after,,,ONCE,,,,,,EMAIL,,study@institution.edu,[baseline_arm_1][contact_email],,,,"Invite for 3 months","<p>Hi,</p><p>Please complete the 3-month forms:</p><p>[3_month_arm_1][survey-link:phq9:Start here]</p><p>thanks,</p><p>Study team</p>",,{},{},N,,,N
```

---

## 4. Common Mistakes

**Leaving `sendgrid-template-data` and `sendgrid-mail-send-configuration` blank.** These columns must contain a JSON object. Use `{}` when not using SendGrid features. A blank cell here can cause import errors.

**Omitting the event prefix on `email-to` in a longitudinal project.** Writing `[contact_email]` without an event prefix may resolve to the wrong event or fail entirely if the field appears at multiple events. Always use `[event_name][field_name]` form for longitudinal recipients.

**Omitting the event prefix in `alert-message` survey links.** `[survey-link:phq9]` without an event prefix is ambiguous in a longitudinal project where the instrument appears at multiple events. Always write `[event_name][survey-link:instrument_name:Link text]`.

**Specifying only `send-on-time-lag-days` for a TIME_LAG send.** All three lag columns — days, hours, and minutes — must be present. Use `0` for the units you don't need; don't leave them blank.

**Leaving `alert-send-how-many` blank or omitting the repeat cap.** For recurring alerts, always set `repeat-for-max`. Without it, REDCap sends indefinitely.

**Building the import file from scratch instead of from an export.** The exact column set varies by project type — a classic (non-longitudinal) project's export omits `unique-event-name`, so its template has one fewer column than a longitudinal project's. Uploading a file whose columns don't match the destination project's template causes the rows to misalign during parsing and the import to fail, often with a misleading error that points at an unrelated field (for example, an email column) rather than at the column count. Always download an existing alert from the destination project first and edit that file, so the column set matches exactly. This is the same reason Section 1 advises "Always download first."

**Using the wrong capitalization in `email-from`.** REDCap validates the alert sender with a case-sensitive, exact-string match against the addresses on the sending user's profile (primary plus additional emails). An address stored in lowercase (e.g., `redcap@yale.edu`) is rejected with "Alert sender is invalid" if it is entered with different casing (e.g., `REDCap@yale.edu`), even though the address genuinely exists on the profile. Match the stored casing exactly.

**Pro tip — splitting one existing alert into two or more.** If you need to break an existing alert's scope into separate alerts (for example, an alert covering two instance/branch conditions gets split into one alert per condition so each can have its own message body), you don't need to invent brand-new IDs for all of them. Reuse the existing alert's ID for one of the new conditions — narrow its `alert-condition` logic and edit its message as needed — and leave `alert-unique-id` **blank** on the additional row(s) for the new condition(s) you're spinning off. This preserves the original alert's send history/notification-log continuity for the condition that stays on its ID, while cleanly creating the rest as new alerts. Inventing IDs for the new rows (rather than reusing a real one or leaving the column blank) will fail on import with "unique alert ID does not exist."

---

## 5. Related Articles

- [RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap](RC-IMP-03_CSV-Upload-Reference.md)(index of all CSV upload types in REDCap)
- [RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md) (full module reference)
- [RC-ALERT-02 — Alert Management & Notification Log](RC-ALERT-02_Alert-Management-and-Notification-Log.md)
- [RC-PIPE-01 — Piping: Basics, Syntax & Field Types](RC-PIPE-01_Piping-Basics-Syntax-and-Field-Types.md)(piping syntax used in `email-to` and `alert-message`)
- [RC-SURV-04 — Survey Link Types & Access Methods](RC-SURV-04_Survey-Link-Types-and-Access-Methods.md)(survey link smart variable syntax)
