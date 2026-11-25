

**Smart Variables: Survey**

| **Article ID** | [RC-PIPE-08 — Smart Variables: Survey](RC-PIPE-08_Smart-Variables-Survey.md) |
|---|---|
| **Domain** | Piping |
| **Applies To** | All project types with surveys enabled |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — smart variable behaviour checked against source code; pages not re-captured |
| **Prerequisite** | [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md) |
| **Version** | 1.0 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md); [RC-PIPE-02 — Piping: Longitudinal, Repeated Instruments & Modifiers](RC-PIPE-02_Piping-Longitudinal-Repeated-Instruments-and-Modifiers.md); [RC-PIPE-07 — Smart Variables: Form](RC-PIPE-07_Smart-Variables-Form.md); [RC-PIPE-04 — Piping: Emails, Notifications & Logic Features](RC-PIPE-04_Piping-in-Emails-and-Notifications.md)|
| **Synonyms** | [survey-link] smart variable; how to pipe a survey link with [survey-link:instrument]; survey smart variables for access code [survey-access-code]; [survey-date-completed] and [survey-date-started] piping; how to show survey completion time with [survey-duration]; [is-survey] smart variable on a survey page; pipe a survey link or access code into an email; survey-level smart variables for links and timestamps |

---

## 1. Overview

Survey smart variables return information about surveys in REDCap — including survey links, access codes, timestamps for when surveys were started and completed, and the total time spent completing a survey. These variables are especially useful in survey invitation emails, confirmation messages, and field notes within surveys. Use them to dynamically generate survey URLs, reference participant progress, and personalize survey communications based on when participants engaged with the form.

---

## 2. Key Concepts & Definitions

**Survey**

A public-facing, link-based data collection instrument in REDCap. Unlike standard data entry forms (accessed by logged-in users), surveys can be distributed to participants who access the form via a unique link or QR code without a REDCap account.

**Survey Access Code**

A security token specific to each record/event/instance that grants access to a survey for that particular record. Access codes are unique per record and instrument, preventing participants from accidentally accessing another record's survey.

**Survey Return Code**

A security token that allows a participant to return to a partially completed survey (Save & Return Later feature). Return codes are different from access codes and serve a different purpose — they enable resumption of incomplete surveys.

**Survey Queue**

A feature in REDCap that displays all surveys available to a participant for a given record. The survey queue is a convenient way for participants to see and access multiple surveys associated with one enrollment.

**Survey Timestamps**

REDCap records when a survey is started, when it is completed, and how long the participant spent on the survey. These timestamps can be piped into other forms, emails, or calculated fields for tracking and follow-up purposes.

**Survey Duration**

The elapsed time from survey start to completion (or from start to current time if the survey is still in progress). Duration can be expressed in various units: seconds, minutes, hours, days, months, or years.

---

## 3. Smart Variable Reference

| Smart Variable | Syntax | Description | Example Output |
|---|---|---|---|
| Is Survey | `[is-survey]` | Returns 1 if the current instrument is being accessed as a survey; returns 0 if accessed as a data entry form. Always 0 in emails, alerts and background processing. Useful in branching logic. | 1 (or 0) |
| Survey URL (Current or Specified) | `[survey-url]` or `[survey-url:instrument]` | The web address (URL) for the specified survey. If `instrument` is omitted, the current instrument is used (see Usage Notes). Can be combined with event prefix: `[previous-event-name][survey-url:followup_survey]`. | https://redcap.yourinstitution.edu/surveys/?... |
| Survey Link (Current or Specified) | `[survey-link]`, `[survey-link:instrument]`, or `[survey-link:instrument:Custom Text]` | An HTML web link to the specified survey. Multiple syntax forms supported. Custom text is optional; if omitted, defaults to the survey title. Can be used as `[survey-link]` or `[survey-link:Custom Text]` when the current instrument is meant. Can be combined with event prefix: `[next-event-name][survey-link:followup_survey]`. | Follow-up Survey or Take the pre-screening survey |
| Survey Access Code (Current or Specified) | `[survey-access-code]` or `[survey-access-code:instrument]` | The unique access code for the specified survey for the current record/event/instance. If `instrument` is omitted, the current instrument is used. Can be combined with event prefix: `[previous-event-name][survey-access-code:followup_survey]`. | LDNP3EW7W |
| Survey Return Code (Current or Specified) | `[survey-return-code]` or `[survey-return-code:instrument]` | The unique return code allowing a participant to resume a partially completed survey (Save & Return Later). A code is returned even when Save & Return Later is not enabled, but it is of no use then. If `instrument` is omitted, the current instrument is used. Can be combined with event prefix. | TFX4E4YN |
| Survey Queue URL | `[survey-queue-url]` | The web address (URL) of the survey queue for the current record. Displays all surveys available to the participant. Blank if the Survey Queue is not enabled or the record has not been saved yet. | https://redcap.yourinstitution.edu/surveys/?... |
| Survey Queue Link | `[survey-queue-link]` or `[survey-queue-link:Custom Text]` | An HTML web link to the survey queue. Custom text is optional; if omitted, defaults to "Survey Queue Link". Blank if the Survey Queue is not enabled or the record has not been saved yet. | Survey Queue Link or View your survey progress |
| Survey Title (Current or Specified) | `[survey-title]` or `[survey-title:instrument]` | The title (display name) of the specified instrument as configured in survey settings. Blank if not in an instrument/survey context. | Enter to Win a New Car or Cardiology Study: Pre-Screening Survey |
| Survey Time Started (Specified) | `[survey-time-started:instrument]` or `[survey-time-started:instrument:value]` | The date and time the specified survey was started. In piping context, displays per user's date/time preferences. Append `:value` for raw YYYY-MM-DD HH:MM:SS format (better for logic). Returns blank if survey was never started, if the form was completed through data entry rather than as a survey, or if response began before REDCap collected start times. Can be combined with instance qualifier: `[survey-time-started:followup][last-instance]`. | 12/25/2018 09:00am or 2018-12-25 09:00:00 |
| Survey Date Started (Specified) | `[survey-date-started:instrument]` or `[survey-date-started:instrument:value]` | Date only (no time) the specified survey was started. Append `:value` for raw YYYY-MM-DD format. Can be combined with instance qualifier. | 12/25/2018 or 2018-12-25 |
| Survey Time Completed (Specified) | `[survey-time-completed:instrument]` or `[survey-time-completed:instrument:value]` | The date and time the specified survey was completed. Append `:value` for raw format. Returns blank if survey has not been completed. Can be combined with instance qualifier. | 12/25/2018 09:30am or 2018-12-25 09:30:00 |
| Survey Date Completed (Specified) | `[survey-date-completed:instrument]` or `[survey-date-completed:instrument:value]` | Date only the specified survey was completed. Append `:value` for raw format. Returns blank if not completed. Can be combined with instance qualifier. | 12/25/2018 or 2018-12-25 |
| Survey Duration | `[survey-duration:instrument]` or `[survey-duration:instrument:units]` | Time elapsed since the survey was started. Can be expressed in units: y (years), M (months), d (days), h (hours), m (minutes), s (seconds, default). For an unfinished survey it counts up to now, so the value keeps changing — run Data Quality rule H for accurate results. Can be combined with instance qualifier: `[visit_1_arm_1][survey-duration:prescreener][last-instance]`. | 845 or 2.34 |
| Survey Duration Completed | `[survey-duration-completed:instrument]` or `[survey-duration-completed:instrument:units]` | Total time to complete the survey (start to completion). Stays blank until the survey has been completed. Same unit options as survey-duration. | 93 or 12.7 or 3.89 |

---

## 4. Usage Notes

**Survey URL and Link Parameters**

When using `[survey-url:instrument]` or `[survey-link:instrument]`, replace `instrument` with the unique form name. If you omit the instrument, the survey link, URL, access code and return code variables use the current instrument: the form or survey page being viewed, the survey in a survey invitation, or the instrument that triggered an alert. They return blank only when there is no current instrument or the current instrument is not enabled as a survey. Including the instrument explicitly is still best practice, because it makes the link unambiguous wherever the text is reused.

A survey link for a record that does not exist yet is blank — the only exception is the public survey link to the first instrument.

**Custom Text in Survey Links**

Use `[survey-link:instrument:Custom Text]` to generate a link with custom text instead of the survey title. For example: `[survey-link:followup_survey:Complete the follow-up survey]`. If omitted, REDCap uses the survey's configured title.

**Event Prefixes in Longitudinal Projects**

In longitudinal projects, you can prepend an event name to a survey smart variable to reference a survey in a different event:
- `[baseline_arm_1][survey-link:demographics]`
- `[next-event-name][survey-url:visit_survey]`
- `[previous-event-name][survey-access-code:followup_survey]`

`[previous-event-name]` and `[next-event-name]` take the literally adjacent event, even if the survey is not designated in that event. `[first-event-name]` and `[last-event-name]` use the first or last event where the instrument is designated. When in doubt, use a specific unique event name.

See [RC-PIPE-02 — Piping: Longitudinal, Repeated Instruments & Modifiers](RC-PIPE-02_Piping-Longitudinal-Repeated-Instruments-and-Modifiers.md) for details on event prefixes.

**Survey Timestamp Formats**

By default, piped survey timestamps display per the logged-in user's date/time preferences. Where there is no logged-in user (survey pages, alerts sent in the background), they display in the system default date format. To display the raw `YYYY-MM-DD HH:MM:SS` format instead, append `:value`:
- `[survey-time-started:instrument:value]` → `2018-12-25 09:00:00`
- `[survey-date-completed:instrument:value]` → `2018-12-25`

In calculations, branching logic and other logic, survey timestamps are always used in raw Y-M-D format, so `:value` is optional (and harmless) there. It only changes what is displayed when the timestamp is piped into text.

Survey timestamps come only from survey responses. If a form was completed through data entry rather than as a survey, they are blank.

**Missing Start Times**

If a survey response began before REDCap started collecting start times (in older responses), `[survey-time-started]` and `[survey-date-started]` return blank. Plan your logic accordingly when working with historical data.

**Survey Duration Units**

When specifying units for duration, use only the letter code without quotes:
- `[survey-duration:prescreener:s]` → seconds
- `[survey-duration:prescreener:m]` → minutes
- `[survey-duration:prescreener:h]` → hours
- `[survey-duration:prescreener:d]` → days
- `[survey-duration:prescreener:M]` → months
- `[survey-duration:prescreener:y]` → years

If no unit is given, seconds are used. Do NOT use quotes around the unit code, and check its case (`m` is minutes, `M` is months): an unrecognised unit silently falls back to seconds.

**Instance Qualifiers for Repeating Surveys**

In projects with repeating instruments, you can append instance qualifiers to survey smart variables:
- `[survey-time-started:followup_survey][last-instance]` — start time of the last instance
- `[survey-duration-completed:prescreener][current-instance]` — duration of the current instance

See [RC-PIPE-10 — Smart Variables: Repeating Instruments and Events](RC-PIPE-10_Smart-Variables-Repeating-Instruments-and-Events.md) for more on instance qualifiers.

**Dynamically Changing Duration in Calculated Fields**

If you place `[survey-duration:instrument]` in a calculated field for a survey that is still in progress, the value will change every time the record is saved. Use a Data Quality rule (Rule H) to capture the final, accurate duration once the survey is completed. `[survey-duration]` on an unfinished survey counts up to now; `[survey-duration-completed]` stays blank until the survey is completed.

**Survey Timestamp Context**

Survey timestamps are most meaningful after a survey has been started or completed. Avoid piping survey-completion timestamps into fields that appear before the survey has been accessed; they will be blank.

---

## 5. Common Questions

**Q: How do I send a participant a link to a survey in an email invitation?**

**A:** Use `[survey-link:instrument:Custom Text]` in your email body. For example:
```
Dear participant,

Please complete the enrollment survey by clicking this link:
[survey-link:enrollment_survey:Start Enrollment Survey]

Your access code is: [survey-access-code:enrollment_survey]
```

**Q: What is the difference between `[survey-access-code]` and `[survey-return-code]`?**

**A:** The access code grants initial access to the survey. The return code allows a participant to resume a partially completed survey (Save & Return Later). Both are unique to the record/event/instance combination. Provide the return code only for surveys that have Save & Return Later enabled — REDCap returns a code even when it is not enabled, but the participant cannot use it.

**Q: Can I use survey smart variables in branching logic?**

**A:** Yes, some survey smart variables work in logic. For example, `[is-survey]=1` shows fields only in survey mode. Timestamp and duration smart variables also work in logic, but are less commonly used there. Most branching logic uses survey smart variables for conditional display based on access context.

**Q: How do I display when a participant completed a survey in a confirmation email?**

**A:** Use `[survey-time-completed:instrument]` or `[survey-date-completed:instrument]` in your email body. For example:
```
Thank you for completing the survey on [survey-date-completed:enrollment_survey].
```

If the survey has not been completed, the variable will be blank.

**Q: I have a repeating survey. How do I reference a specific instance?**

**A:** Append an instance qualifier: `[survey-time-started:followup_survey][last-instance]` references the start time of the last instance. See [RC-PIPE-10 — Smart Variables: Repeating Instruments and Events](RC-PIPE-10_Smart-Variables-Repeating-Instruments-and-Events.md) for all instance qualifier options.

**Q: What is the survey queue, and how do I link to it?**

**A:** The survey queue displays all surveys available to a participant for a given record. Use `[survey-queue-link]` or `[survey-queue-url]` to generate a link to the queue in an email or form. This is useful if you want participants to see all their available surveys at once. Both are blank if the Survey Queue is not enabled or the record has not been saved yet.

**Q: Can I use the `:value` format for survey timestamps in field labels or emails?**

**A:** Yes, but it displays the raw format (YYYY-MM-DD HH:MM:SS). If you want a formatted, human-readable timestamp for display to participants, omit `:value` and let REDCap apply the user's date format (or the system default format when no user is logged in). In calculated fields and logic, `:value` is optional because timestamps are always used in raw format there.

---

## 6. Common Mistakes & Gotchas

**Omitting the instrument name where there is no current survey.** Without an instrument, `[survey-link]`, `[survey-url]`, `[survey-access-code]` and `[survey-return-code]` use the current instrument (the form or survey page, the survey in an invitation, or the instrument that triggered an alert). They are blank when there is no current instrument or the current instrument is not enabled as a survey. Best practice is to name the instrument explicitly: `[survey-link:enrollment_survey]` rather than `[survey-link]`.

**Expecting a survey link for a record that does not exist yet.** Survey links for a not-yet-created record are blank, except the public survey link to the first instrument.

**Using `[previous-event-name]` or `[next-event-name]` before a survey link.** These take the literally adjacent event, even if the survey is not designated there, which can produce a blank or unexpected link. `[first-event-name]` and `[last-event-name]` use the first or last event where the instrument is designated. Prefer a specific unique event name.

**Confusing survey smart variables with form smart variables.** Survey variables like `[survey-link]` are for public survey access. Form variables like `[form-link]` are for data entry forms. Using the wrong type in an email or form may not produce the intended result. See [RC-PIPE-07 — Smart Variables: Form](RC-PIPE-07_Smart-Variables-Form.md) for form smart variables.

**Not testing survey links in survey invitations.** Survey links can be long and complex. Always test survey invitations in a development environment before sending them to real participants to ensure links are valid and access codes work correctly.

**Using survey-completion timestamps before surveys are completed.** If you pipe `[survey-time-completed:instrument]` in a field that appears before participants complete the survey, it will be blank. Plan your data flow carefully and only reference completion timestamps after the survey step.

**Expecting `:value` to matter in calculations.** In calculations, branching logic and other logic, survey timestamps are always used in raw Y-M-D format, so `:value` is optional there. It only changes what is displayed when the timestamp is piped into text.

**Expecting survey timestamps for data-entry forms.** Survey timestamp variables come only from survey responses. If a form was completed through data entry instead of as a survey, they are blank.

**Mistyping the duration unit.** Units are s, m, h, d, M (months) and y; the default is seconds. An unrecognised unit (for example `min`) silently falls back to seconds.

**Relying on `[is-survey]` in emails.** `[is-survey]` is always 0 in emails, alerts and background processing.

**Offering a return code without Save & Return Later.** `[survey-return-code]` returns a code even when Save & Return Later is not enabled, but the code is useless then. Only use it for surveys with Save & Return Later turned on.

**Not accounting for blank start times in historical data.** Very old survey responses may have blank start time values because REDCap did not always collect them. If your logic relies on survey start times, handle the blank case gracefully or filter out historical data.

**Assuming survey duration is final in partially completed surveys.** In a calculated field, `[survey-duration:instrument]` for an incomplete survey counts up to now and changes every time the form is saved. Use `[survey-duration-completed:instrument]` (blank until completion) or Data Quality rule H to capture the final duration once the survey is submitted.

---

## 7. Related Articles

- [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md) (overview of all smart variable categories)
- [RC-PIPE-02 — Piping: Longitudinal, Repeated Instruments & Modifiers](RC-PIPE-02_Piping-Longitudinal-Repeated-Instruments-and-Modifiers.md) (event prefixes and instance qualifiers)
- [RC-PIPE-07 — Smart Variables: Form](RC-PIPE-07_Smart-Variables-Form.md) (form-specific smart variables for comparison)
- [RC-PIPE-10 — Smart Variables: Repeating Instruments and Events](RC-PIPE-10_Smart-Variables-Repeating-Instruments-and-Events.md) (instance qualifiers for repeating surveys)
- [RC-PIPE-04 — Piping: Emails, Notifications & Logic Features](RC-PIPE-04_Piping-in-Emails-and-Notifications.md) (using survey smart variables in survey invitations)
